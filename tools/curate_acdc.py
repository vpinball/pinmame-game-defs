"""Build reviewed AC/DC physical-edition definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from curate_acdc_spatial import apply_led_pro_spatial, apply_original_pro_spatial, apply_vault_spatial
from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("acd_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
PREMIUM_MANUAL = "manual.acdc-premium-le"
LUCI_MANUAL = "manual.acdc-luci-premium"
PRO_MANUAL = "manual.acdc-pro"
PREMIUM_VPX = "vpx.acdc-luci-premium-vpw-1.1.4"
PRO_VPX = "vpx.acdc-pro-1.0-lighting-fix"
PRO_TABLE = "vpx-table.acdc-pro-1.0"
VAULT_VPX = "vpx.acdc-pro-vault-1.0-lighting-fix"
VAULT_TABLE = "vpx-table.acdc-pro-vault-1.0"
PREMIUM_RUNTIME = "runtime.acdc-premium.boot-start"
PRO_RUNTIME = "runtime.acdc-pro.boot-start"
STERN_PRODUCT = "stern.acdc-product-page"
STERN_LED_PRO = "stern.acdc-led-pro-announcement"
IPDB_LUCI = "ipdb.acdc-luci.6060"
IPDB_PREMIUM = "ipdb.acdc-premium.5775"

PREMIUM_IDS = ["acd_150h", "acd_152h", "acd_160h", "acd_161h", "acd_163h", "acd_165h", "acd_168h", "acd_168hc", "acd_170h", "acd_170hc"]
ORIGINAL_PRO_IDS = ["acd_121", "acd_125", "acd_130", "acd_140", "acd_150", "acd_152", "acd_160", "acd_161", "acd_163", "acd_165"]
LED_PRO_IDS = ["acd_168", "acd_168c"]
VAULT_IDS = ["acd_170", "acd_170c"]


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


MATRIX_RETURNS = [
	("WHT-BRN", "J6-P9"), ("WHT-RED", "J6-P8"), ("WHT-ORG", "J6-P7"), ("WHT-YEL", "J6-P6"),
	("WHT-GRN", "J6-P5"), ("WHT-BLU", "J6-P3"), ("WHT-VIO", "J6-P2"), ("WHT-GRY", "J6-P1"),
	("TAN-BLK", "J12-P9"), ("TAN-RED", "J12-P8"), ("TAN-ORG", "J12-P7"), ("TAN-YEL", "J12-P6"),
	("TAN-GRN", "J12-P4"), ("TAN-BLU", "J12-P3"), ("TAN-VIO", "J12-P2"), ("TAN-WHT", "J12-P1"),
]
MATRIX_DRIVES = [("GRN-BRN", "J1-P1"), ("GRN-RED", "J1-P3"), ("GRN-ORG", "J1-P4"), ("GRN-YEL", "J1-P5")]


def switch(label: str, switch_type: str, *, pulse: bool = False, normally_closed: bool = False, roles: list[str] | None = None, notes: str | None = None) -> dict[str, object]:
	result: dict[str, object] = {"label": label, "switch_type": switch_type, "pulse": pulse, "normally_closed": normally_closed}
	if roles:
		result["roles"] = roles
	if notes:
		result["notes"] = notes
	return result


PREMIUM_SWITCHES: dict[int, dict[str, object]] = {
	1: switch("AC/DC drop target A (left)", "microswitch", roles=["position.down"]),
	2: switch("AC/DC drop target C (second)", "microswitch", roles=["position.down"]),
	3: switch("AC/DC drop target slash (center)", "microswitch", roles=["position.down"]),
	4: switch("AC/DC drop target D (fourth)", "microswitch", roles=["position.down"]),
	5: switch("AC/DC drop target C (right)", "microswitch", roles=["position.down"]),
	6: switch("ROCK standup target R", "microswitch", pulse=True),
	7: switch("ROCK standup target O", "microswitch", pulse=True),
	8: switch("ROCK standup target C", "microswitch", pulse=True),
	9: switch("ROCK standup target K", "microswitch", pulse=True),
	10: switch("TNT drop target T (left)", "microswitch", roles=["position.down"]),
	11: switch("TNT drop target N (center)", "microswitch", roles=["position.down"]),
	12: switch("TNT drop target T (right)", "microswitch", roles=["position.down"]),
	13: switch("Left ramp exit", "leaf"),
	14: switch("Left ramp entrance", "leaf"),
	15: switch("Tournament start", "button"),
	16: switch("Start", "button"),
	18: switch("Trough #4 (left / drain end)", "microswitch", roles=["ball.position"]),
	19: switch("Trough #3", "microswitch", roles=["ball.position"]),
	20: switch("Trough #2", "microswitch", roles=["ball.position"]),
	21: switch("Trough #1 (right / eject end)", "microswitch", roles=["ball.position"]),
	22: switch("Trough stack opto / jam", "opto", roles=["ball.jam"]),
	23: switch("Auto-launch shooter lane", "microswitch", roles=["ball.loaded"]),
	24: switch("Left outlane", "leaf"),
	25: switch("Left return lane", "leaf"),
	26: switch("Left slingshot", "leaf", pulse=True),
	27: switch("Right slingshot", "leaf", pulse=True),
	28: switch("Right return lane", "leaf"),
	29: switch("Right outlane", "leaf"),
	30: switch("Left pop bumper", "leaf", pulse=True),
	31: switch("Right pop bumper", "leaf", pulse=True),
	32: switch("Bottom pop bumper", "leaf", pulse=True),
	33: switch("Loop spinner", "other", pulse=True),
	34: switch("Thunder standup target (left / left-ramp standup)", "microswitch", pulse=True),
	35: switch("Thunder standup target (right / right-ramp standup)", "microswitch", pulse=True),
	36: switch("Bell eject saucer", "microswitch", roles=["ball.loaded"]),
	37: switch("Jukebox / top eject saucer", "microswitch", roles=["ball.loaded"]),
	38: switch("Top lane rollover (left)", "leaf"),
	39: switch("Top lane rollover (center)", "leaf"),
	40: switch("Top lane rollover (right)", "leaf"),
	41: switch("Right ramp entrance", "leaf"),
	42: switch("Thunder standup target (center)", "microswitch", pulse=True),
	43: switch("Right ramp exit", "leaf"),
	44: switch("Left orbit", "leaf"),
	45: switch("Cannon entry / loaded", "microswitch", roles=["ball.loaded"]),
	46: switch("Detonator target", "microswitch", pulse=True),
	47: switch("Swinging bell score opto", "opto", pulse=True),
	48: switch("Manual plunger lane", "microswitch", roles=["ball.loaded"]),
	49: switch("Lower mini-playfield eject opto", "opto", roles=["ball.loaded"]),
	50: switch("Lower mini-playfield standup (left)", "microswitch", pulse=True),
	51: switch("Lower mini-playfield standup (center)", "microswitch", pulse=True),
	52: switch("Lower mini-playfield standup (right)", "microswitch", pulse=True),
	53: switch("Lower mini-playfield rollover (left)", "leaf"),
	54: switch("Lower mini-playfield rollover (right)", "leaf"),
	59: switch("Right orbit", "leaf"),
	61: switch("Cannon home", "microswitch", roles=["position.home"]),
	62: switch("Cannon mark / mid-rotation", "microswitch", roles=["position.mark"]),
	64: switch("FIRE button", "button"),
}


PRO_SWITCHES: dict[int, dict[str, object]] = {
	1: switch("AC/DC standup target A (left)", "microswitch", pulse=True),
	2: switch("AC/DC standup target C (second)", "microswitch", pulse=True),
	3: switch("AC/DC standup target slash (center)", "microswitch", pulse=True),
	4: switch("AC/DC standup target D (fourth)", "microswitch", pulse=True),
	5: switch("AC/DC standup target C (right)", "microswitch", pulse=True),
	6: switch("ROCK standup target R", "microswitch", pulse=True),
	7: switch("ROCK standup target O", "microswitch", pulse=True),
	8: switch("ROCK standup target C", "microswitch", pulse=True),
	9: switch("ROCK standup target K", "microswitch", pulse=True),
	10: switch("TNT standup target T (left)", "microswitch", pulse=True),
	11: switch("TNT standup target N (center)", "microswitch", pulse=True),
	12: switch("TNT standup target T (right)", "microswitch", pulse=True),
	13: switch("Left ramp exit", "leaf"),
	14: switch("Left ramp entrance", "leaf"),
	15: switch("Tournament start", "button"),
	16: switch("Start", "button"),
	18: switch("Trough #4 (left / drain end)", "microswitch", roles=["ball.position"]),
	19: switch("Trough #3", "microswitch", roles=["ball.position"]),
	20: switch("Trough #2", "microswitch", roles=["ball.position"]),
	21: switch("Trough #1 (right / eject end)", "microswitch", roles=["ball.position"]),
	22: switch("Trough stack opto / jam", "opto", roles=["ball.jam"]),
	23: switch("Auto-launch shooter lane", "microswitch", roles=["ball.loaded"]),
	24: switch("Left outlane", "leaf"),
	25: switch("Left return lane", "leaf"),
	26: switch("Left slingshot", "leaf", pulse=True),
	27: switch("Right slingshot", "leaf", pulse=True),
	28: switch("Right return lane", "leaf"),
	29: switch("Right outlane", "leaf"),
	30: switch("Left pop bumper", "leaf", pulse=True),
	31: switch("Right pop bumper", "leaf", pulse=True),
	32: switch("Bottom pop bumper", "leaf", pulse=True),
	33: switch("Loop spinner", "other", pulse=True),
	34: switch("Thunder standup target (left)", "microswitch", pulse=True),
	35: switch("Thunder standup target (center)", "microswitch", pulse=True),
	36: switch("Hell's Bell standup target", "microswitch", pulse=True),
	37: switch("Jukebox / top eject saucer", "microswitch", roles=["ball.loaded"]),
	38: switch("Top lane rollover (left)", "leaf"),
	39: switch("Top lane rollover (center)", "leaf"),
	40: switch("Top lane rollover (right)", "leaf"),
	41: switch("Right ramp entrance", "leaf"),
	42: switch("Thunder standup target (right)", "microswitch", pulse=True),
	43: switch("Right ramp exit", "leaf"),
	44: switch("Left orbit", "leaf"),
	45: switch("Cannon entry / loaded", "microswitch", roles=["ball.loaded"]),
	48: switch("Manual plunger lane", "microswitch", roles=["ball.loaded"]),
	59: switch("Right orbit", "leaf"),
	61: switch("Cannon home", "microswitch", roles=["position.home"]),
	62: switch("Cannon mark / mid-rotation", "microswitch", roles=["position.mark"]),
	64: switch("FIRE button", "button"),
}


def input_id(number: int, label: str, group: str = "switch") -> str:
	address = f"neg{abs(number)}" if number < 0 else str(number)
	return f"input.{group}.{address}.{slug(label)}"


def complete_inputs(variant: str, sources: tuple[str, ...]) -> list[dict[str, object]]:
	premium = variant == "premium"
	specs = PREMIUM_SWITCHES if premium else {number: dict(spec) for number, spec in PRO_SWITCHES.items()}
	if variant in {"led-pro", "vault"}:
		specs[36] = switch("Swinging Hell's Bell score switch", "leaf", pulse=True, notes="Passive pendulum score sensor; no bell actuator is fitted.")
	items: list[dict[str, object]] = []
	manual = LUCI_MANUAL if premium else PRO_MANUAL
	for number in range(1, 65):
		spec = specs.get(number)
		row, column = divmod(number - 1, 16)
		used = spec is not None
		label = str(spec["label"]) if used else f"Unused matrix switch #{number}"
		physical: dict[str, object] = {"switch_type": str(spec.get("switch_type", "unknown")) if used else "unknown"}
		if used and spec.get("notes"):
			physical["notes"] = spec["notes"]
		selected_sources = sources if used else (manual,)
		item: dict[str, object] = {
			"id": input_id(number, label), "label": label, "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": number},
			"aliases": aliases("pinmame.switch", number, str(number)),
			"normally_closed": bool(spec.get("normally_closed", False)) if used else False,
			"pulse": bool(spec.get("pulse", False)) if used else False,
			"availability": "used" if used else "unused",
			"physical": physical,
			"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVES[row][0], "drive_connection": MATRIX_DRIVES[row][1], "return_wire": MATRIX_RETURNS[column][0], "return_connection": MATRIX_RETURNS[column][1]},
			"provenance": provenance(*selected_sources),
		}
		if used and spec.get("roles"):
			item["roles"] = spec["roles"]
		items.append(item)
	dedicated = [
		(65, 1, "Left coin chute", "used", "button", False), (66, 2, "Center coin chute", "used", "button", False),
		(67, 3, "Right coin chute", "used", "button", False), (68, 4, "Fourth coin chute", "optional", "button", False),
		(69, 5, "Fifth coin chute", "optional", "button", False), (70, 6, "Unused dedicated switch D6", "unused", "unknown", False),
		(71, 7, "Unused dedicated switch D7", "unused", "unknown", False), (72, 8, "Unused dedicated switch D8", "unused", "unknown", False),
		(84, 9, "Left main flipper button", "used", "button", False), (83, 10, "Left main flipper end-of-stroke", "used", "leaf", True),
		(82, 11, "Right main flipper button", "used", "button", False), (81, 12, "Right main flipper end-of-stroke", "used", "leaf", True),
		(88, 13, "Lower mini-playfield left flipper button" if premium else "Unused dedicated switch D13", "used" if premium else "unused", "button" if premium else "unknown", False),
		(87, 14, "Unused dedicated switch D14", "unused", "unknown", False),
		(86, 15, "Lower mini-playfield right flipper button" if premium else "Unused dedicated switch D15", "used" if premium else "unused", "button" if premium else "unknown", False),
		(85, 16, "Unused dedicated switch D16", "unused", "unknown", False),
		(-7, 17, "Pendulum tilt", "used", "tilt", False), (-6, 18, "Slam tilt", "optional", "tilt", True),
		(-5, 19, "Ticket notch", "optional", "microswitch", False), (-4, 20, "Unused dedicated switch D20", "unused", "unknown", False),
		(-3, 21, "Coin-door Back button", "used", "button", False), (-2, 22, "Coin-door Minus button", "used", "button", False),
		(-1, 23, "Coin-door Plus button", "used", "button", False), (0, 24, "Coin-door Select button", "used", "button", False),
	]
	for device, manual_number, label, availability, switch_type, normally_closed in dedicated:
		selected_sources = sources if availability != "unused" else (manual,)
		items.append({
			"id": input_id(device, label, "dedicated"), "label": label, "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": device},
			"aliases": aliases("pinmame.switch", device, f"D-{manual_number}"),
			"normally_closed": normally_closed, "pulse": False, "availability": availability,
			"physical": {"switch_type": switch_type}, "provenance": provenance(*selected_sources),
		})
	for number in range(1, 9):
		items.append({
			"id": input_id(number, f"CPU DIP {number}", "dip"), "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch",
			"binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"),
			"availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board between J3 and J13"}, "provenance": provenance(manual),
		})
	return items


PREMIUM_SOLENOIDS: dict[int, tuple[str, str, str, str | None]] = {
	1: ("Trough up-kicker", "coil", "used", "1"), 2: ("Auto launch", "coil", "used", "2"),
	3: ("Lower mini-playfield eject", "coil", "used", "3"), 4: ("Lower mini-playfield left flipper", "coil", "used", "4"),
	5: ("Lower mini-playfield right flipper", "coil", "used", "5"), 6: ("AC/DC 5-bank drop-target reset", "coil", "used", "6"),
	7: ("TNT 3-bank drop-target reset", "coil", "used", "7"), 8: ("Shaker motor", "motor", "optional", "8"),
	9: ("Left pop bumper", "coil", "used", "9"), 10: ("Right pop bumper", "coil", "used", "10"),
	11: ("Bottom pop bumper", "coil", "used", "11"), 12: ("Jukebox / top eject", "coil", "used", "12"),
	13: ("Left slingshot", "coil", "used", "13"), 14: ("Right slingshot", "coil", "used", "14"),
	15: ("Left main flipper", "coil", "used", "15"), 16: ("Right main flipper", "coil", "used", "16"),
	17: ("Train flasher", "flasher", "used", "17"), 18: ("Detonator mechanism", "coil", "used", "18"),
	19: ("Bottom arch flashers (two)", "flasher", "used", "19"), 20: ("Left ramp flasher", "flasher", "used", "20"),
	21: ("Left-side dome flasher", "flasher", "used", "21"), 22: ("Back-panel flasher", "flasher", "used", "22"),
	23: ("Top-eject flasher", "flasher", "used", "23"), 24: ("Knocker / optional coin-meter channel", "coil", "optional", "24"),
	25: ("Pop-bumper flashers (three)", "flasher", "used", "25"), 26: ("Bell-arrow flasher", "flasher", "used", "26"),
	27: ("Left-ramp left-side flasher", "flasher", "used", "27"), 28: ("Left-ramp right-side flasher", "flasher", "used", "28"),
	29: ("Right-ramp right-side flasher", "flasher", "used", "29"), 30: ("Right-ramp flasher", "flasher", "used", "30"),
	31: ("Right-side dome flasher", "flasher", "used", "31"), 32: ("Cannon motor", "motor", "used", "32"),
	33: ("Ticket advance", "coil", "optional", "33"), 34: ("Ticket meter", "coil", "optional", "34"), 35: ("Ticket switched ground", "relay", "optional", "35"),
	51: ("Animated band members", "coil", "used", "41"), 52: ("Bell eject", "coil", "used", "42"),
	53: ("Cannon eject / fire", "coil", "used", "43"), 54: ("Swinging-bell magnet", "magnet", "used", "44"),
	55: ("Right-ramp cannon diverter", "coil", "used", "45"), 56: ("Right control gate", "coil", "used", "46"),
	57: ("Left-ramp crossover diverter", "coil", "used", "47"), 58: ("Unused auxiliary output 48", "coil", "unused", "48"),
}


PRO_SOLENOIDS: dict[int, tuple[str, str, str, str | None]] = {
	1: ("Trough up-kicker", "coil", "used", "1"), 2: ("Auto launch", "coil", "used", "2"),
	3: ("Cannon eject / fire", "coil", "used", "3"), 4: ("Right-ramp cannon diverter", "coil", "used", "4"),
	5: ("Right control gate", "coil", "used", "5"), 6: ("Unused main output 6", "coil", "unused", "6"),
	7: ("Unused main output 7", "coil", "unused", "7"), 8: ("Shaker motor", "motor", "optional", "8"),
	9: ("Left pop bumper", "coil", "used", "9"), 10: ("Right pop bumper", "coil", "used", "10"),
	11: ("Bottom pop bumper", "coil", "used", "11"), 12: ("Jukebox / top eject", "coil", "used", "12"),
	13: ("Left slingshot", "coil", "used", "13"), 14: ("Right slingshot", "coil", "used", "14"),
	15: ("Left main flipper", "coil", "used", "15"), 16: ("Right main flipper", "coil", "used", "16"),
	17: ("Train flasher", "flasher", "used", "17"), 18: ("Unused main output 18", "coil", "unused", "18"),
	19: ("Unused main output 19", "coil", "unused", "19"), 20: ("Left ramp flasher", "flasher", "used", "20"),
	21: ("Left-side flasher", "flasher", "used", "21"), 22: ("Back-panel flasher", "flasher", "used", "22"),
	23: ("Top-eject flasher", "flasher", "used", "23"), 24: ("Knocker / optional coin-meter channel", "coil", "optional", "24"),
	25: ("Pop-bumper flashers", "flasher", "used", "25"), 26: ("Bell-arrow flasher", "flasher", "used", "26"),
	27: ("Left-ramp left-side flasher", "flasher", "used", "27"), 28: ("Left-ramp right-side flasher", "flasher", "used", "28"),
	29: ("Right-ramp right-side flasher", "flasher", "used", "29"), 30: ("Right-ramp flasher", "flasher", "used", "30"),
	31: ("Right-side flasher", "flasher", "used", "31"), 32: ("Cannon motor", "motor", "used", "32"),
	33: ("Ticket advance", "coil", "optional", "33"), 34: ("Ticket meter", "coil", "optional", "34"), 35: ("Ticket switched ground", "relay", "optional", "35"),
}


PREMIUM_LAMPS = {
	1: "Jam Multiball", 2: "Super Targets", 3: "Super Lanes", 4: "Album Multiball", 5: "Cannon Fodder", 6: "Cannon Volley", 7: "Cannon Chaos", 8: "Rock Again",
	9: "Super Loops", 10: "Super Combo", 11: "Tour Multiball", 12: "Left outlane", 13: "Left return lane", 14: "2X", 17: "AC/DC last C", 18: "AC/DC D",
	19: "AC/DC slash", 20: "AC/DC first C", 21: "AC/DC A", 22: "Left-ramp standup (left)", 23: "Left-ramp standup (right)", 24: "TNT arrow (white)",
	25: "Lower mini-playfield loop arrow (left)", 32: "Train extra ball", 33: "ROCK K", 34: "ROCK C", 35: "ROCK O", 36: "ROCK R",
	37: "Lower mini-playfield loop arrow (right)", 38: "Special", 40: "Extra Ball", 41: "Right-ramp standup", 42: "3X", 43: "Right return lane", 44: "Right outlane",
	49: "TNT T (left)", 50: "TNT N", 51: "TNT T (right)", 53: "Jukebox horn (left)", 54: "Jukebox horn (right)", 57: "Start button",
	58: "Tournament start button", 59: "FIRE button red", 60: "FIRE button green", 61: "FIRE button blue", 62: "Left pop-bumper insert", 63: "Right pop-bumper insert", 64: "Bottom pop-bumper insert",
	65: "Track: You Shook Me All Night Long", 66: "Track: Highway to Hell", 67: "Track: Rock N Roll Train", 68: "Track: Whole Lotta Rosie",
	69: "Track: Hells Bells", 70: "Track: Thunderstruck", 71: "Track: Let There Be Rock", 72: "Track: Hell Ain't a Bad Place to Be",
	73: "Track: TNT", 74: "Track: For Those About to Rock", 75: "Track: War Machine", 76: "Track: Back in Black",
}

PRO_LAMPS = {
	1: "Start button", 2: "Tournament start button", 3: "Left outlane", 4: "Left return lane", 5: "2X", 6: "3X", 7: "Right return lane", 8: "Right outlane",
	9: "AC/DC last C", 10: "AC/DC D", 11: "AC/DC slash", 12: "AC/DC first C", 13: "AC/DC A", 14: "VPX playfield insert l14", 15: "VPX playfield insert l15", 17: "VPX playfield insert l17", 18: "Left-loop arrow (white)",
	19: "Left-ramp standup (left)", 20: "Left-ramp arrow (white)", 21: "Left-ramp standup (right)", 22: "TNT T (left)", 23: "TNT N", 24: "TNT T (right)",
	25: "TNT arrow (white)", 26: "Right-ramp arrow (white)", 27: "Extra Ball", 28: "Right-loop arrow (red / horns)", 29: "Right-loop arrow (white)",
	30: "ROCK R", 31: "ROCK O", 32: "ROCK C", 33: "ROCK K", 34: "Special", 35: "Bell arrow (red / horns)", 36: "Bell arrow (white)",
	37: "Left top lane", 38: "Center top lane", 39: "Right top lane", 40: "Tunes N Stuff", 41: "Jam Multiball", 42: "Super Targets",
	43: "Super Lanes", 44: "Album Multiball", 45: "Cannon Fodder", 46: "Cannon Volley", 47: "Cannon Chaos", 48: "Rock Again",
	49: "Tour Multiball", 50: "Super Combos", 51: "Super Loops", 52: "Left-loop arrow (red / horns)", 53: "Track: You Shook Me All Night Long",
	54: "Track: Highway to Hell", 55: "Track: Rock N Roll Train", 56: "Track: Whole Lotta Rosie", 57: "Jukebox horn (left)", 58: "Jukebox horn (right)",
	60: "Left pop-bumper insert", 61: "Right pop-bumper insert", 62: "Bottom pop-bumper insert", 63: "FIRE button", 64: "Right-ramp standup",
	65: "Track: Hells Bells", 66: "Track: Thunderstruck", 67: "Track: Back in Black", 68: "Track: War Machine",
	69: "Track: For Those About to Rock", 70: "Track: TNT", 71: "Track: Hell Ain't a Bad Place to Be", 72: "Track: Let There Be Rock",
}

EXTENDED_GROUPS = [
	(81, "Face mouth", "CN1"), (84, "Bell arrow (top)", "CN3"), (87, "Center top lane", "CN4"), (90, "Tunes N Stuff", "CN5"),
	(93, "Right loop arrow (mid)", "CN7"), (96, "Bell arrow (bottom)", "CN8"), (99, "Left top lane", "CN9"), (102, "Right ramp arrow", "CN11"),
	(105, "Left loop arrow (bottom)", "CN12"), (108, "Right loop arrow (bottom)", "CN13"), (111, "Left loop arrow (top)", "CN14"),
	(117, "Face right eye", "CN16"), (120, "Face left eye", "CN17"), (123, "Left ramp arrow", "CN18"), (126, "Right top lane", "CN19"),
]


def output_id(group: str, address: int, label: str) -> str:
	return f"output.{group}.{address}.{slug(label)}"


def output_record(address: int, label: str, kind: str, availability: str, group: str, sources: tuple[str, ...], manual_address: str | None = None, wiring: dict[str, object] | None = None, physical: dict[str, object] | None = None, pwm: bool = False) -> dict[str, object]:
	namespace = {"pinmame.output.solenoid": "pinmame.solenoid", "pinmame.output.lamp": "pinmame.lamp", "pinmame.output.gi": "pinmame.gi", "physical.output.ticket": "manual.service-output"}[group]
	result: dict[str, object] = {
		"id": output_id(group.rsplit(".", 1)[-1], address, label), "label": label, "kind": kind,
		"binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address),
		"availability": availability, "provenance": provenance(*sources),
	}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	if pwm:
		result["range"] = {"minimum": 0, "maximum": 255, "steps": 256}
	return result


def standard_lamp_wiring(address: int) -> dict[str, object]:
	row, column = divmod(address - 1, 8)
	return {"board": "I/O power-driver board lamp matrix", "driver_transistor": f"Q{33 + row}", "drive_connection": f"matrix column {row + 1}", "return_connection": f"matrix row {column + 1}", "nominal_voltage_v": 18, "voltage_type": "dc"}


def complete_outputs(variant: str, sources: tuple[str, ...]) -> list[dict[str, object]]:
	premium = variant == "premium"
	manual = LUCI_MANUAL if premium else PRO_MANUAL
	solenoids = PREMIUM_SOLENOIDS if premium else PRO_SOLENOIDS
	items: list[dict[str, object]] = []
	for address, (base_label, kind, availability, manual_address) in sorted(solenoids.items()):
		label = base_label
		if address in {33, 34, 35}:
			items.append(output_record(address, label, kind, availability, "physical.output.ticket", (manual,), manual_address, physical={"notes": "Optional physical ticket-dispenser service function. The stable LibPinMAME solenoid API does not expose this service identity."}))
			continue
		board = "Auxiliary 8-coil board" if address >= 51 else "I/O power-driver board"
		items.append(output_record(address, label, kind, availability, "pinmame.output.solenoid", sources if availability != "unused" else (manual,), manual_address, {"board": board, "driver_transistor": f"Q{manual_address}", "nominal_voltage_v": 20 if kind in {"flasher", "motor"} else 50, "voltage_type": "dc"}, pwm=kind in {"flasher", "motor", "magnet"}))
	items.append(output_record(33, "PinMAME SAM game-on state", "virtual", "used", "pinmame.output.solenoid", (CORE_SOURCE,), physical={"notes": "SAM_FASTFLIPSOL synthetic state used for low-latency flipper gating; not a physical I/O Power Driver transistor."}))
	lamp_labels = PREMIUM_LAMPS if premium else PRO_LAMPS
	for address in range(1, 81):
		used = address in lamp_labels
		label = lamp_labels.get(address, f"Unused lamp-matrix output #{address}")
		if variant == "vault" and address in {14, 15, 17}:
			used = False
			label = f"Removed Vault Edition insert #{address}"
		items.append(output_record(address, label, "lamp", "used" if used else "unused", "pinmame.output.lamp", sources if used else (manual,), str(address), standard_lamp_wiring(address)))
	items.append(output_record(0, "Conventional GI / game-on illumination channel", "gi", "used", "pinmame.output.gi", sources, "GI-0", {"board": "I/O power-driver board", "control_connection": "GI channel 0", "nominal_voltage_v": 6.3, "voltage_type": "ac"}))
	if not premium:
		return items
	extended: dict[int, tuple[str, str]] = {}
	for start, name, connector in EXTENDED_GROUPS:
		for offset, color in enumerate(("blue", "green", "red")):
			extended[start + offset] = (f"{name} RGB {color}", connector)
	for address in range(81, 129):
		if address in extended:
			label, connector = extended[address]
			items.append(output_record(address, label, "rgb_lamp", "used", "pinmame.output.lamp", sources, f"LED board {connector}", {"board": "LED board 520-5331-00", "drive_connection": connector, "nominal_voltage_v": 18, "voltage_type": "dc"}, {"notes": f"One {label.rsplit(' ', 1)[-1]} channel of a tri-color playfield LED."}, True))
		else:
			items.append(output_record(address, f"Unused extended lamp output #{address}", "lamp", "unused", "pinmame.output.lamp", (manual,), str(address), {"board": "LED board 520-5331-00"}))
	gi_lamps = {130: "Red wedge GI", 132: "Blue wedge GI", 134: "Lower mini-playfield GI", 136: "White wedge GI"}
	for address in range(129, 151):
		if address in gi_lamps:
			label = gi_lamps[address]
			items.append(output_record(address, label, "gi", "used", "pinmame.output.lamp", sources, f"extended {address}", {"board": "LED/GI control outputs", "control_connection": f"public lamp {address}", "nominal_voltage_v": 18, "voltage_type": "dc"}, pwm=True))
		else:
			items.append(output_record(address, f"Unused extended lamp output #{address}", "lamp", "unused", "pinmame.output.lamp", (manual,), str(address), {"board": "LED/GI control outputs"}))
	for address in range(151, 159):
		items.append(output_record(address, f"Highway to Hell flame-tunnel LED {address - 150}", "lamp", "used", "pinmame.output.lamp", sources, f"flame {address - 150}", {"board": "Flame-tunnel LED assembly", "drive_connection": f"LED {address - 150}", "nominal_voltage_v": 18, "voltage_type": "dc"}, pwm=True))
	for address in range(159, 161):
		items.append(output_record(address, f"Unused extended lamp output #{address}", "lamp", "unused", "pinmame.output.lamp", (manual,), str(address), {"board": "LED/GI control outputs"}))
	return items


def binding_map(devices: list[dict[str, object]]) -> dict[tuple[str, int], str]:
	return {(str(device["binding"]["group"]), int(device["binding"]["device"])): str(device["id"]) for device in devices}


def mechanisms(variant: str, inputs: list[dict[str, object]], outputs: list[dict[str, object]], sources: tuple[str, ...]) -> list[dict[str, object]]:
	premium = variant == "premium"
	by_binding = binding_map([*inputs, *outputs])
	def refs(group: str, *addresses: int) -> list[str]:
		return [by_binding[(group, address)] for address in addresses]
	def mech(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[dict[str, object]] | None = None) -> dict[str, object]:
		result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
		if positions:
			result["positions"] = positions
		return result
	result = [
		mech("mechanism.trough", "Four-ball trough", "kicker", refs("pinmame.output.solenoid", 1), refs("pinmame.input.switch", 18, 19, 20, 21, 22), "Create four balls on switches 18-21. Output 1 ejects the rightmost ball and the proven script pulses stack opto 22 when balls remain."),
		mech("mechanism.auto-launch", "Auto launcher", "kicker", refs("pinmame.output.solenoid", 2), refs("pinmame.input.switch", 23), "Switch 23 holds while a ball is in the auto-launch lane. Output 2 fires the impulse plunger; the working scripts use a 55-65 strength implementation-dependent impulse."),
		mech("mechanism.top-eject", "Jukebox / top eject", "kicker", refs("pinmame.output.solenoid", 12), refs("pinmame.input.switch", 37), "A ball closes switch 37 until output 12 ejects it. Premium code can PWM output 12 and the working table preserves the stronger super-skill-shot kick."),
		mech("mechanism.cannon", "Rotating cannon / gun", "rotary", refs("pinmame.output.solenoid", 32, 53 if premium else 3), refs("pinmame.input.switch", 45, 61, 62), "Switch 45 holds a captured ball. The motor sweeps from roughly 110 degrees home toward 20 degrees and back; switch 61 is home and switch 62 is the mid mark. The eject output launches at the current angle and clears switch 45.", [{"id": "position.home", "label": "Home", "sensors": refs("pinmame.input.switch", 61), "description": "Working scripts initialize near 110 degrees with switch 61 active."}, {"id": "position.mid", "label": "Mid mark", "sensors": refs("pinmame.input.switch", 62), "description": "Switch 62 becomes active as the cannon passes the ROM timing mark."}]),
		mech("mechanism.cannon-diverter", "Right-ramp cannon diverter", "diverter", refs("pinmame.output.solenoid", 55 if premium else 4), refs("pinmame.input.switch", 41, 43, 45), "The right-ramp diverter selects normal ramp travel or the cannon capture path. Recreate both physical routes; do not model it as a cosmetic gate."),
		mech("mechanism.right-control-gate", "Right control gate", "gate", refs("pinmame.output.solenoid", 56 if premium else 5), refs("pinmame.input.switch", 43, 59), "The controlled gate changes the right-ramp/right-orbit return path. The VPX script treats energized and released states as distinct collidable gate states."),
		mech("mechanism.main-flippers", "Main flippers", "other", refs("pinmame.output.solenoid", 15, 16), refs("pinmame.input.switch", 84, 83, 82, 81), "Two main flippers use dedicated button and normally-closed EOS contacts. PinMAME exposes the dedicated contacts in reverse-numbered public order."),
		mech("mechanism.pop-bumpers", "Three pop bumpers", "other", refs("pinmame.output.solenoid", 9, 10, 11), refs("pinmame.input.switch", 30, 31, 32), "Each bumper contact pulses its corresponding coil; keep the physical switch-to-coil order left, right, bottom."),
		mech("mechanism.slingshots", "Left and right slingshots", "other", refs("pinmame.output.solenoid", 13, 14), refs("pinmame.input.switch", 26, 27), "Each leaf switch pulses its corresponding slingshot coil."),
		mech("mechanism.spinner", "Loop spinner", "other", [], refs("pinmame.input.switch", 33), "Pulse switch 33 once for each spinner blade transition; do not hold it for a complete spin."),
	]
	if premium:
		result.extend([
			mech("mechanism.lower-playfield-eject", "Lower mini-playfield eject", "kicker", refs("pinmame.output.solenoid", 3), refs("pinmame.input.switch", 49), "A one-ball lower-playfield trough holds switch 49 until output 3 ejects it."),
			mech("mechanism.lower-playfield-flippers", "Lower mini-playfield flippers", "other", refs("pinmame.output.solenoid", 4, 5), refs("pinmame.input.switch", 88, 86), "The cabinet flipper buttons also close dedicated switches 88 and 86. Outputs 4 and 5 drive the two lower flippers independently of the main pair."),
			mech("mechanism.acdc-drop-bank", "AC/DC five-bank drop targets", "drop_target_bank", refs("pinmame.output.solenoid", 6), refs("pinmame.input.switch", 1, 2, 3, 4, 5), "Each target switch remains active while down. Output 6 raises all five targets together."),
			mech("mechanism.tnt-drop-bank", "TNT three-bank drop targets", "drop_target_bank", refs("pinmame.output.solenoid", 7), refs("pinmame.input.switch", 10, 11, 12), "Each target switch remains active while down. Output 7 raises all three targets together."),
			mech("mechanism.bell-eject", "Bell eject", "kicker", refs("pinmame.output.solenoid", 52), refs("pinmame.input.switch", 36), "Switch 36 holds a ball in the bell saucer until public output 52, physical auxiliary coil 42, ejects it."),
			mech("mechanism.swinging-bell", "Swinging bell with captive ball", "toy", refs("pinmame.output.solenoid", 54), refs("pinmame.input.switch", 47), "The bell carries a captive steel ball and must transfer playfield-ball momentum into pendulum motion. Switch 47 reports a score excursion; the working VPX closes it outside the settled angular region. Output 54 is a hidden magnet used by Hells Bells to start the swing."),
			mech("mechanism.left-ramp-diverter", "Left-ramp crossover diverter", "diverter", refs("pinmame.output.solenoid", 57), refs("pinmame.input.switch", 13, 14, 43), "The left-ramp diverter selects the normal left-ramp return or crossover toward the right-ramp route."),
			mech("mechanism.band-members", "Animated band-member display", "toy", refs("pinmame.output.solenoid", 51), [], "Public output 51, physical auxiliary coil 41, drives a timed rocking animation across the molded band figures; the script returns the linked members after the pulse."),
			mech("mechanism.detonator", "Detonator handle", "toy", refs("pinmame.output.solenoid", 18), refs("pinmame.input.switch", 46), "The standup target reports the player's hit on switch 46. Output 18 independently actuates the detonator handle animation."),
		])
	else:
		bell_label = "Passive swinging Hell's Bell" if variant in {"led-pro", "vault"} else "Hell's Bell standup target"
		bell_behavior = "A freely swinging pendulum with a captive ball closes switch 36 when struck; it has no controller actuator." if variant in {"led-pro", "vault"} else "A conventional standup target pulses switch 36; the original 2012 Pro has no swinging-bell mechanism."
		result.append(mech("mechanism.bell", bell_label, "toy" if variant in {"led-pro", "vault"} else "other", [], refs("pinmame.input.switch", 36), bell_behavior))
	return result


def relationships(variant: str, inputs: list[dict[str, object]], outputs: list[dict[str, object]], sources: tuple[str, ...]) -> list[dict[str, object]]:
	premium = variant == "premium"
	by_binding = binding_map([*inputs, *outputs])
	pairs = [
		("trough-eject-stack", 1, 22), ("auto-launch-lane", 2, 23), ("top-eject-release", 12, 37),
		("cannon-eject-release", 53 if premium else 3, 45),
	]
	if premium:
		pairs.extend([("lower-eject-release", 3, 49), ("bell-eject-release", 52, 36)])
	return [{
		"id": f"relationship.{name}", "kind": "pulse",
		"source": by_binding[("pinmame.output.solenoid", output_address)],
		"destination": by_binding[("pinmame.input.switch", switch_address)],
		"provenance": provenance(*sources),
	} for name, output_address, switch_address in pairs]


def driver_records(driver_ids: list[str], notes: str) -> list[dict[str, object]]:
	result: list[dict[str, object]] = []
	for driver_id in driver_ids:
		source = DRIVERS[driver_id]
		record: dict[str, object] = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = ("Colored-ROM modification only; native display colorization does not change physical I/O or mechanisms. " if driver_id.endswith("c") else "") + notes
		result.append(record)
	return result


COMMON_SOURCES = [
	{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/driver.c and generated exact driver catalog"},
	{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c AC/DC ROM declarations, clone lineage, SAM generation, auxiliary-output flags, public output mapping, and DMD topology"},
]
MANUAL_SOURCES = {
	PREMIUM_MANUAL: {"id": PREMIUM_MANUAL, "kind": "manual", "uri": "https://www.sternpinball.com/manuals/", "sha256": "d3de500b504b165023e3858883067ca518543307387ec2460397b740ebe240b6", "locator": "ACDC_Prem_web.pdf pages 16-24 and 42-59; local cache manufacturer.stern.d3de500b504b", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "ACDC_Prem_web.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T17:29:48.3213976Z"},
	LUCI_MANUAL: {"id": LUCI_MANUAL, "kind": "manual", "uri": "https://www.sternpinball.com/manuals/", "sha256": "65bb776389508259513cb72f4c24f054f97dfaa0eee87557a0f76e3175acf524", "locator": "ACDC_Luci_web.pdf pages 16-24 and 42-59; local cache manufacturer.stern.65bb77638950", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "ACDC_Luci_web.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T17:11:09.695917Z"},
	PRO_MANUAL: {"id": PRO_MANUAL, "kind": "manual", "uri": "https://www.sternpinball.com/manuals/", "sha256": "987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5", "locator": "ACDC_Pro_web.pdf pages 16-21 and major-assembly/wiring sections; local cache manufacturer.stern.987d42c68b58", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "ACDC_Pro_web.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-02T17:22:42.0568607Z"},
}
VPX_SOURCES = {
	PREMIUM_VPX: {"id": PREMIUM_VPX, "kind": "vpx_script", "uri": "https://github.com/vpinball/vpxtable_scripts", "revision": VPX_REVISION, "sha256": "b478b21272befd41908aa3ef4daf3a90d4838334346718cb4d5fde7f23bb2fc0", "locator": "AC-DC LUCI Premium VR (Stern 2013) v1.1.4.vbs; callbacks, initial state, routes, cannon, bell, diverters, lamps, and mechanism behavior", "license": "NOASSERTION", "attribution": "VPW table contributors credited in the script"},
	PRO_VPX: {"id": PRO_VPX, "kind": "vpx_script", "uri": "https://github.com/vpinball/vpxtable_scripts", "revision": VPX_REVISION, "sha256": "e0fdef84892ea8bce6eae179509ac8262f103bac0173c2e822a4fe10aafcf7fa", "locator": "AC-DC Pro-1.0 Lighting Bug Fix.vbs; exact Pro controller callbacks, ball devices, cannon positions, switch semantics, GI, lamps, and flashers", "license": "NOASSERTION", "attribution": "ninuzzu and credited AC/DC Pro table contributors"},
	PRO_TABLE: {"id": PRO_TABLE, "kind": "vpx_table", "uri": "local-evidence://vpx-table/acdc-pro-1.0", "sha256": "44bf3d67f96968103ab71f26b8b12786e5590f62bd73589b85060983dc62d9e9", "locator": "AC-DC Pro-1.0.vpx (78,274,560 bytes); cGameName=acd_170 and splash says AC/DC Pro (Stern 2012); 235 centered candidates; normalized bounds 0,0-952,2115; geometry-only shared original-Pro/LED-Pro evidence, not LED-Pro product identity", "license": "NOASSERTION", "attribution": "AC/DC Pro table contributors; geometry reviewed locally", "original_filename": "AC-DC Pro-1.0.vpx", "rights": "NOASSERTION"},
	VAULT_VPX: {"id": VAULT_VPX, "kind": "vpx_script", "uri": "https://github.com/vpinball/vpxtable_scripts", "revision": VPX_REVISION, "sha256": "88101e2184729f952d196fdfe5885f9d7e81ec211b7b1b675d724419fcb6a7f1", "locator": "AC-DC Pro Vault-1.0 Lighting Bug Fix.vbs; exact passive swinging-bell behavior at switch 36 and removed inserts 14, 15, and 17", "license": "NOASSERTION", "attribution": "ninuzzu and credited AC/DC Pro Vault table contributors"},
	VAULT_TABLE: {"id": VAULT_TABLE, "kind": "vpx_table", "uri": "https://vpuniverse.com/files/file/5489-acdc/", "sha256": "10a460c6b84fc1b8b372bf7b3d92b1904ee5eed9d5aad29fe384e7a6502fa328", "locator": "AC-DC Pro Vault-1.0.vpx (79,429,632 bytes); verified and extracted with vpxtool git:v0.33.3; normalized gameitem geometry and collection membership reviewed against manual pages 17, 19, 21, 42, and 48", "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "ninuzzu and credited AC/DC Pro Vault table contributors", "original_filename": "AC-DC Pro Vault-1.0.vpx"},
}
RUNTIME_SOURCES = {
	PREMIUM_RUNTIME: {"id": PREMIUM_RUNTIME, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/acd_170h/boot-start-premium-1.json", "sha256": "31d6c8a83091c62785ce5b23cb1417a12bfb229ed61b5366354451510e4940c0", "locator": "Exact acd_170h.zip SHA-256 1ace847619af4864769b053f641d3e035a1c72d517ac750af7088600cdd291d4; four-ball trough plus cannon-home initial state; boot, four credits, start, and observation", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
	PRO_RUNTIME: {"id": PRO_RUNTIME, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/acd_170/boot-start-pro-1.json", "sha256": "f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511", "locator": "Exact acd_170.zip SHA-256 e55c7386950272568dd639f3c8d70beff6fbd584ed49601d4196b46cb1e66ca5; four-ball trough plus cannon-home initial state; boot, four credits, start, and observation", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes are external"},
}
WEB_SOURCES = {
	STERN_PRODUCT: {"id": STERN_PRODUCT, "kind": "human_review", "uri": "https://sternpinball.com/game/ac-dc/", "locator": "Official edition feature inventory for Pro, Premium, and LUCI; reviewed 2026-08-02", "attribution": "Stern Pinball, Inc."},
	STERN_LED_PRO: {"id": STERN_LED_PRO, "kind": "service_bulletin", "uri": "https://sternpinball.com/2014/08/05/improved-ac-dc-pro-with-leds-and-swinging-bell/", "locator": "Official August 5, 2014 announcement proving LED Pro and newly designed swinging bell", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc."},
	IPDB_LUCI: {"id": IPDB_LUCI, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=6060", "locator": "AC/DC (LUCI Premium), December 2013; identity and notable-feature inventory reviewed in interactive browser"},
	IPDB_PREMIUM: {"id": IPDB_PREMIUM, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=5775", "locator": "AC/DC Premium identity and shared service-document association reviewed in interactive browser"},
}


def source_set(variant: str) -> list[dict[str, object]]:
	if variant == "premium":
		ids = [PREMIUM_MANUAL, LUCI_MANUAL, PREMIUM_VPX, PREMIUM_RUNTIME, STERN_PRODUCT, IPDB_PREMIUM, IPDB_LUCI]
	elif variant == "pro":
		ids = [PRO_MANUAL, PRO_TABLE, PRO_VPX, PRO_RUNTIME, STERN_PRODUCT]
	elif variant == "led-pro":
		ids = [PRO_MANUAL, PRO_TABLE, PRO_VPX, VAULT_VPX, VAULT_TABLE, PRO_RUNTIME, STERN_PRODUCT, STERN_LED_PRO]
	else:
		ids = [PRO_MANUAL, VAULT_VPX, VAULT_TABLE, PRO_RUNTIME, STERN_PRODUCT, STERN_LED_PRO]
	lookup = {**MANUAL_SOURCES, **VPX_SOURCES, **RUNTIME_SOURCES, **WEB_SOURCES}
	return [*COMMON_SOURCES, *(lookup[source_id] for source_id in ids)]


MACHINE_META = {
	"premium": {"id": "stern.ac-dc-premium-limited-edition-luci.2012", "name": "AC/DC Premium / Limited Edition / LUCI Premium", "manufacturer": "Stern", "year": 2012, "kind": "physical_pinball", "model_number": "500-55C7-01 / 500-55C8-01", "ipdb_id": 5775},
	"pro": {"id": "stern.ac-dc-pro.2012", "name": "AC/DC Pro (original)", "manufacturer": "Stern", "year": 2012, "kind": "physical_pinball", "model_number": "500-55C0-01"},
	"led-pro": {"id": "stern.ac-dc-led-pro.2014", "name": "AC/DC LED Pro", "manufacturer": "Stern", "year": 2014, "kind": "physical_pinball"},
	"vault": {"id": "stern.ac-dc-vault-edition.2018", "name": "AC/DC Vault Edition", "manufacturer": "Stern", "year": 2018, "kind": "physical_pinball"},
}
DRIVER_GROUPS = {"premium": PREMIUM_IDS, "pro": ORIGINAL_PRO_IDS, "led-pro": LED_PRO_IDS, "vault": VAULT_IDS}
VARIANT_NOTES = {
	"premium": "Firmware revision for the shared Premium/LE/LUCI playfield; cabinet art and trim packages do not change controller-facing I/O or mechanisms.",
	"pro": "Firmware revision intended for the original 2012 Pro playfield with a standup Hell's Bell target and no Premium auxiliary mechanisms.",
	"led-pro": "Firmware release paired with the 2014 LED Pro hardware: Pro playfield topology, factory LED lighting, and a passive swinging Hell's Bell at switch 36.",
	"vault": "Firmware release paired with the Vault Edition: passive swinging Hell's Bell and the Vault playfield's removal of inserts 14, 15, and 17.",
}


def build(variant: str) -> dict[str, object]:
	source_ids = {
		"premium": (PREMIUM_MANUAL, LUCI_MANUAL, PREMIUM_VPX, PREMIUM_RUNTIME),
		"pro": (PRO_MANUAL, PRO_VPX, PRO_RUNTIME),
		"led-pro": (PRO_MANUAL, PRO_VPX, VAULT_VPX, STERN_LED_PRO),
		"vault": (PRO_MANUAL, VAULT_VPX, PRO_RUNTIME),
	}[variant]
	inputs = complete_inputs(variant, source_ids)
	outputs = complete_outputs(variant, source_ids)
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 1, "machine": MACHINE_META[variant],
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "hardware_generation": "0x00000040", "inversion_applied_by_emulator": True},
		"drivers": driver_records(DRIVER_GROUPS[variant], VARIANT_NOTES[variant]),
		"inputs": inputs, "outputs": outputs,
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance(CORE_SOURCE, PREMIUM_RUNTIME if variant == "premium" else PRO_RUNTIME)}],
		"mechanisms": mechanisms(variant, inputs, outputs, source_ids),
		"relationships": relationships(variant, inputs, outputs, source_ids),
		"sources": source_set(variant),
		"knowledge": {"path": f"knowledge/stern/{MACHINE_META[variant]['id'].split('.', 1)[1].replace('.', '-')}.md", "status": "complete"},
	}
	if variant == "pro":
		apply_original_pro_spatial(
			inputs,
			outputs,
			table_source=PRO_TABLE,
			script_source=PRO_VPX,
			manual_source=PRO_MANUAL,
			core_source=CORE_SOURCE,
		)
		definition["schema_version"] = 2
		definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	elif variant == "led-pro":
		apply_led_pro_spatial(
			inputs,
			outputs,
			table_source=PRO_TABLE,
			script_source=PRO_VPX,
			manual_source=PRO_MANUAL,
			core_source=CORE_SOURCE,
			bell_table_source=VAULT_TABLE,
			bell_script_source=VAULT_VPX,
			identity_source=STERN_LED_PRO,
		)
		definition["schema_version"] = 2
		definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	elif variant == "vault":
		apply_vault_spatial(inputs, outputs, table_source=VAULT_TABLE, script_source=VAULT_VPX, manual_source=PRO_MANUAL, core_source=CORE_SOURCE)
		definition["schema_version"] = 2
		definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	return definition


KNOWLEDGE = {
	"premium": """# AC/DC Premium / Limited Edition / LUCI Premium recreation knowledge

