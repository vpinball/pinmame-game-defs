"""Build the reviewed, author-ready Stern Ripley's machine definition."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.stern-ripleys.2004"
VPX_SOURCE = "vpx.ripleys-vpwmod-1.3"
TABLE_SOURCE = "vpx-table.ripleys-jpsalas-1.0.3-uk"
TABLE_EXTRACTION_MANIFEST_SHA256 = "79cdb19cd01d46d795b32b7638a0f75c19bf824256de89a879d9d5328ce6b61d"
ROM_SOURCE = "rom.stern-ripleys.3.20"
IPDB_SOURCE = "ipdb.stern-ripleys.4917"
RUNTIME_BOOT_SOURCE = "runtime.ripleys.boot"
RUNTIME_START_SOURCE = "runtime.ripleys.boot-start"
RUNTIME_GAMEPLAY_SOURCE = "runtime.ripleys.gameplay"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(dict.fromkeys(source_refs))}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


# label, pulse, availability, roles
SWITCHES: dict[int, tuple[str, bool, str, tuple[str, ...]]] = {
	1: ("Left cabinet button (UK only)", False, "optional", ("cabinet.uk-button-left",)),
	2: ("Fourth coin slot", True, "optional", ("cabinet.coin.fourth",)),
	3: ("Sixth coin slot", True, "optional", ("cabinet.coin.sixth",)),
	4: ("Right coin slot", True, "used", ("cabinet.coin.right",)),
	5: ("Center coin slot / DBA", True, "used", ("cabinet.coin.center",)),
	6: ("Left coin slot", True, "used", ("cabinet.coin.left",)),
	7: ("Fifth coin slot", True, "optional", ("cabinet.coin.fifth",)),
	8: ("Right cabinet button (UK only)", False, "optional", ("cabinet.uk-button-right",)),
	9: ("Head stand-up", True, "used", ()),
	11: ("Four-ball trough 1 (left)", False, "used", ("ball.position",)),
	12: ("Four-ball trough 2", False, "used", ("ball.position",)),
	13: ("Four-ball trough 3", False, "used", ("ball.position",)),
	14: ("Four-ball trough 4 / VUK opto", False, "used", ("ball.position",)),
	15: ("Four-ball stacking opto", True, "used", ("ball.path",)),
	16: ("Shooter lane", False, "used", ("ball.position",)),
	17: ("Tombstone 1", True, "used", ()),
	18: ("Super Jackpot opto", False, "used", ("ball.path",)),
	19: ("Tombstone 5", True, "used", ()),
	20: ("Left spinner", True, "used", ()),
	21: ("Right spinner", True, "used", ()),
	22: ("Tombstone 4", True, "used", ()),
	23: ("Shrunken Head opto", False, "used", ("ball.position",)),
	24: ("Idol Eye opto", False, "used", ("ball.position",)),
	25: ("Lower left pop bumper", True, "used", ()),
	26: ("Lower right pop bumper", True, "used", ()),
	27: ("Lower bottom pop bumper", True, "used", ()),
	28: ("Side scoop entry", False, "used", ("ball.path",)),
	29: ("Scoop VUK", False, "used", ("ball.position",)),
	30: ("Behind Head", False, "used", ("ball.path",)),
	31: ("Left ramp make", False, "used", ("ball.path",)),
	32: ("Tombstones 2 and 3", True, "used", ()),
	33: ("Bonus X inlane left", False, "used", ()),
	34: ("Bonus X inlane middle", False, "used", ()),
	35: ("Bonus X inlane right", False, "used", ()),
	36: ("Right orbit", False, "used", ("ball.path",)),
	38: ("Mini-playfield left", False, "used", ("ball.path",)),
	39: ("Mini-playfield center", False, "used", ("ball.path",)),
	40: ("Mini-playfield right", False, "used", ("ball.path",)),
	41: ("Vari-target opto 1", False, "used", ("position.deep",)),
	42: ("Vari-target opto 2", False, "used", ("position.shallow",)),
	43: ("Vari-target opto 3", False, "used", ("position.middle",)),
	44: ("Lock 1 top", False, "used", ("ball.position",)),
	45: ("Lock 1 middle", False, "used", ("ball.position",)),
	46: ("Lock 1 bottom", False, "used", ("ball.position",)),
	47: ("Left Jackpot loop", False, "used", ("ball.path",)),
	48: ("Left orbit", False, "used", ("ball.path",)),
	49: ("Upper left pop bumper", True, "used", ()),
	50: ("Upper right pop bumper", True, "used", ()),
	51: ("Upper bottom pop bumper", True, "used", ()),
	52: ("Vari-target VUK", False, "used", ("ball.position",)),
	53: ("Right ramp", False, "used", ("ball.path",)),
	54: ("Start button", False, "used", ("cabinet.start",)),
	55: ("Tournament Start", False, "optional", ("cabinet.tournament-start",)),
	56: ("Plumb bob tilt", False, "used", ("cabinet.tilt",)),
	57: ("Left outlane", False, "used", ()),
	58: ("Left return lane", False, "used", ()),
	59: ("Left slingshot", True, "used", ()),
	60: ("Right outlane", False, "used", ()),
	61: ("Right return lane", False, "used", ()),
	62: ("Right slingshot", True, "used", ()),
}

SWITCH_PARTS = {
	1: "180-5160-00", 2: "180-5204-00", 4: "180-5204-00", 5: "180-5204-00", 6: "180-5204-00", 8: "180-5160-00",
	9: "515-5162-08", 11: "180-5119-02", 12: "180-5119-02", 13: "180-5119-02", 16: "180-5157-00", 17: "515-5162-08",
	19: "515-5162-08", 20: "180-5010-04", 21: "180-5010-04", 22: "515-5967-06", 25: "180-5015-03", 26: "180-5015-03",
	27: "180-5015-03", 28: "180-5183-00", 29: "180-5183-00", 30: "500-6227-02", 31: "180-5190-28", 32: "515-5162-08",
	33: "500-6227-02", 34: "500-6227-02", 35: "500-6227-02", 36: "500-6227-02", 38: "180-5183-00", 39: "180-5183-00",
	40: "180-5183-00", 44: "180-5180-00", 45: "180-5179-00", 46: "180-5178-00", 47: "500-6227-02", 48: "500-6227-02",
	49: "180-5015-03", 50: "180-5015-03", 51: "180-5015-03", 52: "180-5116-01", 53: "500-5190-28", 54: "180-5174-00",
	55: "180-5174-00", 57: "500-6227-02", 58: "500-6227-02", 59: "180-5054-00", 60: "500-6227-02", 61: "500-6227-02", 62: "180-5054-00",
}
SWITCH_ASSEMBLIES = {
	14: "515-0173-00 transmitter + 515-0174-00 receiver", 15: "515-0173-00 transmitter + 515-0174-00 receiver",
	18: "500-6775-00 transceiver pair", 23: "500-6775-00 transceiver pair", 24: "500-6775-00 transceiver pair",
	41: "520-5234-00", 42: "520-5234-00", 43: "520-5234-00", 56: "535-5319-00 hanger + 535-7563-01 contact wire",
}
SWITCH_TYPES = {
	**{number: "button" for number in (1, 2, 3, 4, 5, 6, 7, 8, 54, 55)},
	**{number: "opto" for number in (14, 15, 18, 23, 24, 41, 42, 43)},
	**{number: "microswitch" for number in (11, 12, 13, 28, 29, 44, 45, 46, 52)},
	**{number: "leaf" for number in (9, 16, 17, 19, 20, 21, 22, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 47, 48, 49, 50, 51, 53, 57, 58, 59, 60, 61, 62)},
	56: "tilt",
}
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9"), ("WHT-RED", "CN7-P8"), ("WHT-ORG", "CN7-P7"), ("WHT-YEL", "CN7-P6"), ("WHT-GRN", "CN7-P5"), ("WHT-BLU", "CN7-P3"), ("WHT-VIO", "CN7-P2"), ("WHT-GRY", "CN7-P1")]


def switch_id(number: int) -> str:
	label = SWITCHES[number][0] if number in SWITCHES else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int) -> dict[str, object]:
	spec = SWITCHES.get(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	availability = spec[2] if spec else "unused"
	drive_index, return_index = divmod(number - 1, 8)
	physical: dict[str, object] = {"switch_type": SWITCH_TYPES.get(number, "unknown")}
	if number in SWITCH_PARTS:
		field = "assembly_part_number" if SWITCH_PARTS[number].startswith("500-") else "part_number"
		physical[field] = SWITCH_PARTS[number]
	if number in SWITCH_ASSEMBLIES:
		physical["assembly_part_number"] = SWITCH_ASSEMBLIES[number]
	if number in (59, 62):
		physical.update({"quantity": 2, "notes": "The manual specifies two parallel playfield contacts for this slingshot address."})
	elif number in (3, 7):
		physical["notes"] = "The manual marks this optional coin position Future Use and supplies no installed switch part."
	elif not spec:
		physical["notes"] = "The machine-specific manual marks this matrix position Not Used."
	result: dict[str, object] = {
		"id": switch_id(number), "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)), "normally_closed": False, "pulse": spec[1] if spec else False,
		"availability": availability, "physical": physical,
		"wiring": {"board": "Whitestar CPU/Sound board switch matrix", "drive_wire": MATRIX_DRIVE[drive_index][0], "drive_connection": MATRIX_DRIVE[drive_index][1], "return_wire": MATRIX_RETURN[return_index][0], "return_connection": MATRIX_RETURN[return_index][1]},
		"provenance": provenance(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE),
	}
	if spec and spec[3]:
		result["roles"] = list(spec[3])
	if number in (11, 12, 13, 14, 42, 43):
		result["initial_active"] = True
	return result


DEDICATED = {
	-3: ("Coin-door memory protect", "button", "used", False, ("cabinet.memory-protect",), ("", "CN6-P12", "MEMORY PROTECT")),
	-2: ("Volume / service Left (red)", "button", "used", False, ("service.left",), ("GRY-BLU", "CN6-P8", "DS-6")),
	-1: ("Service Credit / service Right (green)", "button", "used", False, ("service.right",), ("GRY-VIO", "CN6-P9", "DS-7")),
	0: ("Begin Test / service Enter (black)", "button", "used", False, ("service.enter",), ("GRY-BLK", "CN6-P10", "DS-8")),
	81: ("Right flipper end-of-stroke", "leaf", "used", False, ("flipper.lower.right.eos",), ("GRY-YEL", "CN6-P6", "DS-4")),
	82: ("Right flipper button", "button", "used", False, ("flipper.lower.right.button",), ("GRY-ORG", "CN6-P4", "DS-3")),
	83: ("Left flipper end-of-stroke", "leaf", "used", False, ("flipper.lower.left.eos",), ("GRY-RED", "CN6-P3", "DS-2")),
	84: ("Left flipper button", "button", "used", False, ("flipper.lower.left.button",), ("GRY-BRN", "CN6-P2", "DS-1")),
	85: ("Unused generic flipper-column input 85", "unknown", "unused", False, (), None),
	86: ("Unused generic flipper-column input 86", "unknown", "unused", False, (), None),
	87: ("Unused generic flipper-column input 87", "unknown", "unused", False, (), None),
	88: ("Upper-right flipper button", "button", "used", False, ("flipper.upper.right.button",), ("GRY-GRN", "CN6-P7", "DS-5")),
}


def dedicated_switch(address: int) -> dict[str, object]:
	label, switch_type, availability, pulse, roles, wire = DEDICATED[address]
	physical: dict[str, object] = {"switch_type": switch_type}
	if address == -3:
		physical["part_number"] = "180-5000-01"
		physical["assembly_part_number"] = "500-5808-00"
		physical["notes"] = "Bottom button of the coin-door dual-switch bracket. It is closed/enabled while the door is closed and opens when the door opens, allowing writes to protected RAM."
	elif address == -2:
		physical["part_number"] = "180-5192-02"
	elif address == -1:
		physical["part_number"] = "180-5192-04"
	elif address == 0:
		physical["part_number"] = "180-5192-00"
	elif address in (81, 83):
		physical["part_number"] = "180-5149-00"
		physical["notes"] = "Physical end-of-stroke contact on the flipper; normally closed."
	elif address in (82, 84, 88):
		physical["part_number"] = "180-5160-00" if address == 84 else "180-5164-00" if address == 82 else "180-5164-00"
	result: dict[str, object] = {
		"id": f"switch.{address if address >= 0 else 'n' + str(abs(address))}-{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address}, "aliases": aliases("pinmame.switch", address, wire[2] if wire else None),
		"normally_closed": address in (81, 83), "pulse": pulse, "availability": availability, "physical": physical,
		"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, VPX_SOURCE),
	}
	if roles:
		result["roles"] = list(roles)
	if address == -3:
		result["initial_active"] = True
	if address == -3:
		result["wiring"] = {"board": "Whitestar CPU/Sound board memory-protect input", "drive_connection": "CN6-P12"}
	elif wire:
		result["wiring"] = {"board": "Whitestar dedicated-switch input", "drive_wire": wire[0], "drive_connection": wire[1], "return_wire": "BLK", "return_connection": "CN6-P1/-P11"}
	return result


def inputs() -> list[dict[str, object]]:
	items = [matrix_switch(number) for number in range(1, 65)]
	items.extend(dedicated_switch(address) for address in sorted(DEDICATED))
	for number in range(1, 9):
		availability = "used" if number <= 5 else "unused"
		items.append({
			"id": f"switch.dip-{number}", "label": f"SW300 country selector bit {number}", "kind": "dip_switch",
			"binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"SW300-{number}"),
			"availability": availability, "physical": {"switch_type": "dip", "location": "Whitestar CPU/Sound board", "notes": "SW300 uses only bits 1-5 for the country code." if number <= 5 else "Unused high bit in the eight-address public DIP bank."},
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE),
		})
	return items


# label, kind, availability, part number
Q_OUTPUTS: dict[int, tuple[str, str, str, str | None]] = {
	1: ("Trough up-kicker", "coil", "used", "090-5044-00B"), 2: ("Auto-launch", "coil", "used", "090-5001-00B"),
	3: ("Vari-target VUK", "coil", "used", "090-5036-00T"), 4: ("Left ramp diverter", "coil", "used", "090-5031-00"),
	5: ("Right ramp diverter", "coil", "used", "090-5031-00"), 6: ("Lower left pop bumper", "coil", "used", "090-5044-00T"),
	7: ("Lower right pop bumper", "coil", "used", "090-5044-00T"), 8: ("Lower bottom pop bumper", "coil", "used", "090-5044-00T"),
	9: ("Upper left pop bumper", "coil", "used", "090-5044-00T"), 10: ("Upper right pop bumper", "coil", "used", "090-5044-00T"),
	11: ("Upper bottom pop bumper", "coil", "used", "090-5044-NL"), 12: ("Scoop VUK", "coil", "used", "090-5036-00T"),
	13: ("Lock kicker", "coil", "used", "090-5001-00B"), 14: ("Upper-right flipper", "coil", "used", "090-5067-00T"),
	15: ("Left flipper", "coil", "used", "090-5032-00T"), 16: ("Right flipper", "coil", "used", "090-5032-00T"),
	17: ("Left slingshot", "coil", "used", "090-5001-00T"), 18: ("Right slingshot", "coil", "used", "090-5001-00T"),
	19: ("Idol magnet", "magnet", "used", "090-5042-00"), 20: ("Shrunken Head magnet", "magnet", "used", "090-5042-00"),
	21: ("Vari-target reset", "coil", "used", "090-5031-00-ND"), 22: ("Idol opto LED", "lamp", "used", None),
	23: ("Top post", "coil", "used", "090-5044-00T"), 24: ("Optional 5 V output (unassigned)", "coil", "optional", None),
	25: ("Lower pops / lower-left flashers", "flasher", "used", "165-5000-89"), 26: ("Left spinner flasher", "flasher", "used", "165-5000-89"),
	27: ("Upper-left flasher", "flasher", "used", "165-5004-00"), 28: ("Shrunken Head flasher", "flasher", "used", "165-5004-02"),
	29: ("Vari-target flasher", "flasher", "used", "165-5000-89"), 30: ("Upper pops / right-ramp flashers", "flasher", "used", None),
	31: ("Right spinner flasher", "flasher", "used", "165-5000-89"), 32: ("Right-ramp lower flasher", "flasher", "used", "165-5004-00"),
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "ORG to VIO-ORG", "ORG-YEL to VIO-YEL", "ORG-GRN to VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]
PUBLIC_BINDING = {15: 48, 16: 46}


def q_output_id(number: int) -> str:
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def q_wiring(number: int) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "Whitestar I/O Power Driver board", "driver_transistor": f"Q{number}", "control_wire": CONTROL_WIRE[number - 1], "control_connection": CONTROL_CONNECTION[number - 1]}
	if number <= 13:
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P4/5", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif number == 14:
		wiring.update({"power_wire": "BLU-YEL via 3 A fuse and RED-YEL feed", "power_connection": "J10-P1/2", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif number == 15:
		wiring.update({"power_wire": "GRY-YEL via 3 A fuse and RED-YEL feed", "power_connection": "J10-P1/2", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif number == 16:
		wiring.update({"power_wire": "BLU-YEL via 3 A fuse and RED-YEL feed", "power_connection": "J10-P1/2", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif number in (17, 18, 22, 23):
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif number in (19, 20, 21):
		wiring.update({"power_wire": "VIO-YEL auxiliary-board feed via VIO-RED", "power_connection": "J10-P3", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif number == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P7", "nominal_voltage_v": 5, "voltage_type": "dc"})
	else:
		wiring.update({"power_wire": "ORG", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	return wiring


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], *, group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, stable_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def solenoid_outputs() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for number, (label, kind, availability, part_number) in Q_OUTPUTS.items():
		address = PUBLIC_BINDING.get(number, number)
		physical: dict[str, object] = {"location": label}
		if part_number:
			physical["part_number"] = part_number
		if number == 15:
			physical["notes"] = "Physical Q15 is removed from standard public 15 and exposed through lower-left power/canonical addresses 47/48. Bind the single physical device to public 48, matching the proven table's sLLFlipper callback; public 47 is its power-phase compatibility state, not another coil."
		elif number == 16:
			physical["notes"] = "Physical Q16 is removed from standard public 16 and exposed through lower-right power/canonical addresses 45/46. Bind the single physical device to public 46, matching the proven table's sLRFlipper callback; public 45 is its power-phase compatibility state, not another coil."
		elif number == 22:
			physical["notes"] = "Switched-ground emitter for the Idol Eye opto path; this is not a decorative playfield lamp."
		elif number == 24:
			physical["notes"] = "The factory table marks this as an optional 5 V output with no assigned stock device. The exact proven VPX script deliberately comments out its SolKnocker callback while retaining a dormant handler; preserve the controller address, but do not construct a stock knocker."
		elif number == 25:
			physical.update({"quantity": 2, "notes": "Two #89 flashers share Q25: the lower-pop and lower-left positions printed as X2 in the manual."})
		elif number == 30:
			physical.update({"quantity": 2, "notes": "Two flashers share Q30 as printed by the manual's X2 suffix: one #89 under the upper playfield and one #906 on the right ramp."})
		source_refs = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE, RUNTIME_GAMEPLAY_SOURCE) if number == 24 else (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)
		items.append(make_output(address, label, kind, availability, source_refs, manual_address=f"Q{number}", physical=physical, wiring=q_wiring(number), stable_id=q_output_id(number)))
	items.append(make_output(15, "PinMAME Whitestar fast-flip game-on state", "virtual", "used", (CORE_SOURCE, RUNTIME_START_SOURCE), physical={"notes": "Synthetic state generated from the ROM fast-flip RAM byte. Physical Q15 is the left flipper and is remapped to public 47/48; never wire this public 15 callback to a transistor."}, stable_id="virtual.fast-flip-game-on"))
	items.append(make_output(16, "Unused remapped-flipper companion address 16", "virtual", "unused", (CORE_SOURCE,), physical={"notes": "Physical Q16 is the right flipper and is remapped to public 45/46. PinMAME configures this public slot alongside fast-flip 15 but never drives it as a physical output."}, stable_id="virtual.remapped-flipper-hole-16"))
	for index, (address, label, control_wire, control_connection, part_number) in enumerate((
		(33, "Optional UK left up/down post", "WHT", "J2-P3", "090-5044-00T"),
		(34, "Optional UK center up/down post", "RED", "J2-P4", "090-5030-00T"),
		(35, "Optional UK right up/down post", "ORG", "J2-P7", "090-5044-00T"),
	), start=1):
		items.append(make_output(address, label, "coil", "optional", (MANUAL_SOURCE, CORE_SOURCE), manual_address=f"AUX {index}", physical={"part_number": part_number, "location": label, "notes": "Installed only for the manual's UK/special application; absence is a valid standard-machine configuration."}, wiring={"board": "UK 3X transistor driver board 520-5068-01", "driver_transistor": f"Q{index}", "power_wire": "BRN", "power_connection": "J7-P1", "control_wire": control_wire, "control_connection": control_connection, "nominal_voltage_v": 20, "voltage_type": "dc"}, stable_id=f"device.aux{index}-{slug(label)}"))
	for address in range(36, 45):
		items.append(make_output(address, f"Unused Whitestar compatibility address {address}", "virtual", "unused", (CORE_SOURCE,), physical={"notes": "No physical Ripley device is installed at this public emulator position."}, stable_id=f"virtual.compatibility-{address}"))
	items.append(make_output(45, "Right flipper power-phase compatibility output", "virtual", "used", (CORE_SOURCE, VPX_SOURCE), physical={"notes": "PinMAME exposes physical Q16's power bit at public 45 and synthesizes the same active state into canonical lower-right callback 46. Bind one right-flipper device at public 46; do not instantiate this compatibility phase as another flipper."}, stable_id="virtual.right-flipper-power-phase"))
	items.append(make_output(47, "Left flipper power-phase compatibility output", "virtual", "used", (CORE_SOURCE, VPX_SOURCE), physical={"notes": "PinMAME exposes physical Q15's power bit at public 47 and synthesizes the same active state into canonical lower-left callback 48. Bind one left-flipper device at public 48; do not instantiate this compatibility phase as another flipper."}, stable_id="virtual.left-flipper-power-phase"))
	items.append(make_output(49, "Unused simulated ball-shooter output", "virtual", "unused", (CORE_SOURCE,), physical={"notes": "Reserved PinMAME simulation output; Ripley's physical shooter is represented by Q2 and switch 16."}, stable_id="virtual.simulated-ball-shooter"))
	items.append(make_output(50, "Reserved public output 50", "virtual", "unused", (CORE_SOURCE,), physical={"notes": "Reserved before PinMAME's custom-solenoid boundary; no Ripley hardware is installed."}, stable_id="virtual.reserved-50"))
	return sorted(items, key=lambda item: item["binding"]["device"])


LAMP_LABELS = {
	1: "Super Jackpot 2 Million", 2: "Super Jackpot 3 Million", 3: "Super Jackpot 1 Million", 4: "Super Jackpot 4 Million", 5: "Shoot Again", 6: "Super Jackpot 5 Million", 7: "Super Jackpot 6 Million", 8: "Right Special",
	9: "Left Special", 10: "Idol Counter 1", 11: "Idol Counter 2", 12: "Idol Counter 3", 13: "Idol Counter 4", 14: "Idol Counter 5", 15: "Tombstone 1", 16: "Scoop Arrow",
	17: "RIPLEY'S R", 18: "RIPLEY'S I", 19: "RIPLEY'S P", 20: "RIPLEY'S L", 21: "RIPLEY'S E", 22: "RIPLEY'S Y", 23: "RIPLEY'S S", 24: "Grid A1 (upper left)",
	25: "Grid B1", 26: "Grid C1", 27: "Grid A2", 28: "Grid B2", 29: "Grid C2", 30: "Grid A3", 31: "Grid B3", 32: "Grid C3",
	33: "Lower left pop bumper", 34: "Lower right pop bumper", 35: "Lower bottom pop bumper", 36: "Skill Shot", 37: "Tombstone 2", 38: "Tombstone 3", 39: "Million Plus", 40: "Loop Jackpot",
	41: "Vari-target Special", 42: "Vari-target Extra Ball", 43: "Vari-target Mystery", 44: "Vari-target South America", 45: "Vari-target North America", 46: "Vari-target Europe", 47: "Vari-target Australia", 48: "Vari-target Asia",
	49: "Tombstone 5", 50: "Penguin", 51: "Advance Tombstone", 52: "Right Spinner", 53: "Right Jackpot", 54: "Lock", 55: "Ripoff", 56: "Vari-target Antarctica",
	57: "Center Jackpot", 58: "Lite Head", 59: "Gate Open", 60: "Upper left pop bumper", 61: "Upper right pop bumper", 62: "Upper bottom pop bumper", 63: "Tombstone 4", 64: "Vari-target Africa",
	65: "Left Spinner", 66: "Multiball", 67: "Light Locks", 68: "Collect Bigfoot Bonus", 69: "Super Jackpot", 70: "Odditorium", 71: "The Head Knows", 72: "Bozo",
	73: "Bonus X inlane left", 74: "Bonus X inlane center", 75: "Bonus X inlane right", 76: "Back Panel A", 77: "Back Panel B", 78: "Back Panel C", 79: "Tournament button", 80: "Start button",
}
LAMP_44 = {11, 16, 50, 51, 52, 63, 65, 76, 77, 78}
LAMP_DRIVE = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]


def lamp_outputs() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address in range(1, 81):
		label = LAMP_LABELS[address]
		column = (address - 1) % 8
		row = (address - 1) // 8
		part_number = "165-5000-44" if address in LAMP_44 else "165-5002-00"
		physical = {"location": label, "part_number": part_number, "notes": "Factory #44 clear bulb and socket from the official matrix." if address in LAMP_44 else "Factory #555 clear bulb and socket from the official matrix."}
		wiring = {"board": "Whitestar I/O Power Driver board lamp matrix", "drive_wire": LAMP_DRIVE[column][0], "drive_connection": LAMP_DRIVE[column][1], "return_wire": LAMP_RETURN[row][0], "return_connection": LAMP_RETURN[row][1]}
		items.append(make_output(address, label, "lamp", "used", (MANUAL_SOURCE, CORE_SOURCE, VPX_SOURCE), group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring=wiring, stable_id=f"lamp.{address}-{slug(label)}"))
	items.append(make_output(0, "General illumination relay", "gi", "used", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_BOOT_SOURCE, VPX_SOURCE), group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Backbox, playfield, and coin-door general illumination", "quantity": 4, "notes": "One PinMAME relay channel controls four separately fused physical strings: F24 back panel; F25 upper/mid-right playfield; F26 upper-left/back panel/coin door; and F27 upper-right/mid-left/lower playfield. Recreate all four circuits but bind their common control to GI 0."}, wiring={"board": "Whitestar I/O Power Driver board GI relay"}, stable_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *, positions: list[dict[str, object]] | None = None, assembly_part_number: str | None = None, sources: tuple[str, ...] = (MANUAL_SOURCE, VPX_SOURCE)) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions is not None:
		result["positions"] = positions
	if assembly_part_number:
		result["assembly_part_number"] = assembly_part_number
	return result


def mechanisms() -> list[dict[str, object]]:
	common = (MANUAL_SOURCE, VPX_SOURCE, IPDB_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough and stacking opto", "kicker", [q_output_id(1)], [switch_id(number) for number in (11, 12, 13, 14, 15)], "Four balls initialize on 11-14. Q1 kicks the rightmost ball from 14, pulses stacking opto 15, and the proven script advances each remaining ball one station after 100 ms. Preserve four independent ball seats, the opto transition, and physical drain/re-stack causality.", sources=common),
		mechanism("mechanism.auto-launch", "Manual shooter with auto-launch", "kicker", [q_output_id(2)], [switch_id(16)], "A ball can rest on shooter switch 16 for manual plunge; Q2 drives the impulse auto-launch. The proven table uses power 44, a 0.7-second full-plunge time, and 0.3 randomization as a starting point for the virtual mechanism.", sources=common),
		mechanism("mechanism.vari-target", "Seven-detent vari-target", "other", [q_output_id(21)], [switch_id(number) for number in (41, 42, 43)], "Assembly 515-7322-00 has seven mechanical stops including home and three 520-5234-00 opto channels. The proven script uses a 267-unit lever, 50-unit width, spring factor 0.3, return speed 600 units/s, and thresholds at path length 1/6 for switch 42, 1/2 for 43, and 3/4 for 41; during motion it clears all three and asserts only the deepest crossed threshold. At table initialization it explicitly closes 42 and 43 and leaves 41 open. Q21 commands reset toward the 15-degree home angle. Preserve the seven detents, overlapping boot state, threshold order, and ball-to-target impulse rather than reducing this to a three-position animation.", positions=[{"id": "position.home", "label": "Reset/home boot state", "sensors": [switch_id(42), switch_id(43)]}, {"id": "position.shallow", "label": "First sensed travel", "sensors": [switch_id(42)]}, {"id": "position.middle", "label": "Second sensed travel", "sensors": [switch_id(43)]}, {"id": "position.deep", "label": "Deepest sensed travel", "sensors": [switch_id(41)]}], assembly_part_number="515-7322-00", sources=common),
		mechanism("mechanism.vari-target-vuk", "Vari-target VUK", "kicker", [q_output_id(3)], [switch_id(52)], "A ball remains at switch 52 below the vari-target until Q3 kicks it at approximately 36 degrees with vertical strength 1.5. Keep this ball device coupled spatially to, but logically distinct from, the seven-detent target and Q21 reset.", sources=common),
		mechanism("mechanism.idol-magnet", "Idol Eye ball-throw magnet", "toy", [q_output_id(19), q_output_id(22)], [switch_id(24)], "A ball crossing the lower Idol Eye closes opto 24. Q19 energizes the lower magnet to hold and throw the ball; Q22 is the separately controlled switched-ground opto emitter. The proven table uses magnet strength 50 without forced centering. Recreate the ball capture/throw interaction and sensor beam, not merely a visual idol animation.", sources=common),
		mechanism("mechanism.shrunken-head-magnet", "Shrunken Head capture-and-throw magnet", "toy", [q_output_id(20)], [switch_id(23)], "Opto 23 identifies the ball beneath the Shrunken Head. The proven table samples every 150 ms, enables center capture on tick 3, removes linear and angular velocity on tick 4, releases/cools down after tick 12, and applies a bounded upward correction when Q20 releases. Treat those values as a proven virtual baseline and preserve the physical magnet's hold-then-throw behavior.", sources=common),
		mechanism("mechanism.scoop-vuk", "Side scoop and scoop VUK", "kicker", [q_output_id(12)], [switch_id(28), switch_id(29)], "Switch 28 records entry into the side scoop path; the ball settles on VUK switch 29. Q12 clears 29 and kicks the ball back to the playfield near 177 degrees with strength around 100. Preserve the hidden path, occupancy, and delayed eject transaction.", sources=common),
		mechanism("mechanism.three-ball-lock", "Three-position visible lock", "kicker", [q_output_id(13)], [switch_id(number) for number in (44, 45, 46)], "Build three independently sensed ball seats ordered top 44, middle 45, and bottom 46. Q5's proven LockDiverter feeds this lock route; Q13 ejects from the modeled lock path. Preserve visible ball containment and cascading occupancy; do not collapse the three sensors into one lock switch.", sources=common),
		mechanism("mechanism.ramp-diverters", "Temple and lock ramp diverters", "diverter", [q_output_id(4), q_output_id(5)], [switch_id(31), switch_id(53)], "The proven callbacks name Q4 TempleDiv on the manual's left-ramp path and Q5 LockDiverter on the manual's right-ramp path. The shared vpmSolDiverter implementation rotates each primitive to its end position while energized and back to its start position while released. Q4 selects the Temple branch; Q5 selects the feed into lock seats 44-46. Switches 31 and 53 sense ball passage on the associated ramps, not diverter position. Recreate both collision states and route a real ball rather than animating decorative primitives.", sources=common),
		mechanism("mechanism.upper-right-flipper", "Upper-right flipper", "other", [q_output_id(14)], ["switch.88-upper-right-flipper-button"], "Physical Q14 is a normal public solenoid-14 output and DS-5/public 88 is its cabinet button. Whitestar does not remap this upper flipper to WPC public 34/36; the proven table also activates its virtual flipper directly from the upper-right key, so its generic sURFlipper callback must not override the Q14 binding.", sources=(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)),
		mechanism("mechanism.lower-flippers", "Lower flippers", "other", [q_output_id(15), q_output_id(16)], ["switch.84-left-flipper-button", "switch.83-left-flipper-end-of-stroke", "switch.82-right-flipper-button", "switch.81-right-flipper-end-of-stroke"], "Physical Q15/Q16 drive left/right flippers. PinMAME moves right Q16 to lower-flipper power/canonical addresses 45/46 and left Q15 to 47/48, synthesizing each canonical callback's hold state from the power bit. Bind the single physical devices to the proven callbacks 46 and 48 and never instantiate power-phase compatibility addresses 45/47 as separate actuators. Both EOS contacts are normally closed.", sources=(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)),
		mechanism("mechanism.pop-bumpers", "Six pop bumpers", "other", [q_output_id(number) for number in range(6, 12)], [switch_id(number) for number in (25, 26, 27, 49, 50, 51)], "Lower left/right/bottom pairs are Q6/SW25, Q7/SW26, and Q8/SW27. Upper left/right/bottom pairs are Q9/SW49, Q10/SW50, and Q11/SW51. The proven table pulses each switch and keeps all six physical assemblies distinct.", sources=common),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [q_output_id(17), q_output_id(18)], [switch_id(59), switch_id(62)], "Q17/SW59 and Q18/SW62 are the left/right slings. Each manual switch address uses two parallel contacts and the proven table emits a pulse on a sling event.", sources=common),
		mechanism("mechanism.top-post", "Controllable top post", "gate", [q_output_id(23)], [], "Q23 raises or releases the top post. Preserve its ball-blocking collision state and coil direction even though the machine has no dedicated position sensor.", sources=common),
		mechanism("mechanism.optional-uk-posts", "Optional UK three-post assembly", "other", ["device.aux1-optional-uk-left-up-down-post", "device.aux2-optional-uk-center-up-down-post", "device.aux3-optional-uk-right-up-down-post"], [], "Board 520-5068-01 drives optional left, center, and right up/down posts at public 33-35. Install them only for the UK/special configuration and reproduce each post's raised and lowered collision states; a standard machine legitimately omits all three. The board has no post-position feedback, and the two UK cabinet buttons are independent rules inputs rather than position sensors.", sources=(MANUAL_SOURCE, CORE_SOURCE)),
		mechanism("mechanism.optional-uk-controls", "Optional UK cabinet controls", "other", [], [switch_id(1), switch_id(8)], "The manual identifies matrix 1 and 8 as the left and right UK-only cabinet buttons. Install both controls with the UK/special configuration and deliver sustained controller input while held. They are rules-facing cabinet buttons; neither the manual nor the proven script declares a direct electrical or mechanical linkage to the three post-position outputs, so do not model them as post sensors.", sources=(MANUAL_SOURCE, CORE_SOURCE)),
		mechanism("mechanism.optional-q24-output", "Optional unassigned 5 V output", "other", [q_output_id(24)], [], "The manual exposes Q24 as an optional 5 V output with no assigned stock device. The exact proven script contains a SolKnocker routine but deliberately comments out the Q24 callback, while runtime merely proves public 24 can transition. Preserve the optional binding for a documented field installation, but a stock recreation must not invent a physical or audible knocker.", sources=(MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE, RUNTIME_GAMEPLAY_SOURCE)),
		mechanism("mechanism.mini-playfield", "Upper mini-playfield", "other", [], [switch_id(number) for number in (38, 39, 40)], "Recreate the elevated mini-playfield and its left, center, and right contacts. Preserve height, entry/exit routing, and real ball travel rather than treating these three switches as ordinary flat lanes.", sources=common),
		mechanism("mechanism.routes-and-targets", "Routes, lanes, spinners, and fixed targets", "other", [], [switch_id(number) for number in (9, 17, 18, 19, 20, 21, 22, 30, 31, 32, 33, 34, 35, 36, 47, 48, 53, 57, 58, 60, 61)], "Build every named stand-up, tombstone, spinner, lane, loop, orbit, ramp, and rollover at its manual address. Use the proven pulse/sustained behavior and keep Tombstones 2+3 as the manual's shared switch 32 rather than inventing two controller inputs.", sources=common),
	]


EXPECTED_DRIVERS = {"rip300", "rip300f", "rip300g", "rip300i", "rip300l", "rip301", "rip301f", "rip301g", "rip301i", "rip301l", "rip302", "rip302f", "rip302g", "rip302i", "rip302l", "rip310", "rip310f", "rip310g", "rip310i", "rip310l", "ripleys", "ripleysf", "ripleysg", "ripleysi", "ripleysl"}
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"] in EXPECTED_DRIVERS}
if set(DRIVERS) != EXPECTED_DRIVERS:
	raise ValueError("Ripley's driver family must be covered exhaustively")


def driver_records() -> list[dict[str, object]]:
	selected = []
	for driver_id in EXPECTED_DRIVERS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware/language revision for the same 2004 physical product. Country configuration can enable the optional three-post UK hardware, which remains explicit optional inventory rather than a separate machine definition."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources() -> list[dict[str, object]]:
	return [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/Ripleys_Manual.pdf", "sha256": "94a94aef7437fa5f78cadddd66801e96224cfe6a5b8ff643c4c6b09d979fad9e", "locator": "Official 191-page operation and parts manual, with drawing sheets split by the publisher's PDF assembly order and verified visually. The front-inserted PDF page 8 is printed DR. 6 and contains the complete Q1-Q32 plus UK AUX1-AUX3 coil chart. The appended PDF page 190 is printed DR. 4 and contains the complete switch and lamp chart. PDF pages 25, 82, and 148 document the memory-protect assembly, part, and CN6-P12 input; PDF pages 120-123 (printed 103-106) document GI and flipper wiring; PDF pages 162-166 document the X3 magnet interface, three 5x7 display board, vari-target optos, and UK 3X auxiliary board.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "Ripleys_Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T07:31:10.006812Z"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Ripley%27s%20Believe%20It%20or%20Not%21%20%28Stern%202004%29%20VPWmod%20v1.3.vbs", "revision": VPX_REVISION, "sha256": "3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7", "locator": "Known-working exact ripleys script. Lines 132-201 establish boot state, four trough balls, both magnets, and the shooter; 332-412 establish callbacks, including TempleDiv/LockDiverter identities, trough causality, and a deliberately commented Q24 SolKnocker hook; 1895-2126 implement the seven-stop vari-target and three threshold optos; 2160-2267 implement Shrunken Head/Idol magnets; 2512-2543 implement Vari-VUK, lock, and scoop; 2613-2644 retain a legacy 15x7 segment view of the three mini-DMDs; 3219-3234 bind the modulated GICallback2 function to the single reported GI address.", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors"},
		{"id": TABLE_SOURCE, "kind": "vpx_table", "known_working": True, "uri": "external:pinmame-vpx-sources/stern/ripley-s-believe-it-or-not-2004/Ripley_s Believe It or Not (Stern 2004)1.0.3.vpx", "original_filename": "Ripley_s Believe It or Not (Stern 2004)1.0.3.vpx", "sha256": "6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48", "locator": "Exact physical Ripley's Believe It or Not! (Stern 2004) table selected from the second requested local archive search location and retained byte-for-byte under external:pinmame-vpx-sources/stern/ripley-s-believe-it-or-not-2004. vpxtool git:v0.33.3 extraction is retained at external:pinmame-vpx-sources/stern/ripley-s-believe-it-or-not-2004/extracted-vpxtool. The source declares a UK model and All-Skill extra-post configuration; its 952 x 2115 playfield is therefore exact geometry evidence for the named common playfield objects and an edition-qualified reference for UK-only hardware, never a standard-machine projection. Embedded script SHA-256 is 717696937a92b076620c2564982a7b514786e72fdab01d761b3b2a301346e014. Deterministic retained-extraction manifest SHA-256 is 79cdb19cd01d46d795b32b7638a0f75c19bf824256de89a879d9d5328ce6b61d over the 1,152-file snapshot.", "license": "NOASSERTION", "attribution": "JPSalas table authors and local user-authorized source", "rights": "NOASSERTION"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/segames.c ripleys GEN_WS/dispBION declares controller indices 0-3 in main, left, center, right layout order and registers the 25-driver family; src/wpc/se.c provides sequential I/O, Q15/Q16 remap, fast-flip 15, 520-5068 outputs 33-35, GI 0, and 520-5236 three-display rasterization; src/wpc/core.c synthesizes lower-flipper canonical hold callbacks and indexes display layouts.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames exact ripleys/rip300/rip301/rip302/rip310 language-driver records and clone graph.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/ripleys.zip", "revision": "3.20", "sha256": "092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3", "locator": "Read-only user-authorized archive. ripcpu.320 SHA-256 b04de0c19b356649422dbb2730fd28bc93b993dedab424fad6df31a32cc3d83d; display ROM ripdispa.300 is shared by the cataloged family. ROM bytes remain external and this source is used for exact runtime identity, not semantic reverse engineering.", "license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external"},
		{"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=4917", "locator": "IPDB 4917 physical identity and 2004 product record. Exact I/O and mechanism behavior are sourced from the official manual and proven VPX script.", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T07:00:00Z"},
		{"id": RUNTIME_BOOT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/ripleys/boot-v1/run.json", "revision": PINMAME_REVISION, "sha256": "1ef3c8baa88ace776fdf3ddbc59137afca0e7e9a6803339627985378a818270e", "locator": "Exact ripleys cold boot with switches 11-14 and 42-43 initialized. LibPinMAME reports one 128x32x2 DMD plus three 5x7x2 CORE_NODISP layouts and GI 0. Only display index 0 emitted captured pixel frames in this run, so mini-DMD content activity is not overclaimed.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_START_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/ripleys/boot-start-v1/run.json", "revision": PINMAME_REVISION, "sha256": "e98f6058ba3d4cbd4e772606f1bc8f03039d334cde8d6045ec18d15444bf8ecc", "locator": "Exact coin/start trace with the four-ball initial state. It observes synthetic public 15, generic flipper mirrors 45-48, physical outputs, lamp activity, four display layouts, and GI 0; activity does not establish absent/unused addresses.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": RUNTIME_GAMEPLAY_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/ripleys/gameplay-v1/run.json", "revision": PINMAME_REVISION, "sha256": "d389ced56f57bccd2704758cdac167b56d0a6f1621f306033adcc74d22fd57c7", "locator": "Targeted host-driven trace after coin/start exercises trough release plus Head, tombstone, spinner, Super Jackpot, Shrunken Head, Idol, scoop, and Vari-VUK inputs. It validates address acceptance and output/display capture only; the official manual and proven table remain semantic/causal evidence.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.ripley-s-believe-it-or-not.2004", "name": "Ripley's Believe It or Not!", "manufacturer": "Stern", "year": 2004, "kind": "physical_pinball", "ipdb_id": 4917, "opdb_id": "GRWyB-MLz6Z"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.whitestar", "inversion_applied_by_emulator": True},
		"drivers": driver_records(), "inputs": inputs(), "outputs": solenoid_outputs() + lamp_outputs(),
		"displays": [
			{"id": "display.dmd", "label": "Main dot-matrix display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, RUNTIME_BOOT_SOURCE)},
			{"id": "display.mini-dmd-left", "label": "Left 5x7 mini-DMD", "kind": "dmd", "controller_index": 1, "width": 5, "height": 7, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_BOOT_SOURCE)},
			{"id": "display.mini-dmd-center", "label": "Center 5x7 mini-DMD", "kind": "dmd", "controller_index": 2, "width": 5, "height": 7, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_BOOT_SOURCE)},
			{"id": "display.mini-dmd-right", "label": "Right 5x7 mini-DMD", "kind": "dmd", "controller_index": 3, "width": 5, "height": 7, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_BOOT_SOURCE)},
		],
		"mechanisms": mechanisms(), "relationships": [], "sources": sources(),
		"knowledge": {"path": "knowledge/stern/ripley-s-believe-it-or-not-2004.md", "status": "complete"}, "conflicts": [],
	}


KNOWLEDGE = """# Ripley's Believe It or Not! (Stern, 2004)

