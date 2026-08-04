"""Build reviewed Star Trek Pro and Premium/Limited Edition definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("st_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
PREMIUM_MANUAL = "manual.star-trek-premium-le"
PRO_MANUAL = "manual.star-trek-pro"
VPX_SOURCE = "vpx.star-trek-le-1.10"
PRO_VPX_SOURCE = "vpx.star-trek-pro-fss"
PRO_VPX_TABLE_SOURCE = "vpx-table.star-trek-pro-fss"
PRO_RUNTIME_SOURCE = "runtime.star-trek-pro.boot-start"


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

SWITCHES = {
	1: ("(BEAM) ME UP target", "microswitch", True), 2: ("BEAM (ME) UP target", "microswitch", True),
	4: ("BEAM ME (UP) target", "microswitch", True), 7: ("Right 3-bank top", "microswitch", True),
	8: ("Right 3-bank center", "microswitch", True), 9: ("Right 3-bank bottom", "microswitch", True),
	10: ("Left eject", "microswitch", False), 11: ("Center drop target", "microswitch", False),
	12: ("Spinner", "other", True), 13: ("Warp ramp entrance", "opto", True),
	14: ("Left ramp entrance", "opto", True), 15: ("Tournament start", "button", False),
	16: ("Start", "button", False), 18: ("Trough #4 left", "microswitch", False),
	19: ("Trough #3", "microswitch", False), 20: ("Trough #2", "microswitch", False),
	21: ("Trough #1", "microswitch", False), 22: ("Trough jam", "opto", False),
	23: ("Shooter lane", "microswitch", False), 24: ("(T)REK target", "microswitch", True),
	25: ("T(R)EK target", "microswitch", True), 26: ("Left slingshot", "leaf", True),
	27: ("Right slingshot", "leaf", True), 28: ("TR(E)K target", "microswitch", True),
	29: ("TRE(K) target", "microswitch", True), 30: ("Left pop bumper", "leaf", True),
	31: ("Right pop bumper", "leaf", True), 32: ("Bottom pop bumper", "leaf", True),
	33: ("Center lock bottom", "opto", False), 34: ("Center lock top", "opto", False),
	35: ("Left ramp exit", "opto", True), 36: ("Warp ramp exit", "opto", True),
	37: ("Right ramp entrance", "opto", True), 38: ("Right ramp exit", "opto", True),
	39: ("Center 3-bank top", "microswitch", True), 40: ("Center 3-bank center", "microswitch", True),
	41: ("Center 3-bank bottom", "microswitch", True), 42: ("Left 2-bank top", "microswitch", True),
	43: ("Left 2-bank bottom", "microswitch", True), 44: ("Right drain", "leaf", False),
	45: ("Red target 1", "microswitch", True), 46: ("Red target 2", "microswitch", True),
	47: ("Red target 3", "microswitch", True), 48: ("Red target 4", "microswitch", True),
	49: ("Red target 5", "microswitch", True), 50: ("Red target 6", "microswitch", True),
	51: ("Right orbit", "leaf", True), 52: ("Left orbit", "leaf", True),
	53: ("Vengeance crash opto", "opto", False),
}
PRO_SWITCHES = {number: spec for number, spec in SWITCHES.items() if number != 53}


def matrix_switch(number: int, manual: str, validated: bool, switches: dict[int, tuple[str, str, bool]] = SWITCHES, vpx_source: str = VPX_SOURCE) -> dict[str, object]:
	spec = switches.get(number)
	used = spec is not None
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	sources = (manual, vpx_source) if validated and used else (manual,)
	device_id = f"switch.{slug(label)}"
	if number in (1, 2, 4):
		device_id = f"{device_id}-{number}"
	return {
		"id": device_id, "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": False, "pulse": bool(spec[2]) if spec else False,
		"availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if spec else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance("validated" if validated else "observed", *sources),
	}


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, manual: str, validated: bool, normally_closed: bool = False, vpx_source: str = VPX_SOURCE) -> dict[str, object]:
	sources = (manual, vpx_source, CORE_SOURCE) if validated and availability != "unused" else (manual, CORE_SOURCE)
	return {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": normally_closed, "pulse": False, "availability": availability,
		"physical": {"switch_type": switch_type},
		"provenance": provenance("validated" if validated else "observed", *sources),
	}


def inputs(manual: str, validated: bool, switches: dict[int, tuple[str, str, bool]] = SWITCHES, vpx_source: str = VPX_SOURCE) -> list[dict[str, object]]:
	items = [matrix_switch(number, manual, validated, switches, vpx_source) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Unused dedicated switch D5", "unused", "unknown", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Fire button", "used", "button", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left flipper button", "used", "button", False), (83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False), (81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False), (87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Upper-right flipper button", "used", "button", False), (85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "used", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for device, manual_number, label, availability, switch_type, normally_closed in dedicated:
		items.append(dedicated_switch(device, manual_number, label, availability, switch_type, manual, validated, normally_closed, vpx_source))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated" if validated else "observed", manual, CORE_SOURCE)})
	return items


MAIN_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Center lock magnet", "magnet", "used"),
	4: ("Center drop target up", "coil", "used"), 5: ("Center drop target down", "coil", "used"), 6: ("Left eject", "coil", "used"),
	7: ("Vengeance super-speed kickback", "coil", "used"), 8: ("Shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	12: ("Upper-right flipper", "coil", "used"), 13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"),
	17: ("Asteroid left flasher", "flasher", "used"), 18: ("Asteroid right flasher", "flasher", "used"),
	19: ("Left ramp top flasher", "flasher", "used"), 20: ("Right ramp top flasher", "flasher", "used"),
	21: ("Kickback flasher", "flasher", "used"), 22: ("Laser projector motor", "motor", "used"),
	23: ("Left ramp flasher", "flasher", "used"), 24: ("Coin meter", "coil", "optional"),
	25: ("Pop bumper flasher", "flasher", "used"), 26: ("Warp ramp entrance flasher", "flasher", "used"),
	27: ("Center three-bank flasher", "flasher", "used"), 28: ("Right ramp flasher", "flasher", "used"),
	29: ("Left loop flasher", "flasher", "used"), 30: ("Upper-right flipper flasher", "flasher", "used"),
	31: ("Vengeance ship flasher", "flasher", "used"), 32: ("Bottom spot left flasher", "flasher", "used"),
}

AUX_COILS = {
	51: ("Left orbit control gate", "coil", "used", "Q51"), 52: ("Right orbit control gate", "coil", "used", "Q52"),
	53: ("Vengeance ship actuator", "motor", "used", "Q53"), 54: ("Bottom drain kickback", "coil", "used", "Q54"),
	55: ("Rotating VUK", "coil", "used", "Q55"), 56: ("Vengeance ship latch", "coil", "used", "Q56"),
	57: ("Unused auxiliary output 57", "coil", "unused", "compatibility-gap"), 58: ("Unused auxiliary output 58", "coil", "unused", "compatibility-gap"),
	59: ("Bottom spot right flasher", "flasher", "used", "Q41"), 60: ("Backbox flasher 1", "flasher", "used", "Q42"),
	61: ("Backbox flasher 2", "flasher", "used", "Q43"), 62: ("Backbox flasher 3", "flasher", "used", "Q44"),
	63: ("Backbox flasher 4", "flasher", "used", "Q45"), 64: ("Backbox flasher 5", "flasher", "used", "Q46"),
	65: ("Unused auxiliary output 65", "coil", "unused", "compatibility-gap"), 66: ("Unused auxiliary output 66", "coil", "unused", "compatibility-gap"),
}

MAIN_CONTROL = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
AUX_CONTROL = {51: "YEL-BRN", 52: "YEL-GRY", 53: "YEL-ORG", 54: "YEL-BLK", 55: "YEL-GRN", 56: "YEL-BLU", 59: "ORG-BRN", 60: "ORG-RED", 61: "ORG-BLK", 62: "ORG-YEL", 63: "ORG-GRN", 64: "ORG-BLU"}


def output(address: int, label: str, kind: str, availability: str, status: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	result = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases("pinmame.lamp" if group.endswith("lamp") else "pinmame.solenoid", address, manual_address), "availability": availability, "provenance": provenance(status, *sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def coils(manual: str, validated: bool, include_auxiliary: bool = True, vpx_source: str = VPX_SOURCE) -> list[dict[str, object]]:
	status = "validated" if validated else "candidate"
	items = []
	for address in range(1, 33):
		label, kind, availability = MAIN_COILS[address]
		power = "VIO-YEL" if address == 3 else ("YEL-VIO" if address <= 16 and address != 8 else "ORG")
		voltage = 50 if address <= 16 and address != 8 else (16 if address == 8 else 20)
		wiring = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "power_wire": power, "control_wire": MAIN_CONTROL[address - 1], "nominal_voltage_v": voltage, "voltage_type": "dc"}
		sources = (manual, vpx_source) if validated and availability == "used" else (manual,)
		items.append(output(address, label, kind, availability, status, sources, manual_address=str(address), wiring=wiring))
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", status, (CORE_SOURCE,), physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	if not include_auxiliary:
		return items
	for address in range(51, 67):
		label, kind, availability, transistor = AUX_COILS[address]
		wiring = {"board": "12-transistor auxiliary driver board", "driver_transistor": transistor}
		if address in AUX_CONTROL:
			wiring.update({"power_wire": "YEL-VIO" if address <= 56 else "ORG", "control_wire": AUX_CONTROL[address], "nominal_voltage_v": 50 if address <= 56 else 20, "voltage_type": "dc"})
		sources = (manual, vpx_source, CORE_SOURCE) if validated and availability != "unused" else (manual, CORE_SOURCE)
		manual_address = f"Q{address}" if address <= 56 else (f"Q{address - 18}" if address <= 64 else None)
		items.append(output(address, label, kind, availability, status, sources, manual_address=manual_address, wiring=wiring))
	return items


PHYSICAL_LAMPS = {
	1: "Left ramp emblem", 2: "Red target 2", 3: "Left ramp Enterprise arrow", 4: "Red target 3", 5: "Center lane emblem",
	6: "Center lane Enterprise arrow", 7: "Red target 4", 8: "Black hole arrow", 9: "Right orbit emblem", 10: "Right orbit Enterprise arrow",
	11: "Red target 6", 12: "Right ramp emblem", 13: "Right ramp Enterprise arrow", 14: "Red target 5", 15: "Special",
	16: "Away team", 17: "Left eject lock", 18: "Mission start", 19: "Left 2-bank top", 20: "Left orbit emblem",
	21: "Red target 1", 22: "Left orbit Enterprise arrow", 23: "Left 2-bank bottom", 24: "Left eject emblem", 25: "Left eject Enterprise arrow",
	26: "Kickback", 27: "(T)REK", 28: "T(R)EK", 29: "Center 3-bank bottom", 30: "Center 3-bank center",
	31: "Center 3-bank top", 32: "Center lane lock", 33: "Extra ball", 34: "Shoot again", 35: "Captain's Chair",
	36: "Save the Enterprise", 37: "Nero", 38: "Destroy the Drill", 39: "Space Jump", 40: "Prime Directive",
	41: "Klingon Battle", 42: "Status 1 bottom", 43: "Status 2", 44: "Status 3", 45: "Status 4", 46: "Status 5",
	47: "Status 6", 48: "Status 7", 49: "Status 8 top", 50: "Warp ramp red", 51: "Enterprise",
	52: "Warp ramp emblem", 53: "(BEAM) ME UP", 54: "BEAM (ME) UP", 55: "BEAM ME (UP)", 56: "Vengeance saucer",
	57: "Vengeance nacelles", 58: "Right 3-bank top", 59: "Right 3-bank center", 60: "Right 3-bank bottom", 61: "TR(E)K",
	62: "TRE(K)", 63: "Left apron", 64: "Right apron", 65: "Start button", 66: "Fire button red",
	67: "Fire button green", 68: "Fire button blue", 69: "Tournament start button",
	70: "Warp chaser 1", 71: "Warp chaser 2", 72: "Warp chaser 3", 73: "Warp chaser 4", 74: "Warp chaser 5",
	75: "Warp chaser 6", 76: "Warp chaser 7", 77: "Warp chaser 8", 78: "Cabinet Enterprise",
	**{number: f"Cabinet phaser {number - 78}" for number in range(79, 101)},
}

RGB_PUBLIC = {
	1: (84, 85, 86), 2: (81, 87, 88), 3: (83, 82, 89), 4: (92, 91, 90), 5: (93, 94, 95), 6: (96, 97, 98),
	7: (99, 100, 101), 8: (102, 103, 104), 9: (113, 114, 115), 10: (116, 117, 118), 11: (119, 120, 121),
	12: (122, 123, 124), 13: (125, 126, 127), 14: (128, 129, 130), 15: (131, 133, 132), 16: (134, 136, 135),
	17: (146, 147, 148), 18: (149, 150, 151), 19: (152, 153, 154), 20: (155, 156, 157), 21: (158, 159, 160),
	22: (161, 162, 163), 23: (164, 165, 166), 24: (167, 168, 169), 25: (170, 171, 172), 26: (179, 177, 178),
	27: (182, 180, 181), 28: (185, 183, 184), 29: (186, 187, 188), 30: (189, 190, 191), 31: (192, 193, 194),
	32: (195, 197, 196), 33: (198, 200, 199), 34: (214, 215, 216), 35: (211, 217, 218), 36: (213, 212, 219),
	37: (222, 221, 220), 38: (223, 224, 225), 39: (226, 227, 228), 40: (229, 230, 231), 41: (232, 233, 234),
	42: (235, 236, 237), 43: (238, 239, 240), 44: (241, 242, 243), 45: (244, 245, 246), 46: (247, 248, 249),
	47: (250, 251, 252), 48: (253, 254, 255), 49: (256, 257, 258), 52: (278, 279, 280), 53: (281, 283, 282),
	54: (284, 286, 285), 55: (287, 289, 288), 58: (308, 309, 310), 59: (311, 312, 313), 60: (314, 315, 316),
	61: (317, 319, 318), 62: (320, 322, 321), 63: (300, 302, 301), 64: (303, 305, 304),
}
SINGLE_PUBLIC = {50: 276, 51: 277, 56: 290, 57: 291, 65: 80, 66: 78, 67: 77, 68: 76, 69: 79, 70: 295, 71: 292, 72: 293, 73: 294, 74: 299, 75: 296, 76: 297, 77: 298, 78: 75, **{number: number - 28 for number in range(79, 101)}}


def lamps(manual: str, validated: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "candidate"
	by_public: dict[int, tuple[str, int, str]] = {}
	for physical_number, channels in RGB_PUBLIC.items():
		for color, address in zip(("red", "green", "blue"), channels):
			by_public[address] = (f"{PHYSICAL_LAMPS[physical_number]} {color}", physical_number, color)
	for physical_number, address in SINGLE_PUBLIC.items():
		by_public[address] = (PHYSICAL_LAMPS[physical_number], physical_number, "single-color")
	items = []
	for address in list(range(1, 145)) + list(range(146, 210)) + list(range(211, 275)) + list(range(276, 340)):
		entry = by_public.get(address)
		if entry:
			label, physical_number, color = entry
			physical = {"location": "Playfield, apron, cabinet, or backbox as shown on the lamp-location and cabinet-wiring diagrams", "notes": f"Physical diagnostic lamp {physical_number}; {color} channel"}
			sources = (manual, VPX_SOURCE, CORE_SOURCE) if validated else (manual, CORE_SOURCE)
			items.append(output(address, label, "lamp", "used", status, sources, "pinmame.output.lamp", str(physical_number), physical, output_id=f"lamp.physical-{physical_number}-{slug(color)}"))
		else:
			board = 0 if address <= 80 else 5 + ((address - 81) // 65)
			label = f"Unused lamp channel {address}" if board == 0 else f"Unused node-board {board} channel {address}"
			items.append(output(address, label, "lamp", "unused", status, (manual, CORE_SOURCE), "pinmame.output.lamp", output_id=f"lamp.unused-{address}"))
	items.append(output(0, "General illumination", "gi", "used", status, (manual, VPX_SOURCE) if validated else (manual,), "pinmame.output.gi", "GI-0", output_id="gi.general-illumination"))
	return items


PRO_LAMPS = {
	3: "Fire button", 4: "(T)REK", 5: "T(R)EK", 7: "TR(E)K", 8: "TRE(K)",
	9: "Prime Directive", 10: "Space Jump", 11: "Save the Enterprise", 12: "Captain's Chair",
	13: "Shoot Again", 14: "Destroy the Drill", 15: "Klingon Battle", 16: "Nero",
	17: "Status 1 bottom", 18: "Status 2", 19: "Status 3", 20: "Status 4", 21: "Status 5",
	22: "Status 6", 23: "Status 7", 24: "Status 8 top", 32: "Left orbit Enterprise arrow",
	40: "Left 2-bank bottom", 48: "Left 2-bank top", 49: "Left ramp Enterprise arrow",
	50: "Red target 1", 51: "Mission start", 52: "Left eject lock", 53: "Center 3-bank bottom",
	54: "Center 3-bank center", 55: "Center 3-bank top", 56: "Left eject Enterprise arrow",
	57: "Red target 2", 59: "Red target 3", 60: "Red target 4", 61: "Black hole arrow",
	62: "Center lane Enterprise arrow", 63: "Center lane lock", 64: "Extra ball",
	65: "(BEAM) ME UP", 66: "BEAM (ME) UP", 67: "BEAM ME (UP)", 68: "Red target 5",
	69: "Red target 6", 70: "Right ramp Enterprise arrow", 71: "Right orbit Enterprise arrow",
	72: "Away team", 73: "Special", 74: "Right 3-bank top", 75: "Right 3-bank center",
	76: "Right 3-bank bottom", 80: "Right-side blue playfield spotlight",
}
PRO_RGB_CHANNELS = {
	25: ("Left orbit emblem", "red", 200.0, 1502.0), 33: ("Left orbit emblem", "green", 200.0, 1502.0), 41: ("Left orbit emblem", "blue", 200.0, 1502.0),
	26: ("Left ramp emblem", "red", 261.7, 1348.0), 34: ("Left ramp emblem", "green", 261.7, 1348.0), 42: ("Left ramp emblem", "blue", 261.7, 1348.0),
	29: ("Left eject emblem", "red", 363.5, 844.0), 37: ("Left eject emblem", "green", 363.5, 844.0), 45: ("Left eject emblem", "blue", 363.5, 844.0),
	30: ("Center lane emblem", "red", 493.2, 836.0), 38: ("Center lane emblem", "green", 493.2, 836.0), 46: ("Center lane emblem", "blue", 493.2, 836.0),
	28: ("Right ramp emblem", "red", 650.2, 1032.0), 36: ("Right ramp emblem", "green", 650.2, 1032.0), 44: ("Right ramp emblem", "blue", 650.2, 1032.0),
	27: ("Right orbit emblem", "red", 781.5, 1054.0), 35: ("Right orbit emblem", "green", 781.5, 1054.0), 43: ("Right orbit emblem", "blue", 781.5, 1054.0),
}


def pro_lamps() -> list[dict[str, object]]:
	items = []
	for address in range(1, 81):
		rgb = PRO_RGB_CHANNELS.get(address)
		if rgb:
			name, color, x, y = rgb
			label = f"{name} {color}"
			items.append(output(address, label, "rgb_lamp", "used", "validated", (PRO_MANUAL, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "pinmame.output.lamp", str(address), {"location": f"Playfield VPX position x={x:.1f}, y={y:.1f}", "notes": f"{color} channel of the physical {name} tri-color insert"}, {"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, f"lamp.{slug(name)}-{color}"))
		elif address in PRO_LAMPS:
			label = PRO_LAMPS[address]
			location = "Right side of the lower playfield at VPX position x=875.25, y=1342.875" if address == 80 else f"{label} playfield or cabinet insert"
			notes = "Blue spotlight with a wide playfield halo; the table names the physical objects l80/f80." if address == 80 else "Semantic label and physical presence agree between the proven table and playfield artwork."
			output_id = f"lamp.{slug(label)}-{address}" if address in (65, 66, 67) else f"lamp.{slug(label)}"
			items.append(output(address, label, "lamp", "used", "validated", (PRO_MANUAL, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "pinmame.output.lamp", str(address), {"location": location, "notes": notes}, {"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id))
		else:
			items.append(output(address, f"Unused lamp channel {address}", "lamp", "unused", "validated", (PRO_MANUAL, PRO_VPX_TABLE_SOURCE), "pinmame.output.lamp", str(address), wiring={"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id=f"lamp.unused-{address}"))
	items.append(output(0, "General illumination", "gi", "used", "validated", (PRO_MANUAL, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE), "pinmame.output.gi", "GI-0", output_id="gi.general-illumination"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, manual: str, validated: bool, positions: list[dict[str, object]] | None = None, vpx_source: str = VPX_SOURCE, extra_sources: tuple[str, ...] = ()) -> dict[str, object]:
	source_refs = (manual, vpx_source, *extra_sources) if validated else (manual, CORE_SOURCE)
	result = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance("validated" if validated else "observed", *source_refs)}
	if positions:
		result["positions"] = positions
	return result


def premium_mechanisms() -> list[dict[str, object]]:
	m = PREMIUM_MANUAL
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1", "switch.trough-jam"], "The physical trough uses position switches 18-21 and jam opto 22. The known-working script initializes four balls on switches 19-22, leaving leftmost switch 18 clear, and output 1 ejects from the right end.", m, True),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches a ball resting at shooter-lane switch 23. The working table uses power 52 with random variation 3.", m, True),
		mechanism("mechanism.left-eject", "Left eject and rotating VUK", "kicker", ["device.left-eject", "device.rotating-vuk"], ["switch.left-eject"], "Switch 10 stays active with a captured ball. Output 55 rotates the two-way VUK/deflector; output 6 then ejects along the selected path. The working table's standard path uses direction 85 degrees, force 38, and Z 100.", m, True, [{"id": "position.normal", "label": "Normal route", "sensors": []}, {"id": "position.rotated", "label": "Rotated route", "sensors": []}]),
		mechanism("mechanism.center-drop-target", "Center memory drop target", "drop_target_bank", ["device.center-drop-target-up", "device.center-drop-target-down"], ["switch.center-drop-target"], "Output 4 raises and output 5 lowers the single memory target. Switch 11 is active while down; a ball held behind it is released when the target rises.", m, True, [{"id": "position.up", "label": "Up", "sensors": []}, {"id": "position.down", "label": "Down", "sensors": ["switch.center-drop-target"]}]),
		mechanism("mechanism.center-lock", "Center magnet lock", "toy", ["device.center-lock-magnet"], ["switch.center-lock-bottom", "switch.center-lock-top"], "Output 3 is a PWM-capable magnet behind the memory target. The working table uses a centered capture field of radius 135 and permits multiple-ball capture; switches 33 and 34 track balls in the center lock lane.", m, True),
		mechanism("mechanism.vengeance", "Animated Vengeance battleship", "motorized", ["device.vengeance-ship-actuator", "device.vengeance-ship-latch", "device.vengeance-super-speed-kickback"], ["switch.vengeance-crash-opto"], "PWM output 53 drives the ship down and into a shake/crash phase; output 56 releases or restores its latch, and switch 53 reports the crashed/latched state. Output 7 fires the captured ball back at super speed. The working animation advances at 100 Hz through down steps 2-50, shake steps 101-154, and return steps 201-250.", m, True, [{"id": "position.raised", "label": "Raised", "sensors": []}, {"id": "position.crashed", "label": "Crashed and latched", "sensors": ["switch.vengeance-crash-opto"]}]),
		mechanism("mechanism.orbit-gates", "Left and right orbit control gates", "gate", ["device.left-orbit-control-gate", "device.right-orbit-control-gate"], ["switch.left-orbit", "switch.right-orbit"], "Outputs 51 and 52 independently control the left and right orbit gates; switches 52 and 51 respectively report ball travel through the adjacent orbits.", m, True),
		mechanism("mechanism.kickback", "Bottom drain kickback", "kicker", ["device.bottom-drain-kickback"], ["switch.right-drain"], "Output 54 returns a ball entering right-drain switch 44. Do not confuse it with output 7, which is the Vengeance super-speed kickback.", m, True),
		mechanism("mechanism.flippers", "Three flippers", "other", ["device.left-flipper", "device.right-flipper", "device.upper-right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke", "switch.upper-right-flipper-button"], "Lower outputs 15/16 use buttons 84/82 and normally-closed EOS inputs 83/81. Upper-right output 12 uses dedicated button 86.", m, True),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Switches 30, 31, and 32 pulse outputs 9, 10, and 11 respectively.", m, True),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26/27 pulse outputs 13/14.", m, True),
		mechanism("mechanism.laser", "Laser projector", "motorized", ["device.laser-projector-motor"], [], "Output 22 runs the playfield laser-projector motor. It has no controller-facing position switch in the manual or working table.", m, True),
		mechanism("mechanism.spinner", "Spinner", "other", [], ["switch.spinner"], "Each rotation pulses switch 12.", m, True),
	]


def pro_mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[dict[str, object]] | None = None, runtime: bool = False) -> dict[str, object]:
	extra_sources = (PRO_RUNTIME_SOURCE,) if runtime else ()
	return mechanism(mechanism_id, label, kind, actuators, sensors, behavior, PRO_MANUAL, True, positions, PRO_VPX_SOURCE, extra_sources)


def pro_mechanisms() -> list[dict[str, object]]:
	return [
		pro_mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1", "switch.trough-jam"], "The physical trough uses switches 18-21 from left to right plus jam opto 22. The proven Pro table creates four balls on 18-21. Output 1 ejects the rightmost ball and the script briefly drives switch 22 as the ball enters the shooter path.", runtime=True),
		pro_mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches a ball held at shooter-lane switch 23. The proven Pro table uses direction 40 degrees, base power 40, random variation 0.3, and a 0.6 second full-plunge time."),
		pro_mechanism("mechanism.left-eject", "Left eject", "kicker", ["device.left-eject"], ["switch.left-eject"], "Switch 10 remains active while a ball is captured. Output 6 ejects it at 184 degrees with force 22, Z velocity 55, and angle/force variation 2 in the proven table."),
		pro_mechanism("mechanism.center-drop-target", "Center memory drop target", "drop_target_bank", ["device.center-drop-target-up", "device.center-drop-target-down"], ["switch.center-drop-target"], "Ball impact drops the target and activates switch 11. Output 4 raises it and output 5 lowers it; raising it also releases a ball held behind the target.", [{"id": "position.up", "label": "Up", "sensors": []}, {"id": "position.down", "label": "Down", "sensors": ["switch.center-drop-target"]}]),
		pro_mechanism("mechanism.center-lock", "Center magnet lock", "toy", ["device.center-lock-magnet"], ["switch.center-lock-bottom", "switch.center-lock-top"], "Output 3 controls the center lock magnet. The proven table models a radius-55 grab field with centered capture and uses optos 33/34 for the bottom/top lock positions."),
		pro_mechanism("mechanism.vengeance", "Passive Vengeance bash toy and kickback", "toy", ["device.vengeance-super-speed-kickback"], ["switch.center-drop-target"], "The Pro ship is a passive bash/shake toy above the center target, not the Premium/LE motorized dive assembly. A hit on switch 11 drops the target and shakes the ship. While output 7 is enabled, the Vengeance kicker returns a captured ball at 175 degrees and force 40. Do not add the Premium actuator, latch, crash opto, orbit gates, rotating VUK, or bottom-drain kickback."),
		pro_mechanism("mechanism.flippers", "Three flippers", "other", ["device.left-flipper", "device.right-flipper", "device.upper-right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke", "switch.upper-right-flipper-button"], "Physical outputs 15/16 drive the lower left/right flippers from dedicated buttons 84/82 and normally-closed EOS contacts 83/81. Physical output 12 and public D15 switch 86 operate the upper-right flipper. The proven legacy VPX table instead couples the visual upper flipper to output 16 and writes public switch 90; that is a table simplification, not the service wiring."),
		pro_mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Switches 30/31/32 pulse outputs 9/10/11 for the left, right, and bottom pop bumpers."),
		pro_mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26/27 pulse outputs 13/14."),
		pro_mechanism("mechanism.spinner", "Spinner", "other", [], ["switch.spinner"], "Each full spinner rotation pulses switch 12; there is no controller-facing actuator."),
		pro_mechanism("mechanism.beam-target-bank", "BEAM ME UP three-target bank", "other", [], ["switch.beam-me-up-target-1", "switch.beam-me-up-target-2", "switch.beam-me-up-target-4"], "The three independent standups pulse switches 1, 2, and 4 and correspond to the three BEAM ME UP insert words at lamps 65-67."),
		pro_mechanism("mechanism.trek-target-bank", "TREK four-target bank", "other", [], ["switch.t-rek-target", "switch.t-r-ek-target", "switch.tr-e-k-target", "switch.tre-k-target"], "The four independent standups pulse switches 24, 25, 28, and 29 and correspond to lamps 4, 5, 7, and 8."),
		pro_mechanism("mechanism.right-target-bank", "Right three-target bank", "other", [], ["switch.right-3-bank-top", "switch.right-3-bank-center", "switch.right-3-bank-bottom"], "The top, center, and bottom targets pulse switches 7, 8, and 9; matching inserts are lamps 74, 75, and 76."),
		pro_mechanism("mechanism.center-target-bank", "Center three-target bank", "other", [], ["switch.center-3-bank-top", "switch.center-3-bank-center", "switch.center-3-bank-bottom"], "The top, center, and bottom targets pulse switches 39, 40, and 41. Their physical inserts are lamps 55, 54, and 53 respectively; output 27 is the bank flasher."),
		pro_mechanism("mechanism.left-target-bank", "Left two-target bank", "other", [], ["switch.left-2-bank-top", "switch.left-2-bank-bottom"], "The top and bottom targets pulse switches 42 and 43; their inserts are lamps 48 and 40."),
		pro_mechanism("mechanism.red-targets", "Six red standup targets", "other", [], [f"switch.red-target-{number}" for number in range(1, 7)], "Six independent red standups pulse switches 45-50 and correspond in order to lamps 50, 57, 59, 60, 68, and 69."),
		pro_mechanism("mechanism.ramps-and-orbits", "Ramps and orbits", "other", [], ["switch.warp-ramp-entrance", "switch.warp-ramp-exit", "switch.left-ramp-entrance", "switch.left-ramp-exit", "switch.right-ramp-entrance", "switch.right-ramp-exit", "switch.left-orbit", "switch.right-orbit"], "Warp-ramp optos are 13/36, left-ramp optos 14/35, and right-ramp optos 37/38. Left and right orbit switches are 52/51. Outputs 19/20 flash the ramp tops and outputs 23/28/29 flash the left ramp, right ramp, and left loop."),
		pro_mechanism("mechanism.laser", "Laser projector", "motorized", ["device.laser-projector-motor"], [], "Output 22 drives the unsensed playfield laser-projector motor."),
		pro_mechanism("mechanism.optional-shaker", "Optional shaker", "motorized", ["device.shaker-motor"], [], "Output 8 drives the optional cabinet shaker; an author may omit the physical accessory while retaining the controller binding."),
	]


def driver_records(premium: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		is_premium = bool(re.fullmatch(r"st_\d+h(?:c)?", driver_id))
		if is_premium != premium:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Colored-ROM modification only; physical I/O and mechanisms are unchanged." if driver_id.endswith("c") else "Firmware revision within this physical edition; playfield I/O and mechanisms are unchanged."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(manual: str, premium: bool) -> list[dict[str, object]]:
	manual_record = {"id": manual, "kind": "manual", "uri": "https://sternpinball.com/support/game-code/", "sha256": "ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d" if premium else "23cb9e6683d7b357ada48678a8e157a8b64102ea012821c350a3f033fae66b28", "locator": "Star-Trek-LE-Manual.pdf, PDF pages 68-77, 114-119, and 153-155" if premium else "Star-Trek-Pro-Manual.pdf: shared switch matrix PDF pages 66-67; main coil chart page 114; GI/wiring page 116; LE-only auxiliary board page 117 excluded; opto boards pages 151-154, including LE-only switch 53 exclusion", "license": "NOASSERTION", "attribution": "Stern Pinball", "source_id": "stern", "original_filename": "Star-Trek-LE-Manual.pdf" if premium else "Star-Trek-Pro-Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"}
	result = [manual_record]
	if premium:
		result.append({"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/special_audiopan_and_audiofade_patched/Star%20Trek%20LE%20(Stern%202013)%20v1.10.vbs", "revision": VPX_REVISION, "sha256": "3337481b28144a67f1df3c3650355be91699104930d8b3cc8503e14225a9d4ff", "locator": "Star Trek LE (Stern 2013) v1.10.vbs lines 438-470, 673-1080, 1490-1590, and 1900-2120", "license": "NOASSERTION", "attribution": "Table authors credited in the script and vpxtable_scripts contributors"})
	else:
		result.extend([
			{"id": PRO_VPX_SOURCE, "kind": "vpx_script", "uri": "local-evidence://vpx-script/star-trek-pro-fss", "sha256": "abc5dbb6ead12f16886143a50cfd2534c9baf855b070924dd7d82e404b4d69bf", "locator": "Star Trek Pro (Stern 2013)-[D&N][FSS][DMD].vbs extracted from the archived table; game st_161, initialization, switch handlers, solenoid callbacks, lamp timer, and mechanism behavior", "license": "NOASSERTION", "attribution": "Table authors credited by the archived table", "original_filename": "Star Trek Pro (Stern 2013)-[D&N][FSS][DMD].vbs"},
			{"id": PRO_VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "https://archive.org/details/Visual_Pinball_2020-06-20", "sha256": "2976e3313a6fa1ee6f26709d515661b81ade8f01894a847b907a5e608e5bb9e7", "locator": "Visual Pinball [VPXx] PinMame Tables [Full Single Screen]/Star Trek Pro (Stern 2013)-[D_N][FSS][DMD].zip; archive SHA-256 eaa577d4514b4945f6d98195a161c3de59d67c61f2b4d75e4c99169c9b6c1a34; physical lamp objects and playfield artwork inspected read-only", "license": "NOASSERTION", "attribution": "Table authors credited by the archived table", "original_filename": "Star Trek Pro (Stern 2013)-[D&N][FSS][DMD].vpx"},
			{"id": PRO_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/st_161c/harness/boot-start-pro.json", "revision": PINMAME_REVISION, "sha256": "a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7", "locator": "Exact st_161c boot/start scenario with switches 18-21 initialized, four coin pulses, and start; ROM archive SHA-256 f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		])
	result.extend([
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Star Trek INITGAME and driver family; src/wpc/core.c SAM switch serialization; vpinball/scripts/sam.vbs dedicated-switch constants. The four-node and auxiliary output topology is LE-only and is excluded from the Pro physical definition." if not premium else "src/wpc/sam.c Star Trek INITGAME, four-node-board topology, custom-solenoid routing, and fast-flip configuration", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	])
	return result


def build_premium() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.star-trek-premium-limited-edition.2013", "name": "Star Trek Premium / Limited Edition", "manufacturer": "Stern", "year": 2013, "ipdb_id": 6046},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(True), "inputs": inputs(PREMIUM_MANUAL, True), "outputs": coils(PREMIUM_MANUAL, True) + lamps(PREMIUM_MANUAL, True),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, VPX_SOURCE)}],
		"mechanisms": premium_mechanisms(), "relationships": [], "sources": sources(PREMIUM_MANUAL, True),
		"knowledge": {"path": "knowledge/stern/star-trek-premium-limited-edition-2013.md", "status": "complete"}, "conflicts": [],
	}


def build_pro() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.star-trek-pro.2013", "name": "Star Trek Pro", "manufacturer": "Stern", "year": 2013, "ipdb_id": 6046},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(False), "inputs": inputs(PRO_MANUAL, True, PRO_SWITCHES, PRO_VPX_SOURCE), "outputs": coils(PRO_MANUAL, True, False, PRO_VPX_SOURCE) + pro_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE)}],
		"mechanisms": pro_mechanisms(), "relationships": [], "sources": sources(PRO_MANUAL, False),
		"knowledge": {"path": "knowledge/stern/star-trek-pro-2013.md", "status": "complete"}, "conflicts": [],
	}


PREMIUM_KNOWLEDGE = """# Star Trek Premium / Limited Edition (Stern, 2013)

Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `st_*h` and `st_*hc` drivers. Those revisions share the Premium/LE playfield; `c` only changes ROM display colorization. Non-`h` drivers are the different Pro machine and have their own definition. The known-working `Star Trek LE (Stern 2013) v1.10.vbs` is ground truth for controller bindings, callbacks, initial state, mechanism causality, and active behavior. The official Stern manual governs physical inventory, wiring, diagnostic numbering, and assemblies. Pinned PinMAME source governs the SAM transport, display, custom-solenoid serialization, node-board topology, and driver identity.

