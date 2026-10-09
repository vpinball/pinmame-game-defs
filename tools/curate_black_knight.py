"""Curate the physical Williams Black Knight (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is embedded as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed, the spatial
audit and the knowledge note.

Evidence priority actually applied here, in the runbook's order:

1. The retained known-working VPX script (Bord, version 3.0, November 2021, byte-identical to the
   pinned vpx-standalone-scripts copy) for runtime callbacks, ball routing and lamp bindings, except
   where it is demonstrably defective.
2. The English game manual with paginated schematics (instruction booklet 16P-500-103, the wiring
   diagrams and the board schematics) for physical construction, wiring, quantities and locations.
3. Pinned PinMAME source for the System 7 controller contract, the special-solenoid switch map and
   the display layout.
4. The retained table's exact geometry for coordinates; the booklet's switch-location drawing,
   registered onto the table frame, supplies coordinates only for devices the table does not model.
5. Hash-pinned LibPinMAME harness runs of the production ROM's own solenoid and switch tests and of
   gameplay sequences, which settle numbering, display roles and mechanism causality, and a static
   reading of the ROM's DIP-port accesses.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
STATUS = "author_ready"
PARTIAL_PATH = ROOT / "machines/partial/williams/black-knight-1980.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/black-knight-1980.json"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/black-knight-1980.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/black-knight-1980.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/black-knight-1980.md"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/black-knight-1980.md"

MACHINE_ID = "williams.black-knight.1980"
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-7"
MANUAL_SOURCE = "manual.williams.black-knight.1980"
SCHEMATICS_SOURCE = "manual.williams.black-knight.1980.schematic-diagrams"
HANDBOOK_SOURCE = "manual.williams.black-knight.1980.instruction-booklet"
KIT_SOURCE = "service-bulletin.williams.a-8762"
IPDB_SOURCE = "ipdb.310"
ROM_SOURCE = "rom.black-knight.dip-port-reads"
VPX_TABLE_SOURCE = "vpx-table.black-knight-bord-3-0"
VPX_SCRIPT_SOURCE = "vpx-script.black-knight-bord-3-0"
VPM_LIBRARY_SOURCE = "vpx-script.vpinmame-s7-library"
VPX_EXTRACTION_SOURCE = "vpx-extraction.black-knight-bord-3-0"
CORPUS_SCRIPT_SOURCE = "vpx-script.black-knight-standalone-corpus"
GEOMETRY_SOURCE = "human-review.black-knight-figure-3-registration"
HARNESS_SOLENOID_SOURCE = "runtime.black-knight.solenoid-test"
HARNESS_SWITCH_SOURCE = "runtime.black-knight.switch-test"
HARNESS_GAMEPLAY_SOURCE = "runtime.black-knight.gameplay-causality"
HARNESS_MULTIBALL_SOURCE = "runtime.black-knight.multiball"
HARNESS_DISPLAY_SOURCE = "runtime.black-knight.four-player-displays"
HARNESS_L3_SOURCE = "runtime.black-knight.l3-solenoid-test"
HARNESS_F4_SOURCE = "runtime.black-knight.f4-solenoid-test"

MANUAL_SHA256 = "3ce4bf0cf3e66150900c579b48302623a654384e0ed558bf64577d300078bb96"
SCHEMATICS_SHA256 = "7538cc080e02c4e44d9c94fab864afcedf356fbfa500202001f1534d28b6eda7"
HANDBOOK_SHA256 = "4758a5fb5fe340874c3e9f321b4688c520e15a7163f9dc941193d53fd2f95e09"
KIT_SHA256 = "6e7875c488be446a8777e4bb34ff6ee315bb75ffa6455130c280bd18d59d5af7"
IPDB_PAGE_SHA256 = "d39d9b75a86923eaff598993b5f3acba1ee8c75c7546c87eaa93bc2f99c43522"
TABLE_SHA256 = "bfaf38dfacd2c7982a609ec219e041c01886eb53cb368ae225e1d7924a5c994c"
SCRIPT_SHA256 = "8f3b80424f7376d30c39524ac28992a186741477febe10db09b2ca3a48219bf8"
# s7.vbs as the operator's VPinMAME installation holds it; byte-identical to scripts/s7.vbs in
# vpinball/vpinball at VPM_LIBRARY_REVISION.
VPM_LIBRARY_SHA256 = "88e6f2500f75315b9f5ad01581d9f24a926ad12af43730af01d8bfab8e5cfe03"
VPM_LIBRARY_REVISION = "6237ce52ef9cee9b9814881f6289d207bf9a3d2b"
CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_SHA256 = {
	"bk_l4": "86e9da7a6170c9d45fb0b37a3f571452d1e79b1e94cc62cdddedf7cd032f6e63",
	"bk_l3": "f030e18a7c37bf56fbc22b234593b55954fe56c05535a933b70819fd736aad2b",
	"bk_f4": "42e37f2e61ce97c0be0965636d59f6b0b918784ff150159c41261fa179b1c666",
}

# run file: (run sha256, scenario file, scenario sha256, init run sha256, game)
HARNESS_RUNS = {
	"run-sol.json": ("bb2a1c7c49d338779036cfc73564a3243eabdf9dd22973f606684e9ba403a3ee", "black-knight-solenoid-test.json", "f542658cf0c1aa105daba00c06c1e0f1f5d19de0f1ef1cb7d06ba6edb1ca7825", "2df7abdd46907054676a120571b768e863cae93ef5e6f986a3af9183980418ce", "bk_l4"),
	"run-sw.json": ("141ee097c5e0c94a6a8ed663a6fe2d663c7bd4a4c58f66bfad62fe5adb197ba6", "black-knight-switch-test.json", "ea4b8cc2b752cfa68973fb9984e305d9becedf5163724060848d64dce4e6b2d8", "7952617a8ee2ad4f71e8641b3244486741e44f569b8358d30480649e958ca394", "bk_l4"),
	"run-play.json": ("ce4901c73373b5d67779d314367dfebcba4b71615d3980aaf79025cbd51c22da", "black-knight-gameplay-causality.json", "4f1de42950c7fc0610a88b7eb90640d0fd7a94e9487379ce6e630bd0c35ccc82", "f607ff7b5e19b79743ceced5e4faa6bd197d746821b282e59bd2e51ab21b58f2", "bk_l4"),
	"run-mb.json": ("4a67e405861d88cf6c6b5728f6036d1c6cab841187d9e3794edc73f1a8b7f2c4", "black-knight-multiball.json", "9cc83f4b4fbf924d41bc46853d308b03918a1f90abf67c7a28492a408ae95349", "be1a27c2e41870b6df9bd9a39e505f1cf0f0eaf21679f08579371516d63573c4", "bk_l4"),
	"run-4p.json": ("72a305dd6a57a09a64e5ab1e7eba1ac6bd54907b69d84f13feb5058b45781e18", "black-knight-four-player-displays.json", "519da4dbc93e9a090e73ba33929d16ec76e244997db85c4b2c00a9f699d87458", "4de14bfaa319c323a231be1ffdae1340833cec69fa07e24750de5edb90cfadd6", "bk_l4"),
	"run-sol-l3.json": ("dfe1b2f87c697ce7b2c079ebeabefd6a2e85427bb7cd6974b063000e5d148722", "black-knight-l3-solenoid-test.json", "5c2145a423c67576e9242ef47766da34610145914d835f177b7f43e285018d0f", "6a5e6fad248efdc5c1f46584af78583bc855dfa0f4123f1a55d299b802585a49", "bk_l3"),
	"run-sol-f4.json": ("683ca047cc9d42b9743c3fa83f8eb185c01066fff6b480eff9f9f56c4a275ca6", "black-knight-f4-solenoid-test.json", "d62e0b2d0da7d4d866e20ca42e248be90ed7831ad5dfdfe94359c5531bec23fd", "46cee6a306fdd1f7865c7d504220e7f697c677ae0c1e041611337ef05e448caf", "bk_f4"),
}
# game: NVRAM-initialization scenario file and sha256
HARNESS_BOOT = {
	"bk_l4": ("black-knight-nvram-init-boot.json", "0f76a557b40f4a90ea9c8b4bc397316db1e4b34a28576859d527eeaaa780b913"),
	"bk_l3": ("black-knight-l3-nvram-init-boot.json", "918963bec06cf99a01b0befc5d0875ebbee55039e3c9ad090b28ec196e7e9b9e"),
	"bk_f4": ("black-knight-f4-nvram-init-boot.json", "cadcef42b1ac35a7899ed93617914df17fa7ea458d60b52b457e40f255cf3bc2"),
}
# Canonical manifest of the whole external runtime-evidence directory (every raw run, every
# initialization run and each state directory's cfg and NVRAM):
# external:pinmame-runtime-evidence/black-knight-1980.manifest.json.
RUNTIME_MANIFEST = (35, 6702842, "8dcfd956cb4f81c9b881aa60f7e92820d0cb35ef137dc8f63c3ca322114e4538")

EXTRACTION_ROOT = Path("williams/black-knight-1980/extracted-vpxtool")
EXTRACTION_DIRECTORY = "black-knight-bord-3.0"
EXTRACTION = (1323, 164805613, "dc16b9dbfc8b1d9fe199f26f8cd7daec7f16ce1d7938c1b8ae4f22e9a571948f")

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

EXCERPT_DIGESTS: dict[str, str] = {
	"cabinet-wiring.md": "ac04b85a2e8dc5d542ae34e778c67a6bce1285e38a8c221a5868f15a50cfeb58",
	"lamp-matrix.md": "2c3a670bce509d41011b1891c4c460e16c4e0c8fee1e5ea6eaf8c0a1388fc042",
	"master-display-lamps.md": "5038c1bcfa5f5a88e1cc2ac5871fbfa36221bcbd1c9c6614a5c991194eb547bb",
	"operation-and-diagnostics.md": "cdd447b043652c3a832374ef3b922341780d2be09f04dd3f6c0ba5565c6e88b4",
	"playfield-lamp-wiring.md": "4808bfccaf391b47e04e53a41f544b66e8c664a4ba7cb0f4c0af11904a699843",
	"playfield-solenoid-wiring.md": "adb37a843eb718cd184908709b9b34e2d9b69e548be62c9a9e7c78065073a588",
	"playfield-switch-wiring.md": "c1c45f738ef227eb79d21bb76ea1a7304eb3ea60a7d1caeb198d4106dbe1deef",
	"power-wiring.md": "822609a574d168a0e91e69860c39cf7bc1d0cc79779f8c50ded6aa10a433007d",
	"retrofit-kit-a-8762.md": "a094a06258192d9995138f72bde446888537c1b5f44c43cf6b5a661b26741e3f",
	"rom-dip-reads.md": "45c496552a5a20a7fb72b2991db3bc323e09a914056ddb412b037728c0cb049f",
	"solenoid-connections.md": "404e4f0503e7e6283cd58117b57834ba546eb3d7311c260cb1d40b7cd073d82a",
	"solenoid-locations.md": "756b9b3fcaea15aae4dab3b9dcca808246db111a81e5bb7346f1b275e6d6c2b1",
	"switch-locations.md": "bd9837e12debb9bdb7258bdb61452e74772ab4d1d7852fa2fe3a5343324a6d9e",
	"switch-matrix.md": "0b389e3c072d05819e7c5633de4b087a9c02b63ddc79d8023ee8a39f1c4c35eb",
	"vpm-s7-library.md": "081da965c06cacab7685f5d33fad2cb75eadc92748fb62f21cda5fea9ac3ca12",
}

# --- Exact centres of the retained table objects used for placements, in table units. Triggers,
# kickers, the bumper, the spinner and lights use their stored centre; walls (slingshots and the
# drop-target primaries) use the centroid of their drag points.
TABLE_POINTS: dict[str, tuple[float, float]] = {
	"sw11": (47.62415, 1440.5862),
	"sw12": (810.41907, 1441.5378),
	"Spinner": (155.9278, 705.52264),
	"sw14": (678.0029, 787.8252),
	"sw15": (745.60913, 1375.3816),
	"sw16": (115.04801, 1375.5354),
	"LeftSlingshot": (211.470088, 1397.256925),
	"RightSlingshot": (643.90444, 1387.855225),
	"sw23": (366.99414, 520.16016),
	"sw24": (517.7518, 741.6429),
	"sw25": (103.5922, 1006.455168),
	"sw26": (120.0881, 947.570925),
	"sw27": (136.75421, 889.817442),
	"sw29": (472.737117, 846.9982),
	"sw30": (424.17868, 812.315023),
	"sw31": (374.69183, 777.09151),
	"sw33": (262.3532, 307.995285),
	"sw34": (275.269227, 248.9143),
	"sw35": (289.330505, 190.440018),
	"sw37": (710.3474, 250.935808),
	"sw38": (672.6485, 203.534873),
	"sw39": (635.2821, 156.743793),
	"Bumper1": (470.20615, 182.43678),
	"sw44": (123.164375, 158.8467),
	"sw45": (893.48224, 1735.7867),
	"BallRelease": (843.15643, 1695.6274),
	"LockOut": (187.65463, 262.17188),
	"MagnetL": (114.583984, 1222.7715),
	"MagnetR": (746.53906, 1222.5391),
	# Insert lights, bound by the script's InitLights through their TimerInterval.
	"Light038": (607.6107, 1222.9934),
	"Light037": (242.0971, 1224.3552),
	"Light030": (48.53529, 1338.932),
	"Light029": (804.72424, 1339.6112),
	"Light033": (192.79987, 815.0959),
	"Light039": (579.31665, 1089.4962),
	"Light028": (687.0781, 1502.3662),
	"Light031": (166.75525, 1503.207),
	"Light032": (168.02628, 964.5227),
	"Light036": (395.17914, 853.4295),
	"Light045": (325.618, 260.7978),
	"Light043": (633.79517, 231.88916),
	"Light050": (584.13605, 66.83232),
	"Light034": (300.63968, 725.0131),
	"Light035": (281.2184, 645.9606),
	"Light022": (524.5181, 928.8785),
	"Light021": (197.53717, 1164.3293),
	"Light026": (208.46286, 1119.4742),
	"Light027": (221.09683, 1073.5012),
	"Light019": (340.3192, 1224.5436),
	"Light025": (464.19968, 1007.53204),
	"Light024": (429.13986, 978.63135),
	"Light023": (387.54004, 945.3174),
	"Light020": (514.5506, 1225.5841),
	"Light046": (445.716, 450.6503),
	"Light047": (415.0502, 376.17377),
	"Light048": (396.7551, 308.53485),
	"l36": (469.22354, 180.45903),
	"Light040": (604.4385, 448.8049),
	"Light041": (603.1903, 377.77664),
	"Light042": (592.9889, 307.96637),
	"Light049": (771.17847, 288.71692),
	"Light044": (123.065636, 243.25157),
	"Light051": (351.93744, 71.42629),
	"Light010": (427.21896, 1698.9336),
	"Light009": (428.11566, 1631.1195),
	"Light008": (427.64023, 1571.6597),
	"Light007": (428.35324, 1512.9586),
	"Light006": (425.64236, 1455.8203),
	"Light001": (426.7797, 1403.4634),
	"Light011": (428.10446, 1354.9199),
	"Light012": (428.2487, 1308.4922),
	"Light013": (428.10443, 1260.9095),
	"Light014": (428.10443, 1214.817),
	"Light015": (427.98343, 1166.9445),
	"Light016": (428.4993, 1122.8021),
	"Light017": (427.92252, 1079.2361),
	"Light018": (428.84805, 1034.9338),
	"Light002": (309.41092, 1506.209),
	"Light003": (366.57312, 1488.7306),
	"Light004": (489.24805, 1489.5973),
	"Light005": (548.89734, 1508.4844),
}

# Registration of the booklet's Figure 3 (handbook PDF page 12, 400 dpi render, 2328 x 3534 px)
# onto the retained table frame; see evidence/excerpts/williams.black-knight.1980/switch-locations.md.
# Each control pairs a drawing pixel with the table point of the same feature.
FIGURE3_CONTROLS: dict[str, tuple[tuple[int, int], tuple[float, float]]] = {
	"Bumper1 (jet bumper 36)": ((627, 1110), (470.206, 182.437)),
	"Spinner (13)": ((303, 1657), (155.928, 705.523)),
	"sw34": ((418, 1168), (275.269, 248.914)),
	"sw38": ((847, 1140), (672.649, 203.535)),
	"sw30": ((585, 1780), (424.179, 812.315)),
	"sw44": ((263, 1090), (123.164, 158.847)),
	"sw11": ((184, 2410), (47.624, 1440.586)),
	"sw12": ((975, 2410), (810.419, 1441.538)),
	"sw16": ((251, 2340), (115.048, 1375.535)),
	"sw15": ((905, 2340), (745.609, 1375.382)),
	"LeftFlipper pivot": ((400, 2625), (267.619, 1636.758)),
	"LeftFlipper tip": ((506, 2688), (370.0, 1691.3)),
	"RightFlipper pivot": ((747, 2623), (589.855, 1636.491)),
	"RightFlipper tip": ((645, 2686), (487.4, 1691.0)),
	"apron bottom-right corner": ((1022, 2977), (873.0, 1974.0)),
	"sw39": ((809, 1088), (635.282, 156.744)),
	"frame top-left corner": ((137, 922), (0.0, 0.0)),
	"frame bottom-left corner": ((123, 2978), (0.0, 1974.0)),
}

# Drawing pixels read for the hidden devices; each is placed at its registered point.
FIGURE3_READINGS: dict[str, tuple[int, int]] = {
	"lockup-bottom": (328, 1190),
	"lockup-center": (342, 1138),
	"lockup-top": (355, 1083),
	"right-ball-ramp": (955, 2708),
	"center-ball-ramp": (897, 2737),
	"left-ball-ramp": (851, 2765),
	"outhole": (615, 2890),
	"playfield-tilt": (250, 2717),
}


def _solve3(m: list[list[float]], v: list[float]) -> list[float]:
	a = [row[:] + [value] for row, value in zip(m, v)]
	for col in range(3):
		pivot = max(range(col, 3), key=lambda r: abs(a[r][col]))
		a[col], a[pivot] = a[pivot], a[col]
		for r in range(3):
			if r != col:
				factor = a[r][col] / a[col][col]
				a[r] = [x - factor * y for x, y in zip(a[r], a[col])]
	return [a[r][3] / a[r][r] for r in range(3)]


def affine_fit(controls: list[tuple[tuple[float, float], tuple[float, float]]]) -> tuple[list[float], list[float]]:
	"""Least-squares affine map from drawing pixels (u, v) to table units: x = a u + b v + c."""
	rows = [(u, v, 1.0) for (u, v), _ in controls]
	normal = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
	fx = _solve3(normal, [sum(r[i] * t[0] for r, (_, t) in zip(rows, controls)) for i in range(3)])
	fy = _solve3(normal, [sum(r[i] * t[1] for r, (_, t) in zip(rows, controls)) for i in range(3)])
	return fx, fy


def apply_fit(fit: tuple[list[float], list[float]], point: tuple[float, float]) -> tuple[float, float]:
	u, v = point
	x, y = (c[0] * u + c[1] * v + c[2] for c in fit)
	return x, y


def two_decimals(value: float) -> float:
	return float(Decimal(repr(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


FIGURE3_FIT = affine_fit(list(FIGURE3_CONTROLS.values()))

# Hidden devices placed from the registered Figure 3. Two decimals: the fit's RMS residual is about
# 0.01 of the playfield width.
DRAWING_POINTS: dict[str, tuple[float, float]] = {}
for _name, _pixel in FIGURE3_READINGS.items():
	_x, _y = apply_fit(FIGURE3_FIT, _pixel)
	DRAWING_POINTS[_name] = (two_decimals(_x / PLAYFIELD_WIDTH), two_decimals(_y / PLAYFIELD_HEIGHT))


def normalized(name: str) -> tuple[float, float]:
	x, y = TABLE_POINTS[name]
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


# --- Switch matrix. Column and row wiring from the switch matrix sheet, the playfield switch
# wiring sheet and the cabinet wiring sheet.
SWITCH_COLUMNS = {
	1: ("GRN-BRN", "2J2-9", "7P1-19"),
	2: ("GRN-RED", "2J2-8", "8P1-1"),
	3: ("GRN-ORN", "2J2-7", "8P1-2"),
	4: ("GRN-YEL", "2J2-6", "8P1-3"),
	5: ("GRN-BLK", "2J2-5", "8P1-4"),
	6: ("GRN-BLU", "2J2-3", "8P1-5"),
	7: ("GRN-VIO", "2J2-2", "8J1-6 N.C."),
	8: ("GRN-GRY", "2J2-1", "8J1-7 N.C."),
}
SWITCH_ROWS = {
	1: ("WHT-BRN", "2J3-9", 8),
	2: ("WHT-RED", "2J3-8", 9),
	3: ("WHT-ORN", "2J3-7", 10),
	4: ("WHT-YEL", "2J3-6", 11),
	5: ("WHT-GRN", "2J3-5", 12),
	6: ("WHT-BLU", "2J3-4", 13),
	7: ("WHT-VIO", "2J3-3", 14),
	8: ("WHT-GRY", "2J3-1", 15),
}
# Switches the playfield switch sheet shades as mounted on the upper playfield.
UPPER_PLAYFIELD_SWITCHES = frozenset({14, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44})

SWITCHES: dict[int, dict[str, Any]] = {
	1: dict(label="Plumb Bob Tilt", role="cabinet.tilt", type="tilt", location="cabinet", cabinet="7SW1"),
	2: dict(label="Ball Roll Tilt", role="cabinet.tilt", type="tilt", location="cabinet", cabinet="7SW2"),
	3: dict(label="Credit Button", role="cabinet.start", type="button", location="cabinet front", cabinet="7SW3"),
	4: dict(label="Right Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW4", door=True, note="Printed 7SW4 RIGHT COIN CHUTE on the cabinet sheet. PinMAME's IPT_COIN1 keyboard bit lands on this address; the gameplay harness run posts credits from it."),
	5: dict(label="Center Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW5", door=True, note="Printed 7SW5 CENTER COIN CHUTE on the cabinet sheet."),
	6: dict(label="Left Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW6", door=True, note="Printed 7SW6 LEFT COIN CHUTE on the cabinet sheet."),
	7: dict(label="Slam Tilt", role="cabinet.slam-tilt", type="tilt", location="coin door", cabinet="7SW7", door=True, note="Printed 7SW7 SLAM TILT. The booklet: Slam tilt return game to game over."),
	8: dict(label="High Score Reset", role="service.high-score-reset", type="button", location="coin door", cabinet="7SW8", door=True, note="Printed 7SW8 HIGH SCORE RESET on the cabinet sheet."),
	9: dict(label="Right Magnet Button", role="cabinet.magna-save.right", type="button", location="cabinet side", cabinet="7SW9", note="Printed 7SW9 RIGHT MAGNET BUTTON, the right Magna-Save button on the side of the cabinet, in switch-matrix column 2 (GRN-RED, 7P1-20) row 1. With the right Magna-Save lamp (9) lit, closing it makes the ROM energize the right magnet relay (solenoid 9) for a few seconds; the gameplay harness run shows exactly that. The playfield switch sheet lists it in its legend but draws no playfield switch, because it is a cabinet switch."),
	10: dict(label="Left Magnet Button", role="cabinet.magna-save.left", type="button", location="cabinet side", cabinet="7SW10", note="Printed 7SW10 LEFT MAGNET BUTTON, the left Magna-Save button on the side of the cabinet, column 2 row 2. With the left Magna-Save lamp (10) lit, closing it makes the ROM energize the left magnet relay (solenoid 10) (gameplay harness run). The cabinet sheet prints its diode as 7D10, a designator it also prints on the coin lockout coil's diode."),
	11: dict(label="Left Outlane", obj="sw11", note="Wire rollover in the left outlane (5,000)."),
	12: dict(label="Right Outlane", obj="sw12", note="Wire rollover in the right outlane; the switch chart prints its score `(5000)` without the comma."),
	13: dict(label="Spinner", obj="Spinner", note="The spinner in the left orbit (100, or 2,500 while lit after the right inside rollover). The switch matrix sheet calls the cell LEFT SPINNER and the switch chart Spinner; the lamp that lights it is printed RIGHT SPINNER (lamp 13), yet it sits beside this same spinner on the left."),
	14: dict(label="Right Ramp Rollunder", obj="sw14", note="The right ramp rollunder (500, or the Mystery value while it flashes after the left inside rollover). The switch sheet shades it as mounted on the upper playfield."),
	15: dict(label="Right Inside Rollover", obj="sw15", note="Wire rollover in the right inlane (2,000, or 10,000 when made after using Magna-Save)."),
	16: dict(label="Left Inside Rollover", obj="sw16", note="Wire rollover in the left inlane (2,000, or 10,000 when made after using Magna-Save)."),
	17: dict(label="Right Ball Ramp", drawing="right-ball-ramp", ramp=True),
	18: dict(label="Center Ball Ramp", drawing="center-ball-ramp", ramp=True, note="The switch matrix sheet prints this cell CENTER BALL RAMP TARGET; the switch chart and the playfield switch sheet say Center Ball Ramp."),
	19: dict(label="Left Ball Ramp", drawing="left-ball-ramp", ramp=True),
	20: dict(label="Outhole", drawing="outhole", note="The outhole below the apron centre, at the lower left end of the dashed ball-ramp outline in Figure 3. The retained table has no outhole switch object: it models the outhole as the entry switch of its cvpmBallStack trough (InitSw 20, 17, 18, 19) on a drain kicker at the table's bottom edge, so the placement is the booklet's registered callout."),
	21: dict(label="Left Kicker", obj="LeftSlingshot", kicker=17, note="The scoring contact behind the left kicker (slingshot) rubber (10 points). The switch matrix sheet prints this cell `LOWER KICKER 3-BANK, LEFT TARGET`, a typing error: the switch chart, the playfield switch sheet and Table 4's special-switch note call it Left Kicker, and the ROM's switch test reports 21 for it."),
	22: dict(label="Right Kicker", obj="RightSlingshot", kicker=18, note="The scoring contact behind the right kicker (slingshot) rubber (10 points)."),
	23: dict(label="Turnaround", obj="sw23", note="The turnaround switch at the top of the lower playfield, under the ramp (5,000). Making it advances the bonus multiplier from 2X to 5X. The booklet's rule that the lock arrows do not flash until it is made is marked adjustable; the lockup trough mechanism records how the factory settings behave. Figure 3 draws it in a dashed circle; the table's trigger lies about 0.04 below the registered circle, and the table object is used."),
	24: dict(label="Lower Playfield Eject Hole", obj="sw24", note="The kick-out hole in the middle of the lower playfield (5,000)."),
	25: dict(label="Lower Left 3-Bank, Lower Target", obj="sw25", drop="lower left"),
	26: dict(label="Lower Left 3-Bank, Center Target", obj="sw26", drop="lower left"),
	27: dict(label="Lower Left 3-Bank, Upper Target", obj="sw27", drop="lower left", note="Switch Test step 5 in the booklet calls switch 27 the lower left 3-bank's `right target`; the switch chart, the matrix and the switch sheet all say Upper Target."),
	29: dict(label="Lower Right 3-Bank, Right Target", obj="sw29", drop="lower right"),
	30: dict(label="Lower Right 3-Bank, Center Target", obj="sw30", drop="lower right"),
	31: dict(label="Lower Right 3-Bank, Left Target", obj="sw31", drop="lower right"),
	33: dict(label="Top Left 3-Bank, Lower Target", obj="sw33", drop="top left"),
	34: dict(label="Top Left 3-Bank, Center Target", obj="sw34", drop="top left"),
	35: dict(label="Top Left 3-Bank, Upper Target", obj="sw35", drop="top left"),
	36: dict(label="Jet Bumper", obj="Bumper1", kicker=19, note="The jet bumper's scoring contact (500), on the upper playfield. The bumper also has its own special switch 8SW67, which fires the coil through the driver board and is not in the switch matrix."),
	37: dict(label="Top Right 3-Bank, Lower Target", obj="sw37", drop="top right"),
	38: dict(label="Top Right 3-Bank, Center Target", obj="sw38", drop="top right"),
	39: dict(label="Top Right 3-Bank, Upper Target", obj="sw39", drop="top right"),
	41: dict(label="Lockup Trough, Bottom", drawing="lockup-bottom", lock=True),
	42: dict(label="Lockup Trough, Center", drawing="lockup-center", lock=True),
	43: dict(label="Lockup Trough, Top", drawing="lockup-top", lock=True),
	44: dict(label="Left Ramp Rollover", obj="sw44", note="Wire rollover at the top of the left ramp, on the upper playfield (5,000; it awards an extra ball when lamp 41 is lit)."),
	45: dict(label="Ballshooter Trough", obj="sw45", note="The ball rests on this switch in the shooter lane until plunged. The booklet: a new game cannot start with more than one ball on it."),
	46: dict(label="Playfield Tilt", drawing="playfield-tilt", type="tilt", note="The playfield tilt below the lower left playfield (Figure 3 draws callout 46 in a dashed circle). The booklet: the ball in play is tilted on the third (adjustable) closure of the plumb bob and playfield tilts; the gameplay harness run shows relay 11 pulsing on the first two closures and the game-on enable (25) dropping on the third."),
}
# The three rebound standups behind the drop-target banks, matrix cells printed NOT USED STANDUP.
OPTIONAL_SWITCHES = {
	28: dict(label="Lower Left 3-Bank, Standup", obj="sw26", bank="lower left", targets=(25, 26, 27)),
	32: dict(label="Lower Right 3-Bank, Standup", obj="sw30", bank="lower right", targets=(29, 30, 31)),
	40: dict(label="Top Right 3-Bank, Standup", obj="sw38", bank="top right", targets=(37, 38, 39)),
}
UNUSED_SWITCH_NOTE = "Printed NOT USED in the switch matrix and not drawn on the playfield switch sheet, whose wires for switch columns 7 and 8 end at N.C. The ROM's switch test never reports this address."
DIAGNOSTIC_SWITCHES = {
	-7: ("Advance", "service.advance", "S7_SWADVANCE", "coin door", "The coin-door ADVANCE pushbutton, 7SW75 on the cabinet sheet, wired to the CPU board's 1P4-3 (GRN). PinMAME samples it into PIA 3 CA1 on every IRQ."),
	-6: ("Auto-Up / Manual-Down", "service.auto-manual", "S7_SWUPDN", "coin door", "The coin-door AUTO-UP / MANUAL-DOWN switch, 7SW74, wired to the CPU board's 1P4-4 (BLU) and sampled into PIA 3 CB1. Public level 1 is Auto-Up: the retained harness runs step the diagnostic tests with 1 and hold a single solenoid with 0, as the booklet's procedure requires."),
	-5: ("CPU Diagnostic", "service.cpu-diagnostic", "S7_SWCPUDIAG", "backbox", "The DIAGNOSTIC SWITCH SW1 on the CPU board logic diagram, wired to the CPU's NMI line; the booklet's CPU board self-test starts from it."),
	-4: ("Sound Diagnostic", "service.sound-diagnostic", "S7_SWSOUNDDIAG", "backbox", "SW1, the pushbutton beside DS1 on the sound board assembly drawing; the booklet's sound board self-test starts from the sound board's diagnostic switch."),
	-3: ("Master Command Enter", "service.master-command-enter", "S7_ENTER", "backbox", "SW2, the INPUT ENABLE pushbutton on the CPU board logic diagram. PinMAME returns the CPU-board DIP banks to the ROM only while it is held; the Black Knight ROM never consumes them (see the DIP records), and the booklet does not mention the button."),
}
FLIPPER_COLUMN_USED = {82: ("Right Flipper Button", "flipper.lower.right.button"), 84: ("Left Flipper Button", "flipper.lower.left.button")}

# DIP addresses follow the profile: bank * 8 + bit + 1.
DIPS: dict[int, tuple[str, str, str]] = {
	1: ("Sound Board DS1 Position 1", "used", "Position 1 of DS1, the two-position option switch beside SW1 on the sound board assembly drawing. PinMAME's S7_COMPORTS names it Sound Dip 1 (bank 0 bit 0, default 0) and src/wpc/wmssnd.c folds it into the command byte the sound CPU reads."),
	2: ("Sound Board DS1 Position 2", "used", "Position 2 of DS1 on the sound board. PinMAME's S7_COMPORTS names it Sound Dip 2 (bank 0 bit 1, default 1) and src/wpc/wmssnd.c folds it into the sound command byte."),
}
for _bit in range(8):
	DIPS[9 + _bit] = (
		f"CPU Board Function Bank F{_bit + 1}",
		"unused",
		f"PinMAME's F{_bit + 1} (bank 1 bit {_bit}), returned on PIA 3 port A by s7_dips_r only while Master Command Enter (-3) is held. The Black Knight game ROM never consumes port A data: its only read of $2800 is the flag-clearing dummy read before it tests the Advance interrupt flag (excerpt rom-dip-reads). The booklet does every adjustment, audit clear and factory restore in software and never mentions the CPU-board DIP switches.",
	)
_D_LABELS = {0: "D1 Clear Audits", 1: "D2 Reset Defaults", 2: "D3 Auto-Cycle Mode"}
for _bit in range(8):
	DIPS[17 + _bit] = (
		f"CPU Board Data Bank D{_bit + 1}",
		"unused",
		f"PinMAME's {_D_LABELS.get(_bit, f'D{_bit + 1}')} (bank 2 bit {_bit}), returned by s7_dips_r only while Master Command Enter (-3) is held. The label is PinMAME's generic System 7 name; on Black Knight the ROM never consumes port A data (excerpt rom-dip-reads), and the booklet clears audits (35), restores factory settings (45) and starts auto-cycle (15) as software functions at Function 50.",
	)

# --- Solenoids. Table 4 of the booklet with the playfield solenoid sheet's coil designators. Each
# driver transistor is given for the earlier D-7997 and the later D-8341 driver board (Table 4 note 1).
SOLENOIDS: dict[int, dict[str, Any]] = {
	1: dict(label="Ball Release", kind="coil", q=("Q15", "Q7"), wire="GRY-BRN", conn="2P11-4, 8P3-1, 8J6-1", part="SA-23-850-DC", coil="8L1", diode="8D129", place=("drawing", "outhole"), note="The outhole kicker: it kicks a drained ball from the outhole (switch 20) up onto the ball ramp. The retained table binds it to bsTrough.SolIn, and the gameplay harness run shows the ROM pulsing it while switch 20 is closed. Figure 2 puts callout 01 under the apron at the outhole."),
	2: dict(label="Lower Left 3-Bank Drop Target Reset", kind="coil", q=("Q17", "Q8"), wire="GRY-RED", conn="2P11-5, 8P3-2, 8J6-2", part="SA3-23-850-DC", coil="8L2", diode="8D130", bank="lower left", place=("obj", "sw26")),
	3: dict(label="Lower Right 3-Bank Drop Target Reset", kind="coil", q=("Q19", "Q9"), wire="GRY-ORN", conn="2P11-7, 8P3-3, 8J6-3", part="SA3-23-850-DC", coil="8L3", diode="8D131", bank="lower right", place=("obj", "sw30")),
	4: dict(label="Upper Left 3-Bank Drop Target Reset", kind="coil", q=("Q21", "Q10"), wire="GRY-YEL", conn="2P11-8, 8P3-4, 8J3-4", part="SA3-23-750-DC", coil="8L4", diode="8D132", bank="top left", place=("obj", "sw34")),
	5: dict(label="Upper Right 3-Bank Drop Target Reset", kind="coil", q=("Q23", "Q11"), wire="GRY-GRN", conn="2P11-9, 8P3-5, 8J3-5", part="SA3-23-750-DC", coil="8L5", diode="8D133", bank="top right", place=("obj", "sw38")),
	6: dict(label="Ball Ramp Thrower", kind="coil", q=("Q25", "Q14"), wire="GRY-BLU", conn="2P11-3, 8P3-6, 8J6-4", part="SG-23-750-DC", coil="8L6", diode="8D134", place=("obj", "BallRelease"), note="It throws the ball at the exit end of the ball ramp (switch 17) into the shooter lane. The retained table binds it to bsTrough.SolOut, whose exit kicker BallRelease is the placement; the gameplay harness run shows it throwing at game start and each time a ball is locked."),
	7: dict(label="Multi-Ball Release", kind="coil", q=("Q27", "Q15"), wire="GRY-VIO", conn="2P11-2, 8P3-7, 8J3-7", part="SG-23-750-DC", coil="8L7", diode="8D135", place=("obj", "LockOut"), note="Printed 8L7 \"MULTIBALL\" RELEASE on the playfield sheet. It releases the balls held in the lockup trough on the upper playfield. The retained table binds it to bsLock.SolOut, which kicks from its LockOut kicker, the placement; the multiball harness run shows it pulsed with all three lockup switches still closed once the third ball is locked."),
	8: dict(label="Lower Eject Hole", kind="coil", q=("Q29", "Q16"), wire="GRY-BLK", conn="2P11-1, 8P3-8, 8J6-5", part="SG-23-750-DC", coil="8L8", diode="8D136", place=("obj", "sw24"), note="Kicks the ball out of the lower playfield eject hole (switch 24); the retained table binds it to its bsSaucer on sw24 and the gameplay harness run shows it pulsed while switch 24 is closed."),
	9: dict(label="Right Magnet Relay", kind="relay", q=("Q31", "Q13"), wire="BRN-BLK", conn="2P9-9, 8P3-9, 8J6-6", part="SM-35-4000-DC", magnet=("right", "8L9", "8D137", "8R7", "8L28", "8F1", "8D156", "24", "GRY"), place=("obj", "MagnetR")),
	10: dict(label="Left Magnet Relay", kind="relay", q=("Q33", "Q12"), wire="BRN-RED", conn="2P9-7, 8P3-10, 8J6-7", part="SM-35-4000-DC", magnet=("left", "8L10", "8D138", "8R8", "8L29", "8F2", "8D157", "23", "BLU"), place=("obj", "MagnetL")),
	11: dict(label="Special Relay (General Illumination)", kind="relay", q=("Q35", "Q17"), wire="BRN-ORN", conn="2P9-1, 3P7-1 (power supply board)", part="SA-24-750-DC", gi=True),
	12: dict(label="Not Used", kind="coil", q=("Q37", "Q18"), wire="BRN-YEL", conn="2P9-2, 8P3-12", unused="Table 4 prints row 12 Not Used with no part number, and the playfield solenoid sheet ends 8J3-12 at N.C."),
	13: dict(label="Not Used", kind="coil", q=("Q39", "Q19"), wire="BRN-GRN", conn="2P9-3, 8P3-13", unused="Table 4 prints row 13 Not Used with no part number, and the playfield solenoid sheet ends 8J3-13 at N.C."),
	14: dict(label="Not Used", kind="coil", q=("Q41", "Q20"), wire="BRN-BLU", conn="2P9-4, 7P1", unused="Table 4 prints row 14 Not Used with no part number, and the cabinet sheet ends the BRN-BLU SOL. 14 (Q41) line at NC (its 7P1 pin is printed 3, the same number as the +28V wire, a misprint)."),
	15: dict(label="Bell", kind="coil", q=("Q43", "Q21"), wire="BRN-VIO", conn="2P9-5, 7P1-17", part="SM29-1000-DC", coil="7L15", diode="7D15", cabinet="cabinet.bell", note="7L15 BELL in the cabinet, with diode 7D15, powered from the +28V line on 7P1-3."),
	16: dict(label="Coin Lockout", kind="coil", q=("Q45", "Q22"), wire="BRN-GRY", conn="2P9-6, 7P1-18, 7P2-4", part="SM-35-4000-DC", coil="7L16", diode="7D10", cabinet="cabinet.coin-lockout", note="7L16 COIN LOCKOUT on the coin door (7P2-4). The cabinet sheet prints its diode 7D10, the same designator as the left magnet button's diode. The ROM energizes it from power-up while credits are below the maximum (harness), and the booklet: coin lockout de-energizes until remaining credits are below maximum."),
	17: dict(label="Left Kicker", kind="coil", q=("Q2", "Q1"), wire="BLU-BRN", conn="2P12-7, 8P3-17, 8J6-8", part="SG-23-850-DC", coil="8L17", diode="8D145", place=("obj", "LeftSlingshot"), special=("8SW65", "ORN-BRN", "2P13-5, 8P3-24, 8J6-10", "8P3-5", 21)),
	18: dict(label="Right Kicker", kind="coil", q=("Q4", "Q5"), wire="BLU-RED", conn="2P12-4, 8P3-18, 8J6-9", part="SG-23-850-DC", coil="8L18", diode="8D146", place=("obj", "RightSlingshot"), special=("8SW66", "ORN-RED", "2P13-3, 8P3-25, 8J6-11", "8P3-6", 22)),
	19: dict(label="Jet Bumper", kind="coil", q=("Q6", "Q4"), wire="BLU-ORN", conn="2P12-3, 8P3-19, 8J3-19", part="SG-23-850-DC", coil="8L19", diode="8D147", place=("obj", "Bumper1"), special=("8SW67", "ORN-BLK", "2P13-2, 8P3-26", "8P3-7", 36)),
	20: dict(label="Not Used", kind="coil", q=("Q8", "Q6"), wire="BLU-YEL", conn="2P12-6, 8P3-20", unused="Table 4 prints row 20 Not Used, and the playfield solenoid sheet ends 8J3-20 and the matching special-switch pin 8J3-27 at N.C."),
	21: dict(label="Not Used", kind="coil", q=("Q10", "Q2"), wire="BLU-GRN", conn="2P12-8, 8P3-21", unused="Table 4 prints row 21 Not Used, and the playfield solenoid sheet ends 8J3-21 and the matching special-switch pin 8J3-28 at N.C."),
	22: dict(label="Not Used", kind="coil", q=("Q12", "Q3"), wire="BLU-BLK", conn="2P12-9, 8P3-22", unused="Table 4 prints row 22 Not Used, and the playfield solenoid sheet ends 8J3-22 and the matching special-switch pin 8J3-29 at N.C."),
}
# Special-solenoid slots 6 and 7 (PIA 0 CB2 and CA2) publish 23 and 24.
EXTRA_SPECIAL_SOLENOIDS = {
	23: "PinMAME's System 7 special-solenoid slot 6 (PIA 0 CB2, setSSSol). The ROM's own solenoid test pulses it as step 23 (harness), as the booklet says (solenoids 01 thru 24 are pulsed). No load is fitted: Table 4 and the solenoid chart end at 22, the driver board's special-solenoid section takes only the six special triggers ST1-ST6 (driver board logic diagram), and no wiring sheet of this game carries a 23. The test sweep is the only state the ROM publishes here.",
	24: "PinMAME's System 7 special-solenoid slot 7 (PIA 0 CA2, setSSSol). The ROM's own solenoid test pulses it as step 24 (harness). No load is fitted: Table 4 and the solenoid chart end at 22, the driver board's special-solenoid section takes only ST1-ST6, and no wiring sheet of this game carries a 24. The test sweep is the only state the ROM publishes here.",
}

# --- Lamps. The lamp matrix with the playfield lamp sheet's bulbs and the master display's
# backbox bulbs.
LAMP_COLUMNS = {
	1: ("YEL-BRN", "2J5-8", "9P1-7 (master display)"),
	2: ("YEL-RED", "2J5-9", "8P2-4"),
	3: ("YEL-ORN", "2J5-6", "8P2-5"),
	4: ("YEL-BLK", "2J5-7", "8P2-6"),
	5: ("YEL-GRN", "2J5-3", "8P2-7"),
	6: ("YEL-BLU", "2J5-5", "8P2-8"),
	7: ("YEL-VIO", "2J5-1", "8P2-9"),
	8: ("YEL-GRY", "2J5-2", "8P2-10"),
}
LAMP_ROWS = {
	1: ("RED-BRN", "2J7-1", 11, 8),
	2: ("RED-BLK", "2J7-2", 12, 9),
	3: ("RED-ORN", "2J7-3", 13, 10),
	4: ("RED-YEL", "2J7-4", 14, 11),
	5: ("RED-GRN", "2J7-5", 15, 12),
	6: ("RED-BLU", "2J7-6", 16, 13),
	7: ("RED-VIO", "2J7-9", 17, None),
	8: ("RED-GRY", "2J7-8", 18, 15),
}
# Backbox lamps on the master display board: label, printed legend.
BACKBOX_LAMPS = {
	1: ("Same Player Shoots Again (Backbox)", "SHOOT AGAIN"),
	2: ("Ball In Play", "BALL \"IN PLAY\""),
	3: ("Tilt", "TILT"),
	4: ("Game Over", "GAME OVER"),
	5: ("Match", "MATCH"),
	6: ("High Score To Date", "HIGH SCORE"),
	8: ("Bonus Ball Time", "BONUS BALL TIMER"),
}
LAMPS: dict[int, tuple[str, str]] = {
	9: ("Right Magna-Save", "Light038"),
	10: ("Left Magna-Save", "Light037"),
	11: ("Left Outlane", "Light030"),
	12: ("Right Outlane", "Light029"),
	13: ("Right Spinner", "Light033"),
	14: ("Ramp Rollunder", "Light039"),
	15: ("Right Inside Rollover", "Light028"),
	16: ("Left Inside Rollover", "Light031"),
	17: ("Bottom Left 3-Bank Lamp", "Light032"),
	18: ("Bottom Right 3-Bank Lamp", "Light036"),
	19: ("Top Left 3-Bank Lamp", "Light045"),
	20: ("Top Right 3-Bank Lamp", "Light043"),
	21: ("Center Lock Lamp", "Light050"),
	22: ("Turnaround Extra Ball When Lit", "Light034"),
	23: ("Turnaround Special", "Light035"),
	24: ("Lower Playfield Eject Hole", "Light022"),
	25: ("Bottom Left 3-Bank, Lower Arrow", "Light021"),
	26: ("Bottom Left 3-Bank, Center Arrow", "Light026"),
	27: ("Bottom Left 3-Bank, Upper Arrow", "Light027"),
	28: ("2X Scoring", "Light019"),
	29: ("Bottom Right 3-Bank, Right Arrow", "Light025"),
	30: ("Bottom Right 3-Bank, Center Arrow", "Light024"),
	31: ("Bottom Right 3-Bank, Left Arrow", "Light023"),
	32: ("3X Scoring", "Light020"),
	33: ("Top Left 3-Bank, Lower Arrow", "Light046"),
	34: ("Top Left 3-Bank, Center Arrow", "Light047"),
	35: ("Top Left 3-Bank, Upper Arrow", "Light048"),
	36: ("Jet Bumper", "l36"),
	37: ("Top Right 3-Bank, Lower Arrow", "Light040"),
	38: ("Top Right 3-Bank, Center Arrow", "Light041"),
	39: ("Top Right 3-Bank, Upper Arrow", "Light042"),
	40: ("Right Lock Lamp", "Light049"),
	41: ("Left Ramp Rollover Extra Ball When Lit", "Light044"),
	42: ("Left Lock Lamp", "Light051"),
	47: ("Same Player Shoots Again (Playfield)", "Light010"),
	48: ("\"1\" Bonus", "Light009"),
	49: ("\"2\" Bonus", "Light008"),
	50: ("\"3\" Bonus", "Light007"),
	51: ("\"4\" Bonus", "Light006"),
	52: ("\"5\" Bonus", "Light001"),
	53: ("\"6\" Bonus", "Light011"),
	54: ("\"7\" Bonus", "Light012"),
	55: ("\"8\" Bonus", "Light013"),
	56: ("\"9\" Bonus", "Light014"),
	57: ("\"10\" Bonus", "Light015"),
	58: ("\"20\" Bonus", "Light016"),
	59: ("\"30\" Bonus", "Light017"),
	60: ("\"40\" Bonus", "Light018"),
	61: ("2X", "Light002"),
	62: ("3X", "Light003"),
	63: ("4X", "Light004"),
	64: ("5X", "Light005"),
}
# Lamps the playfield lamp sheet shades as mounted on the upper playfield.
UPPER_PLAYFIELD_LAMPS = frozenset({19, 20, 21, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42})
LAMP_NOTES = {
	9: "Lit by completing a drop-target bank (the gameplay harness run: the lower left bank lights it); while lit, the right Magna-Save button energizes the right magnet relay, and the lamp flashes while the magnet is on.",
	10: "Lit by completing a drop-target bank while the right Magna-Save is already lit (the gameplay harness run: the lower right bank lights it); while lit, the left Magna-Save button energizes the left magnet relay.",
	13: "Printed RIGHT SPINNER in the lamp matrix and 13 Right Spinner in the bulb list, but the insert sits beside the spinner in the left orbit, which the switch matrix calls LEFT SPINNER. The booklet: making the right inside rollover flashes the spinner, which is presumably why the lamp carries the right-hand name.",
	36: "The jet bumper cap lamp on the upper playfield. The retained table binds two lights to TimerInterval 36: l36 in the bumper cap, which is the placement, and l7, a light at the apron's credit window that the table author evidently meant for lamp 7 (the older corpus script bound it with NFadeL 7, l7). The l7 TimerInterval is a table defect and is not a second bulb.",
	47: "Same Player Shoots Again on the playfield, at the foot of the bonus ladder; the backbox has its own Shoot Again lamp at 1.",
}
UNUSED_LAMPS = {
	7: "Printed CREDITS (PLAYFIELD) in the lamp matrix and 07 Credits (Playfield) in the playfield sheet's bulb list, but no bulb is fitted on either harness: the playfield lamp sheet prints lamp column 1 N.C. at 8J5, and the master display sheet, which carries the other column-1 lamps, draws rows 1-6 and 8 only, with no row 7, 9P1-14, 9D7 or 9B7. The ROM lights it whenever credits are posted (harness), a credit-lamp routine for a bulb this game does not have. The retained table's apron light l7 is bound to lamp 36, not 7.",
	43: "Printed NOT USED in the lamp matrix and 43 Not Used in the bulb list; the playfield lamp sheet draws no bulb or diode at this position. The ROM drives it only in the lamp test, which flashes every matrix position, and in light shows that sweep every lamp position, such as the Multi-Ball start (harness).",
	44: "Printed NOT USED in the lamp matrix and 44 Not Used in the bulb list; no bulb or diode is drawn. The ROM drives it only in the lamp test and in light shows that sweep every lamp position, such as the Multi-Ball start (harness).",
	45: "Printed NOT USED in the lamp matrix and 45 Not Used in the bulb list; no bulb or diode is drawn. The ROM drives it only in the lamp test and in light shows that sweep every lamp position, such as the Multi-Ball start (harness).",
	46: "Printed NOT USED in the lamp matrix and 46 Not Used in the bulb list; no bulb or diode is drawn. The ROM drives it only in the lamp test and in light shows that sweep every lamp position, such as the Multi-Ball start (harness).",
}

# --- Displays: s7_dispS7. (id, label, PinMAME index, display memory start, width)
DISPLAYS = [
	("display.player-1-score", "Player 1 score, seven digits", 2, 1, 7),
	("display.player-2-score", "Player 2 score, seven digits", 3, 9, 7),
	("display.player-3-score", "Player 3 score, seven digits", 0, 21, 7),
	("display.player-4-score", "Player 4 score, seven digits", 1, 29, 7),
	("display.ball-in-play-tens", "Ball in play / match display, tens digit (master display strobe 1)", 4, 0, 1),
	("display.ball-in-play-units", "Ball in play / match display, units digit (master display strobe 9)", 5, 8, 1),
	("display.credits-tens", "Credits display, tens digit (master display strobe 1)", 6, 20, 1),
	("display.credits-units", "Credits display, units digit (master display strobe 9)", 7, 28, 1),
]

DRIVER_IDS = ("bk_l4", "bk_l3", "bk_l2", "bk_f4")
DRIVER_NOTES = {
	"bk_l4": ("identical", "Williams production L-4 game ROMs (IC14, IC17, IC20, IC26) with sound ROM 12 and the English speech ROMs 4-7. This is the driver every harness run of this record uses except the two variant solenoid tests."),
	"bk_l3": ("identical", "Williams L-3: the IC14 and IC26 game ROMs differ from L-4, IC17 and IC20 and the sound and speech ROMs are the same. Same init data, display layout and inputs; its own harness solenoid test pulses public 1 to 24 in the same order as L-4 under the same displayed numbers."),
	"bk_l2": ("identical", "Williams Rev 2 game ROMs (IC14 and IC26) with the L-4 IC17, IC20, sound and speech ROMs, the set IPDB hosts as Game ROMset Rev 2. Same PinMAME init data and display layout as L-4. Its ROM is not in the operator's authorized ROM library, so no harness run of it is retained."),
	"bk_f4": ("identical", "The L-4 game and sound ROMs with French speech ROMs 4f-7f: only the speech content differs, on the same speech board. Its own harness solenoid test pulses public 1 to 24 in the same order as L-4."),
}


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def located(identifier: str, role: str, points: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(points, start=1):
		suffix = f".{index}" if len(points) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*source_refs)})
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def switch_id(address: int) -> str:
	if address in SWITCHES:
		return f"switch.{slug(SWITCHES[address]['label'])}"
	if address in OPTIONAL_SWITCHES:
		return f"switch.{slug(OPTIONAL_SWITCHES[address]['label'])}"
	return f"switch.not-used-{address}"


def solenoid_id(address: int) -> str:
	if address in SOLENOIDS and not SOLENOIDS[address].get("unused"):
		spec = SOLENOIDS[address]
		prefix = "relay" if spec["kind"] == "relay" else "coil"
		return f"{prefix}.{slug(spec['label'])}"
	return f"solenoid.not-used-{address}"


def lamp_id(address: int) -> str:
	if address in BACKBOX_LAMPS:
		return f"lamp.{slug(BACKBOX_LAMPS[address][0])}-{address}"
	if address in LAMPS:
		return f"lamp.{slug(LAMPS[address][0])}-{address}"
	return f"lamp.not-used-{address}"


def switch_wiring(address: int) -> dict[str, Any]:
	column = (address - 1) // 8 + 1
	row = (address - 1) % 8 + 1
	column_wire, column_driver, column_harness = SWITCH_COLUMNS[column]
	row_wire, row_driver, row_playfield = SWITCH_ROWS[row]
	if column == 1 and address in (4, 5, 6, 7, 8):
		drive = f"{column_driver}, 7P1-19, 7P2-6 (coin door)"
		ret = f"{row_driver}, 7P1-{20 + row}, 7P2-{4 + row} (coin door)"
		component = f"diode 7D{address}"
	elif address <= 10:
		drive = f"{column_driver}, {'7P1-19' if column == 1 else '7P1-20'}"
		ret = f"{row_driver}, 7P1-{20 + row}"
		component = f"diode 7D{address}"
	else:
		drive = f"{column_driver}, {column_harness}"
		ret = f"{row_driver}, 8P1-{row_playfield}"
		component = f"switch 8SW{address}, diode 8D{address}"
	return {
		"board": "Williams System 7 driver board",
		"drive_wire": column_wire,
		"drive_connection": drive,
		"return_wire": row_wire,
		"return_connection": ret,
		"return_component": f"{component}, column {column} row {row}",
	}


SWITCH_SOURCES = (MANUAL_SOURCE, HARNESS_SWITCH_SOURCE, CORE_SOURCE)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role, symbol, location, note) in DIAGNOSTIC_SWITCHES.items():
		items.append(
			{
				"id": f"switch.{slug(label)}",
				"label": label,
				"kind": "switch",
				"binding": {"group": "pinmame.input.switch", "device": address},
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"availability": "used",
				"normally_closed": False,
				"roles": [role],
				"physical": {
					"location": location,
					"switch_type": "button" if address != -6 else "other",
					"notes": f"{note} PinMAME constant {symbol}: a direct input in internal switch column 0, not a matrix position.",
				},
				"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE, HARNESS_SOLENOID_SOURCE),
				"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE),
			}
		)
	for address in range(1, 65):
		column = (address - 1) // 8 + 1
		row = (address - 1) % 8 + 1
		base = {
			"binding": {"group": "pinmame.input.switch", "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
		}
		if address in OPTIONAL_SWITCHES:
			spec = OPTIONAL_SWITCHES[address]
			targets = ", ".join(str(target) for target in spec["targets"])
			items.append(
				{
					"id": switch_id(address),
					"label": spec["label"],
					"kind": "switch",
					**base,
					"availability": "optional",
					"normally_closed": False,
					"physical": {
						"location": "upper playfield" if address == 40 else "playfield",
						"notes": (
							f"The vertical rebound switch behind the {spec['bank']} drop-target bank (targets {targets}). The switch matrix sheet prints this cell NOT USED STANDUP and the switch chart Not Used; the playfield switch sheet lists it in its legend as `{spec['label']} (10)` but draws no switch or diode, so the production harness carries none. "
							"IPDB records that three of the four drop-target slots on early playfields have a cutout for this switch and that some production games still had it, and quotes Steve Ritchie: the switch was removed because the bank timers reset the banks too often for it to be hit. The ROM still scans the position: its switch test reports this number when it closes (harness), and the legend scores it 10 points. "
							"A recreation of the documented production machine leaves it out; one that models an early machine fits it. The placement is a projection onto the bank's centre target, behind which the switch stood."
						),
					},
					"wiring": {
						"board": "Williams System 7 driver board",
						"drive_wire": SWITCH_COLUMNS[column][0],
						"drive_connection": f"{SWITCH_COLUMNS[column][1]}, {SWITCH_COLUMNS[column][2]}",
						"return_wire": SWITCH_ROWS[row][0],
						"return_connection": f"{SWITCH_ROWS[row][1]}, 8P1-{SWITCH_ROWS[row][2]}",
						"return_component": f"no switch or diode drawn on the playfield switch sheet, column {column} row {row}",
					},
					"provenance": provenance(MANUAL_SOURCE, HARNESS_SWITCH_SOURCE, IPDB_SOURCE, CORE_SOURCE),
					"spatial": located(switch_id(address), "sensor", [normalized(spec["obj"])], VPX_TABLE_SOURCE, MANUAL_SOURCE, IPDB_SOURCE),
				}
			)
			continue
		if address not in SWITCHES:
			items.append(
				{
					"id": switch_id(address),
					"label": f"Not Used (matrix column {column} row {row})",
					"kind": "switch",
					**base,
					"availability": "unused",
					"physical": {"notes": UNUSED_SWITCH_NOTE},
					"provenance": provenance(MANUAL_SOURCE, HARNESS_SWITCH_SOURCE),
					"spatial": not_applicable("unused", MANUAL_SOURCE, HARNESS_SWITCH_SOURCE),
				}
			)
			continue
		spec = SWITCHES[address]
		notes: list[str] = []
		physical: dict[str, Any] = {}
		refs: list[str] = list(SWITCH_SOURCES)
		if "cabinet" in spec:
			physical["location"] = spec["location"]
			notes.append(f"Cabinet switch {spec['cabinet']} on the cabinet wiring sheet, drawn as a normally open contact with its series diode.")
			if spec.get("door") or address <= 8:
				notes.append("It is an ordinary column-1 matrix position; with PinMAME's keyboard handling on, SWITCH_UPDATE(s7) overwrites column 1 from the S7_COMPORTS port every frame, and with it off, as under LibPinMAME, the consumer writes it directly.")
		else:
			physical["location"] = "upper playfield" if address in UPPER_PLAYFIELD_SWITCHES else ("below the apron" if spec.get("ramp") or address == 20 else "playfield")
			notes.append(f"Playfield switch 8SW{address} with series diode 8D{address} on the playfield switch sheet, drawn as a normally open contact.")
			if address in UPPER_PLAYFIELD_SWITCHES:
				notes.append("The switch sheet shades it as mounted on the upper playfield; its normalized position is the upper playfield's footprint seen from above, over the rear of the lower playfield.")
		if spec.get("type"):
			physical["switch_type"] = spec["type"]
		if spec.get("drop"):
			notes.append(f"One of the three drop targets of the {spec['drop']} 3-bank (1,000 points). A drop target stays down until its bank is reset, so the ROM sees its switch closed for as long as it is down: the gameplay harness run completes each bank only by holding all three switches closed, and the bank's reset coil fires as the third one closes.")
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if spec.get("ramp"):
			notes.append("One of the three ball-rest positions on the ball ramp below the apron: left 19, centre 18, right 17 at the exit end next to the shooter lane (Figure 3 draws the three numbers along a dashed outline under the apron). The retained table models the ramp as a three-ball cvpmBallStack (InitSw 20, 17, 18, 19) with no object per switch, so the placement is the booklet's registered callout. The A-8762 retrofit kit replaces the ball-ramp switches with microswitches.")
			refs += [VPX_SCRIPT_SOURCE, GEOMETRY_SOURCE, KIT_SOURCE, HARNESS_GAMEPLAY_SOURCE]
		if spec.get("lock"):
			notes.append("One of the three ball positions in the lockup trough on the upper playfield (bottom 41, centre 42, top 43); only one of them scores for each locked ball (5,000). The retained table models the lock as one cvpmBallStack (InitSw 0, 41, 42, 43) on its LockMech kicker, so the placement is the booklet's registered callout, which lands on the table's lock kickers. The A-8762 retrofit kit replaces these switches with microswitches; its wire colours (GRN-BLU with WHT-BRN, WHT-RED, WHT-ORN) identify them.")
			refs += [VPX_SCRIPT_SOURCE, GEOMETRY_SOURCE, KIT_SOURCE, HARNESS_MULTIBALL_SOURCE]
		if spec.get("kicker"):
			coil = spec["kicker"]
			notes.append(f"PinMAME uses this matrix address as the special switch for solenoid {coil} (sxx.ssSw): while the game-on enable is set, closing it publishes solenoid {coil}, which the switch-test and gameplay harness runs show.")
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if address in (9, 10):
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if address == 46:
			refs += [HARNESS_GAMEPLAY_SOURCE, GEOMETRY_SOURCE, VPX_SCRIPT_SOURCE]
		if address == 20:
			refs += [HARNESS_GAMEPLAY_SOURCE, GEOMETRY_SOURCE, VPX_SCRIPT_SOURCE]
		if address in (4, 3, 45):
			refs.append(HARNESS_GAMEPLAY_SOURCE)
		if "obj" in spec:
			refs.append(VPX_SCRIPT_SOURCE)
		if spec.get("note"):
			notes.append(spec["note"])
		physical["notes"] = " ".join(notes)
		device: dict[str, Any] = {
			"id": switch_id(address),
			"label": spec["label"],
			"kind": "switch",
			**base,
			"availability": "used",
			"normally_closed": False,
			"physical": physical,
			"wiring": switch_wiring(address),
		}
		if "role" in spec:
			device["roles"] = [spec["role"]]
			device["provenance"] = provenance(*refs)
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			device["provenance"] = provenance(*refs)
			if "obj" in spec:
				device["spatial"] = located(device["id"], "sensor", [normalized(spec["obj"])], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
			else:
				device["spatial"] = located(device["id"], "sensor", [DRAWING_POINTS[spec["drawing"]]], MANUAL_SOURCE, HANDBOOK_SOURCE, GEOMETRY_SOURCE, VPX_TABLE_SOURCE)
		items.append(device)
	for address in range(81, 89):
		base = {"binding": {"group": "pinmame.input.switch", "device": address}, "aliases": [{"namespace": "pinmame.switch", "value": str(address)}]}
		if address not in FLIPPER_COLUMN_USED:
			items.append(
				{
					"id": f"switch.flipper-column-{address}",
					"label": f"Unused emulator flipper-column position {address}",
					"kind": "virtual",
					**base,
					"availability": "unused",
					"physical": {"notes": "PinMAME's generic flipper column (internal column 11) published at 81-88. Black Knight's game data declares no FLIP_SWNO matrix switches, no FLIP_SOL and no FLIP_EOS bits, so only the lower-right (82) and lower-left (84) button bits mean anything; this position has no physical contact and nothing reads it."},
					"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE),
					"spatial": not_applicable("virtual", CONTROLLER_SOURCE, CORE_SOURCE),
				}
			)
			continue
		label, role = FLIPPER_COLUMN_USED[address]
		side = "right" if address == 82 else "left"
		button = "7SW72" if address == 82 else "7SW73"
		outputs = "45 and 46" if address == 82 else "47 and 48"
		coils = "8L25 (lower right) and 8L27 (upper right)" if address == 82 else "8L24 (lower left) and 8L26 (upper left)"
		note = (
			f"PinMAME's synthetic lower-{side} flipper button ({'CORE_SWLRFLIPBUTBIT' if address == 82 else 'CORE_SWLLFLIPBUTBIT'}). Black Knight's game data names no FLIP_SWNO matrix switch, so the ROM never reads this button; PinMAME only fabricates flipper outputs {outputs} from it while the game-on enable (solenoid 25) is set, which the gameplay harness run shows. "
			f"On the machine the cabinet button {button} is drawn as two contacts with a common: one switches the lower {side} flipper coil and the other the upper {side} flipper coil ({coils}), both returned to ground through the driver board's flipper relay Z1, which the game-on line pulls in. One button therefore works both {side} flippers. VPinMAME's S7.VBS maps its {side} flipper key to {'swLRFlip = 82' if address == 82 else 'swLLFlip = 84'}."
		)
		items.append(
			{
				"id": f"switch.{slug(label)}",
				"label": label,
				"kind": "virtual",
				**base,
				"availability": "used",
				"roles": [role],
				"physical": {"notes": note},
				"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE),
				"spatial": not_applicable("virtual", CONTROLLER_SOURCE, CORE_SOURCE),
			}
		)
	for address, (label, availability, note) in sorted(DIPS.items()):
		refs = [CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE]
		if availability == "unused":
			refs.append(ROM_SOURCE)
		items.append(
			{
				"id": f"dip.{slug(label)}",
				"label": label,
				"kind": "dip_switch",
				"binding": {"group": "pinmame.input.dip", "device": address},
				"aliases": [{"namespace": "pinmame.dip", "value": str(address)}],
				"availability": availability,
				"physical": {"location": "backbox, sound board" if address <= 2 else "backbox, CPU board", "switch_type": "dip", "notes": note},
				"provenance": provenance(*refs),
				"spatial": not_applicable("dip_switch", CONTROLLER_SOURCE, MANUAL_SOURCE),
			}
		)
	return items


def solenoid_wiring(address: int, spec: dict[str, Any]) -> dict[str, Any]:
	first, second = spec["q"]
	wiring: dict[str, Any] = {
		"board": "Williams System 7 driver board",
		"driver_transistor": f"{first} (D-7997 board) / {second} (D-8341 board)",
		"drive_wire": spec["wire"],
		"drive_connection": spec["conn"],
		"control_connection": f"driver {first} / {second} (Table 4 solenoid {address:02d})",
	}
	if spec.get("unused"):
		wiring["return_component"] = "no load: the harness wire ends N.C."
		return wiring
	if spec.get("gi"):
		wiring.update({"power_wire": "RED", "power_connection": "3P7-3 (from the solenoid supply)", "return_component": "relay K1 SPECIAL RELAY coil on the power supply board, diode across the coil"})
		return wiring
	if spec.get("cabinet"):
		wiring.update({"power_wire": "RED", "power_connection": "3P3-7, 7P1-3 (+28V)"})
	elif spec.get("magnet"):
		_side, _relay, _diode, resistor, _magnet, fuse, _magnet_diode, pin, colour = spec["magnet"]
		wiring.update({"power_wire": colour, "power_connection": f"flipper supply 3P3-{5 if pin == '24' else 4} to 8P2-{pin} and 8P5-{pin}, after fuse {fuse}, through resistor {resistor}"})
	else:
		wiring.update({"power_wire": "RED", "power_connection": "3P3-6, 8P3-36 (SOL. B+)"})
	if spec.get("magnet"):
		_side, relay, diode, resistor, magnet, fuse, magnet_diode, pin, colour = spec["magnet"]
		wiring["return_component"] = f"relay coil {relay} with diode {diode} and series resistor {resistor} 100 ohm 3 W; its contact grounds magnet {magnet} (diode {magnet_diode}), which is fed from the flipper supply on 8P5-{pin} ({colour}) through fuse {fuse} 8 A"
	else:
		wiring["return_component"] = f"coil {spec['coil']} with diode {spec['diode']}"
	if spec.get("special"):
		switch, wire, connection, _table4, _matrix = spec["special"]
		wiring["control_wire"] = wire
		wiring["control_connection"] = f"special switch {switch}, {connection}"
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	base_refs = (MANUAL_SOURCE, HARNESS_SOLENOID_SOURCE, CORE_SOURCE)
	for address in range(1, 25):
		base = {
			"binding": {"group": "pinmame.output.solenoid", "device": address},
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
		}
		if address in EXTRA_SPECIAL_SOLENOIDS:
			items.append(
				{
					"id": solenoid_id(address),
					"label": "Not Used",
					"kind": "coil",
					**base,
					"availability": "unused",
					"physical": {"notes": EXTRA_SPECIAL_SOLENOIDS[address]},
					"provenance": provenance(MANUAL_SOURCE, HARNESS_SOLENOID_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
					"spatial": not_applicable("unused", MANUAL_SOURCE),
				}
			)
			continue
		spec = SOLENOIDS[address]
		refs = list(base_refs)
		physical: dict[str, Any] = {}
		notes: list[str] = []
		if spec.get("unused"):
			items.append(
				{
					"id": solenoid_id(address),
					"label": "Not Used",
					"kind": "coil",
					**base,
					"availability": "unused",
					"physical": {"notes": f"{spec['unused']} The driver transistor is fitted and the ROM's solenoid test still pulses the address as one of its steps 01-24 (harness); nothing else drives it."},
					"wiring": solenoid_wiring(address, spec),
					"provenance": provenance(*refs),
					"spatial": not_applicable("unused", MANUAL_SOURCE),
				}
			)
			continue
		if spec.get("part"):
			physical["part_number"] = spec["part"]
		if spec.get("coil") and spec["kind"] == "coil":
			notes.append(f"Coil {spec['coil']} with diode {spec['diode']}.")
		if spec.get("bank"):
			refs.append(HARNESS_MULTIBALL_SOURCE)
			notes.append(f"Resets the {spec['bank']} 3-bank of drop targets. The ROM fires it at every ball start, at the start of Multi-Ball, and as soon as the bank is completed with all three switches closed (gameplay and multiball harness runs); the booklet adds that a bank is also reset when its associated lamp goes out before the bank is completed.")
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if spec.get("magnet"):
			side, relay, diode, resistor, magnet, fuse, magnet_diode, pin, colour = spec["magnet"]
			other = "LEFT" if side == "right" else "RIGHT"
			notes.append(
				f"The {side} Magna-Save. This driver pulls in relay {relay}, whose contact switches the {side} magnet {magnet} (Table 4 note 2: the contacts of solenoids 09 and 10 switch ground to the magnets, part no. 20-8991), which sits under the playfield below the lower {side} drop-target bank, under the round Magna-Save emblem in the playfield art, and holds a ball heading for the {side} outlane. "
				f"The placement is the retained table's invisible Magnet{side[0].upper()} trigger, which its cvpmMagnet uses. Figure 2 draws the magnet's dashed callout {address:02d} further inboard and higher (registered at about ({0.26 if side == 'left' else 0.66}, 0.51)), but IPDB's stripped-playfield photograph shows the emblem, and its under-playfield photograph the round magnet, near the {side} side where the table puts it, so the callout is a label placed in open space rather than the device. "
				f"The playfield solenoid sheet prints the relay coil's legend as {relay} {other} MAGNET RELAY, the opposite side, while its own contact symbol, also labelled {relay}, feeds {magnet} {side.upper()} MAGNET; Table 4, the solenoid chart, the retained script (cvpmMagnet Magnet{side[0].upper()} with .Solenoid = {address}) and the ROM (the {side} Magna-Save button fires this address) all put this driver on the {side} magnet, so the coil legend is a drafting error that changes no wiring. "
				f"The ROM energizes it for a few seconds when the {side} Magna-Save button is pressed with the {side} Magna-Save lamp lit (gameplay harness run). Relay part SM-35-4000-DC per Table 4."
			)
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE, IPDB_SOURCE]
		if spec.get("gi"):
			notes.append(
				"Table 4's Special Relay, footnoted `Special relay located on Power Supply Board (games with transformer in cabinet) or in backbox (games with transformer in backbox)`. The power wiring sheet draws it as K1 SPECIAL RELAY on the power supply board, its coil fed from DRIVER BOARD SOL.11 (Q35) on 3P7-1, and its contact in the 3P9-1 line that feeds the general-illumination outputs on 3P8. IPDB: early games had a stand-alone General Illumination relay on the backbox floor, later ones the relay on the D-8345 power supply board. "
				"Energizing it turns the general illumination off. The ROM holds it off in attract mode and play, energizes it when the ball is tilted and flickers it during the Multi-Ball light show and on each tilt warning (gameplay and multiball harness runs), and the retained script's SolGi callback turns its GI lights off while 11 is on. As drawn the coil pulls the contact blade away from its fixed terminal, a contact that opens when energized, which agrees."
			)
			refs += [HARNESS_GAMEPLAY_SOURCE, HARNESS_MULTIBALL_SOURCE, VPX_SCRIPT_SOURCE, IPDB_SOURCE]
			physical["location"] = "power supply board (cabinet or backbox)"
		if spec.get("special"):
			switch, _wire, connection, table4_pin, matrix = spec["special"]
			notes.append(
				f"Special solenoid, fired on the hardware by its own special switch {switch} through the driver board while the game-on enable is set. PinMAME also publishes it whenever matrix switch {matrix} closes while the enable is set (sxx.ssSw), which the switch-test and gameplay harness runs show; that is PinMAME's contract a consumer relies on, while on the machine switch {matrix} is the separate scoring contact on the same assembly. "
				f"Table 4's special-switch note prints the playfield pin as {table4_pin}; the playfield solenoid sheet draws the special-switch wire on {connection.split(', ')[1]}, and Table 4's numbering on 8P3 also disagrees with that sheet for the flipper rows, so the sheet's pin is used."
			)
			refs += [HARNESS_GAMEPLAY_SOURCE, HARNESS_SWITCH_SOURCE, VPX_SCRIPT_SOURCE]
		if spec.get("note"):
			notes.append(spec["note"])
		if address in (1, 6, 8):
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if address == 7:
			refs += [HARNESS_MULTIBALL_SOURCE, VPX_SCRIPT_SOURCE]
		if address == 1:
			refs += [GEOMETRY_SOURCE]
		if address in (15, 16):
			physical["location"] = "cabinet" if address == 15 else "coin door"
			refs += [HARNESS_GAMEPLAY_SOURCE]
		if address in (9, 10):
			physical["location"] = "under the playfield (relay and magnet, on the playfield harness)"
		physical["notes"] = " ".join(notes)
		device: dict[str, Any] = {
			"id": solenoid_id(address),
			"label": spec["label"],
			"kind": spec["kind"],
			**base,
			"availability": "used",
			"physical": physical,
			"wiring": solenoid_wiring(address, spec),
			"provenance": provenance(*refs),
		}
		if spec.get("cabinet"):
			device["roles"] = [spec["cabinet"]]
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif spec.get("gi"):
			device["roles"] = ["cabinet.general-illumination-relay"]
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			how, what = spec["place"]
			if how == "drawing":
				device["spatial"] = located(device["id"], "effect", [DRAWING_POINTS[what]], MANUAL_SOURCE, HANDBOOK_SOURCE, GEOMETRY_SOURCE, VPX_TABLE_SOURCE)
			elif spec.get("magnet"):
				device["spatial"] = located(device["id"], "effect", [normalized(what)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, IPDB_SOURCE, MANUAL_SOURCE)
			else:
				device["spatial"] = located(device["id"], "effect", [normalized(what)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
		items.append(device)
	items.append(
		{
			"id": "relay.game-on-flipper-enable",
			"label": "Game On (Flipper Relay and Special Solenoid Enable)",
			"kind": "relay",
			"binding": {"group": "pinmame.output.solenoid", "device": 25},
			"aliases": [{"namespace": "pinmame.solenoid", "value": "25"}],
			"availability": "used",
			"roles": ["cabinet.flipper-enable-relay"],
			"physical": {
				"location": "backbox, driver board",
				"notes": "PinMAME's S7_GAMEONSOL: the PIA 1 CB2 game-on line (pia1cb2_w), published while the ROM enables play. On the driver board it pulls in the flipper relay Z1, whose contact grounds both flipper-button commons (2J12-1 ORN-VIO and 2J12-2 ORN-GRY, playfield solenoid sheet), and it gates the special solenoids. The booklet: Flipper relay is de-energized with subtest 25 of the solenoid test. The harness runs show it asserting on entering diagnostics and at game start, dropping on the tilting third playfield-tilt closure, and toggling at the solenoid test's step 25. The retained table binds vpmNudge.SolGameOn to SolCallback(23) instead, a table defect: 23 never carries the game-on state on System 7 (the table's S7.VBS declares GameOnSolenoid = 25).",
			},
			"wiring": {"board": "Williams System 7 driver board", "control_connection": "PIA 1 CB2 game-on line, relay Z1", "return_component": "relay Z1 contact to ground on 2J12-1/2J12-2"},
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE, HARNESS_SOLENOID_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE),
			"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
		}
	)
	for address, label, side, button in (
		(45, "Right Flipper Power (synthetic)", "right", 82),
		(46, "Right Flipper Hold (synthetic)", "right", 82),
		(47, "Left Flipper Power (synthetic)", "left", 84),
		(48, "Left Flipper Hold (synthetic)", "left", 84),
	):
		coils = "8L25 (lower, diode 8D153) and 8L27 (upper, diode 8D155)" if side == "right" else "8L24 (lower) and 8L26 (upper), both drawn with a diode printed 8D152"
		items.append(
			{
				"id": f"virtual.{slug(label)}",
				"label": label,
				"kind": "virtual",
				"binding": {"group": "pinmame.output.solenoid", "device": address},
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
				"availability": "used",
				"physical": {
					"notes": f"PinMAME fabricates this state from its synthetic {side}-flipper button (switch {button}) while the game-on enable (solenoid 25) is set, because no System 7 driver declares FLIP_SOL; both of the pair assert together (gameplay harness run). There is no driver-board output behind it. The two physical {side} flipper coils, {coils}, part SFL-19-400/30-750-DC, are switched directly by the cabinet button's two contacts through relay Z1, and each coil's end-of-stroke contact, drawn across part of its winding, drops the power winding out mechanically. A recreation drives both {side} flippers, lower and upper, from this pair.",
				},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_GAMEPLAY_SOURCE),
				"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
			}
		)
	return items


def lamp_wiring(address: int) -> dict[str, Any]:
	column = (address - 1) // 8 + 1
	row = (address - 1) % 8 + 1
	column_wire, column_driver, column_harness = LAMP_COLUMNS[column]
	row_wire, row_driver, row_playfield, row_display = LAMP_ROWS[row]
	if address in BACKBOX_LAMPS:
		drive = f"{column_driver}, {column_harness}"
		ret = f"{row_driver}, 9P1-{row_display} (master display)"
		component = f"bulb 9B{address} with diode 9D{address}"
	else:
		drive = f"{column_driver}, {column_harness}"
		ret = f"{row_driver}, 8P2-{row_playfield}"
		component = f"bulb 8B{address} with diode 8D{64 + address}"
	return {
		"board": "Williams System 7 driver board",
		"drive_wire": column_wire,
		"drive_connection": drive,
		"return_wire": row_wire,
		"return_connection": ret,
		"return_component": f"{component}, column {column} row {row}",
	}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		base = {"binding": {"group": "pinmame.output.lamp", "device": address}, "aliases": [{"namespace": "pinmame.lamp", "value": str(address)}]}
		column = (address - 1) // 8 + 1
		row = (address - 1) % 8 + 1
		if address in UNUSED_LAMPS:
			items.append(
				{
					"id": lamp_id(address),
					"label": f"Not Used (lamp matrix column {column} row {row})" if address != 7 else "Credits (Playfield) (Not Fitted)",
					"kind": "lamp",
					**base,
					"availability": "unused",
					"physical": {"notes": UNUSED_LAMPS[address]},
					"provenance": provenance(MANUAL_SOURCE, HARNESS_SOLENOID_SOURCE, HARNESS_GAMEPLAY_SOURCE, HARNESS_MULTIBALL_SOURCE),
					"spatial": not_applicable("unused", MANUAL_SOURCE),
				}
			)
			continue
		if address in BACKBOX_LAMPS:
			label, legend = BACKBOX_LAMPS[address]
			physical: dict[str, Any] = {"location": "backbox, master display board", "notes": f"Backbox lamp {legend} beside the master display (9P1, master display wiring sheet), not on the playfield."}
			if address == 1:
				physical["quantity"] = 2
				physical["notes"] += " The sheet draws 9B1 as two lamps in parallel under one designator."
			items.append(
				{
					"id": lamp_id(address),
					"label": label,
					"kind": "lamp",
					**base,
					"availability": "used",
					"roles": ["cabinet.backglass"],
					"physical": physical,
					"wiring": lamp_wiring(address),
					"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, HARNESS_GAMEPLAY_SOURCE),
					"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE),
				}
			)
			continue
		label, obj = LAMPS[address]
		physical = {"location": "upper playfield" if address in UPPER_PLAYFIELD_LAMPS else "playfield"}
		notes = []
		if address in UPPER_PLAYFIELD_LAMPS:
			notes.append("The playfield lamp sheet shades it as mounted on the upper playfield.")
		if address in LAMP_NOTES:
			notes.append(LAMP_NOTES[address])
		if notes:
			physical["notes"] = " ".join(notes)
		refs = [MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE]
		if address in (9, 10):
			refs.append(HARNESS_GAMEPLAY_SOURCE)
		items.append(
			{
				"id": lamp_id(address),
				"label": label,
				"kind": "lamp",
				**base,
				"availability": "used",
				"physical": physical,
				"wiring": lamp_wiring(address),
				"provenance": provenance(*refs),
				"spatial": located(lamp_id(address), "emitter", [normalized(obj)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
			}
		)
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": identifier,
			"label": label,
			"kind": "segment",
			"controller_index": index,
			"segment_start": start,
			"width": width,
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, HARNESS_DISPLAY_SOURCE, HARNESS_SOLENOID_SOURCE),
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		}
		for identifier, label, index, start, width in DISPLAYS
	]


def mechanisms() -> list[dict[str, Any]]:
	def m(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
		item: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
		item.update(extra)
		item["provenance"] = provenance(*refs)
		return item

	items = [
		m(
			"mech.outhole-and-ball-ramp",
			"Outhole, ball ramp and ball ramp thrower",
			"other",
			[solenoid_id(1), solenoid_id(6)],
			[switch_id(20), switch_id(19), switch_id(18), switch_id(17), switch_id(45)],
			"Black Knight holds its three balls on a ball ramp below the apron instead of a trough. A drained ball falls into the outhole (switch 20) below the apron centre; Ball Release (solenoid 1) kicks it up onto the ramp, where it rolls to the lowest free rest position: right (17) at the exit end next to the shooter lane, then centre (18), then left (19). Ball Ramp Thrower (solenoid 6) at the exit end throws the ball in position 17 into the shooter lane, where it rests on the Ballshooter Trough switch (45) until plunged, and the remaining balls roll down. The retained gameplay harness run shows the ROM throwing with 6 at game start with three balls on 17-19, pulsing 1 while switch 20 is closed and throwing again each time a ball is locked; the four-player run shows the next player's ball served (bank resets and a throw with 6) each time the kicked ball arrives back on the ramp. The booklet: three balls must rest on the ball ramp, the lockup or the shooter switches (at most one in the shooter trough) before a game will start. The retained table models the ramp as a three-ball cvpmBallStack (InitSw 20, 17, 18, 19) with SolIn on 1 and SolOut on 6.",
			(MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, HARNESS_MULTIBALL_SOURCE, HARNESS_DISPLAY_SOURCE, VPX_SCRIPT_SOURCE, KIT_SOURCE),
			positions=[
				{"id": "mech.outhole-and-ball-ramp.right", "label": "Right (exit end)", "sensors": [switch_id(17)]},
				{"id": "mech.outhole-and-ball-ramp.center", "label": "Centre", "sensors": [switch_id(18)]},
				{"id": "mech.outhole-and-ball-ramp.left", "label": "Left", "sensors": [switch_id(19)]},
			],
		),
		m(
			"mech.lockup-trough",
			"Lockup trough and Multi-Ball release",
			"kicker",
			[solenoid_id(7)],
			[switch_id(41), switch_id(42), switch_id(43)],
			"A ball lock on the upper playfield that holds up to three balls, resting on the bottom (41), centre (42) and top (43) switches; only one of them scores for each locked ball. Each time a ball comes to rest in it the ROM holds it and throws a new ball from the ball ramp (solenoid 6). With three balls locked, or when the lit lower playfield eject hole is made, the ROM starts Multi-Ball and pulses the Multi-Ball Release (solenoid 7) to kick the balls out; the multiball harness run shows the first pulse while all three switches are still closed and a second one after they open. The booklet: making a ball in the lock while a lock arrow is flashing lights that arrow steadily and lights the lower playfield eject hole; the lock arrows (lamps 21, 40, 42) do not flash until the turnaround is made, a rule the booklet marks as adjustable. At the factory settings the gameplay harness run flashes all three lock arrows from game start, before the turnaround (23) is ever made. With locked balls on the last ball, the outside rollovers are lit for a Last Chance release. The retained table models it as a cvpmBallStack (InitSw 0, 41, 42, 43) kicking from its LockOut kicker.",
			(MANUAL_SOURCE, HARNESS_MULTIBALL_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE, KIT_SOURCE),
			positions=[
				{"id": "mech.lockup-trough.bottom", "label": "Bottom", "sensors": [switch_id(41)]},
				{"id": "mech.lockup-trough.center", "label": "Centre", "sensors": [switch_id(42)]},
				{"id": "mech.lockup-trough.top", "label": "Top", "sensors": [switch_id(43)]},
			],
		),
		m("mech.lower-playfield-eject-hole", "Lower playfield eject hole", "kicker", [solenoid_id(8)], [switch_id(24)], "A kick-out hole in the middle of the lower playfield. While switch 24 is closed the ROM kicks the ball out with solenoid 8 (gameplay harness run). When it is lit (lamp 24) after a ball has been locked, making it releases the locked balls for Multi-Ball (booklet).", (MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)),
	]
	for coil, switches, label, optional in (
		(2, (25, 26, 27), "Lower left 3-bank drop targets", 28),
		(3, (29, 30, 31), "Lower right 3-bank drop targets", 32),
		(4, (33, 34, 35), "Top left 3-bank drop targets", None),
		(5, (37, 38, 39), "Top right 3-bank drop targets", 40),
	):
		where = "on the upper playfield" if coil in (4, 5) else "on the lower playfield"
		rebound = f" Early playfields also carried a vertical rebound switch ({optional}) behind the bank; see that switch." if optional else " This bank never had a rebound switch: its matrix position 36 is the jet bumper."
		sensors = [switch_id(address) for address in switches] + ([switch_id(optional)] if optional else [])
		items.append(
			m(
				f"mech.{slug(label)}",
				label,
				"drop_target_bank",
				[solenoid_id(coil)],
				sensors,
				f"A bank of three drop targets {where} ({', '.join(str(a) for a in switches)}), reset by solenoid {coil}. The ROM resets every bank at ball start and at the start of Multi-Ball, and resets a bank as soon as all three of its switches are closed (gameplay harness run); its bank lamp lights after the first target and flashes for a limited time, and if the lamp goes out before the bank is completed the bank is reset (booklet). Completing a bank lights one of its three target arrows and lights a Magna-Save (right first, then left: the gameplay harness run lights lamp 9 on the first completed bank and lamp 10 on the second); spotting arrows lights the extra-ball lamps.{rebound}",
				(MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, HARNESS_MULTIBALL_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	for coil, switch, label in ((17, 21, "Left kicker (slingshot)"), (18, 22, "Right kicker (slingshot)"), (19, 36, "Jet bumper")):
		special = SOLENOIDS[coil]["special"][0]
		items.append(
			m(
				f"mech.{slug(label)}",
				label,
				"kicker" if coil != 19 else "other",
				[solenoid_id(coil)],
				[switch_id(switch)],
				f"Fired directly by its own special switch {special} through the driver board's special-solenoid circuit while the game-on enable is set; matrix switch {switch} is the separate scoring contact. PinMAME publishes solenoid {coil} whenever switch {switch} closes during play, which the switch-test and gameplay harness runs show." + (" The jet bumper sits on the upper playfield." if coil == 19 else ""),
				(MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, HARNESS_SWITCH_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	for coil, button, side in ((9, 9, "right"), (10, 10, "left")):
		items.append(
			m(
				f"mech.{side}-magna-save",
				f"{side.capitalize()} Magna-Save magnet",
				"other",
				[solenoid_id(coil)],
				[switch_id(button)],
				f"Magna-Save: a magnet under the playfield on the {side} side, below the lower {side} drop-target bank, switched by relay {SOLENOIDS[coil]['magnet'][1]} on driver {coil}. With the {side} Magna-Save lamp ({9 if side == 'right' else 10}) lit, pressing the {side} Magna-Save button on the side of the cabinet (switch {button}) makes the ROM energize the magnet for a few seconds, holding a ball that would otherwise drain down the {side} outlane; released, the ball tends to roll through the inside rollover, which then scores 10,000 and advances the bonus five times (booklet; gameplay harness run). During the bonus ball both magnet lamps are lit.",
				(MANUAL_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE, IPDB_SOURCE),
			)
		)
	for side, button, virtuals in (("right", 82, ("virtual.right-flipper-power-synthetic", "virtual.right-flipper-hold-synthetic")), ("left", 84, ("virtual.left-flipper-power-synthetic", "virtual.left-flipper-hold-synthetic"))):
		coils = "8L25 (lower) and 8L27 (upper)" if side == "right" else "8L24 (lower) and 8L26 (upper)"
		items.append(
			m(
				f"mech.{side}-flippers",
				f"{side.capitalize()} flippers, lower and upper",
				"other",
				list(virtuals),
				[f"switch.{side}-flipper-button"],
				f"Two {side} flippers, one on the lower playfield and one on the upper playfield, coils {coils} (SFL-19-400/30-750-DC), both switched by the one {side} cabinet button through its two contacts and relay Z1, and enabled only while the game-on enable (solenoid 25) is set. The ROM cannot read the buttons. In PinMAME the consumer drives synthetic button {button} and PinMAME fabricates outputs {'45 and 46' if side == 'right' else '47 and 48'}, which drive both {side} flippers together, as the retained table's flipper callbacks do.",
				(MANUAL_SOURCE, CORE_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	return items


def relationships() -> list[dict[str, Any]]:
	items = []
	for coil in (17, 18, 19):
		matrix = SOLENOIDS[coil]["special"][4]
		items.append({"id": f"relationship.scoring-switch-{matrix}-publishes-solenoid-{coil}", "kind": "direct", "source": switch_id(matrix), "destination": solenoid_id(coil), "provenance": provenance(CORE_SOURCE, HARNESS_GAMEPLAY_SOURCE, HARNESS_SWITCH_SOURCE)})
	for destination in ("virtual.right-flipper-power-synthetic", "virtual.right-flipper-hold-synthetic", "virtual.left-flipper-power-synthetic", "virtual.left-flipper-hold-synthetic"):
		items.append({"id": f"relationship.game-on-gates-{destination.split('.', 1)[1]}", "kind": "relay_gated", "source": "relay.game-on-flipper-enable", "destination": destination, "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE)})
	return items


EXCERPT_IMAGES: dict[str, tuple[str, str]] = {}


def excerpt(identifier: str, name: str, locator: str, transcribed_by: str = "curator, read from the rendered page") -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier,
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}",
		"sha256": EXCERPT_DIGESTS[name],
		"method": "manual",
		"transcribed_by": transcribed_by,
		"reviewed": True,
	}
	if name in EXCERPT_IMAGES:
		digest, derivation = EXCERPT_IMAGES[name]
		record.update({"image": f"evidence/excerpts/{MACHINE_ID}/{name.removesuffix('.md')}.webp", "image_sha256": digest, "image_derivation": derivation})
	return record


def harness_locator(name: str, description: str) -> str:
	run_sha, scenario, scenario_sha, init_sha, game = HARNESS_RUNS[name]
	init_scenario, init_scenario_sha = HARNESS_BOOT[game]
	return (
		f"LibPinMAME harness run of {game} with tools/run_pinmame_harness.py, library pinmame64.dll built from the pinned "
		f"PinMAME revision (SHA-256 {LIBRARY_SHA256}), ROM archive {game}.zip from the operator's authorized ROM corpus "
		f"(SHA-256 {ROM_SHA256[game]}, CRCs matching the pinned driver), in an isolated state directory, with direct public "
		f"switch writes only (PinMAME keyboard handling and the driver's built-in simulator off). Scenario "
		f"tools/harness-scenarios/system-7/{scenario} (SHA-256 {scenario_sha}). A first power-up from empty CMOS stops on the "
		f"game-identification screen, so the state directory was initialized by exactly one prior empty-NVRAM boot (scenario "
		f"{init_scenario}, SHA-256 {init_scenario_sha}; raw run SHA-256 {init_sha}). {description} The whole run directory is "
		f"pinned by external:pinmame-runtime-evidence/black-knight-1980.manifest.json ({RUNTIME_MANIFEST[0]} files, "
		f"{RUNTIME_MANIFEST[1]} bytes, manifest SHA-256 {RUNTIME_MANIFEST[2]}). No ROM bytes or NVRAM blobs are retained in this repository."
	)


def runtime_source(identifier: str, name: str, description: str) -> dict[str, Any]:
	return {
		"id": identifier,
		"kind": "runtime_scenario",
		"uri": f"external:pinmame-runtime-evidence/black-knight-1980/{name}",
		"revision": PINMAME_REVISION,
		"sha256": HARNESS_RUNS[name][0],
		"locator": harness_locator(name, description),
		"license": "NOASSERTION",
		"attribution": "pinmame-game-defs curation",
	}


def _extraction_summary() -> str:
	count, total, digest = EXTRACTION
	return f"{count} files, {total} bytes, manifest SHA-256 {digest}"


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the bk_l4 clone tree: bk_l4, bk_l3, bk_l2 and bk_f4",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/s7/full/bk.c: the four Black Knight drivers (CORE_GAMEDEF(bk,l4,...,s7_mS7S,0) and the CORE_CLONEDEF "
				"lines for bk_f4, bk_l3 and bk_l2), their S7_ROMSTART8088 ROM sets, and bkGameData = {GEN_S7, s7_dispS7, {0, ...}, "
				"&bkSimData, {{0}}, {0, {21, 22, 36, 0, 0, 0}}}: hw.flippers 0 (no FLIP_SWNO matrix switch, no FLIP_SOL), a zero "
				"inverted-switch mask, and special solenoids 17, 18 and 19 fired by switches 21, 22 and 36; its #define switch and "
				"solenoid names and the simulator tables are a keyboard simulator's guesses and are not used as evidence. "
				"src/wpc/s7games.c s7_dispS7 (DISP_SEG_7(1,0), DISP_SEG_7(1,1), DISP_SEG_7(0,0), DISP_SEG_7(0,1), DISP_SEG_BALLS(0,8), "
				"DISP_SEG_CREDIT(20,28)); src/wpc/core.h DISP_SEG_7/DISP_SEG_BALLS/DISP_SEG_CREDIT; src/wpc/s7.c and s7.h as in the "
				"System 7 controller profile; src/wpc/core.c core_updateSw and core_getSol; src/wpc/core.c layoutAlphanumericFrame "
				"(the extra 128x32 layout frame is a rendering aid, not a machine display)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/system-7.json",
			"revision": "repository",
			"locator": "Williams System 7 public address rules: sequential switch matrix 1-64, diagnostics -7 to -3, synthetic flipper buttons 81-88, DIP addressing bank * 8 + bit + 1, solenoids 1-24 with the game-on enable at 25, synthetic flipper outputs 45-48, lamps 1-64 and no GI channel",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/310/Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf",
			"original_filename": "Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-09T18:07:00Z",
			"locator": (
				"The English Black Knight game manual with paginated schematics, 70 pages, every schematic sheet marked 500, hosted by "
				"IPDB and retrieved live through an interactive browser; retained at external:pinmame-manuals/by-machine/williams.black-knight.1980/. "
				"PDF pages 6-19 are Instruction Booklet 16P-500-103 (December 1980): page 7 game operation, pages 8-10 bookkeeping and "
				"adjustments, pages 12-13 diagnostics, page 14 the lamp matrix, page 15 Figure 2 solenoid locations and chart, page 16 "
				"Table 4 solenoid connections, page 17 Figure 3 switch locations and chart, page 18 the switch matrix, page 19 auto-cycle "
				"and board self-tests. Page 26-28 CPU board logic, 32-34 driver board logic, 42 power wiring, 44 sound board assembly, "
				"53-55 master display, 65 cabinet wiring, 66 playfield lamp wiring, 67 playfield solenoid wiring, 68 playfield switch "
				"wiring, 69 the separate lamp and switch matrix sheet."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [
				excerpt("excerpt.black-knight.switch-matrix", "switch-matrix.md", "PDF page 69, Switch Matrix, all 64 cells, compared cell by cell with the booklet's own matrix on PDF page 18"),
				excerpt("excerpt.black-knight.lamp-matrix", "lamp-matrix.md", "PDF page 69, Lamp Matrix, all 64 cells, compared with the booklet's lamp matrix on PDF page 14"),
				excerpt("excerpt.black-knight.solenoid-connections", "solenoid-connections.md", "PDF page 16, Table 4. Solenoid Connections and its notes"),
				excerpt("excerpt.black-knight.solenoid-locations", "solenoid-locations.md", "PDF page 15, the Solenoid Test and Figure 2. Playfield Solenoid Locations and Solenoid Chart"),
				excerpt("excerpt.black-knight.switch-locations", "switch-locations.md", "PDF pages 16-17, the Switch Test and Figure 3. Playfield Switch Locations and Switch Chart, with the drawing's registration against the retained table", transcribed_by="curator, read from the rendered page and measured on the native-resolution handbook render"),
				excerpt("excerpt.black-knight.operation-and-diagnostics", "operation-and-diagnostics.md", "PDF pages 6-13 and 19: board requirements, game operation, speech, bookkeeping and adjustments, diagnostic procedures, auto-cycle and board self-tests", transcribed_by="curator, OCR text extracted then confirmed against the rendered page"),
				excerpt("excerpt.black-knight.playfield-solenoid-wiring", "playfield-solenoid-wiring.md", "PDF page 67, Playfield Solenoid Wiring Diagram"),
				excerpt("excerpt.black-knight.playfield-switch-wiring", "playfield-switch-wiring.md", "PDF page 68, Playfield Switch Wiring Diagram"),
				excerpt("excerpt.black-knight.playfield-lamp-wiring", "playfield-lamp-wiring.md", "PDF page 66, Playfield Lamp Wiring Diagram"),
				excerpt("excerpt.black-knight.cabinet-wiring", "cabinet-wiring.md", "PDF page 65, Cabinet Wiring Diagram"),
				excerpt("excerpt.black-knight.master-display-lamps", "master-display-lamps.md", "PDF pages 53-55, the master display foldout with the backbox lamps on 9P1"),
				excerpt("excerpt.black-knight.power-wiring", "power-wiring.md", "PDF page 42, Power Wiring Diagram, with the K1 special relay"),
			],
		},
		{
			"id": SCHEMATICS_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/310/Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf",
			"original_filename": "Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf",
			"sha256": SCHEMATICS_SHA256,
			"acquired_at": "2026-10-09T18:07:00Z",
			"locator": "21-page 300 dpi colour scan of the Black Knight schematic diagrams, with a previous owner's pen marks, hosted by IPDB. Used only as a cross-check of the wiring sheets in the manual (its pages 19-21 carry the cabinet, lamp, solenoid and switch wiring diagrams); where the two scans differ, the excerpts record it.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
		},
		{
			"id": HANDBOOK_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/310/Williams_1980_Black_Knight_Operators_Handbook.pdf",
			"original_filename": "Williams_1980_Black_Knight_Operators_Handbook.pdf",
			"sha256": HANDBOOK_SHA256,
			"acquired_at": "2026-10-09T18:07:00Z",
			"locator": "A second, 400 dpi 1-bit scan of Instruction Booklet 16P-500-103 (15 pages), listed on IPDB as Instruction Booklet. Its tables agree with the copy in the manual; its page 12 (Figure 3) and page 10 (Figure 2) are the sharper renders used to register the location drawings onto the table frame.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
		},
		{
			"id": KIT_SOURCE,
			"kind": "service_bulletin",
			"uri": "https://www.ipdb.org/files/310/bkmicroswitchkit.pdf",
			"original_filename": "bkmicroswitchkit.pdf",
			"sha256": KIT_SHA256,
			"acquired_at": "2026-10-09T18:07:00Z",
			"locator": "Williams A-8762 Retrofit Kit, BLACK KNIGHT Playfield, three pages: the kit replaces the locking mechanism and ball ramp switches with microswitches, and its wire colours identify the switches it replaces.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt("excerpt.black-knight.retrofit-kit-a-8762", "retrofit-kit-a-8762.md", "Page 1: heading, GENERAL, KIT COMPLEMENT and the upper and lower playfield switch-identification steps")],
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=310",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-09T18:08:00Z",
			"locator": (
				"IPDB machine 310: Black Knight, Williams Electronics, November 1980, model number 500, Williams System 7, 13,075 units, "
				"design Steve Ritchie, art Tony Ramunni, software Larry DeMar; notable features 'Flippers (4), Pop bumper (1), Slingshots (2), "
				"3-bank drop targets (4), Kick-out holes (2), Spinning target (1). Magna-Save on both inlanes. Split-level playfield with "
				"3 ramps.'; the early stand-alone General Illumination relay and the later D-8345 power board; the vertical rebound "
				"switches cut into three of the four drop-target slots and Steve Ritchie's note on their removal. Retrieved live through "
				"an interactive browser (retained page SHA-256 above). Photographs https://www.ipdb.org/images/310/image-40.jpg (Stripped Playfield, "
				"1200x2129, Brian Lee, SHA-256 27230f5f3e35cd656a27924d89e1edb25012de25c43552003588fdcc557eba5d) and "
				"https://www.ipdb.org/images/310/image-15.jpg (Under Playfield, 480x640, John Yates, SHA-256 "
				"047b26bf6153e84458e7987e656aa76429e0165b7be8555a92174c5c285d0b14), both acquired 2026-10-09, show the Magna-Save "
				"emblems and the two round magnets near the playfield sides; retained at "
				"external:pinmame-review-artifacts/black-knight-1980/ipdb-images/."
			),
			"license": "NOASSERTION",
			"attribution": "The Internet Pinball Database",
		},
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-roms/bk_l4.zip",
			"sha256": ROM_SHA256["bk_l4"],
			"locator": "Static reading of the bk_l4 program ROMs laid out as S7_ROMSTART8088 loads them: every extended-mode access to PIA 3 ($2800-$2803) and the one LDX #$2800. The only read of the DIP port's data is a discarded flag-clearing read; no code consumes the DIP banks. IC17, which holds that code, is the same chip in all four drivers.",
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
			"excerpts": [excerpt("excerpt.black-knight.rom-dip-reads", "rom-dip-reads.md", "The PIA 3 access table, the $FC6A routine and its callers", transcribed_by="curator, read from the ROM image")],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/black-knight-1980/source/Black Knight (Williams 1980).vpx",
			"original_filename": "Black Knight (Williams 1980).vpx",
			"sha256": TABLE_SHA256,
			"revision": "3.0",
			"locator": f"Community recreation by Bord, version 3.0, released November 2021 (built on new assets from Chris; VR by Uncle Paulie), from the operator's table archive. Exact playfield bounds {TABLE_BOUNDS}; normalized coordinates are x/952 and y/1974. Geometry authority for named objects. The upper playfield's objects share the lower playfield's x/y frame.",
			"license": "NOASSERTION",
			"attribution": "Bord",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"external:pinmame-vpx-sources/williams/black-knight-1980/extracted-vpxtool/{EXTRACTION_DIRECTORY}/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Embedded script of the retained table, 124,592 bytes, byte-identical to the pinned corpus copy. Const cGameName=\"bk_l4\" "
				"with S7.VBS and UseSolenoids=2. Runtime authority for: the SolCallback table (1 bsTrough.SolIn, 2-5 the drop-bank resets, "
				"6 bsTrough.SolOut, 7 bsLock.SolOut, 8 bsSaucer.SolOut, 11 SolGi, 15 the bell sound, sLRFlipper/sLLFlipper driving both "
				"flippers on each side); cvpmMagnet MagnetR and MagnetL on solenoids 9 and 10; the trough cvpmBallStack (InitSw 20, 17, "
				"18, 19), the lock (InitSw 0, 41, 42, 43) and the saucer on 24; the switch handlers 11-16, 21-27, 29-31, 33-39, 44, 45; the "
				"Magna-Save keys on switches 10 and 9; and InitLights, which binds each insert light to the lamp in its TimerInterval. "
				"Known defects not followed: SolCallback(23) = vpmNudge.SolGameOn (System 7 publishes game-on at 25); the apron light l7 "
				"carries TimerInterval 36 and lights with the jet bumper."
			),
			"license": "NOASSERTION",
			"attribution": "Bord",
			"rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/black-knight-1980/vpinmame-scripts/s7.vbs",
			"original_filename": "s7.vbs",
			"sha256": VPM_LIBRARY_SHA256,
			"acquired_at": "2026-10-09T18:07:00Z",
			"locator": (
				"The VPinMAME System 7 script library the retained table loads (script.vbs line 102: LoadVPM \"01560000\", \"S7.VBS\", 3.26), "
				"144 lines, header 'Last Updated in VBS v3.61, copied from the operator's Visual Pinball Scripts folder. Byte-identical to "
				f"scripts/s7.vbs in https://github.com/vpinball/vpinball at {VPM_LIBRARY_REVISION}. Its S7 Data constants name the game-on "
				"solenoid 25 and the flipper switches 82 (lower right) and 84 (lower left), which vpmKeyDown/vpmKeyUp set from the flipper keys."
			),
			"license": "NOASSERTION",
			"attribution": "VPinMAME / Visual Pinball script-library maintainers",
			"rights": "NOASSERTION",
			"excerpts": [excerpt("excerpt.black-knight.vpm-s7-library", "vpm-s7-library.md", "s7.vbs lines 20-38 and the flipper keys of vpmKeyDown", transcribed_by="curator, read from the installed library file")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/williams/black-knight-1980/extracted-vpxtool/{EXTRACTION_DIRECTORY}.manifest.json",
			"locator": f"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool/{EXTRACTION_DIRECTORY}: {_extraction_summary()}, produced with vpxtool git:v0.33.3 from the retained table. Bounds {TABLE_BOUNDS}.",
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{CORPUS_REVISION}/Black%20Knight%20%28Williams%201980%29/Black%20Knight%20%28Williams%201980%29.vbs.original",
			"revision": CORPUS_REVISION,
			"sha256": SCRIPT_SHA256,
			"locator": "Pinned corpus copy of the same table's original script (`Black Knight (Williams 1980).vbs.original`), byte-identical to the retained table's embedded script, which ties the retained table to the pinned known-working corpus.",
			"license": "NOASSERTION",
			"attribution": "Bord; pinned copy in jsm174/vpx-standalone-scripts",
		},
		{
			"id": GEOMETRY_SOURCE,
			"kind": "human_review",
			"uri": f"internal:evidence/excerpts/{MACHINE_ID}/switch-locations.md",
			"revision": "repository",
			"locator": "Registration of the booklet's Figure 3 onto the retained table frame on the 400 dpi handbook render: eighteen control points whose convex hull contains every reading, a least-squares affine fit with 9.4 table-unit RMS residual and 17.3 maximum leave-one-out error, and the derived two-decimal coordinates for the outhole, the three ball-ramp positions, the three lockup-trough positions and the playfield tilt; the curator recomputes the fit from the recorded controls and readings. The registered outhole lies 7.6 table units from the outhole tab of the playfield cut-out that the retained table's playfield image shows under the apron. The fit script is retained at external:pinmame-review-artifacts/black-knight-1980/figure3-registration-fit.py.",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		runtime_source(HARNESS_SOLENOID_SOURCE, "run-sol.json", "Diagnostics: Manual-Down plus Advance enters the display digits test; Auto-Up and Advance step Test 00 (sound), Test 01 (lamp test: all 64 lamp addresses flash) and Test 02, each shown in the credit displays (indexes 6 and 7). In Test 02 with Manual-Down each Advance moves one step: the ball-in-play displays (indexes 4 and 5) show 01 to 24 while the ROM pulses public solenoid 1 to 24 respectively, and step 25 toggles the game-on enable at 25. Public 25 asserts on entering diagnostics; 16 is energized from power-up."),
		runtime_source(HARNESS_SWITCH_SOURCE, "run-sw.json", "Test 03 (switch test): nothing is reported at rest; closing each public switch 1 to 46 alone makes the ball-in-play displays show that number, so every matrix switch reads 1 when closed and 0 open with no inversion, including 28, 32 and 40, which no production switch occupies; closing 47 to 64 is never reported. Closing 21, 22 and 36 also publishes 17, 18 and 19."),
		runtime_source(HARNESS_GAMEPLAY_SOURCE, "run-play.json", "With balls on 17, 18 and 19: a coin on 4 posts credits; the credit button (3) asserts 25, pulses 2-5 and throws with 6; 21, 22 and 36 publish 17, 18 and 19; the synthetic buttons 82 and 84 publish 45/46 and 47/48; each bank completed with its three switches held closed fires its reset (25-27 -> 2, 29-31 -> 3, 33-35 -> 4, 37-39 -> 5) and lights an arrow (25, 29, 33, 37) and a Magna-Save lamp (9, then 10); the left and right Magna-Save buttons (10, 9) then energize 10 and 9; closing 24 pulses 8; a ball on 41 is held and 6 throws a new one; a ball on 20 draws repeated pulses of 1; three playfield-tilt closures (46) pulse 11 twice and then hold 11, drop 25 and light the tilt lamp 3."),
		runtime_source(HARNESS_MULTIBALL_SOURCE, "run-mb.json", "After a game start, each ball locked on 41 and 42 is held and 6 throws a new ball; with the third ball on 43 the ROM pulses 2-5, energizes 11 and pulses the Multi-Ball release 7 while all three lockup switches are still closed, and pulses 7 and 11 again after the switches open."),
		runtime_source(HARNESS_DISPLAY_SOURCE, "run-4p.json", "Two coins and four presses of the credit button start a four-player game; each player's 10 points from switch 21 appears on PinMAME display index 2 (player 1), 3 (player 2), 0 (player 3) and 1 (player 4), the ball in play on indexes 4 and 5 and the credits on indexes 6 and 7."),
		runtime_source(HARNESS_L3_SOURCE, "run-sol-l3.json", "The solenoid-test scenario on the L-3 ROM: the same displayed step numbers 01 to 24 pulse public 1 to 24 and step 25 toggles 25."),
		runtime_source(HARNESS_F4_SOURCE, "run-sol-f4.json", "The solenoid-test scenario on the French-speech L-4 ROM: the same displayed step numbers 01 to 24 pulse public 1 to 24 and step 25 toggles 25."),
	]


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
	for driver_id in sorted(DRIVER_IDS):
		record = by_id[driver_id]
		item: dict[str, Any] = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_NOTES[driver_id]
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
			"name": "Black Knight",
			"manufacturer": "Williams",
			"year": 1980,
			"kind": "physical_pinball",
			"model_number": "500",
			"ipdb_id": 310,
			"opdb_id": "GrO7w-M9R03",
			"playfield": {"units": "vpx", "width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": STATUS,
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
				"display_inventory": "validated",
			},
		},
		"controller": {"platform": "pinmame.system-7", "hardware_generation": "0x10000", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Black Knight device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	resolved_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[dict[str, Any]]] = {}
	placement_count = 0
	for device in definition["inputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(binding)
		else:
			resolved_inputs.append(binding["address"])
			placement_count += len(spatial["placements"])
	resolved_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			resolved_outputs.append(binding)
	projections = []
	for address, spec in sorted(SWITCHES.items()):
		if "drawing" in spec:
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Registered from the booklet's Figure 3 ({spec['drawing']}); the retained table has no object for this switch. Two-decimal precision."})
		elif spec.get("obj") in ("LeftSlingshot", "RightSlingshot"):
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Drag-point centroid of the retained {spec['obj']} wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber."})
		elif spec.get("drop"):
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Drag-point centroid of the retained {spec['obj']} drop-target wall, the primary of this target in the script's DTArray."})
	for address, spec in sorted(OPTIONAL_SWITCHES.items()):
		projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Projected onto the {spec['bank']} bank's centre target ({spec['obj']}): the rebound switch stood in the playfield cutout behind the bank, and neither the table nor any drawing locates it more exactly."})
	projections += [
		{"group": "pinmame.output.solenoid", "address": 1, "reason": "Ball Release sits at the outhole below the apron; placed at the registered Figure 3 outhole, which Figure 2's callout 01 matches."},
		{"group": "pinmame.output.solenoid", "address": 6, "reason": "Ball Ramp Thrower sits at the exit end of the ball ramp below the apron; placed on the retained trough's exit kicker BallRelease, which throws into the shooter lane."},
		{"group": "pinmame.output.solenoid", "address": 7, "reason": "Multi-Ball Release placed on the retained lock's exit kicker LockOut, which the registered lockup-trough drawing confirms within 0.01."},
	]
	for address in (2, 3, 4, 5):
		projections.append({"group": "pinmame.output.solenoid", "address": address, "reason": f"Drop-target reset coil projected onto the bank's centre target ({SOLENOIDS[address]['place'][1]}); the coil sits under the bank."})
	for address in (9, 10):
		projections.append({"group": "pinmame.output.solenoid", "address": address, "reason": f"The relay switches a magnet; placed at the retained table's invisible magnet trigger {SOLENOIDS[address]['place'][1]}, which IPDB's stripped and under-playfield photographs corroborate. Figure 2's dashed callout sits further inboard and higher and is a label, not the device."})
	for address in (17, 18, 19):
		projections.append({"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto the retained {SOLENOIDS[address]['place'][1]} object the coil drives."})
	return {
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": f"validated and promoted to {AUTHOR_READY_PATH.relative_to(ROOT).as_posix()}" if STATUS == "author_ready" else "partial",
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifests": {EXTRACTION_DIRECTORY: {"file_count": EXTRACTION[0], "total_bytes": EXTRACTION[1], "manifest_sha256": EXTRACTION[2]}},
			"source_ref": VPX_EXTRACTION_SOURCE,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"manual_sha256": MANUAL_SHA256,
			"instruction_booklet_sha256": HANDBOOK_SHA256,
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(resolved_inputs),
		"resolved_output_bindings": sorted(resolved_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(bindings, key=lambda item: (item["group"], item["address"])) for reason, bindings in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=lambda item: (item["group"], item["address"])) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": projections,
		"excluded_object_classes": [
			"l7, an apron Light at the credit-window position whose TimerInterval is 36: it lights with the jet bumper, and lamp 7 has no bulb on the machine.",
			"Drain, the retained trough's entry kicker on the table's bottom edge; the outhole placement is the booklet's registered callout instead.",
			"LockMech, the lock's entry kicker, which carries all three lockup switches; the switches take the registered Figure 3 positions.",
			"sw25y-sw39y secondary drop-target walls and the psw primitives, animation parts of the drop-target system; the primary walls are used.",
			"GI_* lights and Light17 (TimerInterval 100), the table's general illumination, which has no controller address beyond relay 11.",
			"TriggerLF, TriggerRF and metaltrigger_*, physics and sound helpers with no switch.",
			"All backglass Light, Flasher, Reel and TextBox objects, which render the backbox and score displays.",
		],
		"unresolved": [],
		"visual_review_cache": [
			"external:pinmame-manuals/by-machine/williams.black-knight.1980/render/",
			"external:pinmame-review-artifacts/black-knight-1980/",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Black Knight (Williams, 1980) spatial audit",
		"",
		f"Status: {report['status']}.",
		"",
		f"The coordinate source is the retained `Black Knight (Williams 1980).vpx` 3.0 by Bord at SHA-256 `{TABLE_SHA256}`, bounds `{TABLE_BOUNDS}`, so every coordinate is x/952 and y/1974 rounded to at most six places. The lower flipper pivots land at y 0.829, the shooter-lane switch at 0.879 and the drain kicker at 0.986, which is the check that the y divisor is right. The upper playfield's objects share the same frame, so upper-playfield devices overlie the rear of the lower playfield in normalized space.",
		"",
		"## Evidence decisions",
		"",
		"- Switch, lamp and coil objects are the ones the retained script binds: switch handlers, the DTArray drop-target primaries, the cvpmBallStack and cvpmMagnet objects, and the insert lights InitLights binds by TimerInterval. Each was checked against the booklet's Figure 2 and Figure 3.",
		"- Eight hidden switches have no table object and take the booklet's Figure 3, registered onto the table frame, at two decimals: the outhole (20), the three ball-ramp positions (17, 18, 19), the three lockup-trough positions (41, 42, 43) and the playfield tilt (46). The fit uses eighteen control points with a 9.4 table-unit RMS residual, and every reading lies inside the controls' convex hull; the registered lockup switches land on the table's lock kickers, and the registered outhole lies 7.6 table units from the outhole tab of the playfield cut-out shown in the table's playfield image.",
		"- The three rebound standups 28, 32 and 40 are optional, fitted on early machines only; each is projected onto its bank's centre target.",
		"- The Magna-Save magnets (relays 9 and 10) take the table's invisible magnet triggers. Figure 2's dashed callouts lie further inboard and higher, but IPDB's stripped-playfield and under-playfield photographs show the emblems and the magnets near the sides, where the table puts them.",
		"- Lamp placements are the insert lights; every playfield lamp has exactly one bulb. Lamp 7 (Credits (Playfield)) and 43-46 have no bulb on the machine.",
		"- Backbox lamps 1-6 and 8, the bell (15), the coin lockout (16), the GI relay (11), the game-on relay (25), all cabinet and service switches, the DIPs and the displays take controlled not_applicable records.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		kind = entry["group"].rsplit(".", 1)[-1]
		lines.append(f"- {kind} {entry['address']}: {entry['reason']}")
	lines += ["", "## Excluded object classes", ""]
	for entry in report["excluded_object_classes"]:
		lines.append(f"- {entry}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, bindings in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(bindings)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `external:pinmame-vpx-sources/williams/black-knight-1980/extracted-vpxtool/{EXTRACTION_DIRECTORY}.manifest.json`, SHA-256 `{EXTRACTION[2]}`, {EXTRACTION[0]} files, {EXTRACTION[1]} bytes.",
		"- Figure 3 registration fit `external:pinmame-review-artifacts/black-knight-1980/figure3-registration-fit.py`.",
		"- IPDB photographs `external:pinmame-review-artifacts/black-knight-1980/ipdb-images/`.",
		f"- Transcribed excerpts under `evidence/excerpts/{MACHINE_ID}/`.",
		"",
	]
	return "\n".join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_NOTE


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Black Knight retained directory is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def build_runtime_manifest(runtime_root: Path) -> dict[str, Any]:
	manifest = build_extraction_manifest(runtime_root / "black-knight-1980")
	manifest["format"] = "pinmame-runtime-evidence-manifest"
	return manifest


def manifest_identity(manifest: dict[str, Any]) -> tuple[int, int, str]:
	return (len(manifest["files"]), sum(int(item["size"]) for item in manifest["files"]), hashlib.sha256(canonical_bytes(manifest)).hexdigest())


def configured_root(variable: str, *, required: bool) -> Path | None:
	value = os.environ.get(variable)
	if not value:
		if required:
			raise RuntimeError(f"{variable} is required for this operation")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> None:
	manifest_path = source_root / EXTRACTION_ROOT / f"{EXTRACTION_DIRECTORY}.manifest.json"
	if not manifest_path.is_file():
		raise RuntimeError(f"Black Knight extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(source_root / EXTRACTION_ROOT / EXTRACTION_DIRECTORY)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError("Black Knight extraction manifest does not match the retained files")
	if manifest_identity(actual) != EXTRACTION:
		raise RuntimeError(f"Black Knight extraction identity mismatch: {manifest_identity(actual)}")


def write_manifests(source_root: Path, runtime_root: Path) -> None:
	manifest = build_extraction_manifest(source_root / EXTRACTION_ROOT / EXTRACTION_DIRECTORY)
	write_json(source_root / EXTRACTION_ROOT / f"{EXTRACTION_DIRECTORY}.manifest.json", manifest)
	print("extraction", manifest_identity(manifest))
	runtime = build_runtime_manifest(runtime_root)
	write_json(runtime_root / "black-knight-1980.manifest.json", runtime)
	print("runtime", manifest_identity(runtime))


KNOWLEDGE_NOTE = """# Black Knight (Williams, 1980) - recreation knowledge

