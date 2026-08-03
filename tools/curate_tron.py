"""Build reviewed, author-ready TRON: Legacy Pro and Limited Edition definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("trn_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.tron-legacy-pro-le.2011"
VPX_SOURCE = "vpx.tron-legacy-le-vpm-1.1.4"
STERN_SOURCE = "stern.tron-legacy-product-page"
PRO_IPDB_SOURCE = "ipdb.tron-legacy-pro.5682"
LE_IPDB_SOURCE = "ipdb.tron-legacy-limited-edition.5707"
PRO_RUNTIME_SOURCE = "runtime.tron-legacy-pro.boot-start"
LE_RUNTIME_SOURCE = "runtime.tron-legacy-limited-edition.boot-start"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


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


# Label, switch type, momentary pulse, semantic roles.
COMMON_SWITCHES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	1: ("TRON N target", "microswitch", True, ()), 2: ("TRON O target", "microswitch", True, ()),
	3: ("TRON R target", "microswitch", True, ()), 4: ("TRON T target", "microswitch", True, ()),
	7: ("ZUSE Z target", "microswitch", True, ()), 8: ("ZUSE U target", "microswitch", True, ()),
	11: ("Video game eject", "microswitch", False, ("ball.position",)), 12: ("Zen rollover", "leaf", False, ()),
	13: ("ZUSE E target", "microswitch", True, ()), 14: ("CLU L lane", "leaf", False, ()),
	15: ("Tournament start", "button", False, ("cabinet.tournament-start",)), 16: ("Start", "button", False, ("cabinet.start",)),
	18: ("Trough 4 left", "microswitch", False, ("ball.position",)), 19: ("Trough 3", "microswitch", False, ("ball.position",)),
	20: ("Trough 2", "microswitch", False, ("ball.position",)), 21: ("Trough 1 right", "microswitch", False, ("ball.position",)),
	22: ("Trough jam", "opto", True, ("ball.position",)), 23: ("Shooter lane", "microswitch", False, ("ball.position",)),
	24: ("Left outlane", "leaf", False, ()), 25: ("CLU C lane", "leaf", False, ()),
	26: ("Left slingshot", "leaf", True, ()), 27: ("Right slingshot", "leaf", True, ()),
	28: ("CLU U lane", "leaf", False, ()), 29: ("Right outlane", "leaf", False, ()),
	30: ("Left pop bumper", "leaf", True, ()), 31: ("Right pop bumper", "leaf", True, ()), 32: ("Bottom pop bumper", "leaf", True, ()),
	34: ("Right ramp exit", "microswitch", False, ()), 35: ("Left ramp entrance", "microswitch", False, ()),
	36: ("Right orbit spinner", "other", True, ()), 37: ("Left ramp exit", "microswitch", False, ()),
	38: ("Right ramp entrance", "microswitch", False, ()), 39: ("Right inner loop", "microswitch", False, ()),
	41: ("Disc opto", "opto", False, ("ball.position",)), 43: ("Left orbit", "microswitch", False, ()),
	44: ("Left spinner", "other", True, ()), 46: ("Right orbit", "microswitch", False, ()),
	48: ("ZUSE S target", "microswitch", True, ()),
	49: ("Recognizer three-bank left target", "microswitch", True, ()),
	50: ("Recognizer three-bank center target", "microswitch", True, ()),
	51: ("Recognizer three-bank right target", "microswitch", True, ()),
	52: ("Recognizer three-bank down", "microswitch", False, ("position.down",)),
	53: ("Recognizer three-bank up", "microswitch", False, ("position.up",)),
}
LE_SWITCHES = {
	54: ("Recognizer motor position 1", "microswitch", False, ("position.endpoint",)),
	55: ("Recognizer motor position 2", "microswitch", False, ("position.center",)),
	56: ("Recognizer motor position 3", "microswitch", False, ("position.endpoint",)),
}


def matrix_switch(number: int, limited_edition: bool) -> dict[str, object]:
	specs = COMMON_SWITCHES | (LE_SWITCHES if limited_edition else {})
	spec = specs.get(number)
	used = spec is not None
	label = spec[0] if used else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	physical: dict[str, object] = {"switch_type": spec[1] if used else "unknown"}
	if number in {1, 2, 3, 4}:
		physical["notes"] = "Four-bank resettable drop target on Limited Edition; fixed standup target on Pro. The same switch address reports a hit on either physical assembly."
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)), "normally_closed": False,
		"pulse": bool(spec[2]) if used else False, "availability": "used" if used else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE) if used and (limited_edition or number not in {1, 2, 3, 4}) else provenance(MANUAL_SOURCE),
	}
	if used and spec[3]:
		result["roles"] = list(spec[3])
	return result


SAM_DEDICATED_ROLES = {
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth",
	84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos",
	88: "flipper.upper.left.button", 87: "flipper.upper.left.eos", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, pulse: bool = False, notes: str | None = None) -> dict[str, object]:
	physical: dict[str, object] = {"switch_type": switch_type}
	if notes:
		physical["notes"] = notes
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"), "normally_closed": normally_closed, "pulse": pulse,
		"availability": availability, "physical": physical, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
	}
	if availability in {"used", "optional"} and device in SAM_DEDICATED_ROLES:
		result["roles"] = [SAM_DEDICATED_ROLES[device]]
	return result


def inputs(limited_edition: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, limited_edition) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False, True, None),
		(66, 2, "Center coin chute", "used", "button", False, True, None),
		(67, 3, "Right coin chute", "used", "button", False, True, None),
		(68, 4, "Fourth coin chute", "optional", "button", False, True, None),
		(69, 5, "Fifth coin chute", "optional", "button", False, True, None),
		(70, 6, "Unused dedicated switch D6", "unused", "unknown", False, False, None),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False, False, None),
		(72, 8, "Unused dedicated switch D8", "unused", "unknown", False, False, None),
		(84, 9, "Left flipper button", "used", "button", False, False, None),
		(83, 10, "Left flipper end-of-stroke", "used", "leaf", True, False, None),
		(82, 11, "Right flipper button", "used", "button", False, False, None),
		(81, 12, "Right flipper end-of-stroke", "used", "leaf", True, False, None),
		(88, 13, "Unused dedicated switch D13" if limited_edition else "Upper-left flipper button", "unused" if limited_edition else "used", "unknown" if limited_edition else "button", False, False, "Official LE dedicated-switch chart (PDF page 55, D-13) leaves this contact blank; the proven table stages the upper-left flipper from the left-flipper control." if limited_edition else "Official Pro dedicated-switch chart (PDF page 49, D-13) identifies this contact as the upper-left flipper button; the LE chart on PDF page 55 leaves D-13 blank."),
		(87, 14, "Unused dedicated switch D14" if limited_edition else "Upper-left flipper end-of-stroke", "unused" if limited_edition else "used", "unknown" if limited_edition else "leaf", False if limited_edition else True, False, "Official LE dedicated-switch chart (PDF page 55, D-14) leaves this contact blank; the working table implements staged control locally and has no separate upper-left EOS input." if limited_edition else "Official Pro dedicated-switch chart (PDF page 49, D-14) identifies this normally-closed contact as the upper-left flipper EOS; the LE chart on PDF page 55 leaves D-14 blank."),
		(86, 15, "Unused dedicated switch D15", "unused", "unknown", False, False, None),
		(85, 16, "Unused dedicated switch D16", "unused", "unknown", False, False, None),
		(-7, 17, "Pendulum tilt", "used", "tilt", False, False, None),
		(-6, 18, "Slam tilt", "optional", "tilt", True, False, None),
		(-5, 19, "Ticket notch", "optional", "microswitch", False, False, None),
		(-4, 20, "Unused dedicated switch D20", "unused", "unknown", False, False, None),
		(-3, 21, "Coin-door Back button", "used", "button", False, False, None),
		(-2, 22, "Coin-door Minus button", "used", "button", False, False, None),
		(-1, 23, "Coin-door Plus button", "used", "button", False, False, None),
		(0, 24, "Coin-door Select button", "used", "button", False, False, None),
	]
	items.extend(dedicated_switch(*spec) for spec in dedicated)
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE)})
	return items


PRO_OUTPUTS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Disc direction relay", "relay", "used"),
	4: ("Video game eject", "coil", "used"), 5: ("Disc motor power", "motor", "used"), 6: ("Recognizer three-bank motor relay", "motor", "used"),
	7: ("Orbit up/down post", "coil", "used"), 8: ("Shaker motor", "motor", "optional"), 9: ("Left pop bumper", "coil", "used"),
	10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"), 12: ("Upper-left flipper", "coil", "used"),
	13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"), 15: ("Left flipper", "coil", "used"),
	16: ("Right flipper", "coil", "used"), 17: ("Zen flasher", "flasher", "used"), 18: ("Video game flasher", "flasher", "used"),
	19: ("Back center flasher", "flasher", "used"), 20: ("Bottom arch left flasher", "flasher", "used"), 21: ("Bottom arch right flasher", "flasher", "used"),
	22: ("Lower left flasher", "flasher", "used"), 23: ("Lower right flasher", "flasher", "used"), 24: ("Coin meter", "coil", "optional"),
	25: ("Back left flasher", "flasher", "used"), 26: ("Disc left flasher", "flasher", "used"), 27: ("Disc right flasher", "flasher", "used"),
	28: ("Backpanel flashers x2", "flasher", "used"), 29: ("Recognizer flasher", "flasher", "used"), 30: ("Disc motor relay", "relay", "used"),
	31: ("Red disc left flashers x2", "flasher", "used"), 32: ("Red disc right flashers x2", "flasher", "used"),
}
LE_OUTPUTS = PRO_OUTPUTS | {
	3: ("TRON four-bank drop-target reset", "coil", "used"),
	19: ("Left dome flashers x2", "flasher", "used"),
	22: ("Disc direction relay", "relay", "used"),
	23: ("Recognizer motor relay", "relay", "used"),
	25: ("Right dome flashers x2", "flasher", "used"),
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J8-P11", "J8-P12", "J8-P14", "J8-P15", "J8-P16", "J8-P17", "J8-P18", "J8-P19", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def coil_wiring(address: int, limited_edition: bool) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address == 8:
		power_wire, connection, voltage, voltage_type = "RED-WHT", "J17-P7", 16, "ac"
	elif address in {15, 16}:
		power_wire, connection, voltage, voltage_type = ("GRY-YEL / RED-YEL", "J10-P6/7", 50, "dc") if address == 15 else ("BLU-YEL / RED-YEL", "J10-P6/7", 50, "dc")
	elif address == 12:
		power_wire, connection, voltage, voltage_type = "BLU-BRN", "J10-P6/7", 50, "dc"
	elif address in {5, 6, 30} or address == 3 and not limited_edition or address in {22, 23} and limited_edition:
		power_wire, connection, voltage, voltage_type = "BRN", "J7-P1", 20, "dc"
	elif address <= 16:
		power_wire, connection, voltage, voltage_type = "YEL-VIO", "J10-P9/10", 50, "dc"
	elif address == 24:
		power_wire, connection, voltage, voltage_type = "RED", "J16-P4-8", 5, "dc"
	else:
		power_wire, connection, voltage, voltage_type = "ORG", "J6-P10", 20, "dc"
	wiring.update({"power_wire": power_wire, "power_connection": connection, "nominal_voltage_v": voltage, "voltage_type": voltage_type})
	return wiring


def main_outputs(limited_edition: bool) -> list[dict[str, object]]:
	outputs = LE_OUTPUTS if limited_edition else PRO_OUTPUTS
	items = []
	for address, (label, kind, availability) in outputs.items():
		physical: dict[str, object] | None = None
		if address == 24:
			physical = {"notes": "Optional 5 VDC coin meter circuit."}
		elif limited_edition and address in {19, 25}:
			physical = {"notes": "Resolved source disagreement: the official LE coil chart on PDF page 57 labels output 19 as right domes x2 and output 25 as left domes x2, while the proven VPX callbacks label 19 left and 25 right. The project-wide source policy gives the known-working VPX script precedence for controller-facing semantics, so this definition uses 19 left and 25 right; authors should preserve both source locators when orienting the physical assemblies."}
		elif address == 30:
			physical = {"notes": "Physical disc-motor relay. The proven VPX table simplifies disc motion under output 5 and routes output 30 only to a visual effect; a physical recreation must retain this relay."}
		source_refs = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE) if limited_edition else (MANUAL_SOURCE, CORE_SOURCE)
		items.append(output(address, label, kind, availability, source_refs, manual_address=str(address), physical=physical, wiring=coil_wiring(address, limited_edition)))
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, runtime_source), physical={"notes": "PinMAME synthetic SAM fast-flip game-on output; no physical Q33 device."}, output_id="virtual.game-on"))
	items.append(output(34, "Unused VPX upper-left flipper compatibility callback", "virtual", "unused", (VPX_SOURCE, CORE_SOURCE), physical={"notes": "The proven script contains a commented-out SolCallback(34) compatibility hook and instead calls SolULFlipper directly from its local staged-flipper key handlers. Its physical upper-left flipper remains I/O Power Driver output 12. PinMAME's legacy scalar SAM getter aliases addresses 33-36 to the synthetic game-on bit when modulated-flipper handling is inactive, and the exact runtime traces observe only public game-on 33; do not build or wire a second flipper coil at 34."}, output_id="virtual.unused-upper-left-flipper-compatibility"))
	return items


PRO_LAMPS = {
	1: "Start button", 2: "Tournament start button", 3: "Shoot Again", 4: "Center Flynn", 5: "Center Gem", 6: "Center CLU", 7: "Center Zuse", 8: "Left outlane",
	9: "CLU C", 10: "ZUSE E", 11: "CLU L", 12: "CLU U", 13: "Right outlane", 14: "TRON N", 15: "TRON O", 16: "TRON R", 17: "TRON T",
	18: "TRON double scoring", 19: "Bumpers", 20: "Spinners", 21: "Center Portal", 22: "Center TRON", 23: "Center Recognizer", 24: "Center Light Cycle",
	25: "Center Disc", 26: "Center Quorra", 27: "Eject CLU", 28: "Eject Portal", 29: "Eject Quorra", 30: "Eject Light Cycle", 31: "Eject Extra Ball",
	32: "Right orbit CLU", 33: "ZUSE S", 34: "Right orbit Light Cycle", 35: "Flynn's Arcade", 37: "Right loop arrow", 38: "Right orbit Disc",
	39: "Right ramp Light Cycle", 40: "Left orbit CLU", 41: "ZUSE Z", 42: "Left ramp Light Cycle", 43: "ZUSE U", 44: "Recognizer three-bank",
	45: "Left inner loop CLU", 48: "Advance Quorra", 49: "Right inner loop Light Cycle", 50: "Right ramp Disc", 51: "Right inner loop Disc",
	52: "Right ramp arrow", 53: "Right inner loop arrow", 55: "Left inner loop Disc", 56: "Left inner loop arrow", 57: "Left ramp arrow",
	58: "Left ramp Disc", 59: "Left orbit Light Cycle", 60: "Left bumper", 61: "Right bumper", 62: "Bottom bumper",
	63: "Left inner loop Light Cycle", 64: "Left loop arrow", 66: "Left orbit Disc",
}
LE_LAMPS = {
	1: "TRON N", 2: "TRON O", 3: "TRON R", 4: "TRON T", 5: "TRON double scoring", 6: "Bumpers", 7: "Spinners", 8: "Left outlane",
	9: "CLU C", 10: "ZUSE U", 11: "Left ramp Light Cycle", 12: "ZUSE Z", 13: "Left orbit CLU", 14: "Left orbit Light Cycle", 15: "Left orbit Disc", 16: "Left loop arrow",
	17: "Center Portal", 18: "Center TRON", 19: "Center Recognizer", 20: "Center Light Cycle", 21: "Center Disc", 22: "Center Quorra", 23: "Center Zuse", 24: "Center CLU",
	25: "Center Gem", 26: "Shoot Again", 27: "Center Flynn", 28: "Eject CLU", 29: "ZUSE E", 30: "CLU L", 31: "CLU U", 32: "Right outlane",
	33: "Right loop arrow", 34: "Right orbit Disc", 35: "Right orbit Light Cycle", 36: "Right orbit CLU", 37: "Eject Extra Ball", 38: "Eject Light Cycle",
	39: "Eject Quorra", 40: "Eject Portal", 42: "Right ramp Light Cycle", 43: "ZUSE S", 45: "Flynn's Arcade", 46: "Left bumper", 47: "Right bumper", 48: "Bottom bumper",
	49: "Left ramp arrow", 50: "Left ramp Disc", 51: "Recognizer right", 52: "Recognizer center", 53: "Recognizer left", 54: "Recognizer three-bank",
	55: "Right ramp Disc", 56: "Right ramp arrow", 57: "Right inner loop arrow", 58: "Right inner loop Disc", 59: "Right inner loop Light Cycle",
	60: "Advance Quorra", 61: "Left inner loop CLU", 62: "Left inner loop Light Cycle", 63: "Left inner loop Disc", 64: "Left inner loop arrow",
	65: "Start button", 66: "Tournament start button",
}
RGB_LAMPS = {101: "Right ramp blue", 102: "Right ramp green", 103: "Right ramp red", 104: "Left ramp blue", 105: "Left ramp green", 106: "Left ramp red"}


def lamps(limited_edition: bool) -> list[dict[str, object]]:
	manual_lamps = LE_LAMPS if limited_edition else PRO_LAMPS
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	items = []
	for address in range(1, 81):
		label = manual_lamps.get(address, f"Unused lamp {address}")
		availability = "used" if address in manual_lamps else "unused"
		physical = {"notes": "Factory LED on Limited Edition."} if limited_edition and availability == "used" else {"notes": "Factory LED on Pro; other populated Pro matrix lamps use incandescent #555 lamps."} if address in {60, 61, 62} else None
		used_sources = (MANUAL_SOURCE, VPX_SOURCE, runtime_source) if limited_edition else (MANUAL_SOURCE, runtime_source)
		items.append(output(address, label, "lamp", availability, used_sources if availability == "used" else (MANUAL_SOURCE,), "pinmame.output.lamp", str(address), physical, output_id=f"lamp.{slug(label)}-{address}"))
	for address, label in RGB_LAMPS.items():
		availability = "used" if limited_edition else "unused"
		notes = "PinMAME serializes the tricolor board as two B/G/R public triples. The proven table reverses each BGR triplet when calling its RGB helper; PinMAME source identifies 101-103 as right and 104-106 as left."
		if not limited_edition:
			notes += " Pro firmware shares the public compatibility channels, but the factory Pro lacks the LE tricolor ramp assembly."
		items.append(output(address, label if limited_edition else f"Unpopulated Pro channel {address} ({label})", "lamp", availability, (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE, runtime_source) if limited_edition else (MANUAL_SOURCE, CORE_SOURCE), "pinmame.output.lamp", physical={"notes": notes}, output_id=f"lamp.rgb-{address}-{slug(label)}"))
	items.append(output(0, "General illumination master", "gi", "used", (MANUAL_SOURCE, VPX_SOURCE, runtime_source), "pinmame.output.gi", "GI-0", output_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions:
		result["positions"] = positions
	return result


def mechanisms(limited_edition: bool) -> list[dict[str, object]]:
	s = (MANUAL_SOURCE, VPX_SOURCE)
	items = [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right", "switch.trough-jam"], "Four balls initialize on switches 18-21, left to right. Output 1 ejects from the right end through jam opto 22; the proven table fires at 90 degrees with force 8 and briefly pulses 22 after release.", s),
		mechanism("mechanism.auto-launcher", "Auto launcher and manual plunger", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 fires a ball held at shooter-lane switch 23. The proven recreation retains the manual plunger and uses impulse power 150, time 0.7, and random variation 0.3.", s),
		mechanism("mechanism.video-game-eject", "Flynn's video-game eject", "kicker", ["device.video-game-eject"], ["switch.video-game-eject"], "Switch 11 stays active while a ball is held. Output 4 ejects toward 200 degrees with force 24, Z 0.4, and force variation 2 in the proven table.", s),
		mechanism("mechanism.recognizer-bank", "Motorized Recognizer three-target bank", "motorized", ["device.recognizer-three-bank-motor-relay"], ["switch.recognizer-three-bank-left-target", "switch.recognizer-three-bank-center-target", "switch.recognizer-three-bank-right-target", "switch.recognizer-three-bank-down", "switch.recognizer-three-bank-up"], "Output 6 toggles the three-target bank between raised and lowered endpoints. Switch 53 is active fully up and clears near the start of downward travel; switch 52 becomes active fully down. The proven 29-step model moves targets from Z -20 to -76, disables their collision near the lower endpoint, and initializes down on switch 52.", s, [{"id": "position.up", "label": "Raised and hittable", "sensors": ["switch.recognizer-three-bank-up"]}, {"id": "position.down", "label": "Lowered", "sensors": ["switch.recognizer-three-bank-down"]}]),
		mechanism("mechanism.orbit-post", "Orbit up/down post", "gate", ["device.orbit-up-down-post"], [], "Output 7 raises the post while asserted and drops it when clear. It initializes dropped and has no endpoint switch; nearby orbit and loop inputs report ball travel, not post position.", s, [{"id": "position.down", "label": "Dropped", "sensors": []}, {"id": "position.up", "label": "Raised", "sensors": []}]),
		mechanism("mechanism.disc", "Rinzler spinning identity disc", "rotary", ["device.disc-motor-power", "device.disc-direction-relay", "device.disc-motor-relay"], ["switch.disc-opto"], "Output 5 enables disc power, the edition-specific direction relay is output 22 on LE and output 3 on Pro, and output 30 is the physical motor relay. The proven table simplifies this to output 5 plus direction state, uses maximum turntable speed 8, starts at direction step +40, reverses to -40, and decelerates by 0.1 per 10 ms tick. Preserve rotating ball contact so the disc can carry and throw balls; switch 41 is the disc-area opto, not a motor index.", s),
		mechanism("mechanism.flippers", "Three-flipper assembly", "other", ["device.left-flipper", "device.right-flipper", "device.upper-left-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"] + ([] if limited_edition else ["switch.upper-left-flipper-button", "switch.upper-left-flipper-end-of-stroke"]), "Outputs 15/16 drive the lower left/right flippers and output 12 drives the upper-left flipper used to reach the right ramp. Pro has dedicated upper-left button/EOS inputs D13/D14 (public 88/87). LE leaves D13/D14 unpopulated; its proven table stages the upper flipper from the left control or a separate authoring key. Lower EOS contacts 83/81 and Pro upper EOS 87 are normally closed.", s),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Left, right, and bottom output/switch pairs are 9/30, 10/31, and 11/32.", s),
		mechanism("mechanism.slingshots", "Two slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left and right output/switch pairs are 13/26 and 14/27.", s),
		mechanism("mechanism.ramps-orbits-loops", "Ramps, orbits, loops, and spinners", "other", [], ["switch.right-ramp-exit", "switch.left-ramp-entrance", "switch.right-orbit-spinner", "switch.left-ramp-exit", "switch.right-ramp-entrance", "switch.right-inner-loop", "switch.left-orbit", "switch.left-spinner", "switch.right-orbit"], "Right ramp exit is 34; left ramp entrance/exit 35/37; right ramp entrance 38; right inner loop 39; left/right orbits 43/46; and right/left spinners 36/44. The two light-cycle ramps are independently illuminated by the LE tricolor board; use the manual location drawings for unsensed path geometry.", s),
		mechanism("mechanism.targets-and-lanes", "CLU lanes, ZUSE targets, Zen rollover, and outlanes", "other", [], ["switch.zuse-z-target", "switch.zuse-u-target", "switch.zuse-e-target", "switch.zuse-s-target", "switch.clu-l-lane", "switch.clu-c-lane", "switch.clu-u-lane", "switch.zen-rollover", "switch.left-outlane", "switch.right-outlane"], "ZUSE standup targets are 7/8/13/48. The physical location drawing and sustained Hit/UnHit handlers identify CLU L/C/U 14/25/28 as ball lanes rather than pulsed standup targets. Zen rollover is 12 and outlanes are 24/29.", s),
		mechanism("mechanism.optional-shaker", "Optional shaker motor", "motorized", ["device.shaker-motor"], [], "Output 8 is the optional 16 VAC shaker installation and may be absent from a stock machine.", s),
	]
	if limited_edition:
		items.extend([
			mechanism("mechanism.tron-drop-bank", "TRON four-bank drop targets", "drop_target_bank", ["device.tron-four-bank-drop-target-reset"], ["switch.tron-n-target", "switch.tron-o-target", "switch.tron-r-target", "switch.tron-t-target"], "Switches 1-4 latch as the four TRON targets fall. Output 3 resets the entire bank. The proven table initializes targets in physical N/O/R/T object order mapped back to controller addresses 1/2/3/4.", s, [{"id": "position.up", "label": "Targets raised", "sensors": []}, {"id": "position.down", "label": "Individual target down", "sensors": ["switch.tron-n-target", "switch.tron-o-target", "switch.tron-r-target", "switch.tron-t-target"]}]),
			mechanism("mechanism.recognizer-toy", "Motorized Recognizer toy", "motorized", ["device.recognizer-motor-relay"], ["switch.recognizer-motor-position-1", "switch.recognizer-motor-position-2", "switch.recognizer-motor-position-3"], "Output 23 enables the LE Recognizer sweep. The proven table oscillates between approximately -20 and +20 degrees, activating switch 54 at +18, switch 55 around center, and switch 56 at -18; it initializes centered on 55. Use endpoint cutoff and preserve unsensed motion between the three narrow windows.", s, [{"id": "position.1", "label": "+18-degree endpoint", "sensors": ["switch.recognizer-motor-position-1"]}, {"id": "position.center", "label": "Center", "sensors": ["switch.recognizer-motor-position-2"]}, {"id": "position.3", "label": "-18-degree endpoint", "sensors": ["switch.recognizer-motor-position-3"]}]),
		])
	else:
		items.append(mechanism("mechanism.tron-standups", "TRON four-bank standup targets", "other", [], ["switch.tron-n-target", "switch.tron-o-target", "switch.tron-r-target", "switch.tron-t-target"], "The Pro uses four fixed standup targets on switches 1-4. It has no reset output; output 3 is reassigned to disc direction. Do not import the LE drop-target motion or reset coil.", (MANUAL_SOURCE,)))
	return items


LE_DRIVER_IDS = {driver_id for driver_id, driver in DRIVERS.items() if "Limited Edition" in driver["description"]}
PRO_DRIVER_IDS = set(DRIVERS) - LE_DRIVER_IDS
if LE_DRIVER_IDS != {"trn_100h", "trn_110h", "trn_130h", "trn_140h", "trn_174h"} or PRO_DRIVER_IDS != {"trn_110", "trn_120", "trn_140", "trn_150", "trn_160", "trn_170", "trn_174", "trn_17402"}:
	raise ValueError("TRON drivers must classify exhaustively as Pro or Limited Edition")


def driver_records(limited_edition: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id in LE_DRIVER_IDS if limited_edition else PRO_DRIVER_IDS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision for the Limited Edition physical playfield." if limited_edition else "Firmware revision for the Pro physical playfield; the PinMAME LE clone root records software lineage only."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(limited_edition: bool) -> list[dict[str, object]]:
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	raw_hash = "92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f" if limited_edition else "51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490"
	rom_hash = "7ae5392a3bf6f9a7d282bf3ca002eea00a84ffd8cf39ff9af2e77a75e0eac44b" if limited_edition else "610e8fc71fdd83a94748ebe8691aeaa5964986e2d236ce6b7c46ed13602ff772"
	game = "trn_174h" if limited_edition else "trn_174"
	ipdb_id = 5707 if limited_edition else 5682
	ipdb_source = LE_IPDB_SOURCE if limited_edition else PRO_IPDB_SOURCE
	return [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/Tron-Manual.pdf", "sha256": "1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84", "locator": "Official 111-page scanned Stern manual: Pro switches/coils/lamps PDF pages 49/51/53, LE pages 55/57/59, location maps on following pages, major assemblies 1-30, and wiring 93-111", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "Tron-Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T23:21:40.923848Z"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Tron%20Legacy%20LE%20(Stern%202011)%20VPMmod%20v1.1.4.vbs", "revision": VPX_REVISION, "sha256": "d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc", "locator": "Known-working trn_174h script: four-ball initialization, eject and launcher constants, drop bank, target-bank travel, Recognizer positions, disc and post callbacks, staged upper flipper, and BGR ramp-light consumption", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c TRON driver family, SAM_5COL+1 custom lamp column, tricolor board C/D strobes, fast-flip addresses, GI 0, game-on 33, and 128x32 DMD", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames trn_ records and clone graph", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": STERN_SOURCE, "kind": "human_review", "uri": "https://sternpinball.com/game/tron/", "locator": "Manufacturer product identity and common feature inventory: two ramps, motorized Recognizer target bank, spinning identity disc, three flippers, and licensed presentation", "license": "NOASSERTION", "attribution": "Stern Pinball", "acquired_at": "2026-08-02T23:00:00Z"},
		{"id": ipdb_source, "kind": "human_review", "uri": f"https://www.ipdb.org/machine.cgi?id={ipdb_id}", "locator": f"Physical product identity for Stern Disney TRON Legacy {'Limited Edition, IPDB 5707, model I-00C2' if limited_edition else 'first-edition Pro, IPDB 5682, model I-00B9'}", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-02T23:00:00Z"},
		{"id": runtime_source, "kind": "runtime_scenario", "uri": f"external:pinmame-game-code/tron-legacy-{'limited-edition' if limited_edition else 'pro'}/harness/boot-start.raw.json", "revision": PINMAME_REVISION, "sha256": raw_hash, "locator": f"Exact {game} boot/start scenario with switches 18-21 and target bank down 52 initialized, four coin pulses, and start; LE also initializes Recognizer center 55; ROM archive SHA-256 {rom_hash}", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build(limited_edition: bool) -> dict[str, object]:
	machine_id = "stern.tron-legacy-limited-edition.2011" if limited_edition else "stern.tron-legacy-pro.2011"
	name = "TRON: Legacy Limited Edition" if limited_edition else "TRON: Legacy Pro"
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": machine_id, "name": name, "manufacturer": "Stern", "year": 2011, "kind": "physical_pinball", "model_number": "I-00C2" if limited_edition else "I-00B9", "ipdb_id": 5707 if limited_edition else 5682},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(limited_edition), "inputs": inputs(limited_edition), "outputs": main_outputs(limited_edition) + lamps(limited_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, runtime_source)}],
		"mechanisms": mechanisms(limited_edition), "relationships": [], "sources": sources(limited_edition),
		"knowledge": {"path": f"knowledge/stern/tron-legacy-{'limited-edition' if limited_edition else 'pro'}-2011.md", "status": "complete"}, "conflicts": [],
	}


PRO_KNOWLEDGE = """# TRON: Legacy Pro (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, wiring, mechanisms, initial state, and edition boundary validated**

