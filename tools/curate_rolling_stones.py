"""Build reviewed, author-ready Rolling Stones Standard and Limited Edition definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("rsn_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.rolling-stones-standard-le.2011"
VPX_SOURCE = "vpx.rolling-stones-le-1.0.6i"
STERN_SOURCE = "stern.rolling-stones-product-page"
IPDB_STANDARD_SOURCE = "ipdb.rolling-stones-standard.5668"
IPDB_LE_SOURCE = "ipdb.rolling-stones-limited-edition.5708"
STANDARD_RUNTIME_SOURCE = "runtime.rolling-stones-standard.boot-start"
LE_RUNTIME_SOURCE = "runtime.rolling-stones-limited-edition.boot-start"


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


# label, physical switch type, momentary pulse, semantic roles
COMMON_SWITCHES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	1: ("Mick three-bank bottom target", "microswitch", True, ()),
	2: ("Mick three-bank middle target", "microswitch", True, ()),
	3: ("Mick three-bank top target", "microswitch", True, ()),
	6: ("Top lane Ronnie", "leaf", False, ()), 7: ("Top lane Mick", "leaf", False, ()),
	8: ("Top lane Keith", "leaf", False, ()), 9: ("Top lane Charlie", "leaf", False, ()),
	10: ("Right three-bank bottom target", "microswitch", True, ()),
	11: ("Right three-bank middle target", "microswitch", True, ()),
	12: ("Right three-bank top target", "microswitch", True, ()),
	15: ("Tournament start", "button", False, ("cabinet.tournament-start",)),
	16: ("Start", "button", False, ("cabinet.start",)),
	18: ("Trough 4", "microswitch", False, ("ball.position",)),
	19: ("Trough 3", "microswitch", False, ("ball.position",)),
	20: ("Trough 2", "microswitch", False, ("ball.position",)),
	21: ("Trough 1", "microswitch", False, ("ball.position",)),
	22: ("Trough jam", "opto", False, ("ball.position",)),
	23: ("Shooter lane", "microswitch", False, ("ball.position",)),
	24: ("Left outlane", "leaf", True, ()), 25: ("Left return lane", "leaf", True, ()),
	26: ("Left slingshot", "leaf", True, ()), 27: ("Right slingshot", "leaf", True, ()),
	28: ("Right return lane", "leaf", True, ()), 29: ("Right outlane", "leaf", True, ()),
	30: ("Left pop bumper", "leaf", True, ()), 31: ("Right pop bumper", "leaf", True, ()),
	32: ("Bottom pop bumper", "leaf", True, ()),
	33: ("Mick position 1 home", "microswitch", False, ("position.home",)),
	34: ("Mick position 2", "microswitch", False, ("position.index",)),
	35: ("Mick position 3", "microswitch", False, ("position.index",)),
	36: ("Mick position 4", "microswitch", False, ("position.index",)),
	37: ("Mick position 6", "microswitch", False, ("position.index",)),
	38: ("Mick position 7 away", "microswitch", False, ("position.away",)),
	39: ("Mick position 5 park", "microswitch", False, ("position.park",)),
	41: ("Left orbit spinner", "other", True, ()), 42: ("Left ramp exit", "microswitch", True, ()),
	43: ("Left pop bumper lane", "leaf", True, ()), 44: ("Left orbit", "leaf", True, ()),
	45: ("Right ramp exit", "microswitch", True, ()),
	46: ("Left lock 2 top", "microswitch", False, ("ball.position",)),
	48: ("Right orbit", "leaf", True, ()),
	51: ("Star target left", "microswitch", True, ()),
	53: ("Center lock bottom", "microswitch", False, ("ball.position",)),
	54: ("Rock Star target left", "microswitch", True, ()),
	55: ("Rock Star target right", "microswitch", True, ()),
	56: ("Star target right", "microswitch", True, ()),
	57: ("Star target center", "microswitch", True, ()),
}
LE_SWITCHES = {
	17: ("Trough 5 left", "microswitch", False, ("ball.position",)),
	50: ("Shooter lane top", "leaf", False, ("ball.position",)),
}


def matrix_switch(number: int, limited_edition: bool) -> dict[str, object]:
	specs = COMMON_SWITCHES | (LE_SWITCHES if limited_edition else {})
	spec = specs.get(number)
	used = spec is not None
	label = spec[0] if used else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	sources = (MANUAL_SOURCE, VPX_SOURCE) if used or number == 14 else (MANUAL_SOURCE,)
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
	if number == 14:
		result["physical"]["notes"] = "The official service chart leaves physical matrix switch 14 unpopulated. The proven VPX script mirrors StartGameKey into 14 as a table compatibility shortcut before the standard VPinMAME key handler drives physical Start switch 16; authors must not build a second start switch."
	return result


SAM_DEDICATED_ROLES = {
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth",
	84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos",
	88: "playfield.post.left.button", 86: "playfield.post.right.button", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, sources: tuple[str, ...], kind: str = "switch", pulse: bool = False, notes: str | None = None) -> dict[str, object]:
	physical: dict[str, object] = {} if kind == "virtual" else {"switch_type": switch_type}
	if notes:
		physical["notes"] = notes
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": kind,
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"), "normally_closed": normally_closed,
		"pulse": pulse, "availability": availability, "physical": physical,
		"provenance": provenance("validated", *sources),
	}
	if availability in {"used", "optional"} and device in SAM_DEDICATED_ROLES:
		result["roles"] = [SAM_DEDICATED_ROLES[device]]
	return result


def inputs(limited_edition: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, limited_edition) for number in range(1, 65)]
	manual_core = (MANUAL_SOURCE, CORE_SOURCE)
	working = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)
	dedicated: list[tuple[int, int, str, str, str, bool, tuple[str, ...], str, bool, str | None]] = [
		(65, 1, "Left coin chute", "used", "button", False, manual_core, "switch", True, None),
		(66, 2, "Center coin chute", "used", "button", False, manual_core, "switch", True, None),
		(67, 3, "Right coin chute", "used", "button", False, manual_core, "switch", True, None),
		(68, 4, "Fourth coin chute", "optional", "button", False, manual_core, "switch", True, None),
		(69, 5, "Fifth coin chute", "optional", "button", False, manual_core, "switch", True, None),
		(70, 6, "Unused dedicated switch D6", "unused", "unknown", False, manual_core, "switch", False, None),
		(71, 7, "Magnetic ball detector" if limited_edition else "Unused dedicated switch D7", "used" if limited_edition else "unused", "other" if limited_edition else "unknown", limited_edition, working if limited_edition else manual_core, "switch", False, "Limited Edition active-low ceramic-ball detector. The proven script initializes public 71 active, drives it inactive while the ceramic ball occupies trough switch 21, and restores it after the ball leaves shooter switch 23." if limited_edition else None),
		(72, 8, "Moving Mick target hit", "used", "microswitch", False, working, "switch", True, "One physical target-hit switch shared by every sensed Mick position; do not confuse it with position sensors 33-39."),
		(84, 9, "Left flipper button", "used", "button", False, working, "switch", False, None),
		(83, 10, "Left flipper end-of-stroke", "used", "leaf", True, working, "switch", False, None),
		(82, 11, "Right flipper button", "used", "button", False, working, "switch", False, None),
		(81, 12, "Right flipper end-of-stroke", "used", "leaf", True, working, "switch", False, None),
		(88, 13, "Left up/down post cabinet button" if limited_edition else "Unused dedicated switch D13", "used" if limited_edition else "unused", "button" if limited_edition else "unknown", False, working if limited_edition else manual_core, "switch", False, None),
		(87, 14, "VPX left-flipper compatibility state" if limited_edition else "Unused dedicated switch D14", "used" if limited_edition else "unused", "unknown", False, working if limited_edition else manual_core, "virtual" if limited_edition else "switch", False, "The service chart leaves physical D14 unpopulated. The proven VPX script mirrors the left flipper key here for ROM feature compatibility; authors must not build a separate physical switch." if limited_edition else None),
		(86, 15, "Right up/down post cabinet button" if limited_edition else "Unused dedicated switch D15", "used" if limited_edition else "unused", "button" if limited_edition else "unknown", False, working if limited_edition else manual_core, "switch", False, None),
		(85, 16, "VPX right-flipper compatibility state" if limited_edition else "Unused dedicated switch D16", "used" if limited_edition else "unused", "unknown", False, working if limited_edition else manual_core, "virtual" if limited_edition else "switch", False, "The service chart leaves physical D16 unpopulated. The proven VPX script mirrors the right flipper key here for ROM feature compatibility; authors must not build a separate physical switch." if limited_edition else None),
		(-7, 17, "Pendulum tilt", "used", "tilt", False, manual_core, "switch", False, None),
		(-6, 18, "Slam tilt", "optional", "tilt", True, manual_core, "switch", False, None),
		(-5, 19, "Ticket notch", "optional", "microswitch", False, manual_core, "switch", False, None),
		(-4, 20, "Unused dedicated switch D20", "unused", "unknown", False, manual_core, "switch", False, None),
		(-3, 21, "Coin-door Back button", "used", "button", False, manual_core, "switch", False, None),
		(-2, 22, "Coin-door Minus button", "used", "button", False, manual_core, "switch", False, None),
		(-1, 23, "Coin-door Plus button", "used", "button", False, manual_core, "switch", False, None),
		(0, 24, "Coin-door Select button", "used", "button", False, manual_core, "switch", False, None),
	]
	for spec in dedicated:
		items.append(dedicated_switch(*spec))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated", MANUAL_SOURCE, CORE_SOURCE)})
	return items


COILS: dict[int, tuple[str, str, str]] = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"),
	3: ("Center lockup up", "coil", "used"), 4: ("Center lockup latch", "coil", "used"),
	5: ("Left magnet", "magnet", "edition"), 6: ("Left control gate", "coil", "used"),
	7: ("Right magnet", "magnet", "edition"), 8: ("Shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"),
	11: ("Bottom pop bumper", "coil", "used"), 12: ("Unused output 12", "coil", "unused"),
	13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"),
	17: ("Left up/down post", "coil", "edition"), 18: ("Mick motor relay left", "relay", "used"),
	19: ("Mick motor relay right", "relay", "used"), 20: ("Backpanel right flasher", "flasher", "used"),
	21: ("Backpanel left flasher", "flasher", "used"), 22: ("Left ramp flasher", "flasher", "used"),
	23: ("Lips flasher", "flasher", "used"), 24: ("Coin meter", "coil", "optional"),
	25: ("Ronnie flasher", "flasher", "used"), 26: ("Pop bumper flasher", "flasher", "used"),
	27: ("Charlie flasher", "flasher", "used"), 28: ("Keith flasher", "flasher", "used"),
	29: ("Bottom arch flashers x2", "flasher", "edition"), 30: ("Center up/down post", "coil", "edition"),
	31: ("Rock Star flasher", "flasher", "used"), 32: ("Right up/down post", "coil", "edition"),
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J8-P11", "J8-P12", "J8-P14", "J8-P15", "J8-P16", "J8-P17", "J8-P18", "J8-P19", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance("validated", *sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def coil_wiring(address: int) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address == 12:
		return wiring
	if address == 8:
		power_wire, connection, voltage, voltage_type = "RED-WHT", "J17-P7", 16, "ac"
	elif address in {15, 16}:
		power_wire, connection, voltage, voltage_type = ("GRY-YEL / RED-YEL", "J10-P6/7", 50, "dc") if address == 15 else ("BLU-YEL / RED-YEL", "J10-P6/7", 50, "dc")
	elif address <= 16:
		power_wire, connection, voltage, voltage_type = ("VIO-YEL", "J10-P8", 50, "dc") if address in {5, 7} else ("YEL-VIO", "J10-P9/10", 50, "dc")
	elif address in {17, 18, 19, 30, 32}:
		power_wire, connection, voltage, voltage_type = "BRN", "J7-P1", 20, "dc"
	elif address == 24:
		power_wire, connection, voltage, voltage_type = "RED", "J16-P4-8", 5, "dc"
	else:
		power_wire, connection, voltage, voltage_type = "ORG", "J6-P10", 20, "dc"
	wiring.update({"power_wire": power_wire, "power_connection": connection, "nominal_voltage_v": voltage, "voltage_type": voltage_type})
	return wiring


def main_outputs(limited_edition: bool) -> list[dict[str, object]]:
	items = []
	for address, (label, kind, status) in COILS.items():
		availability = "used" if status == "edition" and limited_edition else "unused" if status == "edition" else status
		physical = None
		if status == "edition" and not limited_edition:
			physical = {"notes": "The official chart reserves this channel for the Premium hardware, corresponding to PinMAME's Limited Edition driver family; it is not installed on the Standard machine."}
		elif address == 12:
			physical = {"notes": "The service chart leaves Q12 unpopulated; preserve the public address as explicitly unused."}
		elif address == 24:
			physical = {"notes": "Optional coin meter circuit; the service chart specifies RED/J16-P4-8 at 5 VDC."}
		sources = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE) if availability in {"used", "optional"} else (MANUAL_SOURCE, CORE_SOURCE)
		items.append(output(address, label if availability != "unused" or status == "unused" else f"Unused Standard output {address} ({label})", kind, availability, sources, manual_address=str(address), physical=physical, wiring=coil_wiring(address), output_id=f"device.{slug(label)}"))
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else STANDARD_RUNTIME_SOURCE
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, runtime_source), physical={"notes": "PinMAME's synthetic SAM fast-flip game-on output; it has no physical Q33 coil."}, output_id="virtual.game-on"))
	return items


LAMPS = {
	1: "Start button", 2: "Tournament start button", 3: "Shoot Again", 4: "Left outlane", 5: "Left return lane", 6: "Right return lane", 7: "Right outlane",
	8: "VIP 1", 9: "VIP 2", 10: "VIP 3", 11: "Guitar 3 top", 12: "Guitar 2 middle", 13: "Guitar 1 bottom", 14: "Left orbit X", 15: "Left loop record", 16: "Left loop arrow",
	17: "Pop lane X", 18: "Pop lane record", 19: "Pop lane arrow", 20: "Star 1 left", 21: "Left ramp X", 22: "Left ramp record", 23: "Left ramp arrow", 24: "Play Records",
	25: "Center lane X", 26: "Center lane record", 27: "Center lane arrow", 28: "Right ramp X", 29: "Right ramp record", 30: "Right ramp arrow", 31: "World Tour", 32: "Fast Scoring",
	33: "Rock Star", 34: "Records", 35: "Licks", 36: "Combos", 37: "Star 2 center", 38: "Star 3 right", 39: "Extra Ball", 40: "Special",
	41: "Right orbit X", 42: "Right orbit record", 43: "Right loop arrow", 44: "Top lane Ronnie", 45: "Top lane Mick", 46: "Top lane Keith", 47: "Top lane Charlie",
	48: "Mick position 7 away", 49: "Mick position 6", 50: "Mick position 4", 51: "Mick position 3", 52: "Mick position 2", 53: "Mick position 1 home",
	58: "Album Multiball", 60: "Left pop bumper LED", 61: "Right pop bumper LED", 62: "Bottom pop bumper LED",
}


def lamps(limited_edition: bool) -> list[dict[str, object]]:
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else STANDARD_RUNTIME_SOURCE
	items = []
	for address in range(1, 81):
		label = LAMPS.get(address, f"Unused lamp {address}")
		availability = "used" if address in LAMPS else "unused"
		physical = {"notes": "The official chart has no Mick-position-5/park lamp; positions 1-4 and 6-7 are the only six position lamps."} if address == 54 else None
		items.append(output(address, label, "lamp", availability, (MANUAL_SOURCE, VPX_SOURCE, runtime_source) if availability == "used" else (MANUAL_SOURCE,), "pinmame.output.lamp", manual_address=str(address), physical=physical, output_id=f"lamp.{slug(label)}-{address}"))
	items.append(output(0, "General illumination master", "gi", "used", (MANUAL_SOURCE, VPX_SOURCE, runtime_source), "pinmame.output.gi", "GI-0", output_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance("validated", *sources)}
	if positions:
		result["positions"] = positions
	return result


def mechanisms(limited_edition: bool) -> list[dict[str, object]]:
	sources = (MANUAL_SOURCE, VPX_SOURCE)
	trough_sensors = (["switch.trough-5-left"] if limited_edition else []) + ["switch.trough-4", "switch.trough-3", "switch.trough-2", "switch.trough-1", "switch.trough-jam"]
	trough_behavior = "Five balls occupy switches 17-21, including one ceramic white ball identified through dedicated public switch 71. Output 1 advances the rightmost ball through jam opto 22 toward shooter-lane switches 23/50." if limited_edition else "Four steel balls occupy switches 18-21. Output 1 advances the rightmost ball through jam opto 22 toward shooter-lane switch 23. Switch 17 and dedicated detector 71 are not installed."
	items = [
		mechanism("mechanism.trough", "Five-ball trough with ceramic ball" if limited_edition else "Four-ball trough", "other", ["device.trough-up-kicker"], trough_sensors, trough_behavior, sources),
		mechanism("mechanism.shooter", "Auto launcher and manual plunger", "kicker", ["device.auto-launch"], ["switch.shooter-lane"] + (["switch.shooter-lane-top"] if limited_edition else []), "Output 2 fires the auto plunger while the cabinet manual plunger remains functional. The Limited Edition adds top shooter-lane switch 50; Standard uses switch 23 only.", sources),
		mechanism("mechanism.center-lock", "Center lock lift and latch", "kicker", ["device.center-lockup-up", "device.center-lockup-latch"], ["switch.center-lock-bottom", "switch.left-lock-2-top"], "Switch 53 senses the bottom of the center lock and switch 46 the upper left-lock position. Output 3 raises the lock, while output 4 energizes the latch; when the latch releases, the two lock barriers drop together to release the held ball route.", sources),
		mechanism("mechanism.moving-mick", "Seven-position Moving Mick target", "motorized", ["device.mick-motor-relay-left", "device.mick-motor-relay-right"], ["switch.mick-position-1-home", "switch.mick-position-2", "switch.mick-position-3", "switch.mick-position-4", "switch.mick-position-5-park", "switch.mick-position-6", "switch.mick-position-7-away", "switch.moving-mick-target-hit"], "Outputs 18/19 move the target left/right across seven sensed stops. The proven table clamps travel to -27..+36 degrees: position 1/home at +34..36, 2 at +24..26, 3 at +14..16, 4 at +3..5, 5/park at -7..-6, 6 at -17..-15, and 7/away at -27..-25. All positions share dedicated hit switch 72; switches 33-39 report carriage position and must not fire on target impact. Lamps exist for positions 1-4 and 6-7 but not position 5.", sources, positions=[
			{"id": "position.home", "label": "Position 1 / home / right", "sensors": ["switch.mick-position-1-home"], "description": "+34 through +36 degrees in the proven VPX model"},
			{"id": "position.2", "label": "Position 2", "sensors": ["switch.mick-position-2"], "description": "+24 through +26 degrees"},
			{"id": "position.3", "label": "Position 3", "sensors": ["switch.mick-position-3"], "description": "+14 through +16 degrees"},
			{"id": "position.4", "label": "Position 4", "sensors": ["switch.mick-position-4"], "description": "+3 through +5 degrees"},
			{"id": "position.park", "label": "Position 5 / park", "sensors": ["switch.mick-position-5-park"], "description": "-7 through -6 degrees"},
			{"id": "position.6", "label": "Position 6", "sensors": ["switch.mick-position-6"], "description": "-17 through -15 degrees"},
			{"id": "position.away", "label": "Position 7 / away / left", "sensors": ["switch.mick-position-7-away"], "description": "-27 through -25 degrees"},
		]),
		mechanism("mechanism.left-control-gate", "Left controlled gate", "gate", ["device.left-control-gate"], [], "Output 6 opens and closes the left control gate; there is no endpoint switch.", sources),
		mechanism("mechanism.flippers", "Two-flipper assembly", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "Outputs 15/16 drive the lower left/right flippers. Public button/EOS pairs are 84/83 and 82/81, with normally-closed EOS contacts. The machine has no upper flippers.", sources),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Left, right, and bottom pop output/switch pairs are 9/30, 10/31, and 11/32; lamps 60-62 are their LEDs and output 26 is their shared feature flasher.", sources),
		mechanism("mechanism.slingshots", "Two slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Left and right slings use output/switch pairs 13/26 and 14/27.", sources),
		mechanism("mechanism.ramps-orbits-lanes", "Ramps, orbits, spinner, and lanes", "other", [], ["switch.left-ramp-exit", "switch.right-ramp-exit", "switch.left-orbit", "switch.right-orbit", "switch.left-orbit-spinner", "switch.left-pop-bumper-lane", "switch.top-lane-ronnie", "switch.top-lane-mick", "switch.top-lane-keith", "switch.top-lane-charlie"], "Switches 42/45 are the ramp exits, 44/48 the left/right orbits, 41 the passive left-orbit spinner, 43 the pop lane, and 6-9 the four band-member top lanes. The service location diagrams are authoritative for the unswitched ramp entrances and return geometry.", sources),
		mechanism("mechanism.targets", "Target banks and standups", "other", [], ["switch.mick-three-bank-bottom-target", "switch.mick-three-bank-middle-target", "switch.mick-three-bank-top-target", "switch.right-three-bank-bottom-target", "switch.right-three-bank-middle-target", "switch.right-three-bank-top-target", "switch.star-target-left", "switch.star-target-center", "switch.star-target-right", "switch.rock-star-target-left", "switch.rock-star-target-right"], "Mick bank switches are 1-3, the right bank is 10-12, STAR standups are 51/57/56, and ROCK STAR standups are 54/55. These are fixed standups, not resettable drop targets.", sources),
		mechanism("mechanism.optional-shaker", "Optional shaker motor", "motorized", ["device.shaker-motor"], [], "Output 8 is the optional 16 VAC shaker installation and may be absent from a stock machine.", sources),
	]
	if limited_edition:
		items.extend([
			mechanism("mechanism.magnetic-ball-diverter", "Premium/LE magnetized ball diverter", "diverter", ["device.left-magnet", "device.right-magnet", "device.left-up-down-post", "device.center-up-down-post", "device.right-up-down-post"], ["switch.left-up-down-post-cabinet-button", "switch.right-up-down-post-cabinet-button", "switch.magnetic-ball-detector"], "The fuller playfield adds two 50 V magnets and three 20 V up/down posts: outputs 5/7 energize the left/right magnets and 17/30/32 raise the left/center/right posts. Raised posts physically block and kick the ball upward in the proven table. Cabinet buttons D13/D15 serialize as public 88/86 for the side posts; the center post is ROM-driven and has no dedicated player button. Public 87/85 are VPX compatibility states mirrored from the flipper keys and are not separate physical switches. Recreate the five physical actuators, button causality, and ball interaction rather than treating the effect as lamp animation.", sources),
			mechanism("mechanism.ceramic-ball", "Ceramic white-ball tracking", "other", [], ["switch.magnetic-ball-detector", "switch.trough-1", "switch.shooter-lane"], "One of the five balls is nonmagnetic ceramic. The proven script preserves its identity through drain/trough recreation, initializes detector 71 active, drives 71 inactive when that ball reaches trough switch 21, and restores it after shooter switch 23 clears. Preserve per-ball identity so magnet behavior and ROM recognition remain coherent.", sources),
		])
	return items


LE_DRIVER_IDS = {driver_id for driver_id, driver in DRIVERS.items() if "Limited Edition" in driver["description"]}
STANDARD_DRIVER_IDS = set(DRIVERS) - LE_DRIVER_IDS
if LE_DRIVER_IDS != {"rsn_100h", "rsn_110h"} or STANDARD_DRIVER_IDS != {"rsn_103", "rsn_105", "rsn_110"}:
	raise ValueError("Rolling Stones drivers must classify exhaustively as Standard or Limited Edition")


def driver_records(limited_edition: bool) -> list[dict[str, object]]:
	selected_ids = LE_DRIVER_IDS if limited_edition else STANDARD_DRIVER_IDS
	selected = []
	for driver_id in selected_ids:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision for the Limited Edition physical playfield; the service manual calls the fuller hardware Premium." if limited_edition else "Firmware revision for the Standard physical playfield; the PinMAME clone parent is an LE software-lineage artifact and does not change physical compatibility."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(limited_edition: bool) -> list[dict[str, object]]:
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else STANDARD_RUNTIME_SOURCE
	raw_hash = "81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c" if limited_edition else "56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59"
	rom_hash = "cd01ff42364505034e9bdaabf211852a8ecc6ae499371840687e8297abfcaadf" if limited_edition else "1d17d6faf937bfa583e7c8f0a822bc9db0aee74b205f043f9068fbcff58bb563"
	game = "rsn_110h" if limited_edition else "rsn_110"
	ipdb_source = IPDB_LE_SOURCE if limited_edition else IPDB_STANDARD_SOURCE
	ipdb_id = 5708 if limited_edition else 5668
	return [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/Rolling-Stones-Manual.pdf", "sha256": "1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf", "locator": "Official 99-page scanned Stern manual: switch chart PDF page 51, lamps 53, coils 55/78, major assemblies 1-24, wiring 85-95, and Premium-only notes on 51/55", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "Rolling-Stones-Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T22:32:15.219822Z"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/The%20Rolling%20Stones%20LE%20(Stern%202011)%20v1.0.6i.vbs", "revision": VPX_REVISION, "sha256": "969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033", "locator": "Known-working rsn_110h table script: callbacks, switches, lamps/GI, trough and ceramic-ball identity, center lock, magnets/posts, controlled gate, auto launch, and seven-position Moving Mick causality", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c rsn INITGAME/driver family, SAM_NO_AUX, SAM switch serialization, game-on output, and 128x32 DMD", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames rsn_ driver records and clone graph", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": STERN_SOURCE, "kind": "human_review", "uri": "https://www.sternpinball.com/game/the-rolling-stones/", "locator": "Manufacturer feature inventory: two ramps, Moving Mick target, ball lock, molded lips, songs, modes, and playfield theme", "license": "NOASSERTION", "attribution": "Stern Pinball", "acquired_at": "2026-08-02T22:00:00Z"},
		{"id": ipdb_source, "kind": "human_review", "uri": f"https://www.ipdb.org/machine.cgi?id={ipdb_id}", "locator": f"Physical product identity and edition record IPDB {ipdb_id}", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-02T22:00:00Z"},
		{"id": runtime_source, "kind": "runtime_scenario", "uri": f"external:pinmame-game-code/rolling-stones-{'limited-edition' if limited_edition else 'standard'}/harness/boot-start.raw.json", "revision": PINMAME_REVISION, "sha256": raw_hash, "locator": f"Exact {game} boot/start scenario with physical trough switches initialized, four coin pulses, and start; ROM archive SHA-256 {rom_hash}", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build(limited_edition: bool) -> dict[str, object]:
	machine_id = "stern.the-rolling-stones-limited-edition.2011" if limited_edition else "stern.the-rolling-stones-standard.2011"
	name = "The Rolling Stones Limited Edition" if limited_edition else "The Rolling Stones (Standard)"
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else STANDARD_RUNTIME_SOURCE
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": machine_id, "name": name, "manufacturer": "Stern", "year": 2011, "kind": "physical_pinball", "ipdb_id": 5708 if limited_edition else 5668},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(limited_edition), "inputs": inputs(limited_edition), "outputs": main_outputs(limited_edition) + lamps(limited_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance("validated", CORE_SOURCE, runtime_source)}],
		"mechanisms": mechanisms(limited_edition), "relationships": [], "sources": sources(limited_edition),
		"knowledge": {"path": f"knowledge/stern/the-rolling-stones-{'limited-edition' if limited_edition else 'standard'}-2011.md", "status": "complete"}, "conflicts": [],
	}


STANDARD_KNOWLEDGE = """# The Rolling Stones Standard (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, mechanism causality, wiring, and edition boundary validated**

