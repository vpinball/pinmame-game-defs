"""Curate the physical Stern The Lord of the Rings (2003) machine definition.

The builder is side-effect free and deterministic: it embeds the transcribed manual tables,
the four-recreation spatial derivation, and every reviewed label, wiring detail and
normalized coordinate as literals, so regeneration reproduces the canonical artifacts
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.
``--export-transcription`` writes the embedded, reviewed manual transcription to an explicit
external evidence path so the source record can be reconstructed and hash-verified.

The embedded spatial artifact treats three factory-layout recreations as measurements of one
physical machine. Independence between them is unestablished, so a placement is validated only
when all three agree. A fourth Neo LED recreation is a disclosed JPSalas derivative and contributes
only supplemental measurements for addresses 81-99. Each table's actual script binding selects the
positioned object; disagreements are recorded and printed diagrams break ties.

The definition, the spatial report and the knowledge note are all generated here from the same
objects, and ``--check`` byte-compares all four artifacts against what this module produces. That
comparison folds CRLF to LF first, so a checkout Git rewrote under ``core.autocrlf=true`` still
passes while every other byte difference still fails; see ``_comparable``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/stern/lord-of-the-rings-2003.json"
SEED_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-2003.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/lord-of-the-rings-2003.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/lord-of-the-rings-2003.md"

ROM_SETS = json.loads(
	"{\"lotr\": [\"lotrcpua.a00\", \"lotrdspa.a00\", \"LOTR_SND\"], \"lotr3\": [\"lotrcpu.300\", \"lotrdspa.300\", \"LOTR_SND\"], \"lotr4\": [\"lotrcpu.401\", \"lotrdspa.403\", \"LOTR_SND\"], \"lotr41\": [\"lotrcpu.410\", \"lotrdspa.404\", \"LOTR_SND\"], \"lotr5\": [\"lotrcpu.500\", \"lotrdspa.500\", \"LOTR_SND\"], \"lotr51\": [\"lotrcpu.501\", \"lotrdspa.501\", \"LOTR_SND\"], \"lotr6\": [\"lotrcpu.600\", \"lotrdspa.600\", \"LOTR_SND\"], \"lotr7\": [\"lotrcpu.700\", \"lotrdspa.700\", \"LOTR_SND\"], \"lotr8\": [\"lotrcpu.800\", \"lotrdspa.800\", \"LOTR_SND\"], \"lotr9\": [\"lotrcpu.900\", \"lotrdspa.900\", \"LOTR_SND\"], \"lotr_f41\": [\"lotrcpu.410\", \"lotrdspf.404\", \"LOTR_SND\"], \"lotr_f51\": [\"lotrcpu.501\", \"lotrdspf.501\", \"LOTR_SND\"], \"lotr_fr\": [\"lotrcpua.a00\", \"lotrdspf.a00\", \"LOTR_SND\"], \"lotr_fr4\": [\"lotrcpu.401\", \"lotrdspf.403\", \"LOTR_SND\"], \"lotr_fr5\": [\"lotrcpu.500\", \"lotrdspf.500\", \"LOTR_SND\"], \"lotr_fr6\": [\"lotrcpu.600\", \"lotrdspf.600\", \"LOTR_SND\"], \"lotr_fr7\": [\"lotrcpu.700\", \"lotrdspf.700\", \"LOTR_SND\"], \"lotr_fr8\": [\"lotrcpu.800\", \"lotrdspf.800\", \"LOTR_SND\"], \"lotr_fr9\": [\"lotrcpu.900\", \"lotrdspf.900\", \"LOTR_SND\"], \"lotr_g41\": [\"lotrcpu.410\", \"lotrdspg.404\", \"LOTR_SND\"], \"lotr_g51\": [\"lotrcpu.501\", \"lotrdspg.501\", \"LOTR_SND\"], \"lotr_gr\": [\"lotrcpua.a00\", \"lotrdspg.a00\", \"LOTR_SND\"], \"lotr_gr4\": [\"lotrcpu.401\", \"lotrdspg.403\", \"LOTR_SND\"], \"lotr_gr5\": [\"lotrcpu.500\", \"lotrdspg.500\", \"LOTR_SND\"], \"lotr_gr6\": [\"lotrcpu.600\", \"lotrdspg.600\", \"LOTR_SND\"], \"lotr_gr7\": [\"lotrcpu.700\", \"lotrdspg.700\", \"LOTR_SND\"], \"lotr_gr8\": [\"lotrcpu.800\", \"lotrdspg.800\", \"LOTR_SND\"], \"lotr_gr9\": [\"lotrcpu.900\", \"lotrdspg.900\", \"LOTR_SND\"], \"lotr_i41\": [\"lotrcpu.410\", \"lotrdspi.404\", \"LOTR_SND\"], \"lotr_i51\": [\"lotrcpu.501\", \"lotrdspi.501\", \"LOTR_SND\"], \"lotr_it\": [\"lotrcpua.a00\", \"lotrdspi.a00\", \"LOTR_SND\"], \"lotr_it4\": [\"lotrcpu.401\", \"lotrdspi.403\", \"LOTR_SND\"], \"lotr_it5\": [\"lotrcpu.500\", \"lotrdspi.500\", \"LOTR_SND\"], \"lotr_it6\": [\"lotrcpu.600\", \"lotrdspi.600\", \"LOTR_SND\"], \"lotr_it7\": [\"lotrcpu.700\", \"lotrdspi.700\", \"LOTR_SND\"], \"lotr_it8\": [\"lotrcpu.800\", \"lotrdspi.800\", \"LOTR_SND\"], \"lotr_it9\": [\"lotrcpu.900\", \"lotrdspi.900\", \"LOTR_SND\"], \"lotr_le\": [\"lotrcpua.a02\", \"lotrdspa.a00\", \"LOTR_SND\"], \"lotr_s51\": [\"lotrcpul.501\", \"lotrdspl.501\", \"LOTR_SND_SP\"], \"lotr_sp\": [\"lotrcpul.a00\", \"lotrdspl.a00\", \"LOTR_SND_SP\"], \"lotr_sp4\": [\"lotrcpul.401\", \"lotrdspl.403\", \"LOTR_SND_SP\"], \"lotr_sp5\": [\"lotrcpul.500\", \"lotrdspl.500\", \"LOTR_SND_SP\"], \"lotr_sp6\": [\"lotrcpul.600\", \"lotrdspl.600\", \"LOTR_SND_SP\"], \"lotr_sp7\": [\"lotrcpul.700\", \"lotrdspl.700\", \"LOTR_SND_SP\"], \"lotr_sp8\": [\"lotrcpul.800\", \"lotrdspl.800\", \"LOTR_SND_SP\"], \"lotr_sp9\": [\"lotrcpul.900\", \"lotrdspl.900\", \"LOTR_SND_SP\"]}"
)
EXTRACTION_FILE_HASHES = json.loads(
	"{\"vpx-extraction.lotr-hanibal-4k\": \"3a5c44e548ddce2bcf9efeb1751a4810abbb58b534189aae2009dadbae2d6a00\", \"vpx-extraction.lotr-jpsalas-600\": \"d22a75dd9a5d12d1000869a2c9b8adb8436328c291d5aa04eb40ce37ab7f5f96\", \"vpx-extraction.lotr-neo-led-mod-1-0-3\": \"4772db87992f0723710d1a484a87fd1658ed34690d100bf85c6ff4972c76967d\", \"vpx-extraction.lotr-vpw-1-6\": \"e53581bdfec7948d023766db238784a9d18acb0012530aa3d83ed5f2ea549269\"}"
)
transcription = json.loads(
	"{\"coil_table\": {\"auxiliary_uk_only\": {\"board\": \"UK 3X Transformer Driver Board\", \"coils\": [{\"address\": \"AUX 1\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J2-P3\", \"control_wire\": \"WHT\", \"name\": \"LEFT UP/DOWN POST\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q1\", \"voltage\": \"20v DC\"}, {\"address\": \"AUX 2\", \"coil_spec\": \"23-1100 / 090-5030-00T\", \"control_connector\": \"J2-P4\", \"control_wire\": \"RED\", \"name\": \"CENTER UP/DOWN POST\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q2\", \"voltage\": \"20v DC\"}, {\"address\": \"AUX 3\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J2-P7\", \"control_wire\": \"ORG\", \"name\": \"RIGHT UP/DOWN POST\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q3\", \"voltage\": \"20v DC\"}], \"edition_scoped\": \"uk\"}, \"coils\": [{\"address\": 1, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J8-P1\", \"control_wire\": \"BRN-BLK\", \"group\": \"high_current_1\", \"name\": \"TROUGH UP-KICKER\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q1\", \"voltage\": \"50v DC\"}, {\"address\": 2, \"board\": \"I/O Power Driver\", \"coil_spec\": \"24-940 / 090-5036-00T\", \"control_connector\": \"J8-P3\", \"control_wire\": \"BRN-RED\", \"group\": \"high_current_1\", \"name\": \"AUTO LAUNCH\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q2\", \"voltage\": \"50v DC\"}, {\"address\": 3, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00B\", \"control_connector\": \"J8-P4\", \"control_wire\": \"BRN-ORG\", \"group\": \"high_current_1\", \"name\": \"LEFT VUK\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q3\", \"voltage\": \"50v DC\"}, {\"address\": 4, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00B\", \"control_connector\": \"J8-P5\", \"control_wire\": \"BRN-YEL\", \"group\": \"high_current_1\", \"name\": \"TOP VUK\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q4\", \"voltage\": \"50v DC\"}, {\"address\": 5, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00B\", \"control_connector\": \"J8-P6\", \"control_wire\": \"BRN-GRN\", \"group\": \"high_current_1\", \"name\": \"RIGHT VUK\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q5\", \"voltage\": \"50v DC\"}, {\"address\": 6, \"board\": \"I/O Power Driver\", \"coil_spec\": \"20.5-480 / 090-5064-02\", \"control_connector\": \"J8-P7\", \"control_wire\": \"BRN-BLU\", \"group\": \"high_current_1\", \"name\": \"RING MAGNET\", \"note\": \"Own fuse F20, 4A 250v S.B., marked THIS GAME ONLY in the quick reference fuse chart\", \"power_connector\": \"J10-P3\", \"power_wire\": \"VIO-YEL\", \"transistor\": \"Q6\", \"voltage\": \"50v DC\"}, {\"address\": 7, \"board\": \"I/O Power Driver\", \"coil_spec\": \"23-800 / 090-5001-NL\", \"control_connector\": \"J8-P8\", \"control_wire\": \"BRN-VIO\", \"dots\": true, \"group\": \"high_current_1\", \"name\": \"RIGHT TOWER\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q7\", \"voltage\": \"50v DC\"}, {\"address\": 8, \"board\": \"I/O Power Driver\", \"coil_spec\": \"22-1080 / 090-5032-00T\", \"control_connector\": \"J8-P9\", \"control_wire\": \"BRN-GRY\", \"group\": \"high_current_1\", \"name\": \"LOOP DIVERTER\", \"power_connector\": \"J10-P1/2\", \"power_wire\": \"GRY-YEL~3A Fuse~YEL-VIO\", \"transistor\": \"Q8\", \"voltage\": \"50v DC\"}, {\"address\": 9, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J9-P1\", \"control_wire\": \"BLU-BRN\", \"group\": \"high_current_2\", \"name\": \"LEFT BUMPER\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q9\", \"voltage\": \"50v DC\"}, {\"address\": 10, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J9-P2\", \"control_wire\": \"BLU-RED\", \"group\": \"high_current_2\", \"name\": \"RIGHT BUMPER\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q10\", \"voltage\": \"50v DC\"}, {\"address\": 11, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00T\", \"control_connector\": \"J9-P4\", \"control_wire\": \"BLU-ORG\", \"group\": \"high_current_2\", \"name\": \"BOTTOM BUMPER\", \"power_connector\": \"J10-P4/5\", \"power_wire\": \"YEL-VIO\", \"transistor\": \"Q11\", \"voltage\": \"50v DC\"}, {\"address\": 12, \"control_connector\": \"J9-P5\", \"control_wire\": \"BLU-YEL\", \"name\": null, \"state\": \"not_used\", \"transistor\": \"Q12\"}, {\"address\": 13, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5044-00B\", \"control_connector\": \"J9-P6\", \"control_wire\": \"BLU-GRN\", \"group\": \"high_current_2\", \"name\": \"ORBIT PIN\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q13\", \"voltage\": \"20v DC\"}, {\"address\": 14, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J9-P7\", \"control_wire\": \"BLU-BLK\", \"group\": \"high_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: HELMS DEEP RT\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q14\", \"voltage\": \"50v DC\"}, {\"address\": 15, \"board\": \"I/O Power Driver\", \"coil_spec\": \"22-900 / 090-5020-20T\", \"control_connector\": \"J9-P8\", \"control_wire\": \"ORG-GRY\", \"group\": \"high_current_2\", \"name\": \"LEFT FLIPPER (50v RED/YEL)\", \"power_connector\": \"J10-P1/2\", \"power_wire\": \"GRY-YEL~3A Fuse~RED-YEL\", \"transistor\": \"Q15\", \"voltage\": \"50v DC\"}, {\"address\": 16, \"board\": \"I/O Power Driver\", \"coil_spec\": \"22-900 / 090-5020-20T\", \"control_connector\": \"J9-P9\", \"control_wire\": \"ORG-VIO\", \"group\": \"high_current_2\", \"name\": \"RIGHT FLIPPER (50v RED/YEL)\", \"power_connector\": \"J10-P1/2\", \"power_wire\": \"BLU-YEL~3A Fuse~RED-YEL\", \"transistor\": \"Q16\", \"voltage\": \"50v DC\"}, {\"address\": 17, \"board\": \"I/O Power Driver\", \"coil_spec\": \"23-800 / 090-5001-00T\", \"control_connector\": \"J7-P2\", \"control_wire\": \"VIO-BRN\", \"group\": \"low_current_1\", \"name\": \"LEFT SLINGSHOT\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q17\", \"voltage\": \"20v DC\"}, {\"address\": 18, \"board\": \"I/O Power Driver\", \"coil_spec\": \"23-800 / 090-5001-00T\", \"control_connector\": \"J7-P3\", \"control_wire\": \"VIO-RED\", \"group\": \"low_current_1\", \"name\": \"RIGHT SLINGSHOT\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q18\", \"voltage\": \"20v DC\"}, {\"address\": 19, \"board\": \"I/O Power Driver\", \"coil_spec\": \"26-1200 / 090-5020-00B\", \"control_connector\": \"J7-P4\", \"control_wire\": \"VIO-ORG\", \"group\": \"low_current_1\", \"name\": \"TOP SAUCER\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q19\", \"voltage\": \"20v DC\"}, {\"address\": 20, \"board\": \"I/O Power Driver\", \"coil_spec\": \"DC Relay 520-5066-00\", \"control_connector\": \"J7-P6\", \"control_wire\": \"VIO-YEL\", \"group\": \"low_current_1\", \"name\": \"BALROG MOTOR RELAY\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q20\", \"voltage\": \"20v DC\"}, {\"address\": 21, \"board\": \"I/O Power Driver\", \"coil_spec\": \"27-1500 / 090-5004-00T\", \"control_connector\": \"J7-P7\", \"control_wire\": \"VIO-GRN\", \"group\": \"low_current_1\", \"name\": \"SWORD LOCK RELEASE\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q21\", \"voltage\": \"20v DC\"}, {\"address\": 22, \"board\": \"I/O Power Driver\", \"coil_spec\": \"Motor 041-5088-01\", \"control_connector\": \"J7-P8\", \"control_wire\": \"VIO-BLU\", \"group\": \"low_current_1\", \"name\": \"BALROG MOTOR\", \"power_connector\": \"J7-P1\", \"power_wire\": \"BRN\", \"transistor\": \"Q22\", \"voltage\": \"20v DC\"}, {\"address\": 23, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J7-P9\", \"control_wire\": \"VIO-BLK\", \"group\": \"low_current_1\", \"kind\": \"flasher\", \"name\": \"FLASH: HELMS DEEP LT\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q23\", \"voltage\": \"20v DC\"}, {\"address\": 24, \"board\": \"I/O Power Driver\", \"coil_spec\": \"Opt. 5v\", \"control_connector\": \"J7-P10\", \"control_wire\": \"VIO-GRY\", \"group\": \"low_current_1\", \"name\": \"OPTIONAL COIL\", \"note\": \"Manual DR.7: coil Q24 is optional; if a coin meter, token dispenser or knocker is required, contact technical support. The known-working VPW script binds this address as the knocker.\", \"power_connector\": \"J16-P7\", \"power_wire\": \"RED\", \"state\": \"optional\", \"transistor\": \"Q24\", \"voltage\": \"5v DC\"}, {\"address\": 25, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J6-P1\", \"control_wire\": \"BLK-BRN\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: POPS X3\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q25\", \"voltage\": \"20v DC\"}, {\"address\": 26, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J6-P2\", \"control_wire\": \"BLK-RED\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"location\": \"Back Panel\", \"name\": \"FLASH: RING\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q26\", \"voltage\": \"20v DC\"}, {\"address\": 27, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J6-P3\", \"control_wire\": \"BLK-ORG\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"location\": \"Back Panel\", \"name\": \"FLASH: BACK PANEL\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q27\", \"voltage\": \"20v DC\"}, {\"address\": 28, \"control_connector\": \"J6-P4\", \"control_wire\": \"BLK-YEL\", \"name\": null, \"state\": \"not_used\", \"transistor\": \"Q28\"}, {\"address\": 29, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Red / 165-5004-02\", \"control_connector\": \"J6-P5\", \"control_wire\": \"BLK-GRN\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: RINGWRAITH\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q29\", \"voltage\": \"20v DC\"}, {\"address\": 30, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#906 Bulb / 165-5004-00\", \"control_connector\": \"J6-P6\", \"control_wire\": \"BLK-BLU\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: SWORD\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q30\", \"voltage\": \"20v DC\"}, {\"address\": 31, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#89 Bulb / 165-5000-89\", \"control_connector\": \"J6-P7\", \"control_wire\": \"BLK-VIO\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: DESTROY THE RING\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q31\", \"voltage\": \"20v DC\"}, {\"address\": 32, \"board\": \"I/O Power Driver\", \"coil_spec\": \"#89 Bulb / 165-5000-89\", \"control_connector\": \"J6-P8\", \"control_wire\": \"BLK-GRY\", \"group\": \"low_current_2\", \"kind\": \"flasher\", \"name\": \"FLASH: BALROG\", \"power_connector\": \"J6-P10\", \"power_wire\": \"ORG\", \"transistor\": \"Q32\", \"voltage\": \"20v DC\"}], \"flasher_addresses\": [14, 23, 25, 26, 27, 29, 30, 31, 32], \"note_from_manual\": \"In Test Flash Lamps Menu ('Flash' Icon), flashers tested are all flash lamps located between Q1-Q32. This game: Q14, Q23, Q25-Q27, Q29-Q32.\"}, \"format\": \"lotr-manual-transcription\", \"lamp_matrix\": {\"addressing\": \"address = (row - 1) * 8 + column\", \"columns\": [{\"column\": 1, \"connector\": \"J13-P9\", \"ic\": \"U17\", \"wire\": \"YEL-BRN\"}, {\"column\": 2, \"connector\": \"J13-P8\", \"ic\": \"U16\", \"wire\": \"YEL-RED\"}, {\"column\": 3, \"connector\": \"J13-P7\", \"ic\": \"U15\", \"wire\": \"YEL-ORG\"}, {\"column\": 4, \"connector\": \"J13-P6\", \"ic\": \"U14\", \"wire\": \"YEL-BLK\"}, {\"column\": 5, \"connector\": \"J13-P5\", \"ic\": \"U13\", \"wire\": \"YEL-GRN\"}, {\"column\": 6, \"connector\": \"J13-P4\", \"ic\": \"U12\", \"wire\": \"YEL-BLU\"}, {\"column\": 7, \"connector\": \"J13-P3\", \"ic\": \"U11\", \"wire\": \"YEL-VIO\"}, {\"column\": 8, \"connector\": \"J13-P1\", \"ic\": \"U10\", \"wire\": \"YEL-GRY\"}], \"geometry\": \"8 columns (18v, YEL-*, J13) x 10 rows (ground, Q33-Q42, J12)\", \"lamps\": [{\"address\": 1, \"bulb\": \"#555\", \"name\": \"(K) EEP\"}, {\"address\": 2, \"bulb\": \"#555\", \"name\": \"K (E) EP\"}, {\"address\": 3, \"bulb\": \"#555\", \"name\": \"KE (E) P\"}, {\"address\": 4, \"bulb\": \"#555\", \"name\": \"KEE (P)\"}, {\"address\": 5, \"bulb\": \"#555\", \"name\": \"THE FELLOWSHIP OF THE RING\"}, {\"address\": 6, \"bulb\": \"#555\", \"name\": \"THE TWO TOWERS\"}, {\"address\": 7, \"bulb\": \"#555\", \"name\": \"THE RETURN OF THE KING\"}, {\"address\": 8, \"bulb\": \"#555\", \"name\": \"SHOOT AGAIN\"}, {\"address\": 9, \"bulb\": \"#555\", \"name\": \"PIPPIN\"}, {\"address\": 10, \"bulb\": \"#555\", \"name\": \"MERRY\"}, {\"address\": 11, \"bulb\": \"#555\", \"name\": \"SAM\"}, {\"address\": 12, \"bulb\": \"#555\", \"name\": \"ARAGORN\"}, {\"address\": 13, \"bulb\": \"#555\", \"name\": \"FRODO\"}, {\"address\": 14, \"bulb\": \"#555\", \"name\": \"GANDALF\"}, {\"address\": 15, \"bulb\": \"#555\", \"name\": \"LEGOLES\", \"note\": \"printed LEGOLES in the manual; almost certainly LEGOLAS\"}, {\"address\": 16, \"bulb\": \"#555\", \"name\": \"GIMLI\"}, {\"address\": 17, \"bulb\": \"#555\", \"name\": \"BOROMIR\"}, {\"address\": 18, \"bulb\": \"#555\", \"name\": \"MYSTERY\"}, {\"address\": 19, \"bulb\": \"#555\", \"name\": \"FRODO ARROW\"}, {\"address\": 20, \"bulb\": \"#44\", \"name\": \"DESTROY RING\"}, {\"address\": 21, \"bulb\": \"#555\", \"name\": \"MODE START\"}, {\"address\": 22, \"bulb\": \"#555\", \"name\": \"PALANTIR\"}, {\"address\": 23, \"bulb\": \"#44\", \"name\": \"PALANTIR GLOBE\"}, {\"address\": 24, \"bulb\": \"#555\", \"name\": \"SPOT RING\"}, {\"address\": 25, \"bulb\": \"#555\", \"name\": \"PIPPIN ARROW\"}, {\"address\": 26, \"bulb\": \"#555\", \"name\": \"GIFT OF THE ELVES\"}, {\"address\": 27, \"bulb\": \"#555\", \"name\": \"LIGHT EXTRA BALL\"}, {\"address\": 28, \"bulb\": \"#555\", \"name\": \"RING MULTIBALL\"}, {\"address\": 29, \"bulb\": \"#555\", \"name\": \"BIG POINTS\"}, {\"address\": 30, \"bulb\": \"#555\", \"name\": \"LIGHT SPECIAL\"}, {\"address\": 31, \"bulb\": \"#555\", \"name\": \"SUPER RING FRENZY\"}, {\"address\": 32, \"bulb\": \"#555\", \"name\": \"2X SCORING\"}, {\"address\": 33, \"bulb\": \"#555\", \"name\": \"LEGOLES ARROW\", \"note\": \"printed LEGOLES in the manual; almost certainly LEGOLAS\"}, {\"address\": 34, \"bulb\": \"#555\", \"name\": \"L RAMP MAN RING\"}, {\"address\": 35, \"bulb\": \"#555\", \"name\": \"L RAMP DWARF RING\"}, {\"address\": 36, \"bulb\": \"#555\", \"name\": \"L RAMP ELF RING\"}, {\"address\": 37, \"bulb\": \"#555\", \"name\": \"GANDALF ARROW\"}, {\"address\": 38, \"bulb\": \"#555\", \"name\": \"C LOOP MAN RING\"}, {\"address\": 39, \"bulb\": \"#555\", \"name\": \"C LOOP DWARF RING\"}, {\"address\": 40, \"bulb\": \"#555\", \"name\": \"C LOOP ELF RING\"}, {\"address\": 41, \"bulb\": \"#555\", \"name\": \"GIMLI ARROW\"}, {\"address\": 42, \"bulb\": \"#555\", \"name\": \"EXTRA BALL\"}, {\"address\": 43, \"bulb\": \"#555\", \"name\": \"GOLLUM MULTIBALL\"}, {\"address\": 44, \"bulb\": \"#555\", \"name\": \"SPECIAL\"}, {\"address\": 45, \"bulb\": \"#555\", \"name\": \"MERRY ARROW\"}, {\"address\": 46, \"bulb\": \"#555\", \"name\": \"R ORBIT MAN RING\"}, {\"address\": 47, \"bulb\": \"#555\", \"name\": \"R ORBIT DWARF RING\"}, {\"address\": 48, \"bulb\": \"#555\", \"name\": \"R ORBIT ELF RING\"}, {\"address\": 49, \"bulb\": \"#555\", \"name\": \"ARAGORN ARROW\"}, {\"address\": 50, \"bulb\": \"#555\", \"name\": \"R RAMP MAN RING\"}, {\"address\": 51, \"bulb\": \"#555\", \"name\": \"R RAMP DWARF RING\"}, {\"address\": 52, \"bulb\": \"#555\", \"name\": \"R RAMP ELF RING\"}, {\"address\": 53, \"bulb\": \"#555\", \"name\": \"LOCK\"}, {\"address\": 54, \"bulb\": \"#555\", \"name\": \"LANES\"}, {\"address\": 55, \"bulb\": \"#555\", \"name\": \"TOWER\"}, {\"address\": 56, \"bulb\": \"#555\", \"name\": \"FLIPPER\"}, {\"address\": 57, \"bulb\": \"#555\", \"name\": \"(O) RC\"}, {\"address\": 58, \"bulb\": \"#555\", \"name\": \"O (R) C\"}, {\"address\": 59, \"bulb\": \"#555\", \"name\": \"OR (C)\"}, {\"address\": 60, \"bulb\": \"#555 Gm.\", \"location\": \"Back Panel\", \"name\": \"POTD U.L.\"}, {\"address\": 61, \"bulb\": \"#555 Gm.\", \"location\": \"Back Panel\", \"name\": \"POTD U.R.\"}, {\"address\": 62, \"bulb\": \"#555 Gm.\", \"location\": \"Back Panel\", \"name\": \"POTD L.L.\"}, {\"address\": 63, \"bulb\": \"#555 Gm.\", \"location\": \"Back Panel\", \"name\": \"POTD L.R.\"}, {\"address\": 64, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #1 BOT\"}, {\"address\": 65, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #2\"}, {\"address\": 66, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #3\"}, {\"address\": 67, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #4\"}, {\"address\": 68, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #5\"}, {\"address\": 69, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #6\"}, {\"address\": 70, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #7\"}, {\"address\": 71, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #8\"}, {\"address\": 72, \"bulb\": \"#44\", \"name\": \"SHOOTER LANE #9 TOP\"}, {\"address\": 73, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"ESCAPE THE RINGWRAITHS\"}, {\"address\": 74, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"GANDALF VS SARUMAN\"}, {\"address\": 75, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"WARG ATTACK\"}, {\"address\": 76, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"WAR OF THE ENTS\"}, {\"address\": 77, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"BATTLE WITH SHELOB\"}, {\"address\": 78, \"bulb\": \"#44\", \"location\": \"Back Panel\", \"name\": \"DESTROY THE WITCH-KING\"}, {\"address\": 79, \"bulb\": \"#555\", \"edition_scoped\": \"tournament_kit\", \"name\": \"TOURNAMENT BUTTON\"}, {\"address\": 80, \"bulb\": \"#555\", \"location\": \"In Cabinet\", \"name\": \"START BUTTON\"}], \"lamps_not_on_playfield\": {\"back_panel\": [60, 61, 62, 63, 73, 74, 75, 76, 77, 78], \"cabinet_or_optional\": [79, 80]}, \"rows\": [{\"connector\": \"J12-P1\", \"drive\": \"Q33\", \"row\": 1, \"wire\": \"RED-BRN\"}, {\"connector\": \"J12-P2\", \"drive\": \"Q34\", \"row\": 2, \"wire\": \"RED-BLK\"}, {\"connector\": \"J12-P3\", \"drive\": \"Q35\", \"row\": 3, \"wire\": \"RED-ORG\"}, {\"connector\": \"J12-P4\", \"drive\": \"Q36\", \"row\": 4, \"wire\": \"RED-YEL\"}, {\"connector\": \"J12-P5\", \"drive\": \"Q37\", \"row\": 5, \"wire\": \"RED-GRN\"}, {\"connector\": \"J12-P6\", \"drive\": \"Q38\", \"row\": 6, \"wire\": \"RED-BLU\"}, {\"connector\": \"J12-P8\", \"drive\": \"Q39\", \"row\": 7, \"wire\": \"RED-VIO\"}, {\"connector\": \"J12-P9\", \"drive\": \"Q40\", \"row\": 8, \"wire\": \"RED-GRY\"}, {\"connector\": \"J12-P10\", \"drive\": \"Q41\", \"row\": 9, \"wire\": \"RED-WHT\"}, {\"connector\": \"J12-P11\", \"drive\": \"Q42\", \"row\": 10, \"wire\": \"RED\"}], \"transposition_warning\": \"PinMAME's lamp column strobe corresponds to the manual's ROW (drive lines Q33-Q42); PinMAME's lamp row corresponds to the manual's COLUMN (return lines U17-U10). Do not map the axes by name.\"}, \"machine_id\": \"stern.lord-of-the-rings.2003\", \"source\": {\"document\": \"Lord-of-the-Rings-Manual.pdf\", \"method\": \"rendered at 300 dpi with pdftoppm and read from cropped halves; the PDF has no text layer\", \"pages\": {\"coil_and_flasher_locations\": \"PDF 9 (printed DR. 7)\", \"coil_table\": \"PDF 8 (printed DR. 6)\", \"lamp_matrix\": \"PDF 7 (printed DR. 5)\", \"switch_matrix\": \"PDF 6 (printed DR. 4)\"}, \"sha256\": \"1334be3a5471ebcf9b00659e2ff63e2eaea78efefab54cd57ed37a8c46ac8d2e\", \"transcribed\": \"2026-08-06\"}, \"source_anomalies\": [{\"addresses\": [15, 33], \"detail\": \"Lamps 15 and 33 are printed LEGOLES, not LEGOLAS. The spelling is consistent across both cells at 300 dpi, so it is the manual's own error rather than a scan artifact. Transcribed as printed; do not silently normalize.\", \"kind\": \"probable_manual_typo\"}, {\"addresses\": [4, 19], \"detail\": \"The known-working VPW script names coil 4 SolULVUK and coil 19 SolURKicker, where the manual prints TOP VUK and TOP SAUCER. Same addresses and same devices; the disagreement is label-only and the manual controls physical naming.\", \"kind\": \"cross_source_naming\"}], \"switch_matrix\": {\"addressing\": \"address = (column - 1) * 8 + row\", \"columns\": [{\"column\": 1, \"connector\": \"CN5-P1\", \"drive\": \"Q1\", \"wire\": \"GRN-BRN\"}, {\"column\": 2, \"connector\": \"CN5-P3\", \"drive\": \"Q2\", \"wire\": \"GRN-RED\"}, {\"column\": 3, \"connector\": \"CN5-P4\", \"drive\": \"Q3\", \"wire\": \"GRN-ORG\"}, {\"column\": 4, \"connector\": \"CN5-P5\", \"drive\": \"Q4\", \"wire\": \"GRN-YEL\"}, {\"column\": 5, \"connector\": \"CN5-P6\", \"drive\": \"Q5\", \"wire\": \"GRN-BLK\"}, {\"column\": 6, \"connector\": \"CN5-P7\", \"drive\": \"Q6\", \"wire\": \"GRN-BLU\"}, {\"column\": 7, \"connector\": \"CN5-P8\", \"drive\": \"Q7\", \"wire\": \"GRN-VIO\"}, {\"column\": 8, \"connector\": \"CN5-P9\", \"drive\": \"Q8\", \"wire\": \"GRN-GRY\"}], \"dedicated_switches\": [{\"address\": \"DS-1\", \"connector\": \"CN6-P2\", \"ic\": \"U206\", \"location\": \"on Cabinet Side\", \"name\": \"#1 LEFT FLIPPER BUTTON\", \"part\": \"180-5160-00\", \"wire\": \"GRY-BRN\"}, {\"address\": \"DS-2\", \"connector\": \"CN6-P3\", \"ic\": \"U206\", \"location\": \"Below Playfield\", \"name\": \"#2 LEFT FLIPPER E.O.S. (End-of-Stroke)\", \"part\": \"180-5149-00 on Flipper\", \"wire\": \"GRY-RED\"}, {\"address\": \"DS-3\", \"connector\": \"CN6-P4\", \"ic\": \"U206\", \"location\": \"on Cabinet Side\", \"name\": \"#3 RIGHT FLIPPER BUTTON\", \"part\": \"180-5160-00\", \"wire\": \"GRY-ORG\"}, {\"address\": \"DS-4\", \"connector\": \"CN6-P6\", \"ic\": \"U206\", \"location\": \"Below Playfield\", \"name\": \"#4 RIGHT FLIPPER E.O.S. (End-of-Stroke)\", \"part\": \"180-5149-00 on Flipper\", \"wire\": \"GRY-YEL\"}, {\"address\": \"DS-5\", \"connector\": \"CN6-P7\", \"ic\": \"U206\", \"name\": null, \"state\": \"not_used\", \"wire\": \"GRY-GRN\"}, {\"address\": \"DS-6\", \"connector\": \"CN6-P8\", \"ic\": \"U206\", \"in_test\": \"LEFT\", \"location\": \"on Coin Door\", \"name\": \"#6 VOLUME (RED BUTTON)\", \"part\": \"180-5192-02\", \"wire\": \"GRY-BLU\"}, {\"address\": \"DS-7\", \"connector\": \"CN6-P9\", \"ic\": \"U206\", \"in_test\": \"RIGHT\", \"location\": \"on Coin Door\", \"name\": \"#7 SERV. CRED. (GREEN BUTTON)\", \"part\": \"180-5192-04\", \"wire\": \"GRY-VIO\"}, {\"address\": \"DS-8\", \"connector\": \"CN6-P10\", \"ic\": \"U206\", \"in_test\": \"ENTER\", \"location\": \"on Coin Door\", \"name\": \"#8 BEGIN TEST (BLACK BUTTON)\", \"part\": \"180-5192-02\", \"wire\": \"GRY-BLK\"}], \"geometry\": \"8 drive columns (Q1-Q8, GRN-*, CN5) x 8 return rows (U400/U401, WHT-*, CN7)\", \"rows\": [{\"connector\": \"CN7-P9\", \"ic\": \"U400\", \"row\": 1, \"wire\": \"WHT-BRN\"}, {\"connector\": \"CN7-P8\", \"ic\": \"U400\", \"row\": 2, \"wire\": \"WHT-RED\"}, {\"connector\": \"CN7-P7\", \"ic\": \"U400\", \"row\": 3, \"wire\": \"WHT-ORG\"}, {\"connector\": \"CN7-P6\", \"ic\": \"U400\", \"row\": 4, \"wire\": \"WHT-YEL\"}, {\"connector\": \"CN7-P5\", \"ic\": \"U401\", \"row\": 5, \"wire\": \"WHT-GRN\"}, {\"connector\": \"CN7-P3\", \"ic\": \"U401\", \"row\": 6, \"wire\": \"WHT-BLU\"}, {\"connector\": \"CN7-P2\", \"ic\": \"U401\", \"row\": 7, \"wire\": \"WHT-VIO\"}, {\"connector\": \"CN7-P1\", \"ic\": \"U401\", \"row\": 8, \"wire\": \"WHT-GRY\"}], \"switches\": [{\"address\": 1, \"edition_scoped\": \"uk\", \"location\": \"Cabinet Side\", \"name\": \"LT BUTTON (UK ONLY)\", \"part\": \"180-5160-00\"}, {\"address\": 2, \"location\": \"Coin Door\", \"name\": \"4TH COIN SLOT\", \"part\": \"180-5204-00\"}, {\"address\": 3, \"location\": \"Coin Door\", \"name\": \"6TH COIN SLOT\", \"note\": \"Future Use\", \"part\": null}, {\"address\": 4, \"location\": \"Coin Door\", \"name\": \"RIGHT COIN SLOT\", \"part\": \"180-5204-00\"}, {\"address\": 5, \"location\": \"Coin Door\", \"name\": \"CENTER COIN SLOT / DBA\", \"part\": \"180-5204-00\"}, {\"address\": 6, \"location\": \"Coin Door\", \"name\": \"LEFT COIN SLOT\", \"part\": \"180-5204-00\"}, {\"address\": 7, \"location\": \"Coin Door\", \"name\": \"5TH COIN SLOT\", \"note\": \"Future Use\", \"part\": null}, {\"address\": 8, \"edition_scoped\": \"uk\", \"location\": \"Cabinet Side\", \"name\": \"RT BUTTON (UK ONLY)\", \"part\": \"180-5160-00\"}, {\"address\": 9, \"dots\": true, \"location\": \"Below P/F\", \"name\": \"LEFT VUK\", \"part\": \"180-5116-01\"}, {\"address\": 10, \"location\": \"Below P/F\", \"name\": \"STANDUP\", \"part\": \"515-6027-08\"}, {\"address\": 11, \"location\": \"Below P/F\", \"name\": \"4-BALL TROUGH #1 (LEFT)\", \"part\": \"180-5119-02\"}, {\"address\": 12, \"location\": \"Below P/F\", \"name\": \"4-BALL TROUGH #2\", \"part\": \"180-5119-02\"}, {\"address\": 13, \"location\": \"Below P/F\", \"name\": \"4-BALL TROUGH #3\", \"part\": \"180-5119-02\"}, {\"address\": 14, \"location\": \"Below P/F\", \"name\": \"4-BALL TROUGH VUK OPTO\", \"note\": \"See Sw. 14 Note: OPTO PC boards used as switches, transmitter 515-0173-00 / receiver 515-0174-00\", \"part\": null}, {\"address\": 15, \"location\": \"Below P/F\", \"name\": \"4-BALL STACKING OPTO\", \"note\": \"See Sw. 15 Note: OPTO PC boards used as switches, transmitter 515-0173-00 / receiver 515-0174-00\", \"part\": null}, {\"address\": 16, \"location\": \"Below P/F\", \"name\": \"SHOOTER LANE\", \"part\": \"180-5157-00\"}, {\"address\": 17, \"location\": \"Above P/F\", \"name\": \"SWORD LOCK HIGH\", \"part\": \"180-5119-02\"}, {\"address\": 18, \"location\": \"Above P/F\", \"name\": \"SWORD LOCK MID\", \"part\": \"180-5119-02\"}, {\"address\": 19, \"location\": \"Above P/F\", \"name\": \"SWORD LOCK LOW\", \"part\": \"180-5119-02\"}, {\"address\": 20, \"location\": \"Below P/F\", \"name\": \"RIGHT ORBIT LOW\", \"part\": \"500-6227-02\"}, {\"address\": 21, \"location\": \"Above P/F\", \"name\": \"RIGHT ORBIT HI\", \"part\": \"180-5190-28\"}, {\"address\": 22, \"location\": \"Above P/F\", \"name\": \"RAIL RAMP EXIT\", \"part\": \"180-5197-00\"}, {\"address\": 23, \"location\": \"Above P/F\", \"name\": \"RIGHT RAMP TARGET\", \"part\": \"515-6027-08\"}, {\"address\": 24, \"location\": \"Above P/F\", \"name\": \"RIGHT RAMP MADE\", \"part\": \"180-5198-00\"}, {\"address\": 25, \"dots\": true, \"location\": \"Above P/F\", \"name\": \"RIGHT RAMP ENTER\", \"part\": \"180-5010-01\"}, {\"address\": 26, \"name\": null, \"state\": \"not_used\"}, {\"address\": 27, \"name\": null, \"state\": \"not_used\"}, {\"address\": 28, \"location\": \"Above P/F\", \"name\": \"BALROG HIT\", \"part\": \"180-5119-00\"}, {\"address\": 29, \"location\": \"Below P/F\", \"name\": \"PALANTIR\", \"part\": \"515-5162-08\"}, {\"address\": 30, \"dots\": true, \"location\": \"Below P/F\", \"name\": \"RIGHT VUK\", \"part\": \"180-5116-01\"}, {\"address\": 31, \"location\": \"Below P/F\", \"name\": \"BALROG OPEN\", \"part\": \"180-5119-02\"}, {\"address\": 32, \"location\": \"Below P/F\", \"name\": \"BALROG CLOSED\", \"part\": \"180-5119-02\"}, {\"address\": 33, \"location\": \"Mini-P/F\", \"name\": \"MINI PF U.L.\", \"part\": \"180-5057-00\"}, {\"address\": 34, \"location\": \"Mini-P/F\", \"name\": \"MINI PF U.R.\", \"part\": \"180-5057-00\"}, {\"address\": 35, \"location\": \"Mini-P/F\", \"name\": \"MINI PF L.L.\", \"part\": \"180-5057-00\"}, {\"address\": 36, \"location\": \"Mini-P/F\", \"name\": \"MINI PF L.R.\", \"part\": \"180-5057-00\"}, {\"address\": 37, \"location\": \"Below P/F\", \"name\": \"LEFT ORBIT LOW\", \"part\": \"500-6227-02\"}, {\"address\": 38, \"location\": \"Below P/F\", \"name\": \"LEFT ORBIT HI\", \"part\": \"500-6227-02\"}, {\"address\": 39, \"location\": \"Below P/F\", \"name\": \"LEFT RAMP ENTER\", \"part\": \"500-6227-02\"}, {\"address\": 40, \"location\": \"Above P/F\", \"name\": \"LEFT RAMP MADE\", \"part\": \"180-5010-01\"}, {\"address\": 41, \"location\": \"Below P/F\", \"name\": \"TOP VUK\", \"note\": \"See Sw. 41 Note: OPTO, transmitter 515-7307-00 / receiver 515-7308-00\", \"part\": null}, {\"address\": 42, \"location\": \"Above P/F\", \"name\": \"INNER LOOP\", \"part\": \"180-5190-28\"}, {\"address\": 43, \"location\": \"Below P/F\", \"name\": \"LEFT TOP LANE\", \"part\": \"500-6227-02\"}, {\"address\": 44, \"location\": \"Below P/F\", \"name\": \"MIDDLE TOP LANE\", \"part\": \"500-6227-02\"}, {\"address\": 45, \"location\": \"Below P/F\", \"name\": \"RIGHT TOP LANE\", \"part\": \"500-6227-02\"}, {\"address\": 46, \"location\": \"Below P/F\", \"name\": \"TOP SAUCER\", \"part\": \"180-5186-00\"}, {\"address\": 47, \"location\": \"Back Panel\", \"name\": \"RING MADE\", \"note\": \"See Sw. 47 Note: OPTO, transmitter 500-6746-00 / receiver 500-6747-00\", \"part\": null}, {\"address\": 48, \"location\": \"Back Panel\", \"name\": \"BACK TROUGH\", \"part\": \"180-5057-00\"}, {\"address\": 49, \"location\": \"Below P/F\", \"name\": \"LEFT BUMPER\", \"part\": \"180-5015-03\"}, {\"address\": 50, \"location\": \"Below P/F\", \"name\": \"RIGHT BUMPER\", \"part\": \"180-5015-03\"}, {\"address\": 51, \"location\": \"Below P/F\", \"name\": \"BOTTOM BUMPER\", \"part\": \"180-5015-03\"}, {\"address\": 52, \"location\": \"Above P/F\", \"name\": \"SPINNER\", \"part\": \"180-5190-28\"}, {\"address\": 53, \"location\": \"Below P/F\", \"name\": \"SPOT RING\", \"part\": \"515-5162-08\"}, {\"address\": 54, \"location\": \"In Cabinet\", \"name\": \"START BUTTON\", \"part\": \"180-5174-00\"}, {\"address\": 55, \"edition_scoped\": \"tournament_kit\", \"location\": \"In Cabinet\", \"name\": \"TOURNAMENT START\", \"part\": \"180-5174-00\"}, {\"address\": 56, \"location\": \"In Cabinet\", \"name\": \"PLUMB BOB TILT\", \"note\": \"See Sw. 56 Note: hanger bracket 535-5319-00 and contact wire 535-7563-01, located in the cabinet\", \"part\": null}, {\"address\": 57, \"location\": \"Below P/F\", \"name\": \"LEFT OUTLANE\", \"part\": \"500-6227-02\"}, {\"address\": 58, \"location\": \"Below P/F\", \"name\": \"LEFT RETURN LANE\", \"part\": \"500-6227-02\"}, {\"address\": 59, \"location\": \"Below P/F\", \"name\": \"LEFT SLINGSHOT\", \"part\": \"180-5054-00 (x2)\"}, {\"address\": 60, \"location\": \"Below P/F\", \"name\": \"RIGHT OUTLANE\", \"part\": \"500-6227-02\"}, {\"address\": 61, \"location\": \"Below P/F\", \"name\": \"RIGHT RETURN LANE\", \"part\": \"500-6227-02\"}, {\"address\": 62, \"location\": \"Below P/F\", \"name\": \"RIGHT SLINGSHOT\", \"part\": \"180-5054-00 (x2)\"}, {\"address\": 63, \"name\": null, \"state\": \"not_used\"}, {\"address\": 64, \"name\": null, \"state\": \"not_used\"}]}, \"version\": 1}"
)
consensus = json.loads(
	"{\"agreement_threshold\":0.025,\"devices\":{\"flasher\":{\"14\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.021273,\"status\":\"validated\",\"x\":0.831754,\"y\":0.79762},\"23\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.008484,\"status\":\"validated\",\"x\":0.142072,\"y\":0.817043},\"25\":{\"agreeing_tables\":[],\"coordinate_origin\":\"computed\",\"derived_from\":[\"vpw-1-6\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.723972,\"y\":0.301436},{\"table\":\"jpsalas-600\",\"x\":0.726342,\"y\":0.298671},{\"table\":\"hanibal-4k\",\"x\":0.579495,\"y\":0.238208}],\"resolution\":\"DR.7 prints '25' three times, once beside each of coils 9, 10 and 11, all marked Red. FLASH: POPS X3 is three physical bulbs at the three pop bumpers, so each table legitimately picked a different one. Placed at the centroid of the three bumper positions with physical.quantity 3.\",\"resolved_by\":\"manual\",\"status\":\"observed\",\"x\":0.706166,\"y\":0.257348},\"26\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.009924,\"status\":\"observed\",\"x\":0.405984,\"y\":0.017749},\"27\":{\"agreeing_tables\":[\"jpsalas-600\"],\"coordinate_origin\":\"computed\",\"derived_from\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.888267,\"y\":0.03249},{\"table\":\"hanibal-4k\",\"x\":0.931488,\"y\":0.074303}],\"resolution\":\"DR.7 states flashers 26 and 27 are on the Back Panel and prints 27 (Clear) at the top right. All three tables place it in that corner but spread x 0.888-0.932 and y 0.033-0.074, just outside the agreement threshold; the per-axis median is taken.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.924182,\"y\":0.048804},\"29\":{\"agreeing_tables\":[\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.867414,\"y\":0.210014},{\"table\":\"hanibal-4k\",\"x\":0.96535,\"y\":0.282254}],\"resolution\":\"DR.7 places 29 (Red) hard against the right playfield edge, level with and slightly above the right pop bumper. JPSalas x=0.9568 y=0.1893 matches; VPW's x=0.867 is too far inboard and Hanibal's y=0.282 sits below the bumper instead of above it.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.95682,\"y\":0.189307},\"30\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"computed\",\"derived_from\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"outliers\":[{\"table\":\"hanibal-4k\",\"x\":0.803046,\"y\":0.568724}],\"resolution\":\"DR.7 places 30 (Clear) on the right rail immediately beside coil 21, Sword Lock Release. All three tables agree on that region within 0.053; the per-axis median is taken.\",\"resolved_by\":\"manual\",\"spread\":0.023371,\"status\":\"observed\",\"x\":0.833041,\"y\":0.568724},\"31\":{\"agreeing_tables\":[\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"resolution\":\"DR.7 places 31 (Clear) at the Destroy The Ring insert. Only JPSalas models it as a positioned flasher; VPW references the same insert in a commented-out DisableLighting p19 call, corroborating the location.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.415316,\"y\":0.388413},\"32\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"resolution\":\"DR.7 places 32 (Clear) at the Balrog, directly above the motor marked 22. VPW's Lbalrogbloom is the only object bound to the Balrog flash in a positioned form.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.418067,\"y\":0.285293}},\"lamp\":{\"1\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002079,\"status\":\"validated\",\"x\":0.054282,\"y\":0.708832},\"10\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.36144,\"y\":0.681136}],\"spread\":0.000568,\"status\":\"observed\",\"x\":0.282988,\"y\":0.641189},\"11\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.349765,\"y\":0.712371}],\"spread\":0.000448,\"status\":\"observed\",\"x\":0.337166,\"y\":0.629499},\"12\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.385921,\"y\":0.740136}],\"spread\":0.000435,\"status\":\"observed\",\"x\":0.395659,\"y\":0.622382},\"13\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.455108,\"y\":0.750791}],\"spread\":0.001017,\"status\":\"observed\",\"x\":0.456285,\"y\":0.619591},\"14\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.524279,\"y\":0.740389}],\"spread\":0.00089,\"status\":\"observed\",\"x\":0.516361,\"y\":0.622964},\"15\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.560638,\"y\":0.711771}],\"spread\":0.00064,\"status\":\"observed\",\"x\":0.574852,\"y\":0.629723},\"16\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.547309,\"y\":0.68107}],\"spread\":0.000781,\"status\":\"observed\",\"x\":0.628643,\"y\":0.641964},\"17\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.491249,\"y\":0.6606}],\"spread\":0.000889,\"status\":\"observed\",\"x\":0.677071,\"y\":0.657582},\"18\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000905,\"status\":\"validated\",\"x\":0.166477,\"y\":0.580704},\"19\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003265,\"status\":\"validated\",\"x\":0.413997,\"y\":0.391071},\"2\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001311,\"status\":\"validated\",\"x\":0.135217,\"y\":0.685034},\"20\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002065,\"status\":\"validated\",\"x\":0.411636,\"y\":0.466792},\"21\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001066,\"status\":\"validated\",\"x\":0.413272,\"y\":0.546256},\"22\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002613,\"status\":\"validated\",\"x\":0.513082,\"y\":0.417116},\"23\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.00929,\"status\":\"validated\",\"x\":0.544765,\"y\":0.371466},\"24\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002451,\"status\":\"validated\",\"x\":0.722807,\"y\":0.584723},\"25\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003687,\"status\":\"validated\",\"x\":0.12684,\"y\":0.403973},\"26\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003948,\"status\":\"validated\",\"x\":0.170826,\"y\":0.452863},\"27\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002778,\"status\":\"validated\",\"x\":0.231177,\"y\":0.495727},\"28\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002858,\"status\":\"validated\",\"x\":0.269301,\"y\":0.509581},\"29\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002002,\"status\":\"validated\",\"x\":0.259448,\"y\":0.530363},\"3\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002006,\"status\":\"validated\",\"x\":0.775315,\"y\":0.685387},\"30\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002873,\"status\":\"validated\",\"x\":0.21573,\"y\":0.537401},\"31\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002053,\"status\":\"validated\",\"x\":0.178703,\"y\":0.523738},\"32\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001724,\"status\":\"validated\",\"x\":0.187751,\"y\":0.502906},\"33\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002413,\"status\":\"validated\",\"x\":0.188552,\"y\":0.318561},\"34\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002207,\"status\":\"validated\",\"x\":0.207459,\"y\":0.353995},\"35\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002552,\"status\":\"validated\",\"x\":0.226695,\"y\":0.389621},\"36\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.00142,\"status\":\"validated\",\"x\":0.247113,\"y\":0.425458},\"37\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000656,\"status\":\"validated\",\"x\":0.286897,\"y\":0.260064},\"38\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001442,\"status\":\"validated\",\"x\":0.291631,\"y\":0.296945},\"39\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002175,\"status\":\"validated\",\"x\":0.297073,\"y\":0.334533},\"4\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001414,\"status\":\"validated\",\"x\":0.855173,\"y\":0.71114},\"40\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001679,\"status\":\"validated\",\"x\":0.30331,\"y\":0.370874},\"41\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000684,\"status\":\"validated\",\"x\":0.596238,\"y\":0.409949},\"42\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001116,\"status\":\"validated\",\"x\":0.564601,\"y\":0.458126},\"43\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000921,\"status\":\"validated\",\"x\":0.540731,\"y\":0.49391},\"44\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001733,\"status\":\"validated\",\"x\":0.517869,\"y\":0.528787},\"45\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001967,\"status\":\"validated\",\"x\":0.834968,\"y\":0.411127},\"46\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001789,\"status\":\"validated\",\"x\":0.805226,\"y\":0.447606},\"47\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001514,\"status\":\"validated\",\"x\":0.776707,\"y\":0.48183},\"48\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001582,\"status\":\"validated\",\"x\":0.747978,\"y\":0.51698},\"49\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004247,\"status\":\"validated\",\"x\":0.678204,\"y\":0.456279},\"5\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.006166,\"status\":\"validated\",\"x\":0.340849,\"y\":0.766212},\"50\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001989,\"status\":\"validated\",\"x\":0.649554,\"y\":0.48979},\"51\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001919,\"status\":\"validated\",\"x\":0.620589,\"y\":0.524135},\"52\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.00102,\"status\":\"validated\",\"x\":0.592093,\"y\":0.558496},\"53\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003074,\"status\":\"validated\",\"x\":0.567542,\"y\":0.589911},\"54\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002107,\"status\":\"validated\",\"x\":0.943881,\"y\":0.465284},\"55\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001988,\"status\":\"validated\",\"x\":0.943934,\"y\":0.510504},\"56\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001794,\"status\":\"validated\",\"x\":0.94417,\"y\":0.555578},\"57\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003315,\"status\":\"validated\",\"x\":0.607802,\"y\":0.124201},\"58\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003242,\"status\":\"validated\",\"x\":0.697426,\"y\":0.124201},\"59\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003317,\"status\":\"validated\",\"x\":0.784131,\"y\":0.124201},\"6\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.457294,\"y\":0.78258}],\"spread\":0.001436,\"status\":\"observed\",\"x\":0.457336,\"y\":0.756793},\"60\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.015511,\"status\":\"validated\",\"x\":0.087224,\"y\":0.049677},\"61\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.014251,\"status\":\"validated\",\"x\":0.175933,\"y\":0.049677},\"62\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.014269,\"status\":\"validated\",\"x\":0.087198,\"y\":0.049677},\"63\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.014384,\"status\":\"validated\",\"x\":0.175933,\"y\":0.049677},\"64\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000997,\"status\":\"validated\",\"x\":0.897584,\"y\":0.796143},\"65\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001608,\"status\":\"validated\",\"x\":0.898567,\"y\":0.758766},\"66\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001118,\"status\":\"validated\",\"x\":0.898567,\"y\":0.713651},\"67\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001419,\"status\":\"validated\",\"x\":0.898634,\"y\":0.667902},\"68\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001066,\"status\":\"validated\",\"x\":0.898619,\"y\":0.623188},\"69\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001599,\"status\":\"validated\",\"x\":0.899136,\"y\":0.57784},\"7\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.005407,\"status\":\"validated\",\"x\":0.572164,\"y\":0.766347},\"70\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0013,\"status\":\"validated\",\"x\":0.899072,\"y\":0.533289},\"71\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001593,\"status\":\"validated\",\"x\":0.899096,\"y\":0.488204},\"72\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002737,\"status\":\"validated\",\"x\":0.886969,\"y\":0.443901},\"73\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004739,\"status\":\"validated\",\"x\":0.302283,\"y\":0.040853},\"74\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004235,\"status\":\"validated\",\"x\":0.33666,\"y\":0.040853},\"75\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004059,\"status\":\"validated\",\"x\":0.381901,\"y\":0.040853},\"76\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004015,\"status\":\"validated\",\"x\":0.430837,\"y\":0.040853},\"77\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.007274,\"status\":\"validated\",\"x\":0.477608,\"y\":0.040853},\"78\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.010432,\"status\":\"validated\",\"x\":0.51302,\"y\":0.040853},\"79\":{\"agreeing_tables\":[\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.80321,\"y\":0.595693},\"8\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001189,\"status\":\"validated\",\"x\":0.45591,\"y\":0.85778},\"80\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.144598,\"y\":0.920488},\"81\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.501064,\"y\":0.815109},\"82\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.475148,\"y\":0.825744},\"83\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.507861,\"y\":0.799613},\"84\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.409614,\"y\":0.815477},\"85\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.437016,\"y\":0.825506},\"86\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.456657,\"y\":0.790295},\"87\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.489487,\"y\":0.786018},\"88\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.455778,\"y\":0.78056},\"89\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.422566,\"y\":0.785884},\"9\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.42068,\"y\":0.660898}],\"spread\":0.000494,\"status\":\"observed\",\"x\":0.234827,\"y\":0.657463},\"90\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.403505,\"y\":0.799639},\"91\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.425156,\"y\":0.806937},\"92\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.442218,\"y\":0.815812},\"93\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.47031,\"y\":0.815803},\"94\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.486578,\"y\":0.806906},\"95\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.479608,\"y\":0.795327},\"96\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.464379,\"y\":0.805762},\"97\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.448215,\"y\":0.805314},\"98\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.455899,\"y\":0.799794},\"99\":{\"agreeing_tables\":[\"neo-led-1-0-3\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.431818,\"y\":0.795345}},\"switch\":{\"1\":{\"status\":\"missing\"},\"10\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002363,\"status\":\"validated\",\"x\":0.070903,\"y\":0.500457},\"11\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.646125,\"y\":0.933046},\"12\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.719888,\"y\":0.91045},\"13\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.79085,\"y\":0.889872},\"14\":{\"agreeing_tables\":[\"vpw-1-6\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.858076,\"y\":0.871312},\"15\":{\"status\":\"missing\"},\"16\":{\"agreeing_tables\":[\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0,\"status\":\"observed\",\"x\":0.945378,\"y\":0.935075},\"17\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"hanibal-4k\",\"x\":0.87655,\"y\":0.542045}],\"spread\":0.001565,\"status\":\"observed\",\"x\":0.847583,\"y\":0.544277},\"18\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.021976,\"status\":\"validated\",\"x\":0.837819,\"y\":0.567522},\"19\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.008406,\"status\":\"validated\",\"x\":0.827823,\"y\":0.595782},\"2\":{\"status\":\"missing\"},\"20\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001734,\"status\":\"validated\",\"x\":0.900604,\"y\":0.352177},\"21\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.008811,\"status\":\"validated\",\"x\":0.893645,\"y\":0.152949},\"22\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.748935,\"y\":0.371031}],\"spread\":0.007358,\"status\":\"observed\",\"x\":0.696002,\"y\":0.37818},\"23\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004829,\"status\":\"validated\",\"x\":0.923845,\"y\":0.193862},\"24\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"hanibal-4k\",\"x\":0.897131,\"y\":0.255224}],\"spread\":0.008283,\"status\":\"observed\",\"x\":0.947066,\"y\":0.287156},\"25\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.750671,\"y\":0.376326}],\"spread\":0.005261,\"status\":\"observed\",\"x\":0.789673,\"y\":0.348579},\"26\":{\"status\":\"missing\"},\"27\":{\"status\":\"missing\"},\"28\":{\"agreeing_tables\":[\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"hanibal-4k\",\"x\":0.438999,\"y\":0.26571}],\"resolution\":\"DR.4 prints 28 Balrog Hit as an above-playfield switch on the Balrog itself. JPSalas x=0.5105 sits on the Balrog assembly, which VPW independently models at x=0.5078; Hanibal's x=0.4390 is off the toy.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.510504,\"y\":0.273516},\"29\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003046,\"status\":\"validated\",\"x\":0.537743,\"y\":0.385227},\"3\":{\"status\":\"missing\"},\"30\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004517,\"status\":\"validated\",\"x\":0.640284,\"y\":0.354792},\"31\":{\"status\":\"missing\"},\"32\":{\"status\":\"missing\"},\"33\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.005632,\"status\":\"validated\",\"x\":0.031946,\"y\":0.159037},\"34\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.018243,\"status\":\"validated\",\"x\":0.112387,\"y\":0.159037},\"35\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.008149,\"status\":\"validated\",\"x\":0.026552,\"y\":0.233488},\"36\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.01716,\"status\":\"validated\",\"x\":0.112387,\"y\":0.240628},\"37\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.020707,\"status\":\"validated\",\"x\":0.056071,\"y\":0.233374},\"38\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002471,\"status\":\"validated\",\"x\":0.057435,\"y\":0.122519},\"39\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004376,\"status\":\"validated\",\"x\":0.124161,\"y\":0.155979},\"4\":{\"status\":\"missing\"},\"40\":{\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.197266,\"y\":0.255998}],\"spread\":0.007749,\"status\":\"observed\",\"x\":0.18085,\"y\":0.290358},\"41\":{\"agreeing_tables\":[\"jpsalas-600\"],\"coordinate_origin\":\"computed\",\"derived_from\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.266002,\"y\":0.08251},{\"table\":\"hanibal-4k\",\"x\":0.182107,\"y\":0.077028}],\"resolution\":\"All three tables agree on y within 0.008 but spread x from 0.182 to 0.266 for the Top VUK. DR.4 places 41 in the upper-left; the per-axis median is taken.\",\"resolved_by\":\"manual\",\"spread\":0.0,\"status\":\"observed\",\"x\":0.209926,\"y\":0.078018},\"42\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.015983,\"status\":\"validated\",\"x\":0.510731,\"y\":0.123656},\"43\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001107,\"status\":\"validated\",\"x\":0.607895,\"y\":0.164392},\"44\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001019,\"status\":\"validated\",\"x\":0.698637,\"y\":0.16422},\"45\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001573,\"status\":\"validated\",\"x\":0.784795,\"y\":0.164878},\"46\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.00314,\"status\":\"validated\",\"x\":0.762881,\"y\":0.055152},\"47\":{\"agreeing_tables\":[\"vpw-1-6\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[{\"table\":\"jpsalas-600\",\"x\":0.406181,\"y\":0.033753}],\"spread\":0.000669,\"status\":\"observed\",\"x\":0.415704,\"y\":0.003215},\"48\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.024608,\"status\":\"validated\",\"x\":0.56677,\"y\":0.014928},\"49\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001024,\"status\":\"observed\",\"x\":0.579876,\"y\":0.236667},\"5\":{\"status\":\"missing\"},\"50\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.000706,\"status\":\"observed\",\"x\":0.814447,\"y\":0.232368},\"51\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.0011,\"status\":\"observed\",\"x\":0.72469,\"y\":0.300211},\"52\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003468,\"status\":\"validated\",\"x\":0.413729,\"y\":0.239164},\"53\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.005932,\"status\":\"validated\",\"x\":0.805672,\"y\":0.559372},\"54\":{\"status\":\"missing\"},\"55\":{\"status\":\"missing\"},\"56\":{\"status\":\"missing\"},\"57\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.001515,\"status\":\"validated\",\"x\":0.057455,\"y\":0.765311},\"58\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003658,\"status\":\"validated\",\"x\":0.132933,\"y\":0.748095},\"59\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.004281,\"status\":\"validated\",\"x\":0.230748,\"y\":0.738155},\"6\":{\"status\":\"missing\"},\"60\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.006373,\"status\":\"validated\",\"x\":0.854087,\"y\":0.766886},\"61\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.003735,\"status\":\"validated\",\"x\":0.778361,\"y\":0.748486},\"62\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.00561,\"status\":\"validated\",\"x\":0.67974,\"y\":0.737213},\"63\":{\"status\":\"missing\"},\"64\":{\"status\":\"missing\"},\"7\":{\"status\":\"missing\"},\"8\":{\"status\":\"missing\"},\"9\":{\"agreeing_tables\":[\"vpw-1-6\",\"jpsalas-600\",\"hanibal-4k\"],\"coordinate_origin\":\"table\",\"outliers\":[],\"spread\":0.002982,\"status\":\"validated\",\"x\":0.070734,\"y\":0.606124}}},\"tables\":{\"hanibal-4k\":{\"bounds\":[0.0,952.0,0.0,2139.0],\"role\":\"factory-playfield-consensus\"},\"jpsalas-600\":{\"bounds\":[0.0,952.0,0.0,2190.0],\"role\":\"factory-playfield-consensus\"},\"neo-led-1-0-3\":{\"bounds\":[0.0,952.0,0.0,2190.0],\"role\":\"led-board-emitters-81-99-only\"},\"vpw-1-6\":{\"bounds\":[0.0,952.0,0.0,2203.0],\"role\":\"factory-playfield-consensus\"}}}"
)
# The full base consensus remains embedded above. Lamps 81-99 are overlaid separately so their
# script-derived bindings stay reviewable without replacing the otherwise unchanged large literal.
# tools/lotr_spatial_resolve.py and the retained external consensus remain the derivation authority;
# the evidence-backed tests require this resulting object to be byte-for-byte equivalent.
_LED_CONSENSUS = json.loads(
	"{\"lamps81_99\":{\"81\":{\"status\":\"observed\",\"x\":0.501301,\"y\":0.815444,\"spread\":0.000335,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.488632,\"y\":0.686322},{\"table\":\"jpsalas-600\",\"x\":0.48939,\"y\":0.786461}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l81\",\"bound_objects\":[\"l81\",\"l81a\"],\"script_lines\":[2144,2145],\"x\":0.488632,\"y\":0.686322},{\"table\":\"jpsalas-600\",\"object\":\"l81\",\"bound_objects\":[\"l81\"],\"script_lines\":[722],\"x\":0.48939,\"y\":0.786461},{\"table\":\"hanibal-4k\",\"object\":\"l98\",\"bound_objects\":[\"l98\",\"l98a\"],\"script_lines\":[1454,1455],\"x\":0.501538,\"y\":0.815779},{\"table\":\"neo-led-1-0-3\",\"object\":\"l81\",\"bound_objects\":[\"l81\"],\"script_lines\":[602],\"x\":0.501064,\"y\":0.815109}],\"coordinate_origin\":\"table\"},\"82\":{\"status\":\"observed\",\"x\":0.474855,\"y\":0.825705,\"spread\":0.000294,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.506653,\"y\":0.699977},{\"table\":\"jpsalas-600\",\"x\":0.507764,\"y\":0.800225}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l82\",\"bound_objects\":[\"l82\",\"l82a\"],\"script_lines\":[2146,2147],\"x\":0.506653,\"y\":0.699977},{\"table\":\"jpsalas-600\",\"object\":\"l82\",\"bound_objects\":[\"l82\"],\"script_lines\":[723],\"x\":0.507764,\"y\":0.800225},{\"table\":\"hanibal-4k\",\"object\":\"l97\",\"bound_objects\":[\"l97\",\"l97a\"],\"script_lines\":[1456,1457],\"x\":0.474561,\"y\":0.825666},{\"table\":\"neo-led-1-0-3\",\"object\":\"l82\",\"bound_objects\":[\"l82\"],\"script_lines\":[603],\"x\":0.475148,\"y\":0.825744}],\"coordinate_origin\":\"table\"},\"83\":{\"status\":\"observed\",\"x\":0.504459,\"y\":0.807495,\"spread\":0.007883,\"agreeing_tables\":[\"jpsalas-600\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.499783,\"y\":0.715932},{\"table\":\"hanibal-4k\",\"x\":0.43731,\"y\":0.825853}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l83\",\"bound_objects\":[\"l83\",\"l83a\"],\"script_lines\":[2148,2149],\"x\":0.499783,\"y\":0.715932},{\"table\":\"jpsalas-600\",\"object\":\"l83\",\"bound_objects\":[\"l83\"],\"script_lines\":[724],\"x\":0.501058,\"y\":0.815378},{\"table\":\"hanibal-4k\",\"object\":\"l96\",\"bound_objects\":[\"l96\",\"l96a\"],\"script_lines\":[1458,1459],\"x\":0.43731,\"y\":0.825853},{\"table\":\"neo-led-1-0-3\",\"object\":\"l83\",\"bound_objects\":[\"l83\"],\"script_lines\":[604],\"x\":0.507861,\"y\":0.799613}],\"coordinate_origin\":\"table\"},\"84\":{\"status\":\"observed\",\"x\":0.409784,\"y\":0.815518,\"spread\":0.00017,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.47307,\"y\":0.725716},{\"table\":\"jpsalas-600\",\"x\":0.474419,\"y\":0.826103}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l84\",\"bound_objects\":[\"l84\",\"l84a\"],\"script_lines\":[2150,2151],\"x\":0.47307,\"y\":0.725716},{\"table\":\"jpsalas-600\",\"object\":\"l84\",\"bound_objects\":[\"l84\"],\"script_lines\":[725],\"x\":0.474419,\"y\":0.826103},{\"table\":\"hanibal-4k\",\"object\":\"l95\",\"bound_objects\":[\"l95\",\"l95a\"],\"script_lines\":[1460,1461],\"x\":0.409953,\"y\":0.815559},{\"table\":\"neo-led-1-0-3\",\"object\":\"l84\",\"bound_objects\":[\"l84\"],\"script_lines\":[605],\"x\":0.409614,\"y\":0.815477}],\"coordinate_origin\":\"table\"},\"85\":{\"status\":\"observed\",\"x\":0.436766,\"y\":0.825727,\"spread\":0.00025,\"agreeing_tables\":[\"jpsalas-600\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.436113,\"y\":0.726021},{\"table\":\"hanibal-4k\",\"x\":0.405078,\"y\":0.800693}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l85\",\"bound_objects\":[\"l85\",\"l85a\"],\"script_lines\":[2152,2153],\"x\":0.436113,\"y\":0.726021},{\"table\":\"jpsalas-600\",\"object\":\"l85\",\"bound_objects\":[\"l85\"],\"script_lines\":[726],\"x\":0.436516,\"y\":0.825948},{\"table\":\"hanibal-4k\",\"object\":\"l94\",\"bound_objects\":[\"l94\",\"l94a\"],\"script_lines\":[1462,1463],\"x\":0.405078,\"y\":0.800693},{\"table\":\"neo-led-1-0-3\",\"object\":\"l85\",\"bound_objects\":[\"l85\"],\"script_lines\":[606],\"x\":0.437016,\"y\":0.825506}],\"coordinate_origin\":\"table\"},\"86\":{\"status\":\"conflicted\",\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l86\",\"bound_objects\":[\"l86\",\"l86a\"],\"script_lines\":[2154,2155],\"x\":0.409096,\"y\":0.71585},{\"table\":\"jpsalas-600\",\"object\":\"l86\",\"bound_objects\":[\"l86\"],\"script_lines\":[727],\"x\":0.409015,\"y\":0.815712},{\"table\":\"hanibal-4k\",\"object\":\"l93\",\"bound_objects\":[\"l93\",\"l93a\"],\"script_lines\":[1464,1465],\"x\":0.421315,\"y\":0.786423},{\"table\":\"neo-led-1-0-3\",\"object\":\"l86\",\"bound_objects\":[\"l86\"],\"script_lines\":[607],\"x\":0.456657,\"y\":0.790295}]},\"87\":{\"status\":\"conflicted\",\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l87\",\"bound_objects\":[\"l87\",\"l87a\"],\"script_lines\":[2156,2157],\"x\":0.403389,\"y\":0.700653},{\"table\":\"jpsalas-600\",\"object\":\"l87\",\"bound_objects\":[\"l87\"],\"script_lines\":[728],\"x\":0.402612,\"y\":0.800014},{\"table\":\"hanibal-4k\",\"object\":\"l92\",\"bound_objects\":[\"l92\",\"l92a\"],\"script_lines\":[1466,1467],\"x\":0.455449,\"y\":0.781288},{\"table\":\"neo-led-1-0-3\",\"object\":\"l87\",\"bound_objects\":[\"l87\"],\"script_lines\":[608],\"x\":0.489487,\"y\":0.786018}]},\"88\":{\"status\":\"conflicted\",\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l88\",\"bound_objects\":[\"l88\",\"l88a\"],\"script_lines\":[2158,2159],\"x\":0.420021,\"y\":0.686594},{\"table\":\"jpsalas-600\",\"object\":\"l88\",\"bound_objects\":[\"l88\"],\"script_lines\":[729],\"x\":0.421907,\"y\":0.786297},{\"table\":\"hanibal-4k\",\"object\":\"l91\",\"bound_objects\":[\"l91\",\"l91a\"],\"script_lines\":[1468,1469],\"x\":0.489667,\"y\":0.786201},{\"table\":\"neo-led-1-0-3\",\"object\":\"l88\",\"bound_objects\":[\"l88\"],\"script_lines\":[609],\"x\":0.455778,\"y\":0.78056}]},\"89\":{\"status\":\"conflicted\",\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l89\",\"bound_objects\":[\"l89\",\"l89a\"],\"script_lines\":[2160,2161],\"x\":0.453796,\"y\":0.681586},{\"table\":\"jpsalas-600\",\"object\":\"l89\",\"bound_objects\":[\"l89\"],\"script_lines\":[730],\"x\":0.455341,\"y\":0.781004},{\"table\":\"hanibal-4k\",\"object\":\"l99\",\"bound_objects\":[\"l99\",\"l99a\"],\"script_lines\":[1470,1471],\"x\":0.508042,\"y\":0.800122},{\"table\":\"neo-led-1-0-3\",\"object\":\"l89\",\"bound_objects\":[\"l89\"],\"script_lines\":[610],\"x\":0.422566,\"y\":0.785884}]},\"90\":{\"status\":\"observed\",\"x\":0.475283,\"y\":0.806262,\"spread\":0.01053,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.479395,\"y\":0.695855},{\"table\":\"neo-led-1-0-3\",\"x\":0.403505,\"y\":0.799639}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l90\",\"bound_objects\":[\"l90\",\"l90a\"],\"script_lines\":[2162,2163],\"x\":0.479395,\"y\":0.695855},{\"table\":\"jpsalas-600\",\"object\":\"l90\",\"bound_objects\":[\"l90\"],\"script_lines\":[731],\"x\":0.479754,\"y\":0.795732},{\"table\":\"hanibal-4k\",\"object\":\"l86\",\"bound_objects\":[\"l86\",\"l86a\"],\"script_lines\":[1472,1473],\"x\":0.470812,\"y\":0.816792},{\"table\":\"neo-led-1-0-3\",\"object\":\"l90\",\"bound_objects\":[\"l90\"],\"script_lines\":[611],\"x\":0.403505,\"y\":0.799639}],\"coordinate_origin\":\"table\"},\"91\":{\"status\":\"observed\",\"x\":0.43395,\"y\":0.811678,\"spread\":0.008794,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.484142,\"y\":0.707111},{\"table\":\"jpsalas-600\",\"x\":0.486578,\"y\":0.807416}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l91\",\"bound_objects\":[\"l91\",\"l91a\"],\"script_lines\":[2164,2165],\"x\":0.484142,\"y\":0.707111},{\"table\":\"jpsalas-600\",\"object\":\"l91\",\"bound_objects\":[\"l91\"],\"script_lines\":[732],\"x\":0.486578,\"y\":0.807416},{\"table\":\"hanibal-4k\",\"object\":\"l87\",\"bound_objects\":[\"l87\",\"l87a\"],\"script_lines\":[1474,1475],\"x\":0.442744,\"y\":0.816419},{\"table\":\"neo-led-1-0-3\",\"object\":\"l91\",\"bound_objects\":[\"l91\"],\"script_lines\":[612],\"x\":0.425156,\"y\":0.806937}],\"coordinate_origin\":\"table\"},\"92\":{\"status\":\"observed\",\"x\":0.432957,\"y\":0.811447,\"spread\":0.009261,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.469286,\"y\":0.717029},{\"table\":\"jpsalas-600\",\"x\":0.469454,\"y\":0.816266}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l92\",\"bound_objects\":[\"l92\",\"l92a\"],\"script_lines\":[2166,2167],\"x\":0.469286,\"y\":0.717029},{\"table\":\"jpsalas-600\",\"object\":\"l92\",\"bound_objects\":[\"l92\"],\"script_lines\":[733],\"x\":0.469454,\"y\":0.816266},{\"table\":\"hanibal-4k\",\"object\":\"l88\",\"bound_objects\":[\"l88\",\"l88a\"],\"script_lines\":[1476,1477],\"x\":0.423696,\"y\":0.807083},{\"table\":\"neo-led-1-0-3\",\"object\":\"l92\",\"bound_objects\":[\"l92\"],\"script_lines\":[613],\"x\":0.442218,\"y\":0.815812}],\"coordinate_origin\":\"table\"},\"93\":{\"status\":\"observed\",\"x\":0.437344,\"y\":0.806058,\"spread\":0.010096,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.442199,\"y\":0.71666},{\"table\":\"neo-led-1-0-3\",\"x\":0.47031,\"y\":0.815803}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l93\",\"bound_objects\":[\"l93\",\"l93a\"],\"script_lines\":[2168,2169],\"x\":0.442199,\"y\":0.71666},{\"table\":\"jpsalas-600\",\"object\":\"l93\",\"bound_objects\":[\"l93\"],\"script_lines\":[734],\"x\":0.441823,\"y\":0.816153},{\"table\":\"hanibal-4k\",\"object\":\"l89\",\"bound_objects\":[\"l89\",\"l89a\"],\"script_lines\":[1478,1479],\"x\":0.432865,\"y\":0.795962},{\"table\":\"neo-led-1-0-3\",\"object\":\"l93\",\"bound_objects\":[\"l93\"],\"script_lines\":[614],\"x\":0.47031,\"y\":0.815803}],\"coordinate_origin\":\"table\"},\"94\":{\"status\":\"conflicted\",\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l94\",\"bound_objects\":[\"l94\",\"l94a\"],\"script_lines\":[2170,2171],\"x\":0.422588,\"y\":0.707148},{\"table\":\"jpsalas-600\",\"object\":\"l94\",\"bound_objects\":[\"l94\"],\"script_lines\":[735],\"x\":0.424689,\"y\":0.807308},{\"table\":\"hanibal-4k\",\"object\":\"l90\",\"bound_objects\":[\"l90\",\"l90a\"],\"script_lines\":[1480,1481],\"x\":0.455431,\"y\":0.790841},{\"table\":\"neo-led-1-0-3\",\"object\":\"l94\",\"bound_objects\":[\"l94\"],\"script_lines\":[615],\"x\":0.486578,\"y\":0.806906}]},\"95\":{\"status\":\"observed\",\"x\":0.48018,\"y\":0.795528,\"spread\":0.000572,\"agreeing_tables\":[\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.431722,\"y\":0.695757},{\"table\":\"jpsalas-600\",\"x\":0.431279,\"y\":0.795787}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l95\",\"bound_objects\":[\"l95\",\"l95a\"],\"script_lines\":[2172,2173],\"x\":0.431722,\"y\":0.695757},{\"table\":\"jpsalas-600\",\"object\":\"l95\",\"bound_objects\":[\"l95\"],\"script_lines\":[736],\"x\":0.431279,\"y\":0.795787},{\"table\":\"hanibal-4k\",\"object\":\"l84\",\"bound_objects\":[\"l84\",\"l84a\"],\"script_lines\":[1482,1483],\"x\":0.480751,\"y\":0.795728},{\"table\":\"neo-led-1-0-3\",\"object\":\"l95\",\"bound_objects\":[\"l95\"],\"script_lines\":[616],\"x\":0.479608,\"y\":0.795327}],\"coordinate_origin\":\"table\"},\"96\":{\"status\":\"observed\",\"x\":0.464379,\"y\":0.805762,\"spread\":0.020898,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.454549,\"y\":0.691039}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l96\",\"bound_objects\":[\"l96\",\"l96a\"],\"script_lines\":[2174,2175],\"x\":0.454549,\"y\":0.691039},{\"table\":\"jpsalas-600\",\"object\":\"l96\",\"bound_objects\":[\"l96\"],\"script_lines\":[737],\"x\":0.456366,\"y\":0.790679},{\"table\":\"hanibal-4k\",\"object\":\"l85\",\"bound_objects\":[\"l85\",\"l85a\"],\"script_lines\":[1484,1485],\"x\":0.485277,\"y\":0.806827},{\"table\":\"neo-led-1-0-3\",\"object\":\"l96\",\"bound_objects\":[\"l96\"],\"script_lines\":[617],\"x\":0.464379,\"y\":0.805762}],\"coordinate_origin\":\"table\"},\"97\":{\"status\":\"observed\",\"x\":0.448215,\"y\":0.805314,\"spread\":0.007578,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.465698,\"y\":0.706148}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l97\",\"bound_objects\":[\"l97\",\"l97a\"],\"script_lines\":[2176,2177],\"x\":0.465698,\"y\":0.706148},{\"table\":\"jpsalas-600\",\"object\":\"l97\",\"bound_objects\":[\"l97\"],\"script_lines\":[738],\"x\":0.455793,\"y\":0.800132},{\"table\":\"hanibal-4k\",\"object\":\"l82\",\"bound_objects\":[\"l82\",\"l82a\"],\"script_lines\":[1486,1487],\"x\":0.44723,\"y\":0.805563},{\"table\":\"neo-led-1-0-3\",\"object\":\"l97\",\"bound_objects\":[\"l97\"],\"script_lines\":[618],\"x\":0.448215,\"y\":0.805314}],\"coordinate_origin\":\"table\"},\"98\":{\"status\":\"observed\",\"x\":0.456263,\"y\":0.800532,\"spread\":0.008074,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.446636,\"y\":0.705504}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l98\",\"bound_objects\":[\"l98\",\"l98a\"],\"script_lines\":[2178,2179],\"x\":0.446636,\"y\":0.705504},{\"table\":\"jpsalas-600\",\"object\":\"l98\",\"bound_objects\":[\"l98\"],\"script_lines\":[739],\"x\":0.464337,\"y\":0.805965},{\"table\":\"hanibal-4k\",\"object\":\"l81\",\"bound_objects\":[\"l81\",\"l81a\"],\"script_lines\":[1488,1489],\"x\":0.456263,\"y\":0.800532},{\"table\":\"neo-led-1-0-3\",\"object\":\"l98\",\"bound_objects\":[\"l98\"],\"script_lines\":[619],\"x\":0.455899,\"y\":0.799794}],\"coordinate_origin\":\"table\"},\"99\":{\"status\":\"observed\",\"x\":0.448112,\"y\":0.805675,\"spread\":0.01834,\"agreeing_tables\":[\"jpsalas-600\",\"hanibal-4k\",\"neo-led-1-0-3\"],\"outliers\":[{\"table\":\"vpw-1-6\",\"x\":0.455128,\"y\":0.70029}],\"script_bound_measurements\":[{\"table\":\"vpw-1-6\",\"object\":\"l99\",\"bound_objects\":[\"l99\",\"l99a\"],\"script_lines\":[2180,2181],\"x\":0.455128,\"y\":0.70029},{\"table\":\"jpsalas-600\",\"object\":\"l99\",\"bound_objects\":[\"l99\"],\"script_lines\":[740],\"x\":0.448112,\"y\":0.805675},{\"table\":\"hanibal-4k\",\"object\":\"l83\",\"bound_objects\":[\"l83\",\"l83a\"],\"script_lines\":[1490,1491],\"x\":0.466452,\"y\":0.806206},{\"table\":\"neo-led-1-0-3\",\"object\":\"l99\",\"bound_objects\":[\"l99\"],\"script_lines\":[620],\"x\":0.431818,\"y\":0.795345}],\"coordinate_origin\":\"table\"}},\"neo_table\":{\"bounds\":[0.0,952.0,0.0,2190.0],\"role\":\"supplemental-derivative-led-measurement\"}}"
)
consensus["devices"]["lamp"].update(_LED_CONSENSUS["lamps81_99"])
consensus["tables"]["neo-led-1-0-3"] = _LED_CONSENSUS["neo_table"]
# Keep the two small post-review resolver changes explicit instead of replacing the otherwise
# unchanged large embedded base literal. Evidence-backed tests require the resulting full object
# to equal the retained external derivation byte-for-byte.
consensus["devices"]["flasher"]["25"] = json.loads(
    '{"status":"validated","quantity":3,"emitters":{"left":{"status":"validated","x":0.579541,"y":0.237587,"spread":0.002795,"agreeing_tables":["vpw-1-6","jpsalas-600","hanibal-4k"],"outliers":[],"measurements":[{"table":"vpw-1-6","object":"Flasherbase1","bound_objects":["Flasherbase1"],"script_lines":[622,1531,1744,1745,2211],"x":0.579541,"y":0.237587},{"table":"jpsalas-600","object":"f25a001","bound_objects":["f25a001","f25c001"],"script_lines":[382,386,396],"x":0.5814,"y":0.235413},{"table":"hanibal-4k","object":"f25b","bound_objects":["f25b","f25e"],"script_lines":[401,1496,1499],"x":0.579495,"y":0.238208}]},"right":{"status":"validated","x":0.815658,"y":0.231756,"spread":0.003172,"agreeing_tables":["vpw-1-6","jpsalas-600","hanibal-4k"],"outliers":[],"measurements":[{"table":"vpw-1-6","object":"Flasherbase3","bound_objects":["Flasherbase3"],"script_lines":[622,1531,1744,1747,2211],"x":0.814299,"y":0.232872},{"table":"jpsalas-600","object":"f25a002","bound_objects":["f25a002","f25c002"],"script_lines":[383,387,396],"x":0.815658,"y":0.23121},{"table":"hanibal-4k","object":"F25a","bound_objects":["F25a","f25f"],"script_lines":[401,1495,1500],"x":0.817471,"y":0.231756}]},"bottom":{"status":"validated","x":0.723972,"y":0.300923,"spread":0.001222,"agreeing_tables":["vpw-1-6","jpsalas-600","hanibal-4k"],"outliers":[],"measurements":[{"table":"vpw-1-6","object":"Flasherbase2","bound_objects":["Flasherbase2"],"script_lines":[622,1531,1744,1746,2211],"x":0.723972,"y":0.301436},{"table":"jpsalas-600","object":"f25a3","bound_objects":["f25a3","f25c"],"script_lines":[384,385,396],"x":0.722852,"y":0.300356},{"table":"hanibal-4k","object":"f25c","bound_objects":["f25c","f25d"],"script_lines":[401,1497,1498],"x":0.724074,"y":0.300923}]}},"resolution":"The public output drives three physical bulbs. Every retained factory-layout script binds all three, grouped here by co-located left, right and bottom emitter objects before consensus."}'
)
consensus["devices"]["switch"]["28"]["resolution"] = (
    "DR.4 prints 28 Balrog Hit as an above-playfield switch on the Balrog itself. JPSalas x=0.5105 "
    "sits on the Balrog assembly shown in the printed location drawing; Hanibal's x=0.4390 is off "
    "the toy. VPW has no bound sw28 object and contributes no switch-28 measurement."
)

partial = json.loads(
	"{\"drivers\": [{\"description\": \"Lord of the Rings, The (10.00)\", \"flags\": 0, \"id\": \"lotr\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (3.00)\", \"flags\": 0, \"id\": \"lotr3\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.01)\", \"flags\": 0, \"id\": \"lotr4\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.10)\", \"flags\": 0, \"id\": \"lotr41\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.00)\", \"flags\": 0, \"id\": \"lotr5\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.01)\", \"flags\": 0, \"id\": \"lotr51\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (6.00)\", \"flags\": 0, \"id\": \"lotr6\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (7.00)\", \"flags\": 0, \"id\": \"lotr7\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (8.00)\", \"flags\": 0, \"id\": \"lotr8\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (9.00)\", \"flags\": 0, \"id\": \"lotr9\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.10 French)\", \"flags\": 0, \"id\": \"lotr_f41\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.01 French)\", \"flags\": 0, \"id\": \"lotr_f51\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (10.00 French)\", \"flags\": 0, \"id\": \"lotr_fr\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.01 French)\", \"flags\": 0, \"id\": \"lotr_fr4\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.00 French)\", \"flags\": 0, \"id\": \"lotr_fr5\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (6.00 French)\", \"flags\": 0, \"id\": \"lotr_fr6\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (7.00 French)\", \"flags\": 0, \"id\": \"lotr_fr7\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (8.00 French)\", \"flags\": 0, \"id\": \"lotr_fr8\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (9.00 French)\", \"flags\": 0, \"id\": \"lotr_fr9\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.10 German)\", \"flags\": 0, \"id\": \"lotr_g41\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.01 German)\", \"flags\": 0, \"id\": \"lotr_g51\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (10.00 German)\", \"flags\": 0, \"id\": \"lotr_gr\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.01 German)\", \"flags\": 0, \"id\": \"lotr_gr4\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.00 German)\", \"flags\": 0, \"id\": \"lotr_gr5\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (6.00 German)\", \"flags\": 0, \"id\": \"lotr_gr6\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (7.00 German)\", \"flags\": 0, \"id\": \"lotr_gr7\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (8.00 German)\", \"flags\": 0, \"id\": \"lotr_gr8\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (9.00 German)\", \"flags\": 0, \"id\": \"lotr_gr9\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.10 Italian)\", \"flags\": 0, \"id\": \"lotr_i41\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.01 Italian)\", \"flags\": 0, \"id\": \"lotr_i51\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (10.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.01 Italian)\", \"flags\": 0, \"id\": \"lotr_it4\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it5\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (6.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it6\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (7.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it7\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (8.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it8\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (9.00 Italian)\", \"flags\": 0, \"id\": \"lotr_it9\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (10.02 Limited Edition)\", \"flags\": 0, \"id\": \"lotr_le\", \"manufacturer\": \"Stern\", \"year\": \"2008\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.01 Spanish)\", \"flags\": 0, \"id\": \"lotr_s51\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (10.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (4.01 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp4\", \"manufacturer\": \"Stern\", \"year\": \"2003\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (5.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp5\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (6.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp6\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (7.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp7\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (8.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp8\", \"manufacturer\": \"Stern\", \"year\": \"2004\"}, {\"clone_of\": \"lotr\", \"description\": \"Lord of the Rings, The (9.00 Spanish)\", \"flags\": 0, \"id\": \"lotr_sp9\", \"manufacturer\": \"Stern\", \"year\": \"2005\"}], \"format\": \"pinmame-machine-definition\", \"machine\": {\"id\": \"stern.lord-of-the-rings.2003\", \"manufacturer\": \"Stern\", \"name\": \"Lord of the Rings\", \"year\": 2003}, \"sources\": [{\"attribution\": \"pinmame-game-defs contributors\", \"id\": \"legacy.game.lotr\", \"kind\": \"legacy_json\", \"locator\": \"games/lotr.json; origin=vbscript-parser\", \"revision\": \"4ea106d080728648a693af3b4dcabb091eee0a02\", \"uri\": \"https://github.com/vpinball/pinmame-game-defs\"}, {\"attribution\": \"PinMAME contributors\", \"id\": \"pinmame.catalog.4ec52ff0ac13\", \"kind\": \"pinmame_catalog\", \"license\": \"BSD-3-Clause\", \"locator\": \"PinmameGetGames\", \"revision\": \"4ec52ff0ac133ac251681518aed2249e19fe26eb\", \"uri\": \"https://github.com/vpinball/pinmame\"}]}"
)

MANUAL = "manual.stern.lord-of-the-rings.2003"
PROFILE = "controller-profile.pinmame-whitestar"
CORE = "pinmame.core.4ec52ff0ac13"
CATALOG = "pinmame.catalog.4ec52ff0ac13"
LEGACY = "legacy.game.lotr"
T_VPW = "vpx-table.lotr-vpw-1-6"
S_VPW = "vpx-script.lotr-vpw-1-6"
T_JPS = "vpx-table.lotr-jpsalas-600"
S_JPS = "vpx-script.lotr-jpsalas-600"
T_HAN = "vpx-table.lotr-hanibal-4k"
S_HAN = "vpx-script.lotr-hanibal-4k"
T_NEO_LED = "vpx-table.lotr-neo-led-mod-1-0-3"
SUPPORT = "manual-support.stern.lord-of-the-rings.2003"
CONSENSUS_SOURCE = "spatial-consensus.stern.lord-of-the-rings.2003"

TABLE_SOURCE = {
    "vpw-1-6": T_VPW,
    "jpsalas-600": T_JPS,
    "hanibal-4k": T_HAN,
    "neo-led-1-0-3": T_NEO_LED,
}


SW = {s["address"]: s for s in transcription["switch_matrix"]["switches"]}
DS = {d["address"]: d for d in transcription["switch_matrix"]["dedicated_switches"]}
LAMPS = {l["address"]: l for l in transcription["lamp_matrix"]["lamps"]}
COILS = {c["address"]: c for c in transcription["coil_table"]["coils"]}
AUX = {a["address"]: a for a in transcription["coil_table"]["auxiliary_uk_only"]["coils"]}
SW_COLS = {c["column"]: c for c in transcription["switch_matrix"]["columns"]}
SW_ROWS = {r["row"]: r for r in transcription["switch_matrix"]["rows"]}
LA_COLS = {c["column"]: c for c in transcription["lamp_matrix"]["columns"]}
LA_ROWS = {r["row"]: r for r in transcription["lamp_matrix"]["rows"]}


def spatial_of(kind: str, address: int):
    entry = consensus["devices"].get(kind, {}).get(str(address))
    if not entry or entry.get("status") not in {"validated", "observed"} or "x" not in entry:
        return None
    return entry


def placement(device_id: str, role: str, entry: dict, extra_refs: tuple[str, ...] = ()):
    # Only tables whose own measurement supports the published coordinate may be cited for it.
    # A computed coordinate cites the tables it was derived from plus the manual that justified
    # the derivation, and never claims a table holds it.
    if entry.get("coordinate_origin") == "computed":
        refs = [TABLE_SOURCE[t] for t in entry.get("derived_from", []) if t in TABLE_SOURCE]
        refs.append(MANUAL)
    else:
        refs = [TABLE_SOURCE[t] for t in entry.get("agreeing_tables", []) if t in TABLE_SOURCE]
        refs += [r for r in extra_refs if r not in refs]
        if entry.get("resolved_by") == "manual" and MANUAL not in refs:
            refs.append(MANUAL)
    # The consensus artifact is the derivation authority for every coordinate, so it is cited
    # alongside the tables that supplied the measurements.
    refs.append(CONSENSUS_SOURCE)
    return {
        "id": f"{device_id}.{role}",
        "provenance": {"source_refs": refs or [MANUAL], "status": entry["status"]},
        "role": role,
        "space": "playfield",
        "x": round(float(entry["x"]), 6),
        "y": round(float(entry["y"]), 6),
    }


COMPUTED_ACROSS_TABLES: set[str] = set()
COMPUTED_WITHIN_ONE_TABLE: set[str] = set()


def located(device_id: str, role: str, entry: dict, extra_refs: tuple[str, ...] = ()):
    """Carry the consensus state through; a single-table measurement stays ``observed``."""
    if entry.get("coordinate_origin") == "computed":
        # `computed` covers two different things and they need different sentences. Where more
        # than one table fed the result it is a per-axis median of tables that disagreed, and all
        # of them appear in source_refs while none holds the published position. Where one table
        # fed it, the coordinate is a centroid of co-located bodies inside that single table -
        # no disagreement is involved, and saying "all three appear in its source_refs" of such a
        # row is simply false. Round seven had them in one bucket with the first sentence.
        (COMPUTED_ACROSS_TABLES if len(entry.get("derived_from", ())) > 1
         else COMPUTED_WITHIN_ONE_TABLE).add(device_id)
    return {"placements": [placement(device_id, role, entry, extra_refs)], "status": entry["status"]}


def not_applicable(reason: str, refs: list[str]):
    return {"provenance": {"source_refs": refs, "status": "validated"}, "reason": reason, "status": "not_applicable"}


def switch_wiring(address: int):
    column = (address - 1) // 8 + 1
    row = (address - 1) % 8 + 1
    col, rw = SW_COLS[column], SW_ROWS[row]
    return {
        "board": "CPU/Sound Board II",
        "drive_wire": col["wire"],
        "drive_connection": col["connector"],
        "driver_transistor": col["drive"],
        "return_wire": rw["wire"],
        "return_connection": rw["connector"],
        "return_component": rw["ic"],
    }


def lamp_wiring(address: int):
    column = (address - 1) % 8 + 1
    row = (address - 1) // 8 + 1
    col, rw = LA_COLS[column], LA_ROWS[row]
    return {
        "board": "I/O Power Driver Board",
        "drive_wire": rw["wire"],
        "drive_connection": rw["connector"],
        "driver_transistor": rw["drive"],
        "return_wire": col["wire"],
        "return_connection": col["connector"],
        "return_component": col["ic"],
        "nominal_voltage_v": 18.0,
        "voltage_type": "dc",
    }


def coil_wiring(record: dict):
    w = {"board": record.get("board") or "I/O Power Driver Board"}
    if record.get("transistor"):
        w["driver_transistor"] = record["transistor"]
    for src, dst in (("power_wire", "power_wire"), ("power_connector", "power_connection"),
                     ("control_wire", "control_wire"), ("control_connector", "control_connection")):
        if record.get(src):
            w[dst] = record[src]
    voltage = record.get("voltage")
    if voltage:
        w["nominal_voltage_v"] = float(voltage.split("v")[0])
        w["voltage_type"] = "dc" if "DC" in voltage.upper() else "ac"
    return w


EXCERPT_DIR = ROOT / "evidence/excerpts/stern.lord-of-the-rings.2003"


def _md_cell(value) -> str:
    if value is None or value == "":
        return "*(blank)*"
    if value is True:
        return "yes"
    return str(value).replace("|", "\\|").replace("~", " -> ")


def _md_table(headers: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(_md_cell(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def _manual_excerpt_contents() -> dict[Path, str]:
    switch = transcription["switch_matrix"]
    lamp = transcription["lamp_matrix"]
    coil = transcription["coil_table"]

    switch_text = "\n\n".join([
        "# Switch Matrix Grid, Dedicated Switches & Locations",
        "Transcribed from `Lord-of-the-Rings-Manual.pdf`, PDF page 6, printed `DR. 4`. The complete switch-matrix and dedicated-switch table regions are represented below. The numbered location drawing on the same page was also visually checked at 300 dpi when assigning the printed `Location` values.",
        "## Matrix drive columns\n\n" + _md_table(
            ["Column", "Drive", "Wire", "Connector"],
            [[row["column"], row["drive"], row["wire"], row["connector"]] for row in switch["columns"]],
        ),
        "## Matrix return rows\n\n" + _md_table(
            ["Row", "IC", "Wire", "Connector"],
            [[row["row"], row["ic"], row["wire"], row["connector"]] for row in switch["rows"]],
        ),
        "## Matrix devices\n\n" + _md_table(
            ["Address", "Name", "Location", "Part", "Edition scope", "DOTS", "Note"],
            [[row["address"], row.get("name"), row.get("location"), row.get("part"), row.get("edition_scoped"), row.get("dots"), row.get("note")] for row in switch["switches"]],
        ),
        "## Dedicated switches\n\n" + _md_table(
            ["Address", "Name", "IC", "Wire", "Connector", "Location", "Part"],
            [[row["address"], row.get("name"), row.get("ic"), row.get("wire"), row.get("connector"), row.get("location"), row.get("part")] for row in switch["dedicated_switches"]],
        ),
        f"Addressing: `{switch['addressing']}`. Geometry: {switch['geometry']}.",
    ]) + "\n"

    lamp_text = "\n\n".join([
        "# Lamp Matrix Grid & Locations",
        "Transcribed from `Lord-of-the-Rings-Manual.pdf`, PDF page 7, printed `DR. 5`. The complete 8x10 matrix, its drive/return wiring, and every printed lamp label and bulb type are represented below. The location drawing and back-panel inset on the same page were visually checked at 300 dpi.",
        "## Printed columns\n\n" + _md_table(
            ["Column", "IC", "Wire", "Connector"],
            [[row["column"], row["ic"], row["wire"], row["connector"]] for row in lamp["columns"]],
        ),
        "## Printed rows\n\n" + _md_table(
            ["Row", "Drive", "Wire", "Connector"],
            [[row["row"], row["drive"], row["wire"], row["connector"]] for row in lamp["rows"]],
        ),
        "## Matrix lamps\n\n" + _md_table(
            ["Address", "Name", "Bulb", "Location", "Note"],
            [[row["address"], row.get("name"), row.get("bulb"), row.get("location"), row.get("note")] for row in lamp["lamps"]],
        ),
        f"Addressing: `{lamp['addressing']}`. Geometry: {lamp['geometry']}.",
        f"Axis warning: {lamp['transposition_warning']}",
    ]) + "\n"

    coil_text = "\n\n".join([
        "# Coils Detailed Chart Table",
        "Transcribed from `Lord-of-the-Rings-Manual.pdf`, PDF page 8, printed `DR. 6`. The complete Q1-Q32 chart and the complete UK-only auxiliary table are represented below, including every `NOT USED` row and blank printed cell.",
        "## Main I/O power-driver outputs\n\n" + _md_table(
            ["Address", "Name", "Group", "State", "Kind", "Drive", "Board", "Power wire", "Power connection", "Voltage", "Control wire", "Control connection", "Coil or bulb"],
            [[row["address"], row.get("name"), row.get("group"), row.get("state"), row.get("kind"), row.get("transistor"), row.get("board"), row.get("power_wire"), row.get("power_connector"), row.get("voltage"), row.get("control_wire"), row.get("control_connector"), row.get("coil_spec")] for row in coil["coils"]],
        ),
        "## Auxiliary (UK only)\n\n" + _md_table(
            ["Address", "Name", "Drive", "Board", "Power wire", "Power connection", "Voltage", "Control wire", "Control connection", "Coil"],
            [[row["address"], row.get("name"), row.get("transistor"), coil["auxiliary_uk_only"]["board"], row.get("power_wire"), row.get("power_connector"), row.get("voltage"), row.get("control_wire"), row.get("control_connector"), row.get("coil_spec")] for row in coil["auxiliary_uk_only"]["coils"]],
        ),
        f"Printed flash-test note: {coil['note_from_manual']}",
    ]) + "\n"

    location_text = "\n\n".join([
        "# Coil & Flash Lamp Locations",
        "Read from `Lord-of-the-Rings-Manual.pdf`, PDF page 9, printed `DR. 7`. The accompanying crop retains the complete numbered playfield and back-panel location drawing. It was rendered from the cited PDF at 300 dpi, visually checked, and kept as an image because the leader lines, repeated flasher 25 callouts, above/below-playfield shading, bulb colours, and back-panel inset cannot be represented faithfully as a flat text table.",
        "## Printed facts used by the definition",
        "- Coil Q6 (Ring Magnet) and flashers 26 and 27 are explicitly located on the back panel.",
        "- Flasher 25 is printed three times at the three pop bumpers; the drawing therefore establishes quantity three rather than three public addresses.",
        "- The diagram marks flashers 14 and 23 yellow, all three flasher-25 bulbs and flasher 29 red, and flashers 26, 27, 30, 31 and 32 clear.",
        "- The drawing places the Balrog motor at 22 and its motor relay at 20, the three UK auxiliary posts at AUX 1-3, and every fitted main output 1-32 at its physical effect.",
        "- The printed legend distinguishes above-playfield, below-playfield and not-on-playfield devices; these dispositions were not inferred from VPX object classes.",
        "- Q24 is optional and may serve a coin meter, token dispenser or knocker; it is not a standard fitted playfield coil.",
    ]) + "\n"

    return {
        EXCERPT_DIR / "switch-matrix-dedicated-switches.md": switch_text,
        EXCERPT_DIR / "lamp-matrix.md": lamp_text,
        EXCERPT_DIR / "coils-detailed-chart.md": coil_text,
        EXCERPT_DIR / "coil-flash-lamp-locations.md": location_text,
    }


EXCERPT_CONTENTS = _manual_excerpt_contents()


def _excerpt_sha(path: Path) -> str:
    return hashlib.sha256(EXCERPT_CONTENTS[path].encode("utf-8")).hexdigest()


# --- authored switch semantics ---------------------------------------------------------
# roles are only added where they carry meaning for a consumer or drive the spatial rules:
# cabinet.* / service.* / flipper.*.button mark cabinet-or-service devices, internal.* marks
# devices with no visible playfield position.
SWITCH_ROLES = {
    1: ["cabinet.button"], 2: ["cabinet.coin"], 3: ["cabinet.coin"], 4: ["cabinet.coin"],
    5: ["cabinet.coin"], 6: ["cabinet.coin"], 7: ["cabinet.coin"], 8: ["cabinet.button"],
    11: ["internal.ball-trough"], 12: ["internal.ball-trough"], 13: ["internal.ball-trough"],
    14: ["internal.ball-trough"], 15: ["internal.ball-trough"],
    # Balrog Open and Closed are end-of-travel switches inside the toy's drive, asserted by the
    # motor logic rather than by a ball, and no retained recreation models them as objects.
    31: ["internal.balrog-mechanism"], 32: ["internal.balrog-mechanism"],
    54: ["cabinet.start"], 55: ["cabinet.start"], 56: ["cabinet.tilt"],
}
SWITCH_TYPES = {14: "opto", 15: "opto", 41: "opto", 47: "opto", 56: "tilt"}
OPTOS = {14, 15, 41, 47}

# Whitestar applies no switch inversion at all. lotrGameData (segames.c:1498) initializes only
# GEN_WS, the display layout and the `hw` struct, leaving the trailing `wpc` member -- and with it
# `wpc.invSw` -- at C zero-initialization, and core.c:2455 memcpy's those zeros into the live
# coreGlobals.invSw. So the public state of an opto is exactly what the recreation asserts; the
# ROM's own firmware accounts for the beam's rest state. An earlier pass here claimed "PinMAME
# normalizes the public state", which reached the right instruction for a recreation through a
# mechanism that does not exist.
#
# For these three the polarity is settled by observation rather than by reasoning: the retained
# known-working VPW 1.6 script drives each of them through a direct pair whose asserted sense is
# unambiguous, and it is known-working on the trough, which is where a reversed opto would break
# first. The cited lines are the assertion and the release.
SCRIPT_EVIDENCED_OPTOS = {
    14: ("656/657", "sw14_Hit sets Controller.Switch(14) = 1 and sw14_UnHit clears it, and the "
                    "ball-start block at line 454 seeds the four trough addresses asserted"),
    41: ("1115/1125", "the Top VUK entry handler sets Controller.Switch(41) = 1 and the kick-out "
                      "path clears it"),
    47: ("1189/1203", "the Ring Made handler sets Controller.Switch(47) = 1 and clears it after "
                      "the ball passes"),
}
# Switch 15 is the exception and the reason this machine carries a polarity conflict: no retained
# recreation binds it. The VPW table routes the stacking opto through its own trough bookkeeping
# without a Controller.Switch call, and neither alt table binds 14 or 15 at all.
UNEVIDENCED_OPTOS = sorted(OPTOS - set(SCRIPT_EVIDENCED_OPTOS))

UK_ONLY = {1, 8}
TOURNAMENT = {55}


def switch_type_for(address: int, record: dict) -> str:
    if address in SWITCH_TYPES:
        return SWITCH_TYPES[address]
    if record.get("location") in {"Coin Door", "Cabinet Side", "In Cabinet"}:
        return "button"
    part = record.get("part") or ""
    if part.startswith(("500-6227", "180-5054", "180-5015")):
        return "leaf"
    return "microswitch"


DEDICATED = [
    (-3, "switch.memory-protect", "Memory Protect", ["service.memory-protect"], "coin door",
     "PinMAME public -3. Printed in the Dr. Pinball board reference as the Memory Protect switch at the bottom of the coin-door bracket, beside the volume and service buttons."),
    (-2, "switch.volume", "Volume (Red Button)", ["service.volume"], "coin door", None),
    (-1, "switch.service-credit", "Service Credit (Green Button)", ["service.credit"], "coin door", None),
    (0, "switch.begin-test", "Begin Test (Black Button)", ["service.test"], "coin door", None),
    (81, "switch.right-flipper-eos", "Right Flipper End-of-Stroke", ["internal.flipper-eos"], "below playfield", None),
    (82, "switch.right-flipper-button", "Right Flipper Button", ["flipper.right.button"], "cabinet side", None),
    (83, "switch.left-flipper-eos", "Left Flipper End-of-Stroke", ["internal.flipper-eos"], "below playfield", None),
    (84, "switch.left-flipper-button", "Left Flipper Button", ["flipper.left.button"], "cabinet side", None),
]
DEDICATED_MANUAL = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1"}

# --- authored output semantics ---------------------------------------------------------
COIL_IDS = {
    1: ("device.trough-up-kicker", "coil"), 2: ("device.auto-launch", "coil"),
    3: ("device.left-vuk", "coil"), 4: ("device.top-vuk", "coil"), 5: ("device.right-vuk", "coil"),
    6: ("device.ring-magnet", "magnet"), 7: ("device.right-tower", "coil"),
    8: ("device.loop-diverter", "coil"), 9: ("device.left-bumper", "coil"),
    10: ("device.right-bumper", "coil"), 11: ("device.bottom-bumper", "coil"),
    13: ("device.orbit-pin", "coil"), 14: ("device.helms-deep-right-flasher", "flasher"),
    17: ("device.left-slingshot", "coil"), 18: ("device.right-slingshot", "coil"),
    19: ("device.top-saucer", "coil"), 20: ("device.balrog-motor-relay", "relay"),
    21: ("device.sword-lock-release", "coil"), 22: ("device.balrog-motor", "motor"),
    23: ("device.helms-deep-left-flasher", "flasher"), 24: ("device.optional-coil", "coil"),
    25: ("device.pop-bumper-flashers", "flasher"), 26: ("device.ring-flasher", "flasher"),
    27: ("device.back-panel-flasher", "flasher"), 29: ("device.ringwraith-flasher", "flasher"),
    30: ("device.sword-flasher", "flasher"), 31: ("device.destroy-the-ring-flasher", "flasher"),
    32: ("device.balrog-flasher", "flasher"),
}
# Effect coils are placed at the mechanism they drive, taken from the co-located switch or
# flasher coordinate that the manual's DR.7 location diagram confirms. Coils with no
# defensible anchor get a controlled internal_nonvisual record instead of a guess.
COIL_ANCHORS = {
    1: ("switch", 14, "DR.7 places 1 at the trough eject end; anchored to the trough eject opto."),
    2: ("switch", 16, "DR.7 places 2 at the shooter lane; anchored to the shooter-lane switch."),
    3: ("switch", 9, "DR.7 places 3 at the left VUK; anchored to its own switch."),
    4: ("switch", 41, "DR.7 places 4 at the top VUK; anchored to its own switch."),
    5: ("switch", 30, "DR.7 places 5 at the right VUK; anchored to its own switch."),
    6: ("flasher", 26, "DR.7's backpanel inset prints coil 6 (Magnet) beside flashers 26 and 27 at the ring; anchored to the ring flasher."),
    9: ("switch", 49, "Bumper coil co-located with its own bumper switch."),
    10: ("switch", 50, "Bumper coil co-located with its own bumper switch."),
    11: ("switch", 51, "Bumper coil co-located with its own bumper switch."),
    17: ("switch", 59, "Slingshot coil co-located with its own slingshot switch."),
    18: ("switch", 62, "Slingshot coil co-located with its own slingshot switch."),
    19: ("switch", 46, "DR.7 places 19 at the top saucer; anchored to its own switch."),
    22: ("switch", 28, "DR.7 places motor 22 at the Balrog; anchored to the Balrog hit switch on the toy."),
}
COIL_ROLES = {24: ["cabinet.knocker"]}
UK_AUX = {33: "AUX 1", 34: "AUX 2", 35: "AUX 3"}
RESERVED_SOLENOIDS = {
    16: "PinMAME's unused companion slot to the synthetic fast-flip state at public 15.",
    36: "Whitestar auxiliary board 520-5068-01 exposes three outputs at 33-35 and leaves 36 unused.",
    37: "Reserved compatibility hole in the Whitestar public solenoid range.",
    38: "Reserved compatibility hole in the Whitestar public solenoid range.",
    39: "Reserved compatibility hole in the Whitestar public solenoid range.",
    40: "Reserved compatibility hole in the Whitestar public solenoid range.",
    41: "Reserved compatibility hole in the Whitestar public solenoid range.",
    42: "Reserved compatibility hole in the Whitestar public solenoid range.",
    43: "Reserved compatibility hole in the Whitestar public solenoid range.",
    44: "Reserved compatibility hole in the Whitestar public solenoid range.",
    49: "PinMAME's simulation shooter slot; not a physical machine output.",
    50: "Reserved slot at the top of the Whitestar public solenoid range.",
}

# --- sources ---------------------------------------------------------------------------
SOURCES = [
    next(s for s in partial["sources"] if s["id"] == CATALOG),
    next(s for s in partial["sources"] if s["id"] == LEGACY),
    {
        "attribution": "PinMAME contributors", "id": CORE, "kind": "pinmame_core", "license": "BSD-3-Clause",
        "locator": (
            "src/wpc/segames.c lotrGameData GEN_WS with se_dmd128x32, FLIP_SW(FLIP_L) with FLIP_SOL(FLIP_L), "
            "lampCol=5, custSol=0 and board identifiers SE_BOARDID_520_5068_01 | SE_BOARDID_520_5242_00, plus the "
            "lotr/lotr_sp/lotr_gr/lotr_fr/lotr_it ROM definitions; src/wpc/se.c coreGlobals.nLamps = 64 + lampCol*8 "
            "sizing the lamp array to 104, with lampdriv_w writing eight matrix columns at CORE_MODOUT_LAMP0 and "
            "auxlamp_w two auxiliary columns at CORE_MODOUT_LAMP0+64 for the printed 8x10 matrix at public 1-80, and "
            "the remaining space carrying the serial board declared by SE_BOARDID_520_5242_00, which src/wpc/se.h "
            "names the Lord of The Rings 19 LED Board: se.c drives it through "
            "core_set_pwm_output_led_vfd(CORE_MODOUT_LAMP0 + 80, 3 * 8, CORE_MODOUT_LED, 4.f / 2.f) and core_write_pwm_output_8b "
            "at CORE_MODOUT_LAMP0 + 80, + 88 and + 96 masked 0x07, i.e. public lamps 81-99. Those nineteen LEDs are "
            "real and are enumerated at public lamp addresses 81-99 through the same widened Whitestar lamp transport; "
            "src/wpc/se.c coreGlobals.nGI = 1 exposing the general-illumination relay as a single aggregate channel; "
            "src/wpc/core.h core_tGameData field order flippers, swCol, lampCol, custSol"
        ),
        "revision": "4ec52ff0ac133ac251681518aed2249e19fe26eb", "uri": "https://github.com/vpinball/pinmame",
    },
    {
        "attribution": "PinMAME contributors", "id": PROFILE, "kind": "human_review", "license": "BSD-3-Clause",
        "locator": (
            "Whitestar public switch, DIP, solenoid, lamp and GI address rules, including the sequential switch "
            "conversion with dedicated inputs at -3..0 and 81-88, the shared lamp transport at 1-336 whose ceiling "
            "is established by src/wpc/bowlgames.c coinGameData (lampCol=34), shared by the titanic and monopred "
            "coin-dropper drivers, with physical addresses determined by each game's own lampCol declaration and "
            "driver writes, and the legacy "
            "lower-flipper pairs that expose Q16 right at power 45 with canonical callback 46 and Q15 left at power "
            "47 with canonical callback 48 while public 15 carries the synthetic fast-flip state"
        ),
        "revision": "repository", "uri": "internal:controllers/pinmame/whitestar.json",
    },
    {
        "attribution": "Stern Pinball, Inc.", "id": MANUAL, "kind": "manual",
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "locator": (
            "Official 184-page English service manual downloaded from Stern Pinball. IPDB machine 4858 independently "
            "identifies the title and links an English manual. The PDF is image-only, so every table was read from pages "
            "rendered at 300 dpi. PDF page 6 "
            "is the printed Dr. Pinball 4 switch matrix, dedicated switches and switch locations; page 7 the Dr. "
            "Pinball 5 lamp matrix and lamp locations including the backpanel inset; page 8 the Dr. Pinball 6 coils "
            "detailed chart table with the UK-only auxiliary board; page 9 the Dr. Pinball 7 coil and flash lamp "
            "locations with the typical switch, lamp and coil wiring schematics."
        ),
        "original_filename": "Lord-of-the-Rings-Manual.pdf",
        "sha256": "1334be3a5471ebcf9b00659e2ff63e2eaea78efefab54cd57ed37a8c46ac8d2e",
        "uri": "external:pinmame-manuals/by-machine/stern.lord-of-the-rings.2003/official-stern/Lord-of-the-Rings-Manual.pdf",
        "excerpts": [
            {
                "id": "excerpt.lotr.switch-matrix-dedicated-switches",
                "locator": "PDF page 6, printed DR. 4, complete switch matrix and dedicated-switch regions",
                "method": "manual",
                "path": "evidence/excerpts/stern.lord-of-the-rings.2003/switch-matrix-dedicated-switches.md",
                "reviewed": True,
                "sha256": _excerpt_sha(EXCERPT_DIR / "switch-matrix-dedicated-switches.md"),
            },
            {
                "id": "excerpt.lotr.lamp-matrix",
                "locator": "PDF page 7, printed DR. 5, complete lamp matrix and location annotations",
                "method": "manual",
                "path": "evidence/excerpts/stern.lord-of-the-rings.2003/lamp-matrix.md",
                "reviewed": True,
                "sha256": _excerpt_sha(EXCERPT_DIR / "lamp-matrix.md"),
            },
            {
                "id": "excerpt.lotr.coils-detailed-chart",
                "locator": "PDF page 8, printed DR. 6, complete Q1-Q32 and UK auxiliary coil tables",
                "method": "manual",
                "path": "evidence/excerpts/stern.lord-of-the-rings.2003/coils-detailed-chart.md",
                "reviewed": True,
                "sha256": _excerpt_sha(EXCERPT_DIR / "coils-detailed-chart.md"),
            },
            {
                "id": "excerpt.lotr.coil-flash-lamp-locations",
                "image": "evidence/excerpts/stern.lord-of-the-rings.2003/coil-flash-lamp-locations.webp",
                "image_derivation": "Lord-of-the-Rings-Manual.pdf page 9, crop box 0.02,0.02,0.58,0.96, rendered at 300 dpi with pdftoppm and reduced to 680px-wide quality-30 WebP",
                "image_sha256": "8bce0f7d1a5e8af01d55643c5d61a6687eac7884808817b6bba0b6026fa97fd9",
                "locator": "PDF page 9, printed DR. 7, complete numbered playfield and back-panel location drawing",
                "method": "manual",
                "path": "evidence/excerpts/stern.lord-of-the-rings.2003/coil-flash-lamp-locations.md",
                "reviewed": True,
                "sha256": _excerpt_sha(EXCERPT_DIR / "coil-flash-lamp-locations.md"),
            },
        ],
    },
    {
        "attribution": "pinmame-game-defs curation", "id": SUPPORT, "kind": "human_review", "license": "NOASSERTION",
        "locator": (
            "Retained machine-readable transcription of every printed table used by this definition, with the rendered "
            "300 dpi page cache beside it. Also records the two source anomalies preserved rather than normalized: the "
            "manual prints LEGOLES for lamps 15 and 33, and the retained scripts label coils 4 and 19 Upper-Left VUK "
            "and Upper-Right Kicker where the manual prints Top VUK and Top Saucer."
        ),
        "revision": "2026-08-06",
		"sha256": "594a7f1f6fc7162b5a0a8043e5fa5b78f7623efc96e1713559168d729aeee2f5",
        "uri": "external:pinmame-manuals/by-machine/stern.lord-of-the-rings.2003/transcription.json",
    },
    {
        "attribution": "pinmame-game-defs curation", "id": CONSENSUS_SOURCE, "kind": "human_review",
        "license": "NOASSERTION",
        "revision": "2026-08-08",
        "sha256": "58eb403ba22b7c71f7360e785b08e47fb844dd77979553119028007815024456",
        "locator": (
            "Four-table spatial derivation produced by tools/lotr_spatial_resolve.py --write <path> from the retained extractions. "
            "Three factory-layout recreations form the lamp, switch and flasher consensus; the Neo LED mod supplies "
            "a supplemental, derivative measurement for script-bound addresses 81-99. The artifact is the authority for every "
            "coordinate in this definition: for each device it records each "
            "table's measurement, the published coordinate, which tables support it within the 0.025 agreement "
            "threshold, which disagree, whether the coordinate is held by a table or computed, and any manual "
            "tie-break with its reason."
        ),
        "uri": "external:pinmame-vpx-sources/stern/lord-of-the-rings-2003/derived/spatial-consensus.json",
    },
]

SOURCES.append({
    "attribution": "JPSalas; Neo LED Mod contributors",
    "id": T_NEO_LED,
    "kind": "vpx_table",
    "license": "NOASSERTION",
    "rights": "NOASSERTION",
    "locator": (
        "Retained installed Lord Of The Rings Neo LED Mod 1.0.3 recreation, 81,432,576 bytes, used only as a "
        "supplemental measurement for its script-bound Light.l81 through Light.l99 objects. Its info.json identifies "
        "JPSalas, table version 1.0.1, and its script header says 'VPX version by jpsalas', so it is disclosed as a "
        "derivative rather than treated as independent corroboration. Valinor is the VPW table's identity, not this one."
    ),
    "original_filename": "Lord Of The Rings (Stern - 2003)Neo LED Mod 1.0.3.vpx",
    "sha256": "c78b9aede14a7d19865777ce25f50634ba8a491b54888d161a0257b2aff91b0a",
    "uri": "external:pinmame-vpx-sources/stern/lord-of-the-rings-2003/source/Lord%20Of%20The%20Rings%20(Stern%20-%202003)Neo%20LED%20Mod%201.0.3.vpx",
})

for extraction_id, table_id, root_note, files, total, digest in [
    ("vpx-extraction.lotr-vpw-1-6", T_VPW, "vpxtool-extract", 2205, 601211181,
     "a0a19f4e9cc4c79926b90ab316976c23d0c630f50836cba13c7217eaa04c8eef"),
    ("vpx-extraction.lotr-jpsalas-600", T_JPS, "alt-jpsalas-600/vpxtool-extract", 991, 29996681,
     "61b56590043a87b2dbc598707b6e3e8795a6cbf7f49bf3b0186d44aa3a59bd20"),
    ("vpx-extraction.lotr-hanibal-4k", T_HAN, "alt-hanibal-4k/vpxtool-extract", 1782, 139913171,
     "4d35775d85997e98154c88755b69bdfee8ca21b30e593ad35a6a0b890c715d1e"),
    ("vpx-extraction.lotr-neo-led-mod-1-0-3", T_NEO_LED, "source/vpxtool-extract", 918, 89622867,
     "9994e751b61834168471aa7add4a90f1a619b93f6e0950ef458403fa771d86b3"),
]:
    _manifest_uri = f"external:pinmame-vpx-sources/stern/lord-of-the-rings-2003/{root_note.rsplit('/', 1)[0] if '/' in root_note else '.'}/extraction-manifest.json".replace("/./", "/")
    SOURCES.append({
        "attribution": "vpxtool extraction", "id": extraction_id, "kind": "vpx_table", "license": "NOASSERTION",
        "locator": (
            f"Canonical manifest of the retained {root_note} tree produced with vpxtool git:v0.33.3: every regular "
            f"file as a sorted relative POSIX path with byte size and SHA-256, {files:,} files, {total:,} bytes. "
            "This record's sha256 is the hash of the manifest file itself, as for every other source here. The "
            f"extraction-tree digest is a separate value, {digest} - the SHA-256 of the manifest object serialised "
            "as canonical JSON with sorted keys and compact separators, carried in the file's own manifest_sha256 "
            "field and recomputable with tools/lotr_extraction_manifest.py --verify. The geometry cited by every "
            f"placement comes from this extraction of {table_id}."
        ),
        # Was the tree digest, so `sha256` meant two different things inside one `sources` array
        # and a consumer hashing the named file got a mismatch. Uniform now; the tree digest is
        # still pinned, in the locator and in the file's own field, and still recomputed by a test.
        "sha256": EXTRACTION_FILE_HASHES[extraction_id],
        "uri": _manifest_uri,
    })
SCRIPT_HASHES = {
    S_VPW: (188766, "20dd6295a58ffd4f22a429bb34b40ebbaa2572b9d314ecfae009758cbef18d69"),
    S_JPS: (34973, "165da470d270cecff33db22e047068bd33b35489a1324dc51f567221409edf23"),
    S_HAN: (52034, "a37d9e5cec70f90a7c60148fc572debde5a52693cf2b89cd8ce443b1b9a4a496"),
}
for table_id, script_id, author, subdir, name, sha, size, note in [
    (T_VPW, S_VPW, "Visual Pinball Workshop", "", "Lord of the Rings (Stern 2003) VPW 1.6.vpx",
     "efd7860292912f1891ebf59337e0907e1f02931887ae2f0c78cbc40760bae1b6", 373870592,
     "Playfield bounds left=0 top=0 right=952 bottom=2203. Its own info.json identifies it as 'Lord Of The Rings - "
     "Valinor Edition' with original artwork, so where its insert layout departs from the printed location diagrams "
     "that is an artwork difference, not an error: its Fellowship inserts form a closed ring of runes rather than the "
     "wide arc of named characters the printed diagram shows. VPW_REJECTED_LAMPS Geometry authority for named objects only. It does model the six "
     "back-panel mode lamps 73-78, as p73-p78 primitives driven through Lampz.Callback rather than as l<N> lights. "
     "Acquisition page: https://vpuniverse.com/files/file/8828-lord-of-the-rings-valinor-edition-stern-2003-vpw/."),
    (T_JPS, S_JPS, "JPSalas", "alt-jpsalas-600/", "JP's Lord of the Rings (Stern 2003) v600.vpx",
     "41026827ebad5fe7b88c28e7ad99e700078dfa0eb32ac4c69d4c54d383185013", 22110208,
     "Its info.json records the playfield as 'based on Ebislit's playfield', the same baseline scan the VPW "
     "recreation credits. Its f<N>l objects are non-positional helper lights parked together and carry no usable "
     "coordinate; only the Flasher props do. Acquisition page: "
     "https://www.vpforums.org/index.php?app=downloads&showfile=12898."),
    (T_HAN, S_HAN, "Hanibal", "alt-hanibal-4k/", "Lord of the Rings (stern 2003) Hanibal 4k.vpx",
     "662a24bdc1619c4708bf4a4a482616f48b02520202855d1a916fb461d91afa2c", 106475520,
     "Identifies itself as 'Lord of the Rings (Stern 2003) 4k Mod', which declares a modification but names no baseline table. Independence between the "
     "three retained recreations is unestablished and no lineage is asserted: measured agreement pairs this table "
     "with the JPSalas recreation (within 0.0155 on every shared lamp, against up to 0.187 for either versus VPW), "
     "while the only documented ancestry pairs VPW with JPSalas, both of which credit an EBIsLit playfield scan. "
     "Because the two signals disagree, a placement is validated here only when all three tables agree on it. "
     "Acquisition page: https://vpuniverse.com/files/file/4626-lord-of-the-rings-hanibals-4k-edition/."),
]:
    SOURCES.append({
        "attribution": author, "id": table_id, "kind": "vpx_table", "license": "NOASSERTION", "rights": "NOASSERTION",
        "locator": f"Retained known-working recreation of the physical machine, {size:,} bytes. {note}",
        "original_filename": name, "sha256": sha,
        "uri": f"external:pinmame-vpx-sources/stern/lord-of-the-rings-2003/{subdir}{name.replace(' ', '%20')}",
    })
    script_name = name.replace(".vpx", ".vbs")
    script_bytes, script_sha = SCRIPT_HASHES[script_id]
    SOURCES.append({
        "attribution": author, "id": script_id, "kind": "vpx_script", "known_working": True,
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "locator": (
            f"Embedded script extracted from {name} with vpxtool, {script_bytes:,} bytes; cGameName = \"lotr\". "
            "Runtime and mechanism-causality authority."
        ),
        "original_filename": script_name,
        "sha256": script_sha,
        "uri": f"external:pinmame-vpx-sources/stern/lord-of-the-rings-2003/{subdir}{script_name.replace(' ', '%20')}",
    })

ACRONYMS = {"VUK", "P/F", "PF", "U.L.", "U.R.", "L.L.", "L.R.", "DBA", "UK", "POTD", "ORC",
            "2X", "L", "R", "C", "E.O.S.", "DMD", "GI"}
LOWERCASE_WORDS = {"of", "the", "and", "vs", "to", "a"}
EXPANSIONS = {"LT": "Left", "RT": "Right"}


def labelize(text: str) -> str:
    """Title-case a printed name without destroying what the printing means.

    Insert names such as ``(K) EEP`` and ``(O) RC`` use capitalisation to show which letter
    the insert lights; lower-casing it throws the name away. Any token carrying a parenthesis
    is therefore emitted exactly as printed, as are known acronyms.
    """
    if "(" in text or ")" in text:
        # A parenthesised letter marks which letter of the word this insert lights, so the whole
        # name is a unit: "(K) EEP", "K (E) EP", "O (R) C". Re-casing any part of it destroys the
        # thing the printing is communicating. Emit exactly as printed.
        return text
    words = text.split()
    out = []
    for index, word in enumerate(words):
        bare = word.strip("():.,")
        if "(" in word or ")" in word:
            out.append(word)
        elif word.upper() in ACRONYMS:
            out.append(word.upper())
        elif bare.upper() in EXPANSIONS:
            out.append(word.upper().replace(bare.upper(), EXPANSIONS[bare.upper()]))
        elif word.startswith("#"):
            out.append(word)
        elif len(bare) == 1:
            out.append(word.upper())
        elif index and word.lower() in LOWERCASE_WORDS:
            out.append(word.lower())
        else:
            out.append(word.capitalize() if word.isupper() else word)
    return " ".join(out)


PROJECTIONS: list[dict] = []
UNPLACED: list[dict] = []

# The printed switch table states, per switch, where the switch physically is. That column is
# the manual placing the device, so it decides whether `not_applicable` is even available:
# a device the manual puts on the playfield can never be recorded as having no placeable
# position on the manual's own authority. Round six fixed that for coils by hand-listing the
# ten DR.7 addresses and left the switch namespace falling through to `not_applicable`, which
# is how switches 15, 31 and 32 kept a false record. This derives the answer instead, so the
# rule cannot be true for one namespace and forgotten in another.
PLAYFIELD_PRINTED_LOCATIONS = {"Above P/F", "Back Panel", "Below P/F", "Below Playfield", "Mini-P/F"}
CABINET_PRINTED_LOCATIONS = {"Cabinet Side", "Coin Door", "In Cabinet", "on Cabinet Side", "on Coin Door"}


def printed_location_class(location: str | None) -> str:
    """Say what the printed location column claims: a playfield position, a cabinet one, or nothing."""
    if location is None:
        return "unstated"
    if location in PLAYFIELD_PRINTED_LOCATIONS:
        return "playfield"
    if location in CABINET_PRINTED_LOCATIONS:
        return "cabinet"
    raise SystemExit(f"printed location not classified: {location!r}")


def unresolved_spatial(device_id: str, address: int, label_text: str, printed_evidence: str):
    """Record the device as having no spatial evidence yet, and say so in the report."""
    UNPLACED.append({"device": device_id, "address": address, "label": label_text,
                     "printed_evidence": printed_evidence})
    return None


inputs = []
for address in range(1, 65):
    rec = SW[address]
    unused = rec.get("state") == "not_used"
    device_id = f"switch.matrix-{address}"
    roles = SWITCH_ROLES.get(address, [])
    optional = address in UK_ONLY or address in TOURNAMENT or (rec.get("note") == "Future Use")
    availability = "unused" if unused else ("optional" if optional else "used")
    entry = {
        "aliases": [{"namespace": "pinmame.switch", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": availability,
        "binding": {"device": address, "group": "pinmame.input.switch"},
        "id": device_id,
        "kind": "switch",
        "label": ({11: "4-Ball Trough #1 (Left)", 12: "4-Ball Trough #2", 13: "4-Ball Trough #3"}.get(address)
                  or labelize(rec["name"]))
                 if rec.get("name") else f"Unused Switch {address}",
        "provenance": {"source_refs": [MANUAL, CORE, PROFILE] + ([] if unused else [S_VPW]), "status": "validated"},
    }
    if roles:
        entry["roles"] = roles
    notes = []
    column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
    notes.append(f"Printed switch-matrix drive column {column}, return row {row}.")
    if rec.get("note"):
        notes.append(rec["note"] + ".")
    if address in UK_ONLY:
        notes.append("Fitted on UK cabinets only.")
    if address in TOURNAMENT:
        notes.append("Present only with the optional Tournament Kit.")
    if unused:
        notes.append("Printed NOT USED in the switch matrix; the address is wired but carries no device.")
    physical = {"notes": " ".join(notes)}
    if rec.get("location"):
        physical["location"] = rec["location"]
    if not unused:
        physical["switch_type"] = switch_type_for(address, rec)
        if rec.get("part"):
            physical["part_number"] = rec["part"]
        entry["normally_closed"] = address in OPTOS
        if address not in OPTOS:
            notes.append(
                "The printed typical switch wiring lands the green drive wire on the normally-open terminal, so matrix "
                "switches rest open."
            )
        else:
            notes.append(
                "Opto assembly: the beam rests made, so the switch rests closed and opens when a ball blocks it. That "
                "describes the physical contact, not the public state: pinned PinMAME applies no inversion on "
                "Whitestar, because lotrGameData (segames.c:1498) leaves the wpc member -- and with it wpc.invSw -- "
                "zero-initialized and core.c:2455 copies those zeros into the live mask, so the ROM's own firmware "
                "accounts for the beam's rest state and the public state is whatever a recreation asserts."
            )
            if address in SCRIPT_EVIDENCED_OPTOS:
                lines, how = SCRIPT_EVIDENCED_OPTOS[address]
                notes.append(
                    f"The retained known-working VPW 1.6 script asserts this address when a ball is present ({how}, "
                    f"lines {lines}), so a recreation should do the same."
                )
            else:
                notes.append(
                    "No retained recreation binds this address, so unlike switches "
                    + ", ".join(str(a) for a in sorted(SCRIPT_EVIDENCED_OPTOS))
                    + " the public sense the ROM expects here is unestablished; see "
                    "conflict.whitestar-invsw-never-populated."
                )
        physical["notes"] = " ".join(notes)
    entry["physical"] = physical
    entry["wiring"] = switch_wiring(address)
    sp = spatial_of("switch", address)
    printed_class = printed_location_class(rec.get("location"))
    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif printed_class == "cabinet" or (roles and any(r.startswith(("cabinet.", "service.")) for r in roles)):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif sp:
        entry["spatial"] = located(device_id, "sensor", sp, (MANUAL,))
    elif printed_class == "playfield":
        entry["spatial"] = unresolved_spatial(
            device_id, address, rec.get("name", device_id),
            f"The printed switch table places switch {address} at {rec['location']}, and no retained table measures it.",
        )
    else:
        entry["spatial"] = not_applicable("internal_nonvisual", [MANUAL, S_VPW])
    if entry["spatial"] is None:
        del entry["spatial"]
    inputs.append(entry)

for address, device_id, label, roles, location, note in DEDICATED:
    manual_ref = DEDICATED_MANUAL.get(address)
    aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
    if manual_ref:
        aliases.append({"namespace": "manual.address", "value": manual_ref})
    rec = DS.get(manual_ref, {})
    notes = [note] if note else []
    if manual_ref:
        notes.append(f"Printed dedicated switch {manual_ref}, {rec.get('wire','')} {rec.get('connector','')} into {rec.get('ic','U206')}.".replace("  ", " "))
    if rec.get("in_test"):
        notes.append(f"In test mode this button acts as {rec['in_test']}.")
    entry = {
        "aliases": aliases,
        "availability": "used",
        "binding": {"device": address, "group": "pinmame.input.switch"},
        "id": device_id,
        "kind": "switch",
        "label": label,
        "normally_closed": False,
        "physical": {"location": location, "switch_type": "button" if "button" in device_id or address <= 0 else "microswitch",
                     "notes": " ".join(n for n in notes if n)},
        "provenance": {"source_refs": [MANUAL, PROFILE, CORE], "status": "validated"},
        "roles": roles,
    }
    printed_class = printed_location_class(rec.get("location"))
    if printed_class == "cabinet" or any(r.startswith(("cabinet.", "service.")) or r.endswith(".button") for r in roles):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, PROFILE])
    elif printed_class == "playfield":
        # DS-2 and DS-4, the flipper end-of-stroke switches. The printed dedicated-switch table
        # puts both below the playfield, so their position is unresolved, not inapplicable.
        entry["spatial"] = unresolved_spatial(
            device_id, address, rec.get("name", label),
            f"The printed dedicated-switch table places {manual_ref} at {rec['location']}, and no retained table measures it.",
        )
    else:
        entry["spatial"] = not_applicable("internal_nonvisual", [MANUAL, PROFILE])
    if entry.get("spatial") is None:
        entry.pop("spatial", None)
    if rec.get("part"):
        entry["physical"]["part_number"] = rec["part"]
    inputs.append(entry)

for address in (85, 86, 87, 88):
    inputs.append({
        "aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
        "availability": "unused",
        "binding": {"device": address, "group": "pinmame.input.switch"},
        "id": f"switch.flipper-column-{address}",
        "kind": "switch",
        "label": f"Unused Flipper-Column Input {address}",
        "physical": {"notes": (
            "Whitestar exposes generic flipper-column holes at 85-87 and a fifth dedicated input at 88 for games with "
            "an upper flipper. Lord of the Rings has two flippers and no upper flipper, so none of these carry a device."
        )},
        "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
        "spatial": not_applicable("unused", [PROFILE]),
    })

# The CPU board's SW300 country selector consumes the low five bits; the profile retains the
# full eight-address LibPinMAME bank so a definition can mark the rest unused explicitly.
DIP_COUNTRIES = "USA, Austria, Australia, Belgium, Canada, Denmark, Finland, France, Germany, Greece, Italy, Netherlands, New Zealand, Norway, Portugal, Spain, Sweden, Switzerland and the UK"
for position in range(1, 9):
    used = position <= 5
    inputs.append({
        "aliases": [{"namespace": "pinmame.dip", "value": str(position)},
                    {"namespace": "manual.address", "value": f"SW300-{position}"}],
        "availability": "used" if used else "unused",
        "binding": {"device": position, "group": "pinmame.input.dip"},
        "id": f"dip.sw300-{position}",
        "kind": "dip_switch",
        "label": f"SW300 Position {position}",
        "physical": {
            "location": "CPU/Sound board, right of CN6",
            "switch_type": "dip",
            "notes": (
                f"Printed CPU DIP switch bank SW300 (KSD08H), position {position}. The printed country chart sets "
                f"positions 1-5 to select {DIP_COUNTRIES}; positions 6-8 are unused."
                if used else
                f"Printed CPU DIP switch bank SW300 (KSD08H), position {position}. The printed country chart never "
                "sets positions 6-8; PinMAME publishes the full eight-address bank regardless."
            ),
        },
        "provenance": {"source_refs": [MANUAL, PROFILE, CORE], "status": "validated"},
        "spatial": not_applicable("dip_switch", [MANUAL, PROFILE]),
    })

outputs = []


# Devices the printed DR.7 location drawing places with a boxed position on the playfield
# outline, but which no retained table models. Their position is UNRESOLVED, not inapplicable:
# saying not_applicable would assert on the manual's authority that a device the manual places
# has no placeable position. A partial definition may omit spatial evidence, so it does, and
# every one is listed in the spatial report.
PRINTED_BUT_UNPLACED = {
    7: "DR.7 prints a boxed position for coil 7 on the playfield outline.",
    8: "DR.7 prints a boxed position for coil 8 on the playfield outline.",
    13: "DR.7 prints a boxed position for coil 13 on the playfield outline.",
    20: "DR.7 prints a boxed position for the Balrog motor relay on the playfield outline.",
    21: "DR.7 prints a boxed position for coil 21 on the playfield outline; the report's own flasher-30 resolution cites it.",
    33: "DR.7 prints Aux 1 at the left inlane area.",
    34: "DR.7 prints Aux 2 between the flippers.",
    35: "DR.7 prints Aux 3 at the right.",
    46: "DR.7 shades printed coil 16, the right flipper, as a coil below the playfield and prints its position.",
    48: "DR.7 shades printed coil 15, the left flipper, as a coil below the playfield and prints its position.",
}


def coil_spatial(address: int, device_id: str, kind: str):
    if address == 25:
        emitter_rows = consensus["devices"]["flasher"]["25"]["emitters"]
        placements = [
            placement(f"{device_id}.{side}", "emitter", emitter_rows[side], (MANUAL,))
            for side in ("left", "right", "bottom")
        ]
        return {"placements": placements, "status": "validated"}
    if kind == "flasher":
        sp = spatial_of("flasher", address)
        if sp:
            return located(device_id, "emitter", sp, (MANUAL,))
    anchor = COIL_ANCHORS.get(address)
    if anchor:
        anchor_kind, anchor_address, reason = anchor
        sp = spatial_of(anchor_kind, anchor_address)
        if sp:
            # A projection, not a measurement. No table measured the coil; its coordinate is
            # borrowed from a co-located device the manual's location diagram puts beside it.
            # It must therefore never inherit the anchor's validated status, and it is recorded
            # in the spatial report's projection list.
            projected = dict(sp)
            projected["status"] = "observed"
            PROJECTIONS.append({
                "device": device_id,
                "anchor": f"{anchor_kind}.{anchor_address}",
                "reason": reason,
                "x": round(float(sp["x"]), 6),
                "y": round(float(sp["y"]), 6),
            })
            return located(device_id, "effect", projected, (MANUAL,))
    if address in PRINTED_BUT_UNPLACED:
        return unresolved_spatial(device_id, address, COILS.get(address, {}).get("name", device_id),
                                  PRINTED_BUT_UNPLACED[address])
    return not_applicable("internal_nonvisual", [MANUAL, S_VPW])


for address in range(1, 33):
    rec = COILS[address]
    unused = rec.get("state") == "not_used"
    if unused:
        outputs.append({
            "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                        {"namespace": "manual.address", "value": f"#{address}"}],
            "availability": "unused",
            "binding": {"device": address, "group": "pinmame.output.solenoid"},
            "id": f"device.solenoid-{address}-unused",
            "kind": "coil",
            "label": f"Unused Solenoid {address}",
            "physical": {"notes": (
                f"Printed NOT USED in the coils detailed chart table of the manual for the 2003 production "
                f"machine, which is not a claim about every driver in the tree. Drive transistor {rec.get('transistor')} and "
                f"control line {rec.get('control_wire')} at {rec.get('control_connector')} exist on the board but no "
                "device is fitted."
            )},
            "provenance": {"source_refs": [MANUAL, CORE], "status": "validated"},
            "spatial": not_applicable("unused", [MANUAL]),
            "wiring": coil_wiring(rec),
        })
        continue
    if address in (15, 16):
        continue  # public 15/16 are PinMAME synthetic slots; the physical coils live at 45-48
    device_id, kind = COIL_IDS[address]
    optional = rec.get("state") == "optional"
    notes = [f"Printed coils chart entry #{address} in group {rec.get('group', '').replace('_', ' ')}."]
    if rec.get("note"):
        notes.append(rec["note"])
    if rec.get("coil_spec"):
        notes.append(f"Printed coil or bulb type {rec['coil_spec']}.")
    if address == 25:
        notes.append(
            "The printed location diagram prints 25 three times, once beside each of coils 9, 10 and 11, so this "
            "address drives three physical flashlamps at the three pop bumpers. Each bulb has its own placement at "
            "the corresponding bumper; no non-physical centroid is published."
        )
    entry = {
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": f"#{address}"}],
        "availability": "optional" if optional else "used",
        "binding": {"device": address, "group": "pinmame.output.solenoid"},
        "id": device_id,
        "kind": kind,
        "label": labelize(rec["name"].replace("FLASH: ", "")) + (" Flasher" if kind == "flasher" else ""),
        "physical": {"notes": " ".join(notes), **({"quantity": 3} if address == 25 else {})},
        "provenance": {"source_refs": [MANUAL, S_VPW, CORE], "status": "validated"},
        "wiring": coil_wiring(rec),
    }
    _spatial = coil_spatial(address, device_id, kind)
    if _spatial is not None:
        entry["spatial"] = _spatial
    if COIL_ROLES.get(address):
        entry["roles"] = COIL_ROLES[address]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    outputs.append(entry)

outputs.append({
    "aliases": [{"namespace": "pinmame.solenoid", "value": "15"}],
    "availability": "used",
    "binding": {"device": 15, "group": "pinmame.output.solenoid"},
    "id": "device.fast-flip-state",
    "kind": "virtual",
    "label": "Fast-Flip Game-On State",
    "physical": {"notes": (
        "PinMAME's synthetic fast-flip and game-on state, not a machine output. The physical flipper coils printed as "
        "#15 and #16 are exposed at public 45-48 instead."
    )},
    "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
    "spatial": not_applicable("virtual", [PROFILE]),
})
for address, note in RESERVED_SOLENOIDS.items():
    outputs.append({
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "binding": {"device": address, "group": "pinmame.output.solenoid"},
        "id": f"device.solenoid-{address}-reserved",
        "kind": "virtual",
        "label": f"Reserved Solenoid Slot {address}",
        "physical": {"notes": note},
        "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
        # These slots are synthetic controller addresses, not absent physical devices, so the
        # controlled reason is virtual rather than unused.
        "spatial": not_applicable("virtual", [PROFILE]),
    })
for address, manual_ref in UK_AUX.items():
    rec = AUX[manual_ref]
    device_id = f"device.uk-{rec['name'].lower().replace('/', '-').replace(' ', '-')}"
    outputs.append({
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": manual_ref}],
        "availability": "optional",
        "binding": {"device": address, "group": "pinmame.output.solenoid"},
        "id": device_id,
        "kind": "coil",
        "label": labelize(rec["name"]) + " (UK)",
        "physical": {"notes": (
            f"Printed auxiliary coil {manual_ref} on the UK 3X Transformer Driver Board, fitted on UK cabinets only. "
            f"Printed coil type {rec['coil_spec']}. Whitestar auxiliary board 520-5068-01, which lotrGameData declares, "
            "exposes exactly three outputs at public 33-35."
        )},
        "provenance": {"source_refs": [MANUAL, PROFILE, CORE], "status": "validated"},
        # The auxiliary coils sit on their own board; the transcription records it at the group
        # level, so it has to be supplied here rather than read from the per-coil record.
        "wiring": {**coil_wiring(rec), "board": transcription["coil_table"]["auxiliary_uk_only"]["board"]},
    })
for power, callback, side, manual_addr in ((45, 46, "right", "#16"), (47, 48, "left", "#15")):
    rec = COILS[16 if side == "right" else 15]
    outputs.append({
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(power)}],
        "availability": "used",
        "binding": {"device": power, "group": "pinmame.output.solenoid"},
        "id": f"device.{side}-flipper-power-phase",
        "kind": "control_signal",
        "label": f"{side.capitalize()} Flipper Power Phase",
        "physical": {"notes": (
            f"Power-phase view of the same physical {side} flipper coil exposed at public {callback}. PinMAME "
            f"synthesizes the canonical callback's hold state whenever this power bit is active, so a recreation must "
            "drive one flipper device, not two."
        )},
        "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
        "spatial": not_applicable("internal_nonvisual", [PROFILE]),
    })
    outputs.append({
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(callback)},
                    {"namespace": "manual.address", "value": manual_addr}],
        "availability": "used",
        "binding": {"device": callback, "group": "pinmame.output.solenoid"},
        "id": f"device.{side}-flipper",
        "kind": "coil",
        "label": f"{side.capitalize()} Flipper",
        "physical": {"notes": (
            f"Printed coils chart entry {manual_addr} {rec['name']}. Whitestar removes the physical flipper coils from "
            f"public 15 and 16 and exposes this one at power-phase address {power} with canonical callback {callback}. "
            f"Printed coil type {rec.get('coil_spec')}."
        )},
        "provenance": {"source_refs": [MANUAL, PROFILE, CORE, S_VPW], "status": "validated"},
        "wiring": coil_wiring(rec),
    })

for address in range(1, 81):
    rec = LAMPS[address]
    device_id = f"lamp.matrix-{address}"
    column, row = (address - 1) % 8 + 1, (address - 1) // 8 + 1
    notes = [f"Printed lamp-matrix column {column}, row {row}. Printed bulb type {rec['bulb'].rstrip('.')}."]
    notes.append(
        "The printed matrix is drawn with the 18v feed as its columns and the ground drive as its rows; PinMAME's "
        "lamp column strobe corresponds to the printed ROW and its lamp row to the printed COLUMN, so the wiring "
        "block below names the drive line by the printed row and the return by the printed column."
    )
    if address in {60, 61, 62, 63}:
        notes.append(
            "Printed on the back panel. The printed backpanel inset draws 60 and 61 above 62 and 63, but none of the "
            "three retained recreations separates the upper pair from the lower: each models 60/62 and 61/63 at the "
            "same coordinate. The published position is therefore the column pair, not the individual bulb, and this "
            "lamp is recorded as observed rather than validated."
        )
    if rec.get("note"):
        notes.append(rec["note"] + ".")
    if rec.get("location"):
        notes.append(f"Printed location {rec['location']}.")
    roles = []
    if address == 79:
        roles = ["cabinet.button"]
        notes.append("Present only with the optional Tournament Kit.")
    if address == 80:
        roles = ["cabinet.start"]
    entry = {
        "aliases": [{"namespace": "pinmame.lamp", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "optional" if address == 79 else "used",
        "binding": {"device": address, "group": "pinmame.output.lamp"},
        "id": device_id,
        "kind": "lamp",
        "label": labelize(rec["name"]),
        "physical": {"notes": " ".join(notes), "quantity": 1},
        "provenance": {"source_refs": [MANUAL, CORE, PROFILE], "status": "validated"},
        "wiring": lamp_wiring(address),
    }
    if roles:
        entry["roles"] = roles
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        sp = spatial_of("lamp", address)
        if sp and address in {60, 61, 62, 63}:
            # No retained table resolves the printed 2x2; the coordinate identifies the pair.
            sp = {**sp, "status": "observed"}
        entry["spatial"] = located(device_id, "emitter", sp, (MANUAL,)) if sp else not_applicable("internal_nonvisual", [MANUAL])
    outputs.append(entry)

CONFLICTED_LED_POSITIONS = []
for address in range(81, 100):
    spatial = spatial_of("lamp", address)
    raw_spatial = consensus["devices"]["lamp"][str(address)]
    if spatial is None and raw_spatial.get("status") != "conflicted":
        raise SystemExit(f"script-bound retained tables produced no usable coordinate for public lamp {address}")
    emitter = address - 80
    device_id = f"lamp.led-board-{emitter:02d}"
    entry = {
        "aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
        "availability": "used",
        "binding": {"device": address, "group": "pinmame.output.lamp"},
        "id": device_id,
        "kind": "lamp",
        "label": f"19-LED Board Emitter {emitter:02d}",
        "physical": {
            "notes": (
                f"Emitter {emitter:02d} of playfield board 520-5242-00. PinMAME publishes it as lamp {address}. "
                "PinMAME identifies the board and its nineteen public outputs; all four retained scripts explicitly "
                "bind this address to a positioned light object, and the spatial resolver compares those bound "
                "objects without assuming that object numbering equals the public address. No factory semantic name "
                "or per-emitter connector pin is asserted, and the official manual is not claimed as LED-board evidence."
            ),
            "quantity": 1,
        },
        "provenance": {
            "source_refs": [CORE, PROFILE, S_VPW, S_JPS, S_HAN, T_NEO_LED],
            "status": "observed",
        },
    }
    if spatial is not None:
        entry["spatial"] = located(device_id, "emitter", spatial)
    else:
        CONFLICTED_LED_POSITIONS.append({
            "device": device_id,
            "address": address,
            "label": entry["label"],
            "measurements": raw_spatial["script_bound_measurements"],
        })
    outputs.append(entry)

outputs.append({
    "aliases": [{"namespace": "pinmame.gi", "value": "0"}],
    "availability": "used",
    "binding": {"device": 0, "group": "pinmame.output.gi"},
    "id": "gi.playfield-relay",
    "kind": "gi",
    "label": "General Illumination Relay",
    "physical": {"notes": (
        "PinMAME exposes Whitestar's general-illumination relay as a single aggregate channel. The cabinet itself has "
        "four separately fused 6.3v AC illumination strings, printed as F24 brown-white, F25 yellow, F26 green and F27 "
        "violet, all behind the one relay, so a recreation must not infer four controllable channels from the fuse chart."
    )},
    "provenance": {"source_refs": [MANUAL, PROFILE, CORE], "status": "validated"},
    "roles": ["internal.general-illumination"],
    "spatial": not_applicable("internal_nonvisual", [MANUAL, PROFILE]),
    "wiring": {"board": "I/O Power Driver Board", "voltage_type": "ac", "nominal_voltage_v": 6.3},
})

# Centralised so no device can silently lose its spatial evidence: anything the printed DR.7
# drawing places, that ended up without a spatial record, is recorded as unresolved exactly once.
_recorded = {row["device"] for row in UNPLACED} | {row["device"] for row in CONFLICTED_LED_POSITIONS}
for _device in outputs:
    _address = _device["binding"]["device"]
    if (_device["binding"]["group"] == "pinmame.output.solenoid"
            and _address in PRINTED_BUT_UNPLACED
            and "spatial" not in _device
            and _device["id"] not in _recorded):
        UNPLACED.append({"device": _device["id"], "address": _address, "label": _device["label"],
                         "printed_evidence": PRINTED_BUT_UNPLACED[_address]})
        _recorded.add(_device["id"])
# Any device that still carries no spatial record and was not deliberately left unresolved is a
# generator bug, not a curation decision. Both namespaces are checked here rather than only the
# one that happened to be under review, because the round-six fix was applied to outputs alone
# and the switch namespace kept shipping false `not_applicable` records for another whole round.
_unaccounted = [d["id"] for d in inputs + outputs if "spatial" not in d and d["id"] not in _recorded]
if _unaccounted:
    raise SystemExit(f"devices without spatial evidence and without an unresolved record: {_unaccounted}")

# And the converse: nothing the manual places may claim, on the manual's own authority, that it
# has no placeable position - whatever reason it gives, and in whichever namespace it lives.
#
# Round seven checked `inputs` only and only the `internal_nonvisual` reason. Both limits were
# holes. The printed lamp table places 60-63 and 73-78 on the Back Panel and 80 In Cabinet, and
# the coil chart places 26 and 27 on the Back Panel, so the output namespace has thirteen printed
# locations the rule never consulted; and because the cabinet/service branch runs before the
# location branch, one wrong entry in the hand-written role table could still route a
# playfield-printed device to `cabinet_or_service` with no guard firing. The join is by binding
# group so a DIP entry is never matched against the switch record that shares its number.
def _printed_record(entry: dict):
    """The printed table row for this device, or None if no printed table covers it."""
    group = entry["binding"]["group"]
    address = entry["binding"]["device"]
    if group == "pinmame.input.switch":
        manual_ref = next((a["value"] for a in entry.get("aliases", ()) if a["namespace"] == "manual.address"), None)
        return SW.get(address) or (DS.get(manual_ref) if manual_ref else None)
    if group == "pinmame.output.lamp":
        return LAMPS.get(address)
    if group == "pinmame.output.solenoid":
        return COILS.get(address)
    return None


_false_na = []
for _entry in inputs + outputs:
    _rec = _printed_record(_entry)
    if not _rec or _entry.get("availability") == "unused":
        continue
    _spatial = _entry.get("spatial")
    if (_spatial and _spatial.get("status") == "not_applicable"
            and printed_location_class(_rec.get("location")) == "playfield"):
        _false_na.append(f"{_entry['id']} ({_spatial.get('reason')})")
if _false_na:
    raise SystemExit(f"devices the printed table places, recorded not_applicable on the manual's authority: {_false_na}")

displays = [{
    "controller_index": 0,
    "height": 32,
    "id": "display.dmd",
    "kind": "dmd",
    "label": "128x32 dot-matrix display",
    "provenance": {"source_refs": [CORE, MANUAL, PROFILE], "status": "validated"},
    "spatial": not_applicable("cabinet_or_service", [CORE, MANUAL]),
    "width": 128,
}]

mechanisms = [
    {
        "actuators": ["device.trough-up-kicker"],
        "behavior": (
            "Four balls rest in the under-playfield trough on printed switches 11, 12 and 13 with the fourth position "
            "read by opto 14, the 4-Ball Trough VUK Opto at the eject end. Solenoid 1, the Trough Up-Kicker, lifts the "
            "ball at the eject end into the shooter lane, where switch 16 reads it. Printed switch 15, the 4-Ball "
            "Stacking Opto, watches the stack feeding the trough. The manual numbers the positions from the left, so "
            "printed Trough #1 is the position furthest from the shooter lane; the retained VPW script numbers its "
            "trough objects in the opposite order, which is a labelling difference and not a wiring disagreement. All "
            "three retained scripts initialise switches 11-14 closed at start of game because balls rest on them."
        ),
        "id": "mechanism.trough",
        "kind": "kicker",
        "label": "Four-ball trough and up-kicker",
        "positions": [
            {"description": "Trough position furthest from the shooter lane.", "id": "ball-1",
             "label": "4-Ball Trough #1 (Left)", "sensors": ["switch.matrix-11"]},
            {"description": "Second trough position.", "id": "ball-2", "label": "4-Ball Trough #2",
             "sensors": ["switch.matrix-12"]},
            {"description": "Third trough position.", "id": "ball-3", "label": "4-Ball Trough #3",
             "sensors": ["switch.matrix-13"]},
            {"description": "Opto at the eject end, read as the up-kicker lifts the ball.", "id": "eject",
             "label": "4-Ball Trough VUK Opto", "sensors": ["switch.matrix-14"]},
            {"description": "Opto watching the stack that feeds the trough.", "id": "stack",
             "label": "4-Ball Stacking Opto", "sensors": ["switch.matrix-15"]},
        ],
        "provenance": {"source_refs": [MANUAL, S_VPW, S_JPS, CORE], "status": "validated"},
        "sensors": ["switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-14", "switch.matrix-15", "switch.matrix-16"],
    },
    {
        "actuators": ["device.balrog-motor", "device.balrog-motor-relay"],
        "assembly_part_number": "041-5088-01",
        "behavior": (
            "The Balrog toy is driven by motor 041-5088-01 on printed solenoid 22, gated by the DC relay 520-5066-00 "
            "on printed solenoid 20. Printed switches 31 Balrog Open and 32 Balrog Closed read the two end positions "
            "and are mutually exclusive; the retained VPW script asserts one and clears the other as the motor runs. "
            "Printed switch 28 Balrog Hit is a separate above-playfield switch on the toy that registers a ball strike "
            "and is driven in the retained script from a wobble value rather than from the motor position, so a "
            "recreation must not derive it from the open or closed state."
        ),
        "id": "mechanism.balrog",
        "kind": "motorized",
        "label": "Balrog motorized toy",
        "positions": [
            {"description": "Toy driven to its open end position.", "id": "open", "label": "Balrog Open",
             "sensors": ["switch.matrix-31"]},
            {"description": "Toy driven to its closed end position.", "id": "closed", "label": "Balrog Closed",
             "sensors": ["switch.matrix-32"]},
        ],
        "provenance": {"source_refs": [MANUAL, S_VPW, S_JPS], "status": "validated"},
        "sensors": ["switch.matrix-28", "switch.matrix-31", "switch.matrix-32"],
    },
    {
        "actuators": ["device.sword-lock-release"],
        "behavior": (
            "Three above-playfield switches read balls held in the sword lock: printed 17 Sword Lock High, 18 Sword "
            "Lock Mid and 19 Sword Lock Low, all switch part 180-5119-02. Printed solenoid 21, the Sword Lock Release, "
            "frees the stack. The high position is the one furthest from the release coil."
        ),
        "id": "mechanism.sword-lock",
        "kind": "kicker",
        "label": "Sword ball lock",
        "positions": [
            {"description": "Ball held furthest from the release coil.", "id": "high", "label": "Sword Lock High",
             "sensors": ["switch.matrix-17"]},
            {"description": "Middle held ball.", "id": "mid", "label": "Sword Lock Mid", "sensors": ["switch.matrix-18"]},
            {"description": "Ball nearest the release coil.", "id": "low", "label": "Sword Lock Low",
             "sensors": ["switch.matrix-19"]},
        ],
        "provenance": {"source_refs": [MANUAL, S_VPW], "status": "validated"},
        "sensors": ["switch.matrix-17", "switch.matrix-18", "switch.matrix-19"],
    },
    {
        "actuators": ["device.ring-magnet"],
        "behavior": (
            "The One Ring on the back panel is held and released by the magnet on printed solenoid 6, which is the only "
            "output with its own fuse, printed F20 4A 250v slow-blow and marked THIS GAME ONLY in the quick reference "
            "fuse chart. Printed opto 47 Ring Made, on the back panel, reads a ball completing the ring. Printed "
            "solenoid 26 flashes the ring and 27 the back panel behind it."
        ),
        "id": "mechanism.ring-magnet",
        "kind": "toy",
        "label": "One Ring magnet and back panel",
        "provenance": {"source_refs": [MANUAL, S_VPW, CORE], "status": "validated"},
        # Only switch 47 belongs to this mechanism. Switch 48 is the Back Trough and was listed
        # here on proximity alone, which the runbook forbids.
        "sensors": ["switch.matrix-47"],
    },
    {
        "actuators": ["device.loop-diverter"],
        "behavior": (
            "Printed solenoid 8, the Loop Diverter, steers a ball out of the loop toward the left Orthanc tower. The "
            "manual carries a dedicated Diverter Gate Adjustment Procedure: with power off and the playfield raised, "
            "the crank-bar set screw is loosened, the paddle is held against the right flat rail to open the gate to "
            "the left tower, the plunger is pushed home, and the screw is retightened so the paddle rests as close to "
            "the left flat rail as possible without touching it. Printed switch 42 Inner Loop and the orbit switches "
            "20, 21, 37 and 38 read balls through the loop."
        ),
        "id": "mechanism.loop-diverter",
        "kind": "diverter",
        "label": "Loop diverter gate",
        "provenance": {"source_refs": [MANUAL, S_VPW], "status": "validated"},
        "sensors": ["switch.matrix-42", "switch.matrix-20", "switch.matrix-21", "switch.matrix-37", "switch.matrix-38"],
    },
    {
        "actuators": ["device.left-vuk", "device.top-vuk", "device.right-vuk", "device.top-saucer"],
        "behavior": (
            "Three vertical up-kickers and one saucer return balls to play. Printed solenoid 3 with switch 9 is the "
            "left VUK, printed solenoid 4 with opto 41 is the top VUK, printed solenoid 5 with switch 30 is the right "
            "VUK, and printed solenoid 19 with switch 46 is the top saucer. The retained VPW and JPSalas scripts label "
            "solenoid 4 Upper-Left VUK and solenoid 19 Upper-Right Kicker; the manual's Top VUK and Top Saucer are the "
            "printed names and control."
        ),
        "id": "mechanism.up-kickers",
        "kind": "kicker",
        "label": "Vertical up-kickers and top saucer",
        "positions": [
            {"description": "Left vertical up-kicker.", "id": "left-vuk", "label": "Left VUK", "sensors": ["switch.matrix-9"]},
            {"description": "Top vertical up-kicker, read by an opto.", "id": "top-vuk", "label": "Top VUK", "sensors": ["switch.matrix-41"]},
            {"description": "Right vertical up-kicker.", "id": "right-vuk", "label": "Right VUK", "sensors": ["switch.matrix-30"]},
            {"description": "Top saucer.", "id": "top-saucer", "label": "Top Saucer", "sensors": ["switch.matrix-46"]},
        ],
        "provenance": {"source_refs": [MANUAL, S_VPW, S_JPS], "status": "validated"},
        "sensors": ["switch.matrix-9", "switch.matrix-30", "switch.matrix-41", "switch.matrix-46"],
    },
    {
        "actuators": [],
        "behavior": (
            "A separate mini playfield carries four switches printed Mini PF U.L., U.R., L.L. and L.R. at addresses 33 "
            "to 36, all switch part 180-5057-00. The printed switch-location drawing shows the mini playfield moved off "
            "the main playfield for clarity, so its printed drawing position is not its installed position; the "
            "coordinates here come from the retained recreations."
        ),
        "id": "mechanism.mini-playfield",
        "kind": "other",
        "label": "Mini playfield",
        "provenance": {"source_refs": [MANUAL, S_VPW], "status": "validated"},
        "sensors": ["switch.matrix-33", "switch.matrix-34", "switch.matrix-35", "switch.matrix-36"],
    },
    {
        "actuators": ["device.uk-left-up-down-post", "device.uk-center-up-down-post", "device.uk-right-up-down-post"],
        "behavior": (
            "UK cabinets add three up and down posts driven from a UK 3X Transformer Driver Board and exposed on "
            "Whitestar auxiliary outputs 33, 34 and 35. The printed coil and flash lamp location drawing places Aux 1 "
            "at the left inlane area, Aux 2 between the flippers and Aux 3 at the right. These are absent from "
            "non-UK cabinets, as are the two cabinet-side buttons at printed switches 1 and 8."
        ),
        "id": "mechanism.uk-up-down-posts",
        "kind": "other",
        "label": "UK-only up/down posts",
        "provenance": {"source_refs": [MANUAL, PROFILE, CORE], "status": "validated"},
        "sensors": [],
    },
]

relationships = [
    {
        "destination": "device.right-flipper", "id": "relationship.right-flipper-power-phase", "kind": "direct",
        "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
        "source": "device.right-flipper-power-phase",
    },
    {
        "destination": "device.left-flipper", "id": "relationship.left-flipper-power-phase", "kind": "direct",
        "provenance": {"source_refs": [PROFILE, CORE], "status": "validated"},
        "source": "device.left-flipper-power-phase",
    },
    {
        "destination": "device.balrog-motor", "id": "relationship.balrog-motor-relay-gate", "kind": "relay_gated",
        "provenance": {"source_refs": [MANUAL, S_VPW], "status": "validated"},
        "source": "device.balrog-motor-relay",
    },
]
# No relationship is declared between the Balrog open and closed limit switches. An earlier
# revision declared them `inverted`, which asserts each is the logical complement of the other.
# The only basis was the retained script, which does keep exactly one of the pair asserted - but
# that is the recreation's two-state model, not evidence about the machine. Two end-of-travel
# switches can both be open while the drive is in transit, and nothing retained here observes the
# mechanism mid-travel. The vocabulary has no term for "mutually exclusive but not exhaustive",
# so the honest record is no relationship; the exclusivity is described in the Balrog mechanism's
# own behavior prose instead.
# No relationship is declared between the trough up-kicker and the shooter-lane switch. Coil 1
# does not actuate switch 16; it launches a ball that later rolls over it. That is a ball path,
# not causality, and the runbook names inventing it as an anti-pattern.

LANGUAGES = {"Spanish": "Spanish", "German": "German", "French": "French", "Italian": "Italian"}

# What actually differs between drivers is read out of pinned segames.c, not asserted. Round six
# said "only the CPU game ROM differs" for all 45 clones; round seven corrected the eight Spanish
# ones and left the sentence wrong on the other 36, which is the same mistake twice. Parsing the
# ROM sets removes the opportunity: the prose below is a description of this table, so it cannot
# be right for the drivers someone looked at and wrong for the ones they did not.

SPANISH_SOUND_DRIVERS = {name for name, (_, _, snd) in ROM_SETS.items() if snd == "LOTR_SND_SP"}


def rom_delta(driver_id: str) -> str:
    """Say exactly which ROMs differ from the root, by comparing the parsed sets.

    Never say "only the X differs" from a template. The real structure has four shapes and the
    round-six/round-seven prose got three of them wrong: a German, French or Italian release
    shares its English sibling's CPU ROM byte for byte and differs only in the display ROM; an
    English revision differs in CPU *and* display; a Spanish release differs in CPU, display and
    the whole sound set; and the Limited Edition differs in CPU alone.
    """
    root_cpu, root_display, root_sound = ROM_SETS["lotr"]
    cpu, display, sound = ROM_SETS[driver_id]
    differs = ([f"the CPU game ROM ({cpu} against the root's {root_cpu})"] if cpu != root_cpu else [])
    differs += ([f"the display ROM ({display} against {root_display})"] if display != root_display else [])
    differs += ([f"the whole five-ROM sound set ({sound} against {root_sound})"] if sound != root_sound else [])
    if not differs:
        return "It carries the root's exact CPU, display and sound ROMs."
    listed = differs[0] if len(differs) == 1 else ", ".join(differs[:-1]) + " and " + differs[-1]
    unchanged = [name for name, same in (("CPU game ROM", cpu == root_cpu),
                                         ("display ROM", display == root_display),
                                         ("sound ROM set", sound == root_sound)) if same]
    tail = f" It shares the root's {' and '.join(unchanged)}." if unchanged else ""
    return f"Against the root driver it differs in {listed}.{tail}"


ENGLISH_DRIVERS = {"lotr", "lotr3", "lotr4", "lotr41", "lotr5", "lotr51", "lotr6", "lotr7", "lotr8", "lotr9"}


def english_sibling(driver_id: str) -> str:
    """Name the English driver this language release shares a CPU ROM with, if there is one.

    Derived, not asserted: a German release at revision 9.00 shares `lotrcpu.900` with `lotr9`,
    which is a different statement from how it compares with the root, and writing both by hand
    produced a note that contradicted itself.
    """
    cpu = ROM_SETS[driver_id][0]
    siblings = sorted(name for name in ENGLISH_DRIVERS if ROM_SETS[name][0] == cpu)
    if not siblings:
        return "its CPU game ROM is its own, shared with no English release."
    return (f"it runs the CPU game ROM of its English sibling {siblings[0]} ({cpu}) byte for byte, "
            "so the display ROM is the only difference between the two.")


def variant_notes(record: dict) -> str:
    description = record.get("description", "")
    revision = description.partition("(")[2].partition(")")[0]
    language = next((name for name in LANGUAGES if name in description), None)
    common = (
        "The switch matrix, lamp matrix, coil complement and playfield hardware are unchanged. "
        + rom_delta(record["id"])
    )
    if record["id"] == "lotr":
        return (
            "Stern production game ROM revision 10.00, the English release PinMAME uses as the root driver for this "
            "physical machine. lotrGameData is shared by every clone in the tree, so all of them present the same "
            "Whitestar hardware."
        )
    if record["id"] == "lotr_le":
        return (
            "Stern game ROM revision 10.02 shipped with the 2008 Limited Edition run. PinMAME defines it as a clone of "
            f"lotr sharing init_lotr, so nothing in the EMULATED hardware differs - a statement about driver "
            f"routing, not about the cabinet. {rom_delta(record['id'])} Whether this limited run differs "
            "physically from the 2003 production machine is not established by anything retained here, and a "
            "limited run is exactly where a manufacturer adds hardware such as a shaker motor. "
            "physical_compatibility is therefore `unknown` for this driver alone, rather than asserting an "
            "identity the evidence does not carry."
        )
    if language:
        if record["id"] in SPANISH_SOUND_DRIVERS:
            return (
                f"Stern {language} release, game ROM revision {revision.split()[0]}. The {language.lower()} text is "
                "carried by a separate display ROM, and this release also carries its own five-ROM sound set: pinned "
                "segames.c gives it LOTR_SND_SP (lotrlu7.100, lotrlu17.100, lotrlu21.100, lotrlu36.100, lotrlu37.100) "
                "where every other driver in the tree takes LOTR_SND. Unlike the German, French and Italian releases, "
                f"which share their English sibling's CPU ROM byte for byte, {english_sibling(record['id'])} "
                "The switch matrix, lamp matrix, coil complement and playfield hardware are unchanged. "
                f"{rom_delta(record['id'])}"
            )
        return (
            f"Stern {language} release, game ROM revision {revision.split()[0]}. The {language.lower()} text is carried "
            f"by a separate display ROM; {english_sibling(record['id'])} " + common
        )
    return f"Stern game ROM revision {revision.split()[0] if revision else 'unknown'} for the same physical machine. {common}"


drivers = []
for record in partial["drivers"]:
    entry = dict(record)
    # `identical` is a claim about the PHYSICAL machine, and shared init_lotr proves only that the
    # emulated hardware matches. For ordinary firmware revisions and language releases those are
    # the same thing in practice. They are not for a limited run, which is exactly where a
    # manufacturer adds hardware, and nothing retained here documents that cabinet.
    entry["physical_compatibility"] = "unknown" if record["id"] == "lotr_le" else "identical"
    entry["variant_notes"] = variant_notes(record)
    drivers.append(entry)

# Every driver in the tree must have a parsed ROM set, and the Spanish sound set must be exactly
# the Spanish releases. Round six asserted a ROM-composition sentence for all 45 clones and round
# seven fixed only the eight that had been reviewed; the point of these guards is that the prose
# above is now generated from ROM_SETS, so a driver the reviewer never looked at cannot carry a
# different claim from the one the source supports.
_driver_ids = {d["id"] for d in drivers}
_unparsed = sorted(_driver_ids - set(ROM_SETS))
if _unparsed:
    raise SystemExit(f"drivers with no ROM set parsed out of segames.c: {_unparsed}")
_mislabelled = [d["id"] for d in drivers
                if (d["id"] in SPANISH_SOUND_DRIVERS) != ("Spanish" in d.get("description", ""))]
if _mislabelled:
    raise SystemExit(f"Spanish sound-ROM set does not match the Spanish releases: {_mislabelled}")
# No driver's note may claim a ROM differs that does not, or stay silent about one that does.
_root_set = ROM_SETS["lotr"]
for _driver in drivers:
    _cpu, _display, _sound = ROM_SETS[_driver["id"]]
    _note = _driver["variant_notes"]
    for _rom, _same, _phrase in ((_cpu, _cpu == _root_set[0], "CPU"),
                                 (_display, _display == _root_set[1], "display"),
                                 (_sound, _sound == _root_set[2], "sound")):
        if _driver["id"] == "lotr":
            continue
        # No exemption. Round eight carved the Spanish drivers out of this guard - the exact
        # class whose prose was wrong in round six and again in round seven - so the guard could
        # not see the only defect it had ever been needed for. A cross-provider review proved it
        # by making lotr_sp9 claim "No driver ROM changes" and watching generation succeed.
        if not _same and _rom not in _note:
            raise SystemExit(f"{_driver['id']}: {_phrase} ROM {_rom} differs from the root but the note does not name it")

definition = {
    "conflicts": [
        {
            "description": (
                "The controller profile pinmame.whitestar declares inversion_applied_by_emulator: true as a platform "
                "capability. For this driver pinned PinMAME applies none: lotrGameData's positional aggregate "
                "initializer (segames.c:1498, {GEN_WS, se_dmd128x32, {...}}) never sets the trailing wpc member, so "
                "core_gameData->wpc.invSw is all-zero, and core.c:2455 copies those zeros into coreGlobals.invSw "
                "unchanged. No SE/Whitestar game table in segames.c assigns wpc.invSw, so this is a platform-wide "
                "fact rather than a defect specific to this game, and it matches what the Simpsons Pinball Party "
                "curation recorded under this same conflict id. Three of this machine's four printed optos are "
                "nonetheless settled here by observation rather than left open: the retained known-working VPW 1.6 "
                "script drives switches 14, 41 and 47 through direct assert/release pairs that are unambiguous about "
                "sense, and it is known-working on the ball trough, where a reversed opto would fail first. Switch 15 "
                "(4-ball Stacking Opto) is the one address with no such evidence -- the VPW table handles stacking "
                "through its own bookkeeping without a Controller.Switch call for 15, and neither the jpsalas nor the "
                "Hanibal table binds 14 or 15 at all -- so whether a consumer must invert the public state it presents "
                "for switch 15 cannot be settled from the manual (which states construction, not public polarity), "
                "from the retained recreations, or from pinned PinMAME (which asserts no inversion at all). Resolution "
                "path: a LibPinMAME gameplay-harness trace of a legal lotr ROM observing the idle public state of "
                "switch 15 with and without a ball resting on the stack. Unresolved."
            ),
            "id": "conflict.whitestar-invsw-never-populated",
            "path": "controller.inversion_applied_by_emulator; inputs[binding.device=15]",
            "source_refs": [CORE, MANUAL, S_VPW],
        },
    ],
    "controller": {"inversion_applied_by_emulator": True, "platform": "pinmame.whitestar"},
    "coverage": {
        # Held at partial. lotrGameData declares SE_BOARDID_520_5242_00, the printed
        # "Lord of The Rings 19 LED Board", and se.c drives public lamps 81-99 through it
        # (CORE_MODOUT_LAMP0 + 80/+88/+96, the last masked 0x07). Those Whitestar addresses
        # enumerate the real emitters through the ordinary lamp binding group.
        # Their address-to-position map is compared across every retained script's actual binding;
        # disagreement remains explicit, and no factory per-emitter semantic names or connector
        # pins are known.
        # physical_wiring is `conflicted` rather than `validated` because of switch 15: every
        # connector, wire colour, driver transistor and return IC is manual-verified, but one
        # printed opto's public polarity is unsettled. That follows the convention Monster Bash
        # and Simpsons Pinball Party already set for an open polarity question.
        "dimensions": {
            "address_enumeration": "validated", "catalog_identity": "validated", "mechanisms": "validated",
            "physical_wiring": "conflicted", "recreation_knowledge": "validated", "semantic_naming": "observed",
            "spatial_placement": "observed", "variant_coverage": "observed",
        },
        # `polarity` and `unresolved_conflicts` are switch 15, the one opto no retained recreation
        # binds. Spatial placement remains incomplete because many positions are observed rather
        # than corroborated and fifteen printed devices are still unplaced. `variant_coverage`
        # keeps the 2008 Limited Edition honest until its physical compatibility is sourced.
        "missing": [
            "polarity", "spatial_placement", "unresolved_conflicts", "variant_differences",
        ],
        "status": "partial",
    },
    "displays": displays,
    "drivers": drivers,
    "format": partial["format"],
    "inputs": inputs,
    "knowledge": {"path": "knowledge/stern/lord-of-the-rings-2003.md", "status": "partial"},
    "machine": {**partial["machine"], "kind": "physical_pinball", "ipdb_id": 4858},
    "mechanisms": mechanisms,
    "outputs": outputs,
    "relationships": relationships,
    "schema_version": 2,
    "sources": SOURCES,
}

# --- derived artifacts: report and knowledge note ----------------------------------------
# Both are generated from the same objects that produced the definition. Every count, list and
# status below is computed, so a statement cannot survive here after the data behind it changes.
def _spatial_rows(status_wanted):
    return [
        {
            "id": device["id"],
            "address": device["binding"]["device"],
            "label": device["label"],
            "supporting_tables": sorted({
                ref for place in device["spatial"].get("placements", [])
                for ref in place["provenance"]["source_refs"] if ref.startswith("vpx-table.")
            }),
        }
        for collection in ("inputs", "outputs")
        for device in definition[collection]
        if device.get("spatial", {}).get("status") == status_wanted
    ]


observed_rows = _spatial_rows("observed")
validated_rows = _spatial_rows("validated")
placement_total = sum(len(d.get("spatial", {}).get("placements", [])) for d in definition["inputs"] + definition["outputs"])
computed_rows = [
    {"kind": kind, "address": int(address), "x": entry["x"], "y": entry["y"],
     "derived_from": entry.get("derived_from", []), "resolution": entry.get("resolution")}
    for kind, bucket in consensus["devices"].items()
    for address, entry in bucket.items()
    if entry.get("coordinate_origin") == "computed"
]
rejected_rows = [
    {"kind": kind, "address": int(address), "accepted": {"x": entry["x"], "y": entry["y"]},
     "accepted_tables": entry.get("agreeing_tables", []), "rejected": entry["outliers"]}
    for kind, bucket in consensus["devices"].items()
    for address, entry in bucket.items()
    if entry.get("outliers")
]
projection_ids = {p["device"] for p in PROJECTIONS}
CO_LOCATED_INSERT_LAMPS = {f"lamp.matrix-{address}" for address in (60, 61, 62, 63)}

# Partition the observed set exactly, so the report can describe it without a hand-typed join.
# Every observed placement falls into exactly one bucket and the buckets sum to the total.
#
# The bucket name has to state the number it means. Round six named these `*_two_tables` on the
# strength of `len(supporting_tables) < 2`, which quietly filed every three-table row under "two"
# - 13 of the 50, including five projections all three tables agree on. Count the support, then
# say the count.
_SUPPORT_WORDS = {1: "one_table", 2: "two_tables", 3: "three_tables", 4: "four_tables"}
_partition: dict[str, list] = {f"{kind}_{word}": []
                               for kind in ("projection", "measured")
                               for word in _SUPPORT_WORDS.values()}
for row in observed_rows:
    kind = "projection" if row["id"] in projection_ids else "measured"
    support = len(row["supporting_tables"])
    if support not in _SUPPORT_WORDS:
        raise SystemExit(f"{row['id']} has {support} supporting tables, which no bucket name describes")
    _partition[f"{kind}_{_SUPPORT_WORDS[support]}"].append(row["id"])
observed_partition = {name: sorted(ids) for name, ids in _partition.items() if ids}
assert sum(len(v) for v in observed_partition.values()) == len(observed_rows)

# Why each row is observed rather than validated. There are three distinct reasons and they are
# not interchangeable: round six stated the "fewer than all three agree" one uniformly, which was
# wrong for the nine rows all three tables do agree on.
_reasons: dict[str, list] = {"projection_never_promoted": [], "co_located_insert_pair": [],
                             "computed_from_disagreeing_tables": [], "computed_within_one_table": [],
                             "incomplete_table_agreement": []}
for row in observed_rows:
    if row["id"] in projection_ids:
        _reasons["projection_never_promoted"].append(row["id"])
    elif row["id"] in CO_LOCATED_INSERT_LAMPS:
        _reasons["co_located_insert_pair"].append(row["id"])
    elif row["id"] in COMPUTED_ACROSS_TABLES:
        # A per-axis median. Every contributing table fed it, none agreed within threshold.
        _reasons["computed_from_disagreeing_tables"].append(row["id"])
    elif row["id"] in COMPUTED_WITHIN_ONE_TABLE:
        # A centroid of co-located bodies inside one table. No disagreement involved.
        _reasons["computed_within_one_table"].append(row["id"])
    else:
        _reasons["incomplete_table_agreement"].append(row["id"])
observed_reasons = {name: sorted(ids) for name, ids in _reasons.items() if ids}
assert sum(len(v) for v in observed_reasons.values()) == len(observed_rows)
FACTORY_TABLE_REFS = {T_VPW, T_JPS, T_HAN}
_wrongly_blamed = [row["id"] for row in observed_rows
                   if row["id"] in set(observed_reasons.get("incomplete_table_agreement", ()))
                   and FACTORY_TABLE_REFS <= set(row["supporting_tables"])]
if _wrongly_blamed:
    raise SystemExit(f"rows blamed on incomplete agreement that all three factory tables support: {_wrongly_blamed}")
# The disagreeing-tables sentence says all three tables appear in the row's source_refs. Prove it
# of every row filed under it: round seven put a one-table centroid in that bucket.
_not_really_disagreeing = [row["id"] for row in observed_rows
                           if row["id"] in set(observed_reasons.get("computed_from_disagreeing_tables", ()))
                           and len(row["supporting_tables"]) < 2]
if _not_really_disagreeing:
    raise SystemExit(f"rows blamed on disagreeing tables with fewer than two supporting tables: {_not_really_disagreeing}")
single_table_rows = [row for row in observed_rows if len(row["supporting_tables"]) < 2]
projection_rows = [row for row in observed_rows if row["id"] in projection_ids]
_REASON_TEXT = {
    "incomplete_table_agreement": "because fewer than all three factory-layout recreations agree on them",
    "projection_never_promoted": "because they are projections onto a co-located anchor and a projection is never promoted however well the tables agree",
    "computed_from_disagreeing_tables": "because the coordinate is a per-axis median of tables that disagreed, so every contributing table appears in its source_refs while none holds the published position",
    "computed_within_one_table": "because the coordinate is a centroid of co-located bodies inside a single table",
    "co_located_insert_pair": "because no retained table separates the printed back-panel insert pairs, so the published coordinate is the pair rather than the bulb",
}
_reason_summary = "; ".join(
    f"{len(observed_reasons[name])} {_REASON_TEXT[name]}" for name in _REASON_TEXT if name in observed_reasons
)

# Which table each rejection actually rejects, and which of them the VPW artwork explains. Round
# six attributed all 22 to VPW's rune ring; only the lamp rows where VPW is the sole outlier are
# the artwork's doing.
_rejections_by_table: dict[str, int] = {
    "vpw-1-6": 0, "jpsalas-600": 0, "hanibal-4k": 0, "neo-led-1-0-3": 0,
}
for _row in rejected_rows:
    for _entry in _row["rejected"]:
        _rejections_by_table[_entry["table"]] += 1
_vpw_only_lamp_rejections = sorted(
    row["address"] for row in rejected_rows
    if row["kind"] == "lamp" and {entry["table"] for entry in row["rejected"]} == {"vpw-1-6"}
)
conflicted_led_rows = sorted(CONFLICTED_LED_POSITIONS, key=lambda row: row["address"])


def _format_addresses(addresses: list[int]) -> str:
    """Render a sorted address list as runs, so the prose cannot claim a range it does not cover."""
    runs, start = [], None
    for index, address in enumerate(addresses):
        if start is None:
            start = address
        if index + 1 == len(addresses) or addresses[index + 1] != address + 1:
            runs.append(str(start) if start == address else f"{start}-{address}")
            start = None
    return ", ".join(runs)


# The VPW locator has to name the lamps actually rejected against it, not a range typed from
# memory. Round six said "lamps 9-17, those nine coordinates"; lamp 6 is rejected too.
_vpw_source = next(s for s in SOURCES if s["id"] == T_VPW)
assert "VPW_REJECTED_LAMPS" in _vpw_source["locator"]
_vpw_source["locator"] = _vpw_source["locator"].replace(
    "VPW_REJECTED_LAMPS",
    f"The {len(_vpw_only_lamp_rejections)} lamp coordinates where this table alone is the outlier - "
    f"{_format_addresses(_vpw_only_lamp_rejections)} - were therefore not taken from it.",
)

spatial_report = {
    "format": "pinmame-spatial-blockers",
    "version": 1,
    "machine_id": "stern.lord-of-the-rings.2003",
    "status": definition["coverage"]["status"],
    "placement_count": placement_total,
    "coordinate_convention": {
        "space": "playfield", "x": "0 left, 1 right", "y": "0 rear, 1 front",
        "normalization": "each table's own gamedata bounds",
        "precision": "at most six fractional decimal places",
    },
    "method": {
        "retained_recreations": len(consensus["tables"]),
        "agreement_threshold": consensus["agreement_threshold"],
        "rule": (
            "A lamp, switch or flasher placement is validated only when all three factory-layout tables agree "
            "within the threshold. Lamps 81-99 are resolved through each table script's explicit binding rather "
            "than object names; the Neo LED table is a disclosed derivative supplemental measurement and cannot "
            "promote a coordinate by itself."
        ),
        "why_all_three": (
            "Independence between the three recreations is unestablished and the two available signals disagree. "
            "Measured: the JPSalas and Hanibal tables agree with each other to within 0.0155 on every lamp both "
            "model, while either differs from VPW by up to 0.187. Documented: VPW credits an 'EBIsLit - Baseline "
            "playfield scan' and JPSalas records its playfield as 'based on Ebislit's playfield', while Hanibal "
            "declares only \"4k Mod\" in its title and names no baseline. The measured clustering pairs JPSalas with "
            "Hanibal; the documented ancestry pairs "
            "VPW with JPSalas. Requiring all three removes the need to guess which signal describes the lineage."
        ),
        "artwork_caveat": (
            "The VPW table identifies itself as 'Lord Of The Rings - Valinor Edition' with original artwork, so "
            "where its insert layout departs from the printed diagrams that is an artwork difference, not an error."
        ),
        "tables": {label: dict(data) for label, data in consensus["tables"].items()},
    },
    "counts": {
        "validated_devices": len(validated_rows),
        "observed_devices": len(observed_rows),
        "single_table_devices": len(single_table_rows),
        "projected_devices": len(projection_rows),
        "computed_coordinates": len(computed_rows),
        "rejected_measurements": len(rejected_rows),
        "conflicting_led_positions": len(conflicted_led_rows),
    },
    "blockers": [
        {
            "id": "placements-not-fully-corroborated",
            "severity": "minor",
            "summary": (
                f"{len(observed_rows)} device spatial records are observed rather than validated: {_reason_summary}. "
                "reason_partition names which device records each reason covers; support_partition counts "
                "how many tables appear in each row's source_refs, which for the computed rows is a count of "
                "contributors and not a count of agreement. Both are disjoint and sum to the total."
            ),
            "reason_partition": {name: len(ids) for name, ids in observed_reasons.items()},
            "support_partition": {name: len(ids) for name, ids in observed_partition.items()},
            "devices": observed_rows,
        },
        {
            "id": "script-bound-led-positions-conflict",
            "severity": "major",
            "summary": (
                f"{len(conflicted_led_rows)} of the nineteen LED-board addresses have no published coordinate because "
                "the four retained scripts bind them to genuinely different positions with no two-table cluster "
                "inside the 0.025 threshold. Each script-derived address-to-object mapping and normalized measurement "
                "is retained below; no object-name guess or arbitrary table winner is substituted."
            ),
            "devices": conflicted_led_rows,
        },
        {
            "id": "devices-printed-but-unplaced",
            "severity": "major",
            "summary": (
                f"{len(UNPLACED)} devices are printed with a position on the DR.7 location drawing but modelled by no "
                "retained recreation, so they carry no spatial evidence at all. They are not recorded as "
                "not_applicable: the manual places them, and asserting otherwise on the manual's own authority would "
                "be false."
            ),
            "devices": sorted(UNPLACED, key=lambda row: row["address"]),
        },
    ],
    "observed_partition": observed_partition,
    "observed_reasons": observed_reasons,
    "conflicted_led_positions": conflicted_led_rows,
    "unplaced_devices": sorted(UNPLACED, key=lambda row: row["address"]),
    "projections": PROJECTIONS,
    "computed_coordinates": computed_rows,
    "rejected_measurements": rejected_rows,
    "excluded_object_classes": [
        "JPSalas f<N>l helper Lights, which are non-positional and parked together at one coordinate",
        "primitive origins left at (0,0) because their transform is baked into mesh vertices",
    ],
    "unresolved": [],
    "promotion_decision": (
        "Not promoted. Held at partial with "
        + ", ".join(definition["coverage"]["missing"])
        + " declared missing."
    ),
}

# Derived from the blocker list rather than typed beside it, so the two can never disagree. They
# did: round six listed two unresolved items against three blockers, and the one it left out was
# the major printed-but-unplaced blocker.
spatial_report["unresolved"] = [blocker["summary"] for blocker in spatial_report["blockers"]]

_unused_switches = sorted(a for a, r in SW.items() if r.get("state") == "not_used")
_unused_coils = sorted(a for a, r in COILS.items() if r.get("state") == "not_used")
_optos = sorted(OPTOS)
_mech_lines = "\n".join(f"- **{m['label']}.** {m['behavior']}" for m in definition["mechanisms"])
_anomaly_lines = "\n".join(f"- {a['detail']}" for a in transcription["source_anomalies"])

knowledge_note = f"""# The Lord of the Rings (Stern, 2003)

