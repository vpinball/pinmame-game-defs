from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from . import SCHEMA_VERSION
from .catalog import _source_record
from .errors import DefinitionError
from .identifiers import slug, unique_identifier
from .jsonio import load_json, write_json, write_text
from .registry import rebuild_catalog

TARGET_OVERRIDES = {
	"trn": "stern.tron-legacy.2011",
	"tron-legacy": "stern.tron-legacy.2011",
}
SOURCE_PARTITIONS = {
	"spiderman": {
		"sman_261": {"id": "stern.spider-man.2007", "name": "Spider-Man", "manufacturer": "Stern", "year": 2007},
		"smanve_101": {"id": "stern.spider-man-vault-edition.2016", "name": "Spider-Man Vault Edition", "manufacturer": "Stern", "year": 2016},
	},
}
PLATFORM_ALIASES = {
	"s11": "system11",
	"system11": "system11",
}
CHANNELS = {"red": 0, "green": 1, "blue": 2}
ROLE_BY_HINT = {
	"start game": "cabinet.start",
	"insert coin slot 1": "cabinet.coin.1",
	"insert coin slot 2": "cabinet.coin.2",
	"insert coin slot 3": "cabinet.coin.3",
	"insert coin slot 4": "cabinet.coin.4",
	"coin door cancel (wpc)": "service.cancel",
	"coin door down (wpc)": "service.down",
	"coin door up (wpc)": "service.up",
	"coin door enter (wpc)": "service.enter",
	"left flipper": "flipper.lower.left",
	"right flipper": "flipper.lower.right",
	"upper left flipper": "flipper.upper.left",
	"upper right flipper": "flipper.upper.right",
	"plunger": "cabinet.launch",
	"coin door open/close": "cabinet.coin-door",
}
HINT_KEYS = {"device_hint", "device_item_hint", "num_matches", "input_action_hint", "input_map_hint"}
MIGRATION_MISSING = [
	"identity",
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
]


# Words that qualify a device without changing which device it is. Device-class
# words are deliberately absent: a relay is not a button, and an end-of-stroke
# contact is not a button either, so `relay`, `solenoid` and `eos` all have to
# keep two labels apart.
_LABEL_NOISE = frozenset({"button", "lower", "plumb", "bob", "bracket", "with", "the", "a"})
_LABEL_SIDES = frozenset({"left", "right", "center", "upper"})
# Equivalences no amount of word overlap can see. Each pair is one device that a
# platform record and a game record simply name differently, and each is written
# out in full rather than reached by stripping words, so adding one is a
# deliberate act with a reviewable diff.
_LABEL_SYNONYMS: tuple[tuple[frozenset[str], frozenset[str]], ...] = (
	(frozenset({"rom", "started"}), frozenset({"game", "on", "relay"})),
	(frozenset({"rom", "started"}), frozenset({"game", "on", "solenoid"})),
	(frozenset({"rom", "started"}), frozenset({"game", "on", "gi", "relay"})),
	(frozenset({"rom", "started"}), frozenset({"gi", "relay"})),
	(frozenset({"start"}), frozenset({"credit"})),
)


def _label_words(label: str) -> list[str]:
	words = "".join(character if character.isalnum() else " " for character in label.lower()).split()
	# One spelling of centre, so `Center Pop Bumper` and `Centre Pop Bumper` do
	# not read as two opposing sides.
	return ["center" if word == "centre" else word for word in words]


