"""Build reviewed Mustang Pro and Premium/Boss/LE machine definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("mt_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
PREMIUM_MANUAL = "manual.mustang-premium-boss-le"
PRO_MANUAL = "manual.mustang-pro"
VPX_SOURCE = "vpx.mustang-premium-le-vpw-1.27"
ROM_SOURCE = "rom.mustang-le-1.45-static-analysis"
PRO_VPX_SOURCE = "vpx.mustang-pro-85vett-gtxjoe-1.0"
PRO_VPX_TABLE_SOURCE = "vpx-table.mustang-pro-85vett-gtxjoe-1.0"
PRO_RUNTIME_SOURCE = "runtime.mustang-pro.boot-start"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(status: str, *source_refs: str) -> dict[str, object]:
	return {"status": status, "source_refs": list(source_refs)}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


MATRIX_RETURN = [
	("WHT-BRN", "J6-P9"), ("WHT-RED", "J6-P8"), ("WHT-ORG", "J6-P7"), ("WHT-YEL", "J6-P6"),
	("WHT-GRN", "J6-P5"), ("WHT-BLU", "J6-P3"), ("WHT-VIO", "J6-P2"), ("WHT-GRY", "J6-P1"),
	("TAN-BLK", "J12-P9"), ("TAN-RED", "J12-P8"), ("TAN-ORG", "J12-P7"), ("TAN-YEL", "J12-P6"),
	("TAN-GRN", "J12-P4"), ("TAN-BLU", "J12-P3"), ("TAN-VIO", "J12-P2"), ("TAN-WHT", "J12-P1"),
]
MATRIX_DRIVE = [("GRN-BRN", "J1-P1"), ("GRN-RED", "J1-P3"), ("GRN-ORG", "J1-P4"), ("GRN-YEL", "J1-P5")]


PREMIUM_SWITCHES: dict[int, dict[str, object]] = {
	1: {"label": "Right 3-bank target bottom", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	2: {"label": "Right 3-bank target center", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	3: {"label": "Right 3-bank target top", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	4: {"label": "N2O target right", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
	5: {"label": "N2O target center", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
	8: {"label": "Captive ball back", "switch_type": "leaf", "part_number": "500-6227-04"},
	9: {"label": "Captive ball front", "switch_type": "leaf", "part_number": "500-6227-04", "roles": ["position.rest"]},
	10: {"label": "Skill shot", "switch_type": "leaf", "part_number": "500-6227-04", "pulse": True},
	11: {"label": "Outer right top lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	12: {"label": "Inner right top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	13: {"label": "Inner left top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	14: {"label": "Outer left top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	15: {"label": "Tournament start", "switch_type": "button", "part_number": "180-5174-00"},
	16: {"label": "Start", "switch_type": "button", "part_number": "180-5174-00"},
	17: {"label": "Trough #6 (left)", "switch_type": "microswitch", "part_number": "180-5119-02"},
	18: {"label": "Trough #5", "switch_type": "microswitch", "part_number": "180-5119-02"},
	19: {"label": "Trough #4", "switch_type": "microswitch", "part_number": "180-5119-02"},
	20: {"label": "Trough #3", "switch_type": "microswitch", "part_number": "180-5119-02"},
	21: {"label": "Trough #2", "switch_type": "microswitch", "part_number": "180-5119-02"},
	22: {"label": "Trough #1 (right opto)", "switch_type": "opto", "part_number": "515-0173-00"},
	23: {"label": "Trough jam", "switch_type": "opto", "part_number": "515-0173-00"},
	24: {"label": "Left outlane", "switch_type": "leaf", "part_number": "500-6227-03"},
	25: {"label": "Left return lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	26: {"label": "Left slingshot", "switch_type": "leaf", "part_number": "180-5054-00", "pulse": True},
	27: {"label": "Right slingshot", "switch_type": "leaf", "part_number": "180-5054-00", "pulse": True},
	28: {"label": "Right return lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	29: {"label": "Right outlane", "switch_type": "leaf", "part_number": "500-6227-03"},
	30: {"label": "Left pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	31: {"label": "Right pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	32: {"label": "Bottom pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	33: {"label": "Top pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	34: {"label": "(G)EARS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	35: {"label": "G(E)ARS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	36: {"label": "GE(A)RS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	37: {"label": "GEA(R)S drop target", "switch_type": "microswitch", "part_number": "520-5252-02", "roles": ["position.down"]},
	38: {"label": "GEAR(S) drop target", "switch_type": "microswitch", "part_number": "520-5252-02", "roles": ["position.down"]},
	39: {"label": "Mid ramp exit", "switch_type": "opto", "part_number": "500-6775-01", "pulse": True},
	40: {"label": "Upper ramp exit", "switch_type": "opto", "part_number": "500-6775-01", "pulse": True},
	41: {"label": "Shift target left", "switch_type": "microswitch", "part_number": "515-7498-02-01", "pulse": True},
	42: {"label": "Shift target right", "switch_type": "microswitch", "part_number": "515-7498-06-00", "pulse": True},
	43: {"label": "Right scoop", "switch_type": "microswitch", "part_number": "180-5183-00", "roles": ["ball.loaded"]},
	44: {"label": "Right orbit", "switch_type": "leaf", "part_number": "500-6227-03", "pulse": True},
	45: {"label": "Left orbit", "switch_type": "leaf", "part_number": "500-6227-03", "pulse": True},
	46: {"label": "Bowl switch", "switch_type": "leaf", "part_number": "180-5057-00", "pulse": True},
	47: {"label": "Shooter lane", "switch_type": "microswitch", "part_number": "180-5157-00"},
	48: {"label": "Spinner", "switch_type": "other", "part_number": "180-5010-04", "pulse": True},
	49: {"label": "Mid ramp down", "switch_type": "other", "roles": ["position.down"]},
	50: {"label": "Upper ramp down", "switch_type": "other", "roles": ["position.down-runtime"]},
	52: {"label": "Turntable index", "switch_type": "opto", "part_number": "520-6931-00", "pulse": True, "roles": ["position.index"]},
	53: {"label": "Turntable home", "switch_type": "opto", "part_number": "520-6931-00", "roles": ["position.home"]},
	54: {"label": "Left lane target", "switch_type": "microswitch", "part_number": "515-7568-09", "pulse": True},
	55: {"label": "N2O target left", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
	56: {"label": "Right 1-bank drop target", "switch_type": "microswitch", "part_number": "520-5252-01", "roles": ["position.down"]},
	57: {"label": "Left 1-bank drop target", "switch_type": "microswitch", "part_number": "520-5252-01", "roles": ["position.down"]},
}


PRO_SWITCHES: dict[int, dict[str, object]] = {
	1: {"label": "Right 3-bank target bottom", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	2: {"label": "Right 3-bank target center", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	3: {"label": "Right 3-bank target top", "switch_type": "microswitch", "part_number": "515-7568-02", "pulse": True},
	4: {"label": "N2O target center", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
	5: {"label": "N2O target right", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
	8: {"label": "Captive ball back", "switch_type": "leaf", "part_number": "500-6227-04"},
	9: {"label": "Captive ball front", "switch_type": "leaf", "part_number": "500-6227-04", "roles": ["position.rest"]},
	10: {"label": "Skill shot", "switch_type": "leaf", "part_number": "500-6227-04", "pulse": True},
	11: {"label": "Outer right top lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	12: {"label": "Inner right top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	13: {"label": "Inner left top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	14: {"label": "Outer left top lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	15: {"label": "Tournament start", "switch_type": "button", "part_number": "180-5174-00"},
	16: {"label": "Start", "switch_type": "button", "part_number": "180-5174-00"},
	17: {"label": "Trough #6 (left)", "switch_type": "microswitch", "part_number": "180-5119-02"},
	18: {"label": "Trough #5", "switch_type": "microswitch", "part_number": "180-5119-02"},
	19: {"label": "Trough #4", "switch_type": "microswitch", "part_number": "180-5119-02"},
	20: {"label": "Trough #3", "switch_type": "microswitch", "part_number": "180-5119-02"},
	21: {"label": "Trough #2", "switch_type": "microswitch", "part_number": "180-5119-02"},
	22: {"label": "Trough #1 (right opto)", "switch_type": "opto", "part_number": "515-0173-00"},
	23: {"label": "Trough jam", "switch_type": "opto", "part_number": "515-0173-00"},
	24: {"label": "Left outlane", "switch_type": "leaf", "part_number": "500-6227-03"},
	25: {"label": "Left return lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	26: {"label": "Left slingshot", "switch_type": "leaf", "part_number": "180-5054-00", "pulse": True},
	27: {"label": "Right slingshot", "switch_type": "leaf", "part_number": "180-5054-00", "pulse": True},
	28: {"label": "Right return lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	29: {"label": "Right outlane", "switch_type": "leaf", "part_number": "500-6227-03"},
	30: {"label": "Left pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	31: {"label": "Right pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	32: {"label": "Bottom pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	33: {"label": "Top pop bumper", "switch_type": "leaf", "part_number": "180-5015-04", "pulse": True},
	34: {"label": "(G)EARS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	35: {"label": "G(E)ARS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	36: {"label": "GE(A)RS drop target", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	37: {"label": "GEA(R)S drop target", "switch_type": "microswitch", "part_number": "520-5252-02", "roles": ["position.down"]},
	38: {"label": "GEAR(S) drop target", "switch_type": "microswitch", "part_number": "520-5252-02", "roles": ["position.down"]},
	39: {"label": "Mid ramp exit", "switch_type": "opto", "part_number": "500-6775-01", "pulse": True},
	40: {"label": "Upper ramp exit", "switch_type": "opto", "part_number": "500-6775-01", "pulse": True},
	41: {"label": "Shift target left", "switch_type": "microswitch", "part_number": "515-7498-02-01", "pulse": True},
	42: {"label": "Shift target right", "switch_type": "microswitch", "part_number": "515-7498-06-00", "pulse": True},
	43: {"label": "Right scoop", "switch_type": "microswitch", "part_number": "180-5183-00", "roles": ["ball.loaded"]},
	44: {"label": "Right orbit", "switch_type": "leaf", "part_number": "500-6227-03", "pulse": True},
	45: {"label": "Left orbit", "switch_type": "leaf", "part_number": "500-6227-03", "pulse": True},
	46: {"label": "Bowl switch", "switch_type": "leaf", "part_number": "180-5057-00", "pulse": True},
	47: {"label": "Shooter lane", "switch_type": "microswitch", "part_number": "180-5157-00"},
	48: {"label": "Spinner", "switch_type": "other", "part_number": "180-5010-04", "pulse": True},
	54: {"label": "Left lane target", "switch_type": "microswitch", "part_number": "515-7568-09", "pulse": True},
	55: {"label": "N2O target left", "switch_type": "microswitch", "part_number": "515-7581-09", "pulse": True},
}


def matrix_switch(number: int, spec: dict[str, object] | None, sources: tuple[str, ...], status: str) -> dict[str, object]:
	row, column = divmod(number - 1, 16)
	used = spec is not None
	label = str(spec["label"]) if used else f"Unused matrix switch #{number}"
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": bool(spec.get("normally_closed", False)) if used else False,
		"pulse": bool(spec.get("pulse", False)) if used else False,
		"availability": "used" if used else "unused",
		"physical": {"switch_type": str(spec.get("switch_type", "unknown")) if used else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(status, *sources),
	}
	if used and spec.get("part_number"):
		result["physical"]["part_number"] = spec["part_number"]
	if used and spec.get("roles"):
		result["roles"] = spec["roles"]
	return result


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, sources: tuple[str, ...], status: str, normally_closed: bool = False) -> dict[str, object]:
	return {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": normally_closed, "pulse": False, "availability": availability,
		"physical": {"switch_type": switch_type}, "provenance": provenance(status, *sources),
	}


def complete_inputs(switches: dict[int, dict[str, object]], manual: str, validated: bool, premium: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "observed"
	used_sources = (manual, VPX_SOURCE, ROM_SOURCE) if premium and validated else (manual, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE) if validated else (manual,)
	items = [matrix_switch(number, switches.get(number), used_sources if number in switches else (manual,), status) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Action button" if premium else "Unused dedicated switch D7", "used" if premium else "unused", "button" if premium else "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left flipper button", "used", "button", False), (83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False), (81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False), (87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Unused dedicated switch D15", "unused", "unknown", False), (85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "optional", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for device, manual_number, label, availability, switch_type, normally_closed in dedicated:
		items.append(dedicated_switch(device, manual_number, label, availability, switch_type, used_sources if availability != "unused" else (manual,), status, normally_closed))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board between connectors J3 and J13"}, "provenance": provenance(status, manual)})
	return items


def output_device(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], status: str, group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	alias_namespace = {"pinmame.output.solenoid": "pinmame.solenoid", "pinmame.output.lamp": "pinmame.lamp", "pinmame.output.gi": "pinmame.gi"}.get(group, group)
	result: dict[str, object] = {
		"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"aliases": aliases(alias_namespace, address, manual_address),
		"availability": availability, "provenance": provenance(status, *sources),
	}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


MAIN_COIL_WIRING = {
	1: ("YEL-VIO", "J10-P9/10", "BRN-BLK", "J8-P1", 50), 2: ("YEL-VIO", "J10-P9/10", "BRN-RED", "J8-P3", 50),
	3: ("YEL-VIO", "J10-P9/10", "BRN-ORG", "J8-P4", 50), 4: ("YEL-VIO", "J10-P9/10", "BRN-YEL", "J8-P5", 50),
	5: ("YEL-VIO", "J10-P9/10", "BRN-GRN", "J8-P6", 50), 6: ("YEL-VIO", "J10-P9/10", "BRN-BLU", "J8-P7", 50),
	7: ("YEL-VIO", "J10-P9/10", "BRN-VIO", "J8-P8", 50), 8: ("RED-WHT", "J17-P7", "BRN-GRY", "J8-P9", 16),
	9: ("YEL-VIO", "J10-P9/10", "BLU-BRN", "J9-P1", 50), 10: ("YEL-VIO", "J10-P9/10", "BLU-RED", "J9-P2", 50),
	11: ("YEL-VIO", "J10-P9/10", "BLU-ORG", "J9-P4", 50), 12: ("YEL-VIO", "J10-P9/10", "BLU-YEL", "J9-P5", 50),
	13: ("YEL-VIO", "J10-P9/10", "BLU-GRN", "J9-P6", 50), 14: ("YEL-VIO", "J10-P9/10", "BLU-BLU", "J9-P7", 50),
	15: ("RED-YEL", "J10-P6/7", "ORG-GRY", "J9-P8", 50), 16: ("RED-YEL", "J10-P6/7", "ORG-VIO", "J9-P9", 50),
	17: ("ORG", "J6-P10", "VIO-BRN", "J7-P2", 20), 18: ("ORG", "J6-P10", "VIO-RED", "J7-P3", 20),
	19: ("ORG", "J6-P10", "VIO-ORG", "J7-P4", 20), 20: ("ORG", "J6-P10", "VIO-YEL", "J7-P6", 20),
	21: ("ORG", "J6-P10", "VIO-GRN", "J7-P7", 20), 22: ("BRN", "J7-P1", "VIO-BLU", "J7-P8", 20),
	23: ("ORG", "J6-P10", "VIO-BLK", "J7-P9", 20), 24: ("RED", "J16-P4-8", "VIO-GRY", "J7-P10", 5),
	25: ("ORG", "J6-P10", "BLK-BRN", "J6-P1", 20), 26: ("ORG", "J6-P10", "BLK-RED", "J6-P2", 20),
	27: ("ORG", "J6-P10", "BLK-ORG", "J6-P3", 20), 28: ("ORG", "J6-P10", "BLK-YEL", "J6-P4", 20),
	29: ("ORG", "J6-P10", "BLK-GRN", "J6-P5", 20), 30: ("ORG", "J6-P10", "BLK-BLU", "J6-P6", 20),
	31: ("ORG", "J6-P10", "BLK-VIO", "J6-P7", 20), 32: ("ORG", "J6-P10", "BLK-GRY", "J6-P8", 20),
}


AUX_COIL_WIRING = {
	51: ("Q51", "YEL-VIO", "YEL-BRN", 50, "Orbit control gate (left)"),
	52: ("Q52", "YEL-VIO", "YEL-GRY", 50, "Orbit control gate (right)"),
	53: ("Q53", "YEL-VIO", "YEL-ORG", 50, "Right 1-bank drop target up"),
	54: ("Q54", "YEL-VIO", "YEL-BLK", 50, "Right 1-bank drop target down"),
	55: ("Q55", "YEL-VIO", "YEL-GRN", 50, "Left 1-bank drop target up"),
	56: ("Q56", "YEL-VIO", "YEL-BLU", 50, "Left 1-bank drop target down"),
	59: ("Q41", "YEL-VIO", "ORG-BRN", 50, "Right scoop"),
	60: ("Q42", "YEL-VIO", "ORG-RED", 50, "Diverter"),
	61: ("Q43", "ORG", "ORG-BLK", 20, "Backbox flasher #1"),
	62: ("Q44", "ORG", "ORG-YEL", 20, "Backbox flasher #2"),
	63: ("Q45", "ORG", "ORG-GRN", 20, "Backbox flasher #3"),
	64: ("Q46", "ORG", "ORG-BLU", 20, "Unused auxiliary output Q46"),
}


def coil_wiring(address: int) -> dict[str, object] | None:
	if address in MAIN_COIL_WIRING:
		power_wire, power_connection, control_wire, control_connection, voltage = MAIN_COIL_WIRING[address]
		return {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "power_wire": power_wire, "power_connection": power_connection, "control_wire": control_wire, "control_connection": control_connection, "nominal_voltage_v": voltage, "voltage_type": "ac" if address == 8 else "dc"}
	if address in AUX_COIL_WIRING:
		transistor, power_wire, control_wire, voltage, _ = AUX_COIL_WIRING[address]
		return {"board": "12-transistor driver board 520-5326-02", "driver_transistor": transistor, "power_wire": power_wire, "control_wire": control_wire, "nominal_voltage_v": voltage, "voltage_type": "dc"}
	return None


PREMIUM_COILS: dict[int, tuple[str, str, str, str | None, str]] = {
	1: ("Trough up-kicker", "coil", "used", "26-1200 / 090-5044-ND", "1"),
	2: ("Auto launch", "coil", "used", "23-800 / 090-5001-ND", "2"),
	3: ("Mid ramp power", "coil", "used", "Dual-winding 090-5083-00-ND", "3"),
	4: ("Mid ramp hold", "coil", "used", "Dual-winding 090-5083-00-ND", "4"),
	5: ("Upper ramp power", "coil", "used", "Dual-winding 090-5083-00-ND", "5"),
	6: ("Upper ramp hold", "coil", "used", "Dual-winding 090-5083-00-ND", "6"),
	7: ("Center 5-bank drop reset", "coil", "used", "25-1240 / 090-5034-ND", "7"),
	8: ("Shaker motor", "motor", "optional", "502-5027-00", "8"),
	9: ("Left pop bumper", "coil", "used", "26-1200 / 090-5044-ND", "9"),
	10: ("Right pop bumper", "coil", "used", "26-1200 / 090-5044-ND", "10"),
	11: ("Bottom pop bumper", "coil", "used", "26-1200 / 090-5044-ND", "11"),
	12: ("Top pop bumper", "coil", "used", "26-1200 / 090-5044-ND", "12"),
	13: ("Left slingshot", "coil", "used", "26-1200 / 090-5044-ND", "13"),
	14: ("Right slingshot", "coil", "used", "26-1200 / 090-5044-ND", "14"),
	15: ("Left flipper", "coil", "used", "23-900 / 090-5020-30-ND", "15"),
	16: ("Right flipper", "coil", "used", "22-1080 / 090-5032-ND", "16"),
	17: ("Left orbit arrow flasher", "flasher", "used", "LED 113-5034-05", "17"),
	18: ("Right orbit arrow flasher", "flasher", "used", "LED 113-5034-05", "18"),
	19: ("Left slingshot flasher", "flasher", "used", "LED 113-5033-08", "19"),
	20: ("Right slingshot flasher", "flasher", "used", "LED 113-5033-08", "20"),
	21: ("Back-panel left flasher", "flasher", "used", "LED 113-5034-08", "21"),
	22: ("Turntable / car motor", "motor", "used", "041-5111-00", "22"),
	23: ("Back-panel right flasher", "flasher", "used", "LED 113-5034-08", "23"),
	24: ("Optional coin meter", "relay", "optional", "Coin meter", "24"),
	25: ("Pop-bumpers right flasher", "flasher", "used", "LED 113-5034-08", "25"),
	26: ("Pop-bumpers left flasher", "flasher", "used", "LED 113-5033-08", "26"),
	27: ("Right scoop arrow flasher", "flasher", "used", "LED 113-5034-08", "27"),
	28: ("180 flasher", "flasher", "used", "LED 113-5034-08", "28"),
	29: ("Skill-shot flasher", "flasher", "used", "LED 113-5034-08", "29"),
	30: ("Turntable flasher", "flasher", "used", "LED 112-5041-08", "30"),
	31: ("Speaker-panel right flasher", "flasher", "used", "LED 113-5034-05", "31"),
	32: ("Speaker-panel left flasher", "flasher", "used", "LED 113-5034-05", "32"),
	51: ("Left orbit control gate", "coil", "used", "32-1250 / 090-5060-01-FC", "51"),
	52: ("Right orbit control gate", "coil", "used", "32-1250 / 090-5060-01-FC", "52"),
	53: ("Right 1-bank drop target up", "coil", "used", "25-1240 / 090-5034-ND", "53"),
	54: ("Right 1-bank drop target down", "coil", "used", "32-1800 / 090-5031-00-ND", "54"),
	55: ("Left 1-bank drop target up", "coil", "used", "25-1240 / 090-5034-ND", "55"),
	56: ("Left 1-bank drop target down", "coil", "used", "32-1800 / 090-5031-00-ND", "56"),
	57: ("Unused auxiliary address #57", "coil", "unused", None, "not populated"),
	58: ("Unused auxiliary address #58", "coil", "unused", None, "not populated"),
	59: ("Right scoop eject", "coil", "used", "27-1500 / 090-5004-ND", "41"),
	60: ("Ramp diverter", "coil", "used", "32-1250 / 090-5060-01-FC", "42"),
	61: ("Backbox flasher #1", "flasher", "used", "LED 113-5034-08", "43"),
	62: ("Backbox flasher #2", "flasher", "used", "LED 113-5034-08", "44"),
	63: ("Backbox flasher #3", "flasher", "used", "LED 113-5034-08", "45"),
	64: ("Unused 12-transistor output Q46", "coil", "unused", None, "46"),
	65: ("Unused auxiliary address #65", "coil", "unused", None, "not populated"),
	66: ("Unused auxiliary address #66", "coil", "unused", None, "not populated"),
}


def premium_coils() -> list[dict[str, object]]:
	items = []
	for address, (label, kind, availability, part_number, manual_address) in PREMIUM_COILS.items():
		vpx_callbacks = {1, 2, 3, 4, 5, 6, 7, *range(15, 31), 51, 52, 53, 54, 55, 56, 59, 60}
		sources = (PREMIUM_MANUAL, VPX_SOURCE, CORE_SOURCE) if availability != "unused" and address in vpx_callbacks else (PREMIUM_MANUAL, CORE_SOURCE, ROM_SOURCE)
		physical = {"location": "Playfield, backbox, or cabinet as shown in the service manual"}
		if part_number:
			physical["part_number"] = part_number
		items.append(output_device(address, label, kind, availability, sources, "validated", manual_address=manual_address, physical=physical, wiring=coil_wiring(address)))
	items.append(output_device(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE,), "validated", physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	return items


STANDARD_LAMP_NAMES = [
	"Start button", "Tournament start button", "Unused matrix lamp #3", "Unused matrix lamp #4", "Unused matrix lamp #5", "Unused matrix lamp #6", "Unused matrix lamp #7", "Unused matrix lamp #8",
	"MUSTAN(G)", "MUSTA(N)G", "MUST(A)NG", "MUS(T)ANG", "MU(S)TANG", "M(U)STANG", "(M)USTANG", "Pony top lane #4",
	"Pony top lane #3", "Pony top lane #2", "Pony top lane #1", "Ford top lane #1 (L)", "Ford top lane #2", "Ford top lane #3", "Ford top lane #4", "N2O center",
	"Jackpot right", "Right orbit green", "Right orbit yellow", "Right orbit red", "Multiball", "Right 1-bank drop target", "Jackpot center", "N2O right",
	"Right 3-bank top", "Right 3-bank center", "Right 3-bank bottom", "Right return lane", "Right outlane", "Right special", "Left outlane top", "Left return lane",
	"Left special", "Extra ball", "N2O boost", "Left orbit red", "Left orbit yellow", "Left orbit green", "Jackpot left", "N2O left",
	"Left 1-bank drop target", "2015 Mustang / 2013 Boss 302", "2012 Mustang / 2012 Boss 302", "1968 Mustang / 1969 Boss 302 bottom", "1970 Mustang / 1970 Boss 302", "2011 Mustang / 2011 Boss 302 right", "1965 Mustang / 1969 Boss 302 top", "1969 Mustang / 1970 Boss 429",
	"2000 Mustang / 1971 Boss 351", "Nitrous upgrade", "Body mods", "Drive-train upgrade", "Engine upgrade", "Tire upgrade", "Handling upgrade", "Tech upgrade",
	"1st gear", "3rd gear", "5th gear", "2nd gear", "4th gear", "6th gear", "Unused matrix lamp #71", "Unused matrix lamp #72",
	"Shoot again", "Unused matrix lamp #74", "Unused matrix lamp #75", "Unused matrix lamp #76", "Top pop bumper", "Left pop bumper", "Bottom pop bumper", "Right pop bumper",
]

STANDARD_LAMP_POWER = [
	("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"),
	("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1"),
]
STANDARD_LAMP_RETURN = [
	("RED-BRN", "J12-P1", "Q33"), ("RED-BLK", "J12-P2", "Q34"), ("RED-ORG", "J12-P3", "Q35"), ("RED-YEL", "J12-P4", "Q36"),
	("RED-GRN", "J12-P5", "Q37"), ("RED-BLU", "J12-P6", "Q38"), ("RED-VIO", "J12-P8", "Q39"), ("RED-GRY", "J12-P9", "Q40"),
	("RED-WHT", "J12-P10", "Q41"), ("RED", "J12-P11", "Q42"),
]


EXTENDED_LAMP_NAMES = {
	81: "Grid red 1", 82: "Grid red 2", 83: "Grid red 3", 84: "Grid red 4", 85: "Grid red 5",
	86: "Grid white 1", 87: "Grid white 2", 88: "Grid white 3", 89: "Grid white 4", 90: "Grid white 5",
	91: "Grid blue 1", 92: "Grid blue 2", 93: "Grid blue 3", 94: "Grid blue 4", 95: "Grid blue 5",
	96: "Shift right target", 97: "Shift left target", 98: "Toolbox", 99: "New car", 100: "Upgrade",
	101: "360 bottom", 102: "360 top", 103: "Shoot combo jackpot", 104: "Short cut", 105: "18(0)", 106: "1(8)0", 107: "(1)80", 108: "Mystery Ford",
	109: "Shot arrow #1 white", 110: "Shot arrow #2 white", 111: "Shot arrow #3 white", 112: "Shot arrow #4 white",
	113: "Shot arrow #5 white", 114: "Shot arrow #6 white", 115: "Shot arrow #7 white", 116: "Shot arrow #8 white",
	117: "Shot arrow #1 red", 118: "Shot arrow #1 green", 119: "Shot arrow #1 blue",
	120: "Shot arrow #2 red", 121: "Shot arrow #2 green", 122: "Shot arrow #2 blue",
	123: "Shot arrow #3 red", 124: "Shot arrow #3 green", 125: "Shot arrow #3 blue",
	126: "Shot arrow #4 red", 127: "Shot arrow #4 green", 128: "Shot arrow #4 blue",
	129: "Shot arrow #5 red", 130: "Shot arrow #5 green", 131: "Shot arrow #5 blue",
	132: "Shot arrow #6 red", 133: "Shot arrow #6 green", 134: "Shot arrow #6 blue",
	135: "Shot arrow #7 red", 136: "Shot arrow #7 green", 137: "Shot arrow #7 blue",
	138: "Shot arrow #8 red", 139: "Shot arrow #8 green", 140: "Shot arrow #8 blue",
	141: "Action button white", 142: "Action button red", 143: "Action button green", 144: "Action button blue",
}

# Board-5 diagnostic numbers are physical service-manual addresses. The node firmware
# serializes them in the order below, which is the order PinMAME exposes as lamps
# 81-144. The known-working VPW script independently confirms every non-white channel
# it consumes, including the counterintuitive G/B/R ordering and sign-light shuffle.
EXTENDED_PUBLIC_BY_MANUAL = {
	**{number: number for number in range(81, 98)},
	98: 103, 99: 102, 100: 104, 101: 105, 102: 106, 103: 107, 104: 108, 105: 109, 106: 110, 107: 111, 108: 112,
	109: 98, 110: 99, 111: 100, 112: 101, 113: 113, 114: 114, 115: 115, 116: 116,
	117: 119, 118: 117, 119: 118, 120: 122, 121: 120, 122: 121, 123: 125, 124: 123, 125: 124,
	126: 128, 127: 126, 128: 127, 129: 132, 130: 130, 131: 131, 132: 135, 133: 133, 134: 134,
	135: 138, 136: 136, 137: 137, 138: 141, 139: 139, 140: 140, 141: 129, 142: 144, 143: 142, 144: 143,
}


def standard_lamps(manual: str, validated: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "observed"
	items = []
	for number, label in enumerate(STANDARD_LAMP_NAMES, start=1):
		row, column = divmod(number - 1, 8)
		power_wire, power_connection = STANDARD_LAMP_POWER[column]
		return_wire, return_connection, transistor = STANDARD_LAMP_RETURN[row]
		availability = "unused" if label.startswith("Unused") else "used"
		sources = (manual, VPX_SOURCE, ROM_SOURCE) if validated and availability != "unused" else (manual,)
		part_number = "112-5033-04" if 65 <= number <= 70 else "112-5033-02" if 77 <= number <= 80 else "112-5033-08"
		items.append(output_device(number, label, "lamp", availability, sources, status, "pinmame.output.lamp", str(number), {"part_number": part_number, "location": "Playfield or cabinet as shown on the lamp-location map"}, {"board": "I/O Power Driver board", "driver_transistor": transistor, "power_wire": power_wire, "power_connection": power_connection, "return_wire": return_wire, "return_connection": return_connection, "nominal_voltage_v": 18, "voltage_type": "dc"}, f"lamp.{slug(label)}"))
	return items


def extended_lamps() -> list[dict[str, object]]:
	items = []
	for manual_number, label in EXTENDED_LAMP_NAMES.items():
		public_address = EXTENDED_PUBLIC_BY_MANUAL[manual_number]
		color_channel = label.rsplit(" ", 1)[-1] in {"red", "green", "blue"}
		kind = "rgb_lamp" if color_channel and (label.startswith("Shot arrow") or label.startswith("Action button")) else "lamp"
		location = "Lockbar action button" if manual_number >= 141 else "Playfield" if manual_number not in range(98, 108) else "Playfield sign"
		physical: dict[str, object] = {"location": location, "notes": f"Physical diagnostic lamp #{manual_number} on Mustang node-board system"}
		if 81 <= manual_number <= 97:
			physical.update({"part_number": "520-6822-00A", "location": "Playfield; onboard Board 5 LED"})
		elif 98 <= manual_number <= 107:
			physical["part_number"] = {98: "112-5034-02", 99: "112-5034-06", 100: "112-5034-08", 101: "112-5034-02", 102: "112-5034-02", 103: "112-5034-05", 104: "112-5034-04", 105: "112-5034-07", 106: "112-5034-07", 107: "112-5034-07"}[manual_number]
		elif manual_number == 108:
			physical["part_number"] = "520-5307-00"
		else:
			physical["part_number"] = "520-5333-00"
		items.append(output_device(public_address, label, kind, "used", (PREMIUM_MANUAL, VPX_SOURCE, ROM_SOURCE, CORE_SOURCE), "validated", "pinmame.output.lamp", str(manual_number), physical, output_id=f"lamp.{slug(label)}"))
	return items


PRO_COILS: dict[int, tuple[str, str, str, str | None]] = {
	1: ("Trough up-kicker", "coil", "used", "26-1200 / 090-5044-ND"),
	2: ("Auto launch", "coil", "used", "23-800 / 090-5001-ND"),
	3: ("Mid ramp power", "coil", "used", "Dual-winding 090-5083-00-ND"),
	4: ("Mid ramp hold", "coil", "used", "Dual-winding 090-5083-00-ND"),
	5: ("Upper ramp power", "coil", "used", "Dual-winding 090-5083-00-ND"),
	6: ("Upper ramp hold", "coil", "used", "Dual-winding 090-5083-00-ND"),
	7: ("Center 5-bank drop reset", "coil", "used", "25-1240 / 090-5034-ND"),
	8: ("Shaker motor", "motor", "optional", "502-5027-00"),
	9: ("Left pop bumper", "coil", "used", "26-1200 / 090-5044-ND"),
	10: ("Right pop bumper", "coil", "used", "26-1200 / 090-5044-ND"),
	11: ("Bottom pop bumper", "coil", "used", "26-1200 / 090-5044-ND"),
	12: ("Top pop bumper", "coil", "used", "26-1200 / 090-5044-ND"),
	13: ("Left slingshot", "coil", "used", "26-1200 / 090-5044-ND"),
	14: ("Right slingshot", "coil", "used", "26-1200 / 090-5044-ND"),
	15: ("Left flipper", "coil", "used", "23-900 / 090-5020-30-ND"),
	16: ("Right flipper", "coil", "used", "22-1080 / 090-5032-ND"),
	17: ("Left orbit arrow flasher", "flasher", "used", "LED 113-5034-05"),
	18: ("Right orbit arrow flasher", "flasher", "used", "LED 113-5034-05"),
	19: ("Left slingshot flasher", "flasher", "used", "LED 113-5033-08"),
	20: ("Right slingshot flasher", "flasher", "used", "LED 113-5033-08"),
	21: ("Back-panel left flasher", "flasher", "used", "LED 113-5034-08"),
	22: ("Unused coil output #22", "coil", "unused", None),
	23: ("Back-panel right flasher", "flasher", "used", "LED 113-5034-08"),
	24: ("Optional coin meter", "relay", "optional", "Coin meter"),
	25: ("Pop-bumpers right flasher", "flasher", "used", "LED 113-5034-08"),
	26: ("Pop-bumpers left flasher", "flasher", "used", "LED 113-5033-08"),
	27: ("Right scoop arrow flasher", "flasher", "used", "LED 113-5034-08"),
	28: ("180 flasher", "flasher", "used", "LED 113-5034-08"),
	29: ("Skill-shot flasher", "flasher", "used", "LED 113-5034-08"),
	30: ("Unused coil output #30", "coil", "unused", None),
	31: ("Orbit post", "coil", "used", "Step-up driver assembly"),
	32: ("Right scoop", "coil", "used", "Step-up driver assembly"),
}


PRO_LAMP_NAMES = [
	"Start button", "Tournament start button", "Unused matrix lamp #3", "Left outlane bottom", "Left outlane top", "Left return lane", "Right return lane", "Right outlane top",
	"Right outlane bottom", "2012 Mustang", "2015 Mustang", "1968 Mustang", "Shoot again", "1970 Mustang", "2011 Mustang", "1965 Mustang",
	"1969 Mustang", "2000 Mustang", "2nd gear", "4th gear", "1st gear", "3rd gear", "5th gear", "Tech upgrade",
	"Handling upgrade", "4th gear green", "Tire upgrade", "Engine upgrade", "Drive-train upgrade", "Body mods", "N2O upgrade", "Shot arrow #1",
	"Shot arrow #2", "6th gear red", "Jackpot left", "N2O left", "Extra ball", "Start N2O", "Left orbit green", "Left orbit yellow",
	"Left orbit red", "6th gear green", "Unused matrix lamp #43", "Shot arrow #5", "Jackpot center", "Right 3-bank top", "Right 3-bank center", "Right 3-bank bottom",
	"Multiball", "Shot arrow #8 red", "Shot arrow #7", "Jackpot right", "N2O right", "Right orbit green", "Right orbit yellow", "Right orbit red",
	"Shot arrow #3", "Shot arrow #6", "Shot arrow #4", "N2O center", "Pony top lane #1 (L)", "Pony top lane #2", "Pony top lane #3", "Pony top lane #4",
	"(M)USTANG", "M(U)STANG", "MU(S)TANG", "MUS(T)ANG", "MUST(A)NG", "MUSTA(N)G", "MUSTAN(G)", "Ford top lane #1 (L)",
	"Ford top lane #2", "Ford top lane #3", "Ford top lane #4", "Top pop bumper", "Left pop bumper", "Bottom pop bumper", "Right pop bumper",
]


PRO_EXTENDED_LAMP_NAMES = {
	81: "Grid red 1", 82: "Grid red 2", 83: "Grid red 3", 84: "Grid red 4", 85: "Grid red 5",
	86: "Grid white 1", 87: "Grid white 2", 88: "Grid white 3", 89: "Grid white 4", 90: "Grid white 5",
	91: "Grid blue 1", 92: "Grid blue 2", 93: "Grid blue 3", 94: "Grid blue 4", 95: "Grid blue 5",
	96: "Shift right target", 97: "Shift left target", 98: "Toolbox", 99: "New car", 100: "Upgrade", 101: "360 bottom", 102: "360 top", 103: "Shoot combo jackpot", 104: "Short cut", 105: "18(0)", 106: "1(8)0", 107: "(1)80", 108: "Mystery Ford",
}

PRO_EXTENDED_PUBLIC_BY_MANUAL = {
	**{number: number for number in range(81, 98)},
	98: 103, 99: 102, 100: 104, 101: 105, 102: 106, 103: 107, 104: 108, 105: 109, 106: 110, 107: 111, 108: 112,
}


def pro_coils() -> list[dict[str, object]]:
	items = []
	for address, (label, kind, availability, part_number) in PRO_COILS.items():
		physical = {"location": "Playfield, backbox, or cabinet as shown in the Pro service manual"}
		if part_number:
			physical["part_number"] = part_number
		items.append(output_device(address, label, kind, availability, (PRO_MANUAL, PRO_VPX_SOURCE), "validated", manual_address=str(address), physical=physical, wiring=coil_wiring(address)))
	items.append(output_device(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, PRO_RUNTIME_SOURCE), "validated", physical={"notes": "SAM_FASTFLIPSOL synthetic state observed during the isolated run; it is not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	return items


def pro_lamps() -> list[dict[str, object]]:
	items = []
	for number, label in enumerate(PRO_LAMP_NAMES, start=1):
		availability = "unused" if label.startswith("Unused") else "used"
		items.append(output_device(number, label, "lamp", availability, (PRO_MANUAL, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE), "validated", "pinmame.output.lamp", str(number), {"location": "Playfield or cabinet as shown on Pro manual PDF page 18"}, output_id=f"lamp.{slug(label)}"))
	for manual_number, label in PRO_EXTENDED_LAMP_NAMES.items():
		public_address = PRO_EXTENDED_PUBLIC_BY_MANUAL[manual_number]
		items.append(output_device(public_address, label, "lamp", "used", (PRO_MANUAL, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE, CORE_SOURCE), "validated", "pinmame.output.lamp", str(manual_number), {"location": "Board 5 or playfield sign", "notes": f"Physical diagnostic lamp #{manual_number}; PinMAME exposes it as public ChangedLamps channel {public_address}."}, output_id=f"lamp.extended-{manual_number}-{slug(label)}"))
	for public_address in (80, 98, 99, 100, 101):
		items.append(output_device(public_address, f"Unpopulated public lamp channel {public_address}", "lamp", "unused", (PRO_MANUAL, PRO_RUNTIME_SOURCE, CORE_SOURCE), "validated", "pinmame.output.lamp", physical={"notes": "The isolated ROM run emitted this compatibility channel, but the Pro manual and Board-5 remap define no physical lamp at this public address."}, output_id=f"lamp.unpopulated-public-{public_address}"))
	items.append(output_device(0, "General illumination", "gi", "used", (PRO_MANUAL, PRO_RUNTIME_SOURCE), "validated", "pinmame.output.gi", "GI-0", {"location": "Playfield and backbox", "notes": "The isolated mt_145 ROM run observes public GI address 0."}, output_id="gi.general-illumination"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], status: str, positions: list[dict[str, object]] | None = None, assembly_part_number: str | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(status, *sources)}
	if positions:
		result["positions"] = positions
	if assembly_part_number:
		result["assembly_part_number"] = assembly_part_number
	return result


def premium_mechanisms() -> list[dict[str, object]]:
	sources = (PREMIUM_MANUAL, VPX_SOURCE)
	return [
		mechanism("mechanism.trough", "Six-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-6-left", "switch.trough-5", "switch.trough-4", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-opto", "switch.trough-jam"], "The physical trough has six ball-position sensors 17-22 plus jam opto 23. The working VPX script creates six balls but configures cvpmBallStack slots as 23,22,21,20,19,18, omitting physical switch 17 and occupying the jam position; this exact script behavior is recorded because it is the proven controller integration, while authors should construct the seven physical sensors shown by the manual. Output 1 ejects from the right end and the script pulses switch 22 after firing.", sources, "validated"),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 fires the automatic plunger for a ball resting at shooter-lane switch 47. The working recreation fires at force 8 and then pulls the plunger back when the output de-asserts.", sources, "validated"),
		mechanism("mechanism.right-scoop", "Right scoop", "kicker", ["device.right-scoop-eject"], ["switch.right-scoop"], "Switch 43 remains active while a ball is held in the right scoop. Public output 59 is auxiliary-board transistor Q41 and ejects toward 185 degrees with nominal force 20, Z 0.4, and force variation 2 in the working table. Its optional erratic-scoop helper briefly captures the entering ball with a script-only magnet before enabling the physical scoop; it is recreation behavior, not another PinMAME output.", sources, "validated", assembly_part_number="515-7575-00"),
		mechanism("mechanism.captive-ball", "Right captive-ball assembly", "toy", [], ["switch.captive-ball-back", "switch.captive-ball-front"], "One nailed ball moves between back switch 8 and front/rest switch 9. The working script uses force transfer 1, minimum impact force 7, and travel/captive parameter 10, then returns the ball toward switch 9.", sources, "validated"),
		mechanism("mechanism.center-drop-bank", "Center five-bank GEARS drop targets", "drop_target_bank", ["device.center-5-bank-drop-reset"], ["switch.g-ears-drop-target", "switch.g-e-ars-drop-target", "switch.ge-a-rs-drop-target", "switch.gea-r-s-drop-target", "switch.gear-s-drop-target"], "Switches 34-38 latch while their targets are down. Output 7 raises the complete bank; the working script delegates drop motion and reset to cvpmDropTarget.", sources, "validated"),
		mechanism("mechanism.mid-ramp", "Mid raising ramp", "motorized", ["device.mid-ramp-power", "device.mid-ramp-hold"], ["switch.mid-ramp-down"], "The physical ramp has dual power/hold outputs 3 and 4 and down sensor 49. The working script uses output 4 as the sustained position signal: asserted lowers the modeled ramp from height 60 to 0 and enables its upper collision surface; de-asserted raises it back to 60 and disables that surface. It does not drive switch 49, so physical switch placement comes from the manual and runtime polarity needs to follow the ROM diagnostic if a native geometry model is used.", sources, "validated", [{"id": "position.down", "label": "Down", "sensors": ["switch.mid-ramp-down"]}, {"id": "position.up", "label": "Up", "sensors": []}]),
		mechanism("mechanism.upper-ramp", "Upper raising ramp", "motorized", ["device.upper-ramp-power", "device.upper-ramp-hold"], ["switch.upper-ramp-down"], "The upper ramp has dual power/hold outputs 5 and 6. The working script uses output 6 as the sustained position signal: asserted lowers the modeled ramp from height 120 to 60, removes the blocking collision surface, and clears switch 50; de-asserted raises it to 120, restores the collision surface, and activates switch 50.", sources, "validated", [{"id": "position.down", "label": "Down", "sensors": []}, {"id": "position.up", "label": "Up", "sensors": ["switch.upper-ramp-down"], "description": "The manual name says down, but the known-working runtime script makes switch 50 active at the raised stop; use script polarity."}]),
		mechanism("mechanism.turntable", "Rotating Mustang car turntable", "rotary", ["device.turntable-car-motor"], ["switch.turntable-index", "switch.turntable-home"], "Output 22 runs the turntable continuously. The working script rotates the car by 0.1 degree per timer tick, pulses index opto 52 across seven broad sectors with narrow clear gaps, and activates home opto 53 from about 352 degrees through wraparound before clearing it between 3 and 5 degrees.", sources, "validated", [{"id": "position.home", "label": "Home", "sensors": ["switch.turntable-home"]}, {"id": "position.index", "label": "Indexed sector", "sensors": ["switch.turntable-index"]}], "520-6821-00"),
		mechanism("mechanism.single-drop-targets", "Left and right single drop targets", "drop_target_bank", ["device.left-1-bank-drop-target-up", "device.left-1-bank-drop-target-down", "device.right-1-bank-drop-target-up", "device.right-1-bank-drop-target-down"], ["switch.left-1-bank-drop-target", "switch.right-1-bank-drop-target"], "Right switch 56 and left switch 57 stay active while their targets are down. Outputs 53/54 raise/lower the right target and 55/56 raise/lower the left target; the working script updates each sustained switch state directly when those outputs fire.", sources, "validated", [{"id": "position.up", "label": "Up", "sensors": []}, {"id": "position.down", "label": "Down", "sensors": ["switch.left-1-bank-drop-target", "switch.right-1-bank-drop-target"]}]),
		mechanism("mechanism.orbit-gates", "Left and right orbit control gates", "gate", ["device.left-orbit-control-gate", "device.right-orbit-control-gate"], ["switch.left-orbit", "switch.right-orbit"], "Public outputs 51 and 52 independently open the left and right orbit gates while asserted and close them when de-asserted. The nearby orbit switches are 45 and 44 respectively.", sources, "validated"),
		mechanism("mechanism.ramp-diverter", "Left-ramp diverter", "diverter", ["device.ramp-diverter"], [], "Public output 60 is auxiliary-board transistor Q42. While asserted, the working script enables the diverter and routes a ball hitting its trigger to the alternate ramp path; it disables that route when de-asserted. There is no position sensor.", sources, "validated", [{"id": "position.normal", "label": "Normal route", "sensors": []}, {"id": "position.diverted", "label": "Alternate route", "sensors": []}]),
		mechanism("mechanism.pop-bumpers", "Four pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper", "device.top-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper", "switch.top-pop-bumper"], "Switches 30-33 pulse the corresponding pop-bumper assemblies driven by outputs 9-12.", sources, "validated"),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26 and 27 pulse the slingshot assemblies driven by outputs 13 and 14.", sources, "validated"),
		mechanism("mechanism.flippers", "Lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "SAM fast-flip inputs drive outputs 15 and 16. Normally-closed EOS contacts are PinMAME switches 83 left and 81 right; buttons are 84 left and 82 right.", (PREMIUM_MANUAL, VPX_SOURCE, CORE_SOURCE), "validated"),
		mechanism("mechanism.spinner", "Spinner", "other", [], ["switch.spinner"], "Each spinner rotation pulses switch 48. The manual identifies assembly 180-5010-04.", sources, "validated", assembly_part_number="180-5010-04"),
	]


def pro_mechanisms() -> list[dict[str, object]]:
	s = (PRO_MANUAL, PRO_VPX_SOURCE)
	return [
		mechanism("mechanism.trough", "Six-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-6-left", "switch.trough-5", "switch.trough-4", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-opto", "switch.trough-jam"], "The physical trough has six ball-position sensors 17-22 plus jam opto 23. The working Pro script creates six balls in cvpmBallStack slots 23,22,21,20,19,18, omitting physical switch 17 and treating the jam location as occupied. Output 1 ejects at 90 degrees with force 8 and pulses switch 22. Construct all seven physical sensors but preserve this proven runtime ordering for script compatibility.", s, "validated"),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 calls AutoFire for a ball in the shooter lane. The proven table uses cvpmImpulseP power 40, time 0.6, and random variation 0.3; physical shooter-lane switch 47 remains a separate sustained table input.", s, "validated"),
		mechanism("mechanism.right-scoop", "Right scoop", "kicker", ["device.right-scoop"], ["switch.right-scoop"], "Switch 43 remains active while a ball is held. Output 32 ejects toward 185 degrees with nominal force 20, Z 0.4, and force variance 2. The proven table lowers the entering ball by 4 units every 2 ms until below -30, destroys that render ball, and transfers it into the controller-facing one-ball stack.", s, "validated"),
		mechanism("mechanism.captive-ball", "Right captive-ball assembly", "toy", [], ["switch.captive-ball-back", "switch.captive-ball-front"], "One nailed ball moves between back switch 8 and front/rest switch 9. The proven table initializes captive travel parameter 10, force transfer 1, minimum impact force 7, and returns the ball toward the front/rest position.", s, "validated"),
		mechanism("mechanism.center-drop-bank", "Center five-bank GEARS drop targets", "drop_target_bank", ["device.center-5-bank-drop-reset"], ["switch.g-ears-drop-target", "switch.g-e-ars-drop-target", "switch.ge-a-rs-drop-target", "switch.gea-r-s-drop-target", "switch.gear-s-drop-target"], "Switches 34-38 latch while their targets are down. Output 7 raises the complete bank through cvpmDropTarget.", s, "validated", [{"id": "position.up", "label": "All raised", "sensors": []}, {"id": "position.down", "label": "Individual target down", "sensors": ["switch.g-ears-drop-target", "switch.g-e-ars-drop-target", "switch.ge-a-rs-drop-target", "switch.gea-r-s-drop-target", "switch.gear-s-drop-target"]}]),
		mechanism("mechanism.mid-ramp", "Mid raising ramp", "motorized", ["device.mid-ramp-power", "device.mid-ramp-hold"], ["switch.mid-ramp-exit"], "The physical assembly has separate power output 3 and hold output 4. The proven table keys route geometry from output 4: asserted opens its gate and makes the bottom/mid ramp surface visible and collidable; de-asserted closes the gate and removes that surface. Switch 39 pulses when a ball exits the route and is not a position sensor.", s, "validated", [{"id": "position.route-enabled", "label": "Ramp route enabled", "sensors": []}, {"id": "position.route-disabled", "label": "Ramp route disabled", "sensors": []}]),
		mechanism("mechanism.upper-ramp", "Upper raising ramp", "motorized", ["device.upper-ramp-power", "device.upper-ramp-hold"], ["switch.upper-ramp-exit"], "The physical assembly has separate power output 5 and hold output 6. The proven table keys route geometry from output 6: asserted opens its gate and makes the upper-ramp surface visible and collidable; de-asserted closes the gate and removes that surface. Switch 40 pulses when a ball exits the route and is not a position sensor.", s, "validated", [{"id": "position.route-enabled", "label": "Ramp route enabled", "sensors": []}, {"id": "position.route-disabled", "label": "Ramp route disabled", "sensors": []}]),
		mechanism("mechanism.orbit-post", "Dual orbit posts", "gate", ["device.orbit-post"], ["switch.right-orbit", "switch.left-orbit"], "Output 31 drives two posts as one logical mechanism. The posts initialize dropped. While output 31 is asserted both posts rise; when de-asserted both drop. Right and left orbit passage switches are 44 and 45 and do not report post position.", s, "validated", [{"id": "position.down", "label": "Posts dropped", "sensors": []}, {"id": "position.up", "label": "Posts raised", "sensors": []}]),
		mechanism("mechanism.bowl", "Whirlpool bowl", "other", [], ["switch.bowl-switch"], "The passive whirlpool/bowl has no dedicated controller output. The proven table holds switch 46 active while a ball occupies its scoring trigger and clears it on exit; reproduce the physical bowl geometry so traversal and dwell drive that switch naturally.", s, "validated"),
		mechanism("mechanism.pop-bumpers", "Four pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper", "device.top-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper", "switch.top-pop-bumper"], "Switches 30-33 pulse the corresponding pop-bumper assemblies driven by outputs 9-12. The proven table maps its visual bumper objects to switches 31, 30, 32, and 33 respectively, while the service-manual labels in the JSON remain authoritative for physical placement.", s, "validated"),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26 and 27 pulse the left and right slingshot assemblies driven by outputs 13 and 14.", s, "validated"),
		mechanism("mechanism.flippers", "Lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "SAM fast-flip inputs drive outputs 15 and 16. Normally-closed EOS contacts are PinMAME switches 83 left and 81 right; buttons are 84 left and 82 right.", (PRO_MANUAL, PRO_VPX_SOURCE, CORE_SOURCE), "validated"),
		mechanism("mechanism.spinner", "Spinner", "other", [], ["switch.spinner"], "Each spinner rotation pulses switch 48. The manual identifies assembly 180-5010-04.", s, "validated", assembly_part_number="180-5010-04"),
	]


def driver_records(premium: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		is_premium = bool(re.fullmatch(r"mt_\d+h(?:b|c)?", driver_id))
		if is_premium != premium:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		if driver_id.endswith("c"):
			record["variant_notes"] = "Colored-ROM modification only; physical playfield I/O, mechanisms, wiring, and native 128x32 DMD topology are unchanged."
		elif driver_id.endswith("hb"):
			record["variant_notes"] = "Boss trim/art package using the same Premium/LE playfield I/O, mechanisms, wiring, and native display topology."
		else:
			record["variant_notes"] = "Firmware revision within this physical edition; playfield I/O, mechanisms, wiring, and native display topology are unchanged."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(manual: str, premium: bool) -> list[dict[str, object]]:
	manual_record = {
		"id": manual, "kind": "manual", "uri": "https://www.sternpinball.com/manuals/",
		"sha256": "b2ae8cdffdfba0640e4f82951369b0596d7599f52111acd1cf794918145917cc" if premium else "63d0b8d44dadb22e8e878586805f805b71aa65038a77e00f5b973ece3b118235",
		"locator": "Mustang_LE_web.pdf, PDF pages 8-17 and mechanism/parts drawings" if premium else "Mustang-Manual.pdf, PDF pages 12-20 and mechanism/parts drawings",
		"license": "NOASSERTION", "attribution": "Stern Pinball", "source_id": "stern", "original_filename": "Mustang_LE_web.pdf" if premium else "Mustang-Manual.pdf", "rights": "NOASSERTION",
		"acquired_at": "2026-08-02T12:34:45.914940Z" if premium else "2026-08-02T12:04:21.184683Z",
	}
	result = [manual_record]
	if premium:
		result.extend([
			{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/special_audiopan_and_audiofade_patched/Mustang%20(Stern%202014)%20v1.27.vbs", "revision": VPX_REVISION, "sha256": "092611fc754374d11d032b81b63638b5a2dc2f43464ee6c7c3cd27874c77e5c3", "locator": "Mustang (Stern 2014) v1.27.vbs lines 138, 204-300, 420-780, 850-930, 1280-1445, and lamp update routines", "license": "NOASSERTION", "attribution": "VPW contributors, prior table authors, and vpxtable_scripts contributors"},
			{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "https://sternpinball.com/wp-content/uploads/2018/11/MUS145LE.BIN", "sha256": "4d26f0cca37435800ea84fa6687e0d6be006437194db36d9087e0e8bcdb9cf25", "locator": "MUS145LE.BIN / mt_145h.bin, 63098052 bytes, CRC32 20ec78b3; PinMAME ROM_LOAD in src/wpc/sam.c and Ghidra raw image base 0x04000000", "license": "NOASSERTION", "attribution": "Stern Pinball firmware; analyzed locally from the user-authorized ROM corpus and official Stern download"},
		])
	else:
		result.extend([
			{"id": PRO_VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "https://vpuniverse.com/files/file/4243-mustang-pro-physmod5-85vett-gtxjoe-mod/", "sha256": "3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c", "locator": "Mustang Pro_85vett_mod_gtxjoe_1.0.vpt from Mustang-Pro-85vett-gtxjoe-v1.0.zip SHA-256 d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615; independently recovered from public archive torrent cf094d405b0a4fc828913b1c139e20960644b660, file index 72", "license": "NOASSERTION", "attribution": "85vett original table; gtxjoe mod; VPU and public archive contributors"},
			{"id": PRO_VPX_SOURCE, "kind": "vpx_script", "uri": "https://vpuniverse.com/files/file/4243-mustang-pro-physmod5-85vett-gtxjoe-mod/", "sha256": "4ddf63df5b96e20da501ae336948e877473d21a4eeaf118a58bb7fcba9105a00", "locator": "GameStg/GameData CODE extracted mechanically from Mustang Pro_85vett_mod_gtxjoe_1.0.vpt; lines 20, 39-88, 154-228, 262-331, 361-390, 423-551", "license": "NOASSERTION", "attribution": "85vett original table; gtxjoe mod"},
			{"id": PRO_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/mt_145/boot-start-pro-1.json", "sha256": "c5002a38d3a392aec6e0160e1cd7988917e38e6118e375ef8e7f03e8d9b7bfe2", "locator": "Isolated LibPinMAME boot/start scenario using physically compatible mt_145.zip SHA-256 4240f7e311dfc571d8d1149e703d5f251d45b4dbccd3dfe157f781e750de7409; captures the script-compatible six-ball trough/captive state, native 128x32x4 DMD, GI 0, standard lamps, and public Board-5 lamps through 112", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
		])
	result.extend([
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Mustang INITGAME/node-board declarations and src/wpc/core.c custom-solenoid mapping", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	])
	return result


def build_premium() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.mustang-premium-limited-edition-boss.2014", "name": "Mustang Premium / Limited Edition / Boss", "manufacturer": "Stern", "year": 2014, "ipdb_id": 6099},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(True), "inputs": complete_inputs(PREMIUM_SWITCHES, PREMIUM_MANUAL, True, True), "outputs": premium_coils() + standard_lamps(PREMIUM_MANUAL, True) + extended_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, VPX_SOURCE)}],
		"mechanisms": premium_mechanisms(), "relationships": [], "sources": sources(PREMIUM_MANUAL, True),
		"knowledge": {"path": "knowledge/stern/mustang-premium-limited-edition-boss-2014.md", "status": "complete"}, "conflicts": [],
	}


def build_pro() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.mustang-pro.2014", "name": "Mustang Pro", "manufacturer": "Stern", "year": 2014, "ipdb_id": 6098},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(False), "inputs": complete_inputs(PRO_SWITCHES, PRO_MANUAL, True, False), "outputs": pro_coils() + pro_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, PRO_RUNTIME_SOURCE)}],
		"mechanisms": pro_mechanisms(), "relationships": [], "sources": sources(PRO_MANUAL, False),
		"knowledge": {"path": "knowledge/stern/mustang-pro-2014.md", "status": "complete"}, "conflicts": [],
	}


PREMIUM_KNOWLEDGE = """# Mustang Premium / Limited Edition / Boss (Stern, 2014)

Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**

