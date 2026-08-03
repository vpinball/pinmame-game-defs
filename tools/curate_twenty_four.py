"""Build the reviewed, author-ready Stern 24 machine definition."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("twenty4_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.stern-24-parts.2009"
SAM_REFERENCE_SOURCE = "manual.stern-sam-io-reference.2014"
VPX_SOURCE = "vpx.stern-24-2.3.1"
ROM_SOURCE = "rom.stern-24.twenty4-150"
IPDB_SOURCE = "ipdb.stern-24.5419"
STERN_SOURCE = "human-review.stern-24-product"
VPU_SOURCE = "human-review.vpu-stern-24-2.4"
RUNTIME_BOOT_SOURCE = "runtime.stern-24.boot-start"
RUNTIME_SWITCH_LOW_SOURCE = "runtime.stern-24-switch-diagnostic-1-17"
RUNTIME_SWITCH_HIGH_SOURCE = "runtime.stern-24-switch-diagnostic-22-64"
RUNTIME_COIL_SOURCE = "runtime.stern-24-coil-diagnostic"
RUNTIME_LAMP_SOURCE = "runtime.stern-24-lamp-diagnostic"
RUNTIME_SUITCASE_SOURCE = "runtime.stern-24-suitcase-motor-menu"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(dict.fromkeys(source_refs))}


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


# label, pulse, roles
SWITCHES: dict[int, tuple[str, bool, tuple[str, ...]]] = {
	1: ("House standup left", True, ()), 2: ("House standup right", True, ()),
	3: ("Safe House eject", False, ("ball.position",)), 4: ("Cell Phone target", True, ()),
	5: ("CHLOE C target", True, ()), 6: ("CHLOE H target", True, ()), 7: ("CHLOE L target", True, ()),
	8: ("CHLOE O target", True, ()), 9: ("CHLOE E target", True, ()), 10: ("Left-loop spinner", True, ()),
	11: ("House drop target left", False, ("position.down",)), 13: ("House drop target right", False, ("position.down",)),
	14: ("Left control gate", False, ()), 15: ("Tournament Start", False, ("cabinet.tournament-start",)),
	16: ("Start button", False, ("cabinet.start",)), 18: ("Trough 4 left", False, ("ball.position",)),
	19: ("Trough 3", False, ("ball.position",)), 20: ("Trough 2", False, ("ball.position",)),
	21: ("Trough 1 right", False, ("ball.position",)), 22: ("Trough jam", False, ("ball.position",)),
	23: ("Shooter lane", False, ("ball.position",)), 24: ("Left outlane", False, ()), 25: ("Left return lane", False, ()),
	26: ("Left slingshot", True, ()), 27: ("Right slingshot", True, ()), 28: ("Right return lane", False, ()),
	29: ("Right outlane", False, ()), 30: ("Left pop bumper", True, ()), 31: ("Right pop bumper", True, ()),
	32: ("Bottom pop bumper", True, ()), 33: ("MOLE two-bank left target", True, ()), 34: ("MOLE two-bank right target", True, ()),
	39: ("Right three-bank bottom target", True, ()), 40: ("Right three-bank middle target", True, ()),
	41: ("Right three-bank top target", True, ()), 43: ("Suitcase lock bottom", False, ("ball.position",)),
	44: ("Suitcase lock middle", False, ("ball.position",)), 45: ("Suitcase lock top", False, ("ball.position",)),
	46: ("Left orbit", False, ()), 48: ("Suitcase home", False, ("position.home",)), 54: ("Right orbit", True, ()),
	55: ("Left top lane", False, ()), 56: ("Center top lane", False, ()), 57: ("Right top lane", False, ()),
	58: ("Right ramp entrance", True, ()), 60: ("Single drop target left", False, ("position.down",)),
	61: ("Single drop target right", False, ("position.down",)), 62: ("Sniper target", True, ()),
}


def switch_id(number: int) -> str:
	label = SWITCHES[number][0] if number in SWITCHES else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int) -> dict[str, object]:
	spec = SWITCHES.get(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	physical: dict[str, object] = {"switch_type": "unknown"}
	if spec:
		physical["notes"] = "The exact factory contact construction is not established by Stern's partial parts book. The ROM diagnostic and proven table validate this semantic binding and its sustained/pulse behavior; choose a suitable physical sensor when recreating it."
	if number == 15:
		physical["switch_type"] = "button"
		physical["notes"] = "Physical Tournament Start cabinet button. A proven table script pulses this address as a software-only trough-release acknowledgement; never create a trough sensor at switch 15."
	elif number == 16:
		physical["switch_type"] = "button"
	if number in {43, 44, 45}:
		physical["notes"] += " Suitcase visible-lock contact. The proven table's corrected VLock mapping is physical bottom 43 to ROM 45, middle 44 to ROM 44, and top 45 to ROM 43. Keep the public ROM binding here and apply that ordering in the modeled lock."
	result: dict[str, object] = {
		"id": switch_id(number), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": False, "pulse": spec[1] if spec else False, "availability": "used" if spec else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(RUNTIME_SWITCH_LOW_SOURCE, RUNTIME_SWITCH_HIGH_SOURCE, VPX_SOURCE, SAM_REFERENCE_SOURCE),
	}
	if spec and spec[2]:
		result["roles"] = list(spec[2])
	return result


DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin chute", "Center coin chute", "Right coin chute", "Unused fourth coin chute", "Optional fifth coin chute", "Unused dedicated switch D6", "Unused Home switch", "Unused Away switch",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Unused dedicated switch D13", "Unused dedicated switch D14", "Unused dedicated switch D15", "Unused dedicated switch D16",
	"Pendulum tilt", "Slam tilt", "Optional ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "unknown", "button", "unknown", "unknown", "unknown", "button", "leaf", "button", "leaf", "unknown", "unknown", "unknown", "unknown", "tilt", "tilt", "microswitch", "unknown", "button", "button", "button", "button"]
DEDICATED_AVAILABILITY = ["used", "used", "used", "unused", "optional", "unused", "unused", "unused", "used", "used", "used", "used", "unused", "unused", "unused", "unused", "used", "used", "optional", "unused", "used", "used", "used", "used"]
DEDICATED_ROLES = {65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 69: "cabinet.coin.fifth", 84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}
DEDICATED_WIRES = [
	("PNK-BRN", "J2-P2"), ("PNK-RED", "J2-P3"), ("PNK-ORG", "J2-P4"), ("PNK-YEL", "J2-P6"), ("PNK-GRN", "J2-P7"), ("PNK-BLU", "J2-P8"), ("PNK-VIO", "J2-P9"), ("PNK-GRY", "J2-P10"),
	("GRY-BRN", "J3-P1"), ("GRY-RED", "J3-P2"), ("GRY-ORG", "J3-P4"), ("GRY-YEL", "J3-P5"), ("GRY-GRN", "J3-P6"), ("GRY-BLU", "J3-P7"), ("GRY-VIO", "J3-P8"), ("GRY-BLK", "J3-P9"),
	("LGN-BRN", "J13-P1"), ("LGN-RED", "J13-P3"), ("LGN-ORG", "J13-P4"), ("LGN-YEL", "J13-P5"), ("LGN-BLK", "J13-P6"), ("LGN-BLU", "J13-P7"), ("LGN-VIO", "J13-P8"), ("LGN-GRY", "J13-P9"),
]
DEDICATED_GROUNDS = [("BLK", "J2-P1/11")] * 8 + [("BLK", "J3-P10")] * 8 + [("BLK", "J13-P10")] * 8


def dedicated_id(number: int) -> str:
	return f"switch.d{number}-{slug(DEDICATED_LABELS[number - 1])}"


def dedicated_switch(number: int) -> dict[str, object]:
	index = number - 1
	device = DEDICATED_DEVICES[index]
	availability = DEDICATED_AVAILABILITY[index]
	result: dict[str, object] = {
		"id": dedicated_id(number), "label": DEDICATED_LABELS[index], "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device}, "aliases": aliases("pinmame.switch", device, f"D-{number}"),
		"normally_closed": number in {10, 12, 18}, "pulse": number in {1, 2, 3, 5}, "availability": availability,
		"physical": {"switch_type": DEDICATED_TYPES[index] if availability != "unused" else "unknown"},
		"wiring": {"board": "CPU/Sound board dedicated-switch input", "drive_wire": DEDICATED_WIRES[index][0], "drive_connection": DEDICATED_WIRES[index][1], "return_wire": DEDICATED_GROUNDS[index][0], "return_connection": DEDICATED_GROUNDS[index][1]},
		"provenance": provenance(SAM_REFERENCE_SOURCE, CORE_SOURCE),
	}
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	return result


def inputs() -> list[dict[str, object]]:
	items = [matrix_switch(number) for number in range(1, 65)]
	items.extend(dedicated_switch(number) for number in range(1, 25))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance(SAM_REFERENCE_SOURCE, CORE_SOURCE)})
	return items


# label, kind, availability
COILS: dict[int, tuple[str, str, str]] = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Safe House eject", "coil", "used"),
	4: ("Single drop target left reset", "coil", "used"), 5: ("Single drop target right reset", "coil", "used"),
	6: ("Left control gate", "coil", "used"), 7: ("Right control gate", "coil", "used"), 8: ("Optional shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	12: ("Safe House facade", "coil", "used"), 13: ("House two-bank reset", "coil", "used"), 14: ("Sniper facade", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"), 17: ("Left slingshot", "coil", "used"), 18: ("Right slingshot", "coil", "used"),
	19: ("Safe House flash x3", "flasher", "used"), 20: ("Sniper flash x2", "flasher", "used"), 21: ("Suitcase stepper drive Q21", "motor", "used"),
	22: ("Left ramp up-post", "coil", "used"), 23: ("Suitcase stepper drive Q23", "motor", "used"), 24: ("Optional 5 V controlled device", "coil", "optional"),
	25: ("Suitcase stepper drive Q25", "motor", "used"), 26: ("Pop bumper flash x3", "flasher", "used"), 27: ("Right-side flash", "flasher", "used"),
	28: ("Suitcase lock and release post", "coil", "used"), 29: ("Sniper up-post", "coil", "used"), 30: ("Suitcase stepper drive Q30", "motor", "used"),
	31: ("Slingshot flash x2", "flasher", "used"), 32: ("Left-spinner flash x3", "flasher", "used"),
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output_id(address: int) -> str:
	return f"device.{address}-{slug(COILS[address][0])}"


def coil_wiring(address: int) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address in set(range(1, 8)) | set(range(9, 15)):
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 8:
		wiring.update({"power_wire": "RED-WHT", "power_connection": "J17-P7", "nominal_voltage_v": 16, "voltage_type": "ac"})
	elif address == 15:
		wiring.update({"power_wire": "GRY-YEL via flipper feed", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 16:
		wiring.update({"power_wire": "BLU-YEL via flipper feed", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address in {17, 18, 22, 29}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4-8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	elif address in {19, 20, 26, 27, 28, 31, 32}:
		wiring.update({"power_wire": "ORG", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address in {21, 23, 25, 30}:
		wiring.update({"nominal_voltage_v": 24, "voltage_type": "dc"})
	return wiring


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, stable_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def main_outputs() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address, (label, kind, availability) in COILS.items():
		physical: dict[str, object] = {}
		if address == 8:
			physical["notes"] = "Optional factory shaker motor; ROM revision 1.44 added shaker code, but installation is not required."
		elif address == 24:
			physical["notes"] = "Common SAM optional 5 V controlled-device channel; no stock 24 playfield device is identified, so do not invent one."
		elif address in {21, 23, 25, 30}:
			physical["assembly_part_number"] = "511-5092-00"
			physical["part_number"] = "511-5072-00"
			physical["notes"] = "One of the four physical 24 V suitcase stepper drive positions listed by the proven VPX script comment at line 626, on cable 036-5634-11-A7. Their electrical phase order and individual supply-wire colors are not established, so the definition preserves Q addresses without assigning A/B/C/D names. The script registers only Q21 as its logical animation callback; Q23/Q25/Q30 remain physical drive positions rather than additional table callbacks."
		items.append(make_output(address, label, kind, availability, (RUNTIME_COIL_SOURCE, RUNTIME_SUITCASE_SOURCE, VPX_SOURCE, MANUAL_SOURCE, SAM_REFERENCE_SOURCE, ROM_SOURCE), manual_address=f"Q{address}", physical=physical, wiring=coil_wiring(address), stable_id=output_id(address)))
	items.append(make_output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, RUNTIME_BOOT_SOURCE), physical={"notes": "Synthetic SAM fast-flip game-on output with no physical Q33 device; public 34-36 are legacy query aliases, not devices."}, stable_id="virtual.game-on"))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused SAM auxiliary compatibility address {address}", "virtual", "unused", (CORE_SOURCE, ROM_SOURCE), physical={"notes": "24 uses SAM_NO_AUX. This is explicit public emulator capacity, not installed hardware."}, stable_id=f"virtual.aux-{address}"))
	return items


LAMPS = {
	1: "Start Button", 2: "Tournament Start Button", 3: "Shoot Again", 4: "Save the President", 5: "Master Agent", 6: "Super Jackpot", 7: "MOLE X: Right Orbit", 8: "Cell Phone", 9: "Not used",
	10: "CELL C", 11: "CELL E", 12: "CELL L left", 13: "CELL L right", 14: "Right three-bank top", 15: "Right three-bank middle", 16: "Right three-bank bottom",
	17: "Terrorists", 18: "Destroy Safe House", 19: "Safe Houses Multiball", 20: "Safe Houses Jackpot", 21: "Safe Houses Super Jackpot", 22: "Safe House Jackpot",
	23: "Lock 1", 24: "Lock 2", 25: "Suitcase Multiball", 26: "Suitcase Jackpot", 27: "Suitcase Super Jackpot", 28: "Nuke Jackpot", 29: "Fire Fight", 30: "Hurry Up",
	31: "Snipers Multiball", 32: "Snipers Jackpot", 33: "Snipers Super Jackpot", 34: "Sniper Jackpot", 35: "Scene 1", 36: "Scene 2", 37: "Scene 3", 38: "Scene 4", 39: "Scene 5", 40: "Scene 6",
	41: "CHLOE C", 42: "CHLOE H", 43: "CHLOE L", 44: "CHLOE O", 45: "CHLOE E", 46: "Left Loop arrow 24", 47: "Left Loop arrow red", 48: "Single drop left 24", 49: "Single drop right 24",
	50: "Escape", 51: "Right Ramp arrow 24", 52: "MOLE X: Suitcase", 53: "Right Ramp arrow red", 54: "Suitcase right", 55: "MOLE X: Dead End", 56: "Dead End arrow 24", 57: "Dead End arrow red",
	58: "Extra Ball", 59: "Sniper", 60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper", 63: "Right Loop arrow 24", 64: "Right Loop arrow red",
	65: "Safe House arrow left", 66: "Safe House arrow center", 67: "Safe House arrow right", 68: "Safe House arrow red", 69: "MOLE X: Safe House", 70: "Left Ramp arrow 24", 71: "Left Ramp arrow red",
	72: "CTU insert 1", 73: "CTU insert 2", 74: "CTU insert 3", 75: "CTU insert 4", 76: "MOLE insert 1", 77: "MOLE insert 2", 78: "MOLE insert 3", 79: "Suitcase left", 80: "Special",
}
LAMP_DRIVE = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]


def lamps() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address in range(1, 81):
		label = LAMPS[address]
		column = (address - 1) % 8
		row = (address - 1) // 8
		availability = "unused" if address == 9 else "used"
		physical: dict[str, object]
		if availability == "unused":
			physical = {"notes": "Unpopulated lamp-matrix address. The ROM Lamp Test explicitly labels it Not used; do not install a lamp."}
		else:
			physical = {"location": label, "notes": "Original 2009 incandescent matrix-lamp construction."}
		if address in range(72, 76):
			physical["notes"] += " The service diagnostic reports only CTU for all four addresses; the numeric suffix preserves unique bindings without claiming an unverified face order."
		elif address in range(76, 79):
			physical["notes"] += " The service diagnostic reports only MOLE for all three addresses; the numeric suffix preserves unique bindings without claiming an unverified face order."
		items.append(make_output(address, label, "lamp", availability, (RUNTIME_LAMP_SOURCE, VPX_SOURCE, SAM_REFERENCE_SOURCE), group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring={"board": "I/O Power Driver board lamp matrix", "drive_wire": LAMP_DRIVE[column][0], "drive_connection": LAMP_DRIVE[column][1], "return_wire": LAMP_RETURN[row][0], "return_connection": LAMP_RETURN[row][1]}, stable_id=f"lamp.{address}-{slug(label)}"))
	items.append(make_output(0, "General illumination master", "gi", "used", (VPX_SOURCE, RUNTIME_BOOT_SOURCE, CORE_SOURCE), group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Playfield general illumination", "notes": "PinMAME exposes the incandescent playfield GI as aggregate channel 0."}, stable_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None, assembly_part_number: str | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions is not None:
		result["positions"] = positions
	if assembly_part_number is not None:
		result["assembly_part_number"] = assembly_part_number
	return result


def mechanisms() -> list[dict[str, object]]:
	common = (VPX_SOURCE, MANUAL_SOURCE, IPDB_SOURCE, RUNTIME_SWITCH_LOW_SOURCE, RUNTIME_SWITCH_HIGH_SOURCE, RUNTIME_COIL_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", [output_id(1)], [switch_id(number) for number in range(18, 23)], "Four balls rest on switches 18-21. Q1 ejects the rightmost ball through jam switch 22 toward shooter switch 23. The proven table pulses physical Tournament Start switch 15 as a software bookkeeping shortcut during release; never build a trough sensor at 15.", common),
		mechanism("mechanism.auto-launch", "Manual shooter with auto launch", "kicker", [output_id(2)], [switch_id(23)], "A ball at shooter switch 23 can be launched manually or by Q2. Preserve both the manual plunger path and ROM-driven auto launch.", common),
		mechanism("mechanism.safe-house", "Exploding Safe House facade and eject", "toy", [output_id(3), output_id(12)], [switch_id(3)], "The ball enters the Safe House saucer at switch 3 and Q3 ejects it. Q12 flips the building front down/open to expose the interior and returns it upright/closed when disabled. IPDB documents internal flashers and miniature army men; model moving collision geometry, not only animation.", common, [{"id": "position.closed", "label": "Facade upright", "sensors": []}, {"id": "position.open", "label": "Facade flipped down", "sensors": []}]),
		mechanism("mechanism.house-drop-bank", "House two-bank drop targets", "drop_target_bank", [output_id(13)], [switch_id(11), switch_id(13)], "Two independently hit drop targets report switches 11/13. Q13 mechanically resets both targets upright.", common),
		mechanism("mechanism.suitcase", "Motorized suitcase and three-ball visible lock", "motorized", [output_id(number) for number in (21, 23, 25, 30, 28)], [switch_id(number) for number in (43, 44, 45, 48)], "Four physical drive positions Q21/Q23/Q25/Q30 energize the 24 V stepper motor through cable 036-5634-11-A7; the proven script documents all four in its Q21 callback comment but uses Q21 alone as the logical VPX animation trigger. Their A/B/C/D electrical order is not established and must be derived when wiring the chosen motor driver. Switch 48 is active only at suitcase home; it clears during motion and returns near home. Q28 controls the separate lock/release post. The suitcase can lock three balls while open or closed. The proven table moves its facade through an approximately 358-to-320-to-358 range and its corrected visible-lock ordering maps bottom physical 43 to ROM 45, middle 44 to 44, and top 45 to 43; preserve that mapping and actual ball containment.", common + (RUNTIME_SUITCASE_SOURCE, ROM_SOURCE,), [{"id": "position.home", "label": "Closed/home", "sensors": [switch_id(48)]}, {"id": "position.open", "label": "Open", "sensors": []}], "511-5092-00"),
		mechanism("mechanism.sniper-house", "Sniper House facade, target, and up-post", "toy", [output_id(14), output_id(29)], [switch_id(62)], "Q14 opens the Sniper House to reveal switch 62 and closes it to obscure the shot. Q29 raises or lowers the adjacent post. IPDB reports that the sniper figure waggles when firing; preserve the opening obstruction, revealed target, post collision, and figure motion.", common, [{"id": "position.closed", "label": "Sniper hidden", "sensors": []}, {"id": "position.open", "label": "Sniper revealed", "sensors": []}]),
		mechanism("mechanism.single-drop-targets", "Left and right single drop targets", "drop_target_bank", [output_id(4), output_id(5)], [switch_id(60), switch_id(61)], "Single drop switches 60/61 latch down when hit; Q4/Q5 reset the left/right targets independently. Along with the Sniper area, these targets can obscure and free shots, so their collision state must follow the physical target position.", common + (STERN_SOURCE,)),
		mechanism("mechanism.control-gates", "Left and right control gates", "gate", [output_id(6), output_id(7)], [switch_id(14)], "Q6/Q7 command the two route gates. Switch 14 senses the left gate/route contact used by the proven table; retain gate collision direction and sustained switch state rather than a cosmetic animation.", common),
		mechanism("mechanism.left-ramp-post", "Left-ramp up-post", "gate", [output_id(22)], [], "Q22 raises and lowers the left-ramp post. It has no public endpoint sensor, so the controller state is the command while the physical post collision must track travel.", common),
		mechanism("mechanism.flippers", "Lower flippers", "other", [output_id(15), output_id(16)], [dedicated_id(number) for number in (9, 10, 11, 12)], "Q15/Q16 drive the left/right flippers. Public button/EOS pairs are 84/83 and 82/81; both EOS contacts are normally closed.", common),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [output_id(9), output_id(10), output_id(11)], [switch_id(number) for number in (30, 31, 32)], "Left, right, and bottom pop pairs are Q9/SW30, Q10/SW31, and Q11/SW32.", common),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [output_id(17), output_id(18)], [switch_id(26), switch_id(27)], "Left and right slingshot pairs are Q17/SW26 and Q18/SW27.", common),
		mechanism("mechanism.shaker", "Optional shaker motor", "motorized", [output_id(8)], [], "Q8 drives the optional 16 VAC shaker. ROM v1.44 added shaker code; absence remains a valid cabinet configuration.", (ROM_SOURCE, RUNTIME_COIL_SOURCE, SAM_REFERENCE_SOURCE)),
		mechanism("mechanism.routes", "Ramp, orbit, spinner, and lane network", "other", [], [switch_id(number) for number in (10, 14, 24, 25, 28, 29, 46, 54, 55, 56, 57, 58)], "Switch 10 is the left-loop spinner; 46/54 are the left/right orbits; 58 is right-ramp entrance; 55-57 are top lanes; 24/25 and 29/28 are lower outlane/return pairs. The working table uses sustained Hit/UnHit state for route contacts and pulses spinner/fast triggers only.", common),
		mechanism("mechanism.fixed-targets", "Fixed standup target groups", "other", [], [switch_id(number) for number in (1, 2, 4, 5, 6, 7, 8, 9, 33, 34, 39, 40, 41)], "Fixed contacts comprise the House pair 1/2, Cell Phone 4, CHLOE bank 5-9, MOLE bank 33/34, and right three-bank 39-41. They are pulse targets and have no reset actuator.", common),
	]


EXPECTED_DRIVERS = {"twenty4_130", "twenty4_140", "twenty4_144", "twenty4_150"}
if set(DRIVERS) != EXPECTED_DRIVERS:
	raise ValueError("24 driver family must be covered exhaustively")


def driver_records() -> list[dict[str, object]]:
	selected = []
	for driver_id in EXPECTED_DRIVERS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision for the February 2009 physical product. PinMAME catalogs final V1.5 as 2010, but that software date does not create a new hardware edition."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources() -> list[dict[str, object]]:
	return [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://sternpinball.com/wp-content/uploads/2018/11/24Manual.pdf", "sha256": "c547202e54b3ffbe53ba955db9eed8d52a6fef4b4807416de2f31ccf18aaf71f", "locator": "Official 72-page partial Pink/Blue parts and assembly book. Custom assemblies are on PDF pages 39-47; suitcase motor assembly 511-5092-00 and 24 V stepper 511-5072-00 are on page 43. This is not a complete service I/O chart; pages 1-52 are image scans and later pages are generic appendices.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "24Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T04:08:34.2127718Z"},
		{"id": SAM_REFERENCE_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2022/06/IronMan_Vault_web.pdf", "sha256": "20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990", "locator": "Later official service manual for a machine using the same SAM CPU/Sound and I/O Power Driver boards. Used only for standardized SAM matrix, dedicated-input, lamp-matrix, Q-control connector pinouts, and supply topology; it is not evidence for any 24 game semantic or installed device.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "IronMan_Vault_web.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T03:02:35.240041Z"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/24%20%28Stern%202009%29%20v.2.3.1.vbs", "revision": VPX_REVISION, "sha256": "7bf550806bd87c17417a974ed75b1700885da883e0dce5ce31d7dc7ba6cc094f", "locator": "Known-working exact twenty4_150 table script: all switch handlers, four-ball trough, corrected suitcase lock mapping and animation, Safe House and Sniper facades, gates/posts, drop resets, flippers, flashers, lamps, and GI. Line 626 registers only SolCallback(21) as the logical animation trigger while its inline hardware comment explicitly lists suitcase motor solenoid positions 21, 23, 25, and 30; the unregistered positions are physical stepper drives, not separate VPX callbacks.", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c twenty4 INITGAME/driver family, SAM_NO_AUX, SAM public switch translation, synthetic game-on output, and 128x32 DMD.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames twenty4_ driver records and clone graph.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/twenty4_150.zip", "revision": "V1.5", "sha256": "f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4", "locator": "Read-only user-authorized archive. 24readme.txt SHA-256 128c6f5f6d73ca6324154df256a45b2d96f38cfcf009bbe0a2341ef36ed6359b documents suitcase positioning, shaker support, and post timing; 24_V1-5_E.BIN SHA-256 6678046c447b92a5965747a40035a13e312cc5f436ab13f0585267f65635ae17.", "license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external"},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=5419", "locator": "IPDB 5419 physical identity and February 2009 release; two flippers, three pops, two slings, 12 standups, four drops, spinner, kickout, and detailed suitcase/Safe House/Sniper toy behavior.", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T04:00:00Z"},
		{"id": STERN_SOURCE, "kind": "human_review", "uri": "https://www.sternpinball.com/game/24-2/", "locator": "Manufacturer feature inventory: three-ball suitcase lock, opening Sniper House, exploding Safe House, single Sniper drop targets, and multiball.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "acquired_at": "2026-08-03T04:25:47Z"},
		{"id": VPU_SOURCE, "kind": "human_review", "uri": "https://vpuniverse.com/files/file/20448-24-stern-2009/", "locator": "Authenticated review of current table release 2.4 for twenty4_150; release history preserves suitcase, Safe House, and Sniper fixes. Exact behavior is sourced from the pinned proven v2.3.1 script rather than this mutable page.", "license": "NOASSERTION", "attribution": "VPUniverse and table authors", "acquired_at": "2026-08-03T05:00:00Z"},
		{"id": RUNTIME_BOOT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/twenty4_150/harness/boot-start-v1/run.json", "revision": PINMAME_REVISION, "sha256": "a1fca511fbebd25e045af4e22e08505820e633c9be493808572b7245c85886db", "locator": "Exact twenty4_150 boot/start run with four occupied trough switches, six coin pulses, start, 128x32x4 DMD, game-on 33, GI 0, and observed lamp addresses.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_SWITCH_LOW_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/twenty4_150/harness/switch-matrix-1-17-held-v2/run.json", "revision": PINMAME_REVISION, "sha256": "d771050fab8d52590383899ca8f11ab8c59886730de25e1be07021ad76261b14", "locator": "ROM service Switch Test captured while switches 1-17 were held; validates semantic labels and unused positions, not factory contact construction.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_SWITCH_HIGH_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/twenty4_150/harness/switch-matrix-held-diagnostic-v1/run.json", "revision": PINMAME_REVISION, "sha256": "7f51c62f83f6933de08379fc7c65ed8bd6193c8ae474a972bdaf588fb282ad0d", "locator": "ROM service Switch Test captured while switches 22-64 were held; validates semantic labels and unused positions, not factory contact construction.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_COIL_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/twenty4_150/harness/coil-diagnostic-v1/run.json", "revision": PINMAME_REVISION, "sha256": "b37e8977dd1fb91cc27cae31ce995ff3cd825a7dfb9ceca9a5589f93be3fdcf0", "locator": "ROM Single Coil Test DMD sweep validates installed Q labels plus independent high-side power and low-side control wire colors. It explicitly shows Q17/Q18/Q22/Q29 on BRN high-side power, Q19/Q20/Q26-Q28/Q31/Q32 on ORG, Q24 on RED, and then skips Q21/Q23/Q25/Q30 before wrapping; the common SAM schematic maps BRN/ORG/RED supplies to J7-P1/J6-P10/J16-P4-8. High-side feed color is machine-harness evidence and need not follow the low-side Q control-connector bank.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_LAMP_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/twenty4_150/harness/lamp-diagnostic-v1/run.json", "revision": PINMAME_REVISION, "sha256": "a3a6d5277e56c833445a3fc3a69d774f3b1d494f4df6aea99bc858670a25f286", "locator": "ROM Single Lamp Test selector sweep through addresses 1-80 validates labels and explicitly marks address 9 Not used. Runtime evidence lamp_addresses_seen records this service selector sweep, not gameplay activity or physical population by itself.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_SUITCASE_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/twenty4_150/harness/suitcase-motor-menu-v1/run.json", "revision": PINMAME_REVISION, "sha256": "6d48aa7e63bd39eb339732888669768b1dcf584a1d51821b6d7a346ca809ea9b", "locator": "ROM auxiliary diagnostic menu visibly exposes a dedicated Suitcase Motor Test. This run validates the separate test's existence only; physical drive positions 21/23/25/30 come from the proven VPX line-626 comment and the ordinary coil test's matching decoder holes, not from an unrecorded actuation sequence.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.twenty-four.2009", "name": "24", "manufacturer": "Stern", "year": 2009, "kind": "physical_pinball", "ipdb_id": 5419},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(), "inputs": inputs(), "outputs": main_outputs() + lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, RUNTIME_BOOT_SOURCE)}],
		"mechanisms": mechanisms(), "relationships": [], "sources": sources(),
		"knowledge": {"path": "knowledge/stern/twenty-four-2009.md", "status": "complete"}, "conflicts": [],
	}


KNOWLEDGE = """# 24 (Stern, 2009)

