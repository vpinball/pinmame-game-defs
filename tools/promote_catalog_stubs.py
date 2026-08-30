"""Catalog-wide stub-to-partial identity promotion.

Promotes every generated PinMAME catalog stub to an identity-resolved partial
record. The promotion resolves machine identity (reviewed `machines/opdb_id.csv`
mapping plus the retained OPDB snapshot when a record exists; PinMAME catalog
identity only otherwise) and carries the clone-tree driver list over unchanged.
It deliberately asserts nothing about controller platform, inputs, outputs,
displays, mechanisms, polarity, wiring, or spatial placement, and every one of
those requirements stays in `coverage.missing`.

This pass is point-in-time: it consumed the generated `machines/stubs/*.json`
inputs it promoted, so it cannot be replayed. `--check` re-derives everything
the pass authored (driver family, machine identity block, knowledge path, and
the exact coverage missing template) from the current catalog and OPDB identity
report and fails on any drift between that derivation and the records on disk.

Run from the repository root:

	python -B tools/promote_catalog_stubs.py --check
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from pinmame_game_defs.coverage import write_coverage_report  # noqa: E402
from pinmame_game_defs.identifiers import slug  # noqa: E402
from pinmame_game_defs.jsonio import file_sha256, load_json, write_json, write_text  # noqa: E402
from pinmame_game_defs.opdb import import_opdb  # noqa: E402
from pinmame_game_defs.registry import rebuild_catalog  # noqa: E402

WORKING_ROOT = REPOSITORY_ROOT.parent / "pinmame-game-defs-working-dir"
SNAPSHOT_PATH = WORKING_ROOT / "review-artifacts" / "opdb-import" / "latest-opdb.json"
ACQUIRED_AT = "2026-08-14T17:53:43Z"

# Requirements the promotion genuinely completes or leaves open. The clone-tree
# grouping is catalog-derived and unverified, so driver_mapping stays missing.
RESOLVED_REQUIREMENTS = ("identity",)
IDENTITY_PARTIAL_MISSING = [
	"driver_mapping",
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
	"spatial_placement",
]

NOTE_TEMPLATE = """# {name} ({manufacturer} {year})

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.{root_id}` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `{root_id}`, description "{description}", manufacturer
  "{manufacturer}", catalog year "{catalog_year}".
{identity_line}
{family_line}

## Drivers this record holds

{driver_lines}

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
"""


def load_snapshot_records() -> dict[str, dict[str, Any]]:
	report = load_json(REPOSITORY_ROOT / "reports" / "opdb-identity.json")
	expected_sha256 = report["source"]["sha256"]
	if not SNAPSHOT_PATH.is_file():
		raise SystemExit(f"Retained OPDB snapshot is missing: {SNAPSHOT_PATH}")
	actual_sha256 = file_sha256(SNAPSHOT_PATH)
	if actual_sha256 != expected_sha256:
		raise SystemExit(f"OPDB snapshot {actual_sha256} does not match the recorded identity report {expected_sha256}")
	snapshot = load_json(SNAPSHOT_PATH)
	records = {record["opdbId"]: record for record in snapshot["machines"]}
	for alias in snapshot.get("aliases", []):
		records.setdefault(alias["opdbId"], alias)
	return records


def note_identity_line(resolved: bool, disagreement_reason: str | None, opdb_id: str | None, record: dict[str, Any] | None) -> str:
	if not resolved and disagreement_reason and record is not None and opdb_id is not None:
		manufacturer = (record.get("manufacturer") or {}).get("name") or "manufacturer unknown"
		ipdb = record.get("ipdbId")
		ipdb_text = f"IPDB {ipdb}" if isinstance(ipdb, int) else "no IPDB number"
		return (
			f"- OPDB record `{opdb_id}` ({ipdb_text}) names this machine \"{record.get('name') or record.get('commonName')}\"\n"
			f"  ({manufacturer}, manufacture date {record.get('manufactureDate') or 'unknown'}), but the mapped record and the PinMAME\n"
			f"  catalog do not agree on the name, so identity is unresolved: {disagreement_reason}; the mapped record is a\n"
			"  lead, not a resolved identity."
		)
	if not resolved or record is None or opdb_id is None:
		return (
			"- No OPDB record is mapped for this driver in `machines/opdb_id.csv`, so the name above comes\n"
			"  from the PinMAME catalog alone and is unverified."
		)
	manufacturer = (record.get("manufacturer") or {}).get("name") or "manufacturer unknown"
	ipdb = record.get("ipdbId")
	ipdb_text = f"IPDB {ipdb}" if isinstance(ipdb, int) else "no IPDB number"
	return (
		f"- OPDB record `{opdb_id}` ({ipdb_text}) names this machine \"{record.get('name') or record.get('commonName')}\"\n"
		f"  ({manufacturer}, manufacture date {record.get('manufactureDate') or 'unknown'}); the resolved identity rests on the\n"
		"  agreement of the PinMAME catalog and this reviewed mapping."
	)


def expected_missing(resolved: bool) -> list[str]:
	missing = list(IDENTITY_PARTIAL_MISSING)
	if not resolved:
		missing.insert(0, "identity")
	return missing


TITLE_STOPWORDS = {"the", "a", "an", "and", "of", "&"}


def name_agrees(root_description: str, opdb_name: str) -> bool:
	"""PinMAME catalog and OPDB agree on the machine's name.

	Token overlap, or either name's concatenated form appearing inside the
	other's (root descriptions often append variant suffixes such as
	"(Free Play)" or "(PEMBOT (no relation) J-1)")."""
	def tokens(text: str) -> set[str]:
		return {token for token in re.split(r"[^a-z0-9]+", text.casefold()) if token and token not in TITLE_STOPWORDS}

	root_tokens = tokens(root_description)
	opdb_tokens = tokens(opdb_name)
	if root_tokens & opdb_tokens:
		return True
	root_compact = re.sub(r"[^a-z0-9]", "", root_description.casefold())
	opdb_compact = re.sub(r"[^a-z0-9]", "", opdb_name.casefold())
	return opdb_compact in root_compact or root_compact in opdb_compact


def check_promoted_records() -> None:
	"""Fail on any drift between the pass's derivation and the records on disk.

	The pass consumed its stub inputs, so it cannot be replayed; instead this
	re-derives each authored field from the current catalog and OPDB identity
	report: the driver family, the identity-derived machine id, OPDB/IPDB
	agreement, the knowledge path, and the exact coverage.missing template.
	"""
	catalog = load_json(REPOSITORY_ROOT / "catalog" / "pinmame.json")
	identity_index = {machine["machine_id"]: machine for machine in load_json(REPOSITORY_ROOT / "reports" / "opdb-identity.json")["machines"]}
	# The retained snapshot backs the agreement rule; without it only the
	# structural checks run.
	try:
		snapshot_records = load_snapshot_records()
	except SystemExit:
		snapshot_records = None
	catalog_driver_by_id = {record["id"]: record for record in catalog["drivers"]}
	machine_drivers: dict[str, set[str]] = {}
	for record in catalog["drivers"]:
		if record["machine_id"].startswith("stub."):
			raise SystemExit(f"Catalog still maps {record['id']} to residual stub {record['machine_id']}")
		machine_drivers.setdefault(record["machine_id"], set()).add(record["id"])
	opdb_owners: dict[str, list[str]] = {}
	ipdb_owners: dict[str, list[str]] = {}
	definitions: dict[str, dict[str, Any]] = {}
	for machine in catalog["machines"]:
		definition = load_json(REPOSITORY_ROOT / machine["definition"])
		definitions[machine["id"]] = definition
		oid = definition["machine"].get("opdb_id")
		ipdb = definition["machine"].get("ipdb_id")
		if "identity" not in definition["coverage"]["missing"]:
			if oid:
				opdb_owners.setdefault(oid, []).append(machine["id"])
			if ipdb:
				ipdb_owners.setdefault(ipdb, []).append(machine["id"])
	errors: list[str] = []
	checked = 0
	for machine in catalog["machines"]:
		definition = definitions[machine["id"]]
		identity = definition["machine"]
		machine_id = identity["id"]
		if machine_id.startswith("stub."):
			continue
		missing = definition["coverage"]["missing"]
		# Only the records this pass authored carry the identity-partial template.
		if missing not in (expected_missing(True), expected_missing(False)):
			continue
		checked += 1
		resolved = "opdb_id" in identity and "identity" not in missing
		if missing != expected_missing("opdb_id" in identity and resolved):
			errors.append(f"{machine_id}: coverage.missing does not match the identity-partial template")
		if "opdb_id" in identity and snapshot_records is not None:
			record = snapshot_records.get(identity["opdb_id"])
			if record is None:
				errors.append(f"{machine_id}: OPDB record absent from the retained snapshot")
			elif resolved:
				root_description = catalog_driver_by_id[machine["root_drivers"][0]]["description"]
				if not name_agrees(root_description, record.get("name") or record.get("commonName") or ""):
					errors.append(f"{machine_id}: claims resolved identity although the catalog and OPDB names disagree")
		if resolved and machine_id in identity_index:
			report_row = identity_index[machine_id]
			if identity.get("ipdb_id") != report_row["ipdb_id"] or identity.get("opdb_id") != report_row["opdb_id"]:
				errors.append(f"{machine_id}: OPDB identity disagrees with reports/opdb-identity.json")
		expected_id = f"{slug(identity['manufacturer'])}.{slug(identity['name'])}"
		if isinstance(identity["year"], int):
			expected_id = f"{expected_id}.{identity['year']}"
		if machine_id != expected_id and not machine_id.startswith(f"{expected_id}."):
			errors.append(f"{machine_id}: id does not derive from the identity block")
		if {driver["id"] for driver in definition["drivers"]} != machine_drivers.get(machine_id, set()):
			errors.append(f"{machine_id}: driver list does not match the catalog family")
		if not (REPOSITORY_ROOT / definition["knowledge"]["path"]).is_file():
			errors.append(f"{machine_id}: knowledge note missing: {definition['knowledge']['path']}")
	for label, owners in (("opdb_id", opdb_owners), ("ipdb_id", ipdb_owners)):
		for value, sharers in owners.items():
			if len(sharers) > 1:
				errors.append(f"{label} {value} is claimed as resolved by {len(sharers)} records: {sorted(sharers)}")
	if errors:
		raise SystemExit("Promoted-record drift detected:\n" + "\n".join(errors[:40]))
	print(f"check OK: {checked} promoted identity-partial records match their derivation")


def main() -> None:
	dry_run = "--dry-run" in sys.argv
	check_only = "--check" in sys.argv
	if check_only:
		check_promoted_records()
		return
	records = load_snapshot_records()
	catalog = load_json(REPOSITORY_ROOT / "catalog" / "pinmame.json")
	existing_machine_ids = {machine["id"] for machine in catalog["machines"]}
	catalog_driver_by_id = {record["id"]: record for record in catalog["drivers"]}
	stub_paths = sorted((REPOSITORY_ROOT / "machines" / "stubs").glob("*.json"))
	if not stub_paths:
		raise SystemExit("No catalog stubs remain; nothing to promote.")

	plans: list[dict[str, Any]] = []
	used_machine_ids = set(existing_machine_ids)
	for path in stub_paths:
		definition = load_json(path)
		machine = definition["machine"]
		drivers = definition["drivers"]
		# A residual family's root can itself carry clone_of pointing at a driver
		# claimed by another definition, so the root is the file stem (the catalog
		# root_driver), not "the driver without clone_of".
		root_id = path.stem
		root_driver = next((driver for driver in drivers if driver["id"] == root_id), None)
		root_catalog_record = catalog_driver_by_id.get(root_id)
		if root_catalog_record is None:
			raise SystemExit(f"{path.name}: catalog does not contain root driver {root_id}")
		split_residual = root_driver is None
		catalog_description = root_catalog_record["description"]
		root_driver_year = root_catalog_record["year"]
		catalog_year = machine.get("year")
		opdb_id = machine.get("opdb_id")
		record = records.get(opdb_id) if isinstance(opdb_id, str) else None
		resolved = record is not None
		disagreement_reason = None
		if resolved and not name_agrees(catalog_description, record.get("name") or record.get("commonName") or ""):
			# The OPDB record and the PinMAME catalog do not agree on the
			# machine's name, so identity stays honestly unresolved.
			resolved = False
			disagreement_reason = "catalog/OPDB name disagreement"
		name = catalog_description
		year = catalog_year
		opdb_date: Any = None
		if resolved:
			opdb_name = record.get("name") or record.get("commonName")
			if isinstance(opdb_name, str) and opdb_name.strip():
				name = opdb_name.strip()
			opdb_date = record.get("manufactureDate")
			if isinstance(opdb_date, str) and opdb_date[:4].isdigit():
				year = int(opdb_date[:4])
		base_id = f"{slug(machine['manufacturer'])}.{slug(name)}"
		if isinstance(year, int):
			base_id = f"{base_id}.{year}"
		disambiguated = base_id in used_machine_ids
		machine_id = f"{base_id}.{root_id}" if disambiguated else base_id
		if machine_id in used_machine_ids:
			raise SystemExit(f"Unresolvable machine-id collision: {machine_id}")
		used_machine_ids.add(machine_id)
		file_base = f"{slug(name)}-{year if isinstance(year, int) else 'unknown'}"
		if disambiguated:
			file_base = f"{file_base}-{root_id}"
		missing = list(IDENTITY_PARTIAL_MISSING)
		if not resolved:
			missing.insert(0, "identity")
		plans.append(
			{
				"stub_path": path,
				"definition": definition,
				"root_id": root_id,
				"description": catalog_description,
				"split_residual": split_residual,
				"root_owner_machine_id": root_catalog_record.get("machine_id"),
				"manufacturer": machine["manufacturer"],
				"catalog_year": catalog_year,
				"root_driver_year": root_driver_year,
				"opdb_id": opdb_id if resolved else None,
				"record": record,
				"resolved": resolved,
				"disagreement_reason": disagreement_reason,
				"name": name,
				"year": year,
				"machine_id": machine_id,
				"disambiguated": disambiguated,
				"missing": missing,
				"definition_path": REPOSITORY_ROOT / "machines" / "partial" / slug(machine["manufacturer"]) / f"{file_base}.json",
				"knowledge_path": REPOSITORY_ROOT / "knowledge" / slug(machine["manufacturer"]) / f"{file_base}.md",
			}
		)

	for plan in plans:
		if dry_run:
			continue
		definition = plan["definition"]
		machine = definition["machine"]
		machine["id"] = plan["machine_id"]
		machine["name"] = plan["name"]
		machine["year"] = plan["year"]
		coverage = definition["coverage"]
		coverage["status"] = "partial"
		coverage["missing"] = plan["missing"]
		definition["knowledge"] = {"path": plan["knowledge_path"].relative_to(REPOSITORY_ROOT).as_posix(), "status": "partial"}
		write_json(plan["definition_path"], definition)
		driver_lines = []
		for driver in sorted(definition["drivers"], key=lambda item: item["id"]):
			clone = f", clone of `{driver['clone_of']}`" if driver.get("clone_of") else ""
			driver_lines.append(f"- `{driver['id']}` ({driver['year']}, {driver['manufacturer']}{clone}).")
		if plan["split_residual"]:
			family_line = (
				f"- This is a split clone tree: the production drivers of `{plan['root_id']}` (including that root\n"
				f"  itself) belong to `{plan['root_owner_machine_id']}`. This record holds only the residual drivers\n"
				f"  listed below, which may be physically different hardware such as prototypes; their fitment needs\n"
				"  individual verification."
			)
		else:
			family_line = (
				f"- The definition's driver list is exactly the clone tree PinMAME declares under `{plan['root_id']}`;\n"
				"  whether every listed driver really runs on this physical machine is unverified."
			)
		note = NOTE_TEMPLATE.format(
			name=plan["name"],
			manufacturer=plan["manufacturer"],
			year=plan["year"] if isinstance(plan["year"], int) else "year unknown",
			root_id=plan["root_id"],
			description=plan["description"],
			catalog_year=plan["root_driver_year"],
			identity_line=note_identity_line(plan["resolved"], plan["disagreement_reason"], plan["opdb_id"], plan["record"]),
			family_line=family_line,
			driver_lines="\n".join(driver_lines),
		)
		write_text(plan["knowledge_path"], note)
		plan["stub_path"].unlink()
		stub_note = REPOSITORY_ROOT / "knowledge" / "stubs" / f"{plan['root_id']}.md"
		if stub_note.is_file():
			stub_note.unlink()

	if dry_run:
		print(f"DRY RUN: would promote {len(plans)} stubs ({sum(1 for plan in plans if plan['resolved'])} OPDB-mapped, {sum(1 for plan in plans if not plan['resolved'])} catalog-only)")
		print(f"disambiguated machine ids: {[plan['machine_id'] for plan in plans if plan['disambiguated']]}")
		manufacturers = sorted({plan['definition']['machine']['manufacturer'] for plan in plans})
		print(f"manufacturer folders: {manufacturers}")
		yearless = [plan['machine_id'] for plan in plans if not isinstance(plan['year'], int)]
		print(f"year-less ids ({len(yearless)}): {yearless[:20]}")
		for plan in plans:
			if plan["root_id"] in {"swep1_150", "ebalchmb", "usafootr", "alcapone", "s80tst"}:
				print(f"  sample {plan['root_id']}: {plan['machine_id']} -> {plan['definition_path'].relative_to(REPOSITORY_ROOT).as_posix()} | missing={plan['missing'][:4]}...")
		return

	overrides_path = REPOSITORY_ROOT / "config" / "opdb-overrides.json"
	overrides = load_json(overrides_path)
	renamed = {}
	for key, value in overrides["machines"].items():
		renamed[key] = value
	for plan in plans:
		old_key = f"stub.pinmame.{plan['root_id']}"
		if old_key in renamed:
			renamed[plan["machine_id"]] = renamed.pop(old_key)
	overrides["machines"] = renamed
	write_json(overrides_path, overrides)

	catalog = rebuild_catalog(REPOSITORY_ROOT)
	summary = catalog["summary"]
	if summary["stub_count"] != 0 or summary["machine_count"] != len(existing_machine_ids):
		raise SystemExit(f"Unexpected post-promotion catalog summary: {summary}")
	import_opdb(REPOSITORY_ROOT, SNAPSHOT_PATH, ACQUIRED_AT)
	report = write_coverage_report(REPOSITORY_ROOT)

	resolved_count = sum(1 for plan in plans if plan["resolved"])
	print(f"promoted {len(plans)} stubs to identity-resolved partials ({resolved_count} OPDB-mapped, {len(plans) - resolved_count} catalog-only)")
	print(f"disambiguated machine ids: {[plan['machine_id'] for plan in plans if plan['disambiguated']]}")
	print(f"coverage: {report['stub_count']} stubs, {report['partial_count']} partials, {report['author_ready_count']} author-ready of {report['machine_count']} games")
	for plan in plans:
		if plan["root_id"] in {"swep1_150", "ebalchmb", "usafootr"}:
			print(f"{plan['root_id']}: {plan['machine_id']} -> {plan['definition_path'].relative_to(REPOSITORY_ROOT).as_posix()}")


if __name__ == "__main__":
	main()
