"""Attach VPX-script-derived candidate I/O to partial definitions with no devices.

The two pinned VPX script corpora are the runbook's top evidence authority for
runtime I/O semantics. The deterministic script extraction already maps 975
scripts onto the catalog; this pass attaches, for partial definitions whose
input and output arrays are empty, the union of their scripts' candidate
switches, lamps, solenoids, and GI strings as candidate devices, each citing
the contributing script through a ``vpx_script`` source record with the
corpus's license/attribution. Script URIs deliberately avoid ``/blob/`` so the
pinned-script link table stays authoritative.

Machines that already hold devices (PinMAME define candidates or curated work)
are skipped, and nothing is claimed: every enumeration requirement stays in
``coverage.missing``. Machines with a controller platform have their candidates
filtered to the profile's declared groups and address rules.

Run from the repository root:

	python -B tools/attach_vpx_script_io.py --dry-run
	python -B tools/attach_vpx_script_io.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from pinmame_game_defs.coverage import write_coverage_report  # noqa: E402
from pinmame_game_defs.identifiers import slug  # noqa: E402
from pinmame_game_defs.jsonio import load_json, write_json, write_text  # noqa: E402
from pinmame_game_defs.validation import _address_allowed  # noqa: E402
from pinmame_game_defs.registry import rebuild_catalog  # noqa: E402

NON_GAME_KINDS = {"diagnostic_software", "system_software"}
CORPUS_REPOSITORIES = {
	"vpxtable-scripts": "https://github.com/sverrewl/vpxtable_scripts",
	"vpx-standalone-scripts": "https://github.com/jsm174/vpx-standalone-scripts",
}
GROUP_KINDS = {
	"pinmame.input.switch": ("switch", "switch", "pinmame.switch"),
	"pinmame.output.solenoid": ("coil", "coil", "pinmame.solenoid"),
	"pinmame.output.lamp": ("lamp", "lamp", "pinmame.lamp"),
	"pinmame.output.gi": ("gi", "gi", "pinmame.gi"),
}


def clean_label(label: str) -> str:
	text = label.strip()
	if text[:2] == "l ":
		text = text[2:]
	if text and text[0].islower():
		text = text[0].upper() + text[1:]
	return text


def candidate_device(candidate: dict[str, Any], source_id: str, occupied: set[str]) -> dict[str, Any] | None:
	group = candidate["group"]
	if group not in GROUP_KINDS:
		return None
	kind, id_prefix, namespace = GROUP_KINDS[group]
	label = clean_label(candidate["label"])
	if not label:
		return None
	id_base = re.sub(r"-{2,}", "-", slug(label))
	base_id = f"{id_prefix}.{id_base}"
	suffix = f"-{candidate['address']}" if candidate["address"] >= 0 else f"-m{abs(candidate['address'])}"
	device_id = base_id
	if device_id in occupied:
		device_id = f"{base_id}{suffix}"
	index = 2
	while device_id in occupied:
		device_id = f"{base_id}{suffix}-{index}"
		index += 1
	occupied.add(device_id)
	return {
		"aliases": [{"namespace": namespace, "value": str(candidate["address"])}],
		"binding": {"device": candidate["address"], "group": group},
		"id": device_id,
		"kind": kind,
		"label": label,
		"provenance": {"source_refs": [source_id], "status": "candidate"},
	}


def script_source_record(entry: dict[str, Any], evidence: dict[str, Any], corpus_repository: str) -> dict[str, Any]:
	return {
		"attribution": evidence["source"]["attribution"],
		"id": f"vpx-script.{Path(entry['evidence']).stem}",
		"kind": "vpx_script",
		"license": evidence["source"]["license"],
		"locator": f"{entry['corpus']}: {entry['source']}",
		"revision": entry["revision"],
		"sha256": evidence["source"]["sha256"],
		"uri": corpus_repository,
	}


def knowledge_note_text(text: str, script_count: int, device_count: int) -> str | None:
	marker = "## What a curator must establish next"
	if marker not in text or "## VPX script candidates" in text:
		return None
	lines = [
		"## VPX script candidates (candidate)",
		"",
		f"- {script_count} retained community table script(s) declare this machine's driver; their "
		f"extracted switch/lamp/solenoid/GI candidates are carried as {device_count} candidate devices. "
		"When curator work weighs sources, a retained script outranks emulator-derived candidates for "
		"runtime semantics, but every device here is still a candidate until a known-working table is "
		"verified against this exact physical machine.",
	]
	return text.replace(marker, "\n".join(lines) + "\n\n" + marker, 1)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--dry-run", action="store_true")
	args = parser.parse_args()

	catalog = load_json(REPOSITORY_ROOT / "catalog" / "pinmame.json")
	report = load_json(REPOSITORY_ROOT / "reports" / "vpx-script-extraction.json")
	profiles = {profile["id"]: profile for profile in (load_json(path) for path in sorted((REPOSITORY_ROOT / "controllers" / "pinmame").glob("*.json")))}
	stale = [entry for entry in report["entries"] if any(machine_id.startswith("stub.") for machine_id in entry["machine_ids"])]
	if stale:
		raise SystemExit(f"{len(stale)} extraction entries still reference stub machine IDs; regenerate the VPX extraction first.")

	entries_by_machine: dict[str, list[dict[str, Any]]] = {}
	for entry in report["entries"]:
		if len(entry["machine_ids"]) == 1:
			entries_by_machine.setdefault(entry["machine_ids"][0], []).append(entry)

	touched = 0
	device_machines = 0
	device_total = 0
	script_total = 0
	for machine in catalog["machines"]:
		if machine["machine_kind"] in NON_GAME_KINDS or machine["coverage_status"] != "partial":
			continue
		entries = entries_by_machine.get(machine["id"])
		if not entries:
			continue
		definition_path = REPOSITORY_ROOT / machine["definition"]
		definition = load_json(definition_path)
		if definition["inputs"] or definition["outputs"]:
			continue
		profile = None
		platform = definition.get("controller", {}).get("platform")
		if platform:
			profile = profiles.get(platform)
		profile_groups = {group["id"]: group for group in profile["groups"]} if profile else None

		occupied: set[str] = set()
		bindings: set[tuple[str, int]] = set()
		source_ids = {source["id"] for source in definition["sources"]}
		merged: list[dict[str, Any]] = []
		contributing: dict[str, dict[str, Any]] = {}
		for entry in sorted(entries, key=lambda item: (item["corpus"], item["source"])):
			evidence = load_json(REPOSITORY_ROOT / entry["evidence"])
			source_id = f"vpx-script.{Path(entry['evidence']).stem}"
			candidates = [*evidence["switches"], *evidence["outputs"]]
			contributed = False
			for candidate in candidates:
				group = candidate["group"]
				if group not in GROUP_KINDS:
					continue
				if profile_groups is not None:
					group_def = profile_groups.get(group)
					if group_def is None:
						continue
					if not _address_allowed(candidate["address"], group_def.get("address_rules", [])):
						continue
				key = (group, candidate["address"])
				if key in bindings:
					continue
				device = candidate_device(candidate, source_id, occupied)
				if device is None:
					continue
				bindings.add(key)
				merged.append(device)
				contributed = True
			if contributed and source_id not in source_ids:
				contributing[source_id] = script_source_record(entry, evidence, CORPUS_REPOSITORIES[entry["corpus"]])
		if not merged:
			continue

		for source in contributing.values():
			definition["sources"].append(source)
		definition["inputs"].extend(device for device in merged if device["binding"]["group"] == "pinmame.input.switch")
		definition["outputs"].extend(device for device in merged if device["binding"]["group"] != "pinmame.input.switch")
		touched += 1
		device_machines += 1
		device_total += len(merged)
		script_total += len(contributing)
		if not args.dry_run:
			write_json(definition_path, definition)
			knowledge_path = REPOSITORY_ROOT / definition["knowledge"]["path"]
			if knowledge_path.is_file():
				updated = knowledge_note_text(knowledge_path.read_text(encoding="utf-8"), len(contributing), len(merged))
				if updated is not None:
					write_text(knowledge_path, updated)

	print(f"{'DRY RUN: ' if args.dry_run else ''}would update {touched} definitions with candidate devices")
	print(f"machines receiving devices: {device_machines} ({device_total} devices from {script_total} scripts)")
	if args.dry_run:
		return
	rebuild_catalog(REPOSITORY_ROOT)
	report = write_coverage_report(REPOSITORY_ROOT)
	print(f"coverage: {report['stub_count']} stubs, {report['partial_count']} partials, {report['author_ready_count']} author-ready")


if __name__ == "__main__":
	main()