Coverage: **author-ready - complete public I/O inventory, wiring, custom mechanisms, firmware variants, and recreation behavior validated**

## Identity and evidence precedence

This definition covers Stern's February 2009 physical machine and every PinMAME driver `twenty4_130`, `twenty4_140`, `twenty4_144`, and `twenty4_150`. PinMAME dates final V1.5 to 2010, but that is a firmware release date, not a second hardware product. The known-working `24 (Stern 2009) v.2.3.1.vbs` is the semantic ground truth for controller callbacks and physical causality. ROM service diagnostics validate labels and wire colors. Stern's partial Pink/Blue book validates physical assemblies but is not a complete service I/O manual; the later official Iron Man Vault manual is used only for standard connector pins on the same SAM boards. IPDB and Stern validate the physical toy behaviors.

## Balls, trough, and shooter

The machine has four balls resting on trough switches 18-21. Q1 feeds through jam switch 22 to shooter switch 23, where the player can plunge manually or Q2 can auto-launch. The proven VPX script pulses switch 15 during its release bookkeeping, but the ROM Switch Test proves 15 is the physical Tournament Start cabinet button. Never construct a fifth trough/release sensor at 15. Preserve individual occupancy and sustained trough/shooter state. Except for the two proven cabinet buttons, the partial manual does not establish factory contact construction; choose suitable physical sensors while preserving every validated semantic binding and pulse/sustained behavior.

