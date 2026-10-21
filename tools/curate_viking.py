#!/usr/bin/env python3
"""Deterministically materialize the partial Bally Viking (1979) artifacts.

The definition and recreation note are reviewed seeds.  This tool intentionally
does not reinterpret those facts: it deep-copies and fail-closed validates the
definition seed, then writes canonical products and a spatial blocker report.
``--check`` is read-only; ``--regenerate`` never removes a stale twin and
refuses every author-ready target.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
from collections.abc import Iterator, Mapping
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from jsonschema import Draft202012Validator  # noqa: E402

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

MACHINE_ID = "bally.viking.1979"
PHYSICAL_RELEASE_YEAR = 1980
ROOT_DRIVER_ID = "viking"
ROOT_DRIVER_RELEASE_YEAR = "1980"

DEFINITION_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "viking-1979.json"
KNOWLEDGE_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "viking-1979-knowledge.md"
SPATIAL_SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "viking-1979-spatial.json"
SCHEMA_PATH = ROOT / "schemas" / "machine.schema.json"

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "viking-1979.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "viking-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "viking-1979.md"
REPORT_JSON_PATH = ROOT / "reports" / "spatial" / "bally" / "viking-1979.json"
REPORT_MD_PATH = ROOT / "reports" / "spatial" / "bally" / "viking-1979.md"

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
EXTERNAL_ROOTS = {"vpx_sources", "manuals", "review_artifacts"}


class CuratorError(RuntimeError):
    """An incomplete seed or unsafe output condition."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CuratorError(message)


def _read_json(path: Path, label: str) -> Any:
    try:
        return load_json(path)
    except FileNotFoundError as error:
        raise CuratorError(f"{label} is missing: {path}") from error
    except json.JSONDecodeError as error:
        raise CuratorError(f"{label} is not valid JSON: {path}: {error}") from error


def _repository_file(relative: str, label: str) -> Path:
    _require("\\" not in relative, f"{label} must use a repository-relative POSIX path: {relative!r}")
    pure = PurePosixPath(relative)
    _require(not pure.is_absolute() and ".." not in pure.parts, f"{label} leaves the repository: {relative!r}")
    candidate = ROOT.joinpath(*pure.parts)
    try:
        candidate.resolve().relative_to(ROOT.resolve())
    except ValueError as error:
        raise CuratorError(f"{label} leaves the repository: {relative!r}") from error
    return candidate


