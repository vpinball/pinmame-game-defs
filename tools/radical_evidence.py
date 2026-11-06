"""Immutable local and optional external evidence gates for Radical only."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath

import build_external_evidence_manifest as manifests

ROOT = Path(__file__).resolve().parents[1]
REGISTER = Path("tools/seeds/bally/radical-1990-evidence.json")
ROOT_ENV = {
	"vpx-sources": "PINMAME_VPX_SOURCES_ROOT",
	"manuals": "PINMAME_MANUALS_ROOT",
	"review-artifacts": "PINMAME_REVIEW_ARTIFACTS_ROOT",
}


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def register(root: Path = ROOT) -> dict:
	return json.loads((root / REGISTER).read_text(encoding="utf-8"))


def safe_path(root: Path, relative: str) -> Path:
	p = PurePosixPath(relative)
	if p.is_absolute() or "\\" in relative or ":" in relative or any(part in ("", ".", "..") for part in relative.split("/")):
		raise RuntimeError(f"Unsafe Radical evidence path: {relative}")
	path = root.joinpath(*p.parts)
	try:
		path.resolve().relative_to(root.resolve())
	except ValueError as error:
		raise RuntimeError(f"Radical evidence escaped its root: {relative}") from error
	return path


def extra_sources(root: Path = ROOT) -> list[dict]:
	data = register(root)
	for source in data["sources"]:
		for excerpt in source.get("excerpts", []):
			path = safe_path(root, excerpt["path"])
			if not path.is_file() or sha256(path) != excerpt["sha256"]:
				raise RuntimeError(f"Radical source excerpt missing or changed: {path}")
	return data["sources"]


def verify_external_evidence(root: Path = ROOT) -> None:
	"""Unset roots skip their external checks; a configured incomplete root fails."""
	data = register(root)
	roots = {name: Path(value) for name, env in ROOT_ENV.items() if (value := os.environ.get(env))}
	for artifact in data["files"]:
		if artifact["root"] not in roots:
			continue
		path = safe_path(roots[artifact["root"]], artifact["path"])
		if not path.is_file() or sha256(path) != artifact["sha256"]:
			raise RuntimeError(f"Radical retained evidence missing or changed: {path}")
	for extraction in data["extractions"]:
		if extraction["root"] not in roots:
			continue
		path = safe_path(roots[extraction["root"]], extraction["path"])
		try:
			digest = manifests.check_manifest(path, extraction["game"])
		except (OSError, ValueError) as error:
			raise RuntimeError(f"Radical full extraction manifest failed: {path}: {error}") from error
		if digest != extraction["manifest_sha256"]:
			raise RuntimeError(f"Radical extraction manifest identity changed: {path}")
		manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
		if len(manifest["files"]) != extraction["file_count"] or sum(entry["size"] for entry in manifest["files"]) != extraction["total_bytes"]:
			raise RuntimeError(f"Radical extraction inventory differs: {path}")