Coverage: **author-ready - complete public I/O inventory, factory wiring and parts, native displays, custom mechanisms, firmware/language variants, and recreation behavior validated**

## Identity and evidence precedence

This definition covers the single 2004 physical product and all 25 PinMAME 3.00, 3.01, 3.02, 3.10, and 3.20 English/French/German/Italian/Spanish drivers. The optional UK three-post board is configuration-dependent hardware, not another product. The known-working VPW v1.3 script is controller-facing semantic and causal ground truth; the official Stern manual governs physical construction, wiring, parts, coils, bulbs, and boards; pinned PinMAME governs public routing, clone identity, and native display layouts. Runtime traces validate the exact ROM, public callbacks, GI, and display availability without treating inactivity as proof of absence.

## Four-ball path, shooter, scoop, and lock

Four balls initialize on trough switches 11-14. Q1 ejects the ball at 14 through stacking opto 15, and the proven table advances the remaining balls at 100 ms intervals. Shooter switch 16 supports manual plunge and Q2 auto-launch. Side-scoop entry 28 leads to held VUK switch 29 and Q12 eject. The Vari-VUK is a separate ball device on 52/Q3. Q5's proven `LockDiverter` feeds the visible lock, whose top/middle/bottom seats are 44/45/46; Q13 ejects from that lock path. Preserve sustained occupancy, actual containment, hidden paths, and release causality rather than pulsing all ball-position switches.