Williams game number 500, November 1980, Williams System 7, four players, two- or three-ball
Multi-Ball, designed by Steve Ritchie with art by Tony Ramunni and software by Larry DeMar (IPDB
310). It is the first game with Magna-Save, the first solid-state game with a multi-level playfield
(an upper playfield over the rear of the lower one, with four flippers), and it introduced the
Bonus Ball. The physical release year comes from the instruction booklet (16P-500-103, December
1980) and IPDB; pinned PinMAME dates every driver 1980.

## Reading the driver declaration

Black Knight's game data lives in PinMAME's simulator file `src/wpc/sims/s7/full/bk.c`, not in
`s7games.c`: `bkGameData = {GEN_S7, s7_dispS7, {0, ...}, &bkSimData, {{0}}, {0, {21, 22, 36, 0, 0, 0}}}`.

- `hw.flippers` is 0: no `FLIP_SWNO` matrix switch and no `FLIP_SOL`. The ROM cannot read the
  flipper buttons; PinMAME only fabricates flipper outputs from its synthetic buttons.
- `{{0}}`: the inverted-switch mask is zero. Every public switch reads 1 closed and 0 open, which the
  ROM's own switch test confirms for every position it reports.
- `{21, 22, 36}`: the switches that fire special solenoids 17, 18 and 19.
- The file's `#define` names and simulator state table (for example `sOuthole 1`, `sBallRel 6`,
  `sKnocker 11`, `swRTrough 17`) are a keyboard simulator's working names and several are wrong for
  the machine: solenoid 1 is the outhole kicker called Ball Release, 6 is the Ball Ramp Thrower and
  11 is the GI relay, not a knocker. This record takes its names from the manual and the ROM.
