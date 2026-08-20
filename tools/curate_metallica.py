"""Build reviewed, author-ready Metallica Premium/LE and Pro definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json as write_json_file, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("mtl_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.metallica-pro-premium"
VPX_SOURCE = "vpx.metallica-premium-monsters-vpw-2.0.2"
VPX_TABLE_SOURCE = "vpx-table.metallica-premium-monsters-vpw-2.0"
RUNTIME_SOURCE = "runtime.metallica-premium.boot-start"
PRO_VPX_SOURCE = "vpx.metallica-pro-jps-6.0.0"
PRO_VPX_TABLE_SOURCE = "vpx-table.metallica-pro-jps-6.0.0"
PRO_RUNTIME_SOURCE = "runtime.metallica-pro.boot-start"

METALLICA_EXCERPTS = [
	{"id": "excerpt.metallica.premium-switches", "locator": "MTLAB1-compressed.pdf PDF page 104, crop box 0.05,0.06,0.95,0.70; Premium switch location and wiring diagrams.", "path": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-switches.md", "sha256": "68e14d56a316100f0a7495ba55d2a1269ee77fceb218045b4b14550cde12efea", "image": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-switches.webp", "image_sha256": "9050ea7971fea1e901c55a5b2550bdac1189b3e9616e7a3d9241ebd166f90e61", "image_derivation": "MTLAB1-compressed.pdf page 104, crop box 0.05,0.06,0.95,0.7, scanned page rendered at its native resolution (embedded image xref 479, 1190px across 8.26in), rendered at 81 dpi, capped to 600px wide, grayscale, 601x605 WebP quality 32", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.metallica.premium-lamps", "locator": "MTLAB1-compressed.pdf PDF page 106, crop box 0.05,0.06,0.95,0.70; Premium lamp location and wiring diagrams.", "path": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-lamps.md", "sha256": "8c5172fc350cdac002bf17cdb92db2a072564ab34828376e05dfa7834e663ba7", "image": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-lamps.webp", "image_sha256": "147346a99d1614496301aedc837a1d7b285baf61653ed0a85f01f74eca35803c", "image_derivation": "MTLAB1-compressed.pdf page 106, crop box 0.05,0.06,0.95,0.7, scanned page rendered at its native resolution (embedded image xref 489, 1190px across 8.26in), rendered at 81 dpi, capped to 600px wide, grayscale, 601x605 WebP quality 32", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.metallica.premium-coils", "locator": "MTLAB1-compressed.pdf PDF page 108, crop box 0.05,0.06,0.95,0.92; Premium coil/back-panel drawing and wiring schematic.", "path": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-coils.md", "sha256": "df990f8b6ddd88f14d4c7fadfe920a4fc9c8b5d33262b4563e800f28c229d83a", "image": "evidence/excerpts/stern.metallica-pro-premium.2013/premium-coils.webp", "image_sha256": "f8bc9812c4b9bf936b7d897e202f4d2e4d2a3e1a0419e7f515bcf5f1ac74cf4d", "image_derivation": "MTLAB1-compressed.pdf page 108, crop box 0.05,0.06,0.95,0.92, scanned page rendered at its native resolution (embedded image xref 499, 1242px across 8.62in), rendered at 94 dpi, capped to 700px wide, grayscale, 701x947 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.metallica.pro-switches", "locator": "MTLAB1-compressed.pdf PDF page 147, crop box 0.05,0.06,0.95,0.70; Pro switch-menu configuration and wiring diagrams.", "path": "evidence/excerpts/stern.metallica-pro-premium.2013/pro-switches.md", "sha256": "7e2aa4c6a4f73c754accc798fa3f742a0170d18e8ccd583cd2312a7a53f6e268", "image": "evidence/excerpts/stern.metallica-pro-premium.2013/pro-switches.webp", "image_sha256": "6d64c57b5a5015cafcdd58e2f69a72add5405e40d606e3098d420e05b4aaaa4f", "image_derivation": "MTLAB1-compressed.pdf page 147, crop box 0.05,0.06,0.95,0.7, scanned page rendered at its native resolution (embedded image xref 682, 1206px across 8.38in), rendered at 81 dpi, capped to 600px wide, grayscale, 601x605 WebP quality 30", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
]


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
	1: ("Left return lane right", "leaf", False, ()), 3: ("Fuel lane rollover", "leaf", True, ()),
	4: ("Fuel lane standup", "microswitch", True, ()), 7: ("Fuel standup bottom", "microswitch", True, ()),
	9: ("Fuel standup top", "microswitch", True, ()), 15: ("Tournament start", "button", False, ()),
	16: ("Start", "button", False, ()), 18: ("Trough 4 left", "microswitch", False, ("ball.position",)),
	19: ("Trough 3", "microswitch", False, ("ball.position",)), 20: ("Trough 2", "microswitch", False, ("ball.position",)),
	21: ("Trough 1 right eject", "microswitch", False, ("ball.position",)), 22: ("Shooter lane jam", "opto", False, ("ball.position",)),
	23: ("Shooter lane", "microswitch", False, ("ball.position",)), 24: ("Left outlane", "leaf", True, ()),
	25: ("Left return lane left", "leaf", True, ()), 26: ("Left slingshot", "leaf", True, ()),
	27: ("Right slingshot", "leaf", True, ()), 28: ("Right return lane", "leaf", True, ()),
	29: ("Right outlane", "leaf", True, ()), 30: ("Left pop bumper", "leaf", True, ()),
	31: ("Right pop bumper", "leaf", True, ()), 32: ("Bottom pop bumper", "leaf", True, ()),
	33: ("Grave marker down", "microswitch", False, ("position.down",)), 34: ("Grave marker up", "microswitch", False, ("position.up",)),
	35: ("Electric chair standup", "microswitch", True, ()), 36: ("Grave lane standup 1 left", "microswitch", True, ()),
	37: ("Grave lane standup 2 right", "microswitch", True, ()), 38: ("Left loop spinner", "other", True, ()),
	39: ("Right loop spinner", "other", True, ()), 40: ("Right ramp standup left", "microswitch", True, ()),
	41: ("Right ramp standup right", "microswitch", True, ()), 42: ("Captive ball", "leaf", True, ()),
	43: ("Left loop", "leaf", True, ()), 44: ("Left top lane", "leaf", True, ()),
	45: ("Right top lane", "leaf", True, ()), 46: ("Right loop", "leaf", True, ()),
	47: ("Right ramp exit", "opto", True, ()), 50: ("Left ramp exit", "opto", True, ()),
	51: ("Right eject scoop", "microswitch", False, ("ball.loaded",)), 52: ("Grave marker opto", "opto", False, ("ball.loaded",)),
	53: ("Electric chair opto", "opto", False, ("ball.loaded",)), 54: ("Snake eject", "microswitch", False, ("ball.loaded",)),
	55: ("Snake jaw open", "microswitch", False, ("position.open",)), 56: ("Snake latch", "microswitch", True, ("position.latched",)),
	57: ("Coffin opto 1 bottom", "opto", False, ("ball.position",)), 58: ("Coffin opto 2 middle", "opto", False, ("ball.position",)),
	59: ("Coffin opto 3 top", "opto", False, ("ball.position",)), 60: ("Drop target bottom", "microswitch", False, ("position.down",)),
	61: ("Drop target middle", "microswitch", False, ("position.down",)), 62: ("Drop target top", "microswitch", False, ("position.down",)),
	63: ("Coffin magnet ball detect", "other", False, ("ball.detected",)), 64: ("Coffin magnet down", "microswitch", False, ("position.down",)),
}


def matrix_switch(number: int, validated: bool) -> dict[str, object]:
	spec = SWITCHES.get(number)
	used = spec is not None
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	sources = (MANUAL_SOURCE, VPX_SOURCE) if validated and used else (MANUAL_SOURCE,)
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": number in (60, 61, 62), "pulse": bool(spec[2]) if spec else False,
		"availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if spec else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance("validated" if validated else "observed", *sources),
	}
	if spec and spec[3]:
		result["roles"] = list(spec[3])
	return result


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, normally_closed: bool, validated: bool) -> dict[str, object]:
	sources = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE) if validated and availability != "unused" else (MANUAL_SOURCE, CORE_SOURCE)
	return {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": normally_closed, "pulse": False, "availability": availability,
		"physical": {"switch_type": switch_type}, "provenance": provenance("validated" if validated else "observed", *sources),
	}


def inputs(validated: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, validated) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left flipper button", "used", "button", False), (83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False), (81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False), (87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Unused dedicated switch D15", "unused", "unknown", False), (85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "optional", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for spec in dedicated:
		items.append(dedicated_switch(*spec, validated))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated" if validated else "observed", MANUAL_SOURCE, CORE_SOURCE)})
	return items


MAIN_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Grave marker magnet", "magnet", "used"),
	4: ("Electric chair magnet", "magnet", "used"), 5: ("Snake eject", "coil", "used"), 6: ("Right eject scoop", "coil", "used"),
	7: ("Unused main output 7", "coil", "unused"), 8: ("Shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	12: ("Snake jaw latch release", "coil", "used"), 13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"), 17: ("Unused main output 17", "coil", "unused"),
	18: ("Electric chair step-up driver", "coil", "used"), 19: ("Grave marker primary flasher", "flasher", "used"),
	20: ("Grave marker motor", "motor", "used"), 21: ("Back panel left flasher", "flasher", "used"),
	22: ("Back panel right flasher", "flasher", "used"), 23: ("Left ramp flasher", "flasher", "used"),
	24: ("Coin meter", "coil", "optional"), 25: ("Pop bumper flasher", "flasher", "used"),
	26: ("Grave marker double flasher", "flasher", "used"), 27: ("Electric chair double flasher", "flasher", "used"),
	28: ("Electric chair spot double flasher", "flasher", "used"), 29: ("Right ramp flasher", "flasher", "used"),
	30: ("Snake flasher", "flasher", "used"), 31: ("Coffin insert double flasher", "flasher", "used"),
	32: ("Electric chair insert flasher", "flasher", "used"), 33: ("Ticket dispenser advance", "coil", "optional"),
	34: ("Ticket dispenser meter", "coil", "optional"), 35: ("Ticket dispenser switched ground", "relay", "optional"),
}
AUX_COILS = {
	51: ("Coffin lock release", "coil", "used", "Q41"), 52: ("Coffin magnet down", "coil", "used", "Q42"),
	53: ("Hammer", "coil", "used", "Q43"), 54: ("Drop targets reset", "coil", "used", "Q44"),
	55: ("Loop up post", "coil", "used", "Q45"), 56: ("Snake jaw close", "coil", "used", "Q46"),
	57: ("Coffin processor D0 mode bit", "virtual", "used", "D0"), 58: ("Coffin processor D1 mode bit", "virtual", "used", "D1"),
}
MAIN_CONTROL = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]


def output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], status: str, group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	alias_namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "manual.service-output" if group == "physical.output.ticket" else "pinmame.solenoid"
	result: dict[str, object] = {"id": output_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(alias_namespace, address, manual_address), "availability": availability, "provenance": provenance(status, *sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def coils(validated: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "candidate"
	items = []
	for address, (label, kind, availability) in MAIN_COILS.items():
		sources = (MANUAL_SOURCE, VPX_SOURCE) if validated and availability != "unused" else (MANUAL_SOURCE,)
		if address in {33, 34, 35}:
			items.append(output(address, label, kind, availability, (MANUAL_SOURCE,), status, "physical.output.ticket", str(address), physical={"notes": "Optional physical ticket-dispenser service function; not a stable LibPinMAME solenoid address."}))
			continue
		wiring = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": MAIN_CONTROL[address - 1] if address <= 32 else f"cabinet-{address}"}
		items.append(output(address, label, kind, availability, sources, status, manual_address=str(address), wiring=wiring))
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE,), status, physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	for address, (label, kind, availability, physical_address) in AUX_COILS.items():
		sources = (MANUAL_SOURCE, VPX_SOURCE, CORE_SOURCE) if validated else (MANUAL_SOURCE, CORE_SOURCE)
		board = "520-5326-01 six-transistor auxiliary driver board" if address <= 56 else "520-6801-00 coffin magnet processor board"
		items.append(output(address, label, kind, availability, sources, status, manual_address=physical_address, wiring={"board": board, "driver_transistor": physical_address}))
	return items


LAMPS = {
	17: "Right loop Electric Chair", 18: "Right loop Snake", 19: "Right loop Grave Marker", 21: "Electric Chair",
	22: "Snake", 23: "Extra Ball", 24: "Crank It Up", 25: "Mystery x2", 26: "Right return lane",
	27: "Right outlane", 28: "Right ramp Electric Chair", 29: "Right ramp Snake", 30: "Right ramp Grave Marker",
	31: "Right ramp standup right", 32: "Right ramp standup left", 33: "Left ramp Electric Chair", 34: "Left ramp Snake",
	35: "Left ramp Grave Marker", 37: "Fuel F", 38: "Fuel 3/4", 39: "Fuel 1/2", 40: "Fuel 1/4",
	41: "Fuel E", 42: "Left return lane in", 43: "Fuel lane award 1", 44: "Fuel lane award 2",
	45: "Fuel lane award 3", 46: "Grave lane Grave Marker", 47: "Grave lane Snake", 48: "Grave lane Electric Chair",
	49: "Left loop Electric Chair", 50: "Left loop Snake", 51: "Left loop Grave Marker", 53: "Shoot Again x2",
	55: "Guitar Pick James", 56: "Guitar Pick Lars", 57: "Guitar Pick Kirk", 58: "Guitar Pick Robert",
	59: "Grave Marker end-of-line", 60: "Electric Chair end-of-line", 61: "Coffin end-of-line", 62: "Snake end-of-line",
	63: "Left outlane", 64: "Left return lane left", 65: "Grave lane standup right", 66: "Left top lane",
	67: "Right top lane", 68: "Electric Chair 1 left", 69: "Electric Chair 2 center", 70: "Electric Chair 3 right",
	71: "Grave lane standup left", 72: "Start", 73: "Bottom pop bumper", 74: "Right pop bumper",
	75: "Left pop bumper", 76: "Tournament start", 77: "Fuel L", 78: "Fuel E final", 79: "Fuel U", 80: "Fuel F final",
}
RGB_CHANNELS = {
	87: ("CN4", "blue", 136.61, 1210.61), 88: ("CN4", "green", 136.61, 1210.61), 89: ("CN4", "red", 136.61, 1210.61),
	90: ("CN5", "blue", 688.84, 847.52), 91: ("CN5", "green", 688.84, 847.52), 92: ("CN5", "red", 688.84, 847.52),
	99: ("CN9", "blue", 802.53, 845.07), 100: ("CN9", "green", 802.53, 845.07), 101: ("CN9", "red", 802.53, 845.07),
	102: ("CN11", "blue", 90.58, 600.67), 103: ("CN11", "green", 90.58, 600.67), 104: ("CN11", "red", 90.58, 600.67),
	108: ("CN13", "blue", 259.57, 786.74), 109: ("CN13", "green", 259.57, 786.74), 110: ("CN13", "red", 259.57, 786.74),
	126: ("CN19", "blue", 320.85, 532.85), 127: ("CN19", "green", 320.85, 532.85), 128: ("CN19", "red", 320.85, 532.85),
}
GI_CHANNELS = {130: "Red GI", 132: "Blue GI", 134: "White upper GI", 136: "White playfield GI"}


def lamps(validated: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "candidate"
	items = []
	for address in range(1, 81):
		label = LAMPS.get(address, f"Unused lamp {address}")
		availability = "used" if address in LAMPS else "unused"
		sources = (MANUAL_SOURCE, VPX_SOURCE) if validated and availability == "used" else (MANUAL_SOURCE,)
		items.append(output(address, label, "lamp", availability, sources, status, "pinmame.output.lamp", str(address), wiring={"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id=f"lamp.{slug(label)}"))
	for address in range(81, 129):
		entry = RGB_CHANNELS.get(address)
		if entry:
			connector, color, x, y = entry
			label = f"{connector} RGB {color}"
			items.append(output(address, label, "rgb_lamp", "used", (MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE, CORE_SOURCE), status, "pinmame.output.lamp", connector, {"location": f"Playfield VPX position x={x:.2f}, y={y:.2f}", "notes": f"{color} channel of physical {connector} tri-color LED"}, {"board": "520-5331-00 RGB/GI driver board", "control_connection": connector}, f"lamp.{slug(connector)}-{color}"))
		else:
			items.append(output(address, f"Unused RGB driver channel {address}", "lamp", "unused", (MANUAL_SOURCE, CORE_SOURCE, VPX_TABLE_SOURCE), status, "pinmame.output.lamp", output_id=f"lamp.unused-{address}"))
	for address, label in GI_CHANNELS.items():
		items.append(output(address, label, "gi", "used", (MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE, CORE_SOURCE), status, "pinmame.output.lamp", str(address), wiring={"board": "520-5331-00 RGB/GI driver board", "control_connection": label}, output_id=f"gi.{slug(label)}"))
	items.append(output(0, "General illumination aggregate", "gi", "used", (MANUAL_SOURCE, VPX_SOURCE, RUNTIME_SOURCE), status, "pinmame.output.gi", "GI-0", output_id="gi.general-illumination"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance("validated", MANUAL_SOURCE, VPX_SOURCE)}
	if positions:
		result["positions"] = positions
	return result


def mechanisms() -> list[dict[str, object]]:
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-eject", "switch.shooter-lane-jam"], "The proven table creates four balls and initializes switches 18-21 active. Output 1 ejects the ball at switch 21 into the shooter path; switch 22 is the downstream jam opto."),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 launches a ball held at shooter-lane switch 23; the proven script uses power 55."),
		mechanism("mechanism.right-eject", "Right eject scoop", "kicker", ["device.right-eject-scoop"], ["switch.right-eject-scoop"], "Switch 51 stays active while a ball is held. Output 6 ejects at approximately 39.5 degrees with strength 54 in the proven table."),
		mechanism("mechanism.grave-marker", "Motorized grave marker and magnet", "motorized", ["device.grave-marker-magnet", "device.grave-marker-motor"], ["switch.grave-marker-down", "switch.grave-marker-up", "switch.grave-marker-opto"], "Output 20 moves the grave marker between its down switch 33 and up switch 34. Output 3 controls the ball magnet and switch 52 senses the captured ball. Output 19 is the marker's primary visual flasher.", [{"id": "position.down", "label": "Down", "sensors": ["switch.grave-marker-down"]}, {"id": "position.up", "label": "Up", "sensors": ["switch.grave-marker-up"]}]),
		mechanism("mechanism.electric-chair", "Electric Chair and Sparky step-up", "motorized", ["device.electric-chair-magnet", "device.electric-chair-step-up-driver"], ["switch.electric-chair-standup", "switch.electric-chair-opto"], "Output 4 holds a ball at electric-chair opto 53. Output 18 drives the Sparky head/step-up animation; standup switch 35 reports a direct hit."),
		mechanism("mechanism.captive-ball-hammer", "Hammer and captive ball", "toy", ["device.hammer"], ["switch.captive-ball"], "Output 53 swings the hammer through its unsensed stroke. Impacts on the captive-ball assembly pulse switch 42; the mechanism has no controller-facing hammer-position sensor."),
		mechanism("mechanism.drop-bank", "Three-bank drop targets", "drop_target_bank", ["device.drop-targets-reset"], ["switch.drop-target-bottom", "switch.drop-target-middle", "switch.drop-target-top"], "The three targets begin raised. Ball impact drops targets and asserts switches 60-62; output 54 raises the complete bank."),
		mechanism("mechanism.loop-post", "Loop up post", "gate", ["device.loop-up-post"], [], "Output 55 raises the loop post while enabled and releases it when disabled. The official auxiliary-board table and proven VPW callback agree; there is no controller-facing position switch.", [{"id": "position.down", "label": "Down", "sensors": []}, {"id": "position.up", "label": "Up", "sensors": []}]),
		mechanism("mechanism.coffin-lock", "Three-ball coffin lock", "gate", ["device.coffin-lock-release"], ["switch.coffin-opto-1-bottom", "switch.coffin-opto-2-middle", "switch.coffin-opto-3-top"], "Coffin optos 57-59 track the bottom, middle, and top lock positions. Output 51 retracts the lock post to release stored balls."),
		mechanism("mechanism.coffin-magnet", "Coffin magnet processor", "toy", ["device.coffin-magnet-down", "device.coffin-processor-d0-mode-bit", "device.coffin-processor-d1-mode-bit"], ["switch.coffin-magnet-ball-detect", "switch.coffin-magnet-down"], "Output 52 lowers the magnet and asserts position switch 64. Processor outputs 57/58 are D0/D1: 00 is off, 10 is detect/hold for up to 10 seconds, 11 is detect with a 250 ms cadence, and 01 is a full-power centered grab for up to 1 second. Detection is reported on switch 63 only in detect/hold or detect mode.", [{"id": "position.raised", "label": "Raised", "sensors": []}, {"id": "position.down", "label": "Down", "sensors": ["switch.coffin-magnet-down"]}]),
		mechanism("mechanism.snake", "Snake jaw, latch, and eject", "motorized", ["device.snake-eject", "device.snake-jaw-latch-release", "device.snake-jaw-close"], ["switch.snake-eject", "switch.snake-jaw-open", "switch.snake-latch"], "Switch 54 holds the snake ball and output 5 ejects it. Output 12 releases the jaw latch and the proven script reports jaw-open switch 55; output 56 closes the jaw, with switch 56 pulsing at the latch contact.", [{"id": "position.closed", "label": "Closed and latched", "sensors": ["switch.snake-latch"]}, {"id": "position.open", "label": "Open", "sensors": ["switch.snake-jaw-open"]}]),
		mechanism("mechanism.flippers", "Two lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "Outputs 15/16 drive the left/right flippers from buttons 84/82 with normally-closed EOS contacts 83/81."),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Switches 30/31/32 pulse outputs 9/10/11 respectively."),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26/27 pulse outputs 13/14."),
	]


def relationships() -> list[dict[str, object]]:
	pairs = [
		("switch.left-pop-bumper", "device.left-pop-bumper"), ("switch.right-pop-bumper", "device.right-pop-bumper"),
		("switch.bottom-pop-bumper", "device.bottom-pop-bumper"), ("switch.left-slingshot", "device.left-slingshot"),
		("switch.right-slingshot", "device.right-slingshot"), ("switch.left-flipper-button", "device.left-flipper"),
		("switch.right-flipper-button", "device.right-flipper"),
	]
	return [{"id": f"relationship.{slug(source)}-to-{slug(destination)}", "kind": "pulse" if "pop-bumper" in source or "slingshot" in source else "direct", "source": source, "destination": destination, "provenance": provenance("validated", MANUAL_SOURCE, VPX_SOURCE)} for source, destination in pairs]


PREMIUM_DRIVER_IDS = {"mtl_113h", "mtl_116h", "mtl_120h", "mtl_122h", "mtl_150h", "mtl_151h", "mtl_160h", "mtl_163h", "mtl_164h", "mtl_164hc", "mtl_170h", "mtl_170hc", "mtl_180h", "mtl_180hc"}


def driver_records(premium: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		if (driver_id in PREMIUM_DRIVER_IDS) != premium:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		edition = "Premium/LE" if premium else "Pro"
		record["variant_notes"] = f"Colored-ROM variant; physical {edition} playfield I/O is unchanged." if driver_id.endswith("c") else f"Firmware revision within the physical {edition} edition; playfield I/O and mechanisms are unchanged."
		selected.append(record)
	return sorted(selected, key=lambda item: item["id"])


def sources(include_validated_evidence: bool) -> list[dict[str, object]]:
	result = [
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/10/MTLAB1-compressed.pdf", "sha256": "f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090", "locator": "MTLAB1-compressed.pdf: wiring PDF pages 42-50; Premium switches, lamps, coils, and assemblies PDF pages 103-110; Pro service tables PDF pages 119-129", "license": "NOASSERTION", "attribution": "Stern Pinball", "source_id": "stern", "original_filename": "MTLAB1-compressed.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Metallica INITGAME, 520-5326-01 auxiliary board, 520-6801-00 magnet processor, 520-5331-00 RGB/GI node board, public custom-output routing, and DMD configuration", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames Metallica driver family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	]
	result[0]["excerpts"] = METALLICA_EXCERPTS
	if include_validated_evidence:
		result.extend([
			{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Metallica%20Premium%20Monsters%20%28Stern%202013%29%20VPW%202.0.2.vbs", "revision": VPX_REVISION, "sha256": "3be5af3f6b05c4f1445c391aab42713bf9e76af87d563bfb061e7bc5daedfd64", "locator": "Lines 404-439, 1091-1130, 1137-1593, 1662-1825, 2145-2301, and 4369-4669: table initialization, callbacks, custom mechanisms, lamps, GI, and switch causality", "license": "NOASSERTION", "attribution": "VPW and table authors credited in the script; vpxtable_scripts contributors"},
			{"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "local-evidence://vpx-table/metallica-premium-monsters-vpw-2.0", "sha256": "afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f", "locator": "Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx; exact AllLamps timer-address bindings and physical RGB object coordinates recovered read-only", "license": "NOASSERTION", "attribution": "VPW and table authors credited by the table", "original_filename": "Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx"},
			{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/mtl_180h/harness/boot-start-premium.json", "revision": PINMAME_REVISION, "sha256": "a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510", "locator": "Exact mtl_180h boot/start scenario with switches 18-21 initialized, coin pulses, and start pulse; ROM archive SHA-256 141018225cdf51421b579b319b925b6dfd6a2fda98471e16998bd648abd86488", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
		])
	return result


def build_premium() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.metallica-premium-limited-edition.2013", "name": "Metallica Premium / Limited Edition", "manufacturer": "Stern", "year": 2013, "ipdb_id": 6031, "opdb_id": "GRBE4-MOE4l"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(True), "inputs": inputs(True), "outputs": coils(True) + lamps(True),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, MANUAL_SOURCE]}}, "provenance": provenance("validated", CORE_SOURCE, VPX_SOURCE, RUNTIME_SOURCE)}],
		"mechanisms": mechanisms(), "relationships": relationships(), "sources": sources(True),
		"knowledge": {"path": "knowledge/stern/metallica-premium-limited-edition-2013.md", "status": "complete"}, "conflicts": [],
	}


PRO_SWITCHES: dict[int, tuple[str, str, bool, tuple[str, ...]]] = {
	1: ("Left return lane right", "leaf", False, ()), 3: ("Fuel lane rollover", "leaf", True, ()),
	4: ("Fuel lane standup", "microswitch", True, ()), 7: ("Fuel standup bottom", "microswitch", True, ()),
	9: ("Fuel standup top", "microswitch", True, ()), 15: ("Tournament start", "button", False, ()),
	16: ("Start", "button", False, ()), 18: ("Trough 4 left", "microswitch", False, ("ball.position",)),
	19: ("Trough 3", "microswitch", False, ("ball.position",)), 20: ("Trough 2", "microswitch", False, ("ball.position",)),
	21: ("Trough 1 right eject", "microswitch", False, ("ball.position",)), 22: ("Shooter lane jam", "opto", False, ("ball.position",)),
	23: ("Shooter lane", "microswitch", False, ("ball.position",)), 24: ("Left outlane", "leaf", True, ()),
	25: ("Left return lane left", "leaf", True, ()), 26: ("Left slingshot", "leaf", True, ()),
	27: ("Right slingshot", "leaf", True, ()), 28: ("Right return lane", "leaf", True, ()),
	29: ("Right outlane", "leaf", True, ()), 30: ("Left pop bumper", "leaf", True, ()),
	31: ("Right pop bumper", "leaf", True, ()), 32: ("Bottom pop bumper", "leaf", True, ()),
	35: ("Electric chair standup", "microswitch", True, ()), 36: ("Grave lane standup left", "microswitch", True, ()),
	37: ("Grave lane standup right", "microswitch", True, ()), 40: ("Right ramp standup left", "microswitch", True, ()),
	41: ("Right ramp standup right", "microswitch", True, ()), 42: ("Captive ball", "leaf", True, ()),
	43: ("Left loop", "leaf", True, ()), 44: ("Left top lane", "leaf", True, ()),
	45: ("Right top lane", "leaf", True, ()), 46: ("Right loop", "leaf", True, ()),
	47: ("Right ramp exit", "opto", True, ()), 50: ("Left ramp exit", "opto", True, ()),
	51: ("Right eject scoop", "microswitch", False, ("ball.loaded",)), 52: ("Grave marker opto", "opto", False, ("ball.loaded",)),
	53: ("Electric chair opto", "opto", False, ("ball.loaded",)), 54: ("Snake eject", "microswitch", False, ("ball.loaded",)),
	60: ("Drop target bottom", "microswitch", False, ("position.down",)), 61: ("Drop target middle", "microswitch", False, ("position.down",)),
	62: ("Drop target top", "microswitch", False, ("position.down",)),
}


def pro_matrix_switch(number: int) -> dict[str, object]:
	spec = PRO_SWITCHES.get(number)
	used = spec is not None
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": number in (60, 61, 62), "pulse": bool(spec[2]) if spec else False,
		"availability": "used" if used else "unused", "physical": {"switch_type": spec[1] if spec else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance("validated", MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE),
	}
	if spec and spec[3]:
		result["roles"] = list(spec[3])
	return result


def pro_inputs() -> list[dict[str, object]]:
	items = [pro_matrix_switch(number) for number in range(1, 65)]
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
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
		items.append({
			"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": device},
			"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"), "normally_closed": normally_closed,
			"pulse": False, "availability": availability, "physical": {"switch_type": switch_type},
			"provenance": provenance("validated", MANUAL_SOURCE, PRO_VPX_SOURCE, CORE_SOURCE),
		})
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance("validated", MANUAL_SOURCE, CORE_SOURCE)})
	return items


PRO_MAIN_COILS = {
	1: ("Trough up-kicker", "coil", "used"), 2: ("Auto launch", "coil", "used"), 3: ("Grave marker magnet", "magnet", "used"),
	4: ("Electric chair magnet", "magnet", "used"), 5: ("Snake eject", "coil", "used"), 6: ("Right eject scoop", "coil", "used"),
	7: ("Loop up post diverter", "coil", "used"), 8: ("Shaker motor", "motor", "optional"),
	9: ("Left pop bumper", "coil", "used"), 10: ("Right pop bumper", "coil", "used"), 11: ("Bottom pop bumper", "coil", "used"),
	12: ("Drop targets reset", "coil", "used"), 13: ("Left slingshot", "coil", "used"), 14: ("Right slingshot", "coil", "used"),
	15: ("Left flipper", "coil", "used"), 16: ("Right flipper", "coil", "used"), 17: ("Unused main output 17", "coil", "unused"),
	18: ("Electric chair step-up driver", "coil", "used"), 19: ("Grave marker flasher", "flasher", "used"),
	20: ("Snake flasher", "flasher", "used"), 21: ("Back panel left flasher", "flasher", "used"),
	22: ("Back panel right flasher", "flasher", "used"), 23: ("Left ramp flasher", "flasher", "used"),
	24: ("Coin meter", "coil", "optional"), 25: ("Pop bumper flasher", "flasher", "used"),
	26: ("Grave marker double flasher", "flasher", "used"), 27: ("Electric chair double flasher", "flasher", "used"),
	28: ("Electric chair spot double flasher", "flasher", "used"), 29: ("Right ramp flasher", "flasher", "used"),
	30: ("Captive ball flasher", "flasher", "used"), 31: ("Coffin insert double flasher", "flasher", "used"),
	32: ("Electric chair insert flasher", "flasher", "used"), 33: ("Ticket dispenser advance", "coil", "optional"),
	34: ("Ticket dispenser meter", "coil", "optional"), 35: ("Ticket dispenser switched ground", "relay", "optional"),
}


PRO_LAMPS = {
	1: "Start button", 2: "Tournament button", 4: "Shoot Again", 5: "Guitar Pick James", 6: "Guitar Pick Lars",
	7: "Guitar Pick Kirk", 8: "Guitar Pick Robert", 9: "Snake end-of-line", 10: "Coffin end-of-line",
	11: "Electric Chair end-of-line", 12: "Grave Marker end-of-line", 13: "Fuel progress E", 14: "Fuel progress 1/4",
	15: "Fuel progress 1/2", 16: "Fuel progress 3/4", 17: "Fuel progress F", 18: "Left outlane",
	19: "Left return lane left", 20: "Left return lane right", 21: "Fuel lane 1", 22: "Fuel lane 2",
	23: "Fuel lane 3", 24: "Fuel lane arrow", 25: "Right outlane", 26: "Right return lane", 27: "Mystery",
	29: "Right loop Grave Marker", 30: "Right ramp Grave Marker", 31: "Right ramp Snake", 32: "Right loop Snake",
	33: "Right loop Electric Chair", 34: "Right ramp Electric Chair", 35: "Right ramp standup right", 36: "Right loop arrow",
	37: "Right ramp arrow", 38: "Right ramp standup left", 40: "Grave lane Grave Marker", 41: "Grave lane Snake",
	42: "FUEL letter F", 43: "FUEL letter U", 44: "FUEL letter E", 45: "FUEL letter L",
	46: "Grave lane Electric Chair", 47: "Left loop Grave Marker", 48: "Left loop Snake", 49: "Grave lane standup left",
	50: "Grave lane arrow", 51: "Grave lane standup right", 52: "Left ramp Grave Marker", 53: "Left ramp Snake",
	54: "Left ramp Electric Chair", 55: "Left ramp arrow", 56: "Electric Chair", 57: "Left loop Electric Chair",
	58: "Left loop arrow", 60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper",
	63: "Left top lane", 64: "Right top lane", 65: "Snake", 67: "Coffin 1 bottom", 68: "Coffin 2 middle",
	69: "Coffin 3 top", 70: "Extra Ball", 71: "Crank It Up", 73: "Electric Chair 1 left",
	75: "Electric Chair 2 center", 78: "Electric Chair 3 right",
}


def pro_outputs() -> list[dict[str, object]]:
	items = []
	for address, (label, kind, availability) in PRO_MAIN_COILS.items():
		if address in {33, 34, 35}:
			items.append(output(address, label, kind, availability, (MANUAL_SOURCE,), "validated", "physical.output.ticket", str(address), physical={"notes": "Optional physical ticket-dispenser service function; not a stable LibPinMAME solenoid address."}))
		else:
			items.append(output(address, label, kind, availability, (MANUAL_SOURCE, PRO_VPX_SOURCE), "validated", manual_address=str(address), wiring={"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": MAIN_CONTROL[address - 1]}))
	items.append(output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, PRO_RUNTIME_SOURCE), "validated", physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	for address in range(1, 81):
		label = PRO_LAMPS.get(address, f"Unused lamp {address}")
		availability = "used" if address in PRO_LAMPS else "unused"
		items.append(output(address, label, "lamp", availability, (MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE), "validated", "pinmame.output.lamp", str(address), wiring={"board": "I/O Power Driver board lamp matrix", "control_connection": f"matrix-{address}"}, output_id=f"lamp.{slug(label)}"))
	items.append(output(0, "General illumination aggregate", "gi", "used", (MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE), "validated", "pinmame.output.gi", "GI-0", output_id="gi.general-illumination"))
	return items


def pro_mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str) -> dict[str, object]:
	return {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance("validated", MANUAL_SOURCE, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE)}


def pro_mechanisms() -> list[dict[str, object]]:
	return [
		pro_mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-eject", "switch.shooter-lane-jam"], "Create four balls with switches 18-21 occupied. Output 1 ejects from the right end and the working script pulses downstream jam switch 22 as the ball enters the shooter path."),
		pro_mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 drives the impulse plunger. The proven table uses power 62, a 0.6 second full-plunge time, and 0.3 random variation; switch 23 is the shooter-lane sensor."),
		pro_mechanism("mechanism.right-eject", "Right eject scoop", "kicker", ["device.right-eject-scoop"], ["switch.right-eject-scoop"], "Switch 51 holds the ball. Output 6 ejects at table angle 220 with strength 25 and force variation 2 in the working script."),
		pro_mechanism("mechanism.grave-marker-magnet", "Static grave-marker magnet", "toy", ["device.grave-marker-magnet"], ["switch.grave-marker-opto"], "Unlike Premium/LE, the Pro grave marker does not move. Output 3 enables the static magnet with working-table strength 70 and centered capture; opto 52 confirms ball presence behind the inline drop targets."),
		pro_mechanism("mechanism.electric-chair", "Electric Chair and Sparky", "toy", ["device.electric-chair-magnet", "device.electric-chair-step-up-driver"], ["switch.electric-chair-standup", "switch.electric-chair-opto"], "Output 4 drives the chair magnet with working-table strength 45 and centered capture. Switch 53 detects the captured ball, switch 35 is the standup, and output 18 shakes/steps up the Sparky head assembly."),
		pro_mechanism("mechanism.captive-ball", "Passive captive ball", "other", [], ["switch.captive-ball"], "The Pro uses one physically captive ball and switch 42. It has no Premium/LE hammer coil; impacts alone close the switch."),
		pro_mechanism("mechanism.drop-bank", "Three inline grave-marker drop targets", "drop_target_bank", ["device.drop-targets-reset"], ["switch.drop-target-bottom", "switch.drop-target-middle", "switch.drop-target-top"], "Switches 60-62 are active while their targets are raised and open when hit. Output 12 resets all three targets together."),
		pro_mechanism("mechanism.loop-post", "Loop up-post diverter", "diverter", ["device.loop-up-post-diverter"], [], "Output 7 raises the post while energized and drops it when disabled. There is no position switch."),
		pro_mechanism("mechanism.snake", "Static snake-head eject", "kicker", ["device.snake-eject"], ["switch.snake-eject"], "The Pro head has no motorized jaw or latch. A ball rests at switch 54 and output 5 ejects it at table angle 195 with strength 26 and angle/force variation 2."),
		pro_mechanism("mechanism.flippers", "Two lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "Dedicated button/EOS pairs D9-D12 drive outputs 15 and 16 through SAM fast flips."),
		pro_mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", ["device.left-pop-bumper", "device.right-pop-bumper", "device.bottom-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.bottom-pop-bumper"], "Switches 30-32 pulse their matching outputs 9-11."),
		pro_mechanism("mechanism.slingshots", "Left and right slingshots", "other", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26/27 pulse outputs 13/14."),
		pro_mechanism("mechanism.optional-shaker", "Optional shaker motor", "toy", ["device.shaker-motor"], [], "Output 8 drives the optional cabinet shaker; omit the physical device only when recreating a cabinet without that factory option."),
		pro_mechanism("mechanism.optional-ticket-dispenser", "Optional ticket dispenser", "other", ["device.ticket-dispenser-advance", "device.ticket-dispenser-meter", "device.ticket-dispenser-switched-ground"], ["switch.ticket-notch"], "Optional redemption hardware uses physical service identities 33 to advance tickets, 34 as the meter, and 35 as switched ground, with dedicated switch D19 (public -5) for the ticket notch. These physical functions use the untransported physical.output.ticket group because LibPinMAME solenoid 33 is the synthetic SAM game-on state."),
	]


def pro_relationships() -> list[dict[str, object]]:
	pairs = [
		("switch.left-pop-bumper", "device.left-pop-bumper"), ("switch.right-pop-bumper", "device.right-pop-bumper"),
		("switch.bottom-pop-bumper", "device.bottom-pop-bumper"), ("switch.left-slingshot", "device.left-slingshot"),
		("switch.right-slingshot", "device.right-slingshot"), ("switch.left-flipper-button", "device.left-flipper"),
		("switch.right-flipper-button", "device.right-flipper"),
	]
	return [{"id": f"relationship.{slug(source)}-to-{slug(destination)}", "kind": "pulse" if "pop-bumper" in source or "slingshot" in source else "direct", "source": source, "destination": destination, "provenance": provenance("validated", MANUAL_SOURCE, PRO_VPX_SOURCE)} for source, destination in pairs]


def pro_sources() -> list[dict[str, object]]:
	result = sources(False)
	for source in result:
		if source["id"] == CORE_SOURCE:
			source["locator"] = "src/wpc/sam.c Metallica SAM generation, public switch/lamp/solenoid groups, DMD configuration, and driver initialization"
	result.extend([
		{"id": PRO_VPX_SOURCE, "kind": "vpx_script", "uri": "https://www.vpforums.org/index.php?app=downloads&showfile=18612", "sha256": "d5ea2810308e05daee22c2a75b3d80a4b19fbd3f89e67144a38f9c20bdb33307", "locator": "JP's Metallica Pro (Stern 2013) v600.vbs lines 35, 81-165, and 200-453: exact mtl_180 game binding, four-ball initialization, magnets, callbacks, GI, switches, drop targets, and mechanism causality", "license": "NOASSERTION", "attribution": "JPSalas and table contributors credited on the VPForums file page", "original_filename": "JP's Metallica Pro (Stern 2013) v600.vbs", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"},
		{"id": PRO_VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "https://www.vpforums.org/index.php?app=downloads&showfile=18612", "sha256": "837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118", "locator": "JP's Metallica Pro (Stern 2013) v600.vpx from archive SHA-256 5fafb136ed9f76ad32dcc035bd72c4dadd856562778f9fae53d7e1bcc9396ff0; known-working Pro layout and physical-object evidence", "license": "NOASSERTION", "attribution": "JPSalas and table contributors credited on the VPForums file page", "original_filename": "JP's Metallica Pro (Stern 2013) v600.vpx", "rights": "NOASSERTION", "acquired_at": "2026-08-02T00:00:00Z"},
		{"id": PRO_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/mtl_170/harness/boot-start-pro.json", "revision": PINMAME_REVISION, "sha256": "65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e", "locator": "Family-compatible mtl_170 Pro boot/start scenario with switches 18-21 initialized, coin pulses, and start pulse; ROM archive SHA-256 2f11830ffb35f2a80258e47a5ea0abd17fc2350995bb1d1d1a165480be61f654", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
	])
	return result


def build_pro() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.metallica-pro.2013", "name": "Metallica Pro", "manufacturer": "Stern", "year": 2013, "ipdb_id": 6028, "opdb_id": "GRBE4-MQK1Z"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(False), "inputs": pro_inputs(), "outputs": pro_outputs(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, MANUAL_SOURCE]}}, "provenance": provenance("validated", CORE_SOURCE, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE)}],
		"mechanisms": pro_mechanisms(), "relationships": pro_relationships(), "sources": pro_sources(),
		"knowledge": {"path": "knowledge/stern/metallica-pro-2013.md", "status": "complete"}, "conflicts": [],
	}


PREMIUM_KNOWLEDGE = """# Metallica Premium / Limited Edition (Stern, 2013)