## Identity and evidence precedence

This definition covers non-`h` drivers `trn_110`, `trn_120`, `trn_140`, `trn_150`, `trn_160`, `trn_170`, `trn_174`, and `trn_17402`. PinMAME roots them under LE firmware for software lineage, but they run the physically different Pro playfield. The official Pro service charts govern installed hardware and wiring. The known-working LE script is ground truth only for shared callbacks, motion, ball routing, and controller behavior; no LE-only device is projected onto Pro. IPDB 5682 identifies this first-edition Pro product as model I-00B9.

## Initial balls, launcher, and eject

Four balls occupy trough switches 18-21. Output 1 ejects through jam opto 22 toward shooter switch 23; the proven table uses 90 degrees and force 8. Output 2 drives the auto launcher while retaining a manual plunger. Flynn's video-game eject holds on switch 11 and output 4 ejects at 200 degrees, force 24, Z 0.4, with variance 2.

## Pro TRON bank and Recognizer bank

Pro switches 1-4 are fixed TRON standups, not drop targets. Output 3 is therefore the disc-direction relay and must not reset or animate them. The common three-target Recognizer bank uses hit switches 49-51, output 6, down switch 52, and up switch 53. The proven 29-step recreation starts down, raises targets to Z -20, lowers them to -76, and removes target collisions near the lower endpoint. Pro has no separate moving Recognizer toy and switches 54-56/output 23 retain their Pro service-chart meanings instead of the LE motion system.

