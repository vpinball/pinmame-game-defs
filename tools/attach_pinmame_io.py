"""Attach PinMAME-derived controller platforms and candidate I/O to partial definitions.

Two mechanical, source-located facts are pulled from the pinned PinMAME checkout:

1. Controller platform. The ``CORE_GAMEDEF`` line that declares a machine's root
   driver selects a PinMAME machine module (for example ``wpc_m95S``); a reviewed
   module-to-profile mapping attaches the matching ``controllers/pinmame``
   platform to the definition. This mirrors what curated partials already claim
   (Junk Yard confirmed ``wpc_m95S`` from the driver's own ``GEN_WPC95`` field),
   so ``controller_platform`` leaves ``coverage.missing`` for attached machines.
2. Candidate inputs/outputs. Driver files that serve exactly one physical machine
   and declare numeric ``sw*``/``s*`` symbols contribute candidate switch and
   solenoid devices with symbol-derived labels and candidate provenance. Nothing
   is claimed beyond what the pinned source declares; the SAM synthetic game-on
   channel (public solenoid 33) is modelled as the platform truth instead of a
   coil. WPC constant-zero channel 32 is deliberately not emitted: modelling it
   correctly drags per-generation 29-31 state-channel modelling with it.

Machines that already carry a controller block, are author-ready, hold existing
devices, or whose driver file serves several machines are deliberately skipped.
Run from the repository root:

	python -B tools/attach_pinmame_io.py --dry-run
	python -B tools/attach_pinmame_io.py
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from pinmame_game_defs.catalog import pinmame_revision  # noqa: E402
from pinmame_game_defs.coverage import write_coverage_report  # noqa: E402
from pinmame_game_defs.identifiers import slug  # noqa: E402
from pinmame_game_defs.jsonio import file_sha256, load_json, write_json, write_text  # noqa: E402
from pinmame_game_defs.pinmame_source import _read_source, _symbol_label  # noqa: E402
from pinmame_game_defs.registry import rebuild_catalog  # noqa: E402

WORKING_ROOT = REPOSITORY_ROOT.parent / "pinmame-game-defs-working-dir"
PINMAME_SOURCE = WORKING_ROOT / "source-checkouts" / "pinmame"

GAMEDEF_PATTERN = re.compile(r"\bCORE_GAMEDEF\s*\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*,\s*\"([^\"]*)\"\s*,\s*([^,]+),\s*\"([^\"]*)\"\s*,\s*([a-z0-9_]+)", re.IGNORECASE)
CLONEDEF_PATTERN = re.compile(r"\bCORE_CLONEDEF\s*\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*,\s*\"([^\"]*)\"\s*,\s*([^,]+),\s*\"([^\"]*)\"\s*,\s*([a-z0-9_]+)", re.IGNORECASE)
GAMEDEFNV_PATTERN = re.compile(r"\bCORE_GAMEDEFNV\s*\(\s*([a-z0-9_]+)\s*,\s*\"([^\"]*)\"\s*,\s*([^,]+),\s*\"([^\"]*)\"\s*,\s*([a-z0-9_]+)", re.IGNORECASE)
CLONEDEFNV_PATTERN = re.compile(r"\bCORE_CLONEDEFNV\s*\(\s*([a-z0-9_]+)\s*,\s*\"([^\"]*)\"\s*,\s*([^,]+),\s*\"([^\"]*)\"\s*,\s*([a-z0-9_]+)", re.IGNORECASE)
DEFINE_PATTERN = re.compile(r"^\s*#\s*define\s+([A-Za-z][A-Za-z0-9_]*)\s+(-?\d+)\s*(?://.*|/\*.*?\*/)?\s*$", re.MULTILINE)

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
PINMAME_URI = "https://github.com/vpinball/pinmame"

# Reviewed mapping from PinMAME machine-module symbol to controller profile ID.
# Modules whose generation the existing profiles do not cover (System 3-7, Bally
# 6803, Hankin, United/Monroe bowlers, first-generation WPC DMD, Sega, and Stern
# MPU-100 -- GEN_STMPU100 is a distinct generation with a different cabinet-switch
# matrix column, so the MPU-200 profile would misstate those machines) stay
# unmapped so controller_platform remains honestly missing for them.
MODULE_PLATFORMS = {
	"wpc_m95S": "pinmame.wpc-95",
	"wpc_m95DCSS": "pinmame.wpc-95",
	"wpc_mFliptronS": "pinmame.wpc-fliptronic",
	"wpc_mSecurityS": "pinmame.wpc-security",
	"wpc_mDCSS": "pinmame.wpc-dcs",
	"wpc_mAlpha": "pinmame.wpc-alpha",
	"wpc_mAlpha2S": "pinmame.wpc-alpha",
	"sam1": "pinmame.sam",
	"sam2": "pinmame.sam",
	"p2k": "pinmame.p2k",
	"s11_mS11S": "pinmame.system-11",
	"s11_mS11AS": "pinmame.system-11",
	"s11_mS11BS": "pinmame.system-11",
	"s11_mS11B2S": "pinmame.system-11",
	"s11_mS11CS": "pinmame.system-11",
	"s11_mS11XS": "pinmame.system-11",
	"s11_mS11XSL": "pinmame.system-11",
	"s9_mS9S": "pinmame.system-11",
	"s9_mS9PS": "pinmame.system-11",
	"s9_mS11S": "pinmame.system-11",
	"cc1": "pinmame.capcom",
	"cc2": "pinmame.capcom",
	# by35_mBY17 and by35_GP are aliases of the plain by35 machine driver whose
	# games declare GEN_BY17, a generation distinct from GEN_BY35 (different
	# display/DIP/sound-enable hardware flags in by35.c), so they must not take
	# the AS-2518-35 profile. by35_mST100bs games declare GEN_STMPU200 even
	# though the module name says ST100 (stgames.c: "uses MPU-200 inports"), so
	# they keep the MPU-200 profile, while by35_mST100/s are GEN_STMPU100 and
	# stay unclaimed.
	"by35_centaur": "pinmame.by35",
	"by35_mST100bs": "pinmame.stern-mpu200",
	"by35_mST200": "pinmame.stern-mpu200",
	"by35_mST200v": "pinmame.stern-mpu200",
}
BY35_PREFIX = "by35_mBY35_"
NON_GAME_KINDS = {"diagnostic_software", "system_software"}

SAM_GAME_ON_DEVICE = {
	"aliases": [{"namespace": "pinmame.solenoid", "value": "33"}],
	"availability": "used",
	"binding": {"device": 33, "group": "pinmame.output.solenoid"},
	"id": "solenoid.33",
	"kind": "virtual",
	"label": "PinMAME SAM game-on state",
	"physical": {
		"notes": "PinMAME's synthetic S.A.M. game-on/fast-flip state, published on public solenoid address 33 (sam.c's SAM_FASTFLIPSOL) rather than a driver-board transistor. Candidate until a per-machine harness trace pins its behavior.",
	},
	"provenance": {"source_refs": ["pinmame.core.PLACEHOLDER"], "status": "candidate"},
}


def parse_driver_files() -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
	"""Return per-driver declarations and per-file numeric switch/solenoid defines."""
	declarations: dict[str, dict[str, Any]] = {}
	file_defines: dict[str, list[dict[str, Any]]] = {}
	for path in sorted(PINMAME_SOURCE.glob("src/**/*.c")):
		text, _encoding = _read_source(path)
		if "CORE_GAMEDEF" not in text:
			continue
		relative = path.relative_to(PINMAME_SOURCE).as_posix()
		defines: list[dict[str, Any]] = []
		for match in DEFINE_PATTERN.finditer(text):
			symbol, raw_address = match.groups()
			if symbol.startswith("sw") or (symbol.startswith("s") and len(symbol) > 1 and symbol[1].isupper()):
				defines.append({"symbol": symbol, "address": int(raw_address), "label": _symbol_label(symbol)})
		if defines:
			file_defines[relative] = sorted(defines, key=lambda item: (item["address"], item["symbol"]))
		for pattern, is_clone in ((GAMEDEF_PATTERN, False), (GAMEDEFNV_PATTERN, False), (CLONEDEF_PATTERN, True), (CLONEDEFNV_PATTERN, True)):
			for match in pattern.finditer(text):
				groups = match.groups()
				if pattern in (GAMEDEFNV_PATTERN, CLONEDEFNV_PATTERN):
					driver_id, _name, _year, manufacturer, module = groups
				else:
					prefix, revision, _name, _year, manufacturer, module = groups
					driver_id = f"{prefix}_{revision}"
				line = text.count("\n", 0, match.start()) + 1
				# A primary GAMEDEF outranks a CLONEDEF seen in an earlier file.
				if driver_id in declarations and not is_clone and declarations[driver_id].get("clone"):
					del declarations[driver_id]
				if driver_id in declarations:
					continue
				declarations[driver_id] = {
					"module": module,
					"manufacturer": manufacturer,
					"file": relative,
					"line": line,
					"clone": is_clone,
				}
	return declarations, file_defines


def core_source_record(revision: str, declaration: dict[str, Any]) -> dict[str, Any]:
	return {
		"attribution": "PinMAME contributors",
		"id": f"pinmame.core.{revision[:12]}",
		"kind": "pinmame_core",
		"license": "BSD-3-Clause",
		"locator": f"{declaration['file']}:{declaration['line']} (machine module {declaration['module']})",
		"revision": revision,
		"uri": PINMAME_URI,
	}


def driver_source_record(revision: str, relative: str) -> dict[str, Any]:
	return {
		"attribution": "PinMAME contributors",
		"id": f"pinmame.driver.{Path(relative).stem}",
		"kind": "pinmame_core",
		"license": "BSD-3-Clause",
		"locator": f"{relative} switch/solenoid #define block",
		"revision": revision,
		"sha256": file_sha256(PINMAME_SOURCE / relative),
		"uri": PINMAME_URI,
	}


def device_from_define(define: dict[str, Any], occupied: set[str]) -> dict[str, Any]:
	if define["group"] == "pinmame.input.switch":
		prefix, kind, namespace = "switch", "switch", "pinmame.switch"
	else:
		prefix, kind, namespace = "coil", "coil", "pinmame.solenoid"
	base_id = f"{prefix}.{slug(define['label'])}"
	device_id = base_id
	if device_id in occupied:
		device_id = f"{base_id}-{define['address']}"
	index = 2
	while device_id in occupied:
		device_id = f"{base_id}-{define['address']}-{index}"
		index += 1
	occupied.add(device_id)
	label = define["label"]
	if label and label[0].islower():
		label = label[0].upper() + label[1:]
	return {
		"aliases": [{"namespace": namespace, "value": str(define["address"])}],
		"binding": {"device": define["address"], "group": define["group"]},
		"id": device_id,
		"kind": kind,
		"label": label,
		"provenance": {"source_refs": [define["source_id"]], "status": "candidate"},
	}


def synthetic_device(template: dict[str, Any], source_id: str) -> dict[str, Any]:
	copied = copy.deepcopy(template)
	for block in (copied.get("provenance"), copied.get("spatial", {}).get("provenance")):
		if isinstance(block, dict) and block.get("source_refs") == ["pinmame.core.PLACEHOLDER"]:
			block["source_refs"] = [source_id]
	return copied


def derive_platform(definition: dict[str, Any], machine: dict[str, Any], declarations: dict[str, dict[str, Any]], profiles: dict[str, dict[str, Any]]) -> tuple[str | None, dict[str, Any] | None, str | None]:
	"""Derive the controller platform for one machine from its root driver's
	CORE_GAMEDEF machine module, or (None, declaration, root) when no reviewed
	profile covers it. A record whose root driver is not in its own driver list
	(a split-tree residual) never derives a platform: the root's module describes
	hardware the record does not hold."""
	root_id = machine["root_drivers"][0] if len(machine["root_drivers"]) == 1 else None
	if root_id is None:
		return None, None, root_id
	declaration = declarations.get(root_id)
	if declaration is None:
		return None, None, root_id
	if root_id not in {driver["id"] for driver in definition["drivers"]}:
		return None, declaration, root_id
	module = declaration["module"]
	if module.startswith(BY35_PREFIX):
		platform = "pinmame.by35"
	elif module.startswith("de_m"):
		# de_m modules serve both Data East and Sega machines; the GAMEDEF's own
		# manufacturer string separates them. Sega machines stay unmapped
		# because their curated records do not agree on a whitestar platform.
		platform = "pinmame.dataeast" if "data east" in declaration["manufacturer"].casefold() else None
	else:
		platform = MODULE_PLATFORMS.get(module)
	if platform is None:
		return None, declaration, root_id
	profile_groups = {group["id"] for group in profiles[platform]["groups"]}
	existing_groups = {
		device["binding"]["group"]
		for collection in ("inputs", "outputs")
		for device in definition[collection]
		if isinstance(device.get("binding"), dict) and isinstance(device["binding"].get("group"), str)
	}
	if not existing_groups <= profile_groups:
		return None, declaration, root_id
	return platform, declaration, root_id


def attach_define_devices(definition: dict[str, Any], machine_id: str, file_machines: dict[str, set[str]], file_defines: dict[str, list[dict[str, Any]]], platform: str | None, skipped_counter: list[int]) -> int:
	"""Merge every eligible driver file's numeric switch/solenoid defines into the
	(empty) device arrays, adding a per-file driver source record. Returns the
	number of attached devices."""
	inputs = definition["inputs"]
	outputs = definition["outputs"]
	sources = definition["sources"]
	source_ids = {source["id"] for source in sources}
	eligible_files = sorted(
		relative
		for relative, machine_ids in file_machines.items()
		if machine_ids == {machine_id} and relative in file_defines
	)
	if not eligible_files:
		return 0
	occupied = {device["id"] for device in inputs + outputs}
	bindings = {(device["binding"]["group"], device["binding"]["device"]) for device in inputs + outputs if isinstance(device.get("binding"), dict)}
	merged: list[dict[str, Any]] = []
	for relative in eligible_files:
		source_id = f"pinmame.driver.{Path(relative).stem}"
		if source_id not in source_ids:
			sources.append(driver_source_record(PINMAME_REVISION, relative))
			source_ids.add(source_id)
		for define in file_defines[relative]:
			group = "pinmame.input.switch" if define["symbol"].startswith("sw") else "pinmame.output.solenoid"
			if platform == "pinmame.sam" and group == "pinmame.output.solenoid" and define["address"] == 33:
				skipped_counter[0] += 1
				continue
			if platform is not None and platform.startswith("pinmame.wpc") and group == "pinmame.output.solenoid" and define["address"] == 32:
				skipped_counter[0] += 1
				continue
			key = (group, define["address"])
			if key in bindings:
				continue
			bindings.add(key)
			merged.append(dict(define, group=group, source_id=source_id))
	for define in merged:
		device = device_from_define(define, occupied)
		(inputs if define["group"] == "pinmame.input.switch" else outputs).append(device)
	return len(merged)


def check_attachments(declarations: dict[str, dict[str, Any]], profiles: dict[str, dict[str, Any]]) -> None:
	"""Fail on drift between the pass's derivation and the records on disk.

	Only records this pass attached carry a core source citing an explicit
	"machine module" locator; curated platform declarations predate that
	convention and are out of this tool's contract."""
	catalog = load_json(REPOSITORY_ROOT / "catalog" / "pinmame.json")
	core_source_id = f"pinmame.core.{PINMAME_REVISION[:12]}"
	errors: list[str] = []
	checked = 0
	for machine in catalog["machines"]:
		definition = load_json(REPOSITORY_ROOT / machine["definition"])
		module_locators = [
			source["locator"]
			for source in definition["sources"]
			if source.get("id") == core_source_id and "machine module " in source.get("locator", "")
		]
		if not module_locators:
			continue
		platform, declaration, _root = derive_platform(definition, machine, declarations, profiles)
		checked += 1
		machine_id = machine["id"]
		if declaration is None:
			errors.append(f"{machine_id}: cites machine module but the pinned source no longer declares its root")
			continue
		controller = definition.get("controller")
		if bool(controller) != (platform is not None):
			errors.append(f"{machine_id}: controller block {controller} does not match the derived platform {platform!r}")
			continue
		if platform is None:
			continue
		if controller["platform"] != platform or controller.get("inversion_applied_by_emulator") is not True:
			errors.append(f"{machine_id}: controller block does not match the derivation")
			continue
		locator = module_locators[0]
		if f"machine module {declaration['module']}" not in locator or f"{declaration['file']}:{declaration['line']}" not in locator:
			errors.append(f"{machine_id}: core source locator does not match the derivation: {locator}")
	if errors:
		raise SystemExit("Attachment drift detected:\n" + "\n".join(errors[:40]))
	print(f"check OK: {checked} attached records match the module derivation")


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--dry-run", action="store_true")
	parser.add_argument("--sanitize-defines", action="store_true", help="Recompute every machine this pass attached defines to with the current define rules.")
	parser.add_argument("--check", action="store_true", help="Verify controller platforms against the module derivation without writing.")
	args = parser.parse_args()

	actual_revision = pinmame_revision(PINMAME_SOURCE)
	if actual_revision != PINMAME_REVISION:
		raise SystemExit(f"Pinned PinMAME checkout drifted: {actual_revision}")
	catalog = load_json(REPOSITORY_ROOT / "catalog" / "pinmame.json")
	if catalog["source"]["pinmame_revision"] != PINMAME_REVISION:
		raise SystemExit("Catalog pins a different PinMAME revision.")
	profiles = {profile["id"]: profile for profile in (load_json(path) for path in sorted((REPOSITORY_ROOT / "controllers" / "pinmame").glob("*.json")))}
	declarations, file_defines = parse_driver_files()
	if args.check:
		check_attachments(declarations, profiles)
		return

	driver_machine = {record["id"]: record["machine_id"] for record in catalog["drivers"]}
	file_machines: dict[str, set[str]] = {}
	for driver_id, declaration in declarations.items():
		machine_id = driver_machine.get(driver_id)
		if machine_id:
			file_machines.setdefault(declaration["file"], set()).add(machine_id)

	core_source_id = f"pinmame.core.{PINMAME_REVISION[:12]}"
	platform_counts: dict[str, int] = {}
	device_machine_count = 0
	device_total = 0
	changed = 0
	skipped_counter = [0]
	writes: list[tuple[Path, dict[str, Any]]] = []
	note_writes: list[tuple[Path, str]] = []
	for machine in catalog["machines"]:
		if machine["machine_kind"] in NON_GAME_KINDS or machine["coverage_status"] != "partial":
			continue
		definition_path = REPOSITORY_ROOT / machine["definition"]
		definition = load_json(definition_path)
		machine_id = machine["id"]
		sanitize_targets = args.sanitize_defines and any(source.get("id", "").startswith("pinmame.driver.") for source in definition["sources"])
		if not sanitize_targets and definition.get("controller"):
			continue
		platform, declaration, root_id = derive_platform(definition, machine, declarations, profiles)
		attached_platform = False
		attached_devices = 0
		synthetic = None
		if sanitize_targets:
			synthetic = next(
				(output for output in definition["outputs"] if output.get("binding") == {"device": 33, "group": "pinmame.output.solenoid"} and output.get("kind") == "virtual"),
				None,
			)
			definition["inputs"] = []
			definition["outputs"] = []
			definition["sources"] = [source for source in definition["sources"] if not source.get("id", "").startswith("pinmame.driver.")]
		if not definition["inputs"] and not definition["outputs"]:
			attached_devices = attach_define_devices(definition, machine_id, file_machines, file_defines, platform, skipped_counter)
		if platform is not None:
			sources = definition["sources"]
			source_ids = {source["id"] for source in sources}
			if core_source_id not in source_ids:
				sources.append(core_source_record(PINMAME_REVISION, declaration))
				source_ids.add(core_source_id)
			definition["controller"] = {"inversion_applied_by_emulator": True, "platform": platform}
			if "controller_platform" in definition["coverage"]["missing"]:
				definition["coverage"]["missing"].remove("controller_platform")
			if platform == "pinmame.sam" and not any(
				isinstance(output.get("binding"), dict) and output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"} for output in definition["outputs"]
			):
				definition["outputs"].append(synthetic_device(SAM_GAME_ON_DEVICE, core_source_id))
				attached_devices += 1
			platform_counts[platform] = platform_counts.get(platform, 0) + 1
			attached_platform = True
		if synthetic is not None:
			definition["outputs"].append(synthetic)
			attached_devices += 1

		if attached_platform or attached_devices or sanitize_targets:
			changed += 1
			if attached_devices:
				device_machine_count += 1
				device_total += attached_devices
			knowledge_path = REPOSITORY_ROOT / definition["knowledge"]["path"]
			if knowledge_path.is_file() and declaration is not None and root_id is not None:
				note_writes.append((knowledge_path, knowledge_note_text(knowledge_path.read_text(encoding="utf-8"), root_id, declaration, platform, len(definition["inputs"]) + len(definition["outputs"]))))
			if args.dry_run:
				continue
			writes.append((definition_path, definition))

	mode = "sanitized" if args.sanitize_defines else "attached"
	print(f"{'DRY RUN: ' if args.dry_run else ''}{mode}: {changed} definitions touched")
	print(f"platform attachments: {platform_counts}")
	print(f"machines with candidate devices: {device_machine_count} ({device_total} devices)")
	print(f"define references skipped by platform rules: {skipped_counter[0]}")
	if args.dry_run:
		return
	for path, definition in writes:
		write_json(path, definition)
	for path, text in note_writes:
		if text is not None:
			write_text(path, text)
	rebuild_catalog(REPOSITORY_ROOT)
	report = write_coverage_report(REPOSITORY_ROOT)
	print(f"coverage: {report['stub_count']} stubs, {report['partial_count']} partials, {report['author_ready_count']} author-ready")


