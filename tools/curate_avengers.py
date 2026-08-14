"""Build author-ready Avengers Pro and Limited Edition machine definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json as write_json_file, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path
try:
	from avengers_le_spatial import apply_spatial, spatial_audit
except ModuleNotFoundError:
	# Direct execution puts tools/ on sys.path; module-oriented callers use
	# the repository namespace package instead.
	from tools.avengers_le_spatial import apply_spatial, spatial_audit


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("avs_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
LE_MANUAL = "manual.avengers-limited-edition"
PRO_MANUAL = "manual.avengers-pro"
LE_SCRIPT = "vpx.avengers-le.jp-salas-v600"
PRO_SCRIPT = "vpx.avengers-pro.vpw-1-3-1"
LE_RUNTIME = "runtime.avengers-le.boot-start"
PRO_RUNTIME = "runtime.avengers-pro.boot-start"

LE_DRIVER_IDS = {"avs_120h", "avs_140h", "avs_170h", "avs_170hc"}
PRO_DRIVER_IDS = {"avs_110", "avs_140", "avs_170", "avs_170c"}

# This base generator owns the fail-closed LE bundle.  Pro definitions and
# knowledge may be built from the pure helpers below, but their files belong
# to the separately reviewed Pro curation flow and are deliberately absent
# from this output manifest.
LE_MACHINE_ID = "stern.avengers-limited-edition.2012"
LE_PARTIAL_PATH = Path("machines/partial/stern/avengers-limited-edition-2012.json")
LE_AUTHOR_READY_PATH = Path("machines/author-ready/stern/avengers-limited-edition-2012.json")
LE_EVIDENCE_PATH = Path("evidence/runtime/sam/avengers-limited-edition-boot-start.json")
LE_KNOWLEDGE_PATH = Path("knowledge/stern/avengers-limited-edition-2012.md")
LE_SPATIAL_AUDIT_PATH = Path("reports/spatial/stern/avengers-limited-edition-2012.json")
LE_LEGACY_STUB_PATHS = (
	Path("machines/stubs/avs_170h.json"),
	Path("knowledge/stubs/avs_170h.md"),
)


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

COMMON_SWITCHES: dict[int, tuple[str, str, bool, bool]] = {
	7: ("Tesseract standup #1", "microswitch", True, False),
	10: ("Left top lane", "microswitch", True, False),
	11: ("Center top lane", "microswitch", True, False),
	12: ("Right top lane", "microswitch", True, False),
	13: ("Tesseract standup #3", "microswitch", True, False),
	14: ("Tesseract standup #2", "microswitch", True, False),
	15: ("Tournament start", "button", False, False),
	16: ("Start", "button", False, False),
	24: ("Left outlane", "microswitch", True, False),
	25: ("Left return lane", "microswitch", True, False),
	26: ("Left slingshot", "leaf", True, False),
	27: ("Right slingshot", "leaf", True, False),
	28: ("Right return lane", "microswitch", True, False),
	29: ("Right outlane", "microswitch", True, False),
	30: ("Left pop bumper", "leaf", True, False),
	31: ("Right pop bumper", "leaf", True, False),
	32: ("Bottom pop bumper", "leaf", True, False),
	33: ("Left inner loop", "microswitch", True, False),
	34: ("Shield target", "microswitch", True, False),
	35: ("Right 2-bank target top", "microswitch", True, False),
	36: ("Right 2-bank target bottom", "microswitch", True, False),
	41: ("Hulk wheel opto #1", "opto", True, False),
	42: ("Hulk wheel opto #2", "opto", True, False),
	43: ("Left ramp exit", "microswitch", True, False),
	44: ("Center spinner", "other", True, False),
	45: ("Tesseract wheel #1", "opto", True, False),
	46: ("Tesseract wheel #2", "opto", True, False),
	47: ("Left orbit", "microswitch", True, False),
	48: ("Right ramp exit", "microswitch", True, False),
	49: ("Loki lock 1 bottom", "opto", False, True),
	50: ("Loki lock 2", "opto", False, True),
	51: ("Loki lock 3", "opto", False, True),
	52: ("(H)ULK drop target", "microswitch", False, False),
	53: ("H(U)LK drop target", "microswitch", False, False),
	54: ("HU(L)K drop target", "microswitch", False, False),
	55: ("HUL(K) drop target", "microswitch", False, False),
	57: ("Hulk platter", "microswitch", False, False),
	62: ("Hulk eject", "microswitch", False, False),
	63: ("Hulk target", "microswitch", True, False),
}


def switch_specs(limited_edition: bool) -> dict[int, tuple[str, str, bool, bool]]:
	specs = dict(COMMON_SWITCHES)
	for number, letter in enumerate(("(T)HOR", "T(H)OR", "TH(O)R", "THO(R)"), start=1):
		specs[number] = (f"{letter} {'drop target' if limited_edition else 'target'}", "microswitch", not limited_edition, False)
	if limited_edition:
		specs.update({
			8: ("Bridge motor down", "microswitch", False, False),
			9: ("Bridge motor up", "microswitch", False, False),
			17: ("Trough #6 left", "microswitch", False, False),
			18: ("Trough #5", "microswitch", False, False),
			19: ("Trough #4", "microswitch", False, False),
			20: ("Trough #3", "microswitch", False, False),
			21: ("Trough #2", "microswitch", False, False),
			22: ("Trough #1 right", "microswitch", False, False),
			23: ("Trough jam", "microswitch", False, False),
			58: ("Right orbit", "microswitch", True, False),
		})
	else:
		specs.update({
			18: ("Trough #4 left", "microswitch", False, False),
			19: ("Trough #3", "microswitch", False, False),
			20: ("Trough #2", "microswitch", False, False),
			21: ("Trough #1 right", "microswitch", False, False),
			22: ("Trough jam", "microswitch", False, False),
			23: ("Shooter lane", "microswitch", False, False),
			61: ("Right orbit", "microswitch", True, False),
		})
	return specs


def matrix_switch(number: int, manual: str, script: str, limited_edition: bool) -> dict[str, object]:
	specs = switch_specs(limited_edition)
	spec = specs.get(number)
	used = spec is not None
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	result = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": spec[3] if spec else False, "pulse": spec[2] if spec else False,
		"availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if spec else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(manual, script),
	}
	if not limited_edition and number in {18, 19, 20, 21}:
		result["roles"] = ["ball.position"]
	elif not limited_edition and number == 22:
		result["roles"] = ["ball.jam"]
	if limited_edition and number == 58:
		result["physical"]["notes"] = "Runtime causality identifies sw58 as the right-orbit callback, but the LE physical switch-location drawing marks the disputed upper-right-orbit coordinate 61. Spatial placement is withheld pending address reconciliation."
		result["provenance"] = {"status": "conflicted", "source_refs": [manual, script]}
	if limited_edition and number == 61:
		result.update({
			"id": "switch.unresolved-upper-right-orbit-address",
			"label": "Unresolved upper-right orbit address",
			"availability": "unknown",
			"physical": {
				"switch_type": "unknown",
				"notes": "The LE physical switch-location drawing marks the disputed upper-right-orbit coordinate 61, while the manual switch matrix grid and known-working LE VPX script identify 58. This address is neither promoted nor classified unused.",
			},
			"provenance": {"status": "conflicted", "source_refs": [manual, script]},
		})
	return result


def conflicts(limited_edition: bool, manual: str, script: str) -> list[dict[str, object]]:
	if not limited_edition:
		return []
	return [{
		"id": "conflict.le-upper-right-orbit-address",
		"path": "inputs[pinmame.input.switch:58|61]",
		"description": "The official LE physical switch-location drawing marks the disputed upper-right-orbit coordinate as switch 61, while the same manual's switch matrix grid identifies switch 58 as RIGHT ORBIT and the known-working LE VPX script drives sw58 without a sw61 handler. The address mapping cannot be reconciled without guessing, so both spatial placements and the unused classification for 61 are withheld. Resolution path: a LibPinMAME Switch Test trace against a legal avs_170h ROM holding public 58 and then 61 and recording the name the ROM prints for each, which shows whether this firmware names any device at 61 at all; or, decisively, a continuity check by an owner or operator with the playfield raised, reading whether the upper-right-orbit switch's return lead is the TAN-RED wire on J12-P8 recorded here for 58 or the TAN-GRN wire on J12-P4 recorded here for 61. Unresolved.",
		"source_refs": [manual, script],
	}]


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, manual: str, script: str) -> dict[str, object]:
	refs = (manual, script, CORE_SOURCE) if availability != "unused" else (manual, CORE_SOURCE)
	return {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": normally_closed, "pulse": False, "availability": availability,
		"physical": {"switch_type": switch_type}, "provenance": provenance(*refs),
	}


def inputs(manual: str, script: str, limited_edition: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, manual, script, limited_edition) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "used", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left flipper button", "used", "button", False), (83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False), (81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False), (87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Shooter lane" if limited_edition else "Unused dedicated switch D15", "used" if limited_edition else "unused", "microswitch" if limited_edition else "unknown", False),
		(85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "used", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for args in dedicated:
		items.append(dedicated_switch(*args, manual, script))
	for number in range(1, 9):
		items.append({
			"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch",
			"binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"),
			"availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"},
			"provenance": provenance(manual, CORE_SOURCE),
		})
	return items


COMMON_MAIN_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"),
	3: ("Hulk counterclockwise", "motor", "used"), 4: ("Hulk clockwise", "motor", "used"),
	5: ("Hulk eject", "coil", "used"), 7: ("Left orbit control gate", "coil", "used"),
	8: ("Shaker motor", "motor", "optional"), 9: ("Left pop bumper", "coil", "used"),
	10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"),
	18: ("Left-side flasher", "flasher", "used"), 19: ("Right-side flasher", "flasher", "used"),
	20: ("Slingshot flashers", "flasher", "used"), 21: ("Hulk flasher", "flasher", "used"),
	24: ("Coin meter", "coil", "optional"), 25: ("Pop-bumper flasher", "flasher", "used"),
	26: ("Tesseract flasher", "flasher", "used"), 27: ("Backpanel left flasher", "flasher", "used"),
	28: ("Backpanel flasher #2", "flasher", "used"), 29: ("Backpanel flasher #3", "flasher", "used"),
	30: ("Backpanel flasher #4", "flasher", "used"), 31: ("Backpanel flasher #5", "flasher", "used"),
	32: ("Backpanel right flasher", "flasher", "used"),
}

PRO_MAIN_OVERRIDES = {
	6: ("Center 4-bank drop reset", "coil", "used"), 12: ("Left ramp control gate", "coil", "used"),
	17: ("Hulk arms", "motor", "used"), 22: ("Loki lockup", "coil", "used"), 23: ("Hulk magnet", "magnet", "used"),
}
LE_MAIN_OVERRIDES = {
	6: ("Left 4-bank drop reset", "coil", "used"), 12: ("Loki lockup", "coil", "used"),
	17: ("Blue GI LED relay", "relay", "used"), 22: ("Bridge motor", "motor", "used"), 23: ("Bridge motor relay", "relay", "used"),
}

MAIN_CONTROL = [
	"BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY",
	"BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO",
	"VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-WHT", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY",
	"BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY",
]
MAIN_CONTROL_CONNECTION = [
	"J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9",
	"J8-P11", "J8-P12", "J8-P14", "J8-P15", "J8-P16", "J8-P17", "J8-P18", "J8-P19",
	"J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10",
	"J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8",
]

MAIN_PARTS = {
	1: "26-1200 / 090-5044-ND", 2: "24-940 / 090-5036-ND", 3: "23-800 / 090-5001-ND", 4: "23-600 / 090-5001-ND",
	5: "26-1200 / 090-5044-ND", 6: "25-1240 / 090-5034-ND", 7: "32-1250 / 090-5060-01-ND", 8: "502-5027-00",
	9: "26-1200 / 090-5044-ND", 10: "26-1200 / 090-5044-ND", 11: "26-1200 / 090-5044-ND", 13: "26-1200 / 090-5044-ND",
	14: "26-1200 / 090-5044-ND", 15: "22-1080 / 090-5032-ND", 16: "22-1080 / 090-5032-ND",
}


def main_wiring(address: int, limited_edition: bool) -> dict[str, object]:
	if address <= 7 or 9 <= address <= 16:
		power_wire, power_connection, voltage, voltage_type = "YEL-VIO", "J10-P9/10", 50, "dc"
	elif address == 8:
		power_wire, power_connection, voltage, voltage_type = "RED-WHT", "J17-P7", 16, "ac"
	elif address in (17, 22) or (limited_edition and address == 23):
		power_wire, power_connection, voltage, voltage_type = "BRN", "J7-P1", 20, "dc"
	elif address == 23:
		power_wire, power_connection, voltage, voltage_type = "VIO-YEL", "J10-P8", 50, "dc"
	elif address == 24:
		power_wire, power_connection, voltage, voltage_type = "RED", "J16-P4-8", 5, "dc"
	else:
		power_wire, power_connection, voltage, voltage_type = "ORG", "J6-P10", 20, "dc"
	return {
		"board": "I/O Power Driver board", "driver_transistor": f"Q{address}",
		"power_wire": power_wire, "power_connection": power_connection, "control_wire": MAIN_CONTROL[address - 1],
		"control_connection": MAIN_CONTROL_CONNECTION[address - 1], "nominal_voltage_v": voltage, "voltage_type": voltage_type,
	}


def output(address: int, label: str, kind: str, availability: str, group: str, refs: tuple[str, ...], manual_address: str, output_id: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None) -> dict[str, object]:
	result: dict[str, object] = {
		"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"aliases": aliases("pinmame.lamp" if group.endswith("lamp") else "pinmame.gi" if group.endswith("gi") else "pinmame.solenoid", address, manual_address),
		"availability": availability, "provenance": provenance(*refs),
	}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


LE_AUX = {
	51: (41, "Center 4-bank drop reset", "coil", "used", "25-1240 / 090-5034-ND", "YEL-VIO", "ORG-GRY", 50),
	52: (42, "Right ramp control gate", "coil", "used", "32-1800 / 515-8595-01-ND", "YEL-VIO", "ORG-RED", 50),
	53: (43, "Left ramp control gate", "coil", "used", "32-1800 / 515-8595-01-ND", "YEL-VIO", "ORG-BLU", 50),
	54: (44, "Hulk magnet", "magnet", "used", "22-650 / 090-5076-00", "VIO-YEL", "ORG-BRN", 50),
	55: (45, "Green GI LED relay", "relay", "used", "190-5004-00", "GRY", "ORG-GRN", 20),
	56: (46, "Hulk arms", "motor", "used", "24-940 / 090-5036-ND-NLB", "YEL-VIO", "ORG-BLK", 50),
	57: (47, "Right orbit control gate", "coil", "used", "32-1250 / 090-5060-01-ND", "YEL-VIO", "ORG-VIO", 50),
	58: (48, "Red GI LED relay", "relay", "used", "190-5004-00", "GRY", "ORG-YEL", 20),
}


def coils(manual: str, script: str, limited_edition: bool) -> list[dict[str, object]]:
	coil_specs = dict(COMMON_MAIN_COILS)
	coil_specs.update(LE_MAIN_OVERRIDES if limited_edition else PRO_MAIN_OVERRIDES)
	items = []
	for address in range(1, 33):
		label, kind, availability = coil_specs[address]
		physical: dict[str, object] = {"location": "Playfield, cabinet, or backpanel as shown on the manual coil-location map"}
		part = MAIN_PARTS.get(address)
		if part:
			physical["part_number"] = part
		refs = (manual, script, CORE_SOURCE) if availability != "unused" else (manual, CORE_SOURCE)
		items.append(output(address, label, kind, availability, "pinmame.output.solenoid", refs, str(address), physical=physical, wiring=main_wiring(address, limited_edition)))
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", "pinmame.output.solenoid", (CORE_SOURCE, LE_RUNTIME if limited_edition else PRO_RUNTIME), "33", output_id="virtual.game-on", physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}))
	if limited_edition:
		for public_address, (physical_address, label, kind, availability, part, power_wire, control_wire, voltage) in LE_AUX.items():
			items.append(output(
				public_address, label, kind, availability, "pinmame.output.solenoid", (manual, script, CORE_SOURCE), str(physical_address),
				physical={"part_number": part, "location": "Avengers LE eight-transistor auxiliary driver assembly"},
				wiring={"board": "520-5325-00 eight-transistor auxiliary driver board", "driver_transistor": f"Q{public_address - 50}", "power_wire": power_wire, "control_wire": control_wire, "nominal_voltage_v": voltage, "voltage_type": "dc"},
			))
	else:
		for address, label in ((53, "Unpopulated LE left-ramp gate channel"), (54, "Unpopulated LE Hulk-magnet channel")):
			items.append(output(address, label, "virtual", "unused", "pinmame.output.solenoid", (PRO_MANUAL, PRO_RUNTIME, CORE_SOURCE), str(address), output_id=f"virtual.unpopulated-le-channel-{address}", physical={"notes": "The shared Pro ROM toggled this LE-compatible custom channel during the isolated run, but the Pro cabinet has no corresponding auxiliary board transistor or physical device."}))
	return items


LE_LAMPS = {
	1: "THO(R)", 2: "TH(O)R", 3: "T(H)OR", 4: "(T)HOR", 5: "Captain America", 6: "Thor", 7: "Hawkeye", 8: "Hulk",
	9: "Black Widow", 10: "Iron Man", 11: "Tesseract standup", 12: "Left inner loop red", 14: "Left return lane", 15: "Left outlane",
	16: "Shoot again", 17: "Captain America #1 bottom", 18: "Captain America #2", 19: "Captain America #3", 20: "Captain America #4",
	21: "Hulk target arrow", 22: "Special", 23: "Left orbit purple", 24: "Hawkeye #4", 25: "Hawkeye #3", 26: "Hawkeye #2",
	27: "Hawkeye #1 bottom", 28: "Black Widow #4", 29: "Black Widow #3", 30: "Black Widow #2", 31: "Left ramp red",
	32: "Black Widow #1 bottom", 33: "HUL(K)", 34: "HU(L)K", 35: "H(U)LK", 36: "(H)ULK", 37: "Extra ball",
	38: "Tesseract standup left", 39: "Tesseract standup right", 40: "Right 2-bank target top", 41: "Right 2-bank target bottom",
	42: "Right return lane", 43: "Right outlane", 44: "Left ramp green", 45: "Lock 3", 46: "Lock 2", 47: "Lock 1",
	48: "Hulk eject green", 49: "(C)OSMIC", 50: "C(O)SMIC", 51: "CO(S)MIC", 52: "COS(M)IC", 53: "COSM(I)C", 54: "COSMI(C)",
	55: "Start button", 56: "Tournament start", 57: "Tesseract #1", 58: "Tesseract #2", 59: "Tesseract #3", 60: "Tesseract #4",
	61: "Tesseract #5", 62: "Bottom pop bumper", 63: "Left pop bumper", 64: "Right pop bumper", 65: "Iron Man #1 bottom",
	66: "Iron Man #2", 67: "Iron Man #3", 68: "Iron Man #4", 72: "Top lane Hulk", 73: "Top lane Iron Man", 74: "Top lane Thor",
	75: "Top lane Captain America", 76: "Top lane Black Widow", 77: "Top lane Hawkeye", 78: "Shield Agent", 80: "Right orbit red",
}

PRO_LAMPS = {
	# Addresses 4-7 were transcribed backwards against the manual's own LAMP MATRIX GRID row 01
	# (Avengers-Pro-Manual.pdf, PDF page 19), which reads LEFT OUTLANE / LEFT RETURN LANE /
	# RIGHT RETURN LANE / RIGHT OUTLANE. The coordinates in curate_avengers_pro_spatial.py were
	# always correct (4 far-left through 7 far-right) and are pairwise co-located with switches
	# 24/25/28/29, whose own left/right labels are undisputed - lamp 4 sits at x=0.041343 and
	# switch 24 "Left outlane" at x=0.041434. Only the four labels were wrong.
	1: "Start button", 2: "Tournament start", 3: "Shoot again", 4: "Left outlane", 5: "Left return lane", 6: "Right return lane",
	7: "Right outlane", 8: "Captain America", 9: "Thor", 10: "Hawkeye", 11: "Hulk", 12: "Black Widow", 13: "Iron Man",
	14: "(T)HOR", 15: "T(H)OR", 16: "TH(O)R", 17: "THO(R)", 18: "Hawkeye #1 bottom", 19: "Hawkeye #2",
	20: "Hawkeye #3", 21: "Hawkeye #4", 22: "Left orbit purple", 23: "Tesseract standup", 24: "Captain America #1 bottom",
	25: "Captain America #2", 26: "Captain America #3", 27: "Captain America #4", 28: "Left inner loop red", 29: "Special",
	30: "Hulk target arrow", 31: "Black Widow #1 bottom", 32: "Black Widow #2", 33: "Black Widow #3", 34: "Black Widow #4",
	35: "Left ramp red", 36: "Left ramp green", 37: "Right 2-bank target top", 38: "Right 2-bank target bottom", 39: "Hulk eject green",
	41: "(C)OSMIC", 42: "C(O)SMIC", 43: "CO(S)MIC", 44: "COS(M)IC", 45: "COSM(I)C", 46: "COSMI(C)",
	47: "(H)ULK", 48: "H(U)LK", 49: "HU(L)K", 50: "HUL(K)", 51: "Tesseract standup left", 52: "Tesseract standup right",
	53: "Right orbit red", 54: "Iron Man #4", 55: "Iron Man #3", 57: "Iron Man #1 bottom", 58: "Shield Agent",
	60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper", 63: "Top lane Hulk", 65: "Top lane Captain America",
	66: "Top lane Hawkeye", 67: "Top lane Thor", 68: "Top lane Black Widow", 69: "Extra ball", 70: "Top lane Iron Man",
	71: "Lock 1", 73: "Lock 2", 75: "Lock 3", 78: "Iron Man #2",
}

LAMP_POWER = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_GROUND_WIRE = ["RED-BRN", "RED-BLK", "RED-ORG", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY", "RED-WHT", "RED"]
LAMP_GROUND_CONNECTION = ["J12-P1", "J12-P2", "J12-P3", "J12-P4", "J12-P5", "J12-P6", "J12-P8", "J12-P9", "J12-P10", "J12-P11"]


def lamps(manual: str, script: str, limited_edition: bool) -> list[dict[str, object]]:
	labels = LE_LAMPS if limited_edition else PRO_LAMPS
	items = []
	for address in range(1, 81):
		label = labels.get(address, f"Unused lamp {address}")
		availability = "used" if address in labels else "unused"
		row, column = divmod(address - 1, 8)
		refs = (manual, script) if availability == "used" else (manual,)
		items.append(output(
			address, label, "lamp", availability, "pinmame.output.lamp", refs, str(address), output_id=f"lamp.{slug(label)}" if availability == "used" else f"lamp.unused-{address}",
			physical={"location": "Playfield or cabinet as shown on the manual lamp-location map"},
			wiring={"board": "I/O Power Driver board", "drive_wire": LAMP_POWER[column][0], "drive_connection": LAMP_POWER[column][1], "return_wire": LAMP_GROUND_WIRE[row], "return_connection": LAMP_GROUND_CONNECTION[row]},
		))
	items.append(output(0, "General illumination", "gi", "used", "pinmame.output.gi", (manual, script), "GI-0", output_id="gi.general-illumination", physical={"location": "Playfield and backbox illumination"}))
	return items


def sid(number: int, limited_edition: bool) -> str:
	return f"switch.{slug(switch_specs(limited_edition)[number][0])}"


def mech(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, manual: str, script: str, positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {
		"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		"behavior": behavior, "provenance": provenance(manual, script),
	}
	if positions:
		result["positions"] = positions
	return result


def common_mechanisms(limited_edition: bool) -> list[dict[str, object]]:
	manual = LE_MANUAL if limited_edition else PRO_MANUAL
	script = LE_SCRIPT if limited_edition else PRO_SCRIPT
	trough_switches = list(range(17, 24)) if limited_edition else list(range(18, 23))
	trough_count = 6 if limited_edition else 4
	shooter = "switch.shooter-lane"
	hulk_bank_output = "device.center-4-bank-drop-reset" if limited_edition else "device.center-4-bank-drop-reset"
	if limited_edition:
		hulk_bank_output = "device.center-4-bank-drop-reset"
	arm_output = "device.hulk-arms"
	magnet_output = "device.hulk-magnet"
	lock_output = "device.loki-lockup"
	items = [
		mech("mechanism.trough", f"{trough_count}-ball trough", "kicker", ["device.trough-up-kicker"], [sid(number, limited_edition) for number in trough_switches], f"The {trough_count}-ball physical trough uses position sensors {trough_switches[0]}-{trough_switches[-2]} and jam sensor {trough_switches[-1]}. The working script initializes {trough_count} balls and output 1 ejects from the right end.", manual, script),
		mech("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], [shooter], f"Output 2 fires a ball at {('dedicated D15/public 86' if limited_edition else 'matrix switch 23')}. The working script uses a 0.6-second impulse and {'power 62 with 0.3 randomness' if limited_edition else 'power 55 with 0.5 randomness'} as a proven baseline.", manual, script),
		mech("mechanism.hulk-eject", "Hulk eject", "kicker", ["device.hulk-eject"], [sid(62, limited_edition)], f"A ball rests on switch 62 until output 5 ejects it. The working script uses angle 25, force {'16' if limited_edition else '20'}, and route variance.", manual, script),
		mech("mechanism.hulk-drop-bank", "HULK four-drop bank", "drop_target_bank", [hulk_bank_output], [sid(number, limited_edition) for number in range(52, 56)], f"Switches 52-55 stay down independently. {'Public auxiliary output 51, physical driver 41' if limited_edition else 'main output 6'} resets all four targets.", manual, script),
		mech("mechanism.hulk-turntable", "Rotating Hulk assembly", "motorized", ["device.hulk-counterclockwise", "device.hulk-clockwise"], [sid(41, limited_edition), sid(42, limited_edition)], "Outputs 3 and 4 drive opposite Hulk rotation directions. Wheel optos 41 and 42 report indexed motion; stop each drive at the intended sensed position and never energize both directions together.", manual, script),
		mech("mechanism.hulk-arms", "Hulk arm lift", "motorized", [arm_output], [], f"{'Public auxiliary output 56, physical driver 46' if limited_edition else 'Main output 17 through the step-up driver board'} raises the Hulk arms while active and lowers them when released. The table animation moves from roughly 130 to 200 degrees in two-degree timer steps.", manual, script),
		mech("mechanism.hulk-magnet", "Hulk platter magnet", "other", [magnet_output], [sid(57, limited_edition)], f"Switch 57 reports a ball on the Hulk platter. {'Public auxiliary output 54, physical driver 44' if limited_edition else 'Main output 23 through the step-up driver board'} energizes the magnet; the working table uses radius 16 and {'does not force the ball to center' if limited_edition else 'centers the captured ball'}.", manual, script),
		mech("mechanism.loki-lock", "Three-ball Loki lock", "gate", [lock_output], [sid(number, limited_edition) for number in range(49, 52)], f"Three active-low optos are initialized high when empty and fall low as balls occupy positions bottom-to-top. {'Output 12' if limited_edition else 'Output 22 through the step-up driver board'} drops the retaining post/releases locked balls.", manual, script, [
			{"id": "position.lock-1", "label": "Bottom lock", "sensors": [sid(49, limited_edition)]},
			{"id": "position.lock-2", "label": "Middle lock", "sensors": [sid(50, limited_edition)]},
			{"id": "position.lock-3", "label": "Top lock", "sensors": [sid(51, limited_edition)]},
		]),
		mech("mechanism.tesseract-spinner", "Inertial Tesseract spinner", "rotary", [], [sid(45, limited_edition), sid(46, limited_edition)], "The playfield ball physically spins the Tesseract; it has no controller motor. Opposed optos 45 and 46 pulse as the inertial wheel crosses their positions. Preserve free rotation, collision-derived angular velocity, and gradual drag.", manual, script),
		mech("mechanism.standard-pops", "Three pop bumpers", "other", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], [sid(30, limited_edition), sid(31, limited_edition), sid(32, limited_edition)], "Left, right, and bottom pop switches 30-32 directly correspond to outputs 9-11; the shared pop flasher is output 25.", manual, script),
		mech("mechanism.standard-slings", "Left and right slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], [sid(26, limited_edition), sid(27, limited_edition)], "Slingshot switches 26/27 drive outputs 13/14 and share flasher output 20.", manual, script),
		mech("mechanism.flippers", "Lower flipper pair", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "The two lower flippers use outputs 15/16, dedicated cabinet buttons D9/D11, and normally-closed EOS contacts D10/D12. Preserve SAM fast-flip behavior.", manual, script),
	]
	if limited_edition:
		items.extend([
			mech("mechanism.thor-drop-bank", "THOR four-drop bank", "drop_target_bank", ["device.left-4-bank-drop-reset"], [sid(number, True) for number in range(1, 5)], "Switches 1-4 stay down independently and main output 6 resets the left THOR bank.", manual, script),
			mech("mechanism.bridge", "Motorized bridge", "diverter", ["device.bridge-motor", "device.bridge-motor-relay"], [sid(8, True), sid(9, True)], "The bridge has down switch 8 and up switch 9. Output 22 supplies the motor and relay output 23 selects motion state; the working script treats 23 active as down (8 active, 9 clear) and inactive as up (8 clear, 9 active). Implement limit-switch cutoff in both directions.", manual, script, [
				{"id": "position.bridge-down", "label": "Bridge down", "sensors": [sid(8, True)]},
				{"id": "position.bridge-up", "label": "Bridge up", "sensors": [sid(9, True)]},
			]),
			mech("mechanism.control-gates", "Orbit and ramp control gates", "gate", ["device.left-orbit-control-gate", "device.right-orbit-control-gate", "device.right-ramp-control-gate", "device.left-ramp-control-gate"], [], "Main output 7 opens the left orbit. Auxiliary public 57/physical 47 opens the right orbit. Auxiliary public 52/53, physical 42/43, actuate the right/left ramp gates. Each returns closed when its drive releases.", manual, script),
			mech("mechanism.rgb-gi-relays", "RGB GI LED relay bank", "other", ["gi.general-illumination", "device.blue-gi-led-relay", "device.green-gi-led-relay", "device.red-gi-led-relay"], [], "GI public address 0 is the common illumination channel. Main output 17 and auxiliary public outputs 55/58 switch the blue, green, and red 112-5033 LED supply rails shown on the LE GI location map. Keep the three relay channels distinct even if a table renderer also exposes a combined GI brightness.", manual, script),
		])
	else:
		items.extend([
			mech("mechanism.thor-target-bank", "THOR four-target bank", "other", [], [sid(number, False) for number in range(1, 5)], "The Pro uses four independently sensed THOR targets at switches 1-4. Unlike LE, the Pro manual and working script provide no THOR reset actuator; do not copy the LE drop-bank output into this machine.", manual, script),
			mech("mechanism.control-gates", "Left orbit and ramp control gates", "gate", ["device.left-orbit-control-gate", "device.left-ramp-control-gate"], [], "Output 7 opens the left orbit gate and output 12 raises the left ramp control gate. Both return closed when their drive releases. The Pro has no LE eight-transistor gate outputs.", manual, script),
		])
	return items


def driver_records(limited_edition: bool) -> list[dict[str, object]]:
	selected_ids = LE_DRIVER_IDS if limited_edition else PRO_DRIVER_IDS
	result = []
	for driver_id in sorted(selected_ids):
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Colored-ROM modification only; physical I/O and mechanisms are unchanged." if driver_id.endswith("c") else "Firmware revision within this physical edition; playfield I/O and mechanisms are unchanged."
		result.append(record)
	return result


def sources(limited_edition: bool) -> list[dict[str, object]]:
	manual = LE_MANUAL if limited_edition else PRO_MANUAL
	script = LE_SCRIPT if limited_edition else PRO_SCRIPT
	runtime = LE_RUNTIME if limited_edition else PRO_RUNTIME
	manual_record = {
		"id": manual, "kind": "manual",
		"uri": "https://wp.sternpinball.com/wp-content/uploads/2018/10/Avengers-LE-Manual-compressed.pdf" if limited_edition else "https://sternpinball.com/wp-content/uploads/2018/10/Avengers-Pro-Manual.pdf",
		"sha256": "4687ae0ed0ac249411deff3b0284d5c13d8fab154e430e95b6bd9f7bb82dca62" if limited_edition else "fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031",
		"locator": "Avengers-LE-Manual-compressed.pdf: PDF pages 63-69, 105-108, and 117 plus assembly drawings" if limited_edition else "Avengers-Pro-Manual.pdf: PDF pages 13-20 plus model-specific assembly drawings",
		"license": "NOASSERTION", "attribution": "Stern Pinball", "source_id": "stern",
		"original_filename": "Avengers-LE-Manual-compressed.pdf" if limited_edition else "Avengers-Pro-Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z",
	}
	script_record = {
		"id": script, "kind": "vpx_script",
		"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPX_REVISION}/{'JPs%20Avengers%20Classic%20LE%20(Stern%20-%202012)%20v600.vbs' if limited_edition else 'Avengers%20(Stern%202012)4k1.3.1.vbs'}",
		"revision": VPX_REVISION,
		"sha256": "c6da231a360a0f062fa5b434d08faca3c1b7b6a5436cc51b5b54dac924e1a3b4" if limited_edition else "85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8",
		"locator": "JPs Avengers Classic LE (Stern - 2012) v600.vbs lines 81-151, 250-315, 343-461, and 745-845" if limited_edition else "Avengers (Stern 2012)4k1.3.1.vbs lines 130-388, 609-658, 927-1060, and 1112-1145",
		"license": "NOASSERTION", "attribution": "Table authors credited in the script and vpxtable_scripts contributors",
	}
	runtime_record = {
		"id": runtime, "kind": "runtime_scenario", "uri": f"local-evidence://pinmame-harness/{'avs_170h/boot-start-2.json' if limited_edition else 'avs_170/boot-start-1.json'}",
		"sha256": "3fdb8e048c0c8ff130163333e508953b6ec3bfb0670931af9cbddc957c011bd3" if limited_edition else "4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6",
		"locator": f"Isolated LibPinMAME boot/start scenario using exact {'avs_170h.zip a5ea0eafcc45671ce66b29336c81f875f49515235034520f53e3042dfdefc74d' if limited_edition else 'avs_170.zip 5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3'}; captures 128x32x4 DMD, GI 0, lamp activity, and public solenoid transitions",
		"license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external",
	}
	return [
		manual_record, script_record, runtime_record,
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Avengers INITGAME, SAM two-color DMD, and eight-custom-solenoid transport configuration", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames Avengers driver family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	]


def build(limited_edition: bool) -> dict[str, object]:
	manual = LE_MANUAL if limited_edition else PRO_MANUAL
	script = LE_SCRIPT if limited_edition else PRO_SCRIPT
	runtime = LE_RUNTIME if limited_edition else PRO_RUNTIME
	name = "The Avengers Limited Edition" if limited_edition else "The Avengers Pro"
	machine_id = "stern.avengers-limited-edition.2012" if limited_edition else "stern.avengers-pro.2012"
	knowledge_path = "knowledge/stern/avengers-limited-edition-2012.md" if limited_edition else "knowledge/stern/avengers-pro-2012.md"
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": machine_id, "name": name, "manufacturer": "Stern", "year": 2012, "ipdb_id": 5940},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(limited_edition), "inputs": inputs(manual, script, limited_edition),
		"outputs": coils(manual, script, limited_edition) + lamps(manual, script, limited_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE_SOURCE, manual)}, "provenance": provenance(CORE_SOURCE, runtime)}],
		"mechanisms": common_mechanisms(limited_edition), "relationships": [], "sources": sources(limited_edition),
		"knowledge": {"path": knowledge_path, "status": "complete"}, "conflicts": conflicts(limited_edition, manual, script),
	}
	return apply_spatial(definition) if limited_edition else definition


LE_KNOWLEDGE = """# The Avengers Limited Edition (Stern, 2012)

