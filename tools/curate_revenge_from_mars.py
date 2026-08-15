from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = "pinmame.catalog.8371478a7640"
CORE_SOURCE = "pinmame.core.8371478a7640"
MANUAL_SOURCE = "manual.rfm.operations-1999"
REJECTED_VPX_SOURCE = "vpx-table.attack-and-revenge-v600-rejected"
MANUAL_SHA256 = "6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df"
MANUAL_EXCERPT = "evidence/excerpts/bally.revenge-from-mars.1999/operations-manual-service-tables.md"
MANUAL_EXCERPT_SHA256 = "e283b2b47f41ebe5c5464d2cda49df531d069dc57db8e91f29c12c9ef90c663b"
REJECTED_VPX_SHA256 = "9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be"
DEFINITION_PATH = ROOT / "machines/partial/bally/revenge-from-mars-1999.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/revenge-from-mars-1999.md"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def provenance(*source_refs: str, status: str = "validated") -> dict[str, object]:
	return {"status": status, "source_refs": list(source_refs)}


def aliases(namespace: str, value: int, manual_value: str) -> list[dict[str, str]]:
	return [
		{"namespace": namespace, "value": str(value)},
		{"namespace": "manual.address", "value": manual_value},
	]


def parse_numbered_names(value: str) -> dict[int, str]:
	result: dict[int, str] = {}
	for line in value.strip().splitlines():
		number, label = line.split("|", 1)
		result[int(number)] = label
	return result


SWITCH_NAMES = parse_numbered_names("""
11|Right Ramp Entrance
12|Left Ramp Exit
13|Start Button
15|Drop Target Down
16|Left Outlane
17|Right Return Lane
18|Shooter Lane
23|Launch Button
25|Left Loop (Low)
26|Left Return Lane
27|Right Outlane
28|Right Ramp Exit
31|Center Loop Reed (Bottom)
32|Center Loop Reed (Top)
33|Center Target 4
34|Center Target 3
35|Center Target 2
36|Center Target 1
37|Martian Target 4 (Center)
38|Up/Down Ramp Up
41|Trough Jam
42|Trough Ball 1
43|Trough Ball 2
44|Trough Ball 3
45|Trough Ball 4
46|Right Popper
47|Jet Exit
51|Right Lockup 1
52|Left Ramp Entrance
53|Trough Ball 5
54|Trough Ball 6
55|Right Lockup 2
56|Right Lockup 3
61|Left Slingshot
62|Right Slingshot
63|Left Jet
64|Right Jet
65|Bottom Jet
67|Right Loop (Low)
68|Right Loop (High)
71|Martian Target 3 (Left Top)
72|Martian Target 2 (Left Mid.)
73|Martian Target 1 (Left Bot.)
74|Center Loop Rollover
75|Center Deflector Panel
76|Right Top Lane
77|Left Top Lane
78|Left Loop (High)
85|Martian Target 7 (Right Bot.)
86|Martian Target 6 (Right Mid.)
87|Martian Target 5 (Right Top)
91|Left Coin Slot
92|Center Coin Slot
93|Right Coin Slot
94|4th Coin Option
101|Escape Button
102|Down Button
103|Up Button
104|Enter Button
105|Right Flipper EOS
106|Left Flipper EOS
111|Slam Tilt
112|Coin Door Closed
113|Plumb Bob Tilt
115|Right Flipper Button
116|Left Flipper Button
117|Right Action Button
118|Left Action Button
""")

OPTIONAL_SWITCHES = {53, 54, 55, 56}
OPTO_SWITCHES = {41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56}
REED_SWITCHES = {31, 32}
CABINET_OR_SERVICE_SWITCHES = set(range(91, 119))

MATRIX_COLUMN_WIRING = [
	("GRN-BRN", "J116-1", "U45-18"),
	("GRN-RED", "J116-2", "U45-17"),
	("GRN-ORG", "J116-3", "U45-16"),
	("GRN-WHT", "J116-4", "U45-15"),
	("GRN-BLK", "J116-5", "U45-14"),
	("GRN-BLU", "J116-6", "U45-13"),
	("GRN-VIO", "J116-7", "U45-12"),
	("GRN-GRY", "J116-8", "U45-11"),
]
MATRIX_ROW_WIRING = [
	("WHT-BRN", "J116-12", "U51-7"),
	("WHT-RED", "J116-13", "U51-5"),
	("WHT-ORG", "J116-14", "U51-9"),
	("WHT-YEL", "J116-15", "U51-11"),
	("WHT-GRN", "J116-16", "U57-7"),
	("WHT-BLU", "J116-17", "U57-5"),
	("WHT-VIO", "J116-18", "U57-9"),
	("WHT-GRY", "J116-19", "U57-11"),
]

