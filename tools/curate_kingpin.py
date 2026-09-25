"""Curate the physical Capcom Kingpin (1996) machine definition.

No printed factory manual is known for Kingpin: it was to follow Big Bang Bar when Capcom closed
its pinball division, Krellan's hands-on page calls it "just as rare, if not more so" than Big Bang
Bar's ten-or-so machines, and pinned PinMAME's own ``capcom.c`` says it "did not find a manual for
this one". The definition therefore rests on four independent sources:

* the pinned PinMAME source (address transport, the capInvSw11 opto mask, output typing);
* the ROM's own service menu, walked on fresh isolated state by the LibPinMAME harness
  (Solenoid/Lamp/Switch Tests print every device's name, wire colours and connector pin,
  and each step pairs that text with the public address that changed);
* the ROM's own I/O name-record table (``tools/capcom_kingpin_rom_records.py``);
* Krellan's hands-on chart of a real machine (lamp positions checked in operator mode).

The builder is side-effect free and deterministic: every reviewed value is a literal below,
so regeneration reproduces the canonical artifact byte-for-byte without reading external
evidence. ``--check`` refuses drift; ``--regenerate`` is the only path that writes.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/capcom/kingpin-1996.json"
SEED_PATH = ROOT / "tools/seeds/capcom/kingpin-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge/capcom/kingpin-1996.md"
MACHINE_ID = "capcom.kingpin.1996"
EXCERPT_DIR = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/capcom/kingpin-service-diagnostics.json"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_SCRIPTS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"

CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-capcom"
ROM_SOURCE = "rom-static.kingpin.kpb105-io-records"
SOLENOID_TEST_SOURCE = "service-diagnostic.kingpin.solenoid-test"
LAMP_TEST_SOURCE = "service-diagnostic.kingpin.lamp-test"
SWITCH_TEST_SOURCE = "service-diagnostic.kingpin.switch-test"
OPTO_TEST_SOURCE = "service-diagnostic.kingpin.opto-test"
TROUBLESHOOTING_BASELINE_SOURCE = "service-diagnostic.kingpin.troubleshooting-baseline"
TROUBLESHOOTING_HELD_SOURCE = "service-diagnostic.kingpin.troubleshooting-held"
TROUBLESHOOTING_SLAM_SOURCE = "service-diagnostic.kingpin.troubleshooting-slam-tilt"
RAMP_RUN_SOURCE = "runtime.kingpin.ramp-down-feedback"
SERVE_RUN_SOURCE = "runtime.kingpin.ball-serve"
DROP_RUN_SOURCE = "runtime.kingpin.drop-targets"
KRELLAN_SOURCE = "human-review.krellan.kingpin"
SCRIPT_SOURCE = "vpx.kingpin-1.2-thalamus"
SCRIPT_OLD_SOURCE = "vpx.kingpin-080715a"
SCRIPT_MOD_SOURCE = "vpx.kingpin-bigus-mod-3.0"

ROM_ARCHIVE_SHA256 = "fb64bcbc1dcd361ccc888cc235dde089e17907eac880af4cdfc3c7812269c0c5"
PROGRAM_ROM_SHA1 = "c731e0b5c9b211574dda8aecbad799bc180a59db"
LIBRARY_SHA256 = "ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d"
KRELLAN_PAGE_SHA256 = "d1aee4120403c311cafaa0252aaecf02b2fc357f610741bdadca5a31b425230e"
SCRIPT_SHA256 = "ebc3d8bd0b2d982e5817e99e5a23e1b480f87ace8fccacc17cbefe8600abb0ee"
SCRIPT_OLD_SHA256 = "4a7276245dd674415909a29f647718880b8e4d44b871ea9eafff2d05f6f63c15"
SCRIPT_MOD_SHA256 = "bea7f77d66d56d5bb01678c36fd21661ced263728d25f3309f5a1979ecab8995"

# BEGIN GENERATED DIAGNOSTIC TABLES
# C1.03 Solenoid Test text per public solenoid: (ROM name, drive wire and pin, supply) -- evidence/excerpts/capcom.kingpin.1996/service-solenoid-test.md
DIAG_SOLENOIDS = {
	1: ('OUTHOLE', 'BRN-BLK J14/13.1', 'VIO 50V'),
	2: ('TROUGH', 'BRN-RED J14/13.2', 'VIO 50V'),
	3: ('KNOCKER', 'BRN-ORG J14/13.3', 'VIO 50V'),
	4: ('LEFT SLINGSHOT', 'BRN-YEL J14/13.4', 'VIO 50V'),
	5: ('RIGHT SLINGSHOT', 'BRN-GRN J14/13.5', 'VIO 50V'),
	6: ('KING DROP RESET', 'BRN-BLU J14/13.6', 'VIO 50V'),
	7: ('PIN DROP RESET', 'BRN-VIO J14/13.7', 'VIO 50V'),
	8: ('GUN EJECT', 'BRN-GRY J14/13.9', 'VIO 50V'),
	9: ('LEFT FLIPPER', 'GRN-BRN J18/17.1', 'GRY-RED 50V L'),
	10: ('RIGHT FLIPPER', 'GRN-RED J18/17.2', 'GRY-GRN 50V R'),
	11: ('SLOT EJECT', 'GRN-ORG J18/17.3', 'VIO 50V'),
	12: ('SLOT MOTOR', 'GRN-YEL J18/17.4', 'YEL 12V'),
	13: ('TOPGATES', 'GRN-BLK J18/17.5', 'VIO 50V'),
	14: ('RAMP', 'GRN-BLU J18/17.7', 'VIO 50V'),
	15: ('C. STAR BUMPER', 'GRN-VIO J18/17.8', 'VIO 50V'),
	16: ('R. STAR BUMPER', 'GRN-GRY J18/17.9', 'VIO 50V'),
	17: ('L. STAR BUMPER', 'VIO-BRN J21/20.1', 'VIO 50V'),
	18: ('L. RAMP FLASHERS', 'VIO-RED J21/20.2', 'RED 20V B'),
	19: ('L. KID FLASHER', 'VIO-ORG J21/20.3', 'RED 20V B'),
	20: ('BIG AL FLASHERS', 'VIO-YEL J21/20.4', 'RED 20V B'),
	21: ('GUN TIP FLASHERS', 'VIO-GRN J21/20.5', 'RED 20V B'),
	22: ('R. RAMP FLASHER', 'VIO-BLU J21/20.6', 'RED 20V B'),
	23: ('BUILDING FLASHER', 'VIO-BLK J21/20.8', 'RED 20V B'),
	24: ('R. KID FLASHER', 'VIO-GRY J21/20.9', 'RED 20V B'),
	25: ('CAPTIVE FLASHER', 'GRY-BRN J25/24.1', 'RED 20V B'),
	26: ('BUMPERS FLASHER', 'GRY-RED J25/24.2', 'RED 20V B'),
	27: ('POWER FLASHERS', 'GRY-ORG J25/24.3', 'RED 20V B'),
	28: ('LEX FLASHER', 'GRY-YEL J25/24.5', 'RED 20V B'),
	29: ('L.ORBIT (EAST) FLASHER', 'GRY-GRN J25/24.6', 'RED 20V B'),
	30: ('KING FLASHERS', 'GRY-BLU J25/24.7', 'RED 20V B'),
	31: ('PIN FLASHERS', 'GRY-VIO J25/24.8', 'RED 20V B'),
	32: ('AUTO PLUNGER', 'GRY-BLK J25/24.9', 'VIO 50V'),
}

# C1.01 Switch Test text per held public switch: (ROM name, switch line, return line) -- service-switch-test.md
DIAG_SWITCHES = {
	1: ('COIN 1', 'GRN-BRN J9.1', 'BLK-GRN J9.10'),
	2: ('COIN 2', 'GRN-RED J9.2', 'BLK-GRN J9.10'),
	3: ('COIN 3', 'GRN-ORG J9.3', 'BLK-GRN J9.10'),
	4: ('COIN 4', 'GRN-YEL J9.4', 'BLK-GRN J9.10'),
	5: ('LEFT FLIPPER', 'GRN-BLK J9.5', 'BLK-GRN J9.10'),
	6: ('RIGHT FLIPPER', 'GRN-BLU J9.6', 'BLK-GRN J9.10'),
	7: ('START BUTTON', 'GRN-VIO J9.7', 'BLK-GRN J9.10'),
	8: ('COIN DOOR', 'GRN-GRY J9.9', 'BLK-GRN J9.10'),
	9: ('SLAM', 'WHT-BRN J7.1', 'BLK-WHT J7.10'),
	10: ('TILT', 'WHT-RED J7.2', 'BLK-WHT J7.10'),
	11: ('NOT USED', 'WHT-ORG J7.3', 'BLK-WHT J7.10'),
	12: ('NOT USED', 'WHT-YEL J7.4', 'BLK-WHT J7.10'),
	13: ('TOKEN EXTRA', 'WHT-GRN J7.5', 'BLK-WHT J7.10'),
	14: ('AUTO PLUNGER', 'WHT-BLU J7.7', 'BLK-WHT J7.10'),
	15: ('TOKEN EXIT', 'WHT-VIO J7.8', 'BLK-WHT J7.10'),
	16: ('TICKET NOTCH', 'WHT-GRY J7.9', 'BLK-WHT J7.10'),
	17: ('R. RAMP SPINNER', 'BRN-BLK J1.1', 'BLK-BRN J1.10'),
	18: ('R. RAMP EXIT', 'BRN-RED J1.2', 'BLK-BRN J1.10'),
	19: ('L. RETURN', 'BRN-ORG J1.3', 'BLK-BRN J1.10'),
	20: ('R. RETURN', 'BRN-YEL J1.4', 'BLK-BRN J1.10'),
	21: ('L. OUTLANE', 'BRN-GRN J1.5', 'BLK-BRN J1.10'),
	22: ('R. OUTLANE', 'BRN-BLU J1.6', 'BLK-BRN J1.10'),
	23: ('LEFT ORBIT', 'BRN-VIO J1.7', 'BLK-BRN J1.10'),
	24: ('RIGHT ORBIT', 'BRN-GRY J1.9', 'BLK-BRN J1.10'),
	25: ('DROP K', 'RED-BRN J2.1', 'BLK-RED J2.10'),
	26: ('DROP I', 'RED-BLK J2.2', 'BLK-RED J2.10'),
	27: ('DROP N', 'RED-ORG J2.3', 'BLK-RED J2.10'),
	28: ('DROP G', 'RED-YEL J2.4', 'BLK-RED J2.10'),
	29: ('DROP P', 'RED-GRN J2.5', 'BLK-RED J2.10'),
	30: ('DROP I', 'RED-BLU J2.7', 'BLK-RED J2.10'),
	31: ('DROP N', 'RED-VIO J2.8', 'BLK-RED J2.10'),
	32: ('CAPTIVE BALL', 'RED-GRY J2.9', 'BLK-RED J2.10'),
	33: ('EOS L', 'ORG-BRN J3.1', 'BLK-ORG J3.10'),
	34: ('EOS R', 'ORG-RED J3.2', 'BLK-ORG J3.10'),
	35: ('OUTHOLE', 'ORG-BLK J3.3', 'BLK-ORG J3.10'),
	36: ('TROUGH 1', 'ORG-YEL J3.4', 'BLK-ORG J3.10'),
	37: ('TROUGH 2', 'ORG-GRN J3.5', 'BLK-ORG J3.10'),
	38: ('TROUGH 3', 'ORG-BLU J3.7', 'BLK-ORG J3.10'),
	39: ('TROUGH 4', 'ORG-VIO J3.8', 'BLK-ORG J3.10'),
	40: ('NOT USED', 'ORG-GRY J3.9', 'BLK-ORG J3.10'),
	41: ('L. SLING', 'YEL-BRN J4.1', 'BLK-YEL J4.10'),
	42: ('R. SLING', 'YEL-RED J4.2', 'BLK-YEL J4.10'),
	43: ('SHOOTER', 'YEL-ORG J4.3', 'BLK-YEL J4.10'),
	44: ('GUN LOCK 1', 'YEL-BLK J4.4', 'BLK-YEL J4.10'),
	45: ('GUN LOCK 2', 'YEL-GRN J4.5', 'BLK-YEL J4.10'),
	46: ('GUN LOCK 3', 'YEL-BLU J4.7', 'BLK-YEL J4.10'),
	47: ('RAMP, DOWN', 'YEL-VIO J4.8', 'BLK-YEL J4.10'),
	48: ('GUN TROUGH OPTO', 'YEL-GRY J4.9', 'BLK-YEL J4.10'),
	49: ('L. SLOT STANDUP', 'GRN-BRN J5.1', 'BLK-GRN J5.10'),
	50: ('R. SLOT STANDUP', 'GRN-RED J5.2', 'BLK-GRN J5.10'),
	51: ('SLOT SAUCER', 'GRN-ORG J5.3', 'BLK-GRN J5.10'),
	52: ('SLOT OPTO', 'GRN-YEL J5.4', 'BLK-GRN J5.10'),
	53: ('L. TOPLANE', 'GRN-BLK J5.5', 'BLK-GRN J5.10'),
	54: ('C. TOPLANE', 'GRN-BLU J5.7', 'BLK-GRN J5.10'),
	55: ('R. TOPLANE', 'GRN-VIO J5.8', 'BLK-GRN J5.10'),
	56: ('NOT USED', 'GRN-GRY J5.9', 'BLK-GRN J5.10'),
	57: ('L. STAR BUMPER', 'BLU-BRN J6.1', 'BLK-BLU J6.10'),
	58: ('C. STAR BUMPER', 'BLU-RED J6.2', 'BLK-BLU J6.10'),
	59: ('R. STAR BUMPER', 'BLU-ORG J6.3', 'BLK-BLU J6.10'),
	60: ('UR. BALL STANDUP', 'BLU-YEL J6.4', 'BLK-BLU J6.10'),
	61: ('L. RAMP SPINNER', 'BLU-GRN J6.5', 'BLK-BLU J6.10'),
	62: ('L. RAMP EXIT', 'BLU-BLK J6.7', 'BLK-BLU J6.10'),
	63: ('RAMP STANDUP', 'BLU-VIO J6.8', 'BLK-BLU J6.10'),
	64: ('NOT USED', 'BLU-GRY J6.9', 'BLK-BLU J6.10'),
	65: ('NOT USED', 'VIO-BRN J7.1', 'BLK-VIO J7.10'),
	66: ('NOT USED', 'VIO-RED J7.2', 'BLK-VIO J7.10'),
	67: ('NOT USED', 'VIO-ORG J7.3', 'BLK-VIO J7.10'),
	68: ('NOT USED', 'VIO-YEL J7.4', 'BLK-VIO J7.10'),
	69: ('NOT USED', 'VIO-GRN J7.5', 'BLK-VIO J7.10'),
	70: ('NOT USED', 'VIO-BLU J7.7', 'BLK-VIO J7.10'),
	71: ('NOT USED', 'VIO-BLK J7.8', 'BLK-VIO J7.10'),
	72: ('NOT USED', 'VIO-GRY J7.9', 'BLK-VIO J7.10'),
	73: ('NOT USED', 'GRY-BRN J8.1', 'BLK-GRY J8.10'),
	74: ('NOT USED', 'GRY-RED J8.2', 'BLK-GRY J8.10'),
	75: ('NOT USED', 'GRY-ORG J8.3', 'BLK-GRY J8.10'),
	76: ('NOT USED', 'GRY-YEL J8.4', 'BLK-GRY J8.10'),
	77: ('NOT USED', 'GRY-GRN J8.5', 'BLK-GRY J8.10'),
	78: ('NOT USED', 'GRY-BLU J8.7', 'BLK-GRY J8.10'),
	79: ('NOT USED', 'GRY-VIO J8.8', 'BLK-GRY J8.10'),
	80: ('NOT USED', 'GRY-BLK J8.9', 'BLK-GRY J8.10'),
}

# C1.04 Lamp Test text per public lamp: (matrix code, ROM name, column strobe line, row line) -- service-lamp-test.md
DIAG_LAMPS = {
	1: ('11A', 'COIN 1/COIN 3', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW1-M1A J1/2.1 RED-BRN'),
	2: ('12A', 'COIN 2/COIN 4', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW2-M2A J1/2.2 RED-BLK'),
	3: ('13A', 'START BUTTON', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW3-M3A J1/2.3 RED-ORG'),
	4: ('14A', 'AUTO PLUNGER', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW4-M4A J1/2.5 RED-YEL'),
	5: ('15A', "L. YOU'RE COVERED", 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW5-M5A J1/2.6 RED-GRN'),
	6: ('16A', 'L. OPEN HIDEOUT', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW6-M6A J1/2.7 RED-BLU'),
	7: ('17A', "R. YOU'RE COVERED", 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW7-M7A J1/2.8 RED-VIO'),
	8: ('18A', 'R. OPEN HIDEOUT', 'COL1-SM1A J6/7.1 YEL-BRN', 'ROW8-M8A J1/2.9 RED-GRY'),
	9: ('21A', '6X SHOTGUN', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW1-M1A J1/2.1 RED-BRN'),
	10: ('22A', '8X MACHINE GUN', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW2-M2A J1/2.2 RED-BLK'),
	11: ('23A', '4X .45 AUTOMATIC', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW3-M3A J1/2.3 RED-ORG'),
	12: ('24A', '2X REVOLVER', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW4-M4A J1/2.5 RED-YEL'),
	13: ('25A', 'TREASURE HUNT', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW5-M5A J1/2.6 RED-GRN'),
	14: ('26A', 'KID GUN LEFT', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW6-M6A J1/2.7 RED-BLU'),
	15: ('27A', 'KID GUN RIGHT', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW7-M7A J1/2.8 RED-VIO'),
	16: ('28A', 'LIVE AGAIN', 'COL2-SM2A J6/7.2 YEL-RED', 'ROW8-M8A J1/2.9 RED-GRY'),
	17: ('31A', 'POWERUP PAYOLA', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW1-M1A J1/2.1 RED-BRN'),
	18: ('32A', 'DOUBLE SPIN CITY', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW2-M2A J1/2.2 RED-BLK'),
	19: ('33A', "BUMP & ROLL'EM", 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW3-M3A J1/2.3 RED-ORG'),
	20: ('34A', 'ARMS RACE', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW4-M4A J1/2.5 RED-YEL'),
	21: ('35A', 'SPIN CITY', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW5-M5A J1/2.6 RED-GRN'),
	22: ('36A', 'LOCK 1', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW6-M6A J1/2.7 RED-BLU'),
	23: ('37A', 'LOCK 2', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW7-M7A J1/2.8 RED-VIO'),
	24: ('38A', 'LOCK 3', 'COL3-SM3A J6/7.3 YEL-ORG', 'ROW8-M8A J1/2.9 RED-GRY'),
	25: ('41A', 'POWER BAR 1', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW1-M1A J1/2.1 RED-BRN'),
	26: ('42A', 'POWER BAR 2', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW2-M2A J1/2.2 RED-BLK'),
	27: ('43A', 'POWER BAR 3', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW3-M3A J1/2.3 RED-ORG'),
	28: ('44A', 'POWER BAR 4', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW4-M4A J1/2.5 RED-YEL'),
	29: ('45A', 'POWER BAR 5', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW5-M5A J1/2.6 RED-GRN'),
	30: ('46A', 'POWER BAR 6', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW6-M6A J1/2.7 RED-BLU'),
	31: ('47A', 'POWER BAR 7', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW7-M7A J1/2.8 RED-VIO'),
	32: ('48A', 'POWER BAR 8', 'COL4-SM4A J6/7.4 YEL-BLK', 'ROW8-M8A J1/2.9 RED-GRY'),
	33: ('51A', 'POWER BAR 9', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW1-M1A J1/2.1 RED-BRN'),
	34: ('52A', 'POWER BAR 10', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW2-M2A J1/2.2 RED-BLK'),
	35: ('53A', 'BONUS 2X', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW3-M3A J1/2.3 RED-ORG'),
	36: ('54A', 'BONUS 4X', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW4-M4A J1/2.5 RED-YEL'),
	37: ('55A', 'BONUS 6X', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW5-M5A J1/2.6 RED-GRN'),
	38: ('56A', 'BONUS 8X', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW6-M6A J1/2.7 RED-BLU'),
	39: ('57A', 'BONUS 10X', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW7-M7A J1/2.8 RED-VIO'),
	40: ('58A', 'SLOT GI (2)', 'COL5-SM5A J6/7.5 YEL-GRN', 'ROW8-M8A J1/2.9 RED-GRY'),
	41: ('61A', 'L. RAMP POWERUP', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW1-M1A J1/2.1 RED-BRN'),
	42: ('62A', 'L. RAMP POINTS', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW2-M2A J1/2.2 RED-BLK'),
	43: ('63A', 'L. DROP KING', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW3-M3A J1/2.3 RED-ORG'),
	44: ('64A', 'R. DROP PIN', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW4-M4A J1/2.5 RED-YEL'),
	45: ('65A', 'L. RAMP LOCK', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW5-M5A J1/2.6 RED-GRN'),
	46: ('66A', 'RAMP STANDUP', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW6-M6A J1/2.7 RED-BLU'),
	47: ('67A', 'R. RAMP POWERUP', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW7-M7A J1/2.8 RED-VIO'),
	48: ('68A', 'R. RAMP POINTS', 'COL6-SM6A J6/7.7 YEL-BLU', 'ROW8-M8A J1/2.9 RED-GRY'),
	49: ('71A', 'R. ORBIT POWERUP', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW1-M1A J1/2.1 RED-BRN'),
	50: ('72A', 'R. ORBIT POINTS', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW2-M2A J1/2.2 RED-BLK'),
	51: ('73A', 'U.R. STANDUP PTS', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW3-M3A J1/2.3 RED-ORG'),
	52: ('74A', 'U.R. CHARMED LIFE', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW4-M4A J1/2.5 RED-YEL'),
	53: ('75A', 'BIG AL', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW5-M5A J1/2.6 RED-GRN'),
	54: ('76A', 'CAPTIVE BALL', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW6-M6A J1/2.7 RED-BLU'),
	55: ('77A', 'U.R. 2 BALL FURY', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW7-M7A J1/2.8 RED-VIO'),
	56: ('78A', 'U.R. STANDUP GUN', 'COL7-SM7A J6/7.8 YEL-VIO', 'ROW8-M8A J1/2.9 RED-GRY'),
	57: ('81A', 'BOSS KILL', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW1-M1A J1/2.1 RED-BRN'),
	58: ('82A', 'GET THE GUNS', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW2-M2A J1/2.2 RED-BLK'),
	59: ('83A', 'BIG HEIST', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW3-M3A J1/2.3 RED-ORG'),
	60: ('84A', 'RAMBLE & GAMBLE', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW4-M4A J1/2.5 RED-YEL'),
	61: ('85A', 'DELIVER THE GOODS', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW5-M5A J1/2.6 RED-GRN'),
	62: ('86A', 'PAYOFF PANIC', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW6-M6A J1/2.7 RED-BLU'),
	63: ('87A', 'DOUBLE CROSS', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW7-M7A J1/2.8 RED-VIO'),
	64: ('88A', 'HIT THE KINGPIN', 'COL8-SM8A J6/7.9 YEL-GRY', 'ROW8-M8A J1/2.9 RED-GRY'),
	65: ('11B', 'L. ORBIT POWERUP', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW1-M1B J4/5.1 ORG-BRN'),
	66: ('12B', 'L. ORBIT POINTS', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW2-M2B J4/5.2 ORG-RED'),
	67: ('13B', 'JACKPOT', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW3-M3B J4/5.4 ORG-BLK'),
	68: ('14B', 'SUPER JACKPOT', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW4-M4B J4/5.5 ORG-YEL'),
	69: ('15B', 'L. TOPLANE', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW5-M5B J4/5.6 ORG-GRN'),
	70: ('16B', 'C. TOPLANE', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW6-M6B J4/5.7 ORG-BLU'),
	71: ('17B', 'R. TOPLANE', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW7-M7B J4/5.8 ORG-VIO'),
	72: ('18B', 'L. SLOT STANDUP', 'COL1-SM1B J9/10.1 BLU-BRN', 'ROW8-M8B J4/5.9 ORG-GRY'),
	73: ('21B', 'R. SLOT STANDUP', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW1-M1B J4/5.1 ORG-BRN'),
	74: ('22B', 'JACKPOT JUMP 2X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW2-M2B J4/5.2 ORG-RED'),
	75: ('23B', 'JACKPOT JUMP 4X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW3-M3B J4/5.4 ORG-BLK'),
	76: ('24B', 'JACKPOT JUMP 6X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW4-M4B J4/5.5 ORG-YEL'),
	77: ('25B', 'JACKPOT JUMP 8X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW5-M5B J4/5.6 ORG-GRN'),
	78: ('26B', 'JACKPOT JUMP 10X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW6-M6B J4/5.7 ORG-BLU'),
	79: ('27B', 'JACKPOT JUMP 12X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW7-M7B J4/5.8 ORG-VIO'),
	80: ('28B', 'JACKPOT JUMP 14X', 'COL2-SM2B J9/10.2 BLU-RED', 'ROW8-M8B J4/5.9 ORG-GRY'),
	81: ('31B', 'L. STAR BUMPER', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW1-M1B J4/5.1 ORG-BRN'),
	82: ('32B', 'C. STAR BUMPER', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW2-M2B J4/5.2 ORG-RED'),
	83: ('33B', 'R. STAR BUMPER', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW3-M3B J4/5.4 ORG-BLK'),
	84: ('34B', 'G.I. 1', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW4-M4B J4/5.5 ORG-YEL'),
	85: ('35B', 'G.I. 2 (2)', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW5-M5B J4/5.6 ORG-GRN'),
	86: ('36B', 'G.I. 3 (2)', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW6-M6B J4/5.7 ORG-BLU'),
	87: ('37B', 'G.I. 4 (RED)', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW7-M7B J4/5.8 ORG-VIO'),
	88: ('38B', 'G.I. 5', 'COL3-SM3B J9/10.3 BLU-ORG', 'ROW8-M8B J4/5.9 ORG-GRY'),
	89: ('41B', 'G.I. 6', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW1-M1B J4/5.1 ORG-BRN'),
	90: ('42B', 'G.I. 7 (RED)', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW2-M2B J4/5.2 ORG-RED'),
	91: ('43B', 'G.I. 8', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW3-M3B J4/5.4 ORG-BLK'),
	92: ('44B', 'G.I. 9 (RED)', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW4-M4B J4/5.5 ORG-YEL'),
	93: ('45B', 'G.I. 10', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW5-M5B J4/5.6 ORG-GRN'),
	94: ('46B', 'G.I. 11 (RED)', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW6-M6B J4/5.7 ORG-BLU'),
	95: ('47B', 'G.I. 12 (2)', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW7-M7B J4/5.8 ORG-VIO'),
	96: ('48B', 'G.I. 13 (2)', 'COL4-SM4B J9/10.4 BLU-YEL', 'ROW8-M8B J4/5.9 ORG-GRY'),
	97: ('51B', 'G.I. 14 (2)', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW1-M1B J4/5.1 ORG-BRN'),
	98: ('52B', 'G.I. 15 (2)', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW2-M2B J4/5.2 ORG-RED'),
	99: ('53B', 'G.I. 16', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW3-M3B J4/5.4 ORG-BLK'),
	100: ('54B', 'G.I. 17 (RED)', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW4-M4B J4/5.5 ORG-YEL'),
	101: ('55B', 'CAPTIVE STANDUP', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW5-M5B J4/5.6 ORG-GRN'),
	102: ('56B', 'G.I. 19 (RED)', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW6-M6B J4/5.7 ORG-BLU'),
	103: ('57B', 'G.I. 20', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW7-M7B J4/5.8 ORG-VIO'),
	104: ('58B', 'G.I. 21 (RED)', 'COL5-SM5B J9/10.5 BLU-GRN', 'ROW8-M8B J4/5.9 ORG-GRY'),
	105: ('61B', 'G.I. 22', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW1-M1B J4/5.1 ORG-BRN'),
	106: ('62B', 'G.I. 23 (RED)', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW2-M2B J4/5.2 ORG-RED'),
	107: ('63B', 'G.I. 24', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW3-M3B J4/5.4 ORG-BLK'),
	108: ('64B', 'G.I. 25 (RED)', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW4-M4B J4/5.5 ORG-YEL'),
	109: ('65B', 'G.I. 26', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW5-M5B J4/5.6 ORG-GRN'),
	110: ('66B', 'G.I. 27 (RED)', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW6-M6B J4/5.7 ORG-BLU'),
	111: ('67B', 'G.I. 28', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW7-M7B J4/5.8 ORG-VIO'),
	112: ('68B', 'G.I. 29 (RED)', 'COL6-SM6B J9/10.6 BLU-BLK', 'ROW8-M8B J4/5.9 ORG-GRY'),
	113: ('71B', 'G.I. 30', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW1-M1B J4/5.1 ORG-BRN'),
	114: ('72B', 'G.I. 31 (RED)', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW2-M2B J4/5.2 ORG-RED'),
	115: ('73B', 'G.I. 36 (RED)', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW3-M3B J4/5.4 ORG-BLK'),
	116: ('74B', 'BACKPANEL, LEFT', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW4-M4B J4/5.5 ORG-YEL'),
	117: ('75B', 'G.I. 32 (2)', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW5-M5B J4/5.6 ORG-GRN'),
	118: ('76B', 'G.I. 33 (2,RED)', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW6-M6B J4/5.7 ORG-BLU'),
	119: ('77B', 'BACKPANEL, CENTER', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW7-M7B J4/5.8 ORG-VIO'),
	120: ('78B', 'BACKPANEL, RIGHT', 'COL7-SM7B J9/10.8 BLU-VIO', 'ROW8-M8B J4/5.9 ORG-GRY'),
	121: ('81B', 'LEFT SPINNER', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW1-M1B J4/5.1 ORG-BRN'),
	122: ('82B', 'RIGHT SPINNER', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW2-M2B J4/5.2 ORG-RED'),
	123: ('83B', 'NOT USED', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW3-M3B J4/5.4 ORG-BLK'),
	124: ('84B', 'NOT USED', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW4-M4B J4/5.5 ORG-YEL'),
	125: ('85B', 'NOT USED', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW5-M5B J4/5.6 ORG-GRN'),
	126: ('86B', 'BACKBOX G.I.(2)', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW6-M6B J4/5.7 ORG-BLU'),
	127: ('87B', 'G.I. 34 (2)', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW7-M7B J4/5.8 ORG-VIO'),
	128: ('88B', 'G.I. 35 (2,RED)', 'COL8-SM8B J9/10.9 BLU-GRY', 'ROW8-M8B J4/5.9 ORG-GRY'),
}

# Internal ROM switch number per public address (rom-io-name-records.md)
ROM_SWITCH_NUMBERS = {
	14: 5,
	17: 24,
	18: 25,
	19: 26,
	20: 27,
	21: 28,
	22: 29,
	23: 30,
	24: 31,
	25: 40,
	26: 41,
	27: 42,
	28: 43,
	29: 44,
	30: 45,
	31: 46,
	32: 47,
	33: 56,
	34: 57,
	35: 58,
	36: 59,
	37: 60,
	38: 61,
	39: 62,
	41: 72,
	42: 73,
	43: 74,
	44: 75,
	45: 76,
	46: 77,
	47: 78,
	48: 79,
	49: 16,
	50: 17,
	51: 18,
	52: 19,
	53: 20,
	54: 21,
	55: 22,
	57: 32,
	58: 33,
	59: 34,
	60: 35,
	61: 36,
	62: 37,
	63: 38,
}

# Internal ROM coil number per public address (rom-io-name-records.md)
ROM_COIL_NUMBERS = {
	1: 15,
	2: 14,
	3: 13,
	4: 12,
	5: 11,
	6: 10,
	7: 9,
	8: 8,
	11: 29,
	12: 28,
	13: 27,
	14: 26,
	15: 25,
	16: 24,
	17: 7,
	18: 6,
	19: 5,
	20: 4,
	21: 3,
	22: 2,
	23: 1,
	24: 0,
	25: 23,
	26: 22,
	27: 21,
	28: 20,
	29: 19,
	30: 18,
	31: 17,
	32: 16,
}

# Internal ROM lamp number per public address (rom-io-name-records.md)
ROM_LAMP_NUMBERS = {
	3: 39,
	4: 55,
	5: 71,
	6: 87,
	7: 103,
	8: 119,
	9: 6,
	10: 22,
	11: 38,
	12: 54,
	13: 70,
	14: 86,
	15: 102,
	16: 118,
	17: 5,
	18: 21,
	19: 37,
	20: 53,
	21: 69,
	22: 85,
	23: 101,
	24: 117,
	25: 4,
	26: 20,
	27: 36,
	28: 52,
	29: 68,
	30: 84,
	31: 100,
	32: 116,
	33: 3,
	34: 19,
	35: 35,
	36: 51,
	37: 67,
	38: 83,
	39: 99,
	40: 115,
	41: 2,
	42: 18,
	43: 34,
	44: 50,
	45: 66,
	46: 82,
	47: 98,
	48: 114,
	49: 1,
	50: 17,
	51: 33,
	52: 49,
	53: 65,
	54: 81,
	55: 97,
	56: 113,
	57: 0,
	58: 16,
	59: 32,
	60: 48,
	61: 64,
	62: 80,
	63: 96,
	64: 112,
	65: 15,
	66: 31,
	67: 47,
	68: 63,
	69: 79,
	70: 95,
	71: 111,
	72: 127,
	73: 14,
	74: 30,
	75: 46,
	76: 62,
	77: 78,
	78: 94,
	79: 110,
	80: 126,
	81: 13,
	82: 29,
	83: 45,
	84: 61,
	85: 77,
	86: 93,
	87: 109,
	88: 125,
	89: 12,
	90: 28,
	91: 44,
	92: 60,
	93: 76,
	94: 92,
	95: 108,
	96: 124,
	97: 11,
	98: 27,
	99: 43,
	100: 59,
	101: 75,
	102: 91,
	103: 107,
	104: 123,
	105: 10,
	106: 26,
	107: 42,
	108: 58,
	109: 74,
	110: 90,
	111: 106,
	112: 122,
	113: 9,
	114: 25,
	115: 41,
	116: 57,
	117: 73,
	118: 89,
	119: 105,
	120: 121,
	121: 8,
	122: 24,
	126: 88,
	127: 104,
	128: 120,
}

# Krellan's hands-on lamp description per public lamp (krellan-lamp-matrix-a/b.md)
KRELLAN_LAMPS = {
	1: 'Coin Slots 1 & 3',
	2: 'Coin Slots 2 & 4',
	3: 'Start Button',
	4: 'Launch Button',
	5: 'Left Outlane',
	6: 'Left Inlane',
	7: 'Right Outlane',
	8: 'Right Inlane',
	9: '(playfield guns) 6X',
	10: '8X',
	11: '4X',
	12: '2X',
	13: "Kingpin's Vault",
	14: 'Sudden (by left flipper)',
	15: 'Death (by right flipper)',
	16: 'Live Again',
	17: '(center modes) Powerup Payola',
	18: 'Double Spin City',
	19: "Bump & Roll 'Em",
	20: 'Arms Race',
	21: 'Spin City',
	22: 'Lock 1',
	23: 'Lock 2',
	24: 'Lock 3',
	25: '(power meter) 1 (left side)',
	26: '2',
	27: '3',
	28: '4',
	29: '5',
	30: '6',
	31: '7',
	32: '8',
	33: '9',
	34: '10',
	35: 'Bonus 2X (playfield above center)',
	36: '4X',
	37: '6X',
	38: '8X',
	39: '10X',
	40: 'Slot GI (x2) (bright above and behind slot machine)',
	41: 'Left Ramp Powerup',
	42: 'North $ (left ramp)',
	43: 'Hurry (left drop targets)',
	44: 'Quick (right drop targets)',
	45: 'Hideout (under left ramp)',
	46: 'Gun (standup between ramps)',
	47: 'Right Ramp Powerup',
	48: 'South $ (right ramp)',
	49: 'Right Orbit Powerup',
	50: 'East $ (right orbit)',
	51: '$ (lane to right gun standup)',
	52: 'Charmed Life (lane to right gun standup)',
	53: 'Big Al (face on playfield by guns)',
	54: 'Captive Ball Start Feature',
	55: '2 Ball (lane to right gun standup)',
	56: 'Gun (right gun standup at end of lane)',
	57: "Finish 'Em Off (into slot machine)",
	58: '(slot machine modes) Get The Guns',
	59: 'Big Heist',
	60: 'Ramble & Gamble',
	61: 'Deliver The Goods',
	62: 'Payoff Panic',
	63: 'Double Cross',
	64: 'Hit The Kingpin',
	65: 'Left Orbit Powerup',
	66: 'West $ (left orbit)',
	67: 'Jackpot (into slot machine)',
	68: 'Super Jackpot',
	69: 'K (top rollover lanes)',
	70: 'I',
	71: 'D',
	72: 'Gun (by left side of slot machine)',
	73: 'Gun (by right side of slot machine)',
	74: 'Backglass Jackpot Jump 2X',
	75: '4X',
	76: '6X',
	77: '8X',
	78: '10X',
	79: '12X',
	80: '14X',
	81: 'Left Jet Bumper',
	82: 'Bottom Jet Bumper',
	83: 'Right Jet Bumper',
	84: '(behind KING targets, under "Flow" in "Flower Shop")',
	85: 'Left Flipper Return (x2)',
	86: 'Right Flipper Return (x2)',
	87: 'Lamppost ("Flower Shop", red)',
	88: '(at bottom of divider between right orbit and lane to right gun standup, yellow)',
	89: '(behind right gun standup in slot machine)',
	90: '(behind above and red)',
	91: 'Top Lane Divider (left of K rollover lane)',
	92: '(behind above and red)',
	93: '(right of slot machine structure, between it and left jet bumper)',
	94: '(behind above and red)',
	95: 'Left Slingshot (x2)',
	96: 'Right Slingshot (x2)',
	97: 'Top Lane (between K and I rollover lanes, x2)',
	98: 'Top Lane (between I and D rollover lanes, x2)',
	99: '(left of base of captive ball)',
	100: '(behind above and red)',
	101: '(end of captive ball lane)',
	102: '(behind above and red)',
	103: '(behind left orbit, far back corner of playfield)',
	104: '(behind above and red)',
	105: '(behind and near end of right drop targets)',
	106: '(behind above and red)',
	107: '(behind far end of right drop targets)',
	108: '(behind above and red)',
	109: '(in front of right orbit, between it and right drop targets)',
	110: '(behind above and red)',
	111: '(behind right orbit, far back corner of playfield)',
	112: '(behind above and red)',
	113: '(under tracks at right ramp entrance)',
	114: '(behind above and red)',
	115: '(behind lamp #38B, between right orbit and lane to right gun standup, red)',
	116: '(back of playfield, vertical, behind artwork on left side)',
	117: 'Between Left & Right Ramps (x2)',
	118: '(behind above and red, x2)',
	119: '(murder victim, center of vertical artwork at back of playfield, red)',
	120: '(right side of vertical artwork)',
	121: 'Left Spin City (over spinner)',
	122: 'Right Spin City (over spinner)',
	126: 'Jackpot Jump (text on backglass, above gun, x2)',
	127: '(behind right gun standup and at corner between that lane and right orbit, x2)',
	128: '(behind above and red, x2)',
}
# END GENERATED DIAGNOSTIC TABLES

WIRE_COLOURS = {"BLK", "BRN", "RED", "ORG", "YEL", "GRN", "BLU", "VIO", "GRY", "WHT"}

# --- Readable labels. The ROM's own text is kept verbatim in physical.notes and as a
# `kingpin.rom-name` alias; these labels only expand its abbreviations (L./R./C./UR.).
CABINET_SWITCHES = {
	1: ("Coin Chute 1", "COIN 1"),
	2: ("Coin Chute 2", "COIN 2"),
	3: ("Coin Chute 3", "COIN 3"),
	4: ("Coin Chute 4", "COIN 4"),
	5: ("Left Flipper Button", "LEFT FLIPPER"),
	6: ("Right Flipper Button", "RIGHT FLIPPER"),
	7: ("Start Button", "START BUTTON"),
	8: ("Coin Door", "COIN DOOR"),
}
SWITCH_LABELS = {
	9: "Slam Tilt", 10: "Tilt", 13: "Token Extra", 14: "Launch Button", 15: "Token Exit", 16: "Ticket Notch",
	17: "Right Ramp Spinner", 18: "Right Ramp Exit", 19: "Left Return Lane", 20: "Right Return Lane",
	21: "Left Outlane", 22: "Right Outlane", 23: "Left Orbit", 24: "Right Orbit",
	25: "KING Drop Target K", 26: "KING Drop Target I", 27: "KING Drop Target N", 28: "KING Drop Target G",
	29: "PIN Drop Target P", 30: "PIN Drop Target I", 31: "PIN Drop Target N", 32: "Captive Ball",
	33: "Left Flipper EOS", 34: "Right Flipper EOS", 35: "Outhole", 36: "Trough 1", 37: "Trough 2",
	38: "Trough 3", 39: "Trough 4", 41: "Left Slingshot", 42: "Right Slingshot", 43: "Shooter Lane",
	44: "Gun Lock 1", 45: "Gun Lock 2", 46: "Gun Lock 3", 47: "Left Ramp Down", 48: "Gun Trough Opto",
	49: "Left Slot Standup", 50: "Right Slot Standup", 51: "Slot Saucer", 52: "Slot Opto",
	53: "Left Top Lane", 54: "Center Top Lane", 55: "Right Top Lane",
	57: "Left Star Bumper", 58: "Center Star Bumper", 59: "Right Star Bumper",
	60: "Upper Right Ball Standup", 61: "Left Ramp Spinner", 62: "Left Ramp Exit", 63: "Ramp Standup",
}
# PinMAME's capInvSw11 = {0, 0x01, 0x00, 0x78, 0x88, 0x08, 0x10} (src/wpc/capgames.c), indexed by
# internal column, bit = row: col1 bit0 -> 17; col3 bits3-6 -> 36-39; col4 bits3,7 -> 44, 48;
# col5 bit3 -> 52; col6 bit4 -> 61. The ROM's own switch records flag exactly this set as optos
# (payload byte 14 bit 1), the ROM's Switch Test draws exactly these as a beam icon, and Krellan's
# hands-on chart sets exactly these names in italic, which the page defines as optos.
OPTO_SWITCHES = {17, 36, 37, 38, 39, 44, 48, 52, 61}
# Contact polarity (docs/INSTRUCTIONS.md: normally_closed is a construction fact about the contact the matrix sees, derived
# from the platform's read path and a runtime proof where no manual prints it). capcom.c's io_r returns swMatrix ^ 0xffff for both the switch board and the cabinet port, so a set swMatrix
# bit is the CPU's closed-contact reading, and core_setSw applies capInvSw11 to the nine optos only; the C1.01 Switch
# Test icons (service-switch-test.md) draw every non-opto contact closed at public 1. Which level the ROM expects at
# rest comes from C5 TROUBLESHOOTING (service-troubleshooting.md): with switches held at 1 from power-up it lists these
# as INFO messages, and in the baseline run, where they rest at 0, it lists none.
TROUBLESHOOTING_REPORTED_AT_1 = {1, 2, 3, 4, 9, 10, 14, 19, 20, 21, 22, 23, 24, 32, 33, 34, 41, 42, 49, 50, 53, 54, 55, 57, 58, 59, 60, 62, 63}
# The same report lists the left-ramp-down switch 47 when it is left at 0, and not while it rests at 1 with the ramp down.
TROUBLESHOOTING_REPORTED_AT_0 = {47}
# Listed neither at 0 in the baseline run nor at 1 in the held run: the report does not check these at rest (ball holders,
# drop targets, the right-ramp exit and the optional dispenser inputs).
TROUBLESHOOTING_UNCHECKED = {13, 15, 16, 18, 25, 26, 27, 28, 29, 30, 31, 35, 43, 45, 46, 51}
# The drop-target run (kpb105-drop-targets): in a game, with every target at 0 for 8 s, no reset fires; with every target of a
# bank at public 1 the ROM fires that bank's reset coil repeatedly (KING 6 four times, PIN 7 six times); one KING target alone
# at 1 draws no reset. So public 1 is a target down.
DROP_TARGET_RESET = {25: 6, 26: 6, 27: 6, 28: 6, 29: 7, 30: 7, 31: 7}
CONTACT_POLARITY_NOTES = {
	5: "The report cannot check it, because the menu walk uses it; the ROM reads public 1 as the press (the walks step the menus with the button bit 84, which PinMAME copies into 5).",
	6: "The report cannot check it, because the menu walk uses it; the ROM reads public 1 as the press (the walks step the menus with the button bit 82, which PinMAME copies into 6).",
	7: "The report cannot check it, because the menu walk uses it; the ROM reads public 1 as the press (Start selects in every walk and starts the game in the ball-serve run).",
	8: (
		"The report cannot check it, because the menu walk uses it; the ROM opens the operator menu when public 8 goes to 1 in every walk "
		"and runs attract with it at 0. PinMAME and the ROM call it the coin door switch, Krellan the operator's Advance button; either way "
		"public 1 is the actuated state."
	),
	9: "Slam switches are normally closed on some other platforms; this ROM reports the slam switch when it is held at 1 at power-up and expects it at 0.",
	33: "End-of-stroke switches are normally closed on some other platforms; this ROM reports EOS L when it is held at 1 at power-up and expects it at 0 with the flipper down.",
	34: "End-of-stroke switches are normally closed on some other platforms; this ROM reports EOS R when it is held at 1 at power-up and expects it at 0 with the flipper down.",
	35: "The ROM treats public 1 as a ball on the switch: it fires the outhole coil 1 in the ball-serve run and repeatedly in the held Troubleshooting run's attract phase.",
	43: "The ROM treats public 1 as a ball in the shooter lane: it fires the auto plunger 32 in the ball-serve run and in the held Troubleshooting run's attract phase.",
	51: (
		"In the held Troubleshooting run's attract phase, with 51 and about fifty other switches at 1 (the slot opto 52 among them), "
		"the ROM fires the slot eject 11 repeatedly, consistent with public 1 being a ball in the saucer."
	),
}
CABINET_SWITCH_ADDRESSES = set(range(1, 17))
# Krellan: 13/15 serve an optional token dispenser and 16 an optional ticket dispenser.
OPTIONAL_SWITCHES = {13, 15, 16}
CABINET_ROLES = {
	1: ["cabinet.coin.1"], 2: ["cabinet.coin.2"], 3: ["cabinet.coin.3"], 4: ["cabinet.coin.4"],
	5: ["flipper.lower.left.button"], 6: ["flipper.lower.right.button"], 7: ["cabinet.start"],
	8: ["cabinet.coin-door"], 9: ["cabinet.slam-tilt"], 10: ["cabinet.tilt"], 14: ["cabinet.launch"],
	13: ["service.ticket"], 15: ["service.ticket"], 16: ["service.ticket"],
}
KRELLAN_SWITCH_NOTES = {
	13: "Krellan: for an optional token dispenser.",
	14: "Krellan: 'Launch Button (for autoplunger)'.",
	15: "Krellan: for an optional token dispenser.",
	16: "Krellan: for an optional ticket dispenser.",
	17: "Krellan: 'Right Spinner (on ramp)'.",
	19: "Krellan: 'Left Inlane'.",
	20: "Krellan: 'Right Inlane'.",
	44: "Krellan: 'Gun Lock 1 (hideout under ramp)'.",
	47: "Krellan: 'Left Ramp Down (active when lowered)'.",
	48: "Krellan is unsure of its purpose and believes it is used when preparing to kick balls out of the lock.",
	49: "Krellan: 'Left Gun Target (by slot machine)'.",
	50: "Krellan: 'Right Gun Target (by slot machine)'.",
	51: "Krellan: 'Slot Machine Saucer'.",
	53: "Krellan: top-lane rollover 'K'.",
	54: "Krellan: top-lane rollover 'I'.",
	55: "Krellan: top-lane rollover 'D'.",
	57: "Krellan: 'Left Jet Bumper'.",
	58: "Krellan: 'Bottom Jet Bumper'.",
	59: "Krellan: 'Right Jet Bumper'.",
	60: "Krellan: 'Gun Target (at end of lane by right side of machine)'.",
	61: "Krellan: 'Left Spinner (on ramp)'.",
	63: "Krellan: 'Gun Target (between ramps)'.",
}

SOLENOID_LABELS = {
	1: "Outhole", 2: "Trough", 3: "Knocker", 4: "Left Slingshot", 5: "Right Slingshot",
	6: "KING Drop Target Reset", 7: "PIN Drop Target Reset", 8: "Gun Eject", 9: "Left Flipper",
	10: "Right Flipper", 11: "Slot Eject", 12: "Slot Motor", 13: "Top Gates", 14: "Left Ramp Entrance",
	15: "Center Star Bumper", 16: "Right Star Bumper", 17: "Left Star Bumper", 18: "Left Ramp Flashers",
	19: "Left Kid Flasher", 20: "Big Al Flashers", 21: "Gun Tip Flashers", 22: "Right Ramp Flasher",
	23: "Building Flasher", 24: "Right Kid Flasher", 25: "Captive Flasher", 26: "Bumpers Flasher",
	27: "Power Flashers", 28: "Lex Flasher", 29: "Left Orbit (East) Flasher", 30: "KING Flashers",
	31: "PIN Flashers", 32: "Auto Plunger",
}
FLASHER_SOLENOIDS = set(range(18, 32))
MOTOR_SOLENOIDS = {12}
KRELLAN_SOLENOID_NOTES = {
	1: "Krellan: 'Outhole (ball lift)'.",
	13: "Krellan: 'Top Diverter (behind and to the left of top lanes, blocks left orbit)'.",
	14: "Krellan: 'Left Ramp Entrance Raise (reveals entrance to Hideout when raised)'.",
	15: "Krellan: 'Bottom Jet Bumper'.",
	16: "Krellan: 'Right Jet Bumper'.",
	17: "Krellan: 'Left Jet Bumper'.",
	19: "Krellan: 'Flasher under \"Sudden\" (near flippers)'.",
	20: "Krellan: 'Big Al (bad yellow guy on backglass)'.",
	24: "Krellan: 'Flasher under \"Death\" (near flippers)'.",
	25: "Krellan: 'Flasher under \"Start Feature\" (in captive ball lane)'.",
	27: "Krellan: 'Flasher under Power Meter'.",
	28: "Krellan: 'Flasher under \"Hotel Lex\" (sign near slot machine)'.",
	29: "Krellan: 'Flasher under East light (right orbit)'.",
	30: "Krellan: 'Behind Left Drop Targets (lamp post by \"Flower Shop\" ...)'.",
	31: "Krellan: 'Behind Right Drop Targets'.",
	32: "Krellan: 'Autoplunger (ball launcher)'.",
}


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def rom_alias(name: str) -> dict[str, str]:
	return {"namespace": "kingpin.rom-name", "value": name}


LAMP_WORD_CASE = {"GI": "G.I.", "G.I.": "G.I.", "KING": "KING", "PIN": "PIN", "LEX": "Lex", "AL": "Al", "&": "&"}


def lamp_label(rom_name: str) -> str:
	"""Expand the ROM's lamp abbreviations; bulb annotations move to physical fields."""
	text = re.sub(r"\s*\((?:2|RED|2,RED)\)$", "", rom_name.replace("G.I.(2)", "G.I. (2)")).strip()
	text = re.sub(r"^U\.R\. ", "UPPER RIGHT ", text)
	text = re.sub(r"^L\. ", "LEFT ", text)
	text = re.sub(r"^R\. ", "RIGHT ", text)
	text = re.sub(r"^C\. ", "CENTER ", text)
	words = []
	for word in text.split():
		if word in LAMP_WORD_CASE:
			words.append(LAMP_WORD_CASE[word])
		elif re.fullmatch(r"[0-9.]+X?|\.45", word):
			words.append(word)
		elif "'" in word:
			head, tail = word.split("'", 1)
			words.append(head.capitalize() + "'" + tail.lower())
		elif "/" in word:
			words.append("/".join(part.capitalize() for part in word.split("/")))
		else:
			words.append(word.rstrip(",").capitalize() + ("," if word.endswith(",") else ""))
	return " ".join(words)


