"""Attach VPX-script-derived candidate I/O to partial definitions with no devices.

The two pinned VPX script corpora are the runbook's top evidence authority for
runtime I/O semantics. The deterministic script extraction already maps 975
scripts onto the catalog; this pass attaches, for partial definitions whose
input and output arrays are empty, the union of their scripts' candidate
switches, lamps, solenoids, and GI strings as candidate devices, each citing
the contributing script through a ``vpx_script`` source record with the
corpus's license/attribution. Script URIs deliberately avoid ``/blob/`` so the
pinned-script link table stays authoritative.

Guardrails (applied to every machine, with or without a declared platform):

- VBScript event-handler symbols (``*_KeyDown``, ``*_KeyUp``, ``*_Init``) are
  keyboard/form plumbing, not playfield devices, and are never attached.
- Public-address sanity bounds: switches 1-128, solenoids 1-128, lamps 1-128,
  GI 0-16. Script references outside these ranges are keyboard aliases,
  diagnostic keys, or extraction artifacts, not matrix devices.
- A script only contributes to a machine when its file path names the machine
  (every significant title token of the machine name, or the concatenated
  title, appears as a path token). Community re-themes reuse licensed-out
  ROMs, so ``cGameName`` alone cannot prove the script depicts the machine;
  non-matching scripts stay in the extraction report as leads instead of
  becoming device sources.

Machines that already hold devices from curated work or from the PinMAME
define attachment are skipped, and nothing is claimed: every enumeration
requirement stays in ``coverage.missing``. Machines with a controller platform
have their candidates filtered to the profile's declared groups and address
rules. ``--sanitize`` recomputes every machine this pass has attached with the
current rules; it is deterministic and safe to re-run.

Run from the repository root:

	python -B tools/attach_vpx_script_io.py --dry-run
	python -B tools/attach_vpx_script_io.py
	python -B tools/attach_vpx_script_io.py --sanitize
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
from pinmame_game_defs.registry import rebuild_catalog  # noqa: E402
from pinmame_game_defs.validation import _address_allowed  # noqa: E402

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
ADDRESS_BOUNDS = {
	"pinmame.input.switch": (1, 128),
	"pinmame.output.solenoid": (1, 128),
	"pinmame.output.lamp": (1, 128),
	"pinmame.output.gi": (0, 16),
}
# VBScript form/keyboard/timer event handlers, never playfield devices.
HANDLER_SYMBOL_PATTERN = re.compile(r"_(?:keydown|keyup|init|mousedown|mouseup|timer)$", re.IGNORECASE)
TITLE_STOPWORDS = {"the", "a", "an", "and", "of"}
YEAR_PATTERN = re.compile(r"\b(?:19|20)\d{2}\b")


def label_well_formed(label: str) -> bool:
	# Raw VBScript fragments (unbalanced parentheses, trailing commas, dotted
	# method calls, bare one-or-two-character object names) are not semantic
	# names a curator can use.
	if len(label) < 3:
		return False
	if label.count("(") != label.count(")"):
		return False
	if label.endswith(","):
		return False
	if re.search(r"\.[A-Za-z_]", label):
		return False
	return True
SAM_GAME_ON_BINDING = {"device": 33, "group": "pinmame.output.solenoid"}


def clean_label(label: str) -> str:
	text = label.strip()
	if text[:2] == "l ":
		text = text[2:]
	if text and text[0].islower():
		text = text[0].upper() + text[1:]
	return text


def candidate_allowed(candidate: dict[str, Any]) -> bool:
	if HANDLER_SYMBOL_PATTERN.search(candidate.get("symbol", "")):
		return False
	bounds = ADDRESS_BOUNDS.get(candidate["group"])
	if bounds is None:
		return False
	return bounds[0] <= candidate["address"] <= bounds[1]


def title_tokens(title: str) -> tuple[list[str], str]:
	tokens = [token for token in re.split(r"[^a-z0-9]+", title.casefold()) if token and token not in TITLE_STOPWORDS]
	return tokens, "".join(tokens)


def title_matches(machine_name: str, machine_year: int | None, script_path: str) -> bool:
	tokens, concatenated = title_tokens(machine_name)
	if not tokens:
		return False
	path_tokens = {token for token in re.split(r"[^a-z0-9]+", script_path.casefold()) if token}
	if not (set(tokens) <= path_tokens or concatenated in path_tokens):
		return False
	# A path that names a different model year ("Pinball Champ 82") does not
	# describe this machine when the machine's own year is known.
	path_years = set(YEAR_PATTERN.findall(script_path))
	if machine_year is not None and path_years and str(machine_year) not in path_years:
		return False
	return True


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


def script_source_record(entry: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
	return {
		"attribution": evidence["source"]["attribution"],
		"id": f"vpx-script.{Path(entry['evidence']).stem}",
		"kind": "vpx_script",
		"license": evidence["source"]["license"],
		"locator": f"{entry['corpus']}: {entry['source']}",
		"revision": entry["revision"],
		"sha256": evidence["source"]["sha256"],
		"uri": CORPUS_REPOSITORIES[entry["corpus"]],
	}


def attach_candidates(
	definition: dict[str, Any],
	entries: list[dict[str, Any]],
	profile_groups: dict[str, dict[str, Any]] | None,
	machine_name: str,
	machine_year: int | None,
	rejected_counter: list[int] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
	"""Return (contributing script source records, merged devices) for empty arrays."""
	occupied: set[str] = {device["id"] for device in definition["inputs"] + definition["outputs"]}
	bindings: set[tuple[str, int]] = {
		(device["binding"]["group"], device["binding"]["device"])
		for device in definition["inputs"] + definition["outputs"]
		if isinstance(device.get("binding"), dict)
	}
	source_ids = {source["id"] for source in definition["sources"]}
	merged: list[dict[str, Any]] = []
	contributing: dict[str, dict[str, Any]] = {}
	for entry in sorted(entries, key=lambda item: (item["corpus"], item["source"])):
		if not title_matches(machine_name, machine_year, entry["source"]):
			continue
		evidence = load_json(REPOSITORY_ROOT / entry["evidence"])
		source_id = f"vpx-script.{Path(entry['evidence']).stem}"
		contributed = False
		for candidate in [*evidence["switches"], *evidence["outputs"]]:
			group = candidate["group"]
			if group not in GROUP_KINDS or not candidate_allowed(candidate):
				continue
			if profile_groups is not None:
				group_def = profile_groups.get(group)
				if group_def is None or not _address_allowed(candidate["address"], group_def.get("address_rules", [])):
					continue
			key = (group, candidate["address"])
			if key in bindings:
				continue
			label = clean_label(candidate["label"])
			if not label or not label_well_formed(label):
				if rejected_counter is not None:
					rejected_counter[0] += 1
				continue
			device = candidate_device(candidate, source_id, occupied)
			if device is None:
				continue
			bindings.add(key)
			merged.append(device)
			contributed = True
		if contributed and source_id not in source_ids:
			contributing[source_id] = script_source_record(entry, evidence)
	return list(contributing.values()), merged


def knowledge_note_section(script_count: int, device_count: int) -> str:
	return (
		"## VPX script candidates (candidate)\n"
		"\n"
		f"- {script_count} retained community table script(s) declare this machine's driver; their "
		f"extracted switch/lamp/solenoid/GI candidates are carried as {device_count} candidate devices. "
		"When curator work weighs sources, a retained script outranks emulator-derived candidates for "
		"runtime semantics, but every device here is still a candidate until a known-working table is "
		"verified against this exact physical machine.\n"
	)


def update_knowledge_note(knowledge_path: Path, script_count: int, device_count: int) -> None:
	if not knowledge_path.is_file():
		return
	text = knowledge_path.read_text(encoding="utf-8")
	section = knowledge_note_section(script_count, device_count)
	marker = "## What a curator must establish next"
	existing_start = text.find("## VPX script candidates")
	if existing_start >= 0:
		existing_end = text.find("\n## ", existing_start + 1)
		# The block ends just before the next heading; keep the blank line that
		# separates sections so replacement does not glue headings together.
		existing_block = text[existing_start:] if existing_end < 0 else text[existing_start:existing_end + 1]
		if device_count:
			text = text.replace(existing_block, section + "\n", 1)
		else:
			text = text.replace(existing_block, "", 1)
	elif device_count:
		if marker not in text:
			return
		text = text.replace(marker, section + "\n" + marker, 1)
	if not text.endswith("\n"):
		text += "\n"
	write_text(knowledge_path, text)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--dry-run", action="store_true")
	parser.add_argument("--sanitize", action="store_true", help="Recompute every machine this pass has attached with the current rules.")
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
	rejected_counter = [0]
	for machine in catalog["machines"]:
		if machine["machine_kind"] in NON_GAME_KINDS or machine["coverage_status"] != "partial":
			continue
		definition_path = REPOSITORY_ROOT / machine["definition"]
		definition = load_json(definition_path)
		corpus_sources = [
			source
			for source in definition["sources"]
			if source.get("kind") == "vpx_script" and source.get("uri") in set(CORPUS_REPOSITORIES.values()) and len(source.get("sha256", "")) == 64
		]
		if args.sanitize:
			if not corpus_sources:
				continue
		elif definition["inputs"] or definition["outputs"] or not entries_by_machine.get(machine["id"]):
			continue
		if args.sanitize and not entries_by_machine.get(machine["id"]):
			# Nothing left to recompute from; drop this pass's devices and citations.
			definition["inputs"] = []
			definition["outputs"] = []
			definition["sources"] = [source for source in definition["sources"] if source not in corpus_sources]
			if not args.dry_run:
				update_knowledge_note(REPOSITORY_ROOT / definition["knowledge"]["path"], 0, 0)
				write_json(definition_path, definition)
			touched += 1
			continue

		platform = definition.get("controller", {}).get("platform")
		profile = profiles.get(platform) if platform else None
		profile_groups = {group["id"]: group for group in profile["groups"]} if profile else None

		synthetic = None
		if args.sanitize:
			# Clear only the devices this pass contributed (provenance entirely
			# citing this pass's vpx-script.* ids); curated devices that merely
			# cite a corpus script survive untouched.
			pass_source_ids = {source["id"] for source in corpus_sources}

			def from_this_pass(device: dict[str, Any]) -> bool:
				refs = device.get("provenance", {}).get("source_refs", [])
				return bool(refs) and all(ref in pass_source_ids for ref in refs)

			synthetic = next((device for device in definition["outputs"] if device.get("binding") == SAM_GAME_ON_BINDING and device.get("kind") == "virtual"), None)
			definition["inputs"] = [device for device in definition["inputs"] if not from_this_pass(device)]
			definition["outputs"] = [device for device in definition["outputs"] if not from_this_pass(device)]
			definition["sources"] = [source for source in definition["sources"] if source not in corpus_sources]

		machine_year = definition["machine"].get("year")
		contributing, merged = attach_candidates(definition, entries_by_machine.get(machine["id"], []), profile_groups, definition["machine"]["name"], machine_year, rejected_counter)
		if merged:
			for source in contributing:
				definition["sources"].append(source)
			definition["inputs"].extend(device for device in merged if device["binding"]["group"] == "pinmame.input.switch")
			definition["outputs"].extend(device for device in merged if device["binding"]["group"] != "pinmame.input.switch")
		if synthetic is not None:
			definition["outputs"].append(synthetic)
		if not merged and args.sanitize:
			if not args.dry_run:
				update_knowledge_note(REPOSITORY_ROOT / definition["knowledge"]["path"], 0, 0)
		elif merged:
			if not args.dry_run:
				update_knowledge_note(REPOSITORY_ROOT / definition["knowledge"]["path"], len(contributing), len(merged))
		if not merged and not args.sanitize:
			continue
		touched += 1
		if merged:
			device_machines += 1
			device_total += len(merged)
			script_total += len(contributing)
		if not args.dry_run:
			write_json(definition_path, definition)

	print(f"{'DRY RUN: ' if args.dry_run else ''}{'sanitized' if args.sanitize else 'attached'}: {touched} definitions touched, {device_machines} machines with devices, {device_total} devices from {script_total} scripts")
	print(f"candidate labels rejected as ill-formed: {rejected_counter[0]}")
	if args.dry_run:
		return
	rebuild_catalog(REPOSITORY_ROOT)
	report = write_coverage_report(REPOSITORY_ROOT)
	print(f"coverage: {report['stub_count']} stubs, {report['partial_count']} partials, {report['author_ready_count']} author-ready")


if __name__ == "__main__":
	main()