## Identity and variants

This definition covers every in-scope h and hc PinMAME driver from 1.50 through 1.70 for the shared Stern Premium, Limited Edition, and LUCI Premium physical playfield. LUCI changes art and presentation; the LE trim packages and colored-ROM derivatives do not change controller-facing devices or mechanisms.

## Source precedence

The known-working VPW-derived LUCI 1.1.4 script is ground truth for public PinMAME addresses, callback routing, initial ball state, and mechanism causality. The exact Premium and LUCI manuals are authoritative for construction, wiring, assemblies, connector identities, and parts. Pinned PinMAME source defines the SAM transport, clone lineage, auxiliary-board translation, and 128x32 four-bit DMD. Manual geometric switch descriptions that disagree with the working script are retained as manual aliases/locators but do not override the proven table behavior.

## Ball inventory and startup

Create four trough balls and close switches 18, 19, 20, and 21. Leave stack opto 22 open until output 1 moves a ball through the eject end; the script pulses 22 when another ball remains. Initialize the cannon empty at home with switch 61 active and 62 inactive. The bell contains a captive steel ball that is part of its pendulum assembly, not a playable trough ball. The lower mini-playfield eject and both saucers start empty.

## Ball paths

Output 2 launches from switch 23. The main playfield includes left and right orbits, left and right ramps, three top lanes, the Jukebox/top saucer at switch 37, the bell eject at 36, and the cannon capture at 45. The right-ramp diverter routes a ball either through the normal ramp or into the cannon. The left-ramp diverter selects the ordinary return or crossover path. The lower mini-playfield has its own two flippers, three standups, two rollovers, and eject opto 49; output 3 returns its held ball.