Coverage: **author-ready - complete Limited Edition I/O, wiring, mechanisms, lighting, initial state, and controller bindings validated; spatial evidence is partial**

## Identity and evidence precedence

This definition covers `avs_120h`, `avs_140h`, `avs_170h`, and `avs_170hc`. The `h` family is the physical Limited Edition; the colored `hc` ROM does not change hardware. The known-working JP Salas LE script is ground truth for PinMAME addresses, callbacks, initial state, ball routing, and mechanism causality. The official Stern LE manual governs physical inventory, service numbers, coil specifications, wiring, assembly construction, and location maps. The isolated exact-ROM run validates the native 128x32 four-bit DMD, public GI 0, conventional lamp callback range, and runtime availability without redistributing ROM content.

## Six-ball trough and launcher

The LE has six balls on trough switches 17-22 and jam switch 23. Initialize all six position switches active and jam clear; output 1 ejects from the right end and the table pulses jam during transfer. The shooter lane is dedicated D15/public switch 86, not matrix 23. Output 2 auto-launches with a proven 0.6-second impulse, power 62, and 0.3 randomness.

## Two drop banks

The left THOR bank uses maintained drop switches 1-4 and main output 6 resets it. The center HULK bank uses switches 52-55 and the LE auxiliary board: PinMAME public output 51 is physical driver 41. Do not reuse the Pro mapping, where main output 6 resets only the center HULK bank and THOR is passive.

