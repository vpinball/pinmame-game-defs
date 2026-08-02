from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = "pinmame.catalog.4ec52ff0ac13"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
MANUAL_SOURCE = "manual.ali.tech-chart"
VPX_SOURCE = "vpx.ali.jp-salas.1.0.1"
VPX_TABLE_SOURCE = "vpx-table.ali.jp-salas.1.0.1"
LAMP_TEST_SOURCE = "runtime.ali.service-lamp-test"
SOLENOID_TEST_SOURCE = "runtime.ali.service-solenoid-test"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


SWITCHES: dict[int, tuple[str, str, bool]] = {
	1: ("Coin chute I (center)", "button", True),
	2: ("Coin chute II (left)", "button", True),
	3: ("Coin chute III (right)", "button", True),
	4: ("Unused matrix position I3/ST0", "unknown", True),
	5: ("Bottom rollover button", "microswitch", True),
	6: ("Credit / start button", "button", False),
	7: ("Tilt", "tilt", False),
	8: ("Slam tilt", "tilt", False),
	9: ("Top-left spinner", "microswitch", True),
	10: ("Unused matrix position I1/ST1", "unknown", True),
	11: ("Two middle rollover buttons (shared input)", "microswitch", True),
	12: ("Right thumper bumper", "leaf", True),
	13: ("Left thumper bumper", "leaf", True),
	14: ("Middle thumper bumper", "leaf", True),
	15: ("Right slingshot", "leaf", True),
	16: ("Left slingshot", "leaf", True),
	17: ("Unused matrix position I0/ST2", "unknown", True),
	18: ("Unused matrix position I1/ST2", "unknown", True),
	19: ("Top three-bank drop target (left)", "leaf", False),
	20: ("Top three-bank drop target (middle)", "leaf", False),
	21: ("Top three-bank drop target (right)", "leaf", False),
	22: ("Left three-bank drop target (bottom)", "leaf", False),
	23: ("Left three-bank drop target (middle)", "leaf", False),
	24: ("Left three-bank drop target (top)", "leaf", False),
	25: ("G stand-up target", "leaf", True),
	26: ("R stand-up target", "leaf", True),
	27: ("E stand-up target", "leaf", True),
	28: ("A stand-up target", "leaf", True),
	29: ("T stand-up target", "leaf", True),
	30: ("Top-left saucer", "leaf", False),
	31: ("Top-middle saucer", "leaf", False),
	32: ("Top-right saucer", "leaf", False),
	33: ("Outhole", "leaf", False),
	34: ("Right outlane", "leaf", True),
	35: ("Left outlane", "leaf", True),
	36: ("Right return lane", "leaf", True),
	37: ("Left return lane", "leaf", True),
	38: ("Middle-right saucer", "leaf", False),
	39: ("Middle-left passive saucer", "leaf", False),
	40: ("Unused matrix position I7/ST4", "unknown", True),
}

STROBES = [
	("WHT-RED / RED-YEL", "A4J2-1 / A4J3-2"),
	("BRN-WHT", "A4J2-2 / A4J3-3 (second connection not used)"),
	("WHT-BLU", "A4J2-3"),
	("WHT-YEL", "A4J2-4"),
	("YEL-RED", "A4J2-5"),
]
RETURNS = [
	("BRN / RED-WHT", "A4J2-8 / A4J3-9"),
	("GRY / BRN-WHT", "A4J2-9 / A4J3-10"),
	("WHT-ORN / BLU", "A4J2-10 / A4J3-11"),
	("WHT-BLK", "A4J2-11 / A4J3-12 (second connection not used)"),
	("WHT-GRN", "A4J2-12 / A4J3-13 (second connection not used)"),
	("WHT-BRN / BLU-WHT", "A4J2-13 / A4J3-14"),
	("BRN-YEL / BLU-ORN", "A4J2-14 / A4J3-15"),
	("ORN / YEL", "A4J2-15 / A4J3-16"),
]


def matrix_switch(number: int) -> dict[str, object]:
	label, switch_type, pulse = SWITCHES[number]
	strobe = (number - 1) // 8
	return_index = (number - 1) % 8
	availability = "unused" if number in {4, 10, 17, 18, 40} else "used"
	wiring = {
		"board": "MPU module M-200 A4",
		"control_wire": STROBES[strobe][0],
		"control_connection": STROBES[strobe][1],
		"return_wire": RETURNS[return_index][0],
		"return_connection": RETURNS[return_index][1],
	}
	sources = (MANUAL_SOURCE, VPX_SOURCE) if availability == "used" else (MANUAL_SOURCE,)
	physical: dict[str, object] = {
		"switch_type": switch_type,
		"location": label,
		"notes": f"Switch-matrix return I{return_index}, strobe ST{strobe}.",
	}
	if number == 9:
		physical["notes"] = "The technical chart calls this a top-left rollover button; the known-working table pulses the same address from its spinner, which is the runtime ground truth."
	if number == 11:
		physical["quantity"] = 2
		physical["notes"] = "Two physical middle rollover buttons are wired in parallel to one MPU input."
	return {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": False,
		"pulse": pulse,
		"availability": availability,
		"physical": physical,
		"wiring": wiring,
		"provenance": provenance(*sources),
	}