## Identity and variants

This definition covers the shared Premium, Limited Edition, and Boss playfield used by PinMAME `mt_*h`, `mt_*hb`, and `mt_*hc` drivers. Boss changes the presentation package; `c` changes ROM display colorization. Non-`h` drivers are the physically different Pro machine and belong to a separate partial definition.

## Evidence precedence

The known-working VPW table script `Mustang (Stern 2014) v1.27.vbs` is authoritative for controller-facing addresses, callbacks, initial runtime state, active polarity, ball routing, and mechanism causality. The official Stern manual is authoritative for physical device inventory, construction, wiring, part numbers, and diagnostic numbering. Pinned PinMAME source is authoritative for SAM controller topology, custom-solenoid routing, display shape, and driver identity. Static analysis of exact Mustang 1.45 LE firmware supports ROM-resident diagnostic semantics but never overrides observed working-script behavior.

## Switch topology

Matrix switches 1-64, dedicated D1-D8 at public 65-72, flipper switches D9-D16 at public 81-88, D17-D24 at public -7 through 0, and DIP D25-D32 are all enumerated. Switches 49 and 50 are the mid-ramp-down and upper-ramp-down positions shown by the manual; the working script only actively updates 50. Switches 52 and 53 are the turntable index and home optos. Single drop targets are 56 right and 57 left. The normally-closed EOS contacts are 83 left and 81 right.

