from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


MANIFEST_FILENAME = "manifest.json"
MANIFEST_DIGEST_FILENAME = "manifest.sha256"
FORMAT = "pinmame-external-evidence-manifest"
VERSION = 1


def sha256_file(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def build_manifest(directory: Path, game: str) -> dict[str, object]:
	directory = directory.resolve()
	if not directory.is_dir():
		raise ValueError(f"evidence directory does not exist: {directory}")

	excluded = {MANIFEST_FILENAME, MANIFEST_DIGEST_FILENAME}
	files = []
	paths = ((path.relative_to(directory).as_posix(), path) for path in directory.rglob("*") if path.is_file())
	for relative, path in sorted(paths, key=lambda item: item[0]):
		if relative in excluded:
			continue
		files.append({"path": relative, "sha256": sha256_file(path), "size": path.stat().st_size})

	return {"files": files, "format": FORMAT, "game": game, "version": VERSION}


def canonical_bytes(manifest: dict[str, object]) -> bytes:
	return json.dumps(
		manifest,
		ensure_ascii=False,
		separators=(",", ":"),
		sort_keys=True,
	).encode("utf-8")


def write_manifest(directory: Path, game: str) -> str:
	manifest = build_manifest(directory, game)
	payload = canonical_bytes(manifest) + b"\n"
	digest = hashlib.sha256(payload).hexdigest()
	(directory / MANIFEST_FILENAME).write_bytes(payload)
	(directory / MANIFEST_DIGEST_FILENAME).write_text(digest + "\n", encoding="ascii", newline="\n")
	return digest


def check_manifest(directory: Path, game: str) -> str:
	manifest_path = directory / MANIFEST_FILENAME
	digest_path = directory / MANIFEST_DIGEST_FILENAME
	if not manifest_path.is_file() or not digest_path.is_file():
		raise ValueError(f"manifest files are missing under: {directory}")
	expected = canonical_bytes(build_manifest(directory, game)) + b"\n"
	actual = manifest_path.read_bytes()
	if actual != expected:
		raise ValueError(f"manifest content is stale: {manifest_path}")
	digest = hashlib.sha256(expected).hexdigest()
	if digest_path.read_text(encoding="ascii") != digest + "\n":
		raise ValueError(f"manifest digest is stale: {digest_path}")
	return digest


def main() -> int:
	parser = argparse.ArgumentParser(description="Build a canonical manifest for an external evidence directory")
	parser.add_argument("directory", type=Path)
	parser.add_argument("--game", required=True, help="PinMAME driver id recorded in the manifest")
	parser.add_argument("--check", action="store_true", help="verify the retained manifest without writing files")
	args = parser.parse_args()
	print(check_manifest(args.directory, args.game) if args.check else write_manifest(args.directory, args.game))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