- `bkSimData` enables PinMAME's built-in simulator only while PinMAME's own keyboard handling is on;
  under LibPinMAME, as in every retained harness run, it does nothing.

No System 7 controller profile existed before this curation; `controllers/pinmame/system-7.json` was
written for it from `s7.c`, `s7.h` and `s7games.c` and applies to every `GEN_S7` game.

## The controller contract a recreation drives

- Switches 1-64 are the sequential matrix, column-major: public = (column - 1) * 8 + row, exactly
  the number the switch matrix prints in each cell. Column 1 is the cabinet: plumb bob and ball roll
  tilts, credit button, three coin switches, slam tilt and high score reset. Column 2 rows 1 and 2
  are the right and left Magna-Save buttons on the cabinet sides (9, 10). The service buttons are
  the direct inputs -7 (Advance), -6 (Auto-Up/Manual-Down, 1 = Auto-Up), -5 (CPU diagnostic), -4
  (sound diagnostic) and -3 (Master Command Enter).
- Flippers are not CPU-driven. Drive PinMAME's synthetic buttons 82 (right) and 84 (left). While the
  game is on (public solenoid 25) PinMAME fabricates flipper states 45/46 from 82 and 47/48 from 84.
  Each cabinet button has two contacts and works both flippers on its side, lower and upper (coils
  8L25 and 8L27 right, 8L24 and 8L26 left, SFL-19-400/30-750-DC), through relay Z1 on the driver
  board, which the game-on line pulls in.