## Lamp addressing

Physical service-manual diagnostic numbers and PinMAME callback channels are not identical for the 64 Board-5 LED channels. The JSON therefore keeps the physical number as `manual.address` while binding the public `ChangedLamps` address. Standard lamps 1-80 are direct. Diagnostic 98 Toolbox is public 103 and diagnostic 99 New Car is public 102. Diagnostic white arrows 109-112 are public 98-101; 113-116 remain public 113-116. RGB channels serialize in G/B/R-style groups: for example physical arrow-1 diagnostics 117/118/119 map to public 119/117/118. Physical action-button white 141 is public 129, and red/green/blue 142/143/144 map to public 144/142/143. Bind the controller to JSON addresses, not the printed diagnostic number.

## Coils and auxiliary driver board

Main outputs 1-32 use the SAM I/O Power Driver board. The 12-transistor board 520-5326-02 is split by PinMAME into public addresses 51-56 for physical Q51-Q56 and public 59-64 for physical Q41-Q46. Thus the right scoop printed as manual output 41 is public 59, the diverter 42 is public 60, backbox flashers 43-45 are public 61-63, and unused Q46 is public 64. Public holes 57, 58, 65, and 66 are enumerated as unused so the complete 16-custom-solenoid SAM space remains explicit.

## Trough and shooter lane