Coverage: **author-ready - complete physical inventory, public PinMAME bindings, custom mechanisms, and recreation behavior validated**

## Identity and evidence precedence

This definition covers the `mtl_*h` and `mtl_*hc` firmware family used by the Premium and Limited Edition playfields. Non-`h` drivers are the different Pro playfield and remain in a conspicuous partial record. The known-working `Metallica Premium Monsters (Stern 2013) VPW 2.0.2.vbs` is ground truth for controller callbacks, initial state, mechanism causality, timing, and active behavior. The official Stern manual governs physical inventory, wiring, assemblies, and service numbering. Pinned PinMAME source governs public custom-output serialization, board topology, DMD transport, and driver identity. The exact local VPX table resolves the final RGB connector-to-public-address mapping that cannot be recovered from lamp object names in the external script alone.

## Controller topology

Metallica uses the Stern SAM CPU/Sound and I/O Power Driver boards, a 520-5326-01 six-transistor auxiliary board exposed as public solenoids 51-56, a 520-6801-00 coffin-magnet processor whose two public mode bits are 57/58, and one 520-5331-00 RGB/GI board exposing public lamp channels 81-128. Physical main outputs are 1-32. PinMAME public solenoid 33 is the synthetic SAM game-on state, while optional physical ticket functions retain service identities 33-35 in the untransported `physical.output.ticket` group. The native display is a 128x32 four-bit DMD; exact-ROM runtime observed PinMAME layout type 14.

