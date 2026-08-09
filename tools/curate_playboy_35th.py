"""Self-contained deterministic curator for Data East Playboy 35th Anniversary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pinmame_game_defs.coverage import build_coverage_report, build_curation_queue, write_coverage_report
from pinmame_game_defs.jsonio import content_sha256, load_json, write_text
from pinmame_game_defs.registry import rebuild_catalog


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
PINMAME_SHORT = PINMAME_REVISION[:12]
MACHINE_ID = "data-east.playboy-35th-anniversary.1989"
MACHINE_PATH = Path("machines/partial/data-east/playboy-35th-anniversary-1989.json")
AUTHOR_READY_PATH = Path("machines/author-ready/data-east/playboy-35th-anniversary-1989.json")
SEED_PATH = Path("tools/seeds/data-east/playboy-35th-anniversary-1989.json")
SPATIAL_JSON_PATH = Path("reports/spatial/data-east/playboy-35th-anniversary-1989.json")
SPATIAL_MD_PATH = Path("reports/spatial/data-east/playboy-35th-anniversary-1989.md")
KNOWLEDGE_PATH = Path("knowledge/data-east/playboy-35th-anniversary-1989.md")
STUB_PATH = Path("machines/stubs/play_a24.json")
STUB_KNOWLEDGE_PATH = Path("knowledge/stubs/play_a24.md")
MANIFEST_PATH = Path("tools/seeds/data-east/playboy-35th-anniversary-1989-extraction-manifest.json")

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_SHORT}"
CORE_SOURCE = f"pinmame.core.{PINMAME_SHORT}"
MANUAL_SOURCE = "manual.data-east.playboy-35th-anniversary.1989"
TABLE_SOURCE = "vpx-table.playboy-35th-hybrid-1.1"
SCRIPT_SOURCE = "vpx-script.playboy-35th-hybrid-1.1"
EXTRACTION_SOURCE = "vpx-extraction.playboy-35th-hybrid-1.1"
RENDER_SOURCE = "human-review.playboy-35th-manual-renders"

MANUAL_FILENAME = "Data_East_1989_Playboy_35th_Anniversary_English_Manual_with_schematics.pdf"
TABLE_FILENAME = "Playboy 35th Anniversary (Data East 1989) Physics Sound Hybrid MOD 1.1.vpx"
MANUAL_SHA256 = "0c4be366c30942919b7101c69acfb6563ac8bc6cd5aaaac0bad24ae5b9b1afa7"
TABLE_SHA256 = "3b32aeacee1c5beb1c723e6e1bba79ae269deb36cc56101201b5d171a7a8336b"
SCRIPT_SHA256 = "83e632d397afbec660ea356b1820aadbd648d0a90d4affdce5bfc4e864bb0da5"
MANIFEST_ALGORITHM = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
MANIFEST_CONTENT_SHA256 = "228204226a90f8974c46d30ef4d9b24c24852099ddccf8f8c743cd4051eaadaf"
MANIFEST_SHA256 = "408ba0ec4e18187f0f86c1970c33cc31b93af53df24ad83f2eeea599822bb672"
RIGHT = 952.0
BOTTOM = 1974.0

SWITCH_DRIVES = ["GRN-BRN", "GRN-RED", "GRN-ORN", "GRN-YEL", "GRN-BLK", "GRN-BLU", "GRN-VIO", "GRN-GRY"]
SWITCH_RETURNS = ["WHT-BRN", "WHT-RED", "WHT-ORN", "WHT-YEL", "WHT-GRN", "WHT-BLU", "WHT-VIO", "WHT-GRY"]
LAMP_DRIVES = ["YEL-BRN", "YEL-RED", "YEL-ORN", "YEL-BLK", "YEL-GRN", "YEL-BLU", "YEL-VIO", "YEL-GRY"]
LAMP_RETURNS = ["RED-BRN", "RED-BLK", "RED-ORN", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY"]

SWITCH_LABELS = {
    1:"Plumb Tilt",2:"Not Used",3:"Credit Button",4:"Right Coin",5:"Center Coin",6:"Left Coin",7:"Slam Tilt",8:"Not Used",
    9:"Not Used",10:"Outhole",11:"Trough #1",12:"Trough #2",13:"Trough #3",14:"Shooter Lane",15:"Left EOS",16:"Right EOS",
    17:"Left Outlane",18:"Left Return",19:"Right Outlane",20:"Right Return",21:"Left Slingshot",22:"Right Slingshot",23:"Champagne Kicker",24:"Grotto 1",
    25:"Left Top Lane",26:"Center Top Lane",27:"Right Top Lane",28:"Ramp Center",29:"Ramp Right",30:"Left Spinner",31:"Grotto 2",32:"Ramp Left",
    33:"P Target",34:"L Target",35:"A Target",36:"1st Y Target",37:"B Target",38:"O Target",39:"2nd Y Target",40:"Not Used",
    41:"Center 3 Bank Left",42:"Center 3 Bank Middle",43:"Center 3 Bank Right",44:"Not Used",45:"VUK",46:"Left Pop Bumper",47:"Center Pop Bumper",48:"Right Pop Bumper",
    49:"Drop1 Top",50:"Drop2 Center",51:"Drop3 Bottom",
}
for _number in range(52,65):
    SWITCH_LABELS[_number] = "Not Used"

SWITCH_MATRIX_LABELS = {
    1:"Plumb Tilt",2:"Not Used",3:"Credit Button",4:"Right Coin",5:"Center Coin",6:"Left Coin",7:"Slam Tilt",8:"Not Used",
    9:"Not Used",10:"Outhole",11:"Trough #1",12:"Trough #2",13:"Trough #3",14:"Shooter Lane",15:"Left EOS",16:"Right EOS",
    17:"Left Outlane",18:"Left Return",19:"Right Outlane",20:"Right Return",21:"Left Slingsht",22:"Right Slingsht",23:"Champ. Kicker",24:"Grotto 1",
    25:"Left Top Lane",26:"Cntr.Top Lane",27:"RightTop Lane",28:"Ramp Center",29:"Ramp Right",30:"Left Spinner",31:"Grotto 2",32:"Ramp Left",
    33:"P Target",34:"L Target",35:"A Target",36:"1st Y Target",37:"B Target",38:"O Target",39:"2nd Y Target",40:"Not Used",
    41:"Ctr 3 Bank-Lft",42:"Ctr 3 Bank-Mid",43:"Ctr 3 Bank-Rt.",44:"Not Used",45:"VUK",46:"Left Pop",47:"Center Pop",48:"Right Pop",
    49:"Drop 1 Top",50:"Drop 2 Center",51:"Drop 3 Bottom",
}
for _number in range(52,65):
    SWITCH_MATRIX_LABELS[_number] = "Not Used"

SWITCH_PARTS = {
    1:"500-5023-00",3:"500-5097-00",4:"180-5024-00",5:"180-5024-00",6:"180-5024-00",7:"180-5022-00",
    10:"180-5011-00",11:"180-5009-00",12:"180-5009-00",13:"180-5010-00",14:"500-5142-00",
    15:"180-5026-00 / 180-5018-00",16:"180-5026-00 / 180-5018-00",17:"500-5143-00",18:"180-5003-00",19:"515-5138-00",20:"180-5003-00",
    21:"180-5054-00 / 180-5055-00",22:"180-5054-00 / 180-5055-00",23:"180-5040-00",24:"180-5028-00",
    25:"515-5138-00",26:"515-5138-00",27:"515-5138-00",28:"180-5010-00",29:"180-5010-00",30:"180-5004-00",31:"180-5040-00",32:"180-5034-00",
    33:"515-5124-18",34:"515-5124-08",35:"515-5124-18",36:"515-5124-18",37:"515-5124-18",38:"515-5124-18",39:"515-5124-18",
    41:"515-5124-18",42:"515-5124-18",43:"515-5124-18",45:"180-5041-00",46:"180-5036-00",47:"180-5036-00",48:"180-5036-00",
    49:"180-5025-01",50:"180-5025-01",51:"180-5025-01",
}

LITERAL_SWITCH_DETAILS = {
    15:"Left Flip. Instant Info.; Left EOS",16:"Right Flip. Instant Info.; Right EOS",
    10:"Out Hole",18:"Left Return Lane",20:"Right Return Lane",
    21:"Left Slingshot Trigger Sw.; Left Slingshot Point Sw.",22:"Right Slingshot Trigger Sw.; Right Slingshot Point Sw.",
    23:"Champagne Kicker",24:"Grotto 1",26:"Center Top Lane",27:"Right Top Lane",31:"Grotto 2",32:"Ramp Left",
    33:"P -Target",34:"L -Target",35:"A -Target",36:"1st Y -Target",37:"B -Target",38:"O -Target",39:"2nd Y -Target",
    49:"Drop 1 (Top)",50:"Drop 2 (Center)",51:"Drop 3 (Bottom)",
}

RAW_SWITCH_POINTS = {
    10:(503.4922,1924.6423),13:(839.1214,1686.0396),14:(899.6983,1763.0642),
    17:(53.316788,1590.0859),
    18:(120.726524,1417.8425),19:(807.4985,1453.0219),20:(742.31104,1417.281),
    21:(271.99661833333334,1420.6663833333332),22:(663.5801566666667,1424.2055666666668),23:(189.14418,1419.1357),24:(53.470776,653.7492),
    25:(455.21185,182.09973),26:(554.58307,182.09978),27:(650.7575,179.16927),28:(893.2316,236.94464),29:(825.41754,593.1829),
    30:(318.76398,438.3393),31:(53.1167,723.741),32:(335.05573,87.82193),
    33:(108.691414,1013.03705),34:(113.037125,963.2591),35:(117.38282,912.6912),36:(120.54331,862.12335),37:(124.888985,811.1602),38:(128.04948,762.1726),39:(131.60507,710.8145),
    41:(430.535,675.32513),42:(472.93832,702.9793),43:(516.1316,730.8969),45:(340.25998,179.71999),
    46:(425.21634,346.2234),47:(633.7957,342.58536),48:(543.24976,539.0381),
    49:(810.94946,884.98676),50:(817.2704,945.78156),51:(822.88916,998.69055),
}

LAMP_MATRIX_LABELS = [
    "Playboy","pLayboy","plAyboy","plaYboy","playBoy","playbOy","playboY",'Lt."H" Lane',
    "Miss July 50k","Miss Aug. 100k","Miss Sept.","Miss Oct.","Miss Nov.","Miss Dec.","Top Left BunnyHop",'Ctr."M" Lane',
    "Photo Shoot 1","Photo Shoot 2","Photo Shoot 3","Photo Shoot 4","Photo Shoot 5","Photo Special","Spinner X-Ball",'Rt."H" Lane',
    "Up L&R Release","Lock Ball #1","Lock Ball Arr.","Left Grn Arr.Tar.","Ctr.Grn Arr.Tar.","Rt.Green Arr.Tar.","Mult.All Scores","Lock Ball #2",
    "Up Rt. Man.Pty","Bonus Hold","Play Again","2X","3X","4X","5X","Up.Left Man.Ply.",
    "Pinball","Rt.Score PBValue","Right Peacock","DropTar. 100K","DropTar. 75K","DropTar. 50K","DropTar. 25K","Up.Rt. BunnyHop",
    "pInball","Lt.Score PBValue","Left Peacock","Lwr.Lft. BunnyHop","piNball","pinBall","pinbAll","pinbaLl",
    "Mansion","mAnsion","maNsion","manSion","mansIon","mansiOn","mansioN","pinbalL.",
]
LAMP_LIST_LABELS = [
    '"P"layboy','p"L"ayboy','pl"A"yboy','pla"Y"boy','play"B"oy','playb"O"y','playbo"Y"','Left "H" Lane',
    "Miss July 50K","Miss August 100k","Miss September Lites Out-lane 50k","Miss October 50K Bonus Hold Over","Miss November Extra Ball","Miss December 1,000,000","Top Left Bunny Hop",'Center "M" Lane',
    "Photo Shoot 1","Photo Shoot 2","Photo Shoot 3","Photo Shoot 4","Photo Shoot 5","Photo Shoot Special","Spinner Extra Ball",'Right "H" Lane',
    "Upper Left and Right Release Ball","Lock Ball #1","Lock Ball (Big arrow)","Left Green Arrow Target","Center Green Arrow Target","Right Green Arrow Target","Multiply All Scores","Lock Ball #2",
    "Upper Right Mansion Party","Bonus Holdover","Play Again","2x","3x","4x","5x","Upper Left Mansion Party",
    '"P"inball',"Rt Score Playboy Value","Right Peacock","Drop Target 100k","Drop Target 75k","Drop Target 50k","Drop Target 25k","Upper Right Bunny Hop",
    'p"I"nball',"Lt.Score Playboy Value","Left Peacock","Lwr Lft.Bunny Hop",'pi"N"ball','pin"B"all','pinb"A"ll','pinba"L"l',
    '"M"ansion','m"A"nsion','ma"N"sion','man"S"ion','mans"I"on','mansi"O"n','mansio"N"','pinbal"L".',
]

RAW_LAMP_POINTS = {
    1:[(190.80855,1092.7064)],2:[(193.30258,1034.7687)],3:[(194.83737,975.2956)],4:[(197.52324,916.5899)],5:[(198.86618,857.3089)],6:[(200.40097,796.8767)],7:[(201.93575,736.0607)],8:[(454.01813,67.79563)],
    9:[(274.54565,1233.0752)],10:[(279.62598,1147.3208)],11:[(286.6493,1062.5724)],12:[(291.0974,977.82477)],13:[(299.29117,894.31757)],14:[(302.28812,806.26825)],15:[(266.06287,688.852)],16:[(554.75433,65.457016)],
    17:[(353.82452,1346.5924)],18:[(360.6283,1260.8644)],19:[(366.58902,1175.5494)],20:[(373.27026,1089.4951)],21:[(378.18655,1003.3428)],22:[(385.04654,919.41534)],23:[(339.95993,702.57025)],24:[(654.59454,64.40791)],
    25:[(798.6131,642.803),(171.94186,465.1077)],27:[(332.3807,614.57574)],28:[(419.08667,760.0203)],29:[(468.0293,793.4446)],30:[(516.4603,826.18665)],31:[(516.26807,926.8222)],
    33:[(778.2789,700.9844)],34:[(468.32938,1471.8823)],35:[(469.55853,1659.0533)],36:[(389.6028,1554.5789)],37:[(441.79013,1568.5745)],38:[(497.03275,1568.5745)],39:[(549.22003,1554.5789)],40:[(186.21942,524.971)],
    41:[(46.623077,273.47015)],42:[(810.47687,1339.3601)],43:[(746.59015,1304.9501),(743.6137,1243.1812)],44:[(652.1609,947.56415)],45:[(659.10754,1003.257)],46:[(664.1378,1063.6208)],47:[(673.00073,1119.195)],48:[(680.30646,846.2388)],
    49:[(78.38416,273.78235)],50:[(55.686993,1336.6099)],51:[(120.70337,1305.2699),(119.5741,1247.5087)],52:[(54.463993,1428.373)],53:[(110.3792,273.62628)],54:[(141.57375,274.0166)],55:[(173.10051,273.9386)],56:[(204.54953,273.7825)],64:[(236.62259,273.15826)],
}
BACKBOX_LAMPS = {26,32,57,58,59,60,61,62,63}
MANUAL_UNLOCATED_PINBALL_LAMPS = {41,49,53,54,55,56,64}

RAW_FLASH_POINTS = {
    1:[(252.19948,275.5784)],2:[(54.08992,114.64898)],3:[(323.05838,514.11365)],4:[(316.33633,434.57153)],5:[(310.45468,353.62897)],
    6:[(516.26807,926.8222)],7:[(166.71355,360.44687)],8:[(561.607,1220.7957)],
    9:[(55.199722,811.08484),(57.141983,1047.4845),(53.884335,811.74255),(54.542023,1033.3853)],
    12:[(81.599976,307.64102),(126.53695,223.29956),(193.16841,152.01721)],13:[(743.6606,952.7933)],14:[(829.04767,547.055)],15:[(815.39935,97.10683)],
}

RAW_GI_POINTS = [
    (239.96535,1459.8373),(147.20518,1550.933),(713.7972,1593.0931),(694.9721,1458.9991),(836.85205,1197.7324),(93.71261,1111.2203),
    (846.65686,417.61713),(835.7201,289.1091),(902.7082,51.232708),(193.78809,62.853157),(53.431927,184.98126),(404.22516,166.03847),
    (503.7889,171.8486),(503.3618,166.99864),(602.2055,171.36852),(601.7784,166.51855),(703.6895,171.20851),(703.2624,166.35857),
    (848.4956,940.18494),(55.74163,985.26105),(463.25656,660.7852),(512.40936,692.55457),(100.60479,545.99536),(46.65655,1095.6678),
    (240.00438,1460.7836),(715.51825,1593.8115),(695.6262,1460.7244),(835.34393,1198.3392),(847.6581,940.9302),(512.3356,692.9872),
    (464.50003,661.7283),(404.65228,170.88843),(94.024345,1111.4034),(46.872868,1096.2474),(56.13479,985.10474),(270.42117,532.9561),
    (53.187824,185.21455),(193.80011,62.704895),(834.83514,291.02475),(848.30695,419.0072),(145.66711,1551.1079),
    (633.4705,351.8896),(633.4705,352.9431),(543.3639,537.53986),(543.3639,548.2441),(424.48688,355.36832),(424.48688,354.3148),
]


def excerpt_switch_matrix() -> str:
    rows = [
        "# Playboy 35th Anniversary switch matrix transcription", "",
        "Source: PDF pages 25-26, printed pages 22-23. Render-decided at 400 dpi; the PDF text layer and OCR were locator/second-reading aids only.", "",
        "The matrix is transcribed column-major. Printed labels, `Not Used` cells, and the adjacent part-number list are preserved before reconciliation.", "",
        "Printed drive headers: `GRN-BRN (51) Q55`, `GRN-RED (52) Q54`, `GRN-ORN (53) Q53`, `GRN-YEL (54) Q52`, `GRN-BLK (50) Q51`, `GRN-BLU (56) Q50`, `GRN-VIO (57) Q49`, `GRN-GRY (58) Q48`.", "",
        "Printed return headers: `WHT-BRN (91)`, `WHT-RED (92)`, `WHT-ORN (93)`, `WHT-YEL (94)`, `WHT-GRN (95)`, `WHT-BLU (96)`, `WHT-VIO (97)`, `WHT-GRY (98)`.", "",
        "| Row / return | GRN-BRN | GRN-RED | GRN-ORN | GRN-YEL | GRN-BLK | GRN-BLU | GRN-VIO | GRN-GRY |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row, return_wire in enumerate(SWITCH_RETURNS):
        cells = [f"{column * 8 + row + 1} {SWITCH_MATRIX_LABELS[column * 8 + row + 1]}" for column in range(8)]
        rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
    rows.extend(["", "## Printed description-list details", ""])
    for number in range(1,52):
        detail = LITERAL_SWITCH_DETAILS.get(number, SWITCH_LABELS[number])
        part = SWITCH_PARTS.get(number)
        mark = " *" if number in {1,4,5,6,7} else ""
        rows.append(f"- {number}: {detail}{mark}" + (f" — `{part}`" if part else ""))
    rows.append("- 52: Not Used Thru 64")
    rows.extend(["", "Printed footnote: `*INDICATES CABINET SWITCHES.`", ""])
    return "\n".join(rows)


def excerpt_lamp_matrix() -> str:
    rows = [
        "# Playboy 35th Anniversary lamp matrix transcription", "",
        "Source: PDF pages 27-28, printed pages 24-25. Render-decided at 400 dpi; the PDF text layer and OCR were locator/second-reading aids only.", "",
        "The matrix-sheet wording and adjacent lamp-description wording are kept separately. Capitalization, quoting, abbreviations, and printed inconsistencies are not silently normalized.", "",
        "Printed drive headers: `YEL-BRN (41) Q71`, `YEL-RED (42) Q70`, `YEL-ORN (43) Q69`, `YEL-BLK (40) Q68`, `YEL-GRN (45) Q67`, `YEL-BLU (46) Q66`, `YEL-VIO (47) Q65`, `YEL-GRY (48) Q64`.", "",
        "Printed return headers: `RED-BRN (21) Q72`, `RED-BLK (20) Q73`, `RED-ORN (23) Q74`, `RED-YEL (24) Q75`, `RED-GRN (25) Q76`, `RED-BLU (26) Q77`, `RED-VIO (27) Q78`, `RED-GRY (28) Q79`.", "",
        "| Row / return | YEL-BRN | YEL-RED | YEL-ORN | YEL-BLK | YEL-GRN | YEL-BLU | YEL-VIO | YEL-GRY |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row, return_wire in enumerate(LAMP_RETURNS):
        cells = [f"{column * 8 + row + 1} {LAMP_MATRIX_LABELS[column * 8 + row]}" for column in range(8)]
        rows.append("| " + return_wire + " | " + " | ".join(cells) + " |")
    rows.extend(["", "## Printed lamp-description list", ""])
    for number,label in enumerate(LAMP_LIST_LABELS,start=1):
        rows.append(f"- {number}: {label}")
    rows.extend([
        "", "## Printed location drawing", "",
        "The drawing places 26 `Lock Ball #1`, 32 `Lock Ball #2`, and the seven MANSION letters 57-63 in the separate backbox/back-panel box. It visibly locates playfield lamps 1-25, 27-31, 33-40, 42-48, and 50-52. Lamps 41, 49, 53-56, and 64 do not appear in either the backbox box or the playfield plan, so the manual does not establish their physical plane.", "",
    ])
    return "\n".join(rows)


def excerpt_coils() -> str:
    return """# Playboy 35th Anniversary coil, relay, flipper, and special-solenoid transcription

