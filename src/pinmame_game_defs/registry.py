from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .catalog import Driver, make_stub_definition, make_stub_knowledge
from .errors import CatalogError
from .jsonio import content_sha256, load_json, write_json, write_text


NON_GAME_KINDS = {"diagnostic_software", "system_software"}


def _driver_from_record(record: dict[str, Any]) -> Driver:
	return Driver(
		id=record["id"],
		clone_of=record.get("clone_of"),
		description=record["description"],
		year=record["year"],
		manufacturer=record["manufacturer"],
		flags=record["flags"],
	)


def _definition_paths(repository_root: Path) -> list[Path]:
	return sorted(
		path
		for path in (repository_root / "machines").glob("**/*.json")
		if "stubs" not in path.relative_to(repository_root / "machines").parts
	)


def _prune_generated_stubs(repository_root: Path, active_roots: set[str]) -> None:
	for relative_directory, suffix in ((Path("machines/stubs"), ".json"), (Path("knowledge/stubs"), ".md")):
		directory = repository_root / relative_directory
		if not directory.is_dir():
			continue
		for path in directory.iterdir():
			if path.suffix != suffix or path.stem in active_roots:
				continue
			if path.is_symlink() or not path.is_file() or path.parent.resolve() != directory.resolve():
				raise CatalogError(f"Refusing to prune unexpected generated-stub path: {path}")
			path.unlink()


def _catalog_machine(
	definition: dict[str, Any],
	definition_path: str,
	driver_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
	drivers = definition["drivers"]
	root_drivers = sorted({driver_records[driver["id"]]["root_driver"] for driver in drivers})
	return {
		"id": definition["machine"]["id"],
		"root_drivers": root_drivers,
		"definition": definition_path,
		"definition_sha256": content_sha256(definition),
		"driver_count": len(drivers),
		"processing_year": definition["machine"].get("year"),
		"machine_kind": definition["machine"].get("kind", "unknown"),
		"coverage_status": definition["coverage"]["status"],
		"missing": definition["coverage"]["missing"],
		"_sort_manufacturer": definition["machine"]["manufacturer"].casefold(),
		"_sort_name": definition["machine"]["name"].casefold(),
	}


def rebuild_catalog(repository_root: Path) -> dict[str, Any]:
	"""Rebuild the exact driver registry around curated definitions and residual stubs.

	Curated definitions own only the driver IDs they list. This permits a single PinMAME
	clone tree to be split between physical products and one physical product to span
	multiple clone-tree roots. Every unclaimed driver remains visibly assigned to a stub.
	"""
	catalog_path = repository_root / "catalog" / "pinmame.json"
	if not catalog_path.is_file():
		raise CatalogError("Generate the pinned PinMAME catalog before rebuilding the registry")
	previous = load_json(catalog_path)
	driver_records = {record["id"]: dict(record) for record in previous["drivers"]}
	all_drivers = {driver_id: _driver_from_record(record) for driver_id, record in driver_records.items()}
	assignments: dict[str, tuple[dict[str, Any], str]] = {}
	curated: list[tuple[dict[str, Any], str]] = []
	machine_ids: dict[str, str] = {}
	for path in _definition_paths(repository_root):
		definition = load_json(path)
		relative_path = path.relative_to(repository_root).as_posix()
		if definition.get("format") != "pinmame-machine-definition":
			raise CatalogError(f"Unexpected machine document format: {relative_path}")
		machine_id = definition.get("machine", {}).get("id")
		if machine_id in machine_ids:
			raise CatalogError(f"Machine ID {machine_id!r} is defined by both {machine_ids[machine_id]} and {relative_path}")
		if isinstance(machine_id, str):
			machine_ids[machine_id] = relative_path
		for driver in definition.get("drivers", []):
			driver_id = driver.get("id")
			if driver_id not in driver_records:
				raise CatalogError(f"{relative_path} references unsupported driver {driver_id!r}")
			if driver_id in assignments:
				other_path = assignments[driver_id][1]
				raise CatalogError(f"Driver {driver_id!r} is assigned by both {other_path} and {relative_path}")
			assignments[driver_id] = (definition, relative_path)
		curated.append((definition, relative_path))

	residual_families: dict[str, list[Driver]] = defaultdict(list)
	for driver_id, record in driver_records.items():
		if driver_id not in assignments:
			residual_families[record["root_driver"]].append(all_drivers[driver_id])

	revision = previous["source"]["pinmame_revision"]
	stub_definitions: list[tuple[dict[str, Any], str]] = []
	for root_id, family in sorted(residual_families.items()):
		family.sort(key=lambda driver: driver.id)
		root = all_drivers[root_id]
		definition = make_stub_definition(root, family, revision)
		relative_path = f"machines/stubs/{root_id}.json"
		write_json(repository_root / relative_path, definition)
		write_text(repository_root / "knowledge" / "stubs" / f"{root_id}.md", make_stub_knowledge(root, family, revision))
		stub_definitions.append((definition, relative_path))
		for driver in family:
			assignments[driver.id] = (definition, relative_path)
	_prune_generated_stubs(repository_root, set(residual_families))

	if set(assignments) != set(driver_records):
		missing = sorted(set(driver_records) - set(assignments))
		raise CatalogError(f"Registry rebuild left drivers unassigned: {missing[:10]}")

	machines: list[dict[str, Any]] = []
	for definition, relative_path in [*curated, *stub_definitions]:
		machines.append(_catalog_machine(definition, relative_path, driver_records))
	machines.sort(
		key=lambda machine: (
			-(machine["processing_year"] or 0),
			machine["_sort_manufacturer"],
			machine["_sort_name"],
			machine["id"],
		)
	)
	for order, machine in enumerate(machines, start=1):
		del machine["_sort_manufacturer"]
		del machine["_sort_name"]
		machine["processing_order"] = order

	machine_by_id = {machine["id"]: machine for machine in machines}
	for driver_id, record in driver_records.items():
		definition, relative_path = assignments[driver_id]
		machine = machine_by_id[definition["machine"]["id"]]
		record.update(
			{
				"machine_id": machine["id"],
				"definition": relative_path,
				"definition_sha256": machine["definition_sha256"],
				"coverage_status": machine["coverage_status"],
			}
		)

	status_counts = {status: sum(machine["coverage_status"] == status for machine in machines) for status in ("stub", "partial", "author_ready")}
	game_count = sum(machine["machine_kind"] not in NON_GAME_KINDS for machine in machines)
	previous["drivers"] = sorted(driver_records.values(), key=lambda record: record["id"])
	previous["machines"] = machines
	previous["summary"].update(
		{
			"driver_count": len(driver_records),
			"machine_count": len(machines),
			"game_count": game_count,
			"non_game_count": len(machines) - game_count,
			"stub_count": status_counts["stub"],
			"partial_count": status_counts["partial"],
			"author_ready_count": status_counts["author_ready"],
		}
	)
	write_json(catalog_path, previous)
	return previous