def _names_one_device(first: str, second: str) -> bool:
	"""True when two labels are two names for the same device.

	The platform record carries generic cabinet labels and a game record carries
	its own, so the two disagree on wording constantly: `ROM Started` against
	`Game On Relay`, `Coin Button 1` against `Coin 1`, `Lower Right Flipper`
	against `Right Flipper`. None of those is a disagreement about the machine,
	and emitting a conflict for each produced dozens of records that no evidence
	could ever resolve because there was nothing to resolve.

	A genuine disagreement -- `Ball Roll Tilt` against `Drop Target 2` -- still
	returns False and still becomes a conflict.
	"""
	words_first = _label_words(first)
	words_second = _label_words(second)

	# The side test runs FIRST and can only ever return False. Side words are
	# stripped as noise below -- they do not distinguish a device from itself --
	# which means `Upper Left Flipper` and `Upper Right Flipper` reduce to the
	# same core and would merge on equality alone. Two devices on opposite sides
	# of the playfield are the single most likely real disagreement in this
	# corpus, so nothing may reach the equality check before this.
	sides_first = {word for word in words_first if word in _LABEL_SIDES}
	sides_second = {word for word in words_second if word in _LABEL_SIDES}
	if sides_first and sides_second and sides_first != sides_second:
		return False

	core_first = frozenset(word for word in words_first if word not in _LABEL_NOISE)
	core_second = frozenset(word for word in words_second if word not in _LABEL_NOISE)
	if core_first == core_second:
		return True

	# No subset rule. `Right Flipper Button` reduces to {flipper} and `Right
	# Flipper EOS` to {flipper, eos}; treating the first as a subset of the
	# second would merge a button with an end-of-stroke contact and delete a
	# real disagreement. Anything beyond exact equality has to be written out.
	return any(
		{core_first, core_second} == {left, right} for left, right in _LABEL_SYNONYMS
	)


def _conflict_resolution_path(group: str, device_number: int) -> str:
	"""The trailing `Resolution path:` clause of a generated label conflict.

	Every conflict this importer emits has the same shape: a legacy platform
	record's blanket cabinet/address map on one side and one game record's own
	label on the other, both claiming one public address. So the evidence that
	settles it is the same shape too, even though the decisive item differs by
	platform -- name all three rather than guess which one this machine needs.

	A conflict with no resolution path asks a future curator to rediscover the
	question before they can start on the answer, which is why the clause is
	generated here instead of being added by hand afterwards.
	"""
	return (
		f"Resolution path: this machine's own printed switch or solenoid table for {group} {device_number}, "
		"read against the pinned PinMAME driver's own address definitions for this game and the platform "
		"input-port declaration its hardware generation uses, since one side of this disagreement is a "
		"legacy platform record's blanket cabinet map and the other is one game's own label; failing that, "
		"a LibPinMAME harness trace against a legal ROM for this machine observing what the address does. "
		"Unresolved."
	)


def _repository_revision(repository_root: Path) -> str:
	try:
		result = subprocess.run(
			["git", "-C", str(repository_root), "rev-parse", "HEAD"],
			check=True,
			capture_output=True,
			text=True,
		)
	except (OSError, subprocess.CalledProcessError) as error:
		raise DefinitionError(f"Unable to resolve legacy repository revision: {error}") from error
	return result.stdout.strip().lower()


def _legacy_source(stem: str, document: dict[str, Any], revision: str) -> dict[str, Any]:
	origin = str(document.get("_source", {}).get("origin", "legacy-json"))
	kind = "vpe_csharp" if origin == "vpe-csharp" else "legacy_json"
	return {
		"id": f"legacy.game.{slug(stem)}",
		"kind": kind,
		"uri": "https://github.com/vpinball/pinmame-game-defs",
		"revision": revision,
		"locator": f"games/{stem}.json; origin={origin}",
		"attribution": "pinmame-game-defs contributors",
	}


def _platform_source(stem: str, revision: str) -> dict[str, Any]:
	return {
		"id": f"legacy.platform.{slug(stem)}",
		"kind": "legacy_json",
		"uri": "https://github.com/vpinball/pinmame-game-defs",
		"revision": revision,
		"locator": f"platforms/{stem}.json",
		"attribution": "pinmame-game-defs contributors",
	}


def _target_id(stem: str, document: dict[str, Any]) -> str:
	if stem in TARGET_OVERRIDES:
		return TARGET_OVERRIDES[stem]
	game = document.get("game", {})
	year = game.get("year")
	return f"{slug(game.get('manufacturer', 'unknown'))}.{slug(game.get('name', stem))}.{year if isinstance(year, int) else 'unknown'}"


