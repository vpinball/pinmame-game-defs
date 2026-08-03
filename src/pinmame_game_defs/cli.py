from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .catalog import generate_stub_catalog
from .coverage import build_coverage_report, write_coverage_report
from .errors import DefinitionError
from .legacy import import_legacy_definitions
from .jsonio import load_json, write_json, write_text
from .manuals import acquire_archive_document, acquire_url_document, extract_manual_document
from .pinmame_source import extract_pinmame_simulations
from .registry import rebuild_catalog
from .roms import index_rom_corpus
from .spatial import extract_from_vpx, extract_spatial_candidates, render_spatial_overlay
from .validation import validate_repository
from .vpx_source import extract_vpx_corpora


def _path(value: str) -> Path:
	return Path(value).expanduser().resolve()


def _repository_root(value: str | None) -> Path:
	return _path(value) if value else Path.cwd().resolve()


def _positive_page_set(value: str) -> set[int]:
	pages: set[int] = set()
	for token in value.split(","):
		token = token.strip()
		if not token:
			continue
		if "-" in token:
			start_text, end_text = token.split("-", 1)
			start, end = int(start_text), int(end_text)
			if start < 1 or end < start:
				raise argparse.ArgumentTypeError(f"Invalid page range: {token!r}")
			pages.update(range(start, end + 1))
		else:
			page = int(token)
			if page < 1:
				raise argparse.ArgumentTypeError(f"Invalid page: {token!r}")
			pages.add(page)
	return pages


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="pinmame-game-defs", description="Generate and validate VPE-neutral PinMAME machine definitions.")
	parser.add_argument("--repository-root", help="Repository checkout to read or update; defaults to the current directory.")
	subparsers = parser.add_subparsers(dest="command", required=True)

	catalog_parser = subparsers.add_parser("generate-catalog", help="Enumerate in-scope physical-machine LibPinMAME drivers and generate explicit stubs.")
	catalog_parser.add_argument("--library", required=True, type=_path, help="Pinned LibPinMAME shared library.")
	catalog_parser.add_argument("--pinmame-source", required=True, type=_path, help="Pinned PinMAME source checkout used to build the library.")

	subparsers.add_parser("validate", help="Validate catalog reachability, hashes, canonical fields, references, and author-ready gates.")
	subparsers.add_parser("import-legacy", help="Migrate legacy games/platforms into partial VPE-neutral definitions and rebuild the exact driver registry.")
	pinmame_source_parser = subparsers.add_parser("extract-pinmame-sims", help="Extract candidate semantic I/O, state, mechanism, and recreation evidence from PinMAME simulations.")
	pinmame_source_parser.add_argument("--pinmame-source", required=True, type=_path, help="Pinned PinMAME source checkout.")
	vpx_parser = subparsers.add_parser("extract-vpx", help="Extract candidate semantic I/O and mechanism evidence from both pinned VPX script corpora.")
	vpx_parser.add_argument("--vpxtable-scripts", required=True, type=_path, help="Pinned sverrewl/vpxtable_scripts checkout.")
	vpx_parser.add_argument("--vpx-standalone-scripts", required=True, type=_path, help="Pinned jsm174/vpx-standalone-scripts checkout.")
	rom_parser = subparsers.add_parser("index-roms", help="Create an external, incremental hash/CRC index of an authorized ROM corpus without extracting ROMs.")
	rom_parser.add_argument("--rom-root", required=True, type=_path, help="Directory containing PinMAME ZIP archives.")
	rom_parser.add_argument("--output", required=True, type=_path, help="External JSON index path; ROM bytes are never copied into the repository.")
	rom_parser.add_argument("--content-hashes", action="store_true", help="Also stream/decompress every member and record its SHA-256; CRC32 is always read from ZIP metadata.")
	archive_parser = subparsers.add_parser("acquire-archive-manual", help="Download one original Internet Archive manual into the organized external cache.")
	archive_parser.add_argument("--cache-root", required=True, type=_path, help="External manual cache containing manifest.json.")
	archive_parser.add_argument("--machine-id", required=True, help="Canonical physical-machine ID.")
	archive_parser.add_argument("--item", required=True, help="Internet Archive item identifier.")
	archive_parser.add_argument("--file", help="Exact original PDF filename when the item contains more than one.")
	archive_parser.add_argument("--document-type", default="manual", choices=("manual", "schematics", "parts_list", "service_bulletin", "rulesheet", "other"))
	archive_parser.add_argument("--language", default="en")
	url_parser = subparsers.add_parser("acquire-url-manual", help="Download one HTTPS-hosted manual into the organized external cache.")
	url_parser.add_argument("--cache-root", required=True, type=_path, help="External manual cache containing manifest.json.")
	url_parser.add_argument("--machine-id", required=True, help="Canonical physical-machine ID.")
	url_parser.add_argument("--source", required=True, choices=("ipdb", "manufacturer", "other"))
	url_parser.add_argument("--source-id", required=True, help="Stable short identifier for the hosting source.")
	url_parser.add_argument("--source-url", required=True, help="HTTPS page documenting the source.")
	url_parser.add_argument("--download-url", required=True, help="Direct HTTPS PDF URL.")
	url_parser.add_argument("--expected-sha256", help="Optional trusted lowercase SHA-256 digest required before the PDF enters the cache.")
	url_parser.add_argument("--filename", required=True, help="Original or stable local PDF filename.")
	url_parser.add_argument("--title", required=True)
	url_parser.add_argument("--attribution", required=True)
	url_parser.add_argument("--rights", default="NOASSERTION")
	url_parser.add_argument("--document-type", default="manual", choices=("manual", "schematics", "parts_list", "service_bulletin", "rulesheet", "other"))
	url_parser.add_argument("--language", default="en")
	extract_manual_parser = subparsers.add_parser("extract-manual", help="Extract deterministic text and selected tables beside a cached manual PDF.")
	extract_manual_parser.add_argument("--cache-root", required=True, type=_path, help="External manual cache containing manifest.json.")
	extract_manual_parser.add_argument("--document-id", required=True, help="Document ID from the manual-cache manifest.")
	extract_manual_parser.add_argument("--table-pages", type=_positive_page_set, default=set(), help="Comma-separated PDF pages or ranges whose tables should also be extracted.")
	coverage_parser = subparsers.add_parser("coverage", help="Print or update the fail-closed coverage report.")
	coverage_parser.add_argument("--write", action="store_true", help="Write reports/coverage.json and reports/coverage.md.")
	spatial_parser = subparsers.add_parser("extract-spatial", help="Extract deterministic, candidate-only normalized geometry from a VPX table.")
	spatial_input = spatial_parser.add_mutually_exclusive_group(required=True)
	spatial_input.add_argument("--extracted-dir", type=_path, help="Existing vpxtool extraction directory containing JSON game data and items.")
	spatial_input.add_argument("--vpx", type=_path, help="VPX source file to extract with --vpxtool.")
	spatial_parser.add_argument("--source-vpx", type=_path, help="Source VPX for --extracted-dir; required because evidence records its SHA-256 and byte size.")
	spatial_parser.add_argument("--vpxtool", type=_path, help="External vpxtool executable; required with --vpx and never vendored by this repository.")
	spatial_parser.add_argument("--output", required=True, type=_path, help="Candidate evidence JSON output path.")
	overlay_parser = subparsers.add_parser("render-spatial-overlay", help="Render canonical machine spatial records as a deterministic SVG overlay.")
	overlay_parser.add_argument("--definition", required=True, type=_path, help="Canonical machine-definition JSON file.")
	overlay_parser.add_argument("--output", required=True, type=_path, help="SVG output path.")
	return parser