def service_switch(number: int, label: str) -> dict[str, object]:
	return {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number),
		"normally_closed": False,
		"pulse": False,
		"availability": "used",
		"physical": {"switch_type": "button", "location": "Cabinet or MPU service controls"},
		"roles": ["service"],
		"provenance": provenance(CORE_SOURCE, VPX_SOURCE),
	}


def flipper_button(number: int, label: str, availability: str) -> dict[str, object]:
	return {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number),
		"normally_closed": False,
		"pulse": False,
		"availability": availability,
		"physical": {"switch_type": "button", "location": "Cabinet side"},
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE),
	}


def dip_switch(number: int) -> dict[str, object]:
	return {
		"id": f"dip.s{number}",
		"label": f"MPU option switch S{number}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number},
		"aliases": aliases("pinmame.dip", number, f"S{number}"),
		"availability": "used",
		"physical": {"switch_type": "dip", "location": "MPU module M-200 A4"},
		"provenance": provenance(CORE_SOURCE, VPX_SOURCE),
	}


def eos_switch(number: int, side: str) -> dict[str, object]:
	return {
		"id": f"switch.{side}-flipper-end-of-stroke",
		"label": f"{side.title()} flipper end-of-stroke contact",
		"kind": "switch",
		"binding": {"group": "physical.input.direct", "device": number},
		"aliases": [{"namespace": "manual.address", "value": f"{side}-flipper-eos"}],
		"normally_closed": True,
		"pulse": False,
		"availability": "used",
		"physical": {
			"switch_type": "leaf",
			"location": f"{side.title()} flipper assembly",
			"notes": "Hard-wired dual-winding flipper contact; this is not a PinMAME switch address.",
		},
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE),
	}


def all_inputs() -> list[dict[str, object]]:
	items = [service_switch(-7, "Self-test button"), service_switch(-6, "CPU diagnostic button"), service_switch(-5, "Sound diagnostic button")]
	items.extend(matrix_switch(number) for number in range(1, 41))
	items.extend([
		flipper_button(81, "Upper-right flipper button position", "unused"),
		flipper_button(82, "Lower-right flipper button", "used"),
		flipper_button(83, "Upper-left flipper button position", "unused"),
		flipper_button(84, "Lower-left flipper button", "used"),
	])
	items.extend(dip_switch(number) for number in range(1, 33))
	items.extend([eos_switch(1, "left"), eos_switch(2, "right")])
	return items


# Public PinMAME address -> physical service-diagnostic number and chart data.
COILS: dict[int, dict[str, object]] = {
	2: {"manual": 1, "label": "Right slingshot", "kind": "coil", "wire": "GRN-ORN", "connector": "A3J2-9, J1-2", "q": "Q1", "part": "J-27-1700"},
	1: {"manual": 2, "label": "Left slingshot", "kind": "coil", "wire": "GRN-BLU", "connector": "A3J2-4, J1-3", "q": "Q2", "part": "J-27-1700"},
	6: {"manual": 3, "label": "Knocker", "kind": "coil", "wire": "GRN-BLK", "connector": "A3J2-5, J3-4", "q": "Q3", "part": "N-26-1200"},
	7: {"manual": 4, "label": "Top three-saucer eject", "kind": "coil", "wire": "BLK-BLU", "connector": "A3J1-5", "q": "Q4", "part": "J-28-2300"},
	3: {"manual": 5, "label": "Left thumper bumper", "kind": "coil", "wire": "GRN-YEL", "connector": "A3J2-10", "q": "Q5", "part": "J-26-1200"},
	4: {"manual": 6, "label": "Middle thumper bumper", "kind": "coil", "wire": "GRY-RED", "connector": "A3J2-11", "q": "Q6", "part": "J-26-1200"},
	5: {"manual": 7, "label": "Right thumper bumper", "kind": "coil", "wire": "RED-YEL", "connector": "A3J2-12", "q": "Q7", "part": "J-26-1200"},
	8: {"manual": 8, "label": "Top three-bank drop-target reset", "kind": "coil", "wire": "BLK-ORN", "connector": "A3J5-10", "q": "Q8", "part": "B-27-2300"},
	11: {"manual": 9, "label": "Outhole eject", "kind": "coil", "wire": "RED-BLU", "connector": "A3J5-9", "q": "Q9", "part": "JX-26-1100"},
	12: {"manual": 10, "label": "Unused momentary output 10", "kind": "coil", "wire": None, "connector": "A3J5-15", "q": "Q10", "part": None},
	14: {"manual": 11, "label": "General-illumination relay", "kind": "relay", "wire": "ORN-BLK", "connector": "A3J5-14", "q": "Q11", "part": "48V relay"},
	13: {"manual": 12, "label": "Unused momentary output 12", "kind": "coil", "wire": None, "connector": "A3J5-13", "q": "Q12", "part": None},
	9: {"manual": 13, "label": "Left three-bank drop-target reset", "kind": "coil", "wire": "BLK-YEL", "connector": "A3J5-12", "q": "Q13", "part": "B-27-2300"},
	10: {"manual": 14, "label": "Middle-right saucer eject", "kind": "coil", "wire": "BLK-GRN", "connector": "A3J5-11", "q": "Q14", "part": "J-28-2300"},
	19: {"manual": 15, "label": "Flipper-enabling relay", "kind": "relay", "wire": None, "connector": "Hard-wired enable circuit", "q": "Q15", "part": "48V relay"},
	15: {"manual": 16, "label": "Unused momentary output 16", "kind": "coil", "wire": None, "connector": "A3J5-8, J2-6, J3-7", "q": "Q16", "part": None},
	17: {"manual": 17, "label": "Unused continuous output 17", "kind": "relay", "wire": None, "connector": "A3J5-7", "q": "Q17", "part": None},
	20: {"manual": 18, "label": "Unused continuous output 18", "kind": "relay", "wire": None, "connector": "A3J5-3, J2-15, J3-9", "q": "Q18", "part": None},
	18: {"manual": 19, "label": "Coin-lockout coil", "kind": "coil", "wire": "YEL-WHT", "connector": "A3J2-8", "q": "Q19", "part": "C-36-5300"},
}