## Hulk assembly

Outputs 3/4 rotate Hulk counterclockwise/clockwise and optos 41/42 report wheel position. Public auxiliary 56, physical driver 46, lifts the arms; the proven animation spans roughly 130-200 degrees. Switch 57 detects a ball on the platter and public auxiliary 54/physical 44 energizes the radius-16 magnet without forcing the ball to center. Switch 62 holds a ball at the Hulk eject until main output 5 kicks it at the proven angle 25 and force 16. Switch 63 is the separate Hulk standup target.

## Loki lock

The three lock optos 49-51 are active-low: initialize them high when empty and drive them low as balls occupy bottom, middle, and top positions. Main output 12 drops the retaining post and releases the visible three-ball lock. Preserve the lock as physical ball storage; it is not a simulated bookkeeping-only lock.

## Bridge, gates, and Tesseract

The bridge uses motor output 22, direction/state relay 23, down switch 8, and up switch 9. The proven table treats relay 23 active as down and inactive as up; add limit cutoff at both sensors. Main output 7 opens the left orbit, public auxiliary 57/physical 47 opens the right orbit, and public auxiliary 52/53 (physical 42/43) actuate the right/left ramp gates. The Tesseract is an inertial playfield spinner, not a ROM-driven motor: the ball imparts angular velocity, optos 45/46 pulse at opposed positions, and drag gradually stops it.

