from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
	return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def content_sha256(value: Any) -> str:
	return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def load_json(path: Path) -> Any:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def write_json(path: Path, value: Any) -> None:
	write_bytes(path, canonical_bytes(value))


def write_text(path: Path, value: str) -> None:
	write_bytes(path, value.encode("utf-8"))


def write_bytes(path: Path, value: bytes) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	if path.exists() and path.read_bytes() == value:
		return
	with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
		temporary = Path(stream.name)
		stream.write(value)
	try:
		os.replace(temporary, path)
	except BaseException:
		temporary.unlink(missing_ok=True)
		raise