## Controller topology

The four node boards expose public lamp ranges 81-144, 146-209, 211-274, and 276-339. Public addresses 145, 210, and 275 are deliberate compatibility gaps, not lamps. The JSON enumerates every addressable lamp channel and marks unused channels explicitly. Main solenoids are 1-32. The auxiliary board exposes Q51-Q56 as public 51-56 and physical Q41-Q46 as public 59-64; 57-58 and 65-66 are explicit unused holes.

## Switches and initial ball state

All matrix positions 1-64, dedicated D1-D24, and DIP inputs are enumerated. The physical four-ball trough has left-to-right sensors 18-21 plus jam opto 22. The working script initializes four balls on 19-22, leaving 18 clear. Shooter lane is 23. Fire is public 71/D7; the upper-right flipper button is public 86/D15. Lower buttons are 84 left and 82 right, with normally-closed EOS contacts 83 left and 81 right.

## Lamps

Manual physical lamp numbers are diagnostic identities, while the JSON binding is the PinMAME `ChangedLamps` callback address observed in the working script. Physical lamps 1-49 are RGB node-board devices; their public channels are not their printed numbers. For example physical lamp 1 maps red/green/blue to public 84/85/86. Physical 50 and 51 map to 276/277. The RGB warp emblem 52 maps to 278/279/280. Start, tournament, and fire-button channels occupy public 76-80. Warp chasers map to 292-299 in script order. Cabinet Enterprise is public 75; cabinet phaser diagnostics 79-100 map to public 51-72. Always bind to public addresses and retain the printed number only as `manual.address`.