## Spinning disc and orbit post

The Rinzler identity disc is a real rotating ball-contact surface. Output 5 supplies disc power, output 3 selects direction, and output 30 is the physical motor relay. Switch 41 is the disc-area opto, not an index sensor. The proven recreation uses maximum turntable speed 8, direction steps ±40, a 10 ms motion timer, and 0.1-per-tick coast-down. Output 7 raises the orbit post while active and drops it while clear; there is no post endpoint sensor.

## Flippers and playfield routes

Output 12 drives the upper-left flipper used for the right ramp. The official Pro dedicated-switch chart on PDF page 49 identifies D13/D14 public 88/87 as its button and normally-closed EOS; the LE chart on PDF page 55 leaves both contacts blank. The proven script's commented output-34 compatibility hook is not another coil: local staged-flipper key handlers directly call `SolULFlipper`, while physical output 12 remains authoritative. Lower flippers are 15/16 with button/EOS pairs 84/83 and 82/81. Ramps use switches 34/35/37/38, right inner loop 39, orbits 43/46, and spinners 36/44. CLU lanes are 14/25/28, ZUSE targets 7/8/13/48, Zen rollover 12, and outlanes 24/29. Pops pair 9/30, 10/31, 11/32; slings pair 13/26 and 14/27.

## Lighting and edition boundary