def knowledge_note_text(text: str, root_id: str, declaration: dict[str, Any], platform: str | None, device_count: int) -> str | None:
	marker = "## What a curator must establish next"
	if marker not in text:
		return None
	platform_text = (
		f"; the definition declares controller platform `{platform}` from it." if platform else "; no reviewed profile covers that module yet, so no platform is declared."
	)
	first_line = (
		f"- The pinned PinMAME source declares `{root_id}` at `{declaration['file']}:{declaration['line']}` with machine module `{declaration['module']}`{platform_text}"
	)
	device_line = (
		f"- The driver source's named switch/solenoid symbols are carried as {device_count} candidate devices in the definition." if device_count else None
	)
	section_start = text.find("## PinMAME source contract")
	if section_start >= 0:
		section_end = text.find("\n## ", section_start + 1)
		existing_block = text[section_start:] if section_end < 0 else text[section_start:section_end + 1]
		lines = ["## PinMAME source contract (candidate)", "", first_line]
		if device_line:
			lines.append(device_line)
		return text.replace(existing_block, "\n".join(lines) + "\n\n", 1)
	lines = ["## PinMAME source contract (candidate)", "", first_line]
	if device_line:
		lines.append(device_line)
	return text.replace(marker, "\n".join(lines) + "\n\n" + marker, 1)


if __name__ == "__main__":
	main()