## Switch corrections and initial state

All matrix positions 1-64, dedicated D1-D24, and DIP inputs are explicit. The manual and working script establish switch 22 as the shooter-lane jam opto and 23 as the shooter lane; the old merged definition had these reversed. Switch 52 is the grave-marker opto and 53 is the electric-chair opto. The proven table creates four trough balls and initializes switches 18, 19, 20, and 21 active. Switch 22 is downstream and starts clear.

## Lamps, RGB connectors, and GI

Standard lamps 1-80 follow the Premium service table; unused matrix addresses are explicit. The RGB/GI board's public addresses are not sequential by physical connector. Exact table timer bindings prove CN4 blue/green/red at 87/88/89, CN5 at 90/91/92, CN9 at 99/100/101, CN11 at 102/103/104, CN13 at 108/109/110, and CN19 at 126/127/128. Every other address from 81 through 128 is an unused controller channel for this playfield. GI uses public lamp addresses 130 red, 132 blue, 134 white upper, and 136 white playfield; group `pinmame.output.gi/0` remains the aggregate compatibility state. Physical RGB-object coordinates were recovered from the exact working table during curation but have not yet been normalized and promoted into the definition.

## Grave marker, electric chair, hammer, and drop bank

The grave marker is a motorized two-position assembly: output 20 moves it between down switch 33 and up switch 34, output 3 controls its ball magnet, and switch 52 is its opto. The electric chair uses magnet output 4, ball opto 53, standup 35, and Sparky step-up output 18. Output 53 swings the hammer without a position sensor; captive-ball impacts pulse switch 42. Drop switches 60-62 start raised and output 54 resets the complete three-bank.

