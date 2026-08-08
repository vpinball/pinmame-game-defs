"""Self-contained source template for the Time Machine deterministic curator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from pinmame_game_defs.coverage import build_coverage_report, build_curation_queue, write_coverage_report
from pinmame_game_defs.jsonio import content_sha256, load_json, write_json, write_text
from pinmame_game_defs.registry import rebuild_catalog


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
PINMAME_SHORT = PINMAME_REVISION[:12]
MACHINE_ID = "data-east.time-machine.1988"
MACHINE_PATH = Path("machines/partial/data-east/time-machine-1988.json")
SEED_PATH = Path("tools/seeds/data-east/time-machine-1988.json")
SPATIAL_JSON_PATH = Path("reports/spatial/data-east/time-machine-1988.json")
SPATIAL_MD_PATH = Path("reports/spatial/data-east/time-machine-1988.md")
KNOWLEDGE_PATH = Path("knowledge/data-east/time-machine-1988.md")
STUB_PATH = Path("machines/stubs/tmac_a24.json")
STUB_KNOWLEDGE_PATH = Path("knowledge/stubs/tmac_a24.md")
MANIFEST_PATH = Path("tools/seeds/data-east/time-machine-1988-extraction-manifest.json")

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_SHORT}"
CORE_SOURCE = f"pinmame.core.{PINMAME_SHORT}"
MANUAL_SOURCE = "manual.data-east.time-machine.1988"
TABLE_SOURCE = "vpx-table.time-machine-2.4.1"
SCRIPT_SOURCE = "vpx-script.time-machine-2.4.1"
EXTRACTION_SOURCE = "vpx-extraction.time-machine-2.4.1"
RENDER_SOURCE = "human-review.time-machine-manual-renders"

MANUAL_SHA256 = "f232f8114ea31776a9d49e274b5ebed32cb3805acb4e719785fe48d43ddd719c"
MANUAL_URI = "https://archive.org/download/Data_East_Time_Machine_Manual/Data_East_1988_Time_Machine_Manual.pdf"
MANUAL_FILENAME = "Data_East_1988_Time_Machine_Manual.pdf"
TABLE_SHA256 = "b6c4b39bc7a672c1914b25e19192ec4cde8432aae00f9a5cd913c9b2f3c3c4f4"
SCRIPT_SHA256 = "1ab7a5cfd7c6e55652a1fc4f9a28e05fd55e24b732b897355e0daec1a5602ee1"
MANIFEST_ALGORITHM = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
MANIFEST_CONTENT_SHA256 = "96ae681549e9284ccec0eddb0181decb07b0388651fcf9bfb22bd299dfb5a8b6"
MANIFEST_SHA256 = "91bb4c4b3be5b24ea9b77493e46d83810dd549ca10186ae47da4a1f8f9eaa185"

SWITCH_DRIVES = ["GRN-BRN", "GRN-RED", "GRN-ORN", "GRN-YEL", "GRN-BLK", "GRN-BLU", "GRN-VIO", "GRN-GRY"]
SWITCH_RETURNS = ["WHT-BRN", "WHT-RED", "WHT-ORN", "WHT-YEL", "WHT-GRN", "WHT-BLU", "WHT-VIO", "WHT-GRY"]
LAMP_DRIVES = ["YEL-BRN", "YEL-RED", "YEL-ORN", "YEL-BLK", "YEL-GRN", "YEL-BLU", "YEL-VIO", "YEL-GRY"]
LAMP_RETURNS = ["RED-BRN", "RED-BLK", "RED-ORN", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY"]

SWITCH_LABELS = {
	1: "Plumb Tilt", 2: "Not Used", 3: "Credit Button", 4: "Right Coin", 5: "Center Coin", 6: "Left Coin", 7: "Slam Tilt", 8: "Not Used",
	9: "Not Used", 10: "Outhole", 11: "Trough #1", 12: "Trough #2", 13: "Trough #3", 14: "Shooter Lane", 15: "Left EOS", 16: "Right EOS",
	17: "Left Outlane", 18: "Left Return", 19: "Right Outlane", 20: "Right Return", 21: "Left Slingshot", 22: "Right Slingshot", 23: "Not Used", 24: "Not Used",
	25: "1 Lane", 26: "2 Lane", 27: "3 Lane", 28: "Left Ramp", 29: "Center Ramp", 30: "Right Ramp", 31: "Left Rollover", 32: "Right Rollover",
	33: "Left Bank1", 34: "Left Bank2", 35: "Left Bank3", 36: "Wireform1", 37: "Wireform2", 38: "Wireform3", 39: "Not Used", 40: "Not Used",
	41: "Center Bank1", 42: "Center Bank2", 43: "Center Bank3", 44: "Wireform4", 45: "Super VUK", 46: "Left Pop Bumper", 47: "Center Pop Bumper", 48: "Right Pop Bumper",
	49: "Right Bank1", 50: "Right Bank2", 51: "Right Bank3",
}
for _number in range(52, 65):
	SWITCH_LABELS[_number] = "Not Used"

SWITCH_PARTS = {
	1: "500-5023-00", 3: "500-5097-00", 4: "180-5024-00", 5: "180-5024-00", 6: "180-5024-00", 7: "180-5022-00",
	10: "180-5011-00", 11: "180-5009-00", 12: "180-5009-00", 13: "180-5010-00", 14: "500-5143-00",
	15: "180-5018-00", 16: "180-5018-00", 17: "500-5144-00", 18: "180-5003-00", 19: "500-5142-00", 20: "180-5003-00",
	21: "180-5023-00 / 180-5035-00", 22: "180-5023-00 / 180-5035-00", 25: "500-5142-00", 26: "500-5142-00", 27: "500-5142-00",
	28: "180-5002-00", 29: "180-5002-00", 30: "180-5002-00", 31: "180-5003-00", 32: "180-5003-00",
	33: "515-5161-02", 34: "515-5124-06", 35: "515-5162-05", 36: "180-5028-00", 37: "180-5028-00", 38: "180-5028-00",
	41: "515-5161-02", 42: "515-5124-06", 43: "515-5162-05", 44: "180-5030-00", 45: "180-5041-00",
	46: "180-5036-00", 47: "180-5036-00", 48: "180-5036-00", 49: "515-5161-02", 50: "515-5124-06", 51: "515-5162-05",
}

SWITCH_POINTS = {
	10: (0.529959, 0.984987), 11: (0.709701, 0.943740), 12: (0.790382, 0.921744), 13: (0.874475, 0.899872),
	14: (0.944829, 0.926649), 17: (0.054134, 0.834254), 18: (0.121331, 0.756275), 19: (0.854162, 0.786102),
	20: (0.789340, 0.752842), 21: (0.256509, 0.791770), 22: (0.713590, 0.705091), 25: (0.477256, 0.117556),
	26: (0.582958, 0.117556), 27: (0.690113, 0.117556), 28: (0.481250, 0.154319), 29: (0.300907, 0.181115),
	30: (0.772000, 0.121466), 31: (0.393000, 0.299920), 32: (0.937097, 0.249336), 33: (0.107214, 0.574160),
	34: (0.122777, 0.543480), 35: (0.137559, 0.515777), 36: (0.111149, 0.429840), 37: (0.095216, 0.399462),
	38: (0.080714, 0.369179), 41: (0.475930, 0.358504), 42: (0.520765, 0.378739), 43: (0.566140, 0.398939),
	44: (0.508000, 0.318162), 45: (0.852500, 0.475589), 46: (0.478135, 0.218832), 47: (0.590782, 0.314294),
	48: (0.694974, 0.215091), 49: (0.785515, 0.514404), 50: (0.799785, 0.543828), 51: (0.813598, 0.572310),
}

LAMP_MATRIX_LABELS = [
	"Starwarp #1", "Starwarp #2", "Starwarp #3", "Starwarp #4", "Starwarp #5", "Starwarp #6", "Starwarp #7", "Starwarp #8",
	"Center Square", "Center Circle", "Center Triangle", "Left 1970", "Left 1960", "Left 1950", "5x", "4x",
	"Special", "3 Ball Jackpot", "Left EMC²SR", "Left Mini Jackpot", "Center Mini Jackpot", "Right Mini Jackpot", "3x", "2x",
	"2x Scores", "Extra Ball", "Bonus Hold", "100K", "50K", "25K", "Targets Lite Special", "All Scores 2x",
	"Left Triangle", "Left Circle", "Left Square", "Left Extra Ball", "Laser Kick", "Left Return", "Extra Ball", "Bonus Hold Over",
	"Right Square", "Right Circle", "Right Triangle", "Right Hotdog", "Right Return", "Right Extra Ball", "Left Hotdog", "Starwarp",
	"Lane1", "Lane2", "Lane3", "Pop Left", "Pop Center", "Pop Right", "1980", "1970",
	"Top Right Arrow", "Right EMC²SR", "Right 1950", "Right 1960", "Right 1970", "Insert", "1960", "1950",
]

LAMP_LIST_LABELS = [
	'"S"tarwarp', 's"T"arwarp', 'st"A"rwarp', 'sta"R"warp', 'star"W"arp', 'starw"A"rp', 'starwa"R"p', 'starwar"P"',
	"Center Square", "Center Circle", "Center Triangle", "Left Ramp 1970", "Left Ramp 1960", "Left Ramp 1950", "5X", "4X",
	"Special", "3 Ball Jackpot", "Left Ramp E=MC²", "Left Mini Jackpot", "Center Mini Jackpot", "Right Mini Jackpot", "3X", "2X",
	"2X All Scores Cntr Plyfld", "Extra Ball Back Panel", "Bonus Hold Back Panel", "100K Back Panel", "50K Back Panel", "25K Back Panel",
	"Targets Light Special", "2X All Scores", "Left Triangle", "Left Circle", "Left Square", "Left Extra Ball", "Laser Kick", "Left Return",
	"Extra Ball Center Playfield", "Bonus Hold Center Plyfld", "Right Square", "Right Circle", "Right Triangle", "Right Hotdog", "Right Return",
	"Right Extra Ball", "Left Hotdog", "Starwarp Center Playfield", "Lane1", "Lane2", "Lane3", "Left Pop Bumper", "Center Pop Bumper",
	"Right Pop Bumper", "1980", "1970", "Top Right Arrow", "Right Ramp E=MC²", "Right Ramp 1950", "Right Ramp 1960", "Right Ramp 1970",
	"Engine", "1960", "1950",
]

LAMP_POINTS = [
	(0.404166,0.973266),(0.419784,0.969110),(0.433101,0.970758),(0.446659,0.970885),(0.467480,0.970251),(0.483218,0.971645),(0.495565,0.971518),(0.510334,0.971518),
	(0.547440,0.434110),(0.498970,0.412917),(0.448960,0.396647),(0.195207,0.432728),(0.208280,0.456666),(0.220566,0.482432),(0.620557,0.658945),(0.576962,0.722630),
	(0.329712,0.461382),(0.308410,0.421478),(0.246355,0.526953),(0.311623,0.525992),(0.361714,0.523706),(0.413401,0.514620),(0.530666,0.787692),(0.484764,0.848441),
	(0.510334,0.956352),(0.495565,0.956352),(0.483218,0.956478),(0.467480,0.955084),(0.446659,0.955718),(0.433101,0.955591),(0.315202,0.670928),(0.339151,0.717712),
	(0.149493,0.594953),(0.159208,0.562045),(0.177259,0.532041),(0.052990,0.690488),(0.054006,0.733144),(0.123831,0.690869),(0.364645,0.764654),(0.394195,0.817503),
	(0.749966,0.590268),(0.736727,0.561547),(0.718513,0.536209),(0.635106,0.511981),(0.777934,0.715601),(0.854304,0.719327),(0.302865,0.630552),(0.401022,0.596430),
	(0.466414,0.036118),(0.575199,0.036980),(0.685226,0.044947),(0.480572,0.217424),(0.590941,0.314224),(0.696300,0.213829),(0.607240,0.551302),(0.561635,0.612904),
	(0.864663,0.343503),(0.704908,0.408182),(0.746567,0.356771),(0.763030,0.330410),(0.777622,0.307034),(0.419784,0.953943),(0.519345,0.675208),(0.475167,0.740072),
]

BACKBOX_LAMPS = {1,2,3,4,5,6,7,8,26,27,28,29,30,62}


def excerpt_switch_matrix() -> str:
	rows = [
		"# Time Machine switch matrix transcription", "", "Source: PDF pages 26-27, printed pages 22-23. Render-decided from retained Archive.org PDF pages; OCR was locator-only.", "",
		"The matrix is transcribed column-major. Printed labels and `Not Used` cells are preserved.", "",
		"| Row / return | GRN-BRN | GRN-RED | GRN-ORN | GRN-YEL | GRN-BLK | GRN-BLU | GRN-VIO | GRN-GRY |",
		"| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
	]
	for row, return_wire in enumerate(SWITCH_RETURNS):
		cells = [f"{column * 8 + row + 1} {SWITCH_LABELS[column * 8 + row + 1]}" for column in range(8)]
		rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
	rows.extend(["", "## Printed description-list details", "", "The adjacent list prints these more specific descriptions:", ""])
	for number in range(1, 65):
		part = SWITCH_PARTS.get(number)
		detail = LITERAL_SWITCH_DETAILS.get(number, SWITCH_LABELS[number])
		rows.append(f"- {number}: {detail}" + (f" — `{part}`" if part else ""))
	return "\n".join(rows) + "\n"


LITERAL_SWITCH_DETAILS = {
	15: "Left Flip. Instant Info.; Left EOS", 16: "Right Flip. Instant Info.; Right EOS",
	17: "Left Outlane", 18: "Left Return Lane", 19: "Right Outlane", 20: "Right Return Lane",
	21: "Left Slingshot Trigger Sw.; Point Sw.", 22: "Right Slingshot Trigger Sw.; Point Sw.",
	25: "Left Top Lane", 26: "Center Top Lane", 27: "Right Top Lane", 28: "Left Ramp", 29: "Center Ramp", 30: "Right Ramp",
	31: "Left Star Rollover", 32: "Right Star Rollover", 33: "Left 3 Bank Bottom", 34: "Left 3 Bank Center", 35: "Left 3 Bank Top",
	36: "Lock Ball #1", 37: "Lock Ball #2", 38: "Lock Ball #3", 41: "Center 3 Bank Left", 42: "Center 3 Bank Middle",
	43: "Center 3 Bank Right", 44: "Ramp Sw. Under Plyfld", 45: "Right Super VUK", 46: "Left Pop Bumper",
	47: "Center Pop Bumper", 48: "Right Pop Bumper", 49: "Right 3 Bank Top", 50: "Right 3 Bank Center", 51: "Right 3 Bank Bottom",
}


def excerpt_lamp_matrix() -> str:
	rows = [
		"# Time Machine lamp matrix transcription", "", "Source: PDF pages 28-29, printed pages 24-25. Render-decided from retained Archive.org PDF pages; OCR was locator-only.", "",
		"The first table preserves the matrix sheet. The second list preserves the adjacent printed description list, including capitalization, quoting, `Lite`, `EMC²SR`, `E=MC²`, and abbreviated location text.", "",
		"| Row / return | YEL-BRN | YEL-RED | YEL-ORN | YEL-BLK | YEL-GRN | YEL-BLU | YEL-VIO | YEL-GRY |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
	]
	for row, return_wire in enumerate(LAMP_RETURNS):
		cells = [f"{column * 8 + row + 1} {LAMP_MATRIX_LABELS[column * 8 + row]}" for column in range(8)]
		rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
	rows.extend(["", "## Printed lamp-description list", ""])
	for number, label in enumerate(LAMP_LIST_LABELS, start=1):
		mark = " *" if number in {1,2,3,4,5,6,7,8,62} else ""
		rows.append(f"- {number}: {label}{mark}")
	rows.extend(["", "Printed footnote: `* Indicates Insert Lamp`.", ""])
	return "\n".join(rows)


def excerpt_coils() -> str:
	return """# Time Machine coil, relay, flipper, and special-solenoid transcription

