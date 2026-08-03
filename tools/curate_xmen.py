"""Build reviewed, author-ready X-Men Limited Edition and Pro definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("xmn_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.x-men-pro-le.2012"
MANUAL_HIRES_SOURCE = "manual.x-men-pro-le.2012.high-resolution"
PRODUCT_SOURCE = "stern.x-men-product-page"
LE_VPX_SOURCE = "vpx.x-men-le-vpw-1.0.6"
PRO_VPX_SOURCE = "vpx.x-men-pro-icpjuggla"
PRO_VPX_TABLE_SOURCE = "vpx-table.x-men-pro-physmod5"
LE_RUNTIME_SOURCE = "runtime.x-men-le.boot-start"


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


SWITCHES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	1: ("Left two-bank bottom target", "microswitch", True, ()), 2: ("Left two-bank top target", "microswitch", True, ()),
	4: ("Lower-left eject", "microswitch", False, ("ball.loaded",)), 7: ("Right two-bank top target", "microswitch", True, ()),
	8: ("Right two-bank bottom target", "microswitch", True, ()), 11: ("Left ramp exit", "opto", True, ()),
	12: ("Left Nightcrawler down", "microswitch", False, ("position.down",)), 13: ("Left ramp entrance", "opto", True, ()),
	14: ("Left orbit", "leaf", False, ()), 15: ("Tournament start", "button", False, ()),
	16: ("Start", "button", False, ()), 18: ("Trough 4 left", "microswitch", False, ("ball.position",)),
	19: ("Trough 3", "microswitch", False, ("ball.position",)), 20: ("Trough 2", "microswitch", False, ("ball.position",)),
	21: ("Trough 1 right", "microswitch", False, ("ball.position",)), 22: ("Trough jam", "opto", False, ("ball.position",)),
	23: ("Shooter lane", "microswitch", False, ("ball.position",)), 24: ("Left outlane", "leaf", False, ()),
	25: ("Left return lane", "leaf", False, ()), 26: ("Left slingshot", "leaf", True, ()),
	27: ("Right slingshot", "leaf", True, ()), 28: ("Right return lane left", "leaf", False, ()),
	29: ("Right outlane", "leaf", False, ()), 30: ("Left pop bumper", "leaf", True, ()),
	31: ("Right pop bumper", "leaf", True, ()), 32: ("Bottom pop bumper", "leaf", True, ()),
	33: ("Right return lane right", "leaf", False, ()), 34: ("Iceman home", "microswitch", False, ("position.home",)),
	35: ("Iceman away", "microswitch", False, ("position.away",)), 36: ("Wolverine bash target", "microswitch", True, ()),
	38: ("Center lock 2", "opto", False, ("ball.position",)), 39: ("Center lock 3", "opto", False, ("ball.position",)),
	40: ("Center lock 4 top", "opto", False, ("ball.position",)), 41: ("Light lock target left", "microswitch", True, ()),
	42: ("Light lock target right", "microswitch", True, ()), 47: ("Cyclops spinner", "other", True, ()),
	48: ("Right ramp entrance", "opto", True, ()), 49: ("Right orbit", "leaf", False, ()),
	50: ("Left Nightcrawler hit", "microswitch", False, ()), 51: ("Right Nightcrawler hit", "microswitch", False, ()),
	52: ("Right ramp exit", "opto", False, ()), 53: ("Center lock 1 bottom", "opto", False, ("ball.position",)),
	54: ("Left inner loop", "leaf", False, ()), 55: ("Left up-kicker", "microswitch", False, ("ball.loaded",)),
	56: ("Right Nightcrawler down", "microswitch", False, ("position.down",)),
}
LE_ONLY_SWITCHES = {12, 34, 35, 50, 51, 56}


def matrix_switch(number: int, le: bool) -> dict[str, object]:
	spec = SWITCHES.get(number)
	used = spec is not None and (le or number not in LE_ONLY_SWITCHES)
	label = spec[0] if used else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	if used:
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, LE_VPX_SOURCE) if le else (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)
	else:
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE)
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)), "normally_closed": False,
		"pulse": bool(spec[2]) if used else False, "availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if used else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance("validated", *sources),
	}
	if used and spec[3]:
		result["roles"] = list(spec[3])
	return result


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, vpx_source: str) -> dict[str, object]:
	if availability != "unused":
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, vpx_source, CORE_SOURCE) if vpx_source != PRO_VPX_SOURCE else (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, CORE_SOURCE)
	else:
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, CORE_SOURCE)
	return {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"), "normally_closed": normally_closed,
		"pulse": False, "availability": availability, "physical": {"switch_type": switch_type},
		"provenance": provenance("validated", *sources),
	}


def inputs(le: bool) -> list[dict[str, object]]:
	vpx_source = LE_VPX_SOURCE if le else PRO_VPX_SOURCE
	items = [matrix_switch(number, le) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left flipper button", "used", "button", False), (83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False), (81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False), (87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Upper-right flipper button", "used", "button", False), (85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "used", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for spec in dedicated:
		items.append(dedicated_switch(*spec, vpx_source))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated", MANUAL_SOURCE, MANUAL_HIRES_SOURCE, CORE_SOURCE)})
	return items


MAIN_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Lower-left eject", "coil", "used"),
	4: ("Magneto magnet", "magnet", "used"), 5: ("Left up-kicker", "coil", "used"), 6: ("Center lock up-posts", "coil", "used"),
	7: ("Center lock latch", "coil", "used"), 8: ("Shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	12: ("Upper-right flipper", "coil", "used"), 13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"), 17: ("Left-side double flasher", "flasher", "used"),
	18: ("Right-side flasher", "flasher", "used"), 19: ("Disc clear double flasher", "flasher", "used"), 20: ("Disc blue double flasher", "flasher", "used"),
	21: ("Wolverine flasher", "flasher", "used"), 22: ("Magneto left/right double flasher", "flasher", "used"),
	23: ("Disc motor power", "relay", "used"), 24: ("Coin meter", "coil", "optional"), 25: ("Pop bumper flasher", "flasher", "used"),
	26: ("Orbit diverter", "coil", "used"), 27: ("Iceman ramp motor", "motor", "used"), 28: ("Backpanel left triple flasher", "flasher", "used"),
	29: ("Backpanel right triple flasher", "flasher", "used"), 30: ("Magneto spotlight flasher", "flasher", "used"),
	31: ("Bottom-arch double flasher", "flasher", "used"), 32: ("Magneto figure flasher", "flasher", "used"),
}
MAIN_CONTROL = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
MAIN_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J8-P11", "J8-P12", "J8-P14", "J8-P15", "J8-P16", "J8-P17", "J8-P18", "J8-P19", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]
AUX_COILS = {
	51: ("Wolverine magnet", "magnet", "Q41", "ORG-BRN"), 52: ("Left Nightcrawler raise", "coil", "Q42", "ORG-RED"),
	53: ("Right Nightcrawler raise", "coil", "Q43", "ORG-BLK"), 54: ("White GI subtract/dim", "gi", "Q44", "ORG-YEL"),
	55: ("Red GI subtract/dim", "gi", "Q45", "ORG-GRN"), 56: ("Blue GI subtract/dim", "gi", "Q46", "ORG-BLU"),
	57: ("Left Nightcrawler latch release", "coil", "Q47", "ORG-VIO"), 58: ("Right Nightcrawler latch release", "coil", "Q48", "ORG-GRY"),
}


def output(address: int, label: str, kind: str, availability: str, status: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	alias_namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(alias_namespace, address, manual_address), "availability": availability, "provenance": provenance(status, *sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def main_wiring(address: int) -> dict[str, object]:
	if address == 8:
		power_wire, power_connection, voltage, voltage_type = "RED-WHT", "J17-P7", 16, "ac"
	elif address in (12, 15, 16):
		power_wire, power_connection, voltage, voltage_type = "GRY-YEL / RED-YEL", "J10-P6/7", 50, "dc"
	elif address == 4:
		power_wire, power_connection, voltage, voltage_type = "VIO-YEL", "J10-P8", 50, "dc"
	elif address <= 16:
		power_wire, power_connection, voltage, voltage_type = "YEL-VIO", "J10-P9/10", 50, "dc"
	elif address in (23, 26, 27):
		power_wire, power_connection, voltage, voltage_type = "BRN", "J7-P1", 20, "dc"
	elif address == 24:
		power_wire, power_connection, voltage, voltage_type = "RED", "J16-P4-8", 5, "dc"
	else:
		power_wire, power_connection, voltage, voltage_type = "ORG", "J6-P10" if address != 32 else "J10-P8", 20, "dc"
	return {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "power_wire": power_wire, "power_connection": power_connection, "nominal_voltage_v": voltage, "voltage_type": voltage_type, "control_wire": MAIN_CONTROL[address - 1], "control_connection": MAIN_CONNECTION[address - 1]}


def le_coils() -> list[dict[str, object]]:
	items = []
	for address, (label, kind, availability) in MAIN_COILS.items():
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, LE_VPX_SOURCE) if availability == "used" else (MANUAL_SOURCE, MANUAL_HIRES_SOURCE)
		items.append(output(address, label, kind, availability, "validated", sources, manual_address=str(address), wiring=main_wiring(address)))
	for address, (label, kind, transistor, wire) in AUX_COILS.items():
		items.append(output(address, label, kind, "used", "validated", (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, LE_VPX_SOURCE, CORE_SOURCE), manual_address=transistor, wiring={"board": "520-5325-00 eight-transistor auxiliary driver board", "driver_transistor": transistor, "power_wire": "YEL-VIO", "nominal_voltage_v": 50, "voltage_type": "dc", "control_wire": wire}))
	items.append(output(33, "ROM flipper-enable state", "virtual", "used", "validated", (LE_VPX_SOURCE, LE_RUNTIME_SOURCE, CORE_SOURCE), physical={"notes": "PinMAME/VPM software output used by the proven table to gate all three flippers; it is not an I/O Power Driver transistor."}, output_id="virtual.flipper-enable"))
	return items


PRO_USED_MAIN = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 24, 25, 26, 27, 28, 29, 31, 32}
PRO_UNUSED_MAIN = {19, 20, 23, 30}
PRO_COIL_OVERRIDES = {
	19: ("Unused Pro output 19 (no Magneto disc clear flasher)", "flasher"),
	20: ("Unused Pro output 20 (no Magneto disc blue flasher)", "flasher"),
	22: ("Magneto feature double flasher", "flasher"),
	23: ("Unused Pro output 23 (no Magneto disc motor)", "relay"),
	27: ("Center-left red feature flasher", "flasher"),
	30: ("Unused Pro output 30", "flasher"),
	31: ("Magneto center red feature flasher", "flasher"),
	32: ("Wolverine magnet", "magnet"),
}
PRO_COIL_PHYSICAL = {
	17: {"location": "Left-side pair at VPX positions x=79.5, y=1336.0 and x=75.5, y=662.0", "notes": "Two table flasher objects are driven together by active-high callback 17."},
	18: {"location": "Right-side pair at VPX positions x=805.5, y=1438.0 and x=917.5, y=594.0", "notes": "Two table flasher objects are driven together by active-high callback 18."},
	21: {"location": "Wolverine area at VPX position x=309.5, y=962.0", "notes": "Active-high flasher callback 21."},
	22: {"location": "Magneto area at VPX position x=503.5, y=288.0", "notes": "Active-high Magneto flasher callback 22."},
	25: {"location": "Pop-bumper area at VPX position x=199.5, y=810.0", "notes": "Active-high pop-bumper flasher callback 25."},
	27: {"location": "Center-left red feature at VPX position x=379.5, y=502.0", "notes": "The authenticated Pro table proves this is a flasher; the LE manual's output-27 Iceman motor label does not apply."},
	28: {"location": "Left backpanel group at VPX positions x=133.5, y=88.0, x=241.5, y=90.0, and x=455.5, y=90.0", "notes": "Three table flasher objects are driven together by active-high callback 28."},
	29: {"location": "Right backpanel group at VPX positions x=843.5, y=94.0 and x=639.5, y=90.0", "notes": "The proven table contains two physical objects driven together by active-high callback 29."},
	31: {"location": "Magneto center red feature at VPX position x=527.5, y=472.0", "notes": "The authenticated Pro table proves this is a flasher; the LE manual's bottom-arch label does not apply."},
	32: {"location": "Under the Wolverine bash-toy area", "notes": "The table's cvpmMagnet binds public solenoid 32 to the Wolverine playfield magnet with GrabCenter disabled."},
}


def pro_coils() -> list[dict[str, object]]:
	items = []
	for address, (manual_label, manual_kind, _) in MAIN_COILS.items():
		label, kind = PRO_COIL_OVERRIDES.get(address, (manual_label, manual_kind))
		availability = "used" if address in PRO_USED_MAIN else "unused"
		if address == 8:
			availability = "optional"
		elif address == 24:
			availability = "optional"
		sources = (PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, PRODUCT_SOURCE, MANUAL_SOURCE, MANUAL_HIRES_SOURCE)
		physical = PRO_COIL_PHYSICAL.get(address)
		items.append(output(address, label, kind, availability, "validated", sources, manual_address=str(address), physical=physical, wiring=main_wiring(address)))
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", "validated", (CORE_SOURCE,), physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	return items


LAMPS = {
	17: "Omega Red", 18: "Sentinels", 19: "Brotherhood", 20: "Rogue", 21: "Iceman", 22: "Wolverine", 23: "Xavier", 24: "Storm",
	25: "Phoenix", 26: "Cyclops", 27: "Beast", 28: "Sabretooth", 29: "Shadow King", 30: "Hellfire Club", 31: "Juggernaut", 32: "Shoot Again",
	33: "Left Special", 34: "Left return lane", 35: "Left two-bank bottom", 36: "Left two-bank top", 37: "Wolverine", 38: "Wolverine red",
	39: "Start button", 41: "Bottom pop bumper", 42: "Right pop bumper", 43: "Left pop bumper", 45: "Dark Phoenix", 46: "Extra Ball",
	47: "Danger Room", 48: "Villain", 49: "Left inner loop green", 50: "Rogue", 51: "Left inner loop red", 52: "Gambit", 53: "Beast",
	54: "Left orbit red", 55: "Left ramp red", 56: "Storm", 57: "Up-kicker red", 58: "Xavier", 59: "Left eject top", 60: "Light Lock left",
	65: "Magneto green", 66: "Magneto", 67: "Magneto red", 68: "Right return lane left", 69: "Right return lane right", 70: "Right Special",
	71: "Right two-bank bottom", 72: "Right two-bank top", 73: "Iceman", 74: "Right ramp red", 75: "Right inner loop red", 76: "Cyclops",
	77: "Light Lock right", 78: "Right orbit red", 79: "Phoenix", 80: "Right orbit green",
}


def le_lamps() -> list[dict[str, object]]:
	items = []
	for address in range(1, 81):
		label = LAMPS.get(address, f"Unused lamp {address}")
		availability = "used" if address in LAMPS else "unused"
		sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, LE_VPX_SOURCE) if availability == "used" else (MANUAL_SOURCE, MANUAL_HIRES_SOURCE)
		items.append(output(address, label, "lamp", availability, "validated", sources, "pinmame.output.lamp", str(address), wiring={"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id=f"lamp.{slug(label)}-{address}"))
	items.append(output(0, "General illumination master", "gi", "used", "validated", (MANUAL_SOURCE, LE_VPX_SOURCE, LE_RUNTIME_SOURCE), "pinmame.output.gi", "GI-0", output_id="gi.master"))
	return items


PRO_LAMPS = {
	3: "Shoot Again", 4: "Left Special", 5: "Left return lane", 6: "Blackbird launch left", 7: "Blackbird launch right", 8: "Right Special",
	9: "Left two-bank bottom", 10: "Left two-bank top", 11: "Left Nightcrawler feature insert", 12: "Dark Phoenix", 13: "Extra Ball",
	14: "Danger Room", 15: "Villain", 16: "Gambit", 17: "Beast", 18: "Far-left upper lane red arrow", 19: "Storm",
	20: "Left ramp red arrow", 21: "Upper-left orbit red arrow", 22: "Rogue", 23: "Left Lock", 24: "Upper-center lane red arrow", 25: "Xavier",
	28: "Left Light Lock", 29: "Right Light Lock", 30: "Wolverine feature insert", 31: "Wolverine red arrow", 33: "Magneto feature insert",
	34: "Center Lock", 35: "Magneto red arrow", 36: "Cyclops red arrow", 37: "Cyclops", 38: "Right Nightcrawler feature insert",
	43: "Iceman red arrow", 44: "Iceman", 45: "Phoenix red arrow", 46: "Phoenix", 47: "Right Lock",
	48: "Magneto completion medallion left", 49: "Magneto completion medallion right",
	50: "Iceman character ring", 51: "Wolverine character ring", 52: "Xavier character ring", 53: "Storm character ring",
	54: "Phoenix character ring", 55: "Cyclops character ring", 56: "Beast character ring", 57: "Rogue character ring",
	60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper",
	65: "Sabretooth", 66: "Shadow King", 67: "Hellfire Club", 68: "Juggernaut", 69: "Brotherhood", 70: "Sentinels", 71: "Omega Red",
}
PRO_LAMP_POSITIONS = {
	3: (410.4, 1835.4), 4: (40.6, 1465.1), 5: (112.5, 1405.3), 6: (691.3, 1376.2), 7: (757.0, 1358.6), 8: (826.6, 1454.1),
	9: (144.7, 1232.4), 10: (158.4, 1169.5), 11: (418.2, 672.6), 12: (300.8, 1117.5), 13: (306.3, 1166.7), 14: (310.8, 1214.5),
	15: (315.5, 1262.6), 16: (188.9, 810.1), 17: (163.1, 671.9), 18: (138.2, 599.0), 19: (248.1, 556.3), 20: (206.0, 496.8),
	21: (235.4, 391.2), 22: (289.1, 446.3), 23: (334.8, 495.0), 24: (373.8, 379.9), 25: (393.7, 472.9), 28: (444.5, 590.5),
	29: (573.6, 590.5), 30: (420.6, 1161.2), 31: (443.1, 1234.2), 33: (507.9, 547.5), 34: (506.6, 621.7), 35: (506.6, 695.5),
	36: (647.9, 444.8), 37: (625.5, 522.5), 38: (687.8, 735.6), 43: (775.2, 486.8), 44: (746.5, 562.0), 45: (866.0, 557.3),
	46: (840.8, 630.2), 47: (814.3, 703.9), 48: (742.9, 1059.2), 49: (742.9, 1130.5), 50: (305.6, 1481.2), 51: (331.6, 1406.7),
	52: (406.1, 1373.7), 53: (480.6, 1404.2), 54: (509.1, 1480.4), 55: (481.6, 1545.2), 56: (405.6, 1579.7), 57: (337.6, 1555.2),
	60: (92.2, 769.0), 61: (307.8, 829.1), 62: (149.2, 949.1), 65: (269.5, 1637.9), 66: (313.8, 1680.5), 67: (361.0, 1718.7),
	68: (408.6, 1755.6), 69: (452.6, 1716.2), 70: (498.3, 1677.4), 71: (540.7, 1636.2),
}
PRO_SCRIPT_LAMPS = set(PRO_LAMPS)


def pro_lamps() -> list[dict[str, object]]:
	items = []
	for address in range(1, 81):
		if address in PRO_LAMPS:
			label = PRO_LAMPS[address]
			x, y = PRO_LAMP_POSITIONS[address]
			physical = {"location": f"Playfield VPX position x={x:.1f}, y={y:.1f}", "notes": "Active-high standard-lamp callback; identity and placement follow the authenticated working Pro table and its playfield artwork."}
			items.append(output(address, label, "lamp", "used", "validated", (PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "pinmame.output.lamp", str(address), physical, {"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, f"lamp.{slug(label)}-{address}"))
		else:
			items.append(output(address, f"Unused Pro lamp channel {address}", "lamp", "unused", "validated", (PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "pinmame.output.lamp", str(address), wiring={"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id=f"lamp.unused-{address}"))
	items.append(output(0, "General illumination master", "gi", "used", "validated", (PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "pinmame.output.gi", "GI-0", physical={"notes": "The proven Pro table treats GI callback 0 as active-high master illumination."}, output_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], status: str = "validated", positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(status, *sources)}
	if positions:
		result["positions"] = positions
	return result


def le_mechanisms() -> list[dict[str, object]]:
	sources = (MANUAL_SOURCE, MANUAL_HIRES_SOURCE, LE_VPX_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "other", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right", "switch.trough-jam"], "Four physical balls occupy switches 18-21 from left to right. Output 1 advances the rightmost ball to the shooter lane through jam opto 22; the proven table initializes 18-21 closed.", sources),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches a ball held at shooter-lane switch 23. Preserve a manual plunger input as well because the shooter assembly supports player plunges.", sources),
		mechanism("mechanism.lower-left-eject", "Power Scoop lower-left eject", "kicker", ["device.lower-left-eject"], ["switch.lower-left-eject"], "Switch 4 stays active while a ball is held. Output 3 ejects it back onto the playfield; the working VPX geometry uses a near-horizontal 354-degree kick with high speed.", sources),
		mechanism("mechanism.left-up-kicker", "Left vertical up-kicker", "kicker", ["device.left-up-kicker"], ["switch.left-up-kicker"], "Switch 55 holds the ball below the playfield. Output 5 kicks vertically and diverts the ball onto the left ramp.", sources),
		mechanism("mechanism.center-lock", "Magneto four-ball center lock", "other", ["device.center-lock-up-posts", "device.center-lock-latch"], ["switch.center-lock-1-bottom", "switch.center-lock-2", "switch.center-lock-3", "switch.center-lock-4-top"], "A four-position vertical lock is retained by two linked up-posts. Output 6 raises both posts for release; output 7 actuates the latch and the proven script lowers both posts after a 500 ms delay. Sensors 53, 38, 39, and 40 report bottom-to-top occupancy.", sources),
		mechanism("mechanism.orbit-diverter", "Magneto orbit diverter", "diverter", ["device.orbit-diverter"], ["switch.right-orbit"], "Output 26 rotates the orbit diverter between the normal orbit and the route into the rear of the Magneto lock.", sources),
		mechanism("mechanism.magneto-disc", "Magneto magnetic spinning disc", "rotary", ["device.magneto-magnet", "device.disc-motor-power"], [], "PWM output 4 controls the playfield magnet beneath the disc. Output 23 powers the disc motor; no index or home switch exists. The proven VPX implementation uses a turntable speed of 100 with a spin-down value of 10 and keeps the magnet independent of motor state.", sources),
		mechanism("mechanism.wolverine", "Wolverine bash toy and magnet", "toy", ["device.wolverine-magnet"], ["switch.wolverine-bash-target"], "The Wolverine is a passive wobbling bash toy sensed by switch 36. Public auxiliary output 51 (physical Q41) controls the nearby magnet; the proven table does not center-grab the ball, which preserves the real toy's deflecting behavior.", sources),
		mechanism("mechanism.iceman-ramp", "Iceman motorized Ice Slide ramp", "motorized", ["device.iceman-ramp-motor"], ["switch.iceman-home", "switch.iceman-away"], "Output 27 moves the ramp toward the opposite endpoint. Home switch 34 closes at the 14-degree endpoint; away switch 35 closes at the 60-degree endpoint; both are open in transit. The proven 8 ms simulation advances 0.16 degree per tick, reverses the next travel direction at each endpoint, and carries a ball with the rotating ramp rather than letting it fall through.", sources, positions=[{"id": "position.home", "label": "Home / right-side route", "sensors": ["switch.iceman-home"]}, {"id": "position.away", "label": "Away / left-side route", "sensors": ["switch.iceman-away"]}]),
		mechanism("mechanism.left-nightcrawler", "Left Nightcrawler pop-up", "motorized", ["device.left-nightcrawler-raise", "device.left-nightcrawler-latch-release"], ["switch.left-nightcrawler-hit", "switch.left-nightcrawler-down"], "Output 52 raises the figure and clears down switch 12. The top position is held mechanically without an upper sensor. A ball strike closes switch 50 and shakes the figure; output 57 releases the latch so gravity returns it, closing switch 12 only when fully down.", sources, positions=[{"id": "position.down", "label": "Retracted", "sensors": ["switch.left-nightcrawler-down"]}, {"id": "position.up", "label": "Raised and latched", "sensors": []}]),
		mechanism("mechanism.right-nightcrawler", "Right Nightcrawler pop-up", "motorized", ["device.right-nightcrawler-raise", "device.right-nightcrawler-latch-release"], ["switch.right-nightcrawler-hit", "switch.right-nightcrawler-down"], "Output 53 raises the figure and clears down switch 56. The top position is held mechanically without an upper sensor. A ball strike closes switch 51 and shakes the figure; output 58 releases the latch so gravity returns it, closing switch 56 only when fully down.", sources, positions=[{"id": "position.down", "label": "Retracted", "sensors": ["switch.right-nightcrawler-down"]}, {"id": "position.up", "label": "Raised and latched", "sensors": []}]),
		mechanism("mechanism.color-gi", "Red, blue, and white GI mixing", "other", ["device.white-gi-subtract-dim", "device.red-gi-subtract-dim", "device.blue-gi-subtract-dim"], [], "GI 0 is the master on/off state. Modulated public outputs 54-56 map to physical Q44-Q46 and subtract/dim the white, red, and blue channels respectively: the proven table renders channel intensity as 255 minus the output value while GI 0 is on.", sources),
		mechanism("mechanism.flippers", "Three-flipper assembly", "other", ["device.left-flipper", "device.right-flipper", "device.upper-right-flipper", "virtual.flipper-enable"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke", "switch.upper-right-flipper-button"], "Outputs 15 and 16 drive the lower flippers; output 12 drives the upper-right flipper. Dedicated inputs 84/83 are left button/EOS, 82/81 right button/EOS, and 86 is the upper staged button. Public virtual output 33 is the ROM flipper-enable state used by the proven table to gate all three coils.", sources),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "The three independently switched pops use outputs/switches 9/30 left, 10/31 right, and 11/32 bottom. Output 25 is their shared flasher.", sources),
		mechanism("mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left and right slings use output/switch pairs 13/26 and 14/27.", sources),
		mechanism("mechanism.spinner", "Cyclops spinner", "rotary", [], ["switch.cyclops-spinner"], "Each rotation pulse of the passive Cyclops spinner closes switch 47.", sources),
		mechanism("mechanism.standup-targets", "Seven standup targets", "other", [], ["switch.left-two-bank-bottom-target", "switch.left-two-bank-top-target", "switch.right-two-bank-top-target", "switch.right-two-bank-bottom-target", "switch.light-lock-target-left", "switch.light-lock-target-right", "switch.wolverine-bash-target"], "The left Hellfire pair is switches 1/2, the right Brotherhood pair 7/8, the Light Lock pair 41/42, and Wolverine is switch 36. These are standups/bash targets, not resettable drop targets.", sources),
		mechanism("mechanism.ramps-and-orbits", "Ramps, loops, and lane guides", "other", [], ["switch.left-ramp-exit", "switch.left-ramp-entrance", "switch.left-orbit", "switch.right-ramp-entrance", "switch.right-orbit", "switch.right-ramp-exit", "switch.left-inner-loop"], "Build the two main molded ramps plus the Iceman transfer ramp, the left and right orbits, and the inner loop. Switches 13/11 bracket the left ramp, 48/52 the right ramp, 14/49 the outer orbits, and 54 the inner loop.", sources),
		mechanism("mechanism.optional-shaker", "Optional shaker motor", "motorized", ["device.shaker-motor"], [], "Output 8 is the optional 16 VAC shaker installation and may be absent from a stock machine.", sources),
	]


def pro_mechanisms() -> list[dict[str, object]]:
	sources = (PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, PRODUCT_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "other", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right", "switch.trough-jam"], "The working Pro script models four balls at switches 18-21 with output 1 feeding the shooter lane through jam opto 22.", sources),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches the ball from switch 23.", sources),
		mechanism("mechanism.lower-left-eject", "Power Scoop lower-left eject", "kicker", ["device.lower-left-eject"], ["switch.lower-left-eject"], "Switch 4 holds the ball and output 3 ejects it.", sources),
		mechanism("mechanism.left-up-kicker", "Left vertical up-kicker", "kicker", ["device.left-up-kicker"], ["switch.left-up-kicker"], "Switch 55 holds the ball; output 5 kicks it vertically onto the left ramp.", sources),
		mechanism("mechanism.center-lock", "Magneto four-ball center lock", "other", ["device.center-lock-up-posts", "device.center-lock-latch"], ["switch.center-lock-1-bottom", "switch.center-lock-2", "switch.center-lock-3", "switch.center-lock-4-top"], "The dual up-post lock uses outputs 6/7 and occupancy sensors 53, 38, 39, and 40.", sources),
		mechanism("mechanism.orbit-diverter", "Magneto orbit diverter", "diverter", ["device.orbit-diverter"], ["switch.right-orbit"], "Output 26 sends the orbit shot into the rear of the lock.", sources),
		mechanism("mechanism.magneto-magnet", "Magneto playfield magnet", "other", ["device.magneto-magnet"], [], "PWM output 4 controls the Magneto magnet. The Pro has no spinning disc motor.", sources),
		mechanism("mechanism.wolverine", "Wolverine bash toy and magnet", "toy", ["device.wolverine-magnet"], ["switch.wolverine-bash-target"], "Switch 36 senses the passive wobbling bash toy; the proven Pro table binds output 32 to a nearby playfield magnet with center-grab disabled, so the ball is deflected rather than rigidly centered.", sources),
		mechanism("mechanism.flippers", "Three-flipper assembly", "other", ["device.left-flipper", "device.right-flipper", "device.upper-right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke", "switch.upper-right-flipper-button"], "Physical outputs 15/16 drive the lower pair and output 12 drives the upper-right flipper; dedicated switch 86 is the staged upper button. The legacy table visually couples the upper flipper to output 16 and comments out callback 12, so recreations must retain the physical 12/86 mapping instead of copying that shortcut.", sources),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "The three pop output/switch pairs are 9/30, 10/31, and 11/32.", sources),
		mechanism("mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left and right slings use output/switch pairs 13/26 and 14/27.", sources),
		mechanism("mechanism.spinner", "Cyclops spinner", "rotary", [], ["switch.cyclops-spinner"], "The passive spinner pulses switch 47.", sources),
		mechanism("mechanism.standup-targets", "Seven standup targets", "other", [], ["switch.left-two-bank-bottom-target", "switch.left-two-bank-top-target", "switch.right-two-bank-top-target", "switch.right-two-bank-bottom-target", "switch.light-lock-target-left", "switch.light-lock-target-right", "switch.wolverine-bash-target"], "The seven physical targets are the two Hellfire, two Brotherhood, two Light Lock, and Wolverine bash targets.", sources),
		mechanism("mechanism.ramps-and-orbits", "Two ramps and orbit network", "other", [], ["switch.left-ramp-exit", "switch.left-ramp-entrance", "switch.left-orbit", "switch.right-ramp-entrance", "switch.right-orbit", "switch.right-ramp-exit", "switch.left-inner-loop"], "The Pro has two molded ramps, left/right orbits, and the inner loop; it does not have the Iceman transfer ramp. Lamps 11 and 38 retain Nightcrawler-themed printed feature art but are static inserts, not sensors or moving mechanisms.", sources),
		mechanism("mechanism.optional-shaker", "Optional shaker motor", "motorized", ["device.shaker-motor"], [], "Output 8 is the optional 16 VAC shaker installation and may be absent from a stock machine.", sources),
	]


LE_DRIVER_IDS = {"xmn_102", "xmn_120h", "xmn_121h", "xmn_122h", "xmn_123h", "xmn_124h", "xmn_130h", "xmn_150h", "xmn_151h", "xmn_151hc"}


def driver_records(le: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		if (driver_id in LE_DRIVER_IDS) != le:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		if driver_id.endswith("c"):
			record["variant_notes"] = "Colored-ROM modification only; physical I/O and mechanisms are unchanged."
		elif driver_id == "xmn_102":
			record["variant_notes"] = "Early Limited Edition firmware is explicitly identified as LE by PinMAME despite lacking the later h suffix; it uses the LE playfield."
		else:
			record["variant_notes"] = "Firmware revision within this physical edition; playfield I/O and mechanisms are unchanged."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(le: bool) -> list[dict[str, object]]:
	vpx_source = {"id": LE_VPX_SOURCE if le else PRO_VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/X-Men%20LE%20(Stern%202012)%20VPW%20v1.0.6.vbs" if le else "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/X-Men(ICPjuggla)6-27c.vbs", "revision": VPX_REVISION, "sha256": "6d445e52398640bd35a498553bb0ba32f1b9ce23e2964d0694c18ff2e9225650" if le else "2441d88ab8aef581fcdef3dd5c0b9523a36feb3ce4afb6133811f1f01b381afb", "locator": "X-Men LE (Stern 2012) VPW v1.0.6.vbs: initialization, solenoid callbacks, GI callbacks, Iceman movement, Nightcrawler state machines, Magneto disc, lock, kickers, trough, and switches" if le else "X-Men(ICPjuggla)6-27c.vbs: Pro ROM xmn_151, solenoid callbacks, lamp callback addresses, Wolverine and Magneto magnets, trough, lock, kickers, ramps, and switches", "license": "NOASSERTION", "attribution": "Table authors credited in the script and vpxtable_scripts contributors"}
	result = [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/XMenManual_042214.pdf", "sha256": "0812b91d0950ff8c1b15c5bc17afc827029ca8aaaa0bbb78cc11ea606b629bf8", "locator": "XMenManual_042214.pdf: PDF pages 56-62 and 97-117; official low-resolution manufacturer copy", "license": "NOASSERTION", "attribution": "Stern Pinball", "source_id": "stern", "original_filename": "XMenManual_042214.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"},
		{"id": MANUAL_HIRES_SOURCE, "kind": "manual", "uri": "https://primetimeamusements.com/wp-content/uploads/2015/05/XMenManual_042214.pdf", "sha256": "d793836fefab6c0de53463943e36245c7ed800d5ca86675e3c2b2f46df693643", "locator": "Higher-resolution scan of the same Stern manual; switch table page 56, lamp table page 58, coil table page 60, eight-transistor board page 101, LE LED boards pages 103-104, GI maps pages 109-111", "license": "NOASSERTION", "attribution": "Stern Pinball manual mirrored by PrimeTime Amusements", "original_filename": "XMenManual_042214-high-resolution.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"},
		vpx_source,
		{"id": PRODUCT_SOURCE, "kind": "human_review", "uri": "https://sternpinball.com/game/x-men-pro/", "locator": "Manufacturer Pro and Limited Edition feature inventories, including edition-only Ice Slide, Nightcrawler, spinning disc, and color GI mechanisms", "license": "NOASSERTION", "attribution": "Stern Pinball", "acquired_at": "2026-08-02T00:00:00Z"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c X-Men INITGAME and full driver family; src/wpc/sam_original.c historical ROM identity; public custom outputs 51-58 for the eight-transistor board", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames X-Men driver records", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	]
	if le:
		result.append({"id": LE_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/xmn_151h/harness/boot-start-le.json", "revision": PINMAME_REVISION, "sha256": "72730b25d7cec239eac1d8df6039f0c465e2c729070d49acebec8d22aa5cb61c", "locator": "Exact xmn_151h boot/start scenario with switches 18-21 initialized, four coin pulses, and start; ROM archive SHA-256 cc8069743e6a0f45c3b310c0804230241739b5cf8c51f0481d96810f9edab5be", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"})
	else:
		result.append({"id": PRO_VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "https://vpuniverse.com/files/file/2679-x-men-pro-stern-2012-85vett/", "sha256": "00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8", "locator": "XMen FS (physmod5).vpt from XMen FS (physmod5).zip; archive SHA-256 6f5eae417c894af5947a819448f45616cb2348a1cfdca5cff544e6bdcda439fb; embedded script SHA-256 90cd88f121798f7c91ba738713c2aae99784751637380beb864ee3e2bcde25cb; read-only inventory SHA-256 ff52f1deaee9182f1b6e33785887dab774d15aa6b963f1ca627a835198ce1020; playfield artwork PF A.jpg SHA-256 bc62ed5d55b1c3394beae1c78b1f72544bcdcf3d3008cf51b1cfefea8be01cc1. The embedded xmen_150 script, physical lamp/flasher objects, coordinates, playfield labels, switches, and mechanisms were inspected.", "license": "NOASSERTION", "attribution": "85vett and table authors credited by the archived table", "original_filename": "XMen FS (physmod5).vpt", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"})
	return result


def build_le() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.x-men-limited-edition.2012", "name": "X-Men Limited Edition (Magneto / Wolverine)", "manufacturer": "Stern", "year": 2012, "kind": "physical_pinball", "model_number": "I-00D2", "ipdb_id": 5823},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(True), "inputs": inputs(True), "outputs": le_coils() + le_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, LE_VPX_SOURCE, LE_RUNTIME_SOURCE)}],
		"mechanisms": le_mechanisms(), "relationships": [], "sources": sources(True),
		"knowledge": {"path": "knowledge/stern/x-men-limited-edition-2012.md", "status": "complete"}, "conflicts": [],
	}


def build_pro() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.x-men-pro.2012", "name": "X-Men Pro", "manufacturer": "Stern", "year": 2012, "kind": "physical_pinball", "model_number": "I-00D1", "ipdb_id": 5822},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(False), "inputs": inputs(False), "outputs": pro_coils() + pro_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)}],
		"mechanisms": pro_mechanisms(), "relationships": [], "sources": sources(False),
		"knowledge": {"path": "knowledge/stern/x-men-pro-2012.md", "status": "complete"},
		"conflicts": [],
	}


LE_KNOWLEDGE = """# X-Men Limited Edition (Stern, 2012)

Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers both artwork packages of the Limited Edition hardware: Magneto LE (IPDB 5823, 250 units) and Wolverine LE (IPDB 5824, 300 units), Stern model I-00D2. They share the same playfield and I/O. Drivers `xmn_*h`/`xmn_*hc` are LE firmware, and early `xmn_102` is also explicitly identified as Limited Edition by PinMAME even though it predates the `h` naming convention. Non-`h` Pro revisions have materially different hardware and are not compatible with this definition.

