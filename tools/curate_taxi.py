"""Materialize the seed-owned Williams Taxi (1988) definition deterministically.

The complete canonical machine JSON and literal recreation knowledge are curator-owned inputs:
this tool never reconstructs source facts, updates a catalog, or writes coverage reports.  It only
checks and materializes the Taxi paths derived from those inputs.  ``--check`` is the default and
fails closed on malformed or non-canonical inputs, stale artifacts, repository-excerpt drift, and
an opposing-status definition.  ``--verify-retained`` separately verifies the external evidence
binding register against caller-provided read-only roots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from pinmame_game_defs.jsonio import canonical_bytes, write_json, write_text
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine
from build_external_evidence_manifest import check_manifest


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "williams.taxi.1988"
SEED_RELATIVE_PATH = Path("tools/seeds/williams/taxi-1988.json")
KNOWLEDGE_SEED_RELATIVE_PATH = Path("tools/seeds/williams/taxi-1988.md")
EVIDENCE_BINDING_RELATIVE_PATH = Path("tools/seeds/williams/taxi-1988-evidence.json")
KNOWLEDGE_RELATIVE_PATH = Path("knowledge/williams/taxi-1988.md")
SPATIAL_REPORT_RELATIVE_PATH = Path("reports/spatial/williams/taxi-1988.json")
SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH = Path("reports/spatial/williams/taxi-1988.md")
PARTIAL_RELATIVE_PATH = Path("machines/partial/williams/taxi-1988.json")
AUTHOR_READY_RELATIVE_PATH = Path("machines/author-ready/williams/taxi-1988.json")

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"

DRIVER_IDS = frozenset({"taxi_l4", "taxi_l5c", "taxi_l5cm", "taxi_l3", "taxi_lu1", "taxi_lg1", "taxi_p5"})
EXPECTED_SWITCH_BINDINGS = frozenset(range(-7, -3)) | frozenset(range(1, 65)) | frozenset(range(81, 89))
EXPECTED_SOLENOID_BINDINGS = frozenset(range(1, 51))
EXPECTED_LAMP_BINDINGS = frozenset(range(1, 65))
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def _path(root: Path, relative_path: Path) -> Path:
	return root / relative_path


def _read_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
	if not path.is_file():
		raise RuntimeError(f"Taxi {label} is missing: {path}")
	try:
		raw = path.read_bytes()
		value = json.loads(raw.decode("utf-8"))
	except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
		raise RuntimeError(f"Taxi {label} is malformed: {path}: {error}") from error
	if not isinstance(value, dict):
		raise RuntimeError(f"Taxi {label} must be a JSON object: {path}")
	return value, raw


def _canonical_json(path: Path, label: str) -> dict[str, Any]:
	value, raw = _read_json(path, label)
	if raw != canonical_bytes(value):
		raise RuntimeError(f"Taxi {label} is not canonical UTF-8 JSON: {path}")
	return value


def _seed_path(root: Path) -> Path:
	return _path(root, SEED_RELATIVE_PATH)


def _knowledge_seed_path(root: Path) -> Path:
	return _path(root, KNOWLEDGE_SEED_RELATIVE_PATH)


def _definition_paths(definition: Mapping[str, Any], root: Path) -> tuple[Path, Path]:
	coverage = definition.get("coverage")
	status = coverage.get("status") if isinstance(coverage, Mapping) else None
	if status == "partial":
		return _path(root, PARTIAL_RELATIVE_PATH), _path(root, AUTHOR_READY_RELATIVE_PATH)
	if status == "author_ready":
		return _path(root, AUTHOR_READY_RELATIVE_PATH), _path(root, PARTIAL_RELATIVE_PATH)
	raise RuntimeError(f"Taxi seed has unsupported coverage status {status!r}; only partial or author_ready can be materialized")


def _validation_errors(definition: dict[str, Any]) -> list[str]:
	errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", "Taxi seed")
	errors.extend(validate_machine(definition))
	return errors


def _binding_index(definition: Mapping[str, Any], collection_name: str) -> dict[tuple[str, int], dict[str, Any]]:
	collection = definition.get(collection_name)
	if not isinstance(collection, list):
		raise RuntimeError(f"Taxi seed {collection_name} must be an array")
	indexed: dict[tuple[str, int], dict[str, Any]] = {}
	for index, item in enumerate(collection):
		if not isinstance(item, dict):
			raise RuntimeError(f"Taxi seed {collection_name}[{index}] must be an object")
		binding = item.get("binding")
		if not isinstance(binding, dict) or not isinstance(binding.get("group"), str) or not isinstance(binding.get("device"), int):
			raise RuntimeError(f"Taxi seed {collection_name}[{index}] has no numeric controller binding")
		key = (binding["group"], binding["device"])
		if key in indexed:
			raise RuntimeError(f"Taxi seed duplicates {collection_name} binding {key}")
		indexed[key] = item
	return indexed


def _assert_exact_taxi_contract(definition: dict[str, Any]) -> None:
	"""Check only the settled controller topology, never semantic source content."""
	errors: list[str] = []
	machine = definition.get("machine")
	if not isinstance(machine, dict) or machine.get("id") != MACHINE_ID:
		errors.append(f"machine.id must be {MACHINE_ID!r}")

	drivers = definition.get("drivers")
	driver_ids = {driver.get("id") for driver in drivers if isinstance(driver, dict)} if isinstance(drivers, list) else set()
	if driver_ids != DRIVER_IDS or not isinstance(drivers, list) or len(drivers) != len(DRIVER_IDS):
		errors.append(f"drivers must be exactly {sorted(DRIVER_IDS)!r}")

	controller = definition.get("controller")
	if not isinstance(controller, dict) or controller.get("platform") != "pinmame.system-11":
		errors.append("controller.platform must be pinmame.system-11 for the pinned GEN_S11B Taxi driver")

	inputs = _binding_index(definition, "inputs")
	expected_inputs = {(SWITCH_GROUP, address) for address in EXPECTED_SWITCH_BINDINGS} | {(DIP_GROUP, 0)}
	if set(inputs) != expected_inputs or len(inputs) != 77:
		errors.append("inputs must be exactly diagnostics -7..-4, matrix 1..64, flipper column 81..88, and country DIP 0 (77 total)")
	for address in set(range(1, 65)) - {2}:
		if inputs.get((SWITCH_GROUP, address), {}).get("kind") != "switch":
			errors.append(f"matrix switch {address} must remain a switch input")
	matrix_two = inputs.get((SWITCH_GROUP, 2))
	if not matrix_two or matrix_two.get("kind") != "virtual":
		errors.append("matrix switch 2 must remain a virtual mux-feedback input")
	elif "physical" in matrix_two:
		errors.append("matrix switch 2 virtual mux-feedback input must not carry physical metadata")
	if inputs.get((DIP_GROUP, 0), {}).get("kind") != "dip_switch":
		errors.append("country DIP 0 must be a dip_switch input")

	outputs = _binding_index(definition, "outputs")
	expected_outputs = {(SOLENOID_GROUP, address) for address in EXPECTED_SOLENOID_BINDINGS} | {(LAMP_GROUP, address) for address in EXPECTED_LAMP_BINDINGS}
	if set(outputs) != expected_outputs or len(outputs) != 114:
		errors.append("outputs must be exactly solenoids 1..50 and lamps 1..64 (114 total)")
	for address in range(45, 49):
		if outputs.get((SOLENOID_GROUP, address), {}).get("kind") != "virtual":
			errors.append(f"solenoid {address} must remain a synthetic virtual flipper state")

	for source_address, matrix_address in ((82, 57), (84, 58)):
		source = inputs.get((SWITCH_GROUP, source_address))
		destination = inputs.get((SWITCH_GROUP, matrix_address))
		if not source or source.get("availability") != "used":
			errors.append(f"flipper-column switch {source_address} must be used")
			continue
		if not destination:
			errors.append(f"Taxi matrix switch {matrix_address} is missing")
			continue
		relationships = definition.get("relationships")
		pairs = {
			(item.get("source"), item.get("destination"))
			for item in relationships
			if isinstance(item, dict) and item.get("kind") == "direct"
		} if isinstance(relationships, list) else set()
		if (source.get("id"), destination.get("id")) not in pairs:
			errors.append(f"flipper-column switch {source_address} must directly copy to matrix switch {matrix_address}")

	displays = definition.get("displays")
	if not isinstance(displays, list) or len(displays) != 3 or any(not isinstance(display, dict) or display.get("kind") != "segment" for display in displays):
		errors.append("Taxi must enumerate exactly three segment displays")
	else:
		widths = sorted(display.get("width") for display in displays)
		if widths != [7, 16, 16]:
			errors.append("Taxi displays must be two 16-character score displays and one seven-digit Jackpot/Meter display")

	if errors:
		raise RuntimeError("Taxi seed violates its settled controller contract:\n- " + "\n- ".join(errors))


def build(root: Path = ROOT) -> dict[str, Any]:
	"""Read and validate the canonical Taxi machine seed without modifying it."""
	definition = _canonical_json(_seed_path(root), "machine seed")
	errors = _validation_errors(definition)
	if errors:
		raise RuntimeError("Taxi machine seed is malformed:\n- " + "\n- ".join(errors))
	_assert_exact_taxi_contract(definition)
	_binding_register(root)
	return definition


def knowledge_text(root: Path = ROOT) -> str:
	"""Return the literal, seed-owned Taxi knowledge note unchanged."""
	path = _knowledge_seed_path(root)
	if not path.is_file():
		raise RuntimeError(f"Taxi knowledge seed is missing: {path}")
	try:
		# Decode bytes directly rather than using text-mode newline translation: this is a literal
		# source, so even its line endings must survive materialization unchanged.
		return path.read_bytes().decode("utf-8")
	except (OSError, UnicodeDecodeError) as error:
		raise RuntimeError(f"Taxi knowledge seed is malformed UTF-8: {path}: {error}") from error


def _safe_repository_path(root: Path, relative: str, label: str) -> Path:
	if not isinstance(relative, str):
		raise RuntimeError(f"Taxi {label} path must be a string")
	parts = PurePosixPath(relative).parts
	if not parts or PurePosixPath(relative).is_absolute() or ".." in parts or "\\" in relative or any(":" in part for part in parts):
		raise RuntimeError(f"Taxi {label} path must be a safe repository-relative POSIX path: {relative!r}")
	candidate = root.joinpath(*parts)
	try:
		candidate.resolve().relative_to(root.resolve())
	except ValueError as error:
		raise RuntimeError(f"Taxi {label} path escapes the repository root: {relative!r}") from error
	return candidate


def _verify_file_digest(path: Path, expected_size: int | None, expected_sha256: str, label: str) -> None:
	if not path.is_file():
		raise RuntimeError(f"Taxi {label} is missing: {path}")
	if expected_size is not None and path.stat().st_size != expected_size:
		raise RuntimeError(f"Taxi {label} size drifted: {path}")
	actual = hashlib.sha256(path.read_bytes()).hexdigest()
	if actual != expected_sha256:
		raise RuntimeError(f"Taxi {label} SHA-256 drifted: {path}")


def _verify_repository_excerpts(definition: Mapping[str, Any], root: Path) -> None:
	sources = definition.get("sources")
	if not isinstance(sources, list):
		raise RuntimeError("Taxi seed sources must be an array")
	for source in sources:
		if not isinstance(source, dict):
			continue
		for excerpt in source.get("excerpts", []):
			if not isinstance(excerpt, dict):
				raise RuntimeError("Taxi seed contains a malformed source excerpt")
			path_text = excerpt.get("path")
			if not isinstance(path_text, str) or not path_text.startswith("evidence/excerpts/"):
				raise RuntimeError(f"Taxi excerpt must remain under evidence/excerpts/: {path_text!r}")
			sha256 = excerpt.get("sha256")
			if not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
				raise RuntimeError(f"Taxi excerpt has an invalid SHA-256: {path_text!r}")
			_verify_file_digest(_safe_repository_path(root, path_text, "excerpt"), None, sha256, "repository excerpt")
			if "image" in excerpt:
				image = excerpt.get("image")
				image_sha256 = excerpt.get("image_sha256")
				if not isinstance(image, str) or not isinstance(image_sha256, str) or not SHA256_PATTERN.fullmatch(image_sha256):
					raise RuntimeError(f"Taxi excerpt image is malformed: {path_text!r}")
				_verify_file_digest(_safe_repository_path(root, image, "excerpt image"), None, image_sha256, "repository excerpt image")


def _report_device_record(device: Mapping[str, Any]) -> dict[str, Any]:
	return {
		"id": device.get("id"),
		"label": device.get("label"),
		"binding": device.get("binding"),
		"kind": device.get("kind"),
		"physical": device.get("physical"),
		"provenance": device.get("provenance"),
	}


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Project only spatial/source facts already declared by the canonical seed."""
	coverage = definition["coverage"]
	status = coverage["status"]
	located: list[dict[str, Any]] = []
	not_applicable: list[dict[str, Any]] = []
	unplaced_physical: list[dict[str, Any]] = []
	projection_disclosures: list[dict[str, Any]] = []

	for collection_name in ("inputs", "outputs"):
		for device in definition[collection_name]:
			spatial = device.get("spatial")
			if isinstance(spatial, dict) and spatial.get("status") == "not_applicable":
				record = _report_device_record(device)
				record["reason"] = spatial.get("reason")
				record["spatial_provenance"] = spatial.get("provenance")
				not_applicable.append(record)
				continue
			if isinstance(spatial, dict) and isinstance(spatial.get("placements"), list):
				record = _report_device_record(device)
				record["spatial"] = spatial
				located.append(record)
				physical = device.get("physical")
				if isinstance(physical, dict) and isinstance(physical.get("notes"), str) and "project" in physical["notes"].casefold():
					projection_disclosures.append(record)
				continue
			if isinstance(device.get("physical"), dict):
				unplaced_physical.append(_report_device_record(device))

	source_hashes = []
	for source in definition["sources"]:
		source_hashes.append({
			"id": source.get("id"),
			"kind": source.get("kind"),
			"uri": source.get("uri"),
			"locator": source.get("locator"),
			"sha256": source.get("sha256"),
			"excerpts": [
				{
					"id": excerpt.get("id"),
					"path": excerpt.get("path"),
					"sha256": excerpt.get("sha256"),
					"image": excerpt.get("image"),
					"image_sha256": excerpt.get("image_sha256"),
				}
				for excerpt in source.get("excerpts", [])
			],
		})

	promotion = {
		"seed_status": status,
		"missing": coverage["missing"],
		"decision": "author_ready as declared by the canonical seed" if status == "author_ready" else "partial; promotion is not declared while coverage.missing is non-empty",
	}
	return {
		"format": "pinmame-spatial-audit" if status == "author_ready" else "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"coordinate_convention": {
			"space": "playfield",
			"x": "0=left, 1=right in player view",
			"y": "0=rear/backglass end, 1=apron end in player view",
		},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"source_hashes": source_hashes,
		"located_devices": located,
		"projection_disclosures": projection_disclosures,
		"unplaced_physical_devices": unplaced_physical,
		"not_applicable_devices": not_applicable,
		"coverage": {"status": status, "missing": coverage["missing"]},
		"promotion_decision": promotion,
		"emitter_policy": "Each emitted placement is reproduced as its own seed placement. Glow sprites and render helpers are not physical socket proof unless the canonical seed records a physical placement and provenance.",
	}