Source: PDF pages 30-31, printed pages 26-27. The Coil I.D. sheet was decided from the retained Archive.org PDF render; OCR was locator-only.

## CPU-controlled Coil I.D. sheet

| Public / printed side | Printed device | Printed type | CPU drive / transistor |
| --- | --- | --- | --- |
| 1 / SIDE L 01 | KLACKER | 29-900 | GRY-BRN / Q46 |
| 25 / SIDE R 01 | OUTHOLE | 23-840 | shared Q46 mux side |
| 2 / SIDE L 02 | CHIME-1 | 27-1400 | GRY-RED / Q45 |
| 26 / SIDE R 02 | TROUGH | 23-840 | shared Q45 mux side |
| 3 / SIDE L 03 | CHIME-2 | 27-1400 | GRY-ORN / Q44 |
| 27 / SIDE R 03 | SUPER VERTICAL UP KICKER | 23-800 | shared Q44 mux side |
| 4 / SIDE L 04 | CHIME 3 | 27-1400 | GRY-YEL / Q43 |
| 28 / SIDE R 04 | BALL LOCK | 24-900 | shared Q43 mux side |
| 5 / SIDE L 05 | FLASH NO.1 | NO.906 (4) | GRY-GRN / Q42 |
| 6 / SIDE L 06 | FLASH NO.2 | NO.906 (4) | GRY-BLU / Q41 |
| 7 / SIDE L 07 | FLASH NO.3 | NO.906 (4) | GRY-VIO / Q40 |
| 8 / SIDE L 08 | FLASH NO.4 | NO.906 (2), NO.89 (2) | GRY-BLK / Q39 |
| 9 | FLASH NO.5 | NO.906 (2), NO.89 (2) | BRN-BLK / Q30 |
| 10 | LEFT/RIGHT COIL RELAY K1 | K1 | BLK-RED / Q29 |
| 11 | GENERAL ILLUM. RELAY K1 | K1 | BRN-ORN / Q28 |
| 12 | FLASH NO.6 | NO.906 (2), NO.89 (2) | BRN-YEL / Q27 |
| 13 | FLASH NO.7 | NO.906 (2), NO.89 (2) | BRN-GRN / Q26 |
| 14 | FLASH NO.8 | NO.906 (2), NO.89 (2) | BRN-BLU / Q25 |
| 15 | FLASH NO.9 | NO.906 (2), NO.89 (2) | BRN-VIO / Q24 |
| 16 | LASER KICK | 23-800 | WHT-GRY / Q23 |

After SIDE R 04, the sheet shows no further right-side device rows. The Coil Tests prose on the same printed page nevertheless says coil 10 switches +34 volts for drives 1-8 between left and right sets and calls the result an effective total of 23 regular coils. Pinned Time Machine `s11.c` also types public 29-32 as four distinct muxed #89-bulb output states. This is material evidence that R05-R08 belong to the addressable right-bank design, but neither the prose nor a device row identifies fitted circuits, quantities, or feature names for them. Their per-address activity and fitment remain unknown rather than dead or invented.

## Coil Tests operating description

The printed prose describes sixteen regular microprocessor-pulsed drivers plus six switch-triggered drivers. Coil 10 works with drives 1-8 to select +34 V between coil/flash-lamp sets termed left and right; the PPB supplies isolation diodes and current-limiting resistors, and the manual says this "effectively provides 23 regular coils." Automatic Test pulses every regular solenoid or flash lamp sequentially while displaying its name and drive number. Select Coil chooses one drive and can pulse it repeatedly.

## Switch-triggered coil table