Coverage: **{definition['coverage']['status']} - manual-verified semantic I/O, mechanism inventory and behaviour, the complete public output inventory including board 520-5242-00 at lamps 81-99, and normalized placements; held below author-ready because switch 15's public opto polarity is unestablished, spatial evidence is not fully corroborated, five LED-board addresses have conflicting positions, fifteen printed devices remain unplaced, and the 2008 Limited Edition's physical compatibility is not yet sourced**

## Identity and evidence precedence

Whitestar machine. PinMAME roots the family at `lotr` with {len(definition['drivers'])} drivers: English revisions, the 10.02 Limited Edition re-run, and Spanish, German, French and Italian releases. Every clone shares `init_lotr` and therefore the same emulator routing through `lotrGameData`. That does **not** prove identical physical hardware: `lotr_le` is a 2008 Limited Edition re-run whose physical compatibility remains unknown. ROM differences are read out of pinned `segames.c` per driver rather than summarized from names. There are four software shapes:

- **A German, French or Italian release runs its English sibling's CPU game ROM byte for byte** and differs only in the display ROM. `lotr`, `lotr_fr`, `lotr_gr` and `lotr_it` all take `lotrcpua.a00`; only `lotrdsp{{a,f,g,i}}.a00` differ. The same holds at every revision.
- **An English revision differs in CPU and display both** - `lotr9` is `lotrcpu.900` with `lotrdspa.900` against the root's `lotrcpua.a00` and `lotrdspa.a00`.
- **A Spanish release differs in all three.** It has its own CPU family `lotrcpul.*`, its own display `lotrdspl.*`, and the only other sound set in the tree: `LOTR_SND_SP`, five ROMs, against `LOTR_SND` for the other {len(definition['drivers']) - len(SPANISH_SOUND_DRIVERS)} drivers.
- **The Limited Edition differs in CPU alone** - `lotrcpua.a02`, sharing the root's display and sound.