Source: PDF pages 29-30, printed pages 26-27. Both pages were decided from 400 dpi renders; the PDF text layer and OCR were locator/second-reading aids only.

## CPU-controlled coil/flash schematic

| Public / printed side | Printed device | Printed type or quantity |
| --- | --- | --- |
| 1 / SIDE L 01 | GROTTO 1 | NO.906 (1) |
| 25 / SIDE R 01 | OUTHOLE | 23-840 |
| 2 / SIDE L 02 | GROTTO 2 | NO.906 (2) |
| 26 / SIDE R 02 | TROUGH | 23-840 |
| 3 / SIDE L 03 | SPINNER 1 | NO.89 (3), NO.906 (1) |
| 27 / SIDE R 03 | VERTICAL UP KICKER | 23-800 |
| 4 / SIDE L 04 | SPINNER 2 | NO.89 (3), NO.906 (1) |
| 28 / SIDE R 04 | CHAMPAGNE KICKER | 22-600 |
| 5 / SIDE L 05 | SPINNER 3 | NO.89 (3), NO.906 (1) |
| 29 / SIDE R 05 | DROP TARGET RESET | `23-1200` as printed on the schematic |
| 6 / SIDE L 06 | MULTI BALL | NO.906 (2) |
| 30 / SIDE R 06 | GROTTO KICKING | 24-900 |
| 7 / SIDE L 07 | RAMP LEFT | NO.906 (1) |
| 31 / SIDE R 07 | no fitted branch printed | — |
| 8 / SIDE L 08 | no feature label printed | NO.89 (2), NO.906 (2) |
| 32 / SIDE R 08 | KNOCKER | 23-800 |
| 9 | PLAYBOY/FLASH | NO.89 (2), NO.906 (2) |
| 10 | LEFT/RIGHT COIL RELAY | K1 |
| 11 | GENERAL ILLUM. RELAY | K1 |
| 12 | INSERT 2 DROP FLASH | NO.89 (4) |
| 13 | RAMP RIGHT | NO.89 (1), NO.906 (4) |
| 14 | MANSION FLASH | NO.89 (3), NO.906 (1) |
| 15 | no feature label printed | NO.89 (2), NO.906 (2) |
| 16 | LASER KICKER | 23-800 |