def coil_output(address: int, spec: dict[str, object]) -> dict[str, object]:
	availability = "unused" if str(spec["label"]).startswith("Unused") else "used"
	wiring: dict[str, object] = {
		"board": "Solenoid Driver / Voltage Regulator module SDU-100 A3",
		"driver_transistor": str(spec["q"]),
		"drive_connection": str(spec["connector"]),
		"nominal_voltage_v": 43,
		"voltage_type": "dc",
	}
	if spec["wire"]:
		wiring["drive_wire"] = str(spec["wire"])
	physical: dict[str, object] = {"location": str(spec["label"])}
	if spec["part"]:
		physical["part_number"] = str(spec["part"])
	sources = (MANUAL_SOURCE, SOLENOID_TEST_SOURCE, VPX_SOURCE) if availability == "used" else (MANUAL_SOURCE, SOLENOID_TEST_SOURCE)
	return {
		"id": f"device.{slug(str(spec['label']))}",
		"label": str(spec["label"]),
		"kind": str(spec["kind"]),
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases("pinmame.solenoid", address, str(spec["manual"])),
		"availability": availability,
		"physical": physical,
		"wiring": wiring,
		"provenance": provenance(*sources),
	}


def flipper_output(address: int, side: str, coil_wire: str, coil_connection: str, button_wire: str, button_connection: str) -> dict[str, object]:
	return {
		"id": f"device.{side}-flipper",
		"label": f"{side.title()} lower flipper dual-winding coil",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": aliases("pinmame.solenoid", address, f"{side}-flipper"),
		"availability": "used",
		"physical": {"part_number": "J-25-450/34-4500", "location": f"{side.title()} flipper assembly"},
		"wiring": {
			"board": "Hard-wired flipper circuit gated by output 19",
			"power_wire": "BLU-WHT",
			"drive_wire": coil_wire,
			"drive_connection": coil_connection,
			"control_wire": button_wire,
			"control_connection": button_connection,
			"nominal_voltage_v": 43,
			"voltage_type": "dc",
		},
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE),
	}


