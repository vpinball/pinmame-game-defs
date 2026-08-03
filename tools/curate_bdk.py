"""Build the reviewed Batman: The Dark Knight Pro and Home definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("bdk_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.stern-batman-the-dark-knight.2008"
VPX_SOURCE = "vpx.batman-the-dark-knight-pro-1.16"
PRO_ROM_SOURCE = "rom.stern-batman-the-dark-knight.bdk-294"
HOME_ROM_SOURCE = "rom.stern-batman-the-dark-knight-home.bdk-300"
PRO_IPDB_SOURCE = "ipdb.batman-the-dark-knight.5307"
HOME_IPDB_SOURCE = "ipdb.batman-the-dark-knight-home.5583"
PRO_BOOT_SOURCE = "runtime.batman-the-dark-knight-pro.boot-start"
HOME_BOOT_SOURCE = "runtime.batman-the-dark-knight-home.boot-start"
HOME_SWITCH_SOURCE = "runtime.batman-the-dark-knight-home.switch-diagnostic"
HOME_LAMP_SOURCE = "runtime.batman-the-dark-knight-home.lamp-diagnostic"
HOME_COIL_SOURCE = "runtime.batman-the-dark-knight-home.coil-diagnostic"

PRO_MACHINE_ID = "stern.batman-the-dark-knight-pro.2008"
HOME_MACHINE_ID = "stern.batman-the-dark-knight-standard-home-edition.2010"
PRO_DRIVERS = {"bdk_130", "bdk_150", "bdk_160", "bdk_200", "bdk_210", "bdk_220", "bdk_240", "bdk_290", "bdk_294"}
HOME_DRIVERS = {"bdk_300"}
if set(DRIVERS) != PRO_DRIVERS | HOME_DRIVERS:
	raise ValueError("Batman: The Dark Knight driver family must be covered exhaustively")


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
PRO_SWITCHES: dict[int, tuple[str, bool, tuple[str, ...]]] = {
	1: ("BATMAN B target", True, ()), 2: ("BATMAN A target", True, ()), 3: ("BATMAN T target", True, ()), 4: ("BATMAN M target", True, ()), 5: ("BATMAN A2 target", True, ()), 6: ("BATMAN N target", True, ()),
	7: ("Left top lane", False, ()), 8: ("Middle top lane", False, ()), 9: ("Right top lane", False, ()), 11: ("Alfred target", True, ()), 12: ("Scarecrow VUK", False, ("ball.position",)),
	13: ("Center ramp entrance", True, ()), 14: ("Right standup target", True, ()), 15: ("Tournament Start", False, ("cabinet.tournament-start",)), 16: ("Start button", False, ("cabinet.start",)),
	18: ("Trough 4 left", False, ("ball.position",)), 19: ("Trough 3", False, ("ball.position",)), 20: ("Trough 2", False, ("ball.position",)), 21: ("Trough 1 right", False, ("ball.position",)),
	22: ("Trough jam", False, ("ball.position",)), 23: ("Shooter lane", False, ("ball.position",)), 24: ("Left outlane", False, ()), 25: ("Left return lane", False, ()),
	26: ("Left slingshot", True, ()), 27: ("Right slingshot", True, ()), 28: ("Right return lane", False, ()), 29: ("Right outlane", False, ()),
	30: ("Left pop bumper", True, ()), 31: ("Right pop bumper", True, ()), 32: ("Bottom pop bumper", True, ()), 33: ("Skill shot", False, ()),
	34: ("Left loop spinner", True, ()), 35: ("Left loop", True, ()), 36: ("Left Joker target", True, ()), 37: ("Center Joker target", True, ()), 38: ("Pop bumper target", True, ()), 39: ("Pop bumper spinner", True, ()),
	41: ("Right loop", True, ()), 42: ("Scarecrow VUK exit", True, ()), 44: ("Top right eject", False, ("ball.position",)), 45: ("Joker drop target", False, ("position.down",)),
	46: ("Joker lockup", False, ("ball.position",)), 47: ("Batmobile crash target", True, ()), 48: ("Right Joker target", True, ()), 49: ("Left standup target", True, ()),
	50: ("Joker position 1 home", False, ("position.home",)), 51: ("Joker position 2 middle", False, ()), 52: ("Joker position 3 away", False, ()),
	53: ("Mini-playfield top left", False, ()), 54: ("Mini-playfield top right", False, ()), 55: ("Mini-playfield bottom left", False, ()),
	56: ("Crane position 6 away", False, ()), 57: ("Crane position 5", False, ()), 58: ("Crane position 4", False, ()), 59: ("Crane position 3", False, ()), 60: ("Crane position 2", False, ()), 61: ("Crane position 1 home", False, ("position.home",)),
	63: ("Mini-playfield bottom right", False, ()), 64: ("Batmobile ramp eject", False, ("ball.position",)),
}

HOME_SWITCHES: dict[int, tuple[str, bool, tuple[str, ...]]] = {
	1: ("Left top lane", False, ()), 2: ("Center top lane", False, ()), 3: ("Right top lane", False, ()), 4: ("Pop bumper target", True, ()), 5: ("Pop bumper spinner", True, ()),
	6: ("Scarecrow VUK", False, ("ball.position",)), 7: ("Right standup target", True, ()), 8: ("Center ramp entrance", True, ()), 9: ("Alfred target", True, ()),
	10: ("Crane position 6 away", False, ()), 11: ("Crane position 5", False, ()), 12: ("Crane position 4", False, ()), 13: ("Crane position 3", False, ()), 14: ("Crane position 2", False, ()), 15: ("Crane position 1 home", False, ("position.home",)),
	16: ("Left Joker target", True, ()), 17: ("Center Joker target", True, ()), 18: ("Right Joker target", True, ()),
	19: ("Left pop bumper", True, ()), 20: ("Right pop bumper", True, ()), 21: ("Bottom pop bumper", True, ()), 22: ("Left loop", True, ()), 23: ("Left loop spinner", True, ()),
	24: ("Batmobile ramp exit", False, ()), 25: ("Scarecrow VUK exit", True, ()), 26: ("Skill shot", False, ()), 27: ("Joker lockup 1", False, ("ball.position",)), 29: ("Right loop", True, ()),
	33: ("Top right eject", False, ("ball.position",)), 34: ("Tournament Start", False, ("cabinet.tournament-start",)), 35: ("Start button", False, ("cabinet.start",)),
	45: ("Left standup target", True, ()), 46: ("Left outlane", False, ()), 47: ("Left return lane", False, ()), 48: ("Left slingshot", True, ()), 49: ("Right slingshot", True, ()), 50: ("Right return lane", False, ()), 51: ("Right outlane", False, ()),
	53: ("Trough 3 left", False, ("ball.position",)), 54: ("Trough 2", False, ("ball.position",)), 55: ("Trough 1 right", False, ("ball.position",)), 56: ("Trough jam", False, ("ball.position",)), 58: ("Shooter lane", False, ("ball.position",)),
	59: ("BATMAN B target", True, ()), 60: ("BATMAN A target", True, ()), 61: ("BATMAN T target", True, ()), 62: ("BATMAN M target", True, ()), 63: ("BATMAN A2 target", True, ()), 64: ("BATMAN N target", True, ()),
}

PRO_SWITCH_PARTS = {
	**{number: "515-7640-05" for number in range(1, 7)}, 7: "500-6227-04", 8: "500-6227-04", 9: "500-6227-04", 11: "515-7640-02", 12: "180-5209-00", 13: "180-5100-01", 14: "515-7496-08-00", 15: "180-5174-00", 16: "180-5174-00",
	18: "180-5119-02", 19: "180-5119-02", 20: "180-5119-02", 21: "180-5119-02", 22: "180-5119-02", 23: "180-5157-00", 24: "500-6227-04", 25: "500-6227-04", 26: "180-5054-00", 27: "180-5054-00", 28: "500-6227-04", 29: "500-6227-04",
	30: "180-5015-04", 31: "180-5015-04", 32: "180-5015-04", 33: "500-6227-04", 34: "180-5100-04", 35: "180-5087-00", 36: "515-7640-04", 37: "515-7640-04", 38: "515-7568-08", 39: "180-5100-04", 41: "180-5087-00", 42: "180-5010-01", 44: "180-5186-01", 45: "180-5158-00", 46: "180-5157-00", 47: "180-5213-00", 48: "515-7640-04", 49: "515-7568-08",
	50: "520-5291-00", 51: "520-5291-00", 52: "520-5292-00", 53: "180-5057-00", 54: "180-5057-00", 55: "180-5057-00", **{number: "520-5290-00" for number in range(56, 62)}, 63: "180-5057-00", 64: "180-5119-02",
}
PRO_SWITCH_TYPES = {
	**{number: "leaf" for number in {1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 45, 47, 48, 49, 53, 54, 55, 63}},
	**{number: "opto" for number in {12, 18, 19, 20, 21, 22, 23, 42, 44, 46, 50, 51, 52, 56, 57, 58, 59, 60, 61, 64}}, 15: "button", 16: "button",
}
HOME_SWITCH_TYPES = {**{number: "opto" for number in {6, 10, 11, 12, 13, 14, 15, 25, 27, 53, 54, 55, 56, 58}}, 34: "button", 35: "button"}


def switch_specs(home: bool) -> dict[int, tuple[str, bool, tuple[str, ...]]]:
	return HOME_SWITCHES if home else PRO_SWITCHES


def switch_id(number: int, home: bool) -> str:
	label = switch_specs(home)[number][0] if number in switch_specs(home) else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int, home: bool) -> dict[str, object]:
	spec = switch_specs(home).get(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	drive_index, return_index = divmod(number - 1, 16)
	sources = (HOME_SWITCH_SOURCE, MANUAL_SOURCE, CORE_SOURCE) if home else (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE)
	physical: dict[str, object] = {"switch_type": (HOME_SWITCH_TYPES if home else PRO_SWITCH_TYPES).get(number, "unknown")}
	if not home and number in PRO_SWITCH_PARTS:
		physical["part_number"] = PRO_SWITCH_PARTS[number]
	if home and spec:
		physical["notes"] = "The exact Home Edition factory contact part is not documented in the available Pro manual. The exact V3.00 ROM diagnostic validates this address and semantic, but not contact duration; pulse or sustained behavior is a functional inference from the named device class and the proven Pro analogue where one exists. Use a functionally equivalent sensor with the declared behavior."
	elif not home and spec:
		physical["notes"] = "The official service-manual grid supplies the physical switch assembly and location; the proven table supplies controller-facing pulse or sustained behavior."
	result: dict[str, object] = {
		"id": switch_id(number, home), "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)), "normally_closed": False, "pulse": spec[1] if spec else False, "availability": "used" if spec else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board switch matrix", "drive_wire": MATRIX_DRIVE[drive_index][0], "drive_connection": MATRIX_DRIVE[drive_index][1], "return_wire": MATRIX_RETURN[return_index][0], "return_connection": MATRIX_RETURN[return_index][1]},
		"provenance": provenance(*sources),
	}
	if spec and spec[2]:
		result["roles"] = list(spec[2])
	return result


DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin chute", "Center coin chute", "Right coin chute", "Unused fourth coin chute", "Optional fifth coin chute", "Unused dedicated switch D6", "Unused dedicated switch D7", "Unused dedicated switch D8",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Unused upper-left flipper button", "Unused upper-left flipper end-of-stroke", "Unused upper-right flipper button", "Scarecrow crane hit",
	"Pendulum tilt", "Slam tilt", "Optional ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "unknown", "button", "unknown", "unknown", "unknown", "button", "leaf", "button", "leaf", "unknown", "unknown", "unknown", "leaf", "tilt", "tilt", "microswitch", "unknown", "button", "button", "button", "button"]
DEDICATED_AVAILABILITY = ["used", "used", "used", "unused", "optional", "unused", "unused", "unused", "used", "used", "used", "used", "unused", "unused", "unused", "used", "used", "used", "optional", "unused", "used", "used", "used", "used"]
DEDICATED_ROLES = {65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 69: "cabinet.coin.fifth", 84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos", 85: "mechanism.crane.hit", -7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter"}
DEDICATED_WIRES = [
	("PNK-BRN", "J2-P2"), ("PNK-RED", "J2-P3"), ("PNK-ORG", "J2-P4"), ("PNK-YEL", "J2-P6"), ("PNK-GRN", "J2-P7"), ("PNK-BLU", "J2-P8"), ("PNK-VIO", "J2-P9"), ("PNK-GRY", "J2-P10"),
	("GRY-BRN", "J3-P1"), ("GRY-RED", "J3-P2"), ("GRY-ORG", "J3-P4"), ("GRY-YEL", "J3-P5"), ("GRY-GRN", "J3-P6"), ("GRY-BLU", "J3-P7"), ("GRY-VIO", "J3-P8"), ("GRY-BLK", "J3-P9"),
	("LGN-BRN", "J13-P1"), ("LGN-RED", "J13-P3"), ("LGN-ORG", "J13-P4"), ("LGN-YEL", "J13-P5"), ("LGN-BLK", "J13-P6"), ("LGN-BLU", "J13-P7"), ("LGN-VIO", "J13-P8"), ("LGN-GRY", "J13-P9"),
]
DEDICATED_GROUNDS = [("BLK", "J2-P1/11")] * 8 + [("BLK", "J3-P10")] * 8 + [("BLK", "J13-P10")] * 8


def dedicated_id(number: int) -> str:
	return f"switch.d{number}-{slug(DEDICATED_LABELS[number - 1])}"


def dedicated_switch(number: int, home: bool) -> dict[str, object]:
	index = number - 1
	device = DEDICATED_DEVICES[index]
	availability = DEDICATED_AVAILABILITY[index]
	result: dict[str, object] = {
		"id": dedicated_id(number), "label": DEDICATED_LABELS[index], "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": device}, "aliases": aliases("pinmame.switch", device, f"D-{number}"),
		"normally_closed": number in {10, 12, 18}, "pulse": number in {1, 2, 3, 5, 16}, "availability": availability, "physical": {"switch_type": DEDICATED_TYPES[index] if availability != "unused" else "unknown"},
		"wiring": {"board": "CPU/Sound board dedicated-switch input", "drive_wire": DEDICATED_WIRES[index][0], "drive_connection": DEDICATED_WIRES[index][1], "return_wire": DEDICATED_GROUNDS[index][0], "return_connection": DEDICATED_GROUNDS[index][1]},
		"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, HOME_SWITCH_SOURCE if home else VPX_SOURCE),
	}
	if home and number == 16:
		result["physical"]["notes"] = "The Home matrix sweep covers only addresses 1-64. D16/public 85 is retained from PinMAME's shared SAM_GAME_3LEDS_BSTB crane-board configuration, the physical Home crane/IPDB review, and the official Pro crane-board manual; the proven Pro script confirms the hit input's momentary behavior."
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	return result


def inputs(home: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, home) for number in range(1, 65)]
	items.extend(dedicated_switch(number, home) for number in range(1, 25))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE)})
	return items


# label, kind, availability
PRO_COILS: dict[int, tuple[str, str, str]] = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Top right eject", "coil", "used"), 4: ("Joker lockup", "coil", "used"),
	5: ("Joker drop target up", "coil", "used"), 6: ("Scarecrow VUK", "coil", "used"), 7: ("Joker drop target down", "coil", "used"), 8: ("Optional shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"), 12: ("Left control gate", "coil", "used"),
	13: ("Batmobile ramp down", "coil", "used"), 14: ("Batmobile ramp control gate", "coil", "used"), 15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"),
	17: ("Left slingshot", "coil", "used"), 18: ("Right slingshot", "coil", "used"), 19: ("Scarecrow home flasher", "flasher", "used"), 20: ("Unused output Q20", "coil", "unused"),
	21: ("Back panel flasher", "flasher", "used"), 22: ("Joker flasher x3", "flasher", "used"), 23: ("Scarecrow flasher", "flasher", "used"), 24: ("Optional 5 V controlled device", "coil", "optional"),
	25: ("Pop bumpers flasher x3", "flasher", "used"), 26: ("Joker motor", "motor", "used"), 27: ("Left slingshot flasher", "flasher", "used"), 28: ("Scarecrow motor relay", "relay", "used"),
	29: ("Right slingshot flasher", "flasher", "used"), 30: ("Joker motor relay", "relay", "used"), 31: ("Scarecrow motor", "motor", "used"), 32: ("Batmobile crash flasher x2", "flasher", "used"),
}
HOME_COILS: dict[int, tuple[str, str, str]] = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Top right eject", "coil", "used"), 4: ("Joker lockup", "coil", "used"),
	5: ("Unused output Q5", "coil", "unused"), 6: ("Scarecrow VUK", "coil", "used"), 7: ("Unused output Q7", "coil", "unused"), 8: ("Optional shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"), 12: ("Unused output Q12", "coil", "unused"),
	13: ("Unused output Q13", "coil", "unused"), 14: ("Unused output Q14", "coil", "unused"), 15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"),
	17: ("Left slingshot", "coil", "used"), 18: ("Right slingshot", "coil", "used"), 19: ("Scarecrow home flasher", "flasher", "used"), 20: ("Unused output Q20", "coil", "unused"),
	21: ("Back panel flasher", "flasher", "used"), 22: ("Joker flasher", "flasher", "used"), 23: ("Scarecrow flasher", "flasher", "used"), 24: ("Optional 5 V controlled device", "coil", "optional"),
	25: ("Pop bumpers flasher", "flasher", "used"), 26: ("Batmobile flasher", "flasher", "used"), 27: ("Left slingshot flasher", "flasher", "used"), 28: ("Scarecrow motor relay", "relay", "used"),
	29: ("Right slingshot flasher", "flasher", "used"), 30: ("Unused output Q30", "coil", "unused"), 31: ("Scarecrow motor", "motor", "used"), 32: ("Batmobile crash flasher", "flasher", "used"),
}
# The Batman manual's machine-specific Q20 row says VIO-WHT at J7-P6. Preserve it even though later generic SAM references used by other curators print VIO-YEL.
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-WHT", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def coil_specs(home: bool) -> dict[int, tuple[str, str, str]]:
	return HOME_COILS if home else PRO_COILS


def output_id(address: int, home: bool) -> str:
	return f"device.{address}-{slug(coil_specs(home)[address][0])}"


def coil_wiring(address: int, home: bool, availability: str) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if availability == "unused":
		return wiring
	if address == 8:
		wiring.update({"power_wire": "RED-WHT", "power_connection": "J17-P7", "nominal_voltage_v": 16, "voltage_type": "ac"})
	elif address == 15:
		wiring.update({"power_wire": "GRY-YEL via RED-YEL fused flipper feed", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 16:
		wiring.update({"power_wire": "BLU-YEL via RED-YEL fused flipper feed", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4-8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	elif home and address in {1, 2, 4, 6, 9, 10, 11}:
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif home and address in {3, 17, 18, 28, 31}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif home and address in {19, 21, 22, 23, 25, 26, 27, 29, 32}:
		wiring.update({"power_wire": "ORG", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif not home and address in {1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 14}:
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif not home and address == 13:
		wiring.update({"power_wire": "BLU-YEL via RED-YEL 3 A fuse", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif not home and address in {3, 17, 18, 26, 28, 30, 31}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif not home and address in {19, 21, 22, 23, 25, 27, 29, 32}:
		wiring.update({"power_wire": "ORG", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	return wiring


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, stable_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def main_outputs(home: bool) -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	semantic_sources = (HOME_COIL_SOURCE, HOME_ROM_SOURCE, CORE_SOURCE, MANUAL_SOURCE) if home else (MANUAL_SOURCE, VPX_SOURCE, PRO_ROM_SOURCE, CORE_SOURCE)
	for address, (label, kind, availability) in coil_specs(home).items():
		physical: dict[str, object] = {}
		if availability == "unused":
			physical["notes"] = "The exact ROM Single Coil Test skips this transistor address; leave it unpopulated as a machine device."
		elif address == 8:
			physical["notes"] = "Optional factory shaker motor; absence is a valid cabinet configuration."
		elif address == 24:
			physical["notes"] = "Optional common SAM 5 V device channel, such as a coin meter; no stock playfield device is installed."
		elif home and address == 26:
			physical["notes"] = "The Home Edition uses Q26 as an orange-fed Batmobile flasher. The Pro machine uses the same address for its brown-fed Joker motor; never project that Pro mechanism onto this product."
		elif not home and address == 26:
			physical.update({"part_number": "041-5108-00", "notes": "One-direction Joker reveal motor, gated by Q30 and position sensors 50-52."})
		elif not home and address == 28:
			physical["part_number"] = "511-5159-01"
		elif not home and address == 30:
			physical["part_number"] = "511-5159-00"
		elif not home and address == 31:
			physical["part_number"] = "041-5107-*"
		items.append(make_output(address, label, kind, availability, semantic_sources, manual_address=f"Q{address}", physical=physical, wiring=coil_wiring(address, home, availability), stable_id=output_id(address, home)))
	game_on_availability = "unused" if home else "used"
	game_on_sources = (CORE_SOURCE, HOME_BOOT_SOURCE) if home else (CORE_SOURCE, PRO_BOOT_SOURCE)
	game_on_notes = "Pinned PinMAME has no bdk_300 fast-flip address and the exact Home boot/start trace emits no public solenoid 33 callback. Drive the physical flippers from Q15/Q16 and their button/EOS inputs; do not invent a game-on transistor." if home else "Synthetic SAM fast-flip game-on output with no physical Q33 device; the exact Pro boot/start trace observes it."
	items.append(make_output(33, "PinMAME SAM game-on state", "virtual", game_on_availability, game_on_sources, physical={"notes": game_on_notes}, stable_id="virtual.game-on"))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused SAM auxiliary compatibility address {address}", "virtual", "unused", (CORE_SOURCE,), physical={"notes": "Batman uses no custom-solenoid auxiliary board. This is explicit public emulator capacity, not installed hardware."}, stable_id=f"virtual.aux-{address}"))
	return items


PRO_LAMPS = {
	1: "Start Button", 2: "Tournament Start Button", 3: "Shoot Again", 4: "Left Outlane", 5: "Left Return Lane", 6: "Joker Played", 7: "Batmobile Played", 8: "Scarecrow Played",
	9: "Joker Multiplier", 10: "Right Return Lane", 11: "Right Outlane", 12: "Bruce Wayne", 13: "Commissioner Gordon", 14: "Rachel Dawes", 15: "The Scarecrow", 16: "The Joker",
	17: "Harvey Dent", 18: "Lucius Fox", 19: "Alfred Pennyworth", 20: "BATMAN B", 21: "BATMAN A", 22: "BATMAN T", 23: "BATMAN M", 24: "BATMAN A2",
	25: "BATMAN N", 26: "Impostors!", 27: "Extricate Lau", 28: "Rescue Rachel", 29: "Locate The Joker", 30: "Not Used", 31: "Left Loop Multiplier", 32: "Crane Position 6 Away",
	33: "Bat Missions", 34: "Mystery", 35: "Left Loop Arrow", 36: "Joker Arrow", 37: "Joker Lock 3", 38: "Joker Lock 2", 39: "Left Gordon Target", 40: "Left Multiplier Target",
	41: "Joker Lock 1", 42: "Crane Position 5", 43: "Crane Position 4", 44: "Crane Position 3", 45: "Crane Position 2", 46: "Not Used", 47: "Batmobile 3", 48: "Batmobile 2",
	49: "Batmobile 1", 50: "Center Ramp Multiplier", 51: "Scarecrow VUK Multiplier", 52: "Right Loop Multiplier", 53: "Right Multiplier Target", 54: "Scarecrow VUK Arrow", 55: "Super Jackpot", 56: "Scarecrow",
	57: "Extra Ball", 58: "Alfred Target", 59: "Mini-playfield Bottom Left", 60: "Left Pop Bumper", 61: "Right Pop Bumper", 62: "Mini-playfield Top Left", 63: "Right Loop Arrow", 64: "Bat Pod",
	65: "Grappling Hook", 66: "Machine Gun", 67: "Cannon", 68: "Mini-playfield Bottom Right", 69: "Scarecrow Skill Shot", 70: "Batmobile Skill Shot", 71: "Joker Skill Shot", 72: "Left Top Lane",
	73: "Middle Top Lane", 74: "Right Top Lane", 75: "Mini-playfield Top Right", 76: "Bat Symbol", 77: "Pop Bumpers Illumination", 78: "Batmobile Illumination", 79: "Joker Illumination", 80: "Scarecrow Illumination",
}
HOME_LAMPS = {
	1: "Joker Played", 2: "Batmobile Played", 3: "Scarecrow Played", 4: "Crane Position 6 Away", 5: "Bat Missions", 6: "Mystery", 7: "Left Loop Arrow", 8: "Pop Bumpers",
	9: "BATMAN B", 10: "BATMAN A", 11: "BATMAN T", 12: "BATMAN M", 13: "BATMAN A2", 14: "BATMAN N", 15: "Start Button", 16: "Tournament Start",
	17: "Left Top Lane", 18: "Center Top Lane", 19: "Right Top Lane", 20: "Right Multiplier Target", 21: "Alfred Target", 22: "Scarecrow Skill Shot", 23: "Batmobile Skill Shot", 24: "Joker Skill Shot",
	25: "Bruce Wayne", 26: "Commissioner Gordon", 27: "Rachel Dawes", 28: "The Scarecrow", 29: "The Joker", 30: "Harvey Dent", 31: "Lucius Fox", 32: "Alfred Pennyworth",
	33: "Impostors!", 34: "Extricate Lau", 35: "Rescue Rachel", 36: "Locate The Joker", 37: "Batmobile 3", 38: "Batmobile 2", 39: "Batmobile 1", 40: "Crane Position 4",
	41: "Shoot Again", 42: "Scarecrow VUK Arrow", 43: "Super Jackpot", 44: "The Scarecrow (Lamp 44)", 45: "Extra Ball", 46: "Crane Position 3", 47: "Not Used", 48: "Bat Symbol",
	49: "Joker Arrow", 50: "Joker Lock 3", 51: "Joker Lock 2", 52: "Left Multiplier Target", 53: "Joker Lock 1", 54: "Crane Position 5", 55: "Left Gordon Target", 56: "Right Loop Arrow",
	57: "Bat Pod", 58: "Grappling Hook", 59: "Machine Gun", 60: "Cannon", 61: "Crane Position 2", 62: "Left Outlane", 63: "Left Return Lane", 64: "Right Return Lane",
	65: "Right Outlane", 66: "Left Pop Bumper", 67: "Right Pop Bumper", 68: "Not Used", 69: "Ramp Billboard 1 Top", 70: "Ramp Billboard 2", 71: "Ramp Billboard 3", 72: "Ramp Billboard 4 Bottom",
	73: "Not Used", 74: "Not Used", 75: "Not Used", 76: "Left Loop Multiplier", 77: "Joker Multiplier", 78: "Center Ramp Multiplier", 79: "Scarecrow VUK Multiplier", 80: "Right Loop Multiplier",
}
LAMP_DRIVE = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
PRO_44_CLEAR = {9, 26, 27, 28, 29, 37, 38, 40, 41, 47, 50, 51, 52, 53, 54, 76, 77}
PRO_GREEN = {59, 62, 68, 75}
PRO_WHITE_LED = {60, 61, 70}


def lamps(home: bool) -> list[dict[str, object]]:
	labels = HOME_LAMPS if home else PRO_LAMPS
	unused = {47, 68, 73, 74, 75} if home else {30, 46}
	sources = (HOME_LAMP_SOURCE, HOME_ROM_SOURCE, CORE_SOURCE, MANUAL_SOURCE) if home else (MANUAL_SOURCE, CORE_SOURCE, VPX_SOURCE)
	items: list[dict[str, object]] = []
	for address in range(1, 81):
		label = labels[address]
		availability = "unused" if address in unused else "used"
		physical: dict[str, object] = {"location": label} if availability == "used" else {}
		if availability == "unused":
			physical["notes"] = "The exact machine-specific lamp table labels this address Not Used; do not install a lamp."
		elif not home:
			if address in PRO_GREEN:
				physical.update({"part_number": "165-5053-04-HF", "notes": "Factory #44 green lamp assembly from the official matrix grid."})
			elif address in PRO_WHITE_LED:
				physical.update({"part_number": "112-5024-08", "notes": "Factory white LED board from the official matrix grid."})
			elif address in PRO_44_CLEAR:
				physical.update({"part_number": "165-5000-44-HF", "notes": "Factory #44 clear lamp assembly from the official matrix grid."})
			else:
				physical.update({"part_number": "165-5002-00", "notes": "Factory #555 clear lamp assembly from the official matrix grid."})
		else:
			physical["notes"] = "Exact V3.00 ROM Single Lamp Test semantic. The unavailable Home service manual prevents claiming a factory bulb part; reproduce this independently controlled visual function at the named location."
		if home and address == 44:
			physical["notes"] += " The ROM diagnostic prints the same The Scarecrow text as lamp 28; the numeric suffix distinguishes this mission-block insert without inventing another semantic name."
		if home and address in {30, 46}:
			physical["notes"] += " Pinned PinMAME revision 4ec52ff incorrectly applies the Pro model's CORE_MODOUT_NONE setting here, so physical/PWM ChangedLamps suppresses the real Home lamp. A LibPinMAME adapter must restore a non-NONE lamp output type for this same address after game start; never remap it."
		if home and address == 47:
			physical["notes"] += " Pinned PinMAME leaves this unused Home address transport-active because it inherited the Pro output-type table; ignore any callback and do not substitute it for real lamp 46."
		column = (address - 1) % 8
		row = (address - 1) // 8
		wiring = {"board": "I/O Power Driver board lamp matrix", "drive_wire": LAMP_DRIVE[column][0], "drive_connection": LAMP_DRIVE[column][1], "return_wire": LAMP_RETURN[row][0], "return_connection": LAMP_RETURN[row][1]}
		items.append(make_output(address, label, "lamp", availability, sources, group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring=wiring, stable_id=f"lamp.{address}-{slug(label)}"))
	for address in range(81, 86):
		items.append(make_output(address, f"Unused crane-board compatibility lamp {address}", "lamp", "unused", (CORE_SOURCE,), group="pinmame.output.lamp", physical={"notes": "Unpopulated compatibility slot before the three retained crane-board LEDs."}, stable_id=f"lamp.{address}-unused-crane-board-compatibility"))
	for address, label in {86: "Scarecrow crane board red LED", 87: "Scarecrow crane board white LED 1", 88: "Scarecrow crane board white LED 2"}.items():
		board_sources = (CORE_SOURCE, HOME_LAMP_SOURCE, MANUAL_SOURCE) if home else (CORE_SOURCE, MANUAL_SOURCE)
		items.append(make_output(address, label, "lamp", "used", board_sources, group="pinmame.output.lamp", physical={"location": "Scarecrow crane opto/LED board 520-5290-00", "part_number": "520-5290-00", "notes": "PinMAME SAM_GAME_3LEDS_BSTB exposes the retained board LED at this backward-compatible ChangedLamps address."}, wiring={"board": "Scarecrow crane opto/LED board 520-5290-00"}, stable_id=f"lamp.{address}-{slug(label)}"))
	gi_sources = (HOME_BOOT_SOURCE, CORE_SOURCE) if home else (PRO_BOOT_SOURCE, VPX_SOURCE, CORE_SOURCE)
	items.append(make_output(0, "General illumination master", "gi", "used", gi_sources, group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Playfield general illumination", "notes": "PinMAME exposes ordinary GI as aggregate channel 0."}, stable_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions is not None:
		result["positions"] = positions
	return result


def pro_mechanisms() -> list[dict[str, object]]:
	common = (VPX_SOURCE, MANUAL_SOURCE, PRO_ROM_SOURCE, PRO_IPDB_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", [output_id(1, False)], [switch_id(number, False) for number in range(18, 23)], "Four balls occupy switches 18-21. Q1 ejects the rightmost ball through jam opto 22 toward shooter switch 23; keep individual occupancy and the physical jam transition.", common),
		mechanism("mechanism.auto-launch", "Manual shooter with auto launch", "kicker", [output_id(2, False)], [switch_id(23, False)], "The player can plunge a ball at switch 23 manually or Q2 can fire the auto-launch assembly.", common),
		mechanism("mechanism.top-right-eject", "Top-right eject", "kicker", [output_id(3, False)], [switch_id(44, False)], "A ball rests on top-right eject switch 44 until Q3 returns it to play.", common),
		mechanism("mechanism.joker-lock", "Joker lockup", "kicker", [output_id(4, False)], [switch_id(46, False)], "Switch 46 retains a ball in the Joker lockup and Q4 ejects it. This ball device is separate from the moving Joker reveal and its drop target.", common),
		mechanism("mechanism.joker-drop", "Joker active drop target", "drop_target_bank", [output_id(5, False), output_id(7, False)], [switch_id(45, False)], "The target latches down on switch 45. Q5 raises it and Q7 actively lowers it; preserve both commanded directions rather than modeling a reset-only target.", common, [{"id": "position.up", "label": "Target up", "sensors": []}, {"id": "position.down", "label": "Target down", "sensors": [switch_id(45, False)]}]),
		mechanism("mechanism.scarecrow-vuk", "Scarecrow VUK", "kicker", [output_id(6, False)], [switch_id(12, False), switch_id(42, False)], "A ball held at VUK opto 12 is kicked vertically by Q6 and crosses exit switch 42.", common),
		mechanism("mechanism.batmobile-ramp", "Pivoting Batmobile bridge and crash path", "motorized", [output_id(13, False), output_id(14, False)], [switch_id(13, False), switch_id(47, False), switch_id(64, False)], "Q13 pivots the bridge between its approximately 10-degree raised return path and lowered path, moving its collision geometry and any captured ball. Switch 64 captures the ball on the ramp; lowering releases it while the Batmobile travels a linked crash path that closes target 47. Q14 controls the route gate. Preserve the real ball, bridge collision, gate direction, and crash switch transaction; the script's invisible helper ball is implementation scaffolding, not another playfield ball.", common, [{"id": "position.raised", "label": "Bridge raised", "sensors": []}, {"id": "position.lowered", "label": "Bridge lowered", "sensors": []}]),
		mechanism("mechanism.joker-reveal", "Rotating Joker reveal", "rotary", [output_id(26, False), output_id(30, False)], [switch_id(number, False) for number in (50, 51, 52)], "Q26 motor motion is gated by relay Q30. The proven table models one 1500 ms, 360-step cycle with home switch 50 at step 359, middle switch 51 at 178-182, and away switch 52 at step 0. Recreate a one-direction reveal with three mutually exclusive position windows and stop/calibrate through the ROM's Joker Motor Test.", common, [{"id": "position.home", "label": "Joker hidden/home", "sensors": [switch_id(50, False)]}, {"id": "position.middle", "label": "Mid travel", "sensors": [switch_id(51, False)]}, {"id": "position.away", "label": "Joker revealed/away", "sensors": [switch_id(52, False)]}]),
		mechanism("mechanism.scarecrow-crane", "Six-position Scarecrow crane", "rotary", [output_id(31, False), output_id(28, False)], [switch_id(number, False) for number in range(56, 62)] + [dedicated_id(16)], "Q31 drives the one-direction chain crane through relay Q28. Position optos run from 56/away through 61/home; the proven table uses 90 steps over 110 ms with windows 56=0-1, 57=30-33, 58=47-50, 59=59-62, 60=71-74, and 61=89. Dedicated D16/public 85 is the ball-hit leaf. The manual documents two factory crane/motor assembly variants; identify the installed hub and shaft type before selecting service parts, never rotate the crane by hand, and calibrate using the ROM test.", common, [{"id": f"position.{number}", "label": f"Crane position {62 - number}{' home' if number == 61 else ' away' if number == 56 else ''}", "sensors": [switch_id(number, False)]} for number in range(56, 62)]),
		mechanism("mechanism.upper-mini-playfield", "Upper mini-playfield", "other", [], [switch_id(number, False) for number in (53, 54, 55, 63)], "Four rollovers identify top-left 53, top-right 54, bottom-left 55, and bottom-right 63. Preserve the elevated ball path and all four contacts; this entire mini-playfield is absent from the Home Edition.", common),
		mechanism("mechanism.flippers", "Lower flippers", "other", [output_id(15, False), output_id(16, False)], [dedicated_id(number) for number in (9, 10, 11, 12)], "Q15/Q16 drive left/right flippers. Public button/EOS pairs are 84/83 and 82/81; both EOS contacts are normally closed.", common),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [output_id(number, False) for number in (9, 10, 11)], [switch_id(number, False) for number in (30, 31, 32)], "Left, right, and bottom pairs are Q9/SW30, Q10/SW31, and Q11/SW32.", common),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [output_id(17, False), output_id(18, False)], [switch_id(26, False), switch_id(27, False)], "Left and right pairs are Q17/SW26 and Q18/SW27.", common),
		mechanism("mechanism.left-control-gate", "Left control gate", "gate", [output_id(12, False)], [], "Q12 controls the left route gate; preserve one-way collision and commanded state.", common),
		mechanism("mechanism.shaker", "Optional shaker motor", "motorized", [output_id(8, False)], [], "Q8 drives the optional 16 VAC shaker; absence is a valid configuration.", common),
		mechanism("mechanism.routes-and-targets", "Routes, lanes, spinners, and fixed targets", "other", [], [switch_id(number, False) for number in sorted(set(PRO_SWITCHES) - {12, 15, 16, 18, 19, 20, 21, 22, 23, 26, 27, 30, 31, 32, 42, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64})], "Build the manual's lane, loop, ramp, spinner, standup, skill-shot, and lower-lane contacts at their named bindings. Use the pulse/sustained flags from the proven script and do not create devices for unused matrix holes.", common),
	]


def home_mechanisms() -> list[dict[str, object]]:
	common = (HOME_SWITCH_SOURCE, HOME_COIL_SOURCE, HOME_ROM_SOURCE, HOME_IPDB_SOURCE)
	return [
		mechanism("mechanism.trough", "Three-ball trough", "kicker", [output_id(1, True)], [switch_id(number, True) for number in (53, 54, 55, 56)], "Three balls occupy trough switches 53-55. Q1 ejects the rightmost ball through jam switch 56 toward shooter switch 58. Do not reuse the Pro trough addresses 18-22.", common),
		mechanism("mechanism.auto-launch", "Manual shooter with auto launch", "kicker", [output_id(2, True)], [switch_id(58, True)], "The player can plunge a ball at switch 58 manually or Q2 can fire the auto-launch assembly.", common),
		mechanism("mechanism.top-right-eject", "Top-right eject", "kicker", [output_id(3, True)], [switch_id(33, True)], "A ball rests at switch 33 until Q3 returns it to play.", common),
		mechanism("mechanism.joker-lock", "Single Joker lockup", "kicker", [output_id(4, True)], [switch_id(27, True)], "Switch 27 retains one ball and Q4 ejects it. The Home product has no motorized Joker reveal and no active Joker drop target.", common),
		mechanism("mechanism.scarecrow-vuk", "Scarecrow VUK", "kicker", [output_id(6, True)], [switch_id(6, True), switch_id(25, True)], "A ball held at VUK switch 6 is kicked by Q6 and crosses exit switch 25.", common),
		mechanism("mechanism.scarecrow-crane", "Six-position Scarecrow crane", "rotary", [output_id(31, True), output_id(28, True)], [switch_id(number, True) for number in range(10, 16)] + [dedicated_id(16)], "Q31 drives the retained one-direction crane through relay Q28. Home V3.00 position sensors are 10/away, 11, 12, 13, 14, and 15/home; D16/public 85 is the ball-hit leaf and lamp addresses 86-88 are its board LEDs. The Pro script is only a comparative implementation reference for the retained board and six-position pattern; use the Home ROM's crane test for direction and endpoint calibration and do not copy Pro switch numbers.", common + (CORE_SOURCE, MANUAL_SOURCE, VPX_SOURCE), [{"id": f"position.{number}", "label": f"Crane position {16 - number}{' home' if number == 15 else ' away' if number == 10 else ''}", "sensors": [switch_id(number, True)]} for number in range(10, 16)]),
		mechanism("mechanism.fixed-batmobile-ramp", "Fixed Batmobile return ramp", "other", [], [switch_id(24, True)], "The Home product has a fixed Batmobile ramp with exit switch 24 and lighting on Q26/Q32. It has no Q13 pivoting bridge, Q14 gate, ball-capture switch 64, or linked moving Batmobile crash transaction from the Pro machine.", common),
		mechanism("mechanism.flippers", "Lower flippers", "other", [output_id(15, True), output_id(16, True)], [dedicated_id(number) for number in (9, 10, 11, 12)], "Q15/Q16 drive left/right flippers. Public button/EOS pairs are 84/83 and 82/81; both EOS contacts are normally closed. Pinned PinMAME has no Home fast-flip/game-on address, so consume the physical flipper outputs directly.", common + (CORE_SOURCE,)),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [output_id(number, True) for number in (9, 10, 11)], [switch_id(number, True) for number in (19, 20, 21)], "Left, right, and bottom pairs are Q9/SW19, Q10/SW20, and Q11/SW21.", common),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [output_id(17, True), output_id(18, True)], [switch_id(48, True), switch_id(49, True)], "Left and right pairs are Q17/SW48 and Q18/SW49.", common),
		mechanism("mechanism.shaker", "Optional shaker motor", "motorized", [output_id(8, True)], [], "Q8 drives the optional 16 VAC shaker; absence is a valid configuration.", common),
		mechanism("mechanism.routes-and-targets", "Routes, lanes, spinners, and fixed targets", "other", [], [switch_id(number, True) for number in sorted(set(HOME_SWITCHES) - {6, 10, 11, 12, 13, 14, 15, 19, 20, 21, 24, 25, 27, 33, 34, 35, 48, 49, 53, 54, 55, 56, 58})], "Build every named lane, loop, ramp, spinner, standup, skill-shot, and lower-lane contact at the Home V3.00 address. The product has no upper mini-playfield, no Joker reveal motor/relay/position bank, and no Joker active drop target.", common),
	]


def driver_records(home: bool) -> list[dict[str, object]]:
	selected: list[dict[str, object]] = []
	for driver_id in HOME_DRIVERS if home else PRO_DRIVERS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		if home:
			record["variant_notes"] = "V3.00 is the distinct Standard/Home/Costco physical product. It must never inherit the Pro playfield despite PinMAME's clone edge to bdk_294."
		else:
			record["variant_notes"] = "Firmware revision for the 2008 Pro/commercial physical product. V2.40-V2.94 change Scarecrow multiball and mechanism calibration in software without changing the installed I/O inventory."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def shared_sources() -> list[dict[str, object]]:
	return [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://www.sternpinball.com/wp-content/uploads/2018/11/Batman_TDK_Manual.pdf", "sha256": "c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219", "locator": "Official 207-page operation and parts manual. PDF pages 6, 8, and 10 are the complete Pro switch, lamp, and Q1-Q32 grids; pages 85-96 document the two Scarecrow crane assembly variants; the game-specific diagnostics describe Joker and crane motor tests. For the Home definition it is used only for the shared SAM connector topology and retained crane-board context, never for Home semantic addresses or omitted Pro mechanisms.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "Batman_TDK_Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T05:50:06.472838Z"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Batman INITGAME/driver family, SAM_GAME_3LEDS_BSTB, public switch translation, 128x32 DMD, bdk_294 fast-flip mapping, missing bdk_300 fast-flip mapping, and prefix-wide output typing that incorrectly applies Pro unused lamps 30/46 to Home V3.00.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames bdk_ driver records and clone graph; source comments identify bdk_294 as Pro and bdk_300 as Standard/Home/Costco.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/jsm174/vpx-standalone-scripts/blob/15d112648a1b94b9f59eb8b3c335d57283653c50/Batman%20%5BThe%20Dark%20Knight%5D%20%28Stern%202008%29%201.16/Batman%20%5BThe%20Dark%20Knight%5D%20%28Stern%202008%29%201.16.vbs", "revision": STANDALONE_REVISION, "sha256": "1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0", "locator": "Known-working exact bdk_294 script. Lines 166-206 establish four-ball initial state and Joker/crane cvpmMech configuration; lines 239-883 establish ball devices, Batmobile bridge/crash causality, targets, routes, and pulse/sustained switch behavior. It is semantic ground truth for Pro. Home uses it only as an explicitly comparative reference for the retained six-position crane pattern.", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpx-standalone-scripts contributors"},
	]


def pro_sources() -> list[dict[str, object]]:
	return shared_sources() + [
		{"id": PRO_ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/bdk_294.zip", "revision": "V2.94", "sha256": "b82a4b996c6561b273a7eda6bcf2a540cb67b3b8947bf439b8e9a8928ace3f49", "locator": "Read-only user-authorized archive. BDK_V2-94_E.BIN SHA-256 2c003b71212e91b965f314509ff507ad5aa0459f8117228f511c03efd67e3b2b; BATreadme.txt SHA-256 b7965b5528d92bc3f76289e58d7d7f4b180119b309f5936bd98f4bbef6901215 documents Batmobile ramp, Scarecrow crane calibration, Joker motor, and two/three-ball Scarecrow multiball revision changes.", "license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external"},
		{"id": PRO_IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=5307", "locator": "IPDB 5307 physical identity, 2008 release, playfield feature inventory, photos, and mechanism descriptions for the commercial machine.", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T04:00:00Z"},
		{"id": PRO_BOOT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/bdk_294/harness/boot-start-v1/run.json", "revision": PINMAME_REVISION, "sha256": "e54ff7c90c52a3305e10961f5e5833a20506e04f373b58d955f47a40b8780bb4", "locator": "Exact bdk_294 boot/start run initialized with trough 18-21, Joker home 50, crane home 61, six coins, and start 16; observes 128x32x4 DMD, GI 0, synthetic game-on 33, and lamp activity.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def home_sources() -> list[dict[str, object]]:
	return shared_sources() + [
		{"id": HOME_ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/bdk_300.zip", "revision": "V3.00", "sha256": "4d34254e60422503a203206e2a50970a2becdb20941f008da159927ed8292612", "locator": "User-authorized archive retained in vpinmame/roms. bdk_300.bin SHA-256 9c4ed3794650496b5d686fdf4e25aedb1b602162da464547d0e76cf0f7b0eab9; ROM-native service diagnostics are the machine-specific semantic source.", "license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external"},
		{"id": HOME_IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=5583", "locator": "IPDB 5583 physical identity, Standard/Home/Costco product history, reported production quantity, and machine photographs. Photos corroborate the simplified fixed Batmobile ramp and retained Scarecrow crane without supplying controller addresses.", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T04:00:00Z"},
		{"id": HOME_BOOT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/bdk_300/harness/boot-start-v3/run.json", "revision": PINMAME_REVISION, "sha256": "1e53a038cdf49bfea8524d938a56560dc36eba03d6ef45c3d18e75629d675029", "locator": "Exact bdk_300 boot/start run initialized with crane home 15 and trough 53-55, six coins, and start 35. It reaches Free Play/game score, observes 128x32x4 DMD and GI 0, and emits no synthetic game-on 33 callback.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": HOME_SWITCH_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/bdk_300/harness/switch-matrix-held-v3/run.json", "revision": PINMAME_REVISION, "sha256": "028db927129a01aeb2226081b21c63203b0f6fc547187e7b487113538f16a7d1", "locator": "Exact V3.00 ROM Switch Test sweep captured while each matrix address 1-64 was held. It had no synthetic initial playfield switches, so every displayed label and unused hole is independently attributable; it does not establish factory contact part numbers.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": HOME_LAMP_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/bdk_300/harness/lamp-diagnostic-v2/run.json", "revision": PINMAME_REVISION, "sha256": "cb5eedfa59f79658cd91f68104c8062dd329cbe9cc582d504b822c16584f50f6", "locator": "Exact V3.00 ROM Single Lamp Test enumerates 1-80 and labels 47/68/73-75 Not Used. It proves real Home lamps 30 Harvey Dent and 46 Crane Position 3 while the physical/PWM callback omits both due to inherited Pro CORE_MODOUT_NONE metadata; callback 47 remains transport-active despite its ROM Not Used label.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": HOME_COIL_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-game-code/bdk_300/harness/coil-diagnostic-v2/run.json", "revision": PINMAME_REVISION, "sha256": "fb2850475661a0e3470e7dbeb2d5d1ff852db86e421a625204fa1b0640a4c52e", "locator": "Exact V3.00 ROM Single Coil Test validates populated Q labels, skips Q5/Q7/Q12-Q14/Q20/Q30, and displays high-side/control wire colors. It proves Home Q26 is an ORANGE-fed Batmobile flasher, not the Pro's BROWN-fed Joker motor.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]


def build(home: bool) -> dict[str, object]:
	machine = {"id": HOME_MACHINE_ID, "name": "Batman: The Dark Knight Standard/Home Edition", "manufacturer": "Stern", "year": 2010, "kind": "physical_pinball", "ipdb_id": 5583} if home else {"id": PRO_MACHINE_ID, "name": "Batman: The Dark Knight Pro", "manufacturer": "Stern", "year": 2008, "kind": "physical_pinball", "ipdb_id": 5307}
	return {
		"format": "pinmame-machine-definition", "schema_version": 1, "machine": machine,
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True}, "drivers": driver_records(home), "inputs": inputs(home), "outputs": main_outputs(home) + lamps(home),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, HOME_BOOT_SOURCE if home else PRO_BOOT_SOURCE)}],
		"mechanisms": home_mechanisms() if home else pro_mechanisms(), "relationships": [], "sources": home_sources() if home else pro_sources(),
		"knowledge": {"path": "knowledge/stern/batman-the-dark-knight-standard-home-edition-2010.md" if home else "knowledge/stern/batman-the-dark-knight-pro-2008.md", "status": "complete"}, "conflicts": [],
	}


PRO_KNOWLEDGE = """# Batman: The Dark Knight Pro (Stern, 2008)

