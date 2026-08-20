"""Build reviewed, author-ready Avatar Pro and Limited Edition definitions."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/avatar-limited-edition-2010.json"
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("avr_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
MANUAL_SOURCE = "manual.avatar-pro-le.2010"
EXCERPT_ROOT = ROOT / "evidence/excerpts/stern.avatar-pro-limited-edition.2010"
VPX_SOURCE = "vpx.avatar-pro-lw-vpumod-1.12"
VPX_TABLE_SOURCE = "vpx-table.avatar-pro.vpuniverse-4755"
PRO_ROM_SOURCE = "rom.avatar-pro.avr-200"
LE_ROM_SOURCE = "rom.avatar-le.avr-120h"
PRO_IPDB_SOURCE = "ipdb.avatar-pro.5618"
LE_IPDB_SOURCE = "ipdb.avatar-limited-edition.5653"
LE_DUMP_SOURCE = "service.avatar-le.real-machine-dmd-1.2"
LE_DETECTOR_SOURCE = "human-review.avatar-le-ceramic-detector"
PRO_RUNTIME_SOURCE = "runtime.avatar-pro.boot-start"
LE_RUNTIME_SOURCE = "runtime.avatar-le.boot-start"
TRANSPORTER_DOWN_SOURCE = "diagnostic.avatar-le.transporter-up-to-down"
TRANSPORTER_UP_SOURCE = "diagnostic.avatar-le.transporter-down-to-up"
AMP_SUIT_SOURCE = "diagnostic.avatar-le.amp-suit-motor"
AMP_BANK_SOURCE = "diagnostic.avatar-le.three-bank-motor"


def avatar_manual_source() -> dict[str, object]:
	base = {
		"id": MANUAL_SOURCE,
		"kind": "manual",
		"uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/Avatar-Manual.pdf",
		"sha256": "afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b",
		"locator": "Official 55-page scanned Stern service manual; assemblies/gameplay pages 4-32, Pro coil chart PDF page 36, Q1-Q32 board wiring 37-38, GI 39, switch matrix 40, lamp matrix 41, cabinet wiring 42, and flippers 43. Page 41 explicitly labels J13 as eight lamp-column drives and J12 as ten lamp returns.",
		"license": "NOASSERTION",
		"attribution": "Stern Pinball, Inc.",
		"source_id": "official-stern",
		"original_filename": "Avatar-Manual.pdf",
		"rights": "NOASSERTION",
		"acquired_at": "2026-08-03T00:42:02.303917Z",
	}
	entries = [
		("coil-chart", "excerpt.avatar-pro-le.coil-chart", "PDF page 36, COILS DETAILED CHART TABLE", "Avatar-Manual.pdf page 36, crop box 0.04,0.05,0.92,0.86, scanned page rendered at its native resolution (embedded image xref 164, 2613px across 8.65in), rendered at 82 dpi, capped to 600px wide, grayscale, 601x782 WebP quality 28"),
		("q1-q32-wiring", "excerpt.avatar-pro-le.q1-q32-wiring", "PDF page 37, Backbox I/O Power Driver Board Detailed Wiring Diagram", "Avatar-Manual.pdf page 37, crop box 0.05,0.04,0.56,0.94, scanned page rendered at its native resolution (embedded image xref 168, 2496px across 8.26in), rendered at 190 dpi, capped to 800px wide, grayscale, 801x1999 WebP quality 30"),
		("backbox-board-layout", "excerpt.avatar-pro-le.backbox-board-layout", "PDF page 38, Backbox Wiring", "Avatar-Manual.pdf page 38, crop box 0.04,0.04,0.96,0.92, scanned page rendered at its native resolution (embedded image xref 173, 3532px across 11.70in), rendered at 93 dpi, capped to 1000px wide, grayscale, 1001x677 WebP quality 35"),
		("gi-wiring", "excerpt.avatar-pro-le.gi-wiring", "PDF page 39, General Illumination Circuit Detailed Wiring Diagram", "Avatar-Manual.pdf page 39, crop box 0.04,0.04,0.96,0.93, scanned page rendered at its native resolution (embedded image xref 178, 2496px across 8.26in), rendered at 99 dpi, capped to 750px wide, grayscale, 751x1027 WebP quality 28"),
		("switch-matrix", "excerpt.avatar-pro-le.switch-matrix", "PDF page 40, Playfield Switch Wiring Diagram", "Avatar-Manual.pdf page 40, crop box 0.05,0.06,0.95,0.91, scanned page rendered at its native resolution (embedded image xref 183, 3532px across 11.70in), rendered at 105 dpi, capped to 1100px wide, grayscale, 1101x735 WebP quality 40"),
		("lamp-matrix", "excerpt.avatar-pro-le.lamp-matrix", "PDF page 41, Playfield Lamp Wiring Diagram", "Avatar-Manual.pdf page 41, crop box 0.04,0.05,0.95,0.92, scanned page rendered at its native resolution (embedded image xref 188, 3536px across 11.71in), rendered at 103 dpi, capped to 1100px wide, grayscale, 1101x744 WebP quality 40"),
		("cabinet-wiring", "excerpt.avatar-pro-le.cabinet-wiring", "PDF page 42, Cabinet and Coin Door Wiring", "Avatar-Manual.pdf page 42, crop box 0.04,0.04,0.96,0.93, scanned page rendered at its native resolution (embedded image xref 193, 2502px across 8.28in), rendered at 118 dpi, capped to 900px wide, grayscale, 901x1233 WebP quality 35"),
		("flipper-wiring", "excerpt.avatar-pro-le.flipper-wiring", "PDF page 43, Flipper Circuit Wiring Diagram", "Avatar-Manual.pdf page 43, crop box 0.04,0.04,0.96,0.93, scanned page rendered at its native resolution (embedded image xref 198, 2496px across 8.26in), rendered at 105 dpi, capped to 800px wide, grayscale, 801x1096 WebP quality 30"),
	]
	excerpts = []
	for stem, excerpt_id, locator, derivation in entries:
		markdown = EXCERPT_ROOT / f"{stem}.md"
		image = EXCERPT_ROOT / f"{stem}.webp"
		if not markdown.is_file() or not image.is_file():
			raise FileNotFoundError(f"Avatar manual excerpt is missing: {markdown} or {image}")
		excerpts.append({
			"id": excerpt_id,
			"locator": locator,
			"path": str(markdown.relative_to(ROOT)).replace("\\", "/"),
			"sha256": hashlib.sha256(markdown.read_bytes()).hexdigest(),
			"image": str(image.relative_to(ROOT)).replace("\\", "/"),
			"image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
			"image_derivation": derivation,
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		})
	base["excerpts"] = excerpts
	return base


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


# label, switch type, pulse, normally closed, roles
COMMON_SWITCHES: dict[int, tuple[str, str, bool, bool, tuple[str, ...]]] = {
	1: ("Left return lane R", "leaf", True, False, ()),
	2: ("NAVI N target", "microswitch", True, False, ()), 3: ("NAVI A target", "microswitch", True, False, ()),
	4: ("NAVI V target", "microswitch", True, False, ()), 5: ("NAVI I target", "microswitch", True, False, ()),
	7: ("Right two-bank bottom target", "microswitch", True, False, ()), 8: ("Right two-bank top target", "microswitch", True, False, ()),
	9: ("Left orbit spinner", "other", True, False, ()), 10: ("Left orbit", "leaf", True, False, ()),
	11: ("Left top lane", "leaf", True, False, ()), 12: ("Center top lane", "leaf", True, False, ()), 13: ("Right top lane", "leaf", True, False, ()),
	14: ("Link lockup", "microswitch", False, False, ("ball.position",)),
	15: ("Tournament start", "button", False, False, ("cabinet.tournament-start",)), 16: ("Start", "button", False, False, ("cabinet.start",)),
	17: ("Center target", "microswitch", True, False, ()),
	18: ("Trough 4", "microswitch", False, False, ("ball.position",)), 19: ("Trough 3", "microswitch", False, False, ("ball.position",)),
	20: ("Trough 2", "microswitch", False, False, ("ball.position",)), 21: ("Trough 1", "microswitch", False, False, ("ball.position",)),
	22: ("Trough jam", "opto", False, False, ("ball.position",)), 23: ("Shooter lane", "microswitch", False, False, ("ball.position",)),
	24: ("Left outlane", "leaf", True, False, ()), 25: ("Left return lane L", "leaf", True, False, ()),
	26: ("Left slingshot", "leaf", True, False, ()), 27: ("Right slingshot", "leaf", True, False, ()),
	28: ("Right return lane", "leaf", True, False, ()), 29: ("Right outlane", "leaf", True, False, ()),
	30: ("Left pop bumper", "leaf", True, False, ()), 31: ("Right pop bumper", "leaf", True, False, ()), 32: ("Bottom pop bumper", "leaf", True, False, ()),
	35: ("Right orbit", "leaf", True, False, ()), 36: ("Center AMP target", "microswitch", True, False, ()),
	37: ("Left AMP target", "microswitch", True, False, ()), 38: ("Right AMP target", "microswitch", True, False, ()),
	39: ("Captive ball", "leaf", True, True, ()), 40: ("Right orbit spinner", "other", True, False, ()),
	42: ("AMP three-bank left target", "microswitch", True, False, ()), 43: ("AMP three-bank center target", "microswitch", True, False, ()),
	44: ("AMP three-bank right target", "microswitch", True, False, ()), 45: ("AMP three-bank down", "microswitch", False, False, ("position.down",)),
	46: ("AMP three-bank up", "microswitch", False, False, ("position.up",)),
	52: ("Left ramp exit", "microswitch", True, False, ()), 57: ("AMP suit motor down", "microswitch", False, False, ("position.down",)),
	58: ("AMP suit motor up", "microswitch", False, False, ("position.up",)),
}
LE_SWITCHES: dict[int, tuple[str, str, bool, bool, tuple[str, ...]]] = {
	41: ("Left ramp entrance", "microswitch", True, False, ()),
	47: ("Transporter down", "microswitch", False, False, ("position.down",)),
	48: ("Transporter up", "microswitch", False, False, ("position.up",)),
}


def switch_specs(limited_edition: bool) -> dict[int, tuple[str, str, bool, bool, tuple[str, ...]]]:
	return COMMON_SWITCHES | (LE_SWITCHES if limited_edition else {})


def switch_id(number: int, limited_edition: bool) -> str:
	spec = switch_specs(limited_edition).get(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int, limited_edition: bool) -> dict[str, object]:
	spec = switch_specs(limited_edition).get(number)
	used = spec is not None
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	rom_source = LE_ROM_SOURCE if limited_edition else PRO_ROM_SOURCE
	if limited_edition and number in LE_SWITCHES:
		sources = (rom_source, LE_DUMP_SOURCE) + ((TRANSPORTER_DOWN_SOURCE, TRANSPORTER_UP_SOURCE) if number in {47, 48} else ())
	else:
		sources = (MANUAL_SOURCE, rom_source, VPX_SOURCE) if used else (MANUAL_SOURCE, rom_source)
	result: dict[str, object] = {
		"id": switch_id(number, limited_edition), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": spec[3] if spec else False, "pulse": spec[2] if spec else False, "availability": "used" if used else "unused",
		"physical": {"switch_type": spec[1] if spec else "unknown"},
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(*sources),
	}
	if spec and spec[4]:
		result["roles"] = list(spec[4])
	if number == 39:
		result["physical"]["notes"] = "The proven VPX script treats the captive-ball contact as inverted/normally closed. Preserve this polarity when binding the physical hit."
	if not limited_edition and number in {41, 47, 48}:
		result["physical"]["notes"] = "The exact avr_200 localized switch table marks this address NOT USED; it is installed only on the Limited Edition playfield."
	return result


DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin chute", "Center coin chute", "Right coin chute", "Fourth coin chute", "Fifth coin chute", "Unused dedicated switch D6", "Unused dedicated switch D7", "Alternate shooter-lane metal detector",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Unused dedicated switch D13", "Unused dedicated switch D14", "Unused dedicated switch D15", "Unused dedicated switch D16",
	"Pendulum tilt", "Slam tilt", "Ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "button", "button", "unknown", "unknown", "other", "button", "leaf", "button", "leaf", "unknown", "unknown", "unknown", "unknown", "tilt", "tilt", "microswitch", "unknown", "button", "button", "button", "button"]
DEDICATED_ROLES = {
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth",
	84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos",
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}


def dedicated_id(manual_number: int, limited_edition: bool) -> str:
	label = DEDICATED_LABELS[manual_number - 1]
	if manual_number == 8 and not limited_edition:
		label = "Unused dedicated switch D8"
	return f"switch.d{manual_number}-{slug(label)}"


def dedicated_switch(manual_number: int, limited_edition: bool) -> dict[str, object]:
	index = manual_number - 1
	device = DEDICATED_DEVICES[index]
	label = DEDICATED_LABELS[index]
	availability = "used"
	if manual_number in {4, 5, 19}:
		availability = "optional"
	elif manual_number in {6, 7, 13, 14, 15, 16, 20} or (manual_number == 8 and not limited_edition):
		availability = "unused"
	if manual_number == 8 and not limited_edition:
		label = "Unused dedicated switch D8"
	rom_source = LE_ROM_SOURCE if limited_edition else PRO_ROM_SOURCE
	sources = [rom_source, CORE_SOURCE]
	if manual_number == 8 and limited_edition:
		sources.extend([LE_DUMP_SOURCE, LE_DETECTOR_SOURCE])
	result: dict[str, object] = {
		"id": dedicated_id(manual_number, limited_edition), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device}, "aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": manual_number in {10, 12, 18}, "pulse": manual_number in {1, 2, 3, 4, 5}, "availability": availability,
		"physical": {"switch_type": DEDICATED_TYPES[index] if availability != "unused" else "unknown"}, "provenance": provenance(*sources),
	}
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	if manual_number == 8 and limited_edition:
		result["physical"]["notes"] = "Two metal rails at the bottom of the shooter lane form a normally-open conductivity detector. A steel ball bridges the rails and closes public switch 72; the ceramic Na'vi ball does not, allowing the ROM to identify it and start double scoring."
	return result


def inputs(limited_edition: bool) -> list[dict[str, object]]:
	items = [matrix_switch(number, limited_edition) for number in range(1, 65)]
	items.extend(dedicated_switch(number, limited_edition) for number in range(1, 25))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance(MANUAL_SOURCE, CORE_SOURCE)})
	return items


# label, output kind, edition-only state (common/limited/optional-pro/optional)
COILS: dict[int, tuple[str, str, str]] = {
	1: ("Trough up-kicker", "coil", "common"), 2: ("Auto launch", "coil", "common"), 3: ("AMP suit magnet", "magnet", "common"),
	4: ("AMP suit right marching leg", "coil", "limited"), 5: ("AMP three-bank motor relay", "relay", "common"), 6: ("Link lockup up", "coil", "common"),
	7: ("Link lockup latch", "coil", "common"), 8: ("Shaker motor", "motor", "optional-pro"), 9: ("Left pop bumper", "coil", "common"),
	10: ("Right pop bumper", "coil", "common"), 11: ("Bottom pop bumper", "coil", "common"), 12: ("AMP suit left marching leg", "coil", "limited"),
	13: ("AMP suit motor direction relay", "relay", "common"), 14: ("Transporter motor reversing relay", "relay", "limited"),
	15: ("Left flipper", "coil", "common"), 16: ("Right flipper", "coil", "common"), 17: ("Left slingshot", "coil", "common"),
	18: ("Right slingshot", "coil", "common"), 19: ("AMP suit motor", "motor", "common"), 20: ("Link flasher", "flasher", "common"),
	21: ("Backpanel flashers x2", "flasher", "common"), 22: ("Link left flasher", "flasher", "common"), 23: ("Link right flasher", "flasher", "common"),
	24: ("Optional coil or coin meter", "coil", "optional"), 25: ("Pop bumper flasher", "flasher", "common"), 26: ("AMP multiball flasher", "flasher", "common"),
	27: ("Bottom arch flashers x2", "flasher", "limited"), 28: ("AMP suit flashers x2", "flasher", "common"), 29: ("Left side flasher", "flasher", "common"),
	30: ("Left blue flasher", "flasher", "common"), 31: ("Right blue flasher", "flasher", "common"), 32: ("Right side flasher", "flasher", "common"),
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLU", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output_id(address: int) -> str:
	return f"device.{address}-{slug(COILS[address][0])}"


def coil_wiring(address: int) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address in {4, 12, 14, 27}:
		return wiring
	if address == 8:
		wiring.update({"power_wire": "RED-WHT", "power_connection": "J17-P7", "nominal_voltage_v": 16, "voltage_type": "ac"})
	elif address in {5, 13}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address in {17, 18, 19}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address in {15, 16}:
		wiring.update({"power_wire": "50 V flipper feed", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4-8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	elif address <= 16:
		wiring.update({"power_wire": "VIO-YEL" if address == 3 else "YEL-VIO", "power_connection": "J10-P8" if address == 3 else "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	else:
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


def main_outputs(limited_edition: bool) -> list[dict[str, object]]:
	rom_source = LE_ROM_SOURCE if limited_edition else PRO_ROM_SOURCE
	items: list[dict[str, object]] = []
	for address, (label, kind, edition) in COILS.items():
		availability = "used"
		if edition == "limited" and not limited_edition:
			availability = "unused"
		elif edition == "optional-pro":
			availability = "used" if limited_edition else "optional"
		elif edition == "optional":
			availability = "optional"
		physical: dict[str, object] | None = None
		if edition == "limited" and not limited_edition:
			physical = {"notes": "The exact avr_200 service table labels this Q channel by number only; the named device is installed only on Limited Edition hardware. The common board schematic proves the Q transistor/control pin, but the Pro coil chart leaves the power feed blank because no device is installed."}
		elif edition == "limited":
			physical = {"notes": "The exact LE ROM and real-machine diagnostic name the installed device. The common scanned manual documents only the Pro configuration and leaves this channel's power feed blank, so the definition preserves the proven Q transistor/control pin without inventing an LE power wire or voltage."}
		elif address == 8:
			physical = {"notes": "Optional on Pro; factory-included shaker on Limited Edition."}
		elif address == 21:
			physical = {"quantity": 2, "notes": "Two physical backpanel flasher bulbs; cabinet/backpanel-only and outside normalized playfield space."}
		elif address == 24:
			physical = {"notes": "Service-chart optional channel for a coil or 5 V accounting meter; preserve it as optional rather than inventing a playfield device."}
		if edition == "limited" and limited_edition:
			sources = (rom_source, LE_DUMP_SOURCE, LE_IPDB_SOURCE, CORE_SOURCE) + ((TRANSPORTER_DOWN_SOURCE, TRANSPORTER_UP_SOURCE) if address == 14 else ())
		else:
			sources = (MANUAL_SOURCE, rom_source, CORE_SOURCE)
		if availability == "used" and edition != "limited":
			sources += (VPX_SOURCE,)
		items.append(make_output(address, label, kind, availability, sources, manual_address=str(address), physical=physical, wiring=coil_wiring(address), stable_id=output_id(address)))
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	items.append(make_output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, runtime_source), physical={"notes": "Synthetic SAM fast-flip game-on output. It has no physical Q33 device; public addresses 34-36 are legacy query aliases and are not separate outputs."}, stable_id="virtual.game-on"))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused SAM auxiliary compatibility address {address}", "virtual", "unused", (CORE_SOURCE, rom_source), physical={"notes": "Avatar is declared with SAM_GAME_AUXSOL12, but exact ROM diagnostics and physical evidence show no installed auxiliary controlled devices. Public 51-66 remain explicit emulator capacity, including decoder gaps."}, stable_id=f"virtual.aux-{address}"))
	return items


LAMPS = {
	1: "Start button", 2: "Tournament start button", 3: "Shoot Again", 4: "Grace", 5: "Tsu'tey", 6: "Mo'at", 7: "Eytukan", 8: "Neytiri", 9: "Jake",
	10: "NAVI I", 11: "NAVI V", 12: "NAVI A", 13: "NAVI N", 14: "Right outlane", 15: "Right return lane", 16: "Right two-bank arrow",
	17: "Left return lane R", 18: "Left return lane L", 19: "Left outlane", 20: "1X", 21: "Right two-bank bottom target", 22: "Right two-bank top target", 23: "Extra Ball", 24: "Navi",
	25: "Unused lamp 25", 26: "Left four-bank arrow", 27: "AMP suit X", 28: "Captive ball X", 29: "Link X", 30: "AMP suit arrow", 31: "Captive ball arrow", 32: "Right orbit X",
	33: "Right loop arrow", 34: "Eywa", 35: "AMP P", 36: "AMP M", 37: "AMP A", 38: "Link arrow", 39: "Left orbit X", 40: "Left ramp X", 41: "Left ramp arrow", 42: "Left loop arrow",
	43: "Link", 44: "2X", 45: "4X", 46: "8X", 47: "Left ramp Banshee", 48: "Light Unobtanium", 49: "Center target arrow", 50: "Center target X", 51: "AMP suit arrow top",
	52: "Special", 53: "AMP Multiball", 54: "Left top lane", 55: "Center top lane", 56: "Right top lane", 57: "Banshee", 58: "Link", 59: "AMP", 60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper", 63: "Valkyrie", 64: "Seeds",
}
LAMP_DRIVE = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
PRO_LAMPS_SEEN = [1] + list(range(3, 25)) + list(range(26, 65))
LE_LAMPS_SEEN = [1] + list(range(3, 25)) + list(range(26, 65))


def lamps(limited_edition: bool) -> list[dict[str, object]]:
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	rom_source = LE_ROM_SOURCE if limited_edition else PRO_ROM_SOURCE
	pro_unused = {20, 25, 44, 45, 46} | set(range(65, 81))
	le_unused = {25} | set(range(65, 81))
	unused = le_unused if limited_edition else pro_unused
	items: list[dict[str, object]] = []
	for address in range(1, 81):
		label = LAMPS.get(address, f"Unused lamp matrix address {address}")
		availability = "unused" if address in unused else "used"
		column = (address - 1) % 8
		row = (address - 1) // 8
		physical = None
		if not limited_edition and address in {20, 44, 45, 46}:
			physical = {"notes": "The localized ROM retains this named scoring address, but the proven Pro VPX script omits the physical insert. IPDB records these formerly unused lamps as working on Limited Edition."}
		items.append(make_output(address, label, "lamp", availability, (MANUAL_SOURCE, rom_source, runtime_source), group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring={"board": "I/O Power Driver board lamp matrix", "drive_wire": LAMP_DRIVE[column][0], "drive_connection": LAMP_DRIVE[column][1], "return_wire": LAMP_RETURN[row][0], "return_connection": LAMP_RETURN[row][1]}, stable_id=f"lamp.{address}-{slug(label)}"))
	items.append(make_output(0, "General illumination master", "gi", "used", (MANUAL_SOURCE, VPX_SOURCE, runtime_source), group="pinmame.output.gi", manual_address="GI-0", physical={"notes": "PinMAME exposes the machine's general illumination as master GI channel 0."}, stable_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions is not None:
		result["positions"] = positions
	return result


def mechanisms(limited_edition: bool) -> list[dict[str, object]]:
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	common_sources = (MANUAL_SOURCE, VPX_SOURCE, runtime_source)
	bank_diagnostic = " Exact LE service evidence starts at switch 46, finishes with output 5 active, and captures the DMD text MOVING TO SWITCH #45." if limited_edition else ""
	suit_diagnostic = " Exact LE service evidence starts at switch 58, finishes with outputs 13 and 19 active, and captures the DMD text MOVING TO SWITCH #57." if limited_edition else ""
	items = [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", [output_id(1)], [switch_id(n, limited_edition) for n in range(18, 23)], "Four balls initialize on occupancy switches 18-21. Output 1 ejects the rightmost ball through jam opto 22 toward shooter switch 23. Keep each ball's identity and occupancy through drains and ejections.", common_sources),
		mechanism("mechanism.auto-launch", "Manual shooter with auto launcher", "kicker", [output_id(2)], [switch_id(23, limited_edition)], "The machine retains a manual plunger. Output 2 also launches a ball resting on shooter-lane switch 23 when the ROM requests an automatic serve.", common_sources),
		mechanism("mechanism.amp-magnet", "AMP suit magnet", "other", [output_id(3)], [], "Output 3 energizes the magnet near the AMP suit. The proven table uses a non-centering magnet, so magnetic force influences a nearby steel ball without teleporting it to the magnet center.", common_sources),
		mechanism("mechanism.amp-three-bank", "Motorized AMP three-target bank", "motorized", [output_id(5)], [switch_id(n, limited_edition) for n in (42, 43, 44, 45, 46)], "Targets 42-44 move together. Switch 46 is fully raised and switch 45 fully lowered. The proven table moves from Z 25 to -24 in 25 steps and disables target collision while down." + bank_diagnostic, common_sources + ((AMP_BANK_SOURCE,) if limited_edition else ()), [{"id": "position.up", "label": "Raised and hittable", "sensors": [switch_id(46, limited_edition)]}, {"id": "position.down", "label": "Lowered", "sensors": [switch_id(45, limited_edition)]}]),
		mechanism("mechanism.link-lock", "Link lockup lift and latch", "other", [output_id(6), output_id(7)], [switch_id(14, limited_edition)], "Switch 14 reports a ball at the Link lock. Output 6 raises the lock pins and output 7 releases or drops the latch. Recreate the physical barriers and ball retention; the associated Jake/Link cover animation is cosmetic.", common_sources),
		mechanism("mechanism.amp-suit", "Motorized AMP suit", "motorized", [output_id(13), output_id(19)], [switch_id(57, limited_edition), switch_id(58, limited_edition)], "Output 19 powers the suit motor and relay 13 selects direction. Switch 57 is the down endpoint and 58 the up endpoint." + suit_diagnostic, common_sources + ((AMP_SUIT_SOURCE,) if limited_edition else ()), [{"id": "position.up", "label": "Suit raised", "sensors": [switch_id(58, limited_edition)]}, {"id": "position.down", "label": "Suit lowered", "sensors": [switch_id(57, limited_edition)]}]),
		mechanism("mechanism.captive-ball", "Captive ball", "toy", [], [switch_id(39, limited_edition)], "One captive ball travels within its constrained lane and pulses normally-closed switch 39 on impact. The proven table creates one captive ball, not two.", common_sources),
		mechanism("mechanism.flippers", "Lower flippers", "other", [output_id(15), output_id(16)], [dedicated_id(n, limited_edition) for n in (9, 10, 11, 12)], "Outputs 15/16 drive the left/right flippers. Dedicated public pairs 84/83 and 82/81 are the cabinet button and normally-closed EOS contacts respectively.", common_sources),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [output_id(9), output_id(10), output_id(11)], [switch_id(n, limited_edition) for n in (30, 31, 32)], "The left, right, and bottom pop bumpers use output/switch pairs 9/30, 10/31, and 11/32. Each switch hit drives the corresponding physical kick ring through ROM control.", common_sources),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [output_id(17), output_id(18)], [switch_id(26, limited_edition), switch_id(27, limited_edition)], "Left and right slingshots use output/switch pairs 17/26 and 18/27.", common_sources),
		mechanism("mechanism.shaker", "Shaker motor", "toy", [output_id(8)], [], "Output 8 drives the 16 VAC shaker. It is optional on Pro and factory-included on Limited Edition.", (MANUAL_SOURCE, LE_IPDB_SOURCE if limited_edition else PRO_IPDB_SOURCE)),
	]
	if limited_edition:
		items.extend([
			mechanism("mechanism.amp-marching-legs", "AMP suit marching legs", "toy", [output_id(4), output_id(12)], [], "Outputs 4 and 12 independently pulse the right and left AMP suit legs. The two unsensed actuators create the advertised physical marching motion; recreate phase-coordinated alternating leg movement while treating exact cadence as author tuning because no proven LE VPX script captures it.", (LE_IPDB_SOURCE, LE_ROM_SOURCE, LE_DUMP_SOURCE)),
			mechanism("mechanism.transporter", "Motorized transporter pod", "motorized", [output_id(14)], [switch_id(47, True), switch_id(48, True)], "A single motor is polarity-reversed by output 14. Switch 47 is fully down and 48 fully up. Exact endpoint-initialized tests finish with output 14 inactive from 48/up and active from 47/down, establishing opposite relay states for travel toward 47/down and 48/up respectively. Endpoint switches stop travel; there is no second public motor output.", (LE_ROM_SOURCE, LE_DUMP_SOURCE, TRANSPORTER_DOWN_SOURCE, TRANSPORTER_UP_SOURCE), [{"id": "position.down", "label": "Pod down", "sensors": [switch_id(47, True)]}, {"id": "position.up", "label": "Pod up", "sensors": [switch_id(48, True)]}]),
			mechanism("mechanism.ceramic-ball", "Ceramic Na'vi ball identification", "other", [], [dedicated_id(8, True), switch_id(21, True), switch_id(23, True)], "The four-ball set contains three steel balls and one ceramic Na'vi ball. The shooter-lane rails close D8/public 72 for steel and remain open for ceramic; the ROM uses the ceramic result to start Na'vi double scoring. Preserve per-ball material identity through trough and drain handling so magnet and detector behavior remain coherent.", (LE_IPDB_SOURCE, LE_DUMP_SOURCE, LE_DETECTOR_SOURCE)),
		])
	return items


LE_DRIVER_IDS = {driver_id for driver_id, driver in DRIVERS.items() if "Limited Edition" in driver["description"]}
PRO_DRIVER_IDS = set(DRIVERS) - LE_DRIVER_IDS
if LE_DRIVER_IDS != {"avr_101h", "avr_120h"} or PRO_DRIVER_IDS != {"avr_106", "avr_110", "avr_200"}:
	raise ValueError("Avatar drivers must classify exhaustively as Pro or Limited Edition")


def driver_records(limited_edition: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id in LE_DRIVER_IDS if limited_edition else PRO_DRIVER_IDS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision for the Limited Edition physical playfield." if limited_edition else "Firmware revision for the Pro physical playfield; the PinMAME LE clone-tree root records software lineage only."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(limited_edition: bool) -> list[dict[str, object]]:
	rom_source = LE_ROM_SOURCE if limited_edition else PRO_ROM_SOURCE
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	rom_hash = "264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269" if limited_edition else "576f70929705761a78a0272a6fb72cd17656e0feb75cccb904a4080e7e5b9bd7"
	raw_hash = "6d00f26380ed4c71b7a921a38fe241bf3a675e472be884c742ee35ac4e8f99e8" if limited_edition else "d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7"
	game = "avr_120h" if limited_edition else "avr_200"
	ipdb_source = LE_IPDB_SOURCE if limited_edition else PRO_IPDB_SOURCE
	ipdb_id = 5653 if limited_edition else 5618
	table_source = {"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "https://vpuniverse.com/files/file/4755-avatar-pro-real-mod-10-neo/", "sha256": "8ddff84ad8f5c8c6f583153f058458ed17bdd6fbafe60304fa2621920872590e", "locator": "Authenticated VPU exact Pro table archive; extracted Avatar (Stern 2010).vpx SHA-256 1838f6fc52c3599dd57382999a2ff7200e38cf741f658c479037b614c51d307a and embedded script SHA-256 0fa91c9232c2eca200c1598c759bd7b1dee742ccc63fb0de87105a062de4b4bd", "attribution": "VPU upload and table authors credited on the linked page"}
	if not limited_edition:
		table_source.update({"known_working": False, "locator": "Authenticated VPU exact Pro geometry candidate; extracted Avatar (Stern 2010).vpx SHA-256 1838f6fc52c3599dd57382999a2ff7200e38cf741f658c479037b614c51d307a and embedded script SHA-256 0fa91c9232c2eca200c1598c759bd7b1dee742ccc63fb0de87105a062de4b4bd, byte-distinct from known-working semantic script SHA-256 8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29; geometry confirmation only"})
	result = [
		avatar_manual_source(),
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Avatar%20%28Stern%202012%29%20v1.12%20LW_VPUMod.vbs", "revision": VPX_REVISION, "sha256": "8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29", "locator": "Known-working exact avr_200 Pro script: switch callbacks, inverted captive-ball contact, lamps/GI, four-ball trough, magnet, AMP bank motion, suit motor, Link lock, and playfield collision causality", "license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors"},
		table_source,
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Avatar INITGAME/driver family, SAM_GAME_AUXSOL12 transport, SAM public switch translation, synthetic game-on output, and 128x32 DMD", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames avr_ driver records and clone graph", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": rom_source, "kind": "rom_static_analysis", "uri": f"external:vpinmame-roms/{game}.zip", "revision": PINMAME_REVISION, "sha256": rom_hash, "locator": f"Exact {game} localized service strings: full 64-switch, D1-D24, 80-lamp, and Q1-Q32 tables; ROM bytes remain external", "license": "NOASSERTION", "attribution": "Analyzed locally from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": ipdb_source, "kind": "human_review", "uri": f"https://www.ipdb.org/machine.cgi?id={ipdb_id}", "locator": f"Physical identity, release record, and edition inventory for IPDB {ipdb_id}", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T00:00:00Z"},
		{"id": runtime_source, "kind": "runtime_scenario", "uri": f"external:pinmame-game-code/avatar-{'limited-edition' if limited_edition else 'pro'}/harness/boot-start-v2/run.json", "revision": PINMAME_REVISION, "sha256": raw_hash, "locator": f"Exact {game} boot/start scenario with the four-ball trough and common mechanism endpoints initialized, four coin pulses, start, 128x32x4 DMD artifacts, GI/lamp transitions, and callback-tracked game-on 33; the independently captured Pro and LE traces happen to observe the same lamp-address set; ROM archive SHA-256 {rom_hash}", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]
	if limited_edition:
		result.extend([
			{"id": LE_DUMP_SOURCE, "kind": "service_diagnostic", "uri": "https://vpuniverse.com/files/file/14088-avatar-premium-le-120-stern-2010/", "sha256": "9ed7b04692e5891305ae17f6f1685a2a95901b26bf987328e4d6769eafffc85b", "locator": "Authenticated real-machine Avatar Premium/LE 1.2 DMD diagnostic dump; decoded diagnostic stream SHA-256 d5334e30dc52cd989aee65188e47f514c09e87384b635d2b442fdce57481b7cf proves LE switch/output names", "license": "NOASSERTION", "attribution": "VPU uploader and the real-machine dump author credited on the linked page"},
			{"id": LE_DETECTOR_SOURCE, "kind": "human_review", "uri": "https://pinside.com/pinball/forum/topic/avatar-rolling-stones-le-ceramic-ball-detection-issue-?tu=CrazyLevi", "locator": "Owner/service discussion identifies the two metal prongs at the bottom of the shooter lane as the metal-ball detector: steel bridges them, ceramic does not, and ceramic starts double scoring", "license": "NOASSERTION", "attribution": "Pinside contributors", "acquired_at": "2026-08-03T00:00:00Z"},
			{"id": TRANSPORTER_DOWN_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/avatar-limited-edition/harness/service-nav-11/run.json", "revision": PINMAME_REVISION, "sha256": "77ba0cab5d2cfa5c77b5e205d65a091dcdc9f5bdcddcd2886a75ff08dbb1c7dc", "locator": "Exact avr_120h service test from switch 48/up toward switch 47/down; output 14 deasserts and DMD reports the target endpoint", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
			{"id": TRANSPORTER_UP_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/avatar-limited-edition/harness/service-nav-12/run.json", "revision": PINMAME_REVISION, "sha256": "761ba656664c40c8fe7f71c1203142c6b50a452a416bfa48dcf614edc546b628", "locator": "Exact avr_120h service test from switch 47/down toward switch 48/up; output 14 asserts and DMD reports the target endpoint", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
			{"id": AMP_SUIT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/avatar-limited-edition/harness/amp-suit-motor-test/run.json", "revision": PINMAME_REVISION, "sha256": "0dc74feaa609f588691138a9907d5261615fccbb334ed8d77a724a240c126881", "locator": "Exact avr_120h service test identifies switches 58/57 and asserts direction relay 13 plus motor 19 while moving from up toward down", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
			{"id": AMP_BANK_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/avatar-limited-edition/harness/three-bank-motor-test/run.json", "revision": PINMAME_REVISION, "sha256": "b5e62835a39af924b757d9f2cac6f73312c149c668699f5882ca1ea932cf901a", "locator": "Exact avr_120h service test identifies switches 46/45 and asserts output 5 while moving from raised toward lowered", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME; ROM bytes remain external"},
		])
	return result


def build(limited_edition: bool) -> dict[str, object]:
	machine_id = "stern.avatar-limited-edition.2010" if limited_edition else "stern.avatar-pro.2010"
	name = "Avatar Limited Edition" if limited_edition else "Avatar Pro"
	runtime_source = LE_RUNTIME_SOURCE if limited_edition else PRO_RUNTIME_SOURCE
	machine: dict[str, object] = {"id": machine_id, "name": name, "manufacturer": "Stern", "year": 2010, "kind": "physical_pinball", "ipdb_id": 5653 if limited_edition else 5618, "opdb_id": "GrZBr-MyNZz" if limited_edition else "GrZBr-MDbx7"}
	if limited_edition:
		machine["model_number"] = "I-00B6"
	return {
		"format": "pinmame-machine-definition", "schema_version": 1, "machine": machine,
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True}, "drivers": driver_records(limited_edition),
		"inputs": inputs(limited_edition), "outputs": main_outputs(limited_edition) + lamps(limited_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, runtime_source)}],
		"mechanisms": mechanisms(limited_edition), "relationships": [], "sources": sources(limited_edition),
		"knowledge": {"path": f"knowledge/stern/avatar-{'limited-edition' if limited_edition else 'pro'}-2010.md", "status": "complete"}, "conflicts": [],
	}


PRO_KNOWLEDGE = """# Avatar Pro (Stern, 2010)