## Coffin lock and magnet processor

Optos 57-59 track three coffin lock positions and output 51 releases the lock post. Output 52 lowers the separate magnet and asserts position switch 64. The processor's public bits are output 57 as D0 and 58 as D1. The proven script defines 00 off, 10 detect/hold at reduced strength for up to 10 seconds, 11 detect on a 250 ms cadence, and 01 full centered grab for up to 1 second. Switch 63 reports ball presence only in detect/hold or detect mode. Preserve those bit combinations and timing; treating outputs 57/58 as ordinary independent coils breaks ball capture.

## Snake, loop post, and standard devices

The snake holds a ball at switch 54 and ejects it with output 5. Output 12 releases the jaw latch and switch 55 reports jaw open; output 56 closes the jaw and switch 56 pulses at the latch contact. Output 55 is the loop up post and has no position switch. Output 6 ejects the right scoop at approximately 39.5 degrees with strength 54, while output 2 auto-launches at power 55. The machine also has two lower flippers, three pop bumpers, two slingshots, two loop spinners, two ramps, fuel-lane targets, and the optional shaker on output 8.

## Recreation checklist

- Construct all physical inputs and outputs, including unused addresses, the six-transistor board, coffin processor, RGB/GI board, cabinet options, and native DMD.
- Initialize four balls on trough switches 18-21; keep shooter-jam 22 clear until a ball enters that path.
- Preserve PWM or sustained behavior for both magnets and preserve the coffin processor's two-bit state machine.
- Model the grave marker's motor limits, electric-chair capture and Sparky step-up, hammer and captive ball, drop bank, loop post, three-position coffin lock, lowering coffin magnet, snake latch/jaw/eject, scoop, auto-launcher, pops, slings, and flippers.
- Bind node LEDs and processor bits to the public JSON addresses; retain connector and service numbers only as physical aliases.
- Use the VPX force, angle, timing, and state transitions as proven authoring baselines, then align geometry to the official assemblies without changing controller causality.