The manual defines six ball-position sensors 17-22 plus jam opto 23. The working script creates six balls but calls `InitSw 0,23,22,21,20,19,18,0`, so its proven runtime model occupies 18-23 and omits physical sensor 17. Recreate all seven physical inputs, preserve the script-compatible runtime ordering until a ROM harness proves a better mapping, and keep this discrepancy visible. Output 1 ejects from the right end and the script pulses switch 22; output 2 auto-launches from shooter-lane switch 47.

## Raising ramps

The mid ramp uses power output 3, hold output 4, and physical down switch 49. The working script keys motion from hold output 4 but does not update 49: asserted lowers its modeled height from 60 to 0 and enables the upper collision surface, while de-asserted raises it and removes that surface. The upper ramp similarly uses power 5 and hold 6; asserted hold lowers from 120 to 60, removes its blocker, and clears switch 50, while de-asserted raises it, restores the blocker, and activates 50. Follow this working-script polarity even though the printed `Upper Ramp Down` label makes the active raised state counterintuitive.

## Turntable and car

Output 22 runs the Mustang car turntable. The working recreation advances the car by 0.1 degree per timer tick. Index opto 52 is active across seven broad sectors separated by narrow clear windows. Home opto 53 becomes active above roughly 352 degrees through wraparound and clears between approximately 3 and 5 degrees. The car and opposite decorative disc rotate in opposite directions; sample current turntable angle for any attached visuals rather than assuming a fixed home-only animation.