Coverage: **author-ready - complete physical I/O inventory, PinMAME bindings, wiring, mechanism causality, variant boundary, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `avr_106`, `avr_110`, and `avr_200`, the Pro physical machine identified as IPDB 5618 and released on 2010-08-27. PinMAME roots these drivers under `avr_120h` for software lineage, but that does not add Limited Edition hardware. The exact known-working `avr_200` VPX script is ground truth for public addresses, contact polarity, initial state, ball routing, and shared mechanism causality. The official scanned manual governs Pro/common physical inventory and wiring, the exact ROM service tables govern localized labels, and pinned PinMAME governs SAM transport and display topology.

## Pro versus Limited Edition

The exact `avr_200` service table marks matrix switch 41 and transporter endpoints 47/48 unused. It leaves Q4, Q12, Q14, and Q27 as unnamed coil numbers; the physical Pro omits the marching AMP legs, transporter motor, and bottom-arch flashers installed on LE. Pro also omits physical inserts at lamp addresses 20 and 44-46 even though the localized ROM retains scoring labels. Shaker output 8 is optional on Pro. Do not project the ceramic Na'vi ball, metal detector D8/public 72, motorized transporter pod, marching legs, or LE bottom-arch window onto this machine.

## Ball path and shooter

The trough carries four steel balls on switches 18-21, with jam opto 22 and up-kicker output 1. Shooter switch 23 supports both the manual plunger and auto-launch output 2. Preserve real occupancy and ball identity through drains and ejections. Main travel sensors are left/right orbit 10/35, spinners 9/40, left ramp exit 52, top lanes 11-13, outlanes/returns 24/25/28/29, and left return-lane R input 1.