def lamp_bulbs(rom_name: str) -> tuple[int, bool]:
	match = re.search(r"\((2|RED|2,RED)\)$", rom_name.replace("G.I.(2)", "G.I. (2)"))
	annotation = match.group(1) if match else ""
	return (2 if "2" in annotation else 1), ("RED" in annotation)


def split_wire(text: str) -> tuple[str, str]:
	"""Split a ROM wire line such as 'BRN-BLK J14/13.1' into colour code and connector."""
	colour, connector = text.split(" ", 1)
	for token in colour.split("-"):
		if token not in WIRE_COLOURS:
			raise ValueError(f"unexpected wire colour token {token!r} in {text!r}")
	return colour, connector


def excerpt(identifier: str, locator: str, stem: str, *, image: bool, method: str, transcribed_by: str) -> dict[str, Any]:
	path = EXCERPT_DIR / f"{stem}.md"
	record: dict[str, Any] = {
		"id": identifier,
		"locator": locator,
		"path": path.relative_to(ROOT).as_posix(),
		"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
		"method": method,
		"transcribed_by": transcribed_by,
		"reviewed": True,
	}
	if image:
		image_path = EXCERPT_DIR / f"{stem}.webp"
		record["image"] = image_path.relative_to(ROOT).as_posix()
		record["image_sha256"] = hashlib.sha256(image_path.read_bytes()).hexdigest()
		record["image_derivation"] = (
			"Lossless grayscale WebP contact sheet of the harness's own 128x32 PGM DMD snapshots for the decoded "
			"steps, pasted unscaled in table order with 2-pixel gutters (review-artifacts/kingpin/ocr/make_excerpts.py)"
		)
	return record