The known-working `X-Men LE (Stern 2012) VPW v1.0.6.vbs` is ground truth for public PinMAME addresses, callbacks, initial states, and mechanism causality. The Stern manual governs physical inventory, diagnostic numbering, wiring, and assemblies. Pinned PinMAME source governs the SAM transport, 128x32 DMD, driver identities, and the eight-transistor board's public custom-output range.

## Controller topology and initial state

The SAM switch matrix is 1-64; dedicated cabinet switches use PinMAME public values 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough closes switches 18-21 at initialization. General illumination is public GI 0. Physical main-driver Q1-Q32 are public solenoids 1-32. PinMAME public 51-58 map in order to physical auxiliary Q41-Q48. Public solenoid 33 is a software flipper-enable event used by the proven VPX table and is not a cabinet transistor.

## Edition-only devices

LE-only switches are 12 left Nightcrawler down, 34/35 Iceman endpoints, 50/51 Nightcrawler hit sensors, and 56 right Nightcrawler down. LE-only public auxiliary outputs are 51 Wolverine magnet, 52/53 Nightcrawler raise coils, 54/55/56 white/red/blue GI dim channels, and 57/58 Nightcrawler latch releases. The LE also uses main output 23 for the Magneto disc motor and output 27 for the Iceman ramp motor. Do not transfer these devices to a Pro recreation.