## Motorized AMP mechanisms

The AMP three-bank contains targets 42-44 and moves as one collision assembly. Switch 46 is fully raised and 45 fully lowered; output 5 changes the motor/relay state. The proven table travels from Z 25 to -24 in 25 steps and removes target collision below the playfield. The AMP suit uses motor output 19 and direction relay 13 with endpoints 57 down and 58 up. Output 3 is a non-centering magnet near the suit. Model moving collision geometry, endpoint transitions, and magnetic force rather than only animating artwork.

## Link lock, captive ball, and standard devices

Switch 14 reports Link lock occupancy. Output 6 raises the lock pins and output 7 controls the retaining latch; preserve the physical barriers even if the Jake/Link cover is animated with them. One captive ball pulses inverted/normally-closed switch 39. Flippers are outputs 15/16 with button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops use output/switch pairs 9/30, 10/31, and 11/32. Slings use 17/26 and 18/27. Fixed targets are NAVI 2-5, right bank 7/8, center 17, AMP standups 36-38, and moving-bank faces 42-44.

## Lamps and controlled devices

Bind Q1-Q32, synthetic game-on 33, explicit unused SAM auxiliary compatibility addresses 51-66, lamp matrix 1-80, GI 0, and the 128x32 four-bit DMD. Manual PDF page 41 proves eight J13 lamp-column drives against ten J12 lamp returns; the JSON records both wires/pins for every address. Q20-23 and Q25-32 are flashers rather than insert lamps. Lamp 25 and 65-80 are unused on both editions; Pro additionally leaves 20 and 44-46 physically unused. Public solenoids 34-36 are a legacy `PinmameGetSolenoid` alias of game-on 33 and must not become physical outputs.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, AMP bank with moving collision targets and both endpoints, motorized suit with direction relay and endpoints, suit magnet, Link lock/latch, one captive ball, flippers, pops, slings, spinners, ramps/orbits, lanes, and fixed targets.
- Initialize switches 18-21, 46, and 58 active. Keep normally-closed captive switch 39 and flipper EOS switches 83/81 electrically correct.
- Bind all explicit JSON inputs and outputs, including unused channels, DIPs, service controls, GI, and DMD. Never turn synthetic or auxiliary compatibility addresses into playfield devices.
- Use the exact working VPX behavior as the runtime tie-breaker and the official manual for construction/wiring when recreating geometry and mechanisms.

