from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import urllib.parse
import urllib.request
import urllib.error
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

import pdfplumber

from .errors import DefinitionError
from .jsonio import file_sha256, load_json, write_json
from .schema_validation import validate_against_schema

ITEM_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
MACHINE_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
DIRECT_SOURCES = {"ipdb", "manufacturer", "other"}
MAX_DOCUMENT_BYTES = 250 * 1024 * 1024
USER_AGENT = "pinmame-game-defs/0.1 manual evidence collector"
EXTRACTION_FORMAT = "pinmame-manual-extraction"
EXTRACTION_VERSION = 1
SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _validate_manifest(manifest: dict[str, Any], label: str) -> None:
	errors = validate_against_schema(manifest, SCHEMA_ROOT / "manual-cache.schema.json", label)
	documents = manifest.get("documents")
	if isinstance(documents, list):
		ids = [document.get("id") for document in documents if isinstance(document, dict)]
		duplicates = sorted({document_id for document_id in ids if isinstance(document_id, str) and ids.count(document_id) > 1})
		for document_id in duplicates:
			errors.append(f"{label} $.documents[].id: duplicate document ID {document_id!r}")
	if errors:
		raise DefinitionError("Invalid manual-cache manifest:\n" + "\n".join(errors))


def _load_manifest(path: Path) -> dict[str, Any]:
	manifest = load_json(path)
	_validate_manifest(manifest, path.as_posix())
	return manifest


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
	_validate_manifest(manifest, path.as_posix())
	write_json(path, manifest)


def _write_extraction(path: Path, extraction: dict[str, Any]) -> None:
	errors = validate_against_schema(extraction, SCHEMA_ROOT / "manual-extraction.schema.json", path.as_posix())
	if errors:
		raise DefinitionError("Invalid manual extraction:\n" + "\n".join(errors))
	write_json(path, extraction)


def _request_json(url: str) -> dict[str, Any]:
	request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
	try:
		with urllib.request.urlopen(request, timeout=60) as response:
			if response.status != 200:
				raise DefinitionError(f"Metadata request failed with HTTP {response.status}: {url}")
			return json.load(response)
	except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
		raise DefinitionError(f"Unable to read metadata {url}: {error}") from error


def _select_original_pdf(metadata: dict[str, Any], requested_file: str | None) -> dict[str, Any]:
	files = metadata.get("files")
	if not isinstance(files, list):
		raise DefinitionError("Internet Archive metadata has no file inventory")
	candidates = []
	for record in files:
		name = record.get("name") if isinstance(record, dict) else None
		if not isinstance(name, str) or not name.casefold().endswith(".pdf"):
			continue
		if requested_file is not None and name != requested_file:
			continue
		if record.get("source") == "original":
			candidates.append(record)
	if requested_file is not None and len(candidates) != 1:
		raise DefinitionError(f"Requested original PDF is missing or ambiguous: {requested_file}")
	if not candidates:
		raise DefinitionError("Internet Archive item has no original PDF")
	if len(candidates) > 1:
		names = ", ".join(sorted(record["name"] for record in candidates))
		raise DefinitionError(f"Internet Archive item has multiple original PDFs; choose --file: {names}")
	return candidates[0]


def _safe_filename(value: str) -> str:
	name = PurePosixPath(value).name
	if name != value or name in {"", ".", ".."}:
		raise DefinitionError(f"Unsafe archive filename: {value!r}")
	return name


def _has_pdf_header(path: Path) -> bool:
	with path.open("rb") as stream:
		return stream.read(5) == b"%PDF-"


