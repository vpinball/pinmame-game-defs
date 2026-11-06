"""Materialize the reviewed F-14 Tomcat seed and its spatial blocker report.

The seed owns source-authority decisions. This tool never infers a socket from
a render light, upgrades assertion state, or makes an author-ready promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from build_external_evidence_manifest import check_manifest
from pinmame_flipper_column import FLIPPER_COLUMN_ADDRESSES
from pinmame_game_defs.jsonio import canonical_bytes
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.f-14-tomcat.1987"
SLUG = "f-14-tomcat-1987"
SEED = Path(f"tools/seeds/williams/{SLUG}.json")
KNOWLEDGE_SEED = Path(f"tools/seeds/williams/{SLUG}.md")
EVIDENCE = Path(f"tools/seeds/williams/{SLUG}-evidence.json")
DEFINITION = Path(f"machines/partial/williams/{SLUG}.json")
AUTHOR_READY = Path(f"machines/author-ready/williams/{SLUG}.json")
KNOWLEDGE = Path(f"knowledge/williams/{SLUG}.md")
REPORT = Path(f"reports/spatial/williams/{SLUG}.json")
REPORT_MD = Path(f"reports/spatial/williams/{SLUG}.md")
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DRIVERS = {"f14_l1", "f14_p3", "f14_p4", "f14_p5"}
SWITCHES = set(range(-7, -3)) | set(range(1, 65)) | set(FLIPPER_COLUMN_ADDRESSES)


def _json(path: Path) -> dict[str, Any]:
	try:
		raw = path.read_bytes()
		value = json.loads(raw)
	except (OSError, ValueError) as error:
		raise RuntimeError(f"Missing or malformed F-14 input: {path}") from error
	if not isinstance(value, dict) or raw != canonical_bytes(value):
		raise RuntimeError(f"F-14 input must be canonical JSON: {path}")
	return value


def _safe(root: Path, relative: str) -> Path:
	path = PurePosixPath(relative)
	if (not relative or "\\" in relative or path.is_absolute() or PureWindowsPath(relative).drive
		or any(part in {"", ".", ".."} or ":" in part for part in relative.split("/"))):
		raise RuntimeError(f"Unsafe F-14 evidence path: {relative!r}")
	result = root.joinpath(*path.parts)
	if not result.resolve().is_relative_to(root.resolve()):
		raise RuntimeError(f"F-14 evidence path escapes root: {relative}")
	return result


def _digest(path: Path, sha256: str, size: int | None = None) -> None:
	try:
		data = path.read_bytes()
	except OSError as error:
		raise RuntimeError(f"Missing F-14 evidence: {path}") from error
	if (size is not None and len(data) != size) or hashlib.sha256(data).hexdigest() != sha256:
		raise RuntimeError(f"F-14 evidence hash or size drift: {path}")


def build(root: Path = ROOT) -> dict[str, Any]:
	definition = _json(root / SEED)
	errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", "F-14 seed")
	errors.extend(validate_machine(definition))
	if errors:
		raise RuntimeError("Invalid F-14 seed:\n" + "\n".join(errors))
	if definition["machine"]["id"] != MACHINE_ID or definition["coverage"]["status"] != "partial":
		raise RuntimeError("F-14 materializer requires this game's reviewed partial seed")
	if {d["id"] for d in definition["drivers"]} != DRIVERS:
		raise RuntimeError("F-14 driver set drift")
	if definition["controller"]["platform"] != "pinmame.system-11":
		raise RuntimeError("F-14 controller platform drift")
	bindings = lambda collection, group: [d["binding"]["device"] for d in definition[collection] if d["binding"]["group"] == group]
	for collection, group, expected in (
		("inputs", "pinmame.input.switch", SWITCHES),
		("inputs", "pinmame.input.dip", {0}),
		("outputs", "pinmame.output.solenoid", set(range(1, 65))),
		("outputs", "pinmame.output.lamp", set(range(1, 65))),
	):
		actual = bindings(collection, group)
		if len(actual) != len(expected) or set(actual) != expected:
			raise RuntimeError(f"F-14 incomplete/duplicate {group} enumeration")
	if any(d["binding"]["group"] == "pinmame.output.gi" for d in definition["outputs"]):
		raise RuntimeError("F-14 has no independent GI callback group")
	for source in definition["sources"]:
		if source["uri"].startswith("evidence/"):
			_digest(_safe(root, source["uri"]), source["sha256"])
		for excerpt in source.get("excerpts", []):
			if not excerpt["path"].startswith(f"evidence/excerpts/{MACHINE_ID}/"):
				raise RuntimeError("F-14 excerpt belongs to another machine")
			_digest(_safe(root, excerpt["path"]), excerpt["sha256"])
			if "image" in excerpt:
				_digest(_safe(root, excerpt["image"]), excerpt["image_sha256"])
	_json(root / EVIDENCE)
	if not (root / KNOWLEDGE_SEED).is_file():
		raise RuntimeError("Missing F-14 knowledge seed")
	return definition


def verify_retained(vpx_root: Path, manuals_root: Path, review_root: Path, *, root: Path = ROOT) -> None:
	register = _json(root / EVIDENCE)
	roots = {"vpx": Path(vpx_root), "manuals": Path(manuals_root), "review": Path(review_root)}
	for entry in register["files"]:
		_digest(_safe(roots[entry["root"]], entry["path"]), entry["sha256"], entry["size"])
	# All retained bundles use the production-ROM label f14_l1, including the harness.
	# This manifest grouping label does not assert prototype hardware compatibility.
	for extraction in register["extractions"]:
		manifest = _safe(roots[extraction.get("root", "vpx")], extraction["path"])
		_digest(manifest, extraction["sha256"])
		if check_manifest(manifest.parent, "f14_l1") != extraction["sha256"]:
			raise RuntimeError("F-14 extraction manifest drift")
		files = json.loads(manifest.read_bytes())["files"]
		if len(files) != extraction["file_count"] or sum(f["size"] for f in files) != extraction["total_bytes"]:
			raise RuntimeError("F-14 extraction count/byte drift")


def spatial_report(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	devices = []
	for collection in ("inputs", "outputs", "displays"):
		for device in definition[collection]:
			devices.append({"collection": collection, **device})
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"coordinate_convention": "playfield: x0 left, x1 right, y0 rear, y1 front; at most six decimals",
		"transformation": "x = (VPW 2025 x - 0) / 952; y = (VPW 2025 y - 0) / 1974; round once to six decimals. Earlier 964x2162 extractions are not coordinate sources.",
		"evidence": _json(root / EVIDENCE), "sources": definition["sources"],
		"located": [d for d in devices if d.get("spatial", {}).get("placements")],
		"not_applicable": [d for d in devices if d.get("spatial", {}).get("status") == "not_applicable"],
		"missing_spatial": [d for d in devices if "spatial" not in d],
		"coverage": definition["coverage"],
		"promotion_decision": "Partial. Retained geometry does not establish every physical lamp/GI/flasher socket or prototype/production fitment; see knowledge and coverage.missing.",
		"projection_policy": "A mechanism anchor projects the named physical assembly onto the playfield plane. No render helper, insert overlay, primitive origin or script-only ball-stack sensor is presented as a socket/contact/winding.",
	}


def report_markdown(report: dict[str, Any]) -> str:
	lines = ["# F-14 Tomcat spatial blockers", "", report["promotion_decision"], "",
		f"Definition SHA-256: `{report['definition_sha256']}`", "", report["coordinate_convention"], "",
		report["transformation"], "", report["projection_policy"], "", "## Exact retained artifacts", ""]
	for entry in report["evidence"]["files"]:
		lines.append(f"- `{entry['root']}:{entry['path']}`: {entry['size']} bytes, SHA-256 `{entry['sha256']}`.")
	for entry in report["evidence"]["extractions"]:
		lines.append(f"- `{entry['path']}`: {entry['file_count']} files, {entry['total_bytes']} bytes; manifest SHA-256 `{entry['sha256']}`.")
	lines += ["", "## Located devices and disclosed projections", ""]
	for device in report["located"]:
		for place in device["spatial"]["placements"]:
			lines.append(f"- `{device['id']}` / `{place['id']}`: ({place['x']}, {place['y']}), {place['role']}; {device.get('physical', {}).get('notes', '')}")
	lines += ["", "## Unplaced records", ""]
	for device in report["missing_spatial"]:
		lines.append(f"- `{device['id']}`: {device['label']}; {device.get('physical', {}).get('notes', '')}")
	lines += ["", "## Controlled not-applicable records", ""]
	for device in report["not_applicable"]:
		lines.append(f"- `{device['id']}`: `{device['spatial']['reason']}`.")
	return "\n".join(lines) + "\n"


def run(*, check: bool = False, root: Path = ROOT) -> dict[str, Any]:
	definition = build(root)
	if (root / AUTHOR_READY).exists():
		raise RuntimeError("Refusing to overwrite or coexist with an author-ready F-14 artifact")
	report = spatial_report(definition, root)
	artifacts = {DEFINITION: canonical_bytes(definition), KNOWLEDGE: (root / KNOWLEDGE_SEED).read_bytes(),
		REPORT: canonical_bytes(report), REPORT_MD: report_markdown(report).encode("utf-8")}
	for path, data in artifacts.items():
		if check:
			if not (root / path).is_file() or (root / path).read_bytes() != data:
				raise RuntimeError(f"F-14 generated artifact drift: {path}")
		else:
			(root / path).parent.mkdir(parents=True, exist_ok=True)
			(root / path).write_bytes(data)
	return definition


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	parser.add_argument("--verify-retained", action="store_true")
	args = parser.parse_args()
	if args.verify_retained:
		variables = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
		if any(not os.environ.get(key) for key in variables):
			raise RuntimeError("--verify-retained requires all three evidence roots")
		verify_retained(*(Path(os.environ[key]) for key in variables))
	run(check=args.check)
	print(f"{MACHINE_ID}: {'checked' if args.check else 'regenerated'} (partial)")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