## Center memory target and magnet lock

The single center target uses switch 11, output 4 up, and output 5 down. The script activates switch 11 while down and releases a captured ball when raising it. The lock magnet is PWM output 3; the proven table uses a radius-135 centered field and allows multiple-ball capture. Lower and upper lock optos are 33 and 34.

## Left eject and rotating VUK

Switch 10 remains active while the left eject holds a ball. Output 55 rotates its two-way VUK/deflector and output 6 ejects along the selected path; no position switch exists. The known normal path uses 85 degrees, force 38, and Z 100. Build the rotating routing geometry even though both operations share the same scoop opening.

## Vengeance battleship

The ship is a latched animated mechanism, not a decorative flasher. PWM output 53 drives its dive and shake, output 56 controls the latch/return, and switch 53 represents the crashed/latched state. Output 7 then returns the ball at super speed. The working 100 Hz animation uses down steps 2-50, shake steps 101-154, and return steps 201-250; use these as a proven timing and motion baseline, then align geometry to the physical ship.

## Gates, kickback, laser, and standard devices

Outputs 51/52 control the left/right orbit gates. Output 54 is the bottom right-drain kickback paired with switch 44; output 7 is instead the Vengeance kicker. Output 22 drives the laser projector without a position sensor. The machine has three flippers, three pops, two slings, a spinner at switch 12, three ramps, four balls, a six-target red bank, a center three-bank, a left two-bank, and the four TREK targets. Output 8 is the optional shaker and output 24 the optional coin meter.