## Sources

- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; wiring PDF pages 42-50 and Premium service tables pages 103-110.
- `vpx.metallica-premium-monsters-vpw-2.0.2`: pinned known-working script, SHA-256 `3be5af3f6b05c4f1445c391aab42713bf9e76af87d563bfb061e7bc5daedfd64`.
- `vpx-table.metallica-premium-monsters-vpw-2.0`: exact local table, SHA-256 `afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f`; used read-only to resolve RGB timer addresses and physical object positions.
- `runtime.metallica-premium.boot-start`: exact `mtl_180h` ROM run, raw SHA-256 `a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510`, ROM archive SHA-256 `141018225cdf51421b579b319b925b6dfd6a2fda98471e16998bd648abd86488`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM implementation, custom-board routing, DMD, and driver configuration.
"""


PRO_KNOWLEDGE = """# Metallica Pro (Stern, 2013)

Coverage: **author-ready - complete physical I/O, mechanisms, variant split, wiring, and recreation behavior validated**

## Identity and evidence precedence

This definition covers all 20 non-`h` Metallica drivers from `mtl_052` through `mtl_180c`. The `h`/`hc` family is the physically different Premium/LE playfield and has its own definition. JP's Metallica Pro 6.0.0 VPX script is the controller-semantics ground truth because it is a current, proven recreation bound to `mtl_180`; the official Stern manual governs physical inventory, wiring, assemblies, and service numbering; pinned PinMAME governs public API address groups, the SAM platform, DMD transport, and driver identity. The table author explicitly states that the Pro layout matches the original; its two added ramp spinners are ornamental, do not score, and must not be recreated as physical Pro switches.