## Seven-detent vari-target

The 515-7322-00 vari-target has seven mechanical stops and three optos on board 520-5234-00. The proven script uses a 267-unit lever, 50-unit target width, 0.3 spring factor, 600-unit/s return, and sensor thresholds at path-length 1/6 for 42, 1/2 for 43, and 3/4 for 41. During travel it clears all three and asserts only the deepest crossed threshold; at boot it deliberately initializes 42 and 43 closed with 41 open. Q21 resets toward the 15-degree home angle. Recreate physical detents, spring/ball energy transfer, threshold order, and the overlapping boot state. The adjacent VUK 52/Q3 must remain a distinct ball device.

## Idol Eye and Shrunken Head magnets

The lower Idol Eye path closes opto 24. Q19 drives the Idol magnet to hold and throw the ball, while Q22 separately powers the opto emitter as a switched-ground LED; do not render Q22 as a decorative lamp. The Shrunken Head closes opto 23 and uses Q20 to hold then throw the ball. The proven virtual implementation samples at 150 ms, centers on tick 3, kills velocity/spin on tick 4, and releases/cools after tick 12 with bounded upward correction. Those timings are a reliable virtual baseline, while the manual's physical assemblies govern placement and field interaction.

## Flippers and Whitestar public-output traps

Q14 is the ordinary upper-right flipper output at public solenoid 14, with DS-5/public switch 88 as its button. The working table directly drives its virtual flipper from that key; its generic `sURFlipper` callback is not a Whitestar remap and must not replace Q14. Physical Q15 left and Q16 right are removed from public 15/16 and moved into PinMAME's lower-flipper pairs: Q16 uses power-phase address 45 and canonical `sLRFlipper` callback 46, while Q15 uses power-phase 47 and canonical `sLLFlipper` callback 48. PinMAME synthesizes each canonical callback's hold bit whenever the power bit is active. Bind the single physical right/left devices to 46/48, never instantiate 45/47 as extra coils, and retain normally-closed EOS inputs 81/83. Public 15 is synthetic fast-flip/game-on, while public 16 is unused.