## Printed coil/flash location drawing

Printed page 26 contains a playfield plan plus a separate `Backbox Flash lamps` inset. A 600-dpi render resolves `1L`, two `2L` callouts, `3L`, `4L`, `5L`, `6L`, `7L`, `8L`, `9`, `13`, `14`, `15`, `16`, `1R`-`4R`, two `5R` callouts, `6R`, and `SP1`-`SP5`; no `7R` or `8R` callout is visible. These are group/location callouts, not a promise that each circle represents one bulb.

The inset uses circled output numbers to identify backbox flash bulbs. The retained scan clearly supports these counts; uncertain small glyphs are not assigned:

| Public output | Clearly legible backbox symbols | Schematic total bulbs |
| --- | ---: | ---: |
| 3 | 3 | 4 |
| 4 | 3 | 4 |
| 8 | 2 | 4 |
| 9 | 2 | 4 |
| 12 | 4 | 4 |
| 14 | at least 3 | 4 |
| 15 | at least 1 | 4 |

Three further glyphs resemble `5`/`6`, and two resemble `13`/`16`, but the retained raster is not clear enough to assign them. Output 12's four clear backbox symbols equal its four-bulb schematic total. The plan is sufficient for physical-plane classification and broad feature location, but its grouped callouts and lack of a registered coordinate frame are insufficient for normalized socket centers.

The adjacent coil part-number chart separately prints:

| Quantity | Coil type | Assembly part number |
| --- | --- | --- |
| 8 | 23-800 | 090-5001-00 |
| 1 | 24-900 | 090-5002-00 |
| 2 | 23-840 | 090-5005-00 |
| 1 | 12-1200 | 090-5008-00 |
| 1 | 22-600 | 090-5017-00 |
| 2 | 22-800 | 090-5020-21 |

It prints one `12-1200` coil and no `23-1200` coil. That self-disagreement is preserved rather than corrected.

## Switch-triggered solenoids

| Printed special address | Printed description | Control / trigger | Transistor / coil |
| --- | --- | --- | --- |
| SP1 | Center Pop Bumper | BLU-ORN / ORN-BLK | Q8 / 23-800 |
| SP2 | Right Pop Bumper | BLU-RED / ORN-RED | Q9 / 23-800 |
| SP3 | Left Slingshot | BLU-YEL / ORN-YEL | Q10 / 23-800 |
| SP4 | Left Pop Bumper | BLU-BRN / ORN-BRN | Q11 / 23-800 |
| SP5 | Right Slingshot | BLU-GRN / ORN-GRN | Q12 / 23-800 |
| SP6 | NOT USED | — | Q13 / — |

## Flippers

The printed flipper table lists one left and one right dual-winding assembly, each with coil type `22-800`, and prints separate CPU, PPB, and power-line wires for the two sides.
"""


def excerpt_mechanisms() -> str:
    return """# Playboy 35th Anniversary mechanism-construction transcription

Source: PDF pages 68 and 71-72, printed pages 49 and 52-53. Render-decided at 300 dpi; OCR/text extraction was not used to infer topology.

The playfield-bottom parts page prints these construction records:

- Ball Feed Cam Assy. — `500-5012-00`
- Ball Trough Sw. Plate Assy. — `500-5041-00`
- 3 Bank Drop Tar. Assy. — `500-5055-31`
- Vertical Up Kicker — `500-5067-00`
- Laser Kick Sw. & Bracket — `500-5142-00`
- Shooter lane Sw. & Bracket — `500-5143-00`
- 7 Bank Standup Tgt. Assy. — `515-5145-00`
- 3 Bank Standup Tgt. Assy. — `500-5103-08`
- Pop Bumper Assembly (3) — `500-5034-00`
- Grotto Kicking Assy. — `500-5053-00`
- Champagne Kicker Assy. — `500-5053-03`
- Slingshot Assembly (2) — `500-5077-00`
- Left Flipper Assembly — `500-5031-52`
- Right Flipper Assembly — `500-5031-51`

The seven-bank drawing shows seven independent leaf-switch/target stations on one bracket (`515-5145-11` family), with no drop faces or reset coil. It is therefore a fixed standup bank. The separate three-bank drop-target listing plus the script's `cvpmDropTarget` construction establishes a real three-position dropping/resetting bank.