## Lighting and standard devices

The conventional 1-80 lamp matrix is fully enumerated, including unused 13, 69-71, and 79. GI is public address 0. The LE additionally uses three physical color relays: main 17 is blue, auxiliary 55/physical 45 is green, and auxiliary 58/physical 48 is red. These switch the 112-5033 RGB GI LED rails shown on the manual location map and must remain distinct even if a renderer also offers combined brightness. Three pops are switches 30-32/outputs 9-11, slings are 26/27 and 13/14, and lower flippers are outputs 15/16 with dedicated buttons and normally-closed EOS contacts.

## Spatial evidence pass

Coordinates use normalized playfield space: x=0 is left and x=1 is right; y=0 is rear/backglass and y=1 is the apron. The promoted subset is observed against the official LE switch, lamp, coil, and RGB-GI maps on manual pages 63, 64, 66, 68, and 117. Assembly anchors are explicitly labeled when the manual groups paired optos or a multi-device mechanism. No coordinate in this LE definition is sourced from a Pro VPX table.

The organized local VPX candidate `Avengers (Stern 2012)-WIP HD neo Hulk rascalV2.vpx` is retained as a review artifact but rejected for LE spatial use: its script identifies ROM `avs_170`, which is Pro-family evidence. The LE evidence itself has an unresolved upper-right-orbit address: the manual's physical location drawing marks the disputed coordinate 61, its switch matrix grid says 58, and the known-working LE script drives `sw58` without a `sw61` handler. Neither input receives that coordinate, and 61 is not classified as unused. The same fail-closed rule applies to LE bridge, auxiliary-board, lock-lamp, Tesseract-lamp, and any relocated geometry.