## Custom mechanisms

The cannon motor sweeps a ball-holding cannon from about 110 degrees home toward 20 degrees and back. Switch 61 is home, switch 62 is the ROM timing mark, and public output 53 fires at the current angle. The swinging bell must transfer collision momentum into the captive ball and pendulum, report a score excursion on switch 47, and accept magnet output 54 during the Hells Bells feature. Public output 51 animates the linked band members. Output 18 actuates the detonator handle independently of target switch 46. Outputs 6 and 7 reset the five-bank AC/DC and three-bank TNT drop targets.

## Lamps and flashers

Standard lamps 1-80 are the manual matrix. Public lamps 81-128 are tri-color LED channels; each three-address group is blue, green, red as proven by the VPX script. Addresses 114-116 and 129 are unused. Color-GI channels 130, 132, 134, and 136 arrive through ChangedLamps and drive red, blue, lower-playfield, and white GI respectively; GI 0 remains a separate emulator-level channel. Flame-tunnel LEDs are 151-158. Local VPX array indices 177, 179, 180, 182, 183, and 185-190 are solenoid-flasher mirrors, not physical PinMAME lamp outputs, and must never be recreated as duplicate lamps.

## Auxiliary output translation

The manual's physical auxiliary coils 41-48 appear through LibPinMAME as public solenoids 51-58. Therefore physical 41 band members is public 51, physical 42 bell eject is 52, physical 43 cannon eject is 53, physical 44 bell magnet is 54, physical 45 right-ramp diverter is 55, physical 46 right control gate is 56, physical 47 left-ramp diverter is 57, and physical 48 is unused/public 58.