## Edition differences that must be preserved

The Pro has ordinary matrix lamps and aggregate GI only. It has no Premium RGB/GI node board, no three-ball under-playfield coffin lock, no lowering coffin magnet or two-bit coffin processor, no captive-ball hammer, no motorized grave marker, and no motorized snake jaw/latch. Consequently public solenoids 51-58 and public lamp channels 81-136 are not part of this physical edition. The Pro retains four balls, a static grave-marker magnet behind three inline drop targets, an Electric Chair magnet and Sparky step-up driver, a passive captive ball, a static snake-head eject, and an electronically controlled loop up-post.

## Switches and initial state

All 64 matrix addresses, 24 dedicated addresses, and eight CPU-board DIP inputs are explicit, including unused locations. Four balls initially occupy trough switches 18-21. Output 1 ejects the rightmost ball and the proven script pulses shooter-path jam opto 22; switch 23 is the shooter lane. Switch 52 is the grave-marker ball opto, 53 is the Electric Chair opto, 51 is the right eject, and 54 is the snake eject. The inline drop targets use switches 60 bottom, 61 middle, and 62 top; they are active while raised and open when hit. Switches 33/34, 38/39, 55-59, and 63/64 are explicitly unused because their Premium-only moving marker, physical spinners, motorized jaw, and coffin hardware are absent.

