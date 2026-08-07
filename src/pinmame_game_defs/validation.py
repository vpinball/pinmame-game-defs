from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .errors import ValidationError
from .evidence_policy import EvidenceAssertion, evidence_priority
from .jsonio import content_sha256, file_sha256, load_json
from .schema_validation import check_schema_documents, validate_against_schema
from .scope import OUT_OF_SCOPE_DRIVER_IDS

IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
GENERIC_LABEL_PATTERN = re.compile(r"^(?:switch|output|solenoid|lamp|gi)\s*#?\s*-?\d+$", re.IGNORECASE)
FORBIDDEN_KEYS = {
	"device_hint",
	"device_item_hint",
	"num_matches",
	"input_action_hint",
	"input_map_hint",
}
AUTHOR_READY_DIMENSIONS = {
	"catalog_identity",
	"address_enumeration",
	"semantic_naming",
	"physical_wiring",
	"mechanisms",
	"variant_coverage",
	"recreation_knowledge",
	"spatial_placement",
}
BASE_COVERAGE_DIMENSIONS = AUTHOR_READY_DIMENSIONS - {"spatial_placement"}
SPATIAL_NA_REASONS = {
	"unused",
	"virtual",
	"constant",
	"dip_switch",
	"cabinet_or_service",
	"internal_nonvisual",
	"no_physical_device",
}
SPATIAL_ROLES = {"sensor", "effect", "emitter"}
EMITTER_OUTPUT_KINDS = {"lamp", "rgb_lamp", "flasher", "gi"}
# Non-emitting outputs. ``control_signal`` covers logic-level lines that drive another board rather
# than a physical actuator, such as the serial clock and data lines into a lamp shift register. Like
# the other effect kinds they have no light of their own, so they take an internal_nonvisual record.
EFFECT_OUTPUT_KINDS = {"coil", "motor", "servo", "magnet", "relay", "control_signal"}
SHARED_RGB_FIELDS = ("quantity", "shared_emitter_group", "emitter_channel", "co_located_addresses", "shared_physical_quantity")
SHARED_RGB_CHANNELS = {"blue", "green", "red"}
LOCAL_L_DRIVE_PATTERN = re.compile(r"(?:^|[^a-z0-9])l:[\\/]", re.IGNORECASE)


def _expect(condition: bool, path: str, message: str, errors: list[str]) -> None:
	if not condition:
		errors.append(f"{path}: {message}")


def _walk_forbidden(value: Any, path: str, errors: list[str]) -> None:
	if isinstance(value, dict):
		for key, nested in value.items():
			child_path = f"{path}.{key}"
			if key in FORBIDDEN_KEYS:
				errors.append(f"{child_path}: VPE authoring hint is forbidden in canonical definitions")
			if key == "extensions" and isinstance(nested, dict) and "vpe" in nested:
				errors.append(f"{child_path}.vpe: open-ended VPE extensions are forbidden")
			_walk_forbidden(nested, child_path, errors)
	elif isinstance(value, list):
		for index, nested in enumerate(value):
			_walk_forbidden(nested, f"{path}[{index}]", errors)


def _validate_identifier(value: Any, path: str, errors: list[str]) -> None:
	_expect(isinstance(value, str) and bool(IDENTIFIER_PATTERN.fullmatch(value)), path, "must be a stable lowercase identifier", errors)


def _unique(values: Iterable[Any], path: str, errors: list[str]) -> None:
	seen: set[Any] = set()
	for value in values:
		if value in seen:
			errors.append(f"{path}: duplicate value {value!r}")
		seen.add(value)


def _required_mapping(value: Any, path: str, keys: set[str], errors: list[str]) -> dict[str, Any]:
	if not isinstance(value, dict):
		errors.append(f"{path}: must be an object")
		return {}
	for key in sorted(keys - set(value)):
		errors.append(f"{path}.{key}: required field is missing")
	return value


def _validate_provenance_refs(provenance: Any, path: str, source_ids: set[str], errors: list[str], require_validated: bool = False) -> None:
	if not isinstance(provenance, dict):
		errors.append(f"{path}: must be an object")
		return
	refs = provenance.get("source_refs")
	_expect(isinstance(refs, list) and bool(refs), f"{path}.source_refs", "must contain a source reference", errors)
	if isinstance(refs, list):
		for source_ref in refs:
			_expect(source_ref in source_ids, f"{path}.source_refs", f"unknown source reference {source_ref!r}", errors)
	if require_validated:
		_expect(provenance.get("status") == "validated", f"{path}.status", "author-ready spatial assertions must be validated", errors)


def _validate_excerpts(
	source: dict[str, Any],
	path: str,
	repository_root: Path | None,
	errors: list[str],
) -> None:
	"""Excerpts must actually be present and match their recorded bytes.

	An excerpt exists so a reader can see what a source said without holding the document. A path
	that does not resolve, or a digest that no longer matches, silently removes that ability, so
	both fail closed rather than being advisory.
	"""
	excerpts = source.get("excerpts")
	if excerpts is None:
		return
	if not isinstance(excerpts, list):
		errors.append(f"{path}.excerpts: must be a list")
		return
	seen: set[str] = set()
	for index, excerpt in enumerate(excerpts):
		item = f"{path}.excerpts[{index}]"
		if not isinstance(excerpt, dict):
			errors.append(f"{item}: must be an object")
			continue
		excerpt_id = excerpt.get("id")
		_validate_identifier(excerpt_id, f"{item}.id", errors)
		if isinstance(excerpt_id, str):
			_expect(excerpt_id not in seen, f"{item}.id", f"duplicate excerpt ID {excerpt_id}", errors)
			seen.add(excerpt_id)
		if repository_root is None:
			continue
		for field, digest_field in (("path", "sha256"), ("image", "image_sha256")):
			relative = excerpt.get(field)
			if not isinstance(relative, str):
				continue
			resolved = repository_root / relative
			if not resolved.is_file():
				errors.append(f"{item}.{field}: missing excerpt file {relative}")
				continue
			recorded = excerpt.get(digest_field)
			if isinstance(recorded, str):
				actual = file_sha256(resolved)
				_expect(actual == recorded, f"{item}.{digest_field}",
				        f"{relative} does not match its recorded digest", errors)


def _has_cabinet_or_service_role(device: dict[str, Any]) -> bool:
	roles = device.get("roles")
	return isinstance(roles, list) and any(
		isinstance(role, str)
		and (role.startswith(("cabinet.", "service.")) or (role.startswith("flipper.") and role.endswith(".button")))
		for role in roles
	)


def _has_internal_role(device: dict[str, Any]) -> bool:
	roles = device.get("roles")
	return isinstance(roles, list) and any(isinstance(role, str) and role.startswith("internal.") for role in roles)


def _fractional_precision(value: float) -> int:
	text = format(value, ".15f").rstrip("0").rstrip(".")
	return len(text.partition(".")[2])


