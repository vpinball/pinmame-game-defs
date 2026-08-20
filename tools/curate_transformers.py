"""Build fail-closed Transformers Pro and Limited Edition partial definitions."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT
SOURCE_ROOT = ROOT / "src"
TOOLS = Path(__file__).resolve().parent
for import_root in (SOURCE_ROOT, TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import file_sha256, write_json, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path
from transformers_pro_spatial_evidence import CANDIDATE_REGISTER_RELATIVE_PATH, load_candidate_register, spatial_review_markdown


CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {
	driver["id"]: driver
	for driver in sorted(CATALOG["drivers"], key=lambda item: item["id"])
	if driver["id"].startswith("tf_")
}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.transformers-pro-le.2011"
EXCERPT_ROOT = REPOSITORY_ROOT / "evidence/excerpts/stern.transformers-pro.2011"
LE_EXCERPT_ROOT = REPOSITORY_ROOT / "evidence/excerpts/stern.transformers-limited-edition.2011"
PRO_VPX_SOURCE = "vpx.transformers-pro-vpw-2.3.1"
PRO_VPX_TABLE_SOURCE = "vpx-table.transformers-pro-sg1bson-mod-of-jpsalas-1.0.0"
PRO_SPATIAL_REGISTER_SOURCE = "evidence.transformers-pro-spatial-candidate-register"
PRO_VPX_TABLE_SHA256 = "c4615c93a4cb16b794308d65867015805a58b332b4f93fb995209c05107242cc"
PRO_VPX_TABLE_URI = "external:pinmame-vpx-sources/stern/transformers-pro-2011/source/Transformers (Stern 2011) SG1bsoN Mod.vpx"
PRO_MANUAL_LOCATOR = "Combined official 134-page Stern manual: Pro switch chart PDF page 129 and switch locations 130, coil/flasher chart 131 and coil/flasher locations 132, lamp matrix chart 133 and physical lamp locations 134; physical inventory and multiplicity authority"
REVIEW_SOURCE = "review.pinball-news.transformers.2011"
PRODUCT_SOURCE = "stern.transformers-product-page"
PRO_RUNTIME_SOURCE = "runtime.transformers-pro.boot-start"
LE_RUNTIME_SOURCE = "runtime.transformers-limited-edition.boot-start"


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


COMMON_SWITCHES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	1: ("Bumblebee target", "microswitch", True, ()), 2: ("Energon left target", "microswitch", True, ()),
	3: ("Allspark left eject", "microswitch", False, ("ball.loaded",)), 4: ("Left ramp entrance", "opto", True, ()),
	5: ("Left orbit bottom", "leaf", False, ()), 6: ("Left orbit top", "leaf", False, ()),
	7: ("Right top lane", "leaf", False, ()), 8: ("Left top lane", "leaf", False, ()),
	10: ("Left ramp exit", "opto", True, ()), 11: ("Center lane", "leaf", False, ()),
	12: ("Right orbit", "leaf", False, ()), 13: ("Right ramp back door", "microswitch", False, ()),
	15: ("Tournament start", "button", False, ()), 16: ("Start", "button", False, ()),
	18: ("Trough 4 left", "microswitch", False, ("ball.position",)), 19: ("Trough 3", "microswitch", False, ("ball.position",)),
	20: ("Trough 2", "microswitch", False, ("ball.position",)), 21: ("Trough 1 right", "microswitch", False, ("ball.position",)),
	22: ("Trough jam", "opto", False, ("ball.position",)), 23: ("Shooter lane", "microswitch", False, ("ball.position",)),
	24: ("Left outlane", "leaf", False, ()), 25: ("Left return lane", "leaf", False, ()),
	26: ("Left slingshot", "leaf", True, ()), 27: ("Right slingshot", "leaf", True, ()),
	28: ("Right return lane", "leaf", False, ()), 29: ("Right outlane", "leaf", False, ()),
	30: ("Top pop bumper", "leaf", True, ()), 31: ("Right pop bumper", "leaf", True, ()),
	32: ("Bottom pop bumper", "leaf", True, ()), 34: ("Right orbit spinner", "other", True, ()),
	35: ("Right ramp entrance", "opto", True, ()), 37: ("Right two-bank bottom target", "microswitch", True, ()),
	38: ("Megatron lock 4", "microswitch", False, ("ball.position",)), 39: ("Megatron lock 3", "microswitch", False, ("ball.position",)),
	40: ("Megatron lock 2", "microswitch", False, ("ball.position",)), 41: ("Megatron lock 1", "microswitch", False, ("ball.position",)),
	42: ("Megatron lock jam", "opto", False, ("ball.position",)), 43: ("Optimus ramp up", "microswitch", False, ("position.up",)),
	44: ("Optimus ramp down", "microswitch", False, ("position.down",)), 45: ("Bumblebee captive ball", "microswitch", True, ()),
	46: ("Energon right target", "microswitch", True, ()), 49: ("Energon center target", "microswitch", True, ()),
	50: ("Right two-bank top target", "microswitch", True, ()), 51: ("Optimus Prime target", "microswitch", True, ()),
}
PRO_SWITCH_OVERRIDES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {14: ("Right ramp exit", "opto", False, ())}
LE_SWITCH_OVERRIDES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	47: ("Megatron down", "microswitch", False, ("position.down",)), 48: ("Megatron up", "microswitch", False, ("position.up",)),
	52: ("Right ramp exit", "opto", False, ()), 53: ("Starscream target", "microswitch", True, ()),
	54: ("Left ramp entrance top", "opto", True, ()), 56: ("Ironhide mini-playfield opto 3", "opto", False, ("ball.position",)),
	57: ("Ironhide mini-playfield opto 4", "opto", False, ("ball.position",)), 59: ("Ironhide mini-playfield opto 2", "opto", False, ("ball.position",)),
	62: ("Ironhide mini-playfield opto 1", "opto", False, ("ball.position",)), 64: ("Megatron drop target", "microswitch", True, ()),
}
SAM_DEDICATED_ROLES = {
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth",
	84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos",
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}


def matrix_switch(number: int, limited_edition: bool) -> dict[str, object]:
	specs = COMMON_SWITCHES | (LE_SWITCH_OVERRIDES if limited_edition else PRO_SWITCH_OVERRIDES)
	spec = specs.get(number)
	used = spec is not None
	label = spec[0] if used else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	sources = (MANUAL_SOURCE, REVIEW_SOURCE) if limited_edition else (MANUAL_SOURCE, PRO_VPX_SOURCE)
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)), "normally_closed": False,
		"pulse": bool(spec[2]) if used else False, "availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if used else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance("validated", *(sources if used else (MANUAL_SOURCE,))),
	}
	roles = list(spec[3]) if used else []
	if number == 15:
		roles.append("cabinet.tournament-start")
	elif number == 16:
		roles.append("cabinet.start")
	if roles:
		result["roles"] = roles
	return result


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, sources: tuple[str, ...]) -> dict[str, object]:
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"), "normally_closed": normally_closed,
		"pulse": False, "availability": availability, "physical": {"switch_type": switch_type},
		"provenance": provenance("validated", *sources),
	}
	if availability in {"used", "optional"} and device in SAM_DEDICATED_ROLES:
		result["roles"] = [SAM_DEDICATED_ROLES[device]]
	return result


def inputs(limited_edition: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, limited_edition) for number in range(1, 65)]
	semantic_sources = (MANUAL_SOURCE, REVIEW_SOURCE, CORE_SOURCE) if limited_edition else (MANUAL_SOURCE, PRO_VPX_SOURCE, CORE_SOURCE)
	manual_sources = (MANUAL_SOURCE, CORE_SOURCE)
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Starscream left limit" if limited_edition else "Unused dedicated switch D7", "used" if limited_edition else "unused", "microswitch" if limited_edition else "unknown", False),
		(72, 8, "Starscream right limit" if limited_edition else "Unused dedicated switch D8", "used" if limited_edition else "unused", "microswitch" if limited_edition else "unknown", False),
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
		items.append(dedicated_switch(device, manual_number, label, availability, switch_type, normally_closed, semantic_sources if availability == "used" else manual_sources))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated", MANUAL_SOURCE, CORE_SOURCE)})
	return items


PRO_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Megatron lock eject", "coil", "used"),
	4: ("Unused Pro output 4", "coil", "unused"), 5: ("Orbit control gate", "coil", "used"), 6: ("Unused Pro output 6", "coil", "unused"),
	7: ("Unused Pro output 7", "coil", "unused"), 8: ("Shaker motor", "motor", "optional"), 9: ("Top pop bumper", "coil", "used"),
	10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"), 12: ("Optimus Prime bash solenoid", "coil", "used"),
	13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"), 15: ("Left flipper", "coil", "used"),
	16: ("Right flipper", "coil", "used"), 17: ("Decepticon flasher", "flasher", "used"), 18: ("Left ramp flasher", "flasher", "used"),
	19: ("Right-side flasher", "flasher", "used"), 20: ("Bumblebee flasher", "flasher", "used"), 21: ("Pop-bumper flasher", "flasher", "used"),
	22: ("Allspark left eject", "coil", "used"), 23: ("Right ramp flasher", "flasher", "used"), 24: ("Coin meter", "coil", "optional"),
	25: ("Center lane arrow flasher", "flasher", "used"), 26: ("Left slingshot flasher", "flasher", "used"), 27: ("Right slingshot flasher", "flasher", "used"),
	28: ("Megatron flasher", "flasher", "used"), 29: ("Unused Pro output 29", "flasher", "unused"), 30: ("Optimus Prime ramp motor relay", "relay", "used"),
	31: ("Optimus Prime flasher", "flasher", "used"), 32: ("Allspark flasher", "flasher", "used"),
}
LE_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Megatron lock eject", "coil", "used"),
	4: ("Left orbit gate", "coil", "used"), 5: ("Right orbit gate", "coil", "used"), 6: ("Megatron drop target down", "coil", "used"),
	7: ("Megatron drop target up", "coil", "used"), 8: ("Shaker motor", "motor", "optional"), 9: ("Top pop bumper", "coil", "used"),
	10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"), 12: ("Ironhide mini-playfield control gate", "coil", "used"),
	13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"), 15: ("Left flipper", "coil", "used"),
	16: ("Right flipper", "coil", "used"), 17: ("Decepticon flasher", "flasher", "used"), 18: ("Left ramp flasher", "flasher", "used"),
	19: ("Right-side flasher", "flasher", "used"), 20: ("Right ramp flasher", "flasher", "used"), 21: ("Pop-bumper flasher", "flasher", "used"),
	22: ("Allspark left eject", "coil", "used"), 23: ("Backpanel right flasher", "flasher", "used"), 24: ("Coin meter", "coil", "optional"),
	25: ("Center lane arrow flasher", "flasher", "used"), 26: ("Megatron figure motor relay", "relay", "used"), 27: ("Slingshot flasher", "flasher", "used"),
	28: ("Megatron flasher", "flasher", "used"), 29: ("Bumblebee flasher", "flasher", "used"), 30: ("Optimus Prime ramp motor relay", "relay", "used"),
	31: ("Optimus Prime flasher", "flasher", "used"), 32: ("Allspark flasher", "flasher", "used"),
}
MAIN_CONTROL = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
MAIN_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J8-P11", "J8-P12", "J8-P14", "J8-P15", "J8-P16", "J8-P17", "J8-P18", "J8-P19", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	alias_namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(alias_namespace, address, manual_address), "availability": availability, "provenance": provenance("validated", *sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def main_wiring(address: int, limited_edition: bool) -> dict[str, object]:
	if address == 8:
		power_wire, power_connection, voltage, voltage_type = "RED-WHT", "J17-P7", 16, "ac"
	elif address in (15, 16):
		power_wire, power_connection, voltage, voltage_type = "GRY-YEL / RED-YEL", "J10-P6/7", 50, "dc"
	elif address <= 16:
		power_wire, power_connection, voltage, voltage_type = "YEL-VIO", "J10-P9/10", 50, "dc"
	elif address == 24 and not limited_edition:
		power_wire, power_connection, voltage, voltage_type = "RED", "J16-P4-8", 5, "dc"
	elif address == 24:
		power_wire, power_connection, voltage, voltage_type = "ORG", "J16-P4", 20, "dc"
	elif address in ({26, 29, 30} if limited_edition else {22, 30}):
		power_wire, power_connection, voltage, voltage_type = "BRN", "J7-P1", 20, "dc"
	else:
		power_wire, power_connection, voltage, voltage_type = "ORG", "J6-P10", 20, "dc"
	return {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "power_wire": power_wire, "power_connection": power_connection, "nominal_voltage_v": voltage, "voltage_type": voltage_type, "control_wire": MAIN_CONTROL[address - 1], "control_connection": MAIN_CONNECTION[address - 1]}


def main_outputs(limited_edition: bool) -> list[dict[str, object]]:
	chart = LE_COILS if limited_edition else PRO_COILS
	sources = (MANUAL_SOURCE, REVIEW_SOURCE, CORE_SOURCE) if limited_edition else (MANUAL_SOURCE, PRO_VPX_SOURCE, REVIEW_SOURCE)
	items = []
	for address, (label, kind, availability) in chart.items():
		physical = None
		if not limited_edition and address == 4:
			physical = {"notes": "The official Pro chart leaves Q4 unused. The proven VPX script registers a left-gate callback for shared table code, but physical review confirms that second controlled gate is LE-only."}
		elif address == 24:
			physical = {"notes": "The edition-specific service chart is authoritative: LE powers this optional Q24 circuit from ORG/J16-P4 at 20 VDC, while the Pro supplement specifies RED/J16-P4-8 at 5 VDC."}
		items.append(output(address, label, kind, availability, sources if availability != "unused" else (MANUAL_SOURCE, REVIEW_SOURCE), manual_address=str(address), physical=physical, wiring=main_wiring(address, limited_edition)))
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, runtime_source), physical={"notes": "PinMAME's SAM_FASTFLIPSOL synthetic output. It gates low-latency flipper handling and is not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	return items


AUX_OUTPUTS = {
	59: ("Starscream platform motor", "motor", "Q41", "YEL-BRN", "J2-P4"),
	60: ("Starscream motor direction relay", "relay", "Q42", "YEL-RED", "J2-P3"),
	61: ("Megatron cannon recoil", "coil", "Q43", "YEL-ORG", "J2-P7"),
	62: ("Optimus Prime bash solenoid", "coil", "Q44", "YEL-BLK", "J2-P4"),
	63: ("Ironhide mini-playfield left", "coil", "Q45", "YEL-GRN", "J2-P3"),
	64: ("Ironhide mini-playfield right", "coil", "Q46", "YEL-BLU", "J2-P7"),
}


def le_aux_outputs() -> list[dict[str, object]]:
	items = []
	for address in range(51, 67):
		if address in AUX_OUTPUTS:
			label, kind, transistor, control_wire, power_connection = AUX_OUTPUTS[address]
			wiring = {"board": "520-5325-01 12-transistor auxiliary driver board", "driver_transistor": transistor, "power_wire": "BRN", "power_connection": power_connection, "nominal_voltage_v": 20, "voltage_type": "dc", "control_wire": control_wire}
			items.append(output(address, label, kind, "used", (MANUAL_SOURCE, REVIEW_SOURCE, CORE_SOURCE, LE_RUNTIME_SOURCE), manual_address=transistor, wiring=wiring))
		else:
			physical_address = f"Q{address}" if address <= 56 else None
			notes = "Public compatibility slot is not populated by Transformers LE hardware."
			if 51 <= address <= 56:
				notes = f"Public output {address} corresponds to unpopulated auxiliary transistor Q{address}; installed Q41-Q46 serialize as public 59-64."
			items.append(output(address, f"Unused auxiliary output {address}", "coil", "unused", (MANUAL_SOURCE, CORE_SOURCE), manual_address=physical_address, physical={"notes": notes}, output_id=f"device.unused-auxiliary-{address}"))
	return items


PRO_LAMPS = {
	1: "Start", 2: "Tournament start", 3: "Roll Out", 4: "Devastator", 5: "Blackout", 6: "Shockwave", 7: "Starscream", 8: "Left outlane",
	9: "Left return lane", 10: "Right return lane", 11: "Right outlane", 12: "Allspark X", 13: "Allspark purple", 14: "Allspark red", 15: "Allspark orange", 16: "Left orbit X",
	17: "Left orbit purple", 18: "Left orbit red", 19: "Left orbit orange", 20: "Right two-bank bottom", 21: "Right two-bank top", 22: "Optimus Prime", 23: "Bumblebee", 24: "Ironhide",
	25: "Mudflap and Skids", 26: "Ratchet", 27: "Megatron", 28: "Sentinel Prime", 29: "Challenge Megatron", 30: "Bumblebee captive ball", 31: "Right ramp X", 32: "Right ramp purple",
	33: "Right ramp red", 34: "Right ramp orange", 35: "Energon right", 36: "Right orbit X", 37: "Right orbit purple", 38: "Right orbit red", 39: "Right orbit orange", 40: "Center lane orange",
	41: "Center lane red", 42: "Center lane purple", 43: "Center lane X", 44: "Left ramp orange", 45: "Left ramp red", 46: "Left ramp purple", 47: "Left ramp X", 48: "Energon left",
	49: "Top lane red bottom", 50: "Top lane purple bottom", 51: "Top lane purple top", 52: "Top lane red top", 53: "Special", 54: "Energon center", 55: "Extra Ball", 57: "Megatron bottom",
	58: "Megatron top", 59: "Optimus Prime challenge", 60: "Top pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper",
}
LE_LAMPS = {
	17: "Ratchet", 18: "Mudflap and Skids", 19: "Ironhide", 20: "Bumblebee", 21: "Optimus Prime", 22: "Megatron", 23: "Starscream", 24: "Shockwave",
	25: "Blackout", 26: "Devastator", 27: "Right outlane", 28: "Right return lane", 29: "Right two-bank bottom", 30: "Right two-bank top", 31: "Sentinel Prime", 32: "Shoot Again and Roll Out",
	33: "Right orbit orange", 34: "Right orbit red", 35: "Right orbit purple", 36: "Right orbit X", 37: "Right ramp X", 38: "Right ramp purple", 39: "Right ramp red", 40: "Right ramp orange",
	41: "Center lane X", 42: "Center lane purple", 43: "Center lane red", 44: "Center lane orange", 45: "Energon right", 46: "Bumblebee captive ball", 47: "Energon center", 48: "Megatron top",
	49: "Allspark orange", 50: "Allspark red", 51: "Allspark purple", 52: "Allspark X", 53: "Left ramp X", 54: "Left ramp purple", 55: "Left ramp red", 56: "Left ramp orange",
	57: "Ironhide mini-playfield 3", 58: "Ironhide mini-playfield 2", 59: "Ironhide mini-playfield 1", 61: "Left outlane", 62: "Left return lane", 63: "Energon left", 64: "Challenge Megatron",
	65: "Left orbit X", 66: "Left orbit purple", 67: "Left orbit red", 68: "Left orbit orange", 69: "Top lane purple top", 70: "Top lane purple bottom", 71: "Top lane red top", 72: "Top lane red bottom",
	73: "Optimus Prime challenge", 74: "Special", 75: "Extra Ball", 76: "Tournament start button", 77: "Top pop bumper", 78: "Bottom pop bumper", 79: "Right pop bumper", 80: "Start button",
}


def lamps(limited_edition: bool) -> list[dict[str, object]]:
	chart = LE_LAMPS if limited_edition else PRO_LAMPS
	sources = (MANUAL_SOURCE, LE_RUNTIME_SOURCE) if limited_edition else (MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE)
	items = []
	for address in range(1, 81):
		label = chart.get(address, f"Unused {'LE' if limited_edition else 'Pro'} lamp {address}")
		availability = "used" if address in chart else "unused"
		physical = {"notes": "Limited Edition feature/insert lighting is distributed through the documented LED boards and SAM lamp channels."} if limited_edition and availability == "used" else None
		items.append(output(address, label, "lamp", availability, sources if availability == "used" else (MANUAL_SOURCE,), "pinmame.output.lamp", physical=physical, output_id=f"lamp.{slug(label)}-{address}"))
	items.append(output(0, "General illumination master", "gi", "used", sources, "pinmame.output.gi", "GI-0", output_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None, assembly_part_number: str | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance("validated", *sources)}
	if positions:
		result["positions"] = positions
	if assembly_part_number:
		result["assembly_part_number"] = assembly_part_number
	return result


def common_mechanisms(limited_edition: bool) -> list[dict[str, object]]:
	behavior_sources = (MANUAL_SOURCE, REVIEW_SOURCE) if limited_edition else (MANUAL_SOURCE, PRO_VPX_SOURCE, REVIEW_SOURCE)
	optimus_actuator = "device.optimus-prime-bash-solenoid"
	mechanisms = [
		mechanism("mechanism.trough", "Four-ball trough", "other", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right", "switch.trough-jam"], "Four balls occupy switches 18-21 from left to right. Output 1 advances the rightmost ball through jam opto 22 toward shooter lane switch 23. The harness scenarios deliberately seed 18-21 from this proven physical initial state; the seed itself is not treated as a ROM observation.", behavior_sources),
		mechanism("mechanism.auto-launcher", "Auto launcher and manual plunger", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches a ball held at shooter-lane switch 23. Preserve the cabinet's manual plunger path as well as ROM-controlled auto launch.", behavior_sources),
		mechanism("mechanism.megatron-lock", "Megatron four-ball mini-trough", "other", ["device.megatron-lock-eject"], ["switch.megatron-lock-4", "switch.megatron-lock-3", "switch.megatron-lock-2", "switch.megatron-lock-1", "switch.megatron-lock-jam"], "The four-position vertical mini-trough stacks balls at switches 41, 40, 39, and 38, with jam opto 42 on the exit path. Output 3 fires one ball at a time; multiball release can pulse rapidly enough to eject the stack sequentially.", behavior_sources, assembly_part_number="511-6977-00"),
		mechanism("mechanism.allspark-eject", "Allspark left eject", "kicker", ["device.allspark-left-eject"], ["switch.allspark-left-eject"], "Switch 3 remains active while the Allspark saucer holds a ball. Output 22 ejects it back onto the playfield.", behavior_sources),
		mechanism("mechanism.optimus-ramp", "Optimus Prime motorized ramp", "motorized", ["device.optimus-prime-ramp-motor-relay"], ["switch.optimus-ramp-up", "switch.optimus-ramp-down"], "The ramp normally sits down and feeds a curved lane into the right orbit. Output 30 powers a motor/cam that raises its rear so a fast shot jumps into the Optimus toy; switches 43 and 44 report the fully up and fully down endpoints, and neither endpoint switch should be asserted in transit.", behavior_sources, positions=[{"id": "position.down", "label": "Down / right-orbit route", "sensors": ["switch.optimus-ramp-down"]}, {"id": "position.up", "label": "Raised / Optimus jump", "sensors": ["switch.optimus-ramp-up"]}]),
		mechanism("mechanism.optimus-bash-toy", "Optimus Prime bash toy", "toy", [optimus_actuator], ["switch.optimus-prime-target"], "A ball jumping from the raised ramp strikes the target in Optimus Prime's left leg at switch 51. The dedicated solenoid under the right foot rocks the figure; it is not a third flipper.", behavior_sources),
		mechanism("mechanism.bumblebee-captive-ball", "Bumblebee captive-ball and target area", "toy", [], ["switch.bumblebee-target", "switch.bumblebee-captive-ball"], "Switch 45 senses the captive ball and switch 1 senses the adjacent Bumblebee standup. The car and captive ball are passive playfield elements without a controller actuator.", behavior_sources),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", ["device.top-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.top-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Top, right, and bottom pop output/switch pairs are 9/30, 10/31, and 11/32.", behavior_sources),
		mechanism("mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left and right slings use output/switch pairs 13/26 and 14/27.", behavior_sources),
		mechanism("mechanism.flippers", "Two-flipper assembly", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "Outputs 15/16 drive the lower left/right flippers. Dedicated public inputs 84/83 are the left button/normally-closed EOS pair and 82/81 are the right pair. No upper or third flipper is installed.", behavior_sources),
		mechanism("mechanism.spinner", "Right-orbit spinner", "rotary", [], ["switch.right-orbit-spinner"], "Each rotation pulse of the passive spinner closes switch 34.", behavior_sources),
		mechanism("mechanism.targets", "Standup targets and right two-bank", "other", [], ["switch.bumblebee-target", "switch.energon-left-target", "switch.energon-right-target", "switch.energon-center-target", "switch.right-two-bank-bottom-target", "switch.right-two-bank-top-target"], "The Energon targets are 2, 46, and 49; Bumblebee is 1; the right-side two-bank is 37 bottom and 50 top. These are standups, not resettable drop targets.", behavior_sources),
		mechanism("mechanism.ramps-orbits-and-lanes", "Ramps, orbits, and top lanes", "other", [], ["switch.left-ramp-entrance", "switch.left-ramp-exit", "switch.left-orbit-bottom", "switch.left-orbit-top", "switch.right-orbit", "switch.right-orbit-spinner", "switch.right-ramp-entrance", "switch.right-ramp-back-door", "switch.right-ramp-exit", "switch.center-lane", "switch.right-top-lane", "switch.left-top-lane"], "Switches 4/10 bracket the left ramp, 35 and the edition-specific exit address bracket the right ramp, 5/6 sense the left orbit, 12 the right orbit, 34 its spinner, 7/8 the top lanes, and 11 the center lane. The Optimus ramp changes one upper route but does not replace these sensors.", behavior_sources),
		mechanism("mechanism.optional-shaker", "Optional shaker motor", "motorized", ["device.shaker-motor"], [], "Output 8 is the optional 16 VAC shaker installation and may be absent from a stock machine.", behavior_sources),
	]
	return mechanisms


def pro_mechanisms() -> list[dict[str, object]]:
	sources = (MANUAL_SOURCE, PRO_VPX_SOURCE, REVIEW_SOURCE)
	items = common_mechanisms(False)
	items.insert(4, mechanism("mechanism.orbit-gate", "Right/top orbit control gate", "gate", ["device.orbit-control-gate"], [], "Output 5 opens the single controlled orbit gate installed on the Pro. Output 4 is physically unused; the extra left rollover-lane gate is LE-only even though the shared VPX script registers a convenience callback at 4.", sources))
	return items


def le_mechanisms() -> list[dict[str, object]]:
	sources = (MANUAL_SOURCE, REVIEW_SOURCE, CORE_SOURCE)
	items = common_mechanisms(True)
	items.insert(4, mechanism("mechanism.orbit-gates", "Left and right controlled orbit gates", "gate", ["device.left-orbit-gate", "device.right-orbit-gate"], [], "LE outputs 4 and 5 independently control the additional left rollover-lane gate and the right/top orbit gate. Neither gate has an endpoint sensor.", sources))
	items.extend([
		mechanism("mechanism.megatron-drop-target", "Megatron motorized drop target", "drop_target_bank", ["device.megatron-drop-target-down", "device.megatron-drop-target-up"], ["switch.megatron-down", "switch.megatron-up", "switch.megatron-drop-target"], "The single target guards the Megatron lock entrance. Switch 64 reports a ball strike; outputs 6 and 7 drive it down and up, while switches 47 and 48 confirm the corresponding endpoints.", sources, positions=[{"id": "position.down", "label": "Dropped", "sensors": ["switch.megatron-down"]}, {"id": "position.up", "label": "Raised", "sensors": ["switch.megatron-up"]}]),
		mechanism("mechanism.megatron-figure-and-cannon", "Megatron animated figure and cannon recoil", "toy", ["device.megatron-figure-motor-relay", "device.megatron-cannon-recoil"], [], "Main output 26 powers the Megatron figure motor. Auxiliary public output 61/physical Q43 kicks the cannon for recoil in coordination with the separate Megatron-lock mechanism's output-3 ejection; the ball exits from the trough and does not physically travel through the cannon barrel.", sources),
		mechanism("mechanism.starscream", "Starscream rotating target platform", "rotary", ["device.starscream-platform-motor", "device.starscream-motor-direction-relay"], ["switch.starscream-left-limit", "switch.starscream-right-limit", "switch.starscream-target"], "Public outputs 59/60 map to auxiliary Q41/Q42 and power/reverse the platform motor. Dedicated D7/D8 serialize as public switches 71/72 and stop the mechanism at its left/right limits. Rotation alternately exposes or blocks the target behind Starscream's legs; switch 53 reports a hit.", sources, positions=[{"id": "position.left", "label": "Left limit", "sensors": ["switch.starscream-left-limit"]}, {"id": "position.right", "label": "Right limit", "sensors": ["switch.starscream-right-limit"]}], assembly_part_number="511-6979-00"),
		mechanism("mechanism.ironhide-mini-playfield", "Ironhide player-controlled mini-playfield", "motorized", ["device.ironhide-mini-playfield-control-gate", "device.ironhide-mini-playfield-left", "device.ironhide-mini-playfield-right"], ["switch.ironhide-mini-playfield-opto-1", "switch.ironhide-mini-playfield-opto-2", "switch.ironhide-mini-playfield-opto-3", "switch.ironhide-mini-playfield-opto-4"], "Output 12 opens the controlled entry gate. During the feature, the flipper buttons command public outputs 63/64 (physical Q45/Q46) to tilt the playfield left/right. Four optos at public 62, 59, 56, and 57 sense ball zones; the exit returns the ball to the right-ramp route. The tilting surface itself has no endpoint switches.", sources),
	])
	return items


LE_DRIVER_IDS = {driver_id for driver_id, driver in DRIVERS.items() if "Limited Edition" in driver["description"]}
PRO_DRIVER_IDS = {driver_id for driver_id, driver in DRIVERS.items() if driver["description"].startswith("Transformers (")}
if LE_DRIVER_IDS | PRO_DRIVER_IDS != set(DRIVERS) or LE_DRIVER_IDS & PRO_DRIVER_IDS:
	raise ValueError("Transformers drivers must classify exhaustively as Pro or Limited Edition")


def driver_records(limited_edition: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		if (driver_id in LE_DRIVER_IDS) != limited_edition:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision within the Limited Edition physical playfield; I/O and mechanisms are unchanged." if limited_edition else "Firmware revision for this Pro physical playfield; the PinMAME clone parent is an LE software-lineage artifact and does not change compatibility with this definition."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def transformers_manual_source(limited_edition: bool) -> dict[str, object]:
	manual_uri = "https://wp.sternpinball.com/wp-content/uploads/2018/11/Transformers-Manual-LE.pdf" if limited_edition else "https://wp.sternpinball.com/wp-content/uploads/2018/11/Transformers-Manual.pdf"
	manual_name = "Transformers-Manual-LE.pdf" if limited_edition else "Transformers-Manual.pdf"
	manual_locator = "Combined 134-page official Stern manual: Limited Edition switches PDF page 60, coils 62-63, lamps 65, and custom assemblies 36-39; Pro supplement switches 129, coils 131, and lamps 133" if limited_edition else PRO_MANUAL_LOCATOR
	base: dict[str, object] = {
		"id": MANUAL_SOURCE,
		"kind": "manual",
		"uri": manual_uri,
		"sha256": "9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8",
		"locator": manual_locator,
		"license": "NOASSERTION",
		"attribution": "Stern Pinball",
		"source_id": "stern",
		"original_filename": manual_name,
		"rights": "NOASSERTION",
		"acquired_at": "2026-08-02T21:00:42Z",
	}
	common_entries = [
		(EXCERPT_ROOT, "meg-ball-trap-assembly", "excerpt.transformers-pro.meg-ball-trap-assembly", "PDF page 36, MEG BALL TRAP ASSEMBLY 511-6977-00", "Transformers-Manual.pdf page 36, crop box 0.04,0.05,0.96,0.92, scanned page rendered at its native resolution (embedded image xref 163, 1684px across 11.69in), rendered at 56 dpi, capped to 600px wide, grayscale, 601x401 WebP quality 30"),
		(EXCERPT_ROOT, "meg-ptegt-assembly", "excerpt.transformers-pro.meg-ptegt-assembly", "PDF page 37, MEG PTEGT ASSEMBLY 511-6978-00", "Transformers-Manual.pdf page 37, crop box 0.04,0.05,0.96,0.92, scanned page rendered at its native resolution (embedded image xref 168, 1684px across 11.69in), rendered at 56 dpi, capped to 600px wide, grayscale, 601x401 WebP quality 30"),
		(EXCERPT_ROOT, "starscream-target-assembly", "excerpt.transformers-pro.starscream-target-assembly", "PDF page 38, STARSCREAM TARGET ASSEMBLY 511-6979-00", "Transformers-Manual.pdf page 38, crop box 0.04,0.05,0.96,0.92, scanned page rendered at its native resolution (embedded image xref 173, 1684px across 11.69in), rendered at 56 dpi, capped to 600px wide, grayscale, 601x401 WebP quality 30"),
		(EXCERPT_ROOT, "back-panel-assembly", "excerpt.transformers-pro.back-panel-assembly", "PDF page 39, BACK PANEL ASSEMBLY 500-7205-01", "Transformers-Manual.pdf page 39, crop box 0.04,0.05,0.96,0.92, scanned page rendered at its native resolution (embedded image xref 177, 1190px across 8.26in), rendered at 105 dpi, capped to 800px wide, grayscale, rotated 270 degrees counter-clockwise, 1072x801 WebP quality 40"),
	]
	if limited_edition:
		entries = common_entries + [
			(LE_EXCERPT_ROOT, "le-switch-matrix", "excerpt.transformers-le.switch-matrix", "PDF page 60, LIMITED EDITION SWITCH MATRIX GRID", "Transformers-Manual.pdf page 60, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 275, 1684px across 11.69in), rendered at 82 dpi, capped to 900px wide, grayscale, 901x609 WebP quality 35"),
			(LE_EXCERPT_ROOT, "le-switch-locations", "excerpt.transformers-le.switch-locations", "PDF page 61, LIMITED EDITION SWITCH LOCATIONS", "Transformers-Manual.pdf page 61, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 280, 1190px across 8.26in), rendered at 84 dpi, capped to 650px wide, grayscale, 651x881 WebP quality 25"),
			(LE_EXCERPT_ROOT, "le-coil-chart", "excerpt.transformers-le.coil-chart", "PDF page 62, LIMITED EDITION COILS DETAILED CHART Q1-Q32", "Transformers-Manual.pdf page 62, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 285, 1190px across 8.26in), rendered at 103 dpi, capped to 800px wide, grayscale, 801x1085 WebP quality 28"),
			(LE_EXCERPT_ROOT, "le-auxiliary-coils", "excerpt.transformers-le.auxiliary-coils", "PDF page 63, LIMITED EDITION AUXILIARY COILS Q41-Q46", "Transformers-Manual.pdf page 63, crop box 0.04,0.05,0.96,0.4, scanned page rendered at its native resolution (embedded image xref 289, 1190px across 8.26in), rendered at 105 dpi, capped to 800px wide, grayscale, 801x432 WebP quality 40"),
			(LE_EXCERPT_ROOT, "le-coil-locations", "excerpt.transformers-le.coil-locations", "PDF page 64, LIMITED EDITION COIL & FLASH LAMP LOCATIONS", "Transformers-Manual.pdf page 64, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 293, 1190px across 8.26in), rendered at 90 dpi, capped to 700px wide, grayscale, 701x949 WebP quality 30"),
			(LE_EXCERPT_ROOT, "le-lamp-matrix", "excerpt.transformers-le.lamp-matrix", "PDF page 65, LIMITED EDITION LAMP MATRIX GRID", "Transformers-Manual.pdf page 65, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 298, 1684px across 11.69in), rendered at 82 dpi, capped to 900px wide, grayscale, 901x609 WebP quality 35"),
			(LE_EXCERPT_ROOT, "le-lamp-locations", "excerpt.transformers-le.lamp-locations", "PDF page 66, LIMITED EDITION LAMP LOCATIONS", "Transformers-Manual.pdf page 66, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 302, 1190px across 8.26in), rendered at 84 dpi, capped to 650px wide, grayscale, 651x881 WebP quality 25"),
		]
	else:
		entries = common_entries + [
			(EXCERPT_ROOT, "pro-switch-matrix", "excerpt.transformers-pro.pro-switch-matrix", "PDF page 129, PRO SWITCH MATRIX GRID", "Transformers-Manual.pdf page 129, crop box 0.04,0.05,0.96,0.78, scanned page rendered at its native resolution (embedded image xref 592, 1684px across 11.69in), rendered at 74 dpi, capped to 800px wide, grayscale, 801x450 WebP quality 30"),
			(EXCERPT_ROOT, "pro-switch-locations", "excerpt.transformers-pro.pro-switch-locations", "PDF page 130, PRO SWITCH LOCATIONS", "Transformers-Manual.pdf page 130, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 597, 1190px across 8.26in), rendered at 84 dpi, capped to 650px wide, grayscale, 651x881 WebP quality 25"),
			(EXCERPT_ROOT, "pro-coil-chart", "excerpt.transformers-pro.pro-coil-chart", "PDF page 131, PRO COILS DETAILED CHART TABLE", "Transformers-Manual.pdf page 131, crop box 0.04,0.05,0.96,0.86, scanned page rendered at its native resolution (embedded image xref 602, 1190px across 8.26in), rendered at 92 dpi, capped to 700px wide, grayscale, 701x873 WebP quality 28"),
			(EXCERPT_ROOT, "pro-coil-locations", "excerpt.transformers-pro.pro-coil-locations", "PDF page 132, PRO COIL & FLASH LAMP LOCATIONS", "Transformers-Manual.pdf page 132, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 607, 1190px across 8.26in), rendered at 84 dpi, capped to 650px wide, grayscale, 651x881 WebP quality 24"),
			(EXCERPT_ROOT, "pro-lamp-matrix", "excerpt.transformers-pro.pro-lamp-matrix", "PDF page 133, PRO LAMP MATRIX GRID", "Transformers-Manual.pdf page 133, crop box 0.04,0.06,0.96,0.78, scanned page rendered at its native resolution (embedded image xref 612, 1684px across 11.69in), rendered at 74 dpi, capped to 800px wide, grayscale, 801x444 WebP quality 30"),
			(EXCERPT_ROOT, "pro-lamp-locations", "excerpt.transformers-pro.pro-lamp-locations", "PDF page 134, PRO LAMP LOCATIONS", "Transformers-Manual.pdf page 134, crop box 0.03,0.04,0.97,0.94, scanned page rendered at its native resolution (embedded image xref 617, 1190px across 8.26in), rendered at 84 dpi, capped to 650px wide, grayscale, 651x881 WebP quality 24"),
		]
	excerpts = []
	for excerpt_root, stem, excerpt_id, locator, derivation in entries:
		markdown = excerpt_root / f"{stem}.md"
		image = excerpt_root / f"{stem}.webp"
		if not markdown.is_file() or not image.is_file():
			raise FileNotFoundError(f"Transformers manual excerpt is missing: {markdown} or {image}")
		excerpts.append({
			"id": excerpt_id,
			"locator": locator,
			"path": str(markdown.relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
			"sha256": hashlib.sha256(markdown.read_bytes()).hexdigest(),
			"image": str(image.relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
			"image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
			"image_derivation": derivation,
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		})
	base["excerpts"] = excerpts
	return base


def sources(limited_edition: bool) -> list[dict[str, object]]:
	manual_uri = "https://wp.sternpinball.com/wp-content/uploads/2018/11/Transformers-Manual-LE.pdf" if limited_edition else "https://wp.sternpinball.com/wp-content/uploads/2018/11/Transformers-Manual.pdf"
	manual_name = "Transformers-Manual-LE.pdf" if limited_edition else "Transformers-Manual.pdf"
	manual_locator = "Combined 134-page official Stern manual: Limited Edition switches PDF page 60, coils 62-63, lamps 65, and custom assemblies 36-39; Pro supplement switches 129, coils 131, and lamps 133" if limited_edition else PRO_MANUAL_LOCATOR
	result = [
		transformers_manual_source(limited_edition),
		{"id": REVIEW_SOURCE, "kind": "human_review", "uri": "https://www.pinballnews.com/games/transformers/index6a.html", "locator": "Contemporaneous detailed physical review: Pro/LE playfield differences; Optimus ramp and switches; Megatron trough, target and cannon; Starscream rotation; Ironhide mini-playfield; controlled gates; lamps", "license": "NOASSERTION", "attribution": "Pinball News", "acquired_at": "2026-08-02T22:00:00Z"},
		{"id": PRODUCT_SOURCE, "kind": "human_review", "uri": "https://www.sternpinball.com/game/transformers/", "locator": "Manufacturer product feature inventory and physical edition overview", "license": "NOASSERTION", "attribution": "Stern Pinball", "acquired_at": "2026-08-02T22:00:00Z"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Transformers INITGAME/driver family, SAM_2COL, 12-output auxiliary-board serialization, PWM lamp declarations, and 128x32 DMD", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames Transformers driver records", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	]
	if limited_edition:
		result.append({"id": LE_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/transformers-limited-edition/harness/boot-start.raw.json", "revision": PINMAME_REVISION, "sha256": "b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7", "locator": "Exact tf_180h boot/start scenario with switches 18-21 initialized, four coin pulses, and start; ROM archive SHA-256 0ce389603bb0ccc237e71937ddadb8a5534f2499fdf610f6ec4087bdf29d22f4", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"})
	else:
		result.extend([
			{"id": PRO_VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Transformers%20Pro%20%28Stern%202011%29%20v.2.3.1.vbs", "revision": VPX_REVISION, "sha256": "987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b", "locator": "Transformers Pro (Stern 2011) v.2.3.1.vbs: tf_180 controller, trough/launcher/ejects, solenoid callbacks, gates, flippers, Megatron lock, Optimus ramp motor and endpoint switches, bash toy, switches, lamps, and GI", "license": "NOASSERTION", "attribution": "VPW and table authors credited in the script; vpxtable_scripts contributors"},
			{"id": PRO_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/transformers-pro/harness/boot-start.raw.json", "revision": PINMAME_REVISION, "sha256": "5f7c0caa85b1b5b8799e6cceef8e7d9ec7d9ddd63f0b8364ab5e9168c88443da", "locator": "Exact tf_180 boot/start scenario with switches 18-21 initialized, four coin pulses, and start; ROM archive SHA-256 8689f01315ad4f6b7001c7a99147093c64297631104610a7ac03e34152e8f352", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		])
	return result


def build(limited_edition: bool) -> dict[str, object]:
	machine_id = "stern.transformers-limited-edition.2011" if limited_edition else "stern.transformers-pro.2011"
	name = "Transformers Limited Edition" if limited_edition else "Transformers Pro"
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": machine_id, "name": name, "manufacturer": "Stern", "year": 2011, "kind": "physical_pinball", "ipdb_id": 5753 if limited_edition else 5709, "opdb_id": "GRnPz-Mx0XO" if limited_edition else "GRnPz-MLBzV"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(limited_edition), "inputs": inputs(limited_edition), "outputs": main_outputs(limited_edition) + (le_aux_outputs() if limited_edition else []) + lamps(limited_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, runtime_source)}],
		"mechanisms": le_mechanisms() if limited_edition else pro_mechanisms(), "relationships": [], "sources": sources(limited_edition),
		"knowledge": {"path": f"knowledge/stern/{'transformers-limited-edition-2011' if limited_edition else 'transformers-pro-2011'}.md", "status": "complete"}, "conflicts": [],
	}


PRO_KNOWLEDGE = """# Transformers Pro (Stern, 2011)