def _download(url: str, destination: Path, expected_size: int, expected_md5: str | None, expected_sha1: str | None) -> None:
	if expected_size < 1 or expected_size > MAX_DOCUMENT_BYTES:
		raise DefinitionError(f"Manual size {expected_size} is outside the allowed range")
	destination.parent.mkdir(parents=True, exist_ok=True)
	request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
	temporary: Path | None = None
	try:
		with urllib.request.urlopen(request, timeout=120) as response:
			if response.status != 200:
				raise DefinitionError(f"Manual download failed with HTTP {response.status}: {url}")
			with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.", delete=False) as stream:
				temporary = Path(stream.name)
				md5 = hashlib.md5()
				sha1 = hashlib.sha1()
				total = 0
				while True:
					block = response.read(1024 * 1024)
					if not block:
						break
					total += len(block)
					if total > MAX_DOCUMENT_BYTES:
						raise DefinitionError("Manual download exceeded the size limit")
					md5.update(block)
					sha1.update(block)
					stream.write(block)
		if total != expected_size:
			raise DefinitionError(f"Manual size mismatch: expected {expected_size}, received {total}")
		if expected_md5 and md5.hexdigest() != expected_md5.casefold():
			raise DefinitionError("Manual MD5 does not match Internet Archive metadata")
		if expected_sha1 and sha1.hexdigest() != expected_sha1.casefold():
			raise DefinitionError("Manual SHA-1 does not match Internet Archive metadata")
		os.replace(temporary, destination)
		temporary = None
	except (OSError, urllib.error.URLError) as error:
		raise DefinitionError(f"Unable to download manual {url}: {error}") from error
	finally:
		if temporary is not None:
			temporary.unlink(missing_ok=True)


def _https_url(value: str, label: str) -> str:
	parsed = urllib.parse.urlsplit(value)
	if parsed.scheme != "https" or not parsed.netloc or parsed.username is not None or parsed.password is not None:
		raise DefinitionError(f"{label} must be an absolute HTTPS URL without credentials: {value!r}")
	return value


class _SameHostHttpsRedirectHandler(urllib.request.HTTPRedirectHandler):
	def redirect_request(self, request: Any, file_pointer: Any, code: int, message: str, headers: Any, new_url: str) -> Any:
		old = urllib.parse.urlsplit(request.full_url)
		resolved_url = urllib.parse.urljoin(request.full_url, new_url)
		new = urllib.parse.urlsplit(resolved_url)
		if new.scheme != "https" or new.hostname != old.hostname or new.username is not None or new.password is not None:
			raise DefinitionError(f"Manual redirect must remain HTTPS on {old.hostname}: {resolved_url}")
		return super().redirect_request(request, file_pointer, code, message, headers, resolved_url)


def _download_direct_pdf(url: str, destination: Path, expected_sha256: str | None = None) -> None:
	if expected_sha256 is not None and not SHA256_PATTERN.fullmatch(expected_sha256):
		raise DefinitionError("Expected SHA-256 must be 64 lowercase hexadecimal characters")
	destination.parent.mkdir(parents=True, exist_ok=True)
	request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
	opener = urllib.request.build_opener(_SameHostHttpsRedirectHandler())
	temporary: Path | None = None
	try:
		with opener.open(request, timeout=120) as response:
			if response.status != 200:
				raise DefinitionError(f"Manual download failed with HTTP {response.status}: {url}")
			final_url = _https_url(response.geturl(), "Final download URL")
			if urllib.parse.urlsplit(final_url).hostname != urllib.parse.urlsplit(url).hostname:
				raise DefinitionError(f"Manual redirect changed host: {final_url}")
			declared_size = response.headers.get("Content-Length")
			if declared_size is not None and (int(declared_size) < 1 or int(declared_size) > MAX_DOCUMENT_BYTES):
				raise DefinitionError(f"Manual size {declared_size} is outside the allowed range")
			with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.", delete=False) as stream:
				temporary = Path(stream.name)
				total = 0
				prefix = b""
				sha256 = hashlib.sha256()
				while True:
					block = response.read(1024 * 1024)
					if not block:
						break
					if not prefix:
						prefix = block[:5]
					total += len(block)
					if total > MAX_DOCUMENT_BYTES:
						raise DefinitionError("Manual download exceeded the size limit")
					sha256.update(block)
					stream.write(block)
		if total < 1 or prefix != b"%PDF-":
			raise DefinitionError(f"Downloaded resource is not a PDF: {url}")
		if declared_size is not None and total != int(declared_size):
			raise DefinitionError(f"Manual size mismatch: expected {declared_size}, received {total}")
		if expected_sha256 is not None and sha256.hexdigest() != expected_sha256:
			raise DefinitionError("Manual SHA-256 does not match the expected digest")
		os.replace(temporary, destination)
		temporary = None
	except (OSError, urllib.error.URLError, ValueError) as error:
		raise DefinitionError(f"Unable to download manual {url}: {error}") from error
	finally:
		if temporary is not None:
			temporary.unlink(missing_ok=True)


