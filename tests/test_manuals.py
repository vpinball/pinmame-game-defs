import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pinmame_game_defs.errors import DefinitionError
from pinmame_game_defs.jsonio import load_json, write_json
from pinmame_game_defs.manuals import _SameHostHttpsRedirectHandler, _has_useful_text_layer, _visible_character_count, acquire_archive_document, acquire_url_document


def _document_record(document_id: str, machine_id: str, relative_path: str, sha256: str, size: int) -> dict[str, object]:
	return {
		"id": document_id,
		"machine_id": machine_id,
		"source": "internet_archive",
		"source_id": "example-item",
		"source_url": "https://archive.org/details/example-item",
		"download_url": "https://archive.org/download/example-item/manual.pdf",
		"original_filename": "manual.pdf",
		"title": "Example manual",
		"document_type": "manual",
		"language": "en",
		"relative_path": relative_path,
		"bytes": size,
		"sha256": sha256,
		"rights": "NOASSERTION",
		"attribution": "Example",
		"acquired_at": "2026-08-02T00:00:00Z",
		"extraction_status": "pending",
	}


class ManualExtractionTests(unittest.TestCase):
	def test_visible_character_count_ignores_layout_whitespace(self) -> None:
		self.assertEqual(2, _visible_character_count("  12\n\t"))

	def test_page_numbers_do_not_qualify_as_a_text_layer(self) -> None:
		self.assertFalse(_has_useful_text_layer([1, 1] + [2] * 46))

	def test_a_document_with_substantive_text_qualifies(self) -> None:
		self.assertTrue(_has_useful_text_layer([250] * 20))

	def test_a_few_text_pages_do_not_hide_a_scanned_document(self) -> None:
		self.assertFalse(_has_useful_text_layer([1000, 1000] + [2] * 18))

	def test_reacquiring_cached_url_document_preserves_extraction(self) -> None:
		with TemporaryDirectory() as temporary:
			cache_root = Path(temporary)
			write_json(cache_root / "manifest.json", {"format": "pinmame-manual-cache", "version": 1, "documents": []})
			destination = cache_root / "by-machine" / "stern.example.2024" / "official-stern" / "manual.pdf"
			destination.parent.mkdir(parents=True)
			destination.write_bytes(b"%PDF-1.4\n%%EOF\n")
			arguments = {
				"cache_root": cache_root,
				"machine_id": "stern.example.2024",
				"source": "manufacturer",
				"source_id": "stern",
				"source_url": "https://example.com/manuals/",
				"download_url": "https://example.com/manual.pdf",
				"filename": "manual.pdf",
				"title": "Example manual",
				"attribution": "Example",
			}
			first = acquire_url_document(**arguments)
			manifest = load_json(cache_root / "manifest.json")
			manifest["documents"][0]["extraction_status"] = "complete"
			manifest["documents"][0]["extraction"] = {
				"relative_path": "by-machine/stern.example.2024/official-stern/extracted/document.json",
				"sha256": "0" * 64,
				"page_count": 1,
				"text_page_count": 1,
				"character_count": 10,
				"table_pages": [],
				"extracted_at": "2026-08-02T00:00:00Z",
			}
			write_json(cache_root / "manifest.json", manifest)

			second = acquire_url_document(**arguments)

			self.assertEqual(first["acquired_at"], second["acquired_at"])
			self.assertEqual("complete", second["extraction_status"])
			self.assertEqual("0" * 64, second["extraction"]["sha256"])

	def test_identical_manuals_for_different_machines_keep_distinct_records(self) -> None:
		with TemporaryDirectory() as temporary:
			cache_root = Path(temporary)
			write_json(cache_root / "manifest.json", {"format": "pinmame-manual-cache", "version": 1, "documents": []})
			for machine_id in ("stern.example-pro.2024", "stern.example-le.2024"):
				destination = cache_root / "by-machine" / machine_id / "official-stern" / "manual.pdf"
				destination.parent.mkdir(parents=True)
				destination.write_bytes(b"%PDF-1.4\n%%EOF\n")
				acquire_url_document(
					cache_root=cache_root,
					machine_id=machine_id,
					source="manufacturer",
					source_id="stern",
					source_url="https://example.com/manuals/",
					download_url="https://example.com/manual.pdf",
					filename="manual.pdf",
					title="Example manual",
					attribution="Example",
				)

			manifest = load_json(cache_root / "manifest.json")
			self.assertEqual(2, len(manifest["documents"]))
			self.assertEqual(2, len({document["id"] for document in manifest["documents"]}))
			self.assertEqual({"stern.example-pro.2024", "stern.example-le.2024"}, {document["machine_id"] for document in manifest["documents"]})

	def test_cached_direct_manual_must_match_expected_sha256(self) -> None:
		with TemporaryDirectory() as temporary:
			cache_root = Path(temporary)
			write_json(cache_root / "manifest.json", {"format": "pinmame-manual-cache", "version": 1, "documents": []})
			destination = cache_root / "by-machine" / "stern.example.2024" / "official-stern" / "manual.pdf"
			destination.parent.mkdir(parents=True)
			destination.write_bytes(b"%PDF-1.4\n%%EOF\n")
			with self.assertRaisesRegex(DefinitionError, "does not match"):
				acquire_url_document(cache_root, "stern.example.2024", "manufacturer", "stern", "https://example.com/manuals/", "https://example.com/manual.pdf", "manual.pdf", "Example manual", "Example", expected_sha256="0" * 64)

	def test_direct_manual_redirect_cannot_change_host(self) -> None:
		handler = _SameHostHttpsRedirectHandler()
		request = __import__("urllib.request").request.Request("https://example.com/manual.pdf")
		with self.assertRaisesRegex(DefinitionError, "must remain HTTPS"):
			handler.redirect_request(request, None, 302, "Found", {}, "https://cdn.example.net/manual.pdf")

	def test_duplicate_manifest_document_ids_are_rejected(self) -> None:
		with TemporaryDirectory() as temporary:
			cache_root = Path(temporary)
			payload = b"%PDF-1.4\n%%EOF\n"
			sha256 = hashlib.sha256(payload).hexdigest()
			record = _document_record("archive.example-item.legacy", "stern.example.2024", "by-machine/stern.example.2024/archive-example-item/manual.pdf", sha256, len(payload))
			write_json(cache_root / "manifest.json", {"format": "pinmame-manual-cache", "version": 1, "documents": [record, dict(record)]})
			with self.assertRaisesRegex(DefinitionError, "duplicate document ID"):
				acquire_url_document(cache_root, "stern.example.2024", "manufacturer", "stern", "https://example.com/manuals/", "https://example.com/manual.pdf", "manual.pdf", "Example manual", "Example")

	def test_archive_legacy_id_migration_preserves_extraction(self) -> None:
		with TemporaryDirectory() as temporary:
			cache_root = Path(temporary)
			machine_id = "stern.example.2024"
			payload = b"%PDF-1.4\n%%EOF\n"
			sha256 = hashlib.sha256(payload).hexdigest()
			relative_path = f"by-machine/{machine_id}/archive-example-item/manual.pdf"
			destination = cache_root.joinpath(*Path(relative_path).parts)
			destination.parent.mkdir(parents=True)
			destination.write_bytes(payload)
			legacy = _document_record(f"archive.example-item.{sha256[:12]}", machine_id, relative_path, sha256, len(payload))
			legacy["extraction_status"] = "complete"
			legacy["extraction"] = {"relative_path": f"by-machine/{machine_id}/archive-example-item/extracted/document.json", "sha256": "0" * 64, "page_count": 1, "text_page_count": 1, "character_count": 10, "table_pages": [], "extracted_at": "2026-08-02T00:00:00Z"}
			write_json(cache_root / "manifest.json", {"format": "pinmame-manual-cache", "version": 1, "documents": [legacy]})
			metadata = {"files": [{"name": "manual.pdf", "source": "original", "size": str(len(payload))}], "metadata": {"title": "Example manual"}}
			with patch("pinmame_game_defs.manuals._request_json", return_value=metadata):
				record = acquire_archive_document(cache_root, machine_id, "example-item")
			self.assertEqual(f"archive.example-item.{machine_id}.{sha256[:12]}", record["id"])
			self.assertEqual("complete", record["extraction_status"])
			self.assertEqual("0" * 64, record["extraction"]["sha256"])
			self.assertEqual(1, len(load_json(cache_root / "manifest.json")["documents"]))


if __name__ == "__main__":
	unittest.main()