## Drop targets and gates

GEARS switches 34-38 latch while down and output 7 resets the entire five-bank. The right single target uses switch 56 with outputs 53 up and 54 down; the left uses switch 57 with outputs 55 up and 56 down. Their switch states are sustained. Public outputs 51 and 52 open the left and right orbit gates while asserted. Public output 60 selects the alternate left-ramp route and has no separate position sensor.

## Scoop and captive ball

The right scoop holds a ball on switch 43 and public output 59 ejects it. The working table uses direction 185 degrees, force 20, Z 0.4, and force variance 2. Its optional erratic-scoop helper momentarily applies a script-only magnet to make settling look natural; do not invent a PinMAME magnet output for it. The captive-ball assembly contains one nailed ball, uses back switch 8 and front/rest switch 9, and in the working recreation uses force transfer 1, minimum impact force 7, and captive travel parameter 10.

## Standard mechanisms

Four pop bumpers pair switches 30-33 with outputs 9-12. Slingshots pair switches 26/27 with outputs 13/14. Lower flippers use outputs 15/16, buttons 84/82, and normally-closed EOS inputs 83/81. Spinner rotations pulse switch 48. Standups 1-5, 41-42, and 54-55 pulse; lane, orbit, outlane, trough, scoop, ramp, and target-position switches remain active while occupied or positioned as described by the JSON.

