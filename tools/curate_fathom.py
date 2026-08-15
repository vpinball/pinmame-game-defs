"""Curate the physical Bally Fathom (1981) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is embedded as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial report.

Evidence priority actually applied here, in the runbook's order:

1. The retained known-working VPX script for runtime semantics and geometry bindings.
2. The Bally game #1233 operations manual and its separate schematics document for physical
   construction, connector assignments and quantities.
3. Pinned PinMAME source for controller topology and the public address space.
4. The retained VPX extraction for coordinates.
5. A LibPinMAME harness run of the production ROM's own solenoid self test, which is what resolves
   the printed Self Test number to public solenoid address mapping and which proves that public
   lamp 47 drives the Solenoid Expander relay rather than a bulb.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/bally/fathom-1981.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/fathom-1981.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/fathom-1981.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/fathom-1981.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/fathom-1981.md"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/fathom-1981.md"

MACHINE_ID = "bally.fathom.1981"
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-by35"
MANUAL_SOURCE = "manual.bally.fathom.1981"
SCHEMATICS_SOURCE = "manual-schematics.bally.fathom.1981"
VPX_TABLE_SOURCE = "vpx-table.fathom-bally-1981"
VPX_SCRIPT_SOURCE = "vpx-script.fathom-bally-1981"
VPX_EXTRACTION_SOURCE = "vpx-extraction.fathom-bally-1981"
HARNESS_SOURCE = "runtime.fathom.solenoid-self-test"
BOARD_SOURCE = "board-mapping.as-2518-23"
IPDB_SOURCE = "ipdb.bally.fathom.1981"

MANUAL_SHA256 = "ce44bcc4470f395ed1498350079bb435e5dbced75daa948471eee33cd93d5e07"
SCHEMATICS_SHA256 = "badb849dcf110846335967024596d2e3853cfef531eae36a6e88d649aedb47a9"
TABLE_SHA256 = "131f29d16bb2d311450c5409981ad0ee7c4664a065f40fd1a4617fd1a09b01a7"
SCRIPT_SHA256 = "b28721214317659c5469ae1612f7316acb293ae4fdc405f6df2791859c2429ac"
HARNESS_SHA256 = "0c5e23417255f4830587db93f767883ae28ac52b27456975758265b4dee84556"
BOOT_HARNESS_SHA256 = "7eda9b26f6b87df76994055fef1ab93751726c38c3f9e515f2bdc7a98c793284"
GEOMETRY_SHA256 = "c02d409b92e5ce34e3dc143bc6abd2351a90ac2bf1b0e62146037593cd91bd7d"

EXTRACTION_RELATIVE_PATH = Path("bally/fathom-1981/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/fathom-1981/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "c6aceb38d454b8236155caa431268ba32ef59212eb3193de983577f307baaac4"
EXTRACTION_FILE_COUNT = 1259
EXTRACTION_TOTAL_BYTES = 87975187

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

DRIVER_IDS = ("fathom", "fathoma", "fathomb")
DRIVER_COMPATIBILITY = {
	"fathom": (
		"identical",
		"Bally production game ROM for the physical 1981 machine, Bally game number 1233. This is the "
		"driver every retained source describes and the one the harness run used.",
	),
	"fathoma": (
		"identical",
		"2004 Bally/Oliver free-play conversion ROM, revision 1. PinMAME reuses init_fathom verbatim "
		"(#define init_fathoma init_fathom), so it declares the identical hardware, display layout, "
		"sound board and lamp-column count. Later firmware for the same physical machine, exactly as "
		"centaura is for Bally Centaur; its 2004 catalogue year is a ROM release date and does not "
		"make it a different game.",
	),
	"fathomb": (
		"identical",
		"2004 Bally/Oliver modified-rules revision 5 ROM. Also shares init_fathom, so it is a rules "
		"revision of the same physical machine rather than a new one.",
	),
}

# --- Printed Switch Assembly Self-Test Display Numbers (manual PDF page 23, printed 17). On this
# platform the printed switch number IS the public address: PinMAME registers BY35 switches as
# sequential matrix positions, address = (column - 1) * 8 + row.
SWITCH_LABELS = {
	1: "Outhole", 2: "#1 Left of Outhole", 3: "#2 Left and #1 Right of Outhole",
	4: "Top Saucer", 5: "Right Saucer", 6: "Credit Button", 7: "Right Flipper Button",
	9: "Coin III (Right)", 10: "Coin I (Left)", 11: "Coin II (Middle)",
	12: '"C" Lane', 13: '"B" Lane', 14: '"A" Lane', 15: "Tilt", 16: "Slam Tilt",
	17: "Right Center Target", 18: "Spinner", 19: "10 Point and 6 Drop Target Rebound",
	20: "3 Left Rollover Buttons", 21: "Right Return Lane", 22: "Right Outlane",
	23: "Left Outlane", 24: "Left Return Lane",
	25: "Top Saucer Rollover Button", 26: "Right Saucer Rollover Button",
	27: "Left Side Drop Target F (Bottom)", 28: "Left Side Drop Target E",
	29: "Left Side Drop Target D", 30: "Left Side Drop Target C",
	31: "Left Side Drop Target B", 32: "Left Side Drop Target A (Top)",
	33: "#3 Middle Drop Target", 34: "#2 Middle Drop Target", 35: "#1 Middle Drop Target",
	36: "Right Slingshot", 37: "Left Slingshot",
	38: "Right Thumper Bumper", 39: "Bottom Thumper Bumper", 40: "Left Thumper Bumper",
	42: "3rd Blue Inline Drop Target", 43: "2nd Blue Inline Drop Target",
	44: "1st Blue Inline Drop Target",
	46: "3rd Green Inline Drop Target", 47: "2nd Green Inline Drop Target",
	48: "1st Green Inline Drop Target",
}
UNUSED_SWITCHES = {8, 41, 45}
CABINET_SWITCHES = {6: "cabinet.start", 7: "flipper.lower.right.button", 9: "cabinet.coin.3",
	10: "cabinet.coin.1", 11: "cabinet.coin.2", 15: "cabinet.tilt", 16: "cabinet.slam-tilt"}
SWITCH_SERIES_CONTACTS = {15: 3, 16: 2}
SWITCH_TYPES = {6: "button", 7: "button", 9: "leaf", 10: "leaf", 11: "leaf", 15: "tilt", 16: "tilt"}

# Normalized from the retained extraction: x/952, y/1974. See review-artifacts/fathom-1981/vpx-geometry.txt.
SWITCH_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.448598, 0.956259)],
	2: [(0.862916, 0.862873)],
	3: [(0.862916, 0.862873)],
	4: [(0.851431, 0.040147)],
	5: [(0.851300, 0.233156)],
	12: [(0.617321, 0.178843)], 13: [(0.509409, 0.169880)], 14: [(0.404175, 0.157521)],
	17: [(0.744859, 0.423130)],
	18: [(0.214635, 0.233539)],
	19: [(0.755709, 0.313871), (0.070477, 0.467662)],
	20: [(0.044643, 0.265001), (0.038340, 0.171789), (0.106618, 0.103850)],
	21: [(0.852782, 0.723877)], 22: [(0.782816, 0.723220)],
	23: [(0.128438, 0.722877)], 24: [(0.059908, 0.720625)],
	25: [(0.702206, 0.039007)], 26: [(0.841912, 0.291343)],
	27: [(0.087875, 0.515137)], 28: [(0.093402, 0.492925)], 29: [(0.098008, 0.469159)],
	30: [(0.103534, 0.445392)], 31: [(0.108140, 0.422069)], 32: [(0.113084, 0.399497)],
	33: [(0.520781, 0.394956)], 34: [(0.468217, 0.380547)], 35: [(0.414269, 0.365648)],
	36: [(0.689207, 0.724223)], 37: [(0.222107, 0.720529)],
	38: [(0.667128, 0.251770)], 39: [(0.514776, 0.323554)], 40: [(0.354023, 0.258026)],
	42: [(0.617606, 0.042733)], 43: [(0.543877, 0.044531)], 44: [(0.469299, 0.045713)],
	46: [(0.841963, 0.331981)], 47: [(0.842331, 0.367716)], 48: [(0.842712, 0.403373)],
}
SWITCH_PROJECTIONS = {
	1: "Projected onto the retained Drain kicker object, the point at which a ball leaves the playfield into the outhole. The outhole switch itself sits inside the outhole under the apron and has no playfield-surface object; the retained script models the whole outhole and trough as one cvpmBallStack (bsTrough.Initsw 0,1,2,3) with no per-switch object.",
	2: "Projected onto the retained BallRelease kicker object, the trough's own eject point. Trough position switches sit inside the ball trough behind the outhole, not on the playfield surface, and the retained script models them only as cvpmBallStack positions.",
	3: "Projected onto the retained BallRelease kicker object; see switch 2. The printed name covers two ball positions on one matrix contact, which is why one address serves the 2nd-left and 1st-right trough stations.",
	18: "Projected onto the retained Spinner object sw18: the spinner switch is part of the spinner assembly rather than a separate playfield sensor.",
	36: "Projected onto the retained RightSlingShot wall, whose _Slingshot handler pulses this address.",
	37: "Projected onto the retained LeftSlingShot wall, whose _Slingshot handler pulses this address.",
	38: "Projected onto the retained Bumper2 object, whose _Hit handler pulses this address.",
	39: "Projected onto the retained Bumper3 object, whose _Hit handler pulses this address.",
	40: "Projected onto the retained Bumper1 object, whose _Hit handler pulses this address.",
}

DIAGNOSTIC_SWITCHES = {
	-7: ("Self Test", "service.self-test", "BY35_SWSELFTEST"),
	-6: ("CPU Diagnostic", "service.diagnostic", "BY35_SWCPUDIAG"),
	-5: ("Sound Diagnostic", "service.diagnostic", "BY35_SWSOUNDDIAG"),
}

SWITCH_ROW_WIRING = {
	1: ("54", "A4J2-8"), 2: ("63", "A4J2-9"), 3: ("57", "A4J2-10"), 4: ("78", "A4J2-11"),
	5: ("60", "A4J2-12"), 6: ("56", "A4J2-13"), 7: ("65", "A4J2-14"), 8: ("52", "A4J2-15"),
}
SWITCH_COLUMN_WIRING = {
	1: ("51", "A4J2-1", "ST 0"), 2: ("70", "A4J2-2", "ST 1"), 3: ("93", "A4J2-3", "ST 2"),
	4: ("53", "A4J2-4", "ST 3"), 5: ("31", "A4J2-5", "ST 4"), 6: ("72", "A4J4-8", "ST 5"),
}

# --- Momentary solenoids. printed_numbers is the printed Self Test # column; the mapping to public
# address comes from the ROM's own solenoid self test, captured by the retained harness run, which
# pulses the coils in printed order 01..21.
SOLENOIDS = {
	1: dict(
		label="3 Top Drop Target Reset / 1st Green Inline Drop Target",
		printed=("09", "14"), pin="A3J2-9", transistor="Q2", selector=0,
		relay_gated=True, kind="coil",
	),
	2: dict(
		label="6 Drop Target Reset / 2nd Green Inline Drop Target",
		printed=("10", "15"), pin="A3J2-4", transistor="Q1", selector=1,
		relay_gated=True, kind="coil",
	),
	3: dict(
		label="3 Middle Drop Target Reset / 3rd Green Inline Drop Target",
		printed=("11", "16"), pin="A3J2-10", transistor="Q5", selector=2,
		relay_gated=True, kind="coil",
	),
	4: dict(label="Right Inline Drop Target Reset", printed=("12",), pin="A3J2-11",
		transistor="Q6", selector=3, wire="91", kind="coil"),
	5: dict(label="Unused Momentary Solenoid 5", printed=(), pin=None, transistor="Q7",
		selector=4, kind="coil", unused=True),
	6: dict(label="Knocker", printed=("01",), pin="A3J2-5", transistor="Q3", selector=5,
		kind="coil", cabinet=True),
	7: dict(label="Outhole Kicker", printed=("13",), pin="A3J1-5", transistor="Q4", selector=6,
		wire="95", kind="coil"),
	8: dict(label="Left Thumper Bumper", printed=("04",), pin="A3J5-10", transistor="Q8",
		selector=7, wire="85", kind="coil"),
	9: dict(label="Bottom Thumper Bumper", printed=("05",), pin="A3J5-12", transistor="Q13",
		selector=8, wire="80", kind="coil"),
	10: dict(label="Right Thumper Bumper", printed=("06",), pin="A3J5-11", transistor="Q14",
		selector=9, wire="78", kind="coil"),
	11: dict(label="Left Slingshot", printed=("07",), pin="A3J5-9", transistor="Q9", selector=10,
		wire="71", kind="coil"),
	12: dict(label="Right Slingshot", printed=("08",), pin="A3J5-15", transistor="Q10",
		selector=11, wire="74", kind="coil"),
	13: dict(label="Top Saucer Kicker / 1st Blue Inline Drop Target", printed=("02", "17"),
		pin="A3J5-13", transistor="Q12", selector=12, wire="67", relay_gated=True, kind="coil"),
	14: dict(label="Right Saucer Kicker / 2nd Blue Inline Drop Target", printed=("03", "18"),
		pin="A3J5-14", transistor="Q11", selector=13, wire="83", relay_gated=True, kind="coil"),
	15: dict(label="3rd Blue Inline Drop Target", printed=("19",), pin="A3J5-8",
		transistor="Q16", selector=14, wire="18", kind="coil"),
	17: dict(label="Unused Continuous Output (CONT 2)", printed=(), pin=None, transistor="Q17",
		continuous="PB4", kind="coil", unused=True),
	18: dict(label="Coin Lockout Door", printed=("20",), pin="A3J3-8", transistor="Q19",
		continuous="PB5", kind="coil", cabinet=True),
	19: dict(label="K1 Relay (Flipper Enable)", printed=("21",), pin="A3J3-5", transistor="Q15",
		continuous="PB6", kind="relay", cabinet=True),
	20: dict(label="Sixth Switch-Column Strobe (ST 5)", printed=(), pin="A4J4-8", transistor="Q18",
		continuous="PB7", kind="control_signal", strobe=True),
}
SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	4: [(0.842712, 0.403373)],
	7: [(0.448598, 0.956259)],
	8: [(0.354023, 0.258026)],
	9: [(0.514776, 0.323554)],
	10: [(0.667128, 0.251770)],
	11: [(0.222107, 0.720529)],
	12: [(0.689207, 0.724223)],
	13: [(0.851431, 0.040147)],
	14: [(0.851300, 0.233156)],
	15: [(0.617606, 0.042733)],
	1: [(0.469299, 0.045713)],
	2: [(0.113084, 0.399497)],
	3: [(0.520781, 0.394956)],
}
SOLENOID_PROJECTIONS = {
	1: "Projected onto the 1st Blue Inline Drop Target (retained object sw44), the target this address raises when the Solenoid Expander relay is de-energized, since the reset coil sits under the bank rather than on the playfield surface.",
	2: "Projected onto the top target of the left six-bank (retained object sw32); the bank reset coil sits under the bank.",
	3: "Projected onto the #3 Middle Drop Target (retained object sw33); the bank reset coil sits under the bank.",
	4: "Projected onto the 1st Green Inline Drop Target (retained object sw48); the bank reset coil sits under the bank.",
	7: "Projected onto the retained Drain kicker object, the outhole mouth. The outhole kicker sits inside the outhole under the apron.",
	8: "Projected onto the retained Bumper1 object; the coil is inside the bumper body.",
	9: "Projected onto the retained Bumper3 object; the coil is inside the bumper body.",
	10: "Projected onto the retained Bumper2 object; the coil is inside the bumper body.",
	11: "Projected onto the retained LeftSlingShot wall; the coil is behind the slingshot rubber.",
	12: "Projected onto the retained RightSlingShot wall; the coil is behind the slingshot rubber.",
	13: "Projected onto the retained sw4 kicker (Top Saucer). With the Solenoid Expander relay energized the same driver output drops the 1st Blue Inline Drop Target instead.",
	14: "Projected onto the retained sw5 kicker (Right Saucer). With the Solenoid Expander relay energized the same driver output drops the 2nd Blue Inline Drop Target instead.",
	15: "Projected onto the 3rd Blue Inline Drop Target (retained object sw42), the target this coil drops.",
}
FLIPPER_OUTPUTS = {
	46: ("Lower Right and Upper Right Flipper Coils", "flipper.lower.right", [(0.625269, 0.845430), (0.857995, 0.526207)]),
	48: ("Lower Left Flipper Coil", "flipper.lower.left", [(0.284084, 0.843743)]),
}

# --- Lamp matrix. public = 16 * data_line + decoder_output + 1 on the AS-2518-23, so U1 owns 1-15,
# U2 17-31, U3 33-47 and U4 49-63. The public-address to A5 connector-pin mapping is a property of
# the AS-2518-23 board itself and is identical on Bally Centaur and Bally Kiss; Fathom's own A5 sheet
# reproduces it for U1's first twelve outputs by straight-line trace and independently confirms it by
# arrow count, and the printed pin functions below are Fathom's own.
LAMPS = {
	1: ("50K Right Return Lane", "A5J1-18", "58"),
	2: ("1K Blue Bonus", "A5J1-19", "60"),
	3: ("5K Blue Bonus", "A5J1-17", "57"),
	4: ("9K Blue Bonus", "A5J1-23", "12"),
	5: ("3X Blue Bonus", "A5J1-14", "54"),
	6: ("1K Green Bonus", "A5J1-15", "13"),
	7: ("5K Green Bonus", "A5J1-16", "90"),
	8: ("9K Green Bonus", "A5J1-28", "78"),
	9: ("3X Green Bonus", "A5J1-24", "50"),
	10: ('"C" Lane', "A5J1-25", "75"),
	11: ("Shoot Again", "A5J2-21", None),
	12: ("Right Thumper Bumper", "A5J1-27", "53"),
	13: ("Ball In Play", "A5J2-22", None),
	14: ("Double Playfield Scores", "A5J2-16", "34"),
	15: ("Top Saucer Lane Arrow", "A5J2-14", "12"),
	17: ("Right Out Special", "A5J1-1", "41"),
	18: ("2K Blue Bonus", "A5J1-9", "43"),
	19: ("6K Blue Bonus", "A5J1-8", "51"),
	20: ("10K Blue Bonus", "A5J1-3", "45"),
	21: ("4X Blue Bonus", "A5J1-2", "52"),
	22: ("2K Green Bonus", "A5J1-10", "23"),
	23: ("6K Green Bonus", "A5J1-7", "34"),
	24: ("10K Green Bonus", "A5J1-6", "25"),
	25: ("4X Green Bonus", "A5J1-5", "48"),
	26: ('"B" Lane', "A5J1-11", "65"),
	27: ("Match", "A5J2-8", None),
	28: ("Bottom Thumper Bumper", "A5J1-12", "61"),
	29: ("High Score To Date", "A5J2-23", None),
	30: ("Triple Playfield Scores", "A5J2-20", "98"),
	31: ("Right Saucer Arrow", "A5J2-15", "23"),
	33: ("Left Out Special", "A5J3-26", "43"),
	34: ("3K Blue Bonus", "A5J3-25", "36"),
	35: ("7K Blue Bonus", "A5J3-19", "67"),
	36: ("Advance Green Bonus", "A5J3-17", "13"),
	37: ("5X Blue Bonus", "A5J3-16", "25"),
	38: ("3K Green Bonus", "A5J3-23", "98"),
	39: ("7K Green Bonus", "A5J3-27", "40"),
	40: ("Release Lagoon Captive Ball", "A5J1-13", "96"),
	41: ("5X Green Bonus", "A5J3-21", "30"),
	42: ('"A" Lane', "A5J3-20", "64"),
	43: ("Same Player Shoot Again", "A5J3-22", "23"),
	44: ("Left Thumper Bumper", "A5J3-24", "72"),
	45: ("Game Over", "A5J2-11", None),
	46: ("In Sequence", "A5J2-6", "10"),
	47: ("Solenoid Expander Relay Drive", "A5J2-2", "20"),
	49: ("50K Left Return Lane", "A5J3-1", "10"),
	50: ("4K Blue Bonus", "A5J3-12", "21"),
	51: ("8K Blue Bonus", "A5J3-15", "53"),
	52: ("Advance Blue Bonus", "A5J3-11", "20"),
	53: ("55K Blue Bonus", "A5J3-9", "15"),
	54: ("4K Green Bonus", "A5J3-3", "81"),
	55: ("8K Green Bonus", "A5J3-4", "14"),
	56: ("Release Cave Captive Ball", "A5J3-2", "95"),
	57: ("55K Green Bonus", "A5J3-10", "91"),
	58: ("A-B-C Special", "A5J3-18", "86"),
	59: ("Credit Indicator", "A5J3-13", "35"),
	60: ("Spinner", "A5J3-14", "84"),
	61: ("Tilt", "A5J2-10", None),
	62: ("Extra Ball", "A5J2-7", "91"),
	63: ("Bonus Special", "A5J2-1", "60"),
}
# Eight AS-2518-23 outputs branch to a second connector pin. On this machine every one of those
# second pins is printed N/U, which is exactly the eight N/U pins that carry an arrow on Fathom's own
# A5 sheet.
LAMP_BRANCH_PINS = {
	11: "A5J1-26", 12: "A5J2-13", 27: "A5J1-4", 28: "A5J2-12",
	43: "A5J2-9", 44: "A5J2-4", 59: "A5J2-5", 60: "A5J2-3",
}
LAMP_QUANTITY = {36: 2, 52: 2}
BACKBOX_LAMPS = {11, 13, 27, 29, 45, 61}
LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.844745, 0.667392)],
	2: [(0.410713, 0.818329)], 3: [(0.412028, 0.687375)], 4: [(0.294380, 0.602649)],
	5: [(0.344039, 0.799975)], 6: [(0.498424, 0.819213)], 7: [(0.500525, 0.687374)],
	8: [(0.617388, 0.603915)], 9: [(0.561536, 0.801571)], 10: [(0.616283, 0.131409)],
	12: [(0.667128, 0.251770)],
	14: [(0.401074, 0.546938)], 15: [(0.121265, 0.308889)],
	17: [(0.782042, 0.665523)], 18: [(0.410977, 0.785401)], 19: [(0.410977, 0.654194)],
	20: [(0.251578, 0.629245)], 21: [(0.328735, 0.767300)], 22: [(0.499478, 0.786539)],
	23: [(0.500263, 0.654825)], 24: [(0.663605, 0.629751)], 25: [(0.576946, 0.770203)],
	26: [(0.508772, 0.121075)],
	28: [(0.514776, 0.323554)],
	30: [(0.509267, 0.546671)], 31: [(0.812341, 0.469462)],
	33: [(0.130656, 0.663768)], 34: [(0.408431, 0.750610)], 35: [(0.410714, 0.621392)],
	36: [(0.697342, 0.491812), (0.461743, 0.442074)],
	37: [(0.318016, 0.740556)], 38: [(0.499736, 0.752344)], 39: [(0.499212, 0.622530)],
	40: [(0.241189, 0.424850)], 41: [(0.596809, 0.741611)], 42: [(0.405095, 0.109397)],
	44: [(0.354023, 0.258026)],
	46: [(0.387806, 0.447580)],
	49: [(0.067536, 0.665334)], 50: [(0.412027, 0.720176)], 51: [(0.360033, 0.600242)],
	52: [(0.358249, 0.413041), (0.461743, 0.442074)],
	53: [(0.330227, 0.641198)], 54: [(0.503072, 0.721510)], 55: [(0.549898, 0.601002)],
	56: [(0.224659, 0.511382)], 57: [(0.576553, 0.641325)], 58: [(0.509953, 0.233521)],
	59: [(0.194812, 0.897478)], 60: [(0.225604, 0.261788)],
	62: [(0.690078, 0.458778)], 63: [(0.453954, 0.579925)],
}
LAMP_PROJECTIONS = {
	12: "Projected onto the retained Bumper2 object, the right thumper bumper the manual names for this circuit. The retained table binds its own address-12 light objects to the bottom bumper instead; see conflict.thumper-bumper-lamp-address-swap.",
	28: "Projected onto the retained Bumper3 object, the bottom thumper bumper the manual names for this circuit. The retained table binds its own address-28 light objects to the right bumper instead; see conflict.thumper-bumper-lamp-address-swap.",
	44: "Projected onto the retained Bumper1 object, the left thumper bumper. The retained table agrees on this one address.",
}
# Auxiliary AS-2518-52 outputs. public = 64 + 16 * data_line + decoder_output + 1; only decoder
# outputs 0-6 are fitted and output 7 is printed N/U on all four chips.
AUX_LAMPS = {
	65: ("#1 Scan Rollover Button", "A9J2-7", [(0.043855, 0.264818)]),
	66: ("#5 Back Scan and 1st Left Lane Scan", "A9J2-8", None),
	81: ("#2 Scan Rollover Button", "A9J2-14", [(0.038603, 0.171606)]),
	82: ("#6 Back Scan and 2nd Left Lane Scan", "A9J2-11", None),
	97: ("#3 Scan Rollover Button", "A9J3-8", [(0.106355, 0.103090)]),
	98: ("#7 Back Scan and 3rd Left Lane Scan", "A9J3-3", None),
	113: ("#4 Back Scan", "A9J3-15", [(0.701943, 0.039197)]),
}
AUX_DRIVEN_UNNAMED = {67, 83, 99, 114, 115}
AUX_UNLABELLED = [68, 69, 70, 71, 84, 85, 86, 87, 100, 101, 102, 103, 116, 117, 118, 119]
AUX_DECODER_N_U = [72, 88, 104, 120]
AUX_SCR = {
	65: "Q1", 66: "Q2", 67: "Q3", 68: "Q4", 69: "Q5", 70: "Q6", 71: "Q7", 72: None,
	81: "Q8", 82: "Q9", 83: "Q10", 84: "Q11", 85: "Q12", 86: "Q13", 87: "Q14", 88: None,
	97: "Q15", 98: "Q16", 99: "Q17", 100: "Q18", 101: "Q19", 102: "Q20", 103: "Q21", 104: None,
	113: "Q22", 114: "Q23", 115: "Q24", 116: "Q25", 117: "Q26", 118: "Q27", 119: "Q28", 120: None,
}

DIPS = {
	1: "Coin chute #1 (hinge side) credits-per-coin selector bit 1",
	2: "Coin chute #1 (hinge side) credits-per-coin selector bit 2",
	3: "Coin chute #1 (hinge side) credits-per-coin selector bit 3",
	4: "Coin chute #1 (hinge side) credits-per-coin selector bit 4",
	5: "Coin chute #1 (hinge side) credits-per-coin selector bit 5",
	6: "End of game balls in saucer",
	7: "Collect bonus special",
	8: "Extra ball lite flashing time",
	9: "Coin chute #3 (right side) credits-per-coin selector bit 1",
	10: "Coin chute #3 (right side) credits-per-coin selector bit 2",
	11: "Coin chute #3 (right side) credits-per-coin selector bit 3",
	12: "Coin chute #3 (right side) credits-per-coin selector bit 4",
	13: "Coin chute #3 (right side) credits-per-coin selector bit 5",
	14: "Undocumented option switch S14",
	15: "Undocumented option switch S15",
	16: "A-B-C special lite",
	17: "Coin chute #2 (center) credits-per-coin selector bit 1",
	18: "Coin chute #2 (center) credits-per-coin selector bit 2",
	19: "Coin chute #2 (center) credits-per-coin selector bit 3",
	20: "Coin chute #2 (center) credits-per-coin selector bit 4",
	21: "Undocumented option switch S21",
	22: "Blue and green inline drop target carry-over",
	23: "1 to 10 bonus lite recall",
	24: "A-B-C lane lite recall",
	25: "Maximum credits selector bit 1",
	26: "Maximum credits selector bit 2",
	27: "Credit display",
	28: "Match feature",
	29: "Number of replays per game",
	30: "Game over attract voice",
	31: "Balls per game selector bit 1",
	32: "Balls per game selector bit 2",
}
DIP_NOTES = {
	6: 'ON is liberal: "any ball in saucer will not kick out at end of game". OFF is conservative: it will kick out.',
	7: 'ON is liberal: reaching both 55 bonus lites and completing blue OR green bonus lites scores 1 replay. OFF requires blue AND green.',
	8: "ON is liberal: the extra-ball lite flashes for 10 seconds. OFF: 6 seconds.",
	16: "ON is liberal: the lite alternates so more than one replay can be collected. OFF: one replay per ball.",
	22: "ON is liberal: any blue or green inline drop target left down will drop down again for the next ball. OFF: it will not.",
	23: "ON is liberal: any lit 1-10 bonus lite carries to the next ball. OFF: it does not.",
	24: "ON is liberal: any lit A-B-C lane lite carries to the next ball. OFF: it does not.",
	27: "ON displays credits, OFF does not.",
	28: "ON enables the match feature, OFF disables it.",
	29: "ON is liberal: all replays earned are collected. OFF: one replay per player per game.",
	30: 'ON is liberal: the voice says "Help! Surface, Surface, Fathom" or "Danger, Sea Nymph Await Fathom" during game over. OFF: no voice.',
}
DIP_GROUP_NOTES = {
	(1, 5): "One of the five option switches that select the credits awarded per coin on this chute. The manual gives thirty-one settings as a combination table rather than a per-switch meaning, so no independent function is asserted for the individual switch.",
	(9, 13): "One of the five option switches that select the credits awarded per coin on this chute; same combination table as S1-S5.",
	(17, 20): "One of the four option switches that select the credits awarded per coin on the centre chute. All four OFF means \"Same as Coin Chute #1 Settings\"; the remaining fifteen combinations give 1/1 through 15/1 coin.",
	(25, 26): "With its partner selects a maximum credit limit of 10, 15, 25 or 40. The manual prints S26 as the more significant column.",
	(31, 32): "With its partner selects 2, 3, 4 or 5 balls per game. The manual prints S32 as the more significant column.",
}
UNDOCUMENTED_DIPS = {14, 15, 21}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Fathom retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Fathom extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Fathom retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Fathom retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Fathom retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": provenance(*source_refs),
			}
		)
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def switch_wiring(address: int) -> dict[str, Any]:
	column = (address - 1) // 8 + 1
	row = (address - 1) % 8 + 1
	drive_wire, drive_connection, strobe = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "Bally MPU AS-2518-35",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"strobe {strobe}, return I {row - 1}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role, symbol) in DIAGNOSTIC_SWITCHES.items():
		items.append(
			_device(
				f"switch.{slug(label)}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				normally_closed=False,
				roles=[role],
				physical={
					"location": "back box" if address == -6 else "door",
					"switch_type": "button",
					"notes": (
						f"Direct diagnostic contact in switch column 0 ({symbol}), not a matrix position, so it has "
						"no strobe or return wire in the playfield harness. The manual's routine-maintenance section "
						"describes the Self-Test button as being inside the door and stepping the game through the "
						"lamp, display, solenoid, sound and stuck-switch tests in that order."
					),
				},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for address in range(1, 49):
		label = SWITCH_LABELS.get(address)
		unused = address in UNUSED_SWITCHES
		identifier = f"switch.matrix-{address}"
		column = (address - 1) // 8 + 1
		row = (address - 1) % 8 + 1
		physical: dict[str, Any] = {"switch_type": SWITCH_TYPES.get(address, "leaf")}
		notes = (
			f"Printed Switch Assembly Self-Test Display Number {address:02d}. Switch-matrix strobe column "
			f"{column} ({SWITCH_COLUMN_WIRING[column][2]}), return row {row} (I {row - 1}). On this platform the "
			"printed switch number is the public address: PinMAME registers Bally MPU switches as sequential "
			"matrix positions, address = (column - 1) * 8 + row."
		)
		if unused:
			notes += (
				" The printed table leaves this position entirely blank - no description and no entry - and the "
				"playfield wiring diagram draws no contact at the corresponding grid crossing, so nothing is fitted."
			)
		if address in SWITCH_SERIES_CONTACTS:
			notes += (
				f" The printed table writes this entry with a parenthesised ({SWITCH_SERIES_CONTACTS[address]}), "
				f"which is the number of series contacts wired onto this one matrix position, not a second address."
			)
		if address == 20:
			notes += (
				" One matrix position serves three separate rollover buttons wired in parallel, which is what the "
				"printed name \"3 LEFT ROLLOVER BUTTONS\" records; the retained script drives the same public "
				"address from three distinct trigger objects (sw20a, sw20b, sw20c)."
			)
		if address == 19:
			notes += (
				" One matrix position serves two separate scoring rubbers, the 10-point rubber and the six-bank "
				"rebound rubber; the retained script pulses this address from two objects (sw19, sw19a)."
			)
		if address == 3:
			notes += (
				" The printed name covers two ball stations on one contact. With switches 1 and 2 this is the "
				"three-position outhole and ball trough: the retained script initialises one cvpmBallStack with "
				"exactly these three addresses (bsTrough.Initsw 0,1,2,3)."
			)
		if address == 7:
			notes += (
				" Only the right flipper button appears in the switch matrix. The left flipper button is wired "
				"directly into the flipper-enable relay circuit on the A3 sheet and has no matrix address, so the "
				"ROM cannot read it; the right button is read so it can act as a modifier during the self tests. "
				"Pinned PinMAME's own by35 SWITCH_UPDATE independently confirms the address, writing the standard "
				"keyboard start and right-flipper bits into matrix column 1 bits 5 and 6, that is public 6 and 7."
			)
		if address in {9, 10, 11}:
			notes += (
				" Pinned PinMAME's by35 SWITCH_UPDATE writes the three standard coin-chute keyboard bits into "
				"matrix column 2 bits 0, 1 and 2, that is public 9, 10 and 11, matching the printed table exactly."
			)
		if address == 16:
			notes += " PinMAME writes the standard slam-tilt keyboard bit into matrix column 2 bit 7, that is public 16."
		physical["notes"] = notes

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.self-test", "value": f"{address:02d}"},
			],
			"physical": physical,
			"wiring": switch_wiring(address),
		}
		if unused:
			availability = "unused"
			label = f"Not Used Matrix Position {address}"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, SCHEMATICS_SOURCE)
			refs = (MANUAL_SOURCE, SCHEMATICS_SOURCE, CONTROLLER_SOURCE)
		else:
			availability = "used"
			extra["normally_closed"] = False
			refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
			if address in CABINET_SWITCHES:
				extra["roles"] = [CABINET_SWITCHES[address]]
				physical["location"] = "coin door" if address in {6, 9, 10, 11} else "cabinet"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
				if address in SWITCH_PROJECTIONS:
					physical["notes"] += " " + SWITCH_PROJECTIONS[address]
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	for address, label in DIPS.items():
		notes = "MPU option switch S%d, one of the thirty-two switches in the four eight-position banks S1-8, S9-16, S17-24 and S25-32 on the A4 MPU module in the back box. The manual states the ON toggle position is marked on the assembly and that power must be off before adjustment." % address
		if address in DIP_NOTES:
			notes += " " + DIP_NOTES[address]
		for (low, high), text in DIP_GROUP_NOTES.items():
			if low <= address <= high:
				notes += " " + text
		if address in UNDOCUMENTED_DIPS:
			notes += (
				" This manual's Game Adjustments and Game Feature Options sections do not document this switch, and "
				"no retained source names it, so no function is asserted."
			)
		items.append(
			_device(
				f"switch.dip-{address}",
				label,
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used" if address not in UNDOCUMENTED_DIPS else "unknown",
				(MANUAL_SOURCE, CONTROLLER_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"S{address}"},
				],
				physical={"location": "A4 MPU module", "switch_type": "dip", "notes": notes},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, spec in sorted(SOLENOIDS.items()):
		label = spec["label"]
		identifier = f"device.{slug(label)}"
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		for printed in spec["printed"]:
			aliases.append({"namespace": "manual.self-test", "value": printed})
		physical: dict[str, Any] = {}
		wiring: dict[str, Any] = {"board": "Bally Solenoid Driver AS-2518-22", "driver_transistor": spec["transistor"]}
		if spec.get("pin"):
			wiring["control_connection"] = spec["pin"]
		if spec.get("wire"):
			wiring["drive_wire"] = spec["wire"]
		if "selector" in spec:
			notes = (
				f"Momentary solenoid: the CPU writes selector value {spec['selector']} to PIA1:B bits 0-3 and "
				f"by35.c sets bit {spec['selector']} of the solenoid word, so the public address is selector + 1. "
				f"Decoded by U2 (74L154) output {spec['selector']} and driven by {spec['transistor']} (SE9302)."
			)
		else:
			notes = (
				f"Continuous output on PIA1:B {spec['continuous']}, inverted in hardware, published at "
				f"{address} (bits 4-7 map to 17-20). Driven by {spec['transistor']} (SE9302)."
			)
		if spec["printed"]:
			printed_text = " and ".join(spec["printed"])
			notes += (
				f" Printed Solenoid Identification Table entry {printed_text}. The printed Self Test number is a "
				"test order, not an address; the mapping to this public address was read off the ROM's own solenoid "
				"self test in the retained harness run, which pulses the coils in printed order 01 through 21."
			)
		if spec.get("relay_gated"):
			notes += (
				" One driver output, two coils. The printed A3 connector label names both alternatives on this pin, "
				"and the playfield sheet draws the two coils with a ganged relay contact between them: the Solenoid "
				"Expander (A15, AS-2518-66, a MOC3011 optocoupler driving a 48 V relay K1) selects which coil the "
				"output reaches. The harness run pulses this address twice per self-test cycle, once for each printed "
                                "entry, which is what proves the sharing."
			)
		if spec.get("strobe"):
			notes += (
				" This address is not a coil. The playfield wiring diagram takes the sixth switch-column strobe ST 5 "
				"from MPU connector A4J4-8, which is the same PIA1:B PB7 line this continuous output publishes, and "
				"the A3 sheet's own Q18 output reaches nothing but pins printed N/U. by35.c's default switch-column "
				"path reads (locals.b1 & 0x80) >> 2 for the sixth column, and PinMAME's LISY bridge, which drives "
                                "real Bally hardware, special-cases Fathom at src/lisy/lisy35.c case 3, sets "
				"lisy35_J4PIN8_is_strobe and masks this bit out of the coil data with cont_data &= 0x07. The retained "
				"harness run shows the address asserted continuously from the moment the game comes up."
			)
		if spec.get("unused") and address == 5:
			notes += (
				" This momentary output is genuinely spare. The printed Solenoid Identification Table lists nineteen "
				"momentary functions across fourteen driver outputs, and the ROM's own solenoid self test in the "
				"retained harness run pulses fourteen momentary addresses - 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, "
				"14, 15 - and never this one."
			)
		if spec.get("unused") and address == 17:
			notes += (
				" Genuinely spare. The A3 sheet routes this continuous driver's output only to pins printed N/U "
				"(A3J5-7 and A3J2C-15), and the self-test run never pulses it. It asserts once during the power-on "
				"pulse that briefly drives all four continuous outputs."
			)
		physical["notes"] = notes
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		availability = "unused" if spec.get("unused") else "used"
		if spec.get("unused"):
			extra["spatial"] = not_applicable("unused", SCHEMATICS_SOURCE, HARNESS_SOURCE)
		elif spec.get("strobe"):
			extra["roles"] = ["internal.switch-strobe"]
			extra["spatial"] = not_applicable("internal_nonvisual", SCHEMATICS_SOURCE, CORE_SOURCE)
		elif spec.get("cabinet"):
			roles = {6: "cabinet.knocker", 18: "cabinet.coin-lockout", 19: "internal.flipper-enable"}
			extra["roles"] = [roles[address]]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATICS_SOURCE)
		else:
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			physical["notes"] += " " + SOLENOID_PROJECTIONS[address]
		refs = (MANUAL_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, spec["kind"], "pinmame.output.solenoid", address, availability, refs, **extra))

	for address, (label, role, positions) in FLIPPER_OUTPUTS.items():
		identifier = f"device.{slug(label)}"
		items.append(
			_device(
				identifier,
				label,
				"coil",
				"pinmame.output.solenoid",
				address,
				"used",
				(CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=[role],
				physical={
					"notes": (
						"Fathom's flipper coils have no driver-board output of their own: the A3 sheet wires them "
						"directly to the 43 VDC bus behind the K1 flipper-enable relay contacts, with the cabinet "
						"buttons in series (A3J2C-1 and A3J2C-2) and the coils on A3J1-8 and A3J1-9. "
						"fathomGameData declares FLIP_SW(FLIP_L) and no FLIP_SOL bit, so PinMAME publishes these two "
						"synthetic lower-flipper addresses purely for ball physics; the retained known-working script "
						"binds them through core.vbs sLRFlipper and sLLFlipper. The upper right flipper is wired in "
						"parallel with the lower right flipper and has no address of its own, which the retained "
						"script reproduces by rotating both RightFlipper and RightFlipper1 from the same callback."
					)
				},
				spatial=located(identifier, "effect", positions, VPX_TABLE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in list(range(1, 16)) + list(range(17, 32)) + list(range(33, 48)) + list(range(49, 64)):
		label, pin, wire = LAMPS[address]
		identifier = f"lamp.{slug(label)}-{address}"
		data_line, decoder_output = divmod(address - 1, 16)
		decoder = f"U{data_line + 1}"
		notes = (
			f"Lamp driver AS-2518-23 output: lamp data line PD{data_line} enables decoder {decoder} (MC14514CP) and "
			f"latched address {decoder_output} selects its output {decoder_output}, so the public address is "
			f"16 * {data_line} + {decoder_output} + 1. Printed function at connector pin {pin}."
		)
		if wire:
			notes += f" Playfield wiring diagram wire {wire}."
		if address in LAMP_BRANCH_PINS:
			notes += (
				f" This board output also reaches {LAMP_BRANCH_PINS[address]}, which Fathom's own A5 sheet prints "
				"N/U: the harness does not use that branch on this machine. Exactly eight AS-2518-23 outputs branch "
				"to a second pin, and all eight of the N/U pins that carry an arrow on Fathom's sheet are those eight."
			)
		if address in LAMP_QUANTITY:
			notes += f" The printed function carries a bulb quantity of ({LAMP_QUANTITY[address]})."
		if address in BACKBOX_LAMPS:
			notes += (
				" Back box status lamp: pin A5J2 is the connector the sheet marks TO BACK BOX, and this address is "
				"one of the fixed Bally MPU status-lamp positions that Bally Centaur and Bally Kiss also carry at the "
				"same public addresses (11 Shoot Again, 13 Ball In Play, 27 Match, 29 High Score To Date, 45 Game "
				"Over, 61 Tilt). The retained known-working script names the same six addresses in its own "
				"commented-out backglass lines."
			)
		if address == 11:
			notes += (
				" The retained table drives an apron-position light object at this address instead. The printed "
				"wiring is unambiguous - A5J2-21 SHOOT AGAIN in the back box, with the playfield branch A5J1-26 "
				"printed N/U - and the separate playfield Same Player Shoot Again insert is address 43, so the "
				"manual is followed here."
			)
		if address == 47:
			notes += (
				" This address is not a lamp. A5J2-2 is printed TO AUX. EXPANDOR J1-2, and the Solenoid Expander "
				"A15's own J1-2 is printed SCR ANODE LAMP DRIVER, so this lamp-driver output is the control input of "
				"the 48 V relay that selects which of two coils five solenoid outputs reach. The retained harness "
				"run proves it directly: during the ROM's solenoid self test this address is energized immediately "
				"before and during each of the six in-line drop-target pulses (printed entries 14 through 19) and is "
				"off for every reset and saucer pulse."
			)
		if address in {12, 28, 44}:
			notes += (
				" Thumper bumper lamp; the bulb sits inside the bumper body, so it is placed on the bumper assembly "
				"itself rather than on a separate insert."
			)
		physical: dict[str, Any] = {"notes": notes}
		if address in LAMP_QUANTITY:
			physical["quantity"] = LAMP_QUANTITY[address]
		wiring: dict[str, Any] = {"board": "Bally Lamp Driver AS-2518-23", "control_connection": pin}
		if wire:
			wiring["drive_wire"] = wire
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
			"physical": physical,
			"wiring": wiring,
		}
		kind = "relay" if address == 47 else "lamp"
		if address == 47:
			extra["roles"] = ["internal.solenoid-expander-gate"]
			extra["spatial"] = not_applicable("internal_nonvisual", SCHEMATICS_SOURCE, HARNESS_SOURCE)
		elif address in BACKBOX_LAMPS:
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATICS_SOURCE)
		elif address == 43:
			physical["notes"] += (
				" No light object in the retained extraction is bound to this address, and the retained script never "
				"references it, so no coordinate is asserted; the spatial key is omitted rather than invented."
			)
		else:
			extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			if address in LAMP_PROJECTIONS:
				physical["notes"] += " " + LAMP_PROJECTIONS[address]
		refs = (SCHEMATICS_SOURCE, MANUAL_SOURCE, BOARD_SOURCE, CORE_SOURCE)
		if address == 47:
			refs = (SCHEMATICS_SOURCE, BOARD_SOURCE, HARNESS_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.lamp", address, "used", refs, **extra))

	for address in sorted(list(AUX_LAMPS) + list(AUX_DRIVEN_UNNAMED) + AUX_UNLABELLED + AUX_DECODER_N_U):
		data_line, decoder_output = divmod(address - 65, 16)
		decoder = f"U{data_line + 2}"
		scr = AUX_SCR[address]
		known = AUX_LAMPS.get(address)
		label = known[0] if known else f"Auxiliary Lamp Driver Position {address}"
		identifier = f"lamp.aux-{address}"
		notes = (
			f"Auxiliary lamp driver AS-2518-52 output: lamp data line PD{data_line} enables decoder {decoder} "
			f"(MC14028B) through its D input and the three latched address bits from U1 (MC14175B) select output "
			f"{decoder_output}, so the public address is 64 + 16 * {data_line} + {decoder_output} + 1. This board is "
			"not the AS-2518-43 that Bally Centaur and Bally Kiss carry: it has four decoders and twenty-eight SCRs "
			"where the -43 has two and twelve, so no derivation transfers from those machines."
		)
		if scr:
			notes += f" SCR {scr}."
		if known:
			notes += f" Printed function at connector pin {known[1]}; this is one of only seven of the twenty-eight SCR outputs that this sheet annotates with a function."
			availability = "used"
		elif address in AUX_DRIVEN_UNNAMED:
			notes += (
				" The SCR is fitted but the sheet leaves its connector destination without a function label, and no "
				"other retained source names it. The retained harness run shows the ROM does drive this address, so "
				"it is enumerated as used with its function unresolved."
			)
			availability = "used"
		elif address in AUX_DECODER_N_U:
			notes += (
				" Decoder output 7 is printed N/U on all four chips, so this address decodes to no fitted SCR. Note "
				"that U1's fourth flip-flop is not driven from J1 at all - it sits on R5 to ground - so only three "
				"latched address bits reach this board and the higher auxiliary addresses PinMAME can publish cannot "
				"produce a distinct physical output here."
			)
			availability = "unused"
		else:
			notes += (
				" The SCR is fitted but the sheet leaves its connector destination without a function label, and the "
				"retained harness run did not observe the ROM driving it. Failure to observe an address is not proof "
				"that it is unused, so this is enumerated with an unknown disposition rather than called unused."
			)
			availability = "unknown"
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
			"physical": {"notes": notes},
			"wiring": {"board": "Bally Auxiliary Lamp Driver AS-2518-52"},
		}
		if known and known[1]:
			extra["wiring"]["control_connection"] = known[1]
		status = "validated" if known else "candidate"
		if address in AUX_DECODER_N_U:
			extra["spatial"] = not_applicable("unused", SCHEMATICS_SOURCE)
			status = "validated"
		elif known and known[2]:
			extra["spatial"] = located(identifier, "emitter", known[2], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			extra["physical"]["notes"] += (
				" No single coordinate is asserted: the retained table either models nothing at this address or "
				"models it as a cluster of co-located and out-of-bounds render lights from which a per-bulb count "
				"cannot be derived, and the manual prints no quantity."
			)
		items.append(
			_device(
				identifier,
				label,
				"lamp",
				"pinmame.output.lamp",
				address,
				availability,
				(SCHEMATICS_SOURCE, MANUAL_SOURCE, HARNESS_SOURCE),
				**extra,
			)
		)
		items[-1]["provenance"]["status"] = status
	return items


def displays() -> list[dict[str, Any]]:
	records = []
	for index in range(4):
		records.append(
			{
				"id": f"display.player-{index + 1}-score",
				"label": f"Player {index + 1} score, seven digits",
				"kind": "segment",
				"controller_index": index,
				"segment_start": index * 8,
				"width": 7,
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
				"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, HARNESS_SOURCE),
			}
		)
	records.append(
		{
			"id": "display.credits",
			"label": "Credit display, two digits",
			"kind": "segment",
			"controller_index": 4,
			"segment_start": 35,
			"width": 2,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, HARNESS_SOURCE),
		}
	)
	records.append(
		{
			"id": "display.match-ball-in-play",
			"label": "Match / Ball in Play display, two digits",
			"kind": "segment",
			"controller_index": 5,
			"segment_start": 38,
			"width": 2,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, HARNESS_SOURCE),
		}
	)
	return records


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str) -> dict[str, Any]:
		return {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}

	def dev(label: str) -> str:
		return f"device.{slug(label)}"

	def lamp(address: int) -> str:
		return f"lamp.{slug(LAMPS[address][0])}-{address}"

	return [
		mechanism(
			"mechanism.outhole-and-trough",
			"Outhole and three-station ball trough",
			"kicker",
			[dev("Outhole Kicker")],
			["switch.matrix-1", "switch.matrix-2", "switch.matrix-3"],
			"Fathom is a three-ball multiball game, so the outhole area carries three switch stations rather than "
			"one. The printed names are Outhole (1), #1 Left of Outhole (2) and #2 Left and #1 Right of Outhole (3); "
			"the third name records that one matrix contact is shared by two ball positions. Public solenoid 7, "
			"printed Self Test 13 Outhole Kicker, kicks the ball from the outhole to the shooter lane. The retained "
			"known-working script models the whole assembly as one cvpmBallStack initialised with exactly these "
			"three addresses (bsTrough.Initsw 0,1,2,3) and kicks from the BallRelease object.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_SOURCE,
		),
		mechanism(
			"mechanism.solenoid-expander",
			"Solenoid Expander relay (A15, AS-2518-66)",
			"other",
			[lamp(47)],
			[],
			"The Bally MPU AS-2518-35 publishes only fifteen momentary solenoid addresses, and the printed Solenoid "
			"Identification Table lists nineteen momentary functions. The Solenoid Expander closes the gap: a "
			"lamp-driver SCR output (public lamp address 47, printed A5J2-2 TO AUX. EXPANDOR J1-2, reaching the "
			"expander's own J1-2 printed SCR ANODE LAMP DRIVER) drives a MOC3011 optocoupler which energizes a 48 V "
			"relay K1. The relay's contacts switch the 43 VDC solenoid bus between two groups of coils, so five "
			"driver outputs each reach one of two coils depending on the relay state: public 1, 2 and 3 reach the "
			"3 Top, 6 Drop and 3 Middle bank reset coils with the relay de-energized and the 1st, 2nd and 3rd Green "
			"Inline drop coils with it energized, and public 13 and 14 reach the Top and Right saucer kickers or the "
			"1st and 2nd Blue Inline drop coils. Public 4 (Right Inline reset) and public 15 (3rd Blue Inline) are "
			"not shared. The retained harness run of the ROM's solenoid self test shows the relay lamp asserted "
			"immediately before and during each of the six in-line drop pulses and off for every reset and saucer "
			"pulse, which is what establishes the direction of the gating.",
			SCHEMATICS_SOURCE, HARNESS_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.left-six-bank",
			"Left side six-bank drop targets",
			"drop_target_bank",
			[dev("6 Drop Target Reset / 2nd Green Inline Drop Target")],
			[f"switch.matrix-{n}" for n in range(27, 33)],
			"Six drop targets in a vertical column on the left side, printed A (top) through F (bottom) and wired "
			"F..A at switches 27..32, so the switch address ascends as the target position rises up the playfield. "
			"The bank is raised by public solenoid 2 (printed Self Test 10, 6 Drop Target Reset); the retained "
			"script binds that address to its dtL cvpmDropTarget with the array sw27..sw32. Knocking down all six "
			"is the machine's principal bonus-advance feature. Hitting the rebound rubber behind the bank scores on "
			"switch 19, which is shared with the 10-point rubber.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_SOURCE,
		),
		mechanism(
			"mechanism.middle-three-bank",
			"Middle three-bank drop targets",
			"drop_target_bank",
			[dev("3 Middle Drop Target Reset / 3rd Green Inline Drop Target")],
			["switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Three drop targets across the centre of the playfield, printed #1, #2 and #3 and wired #3..#1 at "
			"switches 33..35, so #1 is the leftmost. Raised by public solenoid 3 (printed Self Test 11); the "
			"retained script's dtM cvpmDropTarget uses the array sw33, sw34, sw35. The manual's feature description "
			"states that knocking down 1, 2, 3 targets in order lights the extra-ball target.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_SOURCE,
		),
		mechanism(
			"mechanism.blue-inline-bank",
			"Blue in-line drop target bank (printed 3 Top)",
			"drop_target_bank",
			[
				dev("3 Top Drop Target Reset / 1st Green Inline Drop Target"),
				dev("3rd Blue Inline Drop Target"),
			],
			["switch.matrix-42", "switch.matrix-43", "switch.matrix-44"],
			"Three drop targets in line one behind the other in a lane across the top of the playfield, so the ball "
			"can only reach the front one. Each position therefore has its own coil that knocks that target down "
			"when the ROM decides to advance the sequence, plus one reset coil for the bank. Switches 44, 43 and 42 "
			"are the 1st, 2nd and 3rd targets, and their retained objects run left to right, so the 1st target is "
			"the leftmost. The bank reset is public solenoid 1 (printed Self Test 09, 3 Top Drop Target Reset), and "
			"the individual drop coils are public 13, 14 and 15 (printed Self Test 17, 18, 19), of which 13 and 14 "
			"are shared with the two saucer kickers through the Solenoid Expander relay - so they are listed as "
			"actuators of the two saucer mechanisms, which own them, rather than repeated here - while 15 is a "
			"dedicated output. Option switch S22 selects whether a target left down carries over to the next ball.",
			MANUAL_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.green-inline-bank",
			"Green in-line drop target bank (printed Right Inline)",
			"drop_target_bank",
			[dev("Right Inline Drop Target Reset")],
			["switch.matrix-46", "switch.matrix-47", "switch.matrix-48"],
			"The second in-line bank, in a lane up the right side of the playfield. Switches 48, 47 and 46 are the "
			"1st, 2nd and 3rd targets and their retained objects ascend the playfield, so the 1st target is nearest "
			"the player. The bank reset is public solenoid 4 (printed Self Test 12, Right Inline Drop Target Reset), "
			"a dedicated output, while the three individual drop coils are public 1, 2 and 3 (printed Self Test 14, "
			"15, 16) shared with the three bank reset coils through the Solenoid Expander relay, so they are listed "
			"as actuators of the three bank-reset mechanisms that own them (public 1 on the blue in-line bank, 2 on "
			"the left six-bank, 3 on the middle three-bank) rather than repeated here. That is why the printed table "
			"lists nineteen momentary functions on fourteen driver outputs.",
			MANUAL_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.top-saucer",
			"Top saucer",
			"kicker",
			[dev("Top Saucer Kicker / 1st Blue Inline Drop Target")],
			["switch.matrix-4", "switch.matrix-25"],
			"A saucer at the top right of the playfield. Switch 4 (Top Saucer) reports a ball resting in it and "
			"public solenoid 13 (printed Self Test 02, Top Saucer) kicks it out; the retained script models this as "
			"a cvpmBallStack saucer on object sw4. Switch 25 (Top Saucer Rollover Button) is a separate rollover in "
			"the lane feeding the saucer. Option switch S6 selects whether a ball left in a saucer is kicked out at "
			"the end of the game. With the Solenoid Expander relay energized the same driver output drops the 1st "
			"Blue Inline target instead of firing this kicker.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_SOURCE,
		),
		mechanism(
			"mechanism.right-saucer",
			"Right saucer",
			"kicker",
			[dev("Right Saucer Kicker / 2nd Blue Inline Drop Target")],
			["switch.matrix-5", "switch.matrix-26"],
			"A second saucer part way down the right side. Switch 5 reports the ball and public solenoid 14 "
			"(printed Self Test 03, Right Saucer) kicks it out, modelled in the retained script as a cvpmBallStack "
			"saucer on object sw5, with switch 26 (Right Saucer Rollover Button) as the separate rollover feeding "
			"it. Shares its driver output with the 2nd Blue Inline drop coil through the Solenoid Expander relay.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_SOURCE,
		),
		mechanism(
			"mechanism.thumper-bumpers",
			"Three thumper bumpers",
			"other",
			[dev("Left Thumper Bumper"), dev("Bottom Thumper Bumper"), dev("Right Thumper Bumper")],
			["switch.matrix-38", "switch.matrix-39", "switch.matrix-40"],
			"Three CPU-driven pop bumpers in the upper middle of the playfield. The skirt switch closes, the ROM "
			"pulses the matching coil: left switch 40 with coil 8, bottom switch 39 with coil 9, right switch 38 "
			"with coil 10 (printed Self Test 04, 05, 06). Each has its own lamp inside the bumper body: public lamp "
			"12 for the right bumper, 28 for the bottom and 44 for the left, per the printed A5J1-27, A5J1-12 and "
			"A5J3-24 functions. The retained table binds lamps 12 and 28 the other way round; see "
			"conflict.thumper-bumper-lamp-address-swap.",
			MANUAL_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.slingshots",
			"Two slingshots",
			"other",
			[dev("Left Slingshot"), dev("Right Slingshot")],
			["switch.matrix-36", "switch.matrix-37"],
			"Standard pair of slingshots above the flippers. Left switch 37 with coil 11, right switch 36 with coil "
			"12 (printed Self Test 07, 08). The retained table's own wall objects independently confirm the sides: "
			"LeftSlingShot normalizes to x 0.222 and RightSlingShot to x 0.689.",
			MANUAL_SOURCE, HARNESS_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.flippers",
			"Three flippers behind the K1 flipper-enable relay",
			"other",
			[dev("Lower Right and Upper Right Flipper Coils"), dev("Lower Left Flipper Coil")],
			["switch.matrix-7"],
			"Two lower flippers and one upper right flipper. None of the three coils has a driver-board momentary "
			"output: the A3 sheet wires all three to the 43 VDC bus through the contacts of relay K1, the "
			"flipper-enable relay, with the cabinet buttons in series. Public solenoid 19 (printed Self Test 21, K1 "
			"Relay (Flipper Enable)) energizes the relay, and pinned by35.c passes exactly that address into "
			"core_updateSw as the game-on signal. The upper right flipper is wired in parallel with the lower right "
			"flipper, so one button fires both; the retained script reproduces this by rotating RightFlipper and "
			"RightFlipper1 from one callback. Only the right button is in the switch matrix (switch 7); the left "
			"button is direct-wired and the ROM cannot read it.",
			SCHEMATICS_SOURCE, MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.spinner",
			"Spinner",
			"other",
			[],
			["switch.matrix-18"],
			"A single spinner on the left side, switch 18, with its own insert lamp at public lamp 60 (printed "
			"A5J3-14 SPINNER). No coil is involved; the retained script pulses the switch from the Spinner object's "
			"_Spin event.",
			MANUAL_SOURCE, SCHEMATICS_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.captive-balls",
			"Lagoon and Cave captive balls",
			"other",
			[],
			[],
			"Fathom's multiball comes from two captive balls, named Lagoon and Cave on the lamp harness. Each has "
			"its own release insert - public lamp 40 (printed A5J1-13 RELEASE LAGOON CAPTIVE BALL) and public lamp "
			"56 (printed A5J3-2 RELEASE CAVE CAPTIVE BALL) - which lights when the ball may be released. No "
			"controller output releases them: the player releases each captive ball by hitting it while its insert "
			"is lit, which is why neither has an actuator and why the three-station outhole trough exists.",
			MANUAL_SOURCE, SCHEMATICS_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	def dev(label: str) -> str:
		return f"device.{slug(label)}"

	relay = f"lamp.{slug(LAMPS[47][0])}-47"
	items = []
	for label in (
		"3 Top Drop Target Reset / 1st Green Inline Drop Target",
		"6 Drop Target Reset / 2nd Green Inline Drop Target",
		"3 Middle Drop Target Reset / 3rd Green Inline Drop Target",
		"Top Saucer Kicker / 1st Blue Inline Drop Target",
		"Right Saucer Kicker / 2nd Blue Inline Drop Target",
	):
		items.append(
			{
				"id": f"relationship.expander-gates-{slug(label)}",
				"kind": "relay_gated",
				"source": relay,
				"destination": dev(label),
				"provenance": provenance(SCHEMATICS_SOURCE, HARNESS_SOURCE),
			}
		)
	items.append(
		{
			"id": "relationship.flipper-enable-gates-right-flippers",
			"kind": "relay_gated",
			"source": f"device.{slug('K1 Relay (Flipper Enable)')}",
			"destination": dev("Lower Right and Upper Right Flipper Coils"),
			"provenance": provenance(SCHEMATICS_SOURCE, CORE_SOURCE),
		}
	)
	items.append(
		{
			"id": "relationship.flipper-enable-gates-left-flipper",
			"kind": "relay_gated",
			"source": f"device.{slug('K1 Relay (Flipper Enable)')}",
			"destination": dev("Lower Left Flipper Coil"),
			"provenance": provenance(SCHEMATICS_SOURCE, CORE_SOURCE),
		}
	)
	return items


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.thumper-bumper-lamp-address-swap",
			"path": "outputs[binding.group=pinmame.output.lamp,binding.device=12,28]",
			"description": (
				"Which thumper bumper lamp sits on which public address. Fathom's own A5 lamp driver sheet prints "
				"A5J1-27 RIGHT THUMPER BUMPER and A5J1-12 BOTTOM THUMPER BUMPER, and the playfield wiring diagram "
				"prints the same two functions on the same two pins with wires 53 and 61; the AS-2518-23 board's "
				"public-address to connector-pin mapping, identical on Bally Centaur and Bally Kiss and confirmed "
				"here by straight-line trace of U1's first twelve outputs and by arrow count, puts public 12 on "
				"A5J1-27 and public 28 on A5J1-12. That makes public 12 the right bumper and public 28 the bottom "
				"bumper. The retained known-working table binds them the other way round: its address-12 light "
				"objects (Light12, Light12a) normalize to (0.513, 0.325), which is the bottom bumper, and its "
				"address-28 objects to (0.662, 0.251), which is the right bumper, and its own commented-out lines "
				"label 12 'Bumper3' and 28 'Bumper2'. Both sides agree that public 44 is the left bumper. The "
				"definition follows the manual because lamp-to-bulb identity is physical construction rather than "
				"runtime semantics, and because three printed sources agree against one community recreation, but "
				"the disagreement is unresolved on the evidence retained here: settling it needs a lamp test on real "
				"hardware or a photograph of the A5J1 harness. Resolution path: a lamp test on an unrestored machine "
				"observing which thumper bumper lights while public 12 and public 28 are driven in turn, or a "
				"photograph of the A5J1 harness showing which bumper socket pins 12 and 27 each feed; a LibPinMAME "
				"trace cannot settle it, because PinMAME reports the matrix bit rather than the bulb it reaches. "
				"Unresolved."
			),
			"source_refs": [SCHEMATICS_SOURCE, MANUAL_SOURCE, BOARD_SOURCE, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE],
		},
	]


def source_records() -> list[dict[str, Any]]:
	def excerpt(identifier: str, locator: str, name: str, digest: str, *, reviewed: bool = True) -> dict[str, Any]:
		return {
			"id": identifier,
			"locator": locator,
			"path": f"evidence/excerpts/{MACHINE_ID}/{name}",
			"sha256": digest,
			"method": "manual",
			"transcribed_by": "curator, read from rendered pages",
			"reviewed": reviewed,
		}

	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the fathom clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/by35games.c line 1264 INITGAME2(fathom, GEN_BY35, dispBy7, FLIP_SW(FLIP_L), 8, "
				"SNDBRD_BY61B, 0), which expands through the INITGAME2 macro to core_tGameData "
				"{gen, disp, {flippers, swCol=0, lampCol=8, custSol=0, soundBoard, display, BY35GD_NOSOUNDE}} - the "
				"fifth macro argument is the auxiliary lamp-column count, not a switch-column count - together with "
				"#define init_fathoma init_fathom and #define init_fathomb init_fathom; src/wpc/by35.c pia1b_w "
				"(momentary selector on PIA1:B bits 0-3, public address = selector + 1, selector 15 masked off; "
				"continuous nibble inverted and published at 17-20), pia0b_r (five strobes from PIA0:A bits 0-4 plus "
				"a sixth from (locals.b1 & 0x80) >> 2 on the default non-BY35GD_SWVECTOR path), by35_lampStrobe "
				"(decoder selector 0x0f skipped, two matrix columns per data bit, board 1 offset by eight columns) "
				"and by35_vblank's core_updateSw(core_getSol(19)); src/wpc/by35.h BY35_SWSELFTEST/BY35_SWCPUDIAG/"
				"BY35_SWSOUNDDIAG and the BY35GD_ flags; src/wpc/core.c core_getSol's solNo <= 28 branch, which is "
				"why public solenoid addresses above 20 read constant zero on this generation; "
				"src/lisy/lisy35.c lisy35_set_variant case 3 (Fathom) setting lisy35_J4PIN8_is_strobe and "
				"lisy35_solenoid_handler masking cont_data &= 0x07; src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_BY35 = 0x0000000400000"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/by35.json",
			"revision": "repository",
			"locator": (
				"Bally MPU AS-2518-35 public address rules: sequential switch-matrix positions, the -7/-6/-5 "
				"diagnostic contacts, momentary solenoids 1-15 with no 16, continuous outputs 17-20, the synthetic "
				"flipper outputs 46 and 48, and the four runs of fifteen lamp addresses per driver board"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": BOARD_SOURCE,
			"kind": "human_review",
			"uri": "internal:machines/partial/bally/centaur-1981.json",
			"revision": "repository",
			"locator": (
				"The AS-2518-23 lamp driver's public-address to connector-pin mapping, which is a property of the "
				"board rather than of a game. machines/partial/bally/centaur-1981.json and "
				"machines/author-ready/bally/kiss-1979.json record identical mappings for all sixty addresses, "
				"including the eight outputs that branch to a second connector pin (11, 12, 27, 28, 43, 44, 59, 60). "
				"Fathom's own A5 sheet reproduces it independently for U1's first twelve outputs by straight-line "
				"trace, and the eight N/U pins that carry an arrow on Fathom's sheet are exactly those eight branch "
				"destinations, which is what makes the transfer safe. Which branch a harness actually plugs remains "
				"game-specific and is taken from Fathom's own printed pin functions."
			),
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.fathom.1981/ipdb/Bally_1981_Fathom_English_Manual.pdf",
			"original_filename": "Bally_1981_Fathom_English_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"40-page scan of the Bally game #1233 Fathom operations manual, 1981. Printed page 17 (PDF page 23) "
				"carries the Solenoid Identification Table and the Switch Assembly Self-Test Display Numbers; "
				"printed pages 5 to 7 carry the MPU option switches and game feature options; the routine-maintenance "
				"page describes the self-test sequence; PDF pages 27 to 40 carry the module parts lists including the "
				"AS-2518-52 auxiliary lamp driver and the AS-2518-66 solenoid expander."
			),
			"license": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; scan obtained through IPDB",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.fathom.self-test-tables",
					"locator": "PDF page 23, printed page 17: SOLENOID IDENTIFICATION TABLE and SWITCH ASSEMBLY SELF-TEST DISPLAY NUMBERS, both transcribed in full including the three blank switch rows",
					"path": f"evidence/excerpts/{MACHINE_ID}/self-test-tables.md",
					"image": f"evidence/excerpts/{MACHINE_ID}/self-test-tables.webp",
					"sha256": "cda246eed6dfa8d71b71ec59f70832680f29fb438ca8a638baf160f98edaba84",
					"image_sha256": "011e2247b6f44ab2673196205916f292fc381564034ce809020377caab9d0bfe",
					"image_derivation": "Bally_1981_Fathom_English_Manual.pdf page 23, crop box 0.0654,0.0694,0.9477,0.8838, scanned page rendered at its native resolution (embedded image xref 95, 1275px across 8.50in), rendered at 93 dpi, capped to 700px wide, 701x837 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered pages",
					"reviewed": True,
				},
				excerpt(
					"excerpt.fathom.game-adjustments",
					"PDF pages 11, 12, 13 and 19: the self-test procedure and the complete MPU option switch S1-S32 map",
					"game-adjustments.md",
					"fae1d5672cddd11efe586485f45b2588430d2417a0298eee8c9f6a4e3f4ff87b",
				),
				excerpt(
					"excerpt.fathom.auxiliary-lamp-driver-a9",
					"PDF page 37 (A9 AUXILIARY LAMP DRIVER AS-2518-52 component parts list) together with schematics PDF page 6",
					"auxiliary-lamp-driver-a9.md",
					"f81395c4f0b727d566a76440361d2259408c84ba6fe4778fda61e2be348a6add",
				),
			],
		},
		{
			"id": SCHEMATICS_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.fathom.1981/ipdb/Bally_1981_Fathom_Schematics.pdf",
			"original_filename": "Bally_1981_Fathom_Schematics.pdf",
			"sha256": SCHEMATICS_SHA256,
			"locator": (
				"12-page scan of the Bally game #1233 Fathom schematics. PDF page 6 is AUXILIARY LAMP DRIVER A9 "
				"(W-1207-9), page 7 is SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC (W-1183-34c), page 8 is A5 LAMP "
				"DRIVER SCHEMATIC (W-1182-34c), page 9 is SOLENOID EXPANDER (W-1251b) and page 11 is WIRING DIAGRAM "
				"PLAYFIELD (W-1192-30). Every sheet carries the game number 1233 in its title block, which is how "
				"this document was confirmed to be Fathom's own rather than a generic board set."
			),
			"license": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; scan obtained through IPDB",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.fathom.solenoid-driver-a3",
					"locator": "PDF page 7, SOLENOID DRIVER VOLTAGE REGULATOR SCHEMATIC W-1183-34c: the 74L154 momentary decode, all fifteen driver stages, the four continuous outputs and every connector destination label",
					"path": f"evidence/excerpts/{MACHINE_ID}/solenoid-driver-a3.md",
					"image": f"evidence/excerpts/{MACHINE_ID}/solenoid-driver-a3.webp",
					"sha256": "c62783a5b8299ab3868bd30d813e843650ff375bb2437e1cc8b5ce73ee1c1fbc",
					"image_sha256": "8b7fcbbaad259d2fe17ad24b427f7bee85265567de8729fb6a1cfd4f3f998f5c",
					"image_derivation": "Bally_1981_Fathom_Schematics.pdf page 7, crop box 0.06,0.01,0.995,0.98, scanned page rendered at its native resolution (embedded image xref 30, 10030px across 17.00in), rendered at 63 dpi, capped to 1000px wide, 1001x673 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered pages",
					"reviewed": True,
				},
				{
					"id": "excerpt.fathom.lamp-driver-a5",
					"locator": "PDF page 8, A5 LAMP DRIVER SCHEMATIC W-1182-34c: the four MC14514CP decoders, all sixty output-to-SCR pairs and the complete J1/J2/J3 printed pin function lists",
					"path": f"evidence/excerpts/{MACHINE_ID}/lamp-driver-a5.md",
					"image": f"evidence/excerpts/{MACHINE_ID}/lamp-driver-a5.webp",
					"sha256": "9b7ab72dece71b4b8dddae414cc2bf323c92a24b1c22aef8f9ac60ded07235d4",
					"image_sha256": "c97643aca5df79d9ac10b7c9ef6337bd2a9ba4be2a57a4319408e46e16081959",
					"image_derivation": "Bally_1981_Fathom_Schematics.pdf page 8, crop box 0.01,0.015,0.995,0.98, scanned page rendered at its native resolution (embedded image xref 35, 10030px across 17.00in), rendered at 60 dpi, capped to 1000px wide, 1001x635 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered pages",
					"reviewed": True,
				},
				{
					"id": "excerpt.fathom.playfield-wiring",
					"locator": "PDF page 11, WIRING DIAGRAM PLAYFIELD W-1192-30: switch-matrix strobe and return wiring, solenoid coil wires and connectors, general illumination, and the A5J1/A5J2/A5J3 lamp harness lists",
					"path": f"evidence/excerpts/{MACHINE_ID}/playfield-wiring.md",
					"image": f"evidence/excerpts/{MACHINE_ID}/playfield-wiring.webp",
					"sha256": "760e6805942d5d6f71cd25de69bc5c3347a7f5c164ff3c66e3ddafd6750a37f6",
					"image_sha256": "7d85b0e1741110cf0b17668c7145a8c7ca1c3b0c8ae6bda95798f12b82e84054",
					"image_derivation": "Bally_1981_Fathom_Schematics.pdf page 11, crop box 0.03,0.02,0.993,0.965, scanned page rendered at its native resolution (embedded image xref 50, 10030px across 17.00in), rendered at 159 dpi, capped to 2600px wide, 2601x1652 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from rendered pages",
					"reviewed": True,
				},
				{
					"id": "excerpt.fathom.lamp-driver-a5-u1-fanout",
					"locator": "PDF page 8, A5 LAMP DRIVER SCHEMATIC W-1182-34c: the U1 SCR bank and the twelve J1 pins its outputs run straight across to",
					"path": f"evidence/excerpts/{MACHINE_ID}/lamp-driver-a5-u1-fanout.webp",
					"image": f"evidence/excerpts/{MACHINE_ID}/lamp-driver-a5-u1-fanout.webp",
					"sha256": "13d73ffc95b3f798cc0cfe80c4eb865faaca6c7660ad163f5cc3cd6c3768601f",
					"image_sha256": "13d73ffc95b3f798cc0cfe80c4eb865faaca6c7660ad163f5cc3cd6c3768601f",
					"image_derivation": "Bally_1981_Fathom_Schematics.pdf page 8, crop box 0.525,0.055,0.93,0.26 of the page, rendered at 300 dpi with pdftoppm, reduced to 1400px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fathom.aux-lamp-driver-a9-annotated-outputs",
					"locator": "PDF page 6, AUXILIARY LAMP DRIVER A9 W-1207-9: the four MC14028B decoders, their 28 SCRs, and the seven SCR outputs the sheet annotates with a function",
					"path": f"evidence/excerpts/{MACHINE_ID}/aux-lamp-driver-a9-annotated-outputs.webp",
					"image": f"evidence/excerpts/{MACHINE_ID}/aux-lamp-driver-a9-annotated-outputs.webp",
					"sha256": "e578b63694a4e950b5ef2a9f6a8ff0fc1c407d5790e051b37ab915850d83357c",
					"image_sha256": "e578b63694a4e950b5ef2a9f6a8ff0fc1c407d5790e051b37ab915850d83357c",
					"image_derivation": "Bally_1981_Fathom_Schematics.pdf page 6, crop box 0.58,0.06,0.92,0.45 of the page, rendered at 300 dpi with pdftoppm, reduced to 1400px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": HARNESS_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-review-artifacts/fathom-1981/harness-solenoid-self-test.json",
			"revision": "2026-08-08",
			"sha256": HARNESS_SHA256,
			"locator": (
				"LibPinMAME harness run of the production fathom ROM, built from the pinned PinMAME revision, in an "
				"isolated writable state directory with the operator's own authorized ROM archive mounted read-only. "
				"Scenario: boot, wait 18 s for the power-up test to complete, then pulse the Self Test contact (-7) "
				"three times at 4 s intervals to reach the ROM's solenoid test, then observe for 40 s. The recorded "
				"solenoid transitions repeat a twenty-one-pulse cycle in the exact order of the printed Solenoid "
				"Identification Table: public 6, 13, 14, 8, 9, 10, 11, 12, 1, 2, 3, 4, 7, 1, 2, 3, 13, 14, 15, 18, "
				"19 for printed entries 01 through 21. The same run shows public lamp 47 asserted immediately before "
				"and during each of the six in-line drop-target pulses and off for every reset and saucer pulse. A "
				"companion boot-only run (harness-boot.json, SHA-256 " + BOOT_HARNESS_SHA256 + ") records public "
				"solenoid 20 asserted continuously once the game is up, which is the sixth switch-column strobe. No "
				"ROM bytes or NVRAM blobs are retained."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/fathom-1981/source/Fathom%20%28Bally%201981%29.vpx",
			"original_filename": "Fathom (Bally 1981).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working community recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:.0f} and y/{PLAYFIELD_HEIGHT:.0f}. "
				"The 1974 bottom bound is far shorter than the 2117 to 2594 of the 1990s machines curated in this "
				"project, which is consistent with an early-1980s playfield. Geometry authority only, for named "
				"table objects. A normalized dump of every object is retained at "
				"external:pinmame-review-artifacts/fathom-1981/vpx-geometry.txt, SHA-256 " + GEOMETRY_SHA256 + "."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/fathom-1981/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script, 89,378 bytes. Line 982 reads Const cGameName="Fathom" with a capital F, '
				"which is not a PinMAME driver short name; the driver is fathom, and VPinMAME resolves the game name "
				"case-insensitively, so the script binds the pinned production parent. Runtime authority for: the "
				"SolCallback table for public solenoids 1, 2, 3, 4, 6, 7, 13, 14, 15 and the core.vbs sLRFlipper and "
				"sLLFlipper bindings; the vpmTimer.PulseSw and Controller.Switch calls for switches 7, 12, 13, 14, "
				"17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 38, 39, 40; the four cvpmDropTarget instances dtL "
				"(sw27-sw32), dtM (sw33-sw35), dtT (sw42-sw44) and dtR (sw46-sw48); the three cvpmBallStack "
				"instances bsTrough (Initsw 0,1,2,3), bsTopEject (saucer sw4) and bsRightEject (saucer sw5); and the "
				"UpdateLamps routine, which binds public lamp addresses to named light objects. Its SolCallback "
				"assignments for addresses 25, 26, 27, 37 and 38 are dead code on this platform: pinned "
				"core_getSol's solNo <= 28 branch reads coreGlobals.solenoids, where a Bally MPU driver only ever "
				"sets bits 0-14 and 16-19, and the 37-44 branch serves only GEN_WPC95 and GEN_ALLS11, so those five "
				"callbacks can never fire. The ROM's own solenoid self test shows the six individual in-line "
				"drop-target coils are really at public 1, 2, 3, 13, 14 and 15."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/fathom-1981/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=838",
			"revision": "2026-08-08",
			"locator": (
				"IPDB entry for Bally's Fathom (1981), Bally game number 1233. The physical release year is fixed "
				"here from the machine's own manual rather than from IPDB: the title page of the retained manual "
				"reads GAME 1233 and (c) BALLY MFG. CORP 1981, every schematic title block carries the game number "
				"1233 with 1981 approval dates, and pinned PinMAME dates the parent driver 1981 for Bally. The two "
                                "fathoma and fathomb clones are dated 2004 for Bally / Oliver, which is a ROM release date for "
				"later firmware on the same physical machine, not a second physical game."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database",
		},
	]


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
	for driver_id in DRIVER_IDS:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		items.append(item)
	return items


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Fathom",
			"manufacturer": "Bally",
			"year": 1981,
			"kind": "physical_pinball",
			"ipdb_id": 829,
			"opdb_id": "GrPO3-M9Rpx",
			"playfield": {
				"units": "vpx",
				"width": PLAYFIELD_WIDTH,
				"height": PLAYFIELD_HEIGHT,
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
		},
		"coverage": {
			"status": "partial",
			"missing": ["output_semantics", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "candidate",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.by35",
			"hardware_generation": "0x0000000400000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/fathom-1981.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Fathom device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	placement_count = 0
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved_outputs: list[dict[str, Any]] = []
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "partial",
		"blockers": [
			"Twenty-two auxiliary lamp addresses on the AS-2518-52 board carry no semantic identity. Fathom's own "
			"A9 sheet annotates only seven of its twenty-eight SCR outputs with a function, and the harness blocks "
			"it draws for the remaining connector pins print wire numbers, N/U and KEY entries but no functions. "
			"Five of the unannotated addresses (67, 83, 99, 114, 115) are proven driven by the ROM in the retained "
			"harness run and sixteen more are fitted but unobserved, so they are enumerated honestly rather than "
			"named or declared unused.",
			"Three auxiliary addresses that do carry a printed function (66, 82, 98, the combined back-scan and "
			"left-lane-scan circuits) have no asserted coordinate. Their printed names imply more than one bulb, the "
			"manual prints no quantity, and the retained table models each as a cluster of co-located and "
			"out-of-bounds render lights, three of which normalize to a negative x, from which a per-bulb count "
			"cannot be derived.",
			"Public lamp 43 (Same Player Shoot Again, printed A5J3-22) is a genuine playfield insert with no light "
			"object bound to it anywhere in the retained extraction and no reference in the retained script, so its "
			"spatial key is omitted rather than a coordinate being invented.",
			"Public lamps 12 and 28 carry an unresolved identity disagreement between the printed wiring and the "
			"retained table (conflict.thumper-bumper-lamp-address-swap). Their coordinates are the two bumper "
			"assemblies the manual names, so no coordinate is invented, but the disagreement keeps the record "
			"partial.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:.0f}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:.0f}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/fathom-1981/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"schematics_sha256": SCHEMATICS_SHA256,
			"table_sha256": TABLE_SHA256,
			"harness_sha256": HARNESS_SHA256,
			"geometry_dump_sha256": GEOMETRY_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"unresolved_inputs": sorted(unresolved_inputs),
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.lamp", "address": address, "reason": reason} for address, reason in sorted(LAMP_PROJECTIONS.items())]
		),
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.fathom.1981/",
			"transcription": {
				"path": f"evidence/excerpts/{MACHINE_ID}/",
				"sha256": GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"Light L12, which normalizes to exactly the same coordinate as Light L1 and is a co-located leftover rather than a second bulb.",
			"Light L13, a stray object at (0.906, 0.653) for an address the printed wiring puts in the back box and which the retained script's own lamp routine leaves commented out.",
			"Trigger sw1, an unused object at (0.701, 0.005) with no handler anywhere in the retained script; the outhole switch is modelled by the ball stack instead.",
			"HitTarget sw42a, sw43a and sw44a, the rear meshes of the three blue in-line targets, which the retained script passes as second elements of the same drop-target array rather than as separate targets.",
			"Trigger sw20c1, a fourth rollover object with no handler; the printed name gives three rollover buttons and the script drives three.",
			"Light Light66g, Light81a and Light82g, which normalize to a negative x and are table modelling anomalies rather than bulbs.",
		],
		"unresolved": (
			["lamp.same-player-shoot-again-43"]
			+ [f"lamp.aux-{address}" for address in sorted(list(AUX_DRIVEN_UNNAMED) + AUX_UNLABELLED + [66, 82, 98])]
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Fathom (Bally, 1981) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record stays `partial` at "
		"`machines/partial/bally/fathom-1981.json`: twenty-two auxiliary lamp addresses have no semantic identity, "
		"four lamp addresses have no asserted coordinate, and one printed-versus-table identity disagreement is "
		"unresolved. Every switch, every solenoid and all sixty main-board lamp addresses are otherwise complete.",
		"",
		"The matching source is the retained known-working `Fathom (Bally 1981).vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`. Exact playfield bounds are `{TABLE_BOUNDS}`, so every canonical coordinate is "
		f"x/{PLAYFIELD_WIDTH:.0f} and y/{PLAYFIELD_HEIGHT:.0f} rounded to at most six fractional places. The trough "
		"kicker lands at y 0.863, the outhole drain at 0.956, the flippers at 0.844 and the plunger at 0.978, which "
		"is the sanity check that the y divisor is right.",
		"",
		"## Evidence decisions",
		"",
		"- This is a Bally MPU AS-2518-35 machine and reuses `controllers/pinmame/by35.json` unchanged. The fifth "
		"argument of its `INITGAME2` line is the auxiliary lamp-column count, **not** a switch-column count: "
		"`core_tGameData.hw` is `{flippers, swCol, lampCol, custSol, ...}` and the macro passes `0` for `swCol`. "
		"Fathom declares `lampCol = 8`, like Bally Centaur and Bally Kiss.",
		"- Fathom is a six-column switch machine: the printed self-test table numbers forty-eight positions and the "
		"playfield wiring diagram draws six strobes. The sixth strobe `ST 5` comes from `A4J4-8`, which is the "
		"PIA1:B PB7 line published as continuous solenoid **20**, not 17. Three sources agree: the playfield sheet's "
		"own connector, `by35.c`'s default `(locals.b1 & 0x80) >> 2` column path, and `lisy35.c`'s Fathom case, "
		"which sets `lisy35_J4PIN8_is_strobe` and masks that bit out of the coil data. The retained harness run "
		"shows address 20 asserted continuously from the moment the game comes up. Bally Centaur spends public 17 "
		"on its sixth strobe and Bally Kiss spends 17 on a real coil; neither precedent transfers.",
		"- The printed `Self Test #` column is a test order. The ROM's own solenoid test, captured in the retained "
		"harness run, pulses the coils in printed order 01 through 21 and resolved the whole mapping at once, "
		"including the fact that printed 01 (Knocker) is public 6 and printed 13 (Outhole Kicker) is public 7 - the "
		"same outhole address Centaur and Kiss use.",
		"- Nineteen printed momentary functions sit on fourteen driver outputs because the Solenoid Expander "
		"(A15, AS-2518-66) relay-gates five of them between two coils each. Public lamp 47 is the relay's control "
		"input, not a bulb; the harness run proves it by showing that address energized only around the six in-line "
		"drop-target pulses.",
		"- Public momentary 5 and public continuous 17 are genuinely spare: the A3 sheet routes 17 only to pins "
		"printed N/U, and the self-test cycle never pulses either address.",
		"- The AS-2518-23 public-address to connector-pin mapping is a board property. Bally Centaur and Bally Kiss "
		"record identical mappings for all sixty addresses including the eight branch outputs, Fathom's own A5 sheet "
		"reproduces it for U1's first twelve outputs by straight-line trace, and the eight `N/U` pins that carry an "
		"arrow on Fathom's sheet are exactly those eight branch destinations. Fathom's own printed pin functions "
		"then name every address. Independent checks that fell out of this: the blue bonus ladder 1K to 7K lands on "
		"addresses 2, 18, 34, 50, 3, 19, 35 whose retained light objects climb one column at constant x with "
		"monotonically decreasing y, the green ladder does the same one column right, `50K Right Return Lane` (1) "
		"and `50K Left Return Lane` (49) land beside switches 21 and 24, the three `Scan Rollover Button` "
		"auxiliary lamps land on the three rollover buttons of switch 20, and `Solenoid Expander Relay Drive` (47) "
		"matches the harness observation.",
		"- The AS-2518-52 auxiliary board is **not** the AS-2518-43 that Centaur and Kiss carry: four decoders and "
		"twenty-eight SCRs against two and twelve. Its own U1 fourth flip-flop is not driven, so only three latched "
		"address bits reach it and each decoder uses outputs 0-6 with output 7 printed `N/U`.",
		"- General illumination is not a controller output on this machine: the playfield sheet takes it from an "
		"unswitched 5.9 VAC transformer secondary, so no `pinmame.output.gi` device is declared.",
		"- Flipper coils have no driver-board output. All three coils hang on the 43 VDC bus behind relay K1, whose "
		"coil is public solenoid 19; PinMAME's synthetic 46 and 48 are what the retained script binds.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		kind = entry["group"].rsplit(".", 1)[-1]
		lines.append(f"- {kind} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Excluded object classes",
		"",
	]
	for entry in report["excluded_object_classes"]:
		lines.append(f"- {entry}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved inputs (no spatial key): {report['unresolved_inputs']}",
		f"- Unresolved outputs (no spatial key): {len(report['unresolved_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. `coverage.missing` is "
		"`[\"output_semantics\", \"spatial_placement\", \"unresolved_conflicts\"]`, and each entry names a concrete "
		"gap:",
		"",
		"- `output_semantics`: twenty-two AS-2518-52 auxiliary lamp addresses have no function on any retained "
		"source. Resolving them needs a Fathom insert-panel drawing that reaches the A9 J2/J3 pins, or a photograph "
		"of the A9 harness on real hardware.",
		"- `spatial_placement`: lamp 43 and auxiliary lamps 66, 82 and 98 have no asserted coordinate, and the "
		"twenty-two unnamed auxiliary addresses have none either.",
		"- `unresolved_conflicts`: `conflict.thumper-bumper-lamp-address-swap`.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Harness run `external:pinmame-review-artifacts/fathom-1981/harness-solenoid-self-test.json`, SHA-256 "
		f"`{HARNESS_SHA256}`, and the boot run at SHA-256 `{BOOT_HARNESS_SHA256}`.",
		f"- Normalized geometry dump `external:pinmame-review-artifacts/fathom-1981/vpx-geometry.txt`, SHA-256 "
		f"`{GEOMETRY_SHA256}`.",
		"- Rendered manual and schematic pages under `external:pinmame-manuals/rendered/bally.fathom.1981/`.",
		f"- Transcribed excerpts under `evidence/excerpts/{MACHINE_ID}/`.",
		"",
	]
	return "\n".join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_NOTE


KNOWLEDGE_NOTE = """# Fathom (Bally, 1981) - recreation knowledge