Coverage: **author-ready - complete public I/O inventory, factory wiring and lamp parts, custom mechanisms, firmware family, and recreation behavior validated**

## Identity and evidence precedence

This is the 2008 commercial machine, IPDB 5307, called the Pro model in current Stern/PinMAME terminology. It covers `bdk_130`, `bdk_150`, `bdk_160`, `bdk_200`, `bdk_210`, `bdk_220`, `bdk_240`, `bdk_290`, and `bdk_294`. The known-working exact `bdk_294` VPX script is controller-semantic and causal ground truth; the official manual governs physical construction, wiring, bulb/board types, and service assemblies; pinned PinMAME governs transport, display, and driver identity. The firmware readme documents software-only changes to Scarecrow multiball, Batmobile-ramp handling, crane adjustment/calibration, and Joker motor behavior.

## Balls, trough, shooter, and ejects

Four balls rest on trough switches 18-21. Q1 feeds the rightmost ball through jam opto 22 to shooter switch 23, where it can be plunged manually or fired by Q2. Top-right switch 44/Q3 and Scarecrow VUK switch 12/Q6/exit 42 are separate eject paths. Joker lock switch 46 retains a ball until Q4 fires. Preserve sustained occupancy and explicit physical release transactions rather than pulsing every ball-position switch.