LAMP_Q: dict[int, tuple[str, str, str, str]] = {
	1: ("", "A5J1-24", "", "MCR-106"), 2: ("Bonus multiplier 4X", "A5J1-25", "PUR-BLK", "MCR-106"), 3: ("Shoot Again (playfield and backglass)", "A5J1-26/J2-21", "GRY-RED", "MCR-106"), 4: ("Center rollover button 1,000", "A5J1-28", "BLK-BLU", "2N5060"),
	5: ("Top saucer Special", "A5J2-16", "YEL-BLU", "2N5060"), 6: ("Top ALI A", "A5J2-14", "BLU-RED", "2N5060"), 7: ("Bonus 8,000", "A5J2-13", "GRY-GRN", "2N5060"), 8: ("Target T", "A5J1-23", "GRY-BLK", "MCR-106"),
	9: ("Top drop targets 5,000", "A5J1-14", "GRY-ORN", "MCR-106"), 10: ("Left drop targets 4,000", "A5J1-15", "GRY-YEL", "MCR-106"), 11: ("Center 200 G", "A5J1-16", "BLK", "2N5060"), 12: ("Arch T (first)", "A5J1-19", "GRY-GRN", "2N5060"),
	13: ("Target G", "A5J1-17", "PUR", "2N5060"), 14: ("Arch G", "A5J1-18", "BRN-BLK", "2N5060"), 15: ("Ball in Play", "A5J2-23", "", "MCR-106"), 16: ("High Score to Date", "A5J2-22", "GRY-ORN", "MCR-106"),
	17: ("Bonus multiplier 5X", "A5J1-11", "BLK-ORN", "MCR-106"), 18: ("Outlane left", "A5J2-20", "YEL-BLK", "2N5060"), 19: ("Top ALI L", "A5J2-15", "BLK-BLU", "2N5060"), 20: ("", "A5J1-13", "", "2N5060"),
	21: ("Bonus 10,000", "A5J2-12", "WHT-YEL", "2N5060"), 22: ("Left drop targets 6,000", "A5J1-10", "GRY-BLU", "MCR-106"), 23: ("Bonus 2,000", "A5J2-8", "PUR-YEL", "MCR-106"), 24: ("", "A5J1-5", "", "MCR-106"),
	25: ("", "A5J1-6", "", "2N5060"), 26: ("Center 400 R", "A5J1-7", "YEL-GRN", "2N5060"), 27: ("Arch S", "A5J1-9", "GRY", "2N5060"), 28: ("Target R", "A5J1-8", "GRN-BLK", "2N5060"),
	29: ("Arch R", "A5J1-1", "BLU-RED", "2N5060"), 30: ("Outlane right", "A5J2-6", "BLU-WHT", "2N5060"), 31: ("Top ALI I", "A5J2-2", "RED-BLU", "2N5060"), 32: ("Center 600 S", "A5J3-27", "ORN-WHT", "2N5060"),
	33: ("Game Over", "A5J2-11", "GRY-WHT", "MCR-106"), 34: ("Top drop targets 10,000", "A5J1-2", "PUR-WHT", "MCR-106"), 35: ("Return lane S (left)", "A5J1-3", "RED-GRN", "MCR-106"), 36: ("Arch E (first)", "A5J3-26", "BLK-WHT", "2N5060"),
	37: ("Left drop targets 8,000", "A5J3-23", "WHT-GRY", "2N5060"), 38: ("Arch T (second)", "A5J3-25", "RED-YEL", "2N5060"), 39: ("Bonus 20,000", "A5J2-4", "PUR-BLK", "2N5060"), 40: ("Bonus 4,000", "A5J2-9", "GRY", "MCR-106"),
	41: ("Extra Ball (right)", "A5J3-20", "WHT-ORN", "MCR-106"), 42: ("Bonus multiplier 2X", "A5J3-21", "BLK-GRN", "MCR-106"), 43: ("Top saucer 5,000", "A5J2-7", "YEL-WHT", "2N5060"), 44: ("Target E", "A5J3-19", "BLK-RED", "2N5060"),
	45: ("Match", "A5J2-1", "GRY-YEL", "2N5060"), 46: ("Extra Ball (left)", "A5J3-18", "RED-BLU", "2N5060"), 47: ("Tilt", "A5J2-10", "GRY-BLK", "MCR-106"), 48: ("Top drop targets 15,000", "A5J3-16", "RED-BLK", "MCR-106"),
	49: ("Return lane T (right)", "A5J3-17", "YEL-BLU", "MCR-106"), 50: ("Arch E (second)", "A5J3-12", "ORN-RED", "2N5060"), 51: ("Target A", "A5J3-15", "WHT-BLK", "2N5060"), 52: ("Bonus 6,000", "A5J2-5", "BLK-YEL", "2N5060"),
	53: ("Top saucer 10,000", "A5J2-3", "BLK-WHT", "2N5060"), 54: ("", "A5J3-11", "", "MCR-106"), 55: ("Top drop targets 20,000", "A5J3-9", "WHT-RED", "MCR-106"), 56: ("Bonus multiplier 3X", "A5J3-10", "GRY-BLK", "MCR-106"),
	57: ("Arch A", "A5J3-1", "GRN-RED", "2N5060"), 58: ("", "A5J3-2", "", "2N5060"), 59: ("Center 800 E", "A5J3-4", "RED-WHT", "2N5060"), 60: ("Left drop targets 10,000", "A5J3-3", "GRN", "2N5060"),
}

PUBLIC_LAMP_Q = {
	1: 14, 2: 12, 3: 13, 4: 8, 5: 9, 6: 10, 7: 11, 8: 4, 9: 1, 10: 2, 11: 3, 12: 7, 13: 16, 14: 5, 15: 6,
	17: 29, 18: 27, 19: 28, 20: 35, 21: 34, 22: 22, 23: 26, 24: 24, 25: 25, 26: 17, 27: 23, 28: 21, 29: 15, 30: 18, 31: 19,
	33: 36, 34: 38, 35: 44, 36: 49, 37: 48, 38: 37, 39: 32, 40: 20, 41: 42, 42: 46, 43: 40, 44: 39, 45: 33, 46: 30, 47: 31,
	49: 57, 50: 50, 51: 51, 52: 54, 53: 55, 54: 60, 55: 59, 56: 58, 57: 56, 58: 41, 59: 52, 60: 53, 61: 47, 62: 43, 63: 45,
}


def lamp_output(address: int, q_number: int) -> dict[str, object]:
	label, connector, wire, scr_type = LAMP_Q[q_number]
	availability = "used" if label else "unused"
	if not label:
		label = f"Unused controlled-lamp SCR Q{q_number:02d}"
	wiring: dict[str, object] = {
		"board": "Lamp Driver module LDA-100 A5",
		"driver_transistor": f"Q{q_number:02d} ({scr_type})",
		"drive_connection": connector,
	}
	if wire:
		wiring["drive_wire"] = wire
	return {
		"id": f"lamp.{slug(label)}",
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": address},
		"aliases": aliases("pinmame.lamp", address, f"Q{q_number:02d}"),
		"availability": availability,
		"physical": {
			"location": label,
			"notes": "Discrete controlled-lamp circuit; this is not a row/column lamp matrix.",
		},
		"wiring": wiring,
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE, LAMP_TEST_SOURCE),
	}