## Magneto disc and lock

The Magneto disc motor and magnet are independent. Output 23 spins the disc without a position sensor; PWM output 4 controls its magnet. Behind it, the orbit diverter on output 26 routes balls into a four-level vertical lock. Lock sensors are 53 at the bottom, then 38, 39, and 40 at the top. Outputs 6 and 7 operate the dual linked up-post and latch mechanism; the proven model raises both posts and schedules their return after 500 ms.

## Nightcrawler pop-ups

Each Nightcrawler has separate raise and latch-release coils. Output 52 raises the left figure and output 53 the right; the down switches 12/56 clear immediately. The figures mechanically latch at full height without upper sensors. Switches 50/51 register ball strikes. Outputs 57/58 release the latches, after which the figures fall and close their down switches only at the bottom. A faithful simulation must model the un-sensed upper latch and should move a resting ball out of the travel envelope before raising, as the proven table does.

## Iceman Ice Slide

Output 27 drives a two-position motorized ramp that transfers the ball from the right side toward the left. The known endpoints are 14 degrees home and 60 degrees away. Switch 34 is home, switch 35 away, and both remain open during travel. The ROM energizes the motor toward the next endpoint; the working implementation remembers direction and reverses it after each limit. Move any ball already on the ramp with the rotating surface.

## Wolverine, ejects, and standard playfield