## Identity and evidence precedence

This definition covers non-`h` drivers `rsn_103`, `rsn_105`, and `rsn_110`. PinMAME roots them under `rsn_110h` for software lineage, but they run the Standard physical playfield. IPDB identifies the Standard machine as 5668. The official Stern service chart governs physical inventory and wiring. The known-working LE VPX script is ground truth for public addresses and shared mechanism causality; its Premium-only devices are never projected onto Standard. Pinned PinMAME governs SAM serialization, `SAM_NO_AUX`, synthetic game-on 33, and the native 128x32 four-bit DMD.

## Edition boundary and initial state

The Standard trough contains four steel balls at switches 18-21. It omits matrix switch 17, top shooter switch 50, dedicated magnetic detector D7/public 71, cabinet post buttons D13/D15, both magnets, all three up/down posts, and Premium bottom-arch output 29. Accordingly outputs 5, 7, 17, 29, 30, and 32 are explicit unused Standard channels. The manual calls the fuller service-chart variant “Premium”; that hardware corresponds to PinMAME's Limited Edition `h` drivers. Standard still uses moving target D8/public 72 and common Mick position switches 33-39.

## Moving Mick

Moving Mick is a physical traversing target with seven discrete sensors, not seven hit targets. Output 18 moves left and 19 right. The proven script clamps travel from -27 to +36 degrees and asserts one sensor only at each narrow stop: 33 home/right, then 34, 35, 36, 39 park, 37, and 38 away/left. All seven positions share dedicated hit switch 72. The collision body must move with Mick across sensed and unsensed transit zones. Six inserts correspond to positions 1-4 and 6-7; position 5/park deliberately has no lamp.

