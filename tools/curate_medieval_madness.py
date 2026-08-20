"""Curate the physical Williams Medieval Madness (1997) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed
label, wiring detail, and normalized coordinate as a literal, so regeneration
reproduces the canonical artifact byte-for-byte without reading the external
evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only
path that writes the canonical definition and its pinned seed.
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
DEFINITION_PATH = ROOT / "machines/author-ready/williams/medieval-madness-1997.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/medieval-madness-1997.json"
SEED_PATH = ROOT / "tools/seeds/williams/medieval-madness-1997.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/medieval-madness-1997.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/medieval-madness-1997.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.medieval-madness.1997"
MANUAL_PARTS_SOURCE = "manual-parts.williams.medieval-madness.1997"
MANUAL_SCHEMATICS_SOURCE = "manual-schematics.williams.medieval-madness.1997"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.medieval-madness.1997"
VPX_TABLE_SOURCE = "vpx-table.mm-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.mm-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.mm-vpw-1-0"
ROM_SOURCE = "rom.mm-authorized-corpus"
RUNTIME_SOURCE = "runtime.medieval-madness.boot-start-and-service"

TABLE_SHA256 = "9a05a555d03aca3d48d73b3e6566220b27fde46aa5d2517a08faacdbc58bcab9"
SCRIPT_SHA256 = "cdc5590888d810a44b772ec327789362cd27dd7a6c58870bc148b2d87a0f90f8"
MANUAL_PART1_SHA256 = "57d3b23e0d73e31318fb7054a1dc966db0924cf8f908a5844719ba9f50f0e672"
MANUAL_PART2_SHA256 = "71d16833c4c5d562830da1310d05214912dd77e90e966111fe5615ec70770319"
MANUAL_PART3_SHA256 = "1a426136cbc9df6297e8ea41d4f7b166d2b91aa2b188909b74d15be7b1c3d77d"
MANUAL_ARCARC_SHA256 = "9baac8156b1115171c0c5fc1cced2a4bfa2280067c72a49b58678d89c70b6f1d"
ROM_SHA256 = "aa949281de6f26b9f6d01313739c5ef061a30ed83d541fcbbe08f1650232bf75"
MANUAL_TRANSCRIPTION_SHA256 = "b0905ec59747532ca146ba4e0a6e66b384f28ad2528617b29bfed64221f9d4d2"

# Rendered manual pages that a human actually read to decide a canonical value. Recording their
# hashes makes an empty or substituted render cache an audit failure rather than an assumed source.
VISUAL_REVIEW_CACHE = (
	("part1/page-02.png", "81c456d190eacfad6de6eef0a8af8accac5b1742f88e383f12963010d66896ad", "Section 1 front matter: DIP-switch chart plus the complete solenoid/flasher, general-illumination, flipper-circuit, and motor-circuit table"),
	("part1/page-04.png", "e88da6a183f7c7558a5e73926a6b034f53114c84fbad0815ae1e5f1b81601909", "Security-CPU and electronic-ID notice, project number 559"),
	("part1/page-05.png", "2e6981a3357de52bfe2b12dfafcaaffe0968ff265e0de48f2b1ec0c769c732d5", "Coin-door interlock notice, assembly A-18249-3"),
	("hi/loc-47.png", "12c8759eacb7222aa389a1da0837df8d2344be20915aee9e5edda41919dfadac", "Printed page 2-46 lamp-locations parts list at 300 dpi"),
	("hi/loc-48.png", "b55eeb162517a6f478daaf0302646f24a55fe9183c98f867f5b55d4097820282", "Printed page 2-47 lamp-locations playfield map at 300 dpi"),
	("hi/loc-49.png", "891df6be1d33572b4876d762cfe1861a992dc0fb220e048795f5735b47562b30", "Printed page 2-48 switch-locations parts list at 300 dpi"),
	("hi/loc-50.png", "8a84eba215cb465d1ffeabaff605d91e99579b3bf717db5e1a4a20211164b675", "Printed page 2-49 switch-locations playfield map at 300 dpi"),
	("hi/loc-51.png", "10ae92361469b0bf447e466fa5c22ac0eb2d6da05ac26f05523086c0fb2d3d93", "Printed page 2-50 solenoid/flashlamp-locations parts list at 300 dpi"),
	("hi/parts-53.png", "f202054700c40c9af7cda3ca4710a4dcf31668ca295de4c8cd010c17a46e0ec7", "Printed page 2-52 lamp matrix at 300 dpi"),
	("hi/parts-54.png", "e22bbe4c20b9704061500606ca008af1e34ba19d830392d28723567a84dd2360", "Printed page 2-53 switch matrix at 300 dpi"),
	("hi/soltable-top-02.png", "9113448136cb6d94324acc32bbbf629efea6029e8419c66bb924d6d3e73a5c50", "300 dpi crop of the solenoid/flasher table used to re-verify every wire colour, connector, and driver transistor"),
	("hi/lamp15crop-48.png", "f2b608c58efe4315a14300810530e6411ea152d25e8e76ad5791f3c410cb3850", "300 dpi crop of the lamp-locations map showing lamp 15 as one large circular insert between the triangular 14 and the small rectangular 16"),
	("hi/lamp78rcrop-48.png", "9e1b6f09a1532fee00c85db21d0c71da8c7e283c30e431b14b5223842ec4e492", "300 dpi crop of the lamp-locations map showing the called-out lamp 78 arrow insert in the right orbit lane"),
	("hi/lamp78acrop-48.png", "d165bc83976665d0b7b72707cedc749dc52b98b1014c2b236f6b7618577b5ce2", "600 dpi crop of the lamp-locations map showing the matching, uncalled-out arrow insert in the left orbit lane"),
	("hi/troll-27.png", "2f6d7fbb5b2016f072ee7eea982b15a0165c8febaadd21ecce80b38a4b19a0e3", "Printed page 2-26: A-21719 troll assembly, used in games produced before July 21, 1997, with the same FL-11753 coil and 5647-12693-11 switch as the later A-22034"),
	("part3/page-10.png", "c992dd318cb00424713b6b13611f95b1c6c03f526b2f8c7c442740fe05eb3485", "Printed page 3-10: general-illumination circuit, five strings from the 6.3 V secondary, three triac-switched and two bridge-rectified, bounded at up to 18 bulbs per string"),
	("part3/page-11.png", "a9641bc1c4af60d1b051fc09c6ac7679af2ce654dd2067866a96c0d84638e534", "Printed page 3-11: flipper circuit diagram, +50 V flipper and troll supply, +12 V drawbridge motor supply on J139-2, the upper-flipper-to-troll footnote, and the reused F5-F8 template labels"),
	("hi/sec1-48.png", "5f06d8333f4ee2ea12a41e2b9cdf4e1292501b4d4df8c7f189860cd18d392d3f", "Printed page 1-19: T.13 states the matrix notation (left digit is the column, right digit is the row), T.15 places the DIP switches at CPU-board U27, and T.16 begins the loop/gate procedure"),
	("hi/sec1-49.png", "e80ac67493377e179a075f76cea422acdefe5a3c265db3fadb4612d08fb2c8f3", "Printed page 1-20: T.16 loop/gate causality and the stuck-open versus stuck-closed error split"),
	("hi/sec1-50.png", "6b5c6931a3027600db3719782d98340390a22d76c101692ec7e22bd8aafa11b9", "Printed page 1-21: T.17 tower ramp and tower-lock modes"),
	("hi/t17crop-50.png", "8e46e866cf3d5c5287a5017faf00da0143c68a31375da0992eb812e32aa35aff", "Enlarged crop of printed page 1-21 confirming the diverter-down tower path and the two-minute revert"),
	("hi/sec1-51.png", "39b9def69f7b92e579d938f700a4dd7944b63c1fe5221c16f9b5205b7254bb63", "Printed page 1-22: T.18 drawbridge and the start of T.19 castle gate"),
	("hi/sec1-52.png", "93aaf3942401c2f4e3853d2b67deb068cee07ffccf4838e4e9d8eb55a48aad71", "Printed page 1-23: T.19 castle mode ball path and exploding castle, plus T.20 trolls"),
	("hi/sec1-53.png", "f1edbf1fe772526437bebd1f608630bd567f46b29c7434c2e17a71c550f80c0d", "Printed page 1-24: the two-minute troll lower-out and T.21 empty balls"),
)

MANUAL_EXCERPT_BASE = "evidence/excerpts/williams.medieval-madness.1997"
MANUAL_EXCERPT_PATH = f"{MANUAL_EXCERPT_BASE}/manual-proof.md"
MANUAL_EXCERPT_SHA256 = "71e2e0edd657f753d27e73d0be1b51b66b54747c25fc70b6d1813ee024bc1021"


def _manual_excerpt(identifier: str, locator: str, image: str, image_sha256: str, image_derivation: str) -> dict[str, Any]:
	return {
		"id": identifier,
		"locator": locator,
		"path": MANUAL_EXCERPT_PATH,
		"sha256": MANUAL_EXCERPT_SHA256,
		"image": f"{MANUAL_EXCERPT_BASE}/{image}",
		"image_sha256": image_sha256,
		"image_derivation": image_derivation,
		"method": "manual",
		"transcribed_by": "curator, visually checked against the retained crop",
		"reviewed": True,
	}


MANUAL_PART1_EXCERPTS = [
	_manual_excerpt("excerpt.medieval-madness.power-table", "PDF page 2, complete solenoid/flasher, GI, flipper and motor table", "power-table.webp", "369fb7df5b344451a0a0fdb516a9d4a6ae23a3f1cc06ca3cb46ebdcfae08df37", "Medieval_Madness_1_OPS.pdf page 2, crop box 0.08,0.04,0.92,0.96, scanned page rendered at its native resolution (embedded image xref 4, 2601px across 8.67in), rendered at 91 dpi, capped to 650px wide, 651x922 WebP quality 40"),
	_manual_excerpt("excerpt.medieval-madness.loop-gate-tests", "PDF page 49, printed 1-20, Loop/Gate Test", "loop-gate-tests.webp", "94761e88f45947962c8bcbaf943c0b09b4b4e79341a0ab309c143d8c7d4ea2c6", "Medieval_Madness_1_OPS.pdf page 49, crop box 0.05,0.04,0.95,0.96, scanned page rendered at its native resolution (embedded image xref 200, 2569px across 8.56in), rendered at 92 dpi, capped to 700px wide, 701x927 WebP quality 45"),
	_manual_excerpt("excerpt.medieval-madness.tower-troll-test", "PDF page 50, printed 1-21, Tower Test and Trolls Test", "tower-troll-test.webp", "247e02a5a52e29a68f4e78290391816407dc4c46434884be782222dfc07709a6", "Medieval_Madness_1_OPS.pdf page 50, crop box 0.05,0.04,0.95,0.96, scanned page rendered at its native resolution (embedded image xref 204, 2588px across 8.63in), rendered at 92 dpi, capped to 700px wide, 701x927 WebP quality 45"),
	_manual_excerpt("excerpt.medieval-madness.drawbridge-castle-tests", "PDF page 51, printed 1-22, Drawbridge Test and Castle Gate Test", "drawbridge-castle-tests.webp", "3c4c70478aaef3703b4936cf16824d1f0271862fdaa9d03e5e627d857afb7a8f", "Medieval_Madness_1_OPS.pdf page 51, crop box 0.05,0.04,0.95,0.96, scanned page rendered at its native resolution (embedded image xref 208, 2575px across 8.58in), rendered at 92 dpi, capped to 700px wide, 701x927 WebP quality 45"),
	_manual_excerpt("excerpt.medieval-madness.castle-troll-tests", "PDF page 52, printed 1-23, Castle Gate and Trolls tests", "castle-troll-tests.webp", "403ade0b51f6465a1417fed5da1d6ca13cd4c24204cea4dec533817088e54b68", "Medieval_Madness_1_OPS.pdf page 52, crop box 0.05,0.04,0.95,0.96, scanned page rendered at its native resolution (embedded image xref 212, 2569px across 8.56in), rendered at 92 dpi, capped to 700px wide, 701x927 WebP quality 45"),
	_manual_excerpt("excerpt.medieval-madness.troll-empty-balls-tests", "PDF page 53, printed 1-24, Trolls and Empty Balls tests", "troll-empty-balls-tests.webp", "d7bffe524a5a0ddc978934974c133afa382f3135fbaed36e2168e9e844c1474e", "Medieval_Madness_1_OPS.pdf page 53, crop box 0.05,0.04,0.95,0.96, scanned page rendered at its native resolution (embedded image xref 216, 2595px across 8.65in), rendered at 111 dpi, capped to 850px wide, 851x1126 WebP quality 55"),
]

MANUAL_PARTS_EXCERPTS = [
	_manual_excerpt("excerpt.medieval-madness.lamp-locations", "PDF page 48, printed 2-47, complete lamp-location drawing", "lamp-locations.webp", "f34bac59454b880a290f57b2b84031db2dc611948f5fd4fe06f00e8e0598ba7f", "Medievel Madness Operations Manual.pdf page 48, crop box 0.05,0.03,0.95,0.95, scanned page rendered at its native resolution (embedded image xref 207, 2506px across 8.35in), rendered at 113 dpi, capped to 850px wide, 851x1142 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.switch-locations", "PDF page 50, printed 2-49, complete switch-location drawing", "switch-locations.webp", "45559aadeab71a9b71d82385b2a2993895a560041e78322f96055f34e7f41851", "Medievel Madness Operations Manual.pdf page 50, crop box 0.05,0.03,0.95,0.95, scanned page rendered at its native resolution (embedded image xref 215, 2506px across 8.35in), rendered at 113 dpi, capped to 850px wide, 851x1142 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.solenoid-locations", "PDF page 52, printed 2-51, complete solenoid/flashlamp-location drawing", "solenoid-locations.webp", "fbdc3ce1cc747d0757f4c5b76b9cba6856495dc073fc04f518748233f530ed78", "Medievel Madness Operations Manual.pdf page 52, crop box 0.05,0.03,0.95,0.95, scanned page rendered at its native resolution (embedded image xref 224, 2512px across 8.37in), rendered at 113 dpi, capped to 850px wide, 851x1142 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.lamp-matrix", "PDF page 53, printed 2-52, complete lamp matrix", "lamp-matrix.webp", "5e046f3f4c8a4ecdd39669408cb119da11afd5f20aafd1dd4c598ab12c60c9e8", "Medievel Madness Operations Manual.pdf page 53, crop box 0.05,0.03,0.95,0.92, scanned page rendered at its native resolution (embedded image xref 229, 2525px across 8.42in), rendered at 113 dpi, capped to 850px wide, 851x1105 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.switch-matrix", "PDF page 54, printed 2-53, complete switch matrix", "switch-matrix.webp", "bf14d870d39f1dc79cdd3a61d4e183b9291ec29eb126601bcbc5832f0de62a09", "Medievel Madness Operations Manual.pdf page 54, crop box 0.05,0.03,0.95,0.92, scanned page rendered at its native resolution (embedded image xref 234, 2512px across 8.37in), rendered at 113 dpi, capped to 850px wide, 851x1105 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.solenoid-table", "PDF page 55, printed 2-54, complete solenoid/flasher table", "solenoid-table.webp", "53f52b1158200f0fc0ff2136be2eaa2b6696bc02719d5d27b3611943e031abef", "Medievel Madness Operations Manual.pdf page 55, crop box 0.05,0.03,0.95,0.92, scanned page rendered at its native resolution (embedded image xref 238, 2500px across 8.33in), rendered at 93 dpi, capped to 700px wide, 701x911 WebP quality 45"),
]

MANUAL_SCHEMATICS_EXCERPTS = [
	_manual_excerpt("excerpt.medieval-madness.switch-matrix-circuit", "PDF page 2, printed 3-2, switch matrix and CPU-board circuit", "switch-matrix-circuit.webp", "1b1c57b126e0dd12120106d010948938270042aee34abbc931434f81538bb915", "Medieval_Madness_3_OPS.pdf page 2, crop box 0.04,0.03,0.96,0.95, scanned page rendered at its native resolution (embedded image xref 5, 2569px across 8.56in), rendered at 109 dpi, capped to 850px wide, 851x1101 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.solenoid-wiring", "PDF page 6, printed 3-6, controlled-solenoid wiring", "solenoid-wiring.webp", "6847df1b8243f107b496e1eab41ee29ad9a8151527fce82eb5e68ebedec27adb", "Medieval_Madness_3_OPS.pdf page 6, crop box 0.04,0.03,0.96,0.95, scanned page rendered at its native resolution (embedded image xref 24, 2562px across 8.54in), rendered at 109 dpi, capped to 850px wide, 851x1101 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.general-illumination-circuit", "PDF page 10, printed 3-10, general-illumination circuit", "general-illumination-circuit.webp", "255c8e8b63a035a8c7fe1339526a23a24dc7d05b90fee8ceb4d6bf04b9126725", "Medieval_Madness_3_OPS.pdf page 10, crop box 0.04,0.03,0.96,0.95, scanned page rendered at its native resolution (embedded image xref 42, 2562px across 8.54in), rendered at 109 dpi, capped to 850px wide, 851x1101 WebP quality 55"),
	_manual_excerpt("excerpt.medieval-madness.flipper-circuit", "PDF page 11, printed 3-11, complete four-flipper circuit", "flipper-circuit.webp", "fca9e5f01188313f3bf201fc39b352aa6944eb1c38e8cca0d4010c1abcfc8124", "Medieval_Madness_3_OPS.pdf page 11, crop box 0.04,0.03,0.96,0.95, scanned page rendered at its native resolution (embedded image xref 47, 2562px across 8.54in), rendered at 109 dpi, capped to 850px wide, 851x1101 WebP quality 55"),
]

EXTRACTION_RELATIVE_PATH = Path("williams/medieval-madness-1997/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/medieval-madness-1997/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "2f5a08bb9ce459a90934b3999e6ee96b15b4885f5a07dee8681c1f2b3ca50442"
EXTRACTION_FILE_COUNT = 2793
EXTRACTION_TOTAL_BYTES = 1073881024

TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=2164.706"

DRIVER_IDS = ("mm_05", "mm_10", "mm_109", "mm_109b", "mm_109c", "mm_10pfx", "mm_10u")
DRIVER_COMPATIBILITY = {
	"mm_05": (
		"identical",
		"Williams 0.50 prototype game ROM for the same physical Medieval Madness machine; the "
		"switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged.",
	),
	"mm_10": (
		"identical",
		"Williams production 1.0 game ROM shipped with the physical machine and printed on the "
		"operations-manual power-up example (project 559, EPROM 1.0).",
	),
	"mm_109": (
		"identical",
		"Williams 1.09 home-machine game ROM; a later firmware revision of the same physical "
		"machine with no controller-address or playfield change.",
	),
	"mm_109b": (
		"identical",
		"Williams 1.09B home-machine coin-play game ROM. This is the driver the retained known-"
		"working VPW table binds to, and it drives the identical I/O inventory as 1.0.",
	),
	"mm_109c": (
		"identical",
		"Williams 1.09C home-machine game ROM with the profanity speech calls restored; speech "
		"content only, with no hardware or address difference.",
	),
	"mm_10pfx": (
		"compatible",
		"1.0 game ROM re-released by Zen Studios for Pinball FX with modified display text only. "
		"It is a WPC-95 game ROM image for the same physical machine, not a separate product; the "
		"physical playfield, controller generation, and every controller address are unchanged.",
	),
	"mm_10u": (
		"compatible",
		"1.0 game ROM re-released by Global VR for the Ultrapin cabinet with modified display text "
		"only. It is a WPC-95 game ROM image for the same physical machine; the physical playfield, "
		"controller generation, and every controller address are unchanged.",
	),
}

# --- Printed switch matrix (manual page 2-53). First digit is the drive column,
# --- second digit is the return row.
SWITCH_LABELS = {
	11: "Launch Ball", 12: "Catapult Target", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Troll Target", 16: "Left Outlane", 17: "Right Return Lane", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed", 25: "Right Troll Target",
	26: "Left Return Lane", 27: "Right Outlane", 28: "Right Eject",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Left Popper", 37: "Castle Gate", 38: "Catapult",
	41: "Moat Enter", 44: "Castle Lock", 45: "Left Troll (Under Playfield)",
	46: "Right Troll (Under Playfield)", 47: "Left Top Lane", 48: "Right Top Lane",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Left Jet Bumper",
	54: "Bottom Jet Bumper", 55: "Right Jet Bumper", 56: "Drawbridge Up",
	57: "Drawbridge Down", 58: "Tower Exit",
	61: "Left Ramp Enter", 62: "Left Ramp Exit", 63: "Right Ramp Enter", 64: "Right Ramp Exit",
	65: "Left Loop Low", 66: "Left Loop High", 67: "Right Loop Low", 68: "Right Loop High",
	71: "Right Bank Top", 72: "Right Bank Middle", 73: "Right Bank Bottom",
	74: "Left Troll Up", 75: "Right Troll Up",
}

# Printed optos, shaded "OPTO, TYPICALLY CLOSED" on the matrix page. PinMAME's
# mmGameData inverts exactly column 3 rows 1-7 (0x7f) and column 4 row 1 (0x01).
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 41}
# vpmTimer.PulseSw / momentary-target callers in the retained VPW script.
PULSED_SWITCHES = {12, 15, 25, 31, 37, 41, 44, 45, 46, 51, 52, 53, 54, 55, 71, 72, 73}

SWITCH_TYPES = {
	11: "button", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch",
	24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	38: "microswitch", 44: "microswitch", 45: "microswitch", 46: "microswitch",
	47: "microswitch", 48: "microswitch", 51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf",
	55: "leaf", 56: "microswitch", 57: "microswitch", 58: "microswitch", 61: "microswitch",
	62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch",
	66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "microswitch",
	72: "microswitch", 73: "microswitch", 74: "microswitch", 75: "microswitch",
}

SWITCH_PARTS = {
	11: ("20-9663-B-4", None), 12: ("A-21990-4", None), 13: ("20-9663-16", None),
	14: (None, "04-10346"), 15: ("A-18530-6", None),
	16: ("A-17813", "5647-12693-19"), 17: ("A-17813", "5647-12693-19"),
	18: ("A-17791", "5647-12693-32"), 21: ("A-17238", None), 22: (None, "5643-09268-00"),
	24: (None, "5643-15190-00"), 25: ("A-18530-6", None),
	26: ("A-17813", "5647-12693-19"), 27: ("A-17813", "5647-12693-19"),
	28: ("A-21970", "5647-12693-43"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16908 LED with A-16909 photo transistor", None),
	37: ("A-16908 LED with A-16909 photo transistor", None),
	38: ("A-14947-1", "5647-12133-12"),
	41: ("A-16908 LED with A-16909 photo transistor", None),
	44: ("A-21800", "5647-12693-67"), 45: ("A-21724", "A-21743"), 46: ("A-21724", "A-21743"),
	47: ("A-17813", "5647-12693-19"), 48: ("A-17813", "5647-12693-19"),
	51: ("A-17800 kick with A-17794 score", "SW-1A-114 kick, SW-1A-120 score"),
	52: ("A-17800 kick with A-17794 score", "SW-1A-114 kick, SW-1A-120 score"),
	53: ("A-12030-3", "A-16443-1"), 54: ("A-12030-3", "A-16443-1"), 55: ("A-12030-3", "A-16443-1"),
	56: ("A-22036", "5647-12693-11"), 57: (None, "5647-12693-11"),
	58: ("A-21734", "5647-12693-06"),
	61: ("A-21799", "5647-12693-11"), 62: ("A-21821", "5647-12693-13"),
	63: ("A-21777", "5647-12693-11"), 64: ("A-21820", "5647-12693-13"),
	65: ("A-17813", "5647-12693-19"), 66: ("A-17813", "5647-12693-19"),
	67: ("A-21737", "5647-12693-36"), 68: ("A-17813", "5647-12693-19"),
	71: ("A-21576-4", None), 72: ("A-21576-4", None), 73: ("A-21576-4", None),
	74: ("A-22034", "5647-12693-11"), 75: ("A-22034", "5647-12693-11"),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-White", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("Fourth Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed solenoid/flasher table (Section 1 front matter and manual page 2-54).
SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Trough Eject", 3: "Left Popper", 4: "Castle",
	5: "Castle Gate Power", 6: "Castle Gate Hold", 7: "Knocker", 8: "Catapult",
	9: "Right Eject", 10: "Left Slingshot", 11: "Right Slingshot", 12: "Left Jet Bumper",
	13: "Bottom Jet Bumper", 14: "Right Jet Bumper", 15: "Tower Diverter Power",
	16: "Tower Diverter Hold", 17: "Left Side Low Flashers", 18: "Left Ramp Flashers",
	19: "Left Side High Flashers", 20: "Right Side High Flashers", 21: "Right Ramp Flashers",
	22: "Castle Right Side Flashers", 23: "Right Side Low Flashers", 24: "Moat Flashers",
	25: "Castle Left Side Flashers", 26: "Tower Lock Post", 27: "Right Gate", 28: "Left Gate",
	33: "Left Troll Power", 34: "Left Troll Hold", 35: "Right Troll Power",
	36: "Right Troll Hold", 37: "Drawbridge Motor",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	38: "Unused WPC-95 LPDC Output 38",
	39: "Unused WPC-95 LPDC Output 39",
	40: "Unused WPC-95 LPDC Output 40",
	41: "Drawbridge Motor LPDC Mirror",
	42: "Unused WPC-95 LPDC Mirror 42",
	43: "Unused WPC-95 LPDC Mirror 43",
	44: "Unused WPC-95 LPDC Mirror 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}

# address -> (drive wire, drive connection, driver transistor, power connection,
#             coil/flashlamp part, printed solenoid type)
SOLENOID_WIRING = {
	1: ("VIO-BRN", "J116-1", "Q72", "J133-2", "AE-23-800", "High Power"),
	2: ("VIO-RED", "J116-2", "Q68", "J133-2", "AE-26-1500", "High Power"),
	3: ("VIO-ORG", "J116-4", "Q71", "J133-2", "AE-26-1200", "High Power"),
	4: ("VIO-YEL", "J116-5", "Q67", "J133-2", "AE-26-1500", "High Power"),
	5: ("VIO-GRN", "J116-6", "Q70", "J133-2", "A-20099", "High Power"),
	6: ("VIO-BLU", "J116-7", "Q66", None, None, "High Power"),
	7: ("VIO-BLK", "J116-8", "Q69", "J133-2", "AE-23-800", "High Power"),
	8: ("VIO-GRY", "J116-9", "Q65", "J133-2", "AL-23-800", "High Power"),
	9: ("BRN-BLK", "J113-1", "Q44", "J133-3", "AE-27-1200", "Low Power"),
	10: ("BRN-RED", "J113-3", "Q48", "J133-3", "AE-26-1200", "Low Power"),
	11: ("BRN-ORG", "J113-4", "Q43", "J133-3", "AE-26-1200", "Low Power"),
	12: ("BRN-YEL", "J113-5", "Q47", "J133-3", "AE-26-1200", "Low Power"),
	13: ("BRN-GRN", "J113-6", "Q42", "J133-3", "AE-26-1200", "Low Power"),
	14: ("BRN-BLU", "J113-7", "Q46", "J133-3", "AE-26-1200", "Low Power"),
	15: ("BRN-VIO", "J113-8", "Q41", "J133-3", "A-20099", "Low Power"),
	16: ("BRN-GRY", "J113-9", "Q45", None, None, "Low Power"),
	17: ("BLK-BRN", "J111-1", "Q28", "J133-6", "#906", "Flasher"),
	18: ("BLK-RED", "J111-2", "Q32", "J133-6", "#89", "Flasher"),
	19: ("BLK-ORG", "J111-3", "Q27", "J133-6", "#906", "Flasher"),
	20: ("BLK-YEL", "J111-4", "Q31", "J133-6", "#906", "Flasher"),
	21: ("BLU-GRN", "J111-5", "Q26", "J133-6", "#906 and #89", "Flasher"),
	22: ("BLU-BLK", "J111-6", "Q30", "J133-6", "#906", "Flasher"),
	23: ("BLU-VIO", "J111-7", "Q25", "J133-6", "#906 and #89", "Flasher"),
	24: ("BLU-GRY", "J111-8", "Q29", "J133-6", "#89", "Flasher"),
	25: ("BLU-BRN", "J109-1", "Q16", "J133-6", "#906", "Gen. Purpose"),
	26: ("BLU-RED", "J109-2", "Q15", "J133-1", "AE-27-1200", "Gen. Purpose"),
	27: ("BLU-ORG", "J109-3", "Q14", "J133-1", "A-14406", "Gen. Purpose"),
	28: ("BLU-YEL", "J109-4", "Q13", "J133-1", "A-14406", "Gen. Purpose"),
	33: ("YEL-VIO", "J120-6", "Q84", "J119-6", "FL-11753", "Fliptronic power"),
	34: ("ORG-VIO", "J120-4", "Q86", "J119-6", "FL-11753", "Fliptronic hold"),
	35: ("YEL-GRY", "J120-3", "Q81", "J119-8", "FL-11753", "Fliptronic power"),
	36: ("ORG-GRY", "J120-1", "Q83", "J119-8", "FL-11753", "Fliptronic hold"),
	37: ("BRN-WHT", "J110-1", "U3A and U3B", "J139-2", "14-8015", "Low Power motor"),
	45: ("YEL-GRN", "J120-13", "Q90", "J119-1", "FL-11629", "Fliptronic power"),
	46: ("ORG-GRN", "J120-11", "Q92", "J119-1", "FL-11629", "Fliptronic hold"),
	47: ("YEL-BLU", "J120-9", "Q87", "J119-4", "FL-11629", "Fliptronic power"),
	48: ("ORG-BLU", "J120-7", "Q89", "J119-4", "FL-11629", "Fliptronic hold"),
}
# Manual pages 2-23 through 2-37 document a July 21, 1997 production change. The device-level
# coil and switch part numbers are unchanged; only the enclosing assembly differs, so both are
# recorded rather than silently assuming the later build.
PRODUCTION_SPLIT = {
	"A-21712-5": ("A-21712-2", "Up Down Post Assembly"),
	"A-22027": ("A-21733", "Popper Assembly"),
	"A-22034": ("A-21719", "Troll Assembly"),
	"A-22033": ("A-21723", "Drawbridge/Gate Assembly"),
	"A-22036": ("A-21976", "Switch/Bracket Assembly"),
}
PRODUCTION_SPLIT_NOTE = (
	" Production split: games produced before July 21, 1997 use {early} ({name}) instead of {late}; the manual "
	"shows the same coil and switch part numbers in both assemblies, so only the enclosing assembly differs."
)

SOLENOID_ASSEMBLIES = {
	1: "A-21553-1", 2: "A-19963-1", 3: "A-22027", 4: "A-21718", 5: "A-22033", 6: "A-22033",
	7: "B-10686-1", 8: "A-14947-1", 9: "A-21970", 10: "B-9362-L-2", 11: "B-9362-R-3",
	12: "A-9415-3", 13: "A-9415-3", 14: "A-9415-2", 15: "A-21706", 16: "A-21706",
	18: "A-17983", 21: "A-17802 with A-17983", 23: "A-17983", 24: "A-17803",
	26: "A-21712-5", 27: "A-17796", 28: "A-17796-1",
	33: "A-22034", 34: "A-22034", 35: "A-22034", 36: "A-22034", 37: "A-22033",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
# Retained VPW script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "AutoPlunger (Plunger.Fire)", 2: "SolBallRelease (pulses switch 31 and kicks the trough-exit ball)",
	3: "SolMoat", 4: "SolCastle", 5: "SolCastlegatePow", 6: "SolCastlegateHold",
	7: 'vpmSolSound SoundFX("fx_Knocker", DOFKnocker)', 8: "SolCatapult", 9: "SolMerlin",
	15: "SolTowerDivPow", 16: "SolTowerDivHold",
	17: "SolMod17", 18: "SolMod18", 19: "SolMod19", 20: "SolMod20", 21: "SolMod21",
	22: "SolMod22", 23: "SolMod23", 24: "SolMod24", 25: "SolMod25",
	26: "SolTowerLock", 27: "gate3.open", 28: "gate2.open",
	33: "SolLeftTrollPow", 34: "SolLeftTrollHold", 35: "SolRightTrollPow", 36: "SolRightTrollHold",
	37: "SolDrawBridge",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
}
# Manual solenoid/flasher table addresses that differ from the PinMAME public address.
MANUAL_SOLENOID_ALIASES = {41: "37", 45: "29", 46: "30", 47: "31", 48: "32"}

FLASHER_BULBS = {
	17: ("#906 (1) playfield and #906 (1) insert panel", 2, 1),
	18: ("#89 (1) playfield and #906 (1) insert panel", 2, 1),
	19: ("#906 (1) playfield and #906 (1) insert panel", 2, 1),
	20: ("#906 (1) playfield and #906 (1) insert panel", 2, 1),
	21: ("#906 (1) and #89 (1), both on the playfield", 2, 2),
	22: ("#906 (2): one on the playfield and one on the back panel (A-20158)", 2, 2),
	23: ("#906 (1) and #89 (1), both on the playfield", 2, 2),
	24: ("#89 (2), both on the playfield", 2, 2),
	25: ("#906 (2): one on the playfield and one on the back panel (A-20158)", 2, 2),
}

# --- Printed lamp matrix (manual page 2-52). First digit is the drive column.
LAMP_LABELS = {
	11: "Right Bank Top", 12: "Right Bank Middle", 13: "Right Bank Bottom",
	14: "Right Ramp Jackpot", 15: "Save the Damsel!", 16: "Dragon Death",
	17: "Dragon Snack", 18: "Dragon Breath",
	21: "Right Loop Jackpot", 22: "Right Joust Victory!", 23: "Right Clash!",
	24: "Right Charge!", 25: "Patron of the Peasants", 26: "Catapult Ace",
	27: "Joust Champion", 28: "Castle Crusher",
	31: "Trolls!", 32: "Extra Ball", 33: "Merlin's Magic", 34: "Troll Madness",
	35: "Damsel Madness", 36: "Peasant Madness", 37: "Catapult Madness", 38: "Joust Madness",
	41: "Left Loop Jackpot", 42: "Left Joust Victory!", 43: "Left Clash!", 44: "Left Charge!",
	45: "Catapult Jackpot", 46: "Catapult Slam!", 47: "BAM!", 48: "WAM!",
	51: "Center Arrow", 52: "Battle for the Kingdom", 53: "Master of Trolls",
	54: "Defender of Damsels", 55: "Left Top Lane", 56: "Right Top Lane",
	57: "Left Troll Target", 58: "Right Troll Target",
	61: "Francois D'Grimm", 62: "King of Payne", 63: "Earl of Ego", 64: "Left Ramp Jackpot",
	65: "Revolting Peasants!", 66: "Ugly Riot!", 67: "Angry Mob!", 68: "Rabble Rouser",
	71: "Howard Hurtz", 72: "Magic Shield", 73: "Sir Psycho", 74: "Duke of Bourbon",
	75: "Castle Lock 2", 76: "Castle Lock 1", 77: "Super Jackpot", 78: "Super Jets",
	81: "Right Outlane", 82: "Right Return", 83: "Left Return", 84: "Left Outlane",
	85: "Castle Lock 3", 86: "Shoot Again", 87: "Launch Button", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-21322", "#555"), 12: ("A-21322", "#555"), 13: ("A-21322", "#555"),
	14: ("A-21738", "#555"), 15: ("A-21738", "#555"), 16: ("A-21738", "#555"),
	17: ("A-21738", "#555"), 18: ("A-21738", "#555"),
	21: ("A-21740", "#555"), 22: ("A-21740", "#555"), 23: ("A-21740", "#555"),
	24: ("A-21740", "#555"), 25: ("A-21740", "#555"), 26: ("A-21740", "#555"),
	27: ("A-21740", "#555"), 28: ("A-21740", "#555"),
	31: ("A-21322", "#555"), 32: ("A-21322", "#555"), 33: ("A-21322", "#555"),
	34: ("A-21738", "#555"), 35: ("A-21738", "#555"), 36: ("A-21738", "#555"),
	37: ("A-21738", "#555"), 38: ("A-21738", "#555"),
	41: ("A-21740", "#555"), 42: ("A-21740", "#555"), 43: ("A-21740", "#555"),
	44: ("A-21740", "#555"), 45: ("A-21740", "#555"), 46: ("A-21740", "#555"),
	47: ("A-21740", "#555"), 48: ("A-21740", "#555"),
	51: ("A-21741", "#555"), 52: ("A-21741", "#555"), 53: ("A-21741", "#555"),
	54: ("A-21741", "#555"), 55: ("A-17807", "#44"), 56: ("A-17807", "#44"),
	57: ("A-17835", "#44"), 58: ("A-17835", "#44"),
	61: ("A-21739", "#555"), 62: ("A-21739", "#555"), 63: ("A-21739", "#555"),
	64: ("A-21738", "#555"), 65: ("A-21738", "#555"), 66: ("A-21738", "#555"),
	67: ("A-21738", "#555"), 68: ("A-21738", "#555"),
	71: ("A-21739", "#555"), 72: ("A-21739", "#555"), 73: ("A-21739", "#555"),
	74: ("A-21739", "#555"), 75: ("A-21551", "#555"), 76: ("A-21551", "#555"),
	77: ("A-21551", "#555"), 78: ("A-17807", "#44"),
	81: ("A-17835", "#44"), 82: ("A-17807", "#44"), 83: ("A-17835", "#44"),
	84: ("A-17807", "#44"), 85: ("A-21551", "#555"), 86: ("A-17087", "#44"),
	87: ("20-9663-B-4", None), 88: ("20-9663-16", None),
}
LAMP_QUANTITIES = {15: 2, 78: 2}
LAMP_PARTS_LIST_ALIASES = {72: "Ball Save"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
	3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Black", "J121-4", "Q99"),
	5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
	3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
	5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}

GI_STRINGS = {
	0: ("GI 1: Bottom Playfield", "WHT-BRN", "J106-7 and J105-7", "Q5", "J106-1 and J105-1", "#44 playfield and #555 insert"),
	1: ("GI 2: Middle Playfield", "WHT-ORG", "J105-8", "Q4", "J105-2", "#555"),
	2: ("GI 3: Top Playfield", "WHT-YEL", "J105-9", "Q3", "J105-3", "#555"),
	3: ("GI 4: Top Insert Panel", "WHT-GRN", "J106-10", "Q2", "J106-5", "#44"),
	4: ("GI 5: Bottom Insert Panel", "WHT-VIO", "J106-11 and J104-1", "Q1", "J106-6 and J104-3", "#44"),
}

# --- Normalized playfield coordinates derived from the retained VPW extraction.
SWITCH_POSITIONS = {
	12: [(0.044497, 0.440324)],
	15: [(0.374538, 0.2958)],
	16: [(0.041885, 0.732946)],
	17: [(0.790909, 0.731308)],
	18: [(0.941317, 0.887067)],
	25: [(0.534228, 0.319731)],
	26: [(0.110723, 0.731794)],
	27: [(0.865265, 0.733054)],
	28: [(0.606507, 0.287617)],
	31: [(0.848299, 0.870845)],
	32: [(0.848299, 0.870845)],
	33: [(0.780027, 0.888315)],
	34: [(0.707974, 0.907238)],
	35: [(0.476499, 0.963929)],
	36: [(0.112877, 0.230188)],
	37: [(0.4115, 0.177532)],
	38: [(0.05481, 0.589209)],
	41: [(0.425272, 0.23607)],
	44: [(0.276134, 0.178223)],
	45: [(0.370421, 0.431755)],
	46: [(0.544393, 0.43341)],
	47: [(0.710829, 0.11117)],
	48: [(0.805768, 0.113888)],
	51: [(0.213817, 0.722145)],
	52: [(0.691201, 0.721891)],
	53: [(0.648947, 0.227865)],
	54: [(0.815892, 0.272794)],
	55: [(0.82789, 0.189357)],
	56: [(0.407158, 0.190101)],
	57: [(0.407158, 0.190101)],
	58: [(0.9025, 0.037218)],
	61: [(0.142159, 0.274993)],
	62: [(0.591394, 0.045772)],
	63: [(0.747796, 0.331868)],
	64: [(0.666319, 0.215881)],
	65: [(0.071826, 0.329715)],
	66: [(0.220881, 0.075204)],
	67: [(0.811142, 0.439865)],
	68: [(0.942997, 0.171502)],
	71: [(0.8111, 0.538891)],
	72: [(0.816567, 0.565365)],
	73: [(0.823525, 0.592276)],
	74: [(0.370421, 0.431755)],
	75: [(0.544393, 0.43341)],
}
# Switch addresses whose coordinate is an explicit projection onto a documented
# assembly anchor rather than a directly named table object for that switch.
SWITCH_PROJECTIONS = {
	31: "Projected onto the trough-exit ball position: the retained script's SolBallRelease pulses switch 31 and kicks the same trough-exit ball, and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.",
	56: "Projected onto the retained drawbridge door assembly; the manual marks switch 56 as a hidden (dashed) position inside the drawbridge mechanism.",
	57: "Projected onto the retained drawbridge door assembly; the manual marks switch 57 as a hidden (dashed) position inside the drawbridge mechanism.",
	74: "Projected onto the left troll strike surface; the physical position switch is under the playfield inside troll assembly A-22034.",
	75: "Projected onto the right troll strike surface; the physical position switch is under the playfield inside troll assembly A-22034.",
}

SOLENOID_POSITIONS = {
	1: [(0.940614, 0.950299)],
	2: [(0.848299, 0.870845)],
	3: [(0.112877, 0.230188)],
	4: [(0.39982, 0.142162)],
	5: [(0.410651, 0.166828)],
	6: [(0.410651, 0.166828)],
	8: [(0.05481, 0.589209)],
	9: [(0.606507, 0.287617)],
	10: [(0.213817, 0.722145)],
	11: [(0.691201, 0.721891)],
	12: [(0.648947, 0.227865)],
	13: [(0.815892, 0.272794)],
	14: [(0.82789, 0.189357)],
	15: [(0.839987, 0.171083)],
	16: [(0.839987, 0.171083)],
	17: [(0.042197, 0.414609)],
	18: [(0.191355, 0.29454)],
	19: [(0.097228, 0.032771)],
	20: [(0.95151, 0.126212)],
	21: [(0.726333, 0.362813), (0.77214, 0.353211)],
	22: [(0.545235, 0.070608), (0.514696, 0.015555)],
	23: [(0.933126, 0.532879), (0.870953, 0.485226)],
	24: [(0.426483, 0.221157), (0.373418, 0.224618)],
	25: [(0.167981, 0.134287), (0.249416, 0.015858)],
	26: [(0.873591, 0.042871)],
	27: [(0.883313, 0.080814)],
	28: [(0.61807, 0.029929)],
	33: [(0.370421, 0.431755)],
	34: [(0.370421, 0.431755)],
	35: [(0.544393, 0.43341)],
	36: [(0.544393, 0.43341)],
	37: [(0.407158, 0.190101)],
	45: [(0.617799, 0.846535)],
	46: [(0.617799, 0.846535)],
	47: [(0.286271, 0.846535)],
	48: [(0.286271, 0.846535)],
}

LAMP_POSITIONS = {
	11: [(0.766962, 0.555222)], 12: [(0.774368, 0.582621)], 13: [(0.778956, 0.609538)],
	14: [(0.65061, 0.480978)], 15: [(0.620378, 0.52432)], 16: [(0.594909, 0.55314)],
	17: [(0.575101, 0.581968)], 18: [(0.55633, 0.609793)],
	21: [(0.786823, 0.461602)], 22: [(0.746153, 0.506251)], 23: [(0.715031, 0.537803)],
	24: [(0.683415, 0.56669)], 25: [(0.454437, 0.43944)], 26: [(0.439376, 0.473752)],
	27: [(0.425411, 0.507282)], 28: [(0.415952, 0.540218)],
	31: [(0.592505, 0.330009)], 32: [(0.57914, 0.355282)], 33: [(0.571247, 0.382915)],
	34: [(0.531476, 0.473255)], 35: [(0.519718, 0.50254)], 36: [(0.504885, 0.533386)],
	37: [(0.491597, 0.564627)], 38: [(0.475277, 0.596373)],
	41: [(0.11446, 0.401202)], 42: [(0.14842, 0.442524)], 43: [(0.177816, 0.473751)],
	44: [(0.203568, 0.504699)], 45: [(0.136695, 0.533002)], 46: [(0.176334, 0.574965)],
	47: [(0.212952, 0.606598)], 48: [(0.247888, 0.63429)],
	51: [(0.438052, 0.282428)], 52: [(0.459103, 0.336712)], 53: [(0.456008, 0.37205)],
	54: [(0.453477, 0.40588)], 55: [(0.709935, 0.063859)], 56: [(0.80576, 0.066222)],
	57: [(0.389056, 0.333782)], 58: [(0.52081, 0.357684)],
	61: [(0.55812, 0.718023)], 62: [(0.450291, 0.709688)], 63: [(0.344681, 0.718482)],
	64: [(0.257189, 0.437356)], 65: [(0.286267, 0.48002)], 66: [(0.307585, 0.511615)],
	67: [(0.326789, 0.539182)], 68: [(0.344201, 0.568316)],
	71: [(0.549745, 0.741946)], 72: [(0.449165, 0.742523)], 73: [(0.351392, 0.742234)],
	74: [(0.450918, 0.783538)], 75: [(0.3259, 0.320774)], 76: [(0.336581, 0.349444)],
	77: [(0.346432, 0.373798)], 78: [(0.931585, 0.2384), (0.042351, 0.19035)],
	81: [(0.862691, 0.69687)], 82: [(0.78771, 0.679044)], 83: [(0.116837, 0.680035)],
	84: [(0.040232, 0.696606)], 85: [(0.313473, 0.290786)], 86: [(0.451814, 0.877963)],
}

GI_POSITIONS = {
	0: [
		(0.203969, 0.821206), (0.137419, 0.800838), (0.200015, 0.756729),
		(0.165982, 0.713656), (0.699396, 0.820943), (0.765182, 0.800861),
		(0.703393, 0.75675), (0.737161, 0.713551), (0.881421, 0.599869),
		(0.873614, 0.54413),
	],
	1: [
		(0.648064, 0.227403), (0.815776, 0.272126), (0.880672, 0.446492),
		(0.784509, 0.37042), (0.683576, 0.366436), (0.669893, 0.331835),
		(0.537374, 0.275925), (0.26009, 0.310115), (0.228199, 0.275465),
		(0.13851, 0.315759), (0.114416, 0.286223), (0.025624, 0.388991),
	],
	2: [
		(0.099954, 0.176988), (0.161686, 0.115649), (0.08124, 0.0754),
		(0.321112, 0.087457), (0.358828, 0.024513), (0.506036, 0.064942),
		(0.77641, 0.018694), (0.663871, 0.106625), (0.756841, 0.110016),
		(0.854872, 0.111452), (0.827139, 0.189865),
	],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Medieval Madness retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Medieval Madness extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Medieval Madness retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Medieval Madness retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Medieval Madness retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


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


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the mm_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/mm.c switch/solenoid defines, mmGameData GEN_WPC95 with wpc_dispDMD, "
				"FLIP_SW(FLIP_L|FLIP_U) with FLIP_SOL(FLIP_L), the inverted-switch mask 0x7f on column 3 and 0x01 "
				"on column 4, wpc_set_fastflip_addr(0x81), and mm_handleMech drawbridge/troll handling; "
				"src/wpc/core.h WPC solenoid numbering and WPC_swF1..WPC_swF8; src/wpc/core.c core_getSol WPC95 "
				"37..40 to 41..44 duplication; src/wpc/wpc.c WPC_FLIPPERSW95 inversion and the J111/fast-flip "
				"game-on state; src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95=0x80"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-95.json",
			"revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.medieval-madness.1997/archive-arcademanual_Medieval_Madness_1_OPS/Medieval_Madness_1_OPS.pdf",
			"original_filename": "Medieval_Madness_1_OPS.pdf",
			"sha256": MANUAL_PART1_SHA256,
			"locator": (
				"Manifest ID archive.arcademanual_Medieval_Madness_1_OPS.williams.medieval-madness.1997.57d3b23e0d73; "
				"89-page image-only scan of Williams operations manual 16-50059-101 (July 1997 FINAL) front matter and "
				"Section 1. Rendered page 2 carries the DIP-switch chart and the complete solenoid/flasher, general-"
				"illumination, flipper-circuit, and motor-circuit wiring table. Rendered pages 4-5 carry the security-CPU "
				"and coin-door interlock notices. Printed pages 1-19 through 1-24 carry the T.16 loop/gate, T.17 tower, "
				"T.18 drawbridge, T.19 castle-gate, T.20 trolls, and T.21 empty-balls mechanism procedures."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": MANUAL_PART1_EXCERPTS,
		},
		{
			"id": MANUAL_PARTS_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.medieval-madness.1997/arcarc/Medievel%20Madness%20Operations%20Manual.pdf",
			"original_filename": "Medievel Madness Operations Manual.pdf",
			"sha256": MANUAL_ARCARC_SHA256,
			"locator": (
				"Manifest ID other.arcarc.williams.medieval-madness.1997.9baac8156b11; 57-page image-only scan of "
				"Section 2 Parts Information from the same manual. Printed page 2-46 is the lamp-locations parts list, "
				"2-47 the lamp-locations playfield map, 2-48 the switch-locations parts list, 2-49 the switch-locations "
				"playfield map, 2-50 the solenoid/flashlamp-locations parts list, 2-51 the solenoid/flashlamp playfield "
				"map, 2-52 the lamp matrix, 2-53 the switch matrix, and 2-54 the solenoid/flasher table. The equivalent "
				"Internet Archive copy of Section 2 is retained at "
				"external:pinmame-manuals/by-machine/williams.medieval-madness.1997/archive-arcademanual_Medieval_Madness_2_OPS/"
				f"Medieval_Madness_2_OPS.pdf with SHA-256 {MANUAL_PART2_SHA256}."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by Arcade Archive",
			"rights": "NOASSERTION",
			"excerpts": MANUAL_PARTS_EXCERPTS,
		},
		{
			"id": MANUAL_SCHEMATICS_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.medieval-madness.1997/archive-arcademanual_Medieval_Madness_3_OPS/Medieval_Madness_3_OPS.pdf",
			"original_filename": "Medieval_Madness_3_OPS.pdf",
			"sha256": MANUAL_PART3_SHA256,
			"locator": (
				"Manifest ID archive.arcademanual_Medieval_Madness_3_OPS.williams.medieval-madness.1997.1a426136cbc9; "
				"29-page image-only scan of Section 3 Wiring Diagrams and Schematics, including the switch-matrix and "
				"dedicated-switch circuits (3-2, 3-3), the lamp-matrix circuit (3-4), the solenoid/flashlamp circuit "
				"table and wiring (3-5 through 3-9), the general-illumination circuit (3-10), and the flipper circuit "
				"diagram (3-11)."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": MANUAL_SCHEMATICS_EXCERPTS,
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/medieval-madness-1997/manual-transcription.md",
			"revision": "2026-08-05",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/williams.medieval-madness.1997/. All "
				"four retained PDFs are image-only, so the OCR text under "
				"external:pinmame-review-artifacts/medieval-madness-1997/ocr/ is a search index only and never an authority."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/medieval-madness-1997/source/Medieval%20Madness%20(Williams%201997)%20VPW%20v1.0.vpx",
			"original_filename": "Medieval Madness (Williams 1997) VPW v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW v1.0 recreation of the physical machine (table version 1.0, save revision "
				f"941). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/952.941 and y/2164.706. "
				"Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW (Sixtoe, Tomate, Apophis, DaRDog, Mcarter, ClarkKent, Bord, CainArg, Freezy, HauntFreaks, MajorDrain, Tyson171, Niwak, Gedankekojote97, PinStratsDan and the testers named in the table description)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/medieval-madness-1997/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Retained embedded VPW script (211,084 bytes). Runtime and mechanism-causality authority: "
				'cGameName = "mm_109b", Const UseSolenoids = 2 (fast flips), Const UseLamps = 1 with vpmMapLights AllLamps, '
				"the SolCallback/SolModcallback table for solenoids 1-37 and core.vbs sLRFlipper/sLLFlipper, the "
				"Controller.Switch and vpmTimer.PulseSw switch semantics, the trough and drawbridge state machines, and "
				"the GiCallBack2 UpdateGI mapping of GI 0/1/2 to the GIB/GIM/GIT playfield emitter arrays."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/medieval-madness-1997/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are "
				f"{TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-roms/mm_10.zip",
			"sha256": ROM_SHA256,
			"locator": "Pre-existing authorized local ROM archive used only to boot the pinned harness; ROM bytes are never copied into this repository",
			"license": "NOASSERTION",
			"attribution": "Authorized local evidence",
		},
		{
			"id": RUNTIME_SOURCE,
			"kind": "runtime_scenario",
			"uri": "internal:evidence/runtime/wpc-95/medieval-madness-boot-start-and-service.json",
			"revision": PINMAME_REVISION,
			"locator": "Pinned LibPinMAME harness runs that boot mm_10, add credits, start a ball, and hold the coin-door service buttons with the coin door open",
			"license": "NOASSERTION",
			"attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
	]


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


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_component = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC-95 CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		refs = (MANUAL_PARTS_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		if address in {6, 7, 8}:
			refs = (MANUAL_PARTS_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE)
		if address < 5:
			notes = f"Printed dedicated grounded switch D{address}. {note}"
		else:
			notes = (
				f"Printed dedicated grounded switch D{address}. {note} PinMAME's MAME-only keyboard port "
				"(WPC_COMPORTS) labels these four service bits in the opposite order; that is a MAME key binding, not "
				"public address semantics. The pinned harness resolved the whole group: holding public switch 8 with "
				'the coin door open produced the ROM prompt "TO RESET SCORES- HOLD ENTER", pulsing public switch 7 '
				"raised the ROM's own VOLUME display from 12 to 15, and pulsing public switch 6 lowered it back to 12."
			)
			if address == 5:
				notes += (
					" Switch 5 is the remaining position in that group once 6, 7, and 8 are proven, and the printed "
					"matrix names it Service Credits / Escape."
				)
		items.append(
			_device(
				f"switch.cabinet-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"optional" if address == 4 else "used",
				refs,
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": notes},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_PARTS_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			assembly, part_number = SWITCH_PARTS.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
			notes = (
				f"Printed switch-matrix drive column {column}, return row {row}. T.13 in the operations manual states "
				"the notation directly: the number on the left is the column and the number on the right is the row."
			)
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			if address in OPTO_SWITCHES:
				notes += (
					" Printed as an opto that is typically closed; PinMAME's mmGameData inverted-switch mask covers it, "
					"so the public switch state is already normalized and must not be inverted again."
				)
			if address == 24:
				notes += (
					" Physical part 5643-15190-00 is a permanently closed link used to prove the matrix is connected. "
					"The retained VPW script initializes the controller-facing state to 0 at startup, which is a table "
					"simplification; a faithful recreation holds this input active."
				)
			if address == 22:
				notes += " Closed while the coin door is closed; the A-18249-3 interlock removes solenoid power when the door opens."
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if assembly in PRODUCTION_SPLIT:
				early, name = PRODUCTION_SPLIT[assembly]
				notes += PRODUCTION_SPLIT_NOTE.format(early=early, name=name, late=assembly)
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_PARTS_SOURCE)
				refs = (MANUAL_PARTS_SOURCE, CONTROLLER_SOURCE)
				label = f"Not Used Matrix Position {address}"
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_PARTS_SOURCE)
				refs = (MANUAL_PARTS_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				if address in PULSED_SWITCHES:
					extra["pulse"] = True
				refs = (MANUAL_PARTS_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {11, 13, 14, 21, 22}:
					role = {
						11: "cabinet.launch",
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_PARTS_SOURCE)
					physical["location"] = "cabinet" if address in {11, 13} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_PARTS_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316"),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" Medieval Madness has no upper flippers and the switch-locations parts list on manual page 2-48 marks "
				"F5 through F8 Not Used. The flipper circuit diagram on manual page 3-11 disagrees: it draws F6 and F8 as "
				"upper-flipper cabinet optos and labels F5 and F7 Basket Made Opto and Basket Hold, neither of which is a "
				"Medieval Madness device. That page is a reused Williams template, so the game-specific parts list governs "
				"and these four positions stay unused; the disagreement is recorded rather than resolved silently."
			)
			physical["location"] = "not installed"
		elif switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed. WPC-95 reads the flipper column through WPC_FLIPPERSW95 "
				"with a hardware inversion, so the public switch state is already normalized."
			)
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection},
		}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_PARTS_SOURCE)
			extra.pop("wiring")
		else:
			extra["normally_closed"] = bool(normally_closed)
			extra["spatial"] = not_applicable(
				"cabinet_or_service" if role.endswith(".button") else "internal_nonvisual",
				MANUAL_PARTS_SOURCE,
			)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_PARTS_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				**extra,
			)
		)

	dip_labels = {
		1: "CPU DIP 1 (country code bit)", 2: "CPU DIP 2 (country code bit)",
		3: "CPU DIP 3 (country code bit)", 4: "CPU DIP 4 (country code bit)",
		5: "CPU DIP 5 (country code bit)", 6: "CPU DIP 6 (country code bit)",
		7: "CPU DIP 7 (country code bit)", 8: "CPU DIP 8 (country code bit)",
	}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				dip_labels[address],
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-95 CPU board U27",
					"switch_type": "dip",
					"notes": (
						"Printed DIP-switch chart country settings: America Off Off On On On On On On; European "
						"Off Off On On On Off On On; French Off Off On On On On Off Off; German Off Off On On On On "
						"On Off; Spain Off Off On On Off On On On."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			drive_wire, drive_connection, transistor, power_connection, part_number, printed_type = SOLENOID_WIRING[address]
			kind = "flasher" if 17 <= address <= 25 else "motor" if address == 37 else "coil"
			physical: dict[str, Any] = {}
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher":
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" Only the playfield bulb has a playfield placement; the insert-panel bulb is backbox hardware "
						"behind the translite and is deliberately not given a playfield coordinate."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if address in {6, 16}:
				notes += " The hold winding shares the power feed of its power winding, so the printed table leaves its voltage connection blank."
			if address == 7:
				notes += " Backbox knocker; the printed table routes both its voltage and drive connections through the backbox."
			if address in {33, 34, 35, 36}:
				notes += (
					" Physically a troll up/down actuator wired to a Fliptronic upper-flipper circuit. PinMAME exposes it "
					"on the generic upper-flipper solenoid address, and mmGameData declares FLIP_SOL(FLIP_L) so the "
					"emulator never drives it as a flipper."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias."
				)
			if address == 37:
				notes += (
					" WPC-95 LPDC output; PinMAME duplicates it at public address 41, so a recreation must treat 37 and "
					"41 as one physical motor. The flipper circuit diagram on manual page 3-11 shows its supply as "
					"GRAY-YELLOW +12 V on J139-2."
				)
			if address in {33, 34, 35, 36, 45, 46, 47, 48}:
				notes += " Manual page 3-11 shows the flipper and troll circuits fed from the +50 V supply on J119."
			assembly = physical.get("assembly_part_number")
			if assembly in PRODUCTION_SPLIT:
				early, name = PRODUCTION_SPLIT[assembly]
				notes += PRODUCTION_SPLIT_NOTE.format(early=early, name=name, late=assembly)
			physical["notes"] = notes

			wiring: dict[str, Any] = {
				"board": "WPC-95 power driver board",
				"control_wire": drive_wire,
				"control_connection": drive_connection,
				"driver_transistor": transistor,
			}
			if power_connection:
				wiring["power_connection"] = power_connection
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_PARTS_SOURCE)
			else:
				role = "emitter" if kind == "flasher" else "effect"
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, MANUAL_PARTS_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, MANUAL_PARTS_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here. The pinned harness observed it active throughout attract mode; it is not a Medieval Madness playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Medieval Madness playfield device.",
			31: "PinMAME's synthetic game-on state. Medieval Madness sets wpc_set_fastflip_addr(0x81), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay. The pinned harness observed it active while a ball was in play and also in an attract-mode frame four seconds after the coin-door Enter button was released, so a recreation must not treat it as a ball-in-play indicator.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			38: "Unused WPC-95 LPDC general-purpose output; Medieval Madness populates only LPDC output 37.",
			39: "Unused WPC-95 LPDC general-purpose output; Medieval Madness populates only LPDC output 37.",
			40: "Unused WPC-95 LPDC general-purpose output; Medieval Madness populates only LPDC output 37.",
			41: "PinMAME's backward-compatibility mirror of LPDC output 37. It reports the same physical drawbridge motor and is not an additional device; the retained VPW script binds the motor on address 37.",
			42: "Unused WPC-95 LPDC mirror of output 38.",
			43: "Unused WPC-95 LPDC mirror of output 39.",
			44: "Unused WPC-95 LPDC mirror of output 40.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address == 41 else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in MANUAL_SOLENOID_ALIASES:
			virtual_aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if address in {29, 31} else (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=virtual_aliases,
				roles=roles,
				physical={"notes": notes},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"assembly_part_number": assembly, "quantity": LAMP_QUANTITIES.get(address, 1)}
			notes = (
				f"Printed lamp-matrix drive column {column}, return row {row}. T.13 in the operations manual states the "
				"notation directly and uses lamp 23 as its worked example of second column, third row."
			)
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += f" The printed lamp matrix and lamp-locations list both mark this address as driving {LAMP_QUANTITIES[address]} bulbs."
			if address == 15:
				notes += (
					" The printed lamp-locations map draws this as one large circular insert between the triangular 14 "
					"and the small rectangular 16, so the two bulbs share a single insert. The address therefore has "
					"one playfield placement and a physical quantity of two."
				)
			if address == 78:
				notes += (
					" The two bulbs are two separate arrow inserts, one in each orbit lane. The printed lamp-locations "
					"map numbers only the right-hand arrow but draws the matching left-hand arrow uncalled-out, and the "
					"retained table binds a separate emitter to each (l78 right, l78a left), so both are placed."
				)
			if address in LAMP_PARTS_LIST_ALIASES:
				notes += (
					f" The lamp-locations parts list calls the same insert {LAMP_PARTS_LIST_ALIASES[address]!r}; the "
					"printed lamp-matrix insert legend is used as the canonical label."
				)
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated launch/start button assembly."
			physical["notes"] = notes

			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": {
					"board": "WPC-95 power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in {87, 88}:
				extra["roles"] = ["cabinet.launch" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_PARTS_SOURCE)
			else:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					"used",
					(MANUAL_PARTS_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_wire, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		physical: dict[str, Any] = {"notes": ""}
		notes = f"Printed general-illumination string {address + 1:02d}; printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-95 power driver board",
				"control_wire": drive_wire,
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate come "
				"from the retained table's GI emitter array for this string. Manual page 3-10 shows the three playfield "
				"strings on the triac-switched circuit of its Figure 1, fed from the 6.3 V transformer secondary and "
				"bounded at up to 18 bulbs per string."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite. The printed table marks strings 04 and 05 as "
				"always on with no brighten or dim, and the retained script's UpdateGI handles only the three playfield "
				"strings, so this string has no playfield coordinate. The general-illumination circuit on manual page 3-10 "
				"shows why: all five strings run from the 6.3 V transformer secondary, but the three playfield strings use "
				"the triac-switched circuit of its Figure 1 while these two use the bridge-rectified circuit of its "
				"Figure 2, which cannot be dimmed. That page bounds every string at up to 18 bulbs but publishes no exact "
				"per-string count, and no parts page itemizes the insert-panel sockets, so the physical bulb count for "
				"this string is deliberately not asserted and has to be read from the machine."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(
			_device(
				identifier,
				label,
				"gi",
				"pinmame.output.gi",
				address,
				"used",
				(MANUAL_SOURCE, MANUAL_PARTS_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
				**extra,
			)
		)
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_PARTS_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_PARTS_SOURCE, RUNTIME_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(
		identifier: str,
		label: str,
		kind: str,
		actuators: list[str],
		sensors: list[str],
		behavior: str,
		positions: list[tuple[str, str, list[str], str]],
		*refs: str,
		assembly_part_number: str | None = None,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [
				{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
				for position_id, position_label, position_sensors, description in positions
			]
		return record

	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on opto pairs 32-35, with Trough Ball 1 (32) at the eject end nearest the shooter lane and "
			"Trough Ball 4 (35) at the drain entrance. The drain feeds switch 35 and the retained script re-stacks balls "
			"toward 32 on a 300 ms settle timer. Solenoid 2 ejects the ball resting on 32 into the shooter lane and the "
			"same event asserts trough-eject opto 31. All five positions are printed optos that rest closed, and PinMAME "
			"normalizes them, so a recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto at the trough exit, asserted as the ball leaves."),
			],
			VPX_SCRIPT_SOURCE,
			MANUAL_PARTS_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"Medieval Madness has no manual plunger. The ball ejected from the trough rests on shooter-lane switch 18 and "
			"auto-plunger coil 1 launches it when the cabinet Launch Ball button (switch 11) is pressed. The retained "
			"script's AutoPlunger callback fires the plunger and plays the saucer-kick sound at switch 18.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			VPX_SCRIPT_SOURCE,
			MANUAL_PARTS_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-21553-1",
		),
		mechanism(
			"mechanism.drawbridge",
			"Motorized castle drawbridge",
			"motorized",
			[output_id("Drawbridge Motor")],
			["switch.matrix-56", "switch.matrix-57"],
			"A continuously rotating low-power motor on LPDC output 37 (mirrored by PinMAME at 41) drives the drawbridge "
			"through a full cycle; it is not a two-position solenoid. Position switches 56 (up) and 57 (down) close at the "
			"two travel limits, and T.18 runs the motor continuously while pausing briefly on each drawbridge up/down "
			"switch edge. The ROM reports 'Drawbridge Up Switch Bad' or 'Drawbridge Down Switch Bad' when an edge is "
			"missing. PinMAME's own mm_handleMech models the same behaviour with a 500-step position counter that sets "
			"switch 56 near steps 490-10 and switch 57 near steps 240-260, and it starts a session with the drawbridge up.",
			[
				("up", "Drawbridge up", ["switch.matrix-56"], "Raised limit; the drawbridge blocks the castle gate."),
				("down", "Drawbridge down", ["switch.matrix-57"], "Lowered limit; the castle gate becomes reachable."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-22033",
		),
		mechanism(
			"mechanism.castle-gate",
			"Castle gate (portcullis) and moat entrance",
			"gate",
			[output_id("Castle Gate Power"), output_id("Castle Gate Hold")],
			["switch.matrix-41", "switch.matrix-37"],
			"A power/hold coil pair raises and holds the portcullis. T.19 first lowers the drawbridge and refuses to run "
			"without the drawbridge-down switch. With the gate closed, a shot runs moat-enter opto 41, castle-gate opto 37, "
			"then moat-enter opto 41 again as the ball rebounds. With the gate held open, the shot runs 41, then 37, then "
			"castle-lock switch 44 into the lock area. The ROM drops the hold coil after two idle minutes so it cannot "
			"overheat. The retained script gates its castle-gate pulse on the portcullis being dropped.",
			[
				("closed", "Gate closed", ["switch.matrix-37"], "Ball rebounds out through the moat entrance."),
				("open", "Gate held open", ["switch.matrix-44"], "Ball passes through into the castle lock."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-22033",
		),
		mechanism(
			"mechanism.exploding-castle",
			"Exploding castle toy",
			"toy",
			[output_id("Castle")],
			["switch.matrix-44"],
			"Solenoid 4 releases the castle superstructure. Pressing Enter inside T.19 makes the castle shake three times "
			"and then explode for roughly four seconds; the towers and gate then have to be reset by hand before play "
			"continues. Castle-lock switch 44 is the sensor behind the gate that proves the ball reached the castle.",
			[("locked", "Ball in the castle lock", ["switch.matrix-44"], "Castle lock switch behind the gate.")],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-21718",
		),
		mechanism(
			"mechanism.left-popper",
			"Castle left popper",
			"kicker",
			[output_id("Left Popper")],
			["switch.matrix-36"],
			"Balls that pass the castle gate collect on left-popper opto 36 and are ejected back onto the playfield by "
			"solenoid 3. The retained script binds this coil to its SolMoat callback and treats the popper as the single "
			"exit from the castle lock area.",
			[("held", "Ball held in the left popper", ["switch.matrix-36"], "Left popper opto.")],
			VPX_SCRIPT_SOURCE,
			MANUAL_PARTS_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-22027",
		),
		mechanism(
			"mechanism.tower",
			"Right ramp tower, diverter, and lock post",
			"diverter",
			[output_id("Tower Diverter Power"), output_id("Tower Diverter Hold"), output_id("Tower Lock Post")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-58"],
			"T.17 documents two states. With the diverter up, a right-ramp shot runs right-ramp-enter switch 63 then "
			"right-ramp-exit switch 64 and returns the ball to the right flipper. With the diverter held down, the same "
			"shot runs 63, raises the tower lock post, climbs into the tower, and finally closes tower-exit switch 58. "
			"The ROM returns the diverter to the ramp state after two idle minutes so the diverter coil cannot overheat. "
			"The lock post works inverted in the PinMAME simulation: a held ball is released when the post output drops.",
			[
				("ramp", "Diverter up (ramp return)", ["switch.matrix-64"], "Ball returns down the ramp to the right flipper."),
				("tower", "Diverter down (tower lock)", ["switch.matrix-58"], "Ball is diverted into the tower and exits past switch 58."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-21706",
		),
		mechanism(
			"mechanism.left-troll",
			"Left troll",
			"toy",
			[output_id("Left Troll Power"), output_id("Left Troll Hold")],
			["switch.matrix-45", "switch.matrix-74", "switch.matrix-15"],
			"Manual page 3-11 states it outright: the upper-right flipper circuit is used for the left troll. A power/hold Fliptronic circuit pair on public solenoids 33 and 34 raises the left troll through the playfield "
			"and holds it up. Position switch 74 closes while the troll is raised; PinMAME's own mm_handleMech ties switch "
			"74 directly to the hold output. A ball striking the raised troll closes under-playfield switch 45. Left troll "
			"target 15 is the standup behind the troll, reachable while the troll is down. The ROM lowers a raised troll "
			"after two idle minutes so the troll coils cannot overheat.",
			[
				("up", "Troll raised", ["switch.matrix-74"], "Up-position switch inside the troll assembly."),
				("hit", "Troll struck", ["switch.matrix-45"], "Under-playfield strike switch on the troll head."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-22034",
		),
		mechanism(
			"mechanism.right-troll",
			"Right troll",
			"toy",
			[output_id("Right Troll Power"), output_id("Right Troll Hold")],
			["switch.matrix-46", "switch.matrix-75", "switch.matrix-25"],
			"Manual page 3-11 states it outright: the upper-left flipper circuit is used for the right troll. A power/hold Fliptronic circuit pair on public solenoids 35 and 36 raises the right troll and holds it up. "
			"Position switch 75 closes while the troll is raised and PinMAME's mm_handleMech ties it directly to the hold "
			"output. A ball striking the raised troll closes under-playfield switch 46, and right troll target 25 is the "
			"standup behind it. The ROM lowers a raised troll after two idle minutes.",
			[
				("up", "Troll raised", ["switch.matrix-75"], "Up-position switch inside the troll assembly."),
				("hit", "Troll struck", ["switch.matrix-46"], "Under-playfield strike switch on the troll head."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-22034",
		),
		mechanism(
			"mechanism.catapult",
			"Catapult saucer",
			"kicker",
			[output_id("Catapult")],
			["switch.matrix-12", "switch.matrix-38"],
			"Catapult target 12 is the standup in front of the catapult on the left side of the playfield. A ball that "
			"enters the catapult saucer closes switch 38 and solenoid 8 flings it up the left ramp path. The retained "
			"script's SolCatapult callback and PinMAME's simulation both send the fired ball to the left-ramp-made state.",
			[
				("target", "Catapult target", ["switch.matrix-12"], "Standup target guarding the catapult."),
				("held", "Ball in the catapult", ["switch.matrix-38"], "Catapult saucer switch."),
			],
			VPX_SCRIPT_SOURCE,
			MANUAL_SOURCE,
			MANUAL_PARTS_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-14947-1",
		),
		mechanism(
			"mechanism.merlin-eject",
			"Merlin's Magic right eject",
			"kicker",
			[output_id("Right Eject")],
			["switch.matrix-28"],
			"The right eject hole under the jet bumpers is Merlin's Magic hole. A ball resting on switch 28 is ejected by "
			"solenoid 9 (retained script callback SolMerlin) and returns to the right loop exit.",
			[("held", "Ball in Merlin's Magic hole", ["switch.matrix-28"], "Right eject hole switch.")],
			VPX_SCRIPT_SOURCE,
			MANUAL_PARTS_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-21970",
		),
		mechanism(
			"mechanism.loop-gates",
			"Left and right loop control gates",
			"gate",
			[output_id("Left Gate"), output_id("Right Gate")],
			[
				"switch.matrix-65", "switch.matrix-66", "switch.matrix-67", "switch.matrix-68",
				"switch.matrix-47", "switch.matrix-48",
			],
			"Two solenoid-operated control gates decide whether a loop shot completes the loop or is diverted into the jet "
			"bumpers. T.16 documents the exact causality: travelling left to right, the right gate (solenoid 27) opens on "
			"the second left-loop switch, Left Loop High (66); travelling right to left, the left gate (solenoid 28) opens "
			"on the second right-loop switch, Right Loop High (68). When the opposite gate stays closed the ball is routed "
			"through Left Top Lane 47 or Right Top Lane 48 into the jet bumpers instead. The retained script binds solenoid "
			"27 to gate3 and solenoid 28 to gate2.",
			[
				("left-loop", "Left loop path", ["switch.matrix-65", "switch.matrix-66"], "Left loop low then left loop high."),
				("right-loop", "Right loop path", ["switch.matrix-67", "switch.matrix-68"], "Right loop low then right loop high."),
				("to-jets", "Diverted to the jet bumpers", ["switch.matrix-47", "switch.matrix-48"], "Top-lane switches feeding the jets."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-17796 right gate with A-17796-1 left gate",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Bottom Jet Bumper"), output_id("Right Jet Bumper")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-55"],
			"Three A-12030-3 jet bumpers sit above the right ramp entrance. Each A-16443-1 skirt switch pulses its own "
			"matrix address and fires the matching coil; the retained script pulses switches 53, 54, and 55 from the three "
			"bumper hit events.",
			[
				("left", "Left jet bumper", ["switch.matrix-53"], "Left bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-54"], "Bumper closest to the player."),
				("right", "Right jet bumper", ["switch.matrix-55"], "Right bumper of the nest."),
			],
			MANUAL_PARTS_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-12030-3",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot assembly carries two switches: an A-17800/A-17794 kick switch (SW-1A-114) and a separate score "
			"switch (SW-1A-120) with a diode attached. Only the score switch reaches the matrix, at address 51 on the left "
			"and 52 on the right; the retained script pulses those two addresses from the slingshot events.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot score switch."),
			],
			MANUAL_PARTS_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="B-9362-L-2 left with B-9362-R-3 right",
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: the ROM "
			"energizes the power winding on the cabinet button opto (112 right, 114 left), then drops to the hold "
			"winding once the end-of-stroke leaf switch (111 right, 113 left) closes. Medieval Madness runs "
			"Const UseSolenoids = 2 fast flips, so the ROM drives the coils directly rather than letting the flipper "
			"circuit self-commutate, and PinMAME's synthetic game-on state on solenoid 31 follows the ROM's fast-flip "
			"flag. There are no upper flippers: the upper-flipper circuits carry the trolls instead.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE,
			MANUAL_PARTS_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-15849-R-2 right with A-15849-L-2 left",
		),
		mechanism(
			"mechanism.right-target-bank",
			"Right three-bank standup targets",
			"other",
			[],
			["switch.matrix-71", "switch.matrix-72", "switch.matrix-73"],
			"Three A-21576-4 standup targets on the right side of the playfield, top to bottom. They have no coil: the bank "
			"is not a drop-target bank and never resets, and the retained script drives them through the shared standup-"
			"target animation helper that pulses each matrix address on impact.",
			[
				("top", "Right bank top", ["switch.matrix-71"], "Topmost standup."),
				("middle", "Right bank middle", ["switch.matrix-72"], "Middle standup."),
				("bottom", "Right bank bottom", ["switch.matrix-73"], "Bottom standup."),
			],
			MANUAL_PARTS_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-21576-4",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough Eject"),
			"destination": "switch.matrix-31",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_PARTS_SOURCE),
		},
		{
			"id": "relationship.left-troll-up",
			"kind": "direct",
			"source": output_id("Left Troll Hold"),
			"destination": "switch.matrix-74",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.right-troll-up",
			"kind": "direct",
			"source": output_id("Right Troll Hold"),
			"destination": "switch.matrix-75",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
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
			"id": "williams.medieval-madness.1997",
			"name": "Medieval Madness",
			"manufacturer": "Williams",
			"year": 1997,
			"kind": "physical_pinball",
			"ipdb_id": 4032,
			"model_number": "50059",
			"opdb_id": "G5pe4-MePZv",
		},
		"coverage": {
			"status": "author_ready",
			"missing": [],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "validated",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-95",
			"hardware_generation": "0x80",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/medieval-madness-1997.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Medieval Madness device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	for device in definition["inputs"]:
		if device["spatial"]["status"] != "not_applicable":
			placement_count += len(device["spatial"]["placements"])
	return {
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.941, "bottom": 2164.706},
			"x": "x/952.941; 0=left, 1=right",
			"y": "y/2164.706; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/medieval-madness-1997/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_section_1_sha256": MANUAL_PART1_SHA256,
			"manual_section_2_sha256": MANUAL_ARCARC_SHA256,
			"manual_section_2_archive_sha256": MANUAL_PART2_SHA256,
			"manual_section_3_sha256": MANUAL_PART3_SHA256,
			"rom_sha256": ROM_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.medieval-madness.1997/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/medieval-madness-1997/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"pages": [{"path": path, "sha256": digest, "note": note} for path, digest, note in VISUAL_REVIEW_CACHE],
		},
		"excluded_object_classes": [
			"LM_* lightmap helper primitives",
			"BM_* baked-mesh render primitives",
			"VR_* and VRBG* virtual-reality room and backglass objects",
			"ramptrigger* ball-routing helper triggers",
			"BlockerWall* and blocker_* physics helpers",
			"sw*p, sw*o standup-target render primitives",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		f"# Medieval Madness (Williams, 1997) spatial review",
		"",
		f"Status: {report['status']} and promoted to `machines/author-ready/williams/medieval-madness-1997.json`.",
		"",
		"The matching source is the retained known-working `Medieval Madness (Williams 1997) VPW v1.0.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. A fresh `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. `vpxtool` established exact "
		f"playfield bounds `{TABLE_BOUNDS}`, and every canonical coordinate is x/952.941 and y/2164.706 rounded to at "
		"most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is the "
		"physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; the "
		"retained table supplies geometry.",
		"- All four retained manual PDFs are image-only scans. Every printed table used here was read from rendered pages "
		"and transcribed into "
		"`external:pinmame-review-artifacts/medieval-madness-1997/manual-transcription.md`; the retained OCR text is a "
		"search index only.",
		"- Direct table object centres cover every visible sensor, effect, and emitter. Lightmap (`LM_*`), baked-mesh "
		"(`BM_*`), virtual-reality (`VR_*`, `VRBG*`), ball-routing helper (`ramptrigger*`), physics-blocker, and standup "
		"render primitives are excluded from physical multiplicity.",
		"- Flasher addresses 17-20 drive a playfield flasher plus a separate backbox insert-panel flasher; only the "
		"playfield bulb receives a coordinate and the physical quantity stays two. Addresses 21-25 have two playfield "
		"emitters each, and the manual's Note 2 back-panel bulbs for 22 and 25 are the rear-edge pair in the table.",
		"- GI strings 0-2 use the table's GIB/GIM/GIT emitter arrays; the manual prints no per-string bulb count, so the "
		"physical quantity is taken from those arrays. GI strings 3 and 4 are backbox insert-panel circuits and take a "
		"controlled `cabinet_or_service` record.",
		"- Solenoids 33-36 are troll actuators wired to Fliptronic upper-flipper circuits, and solenoid 41 is PinMAME's "
		"mirror of LPDC output 37. The mirror is declared virtual with a `virtual` spatial record so no duplicate motor "
		"is ever placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both PinMAME "
		"core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
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
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, polarity, quantity, or semantic question remains unresolved, the definition "
		"carries no conflict records, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. Promotion to `author_ready` is therefore justified.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Candidate geometry `external:pinmame-review-artifacts/medieval-madness-1997/vpx-spatial-candidates.json`.",
		f"- Rendered manual pages `external:pinmame-manuals/rendered/williams.medieval-madness.1997/`; the "
		f"{len(VISUAL_REVIEW_CACHE)} pages that decided a canonical value are listed with their SHA-256 in the "
		"companion JSON report, so an empty or substituted render cache is an audit failure rather than an assumed "
		"source.",
		f"- Human transcription of every printed table read from those pages, SHA-256 `{MANUAL_TRANSCRIPTION_SHA256}`.",
		"- Harness runs and DMD captures `external:pinmame-review-artifacts/medieval-madness-1997/harness/`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	partial = root / PARTIAL_PATH.relative_to(ROOT)
	if partial.exists():
		partial.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	partial_path = root / PARTIAL_PATH.relative_to(ROOT)
	if partial_path.exists():
		raise RuntimeError(f"Stale Medieval Madness partial definition is still present: {partial_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Medieval Madness definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Medieval Madness seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Medieval Madness definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Medieval Madness seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Medieval Madness spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Medieval Madness spatial review drifted from its deterministic curator: {markdown_path}")
	print("Medieval Madness definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Medieval Madness extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Medieval Madness retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