## Cabinet and service inputs

The main flipper buttons/EOS contacts are public switches 84/83 and 82/81. Lower mini-playfield buttons are public 88 and 86; 87 and 85 are unused. Matrix switch 64 is the FIRE button. Negative public switch addresses are the coin-door and tilt inputs after PinMAME inversion normalization; do not apply physical NC inversion twice.

PinMAME public solenoid 33 is the synthetic SAM game-on/fast-flip state and has no physical transistor. The manual's optional ticket-service identities 33-35 are retained separately under `physical.output.ticket`; the stable LibPinMAME solenoid API does not transport them.

## Timing and tuning

The working table's exact impulses are implementation evidence rather than universal geometry: auto-launch uses roughly 55 strength, bell eject 8, cannon eject 45, and the top eject has a special high-power PWM path for the super skill shot. Preserve the causal state changes first, then tune physical travel in the target engine while retaining the switch/output ordering.

## Evidence

- Official Premium manual SHA-256 d3de500b504b165023e3858883067ca518543307387ec2460397b740ebe240b6 and LUCI manual SHA-256 65bb776389508259513cb72f4c24f054f97dfaa0eee87557a0f76e3175acf524 are organized under E:/_vpe-2025/pinmame-manuals.
- Working LUCI script SHA-256 b478b21272befd41908aa3ef4daf3a90d4838334346718cb4d5fde7f23bb2fc0 comes from pinned vpxtable_scripts revision 0c036bb61b4b4e8c778c37559f6795df8cd1521e.
- Exact acd_170h boot/start evidence SHA-256 31d6c8a83091c62785ce5b23cb1417a12bfb229ed61b5366354451510e4940c0; ROM archive SHA-256 1ace847619af4864769b053f641d3e035a1c72d517ac750af7088600cdd291d4 remains external.
""",
	"pro": """# AC/DC Pro (original) recreation knowledge