Controlled N/A assertions cover DIP switches, unused devices, cabinet/service controls, rear-panel flashers, internal GI/bridge relays, the optional shaker and coin meter, and the virtual game-on output. Remaining physical devices intentionally have no spatial assertion until their individual LE geometry is reconciled: bridge endpoints 8/9, trough contacts 17-23, shooter switch 86, unlocated coils/auxiliary effects, the used lamp matrix, RGB-GI per-emitter locations and multiplicity, and the DMD display field (schema v2 has no display spatial-placement member). This keeps the machine schema-v2 partial and identifies the exact authoring blockers instead of inventing placements.

## Recreation checklist

- Build the six-ball trough, dedicated-switch shooter lane, two resettable four-target banks, three-ball active-low Loki lock, motorized sensed bridge, full Hulk motor/arms/magnet/eject assembly, four controlled gates, and passive inertial Tesseract.
- Bind the auxiliary board by public PinMAME addresses 51-58 while retaining physical diagnostic numbers 41-48 for service UI and wiring.
- Preserve sustained/PWM behavior for motors, magnet, relay, and flipper drives; do not turn every output into a fixed pulse.
- Implement every explicit unused switch and lamp address so omissions are distinguishable from unknown data.
- Use the script force, angle, timing, and rotation values as proven authoring baselines, then align geometry to the manual assembly drawings without changing controller causality.