Coverage: **author-ready - physical inventory, PinMAME bindings, mechanism behavior, and edition differences validated**

## Identity and evidence precedence

This definition covers non-`h` PinMAME drivers `tf_120`, `tf_140`, `tf_150`, `tf_160`, `tf_170`, and `tf_180`. They are mutually compatible Pro firmware even though the clone graph points at the `tf_180h` Limited Edition root; that parent records software lineage, not physical compatibility. The known-working `Transformers Pro (Stern 2011) v.2.3.1.vbs` is ground truth for public controller addresses, callbacks, ball routing, and mechanism causality. The official Pro service supplement governs physical channels and wiring. Pinned PinMAME governs SAM serialization and the native 128x32 four-bit DMD.

## Controller topology and initial state

The SAM switch matrix is public 1-64. Dedicated cabinet inputs are 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. The four-ball trough starts with switches 18-21 closed and jam opto 22 downstream. Main outputs are public 1-32, standard lamps 1-80, and aggregate GI 0. The Pro does not install the Limited Edition auxiliary board.

## Resolved output-4 VPX exception

The proven script registers callbacks for two orbit gates at outputs 4 and 5 because it shares mechanism code with fuller editions. The official Pro coil chart marks output 4 unused, and physical-machine review states that the additional left rollover-lane gate is an LE feature. A physical Pro recreation must therefore leave Q4 unused and build only the right/top orbit gate on output 5. This is a narrow physical-wiring correction; all other public controller semantics continue to follow the working script.