def _source_partitions(
	stem: str,
	document: dict[str, Any],
	matched: set[str],
	drivers_by_id: dict[str, dict[str, Any]],
) -> list[tuple[str, dict[str, Any] | None, set[str]]]:
	partitions = SOURCE_PARTITIONS.get(stem)
	if partitions is None:
		return [(_target_id(stem, document), None, matched)]
	result: list[tuple[str, dict[str, Any] | None, set[str]]] = []
	for root_driver, identity in partitions.items():
		driver_ids = {driver_id for driver_id in matched if drivers_by_id[driver_id]["root_driver"] == root_driver}
		if driver_ids:
			result.append((identity["id"], identity, driver_ids))
	return result


def _match_source_drivers(
	stem: str,
	document: dict[str, Any],
	drivers_by_casefold: dict[str, dict[str, Any]],
	drivers: list[dict[str, Any]],
) -> tuple[set[str], list[str], str]:
	matched: set[str] = set()
	unmatched: list[str] = []
	roms = document.get("roms") or []
	for rom in roms:
		rom_id = str(rom.get("id", ""))
		record = drivers_by_casefold.get(rom_id.casefold())
		if record is None:
			unmatched.append(rom_id)
		else:
			matched.add(record["id"])
	if matched:
		return matched, unmatched, "declared_roms"
	game_id = str(document.get("game", {}).get("id", stem)).casefold()
	exact = drivers_by_casefold.get(game_id)
	if exact is not None:
		return {exact["id"]}, unmatched, "game_id"
	prefix_matches = [driver for driver in drivers if driver["id"].casefold().startswith(f"{game_id}_")]
	prefix_roots = {driver["root_driver"] for driver in prefix_matches}
	if prefix_matches and len(prefix_roots) == 1:
		return {prefix_matches[0]["id"]}, unmatched, "unique_prefix"
	return set(), unmatched, "unmatched"


def _aliases_by_target(document: dict[str, Any]) -> tuple[dict[tuple[str, str], int], dict[tuple[str, int], str]]:
	binding_by_alias: dict[tuple[str, str], int] = {}
	alias_by_binding: dict[tuple[str, int], str] = {}
	for alias in document.get("aliases", []) or []:
		if not isinstance(alias.get("id"), int) or not isinstance(alias.get("alias"), str):
			continue
		kind = str(alias.get("type", ""))
		binding_by_alias[(kind, alias["alias"])] = alias["id"]
		alias_by_binding[(kind, alias["id"])] = alias["alias"]
	return binding_by_alias, alias_by_binding


def _numeric_aliases(namespace: str, value: int) -> list[dict[str, str]]:
	values = [str(value)]
	if value >= 0:
		values.extend([f"{value:02d}", f"{value:03d}"])
	result = [{"namespace": f"pinmame.{namespace}", "value": str(value)}]
	result.extend({"namespace": f"vpe-legacy.{namespace}", "value": alias} for alias in dict.fromkeys(values))
	return result


def _merge_provenance(target: dict[str, Any], source_id: str) -> None:
	refs = target["provenance"]["source_refs"]
	if source_id not in refs:
		refs.append(source_id)
		refs.sort()


def _record_notes(notes: list[tuple[str, str]], locator: str, record: dict[str, Any]) -> None:
	for key, value in record.items():
		if key.startswith("_") and value not in (None, "", [], {}):
			serialized = json.dumps(value, ensure_ascii=False, sort_keys=True) if not isinstance(value, str) else value
			notes.append((f"{locator}.{key}", " ".join(serialized.split())))