## Motorized suitcase and visible lock

The suitcase is a stepper-driven moving assembly and a three-ball visible lock, not a single solenoid animation. The proven VPX script registers Q21 alone as its logical animation callback, but the same line's hardware comment explicitly lists physical suitcase motor positions Q21/Q23/Q25/Q30. These four drives energize the 24 V stepper assembly 511-5072-00 through cable 036-5634-11-A7; their A/B/C/D electrical order and individual supply-wire colors are not established, so retain the Q identities and determine phase wiring for the chosen motor driver. Q28 separately raises/releases the lock post. Home switch 48 is active only at the closed/home endpoint, clears during travel, and returns near home. The ordinary ROM coil diagnostic skips all four drive positions and the auxiliary menu exposes a dedicated Suitcase Motor Test. The proven script animates roughly from 358 to 320 and back, but tune physical travel to the modeled geometry. Its corrected visible-lock order maps physical bottom switch 43 to ROM 45, middle 44 to 44, and top 45 to ROM 43. IPDB confirms balls can remain locked while the suitcase is open or closed. Recreate moving collision geometry, three physical ball seats, the release post, and actual containment.

## Safe House, Sniper House, and drop targets

The Safe House contains a saucer on switch 3 with eject Q3. Q12 flips the entire front down to expose the miniature army-men interior and its flashers; return it upright when disabled and move its collision surface with it. Q13 resets the two House drop targets on 11/13. The Sniper House uses Q14 to open and reveal target 62, Q29 to operate the neighboring up-post, and a figure that waggles while firing. Single drop targets 60/61 reset independently with Q4/Q5. Stern describes several single Sniper targets as obscuring or freeing shots, so every drop and facade position must alter ball collision and shot availability rather than merely render an animation.