## Sources

- `manual.avengers-limited-edition`: official Stern `Avengers-LE-Manual-compressed.pdf`, SHA-256 `4687ae0ed0ac249411deff3b0284d5c13d8fab154e430e95b6bd9f7bb82dca62`; I/O charts on PDF pages 63-69, auxiliary board on 108, RGB GI map on 117, and assembly drawings throughout.
- `vpx.avengers-le.jp-salas-v600`: known-working JP Salas LE script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `c6da231a360a0f062fa5b434d08faca3c1b7b6a5436cc51b5b54dac924e1a3b4`.
- `runtime.avengers-le.boot-start`: isolated exact `avs_170h.zip` run, raw SHA-256 `3fdb8e048c0c8ff130163333e508953b6ec3bfb0670931af9cbddc957c011bd3`; ROM archive SHA-256 `a5ea0eafcc45671ce66b29336c81f875f49515235034520f53e3042dfdefc74d` remains external.
"""

PRO_KNOWLEDGE = """# The Avengers Pro (Stern, 2012)

Coverage: **author-ready - complete Pro I/O, wiring, mechanisms, initial state, and controller bindings validated**

## Identity and evidence precedence

This definition covers `avs_110`, `avs_140`, `avs_170`, and `avs_170c`; the colored ROM changes display presentation only. The known-working VPW-derived Pro table uses `avs_170c` and its callbacks match the model-specific Pro manual: it is ground truth for PinMAME addresses, initial state, ball routing, and mechanism causality. The Pro manual governs physical inventory, service numbering, wiring, assemblies, and edition differences. The exact-ROM harness separately confirms the 128x32 four-bit DMD, GI 0, and conventional lamp activity.