class _DeviceBuilder:
	def __init__(self) -> None:
		self.inputs: list[dict[str, Any]] = []
		self.outputs: list[dict[str, Any]] = []
		self.conflicts: list[dict[str, Any]] = []
		self.notes: list[tuple[str, str]] = []
		self._occupied: set[str] = set()
		self._by_binding: dict[tuple[str, int, int | None], dict[str, Any]] = {}

	def add(
		self,
		*,
		collection: str,
		record: dict[str, Any],
		group: str,
		kind: str,
		prefix: str,
		source_id: str,
		locator: str,
		legacy_type: str,
		binding_by_alias: dict[tuple[str, str], int],
		alias_by_binding: dict[tuple[str, int], str],
		binding_value: object | None = None,
		channel: int | None = None,
	) -> dict[str, Any] | None:
		raw_value = record.get("id") if binding_value is None else binding_value
		if isinstance(raw_value, int):
			device_number = raw_value
		elif isinstance(raw_value, str):
			device_number = binding_by_alias.get((legacy_type, raw_value))
			if device_number is None:
				self.notes.append((locator, f"Unbound legacy {collection} record `{raw_value}` was retained as a migration note only."))
				_record_notes(self.notes, locator, record)
				return None
		else:
			self.notes.append((locator, "Legacy device has no usable signed numeric controller address."))
			return None
		label = str(record.get("description") or record.get("name") or f"{collection} {device_number}")
		binding_key = (group, device_number, channel)
		aliases = _numeric_aliases(legacy_type, device_number)
		legacy_alias = alias_by_binding.get((legacy_type, device_number))
		if legacy_alias:
			aliases.append({"namespace": f"vpe-legacy.{legacy_type}", "value": legacy_alias})
		if binding_key in self._by_binding:
			existing = self._by_binding[binding_key]
			_merge_provenance(existing, source_id)
			for alias in aliases:
				if alias not in existing["aliases"]:
					existing["aliases"].append(alias)
			if kind == "flasher" and existing.get("kind") == "coil":
				existing["kind"] = "flasher"
			if existing.get("label") != label and not _names_one_device(existing.get("label", ""), label):
				refs = existing["provenance"]["source_refs"]
				if len(refs) >= 2:
					self.conflicts.append(
						{
							"id": unique_identifier("conflict", f"{group}-{device_number}-{channel}", {conflict["id"] for conflict in self.conflicts}),
							"path": f"binding:{group}/{device_number}/{channel}",
							"description": f"Legacy sources disagree on label: {existing['label']!r} versus {label!r}. {_conflict_resolution_path(group, device_number)}",
							"source_refs": refs,
						}
					)
				else:
					self.notes.append((locator, f"Duplicate binding label candidate `{label}` differs from `{existing['label']}`."))
			_record_notes(self.notes, locator, record)
			return existing
		semantic_alias = alias_by_binding.get((legacy_type, device_number))
		semantic_label = semantic_alias[2:] if semantic_alias and semantic_alias[:2] in {"s_", "c_"} else label
		device_id = unique_identifier(prefix, semantic_label, self._occupied, device_number)
		device: dict[str, Any] = {
			"id": device_id,
			"label": label,
			"kind": kind,
			"binding": {"group": group, "device": device_number},
			"aliases": aliases,
			"provenance": {"status": "candidate", "source_refs": [source_id]},
		}
		if channel is not None:
			device["binding"]["channel"] = channel
		if collection == "inputs":
			if record.get("normally_closed") is not None:
				device["normally_closed"] = bool(record["normally_closed"])
			if record.get("pulse") is not None:
				device["pulse"] = bool(record["pulse"])
			hint = str(record.get("input_action_hint", "")).casefold()
			if hint in ROLE_BY_HINT:
				device["roles"] = [ROLE_BY_HINT[hint]]
			if record.get("constant_hint") is not None:
				device["kind"] = "constant"
				device["constant_active"] = str(record["constant_hint"]).casefold() in {"always_closed", "active", "on", "true"}
			self.inputs.append(device)
		else:
			if record.get("is_unused") is not None:
				device["availability"] = "unused" if record["is_unused"] else "used"
			if isinstance(record.get("fading_steps"), int):
				device["range"] = {"minimum": 0, "maximum": 1, "steps": record["fading_steps"]}
			self.outputs.append(device)
		self._by_binding[binding_key] = device
		_record_notes(self.notes, locator, record)
		return device

	def by_binding(self, group: str, number: int, channel: int | None = None) -> dict[str, Any] | None:
		return self._by_binding.get((group, number, channel))