The manual's switch list prints shooter-lane part `500-5142-00` and left-outlane part `500-5143-00`. The playfield-bottom list instead prints Laser Kick switch/bracket `500-5142-00` and Shooter lane switch/bracket `500-5143-00`. Both transcriptions are retained as a conflict.
"""


EXCERPTS = {
    Path("evidence/excerpts/data-east.playboy-35th-anniversary.1989/switch-matrix.md"): excerpt_switch_matrix(),
    Path("evidence/excerpts/data-east.playboy-35th-anniversary.1989/lamp-matrix.md"): excerpt_lamp_matrix(),
    Path("evidence/excerpts/data-east.playboy-35th-anniversary.1989/coil-and-flipper.md"): excerpt_coils(),
    Path("evidence/excerpts/data-east.playboy-35th-anniversary.1989/mechanism-construction.md"): excerpt_mechanisms(),
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return digest.hexdigest()


def provenance(status: str, *source_refs: str) -> dict[str, object]:
    return {"status":status,"source_refs":list(dict.fromkeys(source_refs))}


def aliases(namespace: str, number: int | str, manual: str | None = None) -> list[dict[str,str]]:
    result = [{"namespace":namespace,"value":str(number)}]
    if manual is not None:
        result.append({"namespace":"manual.address","value":manual})
    return result


def not_applicable(reason: str, status: str, *source_refs: str) -> dict[str,object]:
    return {"status":"not_applicable","reason":reason,"provenance":provenance(status,*source_refs)}


def norm(point: tuple[float,float]) -> tuple[float,float]:
    x,y = point
    if not (0.0 <= x <= RIGHT and 0.0 <= y <= BOTTOM):
        raise ValueError(f"out-of-bounds retained point: {point}")
    return round(x / RIGHT,6), round(y / BOTTOM,6)


def located(device_id: str, points: list[tuple[float,float]], role: str, status: str, *source_refs: str) -> dict[str,object]:
    placements = []
    for index,raw in enumerate(points,start=1):
        x,y = norm(raw)
        placements.append({"id":f"{device_id}.placement-{index}","role":role,"space":"playfield","x":x,"y":y,"provenance":provenance(status,*source_refs)})
    return {"status":status,"placements":placements}


def switch_input(number: int) -> dict[str,object]:
    label = SWITCH_LABELS[number]
    unused = label == "Not Used"
    device_id = f"switch.matrix-{number}"
    column,row = divmod(number-1,8)
    conflict_numbers = {2,14,15,16}
    physical: dict[str,object] = {"notes":f"Manual matrix column {column+1}, row {row+1}; printed cell '{label}'."}
    if number in SWITCH_PARTS:
        physical["part_number"] = SWITCH_PARTS[number]
    if number in {15,16}:
        physical["notes"] += " The adjacent list also prints an Instant Info flipper function and a physical EOS contact; FLIP1516 publishes the cabinet-button state at this public address."
    if number in {14,17}:
        physical["notes"] += " The switch-list part number conflicts with the playfield-bottom construction list's shooter-lane/Laser-Kick assignment."
    if number == 17:
        physical["notes"] += " The active script's impulse helper names an off-playfield sw17 trigger, but Kicker001_Hit explicitly publishes switch 17 from an in-bounds kickback object; that executable binding supplies the retained candidate coordinate. The visible sw17a name is unbound and excluded."
    result: dict[str,object] = {
        "id":device_id,"label":f"Unused Switch {number}" if unused else label,"kind":"switch",
        "binding":{"group":"pinmame.input.switch","device":number},"aliases":aliases("pinmame.switch",number,str(number)),
        "availability":"unused" if unused else "used","physical":physical,
        "wiring":{"board":"CPU Board","drive_wire":SWITCH_DRIVES[column],"return_wire":SWITCH_RETURNS[row]},
        "provenance":provenance("conflicted" if number in conflict_numbers else "validated",MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE),
    }
    roles = {
        1:"cabinet.tilt",3:"cabinet.start",4:"cabinet.coin",5:"cabinet.coin",6:"cabinet.coin",7:"cabinet.slam-tilt",
        10:"ball.position",11:"ball.position",12:"ball.position",13:"ball.position",14:"ball.position",
        15:"flipper.lower.left.button",16:"flipper.lower.right.button",17:"ball.position",23:"ball.position",24:"ball.position",31:"ball.position",45:"ball.position",
        49:"target.drop",50:"target.drop",51:"target.drop",
    }
    if number in roles:
        result["roles"] = [roles[number]]
    if unused:
        result["spatial"] = not_applicable("unused","validated",MANUAL_SOURCE)
    elif number in {1,3,4,5,6,7,15,16}:
        result["spatial"] = not_applicable("cabinet_or_service","conflicted" if number in {15,16} else "validated",MANUAL_SOURCE,CORE_SOURCE)
    elif number in RAW_SWITCH_POINTS:
        spatial_status = "candidate" if number == 17 else "observed"
        result["spatial"] = located(device_id,[RAW_SWITCH_POINTS[number]],"sensor",spatial_status,TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    return result


def diagnostic_inputs() -> list[dict[str,object]]:
    result = []
    for device,suffix,label,role in [(-7,"7","Black Button / Advance","service.advance"),(-6,"6","Green Button / Up-Down","service.adjust")]:
        result.append({
            "id":f"switch.diagnostic-{suffix}","label":label,"kind":"switch","binding":{"group":"pinmame.input.switch","device":device},
            "aliases":[{"namespace":"pinmame.switch","value":str(device)}],"availability":"used","roles":[role],
            "physical":{"notes":"Shared Data East service-door input declared by DE_COMPORTS."},
            "spatial":not_applicable("cabinet_or_service","validated",CORE_SOURCE),"provenance":provenance("validated",CORE_SOURCE),
        })
    result.append({
        "id":"dip.jumper-w7","label":"Jumper W7 (function undocumented)","kind":"dip_switch","binding":{"group":"pinmame.input.dip","device":0},
        "aliases":[{"namespace":"pinmame.dip","value":"0"}],"availability":"used",
        "physical":{"notes":"Pinned Data East input ports expose one W7 jumper; the retained manual does not document a Playboy-specific function."},
        "spatial":not_applicable("dip_switch","candidate",CORE_SOURCE,MANUAL_SOURCE),"provenance":provenance("candidate",CORE_SOURCE,MANUAL_SOURCE),
    })
    return result


def lamp_output(number: int) -> dict[str,object]:
    device_id = f"lamp.matrix-{number}"
    column,row = divmod(number-1,8)
    label = LAMP_LIST_LABELS[number-1]
    points = RAW_LAMP_POINTS.get(number,[])
    physical: dict[str,object] = {
        "quantity":max(1,len(points)),
        "notes":f"Manual matrix prints '{LAMP_MATRIX_LABELS[number-1]}'; adjacent list prints '{label}'. The active UpdateLamps routine explicitly routes address {number} to a same-number visual object, but that name/center is candidate evidence rather than a surveyed socket binding.",
    }
    result: dict[str,object] = {
        "id":device_id,"label":label,"kind":"lamp","binding":{"group":"pinmame.output.lamp","device":number},
        "aliases":aliases("pinmame.lamp",number,str(number)),"availability":"used","physical":physical,
        "wiring":{"board":"CPU Board","drive_wire":LAMP_DRIVES[column],"return_wire":LAMP_RETURNS[row]},
        "provenance":provenance("candidate",MANUAL_SOURCE,SCRIPT_SOURCE,TABLE_SOURCE),
    }
    if number in BACKBOX_LAMPS:
        physical["location"] = "backbox/back panel"
        physical["notes"] += " This is one of the nine addresses with no numeric Light object: it is bound under the same name as a vertical Flasher proxy at the rear edge because the manual places it in the backbox/back-panel box."
        result["spatial"] = not_applicable("cabinet_or_service","validated",MANUAL_SOURCE,SCRIPT_SOURCE,TABLE_SOURCE)
    elif number in MANUAL_UNLOCATED_PINBALL_LAMPS:
        physical["location"] = "not located by manual; table presentation proxy flagged as backglass"
        physical["notes"] += " The manual location drawing does not show this PINBALL letter in either its backbox box or playfield plan. The retained numeric Light object is flagged is_backglass=true, but presentation geometry alone does not establish the physical socket plane, so its coordinates are withheld."
    else:
        result["spatial"] = located(device_id,points,"emitter","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    return result


SPECIAL_DE_PERMUTATION = (3,4,5,1,0,2)
SPECIAL_PIA_HANDLER_TO_PRINTED = {0:6,1:5,2:2,3:3,4:1,5:4}
SPECIAL_PUBLIC_TO_PRINTED = {17 + SPECIAL_DE_PERMUTATION[handler]:printed for handler,printed in SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
SPECIAL_PRINTED_LABELS = {1:"Center Pop Bumper",2:"Right Pop Bumper",3:"Left Slingshot",4:"Left Pop Bumper",5:"Right Slingshot",6:"Unused SP6 Driver"}

SOLENOID_LABELS = {
    1:"Grotto 1 Flash",2:"Grotto 2 Flash",3:"Spinner 1 Flash",4:"Spinner 2 Flash",5:"Spinner 3 Flash",6:"Multi Ball Flash",7:"Ramp Left Flash",8:"Unlabeled Flash Group 8",
    9:"Playboy Flash",10:"Left/Right Coil Relay K1",11:"General Illumination Relay K1",12:"Insert 2 / Drop Flash",13:"Ramp Right Flash",14:"Mansion Flash",15:"Unlabeled Flash Group 15",16:"Laser Kicker",
    **{public:SPECIAL_PRINTED_LABELS[printed] for public,printed in SPECIAL_PUBLIC_TO_PRINTED.items()},
    24:"Unused Solenoid 24",25:"Outhole",26:"Trough Eject",27:"Vertical Up Kicker",28:"Champagne Kicker",29:"Drop Target Reset",30:"Grotto Kicking",31:"Unfitted Mux Branch R07",32:"Knocker",
    45:"Synthetic Right Flipper Power",46:"Synthetic Right Flipper Hold",47:"Synthetic Left Flipper Power",48:"Synthetic Left Flipper Hold",49:"Simulation Ball Shooter",50:"Reserved Solenoid 50",
}
for _number in range(33,45):
    SOLENOID_LABELS[_number] = f"Inert Solenoid Address {_number}"

SOLENOID_PARTS = {
    16:"23-800",17:"23-800",18:"23-800",19:"23-800",21:"23-800",22:"23-800",25:"23-840",26:"23-840",27:"23-800",28:"22-600",29:"23-1200 / 12-1200",30:"24-900",32:"23-800",
}
SPECIAL_PRINTED_TRANSISTORS = {1:"Q8",2:"Q9",3:"Q10",4:"Q11",5:"Q12",6:"Q13"}
SOLENOID_TRANSISTORS = {
    1:"Q46",2:"Q45",3:"Q44",4:"Q43",5:"Q42",6:"Q41",7:"Q40",8:"Q39",9:"Q30",10:"Q29",11:"Q28",12:"Q27",13:"Q26",14:"Q25",15:"Q24",16:"Q23",
    **{public:SPECIAL_PRINTED_TRANSISTORS[printed] for public,printed in SPECIAL_PUBLIC_TO_PRINTED.items()},
}
SOLENOID_DRIVES = {1:"GRY-BRN",2:"GRY-RED",3:"GRY-ORN",4:"GRY-YEL",5:"GRY-GRN",6:"GRY-BLU",7:"GRY-VIO",8:"GRY-BLK",9:"BRN-BLK",10:"BLK-RED",11:"BRN-ORN",12:"BRN-YEL",13:"BRN-GRN",14:"BRN-BLU",15:"BRN-VIO",16:"WHT-GRY"}
BACKBOX_FLASH_BULBS = {3:3,4:3,8:2,9:2,12:4,14:3,15:1}
MINIMUM_BACKBOX_FLASH_BULBS = {14,15}
FLASH_EFFECT_COUNTS = {number:len(points) for number,points in RAW_FLASH_POINTS.items()}


def solenoid_output(number: int) -> dict[str,object]:
    device_id = "coil.game-on" if number == 23 else f"coil.driver-{number}"
    if number == 23:
        return {
            "id":device_id,"label":"Game On / Flipper and Special-Solenoid Enable","kind":"control_signal",
            "binding":{"group":"pinmame.output.solenoid","device":23},"aliases":aliases("pinmame.solenoid",23),"availability":"used",
            "physical":{"notes":"System 11 public Game On state enables flipper and special-solenoid circuits. The table also uses it to drive an off-playfield FL23 backglass-on proxy; that consumer effect is not a third physical coil."},
            "spatial":not_applicable("internal_nonvisual","validated",CORE_SOURCE),"provenance":provenance("validated",CORE_SOURCE,SCRIPT_SOURCE),
        }
    label = SOLENOID_LABELS[number]
    unused = number in {20,24,33,34,35,36,37,38,39,40,41,42,43,44,49,50}
    if number in {1,2,3,4,5,6,7,8,9,12,13,14,15}:
        kind = "flasher"
    elif number == 10:
        kind = "relay"
    elif number == 11:
        kind = "gi"
    elif number in {24,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50}:
        kind = "virtual"
    else:
        kind = "coil"
    conflict_numbers = {3,4,8,9,12,13,14,15,19,25,26,27,28,29,30,31,32}
    status = "conflicted" if number in conflict_numbers else ("candidate" if number in {8,17,18,21,22,45,46,47,48} else "validated")
    if 1 <= number <= 8:
        manual_number = f"SIDE L {number:02d}"
    elif 9 <= number <= 16:
        manual_number = str(number)
    elif 17 <= number <= 22:
        manual_number = f"SP{SPECIAL_PUBLIC_TO_PRINTED[number]}"
    elif 25 <= number <= 32:
        manual_number = f"SIDE R {number-24:02d}"
    else:
        manual_number = None
    physical: dict[str,object] = {"notes":f"Public solenoid {number}."}
    if manual_number is not None:
        physical["notes"] += f" Manual printed address {manual_number}."
    if not unused and number not in {31,45,46,47,48}:
        physical["quantity"] = 1
    if number in SOLENOID_PARTS:
        physical["part_number"] = SOLENOID_PARTS[number]
    quantities = {1:1,2:2,3:4,4:4,5:4,6:2,7:1,8:4,9:4,12:4,13:5,14:4,15:4}
    if number in quantities:
        physical["quantity"] = quantities[number]
        physical["notes"] += " Quantity and bulb mix follow the rendered manual schematic; VPX visual objects may proxy several sockets."
    if number in BACKBOX_FLASH_BULBS:
        backbox = BACKBOX_FLASH_BULBS[number]
        qualifier = "at least " if number in MINIMUM_BACKBOX_FLASH_BULBS else ""
        physical["location"] = "backbox/back panel" if number == 12 else "includes backbox flash bulbs; complete socket-plane split unresolved"
        physical["notes"] += f" The printed backbox inset contains {qualifier}{backbox} clearly legible bulb symbol{'s' if backbox != 1 else ''} for this output. The retained table has {FLASH_EFFECT_COUNTS[number]} playfield effect object{'s' if FLASH_EFFECT_COUNTS[number] != 1 else ''}; those are presentation consumers rather than a complete physical socket survey."
        if number == 9:
            physical["notes"] += " The two physical backbox symbols and four retained table effect objects are not additive: the effect objects are presentation proxies, not four surveyed playfield sockets."
        if number == 12:
            physical["notes"] += " These four symbols equal the complete four-bulb schematic quantity, and the playfield plan has no output-12 callout, so the physical group is classified as backbox-only."
    if number in {4,5}:
        physical["notes"] += " Active callbacks for both outputs write pseudo-lamp 105, leaving the separately updated Fl4 object without an output callback."
    if number in {13,14,15}:
        physical["notes"] += " Manual labels and active-line inline script comments do not align across this three-address block; the printed manual label is retained."
    if 17 <= number <= 22:
        physical["notes"] += f" Pinned s11.c PIA comments identify handlers 0-5 as printed SP6, SP5, SP2, SP3, SP1, SP4; setSSSol applies the Data East offset permutation {SPECIAL_DE_PERMUTATION}, deriving printed {manual_number} at public {number}."
    if number == 19:
        physical["notes"] += " The manual makes this hardware-triggered left-pop-bumper coil; the active table also maps its public state to off-playfield FL19 as a background flasher proxy."
    if 25 <= number <= 32:
        physical["notes"] += " S11_MUXDELAY holds the PIA port-B byte for one IRQ before publication so the K1-selected A/C bank is attributed with the ROM's relay timing. Pinned s11.c uniformly marks public 25-32 with a #89-bulb PWM type, while the manual fits coils here except unfitted 31. Manual construction controls device semantics; core controls public timing/numbering. Consumers of decoded public outputs must not add another delay."
    if number == 31:
        physical["notes"] += " Availability is unknown because the manual fits no physical R07 device but the decoded public address mirrors the A-side bit while K1 is asserted; only a ROM or runtime trace can establish whether that public state ever activates."
    if number == 29:
        physical["notes"] += " The schematic appears to print 23-1200 while the coil part-number chart prints one 12-1200 and no 23-1200; both are retained."
    if 33 <= number <= 44:
        physical["notes"] += " Pinned System 11 exposes this public address but this Data East driver does not populate it."
    if 45 <= number <= 48:
        physical["notes"] += " Synthetic PinMAME lower-flipper power/hold state; there is no separate physical driver at this public address."
    if number == 49:
        physical["notes"] += " System 11 simulation-only shooter address; the physical machine uses a manual plunger."
    if number == 50:
        physical["notes"] += " Reserved public address with no meaningful machine state."
    source_refs = [CORE_SOURCE,SCRIPT_SOURCE]
    if manual_number is not None:
        source_refs.insert(0,MANUAL_SOURCE)
    result: dict[str,object] = {
        "id":device_id,"label":label,"kind":kind,"binding":{"group":"pinmame.output.solenoid","device":number},
        "aliases":aliases("pinmame.solenoid",number,manual_number),"availability":"unknown" if number == 31 else ("unused" if unused else "used"),
        "physical":physical,"provenance":provenance(status,*source_refs),
    }
    if number in SOLENOID_TRANSISTORS:
        result["wiring"] = {"board":"CPU Board / PPB","driver_transistor":SOLENOID_TRANSISTORS[number]}
        if number in SOLENOID_DRIVES:
            result["wiring"]["drive_wire"] = SOLENOID_DRIVES[number]
    if unused:
        result["spatial"] = not_applicable("virtual" if number == 24 or number in range(33,51) else "unused","validated",*(source_refs[:-1] if SCRIPT_SOURCE in source_refs else source_refs))
    elif number == 12:
        result["spatial"] = not_applicable("cabinet_or_service","conflicted",MANUAL_SOURCE,TABLE_SOURCE,SCRIPT_SOURCE)
    elif number in RAW_FLASH_POINTS:
        result["spatial"] = located(device_id,RAW_FLASH_POINTS[number],"effect","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number == 10:
        result["spatial"] = not_applicable("internal_nonvisual","validated",CORE_SOURCE,MANUAL_SOURCE)
    elif number == 11:
        physical.pop("quantity",None)
        physical["notes"] += " The 47 retained aGiLights entries are visual consumers, not a surveyed physical socket count."
        result["spatial"] = located(device_id,RAW_GI_POINTS,"effect","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number == 16:
        result["spatial"] = located(device_id,[(53.316788,1590.0859)],"effect","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number in {17,18,21,22}:
        point = {17:RAW_SWITCH_POINTS[47],18:RAW_SWITCH_POINTS[21],21:RAW_SWITCH_POINTS[22],22:RAW_SWITCH_POINTS[48]}[number]
        result["spatial"] = located(device_id,[point],"effect","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number == 19:
        result["spatial"] = located(device_id,[RAW_SWITCH_POINTS[46]],"effect","conflicted",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number in {25,26,27,28,29,30}:
        point = {25:RAW_SWITCH_POINTS[10],26:RAW_SWITCH_POINTS[13],27:RAW_SWITCH_POINTS[45],28:RAW_SWITCH_POINTS[23],29:RAW_SWITCH_POINTS[50],30:RAW_SWITCH_POINTS[31]}[number]
        result["spatial"] = located(device_id,[point],"effect","candidate",TABLE_SOURCE,SCRIPT_SOURCE,MANUAL_SOURCE)
    elif number == 31:
        result["spatial"] = not_applicable("virtual","conflicted",MANUAL_SOURCE,CORE_SOURCE)
    elif number == 32:
        result["spatial"] = not_applicable("cabinet_or_service","conflicted",MANUAL_SOURCE,CORE_SOURCE)
    elif number in {45,46,47,48}:
        result["spatial"] = not_applicable("virtual","candidate",CORE_SOURCE,SCRIPT_SOURCE)
    return result


def displays() -> list[dict[str,object]]:
    labels = ["Player 1 alphanumeric display","Player 2 alphanumeric display","Player 3 numeric display","Player 4 numeric display"]
    starts = [1,9,21,29]
    return [{
        "id":f"display.segment-{index}","label":label,"kind":"segment","controller_index":index,"segment_start":starts[index],"width":7,
        "spatial":not_applicable("cabinet_or_service","validated",CORE_SOURCE,MANUAL_SOURCE),"provenance":provenance("validated",CORE_SOURCE,MANUAL_SOURCE),
    } for index,label in enumerate(labels)]


def mechanisms() -> list[dict[str,object]]:
    return [
        {"id":"mechanism.outhole","label":"Outhole feeder","kind":"kicker","actuators":["coil.driver-25"],"sensors":["switch.matrix-10"],"behavior":"Drain_Hit adds the drained ball at switch 10 to a three-ball stack. Public output 25 drives the constructed outhole coil and feeds that stack.","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.ball-trough","label":"Three-ball trough and eject","kind":"other","actuators":["coil.driver-26"],"sensors":["switch.matrix-11","switch.matrix-12","switch.matrix-13"],"behavior":"The active cvpmBallStack declares switch order 13, 12, 11 and starts with three balls. Output 26 kicks the front BallRelease position toward the shooter lane; the manual constructs a feed cam and switch plate.","assembly_part_number":"500-5012-00","positions":[{"id":"trough.position-1","label":"Front eject position","sensors":["switch.matrix-13"]},{"id":"trough.position-2","label":"Middle position","sensors":["switch.matrix-12"]},{"id":"trough.position-3","label":"Rear position","sensors":["switch.matrix-11"]}],"provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.vertical-up-kicker","label":"Vertical Up Kicker","kind":"kicker","actuators":["coil.driver-27"],"sensors":["switch.matrix-45"],"behavior":"The active bsVUK saucer holds a ball at switch 45 and output 27 ejects it vertically. The manual independently lists constructed Vertical Up Kicker 500-5067-00.","assembly_part_number":"500-5067-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.champagne-kicker","label":"Champagne Kicker","kind":"kicker","actuators":["coil.driver-28"],"sensors":["switch.matrix-23"],"behavior":"Kicker2_Hit adds the ball to bsCK at switch 23; output 28 fires its saucer exit. The manual lists Champagne Kicker Assembly 500-5053-03.","assembly_part_number":"500-5053-03","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.grotto-kicker","label":"Two-sensor Grotto path and kickout","kind":"kicker","actuators":["coil.driver-30"],"sensors":["switch.matrix-24","switch.matrix-31"],"behavior":"The in-bound trigger reports printed Grotto 1 at switch 24. The active bsGrotto saucer then holds/ejects at printed Grotto 2 switch 31 through output 30. Manual construction supplies one Grotto Kicking Assembly plus two kicking switches; exact under-playfield transfer geometry is not exposed.","assembly_part_number":"500-5053-00","positions":[{"id":"grotto.entry","label":"Grotto 1 entry","sensors":["switch.matrix-24"]},{"id":"grotto.cup","label":"Grotto 2 kickout cup","sensors":["switch.matrix-31"]}],"provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.drop-bank","label":"Three-bank drop targets","kind":"drop_target_bank","actuators":["coil.driver-29"],"sensors":["switch.matrix-49","switch.matrix-50","switch.matrix-51"],"behavior":"The active cvpmDropTarget orders top, center, and bottom dropping faces at 49-51 and raises all three from output 29. Manual construction names 3 Bank Drop Target Assembly 500-5055-31.","assembly_part_number":"500-5055-31","positions":[{"id":"drop.position-top","label":"Top target","sensors":["switch.matrix-49"]},{"id":"drop.position-center","label":"Center target","sensors":["switch.matrix-50"]},{"id":"drop.position-bottom","label":"Bottom target","sensors":["switch.matrix-51"]}],"provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.laser-kick","label":"Left-outlane Laser Kick","kind":"kicker","actuators":["coil.driver-16"],"sensors":["switch.matrix-17"],"behavior":"The active impulse-plunger helper watches public switch 17 and output 16 auto-fires the left-outlane kickback. Although the helper's sw17 trigger is outside the asserted playfield, Kicker001_Hit explicitly publishes switch 17 from the in-bounds kickback object; that executable point is retained as candidate placement and the unbound sw17a name is excluded.","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.left-flipper","label":"Lower-left flipper","kind":"other","actuators":["coil.driver-47","coil.driver-48"],"sensors":["switch.matrix-15"],"behavior":"One printed 22-800 dual-winding coil moves the sole left flipper. The manual prints physical Left EOS at 15, while FLIP1516 and the key handler publish cabinet-button state there.","assembly_part_number":"500-5031-52","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.right-flipper","label":"Lower-right flipper","kind":"other","actuators":["coil.driver-45","coil.driver-46"],"sensors":["switch.matrix-16"],"behavior":"One printed 22-800 dual-winding coil moves the sole right flipper. The manual prints physical Right EOS at 16, while FLIP1516 and the key handler publish cabinet-button state there.","assembly_part_number":"500-5031-51","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.left-slingshot","label":"Left slingshot","kind":"other","actuators":["coil.driver-18"],"sensors":["switch.matrix-21"],"behavior":"The native left-slingshot event pulses switch 21. The manual maps hardware-triggered SP3 to the left slingshot, and pinned Data East setSSSol publishes SP3 as public 18; public callback pulse timing is not exposed.","assembly_part_number":"500-5077-00","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.right-slingshot","label":"Right slingshot","kind":"other","actuators":["coil.driver-21"],"sensors":["switch.matrix-22"],"behavior":"The native right-slingshot event pulses switch 22. The manual maps hardware-triggered SP5 to the right slingshot, and pinned Data East setSSSol publishes SP5 as public 21; public callback pulse timing is not exposed.","assembly_part_number":"500-5077-00","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.left-pop","label":"Left pop bumper","kind":"other","actuators":["coil.driver-19"],"sensors":["switch.matrix-46"],"behavior":"Bumper1_Hit pulses switch 46; the rendered manual maps SP4 to the left pop, and pinned Data East setSSSol publishes SP4 as public 19. The physical assembly is one of three 500-5034-00 pop bumpers.","assembly_part_number":"500-5034-00","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.center-pop","label":"Center pop bumper","kind":"other","actuators":["coil.driver-17"],"sensors":["switch.matrix-47"],"behavior":"The working VPX script's Bumper2_Hit pulses switch 47 and uses the middle-bumper sound path. Its retained position matches the manual's SP1 center-pop location bubble. The pinned PIA comments plus setSSSol permutation derive SP1 as public 17.","assembly_part_number":"500-5034-00","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE,TABLE_SOURCE)},
        {"id":"mechanism.right-pop","label":"Right pop bumper","kind":"other","actuators":["coil.driver-22"],"sensors":["switch.matrix-48"],"behavior":"The working VPX script's Bumper3_Hit pulses switch 48. Its retained position matches the manual's SP2 right-pop location bubble. The pinned PIA comments plus setSSSol permutation derive SP2 as public 22.","assembly_part_number":"500-5034-00","provenance":provenance("candidate",SCRIPT_SOURCE,MANUAL_SOURCE,CORE_SOURCE,TABLE_SOURCE)},
        {"id":"mechanism.playboy-standups","label":"Seven-bank PLAYBOY fixed standups","kind":"other","actuators":[],"sensors":[f"switch.matrix-{number}" for number in range(33,40)],"behavior":"Seven independent active HitTarget events pulse P, L, A, first Y, B, O, and second Y. The manual's seven-bank construction drawing shows seven leaf-switch target stations and no dropping faces or reset coil.","assembly_part_number":"515-5145-00","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.center-standups","label":"Center three-bank fixed standups","kind":"other","actuators":[],"sensors":["switch.matrix-41","switch.matrix-42","switch.matrix-43"],"behavior":"Three independent active HitTarget events pulse left, middle, and right. Manual construction names 3 Bank Standup Target Assembly 500-5103-08; no reset coil or dropping faces are fitted.","assembly_part_number":"500-5103-08","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.manual-shooter","label":"Manual plunger and shooter lane","kind":"other","actuators":[],"sensors":["switch.matrix-14"],"behavior":"The retained Plunger object provides player-driven launch and the active sw14 trigger reports the shooter lane. No CPU shooter coil is claimed; the two manual parts lists disagree over the 500-5142/500-5143 switch-bracket assignment.","provenance":provenance("conflicted",SCRIPT_SOURCE,MANUAL_SOURCE)},
        {"id":"mechanism.fixed-routes","label":"Fixed lanes, spinner, and ramps","kind":"other","actuators":[],"sensors":["switch.matrix-18","switch.matrix-19","switch.matrix-20","switch.matrix-25","switch.matrix-26","switch.matrix-27","switch.matrix-28","switch.matrix-29","switch.matrix-30","switch.matrix-32"],"behavior":"Executable triggers establish the two returns, right outlane, three top lanes, center/right/left ramps, and the left spinner. The manual construction and switch maps show passive paths; no motor or diverter actuator is inferred from feature labels.","provenance":provenance("validated",SCRIPT_SOURCE,MANUAL_SOURCE)},
    ]


def conflicts() -> list[dict[str,object]]:
    return [
        {"id":"conflict.shared-port-position-2-vs-unfitted","path":"/inputs/switch.matrix-2","description":"Shared Data East DE_COMPORTS names matrix position 2 Ball Tilt, while both Playboy manual switch tables print position 2 Not Used. Game-specific fitment is retained without erasing the shared-port label.","source_refs":[MANUAL_SOURCE,CORE_SOURCE]},
        {"id":"conflict.left-eos-vs-public-button-state","path":"/inputs/switch.matrix-15","description":"The manual prints a physical Left EOS contact at matrix 15 and does not mark it as a cabinet switch. FLIP1516 and the retained key handler put left cabinet-button state at public 15.","source_refs":[MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE]},
        {"id":"conflict.right-eos-vs-public-button-state","path":"/inputs/switch.matrix-16","description":"The manual prints a physical Right EOS contact at matrix 16 and does not mark it as a cabinet switch. FLIP1516 and the retained key handler put right cabinet-button state at public 16.","source_refs":[MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE]},
        {"id":"conflict.shooter-laser-switch-part-numbers","path":"/inputs/switch.matrix-14","description":"The manual switch list prints Shooter Lane part 500-5142-00 and Left Outlane part 500-5143-00. Its playfield-bottom list prints Laser Kick switch/bracket 500-5142-00 and Shooter lane switch/bracket 500-5143-00.","source_refs":[MANUAL_SOURCE,RENDER_SOURCE]},
        {"id":"conflict.outputs-4-and-5-share-pseudo-lamp-105","path":"/outputs/coil.driver-4","description":"The active lines bind both public outputs 4 and 5 to SetLamp 105. UpdateLamps has distinct Fl4 at pseudo 104 and Fl5 at 105, leaving Fl4 without a driving callback even though the manual prints separate Spinner 2 and Spinner 3 flash groups.","source_refs":[SCRIPT_SOURCE,TABLE_SOURCE,MANUAL_SOURCE]},
        {"id":"conflict.outputs-13-through-15-script-comments-vs-manual","path":"/outputs/coil.driver-13","description":"The manual prints 13 Ramp Right, 14 Mansion Flash, and no feature label for 15. Active-line inline comments instead call 13 'flasher13 PB', 14 'Right Ramp', and 15 'mansion flasher'. Generic Fl13/Fl14/Fl15 names do not settle the shift, so manual labels and script annotations remain separate.","source_refs":[MANUAL_SOURCE,SCRIPT_SOURCE,TABLE_SOURCE]},
        {"id":"conflict.muxed-c-bank-core-bulb-type-vs-manual-coils","path":"/outputs/coil.driver-25","description":"Pinned Playboy s11.c uniformly assigns #89-bulb PWM type to public 25-32. The rendered manual fits Outhole, Trough, VUK, Champagne Kicker, Drop Reset, Grotto Kicking and Knocker coils at 25-30/32 and no R07 branch at 31. Core numbering/timing and manual construction are retained without treating the type metadata as fitment authority.","source_refs":[CORE_SOURCE,MANUAL_SOURCE,SCRIPT_SOURCE]},
        {"id":"conflict.drop-reset-coil-type-print","path":"/outputs/coil.driver-29","description":"The rendered output schematic appears to print Drop Target Reset as 23-1200, while the adjacent coil part-number chart prints one 12-1200 coil and no 23-1200. No correction is inferred.","source_refs":[MANUAL_SOURCE,RENDER_SOURCE]},
        {"id":"conflict.special-solenoid-19-vs-background-proxy","path":"/outputs/coil.driver-19","description":"Pinned Data East setSSSol maps the manual's SP4 left-pop-bumper circuit to public 19. The active table additionally maps public 19 to pseudo-lamp 119 and off-playfield FL19 as a background flasher. The proxy is recorded as a consumer side effect, not a physical coil location.","source_refs":[MANUAL_SOURCE,CORE_SOURCE,SCRIPT_SOURCE,TABLE_SOURCE]},
        {"id":"conflict.flash-location-drawing-vs-playfield-proxies","path":"/outputs/coil.driver-3","description":"The manual's separate backbox inset clearly assigns bulbs to outputs 3, 4, 8, 9, 12, 14 and 15, while every retained VPX effect for those outputs is located in playfield space. Output 12 alone has four clear backbox symbols, equal to its complete schematic quantity, yet three playfield effect objects. Small 5/6-like and 13/16-like inset glyphs remain unassigned. Each output note preserves the certain minimum; VPX effects are not promoted into extra physical sockets.","source_refs":[MANUAL_SOURCE,TABLE_SOURCE,SCRIPT_SOURCE]},
    ]


def sources() -> list[dict[str,object]]:
    locators = {
        "switch-matrix.md":"PDF pages 25-26, printed pages 22-23","lamp-matrix.md":"PDF pages 27-28, printed pages 24-25",
        "coil-and-flipper.md":"PDF pages 29-30, printed pages 26-27","mechanism-construction.md":"PDF pages 68 and 71-72, printed pages 49 and 52-53",
    }
    excerpt_meta = [{
        "id":"excerpt.playboy-35th."+path.stem,"path":path.as_posix(),"sha256":sha256_text(content),"method":"manual","reviewed":True,
        "locator":locators[path.name],"transcribed_by":"primary curator; PDF text/OCR located or cross-checked, Poppler render decided",
    } for path,content in EXCERPTS.items()]
    return [
        {"id":CATALOG_SOURCE,"kind":"pinmame_catalog","uri":"https://github.com/vpinball/pinmame","revision":PINMAME_REVISION,"license":"BSD-3-Clause","locator":"catalog/pinmame.json and src/wpc/driver.c line 474 contain only play_a24 for this title; exhaustive CORE_GAMEDEF/CORE_CLONEDEF search found no clone."},
        {"id":CORE_SOURCE,"kind":"pinmame_core","uri":"https://github.com/vpinball/pinmame","revision":PINMAME_REVISION,"license":"BSD-3-Clause","locator":"src/wpc/degames.c lines 77 and 237-245 decode INITGAMES11(play, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, S11_MUXDELAY) into core_tGameData hardware fields and leave wpc.invSw zero-initialized; src/wpc/core.c lines 2455-2456 copy that zero mask into coreGlobals.invSw; src/wpc/s11.h line 229 defines one-IRQ mux delay; src/wpc/s11.c lines 537-554 apply Data East permutation {3,4,5,1,0,2}, lines 618-623 bind handler indices 0-5, and the PIA board comments at lines 714-715, 737-738, and 746-747 identify those handlers as printed SP6, SP5, SP2, SP3, SP1, and SP4 respectively; pia0b_w/updsol and lines 1145-1149 implement prior-byte timing and output types."},
        {"id":MANUAL_SOURCE,"kind":"manual","uri":f"external:pinmame-manuals/by-machine/{MACHINE_ID}/contributor-supplied/{MANUAL_FILENAME}","sha256":MANUAL_SHA256,"locator":"76 pages; 14,450,592 bytes; hashes.json sampled_characters=76,678. Contact sheet at 40 dpi located decisive pages; PDF pages 25-30 rendered at 400 dpi, printed page 26 re-rendered at 600 dpi, and construction pages rendered at 300 dpi. Every mapping cell was read from renders despite the text layer.","license":"Copyright Data East; redistribution status not supplied","attribution":"Data East Playboy 35th Anniversary English manual","original_filename":MANUAL_FILENAME,"rights":"NOASSERTION","excerpts":excerpt_meta},
        {"id":TABLE_SOURCE,"kind":"vpx_table","uri":f"external:pinmame-vpx-sources/data-east/playboy-35th-anniversary-1989/{TABLE_FILENAME}","sha256":TABLE_SHA256,"revision":"Physics Sound Hybrid MOD 1.1","known_working":True,"source_id":"retained-playboy-35th-hybrid-1.1","original_filename":TABLE_FILENAME,"license":"Community table; redistribution terms not supplied","attribution":"Credited Playboy 35th Anniversary table contributors","locator":"vpxtool git:0561bb4; 1748 files under gameitems/; exact asserted bounds (0,0)-(952,1974)"},
        {"id":SCRIPT_SOURCE,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/data-east/playboy-35th-anniversary-1989/vpxtool-extract/script.vbs","sha256":SCRIPT_SHA256,"revision":"script from retained hybrid table 1.1","license":"Community script; redistribution terms not supplied","attribution":"Credited table-script contributors","locator":"Const cGameName=play_a24; HandleMechanics=0; active SetLamp idiom has 15 output bindings plus one SetLamp subroutine definition, no Lampz.MassAssign and no vpmMapLights after whole-line comments are stripped; trough, saucers, Grotto, drop bank, kickback, flippers and sensors supply causality"},
        {"id":EXTRACTION_SOURCE,"kind":"vpx_table","uri":MANIFEST_PATH.as_posix(),"sha256":MANIFEST_CONTENT_SHA256,"revision":"vpxtool git:0561bb4","locator":f"2270 files; 164978347 bytes; algorithm: {MANIFEST_ALGORITHM}; canonical manifest SHA-256 {MANIFEST_SHA256}; 1748 files under gameitems/"},
        {"id":RENDER_SOURCE,"kind":"human_review","uri":f"external:pinmame-manuals/by-machine/{MACHINE_ID}/contributor-supplied/{MANUAL_FILENAME}","locator":"76-page contact sheet at 40 dpi; decisive matrix/coil pages rendered at 400 dpi, printed page 26 re-rendered at 600 dpi, and construction pages rendered at 300 dpi with Poppler on 2026-08-09. Tesseract/PDF text were secondary; rendered cells governed every mapping."},
    ]


def build_machine() -> dict[str,object]:
    inputs = diagnostic_inputs()+[switch_input(number) for number in range(1,65)]
    outputs = [solenoid_output(number) for number in range(1,51)]+[lamp_output(number) for number in range(1,65)]
    return {
        "format":"pinmame-machine-definition","schema_version":2,
        "machine":{"id":MACHINE_ID,"name":"Playboy 35th Anniversary","manufacturer":"Data East","year":1989,"kind":"physical_pinball","playfield":{"width":RIGHT,"height":BOTTOM,"units":"vpx","provenance":provenance("validated",TABLE_SOURCE)}},
        "coverage":{"status":"partial","missing":["controller_platform","output_semantics","mechanism_behavior","polarity","spatial_placement","unresolved_conflicts"],"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"conflicted","physical_wiring":"conflicted","mechanisms":"conflicted","variant_coverage":"validated","recreation_knowledge":"candidate","spatial_placement":"candidate"}},
        "controller":{"platform":"pinmame.dataeast","hardware_generation":"0x1000","inversion_applied_by_emulator":False},
        "drivers":[{"id":"play_a24","description":"Playboy 35th Anniversary (2.4)","year":"1989","manufacturer":"Data East","flags":0,"physical_compatibility":"identical","variant_notes":"The sole published driver. Exhaustive pinned-source search found no CORE_CLONEDEF and no second DRIVER entry; single-driver coverage is deliberate, not an omitted family."}],
        "inputs":inputs,"outputs":outputs,"displays":displays(),"mechanisms":mechanisms(),
        "relationships":[{"id":f"relationship.lr-relay-{number}","kind":"relay_gated","source":"coil.driver-10","destination":f"coil.driver-{number}","provenance":provenance("conflicted",CORE_SOURCE,MANUAL_SOURCE)} for number in range(25,33)],
        "sources":sources(),"knowledge":{"path":KNOWLEDGE_PATH.as_posix(),"status":"partial"},"conflicts":conflicts(),
    }


def build_spatial(machine: dict[str,object]) -> dict[str,object]:
    resolved = []
    for device in machine["inputs"] + machine["outputs"] + machine["displays"]:
        spatial = device.get("spatial")
        if isinstance(spatial,dict) and spatial.get("status") != "not_applicable":
            resolved.append({"id":device["id"],"status":spatial["status"],"placements":len(spatial["placements"])})
    all_lamps = [f"lamp.matrix-{number}" for number in range(1,65)]
    conflict_ids = [conflict["id"] for conflict in machine["conflicts"]]
    return {
        "format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,
        "coordinate_system":{"space":"playfield","x":"0 left, 1 right","y":"0 rear/backglass, 1 front/apron","normalization":"x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top)","raw_bounds":{"left":0.0,"top":0.0,"right":RIGHT,"bottom":BOTTOM}},
        "evidence":{"manual_sha256":MANUAL_SHA256,"table_sha256":TABLE_SHA256,"script_sha256":SCRIPT_SHA256,"extraction_manifest_algorithm":MANIFEST_ALGORITHM,"extraction_manifest_sha256":MANIFEST_SHA256},
        "method":[
            "Asserted both exact gamedata.json bounds (0,0)-(952,1974) before normalization; neither dimension permits borrowing geometry from another machine.",
            "Read every decisive switch-, lamp-, and coil-table cell from rendered manual pages. Text extraction and OCR were only location and second-reading aids.",
            "Established runtime visual consumption only from executable SetLamp callbacks and UpdateLamps routing after whole-line VBScript comments were removed.",
            "Treated numeric object names as candidates. Explicit routing establishes a consumer binding, but object centers remain candidate physical placements unless an executable sensor supplies observed geometry.",
            "Used script for causal topology and rendered manual construction pages for assemblies. A printed feature label alone never created a mechanism edge.",
            "Used the printed-page-26 coil/flash plan and separate backbox inset for physical-plane classification and broad feature locations. Repeated group callouts, unresolved small inset digits, and the unregistered drawing frame do not provide normalized socket centers; disagreements with retained playfield effect objects remain explicit.",
        ],
        "excluded_helpers":{
            "numeric-light-gap":"The nine absent numeric Light names are 26, 32 and 57-63. Each address is explicitly routed to a same-number Flasher proxy and the manual places it in its separate backbox/back-panel box; none is a missing controller output.",
            "pinball-backglass-row":"Same-number Light objects 41, 49, 53-56 and 64 are executable consumers and are flagged is_backglass=true, but the manual location drawing does not show those seven addresses in either its backbox box or playfield plan. Their presentation-row centers are withheld because no physical source establishes the socket plane.",
            "laser-helper":"The off-bounds sw17 helper and unbound visible sw17a are excluded. Kicker001_Hit explicitly publishes switch 17 from an in-bounds kickback object, whose center is retained at candidate strength.",
            "gi-and-flash-proxies":"The 47 aGiLights entries and grouped flasher objects are visual effects, not surveys of physical bulb sockets.",
            "synthetic-flipper-states":"Public outputs 45-48 are PinMAME-generated winding states mapped to two physical flipper assemblies. They are virtual addresses with no independent quantity or placement.",
        },
        "projection_classes":[
            {"class":"setlamp-coordinate-candidate","devices":[device for device in all_lamps if int(device.rsplit('-',1)[1]) not in BACKBOX_LAMPS | MANUAL_UNLOCATED_PINBALL_LAMPS],"status":"candidate","reason":"Executable same-number routing proves a visual consumer; numeric Light centers are not socket surveys."},
            {"class":"mechanical-effect-object","devices":["coil.driver-16","coil.driver-17","coil.driver-18","coil.driver-19","coil.driver-21","coil.driver-22","coil.driver-25","coil.driver-26","coil.driver-27","coil.driver-28","coil.driver-29","coil.driver-30"],"status":"candidate","reason":"Direct events and sensor geometry expose playfield effect anchors rather than under-playfield coil centers."},
        ],
        "resolved":sorted(resolved,key=lambda row:row["id"]),
        "unresolved":[
            {"dimension":"physical_socket_binding","devices":all_lamps,"reason":"Playfield lamp centers are table candidates, nine manual-located backbox lamps are deliberately unprojected, and seven PINBALL-letter sockets are not located by the manual despite having table presentation proxies."},
            {"dimension":"flasher_socket_binding","devices":[f"coil.driver-{number}" for number in [1,2,3,4,5,6,7,8,9,13,14,15]],"reason":"The manual plan and backbox inset establish broad groups and certain backbox membership, but grouped callouts and five unresolved small inset digits do not identify every socket or complete each plane split; retained effects are presentation-only. Output 12 is excluded because its four clearly assigned backbox symbols equal its complete four-bulb schematic quantity and no output-12 callout appears on the playfield plan."},
            {"dimension":"raw-mux-timing","devices":["coil.driver-10"]+[f"coil.driver-{number}" for number in range(25,33)],"reason":"Decoded public outputs are usable, but a board-level recreation would still need the exact one-IRQ PIA/K1 relationship and electrical polarity. Address 31 has no fitted physical device, but no trace proves its decoded public slot is constant-zero."},
        ],
        "blockers":[
            {"dimension":"controller_platform","devices":["pinmame.dataeast"],"reason":"Data East uses a System 11-derived emulator implementation, but its board family and diagnostics are not represented by the Williams-only pinmame.system-11 profile.","would_resolve":"A reviewed Data East controller profile derived from the pinned core and original board documentation."},
            {"dimension":"output_semantics","devices":["coil.driver-4","coil.driver-5","coil.driver-13","coil.driver-14","coil.driver-15","coil.driver-19"]+[f"coil.driver-{number}" for number in range(25,33)],"reason":"Callback aliases/comments disagree with printed groups, one public special-solenoid state is also a background proxy, core PWM typing disagrees with the physical C-bank fitment, and unfitted address 31 lacks a decoded-state trace.","would_resolve":"Original-machine lamp/coil-test video synchronized with public output traces and a harness endpoint survey."},
            {"dimension":"mechanism_behavior","devices":["mechanism.grotto-kicker","mechanism.left-slingshot","mechanism.right-slingshot","mechanism.left-pop","mechanism.center-pop","mechanism.right-pop"],"reason":"Script establishes event edges but not the hidden Grotto transfer geometry or hardware-triggered special-coil pulse behavior.","would_resolve":"Original-machine captures of the Grotto ball path and each special-solenoid switch/coil waveform."},
            {"dimension":"polarity","devices":["switch.matrix-15","switch.matrix-16","coil.driver-10","coil.driver-45","coil.driver-46","coil.driver-47","coil.driver-48"],"reason":"The core publishes cabinet buttons at manual EOS addresses and decoded mux states, but no at-rest/end-of-stroke or relay electrical trace proves physical polarity.","would_resolve":"Bench capture of cabinet button, EOS, K1 relay, raw A/C driver and public output states."},
            {"dimension":"spatial_placement","devices":all_lamps+[f"coil.driver-{number}" for number in [1,2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,21,22,25,26,27,28,29,30]],"reason":"Lamp and mechanism coordinates remain retained-table candidates; the manual supplies broad flash groups and backbox/playfield splits but not registered socket centers, and seven routed PINBALL lamps have no physical location in its drawing. Output 12 is classified as backbox-only and needs no playfield coordinate.","would_resolve":"A dimensionally registered original playfield/backbox survey or address-by-address photographs correlated with lamp, coil, and mechanism tests."},
            {"dimension":"unresolved_conflicts","devices":conflict_ids,"reason":"Ten machine-specific source disagreements remain first-class and promotion-critical.","would_resolve":"Independent original-machine observations or corrected authoritative sources that explicitly settle each recorded conflict."},
        ],
        "conflicts":conflict_ids,
        "promotion_decision":"Keep partial. The record enumerates every public address and resolves the major topology, but output annotations/typing, physical polarity, special-coil behavior, lamp socket placement, and ten preserved conflicts prevent author-ready promotion.",
    }


def spatial_markdown(report: dict[str,object]) -> str:
    rows = [
        "# Playboy 35th Anniversary spatial-resolution report","",
        "Exact retained-table bounds: `left=0`, `top=0`, `right=952`, `bottom=1974`.","",
        "Both extents are asserted, and no other machine geometry was reused.","",
        "## Extraction identity","",
        f"- Manifest algorithm: {report['evidence']['extraction_manifest_algorithm']}",
        f"- Manifest SHA-256: `{report['evidence']['extraction_manifest_sha256']}`","",
        "## Promotion decision","",report["promotion_decision"],"","## Blockers","",
    ]
    for blocker in report["blockers"]:
        rows.extend([f"### {blocker['dimension']}","",blocker["reason"],"",f"Would resolve: {blocker['would_resolve']}","","Devices: " + ", ".join(f"`{device}`" for device in blocker["devices"]),""])
    rows.extend(["## Resolver controls",""]+[f"- {method}" for method in report["method"]]+["","## Excluded helpers",""]+[f"- `{key}`: {value}" for key,value in report["excluded_helpers"].items()]+[""])
    return "\n".join(rows)


def knowledge_markdown(machine: dict[str,object]) -> str:
    missing = ", ".join(f"`{value}`" for value in machine["coverage"]["missing"])
    return f"""# Data East Playboy 35th Anniversary (1989)