## Coils, flashers, lamps, and GI

The Pro I/O Power Driver board exposes physical outputs 1-32. Outputs 1-18 cover trough, auto launch, both magnets, both ejects, loop post, optional shaker, pops, drop-bank reset, slings, flippers, one unused address, and the Sparky step-up driver. Outputs 19-32 are the service-manual flashers and 24 is the optional coin meter. PinMAME public solenoid 33 is the synthetic SAM game-on state, not ticket hardware. Optional ticket-dispenser advance, meter, and switched-ground service identities 33-35 are preserved separately under `physical.output.ticket`, because the stable LibPinMAME API does not transport them. There is no auxiliary-board public range 51-58. Standard lamps 1-80 exactly follow the Pro matrix on manual PDF page 122, with every blank address marked unused. The only PinMAME GI binding is aggregate `pinmame.output.gi/0`; the working script switches the whole ordinary-GI collection together and has no colored GI.

## Grave marker, chair, captive ball, and drop bank

The grave marker is static on Pro. Output 3 drives its centered magnet at working-table strength 70, switch 52 detects the ball, and switches 60-62 sit on the three inline drop targets leading into the capture area. Output 12 resets the bank. The Electric Chair uses magnet output 4 at working-table strength 45, opto 53, standup 35, and output 18 to shake/step up Sparky. The captive ball is passive: its impacts pulse switch 42 and there is no hammer output.