## Recreation checklist

- Build every physical input and output listed in the JSON, including explicit unused controller addresses, the seven trough/jam sensors, 12-transistor board, standard matrix lamps, Board-5 LEDs, and native 128x32 DMD.
- Initialize the five-bank and both single targets raised, the turntable at home, ramps according to the working callback states, and the captive ball at front/rest switch 9.
- Use public callback bindings from the JSON for node-board LEDs and auxiliary outputs; retain printed numbers as diagnostic aliases only.
- Preserve separate power and hold windings for both ramps even though the working VPX animation keys primarily from hold outputs.
- Treat VPX force, angle, travel, and timing values as proven authoring starting points; refine geometry against physical measurements without changing controller causality.

## Sources

- `manual.mustang-premium-boss-le`: official Stern manual `Mustang_LE_web.pdf`, SHA-256 `b2ae8cdffdfba0640e4f82951369b0596d7599f52111acd1cf794918145917cc`; I/O tables on PDF pages 8-17 and parts/mechanism drawings later in the document.
- `vpx.mustang-premium-le-vpw-1.27`: known-working VPW script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `092611fc754374d11d032b81b63638b5a2dc2f43464ee6c7c3cd27874c77e5c3`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and Mustang node-board/custom-solenoid configuration.
- `rom.mustang-le-1.45-static-analysis`: exact 1.45 LE image, CRC32 `20ec78b3`, SHA-256 `4d26f0cca37435800ea84fa6687e0d6be006437194db36d9087e0e8bcdb9cf25`; ROM bytes remain external and are never committed.
"""


PRO_KNOWLEDGE = """# Mustang Pro (Stern, 2014)

Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**

