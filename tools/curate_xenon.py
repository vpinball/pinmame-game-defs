#!/usr/bin/env python3
"""Reproduce Xenon's artifacts from a separately curated, pinned seed."""
from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine
from tools import build_external_evidence_manifest as manifest

MACHINE_ID = "bally.xenon.1980"
SEED_PATH = Path("tools/seeds/bally/xenon-1980.json")
KNOWLEDGE_PATH = Path("knowledge/bally/xenon-1980.md")
REPORT_PATH = Path("reports/spatial/bally/xenon-1980.json")
MARKDOWN_PATH = REPORT_PATH.with_suffix(".md")
ROOT_ENV = {
	"manuals": "PINMAME_MANUALS_ROOT",
	"vpx-sources": "PINMAME_VPX_SOURCES_ROOT",
	"review-artifacts": "PINMAME_REVIEW_ARTIFACTS_ROOT",
}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def load_seed(root: Path | None = None) -> dict[str, Any]:
	path = (root or ROOT) / SEED_PATH
	if not path.is_file():
		raise ValueError(f"missing seed: {path}")
	seed = load_json(path)
	if not isinstance(seed, dict):
		raise ValueError("seed must be an object")
	return seed


def build_definition(seed: dict[str, Any] | None = None) -> dict[str, Any]:
	return copy.deepcopy((load_seed() if seed is None else seed)["definition"])


def build_knowledge(seed: dict[str, Any] | None = None) -> str:
	return (load_seed() if seed is None else seed)["knowledge_note"]


def build_spatial_report(seed: dict[str, Any] | None = None) -> dict[str, Any]:
	return copy.deepcopy((load_seed() if seed is None else seed)["spatial_report"])


def _safe_path(root: Path, relative: Any) -> Path:
	if not isinstance(relative, str) or not relative or "\\" in relative:
		raise ValueError(f"invalid relative POSIX path: {relative!r}")
	p = PurePosixPath(relative)
	if p.is_absolute() or p.as_posix() != relative or any(part in {".", ".."} or ":" in part for part in p.parts):
		raise ValueError(f"invalid relative POSIX path: {relative!r}")
	base = root.resolve()
	path = (base / relative).resolve()
	if not path.is_relative_to(base):
		raise ValueError(f"path escapes root: {relative}")
	return path


def _source_refs(value: Any, source_ids: set[str]) -> None:
	if isinstance(value, dict):
		for key, item in value.items():
			if key == "source_ref" and (not isinstance(item, str) or item not in source_ids):
				raise ValueError(f"unknown source reference: {item!r}")
			if key == "source_refs" and (not isinstance(item, list) or any(not isinstance(ref, str) or ref not in source_ids for ref in item)):
				raise ValueError(f"unknown source references: {item!r}")
			_source_refs(item, source_ids)
	elif isinstance(value, list):
		for item in value:
			_source_refs(item, source_ids)