| Printed special address | Printed description | Control line (CPU to coil) | Power line (PS to coil) | Trigger line (coil switch to CPU) | Drive transistor (TIP 122) | Coil type |
| --- | --- | --- | --- | --- | --- | --- |
| SP1 | RIGHT POP BUMPER | BLU-ORN / CPU CN19-3 | RED / PS CN3-6 | ORN-BLK / CPU CN18-2 | Q8 | 23-800 |
| SP2 | CENTER POP BUMPER | BLU-RED / CPU CN19-4 | RED / PS CN3-6 | ORN-RED / CPU CN18-3 | Q9 | 23-800 |
| SP3 | LEFT SLINGSHOT | BLU-YEL / CPU CN19-6 | RED / PS CN3-6 | ORN-YEL / CPU CN18-4 | Q10 | 23-800 |
| SP4 | LEFT POP BUMPER | BLU-BRN / CPU CN19-7 | RED / PS CN3-6 | ORN-BRN / CPU CN18-5 | Q11 | 23-800 |
| SP5 | RIGHT SLINGSHOT | BLU-GRN / CPU CN19-8 | RED / PS CN3-6 | ORN-GRN / CPU CN18-8 | Q12 | 23-800 |
| SP6 | NOT USED | -- / CPU CN19-9 | -- / PS CN3-6 | -- / CPU CN18-9 | Q13 | -- |

The location drawing on the same printed page labels SP1 at the center pop and SP2 at the right pop. It agrees with SP4 at the left pop. Neither reading is silently corrected.

## Flippers

| Side | Printed coil | Supply / winding wires |
| --- | --- | --- |
| Left | 22-750/30-2600 | ORN-BLU / BLU-GRY / GRY-YEL |
| Right | 22-750/30-2600 | ORN-RED / BLU-VIO / BLK-WHT |
"""


def excerpt_mechanisms() -> str:
	return """# Time Machine playfield construction transcription

Source: PDF page 67 (printed 47) and PDF pages 74, 76, and 77 (printed 54, 56, and 57). Render-decided from the retained Archive.org PDF; OCR was locator-only.

The printed playfield-parts list identifies:

- 8 Laser Kick Assembly — `500-5080-00`
- 9 Slingshot Assembly (2) — `500-5029-01`
- 10 Pop Bumper Assembly (3) — `500-5034-07`
- 11 Left Flipper — `500-5031-12`
- 12 Right Flipper — `500-5031-11`
- 13 Super Vertical Up Kicker — `500-5116-00`
- 14 Ball Lock Assembly — `500-5104-00`
- 15 Ball Trough Eject Assembly — `500-5012-00`
- 16 Outhole Assembly — `500-5082-00`
- 54 Right Ramp — `515-5142-00`
- 55 Left Ramp — `515-5143-00`
- 56 Top Playfield Wire Ramp — `535-5336-00`
- 57 Under Playfield Wire Ramp — `515-5137-00`
- 62 Stand Up Target Assy (3) — `515-5144-00`

The Ball Lock Bracket Assembly drawing (`500-5104-00`) shows one `24-900` coil, one spring-return plunger, one lock-ball cam, and one lock-ball bracket. The machine uses three serial lock positions (switches 36, 37, 38) ahead of that single release cam; the retained table script supplies the causal ordering.

The Super Vertical Up Kicker drawing (`500-5116-00`) shows a `23-800` coil, vertical plunger, ball cup, switch assembly, guide, and return spring. It is a constructed vertical eject, not merely a printed feature label.