HARNESS_LOCATOR = (
	f"LibPinMAME pinmame64.dll SHA-256 {LIBRARY_SHA256} built from vpinball/pinmame {PINMAME_REVISION}; "
	f"ROM archive kpb105.zip SHA-256 {ROM_ARCHIVE_SHA256}; fresh isolated NVRAM per run; raw run and every DMD "
	"frame retained under review-artifacts/kingpin/harness-runs"
)
DMD_TRANSCRIBER = "DMD glyph matcher (review-artifacts/kingpin/ocr), checked by curator against the frames"
KRELLAN_TRANSCRIBER = "curator (HTML table cells extracted verbatim)"
VPXTABLE_BLOB = f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/"
STANDALONE_BLOB = f"https://github.com/jsm174/vpx-standalone-scripts/blob/{STANDALONE_SCRIPTS_REVISION}/"


def _runtime_evidence() -> dict[str, Any]:
	return load_json(RUNTIME_EVIDENCE_PATH)


def _run_locator(scenario: str, locator: str) -> str:
	"""Pin a harness-derived claim to its exact raw run through the committed evidence bundle."""
	run = next(run for run in _runtime_evidence()["runtime"]["raw_runs"] if run["name"] == scenario)
	return (
		f"{locator}; raw run {run['name']} (SHA-256 {run['sha256']}) from scenario {run['scenario_path']} "
		f"(SHA-256 {run['scenario_sha256']}), summarized in evidence/runtime/capcom/kingpin-service-diagnostics.json; {HARNESS_LOCATOR}"
	)