The Pro lamp map is physically different from LE: 1-35, 37-45, 48-53, 55-64, and 66 are populated; 36, 46, 47, 54, and 65 are unused. Start/Tournament are 1/2. Bumper lamps 60-62 are factory LEDs; the other populated Pro matrix positions use #555 lamps. Public custom channels 101-106 exist through the common PinMAME TRON transport but the stock Pro lacks the LE tricolor ramp assembly, so they are explicit unpopulated channels. Do not import the LE four-drop reset, moving Recognizer/sensors, LED lamp numbering, dome mapping, or ramp-light hardware.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, Flynn eject, fixed TRON standups, two-position Recognizer target bank, rotating disc with physical ball interaction, orbit post, three flippers with all Pro button/EOS contacts, pops, slings, ramps, loops, orbits, spinners, CLU/ZUSE targets, Zen rollover, and every flasher group.
- Preserve target-bank collision enablement, disc friction/throw, held-ball states, unsensed post motion, and the upper-flipper shot geometry. Cosmetic animation is insufficient.
- Bind all 64 matrix inputs, dedicated/DIP spaces, physical outputs 1-32, synthetic game-on 33, explicit unused VPX compatibility address 34, lamps 1-80 plus explicit 101-106 compatibility channels, GI 0, and the 128x32 four-bit DMD.

