#!/usr/bin/env python3
"""Curate the physical Stern Meteor (1979) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and retained-table coordinate is a literal in
``tools/meteor_data.py`` or here, and the runtime facts come from the committed compact evidence, so regeneration reproduces the canonical
definition, its pinned seed, the spatial report and the knowledge note byte for byte without reading the external evidence roots. ``--check``
refuses drift, ``--regenerate`` is the only path that writes the repository artifacts, and ``--write-extraction-manifest`` /
``--verify-extraction`` write and verify the canonical manifest of the retained table extraction under ``PINMAME_VPX_SOURCES_ROOT``.

Evidence authority follows the runbook. The two pinned known-working corpus scripts own runtime bindings, this game's own 40-page manual (whose
last pages are its schematic sheets) and its self-test card own physical construction, wiring and device presence, pinned PinMAME owns controller
topology, and the retained harness runs pair printed numbers with public addresses. Where the machine's own sheets disagree only about a connector
pin or a wire colour the disagreement is a device note, not a conflict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
from pinmame_game_defs.schema_validation import validate_against_schema  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
import meteor_data as data  # noqa: E402
import summarize_meteor_runtime as runtime_summary  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = Path("machines/partial/stern/meteor-1979.json")
AUTHOR_READY_PATH = Path("machines/author-ready/stern/meteor-1979.json")
SEED_PATH = Path("tools/seeds/stern/meteor-1979.json")
KNOWLEDGE_PATH = Path("knowledge/stern/meteor-1979.md")
SPATIAL_REPORT_PATH = Path("reports/spatial/stern/meteor-1979.json")
SPATIAL_REPORT_MARKDOWN_PATH = Path("reports/spatial/stern/meteor-1979.md")
RUNTIME_EVIDENCE_PATH = Path("evidence/runtime/stern/meteor-diagnostics-and-gameplay.json")
EXCERPT_ROOT = "evidence/excerpts/stern.meteor.1979"
# The residual record PinMAME's second root (meteora) had before this curation; this record carries that driver now.
RETIRED_PATHS = (Path("machines/partial/stern/meteor-1979-meteora.json"), Path("knowledge/stern/meteor-1979-meteora.md"))

MACHINE_ID = "stern.meteor.1979"
PINMAME_REVISION = runtime_summary.PINMAME_REVISION
LIBRARY_SHA256 = runtime_summary.LIBRARY_SHA256
ROM_ARCHIVES = runtime_summary.ROM_ARCHIVES
CORPUS_REPOSITORY = "https://github.com/sverrewl/vpxtable_scripts"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REPOSITORY = "https://github.com/jsm174/vpx-standalone-scripts"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-stern-mpu200"
MANUAL_SOURCE = "manual.stern.meteor.1979"
SELF_TEST_CARD_SOURCE = "manual.stern.meteor.self-test-card"
IPDB_SOURCE = "ipdb.1580"
SCRIPT_SOURCE = "vpx-script.meteor-corpus"
STANDALONE_SOURCE = "vpx-script.meteor-standalone"
TABLE_SOURCE = "vpx-table.meteor-bord-1-0"
TABLE_SCRIPT_SOURCE = "vpx-script.meteor-bord-1-0"
EXTRACTION_SOURCE = "vpx-extraction.meteor-bord-1-0"
VPM_LIBRARY_SOURCE = "vpx-script.vpinmame-stern-library"
# The VPinMAME script libraries the table loads, copied byte for byte from the retained installed Scripts folder.
VPM_LIBRARY_RELATIVE = Path("stern/meteor-1979/library")
VPM_LIBRARY_FILES = {"stern.vbs": "b835ce5b0c11c6d268f58c92e534c1677e64cb47e103b33179b82c6c337be0e5", "core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"}
# The fields of one retained run in the compact runtime evidence, as the summarizer writes them.
RAW_RUN_FIELDS = {"action_count", "initial_switches", "name", "nvram_initialization", "scenario_path", "scenario_sha256", "self_test_pulses", "sha256", "snapshot_count", "watch_switches"}
# SHA-256 of the committed compact runtime evidence, which summarize_meteor_runtime.py --check reproduces from the retained runs.
RUNTIME_EVIDENCE_SHA256 = "fc93801dc6e255bafcd888576dfd690a98d406c102b76758d0be67bd0c7deac0"
# Every field summarize_meteor_runtime.py emits; the curator refuses a compact document that lacks one.
DOCUMENT_FIELDS = {"driver_ids", "extractor", "format", "machine_ids", "mechanisms", "outputs", "recreation_notes", "runtime", "source", "states", "switches", "version"}
RUNTIME_FIELDS = {"command_template", "emulator", "game", "observations", "raw_runs", "rom_archive_sha256"}
OBSERVATION_FIELDS = {"lamp_addresses_driven_outside_self_test", "lamp_addresses_seen", "lamp_decoder_holes_not_seen", "named_output_addresses", "physical_service_solenoid_to_public",
	"public_solenoid_decoder_holes_not_seen", "runs", "solenoid_addresses_seen"}
_PLAY_RUN_FIELDS = {"named_action_observations", "note", "solenoid_addresses_seen"}
RUN_OBSERVATION_FIELDS = {
	"self-test": {"limitation", "note", "ordered_solenoid_on_sequence", "solenoid_addresses_seen"},
	"solenoid-test": {"note", "ordered_solenoid_on_sequence", "solenoid_addresses_seen"},
	"switch-test": {"note"},
	**{name: _PLAY_RUN_FIELDS for name in ("coin-bookkeeping", "gameplay", "meteora-variant-io", "meteorb-variant-io", "meteorbf-variant-io", "meteorc-variant-io",
		"meteord-variant-io", "meteorfp-variant-io")},
}

MANUAL_PDF = "Stern_1979_Meteor_Manual.pdf"
SELF_TEST_CARD_PDF = "Stern_1979_Meteor_Self_Test_Display_Numbers.pdf"
MANUAL_SHA256 = "d7fd70e914eafc0dc496a04d0589a381031842cf34bdfe3c3d39b59331321349"
SELF_TEST_CARD_SHA256 = "6ed7ce730ed3883dedaf62548b04c087523b6e27b6159756e82b908d74601c13"
IPDB_PAGE_SHA256 = "36021221d945cecf39f9f6e1390bb00e1c1974afd11fe766e75a92b139d42125"
SCRIPT_PATH = "Meteor (Stern 1979).vbs"
SCRIPT_SHA256 = "3e9dab0eb394fd98462c0140866b6b58ae4c9ac2661d76528b976443f72037ea"
STANDALONE_PATH = "Meteor (Stern 1979)/Meteor (Stern 1979).vbs"
STANDALONE_SHA256 = "d2e0a5ebd8d9e4544b427f7450bc24fcbdd928a2ae58ebd4c0f8e8f88dc23ca7"
STANDALONE_BLOB_SHA256 = "7357934f36df6ecd321a2e06407ece42b8943be9e1a6ebc937134db1d7e8fc6b"

TABLE_FILENAME = "Meteor (Stern 1979).vpx"
TABLE_SHA256 = "0f8c826c3e9565835189b79d599a1dd72aa5dd20e1347d6fab8477fa1ff65614"
TABLE_BYTES = 93507584
TABLE_ARCHIVE_FILENAME = "839681115_Meteor(Stern1979)1.0.0a.zip"
TABLE_ARCHIVE_SHA256 = "711b0ca95613822022fb2f3c7272f8ad8959e72e19d6f6eea6de5a2a9189703e"
TABLE_SCRIPT_SHA256 = "b5a7109e18348aabe6aaa1b16f539110ba3df33deaef99eae1a84f7bfb23098a"
TABLE_RELATIVE = Path("stern/meteor-1979/archive")
EXTRACTION_RELATIVE = TABLE_RELATIVE / "extracted-vpxtool"
# vpxtool export obj --units vpu of the retained table, outside Git: x and y are playfield VPX units, z the height. It leaves out invisible primitives.
WORLD_OBJ_RELATIVE = Path("stern/meteor-1979/world-obj/Meteor (Stern 1979).obj")
WORLD_OBJ_SHA256 = "d971105c3b755f73d08ec18dea5ad007cae2b8bd45804538cd749dcc8af24bc5"
WORLD_OBJ_BYTES = 31095858
# A visibility-only derivative of the retained table, outside Git, so the export includes the two invisible dead-bumper primitives: the retained extraction
# with `is_visible` set to true in Primitive.bumper2.json and Primitive.bumper3.json and nothing else changed, assembled with vpxtool, then re-extracted
# (the re-extraction and its manifest) and exported like the table.
BUMPERS_VISIBLE_RELATIVE = Path("stern/meteor-1979/bumpers-visible")
BUMPERS_VISIBLE_VPX = "Meteor (Stern 1979) bumpers visible.vpx"
BUMPERS_VISIBLE_VPX_SHA256 = "08409a84fcac343ff26117e32f785644d7c2975f535f26be8eed37e3e10ac718"
BUMPERS_VISIBLE_VPX_BYTES = 93683712
BUMPERS_VISIBLE_MANIFEST_SHA256 = "012644d79ccfe7ef9e0275721bab9ce1f4d5508e9fd958e91c57afeefbba711c"
BUMPERS_VISIBLE_OBJ_RELATIVE = BUMPERS_VISIBLE_RELATIVE / "world-obj/Meteor (Stern 1979) bumpers visible.obj"
BUMPERS_VISIBLE_OBJ_SHA256 = "8080122eda9a0258560a94383fd7d96f3de068b2550a44a2dd647410e7ad3d53"
BUMPERS_VISIBLE_OBJ_BYTES = 31136534
EXTRACTION_MANIFEST_RELATIVE = TABLE_RELATIVE / "extracted-vpxtool.manifest.json"
EXTRACTION_MANIFEST_SHA256 = "9b16fc8e7a8138c42388241618c9799ba4b40ba41b68dff363bc8ed9b443aab8"
EXTRACTION_FILE_COUNT = 1169
EXTRACTION_TOTAL_BYTES = 115729773
VPXTOOL_VERSION = "git:v0.33.3"
TABLE_REFS = (TABLE_SOURCE, TABLE_SCRIPT_SOURCE)

RUN_NAMES = runtime_summary.RUN_NAMES
RUN_SOURCES = {name: f"runtime.meteor.{name}" for name in RUN_NAMES}
# The pinned LICENSE keeps every PinMAME file whose first line lacks `// license:BSD-3-Clause` under the old MAME license.
PINMAME_UNMARKED_FILES = ("src/wpc/stgames.c", "src/wpc/stsnd.c", "src/wpc/core.h")
PINMAME_BSD_FILES = ("src/wpc/by35.c", "src/wpc/by35.h")
PINMAME_CATALOG_LICENSE = "PinMAME old MAME license: src/wpc/stgames.c carries no BSD-3-Clause marker (pinned LICENSE)"
PINMAME_CORE_LICENSE = ("PinMAME old MAME license for the unmarked " + ", ".join(PINMAME_UNMARKED_FILES[:-1]) + f" and {PINMAME_UNMARKED_FILES[-1]}; BSD-3-Clause for "
	+ " and ".join(PINMAME_BSD_FILES) + ", whose first line carries the marker (pinned LICENSE)")
# Committer times of the pinned revisions read, and of the controller profile's last change before this curation.
PINMAME_COMMITTED = "2026-10-25T20:16:49Z"
CORPUS_COMMITTED = "2026-07-07T06:37:05Z"
STANDALONE_COMMITTED = "2026-06-20T08:33:22Z"
CONTROLLER_COMMITTED = "2026-11-06T12:02:14Z"
# When each retained raw run finished (UTC, from the retained run files).
RUN_AT = {
	"self-test": "2026-11-20T08:34:15Z", "solenoid-test": "2026-11-20T08:35:59Z", "switch-test": "2026-11-20T08:40:15Z",
	"coin-bookkeeping": "2026-11-20T08:55:37Z", "gameplay": "2026-11-20T08:58:07Z", "meteora-variant-io": "2026-11-20T08:56:53Z",
	"meteorb-variant-io": "2026-11-20T08:58:08Z", "meteorbf-variant-io": "2026-11-20T09:11:16Z", "meteorc-variant-io": "2026-11-20T09:13:49Z",
	"meteord-variant-io": "2026-11-20T09:15:06Z", "meteorfp-variant-io": "2026-11-20T09:12:32Z",
}
SELF_TEST_SOURCE = RUN_SOURCES["self-test"]
SOLENOID_TEST_SOURCE = RUN_SOURCES["solenoid-test"]
SWITCH_TEST_SOURCE = RUN_SOURCES["switch-test"]
COIN_SOURCE = RUN_SOURCES["coin-bookkeeping"]
GAMEPLAY_SOURCE = RUN_SOURCES["gameplay"]
VARIANT_SOURCES = tuple(RUN_SOURCES[name] for name in runtime_summary.VARIANT_RUNS)

BOARD_MPU = "MPU module M-200 A4"
BOARD_SDU = "Solenoid Driver / Voltage Regulator module SDU B-432 A3"
BOARD_LDA = "Lamp Driver module LDA-100 B-431 A5"

# The three-bank cells whose position the playfield sheet and the known-working scripts read the other way round (see the conflict record).
CONFLICTED_SWITCHES = (10, 11, 20, 21, 23, 24)
# Switch placements derived from an object rather than taken from its own centre: the slingshot walls' drag-point means and the dead bumpers' mesh centres.
PROJECTED_SWITCHES = (12, 13, 15, 16)
# Solenoids no known-working script mentions at all.
UNSCRIPTED_SOLENOIDS = (17, 18, 20)
# The SDU sheet's load name for each METEOR knock-down coil, by the target switch it drops.
KNOCK_DOWN_LOADS = {32: "\"M\" TARGET", 31: "M\"E\"T TARGET", 30: "\"T\" TARGET", 29: "MET\"E\" TARGET", 28: "\"O\" TARGET", 27: "\"R\" TARGET"}
# The lamps PinMAME drove in no play run: their feature was not reached.
LAMPS_ONLY_IN_SELF_TEST_NOTE = " In the retained runs the ROM drove it only during its service tests; no play run lit it, which says nothing about its fitment."
# Lamp outputs whose list rows the definition does not follow for the drive connection, and why (the pairing notes give the reasons).
LAMP_CONNECTION_OVERRIDES = {31: ("J2", "15"), 62: ("J2", "7")}


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def normalize(x: float, y: float) -> tuple[float, float]:
	return round(x / data.TABLE_WIDTH, 6), round(y / data.TABLE_HEIGHT, 6)


def object_point(names: list[str]) -> tuple[float, float]:
	"""The mean of the named objects' raw centres; one name gives that object's own centre."""
	points = [data.OBJECTS[name][1:3] for name in names]
	return sum(x for x, _ in points) / len(points), sum(y for _, y in points) / len(points)


def located(identifier: str, role: str, groups: list[list[str]], *source_refs: str, status: str = "observed") -> dict[str, Any]:
	"""One placement per object group; a group of several objects is placed at their mean (a projection)."""
	placements = []
	for index, names in enumerate(groups, start=1):
		x, y = normalize(*object_point(names))
		suffix = f".{index}" if len(groups) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y,
			"provenance": provenance(*source_refs, status=status)})
	return {"status": status, "placements": placements}


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


def runtime_evidence_sha256(root: Path = ROOT) -> str:
	return hashlib.sha256((root / RUNTIME_EVIDENCE_PATH).read_bytes()).hexdigest()


def runtime_document(root: Path = ROOT) -> dict[str, Any]:
	"""The compact runtime evidence, refused unless it is the summarizer's complete document. Its digest is written into every run source's locator, so any later
	edit of the file changes the definition and fails --check even without the external runs."""
	document = load_json(root / RUNTIME_EVIDENCE_PATH)
	if (document.get("format") != "pinmame-machine-evidence" or document.get("extractor") != {"id": "tools/summarize_meteor_runtime.py", "version": 1}
			or document.get("machine_ids") != [MACHINE_ID] or not isinstance(document.get("source"), dict) or not document["source"].get("sha256")):
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH} is not the Meteor runtime summary")
	runs = document.get("runtime", {}).get("observations", {}).get("runs", {})
	if sorted(runs) != sorted(RUN_NAMES) or any(not isinstance(runs[name].get("note"), str) or not runs[name]["note"].strip() for name in RUN_NAMES):
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH} does not carry a noted observation for every retained run")
	if [run.get("name") for run in document["runtime"].get("raw_runs", [])] != list(RUN_NAMES):
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH} does not list the retained runs")
	errors = validate_against_schema(document, ROOT / "schemas" / "evidence.schema.json", RUNTIME_EVIDENCE_PATH.as_posix())
	if errors:
		raise RuntimeError("; ".join(errors[:5]))
	# The generic schema leaves most of the summarizer's fields optional; this curator reads them, so every field the summarizer emits must be present.
	runtime = document["runtime"]
	observations = runtime["observations"]
	emulator = runtime.get("emulator") or {}
	if (set(document) != DOCUMENT_FIELDS or set(runtime) != RUNTIME_FIELDS or set(observations) != OBSERVATION_FIELDS
			or set(emulator) != {"binary", "built_from_revision", "sha256"} or emulator["built_from_revision"] != runtime_summary.PINMAME_REVISION
			or not re.fullmatch(r"[0-9a-f]{64}", str(emulator["sha256"])) or runtime.get("game") != "meteor"):
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH} does not carry every field of the summarizer's document")
	for name in RUN_NAMES:
		run = runs[name]
		if set(run) != RUN_OBSERVATION_FIELDS[name] or any(not run[key] for key in run if key != "note"):
			raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH}: the {name} observation does not carry every field the summarizer emits for it")
	# Only the retained runs can prove the document complete (the retained-evidence test rebuilds it from them byte for byte), so the reviewed bytes are pinned: a truncated
	# or edited document is refused even where the field checks above cannot see it, and a new summary needs this digest updated with it.
	if hashlib.sha256((root / RUNTIME_EVIDENCE_PATH).read_bytes()).hexdigest() != RUNTIME_EVIDENCE_SHA256:
		raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH} is not the reviewed summary (SHA-256 {RUNTIME_EVIDENCE_SHA256}); rebuild it from the retained runs and update the pin")
	for run in document["runtime"]["raw_runs"]:
		scenario = f"tools/harness-scenarios/stern/{runtime_summary.RUNS[run['name']][1]}.json"
		if (set(run) != RAW_RUN_FIELDS or run["scenario_path"] != scenario or not all(re.fullmatch(r"[0-9a-f]{64}", run[key] or "") for key in ("sha256", "scenario_sha256"))
				or any(not isinstance(run[key], int) or isinstance(run[key], bool) or run[key] <= 0 for key in ("action_count", "snapshot_count"))):
			raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH}: raw run {run['name']} is not a complete summarizer record")
		if hashlib.sha256((ROOT / scenario).read_bytes()).hexdigest() != run["scenario_sha256"]:
			raise RuntimeError(f"{RUNTIME_EVIDENCE_PATH}: raw run {run['name']} does not pin its scenario {scenario}")
	return document


def runs_exercising_switch(observations: dict[str, Any], address: int) -> list[str]:
	"""The retained runs whose host actions closed or pulsed ``address``."""
	return [RUN_SOURCES[name] for name in RUN_NAMES
		if any(item["input_kind"] == "switch" and item["input_address"] == address for item in observations["runs"][name].get("named_action_observations", []))]


def runs_seeing_solenoid(observations: dict[str, Any], address: int) -> list[str]:
	return [RUN_SOURCES[name] for name in RUN_NAMES if address in (observations["runs"][name].get("solenoid_addresses_seen") or [])]


def runs_seeing_lamp(observations: dict[str, Any], address: int) -> list[str]:
	"""The burn-in drives all sixty lamps; the gameplay run drives every lamp any play run drives (the summarizer refuses otherwise)."""
	refs = [SELF_TEST_SOURCE] if address in observations["lamp_addresses_seen"] else []
	if address in observations["lamp_addresses_driven_outside_self_test"]:
		refs.append(GAMEPLAY_SOURCE)
	return refs


def normalized_text(x: float, y: float) -> str:
	nx, ny = normalize(x, y)
	return f"x {nx:.2f}, y {ny:.2f}"


# --- Inputs -------------------------------------------------------------------------------------------------------------


def matrix_wiring(address: int, cabinet: bool) -> dict[str, Any]:
	strobe, row = (address - 1) // 8, (address - 1) % 8
	strobe_wire, strobe_connection = data.CABINET_STROBE0 if cabinet else data.STROBES[strobe]
	return_wire, return_connection = data.CABINET_RETURNS[row] if cabinet else data.RETURNS[row]
	return {"board": BOARD_MPU, "control_wire": strobe_wire, "control_connection": strobe_connection, "return_wire": return_wire, "return_connection": return_connection}


def switch_construction(address: int, cabinet: bool) -> str:
	if cabinet:
		playfield = "draws this cell without a series diode" if address in data.NO_DIODE_SWITCHES else "draws a series diode in this cell"
		cabinet_sheet = "draws a series diode" if data.CABINET_DIODES[address] else "draws no diode"
		text = (f"Normally open contact. The playfield sheet {playfield} and the cabinet sheet {cabinet_sheet} (both sheets: `ALL DIODES ARE 1N-4004`); a construction detail that changes "
			"nothing PinMAME publishes")
	elif address in data.NO_DIODE_SWITCHES:
		text = "Normally open contact; the playfield sheet draws this cell without the series 1N4004 diode it draws in the other used cells"
	else:
		text = "Normally open contact with a series diode (playfield sheet: `ALL DIODES ARE 1N-4004.`)"
	if address in data.CAPACITOR_SWITCHES:
		text += ", and the playfield sheet draws a capacitor across it"
	return text + "."


def three_bank_provenance_status(address: int) -> str:
	return "conflicted" if address in CONFLICTED_SWITCHES else "validated"


def build_inputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SERVICE_SWITCHES.items()):
		refs = {"manual-and-harness": (MANUAL_SOURCE, SELF_TEST_CARD_SOURCE, CORE_SOURCE, SELF_TEST_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, COIN_SOURCE),
			"mpu-s33": (MANUAL_SOURCE, CORE_SOURCE, IPDB_SOURCE),
			"core": (CORE_SOURCE,)}[spec["evidence"]]
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		if spec.get("virtual"):
			# An emulator route with no fitted contact: no polarity, switch type, location or role.
			inputs.append({
				"aliases": aliases,
				"availability": spec["availability"],
				"binding": {"device": address, "group": "pinmame.input.switch"},
				"id": spec["id"],
				"kind": "virtual",
				"label": spec["label"],
				"physical": {"notes": spec["notes"]},
				"provenance": provenance(*refs),
				"spatial": not_applicable("virtual", CORE_SOURCE),
			})
			continue
		if spec.get("manual_address"):
			aliases.append({"namespace": "manual.address", "value": spec["manual_address"]})
		service: dict[str, Any] = {
			"aliases": aliases,
			"availability": spec["availability"],
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": {"location": spec["location"], "notes": spec["notes"], "switch_type": "button"},
			"provenance": provenance(*refs),
			"pulse": False,
			"roles": spec["roles"],
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		}
		if "quantity" in spec:
			service["physical"]["quantity"] = spec["quantity"]
		if spec.get("wiring"):
			service["wiring"] = dict(spec["wiring"])
		inputs.append(service)

	for address in sorted(data.SWITCHES):
		spec = data.SWITCHES[address]
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.switch", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.self-test", "value": str(address)})
		if spec.get("unused"):
			inputs.append({
				"aliases": aliases,
				"availability": "unused",
				"binding": {"device": address, "group": "pinmame.input.switch"},
				"id": spec["id"],
				"kind": "switch",
				"label": spec["label"],
				"normally_closed": False,
				"physical": {"notes": spec["notes"], "switch_type": "other"},
				"provenance": provenance(MANUAL_SOURCE, SELF_TEST_CARD_SOURCE, SWITCH_TEST_SOURCE),
				"pulse": False,
				"spatial": not_applicable("unused", MANUAL_SOURCE, SELF_TEST_CARD_SOURCE),
			})
			continue
		cabinet = bool(spec.get("cabinet"))
		refs = [MANUAL_SOURCE, SELF_TEST_CARD_SOURCE, SWITCH_TEST_SOURCE, *runs_exercising_switch(observations, address)]
		if not cabinet:
			refs += [SCRIPT_SOURCE, STANDALONE_SOURCE]
		physical: dict[str, Any] = {"switch_type": spec["type"]}
		if cabinet:
			sheet = (f"cabinet sheet: `{spec['cabinet_cell']}`; " + ("the playfield sheet draws an unlabelled contact in this cell" if spec["matrix"] is None
				else f"playfield sheet: `{spec['matrix']}`"))
		else:
			sheet = f"playfield sheet: `{spec['matrix']}`"
		physical["notes"] = f"Self-test card: `{spec['card']}`; {sheet}. {switch_construction(address, cabinet)} " + spec["notes"]
		if "quantity" in spec:
			physical["quantity"] = spec["quantity"]
		status = three_bank_provenance_status(address)
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": physical,
			"provenance": provenance(*refs, status=status),
			"pulse": bool(spec.get("pulse", False)),
			"wiring": matrix_wiring(address, cabinet),
		}
		if spec.get("initial_active"):
			item["initial_active"] = True
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if cabinet:
			physical["location"] = spec.get("location", "Coin door and cabinet")
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SELF_TEST_CARD_SOURCE)
		elif address in data.SWITCH_OBJECTS:
			names, projection = data.SWITCH_OBJECTS[address]
			# A baked-mesh primitive's centre comes from the world-space exports, which the extraction source pins.
			mesh_refs = [EXTRACTION_SOURCE] if any(data.OBJECTS[name][0] == "Primitive" for name in names) else []
			item["spatial"] = located(spec["id"], "sensor", [[name] for name in names], *TABLE_REFS, MANUAL_SOURCE, *mesh_refs,
				status="conflicted" if address in CONFLICTED_SWITCHES else "observed")
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE, *mesh_refs]))
			if address in CONFLICTED_SWITCHES:
				physical["notes"] += " " + projection
			else:
				physical["notes"] += " Placed on the retained table's " + " and ".join(f"{data.OBJECTS[name][0]} `{name}`" for name in names) + ", which its script binds to this address."
				if projection:
					physical["notes"] += " " + projection
		else:
			physical["location"] = "Outhole under the apron"
			physical["notes"] += (" Not placed: both known-working scripts and the retained table model the outhole as a one-ball virtual stack (`bsTrough.Initsw 0,33,0,0,0,0,0,0`) that "
				"their `DRAIN` kicker fills and their shooter-lane `BallRelease` kicker empties, so no table object marks this switch, and the playfield parts drawing does not show the outhole.")
		inputs.append(item)

	for address, (identifier, label, role, wire, connection) in sorted(data.FLIPPER_BUTTONS.items()):
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": identifier,
			"kind": "switch",
			"label": label,
			"normally_closed": False,
			"physical": {
				"location": "Cabinet side",
				"notes": "PinMAME's synthetic cabinet flipper button position (FLIP_SW(FLIP_L)). The physical button is hard-wired through the flipper enable relay's contact to its side's flipper coil, "
					f"not to the switch matrix, so the self-test card's switch list does not name it. The cabinet sheet draws `{label.split()[0].upper()} FLIPPER` from {connection} ({wire}) and the two "
					"buttons' common return to A2J2-9 (O). The retained gameplay run shows PinMAME's flipper outputs answering this address.",
				"quantity": 1,
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, *runs_exercising_switch(observations, address)),
			"pulse": False,
			"roles": [role],
			"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
			"wiring": {"board": "Hard-wired flipper button circuit through the SDU flipper enable relay", "control_wire": wire, "control_connection": connection,
				"return_wire": "O", "return_connection": "A2J2-9"},
		})
	for address, (identifier, label) in sorted(data.UNUSED_FLIPPER_POSITIONS.items()):
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "unused",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": identifier,
			"kind": "switch",
			"label": label,
			"normally_closed": False,
			"physical": {
				"notes": "PinMAME's generic upper flipper button position. Meteor has two cabinet flipper buttons (cabinet sheet `LEFT FLIPPER` and `RIGHT FLIPPER`); its upper right flipper has no "
					"button of its own but hangs off the right flipper's drive (playfield coil sheet), and the driver declares FLIP_SW(FLIP_L) only, so nothing reaches this position.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
		})

	coin_dips = {*range(1, 6), *range(9, 14), *range(17, 20), *range(28, 31)}
	for address in sorted(data.DIPS):
		refs = [MANUAL_SOURCE, CORE_SOURCE] + ([COIN_SOURCE] if address in coin_dips else []) + ([GAMEPLAY_SOURCE] if address == 7 else [])
		inputs.append({
			"aliases": [{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": "S%d" % address}],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": data.DIPS[address],
			"physical": {
				"location": "MPU module option-switch packages in the backbox",
				"notes": "One of the thirty-two MPU option switches (Figure 1 `DETAIL S1-S32 MPU ASS'Y.`). The assignment is the `METEOR SWITCH ASSIGNMENT` list on PDF page 10 and the charts on PDF "
					"pages 11-15; every one of the 32 is assigned. Pinned PinMAME's BY35_COMPORTS defaults S20 (credit display) and S21 (match) to ON and the other thirty to OFF: the retained runs at "
					"that default play three-ball games (switch 7 OFF), credit the center chute's first coin with one credit and its second with two (switches 1-5 all OFF, `3/2 COINS`), stop "
					"crediting at 5 (switches 17-19 all OFF), show the credits and play the match."
					+ (" PinMAME's default for this switch is ON." if address in (20, 21) else " PinMAME's default for this switch is OFF.")
					+ data.DIP_NOTES.get(address, ""),
				"switch_type": "dip",
			},
			"provenance": provenance(*refs),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})

	for side, address, button in (("left", 1, 84), ("right", 2, 82)):
		identifier = f"switch.{side}-flipper-end-of-stroke-contact" + ("s" if side == "right" else "")
		objects = data.DIRECT_OBJECTS[address]
		quantity = len(objects)
		extra = ("" if side == "left" else " The right button works two flippers: the sheet draws the upper right flipper with the same two windings and winding-shunt contact, and feeds it "
			"from the right flipper's drive through a separate series contact labelled `E.O.S.` (physical direct input 6). These two winding-shunt contacts are unlabelled on the sheet.")
		inputs.append({
			"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
			"availability": "used",
			"binding": {"device": address, "group": "physical.input.direct"},
			"id": identifier,
			"kind": "switch",
			"label": f"{side.title()} flipper end-of-stroke contact" + ("s (lower and upper flipper)" if side == "right" else ""),
			"normally_closed": True,
			"physical": {
				"location": f"{side.title()} flipper assembl" + ("ies" if side == "right" else "y"),
				"notes": "Hard-wired contact of the dual-winding flipper coil, not a PinMAME switch address. The playfield coil sheet draws each flipper as two windings in series with a contact "
					"from the top node to the middle node, across the first winding: the end-of-stroke contact of a dual-winding flipper, which conducts at rest and opens at the end of the stroke "
					f"to insert the hold winding (normally closed).{extra} Placed by projection on the retained table's " + " and ".join(f"`{name}`" for name in objects)
					+ " pivot" + ("s" if quantity > 1 else "") + ", because the contact is mounted on its flipper assembly and has no object of its own.",
				"quantity": quantity,
				"switch_type": "leaf",
			},
			"provenance": provenance(MANUAL_SOURCE),
			"pulse": False,
			"spatial": located(identifier, "sensor", [[name] for name in objects], TABLE_SOURCE, MANUAL_SOURCE),
		})
	inputs.append({
		"aliases": [{"namespace": "manual.address", "value": "E.O.S."}],
		"availability": "used",
		"binding": {"device": 6, "group": "physical.input.direct"},
		"id": "switch.upper-right-flipper-series-eos-contact",
		"kind": "switch",
		"label": "Upper right flipper series E.O.S. contact",
		"normally_closed": False,
		"physical": {
			"notes": "Hard-wired contact, not a PinMAME switch address. The playfield coil sheet draws the upper right flipper with no drive line of its own: its lower end joins the right "
				"flipper's drive node (A3J1-8, O) through a contact labelled `E.O.S.`, the only contact on the sheet that carries a label, drawn with the open-contact symbol (two plates and a gap) "
				"rather than the flag symbol of the winding-shunt contacts. The upper right coil is therefore energized only while this contact is closed (normally open as drawn). The sheet does "
				"not say which flipper assembly carries it or when it closes; a contact that closes at the end of the lower right flipper's stroke would fire the upper right flipper just after "
				"the lower one, but no retained source confirms that. PinMAME and both known-working scripts drive the two right flippers together from one callback, and nothing reports this "
				"contact. Not placed: no source locates it.",
			"quantity": 1,
			"switch_type": "leaf",
		},
		"provenance": provenance(MANUAL_SOURCE),
		"pulse": False,
	})
	return inputs


# --- Outputs ------------------------------------------------------------------------------------------------------------


def build_solenoid_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	public_to_physical = {public: number for number, public in data.PHYSICAL_TO_PUBLIC.items()}
	for address, spec in sorted(data.SOLENOIDS.items()):
		number = public_to_physical[address]
		connection, wire, load = data.SDU_LOADS[number]
		if "letter" in spec and load != KNOCK_DOWN_LOADS[spec["letter"]]:
			raise RuntimeError(f"public {address}: the ROM test pairs SDU load `{load}`, not the knock-down coil of switch {spec['letter']}")
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		aliases += [{"namespace": "manual.self-test", "value": str(number)}, {"namespace": "manual.address", "value": f"SDU-Q{number}"}]
		refs = [MANUAL_SOURCE, SOLENOID_TEST_SOURCE, *runs_seeing_solenoid(observations, address)]
		if number in data.CARD_SOLENOIDS:
			refs.insert(1, SELF_TEST_CARD_SOURCE)
		if address not in UNSCRIPTED_SOLENOIDS:
			refs += [SCRIPT_SOURCE, STANDALONE_SOURCE]
		if spec.get("vpm_library"):
			refs.append(VPM_LIBRARY_SOURCE)
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
			physical["quantity"] = 1
		card = f"the self-test card lists solenoid {number:02d} as `{data.CARD_SOLENOIDS[number]}`" if number in data.CARD_SOLENOIDS else f"the self-test card lists no solenoid {number:02d}"
		printed_wire = f", {data.SDU_PRINTED_WIRES.get(number, wire)}" if wire else ""
		physical["notes"] = (f"SDU driver Q{number}, printed load `{load}` ({connection}{printed_wire}) on the Solenoid Driver schematic 12B-432-S113; {card}. The ROM's solenoid test shows "
			f"{number:02d} while public {address} fires. " + spec["notes"] + spec.get("wire_note", ""))
		if spec.get("on_board_relay"):
			# The relay sits on the SDU: Q15 drives coil terminal 8 on the board, and the connector pin the sheet prints feeds coil terminal 7.
			wiring: dict[str, Any] = {"board": BOARD_SDU, "driver_transistor": f"Q{number}", "power_connection": f"A3{connection}"}
			if wire:
				wiring["power_wire"] = wire
		else:
			wiring = {"board": BOARD_SDU, "driver_transistor": f"Q{number}", "drive_connection": f"A3{connection}"}
			if wire:
				wiring["drive_wire"] = wire
		if not spec.get("unused"):
			# Every SDU driver switches its load to the 43 VDC supply's return (`+43V SOLENOID GND`); the transformer sheet routes 43 VDC to the playfield solenoid
			# bus (A2J1-6), the cabinet's coin lock-out and knocker bus (A2J2-2) and the flipper enable relay bus.
			wiring.update({"nominal_voltage_v": 43, "voltage_type": "dc"})
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "unused" if spec.get("unused") else "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": wiring,
		}
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if spec.get("unused"):
			physical["location"] = "Solenoid driver board in the backbox"
			item["spatial"] = not_applicable("unused", MANUAL_SOURCE, SELF_TEST_CARD_SOURCE)
		elif spec.get("cabinet"):
			physical["location"] = "Cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif spec.get("internal"):
			physical["location"] = "Backbox"
			item["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address in data.SOLENOID_OBJECTS:
			names, projection = data.SOLENOID_OBJECTS[address]
			groups = [names] if projection and len(names) > 1 else [[name] for name in names]
			item["spatial"] = located(spec["id"], "effect", groups, *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SOURCE, TABLE_SCRIPT_SOURCE]))
			if projection:
				physical["notes"] += " " + projection
			else:
				physical["notes"] += f" Placed on the retained table's {data.OBJECTS[names[0]][0]} `{names[0]}`, the thumper bumper whose own hit kicks the ball in that table."
		else:
			physical["location"] = "Outhole under the apron"
			physical["notes"] += (" Not placed: both known-working scripts and the retained table kick the ball from a virtual stack into the shooter lane with a `BallRelease` kicker, so no "
				"table object marks the coil, and the playfield parts drawing does not show the outhole.")
		outputs.append(item)

	for address, spec in sorted(data.FLIPPERS.items()):
		power = spec["power"]
		right = spec["side"] == "right"
		pins = ("The SDU sheet prints the coil return as J1-9 [O] for the right and J1-8 [G] for the left flipper; the playfield coil sheet prints the same colours on the other pins "
			"(`LEFT FLIPPER A3J1-9 (-G-)`, `RIGHT FLIPPER A3J1-8 (-O-)`), a connector-pin reading only, and the definition follows the SDU sheet.")
		upper = (" The upper right flipper has no drive line of its own: the playfield coil sheet joins its lower end to the right flipper's drive through a symbol labelled `E.O.S.`, so the right "
			"button and public 46 work both right flippers, and both known-working scripts' right flipper callback moves both `RightFlipper` and `RightFlipper001`." if right else "")
		outputs.append({
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				*({"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)),
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": "coil",
			"label": spec["label"],
			"physical": {
				"part_number": spec["parts"],
				"quantity": spec["quantity"],
				"notes": (f"{'The lower right flipper and the upper right flipper' if right else 'The left flipper'} (parts list `Flipper Left & Right (2)` J-25-500/34-4500"
					+ ("; `Flipper Top` J-25-600/34-4500" if right else "") + ") "
					+ ("are dual-winding coils" if right else "is a dual-winding coil") + " hard-wired from the +43 VDC flipper supply A2J1-6 (BLU-W) through the flipper enable relay's contact "
					f"to the {spec['side']} cabinet button; no numbered solenoid driver drives {'them' if right else 'it'}. {pins}{upper} Public {address} is PinMAME's synthetic held-coil output "
					f"for the {spec['side']} side (FLIP_SW(FLIP_L)); PinMAME also asserts public {power} for the same interval. Both outputs are button states, not measurements of any winding. "
					"Placed on the retained table's " + " and ".join(f"`{name}`" for name in spec["objects"]) + " pivot" + ("s" if right else "") + ", which its flipper callback moves."),
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, *runs_seeing_solenoid(observations, address), SCRIPT_SOURCE, STANDALONE_SOURCE, TABLE_SCRIPT_SOURCE),
			"spatial": located(spec["id"], "effect", [[name] for name in spec["objects"]], *TABLE_REFS, MANUAL_SOURCE),
			"wiring": {
				"board": "Hard-wired flipper circuit gated by the flipper enable relay (public 19)",
				"control_connection": spec["button_conn"],
				"control_wire": spec["button_wire"],
				"drive_connection": spec["conn"],
				"drive_wire": spec["wire"],
				"nominal_voltage_v": 43,
				"power_connection": "A2J1-6",
				"power_wire": "BLU-W",
				"voltage_type": "dc",
			},
		})
		outputs.append({
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(power)}],
			"availability": "used",
			"binding": {"device": power, "group": "pinmame.output.solenoid"},
			"id": f"output.{spec['side']}-flipper-power-state",
			"kind": "virtual",
			"label": f"{spec['side'].title()} synthetic flipper power state",
			"physical": {"notes": f"PinMAME's synthetic power-winding state for the {spec['side']} side, asserted and released together with public {address} for the whole enabled button closure "
				"(retained gameplay and variant runs). It is not another coil and does not measure the power winding."},
			"provenance": provenance(CORE_SOURCE, *runs_seeing_solenoid(observations, power)),
			"spatial": not_applicable("virtual", CORE_SOURCE, GAMEPLAY_SOURCE),
		})
	return outputs


def _jack(text: str) -> str:
	return text.replace("-", "")


def lamp_rows() -> dict[int, list[tuple[int, str, str, str, str]]]:
	"""Public lamp address -> its lamp-list rows (row, description, wire, jack, pin)."""
	rows: dict[int, list[tuple[int, str, str, str, str]]] = {}
	for row, description, wire, jack, pin, public in data.LAMP_LIST:
		rows.setdefault(public, []).append((row, description, wire, _jack(jack), pin))
	if set(rows) != set(data.LAMP_TO_Q):
		raise RuntimeError("Meteor's lamp list does not name the sixty SCR outputs")
	return rows


def excerpt_connector_blocks(root: Path) -> dict[str, list[tuple[str, int]]]:
	"""The lamp driver's J1-J3 connector blocks as the committed excerpt transcribes them: jack -> [(printed pin cell, SCR)] in printed order."""
	blocks: dict[str, list[tuple[str, int]]] = {}
	jack = None
	for line in (root / EXCERPT_ROOT / "lamp-driver.md").read_text(encoding="utf-8").splitlines():
		heading = re.match(r"^### (J[123]) ", line)
		if heading:
			jack = heading.group(1)
			blocks[jack] = []
		elif line.startswith("#"):
			jack = None
		elif jack and line.startswith("|"):
			cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
			if cells[0].isdigit() and re.fullmatch(r"Q\d+", cells[2]):
				blocks[jack].append((cells[1], int(cells[2][1:])))
	return blocks