## Recreation checklist

- Construct all physical inputs and outputs, including explicit unused controller addresses, four node boards, auxiliary board, GI group, and native 128x32 DMD.
- Initialize four trough balls exactly as the working script does: 19-22 active and 18 clear.
- Preserve PWM for the center magnet and Vengeance actuator; do not reduce either to a simple pulse.
- Model the memory target, multi-ball magnet hold, rotating VUK route, Vengeance latch/crash/return sequence, orbit gates, bottom kickback, laser motor, upper flipper, and all sensed ball paths.
- Use public JSON callback bindings for node LEDs and auxiliary outputs; use manual numbers only in service/diagnostic UI.
- Treat VPX force, angle, animation, and capture values as proven authoring baselines and refine only the physical geometry without changing controller causality.

## Sources

- `manual.star-trek-premium-le`: official Stern `Star-Trek-LE-Manual.pdf`, SHA-256 `ca2007093bb4c1425d728a46e548d3af5a3d8fdd844c41dab48cd4ddbacb985d`; I/O and wiring tables on PDF pages 68-77, 114-119, and 153-155.
- `vpx.star-trek-le-1.10`: known-working script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `3337481b28144a67f1df3c3650355be91699104930d8b3cc8503e14225a9d4ff`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, four node boards, custom outputs, display, and driver configuration.
"""

PRO_KNOWLEDGE = """# Star Trek Pro (Stern, 2013)