Physical inventory authority is the **Stern English service manual**, IPDB machine 4858, an image-only 184-page scan with no text layer, so every printed table was read from pages rendered at 300 dpi. Runtime authority is the retained known-working script set; four recreations were retained and all run `cGameName = "lotr"`.

## The 520-5242-00 LED board: nineteen separately addressable emitters

`lotrGameData` declares two board identifiers. The second, `SE_BOARDID_520_5242_00`, is named in `src/wpc/se.h` in plain words: **"Lord of The Rings 19 LED Board"**. `se.c` drives it through `core_set_pwm_output_led_vfd(CORE_MODOUT_LAMP0 + 80, 3 * 8, CORE_MODOUT_LED, 4.f / 2.f)` and writes at `CORE_MODOUT_LAMP0 + 80`, `+ 88` and `+ 96` masked `0x07` - public lamp addresses **81 to 99**, nineteen LEDs. So `lampCol = 5` is not slack: it is 64 base lamps, the two auxiliary matrix columns at 65-80, and room for that board.

All four retained known-working scripts drive them. The controller profile exposes them after the 1-80 matrix through the same PinMAME lamp transport. All nineteen are enumerated as emitters 01-19 at public addresses 81-99; allocation slots 100-104 are not physical devices. Their normalized positions are compared through each script's explicit address-to-object binding rather than by assuming an `l<N>` object's suffix is its public address: that distinction matters because Hanibal reverses and permutes the object numbers. The Neo table's own info and script disclose its JPSalas lineage, so it is a supplemental measurement rather than independent corroboration. Fourteen addresses have an observed coordinate supported by a retained-table cluster; addresses {', '.join(str(row['address']) for row in conflicted_led_rows)} have none because no two script-bound measurements agree inside the threshold. No factory per-emitter semantic name or connector pin is invented, and the manual is not cited for evidence it does not contain.