def all_outputs() -> list[dict[str, object]]:
	items = [coil_output(address, COILS[address]) for address in sorted(COILS)]
	items.extend([
		flipper_output(46, "right", "ORN", "A3J1-9", "RED", "A3J2-1"),
		flipper_output(48, "left", "GRN", "A3J1-8", "BLU", "A3J2-2"),
	])
	items.extend(lamp_output(address, PUBLIC_LAMP_Q[address]) for address in sorted(PUBLIC_LAMP_Q))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *sources: str) -> dict[str, object]:
	return {
		"id": mechanism_id,
		"label": label,
		"kind": kind,
		"actuators": actuators,
		"sensors": sensors,
		"behavior": behavior,
		"provenance": provenance(*sources),
	}


def mechanisms() -> list[dict[str, object]]:
	return [
		mechanism("mechanism.outhole", "Single-ball outhole and manual shooter feed", "kicker", ["device.outhole-eject"], ["switch.outhole"], "Ali has no multi-position trough. Initialize one ball at the outhole. Public output 11 ejects a ball held on switch 33 toward 115 degrees with nominal force 3 in the working table; the player then launches it manually.", MANUAL_SOURCE, VPX_SOURCE),
		mechanism("mechanism.top-three-saucers", "Three top saucers with shared eject", "kicker", ["device.top-three-saucer-eject"], ["switch.top-left-saucer", "switch.top-middle-saucer", "switch.top-right-saucer"], "Switches 30, 31, and 32 independently detect held balls, but all three physical cups share public output 7/service solenoid 4. When asserted, the working table exposes all three kicker holes, ejects every occupied cup toward 180 degrees at force 10 with force/angle variation 3, then restores the visual cup state after 200 ms.", MANUAL_SOURCE, VPX_SOURCE),
		mechanism("mechanism.middle-right-saucer", "Middle-right saucer", "kicker", ["device.middle-right-saucer-eject"], ["switch.middle-right-saucer"], "Switch 38 remains active while a ball is held. Public output 10/service solenoid 14 ejects toward 180 degrees at nominal force 10 with force/angle variation 3; the working table restores the visual cup after 200 ms.", MANUAL_SOURCE, VPX_SOURCE),
		mechanism("mechanism.middle-left-passive-saucer", "Middle-left passive saucer", "other", [], ["switch.middle-left-passive-saucer"], "The physical chart names switch 39 Middle Left Saucer, but the proven table supplies no capture or eject actuator and only mirrors hit/unhit state to the ROM. Recreate it as the passive, gravity-clearing playfield feature shown by the working geometry; do not invent a PinMAME coil.", MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE),
		mechanism("mechanism.top-drop-bank", "Top three-bank drop targets", "drop_target_bank", ["device.top-three-bank-drop-target-reset"], ["switch.top-three-bank-drop-target-left", "switch.top-three-bank-drop-target-middle", "switch.top-three-bank-drop-target-right"], "Switches 19-21 stay active while their respective targets are down. Public output 8/service solenoid 8 resets the complete bank.", MANUAL_SOURCE, VPX_SOURCE),
		mechanism("mechanism.left-drop-bank", "Left three-bank drop targets", "drop_target_bank", ["device.left-three-bank-drop-target-reset"], ["switch.left-three-bank-drop-target-bottom", "switch.left-three-bank-drop-target-middle", "switch.left-three-bank-drop-target-top"], "Switches 22-24 stay active while their respective targets are down. Public output 9/service solenoid 13 resets the complete bank.", MANUAL_SOURCE, VPX_SOURCE),
		mechanism("mechanism.thumper-bumpers", "Three thumper bumpers", "kicker", ["device.left-thumper-bumper", "device.middle-thumper-bumper", "device.right-thumper-bumper"], ["switch.left-thumper-bumper", "switch.middle-thumper-bumper", "switch.right-thumper-bumper"], "Left switch 13 drives public output 3/service solenoid 5, middle switch 14 drives public output 4/service solenoid 6, and right switch 12 drives public output 5/service solenoid 7.", MANUAL_SOURCE, VPX_SOURCE, SOLENOID_TEST_SOURCE),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left switch 16 drives public output 1/service solenoid 2. Right switch 15 drives public output 2/service solenoid 1. This reversed-looking public/service numbering is confirmed by the ROM service sweep and working script semantics.", MANUAL_SOURCE, VPX_SOURCE, SOLENOID_TEST_SOURCE),
		mechanism("mechanism.flippers", "Two lower dual-winding flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.lower-left-flipper-button", "switch.lower-right-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-end-of-stroke"], "Output 19 gates both hard-wired 43 V flipper circuits. Synthetic public switch 84/button and output 48 represent the left flipper; switch 82 and output 46 represent the right. Each J-25-450/34-4500 assembly uses its normally-closed local EOS contact to transfer from power to hold winding.", MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE),
		mechanism("mechanism.spinner", "Top-left spinner", "other", [], ["switch.top-left-spinner"], "Each completed spinner rotation pulses public switch 9. The technical chart calls address 9 a Top Left Rollover Button, but the known-working table script is ground truth for the recreated physical feature and maps its spinner directly to 9.", MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE),
	]