Coverage: **author-ready - physical inventory, public PinMAME bindings, lamp semantics, mechanisms, and edition differences validated**

## Identity and evidence precedence

This definition covers all non-`h` Star Trek drivers: `st_120`, `st_130`, `st_140`, `st_150`, `st_160`, `st_161`, `st_161c`, `st_162`, and `st_162c`. PinMAME declares them as clones of an `h` firmware root for software lineage, while this separate definition describes the physically different Pro playfield they run. The extracted working Pro table runs `st_161` and is ground truth for playfield controller causality, ball state, device behavior, and lamp-object bindings. The official Pro manual governs the physical inventory, service wiring, and diagnostic numbering. Pinned PinMAME and `sam.vbs` govern public address serialization and the native 128x32 four-bit DMD.

## Controller topology and edition boundary

The Pro uses main solenoid outputs 1-32, the ordinary lamp matrix at public addresses 1-80, aggregate GI 0, matrix switches 1-64, dedicated switches D1-D24, and eight board DIP switches. It does not have the Premium/LE 12-transistor auxiliary board, four RGB node boards, motorized Vengeance dive/latch, switch 53 crash opto, output 51/52 orbit gates, output 53 ship actuator, output 54 drain kickback, output 55 rotating VUK, or output 56 ship latch. Manual PDF pages 68-70 describe Premium/LE RGB lamps and page 117 explicitly identifies the auxiliary board as LE-only; neither is part of this Pro definition.

