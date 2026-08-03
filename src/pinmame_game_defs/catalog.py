from __future__ import annotations

import ctypes
import os
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from . import SCHEMA_VERSION
from .errors import CatalogError
from .jsonio import content_sha256, file_sha256, write_json, write_text
from .scope import is_in_scope_driver

PINMAME_MAX_PATH = 512
PINMAME_CALLBACK_COUNT = 12
DRIVER_ID_PATTERN = re.compile(r"^[a-z0-9_]+$")
UNKNOWN_YEAR_PATTERN = re.compile(r"^[?]+$")
VERSION_PATTERN = re.compile(r"^\s*#define\s+VERSION_(MAJOR|MINOR|REV)\s+(\d+)\s*(?://.*)?$", re.MULTILINE)


class _PinmameGame(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char_p),
		("clone_of", ctypes.c_char_p),
		("description", ctypes.c_char_p),
		("year", ctypes.c_char_p),
		("manufacturer", ctypes.c_char_p),
		("flags", ctypes.c_uint32),
		("found", ctypes.c_int32),
	]


class _PinmameConfig(ctypes.Structure):
	_fields_ = [
		("audio_format", ctypes.c_int),
		("sample_rate", ctypes.c_int),
		("vpm_path", ctypes.c_char * PINMAME_MAX_PATH),
		*[(f"callback_{index}", ctypes.c_void_p) for index in range(PINMAME_CALLBACK_COUNT)],
	]


@dataclass(frozen=True, slots=True)
class Driver:
	id: str
	clone_of: str | None
	description: str
	year: str
	manufacturer: str
	flags: int


def _decode(value: bytes | None, field: str) -> str | None:
	if value is None:
		return None
	try:
		return value.decode("utf-8")
	except UnicodeDecodeError as error:
		raise CatalogError(f"LibPinMAME returned non-UTF-8 {field}") from error


def load_libpinmame_games(library_path: Path) -> list[Driver]:
	if not library_path.is_file():
		raise CatalogError(f"LibPinMAME library not found: {library_path}")
	try:
		library = ctypes.CDLL(str(library_path))
	except OSError as error:
		raise CatalogError(f"Unable to load LibPinMAME library {library_path}: {error}") from error
	callback_factory = ctypes.WINFUNCTYPE if os.name == "nt" else ctypes.CFUNCTYPE
	callback_type = callback_factory(None, ctypes.POINTER(_PinmameGame), ctypes.c_void_p)
	library.PinmameSetConfig.argtypes = [ctypes.POINTER(_PinmameConfig)]
	library.PinmameSetConfig.restype = None
	library.PinmameGetGames.argtypes = [callback_type, ctypes.c_void_p]
	library.PinmameGetGames.restype = ctypes.c_int
	rows: list[Driver] = []
	callback_errors: list[BaseException] = []

	@callback_type
	def collect(game_pointer: ctypes.POINTER(_PinmameGame), _user_data: int) -> None:
		if callback_errors:
			return
		try:
			if not game_pointer:
				raise CatalogError("LibPinMAME returned a null game pointer")
			game = game_pointer.contents
			name = _decode(game.name, "driver name")
			description = _decode(game.description, "description")
			year = _decode(game.year, "year")
			manufacturer = _decode(game.manufacturer, "manufacturer")
			if name is None or description is None or year is None or manufacturer is None:
				raise CatalogError("LibPinMAME returned a driver with missing required metadata")
			rows.append(
				Driver(
					id=name,
					clone_of=_decode(game.clone_of, "clone parent") or None,
					description=description,
					year=year,
					manufacturer=manufacturer,
					flags=int(game.flags),
				)
			)
		except BaseException as error:
			callback_errors.append(error)

	config = _PinmameConfig()
	config.audio_format = 0
	config.sample_rate = 44100
	config.vpm_path = b""
	library.PinmameSetConfig(ctypes.byref(config))
	status = int(library.PinmameGetGames(collect, None))
	if status != 0:
		raise CatalogError(f"PinmameGetGames failed with status {status}")
	if callback_errors:
		error = callback_errors[0]
		if isinstance(error, CatalogError):
			raise error
		raise CatalogError(f"PinmameGetGames callback failed: {error}") from error
	validate_driver_catalog(rows)
	return sorted(rows, key=lambda driver: driver.id)


def validate_driver_catalog(drivers: Iterable[Driver]) -> None:
	driver_list = list(drivers)
	if not driver_list:
		raise CatalogError("LibPinMAME returned no supported drivers")
	by_id: dict[str, Driver] = {}
	for driver in driver_list:
		if not DRIVER_ID_PATTERN.fullmatch(driver.id):
			raise CatalogError(f"Invalid PinMAME driver ID: {driver.id!r}")
		if driver.id in by_id:
			raise CatalogError(f"Duplicate PinMAME driver ID: {driver.id}")
		by_id[driver.id] = driver
	for driver in driver_list:
		resolve_root_driver(driver.id, by_id)