def _output_kind(record: dict[str, Any], default: str) -> str:
	value = str(record.get("_inferred_type", "")).casefold()
	if "motor" in value:
		return "motor"
	if "magnet" in value:
		return "magnet"
	if "relay" in value:
		return "relay"
	return default


def _iter_mechanism_numbers(value: Any, keys: set[str]) -> Iterable[int]:
	if isinstance(value, dict):
		for key, nested in value.items():
			if key.casefold().lstrip("_") in keys and isinstance(nested, int):
				yield nested
			yield from _iter_mechanism_numbers(nested, keys)
	elif isinstance(value, list):
		for nested in value:
			yield from _iter_mechanism_numbers(nested, keys)


def _mechanisms(
	documents: list[tuple[str, dict[str, Any]]],
	builder: _DeviceBuilder,
	source_ids: dict[str, str],
) -> list[dict[str, Any]]:
	result: list[dict[str, Any]] = []
	occupied: set[str] = set()
	for stem, document in documents:
		for index, mechanism in enumerate(document.get("mechanisms", []) or []):
			if not isinstance(mechanism, dict):
				continue
			source_id = source_ids[stem]
			label = str(mechanism.get("description") or mechanism.get("name") or mechanism.get("id") or mechanism.get("type") or f"Mechanism {index + 1}")
			actuators: list[str] = []
			for number in dict.fromkeys(_iter_mechanism_numbers(mechanism, {"sol", "sol1", "sol2", "solenoid", "coil_id", "move_sol", "hat_sol"})):
				device = builder.by_binding("pinmame.output.solenoid", number)
				if device is not None:
					actuators.append(device["id"])
			sensors: list[str] = []
			for number in dict.fromkeys(_iter_mechanism_numbers(mechanism, {"sw", "switch", "id", "home_switch", "encoder_switch", "hit_switch"})):
				device = builder.by_binding("pinmame.input.switch", number)
				if device is not None:
					sensors.append(device["id"])
			kind_text = f"{mechanism.get('type', '')} {mechanism.get('mech_type', '')}".casefold()
			kind = "rotary" if "rot" in kind_text else "motorized" if "mech" in kind_text or actuators else "other"
			behavior_parts = [label]
			for key in ("_note", "mech_type", "_mech_type"):
				if mechanism.get(key):
					behavior_parts.append(str(mechanism[key]))
			result.append(
				{
					"id": unique_identifier("mechanism", mechanism.get("id") or mechanism.get("name") or label, occupied, index + 1),
					"label": label,
					"kind": kind,
					"actuators": list(dict.fromkeys(actuators)),
					"sensors": list(dict.fromkeys(sensors)),
					"behavior": " ".join(" ".join(part.split()) for part in behavior_parts),
					"provenance": {"status": "candidate", "source_refs": [source_id]},
				}
			)
			_record_notes(builder.notes, f"games/{stem}.json#/mechanisms/{index}", mechanism)
	return result