Machine definition: `{MACHINE_PATH.as_posix()}`

## Identity and controller contract

Pinned PinMAME publishes one driver only: `play_a24`, from `CORE_GAMEDEF(play,a24,...)`. An exhaustive search found no `CORE_CLONEDEF` and no second catalog driver for the title. The single-driver record is deliberate, not an overlooked clone family.

`INITGAMES11(play, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, S11_MUXDELAY)` must be decoded against `core_tGameData`, not guessed from local argument names. It sets generation `GEN_DE` (`0x1000`), display layout `de_dispAlpha2`, `hw.flippers=FLIP1516`, zero switch/lamp/custom-solenoid offsets, `hw.soundBoard=SNDBRD_DE1S`, `hw.display=0`, `hw.gameSpecific1=S11_MUXDELAY`, and `sxx.muxSol=10`. The display layout supplies two seven-character alphanumeric and two seven-character numeric displays; all are controlled backbox devices with `not_applicable` playfield spatial records.

`S11_MUXDELAY` is bit `0x10`, documented as “delay mux solenoid by one IRQ.” In `pia0b_w`, Playboy retains the current PIA port-B byte and publishes the previous byte. `updsol` then uses solenoid 10/K1 to expose the common eight drivers as A-side public outputs 1-8 or C-side 25-32. This compensates for the ROM's relay timing so the decoded public states land in the correct bank. A VPX-style recreation consuming PinMAME outputs 1-8 and 25-32 must not add another delay or rebuild the raw mux. A raw PIA/board emulator must reproduce the one-IRQ latch; a physical recreation may still model K1 relay construction and sound.