## Gates, posts, routes, and standard devices

Q6/Q7 operate the left/right control gates and Q22 operates the unsensed left-ramp up-post. Left-loop spinner 10 pulses; left/right orbit contacts are 46/54; right-ramp entrance is 58; top lanes are 55-57; lower outlane/return pairs are 24/25 and 29/28. Flippers use Q15/Q16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pop pairs are Q9/SW30, Q10/SW31, and Q11/SW32; slings are Q17/SW26 and Q18/SW27. Fixed standups are House 1/2, Cell Phone 4, CHLOE 5-9, MOLE 33/34, and the right bank 39-41. Q8 is an optional shaker added in ROM v1.44; Q24 is an optional common-board 5 V device channel with no stock playfield device identified.

## Lamps, flashers, display, and emulator capacity

Lamp-matrix addresses 1-80 are populated except explicit unused address 9. The ROM service test reports addresses 72-75 only as CTU and 76-78 only as MOLE; numeric suffixes in JSON preserve unique bindings without inventing an unverified face order. The 2009 machine uses incandescent matrix lamps and aggregate GI 0. Q19/Q20/Q26/Q27/Q31/Q32 are feature flashers. Bind the native 128x32 four-bit DMD and synthetic SAM game-on 33. Because PinMAME declares `SAM_NO_AUX`, public 51-66 remain explicit unused emulator capacity, not physical outputs, and legacy game-on aliases 34-36 are not devices.