Bally game number 1233. A four-player, three-ball-multiball, six-switch-column Bally MPU
AS-2518-35 machine with seven-digit displays, a Squawk & Talk AS-2518-61A sound board, an
AS-2518-52 auxiliary lamp driver and an AS-2518-66 solenoid expander. Physical release year 1981,
taken from the machine's own manual title page (`GAME 1233`, `(c) BALLY MFG. CORP 1981`) and from
the 1981 approval dates in every schematic title block; the two `fathoma` and `fathomb` drivers are
2004 Bally/Oliver free-play and modified-rules ROMs for the same physical machine, exactly as
`centaura` and `centaurb` are for Bally Centaur, and PinMAME reuses `init_fathom` for both.

## Reading the driver declaration

`src/wpc/by35games.c` line 1264 declares
`INITGAME2(fathom, GEN_BY35, dispBy7, FLIP_SW(FLIP_L), 8, SNDBRD_BY61B, 0)`. That fifth argument, 8,
is the **auxiliary lamp-column count**, not a switch-column count: the `INITGAME2` macro expands to
`core_tGameData {gen, disp, {flip, 0, lamps, 0, sb, db, BY35GD_NOSOUNDE}}` and `core_tGameData.hw` is
declared `{flippers, swCol, lampCol, custSol, ...}`, so the macro passes a literal `0` for `swCol`
and `8` for `lampCol`. Bally Centaur and Bally Kiss declare the same `lampCol = 8`. No Bally MPU game
declares a custom switch column at all: `by35.c` reads five strobes from PIA0:A and one more from
PIA1:B, so six columns and forty-eight matrix positions is the platform ceiling, and how many of them
a game wires is a property of its own harness rather than of its driver declaration.