## Identity and variants

This record is the original 2012 Pro playfield and owns non-h firmware revisions 1.21 through 1.65. Later 1.68 software is assigned to the separately documented 2014 LED Pro, and 1.70 to the Vault Edition. The split is intentional: the original has a conventional standup Hell's Bell target at switch 36, while the later products use a passive swinging bell.

## Ground truth and startup

The known-working AC/DC Pro 1.0 script is ground truth for PinMAME bindings and behavior; the Pro manual supplies wiring and construction. Initialize four trough balls on 18-21 and the empty cannon at home on switch 61. Output 1 ejects through stack opto 22, output 2 auto-launches from switch 23, and output 12 clears the Jukebox/top saucer at 37.

## Playfield and mechanisms

The Pro replaces Premium drop banks with standup AC/DC, ROCK, and TNT targets and omits the lower mini-playfield, bell saucer/magnet, band animation, detonator actuator, crossover diverter, and auxiliary 8-coil board. The motorized cannon still captures on 45, reports home 61 and mark 62, and fires through output 3. Output 4 selects the cannon route at the right ramp and output 5 controls the right gate. Three pops, two slings, two main flippers, top lanes, both ramps, both orbits, and spinner 33 complete the active playfield.

## Lamps and controller notes

Only the 1-80 lamp matrix and GI 0 are controller outputs. The service manual marks matrix positions 14, 15, 16, and 17 unused, but the proven Pro VPX script actively binds l14, l15, and l17 and the Vault script explicitly comments those same three bindings out as removed in the Vault Edition. Preserve 14, 15, and 17 as VPX-visible original/LED-Pro playfield inserts, preserve 16 as unused, and treat their artwork semantics as table-asset-defined rather than inventing manual names. The VPX script's 177-191 values are private flasher mirror indices fed by solenoid callbacks and are not lamps. Flashers remain solenoid outputs 17 and 20-31. Public dedicated flipper switches are 84/83 left and 82/81 right; lower-playfield dedicated slots are unused.