## Joker reveal, target, and lock

The Joker area contains three distinct mechanisms. The lockup is switch 46/Q4. The active drop target is switch 45 with Q5 up and Q7 down. The rotating reveal uses motor Q26 through relay Q30 with three positions: 52 away/revealed, 51 middle, and 50 home/hidden. The proven script models a 1500 ms, 360-step one-direction cycle with windows 52 at 0, 51 at 178-182, and 50 at 359. Use the ROM Joker Motor Test to calibrate the physical assembly, retain mutually exclusive position contacts, and never merge its motor, drop, and ball lock into one animation.

## Scarecrow crane

The chain-driven crane uses Q31 motor through relay Q28. Position optos run 56 away, 57, 58, 59, 60, and 61 home; D16/public 85 is the ball-hit leaf. The proven table models 90 steps over 110 ms with windows 56=0-1, 57=30-33, 58=47-50, 59=59-62, 60=71-74, and 61=89. PinMAME exposes the board LEDs at lamps 86-88. The official manual documents two factory crane variants with different hub and motor-shaft shapes. Identify the actual variant before selecting parts, never rotate it by hand, and use the ROM test for direction, endpoint, and adjustment.

## Batmobile bridge and upper mini-playfield

Q13 pivots the Batmobile bridge between an approximately 10-degree raised return path and its lowered release path, while Q14 controls the gate. Switch 64 captures a real ball on the moving ramp. Lowering the bridge releases that ball and drives the linked Batmobile crash path through switch 47; move collision geometry and the captured ball throughout travel. The proven script uses an invisible helper ball only to animate the Batmobile and pulse the crash transaction, so do not add it to the physical ball count. The upper mini-playfield is a separate elevated area with contacts 53 top-left, 54 top-right, 55 bottom-left, and 63 bottom-right.