def _validate_spatial(
	device: dict[str, Any],
	collection_name: str,
	path: str,
	status: Any,
	source_ids: set[str],
	placement_ids: set[str],
	errors: list[str],
) -> None:
	subject = "display" if collection_name == "displays" else "device"
	spatial = device.get("spatial")
	if spatial is None:
		if status == "author_ready":
			errors.append(f"{path}.spatial: author-ready {subject}s require spatial evidence or a controlled not_applicable record")
		return
	if not isinstance(spatial, dict):
		errors.append(f"{path}.spatial: must be an object")
		return
	spatial_status = spatial.get("status")
	if collection_name == "displays" and spatial_status != "not_applicable":
		errors.append(f"{path}.spatial.status: located playfield display coordinates are not supported; displays must use not_applicable with reason cabinet_or_service")
		return
	if spatial_status == "not_applicable":
		reason = spatial.get("reason")
		_expect(reason in SPATIAL_NA_REASONS, f"{path}.spatial.reason", "must be a controlled not_applicable reason", errors)
		_expect("placements" not in spatial, f"{path}.spatial.placements", "not_applicable records cannot contain placements", errors)
		_validate_provenance_refs(spatial.get("provenance"), f"{path}.spatial.provenance", source_ids, errors, status == "author_ready")
		if collection_name == "displays":
			_expect(reason == "cabinet_or_service", f"{path}.spatial.reason", "displays must use reason cabinet_or_service", errors)
			return
		if status != "author_ready":
			return
		availability = device.get("availability")
		kind = device.get("kind")
		if collection_name == "inputs":
			if kind == "virtual":
				expected = "virtual"
			elif kind == "constant":
				expected = "constant"
			elif kind == "dip_switch":
				expected = "dip_switch"
			elif availability == "unused":
				expected = "unused"
			elif kind == "switch" and availability in {"used", "optional"} and _has_cabinet_or_service_role(device):
				expected = "cabinet_or_service"
			elif kind == "switch" and availability in {"used", "optional"} and _has_internal_role(device):
				expected = "internal_nonvisual"
			else:
				expected = None
			_expect(reason == expected, f"{path}.spatial.reason", "does not align with this author-ready input's physical status", errors)
		else:
			if kind == "virtual":
				expected = "virtual"
			elif availability == "unused":
				expected = "unused"
			elif kind in EMITTER_OUTPUT_KINDS | EFFECT_OUTPUT_KINDS and availability in {"used", "optional"} and _has_cabinet_or_service_role(device):
				expected = "cabinet_or_service"
			elif kind in EMITTER_OUTPUT_KINDS | EFFECT_OUTPUT_KINDS and availability in {"used", "optional"} and _has_internal_role(device):
				expected = "internal_nonvisual"
			elif kind in EFFECT_OUTPUT_KINDS and availability in {"used", "optional"}:
				expected = "internal_nonvisual"
			else:
				expected = None
			_expect(reason == expected, f"{path}.spatial.reason", "does not align with this author-ready output's physical status", errors)
		return
	_expect(spatial_status in {"candidate", "observed", "validated", "conflicted"}, f"{path}.spatial.status", "must be a located spatial assertion or not_applicable", errors)
	placements = spatial.get("placements")
	_expect(isinstance(placements, list) and bool(placements), f"{path}.spatial.placements", "located spatial evidence requires one or more placements", errors)
	if not isinstance(placements, list):
		return
	roles: list[Any] = []
	for index, placement in enumerate(placements):
		placement_path = f"{path}.spatial.placements[{index}]"
		if not isinstance(placement, dict):
			errors.append(f"{placement_path}: must be an object")
			continue
		placement_id = placement.get("id")
		_validate_identifier(placement_id, f"{placement_path}.id", errors)
		if isinstance(placement_id, str):
			if placement_id in placement_ids:
				errors.append(f"{placement_path}.id: duplicate spatial placement ID {placement_id!r}")
			placement_ids.add(placement_id)
		role = placement.get("role")
		roles.append(role)
		_expect(role in SPATIAL_ROLES, f"{placement_path}.role", "must be sensor, effect, or emitter", errors)
		_expect(placement.get("space") == "playfield", f"{placement_path}.space", "must use the canonical playfield coordinate space", errors)
		for coordinate in ("x", "y"):
			value = placement.get(coordinate)
			valid_number = isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))
			_expect(valid_number, f"{placement_path}.{coordinate}", "must be a finite number", errors)
			if valid_number:
				_expect(0 <= value <= 1, f"{placement_path}.{coordinate}", "must be within the inclusive 0..1 playfield bounds", errors)
				_expect(_fractional_precision(float(value)) <= 6, f"{placement_path}.{coordinate}", "must use no more than six fractional decimal places", errors)
		_validate_provenance_refs(placement.get("provenance"), f"{placement_path}.provenance", source_ids, errors, status == "author_ready")
	if status != "author_ready":
		return
	_expect(spatial_status == "validated", f"{path}.spatial.status", "author-ready spatial assertions must be validated", errors)
	availability = device.get("availability")
	kind = device.get("kind")
	if collection_name == "inputs":
		if kind == "switch" and availability in {"used", "optional"}:
			_expect(all(role == "sensor" for role in roles), f"{path}.spatial.placements", "used or optional physical switches require only sensor placements", errors)
		else:
			errors.append(f"{path}.spatial: author-ready input requires a controlled not_applicable record")
	else:
		if kind in EMITTER_OUTPUT_KINDS and availability in {"used", "optional"}:
			_expect(all(role == "emitter" for role in roles), f"{path}.spatial.placements", "lamp, rgb_lamp, flasher, and gi outputs require only emitter placements", errors)
		elif kind in EFFECT_OUTPUT_KINDS and availability in {"used", "optional"}:
			_expect(all(role == "effect" for role in roles), f"{path}.spatial.placements", "coil, motor, servo, magnet, and relay outputs require only effect placements", errors)
		else:
			errors.append(f"{path}.spatial: author-ready output requires a controlled not_applicable record")


def _spatial_emitter_signature(device: dict[str, Any]) -> tuple[tuple[Any, Any, Any, Any], ...] | None:
	spatial = device.get("spatial")
	if not isinstance(spatial, dict):
		return None
	placements = spatial.get("placements")
	if not isinstance(placements, list) or not placements:
		return None
	signatures: list[tuple[Any, Any, Any, Any]] = []
	for placement in placements:
		if not isinstance(placement, dict):
			return None
		signatures.append((placement.get("space"), placement.get("role"), placement.get("x"), placement.get("y")))
	return tuple(sorted(signatures, key=lambda signature: tuple(repr(value) for value in signature)))