def _runtime_uri() -> dict[str, str]:
	return {
		"uri": "internal:" + RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix(),
		"sha256": hashlib.sha256(RUNTIME_EVIDENCE_PATH.read_bytes()).hexdigest(),
	}


def service_source(identifier: str, scenario: str, locator: str, excerpts: list[dict[str, Any]] | None = None) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier,
		"kind": "service_diagnostic",
		**_runtime_uri(),
		"revision": PINMAME_REVISION,
		"locator": _run_locator(scenario, locator),
		"license": "NOASSERTION",
		"attribution": "Capcom Coin-Op kpb105 service menu, executed locally with LibPinMAME",
	}
	if excerpts:
		record["excerpts"] = excerpts
	return record


def runtime_source(identifier: str, scenario: str, locator: str) -> dict[str, Any]:
	return {
		"id": identifier,
		"kind": "runtime_scenario",
		**_runtime_uri(),
		"revision": PINMAME_REVISION,
		"locator": _run_locator(scenario, locator),
		"license": "NOASSERTION",
		"attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
	}


def script_source(identifier: str, uri: str, revision: str, sha256: str, locator: str, attribution: str) -> dict[str, Any]:
	return {
		"id": identifier,
		"kind": "vpx_script",
		"uri": uri,
		"revision": revision,
		"sha256": sha256,
		"locator": locator,
		"license": "NOASSERTION",
		"attribution": attribution,
		"known_working": False,
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames driver record kpb105 (the single Kingpin driver; no clones)",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/capgames.c:335-351 (INITGAMEFF(kpb105, 11, cc_dispDMD128x32, 3, SNDBRD_CAPCOMS, 9, 0x70d5), "
				"capInvSw11, FLIP, ROM SHA-1s); src/wpc/capcom.c (cc_sw2m/cc_m2sw, io_w solenoid words and the 9-12 legacy "
				"flipper mirrors, MACHINE_INIT(cc) nLamps and the strncasecmp(gn, \"kpb\", 3) flasher typing 18-19/21-31); "
				"src/wpc/capcom.h (CC_COMPORTS)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/capcom.json",
			"revision": "repository",
			"locator": "Reviewed Capcom switch, solenoid (legacy flipper mirrors, Fast Flips address 51) and lamp address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-review-artifacts/kingpin/rom/records-tool.json",
			"revision": PROGRAM_ROM_SHA1,
			"locator": (
				f"kpb105 program ROM u1hu1l.bin (SHA-1 {PROGRAM_ROM_SHA1}) I/O name-record table at ROM offsets "
				"0x0b453a-0x0b51c6, decoded by tools/capcom_kingpin_rom_records.py: 123 lamp, 46 switch and 30 coil records; "
				"the cabinet-switch name list at 0x0d0cfc-0x0d0d92; the version, opto-supply and 50 V interlock strings listed in the excerpt"
			),
			"license": "NOASSERTION",
			"attribution": "Capcom Coin-Op program ROM, user-authorized local copy; ROM bytes are not redistributed",
			"excerpts": [
				excerpt("excerpt.kingpin.rom-io-name-records", "ROM offsets 0x0b453a-0x0b51c6 (all 199 records), 0x0d0cfc-0x0d0d92 (cabinet switch names) and the cited strings", "rom-io-name-records", image=False, method="mixed", transcribed_by="tools/capcom_kingpin_rom_records.py and a string dump, reviewed by curator"),
			],
		},
		service_source(
			SOLENOID_TEST_SOURCE, "kpb105-solenoid-test", "C DIAGNOSTICS > C1 STANDARD TESTS > C1.03 SOLENOID TEST, S01-S32",
			[excerpt("excerpt.kingpin.service-solenoid-test", "C1.03 Solenoid Test, S01-S32 with the public address each selection fired", "service-solenoid-test", image=True, method="mixed", transcribed_by=DMD_TRANSCRIBER)],
		),
		service_source(
			LAMP_TEST_SOURCE, "kpb105-lamp-test", "C DIAGNOSTICS > C1 STANDARD TESTS > C1.04 LAMP TEST, single-lamp walk forward and backward, 11A-88B",
			[excerpt("excerpt.kingpin.service-lamp-test", "C1.04 Lamp Test, lamps 11A-88B with the public lamp each step lit", "service-lamp-test", image=True, method="mixed", transcribed_by=DMD_TRANSCRIBER)],
		),
		service_source(
			SWITCH_TEST_SOURCE, "kpb105-switch-test", "C DIAGNOSTICS > C1 STANDARD TESTS > C1.01 SWITCH TEST, public switches 1-4 and 9-80 held one at a time",
			[excerpt("excerpt.kingpin.service-switch-test", "C1.01 Switch Test, the ROM's switch number, name, wiring and contact-state icon for each held public switch", "service-switch-test", image=True, method="mixed", transcribed_by=DMD_TRANSCRIBER)],
		),
		service_source(
			OPTO_TEST_SOURCE, "kpb105-opto-test", "C1.02 OPTO TEST entry prompt: DISCONNECT THE OPTO POWER CONNECTOR J15 FROM THE POWER BOARD",
		),
		service_source(
			TROUBLESHOOTING_BASELINE_SOURCE, "kpb105-troubleshooting-baseline",
			"C DIAGNOSTICS > C5 TROUBLESHOOTING with only the trough optos 36-39 and the ramp-down switch 47 held at 1 from power-up: INFO 0-SW",
		),
		service_source(
			TROUBLESHOOTING_HELD_SOURCE, "kpb105-troubleshooting-held",
			"C DIAGNOSTICS > C5 TROUBLESHOOTING with 1-4, 13-39, 41-46, 48-55 and 57-63 held at 1 from power-up and 47 at 0: INFO 28-SW",
			[excerpt("excerpt.kingpin.service-troubleshooting", "C5 Troubleshooting, the switches it lists in the baseline, held and slam-tilt runs", "service-troubleshooting", image=True, method="mixed", transcribed_by=DMD_TRANSCRIBER)],
		),
		service_source(
			TROUBLESHOOTING_SLAM_SOURCE, "kpb105-troubleshooting-slam-tilt",
			"C DIAGNOSTICS > C5 TROUBLESHOOTING with the slam (9) and tilt (10) switches held at 1 from power-up: INFO 2-SW",
		),
		runtime_source(
			DROP_RUN_SOURCE, "kpb105-drop-targets",
			"A game with four balls in the trough: one KING target (25) alone to public 1 and back, all four KING targets (25-28) to 1 "
			"and back, all three PIN targets (29-31) to 1 and back; reset coils 6 and 7 per step",
		),
		runtime_source(RAMP_RUN_SOURCE, "kpb105-ramp-down-feedback", "Attract mode with public switch 47 open, then closed, then open again; public solenoid 14 activity per phase"),
		runtime_source(SERVE_RUN_SOURCE, "kpb105-ball-serve", "Full trough (36-39), coin, Start, shooter lane 43, launch button 14, outhole 35; solenoid response per step"),
		{
			"id": KRELLAN_SOURCE,
			"kind": "human_review",
			"uri": "http://www.krellan.com/pinball/kingpin/",
			"sha256": KRELLAN_PAGE_SHA256,
			"locator": (
				"Krellan's 'Capcom Kingpin \"Manual\"' page: lamp matrices A/B (positions checked on a real machine in operator mode), "
				"switch table (optos in italic), solenoid table, slot-machine drum rows and hardware notes; retained copy "
				"external:pinmame-manuals/by-machine/capcom.kingpin.1996/krellan-kingpin-index.html"
			),
			"license": "NOASSERTION",
			"attribution": "Krellan (krellan.com); unofficial community documentation of a real Kingpin machine",
			"acquired_at": "2026-09-25T11:40:00Z",
			"excerpts": [
				excerpt("excerpt.kingpin.krellan-lamp-matrix-a", "Lamp Matrix A table", "krellan-lamp-matrix-a", image=False, method="manual", transcribed_by=KRELLAN_TRANSCRIBER),
				excerpt("excerpt.kingpin.krellan-lamp-matrix-b", "Lamp Matrix B table", "krellan-lamp-matrix-b", image=False, method="manual", transcribed_by=KRELLAN_TRANSCRIBER),
				excerpt("excerpt.kingpin.krellan-switch-table", "Switch Table", "krellan-switch-table", image=False, method="manual", transcribed_by=KRELLAN_TRANSCRIBER),
				excerpt("excerpt.kingpin.krellan-solenoid-table", "Solenoid Table", "krellan-solenoid-table", image=False, method="manual", transcribed_by=KRELLAN_TRANSCRIBER),
				excerpt("excerpt.kingpin.krellan-slot-machine-and-notes", "Slot Machine Rows table and hardware notes", "krellan-slot-machine-and-notes", image=False, method="manual", transcribed_by="curator (verbatim fragments)"),
			],
		},
		script_source(
			SCRIPT_SOURCE, VPXTABLE_BLOB + "Kingpin%20%28Capcom%201996%291.2.vbs", VPXTABLE_SCRIPTS_REVISION, SCRIPT_SHA256,
			"Kingpin (Capcom 1996)1.2.vbs: SolCallback, Controller.Switch/PulseSw, NFadeL lamp bindings, slot-machine and ramp routines; the script's own header says '!! NOTE : Table not verified yet !!'",
			"Authors credited in Kingpin (Capcom 1996)1.2.vbs (Thalamus 2019 sound update) and repository contributors",
		),
		script_source(
			SCRIPT_OLD_SOURCE, VPXTABLE_BLOB + "kingpin%20080715a.vbs", VPXTABLE_SCRIPTS_REVISION, SCRIPT_OLD_SHA256,
			"kingpin 080715a.vbs: an earlier release of the same table-script lineage (identical I/O bindings)",
			"Authors credited in kingpin 080715a.vbs and repository contributors",
		),
		script_source(
			SCRIPT_MOD_SOURCE,
			STANDALONE_BLOB + "Kingpin%20%28Capcom%201996%29_Bigus%28MOD%293.0/Kingpin%20%28Capcom%201996%29_Bigus%28MOD%293.0.vbs",
			STANDALONE_SCRIPTS_REVISION, SCRIPT_MOD_SHA256,
			"Kingpin (Capcom 1996)_Bigus(MOD)3.0.vbs: a modification of the same lineage (identical I/O bindings). The retained SHA-256 is the "
			"repository checkout's CRLF materialization (the corpus sets eol=crlf for .vbs); the linked Git blob is the identical LF-normalized text "
			"(SHA-256 6f740d30997b177972bfad1127dfafd1d3dd53c71982d47243a051dc029fb81d).",
			"Authors credited in Kingpin (Capcom 1996)_Bigus(MOD)3.0.vbs and repository contributors",
		),
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"aliases": extra.pop("aliases"),
		"availability": availability,
		"provenance": provenance(*refs, status=status),
	}
	device.update(extra)
	return device


