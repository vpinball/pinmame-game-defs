"""Curate the physical Bally Eight Ball Deluxe (1981) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift,
and ``--regenerate`` is the only path that writes the canonical definition and its pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: the auxiliary lamp-board addresses (97-116) are enumerated and spatially placed
# from the retained known-working script's own NFadeLm bindings, but their per-address SCR/A5Jx
# connector labels were not individually traced against the playfield wiring schematic the way
# Centaur's and Kiss's auxiliary lamp boards were. Recreation knowledge therefore remains candidate
# despite the 2026-08-08 independent review. See coverage.missing and the knowledge note.
PARTIAL_PATH = ROOT / "machines/partial/bally/eight-ball-deluxe-1981.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/eight-ball-deluxe-1981.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/eight-ball-deluxe-1981.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/eight-ball-deluxe-1981.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/eight-ball-deluxe-1981.md"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/eight-ball-deluxe-1981.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-by35"
MANUAL_SOURCE = "manual.bally.eight-ball-deluxe.1981"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.eight-ball-deluxe.1981"
VPX_TABLE_SOURCE = "vpx-table.ebd-bord-1-0-1"
VPX_SCRIPT_SOURCE = "vpx-script.ebd-bord-1-0-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ebd-bord-1-0-1"
RUNTIME_SOURCE = "runtime.eight-ball-deluxe.self-test"

MANUAL_SHA256 = "80997521916aa5947d23627a793e723b6ea56a0ec2eb618d5495cd367ba48ef9"
MANUAL_TRANSCRIPTION_SHA256 = "c8c410cdc9e56b5da2dc615f64c06b120278e183afde85eff26743b51fbbdf98"
TABLE_SHA256 = "47b2a634d1b034608458a8f3bed67fbff0b1e42757e1f8a57935f6fb7a3a310d"
SCRIPT_SHA256 = "d08e2d4c01f382ca90b7208c87f10c83360f5dac76727d024771705cd5ef68ff"
EXTRACTION_MANIFEST_SHA256 = "e72bfe3918dfdd1e76a4af8fb02352a60cbebb0a3036195f8541bc5ec7451946"
EXTRACTION_FILE_COUNT = 977
EXTRACTION_TOTAL_BYTES = 74250817

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

DRIVER_IDS = ("eballdlx", "eballd14", "eballdla", "eballdlb", "eballdlc", "eballdld")
DRIVER_COMPATIBILITY = {
	"eballdlx": (
		"identical",
		"Production revision 15 game ROM (838-15) shipped with the physical machine; the reference "
		"driver for this definition. Pinned driver.c declares GEN_BY35, dispBy7 (seven-digit "
		"displays), FLIP_SW(FLIP_L), lampCol=8 (an auxiliary lamp driver board is present), "
		"SNDBRD_BY61 (Squawk & Talk speech), and BY35GD_NOSOUNDE.",
	),
	"eballd14": (
		"identical",
		"Revision 14 game ROM (838-14); an earlier firmware revision of the same physical machine "
		"with no controller-address or playfield change.",
	),
	"eballdla": (
		"identical",
		"2004 Bally/Oliver free-play conversion, revision 1. Keeps the production 838-15 game ROM "
		"and replaces only the sound-select ROM at U6 with a free-play variant; no hardware change.",
	),
	"eballdlb": (
		"identical",
		"2007 Bally/Oliver modified-rules conversion, revision 29. Replaces both game ROMs with a "
		"rules variant; same physical machine and address space.",
	),
	"eballdlc": (
		"identical",
		"2007 Bally/Oliver modified-rules conversion, revision 32; same physical machine and address "
		"space as eballdlb.",
	),
	"eballdld": (
		"identical",
		"2019 community firmware fix (\"P2/4 Bonus Bugfix\") based on revision 15, correcting a "
		"player 2/4 bonus countdown defect; no controller-address or playfield change.",
	),
}

# --- Switch matrix (public address = printed Self Test # directly; harness-confirmed, see
# review-artifacts/eight-ball-deluxe/manual-transcription.md "Harness derivation").
SWITCH_LABELS = {
	1: "2X In-Line Drop Target", 2: "3X In-Line Drop Target", 3: "4X In-Line Drop Target",
	4: "5X In-Line Drop Target", 5: "In-Line Back Target",
	6: "Credit Button", 7: "Tilt", 8: "Outhole",
	9: "Coin Chute III (Right)", 10: "Coin Chute I (Left)", 11: "Coin Chute II (Middle)",
	12: "\"A\" Rollover Lane", 13: "\"B\" Rollover Lane", 14: "\"C\" Rollover Lane",
	15: "\"D\" Rollover Lane", 16: "Slam Tilt",
	17: "1, 9 Drop Target", 18: "2, 10 Drop Target", 19: "3, 11 Drop Target",
	20: "4, 12 Drop Target", 21: "5, 13 Drop Target", 22: "6, 14 Drop Target",
	23: "7, 15 Drop Target", 24: "30 Point Rebound",
	25: "\"D\" Target", 26: "\"E\" Target (First)", 27: "\"L\" Target", 28: "\"U\" Target",
	29: "\"X\" Target", 30: "\"E\" Target (Second)",
	31: "Right Outlane", 32: "Left Outlane", 33: "Single Drop Target", 34: "Saucer",
	35: "Rollover Button", 36: "Right Slingshot", 37: "Left Slingshot",
	38: "Left Thumper Bumper", 39: "Right Thumper Bumper", 40: "Bottom Thumper Bumper",
}
# Manual quantity annotations: "(2)"/"(3)" mark multiple physical switches wired to one address.
SWITCH_QUANTITIES = {7: 3, 16: 2, 24: 2}
CABINET_SWITCHES = {6, 9, 10, 11, 16}
SWITCH_TYPES = {6: "button", 7: "tilt", 16: "leaf"}

# address -> [(x, y), ...] normalized playfield coordinates from the retained VPWmod extraction
# (x/952, y/1974; review-artifacts/eight-ball-deluxe/vpx-geometry.txt).
SWITCH_POSITIONS = {
	1: [(0.199049, 0.334040)], 2: [(0.187240, 0.299090)], 3: [(0.176266, 0.264184)],
	4: [(0.165641, 0.228854)], 5: [(0.207190, 0.135496)],
	8: [(0.452433, 0.960318)],
	12: [(0.315594, 0.151259)], 13: [(0.420116, 0.151953)],
	14: [(0.120585, 0.696801)], 15: [(0.783019, 0.697061)],
	17: [(0.781762, 0.368699)], 18: [(0.792269, 0.397063)], 19: [(0.803196, 0.425351)],
	20: [(0.811822, 0.452807)], 21: [(0.820448, 0.480818)], 22: [(0.829649, 0.507720)],
	23: [(0.837447, 0.534450)],
	24: [(0.587324, 0.171802), (0.680489, 0.224872)],
	25: [(0.819444, 0.379309)], 26: [(0.828070, 0.407043)], 27: [(0.836984, 0.436440)],
	28: [(0.846185, 0.464728)], 29: [(0.856536, 0.493017)], 30: [(0.866312, 0.524355)],
	31: [(0.850362, 0.697356)], 32: [(0.052610, 0.695591)],
	33: [(0.786687, 0.186326)], 34: [(0.591611, 0.100693)], 35: [(0.047613, 0.192706)],
	36: [(0.674637, 0.717181)], 37: [(0.227437, 0.718919)],
	38: [(0.310762, 0.256187)], 39: [(0.527506, 0.259009)], 40: [(0.423003, 0.358058)],
}
SWITCH_OBJECTS = {
	1: "HitTarget.sw1", 2: "HitTarget.sw2", 3: "HitTarget.sw3", 4: "HitTarget.sw4",
	5: "HitTarget.sw5", 8: "Kicker.Drain",
	12: "Trigger.sw12", 13: "Trigger.sw13", 14: "Trigger.sw14", 15: "Trigger.sw15",
	17: "HitTarget.sw17", 18: "HitTarget.sw18", 19: "HitTarget.sw19", 20: "HitTarget.sw20",
	21: "HitTarget.sw21", 22: "HitTarget.sw22", 23: "HitTarget.sw23",
	24: "Wall.sw24 and Wall.sw24a",
	25: "HitTarget.sw25", 26: "HitTarget.sw26", 27: "HitTarget.sw27", 28: "HitTarget.sw28",
	29: "HitTarget.sw29", 30: "HitTarget.sw30",
	31: "Trigger.sw31", 32: "Trigger.sw32",
	33: "HitTarget.sw33", 34: "Kicker.sw34", 35: "Trigger.sw35",
	36: "Wall.RightSlingShot", 37: "Wall.LeftSlingShot",
	38: "Bumper.Bumper1", 39: "Bumper.Bumper2", 40: "Bumper.Bumper3",
}

# --- Solenoids. Public address = selector + 1 (momentary 1-15) or continuous 17-20, resolved
# empirically via the LibPinMAME self-test harness (see manual-transcription.md); it is NOT the
# printed Self Test # directly (unlike switches). 8, 9 and 10 are genuinely dual-function,
# gated by Controller.Lamp(52) in the retained script.
SOLENOID_LABELS = {
	1: "Bottom Thumper Bumper", 2: "Right Thumper Bumper", 3: "Left Thumper Bumper",
	4: "Left Slingshot", 5: "Right Slingshot", 6: "Knocker",
	7: "Single Drop Target Reset (Bank 3)",
	8: "Saucer Kicker / 7-Bank Drop Target Reset (Bank 1, mode-selected)",
	9: "Outhole Kicker / #1, 9 Drop Target Reset (mode-selected)",
	10: "4-Bank Drop Target Reset (Bank 2) / #2, 10 Drop Target Reset (mode-selected)",
	11: "#3, 11 Drop Target Reset", 12: "#4, 12 Drop Target Reset",
	13: "#5, 13 Drop Target Reset", 14: "#6, 14 Drop Target Reset",
	15: "#7, 15 Drop Target Reset (Bottom)",
	18: "Coin Lockout Door", 19: "K1 Relay (Flipper Enable)",
}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 5: "coil", 6: "coil",
	7: "coil", 8: "coil", 9: "coil", 10: "coil", 11: "coil", 12: "coil", 13: "coil",
	14: "coil", 15: "coil", 18: "coil", 19: "relay",
}
# Self-test # each public address answers to (one entry for a single-purpose address, two for a
# dual-function address, in the order Lamp(52)=0 / Lamp(52)=1 that the retained script branches on).
SOLENOID_SELF_TEST = {
	1: (6,), 2: (5,), 3: (4,), 4: (1,), 5: (2,), 6: (3,), 7: (7,),
	8: (15, 17), 9: (8, 18), 10: (9, 16),
	11: (10,), 12: (11,), 13: (12,), 14: (13,), 15: (14,),
	18: (19,), 19: (20,),
}
SOLENOID_UNUSED = (16, 17, 20)
SOLENOID_POSITIONS = {
	1: [(0.423003, 0.358058)], 2: [(0.527506, 0.259009)], 3: [(0.310762, 0.256187)],
	4: [(0.227437, 0.718919)], 5: [(0.674637, 0.717181)],
	6: [(0.909474, 0.847015)],
	7: [(0.786687, 0.186326)],
	8: [(0.591611, 0.100693), (0.452433, 0.960318)],
	9: [(0.452433, 0.960318), (0.781762, 0.368699)],
	10: [(0.199049, 0.334040), (0.792269, 0.397063)],
	11: [(0.803196, 0.425351)], 12: [(0.811822, 0.452807)], 13: [(0.820448, 0.480818)],
	14: [(0.829649, 0.507720)], 15: [(0.837447, 0.534450)],
	18: [(0.909474, 0.847015)],
}
SOLENOID_OBJECTS = {
	1: "Bumper.Bumper3 (BOTTOM THUMPER BUMPER coil)", 2: "Bumper.Bumper2 (RIGHT THUMPER BUMPER coil)",
	3: "Bumper.Bumper1 (LEFT THUMPER BUMPER coil)",
	4: "Wall.LeftSlingShot (LeftSlingShot_Slingshot)", 5: "Wall.RightSlingShot (RightSlingShot_Slingshot)",
	6: "Knocker (vpmSolSound)",
	7: "Kicker.sw33-adjacent dtbank3.SolDropUp (SolCallback(7)=Soldtbank3)",
	8: "Kicker.sw34 saucer (bsTP.SolOut) / Kicker.Drain-area dtbank1.SolDropUp (SolSaucer)",
	9: "Kicker.Drain outhole (bsTrough.SolOut) / HitTarget.sw17 dtbank1.SolHit 1 (SolBallRelease)",
	10: "HitTarget.sw1-4 dtbank2.SolDropUp / HitTarget.sw18 dtbank1.SolHit 2 (SolReset)",
	11: "HitTarget.sw19 dtbank1.SolHit 3", 12: "HitTarget.sw20 dtbank1.SolHit 4",
	13: "HitTarget.sw21 dtbank1.SolHit 5", 14: "HitTarget.sw22 dtbank1.SolHit 6",
	15: "HitTarget.sw23 dtbank1.SolHit 7",
	18: "Coin door lockout coil (no retained table object; cabinet device)",
}

# --- Lamps. Address -> label. Derived from the retained known-working script's own NFadeLm/l<N>
# bindings (script.vbs lines 476-679) cross-referenced against Section IV Feature Operation names
# and the switch/solenoid labels above for co-located features. See knowledge note for the
# per-address reasoning that is not otherwise self-evident.
LAMP_LABELS = {
	1: "Bank Shot 50,000 (In-Line Back Target)",
	2: "2X (In-Line Multiplier)", 3: "3X (In-Line Multiplier)", 4: "4X (In-Line Multiplier)",
	5: "5X (In-Line Multiplier)",
	6: "Deluxe 1", 7: "Deluxe 2", 8: "Deluxe 3", 9: "Deluxe 4", 10: "Deluxe 5",
	11: "Deluxe 6", 12: "Deluxe 7",
	17: "\"A\" Rollover Lane Lit", 18: "Right Lane 20K", 19: "Right Lane 40K",
	20: "Right Lane 60K", 21: "Deluxe 8 Ball", 22: "Deluxe Special",
	23: "\"B\" Rollover Lane Lit", 24: "Right Lane Special", 25: "Right Lane 80K",
	26: "Same Player Shoots Again",
	28: "Extra Ball (Rollover Button)",
	33: "8-Ball Target Flash", 34: "Rollover Button 500", 35: "Rollover Button 10,000",
	36: "Rollover Button 30,000", 37: "Rollover Button 50,000", 38: "Rollover Button 70,000",
	39: "\"C\" Rollover Lane Lit", 40: "\"D\" Rollover Lane Lit",
	41: "Special (Rollover Button)", 42: "Left Outlane Special",
	44: "Right Outlane Special",
	47: "Single Drop Target Lit",
	49: "High Score to Date", 50: "Game Over", 51: "Tilt",
	53: "56K Bonus", 54: "112K Bonus", 55: "Match",
	57: "Left Lane Special", 58: "Left Lane X-Ball",
	59: "Apron Credit",
	60: "Shoot Again",
	63: "Saucer Lit (500/7000)",
	65: "\"X\" Target Lit", 66: "\"D\" Target Lit", 67: "\"L\" Target Lit",
	68: "\"E\" First Target Lit", 69: "\"E\" Second Target Lit",
	70: "Left Thumper Bumper Flash (A-B-C-D 3000)",
	71: "Backbox Deluxe",
	81: "1 Rack", 82: "5 Rack", 83: "9 Rack", 84: "13 Rack", 85: "2X Bonus",
	86: "Right Thumper Bumper Flash (A-B-C-D 3000)",
	87: "3X Bonus",
	97: "2 Rack", 98: "6 Rack", 99: "10 Rack", 100: "14 Rack",
	101: "Deluxe Backbox Lamp Group (multi-image)",
	102: "Bottom Thumper Bumper Flash (A-B-C-D 3000)", 103: "3 Rack",
	113: "4 Rack", 114: "8 Rack", 115: "12 Rack", 116: "4X Bonus",
	117: "50X Deluxe", 118: "Special Deluxe", 119: "Player-Up / Ball-in-Play Feature Group",
}
LAMP_ROLE_NOTES = {
	101: "Multi-image backbox lamp: the retained script layers up to five co-located objects "
	     "(L101, L101a, L101b, and conditional L101DA/DB/DC image variants) on this one address.",
	117: "Multi-image backbox lamp: the retained script layers up to five co-located objects "
	     "(L117, L117a, L117b, and conditional L117DB/DC/DD/D8 image variants) on this one address.",
	118: "Multi-image backbox lamp: the retained script layers four co-located objects (L118, "
	     "L118a, L118b, and conditional L118DD/D8 image variants) on this one address.",
	119: "Multi-image backbox lamp: the retained script layers four co-located objects (L119, "
	     "L119a, L119b, L119c) on this one address.",
}
LAMP_POSITIONS = {
	1: (0.439559, 0.753231), 2: (0.479630, 0.671771), 3: (0.555936, 0.621147),
	4: (0.425200, 0.599882), 5: (0.600032, 0.384826), 6: (0.638374, 0.503076),
	7: (0.540923, 0.389589), 8: (0.577634, 0.507464), 9: (0.313192, 0.101945),
	10: (0.284423, 0.071099), 11: (0.451983, 0.878938), 12: (0.358053, 0.820649),
	17: (0.374007, 0.726272), 18: (0.564571, 0.665080), 19: (0.621277, 0.639787),
	20: (0.515751, 0.593202), 21: (0.610545, 0.414979), 22: (0.646736, 0.532369),
	23: (0.550511, 0.419382), 24: (0.586241, 0.536283), 25: (0.419695, 0.102647),
	26: (0.454664, 0.071821), 28: (0.424350, 0.843117),
	33: (0.506028, 0.723582), 34: (0.316165, 0.649815), 35: (0.260611, 0.620917),
	36: (0.676807, 0.605029), 37: (0.619674, 0.445133), 38: (0.655097, 0.561900),
	39: (0.558534, 0.449002), 40: (0.594233, 0.567237), 41: (0.120252, 0.646169),
	42: (0.851879, 0.648172), 44: (0.488497, 0.842641),
	47: (0.349258, 0.493792),
	49: (0.403419, 0.690195), 50: (0.422807, 0.637459), 51: (0.336975, 0.594352),
	53: (0.627421, 0.473285), 54: (0.810934, 0.253242), 55: (0.568493, 0.477821),
	57: (0.783515, 0.647065), 58: (0.051833, 0.646380), 59: (0.176243, 0.882526),
	60: (0.553368, 0.821937),
	63: (0.427459, 0.487922),
	65: (0.154902, 0.492505), 66: (0.083663, 0.371733), 67: (0.731400, 0.340201),
	68: (0.488264, 0.409109), 69: (0.527549, 0.526120), 70: (0.311323, 0.257396),
	71: (0.376193, 0.789092),
	81: (0.135950, 0.462993), 82: (0.064066, 0.329727), 83: (0.769742, 0.316837),
	84: (0.498777, 0.439129), 85: (0.535572, 0.555472), 86: (0.529361, 0.258603),
	87: (0.523833, 0.789238),
	97: (0.118798, 0.432039), 98: (0.241926, 0.437010), 99: (0.796686, 0.290100),
	100: (0.508460, 0.467681), 101: (0.122899, 0.323703),
	102: (0.422737, 0.357258), 103: (0.450643, 0.788940),
	113: (0.101092, 0.402153), 114: (0.227062, 0.402994), 115: (0.764818, 0.160677),
	116: (0.517036, 0.497701), 117: (0.104456, 0.261795), 118: (0.111464, 0.183699),
	119: (0.157942, 0.123926),
}
# Object filenames as extracted (VBScript identifiers are case-insensitive, so the retained
# script's lowercase "l<N>" and the extraction's capitalized "L<N>" name the same object).
LAMP_OBJECTS = {n: f"Light.l{n}" for n in LAMP_LABELS}
for _n in (70, 86, 101, 102, 117, 118, 119):
	LAMP_OBJECTS[_n] = f"Light.L{_n}"

# --- DIP option switches S1-S32 (AS-2518-35 MPU module, four eight-position banks). Section V.B
# ("Back Box Game Adjustments") and the Feature Operation section (Section IV) document these
# addresses to varying depth; where the manual gives a settings table the switch's exact function
# is recorded, and where it only names a switch inline (e.g. "SW. #8") without a full settings
# table that function is recorded with the same citation. The manual was not exhaustively
# transcribed for every one of the 32 switches in this pass; undocumented addresses are recorded
# honestly as unresolved rather than guessed.
DIP_LABELS = {
	1: "Coin Chute I (hinge side) credits-per-coin selector bit 1",
	2: "Coin Chute I (hinge side) credits-per-coin selector bit 2",
	3: "Coin Chute I (hinge side) credits-per-coin selector bit 3",
	4: "Coin Chute I (hinge side) credits-per-coin selector bit 4",
	5: "Coin Chute I (hinge side) credits-per-coin selector bit 5",
	6: "Game feature option (function not resolved in this pass)",
	7: "Game feature option (function not resolved in this pass)",
	8: "A-B-C-D feature: number of drop targets dropped from the 7-bank per completion (1 or 2)",
	9: "Coin Chute III credits-per-coin selector bit 1",
	10: "Coin Chute III credits-per-coin selector bit 2",
	11: "Coin Chute III credits-per-coin selector bit 3",
	12: "Coin Chute III credits-per-coin selector bit 4",
	13: "Coin Chute III credits-per-coin selector bit 5",
	14: "Rollover Button feature: scoring-sequence variant selector",
	15: "Game feature option (function not resolved in this pass)",
	16: "Saucer feature: 56K/112K super-bonus timer multiplier selector",
	17: "Coin Chute II (center) credits-per-coin selector bit 1",
	18: "Coin Chute II (center) credits-per-coin selector bit 2",
	19: "Coin Chute II (center) credits-per-coin selector bit 3",
	20: "Coin Chute II (center) credits-per-coin selector bit 4",
	21: "7 Bank & Deluxe Targets feature: recall/reset deluxe lites after each ball",
	22: "7 Bank & Deluxe Targets feature: advance backbox deluxe lamps on any deluxe hit vs. only "
	    "on deluxe-SPL",
	23: "7 Bank & Deluxe Targets feature: deluxe 50,000 award vs. 7-target reset selector",
	24: "Bank Shot / Deluxe feature: alternate-or-camp scoring selector",
	25: "Maximum credits selector bit 1",
	26: "Maximum credits selector bit 2",
	27: "High Score Feature on/off",
	28: "Match Feature on/off (also gates Credit Display per the printed adjustment page)",
	29: "Game feature option (function not resolved in this pass)",
	30: "Game feature option (function not resolved in this pass)",
	31: "Balls per game selector bit 1",
	32: "Balls per game selector bit 2",
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def slug(value: str) -> str:
	import re

	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def candidate_provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "candidate", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": round(x, 6),
				"y": round(y, 6),
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
			"locator": "Pinned catalog driver records for the eballd*/fball_ii-adjacent eballdlx clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/by35games.c INITGAME2(eballdlx,GEN_BY35,dispBy7,FLIP_SW(FLIP_L),8,SNDBRD_BY61,0) "
				"and its five eballd14/eballdla/eballdlb/eballdlc/eballdld clone records; "
				"src/wpc/by35.c MACHINE_INIT(by35) hardware setup (BY35HW_DIP4 always set for GEN_BY35, "
				"giving four DIP banks S1-S32), pia0b_r switch-column read, pia1b_w solenoid selector and "
				"continuous nibble, by35_lampStrobe; src/wpc/by35.h BY35_SWSELFTEST/BY35_SWCPUDIAG/"
				"BY35_SWSOUNDDIAG constants and BY35GD_NOSOUNDE; src/wpc/core.h CORE_SOLBIT and lamp-column "
				"sizing; src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_BY35"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/by35.json",
			"revision": "repository",
			"locator": "Bally MPU AS-2518-35 public switch, DIP, solenoid, and lamp address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.eight-ball-deluxe.1981/archive-arcademanual_Eight_Ball_Deluxe_OPS/Eight_Ball_Deluxe_OPS.pdf",
			"original_filename": "Eight_Ball_Deluxe_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"54-page Bally Midway \"Installation and General Game Operation Instructions\" manual "
				"(Internet Archive item arcademanual_Eight_Ball_Deluxe_OPS, Game No. 0B87). PDF page 22 "
				"(printed page 17) carries the Solenoid Identification Table and Switch Assembly Self-Test "
				"Display Numbers table; PDF page 41 carries the full playfield wiring schematic W-1192-28C; "
				"PDF pages 8-9 (printed 3-4) carry Section IV Feature Operation and Scoring; PDF pages "
				"10-13 (printed 5-7) carry Section V Game Adjustments including the 32-position DIP bank "
				"tables."
			),
			"license": "NOASSERTION",
			"attribution": "Bally Midway Mfg. Co.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.eight-ball-deluxe.solenoid-identification-table",
					"locator": "PDF page 22, printed page 17, SOLENOID IDENTIFICATION TABLE",
					"path": "evidence/excerpts/bally.eight-ball-deluxe.1981/solenoid-identification-table.md",
					"sha256": "b734b37cb03ccc8d01fa70e09bfb2964d75f5d5af6d1554e015cf21d737e7f91",
					"image": "evidence/excerpts/bally.eight-ball-deluxe.1981/solenoid-identification-table.webp",
					"image_sha256": "b826717d59e4ae7c8ea2de9e4cb23cc7d72f10081cc1b01497c04764d45720ce",
					"image_derivation": "Eight_Ball_Deluxe_OPS.pdf page 22, crop box 0.0993,0.0807,0.9146,0.3258, scanned page rendered at its native resolution (embedded image xref 92, 2563px across 8.54in), rendered at 260 dpi, capped to 1800px wide, 1801x699 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.eight-ball-deluxe.switch-self-test-table",
					"locator": "PDF page 22, printed page 17, SWITCH ASSEMBLY SELF-TEST DISPLAY NUMBERS",
					"path": "evidence/excerpts/bally.eight-ball-deluxe.1981/switch-self-test-table.md",
					"sha256": "7cbca13d63cab3e21f62f6b13a4fa91158bd649d11c440cd9488d1fdbc6162c2",
					"image": "evidence/excerpts/bally.eight-ball-deluxe.1981/switch-self-test-table.webp",
					"image_sha256": "d78044e556c583d98c633a7c0d491157c58bdfdf18df58e76347c326dcbf8344",
					"image_derivation": "Eight_Ball_Deluxe_OPS.pdf page 22, crop box 0.1012,0.3466,0.9049,0.8059, scanned page rendered at its native resolution (embedded image xref 92, 2563px across 8.54in), rendered at 176 dpi, capped to 1200px wide, 1201x886 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.eight-ball-deluxe.switch-matrix-grid",
					"locator": "PDF page 41, drawing W-1192-28C, WIRING DIAGRAM - PLAYFIELD, switch matrix grid",
					"path": "evidence/excerpts/bally.eight-ball-deluxe.1981/switch-matrix-grid.md",
					"sha256": "9e2ae22da2d5b1c18499edb8c64628cc7622c172c50eeb09819da03302651a9e",
					"image": "evidence/excerpts/bally.eight-ball-deluxe.1981/switch-matrix-grid.webp",
					"image_sha256": "fa98ab8773572497486f3099079e647130ba44ee49b58ff31e3807e3208f3a22",
					"image_derivation": "Eight_Ball_Deluxe_OPS.pdf page 41, crop box 0.0,0.05,0.205,0.65 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.eight-ball-deluxe.feature-operation",
					"locator": "PDF pages 8-9, printed pages 3-4, Section IV FEATURE OPERATION AND SCORING",
					"path": "evidence/excerpts/bally.eight-ball-deluxe.1981/feature-operation.md",
					"sha256": "1c7c655068a1f2f7bb1ddfd70e56b84c58dfdc1fe67c6c812e0334a84f4f5fea",
					"image": "evidence/excerpts/bally.eight-ball-deluxe.1981/feature-operation.webp",
					"image_sha256": "6200d93207efebe46fb0dc9ccb169d5099f4c43415359de297bf961e68903ad7",
					"image_derivation": "Eight_Ball_Deluxe_OPS.pdf page 8, crop box 0.1311,0.0825,0.95,0.8188, scanned page rendered at its native resolution (embedded image xref 29, 2563px across 8.54in), rendered at 86 dpi, capped to 600px wide, 601x697 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/eight-ball-deluxe/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every manual table used by this definition, the "
				"page-to-PDF-index mapping, and the full LibPinMAME harness derivation of the switch and "
				"solenoid public address tables, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/bally.eight-ball-deluxe.1981/."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": RUNTIME_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-review-artifacts/eight-ball-deluxe/harness/",
			"revision": "2026-08-07",
			"locator": (
				"LibPinMAME harness traces against the pinned native library (revision "
				f"{PINMAME_REVISION}) and the user's own legally held eballdlx ROM, generated by "
				"tools/run_pinmame_harness.py. soltest6.json is the clean, uninterrupted 20-step solenoid "
				"self-test cycle used to derive the solenoid Self-Test-#-to-public-address table; "
				"swtest2.json holds public switch addresses 1-40 during the stuck-switch search stage and "
				"confirms the switch address equals its printed Self-Test # directly. ROM bytes and NVRAM "
				"are not retained; only the harness's own JSON event logs are."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/eight-ball-deluxe-1981/source/Eight%20Ball%20Deluxe%20%28Bally%201980%29.vpx",
			"original_filename": "Eight Ball Deluxe (Bally 1980).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working table \"Eight Ball Deluxe 1.0.1\", based on a script by "
				"32assassin, authored by Bord. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/1974. Geometry authority only "
				"for named table objects. The retained table's own title reads \"(Bally 1980)\"; see the "
				"knowledge note for why this definition uses 1981."
			),
			"license": "NOASSERTION",
			"attribution": "Bord, based on a script by 32assassin",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/eight-ball-deluxe-1981/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (44,745 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "eballdlx", Const UseSolenoids = 1, Const UseLamps = 0 with per-address '
				"NFadeLm/NFadeL fader calls (lines 476-679) as the lamp-enumeration source, the "
				"SolCallback table for solenoids 6-15 and 19, the Controller.Lamp(52) mode branch inside "
				"SolSaucer/SolBallRelease/SolReset (lines 77-108) that gives solenoids 8/9/10 their dual "
				"identity, and the dtbank1/dtbank2/dtbank3 cvpmdroptarget mechanism wiring (lines 225-235)."
			),
			"license": "NOASSERTION",
			"attribution": "Bord, based on a script by 32assassin",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/eight-ball-deluxe-1981/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 "
				f"under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
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


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	for address in range(1, 41):
		label = SWITCH_LABELS[address]
		identifier = f"switch.matrix-{address}"
		physical: dict[str, Any] = {"switch_type": SWITCH_TYPES.get(address, "leaf")}
		if address in SWITCH_QUANTITIES:
			physical["quantity"] = SWITCH_QUANTITIES[address]
		notes = None
		if address == 7:
			notes = "TILT (3): the plumb-bob tilt switch plus two related contacts documented in Section II as producing the tilt penalty; all wired to this one address."
		elif address == 16:
			notes = "SLAM (2): Section II documents two factory-installed slam switches (front door, left side of cabinet) wired to this one address; the operator may add more."
		elif address == 24:
			notes = "30 POINT REBOUND (2): the retained table models two physical rebound-rubber switch objects (sw24, sw24a) at this one address."
		elif address in CABINET_SWITCHES:
			notes = "Cabinet/door switch; not shown on the playfield wiring schematic (W-1192-28C is playfield-only)."
		elif address == 8:
			notes = "Outhole ball-trough sensor; positioned at the retained table's Drain kicker, the physical outhole beneath the playfield."
		if notes:
			physical["notes"] = notes
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE)
		if address in SWITCH_OBJECTS:
			refs = refs + (VPX_SCRIPT_SOURCE,)
		item = _device(
			identifier, label, "switch", "pinmame.input.switch", address, "used", refs,
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
			normally_closed=False,
			physical=physical,
		)
		if address in SWITCH_POSITIONS:
			item["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], MANUAL_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		else:
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		items.append(item)

	for address in (-7, -6, -5):
		label = {-7: "Self Test Switch", -6: "CPU Diagnostic Line", -5: "Sound Diagnostic Line"}[address]
		identifier = f"switch.diagnostic-{abs(address)}"
		item = _device(
			identifier, label, "switch", "pinmame.input.switch", address,
			"used" if address == -7 else "optional",
			(CORE_SOURCE, CONTROLLER_SOURCE) + ((RUNTIME_SOURCE,) if address == -7 else ()),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
			normally_closed=False,
			physical={
				"notes": (
					"Momentary pushbutton on the inside of the coin door (Figure III); this curation "
					"exercised it directly via the harness to derive the switch and solenoid address "
					"tables." if address == -7 else
					"MPU-internal diagnostic line (src/wpc/by35.c BY35_SWCPUDIAG/BY35_SWSOUNDDIAG); no "
					"discrete physical operator switch is documented for this address on this machine."
				)
			},
			spatial=not_applicable("cabinet_or_service", CORE_SOURCE),
		)
		items.append(item)

	for address in range(1, 33):
		label = DIP_LABELS[address]
		bank = (address - 1) // 8 + 1
		item = _device(
			f"dip.option-switch-{address}", label, "dip_switch", "pinmame.input.dip", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE),
			aliases=[
				{"namespace": "pinmame.dip", "value": str(address)},
				{"namespace": "manual.address", "value": f"S{address}"},
			],
			physical={
				"notes": f"Bank {bank} of four eight-position banks (S1-S8, S9-S16, S17-S24, S25-S32) on the AS-2518-35 MPU module.",
			},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		)
		if "not resolved in this pass" in label:
			item["provenance"] = candidate_provenance(MANUAL_SOURCE, CONTROLLER_SOURCE)
		items.append(item)

	return items


def output_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	for address in sorted(SOLENOID_LABELS):
		label = SOLENOID_LABELS[address]
		identifier = f"solenoid.{address}"
		self_test_ids = SOLENOID_SELF_TEST[address]
		aliases = [{"namespace": "pinmame.coil", "value": str(address)}]
		for st in self_test_ids:
			aliases.append({"namespace": "manual.self-test", "value": f"{st:02d}"})
		physical_notes: str
		if len(self_test_ids) == 2:
			physical_notes = (
				f"Dual-function coil. The retained known-working script's own Controller.Lamp(52) branch "
				f"selects between two physical roles at runtime: self-test #{self_test_ids[0]:02d} when "
				f"Lamp 52 is off, self-test #{self_test_ids[1]:02d} when Lamp 52 is on. Confirmed twice: "
				"independently by the LibPinMAME solenoid self-test cycle (both self-test numbers pulse "
				"this one public address) and by the script's own SolSaucer/SolBallRelease/SolReset "
				"subs (script.vbs lines 77-108)."
			)
		else:
			physical_notes = f"Self-test #{self_test_ids[0]:02d} on the printed Solenoid Identification Table."
		refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)
		item = _device(
			identifier, label, SOLENOID_KIND[address], "pinmame.output.solenoid", address, "used", refs,
			aliases=aliases,
			physical={"notes": physical_notes},
		)
		if address in SOLENOID_POSITIONS:
			item["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], MANUAL_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		else:
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		items.append(item)

	for address in SOLENOID_UNUSED:
		identifier = f"solenoid.{address}"
		label = {16: "Unused Momentary Solenoid Position 16", 17: "Unused Continuous Output 17", 20: "Unused Continuous Output 20"}[address]
		items.append(
			_device(
				identifier, label, "coil", "pinmame.output.solenoid", address, "unused",
				(CONTROLLER_SOURCE, RUNTIME_SOURCE),
				aliases=[{"namespace": "pinmame.coil", "value": str(address)}],
				physical={"notes": "Never fires during the LibPinMAME solenoid self-test cycle (soltest6.json); no self-test identity is printed for it."},
				spatial=not_applicable("unused", RUNTIME_SOURCE),
			)
		)

	# Note: by35.json documents public flipper-coil addresses 46/48. eballdlx declares
	# FLIP_SW(FLIP_L) only (a switch mask, not FLIP_SOL), so PinMAME fakes rather than drives
	# real hardware there; see knowledge note "Flippers are not CPU-controlled".

	for address in sorted(LAMP_LABELS):
		label = LAMP_LABELS[address]
		identifier = f"lamp.{address}"
		notes = LAMP_ROLE_NOTES.get(address)
		physical = {"notes": notes} if notes else {}
		item = _device(
			identifier, label, "lamp", "pinmame.output.lamp", address, "used",
			(VPX_SCRIPT_SOURCE, MANUAL_SOURCE) if address not in (97, 98, 99, 100, 101, 102, 103, 113, 114, 115, 116, 117, 118, 119) else (VPX_SCRIPT_SOURCE,),
			aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
		)
		if physical:
			item["physical"] = physical
		if address in LAMP_POSITIONS:
			item["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		items.append(item)

	return items


def display_devices() -> list[dict[str, Any]]:
	entries = [
		("display.player-1-score", "Player 1 score, seven digits", 0, 0, 7),
		("display.player-2-score", "Player 2 score, seven digits", 1, 8, 7),
		("display.player-3-score", "Player 3 score, seven digits", 2, 16, 7),
		("display.player-4-score", "Player 4 score, seven digits", 3, 24, 7),
		("display.credits", "Credits, two digits", 4, 32, 2),
		("display.ball-in-play", "Match and ball in play, two digits", 5, 34, 2),
	]
	items = []
	for identifier, label, controller_index, segment_start, width in entries:
		items.append(
			{
				"id": identifier,
				"label": label,
				"kind": "segment",
				"controller_index": controller_index,
				"segment_start": segment_start,
				"width": width,
				"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
				"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			}
		)
	return items


def mechanism_devices() -> list[dict[str, Any]]:
	return [
		{
			"id": "mechanism.drop-target-bank-1",
			"label": "7-Bank Drop Targets (\"1,9\" through \"7,15\", the Deluxe bank)",
			"kind": "drop_target_bank",
			"actuators": ["solenoid.11", "solenoid.12", "solenoid.13", "solenoid.14", "solenoid.15"],
			"sensors": ["switch.matrix-17", "switch.matrix-18", "switch.matrix-19", "switch.matrix-20", "switch.matrix-21", "switch.matrix-22", "switch.matrix-23"],
			"behavior": (
				"Seven individual drop targets, printed \"1,9\" through \"7,15\" (Feature G, \"7 BANK DROP & "
				"DELUXE TARGETS\"): knocking down 1-7 scores 2000 each and flashes the single \"8 ball\" "
				"target (switch.matrix-33, a different mechanism); a second pass over the same seven "
				"targets scores 3000 each as \"deluxe\" once the 8-ball target has been hit. The retained "
				"script's dtbank1 object (script.vbs lines 225-227) wires all seven sensors "
				"(sw17-sw23) to one cvpmdroptarget bank. Each target 3-7 has its own small reset coil, "
				"fired unconditionally (solenoid.11-15, listed as this mechanism's actuators). Targets "
				"1 and 2 are instead individually re-fired only while Lamp 52 is off, by solenoid.9 "
				"(dtbank1.SolHit 1) and solenoid.10 (dtbank1.SolHit 2) respectively -- both owned by "
				"their own mechanism below, since Lamp 52 on gives each its more distinctive "
				"ball-handling identity. Solenoid.8 (owned by mechanism.saucer) raises this whole bank "
				"at once (dtbank1.SolDropUp) while Lamp 52 is off. The manual's own Solenoid "
				"Identification Table names each of these seven addresses after its own target pair "
				"(\"#1, 9 DROP TARGET\" through \"#7, 15 DROP TARGET\")."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "mechanism.drop-target-bank-2",
			"label": "4-Bank In-Line Drop Targets (2X/3X/4X/5X)",
			"kind": "drop_target_bank",
			"actuators": ["solenoid.10"],
			"sensors": ["switch.matrix-1", "switch.matrix-2", "switch.matrix-3", "switch.matrix-4"],
			"behavior": (
				"Four drop targets scoring 5000/10,000/15,000/20,000 for the 1st-4th target down and "
				"lighting 2X/3X/4X/5X respectively (Feature C, \"INLINE DROP & BANK SHOT TARGET FEATURE\"). "
				"The retained script's dtbank2 object (script.vbs lines 229-231) wires sw1-sw4 to one "
				"cvpmdroptarget bank; solenoid 10, in its Lamp(52)=1 identity, raises the whole bank at "
				"once (dtbank2.SolDropUp). The related standup \"In-Line Back Target\" (switch.matrix-5, "
				"the \"Bank Shot\" target scoring 50,000) is a separate, non-drop standup pulsed directly "
				"by the ball and is not part of this bank."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "mechanism.drop-target-single",
			"label": "Single Drop Target",
			"kind": "drop_target_bank",
			"actuators": ["solenoid.7"],
			"sensors": ["switch.matrix-33"],
			"behavior": (
				"One drop target (Feature E, \"SINGLE DROP TARGET FEATURE\"): scores 500 if no right-lane "
				"lite is lit, else scores and advances the lit lane value; stays down until the ball "
				"returns through lane A or B. The retained script's dtbank3 object (script.vbs lines "
				"233-235) wires sw33 to a one-target cvpmdroptarget bank reset unconditionally by "
				"solenoid 7 (Soldtbank3, dtBank3.SolDropUp)."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "mechanism.saucer",
			"label": "Playfield Saucer",
			"kind": "kicker",
			"actuators": ["solenoid.8"],
			"sensors": ["switch.matrix-34"],
			"behavior": (
				"Upper-playfield ball-capture saucer (Feature B, \"SAUCER FEATURE\"): scores the top-right "
				"lane SPL award and 500 or 7000 points per lit inline-bank light, plus the 56K/112K "
				"super-bonus multiplier. The retained script's bsTP cvpmBallStack object "
				"(script.vbs line 220) captures the ball at sw34 and kicks it back into play; solenoid "
				"8, in its Lamp(52)=1 identity, is the kick-out coil (bsTP.SolOut)."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "mechanism.outhole",
			"label": "Outhole / Ball Trough",
			"kind": "kicker",
			"actuators": ["solenoid.9"],
			"sensors": ["switch.matrix-8"],
			"behavior": (
				"Ball-drain sensor beneath the playfield (Section II, General Game Operation: \"the "
				"outhole kicker serves the ball to the shooter alley\"). The retained script's bsTrough "
				"cvpmBallStack object (script.vbs line 213) captures the drained ball at the Drain "
				"kicker (switch.matrix-8) and releases it; solenoid 9, in its Lamp(52)=1 identity, is "
				"the release coil (bsTrough.SolOut)."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	]


def relationship_records() -> list[dict[str, Any]]:
	pairs = [
		(38, 3, "left-thumper-bumper"), (39, 2, "right-thumper-bumper"), (40, 1, "bottom-thumper-bumper"),
		(36, 5, "right-slingshot"), (37, 4, "left-slingshot"),
	]
	items = []
	for switch_address, solenoid_address, slug_name in pairs:
		items.append(
			{
				"id": f"relationship.{slug_name}-direct-fire",
				"kind": "direct",
				"source": f"switch.matrix-{switch_address}",
				"destination": f"solenoid.{solenoid_address}",
				"provenance": provenance(MANUAL_SOURCE),
			}
		)
	return items


def conflict_records() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.retained-table-year-vs-driver",
			"path": "machine.year",
			"description": (
				"The retained known-working table's own title reads \"Eight Ball Deluxe (Bally 1980)\", "
				"but pinned driver.c dates every eballdlx-family CORE_GAMEDEFNV/CORE_CLONEDEFNV entry "
				"1981, and this manual's own printed copyright (\"COPYRIGHT MCMLXXXIV BY BALLY MIDWAY "
				"MFG. CO.\", 1984) is neither value -- it is a later reprint date under the merged "
				"\"Bally Midway\" imprint that did not exist until 1983-84, not the physical machine's "
				"release year. This definition uses 1981, matching the pinned driver and the pre-existing "
				"stub identity; the table author's \"1980\" is treated as an informal/incorrect dating "
				"rather than a competing authority. See knowledge/bally/eight-ball-deluxe-1981.md. "
				"Resolution path: the IPDB machine entry for this title, read through the headful "
				"browser session IPDB's Cloudflare gate requires, or a first-printing copy of this "
				"manual carrying the original Bally imprint rather than the later Bally Midway "
				"reprint stamp; either dates the physical machine independently of the pinned driver "
				"and of the table author's title text. Unresolved."
			),
			"source_refs": [VPX_TABLE_SOURCE, CORE_SOURCE, MANUAL_SOURCE],
		},
	]


def build_definition() -> dict[str, Any]:
	drivers = [
		{
			"id": driver_id,
			"description": {
				"eballdlx": "Eight Ball Deluxe (rev. 15)",
				"eballd14": "Eight Ball Deluxe (rev. 14)",
				"eballdla": "Eight Ball Deluxe (Free Play)",
				"eballdlb": "Eight Ball Deluxe (modified rules rev. 29)",
				"eballdlc": "Eight Ball Deluxe (modified rules rev. 32)",
				"eballdld": "Eight Ball Deluxe (P2/4 Bonus Bugfix)",
			}[driver_id],
			"year": {"eballdlx": "1981", "eballd14": "1981", "eballdla": "2004", "eballdlb": "2007", "eballdlc": "2007", "eballdld": "2019"}[driver_id],
			"manufacturer": {
				"eballdlx": "Bally", "eballd14": "Bally", "eballdla": "Bally / Oliver",
				"eballdlb": "Bally / Oliver", "eballdlc": "Bally / Oliver", "eballdld": "Bally / idleman",
			}[driver_id],
			"flags": 0,
			"physical_compatibility": DRIVER_COMPATIBILITY[driver_id][0],
			"variant_notes": DRIVER_COMPATIBILITY[driver_id][1],
			**({"clone_of": "eballdlx"} if driver_id != "eballdlx" else {}),
		}
		for driver_id in DRIVER_IDS
	]

	inputs = input_devices()
	inputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))
	outputs = output_devices()
	outputs.sort(key=lambda item: (item["binding"]["group"], item["binding"]["device"]))

	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "bally.eight-ball-deluxe.1981",
			"name": "Eight Ball Deluxe",
			"manufacturer": "Bally",
			"year": 1981,
			"kind": "physical_pinball",
			"playfield": {"width": 952.0, "height": 1974.0, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)},
			# The OPDB import added both identity fields to the committed record
			# but only `opdb_id` here, so the next regeneration of this curator
			# silently dropped the IPDB id. `--check` stayed green because the
			# file then matched the curator's own incomplete output; only
			# `reports/opdb-identity.json` noticed.
			"ipdb_id": 762,
			"opdb_id": "G5KXk-MLB9V",
		},
		"coverage": {
			"status": "partial",
			"missing": ["input_semantics", "output_semantics", "recreation_notes", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "candidate",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "candidate",
				"spatial_placement": "validated",
			},
		},
		"controller": {"platform": "pinmame.by35", "inversion_applied_by_emulator": True},
		"drivers": drivers,
		"inputs": inputs,
		"outputs": outputs,
		"displays": display_devices(),
		"mechanisms": mechanism_devices(),
		"relationships": relationship_records(),
		"conflicts": conflict_records(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/eight-ball-deluxe-1981.md", "status": "partial"},
	}


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	not_applicable_inputs: dict[str, list[int]] = {}
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	resolved_input_addresses: list[int] = []
	resolved_output_bindings: list[dict[str, Any]] = []
	placement_count = 0

	for item in definition["inputs"]:
		address = item["binding"]["device"]
		spatial = item.get("spatial")
		if spatial is None:
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			resolved_input_addresses.append(address)
			placement_count += len(spatial["placements"])

	for item in definition["outputs"]:
		if item["binding"]["group"] != "pinmame.output.solenoid" and item["kind"] != "lamp":
			continue
		address = item["binding"]["device"]
		spatial = item.get("spatial")
		if spatial is None:
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append({"address": address, "group": item["binding"]["group"]})
		else:
			resolved_output_bindings.append({"address": address, "group": item["binding"]["group"]})
			placement_count += len(spatial["placements"])

	for values in not_applicable_inputs.values():
		values.sort()
	for values in not_applicable_outputs.values():
		values.sort(key=lambda entry: (entry["group"], entry["address"]))
	resolved_input_addresses.sort()
	resolved_output_bindings.sort(key=lambda entry: (entry["group"], entry["address"]))

	blockers = [
		"Auxiliary lamp-board addresses 97-116 are enumerated and spatially placed from the "
		"retained known-working script's own address bindings, but their individual A5J1/A5J3-to-"
		"A9J2/A9J3 SCR/connector pin assignments were not traced against the playfield wiring "
		"schematic (W-1192-28C) the way Centaur's and Kiss's auxiliary lamp boards were.",
		"DIP option switches 6, 7, 15, 29, and 30 have a confirmed public address and cabinet "
		"location but no resolved function; the manual's Section V.B game-adjustment tables were "
		"not exhaustively transcribed for every one of the 32 option switches.",
		"conflict.retained-table-year-vs-driver is recorded for transparency though this "
		"definition already resolves it (1981, matching pinned driver.c) rather than leaving the "
		"machine year itself unresolved.",
		"Recreation knowledge remains candidate until the five unresolved DIP functions and the "
		"auxiliary lamp-board connector identities above are documented.",
	]

	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": "bally.eight-ball-deluxe.1981",
		"status": "partial",
		"coordinate_convention": {
			"space": "playfield",
			"x": "x/952; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 1974.0},
		},
		"extraction": {
			"source_ref": VPX_EXTRACTION_SOURCE,
			"manifest_uri": "external:pinmame-vpx-sources/bally/eight-ball-deluxe-1981/extracted-vpxtool.manifest.json",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
			"fail_closed": True,
		},
		"resolved_input_addresses": resolved_input_addresses,
		"not_applicable_inputs": not_applicable_inputs,
		"resolved_output_bindings": resolved_output_bindings,
		"not_applicable_outputs": not_applicable_outputs,
		"placement_count": placement_count,
		"excluded_object_classes": [
			"Light.LED1-LED286 and Light.Light1-Light24 (backglass scoreboard/decorative render "
			"objects with no NFadeLm public-lamp binding in the retained script) -- render-only, "
			"not addressable controlled devices.",
			"Primitive.BulbFil1-28/BulbTop1-28 (filament/glass primitive render doubles of the l<N> "
			"Light objects) -- cosmetic doubles of an already-placed emitter, not a distinct address.",
		],
		"projections": [],
		"unresolved": [
			"lamp.97-116 auxiliary-board SCR/connector pin identity (see blockers)",
			"dip.option-switch-6, dip.option-switch-7, dip.option-switch-15, dip.option-switch-29, dip.option-switch-30 function",
		],
		"source_hashes": {
			"manual_pdf_sha256": MANUAL_SHA256,
			"manual_transcription_sha256": MANUAL_TRANSCRIPTION_SHA256,
			"vpx_table_sha256": TABLE_SHA256,
			"vpx_script_sha256": SCRIPT_SHA256,
			"vpx_extraction_manifest_sha256": EXTRACTION_MANIFEST_SHA256,
		},
		"visual_review_cache": [
			"manuals/rendered/bally.eight-ball-deluxe.1981/page-01.png",
			"manuals/rendered/bally.eight-ball-deluxe.1981/page-02.png",
			"manuals/rendered/bally.eight-ball-deluxe.1981/page-22.png",
			"manuals/rendered/bally.eight-ball-deluxe.1981/page-41.png",
		],
		"blockers": blockers,
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Bally Eight Ball Deluxe (1981) spatial audit",
		"",
		f"Status: **{report['status']}**. Format `{report['format']}`.",
		"",
		"## Coordinate convention",
		"",
		f"- Space: `{report['coordinate_convention']['space']}`",
		f"- x: {report['coordinate_convention']['x']}",
		f"- y: {report['coordinate_convention']['y']}",
		f"- Source bounds: {report['coordinate_convention']['source_bounds']}",
		"",
		"## Extraction identity",
		"",
		f"- Source ref: `{report['extraction']['source_ref']}`",
		f"- Manifest SHA-256: `{report['extraction']['manifest_sha256']}`",
		f"- Files: {report['extraction']['file_count']}, bytes: {report['extraction']['total_bytes']}",
		f"- vpxtool: {report['extraction']['vpxtool_version']}",
		"",
		f"## Placements: {report['placement_count']}",
		"",
		f"- Resolved input addresses: {len(report['resolved_input_addresses'])}",
		f"- Resolved output bindings: {len(report['resolved_output_bindings'])}",
		"",
		"## Not-applicable inputs",
		"",
	]
	for reason, addresses in sorted(report["not_applicable_inputs"].items()):
		lines.append(f"- `{reason}`: {addresses}")
	lines.append("")
	lines.append("## Not-applicable outputs")
	lines.append("")
	for reason, entries in sorted(report["not_applicable_outputs"].items()):
		lines.append(f"- `{reason}`: {entries}")
	lines.append("")
	lines.append("## Excluded object classes")
	lines.append("")
	for entry in report["excluded_object_classes"]:
		lines.append(f"- {entry}")
	lines.append("")
	lines.append("## Unresolved")
	lines.append("")
	for entry in report["unresolved"]:
		lines.append(f"- {entry}")
	lines.append("")
	lines.append("## Blockers")
	lines.append("")
	for entry in report["blockers"]:
		lines.append(f"- {entry}")
	return "\n".join(lines).rstrip("\n") + "\n"


def check(root: Path) -> None:
	definition = build_definition()
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Eight Ball Deluxe definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Eight Ball Deluxe seed is not byte-identical to the promoted definition: {seed_path}")
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.is_file():
		raise RuntimeError(f"stale artifact for the other coverage status: {stale}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Eight Ball Deluxe spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Eight Ball Deluxe spatial review drifted from its deterministic curator: {markdown_path}")
	if not KNOWLEDGE_PATH.is_file():
		raise RuntimeError(f"Eight Ball Deluxe knowledge note is missing: {KNOWLEDGE_PATH}")
	print("Eight Ball Deluxe definition, seed, and spatial audit match the deterministic curator.")


def generate(root: Path) -> list[Path]:
	definition = build_definition()
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.is_file():
		stale.unlink()
	write_json(definition_path, definition)
	write_json(seed_path, definition)
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	write_json(report_path, report)
	write_text(markdown_path, render_spatial_report(report))
	return [definition_path, seed_path, report_path, markdown_path]


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	elif args.regenerate:
		written = generate(ROOT)
		for path in written:
			print(f"Wrote {path.relative_to(ROOT).as_posix()}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