def _validate_shared_rgb_emitters(outputs: Any, errors: list[str]) -> None:
	"""Validate shared physical RGB emitter groups without machine-specific assumptions."""
	if not isinstance(outputs, list):
		return
	output_by_group: dict[str, dict[int, tuple[str, dict[str, Any]]]] = {}
	records_by_shared_group: dict[str, list[dict[str, Any]]] = {}
	for index, device in enumerate(outputs):
		if not isinstance(device, dict):
			continue
		path = f"$.outputs[{index}]"
		binding = device.get("binding")
		if isinstance(binding, dict) and isinstance(binding.get("group"), str) and isinstance(binding.get("device"), int) and not isinstance(binding.get("device"), bool):
			output_by_group.setdefault(binding["group"], {})[binding["device"]] = (path, device)
		physical = device.get("physical")
		if not isinstance(physical, dict):
			continue
		if not any(field in physical for field in SHARED_RGB_FIELDS[1:]):
			continue
		missing = [field for field in SHARED_RGB_FIELDS if field not in physical]
		for field in missing:
			errors.append(f"{path}.physical.{field}: shared RGB emitter metadata fields must appear together")
		if missing:
			continue
		shared_group = physical.get("shared_emitter_group")
		_validate_identifier(shared_group, f"{path}.physical.shared_emitter_group", errors)
		channel = physical.get("emitter_channel")
		_expect(channel in SHARED_RGB_CHANNELS, f"{path}.physical.emitter_channel", "shared RGB emitter channels must be blue, green, or red", errors)
		addresses = physical.get("co_located_addresses")
		valid_addresses = isinstance(addresses, list) and bool(addresses) and all(isinstance(address, int) and not isinstance(address, bool) for address in addresses)
		_expect(valid_addresses, f"{path}.physical.co_located_addresses", "must be a non-empty list of integer sibling addresses", errors)
		if valid_addresses:
			_unique(addresses, f"{path}.physical.co_located_addresses", errors)
		shared_quantity = physical.get("shared_physical_quantity")
		valid_shared_quantity = isinstance(shared_quantity, int) and not isinstance(shared_quantity, bool) and shared_quantity >= 1
		_expect(valid_shared_quantity, f"{path}.physical.shared_physical_quantity", "must be a positive integer", errors)
		quantity = physical.get("quantity")
		valid_quantity = isinstance(quantity, int) and not isinstance(quantity, bool) and quantity >= 1
		_expect(valid_quantity, f"{path}.physical.quantity", "must be a positive integer for a shared RGB emitter", errors)
		_expect(device.get("kind") in EMITTER_OUTPUT_KINDS, f"{path}.kind", "shared RGB emitter metadata requires an emitter output kind", errors)
		binding_group = binding.get("group") if isinstance(binding, dict) else None
		address = binding.get("device") if isinstance(binding, dict) else None
		if not isinstance(shared_group, str) or not isinstance(addresses, list) or not valid_addresses or not isinstance(binding_group, str) or not isinstance(address, int) or isinstance(address, bool):
			continue
		if valid_quantity and valid_shared_quantity:
			_expect(quantity == shared_quantity, f"{path}.physical.quantity", "must equal shared_physical_quantity for a shared RGB emitter", errors)
		records_by_shared_group.setdefault(shared_group, []).append(
			{
				"path": path,
				"device": device,
				"physical": physical,
				"binding_group": binding_group,
				"address": address,
				"addresses": set(addresses),
				"channel": channel,
				"shared_quantity": shared_quantity,
				"signature": _spatial_emitter_signature(device),
			}
		)

	for shared_group, records in records_by_shared_group.items():
		paths = [record["path"] for record in records]
		binding_groups = {record["binding_group"] for record in records}
		if len(binding_groups) != 1:
			errors.append(f"{paths[0]}.physical.shared_emitter_group: siblings must use the same output binding group")
		output_group = next(iter(binding_groups), None)
		actual_addresses = {record["address"] for record in records if record["binding_group"] == output_group}
		channels = [record["channel"] for record in records]
		valid_channels = all(isinstance(channel, str) for channel in channels)
		if not valid_channels or len(channels) != 3 or len(set(channels)) != 3 or set(channels) != SHARED_RGB_CHANNELS:
			errors.append(f"{paths[0]}.physical.emitter_channel: shared RGB emitter channels must be the unique exact blue/green/red set")
		if len({frozenset(record["addresses"]) for record in records}) != 1:
			errors.append(f"{paths[0]}.physical.co_located_addresses: siblings must agree on the complete address set")
		if any(record["shared_quantity"] != records[0]["shared_quantity"] for record in records[1:]):
			errors.append(f"{paths[0]}.physical.shared_physical_quantity: siblings must agree on the shared physical quantity")
		baseline_signature = records[0]["signature"]
		if baseline_signature is None:
			errors.append(f"{records[0]['path']}.spatial: shared RGB emitter siblings require placements")
		for record in records:
			path = record["path"]
			addresses = record["addresses"]
			address = record["address"]
			if address not in addresses:
				errors.append(f"{path}.physical.co_located_addresses: device's own address must be included")
			if addresses != actual_addresses:
				errors.append(f"{path}.physical.co_located_addresses: every sibling must be present in the same output group and the address set must match the group")
			for sibling_address in sorted(addresses):
				if output_group is None or sibling_address not in output_by_group.get(output_group, {}):
					errors.append(f"{path}.physical.co_located_addresses: sibling address {sibling_address} is not present in the same output group")
					continue
				sibling_path, sibling = output_by_group[output_group][sibling_address]
				sibling_physical = sibling.get("physical")
				if not isinstance(sibling_physical, dict) or any(field not in sibling_physical for field in SHARED_RGB_FIELDS):
					errors.append(f"{path}.physical.co_located_addresses: sibling {sibling_path} must declare complete shared RGB emitter metadata")
					continue
				if sibling_physical.get("shared_emitter_group") != shared_group:
					errors.append(f"{path}.physical.shared_emitter_group: siblings must agree on shared emitter group identity")
				sibling_addresses = sibling_physical.get("co_located_addresses")
				if isinstance(sibling_addresses, list) and all(isinstance(sibling_address, int) and not isinstance(sibling_address, bool) for sibling_address in sibling_addresses) and set(sibling_addresses) != addresses:
					errors.append(f"{path}.physical.co_located_addresses: siblings must agree on the complete address set")
				if sibling_physical.get("shared_physical_quantity") != record["shared_quantity"]:
					errors.append(f"{path}.physical.shared_physical_quantity: siblings must agree on the shared physical quantity")
				sibling_signature = _spatial_emitter_signature(sibling)
				if sibling_signature != record["signature"]:
					errors.append(f"{path}.spatial: sibling placements must have equivalent coordinates, roles, and coordinate space")