The Wolverine assembly combines a passive bash toy on switch 36 with a separate playfield magnet on public output 51/physical Q41. The toy should wobble from impact rather than behave like a drop target. The Power Scoop at switch 4 ejects through output 3. The vertical up-kicker at switch 55 fires with output 5 and diverts the ball onto the left ramp. Output 2 auto-launches from shooter switch 23. The upper-right flipper is output 12 with dedicated button 86; lower flippers are 15/16 with buttons 84/82 and normally-closed EOS contacts 83/81.

## Lamps and GI

The standard lamp matrix is exactly 1-80; 1-16, 40, 44, and 61-64 are explicitly unused in the service chart. The remaining addresses and names are enumerated in the JSON. GI 0 is the master supply. Public modulated outputs 54-56 are active subtraction/dimming channels: the proven table computes each color as `255 - output` while GI is on. This polarity matters when recreating red, blue, white, and mixed illumination.

## Other physical inventory

The machine has four balls, three flippers, three pops, two slings, a passive Cyclops spinner, two main molded ramps, the Iceman transfer ramp, seven standup/bash targets, the Magneto diverter/lock, two playfield magnets, two eject devices, and an optional shaker. The left pair 1/2 are Hellfire targets, right pair 7/8 Brotherhood, 41/42 Light Lock, and 36 Wolverine. None of these target banks is a resettable drop-target bank.
"""


PRO_KNOWLEDGE = """# X-Men Pro (Stern, 2012)