## Addresses that are synthetic, mirrored or reserved

- Public 45 and 47 are the power-phase view of the same physical coils exposed at 46 and 48. Binding both halves creates two flippers where the machine has one.
- Public 15 is PinMAME's synthetic fast-flip and game-on state; 16 is its unused companion.
- Whitestar auxiliary board 520-5068-01 exposes three outputs, so 33, 34 and 35 carry the UK-only up/down posts and 36 is unused.
- General illumination is a **single aggregate channel 0**, although the cabinet has four separately fused 6.3v strings. A recreation must not infer four controllable channels from the fuse chart.

## Opto polarity: PinMAME normalizes nothing here

The controller profile declares `inversion_applied_by_emulator: true` as a platform capability, and for this driver pinned PinMAME exercises none of it. `lotrGameData` (`segames.c:1498`) is a positional aggregate that sets only `GEN_WS`, the display layout and the `hw` struct; the trailing `wpc` member - which is where `invSw` lives - is left at C zero-initialization, and `core.c:2455` memcpy's those zeros into the live `coreGlobals.invSw`. **The four printed optos are therefore published exactly as a recreation asserts them, and the ROM's own firmware accounts for the beam resting made.** An earlier pass of this definition said "PinMAME normalizes the public state", which arrived at the right instruction for a recreation by way of a mechanism that does not exist.