## Standard devices, routes, lamps, and display

Flippers are Q15/Q16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed. Pops are Q9/SW30, Q10/SW31, Q11/SW32 and slings are Q17/SW26, Q18/SW27. Q12 controls the left gate and Q8 is an optional shaker. Every lane, standup, spinner, loop, ramp, and target is enumerated in JSON with the manual's assembly part and the working script's pulse/sustained behavior. Lamps 1-80 follow the official grid exactly; only 30 and 46 are unused. Original #555, #44, green, and white-LED parts are preserved, ordinary GI is aggregate 0, crane-board LEDs are 86-88, and the display is native 128x32 four-bit DMD. Public solenoid 33 is synthetic fast-flip/game-on, while 51-66 are unused compatibility capacity.

## Author construction checklist

- Build the four-ball path, manual/auto shooter, both ejects, Joker lock/drop/reveal, six-position crane, moving Batmobile bridge/gate/crash transaction, upper mini-playfield, flippers, pops, slings, left gate, shaker option, routes, targets, complete lamps/GI, and DMD.
- Initialize trough 18-21, Joker home 50, and crane home 61; preserve normally-closed EOS contacts, ball occupancy, position windows, moving collision, drop latching, gate direction, and physical release causality.
- Bind matrix 1-64, dedicated/DIP inputs, Q1-Q32, synthetic 33, unused 51-66, lamps 1-88, GI 0, and the DMD. Never infer Home hardware from the bdk_300 clone edge.