def _binding_text(record: Mapping[str, Any]) -> str:
	binding = record.get("binding")
	if not isinstance(binding, Mapping):
		return "unbound"
	return f"{binding.get('group')} {binding.get('device')}"


def render_spatial_report(report: dict[str, Any]) -> str:
	"""Render the machine-specific report without reading non-seed evidence."""
	lines = [
		f"# Spatial report — {report['machine_id']}",
		"",
		f"Format: `{report['format']}` v{report['version']}",
		f"Definition SHA-256: `{report['definition_sha256']}`",
		"",
		"## Coordinate convention",
		"",
		f"- `{report['coordinate_convention']['x']}`",
		f"- `{report['coordinate_convention']['y']}`",
		"",
		"## Coverage and promotion decision",
		"",
		f"- Seed status: `{report['coverage']['status']}`",
		f"- Missing coverage: `{json.dumps(report['coverage']['missing'], ensure_ascii=False)}`",
		f"- Decision: {report['promotion_decision']['decision']}",
		"",
		"## Source hashes and repository excerpts",
		"",
	]
	for source in report["source_hashes"]:
		lines.append(f"- `{source['id']}` ({source['kind']}): `{source['sha256']}`")
		lines.append(f"  - {source['uri']} — {source['locator']}")
		for excerpt in source["excerpts"]:
			lines.append(f"  - `{excerpt['id']}` — `{excerpt['path']}` SHA-256 `{excerpt['sha256']}`")
			if excerpt.get("image") is not None:
				lines.append(f"    - image `{excerpt['image']}` SHA-256 `{excerpt['image_sha256']}`")

	lines.extend(["", "## Exact seeded placements", ""])
	if report["located_devices"]:
		for device in report["located_devices"]:
			lines.append(f"- `{device['id']}` ({_binding_text(device)}): `{device['spatial']['status']}`")
			for placement in device["spatial"]["placements"]:
				lines.append(f"  - `{placement['id']}` — {placement['role']} at ({placement['x']}, {placement['y']}); sources `{', '.join(placement['provenance']['source_refs'])}`")
	else:
		lines.append("- None recorded by the canonical seed.")

	lines.extend(["", "## Projection disclosures", ""])
	if report["projection_disclosures"]:
		for device in report["projection_disclosures"]:
			lines.append(f"- `{device['id']}` ({_binding_text(device)}): {device['physical']['notes']}")
	else:
		lines.append("- No placement notes explicitly disclose a projection.")

	lines.extend(["", "## Unplaced physical devices", ""])
	if report["unplaced_physical_devices"]:
		for device in report["unplaced_physical_devices"]:
			lines.append(f"- `{device['id']}` ({_binding_text(device)})")
	else:
		lines.append("- None recorded by the canonical seed.")

	lines.extend(["", "## Controlled not-applicable spatial records", ""])
	if report["not_applicable_devices"]:
		for device in report["not_applicable_devices"]:
			lines.append(f"- `{device['id']}` ({_binding_text(device)}): `{device['reason']}`")
	else:
		lines.append("- None recorded by the canonical seed.")

	lines.extend(["", "## Emitter policy", "", report["emitter_policy"], ""])
	return "\n".join(lines)


