from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from .errors import DefinitionError
from .jsonio import canonical_bytes, file_sha256, load_json, write_json, write_text


OPDB_SNAPSHOT_URI = "https://mp-data.sfo3.cdn.digitaloceanspaces.com/latest-opdb.json"
OPDB_ID_PATTERN = re.compile(r"^G[A-Za-z0-9]+(?:-[A-Za-z0-9]+){1,2}$")


@dataclass(frozen=True, slots=True)
class OpdbResolution:
	machine_id: str
	definition: str
	opdb_id: str
	family_opdb_id: str
	ipdb_id: int
	mapped_driver_count: int
	mapped_opdb_ids: tuple[str, ...]
	resolution: str


def _load_mapping(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
	with path.open("r", encoding="utf-8-sig", newline="") as stream:
		reader = csv.DictReader(stream)
		if reader.fieldnames != ["romset", "opdb_id"]:
			raise DefinitionError(f"{path}: expected CSV columns romset,opdb_id")
		mapping: dict[str, str] = {}
		rows: list[dict[str, str]] = []
		for line_number, row in enumerate(reader, start=2):
			romset = (row.get("romset") or "").strip()
			opdb_id = (row.get("opdb_id") or "").strip()
			if not romset or not re.fullmatch(r"[a-z0-9_]+", romset):
				raise DefinitionError(f"{path}:{line_number}: invalid PinMAME ROM set {romset!r}")
			if not OPDB_ID_PATTERN.fullmatch(opdb_id):
				raise DefinitionError(f"{path}:{line_number}: invalid OPDB ID {opdb_id!r}")
			if romset in mapping:
				raise DefinitionError(f"{path}:{line_number}: duplicate PinMAME ROM set {romset}")
			mapping[romset] = opdb_id
			rows.append({"romset": romset, "opdb_id": opdb_id})
	return mapping, rows


def _snapshot_indexes(snapshot: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[int, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
	groups = snapshot.get("machineGroups")
	machines = snapshot.get("machines")
	aliases = snapshot.get("aliases")
	if not isinstance(groups, list) or not isinstance(machines, list) or not isinstance(aliases, list):
		raise DefinitionError("OPDB snapshot must contain machineGroups, machines, and aliases arrays")
	group_by_id = {record.get("opdbId"): record for record in groups if isinstance(record, dict) and isinstance(record.get("opdbId"), str)}
	records = [record for record in [*machines, *aliases] if isinstance(record, dict) and isinstance(record.get("opdbId"), str)]
	record_by_id = {record["opdbId"]: record for record in records}
	if len(record_by_id) != len(records):
		raise DefinitionError("OPDB snapshot contains duplicate machine or alias IDs")
	by_ipdb: dict[int, list[dict[str, Any]]] = defaultdict(list)
	by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
	for record in records:
		by_group[_group_id(record["opdbId"])].append(record)
		if isinstance(record.get("ipdbId"), int):
			by_ipdb[record["ipdbId"]].append(record)
	return group_by_id, record_by_id, dict(by_ipdb), dict(by_group)


def _group_id(opdb_id: str) -> str:
	return opdb_id.split("-", 1)[0]


def opdb_family_id(group_id: str) -> str:
	digest = hashlib.sha256(group_id.encode("ascii")).hexdigest()[:8]
	return f"opdb.{group_id.casefold()}.{digest}"


def _family_filename(group_id: str, casefold_peers: list[str]) -> str:
	if group_id == sorted(casefold_peers)[0]:
		return f"{group_id.casefold()}.json"
	return f"{group_id.casefold()}-{opdb_family_id(group_id).rsplit('.', 1)[1]}.json"


def _normalize(value: str | None) -> str:
	text = (value or "").casefold().removeprefix("stub - ")
	return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _similarity(left: str | None, right: str | None) -> float:
	return SequenceMatcher(None, _normalize(left), _normalize(right)).ratio()


def _record_score(definition: dict[str, Any], record: dict[str, Any]) -> float:
	machine = definition["machine"]
	name_score = max(_similarity(machine["name"], record.get("name")), _similarity(machine["name"], record.get("commonName")))
	manufacturer = record.get("manufacturer") if isinstance(record.get("manufacturer"), dict) else {}
	manufacturer_score = max(_similarity(machine["manufacturer"], manufacturer.get("name")), _similarity(machine["manufacturer"], manufacturer.get("fullName")))
	score = 100 * name_score + 20 * manufacturer_score
	manufacture_date = record.get("manufactureDate")
	if isinstance(machine.get("year"), int) and isinstance(manufacture_date, str) and re.match(r"^\d{4}", manufacture_date):
		score += max(-30, 20 - 8 * abs(machine["year"] - int(manufacture_date[:4])))
	return score


def _choose_group(definition: dict[str, Any], mapped_records: list[dict[str, Any]], override_record: dict[str, Any] | None) -> str:
	if override_record is not None:
		return _group_id(override_record["opdbId"])
	group_ids = sorted({_group_id(record["opdbId"]) for record in mapped_records})
	if len(group_ids) == 1:
		return group_ids[0]
	if not group_ids:
		raise DefinitionError(f"{definition['machine']['id']}: no current OPDB records remain after stale-ID rewrites")
	ranked = sorted(
		((max(_record_score(definition, record) for record in mapped_records if _group_id(record["opdbId"]) == group_id), group_id) for group_id in group_ids),
		reverse=True,
	)
	if len(ranked) > 1 and ranked[0][0] - ranked[1][0] < 10:
		raise DefinitionError(f"{definition['machine']['id']}: ambiguous OPDB family candidates {group_ids}; add an explicit override")
	return ranked[0][1]


def _record_for_existing_ipdb(ipdb_id: int, group_id: str, by_ipdb: dict[int, list[dict[str, Any]]], mapped_ids: set[str]) -> dict[str, Any] | None:
	candidates = [record for record in by_ipdb.get(ipdb_id, []) if _group_id(record["opdbId"]) == group_id]
	if not candidates:
		return None
	return sorted(candidates, key=lambda record: (record["opdbId"] not in mapped_ids, record["opdbId"]))[0]


def _choose_record(
	definition: dict[str, Any],
	group_id: str,
	mapped_records: list[dict[str, Any]],
	override_record: dict[str, Any] | None,
	by_ipdb: dict[int, list[dict[str, Any]]],
) -> tuple[dict[str, Any], str]:
	if override_record is not None:
		return override_record, "override"
	mapped_in_group = [record for record in mapped_records if _group_id(record["opdbId"]) == group_id]
	mapped_ids = {record["opdbId"] for record in mapped_in_group}
	existing_ipdb = definition["machine"].get("ipdb_id")
	if isinstance(existing_ipdb, int):
		existing_record = _record_for_existing_ipdb(existing_ipdb, group_id, by_ipdb, mapped_ids)
		if existing_record is not None:
			return existing_record, "existing"
	with_ipdb = [record for record in mapped_in_group if isinstance(record.get("ipdbId"), int)]
	distinct_ipdb = {record["ipdbId"] for record in with_ipdb}
	if len(distinct_ipdb) == 1:
		return sorted(with_ipdb, key=lambda record: record["opdbId"])[0], "csv"
	if not with_ipdb:
		raise DefinitionError(f"{definition['machine']['id']}: mapped OPDB records have no IPDB number; add an alias override")
	ranked = sorted(((_record_score(definition, record), record) for record in with_ipdb), key=lambda item: (-item[0], item[1]["opdbId"]))
	if len(ranked) > 1 and ranked[0][0] - ranked[1][0] < 10:
		raise DefinitionError(f"{definition['machine']['id']}: ambiguous OPDB machine records; add an explicit override")
	return ranked[0][1], "csv"


def _definition_paths(repository_root: Path) -> list[Path]:
	return sorted((repository_root / "machines").glob("**/*.json"))


def _source_record(snapshot_sha256: str, acquired_at: str, group_id: str, member_ids: list[str]) -> dict[str, Any]:
	return {
		"acquired_at": acquired_at,
		"attribution": "Open Pinball Database contributors",
		"id": f"opdb.snapshot.{snapshot_sha256[:12]}",
		"kind": "human_review",
		"license": "NOASSERTION",
		"locator": f"machineGroups[{group_id}] and records {', '.join(member_ids)}",
		"revision": snapshot_sha256,
		"sha256": snapshot_sha256,
		"uri": OPDB_SNAPSHOT_URI,
	}


def _family_document(group: dict[str, Any], members: list[tuple[dict[str, Any], OpdbResolution]], snapshot_sha256: str, acquired_at: str) -> dict[str, Any]:
	group_id = group["opdbId"]
	manufacturers = {definition["machine"]["manufacturer"] for definition, _ in members}
	family: dict[str, Any] = {"id": opdb_family_id(group_id), "opdb_id": group_id, "title": group["name"]}
	if len(manufacturers) == 1:
		family["manufacturer"] = next(iter(manufacturers))
	member_records = []
	for definition, resolution in sorted(members, key=lambda item: item[0]["machine"]["id"]):
		machine_name = definition["machine"]["name"].removeprefix("STUB - ")
		member: dict[str, Any] = {"machine_id": resolution.machine_id}
		if _normalize(machine_name) != _normalize(group["name"]):
			member["edition"] = machine_name
		member_records.append(member)
	return {
		"family": family,
		"format": "pinmame-machine-family",
		"members": member_records,
		"schema_version": 1,
		"sources": [_source_record(snapshot_sha256, acquired_at, group_id, sorted({resolution.opdb_id for _, resolution in members}))],
	}


def _render_incoherences(incoherences: dict[str, Any]) -> str:
	lines = ["# OPDB mapping incoherences", "", "This report is generated from `machines/opdb_id.csv`, the pinned PinMAME catalog, the current machine definitions, and the retained OPDB snapshot identified in `reports/opdb-identity.json`.", ""]
	for title, key in (
		("CSV OPDB IDs absent from the snapshot", "csv_targets_missing_from_snapshot"),
		("CSV ROM sets absent from the PinMAME catalog", "csv_romsets_not_in_catalog"),
		("Catalog drivers without a CSV mapping", "catalog_drivers_without_csv_mapping"),
		("Machine definitions without a CSV mapping", "machine_definitions_without_csv_mapping"),
		("CSV OPDB records without an IPDB number", "csv_records_without_ipdb"),
		("Definitions mapped to multiple OPDB machine records", "definitions_with_multiple_csv_records"),
		("Definitions mapped across multiple OPDB families", "definitions_with_multiple_csv_families"),
		("CSV OPDB machine records split across definitions", "csv_records_split_across_definitions"),
		("Selected OPDB records that intentionally differ from the CSV machine record", "selected_record_differs_from_csv"),
		("Selected OPDB families that differ from the CSV family", "selected_family_differs_from_csv"),
	):
		values = incoherences[key]
		lines.extend([f"## {title}", "", f"Count: **{len(values)}**", ""])
		if not values:
			lines.extend(["- None.", ""])
		elif all(isinstance(value, str) for value in values):
			lines.extend([*(f"- `{value}`" for value in values), ""])
		else:
			for value in values:
				fields = "; ".join(f"{name}={','.join(item) if isinstance(item, list) else item}" for name, item in value.items())
				lines.append(f"- {fields}")
			lines.append("")
	return "\n".join(lines)


def _build_incoherences(
	rows: list[dict[str, str]],
	catalog_driver_ids: set[str],
	mapping: dict[str, str],
	stale_ids: dict[str, str],
	definition_rows: list[tuple[dict[str, Any], str, list[str], list[str]]],
	resolutions: list[OpdbResolution],
	record_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
	missing_targets: list[dict[str, Any]] = []
	for stale_id, replacement in sorted(stale_ids.items()):
		romsets = sorted(row["romset"] for row in rows if row["opdb_id"] == stale_id)
		if romsets:
			missing_targets.append({"csv_opdb_id": stale_id, "replacement_opdb_id": replacement, "romsets": romsets})
	multiple_records = []
	multiple_families = []
	record_machines: dict[str, set[str]] = defaultdict(set)
	for definition, _, _, normalized_ids in definition_rows:
		machine_id = definition["machine"]["id"]
		unique_ids = sorted(set(normalized_ids))
		for opdb_id in unique_ids:
			record_machines[opdb_id].add(machine_id)
		if len(unique_ids) > 1:
			multiple_records.append({"machine_id": machine_id, "opdb_ids": unique_ids})
		groups = sorted({_group_id(opdb_id) for opdb_id in unique_ids})
		if len(groups) > 1:
			multiple_families.append({"machine_id": machine_id, "family_opdb_ids": groups, "opdb_ids": unique_ids})
	resolution_by_machine = {resolution.machine_id: resolution for resolution in resolutions}
	selected_record_differs = []
	selected_family_differs = []
	for definition, _, _, normalized_ids in definition_rows:
		machine_id = definition["machine"]["id"]
		resolution = resolution_by_machine.get(machine_id)
		if resolution is None:
			continue
		mapped_ipdb_ids = sorted({record_by_id[opdb_id]["ipdbId"] for opdb_id in normalized_ids if isinstance(record_by_id[opdb_id].get("ipdbId"), int)})
		if resolution.opdb_id not in normalized_ids and resolution.ipdb_id not in mapped_ipdb_ids:
			selected_record_differs.append({"machine_id": machine_id, "csv_opdb_ids": sorted(set(normalized_ids)), "selected_opdb_id": resolution.opdb_id, "selected_ipdb_id": resolution.ipdb_id})
		csv_groups = sorted({_group_id(opdb_id) for opdb_id in normalized_ids})
		if resolution.family_opdb_id not in csv_groups:
			selected_family_differs.append({"machine_id": machine_id, "csv_family_opdb_ids": csv_groups, "selected_family_opdb_id": resolution.family_opdb_id})
	return {
		"catalog_drivers_without_csv_mapping": sorted(catalog_driver_ids - set(mapping)),
		"csv_records_split_across_definitions": [
			{"opdb_id": opdb_id, "machine_ids": sorted(machine_ids)}
			for opdb_id, machine_ids in sorted(record_machines.items())
			if len(machine_ids) > 1
		],
		"csv_romsets_not_in_catalog": [row for row in rows if row["romset"] not in catalog_driver_ids],
		"csv_records_without_ipdb": [
			{"opdb_id": opdb_id, "name": record_by_id[opdb_id].get("name") or ""}
			for opdb_id in sorted({stale_ids.get(row["opdb_id"], row["opdb_id"]) for row in rows})
			if not isinstance(record_by_id[opdb_id].get("ipdbId"), int)
		],
		"csv_targets_missing_from_snapshot": missing_targets,
		"definitions_with_multiple_csv_families": multiple_families,
		"definitions_with_multiple_csv_records": multiple_records,
		"selected_family_differs_from_csv": selected_family_differs,
		"selected_record_differs_from_csv": selected_record_differs,
	}


def build_opdb_import(repository_root: Path, snapshot_path: Path, acquired_at: str) -> tuple[dict[str, Any], dict[Path, Any], dict[Path, str]]:
	try:
		datetime.fromisoformat(acquired_at.replace("Z", "+00:00"))
	except ValueError as error:
		raise DefinitionError(f"Invalid OPDB acquisition timestamp: {acquired_at!r}") from error
	snapshot = load_json(snapshot_path)
	group_by_id, record_by_id, by_ipdb, _ = _snapshot_indexes(snapshot)
	overrides = load_json(repository_root / "config" / "opdb-overrides.json")
	if overrides.get("format") != "pinmame-opdb-overrides" or overrides.get("schema_version") != 1:
		raise DefinitionError("config/opdb-overrides.json has an unsupported format or schema version")
	if not isinstance(overrides.get("stale_opdb_ids"), dict) or not isinstance(overrides.get("machines"), dict):
		raise DefinitionError("config/opdb-overrides.json must contain stale_opdb_ids and machines objects")
	stale_ids = overrides["stale_opdb_ids"]
	machine_overrides = overrides["machines"]
	mapping_path = repository_root / "machines" / "opdb_id.csv"
	mapping, rows = _load_mapping(mapping_path)
	for stale_id, replacement in stale_ids.items():
		if stale_id in record_by_id:
			raise DefinitionError(f"Stale OPDB override {stale_id} is now present in the snapshot and must be reviewed")
		if replacement not in record_by_id:
			raise DefinitionError(f"Replacement OPDB ID {replacement} is absent from the snapshot")
	unknown_targets = sorted({opdb_id for opdb_id in mapping.values() if opdb_id not in record_by_id and opdb_id not in stale_ids})
	if unknown_targets:
		raise DefinitionError(f"CSV contains OPDB IDs absent from the snapshot: {unknown_targets}")
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	catalog_driver_ids = {record["id"] for record in catalog["drivers"]}
	definitions: list[tuple[dict[str, Any], str]] = []
	for path in _definition_paths(repository_root):
		definition = load_json(path)
		if definition.get("format") != "pinmame-machine-definition":
			continue
		definitions.append((definition, path.relative_to(repository_root).as_posix()))
	definition_rows: list[tuple[dict[str, Any], str, list[str], list[str]]] = []
	resolutions: list[OpdbResolution] = []
	definitions_by_machine: dict[str, dict[str, Any]] = {}
	json_outputs: dict[Path, Any] = {}
	stale_rewrite_machines: set[str] = set()
	for definition, relative_path in definitions:
		machine_id = definition["machine"]["id"]
		definitions_by_machine[machine_id] = definition
		driver_ids = [driver["id"] for driver in definition["drivers"]]
		raw_ids = [mapping[driver_id] for driver_id in driver_ids if driver_id in mapping]
		normalized_ids = [stale_ids.get(opdb_id, opdb_id) for opdb_id in raw_ids]
		if raw_ids:
			definition_rows.append((definition, relative_path, raw_ids, normalized_ids))
		if not normalized_ids:
			continue
		if raw_ids != normalized_ids:
			stale_rewrite_machines.add(machine_id)
		mapped_records = [record_by_id[opdb_id] for opdb_id in sorted(set(normalized_ids))]
		override = machine_overrides.get(machine_id)
		override_record = None
		if override is not None:
			override_record = record_by_id.get(override["opdb_id"])
			if override_record is None:
				raise DefinitionError(f"{machine_id}: override OPDB ID {override['opdb_id']} is absent from the snapshot")
		group_id = _choose_group(definition, mapped_records, override_record)
		if group_id not in group_by_id:
			raise DefinitionError(f"{machine_id}: OPDB family {group_id} is absent from machineGroups")
		selected, method = _choose_record(definition, group_id, mapped_records, override_record, by_ipdb)
		ipdb_id = selected.get("ipdbId")
		if not isinstance(ipdb_id, int):
			raise DefinitionError(f"{machine_id}: selected OPDB record {selected['opdbId']} has no IPDB number")
		mapped_ipdb_ids = {record.get("ipdbId") for record in mapped_records if isinstance(record.get("ipdbId"), int)}
		if override_record is not None:
			method = "override"
		elif machine_id in stale_rewrite_machines:
			method = "stale_id_rewrite"
		elif selected["opdbId"] in normalized_ids or ipdb_id in mapped_ipdb_ids:
			method = "csv"
		else:
			method = "existing"
		resolution = OpdbResolution(machine_id, relative_path, selected["opdbId"], group_id, ipdb_id, sum(driver_id in mapping for driver_id in driver_ids), tuple(sorted(set(normalized_ids))), method)
		resolutions.append(resolution)
		updated = dict(definition)
		updated["machine"] = dict(definition["machine"])
		updated["machine"]["ipdb_id"] = ipdb_id
		updated["machine"]["opdb_id"] = selected["opdbId"]
		json_outputs[repository_root / relative_path] = updated
	for machine_id in machine_overrides:
		if machine_id not in {resolution.machine_id for resolution in resolutions}:
			raise DefinitionError(f"Unused OPDB machine override: {machine_id}")
	resolution_by_machine = {resolution.machine_id: resolution for resolution in resolutions}
	for seed_path in sorted((repository_root / "tools" / "seeds").glob("**/*.json")):
		seed = load_json(seed_path)
		if seed.get("format") != "pinmame-machine-definition":
			continue
		resolution = resolution_by_machine.get(seed.get("machine", {}).get("id"))
		if resolution is None:
			continue
		updated_seed = dict(seed)
		updated_seed["machine"] = dict(seed["machine"])
		updated_seed["machine"]["ipdb_id"] = resolution.ipdb_id
		updated_seed["machine"]["opdb_id"] = resolution.opdb_id
		json_outputs[seed_path] = updated_seed
	family_members: dict[str, list[tuple[dict[str, Any], OpdbResolution]]] = defaultdict(list)
	for resolution in resolutions:
		family_members[resolution.family_opdb_id].append((definitions_by_machine[resolution.machine_id], resolution))
	casefold_groups: dict[str, list[str]] = defaultdict(list)
	for group_id in family_members:
		casefold_groups[group_id.casefold()].append(group_id)
	for group_id, members in sorted(family_members.items()):
		filename = _family_filename(group_id, casefold_groups[group_id.casefold()])
		json_outputs[repository_root / "families" / "opdb" / filename] = _family_document(group_by_id[group_id], members, file_sha256(snapshot_path), acquired_at)
	unmapped_machine_ids = sorted(set(definitions_by_machine) - set(resolution_by_machine))
	incoherences = _build_incoherences(rows, catalog_driver_ids, mapping, stale_ids, definition_rows, resolutions, record_by_id)
	incoherences["machine_definitions_without_csv_mapping"] = unmapped_machine_ids
	report = {
		"format": "pinmame-opdb-identity",
		"incoherences": incoherences,
		"machines": [
			{
				"definition": resolution.definition,
				"family_opdb_id": resolution.family_opdb_id,
				"ipdb_id": resolution.ipdb_id,
				"machine_id": resolution.machine_id,
				"mapped_driver_count": resolution.mapped_driver_count,
				"mapped_opdb_ids": list(resolution.mapped_opdb_ids),
				"opdb_id": resolution.opdb_id,
				"resolution": resolution.resolution,
			}
			for resolution in sorted(resolutions, key=lambda item: item.machine_id)
		],
		"mapping": {"path": "machines/opdb_id.csv", "row_count": len(rows), "sha256": file_sha256(mapping_path)},
		"schema_version": 1,
		"source": {"acquired_at": acquired_at, "sha256": file_sha256(snapshot_path), "uri": OPDB_SNAPSHOT_URI},
		"summary": {
			"catalog_driver_count": len(catalog_driver_ids),
			"csv_row_count": len(rows),
			"family_count": len(family_members),
			"mapped_catalog_driver_count": len(catalog_driver_ids & set(mapping)),
			"resolved_machine_count": len(resolutions),
			"unmapped_catalog_driver_count": len(catalog_driver_ids - set(mapping)),
			"unmapped_machine_count": len(unmapped_machine_ids),
		},
		"unmapped_machine_ids": unmapped_machine_ids,
	}
	json_outputs[repository_root / "reports" / "opdb-identity.json"] = report
	text_outputs = {repository_root / "reports" / "opdb-incoherences.md": _render_incoherences(incoherences)}
	return report, json_outputs, text_outputs


def import_opdb(repository_root: Path, snapshot_path: Path, acquired_at: str, check: bool = False) -> dict[str, Any]:
	report, json_outputs, text_outputs = build_opdb_import(repository_root, snapshot_path, acquired_at)
	family_root = repository_root / "families" / "opdb"
	expected_family_paths = {path.resolve() for path in json_outputs if path.parent == family_root}
	existing_family_paths = {path.resolve() for path in family_root.glob("*.json")} if family_root.is_dir() else set()
	unexpected_family_paths = sorted(existing_family_paths - expected_family_paths)
	if unexpected_family_paths:
		relative = [path.relative_to(repository_root).as_posix() for path in unexpected_family_paths]
		raise DefinitionError(f"Unexpected stale OPDB family files require review: {', '.join(relative[:20])}{' ...' if len(relative) > 20 else ''}")
	if check:
		drift = []
		for path, value in json_outputs.items():
			if not path.is_file() or path.read_bytes() != canonical_bytes(value):
				drift.append(path.relative_to(repository_root).as_posix())
		for path, value in text_outputs.items():
			if not path.is_file() or path.read_text(encoding="utf-8") != value:
				drift.append(path.relative_to(repository_root).as_posix())
		if drift:
			raise DefinitionError(f"OPDB-derived files are stale: {', '.join(sorted(drift)[:20])}{' ...' if len(drift) > 20 else ''}")
		return report
	for path, value in json_outputs.items():
		write_json(path, value)
	for path, value in text_outputs.items():
		write_text(path, value)
	return report


def load_opdb_machine_identity_index(repository_root: Path) -> dict[str, dict[str, Any]]:
	path = repository_root / "reports" / "opdb-identity.json"
	if not path.is_file():
		return {}
	report = load_json(path)
	if report.get("format") != "pinmame-opdb-identity":
		return {}
	return {
		record["machine_id"]: {"ipdb_id": record["ipdb_id"], "opdb_id": record["opdb_id"]}
		for record in report.get("machines", [])
		if isinstance(record, dict)
		and isinstance(record.get("machine_id"), str)
		and isinstance(record.get("ipdb_id"), int)
		and isinstance(record.get("opdb_id"), str)
	}
