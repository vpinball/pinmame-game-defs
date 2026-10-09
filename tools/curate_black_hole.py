"""Curate the physical Gottlieb Black Hole (1981) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and table
coordinate is a literal here, so regeneration reproduces the canonical definition, its pinned seed,
the knowledge note (from its seed) and the spatial report byte for byte without reading the external evidence roots. ``--check`` refuses
drift, and ``--regenerate`` is the only path that writes them.

Black Hole is game #668 on Gottlieb System 80 (``GEN_GTS80``), the first System 80 machine in this
repository, and its controller contract is the new ``pinmame.gts80`` profile. Most of its playfield
mechanisms are not solenoid drivers at all: System 80 has nine solenoid drivers, and Black Hole runs
its two hole kickers, both ball gates, the ball lift, the re-entry gate and the U/L relays that switch
the flippers and illumination between the two playfields from lamp drivers (public lamps 8 and
12-18). The pop bumpers, kicking rubbers, kicking target and six flippers are fired by their own
switches and are not controller outputs.

Evidence priority actually applied here, in the runbook's order:

1. The retained known-working VPX table by cyberpez (v1.1) for runtime bindings and the lamp-driven
   device callbacks, except where it is demonstrably defective (it binds the upper pop-bumper caps to
   lamp 2, the coin lockout coil, and pulses drop-target switches instead of holding them).
2. The Black Hole instruction manual (two retained scans: Scribd document 223467608, complete but with
   the fold-out sheets cropped at the right; idoc.pub jlk9z9rz1545, sharper but ending at page 28) for
   wiring, fitment and behaviour.
3. Pinned PinMAME source for the System 80 contract.
4. The retained table's geometry for coordinates.
5. Hash-pinned LibPinMAME harness runs of the ROM's own self tests and of gameplay sequences, which
   settle the solenoid numbering the manual misprints, the switch numbering, the lamp-driven devices'
   addresses, the tilt inputs and the lightbox lamps.
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
MACHINE_ID = "gottlieb.black-hole.1981"
STATUS = "partial"
PARTIAL_PATH = ROOT / "machines/partial/gottlieb/black-hole-1981.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/gottlieb/black-hole-1981.json"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/gottlieb/black-hole-1981.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/gottlieb/black-hole-1981.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/gottlieb/black-hole-1981.md"
KNOWLEDGE_PATH = "knowledge/gottlieb/black-hole-1981.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/gottlieb/black-hole-1981.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
SCENARIO_DIRECTORY = "tools/harness-scenarios/gts80"
# The sound-only (668A) drivers had their own residual record; the manual documents that build as the
# same machine with the sound board fitted in place of the sound/speech board, so it is folded in here.
RETIRED_ARTIFACTS = (
	ROOT / "machines/partial/gottlieb/black-hole-1981-blkholea.json",
	ROOT / "knowledge/gottlieb/black-hole-1981-blkholea.md",
)

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-gts80"
MANUAL_SOURCE = "manual.gottlieb.black-hole.1981.scribd"
MANUAL_IDOC_SOURCE = "manual.gottlieb.black-hole.1981.idoc"
IPDB_SOURCE = "ipdb.307"
VPX_TABLE_SOURCE = "vpx-table.black-hole-cyberpez-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.black-hole-cyberpez-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.black-hole-cyberpez-1-1"
VPM_LIBRARY_SOURCE = "vpm-script-library.sys80-vbs"
SISTER_SCRIPTS_SOURCE = "vpx-script.system-80-sister-tables"

MANUAL_SCRIBD_MANIFEST_SHA256 = "1c65c214173f47a6a800005758b4bd6ac93b08ce12e46a9b186dbefb1ce77c66"
MANUAL_IDOC_MANIFEST_SHA256 = "156cb601d6ffaf8f6c67fbe1cb32b45252231f548c3c9cf452af6de213e1dd43"
IPDB_PAGE_SHA256 = "085657f322406e81a0682ee1886d78e2f0c724e296ddae6b0c53c016737bc64b"
TABLE_SHA256 = "23db54a8c2f3feed3e299c7c64e1cb43a516fd6bba0f55a016dc48c38ce36d3a"
DIRECTB2S_SHA256 = "dfc3b95f49bb45c657dcfa361b2bb57aa3e4407a11bf35a349001bbf4d76c392"
SCRIPT_SHA256 = "9ecdc9f67b2623360335c5ce1e7601ae792a923a6898fe9c60fd11a398530b99"
VPM_SYS80_SHA256 = "5e14a206222039389c220aac40bf410e35fd7c730786bb6686d1b8ab6494de8c"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = {
	"blckhole": "cd3263c830194b541f2eb0480a78fc1456701df5b46b16e65f5fdd0dc1bf4a99",
	"blkhole2": "4005ccb8f1af1626391f8a78ebce8eae4bfd7e5f30a0b5870aa4b89951e456eb",
	"blkholea": "4f3fba6abd4ccf4269ffdcd6e4ef301ac379a85c1907e86d56f8e79900786ca3",
	"blkhole7": "b47132083c1079b586041db79e46fc872830cabfccac363ecdb7c660a9f3c7b6",
	"blkhol7s": "2abcfb17c9a4e06b6bd251d40ba01a1c372bb31da34374150c45d155ddeb265b",
}

EXTRACTION_RELATIVE_PATH = Path("gottlieb/black-hole-1981/extracted-vpxtool/black-hole-gottlieb-1981-vpx-1.1")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("gottlieb/black-hole-1981/extracted-vpxtool/black-hole-gottlieb-1981-vpx-1.1.manifest.json")
EXTRACTION_FILE_COUNT = 1129
EXTRACTION_TOTAL_BYTES = 101152443
EXTRACTION_MANIFEST_SHA256 = "bb3615dd9725e0e98d2d271e8f4eb0c23d5e324e2a5c998913ae1410fc99dc34"
SPATIAL_CANDIDATES_SHA256 = "2df73f13d773f845bd0590ef3e4476bd969860180805457a49deb6cafe16abf4"

TABLE_BOUNDS = "left=0 top=0 right=1116 bottom=2186"
PLAYFIELD_WIDTH = 1116.0
PLAYFIELD_HEIGHT = 2186.0

# Retained harness runs under the working root's runtime-evidence/black-hole-1981/<name>/:
# name: (game, run.json sha256, scenario file, scenario sha256)
HARNESS_RUNS = {
	"lamp-driver-test": ("blckhole", "06827fad3431e2871bb0d40f61b2d296acecc492646d30d6515474806a9088ec", "black-hole-lamp-driver-test.json", "b4ab36dd6d7a0610895ec8c21f650f88bc3b3f427704117515ffc0d6e807862a"),
	"solenoid-test": ("blckhole", "b1005095ea4d037326ea0cd6c921156e7c94358b82464d74dbe03a6b2e5e103c", "black-hole-solenoid-test.json", "950025d0678543ebf93763033eec601e9d848a79f5b7351046702dabee8058fc"),
	"switch-test-a": ("blckhole", "56f3497216be411509ae3b016ab47584cc7fa91fe729d64158d138a4a4c5079f", "black-hole-switch-test-a.json", "4752b419b0df1a3cf7f439aa4e2531b46c8ed4f0e7401cc514988ead29ac7721"),
	"switch-test-b": ("blckhole", "206a156542eb4b2ef94cd45d2eddc1c263afae3059a9693e0dae3e3305102aa5", "black-hole-switch-test-b.json", "c091e4a0510bf77ea3122128adeb00ff0a669e8c12ca552d71f27330c53f91ac"),
	"switch-test-c": ("blckhole", "c16424834b790555b6a1ddc08b8cb6008fe0568b10ff8815c20b9dbada233071", "black-hole-switch-test-c.json", "3da64bfd48915f3898deef284396973dcd4d193fd4d2f77df58f4f6bf331afaa"),
	"switch-test-d": ("blckhole", "d7de89e9f9fe1f15b34b38600d5e8875768b52cda80899e79d1e2b719f566b21", "black-hole-switch-test-d.json", "5758f08d2c1c42fcfc1a4062bff569c46fe839a027b7cc2650665b823021cfc6"),
	"switch-test-e": ("blckhole", "4b12b4c87a74f249e9e21cd78d150046383495968c1074e5dbe5581604549aea", "black-hole-switch-test-e.json", "499d457df95ad8f36a0183bf8632752d17ece65a901c852740c574738c2a358b"),
	"gameplay-causality": ("blckhole", "9b0bf518d1a18081e5eb7afc76f3e46223aa2283dc15844987b35902e2e47585", "black-hole-gameplay-causality.json", "87db8a4534faa5f7798eb048167eedd92bf67d7abf2e7dff4a20220c8231b0d7"),
	"high-game-to-date": ("blckhole", "ea383e963888982af1a2301f1ba18628fba0d14bd443213542c336665d70872b", "black-hole-high-game-to-date.json", "0e4699165deb613fe38578728f58b39fff612706bc3a9236e81e958ce5c3c837"),
	"tilt-26": ("blckhole", "4bb8c6c77667afe04f2a6ab0a180dca6319881f0260f3313732725b10ec838a7", "black-hole-tilt-26.json", "cfb824b922e5a370f1cbd241cd709b879dd1a639a43381f419865c777346d1df"),
	"tilt-57": ("blckhole", "8c269e900893cbdc74f2fe25d9f3578514d1e2cea6506c22d74a7dce510ecaaa", "black-hole-tilt-57.json", "57346244a673c0d92526d99bba57899028c72f637a99204e31142c95d10955c2"),
	"tilt-77": ("blckhole", "e1ab90f63e79f51e69c07b3715ae950a98c4e97c35ae8c648381c5f778fb8377", "black-hole-tilt-77.json", "e307bbd0cc395665b80b9e20a888f695c5f5214129740ccaaa39f8902c047145"),
	"slam": ("blckhole", "9e97aaa8f3e531c8611648be328411e49c3644716d6a43e332cb7fabd391219e", "black-hole-slam.json", "9024b42d3c7e430082756b6edf2c055268dc1b0e21e94d421ff0148f64abd59d"),
	"blkhole2-service": ("blkhole2", "b7e0d00906ea9253fca4abffb31e69cee73391293484c4012bd4f22c80a07861", "black-hole-blkhole2-service.json", "cc49f77be3a9c87d6b541a7993ab83549b2aa6493bf05850456b6d3e100cd7d5"),
	"blkholea-service": ("blkholea", "fa1267ce56b2afe240dc2a2d9d24cc4866f32cf835f023da3b9715f389f26b57", "black-hole-blkholea-service.json", "a51fd25070d0aea1f432a8402e6bd39b1e3e88deef578b7140aaab3b95df1ac1"),
	"blkhole7-service": ("blkhole7", "84dc32b984e1ea89e40aedad3da7109df8bcce991f9e6d7d4e414b76b1aaa7f0", "black-hole-blkhole7-service.json", "32b99cae4c091edf6d67d831db8fb9bb73cb07ef435c68f140ea076f351dd5fb"),
	"blkhol7s-service": ("blkhol7s", "88763a17f3816185b79f679a5644dff4782ab989f95b8f66cf64b225e11f5cdf", "black-hole-blkhol7s-service.json", "01f069c222dc753b9430ca5e17813c4e4f8844ac961745097528cb7f64e850df"),
}
RUNTIME_DIRECTORY = "black-hole-1981"
# (file count, total bytes, manifest.json sha256) of runtime-evidence/black-hole-1981, written by
# tools/build_external_evidence_manifest.py.
RUNTIME_MANIFEST = (85, 23674680, "aa9cde8eb85149f422ef7594f8ab54f7313f093ac4d362e80590db090862f8f2")

RUN_SOURCE = {name: f"runtime.black-hole.{name}" for name in HARNESS_RUNS}
SWITCH_TEST_SOURCES = tuple(RUN_SOURCE[f"switch-test-{part}"] for part in "abcde")
VARIANT_SOURCES = tuple(RUN_SOURCE[f"{game}-service"] for game in ("blkhole2", "blkholea", "blkhole7", "blkhol7s"))

SWITCH = "pinmame.input.switch"
DIP = "pinmame.input.dip"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
GI = "pinmame.output.gi"


def norm(x: float, y: float) -> tuple[float, float]:
	return round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6)


# --- Exact centres of the retained table objects used for placements, in table units: triggers,
# kickers, bumpers, spinners, flippers, hit targets and lights at their stored centre, walls at their
# drag-point centroid, and the lower playfield's insert flashers at their stored position.
TABLE_POINTS: dict[str, tuple[float, float]] = {
	"Tri_TopLeft": (569.16003, 278.71503),
	"Tri_TopMid": (642.81604, 278.71503),
	"Tri_TopRight": (725.4, 280.901),
	"Tsw01": (815.5711433333332, 1148.0911333333333),
	"Tsw11": (828.9377833333334, 1201.7138333333332),
	"Tsw21": (843.3465233333333, 1252.5215666666666),
	"Tsw31": (857.8153033333333, 1305.8753666666667),
	"TargetH": (841.32574, 602.7599),
	"TargetO": (853.04376, 653.5844),
	"TargetL2": (867.55176, 704.4089),
	"TargetE": (880.38574, 755.2334),
	"TargetB": (343.1172, 586.39453),
	"TargetL": (368.22717, 539.66876),
	"TargetA": (395.01117, 489.39078),
	"TargetC": (421.7952, 442.93826),
	"TargetK": (448.02118, 398.12527),
	"sw05": (64.52452, 909.88983),
	"Bumper1": (590.92206, 703.3455),
	"Bumper2": (633.33, 478.734),
	"Bumper3": (843.13806, 358.69003),
	"Bumper4": (107.69401, 1461.3411),
	"Bumper5": (505.9453, 1628.5872),
	"Bumper6": (811.3331, 1191.318),
	"Drain": (552.978, 2081.072),
	"Spinner1": (87.76, 638.1156),
	"Gate_TopLeft": (424.08002, 197.83301),
	"kicker1": (965.34, 1862.472),
	"kicker3": (822.49207, 1935.7031),
	"Tri_MidRightLane": (970.5, 689.0),
	"Tri_BlackHole": (225.0, 293.0),
	"Sling1": (136.70221, 950.5398633333333),
	"Sling3": (296.5987875, 1586.06615),
	"Sling4": (389.42947000000004, 463.799455),
	"Sling5": (876.5813375, 675.8921475),
	"Sling6": (799.6314649999999, 1491.7177),
	"Sling7": (284.994575, 1075.68985),
	"Sling8": (708.2173225, 996.30125),
	"Sling9": (648.41279, 1532.9836),
	"Tri_LeftInlane": (868.1085, 1496.317),
	"TargetLL40": (341.447565, 1510.835125),
	"TargetLL50": (332.4811975, 1461.575825),
	"TargetLL60": (323.828955, 1411.67985),
	"TargetLL70": (315.70063749999997, 1362.51405),
	"TargetLR41": (702.5901, 1366.909125),
	"TargetLR51": (660.3430075, 1395.468625),
	"TargetLR61": (616.8473074999999, 1424.9672249999999),
	"sw42": (293.21246, 1624.496),
	"sw43": (965.84467, 401.69705),
	"sw52": (745.541, 1668.487),
	"sw53": (818.35504, 488.08383),
	"Tri_sw62": (165.69994, 1085.4744),
	"Flipper1": (907.58704, 1579.7949),
	"L3": (514.197, 1883.5123),
	"L7": (144.522, 753.62354),
	"L21": (389.484, 815.92456),
	"L22": (420.87152, 769.3354),
	"L23": (449.32953, 721.1068),
	"L24": (477.92703, 671.23865),
	"L25": (508.47754, 620.82404),
	"L26": (683.82904, 749.1149),
	"L27": (698.75555, 801.30566),
	"L28": (713.403, 852.6767),
	"L29": (728.74805, 904.5942),
	"L30": (424.08002, 903.9111),
	"L31": (481.83304, 904.4575),
	"L32": (540.14404, 905.004),
	"L33": (598.176, 901.72504),
	"L34": (271.18802, 433.92102),
	"L35": (290.71802, 380.364),
	"L36": (315.828, 327.90002),
	"L37": (165.16801, 1121.4181),
	"L38": (197.53201, 1184.812),
	"L39c": (813.28503, 1384.148),
	"L40": (973.15204, 560.70905),
	"L41": (562.46405, 173.787),
	"L42": (639.468, 171.60101),
	"L43": (716.47205, 171.60101),
	"L48": (791.80206, 1176.6145),
	"L49": (804.07806, 1230.1715),
	"L50": (813.564, 1286.461),
	"L51": (828.072, 1340.0181),
	"L4": (504.8437, 1125.7233),
	"L5": (408.56357, 873.95306),
	"L6": (481.30615, 873.32874),
	"L19a": (199.38988, 1206.3896),
	"L19b": (253.0087, 1120.4105),
	"L19c": (309.68234, 1033.1263),
	"L20a": (665.6274, 1192.0807),
	"L20b": (617.81805, 1115.7792),
	"L20c": (572.56354, 1037.419),
	"L44": (436.48825, 1293.3828),
	"L45": (425.92465, 1239.8275),
	"l46": (414.54755, 1189.8959),
	"l47": (404.23398, 1137.2183),
	"Credits": (112.1933775, 1919.16115),
	"BallsInPlay": (181.343505, 1918.928925),
	"BonusDisplay": (512.52302, 1647.2118500000001),
}
LOWER_PLAYFIELD_OBJECTS = frozenset({
	"Bumper5", "Bumper6", "Sling7", "Sling8", "Sling9", "TargetLL40", "TargetLL50", "TargetLL60", "TargetLL70",
	"TargetLR41", "TargetLR51", "TargetLR61", "sw42", "sw43", "sw52", "sw53", "Tri_sw62",
	"L4", "L5", "L6", "L19a", "L19b", "L19c", "L20a", "L20b", "L20c", "L44", "L45", "l46", "l47",
})
LOWER_NOTE = (
	"A lower-playfield device: the retained table models the lower playfield in the same plan as the upper one, below "
	"the window, so this coordinate is the device's projection into the shared playfield space, as the player sees it "
	"through the window or under the upper playfield."
)


def midpoint(*names: str) -> tuple[float, float]:
	points = [TABLE_POINTS[name] for name in names]
	return sum(x for x, _ in points) / len(points), sum(y for _, y in points) / len(points)


# --- Switches -------------------------------------------------------------------------------------
# address: (label, manual name as printed on the matrix sheet, wire, location, switch type, table objects, extra note)
UPPER_SWITCHES: dict[int, tuple[str, str, str, str, str, tuple[str, ...], str]] = {
	0: ("Top #1 Rollover", "TOP #1 ROLLOVER", "111", "upper playfield, left of the three top lanes", "leaf", ("Tri_TopLeft",), ""),
	1: ("#1 Spot Target", "#1 SPOT TARGET", "344", "upper playfield, right side of the window, top of the four yellow spot targets", "leaf", ("Tsw01",), ""),
	2: ("Right #1 Drop Target \"H\"", "RIGHT #1 DROP TARGET \"H\"", "033", "upper playfield, right drop bank, top target", "leaf", ("TargetH",), "Through A9J2/A9P2 pin 1."),
	3: ("Left #1 Drop Target \"B\"", "LEFT #1 DROP TARGET \"B\"", "100", "upper playfield, left drop bank, lowest target", "leaf", ("TargetB",), "Through A9J3/A9P3 pin 1."),
	4: ("Left #4 Drop Target \"C\"", "LEFT #4 DROP TARGET \"C\"", "166", "upper playfield, left drop bank, fourth target from the bottom", "leaf", ("TargetC",), "Through A9J3/A9P3 pin 4."),
	5: ("Ball Kicker Hole Switch (Upper Capture Hole)", "BALL KICKER HOLE SWITCH", "800", "upper playfield, kick-out hole at the left edge", "leaf", ("sw05",), ""),
	6: ("Pop Bumpers (4)", "POP BUMPERS (4)", "855", "upper playfield, the four pop bumpers", "leaf", ("Bumper1", "Bumper2", "Bumper3", "Bumper4"), "One matrix address for all four upper pop bumpers' scoring contacts; each bumper's coil is fired by its own pop bumper driver board, not by the controller."),
	10: ("Top #2 Rollover", "TOP #2 ROLLOVER", "133", "upper playfield, middle of the three top lanes", "leaf", ("Tri_TopMid",), ""),
	11: ("#2 Spot Target", "#2 SPOT TARGET", "355", "upper playfield, right side of the window, second spot target", "leaf", ("Tsw11",), ""),
	12: ("Right #2 Drop Target \"O\"", "RIGHT #2 DROP TARGET \"O\"", "055", "upper playfield, right drop bank, second target", "leaf", ("TargetO",), "Through A9J2/A9P2 pin 2."),
	13: ("Left #2 Drop Target \"L\"", "LEFT #2 DROP TARGET \"L\"", "122", "upper playfield, left drop bank, second target from the bottom", "leaf", ("TargetL",), "Through A9J3/A9P3 pin 2."),
	14: ("Left #5 Drop Target \"K\"", "LEFT #5 DROP TARGET \"K\"", "177", "upper playfield, left drop bank, top target", "leaf", ("TargetK",), "Through A9J3/A9P3 pin 5."),
	15: ("Outhole", "OUTHOLE", "833", "upper playfield, outhole below the flippers", "leaf", ("Drain",), ""),
	16: ("Left Spinning Target", "LEFT SPINNING TARGET", "811", "upper playfield, spinner in the left lane", "leaf", ("Spinner1",), ""),
	20: ("Top #3 Rollover", "TOP #3 ROLLOVER", "144", "upper playfield, right of the three top lanes", "leaf", ("Tri_TopRight",), ""),
	21: ("#3 Spot Target", "#3 SPOT TARGET", "366", "upper playfield, right side of the window, third spot target", "leaf", ("Tsw21",), ""),
	22: ("Right #3 Drop Target \"L\"", "RIGHT #3 DROP TARGET \"L\"", "066", "upper playfield, right drop bank, third target", "leaf", ("TargetL2",), "Through A9J2/A9P2 pin 3."),
	23: ("Left #3 Drop Target \"A\"", "LEFT #3 DROP TARGET \"A\"", "155", "upper playfield, left drop bank, middle target", "leaf", ("TargetA",), "Through A9J3/A9P3 pin 3."),
	24: ("Top Lane Rollunder Switch", "TOP LANE ROLLUNDER SWITCH", "844", "upper playfield, rollunder gate at the top of the left lanes", "leaf", ("Gate_TopLeft",), ""),
	25: ("3rd Position Ball Return (Trough)", "3RD POSITION BALL RETURN (TROUGH)", "333", "ball return trough below the playfield", "leaf", ("kicker3",), "The only trough switch: the manual requires all three balls in the ball return trough to start a game, and the ROM serves a ball only while this switch is closed."),
	26: ("Tilt Switch (Playboard)", "TILT SWITCH (PLAYBOARD)", "011", "upper playfield, mounted on the playboard; the location drawing prints SW26 at the lower left above the apron", "tilt", (), "The retained table writes its nudge tilt here (vpmNudge.TiltSwitch=26). In the ROM's switch test it is an ordinary address that shows 26; closing it once during play tilts the game (lamp 1, the T relay, energizes, solenoid 11 rises and the game-on solenoid 10 drops)."),
	30: ("Right Side Rollover", "RIGHT SIDE ROLLOVER", "300", "upper playfield, right-hand lane beside the right drop bank", "leaf", ("Tri_MidRightLane",), ""),
	31: ("#4 Spot Target", "#4 SPOT TARGET", "377", "upper playfield, right side of the window, bottom spot target", "leaf", ("Tsw31",), ""),
	32: ("Right #4 Drop Target \"E\"", "RIGHT #4 DROP TARGET \"E\"", "077", "upper playfield, right drop bank, bottom target", "leaf", ("TargetE",), "Through A9J2/A9P2 pin 4."),
	33: ("Black Hole Rollover", "BLACK HOLE ROLLOVER", "822", "upper playfield, U-shaped lane at the upper left that leads down to the lower playfield", "leaf", ("Tri_BlackHole",), "Closing it during play energizes the U relay (lamp 16) and the L relay (lamp 17), handing the flippers and illumination to the lower playfield (gameplay harness run)."),
	34: ("10 Point Switches (5)", "10 POINT SWITCHES (5)", "044", "upper playfield, five rebound rubbers: beside the left and right drop banks, on the left rail below the capture hole, above the left kicking rubber and beside the post left of the right return lane", "leaf", ("Sling4", "Sling5", "Sling1", "Sling3", "Sling6"), "Five contacts in parallel on one address. The retained table also pulses 34 from its right kicking rubber (Sling2), where the location drawing prints no SW34; that object is not placed."),
	35: ("Right Return Rollover", "RIGHT RETURN ROLLOVER", "711", "upper playfield, right return lane", "leaf", ("Tri_LeftInlane",), "The retained table names the trigger Tri_LeftInlane although it sits in the right return lane; its handler writes 35."),
}
LOWER_SWITCHES: dict[int, tuple[str, str, str, str, str, tuple[str, ...], str]] = {
	40: ("Lower Left #1 Drop Target", "LEFT #1 DROP TARGET", "700", "lower playfield, yellow four-bank, nearest the player", "leaf", ("TargetLL40",), ""),
	41: ("Lower Right #1 Drop Target", "RIGHT #1 DROP TARGET", "744", "lower playfield, white three-bank, right end", "leaf", ("TargetLR41",), ""),
	42: ("Lower Hole Kicker Switch (Lower Capture Hole)", "HOLE KICKER SWITCH", "533", "lower playfield, capture hole at the lower left", "leaf", ("sw42",), ""),
	43: ("Ball Tube Kicker Switch", "BALL TUBE KICKER SWITCH", "844", "lower playfield, the ball lift's kicker at the foot of the re-entry tube (the backbox end of the lower playfield, right side)", "leaf", ("sw43",), "Closing it during lower-playfield play fires the ball lift (lamp 14) and releases the U and L relays (lamps 16 and 17), handing play back to the upper playfield (gameplay harness run)."),
	50: ("Lower Left #2 Drop Target", "LEFT #2 DROP TARGET", "711", "lower playfield, yellow four-bank, second target", "leaf", ("TargetLL50",), ""),
	51: ("Lower Right #2 Drop Target", "RIGHT #2 DROP TARGET", "755", "lower playfield, white three-bank, middle target", "leaf", ("TargetLR51",), ""),
	52: ("Rollunder Gate", "ROLLUNDER GATE", "566", "lower playfield, rollunder gate at the lower right", "leaf", ("sw52",), ""),
	53: ("Track Switch", "TRACK SWITCH", "855", "lower playfield, the entry track along the top guide rail where the ball waits at the lower ball gate", "leaf", ("sw53",), "Closing it with the lower playfield selected fires the lower ball gate (lamp 8) once (gameplay harness run)."),
	60: ("Lower Left #3 Drop Target", "LEFT #3 DROP TARGET", "722", "lower playfield, yellow four-bank, third target", "leaf", ("TargetLL60",), ""),
	61: ("Lower Right #3 Drop Target", "RIGHT #3 DROP TARGET", "766", "lower playfield, white three-bank, left end", "leaf", ("TargetLR61",), ""),
	62: ("Lower Return Rollover", "RETURN ROLLOVER", "577", "lower playfield, the left lane", "leaf", ("Tri_sw62",), ""),
	70: ("Lower Left #4 Drop Target", "LEFT #4 DROP TARGET", "733", "lower playfield, yellow four-bank, farthest from the player", "leaf", ("TargetLL70",), ""),
	71: ("Lower Level Pop Bumpers (2)", "LOWER LEVEL POP BUMPERS (2)", "777", "lower playfield, the two pop bumpers", "leaf", ("Bumper5", "Bumper6"), "One matrix address for both lower pop bumpers' scoring contacts; each bumper's coil is fired by its own pop bumper driver board."),
	72: ("10 Point Switches and Kicking Target", "10 POINT SWITCHES AND KICKING TARGET", "288", "lower playfield: the kicking target on the left lane wall, the kicking rubber at the upper right and the rubber at the lower right", "leaf", ("Sling7", "Sling8", "Sling9"), "Several contacts in parallel on one address. The kicking target's and the kicking rubber's coils are fired by their own switches, not by the controller."),
}
UNUSED_MATRIX = (36, 44, 45, 46, 54, 55, 56, 63, 64, 65, 66, 73, 74, 75, 76)
UNKNOWN_RETURN_7 = (57, 67, 77)
SWITCH_RUNTIME_NOTE = (
	"In the ROM's own Step 18 switch test (harness runs switch-test-a to -e) the status display reads 99 with every switch "
	"open and shows {n:02d} while this address alone is held closed."
)
POLARITY_NOTE = (
	"Normally open: riot6532_0a_r hands the ROM the matrix bits unmodified and Black Hole's driver declares a zero invSw, so "
	"public 1 is the closed contact, and the ROM's switch test reports the address at 1."
)
DROP_TARGET_NOTE = " The retained table pulses this address briefly when its target drops (vpmTimer.PulseSw)."
STROBE_WIRES = ("400", "411", "422", "433", "444", "455", "466", "477")
RETURN_WIRES = ("600", "611", "622", "633", "644", "655", "666")


def matrix_wiring(address: int, wire: str) -> dict[str, Any]:
	strobe, ret = divmod(address, 10)
	lower = strobe >= 4
	wiring: dict[str, Any] = {
		"board": "A1 control board, switch matrix",
		"drive_connection": f"strobe {strobe}, A1J6-{strobe + 1}" + (f" through A9J7/A9P7-{strobe - 3}" if lower else ""),
		"return_connection": f"return {ret}, A1J6-{ret + 10}" + (f" through A9J7/A9P7-{ret + 5}" if lower else ""),
		"return_component": f"1N270 diode; cell wire {wire} as printed",
		"drive_wire": STROBE_WIRES[strobe],
		"return_wire": RETURN_WIRES[ret],
	}
	return wiring


# --- Generic helpers ---------------------------------------------------------------------------------

def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Black Hole retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Black Hole extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Black Hole retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Black Hole retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Black Hole retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT or sum(item["size"] for item in actual["files"]) != EXTRACTION_TOTAL_BYTES:
		raise RuntimeError("Black Hole retained extraction file count or size changed")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


GEOMETRY_REFS = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, VPX_EXTRACTION_SOURCE)


def located(identifier: str, role: str, objects: tuple[str, ...] | list[tuple[float, float]], *refs: str, status: str = "observed") -> dict[str, Any]:
	points = [TABLE_POINTS[name] if isinstance(name, str) else name for name in objects]
	placements = []
	for index, point in enumerate(points, start=1):
		x, y = norm(*point)
		placements.append({
			"id": f"{identifier}.{role}" + (f".{index}" if len(points) > 1 else ""),
			"role": role, "space": "playfield", "x": x, "y": y,
			"provenance": provenance(*(refs or GEOMETRY_REFS), status=status),
		})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def _excerpt(identifier: str, locator: str, filename: str, *, image: tuple[str, str] | None = None, credit: str = "curator, read from the rendered page images") -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	excerpt = {
		"id": f"excerpt.black-hole.{identifier}", "locator": locator, "path": path.relative_to(ROOT).as_posix(),
		"sha256": _file_sha256(path), "method": "manual", "transcribed_by": credit, "reviewed": True,
	}
	if image:
		image_path = EXCERPT_DIRECTORY / image[0]
		excerpt.update({"image": image_path.relative_to(ROOT).as_posix(), "image_sha256": _file_sha256(image_path), "image_derivation": image[1]})
	return excerpt


IMAGE_DERIVATIONS = {
	"switch-matrix": "scribd-223467608 page image 45.jpg (904x1155 JPEG, SHA-256 2e1ffa59c08fdf005e55c0088c8be82697620cabfc045c4cfd385bf43de50ed1), crop box 0.02,0.07,0.99,0.96 at the image's own resolution, grayscale, 877x1028 WebP quality 75, Pillow 12.3.0",
	"upper-playfield-assignments": "scribd-223467608 page image 44.jpg (904x1160 JPEG, SHA-256 f8f85e6bb09f9e515d72e1eb92f9021e325f8137e067f3072da80212cc88b94c), crop box 0.03,0.07,0.99,0.97 at the image's own resolution, grayscale, 868x1044 WebP quality 75, Pillow 12.3.0",
	"lower-playfield-assignments": "scribd-223467608 page image 42.jpg (904x1160 JPEG, SHA-256 5054f3a7beaf8792a19f1395901d22bf8a29562d8367596b548849d8cefdbb13), crop box 0.06,0.18,0.99,0.82 at the image's own resolution, grayscale, 841x742 WebP quality 75, Pillow 12.3.0",
	"controlled-solenoids-and-illumination": "scribd-223467608 page image 46.jpg (904x1150 JPEG, SHA-256 d0bc29db46d6b5b70186671e35ab7e7b3c87a901dcad2ed8340eb1962a76388d), crop box 0.0,0.03,1.0,0.94 at the image's own resolution, grayscale, 904x1047 WebP quality 70, Pillow 12.3.0",
	"non-controlled-solenoids-and-illumination": "scribd-223467608 page image 47.jpg (904x1158 JPEG, SHA-256 985f1fbc2b611e61794ffa213421b0417e4860ca95962fb7d24fd30cb7d86471), crop box 0.0,0.02,1.0,0.96 at the image's own resolution, grayscale, 904x1089 WebP quality 70, Pillow 12.3.0",
	"driver-board-outputs": "idoc-jlk9z9rz1545 page image 27.jpg (1230x1572 JPEG, SHA-256 ab2efa9c9c5605390fd45f634323540a28be5a3ae2da534c7177aae7b66021d8), crop box 0.0,0.06,1.0,0.94 at the image's own resolution, grayscale, 1230x1384 WebP quality 70, Pillow 12.3.0",
}


def _image(name: str) -> tuple[str, str]:
	return f"{name}.webp", IMAGE_DERIVATIONS[name]


def _run_locator(name: str) -> str:
	game, run_sha, scenario, scenario_sha = HARNESS_RUNS[name]
	return (
		f"LibPinMAME harness run of {game} with tools/run_pinmame_harness.py, library pinmame64.dll built from the pinned PinMAME "
		f"revision (SHA-256 {LIBRARY_SHA256}), ROM archive {game}.zip from the operator's authorized ROM corpus (SHA-256 "
		f"{ROM_ARCHIVE_SHA256[game]}, CRCs and SHA-1s matching the pinned driver), from a new empty state directory; System 80 "
		f"boots straight into attract mode, so no NVRAM initialization run is needed. Scenario {SCENARIO_DIRECTORY}/{scenario} "
		f"(SHA-256 {scenario_sha}). {RUN_FINDINGS[name]} The run directory (run.json, a copy of the scenario and the state "
		f"directory) is pinned by external:pinmame-runtime-evidence/{RUNTIME_DIRECTORY}/manifest.json ({RUNTIME_MANIFEST[0]} files, "
		f"{RUNTIME_MANIFEST[1]} bytes, SHA-256 {RUNTIME_MANIFEST[2]}). No ROM bytes or NVRAM are retained in this repository."
	)


RUN_FINDINGS = {
	"lamp-driver-test": "Self/Test (07) then Credit (47) start Step 16, which pulses lamp 0 (with synthetic solenoid 10) twice, lamp 1 (with synthetic solenoid 11) twice and lamp 2 twice, then chases lamps 3-47 in ascending order, with 48-51 always the inverse of 44-47.",
	"solenoid-test": "Step 17 pulses public solenoids 1, 2, 5, 6, 8 and 9 in order, each about 0.15 s, while the status display shows the same number (1, 2, 5, 6, 8, 9) and the credit display shows 17; solenoids 3, 4 and 7 (the coin counters, the manual's Note B) are not pulsed.",
	"switch-test-a": "Step 18 shows 99 with every switch open and the address's own number while each of 00-06, 10-17 and 20-22 is held alone; the ROM then leaves the test about 127 s after entering it, before 23 is shown.",
	"switch-test-b": "Step 18 shows 99 with every switch open and the address's own number while each of 26, 27, 30-37, 40-46 and 50 is held alone (including the empty matrix cells 36 and 44-46).",
	"switch-test-c": "Step 18 shows 99 with every switch open and the address's own number while each of 54, 55 and 56 is held; closing 57 leaves the test with the displays blank, as the manual's 'close tilt switch' exit says.",
	"switch-test-d": "Step 18 shows the address's own number while each of 23-25, 51-53, 60-67 and 70-73 is held alone.",
	"switch-test-e": "Step 18 shows the address's own number while each of 74, 75 and 76 is held; closing 77 leaves the test like 57 does.",
	"gameplay-causality": "Coins on 17, 27 and 37 pulse solenoids 3, 4 and 7; the right flipper button (112) publishes nothing before a game; Credit (47) energizes lamp 0 and raises solenoid 10, pulses the four bank resets 1, 2, 5, 6 and the outhole kicker 9, and lights lamps 15 and 10 together for 2.5 s; during play 112 publishes 45/46 and 114 publishes 47/48; completing B-L-A-C-K (03, 13, 23, 04, 14) pulses solenoid 2 and completing H-O-L-E (02, 12, 22, 32) pulses solenoid 1; holding 05 before the capture is enabled pulses lamp 13 repeatedly, and after the four spot targets 01-31 it holds the ball and serves a new one (lamps 15 and 10); 33 energizes lamps 16 and 17; 53 pulses lamp 8; 52, 71, 72, 62 and the lower drop targets change no driver output; 43 pulses lamp 14, releases lamps 16, 17 and 18 and pulses solenoids 6, 5 and the knocker 8; the outhole 15 pulses solenoid 9 repeatedly while held and the captured upper ball is kicked out with lamp 13.",
	"high-game-to-date": "After a game that ends with a non-zero score, starting a second game lights lamp 10 for 2.5 s while all four player displays and the lower playfield display show the high game to date (770000) and lamp 15 releases the ball, exactly as the manual's III.A.5.b describes; lamp 11 flashes at about 2 Hz throughout game-over attract mode and stops when a game starts.",
	"tilt-26": "Closing 26 once during play energizes lamp 1 (the T relay) and synthetic solenoid 11 and drops solenoid 10.",
	"tilt-57": "Closing 57 once during play energizes lamp 1 (the T relay) and synthetic solenoid 11 and drops solenoid 10, exactly as 26 does.",
	"tilt-77": "Closing 77 once during play blanks the ball-in-play and credit displays, and about two seconds later every output and display stops changing for the rest of the 20 s observation.",
	"slam": "Setting -1 to 1 for 0.5 s during play ends the game: lamp 0 and solenoid 10 drop and lamp 11 resumes its attract-mode flashing.",
	"blkhole2-service": "The rev. 2 game ROM fires solenoids 1, 2, 5, 6, 8 and 9 in Step 17 and shows 33 in Step 18 for switch 33, as blckhole does; same display layout.",
	"blkholea-service": "The sound-only (668A) game ROM on the sound-only board fires solenoids 1, 2, 5, 6, 8 and 9 in Step 17 and shows 33 in Step 18 for switch 33, as blckhole does; same display layout.",
	"blkhole7-service": "The Oliver seven-digit conversion fires solenoids 1, 2, 5, 6, 8 and 9 in Step 17 and shows 33 for switch 33; its four player displays are seven digits wide at the same memory starts and the lower playfield display is unchanged.",
	"blkhol7s-service": "The Oliver seven-digit sound-only conversion fires solenoids 1, 2, 5, 6, 8 and 9 in Step 17 and shows 33 for switch 33; its four player displays are seven digits wide at the same memory starts.",
}


def source_records() -> list[dict[str, Any]]:
	sources: list[dict[str, Any]] = [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog records for blckhole (Black Hole (rev. 4)), its clones blkhole2 (rev. 2) and blkhole7 (Oliver 7-digit conversion), and the sound-only root blkholea with its clone blkhol7s",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/gts80games.c lines 34-39 dispNumeric2 (four 6-digit player displays at memory 2, 9, 22 and 29, DISP_SEG_CREDIT(40,41), "
				"DISP_SEG_BALLS(42,43) and a fifth 6-digit display at 50) and dispNumeric4 (the same with 7-digit player displays and the fifth "
				"display at layout column 9), lines 53-79 INIT_S80 and INIT_S80D7 (GEN_GTS80, hw.flippers 0, zero invSw, lampCol 0, the stock u2_80/u3_80 "
				"or Oliver u2g807dc/u3g807dc system ROMs), lines 433-481: INIT_S80(blckhole, dispNumeric2, SNDBRD_GTS80SS_VOTRAX) with 668-4.cpu, "
				"INIT_S80D7(blkhole7, dispNumeric4, SNDBRD_GTS80SS_VOTRAX), INIT_S80(blkhole2, ...) with 668-2.cpu, INIT_S80(blkholea, dispNumeric2, "
				"SNDBRD_GTS80S) with 668-a2.cpu and 668-a-s.snd, INIT_S80D7(blkhol7s, dispNumeric4, SNDBRD_GTS80S) and their CORE_CLONEDEFNV lines; "
				"src/wpc/gts80.c GTS80_vblank (lamps 0 and 1 published as solenoids 10 and 11, core_updateSw(gameOn & 1)), GTS80_sw2m/GTS80_m2sw, "
				"GTS80_lamp2m/GTS80_m2lamp, SWITCH_UPDATE(GTS80), riot6532_0a_r, slam_sw_r, riot6532_2a_w (solenoids 1-9, sound command with lamp 9 as "
				"Sound 16), riot6532_2b_w (twelve lamp latches and the inverted twelfth column at 48-51), MACHINE_INIT(gts80); src/wpc/gts80.h "
				"GTS80_COMPORTS, GTS80_DIPS, GTS80_SNDDIPS, GTS80_SWSLAMTILT; src/wpc/gts80s.c gts80s_init and gts80ss_init DIP reads; src/wpc/gen.h "
				"GEN_GTS80 (0x200000000); src/wpc/core.c core_updateSw and core_getSol"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/gts80.json", "revision": "repository",
			"locator": "Gottlieb System 80 public address rules: strobe*10+return switch numbers 0-77, dedicated inputs -8 to -1 (slam -1, sound test -4), the synthetic flipper column 111-118, DIPs 1-42, solenoids 1-9 with synthetic 10 (game on) and 11 (tilt relay), synthetic flipper outputs 45-48, lamps 0-63 with the inverted 48-51, and one physical-output-mode GI channel",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "https://www.scribd.com/doc/223467608/Gottlieb-Black-Hole-Instruction-Manual",
			"sha256": MANUAL_SCRIBD_MANIFEST_SHA256,
			"locator": (
				"Gottlieb Black Hole (Game #668) Instruction Manual, final edition 'applicable to all games not having the letter S in their serial "
				"number', 53 pages as served by Scribd's viewer (uploader Tatooinesky). The 53 page images were downloaded unmodified from "
				"html.scribdassets.com and are retained at external:pinmame-manuals/by-machine/gottlieb.black-hole.1981/scribd-223467608/pages/; "
				"sha256 is that of the canonical page manifest pages.manifest.json, which lists every page's URL, size and SHA-256. Printed page = "
				"viewer page - 2. The fold-out schematic sheets are cropped at the right edge in this copy (printed pages 35, 44 and 47)."
			),
			"license": "NOASSERTION", "attribution": "D. Gottlieb & Co.; scan uploaded to Scribd by Tatooinesky",
			"acquired_at": "2026-10-09T16:20:00Z",
			"excerpts": [
				_excerpt("switch-matrix", "Printed page 43, drawing E-21340 upper and lower playfield switch matrix, every cell", "switch-matrix.md", image=_image("switch-matrix")),
				_excerpt("upper-playfield-assignments", "Printed page 42, top playfield switch and lamp assignments and the location drawing", "upper-playfield-assignments.md", image=_image("upper-playfield-assignments")),
				_excerpt("lower-playfield-assignments", "Printed pages 39-40, bottom playboard parts, switch and lamp assignments and the location drawing", "lower-playfield-assignments.md", image=_image("lower-playfield-assignments")),
				_excerpt("controlled-solenoids-and-illumination", "Printed page 44, playfields 'controlled' solenoids and illumination", "controlled-solenoids-and-illumination.md", image=_image("controlled-solenoids-and-illumination")),
				_excerpt("non-controlled-solenoids-and-illumination", "Printed page 45, playfields 'non-controlled' solenoids and illumination", "non-controlled-solenoids-and-illumination.md", image=_image("non-controlled-solenoids-and-illumination")),
				_excerpt("lightbox-and-displays", "Printed pages 34, 35 (left part) and 38: auxiliary lamp driver board, light box and four-digit display", "lightbox-and-displays.md"),
			],
		},
		{
			"id": MANUAL_IDOC_SOURCE, "kind": "manual",
			"uri": "https://idoc.pub/documents/gottlieb-black-hole-instruction-manual-jlk9z9rz1545",
			"sha256": MANUAL_IDOC_MANIFEST_SHA256,
			"locator": (
				"A second, sharper scan of the same Black Hole instruction manual on idoc.pub (uploaded November 2019), 30 pages ending after printed "
				"page 28. The background page images of its pdf2htmlEX viewer were downloaded unmodified (the site's PDF link returned HTTP 404) and "
				"are retained with the viewer HTML at external:pinmame-manuals/by-machine/gottlieb.black-hole.1981/idoc-jlk9z9rz1545/; sha256 is that "
				"of its canonical page manifest. Used for the driver-board schematic, self test, operation, adjustments and general information pages."
			),
			"license": "NOASSERTION", "attribution": "D. Gottlieb & Co.; scan hosted by idoc.pub",
			"acquired_at": "2026-10-09T16:15:00Z",
			"excerpts": [
				_excerpt("driver-board-outputs", "Printed pages 25-26, drawing E-20915 driver board (A3): lamp latches, transistors and connector pins, solenoid and sound lines", "driver-board-outputs.md", image=_image("driver-board-outputs")),
				_excerpt("self-test", "Printed pages 12-13, bookkeeping and self test text, flow chart and notes A-D", "self-test.md"),
				_excerpt("game-operation", "Printed pages 5-9, initialization, game operation and game play", "game-operation.md"),
				_excerpt("adjustments", "Printed pages 11-12, control board switches S1-S32 and sound/speech switch bank SB1", "adjustments.md"),
				_excerpt("general-information", "Cover, contents and PROM list, printed pages 15-18 (boards, wire colours, fuses, coil chart, sound board test) and printed page 29 (System 80 sound circuitry, from the Scribd copy)", "general-information.md"),
			],
		},
		{
			"id": IPDB_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=307", "sha256": IPDB_PAGE_SHA256,
			"locator": (
				"IPDB machine 307: Black Hole, D. Gottlieb & Co., October 1981, model 668, Gottlieb System 80, widebody, 8,774 units; notable features "
				"six flippers, six pop bumpers, three slingshots, the 5-, 4- and 3-bank drop targets, two kick-out holes, a kick target, a rollunder, a "
				"right outlane ball detour gate, a score display in the playfield, the rotating backglass disc and multiball with speech on non-export "
				"games. Retrieved through the Wayback capture of 2025-12-30 (retained page SHA-256 above) with four photographs from the live site "
				"(external:pinmame-manuals/by-machine/gottlieb.black-hole.1981/ipdb-307/)."
			),
			"license": "NOASSERTION", "attribution": "The Internet Pinball Database",
			"acquired_at": "2026-10-09T16:30:00Z",
			"excerpts": [_excerpt("ipdb-307", "Machine page fields, notable features and the four photographs used", "ipdb-307.md", credit="curator, quoted from the retained page and photographs")],
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/gottlieb/black-hole-1981/source/Black%20Hole%20(Gottlieb%201981)%20vpx%201.1.vpx",
			"sha256": TABLE_SHA256, "original_filename": "Black Hole (Gottlieb 1981) vpx 1.1.vpx", "revision": "vpx 1.1",
			"locator": (
				f"Community recreation by cyberpez, version 1.1 (file dated 2020-01-20), from the operator's table archive, with its backglass "
				f"'Black Hole (Gottlieb 1981) vpx 1.1.directb2s' (SHA-256 {DIRECTB2S_SHA256}). Exact playfield bounds {TABLE_BOUNDS}; normalized "
				"coordinates are x/1116 and y/2186. The table draws the lower playfield in the same plan as the upper one, under the window. "
				f"Geometry authority for named objects; a normalized candidate dump is retained at external:pinmame-review-artifacts/black-hole-1981/vpx-spatial-candidates.json (SHA-256 {SPATIAL_CANDIDATES_SHA256})."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "cyberpez",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": "external:pinmame-vpx-sources/gottlieb/black-hole-1981/extracted-vpxtool/black-hole-gottlieb-1981-vpx-1.1/script.vbs",
			"sha256": SCRIPT_SHA256, "original_filename": "script.vbs",
			"locator": (
				"Embedded script of the retained table, 3182 lines: LoadVPM sys80.VBS, RomSet 5 (blkhole7) by default with blckhole, blkhole2, blkholea "
				"and blkhol7s selectable, UseSolenoids=1. Runtime authority for the switch handlers, the four drop-bank and outhole SolCallbacks (1, 2, "
				"5, 6, 9), the knocker (8), sLRFlipper/sLLFlipper gated by Controller.Lamp(16) and Controller.Lamp(17), the lamp-driven devices in "
				"CheckSolenoid (lamps 8 and 12-18) and the Lights()/UpdateLamps lamp bindings. The pinned corpus copy 'Black Hole (Gottlieb 1981) vpx "
				f"1.1.vbs' (sverrewl/vpxtable_scripts {VPXTABLE_SCRIPTS_REVISION[:12]}) is a later Thalamus revision of the same script with different "
				"option defaults and FFv2/cvpmflips additions."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "cyberpez",
			"excerpts": [_excerpt("vpx-script-bindings", "Every line that binds a controller address or decides what an address drives, quoted with line numbers", "vpx-script-bindings.md", credit="curator, quoted from the extracted script")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/gottlieb/black-hole-1981/extracted-vpxtool/black-hole-gottlieb-1981-vpx-1.1.manifest.json",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under "
				f"extracted-vpxtool/black-hole-gottlieb-1981-vpx-1.1: {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced "
				f"with vpxtool git:v0.33.3 from the retained table. Bounds {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sys80.vbs",
			"sha256": VPM_SYS80_SHA256, "original_filename": "sys80.vbs",
			"locator": (
				"VPinMAME System 80 script library the retained table loads (LoadVPM ... \"sys80.VBS\"), retained from the contributor's working "
				f"installation beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). Lines 21-34 define GameOnSolenoid = 10, swTest = 07, "
				"swCoin1-3 = 17/27/37, swStartButton = 47, swTilt = 57, swSlamTilt = -1, swLRFlip = 112 and swLLFlip = 114; vpmKeyDown/vpmKeyUp "
				"write them from the cabinet keys."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-sys80-library", "Lines 18-34 and the vpmKeyDown/vpmKeyUp switch writes (lines 82-135)", "vpm-sys80-library.md", credit="curator, quoted from the library file")],
		},
		{
			"id": SISTER_SCRIPTS_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts", "revision": VPXTABLE_SCRIPTS_REVISION,
			"locator": (
				"Pinned corpus scripts of other Gottlieb System 80 tables that bind the two lightbox lamps by number: 'Amazing Spider-man (Gottlieb "
				"1980).vbs' lines 658 and 679 (Lamp 10 'HIGH SCORE TO DATE', 'high game to date - backbox'), 'Eclipse (Gottlieb 1982).vbs' lines 801 "
				"and 815 (Lamp 11 GAME OVER, Lamp 10 HIGH SCORE TO DATE), \"Goin' Nuts (Gottlieb 1983).vbs\" lines 1835-1836 (Lamp 10 Highscore, Lamp "
				"11 Game Over) and 'Alien Star (Gottlieb 1984) 2.0_Thal.vbs' lines 264 and 278. Used only as corroboration of the platform-wide role "
				"of lamps 10 and 11; Black Hole's own runs and manual decide."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Community table authors; pinned copies in sverrewl/vpxtable_scripts",
		},
	]
	for name in HARNESS_RUNS:
		sources.append({
			"id": RUN_SOURCE[name], "kind": "runtime_scenario",
			"uri": f"external:pinmame-runtime-evidence/{RUNTIME_DIRECTORY}/{name}/run.json",
			"revision": PINMAME_REVISION, "sha256": HARNESS_RUNS[name][1],
			"locator": _run_locator(name),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		})
	return sources


# --- Inputs ------------------------------------------------------------------------------------------

MANUAL_SWITCH_REFS = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE)


def _switch(address: int, data: tuple[str, str, str, str, str, tuple[str, ...], str], lower: bool) -> dict[str, Any]:
	label, printed, wire, location, switch_type, objects, extra = data
	notes = [f"Printed on the matrix sheet as \"{printed}\" (SW.{address:02d}, strobe {address // 10}, return {address % 10})."]
	if extra:
		notes.append(extra)
	if "Drop Target" in label:
		notes.append(DROP_TARGET_NOTE.strip())
	notes.append(SWITCH_RUNTIME_NOTE.format(n=address))
	notes.append(POLARITY_NOTE)
	if lower:
		notes.append(LOWER_NOTE)
	device: dict[str, Any] = {
		"id": f"switch.{slug(label)}",
		"label": label,
		"kind": "switch",
		"binding": {"group": SWITCH, "device": address},
		"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
		"availability": "used",
		"normally_closed": False,
		"physical": {"location": location, "switch_type": switch_type, "notes": " ".join(notes)},
		"wiring": matrix_wiring(address, wire),
		"provenance": provenance(*MANUAL_SWITCH_REFS, *SWITCH_TEST_SOURCES),
	}
	if objects:
		device["spatial"] = located(device["id"], "sensor", objects)
	return device


CABINET_SWITCHES = {
	7: ("Self/Test Button", "service.self-test", "front door", "button", "The SELF/TEST button inside the front door (manual section VII): one press enters bookkeeping, and Credit then starts the self test (Steps 16-20). PinMAME's GTS80_COMPORTS names it Test and sys80.vbs swTest = 07. Every harness run's test entry presses it."),
	17: ("Coin Switch, Left Chute", "cabinet.coin-1", "coin door", "leaf", "The left coin chute: a coin closure pulses coin counter solenoid 3 (gameplay harness run) and adds credits per switches S1-S4. GTS80_COMPORTS Coin 1, sys80.vbs swCoin1 = 17."),
	27: ("Coin Switch, Right Chute", "cabinet.coin-2", "coin door", "leaf", "The right coin chute: a coin closure pulses coin counter solenoid 4 (gameplay harness run) and adds credits per switches S5-S8. GTS80_COMPORTS Coin 2, sys80.vbs swCoin2 = 27."),
	37: ("Coin Switch, Center Chute", "cabinet.coin-3", "coin door", "leaf", "The center coin chute: a coin closure pulses coin counter solenoid 7 (gameplay harness run) and adds credits per switches S9-S12. GTS80_COMPORTS Coin 3, sys80.vbs swCoin3 = 37."),
	47: ("Credit (Replay) Button", "cabinet.start", "front door", "button", "The Credit button on the front door, which the manual also calls the replay button: it starts a game and adds players, and in bookkeeping and self test it resets a step or starts and repeats a test. GTS80_COMPORTS Start, sys80.vbs swStartButton = 47."),
}
CABINET_REFS = (MANUAL_SOURCE, MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE)


def input_devices() -> list[dict[str, Any]]:
	devices: list[dict[str, Any]] = []
	# Dedicated inputs in internal column 0.
	devices.append({
		"id": "switch.slam", "label": "Slam Switch", "kind": "switch",
		"binding": {"group": SWITCH, "device": -1},
		"aliases": [{"namespace": "pinmame.switch", "value": "-1"}],
		"availability": "used", "normally_closed": True, "roles": ["cabinet.slam-tilt"],
		"physical": {
			"location": "inside the front door", "switch_type": "tilt",
			"notes": (
				"The manual (section III, F) describes a normally closed slam switch inside the front door whose opening ends the game for all "
				"players. It is not part of the switch matrix: PinMAME's GTS80_SWSLAMTILT (-1) is read on RIOT U5 port A bit 7 (slam_sw_r), and "
				"public 1 is the slammed state, the contact open, so a consumer holds -1 at 0 for a machine at rest. The slam harness run shows "
				"-1 = 1 ending the game (lamp 0 and solenoid 10 drop, lamp 11 resumes flashing), and the self test's exit list includes 'open slam "
				"switch'. sys80.vbs writes it from the slam key as swSlamTilt = -1."
			),
		},
		"provenance": provenance(MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUN_SOURCE["slam"]),
		"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
	})
	devices.append({
		"id": "switch.sound-board-test", "label": "Sound Board Test Button", "kind": "switch",
		"binding": {"group": SWITCH, "device": -4},
		"aliases": [{"namespace": "pinmame.switch", "value": "-4"}],
		"availability": "used", "normally_closed": False, "roles": ["service.sound-test"],
		"physical": {
			"location": "backbox, sound/speech board (A6)", "switch_type": "button",
			"notes": (
				"The test button on the sound/speech board (manual section IX, E: 'Pressing the test button on the sound board will initiate the "
				"test', in game-over mode only). PinMAME's GTS80_COMPORTS 'Sound Test' bit lands in internal column 0 row 4 (public -4), and "
				"SWITCH_UPDATE(GTS80) passes it to sndbrd_0_diag; the main ROM never reads it."
			),
		},
		"provenance": provenance(MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
		"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
	})
	for address in (-8, -7, -6, -5, -3, -2):
		reason = "Caveman's video joystick bit, published only on GTS80_DISPVIDEO drivers" if address <= -5 else "written by no input port"
		devices.append({
			"id": f"switch.unused-dedicated-{abs(address)}", "label": f"Unused Dedicated Input ({address})", "kind": "switch",
			"binding": {"group": SWITCH, "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "unused",
			"physical": {"location": "internal public address space", "switch_type": "other", "notes": f"Internal column 0 row {address + 8}: {reason}. Black Hole is not a video game and the ROM cannot read column 0."},
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE),
			"spatial": not_applicable("unused", CORE_SOURCE, CONTROLLER_SOURCE),
		})
	for strobe in range(8):
		for ret in range(8):
			address = strobe * 10 + ret
			if address in UPPER_SWITCHES:
				devices.append(_switch(address, UPPER_SWITCHES[address], False))
			elif address in LOWER_SWITCHES:
				devices.append(_switch(address, LOWER_SWITCHES[address], True))
			elif address in CABINET_SWITCHES:
				label, role, location, switch_type, note = CABINET_SWITCHES[address]
				devices.append({
					"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
					"binding": {"group": SWITCH, "device": address},
					"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
					"availability": "used", "normally_closed": False, "roles": [role],
					"physical": {
						"location": location, "switch_type": switch_type,
						"notes": f"{note} Return 7 (strobe {strobe}): the playfield matrix sheet prints 'RETURN 7 NOT USED' because the cabinet switches are on the cabinet sheet, which this manual copy crops. {POLARITY_NOTE}",
					},
					"wiring": {"board": "A1 control board, switch matrix", "drive_connection": f"strobe {strobe}, A1J6-{strobe + 1}", "drive_wire": STROBE_WIRES[strobe], "return_connection": "return 7 (cabinet sheet not legible in the retained copy)"},
					"provenance": provenance(*CABINET_REFS, RUN_SOURCE["gameplay-causality"] if address != 7 else RUN_SOURCE["lamp-driver-test"]),
					"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
				})
			elif address in UNKNOWN_RETURN_7:
				devices.append(_return_seven_unknown(address))
			elif address in UNUSED_MATRIX:
				devices.append({
					"id": f"switch.unused-matrix-{address:02d}", "label": f"Unused Matrix Position {address:02d}", "kind": "switch",
					"binding": {"group": SWITCH, "device": address},
					"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
					"availability": "unused",
					"physical": {
						"location": "switch matrix", "switch_type": "other",
						"notes": (
							f"Strobe {strobe}, return {ret}: the matrix sheet draws no cell here. The ROM still scans the position: its switch test "
							f"shows {address:02d} while the address is held, so the absence of a switch is the sheet's, not the ROM's."
						),
					},
					"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, *SWITCH_TEST_SOURCES),
					"spatial": not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
				})
			else:
				raise AssertionError(address)
	for address in range(111, 119):
		devices.append(_flipper_column(address))
	devices.extend(dip_devices())
	return devices


def _return_seven_unknown(address: int) -> dict[str, Any]:
	strobe = address // 10
	if address == 57:
		label, note, refs = "Tilt (Return 7, Strobe 5)", (
			"PinMAME's GTS80_COMPORTS names this position Tilt and sys80.vbs defines swTilt = 57. The ROM treats it as a tilt: closing it once "
			"during play energizes the T relay (lamp 1, solenoid 11) and drops solenoid 10 (tilt-57 harness run), and closing it in the switch "
			"test leaves the test, the manual's 'close tilt switch' exit (switch-test-c). Whether Black Hole's cabinet wires its plumb-bob and "
			"ball-roll tilts here or, with the playfield tilt, to 26 is on the cabinet wiring sheet (printed page 47), which the retained copy "
			"crops; the retained table writes its tilt to 26. Fitment stays unknown."
		), (CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUN_SOURCE["tilt-57"], RUN_SOURCE["switch-test-c"], VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
	elif address == 67:
		label, note, refs = "Unassigned Return-7 Position 67", (
			"No input port writes this position and no retained source names it. The ROM reads it: its switch test shows 67 while it is held "
			"(switch-test-d). Whether anything is wired here is on the cabinet wiring sheet, which the retained copy crops."
		), (CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["switch-test-d"], MANUAL_SOURCE)
	else:
		label, note, refs = "Unassigned Return-7 Position 77", (
			"No input port writes this position and no retained source names it. The ROM reacts to it: closing it in the switch test leaves the "
			"test as 57 does (switch-test-e), and closing it once during play blanks the credit and ball-in-play displays, after which every "
			"output and display stops changing for the rest of a 20 s observation (tilt-77). Whether anything is wired here is on the cabinet "
			"wiring sheet, which the retained copy crops."
		), (CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["switch-test-e"], RUN_SOURCE["tilt-77"], MANUAL_SOURCE)
	return {
		"id": f"switch.return-7-{address}", "label": label, "kind": "switch",
		"binding": {"group": SWITCH, "device": address},
		"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
		"availability": "unknown",
		"physical": {"location": "cabinet (return 7)", "switch_type": "unknown", "notes": note},
		"wiring": {"board": "A1 control board, switch matrix", "drive_connection": f"strobe {strobe}, A1J6-{strobe + 1}", "drive_wire": STROBE_WIRES[strobe], "return_connection": "return 7 (cabinet sheet not legible in the retained copy)"},
		"provenance": provenance(*refs, status="observed"),
	}


def _flipper_column(address: int) -> dict[str, Any]:
	bit = address - 111
	base = (
		f"PinMAME flipper switch column (CORE_FLIPPERSWCOL, internal column 11), bit 0x{1 << bit:02X}, published at {address} by "
		"GTS80_sw2m's no >= 96 branch."
	)
	refs = (CORE_SOURCE, CONTROLLER_SOURCE)
	if address in (112, 114):
		side = "right" if address == 112 else "left"
		outputs = "45/46" if address == 112 else "47/48"
		return {
			"id": f"switch.{side}-flipper-button", "label": f"{side.title()} Flipper Button", "kind": "switch",
			"binding": {"group": SWITCH, "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"availability": "used", "normally_closed": False, "roles": [f"flipper.lower.{side}.button"],
			"physical": {
				"location": "cabinet flipper button", "switch_type": "button",
				"notes": (
					f"{base} This is the {side} cabinet flipper button as PinMAME receives it ({'CORE_SWLRFLIPBUTBIT' if address == 112 else 'CORE_SWLLFLIPBUTBIT'}). "
					"On the machine the button is a leaf switch that powers the flipper coils directly through relay contacts (the 'LEFT/RIGHT "
					"FLIPPERS SW.' lines of page 45) and the CPU never reads it. Black Hole's driver sets no FLIP_SWNO, so PinMAME copies the bit "
					f"into no matrix switch; it only fabricates the synthetic outputs {outputs} from it while solenoid 10 (game on) is set "
					f"(gameplay harness run). sys80.vbs writes it as {'swLRFlip' if address == 112 else 'swLLFlip'} = {address}. The same button "
					"works the flippers of whichever playfield the U and L relays (lamps 16 and 17) select."
				),
			},
			"provenance": provenance(*refs, VPM_LIBRARY_SOURCE, MANUAL_SOURCE, RUN_SOURCE["gameplay-causality"]),
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		}
	reason = (
		"an end-of-stroke bit" if address in (111, 113, 115, 117) else "an upper-flipper button bit"
	)
	notes = (
		f"{base} It is {reason}, which joins locals.flipMask only when hw.flippers declares it; Black Hole's INIT_S80 sets hw.flippers to 0, "
		"so core_updateSw neither synthesizes nor copies it, and riot6532_0a_r reads only internal columns 1-8, so the ROM cannot read it."
	)
	if address in (113, 115):
		notes += (
			f" sys80.vbs names {address} {'swURFlip' if address == 113 else 'swULFlip'} and writes it from a staged flipper key only while an "
			"upper flipper solenoid is registered; the write has no effect here."
		)
	return {
		"id": f"switch.unused-flipper-column-{address}", "label": f"Unused Flipper Column Position ({address})", "kind": "switch",
		"binding": {"group": SWITCH, "device": address},
		"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
		"availability": "unused",
		"physical": {"location": "internal public address space", "switch_type": "other", "notes": notes},
		"provenance": provenance(*refs, *((VPM_LIBRARY_SOURCE,) if address in (113, 115) else ())),
		"spatial": not_applicable("unused", CORE_SOURCE, CONTROLLER_SOURCE),
	}


CPU_DIP_FUNCTIONS = {
	**{n: ("Coin Chute Adjustment, Left Chute", f"one of four left-chute coins/credits switches S1-S4 (table on page 11)") for n in range(1, 5)},
	**{n: ("Coin Chute Adjustment, Right Chute", "one of four right-chute coins/credits switches S5-S8") for n in range(5, 9)},
	**{n: ("Coin Chute Adjustment, Center Chute", "one of four center-chute coins/credits switches S9-S12") for n in range(9, 13)},
	13: ("Extra Credits", "ON adds 9 credits to the center coin chute setting; OFF no effect"),
	14: ("Coin Chute Control", "ON left and right chutes same; OFF left and right chutes separate"),
	15: ("Maximum Credits", "with S16: OFF OFF 8, OFF ON 10, ON OFF 15, ON ON 25"),
	16: ("Maximum Credits", "with S15: OFF OFF 8, OFF ON 10, ON OFF 15, ON ON 25"),
	17: ("Balls per Game", "ON 3, OFF 5"),
	18: ("Match Feature", "ON on, OFF off"),
	19: ("Replay Limit", "ON limits each player to one replay per game; OFF no replay limit"),
	20: ("Novelty Mode", "ON: playfield SPECIAL and EXTRA BALL award 50,000 points and 5 knocks, high score, high game to date and match disabled; overrides S21"),
	21: ("Game Mode", "ON extra ball, OFF replay; ON also disables the high game to date and match awards"),
	22: ("Playfield Special", "ON awards extra ball, OFF awards special"),
	23: ("High Game to Date", "with S24: OFF OFF not displayed, no award; OFF ON displayed, no award; ON OFF displayed, 2 replays; ON ON displayed, 3 replays"),
	24: ("High Game to Date", "with S23 (see S23)"),
	25: ("Must Remain On", "printed MUST REMAIN ON"),
	26: ("Must Remain On", "printed MUST REMAIN ON"),
	27: ("Coin Switch Tune", "ON yes, OFF no"),
	28: ("Credits Displayed", "ON yes, OFF no"),
	29: ("Off", "printed only as OFF"),
	30: ("Attract Features", "ON on, OFF off"),
	31: ("Must Remain Off", "printed MUST REMAIN OFF"),
	32: ("Background Tone (Sound Board Only)", "ON on, OFF off; must remain off on a game with the sound/speech board"),
}
SOUND_DIP_FUNCTIONS = {
	33: ("SB1-1 Self-Test", "used", "USED IN SELF-TEST ONLY; gts80ss_init passes it to the board as its self-test input"),
	34: ("SB1-2 Not Used", "unused", "NOT USED; gts80ss_init leaves it unread (comment: goes to the expansion board, pin J1-1)"),
	35: ("SB1-3 Attract Mode Speech", "used", "with SB1-4: OFF OFF disabled, ON OFF every 10 seconds, OFF ON every 2 minutes, ON ON every 4 minutes"),
	36: ("SB1-4 Attract Mode Speech", "used", "with SB1-3 (see SB1-3)"),
	37: ("SB1-5 Background Sound", "used", "ON enabled, OFF disabled"),
	38: ("SB1-6 Speech", "used", "ON all speech enabled, OFF all speech disabled"),
	39: ("SB1-7 Not Used", "unused", "NOT USED in the manual; gts80ss_init still passes it to the board (comment: connected, usage unknown)"),
	40: ("SB1-8 Not Used", "unused", "NOT USED; gts80ss_init leaves it unread (comment: goes to the expansion board, pin J1-17)"),
}


def dip_devices() -> list[dict[str, Any]]:
	devices = []
	for n in range(1, 33):
		label, function = CPU_DIP_FUNCTIONS[n]
		devices.append({
			"id": f"dip.cpu-s{n}", "label": f"CPU Switch S{n}: {label}", "kind": "dip_switch",
			"binding": {"group": DIP, "device": n},
			"aliases": [{"namespace": "pinmame.dip", "value": str(n)}, {"namespace": "manual.address", "value": f"S{n}"}],
			"availability": "used",
			"physical": {
				"location": "backbox, A1 control board",
				"switch_type": "dip",
				"notes": (
					f"Control board switch S{n} (manual page 11, section VI A): {function}. PinMAME's GTS80_DIPS names it S{n} at bank {(n - 1) // 8} "
					f"bit {(n - 1) % 8}; riot6532_0a_r returns the bank, bit-reversed, while RIOT U5 port B bit 7 is set. The ROM reads the switches "
					"at power-up and when the first player of a new game starts."
				),
			},
			"provenance": provenance(MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_IDOC_SOURCE, CORE_SOURCE),
		})
	for n in range(33, 41):
		label, availability, function = SOUND_DIP_FUNCTIONS[n]
		devices.append({
			"id": f"dip.sound-speech-sb1-{n - 32}", "label": f"Sound/Speech Board {label}", "kind": "dip_switch",
			"binding": {"group": DIP, "device": n},
			"aliases": [{"namespace": "pinmame.dip", "value": str(n)}, {"namespace": "manual.address", "value": f"SB1-{n - 32}"}],
			"availability": availability,
			"physical": {
				"location": "backbox, sound/speech board (A6), switch bank SB1",
				"switch_type": "dip",
				"notes": (
					f"Switch bank SB1 position {n - 32} (manual page 12): {function}. PinMAME's GTS80_SNDDIPS calls it SS:S{n - 32} (bank 4 bit {n - 33}); "
					"gts80ss_init reads it once when the sound/speech board starts. The sound-only (668A) drivers do not read bank 4."
				),
			},
			"provenance": provenance(MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
			"spatial": not_applicable("dip_switch", MANUAL_IDOC_SOURCE, CORE_SOURCE),
		})
	for n, function in ((41, "Sound/Tones"), (42, "Attract Mode Tunes")):
		devices.append({
			"id": f"dip.sound-board-s{n - 40}", "label": f"Sound-Only Board S{n - 40}: {function}", "kind": "dip_switch",
			"binding": {"group": DIP, "device": n},
			"aliases": [{"namespace": "pinmame.dip", "value": str(n)}],
			"availability": "optional",
			"physical": {
				"location": "backbox, sound board (A6) of the sound-only build",
				"switch_type": "dip",
				"notes": (
					f"PinMAME's GTS80_SNDDIPS 'S:S{n - 40}' (bank 5 bit {n - 41}), read once by gts80s_init on the sound-only board ('{function}' in its "
					"comment). Only the sound-only drivers blkholea and blkhol7s use it; on the sound/speech build the bank is unread. The retained "
					"manual covers the sound-only board only by its installation note (page 29) and prints no switch table for it."
				),
			},
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE, status="observed"),
			"spatial": not_applicable("dip_switch", CORE_SOURCE, CONTROLLER_SOURCE),
		})
	return devices


# --- Outputs -----------------------------------------------------------------------------------------

DRIVER_REFS = (MANUAL_SOURCE, MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)

# address: (id, label, part, connector, wire, transistor, through, fuse, location, objects, note)
SOLENOID_COILS = {
	1: ("coil.upper-hole-bank-reset", "Upper 4-Position Drop Target Bank Reset (H-O-L-E)", "A-18318", "A3J4-7", "266", "Q60 2N6043", "A9J2/A9P2 5 and 7", "F14 2 AMP SLO-BLO", "upper playfield, under the right (H-O-L-E) drop bank", ("TargetO", "TargetL2"),
		"Printed on page 44 as SOLENOID #1, 4 POS. BANK; coil chart A-18318 4 BANK RESET. The ROM's solenoid test pulses public 1 while showing 1, and completing H-O-L-E during play pulses it (gameplay run). The manual's Note A misprints solenoid 1 as the lower 4-bank. The retained table binds it to HoleTargetsUp."),
	2: ("coil.upper-black-bank-reset", "Upper 5-Position Drop Target Bank Reset (B-L-A-C-K)", "A-17891", "A3J4-13", "200", "Q58 2N3055, driven by Q57 MPS-U45", "A9J3/A9P3 6 and 9", "F14 2 AMP SLO-BLO", "upper playfield, under the left (B-L-A-C-K) drop bank", ("TargetA",),
		"Printed on page 44 as SOLENOID #2, 5 POS. BANK; coil chart A-17891 5 BANK RESET. The ROM's solenoid test pulses public 2 while showing 2, and completing B-L-A-C-K during play pulses it (gameplay run). The manual's Note A misprints solenoid 2 as the lower 3-bank. The retained table binds it to BlackTargetsUp."),
	5: ("coil.lower-yellow-bank-reset", "Lower 4-Position Drop Target Bank Reset (Yellow)", "A-18318", "A3J4-6", "211", "Q62 2N3055, driven by Q61 MPS-U45", "A9J8/A9P8 7", "F18 2 AMP SLO-BLO", "lower playfield, under the yellow four-bank", ("TargetLL50", "TargetLL60"),
		"Printed on page 44 as SOLENOID #5, 4 POS. BANK in the block located on the lower playfield. The ROM's solenoid test pulses public 5 while showing 5; during play the ROM resets the lower banks only when the ball returns from the lower playfield (gameplay run: no reset when the bank completes, a pulse as switch 43 releases), as the manual's 'will not reset until completed for each player' implies. The retained table binds it to YellowTargetsUp."),
	6: ("coil.lower-white-bank-reset", "Lower 3-Position Drop Target Bank Reset (White)", "A-18102", "A3J4-12", "233", "Q64 2N3055, driven by Q63 MPS-U45", "A9J8/A9P8 8", "F20 1 AMP SLO-BLO", "lower playfield, under the white three-bank", ("TargetLR51",),
		"Printed on page 44 as SOLENOID #6, 3 POS. BANK in the lower-playfield block; coil chart A-18102 3 BANK RESET. The ROM's solenoid test pulses public 6 while showing 6, and after the bank was completed the gameplay run pulses it once, for about 0.2 s, 3.5 s into a 4 s closure of switch 43. The retained table binds it to WhiteTargetsUp."),
	9: ("coil.outhole-kicker", "Outhole Kicker", "A-16570", "A3J4-8", "244", "Q59 2N6043", "", "F15 1 AMP SLO-BLO", "below the upper playfield, at the outhole", ("Drain",),
		"Printed on page 44 as SOLENOID #9, OUTHOLE; coil chart A-16570 OUTHOLE. It kicks a drained ball from the outhole (switch 15) into the ball return trough (switch 25). The ROM's solenoid test pulses public 9 while showing 9, and the gameplay run pulses it repeatedly while 15 is held. The manual's Note A misprints the outhole as solenoid 3 and 10. The retained table binds it to SolOuthole."),
}
CABINET_SOLENOIDS = {
	3: ("coil.coin-counter-left-chute", "Coin Counter, Left Chute", "A3J6-3", "Q54 MPS-U45", "cabinet.coin-counter-1", "Pulsed by a coin on the left chute (switch 17, gameplay run). Note B: 'Mechanical coin counters are optional and are not pulsed during solenoid test', and the solenoid test skips 3, 4 and 7."),
	4: ("coil.coin-counter-right-chute", "Coin Counter, Right Chute", "A3J6-2", "Q55 MPS-U45", "cabinet.coin-counter-2", "Pulsed by a coin on the right chute (switch 27, gameplay run). Note D: on German games solenoid #4 is assigned to the center chute."),
	7: ("coil.coin-counter-center-chute", "Coin Counter, Center Chute", "A3J6-1", "Q56 MPS-U45", "cabinet.coin-counter-3", "Pulsed by a coin on the center chute (switch 37, gameplay run). Note D: on German games solenoid #7 is assigned to the right chute."),
}


def _coil_wiring(connector: str, wire: str, transistor: str, through: str, fuse: str) -> dict[str, Any]:
	wiring: dict[str, Any] = {
		"board": "A3 driver board", "drive_connection": connector + (f", {through}" if through else ""),
		"drive_wire": wire, "driver_transistor": transistor, "nominal_voltage_v": 24, "voltage_type": "dc",
		"control_connection": f"driver board {connector}",
	}
	if fuse:
		wiring["power_connection"] = f"+24V DC bus (wire 222) through {fuse}"
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	devices: list[dict[str, Any]] = []
	for address in range(1, 12):
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in SOLENOID_COILS:
			identifier, label, part, connector, wire, transistor, through, fuse, location, objects, note = SOLENOID_COILS[address]
			lower = any(name in LOWER_PLAYFIELD_OBJECTS for name in objects)
			points = [midpoint(*objects)] if len(objects) > 1 else list(objects)
			device = {
				"id": identifier, "label": label, "kind": "coil",
				"binding": {"group": SOLENOID, "device": address},
				"aliases": aliases + [{"namespace": "manual.address", "value": f"#{address}"}],
				"availability": "used",
				"physical": {
					"location": location, "part_number": part,
					"notes": note + (" Placed at the midpoint of the bank's two middle targets in the retained table, as a projection of the reset coil under the bank." if len(objects) > 1 else "") + (" " + LOWER_NOTE if lower else ""),
				},
				"wiring": _coil_wiring(connector, wire, transistor, through, fuse),
				"provenance": provenance(*DRIVER_REFS, RUN_SOURCE["solenoid-test"], RUN_SOURCE["gameplay-causality"], VPX_SCRIPT_SOURCE),
				"spatial": located(identifier, "effect", points),
			}
			devices.append(device)
		elif address in CABINET_SOLENOIDS:
			identifier, label, connector, transistor, role, note = CABINET_SOLENOIDS[address]
			devices.append({
				"id": identifier, "label": label, "kind": "coil",
				"binding": {"group": SOLENOID, "device": address},
				"aliases": aliases + [{"namespace": "manual.address", "value": f"SOL. {address}"}],
				"availability": "optional", "roles": [role],
				"physical": {"location": "cabinet, coin door", "notes": f"Driver board output SOL. {address} on {connector} ({transistor}). {note} The retained table binds nothing to it."},
				"wiring": {"board": "A3 driver board", "drive_connection": connector, "driver_transistor": transistor, "control_connection": f"driver board {connector}"},
				"provenance": provenance(*DRIVER_REFS, RUN_SOURCE["gameplay-causality"], RUN_SOURCE["solenoid-test"]),
				"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
			})
		elif address == 8:
			devices.append({
				"id": "coil.knocker", "label": "Knocker", "kind": "coil",
				"binding": {"group": SOLENOID, "device": 8},
				"aliases": aliases + [{"namespace": "manual.address", "value": "SOL. 8"}],
				"availability": "used", "roles": ["cabinet.knocker"],
				"physical": {
					"location": "cabinet, fuse/knocker panel behind the front door",
					"notes": (
						"Driver board output SOL. 8 on A3J5-8 (Q53 2N6043); the manual's adjustments page puts the volume control 'on the Fuse/Knocker "
						"panel. Which is accessible through the front door', and its generic coil chart lists A-5195 for KNOCKER. The ROM's solenoid test "
						"pulses public 8 while showing 8, and the gameplay run knocks it for awarded replays. The manual's Note A misprints 8 as the upper "
						"capture hole. The retained table binds it to the knocker sound."
					),
				},
				"wiring": {"board": "A3 driver board", "drive_connection": "A3J5-8", "driver_transistor": "Q53 2N6043", "control_connection": "driver board A3J5-8"},
				"provenance": provenance(*DRIVER_REFS, RUN_SOURCE["solenoid-test"], RUN_SOURCE["gameplay-causality"], VPX_SCRIPT_SOURCE),
				"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
			})
		elif address == 10:
			devices.append({
				"id": "virtual.game-on", "label": "Game On (Q Relay Energized, T Relay Released)", "kind": "virtual",
				"binding": {"group": SOLENOID, "device": 10},
				"aliases": aliases, "availability": "used",
				"physical": {
					"notes": (
						"Synthetic: GTS80_vblank publishes lamp 0's driver state (the Q, game-over relay) while lamp 1 (the T, tilt relay) is off. It "
						"is high during play and drops on a tilt (tilt runs) or a slam (slam run). It is also the flipper enable that gates the "
						"synthetic flipper outputs 45-48. On the machine the Q and T relay contacts switch the +38V flipper and +24V kicking-rubber "
						"supplies (page 45). sys80.vbs names it GameOnSolenoid; the retained table binds it to nothing (its sEnable constant is 19, "
						"which System 80 never publishes)."
						" PinMAME publishes it only in binary solenoid mode: with physical or modulated solenoid output enabled, core_getSol reads solenoids 1-28 from physicOutputState, which System 80 writes only for 1-9, so this address reads 0 and a consumer takes the state from the physical lamp outputs as lamp 0 on while lamp 1 is off. The synthetic flipper outputs "
						"45-48 are unaffected."
					),
				},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["gameplay-causality"], RUN_SOURCE["tilt-26"], VPM_LIBRARY_SOURCE),
				"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
			})
		else:
			devices.append({
				"id": "virtual.tilt-relay-state", "label": "Tilt Relay State (T Relay)", "kind": "virtual",
				"binding": {"group": SOLENOID, "device": 11},
				"aliases": aliases, "availability": "used",
				"physical": {"notes": "Synthetic: GTS80_vblank publishes lamp 1's driver state, the T (tilt) relay, here. It rises on a tilt (tilt-26 and tilt-57 runs) and is pulsed in the lamp-driver test with lamp 1. PinMAME publishes it only in binary solenoid mode: with physical or modulated solenoid output enabled, core_getSol reads solenoids 1-28 from physicOutputState, which System 80 writes only for 1-9, so this address reads 0 and a consumer takes lamp 1 instead."},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["tilt-26"], RUN_SOURCE["lamp-driver-test"]),
				"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
			})
	for address, identifier, label, button in (
		(45, "virtual.right-flipper-power-synthetic", "Right Flipper Power (Synthetic)", 112),
		(46, "virtual.right-flipper-hold-synthetic", "Right Flipper (Synthetic)", 112),
		(47, "virtual.left-flipper-power-synthetic", "Left Flipper Power (Synthetic)", 114),
		(48, "virtual.left-flipper-hold-synthetic", "Left Flipper (Synthetic)", 114),
	):
		devices.append({
			"id": identifier, "label": label, "kind": "virtual",
			"binding": {"group": SOLENOID, "device": address},
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
			"availability": "used",
			"physical": {
				"notes": (
					f"Synthetic: core_updateSw sets this bit from the flipper button {button} while solenoid 10 (game on) is set; there is no driver "
					"output behind it. The gameplay run publishes it only during play. It does not say which flippers move: the cabinet button powers "
					"the upper playfield's two flippers on its side through the U relay's normally closed contact and the lower playfield's flipper "
					"through the L relay's normally open contact (page 45), so a consumer gates it with lamps 16 and 17, as the retained table's "
					"SolLFlipper/SolRFlipper do."
				),
			},
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["gameplay-causality"], MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
		})
	return devices


# Lamp connector pins from the driver board sheet (printed pages 25-26), wires from page 44.
LAMP_CONNECTOR = {
	0: "A3J3-A (overbar)", 1: "A3J3-B (overbar)", 2: "A3J5-2", 3: "A3J3-C (overbar) and A3J2-1",
	4: "A3J2-2", 5: "A3J2-3", 6: "A3J2-5", 7: "A3J2-4", 8: "A3J2-10", 9: "A3J2-9", 10: "A3J2-7", 11: "A3J2-8",
	12: "A3J3-25", 13: "A3J3-24", 14: "A3J3-22", 15: "A3J3-23", 16: "A3J3-13", 17: "A3J3-14", 18: "A3J3-16", 19: "A3J3-15",
	20: "A3J3-21", 21: "A3J3-20", 22: "A3J3-18", 23: "A3J3-19", 24: "A3J3-9", 25: "A3J3-10", 26: "A3J3-12", 27: "A3J3-11",
	28: "A3J3-Y", 29: "A3J3-X", 30: "A3J3-V", 31: "A3J3-W", 32: "A3J3-5", 33: "A3J3-6", 34: "A3J3-K", 35: "A3J3-7",
	36: "A3J4-1", 37: "A3J4-2", 38: "A3J4-4", 39: "A3J4-3", 40: "A3J3-4", 41: "A3J3-3", 42: "A3J3-T", 43: "A3J3-2",
	44: "A3J3-D", 45: "A3J3-F", 46: "A3J3-P", 47: "A3J3-M", 48: "A3J3-E", 49: "A3J3-H", 50: "A3J3-R", 51: "A3J3-N",
}
LAMP_WIRE = {
	3: "588", 4: "500", 5: "511", 6: "522", 7: "533", 8: "544", 12: "100", 13: "111", 14: "122", 15: "133", 16: "144", 17: "155", 18: "166", 19: "177",
	20: "300", 21: "311", 22: "322", 23: "333", 24: "344", 25: "355", 26: "366", 27: "377", 28: "500", 29: "511", 30: "522", 31: "533",
	32: "544", 33: "555", 34: "566", 35: "577", 36: "700", 37: "711", 38: "722", 39: "733", 40: "744", 41: "755", 42: "766", 43: "777",
	44: "800", 45: "811", 46: "822", 47: "833", 48: "844", 49: "855", 50: "866", 51: "877", 0: "288", 1: "277",
}
A13_LAMPS = frozenset(range(4, 12)) | frozenset(range(32, 44))

# address: (label, location, table objects, extra note)
PLAYFIELD_LAMPS: dict[int, tuple[str, str, tuple[str, ...], str]] = {
	4: ("3 Pos. Bank Special (Lower Playfield)", "lower playfield, the red WHEN LIT insert beside the white three-bank", ("L4",), ""),
	5: ("\"+1X\" Scoring (L) (Lower Playfield)", "lower playfield, left g-force accelerator insert", ("L5",), ""),
	6: ("\"+1X\" Scoring (R) (Lower Playfield)", "lower playfield, right g-force accelerator insert", ("L6",), "The retained table omits lamp 6 from its Lights() list but drives its insert in UpdateLamps."),
	7: ("Left Spinning Target", "upper playfield, left lane below the spinner", ("L7",), ""),
	19: ("Hole Lights (Arrows) (Lower Playfield)", "lower playfield, three blue arrow inserts pointing at the capture hole", ("L19a", "L19b", "L19c"), "Three bulbs: the location drawing prints L19 three times."),
	20: ("Loop Lights (Arrows) (Lower Playfield)", "lower playfield, three blue arrow inserts on the right", ("L20a", "L20b", "L20c"), "Three bulbs: the location drawing prints L20 three times."),
	21: ("\"B\" Drop Target Light", "upper playfield, arrow insert in front of the left bank", ("L21",), ""),
	22: ("\"L\" Drop Target Light", "upper playfield, arrow insert in front of the left bank", ("L22",), ""),
	23: ("\"A\" Drop Target Light", "upper playfield, arrow insert in front of the left bank", ("L23",), ""),
	24: ("\"C\" Drop Target Light", "upper playfield, arrow insert in front of the left bank", ("L24",), ""),
	25: ("\"K\" Drop Target Light", "upper playfield, arrow insert in front of the left bank", ("L25",), ""),
	26: ("\"H\" Drop Target Light", "upper playfield, arrow insert in front of the right bank", ("L26",), ""),
	27: ("\"O\" Drop Target Light", "upper playfield, arrow insert in front of the right bank", ("L27",), ""),
	28: ("\"L\" Drop Target Light (Hole Bank)", "upper playfield, arrow insert in front of the right bank", ("L28",), ""),
	29: ("\"E\" Drop Target Light", "upper playfield, arrow insert in front of the right bank", ("L29",), ""),
	30: ("2X Multiplier", "upper playfield, round insert above the window", ("L30",), ""),
	31: ("3X Multiplier", "upper playfield, round insert above the window", ("L31",), ""),
	32: ("4X Multiplier", "upper playfield, round insert above the window", ("L32",), ""),
	33: ("5X Multiplier", "upper playfield, round insert above the window", ("L33",), ""),
	34: ("Top Lane #1 (10,000)", "upper playfield, left arc of lanes", ("L34",), ""),
	35: ("Top Lane #2 (Extra Ball)", "upper playfield, left arc of lanes", ("L35",), ""),
	36: ("Top Lane #3 (Special)", "upper playfield, left arc of lanes", ("L36",), ""),
	37: ("Top Hole #1 (Captive)", "upper playfield, below the capture hole on the left", ("L37",), "The blue capture-hole lamp the manual says flashes until a ball is captured once the spot targets are complete; the gameplay run makes it flash after 01-31."),
	38: ("Top Hole #2 (Extra Ball)", "upper playfield, below the capture hole on the left", ("L38",), ""),
	39: ("Right Return Rollover", "upper playfield, arrow insert at the right return lane", ("L39c",), "The retained table binds Lights(39) to L39c; its L39a and L39b are gate indicators it drives from lamp 18 itself."),
	40: ("Right Side Rollover", "upper playfield, right-hand lane", ("L40",), ""),
	41: ("#1 Top Rollover", "upper playfield, above the left top lane", ("L41",), ""),
	42: ("#2 Top Rollover", "upper playfield, above the middle top lane", ("L42",), ""),
	43: ("#3 Top Rollover", "upper playfield, above the right top lane", ("L43",), ""),
	44: ("#1 Drop Target Light (Lower Playfield)", "lower playfield, yellow insert beside the four-bank, nearest the player", ("L44",), ""),
	45: ("#2 Drop Target Light (Lower Playfield)", "lower playfield, yellow insert beside the four-bank", ("L45",), ""),
	46: ("#3 Drop Target Light (Lower Playfield)", "lower playfield, yellow insert beside the four-bank", ("l46",), ""),
	47: ("#4 Drop Target Light (Lower Playfield)", "lower playfield, yellow insert beside the four-bank, farthest from the player", ("l47",), ""),
	48: ("#1 Spot Target Light", "upper playfield, round insert beside the #1 spot target", ("L48",), "Driven by the inverted output of the latch that holds lamp 44 (Z12 Q1-bar, Q49): it is lit exactly when lamp 44 is off. PinMAME models this as public 48 = NOT 44."),
	49: ("#2 Spot Target Light", "upper playfield, round insert beside the #2 spot target", ("L49",), "Inverted latch output of lamp 45 (Z12 Q2-bar, Q50): lit exactly when lamp 45 is off."),
	50: ("#3 Spot Target Light", "upper playfield, round insert beside the #3 spot target", ("L50",), "Inverted latch output of lamp 46 (Z12 Q3-bar, Q51): lit exactly when lamp 46 is off."),
	51: ("#4 Spot Target Light", "upper playfield, round insert beside the #4 spot target", ("L51",), "Inverted latch output of lamp 47 (Z12 Q4-bar, Q52): lit exactly when lamp 47 is off."),
}
# Lamp-driven devices: address: (id, label, kind, part, location, objects, note)
LAMP_DEVICES: dict[int, tuple[str, str, str, str, str, tuple[str, ...], str]] = {
	8: ("coil.lower-ball-gate", "Lower Playfield Ball Gate", "coil", "A-16570", "lower playfield, the gate at the end of the entry track", ("sw53",),
		"Remote transistor Q3 (2N5875) 'BALL GATE' in the lower-playfield block of page 44, fed from the light box (A10P4-6) and fused by F19 'Ball Return Gate 24VDC'. It releases the ball waiting on the track switch (53) onto the lower playfield: the gameplay run pulses lamp 8 once when 53 closes with the lower playfield selected, and the retained table kicks the ball out of sw53 on it."),
	12: ("coil.lower-hole-kicker", "Lower Playfield Hole Kicker", "coil", "A-16570", "lower playfield, the capture hole at the lower left", ("sw42",),
		"Remote transistor Q4 (2N5875) 'HOLE KICKER' (L) on page 44, coil chart HOLE KICKER (L) A-16570. The lower capture hole holds a ball for multiball; the manual says the lower ball is released first when multiball starts and all captive balls are ejected at game over. The lamp-driver test pulses it in its chase; the retained table kicks sw42 on it and starts its multiball lighting."),
	13: ("coil.upper-hole-kicker", "Upper Playfield Hole Kicker", "coil", "A-16570", "upper playfield, the capture hole at the left edge", ("sw05",),
		"Remote transistor Q1 (2N5875) 'HOLE KICKER' on page 44, fused by F15 'Outhole, Hole Kicker 24VDC'. While the capture is not enabled the ROM kicks a ball in the hole straight out (repeated pulses while 05 is held, gameplay run); once the four spot targets enable it the ball is held, and it is ejected at the end of the player's turn (the gameplay run's drain)."),
	14: ("coil.ball-lift-kicker", "Ball Lift Kicker (Re-entry Tube)", "coil", "A-4893", "lower playfield, foot of the re-entry tube at the backbox end", ("sw43",),
		"Remote transistor Q5 (2N5875) 'BALL LIFT KICKER' on page 44, coil A-4893, fused by F17 6 1/4 AMP 'Kicker (to upper playfield)'. It kicks a ball from the ball tube kicker switch (43) up the tube to the upper playfield: the gameplay run pulses it when 43 closes. The retained table kicks sw43 on it."),
	15: ("coil.trough-ball-gate", "Ball Gate (Trough Release)", "coil", "A-16570", "below the upper playfield, the ball return trough's exit to the shooter lane", ("kicker1",),
		"Remote transistor Q2 (2N5875) 'BALL GATE (CARDHOLDER)' on page 44, fused by F16 'Trough Ball Gate 24VDC'. It releases a ball from the ball return trough to the shooter lane: the ROM holds it for 2.5 s at every serve (gameplay and high-game-to-date runs), and the retained table's ReleaseBall kicks its trough exit (kicker1) on it."),
	18: ("coil.reentry-wireform-gate", "Wireform Ball Gate (Re-entry Gate)", "coil", "A-17564", "upper playfield, right side, where the re-entry tube returns the ball", ("Flipper1",),
		"Driven directly by the driver board line A3J3-16 (L18), 'WIREFORM BALL GATE' on page 44, coil A-17564. Energized it opens the re-entry gate so a ball lifted from the lower playfield is directed onto the upper playfield (manual: opened by completing a lower bank or by the flashing right return rollover, always open in 3-ball play); closed, the returning ball is lost. The gameplay run energizes it at game start and releases it when the ball returns from the lower playfield. The retained table swings its Flipper1 diverter on it."),
}
RELAYS: dict[int, tuple[str, str, str, str, str]] = {
	0: ("relay.game-over-q", "Game Over (Q) Relay", "under the playfield", "A-16890",
		"The Q relay, energized while a game is in play (the gameplay run raises lamp 0 at the Credit press, and the slam run drops it). Its contacts, with the T relay's, switch the +38V flipper and +24V kicking-rubber supplies (page 45). PinMAME publishes it, gated by the T relay, as solenoid 10. The manual's initialization chart: 'GAME OVER (Q) AND TILT RELAY (T) (UNDER PLAYFIELD) ARE PULSED ON/OFF'."),
	1: ("relay.tilt-t", "Tilt (T) Relay", "under the playfield", "A-16890",
		"The T relay, energized on a tilt (tilt-26 and tilt-57 runs). Its contacts cut the flipper and kicking-rubber supplies and the upper playfield illumination and light the light box's TILT lamp (pages 44-45). Page 45 puts every pop bumper lamp on the illumination T cuts, while the manual's tilt mode says the pop bumper lights stay lit; the conflict records the disagreement. PinMAME publishes its state as solenoid 11."),
	16: ("relay.upper-playfield-u", "Upper Playfield (U) Relay", "upper playfield wiring, under the playfield", "A-16890",
		"Driver board line A3J3-13 (L16), 'U RELAY' on page 44. Energized while the ball is on the lower playfield (the gameplay run raises it when the black hole rollover 33 closes and releases it when 43 lifts the ball back). Its normally closed contacts carry the cabinet flipper buttons to the four upper flippers and the 6.3 V AC to the upper pop bumper lamps, the hole lamp and the upper playfield illumination (page 45), so energizing it disables the upper flippers and darkens the upper playfield. The retained table runs its upper flippers and upper G.I. only while lamp 16 is off."),
	17: ("relay.lower-playfield-l", "Lower Playfield (L) Relay", "lower playfield", "A-16890",
		"Driver board line A3J3-14 (L17), 'L RELAY' in the lower-playfield block of page 44. Energized together with the U relay while the ball is on the lower playfield. Its normally open contacts carry the flipper buttons to the two lower flippers, the 6.3 V AC to the lower playfield illumination and its two pop bumper lamps, and the switched +24V DC to the lower kicking rubber and kicking target (page 45). The retained table runs its lower flippers, lower bumper caps and lower G.I. only while lamp 17 is on."),
}


def lamp_outputs() -> list[dict[str, Any]]:
	devices: list[dict[str, Any]] = []
	lamp_refs = (MANUAL_SOURCE, MANUAL_IDOC_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, RUN_SOURCE["lamp-driver-test"])
	for address in range(64):
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
		if address < 52:
			aliases.append({"namespace": "manual.address", "value": f"L{address}"})
		transistor = (f"Q{address + 1}" if address < 48 else f"Q{address + 1} (inverted latch output)") + (" MPS-A13" if address in A13_LAMPS else " MPS-U45")
		wiring = {"board": "A3 driver board", "drive_connection": LAMP_CONNECTOR.get(address, ""), "driver_transistor": transistor}
		if address in LAMP_WIRE:
			wiring["drive_wire"] = LAMP_WIRE[address]
		if address in PLAYFIELD_LAMPS:
			label, location, objects, extra = PLAYFIELD_LAMPS[address]
			lower = any(name in LOWER_PLAYFIELD_OBJECTS for name in objects)
			notes = f"#44 bulb (page 44 note 3)." + (f" {extra}" if extra else "") + " The lamp-driver test lights it in its ascending chase." + (" " + LOWER_NOTE if lower else "")
			devices.append({
				"id": f"lamp.{slug(label)}", "label": label, "kind": "lamp",
				"binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "used",
				"physical": {"location": location, "notes": notes, **({"quantity": len(objects)} if len(objects) > 1 else {})},
				"wiring": {**wiring, "nominal_voltage_v": 6, "voltage_type": "dc", "power_connection": "+6V DC (wire 255) rectified from the controlled-lamp 8VAC winding, fuse F5 10 Amp"},
				"provenance": provenance(*lamp_refs, VPX_SCRIPT_SOURCE),
				"spatial": located(f"lamp.{slug(label)}", "emitter", objects),
			})
		elif address == 3:
			devices.append({
				"id": "lamp.shoot-again", "label": "Shoot Again", "kind": "lamp",
				"binding": {"group": LAMP, "device": 3}, "aliases": aliases, "availability": "used",
				"physical": {
					"location": "upper playfield between the flippers, and the light box",
					"quantity": 2,
					"notes": (
						"One driver (Z1 Q4, transistor Q4) feeds two bulbs: A3J3-C (overbar) 'L3 SHOOT AGAIN (PLAYBOARD)' and A3J2-1 'L2 SHOOT AGAIN "
						"(LIGHTBOX)' on the driver board sheet; the lamp-driver test lights it first in its chase. Only the playfield bulb is placed."
					),
				},
				"wiring": wiring,
				"provenance": provenance(*lamp_refs, VPX_SCRIPT_SOURCE),
				"spatial": located("lamp.shoot-again", "emitter", ("L3",)),
			})
		elif address in LAMP_DEVICES:
			identifier, label, kind, part, location, objects, note = LAMP_DEVICES[address]
			lower = any(name in LOWER_PLAYFIELD_OBJECTS for name in objects)
			devices.append({
				"id": identifier, "label": label, "kind": kind,
				"binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "used",
				"physical": {"location": location, "part_number": part, "notes": f"A coil on a lamp driver: {note}" + (" " + LOWER_NOTE if lower else "")},
				"wiring": {**wiring, "nominal_voltage_v": 24, "voltage_type": "dc"},
				"provenance": provenance(*lamp_refs, RUN_SOURCE["gameplay-causality"], VPX_SCRIPT_SOURCE),
				"spatial": located(identifier, "effect", objects),
			})
		elif address in RELAYS:
			identifier, label, location, part, note = RELAYS[address]
			devices.append({
				"id": identifier, "label": label, "kind": "relay",
				"binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "used",
				"roles": [f"internal.{identifier.split('.', 1)[1]}"],
				"physical": {"location": location, "part_number": part, "notes": note},
				"wiring": wiring,
				"provenance": provenance(*lamp_refs, RUN_SOURCE["gameplay-causality"], RUN_SOURCE["tilt-26"], VPX_SCRIPT_SOURCE),
				"spatial": not_applicable("internal_nonvisual", MANUAL_SOURCE, MANUAL_IDOC_SOURCE),
			})
		elif address == 2:
			devices.append({
				"id": "coil.coin-lockout", "label": "Coin Lockout Coil", "kind": "coil",
				"binding": {"group": LAMP, "device": 2}, "aliases": aliases, "availability": "used", "roles": ["cabinet.coin-lockout"],
				"physical": {
					"location": "cabinet, coin door",
					"part_number": "A-16890",
					"notes": (
						"Z1 Q3 (transistor Q3) on A3J5-2, 'COIN LOCKOUT COIL'; the coil chart's A-16890 covers the 'Q, T, AND COIN LOCKOUT RELAYS'. "
						"Energized while the game accepts coins (manual initialization chart) and dropped by a slam ('All coins will be rejected'); "
						"the lamp-driver test pulses it twice after the Q and T relays. The retained table drives its four upper pop-bumper cap lights "
						"from lamp 2, a table defect: those lamps are on the 6.3 V AC illumination behind the T and U relay contacts (page 45)."
					),
				},
				"wiring": wiring,
				"provenance": provenance(*lamp_refs, VPX_SCRIPT_SOURCE),
				"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
			})
		elif address == 9:
			devices.append({
				"id": "control.sound-16", "label": "Sound 16 Line", "kind": "control_signal",
				"binding": {"group": LAMP, "device": 9}, "aliases": aliases, "availability": "used", "roles": ["internal.sound-16"],
				"physical": {
					"location": "backbox, to the sound/speech board",
					"notes": (
						"Z3 Q2 (transistor Q10) on A3J2-9 is printed 'SOUND 16' on the driver board sheet: the fifth sound-command bit beside SOUND "
						"1-8 on A3J5, which the sound board test jumpers at A6J1-2. riot6532_2a_w adds 0x10 to the sound command while lamp 9 is on, "
						"and the gameplay run shows it pulsing with scoring sounds. Not a lamp."
					),
				},
				"wiring": wiring,
				"provenance": provenance(*lamp_refs, RUN_SOURCE["gameplay-causality"]),
				"spatial": not_applicable("internal_nonvisual", MANUAL_IDOC_SOURCE, CORE_SOURCE),
			})
		elif address in (10, 11):
			hgtd = address == 10
			devices.append({
				"id": "lamp.high-game-to-date-lightbox" if hgtd else "lamp.game-over-lightbox",
				"label": "High Game to Date (Light Box)" if hgtd else "Game Over (Light Box)",
				"kind": "lamp", "binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "used",
				"roles": ["cabinet.lightbox"],
				"physical": {
					"location": "backbox light box",
					"notes": (
						f"Z3 {'Q3 (transistor Q11) on A3J2-7' if hgtd else 'Q4 (transistor Q12) on A3J2-8'}: the A3J2 lines run to the light box. "
						f"The driver board sheet labels this line {'L11' if hgtd else 'L10'}, the reverse of the Q1-Q4 order every other latch "
						"follows (Q3 'L11', Q4 'L10'); PinMAME's address follows the latch order, so the connector here follows the drawn "
						"transistor line rather than the printed label, and the ROM's behaviour below follows PinMAME's address. "
						+ (
							"The ROM lights it for 2.5 s at every ball release, exactly while all four player displays and the lower playfield display "
							"show the high game to date (high-game-to-date run: 770000 with lamp 10 lit), which the manual describes at III.A.5.b; "
							"other System 80 tables in the pinned script corpus bind lamp 10 to HIGH SCORE TO DATE. The light box sheet that would show "
							"its legend is cropped in the retained manual copy."
							if hgtd else
							"The ROM flashes it at about 2 Hz through game-over attract mode, stops it when a game starts and resumes it after a slam "
							"(high-game-to-date and slam runs), as the manual's 'GAME OVER lamp continually flashes' describes; the backglass photograph "
							"shows a round GAME OVER legend, and other System 80 tables in the pinned script corpus bind lamp 11 to GAME OVER."
						)
					),
				},
				"wiring": wiring,
				"provenance": provenance(*lamp_refs, RUN_SOURCE["high-game-to-date"], IPDB_SOURCE, SISTER_SCRIPTS_SOURCE, *((RUN_SOURCE["slam"],) if not hgtd else ())),
				"spatial": not_applicable("cabinet_or_service", MANUAL_IDOC_SOURCE, CORE_SOURCE),
			})
		elif 52 <= address <= 60:
			solenoid = address - 51
			devices.append({
				"id": f"virtual.solenoid-{solenoid}-lamp-mirror", "label": f"Solenoid {solenoid} Mirror (Physical-Output Mode)", "kind": "virtual",
				"binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "optional",
				"physical": {"notes": f"In PinMAME's physical-output mode riot6532_2a_w writes solenoid {solenoid} to physical lamp output {address} as well ('solenoids are often also used to drive flashers in parallel'); in binary mode it is constant 0. No Black Hole flasher is wired in parallel with a solenoid."},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE),
				"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
			})
		else:
			devices.append({
				"id": f"virtual.unused-lamp-{address}", "label": f"Unused Lamp Address {address}", "kind": "virtual",
				"binding": {"group": LAMP, "device": address}, "aliases": aliases, "availability": "unused",
				"physical": {"notes": "Within PinMAME's 64 System 80 lamp outputs but written by no latch and no solenoid mirror: constant 0 in both output modes."},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE),
				"spatial": not_applicable("unused", CORE_SOURCE, CONTROLLER_SOURCE),
			})
	return devices


def gi_outputs() -> list[dict[str, Any]]:
	return [{
		"id": "virtual.gi-0-lamp-0-model", "label": "PinMAME GI Channel 0 (Lamp 0 Model)", "kind": "virtual",
		"binding": {"group": GI, "device": 0},
		"aliases": [{"namespace": "pinmame.gi", "value": "0"}],
		"availability": "optional",
		"physical": {
			"notes": (
				"MACHINE_INIT(gts80) declares one GI output that riot6532_2b_w fills from lamp 0's latch bit as a reversed #44 bulb (lit while the Q "
				"relay is released), in physical-output mode only; in binary mode it is constant 0. It is not a Black Hole G.I. string: the upper "
				"playfield illumination runs on 6.3 V AC through the T and U relay contacts and the lower playfield illumination through the L relay "
				"(page 45), so a recreation lights them from lamps 1, 16 and 17."
			),
		},
		"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE),
		"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
	}]


# --- Displays ----------------------------------------------------------------------------------------

def displays() -> list[dict[str, Any]]:
	refs = (CORE_SOURCE, MANUAL_SOURCE, MANUAL_IDOC_SOURCE, RUN_SOURCE["solenoid-test"], RUN_SOURCE["high-game-to-date"])
	items: list[dict[str, Any]] = []
	for index, start in enumerate((2, 9, 22, 29)):
		items.append({
			"id": f"display.player-{index + 1}-score", "label": f"Player {index + 1} score, six digits", "kind": "segment",
			"controller_index": index, "segment_start": start, "width": 6, "physical_location": "cabinet_or_service",
			"provenance": provenance(*refs, IPDB_SOURCE),
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		})
	status_refs = (CORE_SOURCE, MANUAL_SOURCE, MANUAL_IDOC_SOURCE, RUN_SOURCE["solenoid-test"], *SWITCH_TEST_SOURCES)
	for index, (identifier, label, start, obj) in enumerate((
		("display.credits-tens", "Credits, tens digit (status display, left pair)", 40, "Credits"),
		("display.credits-units", "Credits, units digit (status display, left pair)", 41, "Credits"),
		("display.ball-in-play-tens", "Ball in play / status, tens digit (status display, right pair)", 42, "BallsInPlay"),
		("display.ball-in-play-units", "Ball in play / status, units digit (status display, right pair)", 43, "BallsInPlay"),
	), start=4):
		items.append({
			"id": identifier, "label": label, "kind": "segment",
			"controller_index": index, "segment_start": start, "width": 1, "physical_location": "playfield",
			"provenance": provenance(*status_refs),
			"spatial": {
				"status": "observed",
				"placements": [{
					"id": f"{identifier}.display", "role": "display", "space": "playfield",
					"x": norm(*TABLE_POINTS[obj])[0], "y": norm(*TABLE_POINTS[obj])[1],
					"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, VPX_TABLE_SOURCE, status="observed"),
				}],
			},
		})
	items.append({
		"id": "display.lower-playfield-bonus", "label": "Lower playfield (bonus) display, six digits", "kind": "segment",
		"controller_index": 8, "segment_start": 50, "width": 6, "physical_location": "playfield",
		"provenance": provenance(*refs, IPDB_SOURCE),
		"spatial": {
			"status": "observed",
			"placements": [{
				"id": "display.lower-playfield-bonus.display", "role": "display", "space": "playfield",
				"x": norm(*TABLE_POINTS["BonusDisplay"])[0], "y": norm(*TABLE_POINTS["BonusDisplay"])[1],
				"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, VPX_TABLE_SOURCE, IPDB_SOURCE, status="observed"),
			}],
		},
	})
	return items


# --- Drivers ------------------------------------------------------------------------------------------

SEVEN_DIGIT_OVERRIDES = tuple(
	(f"display.player-{index + 1}-score", start) for index, start in enumerate((2, 9, 22, 29))
)


def drivers() -> list[dict[str, Any]]:
	def seven_digit(run: str) -> list[dict[str, Any]]:
		return [
			{"target": target, "segment_start": start, "width": 7, "provenance": provenance(CORE_SOURCE, RUN_SOURCE[run])}
			for target, start in SEVEN_DIGIT_OVERRIDES
		]
	return [
		{
			"id": "blckhole", "clone_of": "gts80", "description": "Black Hole (rev. 4)", "flags": 0, "manufacturer": "Gottlieb", "year": "1981",
			"physical_compatibility": "identical",
			"variant_notes": (
				"Gottlieb game PROM 668-4 with the sound/speech PROMs 668-s1 and 668-s2 on the System 80 sound/speech board (SNDBRD_GTS80SS_VOTRAX, "
				"Votrax SC-01 speech) and the stock u2_80/u3_80 system ROMs; display layout dispNumeric2. Every harness run except the variant checks "
				"uses this driver. The manual's PROM list names game PROM 668/2 for games with sound and speech; rev. 4 is PinMAME's root."
			),
		},
		{
			"id": "blkhole2", "clone_of": "blckhole", "description": "Black Hole (rev. 2)", "flags": 0, "manufacturer": "Gottlieb", "year": "1981",
			"physical_compatibility": "identical",
			"variant_notes": (
				"Gottlieb game PROM 668-2, the revision the manual's PROM list names (668/2), with the same sound/speech PROMs, system ROMs, display "
				"layout and init data as blckhole. Its solenoid and switch tests number the outputs and switches as blckhole's do (variant harness run)."
			),
		},
		{
			"id": "blkholea", "clone_of": "gts80s", "description": "Black Hole (Sound Only)", "flags": 0, "manufacturer": "Gottlieb", "year": "1981",
			"physical_compatibility": "compatible",
			"variant_notes": (
				"Game 668A: game PROM 668-a2 and sound PROM 668-a-s on the System 80 sound-only board (SNDBRD_GTS80S, no speech). The manual covers "
				"it: its PROM list names 668A/2 for 'GAMES WITH SOUND ONLY' and 668A/S, and printed page 29 tells how to fit the Sound Board in the "
				"sound/speech board's connector A6J1 with the A7 sound/speech power supply removed. IPDB says multiball, speech and the rotating "
				"backglass disc are on non-export games only. The playfield, the driver outputs and the switch matrix are the same: its solenoid and "
				"switch tests number them as blckhole's do (variant harness run). It reads the sound-only board's DIPs 41-42 instead of the "
				"sound/speech bank 33-40. PinMAME roots it under gts80s rather than blckhole, which is why the catalog once gave it its own record."
			),
		},
		{
			"id": "blkhole7", "clone_of": "blckhole", "description": "Black Hole (7-digit conversion)", "flags": 0, "manufacturer": "Oliver", "year": "2008",
			"physical_compatibility": "compatible",
			"variant_notes": (
				"Oliver 2008 seven-digit conversion: replacement system ROMs u2g807dc/u3g807dc with the stock 668-4 game PROM and sound/speech PROMs "
				"on the same System 80 boards, driving seven-digit player displays (dispNumeric4). The four player displays are seven digits at the "
				"same memory starts (see display_overrides); the lower playfield display keeps six digits at 50. Outputs and switches number as "
				"blckhole's (variant harness run). The retained table selects this driver by default (RomSet = 5)."
			),
			"display_overrides": seven_digit("blkhole7-service"),
		},
		{
			"id": "blkhol7s", "clone_of": "blkholea", "description": "Black Hole (Sound Only, 7-digit conversion)", "flags": 0, "manufacturer": "Oliver", "year": "2008",
			"physical_compatibility": "compatible",
			"variant_notes": (
				"Oliver 2008 seven-digit conversion of the sound-only game 668A: system ROMs u2g807dc/u3g807dc with game PROM 668-a2 and the "
				"sound-only board. Seven-digit player displays as blkhole7 (display_overrides); outputs and switches number as blckhole's (variant "
				"harness run)."
			),
			"display_overrides": seven_digit("blkhol7s-service"),
		},
	]


# --- Mechanisms ---------------------------------------------------------------------------------------

def mechanisms() -> list[dict[str, Any]]:
	game = RUN_SOURCE["gameplay-causality"]
	m = []

	def add(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str) -> None:
		m.append({
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		})

	add("mech.ball-return-trough", "Outhole and ball return trough", "kicker",
		["coil.outhole-kicker", "coil.trough-ball-gate"], ["switch.outhole", "switch.3rd-position-ball-return-trough"],
		"Black Hole uses three balls (manual: 'THIS GAME REQUIRES 3 BALLS'; 'All three balls must be in the ball return trough to start a game'). "
		"A ball drained from the upper playfield lands in the outhole (switch 15), where the outhole kicker (solenoid 9) kicks it into the ball "
		"return trough below the playfield; the trough has one switch, at its third position (25). The ball gate (lamp 15, remote transistor Q2) "
		"releases a ball into the shooter lane: the ROM holds it for 2.5 s at every serve, with lamp 10 lighting the high game to date. The "
		"gameplay run shows 9 pulsing repeatedly while 15 is held and 15/10 at each serve once 25 is closed.",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, game, RUN_SOURCE["high-game-to-date"], VPX_SCRIPT_SOURCE)
	add("mech.upper-black-bank", "Upper B-L-A-C-K five-bank drop targets", "drop_target_bank",
		["coil.upper-black-bank-reset"], [f"switch.{slug(UPPER_SWITCHES[a][0])}" for a in (3, 13, 23, 4, 14)],
		"Five drop targets on the left, B (03) at the lower end to K (14) at the upper end, reset by solenoid 2. Completing the bank resets it "
		"(gameplay run: solenoid 2 pulses after K) and lights the spinner; completing the lamp sequence in order lights a g-force lamp on the lower "
		"playfield.",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.upper-hole-bank", "Upper H-O-L-E four-bank drop targets", "drop_target_bank",
		["coil.upper-hole-bank-reset"], [f"switch.{slug(UPPER_SWITCHES[a][0])}" for a in (2, 12, 22, 32)],
		"Four drop targets on the right, H (02) at the upper end to E (32) at the lower end, reset by solenoid 1 (gameplay run: solenoid 1 pulses "
		"after E). Completing the sequence lights the right side rollover.",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.upper-capture-hole", "Upper playfield capture hole", "kicker",
		["coil.upper-hole-kicker"], ["switch.ball-kicker-hole-switch-upper-capture-hole"],
		"A kick-out hole at the left edge (switch 05, kicker lamp 13). Until the four yellow spot targets (01-31) are completed the ROM kicks the "
		"ball straight back out (repeated lamp 13 pulses while 05 is held); once they are, the blue capture lamp (37) flashes and the next ball in "
		"the hole is held while a new ball is served. A captured upper ball is ejected at the end of the player's turn and at game over (gameplay "
		"run: lamp 13 pulses as the ball drains).",
		MANUAL_IDOC_SOURCE, MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.playfield-select-relays", "Upper (U) and lower (L) playfield relays", "other",
		["relay.upper-playfield-u", "relay.lower-playfield-l"], ["switch.black-hole-rollover", "switch.ball-tube-kicker-switch"],
		"Black Hole's two playfields share one pair of flipper buttons. The U relay (lamp 16) breaks, through normally closed contacts, the "
		"buttons' feed to the four upper flippers and the 6.3 V AC to the upper playfield, pop bumper and hole lamps; the L relay (lamp 17) makes, "
		"through normally open contacts, the feed to the two lower flippers, the lower playfield illumination, its two pop bumper lamps and the "
		"lower kicking rubber and kicking target (page 45). When the ball rolls through the black hole rollover (33) the ROM energizes both "
		"(gameplay run), so the upper playfield goes dark and its flippers dead while the lower one plays; when the ball tube kicker (43) lifts "
		"the ball back up, both release.",
		MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.lower-entry-and-ball-gate", "Lower playfield entry track and ball gate", "gate",
		["coil.lower-ball-gate"], ["switch.track-switch"],
		"A ball that drops through the black hole runs down a track to the lower playfield, where it waits on the track switch (53) at the lower "
		"ball gate (lamp 8, remote transistor Q3). The ROM opens the gate once to put the ball into play (gameplay run). Because it hangs on a lamp "
		"driver, the ROM's lamp-driver test chase pulses it too.",
		MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.lower-yellow-bank", "Lower yellow four-bank drop targets", "drop_target_bank",
		["coil.lower-yellow-bank-reset"], [f"switch.{slug(LOWER_SWITCHES[a][0])}" for a in (40, 50, 60, 70)],
		"Four yellow drop targets on the lower playfield's left (40 nearest the player to 70), each with an insert (44-47) that lights when the "
		"matching right-side spot target is made. Completing the bank opens the re-entry gate and, with all targets lit, lights the extra ball; "
		"the bank resets (solenoid 5) only when the ball leaves the lower playfield (gameplay run).",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.lower-white-bank", "Lower white three-bank drop targets", "drop_target_bank",
		["coil.lower-white-bank-reset"], [f"switch.{slug(LOWER_SWITCHES[a][0])}" for a in (41, 51, 61)],
		"Three white drop targets on the lower playfield's right (41 at the right end to 61). Completing the bank opens the re-entry gate, advances "
		"the upper rollunder value and awards the special when lit; it resets (solenoid 6) when the ball leaves the lower playfield (gameplay run).",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.lower-capture-hole", "Lower playfield capture hole", "kicker",
		["coil.lower-hole-kicker"], ["switch.lower-hole-kicker-switch-lower-capture-hole"],
		"A capture hole at the lower playfield's lower left (switch 42, kicker lamp 12), always active, with three blue arrows (lamp 19) flashing "
		"until a ball is captured. A captured ball is remembered from ball to ball; multiball starts when a ball reaches the lower playfield while "
		"both capture holes are occupied, and the lower ball is released first; all captive balls are ejected at game over. The retained harness "
		"runs do not reach a multiball, so they show the kicker only in the lamp-driver test.",
		MANUAL_IDOC_SOURCE, MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.ball-lift", "Ball lift and re-entry tube", "kicker",
		["coil.ball-lift-kicker"], ["switch.ball-tube-kicker-switch"],
		"Balls drain from the lower playfield past its flippers at the backbox end into the ball tube kicker (43), where the ball lift kicker "
		"(lamp 14, coil A-4893, fused 6 1/4 A) fires them up the clear re-entry tube to the upper playfield's right side. The gameplay run pulses "
		"lamp 14 and releases the U and L relays when 43 closes.",
		MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.reentry-gate", "Re-entry wireform gate", "diverter",
		["coil.reentry-wireform-gate"], [],
		"A wireform gate (lamp 18, coil A-17564) at the top of the re-entry tube. Energized, it directs the lifted ball onto the upper playfield; "
		"released, the ball is lost to the outhole. The manual opens it when either lower bank is completed or the ball crosses the flashing right "
		"return rollover, and keeps it open in 3-ball play; upper pop bumpers and ten-point switches close it except in multiball. The gameplay run "
		"energizes it at game start and releases it as the ball returns from the lower playfield.",
		MANUAL_IDOC_SOURCE, MANUAL_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.game-over-and-tilt-relays", "Game over (Q) and tilt (T) relays", "other",
		["relay.game-over-q", "relay.tilt-t"], ["switch.tilt-switch-playboard", "switch.slam"],
		"The Q relay (lamp 0) energizes for a game and the T relay (lamp 1) on a tilt; together their contacts switch the +38 V flipper and +24 V "
		"kicking-rubber supplies, and T also the upper illumination and the light box tilt lamp. Closing the playboard tilt switch (26) once tilts "
		"the game (tilt-26 run); opening the slam switch (-1) ends it (slam run). PinMAME publishes Q-and-not-T as solenoid 10 and T as 11.",
		MANUAL_SOURCE, MANUAL_IDOC_SOURCE, RUN_SOURCE["tilt-26"], RUN_SOURCE["slam"], game, CORE_SOURCE)
	add("mech.right-flippers", "Right flippers (two upper, one lower)", "other",
		["virtual.right-flipper-power-synthetic", "virtual.right-flipper-hold-synthetic"], ["switch.right-flipper-button"],
		"The right cabinet button powers, through the U relay's normally closed contact, the upper playfield's two right flippers (the lower right "
		"flipper and the one above the right return lane), each through its own end-of-stroke switch, and, through the L relay's normally open "
		"contact, the lower playfield's right flipper (page 45; A-17875 coils). Only the Q and T relays enable them; the CPU never reads the "
		"button. In PinMAME the consumer drives 112 and gates 45/46 by lamps 16 and 17.",
		MANUAL_SOURCE, CORE_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.left-flippers", "Left flippers (two upper, one lower)", "other",
		["virtual.left-flipper-power-synthetic", "virtual.left-flipper-hold-synthetic"], ["switch.left-flipper-button"],
		"The left cabinet button powers the upper playfield's lower left flipper and its upper left flipper (on the left side above the left pop "
		"bumper) through the U relay, and the lower playfield's left flipper through the L relay (page 45). In PinMAME the consumer drives 114 and "
		"gates 47/48 by lamps 16 and 17.",
		MANUAL_SOURCE, CORE_SOURCE, game, VPX_SCRIPT_SOURCE)
	add("mech.upper-pop-bumpers", "Upper pop bumpers (4)", "other", [], ["switch.pop-bumpers-4"],
		"Four pop bumpers, each fired by its own switch through its own pop bumper driver board (1A8-4A8, A-1496 coils, fuses F10-F13) on the "
		"switched +38 V, not by the controller; the matrix switch 06 is their shared scoring contact. Their lamps are on the upper 6.3 V AC "
		"illumination behind the T and U contacts.",
		MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
	add("mech.lower-pop-bumpers", "Lower pop bumpers (2)", "other", [], ["switch.lower-level-pop-bumpers-2"],
		"Two pop bumpers on the lower playfield, each fired by its own driver board (5A8, 6A8; fuses F21, F22); matrix switch 71 is their shared "
		"scoring contact.",
		MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
	add("mech.upper-kicking-rubbers", "Upper kicking rubbers (2)", "other", [], ["switch.10-point-switches-5"],
		"Two kicking-rubber (slingshot) coils (A-1496), on the left beside the capture hole and on the right beside the window, each fired by two "
		"kicking-rubber switches through the T and Q contacts on the switched +24 V, not by the controller (page 45). The matrix sees the "
		"surrounding rubbers' ten-point contacts on 34.",
		MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
	add("mech.lower-kicking-rubber-and-target", "Lower kicking rubber and kicking target", "other", [], ["switch.10-point-switches-and-kicking-target"],
		"On the lower playfield a kicking-rubber coil fired by two kicking-rubber switches and a kicking target (A-5194 coil) fired by its own "
		"switch, both on the switched +24 V behind the L relay (page 45); matrix switch 72 is their ten-point scoring contact.",
		MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
	add("mech.left-spinner", "Left spinning target", "other", [], ["switch.left-spinning-target"],
		"A spinner in the left lane; switch 16 scores each revolution (100, 1,000 when lit by completing B-L-A-C-K).",
		MANUAL_IDOC_SOURCE, VPX_SCRIPT_SOURCE)
	return m


# --- Relationships -------------------------------------------------------------------------------------

def relationships() -> list[dict[str, Any]]:
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	items = [
		("relationship.q-relay-drives-game-on", "direct", "relay.game-over-q", "virtual.game-on", (*core, RUN_SOURCE["gameplay-causality"])),
		("relationship.t-relay-inhibits-game-on", "inverted", "relay.tilt-t", "virtual.game-on", (*core, RUN_SOURCE["tilt-26"])),
		("relationship.t-relay-drives-tilt-state", "direct", "relay.tilt-t", "virtual.tilt-relay-state", (*core, RUN_SOURCE["tilt-26"])),
		("relationship.spot-1-inverse-of-lamp-44", "inverted", "lamp.1-drop-target-light-lower-playfield", "lamp.1-spot-target-light", (*core, MANUAL_IDOC_SOURCE, RUN_SOURCE["lamp-driver-test"])),
		("relationship.spot-2-inverse-of-lamp-45", "inverted", "lamp.2-drop-target-light-lower-playfield", "lamp.2-spot-target-light", (*core, MANUAL_IDOC_SOURCE, RUN_SOURCE["lamp-driver-test"])),
		("relationship.spot-3-inverse-of-lamp-46", "inverted", "lamp.3-drop-target-light-lower-playfield", "lamp.3-spot-target-light", (*core, MANUAL_IDOC_SOURCE, RUN_SOURCE["lamp-driver-test"])),
		("relationship.spot-4-inverse-of-lamp-47", "inverted", "lamp.4-drop-target-light-lower-playfield", "lamp.4-spot-target-light", (*core, MANUAL_IDOC_SOURCE, RUN_SOURCE["lamp-driver-test"])),
	]
	for side, outputs in (("right", ("power", "hold")), ("left", ("power", "hold"))):
		for kind in outputs:
			items.append((f"relationship.game-on-gates-{side}-flipper-{kind}-synthetic", "relay_gated", "virtual.game-on", f"virtual.{side}-flipper-{kind}-synthetic", (*core, RUN_SOURCE["gameplay-causality"])))
	return [
		{"id": identifier, "kind": kind, "source": source, "destination": destination, "provenance": provenance(*refs)}
		for identifier, kind, source, destination, refs in items
	]


# --- Coverage and assembly ------------------------------------------------------------------------------

MISSING = ["input_semantics", "spatial_placement", "unresolved_conflicts"]


def build() -> dict[str, Any]:
	inputs = input_devices()
	outputs = solenoid_outputs() + lamp_outputs() + gi_outputs()
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Black Hole", "manufacturer": "Gottlieb", "year": 1981, "kind": "physical_pinball",
			"ipdb_id": 307, "opdb_id": "G41yq-MQP65", "model_number": "668",
			"playfield": {"units": "vpx", "width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": STATUS,
			"missing": MISSING,
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "observed",
				"physical_wiring": "observed",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"display_inventory": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.gts80", "hardware_generation": "0x200000000", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": inputs,
		"outputs": outputs,
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "partial"},
		"conflicts": [
			{
				"id": "conflict.tilt-pop-bumper-lights",
				"path": "outputs.relay.tilt-t",
				"description": (
					"The manual's tilt mode (printed page 6, III.E.2) says 'When the game is tilted, all the playfield lamps go off except the pop "
					"bumper lights', but its non-controlled illumination sheet (printed page 45) feeds every pop bumper lamp from the 6.3 V AC "
					"string (wire 788) that the T relay's normally closed contact opens on a tilt: the four upper pop bumpers through the U relay's "
					"normally closed contact and the two lower ones through the L relay's contact, while T's normally open side lights the light "
					"box TILT lamp (wire 022). No controlled lamp is a pop bumper light, so one of the two descriptions is wrong, and a recreation "
					"must decide whether the pop bumper caps stay lit on a tilt. Resolution path: tilt a working Black Hole and note whether the "
					"pop bumper lamps stay lit, which any owner or operator of the machine can do."
				),
				"source_refs": [MANUAL_IDOC_SOURCE, MANUAL_SOURCE],
				"status": "unresolved",
			},
		],
	}
	return definition


SPATIAL_BLOCKERS = [
	"Every placement comes from one community table (cyberpez's vpx 1.1) and keeps its observed status: the table's objects were matched "
	"to the manual's location drawings (printed pages 40 and 42) by side, order and neighbourhood, not by a registered fit with a "
	"leave-one-out check, and no second factory-layout table is retained.",
	"The lower playfield's devices are placed where the table draws them, under the window in the shared plan; the manual's lower playfield "
	"drawing has its own frame and has not been registered onto the table.",
	"Switch 26 (the playboard tilt) has no table object and keeps no spatial record; the drawing prints SW26 at the lower left above the apron.",
	"Switch 34's table also binds the right kicking rubber (Sling2), where the drawing prints no SW34; it is left unplaced.",
]


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	located_outputs: list[dict[str, Any]] = []
	na_inputs: dict[str, list[dict[str, Any]]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	omitted: list[dict[str, Any]] = []
	statuses: dict[str, int] = {}
	count = 0
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			binding = {"group": device["binding"]["group"], "address": device["binding"]["device"]}
			spatial = device.get("spatial")
			if spatial is None:
				omitted.append(binding)
			elif spatial["status"] == "not_applicable":
				(na_inputs if collection == "inputs" else na_outputs).setdefault(spatial["reason"], []).append(binding)
			else:
				(located_inputs.append(binding["address"]) if collection == "inputs" else located_outputs.append(binding))
				for item in spatial["placements"]:
					count += 1
					statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	key = lambda item: (item["group"], item["address"])  # noqa: E731
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/1116; 0=left, 1=right",
			"y": "y/2186; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256, "source_ref": VPX_EXTRACTION_SOURCE, "vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {"table_sha256": TABLE_SHA256, "embedded_script_sha256": SCRIPT_SHA256, "spatial_candidates_sha256": SPATIAL_CANDIDATES_SHA256},
		"placement_count": count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=key),
		"not_applicable_inputs": {reason: sorted(values, key=key) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=key) for reason, values in sorted(na_outputs.items())},
		"omitted": sorted(omitted, key=key),
		"projections": [
			{"group": SOLENOID, "address": 1, "reason": "Midpoint of the H-O-L-E bank's two middle targets (TargetO, TargetL2): the reset coil sits under the bank."},
			{"group": SOLENOID, "address": 2, "reason": "The B-L-A-C-K bank's middle target (TargetA): the reset coil sits under the bank."},
			{"group": SOLENOID, "address": 5, "reason": "Midpoint of the yellow bank's two middle targets (TargetLL50, TargetLL60)."},
			{"group": SOLENOID, "address": 6, "reason": "The white bank's middle target (TargetLR51)."},
			{"group": SOLENOID, "address": 9, "reason": "The table's drain kicker below the flippers, where the outhole kicker sits."},
			{"group": LAMP, "address": 8, "reason": "The table's sw53 kicker, where the ball waits at the lower ball gate."},
			{"group": LAMP, "address": 15, "reason": "The table's trough exit kicker (kicker1), which its ReleaseBall kicks."},
			{"group": LAMP, "address": 18, "reason": "The table's Flipper1 diverter at the re-entry tube's exit."},
		],
		"excluded_object_classes": [
			"Light objects gi1-gi21, Flashers lgi1-lgi4 and Flasher20-Flasher27: the table's G.I. lights, which it switches from lamps 16 and 17; the machine's illumination is not a controller output",
			"Lights BLight1b-BLight4b, b5light, b6light and the PBumpCap primitives: pop bumper cap lights the table drives from lamps 2 and 17",
			"Lights L39a, L39b and the TubeGlow primitive: re-entry gate and tube indicators the table drives from its own lamp numbers 123, 138 and 139",
			"Flashers H19a-c, h20a-c, h4-h6, h44, H45-H47 and CaptiveLightHalo: halo sprites over the inserts",
			"Light LCaptiveLight: a coloured glow the table adds at the capture hole from lamp 37; lamp 37's insert is L37",
			"Kickers kicker2 and kicker4-kicker6 and LowerStage, Triggers Trigger1, ToBasementRampEnd, ReEnrtyTubeExit, Tsling7, tWallHit1-2: trough stages and physics or sound helpers with no switch binding",
			"Wall Sling2: the right upper kicking rubber, whose handler also pulses 34 although the drawing prints no SW34 there",
		],
		"unresolved": [{"group": SWITCH, "address": 26, "reason": "No table object for the playboard tilt switch."}],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Black Hole (Gottlieb, 1981) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/gottlieb/black-hole-1981.json`; its spatial "
		"dimension stays open because of the blockers below.",
		"",
		f"The geometry source is the retained `Black Hole (Gottlieb 1981) vpx 1.1.vpx` by cyberpez, SHA-256 `{TABLE_SHA256}`, whose embedded "
		f"script (SHA-256 `{SCRIPT_SHA256}`) is the binding authority. Bounds are `{TABLE_BOUNDS}`; every coordinate is x/1116 and y/2186, "
		"rounded to at most six places.",
		"",
		"## Evidence decisions",
		"",
		"- A switch placement is the centre of the table object the script binds to the address: a trigger, hit target, kicker, bumper, "
		"spinner or the drag-point centroid of a target or rubber wall. A shared address (06 pop bumpers, 34 and 72 ten-point switches, 71 lower "
		"bumpers) gets one placement per object the drawing confirms.",
		"- A lamp placement is the script-bound insert light: the upper playfield's Light objects and the lower playfield's insert Flasher "
		"objects, which this table uses as the inserts themselves. Lamps 19 and 20 have three bulbs each, as the drawing prints them.",
		"- Coils on lamp drivers (8, 12-15, 18) sit at the kicker, hole or diverter object the script fires; the bank reset coils are projected "
		"under their banks (below).",
		"- Relays, the coin lockout, the coin counters, the knocker, the Sound 16 line, the light box lamps, cabinet and service switches, the "
		"DIPs and the four player displays take controlled `not_applicable` records. The two status-display pairs and the lower playfield "
		"display are on the playfield and placed on the table's display walls.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		short = "Solenoid" if entry["group"] == SOLENOID else "Lamp"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Devices without a spatial record: {len(report['omitted'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion is refused. Besides the spatial blockers, the cabinet wiring sheet (printed page 47) is cropped in both retained manual "
		"copies, so the fitment of return-7 positions 57, 67 and 77 stays unknown (`input_semantics`). A complete scan of the manual's fold-out "
		"sheets, and a registered fit of the two location drawings onto the table, would close both.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Black Hole definition with a {STATUS} one: {stale}")
		stale.unlink()
	for retired in RETIRED_ARTIFACTS:
		target = root / retired.relative_to(ROOT)
		if target.exists():
			target.unlink()
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	(root / KNOWLEDGE_PATH).write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Black Hole is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	for retired in RETIRED_ARTIFACTS:
		if (root / retired.relative_to(ROOT)).exists():
			raise RuntimeError(f"retired Black Hole residual artifact still exists: {retired.relative_to(ROOT).as_posix()}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Black Hole definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Black Hole seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Black Hole spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Black Hole spatial review drifted from its deterministic curator: {markdown_path}")
	knowledge_path = root / KNOWLEDGE_PATH
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != KNOWLEDGE_SEED_PATH.read_bytes():
		raise RuntimeError(f"Black Hole knowledge note drifted from its pinned seed: {knowledge_path}")
	print("Black Hole definition, seed, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, the knowledge note and the pinned seeds")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed, the knowledge note and the spatial report")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest")
	args = parser.parse_args()
	if args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Black Hole retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