def _walk_source_refs(value: Any, path: str = "$") -> Iterator[tuple[str, list[Any]]]:
    if isinstance(value, Mapping):
        if "source_refs" in value:
            refs = value["source_refs"]
            yield f"{path}.source_refs", refs if isinstance(refs, list) else []
            if not isinstance(refs, list):
                raise CuratorError(f"{path}.source_refs must be a list")
        for key, child in value.items():
            yield from _walk_source_refs(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_source_refs(child, f"{path}[{index}]")


def _validate_schema(definition: dict[str, Any]) -> None:
    schema = _read_json(SCHEMA_PATH, "machine schema")
    _require(isinstance(schema, dict), "machine schema must be a JSON object")
    errors = sorted(Draft202012Validator(schema).iter_errors(definition), key=lambda error: list(error.absolute_path))
    if errors:
        rendered = "; ".join(f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}" for error in errors[:5])
        raise CuratorError(f"definition seed does not satisfy schema v2: {rendered}")


def _validate_sources_and_excerpts(definition: dict[str, Any]) -> None:
    sources = definition.get("sources")
    _require(isinstance(sources, list) and sources, "definition seed requires sources")
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        _require(isinstance(source, dict), f"sources[{index}] must be an object")
        source_id = source.get("id")
        _require(isinstance(source_id, str) and source_id, f"sources[{index}].id is required")
        _require(source_id not in source_ids, f"duplicate source id: {source_id}")
        source_ids.add(source_id)
        excerpts = source.get("excerpts", [])
        _require(isinstance(excerpts, list), f"source {source_id}.excerpts must be a list")
        for excerpt_index, excerpt in enumerate(excerpts):
            prefix = f"source {source_id}.excerpts[{excerpt_index}]"
            _require(isinstance(excerpt, dict), f"{prefix} must be an object")
            path = excerpt.get("path")
            digest = excerpt.get("sha256")
            _require(isinstance(path, str) and path, f"{prefix}.path is required")
            _require(isinstance(digest, str) and SHA256.fullmatch(digest) is not None, f"{prefix}.sha256 must be a SHA-256")
            excerpt_path = _repository_file(path, f"{prefix}.path")
            _require(excerpt_path.is_file(), f"{prefix} file is missing: {path}")
            _require(file_sha256(excerpt_path) == digest, f"{prefix} hash mismatch: {path}")
            if "image" in excerpt:
                image = excerpt["image"]
                image_digest = excerpt.get("image_sha256")
                _require(isinstance(image, str) and image, f"{prefix}.image must be a path")
                _require(isinstance(image_digest, str) and SHA256.fullmatch(image_digest) is not None, f"{prefix}.image_sha256 must be a SHA-256")
                image_path = _repository_file(image, f"{prefix}.image")
                _require(image_path.is_file(), f"{prefix} image is missing: {image}")
                _require(file_sha256(image_path) == image_digest, f"{prefix} image hash mismatch: {image}")
    for path, refs in _walk_source_refs(definition):
        _require(refs, f"{path} must name at least one source")
        unknown = sorted({ref for ref in refs if not isinstance(ref, str) or ref not in source_ids})
        _require(not unknown, f"{path} contains unknown source reference(s): {unknown}")


def _validate_definition(definition: dict[str, Any]) -> None:
    _require(isinstance(definition, dict), "definition seed must be a JSON object")
    _validate_schema(definition)
    _require(definition.get("schema_version") == 2, "definition seed must be schema_version 2")
    machine = definition.get("machine")
    _require(isinstance(machine, dict), "definition seed requires machine")
    _require(machine.get("id") == MACHINE_ID, f"machine.id must be {MACHINE_ID}")
    _require(machine.get("year") == PHYSICAL_RELEASE_YEAR, f"machine.year must be physical release year {PHYSICAL_RELEASE_YEAR}")
    coverage = definition.get("coverage")
    _require(isinstance(coverage, dict) and coverage.get("status") == "partial", "Viking must remain partial for now")
    drivers = definition.get("drivers")
    _require(isinstance(drivers, list), "definition seed requires drivers")
    root_driver = next((driver for driver in drivers if isinstance(driver, dict) and driver.get("id") == ROOT_DRIVER_ID), None)
    _require(root_driver is not None, "definition seed requires root driver viking")
    _require(root_driver.get("year") == ROOT_DRIVER_RELEASE_YEAR, "root driver viking must retain its 1980 release year")
    _validate_sources_and_excerpts(definition)
    errors = validate_machine(definition, ROOT)
    _require(not errors, "definition seed failed repository validation: " + "; ".join(errors[:8]))


def build_definition() -> dict[str, Any]:
    """Load a fresh deep copy so callers can never mutate the parsed seed."""
    seed = _read_json(DEFINITION_SEED_PATH, "definition seed")
    definition = copy.deepcopy(seed)
    _validate_definition(definition)
    return definition


def build_knowledge() -> bytes:
    try:
        knowledge = KNOWLEDGE_SEED_PATH.read_bytes()
    except FileNotFoundError as error:
        raise CuratorError(f"knowledge seed is missing: {KNOWLEDGE_SEED_PATH}") from error
    _require(knowledge, "knowledge seed must not be empty")
    try:
        decoded = knowledge.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CuratorError("knowledge seed must be UTF-8") from error
    _require(decoded.strip(), "knowledge seed must not be blank")
    return knowledge


def _validate_spatial_seed(seed: Any) -> dict[str, Any]:
    _require(isinstance(seed, dict), "spatial seed must be a JSON object")
    required = {
        "bounds",
        "table_sha256",
        "extraction_manifest_sha256",
        "extraction_inventory",
        "objects",
        "evidence_artifacts",
        "projection_disclosures",
        "unresolved",
        "transformation",
    }
    _require(required <= set(seed), f"spatial seed is incomplete; missing {sorted(required - set(seed))}")
    bounds = seed["bounds"]
    _require(isinstance(bounds, dict) and set(bounds) == {"left", "top", "right", "bottom"}, "spatial seed bounds must contain exactly left, top, right and bottom")
    for name, value in bounds.items():
        _require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), f"spatial seed bounds.{name} must be finite")
    _require(bounds["right"] > bounds["left"] and bounds["bottom"] > bounds["top"], "spatial seed bounds must have positive width and height")
    for key in ("table_sha256", "extraction_manifest_sha256"):
        _require(isinstance(seed[key], str) and SHA256.fullmatch(seed[key]) is not None, f"spatial seed {key} must be a SHA-256")
    inventory = seed["extraction_inventory"]
    _require(isinstance(inventory, dict), "spatial seed extraction_inventory must be an object")
    for key in ("file_count", "total_bytes", "raw_gameitem_count"):
        value = inventory.get(key)
        _require(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"spatial seed extraction_inventory.{key} must be a positive integer")
    objects = seed["objects"]
    _require(isinstance(objects, list) and objects, "spatial seed objects must be a non-empty list")
    names: set[str] = set()
    for index, item in enumerate(objects):
        prefix = f"spatial seed objects[{index}]"
        _require(isinstance(item, dict), f"{prefix} must be an object")
        _require(set(("name", "path", "raw_x", "raw_y", "x", "y")) <= set(item), f"{prefix} is incomplete")
        name = item["name"]
        _require(isinstance(name, str) and name and name not in names, f"{prefix}.name must be unique")
        names.add(name)
        _require(isinstance(item["path"], str) and item["path"], f"{prefix}.path must be a non-empty relative path")
        path = PurePosixPath(item["path"])
        _require(not path.is_absolute() and ".." not in path.parts and "\\" not in item["path"], f"{prefix}.path must stay relative")
        for coordinate in ("raw_x", "raw_y", "x", "y"):
            value = item[coordinate]
            _require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), f"{prefix}.{coordinate} must be finite")
        _require(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1, f"{prefix} normalized coordinates must be in range")
    artifacts = seed["evidence_artifacts"]
    _require(isinstance(artifacts, list) and artifacts, "spatial seed evidence_artifacts must be a non-empty list")
    for index, artifact in enumerate(artifacts):
        prefix = f"spatial seed evidence_artifacts[{index}]"
        _require(isinstance(artifact, dict) and set(artifact) == {"root", "path", "sha256"}, f"{prefix} must contain exactly root, path and sha256")
        _require(artifact["root"] in EXTERNAL_ROOTS, f"{prefix}.root is not an approved external root")
        _require(isinstance(artifact["path"], str) and artifact["path"], f"{prefix}.path is required")
        path = PurePosixPath(artifact["path"])
        _require(not path.is_absolute() and ".." not in path.parts and "\\" not in artifact["path"], f"{prefix}.path must stay relative")
        _require(isinstance(artifact["sha256"], str) and SHA256.fullmatch(artifact["sha256"]) is not None, f"{prefix}.sha256 must be a SHA-256")
    vpx_paths = [artifact["path"] for artifact in artifacts if artifact["root"] == "vpx_sources"]
    _require(any(path == "bally/viking-1979/extracted" or path.startswith("bally/viking-1979/extracted/") for path in vpx_paths), "spatial seed must pin the Viking table extraction under bally/viking-1979/extracted")
    for key in ("projection_disclosures", "unresolved"):
        values = seed[key]
        _require(isinstance(values, list) and all(isinstance(value, str) and value.strip() for value in values), f"spatial seed {key} must be a list of non-blank strings")
    _require(seed["unresolved"], "partial Viking spatial seed must state explicit unresolved blockers")
    _require(isinstance(seed["transformation"], str) and seed["transformation"].strip(), "spatial seed transformation must be a non-blank string")
    return seed