## Diverters, post, pops, slings, routes, and optional hardware

The proven table binds Q4 to `TempleDiv` on the manual's left-ramp path and Q5 to `LockDiverter` on the right-ramp path. Energizing either callback rotates its collision primitive to the end position; release returns it to the start position. Recreate Q4's Temple branch and Q5's feed into lock seats 44-46, while treating ramp switches 31/53 as ball-passage sensors rather than diverter-position feedback. Q23 controls the unsensed top post. Six pop pairs are Q6/SW25, Q7/SW26, Q8/SW27, Q9/SW49, Q10/SW50, and Q11/SW51. Slings are Q17/SW59 and Q18/SW62, with two physical contacts per switch address. The upper mini-playfield has left/center/right contacts 38-40. Build every named orbit, ramp, spinner, lane, jackpot loop, head/tombstone target, and shared Tombstones 2+3 switch 32.

Q24 remains an optional, unassigned 5 V output: the exact script retains a `SolKnocker` routine but deliberately comments out the Q24 callback, and runtime activity proves only that public 24 can transition. A stock recreation must not invent either a physical or audible knocker. The UK 520-5068-01 board adds left/center/right posts at public 33-35; optional matrix switches 1/8 are sustained left/right UK cabinet buttons. They are rules-facing inputs, not post-position sensors, and no direct electrical/mechanical button-to-post linkage is established. Install all five items only for the UK/special configuration; a standard configuration legitimately omits them.