- Solenoids: 1-8 coils (ball release, the four drop-bank resets, ball ramp thrower, Multi-Ball
  release, lower eject hole), 9 and 10 the Magna-Save magnet relays, 11 the GI relay, 15 the bell,
  16 the coin lockout, 17-19 the special solenoids (left and right kicker, jet bumper), 25 the
  game-on enable. 12-14 and 20-24 have no load; the ROM's solenoid test still pulses 1 to 24.
- Lamps: public = (column - 1) * 8 + row. Column 1 rows 1-6 and 8 are the backbox lamps on the
  master display (Shoot Again, Ball In Play, Tilt, Game Over, Match, High Score, Bonus Ball Time);
  everything else from 9 to 64 is on the playfield except 43-46 (not used). Lamp 7 is printed
  Credits (Playfield) but no bulb is fitted: the playfield harness leaves lamp column 1 N.C. and the
  master display has no row 7. The ROM lights it whenever credits are posted.
- Displays: PinMAME's s7_dispS7 publishes eight entries. Index 2 is player 1 (memory start 1),
  index 3 player 2 (9), index 0 player 3 (21) and index 1 player 4 (29), all seven digits; indexes 4
  and 5 are the tens and units of the ball-in-play / match display (starts 0 and 8) and indexes 6
  and 7 those of the credit display (starts 20 and 28), the four digits of the master display. The
  four-player harness run shows each player's score on those indexes. PinMAME also publishes a
  128x32 rendering frame, which is not a display on the machine.