Coverage: **author-ready - physical inventory, public PinMAME bindings, lamp semantics, mechanisms, and edition differences validated**

## Identity and evidence precedence

This definition covers non-LE drivers `xmn_100`, `xmn_104`, `xmn_105`, `xmn_130`, `xmn_150`, `xmn_151`, and `xmn_151c`, using Stern model I-00D1 and IPDB 5822. Those revisions use one physical Pro playfield; `xmn_151c` only changes ROM colorization. The authenticated `XMen FS (physmod5).vpt` table running `xmen_150` is ground truth for controller callbacks, object placement, playfield labels, mechanisms, and active-high rendering behavior. The independent known-working Pro script corroborates public addresses. The combined Stern manual supplies common SAM service topology and shared assemblies but its edition-specific lamp and low-current output charts describe the LE, so those labels are deliberately not transferred to the Pro. Pinned PinMAME source governs driver identity, SAM serialization, and the native 128x32 four-bit DMD.

## Controller topology and initial state

The SAM switch matrix is public 1-64; dedicated cabinet inputs occupy 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough initializes switches 18-21 closed, and switch 22 is its jam opto. Standard lamps are public 1-80 and GI is public 0. Main outputs are public 1-32. The Pro does not install the LE auxiliary eight-transistor board or its public 51-58 output range.