DIRECT_WIRING = {
	1: ("ORN-BRN", "J114-1", "U43-7", "J114-14"),
	2: ("ORN-RED", "J114-2", "U43-5", "J114-14"),
	3: ("ORN-BLK", "J114-3", "U43-9", "J114-14"),
	4: ("ORN-YEL", "J114-4", "U43-11", "J114-14"),
	5: ("ORN-GRN", "J114-5", "U48-7", "J114-14"),
	6: ("ORN-BLU", "J114-6", "U48-5", "J114-14"),
	7: ("ORN-VIO", "J114-8", "U48-9", "J114-14"),
	8: ("ORN-GRY", "J114-9", "U48-11", "J114-14"),
	9: ("GRY-BLK", "J114-10", "U50-7", "J114-14"),
	10: ("GRY-ORG", "J114-11", "U50-5", "J114-14"),
	11: ("GRY-RED", "J114-12", "U50-9", "J114-14"),
	12: ("GRY-BRN", "J114-13", "U50-11", "J114-14"),
	13: ("BLK-GRN", "J115-9", "U56-7", "J115-22"),
	14: ("BLK-BLU", "J115-10", "U56-5", "J115-22"),
	15: ("BLK-VIO", "J115-20", "U56-9", "J115-22"),
	16: ("BLK-GRY", "J115-21", "U56-11", "J115-22"),
	17: ("BLK-BRN", "J113-1", "U49-7", "J113-10"),
	18: ("BLK-RED", "J113-2", "U49-5", "J113-10"),
	19: ("BLK-ORG", "J113-3", "U49-9", "J113-10"),
	20: ("BLK-YEL", "J113-4", "U49-11", "J113-10"),
	21: ("BLK-GRN", "J113-6", "U55-7", "J113-10"),
	22: ("BLK-BLU", "J113-7", "U55-5", "J113-10"),
	23: ("BLK-VIO", "J113-8", "U55-9", "J113-10"),
	24: ("BLK-GRY", "J113-9", "U55-11", "J113-10"),
}


def direct_number(public_address: int) -> int:
	if 91 <= public_address <= 98:
		return public_address - 90
	if 101 <= public_address <= 108:
		return public_address - 92
	if 111 <= public_address <= 118:
		return public_address - 94
	raise ValueError(public_address)


def input_switch_type(address: int) -> str:
	if address in OPTO_SWITCHES:
		return "opto"
	if address in REED_SWITCHES:
		return "reed"
	if address in {13, 23, 91, 92, 93, 94, 101, 102, 103, 104, 115, 116, 117, 118}:
		return "button"
	if address in {111, 113}:
		return "tilt"
	return "unknown"


def input_roles(address: int) -> list[str]:
	return {
		13: ["cabinet.start"],
		23: ["cabinet.launch"],
		91: ["cabinet.coin.1"],
		92: ["cabinet.coin.2"],
		93: ["cabinet.coin.3"],
		94: ["cabinet.coin.4"],
		101: ["service.escape"],
		102: ["service.down"],
		103: ["service.up"],
		104: ["service.enter"],
		111: ["cabinet.slam-tilt"],
		112: ["cabinet.coin-door"],
		113: ["cabinet.tilt"],
		115: ["cabinet.flipper.right"],
		116: ["cabinet.flipper.left"],
		117: ["cabinet.action.right"],
		118: ["cabinet.action.left"],
	}.get(address, [])