- General illumination is a 6.3 VAC supply routed through the K1 Special Relay on the power supply
  board (early games: a stand-alone GI relay on the backbox floor). Solenoid 11 energizes K1 and
  turns the GI off. The ROM keeps it off (GI on) in attract mode and play, energizes it when the
  ball is tilted, and flickers it on tilt warnings and during the Multi-Ball light show.
- DIP switches: 1 and 2 are DS1 on the sound board. The CPU board's two banks (9-24) are never read
  by the Black Knight ROM: its only read of the DIP port is a discarded flag-clearing read. All
  settings are software adjustments (Functions 13-41, reached with Advance and the credit button);
  Functions 42-49 are the factory audit totals.

## Special solenoids

The left kicker (17), right kicker (18) and jet bumper (19) are each fired directly by their own
special switch (8SW65, 8SW66, 8SW67) through the driver board while the game-on enable is set; the
CPU only sees the separate scoring contacts 21, 22 and 36. PinMAME publishes the special solenoid
whenever that matrix switch closes, which the switch-test and gameplay harness runs show. The ROM
can also fire special solenoid slots itself: its solenoid test pulses 17 to 24 as steps 17 to 24.
Slots 6 and 7 (public 23 and 24) have no driver on the Black Knight driver board.

## Mechanisms a table author has to build