def acquire_url_document(
	cache_root: Path,
	machine_id: str,
	source: str,
	source_id: str,
	source_url: str,
	download_url: str,
	filename: str,
	title: str,
	attribution: str,
	rights: str = "NOASSERTION",
	document_type: str = "manual",
	language: str = "en",
	expected_sha256: str | None = None,
) -> dict[str, Any]:
	if not MACHINE_PATTERN.fullmatch(machine_id):
		raise DefinitionError(f"Invalid machine ID: {machine_id!r}")
	if source not in DIRECT_SOURCES:
		raise DefinitionError(f"Direct manual source must be one of {sorted(DIRECT_SOURCES)}")
	if not ITEM_PATTERN.fullmatch(source_id):
		raise DefinitionError(f"Invalid source ID: {source_id!r}")
	filename = _safe_filename(filename)
	source_url = _https_url(source_url, "Source URL")
	download_url = _https_url(download_url, "Download URL")
	manifest_path = cache_root / "manifest.json"
	if not manifest_path.is_file():
		raise DefinitionError(f"Manual-cache manifest is missing: {manifest_path}")
	manifest = _load_manifest(manifest_path)
	directory = f"official-{source_id}" if source == "manufacturer" else source_id
	relative_path = PurePosixPath("by-machine", machine_id, directory, filename)
	destination = cache_root.joinpath(*relative_path.parts)
	if destination.is_file():
		if destination.stat().st_size < 1 or destination.stat().st_size > MAX_DOCUMENT_BYTES or not _has_pdf_header(destination):
			raise DefinitionError(f"Cached resource is not a valid-sized PDF: {destination}")
	else:
		_download_direct_pdf(download_url, destination, expected_sha256)
	sha256 = file_sha256(destination)
	if expected_sha256 is not None:
		if not SHA256_PATTERN.fullmatch(expected_sha256):
			raise DefinitionError("Expected SHA-256 must be 64 lowercase hexadecimal characters")
		if sha256 != expected_sha256:
			raise DefinitionError("Cached manual SHA-256 does not match the expected digest")
	legacy_document_id = f"{source}.{source_id}.{sha256[:12]}"
	document_id = f"{source}.{source_id}.{machine_id}.{sha256[:12]}"
	record: dict[str, Any] = {
		"id": document_id,
		"machine_id": machine_id,
		"source": source,
		"source_id": source_id,
		"source_url": source_url,
		"download_url": download_url,
		"original_filename": filename,
		"title": title,
		"document_type": document_type,
		"language": language,
		"relative_path": relative_path.as_posix(),
		"bytes": destination.stat().st_size,
		"sha256": sha256,
		"rights": rights,
		"attribution": attribution,
		"acquired_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
		"extraction_status": "pending",
	}
	previous = next((document for document in manifest.get("documents", []) if document.get("id") == document_id), None)
	if previous is None:
		previous = next((document for document in manifest.get("documents", []) if document.get("id") == legacy_document_id and document.get("machine_id") == machine_id and document.get("sha256") == sha256 and document.get("relative_path") == record["relative_path"]), None)
	if previous is not None and previous.get("sha256") == sha256 and previous.get("relative_path") == record["relative_path"]:
		record["acquired_at"] = previous["acquired_at"]
		record["extraction_status"] = previous.get("extraction_status", "pending")
		if "extraction" in previous:
			record["extraction"] = previous["extraction"]
	documents = [document for document in manifest.get("documents", []) if document.get("id") != document_id and not (document.get("id") == legacy_document_id and document.get("machine_id") == machine_id and document.get("sha256") == sha256 and document.get("relative_path") == record["relative_path"])]
	documents.append(record)
	manifest["documents"] = sorted(documents, key=lambda document: (document["machine_id"], document["source"], document["source_id"], document["id"]))
	_write_manifest(manifest_path, manifest)
	return record