`dispBy7` gives four seven-digit player score displays plus a two-digit credit display and a
two-digit Match / Ball in Play display. `BY35GD_NOSOUNDE` is set, and `BY35GD_SWVECTOR` is not, which
is what puts the sixth switch strobe on PIA1:B bit 7 rather than bit 4.

## What is unusual about this machine

**Nineteen printed momentary solenoid functions on fourteen driver outputs.** The Bally MPU
publishes fifteen momentary addresses, and Fathom needs more, because each of its two three-target
in-line drop banks has an individual coil per target position as well as a bank reset coil. The
Solenoid Expander (A15, AS-2518-66) closes the gap. A lamp-driver SCR output - public lamp address
47, printed `TO AUX. EXPANDOR J1-2` on the A5 sheet and `SCR ANODE LAMP DRIVER` on the expander's
own connector - drives a MOC3011 optocoupler which energizes a 48 V relay K1, and the relay's
contacts switch the 43 VDC solenoid bus between two groups of coils. Five driver outputs therefore
each reach one of two coils:

| public solenoid | relay de-energized | relay energized |
| --- | --- | --- |
| 1 | 3 Top Drop Target Reset (blue in-line bank) | 1st Green Inline Drop Target |
| 2 | 6 Drop Target Reset (left six-bank) | 2nd Green Inline Drop Target |
| 3 | 3 Middle Drop Target Reset | 3rd Green Inline Drop Target |
| 13 | Top Saucer Kicker | 1st Blue Inline Drop Target |
| 14 | Right Saucer Kicker | 2nd Blue Inline Drop Target |