## Spatial reconstruction

Every playfield switch, effect, insert, flasher, and GI emitter has a reviewed normalized placement in VPX/player view (`x=0` left, `x=1` right, `y=0` rear, `y=1` apron). Coordinates come from the exact working `AC-DC Pro-1.0.vpx` table. The original standup target at switch 36 uses that table's target point rather than the different swinging-bell contact point used by LED Pro and Vault. Switches 18-22 describe the real under-apron trough order, while cannon switches 61 and 62 share one projected assembly center because their distinction is cam state rather than playfield position.

GI 0 has 38 normalized playfield emitter placements and physical quantity 45; the seven rear-panel GI bulbs are documented physically but receive no playfield coordinates. Rear-panel lamp addresses 53-56 and 65-72 and rear-panel flasher solenoid 22 likewise retain their physical quantity and construction notes while remaining spatially N/A. This keeps cabinet/rear-panel fixtures out of the normalized playfield plane without losing hardware needed to recreate the machine.

PinMAME public solenoid 33 is the synthetic SAM game-on/fast-flip state, not a Q33 ticket driver. Optional physical ticket-service identities 33-35 are preserved in the untransported `physical.output.ticket` group.

## Timing and service

The working script sweeps the cannon from roughly 110 degrees to 20 and back, asserts 62 at about 80 degrees, and will fire only before the cannon returns near home. Auto-launch uses an implementation impulse near 65 and the Jukebox eject uses the saucer route at switch 37. Keep these state boundaries; tune physical velocities to the target simulation.