def validate_machine(definition: dict[str, Any], repository_root: Path | None = None) -> list[str]:
	errors: list[str] = []
	_walk_forbidden(definition, "$", errors)
	_expect(definition.get("format") == "pinmame-machine-definition", "$.format", "must equal pinmame-machine-definition", errors)
	schema_version = definition.get("schema_version")
	_expect(schema_version in {1, 2}, "$.schema_version", "must equal 1 or 2", errors)
	machine = _required_mapping(definition.get("machine"), "$.machine", {"id", "name", "manufacturer", "year"}, errors)
	machine_id = machine.get("id")
	_validate_identifier(machine_id, "$.machine.id", errors)
	_expect(machine.get("kind") != "virtual_pinball", "$.machine.kind", "virtual pinball records are outside the physical-machine scope", errors)
	coverage = _required_mapping(definition.get("coverage"), "$.coverage", {"status", "missing", "dimensions"}, errors)
	status = coverage.get("status")
	_expect(status in {"stub", "partial", "author_ready"}, "$.coverage.status", "must be stub, partial, or author_ready", errors)
	missing = coverage.get("missing")
	_expect(isinstance(missing, list), "$.coverage.missing", "must be an array", errors)
	if isinstance(missing, list):
		_unique(missing, "$.coverage.missing", errors)
	dimensions = coverage.get("dimensions")
	_expect(isinstance(dimensions, dict), "$.coverage.dimensions", "must be an object", errors)
	if isinstance(dimensions, dict):
		for dimension in (AUTHOR_READY_DIMENSIONS if schema_version == 2 else BASE_COVERAGE_DIMENSIONS):
			_expect(dimension in dimensions, f"$.coverage.dimensions.{dimension}", "required coverage dimension is missing", errors)
	if status == "stub":
		_expect(isinstance(machine_id, str) and machine_id.startswith("stub.pinmame."), "$.machine.id", "stub IDs must start with stub.pinmame.", errors)
		_expect(isinstance(machine.get("name"), str) and machine["name"].startswith("STUB - "), "$.machine.name", "stub names must start with STUB -", errors)
		_expect(isinstance(missing, list) and bool(missing), "$.coverage.missing", "stub must list missing authoring requirements", errors)
	else:
		_expect(isinstance(machine_id, str) and not machine_id.startswith("stub."), "$.machine.id", "non-stub definition cannot use a stub ID", errors)
	if status == "partial":
		_expect(isinstance(missing, list) and bool(missing), "$.coverage.missing", "partial definition must list missing authoring requirements", errors)
	if status == "author_ready":
		_expect(schema_version == 2, "$.schema_version", "author-ready definitions must use schema version 2", errors)
		_expect(missing == [], "$.coverage.missing", "author-ready definition cannot have missing requirements", errors)
		if isinstance(dimensions, dict):
			for dimension in AUTHOR_READY_DIMENSIONS:
				_expect(dimensions.get(dimension) in {"validated", "not_applicable"}, f"$.coverage.dimensions.{dimension}", "author-ready dimension must be validated or not_applicable", errors)
	drivers = definition.get("drivers")
	_expect(isinstance(drivers, list) and bool(drivers), "$.drivers", "must contain at least one driver", errors)
	if isinstance(drivers, list):
		driver_ids = [driver.get("id") for driver in drivers if isinstance(driver, dict)]
		_unique(driver_ids, "$.drivers[].id", errors)
		for index, driver_id in enumerate(driver_ids):
			_validate_identifier(driver_id, f"$.drivers[{index}].id", errors)
			_expect(driver_id not in OUT_OF_SCOPE_DRIVER_IDS, f"$.drivers[{index}].id", "custom-ROM-only virtual driver is outside the physical-machine scope", errors)
			if status == "author_ready":
				driver = drivers[index]
				_expect(driver.get("physical_compatibility") in {"identical", "compatible"}, f"$.drivers[{index}].physical_compatibility", "author-ready variants must be physically compatible with the containing machine definition", errors)
				_expect(isinstance(driver.get("variant_notes"), str) and bool(driver["variant_notes"].strip()), f"$.drivers[{index}].variant_notes", "author-ready variants must explain their physical impact", errors)
	sources = definition.get("sources")
	_expect(isinstance(sources, list) and bool(sources), "$.sources", "must contain at least one source", errors)
	source_ids: set[str] = set()
	source_by_id: dict[str, dict[str, Any]] = {}
	if isinstance(sources, list):
		for index, source in enumerate(sources):
			if not isinstance(source, dict):
				errors.append(f"$.sources[{index}]: must be an object")
				continue
			source_id = source.get("id")
			_validate_identifier(source_id, f"$.sources[{index}].id", errors)
			if isinstance(source_id, str):
				if source_id in source_ids:
					errors.append(f"$.sources[{index}].id: duplicate source ID {source_id}")
				source_ids.add(source_id)
				source_by_id[source_id] = source
			if source.get("kind") in {"vpx_script", "manual", "service_bulletin"}:
				_expect(bool(source.get("license")), f"$.sources[{index}].license", "required for community scripts and documents", errors)
				_expect(bool(source.get("attribution")), f"$.sources[{index}].attribution", "required for community scripts and documents", errors)
			_validate_excerpts(source, f"$.sources[{index}]", repository_root, errors)
			for field, value in source.items():
				_expect(not isinstance(value, str) or not LOCAL_L_DRIVE_PATTERN.search(value), f"$.sources[{index}].{field}", "canonical machine sources cannot store local L: paths", errors)
	device_ids: set[str] = set()
	spatial_placement_ids: set[str] = set()
	bindings: set[tuple[str, int, int | None]] = set()
	physical_output_connections: dict[tuple[str, str], str] = {}
	sam_game_on_outputs: list[tuple[str, dict[str, Any]]] = []
	for collection_name in ("inputs", "outputs"):
		collection = definition.get(collection_name)
		_expect(isinstance(collection, list), f"$.{collection_name}", "must be an array", errors)
		if not isinstance(collection, list):
			continue
		for index, device in enumerate(collection):
			path = f"$.{collection_name}[{index}]"
			if not isinstance(device, dict):
				errors.append(f"{path}: must be an object")
				continue
			device_id = device.get("id")
			_validate_identifier(device_id, f"{path}.id", errors)
			if isinstance(device_id, str):
				if device_id in device_ids:
					errors.append(f"{path}.id: duplicate device ID {device_id}")
				device_ids.add(device_id)
			label = device.get("label")
			_expect(isinstance(label, str) and bool(label.strip()), f"{path}.label", "must be non-empty", errors)
			if status == "author_ready" and isinstance(label, str):
				_expect(not GENERIC_LABEL_PATTERN.fullmatch(label.strip()), f"{path}.label", "generic generated label is forbidden in author-ready definitions", errors)
				_expect(device.get("availability") in {"used", "unused", "optional"}, f"{path}.availability", "author-ready devices must declare used, unused, or optional", errors)
				if collection_name == "inputs" and device.get("kind") == "switch" and device.get("availability") in {"used", "optional"}:
					_expect(isinstance(device.get("normally_closed"), bool), f"{path}.normally_closed", "used and optional physical switches require physical contact polarity", errors)
			binding = device.get("binding")
			if isinstance(binding, dict) and isinstance(binding.get("group"), str) and isinstance(binding.get("device"), int):
				binding_key = (binding["group"], binding["device"], binding.get("channel"))
				if binding_key in bindings:
					errors.append(f"{path}.binding: duplicate controller binding {binding_key}")
				bindings.add(binding_key)
			else:
				errors.append(f"{path}.binding: group and integer device are required")
			if collection_name == "outputs" and status == "author_ready" and isinstance(binding, dict) and binding.get("group") == "pinmame.output.solenoid" and device.get("kind") != "virtual" and device.get("availability") in {"used", "optional"}:
				wiring = device.get("wiring")
				if isinstance(wiring, dict) and isinstance(wiring.get("board"), str) and isinstance(wiring.get("control_connection"), str):
					connection = (wiring["board"], wiring["control_connection"])
					if connection in physical_output_connections:
						errors.append(f"{path}.wiring.control_connection: duplicates physical output connection used by {physical_output_connections[connection]}")
					else:
						physical_output_connections[connection] = str(device_id)
			if collection_name == "outputs" and definition.get("controller", {}).get("platform") == "pinmame.sam" and isinstance(binding, dict) and binding.get("group") == "pinmame.output.solenoid" and binding.get("device") == 33:
				sam_game_on_outputs.append((path, device))
			provenance = device.get("provenance")
			if not isinstance(provenance, dict):
				errors.append(f"{path}.provenance: must be an object")
			else:
				refs = provenance.get("source_refs")
				_expect(isinstance(refs, list) and bool(refs), f"{path}.provenance.source_refs", "must contain a source reference", errors)
				if isinstance(refs, list):
					for source_ref in refs:
						_expect(source_ref in source_ids, f"{path}.provenance.source_refs", f"unknown source reference {source_ref!r}", errors)
				if status == "author_ready":
					_expect(provenance.get("status") == "validated", f"{path}.provenance.status", "author-ready device assertions must be validated", errors)
			_validate_spatial(device, collection_name, path, status, source_ids, spatial_placement_ids, errors)
	_validate_shared_rgb_emitters(definition.get("outputs"), errors)
	if status == "author_ready" and definition.get("controller", {}).get("platform") == "pinmame.sam":
		_expect(len(sam_game_on_outputs) == 1, "$.outputs", "author-ready SAM definition must declare public solenoid 33 exactly once as PinMAME's synthetic game-on state", errors)
		for path, output in sam_game_on_outputs:
			_expect(output.get("kind") == "virtual", f"{path}.kind", "SAM public solenoid 33 is the synthetic game-on state, never a physical device", errors)
			_expect("wiring" not in output, f"{path}.wiring", "SAM synthetic game-on state cannot have physical wiring", errors)
	knowledge = definition.get("knowledge")
	if isinstance(knowledge, dict):
		knowledge_path = knowledge.get("path")
		if status == "author_ready":
			_expect(knowledge.get("status") == "complete", "$.knowledge.status", "author-ready knowledge must be complete", errors)
		if repository_root is not None and isinstance(knowledge_path, str):
			parts = PurePosixPath(knowledge_path).parts
			_expect(".." not in parts and bool(parts) and parts[0] == "knowledge", "$.knowledge.path", "must remain under knowledge/", errors)
			if ".." not in parts and parts and parts[0] == "knowledge":
				_expect((repository_root.joinpath(*parts)).is_file(), "$.knowledge.path", f"referenced note does not exist: {knowledge_path}", errors)
	else:
		errors.append("$.knowledge: must be an object")
	mechanisms = definition.get("mechanisms")
	if isinstance(mechanisms, list):
		mechanism_ids: set[str] = set()
		actuator_owners: dict[str, str] = {}
		for index, mechanism in enumerate(mechanisms):
			path = f"$.mechanisms[{index}]"
			if not isinstance(mechanism, dict):
				errors.append(f"{path}: must be an object")
				continue
			mechanism_id = mechanism.get("id")
			_validate_identifier(mechanism_id, f"{path}.id", errors)
			if isinstance(mechanism_id, str):
				if mechanism_id in mechanism_ids or mechanism_id in device_ids:
					errors.append(f"{path}.id: duplicate identifier {mechanism_id}")
				mechanism_ids.add(mechanism_id)
			for role in ("actuators", "sensors"):
				refs = mechanism.get(role)
				_expect(isinstance(refs, list), f"{path}.{role}", "must be an array", errors)
				if isinstance(refs, list):
					for ref in refs:
						_expect(ref in device_ids, f"{path}.{role}", f"unknown device reference {ref!r}", errors)
						if role == "actuators" and isinstance(ref, str):
							if ref in actuator_owners:
								errors.append(f"{path}.actuators: actuator {ref!r} is already owned by {actuator_owners[ref]!r}")
							else:
								actuator_owners[ref] = str(mechanism_id)
			for position_index, position in enumerate(mechanism.get("positions", [])):
				if not isinstance(position, dict):
					continue
				for ref in position.get("sensors", []):
					_expect(ref in device_ids, f"{path}.positions[{position_index}].sensors", f"unknown device reference {ref!r}", errors)
			provenance = mechanism.get("provenance")
			if isinstance(provenance, dict):
				mechanism_source_refs = provenance.get("source_refs", [])
				for source_ref in mechanism_source_refs:
					_expect(source_ref in source_ids, f"{path}.provenance.source_refs", f"unknown source reference {source_ref!r}", errors)
				if status == "author_ready":
					_expect(provenance.get("status") == "validated", f"{path}.provenance.status", "author-ready mechanism assertions must be validated", errors)
					causality_sources = [source_by_id[source_ref] for source_ref in mechanism_source_refs if source_ref in source_by_id]
					_expect(
						any(evidence_priority("mechanism_causality", EvidenceAssertion(None, str(source.get("id")), str(source.get("kind")), bool(source.get("known_working")))) > 0 for source in causality_sources),
						f"{path}.provenance.source_refs",
						"author-ready mechanism requires evidence with mechanism-causality authority",
						errors,
					)
			else:
				errors.append(f"{path}.provenance: must be an object")
	displays = definition.get("displays")
	display_ids: set[str] = set()
	displays_by_id: dict[str, dict[str, Any]] = {}
	if isinstance(displays, list):
		for index, display in enumerate(displays):
			path = f"$.displays[{index}]"
			if not isinstance(display, dict):
				continue
			display_id = display.get("id")
			_validate_identifier(display_id, f"{path}.id", errors)
			if isinstance(display_id, str):
				if display_id in display_ids:
					errors.append(f"{path}.id: duplicate display ID {display_id!r}")
				display_ids.add(display_id)
				displays_by_id[display_id] = display
			if "segment_start" in display:
				_expect(display.get("kind") == "segment", f"{path}.segment_start", "is only valid for segment displays", errors)
			provenance = display.get("provenance")
			if not isinstance(provenance, dict):
				errors.append(f"{path}.provenance: must be an object")
				continue
			for source_ref in provenance.get("source_refs", []):
				_expect(source_ref in source_ids, f"{path}.provenance.source_refs", f"unknown source reference {source_ref!r}", errors)
			if status == "author_ready":
				_expect(provenance.get("status") == "validated", f"{path}.provenance.status", "author-ready display assertions must be validated", errors)
				if display.get("kind") in {"dmd", "video"}:
					_expect(isinstance(display.get("width"), int) and isinstance(display.get("height"), int), path, "pixel displays require width and height", errors)
				elif display.get("kind") == "segment":
					_expect(
						all(isinstance(display.get(field), int) for field in ("controller_index", "segment_start", "width")),
						path,
						"segment displays require controller_index, segment_start, and width",
						errors,
					)
			_validate_spatial(display, "displays", path, status, source_ids, spatial_placement_ids, errors)
	if isinstance(drivers, list):
		for driver_index, driver in enumerate(drivers):
			if not isinstance(driver, dict):
				continue
			path = f"$.drivers[{driver_index}]"
			if driver.get("physical_compatibility") == "identical" and "display_overrides" in driver:
				errors.append(f"{path}.display_overrides: physically identical drivers cannot carry display overrides")
			overrides = driver.get("display_overrides")
			if overrides is None:
				continue
			_expect(isinstance(overrides, list), f"{path}.display_overrides", "must be an array", errors)
			if not isinstance(overrides, list):
				continue
			targets: set[str] = set()
			for override_index, override in enumerate(overrides):
				override_path = f"{path}.display_overrides[{override_index}]"
				if not isinstance(override, dict):
					errors.append(f"{override_path}: must be an object")
					continue
				target = override.get("target")
				_validate_identifier(target, f"{override_path}.target", errors)
				_expect(isinstance(target, str) and target in display_ids, f"{override_path}.target", "must resolve to a canonical display ID", errors)
				if isinstance(target, str):
					if target in targets:
						errors.append(f"{override_path}.target: duplicate display override target {target!r}")
					targets.add(target)
				_expect(
					any(field in override for field in ("controller_index", "segment_start", "width", "height")),
					override_path,
					"must override at least one of controller_index, segment_start, width, or height",
					errors,
				)
				if isinstance(target, str) and target in displays_by_id:
					canonical_display = displays_by_id[target]
					if "segment_start" in override:
						_expect(canonical_display.get("kind") == "segment", f"{override_path}.segment_start", "is only valid for segment displays", errors)
					_expect(
						any(
							field in override and override[field] != canonical_display.get(field)
							for field in ("controller_index", "segment_start", "width", "height")
						),
						override_path,
						"must change at least one canonical display value",
						errors,
					)
				_validate_provenance_refs(override.get("provenance"), f"{override_path}.provenance", source_ids, errors)
				if status == "author_ready":
					provenance = override.get("provenance")
					_expect(
						isinstance(provenance, dict) and provenance.get("status") == "validated",
						f"{override_path}.provenance.status",
						"author-ready display override provenance must be validated",
						errors,
					)
	if status == "author_ready":
		_expect(bool(definition.get("inputs")), "$.inputs", "author-ready definition requires a complete input inventory", errors)
		_expect(bool(definition.get("outputs")), "$.outputs", "author-ready definition requires a complete output inventory", errors)
		_expect(bool(definition.get("displays")), "$.displays", "author-ready definition requires a display inventory", errors)
		_expect(bool(definition.get("mechanisms")), "$.mechanisms", "author-ready definition requires a mechanism inventory", errors)
		_expect(not definition.get("conflicts"), "$.conflicts", "author-ready definition cannot have unresolved conflicts", errors)
	return errors