def _verify_generated_artifacts(definition: dict[str, Any], root: Path, expected_knowledge: str) -> None:
	definition_path, opposing_path = _definition_paths(definition, root)
	if opposing_path.exists():
		raise RuntimeError(f"Taxi has a stale opposing-status artifact: {opposing_path}")
	expected_definition = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected_definition:
		raise RuntimeError(f"Taxi generated definition drifted from the canonical seed: {definition_path}")

	knowledge_path = _path(root, KNOWLEDGE_RELATIVE_PATH)
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != expected_knowledge.encode("utf-8"):
		raise RuntimeError(f"Taxi generated knowledge note drifted from its literal seed: {knowledge_path}")

	report = build_spatial_report(definition)
	report_path = _path(root, SPATIAL_REPORT_RELATIVE_PATH)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Taxi spatial report drifted from the canonical seed: {report_path}")
	markdown_path = _path(root, SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH)
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Taxi spatial report Markdown drifted from the canonical seed: {markdown_path}")


def generate(root: Path = ROOT) -> Path:
	"""Write only Taxi-derived artifacts, never the seed, catalog, or coverage reports."""
	definition = build(root)
	knowledge = knowledge_text(root)
	_verify_repository_excerpts(definition, root)
	definition_path, opposing_path = _definition_paths(definition, root)
	if opposing_path.exists():
		if definition["coverage"]["status"] == "partial" and opposing_path == _path(root, AUTHOR_READY_RELATIVE_PATH):
			raise RuntimeError(f"Refusing to overwrite an existing author-ready Taxi artifact with a partial seed: {opposing_path}")
		raise RuntimeError(f"Refusing to generate Taxi while a stale opposing-status artifact exists: {opposing_path}")

	write_json(definition_path, definition)
	write_text(_path(root, KNOWLEDGE_RELATIVE_PATH), knowledge)
	report = build_spatial_report(definition)
	write_json(_path(root, SPATIAL_REPORT_RELATIVE_PATH), report)
	write_text(_path(root, SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH), render_spatial_report(report))
	return definition_path