## Lamps and physical placement

All public lamp addresses 1-80 are explicit in the JSON. The authenticated table consumes exactly 3-25, 28-31, 33-38, 43-57, 60-62, and 65-71; every other address is explicitly unused. Each used lamp was correlated with an extracted VPX coordinate during curation, but those coordinates have not yet been normalized and promoted into this definition. Semantic labels come from the table's playfield art. Descriptive location labels are retained for otherwise unlabeled red route arrows and the two Magneto completion medallions so an author can identify them without inventing rule terminology. Lamps 11 and 38 carry left/right Nightcrawler feature artwork but are ordinary static inserts on the Pro, not moving toys. Lamp callbacks and GI 0 are active-high in the proven scripts.

## Coils, flashers, and the upper flipper exception

Outputs 1-18 are the common trough, launcher, eject, magnets, lock, optional shaker, pops, three physical flippers, slings, and left/right flashers. Outputs 19, 20, 23, and 30 are unused on the Pro; in particular there is no spinning Magneto disc motor. Output 21 flashes Wolverine, 22 Magneto, 25 the pop area, 26 moves the orbit diverter, 27 is a center-left red flasher, 28/29 drive left/right backpanel groups, 31 is the Magneto center red flasher, and 32 is the Wolverine playfield magnet. The JSON records every observed flasher object's coordinates, including multi-object groups.