- **Outhole and ball ramp.** No trough: the three balls rest on a ball ramp below the apron, with
  rest switches 19 (left), 18 (centre) and 17 (right, the exit end by the shooter lane). A drained
  ball falls into the outhole (20); Ball Release (1) kicks it onto the ramp. Ball Ramp Thrower (6)
  throws the ball at 17 into the shooter lane onto the Ballshooter Trough switch (45). A game starts
  only with all three balls on the ramp, the lockup or the shooter switch (at most one in the
  shooter lane).
- **Four drop-target 3-banks**: lower left (25-27, reset 2), lower right (29-31, reset 3), top left
  (33-35, reset 4) and top right (37-39, reset 5), the top two on the upper playfield. A drop target
  stays down, so the ROM sees its switch closed until the reset; it resets a bank the moment all
  three are down, at every ball start and at the start of Multi-Ball, and when the bank's timed lamp
  (17-20) runs out first (booklet). Completing a bank lights one of its three arrows and a
  Magna-Save, right (lamp 9) first, then left (lamp 10).
- **Magna-Save.** A magnet under each side of the lower playfield, below the lower drop banks,
  switched by relay 9 (right) or 10 (left). With its lamp lit, the Magna-Save button on that side of
  the cabinet (switch 9 right, 10 left) makes the ROM energize the magnet for a few seconds to catch
  a ball heading for the outlane; the inside rollovers then score 10,000. The playfield solenoid
  sheet prints the relay coils' legends with the sides swapped (8L9 LEFT MAGNET RELAY on solenoid 9),
  but its own contact labels, Table 4, the retained script and the ROM put 9 on the right magnet.