## Megatron mini-trough

The Megatron assembly is a four-position vertical mini-trough, not a single saucer. Balls stack at switches 41, 40, 39, and 38, with switch 42 guarding the exit. Output 3 ejects one ball at a time and may be pulsed in rapid succession for multiball. Build the complete stack and single-file exit so ROM lock accounting matches physical occupancy. The manual identifies the ball-trap assembly as `511-6977-00`.

## Optimus Prime

Output 30 powers the ramp motor relay. With the ramp down, the shot enters a curved lane and continues toward the right orbit; when raised, the rear of the ramp becomes a jump into Optimus Prime. Switches 43/44 are the full-up/full-down limits and both should be open in transit. The working script models intermediate collision ramps rather than teleporting the ball, which is the correct construction principle for a digital recreation. Switch 51 in the left leg senses the hit, and output 12 actuates a solenoid under the right foot to rock the figure. Output 12 is a toy coil, not a third flipper.

## Allspark, Bumblebee, and standard ball devices

The Allspark saucer holds a ball on switch 3 and ejects through output 22. Output 2 auto-launches from shooter switch 23 while retaining a manual plunger path. Bumblebee uses standup switch 1 and captive-ball switch 45; the car and captive ball have no controlled actuator. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 13/26 and 14/27. The passive right-orbit spinner pulses switch 34. The two physical flippers are outputs 15/16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed.