## Evidence

- Official Pro manual SHA-256 987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5 is organized under E:/_vpe-2025/pinmame-manuals.
- Working Pro script SHA-256 e0fdef84892ea8bce6eae179509ac8262f103bac0173c2e822a4fe10aafcf7fa.
- Exact working `AC-DC Pro-1.0.vpx` SHA-256 44bf3d67f96968103ab71f26b8b12786e5590f62bd73589b85060983dc62d9e9; 78,274,560 bytes; verified and extracted with vpxtool. The source table is retained in the organized external VPX cache and is not redistributed by this repository.
- Exact acd_170 topology run SHA-256 f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511; ROM archive SHA-256 e55c7386950272568dd639f3c8d70beff6fbd584ed49601d4196b46cb1e66ca5 remains external.
""",
	"led-pro": """# AC/DC LED Pro recreation knowledge

Coverage: **author-ready - complete Pro-derived I/O, wiring, mechanisms, LED lighting, spatial dispositions, and product boundary validated**

## Identity

This is Stern's upgraded 2014 LED Pro production and it owns the 1.68 and 1.68 colored PinMAME drivers. The physical differences from the original Pro are all-LED lighting, a newly designed passive swinging Hell's Bell, and the modern metal/wood backbox and cabinet. The game's features, playfield art, and music remain otherwise unchanged. Stern's official August 5, 2014 announcement is the product-identity boundary.