def build_inputs() -> list[dict[str, object]]:
	addresses = [column * 10 + row for column in range(1, 9) for row in range(1, 9)]
	addresses += list(range(91, 99)) + list(range(101, 109)) + list(range(111, 119))
	result: list[dict[str, object]] = []
	for address in addresses:
		label = SWITCH_NAMES.get(address, f"Unused input {address}")
		availability = "optional" if address in OPTIONAL_SWITCHES else "used" if address in SWITCH_NAMES else "unused"
		manual_address = str(address)
		if address >= 91:
			manual_address = f"D{direct_number(address)}"
		item: dict[str, object] = {
			"id": f"switch.{address}.{slug(label)}",
			"label": label,
			"kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": address},
			"aliases": aliases("pinmame.switch", address, manual_address),
			"availability": availability,
			"physical": {
				"switch_type": input_switch_type(address),
				"location": label if availability != "unused" else f"Unpopulated manual position {manual_address}",
			},
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
		if address in OPTO_SWITCHES:
			item["normally_closed"] = True
		roles = input_roles(address)
		if roles:
			item["roles"] = roles
		if address < 90:
			column = address // 10
			row = address % 10
			column_wire, column_connection, column_component = MATRIX_COLUMN_WIRING[column - 1]
			row_wire, row_connection, row_component = MATRIX_ROW_WIRING[row - 1]
			item["wiring"] = {
				"board": "Pinball 2000 power driver board",
				"control_wire": column_wire,
				"control_connection": f"{column_connection} ({column_component})",
				"return_wire": row_wire,
				"return_connection": row_connection,
				"return_component": row_component,
			}
		else:
			direct = direct_number(address)
			wire, connection, receiver, ground = DIRECT_WIRING[direct]
			item["wiring"] = {
				"board": "Pinball 2000 power driver board",
				"drive_wire": wire,
				"drive_connection": f"{connection} ({receiver})",
				"return_wire": "BLK",
				"return_connection": ground,
			}
		if availability == "unused":
			item["spatial"] = {"status": "not_applicable", "reason": "unused", "provenance": provenance(MANUAL_SOURCE)}
		elif address in CABINET_OR_SERVICE_SWITCHES or address in {13, 23}:
			item["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(MANUAL_SOURCE)}
		result.append(item)
	return result


COIL_NAMES = parse_numbered_names("""
1|Left Martian
2|Right Martian
3|Jet Exit Post
4|Right Gate
5|Left Gate
6|Drop Target Down
7|Drop Target Up
8|Right Popper
9|Trough Eject
10|Left Slingshot
11|Right Slingshot
12|Left Jet
13|Right Jet
14|Bottom Jet
15|Autoplunger
16|Right Lockup
17|Center Arrow Flasher
18|Knocker (Optional)
19|Shaker (Optional)
22|Right Popper Flasher
23|Left Arch Flasher
25|Right Arch Flasher
26|Left Martian Flasher
27|Right Martian Flasher
28|Attack Mars Flasher
33|Right Flipper Power
34|Right Flipper Hold
35|Left Flipper Power
36|Left Flipper Hold
37|Lock Diverter Power
38|Lock Diverter Hold
39|Up/Down Ramp Power
40|Up/Down Ramp Hold
48|Ticket Dispenser (Optional)
""")

COIL_PARTS = {
	1: "AE1-26-1500", 2: "AE1-26-1500", 3: "AE1-26-1500", 4: "A-14406", 5: "A-14406",
	6: "SM1-26-600", 7: "AE1-26-1200", 8: "AE1-25-1000", 9: "AE1-26-1500",
	10: "AE1-26-1200", 11: "AE1-26-1200", 12: "AE1-26-1200", 13: "AE1-26-1200",
	14: "AE1-26-1200", 15: "AE1-23-800", 16: "AE1-23-800", 17: "#906", 18: "AE-26-1200 kit",
	22: "#906", 23: "#89", 25: "#89", 26: "#89", 27: "#89", 28: "#906",
	33: "FL1-11629", 34: "FL1-11629", 35: "FL1-11629", 36: "FL1-11629",
	37: "FL1-22241", 38: "FL1-22241", 39: "FL1-11753", 40: "FL1-11753",
}

COIL_WIRING = {
	1: ("Q59", "J110-13", "VIO-BRN", "J102-1", "RED-BRN"),
	2: ("Q60", "J110-14", "VIO-RED", "J102-1", "RED-BRN"),
	3: ("Q61", "J110-15", "VIO-ORG", "J102-1", "RED-BRN"),
	4: ("Q62", "J110-16", "VIO-YEL", "J102-1", "RED-BRN"),
	5: ("Q63", "J110-17", "VIO-GRN", "J102-2", "RED-BLK"),
	6: ("Q64", "J110-18", "VIO-BLU", "J102-2", "RED-BLK"),
	7: ("Q65", "J110-19", "VIO-BLK", "J102-2", "RED-BLK"),
	8: ("Q66", "J110-20", "VIO-GRY", "J102-2", "RED-BLK"),
	9: ("Q51", "J112-11", "BRN-BLK", "J102-3", "RED-ORG"),
	10: ("Q52", "J112-12", "BRN-RED", "J102-3", "RED-ORG"),
	11: ("Q53", "J112-13", "BRN-ORG", "J102-3", "RED-ORG"),
	12: ("Q54", "J112-14", "BRN-YEL", "J102-3", "RED-ORG"),
	13: ("Q55", "J112-15", "BRN-GRN", "J102-7", "RED-YEL"),
	14: ("Q56", "J112-16", "BRN-BLU", "J102-7", "RED-YEL"),
	15: ("Q57", "J112-17", "BRN-VIO", "J102-7", "RED-YEL"),
	16: ("Q58", "J112-18", "BRN-GRY", "J102-7", "RED-YEL"),
	17: ("Q43", "J110-1", "BLU-BRN", "J102-8", "RED-WHT"),
	18: ("Q44", "J110-2", "BLU-RED", "", ""),
	19: ("Q45", "J110-3", "BLU-ORG", "", ""),
	20: ("Q46", "J110-4", "BLU-YEL", "", ""),
	21: ("Q47", "J110-5", "BLU-GRN", "", ""),
	22: ("Q48", "J110-6", "BLU-BLK", "J102-8", "RED-WHT"),
	23: ("Q49", "J110-7", "BLU-VIO", "J102-8", "RED-WHT"),
	24: ("Q50", "J110-8", "BLU-GRY", "", ""),
	25: ("Q67", "J112-9", "BLK-BRN", "J102-8", "RED-WHT"),
	26: ("Q68", "J112-10", "BLK-RED", "J102-8", "RED-WHT"),
	27: ("Q69", "J112-19", "BLK-ORG", "J102-8", "RED-WHT"),
	28: ("Q70", "J112-20", "BLK-YEL", "J102-8", "RED-WHT"),
	33: ("Q35", "J112-1", "YEL-GRN", "J103-1", "RED-GRN"),
	34: ("Q36", "J112-2", "ORG-GRN", "J103-1", "RED-GRN"),
	35: ("Q37", "J112-3", "YEL-BLU", "J103-2", "RED-BLU"),
	36: ("Q38", "J112-4", "ORG-BLU", "J103-2", "RED-BLU"),
	37: ("Q39", "J112-5", "YEL-VIO", "J103-3", "RED-VIO"),
	38: ("Q40", "J112-6", "ORG-VIO", "J103-3", "RED-VIO"),
	39: ("Q41", "J112-7", "YEL-GRY", "J103-4", "RED-GRY"),
	40: ("Q42", "J112-8", "ORG-GRY", "J103-4", "RED-GRY"),
}

FLASHERS = {17, 22, 23, 25, 26, 27, 28}
OPTIONAL_DRIVERS = {18, 19, 48}


def public_solenoid(driver: int) -> int:
	if driver <= 32:
		return driver
	if driver <= 36:
		return driver + 12
	return driver + 14


def build_outputs() -> list[dict[str, object]]:
	result: list[dict[str, object]] = []
	for driver in range(1, 49):
		public = public_solenoid(driver)
		label = COIL_NAMES.get(driver, f"Unused driver {driver}")
		availability = "optional" if driver in OPTIONAL_DRIVERS else "used" if driver in COIL_NAMES else "unused"
		if driver in FLASHERS:
			kind = "flasher"
		elif driver in {19, 48}:
			kind = "motor"
		elif availability == "unused":
			kind = "virtual"
		else:
			kind = "coil"
		item: dict[str, object] = {
			"id": f"driver.{driver}.{slug(label)}",
			"label": label,
			"kind": kind,
			"binding": {"group": "pinmame.output.solenoid", "device": public},
			"aliases": aliases("pinmame.solenoid", public, str(driver)),
			"availability": availability,
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE) if driver <= 40 else provenance(CORE_SOURCE),
		}
		physical: dict[str, object] = {"location": label}
		if part := COIL_PARTS.get(driver):
			physical["part_number"] = part
		if driver == 18:
			physical["notes"] = "Aftermarket knocker kit; the factory manual marks driver 18 unused."
		elif driver == 19:
			physical["notes"] = "Aftermarket shaker-motor kit; the factory manual marks driver 19 unused."
		elif driver == 48:
			physical["notes"] = "Optional ticket-dispenser output named by the game device table; not normally fitted to a pinball cabinet."
		item["physical"] = physical
		if driver in COIL_WIRING:
			transistor, connection, wire, power_connection, power_wire = COIL_WIRING[driver]
			wiring: dict[str, object] = {
				"board": "Pinball 2000 power driver board",
				"driver_transistor": transistor,
				"drive_connection": connection,
				"drive_wire": wire,
			}
			if power_connection:
				wiring["power_connection"] = power_connection
				wiring["power_wire"] = power_wire
			item["wiring"] = wiring
		if availability == "unused":
			item["spatial"] = {"status": "not_applicable", "reason": "unused", "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE) if driver <= 40 else provenance(CORE_SOURCE)}
		elif driver in OPTIONAL_DRIVERS:
			item["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE_SOURCE)}
		result.append(item)
	result.extend(build_lamps())
	return result


LAMP_NAMES = parse_numbered_names("""
2|Start Button
4|Right Top Lane
5|Left Top Lane
6|Martian Target 4 (Center)
7|Center Loop Arrow
8|Secret Weapon
9|Tower Struggle
10|Center Saucer Beam (Left)
11|Question Mark
12|Center Saucer Beam (Right)
13|Drive-In Demolition
14|Paris In Peril
15|Right Slingshot Spotlight
16|Tickets Low
18|Launch Button
19|Coin Door Illumination
20|Mothership Multiball (Right)
21|Mothership Multiball (Left)
22|Left Return Lane
23|Left Outlane
24|Big-O-Beam
25|Right Saucer Beam (Left)
26|Weapons
27|Saucer
28|Fuel
29|Left Saucer Beam (Right)
30|Center Saucer Beam (Center)
31|Left Slingshot Spotlight
36|Left Drain To Trough
37|Right Drain To Trough
38|Right Return Lane
39|Right Outlane
40|Mars Kneads Women
41|Right Saucer Beam (Right)
42|Saucer Rim 9 (Right)
43|Saucer Rim 8
44|Saucer Rim 7
45|Saucer Rim 6
46|Saucer Rim 5
48|Right Popper Arrow
49|Extra Ball
50|Martian Attack
51|Stroke Of Luck
52|Left Side Spotlight
53|Center Arrow
54|Right Martian (High)
55|Right Martian (Low)
56|Martian Happy Hour
57|Alien Abduction
58|Left Saucer Beam (Left)
59|Saucer Rim 1 (Left)
60|Saucer Rim 2
61|Saucer Rim 3
62|Saucer Rim 4
64|Multiball
65|Capture 2
66|Capture 1
67|Capture Zone Active
68|Shoot Again
69|Behind Center Targets
70|Upper Right Corner (Middle)
72|Right Loop Arrow
73|Right Loop Circle
74|Right Ramp Arrow
75|Right Ramp Circle
76|Left Loop Arrow
77|Left Ramp Arrow
78|Left Loop Circle
79|Left Ramp Circle
80|Shooter Lane 9 (Top)
81|Under Right Ramp (Low)
82|Under Right Ramp (High)
83|Upper Right Corner (Low)
84|Right Arch (Right)
85|Right Arch (Left)
86|Left Arch (Right)
87|Left Arch (Left)
88|Martian Target 5 (Right Top)
89|Martian Target 6 (Right Mid.)
90|Martian Target 7 (Right Bot.)
91|Martian Target 3 (Left Top)
92|Martian Target 2 (Left Mid.)
93|Martian Target 1 (Left Bot.)
94|Right Martian Eye
95|Left Martian Eye
96|Left Side 1 (Bottom)
97|Left Side 2
98|Left Side 3
99|Left Side 4 (Top)
100|Under Left Ramp (Bottom)
101|Under Left Ramp (Top)
102|Between Left/Bottom Jets
103|Upper Left Corner
104|Bottom Jet Bumper
106|Left Jet Bumper
107|Left of Left Top Lane
108|Between Upper/Right Top Lanes
109|Right of Right Top Lane
110|Top of Center Loop
111|Upper Right Corner (High)
112|Right Slingshot (Bottom)
113|Right Slingshot (Saucer)
114|Right Return Lane (Right)
115|Right Return Lane (Left)
116|Left Return Lane (Right)
117|Left Return Lane (Left)
118|Left Slingshot (Saucer)
119|Left Slingshot (Bottom)
120|Shooter Lane 1 (Bottom)
121|Shooter Lane 2
122|Shooter Lane 3
123|Shooter Lane 4
124|Shooter Lane 5
125|Shooter Lane 6
126|Shooter Lane 7
127|Shooter Lane 8
""")

LAMP_COLUMN_WIRING = {
	"A": [("YEL-BRN", "J108-9", "Q5"), ("YEL-RED", "J108-10", "Q9"), ("YEL-ORG", "J108-11", "Q13"), ("YEL-BLK", "J108-12", "Q17"), ("YEL-GRN", "J108-13", "Q21"), ("YEL-BLU", "J108-14", "Q25"), ("YEL-VIO", "J108-15", "Q29"), ("YEL-GRY", "J108-16", "Q33")],
	"B": [("YEL-BRN", "J107-10", "Q6"), ("YEL-RED", "J107-11", "Q10"), ("YEL-ORG", "J107-12", "Q14"), ("YEL-BLK", "J107-13", "Q18"), ("YEL-GRN", "J107-14", "Q22"), ("YEL-BLU", "J107-15", "Q26"), ("YEL-VIO", "J107-16", "Q30"), ("YEL-GRY", "J107-17", "Q34")],
}
LAMP_ROW_WIRING = {
	"A": [("BRN-BLK", "J108-1", "Q3"), ("BRN-RED", "J108-2", "Q7"), ("BRN-ORG", "J108-3", "Q11"), ("BRN-YEL", "J108-4", "Q15"), ("BRN-GRN", "J108-5", "Q19"), ("BRN-BLU", "J108-6", "Q23"), ("BRN-VIO", "J108-7", "Q27"), ("BRN-GRY", "J108-8", "Q31")],
	"B": [("RED-BRN", "J107-1", "Q4"), ("RED-BLK", "J107-2", "Q8"), ("RED-ORG", "J107-3", "Q12"), ("RED-YEL", "J107-4", "Q16"), ("RED-GRN", "J107-5", "Q20"), ("RED-BLU", "J107-6", "Q24"), ("RED-VIO", "J107-7", "Q28"), ("RED-GRY", "J107-8", "Q32")],
}
CABINET_LAMPS = {2, 16, 18, 19}


def lamp_manual_address(address: int) -> tuple[str, int, int]:
	column = address // 16 + 1
	within = address % 16
	bank = "A" if within < 8 else "B"
	row = within + 1 if bank == "A" else within - 7
	return f"{column}{row}{bank}", column, row


def build_lamps() -> list[dict[str, object]]:
	result: list[dict[str, object]] = []
	for address in range(128):
		manual_address, column, row = lamp_manual_address(address)
		bank = manual_address[-1]
		label = LAMP_NAMES.get(address, f"Unused lamp {manual_address}")
		availability = "used" if address in LAMP_NAMES else "unused"
		column_wire, column_connection, transistor = LAMP_COLUMN_WIRING[bank][column - 1]
		row_wire, row_connection, return_component = LAMP_ROW_WIRING[bank][row - 1]
		item: dict[str, object] = {
			"id": f"lamp.{address}.{slug(label)}",
			"label": label,
			"kind": "lamp",
			"binding": {"group": "pinmame.output.lamp", "device": address},
			"aliases": aliases("pinmame.lamp", address, manual_address),
			"availability": availability,
			"physical": {"location": label if availability == "used" else f"Unpopulated manual cell {manual_address}", "notes": f"Manual lamp-matrix position {manual_address}."},
			"wiring": {
				"board": "Pinball 2000 power driver board",
				"driver_transistor": transistor,
				"control_wire": column_wire,
				"control_connection": column_connection,
				"return_wire": row_wire,
				"return_connection": row_connection,
				"return_component": return_component,
			},
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
		if availability == "unused":
			item["spatial"] = {"status": "not_applicable", "reason": "unused", "provenance": provenance(MANUAL_SOURCE)}
		elif address in CABINET_LAMPS:
			item["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(MANUAL_SOURCE)}
		result.append(item)
	return result


def device_id(group: str, address: int, devices: list[dict[str, object]]) -> str:
	return next(str(device["id"]) for device in devices if device["binding"] == {"group": group, "device": address})


def build_mechanisms(inputs: list[dict[str, object]], outputs: list[dict[str, object]]) -> list[dict[str, object]]:
	switch = lambda address: device_id("pinmame.input.switch", address, inputs)
	solenoid = lambda address: device_id("pinmame.output.solenoid", address, outputs)
	prov = provenance(CORE_SOURCE, MANUAL_SOURCE, status="observed")
	return [
		{"id": "mechanism.ball-trough", "label": "Four-ball trough", "kind": "kicker", "actuators": [solenoid(9)], "sensors": [switch(number) for number in (41, 42, 43, 44, 45)], "behavior": "Stock assembly exposes a jam opto followed by four ball-position optos; the trough-eject coil feeds the shooter lane. Later firmware can use optional fifth and sixth ball optos, but their exact physical expansion geometry remains unvalidated.", "assembly_part_number": "A-22971", "provenance": prov},
		{"id": "mechanism.right-popper", "label": "Right popper", "kind": "kicker", "actuators": [solenoid(8)], "sensors": [switch(46)], "behavior": "The right-popper opto reports an occupied ball and the right-popper coil ejects it; exact launch vector and timing are not yet validated.", "assembly_part_number": "A-23156", "provenance": prov},
		{"id": "mechanism.drop-target", "label": "Single drop target", "kind": "drop_target_bank", "actuators": [solenoid(6), solenoid(7)], "sensors": [switch(15)], "behavior": "Separate down and up coils move the single target and the Drop Target Down switch reports the lowered state; timing and startup state remain to be runtime-validated.", "assembly_part_number": "A-15211-1", "provenance": prov},
		{"id": "mechanism.jet-exit-post", "label": "Jet exit post", "kind": "other", "actuators": [solenoid(3)], "sensors": [switch(47)], "behavior": "A dedicated coil drives the jet-exit post and a normally-closed opto reports the jet-exit path; the exact mechanical sequence remains to be runtime-validated.", "assembly_part_number": "A-22977", "provenance": prov},
		{"id": "mechanism.lock-diverter", "label": "Lock diverter", "kind": "diverter", "actuators": [solenoid(51), solenoid(52)], "sensors": [], "behavior": "Power and hold windings operate the lock diverter. The manual identifies the assembly and electrical pair, but positions and transition timing are not yet validated.", "assembly_part_number": "A-22993", "provenance": prov},
		{"id": "mechanism.up-down-ramp", "label": "Up/down ramp", "kind": "diverter", "actuators": [solenoid(53), solenoid(54)], "sensors": [switch(38)], "behavior": "Power and hold windings move the ramp; switch 38 reports Ramp Up. Exact startup position and transition timing remain to be runtime-validated.", "assembly_part_number": "A-22989", "provenance": prov},
		{"id": "mechanism.right-lockup", "label": "Right lockup", "kind": "kicker", "actuators": [solenoid(16)], "sensors": [switch(51), switch(55), switch(56)], "behavior": "The stock cabinet has one right-lockup opto and eject coil. Later firmware names two optional additional lockup optos; exact expansion fitment and ball-state behavior remain unvalidated.", "assembly_part_number": "A-20680-1", "provenance": prov},
		{"id": "mechanism.auto-plunger", "label": "Auto plunger", "kind": "kicker", "actuators": [solenoid(15)], "sensors": [switch(18)], "behavior": "The shooter-lane switch reports a staged ball and the auto-plunger coil launches it; exact launch vector and timing remain to be validated in a faithful RFM recreation.", "assembly_part_number": "A-22429-4", "provenance": prov},
	]


VARIANT_NOTES = {
	"rfm_120": "Factory 1.20 update for the stock model 50070 cabinet and original four-ball playfield.",
	"rfm_140": "Factory 1.40 update for the same stock model 50070 cabinet and I/O contract.",
	"rfm_150": "Factory 1.50 update documented by the February 1999 operations manual; same stock cabinet and I/O contract.",
	"rfm_160": "Last official 1.60 update for the stock model 50070 cabinet; canonical physical baseline for this clone family.",
	"rfm_180": "Unofficial tournament-oriented update for the stock playfield; PinMAME notes an 8 MB RAM requirement but no new playfield I/O.",
	"rfm_190": "Unofficial hemtoni update for the stock playfield and stock sound flash.",
	"rfm_191": "Unofficial hemtoni update that ships a distinct sound flash with additional sounds; playfield I/O remains compatible.",
	"rfm_195": "Unofficial German retranslation branch based on the 1.90-era software and stock playfield hardware.",
	"rfm_200": "First myPinballs update; reuses the 1.91 sound flash and does not yet enable the optional shaker/knocker outputs introduced in 2.10.",
	"rfm_210": "myPinballs update compatible with the stock playfield and able to use optional aftermarket knocker driver 18 and shaker driver 19 when fitted.",
	"rfm_222": "myPinballs update compatible with the stock four-ball playfield; later six-ball hardware support begins in this firmware line and exact optional fitment must be selected by the author.",
	"rfm_223": "myPinballs update compatible with the stock four-ball playfield and optional six-ball/opto-expander hardware.",
	"rfm_224": "myPinballs update compatible with the stock four-ball playfield and optional six-ball/opto-expander hardware.",
	"rfm_250": "myPinballs update compatible with the stock four-ball playfield and optional six-ball/opto-expander hardware.",
	"rfm_260": "myPinballs update that requires the opto expansion for its six-ball mode and uses optional switches 53-56; it can still run the unmodified stock playfield configuration described by the project notes, but the selected hardware mode must be explicit.",
}


def build_drivers() -> list[dict[str, object]]:
	catalog = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
	rows = sorted((row for row in catalog["drivers"] if row["id"].startswith("rfm_")), key=lambda row: row["id"])
	if {row["id"] for row in rows} != set(VARIANT_NOTES):
		raise RuntimeError("catalog RFM driver set no longer matches the curated variant table")
	result: list[dict[str, object]] = []
	for row in rows:
		driver = {key: row[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if "clone_of" in row:
			driver["clone_of"] = row["clone_of"]
		driver["physical_compatibility"] = "identical" if row["id"] in {"rfm_120", "rfm_140", "rfm_150", "rfm_160"} else "compatible"
		driver["variant_notes"] = VARIANT_NOTES[row["id"]]
		result.append(driver)
	return result


SOURCES = [
	{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames: exact 15-driver rfm_120 through rfm_260 clone family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/p2k.c: public switch translation, opto polarity, output publication, video layout, ROM variants, and hardware-generation contract; src/wpc/p2k_names.h: machine-test-verified RFM switch, coil, and lamp tables", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": MANUAL_SOURCE, "kind": "manual", "uri": "external:pinmame-manuals/_unsorted/Bally_1999_Revenge_From_Mars_Operations_Manual_February_1999_OCR_searchable.pdf", "sha256": MANUAL_SHA256, "locator": "February 1999 model 50070 operations manual; PDF pages 86-88 / printed pages 2-46 through 2-48 lamp matrices, switch matrix, dedicated inputs, and solenoid table; assembly and wiring sections", "excerpts": [{"id": "excerpt.rfm.operations-service-tables", "locator": "PDF pages 86-88; printed pages 2-46 through 2-48", "path": MANUAL_EXCERPT, "sha256": MANUAL_EXCERPT_SHA256, "method": "mixed", "transcribed_by": "Codex with pypdf text extraction and visual page review", "reviewed": True}], "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics Games, Inc."},
	{"id": REJECTED_VPX_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/revenge-from-mars-1999/source/Attack%20and%20Revenge%20from%20Mars%20%28Midway-Williams%29%20v600.vpx", "sha256": REJECTED_VPX_SHA256, "locator": "12,959,744-byte hybrid JPSalas v6.0.0 table; embedded script cGameName=afm_113b and AFM switch/solenoid callbacks; visually confirmed Attack from Mars geometry, rejected for RFM spatial or controller evidence", "original_filename": "Attack and Revenge from Mars (Midway-Williams) v600.vpx", "known_working": False, "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "JPSalas and credited table contributors"},
]


def build_definition() -> dict[str, object]:
	inputs = build_inputs()
	outputs = build_outputs()
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {"id": "bally.revenge-from-mars.1999", "name": "Revenge from Mars", "manufacturer": "Bally", "year": 1999, "kind": "physical_pinball", "model_number": "50070", "ipdb_id": 4446},
		"coverage": {"status": "partial", "missing": ["mechanism_behavior", "polarity", "variant_differences", "spatial_placement"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "observed", "mechanisms": "observed", "variant_coverage": "observed", "recreation_knowledge": "observed", "spatial_placement": "unknown"}},
		"controller": {"platform": "pinmame.p2k", "hardware_generation": "0x8000000000000", "inversion_applied_by_emulator": True},
		"drivers": build_drivers(),
		"inputs": inputs,
		"outputs": outputs,
		"displays": [{"id": "display.pinball-2000-video", "label": "Pinball 2000 reflected playfield video", "kind": "video", "controller_index": 0, "width": 640, "height": 480, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE_SOURCE)}, "provenance": provenance(CORE_SOURCE)}],
		"mechanisms": build_mechanisms(inputs, outputs),
		"relationships": [],
		"sources": SOURCES,
		"knowledge": {"path": "knowledge/bally/revenge-from-mars-1999.md", "status": "partial"},
		"conflicts": [{"id": "conflict.slingshot-spotlight-lamp-pair", "path": "$.outputs[manual.address=18B|28B].label", "description": "The operations manual prints Left Slingshot Spotlight at 18B and Right at 28B. PinMAME's complete machine lamp-test walk reports the opposite pair: public 15/manual 18B is Right and public 31/manual 28B is Left. The canonical labels follow the measured machine test.", "source_refs": [MANUAL_SOURCE, CORE_SOURCE], "status": "ignored", "rationale": "The discrepancy is fully resolved for recreation by the machine test; retaining it documents why the runtime-correct labels intentionally differ from the printed grid."}],
	}


KNOWLEDGE = """# Revenge from Mars (Bally, 1999)

Coverage: **partial - complete public address inventory and stock wiring, with mechanism dynamics, non-opto polarity, firmware-option fitment, and spatial placement still incomplete**

## Identity and Pinball 2000 architecture

This is Bally model 50070, *Revenge from Mars*, the first Pinball 2000 title. A MediaGX PC renders a 640x240 game framebuffer onto a monitor in the head; the cabinet optics reflect that image onto a partly transparent playfield surface. PinMAME exports one 640x480 video display because each native row is doubled in the current layout. VPE should consume that exported video surface as the overlay texture, preserve its 2:1 logical pixel shape, and place the rendered plane through table-specific scene geometry rather than treating it as a DMD.

The power-driver board still exposes conventional playfield switches, coils, flashers, and lamps. PinMAME publishes those through the normal switch, solenoid, and lamp groups while the video frame is a separate display output. No general-illumination group is currently exported by the P2K driver, so this definition does not invent one.

## Public controller numbering

Playfield switches use public column/row addresses `11-88`. Printed direct inputs `D1-D8`, `D9-D16`, and `D17-D24` are exposed at `91-98`, `101-108`, and `111-118`. The factory manual's shaded trough, popper, jet-exit, lockup, and ramp-entry optos physically rest closed; PinMAME normalizes them before exposing switch state. The later optional expansion positions 53-56 are also optos.

Board drivers 1-32 retain public solenoid numbers 1-32. Board drivers 33-36 are exported through PinMAME's lower-flipper public addresses 45-48. Board drivers 37-48 become custom public outputs 51-62. Do not remap the printed driver numbers directly for 33-48; the JSON preserves both values as separate aliases.

The lamp board is not two contiguous 8x8 matrices. It is eight columns of sixteen bits, interleaving Bank A and Bank B per column. Convert printed notation with `public = (column - 1) * 16 + (Bank B ? 8 : 0) + (row - 1)`. The public range is zero-based `0-127` and the definition includes every cell, including all twelve printed unused positions.

## Stock devices and optional hardware

The February 1999 manual validates the stock four-ball trough, single drop target, right popper, auto plunger, right lockup, jet-exit post, lock diverter, up/down ramp, two Martian toys, gates, slings, jets, flashers, and flippers. It provides the connector, wire, transistor, and part data encoded in the definition. The manual establishes inventory and wiring but not enough dynamic detail to claim complete ball routing, actuator timing, startup positions, or launch vectors; those mechanism records remain observed.

Factory RFM leaves drivers 18 and 19 unpopulated. Community firmware 2.10 and later can drive an aftermarket knocker on 18 and shaker motor on 19. Driver 48 is a game-table ticket-dispenser option and is not normally fitted to a pinball cabinet. Firmware 2.22 and later can support a six-ball trough through an opto expansion; 2.60 uses optional switches 53-56 and requires the expansion for its six-ball mode. An author must select the intended firmware and physical option set explicitly.

The exact Prism boot-ROM revision paired with every later community update has not been independently authenticated. PinMAME boots its currently declared set combinations, but that is not proof that each pairing shipped together. Preserve the catalog variants and their notes; do not silently collapse all revisions into a single hardware claim.

## Display and rendering contract

PinMAME's P2K video source is 640x240. The exported CORE_VIDEO layout is 640x480 with rows doubled so legacy display sizing does not halve the output. The frame is already turned into readable row order by the driver; VPE must not mirror or vertically flip it again. A CRT-style filter may reconstruct scanline and shadow-mask character at the logical 640x240 resolution, but geometry, keystone, reflection plane, and cabinet occlusion belong to the authored Unity scene.

## Evidence precedence and known discrepancy

PinMAME's current `p2k_names.h` tables were walked completely against the games' own switch, coil, and lamp tests. Those measured runtime names and public addresses take precedence over visual inference. The manual remains physical truth for connectors, wires, driver transistors, parts, and stock-vs-unused fitment.

The operations manual swaps one lamp-name pair: it prints Left Slingshot Spotlight at 18B and Right at 28B. The machine lamp test reports the reverse. The definition therefore binds public 15/manual 18B to Right Slingshot Spotlight and public 31/manual 28B to Left Slingshot Spotlight, matching the running machine, and retains the discrepancy as an ignored conflict with rationale.

The supplied `Attack and Revenge from Mars (Midway-Williams) v600.vpx` is not RFM geometry. Its embedded script runs `afm_113b`, its callbacks are Attack from Mars addresses, and its extracted screenshot shows the AFM playfield. It is retained at SHA-256 `9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be` as a rejected candidate and contributes no RFM spatial or controller assertion.

## Remaining author-ready work

- Obtain a faithful RFM VPX/VPE scene or measured playfield survey and map each physical playfield sensor, lamp effect, flasher, and actuator into normalized coordinates.
- Validate mechanism startup states, transition timing, ball routes, and launch vectors in an actual RFM recreation or repeatable runtime harness.
- Complete non-opto normally-open/closed and pulse semantics instead of inferring them from labels alone.
- Authenticate the optional six-ball/opto-expander, knocker, shaker, ticket, and Prism/firmware combinations per driver revision.

## Sources

- `manual.rfm.operations-1999`: February 1999 model 50070 operations manual, SHA-256 `6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df`; service tables and assemblies.
- `pinmame.core.8371478a7640`: pinned P2K implementation and machine-test-verified device tables at revision `8371478a7640f1896dcdf565aed340dc5df989ba`.
- `vpx-table.attack-and-revenge-v600-rejected`: exact user-supplied hybrid VPX, rejected because it runs AFM ROM semantics and AFM geometry.
"""


def expected_files() -> dict[Path, str]:
	definition = json.dumps(build_definition(), indent=2, ensure_ascii=False, sort_keys=True) + "\n"
	return {DEFINITION_PATH: definition, KNOWLEDGE_PATH: KNOWLEDGE}


def check() -> None:
	errors: list[str] = []
	for path, expected in expected_files().items():
		if not path.exists():
			errors.append(f"missing {path.relative_to(ROOT)}")
		elif path.read_text(encoding="utf-8") != expected:
			errors.append(f"stale {path.relative_to(ROOT)}")
	for obsolete in (ROOT / "machines/stubs/rfm_160.json", ROOT / "knowledge/stubs/rfm_160.md"):
		if obsolete.exists():
			errors.append(f"obsolete {obsolete.relative_to(ROOT)} still exists")
	excerpt = ROOT / MANUAL_EXCERPT
	if hashlib.sha256(excerpt.read_bytes()).hexdigest() != MANUAL_EXCERPT_SHA256:
		errors.append(f"hash mismatch for {MANUAL_EXCERPT}")
	if errors:
		raise SystemExit("\n".join(errors))


def write() -> None:
	definition = build_definition()
	DEFINITION_PATH.parent.mkdir(parents=True, exist_ok=True)
	KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
	write_json(DEFINITION_PATH, definition)
	write_text(KNOWLEDGE_PATH, KNOWLEDGE)


def main() -> None:
	parser = argparse.ArgumentParser(description="Build the Revenge from Mars partial machine definition")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	if args.write:
		write()
	else:
		check()


if __name__ == "__main__":
	main()