def _address_allowed(address: int, rules: list[dict[str, Any]]) -> bool:
	for rule in rules:
		values = rule.get("values")
		if isinstance(values, list) and address in values:
			return True
		minimum, maximum = rule.get("minimum"), rule.get("maximum")
		if isinstance(minimum, int) and isinstance(maximum, int) and minimum <= address <= maximum:
			return True
	return False


def validate_controller_profile(profile: dict[str, Any]) -> list[str]:
	errors: list[str] = []
	groups = profile.get("groups")
	if not isinstance(groups, list):
		return ["$.groups: must be an array"]
	group_ids: set[str] = set()
	plugin_routes: set[tuple[str, int]] = set()
	for index, group in enumerate(groups):
		path = f"$.groups[{index}]"
		if not isinstance(group, dict):
			continue
		group_id = group.get("id")
		if isinstance(group_id, str):
			if group_id in group_ids:
				errors.append(f"{path}.id: duplicate group ID {group_id!r}")
			group_ids.add(group_id)
		for rule_index, rule in enumerate(group.get("address_rules", [])):
			if isinstance(rule, dict) and "minimum" in rule and "maximum" in rule:
				_expect(rule["minimum"] <= rule["maximum"], f"{path}.address_rules[{rule_index}]", "minimum must not exceed maximum", errors)
		plugin = group.get("transports", {}).get("controller_plugin")
		if isinstance(plugin, dict) and isinstance(plugin.get("group_id"), int):
			route = (str(group.get("direction")), plugin["group_id"])
			if route in plugin_routes:
				errors.append(f"{path}.transports.controller_plugin.group_id: duplicate route in direction {route[0]!r}")
			plugin_routes.add(route)
	return errors