def relationships() -> list[dict[str, object]]:
	items: list[tuple[str, str, str, str]] = [
		("relationship.left-sling", "direct", "switch.left-slingshot", "device.left-slingshot"),
		("relationship.right-sling", "direct", "switch.right-slingshot", "device.right-slingshot"),
		("relationship.left-pop", "direct", "switch.left-thumper-bumper", "device.left-thumper-bumper"),
		("relationship.middle-pop", "direct", "switch.middle-thumper-bumper", "device.middle-thumper-bumper"),
		("relationship.right-pop", "direct", "switch.right-thumper-bumper", "device.right-thumper-bumper"),
		("relationship.outhole", "pulse", "switch.outhole", "device.outhole-eject"),
		("relationship.middle-right-saucer", "pulse", "switch.middle-right-saucer", "device.middle-right-saucer-eject"),
		("relationship.left-flipper", "relay_gated", "switch.lower-left-flipper-button", "device.left-flipper"),
		("relationship.right-flipper", "relay_gated", "switch.lower-right-flipper-button", "device.right-flipper"),
	]
	for number, name in ((30, "top-left"), (31, "top-middle"), (32, "top-right")):
		items.append((f"relationship.{name}-saucer", "pulse", matrix_switch(number)["id"], "device.top-three-saucer-eject"))
	return [
		{"id": relationship_id, "kind": kind, "source": source, "destination": destination, "provenance": provenance(MANUAL_SOURCE, VPX_SOURCE)}
		for relationship_id, kind, source, destination in items
	]