The three-bank standup drawing (`515-5144-00`) shows three independent switch/bracket targets with a red triangle, yellow circle, and blue square face. The machine has three such fixed banks; the manual does not show a reset coil or dropping target faces.
"""


EXCERPTS = {
	Path("evidence/excerpts/data-east.time-machine.1988/switch-matrix.md"): excerpt_switch_matrix(),
	Path("evidence/excerpts/data-east.time-machine.1988/lamp-matrix.md"): excerpt_lamp_matrix(),
	Path("evidence/excerpts/data-east.time-machine.1988/coil-and-flipper.md"): excerpt_coils(),
	Path("evidence/excerpts/data-east.time-machine.1988/mechanism-construction.md"): excerpt_mechanisms(),
}


def sha256_text(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def provenance(status: str, *source_refs: str) -> dict[str, object]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def aliases(namespace: str, number: int | str, manual: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(number)}]
	if manual is not None:
		result.append({"namespace": "manual.address", "value": manual})
	return result


def not_applicable(reason: str, status: str, *source_refs: str) -> dict[str, object]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(status, *source_refs)}


def located(device_id: str, point: tuple[float, float], role: str, status: str, *source_refs: str) -> dict[str, object]:
	return {
		"status": status,
		"placements": [{
			"id": f"{device_id}.placement-1", "role": role, "space": "playfield",
			"x": point[0], "y": point[1], "provenance": provenance(status, *source_refs),
		}],
	}


def switch_input(number: int) -> dict[str, object]:
	label = SWITCH_LABELS[number]
	unused = label == "Not Used"
	device_id = f"switch.matrix-{number}"
	column, row = divmod(number - 1, 8)
	physical: dict[str, object] = {
		"notes": f"Manual switch matrix column {column + 1}, row {row + 1}; printed cell '{label}'.",
	}
	if number in SWITCH_PARTS:
		physical["part_number"] = SWITCH_PARTS[number]
	if number in {15, 16}:
		physical["notes"] += " The printed parts list separately names the Instant Info flipper function and a physical EOS contact at this address; PinMAME FLIP1516 publishes cabinet-button state here."
	result: dict[str, object] = {
		"id": device_id, "label": f"Unused Switch {number}" if unused else label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number},
		"aliases": aliases("pinmame.switch", number, str(number)),
		"availability": "unused" if unused else "used", "physical": physical,
		"wiring": {"board": "CPU Board", "drive_wire": SWITCH_DRIVES[column], "return_wire": SWITCH_RETURNS[row]},
		"provenance": provenance("conflicted" if number in {2, 15, 16} else "validated", MANUAL_SOURCE, CORE_SOURCE, SCRIPT_SOURCE),
	}
	roles = {
		1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin", 7: "cabinet.slam-tilt",
		10: "ball.position", 11: "ball.position", 12: "ball.position", 13: "ball.position", 14: "ball.position",
		15: "flipper.lower.left.button", 16: "flipper.lower.right.button", 36: "ball.position", 37: "ball.position", 38: "ball.position", 45: "ball.position",
	}
	if number in roles:
		result["roles"] = [roles[number]]
	if unused:
		result["spatial"] = not_applicable("unused", "validated", MANUAL_SOURCE)
	elif number in {1, 3, 4, 5, 6, 7, 15, 16}:
		result["spatial"] = not_applicable("cabinet_or_service", "conflicted" if number in {15, 16} else "validated", MANUAL_SOURCE, CORE_SOURCE)
	elif number in SWITCH_POINTS:
		result["spatial"] = located(device_id, SWITCH_POINTS[number], "sensor", "observed", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	return result


def diagnostic_inputs() -> list[dict[str, object]]:
	result = []
	for device, suffix, label in [(-7, "7", "Black Button / Advance"), (-6, "6", "Green Button / Up-Down")]:
		result.append({
			"id": f"switch.diagnostic-{suffix}", "label": label, "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": device},
			"aliases": [{"namespace": "pinmame.switch", "value": str(device)}], "availability": "used",
			"roles": ["service.advance" if device == -7 else "service.adjust"],
			"physical": {"notes": "Shared Data East service-door input declared by DE_COMPORTS."},
			"spatial": not_applicable("cabinet_or_service", "validated", CORE_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE),
		})
	result.append({
		"id": "dip.jumper-w7", "label": "Jumper W7 (function undocumented)", "kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": 0},
		"aliases": [{"namespace": "pinmame.dip", "value": "0"}], "availability": "used",
		"physical": {"notes": "Pinned Data East input ports expose one W7 jumper; the game-specific function is not documented by the retained manual pages."},
		"spatial": not_applicable("dip_switch", "candidate", CORE_SOURCE, MANUAL_SOURCE),
		"provenance": provenance("candidate", CORE_SOURCE, MANUAL_SOURCE),
	})
	return result


def lamp_output(number: int) -> dict[str, object]:
	device_id = f"lamp.matrix-{number}"
	column, row = divmod(number - 1, 8)
	label = LAMP_LIST_LABELS[number - 1]
	status = "conflicted" if number == 25 else "candidate"
	physical: dict[str, object] = {
		"quantity": 1,
		"notes": f"Manual matrix prints '{LAMP_MATRIX_LABELS[number - 1]}'; adjacent description list prints '{label}'. Active vpmMapLights AllLamps membership routes every Light whose TimerInterval is {number}; the retained coordinate is a visual candidate, not a surveyed socket.",
	}
	if number in BACKBOX_LAMPS:
		physical["location"] = "backbox/back panel"
	if number == 25:
		physical["location"] = "center playfield"
		physical["notes"] += " The manual explicitly says Cntr Plyfld, while the sole TimerInterval 25 Light is flagged is_backglass=true on the hSpacewarpLights surface."
	result: dict[str, object] = {
		"id": device_id, "label": label, "kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": number},
		"aliases": aliases("pinmame.lamp", number, str(number)), "availability": "used", "physical": physical,
		"wiring": {"board": "CPU Board", "drive_wire": LAMP_DRIVES[column], "return_wire": LAMP_RETURNS[row]},
		"provenance": provenance(status, MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
	}
	if number in BACKBOX_LAMPS:
		result["spatial"] = not_applicable("cabinet_or_service", "validated", MANUAL_SOURCE, TABLE_SOURCE)
	elif number != 25:
		result["spatial"] = located(device_id, LAMP_POINTS[number - 1], "emitter", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	return result


SPECIAL_DE_PERMUTATION = (3, 4, 5, 1, 0, 2)
SPECIAL_PIA_HANDLER_TO_PRINTED = {0: 6, 1: 5, 2: 2, 3: 3, 4: 1, 5: 4}
SPECIAL_PUBLIC_TO_PRINTED = {17 + SPECIAL_DE_PERMUTATION[handler]: printed for handler, printed in SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
SPECIAL_PRINTED_LABELS = {
	1: "Right Pop Bumper (Coil Test table)", 2: "Center Pop Bumper (Coil Test table)",
	3: "Left Slingshot", 4: "Left Pop Bumper", 5: "Right Slingshot", 6: "Unused SP6 Driver",
}

SOLENOID_LABELS = {
	1: "Klacker", 2: "Chime 1", 3: "Chime 2", 4: "Chime 3", 5: "Flash No.1", 6: "Flash No.2", 7: "Flash No.3", 8: "Flash No.4",
	9: "Flash No.5", 10: "Left/Right Coil Relay K1", 11: "General Illumination Relay K1", 12: "Flash No.6", 13: "Flash No.7", 14: "Flash No.8", 15: "Flash No.9", 16: "Laser Kick",
	**{public: SPECIAL_PRINTED_LABELS[printed] for public, printed in SPECIAL_PUBLIC_TO_PRINTED.items()},
	24: "Unused Solenoid 24", 25: "Outhole", 26: "Trough Eject", 27: "Super Vertical Up Kicker", 28: "Ball Lock Release",
	29: "Emulator-Published Mux State 29", 30: "Emulator-Published Mux State 30", 31: "Emulator-Published Mux State 31", 32: "Emulator-Published Mux State 32",
	45: "Synthetic Right Flipper Power", 46: "Synthetic Right Flipper Hold", 47: "Synthetic Left Flipper Power", 48: "Synthetic Left Flipper Hold",
	49: "Simulation Ball Shooter", 50: "Reserved Solenoid 50",
}
for _number in range(33, 45):
	SOLENOID_LABELS[_number] = f"Inert Solenoid Address {_number}"

SOLENOID_PARTS = {1:"29-900",2:"27-1400",3:"27-1400",4:"27-1400",16:"23-800",17:"23-800",18:"23-800",19:"23-800",21:"23-800",22:"23-800",25:"23-840",26:"23-840",27:"23-800",28:"24-900"}
SOLENOID_TRANSISTORS = {1:"Q46",2:"Q45",3:"Q44",4:"Q43",5:"Q42",6:"Q41",7:"Q40",8:"Q39",9:"Q30",10:"Q29",11:"Q28",12:"Q27",13:"Q26",14:"Q25",15:"Q24",16:"Q23",17:"Q8",18:"Q10",19:"Q11",20:"Q13",21:"Q12",22:"Q9"}
SOLENOID_DRIVES = {1:"GRY-BRN",2:"GRY-RED",3:"GRY-ORN",4:"GRY-YEL",5:"GRY-GRN",6:"GRY-BLU",7:"GRY-VIO",8:"GRY-BLK",9:"BRN-BLK",10:"BLK-RED",11:"BRN-ORN",12:"BRN-YEL",13:"BRN-GRN",14:"BRN-BLU",15:"BRN-VIO",16:"WHT-GRY"}


def solenoid_output(number: int) -> dict[str, object]:
	device_id = "coil.game-on" if number == 23 else f"coil.driver-{number}"
	if number == 23:
		return {
			"id": device_id, "label": "Game On / Flipper and Special-Solenoid Enable", "kind": "control_signal",
			"binding": {"group": "pinmame.output.solenoid", "device": 23}, "aliases": aliases("pinmame.solenoid", 23), "availability": "used",
			"physical": {"notes": "PinMAME's shared s11 core public Game On state enables the flipper and special-solenoid circuits; this is a controller signal, not a playfield coil."},
			"spatial": not_applicable("internal_nonvisual", "validated", CORE_SOURCE), "provenance": provenance("validated", CORE_SOURCE),
		}
	label = SOLENOID_LABELS[number]
	unused = number in {20,24,33,34,35,36,37,38,39,40,41,42,43,44,49,50}
	kind = "virtual"
	if number in {5,6,7,8,9,12,13,14,15,29,30,31,32}: kind = "flasher"
	elif number == 10: kind = "relay"
	elif number == 11: kind = "gi"
	elif number not in {24,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50}: kind = "coil"
	status = "validated"
	if number in {17,22}: status = "conflicted"
	if number in {29,30,31,32}: status = "candidate"
	manual_number = (
		f"SIDE L {number:02d}" if 1 <= number <= 8
		else (str(number) if 9 <= number <= 16
		else (f"SP{SPECIAL_PUBLIC_TO_PRINTED[number]}" if 17 <= number <= 22
		else (f"SIDE R {number - 24:02d}" if 25 <= number <= 28 else None)))
	)
	physical: dict[str, object] = {"notes": f"Public solenoid {number}."}
	if manual_number is not None:
		physical["notes"] = f"Public solenoid {number}; manual printed address {manual_number}."
	if number not in {20,24,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50}:
		physical["quantity"] = 1
	if number in SOLENOID_PARTS: physical["part_number"] = SOLENOID_PARTS[number]
	if number in {5,6,7}: physical.update({"quantity": 4, "notes": physical["notes"] + " Manual prints four No.906 bulbs."})
	if number in {8,9,12,13,14,15}: physical.update({"quantity": 4, "notes": physical["notes"] + " Manual prints two No.906 and two No.89 bulbs."})
	if 17 <= number <= 22: physical["notes"] += f" Pinned s11.c PIA comments identify handlers 0-5 as printed SP6, SP5, SP2, SP3, SP1, SP4; setSSSol applies the Data East offset permutation {SPECIAL_DE_PERMUTATION}, deriving printed {manual_number} at public {number}."
	if number in {17,22}: physical["notes"] += " The Coil Test table and location drawing disagree over the right/center assignment; no winning label is inferred."
	if number == 24: physical["notes"] += " Pinned core never populates this public address, and the manual identifies no physical circuit for it."
	if 29 <= number <= 32: physical["notes"] += " The manual's Coil Tests prose says coil 10 multiplexes drives 1-8 between left and right sets for an effective total of 23 regular coils, and pinned Time Machine s11.c registers this as one of four distinct muxed #89-bulb output types at addresses 29-32. However, the retained device chart stops at SIDE R 04 and the retained script registers no callback, so static evidence cannot establish this exact state's runtime activity, fitted circuit, physical quantity, feature name, or socket."
	if 33 <= number <= 44: physical["notes"] += " PinMAME's shared s11 core exposes this address but the Data East game driver never populates it."
	if 45 <= number <= 48: physical["notes"] += " PinMAME-generated lower-flipper power/hold state; it is meaningful controller state, not a separate physical driver, winding, or part at this public number."
	if number == 49: physical["notes"] += " PinMAME's shared s11 core simulation-only shooter address; it is not a physical Data East output."
	if number == 50: physical["notes"] += " Reserved public address with no meaningful game state."
	if number in {20,24}:
		output_sources = (MANUAL_SOURCE, CORE_SOURCE)
	elif number in {33,34,35,36,37,38,39,40,41,42,43,44,49,50}:
		output_sources = (CORE_SOURCE,)
	elif number in {45,46,47,48}:
		output_sources = (CORE_SOURCE, SCRIPT_SOURCE)
	else:
		output_sources = (MANUAL_SOURCE, CORE_SOURCE, SCRIPT_SOURCE)
	result: dict[str, object] = {
		"id": device_id, "label": label, "kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": number},
		"aliases": aliases("pinmame.solenoid", number, manual_number), "availability": "unknown" if 29 <= number <= 32 else ("unused" if unused else "used"),
		"physical": physical, "provenance": provenance(status, *output_sources),
	}
	if number in SOLENOID_TRANSISTORS:
		result["wiring"] = {"board": "CPU Board / PPB", "driver_transistor": SOLENOID_TRANSISTORS[number]}
		if number in SOLENOID_DRIVES: result["wiring"]["drive_wire"] = SOLENOID_DRIVES[number]
	if unused:
		result["spatial"] = not_applicable("virtual" if number == 24 or number in set(range(33,51)) - {45,46,47,48} else "unused", "validated", *output_sources)
	elif number in {45,46,47,48}:
		result["spatial"] = not_applicable("virtual", "validated", *output_sources)
	elif number in {1,2,3,4,10,11}:
		result["spatial"] = not_applicable("cabinet_or_service", "validated", MANUAL_SOURCE, CORE_SOURCE)
	elif number == 16:
		result["spatial"] = located(device_id, (0.055000,0.871335), "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 18:
		result["spatial"] = located(device_id, SWITCH_POINTS[21], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 19:
		result["spatial"] = located(device_id, SWITCH_POINTS[46], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 21:
		result["spatial"] = located(device_id, SWITCH_POINTS[22], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 25:
		result["spatial"] = located(device_id, SWITCH_POINTS[10], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 26:
		result["spatial"] = located(device_id, SWITCH_POINTS[13], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 27:
		result["spatial"] = located(device_id, SWITCH_POINTS[45], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	elif number == 28:
		result["spatial"] = located(device_id, SWITCH_POINTS[36], "effect", "candidate", TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	return result


def displays() -> list[dict[str, object]]:
	labels = ["Player 1 alphanumeric display", "Player 2 alphanumeric display", "Player 3 numeric display", "Player 4 numeric display"]
	starts = [1, 9, 21, 29]
	return [{
		"id": f"display.segment-{index}", "label": label, "kind": "segment", "controller_index": index,
		"segment_start": starts[index], "width": 7,
		"spatial": not_applicable("cabinet_or_service", "validated", CORE_SOURCE, MANUAL_SOURCE),
		"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
	} for index, label in enumerate(labels)]


def mechanisms() -> list[dict[str, object]]:
	return [
		{"id":"mechanism.outhole","label":"Outhole feeder","kind":"kicker","actuators":["coil.driver-25"],"sensors":["switch.matrix-10"],"behavior":"Drain_Hit sustains switch 10 while the ball rests in the outhole. Output 25 kicks Drain at 90 degrees into the three-ball trough; the printed playfield list independently identifies Outhole Assembly 500-5082-00.","assembly_part_number":"500-5082-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.ball-trough","label":"Three-ball trough and eject","kind":"other","actuators":["coil.driver-26"],"sensors":["switch.matrix-11","switch.matrix-12","switch.matrix-13"],"behavior":"The retained table creates three balls at the front BallRelease position (switch 13), middle switch 12, and rear switch 11. Its update routine advances 11 to 12 to 13; output 26 kicks the front ball toward the manual shooter lane.","assembly_part_number":"500-5012-00","positions":[{"id":"trough.position-1","label":"Front eject position","sensors":["switch.matrix-13"]},{"id":"trough.position-2","label":"Middle position","sensors":["switch.matrix-12"]},{"id":"trough.position-3","label":"Rear position","sensors":["switch.matrix-11"]}],"provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.super-vuk","label":"Super Vertical Up Kicker","kind":"kicker","actuators":["coil.driver-27"],"sensors":["switch.matrix-44","switch.matrix-45"],"behavior":"A ball entering the under-playfield path pulses ramp switch 44, then is staged at VUK switch 45. Output 27 drives the constructed 23-800 vertical plunger/cup assembly and clears switch 45 as the ball is kicked upward.","assembly_part_number":"500-5116-00","positions":[{"id":"super-vuk.entry","label":"Under-playfield entry","sensors":["switch.matrix-44"]},{"id":"super-vuk.cup","label":"VUK cup","sensors":["switch.matrix-45"]}],"provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.visible-lock","label":"Three-position visible ball lock","kind":"other","actuators":["coil.driver-28"],"sensors":["switch.matrix-36","switch.matrix-37","switch.matrix-38"],"behavior":"The retained cvpmVLock orders three serial positions at switches 36, 37, and 38 and releases through output 28. The manual shows one 24-900 coil, spring-return plunger, lock cam, and bracket assembly rather than three independent ejectors.","assembly_part_number":"500-5104-00","positions":[{"id":"lock.position-1","label":"Lock Ball #1 / player-nearest","sensors":["switch.matrix-36"]},{"id":"lock.position-2","label":"Lock Ball #2 / middle","sensors":["switch.matrix-37"]},{"id":"lock.position-3","label":"Lock Ball #3 / rear","sensors":["switch.matrix-38"]}],"provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.laser-kick","label":"Laser Kick kickback","kind":"kicker","actuators":["coil.driver-16"],"sensors":["switch.matrix-17"],"behavior":"Switch 17 reports the left outlane ahead of the printed Laser Kick assembly. Output 16 fires and retracts the retained KickBack plunger; the manual identifies assembly 500-5080-00 and a 23-800 coil.","assembly_part_number":"500-5080-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.left-flipper","label":"Lower-left flipper","kind":"other","actuators":["coil.driver-47","coil.driver-48"],"sensors":["switch.matrix-15"],"behavior":"One 22-750/30-2600 dual-winding coil moves the sole left flipper. The manual prints a physical Left EOS at 15, while FLIP1516 and the retained key handler publish cabinet-button state at that address.","assembly_part_number":"500-5031-12","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
		{"id":"mechanism.right-flipper","label":"Lower-right flipper","kind":"other","actuators":["coil.driver-45","coil.driver-46"],"sensors":["switch.matrix-16"],"behavior":"One 22-750/30-2600 dual-winding coil moves the sole right flipper. The manual prints a physical Right EOS at 16, while FLIP1516 and the retained key handler publish cabinet-button state at that address.","assembly_part_number":"500-5031-11","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
		{"id":"mechanism.left-slingshot","label":"Left slingshot","kind":"other","actuators":["coil.driver-18"],"sensors":["switch.matrix-21"],"behavior":"The manual fits a trigger and point switch plus a switch-triggered SP3 coil; pinned Data East setSSSol publishes SP3 as public 18, and the retained native slingshot event pulses switch 21. No public SolCallback exists because the special circuit is hardware-triggered.","assembly_part_number":"500-5029-01","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
		{"id":"mechanism.right-slingshot","label":"Right slingshot","kind":"other","actuators":["coil.driver-21"],"sensors":["switch.matrix-22"],"behavior":"The manual fits a trigger and point switch plus a switch-triggered SP5 coil; pinned Data East setSSSol publishes SP5 as public 21, and the retained native slingshot event pulses switch 22. No public SolCallback exists because the special circuit is hardware-triggered.","assembly_part_number":"500-5029-01","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
		{"id":"mechanism.left-pop","label":"Left pop bumper","kind":"other","actuators":["coil.driver-19"],"sensors":["switch.matrix-46"],"behavior":"The retained Bumper1 event pulses switch 46. Both manual special-coil representations agree that SP4 is the left pop, and pinned Data East setSSSol publishes SP4 as public 19, but public callback timing is not exposed.","assembly_part_number":"500-5034-07","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
		{"id":"mechanism.center-pop","label":"Center pop bumper","kind":"other","actuators":[],"sensors":["switch.matrix-47"],"behavior":"The retained Bumper3 event pulses switch 47. The manual Coil Test table calls SP2 center while its location drawing calls SP1 center, so no actuator is selected.","assembly_part_number":"500-5034-07","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.right-pop","label":"Right pop bumper","kind":"other","actuators":[],"sensors":["switch.matrix-48"],"behavior":"The retained Bumper2 event pulses switch 48. The manual Coil Test table calls SP1 right while its location drawing calls SP2 right, so no actuator is selected.","assembly_part_number":"500-5034-07","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.left-standups","label":"Left three-bank fixed standups","kind":"other","actuators":[],"sensors":["switch.matrix-33","switch.matrix-34","switch.matrix-35"],"behavior":"Three independent fixed standup targets report bottom, center, and top. The manual's 515-5144-00 drawing shows switch/bracket targets and no drop/reset construction.","assembly_part_number":"515-5144-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.center-standups","label":"Center three-bank fixed standups","kind":"other","actuators":[],"sensors":["switch.matrix-41","switch.matrix-42","switch.matrix-43"],"behavior":"Three independent fixed standup targets report left, middle, and right. The manual's 515-5144-00 drawing shows switch/bracket targets and no drop/reset construction.","assembly_part_number":"515-5144-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.right-standups","label":"Right three-bank fixed standups","kind":"other","actuators":[],"sensors":["switch.matrix-49","switch.matrix-50","switch.matrix-51"],"behavior":"Three independent fixed standup targets report top, center, and bottom. The manual's 515-5144-00 drawing shows switch/bracket targets and no drop/reset construction.","assembly_part_number":"515-5144-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.manual-shooter","label":"Manual plunger and shooter lane","kind":"other","actuators":[],"sensors":["switch.matrix-14"],"behavior":"The playfield-parts illustration and shooter-switch assembly show a player-driven ball shooter. The retained plunger path crosses switch 14; no CPU shooter coil is claimed.","assembly_part_number":"500-5143-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
		{"id":"mechanism.fixed-ramps","label":"Fixed ramp, wireform, and subway paths","kind":"other","actuators":[],"sensors":["switch.matrix-28","switch.matrix-29","switch.matrix-30","switch.matrix-31","switch.matrix-32","switch.matrix-44"],"behavior":"The printed playfield list fits left/right ramps, a top wire ramp, and an under-playfield wire ramp. The retained script reports their fixed paths; it registers no motor or diverter actuator.","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
	]


def conflicts() -> list[dict[str, object]]:
	return [
		{"id":"conflict.left-eos-vs-public-button-state","path":"/inputs/switch.matrix-15","description":"The manual prints a physical Left EOS contact at matrix 15 and does not mark it as a cabinet switch. FLIP1516 and the retained key handler put left cabinet-button state at public 15.","source_refs":[MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE]},
		{"id":"conflict.right-eos-vs-public-button-state","path":"/inputs/switch.matrix-16","description":"The manual prints a physical Right EOS contact at matrix 16 and does not mark it as a cabinet switch. FLIP1516 and the retained key handler put right cabinet-button state at public 16.","source_refs":[MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE]},
		{"id":"conflict.shared-port-position-2-vs-unfitted","path":"/inputs/switch.matrix-2","description":"Shared Data East DE_COMPORTS names matrix position 2 Ball Tilt, while both Time Machine manual switch tables explicitly print position 2 Not Used. The machine record follows the game-specific fitment without erasing the shared-port label.","source_refs":[MANUAL_SOURCE,CORE_SOURCE]},
		{"id":"conflict.special-coil-right-center-location","path":"/outputs/coil.driver-17","description":"The manual Coil Test table prints SP1 Right Pop Bumper and SP2 Center Pop Bumper. Its location drawing places SP1 at the center pop and SP2 at the right pop. Pinned Data East setSSSol publishes SP1 at public 17 and SP2 at public 22; the two physical assignments remain unresolved and neither output is assigned to a mechanism or coordinate.","source_refs":[MANUAL_SOURCE,RENDER_SOURCE,CORE_SOURCE]},
		{"id":"conflict.lamp-25-playfield-vs-table-backglass","path":"/outputs/lamp.matrix-25","description":"The manual description list explicitly prints lamp 25 as 2X All Scores Cntr Plyfld. The sole AllLamps member with TimerInterval 25 is Light l25, flagged is_backglass=true on hSpacewarpLights. No physical placement is selected.","source_refs":[MANUAL_SOURCE,TABLE_SOURCE,SCRIPT_SOURCE]},
	]


def sources() -> list[dict[str, object]]:
	excerpt_meta = []
	for path, content in EXCERPTS.items():
		excerpt_meta.append({
			"id": "excerpt.time-machine." + path.stem,
			"path": path.as_posix(), "sha256": sha256_text(content), "method": "manual", "reviewed": True,
			"locator": {"switch-matrix.md":"PDF pages 26-27, printed pages 22-23","lamp-matrix.md":"PDF pages 28-29, printed pages 24-25","coil-and-flipper.md":"PDF pages 30-31, printed pages 26-27","mechanism-construction.md":"PDF page 67 (printed 47) and PDF pages 74, 76, 77 (printed 54, 56, 57)"}[path.name],
			"transcribed_by": "primary curator; OCR located, Poppler render decided",
		})
	return [
		{"id":CATALOG_SOURCE,"kind":"pinmame_catalog","uri":"https://github.com/vpinball/pinmame","revision":PINMAME_REVISION,"license":"BSD-3-Clause","attribution":"vpinball/PinMAME contributors","acquired_at":"2026-08-05T09:24:53Z","locator":"catalog/pinmame.json entries tmac_a24, tmac_a18, tmac_g18; src/wpc/driver.c lines 471-473 date all three 12/88"},
		{"id":CORE_SOURCE,"kind":"pinmame_core","uri":"https://github.com/vpinball/pinmame","revision":PINMAME_REVISION,"license":"BSD-3-Clause","attribution":"vpinball/PinMAME contributors","acquired_at":"2026-08-05T09:24:53Z","locator":"src/wpc/degames.c lines 208 and 216-232: INITGAMES11(tmac, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, 0), parent a24 and two clones; the initializer leaves wpc.invSw zero-initialized and src/wpc/core.c lines 2455-2456 copy that zero mask into coreGlobals.invSw; src/wpc/s11.c lines 537-554 apply Data East permutation {3,4,5,1,0,2}, lines 618-623 bind handler indices 0-5, and PIA board comments at lines 714-715, 737-738, and 746-747 identify those handlers as printed SP6, SP5, SP2, SP3, SP1, and SP4; lines 1169-1173 provide Time Machine-specific output types and mux relay, plus core flipper/public-output code"},
		{"id":MANUAL_SOURCE,"kind":"manual","uri":MANUAL_URI,"sha256":MANUAL_SHA256,"locator":"Internet Archive item Data_East_Time_Machine_Manual, original file Data_East_1988_Time_Machine_Manual.pdf: 78 pages, 4,542,921 bytes. Item metadata says the file was originally downloaded from IPDB. Rendered pages 26-27 (printed 22-23), 28-29 (printed 24-25), 30-31 (printed 26-27), 67 (printed 47), 74 (printed 54), 76 (printed 56), and 77 (printed 57) decide the transcribed claims; PDF page 78 is blank.","license":"NOASSERTION","attribution":"Data East Pinball, Inc.; Internet Archive item uploaded by wouterdevlieger@gmail.com and described as originally downloaded from IPDB","source_id":"Data_East_Time_Machine_Manual","original_filename":MANUAL_FILENAME,"rights":"NOASSERTION","acquired_at":"2026-08-09T12:41:47Z","excerpts":excerpt_meta},
		{"id":TABLE_SOURCE,"kind":"vpx_table","uri":"external:pinmame-vpx-sources/data-east/time-machine-1988/Time Machine (Data East 1988) v.2.4.1.vpx","sha256":TABLE_SHA256,"revision":"2.4.1","known_working":True,"source_id":"retained-time-machine-2.4.1","original_filename":"Time Machine (Data East 1988) v.2.4.1.vpx","license":"Community table; redistribution terms not supplied","attribution":"Credited Time Machine table contributors","rights":"NOASSERTION","acquired_at":"2026-08-09T12:35:47Z","locator":"vpxtool git:0561bb4; 2389 extracted gameitem files; exact asserted bounds (0,0)-(1000,1910)"},
		{"id":SCRIPT_SOURCE,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/data-east/time-machine-1988/vpxtool-extract/script.vbs","sha256":SCRIPT_SHA256,"revision":"script from retained table 2.4.1","source_id":"retained-time-machine-2.4.1-script","original_filename":"script.vbs","license":"Community script; redistribution terms not supplied","attribution":"Credited Time Machine table-script contributors","rights":"NOASSERTION","acquired_at":"2026-08-09T12:35:55Z","locator":"Const cGameName=tmac_a24; UseSolenoids=2, UseLamps=1; HandleMechanics=0; vpmMapLights AllLamps; whole-line comments stripped before callback attribution; trough, VUK, three-position lock, kickback, flipper and sensor causality"},
		{"id":EXTRACTION_SOURCE,"kind":"vpx_table","uri":MANIFEST_PATH.as_posix(),"sha256":MANIFEST_CONTENT_SHA256,"revision":"vpxtool git:0561bb4","source_id":"retained-time-machine-2.4.1-extraction","original_filename":"time-machine-1988-extraction-manifest.json","license":"Repository-generated metadata under MIT; underlying community-table rights are unchanged","attribution":"Generated from the retained Time Machine 2.4.1 table with vpxtool git:0561bb4","rights":"NOASSERTION","acquired_at":"2026-08-09T12:35:55Z","locator":f"3049 files; 313925219 bytes; algorithm: {MANIFEST_ALGORITHM}; canonical manifest SHA-256 {MANIFEST_SHA256}; 2389 files under gameitems/"},
		{"id":RENDER_SOURCE,"kind":"human_review","uri":MANUAL_URI,"revision":"visual review 2026-08-09","sha256":MANUAL_SHA256,"license":"NOASSERTION","attribution":"Primary curator review of the retained Data East manual","rights":"NOASSERTION","acquired_at":"2026-08-09T12:41:47Z","locator":"Reviewed retained Archive.org renders at PDF pages 26-31, 67, 74, 76, and 77; every manual claim in the excerpts is limited to visible rendered-page content. PDF page 78 is blank."},
	]


def build_machine() -> dict[str, object]:
	inputs = diagnostic_inputs() + [switch_input(number) for number in range(1, 65)]
	outputs = [solenoid_output(number) for number in range(1, 51)] + [lamp_output(number) for number in range(1, 65)]
	return {
		"format":"pinmame-machine-definition", "schema_version":2,
		"machine":{"id":MACHINE_ID,"name":"Time Machine","manufacturer":"Data East","year":1988,"kind":"physical_pinball","playfield":{"width":1000.0,"height":1910.0,"units":"vpx","provenance":provenance("validated",TABLE_SOURCE)}},
		"coverage":{"status":"partial","missing":["controller_platform","output_semantics","mechanism_behavior","polarity","spatial_placement","unresolved_conflicts"],"dimensions":{"catalog_identity":"validated","controller_platform":"unknown","address_enumeration":"validated","semantic_naming":"conflicted","physical_wiring":"conflicted","mechanisms":"conflicted","variant_coverage":"validated","recreation_knowledge":"candidate","spatial_placement":"candidate"}},
		"controller":{"platform":"pinmame.dataeast","hardware_generation":"0x1000","inversion_applied_by_emulator":False},
		"drivers":[
			{"id":"tmac_a24","description":"Time Machine (2.4)","year":"1988","manufacturer":"Data East","flags":0,"physical_compatibility":"identical","variant_notes":"Clone-tree parent and retained-table ROM. Highest firmware revision; shared tmacGameData and physical definition."},
			{"id":"tmac_a18","clone_of":"tmac_a24","description":"Time Machine (1.8)","year":"1988","manufacturer":"Data East","flags":0,"physical_compatibility":"compatible","variant_notes":"Earlier English-language program ROMs; same INITGAMES11 physical GameData, display array, flipper declaration, and sound board as the parent."},
			{"id":"tmac_g18","clone_of":"tmac_a24","description":"Time Machine (1.8 German)","year":"1988","manufacturer":"Data East","flags":0,"physical_compatibility":"compatible","variant_notes":"German program ROM revision; same INITGAMES11 physical GameData, display array, flipper declaration, and sound board as the parent."},
		],
		"inputs":inputs, "outputs":outputs, "displays":displays(), "mechanisms":mechanisms(),
		"relationships":[{"id":f"relationship.lr-relay-{number}","kind":"relay_gated","source":"coil.driver-10","destination":f"coil.driver-{number}","provenance":provenance("validated",CORE_SOURCE,MANUAL_SOURCE)} for number in range(25,33)],
		"sources":sources(), "knowledge":{"path":KNOWLEDGE_PATH.as_posix(),"status":"partial"}, "conflicts":conflicts(),
	}


def build_spatial(machine: dict[str, object]) -> dict[str, object]:
	resolved = []
	for device in machine["inputs"] + machine["outputs"] + machine["displays"]:
		spatial = device.get("spatial")
		if isinstance(spatial, dict) and spatial.get("status") != "not_applicable":
			resolved.append({"id":device["id"],"status":spatial["status"],"placements":len(spatial["placements"])})
	conflict_ids = [conflict["id"] for conflict in machine["conflicts"]]
	all_lamps = [f"lamp.matrix-{number}" for number in range(1,65)]
	return {
		"format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,
		"coordinate_system":{"space":"playfield","x":"0 left, 1 right","y":"0 rear/backglass, 1 front/apron","normalization":"x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top)","raw_bounds":{"left":0.0,"top":0.0,"right":1000.0,"bottom":1910.0}},
		"evidence":{"manual_sha256":MANUAL_SHA256,"table_sha256":TABLE_SHA256,"script_sha256":SCRIPT_SHA256,"extraction_manifest_algorithm":MANIFEST_ALGORITHM,"extraction_manifest_sha256":MANIFEST_SHA256},
		"method":[
			"Asserted both exact gamedata.json bounds (0,0)-(1000,1910) before normalization; width agreement alone is insufficient.",
			"Removed whole-line VBScript comments before attributing callbacks or vpmMapLights membership.",
			"Resolved switch coordinates only from executable sensor objects or the native slingshot wall segment tied to that public address.",
			"Established the lamp idiom from executable vpmMapLights AllLamps plus each Light TimerInterval. The collection has 134 Light members: TimerInterval 1-64 map hardware addresses; sole TimerInterval 65 member l65 is unreachable from the 64-address controller matrix.",
			"Recorded numeric l1-l64 centers at candidate strength only where the manual places the lamp on the playfield. Backbox/back-panel lamps are controlled not_applicable records; lamp 25 has no placement because source locations conflict.",
			"Used script for causal topology and the rendered manual for construction. A printed feature label by itself never created a mechanism edge.",
		],
		"excluded_helpers":{"lamp_65":"l65 is an is_backglass=true hSpacewarpLights helper with TimerInterval 65. PinMAME publishes only lamp addresses 1-64, so ChangedLamps can never update slot 65; it is not a 65th output.","lamp_reflections":"Additional AllLamps members sharing TimerInterval values are reflection, bloom, or backglass presentation objects; they do not multiply physical ROM addresses.","backbox_lamps":"Manual construction places 1-8 and 62 on the insert/backbox presentation and 26-30 on the back panel; table coordinates are presentation proxies, not playfield emitters.","flash_groups":"Callbacks for Flash No.1-No.9 expose visual effects but neither script grouping nor generic manual labels establish surveyed physical bulb centers.","muxed_states_29_32":"The manual describes the full left/right multiplexing design as effectively 23 regular coils, and s11.c configures four individual emulator-published mux-state types at 29-32. The device chart stops at SIDE R 04, the script binds no callback, and no runtime trace establishes per-address activity, fitted circuit, quantity, feature, or socket for R05-R08."},
		"projection_classes":[
			{"class":"vpm-map-lights-coordinate-candidate","devices":[device for device in all_lamps if int(device.rsplit('-',1)[1]) not in BACKBOX_LAMPS | {25}],"status":"candidate","reason":"TimerInterval membership proves a runtime visual group; the numeric Light center is not a socket survey."},
			{"class":"mechanical-effect-object","devices":["coil.driver-16","coil.driver-18","coil.driver-19","coil.driver-21","coil.driver-25","coil.driver-26","coil.driver-27","coil.driver-28"],"status":"candidate","reason":"Direct callbacks and sensor geometry expose mechanism effect anchors rather than under-playfield coil centers."},
		],
		"resolved":sorted(resolved,key=lambda row:row["id"]),
		"unresolved":[
			{"dimension":"physical_socket_binding","devices":all_lamps,"reason":"Every playfield lamp coordinate remains candidate, cabinet lamps are deliberately not projected, and lamp 25 has a location conflict."},
			{"dimension":"flasher_placement","devices":[f"coil.driver-{number}" for number in [5,6,7,8,9,12,13,14,15,29,30,31,32]],"reason":"No source supplies an address-to-physical-bulb-center survey; static evidence does not establish activity, feature names, quantities, or socket locations for 29-32."},
			{"dimension":"special_coil_binding","devices":["coil.driver-17","coil.driver-22"],"reason":"The manual swaps right and center pop assignments between its table and drawing; pinned Data East routing establishes only that SP1 and SP2 publish as 17 and 22."},
		],
		"blockers":[
			{"dimension":"controller_platform","devices":["controller.platform"],"reason":"Time Machine is correctly classified as pinmame.dataeast, but no Data East controller profile is authored. A System 11 profile cannot stand in for the Data East address contract.","would_resolve":"A reviewed pinmame.dataeast controller profile that explicitly derives the Data East matrix, diagnostic, PIA, mux, and flipper-state rules from pinned PinMAME source."},
			{"dimension":"output_semantics","devices":["coil.driver-29","coil.driver-30","coil.driver-31","coil.driver-32"],"reason":"Pinned source configures four distinct emulator-published mux-state output types at 29-32, but static evidence does not prove runtime activity. The retained manual has no printed device row for these public states and the retained script registers no callback, so availability is unknown and no physical quantity or socket is claimed.","would_resolve":"A retained original-machine or LibPinMAME runtime trace that records each public state 29-32 under controlled relay conditions, paired with a source-backed circuit or socket survey."},
			{"dimension":"mechanism_behavior","devices":["coil.driver-17","coil.driver-18","coil.driver-19","coil.driver-21","coil.driver-22"],"reason":"Hardware-triggered special-coil pulse timing is absent from the retained public callbacks, and SP1/SP2 physical assignment conflicts.","would_resolve":"Original-machine captures of each bumper/slingshot switch and special-solenoid state, with right and center bumpers exercised separately."},
			{"dimension":"polarity","devices":["switch.matrix-15","switch.matrix-16","coil.driver-45","coil.driver-46","coil.driver-47","coil.driver-48"],"reason":"Physical EOS contacts and controller-facing button/synthetic winding states share public meanings without an at-rest/end-of-stroke bench capture.","would_resolve":"Bench capture of cabinet button, EOS at rest/end of stroke, and public power/hold states on an original machine or faithful harness."},
			{"dimension":"spatial_placement","devices":all_lamps+[f"coil.driver-{number}" for number in [5,6,7,8,9,12,13,14,15,17,22,29,30,31,32]],"reason":"Lamp positions are table candidates, two pop actuators conflict, and flash groups lack socket-level coordinates.","would_resolve":"A photographed socket/address survey above and below an original playfield plus the backbox/back-panel lamp boards."},
			{"dimension":"unresolved_conflicts","devices":conflict_ids,"reason":"Five machine-specific source disagreements remain first-class and promotion-critical.","would_resolve":"Corrected upstream sources or independent original-machine traces that explicitly settle each conflicting state."},
		],
		"conflicts":conflict_ids,
		"promotion_decision":"Keep partial. The Data East controller profile, runtime activity of mux states 29-32, SP1/SP2 placement, EOS/button semantics, lamp 25 location, special-coil behavior, polarity, and socket-level placement remain unresolved.",
	}


def spatial_markdown(report: dict[str, object]) -> str:
	rows = ["# Time Machine spatial-resolution report", "", "Exact retained-table bounds: `left=0`, `top=0`, `right=1000`, `bottom=1910`.", "", "The resolver fails if either right or bottom changes. Coordinates use player-view playfield space; backbox and service devices are never projected onto it.", "", "## Extraction identity", "", f"- Manifest algorithm: {report['evidence']['extraction_manifest_algorithm']}", f"- Manifest SHA-256: `{report['evidence']['extraction_manifest_sha256']}`", "", "## Promotion decision", "", report["promotion_decision"], "", "## Blockers", ""]
	for blocker in report["blockers"]:
		rows.extend([f"### {blocker['dimension']}", "", blocker["reason"], "", f"Would resolve: {blocker['would_resolve']}", "", "Devices: " + ", ".join(f"`{device}`" for device in blocker["devices"]), ""])
	rows.extend(["## Resolver controls", ""] + [f"- {method}" for method in report["method"]] + ["", "## Excluded helpers", ""] + [f"- `{key}`: {value}" for key,value in report["excluded_helpers"].items()] + [""])
	return "\n".join(rows)


def knowledge_markdown(machine: dict[str, object]) -> str:
	missing = ", ".join(f"`{value}`" for value in machine["coverage"]["missing"])
	return f"""# Data East Time Machine (1988)