## Locks, shooter, and ball paths

The center lock uses switch 53 at the bottom and switch 46 at the upper left-lock position. Output 3 raises the lock and output 4 holds/releases the latch barriers. Output 1 feeds the trough; output 2 auto-launches from switch 23 while retaining the manual plunger. Output 6 controls the left gate. Ramps exit at 42/45, orbits at 44/48, the passive left-orbit spinner pulses 41, pop lane is 43, and band-member top lanes are 6-9.

## Remaining playfield inventory

The two flippers are outputs 15/16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 13/26 and 14/27. Fixed target groups are Mick 1-3, right bank 10-12, STAR 51/57/56, and ROCK STAR 54/55. Q12 is physically unused, output 8 is the optional shaker, and output 24 is an optional 5 V coin meter. Lamps 1-53, 58, and 60-62 are used; 54-57, 59, and 63-80 are explicit unused addresses. Output flashers 20-23 and 25-28/31 are separate from matrix lamps.

## Author construction checklist

- Build the four-ball trough, manual plunger plus auto launcher, center lock/latch, moving target with seven position sensors and one shared hit switch, left control gate, two flippers, three pops, two slings, spinner, two ramps, two orbits, lanes, and fixed target groups.
- Bind every matrix and dedicated input, output 1-33, lamp 1-80, GI 0, and DMD from the JSON. Keep unused channels explicit and do not add Premium mechanisms to Standard.
- Preserve ball occupancy, lock barriers, moving collision geometry, Mick transit/endpoint causality, and the manual plunger path. Cosmetic animation is insufficient for the moving target or lock.
- Use the proven VPX motion ranges and callback causality as starting values while retaining the official service-manual physical boundary and wiring.