def switch_id(address: int) -> str:
	return f"switch.{address}"


def solenoid_id(address: int) -> str:
	return f"solenoid.{address}"


def lamp_id(address: int) -> str:
	return f"lamp.{address}"


def switch_wiring(address: int) -> dict[str, Any]:
	entry = DIAG_SWITCHES[address]
	signal_colour, signal_pin = split_wire(entry[1])
	return_colour, return_pin = split_wire(entry[2])
	return {
		"control_wire": signal_colour,
		"control_connection": signal_pin,
		"return_wire": return_colour,
		"return_connection": return_pin,
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		rom_name = DIAG_SWITCHES[address][0] if address in DIAG_SWITCHES else CABINET_SWITCHES[address][1]
		unused = rom_name == "NOT USED"
		label = (CABINET_SWITCHES[address][0] if address in CABINET_SWITCHES else SWITCH_LABELS.get(address)) or f"Not Used Switch {address}"
		refs: list[str] = [CORE_SOURCE, CONTROLLER_SOURCE]
		notes = []
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, rom_alias(rom_name)]}
		if address in DIAG_SWITCHES:
			refs.insert(0, SWITCH_TEST_SOURCE)
			shown = DIAG_SWITCHES[address]
			how = " (browsed with the flipper buttons, because this input drives the menu)" if address in (5, 6, 7, 8) else ""
			notes.append(f"ROM Switch Test prints {address:02d}) '{rom_name}'{how}, switch line {shown[1]}, return {shown[2]}.")
			extra["wiring"] = switch_wiring(address)
		else:
			notes.append(
				f"Cabinet input; name '{rom_name}' from the ROM's cabinet-switch string table. Public {address} is a CC_COMPORTS "
				"input (src/wpc/capcom.h) and drives the service-menu navigation used by every harness scenario."
			)
			refs.insert(0, ROM_SOURCE)
		if address in ROM_SWITCH_NUMBERS:
			refs.append(ROM_SOURCE)
			notes.append(f"ROM I/O record {ROM_SWITCH_NUMBERS[address]} (internal number) names it '{rom_name}'.")
		if address in KRELLAN_SWITCH_NOTES:
			refs.append(KRELLAN_SOURCE)
			notes.append(KRELLAN_SWITCH_NOTES[address])
		if unused:
			notes.append("The ROM's own Switch Test names this position NOT USED; nothing is fitted.")
			extra["spatial"] = not_applicable("unused", SWITCH_TEST_SOURCE)
			physical["notes"] = " ".join(notes)
			extra["physical"] = physical
			items.append(_device(switch_id(address), label, "switch", "pinmame.input.switch", address, "unused", tuple(refs), **extra))
			continue
		if address in OPTO_SWITCHES:
			physical["switch_type"] = "opto"
			notes.append(
				"Opto: PinMAME's capInvSw11 mask normalizes this address, the ROM's switch record carries its opto flag, the ROM's Switch "
				"Test draws it as a beam rather than a contact, and Krellan's hands-on chart sets it in italic (optos). The public state is already normalized and must not be inverted again; the "
				"ROM's Opto Test identifies connector J15 on the power board as the opto supply."
			)
			refs += [ROM_SOURCE, KRELLAN_SOURCE, OPTO_TEST_SOURCE]
		elif address in {5, 6, 7, 14}:
			physical["switch_type"] = "button"
		elif address in {9, 10}:
			physical["switch_type"] = "tilt"
		else:
			physical["switch_type"] = "unknown"
		if address in CABINET_SWITCH_ADDRESSES:
			physical["location"] = "cabinet"
			extra["spatial"] = not_applicable("cabinet_or_service", SWITCH_TEST_SOURCE if address in DIAG_SWITCHES else ROM_SOURCE)
			if address in CABINET_ROLES:
				extra["roles"] = CABINET_ROLES[address]
		if address in SWITCH_EXTRA_NOTES:
			notes.append(SWITCH_EXTRA_NOTES[address])
		refs += SWITCH_EXTRA_REFS.get(address, [])
		if address in OPTO_SWITCHES:
			extra["normally_closed"] = True
			ball = (
				" The ball-serve run holds it at 1 for a ball present, and the ROM serves from the trough."
				if address in (36, 37, 38, 39) else ""
			)
			notes.append(
				"Contact polarity: the ROM's Switch Test draws this switch as a beam, broken while it is held at public 1 and clear at "
				f"public 0.{ball} core_setSw applies capInvSw11 to this address and capcom.c's io_r complements the switch-board read, so "
				"the CPU sees the contact open while the beam is blocked and closed while it is clear: normally closed."
			)
			if address in (36, 37, 38, 39):
				refs.append(SERVE_RUN_SOURCE)
		else:
			extra["normally_closed"] = False
			drawn = (
				"closed at 1 (the coin door switch stays at 1 while the menu is open)" if address == 8
				else "open at 0 (browsed with the button released)" if address in (5, 6, 7)
				else "closed at 1 and open at 0"
			)
			read_path = (
				"PinMAME does not mask this address and capcom.c's io_r complements the active-low read, so public 1 is the CPU's "
				f"closed-contact reading, and the ROM's Switch Test draws the contact {drawn}."
			)
			if address in TROUBLESHOOTING_REPORTED_AT_1:
				notes.append(
					"Contact polarity: the ROM's C5 Troubleshooting report lists this switch when it is held at public 1 from power-up, "
					f"and lists no switch in the baseline run, so the ROM expects it at 0 with the machine at rest. {read_path} The contact "
					"therefore rests open: normally open."
				)
				refs.append(TROUBLESHOOTING_HELD_SOURCE if address not in (9, 10) else TROUBLESHOOTING_SLAM_SOURCE)
				refs.append(TROUBLESHOOTING_BASELINE_SOURCE)
			elif address in TROUBLESHOOTING_REPORTED_AT_0:
				notes.append(
					"Contact polarity: the ROM's C5 Troubleshooting report lists this switch when it is left at 0 and not while it rests at 1, "
					"so the ROM expects the ramp-down contact closed while the ramp rests down. The lowered ramp actuates it (Krellan: "
					"'active when lowered'), and normally_closed describes the contact itself, open until actuated, not where the ramp "
					f"happens to rest. {read_path} Normally open."
				)
				refs += [TROUBLESHOOTING_HELD_SOURCE, TROUBLESHOOTING_BASELINE_SOURCE]
			elif address in DROP_TARGET_RESET:
				bank = "KING" if DROP_TARGET_RESET[address] == 6 else "PIN"
				pulses = "four pulses" if bank == "KING" else "six pulses"
				notes.append(
					f"Contact polarity: the Troubleshooting report does not check it (listed neither at 0 in the baseline run nor at 1 in "
					f"the held run). In the drop-target run, a game with every target at 0 draws no reset for 8 s; with every {bank} target "
					f"at public 1 the ROM fires the {bank} reset coil {DROP_TARGET_RESET[address]} repeatedly ({pulses}); one KING target "
					f"alone at 1 draws no reset. So public 1 is the target down and 0, the target standing, is its rest level. {read_path} "
					"Normally open."
				)
				refs += [DROP_RUN_SOURCE, TROUBLESHOOTING_HELD_SOURCE, TROUBLESHOOTING_BASELINE_SOURCE]
			else:
				checked = (
					"the Troubleshooting report does not check it (listed neither at 0 in the baseline run nor at 1 in the held run). "
					if address in TROUBLESHOOTING_UNCHECKED else ""
				)
				notes.append(
					f"Contact polarity: {checked}{read_path} Normally open is the ordinary construction of a mechanical contact, which "
					"Krellan lists among the 'normal switches' as opposed to the optos; no source prints this switch's contact type."
				)
				if address in TROUBLESHOOTING_UNCHECKED:
					refs += [TROUBLESHOOTING_HELD_SOURCE, TROUBLESHOOTING_BASELINE_SOURCE]
			if address in CONTACT_POLARITY_NOTES:
				notes.append(CONTACT_POLARITY_NOTES[address])
		physical["notes"] = " ".join(notes)
		extra["physical"] = physical
		if address in PULSED_SWITCHES:
			extra["pulse"] = True
			refs.append(SCRIPT_SOURCE)
		availability = "optional" if address in OPTIONAL_SWITCHES else "used"
		items.append(_device(switch_id(address), label, "switch", "pinmame.input.switch", address, availability, tuple(refs), **extra))
	items.append(
		_device(
			"switch.synthetic-flipper-column",
			"PinMAME Synthetic Flipper EOS and Upper-Flipper Bits",
			"virtual",
			"pinmame.input.switch",
			81,
			"unused",
			(CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": "81"}],
			physical={
				"notes": (
					"Addresses 81-88 are PinMAME's internal flipper column (CORE_FLIPPERSWCOL = 11, cc_m2sw row + 81). This record covers "
					"81, 83 and 85-88. core_updateSw's end-of-stroke model writes the end-of-stroke bits 81, 83, 85 and 87 every frame, and "
					"the upper-flipper button bits 86 and 88 are written back unchanged. No Capcom circuit is behind them and the ROM "
					"never reads the column; the machine's real "
					"end-of-stroke switches are public 33/34. The two lower-flipper button bits are recorded separately at 82 and 84, "
					"because PinMAME copies them into the ROM-read switches 5/6."
				)
			},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	for address, side, target in ((82, "Right", 6), (84, "Left", 5)):
		bit = "CORE_SWLRFLIPBUTBIT (0x02)" if address == 82 else "CORE_SWLLFLIPBUTBIT (0x08)"
		items.append(
			_device(
				f"switch.{address}",
				f"{side} Flipper Button Host Input",
				"virtual",
				"pinmame.input.switch",
				address,
				"used",
				(CORE_SOURCE, CONTROLLER_SOURCE, SWITCH_TEST_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				physical={
					"notes": (
						f"PinMAME's {side.lower()} flipper button bit {bit} in the flipper column, public {address} by cc_m2sw. kpb105 declares "
						f"FLIP_SWNO(5,6), and with keyboard handling off (LibPinMAME's default, and the retained table's HandleKeyboard = 0) "
						f"core_updateSw reads this bit and writes it into matrix switch {target} every frame (src/wpc/core.c, 'set switches in "
						f"matrix for non-fliptronic games'). A host therefore presses the physical {side.lower()} flipper button by driving "
						f"{address}; a direct write to {target} lasts at most one frame. Every harness scenario presses the flippers this way."
					)
				},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	items.append(
		_device(
			"switch.unused-platform-column-10",
			"Unused Platform Switch Column 10",
			"virtual",
			"pinmame.input.switch",
			89,
			"unused",
			(CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": "89"}],
			physical={"notes": "Addresses 89-96 exist only because CORE_STDSWCOLS reserves 12 columns; no cc driver reads or writes them."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 33):
		rom_name, drive, supply = DIAG_SOLENOIDS[address]
		kind = "flasher" if address in FLASHER_SOLENOIDS else "motor" if address in MOTOR_SOLENOIDS else "coil"
		drive_colour, drive_pin = split_wire(drive)
		supply_parts = supply.split()
		wiring: dict[str, Any] = {"drive_wire": drive_colour, "drive_connection": drive_pin}
		if supply_parts[0] not in {"50V", "20V", "12V"}:
			wiring["power_wire"] = supply_parts[0]
			voltage = supply_parts[1]
		else:
			voltage = supply_parts[0]
		wiring["nominal_voltage_v"] = float(voltage.rstrip("V"))
		refs = [SOLENOID_TEST_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE]
		fired = "public 20 pulses throughout the test, so this step cannot isolate it" if address == 20 else f"selecting it fired public {address}"
		notes = [f"ROM Solenoid Test prints S{address:02d} - {rom_name}, drive {drive}, supply {supply}; {fired}."]
		if address in ROM_COIL_NUMBERS:
			refs.append(ROM_SOURCE)
			notes.append(f"ROM I/O record {ROM_COIL_NUMBERS[address]} (internal number) names it '{rom_name}'.")
		if address in KRELLAN_SOLENOID_NOTES:
			refs.append(KRELLAN_SOURCE)
			notes.append(KRELLAN_SOLENOID_NOTES[address])
		if address in SOLENOID_EXTRA_NOTES:
			notes.append(SOLENOID_EXTRA_NOTES[address])
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, rom_alias(rom_name)],
			"wiring": wiring,
			"physical": {"notes": " ".join(notes)},
		}
		if address == 20:
			# Krellan places Big Al on the backglass but also says some flashers may be on both the backglass and the
			# playfield, so the backbox-only placement is observed, not validated.
			extra["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(KRELLAN_SOURCE, SOLENOID_TEST_SOURCE, status="observed")}
			extra["physical"]["location"] = "backbox"
		if address in SOLENOID_ROLES:
			extra["roles"] = SOLENOID_ROLES[address]
		refs += SOLENOID_EXTRA_REFS.get(address, [])
		items.append(_device(solenoid_id(address), SOLENOID_LABELS[address], kind, "pinmame.output.solenoid", address, "used", tuple(refs), **extra))
	for address, target in ((33, 11), (35, 12), (45, 9), (47, 10)):
		items.append(
			_device(
				solenoid_id(address),
				f"Legacy Mirror of {SOLENOID_LABELS[target]}",
				"virtual",
				"pinmame.output.solenoid",
				address,
				"used",
				(SOLENOID_TEST_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				physical={
					"notes": (
						f"capcom.c's io_w mirrors physical solenoid {target} into public {address} for old DOF configurations; the "
						f"Solenoid Test walk fired {address} together with {target}. No device of its own: consume public {target}."
						+ (" On Kingpin the mirrored circuit is not a flipper at all, whatever PinMAME's flipper-shaped name suggests." if target in {11, 12} else "")
					)
				},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	for address in (34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50):
		items.append(
			_device(
				solenoid_id(address),
				f"Unused Solenoid Address {address}",
				"virtual",
				"pinmame.output.solenoid",
				address,
				"unused",
				(CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				physical={"notes": "No cc driver writes this public address; it stays zero."},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	items.append(
		_device(
			solenoid_id(51),
			"Fast Flips Game-On State",
			"virtual",
			"pinmame.output.solenoid",
			51,
			"used",
			(CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": "51"}],
			physical={
				"notes": (
					"INITGAMEFF(kpb105, ..., 0x70d5) declares hw.custSol = 1 and a getsol callback that reports the RAM byte at 0x70d5 "
					"(> 0), a game-on flag the driver comment says goes from 128 to 0 during the bonus collection sequence. Synthetic "
					"state for fast-flip consumers, not a driver-board circuit."
				)
			},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 129):
		code, rom_name, column_line, row_line = DIAG_LAMPS[address]
		unused = rom_name == "NOT USED"
		refs = [LAMP_TEST_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE]
		notes = [f"ROM Lamp Test prints {code} - {rom_name}: column {column_line}, row {row_line}."]
		column_parts = column_line.split(" ")
		row_parts = row_line.split(" ")
		wiring = {
			"control_wire": column_parts[2],
			"control_connection": column_parts[1],
			"drive_wire": row_parts[2],
			"drive_connection": row_parts[1],
		}
		for colour in (wiring["control_wire"], wiring["drive_wire"]):
			split_wire(colour + " x")
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "kingpin.lamp-matrix", "value": code}, rom_alias(rom_name)], "wiring": wiring}
		if address in ROM_LAMP_NUMBERS:
			refs.append(ROM_SOURCE)
		if unused:
			notes.append("The ROM's own Lamp Test names this matrix position NOT USED, and Krellan's chart marks it NU.")
			refs.append(KRELLAN_SOURCE)
			extra["physical"] = {"notes": " ".join(notes)}
			extra["spatial"] = not_applicable("unused", LAMP_TEST_SOURCE)
			items.append(_device(lamp_id(address), f"Not Used Lamp {code}", "lamp", "pinmame.output.lamp", address, "unused", tuple(refs), **extra))
			continue
		quantity, red = lamp_bulbs(rom_name)
		physical: dict[str, Any] = {}
		if quantity > 1:
			physical["quantity"] = quantity
			notes.append("The ROM's '(2)' annotation marks two bulbs on this output.")
		if red:
			notes.append("The ROM's 'RED' annotation marks a red bulb.")
		if address in KRELLAN_LAMPS:
			refs.append(KRELLAN_SOURCE)
			notes.append(f"Krellan (checked on a real machine): '{KRELLAN_LAMPS[address]}'.")
		if address in LAMP_EXTRA_NOTES:
			notes.append(LAMP_EXTRA_NOTES[address])
		physical["notes"] = " ".join(notes)
		if address in CABINET_LAMPS:
			physical["location"] = CABINET_LAMPS[address]
			extra["spatial"] = not_applicable("cabinet_or_service", LAMP_TEST_SOURCE, KRELLAN_SOURCE)
		extra["physical"] = physical
		label = lamp_label(rom_name)
		items.append(_device(lamp_id(address), label, "lamp", "pinmame.output.lamp", address, "used", tuple(refs), **extra))
	for address, label in ((129, "CPU Board Diagnostic LED"), (130, "Sound Board Diagnostic LED")):
		items.append(
			_device(
				lamp_id(address), label, "virtual", "pinmame.output.lamp", address, "used", (CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={"notes": "MACHINE_INIT(cc) publishes the board diagnostic LED in the extra lamp column after the two matrices (nLamps = 64 + 9 * 8 = 136)."},
				spatial=not_applicable("internal_nonvisual", CORE_SOURCE),
			)
		)
	for address in range(131, 137):
		items.append(
			_device(
				lamp_id(address), f"Unused Diagnostic Column Address {address}", "virtual", "pinmame.output.lamp", address, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={"notes": "The last six addresses of the diagnostic column are typed CORE_MODOUT_NONE by MACHINE_INIT(cc)."},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


# Exactly the switches the retained script lineage reports with vpmTimer.PulseSw: both spinners, the
# three star bumpers and the four standups. It is a lead for how a recreation reports them, cited to
# that script.
PULSED_SWITCHES = {17, 49, 50, 57, 58, 59, 60, 61, 63}

SWITCH_EXTRA_NOTES = {
	5: "The ROM reads the left flipper button here, but under PinMAME a host must drive public 84: core_updateSw overwrites this switch from that button bit every frame (see switch.84). The retained script lineage writes Controller.Switch(5) from its flipper key, which PinMAME overwrites in the same way; that is a defect of the table, not of the machine.",
	6: "The ROM reads the right flipper button here, but under PinMAME a host must drive public 82: core_updateSw overwrites this switch from that button bit every frame (see switch.82). The retained script lineage writes Controller.Switch(6) from its flipper key, which PinMAME overwrites in the same way; that is a defect of the table, not of the machine.",
	8: "CC_COMPORTS labels this input Coin Door and declares it a toggle (COREPORT_BITTOG). Krellan calls it the operator's Advance button, not a coin lockout. Every harness scenario enters the operator menu by making this switch; the flipper buttons then step and Start selects. The ROM's 50 V interlock message ('Check 50V Interlock SW.', French 'VERIFIE SW.PORTE 50V', German 'PRUEFE 50V TUERSCHALTER') refers to a door switch in the 50 V supply, and no source ties that interlock to this input.",
	14: "The ROM's own I/O record for this cabinet input is 'AUTO PLUNGER', the name it also gives coil 32; the cabinet lamp at public 4 carries the same name.",
	32: "The retained script lineage's captive-ball target object pulses switch 49 instead of 32 (`Sub sw32_Hit : vpmTimer.PulseSw 49`), a defect in that table, not in the machine: the ROM names 32 CAPTIVE BALL and 49 L. SLOT STANDUP.",
	33: "Capcom flippers are CPU-driven (FLIP_SOL for all four positions, src/wpc/capgames.c); the ROM reads this end-of-stroke switch itself. PinMAME does not synthesize it, and the retained script lineage never drives it.",
	34: "Capcom flippers are CPU-driven (FLIP_SOL for all four positions, src/wpc/capgames.c); the ROM reads this end-of-stroke switch itself. PinMAME does not synthesize it, and the retained script lineage never drives it.",
	47: "The ramp-down-feedback scenario shows the ROM driving RAMP (public 14) for about 1.3 s, resting about 1.0 s and repeating while this switch is open, and stopping as soon as it closes: the ROM uses it as the lowered-position feedback of the left ramp entrance (Krellan: 'active when lowered').",
	35: "The ball-serve scenario shows the ROM firing OUTHOLE (public 1) while this switch is closed in attract.",
	43: "The ball-serve scenario shows the ROM firing AUTO PLUNGER (public 32) when a ball rests here outside a game.",
	52: "The retained script lineage models the slot drum as 360 motor steps with this opto made for 39 of every 40 (nine symbol rows); the ROM treats it as the drum's index sensor. That timing is the table author's model, not a measurement.",
}
SWITCH_EXTRA_REFS = {
	47: [RAMP_RUN_SOURCE],
	35: [SERVE_RUN_SOURCE],
	43: [SERVE_RUN_SOURCE],
}

SOLENOID_EXTRA_NOTES = {
	9: "CPU-driven flipper power (FLIP_SOL); the ROM switches between full power and hold using end-of-stroke switch 33. Also mirrored at legacy public 45.",
	10: "CPU-driven flipper power (FLIP_SOL); the ROM switches between full power and hold using end-of-stroke switch 34. Also mirrored at legacy public 47.",
	11: "Also mirrored at legacy public 33 by capcom.c's fixed flipper-shaped mirror, although this circuit is the slot eject.",
	12: "The ROM's Solenoid Test draws a motor symbol and a 12 V YEL supply for this output (every other coil shows 50 V VIO). Also mirrored at legacy public 35.",
	13: "The ROM's Solenoid Test draws this output with a different symbol from the plain coils. The retained script lineage treats each pulse as a toggle of the left-orbit gate; the physical latch behaviour is not documented.",
	14: "The ramp-down-feedback scenario shows the ROM's software loop: with switch 47 open it drives this coil for about 1.3 s, rests about 1.0 s and repeats (9 drives in 30 s), stops once 47 closes, and resumes when 47 reopens. Whether the lift is a latch that each drive toggles (as the retained script lineage models it) or needs its drive held is not documented.",
	18: "pinned capcom.c types 18-19 and 21-31 as #89 flashers from a VPX table because no manual was found; the ROM prints this output as a 20 V flasher. Krellan reports #67 and #906 flasher bulbs on this machine.",
	20: "The binding still holds: when S20 is selected nothing but 20 changes, and every neighbouring step fires its own number. The ROM prints S20 as a 20 V flasher output; Krellan places Big Al on the backglass, while also saying some flashers may be on both the backglass and the playfield. pinned capcom.c's flasher typing, taken from a VPX table, leaves 20 out, and the retained table lineage does not bind 20, so PinMAME models it as a plain two-state solenoid. During the whole C1.03 Solenoid Test the ROM pulses this output continuously, whichever coil is selected.",
	22: "The retained script lineage binds its right-ramp flasher routine to 23 (`SolCallback(23) = \"RightRampFlash\"`) and a generic flasher object to 22; the ROM names 22 R. RAMP FLASHER and 23 BUILDING FLASHER. That is a defect in the table, not a question about the machine.",
	29: "See conflict.flasher-29-orbit-side: the ROM's own name points at the left orbit while calling it EAST, and Krellan puts it under the East light at the right orbit.",
	32: "The ball-serve scenario shows the ROM firing this coil on its own when a ball rests in the shooter lane (43) outside a game. The cabinet launch button (14) is the player's control for it in play; the harness, having no ball model, does not isolate that path.",
	1: "The ball-serve scenario shows the ROM firing this coil when the outhole switch (35) closes in attract, again about every 1.2 s while it stays closed, and once more about 0.7 s after it opens.",
	2: "The ball-serve scenario shows the ROM firing this coil when a game starts with a credit and balls held on trough switches 36-39; the same Start also fires both drop-target resets (6, 7), runs the slot motor (12) and sets the Fast Flips game-on state (51).",
}
SOLENOID_EXTRA_REFS = {
	1: [SERVE_RUN_SOURCE],
	2: [SERVE_RUN_SOURCE],
	14: [RAMP_RUN_SOURCE],
	32: [SERVE_RUN_SOURCE],
	22: [SCRIPT_SOURCE],
	13: [SCRIPT_SOURCE],
}
SOLENOID_ROLES = {
	9: ["flipper.lower.left.power"],
	10: ["flipper.lower.right.power"],
}
CABINET_LAMPS = {
	1: "cabinet",
	2: "cabinet",
	3: "cabinet",
	4: "cabinet",
	74: "backbox",
	75: "backbox",
	76: "backbox",
	77: "backbox",
	78: "backbox",
	79: "backbox",
	80: "backbox",
	126: "backbox",
}
LAMP_EXTRA_NOTES = {
	1: "Coin-slot lamp; lit continuously in attract.",
	2: "Coin-slot lamp; lit continuously in attract.",
	3: "Start-button lamp.",
	4: "Launch-button lamp (the ROM calls the launch button AUTO PLUNGER).",
	74: "Krellan labels this group 'Backglass Jackpot Jump'; the retained script lineage has no light object for 74-80.",
	126: "Lit continuously in attract.",
}


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, SOLENOID_TEST_SOURCE),
			"provenance": provenance(CORE_SOURCE, SOLENOID_TEST_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: list[str], status: str) -> dict[str, Any]:
		return {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs, status=status),
		}

	return [
		mechanism(
			"mechanism.trough", "Outhole and four-ball trough", "kicker",
			[solenoid_id(1), solenoid_id(2)], [switch_id(35), switch_id(36), switch_id(37), switch_id(38), switch_id(39)],
			"A drained ball lands on the outhole switch (35); the OUTHOLE coil (1), which Krellan calls the ball lift, moves it into a "
			"four-position opto trough (36-39, optos powered through J15). The TROUGH coil (2) feeds one ball to the shooter lane. "
			"Krellan's page says to install four balls. The ball-serve scenario shows the ROM firing 1 when 35 closes in attract (again about "
			"every 1.2 s while it stays closed, once more about 0.7 s after it opens) and 2 when a game starts with balls held on 36-39.",
			[SERVE_RUN_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE], "validated",
		),
		mechanism(
			"mechanism.auto-plunger", "Auto plunger", "kicker",
			[solenoid_id(32)], [switch_id(43), switch_id(14)],
			"The shooter lane (43) holds the served ball; the AUTO PLUNGER coil (32) launches it. The ROM fires 32 on its own when a ball "
			"sits in the shooter lane outside a game (ball-serve scenario). The cabinet launch button (14, which the ROM's I/O record also names "
			"AUTO PLUNGER; Krellan: 'Launch Button (for autoplunger)') is the player's control for it.",
			[SERVE_RUN_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE], "validated",
		),
		mechanism(
			"mechanism.left-ramp-entrance", "Left ramp entrance lift", "diverter",
			[solenoid_id(14)], [switch_id(47)],
			"Krellan: raising the left ramp entrance reveals the Hideout (gun lock) entrance beneath it. Switch 47 reports the lowered "
			"position (Krellan: 'active when lowered'). While 47 is open the ROM drives RAMP (14) for about 1.3 s, rests about 1.0 s and "
			"repeats; it stops once 47 closes. Whether each drive toggles a latch (as the retained script models it) or the lift needs a "
			"held drive is not documented.",
			[RAMP_RUN_SOURCE, SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE], "observed",
		),
		mechanism(
			"mechanism.gun-lock", "Hideout gun lock and hinged-playfield eject", "kicker",
			[solenoid_id(8)], [switch_id(44), switch_id(45), switch_id(46), switch_id(48)],
			"Balls entering the Hideout under the raised left ramp stack in a three-position lock (44 is an opto; 45/46 mechanical). "
			"GUN EJECT (8) kicks a ball out from under the playfield near the left orbit: Krellan reports that the playfield area there "
			"is hinged at the rear, the kick pushes it up, and the ball is fired down at the player. The purpose of GUN TROUGH OPTO (48) "
			"is not documented; Krellan believes it is used when preparing a kickout.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE], "observed",
		),
		mechanism(
			"mechanism.slot-machine", "Slot machine drum", "reel",
			[solenoid_id(12)], [switch_id(52)],
			"One motorized drum (SLOT MOTOR, 12, 12 V) shows nine rows of three identical symbols through the window: Money, Goods, "
			"Sevens, Gangsters, Bars, Power, Guns, Crazy Cash, Cherries (Krellan, in spin order). The drum does not spin three reels "
			"independently. SLOT OPTO (52) indexes it; Krellan notes the motor often stops between rows and the software rounds to the "
			"nearest row. The opto's duty cycle per row is not documented.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE], "observed",
		),
		mechanism(
			"mechanism.slot-saucer", "Slot machine saucer", "kicker",
			[solenoid_id(11)], [switch_id(51)],
			"A ball shot into the slot machine rests on SLOT SAUCER (51) and is kicked out by SLOT EJECT (11), flanked by the left and "
			"right slot standups (49/50).",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE], "observed",
		),
		mechanism(
			"mechanism.king-drop-targets", "KING four-bank drop targets", "drop_target_bank",
			[solenoid_id(6)], [switch_id(25), switch_id(26), switch_id(27), switch_id(28)],
			"Four drop targets K-I-N-G on the left (Krellan: 'left drop target bank'), reset together by KING DROP RESET (6). "
			"The ROM resets the bank when a game starts, and during play when all four targets read down (public 1): the "
			"drop-target run records four pulses of 6 while they stay down, and none for one target alone.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE, DROP_RUN_SOURCE], "observed",
		),
		mechanism(
			"mechanism.pin-drop-targets", "PIN three-bank drop targets", "drop_target_bank",
			[solenoid_id(7)], [switch_id(29), switch_id(30), switch_id(31)],
			"Three drop targets P-I-N on the right (Krellan: 'right drop target bank'), reset together by PIN DROP RESET (7). "
			"The ROM resets the bank when a game starts, and during play when all three targets read down (public 1): the "
			"drop-target run records six pulses of 7 before the ROM stops while they are still down.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE, DROP_RUN_SOURCE], "observed",
		),
		mechanism(
			"mechanism.top-gates", "Top diverter", "gate",
			[solenoid_id(13)], [],
			"TOPGATES (13) moves a diverter behind and to the left of the top lanes that blocks the left orbit (Krellan). No position "
			"switch exists. The retained script lineage toggles the gate on each pulse; the physical behaviour is not documented.",
			[SOLENOID_TEST_SOURCE, KRELLAN_SOURCE, SCRIPT_SOURCE], "candidate",
		),
		mechanism(
			"mechanism.star-bumpers", "Three star (jet) bumpers", "kicker",
			[solenoid_id(17), solenoid_id(15), solenoid_id(16)], [switch_id(57), switch_id(58), switch_id(59)],
			"Left (17 coil, 57 switch), center/bottom (15, 58) and right (16, 59) star bumpers; the ROM names each coil and switch pair "
			"identically. Whether the switch fires the coil directly or through the CPU is not documented; the ROM's coil test drives each "
			"coil on its own.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, KRELLAN_SOURCE], "observed",
		),
		mechanism(
			"mechanism.slingshots", "Slingshots", "kicker",
			[solenoid_id(4), solenoid_id(5)], [switch_id(41), switch_id(42)],
			"Left (4, switch 41) and right (5, switch 42) slingshots.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE], "observed",
		),
		mechanism(
			"mechanism.flippers", "CPU-driven lower flippers", "other",
			[solenoid_id(9), solenoid_id(10)], [switch_id(5), switch_id(6), switch_id(33), switch_id(34)],
			"Two lower flippers driven by the CPU (FLIP_SOL): the ROM reads the buttons at 5/6 (which a PinMAME host drives through the "
			"button bits 84/82), drives the flipper coils (9/10) and uses the end-of-stroke switches (33/34). Krellan: the flipper power is software-adjustable, and in the timed game the "
			"flippers weaken and finally stop when the power meter runs out.",
			[SOLENOID_TEST_SOURCE, SWITCH_TEST_SOURCE, CORE_SOURCE, KRELLAN_SOURCE], "observed",
		),
	]


def relationships() -> list[dict[str, Any]]:
	# The ramp-down-feedback run proves that switch 47 governs whether the ROM drives coil 14 (software
	# feedback). It does not show the coil working the switch, so no physical relationship is asserted.
	return []


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.flasher-29-orbit-side",
			"path": "$.outputs[?(@.binding.group=='pinmame.output.solenoid' && @.binding.device==29)]",
			"description": (
				"The ROM's Solenoid Test names public 29 'L.ORBIT (EAST) FLASHER', but in the ROM's own lamp naming the orbit that carries "
				"the EAST insert is the right orbit (lamp 50 'R. ORBIT POINTS', which Krellan's chart calls 'East $ (right orbit)'), and "
				"Krellan places this flasher 'under East light (right orbit)'. One of the two sources is wrong about which orbit the flasher "
				"lights; Krellan also says he does not know the exact placement of many flashers. Resolution path: locate the flasher-29 "
				"socket on a real machine or in a photograph of one (Krellan's retained photo set, or an owner's inspection)."
			),
			"source_refs": [SOLENOID_TEST_SOURCE, KRELLAN_SOURCE],
		},
	]


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	record = next(driver for driver in catalog["drivers"] if driver["id"] == "kpb105")
	item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
	item["physical_compatibility"] = "identical"
	item["variant_notes"] = (
		"The only Kingpin driver in pinned PinMAME (capgames.c: 'previously known as V1.0 or B1.06'); its operator-menu header shows "
		"'KING PIN' and version 1.5 beta, displayed as β1.5 (program-ROM strings at 0x0b85a2 and 0x0b85ab). The "
		"user's local kpv106.zip is byte-identical to kpb105.zip. Krellan reports two known ROM versions, 1.4 beta and 1.5 beta, each "
		"with a different bug, and that both play styles (standard three-ball and the timed power-meter game) are operator settings "
		"available in either version; no other version is dumped in pinned PinMAME."
	)
	return [item]


COVERAGE_MISSING = [
	"mechanism_behavior",
	"recreation_notes",
	"spatial_placement",
	"unresolved_conflicts",
]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Kingpin",
			"manufacturer": "Capcom",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 4000,
			"opdb_id": "G48od-MJNnn",
		},
		"coverage": {
			"status": "partial",
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "observed",
				"variant_coverage": "validated",
				"recreation_knowledge": "observed",
				"spatial_placement": "unknown",
			},
		},
		"controller": {
			"platform": "pinmame.capcom",
			"hardware_generation": "0x0",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/capcom/kingpin-1996.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Kingpin device identifiers are not unique: {duplicates}")
	return definition


KNOWLEDGE_NOTE = """# Kingpin (Capcom 1996)

Coverage: **partial.** The complete controller contract is validated: every public switch, solenoid
and lamp address, its name, its wiring colour code and connector pin, every fitted switch's contact
polarity (ten by ordinary construction) and the DMD. Still open: spatial placement (no VPX table is retained yet), the physical
behaviour of several mechanisms, one conflict about a flasher's position, and the recreation notes
that depend on those.

## Why this record has no manual

Kingpin was to be Capcom's next pinball machine after Big Bang Bar when Capcom closed its pinball
factory in 1996. Krellan's page puts Big Bang Bar at "10-or-so" machines and calls Kingpin "just as
rare, if not more so". No printed factory manual is known: pinned PinMAME's `capcom.c` says it "did
not find a manual for this one", and Krellan says the same. This definition replaces the manual with
the machine's own firmware plus one hands-on survey:

1. **The ROM's service menu.** Walked on fresh isolated state by the LibPinMAME harness
   (`tools/harness-scenarios/capcom/kpb105-*.json`). The Solenoid, Lamp and Switch Tests print each
   device's name, its wire colours and its connector pin. Each harness step pairs that text with the
   public address that changed (solenoids, lamps) or was held (switches). Every row is transcribed in
   `evidence/excerpts/capcom.kingpin.1996/service-*.md` beside a sheet of the frames, and the runs are
   pinned by hash in `evidence/runtime/capcom/kingpin-service-diagnostics.json`.
2. **The ROM's I/O name-record table.** `tools/capcom_kingpin_rom_records.py` decodes the 199 records
   (123 lamps, 46 switches, 30 coils) the menu reads. The lamp and switch conversions reproduce the
   observed public addresses (the switch column pairing follows `capcom.c`'s `io_r`); the coil byte
   order is taken from the Solenoid Test walk. The record's opto flag marks exactly the nine optos.
3. **Pinned PinMAME** for transport: `cc_sw2m`/`cc_m2sw`, the solenoid words and legacy mirrors, the
   two lamp matrices, and the `capInvSw11` opto mask.
4. **Krellan's page** (krellan.com/pinball/kingpin). Its author checked every lamp position on a real
   machine in operator mode. The page also lists switches, solenoids, the slot-machine drum and
   several hardware notes.

The three retained community table scripts are one lineage, all marked "Table not verified yet", and
are used only as leads.

## Controller contract

- **Driver:** `kpb105`, the only Kingpin driver. The operator menu shows "KING PIN" version β1.5
  (Krellan: two known versions, 1.4 beta and 1.5 beta). `kpv106.zip` in the user's ROM library is
  byte-identical.
- **Switches:** cabinet 1-16, playfield 17-80; the ROM's own switch numbers equal PinMAME's public
  addresses. Unused per the ROM: 11, 12, 40, 56, 64-80. Nine optos (17, 36-39, 44, 48, 52, 61) are
  normalized by PinMAME, so do not invert them again. Their supply is connector J15 on the power
  board. Contact polarity: the ROM's Switch Test draws the nine optos as a beam and every other
  switch as a lever contact closed at public 1. Its C5 Troubleshooting report lists a switch it
  checks when the switch sits at a level other than the one it expects at rest: held at 1 from
  power-up it lists 1-4, 9, 10, 14, 19-24, 32, 33, 34, 41, 42, 49, 50, 53-55, 57-60, 62 and 63,
  and it lists 47 (ramp down) only when it is at 0. In a game the ROM resets a drop bank when all
  its targets (25-28 or 29-31) read 1. With PinMAME's opto mask and `capcom.c`'s complemented read,
  that makes all of those normally open, including the end-of-stroke switches 33/34 and slam
  switch 9, which are normally closed on some other platforms, and the masked optos normally
  closed. The ball holders 35, 43 and 51 are read as a ball present at 1. For ten switches, 13, 15
  and 16 (optional dispenser inputs), 18, 45, 46 and the menu inputs 5-8, normally open is ordinary
  construction. 81-88 are PinMAME's synthetic
  flipper column, 89-96 are empty.
- **Wiring:** the colours and pins the service menu prints come from the ROM's fixed colour tables.
  They are the manufacturer's standard harness code for each position, not a trace of a real
  harness, and this machine barely left prototype.
- **Flipper buttons:** the ROM reads them at 5 (left) and 6 (right). Under PinMAME a host must
  press them through the flipper-column button bits, **84** (left) and **82** (right), because
  `core_updateSw` copies those bits into 5/6 every frame. A direct write to 5 or 6 lasts at most one
  frame. The retained table scripts write 5/6 directly.
- **Solenoids:** 32 driver outputs:
  - 1-11, 13-17 and 32 are 50 V coils;
  - 12 is a 12 V motor;
  - 18-31 are 20 V flashers;
  - 9 and 10 are the CPU-driven flippers.

  PinMAME mirrors 9/10/11/12 at 45/47/33/35 for old DOF configurations. On Kingpin the 33 and 35
  mirrors carry the slot eject and slot motor, not flippers. 51 is the Fast Flips game-on state.
- **Lamps:** two 8x8 matrices, 1-64 (A) and 65-128 (B); 123-125 are NOT USED per the ROM. There is no
  GI channel: every light is a matrix lamp. That includes 35 numbered "G.I." positions (G.I. 1-36
  with no 18; the matrix slot between 17 and 19 is the captive standup) and a backbox G.I. The ROM's
  "(2)" marks an output with two bulbs and "RED" a red bulb. Krellan describes many of them as
  "behind above and red": a red light immediately behind the previous one on its own output. He
  notes that this gives the game "the capability to turn almost the entire GI to a red color".
  129/130 are the CPU and sound board diagnostic LEDs.
- **Operator menu:** making switch 8 (PinMAME's "Coin Door", Krellan's "operator's Advance button")
  enters it. The flipper buttons then step and Start selects. The ROM also warns about a 50 V door
  interlock switch ("Check 50V Interlock SW."); nothing ties that switch to a public address. At
  factory settings a credit costs two coins.

## Mechanisms

- **Trough.** Outhole switch 35 and OUTHOLE coil 1 (Krellan: "ball lift"), a four-opto trough
  (36-39), and TROUGH coil 2 serving the shooter lane. Install four balls. The ROM fires 1 when 35
  closes (again about every 1.2 s while it stays closed, once more about 0.7 s after it opens) and
  fires 2 when a game starts.
- **Auto plunger.** Shooter lane 43 and AUTO PLUNGER coil 32; the cabinet launch button is switch 14.
  Outside a game the ROM launches any ball it finds in the shooter lane.
- **Left ramp entrance lift.** RAMP coil 14 raises the entrance to reveal the Hideout, and switch 47
  reads the lowered position. While 47 is open the ROM drives 14 for about 1.3 s, rests about 1.0 s
  and repeats; it stops once 47 closes. Whether the lift latches or needs a held drive is not
  documented.
- **Hideout gun lock.** A three-ball lock under the ramp (44 opto, 45, 46) with GUN EJECT coil 8.
  Krellan: the playfield area near the left orbit is hinged at the rear, so the eject lifts it and
  the ball shoots down at the player from under the floor. The role of GUN TROUGH OPTO 48 is unknown.
- **Slot machine.** One drum, turned by SLOT MOTOR 12 and indexed by SLOT OPTO 52. It shows nine rows
  of three identical symbols; in spin order: Money, Goods, Sevens, Gangsters, Bars, Power, Guns,
  Crazy Cash, Cherries. The motor often stops between rows and the software rounds to the nearest
  row. How the opto is timed per row is not documented. The saucer (51, SLOT EJECT 11) is flanked by
  standups 49/50.
- **Drop targets.** KING bank 25-28 (reset 6) on the left, PIN bank 29-31 (reset 7) on the right. Both
  resets fire at game start.
- **Top diverter.** TOPGATES 13, behind and left of the top lanes, blocks the left orbit. It has no
  position switch.
- **Other devices:**
  - star bumpers: left 17/57, center 15/58, right 16/59;
  - slingshots: 4/41 and 5/42;
  - captive ball: switch 32;
  - spinners: 17 (right ramp) and 61 (left ramp), both optos.
- **Flippers** are CPU-driven, with end-of-stroke switches 33/34 read by the ROM. Their strength is
  software-adjustable. In the timed "power meter" game style they weaken and stop when the meter runs
  out (Krellan).

## Things a table author will trip over

- **Table defects.** The retained script lineage's captive-ball target pulses 49 instead of 32. It
  binds its right-ramp flasher routine to 23, although the ROM names 22 R. RAMP FLASHER and 23
  BUILDING FLASHER. It also presses the flipper buttons by writing 5/6, which PinMAME overwrites
  every frame (use 84/82).
- **Flasher typing.** PinMAME's flasher typing for Kingpin (18-19, 21-31) came from a VPX table. The
  ROM prints 20 (Big Al) as a flasher too; Krellan puts Big Al on the backglass, and the retained
  table does not bind 20. Krellan reports #67 and #906 flasher bulbs rather than #89.
- **Output 20 in the service test.** During the ROM's Solenoid Test, public 20 pulses continuously
  whichever coil is selected.
- **Flasher 29.** The ROM names it "L.ORBIT (EAST)", although EAST is the right-orbit insert
  (`conflict.flasher-29-orbit-side`).

## What is still needed

- **Spatial placement:** a VPX recreation to measure device positions, cross-checked against
  Krellan's lamp positions and photographs of a real machine.
- **Mechanism behaviour:** whether the ramp and top-diverter coils toggle latches or need a held drive,
  what GUN TROUGH OPTO does, and how the slot drum's opto is timed.
- **Flasher 29:** its actual orbit side.
"""


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	(root / KNOWLEDGE_PATH.relative_to(ROOT)).write_text(KNOWLEDGE_NOTE, encoding="utf-8", newline="\n")
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"Kingpin artifact is missing: {path}")
	expected = canonical_bytes(build())
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Kingpin definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Kingpin seed is not byte-identical to the definition: {seed_path}")
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != KNOWLEDGE_NOTE.encode("utf-8"):
		raise RuntimeError(f"Kingpin knowledge note drifted from its deterministic curator: {knowledge_path}")
	print("Kingpin definition, seed, and knowledge note match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition and pinned seed")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