## Sources

- `manual.avatar-pro-le.2010`: official 55-page Stern manual, SHA-256 `afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b`; relevant scanned pages are organized in the external manual cache.
- `vpx.avatar-pro-lw-vpumod-1.12`: exact known-working `avr_200` script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29`.
- `rom.avatar-pro.avr-200`: exact localized service tables from ROM archive SHA-256 `576f70929705761a78a0272a6fb72cd17656e0feb75cccb904a4080e7e5b9bd7`; ROM bytes remain external.
- `runtime.avatar-pro.boot-start`: corrected callback-state harness evidence SHA-256 `d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7`.
"""


LE_KNOWLEDGE = """# Avatar Limited Edition (Stern, 2010)

Coverage: **author-ready - complete physical I/O inventory, PinMAME bindings, wiring, custom mechanism causality, variant boundary, and recreation behavior validated**

## Identity and evidence precedence

This definition covers `avr_101h` and `avr_120h`, the 250-unit Limited Edition/Premium physical machine identified as IPDB 5653, model I-00B6, released on 2010-12-02. The exact `avr_120h` ROM service tables and real-machine diagnostic dump establish LE-specific names. The exact known-working Pro VPX script is ground truth for shared controller behavior and mechanisms; no independently proven LE VPX table was found, so LE-only causality is additionally validated through exact-ROM service tests, owner/service documentation, and the physical edition record. The official manual controls common wiring and construction facts.

## Four-ball set and ceramic Na'vi detection

The LE still uses four balls, not five: three steel balls and one ceramic Na'vi ball. Trough switches are 18-21, jam opto 22, up-kicker output 1, and shooter switch 23 with manual plunger plus auto-launch output 2. Two exposed metal rails at the bottom of the shooter lane are dedicated D8/public switch 72. A steel ball bridges and closes them; the nonconductive ceramic ball leaves them open, which tells the ROM to begin Na'vi double scoring. Preserve per-ball material identity through every drain, trough shift, and serve so detector and magnet response remain correct.

## AMP three-bank, suit, magnet, and marching legs

The AMP bank moves targets 42-44 together between switch 46 up and 45 down under output 5. Exact diagnostics show output 5 asserted from 46 while moving toward 45; the proven table supplies the 25-step Z range and collision gating. The AMP suit uses motor 19 plus direction relay 13 between switch 58 up and 57 down. Starting at 58, the exact service test asserts 13 and 19 and reports movement toward 57. Magnet output 3 influences steel balls without centering them. LE adds unsensed right/left marching-leg actuators on outputs 4/12; alternate their pulses so the suit physically walks rather than treating them as lamps.

## Motorized transporter pod

The transporter is a separate LE playfield mechanism, not the Link lock animation. One motor is driven through reversing relay output 14. Switch 47 is down and switch 48 up. Exact `avr_120h` service tests prove both directions: from 48/up, output 14 deasserts while moving toward 47/down; from 47/down, it asserts while moving toward 48/up. Endpoint switches stop travel. Build the pod's moving collision/cover geometry with a single reversible motor path; do not invent a second motor output or an auxiliary-board channel.

## Link lock and shared playfield

Switch 14 reports the Link lock. Output 6 raises its pins and output 7 controls the latch; this ball-retention mechanism is separate from transporter output 14. One captive ball uses inverted/normally-closed switch 39. LE adds left ramp entrance switch 41 before common ramp exit 52. Spinners are 9/40, orbits 10/35, flippers outputs 15/16 with public button/EOS pairs 84/83 and 82/81, pops 9/30, 10/31, 11/32, and slings 17/26, 18/27.

## Lamps, flashers, and controller capacity

LE makes previously unused scoring inserts 20 and 44-46 physical and adds bottom-arch flashers on output 27. Manual PDF page 41 proves eight J13 lamp-column drives against ten J12 lamp returns; the JSON records both wires/pins for every matrix address. Output 8 is the factory-included shaker. Lamp 25 and 65-80 remain unused. Q20-23 and Q25-32 are flashers. The common scanned manual is Pro-only for Q4/Q12/Q14/Q27: its board schematic proves their Q/control pins but its coil chart leaves their power feeds blank, so the definition does not invent LE wire colours or voltages. PinMAME declares `SAM_GAME_AUXSOL12`, but exact diagnostics and physical evidence show no installed Avatar auxiliary controlled devices; public 51-66 are explicit unused emulator capacity. Synthetic game-on 33 has no coil, and legacy public queries 34-36 alias it rather than naming separate devices.

## Author construction checklist

- Build the typed four-ball trough, metal-rail shooter detector, manual/auto shooter, motorized AMP bank and suit, non-centering magnet, alternating marching legs, reversible transporter with both endpoints, Link lock/latch, captive ball, flippers, pops, slings, ramps/orbits, spinners, lanes, targets, shaker, and LE flashers/inserts.
- Initialize switches 18-21, 46, 48, and 58 active. Keep ceramic material identity, switch 39 polarity, EOS polarity, motor endpoint exclusion, and moving collision geometry accurate.
- Bind every matrix/dedicated/DIP input, Q1-Q32, game-on 33, explicit unused auxiliary 51-66, lamp 1-80, GI 0, and the DMD. Do not add a physical aux board or device merely because PinMAME reserves address capacity.
- Use the proven Pro script for shared runtime behavior, exact LE service diagnostics for added mechanism direction/endpoints, and the manual/IPDB records for physical construction boundaries.

## Sources

- `manual.avatar-pro-le.2010`: official Stern manual, SHA-256 `afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b`; organized under the external Avatar manual cache.
- `service.avatar-le.real-machine-dmd-1.2`: authenticated real-machine diagnostic archive SHA-256 `9ed7b04692e5891305ae17f6f1685a2a95901b26bf987328e4d6769eafffc85b`; decoded diagnostic stream SHA-256 `d5334e30dc52cd989aee65188e47f514c09e87384b635d2b442fdce57481b7cf`.
- `rom.avatar-le.avr-120h`: exact LE ROM archive SHA-256 `264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269`; ROM bytes remain external.
- `runtime.avatar-le.boot-start`: corrected callback-state evidence SHA-256 `6d00f26380ed4c71b7a921a38fe241bf3a675e472be884c742ee35ac4e8f99e8`.
- Transporter, suit, and three-bank exact service-test hashes are recorded in the definition sources and mechanism-diagnostic evidence file.
"""


def runtime_evidence(limited_edition: bool) -> dict[str, object]:
	game = "avr_120h" if limited_edition else "avr_200"
	machine_id = "stern.avatar-limited-edition.2010" if limited_edition else "stern.avatar-pro.2010"
	raw_hash = "6d00f26380ed4c71b7a921a38fe241bf3a675e472be884c742ee35ac4e8f99e8" if limited_edition else "d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7"
	rom_hash = "264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269" if limited_edition else "576f70929705761a78a0272a6fb72cd17656e0feb75cccb904a4080e7e5b9bd7"
	initial = "--initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 46 " + ("--initial-switch 48 " if limited_edition else "") + "--initial-switch 58"
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": [machine_id], "driver_ids": [game], "extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": game, "command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir <isolated-state> {initial} --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16:150:2 --dmd-dir <external-dmd-dir> --output <external-json>", "rom_archive_sha256": rom_hash, "raw_runs": [{"name": "boot-start-v2", "sha256": raw_hash, "self_test_pulses": 0}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": LE_LAMPS_SEEN if limited_edition else PRO_LAMPS_SEEN, "solenoid_addresses_seen": [33], "gi_addresses_seen": [0]}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/avatar-{'limited-edition' if limited_edition else 'pro'}/harness/boot-start-v2", "sha256": raw_hash, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
	}


def service_diagnostic_evidence(name: str, raw_folder: str, raw_hash: str, self_test_pulses: int, solenoid_addresses: list[int], command_template: str, snapshot: dict[str, object]) -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1, "machine_ids": ["stern.avatar-limited-edition.2010"], "driver_ids": ["avr_120h"], "extractor": {"id": "libpinmame-service-diagnostic-harness", "version": 1},
		"switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
		"runtime": {"game": "avr_120h", "command_template": command_template, "rom_archive_sha256": "264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269", "raw_runs": [{"name": name, "sha256": raw_hash, "self_test_pulses": self_test_pulses}], "observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "diagnostic_snapshots": [snapshot], "solenoid_addresses_seen": solenoid_addresses}},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/avatar-limited-edition/harness/{raw_folder}/run.json", "sha256": raw_hash, "license": "NOASSERTION", "quality": "validated", "attribution": "Exact-ROM LibPinMAME service test cross-checked against the authenticated real-machine DMD diagnostic dump; ROM and dump bytes remain external"},
	}


def main() -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to regenerate Avatar LE partial state while author-ready artifact exists: {AUTHOR_READY_PATH}")
	# The Pro definition and knowledge are owned by curate_avatar_pro_spatial.py.
	# Keep the newer LE spatial curator in this base regeneration path, but never
	# replace a reviewed Pro partial with the older semantic-only baseline.
	write_json(spatial_partial_path(ROOT / "machines/partial/stern/avatar-limited-edition-2010.json"), fail_closed_spatial_partial(build(True)))
	write_json(ROOT / "evidence/runtime/sam/avatar-pro-boot-start.json", runtime_evidence(False))
	write_json(ROOT / "evidence/runtime/sam/avatar-limited-edition-boot-start.json", runtime_evidence(True))
	common_command = "python tools/run_pinmame_harness.py --library <libpinmame> --game avr_120h --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 46"
	menu_command = " --initial-switch 48 --initial-switch 58 --pulse 0:150:0.3 --pulse 0:150:0.3 --pulse 0:150:0.3 --pulse -1:150:0.2 --pulse -1:150:0.2 --pulse -1:150:0.2 --pulse -1:150:0.2 --pulse 0:150:0.5"
	write_json(ROOT / "evidence/runtime/sam/avatar-limited-edition-transporter-up-to-down.json", service_diagnostic_evidence("transporter-up-to-down", "service-nav-11", "77ba0cab5d2cfa5c77b5e205d65a091dcdc9f5bdcddcd2886a75ff08dbb1c7dc", 10, [14], common_command + menu_command + " --pulse 0:150:1.5 --pulse 0:300:1.0 --observe 1 --dmd-dir <external-dmd-dir> --output <external-json>", {"label": "after pulse 10: switch 0", "display_index": 0, "pixel_sha256": "0f4bc3fc1be9d9bb7d75963335add93106d47e215418c8f9b9724a4087ff3797", "nonzero_pixels": 949, "interpreted_text": "TRANSPORTER MOTOR TEST; #48 - TRANSPORTER (UP); #47 - TRANSPORTER (DN); USE +/- OR SELECT TO TEST. Starting at active endpoint 48/up, the test finishes with output 14 inactive.", "active_solenoid_addresses": []}))
	write_json(ROOT / "evidence/runtime/sam/avatar-limited-edition-transporter-down-to-up.json", service_diagnostic_evidence("transporter-down-to-up", "service-nav-12", "761ba656664c40c8fe7f71c1203142c6b50a452a416bfa48dcf614edc546b628", 10, [14], common_command + menu_command.replace("--initial-switch 48", "--initial-switch 47") + " --pulse 0:150:1.5 --pulse 0:300:1.0 --observe 1 --dmd-dir <external-dmd-dir> --output <external-json>", {"label": "after pulse 10: switch 0", "display_index": 0, "pixel_sha256": "5c14f36a70c48867c1f57d6349f956cdb3f444513c37fe3e4899910f79a29323", "nonzero_pixels": 940, "interpreted_text": "TRANSPORTER MOTOR TEST; #48 - TRANSPORTER (UP); #47 - TRANSPORTER (DN); MOVING TO SWITCH #48. Starting at active endpoint 47/down, the test finishes with output 14 active.", "active_solenoid_addresses": [14]}))
	write_json(ROOT / "evidence/runtime/sam/avatar-limited-edition-amp-suit-motor.json", service_diagnostic_evidence("amp-suit-motor", "amp-suit-motor-test", "0dc74feaa609f588691138a9907d5261615fccbb334ed8d77a724a240c126881", 12, [13, 14, 19], common_command + menu_command + " --pulse -1:150:0.25 --pulse -1:150:0.25 --pulse 0:150:1.5 --pulse 0:300:1.0 --observe 1 --dmd-dir <external-dmd-dir> --output <external-json>", {"label": "after pulse 12: switch 0", "display_index": 0, "pixel_sha256": "0fa290638c0cdd0939e698629612c9579ff1c4ce83653606114066a5ba363363", "nonzero_pixels": 725, "interpreted_text": "AMP SUIT MOTOR TEST; #58; #57; MOVING TO SWITCH #57. Starting at active endpoint 58/up, the test finishes with direction relay 13 and motor 19 active.", "active_solenoid_addresses": [13, 19]}))
	write_json(ROOT / "evidence/runtime/sam/avatar-limited-edition-three-bank-motor.json", service_diagnostic_evidence("three-bank-motor", "three-bank-motor-test", "b5e62835a39af924b757d9f2cac6f73312c149c668699f5882ca1ea932cf901a", 11, [5, 14], common_command + menu_command + " --pulse -1:150:0.25 --pulse 0:150:1.5 --pulse 0:300:1.0 --observe 1 --dmd-dir <external-dmd-dir> --output <external-json>", {"label": "after pulse 11: switch 0", "display_index": 0, "pixel_sha256": "50244361cd9a54cb473f02e3ad5a504c515f234d97a90967fb12363c0988f1ad", "nonzero_pixels": 950, "interpreted_text": "AMP SUIT 3-BANK MOTOR TEST; #46 - 3-BANK MOTOR (UP); #45 - 3-BANK MOTOR (DN); MOVING TO SWITCH #45. Starting at active endpoint 46/up, the test finishes with output 5 active.", "active_solenoid_addresses": [5]}))
	write_text(ROOT / "knowledge/stern/avatar-limited-edition-2010.md", fail_closed_spatial_knowledge("stern.avatar-limited-edition.2010", LE_KNOWLEDGE))
	from curate_avatar_le_spatial import curate
	curate()


if __name__ == "__main__":
	main()