def _generate_catalog(args: argparse.Namespace, repository_root: Path) -> int:
	catalog = generate_stub_catalog(args.library, args.pinmame_source, repository_root)
	catalog = rebuild_catalog(repository_root)
	report = write_coverage_report(repository_root)
	print(
		f"Generated {catalog['summary']['driver_count']} driver records and "
		f"{catalog['summary']['machine_count']} explicit stubs from PinMAME {catalog['source']['pinmame_revision']}."
	)
	print(f"Author-ready coverage: {report['author_ready_count']}/{report['machine_count']} ({report['author_ready_percent']:.4f}%).")
	return 0


def _validate(repository_root: Path) -> int:
	errors = validate_repository(repository_root)
	if errors:
		for error in errors:
			print(error, file=sys.stderr)
		print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
		return 1
	print("Validation passed.")
	return 0


def _coverage(args: argparse.Namespace, repository_root: Path) -> int:
	report = write_coverage_report(repository_root) if args.write else build_coverage_report(repository_root)
	print(json.dumps(report, indent=2, sort_keys=True))
	return 0 if report["completion_gate"] else 2


def main(argv: Sequence[str] | None = None) -> None:
	parser = _build_parser()
	args = parser.parse_args(argv)
	repository_root = _repository_root(args.repository_root)
	try:
		if args.command == "generate-catalog":
			status = _generate_catalog(args, repository_root)
		elif args.command == "validate":
			status = _validate(repository_root)
		elif args.command == "coverage":
			status = _coverage(args, repository_root)
		elif args.command == "extract-spatial":
			if args.extracted_dir is not None:
				if args.source_vpx is None:
					raise DefinitionError("--source-vpx is required with --extracted-dir so candidate evidence can record the VPX SHA-256 and byte size")
				report = extract_spatial_candidates(args.extracted_dir, args.source_vpx)
			else:
				if args.vpxtool is None:
					raise DefinitionError("--vpxtool is required with --vpx")
				report = extract_from_vpx(args.vpx, args.vpxtool)
			write_json(args.output, report)
			print(f"Extracted {len(report['objects'])} candidate spatial points.")
			status = 0
		elif args.command == "render-spatial-overlay":
			write_text(args.output, render_spatial_overlay(load_json(args.definition)))
			print(f"Rendered spatial overlay: {args.output}")
			status = 0
		elif args.command == "import-legacy":
			report = import_legacy_definitions(repository_root)
			write_coverage_report(repository_root)
			print(f"Created {report['created_machine_count']} partial physical-machine definitions from legacy sources.")
			print(f"Catalog now contains {report['catalog_summary']['machine_count']} records: {report['catalog_summary']['partial_count']} partial and {report['catalog_summary']['stub_count']} stubs.")
			status = 0
		elif args.command == "extract-pinmame-sims":
			report = extract_pinmame_simulations(args.pinmame_source, repository_root)
			print(f"Extracted {report['file_count']} PinMAME simulations ({report['full_count']} full, {report['preliminary_count']} preliminary).")
			print(f"Candidates: {report['named_switch_candidate_count']} named switches and {report['named_output_candidate_count']} named outputs.")
			status = 0
		elif args.command == "extract-vpx":
			report = extract_vpx_corpora(
				[
					("vpxtable-scripts", args.vpxtable_scripts, "https://github.com/sverrewl/vpxtable_scripts"),
					("vpx-standalone-scripts", args.vpx_standalone_scripts, "https://github.com/jsm174/vpx-standalone-scripts"),
				],
				repository_root,
			)
			print(f"Extracted {report['script_count']} VPX scripts; {report['mapped_script_count']} map to the pinned PinMAME catalog.")
			print(f"Candidates: {report['switch_candidate_count']} switches, {report['output_candidate_count']} outputs, and {report['mechanism_candidate_count']} mechanism lines.")
			status = 0
		elif args.command == "index-roms":
			report = index_rom_corpus(args.rom_root, repository_root / "catalog" / "pinmame.json", args.output, args.content_hashes)
			summary = report["summary"]
			print(f"Indexed {summary['archive_count']} ROM archives; {summary['matched_driver_count']}/{summary['catalog_driver_count']} pinned drivers have same-named archives.")
			print(f"Invalid ZIPs: {summary['invalid_archive_count']}; unmatched archives: {summary['unmatched_archive_count']}; member SHA-256: {'enabled' if report['content_hashes'] else 'disabled'}.")
			status = 0
		elif args.command == "acquire-archive-manual":
			record = acquire_archive_document(args.cache_root, args.machine_id, args.item, args.file, args.document_type, args.language)
			print(f"Cached {record['title']} ({record['bytes']} bytes, sha256 {record['sha256']}) at {record['relative_path']}.")
			status = 0
		elif args.command == "acquire-url-manual":
			record = acquire_url_document(args.cache_root, args.machine_id, args.source, args.source_id, args.source_url, args.download_url, args.filename, args.title, args.attribution, args.rights, args.document_type, args.language, args.expected_sha256)
			print(f"Cached {record['title']} ({record['bytes']} bytes, sha256 {record['sha256']}) at {record['relative_path']}.")
			status = 0
		elif args.command == "extract-manual":
			extraction = extract_manual_document(args.cache_root, args.document_id, args.table_pages)
			print(
				f"Extracted {extraction['page_count']} pages ({extraction['text_page_count']} with text, "
				f"{extraction['character_count']} characters); status {extraction['status']}."
			)
			status = 0
		else:
			parser.error(f"Unknown command {args.command}")
			raise AssertionError("unreachable")
	except DefinitionError as error:
		print(str(error), file=sys.stderr)
		status = 1
	raise SystemExit(status)