## Four-ball trough and launcher

The Pro has four balls at switches 18-21 plus jam switch 22. The working table initializes 21, 20, 19, and 18 and output 1 ejects from the right end. Unlike LE, the shooter lane is matrix switch 23; dedicated D15/public 86 is unused. Output 2 drives the auto launcher with a proven 0.6-second impulse, power 55, and 0.5 randomness.

## Pro-specific output topology

The Pro has no LE eight-transistor auxiliary board. Its center HULK reset is main output 6, left ramp gate is 12, Hulk arms are 17 through a step-up board, Loki lock is 22 through a step-up board, and Hulk magnet is 23 through a step-up board. The pinned PinMAME root configures eight custom callback slots for the whole Avengers clone family, so a Pro ROM can emit public 51-58 transitions even though those drivers are physically absent. The model-specific manual and working Pro script resolve that emulator-family artifact: do not instantiate 51-58 on the Pro playfield.

## Targets and routes

The Pro THOR switches 1-4 are passive targets with no reset output; do not copy the LE THOR drop bank. The center HULK drop bank uses switches 52-55 and resets through main output 6. Left orbit is switch 47, right ramp exit is 48, and the Pro right orbit is switch 61 rather than LE switch 58. Output 7 opens the left orbit gate and output 12 raises the left ramp gate.