Three of the four are settled by observation rather than by argument. The retained known-working VPW 1.6 script asserts switches {_format_addresses(sorted(SCRIPT_EVIDENCED_OPTOS))} when a ball is present, through direct assert/release pairs whose sense is unambiguous - and it is known-working on the ball trough, which is exactly where a reversed opto fails first. Switch 15 is the exception: no retained recreation binds it at all (the VPW table does its stacking bookkeeping without a `Controller.Switch(15)` call, and neither alt table binds 14 or 15), so the public sense the ROM expects there is genuinely unestablished and is carried as `conflict.whitestar-invsw-never-populated` rather than guessed from its sibling.

`normally_closed: true` on these four records describes the physical contact, not the public state. Do not read it as a polarity instruction.

## Custom mechanisms

{_mech_lines}

## How coordinates were resolved

Four recreations were retained. Three factory-layout tables are treated as three measurements: a lamp, switch or flasher placement is `validated` only when **all three agree** within {consensus['agreement_threshold']} normalized units. The fourth Neo LED recreation is a disclosed JPSalas derivative and contributes only a supplemental measurement for addresses 81-99. Every one of those addresses is resolved through each table script's own binding; fourteen positions remain `observed` and five remain unpublished conflicts. Overall, {len(observed_rows)} device spatial records are observed against {len(validated_rows)} validated, with {placement_total} physical placements in total because one output can drive multiple emitters.