## Ramps, targets, lamps, and flashers

Switches 4/10 bracket the left ramp. The Pro right ramp uses entrance 35, back-door 13, and exit 14. The left orbit uses 5/6, right orbit 12, top lanes 7/8, and center lane 11. Energon standups are 2/46/49, the right two-bank is 37/50, and Bumblebee is 1. All 80 lamp addresses are explicit: 1-55 and 57-62 are used according to the Pro chart; 56 and 63-80 are unused. Flashers and toy/ball-device outputs are enumerated separately from lamps so authors do not infer physical type from PinMAME transport group.

## Author construction checklist

- Build the four-ball trough, shooter/manual plunger, auto launcher, Megatron four-ball stack/eject, Allspark eject, single orbit gate, motorized Optimus ramp with two limits, Optimus bash toy, Bumblebee captive-ball area, two flippers, three pops, two slings, spinner, both ramps, both orbits, top lanes, center lane, targets, and optional shaker.
- Bind every input, main output, lamp, GI 0, and DMD from the JSON; retain explicit unused channels and the physical Q4 exception.
- Preserve ball occupancy and endpoint causality. Do not replace the Megatron stack with a pulse-only toy or the Optimus ramp with a cosmetic animation.
- Use the proven VPX force, timing, and animation choices as starting values while keeping the service-manual wiring and physical edition boundary.