Machine definition: `{MACHINE_PATH.as_posix()}`

## Identity and controller contract

Pinned PinMAME defines `tmac_a24` as the clone-tree parent, with `tmac_a18` and `tmac_g18` cloning it. All three catalog rows are dated 12/88. The physical declaration is `INITGAMES11(tmac, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, 0)`. The parent is the highest revision because that is what the macro says; no revision-order rule was inferred.

`de_dispAlpha2` supplies two seven-character alphanumeric and two seven-character numeric displays. They are controlled backbox devices and have explicit `not_applicable` playfield-spatial records. The machine is correctly bound to `pinmame.dataeast`; no Data East controller profile is authored, so `controller_platform` remains a concrete coverage blocker rather than borrowing the System 11 profile. `INITGAMES11` leaves Time Machine's `wpc.invSw` array zero-initialized, and `core.c` copies that zero mask into `coreGlobals.invSw`, so the emulator applies no per-game switch inversion for any of the three drivers.

## Address coverage

- Inputs: service switches -7/-6, DIP/jumper address 0, and every matrix address 1-64.
- Outputs: every lamp address 1-64 and every Data East public solenoid address 1-50.
- Solenoid 23 is the Game On/control signal; 24 is unused; 33-44 are inert; 45-48 are synthetic lower-flipper winding states; 49 is a simulation-only shooter state; 50 is reserved.
- Solenoid 10 is the left/right mux relay. Its public right bank is 25-32. The manual says the complete left/right arrangement effectively provides 23 regular coils, while its device chart names only SIDE R 01-04. Manual and script resolve mechanisms only at 25-28; pinned source configures four distinct emulator-published mux states at 29-32, but no retained runtime trace proves their per-address activity and no retained source identifies fitted physical circuits for SIDE R 05-08.