def check(root: Path = ROOT) -> None:
	"""Fail closed when a Taxi input, repository excerpt, or generated artifact drifts."""
	definition = build(root)
	knowledge = knowledge_text(root)
	_definition_path, opposing_path = _definition_paths(definition, root)
	if opposing_path.exists():
		raise RuntimeError(f"Taxi has a stale opposing-status artifact: {opposing_path}")
	knowledge_path = definition.get("knowledge", {}).get("path") if isinstance(definition.get("knowledge"), dict) else None
	if knowledge_path != KNOWLEDGE_RELATIVE_PATH.as_posix():
		raise RuntimeError(f"Taxi seed must reference {KNOWLEDGE_RELATIVE_PATH.as_posix()!r}, not {knowledge_path!r}")
	semantic_errors = validate_machine(definition, root)
	if semantic_errors:
		raise RuntimeError("Taxi seed has invalid repository references:\n- " + "\n- ".join(semantic_errors))
	_verify_repository_excerpts(definition, root)
	_verify_generated_artifacts(definition, root, knowledge)
	print("Taxi definition, literal knowledge note, spatial report, and repository excerpts match the canonical seed.")


def _register_entry(entry: Any, label: str) -> tuple[str, str, int, str, dict[str, Any] | None]:
	if not isinstance(entry, dict):
		raise RuntimeError(f"Taxi evidence binding {label} must be an object")
	allowed = {"root", "path", "size", "sha256", "extraction_manifest"}
	unknown = set(entry) - allowed
	if unknown:
		raise RuntimeError(f"Taxi evidence binding {label} has unsupported fields: {sorted(unknown)!r}")
	if set(entry) - {"extraction_manifest"} != {"root", "path", "size", "sha256"}:
		raise RuntimeError(f"Taxi evidence binding {label} must contain root, path, size, and sha256")
	root = entry["root"]
	path = entry["path"]
	size = entry["size"]
	sha256 = entry["sha256"]
	if root not in {"vpx", "manuals", "review"} or not isinstance(path, str) or not isinstance(size, int) or isinstance(size, bool) or size < 0 or not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
		raise RuntimeError(f"Taxi evidence binding {label} is malformed")
	manifest = entry.get("extraction_manifest")
	if manifest is not None and not isinstance(manifest, dict):
		raise RuntimeError(f"Taxi evidence binding {label} extraction_manifest must be an object")
	return root, path, size, sha256, manifest