Pinned `s11.c` types output 9 as a bulb, 11 as GI, 12-15 as bulbs, and 25-32 as eight muxed #89 bulbs under K1 at output 10. The manual instead fits physical coils at 25-30 and 32, with branch 31 unfitted. The core type is output/PWM metadata, not physical-fitment authority, so the disagreement stays a conflict.

## Address coverage

- Inputs enumerate service switches -7/-6, DIP/jumper 0, and matrix addresses 1-64.
- Outputs enumerate lamps 1-64 and System 11 public solenoids 1-50.
- Solenoid 23 is Game On; 24 is unused; 33-44 are inert; 45-48 are synthetic lower-flipper winding states; 49 is a simulation-only shooter state; 50 is reserved.
- Solenoid 10 is K1, which selects the C-bank block at public outputs 25-32.

The controller id is `pinmame.dataeast`, not `pinmame.system-11`: sharing PinMAME's `s11.c` implementation does not turn the physical Data East CPU/driver board into Williams System 11 hardware. `INITGAMES11` leaves Playboy's `wpc.invSw` array zero-initialized, and `core.c` copies that zero mask into `coreGlobals.invSw`, so the emulator applies no per-game switch inversion for this driver. No reviewed Data East controller profile exists yet, so `controller_platform` remains an explicit promotion blocker.