Public 4 (Right Inline Drop Target Reset) and public 15 (3rd Blue Inline Drop Target) are not
shared. A table author has to model this: firing address 13 does one of two completely different
things depending on the state of lamp 47.

**The sixth switch-column strobe is public solenoid 20.** Fathom wires forty-eight switches, which
is six columns of eight, but the MPU's PIA0:A supplies only five strobes. The playfield wiring
diagram takes `ST 5` from `A4J4-8`, and that is the PIA1:B PB7 line that PinMAME publishes as
continuous solenoid 20. The A3 sheet's own Q18 driver output for that line reaches nothing but pins
printed `N/U`. So address 20 is permanently asserted in play and is not a coil. This differs from
both earlier BY35 machines in this project: Bally Centaur spends public 17 on its sixth strobe, and
Bally Kiss, a five-column game, spends 17 on a real coil.

**The flipper coils have no address of their own.** All three coils - lower left, lower right and
an upper right flipper wired in parallel with the lower right - hang on the 43 VDC bus behind the
contacts of relay K1, whose coil is public solenoid 19. Only the right flipper button is in the
switch matrix, at address 7; the left button is direct-wired into the relay circuit and the ROM
cannot read it. PinMAME's public 46 and 48 are synthetic ball-physics outputs.

## Mechanisms a table author has to build