def acquire_archive_document(
	cache_root: Path,
	machine_id: str,
	item_id: str,
	requested_file: str | None = None,
	document_type: str = "manual",
	language: str = "en",
) -> dict[str, Any]:
	if not MACHINE_PATTERN.fullmatch(machine_id):
		raise DefinitionError(f"Invalid machine ID: {machine_id!r}")
	if not ITEM_PATTERN.fullmatch(item_id):
		raise DefinitionError(f"Invalid Internet Archive item ID: {item_id!r}")
	manifest_path = cache_root / "manifest.json"
	if not manifest_path.is_file():
		raise DefinitionError(f"Manual-cache manifest is missing: {manifest_path}")
	manifest = _load_manifest(manifest_path)
	metadata_url = f"https://archive.org/metadata/{urllib.parse.quote(item_id, safe='')}"
	metadata = _request_json(metadata_url)
	file_record = _select_original_pdf(metadata, requested_file)
	filename = _safe_filename(file_record["name"])
	expected_size = int(file_record["size"])
	download_url = f"https://archive.org/download/{urllib.parse.quote(item_id, safe='')}/{urllib.parse.quote(filename)}"
	relative_path = PurePosixPath("by-machine", machine_id, f"archive-{item_id}", filename)
	destination = cache_root.joinpath(*relative_path.parts)
	if destination.is_file():
		if destination.stat().st_size != expected_size:
			raise DefinitionError(f"Cached manual has the wrong size: {destination}")
	else:
		_download(download_url, destination, expected_size, file_record.get("md5"), file_record.get("sha1"))
	sha256 = file_sha256(destination)
	item_metadata = metadata.get("metadata", {})
	legacy_document_id = f"archive.{item_id}.{sha256[:12]}"
	document_id = f"archive.{item_id}.{machine_id}.{sha256[:12]}"
	record: dict[str, Any] = {
		"id": document_id,
		"machine_id": machine_id,
		"source": "internet_archive",
		"source_id": item_id,
		"source_url": f"https://archive.org/details/{item_id}",
		"download_url": download_url,
		"original_filename": filename,
		"title": str(item_metadata.get("title") or filename),
		"document_type": document_type,
		"language": language,
		"relative_path": relative_path.as_posix(),
		"bytes": destination.stat().st_size,
		"sha256": sha256,
		"rights": str(item_metadata.get("licenseurl") or item_metadata.get("rights") or "NOASSERTION"),
		"attribution": str(item_metadata.get("creator") or item_metadata.get("uploader") or "Internet Archive item contributor"),
		"uploader": str(item_metadata.get("uploader") or ""),
		"acquired_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
		"extraction_status": "pending",
	}
	if file_record.get("md5"):
		record["md5"] = str(file_record["md5"]).casefold()
	if file_record.get("sha1"):
		record["sha1"] = str(file_record["sha1"]).casefold()
	previous = next((document for document in manifest.get("documents", []) if document.get("id") == document_id), None)
	if previous is None:
		previous = next((document for document in manifest.get("documents", []) if document.get("id") == legacy_document_id and document.get("machine_id") == machine_id and document.get("sha256") == sha256 and document.get("relative_path") == record["relative_path"]), None)
	if previous is not None and previous.get("sha256") == sha256 and previous.get("relative_path") == record["relative_path"]:
		record["acquired_at"] = previous["acquired_at"]
		record["extraction_status"] = previous.get("extraction_status", "pending")
		if "extraction" in previous:
			record["extraction"] = previous["extraction"]
	documents = [document for document in manifest.get("documents", []) if document.get("id") != document_id and not (document.get("id") == legacy_document_id and document.get("machine_id") == machine_id and document.get("sha256") == sha256 and document.get("relative_path") == record["relative_path"])]
	documents.append(record)
	manifest["documents"] = sorted(documents, key=lambda document: (document["machine_id"], document["source"], document["source_id"], document["id"]))
	_write_manifest(manifest_path, manifest)
	return record


def _manifest_document(manifest: dict[str, Any], document_id: str) -> dict[str, Any]:
	documents = manifest.get("documents")
	if not isinstance(documents, list):
		raise DefinitionError("Manual-cache manifest has no document inventory")
	matches = [document for document in documents if isinstance(document, dict) and document.get("id") == document_id]
	if len(matches) != 1:
		raise DefinitionError(f"Manual document ID is missing or ambiguous: {document_id!r}")
	return matches[0]