## Sources

- `manual.transformers-pro-le.2011`: official combined Stern manual, SHA-256 `9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8`; Pro switch chart/locations, coil-flasher chart/locations, and lamp chart/locations are PDF pages 129/130, 131/132, and 133/134 respectively.
- `vpx.transformers-pro-vpw-2.3.1`: known-working Pro script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b`.
- `vpx-table.transformers-pro-sg1bson-mod-of-jpsalas-1.0.0`: retained SG1bsoN Mod derivative of JP's 1.0.0, SHA-256 `c4615c93a4cb16b794308d65867015805a58b332b4f93fb995209c05107242cc`; a 2022 save revision 156 geometry candidate, not asserted known-working.
- `review.pinball-news.transformers.2011`: contemporaneous physical mechanism and edition-difference review.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and driver family.
"""


def curated_pro_partial(root: Path = ROOT) -> dict[str, object]:
	"""Build the single canonical fail-closed Pro output owned by this curator."""
	load_candidate_register(root)
	definition = build(False)
	definition["sources"].append({
		"id": PRO_VPX_TABLE_SOURCE,
		"kind": "vpx_table",
		"uri": PRO_VPX_TABLE_URI,
		"sha256": PRO_VPX_TABLE_SHA256,
		"locator": "SG1bsoN Mod derivative of JP's Transformers v1.0.0 by jpsalas: table save revision 156, saved 2022-02-08; embedded tf_180 Pro table; exact 952 by 2164 playfield bounds; extracted read-only with vpxtool git:v0.33.3. The retained derivative is geometry candidate evidence only; no cited observation establishes it as known-working.",
		"license": "NOASSERTION",
		"attribution": "JP Salas original v1.0.0; SG1bsoN 2022 lighting-mod derivative and credited table authors",
		"original_filename": "Transformers (Stern 2011) SG1bsoN Mod.vpx",
		"rights": "NOASSERTION",
		"known_working": False,
	})
	definition["sources"].append({
		"id": PRO_SPATIAL_REGISTER_SOURCE,
		"kind": "human_review",
		"uri": f"evidence:{CANDIDATE_REGISTER_RELATIVE_PATH.relative_to('evidence').as_posix()}",
		"sha256": file_sha256(root / CANDIDATE_REGISTER_RELATIVE_PATH),
		"locator": "Portable fail-closed register for the exact SG1bsoN VPX extraction, including both Q20 render candidates, Q32 raw geometry, GI candidate anchors, coordinate-space labels, manual supplement gaps, and unresolved dispositions.",
		"license": "NOASSERTION",
		"attribution": "Generated from the retained user-authorized VPX extraction and official Stern manual",
	})
	return fail_closed_spatial_partial(definition)


def curated_pro_knowledge(root: Path = ROOT) -> str:
	"""Build the canonical fail-closed Pro knowledge note."""
	return fail_closed_spatial_knowledge(
		"stern.transformers-pro.2011",
		PRO_KNOWLEDGE.replace(
			"## Sources\n\n",
			f"{spatial_review_markdown(root)}## Sources\n\n- `{CANDIDATE_REGISTER_RELATIVE_PATH.as_posix()}`: portable spatial candidate register, SHA-256 `{file_sha256(root / CANDIDATE_REGISTER_RELATIVE_PATH)}`; records exact artifact hashes, coordinate spaces, and unresolved Q20/Q32/GI dispositions.\n",
			1,
		),
	)


LE_KNOWLEDGE = """# Transformers Limited Edition (Stern, 2011)

Coverage: **author-ready - physical inventory, PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers Limited Edition drivers `tf_088h`, `tf_100h`, `tf_120h`, `tf_130h`, `tf_140h`, `tf_150h`, and root `tf_180h`. Firmware dates in the PinMAME catalog extend into 2012/2013, but the physical product is the 2011 Limited Edition. The official Stern service charts govern complete I/O and wiring; the exact `tf_180h` harness validates the SAM address stream, native DMD, GI, and installed auxiliary output mapping; contemporary physical review supplies mechanism behavior that the diagnostic charts do not explain. No public proven LE VPX table was found, so no Pro-only table behavior is silently promoted to LE.

## Controller topology and auxiliary serialization

Matrix switches are public 1-64; dedicated controls are 65-72, 81-88, and -7 through 0; DIP inputs are 1-8. Main outputs are 1-32, lamps 1-80, and GI 0. The installed 12-transistor auxiliary board uses physical Q41-Q46, which PinMAME serializes as public outputs 59-64. Public 51-56 represent unpopulated Q51-Q56 and 57/58 plus 65/66 are compatibility gaps; all ten are explicit unused entries. The exact-ROM boot run observes public 63 active, corroborating Q45 to public 63 rather than a naive Q45 to 55 mapping.

## Megatron system

The four-ball mini-trough is common with the Pro: switches 41, 40, 39, and 38 sense the stack, switch 42 senses the exit, and output 3 ejects one ball per pulse. The LE adds a motorized drop target at the entrance: switch 64 senses a hit, outputs 6/7 drive down/up, and switches 47/48 confirm those endpoints. Main output 26 powers movement of the Megatron figure. Auxiliary public 61/physical Q43 kicks the cannon in recoil as the trough ejects; the ball never travels through the barrel. The ball-trap assembly is `511-6977-00`.

## Starscream platform

The Starscream target platform rotates to alternately expose or block the target between the figure's legs. Public outputs 59/60 map to Q41/Q42 and supply motor power and direction relay. Dedicated limits D7/D8 appear to PinMAME as public 71/72 and stop left/right travel; switch 53 is the target. Model the two sensed endpoints and unsensed transit rather than treating output state as position. The manual identifies assembly `511-6979-00` and a 40-degree mechanical reference.

## Ironhide mini-playfield

Output 12 controls entry to the mini-playfield. During the feature, the player uses the flipper buttons to command public outputs 63/64 (physical Q45/Q46), tilting the surface left or right. Four optos sense the ball at public addresses 62, 59, 56, and 57; none is a surface endpoint. The exit rejoins the right-ramp route. A recreation must separately model the controlled gate, tilting body, ball-on-body motion, four opto zones, and fall-through/exit geometry.

## Optimus Prime and orbit gates

The Optimus ramp matches the Pro: output 30 drives the motor relay, switch 43 is full up, and 44 full down. Down routes the ball into the curved/right-orbit lane; up creates the jump into Optimus. Switch 51 senses the target in the left leg. Because LE main output 12 belongs to Ironhide, the Optimus rocking solenoid moves to auxiliary public 62/physical Q44. The LE also has two controlled gates: output 4 for the additional left rollover-lane gate and output 5 for the right/top orbit gate.

## Lamps and other playfield inventory

The LE service chart uses lamps 17-59 and 61-80; 1-16 and 60 are unused. Many feature and insert lights are implemented on dedicated LED boards, so preserve address identity even if a digital recreation renders a modern light source. The Allspark eject is switch/output 3/22, auto launch is 23/2, pops are 30-32 with outputs 9-11, slings are 26/27 with outputs 13/14, and the spinner is 34. The machine has two flippers on outputs 15/16; output 12 is the Ironhide gate, never a flipper.

## Author construction checklist

- Build every common Pro ball path plus the second orbit gate, Megatron drop target/figure/cannon, Starscream rotating platform, and Ironhide controlled/tilting mini-playfield.
- Implement the auxiliary address translation exactly: public 59-64 are physical Q41-Q46, with 51-58 and 65-66 explicit unused compatibility positions.
- Preserve the four-ball Megatron stack, all motor endpoints, Starscream limits, Ironhide ball optos, and Optimus route change as causal state, not cosmetic animation.
- Keep the official manual files in the external organized cache; both official URLs currently resolve to byte-identical 134-page PDFs and are retained under their separate machine identities.

## Spatial retrofit blocker register

The normalized playfield placement gate remains fail-closed. The ordered local search found only `Transformers (Stern 2011) SG1bsoN Mod.vpx` in the primary tables folder and `Transformers (Stern 2011) v1 mod 1.vpx` in the archive; both identify JP's **Pro** recreation and embed `tf_180`, so neither can provide LE geometry. The archived `Transformers G1 Generation One (TBA 2018).vpx` is unrelated community content and is excluded. Browser escalation identified the [VPUniverse detail mod](https://vpuniverse.com/files/file/6355-transformers-stern-2011-detail-mod/) and [VPForums JP table](https://www.vpforums.org/index.php?app=downloads&showfile=13612) as Pro candidates only; no exact LE VPX or LE controller script was identified.

The manual, exact `tf_180h` runtime harness, and physical review establish LE inventory, wiring, multiplicity, and custom-mechanism causality, but they do not establish normalized VPX/player-view coordinates for every LE sensor, effect, lamp/GI/flasher emitter, or moving assembly. In particular, Starscream, Ironhide, the Megatron drop-target/cannon assembly, and the additional LE gate cannot be located from the Pro frame without violating the edition boundary. Keep `coverage.status` as `partial` and `coverage.missing` as `spatial_placement` until an exact LE source with an LE driver identity and visibly matching playfield is acquired and reconciled.

## Sources

- `manual.transformers-pro-le.2011`: official combined Stern manual, SHA-256 `9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8`; LE switches/coils/lamps on PDF pages 60/62-63/65 and custom assemblies on 36-39.
- `review.pinball-news.transformers.2011`: detailed physical operation of Starscream, Megatron, Optimus, Ironhide, and the edition-only gate.
- `runtime.transformers-limited-edition.boot-start`: exact `tf_180h` ROM harness, SHA-256 `b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM auxiliary serialization, display, and driver family.
"""


def runtime_evidence(limited_edition: bool) -> dict[str, object]:
	game = "tf_180h" if limited_edition else "tf_180"
	machine_id = "stern.transformers-limited-edition.2011" if limited_edition else "stern.transformers-pro.2011"
	raw_hash = "b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7" if limited_edition else "5f7c0caa85b1b5b8799e6cceef8e7d9ec7d9ddd63f0b8364ab5e9168c88443da"
	rom_hash = "0ce389603bb0ccc237e71937ddadb8a5534f2499fdf610f6ec4087bdf29d22f4" if limited_edition else "8689f01315ad4f6b7001c7a99147093c64297631104610a7ac03e34152e8f352"
	lamps_seen = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80] if limited_edition else [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62]
	solenoids_seen = [26, 30, 33, 63] if limited_edition else [30, 33]
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": [machine_id], "driver_ids": [game],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": game, "command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>", "rom_archive_sha256": rom_hash, "raw_runs": [{"name": "boot-start", "sha256": raw_hash, "self_test_pulses": 0}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": lamps_seen, "solenoid_addresses_seen": solenoids_seen, "gi_addresses_seen": [0]}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/{'transformers-limited-edition' if limited_edition else 'transformers-pro'}/harness", "sha256": raw_hash, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def write_pending_machine(limited_edition: bool, root: Path) -> None:
	filename = "transformers-limited-edition-2011.json" if limited_edition else "transformers-pro-2011.json"
	machine_id = "stern.transformers-limited-edition.2011" if limited_edition else "stern.transformers-pro.2011"
	if machine_id not in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		return
	if (root / "machines/author-ready/stern" / filename).exists():
		return
	definition_path = spatial_partial_path(root / "machines/partial/stern" / filename)
	definition = fail_closed_spatial_partial(build(True)) if limited_edition else curated_pro_partial(root)
	knowledge_filename = filename.removesuffix(".json") + ".md"
	knowledge = fail_closed_spatial_knowledge(machine_id, LE_KNOWLEDGE) if limited_edition else curated_pro_knowledge(root)
	write_json(definition_path, definition)
	write_text(root / "knowledge/stern" / knowledge_filename, knowledge)


def regenerate(root: Path) -> None:
	write_pending_machine(False, root)
	write_pending_machine(True, root)
	write_json(root / "evidence/runtime/sam/transformers-pro-boot-start.json", runtime_evidence(False))
	write_json(root / "evidence/runtime/sam/transformers-limited-edition-boot-start.json", runtime_evidence(True))


def main() -> None:
	regenerate(ROOT)


if __name__ == "__main__":
	main()
