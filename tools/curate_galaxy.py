#!/usr/bin/env python3
"""Curate the physical Stern Galaxy (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and retained-table coordinate is a literal in
``tools/galaxy_data.py`` or here, so regeneration reproduces the canonical definition, its pinned seed, the spatial report and the knowledge
note byte for byte without reading the external evidence roots. ``--check`` refuses drift and ``--regenerate`` is the only path that writes.

Evidence authority follows the runbook. The known-working VPX script owns runtime semantics, this game's own manual (whose schematic pages are
drawn for Galaxy) owns physical construction, wiring and device presence, pinned PinMAME owns controller topology, and the retained harness
runs pair printed numbers with public addresses. Where the machine's own sheets disagree only about a connector pin or wire colour the
disagreement is a device note, not a conflict.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
import galaxy_data as data  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = Path("machines/partial/stern/galaxy-1980.json")
AUTHOR_READY_PATH = Path("machines/author-ready/stern/galaxy-1980.json")
SEED_PATH = Path("tools/seeds/stern/galaxy-1980.json")
KNOWLEDGE_PATH = Path("knowledge/stern/galaxy-1980.md")
SPATIAL_REPORT_PATH = Path("reports/spatial/stern/galaxy-1980.json")
SPATIAL_REPORT_MARKDOWN_PATH = Path("reports/spatial/stern/galaxy-1980.md")
RUNTIME_EVIDENCE_PATH = Path("evidence/runtime/stern/galaxy-diagnostics-and-gameplay.json")
EXCERPT_ROOT = "evidence/excerpts/stern.galaxy.1980"

MACHINE_ID = "stern.galaxy.1980"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "b7857639b384d7b25d398ac925833a607185fce5e231c56ee31be486c5d9937a"
CLONE_ROM_ARCHIVE_SHA256 = "cfba29a71b9fe8e0d108527773f0a5b988078591c88493f4e1a1be720fc4ed52"
CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-stern-mpu200"
MANUAL_SOURCE = "manual.stern.galaxy.1980"
IPDB_SOURCE = "ipdb.980"
SCRIPT_SOURCE = "vpx-script.galaxy-bord-1-2"
SELF_TEST_SOURCE = "runtime.galaxy.self-test"
SOLENOID_TEST_SOURCE = "runtime.galaxy.solenoid-test"
SWITCH_TEST_SOURCE = "runtime.galaxy.switch-test"
GAMEPLAY_SOURCE = "runtime.galaxy.gameplay"
GAME_OVER_SOURCE = "runtime.galaxy.game-over-and-slam"
CLONE_SOLENOID_TEST_SOURCE = "runtime.galaxyb.solenoid-test"

MANUAL_PDF = "Stern_1980_Galaxy_Manual.pdf"
MANUAL_SHA256 = "76a5e744a3377e37f521f5a62c17e37e09a49a27e839db7acd0168c104206ea2"
SCRIPT_PATH = "Galaxy (Stern 1980)/Galaxy (Stern 1980).vbs.original"
SCRIPT_SHA256 = "ac7e8751a2f26307a8d2ddd9a74c64af944b32aef8f2ddf896c1eab13d2856e4"

TABLE_SOURCE = "vpx-table.galaxy-bord-1-2"
TABLE_SCRIPT_SOURCE = "vpx-script.galaxy-bord-1-2-embedded"
EXTRACTION_SOURCE = "vpx-extraction.galaxy-bord-1-2"
TABLE_FILENAME = "Galaxy (Stern 1980).vpx"
TABLE_SHA256 = "5c457aaea7ea8cab3bbe9900756cd90eaa0461413aeea9e3a5e756f21ede77fd"
TABLE_BYTES = 103747584
TABLE_RELATIVE = Path("stern/galaxy-1980/bord-1.2")
EXTRACTION_RELATIVE = TABLE_RELATIVE / "Galaxy (Stern 1980)"
EXTRACTION_MANIFEST_SHA256 = "ebdb7074712c2457cdad50a8e4bea5b9bfac641f59aae6cd10462edccc122446"
EXTRACTION_FILE_COUNT = 1292
EXTRACTION_TOTAL_BYTES = 123292884
TABLE_REFS = (TABLE_SOURCE, TABLE_SCRIPT_SOURCE)

RUN_NAMES = ("self-test", "solenoid-test", "switch-test", "gameplay", "game-over-and-slam", "galaxyb-solenoid-test")
RUN_SOURCES = {"self-test": SELF_TEST_SOURCE, "solenoid-test": SOLENOID_TEST_SOURCE, "switch-test": SWITCH_TEST_SOURCE,
	"gameplay": GAMEPLAY_SOURCE, "game-over-and-slam": GAME_OVER_SOURCE, "galaxyb-solenoid-test": CLONE_SOLENOID_TEST_SOURCE}

BOARD_MPU = "MPU module M-200 A4"
BOARD_SDU = "Solenoid Driver / Voltage Regulator module SDU B-432 A3"
BOARD_LDA = "Lamp Driver module LDA-100 B-431 A5"


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


def located(identifier: str, role: str, groups: list[list[str]], *source_refs: str) -> dict[str, Any]:
	"""One placement per object group; a group of several objects is placed at their mean (a projection)."""
	placements = []
	for index, names in enumerate(groups, start=1):
		x, y = normalize(*object_point(names))
		suffix = f".{index}" if len(groups) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y,
			"provenance": provenance(*source_refs, status="observed")})
	return {"status": "observed", "placements": placements}


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


def run_digests(root: Path = ROOT) -> dict[str, str]:
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)
	return {run["name"]: run["sha256"] for run in runtime["runtime"]["raw_runs"]}


# --- Inputs -------------------------------------------------------------------------------------------------------------


def matrix_wiring(address: int, cabinet: bool) -> dict[str, Any]:
	strobe, row = (address - 1) // 8, (address - 1) % 8
	strobe_wire, strobe_connection = data.CABINET_STROBE0 if cabinet else data.STROBES[strobe]
	return_wire, return_connection = data.CABINET_RETURNS[row] if cabinet else data.RETURNS[row]
	return {"board": BOARD_MPU, "control_wire": strobe_wire, "control_connection": strobe_connection, "return_wire": return_wire, "return_connection": return_connection}


def build_inputs() -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address, spec in sorted(data.SERVICE_SWITCHES.items()):
		refs = {"manual-and-harness": (MANUAL_SOURCE, CORE_SOURCE, SELF_TEST_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE), "core": (CORE_SOURCE,)}[spec["evidence"]]
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
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
		})

	for address in sorted(data.SWITCHES):
		spec = data.SWITCHES[address]
		cabinet = bool(spec.get("cabinet"))
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.switch", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.self-test", "value": str(address)})
		refs = [MANUAL_SOURCE, SWITCH_TEST_SOURCE]
		refs += [GAME_OVER_SOURCE] if address == 8 else [GAMEPLAY_SOURCE]
		if not cabinet:
			refs += [SCRIPT_SOURCE]
		physical: dict[str, Any] = {"switch_type": spec["type"]}
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		construction = ("Normally open contact, drawn on the cabinet sheet without the series diode the playfield sheet draws in the same matrix cell" if address in data.NO_DIODE_SWITCHES
			else "Normally open contact with a series diode on the " + ("cabinet sheet" if cabinet else "playfield wiring diagram"))
		physical["notes"] = f"Switch Identification table: `{spec['printed']}`; matrix sheet: `{spec['matrix']}`. {construction}. " + spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"normally_closed": False,
			"physical": physical,
			"provenance": provenance(*refs),
			"pulse": bool(spec.get("pulse", False)),
			"wiring": matrix_wiring(address, cabinet),
		}
		if spec.get("initial_active"):
			item["initial_active"] = True
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if cabinet:
			physical["location"] = "Coin door and cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			names, projection = data.SWITCH_OBJECTS[address]
			item["spatial"] = located(spec["id"], "sensor", [[name] for name in names], *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE]))
			if projection:
				physical["notes"] += " " + projection
			else:
				physical["notes"] += " Placed on the retained table's " + " and ".join(f"{data.OBJECTS[name][0]} `{name}`" for name in names) + ", which its script binds to this address."
		inputs.append(item)

	for address in data.OPEN_SWITCHES:
		inputs.append({
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.self-test", "value": str(address)}],
			"availability": "unused",
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": f"switch.unused-{address}",
			"kind": "switch",
			"label": f"Unused matrix position {address}",
			"normally_closed": False,
			"physical": {"notes": f"The Switch Identification table prints {address} as `OPEN` and the playfield matrix sheet labels that cell `N/U` (`NOT USED`); neither the location drawing nor the "
				"known-working script uses it. The ROM's switch test still answers a host write there with its number, which proves only the matrix position, not a fitted contact."},
			"provenance": provenance(MANUAL_SOURCE, SWITCH_TEST_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE),
		})

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
				"notes": "PinMAME's synthetic cabinet flipper button position (FLIP_SW(FLIP_L)). The physical button is hard-wired through the flipper enable relay's contacts to its side's flipper coil, "
					"not to the switch matrix, so the switch test does not show it. The retained gameplay run shows PinMAME's flipper outputs answering this address.",
				"quantity": 1,
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE),
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
				"notes": "PinMAME's generic upper flipper button position. Galaxy has one flipper on each side (parts list, playfield parts drawing, IPDB `Flippers (2)`) and the driver declares "
					"FLIP_SW(FLIP_L) only, so no button reaches this position.",
				"switch_type": "button",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
			"pulse": False,
			"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
		})

	for address in sorted(data.DIPS):
		inputs.append({
			"aliases": [{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": "S%d" % address}],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": data.DIPS[address],
			"physical": {
				"location": "MPU module option-switch packages in the backbox",
				"notes": "One of the thirty-two MPU option switches S1-S32 on the MPU module (manual Figure 1). The assignment is the `GALAXY SWITCH ASSIGNMENT` and the adjustment pages 9-13, which "
					"give every one of the thirty-two a function. S33 on the same module is a momentary memory-clear pushbutton, not an option switch.",
				"switch_type": "dip",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})

	for side, address in (("left", 1), ("right", 2)):
		identifier = f"switch.{side}-flipper-end-of-stroke-contact"
		inputs.append({
			"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
			"availability": "used",
			"binding": {"device": address, "group": "physical.input.direct"},
			"id": identifier,
			"kind": "switch",
			"label": f"{side.title()} flipper end-of-stroke contact",
			"normally_closed": True,
			"physical": {
				"location": f"{side.title()} flipper assembly",
				"notes": data.EOS_NOTES + " Placed by projection on the flipper pivot in the retained table, because the contact is mounted on its flipper assembly and has no object of its own.",
				"quantity": 1,
				"switch_type": "leaf",
			},
			"provenance": provenance(MANUAL_SOURCE),
			"pulse": False,
			"spatial": located(identifier, "sensor", [[data.DIRECT_OBJECTS[address]]], TABLE_SOURCE, MANUAL_SOURCE),
		})
	inputs.append({
		"aliases": [{"namespace": "manual.address", "value": "remote-s33"}],
		"availability": "used",
		"binding": {"device": 3, "group": "physical.input.direct"},
		"id": "switch.remote-memory-clear",
		"kind": "switch",
		"label": "Remote S33 memory clear button (coin door)",
		"normally_closed": False,
		"physical": {"location": "Inside the coin door", "notes": data.REMOTE_MEMORY_CLEAR_NOTES, "switch_type": "button"},
		"provenance": provenance(MANUAL_SOURCE),
		"pulse": False,
		"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE),
		"wiring": {"board": "MPU external memory-clear circuit", "control_wire": "W", "control_connection": "A4J3-5", "return_wire": "Y-R", "return_connection": "A3J2-7"},
	})
	return inputs


# --- Outputs ------------------------------------------------------------------------------------------------------------


def coil_wiring(spec: dict[str, Any], physical_number: int) -> dict[str, Any]:
	wiring: dict[str, Any] = {"board": BOARD_SDU, "driver_transistor": f"Q{physical_number}", "nominal_voltage_v": 43, "voltage_type": "dc"}
	if spec.get("wire"):
		wiring["drive_wire"] = spec["wire"]
	if spec.get("conn"):
		wiring["drive_connection"] = spec["conn"]
	return wiring


def build_solenoid_outputs() -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	public_to_physical = {public: number for number, public in data.PHYSICAL_TO_PUBLIC.items()}
	for address, spec in sorted(data.SOLENOIDS.items()):
		physical_number = public_to_physical[address]
		if spec.get("phys") and spec["phys"] != physical_number:
			raise RuntimeError(f"solenoid {address}: data names driver {spec['phys']}, the ROM test pairs {physical_number}")
		unused = bool(spec.get("unused"))
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		aliases += [{"namespace": "manual.self-test", "value": str(physical_number)}, {"namespace": "manual.address", "value": f"SDU-Q{physical_number}"}]
		refs = [MANUAL_SOURCE, SOLENOID_TEST_SOURCE, SELF_TEST_SOURCE, CLONE_SOLENOID_TEST_SOURCE]
		if address in data.GAMEPLAY_SOLENOIDS:
			refs.append(GAMEPLAY_SOURCE)
		if address in data.SCRIPT_SOLENOIDS:
			refs.append(SCRIPT_SOURCE)
		if address in (17, 18, 19, 20):
			refs.append(GAME_OVER_SOURCE)
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
			physical["quantity"] = 1
		printed = data.PRINTED_SOLENOIDS[physical_number]
		physical["notes"] = f"SDU driver Q{physical_number}, printed solenoid {physical_number} `{printed}`; the ROM's solenoid test shows {physical_number} while public {address} fires. " + spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": "unused" if unused else "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": coil_wiring(spec, physical_number),
		}
		if spec.get("roles"):
			item["roles"] = spec["roles"]
		if unused:
			item["spatial"] = not_applicable("unused", MANUAL_SOURCE, SOLENOID_TEST_SOURCE)
		elif spec.get("cabinet"):
			physical["location"] = "Cabinet"
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif spec.get("internal"):
			physical["location"] = spec.get("location", "Solenoid driver board in the backbox")
			item["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		else:
			names, projection = data.SOLENOID_OBJECTS[address]
			groups = [names] if projection and len(names) > 1 else [[name] for name in names]
			item["spatial"] = located(spec["id"], "effect", groups, *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [TABLE_SCRIPT_SOURCE]))
			if projection:
				physical["notes"] += " " + projection
			else:
				physical["notes"] += f" Placed on the retained table's {data.OBJECTS[names[0]][0]} `{names[0]}`, which its script drives from this address."
		outputs.append(item)

	for address, spec in sorted(data.FLIPPERS.items()):
		power = spec["power"]
		outputs.append({
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				*({"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)),
				{"namespace": "manual.self-test", "value": "15"},
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": "coil",
			"label": spec["label"],
			"physical": {
				"part_number": data.FLIPPER_PART,
				"quantity": 1,
				"notes": f"The {spec['side']} flipper (parts list `{data.FLIPPER_PART_ROW}`) is a dual-winding coil hard-wired through the flipper enable relay's contacts to the {spec['side']} cabinet button; "
					f"no numbered solenoid transistor drives it. Public {address} is PinMAME's synthetic held-coil output for the {spec['side']} side (FLIP_SW(FLIP_L)); PinMAME also asserts public {power} "
					f"for the same interval. Both outputs are button states, not measurements of either winding. Placed on the retained table's flipper pivot `{spec['object']}`, which this callback moves.",
			},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, GAMEPLAY_SOURCE, SCRIPT_SOURCE, TABLE_SCRIPT_SOURCE),
			"spatial": located(spec["id"], "effect", [[spec["object"]]], *TABLE_REFS, MANUAL_SOURCE),
			"wiring": {
				"board": "Hard-wired flipper circuit gated by the flipper enable relay (public 19)",
				"control_connection": spec["button_conn"],
				"control_wire": spec["button_wire"],
				"drive_connection": spec["conn"],
				"drive_wire": spec["wire"],
				"nominal_voltage_v": 43,
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
				"(retained gameplay run). It is not another coil and does not measure the power winding."},
			"provenance": provenance(CORE_SOURCE, GAMEPLAY_SOURCE),
			"spatial": not_applicable("virtual", CORE_SOURCE, GAMEPLAY_SOURCE),
		})
	return outputs


def lamp_rows() -> dict[int, list[tuple[str, str, str, int]]]:
	"""Printed lamp-list rows by public address, through the connector block and the decoder table."""
	q_to_public = {q: public for public, q in data.LAMP_TO_Q.items()}
	rows: dict[int, list[tuple[str, str, str, int]]] = {}
	for description, wire, jack, pin in data.LAMP_LIST:
		read_jack, read_pin = data.ROW_PIN_CORRECTIONS.get(description, (jack, int(pin)))
		q = data.LDA_CONNECTORS[read_jack][read_pin]
		rows.setdefault(q_to_public[q], []).append((description, wire, read_jack, read_pin))
	return rows


def build_lamp_outputs() -> list[dict[str, Any]]:
	rows = lamp_rows()
	unused = set(data.UNUSED_LAMP_ADDRESSES)
	if set(rows) | unused != set(data.LAMP_TO_Q) or set(rows) & unused or set(rows) != set(data.LAMP_NAMES):
		raise RuntimeError("Galaxy lamp inventory does not partition the sixty SCR outputs")
	outputs: list[dict[str, Any]] = []
	for address in sorted(data.LAMP_TO_Q):
		q = data.LAMP_TO_Q[address]
		k, a = divmod(address - 1, 16)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.address", "value": f"LDA-Q{q}"})
		wiring: dict[str, Any] = {"board": BOARD_LDA, "driver_transistor": f"Q{q}"}
		detail = f"Lamp Driver SCR Q{q}, decoder U{k + 1} output S{a}, resistor R{q}. Discrete SCR output on the LDA-100, not a lamp matrix."
		if address in unused:
			pins = [f"A5{jack}-{pin}" for jack, pins in data.LDA_CONNECTORS.items() for pin, scr in pins.items() if scr == q]
			wiring["drive_connection"] = ", ".join(pins)
			outputs.append({
				"aliases": aliases,
				"availability": "unused",
				"binding": {"device": address, "group": "pinmame.output.lamp"},
				"id": f"lamp.unused-scr-q{q}",
				"kind": "lamp",
				"label": f"Unused lamp driver SCR Q{q}",
				"physical": {"notes": detail + f" The connector block brings it out on {', '.join(pins)}, but neither of this game's two printed lamp lists gives it a load, the known-working "
					"script binds no light to it, and the ROM drives it only in its own burn-in and lamp tests: it never changes in attract mode, play, drain, tilt, game over or slam in the retained runs."},
				"provenance": provenance(MANUAL_SOURCE, SELF_TEST_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE),
				"spatial": not_applicable("unused", MANUAL_SOURCE, SELF_TEST_SOURCE),
				"wiring": wiring,
			})
			continue
		identifier, label = data.LAMP_NAMES[address]
		lamp_list = rows[address]
		description, wire, jack, pin = lamp_list[0]
		wiring["drive_connection"] = ", ".join(dict.fromkeys(f"A5{row[2]}-{row[3]}" for row in lamp_list))
		wiring["drive_wire"] = wire
		aliases += [{"namespace": "manual.address", "value": f"LDA-{row[2]}-{row[3]}"} for row in lamp_list]
		backbox = description in data.BACKBOX_ROWS
		printed = "; ".join(f"`{row[0]}` ({row[1]}, LDA {row[2]} pin {row[3]})" for row in lamp_list)
		detail += f" Printed load on both of this game's lamp lists: {printed}."
		physical: dict[str, Any] = {"notes": detail}
		refs = [MANUAL_SOURCE, SELF_TEST_SOURCE]
		if address in data.GAMEPLAY_LAMPS:
			refs.append(GAMEPLAY_SOURCE)
		if address in data.LAMP_NOTES:
			physical["notes"] += " " + data.LAMP_NOTES[address]
		item: dict[str, Any] = {
			"aliases": list({(alias["namespace"], alias["value"]): alias for alias in aliases}.values()),
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": identifier,
			"kind": "lamp",
			"label": label,
			"physical": physical,
			"provenance": provenance(*refs),
			"wiring": wiring,
		}
		if backbox:
			physical["location"] = "Backbox"
			item["roles"] = ["cabinet.backglass"]
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		else:
			names = data.LAMP_OBJECTS[address]
			if len(names) > 1:
				physical["quantity"] = len(names)
			item["spatial"] = located(identifier, "emitter", [[name] for name in names], *TABLE_REFS, MANUAL_SOURCE)
			item["provenance"]["source_refs"] = list(dict.fromkeys(item["provenance"]["source_refs"] + [SCRIPT_SOURCE, TABLE_SOURCE, TABLE_SCRIPT_SOURCE]))
			physical["notes"] += " Placed on the retained table's bulb " + " and ".join(f"light `{name}`" for name in names) + ", which its script drives from this address."
		outputs.append(item)
	return outputs


def build_gi() -> dict[str, Any]:
	return {
		"aliases": [],
		"availability": "used",
		"binding": {"device": 1, "group": "physical.output.gi"},
		"id": "gi.general-illumination",
		"kind": "gi",
		"label": "Relay-switched general illumination",
		"physical": {"notes": data.GI_NOTES},
		"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, IPDB_SOURCE),
		"wiring": data.GI_WIRING,
	}


def build_outputs() -> list[dict[str, Any]]:
	outputs = build_solenoid_outputs() + build_lamp_outputs() + [build_gi()]
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


# --- Mechanisms, relationships --------------------------------------------------------------------------------------------


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str, part: str | None = None) -> dict[str, Any]:
	item: dict[str, Any] = {"actuators": actuators, "behavior": behavior, "id": identifier, "kind": kind, "label": label, "provenance": provenance(*sources), "sensors": sensors}
	if part:
		item["assembly_part_number"] = part
	return item


# Drop target, its switch, its knock-down coil, and the stand-up target or lane that spots it.
DROP_TARGETS = (
	("black", 9, 14, "switch.standup-target-upper"),
	("yellow", 10, 13, "switch.standup-target-middle"),
	("blue", 11, 10, "switch.standup-target-lower"),
	("red", 4, 9, None),
)


def build_mechanisms() -> list[dict[str, Any]]:
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	solenoid_id = {address: spec["id"] for address, spec in data.SOLENOIDS.items()}
	return [
		mechanism(
			"mech.out-hole", "Single-ball out-hole and shooter feed", "kicker", ["device.out-hole-kicker"], ["switch.outhole"],
			"Galaxy is a single-ball machine with no trough. The known-working script starts with the ball on the out-hole switch (public 33). When the credit button starts a game the ROM resets the "
			"drop-target bank (public 4) and kicks the out-hole (public 11, J-26-1000), repeating the kick for as long as public 33 stays closed; the retained runs show the repeats stop once 33 opens. "
			"The kick sends the ball to the shooter lane, where the player launches it with the plunger. After every drain the bonus is counted, the player and ball advance, and the kick repeats.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.eject-pocket", "Top eject pocket (saucer)", "kicker", ["device.saucer-eject"], ["switch.saucer"],
			"A saucer at the top centre of the playfield (parts list `Saucer Eject` J-28-2300). A ball in it holds public 40 closed; the ROM scores the pocket's lit value and pulses public 8 about three "
			"seconds after the closure, ejecting the ball (retained gameplay run). The value, shown on the 2,000 to 10,000 inserts (lamps 60, 12, 28, 44, 59), is advanced by the top thumper and the "
			"spinner and reset to 2,000 when the ball drains (manual). The known-working script kicks it out at 110 degrees.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.kicker-lane", "Upper-left kicker lane (kickback)", "kicker", ["device.ball-kicker"], ["switch.kicker-lane"],
			"A lane at the upper left with a roll-over switch (public 35) and a kicker coil (public 5, parts list `Kicker` J-28-2300) at its foot. When the switch closes the ROM scores the lane, "
			"3,000 plus 2,000 for each letter of G-A-L-A-X-Y spotted (manual), and then pulses public 5 about four seconds later, driving the ball back up and out of the lane (retained gameplay run). "
			"The kicker-lane letter lamps (49 X, 33 Y, 50 G, 34 A, 18 L, 2 second A) show the letters spotted.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.four-bank-drop-targets", "Left four-target drop bank with individual knock-down coils", "drop_target_bank",
			["device.drop-target-bank-reset"] + [solenoid_id[coil] for _, _, coil, _ in DROP_TARGETS],
			[switch_id[address] for address in (9, 10, 11, 4)],
			"Four drop targets in one bank on the left side, top to bottom black (switch 9), yellow (10), blue (11) and red (4) (switch location drawing; IPDB `4-bank drop targets (1)`). A target's "
			"switch is closed while it is down. One reset coil (public 4, parts list `Drop Target Reset (1)` B-27-2300) raises the whole bank, and each target has its own knock-down coil (parts list "
			"`Drop Target Reset (Each Target) 4`): public 14 black, 13 yellow, 10 blue and 9 red. The ROM uses the knock-down coils to spot targets: the upper, middle and lower stand-up targets (switches 30, "
			"29, 26) knock down the black, yellow and blue targets, and the return lanes knock down the red one (retained gameplay run; the feature text says the stand-ups spot the matching target). Home "
			"state is all four up. The ROM resets the bank at game start, after every drain and when the fourth target goes down; completing the bank advances the planet ladder (Mercury to Pluto, lamps 54, "
			"38, 22, 6, 53, 37, 21 and 5 in the retained gameplay run).",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.spinner", "Spinning target below the eject pocket", "other", [], ["switch.spinner"],
			"One spin target assembly (A-563-10) hangs across the opening below the eject pocket (switch location drawing). Each rotation closes its contact once; there is no coil or home sensor. It scores "
			"100, 1,000 when its SPIN lamp (1) is lit, and advances the eject pocket value (manual).",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mech.thumper-bumpers", "Three thumper bumpers", "kicker",
			["device.top-thumper-bumper", "device.lower-right-thumper-bumper", "device.lower-left-thumper-bumper"],
			["switch.top-thumper-bumper", "switch.lower-right-thumper-bumper", "switch.lower-left-thumper-bumper"],
			"Three J-26-1200 thumper bumpers. The ROM fires each coil when its own switch closes and scores 1,000 on the 3-ball setting: switch 12 (top) fires public 3, switch 13 (lower right) public 7 "
			"and switch 14 (lower left) public 12 in the retained gameplay run. Printed solenoid numbers are 5, 4 and 10. The top bumper also advances the eject pocket value (manual).",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, SOLENOID_TEST_SOURCE,
		),
		mechanism(
			"mech.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"],
			"Two J-27-1700 slingshots, long ones along each side of the lower playfield. The ROM fires each coil when its switch closes and scores 10: switch 16 fires public 2 (left) and switch 15 "
			"public 1 (right) (retained gameplay run). Printed solenoid numbers are 1 and 2.",
			MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, SOLENOID_TEST_SOURCE,
		),
		mechanism(
			"mech.flippers", "Two dual-winding flippers", "other",
			["device.left-flipper", "device.right-flipper", "device.flipper-enable-relay"],
			["switch.left-flipper-button", "switch.right-flipper-button", "switch.left-flipper-end-of-stroke-contact", "switch.right-flipper-end-of-stroke-contact"],
			"One flipper on each side at the bottom of the playfield (IPDB `Flippers (2)`). Each coil is hard-wired through the contacts of the flipper enable relay to its side's cabinet button. The relay "
			"is public 19 (printed solenoid 15): the ROM raises it when a game starts and drops it on a tilt and at game over (retained runs). Each coil's end-of-stroke contact is closed at rest and "
			"opens at the end of the stroke to insert the hold winding. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside).",
			MANUAL_SOURCE, CORE_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE, GAME_OVER_SOURCE,
		),
		mechanism(
			"mech.ball-gates", "Passive ball gates", "gate", [], [],
			data.GATE_NOTES,
			MANUAL_SOURCE,
		),
	]


def build_relationships() -> list[dict[str, Any]]:
	relationships = []
	for source, destination in (
		("switch.top-thumper-bumper", "device.top-thumper-bumper"),
		("switch.lower-left-thumper-bumper", "device.lower-left-thumper-bumper"),
		("switch.lower-right-thumper-bumper", "device.lower-right-thumper-bumper"),
		("switch.left-slingshot", "device.left-slingshot"),
		("switch.right-slingshot", "device.right-slingshot"),
	):
		relationships.append({"id": f"rel.{destination.split('.', 1)[1]}-fired-by-its-switch", "kind": "direct", "source": source, "destination": destination, "provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.out-hole-kicker-follows-the-out-hole-switch", "kind": "pulse", "source": "switch.outhole", "destination": "device.out-hole-kicker", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.saucer-eject-follows-the-saucer-switch", "kind": "pulse", "source": "switch.saucer", "destination": "device.saucer-eject", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.ball-kicker-follows-the-kicker-lane-switch", "kind": "pulse", "source": "switch.kicker-lane", "destination": "device.ball-kicker", "provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	switch_id = {address: spec["id"] for address, spec in data.SWITCHES.items()}
	solenoid_id = {address: spec["id"] for address, spec in data.SOLENOIDS.items()}
	for colour, address, coil, _ in DROP_TARGETS:
		relationships.append({"id": f"rel.bank-reset-raises-the-{colour}-target", "kind": "pulse", "source": "device.drop-target-bank-reset", "destination": switch_id[address],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
		relationships.append({"id": f"rel.{colour}-knock-down-coil-drops-its-target", "kind": "pulse", "source": solenoid_id[coil], "destination": switch_id[address],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, GAMEPLAY_SOURCE)})
	for side in ("left", "right"):
		relationships.append({"id": f"rel.{side}-flipper-button-gated-by-the-enable-relay", "kind": "relay_gated", "source": f"switch.{side}-flipper-button", "destination": f"device.{side}-flipper",
			"provenance": provenance(MANUAL_SOURCE, GAMEPLAY_SOURCE)})
	relationships.append({"id": "rel.general-illumination-off-while-the-relay-is-energized", "kind": "inverted", "source": "device.general-illumination-relay", "destination": "gi.general-illumination",
		"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE)})
	relationships.sort(key=lambda item: item["id"])
	return relationships


# --- Sources ------------------------------------------------------------------------------------------------------------

# excerpt name -> (locator, has image)
EXCERPTS: dict[str, tuple[str, bool]] = {
	"switch-identification": ("PDF page 16, GALAXY SWITCH IDENTIFICATION SELF TEST DISPLAY NUMBERS", False),
	"switch-locations": ("PDF page 17, SWITCHES GALAXY location drawing and the list of switches not on the playfield", True),
	"solenoid-identification": ("PDF page 18, GALAXY SOLENOID IDENTIFICATION SELF TEST DISPLAY NUMBERS", False),
	"solenoid-locations": ("PDF page 19, SOLENOIDS GALAXY location drawing", True),
	"parts-list": ("PDF page 14, PARTS LIST GAME #114 GALAXY", False),
	"playfield-parts": ("PDF page 15, PLAYFIELD PARTS GALAXY drawing and lists", True),
	"mpu-switch-assignment": ("PDF pages 9-13, GALAXY SWITCH ASSIGNMENT and the credit and game adjustment tables", False),
	"self-test": ("PDF pages 1 and 4, routine maintenance self tests and IV. SELF TEST AND BOOKKEEPING FUNCTIONS", False),
	"general-operation": ("PDF pages 2, 3 and 5, Figure 1, III. GENERAL GAME OPERATION and the front-door adjustments", False),
	"feature-operation": ("PDF pages 7 and 8, feature operation and scoring", False),
	"playfield-switch-matrix": ("PDF page 23, Playfield Wiring Diagram for GALAXY, switch matrix", True),
	"playfield-coil-wiring": ("PDF pages 22 and 23, Playfield Wiring Diagram for GALAXY, coil and flipper wiring", True),
	"playfield-lamp-wiring-list": ("PDF page 22, Playfield Wiring Diagram for GALAXY, typed lamp list", False),
	"lamp-driver-lamp-list": ("PDF page 31, Lamp Driver Schematic 12B-431-S-114 for GALAXY, typed lamp list", False),
	"lamp-driver-connector-labels": ("PDF page 31, Lamp Driver Schematic 12B-431-S-114, connector blocks J1, J2 and J3 with their SCR labels", True),
	"lamp-driver-decoder-outputs": ("PDF page 30, Lamp Driver Schematic 12B-431-S-114, decoder chips U1-U4 with their output resistors and SCRs", True),
	"cabinet-wiring": ("PDF pages 24 and 25, cabinet and front-door wiring", True),
	"solenoid-driver": ("PDF pages 26 and 27, Solenoid Driver / Voltage Regulator Schematic 12B-432-S-114 for GALAXY", True),
	"general-illumination": ("PDF page 34, Transformer Schematic 12B-16B-6 (general use), connector list", False),
}


def excerpt_record(name: str, root: Path) -> dict[str, Any]:
	locator, has_image = EXCERPTS[name]
	path = root / EXCERPT_ROOT / f"{name}.md"
	if not path.is_file():
		raise RuntimeError(f"Galaxy excerpt is missing: {path}")
	record: dict[str, Any] = {
		"id": f"excerpt.galaxy.{name}",
		"locator": locator,
		"method": "manual",
		"path": f"{EXCERPT_ROOT}/{name}.md",
		"reviewed": True,
		"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
		"transcribed_by": "curator, read from the retained rendered page",
	}
	if has_image:
		image = root / EXCERPT_ROOT / f"{name}.webp"
		if not image.is_file():
			raise RuntimeError(f"Galaxy excerpt image is missing: {image}")
		record["image"] = f"{EXCERPT_ROOT}/{name}.webp"
		record["image_sha256"] = hashlib.sha256(image.read_bytes()).hexdigest()
		record["image_derivation"] = data.CROP_DERIVATIONS[name]
	return record


def build_sources(root: Path) -> list[dict[str, Any]]:
	digests = run_digests(root)
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)
	scenario = {run["name"]: (run["scenario_path"], run["scenario_sha256"]) for run in runtime["runtime"]["raw_runs"]}
	manifest = runtime["source"]["sha256"]
	ipdb = "external:pinmame-manuals/by-machine/stern.galaxy.1980/ipdb/"
	sources = [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c CORE_GAMEDEFNV(galaxy) and the four CORE_CLONEDEFNV entries galaxyfp, galaxyps, galaxyb and galaxyc that name it as parent",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "src/wpc/stgames.c INITGAME(galaxy, GEN_STMPU200, dispst6, FLIP_SW(FLIP_L), 0, SNDBRD_ST300, 0), the identical lines of galaxyfp and galaxyps and the dispst7 lines of galaxyb "
				"and galaxyc, with the dispst6 and dispst7 layouts; src/wpc/by35.c by35_lampStrobe, pia1b_w (solenoid decoder low nibble and the inverted continuous high nibble PB4-PB7); "
				"src/wpc/core.h sLRFlip/sLLFlip power and hold addresses 45-48",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/stern-mpu200.json", "revision": "repository",
			"locator": "Stern MPU-200 controller profile: matrix 1-40, diagnostics -7 to -5, flipper-button positions 81-84, option switches 1-32, decoder solenoids 1-15, continuous 17-20 and synthetic flipper outputs 45-48, "
				"sixty discrete SCR lamps 1-63, physical direct inputs 1-3 and GI identity 1",
			"license": "MIT", "attribution": "pinmame-game-defs curation"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://www.ipdb.org/files/980/Stern_1980_Galaxy_Manual.pdf", "original_filename": MANUAL_PDF, "sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-30T00:00:00Z",
			"locator": f"Stern Galaxy game manual (IPDB 980 `English Manual (may be incomplete, with paginated schematics shown in halves)`), 35 pages, each a 2550x3300 grayscale scan at 300 dpi with no "
				f"text layer, retained at {ipdb}. Pages 1-5 maintenance, Figure 1, operation, self test and front-door adjustments; 6 transformer wiring; 7-8 feature operation; 9-13 option switches; 14 "
				"parts list; 15 playfield parts; 16 switch identification; 17 switch locations; 18 solenoid identification; 19 solenoid locations; 20-21 MPU schematic; 22-23 Playfield Wiring Diagram for "
				"GALAXY; 24-25 cabinet wiring; 26-27 Solenoid Driver / Voltage Regulator Schematic 12B-432-S-114 for GALAXY; 28-29 display schematics; 30-31 Lamp Driver Schematic 12B-431-S-114 for "
				"GALAXY; 32-35 wiring diagrams and transformer. Each schematic is printed in two halves on consecutive pages.",
			"license": "NOASSERTION", "attribution": "Stern Electronics, Inc.; scan hosted by the Internet Pinball Database", "rights": "NOASSERTION",
			"excerpts": [excerpt_record(name, root) for name in EXCERPTS]},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=980", "acquired_at": "2026-10-30T00:00:00Z",
			"locator": "IPDB machine 980: Galaxy, Stern Electronics, January 1980, model number 114, MPU Stern M-200, 4,947 units; notable features 'Flippers (2), Pop bumpers (3), Slingshots (2), Star "
				"rollovers (4), Standup targets (3), 4-bank drop targets (1), Spinning target (1), Kick-out saucer (1), Kickback lane, Left and right dual inlanes'; notes that Galaxy has "
				"computer-controlled general illumination; design Harry Williams, art Bob Timm, software Rob Quinn. The page was saved as machine-980.html beside the manual; its title and machine "
				"number match, and the retained manual was downloaded from its links.",
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database"},
		{"id": SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{CORPUS_REVISION}/{SCRIPT_PATH.replace(' ', '%20').replace('(', '%28').replace(')', '%29')}",
			"revision": CORPUS_REVISION, "sha256": SCRIPT_SHA256,
			"locator": f"{SCRIPT_PATH} in the pinned known-working script corpus (bord's Galaxy table 1.2), cGameName = \"galaxy\": SolCallback 4 ResetDropT, 5 solleftout (kicker lane), 6 knocker, 8 "
				"SolTopSaucer (sw40), 9, 10, 13 and 14 drop targets 4, 11, 10 and 9, 11 solrelease (out-hole, switch 33), 15 BRelease (no such Sub is defined), 17 PFGI, 19 vpmNudge.SolGameOn; "
				"bumpers PulseSw 12-14, slings 15 and 16, stand-ups 26, 29, 30, spinner 5; Controller.Switch 18-24, 35-40; Lampz.MassAssign lamp bindings.",
			"license": "NOASSERTION", "attribution": "bord and repository contributors", "known_working": True},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{(TABLE_RELATIVE / TABLE_FILENAME).as_posix()}", "original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256,
			"revision": "bord 1.2", "acquired_at": "2026-10-30T00:00:00Z",
			"locator": f"Galaxy (Stern 1980), bord's table version 1.2 (released May 2018, saved May 2023), {TABLE_BYTES:,} bytes, downloaded by the operator from VPUniverse. Exact playfield bounds left 0, "
				f"top 0, right {data.TABLE_WIDTH:g}, bottom {data.TABLE_HEIGHT:g}; normalized coordinates are x/{data.TABLE_WIDTH:g} and y/{data.TABLE_HEIGHT:g}. The geometry source for every located "
				"placement; it models the two flippers, the left four-bank, the three stand-ups, the saucer, the spinner and the kicker lane where the factory location drawings put them.",
			"license": "NOASSERTION", "attribution": "bord; redistribution rights not granted", "rights": "NOASSERTION"},
		{"id": TABLE_SCRIPT_SOURCE, "kind": "vpx_script", "uri": f"external:pinmame-vpx-sources/{(EXTRACTION_RELATIVE / 'script.vbs').as_posix()}", "original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": "Embedded script of the retained table, 152,392 bytes, cGameName = \"galaxy\"; byte-identical to the pinned corpus script (same SHA-256), so it binds each placement's object.",
			"license": "NOASSERTION", "attribution": "bord", "known_working": True},
		{"id": EXTRACTION_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}", "sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": f"Retained vpxtool git:v0.33.3 extraction of the table; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256} (tools/build_external_evidence_manifest.py: every file as sorted relative POSIX path, "
				f"size and SHA-256, compact canonical JSON plus LF, the manifest files excluded); {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
			"license": "NOASSERTION", "attribution": "bord; redistribution rights not granted"},
	]
	for name in RUN_NAMES:
		game = "galaxyb" if name.startswith("galaxyb") else "galaxy"
		archive = CLONE_ROM_ARCHIVE_SHA256 if game == "galaxyb" else ROM_ARCHIVE_SHA256
		path, scenario_sha = scenario[name]
		sources.append({
			"id": RUN_SOURCES[name],
			"kind": "service_diagnostic" if name in ("self-test", "solenoid-test", "switch-test", "galaxyb-solenoid-test") else "runtime_scenario",
			"uri": f"external:pinmame-review-artifacts/galaxy-1980/harness/{name}/run.json",
			"sha256": digests[name],
			"locator": f"tools/run_pinmame_harness.py with pinmame64.dll SHA-256 {LIBRARY_SHA256} (built from {PINMAME_REVISION[:12]}), driver {game}, ROM archive SHA-256 {archive}; "
				f"scenario {path} (SHA-256 {scenario_sha}), fresh state directory. Run directory manifest SHA-256 {manifest}; compact derived evidence in {RUNTIME_EVIDENCE_PATH.as_posix()}.",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		})
	return sources


# --- Definition ---------------------------------------------------------------------------------------------------------

MISSING = ["spatial_placement"]


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	if len(data.SWITCHES) + len(data.OPEN_SWITCHES) != 40 or set(data.SWITCHES) & set(data.OPEN_SWITCHES) or set(data.DIPS) != set(range(1, 33)):
		raise RuntimeError("Galaxy switch or option-switch inventory is incomplete")
	if sorted(data.PHYSICAL_TO_PUBLIC) != list(range(1, 20)) or set(data.SOLENOIDS) != set(data.PHYSICAL_TO_PUBLIC.values()):
		raise RuntimeError("Galaxy solenoid inventory is incomplete")
	if {q for qs in data.DECODER.values() for q in qs} != set(range(1, 61)):
		raise RuntimeError("Galaxy decoder map does not cover SCRs 1-60 exactly once")
	runtime = load_json(root / RUNTIME_EVIDENCE_PATH)["runtime"]["observations"]
	if {int(key): value for key, value in runtime["physical_service_solenoid_to_public"].items()} != data.PHYSICAL_TO_PUBLIC:
		raise RuntimeError("Galaxy solenoid translation disagrees with the retained solenoid test")
	return build_unchecked_definition(root)


def build_drivers() -> list[dict[str, Any]]:
	drivers = []
	for driver_id in sorted(data.DRIVERS):
		description, year, manufacturer, parent, compatibility, notes = data.DRIVERS[driver_id]
		item: dict[str, Any] = {"description": description, "flags": 0, "id": driver_id, "manufacturer": manufacturer, "physical_compatibility": compatibility, "variant_notes": notes, "year": year}
		if parent:
			item["clone_of"] = parent
		if driver_id in data.SEVEN_DIGIT_DRIVERS:
			refs = (CORE_SOURCE, CLONE_SOLENOID_TEST_SOURCE) if driver_id == "galaxyb" else (CORE_SOURCE,)
			item["display_overrides"] = [{"provenance": provenance(*refs), "segment_start": start, "target": target, "width": 7} for target, start in data.SEVEN_DIGIT_STARTS.items()]
		drivers.append(item)
	return drivers


def build_unchecked_definition(root: Path = ROOT) -> dict[str, Any]:
	return {
		"conflicts": [],
		"controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.stern-mpu200"},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"causal_exercise": "observed",
				"diagnostic_enumeration": "validated",
				"emulator_normalization": "validated",
				"mechanisms": "validated",
				"physical_wiring": "validated",
				"recreation_knowledge": "validated",
				"runtime_observation": "observed",
				"semantic_naming": "validated",
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
		"inputs": build_inputs(),
		"knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "complete"},
		"machine": {"id": MACHINE_ID, "ipdb_id": 980, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "114", "name": "Galaxy", "opdb_id": "GrdDB-ML8xK", "year": 1980,
			"playfield": {"height": data.TABLE_HEIGHT, "provenance": provenance(TABLE_SOURCE), "units": "vpx", "width": data.TABLE_WIDTH}},
		"mechanisms": build_mechanisms(),
		"outputs": build_outputs(),
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(root),
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
	projections = [{"address": address, "group": "pinmame.input.switch", "reason": reason} for address, (_, reason) in sorted(data.SWITCH_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "pinmame.output.solenoid", "reason": reason} for address, (_, reason) in sorted(data.SOLENOID_OBJECTS.items()) if reason]
	projections += [{"address": address, "group": "physical.input.direct", "reason": f"Placed on the {side} flipper pivot: the end-of-stroke contact is mounted on its flipper assembly."}
		for address, side in ((1, "left"), (2, "right"))]
	return {
		"blockers": [
			"Every placement is `observed`: the manual prints no lamp-location drawing, so nothing independent checks the lamp positions, and the switch and coil placements have not been through "
			"the factory location-drawing callout check (tools/drawing_callouts.py) against the manual's switch and solenoid drawings (PDF pages 17 and 19).",
			"General illumination has no placement: no retained source gives its bulb quantity or positions, and the table's GI light collection is render membership, not a socket count.",
		],
		"coordinate_convention": {"source_bounds": {"bottom": data.TABLE_HEIGHT, "left": 0.0, "right": data.TABLE_WIDTH, "top": 0.0}, "space": "playfield",
			"x": f"x/{data.TABLE_WIDTH:g}; 0=left, 1=right", "y": f"y/{data.TABLE_HEIGHT:g}; 0=rear/backglass, 1=apron/player"},
		"excluded_object_classes": data.EXCLUDED_OBJECT_CLASSES,
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_algorithm": "tools/build_external_evidence_manifest.py: every file as sorted relative POSIX path, size and SHA-256, compact canonical JSON plus LF, manifest files excluded",
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE.as_posix()}/manifest.json", "source_ref": EXTRACTION_SOURCE, "total_bytes": EXTRACTION_TOTAL_BYTES,
			"table_sha256": TABLE_SHA256, "script_sha256": SCRIPT_SHA256, "vpxtool_version": "git:v0.33.3"},
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
		"# Galaxy (Stern, 1980) spatial review",
		"",
		"Status: incomplete. Every placement is `observed` and general illumination has none, so the machine record stays `partial` at `machines/partial/stern/galaxy-1980.json`.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}` (bord, version 1.2) at SHA-256 `{TABLE_SHA256}`; its embedded script is byte-identical to the pinned known-working corpus script "
		f"(SHA-256 `{SCRIPT_SHA256}`). Exact playfield bounds are left 0, top 0, right {data.TABLE_WIDTH:g}, bottom {data.TABLE_HEIGHT:g}, and every canonical coordinate is x/{data.TABLE_WIDTH:g} and "
		f"y/{data.TABLE_HEIGHT:g} rounded to six decimal places. Coordinate convention: x=0 left, x=1 right; y=0 rear/backglass, y=1 apron, in normalized VPX/player view.",
		"",
		"## Evidence decisions",
		"",
		"- The script's bindings choose each switch's and coil's object. Each lamp is placed on the bulb light (`L<n>a`) under the insert the script drives from its address, never on the insert overlay.",
		"- The switch, lamp and solenoid assignments agree between the script, this game's lamp lists and the ROM; no table binding defect was found.",
		"",
		"## Explicit projections",
		"",
	]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += ["", "## Counts", ""]
	lines.append(f"- Placements: {sum(item['placements'] for item in report['located_records'])} ({', '.join(f'{count} {name}' for name, count in report['placement_statuses'].items())}) on {len(report['located_records'])} records")
	for reason, ids in report["not_applicable_records"].items():
		lines.append(f"- Records with a controlled `{reason}` record: {len(ids)}")
	lines.append(f"- Records with no spatial key: {len(report['unplaced_records'])} ({', '.join(item['id'] for item in report['unplaced_records']) or 'none'})")
	lines += ["", "## Excluded table objects", ""]
	lines += [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Promotion decision", "",
		"Promotion to `author_ready` is refused: every placement rests on one community table with no independent check, and general illumination has no placement. The record stays `partial` "
		"with `coverage.missing = [\"spatial_placement\"]`.", "",
		"## Retained evidence", "",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Object-centre dump of every extracted game item at `external:pinmame-review-artifacts/galaxy-1980/bord-1.2-geometry.tsv`.", ""]
	return "\n".join(lines)


# --- Generation and checking ------------------------------------------------------------------------------------------


def products(root: Path = ROOT) -> dict[Path, bytes]:
	definition = build_definition(root)
	errors = validate_machine(definition, root)
	if errors:
		raise RuntimeError("Invalid Galaxy definition: " + "; ".join(errors[:20]))
	report = build_spatial_report(definition)
	return {
		DEFINITION_PATH: canonical_bytes(definition),
		SEED_PATH: canonical_bytes(definition),
		SPATIAL_REPORT_PATH: canonical_bytes(report),
		SPATIAL_REPORT_MARKDOWN_PATH: render_spatial_report(report).encode("utf-8"),
		KNOWLEDGE_PATH: data.KNOWLEDGE.encode("utf-8"),
	}


def generate(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Galaxy artifact")
	for path, payload in products(root).items():
		(root / path).parent.mkdir(parents=True, exist_ok=True)
		(root / path).write_bytes(payload)


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("A Galaxy author-ready definition is present although the record is partial")
	for path, payload in products(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != payload:
			raise RuntimeError(f"Galaxy deterministic artifact missing or drifted: {path}")
	print("Galaxy definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, knowledge note and spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		generate(ROOT)
		print(f"Wrote {DEFINITION_PATH}")


if __name__ == "__main__":
	main()