def _add_document_devices(
	stem: str,
	document: dict[str, Any],
	source_id: str,
	builder: _DeviceBuilder,
	locator_prefix: str,
) -> Counter[str]:
	binding_by_alias, alias_by_binding = _aliases_by_target(document)
	dropped: Counter[str] = Counter()
	for collection_name in ("switches", "coils", "lamps", "flashers", "gi", "gi_strings", "lamp_coils"):
		for index, record in enumerate(document.get(collection_name, []) or []):
			if not isinstance(record, dict):
				continue
			for key in HINT_KEYS:
				if key in record:
					dropped[key] += 1
			locator = f"{locator_prefix}#/{collection_name}/{index}"
			if collection_name == "switches":
				builder.add(collection="inputs", record=record, group="pinmame.input.switch", kind="switch", prefix="switch", source_id=source_id, locator=locator, legacy_type="switch", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding)
			elif collection_name == "coils":
				kind = "flasher" if record.get("is_lamp") else _output_kind(record, "coil")
				builder.add(collection="outputs", record=record, group="pinmame.output.solenoid", kind=kind, prefix="device", source_id=source_id, locator=locator, legacy_type="coil", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding)
			elif collection_name == "lamps":
				channel = CHANNELS.get(str(record.get("channel", "")).casefold())
				group = "pinmame.output.gi" if str(record.get("source", "")).casefold() == "gi" else "pinmame.output.lamp"
				kind = "rgb_lamp" if str(record.get("type", "")).casefold() == "rgb_multi" else "lamp"
				builder.add(collection="outputs", record=record, group=group, kind=kind, prefix="lamp", source_id=source_id, locator=locator, legacy_type="lamp", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding, channel=channel)
			elif collection_name == "flashers":
				builder.add(collection="outputs", record=record, group="pinmame.output.solenoid", kind="flasher", prefix="device", source_id=source_id, locator=locator, legacy_type="coil", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding, binding_value=record.get("coil_id"))
			elif collection_name in {"gi", "gi_strings"}:
				builder.add(collection="outputs", record=record, group="pinmame.output.gi", kind="gi", prefix="gi", source_id=source_id, locator=locator, legacy_type="gi", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding)
			elif collection_name == "lamp_coils":
				builder.add(collection="outputs", record=record, group="pinmame.output.lamp", kind=_output_kind(record, "coil"), prefix="device", source_id=source_id, locator=locator, legacy_type="lamp", binding_by_alias=binding_by_alias, alias_by_binding=alias_by_binding, binding_value=record.get("lamp_id"))
	return dropped


def _knowledge_markdown(
	identity: dict[str, Any],
	documents: list[tuple[str, dict[str, Any]]],
	mechanisms: list[dict[str, Any]],
	notes: list[tuple[str, str]],
	source_ids: dict[str, str],
) -> str:
	lines = [
		f"# {identity['name']}",
		"",
		"Coverage: **partial - source-derived recreation knowledge requiring validation**",
		"",
		"## Overview",
		"",
		f"Legacy evidence identifies this candidate as {identity['manufacturer']} ({identity.get('year') or 'year unknown'}). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.",
		"",
		"## Playfield devices",
		"",
		"Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.",
		"",
		"## Custom mechanisms",
		"",
	]
	if mechanisms:
		for mechanism in mechanisms:
			lines.append(f"- `{mechanism['id']}`: {mechanism['behavior']} [source: {', '.join(mechanism['provenance']['source_refs'])}]")
	else:
		lines.append("No custom mechanism conclusion has been validated. Manuals, schematics, PinMAME source, and gameplay evidence still need to be checked.")
	lines.extend(["", "## Ball-state transitions", "", "Ball paths, trough ordering, locks, kickouts, and causal transitions have not yet been normalized. Relevant source notes follow under Evidence notes.", "", "## Controller interactions", "", "Controller callbacks and bindings are candidate evidence only until reconciled against PinMAME and physical documentation.", "", "## Service and setup information", "", "Unknown; locate operator/service documentation.", "", "## Timing and tuning observations", "", "Source timing values may describe a particular VPX implementation rather than physical hardware and require review.", "", "## Recreation guidance", "", "Do not treat this partial definition as a complete authoring specification. Resolve every coverage requirement and conflict before promotion.", "", "## Evidence notes", ""])
	for locator, note in notes:
		lines.append(f"- `{locator}`: {note}")
	for stem, document in documents:
		confidence = document.get("_source", {}).get("confidence_notes")
		if confidence:
			lines.append(f"- `games/{stem}.json#/_source/confidence_notes`: {' '.join(str(confidence).split())}")
	lines.extend(["", "## Unresolved questions", "", "- Is the I/O enumeration complete for every supported physical/controller variant?", "- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?", "- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?", "", "## Sources", ""])
	for stem, _document in documents:
		lines.append(f"- `{source_ids[stem]}`: `games/{stem}.json` at the pinned migration revision.")
	return "\n".join(lines) + "\n"