## Sources

- `manual.stern-batman-the-dark-knight.2008`: official 207-page manual SHA-256 `c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219`, organized under the external manual cache with native-text extraction and rendered grid review.
- `vpx.batman-the-dark-knight-pro-1.16`: exact working script SHA-256 `1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0`.
- `rom.stern-batman-the-dark-knight.bdk-294`: exact archive SHA-256 `b82a4b996c6561b273a7eda6bcf2a540cb67b3b8947bf439b8e9a8928ace3f49`; ROM bytes remain external.
- `runtime.batman-the-dark-knight-pro.boot-start`: exact boot/start trace SHA-256 `e54ff7c90c52a3305e10961f5e5833a20506e04f373b58d955f47a40b8780bb4`.
"""


HOME_KNOWLEDGE = """# Batman: The Dark Knight Standard/Home Edition (Stern, 2010)

Coverage: **author-ready - complete V3.00 public I/O inventory, physical product differences, retained crane, transport corrections, and recreation behavior validated**

## Identity and evidence precedence

This is the distinct 2010 Standard/Home/Costco product, IPDB 5583, covered only by `bdk_300`. PinMAME makes it a clone of `bdk_294` for software lineage, but its playfield and address map are materially different. Exact V3.00 ROM switch/lamp/coil diagnostics are machine-specific ground truth. The held matrix sweep validates switch addresses, semantics, and unused holes, not contact duration; pulse/sustained behavior is a functional inference from each named device class and the proven Pro analogue where one exists. IPDB photos govern visible product identity. The official Pro manual supplies only shared SAM connector topology and retained crane-board context; it must not add omitted Pro mechanisms. The known-working Pro script is used only as a clearly labeled comparative reference for the retained six-position crane pattern.