## Hulk, Loki, and Tesseract

Outputs 3/4 rotate Hulk in opposite directions with wheel optos 41/42. Output 17 lifts the arms. Switch 57 detects the Hulk plate and output 23 energizes its radius-16 centering magnet. Switch 62 holds the eject ball until output 5 kicks it at the proven angle 25 and force 20. The active-low Loki optos 49-51 initialize high when empty and output 22 drops the retaining post. The Tesseract is passive and inertial: ball impact drives rotation, optos 45/46 report it, and there is no motor output.

## Lamps and standard devices

All 80 matrix addresses are present, with unused 40, 56, 59, 64, 72, 74, 76, 77, 79, and 80 explicit. This matrix is substantially different from LE and must not be shared by number. GI is address 0. Three pops use switches 30-32/outputs 9-11, slings use 26/27 and 13/14, and the lower flippers use outputs 15/16 with dedicated buttons and normally-closed EOS contacts.

## Recreation checklist

- Build the four-ball trough, matrix shooter lane, passive THOR target bank, resettable center HULK bank, active-low three-ball Loki lock, Hulk rotation/arms/magnet/eject assembly, left orbit and ramp gates, and free-spinning Tesseract.
- Do not add the LE bridge, second resettable bank, right-orbit/ramp auxiliary gates, RGB GI relay bank, six-ball trough, or physical outputs 41-48.
- Treat exact Pro manual addresses as authoritative over clone-root callback capacity; observed public 53/54 activity during boot is not proof of physical Pro coils.
- Preserve sustained/PWM semantics for motors, magnet, lock, gates, and flippers, and use the proven script motion/force values as authoring baselines.

## Sources

- `manual.avengers-pro`: official Stern `Avengers-Pro-Manual.pdf`, SHA-256 `fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031`; switch chart PDF page 13, coil chart page 16, lamp chart page 19, location maps, and model-specific assembly drawings.
- `vpx.avengers-pro.vpw-1-3-1`: known-working Pro script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8`.
- `runtime.avengers-pro.boot-start`: isolated exact `avs_170.zip` run, raw SHA-256 `4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6`; ROM archive SHA-256 `5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3` remains external.
"""


LE_LAMPS_SEEN = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 80]
PRO_LAMPS_SEEN = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 73, 75, 78]


def runtime_evidence(limited_edition: bool) -> dict[str, object]:
	machine_id = "stern.avengers-limited-edition.2012" if limited_edition else "stern.avengers-pro.2012"
	driver_id = "avs_170h" if limited_edition else "avs_170"
	raw_sha = "3fdb8e048c0c8ff130163333e508953b6ec3bfb0670931af9cbddc957c011bd3" if limited_edition else "4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6"
	rom_sha = "a5ea0eafcc45671ce66b29336c81f875f49515235034520f53e3042dfdefc74d" if limited_edition else "5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3"
	initial = "17 --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 22" if limited_edition else "18 --initial-switch 19 --initial-switch 20 --initial-switch 21"
	return {
		"format": "pinmame-machine-evidence", "version": 1, "extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/{driver_id}/harness", "sha256": raw_sha, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
		"driver_ids": [driver_id], "machine_ids": [machine_id], "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": driver_id, "rom_archive_sha256": rom_sha,
			"raw_runs": [{"name": "boot-start", "sha256": raw_sha, "self_test_pulses": 0}],
			"command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver_id} --rom-path <roms> --work-dir <isolated-state> --initial-switch {initial} --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>",
			"observations": {"lamp_addresses_seen": LE_LAMPS_SEEN if limited_edition else PRO_LAMPS_SEEN, "gi_addresses_seen": [0], "solenoid_addresses_seen": [22, 23, 24] if limited_edition else [24, 53, 54], "display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}]},
		},
	}


def write_json(path: Path, value: dict[str, object]) -> None:
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json_file(path, value)


def _remove_legacy_stubs() -> None:
	for relative_path in LE_LEGACY_STUB_PATHS:
		path = ROOT / relative_path
		if path.exists():
			path.unlink()


def main() -> None:
	"""Generate the canonical, fail-closed Avengers LE base bundle.

	The Pro definition is intentionally not generated here.  A separately
	reviewed Pro promotion may own either its partial or author-ready definition
	and its knowledge, and the base LE generator must be safe to run before or
	after that work.  Likewise, a promoted LE definition is authoritative over
	the base partial and spatial knowledge, so it is never replaced here.
	"""
	if (ROOT / LE_AUTHOR_READY_PATH).exists():
		_remove_legacy_stubs()
		return

	# Build every LE artifact before the first write so generation order cannot
	# leave a newly written artifact based on a later build failure.
	le_definition = build(True)
	le_evidence = runtime_evidence(True)
	le_audit = spatial_audit(le_definition)
	le_knowledge = fail_closed_spatial_knowledge(LE_MACHINE_ID, LE_KNOWLEDGE)

	_remove_legacy_stubs()
	write_json(ROOT / LE_PARTIAL_PATH, le_definition)
	write_json(ROOT / LE_EVIDENCE_PATH, le_evidence)
	write_json_file(ROOT / LE_SPATIAL_AUDIT_PATH, le_audit)
	write_text(ROOT / LE_KNOWLEDGE_PATH, le_knowledge)


if __name__ == "__main__":
	main()