## Identity and variants

This definition covers the physical Pro playfield used by non-`h` PinMAME drivers `mt_120`, `mt_130`, `mt_140`, `mt_145`, and colored-ROM variant `mt_145c`. IPDB 6098 identifies the Stern SAM Pro machine from April 2014; Premium, Limited Edition, and Boss use the physically different `h` family and a separate definition.

## Evidence precedence

The recovered working Mustang Pro PhysMod5 table by 85vett with gtxjoe's 1.0 functional mod is authoritative for controller-facing addresses, callback polarity, initial state, ball routing, mechanism causality, and the Board-5 lamp shuffle. The official Stern Pro manual is authoritative for the physical inventory, labels, wiring, part numbers, and printed diagnostic numbers. Pinned PinMAME source is authoritative for SAM topology and driver identity. An isolated exact-ROM run independently confirms the native display, GI address, and public lamp range. When these sources differ, preserve both physical and runtime facts and follow the proven table script for controller behavior.

## Physical differences from Premium/LE

The Pro lacks the Premium/LE turntable and its index/home switches, both single drop targets, auxiliary orbit gates, ramp diverter, lockbar action button, RGB arrow/action lighting, and 12-transistor auxiliary output board. Matrix positions 49-53 and 56-64 are therefore unused. The Pro instead has a dual orbit-post mechanism at output 31 and right-scoop eject at output 32 through step-up drivers. N2O center/right are switches 4/5, spinner is 48, the standard lamp matrix uses Pro-specific labels, and its white/grid/sign Board-5 inventory ends at printed diagnostic 108.