## Lamp mapping and the 65th object

The active script calls `vpmMapLights AllLamps`. Shared VPM uses each Light's `TimerInterval` as its ROM lamp index. The collection contains 134 Light members and covers TimerInterval 1-65. Addresses 1-64 are the complete hardware matrix. The sole TimerInterval-65 member is `l65`, an `is_backglass=true` presentation helper on `hSpacewarpLights`; the controller never publishes lamp 65, so it is deliberately excluded rather than counted as an output.

Lamp 25 remains conflicted: the manual explicitly prints `2X All Scores Cntr Plyfld`, but the collection's sole TimerInterval-25 object is marked backglass. No coordinate is selected. Backbox/back-panel lamps are also kept off the playfield coordinate plane even when the retained table uses in-bounds presentation proxies.

## Mechanism topology

The script supplies causality and the manual supplies construction. Together they establish a serial three-ball trough, an outhole feeder, a three-position visible lock released by one cam/coil assembly, a separate super VUK reached from an under-playfield path, the Laser Kick outlane kickback, two flippers, two slingshots, three pop bumpers, three independent fixed three-target standup banks, a manual shooter, and fixed ramp/wireform paths. The standup banks are not drop-target banks: the manual assembly shows switch/bracket targets and no reset coil.

The special-solenoid table and location drawing swap SP1/SP2 between the right and center pop bumpers. Pinned `s11.c` PIA comments identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4; applying `setSSSol`'s Data East offsets `{3,4,5,1,0,2}` derives SP1, SP3, SP4, SP6, SP5 and SP2 at public addresses 17-22. This is not inferred by treating printed SP numbers as handler indices. The right/center mechanisms keep empty actuator lists until an original-machine capture settles the disagreement; SP3, SP4, and SP5 agree as left sling, left pop, and right sling, while SP6 is unfitted.

