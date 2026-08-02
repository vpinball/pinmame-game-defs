from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .jsonio import load_json, write_json, write_text


NON_GAME_KINDS = {"diagnostic_software", "system_software"}


def build_coverage_report(repository_root: Path) -> dict[str, Any]:
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	all_records = catalog["machines"]
	machines = [machine for machine in all_records if machine.get("machine_kind", "unknown") not in NON_GAME_KINDS]
	drivers = catalog["drivers"]
	status_counts = Counter(machine["coverage_status"] for machine in machines)
	missing_counts: Counter[str] = Counter()
	for machine in machines:
		missing_counts.update(machine.get("missing", []))
	author_ready = status_counts["author_ready"]
	machine_count = len(machines)
	return {
		"format": "pinmame-machine-coverage",
		"version": 1,
		"pinmame_revision": catalog["source"]["pinmame_revision"],
		"driver_count": len(drivers),
		"catalog_record_count": len(all_records),
		"non_game_record_count": len(all_records) - machine_count,
		"machine_count": machine_count,
		"stub_count": status_counts["stub"],
		"partial_count": status_counts["partial"],
		"author_ready_count": author_ready,
		"author_ready_percent": round((author_ready / machine_count) * 100, 4) if machine_count else 0.0,
		"missing_requirement_counts": dict(sorted(missing_counts.items())),
		"completion_gate": author_ready == machine_count and machine_count > 0,
	}


def build_curation_queue(repository_root: Path) -> dict[str, Any]:
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	entries: list[dict[str, Any]] = []
	for machine in sorted(catalog["machines"], key=lambda record: record["processing_order"]):
		if machine.get("machine_kind", "unknown") in NON_GAME_KINDS:
			continue
		definition = load_json(repository_root / machine["definition"])
		identity = definition["machine"]
		entries.append(
			{
				"order": machine["processing_order"],
				"machine_id": machine["id"],
				"name": identity["name"],
				"manufacturer": identity["manufacturer"],
				"year": machine["processing_year"],
				"machine_kind": machine.get("machine_kind", "unknown"),
				"root_drivers": machine["root_drivers"],
				"coverage_status": machine["coverage_status"],
				"definition": machine["definition"],
			}
		)
	return {
		"format": "pinmame-machine-curation-queue",
		"version": 1,
		"ordering": "year_desc_manufacturer_title; unknown_year_last; related_driver_variants_together",
		"pinmame_revision": catalog["source"]["pinmame_revision"],
		"entries": entries,
	}


def write_coverage_report(repository_root: Path) -> dict[str, Any]:
	report = build_coverage_report(repository_root)
	write_json(repository_root / "reports" / "coverage.json", report)
	markdown = f"""# Machine-definition coverage

PinMAME revision: `{report['pinmame_revision']}`

Author-ready coverage: **{report['author_ready_count']} / {report['machine_count']} physical-machine records ({report['author_ready_percent']:.4f}%)**

- Supported drivers: {report['driver_count']}
- Catalog records: {report['catalog_record_count']} ({report['non_game_record_count']} diagnostic/system-software records excluded from game coverage)
- Explicit stubs: {report['stub_count']}
- Partial definitions: {report['partial_count']}
- Author-ready definitions: {report['author_ready_count']}
- Completion gate: {'PASS' if report['completion_gate'] else 'FAIL'}

Stubs and partial definitions are not usable completion credit. A clone driver contributes coverage only through its fully resolved physical-machine definition.
"""
	write_text(repository_root / "reports" / "coverage.md", markdown)
	queue = build_curation_queue(repository_root)
	write_json(repository_root / "reports" / "curation-queue.json", queue)
	rows = ["# Curation queue", "", "Physical machines are processed newest-to-oldest. Unknown-year candidates are last, and related driver variants stay together.", "", "| Order | Year | Machine | Manufacturer | Status |", "| ---: | ---: | --- | --- | --- |"]
	for entry in queue["entries"]:
		year = str(entry["year"]) if entry["year"] is not None else "unknown"
		rows.append(f"| {entry['order']} | {year} | {entry['name']} | {entry['manufacturer']} | {entry['coverage_status']} |")
	write_text(repository_root / "reports" / "curation-queue.md", "\n".join(rows) + "\n")
	return report