- **Lockup trough and Multi-Ball** on the upper playfield: three switches 41 (bottom), 42, 43 (top).
  Each locked ball is held and a new one thrown with 6. Three locked balls, or the lit lower
  playfield eject hole (24, solenoid 8), start Multi-Ball: the ROM pulses the Multi-Ball Release (7)
  with the balls still in the lock. The booklet marks as adjustable its rule that the lock arrows (21, 40,
  42) do not flash until the turnaround (23) is made; at the factory settings the gameplay harness
  run flashes them from game start, before 23 is made. Scoring is doubled with two balls in play and tripled with three.
- **Lower playfield eject hole** (24), kicked by 8.
- **One jet bumper** on the upper playfield and **two kickers** (slingshots), on special solenoids.
- **Spinner** in the left orbit (13), lit by the right inside rollover; **right ramp rollunder**
  (14, upper playfield) with the Mystery value lit by the left inside rollover; **left ramp
  rollover** (44, upper playfield) and the **turnaround** (23) for the extra balls; outlanes 11 and
  12, inlanes 15 and 16.
- **Rebound standups**: early playfields carried a vertical switch behind three of the drop banks
  (28, 32, 40). The manual prints them NOT USED and draws none; IPDB and Steve Ritchie record that
  they were removed in production. The ROM still scans them. They are optional devices here.