def load_spatial_seed() -> dict[str, Any]:
    return _validate_spatial_seed(copy.deepcopy(_read_json(SPATIAL_SEED_PATH, "spatial seed")))


def _devices(definition: dict[str, Any]) -> Iterator[tuple[str, dict[str, Any]]]:
    for collection_name in ("inputs", "outputs"):
        for device in definition.get(collection_name, []):
            if isinstance(device, dict):
                yield collection_name[:-1], device


def _is_used_physical_playfield_candidate(device: dict[str, Any]) -> bool:
    if device.get("availability") != "used" or not isinstance(device.get("physical"), dict):
        return False
    spatial = device.get("spatial")
    return not (isinstance(spatial, dict) and spatial.get("status") == "not_applicable")


def _source_hashes(definition: dict[str, Any]) -> dict[str, str]:
    return {
        source["id"]: source["sha256"]
        for source in definition["sources"]
        if isinstance(source, dict) and isinstance(source.get("id"), str) and isinstance(source.get("sha256"), str)
    }


def build_report(definition: dict[str, Any]) -> tuple[dict[str, Any], str]:
    spatial_seed = load_spatial_seed()
    located: list[tuple[str, dict[str, Any]]] = []
    unplaced: list[dict[str, Any]] = []
    controlled_na: list[dict[str, Any]] = []
    for collection, device in _devices(definition):
        device_id = device.get("id")
        if not isinstance(device_id, str):
            continue
        spatial = device.get("spatial")
        if isinstance(spatial, dict) and spatial.get("status") == "not_applicable":
            provenance = spatial.get("provenance", {})
            controlled_na.append({
                "id": device_id,
                "collection": collection,
                "reason": spatial.get("reason"),
                "source_refs": list(provenance.get("source_refs", [])) if isinstance(provenance, dict) else [],
            })
        if not _is_used_physical_playfield_candidate(device):
            continue
        placements = spatial.get("placements", []) if isinstance(spatial, dict) else []
        if isinstance(placements, list) and placements:
            located.append((collection, device))
        else:
            unplaced.append({
                "id": device_id,
                "collection": collection,
                "kind": device.get("kind"),
                "binding": copy.deepcopy(device.get("binding")),
            })
    located_counts = {
        "physical_used_playfield_devices": len(located),
        "physical_used_playfield_placements": sum(len(device["spatial"]["placements"]) for _, device in located),
        "inputs": sum(collection == "input" for collection, _ in located),
        "outputs": sum(collection == "output" for collection, _ in located),
    }
    report = {
        "format": "pinmame-spatial-blockers",
        "version": 1,
        "machine_id": definition["machine"]["id"],
        "definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
        "coverage": copy.deepcopy(definition["coverage"]),
        "coordinate_evidence": {
            "bounds": copy.deepcopy(spatial_seed["bounds"]),
            "table_sha256": spatial_seed["table_sha256"],
            "extraction_manifest_sha256": spatial_seed["extraction_manifest_sha256"],
            "spatial_seed_sha256": hashlib.sha256(canonical_bytes(spatial_seed)).hexdigest(),
            "transformation": spatial_seed["transformation"],
            "object_count": len(spatial_seed["objects"]),
            "extraction_inventory": copy.deepcopy(spatial_seed["extraction_inventory"]),
        },
        "evidence_artifacts": copy.deepcopy(spatial_seed["evidence_artifacts"]),
        "source_hashes": _source_hashes(definition),
        "located_counts": located_counts,
        "unplaced_physical_used_playfield_devices": sorted(unplaced, key=lambda item: item["id"]),
        "controlled_not_applicable_records": sorted(controlled_na, key=lambda item: item["id"]),
        "projection_disclosures": list(spatial_seed["projection_disclosures"]),
        "unresolved": list(spatial_seed["unresolved"]),
        "promotion_decision": "Remain partial: controlled-lamp lens projections and the factory GI socket inventory are not validated physical emitter geometry.",
    }
    machine = definition["machine"]
    lines = [
        f"# {machine['name']} ({machine['manufacturer']} {machine['year']}) spatial blockers",
        "",
        f"Coverage: **{definition['coverage']['status']}**; missing {', '.join(f'`{item}`' for item in definition['coverage']['missing'])}.",
        "",
        f"Located physical used playfield devices: {located_counts['physical_used_playfield_devices']} devices in {located_counts['physical_used_playfield_placements']} placements ({located_counts['inputs']} inputs, {located_counts['outputs']} outputs).",
        f"Controlled not-applicable records: {len(controlled_na)}.",
        "",
        "## Coordinate evidence",
        "",
        f"Bounds: left={spatial_seed['bounds']['left']}, top={spatial_seed['bounds']['top']}, right={spatial_seed['bounds']['right']}, bottom={spatial_seed['bounds']['bottom']}.",
        f"Table SHA-256: `{spatial_seed['table_sha256']}`.",
        f"Extraction manifest SHA-256: `{spatial_seed['extraction_manifest_sha256']}`.",
        f"Spatial seed SHA-256: `{report['coordinate_evidence']['spatial_seed_sha256']}`.",
        f"Transformation: {spatial_seed['transformation']}",
        f"Retained extraction: {spatial_seed['extraction_inventory']['file_count']} files, {spatial_seed['extraction_inventory']['total_bytes']} bytes; {spatial_seed['extraction_inventory']['raw_gameitem_count']} raw game items. Unsupported and out-of-range object dispositions are retained in the JSON audit.",
        report["promotion_decision"],
        "",
        "## Unplaced physical used playfield devices",
        "",
    ]
    lines.extend(f"- `{item['id']}` ({item['collection']}, binding {item['binding']})." for item in report["unplaced_physical_used_playfield_devices"])
    if not report["unplaced_physical_used_playfield_devices"]:
        lines.append("- None.")
    lines += ["", "## Controlled not-applicable records", ""]
    lines.extend(f"- `{item['id']}`: `{item['reason']}` (sources: {', '.join(f'`{ref}`' for ref in item['source_refs'])})." for item in report["controlled_not_applicable_records"])
    if not report["controlled_not_applicable_records"]:
        lines.append("- None.")
    lines += ["", "## Projection disclosures", ""]
    lines.extend(f"- {item}" for item in report["projection_disclosures"])
    if not report["projection_disclosures"]:
        lines.append("- None declared.")
    lines += ["", "## Explicit unresolved blockers", ""]
    lines.extend(f"- {item}" for item in report["unresolved"])
    lines.append("")
    return report, "\n".join(lines)