## Sources

- `manual.rolling-stones-standard-le.2011`: official Stern manual, SHA-256 `1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf`; switches PDF page 51, lamps 53, coils 55/78, assemblies 1-24, and wiring 85-95.
- `vpx.rolling-stones-le-1.0.6i`: known-working script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`; used only for shared hardware causality on Standard.
- `runtime.rolling-stones-standard.boot-start`: exact `rsn_110` harness, SHA-256 `56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation and driver family.
"""


LE_KNOWLEDGE = """# The Rolling Stones Limited Edition (Stern, 2011)

Coverage: **author-ready - complete physical inventory, PinMAME bindings, custom mechanisms, wiring, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `rsn_100h` and `rsn_110h`, the PinMAME Limited Edition family, and IPDB machine 5708. The service charts label the fuller hardware “Premium”; the PinMAME descriptions and physical product record call it Limited Edition. They are treated as one physical I/O variant, not a third machine. The known-working `The Rolling Stones LE (Stern 2011) v1.0.6i.vbs` is ground truth for address callbacks and mechanism causality, with the official manual authoritative for installed wiring.

## Five-ball trough and ceramic ball

The LE trough holds five balls at switches 17-21. One is a white nonmagnetic ceramic ball. Dedicated D7 serializes as public 71 with an active-low/normally-closed controller sense: the proven table initializes 71 active, drives it inactive while the ceramic ball occupies trough switch 21, and restores it after the ball clears shooter switch 23. Drain handling preserves the ball's identity. Recreate a per-ball material/type flag; replacing every drain with a generic steel ball breaks detector and magnet behavior. Output 1 feeds through jam opto 22, output 2 auto-launches, and the LE adds top shooter switch 50 while retaining the manual plunger.