## Sources

- `manual.tron-legacy-pro-le.2011`: official Stern manual, SHA-256 `1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84`; Pro switches/coils/lamps PDF pages 49/51/53 and location maps 50/52/54.
- `vpx.tron-legacy-le-vpm-1.1.4`: known-working shared-hardware reference at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc`.
- `runtime.tron-legacy-pro.boot-start`: exact `trn_174` harness with the shared target bank initialized down on switch 52, SHA-256 `51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM transport, driver family, DMD, GI, tricolor address allocation, and game-on output.
"""


LE_KNOWLEDGE = """# TRON: Legacy Limited Edition (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, initial state, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `trn_100h`, `trn_110h`, `trn_130h`, `trn_140h`, and `trn_174h`. The exact `trn_174h` VPW-derived script is ground truth for controller callbacks, initial state, motion, and ball routing. The official LE service charts govern physical inventory and wiring. Pinned PinMAME governs public SAM serialization, the custom tricolor column, GI 0, synthetic game-on 33, and the native 128x32 four-bit DMD. IPDB 5707 identifies the Limited Edition as model I-00C2.

## Initial balls, launcher, and eject

Four balls initialize on trough switches 18-21. Output 1 ejects through jam opto 22, output 2 auto-launches from shooter switch 23, and the manual plunger remains functional. Flynn's video-game eject holds at switch 11; output 4 uses the proven 200-degree, force-24, Z-0.4 path with variance 2.