## Lamps, GI, and four native display surfaces

All matrix lamps 1-80 are installed with the exact #555/#44 parts and matrix wiring in JSON. The matrix is eight drive columns by ten return rows, enumerated across each row. Q25-Q32 are the eight flasher channels: Q25 drives two #89 lower-pop/lower-left flashers, while Q30 drives one #89 under the upper playfield and one #906 on the right ramp. GI public 0 is one relay controlling four separately fused physical strings: F24 back panel, F25 upper/mid-right playfield, F26 upper-left/back panel/coin door, and F27 upper-right/mid-left/lower playfield. The script's `GIUpdate2` suffix selects the second, modulated callback interface; it is not a second GI address. Recreate the four physical circuits but route their common controllable state through GI 0.

The machine has a main native 128x32 DMD and three independent physical 5x7 mini-DMD blocks on board 520-5236-00. The `dispBION` layout array exposes them in controller-index order 0 main, 1 left, 2 center, and 3 right, which is encoded explicitly in JSON. `CORE_NODISP` only suppresses the three small layouts from the legacy composite renderer; it does not make them virtual or absent. PinMAME also writes a backward-compatible 15x7 segment representation, and the proven script consumes that legacy view, but a new recreation should bind the three native 5x7 surfaces and avoid building a single physical 15x7 display. The boot harness received layout callbacks for indices 0-3 but pixel-frame callbacks only for the main DMD, so runtime activity of the small displays is not claimed beyond source/manual validation.