def _load_controller_profiles(repository_root: Path, errors: list[str]) -> dict[str, dict[str, Any]]:
	profiles: dict[str, dict[str, Any]] = {}
	for path in sorted((repository_root / "controllers").glob("**/*.json")):
		relative_path = path.relative_to(repository_root).as_posix()
		profile = load_json(path)
		errors.extend(validate_against_schema(profile, repository_root / "schemas" / "controller.schema.json", relative_path))
		for error in validate_controller_profile(profile):
			errors.append(f"{relative_path} {error}")
		profile_id = profile.get("id")
		if isinstance(profile_id, str):
			if profile_id in profiles:
				errors.append(f"{relative_path}: duplicate controller profile ID {profile_id!r}")
			profiles[profile_id] = profile
	return profiles


def _validate_machine_controller_bindings(definition: dict[str, Any], relative_path: str, profiles: dict[str, dict[str, Any]], errors: list[str]) -> None:
	controller_id = definition.get("controller", {}).get("platform")
	status = definition.get("coverage", {}).get("status")
	profile = profiles.get(controller_id)
	if profile is None:
		if status == "author_ready":
			errors.append(f"{relative_path} $.controller.platform: author-ready definition requires a controller profile for {controller_id!r}")
		return
	groups = {group["id"]: group for group in profile.get("groups", []) if isinstance(group, dict) and isinstance(group.get("id"), str)}
	for collection_name in ("inputs", "outputs"):
		for index, device in enumerate(definition.get(collection_name, [])):
			if not isinstance(device, dict):
				continue
			binding = device.get("binding")
			if not isinstance(binding, dict):
				continue
			group_id, address = binding.get("group"), binding.get("device")
			group = groups.get(group_id)
			path = f"{relative_path} $.{collection_name}[{index}].binding"
			if group is None:
				errors.append(f"{path}.group: {group_id!r} is not declared by controller profile {controller_id!r}")
			elif status == "author_ready" and isinstance(address, int) and not _address_allowed(address, group.get("address_rules", [])):
				errors.append(f"{path}.device: address {address} is outside controller group {group_id!r}")