def validate_seed(seed: dict[str, Any], root: Path) -> None:
	required = {"definition", "knowledge_note", "spatial_report", "spatial_markdown", "external_files", "extraction"}
	if not isinstance(seed, dict) or not required <= seed.keys():
		raise ValueError(f"missing seed keys: {sorted(required - seed.keys()) if isinstance(seed, dict) else sorted(required)}")
	definition, report = seed["definition"], seed["spatial_report"]
	for name in ("knowledge_note", "spatial_markdown"):
		if not isinstance(seed[name], str) or not seed[name].strip():
			raise ValueError(f"{name} must be a nonempty string")
	for label, value, schema in (("definition", definition, "machine.schema.json"), ("report", report, "spatial-report.schema.json")):
		errors = validate_against_schema(value, ROOT / "schemas" / schema, label)
		if errors:
			raise ValueError("\n".join(errors))
	machine = definition["machine"]
	if (machine.get("id"), machine.get("name"), machine.get("manufacturer"), machine.get("year")) != (MACHINE_ID, "Xenon", "Bally", 1980) or report["machine_id"] != MACHINE_ID:
		raise ValueError("wrong machine identity")
	if definition.get("knowledge", {}).get("path") != KNOWLEDGE_PATH.as_posix():
		raise ValueError("wrong knowledge path")
	# The note is itself an output and may not exist before regeneration.
	errors = validate_machine(definition)
	if errors:
		raise ValueError("\n".join(errors))
	for source in definition["sources"]:
		uri = source["uri"]
		local = uri.removeprefix("internal:") if uri.startswith("internal:") else uri if uri.startswith("evidence/") else None
		if local is not None:
			path = _safe_path(root, local)
			if not path.is_file() or file_sha256(path) != source.get("sha256"):
				raise ValueError(f"missing or drifted repository source: {path}")
		for excerpt in source.get("excerpts", []):
			for field, digest_field in (("path", "sha256"), ("image", "image_sha256")):
				if field in excerpt:
					path = _safe_path(root, excerpt[field])
					if not path.is_file() or file_sha256(path) != excerpt.get(digest_field):
						raise ValueError(f"missing or drifted excerpt: {path}")
	status = definition["coverage"]["status"]
	if (report["format"] == "pinmame-spatial-audit") != (status == "author_ready"):
		raise ValueError("spatial report format contradicts coverage status")
	ids = {source["id"] for source in definition["sources"]}
	_source_refs(definition, ids)
	_source_refs(report, ids)
	files = seed["external_files"]
	if not isinstance(files, list) or not files:
		raise ValueError("external_files must contain pinned assertions")
	assertions = {}
	for item in files:
		if not isinstance(item, dict) or set(item) != {"root", "path", "sha256"} or not isinstance(item["root"], str) or item["root"] not in ROOT_ENV or not isinstance(item["sha256"], str) or not SHA256.fullmatch(item["sha256"]):
			raise ValueError(f"invalid external file assertion: {item!r}")
		_safe_path(root, item["path"])
		key = (item["root"], item["path"])
		if key in assertions:
			raise ValueError(f"duplicate external file assertion: {key}")
		assertions[key] = item["sha256"]
	ext = seed["extraction"]
	if not isinstance(ext, dict) or set(ext) != {"root", "path", "game", "manifest_sha256", "file_count", "total_bytes"}:
		raise ValueError("invalid extraction assertion")
	if ext["root"] != "vpx-sources" or ext["path"] != "bally/xenon-1980/extracted-v2.5.2" or ext["game"] != "xenon" or not isinstance(ext["manifest_sha256"], str) or not SHA256.fullmatch(ext["manifest_sha256"]) or any(type(ext[k]) is not int or ext[k] < 0 for k in ("file_count", "total_bytes")):
		raise ValueError("invalid extraction identity or digest")
	if (ext["root"], ext["path"]) in assertions:
		raise ValueError("extraction directory cannot also be an external file")
	assertions[(ext["root"], ext["path"])] = ext["manifest_sha256"]
	for secondary in seed.get("secondary_extractions", []):
		if not isinstance(secondary, dict) or set(secondary) != set(ext):
			raise ValueError("invalid secondary extraction assertion")
		if secondary["root"] != "vpx-sources" or secondary["path"] != "bally/xenon-1980/extracted-v600" or secondary["game"] != "xenon" or not SHA256.fullmatch(str(secondary["manifest_sha256"])) or any(type(secondary[k]) is not int or secondary[k] < 0 for k in ("file_count", "total_bytes")):
			raise ValueError("invalid secondary extraction identity")
		_safe_path(root, secondary["path"])
	for source in definition["sources"]:
		uri = source["uri"]
		if uri.startswith("external:"):
			prefix, sep, path = uri.removeprefix("external:").partition("/")
			label = prefix.removeprefix("pinmame-") if prefix.startswith("pinmame-") else ""
			if not sep or label not in ROOT_ENV or (label, path) not in assertions or assertions[(label, path)] != source.get("sha256"):
				raise ValueError(f"missing or inconsistent external source assertion: {uri}")


def verify_bally_excerpt(source: Path, excerpt: Path) -> None:
	"""Check literal code against the retained library, not only its excerpt digest."""
	lines = source.read_text(encoding="utf-8").splitlines()
	blocks = re.findall(r"Lines (\d+)-(\d+):[^\n]*\n\n```vb\n(.*?)\n```", excerpt.read_text(encoding="utf-8"), re.S)
	if [(int(start), int(end)) for start, end, _ in blocks] != [(20, 47), (72, 139)]:
		raise ValueError("Bally excerpt must declare the constants and both complete keyboard-handler ranges")
	for start, end, code in blocks:
		if code != "\n".join(lines[int(start) - 1:int(end)]):
			raise ValueError(f"Bally excerpt is not source-literal at lines {start}-{end}")