## Author construction checklist

- Build four trough seats/stacking opto, manual and auto shooter, side scoop/VUK, three-seat visible lock, seven-detent vari-target and its separate VUK, both ball-throw magnets, both ramp diverters, top post, three flippers, six pops, two slings, elevated mini-playfield, all routes/targets/spinners, optional UK posts, complete lamps/flashers/GI, and all four native DMD surfaces.
- Initialize coin-door memory protect -3, trough 11-14, and vari optos 42/43 active. Preserve ball occupancy, normally-closed lower EOS contacts, vari detents and threshold order, magnet capture/release timing, moving collision, diverter/post direction, visible lock containment, and real release paths.
- Bind all matrix/dedicated/DIP inputs, every physical Q1-Q32 through its declared public address, fast-flip 15, optional AUX33-35, explicit unused compatibility positions, lamps 1-80, GI 0, and four displays. Never instantiate mirror/compatibility callbacks as extra playfield hardware.

## Sources

- `manual.stern-ripleys.2004`: official 191-page manual SHA-256 `94a94aef7437fa5f78cadddd66801e96224cfe6a5b8ff643c4c6b09d979fad9e`, organized under the external manual cache with searchable text, table extraction, and rendered visual review.
- `vpx.ripleys-vpwmod-1.3`: exact known-working script SHA-256 `3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7`.
	- `vpx-table.ripleys-jpsalas-1.0.3-uk`: retained exact local VPX SHA-256 `6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48`; the embedded script SHA-256 is `717696937a92b076620c2564982a7b514786e72fdab01d761b3b2a301346e014`, the retained extraction manifest SHA-256 is `79cdb19cd01d46d795b32b7638a0f75c19bf824256de89a879d9d5328ce6b61d`, and the table is explicitly UK/All-Skill.