## Magnetized ball diverter and player controls

The LE adds left/right 50 V magnets on outputs 5/7 and left/center/right 20 V up/down posts on 17/30/32. In the proven table, an enabled post rises into the ball path and imparts an upward reaction on collision. Dedicated cabinet buttons D13/D15 serialize as public 88/86 for the left/right posts; the center post is ROM-driven and has no dedicated player button. The script also mirrors the ordinary flipper keys into public 87/85, but the service chart leaves physical D14/D16 unpopulated; those are explicit virtual compatibility states, not two extra cabinet switches. Model all five actuators, both real buttons, magnetic response by ball material, and the resulting routing/collision behavior.

## Moving Mick

Outputs 18/19 move Mick left/right across seven stops. Position sensors are 33 home/right, 34, 35, 36, 39 park, 37, and 38 away/left. The proven angular windows are +34..36, +24..26, +14..16, +3..5, -7..-6, -17..-15, and -27..-25 degrees. Every physical collision pulses the single dedicated target switch 72. Keep separate target-hit and carriage-position state, plus unsensed transit geometry. Position 5/park intentionally has no dedicated position lamp.

## Center lock, gate, and common mechanisms

Switches 53/46 sense the center/left lock path. Output 3 raises the lock and output 4 controls its latch; latch release drops both modeled barriers. Output 6 controls the left gate. Flippers use 15/16 with button/EOS pairs 84/83 and 82/81. Pops are 9/30, 10/31, and 11/32; slings 13/26 and 14/27. Ramps exit at 42/45, orbits at 44/48, spinner at 41, pop lane at 43, and top lanes at 6-9. Fixed standups are Mick bank 1-3, right bank 10-12, STAR 51/57/56, and ROCK STAR 54/55.