The manual prints physical flipper EOS contacts at matrix 15/16, but `FLIP1516` makes the non-fliptronic core overwrite those public addresses with left/right cabinet-button state. This is a PinMAME public-address behavior rather than a description of the physical EOS wiring. A recreation should use public 15/16 as cabinet-button state and must not infer physical EOS state from them.

## Lamp mapping and object accounting

The active table uses `SetLamp`: 16 active occurrences, with no `Lampz.MassAssign` and no `vpmMapLights`. Mapping claims therefore remain specific to this retained implementation.

Only 55 numeric `L*` Light objects exist for 64 addresses. The nine absent names are 26, 32, and 57-63. They are not missing outputs: `UpdateLamps` explicitly routes all nine to same-number Flasher objects, and the manual location drawing puts those exact addresses in a separate backbox/back-panel box. They therefore have controlled `not_applicable` playfield-spatial records. The drawing does not locate PINBALL-letter lamps 41, 49, 53-56, or 64 in either its backbox box or playfield plan. Their same-number table objects are presentation proxies flagged as backglass; those centers are withheld without turning the manual's silence into a false playfield claim.

Numeric Light objects 41, 49, 53, 54, 55, 56, and 64 are executable consumers but are flagged `is_backglass=true` in the retained table. The manual location drawing does not locate these PINBALL-letter lamps in either its backbox box or playfield plan. Their names prove consumption, not a physical socket plane, so their coordinates are withheld as unresolved placement evidence rather than classified as a source conflict. All remaining Light centers are only candidate placement evidence.