## Switch inventory and ball state

The four-ball trough occupies switches 18-21 from left to right and jam opto 22 is downstream. The proven table creates four balls on 18-21; output 1 ejects the ball at switch 21 and briefly drives switch 22. Shooter lane is 23 and output 2 is the auto launcher. Switches 33/34 are bottom/top center-lock optos. Ramp optos are warp entrance/exit 13/36, left entrance/exit 14/35, and right entrance/exit 37/38. Orbits are right 51 and left 52. Pops are left/right/bottom 30/31/32, center bank top/center/bottom 39/40/41, left bank top/bottom 42/43, and the six red targets are 45-50. Switch 53 is unused on Pro.

The dedicated controls use public PinMAME addresses rather than the manual's D labels: fire is 71/D7; lower-left button/EOS are 84/D9 and 83/D10; lower-right are 82/D11 and 81/D12; upper-right button is 86/D15. EOS contacts 83 and 81 are normally closed. Cabinet tilt/service inputs use PinMAME's negative and zero public values as recorded in the JSON.

## Lamp matrix

All 80 public lamp callbacks are explicit. Physical unused channels are 1, 2, 6, 31, 39, 47, 58, and 77-79. Lamps 25-30, 33-38, and 41-46 are the red, green, and blue channels for six physical emblems: left orbit, left ramp, right orbit, right ramp, left eject, and center lane. Exact VPX playfield coordinates were observed during curation but have not yet been normalized and promoted into the definition. The remaining inserts are named from the working table and playfield artwork, including the four TREK letters at 4/5/7/8, status ladder 17-24, six red-target inserts at 50/57/59/60/68/69, six Enterprise arrows, the banks, missions, locks, and awards. Address 80 is the right-side blue playfield spotlight represented by table objects `l80`/`f80`. Script-only visual aliases 119, 120, 129, and 131 are driven from solenoids and are not physical/public lamp addresses, so they are intentionally excluded.

