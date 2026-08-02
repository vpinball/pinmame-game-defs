from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO

from .errors import DefinitionError
from .jsonio import file_sha256, load_json, write_json


def _stream_sha256(stream: BinaryIO) -> str:
	digest = hashlib.sha256()
	for block in iter(lambda: stream.read(1024 * 1024), b""):
		digest.update(block)
	return digest.hexdigest()


def _cached_archive(existing: dict[str, Any] | None, path: Path, content_hashes: bool) -> dict[str, Any] | None:
	if existing is None:
		return None
	stat = path.stat()
	if existing.get("bytes") != stat.st_size or existing.get("mtime_ns") != stat.st_mtime_ns:
		return None
	if not content_hashes:
		return existing
	for member in existing.get("members", []):
		if member.get("directory"):
			continue
		if "sha256" not in member and "hash_error" not in member:
			return None
	return existing


def _member_record(archive: zipfile.ZipFile, info: zipfile.ZipInfo, content_hashes: bool) -> dict[str, Any]:
	record: dict[str, Any] = {
		"filename": info.filename,
		"bytes": info.file_size,
		"compressed_bytes": info.compress_size,
		"crc32": f"{info.CRC:08x}",
		"compression": info.compress_type,
		"encrypted": bool(info.flag_bits & 0x1),
		"directory": info.is_dir(),
	}
	if content_hashes and not info.is_dir():
		try:
			with archive.open(info, "r") as stream:
				record["sha256"] = _stream_sha256(stream)
		except (RuntimeError, OSError, zipfile.BadZipFile) as error:
			record["hash_error"] = f"{type(error).__name__}: {error}"
	return record


def _archive_record(path: Path, root: Path, driver_ids: set[str], content_hashes: bool) -> dict[str, Any]:
	stat = path.stat()
	driver_id = path.stem.casefold()
	record: dict[str, Any] = {
		"relative_path": PurePosixPath(path.relative_to(root)).as_posix(),
		"bytes": stat.st_size,
		"mtime_ns": stat.st_mtime_ns,
		"sha256": file_sha256(path),
		"driver_id": driver_id if driver_id in driver_ids else None,
		"status": "valid_zip",
		"members": [],
	}
	try:
		with zipfile.ZipFile(path, "r") as archive:
			record["members"] = [_member_record(archive, info, content_hashes) for info in archive.infolist()]
	except (OSError, zipfile.BadZipFile) as error:
		record["status"] = "invalid_zip"
		record["error"] = f"{type(error).__name__}: {error}"
	return record


def index_rom_corpus(rom_root: Path, catalog_path: Path, output_path: Path, content_hashes: bool = False) -> dict[str, Any]:
	rom_root = rom_root.resolve()
	if not rom_root.is_dir():
		raise DefinitionError(f"ROM root is not a directory: {rom_root}")
	if not catalog_path.is_file():
		raise DefinitionError(f"PinMAME catalog not found: {catalog_path}")
	catalog = load_json(catalog_path)
	driver_ids = {str(driver["id"]).casefold() for driver in catalog.get("drivers", [])}
	if not driver_ids:
		raise DefinitionError(f"PinMAME catalog contains no drivers: {catalog_path}")
	existing_by_path: dict[str, dict[str, Any]] = {}
	if output_path.is_file():
		try:
			existing = load_json(output_path)
			existing_by_path = {str(record["relative_path"]): record for record in existing.get("archives", [])}
		except (OSError, ValueError, KeyError, TypeError):
			existing_by_path = {}
	archives = []
	for path in sorted(rom_root.rglob("*.zip"), key=lambda candidate: PurePosixPath(candidate.relative_to(rom_root)).as_posix().casefold()):
		relative_path = PurePosixPath(path.relative_to(rom_root)).as_posix()
		record = _cached_archive(existing_by_path.get(relative_path), path, content_hashes)
		archives.append(record if record is not None else _archive_record(path, rom_root, driver_ids, content_hashes))
	matched_driver_ids = {record["driver_id"] for record in archives if record.get("driver_id")}
	invalid_count = sum(record["status"] != "valid_zip" for record in archives)
	index = {
		"format": "pinmame-rom-corpus-index",
		"version": 1,
		"catalog_revision": catalog["source"]["pinmame_revision"],
		"content_hashes": content_hashes,
		"summary": {
			"archive_count": len(archives),
			"valid_archive_count": len(archives) - invalid_count,
			"invalid_archive_count": invalid_count,
			"catalog_driver_count": len(driver_ids),
			"matched_driver_count": len(matched_driver_ids),
			"missing_driver_count": len(driver_ids - matched_driver_ids),
			"unmatched_archive_count": sum(record.get("driver_id") is None for record in archives),
		},
		"missing_driver_ids": sorted(driver_ids - matched_driver_ids),
		"archives": archives,
	}
	write_json(output_path, index)
	return index