SOURCES: list[dict[str, object]] = [
	{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames entries alib and alic", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/stgames.c lines 7-16 and 595-632; src/wpc/by35.c; src/wpc/by35.h", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://www.pinballrebel.com/pinball/cards/Tech_Charts/Stern_Ali_Tech_Chart.pdf", "sha256": "455ea85f99eff031ffcca75489ab4dfea0a587a864522fb2fa30a4bfd160d78b", "locator": "Stern_Ali_Tech_Chart.pdf page 1: switch matrix, controlled-lamp chart, coil table, flipper circuits, boards, and fuses", "license": "NOASSERTION", "attribution": "Inkochnito; hosted by Pinball Rebel", "source_id": "pinballrebel", "original_filename": "Stern_Ali_Tech_Chart.pdf", "rights": "NOASSERTION"},
	{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Ali-v1.0.1.vbs", "revision": VPX_REVISION, "sha256": "6dbde0131a367c643ae87fe511052d28d83ed0cb6b74b87ba731a900678f1849", "locator": "Ali-v1.0.1.vbs: initialization, switches 1-40, outputs 6-11/19/46/48, lamp objects 1-63, ball stacks, drop banks, and mechanism callbacks", "license": "NOASSERTION", "attribution": "JP Salas, table contributors, and vpxtable_scripts contributors"},
	{"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "local-evidence://vpx/Ali-Stern-1980.vpx", "sha256": "14137b288aee843e834f509b467dd288fcf0e3269afcbd397e2276d31c24533f", "locator": "Ali (Stern 1980).vpx, 3571712 bytes; embedded playfield art and object positions inspected without modifying the table", "license": "NOASSERTION", "attribution": "JP Salas and table contributors", "original_filename": "Ali (Stern 1980).vpx", "rights": "NOASSERTION"},
	{"id": LAMP_TEST_SOURCE, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/ali-service-single.json", "sha256": "320e2e140e58235d6ee4ef5cbc66788eb2006b0a6fb743dcae889793865db0c3", "locator": "tools/run_pinmame_harness.py; exact ali.zip SHA-256 bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b; one -7 self-test pulse; all 60 valid lamp addresses observed and invalid 16/32/48/64 absent", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
	{"id": SOLENOID_TEST_SOURCE, "kind": "service_diagnostic", "uri": "local-evidence://pinmame-harness/ali-service-solenoids.json", "sha256": "cb14917ee85f7b86b1c4c61b4b9c147c8e7909a97e52e21f2dfe237ac35219bf", "locator": "tools/run_pinmame_harness.py; exact ali.zip SHA-256 bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b; two -7 self-test pulses; repeated physical 1-19 to public-output sweep captured", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
]


def build_definition() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 1,
		"machine": {"id": "stern.ali-seven-digit-conversion.2023", "name": "Ali seven-digit conversion", "manufacturer": "Stern / Idleman / slochar", "year": 2023, "kind": "physical_conversion", "ipdb_id": 43},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.stern-mpu200", "inversion_applied_by_emulator": True},
		"drivers": [
			{"id": "alib", "description": "Ali (7-digit conversion Free Play rev. 76)", "year": "2023", "manufacturer": "Stern / Idleman", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Revision 76 conversion software for the same physical Ali playfield, Stern MPU-200 I/O, ST300 sound board, and seven-digit display conversion."},
			{"id": "alic", "description": "Ali (7-digit conversion Free Play rev. 85)", "year": "2023", "manufacturer": "Stern / slochar", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Revision 85 conversion software for the same physical Ali playfield, Stern MPU-200 I/O, ST300 sound board, and seven-digit display conversion."},
		],
		"inputs": all_inputs(),
		"outputs": all_outputs(),
		"displays": [
			{"id": f"display.player-{number}", "label": f"Player {number} seven-digit score display", "kind": "segment", "width": 7, "provenance": provenance(CORE_SOURCE)}
			for number in range(1, 5)
		] + [
			{"id": "display.credits", "label": "Two-digit credit display", "kind": "segment", "width": 2, "provenance": provenance(CORE_SOURCE)},
			{"id": "display.ball-match", "label": "Two-digit ball / match display", "kind": "segment", "width": 2, "provenance": provenance(CORE_SOURCE)},
		],
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": SOURCES,
		"knowledge": {"path": "knowledge/stern/ali-seven-digit-conversion-2023.md", "status": "complete"},
		"conflicts": [],
	}


KNOWLEDGE = """# Ali seven-digit conversion (Stern, 2023 software on the 1980 playfield)

Coverage: **author-ready - complete physical inventory, controller bindings, wiring, mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers PinMAME `alib` revision 76 and `alic` revision 85. They are seven-digit free-play software conversions for the physical Stern Ali playfield (IPDB 43), not newly manufactured 2023 tables. Both PinMAME declarations use Stern MPU-200, the same switch-port definition, ST300 sound, and the seven-digit `dispst7` layout. The original six-digit `ali`/`alifp` drivers will receive their own definition because their score displays differ.

The known-working `Ali-v1.0.1.vbs` script is ground truth for controller-facing semantics and mechanism behavior. The Ali technical chart is authoritative for physical inventory, board connectors, wire colors, driver transistors, coil types, and diagnostic numbers. Pinned PinMAME source is authoritative for driver identity and public controller topology. The repeatable ROM harness used the available original `ali` image to validate the unchanged MPU-200 public-address translation; the conversion ROM archives were not present locally, so the harness is not used to infer conversion-only rules.

## Controller address translations

The 19 physical service solenoids do not line up numerically with PinMAME callbacks. The service sweep proves this physical-to-public sequence: `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18`. Public output 16 is an unaddressable decoder slot. Lower flippers are generic callbacks 46 right and 48 left, gated by public output 19.

The LDA-100 has sixty discrete SCR outputs, not a lamp matrix. The JSON maps each public address to its physical Q-number, connector, wire, and SCR type. Public 16, 32, 48, and 64 are unaddressable decoder slots and therefore are not devices. The ROM lamp test exercised every other address, including unused Q01, Q20, Q24, Q25, Q54, and Q58. The manual leaves Q15 unnamed, but the working script identifies its public address 29 as Ball in Play; script semantics win.

## Switches and shared contacts

The switch matrix is five strobes by eight returns, public addresses 1-40. Addresses 4, 10, 17, 18, and 40 are physically unused. Two separate middle rollover buttons share address 11 and must be wired in parallel. The technical chart calls address 9 a top-left rollover button, while the proven recreation pulses it from the spinner; build the spinner shown by the working table and bind it to 9. Service controls are -7 self-test, -6 CPU diagnostic, and -5 sound diagnostic. Cabinet flipper inputs are 82 right and 84 left; 81/83 are unused upper positions. All 32 MPU option switches are retained as configuration inputs.

## Ball lifecycle and saucers

Ali is a single-ball game with no trough stack. Initialize one ball in the outhole on switch 33. Public output 11/service solenoid 9 sends it toward the shooter lane at 115 degrees with nominal force 3; launching from the shooter lane is manual.

Top saucer switches 30, 31, and 32 share one physical eject output: public 7/service solenoid 4. The working table fires every occupied top cup toward 180 degrees at force 10 with force and angle variation 3, and resets its visual cup state after 200 ms. The middle-right cup holds on switch 38 and ejects through public 10/service solenoid 14 with the same vector and variation. The physical chart names switch 39 Middle Left Saucer, but the working table gives it no kicker or capture stack; model the known passive geometry and do not invent an output.

## Drop targets, bumpers, and slings

The top bank holds switches 19-21 while down and resets all three from public 8/service solenoid 8. The left bank holds switches 22-24 and resets from public 9/service solenoid 13. Stand-ups 25-29 spell GREAT and pulse individually.

The public callback mapping for direct playfield coils is intentionally non-obvious. Left slingshot switch 16 uses public output 1/service solenoid 2; right switch 15 uses public 2/service 1. Left thumper switch 13 uses public 3/service 5, middle switch 14 uses public 4/service 6, and right switch 12 uses public 5/service 7. Preserve the JSON public addresses in the controller integration and the service numbers only as physical aliases.

## Flippers, relays, and illumination

Output 19 drives the 48 V flipper-enabling relay. The two J-25-450/34-4500 assemblies are hard-wired dual-winding circuits: public 48 represents the left coil and public 46 the right, with local normally-closed EOS contacts transferring from power to hold windings. The manual preserves power, coil, and button wire colors and connectors in the JSON.

Public 14/service 11 is the physical general-illumination relay. The working VPX table turns GI on whenever a ball exists and off when none exists rather than subscribing to that callback. Build the relay-controlled GI circuit from the physical chart; treat the script's ball-count behavior as a compatibility fallback, not extra ROM I/O. Public 18/service 19 is the coin-lockout coil. Public 12, 13, 15, 17, and 20 are wired diagnostic positions with no installed device and remain explicitly unused.

## Displays and sound

The conversion uses four seven-digit player score displays, a two-digit credit display, and a two-digit ball/match display. PinMAME `dispst7` is the exact layout contract. The original Ali hardware used six-digit player displays, which is why original and conversion drivers must not be merged. Sound is Stern ST300; sound-command behavior belongs to PinMAME and does not add playfield devices.

## Recreation checklist

- Build every JSON input and output, including unused wired positions, both physical EOS contacts, shared switch 11, all sixty valid SCR lamp outputs, and the two seven-digit-conversion auxiliary displays.
- Initialize one ball at switch 33; initialize both drop banks raised and every saucer empty.
- Use PinMAME public bindings for runtime callbacks and retain physical service numbers/Q-numbers as diagnostic aliases.
- Reproduce shared top-saucer actuation, passive switch-39 geometry, manual shooter launch, hard-wired dual-winding flippers, GI relay, and coin lockout.
- Treat the working VPX force, angle, variance, and 200 ms visual reset values as validated authoring starting points; refine only geometry-dependent tuning without changing controller causality.

## Sources

- `manual.ali.tech-chart`: organized external `Stern_Ali_Tech_Chart.pdf`, SHA-256 `455ea85f99eff031ffcca75489ab4dfea0a587a864522fb2fa30a4bfd160d78b`; one-page switch, lamp, coil, flipper, board, and fuse chart.
- `vpx.ali.jp-salas.1.0.1`: pinned known-working script, SHA-256 `6dbde0131a367c643ae87fe511052d28d83ed0cb6b74b87ba731a900678f1849`.
- `vpx-table.ali.jp-salas.1.0.1`: locally available working VPX used only for embedded playfield art/object-position confirmation, SHA-256 `14137b288aee843e834f509b467dd288fcf0e3269afcbd397e2276d31c24533f`.
- `runtime.ali.service-lamp-test` and `runtime.ali.service-solenoid-test`: isolated harness captures from exact `ali.zip` SHA-256 `bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b`; ROM bytes and raw mutable NVRAM remain outside the repository.
- `pinmame.core.4ec52ff0ac13`: pinned driver declarations, MPU-200 implementation, public-address conversion, and display layouts.
"""


EVIDENCE_SUMMARY = {
	"format": "pinmame-machine-evidence",
	"version": 1,
	"extractor": {"id": "libpinmame-service-harness", "version": 1},
	"source": {
		"kind": "service_diagnostic",
		"repository": "https://github.com/vpinball/pinmame",
		"revision": PINMAME_REVISION,
		"path": "external:pinmame-game-code/ali/harness/ali-service-solenoids.json",
		"sha256": "cb14917ee85f7b86b1c4c61b4b9c147c8e7909a97e52e21f2dfe237ac35219bf",
		"license": "NOASSERTION",
		"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		"quality": "validated",
	},
	"driver_ids": ["ali", "alib", "alic"],
	"machine_ids": ["stern.ali-seven-digit-conversion.2023"],
	"switches": [],
	"outputs": [],
	"states": [],
	"mechanisms": [],
	"recreation_notes": [],
	"runtime": {
		"game": "ali",
		"rom_archive_sha256": "bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b",
		"raw_runs": [
			{"name": "lamp-test", "sha256": "320e2e140e58235d6ee4ef5cbc66788eb2006b0a6fb743dcae889793865db0c3", "self_test_pulses": 1},
			{"name": "solenoid-test", "sha256": "cb14917ee85f7b86b1c4c61b4b9c147c8e7909a97e52e21f2dfe237ac35219bf", "self_test_pulses": 2},
		],
		"observations": {
			"lamp_addresses_seen": list(PUBLIC_LAMP_Q),
			"lamp_decoder_holes_not_seen": [16, 32, 48, 64],
			"physical_service_solenoid_to_public": {str(spec["manual"]): address for address, spec in sorted(COILS.items(), key=lambda item: int(item[1]["manual"]))},
			"public_solenoid_decoder_holes_not_seen": [16],
		},
		"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game ali --rom-path <roms> --work-dir <isolated-state> --pulse=-7:120:8 --pulse=-7:120:1 --observe 25 --output <external-json>",
	},
}


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


for driver_id in ("alib", "alic"):
	for path in (ROOT / f"machines/stubs/{driver_id}.json", ROOT / f"knowledge/stubs/{driver_id}.md"):
		if path.exists():
			path.unlink()


write_json(ROOT / "machines/author-ready/stern/ali-seven-digit-conversion-2023.json", build_definition())
write_json(ROOT / "evidence/runtime/stern/ali-service-diagnostics.json", EVIDENCE_SUMMARY)
knowledge_path = ROOT / "knowledge/stern/ali-seven-digit-conversion-2023.md"
knowledge_path.parent.mkdir(parents=True, exist_ok=True)
knowledge_path.write_text(KNOWLEDGE, encoding="utf-8")