## Four-drop bank and motorized Recognizer systems

TRON switches 1-4 are a resettable four-bank on LE and output 3 raises all four. Separately, output 6 toggles the three-target Recognizer bank on switches 49-51 between down switch 52 and up switch 53. The proven 29-step model initializes down, removes collisions near Z -76, and restores targets at Z -20. Output 23 runs the moving Recognizer toy: switch 54 activates near +18 degrees, 55 near center, and 56 near -18 while the toy oscillates between about ±20. Initialize the toy centered on 55 and the target bank down on 52.

## Spinning disc and orbit post

The Rinzler disc uses output 5 for power, output 22 for direction, and output 30 for its physical relay. The working table simplifies output 30 to a visual effect, but a physical recreation must retain it. Use the proven maximum speed 8, ±40 direction steps, 10 ms updates, and 0.1 coast-down as a motion baseline. The disc must impart velocity to balls; switch 41 is the disc-area opto. Output 7 raises the unsensed orbit post while active and drops it when clear.

## Three flippers and edition-specific controls

Outputs 15/16 drive lower left/right and output 12 drives upper-left. Lower button/EOS inputs are 84/83 and 82/81 with normally-closed EOS contacts. The official LE dedicated-switch chart on PDF page 55 leaves D13/D14 blank despite the upper flipper; the Pro chart on PDF page 49 explicitly populates them. The proven table stages the LE upper flipper from the left control by default or a separate authoring key. Its `SolCallback(34)` line is commented out and the key handlers call `SolULFlipper` directly, so public 34 is retained only as an explicit unused compatibility artifact. Do not invent physical public 88/87 contacts or a second output-34 coil for LE.