def resolve_root_driver(driver_id: str, drivers: dict[str, Driver]) -> str:
	visited: list[str] = []
	current = driver_id
	while True:
		if current in visited:
			cycle = " -> ".join([*visited, current])
			raise CatalogError(f"Clone cycle detected: {cycle}")
		visited.append(current)
		driver = drivers.get(current)
		if driver is None:
			return visited[-2] if len(visited) > 1 else driver_id
		if driver.clone_of is None:
			return current
		current = driver.clone_of


def pinmame_revision(source_root: Path) -> str:
	try:
		result = subprocess.run(
			["git", "-C", str(source_root), "rev-parse", "HEAD"],
			check=True,
			capture_output=True,
			text=True,
		)
	except (OSError, subprocess.CalledProcessError) as error:
		raise CatalogError(f"Unable to resolve PinMAME revision from {source_root}") from error
	revision = result.stdout.strip().lower()
	if not re.fullmatch(r"[0-9a-f]{40}", revision):
		raise CatalogError(f"Unexpected PinMAME revision: {revision!r}")
	return revision


def pinmame_version(source_root: Path) -> str:
	version_path = source_root / "src" / "version.h"
	if not version_path.is_file():
		raise CatalogError(f"PinMAME version header not found: {version_path}")
	parts = {name.lower(): value for name, value in VERSION_PATTERN.findall(version_path.read_text(encoding="utf-8"))}
	if set(parts) != {"major", "minor", "rev"}:
		raise CatalogError(f"Could not parse PinMAME version from {version_path}")
	return f"{parts['major']}.{parts['minor']}.{parts['rev']}"


def _integer_year(value: str) -> int | None:
	match = re.search(r"(?:19|20)\d{2}", value)
	if match is None or UNKNOWN_YEAR_PATTERN.fullmatch(value):
		return None
	return int(match.group(0))


def _source_record(revision: str) -> dict[str, object]:
	return {
		"id": f"pinmame.catalog.{revision[:12]}",
		"kind": "pinmame_catalog",
		"uri": "https://github.com/vpinball/pinmame",
		"revision": revision,
		"locator": "PinmameGetGames",
		"license": "BSD-3-Clause",
		"attribution": "PinMAME contributors",
	}


def _stub_missing() -> list[str]:
	return [
		"identity",
		"controller_platform",
		"input_enumeration",
		"input_semantics",
		"output_enumeration",
		"output_semantics",
		"display_inventory",
		"mechanism_inventory",
		"mechanism_behavior",
		"polarity",
		"variant_differences",
		"recreation_notes",
		"provenance",
	]


def make_stub_definition(root: Driver, family: list[Driver], revision: str) -> dict[str, object]:
	source = _source_record(revision)
	machine_id = f"stub.pinmame.{root.id}"
	driver_records = []
	for driver in family:
		record: dict[str, object] = {
			"id": driver.id,
			"description": driver.description,
			"year": driver.year,
			"manufacturer": driver.manufacturer,
			"flags": driver.flags,
		}
		if driver.clone_of is not None:
			record["clone_of"] = driver.clone_of
		driver_records.append(record)
	return {
		"format": "pinmame-machine-definition",
		"schema_version": SCHEMA_VERSION,
		"machine": {
			"id": machine_id,
			"name": f"STUB - {root.description}",
			"manufacturer": root.manufacturer,
			"year": _integer_year(root.year),
		},
		"coverage": {
			"status": "stub",
			"missing": _stub_missing(),
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "unknown",
				"semantic_naming": "unknown",
				"physical_wiring": "unknown",
				"mechanisms": "unknown",
				"variant_coverage": "candidate",
				"recreation_knowledge": "unknown",
			},
		},
		"drivers": driver_records,
		"inputs": [],
		"outputs": [],
		"displays": [],
		"mechanisms": [],
		"relationships": [],
		"sources": [source],
		"knowledge": {
			"path": f"knowledge/stubs/{root.id}.md",
			"status": "stub",
		},
		"conflicts": [],
	}