## Center target, lock, and Vengeance

The single center memory target reports switch 11; output 4 raises it and output 5 lowers it. A direct hit drops it, shakes the passive Vengeance toy, and can release a held ball when it rises. Output 3 controls the center magnet; the proven table uses a radius-55 centered grab field and optos 33/34 track the lock path. The Pro Vengeance is a bash toy with output 7 as its super-speed ball return. When enabled, the table kicks at 175 degrees and force 40. Do not reproduce the Premium/LE motor, latch, crash sensor, or dive state machine on this edition.

## Ball devices and standard mechanisms

Left eject switch 10 remains active while occupied; output 6 ejects at 184 degrees, force 22, Z 55, with variation 2 in the proven table. Auto-launch output 2 uses direction 40 degrees, power 40, random variation 0.3, and a 0.6-second full-plunge time. The spinner pulses switch 12. Outputs 9-11 drive the three pops, 13/14 the slings, 15/16 the lower flippers, and 12 the upper-right flipper. Output 22 drives the unsensed laser projector. Outputs 17-21, 23, and 25-32 are named flashers; output 8 is the optional shaker and output 24 the optional coin meter.

The complete target inventory is three BEAM ME UP standups at 1/2/4, four TREK standups at 24/25/28/29, the right three-bank at 7-9, center three-bank at 39-41, left two-bank at 42/43, and six red standups at 45-50. The ramp/orbit sensor pairings and all corresponding insert/arrow addresses are encoded in the JSON mechanisms and outputs.