def verify_evidence(seed: dict[str, Any], *, required: bool = False, root: Path | None = None) -> None:
	items = seed["external_files"]
	needed = {item["root"] for item in items} | {seed["extraction"]["root"]}
	roots = {}
	for label in needed:
		value = os.environ.get(ROOT_ENV[label])
		if not value:
			if required:
				raise ValueError(f"{ROOT_ENV[label]} is required")
			continue
		evidence_root = Path(value).expanduser().resolve()
		if not evidence_root.is_dir():
			raise ValueError(f"configured evidence root is missing: {evidence_root}")
		roots[label] = evidence_root
	for item in items:
		if item["root"] in roots:
			path = _safe_path(roots[item["root"]], item["path"])
			if not path.is_file() or file_sha256(path) != item["sha256"]:
				raise ValueError(f"missing or drifted external file: {path}")
	bally_hashes = {item["sha256"] for item in items if item["root"] == "vpx-sources" and PurePosixPath(item["path"]).name.casefold() == "bally.vbs"}
	bally_claims = []
	for source in seed["definition"]["sources"]:
		claims = [e for e in source.get("excerpts", []) if e["id"] == "bally-library" or e["path"] == "evidence/excerpts/bally.xenon.1980/bally-library.md"]
		retained_bally = source.get("sha256") in bally_hashes or PurePosixPath(source["uri"]).name.casefold() == "bally.vbs"
		if retained_bally or claims:
			bally_claims.append((source, claims))
	if bally_claims:
		if len(bally_claims) != 1 or len(bally_claims[0][1]) != 1:
			raise ValueError("Bally literal claim must identify one retained source and one excerpt")
		source, (excerpt,) = bally_claims[0]
		prefix = "external:pinmame-vpx-sources/"
		if not source["uri"].startswith(prefix):
			raise ValueError("Bally literal claim requires a supported external source URI")
		if "vpx-sources" in roots:
			verify_bally_excerpt(_safe_path(roots["vpx-sources"], source["uri"].removeprefix(prefix)), _safe_path(root or ROOT, excerpt["path"]))
	for ext in [seed["extraction"], *seed.get("secondary_extractions", [])]:
		if ext["root"] in roots:
			path = _safe_path(roots[ext["root"]], ext["path"])
			actual = manifest.build_manifest(path, ext["game"])
			digest = hashlib.sha256(manifest.canonical_bytes(actual) + b"\n").hexdigest()
			if (digest, len(actual["files"]), sum(f["size"] for f in actual["files"])) != (ext["manifest_sha256"], ext["file_count"], ext["total_bytes"]):
				raise ValueError(f"extraction identity mismatch: {path}")
			if manifest.check_manifest(path, ext["game"]) != digest:
				raise ValueError(f"extraction manifest mismatch: {path}")


def artifacts(seed: dict[str, Any], root: Path) -> dict[Path, bytes]:
	status = seed["definition"]["coverage"]["status"]
	directory = {"author_ready": "author-ready", "partial": "partial", "stub": "stubs"}[status]
	return {
		root / "machines" / directory / "bally/xenon-1980.json": canonical_bytes(build_definition(seed)),
		root / KNOWLEDGE_PATH: build_knowledge(seed).encode("utf-8"),
		root / REPORT_PATH: canonical_bytes(build_spatial_report(seed)),
		root / MARKDOWN_PATH: seed["spatial_markdown"].encode("utf-8"),
	}


def run(root: Path, mode: str, seed: dict[str, Any] | None = None) -> None:
	seed = load_seed(root) if seed is None else seed
	validate_seed(seed, root)
	verify_evidence(seed, required=mode == "verify-evidence", root=root)
	if mode == "verify-evidence":
		return
	expected = artifacts(seed, root)
	author_ready = root / "machines/author-ready/bally/xenon-1980.json"
	if author_ready.exists() and (author_ready not in expected or author_ready.read_bytes() != expected[author_ready]):
		raise ValueError(f"refusing to overwrite or demote author-ready artifact: {author_ready}")
	other_paths = [root / "machines" / folder / "bally/xenon-1980.json" for folder in ("author-ready", "partial", "stubs")]
	stale = [path for path in other_paths if path not in expected and path.exists()]
	if mode == "check":
		if stale:
			raise ValueError(f"stale machine artifact: {stale[0]}")
		for path, contents in expected.items():
			if not path.is_file() or path.read_bytes() != contents:
				raise ValueError(f"missing or drifted artifact: {path}")
	elif mode == "regenerate":
		for path, contents in expected.items():
			write_bytes(path, contents)
		for path in stale:
			path.unlink()
	else:
		raise ValueError(f"unknown mode: {mode}")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	modes = parser.add_mutually_exclusive_group(required=True)
	modes.add_argument("--check", action="store_true")
	modes.add_argument("--regenerate", action="store_true")
	modes.add_argument("--verify-evidence", action="store_true")
	args = parser.parse_args()
	mode = "check" if args.check else "regenerate" if args.regenerate else "verify-evidence"
	try:
		run(ROOT, mode)
	except (ValueError, OSError) as exc:
		print(f"Xenon curator: {exc}", file=sys.stderr)
		return 1
	print(f"Xenon curator {mode} succeeded")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