def _validate_runtime_observations(evidence: dict[str, Any], relative_path: str, definitions_by_machine: dict[str, dict[str, Any]], errors: list[str]) -> None:
	observations = evidence.get("runtime", {}).get("observations")
	if not isinstance(observations, dict):
		return
	observation_groups = {
		"solenoid_addresses_seen": "pinmame.output.solenoid",
		"lamp_addresses_seen": "pinmame.output.lamp",
		"gi_addresses_seen": "pinmame.output.gi",
	}
	for machine_id in evidence.get("machine_ids", []):
		definition = definitions_by_machine.get(machine_id)
		if definition is None:
			errors.append(f"{relative_path} $.machine_ids: runtime evidence references unknown machine {machine_id!r}")
			continue
		if definition.get("coverage", {}).get("status") != "author_ready":
			continue
		declared: dict[str, set[int]] = {group: set() for group in observation_groups.values()}
		for output in definition.get("outputs", []):
			if not isinstance(output, dict):
				continue
			binding = output.get("binding")
			if isinstance(binding, dict) and binding.get("group") in declared and isinstance(binding.get("device"), int):
				declared[binding["group"]].add(binding["device"])
		for observation_name, group in observation_groups.items():
			for address in observations.get(observation_name, []):
				if address not in declared[group]:
					errors.append(f"{relative_path} $.runtime.observations.{observation_name}: address {address} is not declared in {machine_id!r} group {group!r}")
		for snapshot_index, snapshot in enumerate(observations.get("diagnostic_snapshots", [])):
			for address in snapshot.get("active_solenoid_addresses", []):
				if address not in declared["pinmame.output.solenoid"]:
					errors.append(f"{relative_path} $.runtime.observations.diagnostic_snapshots[{snapshot_index}].active_solenoid_addresses: address {address} is not declared in {machine_id!r} group 'pinmame.output.solenoid'")


def validate_catalog(catalog: dict[str, Any], repository_root: Path) -> list[str]:
	errors: list[str] = []
	_expect(catalog.get("format") == "pinmame-driver-catalog", "$.format", "must equal pinmame-driver-catalog", errors)
	_expect(catalog.get("schema_version") == 1, "$.schema_version", "must equal 1", errors)
	drivers = catalog.get("drivers")
	machines = catalog.get("machines")
	summary = catalog.get("summary")
	_expect(isinstance(drivers, list) and bool(drivers), "$.drivers", "must contain drivers", errors)
	_expect(isinstance(machines, list) and bool(machines), "$.machines", "must contain machines", errors)
	_expect(isinstance(summary, dict), "$.summary", "must be an object", errors)
	if not isinstance(drivers, list) or not isinstance(machines, list):
		return errors
	driver_records = {record.get("id"): record for record in drivers if isinstance(record, dict)}
	_expect(len(driver_records) == len(drivers), "$.drivers", "driver IDs must be unique and non-null", errors)
	for driver_id in sorted(OUT_OF_SCOPE_DRIVER_IDS & set(driver_records)):
		errors.append(f"$.drivers: custom-ROM-only virtual driver {driver_id!r} is outside the physical-machine scope")
	abstract_parents = catalog.get("abstract_parents")
	_expect(isinstance(abstract_parents, list), "$.abstract_parents", "must be an array", errors)
	abstract_parent_ids = {parent.get("id") for parent in abstract_parents if isinstance(parent, dict)} if isinstance(abstract_parents, list) else set()
	machine_records = {record.get("id"): record for record in machines if isinstance(record, dict)}
	_expect(len(machine_records) == len(machines), "$.machines", "machine IDs must be unique and non-null", errors)
	processing_orders = [record.get("processing_order") for record in machines if isinstance(record, dict)]
	_unique(processing_orders, "$.machines[].processing_order", errors)
	_expect(sorted(order for order in processing_orders if isinstance(order, int)) == list(range(1, len(machines) + 1)), "$.machines[].processing_order", "must be a contiguous 1-based queue", errors)
	definition_driver_sets: dict[str, set[str]] = {}
	for index, record in enumerate(drivers):
		if not isinstance(record, dict):
			errors.append(f"$.drivers[{index}]: must be an object")
			continue
		driver_id = record.get("id")
		clone_of = record.get("clone_of")
		if clone_of is not None:
			_expect(clone_of in driver_records or clone_of in abstract_parent_ids, f"$.drivers[{index}].clone_of", f"missing parent or abstract container {clone_of!r}", errors)
		machine_id = record.get("machine_id")
		_expect(machine_id in machine_records, f"$.drivers[{index}].machine_id", f"missing machine {machine_id!r}", errors)
		definition_path = record.get("definition")
		if isinstance(definition_path, str):
			parts = PurePosixPath(definition_path).parts
			if ".." in parts or not parts or parts[0] != "machines":
				errors.append(f"$.drivers[{index}].definition: path must remain under machines/")
				continue
			path = repository_root.joinpath(*parts)
			if not path.is_file():
				errors.append(f"$.drivers[{index}].definition: missing file {definition_path}")
				continue
			definition = load_json(path)
			_expect(definition.get("machine", {}).get("id") == machine_id, f"$.drivers[{index}].machine_id", "does not match definition machine ID", errors)
			_expect(definition.get("coverage", {}).get("status") == record.get("coverage_status"), f"$.drivers[{index}].coverage_status", "does not match definition", errors)
			_expect(content_sha256(definition) == record.get("definition_sha256"), f"$.drivers[{index}].definition_sha256", "does not match canonical definition content", errors)
			if definition_path not in definition_driver_sets:
				definition_driver_sets[definition_path] = {driver.get("id") for driver in definition.get("drivers", []) if isinstance(driver, dict)}
	for index, machine in enumerate(machines):
		if not isinstance(machine, dict):
			continue
		count = sum(1 for driver in drivers if isinstance(driver, dict) and driver.get("machine_id") == machine.get("id"))
		_expect(count == machine.get("driver_count"), f"$.machines[{index}].driver_count", f"expected {count}", errors)
		root_drivers = machine.get("root_drivers")
		_expect(isinstance(root_drivers, list) and bool(root_drivers), f"$.machines[{index}].root_drivers", "must contain at least one clone-tree root", errors)
		if isinstance(root_drivers, list):
			_unique(root_drivers, f"$.machines[{index}].root_drivers", errors)
			for root_driver in root_drivers:
				_expect(root_driver in driver_records, f"$.machines[{index}].root_drivers", f"unknown root driver {root_driver!r}", errors)
		definition_path = machine.get("definition")
		if isinstance(definition_path, str) and definition_path in definition_driver_sets:
			catalog_driver_ids = {driver.get("id") for driver in drivers if isinstance(driver, dict) and driver.get("machine_id") == machine.get("id")}
			_expect(definition_driver_sets[definition_path] == catalog_driver_ids, f"$.machines[{index}].definition", "definition driver set does not exactly match the catalog mapping", errors)
	if isinstance(summary, dict):
		_expect(summary.get("driver_count") == len(drivers), "$.summary.driver_count", f"expected {len(drivers)}", errors)
		_expect(summary.get("machine_count") == len(machines), "$.summary.machine_count", f"expected {len(machines)}", errors)
		game_count = sum(machine.get("machine_kind", "unknown") not in {"diagnostic_software", "system_software"} for machine in machines if isinstance(machine, dict))
		_expect(summary.get("game_count") == game_count, "$.summary.game_count", f"expected {game_count}", errors)
		_expect(summary.get("non_game_count") == len(machines) - game_count, "$.summary.non_game_count", f"expected {len(machines) - game_count}", errors)
		status_counts = Counter(machine.get("coverage_status") for machine in machines if isinstance(machine, dict))
		for status in ("stub", "partial", "author_ready"):
			_expect(summary.get(f"{status}_count") == status_counts[status], f"$.summary.{status}_count", f"expected {status_counts[status]}", errors)
	return errors