## Lighting

LE ordinary lamps are factory LEDs with its own map: 1-40, 42-43, and 45-66 are populated; 41, 44, and 67-80 are unused. The tricolor board adds right ramp public B/G/R 101/102/103 and left ramp B/G/R 104/105/106. The script proves channel order by passing each triplet in reverse to an RGB helper; PinMAME source proves which C/D strobe belongs to each side. A resolved source disagreement remains explicit: the official coil chart on PDF page 57 says 19 right domes and 25 left, while the proven VPX callbacks say 19 left and 25 right. Per the project-wide ground-truth policy the working script wins for controller-facing semantics, so this definition uses 19 left and 25 right while retaining both locators for physical orientation.

## Routes and remaining devices

Ramps use 34/35/37/38, right inner loop 39, left/right orbits 43/46, and spinners 36/44. The physical location drawing and sustained VPX handlers identify CLU L/C/U 14/25/28 as lanes; ZUSE standup targets are 7/8/13/48, Zen rollover 12, and outlanes 24/29. Pops pair 9/30, 10/31, 11/32; slings 13/26 and 14/27. Output 8 is an optional 16 VAC shaker and output 24 an optional 5 V coin meter.

## Author construction checklist

- Build the typed four-ball state, launcher and manual plunger, Flynn eject, TRON drop bank, moving three-target bank, independent moving Recognizer with three sensors, disc power/direction/relay and physical ball contact, orbit post, three staged flippers, all routes/targets, flashers, ordinary LEDs, and both tricolor ramp assemblies.
- Preserve held-ball states, target-bank collision gating, endpoint cutoff, Recognizer transit, disc friction/throw and coast-down, and the upper-flipper shot. Do not collapse the two Recognizer mechanisms into one animation.
- Bind the complete explicit input/output spaces, including unused contacts, public RGB 101-106, synthetic game-on 33, GI 0, and the DMD.