That threshold is deliberately conservative because **independence between the three is unestablished and the two available signals disagree**. Measured, the JPSalas and Hanibal tables agree with each other to within 0.0155 on every lamp both model while either differs from VPW by up to 0.187. Documented, VPW credits an "EBIsLit - Baseline playfield scan" and JPSalas records its playfield as "based on Ebislit's playfield", while Hanibal declares only "4k Mod" in its title and names no baseline. The measured clustering pairs JPSalas with Hanibal; the documented ancestry pairs VPW with JPSalas. No lineage model is asserted.

The VPW table identifies itself as **"Lord Of The Rings - Valinor Edition"** with original artwork, so where its insert layout departs from the printed diagrams that is an artwork difference rather than an error. Its Fellowship inserts form a closed ring of runes rather than the printed arc of named characters, which accounts for {len(_vpw_only_lamp_rejections)} of the {len(rejected_rows)} rejected measurements - lamps {_format_addresses(_vpw_only_lamp_rejections)}, where VPW alone is the outlier. Across all {len(rejected_rows)} rows the rejected measurement is VPW's {_rejections_by_table['vpw-1-6']} times, Hanibal's {_rejections_by_table['hanibal-4k']} times, JPSalas's {_rejections_by_table['jpsalas-600']} times and Neo's {_rejections_by_table['neo-led-1-0-3']} times. Neo participates only for addresses 81-99 and its disclosed JPSalas lineage means its agreement is supplemental, not an independent vote.