## Ejects, post, and standard devices

The right scoop holds a ball at switch 51 and output 6 ejects at VPX angle 220, strength 25, and force variation 2. The static snake mouth holds a ball at switch 54 and output 5 ejects at angle 195, strength 26, and angle/force variation 2; it deliberately has no jaw-open or latch sensor. Output 7 raises the loop post while energized and drops it when disabled, with no position sensor. Output 2 drives the auto launcher at VPX power 62 with 0.6 second full-plunge time and 0.3 random variation. The remaining playfield includes two lower flippers, three pop bumpers, two slingshots, two ramps, fuel standups, guitar-pick standups, and ordinary rollover/target switches. Do not add scoring loop spinners merely because JP's VPX includes two decorative non-scoring spinner objects.

## Optional cabinet hardware

Output 8 is the optional shaker and output 24 is the optional coin meter. The optional ticket dispenser uses physical service identities 33 for advance, 34 for its meter, and 35 for switched ground, plus dedicated switch D19 (public switch -5) for ticket-notch feedback. Retain those `physical.output.ticket` bindings even when a specific recreation omits the option; do not bind its advance line to PinMAME solenoid 33, which is game-on.

## Recreation checklist

- Create four trough balls on switches 18-21, keep switch 22 clear downstream, and bind shooter lane 23.
- Build the static grave-marker magnet and three normally-closed inline drop targets, the Electric Chair magnet/Sparky toy, passive captive ball, static snake eject, right scoop, auto launcher, and unsensed loop up-post with the documented causality.
- Implement public physical outputs 1-32, virtual game-on 33, matrix lamps 1-80, aggregate GI 0, the 128x32 DMD, all dedicated cabinet inputs, and optional shaker/coin/ticket hardware; the ticket service functions are physical identities without a stable LibPinMAME transport.
- Do not copy Premium-only outputs 51-58, RGB/GI lamp channels, coffin mechanisms, hammer, moving grave marker, motorized snake jaw, or loop-spinner scoring switches.
- Use the working VPX strengths, angles, timing, and state transitions as initial authoring values and the manual's service drawings for physical placement and wiring.

## Sources

- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; Pro service tables on PDF pages 119-129.
- `vpx.metallica-pro-jps-6.0.0`: extracted known-working `mtl_180` script, SHA-256 `d5ea2810308e05daee22c2a75b3d80a4b19fbd3f89e67144a38f9c20bdb33307`; callbacks and mechanisms on lines 35, 81-165, and 200-453.
- `vpx-table.metallica-pro-jps-6.0.0`: VPForums table, SHA-256 `837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118`; downloaded archive SHA-256 `5fafb136ed9f76ad32dcc035bd72c4dadd856562778f9fae53d7e1bcc9396ff0`.
- `runtime.metallica-pro.boot-start`: family-compatible `mtl_170` ROM run, raw SHA-256 `65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e`, ROM archive SHA-256 `2f11830ffb35f2a80258e47a5ea0abd17fc2350995bb1d1d1a165480be61f654`.
- `pinmame.core.4ec52ff0ac13`: pinned SAM platform, display, and driver configuration.
"""


def runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"machine_ids": ["stern.metallica-premium-limited-edition.2013"], "driver_ids": ["mtl_180h"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": "mtl_180h", "rom_archive_sha256": "141018225cdf51421b579b319b925b6dfd6a2fda98471e16998bd648abd86488",
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game mtl_180h --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>",
			"raw_runs": [{"name": "boot-start", "sha256": "a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510", "self_test_pulses": 0}],
			"observations": {
				"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "gi_addresses_seen": [0],
				"solenoid_addresses_seen": [20],
				"lamp_addresses_seen": [17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 77, 78, 79, 80, 87, 88, 89, 90, 91, 92, 99, 100, 101, 102, 103, 104, 108, 109, 110, 126, 127, 128, 130, 132, 134, 136],
			},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/mtl_180h/harness", "sha256": "a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510", "quality": "validated", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def pro_runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"machine_ids": ["stern.metallica-pro.2013"], "driver_ids": ["mtl_170"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": "mtl_170", "rom_archive_sha256": "2f11830ffb35f2a80258e47a5ea0abd17fc2350995bb1d1d1a165480be61f654",
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game mtl_170 --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>",
			"raw_runs": [{"name": "boot-start", "sha256": "65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e", "self_test_pulses": 0}],
			"observations": {
				"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "gi_addresses_seen": [0],
				"solenoid_addresses_seen": [24],
				"lamp_addresses_seen": [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 67, 68, 69, 70, 71, 73, 75, 78],
			},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/mtl_170/harness", "sha256": "65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e", "quality": "validated", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def write_json(path: Path, value: dict[str, object]) -> None:
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json_file(path, value)


def main() -> None:
	for stale in (
		ROOT / "machines/partial/stern/metallica-premium-2013.json",
		ROOT / "machines/partial/stern/metallica-pro-2013.json",
		ROOT / "knowledge/stern/metallica-premium-2013.md",
	):
		if stale.exists():
			stale.unlink()
	premium_machine_id = "stern.metallica-premium-limited-edition.2013"
	if premium_machine_id in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		write_json(ROOT / "machines/partial/stern/metallica-premium-limited-edition-2013.json", build_premium())
		write_text(ROOT / "knowledge/stern/metallica-premium-limited-edition-2013.md", fail_closed_spatial_knowledge(premium_machine_id, PREMIUM_KNOWLEDGE))
	pro_machine_id = "stern.metallica-pro.2013"
	if pro_machine_id in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		write_json(ROOT / "machines/partial/stern/metallica-pro-2013.json", build_pro())
		write_text(ROOT / "knowledge/stern/metallica-pro-2013.md", fail_closed_spatial_knowledge(pro_machine_id, PRO_KNOWLEDGE))
	write_json(ROOT / "evidence/runtime/sam/metallica-premium-boot-start.json", runtime_evidence())
	write_json(ROOT / "evidence/runtime/sam/metallica-pro-boot-start.json", pro_runtime_evidence())


if __name__ == "__main__":
	main()