## Manual transcription policy

The retained Archive.org manual is a 78-page, 4,542,921-byte scan with SHA-256 `{MANUAL_SHA256}`. Only visible rendered-page content is used: PDF 26-27 = printed 22-23 (switches), 28-29 = printed 24-25 (lamps), 30-31 = printed 26-27 (coils), 67 = printed 47 (parts list), 74 = printed 54 (three-bank standups), 76 = printed 56 (lock bracket), and 77 = printed 57 (super VUK). PDF 78 is blank.

## Retained table and geometry

The retained table SHA-256 is `{TABLE_SHA256}` and binds the correct parent with `Const cGameName = "tmac_a24"`. Its exact bounds are 1000 by 1910. Both values are asserted before normalization. Whole-line VBScript comments are removed before any callback or mapping claim; inline executable code remains.

## Coverage and blockers

Status remains `partial`. `coverage.missing` is [{missing}].

- `controller_platform`: the Data East platform has no authored controller profile.
- `output_semantics`: public 29-32 are distinct emulator-published mux states whose runtime activity, physical quantity, and circuit identity are untraced.
- `mechanism_behavior`: hardware-triggered special-coil timing is not exposed, and SP1/SP2 assignment conflicts.
- `polarity`: FLIP1516 publishes cabinet-button state where the manual prints physical EOS contacts; no bench capture reconciles rest/end-of-stroke state.
- `spatial_placement`: lamp coordinates are table candidates, flash groups lack socket surveys, and the conflicted outputs have no selected position.
- `unresolved_conflicts`: five source disagreements remain recorded in the definition and spatial report.