Public flasher 25 is not a single-point device. All three retained factory-layout scripts bind all three physical bulbs, and the resolver groups their co-located rendering objects into left, right and bottom emitter measurements before consensus. Every emitter is independently `validated` by all three tables; none is a projection or a rejected alternate measurement.

**{len(PROJECTIONS)} placements across {len(projection_rows)} device records are projections**, not measurements: each takes the coordinate of a co-located device the printed DR.7 diagram places beside it. Be precise about why. The resolver searches the three tables for `l<N>`, `sw<N>` and configured flasher objects only, so no coil search was ever run and this is not a finding that the tables model no coils - it is that the resolver has no coil group and the projection therefore stands on the printed diagram alone. Every one is `observed` and listed with its anchor in the spatial report. **{len(computed_rows)} coordinates are computed** rather than held by any table - per-axis medians of tables that disagreed - and each is marked `coordinate_origin: computed` with the tables it was derived from.

## Notable printed details

- Optos, which rest closed, are switches {", ".join(str(a) for a in _optos)}.
- Printed NOT USED: matrix switches {", ".join(str(a) for a in _unused_switches)}; dedicated switch DS-5; solenoids {", ".join(str(a) for a in _unused_coils)}.
- The ring magnet on coil 6 is the only output with its own fuse, printed F20 and marked THIS GAME ONLY.
- The lamp matrix axes are transposed between the manual and PinMAME: PinMAME's lamp column strobe corresponds to the printed **row** and its lamp row to the printed **column**. Do not map them by name.