## Sources

- `manual.tron-legacy-pro-le.2011`: official Stern manual, SHA-256 `1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84`; LE switches/coils/lamps PDF pages 55/57/59 and location maps 56/58/60.
- `vpx.tron-legacy-le-vpm-1.1.4`: exact known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc`.
- `runtime.tron-legacy-limited-edition.boot-start`: exact `trn_174h` harness, SHA-256 `92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM transport, custom lamp column, driver family, DMD, GI, and game-on output.
"""


PRO_LAMPS_SEEN = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66]
LE_LAMPS_SEEN = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 101, 102, 103, 104, 105, 106]


def runtime_evidence(limited_edition: bool) -> dict[str, object]:
	game = "trn_174h" if limited_edition else "trn_174"
	machine_id = "stern.tron-legacy-limited-edition.2011" if limited_edition else "stern.tron-legacy-pro.2011"
	raw_hash = "92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f" if limited_edition else "51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490"
	rom_hash = "7ae5392a3bf6f9a7d282bf3ca002eea00a84ffd8cf39ff9af2e77a75e0eac44b" if limited_edition else "610e8fc71fdd83a94748ebe8691aeaa5964986e2d236ce6b7c46ed13602ff772"
	extra_initial = "--initial-switch 55 " if limited_edition else ""
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": [machine_id], "driver_ids": [game],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": game, "command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 52 {extra_initial}--pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>", "rom_archive_sha256": rom_hash, "raw_runs": [{"name": "boot-start", "sha256": raw_hash, "self_test_pulses": 0}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": LE_LAMPS_SEEN if limited_edition else PRO_LAMPS_SEEN, "solenoid_addresses_seen": [6, 33] if limited_edition else [6, 24, 33], "gi_addresses_seen": [0]}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/tron-legacy-{'limited-edition' if limited_edition else 'pro'}/harness", "sha256": raw_hash, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def main() -> None:
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/tron-legacy-pro-2011.json"), fail_closed_spatial_partial(build(False)))
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/tron-legacy-limited-edition-2011.json"), fail_closed_spatial_partial(build(True)))
	write_json(ROOT / "evidence/runtime/sam/tron-legacy-pro-boot-start.json", runtime_evidence(False))
	write_json(ROOT / "evidence/runtime/sam/tron-legacy-limited-edition-boot-start.json", runtime_evidence(True))
	write_text(ROOT / "knowledge/stern/tron-legacy-pro-2011.md", fail_closed_spatial_knowledge("stern.tron-legacy-pro.2011", PRO_KNOWLEDGE))
	write_text(ROOT / "knowledge/stern/tron-legacy-limited-edition-2011.md", fail_closed_spatial_knowledge("stern.tron-legacy-limited-edition.2011", LE_KNOWLEDGE))


if __name__ == "__main__":
	main()