## Recreation delta from original Pro

Use the complete original Pro switch, lamp, solenoid, cannon, ramp, trough, shooter, pop, sling, flipper, art, music, and game-feature contract. Replace the standup bell with a freely swinging captive-ball pendulum whose score contact is still public switch 36. There is no bell magnet or bell actuator; collision energy alone moves it. Retain the VPX-visible original Pro insert addresses 14, 15, and 17 even though the Pro service manual labels those matrix positions unused; the Vault script's explicit removal is the edition-delta evidence. Implement the factory all-LED lighting without changing the 1-80 PinMAME bindings.

## Spatial evidence and timing

The supplied AC-DC Pro VPX table is used only as shared original-Pro/LED-Pro geometry evidence: its `cGameName=acd_170` and splash identify it as AC/DC Pro (Stern 2012), so it does not establish LED Pro product identity. Its 235 centered candidates provide the normalized VPX/player-view geometry for the shared playfield, including active LED-Pro lamps 14, 15, and 17 and GI 0. The Pro script and manual supply the shared controller, wiring, and physical placement conventions. The exact Vault VPX table and script, together with Stern's LED Pro announcement, establish the passive swinging-bell contact at switch 36 and its 2014 product boundary. Cannon and ball-device timing remains as documented for the original Pro. Rear-panel lamp addresses 53-56 and 65-72, the seven rear-panel GI bulbs, and flasher solenoid 22 are physical fixtures with recorded quantities but intentionally have no normalized playfield coordinates.
""",
	"vault": """# AC/DC Vault Edition recreation knowledge

## Identity

This record covers the 2018 1.70 and 1.70 colored PinMAME drivers on the AC/DC Vault Edition physical product. It retains the Pro ball paths and passive swinging-bell product line but changes artwork and removes lamp inserts 14, 15, and 17.

## Ground truth and differences

The known-working AC/DC Pro Vault 1.0 script is ground truth. Switch 36 is a physical swinging-bell hit contact, not the original Pro's standup target. The bell has no controller actuator. Lamps 14, 15, and 17 are absent and explicitly unused; every other Pro switch, lamp, flasher, coil, trough, shooter, cannon, gate, ramp, orbit, pop, sling, flipper, and spinner binding is retained.

## Cannon and ball devices

Start four balls on trough switches 18-21 and the cannon at home on 61. Output 1 ejects, output 2 launches, output 12 clears Jukebox switch 37, output 4 routes into the cannon, output 32 rotates, and output 3 fires the ball held on 45. Switch 62 is the cannon timing mark. The right control gate is output 5.

## Spatial reconstruction

Every physical playfield switch, effect, insert, flasher, and GI emitter has a reviewed normalized placement in VPX/player view (`x=0` left, `x=1` right, `y=0` rear, `y=1` apron). Coordinates come from the exact working `AC-DC Pro Vault-1.0.vpx` table and were checked against the official switch, lamp, and coil location sheets. Switches 18-22 follow the real under-apron trough assembly from drain end to eject/jam end rather than collapsing onto the table's two simulated kicker objects. Cannon switches 61 and 62 share the rotating assembly's projected center because their physical contacts differ by cam state, not playfield position. Rear-panel lamp addresses 53-56 and 65-72 and rear-panel flasher solenoid 22 retain physical quantities and construction notes but intentionally have no normalized playfield coordinates.

Solenoid 25 has three emitter placements, one at each pop bumper. GI 0 has 38 normalized playfield emitter placements; its physical quantity is 45 because the back-panel parts diagram corroborates another seven bulbs that are intentionally left without playfield coordinates. Cosmetic reflection and desktop-render helper objects are not duplicate physical emitters. Cabinet/start/tournament/FIRE lamps, cabinet/service switches, the shaker, knocker, and optional ticket hardware are explicitly marked `cabinet_or_service` instead of being forced into playfield coordinates.

## Evidence

- Vault script SHA-256 88101e2184729f952d196fdfe5885f9d7e81ec211b7b1b675d724419fcb6a7f1.
- Exact working VPX SHA-256 10a460c6b84fc1b8b372bf7b3d92b1904ee5eed9d5aad29fe384e7a6502fa328; 79,429,632 bytes; verified and extracted with vpxtool git:v0.33.3. The source table is retained in the organized external VPX cache and is not redistributed by this repository.
- Official Pro manual SHA-256 987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5 supplies the unchanged base wiring.
- Exact acd_170 run SHA-256 f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511; exact ROM archive remains external.
""",
}


PREMIUM_LAMPS_SEEN = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 49, 50, 51, 53, 54, 57, 59, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 130, 132, 134, 136]
PRO_LAMPS_SEEN = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]


def runtime_evidence(premium: bool) -> dict[str, object]:
	driver_id = "acd_170h" if premium else "acd_170"
	raw_sha = "31d6c8a83091c62785ce5b23cb1417a12bfb229ed61b5366354451510e4940c0" if premium else "f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511"
	rom_sha = "1ace847619af4864769b053f641d3e035a1c72d517ac750af7088600cdd291d4" if premium else "e55c7386950272568dd639f3c8d70beff6fbd584ed49601d4196b46cb1e66ca5"
	machine_ids = [MACHINE_META["premium"]["id"]] if premium else [MACHINE_META["pro"]["id"], MACHINE_META["led-pro"]["id"], MACHINE_META["vault"]["id"]]
	return {
		"format": "pinmame-machine-evidence", "version": 1, "extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": f"external:pinmame-game-code/{driver_id}/harness", "sha256": raw_sha, "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"},
		"driver_ids": [driver_id], "machine_ids": machine_ids, "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
		"runtime": {
			"game": driver_id, "rom_archive_sha256": rom_sha,
			"raw_runs": [{"name": "boot-start", "sha256": raw_sha, "self_test_pulses": 0}],
			"command_template": f"python tools/run_pinmame_harness.py --library <libpinmame> --game {driver_id} --rom-path <roms> --work-dir <isolated-state> --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --initial-switch 61 --pulse 65 --pulse 65 --pulse 65 --pulse 65 --pulse 16 --output <external-json>",
			"observations": {"lamp_addresses_seen": PREMIUM_LAMPS_SEEN if premium else PRO_LAMPS_SEEN, "gi_addresses_seen": [0], "solenoid_addresses_seen": [24, 33], "display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}]},
		},
	}


for stale in [
	ROOT / "machines/partial/stern/ac-dc-luci-premium-2013.json",
	ROOT / "machines/partial/stern/ac-dc-pro-2012.json",
	ROOT / "knowledge/stern/ac-dc-luci-premium-2013.md",
	ROOT / "knowledge/stern/ac-dc-premium-limited-edition-luci.2012.md",
	ROOT / "knowledge/stern/ac-dc-pro.2012.md",
	ROOT / "knowledge/stern/ac-dc-led-pro.2014.md",
	ROOT / "knowledge/stern/ac-dc-vault-edition.2018.md",
	ROOT / "machines/partial/stern/ac-dc-led-pro-2014.json",
	ROOT / "machines/partial/stern/ac-dc-vault-edition-2018.json",
]:
	if stale.exists():
		stale.unlink()

PATHS = {
	"premium": ROOT / "machines/partial/stern/ac-dc-premium-limited-edition-luci-2012.json",
	"pro": ROOT / "machines/author-ready/stern/ac-dc-pro-2012.json",
	"led-pro": ROOT / "machines/author-ready/stern/ac-dc-led-pro-2014.json",
	"vault": ROOT / "machines/author-ready/stern/ac-dc-vault-edition-2018.json",
}
for variant, path in PATHS.items():
	definition = build(variant)
	output_path = spatial_partial_path(path) if definition["machine"]["id"] in SPATIAL_RETROFIT_PENDING_MACHINE_IDS else path
	write_json(output_path, fail_closed_spatial_partial(definition))
	knowledge_path = ROOT.joinpath(*str(definition["knowledge"]["path"]).split("/"))
	write_text(knowledge_path, fail_closed_spatial_knowledge(definition["machine"]["id"], KNOWLEDGE[variant]))

write_json(ROOT / "evidence/runtime/sam/ac-dc-premium-boot-start.json", runtime_evidence(True))
write_json(ROOT / "evidence/runtime/sam/ac-dc-pro-boot-start.json", runtime_evidence(False))