## Mechanism topology

Script causality plus manual construction establishes a serial three-ball trough and eject, outhole feeder, VUK, Champagne saucer, two-sensor Grotto path with kickout, three-face resetting drop bank, Laser Kick outlane kickback, two flippers, two slingshots, three pop bumpers, seven fixed PLAYBOY standups, three fixed center standups, manual shooter, and passive lanes/ramps/spinner. The fixed target banks are not drop banks: their drawings show independent leaf-switch stations and no reset coil.

The printed coil/flash location page adds a separate backbox inset to the playfield plan. It proves that outputs 3, 4, 8, 9, 12, 14 and 15 include backbox bulbs even though every retained VPX effect for those outputs sits in playfield space; output 12's four clear inset symbols already equal its complete schematic quantity. Three 5/6-like and two 13/16-like inset glyphs remain deliberately unassigned. The certain per-address minima are retained in the output notes. The diagram supports physical-plane classification and broad feature locations, but its grouped bubbles, unresolved small digits and lack of a registered coordinate frame do not support normalized socket centers.

The Laser Kick uses candidate Kicker001 geometry because `Kicker001_Hit` explicitly publishes switch 17. The off-bounds sw17 helper and unbound visible sw17a are excluded. Pinned `s11.c` PIA comments identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4; applying `setSSSol`'s Data East offsets `{3,4,5,1,0,2}` derives printed SP1, SP3, SP4, SP6, SP5 and SP2 at public addresses 17-22. This is not inferred by treating printed SP numbers as handler indices. The manual, retained table geometry, and working script agree on the pop switches: Bumper2 is the center pop at switch 47 and Bumper3 is the right pop at switch 48; their SP1/SP2 coils are public outputs 17/22 respectively. Hidden Grotto transfer construction and special-solenoid pulse timing remain unresolved.

## Literal transcription and reconciliation

The 76-page manual has SHA-256 `{MANUAL_SHA256}` and a 76,678-character text layer. That layer was not trusted for multi-column tables: all decisive switch, lamp, coil and construction cells were read from 300/400 dpi renders. Excerpts preserve printed capitalization, abbreviations and typos such as `Ctr 3 Bank-Mid`, `DropTar. 50K`, `pinbAll`, `mansIon`, schematic `23-1200`, and chart `12-1200`. Normalized semantic labels appear only in the machine record, while disagreements remain in its reconciliation conflicts.

## Retained table and geometry

The table SHA-256 is `{TABLE_SHA256}`, contains 1,748 gameitems, and binds `Const cGameName = "play_a24"`. Its exact bounds are right 952 and bottom 1974. Both values are asserted before normalization, and no other machine's geometry is reused.

## Coverage and blockers

Status remains `partial`; `coverage.missing` is [{missing}].

- `controller_platform`: no reviewed Data East controller profile yet represents this physical board family.
- `output_semantics`: callback group aliases/comments and core C-bank bulb typing disagree with printed physical functions.
- `mechanism_behavior`: hidden Grotto transfer geometry and hardware-triggered special-coil pulse behavior are absent.
- `polarity`: no original-machine trace reconciles cabinet button/EOS, K1 relay, and raw versus decoded output states.
- `spatial_placement`: table objects are presentation candidates, flash groups lack socket surveys, and seven routed PINBALL lamps are not located by the manual's drawing at all.
- `unresolved_conflicts`: ten source disagreements remain first-class.

## Recreation boundary

Consume PinMAME's decoded public mux outputs without adding another IRQ delay. Treat public 15/16 as flipper buttons rather than physical EOS contacts. Do not convert presentation proxies into extra hardware, infer socket locations from names, or erase the manual/core and manual/table disagreements.
"""


LEDGER_ANCHOR = "Data East Playboy 35th Anniversary (`data-east.playboy-35th-anniversary.1989`)"
LEDGER_BLOCK = """Data East Playboy 35th Anniversary (`data-east.playboy-35th-anniversary.1989`) was curated on 2026-08-09, replacing `stub.pinmame.play_a24`. Pinned source contains the single `CORE_GAMEDEF(play,a24,...)` and no `CORE_CLONEDEF`; the one-driver physical family is deliberate. It remains `partial` with `coverage.missing = ["controller_platform", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"]` and ten preserved conflicts. The retained geometry is exactly 952 by 1974, and both extents are asserted before normalization. The controller id is `pinmame.dataeast`; sharing PinMAME's `s11.c` implementation does not make the physical CPU/driver board Williams System 11 hardware, and a reviewed Data East controller profile is still required.

Six points generalise from this record.

1. **`S11_MUXDELAY` is public-output timing, not a second mux for consumers to recreate.** Playboy sets a non-zero `gameSpecific1` value. `pia0b_w` delays its PIA port-B byte by one IRQ; `updsol` then attributes the shared A/C driver byte to outputs 1-8 or 25-32 using K1 at output 10. Decoded-output recreations must not add another delay, while raw PIA/board emulation must reproduce the latch.
2. **The flipper EOS/button disagreement comes from the public PinMAME address contract.** The manual prints EOS contacts at the two `FLIP_SWNO` addresses while PinMAME publishes cabinet-button state there. Keep the pair as conflicts and consume the public addresses as buttons.
3. **Object-count gaps can describe a presentation choice rather than missing mappings.** The table has 55 numeric Light names for 64 lamp addresses. The missing nine—26, 32 and 57-63—are explicitly routed to Flasher proxies and are exactly the lamps the manual locates in a separate backbox/back-panel box. Seven named PINBALL Light proxies are also flagged backglass, but the manual drawing does not locate those addresses at all; presentation names and centers therefore do not prove their physical plane.
4. **Lamp idioms remain table-specific evidence.** Playboy uses 16 active `SetLamp` occurrences and neither `Lampz.MassAssign` nor `vpmMapLights`. Count executable routes and reconcile every address; do not transfer mapping rules between tables.
5. **A flasher output can span both the playfield and backbox, while a VPX recreation may model only playfield effects.** Playboy's printed inset clearly assigns backbox bulbs to outputs 3, 4, 8, 9, 12, 14 and 15, but every retained VPX effect for those outputs sits in playfield space; output 12's clear backbox count already equals its schematic total. Preserve certain minima, mark unreadable digits unresolved and treat the VPX points as presentation consumers rather than physical sockets.
6. **Data East's printed SP1-SP6 sequence does not equal PinMAME public 17-22 order.** The nearby `s11.c` PIA comments—not an assumed printed-number/handler correspondence—identify handlers 0-5 as SP6, SP5, SP2, SP3, SP1 and SP4. Applying `setSSSol`'s Data East offsets `{3,4,5,1,0,2}` derives printed SP1, SP3, SP4, SP6, SP5 and SP2 at public 17-22. Preserve each printed SP number as a manual alias, derive the public binding from both the handler comments and permutation, and keep an unfitted SP6 as the physical unused driver at public 20 rather than shifting it to 22.

"""


def merge_ledger(current: str) -> str:
    if LEDGER_BLOCK in current:
        return current
    if LEDGER_ANCHOR in current:
        raise ValueError("Playboy 35th Anniversary ledger entry exists but differs from the generated block")
    marker = "Before selecting a game, check this ledger"
    if marker not in current:
        raise ValueError("CURRENT-STATE insertion marker missing")
    return current.replace(marker,LEDGER_BLOCK+marker,1)


def json_text(value: object) -> str:
    return json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n"


def desired_files() -> dict[Path,str]:
    machine = build_machine()
    spatial = build_spatial(machine)
    return {
        MACHINE_PATH:json_text(machine),SEED_PATH:json_text(machine),SPATIAL_JSON_PATH:json_text(spatial),
        SPATIAL_MD_PATH:spatial_markdown(spatial),KNOWLEDGE_PATH:knowledge_markdown(machine),**EXCERPTS,
    }


def compare_lf(path: Path, expected: str) -> bool:
    return path.is_file() and path.read_text(encoding="utf-8").replace("\r\n","\n") == expected.replace("\r\n","\n")


def coverage_markdown(report: dict[str,object]) -> str:
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


def queue_markdown(queue: dict[str,object]) -> str:
    rows = ["# Curation queue","","Physical machines are processed newest-to-oldest. Unknown-year candidates are last, and related driver variants stay together.","","| Order | Year | Machine | Manufacturer | Status |","| ---: | ---: | --- | --- | --- |"]
    for entry in queue["entries"]:
        year = str(entry["year"]) if entry["year"] is not None else "unknown"
        rows.append(f"| {entry['order']} | {year} | {entry['name']} | {entry['manufacturer']} | {entry['coverage_status']} |")
    return "\n".join(rows)+"\n"


def generate() -> None:
    if (ROOT/AUTHOR_READY_PATH).exists():
        raise RuntimeError(f"refusing to overwrite partial artifacts while {AUTHOR_READY_PATH.as_posix()} exists")
    for relative,content in desired_files().items():
        write_text(ROOT/relative,content.replace("\r\n","\n"))
    for path in [ROOT/STUB_PATH,ROOT/STUB_KNOWLEDGE_PATH]:
        if path.exists():
            path.unlink()
    ledger_path = ROOT/"docs/CURRENT-STATE.md"
    write_text(ledger_path,merge_ledger(ledger_path.read_text(encoding="utf-8").replace("\r\n","\n")))
    rebuild_catalog(ROOT)
    write_coverage_report(ROOT)


def check() -> None:
    drift = [relative.as_posix() for relative,content in desired_files().items() if not compare_lf(ROOT/relative,content)]
    if not (ROOT/MANIFEST_PATH).is_file() or sha256_file(ROOT/MANIFEST_PATH) != MANIFEST_CONTENT_SHA256:
        drift.append(MANIFEST_PATH.as_posix())
    if (ROOT/AUTHOR_READY_PATH).exists():
        drift.append(AUTHOR_READY_PATH.as_posix())
    if (ROOT/STUB_PATH).exists() or (ROOT/STUB_KNOWLEDGE_PATH).exists():
        drift.extend([STUB_PATH.as_posix(),STUB_KNOWLEDGE_PATH.as_posix()])
    ledger = (ROOT/"docs/CURRENT-STATE.md").read_text(encoding="utf-8").replace("\r\n","\n")
    if ledger.count(LEDGER_ANCHOR) != 1 or LEDGER_BLOCK not in ledger:
        drift.append("docs/CURRENT-STATE.md")
    catalog = load_json(ROOT/"catalog/pinmame.json")
    machine_rows = [row for row in catalog["machines"] if row["id"] == MACHINE_ID]
    if len(machine_rows) != 1 or machine_rows[0].get("definition") != MACHINE_PATH.as_posix() or machine_rows[0].get("definition_sha256") != content_sha256(build_machine()):
        drift.append("catalog/pinmame.json")
    driver_row = {row["id"]:row for row in catalog["drivers"]}.get("play_a24",{})
    if driver_row.get("machine_id") != MACHINE_ID or driver_row.get("definition") != MACHINE_PATH.as_posix():
        drift.append("catalog/pinmame.json")
    coverage = build_coverage_report(ROOT)
    queue = build_curation_queue(ROOT)
    generated = {
        Path("reports/coverage.json"):json_text(coverage),Path("reports/coverage.md"):coverage_markdown(coverage),
        Path("reports/curation-queue.json"):json_text(queue),Path("reports/curation-queue.md"):queue_markdown(queue),
    }
    drift.extend(relative.as_posix() for relative,content in generated.items() if not compare_lf(ROOT/relative,content))
    if drift:
        raise SystemExit("drift: "+", ".join(sorted(set(drift))))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the reviewed Data East Playboy 35th Anniversary physical-machine record")
    parser.add_argument("--check",action="store_true",help="refuse generated-artifact drift; CRLF and LF compare equally")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