## Switch topology

Matrix switches 1-64, dedicated D1-D8 at public 65-72, flipper switches D9-D16 at public 81-88, D17-D24 at public -7 through 0, and DIP D25-D32 are explicitly enumerated, including unused addresses. Normally-closed EOS inputs are 83 left and 81 right; flipper buttons are 84 left and 82 right. Momentary playfield contacts are marked `pulse`; lanes, trough, scoop, captive-ball, and other occupancy contacts remain sustained while occupied. The passive bowl/whirlpool holds switch 46 active from trigger entry until exit.

## Lamp addressing and GI

Standard matrix lamps 1-80 are direct. Board-5 printed diagnostics 81-97 are also direct, but printed 98 Toolbox is public `ChangedLamps` channel 103, printed 99 New Car is public 102, and printed 100-108 map to public 104-112. The JSON binds public controller channels and retains every printed value as `manual.address`; never wire the sign lamps by printed number alone. This exact shuffle is implemented by the recovered table and documented by the contemporaneous PinMAME integration discussion. The exact `mt_145` run emits public lamps through 112 and GI channel 0. The native display is a 128x32, depth-4 DMD.

## Trough and shooter lane

The physical trough has six ball sensors 17-22 plus jam opto 23. The recovered table creates six balls using `InitSw 0,23,22,21,20,19,18,0`, so its proven controller model occupies 18-23 and omits physical switch 17. Recreate all seven physical sensors, but use the script-compatible ordering unless a more exact physical simulation deliberately models the discrepancy. Output 1 ejects at 90 degrees with force 8 and pulses switch 22. Output 2 invokes an impulse auto-plunger using power 40, time 0.6, and random variation 0.3; physical shooter-lane occupancy is switch 47.

## Raising ramps

The mid and upper ramp assemblies each have distinct power/hold windings: outputs 3/4 and 5/6. The recovered recreation keys geometry from the hold windings. When output 4 is asserted it opens the mid gate and makes the bottom/mid ramp surface visible and collidable; de-assertion closes it and removes the surface. Output 6 does the equivalent for the upper ramp. Switches 39 and 40 are exit optos that pulse on ball traversal, not ramp-position sensors. Preserve both windings in the authored machine even though the proven script only uses the hold callbacks to select its simplified two-state route geometry.

## Orbit posts

Output 31 controls two physical posts as one mechanism. Both initialize dropped. Assertion raises both posts; de-assertion drops both. Switches 44 right orbit and 45 left orbit report ball passage and do not sense post position. A recreation should therefore animate both posts atomically from the output and let table geometry determine the resulting route.

## Scoop and captive ball

Switch 43 remains active while a ball is held in the right scoop. Output 32 ejects it at 185 degrees with nominal force 20, Z 0.4, and force variance 2. The working table visually sinks an entering ball by 4 units per 2 ms tick until below -30, then transfers it into the controller-facing one-ball stack; this is render/ownership handling rather than an extra PinMAME mechanism. The captive assembly has one nailed ball, back switch 8, front/rest switch 9, travel parameter 10, force transfer 1, and minimum impact force 7.

## Drops, pops, slings, flippers, spinner, and bowl

GEARS switches 34-38 latch individually while down; output 7 raises the complete five-bank. Pop switches 30-33 pair with outputs 9-12 using the physical labels in the service manual. Slingshot switches 26/27 pair with outputs 13/14. Lower flippers use outputs 15/16, buttons 84/82, and normally-closed EOS inputs 83/81. Every spinner rotation pulses switch 48. The passive whirlpool/bowl has no dedicated output and keeps switch 46 active while a ball crosses its trigger.

## Recreation checklist

- Construct every listed physical input and output, including explicit unused controller positions, seven trough/jam sensors, two orbit posts on one output, the two dual-winding ramps, standard lamp matrix, Board-5 grid/sign lighting, GI, and native DMD.
- Initialize both orbit posts dropped, the captive ball at front/rest switch 9, five-bank targets raised, six trough balls with the script-compatible 18-23 ordering, and ramp collision routes according to their hold-output state.
- Bind extended lamps to JSON public addresses and use the printed diagnostics only as physical aliases.
- Keep route-exit switches 39/40 distinct from ramp position; neither ramp has a dedicated position switch on the Pro.
- Treat the recovered table's force, direction, Z, timing, and captive-ball constants as proven authoring starting points; refine geometry against measurements without changing controller causality.

## Sources

- `manual.mustang-pro`: official Stern `Mustang-Manual.pdf`, SHA-256 `63d0b8d44dadb22e8e878586805f805b71aa65038a77e00f5b973ece3b118235`; scanned I/O tables on PDF pages 12, 15, 18, and 20.
- `vpx-table.mustang-pro-85vett-gtxjoe-1.0`: working VPT SHA-256 `3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c`, retained externally under `pinmame-game-code/mt_145/vpx-table`; source archive SHA-256 `d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615`.
- `vpx.mustang-pro-85vett-gtxjoe-1.0`: exact embedded script SHA-256 `4ddf63df5b96e20da501ae336948e877473d21a4eeaf118a58bb7fcba9105a00`, extracted mechanically from the retained VPT.
- `runtime.mustang-pro.boot-start`: exact `mt_145.zip` isolated run; raw evidence SHA-256 `c5002a38d3a392aec6e0160e1cd7988917e38e6118e375ef8e7f03e8d9b7bfe2`, ROM archive SHA-256 `4240f7e311dfc571d8d1149e703d5f251d45b4dbccd3dfe157f781e750de7409`; ROM bytes remain external.
- `pinmame.core.4ec52ff0ac13`: pinned SAM platform and driver configuration.
- IPDB machine 6098: Mustang (Pro), Stern, April 2014; browser-verified because IPDB's Cloudflare gate prevents stable automated retrieval.
"""


def write(path: Path, value: dict[str, object]) -> None:
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json(path, value)


old_stub = ROOT / "machines/stubs/mt_145h.json"
if old_stub.exists():
	old_stub.unlink()
old_knowledge = ROOT / "knowledge/stubs/mt_145h.md"
if old_knowledge.exists():
	old_knowledge.unlink()
write(ROOT / "machines/partial/stern/mustang-premium-limited-edition-boss-2014.json", build_premium())
old_pro = ROOT / "machines/partial/stern/mustang-pro-2014.json"
if old_pro.exists():
	old_pro.unlink()
write(ROOT / "machines/partial/stern/mustang-pro-2014.json", build_pro())
write_text(ROOT / "knowledge/stern/mustang-premium-limited-edition-boss-2014.md", fail_closed_spatial_knowledge("stern.mustang-premium-limited-edition-boss.2014", PREMIUM_KNOWLEDGE))
write_text(ROOT / "knowledge/stern/mustang-pro-2014.md", fail_closed_spatial_knowledge("stern.mustang-pro.2014", PRO_KNOWLEDGE))