## Balls, trough, shooter, and ejects

The Home product has three balls on trough switches 53-55, jam switch 56, and shooter switch 58. Q1 releases the rightmost ball and Q2 auto-launches it. Top-right eject is switch 33/Q3. The Scarecrow VUK is switch 6/Q6 with exit 25. The single Joker lock is switch 27/Q4. These addresses replace the Pro ball path; never initialize or construct a Pro trough at 18-22.

## Retained Scarecrow crane

The Home crane still uses Q31 motor through relay Q28, D16/public 85 for the ball hit, and board LEDs 86-88. Its position sensors are 10 away, 11, 12, 13, 14, and 15 home. This sequence is exact V3.00 ROM evidence and differs from Pro 56-61. D16 lies outside the 1-64 matrix sweep; its Home identity is supported by PinMAME's shared `SAM_GAME_3LEDS_BSTB` configuration, the retained physical crane/IPDB review, the official crane-board manual, and the proven Pro hit-input behavior. Use the Home ROM's crane test to establish direction and tune endpoint windows. The Pro script confirms the retained board's one-direction six-position design only; its 110 ms timing and Pro address ranges are not automatically Home calibration values.

## Simplified playfield and negative knowledge

The Batmobile path is fixed and reports ramp exit 24. Q26 is an orange-fed Batmobile flasher and Q32 the crash flasher; Q13/Q14 are unused, so there is no pivoting bridge or controlled gate. The product has no upper mini-playfield, no Joker reveal motor/relay/position bank, and no active Joker drop target. Q5, Q7, Q12-Q14, Q20, and Q30 are explicitly unused. Build the fixed ramp, three top lanes, both loops, two spinners, VUK, two eject/lock devices, targets, lower lanes, pops, slings, and flippers exactly at the Home addresses rather than removing Pro toys visually while retaining their I/O.