def branch_reading(jack: str, pin: str) -> str:
	"""How a lamp note must quote a connector-block entry: a legible pin plainly, a cell with any illegible part verbatim in backticks."""
	return f"{jack} pin {pin}" if pin.isdigit() else f"{jack} pin `{pin}`"


def block_entries(q: int) -> list[tuple[str, str]]:
	return [(jack, pin) for jack, entries in data.CONNECTOR_BLOCKS.items() for pin, scr in entries if scr == q]


def unlisted_branches(public: int) -> list[tuple[str, str]]:
	"""Connector-block entries of a lamp's SCR that no lamp-list row of that lamp uses."""
	listed = {(jack, pin) for _, _, _, jack, pin in lamp_rows()[public]}
	return [entry for entry in block_entries(data.LAMP_TO_Q[public]) if entry not in listed]


def check_lamp_pairings() -> None:
	"""Compare each lamp's list rows and its SCR's connector-block entries both ways: a disagreement either way needs a pairing note, except a fully legible extra
	branch beside a matching row, which build_lamp_outputs states on the lamp."""
	rows = lamp_rows()
	for public, items in sorted(rows.items()):
		entries = block_entries(data.LAMP_TO_Q[public])
		if not entries:
			raise RuntimeError(f"lamp {public}: the connector blocks print no entry for Q{data.LAMP_TO_Q[public]}")
		if any((jack, pin) not in entries for _, _, _, jack, pin in items) and public not in data.PAIRING_NOTES:
			raise RuntimeError(f"lamp {public}: list rows {items} disagree with the connector block {entries} and no pairing note explains it")
		extra = unlisted_branches(public)
		if extra and public not in data.PAIRING_NOTES and any("?" in pin or not pin for _, pin in extra):
			raise RuntimeError(f"lamp {public}: the connector block's unlisted entries {extra} are not legible and no pairing note explains them")
	for public in data.PAIRING_NOTES:
		if public not in rows:
			raise RuntimeError(f"pairing note for an unknown lamp {public}")
	for public, (jack, pin) in LAMP_CONNECTION_OVERRIDES.items():
		if (jack, pin) not in block_entries(data.LAMP_TO_Q[public]) or public not in data.PAIRING_NOTES:
			raise RuntimeError(f"lamp {public}: the drive-connection override is not the connector block's reading")