def _safe_cache_path(cache_root: Path, relative_path: str) -> Path:
	parts = PurePosixPath(relative_path).parts
	if not parts or ".." in parts or parts[0] != "by-machine":
		raise DefinitionError(f"Manual path must remain under by-machine/: {relative_path!r}")
	path = cache_root.joinpath(*parts).resolve()
	root = cache_root.resolve()
	try:
		path.relative_to(root)
	except ValueError as error:
		raise DefinitionError(f"Manual path escapes the cache: {relative_path!r}") from error
	return path


def _page_text(page: Any) -> str:
	return (page.extract_text(layout=True) or "").replace("\x00", "").rstrip()


def _visible_character_count(text: str) -> int:
	return sum(not character.isspace() for character in text)


def _has_useful_text_layer(visible_characters_per_page: list[int]) -> bool:
	"""Reject scans whose only embedded text is page numbering or similar noise."""
	if not visible_characters_per_page:
		return False
	useful_pages = sum(character_count >= 80 for character_count in visible_characters_per_page)
	minimum_useful_pages = max(1, (len(visible_characters_per_page) + 4) // 5)
	return sum(visible_characters_per_page) >= max(1000, len(visible_characters_per_page) * 100) and useful_pages >= minimum_useful_pages


def extract_manual_document(cache_root: Path, document_id: str, table_pages: set[int] | None = None) -> dict[str, Any]:
	"""Extract deterministic text and selected tables beside a cached PDF.

	This intentionally does not perform OCR. A scan without a useful text layer is
	marked ``ocr_required`` so a separate, cheaper OCR workflow can process it.
	"""
	manifest_path = cache_root / "manifest.json"
	if not manifest_path.is_file():
		raise DefinitionError(f"Manual-cache manifest is missing: {manifest_path}")
	manifest = _load_manifest(manifest_path)
	document = _manifest_document(manifest, document_id)
	pdf_path = _safe_cache_path(cache_root, document["relative_path"])
	if not pdf_path.is_file():
		raise DefinitionError(f"Cached manual is missing: {pdf_path}")
	if file_sha256(pdf_path) != document.get("sha256"):
		raise DefinitionError(f"Cached manual hash no longer matches the manifest: {pdf_path}")
	requested_pages = set(table_pages or set())
	pages: list[dict[str, Any]] = []
	try:
		with pdfplumber.open(pdf_path) as pdf:
			invalid_pages = sorted(page for page in requested_pages if page < 1 or page > len(pdf.pages))
			if invalid_pages:
				raise DefinitionError(f"Requested table pages are outside the PDF: {invalid_pages}")
			for page_number, page in enumerate(pdf.pages, start=1):
				text = _page_text(page)
				record: dict[str, Any] = {
					"page": page_number,
					"text": text,
					"text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
				}
				if page_number in requested_pages:
					record["tables"] = page.extract_tables()
				pages.append(record)
	except DefinitionError:
		raise
	except Exception as error:
		raise DefinitionError(f"Unable to extract PDF {pdf_path}: {error}") from error
	visible_characters_per_page = [_visible_character_count(page["text"]) for page in pages]
	character_count = sum(visible_characters_per_page)
	text_pages = sum(bool(page["text"].strip()) for page in pages)
	extraction_status = "text_native" if _has_useful_text_layer(visible_characters_per_page) else "ocr_required"
	extraction: dict[str, Any] = {
		"format": EXTRACTION_FORMAT,
		"version": EXTRACTION_VERSION,
		"document_id": document_id,
		"document_sha256": document["sha256"],
		"extractor": {
			"id": "pdfplumber",
			"version": 1,
			"library_version": getattr(pdfplumber, "__version__", "unknown"),
		},
		"status": extraction_status,
		"page_count": len(pages),
		"text_page_count": text_pages,
		"character_count": character_count,
		"table_pages": sorted(requested_pages),
		"pages": pages,
	}
	extraction_path = pdf_path.parent / "extracted" / "document.json"
	_write_extraction(extraction_path, extraction)
	extraction_relative_path = extraction_path.relative_to(cache_root.resolve()).as_posix()
	document["extraction_status"] = extraction_status
	document["extraction"] = {
		"relative_path": extraction_relative_path,
		"sha256": file_sha256(extraction_path),
		"page_count": len(pages),
		"text_page_count": text_pages,
		"character_count": character_count,
		"table_pages": sorted(requested_pages),
		"extracted_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
	}
	_write_manifest(manifest_path, manifest)
	return extraction
