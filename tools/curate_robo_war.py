"""Reproduce the reviewed Robo-War definition, its knowledge note and its spatial audit.

The seed is reviewed factual data with every placement at its table status; this curator applies
the factory location-drawing callout check (tools/seeds/gottlieb/robo-war-1988-callouts.json),
which validates the placements whose own callout agrees. External sources are optional for
ordinary regeneration; when configured, they must match their pinned hashes and complete
extraction manifest before any write.

Usage::

	python tools/curate_robo_war.py --check        # fail if the committed artifacts drift
	python tools/curate_robo_war.py --regenerate   # rewrite them from the seeds
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.validation import validate_against_schema, validate_machine

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import drawing_callouts  # noqa: E402
from build_external_evidence_manifest import check_manifest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.robo-war.1988"
GAME = "robowars"
SEED = ROOT / "tools/seeds/gottlieb/robo-war-1988.json"
NOTE_SEED = ROOT / "tools/seeds/gottlieb/robo-war-1988.md"
AUDIT_SEED = ROOT / "tools/seeds/gottlieb/robo-war-1988-spatial.json"
CALLOUT_SEED = ROOT / "tools/seeds/gottlieb/robo-war-1988-callouts.json"
CALLOUTS = "review.robo-war-drawing-callouts-2026-11-13"
PARTIAL = ROOT / "machines/partial/gottlieb/robo-war-1988.json"
READY = ROOT / "machines/author-ready/gottlieb/robo-war-1988.json"
NOTE = ROOT / "knowledge/gottlieb/robo-war-1988.md"
AUDIT = ROOT / "reports/spatial/gottlieb/robo-war-1988.json"
AUDIT_MD = ROOT / "reports/spatial/gottlieb/robo-war-1988.md"
EXPECTED = {
	"pinmame.input.switch": set(range(-8, 0)) | {10 * s + r for s in range(8) for r in range(8)} | set(range(111, 119)),
	"pinmame.input.dip": set(range(1, 43)),
	"pinmame.output.solenoid": set(range(1, 12)) | set(range(45, 49)),
	"pinmame.output.lamp": set(range(64)),
	"pinmame.output.gi": {0},
}
KINDS = {"SW": "switch", "L": "lamp", "SOL": "solenoid"}


def digest(path: Path) -> str:
	with path.open("rb") as stream:
		return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_excerpts(definition: dict) -> None:
	for source in definition["sources"]:
		for excerpt in source.get("excerpts", []):
			for key, hash_key in (("path", "sha256"), ("image", "image_sha256")):
				if key not in excerpt:
					continue
				path = ROOT / excerpt[key]
				if not path.is_file() or digest(path) != excerpt[hash_key]:
					raise ValueError(f"Missing or changed excerpt: {path}")
				if key == "path" and b"tokens truncated" in path.read_bytes():
					raise ValueError(f"Truncated source excerpt: {path}")


def verify_external(audit: dict) -> None:
	for artifact in audit["retained_artifacts"]:
		root = os.environ.get(artifact["environment"])
		if not root:
			continue
		path = Path(root) / artifact["relative_path"]
		if artifact.get("directory_manifest"):
			actual = check_manifest(path, GAME)
		else:
			if not path.is_file():
				raise ValueError(f"Missing retained artifact: {path}")
			actual = digest(path)
		if actual != artifact["sha256"]:
			raise ValueError(f"Changed retained artifact: {path}")


def verify_callouts() -> None:
	manuals, reviews = os.environ.get("PINMAME_MANUALS_ROOT"), os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	drawing_callouts.verify_retained(load_json(CALLOUT_SEED), ROOT, Path(manuals) if manuals else None, Path(reviews) if reviews else None)


def build() -> dict:
	definition = load_json(SEED)
	if definition["machine"]["id"] != MACHINE_ID:
		raise ValueError("Wrong machine seed")
	if definition["coverage"]["status"] != "partial" or not definition["coverage"]["missing"]:
		raise ValueError("This partial curator cannot authorize promotion")
	verify_excerpts(definition)
	sources = {source["id"]: source for source in definition["sources"]}
	if sources.get(CALLOUTS, {}).get("sha256") != digest(CALLOUT_SEED):
		raise ValueError("The drawing callout source record does not pin the committed callout seed")
	for group, addresses in EXPECTED.items():
		actual = {d["binding"]["device"] for d in definition["inputs"] + definition["outputs"] if d["binding"]["group"] == group}
		if actual != addresses:
			raise ValueError(f"Incomplete controller address inventory: {group}")
	drawing_callouts.apply_to_definition(definition, load_json(CALLOUT_SEED), CALLOUTS)
	errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", str(SEED)) + validate_machine(definition, ROOT)
	if errors:
		raise ValueError("Invalid reviewed seed: " + "; ".join(errors))
	return definition


def callout_check(definition: dict) -> dict:
	seed = load_json(CALLOUT_SEED)
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	return drawing_callouts.summary(seed, decisions, CALLOUT_SEED.relative_to(ROOT).as_posix(), digest(CALLOUT_SEED))


def callout_sentence(check: dict) -> str:
	rest: dict[str, set[int]] = {}
	for item in check["not_validated"].values():
		prefix = item["label"].rstrip("0123456789")
		rest.setdefault(KINDS[prefix], set()).add(int(item["label"][len(prefix):]))
	parts = [f"{kind}{'' if len(numbers) == 1 else 'es' if kind == 'switch' else 's'} {', '.join(str(n) for n in sorted(numbers))}" for kind, numbers in sorted(rest.items())]
	left = f" The checked placements that stay observed, each with a note on its device: {'; '.join(parts)}." if parts else ""
	return (f"A factory location-drawing callout check validates {check['validated']} of the {check['checked']} table placements it covers: "
	        "every callout on the folio 48 playboard drawing was read independently, the page was fitted against its three pop-bumper caps "
	        "and two flipper pivots and against its other callouts, and a placement validates when its own callout lands within 0.07 "
	        f"normalized under both fits (`{check['seed']}`).{left}")


def audit(definition: dict) -> dict:
	seed = load_json(AUDIT_SEED)
	if seed.get("machine_id") != MACHINE_ID or seed.get("format") != "pinmame-spatial-blockers":
		raise ValueError("Wrong spatial evidence seed")
	groups = ("inputs", "outputs", "displays")
	placements = [p for group in groups for device in definition[group] for p in (device.get("spatial") or {}).get("placements", [])]
	return {
		**seed,
		"drawing_callout_check": callout_check(definition),
		"located_observations": len(placements),
		"missing_spatial_ids": [d["id"] for group in groups for d in definition[group] if d.get("availability", "used") in {"used", "optional"} and "spatial" not in d],
		"source_seed_sha256": digest(AUDIT_SEED),
		"validated_placements": sum(p["provenance"]["status"] == "validated" for p in placements),
	}


def audit_markdown(record: dict) -> bytes:
	check = record["drawing_callout_check"]
	rows = ["# Robo-War spatial evidence", "", "Coverage: **partial**. " + record["promotion_decision"], "", record["coordinate_convention"], "",
	        f"{record['located_observations']} placements; {record['validated_placements']} validated by the folio 48 callout check "
	        f"({check['validated']} of {check['checked']} checked), the rest observed.", "", "## Remaining requirements", ""]
	rows.extend("- " + item for item in record["blockers"])
	rows.extend(["", "## Evidence and transformation", "", record["method"], ""])
	rows.extend("- " + item for item in record["projections"])
	rows.extend(["", "All raw coordinates and exact object bindings are retained in the machine's spatial-mapping excerpt. Coordinates are rounded once to six decimals. No render helper is counted as a physical socket.", ""])
	return "\n".join(rows).encode("utf-8")


def artifacts() -> dict[Path, bytes]:
	definition = build()
	record = audit(definition)
	verify_external(record)
	verify_callouts()
	note = NOTE_SEED.read_text(encoding="utf-8")
	if "{CALLOUT_CHECK}" not in note:
		raise ValueError("The knowledge note seed has no callout check placeholder")
	return {
		PARTIAL: canonical_bytes(definition),
		NOTE: note.replace("{CALLOUT_CHECK}", callout_sentence(record["drawing_callout_check"])).encode("utf-8"),
		AUDIT: canonical_bytes(record),
		AUDIT_MD: audit_markdown(record),
	}


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	if args.check == args.regenerate:
		parser.error("choose --check or --regenerate")
	if READY.exists():
		raise ValueError("Refusing to overwrite an existing author-ready artifact")
	for path, data in artifacts().items():
		if args.check:
			if not path.is_file() or path.read_bytes() != data:
				raise ValueError(f"Curator drift: {path}")
		else:
			write_bytes(path, data)
	print("Robo-War: checked" if args.check else "Robo-War: regenerated")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