def make_stub_knowledge(root: Driver, family: list[Driver], revision: str) -> str:
	driver_ids = ", ".join(f"`{driver.id}`" for driver in family)
	return f"""# STUB - {root.description}

Coverage: **stub - not usable to recreate this machine**

This note was generated from PinMAME catalog identity only. It deliberately contains no inferred playfield or mechanism claims. The definition remains incomplete until every section below is supported by cited evidence.

## Identity and variants

- Candidate root driver: `{root.id}`
- Candidate manufacturer: {root.manufacturer}
- Candidate year: {root.year}
- Drivers currently grouped by the PinMAME clone chain: {driver_ids}

## Playfield devices

Unknown. Complete switch, lamp/GI, controlled-device, display, and physical-type inventories are required.

## Custom mechanisms

Unknown. Check manuals, schematics, PinMAME source/simulations, VPX scripts, service diagnostics, gameplay traces, and physical-machine references. If no custom mechanism exists, document the evidence checked before marking this section complete.

## Ball-state transitions

Unknown.

## Controller interactions

Unknown.

## Service and setup information

Unknown.

## Timing and tuning observations

Unknown.

## Recreation guidance

Do not use this stub as an authoring definition.

## Unresolved questions

- Does the clone chain represent one physical machine or multiple conversions/custom machines?
- What is the complete semantic I/O inventory?
- Which custom mechanisms, wiring relationships, and variant differences must be modeled?

## Sources

- PinMAME `{revision}`, public `PinmameGetGames` catalog entry for `{root.id}`.
"""


def generate_stub_catalog(library_path: Path, pinmame_source: Path, repository_root: Path) -> dict[str, object]:
	drivers = [driver for driver in load_libpinmame_games(library_path) if is_in_scope_driver(driver.id)]
	revision = pinmame_revision(pinmame_source)
	version = pinmame_version(pinmame_source)
	by_id = {driver.id: driver for driver in drivers}
	abstract_parent_counts: dict[str, int] = defaultdict(int)
	for driver in drivers:
		if driver.clone_of is not None and driver.clone_of not in by_id:
			abstract_parent_counts[driver.clone_of] += 1
	families: dict[str, list[Driver]] = defaultdict(list)
	for driver in drivers:
		families[resolve_root_driver(driver.id, by_id)].append(driver)
	definitions: dict[str, dict[str, object]] = {}
	for root_id, family in sorted(families.items()):
		family.sort(key=lambda driver: driver.id)
		root = by_id[root_id]
		definition = make_stub_definition(root, family, revision)
		definitions[root_id] = definition
		write_json(repository_root / "machines" / "stubs" / f"{root_id}.json", definition)
		write_text(repository_root / "knowledge" / "stubs" / f"{root_id}.md", make_stub_knowledge(root, family, revision))
	catalog_drivers: list[dict[str, object]] = []
	for driver in drivers:
		root_id = resolve_root_driver(driver.id, by_id)
		definition_hash = content_sha256(definitions[root_id])
		record: dict[str, object] = {
			"id": driver.id,
			"root_driver": root_id,
			"description": driver.description,
			"year": driver.year,
			"manufacturer": driver.manufacturer,
			"flags": driver.flags,
			"machine_id": f"stub.pinmame.{root_id}",
			"definition": f"machines/stubs/{root_id}.json",
			"definition_sha256": definition_hash,
			"coverage_status": "stub",
		}
		if driver.clone_of is not None:
			record["clone_of"] = driver.clone_of
		catalog_drivers.append(record)
	catalog_machines = [
		{
			"id": f"stub.pinmame.{root_id}",
			"root_drivers": [root_id],
			"definition": f"machines/stubs/{root_id}.json",
			"definition_sha256": content_sha256(definitions[root_id]),
			"driver_count": len(families[root_id]),
			"processing_year": _integer_year(by_id[root_id].year),
			"machine_kind": "unknown",
			"coverage_status": "stub",
			"missing": definitions[root_id]["coverage"]["missing"],
		}
		for root_id in sorted(families)
	]
	catalog_machines.sort(
		key=lambda machine: (
			-(machine["processing_year"] or 0),
			str(definitions[machine["root_drivers"][0]]["machine"]["manufacturer"]).casefold(),
			str(definitions[machine["root_drivers"][0]]["machine"]["name"]).casefold(),
			machine["id"],
		)
	)
	for processing_order, machine in enumerate(catalog_machines, start=1):
		machine["processing_order"] = processing_order
	catalog: dict[str, object] = {
		"format": "pinmame-driver-catalog",
		"schema_version": SCHEMA_VERSION,
		"source": {
			"pinmame_revision": revision,
			"library_sha256": file_sha256(library_path),
			"library_version": version,
		},
		"summary": {
			"driver_count": len(drivers),
			"root_driver_count": len(families),
			"machine_count": len(families),
			"game_count": len(families),
			"non_game_count": 0,
			"stub_count": len(families),
			"partial_count": 0,
			"author_ready_count": 0,
		},
		"abstract_parents": [
			{"id": parent_id, "direct_child_count": direct_child_count}
			for parent_id, direct_child_count in sorted(abstract_parent_counts.items())
		],
		"drivers": catalog_drivers,
		"machines": catalog_machines,
	}
	write_json(repository_root / "catalog" / "pinmame.json", catalog)
	return catalog