The physical upper-right flipper is output 12 with staged dedicated button 86/D15. The legacy table comments out callback 12 and rotates its upper flipper object together with lower-right output 16. That is a table shortcut, not machine wiring; authors must implement the physical 12/86 channel pair. Lower flippers are outputs 15/16 with buttons 84/82 and normally-closed EOS inputs 83/81.

## Magneto lock, Wolverine, and ball devices

PWM output 4 controls the Magneto playfield magnet. Output 26 routes the orbit shot into the four-position vertical Magneto lock. Occupancy switches are 53 at the bottom, followed by 38, 39, and 40 at the top; outputs 6 and 7 operate the linked up-post and latch mechanism. Wolverine is a passive wobbling bash toy on switch 36 plus a separate output-32 playfield magnet. The proven table disables center-grab so the magnet deflects the ball rather than pinning it rigidly.

The Power Scoop holds a ball at switch 4 and ejects with output 3. The left vertical up-kicker holds at switch 55 and output 5 sends the ball onto the left ramp. Output 2 auto-launches from shooter switch 23 while the cabinet also retains a manual plunger. Pops use output/switch pairs 9/30, 10/31, and 11/32; slings use 13/26 and 14/27. The passive Cyclops spinner pulses switch 47.

## Important Pro differences

The Pro omits the LE motorized Iceman Ice Slide, both latched Nightcrawler pop-up mechanisms, the spinning Magneto disc, red/blue/white subtractive color-GI channels, and auxiliary driver board. It retains two printed Nightcrawler lamp features and ordinary Iceman inserts, which must not be mistaken for the missing LE mechanisms. The Wolverine magnet moves from LE public 51/physical Q41 to Pro main output 32. Output 27 is a flasher instead of the LE Iceman motor, and output 31 is a different red feature flasher. Never apply the combined manual's LE lamp table or these LE output labels to a Pro recreation.