- `rom.stern-ripleys.3.20`: exact external archive SHA-256 `092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3`; ROM bytes remain external.
- `runtime.ripleys.boot`, `runtime.ripleys.boot-start`, and `runtime.ripleys.gameplay`: separately hashed LibPinMAME traces with their evidence limits stated in JSON.
"""


def runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": ["stern.ripley-s-believe-it-or-not.2004"], "driver_ids": ["ripleys"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {
			"game": "ripleys", "command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game ripleys --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 11 --initial-switch 12 --initial-switch 13 --initial-switch 14 --initial-switch 42 --initial-switch 43 --pulse 6:150:0.3 <three coin pulses> --pulse 54:400:2 --pulse 14:80:0.2 --pulse 15:100:0.3 --pulse 16:150:1 --pulse <targeted gameplay switches> --observe 2 --dmd-dir <external-dmd-dir> --output <external-json>",
			"rom_archive_sha256": "092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3",
			"raw_runs": [
				{"name": "boot-v1", "sha256": "1ef3c8baa88ace776fdf3ddbc59137afca0e7e9a6803339627985378a818270e", "self_test_pulses": 0},
				{"name": "boot-start-v1", "sha256": "e98f6058ba3d4cbd4e772606f1bc8f03039d334cde8d6045ec18d15444bf8ecc", "self_test_pulses": 0},
				{"name": "gameplay-v1", "sha256": "d389ced56f57bccd2704758cdac167b56d0a6f1621f306033adcc74d22fd57c7", "self_test_pulses": 0},
			],
			"observations": {
				"display_indices_seen": [0, 1, 2, 3],
				"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 2}, {"type": 526, "width": 5, "height": 7, "depth": 2}],
				"lamp_addresses_seen": list(range(1, 79)) + [80], "solenoid_addresses_seen": [1, 15, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32, 45, 46, 47, 48], "gi_addresses_seen": [0],
			},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/ripleys", "sha256": "d389ced56f57bccd2704758cdac167b56d0a6f1621f306033adcc74d22fd57c7", "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def main() -> None:
	partial_path = spatial_partial_path(ROOT / "machines/partial/stern/ripley-s-believe-it-or-not-2004.json")
	if partial_path.exists():
		existing = load_json(partial_path)
		if any("spatial" in device for device in [*existing.get("inputs", []), *existing.get("outputs", [])]):
			raise RuntimeError("Refusing to clobber reviewed Ripley's spatial placements; run tools/curate_ripleys_spatial.py for the spatial overlay")
	write_json(partial_path, fail_closed_spatial_partial(build()))
	write_json(ROOT / "evidence/runtime/whitestar/ripleys-boot-start-and-gameplay.json", runtime_evidence())
	write_text(ROOT / "knowledge/stern/ripley-s-believe-it-or-not-2004.md", fail_closed_spatial_knowledge("stern.ripley-s-believe-it-or-not.2004", KNOWLEDGE))


if __name__ == "__main__":
	main()