- **Outhole and three-station trough.** Fathom is a multiball game, so the outhole carries three
  matrix stations: `Outhole` (1), `#1 Left of Outhole` (2) and `#2 Left and #1 Right of Outhole`
  (3). The third printed name records that one contact serves two ball positions. Public solenoid 7
  kicks a ball to the shooter lane.
- **Left six-bank drop targets**, printed A (top) to F (bottom), switches 32 down to 27, raised by
  public solenoid 2. A rebound rubber behind the bank scores on switch 19, which is shared with the
  10-point rubber elsewhere on the playfield.
- **Middle three-bank drop targets**, switches 35, 34, 33 for #1, #2, #3, raised by public
  solenoid 3. Knocking them down in order lights the extra-ball target.
- **Two in-line drop target banks.** The blue bank (printed `3 Top`) lies across the top of the
  playfield: switches 44, 43, 42 for the 1st, 2nd, 3rd target, running left to right, reset by
  public solenoid 1, with individual drop coils at public 13, 14, 15. The green bank (printed
  `Right Inline`) runs up the right side: switches 48, 47, 46 for the 1st, 2nd, 3rd target, nearest
  the player first, reset by public solenoid 4, with individual drop coils at public 1, 2, 3. Only
  the front target of an in-line bank can be hit, so the ROM knocks each target down with its own
  coil to advance the sequence. Option switch S22 decides whether targets left down carry over.