def _external_file(root: Path, relative: str, label: str) -> Path:
	parts = PurePosixPath(relative).parts
	if not parts or PurePosixPath(relative).is_absolute() or ".." in parts or "\\" in relative or any(":" in part for part in parts):
		raise RuntimeError(f"Taxi {label} must use a safe relative POSIX path: {relative!r}")
	candidate = root.joinpath(*parts)
	try:
		candidate.resolve().relative_to(root.resolve())
	except ValueError as error:
		raise RuntimeError(f"Taxi {label} escapes its configured source root: {relative!r}") from error
	return candidate


def _verify_manifest_binding(manifest: dict[str, Any], default_root: str, roots: Mapping[str, Path | None], label: str) -> None:
	allowed = {"root", "path", "size", "sha256"}
	if set(manifest) != {"path", "size", "sha256"} and set(manifest) != allowed:
		raise RuntimeError(f"Taxi {label} extraction_manifest must contain path, size, sha256, and optional root")
	root_name = manifest.get("root", default_root)
	path = manifest.get("path")
	size = manifest.get("size")
	sha256 = manifest.get("sha256")
	if root_name not in roots or not isinstance(path, str) or not isinstance(size, int) or isinstance(size, bool) or size < 0 or not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
		raise RuntimeError(f"Taxi {label} extraction_manifest is malformed")
	external_root = roots[root_name]
	if external_root is None or not external_root.is_dir():
		raise RuntimeError(f"Taxi {label} requires a readable {root_name} source root")
	manifest_path = _external_file(external_root, path, f"{label} extraction manifest")
	_verify_file_digest(manifest_path, size, sha256, f"{label} extraction manifest")
	if manifest_path.name == "manifest.json":
		try:
			check_manifest(manifest_path.parent, "taxi_l4")
		except (ValueError, OSError) as error:
			raise RuntimeError(f"Taxi extraction content drifted: {error}") from error