## Lamps and the pinned PinMAME transport correction

The exact ROM Single Lamp Test defines lamps 1-80; only 47, 68, and 73-75 are Not Used. Real lamp 30 is Harvey Dent and real lamp 46 is Crane Position 3. Pinned PinMAME revision `4ec52ff` applies the Pro model's `CORE_MODOUT_NONE` settings to both, suppressing their physical/PWM ChangedLamps callbacks, while unused Home address 47 remains transport-active. A LibPinMAME consumer must restore a non-NONE lamp output type at the same addresses 30 and 46 after `bdk_300` starts and must ignore 47; never remap 30/46 or treat 47 as Crane Position 3. This is a resolved emulator-metadata defect, not a physical ambiguity. The Home ROM also uses crane-board LEDs 86-88 and aggregate GI 0.

## Flippers and game-on state

Flippers are Q15/Q16 with public button/EOS pairs 84/83 and 82/81; both EOS contacts are normally closed. The pinned PinMAME fast-flip table contains `bdk_294` but no `bdk_300`, and the exact Home boot/start trace produces no synthetic solenoid 33 event. Consume Q15/Q16 directly and do not invent a Q33 transistor. A future verified fast-flip address would be an emulator improvement, not a change to physical machine construction.

## Author construction checklist

- Build the three-ball path, manual/auto shooter, top eject, single Joker lock, Scarecrow VUK, six-position crane, fixed Batmobile ramp, flippers, pops, slings, routes, targets, complete Home lamps/GI, and DMD.
- Initialize trough 53-55 and crane home 15; preserve jam/shooter occupancy, crane positions/hit input, normally-closed EOS state, ball locks, and eject causality.
- Bind every matrix/dedicated/DIP input, Q1-Q32 including all explicit unused holes, unavailable synthetic 33, unused 51-66, lamps 1-88 with the 30/46 output-type correction, GI 0, and the 128x32 DMD.
- Do not add the Pro's Joker reveal/drop, pivoting Batmobile bridge/gate, upper mini-playfield, four-ball trough, or Pro switch/output addresses.