BACKGLASS_EXTRAS = {
	61: " The VR callback also dims the VR room's backglass while this lamp is on (`VR_Backbox_Backglass.blenddisablelighting` 0.5, and 2 while it is off).",
	63: " The VR callback also hides the Ball In Play flasher `FlBGL29` while this lamp is on and shows it while it is off.",
}


def states_branch(notes: str, jack: str, pin: str) -> bool:
	"""Whether ``notes`` quotes this connector-block entry as printed, as a whole pin token (``J3 pin 1`` is not stated by ``J3 pin 13``)."""
	return re.search(re.escape(branch_reading(jack, pin)) + r"(?![0-9])", notes) is not None


def build_lamp_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	check_lamp_pairings()
	rows = lamp_rows()
	named = observations["named_output_addresses"]
	drop_lamps = {data.SWITCHES[switch]["letter"]: lamp for (switch, _, lamp) in runtime_summary.METEOR_BANK.values()}
	for letter, (switch, _, lamp) in runtime_summary.METEOR_BANK.items():
		key = f"meteor-{letter.replace(' ', '-').lower()}-drop-lamp"
		if named.get(key) != lamp or "DROP" not in rows[lamp][0][1]:
			raise RuntimeError(f"the ROM's {letter} drop lamp is not public {lamp}, a printed drop-lamp row")
	spot = {named[f"switch-{switch}-spot-lamp"]: switch for switch in runtime_summary.SPOT_STEPS}
	outside = set(observations["lamp_addresses_driven_outside_self_test"])
	letter_by_lamp = {lamp: letter for letter, lamp in drop_lamps.items()}
	outputs: list[dict[str, Any]] = []
	for address in sorted(data.LAMP_TO_Q):
		q = data.LAMP_TO_Q[address]
		k, a = divmod(address - 1, 16)
		identifier, label = data.LAMP_NAMES[address]
		items = rows[address]
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.address", "value": f"LDA-Q{q}"})
		connections = [LAMP_CONNECTION_OVERRIDES[address]] if address in LAMP_CONNECTION_OVERRIDES else list(dict.fromkeys((jack, pin) for _, _, _, jack, pin in items))
		aliases += [{"namespace": "manual.address", "value": f"LDA-{jack}-{pin}"} for jack, pin in connections]
		printed = "; ".join(f"row {row} `{description}` ({wire}, {jack} pin {pin})" for row, description, wire, jack, pin in items)
		notes = (f"Lamp Driver SCR Q{q}, decoder U{k + 1} output S{a} (Lamp Driver schematic 12B-431S-113, lettered for this game); a discrete SCR output on the LDA-100, not a lamp matrix. "
			f"The lamp list prints {printed}.")
		if address in data.PAIRING_NOTES:
			notes += " " + data.PAIRING_NOTES[address]
		else:
			extra = unlisted_branches(address)
			if extra:
				notes += (" The connector block also prints SCR Q%d on %s, a branch no lamp-list row uses; no bulb is asserted on it." % (q, " and ".join(branch_reading(*entry) for entry in extra)))
		# Every branch of this SCR that no row of this lamp prints is quoted as the block prints it, whether a pairing note or the sentence above states it.
		for jack, pin in unlisted_branches(address):
			if not states_branch(notes, jack, pin):
				raise RuntimeError(f"lamp {address}: the connector block's {jack} entry `{pin}` for Q{q} is not stated on the lamp")
		if address in letter_by_lamp:
			letter = letter_by_lamp[address]
			if letter == "R":
				notes += (" The ROM proves the pairing: in the retained gameplay run the R target completed the bank, and at the drain the ROM restored the made targets with exactly the knock-down "
					"coils whose drop lamps were out, R's (public 14) among them with this lamp.")
			else:
				notes += f" The ROM proves the pairing: in the retained gameplay run this lamp went out when the METEOR {letter} target went down and was the only lamp that stayed out through the end of that step."
		if address in spot:
			notes += f" The ROM proves the pairing: in the retained gameplay run switch {spot[address]} put this lamp out as it fired a knock-down coil to spot a METEOR target."
		if address in data.SCRIPT_LIGHTS and data.SCRIPT_LIGHTS[address]:
			notes += (" Both known-working scripts and the retained table drive " + " and ".join(f"`{name}` ({normalized_text(x, y)})" for name, x, y in data.SCRIPT_LIGHTS[address])
				+ " from this lamp.")
		if address not in outside:
			notes += LAMPS_ONLY_IN_SELF_TEST_NOTE
		refs = [MANUAL_SOURCE, *runs_seeing_lamp(observations, address)]
		physical: dict[str, Any] = {"part_number": "#44 (8A-101)", "notes": notes}
		wires = list(dict.fromkeys(wire for _, _, wire, _, _ in items))
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": identifier,
			"kind": "lamp",
			"label": label,
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": {"board": BOARD_LDA, "driver_transistor": f"Q{q}", "drive_connection": "; ".join(f"A5{jack}-{pin}" for jack, pin in connections), "drive_wire": "; ".join(wires)},
		}
		if address in data.BACKBOX_LAMPS:
			physical["location"] = "Backbox"
			physical["notes"] += (" A backbox lamp: the row names a backglass feature (the operating text names the `\"Game Over\" light` and the `\"Match\" light`), and both known-working scripts "
				"and the retained table show it only on the backglass: in their desktop mode (`VR_Room = 0` with `cab_mode = 0`) as the desktop backglass reel `L" + str(address)
				+ "` (`FadeReel`), and in their VR room mode (`VR_Room = 1`) as the flasher `FlBGL" + str(address) + "` from the `UpdateMultipleLamps` lamp callback. All three ship in "
				"cabinet mode (`VR_Room = 0`, `cab_mode = 1`), which shows neither." + BACKGLASS_EXTRAS.get(address, ""))
			item["roles"] = ["cabinet.backglass"]
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			item["provenance"] = provenance(*refs, SCRIPT_SOURCE, STANDALONE_SOURCE)
		else:
			physical["notes"] += (" Not placed: the retained table, the only one available, draws its inserts with lights that show no bulb mesh, and the manual's playfield parts drawing draws "
				"the insert circles without lamp numbers, so no source marks the socket.")
			item["provenance"] = provenance(*refs, SCRIPT_SOURCE, STANDALONE_SOURCE, TABLE_SCRIPT_SOURCE)
		outputs.append(item)
	return outputs