## Lamps, flashers, and optional devices

Lamps 1-53, 58, and 60-62 are used; 54-57, 59, and 63-80 are unused. Output 29 drives two LE bottom-arch flashers in addition to common flashers 20-23, 25-28, and 31. Q12 is unused. Output 8 is an optional 16 VAC shaker and output 24 an optional 5 V coin meter. The machine uses `SAM_NO_AUX`; no auxiliary-board output range should be invented.

## Author construction checklist

- Build the five-ball typed trough, detector behavior, manual/auto shooter with both switches, two magnets, three up/down posts and cabinet buttons, center lock/latch, moving Mick with all seven positions and shared hit switch, gate, flippers, pops, slings, spinner, ramps, orbits, lanes, and standups.
- Preserve ceramic-versus-steel magnetic response, individual ball identity through drain/trough cycling, raised-post collisions, lock occupancy, and moving-target collision geometry.
- Treat public 87/85 as proven VPX compatibility states with no physical D14/D16; do not turn them into extra cabinet controls. Treat service-manual “Premium” notes as this LE hardware variant.
- Bind the complete explicit I/O address spaces, including unused channels, synthetic game-on 33, GI 0, and the 128x32 DMD.

## Sources

- `manual.rolling-stones-standard-le.2011`: official Stern manual, SHA-256 `1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf`; Premium-only switch/output notes and magnetized-diverter wiring are on PDF pages 51, 55, and 95.
- `vpx.rolling-stones-le-1.0.6i`: known-working LE script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033`.
- `runtime.rolling-stones-limited-edition.boot-start`: exact `rsn_110h` harness, SHA-256 `81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, driver family, display, and no-aux configuration.
"""


def runtime_evidence(limited_edition: bool) -> dict[str, object]:
	game = "rsn_110h" if limited_edition else "rsn_110"
	machine_id = "stern.the-rolling-stones-limited-edition.2011" if limited_edition else "stern.the-rolling-stones-standard.2011"
	raw_hash = "81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c" if limited_edition else "56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59"
	rom_hash = "cd01ff42364505034e9bdaabf211852a8ecc6ae499371840687e8297abfcaadf" if limited_edition else "1d17d6faf937bfa583e7c8f0a822bc9db0aee74b205f043f9068fbcff58bb563"
	initial = "--initial-switch 17 " if limited_edition else ""
	if limited_edition:
		initial += "--initial-switch 71 "
	lamps_seen = [1] + list(range(3, 54)) + [58, 60, 61, 62]
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": [machine_id], "driver_ids": [game],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1}, "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": game, "command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir <isolated-state> {initial}--initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>", "rom_archive_sha256": rom_hash, "raw_runs": [{"name": "boot-start", "sha256": raw_hash, "self_test_pulses": 0}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": lamps_seen, "solenoid_addresses_seen": [18, 19, 33], "gi_addresses_seen": [0]}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/rolling-stones-{'limited-edition' if limited_edition else 'standard'}/harness", "sha256": raw_hash, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def main() -> None:
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/the-rolling-stones-standard-2011.json"), fail_closed_spatial_partial(build(False)))
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/the-rolling-stones-limited-edition-2011.json"), fail_closed_spatial_partial(build(True)))
	write_json(ROOT / "evidence/runtime/sam/rolling-stones-standard-boot-start.json", runtime_evidence(False))
	write_json(ROOT / "evidence/runtime/sam/rolling-stones-limited-edition-boot-start.json", runtime_evidence(True))
	write_text(ROOT / "knowledge/stern/the-rolling-stones-standard-2011.md", fail_closed_spatial_knowledge("stern.the-rolling-stones-standard.2011", STANDARD_KNOWLEDGE))
	write_text(ROOT / "knowledge/stern/the-rolling-stones-limited-edition-2011.md", fail_closed_spatial_knowledge("stern.the-rolling-stones-limited-edition.2011", LE_KNOWLEDGE))


if __name__ == "__main__":
	main()