## Sources

- `rom.stern-batman-the-dark-knight-home.bdk-300`: exact V3.00 archive SHA-256 `4d34254e60422503a203206e2a50970a2becdb20941f008da159927ed8292612`, retained under `vpinmame/roms`; ROM bytes remain external.
- `runtime.batman-the-dark-knight-home.switch-diagnostic`: complete held matrix trace SHA-256 `028db927129a01aeb2226081b21c63203b0f6fc547187e7b487113538f16a7d1`.
- `runtime.batman-the-dark-knight-home.lamp-diagnostic`: exact lamp selector trace SHA-256 `cb5eedfa59f79658cd91f68104c8062dd329cbe9cc582d504b822c16584f50f6`.
- `runtime.batman-the-dark-knight-home.coil-diagnostic`: exact Q selector trace SHA-256 `fb2850475661a0e3470e7dbeb2d5d1ff852db86e421a625204fa1b0640a4c52e`.
- `runtime.batman-the-dark-knight-home.boot-start`: corrected three-ball boot/start trace SHA-256 `1e53a038cdf49bfea8524d938a56560dc36eba03d6ef45c3d18e75629d675029`.
"""


def runtime_evidence(home: bool) -> dict[str, object]:
	if home:
		raw_runs = [
			{"name": "boot-start-v3", "sha256": "1e53a038cdf49bfea8524d938a56560dc36eba03d6ef45c3d18e75629d675029", "self_test_pulses": 0},
			{"name": "switch-matrix-held-v3", "sha256": "028db927129a01aeb2226081b21c63203b0f6fc547187e7b487113538f16a7d1", "self_test_pulses": 64},
			{"name": "lamp-diagnostic-v2", "sha256": "cb5eedfa59f79658cd91f68104c8062dd329cbe9cc582d504b822c16584f50f6", "self_test_pulses": 80},
			{"name": "coil-diagnostic-v2", "sha256": "fb2850475661a0e3470e7dbeb2d5d1ff852db86e421a625204fa1b0640a4c52e", "self_test_pulses": 32},
		]
		observed_lamps = list(range(1, 30)) + list(range(31, 46)) + list(range(47, 81)) + [86, 87, 88]
		observations = {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": observed_lamps, "lamp_decoder_holes_not_seen": [30, 46], "solenoid_addresses_seen": [], "gi_addresses_seen": [0]}
		command = "Boot: python tools/run_pinmame_harness.py --library <libpinmame> --game bdk_300 --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 15 --initial-switch 53 --initial-switch 54 --initial-switch 55 --pulse 65:300:0.7 <six coin pulses> --pulse 35:500:3 --observe 3 --output <external-json>; held switch/lamp/coil diagnostics: use service switches 0/-1 with --snapshot-while-held and the exact scenario sequences preserved in each external run"
		game, machine_ids, archive_sha, primary_sha = "bdk_300", [HOME_MACHINE_ID], "4d34254e60422503a203206e2a50970a2becdb20941f008da159927ed8292612", raw_runs[0]["sha256"]
	else:
		raw_runs = [{"name": "boot-start-v1", "sha256": "e54ff7c90c52a3305e10961f5e5833a20506e04f373b58d955f47a40b8780bb4", "self_test_pulses": 0}]
		observed_lamps = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 86, 87, 88]
		observations = {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": observed_lamps, "solenoid_addresses_seen": [33], "gi_addresses_seen": [0]}
		command = "python tools/run_pinmame_harness.py --library <libpinmame> --game bdk_294 --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 50 --initial-switch 61 --pulse 65:300:0.7 <six coin pulses> --pulse 16:500:3 --observe 3 --output <external-json>"
		game, machine_ids, archive_sha, primary_sha = "bdk_294", [PRO_MACHINE_ID], "b82a4b996c6561b273a7eda6bcf2a540cb67b3b8947bf439b8e9a8928ace3f49", raw_runs[0]["sha256"]
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": machine_ids, "driver_ids": [game], "extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": game, "command_template": command, "rom_archive_sha256": archive_sha, "raw_runs": raw_runs, "observations": observations},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/{game}/harness", "sha256": primary_sha, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def main() -> None:
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/batman-the-dark-knight-pro-2008.json"), fail_closed_spatial_partial(build(False)))
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/batman-the-dark-knight-standard-home-edition-2010.json"), fail_closed_spatial_partial(build(True)))
	write_json(ROOT / "evidence/runtime/sam/batman-the-dark-knight-pro-boot-start.json", runtime_evidence(False))
	write_json(ROOT / "evidence/runtime/sam/batman-the-dark-knight-home-boot-start-and-diagnostics.json", runtime_evidence(True))
	write_text(ROOT / "knowledge/stern/batman-the-dark-knight-pro-2008.md", fail_closed_spatial_knowledge("stern.batman-the-dark-knight-pro.2008", PRO_KNOWLEDGE))
	write_text(ROOT / "knowledge/stern/batman-the-dark-knight-standard-home-edition-2010.md", fail_closed_spatial_knowledge("stern.batman-the-dark-knight-standard-home-edition.2010", HOME_KNOWLEDGE))


if __name__ == "__main__":
	main()
