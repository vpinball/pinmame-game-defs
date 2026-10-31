"""Validation for rom-maps/: supplemental firmware maps that extend Pinball Memory Maps documents.

A ROM map never feeds a machine definition, so its checks are about the map itself: the wrapper
schema, the embedded `memory_map` against the vendored upstream schema, identity against the
catalog, fail-closed evidence coverage, and the switch-timing rules a mode-replay recipe must obey.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

from .jsonio import load_json
from .schema_validation import validate_against_schema

ROM_MAPS_DIRECTORY = "rom-maps"
VENDOR_DIRECTORY = "_vendor"
REQUIRED_LICENCE_FILES = ("LICENSE-ODbL.md", "LICENSE-DbCL")


def _escape(token: str) -> str:
	return token.replace("~", "~0").replace("/", "~1")


def _resolve(document: Any, pointer: str) -> bool:
	node = document
	for raw in pointer.split("/")[1:]:
		token = raw.replace("~1", "/").replace("~0", "~")
		if isinstance(node, dict) and token in node:
			node = node[token]
		elif isinstance(node, list) and token.isdigit() and int(token) < len(node):
			node = node[int(token)]
		else:
			return False
	return True


def _memory_descriptors(value: Any, pointer: str) -> Iterator[str]:
	"""Every Pinball Memory Maps descriptor: an object carrying `encoding`, or a high-score entry."""
	if isinstance(value, dict):
		if "encoding" in value or "score" in value:
			yield pointer
			return
		for key, child in value.items():
			if not key.startswith("_"):
				yield from _memory_descriptors(child, f"{pointer}/{_escape(key)}")
	elif isinstance(value, list):
		for index, child in enumerate(value):
			yield from _memory_descriptors(child, f"{pointer}/{index}")


def _extension_items(extensions: dict[str, Any]) -> Iterator[str]:
	for key in extensions.get("mode_state", {}):
		yield f"/extensions/mode_state/{_escape(key)}"
	for index, _ in enumerate(extensions.get("replay_levels", [])):
		yield f"/extensions/replay_levels/{index}"
	for key in extensions.get("sound_commands", {}).get("commands", {}):
		yield f"/extensions/sound_commands/commands/{_escape(key)}"
	if "protocol" in extensions.get("sound_commands", {}):
		yield "/extensions/sound_commands/protocol"
	for key in ("timing", "mode_word", "ops"):
		if key in extensions.get("mode_replay", {}):
			yield f"/extensions/mode_replay/{key}"
	for index, _ in enumerate(extensions.get("mode_replay", {}).get("modes", [])):
		yield f"/extensions/mode_replay/modes/{index}"
	if extensions.get("notes"):
		yield "/extensions/notes"
	if "addressing" in extensions:
		yield "/extensions/addressing"


def _covered(pointer: str, evidence: dict[str, Any]) -> bool:
	candidate = pointer
	while candidate:
		if candidate in evidence:
			return True
		candidate = candidate.rsplit("/", 1)[0]
	return False


def _mode_replay_errors(replay: dict[str, Any], label: str) -> list[str]:
	errors: list[str] = []
	timing = replay.get("timing", {})
	minimum, same_gap = timing.get("min_closed_ms"), timing.get("same_switch_gap_ms")
	ops = replay.get("ops", {})
	identifiers = [mode.get("id") for mode in replay.get("modes", [])]
	for duplicate in sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1}):
		errors.append(f"{label} $.extensions.mode_replay.modes: duplicate mode id {duplicate!r}")
	for mode in replay.get("modes", []):
		steps = mode.get("steps", [])
		for index, step in enumerate(steps):
			where = f"{label} $.extensions.mode_replay.modes[{mode.get('id')}].steps[{index}]"
			if "sw" in step:
				hold = step.get("hold", timing.get("comfortable_closed_ms"))
				if hold is None:
					errors.append(f"{where}: hold or timing.comfortable_closed_ms is required")
				elif isinstance(minimum, int) and hold < minimum:
					errors.append(f"{where}: hold {hold} ms is below the ROM minimum {minimum} ms")
			elif step.get("op") not in ops:
				errors.append(f"{where}: op {step.get('op')!r} is not described in ops")

		# A second traversal covers every block boundary, regardless of repeat_block's size.
		elapsed = 0
		last_release: dict[int, int] = {}
		for _ in range(min(mode.get("repeat_block", 1), 2)):
			for index, step in enumerate(steps):
				where = f"{label} $.extensions.mode_replay.modes[{mode.get('id')}].steps[{index}]"
				gap = step.get("gap", 0)
				if "sw" in step:
					switch = step["sw"]
					if switch in last_release and isinstance(same_gap, int):
						span = elapsed - last_release[switch]
						if span < same_gap:
							error = f"{where}: switch {switch} repeats after {span} ms, under the {same_gap} ms same-switch gap"
							if error not in errors:
								errors.append(error)
					# A step may repeat when either RAM field is present; check its shortest
					# possible repetition without assuming an unknown RAM value.
					repeats_step = ("repeat_ram" in step or "repeat_until_zero" in step) and step.get("repeat_max", 2) > 1
					if repeats_step and isinstance(same_gap, int) and gap < same_gap:
						error = f"{where}: switch {switch} repeats after {gap} ms, under the {same_gap} ms same-switch gap"
						if error not in errors:
							errors.append(error)
					elapsed += step.get("hold", timing.get("comfortable_closed_ms", 0))
					last_release[switch] = elapsed
				# Mechanical op duration is unknown; only the declared gap is guaranteed.
				elapsed += gap
	return errors


def validate_rom_map(document: Any, label: str, repository_root: Path, drivers_by_machine: dict[str, set[str]]) -> list[str]:
	errors = validate_against_schema(document, repository_root / "schemas" / "rom-map.schema.json", label)
	if errors:
		return errors
	memory_map = document["memory_map"]
	upstream_schema = repository_root / ROM_MAPS_DIRECTORY / VENDOR_DIRECTORY / "map.schema.json"
	errors.extend(f"{label} memory_map: {error.split(' ', 1)[1]}" for error in validate_against_schema(memory_map, upstream_schema, label))

	machine_id = document["machine_id"]
	roms = document["roms"]
	known = drivers_by_machine.get(machine_id)
	if known is None:
		errors.append(f"{label} $.machine_id: {machine_id!r} is not a catalog machine")
	else:
		for rom in roms:
			if rom not in known:
				errors.append(f"{label} $.roms: {rom!r} is not a driver of {machine_id}")
	if memory_map.get("_metadata", {}).get("roms") != roms:
		errors.append(f"{label} $.memory_map._metadata.roms: must equal $.roms")

	source_ids = [source["id"] for source in document["sources"]]
	if len(source_ids) != len(set(source_ids)):
		errors.append(f"{label} $.sources: duplicate source id")
	evidence = document["evidence"]
	for pointer, entry in evidence.items():
		if not _resolve(document, pointer):
			errors.append(f"{label} $.evidence[{pointer!r}]: pointer resolves to nothing")
		for source in entry["sources"]:
			if source not in source_ids:
				errors.append(f"{label} $.evidence[{pointer!r}]: unknown source {source!r}")
		for field in ("verified_on", "applies_to"):
			for rom in entry.get(field, []):
				if rom not in roms:
					errors.append(f"{label} $.evidence[{pointer!r}].{field}: {rom!r} is not one of this map's roms")

	pointers = list(_memory_descriptors(memory_map, "/memory_map")) + list(_extension_items(document["extensions"]))
	for pointer in pointers:
		if not _covered(pointer, evidence):
			errors.append(f"{label} {pointer}: no evidence entry covers this descriptor")

	replay = document["extensions"].get("mode_replay")
	if replay:
		errors.extend(_mode_replay_errors(replay, label))
	return errors


def validate_rom_maps(repository_root: Path, catalog: dict[str, Any]) -> list[str]:
	directory = repository_root / ROM_MAPS_DIRECTORY
	if not directory.is_dir():
		return []
	errors: list[str] = []
	for name in REQUIRED_LICENCE_FILES:
		if not (directory / VENDOR_DIRECTORY / name).is_file():
			errors.append(f"{ROM_MAPS_DIRECTORY}/{VENDOR_DIRECTORY}/{name}: licence text is missing")
	if not (directory / "README.md").is_file():
		errors.append(f"{ROM_MAPS_DIRECTORY}/README.md: licence and attribution notice is missing")
	drivers_by_machine: dict[str, set[str]] = {}
	for driver in catalog.get("drivers", []):
		if isinstance(driver, dict) and isinstance(driver.get("machine_id"), str):
			drivers_by_machine.setdefault(driver["machine_id"], set()).add(driver["id"])
	seen: dict[tuple[str, str], str] = {}
	for path in sorted(directory.glob("**/*.json")):
		relative = path.relative_to(repository_root).as_posix()
		if VENDOR_DIRECTORY in path.relative_to(directory).parts:
			continue
		document = load_json(path)
		errors.extend(validate_rom_map(document, relative, repository_root, drivers_by_machine))
		if not isinstance(document, dict):
			continue
		machine_id, map_id = document.get("machine_id"), document.get("map_id")
		if isinstance(machine_id, str) and isinstance(map_id, str):
			slug = machine_id.split(".", 1)[-1].rsplit(".", 1)[0]
			year = machine_id.rsplit(".", 1)[-1]
			expected = f"{machine_id.split('.', 1)[0]}/{slug}-{year}.{map_id}.json"
			if relative != f"{ROM_MAPS_DIRECTORY}/{expected}":
				errors.append(f"{relative}: expected path {ROM_MAPS_DIRECTORY}/{expected}")
			if (machine_id, map_id) in seen:
				errors.append(f"{relative}: duplicates {seen[(machine_id, map_id)]}")
			seen[(machine_id, map_id)] = relative
	return errors