- **Two saucers**, top and right, with a rollover button in each feeding lane (switches 25 and 26)
  separate from the saucer switch itself (4 and 5). Option switch S6 decides whether a ball left in
  a saucer is kicked out at end of game.
- **Three CPU-driven thumper bumpers** and **two slingshots**, all on ordinary switch-then-coil
  pairs.
- **Two captive balls**, Lagoon and Cave, each with its own release insert (public lamps 40 and 56)
  that lights when the ball may be freed. Nothing releases them electrically; the player does it by
  hitting the captive ball. That, and the three-station trough, is where the multiball comes from.
- **A spinner** on the left side (switch 18) with its own insert at public lamp 60.

## Lamp inventory

The AS-2518-23 lamp driver has four MC14514CP decoders, one per lamp data line, each using outputs
0 to 14 and leaving output 15 unconnected - which is exactly the selector value PinMAME's
`by35_lampStrobe` skips. So public lamp address = `16 * data_line + decoder_output + 1`, giving
four runs of fifteen: 1-15, 17-31, 33-47 and 49-63, with 16, 32, 48 and 64 unreachable decoder
slots rather than unused lamps.

The address-to-connector-pin part of that chain is a property of the board and is identical on
Centaur, Kiss and Fathom, including the eight outputs (11, 12, 27, 28, 43, 44, 59, 60) that branch
to a second connector pin. On Fathom every one of those second pins is printed `N/U`, which is a
useful self-check: Fathom's own A5 sheet draws arrows into exactly eight `N/U` pins, and they are
exactly those eight.