## Preserved source anomalies

{_anomaly_lines}

## Recreation guidance

Bind the flippers once, at 46 and 48. Enumerate the dedicated switches at their negative and 81-84 addresses rather than folding them into the matrix. Treat GI as one channel. Model the trough with the printed numbering, remembering that printed Trough #1 is furthest from the shooter lane. Drive Balrog Hit from a collision, not from the toy's position. The 8x10 matrix occupies 1-80 and the nineteen-emitter board occupies 81-99 on the same lamp transport; do not invent anything at 100-104, which is allocation space rather than physical hardware.
"""


def build() -> dict:
	"""Return the canonical definition assembled from the embedded literals."""
	return definition


def _definition_bytes() -> bytes:
	"""The exact bytes write_json produces for the definition.

	Comparing canonical JSON instead would accept any reformatting of the canonical artifact,
	which is the weakest link this gate previously had: the prose was byte-locked while the
	product was not.
	"""
	with tempfile.TemporaryDirectory() as scratch:
		probe = Path(scratch) / "definition.json"
		write_json(probe, definition)
		return probe.read_bytes()


def _artifacts() -> tuple[tuple[Path, bytes], ...]:
	"""Every artifact this curator owns, with the exact bytes it should contain.

    Every generated artifact is compared byte-for-byte. The spatial report, knowledge note and
    manual excerpts are generated here rather than pinned independently, so prose cannot outlive
    the structured data behind it.
	"""
	report_bytes = (json.dumps(spatial_report, indent="\t", sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
	definition_bytes = _definition_bytes()
	return (
		(DEFINITION_PATH, definition_bytes),
		(SEED_PATH, definition_bytes),
		(SPATIAL_REPORT_PATH, report_bytes),
		(KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
		*((path, content.encode("utf-8")) for path, content in sorted(EXCERPT_CONTENTS.items())),
	)


def _comparable(payload: bytes) -> bytes:
	"""``payload`` with CRLF folded to LF, so the comparison ignores line endings and nothing else.

	These artifacts are compared byte-for-byte rather than as canonical JSON because their bytes
	are their identity: the gate has to keep refusing a reformatted definition, reordered keys or
	changed indentation, which a canonical-JSON comparison would wave through. What it must not
	refuse is a checkout Git rewrote on the way to disk. Git's Windows default
	``core.autocrlf=true`` turns every LF in the working tree into CRLF, so an untouched clone
	would fail this gate for a reason that has nothing to do with curation. Folding CRLF to LF on
	both sides forgives exactly that; a lone CR, a changed byte, an added or removed line all
	still fail.
	"""
	return payload.replace(b"\r\n", b"\n")


def _write(root: Path) -> None:
	existing = root / "machines/author-ready/stern/lord-of-the-rings-2003.json"
	if existing.is_file() and definition["coverage"]["status"] != "author_ready":
		raise RuntimeError(
			f"refusing to curate while an author-ready artifact exists (preserved): {existing}"
		)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	for path, payload in _artifacts()[2:]:
		target = root / path.relative_to(ROOT)
		target.parent.mkdir(parents=True, exist_ok=True)
		with target.open("wb") as stream:
			stream.write(payload)


def _check(root: Path) -> None:
	for path, expected in _artifacts()[:2]:
		target = root / path.relative_to(ROOT)
		label = "definition" if "machines" in target.parts else "seed"
		if not target.is_file():
			raise RuntimeError(f"Lord of the Rings {label} is missing: {target}")
		if _comparable(target.read_bytes()) != _comparable(expected):
			raise RuntimeError(f"Lord of the Rings {label} does not match the deterministic curator: {target}")
	# Byte-compare the generated report and knowledge note against what is on disk. Both are
	# produced from the same objects as the definition, so drift between prose and data is
	# impossible by construction rather than caught by a pinned digest.
	for path, expected in _artifacts()[2:]:
		target = root / path.relative_to(ROOT)
		label = "spatial report" if target.suffix == ".json" else "knowledge note"
		if not target.is_file():
			raise RuntimeError(f"Lord of the Rings {label} is missing: {target}")
		if _comparable(target.read_bytes()) != _comparable(expected):
			raise RuntimeError(
				f"Lord of the Rings {label} does not match the deterministic curator: {target}"
			)
	report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
	expected_format = "pinmame-spatial-audit" if definition["coverage"]["status"] == "author_ready" else "pinmame-spatial-blockers"
	if report.get("format") != expected_format or report.get("machine_id") != definition["machine"]["id"]:
		raise RuntimeError(
			f"Lord of the Rings spatial report must be {expected_format} for a "
			f"{definition['coverage']['status']} machine and must name this machine"
		)
	placements = sum(
		len(device.get("spatial", {}).get("placements", []))
		for collection in ("inputs", "outputs")
		for device in definition[collection]
	)
	if report.get("placement_count") != placements:
		raise RuntimeError(
			f"Lord of the Rings spatial audit claims {report.get('placement_count')} placements "
			f"but the definition carries {placements}"
		)
	print("Lord of the Rings definition, seed, spatial audit, and knowledge note match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts.")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed.")
	mode.add_argument(
		"--export-transcription",
		type=Path,
		help="Write the embedded reviewed manual transcription to this explicit external evidence path.",
	)
	parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository root to operate on.")
	args = parser.parse_args()
	root = args.repository_root.resolve()
	if args.export_transcription:
		write_json(args.export_transcription.resolve(), transcription)
		print(f"Wrote reviewed manual transcription to {args.export_transcription.resolve()}")
		return
	if args.regenerate:
		_write(root)
		print(f"Wrote {DEFINITION_PATH.relative_to(ROOT)} and {SEED_PATH.relative_to(ROOT)}")
		return
	_check(root)


if __name__ == "__main__":
	main()