SPATIAL_AUDIT_FORMAT = "pinmame-spatial-audit"
SPATIAL_BLOCKERS_FORMAT = "pinmame-spatial-blockers"


def _validate_spatial_reports(
	repository_root: Path,
	definitions_by_machine: dict[str, dict[str, Any]],
	errors: list[str],
) -> None:
	"""Check the envelope of every report under reports/spatial and its agreement with the machine.

	Two report purposes exist and each has its own format identifier. An audit justifies a promotion
	and may only describe an author-ready machine; a blocker report explains why a machine cannot be
	promoted and may only describe one that is not author-ready. Without this a report can claim a
	promotion its own definition contradicts, which is exactly the kind of drift the reports exist to
	prevent.
	"""
	spatial_root = repository_root / "reports" / "spatial"
	if not spatial_root.is_dir():
		return
	schema_path = repository_root / "schemas" / "spatial-report.schema.json"
	for path in sorted(spatial_root.glob("**/*.json")):
		relative_path = path.relative_to(repository_root).as_posix()
		report = load_json(path)
		errors.extend(validate_against_schema(report, schema_path, relative_path))
		machine_id = report.get("machine_id")
		if not isinstance(machine_id, str):
			continue
		definition = definitions_by_machine.get(machine_id)
		if definition is None:
			errors.append(f"{relative_path} $.machine_id: does not resolve to a machine definition")
			continue
		status = definition.get("coverage", {}).get("status")
		report_format = report.get("format")
		if report_format == SPATIAL_AUDIT_FORMAT:
			_expect(
				status == "author_ready",
				f"{relative_path} $.format",
				f"a spatial audit describes a promotion, but {machine_id} is {status!r}; use {SPATIAL_BLOCKERS_FORMAT}",
				errors,
			)
		elif report_format == SPATIAL_BLOCKERS_FORMAT:
			_expect(
				status != "author_ready",
				f"{relative_path} $.format",
				f"a blocker report describes an unpromotable machine, but {machine_id} is author_ready; use {SPATIAL_AUDIT_FORMAT}",
				errors,
			)


def validate_repository(repository_root: Path) -> list[str]:
	errors: list[str] = check_schema_documents(repository_root)
	controller_profiles = _load_controller_profiles(repository_root, errors)
	catalog_path = repository_root / "catalog" / "pinmame.json"
	if not catalog_path.is_file():
		return [f"{catalog_path}: catalog is missing"]
	catalog = load_json(catalog_path)
	errors.extend(validate_against_schema(catalog, repository_root / "schemas" / "catalog.schema.json", "catalog/pinmame.json"))
	errors.extend(validate_catalog(catalog, repository_root))
	referenced_definition_paths = {record.get("definition") for record in catalog.get("machines", []) if isinstance(record, dict) and isinstance(record.get("definition"), str)}
	definition_paths = sorted((repository_root / "machines").glob("**/*.json"))
	definitions_by_machine: dict[str, dict[str, Any]] = {}
	for path in definition_paths:
		definition = load_json(path)
		machine_id = definition.get("machine", {}).get("id")
		if isinstance(machine_id, str):
			definitions_by_machine[machine_id] = definition
		relative_path = path.relative_to(repository_root).as_posix()
		if relative_path not in referenced_definition_paths:
			errors.append(f"{relative_path}: definition is not reachable from the catalog")
		status = definition.get("coverage", {}).get("status")
		expected_directory = {"stub": "machines/stubs/", "partial": "machines/partial/", "author_ready": "machines/author-ready/"}.get(status)
		if expected_directory is not None and not relative_path.startswith(expected_directory):
			errors.append(f"{relative_path}: {status} definitions must live under {expected_directory}")
		errors.extend(validate_against_schema(definition, repository_root / "schemas" / "machine.schema.json", relative_path))
		for error in validate_machine(definition, repository_root):
			errors.append(f"{relative_path} {error}")
		_validate_machine_controller_bindings(definition, relative_path, controller_profiles, errors)
	for path in sorted((repository_root / "evidence").glob("**/*.json")):
		relative_path = path.relative_to(repository_root).as_posix()
		evidence = load_json(path)
		if evidence.get("format") == "pinmame-vpx-candidate-register":
			evidence_schema = repository_root / "schemas" / "vpx-candidate-register.schema.json"
		elif evidence.get("format") == "pinmame-vpx-spatial-candidate-register":
			evidence_schema = repository_root / "schemas" / "vpx-spatial-candidate-register.schema.json"
		elif evidence.get("format") == "pinmame-vpx-spatial-candidates":
			evidence_schema = repository_root / "schemas" / "vpx-spatial-candidates.schema.json"
		else:
			evidence_schema = repository_root / "schemas" / "evidence.schema.json"
		errors.extend(validate_against_schema(evidence, evidence_schema, relative_path))
		if evidence.get("format") in {"pinmame-vpx-candidate-register", "pinmame-vpx-spatial-candidate-register"}:
			continue
		evidence_driver_ids = evidence.get("driver_ids")
		if isinstance(evidence_driver_ids, list):
			for driver_id in sorted(OUT_OF_SCOPE_DRIVER_IDS & {driver_id for driver_id in evidence_driver_ids if isinstance(driver_id, str)}):
				errors.append(f"{relative_path} $.driver_ids: custom-ROM-only virtual driver {driver_id!r} is outside the physical-machine scope")
		_validate_runtime_observations(evidence, relative_path, definitions_by_machine, errors)
	_validate_spatial_reports(repository_root, definitions_by_machine, errors)
	return errors


def require_valid_repository(repository_root: Path) -> None:
	errors = validate_repository(repository_root)
	if errors:
		raise ValidationError("\n".join(errors))