## Author construction checklist

- Build the four-ball trough, shooter/manual plunger, auto launcher, Power Scoop eject, left VUK, four-level Magneto lock and diverter, two playfield magnets, passive Wolverine bash toy, three flippers, three pops, two slings, Cyclops spinner, seven standup/bash targets, two molded ramps, inner loop, and both outer orbits.
- Bind every public input and output from the JSON, including explicit unused lamp and coil channels, GI 0, the 128x32 DMD, and the upper-right physical flipper exception.
- Recover and normalize the 58 standard-lamp and flasher-group placements from the authenticated table and pinned playfield art before authoring; these coordinates are not yet stored in the definition. Do not invent LE hardware where the Pro art retains only a themed insert.
- Treat working-table kick force, angle, animation, capture, and magnet values as proven authoring baselines, while preserving controller causality and physical channel assignments.
"""


def runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": ["stern.x-men-limited-edition.2012"], "driver_ids": ["xmn_151h"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": "xmn_151h", "command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game xmn_151h --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>", "rom_archive_sha256": "cc8069743e6a0f45c3b310c0804230241739b5cf8c51f0481d96810f9edab5be", "raw_runs": [{"name": "boot-start", "sha256": "72730b25d7cec239eac1d8df6039f0c465e2c729070d49acebec8d22aa5cb61c", "self_test_pulses": 0}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80], "solenoid_addresses_seen": [27, 30, 33], "gi_addresses_seen": [0]}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/xmn_151h/harness", "sha256": "72730b25d7cec239eac1d8df6039f0c465e2c729070d49acebec8d22aa5cb61c", "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def write(path: Path, value: dict[str, object]) -> None:
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json(path, value)


def main() -> None:
	write(ROOT / "machines/partial/stern/x-men-limited-edition-2012.json", build_le())
	write(ROOT / "machines/partial/stern/x-men-pro-2012.json", build_pro())
	write(ROOT / "evidence/runtime/sam/x-men-limited-edition-boot-start.json", runtime_evidence())
	write_text(ROOT / "knowledge/stern/x-men-limited-edition-2012.md", fail_closed_spatial_knowledge("stern.x-men-limited-edition.2012", LE_KNOWLEDGE))
	write_text(ROOT / "knowledge/stern/x-men-pro-2012.md", fail_closed_spatial_knowledge("stern.x-men-pro.2012", PRO_KNOWLEDGE))
	stale = ROOT / "machines/partial/stern/x-men-le-2012.json"
	if stale.exists():
		stale.unlink()


if __name__ == "__main__":
	main()