def import_legacy_definitions(repository_root: Path) -> dict[str, Any]:
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	drivers = catalog["drivers"]
	drivers_by_id = {driver["id"]: driver for driver in drivers}
	drivers_by_casefold = {driver["id"].casefold(): driver for driver in drivers}
	drivers_by_root: dict[str, list[dict[str, Any]]] = defaultdict(list)
	for driver in drivers:
		drivers_by_root[driver["root_driver"]].append(driver)
	revision = _repository_revision(repository_root)
	sources: list[tuple[str, str, dict[str, Any], set[str], dict[str, Any] | None]] = []
	file_report: list[dict[str, Any]] = []
	for path in sorted((repository_root / "games").glob("*.json")):
		try:
			document = load_json(path)
		except (OSError, json.JSONDecodeError) as error:
			file_report.append({"file": path.name, "status": "invalid_json", "error": str(error)})
			continue
		stem = path.stem
		matched, unmatched, method = _match_source_drivers(stem, document, drivers_by_casefold, drivers)
		partitions = _source_partitions(stem, document, matched, drivers_by_id) if matched else []
		file_report.append({"file": path.name, "status": "matched" if matched else "outside_pinmame", "target_machine_ids": [target_id for target_id, _identity, _drivers in partitions], "match_method": method, "matched_drivers": sorted(matched), "unmatched_declared_roms": unmatched})
		if matched:
			for target_id, identity_override, partition_drivers in partitions:
				sources.append((target_id, stem, document, partition_drivers, identity_override))

	documents_by_target: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
	explicit_by_target: dict[str, set[str]] = defaultdict(set)
	identity_by_target: dict[str, dict[str, Any]] = {}
	for target_id, stem, document, matched, identity_override in sources:
		documents_by_target[target_id].append((stem, document))
		explicit_by_target[target_id].update(matched)
		if identity_override is not None:
			identity_by_target[target_id] = identity_override

	roots_by_target = {target: {drivers_by_id[driver_id]["root_driver"] for driver_id in explicit} for target, explicit in explicit_by_target.items()}
	targets_by_root: dict[str, set[str]] = defaultdict(set)
	for target, roots in roots_by_target.items():
		for root in roots:
			targets_by_root[root].add(target)
	assigned_by_target: dict[str, set[str]] = defaultdict(set)
	unresolved_split_drivers: list[dict[str, Any]] = []
	for target, explicit in explicit_by_target.items():
		assigned_by_target[target].update(explicit)
		for root in roots_by_target[target]:
			if len(targets_by_root[root]) == 1:
				assigned_by_target[target].update(driver["id"] for driver in drivers_by_root[root])
	for root, targets in sorted(targets_by_root.items()):
		if len(targets) <= 1:
			continue
		assigned = set().union(*(assigned_by_target[target] for target in targets))
		remaining = sorted(driver["id"] for driver in drivers_by_root[root] if driver["id"] not in assigned)
		if remaining:
			unresolved_split_drivers.append({"root_driver": root, "targets": sorted(targets), "unassigned_drivers": remaining})

	dropped_hints: Counter[str] = Counter()
	created: list[dict[str, Any]] = []
	for target_id, target_documents in sorted(documents_by_target.items()):
		ordered_documents = sorted(target_documents, key=lambda item: (item[1].get("_source", {}).get("origin") != "vpe-csharp", item[0]))
		identity_source = ordered_documents[0][1]
		game = identity_source["game"]
		identity_override = identity_by_target.get(target_id)
		identity: dict[str, Any] = dict(identity_override) if identity_override is not None else {"id": target_id, "name": game["name"], "manufacturer": game["manufacturer"], "year": game.get("year")}
		if identity_override is None and isinstance(game.get("ipdb_id"), int):
			identity["ipdb_id"] = game["ipdb_id"]
		source_records: list[dict[str, Any]] = [_source_record(catalog["source"]["pinmame_revision"])]
		source_ids: dict[str, str] = {}
		builder = _DeviceBuilder()
		seen_platforms: set[str] = set()
		for stem, document in ordered_documents:
			source = _legacy_source(stem, document, revision)
			source_records.append(source)
			source_ids[stem] = source["id"]
			platform = str(document.get("game", {}).get("platform", "")).casefold()
			platform_stem = PLATFORM_ALIASES.get(platform, platform)
			platform_path = repository_root / "platforms" / f"{platform_stem}.json"
			if platform_stem and platform_stem not in seen_platforms and platform_path.is_file():
				platform_document = load_json(platform_path)
				platform_source = _platform_source(platform_stem, revision)
				source_records.append(platform_source)
				dropped_hints.update(_add_document_devices(platform_stem, platform_document, platform_source["id"], builder, f"platforms/{platform_stem}.json"))
				seen_platforms.add(platform_stem)
			dropped_hints.update(_add_document_devices(stem, document, source["id"], builder, f"games/{stem}.json"))
		mechanisms = _mechanisms(ordered_documents, builder, source_ids)
		assigned_drivers = sorted(assigned_by_target[target_id])
		driver_definitions = []
		for driver_id in assigned_drivers:
			record = drivers_by_id[driver_id]
			driver_definition = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
			if record.get("clone_of") is not None:
				driver_definition["clone_of"] = record["clone_of"]
			driver_definitions.append(driver_definition)
		knowledge_path = f"knowledge/{slug(identity['manufacturer'])}/{slug(identity['name'])}-{identity.get('year') or 'unknown'}.md"
		definition: dict[str, Any] = {
			"format": "pinmame-machine-definition",
			"schema_version": SCHEMA_VERSION,
			"machine": identity,
			"coverage": {
				"status": "partial",
				# A conflict this importer just emitted is an outstanding
				# requirement, and `completion_score` is derived from this list:
				# omitting it hands the machine credit for work nobody has done.
				# The fixed list left it out regardless of what was emitted,
				# which silently overstated eighteen definitions.
				"missing": MIGRATION_MISSING + ["unresolved_conflicts"] if builder.conflicts else MIGRATION_MISSING,
				"dimensions": {
					"catalog_identity": "observed",
					"address_enumeration": "candidate",
					"semantic_naming": "candidate",
					"physical_wiring": "candidate",
					"mechanisms": "candidate" if mechanisms else "unknown",
					"variant_coverage": "candidate",
					"recreation_knowledge": "candidate",
				},
			},
			"controller": {"platform": f"pinmame.{slug(game.get('platform', 'unknown'))}", "inversion_applied_by_emulator": True},
			"drivers": driver_definitions,
			"inputs": sorted(builder.inputs, key=lambda device: (device["binding"]["group"], device["binding"]["device"], device["binding"].get("channel", -1), device["id"])),
			"outputs": sorted(builder.outputs, key=lambda device: (device["binding"]["group"], device["binding"]["device"], device["binding"].get("channel", -1), device["id"])),
			"displays": [],
			"mechanisms": mechanisms,
			"relationships": [],
			"sources": sorted({source["id"]: source for source in source_records}.values(), key=lambda source: source["id"]),
			"knowledge": {"path": knowledge_path, "status": "partial"},
			"conflicts": builder.conflicts,
		}
		definition_path = f"machines/partial/{slug(identity['manufacturer'])}/{slug(identity['name'])}-{identity.get('year') or 'unknown'}.json"
		write_json(repository_root / definition_path, definition)
		write_text(repository_root / knowledge_path, _knowledge_markdown(identity, ordered_documents, mechanisms, builder.notes, source_ids))
		created.append({"machine_id": target_id, "definition": definition_path, "driver_count": len(assigned_drivers), "source_files": [f"{stem}.json" for stem, _document in ordered_documents]})

	rebuilt = rebuild_catalog(repository_root)
	report = {
		"format": "pinmame-legacy-migration-report",
		"version": 1,
		"legacy_revision": revision,
		"pinmame_revision": catalog["source"]["pinmame_revision"],
		"created_machine_count": len(created),
		"created": created,
		"files": file_report,
		"dropped_vpe_hints": dict(sorted(dropped_hints.items())),
		"unresolved_split_drivers": unresolved_split_drivers,
		"catalog_summary": rebuilt["summary"],
	}
	write_json(repository_root / "reports" / "legacy-migration.json", report)
	return report