## Author construction checklist

- Build the typed four-ball trough, manual/auto shooter, motorized suitcase with four addressed stepper drives/home sensor/three ball seats/release post, Safe House facade and saucer, House two-bank, Sniper facade/figure/target/post, both single drops, control gates, ramp post, flippers, pops, slings, routes, spinner, and fixed targets.
- Initialize trough switches 18-21 and suitcase home switch 48. Preserve ball occupancy, normally-closed EOS state, endpoints, moving collision geometry, drop latching/reset, gate direction, lock ordering, and physical release causality.
- Bind every matrix/dedicated/DIP input, Q1-Q32, synthetic game-on 33, explicit unused auxiliary 51-66, lamp 1-80, GI 0, and the DMD. Do not create playfield hardware from aliases or emulator capacity.
- Use the proven VPX script as the runtime tie-breaker, ROM diagnostics for exact semantics and wire labels, Stern's partial manual for 24 construction, and the later SAM schematic only for standardized board connector pins.

## Sources

- `manual.stern-24-parts.2009`: official partial parts book SHA-256 `c547202e54b3ffbe53ba955db9eed8d52a6fef4b4807416de2f31ccf18aaf71f`, organized under the external manual cache with searchable text and rendered pages.
- `vpx.stern-24-2.3.1`: pinned known-working script SHA-256 `7bf550806bd87c17417a974ed75b1700885da883e0dce5ce31d7dc7ba6cc094f`.
- `rom.stern-24.twenty4-150`: exact external archive SHA-256 `f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4`; the ROM readme supplies revision-specific mechanism fixes.
- `runtime.stern-24-switch-diagnostic-1-17`, `runtime.stern-24-switch-diagnostic-22-64`, `runtime.stern-24-coil-diagnostic`, `runtime.stern-24-lamp-diagnostic`, and `runtime.stern-24-suitcase-motor-menu`: separately hashed held-switch, coil, lamp, and menu traces with their evidence limits stated in JSON.
"""


def runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": ["stern.twenty-four.2009"], "driver_ids": ["twenty4_150"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {
			"game": "twenty4_150",
			"command_template": "Boot: python tools/run_pinmame_harness.py --library <libpinmame> --game twenty4_150 --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:1.0 --pulse 16:500:3 --observe 3 --dmd-dir <external-dmd-dir> --output <external-json>; held Switch Test: python tools/run_pinmame_harness.py --library <libpinmame> --game twenty4_150 --rom-path <vpinmame-roms> --work-dir <isolated-state> --snapshot-while-held --pulse <service-and-matrix-switch-sequence> --output <external-json>",
			"rom_archive_sha256": "f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4",
			"raw_runs": [
				{"name": "boot-start-v1", "sha256": "a1fca511fbebd25e045af4e22e08505820e633c9be493808572b7245c85886db", "self_test_pulses": 0},
				{"name": "switch-matrix-1-17-held-v2", "sha256": "d771050fab8d52590383899ca8f11ab8c59886730de25e1be07021ad76261b14", "self_test_pulses": 17},
				{"name": "switch-matrix-held-diagnostic-v1", "sha256": "7f51c62f83f6933de08379fc7c65ed8bd6193c8ae474a972bdaf588fb282ad0d", "self_test_pulses": 43},
				{"name": "coil-diagnostic-v1", "sha256": "b37e8977dd1fb91cc27cae31ce995ff3cd825a7dfb9ceca9a5589f93be3fdcf0", "self_test_pulses": 0},
				{"name": "lamp-diagnostic-v1", "sha256": "a3a6d5277e56c833445a3fc3a69d774f3b1d494f4df6aea99bc858670a25f286", "self_test_pulses": 0},
				{"name": "suitcase-motor-menu-v1", "sha256": "6d48aa7e63bd39eb339732888669768b1dcf584a1d51821b6d7a346ca809ea9b", "self_test_pulses": 0},
			],
			"observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": list(range(1, 81)), "initial_lamp_addresses": [1, 4, 5, 7, 8] + list(range(10, 60)) + list(range(63, 81)), "solenoid_addresses_seen": [33], "gi_addresses_seen": [0], "public_solenoid_decoder_holes_not_seen": [21, 23, 25, 30]},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/twenty4_150/harness", "sha256": "a1fca511fbebd25e045af4e22e08505820e633c9be493808572b7245c85886db", "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def main() -> None:
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/twenty-four-2009.json"), fail_closed_spatial_partial(build()))
	write_json(ROOT / "evidence/runtime/sam/twenty-four-boot-start-and-diagnostics.json", runtime_evidence())
	write_text(ROOT / "knowledge/stern/twenty-four-2009.md", fail_closed_spatial_knowledge("stern.twenty-four.2009", KNOWLEDGE))


if __name__ == "__main__":
	main()