## Resolved upper-right flipper discrepancy

The legacy Pro table writes public switch 90 and visually couples the upper-right flipper to lower-right output 16. The service manual's dedicated-input table, coil chart, and PinMAME `sam.vbs` agree that the physical machine instead uses public switch 86/D15 and output 12. This definition therefore uses 86/12 and preserves the table discrepancy here as a portability warning. The rest of the table remains the proven behavioral source; this narrow exception is resolved by concordant physical and controller documentation rather than guessed.

## Recreation checklist

- Create four trough balls on switches 18-21, keep jam opto 22 clear until ejection, and bind shooter lane 23.
- Implement all main outputs 1-32, standard lamps 1-80, GI 0, the native 128x32 DMD, every matrix/dedicated input, and optional shaker/coin-meter hardware.
- Build the center memory target, center magnet and two lock optos, passive Vengeance bash/kickback, left eject, auto launcher, laser, three physical flippers, pops, slings, spinner, every target bank, and all ramp/orbit paths.
- Do not add Premium/LE auxiliary outputs, node-board lamps, switch 53, rotating VUK, controlled orbit gates, bottom-drain kickback, or motorized Vengeance hardware.
- Use the proven table's angle, force, timing, capture, and state-transition values as authoring baselines while using the manual for physical placement and wiring.
- Bind the upper-right flipper to physical public switch 86 and output 12; treat the table's 90/16 coupling only as a documented legacy-table simplification.

## Sources

- `manual.star-trek-pro`: official Stern `Star-Trek-Pro-Manual.pdf`, SHA-256 `23cb9e6683d7b357ada48678a8e157a8b64102ea012821c350a3f033fae66b28`; switch matrix on PDF pages 66-67, coil chart 114, GI/wiring 116, LE-only auxiliary declaration 117, and opto boards 151-154.
- `vpx.star-trek-pro-fss`: extracted working `Star Trek Pro (Stern 2013)-[D&N][FSS][DMD].vbs`, SHA-256 `abc5dbb6ead12f16886143a50cfd2534c9baf855b070924dd7d82e404b4d69bf`; runs `st_161` and supplies initialization, switch handlers, outputs, lamps, and mechanism behavior.
- `vpx-table.star-trek-pro-fss`: archived VPX, SHA-256 `2976e3313a6fa1ee6f26709d515661b81ade8f01894a847b907a5e608e5bb9e7`; containing archive SHA-256 `eaa577d4514b4945f6d98195a161c3de59d67c61f2b4d75e4c99169c9b6c1a34`; lamp objects and artwork were inspected read-only.
- `runtime.star-trek-pro.boot-start`: exact `st_161c` LibPinMAME run, SHA-256 `a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7`; ROM archive SHA-256 `f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0` remains external.
- `pinmame.core.4ec52ff0ac13`: pinned SAM driver, switch serialization, dedicated-input constants, and display implementation.
"""


def pro_runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"machine_ids": ["stern.star-trek-pro.2013"], "driver_ids": ["st_161c"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": "st_161c", "rom_archive_sha256": "f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0",
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game st_161c --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>",
			"raw_runs": [{"name": "boot-start", "sha256": "a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7", "self_test_pulses": 0}],
			"observations": {
				"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "gi_addresses_seen": [0],
				"solenoid_addresses_seen": [],
				"lamp_addresses_seen": list(range(3, 81)),
			},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/st_161c/harness", "sha256": "a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7", "quality": "validated", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def write(path: Path, value: dict[str, object]) -> None:
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json(path, value)


def main() -> None:
	old = ROOT / "machines/partial/stern/star-trek-enterprise-limited-edition-2013.json"
	if old.exists():
		old.unlink()
	old_knowledge = ROOT / "knowledge/stubs/st_162h.md"
	if old_knowledge.exists():
		old_knowledge.unlink()
	premium_machine_id = "stern.star-trek-premium-limited-edition.2013"
	if premium_machine_id in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		write(ROOT / "machines/partial/stern/star-trek-premium-limited-edition-2013.json", build_premium())
		write_text(ROOT / "knowledge/stern/star-trek-premium-limited-edition-2013.md", fail_closed_spatial_knowledge(premium_machine_id, PREMIUM_KNOWLEDGE))
	pro_machine_id = "stern.star-trek-pro.2013"
	if pro_machine_id in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		stale_pro = ROOT / "machines/partial/stern/star-trek-pro-2013.json"
		if stale_pro.exists():
			stale_pro.unlink()
		write(stale_pro, build_pro())
		write_text(ROOT / "knowledge/stern/star-trek-pro-2013.md", fail_closed_spatial_knowledge(pro_machine_id, PRO_KNOWLEDGE))
	write(ROOT / "evidence/runtime/sam/star-trek-pro-boot-start.json", pro_runtime_evidence())


if __name__ == "__main__":
	main()