Public lamp 47 is not a lamp at all - it is the Solenoid Expander relay's control input. The other
fifty-nine main-board addresses are real: two ten-step bonus ladders (blue and green, 1K to 10K
plus 50K and 55K) with 3X to 5X multipliers, the A/B/C lanes, both out and return lane specials, the
three thumper bumper lamps, the spinner, the two captive-ball release inserts, `A-B-C Special`,
`In Sequence`, `Double`/`Triple Playfield Scores`, both saucer arrows, `Extra Ball`, `Bonus
Special`, `Same Player Shoot Again` and the credit indicator, plus the six fixed Bally back box
status lamps at the platform's usual addresses (11 Shoot Again, 13 Ball In Play, 27 Match, 29 High
Score To Date, 45 Game Over, 61 Tilt).

The auxiliary AS-2518-52 board is where the record is incomplete. It is **not** the AS-2518-43 that
Centaur and Kiss carry: four MC14028B decoders and twenty-eight SCRs against two and twelve, so no
derivation transfers. Its own U1 fourth flip-flop is not driven from J1, so only three latched
address bits reach it, each decoder uses outputs 0 to 6, and output 7 is printed `N/U` on all four.
Public auxiliary address = `64 + 16 * data_line + decoder_output + 1`, giving 65-71, 81-87, 97-103
and 113-119. Fathom's A9 sheet annotates only seven of the twenty-eight outputs with a function, and
those seven are a seven-step chase: `#1`, `#2`, `#3 Scan Rollover Button` at 65, 81, 97, and `#4`
through `#7 Back Scan` at 113, 66, 82, 98, with #5, #6 and #7 also scanning the three left lanes.
The three `Scan Rollover Button` lamps land exactly on the three rollover buttons of switch 20 in
the retained table, which independently confirms the arithmetic. The other twenty-one outputs are
fitted SCRs whose connector destinations the sheet leaves unlabelled; five of them (67, 83, 99, 114,
115) are proven driven by the ROM in the retained harness run and are enumerated as used with an
unresolved function, and sixteen more are enumerated with an unknown disposition rather than
declared unused, because failing to observe an address is not proof it is unused.