- **Bonus Ball**: with two or more players the highest scorer gets a timed bonus ball (lamp 8 in the
  backbox), with both magnets lit.

## Tilts

Ball roll tilt (2) tilts on its first closure; plumb bob (1) and playfield tilt (46) on the third
(adjustable). Each warning closure flickers the GI through relay 11. Slam tilt (7) returns the game
to game over.

## Driver variants

`bk_l4` (production L-4), `bk_l3` (L-3, different IC14 and IC26), `bk_l2` (the Rev 2 game ROMs IPDB
hosts) and `bk_f4` (L-4 with French speech). All run the same hardware with the same init data and
display layout; the L-3 and French-speech solenoid tests behave exactly like L-4. The `bk_l2` ROM is
not in the authorized ROM library, so it has no harness run.

## Running the ROM in LibPinMAME

A first power-up from empty CMOS stops on the game-identification screen. Power up once more with
the saved NVRAM and the game comes up in attract mode; every retained run initializes its state
directory with one empty-NVRAM boot first. The diagnostics are entered with Manual-Down (-6 = 0) and
Advance (-7); Auto-Up then steps Test 00 (sound), 01 (lamps), 02 (solenoids) and 03 (switches), each
shown in the credit display, and Manual-Down holds one solenoid step. Drive everything with direct
switch writes so the driver's simulator stays off. In gameplay, hold drop-target switches closed
until the reset fires, as real drop targets stay down; a momentary pulse never completes a bank.

## Retained table caveats

The retained known-working table (Bord, 3.0, November 2021) is faithful in layout and bindings. Its
defects:

1. `SolCallback(23) = "vpmNudge.SolGameOn"`: on System 7 the game-on state is 25 (the table's own
   S7.VBS says so), so the nudge handler never sees game-on. Gate on 25.
2. The apron light `l7` has TimerInterval 36 and lights with the jet bumper; lamp 7 has no bulb on
   the machine.
3. The ball ramp and the lock are modelled as ball stacks without per-switch objects, and the
   outhole as the trough's entry kicker; place those switches from Figure 3.

## Evidence

- The English manual with paginated schematics (IPDB) for every table, chart, location drawing and
  wiring sheet; the 400 dpi copy of the instruction booklet for the drawing registration; the
  colour schematic scan as a cross-check; the A-8762 retrofit kit sheet.
- IPDB 310 for identity, production history, the GI relay and the rebound switches, and its
  photographs for the magnet positions.
- Pinned PinMAME `97aa922b` for the System 7 contract and the Black Knight game data.
- The retained table and its byte-identical pinned corpus script for geometry and runtime bindings,
  and the S7.VBS library it loads.
- LibPinMAME harness runs: solenoid test (L-4, L-3, French L-4), switch test, gameplay causality,
  Multi-Ball, and the four-player display roles; and a static reading of the ROM's DIP-port access.
"""


def generate(root: Path = ROOT) -> Path:
	definition = build()
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), build_knowledge())
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		raise RuntimeError(f"stale Black Knight artifact under the other coverage directory: {stale}")
	definition = build()
	expected = canonical_bytes(definition)
	for path in (root / DEFINITION_PATH.relative_to(ROOT), root / SEED_PATH.relative_to(ROOT)):
		if not path.is_file() or path.read_bytes() != expected:
			raise RuntimeError(f"Black Knight artifact drifted from its deterministic curator: {path}")
	report = build_spatial_report(definition)
	if (root / SPATIAL_REPORT_PATH.relative_to(ROOT)).read_bytes() != canonical_bytes(report):
		raise RuntimeError("Black Knight spatial audit drifted from its deterministic curator")
	if (root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)).read_bytes() != render_spatial_report(report).encode("utf-8"):
		raise RuntimeError("Black Knight spatial review drifted from its deterministic curator")
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != build_knowledge().encode("utf-8"):
		raise RuntimeError("Black Knight knowledge note drifted from its deterministic curator")
	for name, digest in EXCERPT_DIGESTS.items():
		path = root / "evidence/excerpts" / MACHINE_ID / name
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
			raise RuntimeError(f"Black Knight excerpt drifted from its pinned digest: {path}")
	print("Black Knight definition, seed, spatial audit, knowledge note and excerpts match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, spatial audit and knowledge note")
	mode.add_argument("--write-manifests", action="store_true", help="Write the retained extraction and runtime-evidence manifests")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_manifests:
		source_root = configured_root("PINMAME_VPX_SOURCES_ROOT", required=True)
		runtime_root = configured_root("PINMAME_RUNTIME_EVIDENCE_ROOT", required=True)
		assert source_root is not None and runtime_root is not None
		write_manifests(source_root, runtime_root)
	elif args.verify_extraction:
		source_root = configured_root("PINMAME_VPX_SOURCES_ROOT", required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Black Knight retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
