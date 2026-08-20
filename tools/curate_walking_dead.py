"""Build the reviewed Walking Dead Pro and Premium/LE machine definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_partial, spatial_partial_path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("twd_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
PRO_VPX_REVISION = "bfc4e21042b59e7c6495604166e9219d52c6b813"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
PREMIUM_MANUAL = "manual.walking-dead-premium-le"
PRO_MANUAL = "manual.walking-dead-pro"
VPX_SOURCE = "vpx.walking-dead-premium-le-vpw-day-1.1"
PRO_VPX_SOURCE = "vpx.walking-dead-pro.jp-salas-v5.5.0"
PRO_RUNTIME_SOURCE = "runtime.walking-dead-pro.boot-start"
PREMIUM_ROM_SOURCE = "rom-static.walking-dead-premium-le-output-names"
PREMIUM_BOOT_SOURCE = "runtime.walking-dead-premium-le.boot-start"

WALKING_DEAD_PREMIUM_EXCERPTS = [
	{"id": "excerpt.walking-dead-premium.switch-map", "locator": "Walking Dead pinball Manual.pdf PDF page 10, crop box 0.07,0.08,0.94,0.62; visible Premium/LE lamp and switch inventory rows 1–32.", "path": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/switch-map.md", "sha256": "de1a340d86a2a1152e513db662d31ab7922392da76c8a90ad165cfa962d2dc2b", "image": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/switch-map.webp", "image_sha256": "a6e110447b3a867e4d5d4d1eab9a446833fa142047bb92f2c180246e2a0fe694", "image_derivation": "Walking Dead pinball Manual.pdf page 10, crop box 0.07,0.08,0.94,0.62, born-digital page rendered for legibility (smallest type in region 1.9pt, targeting 11px glyphs), rendered at 81 dpi, capped to 600px wide, grayscale, 601x483 WebP quality 35", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.walking-dead-premium.coil-map", "locator": "Walking Dead pinball Manual.pdf PDF page 14, crop box 0.06,0.08,0.95,0.90; coil-location drawing and typical coil wiring.", "path": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/coil-map.md", "sha256": "2685039fa9bd19b44b86355976c0a37ce8749d74c42a0357ae8509f9d8713250", "image": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/coil-map.webp", "image_sha256": "24caaafac8cc78b48a0852911321b95a873396efe1cdefe0ac51b40fdd7bc17a", "image_derivation": "Walking Dead pinball Manual.pdf page 14, crop box 0.06,0.08,0.95,0.9, scanned page rendered at its native resolution (embedded image xref 59, 1290px across 8.60in), rendered at 93 dpi, capped to 700px wide, grayscale, 701x836 WebP quality 45", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.walking-dead-premium.gi-map", "locator": "Walking Dead pinball Manual.pdf PDF page 135, crop box 0.06,0.08,0.95,0.90, rotated 90° counter-clockwise; GI map and rear-panel socket inset.", "path": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/gi-map.md", "sha256": "307ace916c18d48c98e1de9e22a47c0b69f57aef237dbda93eac610f85bb10d6", "image": "evidence/excerpts/stern.the-walking-dead-premium-limited-edition.2014/gi-map.webp", "image_sha256": "16fe956daf2b1799c481118987690993944c4fc8f9951ed1a7cd301001719da2", "image_derivation": "Walking Dead pinball Manual.pdf page 135, crop box 0.06,0.08,0.95,0.9, born-digital page rendered for legibility (smallest type in region 1.2pt, targeting 11px glyphs), rendered at 93 dpi, capped to 700px wide, grayscale, rotated 90 degrees counter-clockwise, 836x701 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
]

WALKING_DEAD_PRO_EXCERPTS = [
	{"id": "excerpt.walking-dead-pro.switch-map", "locator": "WD-PRO-MAN.pdf PDF page 13, crop box 0.06,0.08,0.95,0.90; switch-location drawing and switch schematics.", "path": "evidence/excerpts/stern.the-walking-dead-pro.2014/switch-map.md", "sha256": "24cff6b5cd977c0ed711c7e663a4371ee82bff675449b9eec597d217d2ecacc0", "image": "evidence/excerpts/stern.the-walking-dead-pro.2014/switch-map.webp", "image_sha256": "66f5f4abae66b9f593079794f9372cf3c89ab9a208539aa66b1923195643eb0c", "image_derivation": "WD-PRO-MAN.pdf page 13, crop box 0.06,0.08,0.95,0.9, scanned page rendered at its native resolution (embedded image xref 55, 2453px across 8.36in), rendered at 93 dpi, capped to 700px wide, grayscale, 701x836 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.walking-dead-pro.coil-map", "locator": "WD-PRO-MAN.pdf PDF page 16, crop box 0.06,0.08,0.95,0.90; coil/flasher location drawing and typical coil wiring.", "path": "evidence/excerpts/stern.the-walking-dead-pro.2014/coil-map.md", "sha256": "5350fd9a93e9f0feb9731b58c017cc78e1b82a30ca8e7ded3a7660ec349bcd82", "image": "evidence/excerpts/stern.the-walking-dead-pro.2014/coil-map.webp", "image_sha256": "c31cc62b195f672bf22496d705d9fe8bbe2d43806b8a9671a1f5673b6d300c18", "image_derivation": "WD-PRO-MAN.pdf page 16, crop box 0.06,0.08,0.95,0.9, scanned page rendered at its native resolution (embedded image xref 68, 2478px across 8.35in), rendered at 93 dpi, capped to 700px wide, grayscale, 701x836 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.walking-dead-pro.lamp-map", "locator": "WD-PRO-MAN.pdf PDF page 19, crop box 0.06,0.08,0.95,0.90; lamp-location drawing and lamp schematics.", "path": "evidence/excerpts/stern.the-walking-dead-pro.2014/lamp-map.md", "sha256": "cca69fafd2bbf7401f46f295eb3a3b72b503f2367a10d68fd97366ab14175acb", "image": "evidence/excerpts/stern.the-walking-dead-pro.2014/lamp-map.webp", "image_sha256": "765338db0948ef2e4d6d08723100aab972c93897a59dcfe9690815d54749a0c1", "image_derivation": "WD-PRO-MAN.pdf page 19, crop box 0.06,0.08,0.95,0.9, scanned page rendered at its native resolution (embedded image xref 85, 2478px across 8.35in), rendered at 93 dpi, capped to 700px wide, grayscale, 701x836 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
]


def slug(value: str) -> str:
	value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
	return value or "unnamed"


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


def matrix_switch(number: int, spec: dict[str, object] | None, sources: tuple[str, ...], status: str) -> dict[str, object]:
	row, column = divmod(number - 1, 16)
	used = spec is not None
	label = str(spec["label"]) if used else f"Unused matrix switch #{number}"
	result: dict[str, object] = {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": bool(spec.get("normally_closed", False)) if used else False,
		"pulse": bool(spec.get("pulse", False)) if used else False,
		"availability": "used" if used else "unused",
		"physical": {"switch_type": str(spec.get("switch_type", "unknown")) if used else "unknown"},
		"wiring": {
			"board": "CPU/Sound board",
			"drive_wire": MATRIX_DRIVE[row][0],
			"drive_connection": MATRIX_DRIVE[row][1],
			"return_wire": MATRIX_RETURN[column][0],
			"return_connection": MATRIX_RETURN[column][1],
		},
		"provenance": provenance(status, *sources),
	}
	if used and spec.get("part_number"):
		result["physical"]["part_number"] = spec["part_number"]
	if used and spec.get("roles"):
		result["roles"] = spec["roles"]
	return result


def dedicated_switch(device: int, manual_number: int, label: str, availability: str, switch_type: str, sources: tuple[str, ...], status: str, normally_closed: bool = False, pulse: bool = False) -> dict[str, object]:
	return {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device},
		"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
		"normally_closed": normally_closed,
		"pulse": pulse,
		"availability": availability,
		"physical": {"switch_type": switch_type},
		"provenance": provenance(status, *sources),
	}


def dip_switch(number: int, source: str, status: str) -> dict[str, object]:
	return {
		"id": f"switch.dip-{number}",
		"label": f"CPU/Sound board DIP switch {number}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": number},
		"aliases": aliases("pinmame.dip", number, f"D-{24 + number}"),
		"availability": "used",
		"physical": {"switch_type": "dip", "location": "CPU/Sound board between connectors J3 and J13"},
		"provenance": provenance(status, source),
	}


PREMIUM_SWITCHES: dict[int, dict[str, object]] = {
	1: {"label": "Right spinner", "switch_type": "other", "pulse": True},
	2: {"label": "Well Walker", "switch_type": "microswitch", "part_number": "180-5119-02", "roles": ["position.rest"]},
	3: {"label": "Prison Walker hit", "switch_type": "other", "pulse": True, "part_number": "515-7497-02"},
	4: {"label": "Prison doors closed", "switch_type": "microswitch", "part_number": "180-5119-02", "roles": ["position.open-runtime"]},
	9: {"label": "Left 3-bank target #1 (bottom)", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	10: {"label": "Left 3-bank target #2 (middle)", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	11: {"label": "Left 3-bank target #3 (top)", "switch_type": "microswitch", "part_number": "520-5252-03", "roles": ["position.down"]},
	15: {"label": "Tournament start", "switch_type": "button", "part_number": "180-5174-00"},
	16: {"label": "Start", "switch_type": "button", "part_number": "180-5174-00"},
	18: {"label": "Trough #4 (left)", "switch_type": "microswitch", "part_number": "180-5119-02"},
	19: {"label": "Trough #3", "switch_type": "microswitch", "part_number": "180-5119-02"},
	20: {"label": "Trough #2", "switch_type": "microswitch", "part_number": "180-5119-02"},
	21: {"label": "Trough #1 (right opto)", "switch_type": "opto", "part_number": "515-0173-00"},
	22: {"label": "Trough jam", "switch_type": "opto", "part_number": "515-0173-00"},
	23: {"label": "Shooter lane", "switch_type": "microswitch", "part_number": "180-5157-01"},
	24: {"label": "Left outlane", "switch_type": "leaf", "part_number": "500-6227-04"},
	25: {"label": "Left return lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	26: {"label": "Left slingshot", "switch_type": "leaf", "pulse": True, "part_number": "180-5054-00"},
	27: {"label": "Right slingshot", "switch_type": "leaf", "pulse": True, "part_number": "180-5054-00"},
	28: {"label": "Right return lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	29: {"label": "Right outlane", "switch_type": "leaf", "part_number": "500-6227-04"},
	30: {"label": "Left pop bumper", "switch_type": "leaf", "pulse": True, "part_number": "180-5015-04"},
	31: {"label": "Right pop bumper", "switch_type": "leaf", "pulse": True, "part_number": "180-5015-04"},
	32: {"label": "Top pop bumper", "switch_type": "leaf", "pulse": True, "part_number": "180-5015-04"},
	33: {"label": "Upper shooter lane", "switch_type": "leaf", "part_number": "500-6227-03"},
	34: {"label": "Right ramp enter", "switch_type": "microswitch", "part_number": "180-5087-00"},
	35: {"label": "Left ramp exit", "switch_type": "microswitch", "pulse": True, "part_number": "180-5087-00"},
	36: {"label": "Left top lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	37: {"label": "Right top lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	38: {"label": "Tower standup", "switch_type": "other", "pulse": True, "part_number": "515-7640-08"},
	39: {"label": "Right loop", "switch_type": "leaf", "pulse": True, "part_number": "500-6227-03"},
	40: {"label": "Left loop spinner", "switch_type": "other", "pulse": True, "part_number": "180-5010-04"},
	41: {"label": "Left loop", "switch_type": "leaf", "pulse": True, "part_number": "500-6227-04"},
	42: {"label": "Right ramp exit", "switch_type": "microswitch", "pulse": True, "part_number": "180-5087-00"},
	43: {"label": "Left ramp enter", "switch_type": "microswitch", "pulse": True, "part_number": "180-5057-00"},
	44: {"label": "Left prison standup", "switch_type": "other", "pulse": True, "part_number": "515-7561-08"},
	45: {"label": "Right prison standup", "switch_type": "other", "pulse": True, "part_number": "515-7581-08"},
	46: {"label": "Prison doors opto", "switch_type": "opto", "part_number": "500-6775-01"},
	47: {"label": "Center lane", "switch_type": "leaf", "part_number": "500-6227-04"},
	48: {"label": "Right drop target", "switch_type": "microswitch", "part_number": "520-5252-01", "roles": ["position.down"]},
	49: {"label": "Bicycle Girl hit", "switch_type": "other", "pulse": True, "part_number": "515-7497-02"},
	50: {"label": "Crossbow home", "switch_type": "microswitch", "part_number": "180-5119-02", "roles": ["position.home"]},
	51: {"label": "Crossbow mark", "switch_type": "microswitch", "part_number": "180-5119-02", "roles": ["position.mark"]},
	52: {"label": "Crossbow eject / ball loaded", "switch_type": "microswitch", "part_number": "515-5181-00", "roles": ["ball.loaded"]},
}

PRO_SWITCHES = {number: dict(spec) for number, spec in PREMIUM_SWITCHES.items() if number not in {1, 12, 13, 40, 48, 49, 50, 51, 52}}
PRO_SWITCHES[4] = {**PRO_SWITCHES[4], "roles": ["position.closed-runtime"]}
PRO_SWITCHES[12] = {"label": "Star rollover (top)", "switch_type": "leaf", "part_number": "520-6824-18"}
PRO_SWITCHES[13] = {"label": "Star rollover (bottom)", "switch_type": "leaf", "part_number": "520-6824-18"}


def complete_inputs(switches: dict[int, dict[str, object]], manual: str, validated: bool, premium: bool) -> list[dict[str, object]]:
	status = "validated" if validated else "observed"
	script_source = VPX_SOURCE if premium else PRO_VPX_SOURCE
	runtime_sources = (manual, script_source) if validated else (manual,)
	items = [matrix_switch(number, switches.get(number), runtime_sources if number in switches else (manual,), status) for number in range(1, 65)]
	dedicated_specs = [
		(65, 1, "Left coin chute", "used", "button", False),
		(66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False),
		(68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False),
	]
	if premium:
		dedicated_specs.extend([
			(70, 6, "Star rollover (bottom)", "used", "leaf", False),
			(71, 7, "Fire button", "used", "button", False),
			(72, 8, "Star rollover (top)", "used", "leaf", False),
		])
	else:
		dedicated_specs.extend([(70, 6, "Unused dedicated switch D6", "unused", "unknown", False), (71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False)])
	dedicated_specs.extend([
		(84, 9, "Left flipper button", "used", "button", False),
		(83, 10, "Left flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right flipper button", "used", "button", False),
		(81, 12, "Right flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Unused dedicated switch D13", "unused", "unknown", False),
		(87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Unused dedicated switch D15", "unused", "unknown", False),
		(85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False),
		(-6, 18, "Slam tilt", "optional", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False),
		(-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False),
		(-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False),
		(0, 24, "Coin-door Select button", "used", "button", False),
	])
	for device, manual_number, label, availability, switch_type, normally_closed in dedicated_specs:
		items.append(dedicated_switch(device, manual_number, label, availability, switch_type, runtime_sources if availability != "unused" else (manual,), status, normally_closed))
	items.extend(dip_switch(number, manual, status) for number in range(1, 9))
	return items


def output_device(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], status: str, group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, output_id: str | None = None) -> dict[str, object]:
	alias_namespace = "pinmame.solenoid" if group.endswith("solenoid") else "pinmame.gi" if group.endswith(".gi") else "pinmame.lamp"
	result: dict[str, object] = {
		"id": output_id or f"device.{slug(label)}",
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"aliases": aliases(alias_namespace, address, manual_address),
		"availability": availability,
		"provenance": provenance(status, *sources),
	}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


COIL_WIRING = {
	1: ("YEL-VIO", "J10-P9/10", "BRN-BLK", "J8-P1", 50), 2: ("YEL-VIO", "J10-P9/10", "BRN-RED", "J8-P3", 50),
	3: ("YEL-VIO", "J10-P9/10", "BRN-ORG", "J8-P4", 50), 4: ("YEL-VIO", "J10-P9/10", "BRN-YEL", "J8-P5", 50),
	5: ("YEL-VIO", "J10-P9/10", "BRN-GRN", "J8-P6", 50), 6: ("VIO-YEL", "J10-P8", "BRN-BLU", "J8-P7", 50),
	7: ("VIO-YEL", "J10-P8", "BRN-VIO", "J8-P8", 50), 8: ("RED-WHT", "J17-P7", "BRN-GRY", "J8-P9", 16),
	9: ("YEL-VIO", "J10-P9/10", "BLU-BRN", "J9-P1", 50), 10: ("YEL-VIO", "J10-P9/10", "BLU-RED", "J9-P2", 50),
	11: ("YEL-VIO", "J10-P9/10", "BLU-ORG", "J9-P4", 50), 12: ("YEL-VIO", "J10-P9/10", "BLU-YEL", "J9-P5", 50),
	13: ("YEL-VIO", "J10-P9/10", "BLU-GRN", "J9-P6", 50), 14: ("YEL-VIO", "J10-P9/10", "BLU-BLU", "J9-P7", 50),
	15: ("RED-YEL", "J10-P6/7", "ORG-GRY", "J9-P8", 50), 16: ("RED-YEL", "J10-P6/7", "ORG-VIO", "J9-P9", 50),
	19: ("ORG", "J6-P10", "VIO-ORG", "J7-P4", 20), 20: ("ORG", "J6-P10", "VIO-YEL", "J7-P6", 20),
	21: ("BRN", "J7-P1", "VIO-GRN", "J7-P7", 20), 24: ("RED", "J16-P4-8", "VIO-GRY", "J7-P10", 5),
	25: ("ORG", "J6-P10", "BLK-BRN", "J6-P1", 20), 26: ("ORG", "J6-P10", "BLK-RED", "J6-P2", 20),
	27: ("ORG", "J6-P10", "BLK-ORG", "J6-P3", 20), 28: ("ORG", "J6-P10", "BLK-YEL", "J6-P4", 20),
	29: ("ORG", "J6-P10", "BLK-GRN", "J6-P5", 20), 31: ("ORG", "J6-P10", "BLK-VIO", "J6-P7", 20),
	32: ("ORG", "J6-P10", "BLK-GRY", "J6-P8", 20),
	51: ("YEL-VIO", None, "YEL-BRN", None, 50), 52: ("YEL-VIO", None, "YEL-GRY", None, 50),
	53: ("YEL-VIO", None, "YEL-ORG", None, 50), 55: ("YEL-VIO", None, "YEL-GRN", None, 50),
	56: ("YEL-VIO", None, "YEL-BLU", None, 50),
}


def coil_wiring(address: int) -> dict[str, object] | None:
	if address not in COIL_WIRING:
		return None
	power_wire, power_connection, control_wire, control_connection, voltage = COIL_WIRING[address]
	wiring = {"board": "I/O Power Driver board" if address <= 32 else "6-transistor driver board", "driver_transistor": f"Q{address}", "power_wire": power_wire, "control_wire": control_wire, "nominal_voltage_v": voltage, "voltage_type": "ac" if address == 8 else "dc"}
	if power_connection:
		wiring["power_connection"] = power_connection
	if control_connection:
		wiring["control_connection"] = control_connection
	return wiring


PREMIUM_COILS = {
	1: ("Trough up-kicker", "coil", "used", "26-1200 / 090-5044-ND"), 2: ("Auto launch", "coil", "used", "23-800 / 090-5001-ND"),
	3: ("Prison doors (power)", "coil", "used", "090-5083-00"), 4: ("Prison doors (hold)", "coil", "used", "090-5083-00"),
	5: ("Ramp magnet diverter", "magnet", "used", "31-1500 / 090-5045-ND"), 6: ("Well magnet", "magnet", "used", "22-850 / 511-5065-ND"),
	7: ("Prison magnet", "magnet", "used", "22-850 / 511-5065-ND"), 8: ("Shaker motor", "motor", "optional", "502-5027-00"),
	9: ("Left pop bumper", "coil", "used", "26-1200 / 090-5044-ND"), 10: ("Right pop bumper", "coil", "used", "26-1200 / 090-5044-ND"),
	11: ("Top pop bumper", "coil", "used", "26-1200 / 090-5044-ND"), 12: ("Left 3-bank drop-target reset", "coil", "used", "25-1240 / 090-5034-ND"),
	13: ("Left slingshot", "coil", "used", "26-1200 / 090-5044-ND"), 14: ("Right slingshot", "coil", "used", "26-1200 / 090-5044-ND"),
	15: ("Left flipper", "coil", "used", "22-1080 / 090-5032-ND"), 16: ("Right flipper", "coil", "used", "22-1080 / 090-5032-ND"),
	17: ("Unused coil output #17", "coil", "unused", None), 18: ("Unused coil output #18", "coil", "unused", None),
	19: ("Well Walker flasher", "flasher", "used", "LED 113-5034-02"), 20: ("Right spinner flasher", "flasher", "used", "LED 113-5034-08"),
	21: ("Crossbow motor", "motor", "used", "041-5081-00"), 22: ("Unused coil output #22", "coil", "unused", None),
	23: ("Unused coil output #23", "coil", "unused", None), 24: ("Optional coin meter", "relay", "optional", "Coin meter"),
	25: ("Pop-bumper flasher", "flasher", "used", "LED 113-5034-08"), 26: ("Prison top flasher", "flasher", "used", "LED 113-5034-08"),
	27: ("Prison bottom flashers (x2)", "flasher", "used", "LED 112-5044-02"), 28: ("Left dome flasher", "flasher", "used", "LED 113-5034-08"),
	29: ("Right dome flasher", "flasher", "used", "LED 113-5034-08"), 30: ("Unused coil output #30", "coil", "unused", None),
	31: ("Left loop flasher", "flasher", "used", "LED 113-5034-08"), 32: ("Center loop flasher", "flasher", "used", "LED 113-5034-08"),
	51: ("Crossbow eject", "coil", "used", "23-800 / 090-5001-NL"), 52: ("Right drop target (down)", "coil", "used", "32-1800 / 090-5031-00-ND"),
	53: ("Right drop target (up)", "coil", "used", "25-1240 / 090-5034-ND"), 54: ("Unused auxiliary output #54", "coil", "unused", None),
	55: ("Bicycle Girl ramp (power)", "coil", "used", "Dual winding 090-5083-00-ND"), 56: ("Bicycle Girl ramp (hold)", "coil", "used", "Dual winding 090-5083-00-ND"),
}

PRO_COILS = {address: spec for address, spec in PREMIUM_COILS.items() if address <= 32}
for address in (5, 6, 20):
	PRO_COILS[address] = (f"Unused coil output #{address}", "coil", "unused", None)
PRO_COILS[21] = ("Horde flasher", "flasher", "used", "LED 113-5034-08")


PREMIUM_LAMP_NAMES = [
	"Start button", "Tournament start button", "2X playfield values", "Shoot again", "4 walkers killed", "3 walkers killed", "2 walkers killed", "1 walker killed",
	"40 walkers killed", "Last Man Standing", "5 walkers killed", "10 walkers killed", "20 walkers killed", "30 walkers killed", "Hammer multi-kill", "Sword multi-kill",
	"Crossbow multi-kill", "Gun multi-kill", "Knife multi-kill", "Axe multi-kill", "Horde", "Left outlane", "Left return lane", "Right loop arrow",
	"Blood Bath", "First Aid", "Weapons", "Food", "Left ramp Walker kill", "Left loop Walker kill", "Left loop multi-kill", "Barn mode",
	"Left loop arrow", "Left ramp multi-kill", "CDC mode", "Left ramp arrow", "Right outlane", "Right return lane", "Extra ball", "Welcome to Woodbury",
	"Right ramp arrow", "Right ramp Walker kill", "Right ramp multi-kill", "Arena mode", "Well Walker kill", "(W)ELL", "W(E)LL", "WE(L)L",
	"WEL(L)", "Well Walker", "Right loop Walker kill", "Right loop multi-kill", "Tunnel mode", "Siege", "Right prison standup", "Left prison standup",
	"Center lane arrow", "Riot mode", "Center lane multi-kill", "Top pop bumper", "Right pop bumper", "Left pop bumper", "Center lane Walker kill", "(P)RISON",
	"P(R)ISON", "PR(I)SON", "PRI(S)ON", "PRIS(O)N", "PRISO(N)", "Crossbow", "Fish tank", "Tower",
	"Fish tank head #1", "Fish tank head #2", "Fish tank head #3", "Left top lane", "Right top lane", "Bicycle Girl", "Star rollover (bottom)", "Star rollover (top)",
]

PRO_LAMP_NAMES = list(PREMIUM_LAMP_NAMES)
PRO_LAMP_NAMES[9] = "Killing spree"
PRO_LAMP_NAMES[15] = "Katana multi-kill"
PRO_LAMP_NAMES[17] = "Pistol multi-kill"
PRO_LAMP_NAMES[19] = "Chair multi-kill"

RGB_LAMPS = {
	24: ("Right loop arrow", {"red": 168, "green": 169, "blue": 170}),
	33: ("Left loop arrow", {"red": 195, "green": 196, "blue": 197}),
	36: ("Left ramp arrow", {"red": 203, "green": 204, "blue": 205}),
	41: ("Right ramp arrow", {"red": 152, "green": 153, "blue": 154}),
	57: ("Center lane arrow", {"red": 187, "green": 188, "blue": 189}),
	79: ("Star rollover (bottom)", {"red": 138, "green": 137, "blue": 136}),
	80: ("Star rollover (top)", {"red": 135, "green": 134, "blue": 133}),
	81: ("Fire button", {"red": 122, "green": 121, "blue": 120}),
}


def premium_lamps() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for manual_number, label in enumerate(PREMIUM_LAMP_NAMES, start=1):
		if manual_number in RGB_LAMPS:
			continue
		items.append(output_device(manual_number, label, "lamp", "used", (PREMIUM_MANUAL, VPX_SOURCE), "validated", "pinmame.output.lamp", str(manual_number), {"location": "Playfield or cabinet as shown on manual PDF pages 10-12", "notes": f"Physical lamp #{manual_number}"}, output_id=f"lamp.{slug(label)}"))
	for manual_number, (label, channels) in RGB_LAMPS.items():
		for color, address in channels.items():
			items.append(output_device(address, f"{label} ({color})", "rgb_lamp", "used", (PREMIUM_MANUAL, VPX_SOURCE, CORE_SOURCE), "validated", "pinmame.output.lamp", f"{manual_number}:{color}", {"location": "Playfield" if manual_number != 81 else "Lockbar fire button", "notes": f"{color.capitalize()} channel of physical RGB lamp #{manual_number}"}, output_id=f"lamp.{slug(label)}.{color}"))
	items.append(output_device(106, "White general illumination", "gi", "used", (PREMIUM_MANUAL, VPX_SOURCE, PREMIUM_ROM_SOURCE, CORE_SOURCE, PREMIUM_BOOT_SOURCE), "validated", "pinmame.output.lamp", "GI-0-WHT", {"quantity": 23, "location": "Twenty-three white bayonet LEDs around the playfield", "notes": "Exact-ROM output name WHITE and manual circuit GI-0-WHT; the known-working VPW script consumes public address 106 as white GI. Socket positions come from manual sheet Y26 in player view."}, output_id="lamp.gi-white"))
	items[-1]["range"] = {"minimum": 0, "maximum": 255, "steps": 256}
	items.append(output_device(107, "Rear-panel red general illumination", "gi", "used", (PREMIUM_MANUAL, PREMIUM_ROM_SOURCE, CORE_SOURCE, PREMIUM_BOOT_SOURCE), "validated", "pinmame.output.lamp", "GI-1-BACK PANEL", {"quantity": 2, "location": "Two red bayonet LEDs on the five-socket GI mounting panel shown in the manual Y26 inset, projected to the rear playfield edge", "notes": "Exact-ROM output name BACK PANEL and manual circuit GI-1-BACK PANEL identify this red pair. The VPW table instead applies address 107 as a broad red-GI rendering shortcut. The Y26 inset exposes the 077-5000-00 staple-bayonet socket mounting hardware and rear connector/board enclosure, establishing a service/rear-face view; socket x positions are normalized within the panel outline and reflected into player view."}, output_id="lamp.gi-back-panel-red"))
	items[-1]["range"] = {"minimum": 0, "maximum": 255, "steps": 256}
	items.append(output_device(108, "Left drop-target-bank green illumination", "gi", "used", (PREMIUM_MANUAL, PREMIUM_ROM_SOURCE, CORE_SOURCE, PREMIUM_BOOT_SOURCE), "validated", "pinmame.output.lamp", "GI-2-GRN", {"quantity": 3, "location": "Three green bayonet LEDs on the five-socket GI mounting panel shown in the manual Y26 inset, projected to the rear playfield edge", "notes": "Exact-ROM output name LEFT DROP TARGET BANK identifies the controller effect; manual circuit GI-2-GRN identifies its green three-socket group. The firmware name does not assert that the sockets sit directly above the drop targets. The Y26 inset exposes the 077-5000-00 staple-bayonet socket mounting hardware and rear connector/board enclosure, establishing a service/rear-face view; socket x positions are normalized within the panel outline and reflected into player view."}, output_id="lamp.gi-left-drop-target-bank"))
	items[-1]["range"] = {"minimum": 0, "maximum": 255, "steps": 256}
	items.append(output_device(109, "Red general illumination", "gi", "used", (PREMIUM_MANUAL, PREMIUM_ROM_SOURCE, CORE_SOURCE, PREMIUM_BOOT_SOURCE), "validated", "pinmame.output.lamp", "GI-3-RED", {"quantity": 14, "location": "Fourteen red bayonet LEDs around the playfield", "notes": "Exact-ROM output name RED and manual circuit GI-3-RED identify the fourteen red playfield emitters. Socket positions come from manual sheet Y26 in player view."}, output_id="lamp.gi-red"))
	items[-1]["range"] = {"minimum": 0, "maximum": 255, "steps": 256}
	return items


def pro_lamps() -> list[dict[str, object]]:
	items = []
	for number, label in enumerate(PRO_LAMP_NAMES, start=1):
		note = f"Physical lamp #{number}. The Pro script consumes the conventional SAM lamp callback at this address."
		if number == 2:
			note = "Physical lamp #2 is identified by the Pro manual. The known-working Pro table omits its render callback, which is a table-object omission rather than evidence that the cabinet lamp is absent."
		elif number in {73, 74, 75}:
			note = f"Physical lamp #{number} is identified by the Pro manual. The known-working Pro script retains but comments out its table-render callback; the manual remains authoritative for the physical lamp."
		items.append(output_device(number, label, "lamp", "used", (PRO_MANUAL, PRO_VPX_SOURCE), "validated", "pinmame.output.lamp", str(number), {"location": "Playfield or cabinet as shown on manual PDF page 19", "notes": note}, output_id=f"lamp.{slug(label)}"))
	items.append(output_device(0, "General illumination", "gi", "used", (PRO_MANUAL, PRO_VPX_SOURCE, PRO_RUNTIME_SOURCE), "validated", "pinmame.output.gi", "GI-0", {"quantity": 33, "location": "Twenty-eight white playfield bayonets plus five white back-panel bayonets", "notes": "Official Pro manual PDF page 38 / printed page 36 is the physical emitter map. The known-working Pro script uses one GICallback and the isolated ROM run observes public GI address 0."}, output_id="gi.general-illumination"))
	return items


def coil_outputs(specs: dict[int, tuple[str, str, str, str | None]], manual: str, validated: bool, script_source: str = VPX_SOURCE) -> list[dict[str, object]]:
	status = "validated" if validated else "observed"
	items = []
	for address, (label, kind, availability, part_number) in specs.items():
		sources = (manual, script_source) if validated and availability != "unused" else (manual,)
		physical = {"location": "Playfield or cabinet"}
		if part_number:
			physical["part_number"] = part_number
		items.append(output_device(address, label, kind, availability, sources, status, manual_address=str(address), physical=physical, wiring=coil_wiring(address)))
	items.append(output_device(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, PRO_RUNTIME_SOURCE) if manual == PRO_MANUAL else (CORE_SOURCE,), status, physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}, output_id="virtual.game-on"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], status: str, positions: list[dict[str, object]] | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(status, *sources)}
	if positions:
		result["positions"] = positions
	return result


def premium_mechanisms() -> list[dict[str, object]]:
	sources = (PREMIUM_MANUAL, VPX_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-opto", "switch.trough-jam"], "Four balls begin at switches 18-21. A drained ball enters the left end; the working script settles vacancies from 18 toward 21 after 150 ms, and output 1 ejects the ball at switch 21 toward the shooter lane. Switch 22 is the entrance/jam opto.", sources, "validated"),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 fires the automatic plunger for a ball resting at shooter-lane switch 23.", sources, "validated"),
		mechanism("mechanism.prison-doors", "Dual prison doors", "gate", ["device.prison-doors-power", "device.prison-doors-hold"], ["switch.prison-doors-closed", "switch.prison-doors-opto"], "The doors use a dual-winding power/hold coil. The known-working script starts opening on output 3 and starts closing when output 4 de-asserts. Despite the manual name 'Prison Doors Closed', the script reports switch 4 inactive at the closed initial position and active at its fully open position; switch 46 reports ball passage through the door opto.", sources, "validated", [{"id": "position.closed", "label": "Closed", "sensors": [], "description": "Initial runtime state; switch 4 is inactive in the known-working script."}, {"id": "position.open", "label": "Open", "sensors": ["switch.prison-doors-closed"], "description": "Known-working script sets switch 4 active at the open stop."}]),
		mechanism("mechanism.ramp-diverter-magnet", "Ramp diverter magnet", "diverter", ["device.ramp-magnet-diverter"], [], "Output 5 energizes the magnetic diverter zone. The working script applies magnetic force directly to balls entering that zone; there is no separate position switch.", sources, "validated"),
		mechanism("mechanism.well-walker", "Well Walker target and magnet", "toy", ["device.well-magnet"], ["switch.well-walker"], "The Well Walker is a spring-return target with a magnetic ball-control zone. Switch 2 is active at rest in the working script, clears on a hit, and reactivates when the toy returns. Output 6 controls the well magnet.", sources, "validated", [{"id": "position.rest", "label": "Rest", "sensors": ["switch.well-walker"]}, {"id": "position.deflected", "label": "Deflected", "sensors": []}]),
		mechanism("mechanism.prison-magnet", "Prison capture magnet", "other", ["device.prison-magnet"], ["switch.prison-doors-opto"], "Output 7 controls the prison capture magnet. The working script adds a ball when it enters the prison magnet zone and releases it with a small randomized lateral/forward velocity when the magnet turns off.", sources, "validated"),
		mechanism("mechanism.left-drop-bank", "Left three-bank drop targets", "drop_target_bank", ["device.left-3-bank-drop-target-reset"], ["switch.left-3-bank-target-1-bottom", "switch.left-3-bank-target-2-middle", "switch.left-3-bank-target-3-top"], "Targets 9-11 latch down and keep their switches active. Output 12 raises all three targets; the script uses approximately 110 ms down travel, 40 ms initial up travel, and 40 ms at the raised overshoot before settling.", sources, "validated"),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.top-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.top-pop-bumper"], "Switches 30-32 pulse the corresponding pop-bumper mechanisms driven by outputs 9-11.", sources, "validated"),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26 and 27 pulse the left and right slingshot assemblies driven by outputs 13 and 14.", sources, "validated"),
		mechanism("mechanism.flippers", "Lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "SAM fast-flip inputs drive outputs 15 and 16. The normally-closed EOS contacts are exposed at PinMAME switches 83 (left) and 81 (right).", (PREMIUM_MANUAL, VPX_SOURCE, CORE_SOURCE), "validated"),
		mechanism("mechanism.crossbow-cannon", "Motorized crossbow cannon", "motorized", ["device.crossbow-motor", "device.crossbow-eject"], ["switch.crossbow-home", "switch.crossbow-mark", "switch.crossbow-eject-ball-loaded"], "At home, switch 50 is active and switch 52 is active only while a ball is loaded. Output 21 starts the sweep: the script clears 50 and 52, activates mark switch 51 near the center, reverses at the far limit, then restores 50 and any loaded-ball state on return. Output 51 ejects the carried ball in the current cannon direction.", sources, "validated", [{"id": "position.home", "label": "Home", "sensors": ["switch.crossbow-home"]}, {"id": "position.mark", "label": "Mark", "sensors": ["switch.crossbow-mark"]}, {"id": "position.loaded", "label": "Ball loaded", "sensors": ["switch.crossbow-eject-ball-loaded"]}]),
		mechanism("mechanism.right-drop-target", "Right single drop target", "drop_target_bank", ["device.right-drop-target-down", "device.right-drop-target-up"], ["switch.right-drop-target"], "Output 52 forces target 48 down; output 53 raises it. Switch 48 remains active while the target is down.", sources, "validated", [{"id": "position.up", "label": "Up", "sensors": []}, {"id": "position.down", "label": "Down", "sensors": ["switch.right-drop-target"]}]),
		mechanism("mechanism.bicycle-girl-ramp", "Bicycle Girl motorized ramp", "motorized", ["device.bicycle-girl-ramp-power", "device.bicycle-girl-ramp-hold"], [], "The physical ramp uses dual-winding outputs 55 (short power/open pulse) and 56 (hold). The known-working script intentionally keys animation from output 56: asserted raises the ramp and removes the blocking surface; de-asserted lowers it and restores the surface. It does not attach a callback to the short output-55 pulse.", sources, "validated", [{"id": "position.lowered", "label": "Lowered", "sensors": []}, {"id": "position.raised", "label": "Raised", "sensors": []}]),
		mechanism("mechanism.bicycle-girl-target", "Bicycle Girl bash target", "toy", [], ["switch.bicycle-girl-hit"], "A ball hit pulses switch 49 and deflects the spring-return Bicycle Girl figure before it returns to rest.", sources, "validated"),
		mechanism("mechanism.prison-walker-target", "Prison Walker bash target", "toy", [], ["switch.prison-walker-hit"], "A ball hit pulses switch 3 and deflects the spring-return Prison Walker figure before it returns to rest.", sources, "validated"),
		mechanism("mechanism.spinners", "Left and right spinners", "other", [], ["switch.right-spinner", "switch.left-loop-spinner"], "Each spinner rotation pulses its switch: right spinner 1 and left-loop spinner 40.", sources, "validated"),
	]


def pro_mechanisms() -> list[dict[str, object]]:
	s = (PRO_MANUAL, PRO_VPX_SOURCE)
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", ["device.trough-up-kicker"], ["switch.trough-4-left", "switch.trough-3", "switch.trough-2", "switch.trough-1-right-opto", "switch.trough-jam"], "Initialize four balls at switches 18-21. The known-working Pro script orders the stack from exit switch 21 through 20, 19, and left switch 18, identifies it as a trough, ejects through output 1 at angle 90 and force 4, and pulses jam switch 22 during release.", s, "validated"),
		mechanism("mechanism.auto-launcher", "Auto launcher", "kicker", ["device.auto-launch"], ["switch.shooter-lane"], "Output 2 fires the automatic plunger for a ball at shooter-lane switch 23. The proven impulse settings are power 50, duration 0.6, and randomness 1.5.", s, "validated"),
		mechanism("mechanism.prison-doors", "Dual prison doors", "gate", ["device.prison-doors-power", "device.prison-doors-hold"], ["switch.prison-doors-closed", "switch.prison-doors-opto"], "The doors use a dual-winding power/hold coil. In the known-working Pro script, output 3 asserted opens both doors and clears switch 4; output 4 de-asserted closes them and sets switch 4. Switch 46 reports ball passage through the prison-door opto.", s, "validated", [{"id": "position.open", "label": "Open", "sensors": [], "description": "Output 3 asserted; switch 4 inactive in the Pro script."}, {"id": "position.closed", "label": "Closed", "sensors": ["switch.prison-doors-closed"], "description": "Output 4 de-asserted; switch 4 active in the Pro script."}]),
		mechanism("mechanism.prison-magnet", "Prison capture magnet", "other", ["device.prison-magnet"], ["switch.prison-doors-opto"], "Output 7 controls a radius-30 centered capture magnet. On release, balls within radius 15 receive a random full-circle direction and speed from 15 up to 20 before the magnet turns off.", s, "validated"),
		mechanism("mechanism.left-drop-bank", "Left three-bank drop targets", "drop_target_bank", ["device.left-3-bank-drop-target-reset"], ["switch.left-3-bank-target-1-bottom", "switch.left-3-bank-target-2-middle", "switch.left-3-bank-target-3-top"], "Targets 9-11 latch down and maintain their switches. Output 12 raises the complete bank through the VPX drop-target controller.", s, "validated"),
		mechanism("mechanism.well-walker", "Well Walker target", "toy", [], ["switch.well-walker"], "The Well Walker is a spring-return target without the Premium/LE well magnet. Switch 2 initializes active at rest, clears on impact, and returns active when the target timer restores it.", s, "validated", [{"id": "position.rest", "label": "Rest", "sensors": ["switch.well-walker"]}, {"id": "position.deflected", "label": "Deflected", "sensors": []}]),
		mechanism("mechanism.prison-walker-target", "Prison Walker bash target", "toy", [], ["switch.prison-walker-hit"], "A ball hit pulses switch 3 and briefly deflects the spring-return Prison Walker figure before the table timer restores it.", s, "validated"),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "kicker", ["device.left-pop-bumper", "device.right-pop-bumper", "device.top-pop-bumper"], ["switch.left-pop-bumper", "switch.right-pop-bumper", "switch.top-pop-bumper"], "Switches 30-32 pulse the corresponding pop-bumper mechanisms driven by outputs 9-11.", s, "validated"),
		mechanism("mechanism.slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switches 26 and 27 pulse the left and right slingshot assemblies driven by outputs 13 and 14.", s, "validated"),
		mechanism("mechanism.flippers", "Lower flippers", "other", ["device.left-flipper", "device.right-flipper"], ["switch.left-flipper-button", "switch.left-flipper-end-of-stroke", "switch.right-flipper-button", "switch.right-flipper-end-of-stroke"], "SAM fast-flip inputs drive outputs 15 and 16. The normally-closed EOS contacts are exposed at PinMAME switches 83 (left) and 81 (right).", (PRO_MANUAL, PRO_VPX_SOURCE, CORE_SOURCE), "validated"),
	]


def driver_records(le: bool) -> list[dict[str, object]]:
	selected = []
	for driver_id, source in DRIVERS.items():
		is_le = bool(re.fullmatch(r"twd_\d+h(?:c)?", driver_id))
		if is_le != le:
			continue
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		if driver_id.endswith("c"):
			record["variant_notes"] = "Colored-ROM modification only; physical playfield I/O, mechanisms, wiring, and native 128x32 DMD topology are unchanged."
		else:
			record["variant_notes"] = "Firmware revision only within this physical edition; playfield I/O, mechanisms, wiring, and native display topology are unchanged."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(manual: str, premium: bool) -> list[dict[str, object]]:
	manual_record = {
		"id": manual, "kind": "manual", "uri": "https://archive.org/details/WalkingDeadPinballManual" if premium else "https://archive.org/details/SternPinballTheWalkingDeadProModelManual",
		"sha256": "4dd644210cc0432b254b8252b836c73c878517fa16eda119902155ece24f0b3e" if premium else "03bbf27093ad8b851ffe5b6284b1f14a4ccbce1ca0a68e79800db728bc92a5ae",
		"locator": "Walking Dead pinball Manual.pdf, PDF pages 8-15 and mechanism/parts drawings" if premium else "WD-PRO-MAN.pdf: switch map page 13, coil map page 16, lamp map page 19, GI map page 38, and wiring/assembly pages 39-45",
		"license": "CC0-1.0" if premium else "NOASSERTION", "attribution": "Stern Pinball", "source_id": "WalkingDeadPinballManual" if premium else "SternPinballTheWalkingDeadProModelManual",
		"original_filename": "Walking Dead pinball Manual.pdf" if premium else "WD-PRO-MAN.pdf", "rights": "http://creativecommons.org/publicdomain/zero/1.0/" if premium else "NOASSERTION",
		"acquired_at": "2026-08-02T11:12:01.288660Z" if premium else "2026-08-02T11:11:58.008489Z",
	}
	manual_record["excerpts"] = WALKING_DEAD_PREMIUM_EXCERPTS if premium else WALKING_DEAD_PRO_EXCERPTS
	result = [manual_record]
	if premium:
		result.extend([
			{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/The%20Walking%20Dead%20LE%20Premium%20%28Stern%202014%29%20day%201.1.vbs", "revision": VPX_REVISION, "sha256": "bd6868c93f180c58f6835cccd869c0fa1e28832fea6afc5bb4f9660505908e47", "locator": "The Walking Dead LE Premium (Stern 2014) day 1.1.vbs lines 123-300, 315-728, 1320-1710, and 4328-4470", "license": "NOASSERTION", "attribution": "Flupper1, Robby King Pin, Rothbauerw, VPW contributors, prior table authors, and vpxtable_scripts contributors"},
			{"id": PREMIUM_ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/twd_160h.zip", "revision": "V1.60", "sha256": "e09cba4477c9d551e858c0b4c8ee005fb041d3008a4cc5e928d502127329d3fd", "locator": "Exact user-authorized twd_160h.zip archive. Its member is named TWD160h.BIN (96,994,376 bytes), SHA-256 5f618c875d160ce27a73a0edf30659b63f08478147c4476b5b8916a614d6d6a3, SHA-1 1fbaa077ec834ff9d289008ef1169e0e7fd68271, CRC32 1ed7b80a; PinMAME declares the same bytes under canonical filename twd_160h.bin. Localized records at file offsets 0x109060, 0x109078, 0x109090, and 0x1090a8 are referenced by 1-based output IDs 25-28 at 0x1090c8-0x1090e0: WHITE, BACK PANEL, LEFT DROP TARGET BANK, and RED. PinMAME sam.c:1913-1919 maps node-board-3 ledMap index i to CORE_MODOUT_LAMP0+81+i, public lamp 82+i; IDs 25-28 are indices 24-27 and therefore public addresses 106-109. ROM bytes remain external.", "license": "NOASSERTION", "attribution": "Stern Pinball game code; analyzed locally from the user-authorized ROM corpus"},
			{"id": PREMIUM_BOOT_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/twd_160h/harness/boot-start-le-1.json", "revision": PINMAME_REVISION, "sha256": "dc40cfe85c90de2cc8c2ae16a8ca5a0d3cf2f8cbdc24d7eba39600601506fa77", "locator": "Exact twd_160h boot/start trace using PinMAME DLL SHA-256 79f6cfb0048470218b2302ca4fb0d078839acf7f05883c36fc93881ba8abac84 and ROM archive SHA-256 e09cba4477c9d551e858c0b4c8ee005fb041d3008a4cc5e928d502127329d3fd. Public 106 modulates independently; 107-109 have byte-for-byte identical event streams in this observed window.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
		])
	else:
		result.extend([
			{"id": PRO_VPX_SOURCE, "kind": "vpx_script", "uri": f"https://github.com/LegendsUnchained/vpx-standalone-alp4k/blob/{PRO_VPX_REVISION}/external/vpx-thewalkingdead/table.vbs", "revision": PRO_VPX_REVISION, "sha256": "18d92b612f8d4f0fe1c0f20131fbeb3588d8393502330ca321deb36c9fcbcac4", "locator": "external/vpx-thewalkingdead/table.vbs lines 1-165, 322-525, and 661-770", "license": "NOASSERTION", "attribution": "JPSalas and LegendsUnchained/vpx-standalone-alp4k contributors"},
			{"id": PRO_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/twd_156/boot-start-pro-1.json", "sha256": "ffb741cfa5f1238d756035c4c113b77ad94fdd2a9e015c21a92af0813595bccb", "locator": "Isolated LibPinMAME boot/start scenario using physically compatible twd_156.zip SHA-256 9f0fa7803236c566829037612c9d7732c153e5fa35681b7513324d3ae380a716; captures initial trough/Well state, 128x32x4 DMD, GI 0, lamp activity, and public solenoid transitions", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
		])
	result.extend([
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c lines 114-116, 455-461, 1388-1418, 1558-1563, and 1782-2190", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	])
	return result


def build_premium() -> dict[str, object]:
	outputs = coil_outputs(PREMIUM_COILS, PREMIUM_MANUAL, True) + premium_lamps()
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.the-walking-dead-premium-limited-edition.2014", "name": "The Walking Dead Premium / Limited Edition", "manufacturer": "Stern", "year": 2014, "ipdb_id": 6156, "opdb_id": "G5nz5-MP3r1"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(True), "inputs": complete_inputs(PREMIUM_SWITCHES, PREMIUM_MANUAL, True, True), "outputs": outputs,
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, PREMIUM_MANUAL]}}, "provenance": provenance("validated", CORE_SOURCE, VPX_SOURCE)}],
		"mechanisms": premium_mechanisms(), "relationships": [], "sources": sources(PREMIUM_MANUAL, True),
		"knowledge": {"path": "knowledge/stern/the-walking-dead-premium-limited-edition-2014.md", "status": "complete"}, "conflicts": [],
	}


def build_pro() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": "stern.the-walking-dead-pro.2014", "name": "The Walking Dead Pro", "manufacturer": "Stern", "year": 2014, "ipdb_id": 6155, "opdb_id": "G5nz5-M3d38"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(False), "inputs": complete_inputs(PRO_SWITCHES, PRO_MANUAL, True, False), "outputs": coil_outputs(PRO_COILS, PRO_MANUAL, True, PRO_VPX_SOURCE) + pro_lamps(),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, PRO_MANUAL]}}, "provenance": provenance("validated", CORE_SOURCE, PRO_RUNTIME_SOURCE)}],
		"mechanisms": pro_mechanisms(), "relationships": [], "sources": sources(PRO_MANUAL, False),
		"knowledge": {"path": "knowledge/stern/the-walking-dead-pro-2014.md", "status": "complete"}, "conflicts": [],
	}


def write_pending(path: Path, value: dict[str, object]) -> None:
	if value["machine"]["id"] not in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		return
	path = spatial_partial_path(path)
	value = fail_closed_spatial_partial(value)
	path.parent.mkdir(parents=True, exist_ok=True)
	write_json(path, value)


def curate() -> None:
	stale_paths = (
		ROOT / "machines/partial/stern/the-walking-dead-limited-edition-2014.json",
		ROOT / "machines/partial/stern/the-walking-dead-premium-limited-edition-2014.json",
		ROOT / "machines/partial/stern/the-walking-dead-pro-2014.json",
	)
	for stale_path in stale_paths:
		if stale_path.exists():
			stale_path.unlink()
	write_pending(ROOT / "machines/author-ready/stern/the-walking-dead-premium-limited-edition-2014.json", build_premium())
	write_pending(ROOT / "machines/author-ready/stern/the-walking-dead-pro-2014.json", build_pro())


if __name__ == "__main__":
	curate()