## Recreation boundary

Recreate only the explicitly mapped addresses and topologies. Do not invent activity, physical quantities, or feature names for public mux states 29-32. Also do not treat presentation helpers as extra hardware, convert the fixed target banks into drop targets, or infer physical switch/coil polarity from controller-normalized public state.
"""


LEDGER_BLOCK = """Data East Time Machine (`data-east.time-machine.1988`) was corrected on 2026-08-09 in its isolated worktree. It remains `partial` with `coverage.missing = ["controller_platform", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"]` and five unresolved source conflicts. The retained geometry is exactly 1000 by 1910, and both extents are asserted before normalization.

Four things from it generalise.

1. **An emulator-published output type is not runtime evidence.** Time Machine's `s11.c` short-name block configures four distinct mux-state types at public 29-32, while the retained manual and active table resolve only the first four right-bank devices at 25-28. Without a trace, the remaining states are `unknown` availability with no physical quantity, rather than either live hardware or dead address space.
2. **A collection-driven lamp mapper can contain more numeric Light names than the controller has addresses.** `vpmMapLights` indexes each member by `TimerInterval`; TimerInterval 1-64 cover the hardware matrix, while sole member `l65` targets unreachable slot 65 and is a backglass presentation helper. Count controller addresses first, then explain every extra object.
3. **Data East is not a substitute name for the System 11 profile.** Time Machine shares emulator implementation paths with System 11, but its platform record is `pinmame.dataeast`; it remains a controller-platform blocker until an explicit Data East profile is independently derived. Construction and causality likewise remain separate: the script proves a three-position serial lock released through one output, while the retained Archive.org manual's assembly drawing proves one cam, spring-return plunger and coil.
4. **Data East's printed SP1-SP6 order is not PinMAME public 17-22 order.** `src/wpc/s11.c` PIA comments identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4; applying the Data East `ssSolNo` offsets `{3,4,5,1,0,2}` derives printed SP1, SP3, SP4, SP6, SP5 and SP2 at public 17-22. On Time Machine that moves the unfitted SP6 circuit to public 20, places the known left sling/left pop/right sling at 18/19/21, and leaves the conflicting right/center SP1/SP2 pair at 17/22. Preserve the printed SP identity as a manual alias and derive the public binding from both the handler comments and permutation; sequentially assigning SP1-SP6 to 17-22 silently mislabels five of six addresses.

The physical family is the three-driver `tmac_*` clone tree (`tmac_a24` parent plus English `tmac_a18` and German `tmac_g18` firmware); all share the same physical game-data declaration.

"""


def merge_ledger(current: str) -> str:
	anchor = "Data East Time Machine (`data-east.time-machine.1988`)"
	if LEDGER_BLOCK in current:
		return current
	if anchor in current:
		raise ValueError("Time Machine ledger entry exists but differs from the generated block")
	marker = "Before selecting a game, check this ledger"
	if marker not in current:
		raise ValueError("CURRENT-STATE insertion marker missing")
	return current.replace(marker, LEDGER_BLOCK + marker, 1)


def json_text(value: object) -> str:
	return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def desired_files() -> dict[Path, str]:
	machine = build_machine()
	spatial = build_spatial(machine)
	files = {
		MACHINE_PATH: json_text(machine), SEED_PATH: json_text(machine), SPATIAL_JSON_PATH: json_text(spatial),
		SPATIAL_MD_PATH: spatial_markdown(spatial), KNOWLEDGE_PATH: knowledge_markdown(machine), **EXCERPTS,
	}
	return files


def compare_lf(path: Path, expected: str) -> bool:
	return path.is_file() and path.read_text(encoding="utf-8").replace("\r\n","\n") == expected.replace("\r\n","\n")


def coverage_markdown(report: dict[str, object]) -> str:
	return f"""# Machine-definition coverage

PinMAME revision: `{report['pinmame_revision']}`

Author-ready coverage: **{report['author_ready_count']} / {report['machine_count']} physical-machine records ({report['author_ready_percent']:.4f}%)**

- In-scope drivers: {report['driver_count']}
- Catalog records: {report['catalog_record_count']} ({report['non_game_record_count']} diagnostic/system-software records excluded from game coverage)
- Explicit stubs: {report['stub_count']}
- Partial definitions: {report['partial_count']}
- Author-ready definitions: {report['author_ready_count']}
- Completion gate: {'PASS' if report['completion_gate'] else 'FAIL'}

Stubs and partial definitions are not usable completion credit. A clone driver contributes coverage only through its fully resolved physical-machine definition.
"""


def queue_markdown(queue: dict[str, object]) -> str:
	rows = ["# Curation queue", "", "Physical machines are processed newest-to-oldest. Unknown-year candidates are last, and related driver variants stay together.", "", "| Order | Year | Machine | Manufacturer | Status |", "| ---: | ---: | --- | --- | --- |"]
	for entry in queue["entries"]:
		year = str(entry["year"]) if entry["year"] is not None else "unknown"
		rows.append(f"| {entry['order']} | {year} | {entry['name']} | {entry['manufacturer']} | {entry['coverage_status']} |")
	return "\n".join(rows) + "\n"


def generate() -> None:
	for relative, content in desired_files().items():
		write_text(ROOT / relative, content.replace("\r\n","\n"))
	for path in [ROOT / STUB_PATH, ROOT / STUB_KNOWLEDGE_PATH]:
		if path.exists(): path.unlink()
	ledger_path = ROOT / "docs/CURRENT-STATE.md"
	write_text(ledger_path, merge_ledger(ledger_path.read_text(encoding="utf-8").replace("\r\n","\n")))
	rebuild_catalog(ROOT)
	write_coverage_report(ROOT)


def check() -> None:
	evidence_errors = []
	vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if vpx_root:
		vpx_base = Path(vpx_root) / "data-east" / "time-machine-1988"
		for path, expected in (
			(vpx_base / "Time Machine (Data East 1988) v.2.4.1.vpx", TABLE_SHA256),
			(vpx_base / "vpxtool-extract" / "script.vbs", SCRIPT_SHA256),
		):
			if not path.is_file(): evidence_errors.append(f"missing {path}")
			elif sha256_file(path) != expected: evidence_errors.append(f"digest mismatch {path}")
	manual_root = os.environ.get("PINMAME_MANUALS_ROOT")
	if manual_root:
		manual = Path(manual_root) / "by-machine" / MACHINE_ID / "archive-org" / MANUAL_FILENAME
		if not manual.is_file(): evidence_errors.append(f"missing {manual}")
		elif sha256_file(manual) != MANUAL_SHA256: evidence_errors.append(f"digest mismatch {manual}")
	if evidence_errors: raise SystemExit("evidence: " + ", ".join(evidence_errors))
	drift = [relative.as_posix() for relative,content in desired_files().items() if not compare_lf(ROOT / relative, content)]
	if (ROOT / STUB_PATH).exists() or (ROOT / STUB_KNOWLEDGE_PATH).exists(): drift.extend([STUB_PATH.as_posix(),STUB_KNOWLEDGE_PATH.as_posix()])
	ledger = (ROOT / "docs/CURRENT-STATE.md").read_text(encoding="utf-8").replace("\r\n","\n")
	if LEDGER_BLOCK not in ledger: drift.append("docs/CURRENT-STATE.md")
	catalog = load_json(ROOT / "catalog/pinmame.json")
	machine_rows = [row for row in catalog["machines"] if row["id"] == MACHINE_ID]
	if len(machine_rows) != 1 or machine_rows[0].get("definition") != MACHINE_PATH.as_posix() or machine_rows[0].get("definition_sha256") != content_sha256(build_machine()):
		drift.append("catalog/pinmame.json")
	driver_rows = {row["id"]:row for row in catalog["drivers"]}
	for driver_id in {"tmac_a24","tmac_a18","tmac_g18"}:
		row = driver_rows.get(driver_id,{})
		if row.get("machine_id") != MACHINE_ID or row.get("definition") != MACHINE_PATH.as_posix(): drift.append("catalog/pinmame.json")
	coverage = build_coverage_report(ROOT)
	queue = build_curation_queue(ROOT)
	generated = {
		Path("reports/coverage.json"):json_text(coverage), Path("reports/coverage.md"):coverage_markdown(coverage),
		Path("reports/curation-queue.json"):json_text(queue), Path("reports/curation-queue.md"):queue_markdown(queue),
	}
	drift.extend(relative.as_posix() for relative,content in generated.items() if not compare_lf(ROOT / relative,content))
	if drift: raise SystemExit("drift: " + ", ".join(sorted(set(drift))))


def main() -> int:
	parser = argparse.ArgumentParser(description="Generate the reviewed Data East Time Machine physical-machine record")
	parser.add_argument("--check", action="store_true", help="refuse generated-artifact drift; CRLF and LF compare equally")
	args = parser.parse_args()
	if args.check: check()
	else: generate()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