def build_gi() -> dict[str, Any]:
	placements = []
	for index, (x, y, _) in enumerate(sorted(data.GI_BULBS, key=lambda bulb: (bulb[1], bulb[0])), start=1):
		nx, ny = normalize(x, y)
		placements.append({"id": f"gi.general-illumination.emitter.{index}", "role": "emitter", "space": "playfield", "x": nx, "y": ny,
			"provenance": provenance(TABLE_SOURCE, EXTRACTION_SOURCE, status="observed")})
	return {
		"aliases": [],
		"availability": "used",
		"binding": {"device": 1, "group": "physical.output.gi"},
		"id": "gi.general-illumination",
		"kind": "gi",
		"label": "Uncontrolled general illumination",
		"physical": {
			"notes": "Transformer-fed general illumination with no controller address. The playfield sheet draws `GEN. ILLUM` from A2J1-8 (W) at `6 VAC`, returning on A2J1-1 (R); the "
				"transformer schematic 12B-16B-6 takes the GEN. ILL. buses off its 7.3 VAC winding (terminals 17 and 18, fuse F5 20 A): the playfield bus on J1-8 (W), the cabinet bus on J2-1 "
				"(Y-B, return J2-5 G-R) and the backbox buses on J3-10 (O) and J3-11 (R) (returns J3-1 G and J3-2 W). The two sheets print 6 VAC and 7.3 VAC for the same bus; no relay, "
				"transistor or other switching device is drawn in any of these lines. No sheet prints a bulb count or position; the parts list gives only `Bulbs, #44` 8A-101. "
				f"Placed on the {len(placements)} connected pieces of the retained table's baked bulb mesh `layer1bulbs`, each with one of its general-illumination lights (`Light<n>`) within 3.6 VPX "
				"units of its centre; the table's grouping is render membership, not the machine's wiring, so no quantity is asserted, and its backbox and cabinet bulbs are not placed.",
		},
		"provenance": provenance(MANUAL_SOURCE, TABLE_SOURCE, EXTRACTION_SOURCE),
		"spatial": {"status": "observed", "placements": placements},
		"wiring": {"board": "Transformer/rectifier A2, uncontrolled general-illumination buses", "power_connection": "A2J1-8 (playfield); J2-1 (cabinet); J3-10, J3-11 (backbox)",
			"return_connection": "A2J1-1; J2-5; J3-1, J3-2", "voltage_type": "ac", "nominal_voltage_v": 6},
	}


def build_outputs(observations: dict[str, Any]) -> list[dict[str, Any]]:
	outputs = build_solenoid_outputs(observations) + build_lamp_outputs(observations) + [build_gi()]
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


# --- Mechanisms, relationships --------------------------------------------------------------------------------------------


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str, part: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"actuators": actuators, "behavior": behavior, "id": identifier, "kind": kind, "label": label, "provenance": provenance(*sources), "sensors": sensors}
	if part:
		item["assembly_part_number"] = part
	return item


KNOCK_DOWN = {spec["letter"]: address for address, spec in data.SOLENOIDS.items() if "letter" in spec}
# bank, label, matrix switches, reset device, reset public, missile row, playfield-parts callout (item 2 `3-BANK TARGET D-580-1 to 3`)
THREE_BANKS = (
	("right", "Right three-target drop bank", (9, 10, 11), "device.right-bank-reset", 9, "the right missile row (rocket 3: the first hit lit public 54, its 1K lamp)", 3),
	("top-left", "Top left three-target drop bank", (19, 20, 21), "device.top-left-bank-reset", 3, "the middle missile row (rocket 2: the first hit lit public 52, its 1K lamp)", 2),
	("lower-left", "Lower left three-target drop bank", (22, 23, 24), "device.lower-left-bank-reset", 7, "the left missile row (rocket 1: the first hit lit public 50, its 1K lamp)", 1),
)


def build_mechanisms() -> list[dict[str, Any]]:
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	items = [
		mechanism(
			"mech.outhole", "Single-ball outhole and shooter feed", "kicker", ["device.outhole-kicker"], ["switch.outhole"],
			"Meteor holds one ball. A drained ball rests on the outhole switch (public 33) under the apron in front of the outhole kicker (public 15, `Outhole Kicker (1)` J-26-1100), which kicks "
			"it into the shooter lane. Pressing the credit button with credits makes the outhole kicker move the ball to the shooter lane (manual, which "
			"resets the drop targets in its power-on description); in the retained runs the ROM raises the flipper enable relay (19) at the start of a game and fires the outhole kicker "
			"followed by the four bank resets in sequence (15, then 3, 7, 9 and 13, about 0.6 s from the kick to the last reset) and repeats that sequence about every 1.7 s while 33 "
			"stays closed. After a drain that leaves play to continue, the bonus is added "
			"to the score (a tilted ball forfeits it, manual), the player or ball advances, the METEOR targets that player had made are restored with their knock-down coils (the bank's memory, manual), and the kicker "
			"serves again; "
			"an extra ball is played without advancing. After the last ball's drain the retained gameplay trace records no kicker pulse in the 30 s the host then holds 33 closed "
			"before crediting the next game, so the ball stays in the outhole. Both scripts model "
			"the outhole as a one-ball virtual stack and serve from a shooter-lane kicker.",
			MANUAL_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, *VARIANT_SOURCES,
		),
		mechanism(
			"mech.meteor-bank", "Six-target METEOR memory drop bank", "drop_target_bank",
			["device.meteor-bank-reset", *(data.SOLENOIDS[KNOCK_DOWN[switch]]["id"] for switch in (32, 31, 30, 29, 28, 27))],
			[switch_id[address] for address in (32, 31, 30, 29, 28, 27)],
			"Six drop targets spelling M-E-T-E-O-R from left to right (switches 32, 31, 30, 29, 28 and 27; `6-BANK TARGET D-548-6A`) on one reset coil (public 13, B-27-2300), and each with its own "
			"knock-down coil (C1-34-3400; M 4, first E 5, T 8, second E 11, O 12, R 14). A target's switch is closed while it is down. Home state: all six up. Each target's drop lamp (M 58, first "
			"E 42, T 26, second E 10, O 57, R 41) is lit while it still has to be made and goes out when it falls (retained gameplay run). The end targets score 6,000 and the middle ones 2,000, "
			"and each down target adds to the spinner value; completing the bank resets it, advances the bonus multiplier (1X, 2X, 3X, 4X, 5X, 6X, 7X, carried over up to 6X) and relights the drop "
			"lamps. Lit star rollovers, lit return lanes and the lit stationary target spot a target (manual): the ROM fires that target's knock-down coil, as the retained gameplay run shows for "
			"the stand-up target and the upper and lower star rollovers (switches 4, 38 and 40); the middle rollover and both return lanes were closed there with their spot lamps already out. The bank has memory: "
			"`The status of the target is restored for each player after the ball enters the outhole and the bonus is collected` (manual). After the first drain of the retained single-player "
			"gameplay run the ROM fired exactly the knock-down coils of the targets whose drop lamps were out (T, second E, O and R); no run exercised a player change. "
			"From the 5th or 6th reset (adjustable) a lamp steps across the bank and a lit target can award an extra ball (manual).",
			MANUAL_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, part="D-548-6A",
		),
	]
	for bank, label, switches, reset, public, row, callout in THREE_BANKS:
		items.append(mechanism(
			f"mech.{bank}-three-bank", label, "drop_target_bank", [reset], [switch_id[address] for address in switches],
			f"Three drop targets (switches {switches[0]}, {switches[1]} and {switches[2]} in matrix order) on one reset coil (public {public}, B-27-2300) and no knock-down coils. The playfield "
			f"parts drawing calls this bank `2-{callout}` and its list prints item 2 as `3-BANK TARGET D-580-1 to 3`, so this bank is D-580-{callout} (the dash number read by matching the "
			"callout suffix, as the drawing pairs the bumper caps with `13A-32-1 & 3`)."
			" Home state: all up. The playfield sheet prints the three cells as top, lower and middle target; the known-working scripts bind them as top, middle and lower, and "
			"the conflict record keeps that open. Each hit advances one lamp of "
			f"{row} and scores the advanced value; when all three are down the ROM fires the reset, and it repeats the reset about every 1.2 s while the host holds all three targets down (retained gameplay run). When all three missile values "
			"are equal a rotating WOW (extra ball) lights, and the special the bank lights is awarded on its center target (manual).",
			MANUAL_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, GAMEPLAY_SOURCE, part=f"D-580-{callout}",
		))
	items += [
		mechanism(
			"mech.thumper-bumper", "Thumper (pop) bumper", "kicker", ["device.thumper-bumper"], [switch_id[14]],
			"One thumper bumper left of center (`Thumper Bumper (1) J-26-1200`; `THUMPER CAP 4A-134-R`). The ROM fires public 2 when switch 14 closes (retained gameplay and variant runs); it scores "
			"1,000 in three-ball and 100 in five-ball games (manual).",
			MANUAL_SOURCE, GAMEPLAY_SOURCE, *VARIANT_SOURCES,
		),
		mechanism(
			"mech.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], [switch_id[16], switch_id[15]],
			"Two J-27-1700 slingshots. The ROM fires each coil when its switch closes: left switch 16 fires public 1 and right switch 15 fires public 10 (retained gameplay and variant runs); "
			"while the game was tilted the right slingshot fired nothing (retained gameplay run). Each scores 10 and, unless option switch 25 is ON, moves the lit WOW, special, spot, METEOR, outlane and bumper lamps (manual).",
			MANUAL_SOURCE, GAMEPLAY_SOURCE, *VARIANT_SOURCES,
		),
		mechanism(
			"mech.flippers", "Three dual-winding flippers on two buttons", "other", ["device.left-flipper", "device.right-flippers", "device.flipper-enable-relay"],
			["switch.left-flipper-button", "switch.right-flipper-button", "switch.left-flipper-end-of-stroke-contact", "switch.right-flipper-end-of-stroke-contacts",
				"switch.upper-right-flipper-series-eos-contact"],
			"A left and a right flipper at the bottom (`Flipper Left & Right (2)` J-25-500/34-4500) and an upper right flipper (`Flipper Top` J-25-600/34-4500; IPDB `Flippers (3)`). Each is a "
			"dual-winding coil fed from +43 VDC (A2J1-6) through a contact of the flipper enable relay (public 19, SDU driver Q15, CR20 across its coil) to its cabinet button. "
			"Each coil's winding-shunt end-of-stroke contact is closed at rest and opens at the end of the stroke to insert the hold winding. The upper right flipper has no button or drive line "
			"of its own: the playfield coil sheet joins its lower end to the right flipper's drive (A3J1-8) through a separate contact labelled `E.O.S.`, drawn as an open contact, so the right "
			"button works both and the upper right coil is energized only while that contact is closed. The sheet does not say which assembly carries the contact; a contact that closes at "
			"the end of the lower right flipper's stroke would fire the upper right flipper just after the lower one, but no retained source confirms it. PinMAME and both scripts drive the two "
			"right flippers together from one callback. The ROM energizes the relay when a game starts and drops it on a tilt and at game over (retained runs). PinMAME publishes 46 (right) and "
			"48 (left) with 45 and 47 alongside.",
			MANUAL_SOURCE, CORE_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.scoring-bumpers", "Two passive scoring bumpers", "other", [], [switch_id[12], switch_id[13]],
			"Two bumpers at the top with switches and no coil (IPDB `Passive bumpers (2)`; `BUMPER CAP 13A-32-1 & 3`): upper right (12) and upper left (13). They score 500 with no missile "
			"lamp advanced, otherwise the corresponding missile value, and advance missile rows 1 and 3 when lit (manual). Neither changed a lamp or solenoid in the retained gameplay run; the score display advanced and sound commands were sent.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.spinner", "Spinning target", "other", [], [switch_id[5]],
			"A spinning target at the upper right (`SPIN TARGET A-563-9`); each rotation closes switch 5 once and scores 200 plus 600 for each end and 200 for each middle METEOR target down; "
			"resetting the bank resets the value (manual). No coil or home sensor.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.stationary-target", "Center stationary target", "other", [], [switch_id[4]],
			"The stand-up target below the spinner (`TARGET ASS'Y A-461-2Y`; switch 4). It scores 500, plus 1,500 and a spotted METEOR target when lit, or awards the WOW or the special when those "
			"are lit (manual); in the retained gameplay run, with lamp 5 lit, it fired the METEOR O knock-down coil (12) and put lamp 5 out.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.passive-gates", "Passive ball gate", "gate", [], [],
			"The playfield parts list names a `BALL GATE, RIGHT A-104-R2` at the top right of the arch and `BALL GATE POST 2A-200` posts, with no coil or switch. They route the ball by its own "
			"motion; do not invent a powered diverter.",
			MANUAL_SOURCE,
		),
	]
	return items