def _binding_register(root: Path) -> dict[str, Any]:
	"""Validate the third authored input even without external evidence roots."""
	register = _canonical_json(_path(root, EVIDENCE_BINDING_RELATIVE_PATH), "external evidence binding register")
	if set(register) - {"format", "version", "files"} or not isinstance(register.get("files"), list) or not register["files"]:
		raise RuntimeError("Taxi external evidence binding register must be a simple non-empty files list")
	if register.get("format") != "taxi-retained-evidence-bindings" or register.get("version") != 1:
		raise RuntimeError("Taxi external evidence binding register has the wrong format or version")
	seen: set[tuple[str, str]] = set()
	for index, entry in enumerate(register["files"]):
		root_name, relative, _size, _sha, manifest = _register_entry(entry, f"files[{index}]")
		_safe_repository_path(root, relative, "retained evidence")
		key = (root_name, relative)
		if key in seen:
			raise RuntimeError(f"Taxi evidence binding register duplicates {root_name}:{relative}")
		seen.add(key)
		if manifest is not None:
			_manifest_root, manifest_path, _size, _sha, _ = _register_entry(
				{"root": root_name, **manifest}, f"files[{index}] extraction_manifest")
			_safe_repository_path(root, manifest_path, "extraction manifest")
	return register


def verify_retained(
	vpx_root: Path | str | None,
	manuals_root: Path | str | None,
	review_root: Path | str | None,
	*,
	root: Path = ROOT,
) -> None:
	"""Verify all read-only external files pinned by Taxi's binding register."""
	register = _binding_register(root)
	roots: dict[str, Path | None] = {
		"vpx": Path(vpx_root) if vpx_root is not None else None,
		"manuals": Path(manuals_root) if manuals_root is not None else None,
		"review": Path(review_root) if review_root is not None else None,
	}
	seen: set[tuple[str, str]] = set()
	for index, entry in enumerate(register["files"]):
		root_name, relative_path, size, sha256, manifest = _register_entry(entry, f"files[{index}]")
		key = (root_name, relative_path)
		if key in seen:
			raise RuntimeError(f"Taxi evidence binding register duplicates {root_name}:{relative_path}")
		seen.add(key)
		external_root = roots[root_name]
		if external_root is None or not external_root.is_dir():
			raise RuntimeError(f"Taxi evidence binding files[{index}] requires a readable {root_name} source root")
		_verify_file_digest(_external_file(external_root, relative_path, f"evidence binding files[{index}]"), size, sha256, f"retained {root_name} evidence")
		if manifest is not None:
			_verify_manifest_binding(manifest, root_name, roots, f"evidence binding files[{index}]")


def _configured_root(name: str) -> Path | None:
	value = os.environ.get(name)
	return Path(value) if value else None


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true", help="Check Taxi seed-owned artifacts; this is the default")
	mode.add_argument("--regenerate", action="store_true", help="Materialize only Taxi definition, knowledge, and spatial-report paths")
	mode.add_argument("--verify-retained", action="store_true", help="Verify the optional external evidence binding register")
	parser.add_argument("--vpx-root", type=Path, help="Override PINMAME_VPX_SOURCES_ROOT for --verify-retained")
	parser.add_argument("--manuals-root", type=Path, help="Override PINMAME_MANUALS_ROOT for --verify-retained")
	parser.add_argument("--review-root", type=Path, help="Override PINMAME_REVIEW_ARTIFACTS_ROOT for --verify-retained")
	args = parser.parse_args()
	if args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	elif args.verify_retained:
		verify_retained(
			args.vpx_root or _configured_root("PINMAME_VPX_SOURCES_ROOT"),
			args.manuals_root or _configured_root("PINMAME_MANUALS_ROOT"),
			args.review_root or _configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT"),
		)
		print("Taxi retained external evidence matches its binding register.")
	else:
		check(ROOT)


if __name__ == "__main__":
	main()
