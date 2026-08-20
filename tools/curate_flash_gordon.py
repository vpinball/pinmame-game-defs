#!/usr/bin/env python3
"""Curate the physical Bally Flash Gordon (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail, and retained
table coordinate is embedded as a literal, so regeneration reproduces the canonical definition, its
pinned seed, and the spatial report byte-for-byte without reading the external evidence roots.
``--check`` refuses drift and ``--regenerate`` is the only path that writes.

Raw retained-table coordinates are stored rather than pre-normalized ones, and the normalization is
done here, so a reviewer can check a placement against
``external:pinmame-review-artifacts/flash-gordon-1980/vpx-geometry.txt`` by eye instead of trusting
arithmetic that was done once by hand.

Evidence authority follows the runbook: the retained known-working VPX script owns runtime address
semantics, the Bally game #1215 manual owns physical construction, wiring, quantity and device
presence, and pinned PinMAME owns controller topology. Where they disagree the disagreement is a
first-class ``conflicts`` entry rather than a silent choice.
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
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/flash-gordon-1980.json"
PARTIAL_PATH = ROOT / "machines/partial/bally/flash-gordon-1980.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/flash-gordon-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/flash-gordon-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/flash-gordon-1980.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/flash-gordon-1980.md"

MACHINE_ID = "bally.flash-gordon.1980"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-by35"
MANUAL_SOURCE = "manual.bally.flash-gordon.1980"
TABLE_SOURCE = "vpx-table.flash-gordon-2-0"
SCRIPT_SOURCE = "vpx-script.flash-gordon-2-0"
EXTRACTION_SOURCE = "vpx-extraction.flash-gordon-2-0"
CORPUS_SCRIPT_SOURCE = "vpx-script.flash-gordon-vpw-3-1-3"

MANUAL_SHA256 = "179536aa00448188602ce0ac7e7d5c729b8649f8638358b4b4c9a065c2adb63a"
TABLE_SHA256 = "b2c5ea9eac7e4b7b6cf8f81809482b3d31ee9f1cb23a8242df0e7c2bf2790b0e"
SCRIPT_SHA256 = "e440f644ee509f392aa2340f652918144728bd8fe6f306eec7b5ed6441d10c2c"
CORPUS_SCRIPT_SHA256 = "fe7d56aa0c8336f16181fdaf8a2ca51aa9da4f0d7956af288e42145565d16275"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

EXTRACTION_RELATIVE_PATH = Path("bally/flash-gordon-1980/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/flash-gordon-1980/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "50810dd697738d98061624512a948cec08ca6eaad037d5dd61d3a7d9935fc775"
EXTRACTION_FILE_COUNT = 1447
EXTRACTION_TOTAL_BYTES = 168438120

# The retained table's own playfield bounds. Flash Gordon is an early-1980s cabinet and its
# playfield is markedly shorter than the WPC machines curated elsewhere in this project, so the y
# divisor is 1976.471 rather than 2162; using a WPC divisor here would compress every y by 9%.
TABLE_WIDTH = 952.9412
TABLE_HEIGHT = 1976.471
TABLE_BOUNDS = "left=0 top=0 right=952.9412 bottom=1976.471"

DRIVER_IDS = (
	"flashgdn",
	"flashgda",
	"flashgdf",
	"flashgdp",
	"flashgdv",
	"flashgfa",
	"flashgp2",
	"flashgva",
	"flashgvf",
	"flashgvffp",
)

DRIVERS = {
	"flashgdn": ("Flash Gordon", "1981", "Bally", None, "identical",
		"The production ROM and the reference for this definition: Squawk & Talk -61 sound board "
		"(SNDBRD_BY61), GEN_BY35, dispBy7 seven-digit displays, FLIP_SW(FLIP_L), lampCol 8. It is "
		"the driver the retained known-working table binds (cGameName = \"flashgdn\")."),
	"flashgda": ("Flash Gordon (Free Play)", "2004", "Bally / Oliver", "flashgdn", "identical",
		"Bally/Oliver free-play conversion of the production ROM; U6 is the generic 7526fn free-play "
		"ROM and the game ROM is unchanged, so the I/O inventory is identical."),
	"flashgdf": ("Flash Gordon (French)", "1981", "Bally", "flashgdn", "identical",
		"French speech ROMs on the same Squawk & Talk board; identical playfield hardware."),
	"flashgdp": ("Flash Gordon (Prototype rev. 1)", "1981", "Bally", "flashgdn", "compatible",
		"Prototype game ROM for the same physical machine. It runs on the production board set and "
		"the same switch, lamp and solenoid inventory; rules differ."),
	"flashgdv": ("Flash Gordon (Vocalizer Sound)", "1981", "Bally", "flashgdn", "identical",
		"Same physical machine fitted with the Vocalizer -56/-57 sound boards (SNDBRD_BY56) instead "
		"of Squawk & Talk -61. Sound hardware only: the switch matrix, lamp matrix and solenoid "
		"complement are unchanged, and PinMAME gives it the same lampCol 8 and dispBy7."),
	"flashgfa": ("Flash Gordon (French Free Play)", "2004", "Bally / Oliver", "flashgdn", "identical",
		"Bally/Oliver free-play conversion of the French Squawk & Talk build."),
	"flashgp2": ("Flash Gordon (Prototype rev. 2)", "1981", "Bally", "flashgdn", "compatible",
		"Second prototype game ROM; see flashgdp."),
	"flashgva": ("Flash Gordon (Vocalizer Sound Free Play)", "2004", "Bally / Oliver", "flashgdn", "identical",
		"Bally/Oliver free-play conversion of the Vocalizer build."),
	"flashgvf": ("Flash Gordon (French Vocalizer Sound)", "1981", "Bally", "flashgdn", "identical",
		"French speech ROMs on the Vocalizer sound boards."),
	"flashgvffp": ("Flash Gordon (French Vocalizer Sound Free Play)", "2004", "Bally / Oliver", "flashgdn", "identical",
		"Bally/Oliver free-play conversion of the French Vocalizer build."),
}

# --- Switches -------------------------------------------------------------------------------
#
# Public address = (column - 1) * 8 + row + 1 on the five-column Playfield A6 matrix, which is the
# same number the printed Switch Assembly Self-Test table uses. Unlike the solenoid table, where the
# printed number is a test order, the switch numbers really are the matrix positions: the retained
# script's own Controller.Switch / vpmTimer.PulseSw calls agree with the printed table on every one
# of the thirty-four addresses it drives.
#
# Fields: id, label, switch_type, quantity, availability, spatial (raw table coordinates or a
# not-applicable reason), notes.
SWITCHES: dict[int, dict[str, Any]] = {
	1: {
		"id": "switch.left-and-right-rollover-buttons",
		"label": "2 Left & Right Rollover Buttons",
		"switch_type": "button",
		"quantity": 4,
		"positions": [(743.820, 410.032), (732.622, 301.927), (241.721, 53.848), (76.838, 122.656)],
		"notes": "Four rollover buttons wired in parallel onto one matrix position, two at the top "
			"left and two on the right-hand arc, which is how the printed description reads \"2 left "
			"and right\". The retained script models all four (sw1a through sw1d) and pulses this one "
			"address from each. Two of the four have their own lamp - public 47 lights the lower "
			"right one and public 65 the upper right one - and the left pair's lamp is the subject of "
			"conflict.aux-lamp-100-left-rollover-fitment.",
	},
	2: {
		"id": "switch.shooter-lane-rollover-buttons",
		"label": "3 Shooter Lane Rollover Buttons",
		"switch_type": "button",
		"quantity": 3,
		"positions": [(872.066, 299.635), (794.477, 175.920), (673.114, 89.235)],
		"notes": "Three rollover buttons in the shooter-alley return arc, wired in parallel onto one "
			"matrix position; the retained script models them as sw2a, sw2b and sw2c. Each has its own "
			"auxiliary-board lamp: public 113 lower, 97 middle, 81 top.",
	},
	3: {
		"id": "switch.top-single-drop-target",
		"label": "Top Single Drop Target",
		"switch_type": "leaf",
		"positions": [(665.223, 208.175)],
		"notes": "The single drop target at the top right of the playfield. It is the only target on "
			"the machine the ROM can pull down on command as well as reset; see mech.single-drop-target.",
	},
	4: {
		"id": "switch.shooter-lane-rollover",
		"label": "Shooter Lane Rollover",
		"switch_type": "leaf",
		"positions": [(899.981, 1524.581)],
		"notes": "Rollover in the shooter lane itself, below the three shooter-alley rollover buttons.",
	},
	5: {
		"id": "switch.drop-target-50-point-rebound",
		"label": "Drop Target 50 Point Rebound (2)",
		"switch_type": "leaf",
		"quantity": 2,
		"positions": None,
		"notes": "Two rebound rubbers beside the four-bank drop target, wired in parallel onto one "
			"matrix position; the printed \"(2)\" is the contact count. The retained table implements "
			"them as a single collidable Primitive named phys_sw5 whose own origin, size and "
			"rot_and_tra are all zero, so the extraction carries no usable coordinate for it and the "
			"spatial key is omitted rather than invented.",
	},
	6: {
		"id": "switch.credit-button",
		"label": "Credit Button",
		"switch_type": "button",
		"spatial_reason": "cabinet_or_service",
		"notes": "Coin door. Figure V's legend lists switch 06 under DOOR. The retained script leaves "
			"it to VPinMAME's own keyboard handling.",
	},
	7: {
		"id": "switch.tilt",
		"label": "Tilt (3)",
		"switch_type": "tilt",
		"quantity": 3,
		"spatial_reason": "cabinet_or_service",
		"notes": "Three tilt contacts in parallel - plumb bob, ball roll and cabinet slam-adjacent - "
			"on one matrix position; Figure V lists switch 07 under CABINET. The retained script sets "
			"vpmNudge.TiltSwitch = 7.",
	},
	8: {
		"id": "switch.outhole",
		"label": "Outhole",
		"switch_type": "leaf",
		"positions": [(436.123, 1882.417)],
		"initial_active": True,
		"notes": "The single-ball outhole. The retained script asserts this address at table init and "
			"whenever a ball rests in the drain, and the outhole kicker at public 7 clears it.",
	},
	9: {
		"id": "switch.coin-chute-3-right",
		"label": "Coin III (Right)",
		"switch_type": "leaf",
		"spatial_reason": "cabinet_or_service",
		"notes": "Coin door. Its credit ratio is set by option switches S9-S13.",
	},
	10: {
		"id": "switch.coin-chute-1-left",
		"label": "Coin I (Left)",
		"switch_type": "leaf",
		"spatial_reason": "cabinet_or_service",
		"notes": "Coin door, the hinge-side chute. Its credit ratio is set by option switches S1-S5.",
	},
	11: {
		"id": "switch.coin-chute-2-middle",
		"label": "Coin II (Middle)",
		"switch_type": "leaf",
		"spatial_reason": "cabinet_or_service",
		"notes": "Coin door, the centre chute. Its credit ratio is set by option switches S17-S20, "
			"which can also be set to follow chute #1.",
	},
	12: {
		"id": "switch.right-side-lower-target",
		"label": "Right Side Lower Target",
		"switch_type": "leaf",
		"positions": [(777.785, 1123.392)],
		"notes": "Lower of the two standup targets on the right rail of the lower playfield, lit by "
			"public lamp 10. The label and the placement carry conflict."
			"right-side-target-upper-lower-transposition: the printed Switch Assembly Self-Test table "
			"and Figure V both make this address the lower target, while the Playfield A6 schematic "
			"sheet labels the same matrix position RIGHT SIDE UPPER TARGET and the retained table "
			"names its upper object sw12. The two-source majority is used for the label and the "
			"placement, so this address is deliberately placed on the object the retained table calls "
			"sw15.",
	},
	13: {
		"id": "switch.flipper-feed-lane-right",
		"label": "Flipper Feed Lane (Right)",
		"switch_type": "leaf",
		"positions": [(747.146, 1395.548)],
		"notes": "Right inlane, lit by public lamp 26.",
	},
	14: {
		"id": "switch.flipper-feed-lane-left",
		"label": "Flipper Feed Lane (Left)",
		"switch_type": "leaf",
		"positions": [(112.556, 1392.854)],
		"notes": "Left inlane, lit by public lamp 42.",
	},
	15: {
		"id": "switch.right-side-upper-target",
		"label": "Right Side Upper Target",
		"switch_type": "leaf",
		"positions": [(778.478, 1071.108)],
		"notes": "Upper of the two standup targets on the right rail of the lower playfield, lit by "
			"public lamp 58. See conflict.right-side-target-upper-lower-transposition; this address is "
			"deliberately placed on the object the retained table calls sw12.",
	},
	16: {
		"id": "switch.slam",
		"label": "Slam (2)",
		"switch_type": "leaf",
		"quantity": 2,
		"spatial_reason": "cabinet_or_service",
		"notes": "Two slam contacts on one matrix position. Figure V lists switch 16 under both "
			"CABINET and DOOR, which is why the printed description carries \"(2)\".",
	},
	17: {
		"id": "switch.four-drop-target-a-bottom",
		"label": "4 Drop Target \"A\" (Bottom)",
		"switch_type": "leaf",
		"positions": [(80.665, 1068.706)],
		"notes": "Bottom target of the left four-bank, lit by public lamp 9.",
	},
	18: {
		"id": "switch.four-drop-target-b",
		"label": "4 Drop Target \"B\"",
		"switch_type": "leaf",
		"positions": [(94.903, 1015.392)],
		"notes": "Second target of the left four-bank, lit by public lamp 25.",
	},
	19: {
		"id": "switch.four-drop-target-c",
		"label": "4 Drop Target \"C\"",
		"switch_type": "leaf",
		"positions": [(109.482, 961.962)],
		"notes": "Third target of the left four-bank, lit by public lamp 41.",
	},
	20: {
		"id": "switch.four-drop-target-d-top",
		"label": "4 Drop Target \"D\" (Top)",
		"switch_type": "leaf",
		"positions": [(123.871, 908.019)],
		"notes": "Top target of the left four-bank, lit by public lamp 57.",
	},
	21: {
		"id": "switch.three-drop-target-top",
		"label": "3 Drop Target (Top)",
		"switch_type": "leaf",
		"positions": [(277.469, 165.277)],
		"notes": "Top target of the upper-left three-bank, whose three arrow lamps are public 8, 24 "
			"and 40.",
	},
	22: {
		"id": "switch.three-drop-target-middle",
		"label": "3 Drop Target (Middle)",
		"switch_type": "leaf",
		"positions": [(262.093, 218.469)],
		"notes": "Middle target of the upper-left three-bank.",
	},
	23: {
		"id": "switch.three-drop-target-bottom",
		"label": "3 Drop Target (Bottom)",
		"switch_type": "leaf",
		"positions": [(246.088, 271.764)],
		"notes": "Bottom target of the upper-left three-bank.",
	},
	24: {
		"id": "switch.top-target",
		"label": "Top Target",
		"switch_type": "leaf",
		"positions": [(373.004, 59.870)],
		"notes": "Standup target across the top of the playfield, lit by public 62 (collect bonus) and "
			"public 63 (special).",
	},
	25: {
		"id": "switch.first-in-line-drop-target",
		"label": "1st In Line Drop Target",
		"switch_type": "leaf",
		"positions": [(764.696, 887.802)],
		"notes": "Nearest target of the right in-line bank, the one the ball reaches first.",
	},
	26: {
		"id": "switch.second-in-line-drop-target",
		"label": "2nd In Line Drop Target",
		"switch_type": "leaf",
		"positions": [(774.801, 816.731)],
		"notes": "Middle target of the right in-line bank.",
	},
	27: {
		"id": "switch.third-in-line-drop-target",
		"label": "3rd In Line Drop Target",
		"switch_type": "leaf",
		"positions": [(787.428, 747.959)],
		"notes": "Far target of the right in-line bank.",
	},
	28: {
		"id": "switch.in-line-back-target",
		"label": "In Line Back Target",
		"switch_type": "leaf",
		"positions": [(806.212, 638.419)],
		"notes": "Standup target behind the in-line drop bank, reachable only once the three drop "
			"targets in front of it are down. The retained table models it as an ordinary standup "
			"(STHit 28) and not as a fourth drop target.",
	},
	29: {
		"id": "switch.ten-point-rebound",
		"label": "10 Point Rebound (2)",
		"switch_type": "leaf",
		"quantity": 2,
		"positions": None,
		"notes": "Two rebound rubbers wired in parallel onto one matrix position. Like switch 5 the "
			"retained table implements them as one collidable Primitive (phys_sw29) sitting at a local "
			"origin with no usable coordinate, so the spatial key is omitted.",
	},
	30: {
		"id": "switch.saucer",
		"label": "Saucer",
		"switch_type": "leaf",
		"positions": [(431.987, 610.843)],
		"notes": "The centre saucer's ball-present switch. It gates both saucer coils in the retained "
			"script, which reads it before firing either kicker.",
	},
	31: {
		"id": "switch.right-outlane",
		"label": "Right Outlane",
		"switch_type": "leaf",
		"positions": [(811.936, 1454.412)],
		"notes": "Right outlane, lit by public lamp 15 (Rt. Out Special).",
	},
	32: {
		"id": "switch.left-outlane",
		"label": "Left Outlane",
		"switch_type": "leaf",
		"positions": [(49.586, 1453.559)],
		"notes": "Left outlane, lit by public lamp 31 (Lft. Out Special).",
	},
	33: {
		"id": "switch.right-spinner",
		"label": "Right Spinner",
		"switch_type": "leaf",
		"positions": [(628.547, 874.774)],
		"notes": "Right rollunder spinner, lit by public lamp 35.",
	},
	34: {
		"id": "switch.left-spinner",
		"label": "Left Spinner",
		"switch_type": "leaf",
		"positions": [(162.507, 691.161)],
		"notes": "Left rollunder spinner, lit by public lamp 51.",
	},
	35: {
		"id": "switch.right-slingshot",
		"label": "Right Slingshot",
		"switch_type": "leaf",
		"positions": [(649.282, 1390.045)],
		"notes": "Right slingshot blade. The printed switch table's own footnote says the slingshot "
			"coil energizes when the switch is made, so the pairing is hardware and not ROM logic.",
	},
	36: {
		"id": "switch.left-slingshot",
		"label": "Left Slingshot",
		"switch_type": "leaf",
		"positions": [(210.836, 1391.856)],
		"notes": "Left slingshot blade; see switch 35 for the hardware pairing.",
	},
	37: {
		"id": "switch.top-thumper-bumper",
		"label": "Top Thumper Bumper",
		"switch_type": "leaf",
		"positions": [(491.210, 97.733)],
		"notes": "Skirt switch of the thumper bumper at the very top of the playfield, lit by public "
			"lamp 14. Its coil energizes directly from this switch.",
	},
	38: {
		"id": "switch.unused-matrix-position-38",
		"label": "Unused switch matrix position 38",
		"availability": "unused",
		"spatial_reason": "unused",
		"notes": "The only one of the forty matrix positions printed with no description at all in the "
			"Switch Assembly Self-Test table, and the only one the Playfield A6 sheet draws with no "
			"label. The retained script never references it.",
	},
	39: {
		"id": "switch.right-thumper-bumper",
		"label": "Right Thumper Bumper",
		"switch_type": "leaf",
		"positions": [(514.220, 786.559)],
		"notes": "Skirt switch of the right thumper bumper in the middle of the playfield. Its coil "
			"energizes directly from this switch.",
	},
	40: {
		"id": "switch.left-thumper-bumper",
		"label": "Left Thumper Bumper",
		"switch_type": "leaf",
		"positions": [(322.502, 850.330)],
		"notes": "Skirt switch of the left thumper bumper in the middle of the playfield. Its coil "
			"energizes directly from this switch.",
	},
}

# --- Solenoids ------------------------------------------------------------------------------
#
# Public momentary address = PIA1:B selector + 1, so 1-15 with no 16 because selector 15 is the idle
# state; PIA1:B bits 4-7 are the four continuous outputs at 17-20. The printed Self Test # is a test
# order, never an address. The mapping below is the retained known-working script's own printed
# cross-reference ("'1 = 6 - 4 Drop Target Reset" and so on), which the pinned corpus script repeats
# verbatim, corroborated on the two continuous outputs by src/lisy/lisy35.c naming continuous bit 1
# the coin lockout and bit 2 the flipper-enable relay - public 18 and 19 - and on the two
# lowest-numbered momentary coils by Bally Kiss and Bally Centaur, which also put the knocker on
# public 6 and the outhole kicker on public 7.
SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {
		"id": "device.four-drop-target-reset",
		"label": "4 Drop Target Reset",
		"kind": "coil",
		"self_test": "06",
		"part_number": "NO-26-1900",
		"positions": [(102.230, 988.520)],
		"projection": "Projected onto the left four-bank drop target assembly it resets (the mean of "
			"the retained table's own four target objects sw17-sw20). The reset coil is mounted under "
			"the bank and has no object of its own in the extraction.",
		"notes": "One of the three NO-26-1900 Drop Target Reset coils in the parts list. It resets all "
			"four targets of the left bank together; there are no individual down coils.",
	},
	2: {
		"id": "device.three-drop-target-reset",
		"label": "3 Drop Target Reset",
		"kind": "coil",
		"self_test": "07",
		"part_number": "NO-26-1900",
		"positions": [(261.883, 218.503)],
		"projection": "Projected onto the upper-left three-bank drop target assembly it resets (the "
			"mean of the retained table's own target objects sw21-sw23).",
		"notes": "Second of the three NO-26-1900 reset coils; resets the upper-left three-bank.",
	},
	3: {
		"id": "device.in-line-drop-target-reset",
		"label": "In Line Drop Target Reset",
		"kind": "coil",
		"self_test": "08",
		"part_number": "NO-26-1900",
		"positions": [(775.642, 817.497)],
		"projection": "Projected onto the right in-line drop target assembly it resets (the mean of "
			"the retained table's own target objects sw25-sw27).",
		"notes": "Third of the three NO-26-1900 reset coils; resets the right in-line bank. The A3J2-10 "
			"connector pin is printed IN-LINE DROP TAR. RESET.",
	},
	4: {
		"id": "device.saucer-kick-down",
		"label": "Saucer Kick Down",
		"kind": "coil",
		"self_test": "03",
		"part_number": "AO-29-2100",
		"positions": [(431.987, 610.843)],
		"notes": "One of the centre saucer's two kicker coils, the one that throws the ball back down "
			"the playfield. Wired to A3J2-11.",
	},
	5: {
		"id": "device.unused-solenoid-output-5",
		"label": "Unused solenoid output 5",
		"kind": "coil",
		"availability": "unused",
		"spatial_reason": "unused",
		"notes": "The printed Solenoid Identification Table lists sixteen entries and the retained "
			"script's cross-reference accounts for all fourteen momentary ones plus the two continuous "
			"ones, leaving this momentary address with no device. The A3 connector sheet likewise "
			"names fourteen coil destinations and no fifteenth.",
	},
	6: {
		"id": "device.knocker",
		"label": "Knocker",
		"kind": "coil",
		"self_test": "02",
		"part_number": "AR-26-1200",
		"spatial_reason": "cabinet_or_service",
		"notes": "Cabinet-mounted knocker, wired to A3J2-5. Figure V lists solenoid 02 under CABINET, "
			"so it has no playfield coordinate. Public 6 is the knocker on Bally Kiss and Bally Centaur "
			"as well.",
	},
	7: {
		"id": "device.outhole-kicker",
		"label": "Outhole Kicker",
		"kind": "coil",
		"self_test": "01",
		"part_number": "AN-26-1200",
		"positions": [(436.123, 1882.417)],
		"notes": "Single-ball outhole kicker, wired to A3J1-5, drawn on Figure V as square 01 beside "
			"switch circle 08. Public 7 is the outhole kicker on Bally Kiss and Bally Centaur as well.",
	},
	8: {
		"id": "device.saucer-kick-up",
		"label": "Saucer Kick Up",
		"kind": "coil",
		"self_test": "04",
		"part_number": "AO-27-1300",
		"positions": [(431.987, 610.843)],
		"notes": "The centre saucer's other kicker coil, the one that throws the ball up the playfield. "
			"Wired to A3J5-10. Co-located with public 4 because they are the two coils of one assembly.",
	},
	9: {
		"id": "device.single-drop-target-reset",
		"label": "Single Drop Target Reset",
		"kind": "coil",
		"self_test": "05",
		"part_number": "AO-27-1300",
		"positions": [(665.223, 208.175)],
		"notes": "Raises the single top drop target. Wired to A3J5-12.",
	},
	10: {
		"id": "device.left-thumper-bumper",
		"label": "Left Thumper Bumper",
		"kind": "coil",
		"self_test": "09",
		"part_number": "AN-26-1200",
		"positions": [(322.502, 850.330)],
		"notes": "Wired to A3J5-11. Energized directly by switch 40 as well as by the ROM.",
	},
	11: {
		"id": "device.right-thumper-bumper",
		"label": "Right Thumper Bumper",
		"kind": "coil",
		"self_test": "10",
		"part_number": "AN-26-1200",
		"positions": [(514.220, 786.559)],
		"notes": "Wired to A3J5-9. Energized directly by switch 39 as well as by the ROM.",
	},
	12: {
		"id": "device.single-drop-target-pull-down",
		"label": "Single Drop Target Pull Down",
		"kind": "coil",
		"self_test": "11",
		"part_number": "CE-31-2000",
		"positions": [(665.223, 208.175)],
		"notes": "Pulls the single top drop target down on ROM command, which no other target on the "
			"machine can do. Wired to A3J5-15 and co-located with its reset coil at public 9.",
	},
	13: {
		"id": "device.top-thumper-bumper",
		"label": "Top Thumper Bumper",
		"kind": "coil",
		"self_test": "12",
		"part_number": "AN-26-1200",
		"positions": [(491.210, 97.733)],
		"notes": "Wired to A3J5-13. Energized directly by switch 37 as well as by the ROM.",
	},
	14: {
		"id": "device.left-slingshot",
		"label": "Left Slingshot",
		"kind": "coil",
		"self_test": "13",
		"part_number": "AN-26-1200",
		"positions": [(210.836, 1391.856)],
		"notes": "Wired to A3J5-14. Energized directly by switch 36 as well as by the ROM.",
	},
	15: {
		"id": "device.right-slingshot",
		"label": "Right Slingshot",
		"kind": "coil",
		"self_test": "14",
		"part_number": "AN-26-1200",
		"positions": [(649.282, 1390.045)],
		"notes": "Wired to A3J5-8. Energized directly by switch 35 as well as by the ROM.",
	},
	17: {
		"id": "device.unused-continuous-output-17",
		"label": "Unused continuous output 17",
		"kind": "coil",
		"availability": "unused",
		"spatial_reason": "unused",
		"notes": "The first of the four continuous outputs. Flash Gordon wires five switch columns, so "
			"unlike a six-column BY35 game it needs no continuous output to carry a sixth column "
			"strobe, and the printed tables account for only two continuous devices - the coin lockout "
			"and the K1 relay.",
	},
	18: {
		"id": "device.coin-lockout",
		"label": "Coin Lockout Door",
		"kind": "coil",
		"self_test": "15",
		"part_number": "FO-36-7000",
		"spatial_reason": "cabinet_or_service",
		"notes": "Coin door lockout coil, wired to A3J2-8. Figure V lists solenoid 15 under DOOR. "
			"src/lisy/lisy35.c independently identifies continuous bit 1 - public 18 - as the coin "
			"lockout on this platform.",
	},
	19: {
		"id": "device.k1-flipper-enable-relay",
		"label": "K1 Relay (Flipper Enable)",
		"kind": "relay",
		"self_test": "16",
		"spatial_reason": "cabinet_or_service",
		"notes": "The flipper-enable relay, which switches the 43 VDC feed to all three flipper coils. "
			"Figure V lists solenoid 16 under BACKBOX. src/lisy/lisy35.c independently identifies "
			"continuous bit 2 - public 19 - as the flipper relay. The flipper coils themselves have no "
			"driver-board output and therefore no public address of their own.",
	},
	20: {
		"id": "device.unused-continuous-output-20",
		"label": "Unused continuous output 20",
		"kind": "coil",
		"availability": "unused",
		"spatial_reason": "unused",
		"notes": "The fourth continuous output. On a six-column BY35 game without BY35GD_SWVECTOR this "
			"bit carries the sixth switch-column strobe; Flash Gordon has five columns, so it carries "
			"nothing.",
	},
}

# --- Lamps ----------------------------------------------------------------------------------
#
# public = 16 * d + lampadr + 1 (+64 on the auxiliary board), where d is the lamp data line PD0-PD3
# and lampadr the latched address; by35_lampStrobe skips lampadr 15, which is why 16, 32, 48, 64, 80,
# 96, 112 and 128 are unreachable decoder slots rather than unused lamps. The AS-2518-23 main board
# gives sixty outputs at 1-15, 17-31, 33-47 and 49-63; the AS-2518-52 auxiliary board decodes only
# seven outputs per data line, so it reaches 65-71, 81-87, 97-103 and 113-119 and no further.
#
# Function names come from this game's own A5 and A9 connector sheets. Coordinates come from the
# retained table's Light objects, whose addresses are set by the script's own Lampz.MassAssign calls
# rather than by object-name pattern matching.
LAMPS: dict[int, dict[str, Any]] = {
	1: {"id": "lamp.1k-mini-bonus", "label": "1K Mini Bonus", "pin": "A5J1-18", "positions": [(431.186, 1096.390)]},
	2: {"id": "lamp.5k-mini-bonus", "label": "5K Mini Bonus", "pin": "A5J1-19", "positions": [(482.906, 1255.823)]},
	3: {"id": "lamp.9k-mini-bonus", "label": "9K Mini Bonus", "pin": "A5J1-17", "positions": [(346.855, 1156.916)]},
	4: {
		"id": "lamp.1k-super-bonus", "label": "1K Super Bonus", "pin": "A5J1-23",
		"positions": [(430.823, 1336.819)],
		"notes": "The A5 connector sheet prints A5J1-23 \"1K MINI BONUS\", duplicating A5J1-18. It is a "
			"printed error: sweeping the whole sheet leaves the SUPER BONUS ladder missing exactly its "
			"1K step and no other row unaccounted for, and the retained script binds this address to "
			"its own LBonus1 while binding public 1 to LMiniBonus1.",
	},
	5: {"id": "lamp.5k-super-bonus", "label": "5K Super Bonus", "pin": "A5J1-14", "positions": [(482.648, 1497.316)]},
	6: {"id": "lamp.9k-super-bonus", "label": "9K Super Bonus", "pin": "A5J1-15", "positions": [(346.631, 1397.514)]},
	7: {"id": "lamp.2x-bonus", "label": "2X Bonus", "pin": "A5J1-16", "positions": [(303.490, 1541.557)]},
	8: {"id": "lamp.first-drop-target-arrow", "label": "#1 Drop Target Arrow", "pin": "A5J1-28", "positions": [(392.015, 231.807)]},
	9: {"id": "lamp.four-drop-target-a-bottom", "label": "4 Drop Target \"A\" (Bottom)", "pin": "A5J1-24", "positions": [(151.787, 1077.457)]},
	10: {"id": "lamp.right-side-lower-target", "label": "Rt. Side Lower Target", "pin": "A5J1-25", "positions": [(729.781, 1063.450)]},
	11: {
		"id": "lamp.shoot-again", "label": "Shoot Again", "pin": "A5J2-21", "location": "backbox",
		"spatial_reason": "cabinet_or_service",
		"notes": "Back box insert-panel lamp. It is one of the six functional A5J2 pins that Table B "
			"does not carry onward to the playfield.",
	},
	12: {"id": "lamp.10k-saucer", "label": "10K Saucer", "pin": "A5J1-27", "positions": [(431.348, 885.708)]},
	13: {
		"id": "lamp.ball-in-play", "label": "Ball In Play", "pin": "A5J2-22", "location": "backbox",
		"spatial_reason": "cabinet_or_service", "notes": "Back box insert-panel lamp.",
	},
	14: {
		"id": "lamp.top-thumper-bumper", "label": "Top Thumper Bumper", "pin": "A5J2-16",
		"positions": [(491.210, 97.733)],
		"notes": "Carried from the back box insert panel to a playfield insert by Table B pin 4. The "
			"retained table models it as two co-located Light objects (upperbumperlight001 and 002) at "
			"the top bumper's own centre; that is a render double, so one placement is recorded.",
	},
	15: {
		"id": "lamp.right-outlane-special", "label": "Rt. Out Special", "pin": "A5J2-14",
		"positions": [(49.274, 1332.927)],
		"notes": "Carried to a playfield insert by Table B pin 1. Note that the insert sits beside the "
			"left-hand drain area of the retained table's geometry while the switch it belongs to is on "
			"the right; the manual prints the pin function, and this definition does not reinterpret it.",
	},
	17: {"id": "lamp.2k-mini-bonus", "label": "2K Mini Bonus", "pin": "A5J1-1", "positions": [(482.995, 1112.849)]},
	18: {"id": "lamp.6k-mini-bonus", "label": "6K Mini Bonus", "pin": "A5J1-9", "positions": [(431.193, 1273.453)]},
	19: {"id": "lamp.10k-mini-bonus", "label": "10K Mini Bonus", "pin": "A5J1-8", "positions": [(379.187, 1113.092)]},
	20: {"id": "lamp.2k-super-bonus", "label": "2K Super Bonus", "pin": "A5J1-3", "positions": [(483.575, 1354.106)]},
	21: {"id": "lamp.6k-super-bonus", "label": "6K Super Bonus", "pin": "A5J1-2", "positions": [(430.765, 1514.488)]},
	22: {"id": "lamp.10k-super-bonus", "label": "10K Super Bonus", "pin": "A5J1-10", "positions": [(379.241, 1353.405)]},
	23: {"id": "lamp.3x-bonus", "label": "3X Bonus", "pin": "A5J1-7", "positions": [(364.885, 1582.349)]},
	24: {"id": "lamp.second-drop-target-arrow", "label": "#2 Drop Target Arrow", "pin": "A5J1-6", "positions": [(373.727, 278.656)]},
	25: {"id": "lamp.four-drop-target-b", "label": "4 Drop Target \"B\"", "pin": "A5J1-5", "positions": [(165.958, 1028.548)]},
	26: {"id": "lamp.flipper-feed-lane-right", "label": "Flipper Feed Lane (Rt.)", "pin": "A5J1-11", "positions": [(746.794, 1275.501)]},
	27: {
		"id": "lamp.match", "label": "Match", "pin": "A5J2-8", "location": "backbox",
		"spatial_reason": "cabinet_or_service",
		"notes": "Back box insert-panel lamp. Its SCR also reaches A5J1-4, which this game's sheet "
			"marks N/U, so only the J2 branch is fitted.",
	},
	28: {"id": "lamp.20k-saucer", "label": "20K Saucer", "pin": "A5J1-12", "positions": [(420.202, 832.254)]},
	29: {
		"id": "lamp.high-score-to-date", "label": "High Score To Date", "pin": "A5J2-23",
		"location": "backbox", "spatial_reason": "cabinet_or_service", "notes": "Back box insert-panel lamp.",
	},
	30: {
		"id": "lamp.in-line-drop-target-extra-ball", "label": "In-Line Drop Tar. X-Ball", "pin": "A5J2-20",
		"positions": [(665.770, 1022.284)],
		"notes": "Carried to a playfield insert by Table B pin 8.",
	},
	31: {
		"id": "lamp.left-outlane-special", "label": "Lft. Out Special", "pin": "A5J2-15",
		"positions": [(812.723, 1333.463)],
		"notes": "Carried to a playfield insert by Table B pin 3. As with public 15 the retained table "
			"places this insert on the opposite side from the switch of the same name; the printed pin "
			"function is preserved as-is.",
	},
	33: {"id": "lamp.3k-mini-bonus", "label": "3K Mini Bonus", "pin": "A5J3-26", "positions": [(514.896, 1157.096)]},
	34: {"id": "lamp.7k-mini-bonus", "label": "7K Mini Bonus", "pin": "A5J3-25", "positions": [(378.622, 1255.873)]},
	35: {"id": "lamp.right-spinner", "label": "Rt. Spinner", "pin": "A5J3-19", "positions": [(635.406, 917.731)]},
	36: {"id": "lamp.3k-super-bonus", "label": "3K Super Bonus", "pin": "A5J3-17", "positions": [(514.842, 1398.346)]},
	37: {"id": "lamp.7k-super-bonus", "label": "7K Super Bonus", "pin": "A5J3-16", "positions": [(379.087, 1497.173)]},
	38: {"id": "lamp.50k-mini-bonus", "label": "50K Mini Bonus", "pin": "A5J3-23", "positions": [(431.331, 1185.030)]},
	39: {"id": "lamp.4x-bonus", "label": "4X Bonus", "pin": "A5J3-27", "positions": [(495.154, 1575.501)]},
	40: {"id": "lamp.third-drop-target-arrow", "label": "#3 Drop Target Arrow", "pin": "A5J1-13", "positions": [(361.565, 327.091)]},
	41: {"id": "lamp.four-drop-target-c", "label": "4 Drop Target \"C\"", "pin": "A5J3-21", "positions": [(180.119, 981.125)]},
	42: {"id": "lamp.flipper-feed-lane-left", "label": "Flipper Feed Lane (Left)", "pin": "A5J3-20", "positions": [(112.560, 1271.592)]},
	43: {
		"id": "lamp.same-player-shoots-again", "label": "Same Player S.A.", "pin": "A5J3-22",
		"positions": [(429.419, 1700.426)],
		"notes": "The SCR also reaches A5J2-9, which this game's sheet marks N/U, so only the J3 "
			"playfield branch is fitted - the same fan-out that had to be corrected on Bally Kiss.",
	},
	44: {"id": "lamp.extra-ball-saucer", "label": "X-Ball Saucer", "pin": "A5J3-24", "positions": [(402.358, 719.788)]},
	45: {
		"id": "lamp.game-over", "label": "Game Over", "pin": "A5J2-11", "location": "backbox",
		"spatial_reason": "cabinet_or_service", "notes": "Back box insert-panel lamp.",
	},
	46: {
		"id": "lamp.30k-saucer", "label": "30K Saucer", "pin": "A5J2-6", "positions": [(407.820, 778.982)],
		"notes": "Carried to a playfield insert by Table B pin 6.",
	},
	47: {
		"id": "lamp.lower-top-right-rollover-button", "label": "Lower Top Rt. R.O. Button", "pin": "A5J2-2",
		"positions": [(743.219, 411.865)],
		"notes": "Carried to a playfield insert by Table B pin 2. It lights the lower of the two "
			"right-hand rollover buttons on switch 1; the upper one is public 65 on the auxiliary board.",
	},
	49: {"id": "lamp.4k-mini-bonus", "label": "4K Mini Bonus", "pin": "A5J3-1", "positions": [(515.227, 1211.579)]},
	50: {"id": "lamp.8k-mini-bonus", "label": "8K Mini Bonus", "pin": "A5J3-12", "positions": [(346.837, 1211.655)]},
	51: {"id": "lamp.left-spinner", "label": "Left Spinner", "pin": "A5J3-15", "positions": [(157.458, 733.604)]},
	52: {"id": "lamp.4k-super-bonus", "label": "4K Super Bonus", "pin": "A5J3-11", "positions": [(514.725, 1452.424)]},
	53: {"id": "lamp.8k-super-bonus", "label": "8K Super Bonus", "pin": "A5J3-9", "positions": [(346.873, 1452.115)]},
	54: {"id": "lamp.100k-super-bonus", "label": "100K Super Bonus", "pin": "A5J3-3", "positions": [(430.890, 1427.526)]},
	55: {"id": "lamp.5x-bonus", "label": "5X Bonus", "pin": "A5J3-4", "positions": [(556.972, 1535.554)]},
	56: {"id": "lamp.4x-three-drop-target", "label": "4X 3 Drop Tar.", "pin": "A5J3-2", "positions": [(456.695, 330.355)]},
	57: {"id": "lamp.four-drop-target-d-top", "label": "4 Drop Target \"D\" (Top)", "pin": "A5J3-10", "positions": [(193.078, 929.536)]},
	58: {"id": "lamp.right-side-upper-target", "label": "Rt. Side Upper Target", "pin": "A5J3-18", "positions": [(730.206, 1123.847)]},
	59: {
		"id": "lamp.credit-indicator", "label": "Credit Indicator", "pin": "A5J3-13",
		"positions": [(161.163, 1741.961)],
		"notes": "A5J3 is the playfield connector on this sheet and the retained table places the "
			"credit indicator on the apron, so it is recorded as a playfield placement rather than a "
			"cabinet record. Its SCR also reaches A5J2-5, which this game's sheet marks N/U.",
	},
	60: {"id": "lamp.5x-four-drop-target", "label": "5X 4 Drop Tar.", "pin": "A5J3-14", "positions": [(230.389, 1019.500)]},
	61: {
		"id": "lamp.tilt", "label": "Tilt", "pin": "A5J2-10", "location": "backbox",
		"spatial_reason": "cabinet_or_service", "notes": "Back box insert-panel lamp.",
	},
	62: {
		"id": "lamp.top-target-collect-bonus", "label": "Top Tar. Col. Bonus", "pin": "A5J2-7",
		"positions": [(434.265, 167.897)],
		"notes": "Carried to a playfield insert by Table B pin 7.",
	},
	63: {
		"id": "lamp.top-target-special", "label": "Top Tar. Special", "pin": "A5J2-1",
		"positions": [(404.150, 117.184)],
		"notes": "Carried to a playfield insert by Table B pin 5.",
	},
	65: {
		"id": "lamp.upper-top-right-rollover-button", "label": "Upper Top Rt. R.O. Button",
		"pin": "A9J2-7", "scr": "Q1", "positions": [(734.360, 302.020)],
		"notes": "Lights the upper of the two right-hand rollover buttons on switch 1.",
	},
	66: {
		"id": "lamp.flash-gordon-letter-group-1", "label": "1 Flash Gordon", "pin": "A9J2-4", "scr": "Q2",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "First of the six back box circuits that animate the FLASH GORDON logo. The retained "
			"table drives its backglass material named FL, matching the printed numbering 1-6 running "
			"FL-AS-H-GO-RD-ON.",
	},
	67: {
		"id": "lamp.flash-gordon-letter-group-4", "label": "4 Flash Gordon", "pin": "A9J2-8", "scr": "Q3",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "Fourth FLASH GORDON logo circuit; the retained table's backglass material is GO.",
	},
	68: {
		"id": "lamp.face-of-ming-lower", "label": "Face Of Ming (lower pair)", "pin": "A9J2-10", "scr": "Q4",
		"positions": [(248.841, 586.108), (333.095, 603.121)],
		"notes": "One of two identically printed FACE OF MING circuits. The retained script's own "
			"comments split the four Ming lamps into \"Bottom 2\" for this address and \"Top 2\" for "
			"public 84, and the two objects placed here are the pair with the larger y. The script "
			"assigns all four objects to this address and leaves its public 84 assignment commented "
			"out; the manual's two separate circuits are followed instead.",
	},
	69: {
		"id": "lamp.3x-15-second-clock", "label": "3X 15 Second Clock", "pin": "A9J2-9", "scr": "Q5",
		"positions": [(572.489, 1304.662)],
		"notes": "One of the pair of timed multiplier lamps; the retained table calls it the right "
			"clock-seconds lamp.",
	},
	70: {"id": "lamp.unused-auxiliary-output-70", "label": "Unused auxiliary lamp output 70", "pin": "A9J2-6", "scr": "Q6", "availability": "unused", "spatial_reason": "unused"},
	71: {"id": "lamp.unused-auxiliary-output-71", "label": "Unused auxiliary lamp output 71", "pin": "A9J2-5", "scr": "Q7", "availability": "unused", "spatial_reason": "unused"},
	81: {
		"id": "lamp.top-shooter-alley-rollover-button", "label": "Top Shooter Alley R.O. Button",
		"pin": "A9J2-14", "scr": "Q8", "positions": [(673.748, 91.947)],
	},
	82: {
		"id": "lamp.flash-gordon-letter-group-2", "label": "2 Flash Gordon", "pin": "A9J2-11", "scr": "Q9",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "Second FLASH GORDON logo circuit; the retained table's backglass material is AS.",
	},
	83: {
		"id": "lamp.flash-gordon-letter-group-5", "label": "5 Flash Gordon", "pin": "A9J2-15", "scr": "Q10",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "Fifth FLASH GORDON logo circuit; the retained table's backglass material is RD.",
	},
	84: {
		"id": "lamp.face-of-ming-upper", "label": "Face Of Ming (upper pair)", "pin": "A9J2-18", "scr": "Q11",
		"positions": [(192.131, 458.917), (346.867, 494.563)],
		"notes": "The second FACE OF MING circuit. The retained script comments this address \"Top 2\" "
			"but leaves the assignment commented out, so the two objects with the smaller y are placed "
			"here on the strength of that comment and the manual's two separate circuits.",
	},
	85: {
		"id": "lamp.2x-15-second-clock", "label": "2X 15 Second Clock", "pin": "A9J2-17", "scr": "Q12",
		"positions": [(287.884, 1306.193)],
		"notes": "The other timed multiplier lamp; the retained table calls it the left clock-seconds lamp.",
	},
	86: {"id": "lamp.unused-auxiliary-output-86", "label": "Unused auxiliary lamp output 86", "pin": "A9J2-13", "scr": "Q13", "availability": "unused", "spatial_reason": "unused"},
	87: {"id": "lamp.unused-auxiliary-output-87", "label": "Unused auxiliary lamp output 87", "pin": "A9J2-12", "scr": "Q14", "availability": "unused", "spatial_reason": "unused"},
	97: {
		"id": "lamp.middle-shooter-alley-rollover-button", "label": "Middle Shooter Alley R.O. Button",
		"pin": "A9J3-8", "scr": "Q15", "positions": [(795.926, 176.567)],
	},
	98: {
		"id": "lamp.flash-gordon-letter-group-3", "label": "3 Flash Gordon", "pin": "A9J3-3", "scr": "Q16",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "Third FLASH GORDON logo circuit; the retained table's backglass material is H.",
	},
	99: {
		"id": "lamp.flash-gordon-letter-group-6", "label": "6 Flash Gordon", "pin": "A9J3-9", "scr": "Q17",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "Sixth FLASH GORDON logo circuit; the retained table's backglass material is ON.",
	},
	100: {
		"id": "lamp.unused-auxiliary-output-100", "label": "Unused auxiliary lamp output 100",
		"pin": "A9J3-11", "scr": "Q18", "availability": "unused",
		"notes": "The A9 board sheet prints this circuit's connector pin N/U and the A9J3 harness plug "
			"table on the same sheet gives it no wire, yet the retained known-working table binds the "
			"address to the two left-hand rollover-button inserts of switch 1 - which Figure V draws "
			"with the same star-burst symbol it uses for the lit rollover buttons that do have "
			"circuits. Recorded as conflict.aux-lamp-100-left-rollover-fitment and left unused with no "
			"spatial key rather than resolved either way.",
	},
	101: {
		"id": "lamp.3x-saucer-arrow", "label": "3X Saucer Arrow", "pin": "A9J3-10", "scr": "Q19",
		"positions": [(477.349, 963.657)],
	},
	102: {"id": "lamp.unused-auxiliary-output-102", "label": "Unused auxiliary lamp output 102", "pin": "A9J3-7", "scr": "Q20", "availability": "unused", "spatial_reason": "unused"},
	103: {"id": "lamp.unused-auxiliary-output-103", "label": "Unused auxiliary lamp output 103", "pin": "A9J3-4", "scr": "Q21", "availability": "unused", "spatial_reason": "unused"},
	113: {
		"id": "lamp.lower-shooter-alley-rollover-button", "label": "Lower Shooter Alley R.O. Button",
		"pin": "A9J3-15", "scr": "Q22", "positions": [(872.241, 299.939)],
	},
	114: {"id": "lamp.unused-auxiliary-output-114", "label": "Unused auxiliary lamp output 114", "pin": "A9J3-12", "scr": "Q23", "availability": "unused", "spatial_reason": "unused"},
	115: {"id": "lamp.unused-auxiliary-output-115", "label": "Unused auxiliary lamp output 115", "pin": "A9J3-16", "scr": "Q24", "availability": "unused", "spatial_reason": "unused"},
	116: {
		"id": "lamp.back-box-strobe", "label": "Back Box Strobe", "pin": "A9J3-18", "scr": "Q25",
		"location": "backbox", "spatial_reason": "cabinet_or_service",
		"notes": "This circuit does not light a bulb: A9J3-18 runs to pin 7 of the Strobe Module A13 "
			"(AS-2518-62), the back box flash tube, as the back box wiring sheet's own A13 connector "
			"list shows.",
	},
	117: {
		"id": "lamp.2x-saucer-arrow", "label": "2X Saucer Arrow", "pin": "A9J3-17", "scr": "Q26",
		"positions": [(386.286, 961.329)],
	},
	118: {"id": "lamp.unused-auxiliary-output-118", "label": "Unused auxiliary lamp output 118", "pin": "A9J3-14", "scr": "Q27", "availability": "unused", "spatial_reason": "unused"},
	119: {"id": "lamp.unused-auxiliary-output-119", "label": "Unused auxiliary lamp output 119", "pin": "A9J3-13", "scr": "Q28", "availability": "unused", "spatial_reason": "unused"},
}

MAIN_BOARD_ADDRESSES = tuple(
	address for address in range(1, 64) if address % 16 != 0
)
AUXILIARY_ADDRESSES = tuple(
	64 + 16 * data_line + latched + 1
	for data_line in range(4)
	for latched in range(7)
)

# Table B on the back box wiring sheet carries these eight A5J2 circuits onward from the back box
# insert panel to playfield inserts. The other six functional A5J2 pins are the insert-panel lamps.
TABLE_B_ADDRESSES = (63, 47, 46, 62, 15, 31, 14, 30)

DIPS: dict[int, str] = {
	1: "Credits per coin, coin chute #1 (hinge side), selector bit 1",
	2: "Credits per coin, coin chute #1 (hinge side), selector bit 2",
	3: "Credits per coin, coin chute #1 (hinge side), selector bit 3",
	4: "Credits per coin, coin chute #1 (hinge side), selector bit 4",
	5: "Credits per coin, coin chute #1 (hinge side), selector bit 5",
	6: "Saucer 10,000 lite adjustment (ON = lit at start of game)",
	7: "Saucer values lite adjustment (ON = lit values carry to next ball)",
	8: "Saucer 2X/3X arrow lite adjustment (ON = lit arrow carries to next ball)",
	9: "Credits per coin, coin chute #3 (right side), selector bit 1",
	10: "Credits per coin, coin chute #3 (right side), selector bit 2",
	11: "Credits per coin, coin chute #3 (right side), selector bit 3",
	12: "Credits per coin, coin chute #3 (right side), selector bit 4",
	13: "Credits per coin, coin chute #3 (right side), selector bit 5",
	14: "Outlane specials lite adjustment (ON = lit specials carry to next ball)",
	15: "Top target special lite adjustment (ON = lit special carries to next ball)",
	16: "2X/3X/4X/5X bonus lite adjustment (ON = lit bonus carries to next ball)",
	17: "Credits per coin, coin chute #2 (center), selector bit 1",
	18: "Credits per coin, coin chute #2 (center), selector bit 2",
	19: "Credits per coin, coin chute #2 (center), selector bit 3",
	20: "Credits per coin, coin chute #2 (center), selector bit 4",
	21: "Game over attract voice (ON = \"Emperor Ming Awaits\")",
	22: "2 side targets and flipper feed lanes lite adjustment",
	23: "4 drop target lite adjustment",
	24: "Top 3 target arrow lite adjustment",
	25: "Maximum credits selector bit 1 (10, 15, 25 or 40)",
	26: "Maximum credits selector bit 2 (10, 15, 25 or 40)",
	27: "Credit display (ON = credits displayed)",
	28: "Match feature (ON = match on)",
	29: "Replays per game (ON = all replays collected, OFF = one per player per game)",
	30: "In-line extra ball lite adjustment (ON = one extra ball per ball)",
	31: "Balls per game selector bit 1 (2, 3, 4 or 5)",
	32: "Balls per game selector bit 2 (2, 3, 4 or 5)",
}

DISPLAYS = (
	("display.player-1-score", "Player 1 score, seven digits", 0, 1, 7),
	("display.player-2-score", "Player 2 score, seven digits", 1, 9, 7),
	("display.player-3-score", "Player 3 score, seven digits", 2, 17, 7),
	("display.player-4-score", "Player 4 score, seven digits", 3, 25, 7),
	("display.credits", "Credits, two digits", 4, 35, 2),
	("display.ball-in-play", "Match and ball in play, two digits", 5, 38, 2),
)

CONFLICTS = [
	{
		"id": "conflict.outlane-special-insert-side-transposition",
		"path": "binding:pinmame.output.lamp/15",
		"description": "The two outlane Special inserts are placed on the opposite side of the "
			"playfield from the outlane each one is named for, and the disagreement is inside the "
			"retained table rather than between the table and the manual. The manual's lamp list "
			"names public 15 \"Rt. Out Special\" (A5J2-14) and public 31 \"Lft. Out Special\" "
			"(A5J2-15), and the retained table's own outlane switch objects are sided in agreement "
			"with those names: the left outlane sensor normalizes to x = 0.052 and the right to "
			"x = 0.852. But the table's Light objects invert it, placing L15 at x = 0.051708 on the "
			"left and L31 at x = 0.852858 on the right. The table is therefore internally "
			"inconsistent about one physical location, exactly as Stern Ripley's Believe It or Not! "
			"turned out to be about its pop bumpers. This definition preserves the observed object "
			"coordinates rather than swapping them, because swapping would assert a coordinate no "
			"source observed for the insert of that name; the disagreement is recorded here instead "
			"so the placement is not read as a settled fact. Resolving it needs this game's own "
			"printed playfield insert map traced to A5J2-14 and A5J2-15, or a lamp test on real "
			"hardware. Note the same shape may affect public lamps 10 and 58, whose emitter "
			"y-coordinates are likewise swapped relative to the switches of the same names; that "
			"pair additionally sits inside "
			"conflict.right-side-target-upper-lower-transposition and is not independently resolved "
			"here. Resolution path: this game's own printed playfield insert map traced to A5J2-14 "
			"and A5J2-15, a photograph of an unrestored machine's A5J2 harness at those two pins, or "
			"a lamp test on real hardware observing which outlane insert lights while public 15 and "
			"public 31 are driven in turn. Unresolved.",
		"source_refs": [MANUAL_SOURCE, TABLE_SOURCE, SCRIPT_SOURCE],
	},
	{
		"id": "conflict.right-side-target-upper-lower-transposition",
		"path": "binding:pinmame.input.switch/12",
		"description": "The two right-rail standup targets are labelled the opposite way round by two "
			"parts of this machine's own manual. The printed Switch Assembly Self-Test table (PDF page "
			"22) reads \"12 LOWER RIGHT SIDE TARGET\" and \"15 UPPER RIGHT SIDE TARGET\", and Figure V "
			"(PDF page 23) independently draws circle 15 on the upper target and circle 12 on the "
			"lower one. The Playfield A6 switch matrix sheet (PDF page 46) labels the same two matrix "
			"positions RIGHT SIDE UPPER TARGET at 12 and RIGHT SIDE LOWER TARGET at 15, and the "
			"retained known-working table follows the schematic, naming its upper object sw12 and its "
			"lower object sw15. The two agreeing manual sources are used for both the label and the "
			"placement, which means this definition deliberately places switch 12 on the table object "
			"named sw15 and switch 15 on the object named sw12. Resolving it needs a photograph of an "
			"unrestored machine with the two target harnesses traced, or a stuck-switch self-test on "
			"real hardware. Resolution path: a photograph of an unrestored machine with the two "
			"right-rail target harnesses traced back to the A6 switch matrix, or closing each of the "
			"two targets by hand on real hardware during the machine's own Switch Assembly self test "
			"and reading which number the score displays report for it. Unresolved.",
		"source_refs": [MANUAL_SOURCE, TABLE_SOURCE, SCRIPT_SOURCE],
	},
	{
		"id": "conflict.aux-lamp-100-left-rollover-fitment",
		"path": "binding:pinmame.output.lamp/100",
		"description": "Public lamp 100 is auxiliary circuit U4 output 3 through SCR Q18 to A9J3-11. "
			"The A9 schematic prints that pin's function as N/U and the A9J3 harness plug table on the "
			"same sheet gives the pin no wire, so on the manual's evidence nothing is fitted. The "
			"retained known-working table nevertheless binds public 100 to the two left-hand rollover "
			"buttons of switch 1, which are the only two of the seven rollover buttons on the machine "
			"with no lamp circuit of their own, and Figure V draws them with the same star-burst symbol "
			"as the five that do. The address is left unused with no spatial key rather than resolved "
			"either way; a LibPinMAME harness trace observing whether a legal flashgdn ROM ever drives "
			"public 100 outside the lamp self-test would settle whether the ROM believes the circuit "
			"exists, though only a machine or a factory insert map can settle whether a bulb does. "
			"Resolution path: run the implemented LibPinMAME gameplay harness against a legal "
			"flashgdn ROM and observe whether public lamp 100 is ever driven outside the lamp self "
			"test, then a photograph of an unrestored machine's A9J3 harness at pin 11, or a factory "
			"playfield insert map reaching that pin, to settle whether a bulb is fitted behind it. "
			"Unresolved.",
		"source_refs": [MANUAL_SOURCE, SCRIPT_SOURCE],
	},
]


def normalize(x: float, y: float) -> tuple[float, float]:
	return round(x / TABLE_WIDTH, 6), round(y / TABLE_HEIGHT, 6)


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (raw_x, raw_y) in enumerate(positions, start=1):
		x, y = normalize(raw_x, raw_y)
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": provenance(*source_refs),
		})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def legacy_numeric(address: int) -> list[str]:
	"""The legacy corpus exposed each address bare, then two-digit, then three-digit."""
	return list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))


def build_inputs() -> list[dict[str, Any]]:
	inputs: list[dict[str, Any]] = []
	for address in sorted(SWITCHES):
		spec = SWITCHES[address]
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.switch", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.self-test", "value": "%02d" % address})
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": spec.get("availability", "used"),
			"binding": {"device": address, "group": "pinmame.input.switch"},
			"id": spec["id"],
			"kind": "switch",
			"label": spec["label"],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, CORE_SOURCE),
		}
		if "initial_active" in spec:
			item["initial_active"] = spec["initial_active"]
		physical: dict[str, Any] = {}
		if "switch_type" in spec:
			physical["switch_type"] = spec["switch_type"]
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		if spec.get("location"):
			physical["location"] = spec["location"]
		if spec.get("notes"):
			physical["notes"] = spec["notes"]
		if physical:
			item["physical"] = physical
		if spec.get("positions"):
			item["spatial"] = located(spec["id"], "sensor", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
		elif spec.get("spatial_reason"):
			item["spatial"] = not_applicable(spec["spatial_reason"], MANUAL_SOURCE, CORE_SOURCE)
		inputs.append(item)

	for address in sorted(DIPS):
		inputs.append({
			"aliases": [
				{"namespace": "pinmame.dip", "value": str(address)},
				{"namespace": "manual.address", "value": "S%d" % address},
			],
			"availability": "used",
			"binding": {"device": address, "group": "pinmame.input.dip"},
			"id": "dip.option-switch-%d" % address,
			"kind": "dip_switch",
			"label": DIPS[address],
			"physical": {
				"switch_type": "dip",
				"notes": "One of the thirty-two MPU option switches on module A4 in the back box, "
					"supplied in four sixteen-lead packages printed S1-8, S9-16, S17-24 and S25-32. "
					"S33 on the same assembly is a momentary high-score reset button and not an option "
					"switch.",
			},
			"provenance": provenance(MANUAL_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		})
	return inputs


def build_outputs() -> list[dict[str, Any]]:
	outputs: list[dict[str, Any]] = []
	for address in sorted(SOLENOIDS):
		spec = SOLENOIDS[address]
		aliases = [{"namespace": "pinmame.coil", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.coil", "value": value} for value in legacy_numeric(address)]
		if spec.get("self_test"):
			aliases.append({"namespace": "manual.self-test", "value": spec["self_test"]})
		physical: dict[str, Any] = {}
		if spec.get("part_number"):
			physical["part_number"] = spec["part_number"]
		if spec.get("notes"):
			physical["notes"] = spec["notes"]
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": spec.get("availability", "used"),
			"binding": {"device": address, "group": "pinmame.output.solenoid"},
			"id": spec["id"],
			"kind": spec["kind"],
			"label": spec["label"],
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, CORE_SOURCE),
		}
		if physical:
			item["physical"] = physical
		if spec.get("positions"):
			item["spatial"] = located(spec["id"], "effect", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
		elif spec.get("spatial_reason"):
			item["spatial"] = not_applicable(spec["spatial_reason"], MANUAL_SOURCE, CORE_SOURCE)
		outputs.append(item)

	for address in sorted(LAMPS):
		spec = LAMPS[address]
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		aliases += [{"namespace": "vpe-legacy.lamp", "value": value} for value in legacy_numeric(address)]
		aliases.append({"namespace": "manual.address", "value": spec["pin"]})
		board = "Auxiliary Lamp Driver A9 (AS-2518-52)" if address > 64 else "Lamp Driver A5 (AS-2518-23)"
		note = spec.get("notes")
		physical: dict[str, Any] = {"quantity": len(spec.get("positions") or []) or 1}
		if spec.get("location"):
			physical["location"] = spec["location"]
		detail = f"{board}, connector pin {spec['pin']}"
		if spec.get("scr"):
			detail += f", SCR {spec['scr']}"
		detail += "."
		if address in TABLE_B_ADDRESSES:
			detail += (" A5J2 is the back box insert-panel connector; Table B on the back box wiring "
				"sheet carries this circuit onward through the panel-to-back-cab plug to a playfield "
				"insert.")
		physical["notes"] = f"{detail} {note}" if note else detail
		item: dict[str, Any] = {
			"aliases": aliases,
			"availability": spec.get("availability", "used"),
			"binding": {"device": address, "group": "pinmame.output.lamp"},
			"id": spec["id"],
			"kind": "lamp",
			"label": spec["label"],
			"physical": physical,
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, CORE_SOURCE),
		}
		if spec.get("positions"):
			item["spatial"] = located(spec["id"], "emitter", spec["positions"], TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
		elif spec.get("spatial_reason"):
			item["spatial"] = not_applicable(spec["spatial_reason"], MANUAL_SOURCE, CORE_SOURCE)
		outputs.append(item)

	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	return outputs


def build_mechanisms() -> list[dict[str, Any]]:
	return [
		{
			"id": "mech.four-bank-drop-target",
			"label": "Left four-bank drop target",
			"kind": "drop_target_bank",
			"assembly_part_number": "NO-26-1900",
			"actuators": ["device.four-drop-target-reset"],
			"sensors": [
				"switch.four-drop-target-a-bottom",
				"switch.four-drop-target-b",
				"switch.four-drop-target-c",
				"switch.four-drop-target-d-top",
			],
			"behavior": "Four drop targets running up the left side of the lower playfield, printed A "
				"at the bottom through D at the top, with one shared reset coil and no individual down "
				"coils. Home state is all four up; a target's switch closes as it falls and opens again "
				"when the bank is reset, so the bank can only be restored as a whole. Two rebound "
				"rubbers beside the bank are a separate two-contact address, public switch 5. Each "
				"target has its own insert lamp - public 9, 25, 41 and 57 bottom to top - and the bank "
				"carries a 5X multiplier lamp at public 60.",
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
		},
		{
			"id": "mech.three-bank-drop-target",
			"label": "Upper-left three-bank drop target",
			"kind": "drop_target_bank",
			"assembly_part_number": "NO-26-1900",
			"actuators": ["device.three-drop-target-reset"],
			"sensors": [
				"switch.three-drop-target-top",
				"switch.three-drop-target-middle",
				"switch.three-drop-target-bottom",
			],
			"behavior": "Three drop targets on the upper-left playfield with one shared reset coil and "
				"no individual down coils. Three arrow inserts in front of the bank - public 8, 24 and "
				"40, printed #1, #2 and #3 Drop Tar. Arw. - show which target is currently worth the "
				"award, and public 56 is the bank's 4X multiplier.",
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
		},
		{
			"id": "mech.in-line-drop-target",
			"label": "Right in-line drop target bank and back target",
			"kind": "drop_target_bank",
			"assembly_part_number": "NO-26-1900",
			"actuators": ["device.in-line-drop-target-reset"],
			"sensors": [
				"switch.first-in-line-drop-target",
				"switch.second-in-line-drop-target",
				"switch.third-in-line-drop-target",
				"switch.in-line-back-target",
			],
			"behavior": "Three drop targets in line up the right side of the playfield, so the ball can "
				"only reach the second once the first is down and the third once the second is down, "
				"with one shared reset coil. Behind them sits a standup target, public switch 28, which "
				"is exposed only when all three have dropped; the retained script models it as an "
				"ordinary standup with no drop mechanism. Public lamp 30 is the bank's extra-ball insert.",
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
		},
		{
			"id": "mech.single-drop-target",
			"label": "Top single drop target",
			"kind": "drop_target_bank",
			"actuators": ["device.single-drop-target-reset", "device.single-drop-target-pull-down"],
			"sensors": ["switch.top-single-drop-target"],
			"behavior": "A one-target drop bank at the top right with two coils rather than one: an "
				"AO-27-1300 reset that raises it and a CE-31-2000 pull-down that drops it on ROM "
				"command. No other target on the machine can be lowered by the ROM. Home state is up; "
				"the switch closes while the target is down. The retained script drives both directions "
				"from these two addresses (DropSingleUp on public 9, DropSingleDown on public 12).",
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
		},
		{
			"id": "mech.centre-saucer",
			"label": "Centre two-way saucer",
			"kind": "kicker",
			"actuators": ["device.saucer-kick-up", "device.saucer-kick-down"],
			"sensors": ["switch.saucer"],
			"behavior": "A saucer in the middle of the playfield with two kicker coils that eject the "
				"ball in opposite directions: an AO-27-1300 kick-up that throws it back up the "
				"playfield and an AO-29-2100 kick-down that returns it toward the flippers. The saucer "
				"switch reports ball-present and both coils are gated on it in the retained script, "
				"which clears the switch before either kick. Its value inserts are public 12, 28 and 46 "
				"(10K, 20K and 30K) plus public 44 for extra ball, and the 2X and 3X saucer arrows are "
				"the auxiliary-board lamps 117 and 101.",
			"provenance": provenance(MANUAL_SOURCE, SCRIPT_SOURCE, TABLE_SOURCE),
		},
	]


def build_relationships() -> list[dict[str, Any]]:
	pairs = [
		("switch.right-slingshot", "device.right-slingshot"),
		("switch.left-slingshot", "device.left-slingshot"),
		("switch.top-thumper-bumper", "device.top-thumper-bumper"),
		("switch.right-thumper-bumper", "device.right-thumper-bumper"),
		("switch.left-thumper-bumper", "device.left-thumper-bumper"),
	]
	relationships = []
	for source, destination in pairs:
		name = destination.split(".", 1)[1]
		relationships.append({
			"id": f"rel.{name}-energized-by-its-switch",
			"kind": "direct",
			"source": source,
			"destination": destination,
			"provenance": provenance(MANUAL_SOURCE),
		})
	relationships.sort(key=lambda item: item["id"])
	return relationships


def build_sources() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "src/wpc/by35games.c CORE_GAMEDEFNV(flashgdn) and the nine CORE_CLONEDEFNV "
				"entries that name it as parent",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "src/wpc/by35games.c INITGAME2(flashgdn, GEN_BY35, dispBy7, FLIP_SW(FLIP_L), 8, "
				"SNDBRD_BY61, 0); src/wpc/by35.c pia1b_w solenoid selector and continuous nibble, "
				"by35_lampStrobe, pia0b_r column assembly; src/wpc/by35.h BY35GD_NOSOUNDE and "
				"BY35GD_SWVECTOR; src/wpc/core.h CORE_FIRSTUFLIPSOL/CORE_FIRSTLFLIPSOL; "
				"src/lisy/lisy35.c continuous-output identification",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "controllers/pinmame/by35.json",
			"revision": "1",
			"locator": "Bally MPU AS-2518-35 controller profile: switch, dip, solenoid and lamp address "
				"rules and the algebraic collapse of by35_lampStrobe",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.flash-gordon.1980/"
				"archive-arcademanual_Flash_Gordon_Bally_1981_English_Manual/"
				"Flash Gordon Bally 1981 English Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": "Bally game #1215 Flash Gordon operations manual, 63 PDF pages, (c) Bally Mfg. "
				"Corp. 1980; schematic sheets W-1187-26C dated 11-16-80 and W-1207-5C dated 11-17-80",
			"license": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; scan hosted by the Internet Archive "
				"(arcademanual_Flash_Gordon_Bally_1981_English_Manual)",
			"excerpts": [
				{
					"id": "excerpt.flash-gordon.self-test-tables",
					"image": "evidence/excerpts/bally.flash-gordon.1980/self-test-tables.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 22, crop box "
						"0.06,0.03,0.9,0.775, scanned page rendered at its native resolution (embedded "
						"image xref 87, 2556px across 8.52in), rendered at 300 dpi, 2142x2459 WebP "
						"quality 80",
					"image_sha256": "@self-test-tables.webp",
					"locator": "PDF page 22, printed 17, Solenoid Identification Table and Switch "
						"Assembly Self-Test Display Numbers",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/self-test-tables.md",
					"reviewed": True,
					"sha256": "@self-test-tables.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.switch-matrix",
					"image": "evidence/excerpts/bally.flash-gordon.1980/switch-matrix.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 46, crop box "
						"0.04,0.09,0.38,0.58 of the page, rendered at 300 dpi with pdftoppm, reduced to "
						"1000px wide grayscale, quality 75 WebP",
					"image_sha256": "@switch-matrix.webp",
					"locator": "PDF page 46, drawing W-1187-26 sheet PLAYFIELD A6, switch matrix block",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/switch-matrix-schematic.md",
					"reviewed": True,
					"sha256": "@switch-matrix-schematic.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.figure-v-locations",
					"image": "evidence/excerpts/bally.flash-gordon.1980/figure-v-right-rail.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 23, crop box "
						"0.42,0.38,0.65,0.56 of the page, rendered at 300 dpi with pdftoppm, reduced to "
						"1000px wide grayscale, quality 75 WebP",
					"image_sha256": "@figure-v-right-rail.webp",
					"locator": "PDF page 23, printed 18, Figure V switch and solenoid location map",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/figure-v-locations.md",
					"reviewed": True,
					"sha256": "@figure-v-locations.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.lamp-driver-a5-connectors",
					"image": "evidence/excerpts/bally.flash-gordon.1980/lamp-driver-a5-connectors.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 48, crop box "
						"0.015,0.455,0.585,0.895, scanned page rendered at its native resolution "
						"(embedded image xref 204, 2550px across 8.50in), rendered at 300 dpi, "
						"1454x1453 WebP quality 80",
					"image_sha256": "@lamp-driver-a5-connectors.webp",
					"locator": "PDF page 48, LAMP DRIVER A5 connector block, J1/J2/J3/J4",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/lamp-driver-a5-connectors.md",
					"reviewed": True,
					"sha256": "@lamp-driver-a5-connectors.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.auxiliary-lamp-driver-a9",
					"image": "evidence/excerpts/bally.flash-gordon.1980/auxiliary-lamp-driver-fanout.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 55, crop box "
						"0.60,0.09,0.92,0.65 of the page, rendered at 300 dpi with pdftoppm, reduced to "
						"1000px wide grayscale, quality 75 WebP",
					"image_sha256": "@auxiliary-lamp-driver-fanout.webp",
					"locator": "PDF page 55, drawing W-1207-5C, AUXILIARY LAMP DRIVER \"A9\"",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/auxiliary-lamp-driver-a9.md",
					"reviewed": True,
					"sha256": "@auxiliary-lamp-driver-a9.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.solenoid-driver-a3-connectors",
					"image": "evidence/excerpts/bally.flash-gordon.1980/solenoid-driver-a3-connectors.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 49, crop box "
						"0.385,0.065,0.975,0.895, scanned page rendered at its native resolution "
						"(embedded image xref 209, 2550px across 8.50in), rendered at 300 dpi, "
						"1506x2740 WebP quality 80",
					"image_sha256": "@solenoid-driver-a3-connectors.webp",
					"locator": "PDF page 49, drawing W-1187-26C, Voltage Regulator / Solenoid Driver A3 "
						"connectors, Table B, Table C and Strobe Module A13",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/solenoid-driver-a3-connectors.md",
					"reviewed": True,
					"sha256": "@solenoid-driver-a3-connectors.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.parts-list-coils",
					"image": "evidence/excerpts/bally.flash-gordon.1980/parts-list-coils.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 25, crop box "
						"0.06,0.03,0.94,0.635, scanned page rendered at its native resolution (embedded "
						"image xref 100, 2569px across 8.56in), rendered at 300 dpi, 2244x1997 WebP "
						"quality 80",
					"image_sha256": "@parts-list-coils.webp",
					"locator": "PDF page 25, printed 20, XI. PARTS LIST, plus the cover copyright line",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/parts-list-coils.md",
					"reviewed": True,
					"sha256": "@parts-list-coils.md",
					"transcribed_by": "curator, read from the rendered page",
				},
				{
					"id": "excerpt.flash-gordon.option-switches",
					"locator": "PDF pages 10-13, printed 5-8, V. GAME ADJUSTMENTS",
					"image": "evidence/excerpts/bally.flash-gordon.1980/option-switches.webp",
					"image_derivation": "Flash Gordon Bally 1981 English Manual.pdf page 12, crop box 0.05,0.05,0.95,0.94, scanned page rendered at its native resolution (embedded image xref 45, 2556px across 8.52in), rendered at 92 dpi, capped to 700px wide, 701x897 WebP quality 70",
					"image_sha256": "1781a4e2fed90ce9045e91109441dc76c2773ee441a7e0bf13772deade31d0dc",
					"method": "manual",
					"path": "evidence/excerpts/bally.flash-gordon.1980/option-switches.md",
					"reviewed": True,
					"sha256": "@option-switches.md",
					"transcribed_by": "curator, read from the retained text layer and checked against "
						"the rendered page",
				},
			],
		},
		{
			"id": TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/flash-gordon-1980/source/"
				"Flash Gordon (Bally 1981) 2.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": "Retained known-working community recreation, playfield bounds "
				f"{TABLE_BOUNDS}; the geometry authority for this definition",
			"license": "NOASSERTION",
			"attribution": "Community VPX table authors; redistribution rights not granted",
			"known_working": True,
		},
		{
			"id": SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/flash-gordon-1980/extracted-vpxtool/script.vbs",
			"sha256": SCRIPT_SHA256,
			"locator": "Embedded table script, 148322 bytes, cGameName = \"flashgdn\"; SolCallback "
				"cross-reference block and Lampz.MassAssign lamp bindings; the runtime address and "
				"causality authority",
			"license": "NOASSERTION",
			"attribution": "Community VPX table authors; redistribution rights not granted",
			"known_working": True,
		},
		{
			"id": EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/flash-gordon-1980/extracted-vpxtool",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": f"Retained vpxtool extraction; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes. The extraction does not "
				"record the extractor version, so the manifest identity is what pins it.",
			"license": "NOASSERTION",
			"attribution": "Community VPX table authors; redistribution rights not granted",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Flash%20Gordon%20%28Bally%201981%29%20VPW%20Mod%20v3.1.3.vbs",
			"revision": CORPUS_REVISION,
			"sha256": CORPUS_SCRIPT_SHA256,
			"locator": "Flash Gordon (Bally 1981) VPW Mod v3.1.3.vbs in the pinned known-working script "
				"corpus. Its SolCallback cross-reference block is verbatim identical to the retained "
				"table's, so it corroborates the transcription but shares ancestry and is not "
				"independent evidence of the mapping.",
			"license": "NOASSERTION",
			"attribution": "sverrewl/vpxtable_scripts contributors",
			"known_working": True,
		},
	]


def build() -> dict[str, Any]:
	inputs = build_inputs()
	outputs = build_outputs()
	return {
		"conflicts": CONFLICTS,
		"controller": {
			"platform": "pinmame.by35",
			"inversion_applied_by_emulator": True,
		},
		"coverage": {
			"dimensions": {
				"address_enumeration": "validated",
				"catalog_identity": "validated",
				"display_inventory": "validated",
				"mechanisms": "validated",
				"physical_wiring": "conflicted",
				"recreation_knowledge": "validated",
				"semantic_naming": "conflicted",
				"spatial_placement": "observed",
				"variant_coverage": "validated",
			},
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"status": "partial",
		},
		"displays": [
			{
				"controller_index": index,
				"id": identifier,
				"kind": "segment",
				"label": label,
				"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
				"segment_start": start,
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
				"width": width,
			}
			for identifier, label, index, start, width in DISPLAYS
		],
		"drivers": [
			{
				"description": DRIVERS[driver_id][0],
				"flags": 0,
				"id": driver_id,
				"manufacturer": DRIVERS[driver_id][2],
				"physical_compatibility": DRIVERS[driver_id][4],
				"variant_notes": DRIVERS[driver_id][5],
				"year": DRIVERS[driver_id][1],
				**({"clone_of": DRIVERS[driver_id][3]} if DRIVERS[driver_id][3] else {}),
			}
			for driver_id in sorted(DRIVER_IDS)
		],
		"format": "pinmame-machine-definition",
		"inputs": inputs,
		"knowledge": {"path": "knowledge/bally/flash-gordon-1980.md", "status": "complete"},
		"machine": {
			"id": MACHINE_ID,
			"kind": "physical_pinball",
			"manufacturer": "Bally",
			"model_number": "1215",
			"name": "Flash Gordon",
			"ipdb_id": 874,
			"opdb_id": "G5728-MDbjD",
			"playfield": {
				"height": TABLE_HEIGHT,
				"provenance": provenance(TABLE_SOURCE),
				"units": "vpx",
				"width": TABLE_WIDTH,
			},
			"year": 1980,
		},
		"mechanisms": build_mechanisms(),
		"outputs": outputs,
		"relationships": build_relationships(),
		"schema_version": 2,
		"sources": build_sources(),
	}


def resolve_excerpt_digests(document: dict[str, Any], root: Path) -> None:
	"""Replace ``@<file>`` digest placeholders with the real digest of the committed excerpt."""
	for source in document["sources"]:
		for excerpt in source.get("excerpts", []) or []:
			for field in ("sha256", "image_sha256"):
				value = excerpt.get(field)
				if isinstance(value, str) and value.startswith("@"):
					target = root / "evidence/excerpts/bally.flash-gordon.1980" / value[1:]
					if not target.is_file():
						raise RuntimeError(f"Flash Gordon excerpt is missing: {target}")
					excerpt[field] = hashlib.sha256(target.read_bytes()).hexdigest()


def build_definition(root: Path = ROOT) -> dict[str, Any]:
	document = build()
	resolve_excerpt_digests(document, root)
	return document


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	placements = 0
	resolved_inputs: list[int] = []
	resolved_outputs: list[dict[str, Any]] = []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	no_spatial_inputs: list[int] = []
	no_spatial_outputs: list[dict[str, Any]] = []

	for item in definition["inputs"]:
		address = item["binding"]["device"]
		spatial = item.get("spatial")
		if spatial is None:
			no_spatial_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			placements += len(spatial["placements"])
			resolved_inputs.append(address)
	for item in definition["outputs"]:
		binding = {"address": item["binding"]["device"], "group": item["binding"]["group"]}
		spatial = item.get("spatial")
		if spatial is None:
			no_spatial_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placements += len(spatial["placements"])
			resolved_outputs.append(binding)

	projections = [
		{"address": address, "group": "pinmame.output.solenoid", "reason": SOLENOIDS[address]["projection"]}
		for address in sorted(SOLENOIDS)
		if SOLENOIDS[address].get("projection")
	]

	return {
		"blockers": [
			"Public switches 5 (Drop Target 50 Point Rebound) and 29 (10 Point Rebound) are real, "
			"fitted two-contact rebound addresses that the retained table implements as collidable "
			"Primitives named phys_sw5 and phys_sw29, both of which sit at a zero position with a zero "
			"rot_and_tra and no axis-aligned bounds recorded in the extraction. There is no usable "
			"coordinate for either, so the spatial key is omitted rather than a position invented.",
			"Public lamp 100 has no spatial key because the manual marks its circuit N/U in two places "
			"while the retained table binds it to the two left-hand rollover buttons of switch 1; see "
			"conflict.aux-lamp-100-left-rollover-fitment.",
			"Switches 12 and 15 are placed on the two right-rail standup targets according to the "
			"printed self-test table and Figure V, which means their placements are deliberately the "
			"reverse of the retained table's own object names; see "
			"conflict.right-side-target-upper-lower-transposition.",
		],
		"coordinate_convention": {
			"source_bounds": {"bottom": TABLE_HEIGHT, "left": 0.0, "right": TABLE_WIDTH, "top": 0.0},
			"space": "playfield",
			"x": f"x/{TABLE_WIDTH}; 0=left, 1=right",
			"y": f"y/{TABLE_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"excluded_object_classes": [
			"upperbumperlight002, a co-located render double of upperbumperlight001 at the top thumper "
			"bumper's own centre (public lamp 14 is one bulb, not two)",
			"creditlightoff, a co-located off-state double of creditlight (public lamp 59)",
			"p<n> and bulb<n> Primitive meshes, which are the retained script's DisableLighting2 render "
			"helpers for a lamp rather than emitters",
			"pstar<n> and star<n> Primitive meshes, the rollover-button animation helpers beside the "
			"Trigger objects that carry the switch",
			"GI_001 through GI_029 Light objects: Flash Gordon's general illumination is a plain 5.9 "
			"VAC transformer circuit with no driver-board output and no controller address, so it is "
			"not a device in this definition",
		],
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as "
				"sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/flash-gordon-1980/"
				"extracted-vpxtool.manifest.json",
			"source_ref": EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "unrecorded in the retained extraction",
		},
		"format": "pinmame-spatial-blockers",
		"machine_id": MACHINE_ID,
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(values, key=lambda item: (item["group"], item["address"]))
			for reason, values in sorted(na_outputs.items())
		},
		"placement_count": placements,
		"projections": projections,
		"resolved_input_addresses": sorted(resolved_inputs),
		"resolved_output_bindings": sorted(resolved_outputs, key=lambda item: (item["group"], item["address"])),
		"unplaced_input_addresses": sorted(no_spatial_inputs),
		"unplaced_output_bindings": sorted(no_spatial_outputs, key=lambda item: (item["group"], item["address"])),
		"version": 1,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Flash Gordon (Bally, 1980) spatial review",
		"",
		"Status: incomplete. Three addresses carry no placement and two carry a deliberately "
		"reversed one, so the machine record stays `partial` at "
		"`machines/partial/bally/flash-gordon-1980.json`.",
		"",
		"The matching source is the retained known-working `Flash Gordon (Bally 1981) 2.0.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. Its embedded script at SHA-256 `{SCRIPT_SHA256}` is the runtime "
		"address and causality authority. Exact playfield bounds are "
		f"`{TABLE_BOUNDS}`, and every canonical coordinate is x/952.9412 and y/1976.471 rounded to at "
		"most six fractional places. That y divisor is far shorter than the 2162 of the WPC machines "
		"curated elsewhere in this project, which is what an early-1980s playfield looks like; the "
		"lower flippers land at y = 0.833 and the outhole at y = 0.952.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script owns runtime addresses and causality, the Bally game #1215 manual owns "
		"physical construction, wiring, quantity and device presence, pinned PinMAME owns controller "
		"topology, and the retained table supplies geometry.",
		"- The public solenoid mapping is the retained script's own printed cross-reference, not the "
		"manual's Self Test # column, which is a test order. The manual says so itself. The two "
		"continuous outputs are corroborated independently by `src/lisy/lisy35.c`, which names "
		"continuous bit 1 the coin lockout and bit 2 the flipper-enable relay - public 18 and 19.",
		"- Lamp bindings come from the script's own `Lampz.MassAssign` calls, not from object-name "
		"patterns, and every one of them was checked against the function this game's A5 or A9 "
		"connector sheet prints against the pin the address reaches.",
		"- General illumination is not a device on this machine. The Playfield A6 sheet draws it as a "
		"5.9 VAC transformer circuit with no driver-board connection, and the BY35 controller profile "
		"declares no general-illumination group, so the retained table's `GI_*` Light objects are "
		"excluded rather than bound to an invented address.",
		"- Three flipper coils are fitted (parts list `Flipper (3)`), driven through the K1 relay at "
		"public 19 rather than by driver-board outputs, so they have no address and no placement. The "
		"retained table models the same three: two lower flippers and an upper right flipper that its "
		"own key handler drives from the right flipper button.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Solenoid {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		f"- Inputs with no spatial key at all: {len(report['unplaced_input_addresses'])} "
		f"({', '.join(str(value) for value in report['unplaced_input_addresses']) or 'none'})",
		f"- Outputs with no spatial key at all: {len(report['unplaced_output_bindings'])} "
		f"({', '.join(str(item['address']) for item in report['unplaced_output_bindings']) or 'none'})",
		"",
		"## Blockers",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. Two addresses that are certainly fitted - public "
		"switches 5 and 29, the two rebound-rubber pairs - have no coordinate anywhere in the retained "
		"extraction, and two first-class conflicts remain open: which of the two right-rail standup "
		"targets is switch 12 and which is switch 15, and whether auxiliary lamp circuit 100 is fitted "
		"at all. The record stays `partial` with "
		"`coverage.missing = [\"spatial_placement\", \"unresolved_conflicts\"]`.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Object-centre dump of every extracted game item, raw and normalized, at "
		"`external:pinmame-review-artifacts/flash-gordon-1980/vpx-geometry.txt`.",
		f"- Manual `Flash Gordon Bally 1981 English Manual.pdf`, SHA-256 `{MANUAL_SHA256}`, with eight "
		"transcribed excerpts under `evidence/excerpts/bally.flash-gordon.1980/`.",
		"",
	]
	return "\n".join(lines)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Flash Gordon retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Flash Gordon extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Flash Gordon retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Flash Gordon retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Flash Gordon retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def generate(root: Path = ROOT) -> Path:
	definition = build_definition(root)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_path.exists():
		raise RuntimeError(f"Stale Flash Gordon author-ready definition is still present: {stale_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Flash Gordon definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Flash Gordon seed is missing: {seed_path}")
	definition = build_definition(root)
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Flash Gordon definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Flash Gordon seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Flash Gordon spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Flash Gordon spatial review drifted from its deterministic curator: {markdown_path}")
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file():
		raise RuntimeError(f"Flash Gordon knowledge note is missing: {knowledge_path}")
	print("Flash Gordon definition, seed, and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Flash Gordon extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Flash Gordon retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