def build_artifacts() -> tuple[bytes, bytes, bytes, bytes]:
    definition = build_definition()
    report, report_markdown = build_report(definition)
    return canonical_bytes(definition), build_knowledge(), canonical_bytes(report), report_markdown.encode("utf-8")


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def _refuse_author_ready(paths: tuple[Path, ...]) -> None:
    if AUTHOR_READY_PATH.exists():
        raise CuratorError(f"stale author-ready artifact: {AUTHOR_READY_PATH}")
    resolved_author_ready = AUTHOR_READY_PATH.resolve()
    if any(path.resolve() == resolved_author_ready for path in paths):
        raise CuratorError(f"refusing to write author-ready artifact: {AUTHOR_READY_PATH}")
    for path in paths:
        if path.is_file() and path.suffix == ".json":
            try:
                existing = load_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(existing, dict) and existing.get("format") == "pinmame-machine-definition" and existing.get("coverage", {}).get("status") == "author_ready":
                raise CuratorError(f"refusing to overwrite author-ready artifact: {path}")


def write_artifacts(outputs: tuple[tuple[Path, bytes], ...]) -> None:
    _refuse_author_ready(tuple(path for path, _ in outputs))
    for path, content in outputs:
        write_bytes(path, content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definition", type=Path, default=DEFINITION_PATH, help="definition target override for tests")
    parser.add_argument("--knowledge", type=Path, default=KNOWLEDGE_PATH, help="knowledge target override for tests")
    parser.add_argument("--report-json", type=Path, default=REPORT_JSON_PATH, help="spatial JSON target override for tests")
    parser.add_argument("--report-md", type=Path, default=REPORT_MD_PATH, help="spatial Markdown target override for tests")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail on any drift and never write")
    mode.add_argument("--regenerate", action="store_true", help="write only the four requested targets")
    args = parser.parse_args()
    try:
        definition, knowledge, report_json, report_md = build_artifacts()
        outputs = ((args.definition, definition), (args.knowledge, knowledge), (args.report_json, report_json), (args.report_md, report_md))
        _refuse_author_ready(tuple(path for path, _ in outputs))
        if args.check:
            drifted = False
            for path, wanted in outputs:
                if not path.is_file() or path.read_bytes() != wanted:
                    print(f"canonical content mismatch: {_display(path)}", file=sys.stderr)
                    drifted = True
            if drifted:
                return 1
            print("Viking definition, knowledge note and spatial blockers match the deterministic curator.")
            return 0
        write_artifacts(outputs)
        for path, _ in outputs:
            print(f"wrote {_display(path)}")
        return 0
    except (CuratorError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