def build_relationships() -> list[dict[str, Any]]:
	relationships = []
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	for source, destination in ((switch_id[16], "device.left-slingshot"), (switch_id[15], "device.right-slingshot"), (switch_id[14], "device.thumper-bumper")):
		relationships.append({"id": f"rel.{destination.split('.', 1)[1]}-fired-by-its-switch", "kind": "direct", "source": source, "destination": destination,
			"provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.outhole-kicker-follows-the-outhole-switch", "kind": "pulse", "source": switch_id[33], "destination": "device.outhole-kicker",
		"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	resets = [(reset, switches) for _, _, switches, reset, _, _, _ in THREE_BANKS] + [("device.meteor-bank-reset", (27, 28, 29, 30, 31, 32))]
	for actuator, switches in resets:
		for address in switches:
			relationships.append({"id": f"rel.{actuator.split('.', 1)[1]}-raises-target-{address}", "kind": "pulse", "source": actuator, "destination": switch_id[address],
				"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	for letter_switch, address in sorted(KNOCK_DOWN.items()):
		relationships.append({"id": f"rel.knock-down-coil-drops-target-{letter_switch}", "kind": "pulse", "source": data.SOLENOIDS[address]["id"], "destination": switch_id[letter_switch],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	for side, flipper in (("left", "device.left-flipper"), ("right", "device.right-flippers")):
		relationships.append({"id": f"rel.{side}-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": f"switch.{side}-flipper-button", "destination": flipper,
			"provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.sort(key=lambda item: item["id"])
	return relationships


# --- Conflicts ----------------------------------------------------------------------------------------------------------


def build_conflicts() -> list[dict[str, Any]]:
	return [{
		"description": "Which matrix position is the middle target of each three-target bank. The playfield sheet (manual PDF page 36) prints each bank's three cells, in matrix order, as the top, "
			"lower and middle target: `RT. 3-BANK` `TOP TARG.` (9), `LOWER TARG.` (10) and `MID. TARG.` (11), and the same order for the top left bank (19, 20, 21) and the lower left bank (22, 23, "
			"24). Both known-working scripts and the retained table bind them top, middle and lower: the object between each bank's top and bottom target writes 10, 20 and 23. Nothing else "
			"retained names a position: the self-test card lists each bank as one group (`9-11 3-Bank Drop-Targets (Right)`), and the playfield parts drawing does not number the switches. A "
			"recreation needs the answer because the special the ROM awards on a bank's center target (manual PDF page 15) follows the switch number. Resolution path: boot meteor with option "
			"switches 14, 31 and 32 set to a special award (14, 31 and 32 all OFF, PinMAME's default, is `No Award`), light a bank's special lamp (1, 3 or 23) and close each of the bank's two lower switches "
			"alone; the one that awards the special is the center target. tools/run_pinmame_harness.py cannot set option switches yet (libpinmame exports PinmameSetDIP), so the probe needs that "
			"input added; an owner can also open the switch test and press the middle target of each bank.",
		"id": "conflict.three-bank-middle-and-lower-target-switches",
		"path": "inputs[pinmame.input.switch:10|11|20|21|23|24]",
		"source_refs": [MANUAL_SOURCE, SCRIPT_SOURCE, STANDALONE_SOURCE, TABLE_SCRIPT_SOURCE],
	}]


# --- Sources ------------------------------------------------------------------------------------------------------------

# excerpt name -> (source key, locator)
EXCERPTS: dict[str, tuple[str, str]] = {
	"general-operation": (MANUAL_SOURCE, "PDF pages 2-4, I. INSTALLATION (tilt switches), Figure 1 and IV. GENERAL GAME OPERATION"),
	"self-test-and-bookkeeping": (MANUAL_SOURCE, "PDF pages 5-6, V. A. SELF TEST AND BOOKKEEPING FUNCTIONS and VI. FRONT DOOR GAME ADJUSTMENTS"),
	"feature-operation": (MANUAL_SOURCE, "PDF pages 8-9, drop target, bonus multiplier and feature scoring"),
	"switch-assignment": (MANUAL_SOURCE, "PDF pages 10-15, VIII. GAME ADJUSTMENTS, the METEOR SWITCH ASSIGNMENT list and the credit and option-switch charts"),
	"playfield-parts": (MANUAL_SOURCE, "PDF page 16, METEOR PLAYFIELD PARTS drawing and its lists"),
	"parts-list": (MANUAL_SOURCE, "PDF page 21, VIII. PARTS LIST - GAME #113 METEOR"),
	"solenoid-driver": (MANUAL_SOURCE, "PDF pages 24-25, SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC for METEOR 12B-432-S113"),
	"lamp-driver": (MANUAL_SOURCE, "PDF pages 28-29 and 37, Lamp Driver schematic 12B-431S-113 decoders and connector blocks, and the lamp list"),
	"cabinet-wiring": (MANUAL_SOURCE, "PDF pages 32-33, CABINET AND FRONT DOOR WIRING"),
	"general-illumination": (MANUAL_SOURCE, "PDF pages 34-36, TRANSFORMER SCHEMATIC 12B-16B-6 and the playfield GEN. ILLUM string"),
	"playfield-switch-matrix": (MANUAL_SOURCE, "PDF page 36, PLAYFIELD switch matrix"),
	"playfield-coil-wiring": (MANUAL_SOURCE, "PDF pages 36-37, PLAYFIELD flipper and coil wiring"),
	"interboard-wiring": (MANUAL_SOURCE, "PDF pages 22-23, WIRING DIAGRAM FOR SOLID STATE 12B-STD.-110-2: the A2 transformer J3 and MPU A4 J3 connector blocks"),
	"mpu-schematic": (MANUAL_SOURCE, "PDF pages 30-31, MPU 200 SCHEMATIC 12B-602-S: the title block and S33 at the MPU's NMI input"),
	"vpinmame-library": (VPM_LIBRARY_SOURCE, "stern.vbs GameOnSolenoid; core.vbs cvpmNudge.SolGameOn, the vpmFlips solenoid, its TiltObjects default, TiltSol and EnableFlippers, and the solenoid dispatch; the corpus script's settings"),
	"ipdb-schematic-errata": (IPDB_SOURCE, "The page's notes: `Schematic errors & omissions`"),
	"self-test-card": (SELF_TEST_CARD_SOURCE, "The single page: self test procedure, solenoid and switch identification and coin door switch drawings"),
}
REVIEWED_EXCERPTS: frozenset[str] = frozenset()
# Excerpts copied from retained text rather than read from scanned pages: (method, transcribed_by).
TEXT_EXCERPTS: dict[str, tuple[str, str]] = {
	"vpinmame-library": ("manual", "curator, copied verbatim from the retained stern.vbs and core.vbs and the corpus script; the retained-evidence test checks every quoted library line "
		"against the files"),
	"ipdb-schematic-errata": ("manual", "curator, copied verbatim from the text of the retained IPDB page; the retained-evidence test checks the quotation against the page"),
}
# Scanned-page excerpts read on renders other than the scan's own 300 dpi, as each excerpt's header states.
SCAN_EXCERPT_RENDERS: dict[str, str] = {
	"mpu-schematic": "250-600 dpi renders of the 300 dpi scan, the faint S33 label on the 600 dpi render",
}


def excerpt_record(name: str, root: Path) -> dict[str, Any]:
	_, locator = EXCERPTS[name]
	path = root / EXCERPT_ROOT / f"{name}.md"
	if not path.is_file():
		raise RuntimeError(f"Meteor excerpt is missing: {path}")
	reviewed = name in REVIEWED_EXCERPTS
	if name in TEXT_EXCERPTS:
		method, transcribed_by = TEXT_EXCERPTS[name]
	else:
		# The manual and the self-test card are 300 dpi scans without a text layer; the MPU sheet's faint S33 label was read on finer renders of it.
		method = "mixed"
		renders = SCAN_EXCERPT_RENDERS.get(name, "300 dpi page renders")
		transcribed_by = "curator, checked cell by cell against the rendered page" if reviewed else f"curator, read from {renders}; not yet checked cell by cell"
	return {
		"id": f"excerpt.meteor.{name}",
		"locator": locator,
		"method": method,
		"path": f"{EXCERPT_ROOT}/{name}.md",
		"reviewed": reviewed,
		"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
		"transcribed_by": transcribed_by,
	}


def excerpts_for(source: str, root: Path) -> list[dict[str, Any]]:
	return [excerpt_record(name, root) for name, (key, _) in EXCERPTS.items() if key == source]


def run_locator(name: str, scenario_sha256: str, manifest: str, evidence_sha256: str) -> str:
	driver, stem = runtime_summary.RUNS[name]
	return (f"tools/run_pinmame_harness.py with pinmame64.dll SHA-256 {LIBRARY_SHA256} (built from {PINMAME_REVISION[:12]}), driver {driver}, ROM archive SHA-256 {ROM_ARCHIVES[driver]}; "
		f"scenario tools/harness-scenarios/stern/{stem}.json (SHA-256 {scenario_sha256}), fresh state directory. Run directory manifest SHA-256 {manifest}; compact derived evidence in "
		f"{RUNTIME_EVIDENCE_PATH.as_posix()} (SHA-256 {evidence_sha256}).")


def build_sources(root: Path, runtime: dict[str, Any]) -> list[dict[str, Any]]:
	raw = {run["name"]: run for run in runtime["runtime"]["raw_runs"]}
	evidence_sha256 = runtime_evidence_sha256(root)
	manifest = runtime["source"]["sha256"]
	manuals = f"external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb/"
	sources = [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED,
			"locator": "src/wpc/stgames.c CORE_GAMEDEFNV(meteor) and CORE_GAMEDEFNV(meteora), the two roots, and the thirteen CORE_CLONEDEFNV entries meteorbf, meteora2, meteorfp, meteorns, "
				"meteore, meteorf, meteorg, meteorb, meteorc, meteord, meteore7, meteorf7 and meteorg7 that name meteor as parent",
			"license": PINMAME_CATALOG_LICENSE, "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "acquired_at": PINMAME_COMMITTED,
			"locator": "src/wpc/stgames.c INITGAME(meteor, GEN_STMPU200, dispst6, FLIP_SW(FLIP_L), 0, SNDBRD_ST300, 0), the identical game data of the other six-digit drivers and the dispst7 "
				"data of meteorb, meteorc, meteord, meteore7, meteorf7 and meteorg7, the drivers' source comments, input_ports_st and the dispst6/dispst7 layouts; src/wpc/by35.c by35_lampStrobe "
				"and pia1b_w (solenoid decoder low nibble and the continuous high nibble PB4-PB7); src/wpc/by35.h BY35_COMPORTS (option switches S1-S32, default OFF except S20 and S21, which default ON) and the diagnostic inputs -7 to "
				"-5; src/wpc/by35.c's switch update, which drives the 6800's NMI line from -6 (BY35_SWCPUDIAG) and passes -5 (BY35_SWSOUNDDIAG) to sndbrd_0_diag; src/wpc/stsnd.c "
				"st300_switch_w, which stores -5 as voiceSw, and st300_ctrl_w, which sends a control write to the S14001A speech path while it is set; src/wpc/core.h sLRFlip/sLLFlip "
				"power and hold addresses 45-48",
			"license": PINMAME_CORE_LICENSE, "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/stern-mpu200.json", "revision": "repository", "acquired_at": CONTROLLER_COMMITTED,
			"locator": "Stern MPU-200 controller profile: matrix 1-40, diagnostics -7 to -5, flipper-button positions 81-84, option switches 1-32, decoder solenoids 1-15, continuous 17-20 and synthetic "
				"flipper outputs 45-48, sixty discrete SCR lamps 1-63, physical direct inputs 1-6 and uncontrolled GI identity 1",
			"license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": f"https://www.ipdb.org/files/1580/{MANUAL_PDF}", "original_filename": MANUAL_PDF, "sha256": MANUAL_SHA256,
			"acquired_at": "2026-11-20T08:28:23Z",
			"locator": f"Stern Meteor game manual with its schematic sheets (IPDB 1580 `Manual`), 40 pages, 2,965,886 bytes, 300 dpi one-bit scans without a text layer, retained at {manuals}. "
				"Retrieved through the Internet Archive's Wayback Machine copy of the IPDB file (https://web.archive.org/web/20250706054609id_/https://www.ipdb.org/files/1580/Stern_1979_Meteor_Manual.pdf). "
				"Pages 2-6 installation, Figure 1, operation, self test, bookkeeping and front-door adjustments; 8-9 feature operation; 10-15 option switches; 16 playfield parts; 21 parts list; "
				"24-25 Solenoid Driver schematic 12B-432-S113 for METEOR; 28-29 Lamp Driver schematic 12B-431S-113 with its connector blocks and a copy of the lamp list; 32-33 cabinet and front door "
				"wiring; 34-35 Transformer schematic 12B-16B-6; 36-37 PLAYFIELD switch matrix, coil wiring and lamp list.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION", "excerpts": excerpts_for(MANUAL_SOURCE, root)},
		{"id": SELF_TEST_CARD_SOURCE, "kind": "manual", "uri": f"https://www.ipdb.org/files/1580/{SELF_TEST_CARD_PDF}", "original_filename": SELF_TEST_CARD_PDF, "sha256": SELF_TEST_CARD_SHA256,
			"acquired_at": "2026-11-20T08:28:35Z",
			"locator": f"Stern `METEOR SELF TEST DISPLAY NUMBERS` card (IPDB 1580 `Self Test Display Numbers`), one page, 722,006 bytes, a photocopy of a folded card, retained at {manuals}. "
				"Retrieved through the Internet Archive's Wayback Machine copy of the IPDB file "
				"(https://web.archive.org/web/20230314015335id_/https://www.ipdb.org/files/1580/Stern_1979_Meteor_Self_Test_Display_Numbers.pdf). Self test procedure, the solenoid list 01-16 and 19, "
				"the switch list 1-40 and the coin door switch drawings.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION",
			"excerpts": excerpts_for(SELF_TEST_CARD_SOURCE, root)},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1580", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-11-20T08:28:12Z",
			"locator": "IPDB machine 1580: Meteor, Stern Electronics, September 1979, model number 113, MPU Stern M-200, 7,939 units; notable features `Flippers (3), Pop bumper (1), Passive bumpers "
				"(2), Slingshots (2), Star rollovers (3), 3-bank drop targets (3), 6-bank memory drop targets (1), Spinning target (1), Standup target (1)` and `Only the 6-bank of drop targets has "
				"memory`; design Steve Kirk, art Leslie Kaip and Jorge Obregon, software Alan McNeil; first game with the SB-300 sound board. Read from the Wayback Machine's capture "
				f"(https://web.archive.org/web/20250108044417id_/https://www.ipdb.org/machine.cgi?id=1580), retained as {manuals}machine-1580.html; its title and machine number match, and the "
				"retained manual and self-test card are the files it links. Its notes list two schematic errata: a Memory Clear switch omitted from the switch-matrix page, and the 2X lamp on J2-15, "
				"not J3-15.",
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database", "excerpts": excerpts_for(IPDB_SOURCE, root)},
		{"id": SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"{CORPUS_REPOSITORY}/blob/{CORPUS_REVISION}/{quote(SCRIPT_PATH, safe='/')}", "revision": CORPUS_REVISION, "sha256": SCRIPT_SHA256,
			"acquired_at": CORPUS_COMMITTED,
			"locator": f"{SCRIPT_PATH} in the pinned known-working script corpus (114,961 bytes, LF; the Git blob is the file), cGameName = \"meteorb\": SolCallback 3, 7 and 9 raise the top left "
				"(19-21), lower left (22-24) and right (9-11) banks, 4, 5, 8, 11, 12 and 14 knock down M, first E, T, second E, O and R (DTDrop 32 to 27), 6 knocker, 13 the METEOR bank, 15 the outhole "
				"(bsTrough.Initsw 0,33,0,0,0,0,0,0), 16 vpmNudge.SolGameOn; Controller.Switch handlers 34-40, PulseSw 4, 5 and 12-16, and the drop targets 9-11, 19-24 and 27-32 through its DTArray. "
				"It differs from the retained table's script only in whitespace.",
			"license": "NOASSERTION", "attribution": "Meteor VPX table authors (bord; VR by Uncle_Paulie) and repository contributors", "known_working": True},
		{"id": STANDALONE_SOURCE, "kind": "vpx_script", "uri": f"{STANDALONE_REPOSITORY}/blob/{STANDALONE_REVISION}/{quote(STANDALONE_PATH, safe='/')}", "revision": STANDALONE_REVISION,
			"sha256": STANDALONE_SHA256, "acquired_at": STANDALONE_COMMITTED,
			"locator": f"vpx-standalone-scripts: {STANDALONE_PATH} (116,383 bytes), the second pinned known-working corpus; its solenoid, switch and lamp bindings are the corpus script's. Checkout "
				f"SHA256 is CRLF materialization; LF-normalized text matches Git blob SHA256 {STANDALONE_BLOB_SHA256}.",
			"license": "NOASSERTION", "attribution": "Meteor VPX table authors (bord; VR by Uncle_Paulie) and repository contributors", "known_working": True},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{(TABLE_RELATIVE / TABLE_FILENAME).as_posix()}", "original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256,
			"revision": "bord 1.0 (December 2020)", "acquired_at": "2026-11-20T08:39:34Z",
			"locator": f"Meteor by bord with a VR room by Uncle_Paulie, table version 1.0, December 2020 (its info names it `Meteor (Stern 1978)`), {TABLE_BYTES:,} bytes, from the archive "
				f"`{TABLE_ARCHIVE_FILENAME}` (SHA-256 {TABLE_ARCHIVE_SHA256}) that the operator downloaded from VPUniverse for this curation. Exact playfield bounds left 0, top 0, right "
				f"{data.TABLE_WIDTH}, bottom {data.TABLE_HEIGHT}; normalized coordinates are x/{data.TABLE_WIDTH} and y/{data.TABLE_HEIGHT}. The geometry source for every located placement. "
				"Its 302 lights are all bulb-mode and none shows a bulb mesh; the 17 connected pieces of its baked `layer1bulbs` mesh are the general-illumination bulbs.",
			"license": "NOASSERTION", "attribution": "bord, VR room by Uncle_Paulie; redistribution rights not granted", "rights": "NOASSERTION"},
		{"id": TABLE_SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{(EXTRACTION_RELATIVE / 'script.vbs').as_posix()}", "original_filename": "script.vbs",
			"sha256": TABLE_SCRIPT_SHA256, "acquired_at": "2026-11-20T08:39:39Z",
			"locator": "Embedded script of the retained table, 114,760 bytes (CRLF), cGameName = \"meteorb\"; the corpus script in CRLF with whitespace differences, so its bindings are the corpus "
				"script's, including the defect stated on the stand-up target: its handler `Tsw4_Hit` also pulses switch 12. Its `SolCallback(16) = vpmNudge.SolGameOn` hangs on an address "
				"the MPU-200 never drives, a dead binding the loaded VPinMAME libraries make redundant: they hand output 19 to vpmFlips, which on a tilt disables the flippers and the thumper "
				"bumper and slingshots (stated on the flipper enable relay). It binds each switch and coil placement's object.",
			"license": "NOASSERTION", "attribution": "bord", "known_working": True},
		{"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{(VPM_LIBRARY_RELATIVE / 'stern.vbs').as_posix()}", "original_filename": "stern.vbs",
			"sha256": VPM_LIBRARY_FILES["stern.vbs"], "acquired_at": "2026-11-20T12:28:02Z",
			"locator": f"stern.vbs ('Last Updated in VBS v3.61') and core.vbs (VPinMAMEDriverVer 3.61, SHA-256 {VPM_LIBRARY_FILES['core.vbs']}) beside it, the VPinMAME script libraries "
				"the retained table and both corpus scripts load (`LoadVPM \"01000100\", \"Stern.VBS\", 1.2`), copied byte for byte from the retained installed VPinMAME Scripts folder: "
				"stern.vbs `Const GameOnSolenoid = 19`; with `UseSolenoids=2` core.vbs makes that output vpmFlips' solenoid and hands each change of it to `vpmFlips.TiltSol`, whose "
				"EnableFlippers enables or disables the flippers and, with `TiltObjects` at its constructor default of 1, calls cvpmNudge.SolGameOn with the same state, which raises the "
				"thresholds of `vpmNudge.TiltObj` to 100 when the game is off and restores them when it is on.",
			"license": "NOASSERTION", "attribution": "VPinMAME contributors", "excerpts": excerpts_for(VPM_LIBRARY_SOURCE, root)},
		{"id": EXTRACTION_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}", "sha256": EXTRACTION_MANIFEST_SHA256,
			"acquired_at": "2026-11-20T08:39:39Z",
			"locator": f"Retained vpxtool {VPXTOOL_VERSION} extraction of the table; manifest external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE.as_posix()} (format pinmame-vpx-extraction-manifest "
				f"v1: every file as sorted relative POSIX path, size and SHA-256, canonical JSON), SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes. "
				"tools/curate_meteor.py --verify-extraction recomputes it. Primitive mesh centres are checked against the vpxtool "
				f"{VPXTOOL_VERSION} `export obj --units vpu` world-space export external:pinmame-vpx-sources/{WORLD_OBJ_RELATIVE.as_posix()} (SHA-256 {WORLD_OBJ_SHA256}, "
				f"{WORLD_OBJ_BYTES} bytes). That export leaves out the invisible dead-bumper primitives `bumper2` and `bumper3`, so their centres come from the same export of a "
				f"visibility-only derivative, external:pinmame-vpx-sources/{(BUMPERS_VISIBLE_RELATIVE / BUMPERS_VISIBLE_VPX).as_posix()} (SHA-256 {BUMPERS_VISIBLE_VPX_SHA256}, "
				f"{BUMPERS_VISIBLE_VPX_BYTES} bytes): this extraction with `is_visible` set to true in those two primitives and nothing else changed, assembled with vpxtool "
				f"{VPXTOOL_VERSION}; its re-extraction (manifest SHA-256 {BUMPERS_VISIBLE_MANIFEST_SHA256}) differs from this one only in those two files, and its export "
				f"external:pinmame-vpx-sources/{BUMPERS_VISIBLE_OBJ_RELATIVE.as_posix()} (SHA-256 {BUMPERS_VISIBLE_OBJ_SHA256}, {BUMPERS_VISIBLE_OBJ_BYTES} bytes) adds only "
				"those two objects, every other object's vertices unchanged.",
			"license": "NOASSERTION", "attribution": "bord; redistribution rights not granted"},
	]
	for name in RUN_NAMES:
		sources.append({
			"id": RUN_SOURCES[name],
			"kind": "service_diagnostic" if name in runtime_summary.SERVICE_RUNS else "runtime_scenario",
			"uri": f"external:pinmame-review-artifacts/meteor-1979/harness/{name}/run.json",
			"sha256": raw[name]["sha256"],
			"acquired_at": RUN_AT[name],
			"locator": run_locator(name, raw[name]["scenario_sha256"], manifest, evidence_sha256),
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		})
	return sources


# --- Definition ---------------------------------------------------------------------------------------------------------

MISSING = ["spatial_placement", "unresolved_conflicts"]


def build_drivers() -> list[dict[str, Any]]:
	drivers = []
	for driver_id in sorted(data.DRIVERS):
		description, year, manufacturer, clone_of, notes, seven_digit = data.DRIVERS[driver_id]
		item: dict[str, Any] = {"description": description, "flags": 0, "id": driver_id, "manufacturer": manufacturer,
			"physical_compatibility": "compatible" if seven_digit else "identical", "variant_notes": notes, "year": year}
		if clone_of:
			item["clone_of"] = clone_of
		if seven_digit:
			item["display_overrides"] = [{"provenance": provenance(CORE_SOURCE), "segment_start": start, "target": target, "width": 7}
				for target, start in data.SEVEN_DIGIT_STARTS.items()]
		drivers.append(item)
	return drivers


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	used = {address for address, spec in data.SWITCHES.items() if not spec.get("unused")}
	if set(data.SWITCHES) != set(range(1, 41)) or used | data.UNUSED_SWITCHES != set(range(1, 41)) or set(data.DIPS) != set(range(1, 33)):
		raise RuntimeError("Meteor switch or option-switch inventory is incomplete")
	if sorted(data.PHYSICAL_TO_PUBLIC) != list(range(1, 20)) or set(data.SOLENOIDS) != set(data.PHYSICAL_TO_PUBLIC.values()) or set(data.SDU_LOADS) != set(range(1, 20)):
		raise RuntimeError("Meteor solenoid inventory is incomplete")
	if {q for qs in data.DECODER.values() for q in qs} != set(range(1, 61)) or any(len(qs) != 15 for qs in data.DECODER.values()):
		raise RuntimeError("Meteor decoder map does not cover SCRs 1-60 exactly once")
	if sorted(KNOCK_DOWN) != list(range(27, 33)) or {address for _, address in KNOCK_DOWN.items()} != set(runtime_summary.KNOCK_DOWN_COILS):
		raise RuntimeError("Meteor knock-down coils disagree with the runtime summary")
	if any(data.METEOR_LETTERS[switch][1] != letter or KNOCK_DOWN[switch] != coil for letter, (switch, coil, _) in runtime_summary.METEOR_BANK.items()):
		raise RuntimeError("Meteor bank letters disagree between the data module and the runtime summary")
	if set(data.LAMP_NAMES) != set(data.LAMP_TO_Q):
		raise RuntimeError("Meteor lamp names do not cover the sixty outputs")
	if excerpt_connector_blocks(root) != data.CONNECTOR_BLOCKS:
		raise RuntimeError("Meteor connector-block readings disagree with the lamp-driver excerpt")
	runtime = runtime_document(root)
	observations = runtime["runtime"]["observations"]
	if {int(key): value for key, value in observations["physical_service_solenoid_to_public"].items()} != data.PHYSICAL_TO_PUBLIC:
		raise RuntimeError("Meteor solenoid translation disagrees with the retained solenoid test")
	if [run["name"] for run in runtime["runtime"]["raw_runs"]] != list(RUN_NAMES):
		raise RuntimeError("Meteor runtime evidence does not carry the curator's runs")
	if set(observations["lamp_addresses_seen"]) != set(data.LAMP_TO_Q) or observations["lamp_decoder_holes_not_seen"] != [16, 32, 48, 64]:
		raise RuntimeError("Meteor burn-in lamps are not the sixty SCR outputs")
	return build_unchecked_definition(root, runtime)


def build_unchecked_definition(root: Path, runtime: dict[str, Any]) -> dict[str, Any]:
	observations = runtime["runtime"]["observations"]
	return {
		"conflicts": build_conflicts(),
		"controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.stern-mpu200"},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"causal_exercise": "validated",
				"diagnostic_enumeration": "validated",
				"display_inventory": "validated",
				"emulator_normalization": "validated",
				"mechanisms": "validated",
				"physical_wiring": "validated",
				"recreation_knowledge": "validated",
				"runtime_observation": "validated",
				"semantic_naming": "conflicted",
				"spatial_placement": "observed",
				"variant_coverage": "validated",
			},
			"missing": list(MISSING),
			"status": "partial",
		},
		"displays": [
			{"controller_index": index, "id": identifier, "kind": "segment", "label": label, "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, GAMEPLAY_SOURCE), "segment_start": start,
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "width": width}
			for identifier, label, index, start, width in data.DISPLAYS
		],
		"drivers": build_drivers(),
		"format": "pinmame-machine-definition",
		"inputs": build_inputs(observations),
		"knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "complete"},
		"machine": {"id": MACHINE_ID, "ipdb_id": 1580, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "113", "name": "Meteor", "opdb_id": "G5b38-MDqkx", "year": 1979,
			"playfield": {"height": data.TABLE_HEIGHT, "provenance": provenance(TABLE_SOURCE), "units": "vpx", "width": data.TABLE_WIDTH}},
		"mechanisms": build_mechanisms(),
		"outputs": build_outputs(observations),
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(root, runtime),
	}


# --- Spatial report -----------------------------------------------------------------------------------------------------


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_records: list[dict[str, Any]] = []
	not_applicable_records: dict[str, list[str]] = {}
	unplaced: list[dict[str, Any]] = []
	statuses: dict[str, int] = {}
	for collection in ("inputs", "outputs", "displays"):
		for item in definition[collection]:
			spatial = item.get("spatial")
			binding = item.get("binding", {})
			record = {"id": item["id"], "group": binding.get("group", "display"), "address": binding.get("device", item.get("controller_index"))}
			if spatial is None:
				unplaced.append(record)
			elif spatial["status"] == "not_applicable":
				not_applicable_records.setdefault(spatial["reason"], []).append(item["id"])
			else:
				located_records.append({**record, "placements": len(spatial["placements"])})
				for placement in spatial["placements"]:
					statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
	projections = [{"address": address, "group": "pinmame.input.switch", "reason": data.SWITCH_OBJECTS[address][1]} for address in PROJECTED_SWITCHES]
	projections += [{"address": address, "group": "pinmame.output.solenoid", "reason": reason} for address, (_, reason) in sorted(data.SOLENOID_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "physical.input.direct", "reason": reason} for address, reason in (
		(1, "Placed on the left flipper pivot: the end-of-stroke contact is mounted on its flipper assembly."),
		(2, "Placed on the right flipper pivots: each end-of-stroke contact is mounted on its flipper assembly."))]
	unplaced_lamps = [item["address"] for item in unplaced if item["group"] == "pinmame.output.lamp"]
	return {
		"blockers": [
			f"No playfield lamp is placed ({len(unplaced_lamps)} of the 60 lamp outputs; the other four are backbox lamps): the retained table, the only Meteor table available, draws every insert "
			"with lights that show no bulb mesh, and the manual's playfield parts drawing draws the insert circles without lamp numbers, so no source marks a socket (docs/SPATIAL.md, Picking the bulb).",
			"The outhole switch 33 and the outhole kicker (public 15) are not placed: both known-working scripts and the table model the outhole as a one-ball virtual stack with no object at "
			"the switch, and the playfield parts drawing does not show the outhole.",
			"The upper right flipper's series `E.O.S.` contact (physical direct input 6) is not placed: the playfield coil sheet draws it in the circuit only and does not say which flipper "
			"assembly carries it.",
			"Every switch, coil and general-illumination placement is `observed` from the one table; no factory-drawing callout check was made, and the manual has no switch or lamp location drawing.",
			"The placements of the three-banks' middle and lower targets (switches 10, 11, 20, 21, 23 and 24) are `conflicted`: they follow the playfield sheet's matrix labels, which the "
			"known-working scripts' bindings contradict (the record's conflict).",
		],
		"coordinate_convention": {"source_bounds": {"bottom": data.TABLE_HEIGHT, "left": 0.0, "right": data.TABLE_WIDTH, "top": 0.0}, "space": "playfield",
			"x": f"x/{data.TABLE_WIDTH}; 0=left, 1=right", "y": f"y/{data.TABLE_HEIGHT}; 0=rear/backglass, 1=apron/player"},
		"excluded_object_classes": [
			"L<n>, L<n>a and L<n>A lights: insert lights the scripts bind to lamp numbers; none of the table's 302 lights shows a bulb mesh, so none marks a socket",
			"Light<n> lights: the general-illumination glows, placed through the `layer1bulbs` mesh piece each sits on, not on their own",
			"LED<n> lights, the LED/led display-segment flashers, the FlBGL backglass flashers, the L13, L45, L61 and L63 and EMReel reels, and the VR room walls and ramps: backbox, desktop and "
			"render helpers, not playfield devices",
			"<target>y walls (sw9y and the like) and the psw<n> primitives: the drop targets' animation helpers; each target is placed on its own sw<n> wall",
			"DRAIN and BallRelease kickers: the one-ball virtual stack's entry and its shooter-lane exit, not the physical outhole",
			"Gate003 and Gate7 and the TriggerLF, TriggerRF and ballatplunger triggers: passive or helper objects with no controller binding",
		],
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_algorithm": "format pinmame-vpx-extraction-manifest v1: every file as sorted relative POSIX path, size and SHA-256, canonical JSON (tools/curate_meteor.py)",
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE.as_posix()}", "source_ref": EXTRACTION_SOURCE, "total_bytes": EXTRACTION_TOTAL_BYTES,
			"table_sha256": TABLE_SHA256, "script_sha256": TABLE_SCRIPT_SHA256, "vpxtool_version": VPXTOOL_VERSION},
		"format": "pinmame-spatial-blockers",
		"located_records": sorted(located_records, key=lambda item: item["id"]),
		"machine_id": MACHINE_ID,
		"not_applicable_records": {reason: sorted(ids) for reason, ids in sorted(not_applicable_records.items())},
		"placement_statuses": dict(sorted(statuses.items())),
		"projections": projections,
		"readiness": {"missing": definition["coverage"]["missing"], "status": definition["coverage"]["status"], "unresolved_conflicts": len(unresolved_conflicts(definition))},
		"unplaced_records": sorted(unplaced, key=lambda item: item["id"]),
		"version": 1,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Meteor (Stern, 1979) spatial review",
		"",
		"Status: incomplete. No playfield lamp is placed, every placement is `observed` or `conflicted`, so the machine record stays `partial` at `machines/partial/stern/meteor-1979.json`.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}` (bord, 1.0, December 2020) at SHA-256 `{TABLE_SHA256}`; its embedded script (SHA-256 `{TABLE_SCRIPT_SHA256}`) is the pinned "
		f"corpus script with whitespace differences. Exact playfield bounds are left 0, top 0, right {data.TABLE_WIDTH}, bottom {data.TABLE_HEIGHT}, and every canonical coordinate is "
		f"x/{data.TABLE_WIDTH} and y/{data.TABLE_HEIGHT} rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.",
		"",
		"## Evidence decisions",
		"",
		"- The script's bindings choose each switch's and coil's object. A switch sits on its trigger, target wall, bumper, stand-up target or spinner; a coil sits on the object it moves, or at "
		"the mean of the targets a reset coil raises.",
		f"- The world-space mesh source is the vpxtool {VPXTOOL_VERSION} `export obj --units vpu` export of the retained table, `{WORLD_OBJ_RELATIVE.as_posix()}` under the VPX sources "
		f"root (SHA-256 `{WORLD_OBJ_SHA256}`, {WORLD_OBJ_BYTES} bytes, outside Git), whose x and y are playfield VPX units.",
		"- The two passive scoring bumpers are baked-mesh primitives at the origin, invisible collidables that the export leaves out. Each is placed on the world-space bounding-box "
		f"centre of its mesh in the same export of a visibility-only derivative, `{(BUMPERS_VISIBLE_RELATIVE / BUMPERS_VISIBLE_VPX).as_posix()}` (SHA-256 "
		f"`{BUMPERS_VISIBLE_VPX_SHA256}`, outside Git): the retained extraction with `is_visible` set to true in `Primitive.bumper2.json` and `Primitive.bumper3.json` and nothing else "
		"changed, assembled with vpxtool. Its re-extraction differs from the retained extraction only in those two files, and its export, "
		f"`{BUMPERS_VISIBLE_OBJ_RELATIVE.as_posix()}` (SHA-256 `{BUMPERS_VISIBLE_OBJ_SHA256}`, {BUMPERS_VISIBLE_OBJ_BYTES} bytes), adds only those two objects to the table's, "
		"every other object's vertices unchanged. The exported centres equal the primitive's position plus each local vertex times its size (185.274, no rotation) within 0.0001 VPX "
		"units, and fall within 1.3 VPX units of each bumper's own light.",
		"- Lamps are not placed. The table's 302 lights are all bulb-mode, but none shows a bulb mesh, and docs/SPATIAL.md requires a real bulb for a socket.",
		"- General illumination is placed on the export's world-space bounding-box centres of the 17 connected pieces of the baked `layer1bulbs` mesh, each with a `Light<n>` "
		"general-illumination light within 3.6 VPX units of its centre. The playfield sheet draws one `GEN. ILLUM` string (feed A2J1-8, return A2J1-1) as a single lamp symbol, so no "
		"machine source gives the sockets' positions or count, and the placements stay `observed`.",
		"- The playfield sheet labels each three-bank's matrix cells top, lower and middle; the table binds them top, middle and lower. The placements follow the sheet and are `conflicted` "
		"until the record's conflict is settled.",
		"",
		"## Explicit projections",
		"",
	]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += ["", "## Counts", ""]
	lines.append(f"- Placements: {sum(item['placements'] for item in report['located_records'])} ({', '.join(f'{count} {name}' for name, count in report['placement_statuses'].items())}) on {len(report['located_records'])} records")
	for reason, ids in report["not_applicable_records"].items():
		lines.append(f"- Records with a controlled `{reason}` record: {len(ids)}")
	lines.append(f"- Records with no spatial key: {len(report['unplaced_records'])}")
	lines += ["", "## Excluded table objects", ""]
	lines += [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Promotion decision", "",
		"Promotion to `author_ready` is refused: no playfield lamp has a socket, the outhole has no physical object, every placement rests on one table with no factory-drawing check, and the "
		"three-banks' middle and lower targets carry an unresolved conflict about their switch numbers. It stays `partial` with "
		f"`coverage.missing = {json.dumps(report['readiness']['missing'])}`.", "",
		"## Retained evidence", "",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.", ""]
	return "\n".join(lines)


# --- Knowledge note -----------------------------------------------------------------------------------------------------

KNOWLEDGE = """# Meteor (Stern, 1979)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; no playfield lamp is placed, and which switch is each three-bank's middle target is unresolved**

## Identity and evidence precedence

This is the one physical Stern Meteor (IPDB 1580, September 1979, model 113, Stern M-200 MPU, 7,939 units; design Steve Kirk, art Leslie Kaip and Jorge Obregon, software Alan McNeil). Every PinMAME
Meteor driver runs on this machine, so one record carries all fifteen:

- `meteor` is the production ROM set and `meteora` Stern's factory fix of its U1 (`cpu_u1a.716`), which PinMAME declares as a second root rather than as a clone. `meteorbf` is an earlier,
  different bonus-count fix, `meteorfp` the free-play set, `meteora2` a community build with a sound-register fix and `meteorns` a community patch that removes the background sound.
- `meteore`, `meteorf` and `meteorg` are Idleman's free-play rules modifications (revisions 64-66, 2019-2021).
- `meteorb` (2003) is Oliver's seven-digit conversion, `meteorc` its free-play build and `meteord` (2005) a /10 scoring build on the same layout; `meteore7`, `meteorf7` and `meteorg7` are seven-digit
  builds of Idleman's modification (revisions 74-76). These six use PinMAME's `dispst7` layout (player displays at segment starts 1, 9, 17 and 25, width 7), recorded as display overrides; the
  conversion needs seven-digit player displays and changes nothing else.

All fifteen share the rest of the game data (`GEN_STMPU200`, `FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound). The authorized ROM library holds `meteor`, `meteora`, `meteorb`, `meteorbf`,
`meteorc`, `meteord` and `meteorfp`; each of the six besides `meteor` was run once. Before the drain each fired the same set of solenoids as `meteor` for the same steps (the thumper,
both slingshots, the stand-up target, the right three-bank and both flipper buttons; firing order, timing and lamps were not compared), except that in `meteorc` and `meteord`
(knock-down 8) and `meteorfp` (knock-down 14) the stand-up target spotted a different METEOR target from the one `meteor` spotted (knock-down 12). Across the drain and the next
serve taken together each fired the outhole kick (15) and the bank resets (3, 7, 9, 13), though not in the same windows: `meteor`'s run fired them before the served ball left the
outhole and only target restores after it, while each variant fired them again after it. No variant fired a knock-down coil there: no METEOR target switch closed in those runs,
while `meteor`'s run restored the four it had down.

Evidence order is the runbook's. The two pinned corpus scripts (whose `cGameName` is `meteorb`) give runtime bindings, this game's own 40-page manual and its self-test card give construction and
wiring, pinned PinMAME gives the controller topology, and eleven retained harness runs (burn-in, solenoid test, switch test, a coin and bookkeeping run, a scripted game and one run of each other
driver held) pair the printed numbers with public addresses and show the ROM's responses. The manual is a 300 dpi one-bit scan whose last pages are the schematic sheets lettered for METEOR.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty (retained run), so the self-test
card's switch numbers are the public addresses. Positions 17, 18, 25 and 26 are not used (card `Open`, playfield sheet `N/U`). The cabinet switches 1-3 (coin chutes), 6 (credit), 7 (tilts) and 8 (slam)
are strobed on R-Y (A4J3-2) and return on MPU connector A4J3; the playfield sheet repeats 6, 7 and 8 and draws 1-3 as unlabelled contacts. Every matrix contact is normally open. The coin chutes, by
the bookkeeping counts of the retained coin run: public 1 is the hinge-side chute (credit table switches 28-30), 2 the center chute (switches 1-5) and 3 the right chute (switches 9-13); the cabinet
sheet's `CHUTE #3/#2/#1` labels run the other way. Service inputs are -7 (Self Test, inside the coin door), -6 and -5. Public -6 is S33, the pushbutton on the MPU assembly: the MPU schematic
wires it to the 6800's NMI input, the line PinMAME drives from -6; the manual names it only for zeroing a high score level while adjusting it. Public -5 is a virtual input: PinMAME passes it to the ST300 sound
board's diagnostic callback, which holds it as the voice-select state, and no fitted contact is established for it, so a recreation leaves it open. IPDB's schematic errata report a remote memory-clear switch wired to A4J3-5, which the interboard wiring diagram prints `N.U`, so no
remote contact is recorded. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' winding-shunt end-of-stroke contacts (physical direct inputs 1
and 2) and the upper right flipper's series `E.O.S.` contact (6) have only profile-local identities.

**Solenoids.** The self-test card's solenoid numbers are the SDU driver transistor numbers, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires,
pairing them as `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over four identical cycles. In public terms: 1 left
slingshot, 2 thumper bumper, 3 top left three-bank reset, 4 METEOR M knock-down, 5 first E knock-down, 6 knocker, 7 lower left three-bank reset, 8 T knock-down, 9 right three-bank reset, 10 right
slingshot, 11 second E knock-down, 12 O knock-down, 13 METEOR bank reset, 14 R knock-down, 15 outhole kicker, 18 coin lockout, 19 flipper enable relay. Public 16 is the decoder's unaddressable slot.
Public 17 (Q17) and 20 (Q18) are continuous drivers wired only to pins marked `N/U`, with no load in the card or the parts list: in the retained runs the ROM drives them only in the power-up initialisation
pulse it gives all four continuous lines (at power-up and after a slam) and in its own tests, so they are unused.

**Continuous outputs.** Public 18 (Q19) and 19 (Q15) are held. The coin lockout is energized from about 2.5 s after the power-up pulse and drops when the credits reach the maximum (5 at the default
option switches, in the retained coin run). The flipper relay is held on while a game is played and drops on a tilt and at game over; outside play the retained runs
show it raised only in the power-up initialisation pulse the ROM gives all four continuous lines (at power-up and after a slam) and in the ROM's burn-in and solenoid
tests, and off in steady attract mode.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this
game's lettered copy of sheet 12B-431S-113 was read for all sixty lines. The game's lamp assignment is the lamp list on the playfield sheet (a copy on the lamp driver sheet adds a handwritten Tilt row),
which names a load, wire, jack and pin for every output; its pins were checked against the lamp driver sheet's connector blocks, and every disagreement is stated on the lamp. The ROM proves the
METEOR drop lamps (M 58, first E 42, T 26, second E 10, O 57, R 41), the spot lamps 5 (stand-up target), 25 (upper rollover) and 9 (lower rollover), which went out as their switch spotted a
target, and the backbox TILT lamp (61); the lamp list and the scripts pair the same lamps with the middle rollover (5), the left return lane (25) and the right return lane (9), which the run exercised
with those lamps already out; GAME OVER (45), MATCH (63) and HIGH SCORE TO DATE (13) are the other backbox lamps. The bank WOW lamps 30, 46 and 62 and the stand-up WOW 14 changed state
only in the service runs; they are printed loads and stay used.

**General illumination** is uncontrolled: the playfield string from A2J1-8 (printed 6 VAC there, off the transformer's 7.3 VAC winding), the cabinet bus and the backbox buses, with no relay or driver in
any line.

## Ball lifecycle

The single ball rests on the outhole switch (33) under the apron in front of the outhole kicker (15). When a game starts the ROM raises the flipper relay (19) and fires the outhole kicker followed
by the four bank resets in sequence (15, then 3, 7, 9 and 13, about 0.6 s from the kick to the last reset) and repeats that sequence about every 1.7 s while 33 stays closed (retained runs); a real
ball leaves 33 on the first kick and rolls into the shooter lane. After a drain while play continues the bonus times the
multiplier is added (a tilted ball forfeits it, manual), the ball or player advances, the ROM restores the METEOR targets that player had made with their knock-down coils (the bank's memory, manual) and serves again; an extra ball is
played without advancing. A tilt drops the flipper relay and lights TILT (61); in the retained run a right slingshot hit while tilted fired nothing, and on the next ball the left
slingshot and the left flipper button both worked. A slam ends the
game, and the ROM repeats its power-up initialisation. After the last ball's drain the retained trace records no outhole kicker pulse in the 30 s the host then holds 33 closed before
crediting the next game, so the ball stays in the outhole; the ROM drops the flipper relay and lights GAME OVER (45) and MATCH (63). In the
retained run the final score 539,740 matched the match number 40, and the ROM fired the knocker (6) once as the credits went from 02 to 03; the match is played only with option switch 21 ON
(PinMAME's default).

## Mechanisms

- **METEOR bank**: six drop targets (32 M, 31 E, 30 T, 29 E, 28 O, 27 R from left to right) on one reset coil (13) with a knock-down coil each (M 4, first E 5, T 8, second E 11, O 12, R 14). The ROM
  spots targets with the knock-down coils and, after a drain that continues play, restores the targets the next ball's player had made (the bank's memory: the manual's rule, which IPDB
  notes is the only drop-target memory on the game). The retained single-player run restores T, second E, O and R after each of its first two drains (the second one tilted) and fires
  no restore after the last ball.
- **Three-banks**: right (9-11, reset 9), top left (19-21, reset 3) and lower left (22-24, reset 7), no knock-downs. Each controls one missile row: right bank the right row (rocket 3), top left the
  middle row (rocket 2), lower left the left row (rocket 1); each hit advances one lamp of its row.
- **Thumper bumper** (14 fires 2), **slingshots** (16 fires 1, 15 fires 10), two passive **scoring bumpers** (12, 13), the **spinner** (5), the center **stationary target** (4) and a passive ball gate.
- **Flippers**: three dual-winding coils on two buttons, gated by the flipper enable relay; the upper right flipper hangs off the right flipper's drive through a separate series contact labelled
  `E.O.S.`, drawn open, so it is energized only while that contact is closed. The sheet does not say which assembly carries it; PinMAME and the scripts move both right flippers together. PinMAME
  publishes 46 (right) and 48 (left) with 45 and 47 alongside.

## Rules summary

From the manual's feature pages: the METEOR end targets score 6,000 and the middle ones 2,000, and each down target adds 600 (end) or 200 (middle) to every spinner spin. Completing the bank advances the
bonus multiplier 1X-7X (carried over up to 6X; after 7X it resets to 3X for the next ball); from the 5th or 6th reset (option switches 23-24) a lamp steps across the bank for an extra ball. Lit star
rollovers (2,000 or 6,000), lit return lanes and the lit stationary target spot a METEOR target. Each three-bank hit advances its missile row and scores the value; three equal missile values light a
rotating WOW (extra ball), and a bank's special is awarded on its center target. The scoring bumpers score 500 or the missile value and advance missile rows 1 and 3 when lit; the outlanes score 3,000
plus 1,000 per missile lamp when lit; the thumper scores 1,000 (three-ball) or 100 (five-ball); the slingshots score 10 and move the lit features unless option switch 25 is ON.

## Option switches

The thirty-two MPU option switches (Figure 1 `DETAIL S1-S32 MPU ASS'Y.`) are assigned by the `METEOR SWITCH ASSIGNMENT` list on PDF page 10 and the charts on pages 11-15: S1-5 center chute, S9-13
right chute and S28-30 hinge-side chute credits, S6 high score award, S7 balls per game, S8 missile WOWs, S14/S31/S32 special award, S15-16 high game to date, S17-19 maximum credits, S20 credit display,
S21 match, S22 replays per ball, S23-24 METEOR bank WOW at 6X or 7X, S25 slingshot movement, S26 spot METEOR lamps per multiplier and S27 spot METEOR lanes. Pinned PinMAME boots with S20 and S21
ON and the rest OFF (by35.h BY35_COMPORTS), which gives the three-ball games, the 3/2 center-chute pricing, the 5-credit maximum, the credit display and the match of the retained runs. The page-10 list numbers the chutes `Coin Chute #1 Germany or #2 All Others` for 28-30 and
`No. 2 Germany or No. 1 All Others` for 1-5, while the credit chart calls 28-30 the chute `next to hinge` and 1-5 the center chute; the bookkeeping counts above settle which public input each counts.

## Displays and sound

Four six-digit player displays (indices 0-3, segment starts 2, 10, 18 and 26), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME
`dispst6`. The six seven-digit drivers move the player displays to starts 1, 9, 17 and 25, width 7. Sound is the Stern SB-300 sound module (parts list `Sound Module C-605`; PinMAME `SNDBRD_ST300`);
sound commands add no playfield devices.

## Disagreements between this game's own documents

- **Three-bank middle and lower targets (unresolved).** The playfield sheet prints each bank's cells top, lower, middle in matrix order (9, 10, 11; 19, 20, 21; 22, 23, 24); both known-working scripts
  bind the middle object to 10, 20 and 23. The special a bank awards on its center target depends on it. A harness run with a special award set by option switches 14, 31 and 32 would settle it, but
  `tools/run_pinmame_harness.py` cannot set option switches yet; an owner pressing each middle target in the switch test would also settle it.
- The SDU sheet and the playfield coil sheet swap the flipper return pins (J1-8 and J1-9) while agreeing on the colours; the thumper's `A3J2-4` on the coil sheet repeats the left slingshot's pin where
  its colour is the SDU's J2-9; the first E knock-down is Y-B on the SDU sheet and Y-W on the coil sheet; the right slingshot's colour is struck through on the SDU sheet. Wiring-detail readings only;
  the SDU sheet is followed except where its own entry is struck out.
- The lamp list and the lamp driver connector blocks disagree on several pins, and the list prints the lower left bank WOW twice and `2X` on another row's pin; each case is stated on its lamp.
- The playfield sheet draws credit (6) and coin chute 1 without a diode where the cabinet sheet draws one; the cabinet sheet's chute numbers run opposite to the credit table's.
- The playfield sheet prints the playfield G.I. string as 6 VAC; the transformer sheet's G.I. winding is 7.3 VAC.

## Recreation checklist

- Build the full inventory: 36 used matrix switches and four unused positions, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 (17 and 20
  unused) with the two flipper callbacks, the sixty SCR lamp addresses and the six displays (with the seven-digit overrides for the drivers that need them).
- Start with the ball on the outhole (33 closed), every drop target up and the flipper relay off in steady attract mode, after the power-up
  initialisation pulse, until a game starts.
- Make each knock-down coil put its METEOR target down so that its switch closes; the ROM spots targets and restores each player's made targets after a drain with them.
- Bind the right flipper callback to both right flippers.
- Treat the manual's feature pages and the ROM as the rules authority; the community ROMs change rules or scoring, not hardware.
- Placements: switches, coils and general illumination come from the retained table and are `observed` (the three-banks' middle and lower targets `conflicted`); lamps are unplaced until a table or
  drawing marks their sockets.

## What would complete the record

- **Spatial placement**: a Meteor table that models its insert bulbs (or a lamp-location drawing), a second independent table or a factory-drawing callout check for the switches and coils, and an
  outhole model with an object at 33.
- **Three-bank middle targets**: the harness probe or owner check described above.

## Retained table and its defects

The geometry comes from `Meteor (Stern 1979).vpx` by bord with a VR room by Uncle_Paulie (1.0, December 2020), downloaded for this curation. Its script is the pinned corpus script with whitespace
differences. Its defect, stated on the stand-up target: the target's handler also pulses switch 12 (the upper right scoring bumper) on every hit. With `UseSolenoids=2` the loaded VPinMAME
libraries (stern.vbs `GameOnSolenoid = 19`, core.vbs `vpmFlips.TiltSol` and `EnableFlippers`, `TiltObjects` left at 1) follow the flipper enable output 19, so on a tilt the table's flippers
go dead and its thumper bumper and slingshots stop kicking; the retained run exercised only the right slingshot while tilted, and the ROM fired nothing for it.
That makes the script's `SolCallback(16) = "vpmNudge.SolGameOn"` redundant; it hangs on an address the MPU-200 never drives and never fires. Its insert lights show no bulb mesh, so they place
no lamp.

## Sources

- `manual.stern.meteor.1979`: the 40-page IPDB manual with its schematic sheets, with transcribed excerpts of its operating text, option switches, parts pages, switch matrix, coil wiring, solenoid
  driver, lamp driver and lamp list, cabinet wiring and general illumination.
- `manual.stern.meteor.self-test-card`: the self-test card's procedure and solenoid and switch lists.
- `vpx-script.meteor-corpus` and `vpx-script.meteor-standalone`: the pinned known-working corpus scripts.
- `vpx-table.meteor-bord-1-0`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.meteor.*`: eleven isolated harness runs on the pinned `pinmame64.dll`, five of `meteor` (ROM archive SHA-256 `ee849e28a5edd2832012c433e6e71713f8c8773c874139ea24bc6d4bb9529438`) and one each of
  `meteora`, `meteorb`, `meteorbf`, `meteorc`, `meteord` and `meteorfp`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layouts.
"""


# --- Retained extraction manifest -------------------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Meteor retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required for the retained Meteor extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE
	if not manifest_path.is_file():
		raise RuntimeError(f"Meteor retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(source_root / EXTRACTION_RELATIVE)
	if canonical_bytes(actual) != canonical_bytes(expected) or manifest_path.read_bytes() != canonical_bytes(actual):
		raise RuntimeError(f"Meteor retained extraction manifest does not match all files under {source_root / EXTRACTION_RELATIVE}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Meteor retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	"""Write the canonical manifest beside the extraction; refuse to replace a manifest whose content differs."""
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE
	payload = canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE))
	if manifest_path.exists() and manifest_path.read_bytes() != payload:
		raise RuntimeError(f"Refusing to overwrite a differing Meteor extraction manifest: {manifest_path}")
	manifest_path.write_bytes(payload)
	return manifest_path


# --- Generation and checking ------------------------------------------------------------------------------------------


def products(root: Path = ROOT) -> dict[Path, bytes]:
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Meteor definition: " + "; ".join(errors[:20]))
	if unresolved_conflicts(definition) and "unresolved_conflicts" not in definition["coverage"]["missing"]:
		raise RuntimeError("Meteor holds unresolved conflicts but does not list them as missing")
	report = build_spatial_report(definition)
	return {
		DEFINITION_PATH: canonical_bytes(definition),
		SEED_PATH: canonical_bytes(definition),
		SPATIAL_REPORT_PATH: canonical_bytes(report),
		SPATIAL_REPORT_MARKDOWN_PATH: render_spatial_report(report).encode("utf-8"),
		KNOWLEDGE_PATH: KNOWLEDGE.encode("utf-8"),
	}


def generate(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Meteor artifact")
	for path, payload in products(root).items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("A Meteor author-ready definition is present although the record is partial")
	for path in RETIRED_PATHS:
		if (root / path).exists():
			raise RuntimeError(f"The retired Meteor residual artifact is still present: {path}")
	for path, payload in products(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Meteor deterministic artifact missing or drifted: {path}")
	print("Meteor definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, knowledge note and spatial report")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained VPX extraction against its pinned manifest identity (needs PINMAME_VPX_SOURCES_ROOT)")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained extraction's canonical manifest; refuses to replace a differing one")
	args = parser.parse_args()
	if args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Meteor retained extraction matches its pinned manifest identity.")
	elif args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Wrote {write_extraction_manifest(source_root)}")
	elif args.check:
		check(ROOT)
	else:
		generate(ROOT)
		print(f"Wrote {DEFINITION_PATH}")


if __name__ == "__main__":
	main()