## General illumination

Fathom has no general-illumination controller channel. The playfield wiring diagram feeds the
general illumination from an unswitched 5.9 VAC transformer secondary at `A2J1-1/3/4/6`, with a
separate `FEATURE LAMP BUS` at `A2J1-5`. `coreGlobals.gi[]` is WPC, Whitestar and SAM only, so
there is nothing for a consumer to bind.

## Retained table caveats

The retained known-working table is a competent recreation but three of its bindings are wrong on
this platform and must not be copied:

1. Its `SolCallback(25)`, `(26)`, `(27)`, `(37)` and `(38)` assignments for five of the six
   individual in-line drop-target coils are dead code. Pinned `core_getSol`'s `solNo <= 28` branch
   reads `coreGlobals.solenoids`, where a Bally MPU driver only ever sets bits 0-14 and 16-19, and
   its 37-44 branch serves only WPC-95 and System 11. Those five callbacks can never fire. The real
   addresses are public 1, 2, 3 (green) and 13, 14 (blue); only its `SolCallback(15)` for the 3rd
   blue target is right.
2. It binds public lamps 12 and 28 to the bottom and right thumper bumpers respectively, which is
   the opposite of the printed wiring. See
   `conflict.thumper-bumper-lamp-address-swap`; the definition follows the manual.
3. It drives an apron light object at public lamp 11, where the printed wiring puts the back box
   `Shoot Again` socket; the playfield `Same Player Shoot Again` insert is public lamp 43.

Its `Const cGameName="Fathom"` line uses a capital F, which is not a PinMAME driver short name;
VPinMAME resolves the name case-insensitively, so it does bind the production `fathom` parent.
"""


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), build_knowledge())
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		raise RuntimeError(f"stale author-ready artifact for a partial record: {stale}")
	if not definition_path.is_file():
		raise RuntimeError(f"Fathom definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Fathom seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Fathom definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Fathom seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Fathom spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Fathom spatial review drifted from its deterministic curator: {markdown_path}")
	if not knowledge_path.is_file() or knowledge_path.read_text(encoding="utf-8") != build_knowledge():
		raise RuntimeError(f"Fathom knowledge note drifted from its deterministic curator: {knowledge_path}")
	print("Fathom definition, seed, spatial audit, and knowledge note match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, spatial report, and knowledge note")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Fathom extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Fathom retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
