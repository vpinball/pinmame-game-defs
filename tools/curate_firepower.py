"""Curate the physical Williams Firepower (1980) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is embedded as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed, the spatial
audit and the knowledge note.

Evidence priority actually applied here, in the runbook's order:

1. The retained known-working VPX script (3rdaxis, Slydog43 & G5K, 2018) for runtime callbacks,
   ball routing and lamp bindings, except where it is demonstrably defective.
2. The January 1980 instruction booklet 16P-497-103 and the March 1980 schematics for physical
   construction, wiring, quantities and device locations.
3. Pinned PinMAME source for the System 6 controller contract, the special-solenoid switch map and
   the display layouts.
4. The retained table's exact geometry for coordinates, reconciled against the booklet's location
   drawings; the drawing, registered onto the table frame, supplies coordinates only for devices the
   table does not model.
5. Hash-pinned LibPinMAME harness runs of the production ROM's own solenoid and switch tests and of
   gameplay sequences, which settle numbering, display roles and mechanism causality.
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
STATUS = "author_ready"
PARTIAL_PATH = ROOT / "machines/partial/williams/firepower-1980.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/firepower-1980.json"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/firepower-1980.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/firepower-1980.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/firepower-1980.md"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/firepower-1980.md"
# The five Oliver System 7 conversion drivers run on a System 7 CPU board, a different controller
# generation from the production machine's System 6 board, so they form one separate conversion
# record (the Kiss and Eight Ball Deluxe rule). It keeps the id of the old frpwr_a7 residual; the
# separate frpwr_d7 and frpwr_e7 residuals were merged into it and must not come back.
CONVERSION_ID = "williams-oliver.firepower.1980"
CONVERSION_PATH = ROOT / "machines/partial/williams-oliver/firepower-1980.json"
CONVERSION_KNOWLEDGE_PATH = ROOT / "knowledge/williams-oliver/firepower-1980.md"
RETIRED_ARTIFACTS = (
	ROOT / "machines/partial/williams-oliver/firepower-1980-frpwr_d7.json",
	ROOT / "machines/partial/williams-oliver/firepower-1980-frpwr_e7.json",
	ROOT / "knowledge/williams-oliver/firepower-1980-frpwr_d7.md",
	ROOT / "knowledge/williams-oliver/firepower-1980-frpwr_e7.md",
)

MACHINE_ID = "williams.firepower.1980"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-6"
BOOKLET_SOURCE = "manual.williams.firepower.1980.instruction-booklet"
BOOKLET_ALT_SOURCE = "manual.williams.firepower.1980.instruction-booklet-archive"
SCHEMATICS_SOURCE = "manual.williams.firepower.1980.schematics"
BULLETIN_SOURCE = "service-bulletin.williams.ss20"
PROTOTYPE_SOURCE = "human-review.firepower-drop-target-retrofit"
IPDB_SOURCE = "ipdb.856"
VPX_TABLE_SOURCE = "vpx-table.firepower-williams-1980-v1-0"
VPX_SCRIPT_SOURCE = "vpx-script.firepower-williams-1980-v1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.firepower-williams-1980-v1-0"
VPX_AI_TABLE_SOURCE = "vpx-table.firepower-vs-ai-v3-4-2"
VPX_AI_SCRIPT_SOURCE = "vpx-script.firepower-vs-ai-v3-4-2"
THAL_SCRIPT_SOURCE = "vpx-script.firepower-1-1-thal-mod"
GEOMETRY_SOURCE = "human-review.firepower-geometry-registration"
HARNESS_SOLENOID_SOURCE = "runtime.firepower.solenoid-test"
HARNESS_SWITCH_SOURCE = "runtime.firepower.switch-test"
HARNESS_GAMEPLAY_SOURCE = "runtime.firepower.gameplay-causality"
HARNESS_KICKER_SOURCE = "runtime.firepower.ball-saver-kicker"
HARNESS_SYS7_SOURCE = "runtime.firepower.sys7-conversion"
HARNESS_FLIPPER_SOURCE = "runtime.firepower.flipper-button-copy"
HARNESS_B6_SOURCE = "runtime.firepower.seven-digit-b6"
HARNESS_C6_SOURCE = "runtime.firepower.seven-digit-c6"

BOOKLET_SHA256 = "ed59481c2a4eeb89a130e7d42e1fa98ae6d8fe68022bbd12658d46a46a500f94"
BOOKLET_ALT_SHA256 = "5054f1c5f9f73ca8f95c3ed03566d7833280dcdccd04a865a84b465e2f14c5d6"
SCHEMATICS_SHA256 = "a3b403c78b5fc3560c9e2bce8401dbdc0493e2f5cd01a2ce90ce92373343e34b"
BULLETIN_SHA256 = "d4ababaebe289472b9fd4c65e9e1170e55190b9e7838e419b39efac3c6b8e397"
PROTOTYPE_SHA256 = "8d5f6647412a9db31c62dafabef53eb8590706a228249bb93731de336a60535c"
IPDB_PAGE_SHA256 = "b81dc9f4154ada558110aa700a7272ab905417d5c04cfa64c850dfa870efa6ea"
TABLE_SHA256 = "7786f7d073b6580e808acfb8aff60d1f30436f9d4d224b0ff57ca2ef899db179"
SCRIPT_SHA256 = "8d0ec27855bf80407a6efb54e28cf9fee476d2e8ec2d630a3c2016981f8e58dc"
AI_TABLE_SHA256 = "070c34356ef677d8d1f37079ef9a18de8f9fc6629bbbb15df660918cfebba19c"
AI_SCRIPT_SHA256 = "fa95a85f322ead59918f5004020ff5e662330baa5d3a317de636e45ec03cbefe"
THAL_SCRIPT_SHA256 = "485e36dda12e12bd371001e093cfb1280d3f657be96f55892fc2e155b83bf8d0"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
GEOMETRY_CANDIDATES_SHA256 = "0dbb74f4f0d508c3b6b772f62f3dec5fe1e052b259def1f8698b0791e934d85c"
GEOMETRY_AI_CANDIDATES_SHA256 = "7e646afe424fca7a04d0dde028cb71d9fe830c8af7ff08aac26504e18c2f3abc"
PRIMITIVE_BOUNDS_SHA256 = "0d4a67a9f99f6e04c67a56ff231eba434e855282a1d87e936920319f4b5c7fc1"
LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
ROM_L6_SHA256 = "09d60b4eb0f5180b4b36cd33d729c75bbba56c24189e0f518e1f520b3a894ab1"
ROM_B7_SHA256 = "4c862efdd027117bc4cfc088f759d887b811fa23d51b8cfa8541ed8a6e19c928"
ROM_B6_SHA256 = "c43d357fe1662360f8576e3107f8dd38965617683d3a63a501c81b2ec1ef6b10"
ROM_C6_SHA256 = "fe3b33c30078c964e0bd632d5f5152da68f2b628627fbe2722d64c7b6e5e2934"

# name: (run sha256, scenario file, scenario sha256, NVRAM-initialization run sha256)
HARNESS_RUNS = {
	"run-sol.json": ("aae363a502188fd45813adc6c1a094eef1ed26a700b91fa0da9d701db2049f74", "firepower-solenoid-test.json", "ae89585247ea3a3a590e3e0746bad2aeed960274a559d17c6e9dd2d36ed27bb7", "f5a4f91c67c4d27644e72fbebc445ac4cd48e9ebc35eaceecb5cb56306c35c07"),
	"run-sw.json": ("5653f72185c5d37975863fd6099f8957caa3cd6f1afe799145f564fa73a0e0c4", "firepower-switch-test.json", "94d6e78f2170b0a8e687c9625036944eaffaf96e1b6039699425abb9003f745f", "346d62e0e53d6ab0268e4b0946451bf09bc396ce5ebaebaae0afe7b0ca2ad5a4"),
	"run-play.json": ("d0bfae495c5362389195529569dad643f3707eb8bd88d36f03425e2672bcde25", "firepower-gameplay-causality.json", "49e8a4aa013b81d7a91d466ec2e0dc8a88e6a53a2a44f43a5425efe96a555bb5", "4437ba680f1e25baf147c1e4643fb00e357c13397ea9fe23aa131110b75ece85"),
	"run-kick.json": ("07ee402a33463e53a19c935857d28f4231f3f7f57a88dca2e462961c773efd28", "firepower-ball-saver-kicker.json", "a20206304edee1527f4cd5c535fe09a88e9eebaf1c461ca1081f5970debae113", "f8466589fb6254a10444d8e056694b7fff06461f2dfaaa55e6bffee9479293ff"),
	"run-b7.json": ("7422c2d8b6e4f511e3bb12be0a2c6109720e9d3b27a71669116ba0237205fea6", "firepower-sys7-conversion-gameplay.json", "3446b71166ea1731aaaa2be57aca3364b2abc9683176e45a6181b59e6ddff45b", "a00bdb89d102411abb8f5ec1496f34926691efdd01e3f69d531980f81b41adb0"),
	"run-flip.json": ("623f63b8c681458cb051ef3e8af2e717143f7024e022ff3a5cad16a9a4c5e107", "firepower-flipper-button-copy.json", "6037d5d7955703ecdda18f185b9bb52f368ab2ef7c4f1f4ab3e3d23a48a50b7f", "5523e3e88b11f061179f0c587f6786536b62734eb602716df14821c266fded22"),
	"run-b6.json": ("0222d9b1901915080854d21a730178628aab17554253f06c819891e4573098a6", "firepower-b6-seven-digit-gameplay.json", "244fd92fcd8b7a6ffd9b55dd489e3e382c4a74945f06e6d0a2cdb0c35f70a7ef", "c7ec82e0dd0859c37c9e46fb0befc282b48b58eb3ce93d511c4d20e6132fcb47"),
	"run-c6.json": ("e7851323a0f8c57d7421c21a06ed1c829873ffe9eaf1e8be734bdf496130345c", "firepower-c6-seven-digit-gameplay.json", "40f71e0a674f5807e530e2cb4c37b2718cda8b5cdd1ff7e1755586c5d67e881d", "9ffb5abf8c8c1aa66465a2b694ec713660d846733fc747a85aa5fdd54fab78db"),
}
# Canonical manifest of the whole external runtime-evidence directory (every raw run, every
# initialization run and each state directory's cfg and NVRAM), written with the same algorithm as
# the VPX extraction manifests: external:pinmame-runtime-evidence/firepower-1980.manifest.json.
RUNTIME_MANIFEST = (40, 5508646, "2af0fcd687c87a98813e5e4bfc6ebd22cd3730e7584ff81ff4ab8c1e621b42c6")
INIT_SCENARIO_SHA256 = "5ad5f8beadd1006f7b2b79d9cf0098a842e3454088f1ad25280928acc77a33eb"
SYS7_INIT_SCENARIO_SHA256 = "9e659cd6e73f66581642e059af4557c0c1d9b75ef3bd28e6159dfb5455adbb9a"
B6_INIT_SCENARIO_SHA256 = "9109981741ff8390cc8472a82c61c4447043fe86276e32be13e7ddaafdfde160"
C6_INIT_SCENARIO_SHA256 = "8cc913f27610af8d211db0d1117c8d384f47880ea65a10af63442948135e9420"
# game: (NVRAM-initialization scenario sha256, ROM archive sha256)
HARNESS_BOOT = {
	"frpwr_l6": (INIT_SCENARIO_SHA256, ROM_L6_SHA256),
	"frpwr_b6": (B6_INIT_SCENARIO_SHA256, ROM_B6_SHA256),
	"frpwr_c6": (C6_INIT_SCENARIO_SHA256, ROM_C6_SHA256),
	"frpwr_b7": (SYS7_INIT_SCENARIO_SHA256, ROM_B7_SHA256),
}

EXTRACTION_ROOT = Path("williams/firepower-1980/extracted-vpxtool")
EXTRACTIONS = {
	# relative directory: (file count, total bytes, manifest sha256)
	"firepower-williams-1980-v1.0": (1098, 252535142, "119ea4e367f16ae078fe76ac9dcd50f80f8b01192e4bd413b1dbb963f9c26c31"),
	"firepower-vs-ai-v3.4.2": (1065, 332893876, "cb8357b34e6ed744e9bae39f3845fd6477a1361925f5d8248f54936349252055"),
}

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

EXCERPT_DIGESTS = {
	"cabinet-wiring.md": "eb992cadd02f70759bfaa7015b7015a5e45dfa5b5177c63c566b491e636a2b93",
	"insert-board-wiring.md": "1854a809fcd94b215bcef3286ccf71934a9b9e0434f9be98e317d2baa24291d0",
	"lamp-matrix.md": "0b918775359d978fa25ce848553b08af69e210c1a216c5b73fe61519fea156d5",
	"operation-and-diagnostics.md": "2ff1b708daf01bfcfc372ac4d62f99899906aae2a9f5b9693481064b129d5dfb",
	"playfield-lamp-wiring.md": "e17d36a803a56a291382474f56f777a54a5644e7f0fbae50f34357d7cd7b642f",
	"playfield-solenoid-wiring.md": "d299073c37e84227fd9158b5fda1b215b6b3e1ea2b29065587a68113940f6a1a",
	"playfield-switch-wiring.md": "1b7d1e574d0acfa3e5791c52739e2665220327f66492b1dc49076a5a12d4e040",
	"power-wiring.md": "6e1a742072d672c9bb32697bbe6e0c3b9ac46063cf4e6c487e1bc59694fff0de",
	"prototype-drop-targets.md": "1c41020cc0bc715fa2da3c7f41a012c014114809ece43057e7148df46c6ef1a9",
	"service-bulletin-ss20.md": "ee75353c5172107d5ebd4f73e367f4eac541cdddd9b87e2a6e34a57014e1a5f7",
	"solenoid-connections.md": "8f6aa5625c5f7856cce71617391dd002ddd7817add0bfbdb15902cd782e9dbd5",
	"solenoid-locations.md": "eba70b860fa6355f986d6a9d56c62dc6941423b2eec082c1d9c56d6bc9643cfa",
	"sound-board-ds1.md": "88269618ddd263f16ecae241f7cc63ffc5c8d320407e5a4390bef888c044dc0b",
	"switch-locations.md": "535fa4e751ebaa7fdc88ab74de4d296a00c68db38ce082f3135ce67b3f011a1f",
	"switch-matrix.md": "4315fd028197883a511c94da4a4f995abbbfc65cfec19a3bd5393758ac156de3",
}
EXCERPT_IMAGES = {
	"switch-matrix.md": ("c2997435fb125fb71b02dcec289da3261ed739f560ce42b993c499db7634faa7", "Williams_1980_Firepower_Instruction_Booklet.pdf page 11, crop box 0.165,0.045,0.925,0.935, scanned page rendered at its native resolution (embedded image xref 61, 5402px across 9.00in), rendered at 183 dpi, capped to 1250px wide, grayscale, 1251x911 WebP quality 78"),
	"lamp-matrix.md": ("816cbbc02dc16ad9f531b3aba1a55a0bd0f1175ebb979815a9e87aab639edb8d", "Williams_1980_Firepower_Instruction_Booklet.pdf page 12, crop box 0.165,0.06,0.93,0.935, scanned page rendered at its native resolution (embedded image xref 69, 5400px across 9.00in), rendered at 174 dpi, capped to 1200px wide, grayscale, 1201x853 WebP quality 75"),
	"solenoid-connections.md": ("576e8caa1a53b0b519361bfd929e1abce9a7695887ad41f4767bacae8252b6a1", "Williams_1980_Firepower_Instruction_Booklet.pdf page 9, crop box 0.03,0.08,0.99,0.76, scanned page rendered at its native resolution (embedded image xref 49, 3341px across 5.57in), rendered at 206 dpi, capped to 1100px wide, grayscale, 1101x1259 WebP quality 75"),
	"switch-locations.md": ("d1636730d1c9b08d907dbda832a7d489d3ffe8db329bef5219001b749449da3d", "Williams_1980_Firepower_Instruction_Booklet.pdf page 10, crop box 0,0.03,1,0.93, scanned page rendered at its native resolution (embedded image xref 55, 3353px across 5.59in), rendered at 233 dpi, capped to 1300px wide, grayscale, 1300x1885 WebP quality 80"),
	"solenoid-locations.md": ("a4a80efc942b657e46cafa7206319675fcdad4ed4aa6dea6b7651cf1c3df4438", "Williams_1980_Firepower_Instruction_Booklet.pdf page 8, crop box 0,0.03,1,0.93, scanned page rendered at its native resolution (embedded image xref 43, 3315px across 5.52in), rendered at 199 dpi, capped to 1100px wide, grayscale, 1100x1607 WebP quality 75"),
	"playfield-solenoid-wiring.md": ("4bec5a59e66efc22bbd02327a145a1901b84a500f3bf1b3f5a6d94a2a3874964", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 25, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 66, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"playfield-switch-wiring.md": ("86e7b9bcba4612f27b44e6bced284e28aa1bbfa5b33fe98350b182618e9996b3", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 26, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 69, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"playfield-lamp-wiring.md": ("870077f5faee6fa6a67deb4702ecfe3a5be0bd081ccd37e19f559ef579fbeb84", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 27, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 72, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"cabinet-wiring.md": ("2c5d0737ba3dedfaf2828a9bdb2a6423933c9d31e785670b7a735e162132660c", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 24, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 63, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"insert-board-wiring.md": ("0e568ad2a9eb5c2747db4b866bca5641eee7cb0e34e206112005773fa9f9bd31", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 28, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 75, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"power-wiring.md": ("85c7e8c14c8ea1ddefbe2a8e060f47510b56f73eed6ffa524b3c05dac1df29af", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 23, crop box 0.03,0.02,0.99,0.97, scanned page rendered at its native resolution (embedded image xref 60, 5100px across 8.50in), rendered at 245 dpi, capped to 2000px wide, grayscale, rotated 270 degrees counter-clockwise, 2563x2001 WebP quality 75"),
	"sound-board-ds1.md": ("8293d15052635a76a678f2ec217de3a01873fb2b60ba23b59f48dd7cf749dba7", "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf page 15, crop box 0.1,0.3,0.58,0.72, scanned page rendered at its native resolution (embedded image xref 36, 10200px across 17.00in), rendered at 172 dpi, capped to 1400px wide, grayscale, 1401x793 WebP quality 80"),
}

# --- Exact centres of the retained table objects used for placements, in table units. Walls are
# drag-point centroids; the four standup-target primitives are the centres of their world-space
# mesh bounds from `vpxtool export obj --units vpu`, because their stored position is a local offset
# (review-artifacts/firepower-1980/primitive-world-bounds.json).
TABLE_POINTS: dict[str, tuple[float, float]] = {
	"LeftOutsideRollover": (60.32089, 1547.831),
	"LeftInsideRollover": (125.890724, 1398.2422),
	"FRollover": (276.5903, 168.1979),
	"IRollover": (376.883, 189.4907),
	"RRollover": (502.66037, 215.09303),
	"ERollover": (602.6355, 235.22707),
	"RightInsideRollover": (748.378, 1400.466),
	"RightOutsideRollover": (814.04095, 1447.5771),
	"BallShooter": (900.61847, 1746.4131),
	"LeftEjectRollover": (98.07811, 992.4849),
	"RightEjectRollover": (782.4503, 511.5642),
	"LeftSlingShot": (214.770305, 1387.39395),
	"RightSlingShot": (660.84819, 1391.2061666666668),
	"StandupTarget1": (208.729275, 264.59590000000003),
	"StandupTarget2": (676.3924, 310.94629),
	"StandupTarget3": (712.2946775, 422.0900125),
	"StandupTarget4": (73.84082075, 615.6974125),
	"StandupTarget5": (828.3912925, 1143.003525),
	"StandupTarget6": (129.777086, 834.7969475),
	"StandupTarget7": (822.8543625, 817.4178675),
	"KLeftEjectHole": (60.186, 757.5807),
	"KRightEjectHole": (741.2974, 301.0851),
	"KUpperEjectHole": (670.62103, 63.962223),
	"KBallSaveKicker": (58.0, 1570.804),
	"BallRelease": (795.05115, 1707.625),
	"Spinner": (93.05807, 460.41278),
	"Bumper1": (324.99466, 379.5508),
	"Bumper2": (548.6356, 424.31635),
	"Bumper3": (541.22864, 624.11053),
	"Bumper4": (342.46472, 579.6772),
	"Target1T": (261.20285, 734.59607),
	"Target2T": (311.941, 718.91895),
	"Target3T": (372.67593, 704.99786),
	"Target4T": (497.9665, 751.19714),
	"Target5T": (552.2136, 762.4956),
	"Target6T": (611.3323, 775.6248),
	"PTTarget_6": (790.9817, 919.5844),
	"PMTarget_6": (805.5827, 974.0984),
	"PBTarget_6": (819.6124, 1032.5696),
	"TopTarget_6": (441.7953, 227.291),
	"LShootAgain": (435.6717, 1705.5168),
	"LShieldOn": (78.250404, 1239.7133),
	"LFire1": (223.4015, 1228.3005),
	"LFire2": (311.1277, 1151.9413),
	"LPower1": (563.33264, 1154.0721),
	"LPower2": (651.5153, 1224.5571),
	"LF": (276.63257, 94.64838),
	"LI": (377.40863, 117.28516),
	"LR": (503.4891, 137.99759),
	"LE": (603.51306, 162.34746),
	"LBlueTop": (761.6881, 969.5099),
	"LBlueMiddle": (777.98834, 1023.6577),
	"LBlueBottom": (791.5954, 1079.5092),
	"LRightBlue1000": (747.7938, 1295.8584),
	"LLeftBlue1000": (123.683716, 1301.8564),
	"L1": (436.87485, 1633.7412),
	"L2": (437.20972, 1574.4678),
	"L3": (437.96878, 1515.4844),
	"L4": (438.49936, 1456.8883),
	"L5": (437.95984, 1397.6344),
	"L6": (437.60867, 1337.6299),
	"L7": (438.66003, 1278.621),
	"L8": (436.32645, 1219.515),
	"L9": (434.56638, 1161.0259),
	"L10": (437.1504, 1098.9065),
	"L20": (435.36194, 1018.04913),
	"LT1": (343.21976, 1050.2467),
	"LT2": (365.2645, 953.70886),
	"LT3": (393.17438, 858.08295),
	"LT4": (473.0144, 908.32477),
	"LT5": (503.08142, 999.70953),
	"LT6": (527.0947, 1083.2777),
	"LSpinner": (112.48479, 547.2603),
	"LLeftHole": (149.24942, 1091.0208),
	"LRightHole": (741.82404, 609.9177),
	"LBackHole": (497.71082, 58.775326),
	"L2X": (280.08234, 1521.122),
	"L3X": (327.60516, 1556.9913),
	"L4X": (546.1408, 1558.0127),
	"L5X": (592.77454, 1523.2971),
	"LExtraBall": (727.63135, 1099.5388),
	"L10K": (441.29605, 504.1623),
	"L30K": (442.81265, 418.02744),
	"L50K": (441.2942, 318.5448),
	"LBumperTopLeft": (323.5325, 379.51852),
	"LBumperTopRight": (548.6456, 425.64804),
	"LBumperBottomRight": (544.1928, 623.0253),
	"LBumperBottomLeft": (342.15704, 579.01170),
	"LLeftSpecial": (63.282417, 1353.1709),
	"LRightSpecial": (812.8196, 1346.5988),
	"FlasherLightFire": (253.57352, 1180.9282),
	"FlasherLightPower": (620.9616, 1179.3502),
	# The Vs A.I. revision's apron credit lamp; the base table does not model lamp 56.
	"CreditLight1": (89.250626, 1694.0946),
}

# Hidden devices placed from the booklet's Figure 4, registered onto the table frame (see
# evidence/excerpts/williams.firepower.1980/switch-locations.md). Two decimals: the fit's residual is
# about 0.02 of the playfield width.
DRAWING_POINTS: dict[str, tuple[float, float]] = {
	"outhole": (0.47, 0.92),
	"playfield-tilt": (0.16, 0.86),
	"lane-change": (0.57, 0.80),
	"left-ball-ramp": (0.78, 0.89),
	"center-ball-ramp": (0.82, 0.88),
	"right-ball-ramp": (0.85, 0.88),
	"center-middle-left-standup": (0.12, 0.37),
}


def normalized(name: str) -> tuple[float, float]:
	x, y = TABLE_POINTS[name]
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


# --- Switch matrix. Label, role, switch_type, object(s) or drawing point, construction note.
# Column/row wiring from Figure 5 and the schematics' switch and cabinet sheets.
SWITCH_COLUMNS = {
	1: ("GRN-BRN", "2J2-9, 7P1-19"),
	2: ("GRN-RED", "2J2-8, 8P1-1"),
	3: ("GRN-ORN", "2J2-7, 8P1-2"),
	4: ("GRN-YEL", "2J2-6, 8P1-3"),
	5: ("GRN-BLK", "2J2-5, 8P1-4"),
	6: ("GRN-BLU", "2J2-3, 8P1-5"),
	7: ("GRN-VIO", "2J2-2, 8P1-6"),
	8: ("GRN-GRY", "2J2-1, 8P1-7"),
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

S = "script"  # bound by the retained known-working script
SWITCHES: dict[int, dict[str, Any]] = {
	1: dict(label="Plumb Bob Tilt", role="cabinet.tilt", type="tilt", location="cabinet", cabinet="7SW1"),
	2: dict(label="Ball Roll Tilt", role="cabinet.tilt", type="tilt", location="cabinet", cabinet="7SW2"),
	3: dict(label="Credit Button", role="cabinet.start", type="button", location="cabinet front", cabinet="7SW3"),
	4: dict(label="Right Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW4", note="Printed 7SW4 RIGHT COIN CHUTE on the cabinet sheet, reached through the coin-door connector 7J2-8. PinMAME's IPT_COIN1 keyboard bit lands on this address."),
	5: dict(label="Center Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW5", note="Printed 7SW5 CENTER COIN CHUTE, coin-door connector 7J2-9."),
	6: dict(label="Left Coin Switch", role="cabinet.coin", location="coin door", cabinet="7SW6", note="Printed 7SW6 LEFT COIN CHUTE, coin-door connector 7J2-10."),
	7: dict(label="Slam Tilt", role="cabinet.slam-tilt", type="tilt", location="coin door", cabinet="7SW7", note="Printed 7SW7 SLAM TILT, coin-door connector 7J2-11, drawn as a normally open contact. The booklet: Slam Tilt returns game to game over."),
	8: dict(label="High Score Reset", role="service.high-score-reset", type="button", location="coin door", cabinet="7SW8", note="Printed 7SW8 HIGH SCORE RESET, coin-door connector 7J2-12; the booklet's Figure 1 shows it among the coin-door diagnostic switches."),
	9: dict(label="Outhole", drawing="outhole", note="Below the apron: Figure 4 draws callout 09 in a dashed circle under the apron. The known-working table models the outhole as the entry of a cvpmTrough (trTrough.EntrySw = cOutHoleSW) at a drain kicker on the table's bottom edge, so the placement is the booklet's registered callout rather than that drain object."),
	10: dict(label="Left Outside Rollover", obj="LeftOutsideRollover", note="Wire rollover in the left outlane, above the ball saver kicker."),
	11: dict(label="Left Inside Rollover", obj="LeftInsideRollover"),
	12: dict(label="Left Kicker", obj="LeftSlingShot", note="The scoring contact behind the left kicker (slingshot) rubber, drawn in a dashed circle in Figure 4. Separate from the special switch 8SW70 that fires solenoid 22 on the hardware; PinMAME uses this matrix address as the special switch (sxx.ssSw[5] = 12)."),
	13: dict(label="Left Eject Hole", obj="KLeftEjectHole"),
	14: dict(label="Upper Middle Left Standup", obj="StandupTarget4", standup=True),
	15: dict(label="Spinner", obj="Spinner"),
	16: dict(label="Top Left Standup", obj="StandupTarget1", standup=True),
	17: dict(label='"1" Target', obj="Target1T", target=True),
	18: dict(label='"2" Target', obj="Target2T", target=True),
	19: dict(label='"3" Target', obj="Target3T", target=True),
	21: dict(label='"4" Target', obj="Target4T", target=True),
	22: dict(label='"5" Target', obj="Target5T", target=True),
	23: dict(label='"6" Target', obj="Target6T", target=True),
	25: dict(label="Bottom Left Jet Bumper", obj="Bumper4", bumper="8SW66"),
	26: dict(label="Top Left Jet Bumper", obj="Bumper1", bumper="8SW65"),
	27: dict(label="Top Right Jet Bumper", obj="Bumper2", bumper="8SW67"),
	28: dict(label="Bottom Right Jet Bumper", obj="Bumper3", bumper="8SW68"),
	29: dict(label="Top Center Target", obj="TopTarget_6", note="The standup target between the I and R top lanes. The table models it as a collidable primitive whose stored position is a local offset; the placement is the centre of its world-space mesh bounds."),
	30: dict(label="Right Eject Hole", obj="KRightEjectHole"),
	31: dict(label="Upper Top Right Standup", obj="StandupTarget2", standup=True),
	32: dict(label='"F" Rollover', obj="FRollover"),
	33: dict(label='"I" Rollover', obj="IRollover"),
	34: dict(label='"R" Rollover', obj="RRollover"),
	35: dict(label='"E" Rollover', obj="ERollover"),
	36: dict(label="Upper Right Eject Hole", obj="KUpperEjectHole"),
	37: dict(label="Lower Top Right Standup", obj="StandupTarget3", standup=True),
	38: dict(label="Middle Right Standup", obj="StandupTarget7", standup=True),
	39: dict(label='Top "POWER" Target', obj="PTTarget_6", power=True),
	40: dict(label='Middle "POWER" Target', obj="PMTarget_6", power=True),
	41: dict(label='Bottom "POWER" Target', obj="PBTarget_6", power=True),
	42: dict(label="Right Kicker", obj="RightSlingShot", note="The scoring contact behind the right kicker (slingshot) rubber, dashed in Figure 4. Separate from the special switch 8SW69 that fires solenoid 21 on the hardware; PinMAME uses this matrix address as the special switch (sxx.ssSw[4] = 42)."),
	43: dict(label="Right Inside Rollover", obj="RightInsideRollover"),
	44: dict(label="Right Outside Rollover", obj="RightOutsideRollover"),
	45: dict(label="Right Flipper Lane Change Switch", drawing="lane-change", note="The LANE CHANGE switch 8SW45, a playfield-harness switch drawn in a dashed circle below the playfield near the right flipper. The ROM rotates the lit F-I-R-E lane lamps each time it closes (booklet, and the retained gameplay harness run: public 45 moves lamp 5 off and lamp 6 on). PinMAME's FLIP_SWNO(0,45) copies its synthetic right-flipper button (public 82) into this address every frame, so a consumer drives public 82 rather than 45: the retained flipper-button harness run never writes 45, and pressing 82 alone moves the lit lamp from 5 to 6 and then from 6 to 7."),
	46: dict(label="Ball Shooter", obj="BallShooter"),
	47: dict(label="Playfield Tilt", drawing="playfield-tilt", type="tilt", note="Below the playfield at the lower left (dashed callout 47 in Figure 4). The booklet: the ball in play is tilted on the first closure of the Playfield and Ball Roll tilts."),
	48: dict(label="Lower Right Standup", obj="StandupTarget5", standup=True),
	49: dict(label="Center Middle Left Standup", drawing="center-middle-left-standup", standup=True, note="Figure 4 draws 49 on the left rail rubber level with the left eject hole, between 14 above and 50 below. The base V1.0 table has no wall there (its StandupTarget8 handler has no object behind it); the Vs A.I. revision adds StandupTarget8 at normalized (0.1116, 0.3699), which, like every standup wall in both tables, pulses switch 48. The placement is the booklet's registered rubber segment, which that wall corroborates to within 0.01."),
	50: dict(label="Lower Middle Left Standup", obj="StandupTarget6", standup=True),
	51: dict(label="Left Ball Ramp", drawing="left-ball-ramp", ramp=True),
	53: dict(label="Left Eject Rollover", obj="LeftEjectRollover", note="Star rollover in the lane feeding the left eject hole."),
	54: dict(label="Right Eject Rollover", obj="RightEjectRollover", note="Star rollover in the lane feeding the right eject hole."),
	57: dict(label="Right Ball Ramp", drawing="right-ball-ramp", ramp=True),
	58: dict(label="Center Ball Ramp", drawing="center-ball-ramp", ramp=True),
}
UNUSED_SWITCHES = {
	20: "Printed NOT USED in Figure 5 and not drawn on the schematic's switch sheet. On the drop-target prototype this was the '1-3' bank's series switch (Ted Estes).",
	24: "Printed NOT USED in Figure 5 and not drawn on the schematic's switch sheet. On the drop-target prototype this was the '4-6' bank's series switch (Ted Estes).",
	52: "Printed NOT USED in Figure 5 and not drawn on the schematic's switch sheet. On the drop-target prototype this was the '4-6' bank's 10-point switch (Ted Estes).",
	55: "Printed NOT USED in Figure 5 and not drawn on the schematic's switch sheet. On the drop-target prototype this was the '1-3' bank's 10-point switch (Ted Estes).",
	56: "Printed NOT USED in Figure 5 and not drawn on the schematic's switch sheet.",
	59: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
	60: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
	61: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
	62: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
	63: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
	64: "Printed NOT USED in Figure 5; the schematic draws column 8 with only 57 and 58, and the ROM's own switch test never reports this address.",
}
DIAGNOSTIC_SWITCHES = {
	-7: ("Advance", "service.advance", "S6_SWADVANCE", "coin door", "The coin-door ADVANCE pushbutton, 7SW75 on the cabinet sheet, wired to the CPU board's 1J4-3. PinMAME samples it into PIA 0 CA1 on every IRQ."),
	-6: ("Auto-Up / Manual-Down", "service.auto-manual", "S6_SWUPDN", "coin door", "The coin-door AUTO-UP / MANUAL-DOWN alternate-action switch, 7SW74, wired to the CPU board's 1J4-4 and sampled into PIA 0 CB1. Public level 1 is Auto-Up: the retained harness runs enter the lamp and switch tests with 1 and the solenoid test with 0, exactly as the booklet's procedure requires."),
	-5: ("CPU Diagnostic", "service.cpu-diagnostic", "S6_SWCPUDIAG", "backbox", "The DIAGNOSTIC pushbutton on the CPU board (booklet Figure 2), wired to the CPU's NMI line."),
	-4: ("Sound Diagnostic", "service.sound-diagnostic", "S6_SWSOUNDDIAG", "backbox", "SW1, the DIAGNOSTIC SWITCH on the D-8224 sound board (schematics page 15)."),
	-3: ("Master Command Enter", "service.master-command-enter", "S6_ENTER", "backbox", "The MASTER COMMAND ENTER pushbutton on the CPU board (booklet Figure 2). PinMAME returns the Master Command switch bank to the ROM only while it is held."),
}
FLIPPER_COLUMN = {
	81: None, 82: ("Right Flipper Button", "flipper.lower.right.button"), 83: None, 84: ("Left Flipper Button", "flipper.lower.left.button"),
	85: None, 86: None, 87: None, 88: None,
}
# DIP addresses follow the profile: bank * 8 + bit + 1.
DIPS = {
	1: ("Sound Board DS1 Position 1", "used", "Position 1 of DS1, the two-position option switch on the D-8224 sound board (schematics page 15). PinMAME's S6_COMPORTS names it Sound Dip 1 (bank 0 bit 0, default 0) and src/wpc/wmssnd.c folds it into bit 5 of the command byte the sound CPU reads."),
	2: ("Sound Board DS1 Position 2", "used", "Position 2 of DS1 on the D-8224 sound board, through jumper W9. PinMAME's S6_COMPORTS names it Sound Dip 2 (bank 0 bit 1, default 1) and src/wpc/wmssnd.c folds it into bit 6 of the sound command byte. The retained known-working script writes Controller.Dip(0) = 0."),
}
for _bit in range(8):
	DIPS[9 + _bit] = (
		f"CPU Board Lower Function Bank F{_bit + 1}",
		"unused",
		f"PinMAME's F{_bit + 1} (bank 1 bit {_bit}), which s6_dips_r returns only at display strobe positions 0 and 1; the source comment 's6 games only want dipcol 2' records that System 6 ROMs never read them. The booklet's Figure 2 labels the second eight-position bank on the CPU board NOT USED.",
	)
MASTER_COMMAND = {
	0: ("Master Command Switch 8 - Zero Audit Totals", "used", "PinMAME's D1 Clear Audits (bank 2 bit 0). The booklet (page 7): 'To zero audit totals (Functions 01-11) set switch 8 to ON' and momentarily press MASTER COMMAND ENTER."),
	1: ("Master Command Switch 7 - Restore Factory Settings", "used", "PinMAME's D2 Reset Defaults (bank 2 bit 1). The booklet: 'To restore factory settings and zero audit totals, set switch 7 to ON. Coin Door must remain open to restore factory settings.'"),
	2: ("Master Command Switch 6 - Auto-Cycle Mode", "used", "PinMAME's D3 Auto-Cycle Mode (bank 2 bit 2). The booklet: 'For Auto-Cycle Mode set switch 6 to ON.'"),
	3: ("Master Command Bank D4", "unused", "PinMAME's D4 (bank 2 bit 3). It is in the nibble the ROM samples, but the booklet assigns no function to any Master Command position other than 8, 7 and 6."),
}
for _bit in range(4, 8):
	MASTER_COMMAND[_bit] = (
		f"Master Command Bank D{_bit + 1}",
		"unused",
		f"PinMAME's D{_bit + 1} (bank 2 bit {_bit}), returned only at display strobe position 3, which the source comment says System 6 ROMs do not sample. The booklet assigns it no function.",
	)
for _bit, _spec in MASTER_COMMAND.items():
	DIPS[17 + _bit] = _spec

# --- Solenoids. Table 3 of the booklet with the schematic's coil designators.
SOLENOIDS: dict[int, dict[str, Any]] = {
	1: dict(label="Ball Release", kind="coil", q="Q15", wire="GRY-BRN", conn="2P11-4, 8P3-17", part="SA-23-850-DC", coil="8L1", diode="8D129", place=("drawing", "outhole"), note="The outhole kicker: it kicks a drained ball from the outhole (switch 9) up onto the ball ramp. The retained table binds it to trTrough.SolIn, and the gameplay harness run shows the ROM pulsing it repeatedly while switch 9 is held. Figure 3 puts callout 01 under the apron, centre."),
	2: dict(label="Left Drop Target Reset (Not Used)", kind="coil", q="Q17", wire="GRY-RED", conn="2P11-5, 8P3-18", unused=True, note="Printed Not Used in Table 3 with no part number, and the playfield sheet ends 8P3-18 at N/C. The driver and harness wire are fitted and the ROM still drives the address: the harness runs show it pulsed at every ball start and when targets 1-3 are made, which is the left drop-target bank reset of the ten drop-target prototypes (Ted Estes, IPDB)."),
	3: dict(label="Right Drop Target Reset (Not Used)", kind="coil", q="Q19", wire="GRY-ORN", conn="2P11-7, 8P3-19", unused=True, note="Printed Not Used in Table 3 with no part number, and the playfield sheet ends 8P3-19 at N/C. The ROM still pulses it at every ball start; on the drop-target prototypes it was the right bank reset (Ted Estes, IPDB)."),
	4: dict(label="Left Eject Hole", kind="coil", q="Q21", wire="GRY-YEL", conn="2P11-8, 8P3-20", part="SG-23-850-DC", coil="8L4", diode="8D132", place=("obj", "KLeftEjectHole")),
	5: dict(label="Right Eject Hole", kind="coil", q="Q23", wire="GRY-GRN", conn="2P11-9, 8P3-21", part="SG-23-850-DC", coil="8L5", diode="8D133", place=("obj", "KRightEjectHole")),
	6: dict(label="Upper Right Eject Hole", kind="coil", q="Q25", wire="GRY-BLU", conn="2P11-3, 8P3-22", part="SG-23-850-DC", coil="8L6", diode="8D135", place=("obj", "KUpperEjectHole")),
	7: dict(label="Left Ball Saver Kicker", kind="coil", q="Q27", wire="GRY-VIO", conn="2P11-2, 8P3-23", part="SG-23-850-DC", coil="8L7", diode="8D136", place=("obj", "KBallSaveKicker"), note="The outlane kickback at the foot of the left outlane (Figure 3 callout 07). The retained kicker harness run shows the ROM firing it when the left outside rollover (switch 10) closes with the Ball Saver Kicker On lamp (2) lit, and turning lamp 2 off. The retained table does not use this callback to kick: it kicks locally from its own copy of lamp 2, which is a table simplification, not machine behaviour."),
	8: dict(label="Ball Ramp Thrower", kind="coil", q="Q29", wire="GRY-BLK", conn="2P11-1, 8P3-24", part="SA-23-850-DC", coil="8L8", diode="8D136", place=("obj", "BallRelease"), note="Printed 8L8 BALL RAMP on the schematic. It throws the ball at the exit end of the ball ramp into the shooter lane; the booklet's diagnostic procedure pulses it 'three times to remove balls from ramp'. The retained table binds it to trTrough.SolOut, whose exit kicker is the placement."),
	9: dict(label="Sound Line 1", kind="control_signal", q="Q31", wire="BRN-BLK", conn="2P9-9, 10P3-3", sound=True),
	10: dict(label="Sound Line 2", kind="control_signal", q="Q33", wire="BRN-RED", conn="2P9-7, 10P3-2", sound=True),
	11: dict(label="Sound Line 3", kind="control_signal", q="Q35", wire="BRN-ORN", conn="2P9-1, 10P3-5", sound=True),
	12: dict(label="Sound Line 4", kind="control_signal", q="Q37", wire="BRN-YEL", conn="2P9-2, 10P3-4", sound=True),
	13: dict(label="Sound Line 5", kind="control_signal", q="Q39", wire="BRN-GRN", conn="2P9-3, 10P3-7", sound=True),
	14: dict(label="Credit Knocker", kind="coil", q="Q41", wire="BRN-BLU", conn="2P9-4, 7P1-16", part="SA2-23-850-DC", coil="7L14", diode="7D9", cabinet="cabinet.knocker", note="7L14 CREDIT KNOCKER in the cabinet. The harness gameplay run shows it pulsed when a coin is inserted; the booklet: 'Insert coin; knocker sounds'."),
	15: dict(label="Flash Lamps", kind="flasher", q="Q43", wire="BRN-VIO", conn="2P9-5, 6P2", part="Type 89 Bulbs", place=("objs", ("FlasherLightFire", "FlasherLightPower")), quantity=2, note="Two Type 89 bulbs, 8B65 and 8B66, under the FIRE and POWER inserts above the kickers (Figure 3 draws callout 15 twice, once on each insert). The ROM flashes them every few seconds in attract mode (harness). Service Bulletin SS 20: on production games the flash lamp circuit has its own ground through the 3-pin 6P2/6J2 connector."),
	16: dict(label="Coin Lockout", kind="coil", q="Q45", wire="BRN-GRY", conn="2P9-6, 7P1-18, 7P2-4", part="SM-35-4000-DC", coil="7L16", diode="7D10", cabinet="cabinet.coin-lockout", note="7L16 COIN LOCKOUT on the coin door (7P2-4). The ROM energizes it at power-up (harness) and de-energizes it when credits reach the maximum (booklet)."),
	17: dict(label="Top Left Jet Bumper", kind="coil", q="Q2", wire="BLU-BRN", conn="2P12-7, 8P3-11", part="SG-23-850-DC", coil="8L17", diode="8D137", place=("obj", "Bumper1"), special=("8SW65", "ORN-BRN", "2P13-5, 8P3-5", 26)),
	18: dict(label="Bottom Left Jet Bumper", kind="coil", q="Q4", wire="BLU-RED", conn="2P12-4, 8P3-12", part="SG-23-850-DC", coil="8L18", diode="8D138", place=("obj", "Bumper4"), special=("8SW66", "ORN-RED", "2P13-3, 8P3-6", 25)),
	19: dict(label="Top Right Jet Bumper", kind="coil", q="Q6", wire="BLU-ORN", conn="2P12-3, 8P3-13", part="SG-23-850-DC", coil="8L19", diode="8D139", place=("obj", "Bumper2"), special=("8SW67", "ORN-BLK", "2P13-2, 8P3-7", 27)),
	20: dict(label="Bottom Right Jet Bumper", kind="coil", q="Q8", wire="BLU-YEL", conn="2P12-6, 8P3-14", part="SG-23-850-DC", coil="8L20", diode="8D140", place=("obj", "Bumper3"), special=("8SW68", "ORN-YEL", "2P13-4, 8P3-8", 28), extra_note="Table 3 and Figure 3's chart both print this row 'Bottom Left Jet Bumper', repeating row 18. The schematic labels the coil 8L20 BOTTOM RIGHT JET BUMPER and its special switch 8SW68 BOTTOM RIGHT JET BUMPER, Figure 3 draws callout 20 inside the lower right bumper, PinMAME's sxx.ssSw fires it from switch 28 (Bottom Right Jet Bumper), and the gameplay harness run shows switch 28 publishing it. The printed chart row is a typing error."),
	21: dict(label="Right Kicker", kind="coil", q="Q10", wire="BLU-GRN", conn="2P12-8, 8P3-15", part="SG-23-850-DC", coil="8L21", diode="8D143", place=("obj", "RightSlingShot"), special=("8SW69", "ORN-GRN", "2P13-8, 8P3-9", 42)),
	22: dict(label="Left Kicker", kind="coil", q="Q12", wire="BLU-BLK", conn="2P12-9, 8P3-16", part="SG-23-800-DC", coil="8L22", diode="8D144", place=("obj", "LeftSlingShot"), special=("8SW70", "ORN-BLU", "2P13-9, 8P3-10", 12)),
}

# --- Lamps. Figure 6 labels; quantities from Figure 6 and the insert-board sheet.
LAMP_COLUMNS = {
	1: ("YEL-BRN", "2J5-8, 8P2-3"),
	2: ("YEL-RED", "2J5-9, 8P2-4"),
	3: ("YEL-ORN", "2J5-6, 8P2-5"),
	4: ("YEL-BLK", "2J5-7, 8P2-6"),
	5: ("YEL-GRN", "2J5-3, 8P2-7"),
	6: ("YEL-BLU", "2J5-5, 8P2-8"),
	7: ("YEL-VIO", "2J5-1, 8P2-9 (playfield), 9J1-6 (insert board)"),
	8: ("YEL-GRY", "9J1-7 (insert board)"),
}
LAMP_ROWS = {
	1: ("RED-BRN", "2J7-1", 11, 8),
	2: ("RED-BLK", "2J7-2", 12, 9),
	3: ("RED-ORN", "2J7-3", 13, 10),
	4: ("RED-YEL", "2J7-4", 14, 11),
	5: ("RED-GRN", "2J7-5", 15, 12),
	6: ("RED-BLU", "2J7-6", 16, 13),
	7: ("RED-VIO", "2J7-9", 17, 14),
	8: ("RED-GRY", "2J7-8", 18, 15),
}
LAMPS: dict[int, tuple[str, Any]] = {
	1: ("Same Player Shoots Again (Playfield)", ("LShootAgain",)),
	2: ("Ball Saver Kicker On", ("LShieldOn",)),
	3: ("FIRE", ("LFire1", "LFire2")),
	4: ("POWER", ("LPower1", "LPower2")),
	5: ('"F"', ("LF",)),
	6: ('"I"', ("LI",)),
	7: ('"R"', ("LR",)),
	8: ('"E"', ("LE",)),
	9: ("Top POWER Target", ("LBlueTop",)),
	10: ("Center POWER Target", ("LBlueMiddle",)),
	11: ("Bottom POWER Target", ("LBlueBottom",)),
	12: ("Right Inside Rollover", ("LRightBlue1000",)),
	13: ("Left Inside Rollover", ("LLeftBlue1000",)),
	14: ("1,000 Bonus", ("L1",)),
	15: ("2,000 Bonus", ("L2",)),
	16: ("3,000 Bonus", ("L3",)),
	17: ("4,000 Bonus", ("L4",)),
	18: ("5,000 Bonus", ("L5",)),
	19: ("6,000 Bonus", ("L6",)),
	20: ("7,000 Bonus", ("L7",)),
	21: ("8,000 Bonus", ("L8",)),
	22: ("9,000 Bonus", ("L9",)),
	24: ("10,000 Bonus", ("L10",)),
	25: ("20,000 Bonus", ("L20",)),
	26: ('"1" Target Arrow', ("LT1",)),
	27: ('"2" Target Arrow', ("LT2",)),
	28: ('"3" Target Arrow', ("LT3",)),
	29: ('"4" Target Arrow', ("LT4",)),
	30: ('"5" Target Arrow', ("LT5",)),
	31: ('"6" Target Arrow', ("LT6",)),
	32: ("Spinner 1,000 When Lit", ("LSpinner",)),
	33: ("Left Eject Hole Arrow", ("LLeftHole",)),
	34: ("Right Eject Hole Arrow", ("LRightHole",)),
	35: ("Upper Right Eject Hole Arrow", ("LBackHole",)),
	36: ("2X", ("L2X",)),
	37: ("3X", ("L3X",)),
	38: ("4X", ("L4X",)),
	39: ("5X", ("L5X",)),
	40: ("Extra Ball When Lit", ("LExtraBall",)),
	41: ("10,000 FIREPOWER Bonus", ("L10K",)),
	42: ("30,000 FIREPOWER Bonus", ("L30K",)),
	43: ("50,000 FIREPOWER Bonus", ("L50K",)),
	44: ("Top Left Jet Bumper", ("LBumperTopLeft",)),
	45: ("Top Right Jet Bumper", ("LBumperTopRight",)),
	46: ("Bottom Right Jet Bumper", ("LBumperBottomRight",)),
	47: ("Bottom Left Jet Bumper", ("LBumperBottomLeft",)),
	48: ("Left Special", ("LLeftSpecial",)),
	49: ("Right Special", ("LRightSpecial",)),
	50: ("1 Can Play", None),
	51: ("2 Can Play", None),
	52: ("3 Can Play", None),
	53: ("4 Can Play", None),
	54: ("Match", None),
	55: ("Ball In Play", None),
	56: ("Credits (Playfield)", ("CreditLight1",)),
	57: ("#1 Player Up", None),
	58: ("#2 Player Up", None),
	59: ("#3 Player Up", None),
	60: ("#4 Player Up", None),
	61: ("Tilt", None),
	62: ("Game Over", None),
	63: ("Same Player Shoots Again (Backbox)", None),
	64: ("High Score To Date", None),
}
LAMP_QUANTITY = {3: 2, 4: 2, 62: 2, 63: 2, 64: 2}
LAMP_NOTES = {
	3: "Figure 6 prints FIRE (x2): two bulbs under the red FIRE insert above the left kicker, which also carries one of the two Type 89 flash lamps (solenoid 15).",
	4: "Figure 6 prints POWER (x2): two bulbs under the green POWER insert above the right kicker, which also carries the second Type 89 flash lamp.",
	16: "The playfield lamp sheet labels this bulb a second '8B15' in the lighter hand of a later addition; its row-8 position and diode 8D80 make it bulb 16.",
	26: "The playfield lamp sheet's bulb list calls 26-31 'Drop Target Arrow', from the drop-target prototype; the booklet's Figure 6 says TARGET ARROW. The retained table binds 26-31 twice over, through vpmMapLights and through explicit Set Lights(26..31) lines, to the same six LT objects.",
	44: "The retained table binds public 44-47 with explicit Set Lights() lines to the four bumper-cap lights, which are not in its vpmMapLights collection.",
	46: "Bound by the retained table's explicit Set Lights(46)=LBumperBottomRight. That light object's own TimerInterval is 47, but it is not in the vpmMapLights collection, so the interval is never used.",
	49: "The playfield lamp sheet labels this bulb '8B47' in the lighter hand of a later addition; it sits in column 7 row 1 with diode 8D113, so it is bulb 49. The real 8B47 is drawn in column 6 with 8D111.",
	56: "CREDITS (PLAYFIELD), bulb 8B56 on the playfield harness, lights the round credit window on the left of the apron (IPDB playfield photographs). The booklet: in attract mode 'all playfield lamps except for credit lamp cycle'. The base known-working table does not model it; the Vs A.I. revision of the same table places CreditLight1 behind the apron window, which is the placement.",
}
BACKBOX_INSERTS = {
	50: '"1 CAN PLAY"', 51: '"2 CAN PLAY"', 52: '"3 CAN PLAY"', 53: '"4 CAN PLAY"', 54: '"MATCH"', 55: '"BALL IN PLAY"',
	57: '"PLAYER 1 UP"', 58: '"PLAYER 2 UP"', 59: '"PLAYER 3 UP"', 60: '"PLAYER 4 UP"', 61: '"TILT"', 62: '"GAME OVER"',
	63: '"SAME PLAYER SHOOTS"', 64: '"HIGH SCORE"',
}

# --- Displays: s6_6digit_disp.
DISPLAYS = [
	("display.player-1-score", "Player 1 score, six digits", 0, 0, 6),
	("display.player-2-score", "Player 2 score, six digits", 1, 8, 6),
	("display.player-3-score", "Player 3 score, six digits", 2, 20, 6),
	("display.player-4-score", "Player 4 score, six digits", 3, 28, 6),
	("display.credits", "Credit display, two digits (master display left pair, strobes 15-16)", 4, 14, 2),
	("display.ball-in-play", "Ball in play and match display, two digits (master display right pair, strobes 7-8)", 5, 6, 2),
]
SEVEN_DIGIT_OVERRIDES = {
	"display.player-1-score": (0, 7),
	"display.player-2-score": (7, 7),
	"display.player-3-score": (20, 7),
	"display.player-4-score": (27, 7),
	"display.credits": (34, 2),
	"display.ball-in-play": (14, 2),
}

DRIVER_IDS = (
	"frpwr_l6", "frpwr_l2", "frpwr_l6ff", "frpwr_l2ff", "frpwr_t6", "frpwr_t6ff",
	"frpwr_a6", "frpwr_d6", "frpwr_b6", "frpwr_c6",
)
# driver: the harness run that observed which fp_7digit_disp entry carries credits and ball in play
SEVEN_DIGIT_DRIVERS = {"frpwr_b6": HARNESS_B6_SOURCE, "frpwr_c6": HARNESS_C6_SOURCE}
CONVERSION_DRIVER_IDS = ("frpwr_a7", "frpwr_e7", "frpwr_b7", "frpwr_c7", "frpwr_d7")
DRIVER_NOTES = {
	"frpwr_l6": ("identical", "Williams production L-6 game ROM set on the System 6 CPU board: game ROM, green flipper ROMs 1 and 2 and PROMs 1-3 (prom1_6), with sound ROM 3 and speech ROMs 5T4971-5T4973. The booklet requires green-labeled FIREPOWER PROMs, game ROM and flipper ROMs on a revision 6 or later CPU board. This is the driver the solenoid-test, switch-test, gameplay, ball-saver-kicker and flipper-button harness runs use; the seven-digit display runs use frpwr_b6 and frpwr_c6."),
	"frpwr_l2": ("identical", "Earlier Williams L-2 release: the same game ROM and flipper ROMs with the earlier PROM 1 (prom1.474). IPDB records that the only differences between L-2 and L-6 are the price presets and the maximum credits. Same init data, display layout and inputs as L-6."),
	"frpwr_l6ff": ("identical", "L-6 with the community free-play fix: flipper ROM 1 replaced by green1fpfix.716, which keeps the credit knocker working when Adjustment 18 sets free play (s6games.c header comment). Same hardware and addresses."),
	"frpwr_l2ff": ("identical", "L-2 with the same free-play-fix flipper ROM 1. Same hardware and addresses."),
	"frpwr_t6": ("identical", "Ted Estes's T-6 revision (driver.c: /10 scoring): flipper ROM 2 replaced by green2a.716 on the L-6 set. Same hardware and addresses."),
	"frpwr_t6ff": ("identical", "T-6 with the free-play-fix flipper ROM 1. Same hardware and addresses."),
	"frpwr_a6": ("compatible", "Oliver 2008 System 6 six-digit custom ROM, revision 31: a 4 KB game EPROM in IC14 (S6_ROMSTARTMOD) replacing the stock ROM and PROM set on the same System 6 board, with the stock sound and speech ROMs. Addresses, display layout and hardware are the production machine's; only the CPU ROM chip set differs."),
	"frpwr_d6": ("compatible", "Oliver 2008 System 6 six-digit /10 scoring ROM, revision 31, fitted the same way as frpwr_a6. Addresses, display layout and hardware are the production machine's."),
	"frpwr_b6": ("compatible", "Oliver 2003 System 6 seven-digit conversion: custom CPU ROMs plus seven-digit player displays on the same System 6 CPU board. PinMAME declares fp_7digit_disp for it, so the six displays are published at different display-memory positions and the player displays are seven digits wide; see display_overrides. PinMAME labels the two small entries only as left and right side; the retained frpwr_b6 harness run shows the coin credit on the entry at position 34 and the ball in play on the entry at position 14. Switch, lamp and solenoid addresses are the production machine's, and the same run reproduces the special-solenoid, eject-hole, outhole and ball-ramp causality."),
	"frpwr_c6": ("compatible", "Oliver 2008 System 6 seven-digit conversion, revision 31. Same seven-digit display layout as frpwr_b6; see display_overrides. Its own harness run shows the credit on position 34 and the ball in play on position 14, and the same special-solenoid, eject-hole, outhole and ball-ramp causality. Switch, lamp and solenoid addresses are the production machine's."),
}
CONVERSION_DRIVER_NOTES = {
	"frpwr_a7": "Oliver 2005 System 7 six-digit conversion, revision 31 (s7games.c: s7_mS7S6, GEN_S7, s7_6digit_disp). PinMAME declares it as its own root. No harness run of this driver is retained.",
	"frpwr_e7": "Oliver 2005 System 7 six-digit /10 scoring conversion, revision 31 (s7_mS7S6, s7_6digit_disp). PinMAME declares it as its own root. No harness run of this driver is retained.",
	"frpwr_b7": "Oliver 2003 System 7 seven-digit conversion (s7_mS7S6, fp_7digit_disp), declared a clone of frpwr_l6. The ROM the retained known-working Firepower table loads. One retained harness run covers a game start and the switch-driven special-solenoid path; see the knowledge note for what it does and does not show.",
	"frpwr_c7": "Oliver 2006 System 7 seven-digit conversion, revision 38, with an extra IC26 ROM and speech ROM v_ic4 (s7_mS7S6, fp_7digit_disp), declared a clone of frpwr_l6. No harness run of this driver is retained.",
	"frpwr_d7": "Oliver 2005 System 7 seven-digit conversion, revision 31 (s7_mS7S6, fp_7digit_disp). PinMAME declares it as its own root. No harness run of this driver is retained.",
}


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def located(identifier: str, role: str, points: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(points, start=1):
		suffix = f".{index}" if len(points) > 1 else ""
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


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def switch_id(address: int) -> str:
	if address in SWITCHES:
		return f"switch.{slug(SWITCHES[address]['label'])}"
	return f"switch.not-used-{address}"


def solenoid_id(address: int) -> str:
	return f"{'flasher' if SOLENOIDS[address]['kind'] == 'flasher' else 'coil'}.{slug(SOLENOIDS[address]['label'])}"


def lamp_id(address: int) -> str:
	return f"lamp.{slug(LAMPS[address][0]) if address in LAMPS else 'not-used'}-{address}"


def switch_wiring(address: int) -> dict[str, Any]:
	column = (address - 1) // 8 + 1
	row = (address - 1) % 8 + 1
	column_wire, column_connection = SWITCH_COLUMNS[column]
	row_wire, row_driver, row_playfield = SWITCH_ROWS[row]
	if column == 1:
		return_connection = f"{row_driver}, 7P1-{20 + row}"
		diode = f"7D{address}"
	else:
		return_connection = f"{row_driver}, 8P1-{row_playfield}"
		diode = f"8D{address}"
	return {
		"board": "Williams System 6 driver board",
		"drive_wire": column_wire,
		"drive_connection": column_connection,
		"return_wire": row_wire,
		"return_connection": return_connection,
		"return_component": f"diode {diode}, column {column} row {row}",
	}


SWITCH_SOURCES = (BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_SWITCH_SOURCE, CORE_SOURCE)


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
				"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE, BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOLENOID_SOURCE),
				"spatial": not_applicable("cabinet_or_service", BOOKLET_SOURCE, SCHEMATICS_SOURCE),
			}
		)
	for address in range(1, 65):
		column = (address - 1) // 8 + 1
		row = (address - 1) % 8 + 1
		base = {
			"binding": {"group": "pinmame.input.switch", "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
		}
		if address in UNUSED_SWITCHES:
			device = {
				"id": switch_id(address),
				"label": f"Not Used (matrix column {column} row {row})",
				"kind": "switch",
				**base,
				"availability": "unused",
				"physical": {"notes": UNUSED_SWITCHES[address]},
				"provenance": provenance(BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_SWITCH_SOURCE),
				"spatial": not_applicable("unused", BOOKLET_SOURCE, SCHEMATICS_SOURCE),
			}
			items.append(device)
			continue
		spec = SWITCHES[address]
		notes: list[str] = []
		physical: dict[str, Any] = {}
		refs: list[str] = list(SWITCH_SOURCES)
		spatial_refs: list[str] = [BOOKLET_SOURCE, GEOMETRY_SOURCE]
		if "cabinet" in spec:
			physical["location"] = spec["location"]
			notes.append(f"Cabinet switch {spec['cabinet']} on the cabinet wiring sheet, drawn as a normally open contact with series diode {spec['cabinet'].replace('SW', 'D')}.")
			if address in (4, 5, 6, 7, 8):
				notes.append("On the hardware it is an ordinary column-1 matrix position; with PinMAME's keyboard handling on, SWITCH_UPDATE(s6) overwrites column 1 from the S6_COMPORTS port every frame, and with it off, as under LibPinMAME, the consumer writes it directly.")
		else:
			physical["location"] = "playfield"
			notes.append(f"Playfield switch 8SW{address} with series diode 8D{address} on the schematic's switch sheet, drawn as a normally open contact.")
		if spec.get("type"):
			physical["switch_type"] = spec["type"]
		if spec.get("standup"):
			notes.append("A 50-point standup on a rubber-post run. Both retained tables pulse switch 48 from all of their StandupTarget walls, a table defect; the pinned 1.1 Thal Mod script binds each standup to its own address, and the ROM's switch test reports each address as printed.")
			refs.append(THAL_SCRIPT_SOURCE)
		if spec.get("target"):
			notes.append("A 1000-point standup in the two three-target banks above the flippers. The schematic's switch list still calls it a Drop Target: the first ten machines had two 3-banks of drop targets here and production shipped standups (IPDB; Ted Estes).")
			refs += [VPX_SCRIPT_SOURCE, PROTOTYPE_SOURCE]
		if spec.get("power"):
			notes.append("One of the three POWER standups on the right side, top to bottom 39, 40, 41; the table models each as a collidable primitive whose stored position is a local offset, so the placement is the centre of its world-space mesh bounds.")
			refs.append(VPX_SCRIPT_SOURCE)
		if spec.get("bumper"):
			notes.append(f"The jet bumper's scoring contact. The bumper also has a special switch, {spec['bumper']}, that fires its coil through the driver board and is not in the switch matrix; PinMAME models that by publishing the bumper's special solenoid whenever this matrix switch closes (sxx.ssSw), which the gameplay harness run confirms.")
			refs.append(VPX_SCRIPT_SOURCE)
		if spec.get("ramp"):
			notes.append("One of the three ball-rest positions on the ball ramp below the apron, left 51, centre 58, right 57 at the exit end (Figure 4 draws them side by side in a dashed oval). The retained table models the ramp as a three-ball cvpmTrough with addsw 2, 1, 0 = 51, 58, 57.")
			refs.append(VPX_SCRIPT_SOURCE)
			physical["location"] = "below the apron"
		if spec.get("note"):
			notes.append(spec["note"])
		if address == 45:
			refs += [HARNESS_GAMEPLAY_SOURCE, HARNESS_FLIPPER_SOURCE]
		if "obj" in spec and not spec.get("standup") and not spec.get("target") and not spec.get("power") and not spec.get("bumper"):
			refs.append(VPX_SCRIPT_SOURCE)
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
			device["spatial"] = not_applicable("cabinet_or_service", BOOKLET_SOURCE, SCHEMATICS_SOURCE)
		else:
			device["provenance"] = provenance(*refs)
			if "obj" in spec:
				point = normalized(spec["obj"])
				spatial_refs = [VPX_TABLE_SOURCE, BOOKLET_SOURCE]
				if spec.get("standup"):
					spatial_refs.append(GEOMETRY_SOURCE)
			else:
				point = DRAWING_POINTS[spec["drawing"]]
				spatial_refs = [BOOKLET_SOURCE, GEOMETRY_SOURCE, VPX_TABLE_SOURCE]
				if spec.get("standup"):
					spatial_refs.append(VPX_AI_TABLE_SOURCE)
			device["spatial"] = located(device["id"], "sensor", [point], *spatial_refs)
		items.append(device)
	for address, spec in FLIPPER_COLUMN.items():
		base = {
			"binding": {"group": "pinmame.input.switch", "device": address},
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
		}
		if spec is None:
			items.append(
				{
					"id": f"switch.flipper-column-{address}",
					"label": f"Unused emulator flipper-column position {address}",
					"kind": "virtual",
					**base,
					"availability": "unused",
					"physical": {"notes": "PinMAME's generic flipper column (internal column 11) published at 81-88. Firepower declares FLIP_SWNO(0,45) with no FLIP_SOL or FLIP_EOS bit, so only the lower-right (82) and lower-left (84) button bits mean anything; this position has no physical contact and nothing reads it."},
					"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE),
					"spatial": not_applicable("virtual", CONTROLLER_SOURCE, CORE_SOURCE),
				}
			)
			continue
		label, role = spec
		if address == 82:
			note = "PinMAME's synthetic lower-right flipper button (CORE_SWLRFLIPBUTBIT). core_updateSw copies it into public switch 45, the LANE CHANGE switch the ROM reads, and fabricates flipper outputs 45 and 46 from it while the game-on enable (solenoid 23) is set. On the machine the cabinet button 7SW72 switches the right flipper coil directly through relay Z1 and is not a matrix switch. The retained flipper-button harness run shows both effects without ever writing 45: pressing 82 pulses outputs 45 and 46 and moves the lit lane-change lamp. The retained Vs A.I. revision writes Controller.Switch(82) for its flipper key, and VPinMAME's S6.VBS maps its right flipper key to swLRFlip = 82."
		else:
			note = "PinMAME's synthetic lower-left flipper button (CORE_SWLLFLIPBUTBIT). FLIP_SWNO(0,45) names no left matrix switch, so the ROM never reads it; PinMAME only fabricates flipper outputs 47 and 48 from it while the game-on enable (solenoid 23) is set; the retained flipper-button harness run shows 84 pulsing 47 and 48 and nothing else. On the machine the cabinet button 7SW73 switches the left flipper coil directly through relay Z1. VPinMAME's S6.VBS maps its left flipper key to swLLFlip = 84."
		items.append(
			{
				"id": f"switch.{slug(label)}",
				"label": label,
				"kind": "virtual",
				**base,
				"availability": "used",
				"roles": [role],
				"physical": {"notes": note},
				"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE, SCHEMATICS_SOURCE, VPX_AI_SCRIPT_SOURCE, HARNESS_FLIPPER_SOURCE),
				"spatial": not_applicable("virtual", CONTROLLER_SOURCE, CORE_SOURCE),
			}
		)
	for address, (label, availability, note) in sorted(DIPS.items()):
		items.append(
			{
				"id": f"dip.{slug(label)}",
				"label": label,
				"kind": "dip_switch",
				"binding": {"group": "pinmame.input.dip", "device": address},
				"aliases": [{"namespace": "pinmame.dip", "value": str(address)}],
				"availability": availability,
				"physical": {"location": "backbox" if address > 2 else "backbox, sound board", "switch_type": "dip", "notes": note},
				"provenance": provenance(CONTROLLER_SOURCE, CORE_SOURCE, BOOKLET_SOURCE, SCHEMATICS_SOURCE),
				"spatial": not_applicable("dip_switch", CONTROLLER_SOURCE, BOOKLET_SOURCE),
			}
		)
	return items


def solenoid_wiring(address: int, spec: dict[str, Any]) -> dict[str, Any]:
	wiring: dict[str, Any] = {
		"board": "Williams System 6 driver board",
		"driver_transistor": spec["q"],
		"drive_wire": spec["wire"],
		"drive_connection": spec["conn"],
		"control_connection": f"driver {spec['q']} (Table 3 solenoid {address:02d})",
	}
	if spec["kind"] == "control_signal":
		wiring["return_component"] = "sound board sound/speech select input"
		return wiring
	if spec.get("unused"):
		wiring["return_component"] = "harness wire ends N/C on the playfield solenoid sheet"
		return wiring
	if address in (14, 16):
		wiring.update({"power_wire": "RED", "power_connection": "3J3-7, 7J1-3 (+28V)", "nominal_voltage_v": 28, "voltage_type": "dc"})
	elif address == 15:
		wiring.update({"return_component": "8B65 and 8B66 Type 89, 8R7 1 ohm 1/2 W, 8R8 330 ohm 2 W"})
	else:
		wiring.update({"power_wire": "RED", "power_connection": "3J3-6, 8P3-1 (SOL. B+)", "nominal_voltage_v": 28, "voltage_type": "dc"})
	if spec.get("diode"):
		wiring["return_component"] = f"coil {spec['coil']} with diode {spec['diode']}"
	if spec.get("special"):
		switch, wire, connection, _matrix = spec["special"]
		wiring["control_wire"] = wire
		wiring["control_connection"] = f"special switch {switch}, {connection}"
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	base_refs = (BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOLENOID_SOURCE, CORE_SOURCE)
	for address in range(1, 23):
		spec = SOLENOIDS[address]
		notes: list[str] = []
		refs = list(base_refs)
		physical: dict[str, Any] = {}
		if spec.get("part"):
			physical["part_number"] = spec["part"]
		if spec.get("quantity"):
			physical["quantity"] = spec["quantity"]
		if spec.get("coil"):
			notes.append(f"Coil {spec['coil']} with diode {spec['diode']}." if spec["kind"] == "coil" else "")
		if spec.get("sound"):
			notes.append(f"Printed Sound in Table 3. Driver {spec['q']} feeds the D-8224 sound board's SOUND/SPEECH SELECT INPUT at {spec['conn'].split(', ')[1]}; PinMAME passes the inverted port byte to the sound board (sndbrd_0_data_w) and publishes the same bits as solenoids 9-16, so these addresses carry sound commands, not coils.")
			physical["location"] = "backbox"
		if spec.get("special"):
			switch, _wire, _connection, matrix = spec["special"]
			notes.append(f"Special solenoid {address - 16} of 6, driven from a PIA CA2/CB2 line and fired on the hardware by special switch {switch}; PinMAME also publishes it whenever matrix switch {matrix} closes while the game-on enable is set (sxx.ssSw), which the gameplay harness run confirms. That switch-to-coil relationship is PinMAME's contract, which a consumer relies on; on the machine switch {matrix} is the separate scoring contact on the same assembly, and one ball hit closes it and the special switch together without one driving the other.")
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if spec.get("note"):
			notes.append(spec["note"])
		if spec.get("extra_note"):
			notes.append(spec["extra_note"])
		if address in (1, 4, 5, 6, 8):
			refs += [HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE]
		if address == 7:
			refs += [HARNESS_KICKER_SOURCE]
		if address in (2, 3):
			refs += [HARNESS_GAMEPLAY_SOURCE, HARNESS_KICKER_SOURCE, PROTOTYPE_SOURCE]
		if address in (14, 16):
			refs += [HARNESS_GAMEPLAY_SOURCE]
			physical["location"] = "cabinet" if address == 14 else "coin door"
		if address == 15:
			refs += [VPX_SCRIPT_SOURCE, BULLETIN_SOURCE]
		physical["notes"] = " ".join(note for note in notes if note)
		device: dict[str, Any] = {
			"id": solenoid_id(address),
			"label": spec["label"],
			"kind": spec["kind"],
			"binding": {"group": "pinmame.output.solenoid", "device": address},
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"availability": "unused" if spec.get("unused") else "used",
			"physical": physical,
			"wiring": solenoid_wiring(address, spec),
			"provenance": provenance(*refs),
		}
		if spec.get("cabinet"):
			device["roles"] = [spec["cabinet"]]
			device["spatial"] = not_applicable("cabinet_or_service", BOOKLET_SOURCE, SCHEMATICS_SOURCE)
		elif spec.get("unused"):
			device["spatial"] = not_applicable("unused", BOOKLET_SOURCE, SCHEMATICS_SOURCE)
		elif spec.get("sound"):
			device["spatial"] = not_applicable("internal_nonvisual", BOOKLET_SOURCE, SCHEMATICS_SOURCE)
		else:
			how, what = spec["place"]
			role = "emitter" if spec["kind"] == "flasher" else "effect"
			if how == "drawing":
				device["spatial"] = located(device["id"], role, [DRAWING_POINTS[what]], BOOKLET_SOURCE, GEOMETRY_SOURCE, VPX_TABLE_SOURCE)
			elif how == "objs":
				device["spatial"] = located(device["id"], role, [normalized(name) for name in what], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, BOOKLET_SOURCE)
			else:
				device["spatial"] = located(device["id"], role, [normalized(what)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, BOOKLET_SOURCE)
		items.append(device)
	items.append(
		{
			"id": "relay.game-on-flipper-enable",
			"label": "Game On (Flipper Relay and Special Solenoid Enable)",
			"kind": "relay",
			"binding": {"group": "pinmame.output.solenoid", "device": 23},
			"aliases": [{"namespace": "pinmame.solenoid", "value": "23"}],
			"availability": "used",
			"roles": ["cabinet.flipper-enable-relay"],
			"physical": {
				"location": "backbox, driver board",
				"notes": "PinMAME's CORE_SSFLIPENSOL: the PIA 3 CB2 game-on line (s6_gameon_w), published while the ROM enables play. On the driver board that line pulls in relay Z1, whose contact grounds both flipper-button returns (2J12-1 and 2J12-2), and it gates the six special solenoids. The harness runs show it asserting at game start and on entering the solenoid test.",
			},
			"wiring": {"board": "Williams System 6 driver board", "control_connection": "PIA 3 CB2 game-on line, relay Z1", "return_component": "relay Z1 contact to ground on 2J12-1/2J12-2"},
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, SCHEMATICS_SOURCE, HARNESS_SOLENOID_SOURCE, HARNESS_GAMEPLAY_SOURCE),
			"spatial": not_applicable("cabinet_or_service", SCHEMATICS_SOURCE, CORE_SOURCE),
		}
	)
	for address, label, side, button in (
		(45, "Right Flipper Power (synthetic)", "right", 82),
		(46, "Right Flipper Hold (synthetic)", "right", 82),
		(47, "Left Flipper Power (synthetic)", "left", 84),
		(48, "Left Flipper Hold (synthetic)", "left", 84),
	):
		coil = "8L25" if side == "right" else "8L24"
		items.append(
			{
				"id": f"virtual.{slug(label)}",
				"label": label,
				"kind": "virtual",
				"binding": {"group": "pinmame.output.solenoid", "device": address},
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
				"availability": "used",
				"physical": {
					"notes": f"PinMAME fabricates this state from its synthetic {side}-flipper button (switch {button}) while the game-on enable (solenoid 23) is set, because no System 6 driver declares FLIP_SOL; both of the pair assert together. There is no driver-board output behind it. The physical {side} flipper coil {coil}, part SFL-19-400/30-750-DC, is a dual-wound coil switched directly by the cabinet button through relay Z1, and its end-of-stroke contact, drawn across part of the winding, drops the power winding out mechanically. A recreation drives its {side} flipper from this pair and has no winding choice to make.",
				},
				"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, SCHEMATICS_SOURCE, BOOKLET_SOURCE, VPX_SCRIPT_SOURCE, HARNESS_FLIPPER_SOURCE),
				"spatial": not_applicable("virtual", CORE_SOURCE, CONTROLLER_SOURCE),
			}
		)
	return items


def lamp_wiring(address: int) -> dict[str, Any]:
	column = (address - 1) // 8 + 1
	row = (address - 1) % 8 + 1
	column_wire, column_connection = LAMP_COLUMNS[column]
	row_wire, row_driver, row_playfield, row_insert = LAMP_ROWS[row]
	backbox = address in BACKBOX_INSERTS
	if backbox:
		return_connection = f"{row_driver}, 9J1-{row_insert} (insert board)"
		component = f"insert {BACKBOX_INSERTS[address]} with series diode"
	else:
		return_connection = f"{row_driver}, 8P2-{row_playfield}"
		component = f"bulb 8B{address} with diode 8D{64 + address}"
	return {
		"board": "Williams System 6 driver board",
		"drive_wire": column_wire,
		"drive_connection": column_connection,
		"return_wire": row_wire,
		"return_connection": return_connection,
		"return_component": f"{component}, column {column} row {row}",
		"nominal_voltage_v": 18,
		"voltage_type": "dc",
	}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		base = {
			"binding": {"group": "pinmame.output.lamp", "device": address},
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
		}
		if address == 23:
			items.append(
				{
					"id": lamp_id(23),
					"label": "Not Used (lamp matrix column 3 row 7)",
					"kind": "lamp",
					**base,
					"availability": "unused",
					"physical": {"notes": "Printed NOT USED in Figure 6 and in the lamp sheet's bulb list, and the lamp sheet draws no bulb in column 3 row 7. The ROM lights it only during the lamp test, which flashes every matrix position (harness)."},
					"provenance": provenance(BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_GAMEPLAY_SOURCE),
					"spatial": not_applicable("unused", BOOKLET_SOURCE, SCHEMATICS_SOURCE),
				}
			)
			continue
		label, objects = LAMPS[address]
		physical: dict[str, Any] = {}
		notes: list[str] = []
		if address in BACKBOX_INSERTS:
			physical["location"] = "backbox insert board"
			notes.append(f"Backbox insert {BACKBOX_INSERTS[address]} on the insert board (schematics page 28), not on the playfield.")
		else:
			physical["location"] = "apron" if address == 56 else "playfield"
		if address in LAMP_QUANTITY:
			physical["quantity"] = LAMP_QUANTITY[address]
			if address in (62, 63, 64):
				notes.append("The insert-board sheet draws two bulbs in parallel for this insert.")
		if address in LAMP_NOTES:
			notes.append(LAMP_NOTES[address])
		if notes:
			physical["notes"] = " ".join(notes)
		refs = [BOOKLET_SOURCE, SCHEMATICS_SOURCE, CORE_SOURCE]
		if objects is not None and address != 56:
			refs.append(VPX_SCRIPT_SOURCE)
		if address == 56:
			refs += [VPX_AI_TABLE_SOURCE, IPDB_SOURCE]
		device: dict[str, Any] = {
			"id": lamp_id(address),
			"label": label,
			"kind": "lamp",
			**base,
			"availability": "used",
			"physical": physical,
			"wiring": lamp_wiring(address),
			"provenance": provenance(*refs),
		}
		if not physical:
			del device["physical"]
		if objects is None:
			device["roles"] = ["cabinet.backglass"]
			device["spatial"] = not_applicable("cabinet_or_service", SCHEMATICS_SOURCE, BOOKLET_SOURCE)
		elif address == 56:
			device["spatial"] = located(device["id"], "emitter", [normalized(objects[0])], VPX_AI_TABLE_SOURCE, IPDB_SOURCE, SCHEMATICS_SOURCE)
		else:
			device["spatial"] = located(device["id"], "emitter", [normalized(name) for name in objects], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, BOOKLET_SOURCE)
		items.append(device)
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
			"provenance": provenance(CORE_SOURCE, SCHEMATICS_SOURCE, BOOKLET_SOURCE, HARNESS_SOLENOID_SOURCE),
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, SCHEMATICS_SOURCE),
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
			[solenoid_id(1), solenoid_id(8)],
			[switch_id(9), switch_id(51), switch_id(58), switch_id(57), switch_id(46)],
			"Firepower holds its three balls on a ball ramp below the apron instead of a trough. A drained ball falls into the outhole (switch 9) below the apron centre; Ball Release (solenoid 1) kicks it up onto the ramp, where it rolls to the lowest free rest position: right (57) at the exit end, then centre (58), then left (51). Ball Ramp Thrower (solenoid 8) at the exit end throws the ball in position 57 into the shooter lane, where it rests on the Ball Shooter switch (46) until plunged; the next ball then rolls down into 57. The retained gameplay harness run shows the ROM pulsing solenoid 8 at game start with the ramp full, pulsing solenoid 1 repeatedly while switch 9 is held, and throwing the next ball once a ball returns to 57. The booklet's solenoid test tells the operator to pulse solenoid 08 three times to empty the ramp, and a new game cannot start until every ball is back on the ramp. The retained table models the ramp as a three-ball cvpmTrough with SolIn on solenoid 1 and SolOut on solenoid 8.",
			(BOOKLET_SOURCE, SCHEMATICS_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE),
			positions=[
				{"id": "mech.outhole-and-ball-ramp.right", "label": "Right (exit end)", "sensors": [switch_id(57)]},
				{"id": "mech.outhole-and-ball-ramp.center", "label": "Centre", "sensors": [switch_id(58)]},
				{"id": "mech.outhole-and-ball-ramp.left", "label": "Left", "sensors": [switch_id(51)]},
			],
		),
		m("mech.left-eject-hole", "Left eject hole", "kicker", [solenoid_id(4)], [switch_id(13)], "A kick-out hole in the left rail. While switch 13 is closed the ROM either holds the ball (locked for MULTI-BALL when the hole is flashing) or kicks it out with solenoid 4; the gameplay harness run shows repeated solenoid 4 pulses while the switch is held with the hole not locking. Locking a ball releases a new one from the ball ramp, a flashing hole or an unlit hole, in that order; locking all three balls starts MULTI-BALL.", (BOOKLET_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)),
		m("mech.right-eject-hole", "Right eject hole", "kicker", [solenoid_id(5)], [switch_id(30)], "A kick-out hole on the right below the upper right eject hole, fed by the right eject lane (star rollover 54). Kicked by solenoid 5 while switch 30 is closed, or held for MULTI-BALL as for the left hole (gameplay harness run).", (BOOKLET_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)),
		m("mech.upper-right-eject-hole", "Upper right eject hole", "kicker", [solenoid_id(6)], [switch_id(36)], "A kick-out hole in the top right corner at the end of the right orbit, kicked by solenoid 6 while switch 36 is closed or held for MULTI-BALL (gameplay harness run).", (BOOKLET_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)),
		m("mech.left-ball-saver-kicker", "Left ball saver kicker", "kicker", [solenoid_id(7)], [switch_id(10)], "An outlane kickback at the foot of the left outlane. When the Ball Saver Kicker On lamp (2) is lit, the ROM fires solenoid 7 as the ball rolls over the left outside rollover (switch 10) and turns lamp 2 off; with lamp 2 unlit nothing fires. The retained kicker harness run shows exactly this: a control closure of 10 with lamp 2 off, then targets 1-3 made on the same ball light lamp 2, and the next closure of 10 pulses solenoid 7 and clears lamp 2. Which feat lights the kicker is an operator adjustment (booklet Table 1): POWER targets, 1-3 or 4-6 on one ball, or spotting 1-6.", (BOOKLET_SOURCE, HARNESS_KICKER_SOURCE, SCHEMATICS_SOURCE)),
	]
	for coil_address, switch_address, label in (
		(17, 26, "Top left jet bumper"),
		(18, 25, "Bottom left jet bumper"),
		(19, 27, "Top right jet bumper"),
		(20, 28, "Bottom right jet bumper"),
	):
		special = SOLENOIDS[coil_address]["special"][0]
		items.append(
			m(
				f"mech.{slug(label)}",
				label,
				"other",
				[solenoid_id(coil_address)],
				[switch_id(switch_address)],
				f"A jet bumper fired directly by its own special switch {special} through the driver board's special solenoid circuit, independent of the ROM's matrix scan, while the game-on enable is set; the matrix switch {switch_address} is the bumper's separate scoring contact. PinMAME publishes special solenoid {coil_address} whenever switch {switch_address} closes during play, and the gameplay harness run shows exactly that.",
				(SCHEMATICS_SOURCE, BOOKLET_SOURCE, HARNESS_GAMEPLAY_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	for coil_address, switch_address, label in ((22, 12, "Left kicker (slingshot)"), (21, 42, "Right kicker (slingshot)")):
		special = SOLENOIDS[coil_address]["special"][0]
		items.append(
			m(
				f"mech.{slug(label)}",
				label,
				"kicker",
				[solenoid_id(coil_address)],
				[switch_id(switch_address)],
				f"A slingshot above the flipper, fired by its special switch {special} through the driver board while the game-on enable is set; matrix switch {switch_address} is its 10-point scoring contact. PinMAME publishes solenoid {coil_address} whenever switch {switch_address} closes during play (gameplay harness run).",
				(SCHEMATICS_SOURCE, BOOKLET_SOURCE, HARNESS_GAMEPLAY_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)
	items += [
		m(
			"mech.right-flipper",
			"Right flipper",
			"other",
			["virtual.right-flipper-power-synthetic", "virtual.right-flipper-hold-synthetic"],
			["switch.right-flipper-button", switch_id(45)],
			"One lower right flipper, coil 8L25 (SFL-19-400/30-750-DC), switched by the cabinet button 7SW72 through relay Z1 and enabled only while the game-on enable (solenoid 23) is set. Pressing it also closes the LANE CHANGE switch 45, which the ROM uses to rotate the lit F-I-R-E lane lamps one lane (gameplay harness run: lamp 5 off, lamp 6 on). In PinMAME the consumer drives synthetic button 82; PinMAME copies it into switch 45 and fabricates outputs 45 and 46.",
			(SCHEMATICS_SOURCE, BOOKLET_SOURCE, CORE_SOURCE, HARNESS_GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE),
		),
		m(
			"mech.left-flipper",
			"Left flipper",
			"other",
			["virtual.left-flipper-power-synthetic", "virtual.left-flipper-hold-synthetic"],
			["switch.left-flipper-button"],
			"One lower left flipper, coil 8L24 (SFL-19-400/30-750-DC), switched by the cabinet button 7SW73 through relay Z1 and enabled only while the game-on enable is set. The ROM cannot read the left button. In PinMAME the consumer drives synthetic button 84 and PinMAME fabricates outputs 47 and 48.",
			(SCHEMATICS_SOURCE, BOOKLET_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
		),
	]
	return items


def relationships() -> list[dict[str, Any]]:
	items = []
	for coil_address in range(17, 23):
		matrix = SOLENOIDS[coil_address]["special"][3]
		items.append(
			{
				"id": f"relationship.scoring-switch-{matrix}-publishes-solenoid-{coil_address}",
				"kind": "direct",
				"source": switch_id(matrix),
				"destination": solenoid_id(coil_address),
				"provenance": provenance(CORE_SOURCE, HARNESS_GAMEPLAY_SOURCE),
			}
		)
	for destination in ("virtual.right-flipper-power-synthetic", "virtual.right-flipper-hold-synthetic", "virtual.left-flipper-power-synthetic", "virtual.left-flipper-hold-synthetic"):
		items.append(
			{
				"id": f"relationship.game-on-gates-{destination.split('.', 1)[1]}",
				"kind": "relay_gated",
				"source": "relay.game-on-flipper-enable",
				"destination": destination,
				"provenance": provenance(CORE_SOURCE, SCHEMATICS_SOURCE),
			}
		)
	items.append(
		{
			"id": "relationship.right-flipper-button-drives-lane-change-switch",
			"kind": "direct",
			"source": "switch.right-flipper-button",
			"destination": switch_id(45),
			"provenance": provenance(CORE_SOURCE, CONTROLLER_SOURCE, HARNESS_FLIPPER_SOURCE),
		}
	)
	return items


def excerpt(identifier: str, name: str, locator: str) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier,
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}",
		"sha256": EXCERPT_DIGESTS[name],
		"method": "manual",
		"transcribed_by": "curator, read from rendered pages",
		"reviewed": True,
	}
	if name in EXCERPT_IMAGES:
		digest, derivation = EXCERPT_IMAGES[name]
		record.update({"image": f"evidence/excerpts/{MACHINE_ID}/{name.removesuffix('.md')}.webp", "image_sha256": digest, "image_derivation": derivation})
	return record


def harness_locator(name: str, description: str, game: str = "frpwr_l6") -> str:
	run_sha, scenario, scenario_sha, init_sha = HARNESS_RUNS[name]
	init_scenario, rom = HARNESS_BOOT[game]
	return (
		f"LibPinMAME harness run of {game} with tools/run_pinmame_harness.py, library pinmame64.dll built from "
		f"the pinned PinMAME revision (SHA-256 {LIBRARY_SHA256}), ROM archive {game}.zip from the operator's "
		f"authorized ROM corpus (SHA-256 {rom}, CRCs matching the pinned driver), in an isolated state directory. "
		f"Scenario tools/harness-scenarios/system-6/{scenario} (SHA-256 {scenario_sha}). A first power-up from "
		"empty CMOS stops on the game-identification/audit screen, so every evidentiary run starts from a state "
		f"directory initialized by exactly one prior empty-NVRAM boot (scenario SHA-256 {init_scenario}, raw run "
		f"SHA-256 {init_sha}). {description} The whole run directory is pinned by "
		f"external:pinmame-runtime-evidence/firepower-1980.manifest.json ({RUNTIME_MANIFEST[0]} files, {RUNTIME_MANIFEST[1]} bytes, "
		f"manifest SHA-256 {RUNTIME_MANIFEST[2]}). No ROM bytes or NVRAM blobs are retained in this repository."
	)


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the System 6 members of the frpwr_l6 clone tree: frpwr_l6, frpwr_l2, frpwr_l6ff, frpwr_l2ff, frpwr_t6, frpwr_t6ff, frpwr_a6, frpwr_d6, frpwr_b6 and frpwr_c6",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s6games.c 'Firepower - Sys.6 (Game #497)': INITGAMEFULL(frpwr_l6, s6_6digit_disp, 0, 45, 26, 25, "
				"27, 28, 42, 12), which expands to core_tGameData {GEN_S6, s6_6digit_disp, {FLIP_SWNO(0,45)}, NULL, {{0}}, "
				"{0, {26, 25, 27, 28, 42, 12}}} - no left flipper matrix switch, the right-flipper button copied into switch "
				"45, a zero inverted-switch mask, and special solenoids 17-22 fired by switches 26, 25, 27, 28, 42 and 12 - "
				"with the same INITGAMEFULL line for every System 6 Firepower driver and fp_7digit_disp (player displays at "
				"memory positions 0, 7, 20 and 27, seven digits, and the two-digit left and right side entries at 34 and 14) "
				"for frpwr_b6 and frpwr_c6; src/wpc/s6.c (PIA wiring, setSSSol, s6_gameon_w, s6_vblank's ssSw loop and "
				"CORE_SSFLIPENSOL, s6_dips_r, SWITCH_UPDATE(s6), s6_6digit_disp); src/wpc/s6.h (S6_COMPORTS DIP and "
				"diagnostic ports); src/wpc/core.c (core_swSeq2m, core_updateSw, core_getSol); src/wpc/core.h; "
				"src/wpc/wmssnd.c (sound DIP bits); src/wpc/core.c layoutAlphanumericFrame (the extra 128x32 layout "
				"frame is a rendering aid, not a machine display)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/system-6.json",
			"revision": "repository",
			"locator": "Williams System 6 public address rules: sequential switch matrix 1-64, diagnostics -7 to -3, synthetic flipper buttons 81-88, DIP addressing bank * 8 + bit + 1, solenoids 1-23 with the game-on enable at 23, synthetic flipper outputs 45-48, lamps 1-64 and no GI channel",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": BOOKLET_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/856/Williams_1980_Firepower_Instruction_Booklet.pdf",
			"original_filename": "Williams_1980_Firepower_Instruction_Booklet.pdf",
			"sha256": BOOKLET_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": (
				"Instruction Booklet 16P-497-103, Game No. 497, January 1980, twelve pages, 600 dpi colour scan hosted by "
				"IPDB (retrieved through the Internet Archive's Wayback Machine copy of 2026-01-08 because IPDB is "
				"Cloudflare-gated; retained at external:pinmame-manuals/by-machine/williams.firepower.1980/). Page 1 board "
				"requirements, pages 1-3 game operation, bookkeeping and diagnostics, page 7 the Master Command switch, "
				"page 8 Figure 3 solenoid locations and chart, page 9 Table 3 solenoid connections, page 10 Figure 4 switch "
				"locations and chart, page 11 Figure 5 switch matrix, page 12 Figure 6 lamp matrix."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [
				excerpt("excerpt.firepower.switch-matrix", "switch-matrix.md", "PDF page 11, Figure 5. Switch Matrix, all 64 cells"),
				excerpt("excerpt.firepower.lamp-matrix", "lamp-matrix.md", "PDF page 12, Figure 6. Lamp Matrix, all 64 cells"),
				excerpt("excerpt.firepower.solenoid-connections", "solenoid-connections.md", "PDF page 9, Table 3. Solenoid Connections and its notes"),
				excerpt("excerpt.firepower.switch-locations", "switch-locations.md", "PDF page 10, Figure 4. Playfield Switch Locations and Switch Chart, with the drawing's registration against the retained table"),
				excerpt("excerpt.firepower.solenoid-locations", "solenoid-locations.md", "PDF page 8, Figure 3. Playfield Solenoid Locations and Solenoid Chart"),
				excerpt("excerpt.firepower.operation-and-diagnostics", "operation-and-diagnostics.md", "PDF pages 1, 2, 3 and 7: board requirements, game operation, bookkeeping, diagnostic procedures and the Master Command switch"),
			],
		},
		{
			"id": BOOKLET_ALT_SOURCE,
			"kind": "manual",
			"uri": "https://archive.org/details/arcademanual_Firepower_OPS",
			"source_id": "arcademanual_Firepower_OPS",
			"original_filename": "Firepower_OPS.pdf",
			"sha256": BOOKLET_ALT_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": "Internet Archive item arcademanual_Firepower_OPS, uploaded 2017-09-20 by manuallibrary@textfiles.com, file Firepower_OPS.pdf (400 dpi 1-bit scan, 'Scanned by www.gamearchive.com', 1999). A different printing of the same instruction booklet: its tables and figures agree with the IPDB copy cell for cell, and its game-operation text says 'targets' where the IPDB copy says 'drop targets'. Used as a cross-check of the IPDB copy.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan by gamearchive.com via the Internet Archive",
			"rights": "NOASSERTION",
		},
		{
			"id": SCHEMATICS_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/856/Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf",
			"original_filename": "Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf",
			"sha256": SCHEMATICS_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": "28-page 600 dpi scan of the schematics section of the March 1980 Firepower game manual, every sheet marked 497, hosted by IPDB (retrieved through the Wayback Machine). Page 15 sound board logic (16D-8224), page 23 power wiring, page 24 cabinet wiring, page 25 playfield solenoid wiring, page 26 playfield switch wiring, page 27 playfield lamp wiring, page 28 insert board and master display wiring.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [
				excerpt("excerpt.firepower.playfield-solenoid-wiring", "playfield-solenoid-wiring.md", "PDF page 25, Playfield Solenoid Wiring Diagram"),
				excerpt("excerpt.firepower.playfield-switch-wiring", "playfield-switch-wiring.md", "PDF page 26, Playfield Switch Wiring Diagram"),
				excerpt("excerpt.firepower.playfield-lamp-wiring", "playfield-lamp-wiring.md", "PDF page 27, Playfield Lamp Wiring Diagram"),
				excerpt("excerpt.firepower.cabinet-wiring", "cabinet-wiring.md", "PDF page 24, Cabinet Wiring Diagram"),
				excerpt("excerpt.firepower.insert-board-wiring", "insert-board-wiring.md", "PDF page 28, Insert Board Wiring Diagram and master display"),
				excerpt("excerpt.firepower.power-wiring", "power-wiring.md", "PDF page 23, Power Wiring Diagram"),
				excerpt("excerpt.firepower.sound-board-ds1", "sound-board-ds1.md", "PDF page 15, Sound Board Logic Diagram: the sound/speech select input and option switch DS1"),
			],
		},
		{
			"id": BULLETIN_SOURCE,
			"kind": "service_bulletin",
			"uri": "https://www.ipdb.org/files/856/Williams_1980_Firepower_Service_Bulletin_SS20_no_date_wiring_change_for_production_and_test_games.pdf",
			"original_filename": "Williams_1980_Firepower_Service_Bulletin_SS20_no_date_wiring_change_for_production_and_test_games.pdf",
			"sha256": BULLETIN_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": "Williams Service Bulletin SS 20, two pages, undated: the Flash lamp circuit ground on Firepower production and test games.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
			"rights": "NOASSERTION",
			"excerpts": [excerpt("excerpt.firepower.service-bulletin-ss20", "service-bulletin-ss20.md", "Both pages: the WIRING CHANGE paragraph and the FIREPOWER Test Games section")],
		},
		{
			"id": PROTOTYPE_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/files/856/Williams_1980_Firepower_Prototype_Drop_Targets_Info.txt",
			"original_filename": "Williams_1980_Firepower_Prototype_Drop_Targets_Info.txt",
			"sha256": PROTOTYPE_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": "Ted Estes, 'Firepower drop target retrofit', rec.games.pinball, 22 May 1995, as hosted by IPDB. Secondary source, used only to explain the prototype origin of unused solenoids 2-3 and unused switches 20, 24, 52 and 55.",
			"license": "NOASSERTION",
			"attribution": "Edward (Ted) Estes; hosted by the Internet Pinball Database",
			"excerpts": [excerpt("excerpt.firepower.prototype-drop-targets", "prototype-drop-targets.md", "The drop-target wiring steps and the prototype history")],
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=856",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-09-25T00:00:00Z",
			"locator": "IPDB machine 856: Firepower, Williams Electronics, February 1980, model number 497, Williams System 6, 17,410 units, design Steve Ritchie, software and sound Eugene Jarvis; notable features 'Flippers (2), Pop bumpers (4), Slingshots (2), Standup targets (10), Kick-out holes (3), Star rollovers (2), Spinning target (1), Left outlane kickback, 3-ball multiball, Speech', first Lane Change and first electronic multiball, the ten drop-target prototypes. Retrieved through the Wayback Machine capture of 2026-01-08 (retained page SHA-256 above); playfield photographs image-28 and image-31 show the apron's round credit window to the left of the left flipper, retained at external:pinmame-review-artifacts/firepower-1980/ipdb-images/.",
			"license": "NOASSERTION",
			"attribution": "The Internet Pinball Database",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/firepower-1980/source/Firepower (Williams 1980).vpx",
			"original_filename": "Firepower (Williams 1980).vpx",
			"sha256": TABLE_SHA256,
			"revision": "V1.0",
			"locator": f"Community recreation by 3rdaxis, Slydog43 & G5K, version V1.0, release date 12-06-2018, from the operator's table archive. Exact playfield bounds {TABLE_BOUNDS}; normalized coordinates are x/952 and y/1974. Geometry authority for named objects. A normalized candidate dump is retained at external:pinmame-review-artifacts/firepower-1980/vpx-spatial-candidates.json (SHA-256 {GEOMETRY_CANDIDATES_SHA256}).",
			"license": "NOASSERTION",
			"attribution": "3rdaxis, Slydog43 & G5K",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-williams-1980-v1.0/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Embedded script of the retained table, 135,191 bytes. Const cGameName=\"frpwr_b7\" with S6.VBS and "
				"UseSolenoids=25 (the frpwr_b7 game-on address; this record's System 6 drivers publish game-on at 23). Runtime authority for: the SolCallback table (1 trTrough.SolIn, 4/5/6 eject holes, 7 "
				"BallSaveKick, 8 trTrough.SolOut, 14 knocker, 15 Flashers, 21/22 slingshots, sLRFlipper/sLLFlipper); "
				"switch constants 9-58; the three-ball cvpmTrough with entry switch 9 and addsw 2, 1, 0 = 51, 58, 57; "
				"vpmMapLights AllLights, which binds each light to its TimerInterval lamp number, plus Set Lights(26..31) "
				"and Set Lights(44..47). Known defects not followed: all eight StandupTarget handlers pulse switch 48 (the table has walls for seven of them; StandupTarget8 has no object); "
				"BallSaveKick only plays a sound while the table kicks locally from its own lamp copy; lamp 56 is not "
				"modelled."
			),
			"license": "NOASSERTION",
			"attribution": "3rdaxis, Slydog43 & G5K",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-williams-1980-v1.0.manifest.json",
			"locator": _extraction_locator("firepower-williams-1980-v1.0"),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPX_AI_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/firepower-1980/source/FirePower(Vs A.I.)V3.4.2.vpx",
			"original_filename": "FirePower(Vs A.I.)V3.4.2.vpx",
			"sha256": AI_TABLE_SHA256,
			"revision": "V3.4.2",
			"locator": f"The 'FirePower (Vs A.I.)' revision of the same table by 3rdaxis, rothbauerw, Slydog43 & G5K (table_version V3.4.0 in its metadata, file V3.4.2), bounds {TABLE_BOUNDS}. Same lineage as the base table, so not independent geometry; used for the apron credit lamp CreditLight1 (TimerInterval 56), which the base table lacks, and as corroboration for standup 49, whose wall (StandupTarget8, drag-point centroid (0.111636, 0.369892), pulsing 48 like every standup wall) the base table also lacks. Extraction manifest external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-vs-ai-v3.4.2.manifest.json ({_extraction_summary('firepower-vs-ai-v3.4.2')}); candidate dump SHA-256 {GEOMETRY_AI_CANDIDATES_SHA256}.",
			"license": "NOASSERTION",
			"attribution": "3rdaxis, rothbauerw, Slydog43 & G5K",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_AI_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/firepower-vs-ai-v3.4.2/script.vbs",
			"original_filename": "script.vbs",
			"sha256": AI_SCRIPT_SHA256,
			"locator": "Embedded script of the Vs A.I. revision, 179,787 bytes, cGameName frpwr_b7. Cited only for its direct Controller.Switch(82)/(84) flipper-button writes and lamp 56 binding.",
			"license": "NOASSERTION",
			"attribution": "3rdaxis, rothbauerw, Slydog43 & G5K",
			"rights": "NOASSERTION",
		},
		{
			"id": THAL_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/FirePower%20%28Williams%201980%29%201.1_Thal_Mod.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": THAL_SCRIPT_SHA256,
			"locator": "Pinned corpus script 'FirePower (Williams 1980) 1.1_Thal_Mod.vbs', cGameName frpwr_c7, an earlier table whose geometry is not retained. Cited only because it binds each 50-point standup to its own switch address (UpperMiddleLeftStandup 14, TopLeftStandup 16, LowerTopRightStandup 37, MiddleRightStandup 38, LowerRightStandup 48, CenterMIddleLeftStandup 49, LowerMIddleLeftStandup 50), where the retained tables pulse 48 from all of them.",
			"license": "NOASSERTION",
			"attribution": "Community table authors; pinned copy in sverrewl/vpxtable_scripts",
		},
		{
			"id": GEOMETRY_SOURCE,
			"kind": "human_review",
			"uri": f"internal:evidence/excerpts/{MACHINE_ID}/switch-locations.md",
			"revision": "repository",
			"locator": f"Registration of the booklet's Figure 4 onto the retained table frame: ten control points, a least-squares affine fit with 21.1 table-unit RMS residual, identity reading of every callout, and the derived two-decimal coordinates for the outhole, playfield tilt, lane-change switch, the three ball-ramp positions and standup 49. It also records which StandupTarget wall is which standup (1=16, 2=31, 3=37, 4=14, 5=48, 6=50, 7=38). World-space primitive bounds for the POWER and top centre targets are retained at external:pinmame-review-artifacts/firepower-1980/primitive-world-bounds.json (SHA-256 {PRIMITIVE_BOUNDS_SHA256}).",
			"license": "MIT",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_SOLENOID_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-sol.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-sol.json"][0],
			"locator": harness_locator("run-sol.json", "The ROM's own Test 02 pulses public solenoids 1 to 22 in order, each for about a second per Advance, while the ball-in-play display (PinMAME display index 5, memory positions 6-7) shows the same number and the credit display (index 4, positions 14-15) shows 02; public 23 asserts on entering the test. It also shows the attract mode flashing solenoid 15 and energizing 16 at power-up, and the lamp test lighting all 64 lamp addresses."),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_SWITCH_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-sw.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-sw.json"][0],
			"locator": harness_locator("run-sw.json", "Test 03 (switch test): closing each public switch 1 to 58 alone makes the ball-in-play display show that number, with no stuck switch reported at rest, so every matrix switch reads 1 when closed and 0 open with no inversion; closing 59 to 64 is never reported."),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_GAMEPLAY_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-play.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-play.json"][0],
			"locator": harness_locator("run-play.json", "With switches 51, 58 and 57 closed: a coin on switch 4 pulses the knocker (14); the credit button (3) asserts 23, pulses 2 and 3 once and throws with 8; switch 32 lights lamp 5 and switch 45 moves it to lamp 6; switches 12, 42, 26, 25, 27 and 28 each publish 22, 21, 17, 18, 19 and 20; holding 13, 30 and 36 draws repeated pulses of 4, 5 and 6; holding 9 draws repeated pulses of 1; closing 57 again throws with 8. Lamp 23 is never lit outside the lamp test."),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_KICKER_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-kick.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-kick.json"][0],
			"locator": harness_locator("run-kick.json", "In play, switch 10 with lamp 2 off fires nothing; the three POWER targets light the POWER insert and inside rollovers but not lamp 2 at factory settings; targets 17, 18 and 19 on the same ball light lamp 2 and pulse solenoid 2; the next closure of 10 pulses solenoid 7 and turns lamp 2 off."),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_FLIPPER_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-flip.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-flip.json"][0],
			"locator": harness_locator("run-flip.json", "The scenario never writes public switch 45. After a started game lights lamp 5 from the F rollover (32), pressing the right cabinet button (synthetic 82) pulses outputs 45 and 46 and moves the lit lamp from 5 to 6; pressing the left button (84) pulses 47 and 48 and changes no lamp; pressing 82 again pulses 45 and 46 and moves the lamp from 6 to 7."),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_B6_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-b6.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-b6.json"][0],
			"locator": harness_locator("run-b6.json", "The gameplay causality sequence on the Oliver System 6 seven-digit conversion frpwr_b6 (fp_7digit_disp): the coin credit appears on display index 4 (memory position 34) as 01 and returns to 00 when the credit button starts the game, while display index 5 (position 14) then shows ball 1; the special-solenoid pairs, eject-hole kicks, outhole kick and ball-ramp throw match the frpwr_l6 run.", game="frpwr_b6"),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": HARNESS_C6_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-c6.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-c6.json"][0],
			"locator": harness_locator("run-c6.json", "The same sequence on frpwr_c6 (revision 31): credit 01 on display index 4 (position 34) after the coin, ball 1 on index 5 (position 14) after the start, and the same special-solenoid pairs.", game="frpwr_c6"),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
	]


def _extraction_summary(directory: str) -> str:
	count, total, digest = EXTRACTIONS[directory]
	return f"{count} files, {total} bytes, manifest SHA-256 {digest}"


def _extraction_locator(directory: str) -> str:
	return (
		"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under "
		f"extracted-vpxtool/{directory}: {_extraction_summary(directory)}, produced with vpxtool git:v0.33.3 "
		f"from the retained table. Bounds {TABLE_BOUNDS}."
	)


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
		if driver_id in SEVEN_DIGIT_DRIVERS:
			item["display_overrides"] = [
				{"target": target, "segment_start": start, "width": width, "provenance": provenance(CORE_SOURCE, SEVEN_DIGIT_DRIVERS[driver_id])}
				for target, (start, width) in SEVEN_DIGIT_OVERRIDES.items()
			]
		items.append(item)
	return items


def conversion_drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
	for driver_id in sorted(CONVERSION_DRIVER_IDS):
		record = by_id[driver_id]
		item: dict[str, Any] = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		item["variant_notes"] = CONVERSION_DRIVER_NOTES[driver_id]
		items.append(item)
	return items


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Firepower",
			"manufacturer": "Williams",
			"year": 1980,
			"kind": "physical_pinball",
			"model_number": "497",
			"ipdb_id": 856,
			"opdb_id": "G5VDd-MJpqO",
			"playfield": {
				"units": "vpx",
				"width": PLAYFIELD_WIDTH,
				"height": PLAYFIELD_HEIGHT,
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
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
		"controller": {
			"platform": "pinmame.system-6",
			"hardware_generation": "0x20000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/firepower-1980.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Firepower device identifiers are not unique: {duplicates}")
	return definition


CONVERSION_MISSING = [
	"identity",
	"controller_platform",
	"input_enumeration",
	"input_semantics",
	"output_enumeration",
	"output_semantics",
	"display_inventory",
	"mechanism_inventory",
	"mechanism_behavior",
	"polarity",
	"variant_differences",
	"recreation_notes",
	"provenance",
	"spatial_placement",
]


def conversion_source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the Oliver System 7 Firepower conversions: frpwr_a7, frpwr_d7 and frpwr_e7 (roots of their own) and frpwr_b7 and frpwr_c7 (clones of frpwr_l6)",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s7games.c 'Firepower - Sys.7': every driver declares machine driver s7_mS7S6 (GEN_S7 CPU board "
				"with the System 6 sound board) and INITGAMEFULL(name, disp, 0, 45, 11774, 26, 25, 27, 28, 42, 12) with "
				"s7_6digit_disp for frpwr_a7/e7 and fp_7digit_disp for frpwr_b7/d7 (frpwr_c7 reuses frpwr_b7's init); "
				"src/wpc/s7.h S7_GAMEONSOL 25 and the -7..-3 diagnostic inputs; src/wpc/s7.c s7_vblank (game-on at 25 and "
				"an eight-entry sxx.ssSw loop), the PIA CA2/CB2 handlers that map ROM-fired special solenoids through "
				"setSSSol slots 0-7 (pia2cb2 0, pia2ca2 1, pia4cb2 2, pia4ca2 3, pia1ca2 4, pia3cb2 5, pia0cb2 6, "
				"pia0ca2 7), and s7_dips_r, whose body matches s6_dips_r (both banks, by strobe position, while -3 is held)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": HARNESS_SYS7_SOURCE,
			"kind": "runtime_scenario",
			"uri": "external:pinmame-runtime-evidence/firepower-1980/run-b7.json",
			"revision": PINMAME_REVISION,
			"sha256": HARNESS_RUNS["run-b7.json"][0],
			"locator": harness_locator("run-b7.json", "The frpwr_l6 gameplay causality sequence run on the Oliver System 7 conversion frpwr_b7: the game-on enable asserts at public 25, the coin credit appears on display index 4 (fp_7digit_disp position 34) and the ball number on index 5, and closing matrix switches 26, 25, 27, 28, 42 and 12 publishes 17-22 in order. That special-solenoid pairing is PinMAME's switch-driven sxx.ssSw path, which is sequential by construction; the run never makes the ROM fire a special solenoid itself, reaches no service test and reads no DIP switch.", game="frpwr_b7"),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
	]


def build_conversion() -> dict[str, Any]:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": CONVERSION_ID,
			"name": "Firepower",
			"manufacturer": "Williams / Oliver",
			"year": 1980,
			"kind": "physical_conversion",
			"ipdb_id": 856,
			"opdb_id": "G5VDd-MJpqO",
		},
		"coverage": {
			"status": "partial",
			"missing": list(CONVERSION_MISSING),
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "unknown",
				"semantic_naming": "unknown",
				"physical_wiring": "unknown",
				"mechanisms": "unknown",
				"variant_coverage": "candidate",
				"recreation_knowledge": "candidate",
				"spatial_placement": "unknown",
			},
		},
		"drivers": conversion_drivers(),
		"inputs": [],
		"outputs": [],
		"displays": [],
		"mechanisms": [],
		"relationships": [],
		"sources": conversion_source_records(),
		"knowledge": {"path": CONVERSION_KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "partial"},
		"conflicts": [],
	}


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
		if "drawing" in spec and spec.get("standup"):
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Registered from the booklet's Figure 4 callout ({spec['drawing']}); the base table has no wall for this standup. The Vs A.I. revision's StandupTarget8 wall at (0.111636, 0.369892) corroborates it to within 0.01. Two-decimal precision."})
		elif "drawing" in spec:
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Registered from the booklet's Figure 4 callout ({spec['drawing']}); the retained table has no object for this device. Two-decimal precision."})
		elif spec.get("obj") in ("LeftSlingShot", "RightSlingShot"):
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Drag-point centroid of the retained {spec['obj']} wall, whose _Slingshot handler pulses this address; the contact sits behind the rubber."})
		elif spec.get("standup"):
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Drag-point centroid of the retained {spec['obj']} wall, identified as this standup by the registered Figure 4 callouts (the table's own handler pulses 48 for every standup wall)."})
		elif spec.get("power") or spec.get("obj") == "TopTarget_6":
			projections.append({"group": "pinmame.input.switch", "address": address, "reason": f"Centre of the world-space mesh bounds of the retained {spec['obj']} primitive."})
	projections += [
		{"group": "pinmame.output.solenoid", "address": 1, "reason": "Ball Release sits with the outhole below the apron; placed at the registered Figure 4 outhole callout, which Figure 3's callout 01 matches."},
		{"group": "pinmame.output.solenoid", "address": 8, "reason": "Ball Ramp Thrower sits at the exit end of the ball ramp below the apron; placed on the retained trough's exit kicker BallRelease, which throws into the shooter lane."},
	]
	for address in (17, 18, 19, 20, 21, 22):
		projections.append({"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto the retained {SOLENOIDS[address]['place'][1]} object the coil drives."})
	return {
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "validated and promoted to machines/author-ready/williams/firepower-1980.json",
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifests": {
				directory: {"file_count": count, "total_bytes": total, "manifest_sha256": digest}
				for directory, (count, total, digest) in sorted(EXTRACTIONS.items())
			},
			"source_ref": VPX_EXTRACTION_SOURCE,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"instruction_booklet_sha256": BOOKLET_SHA256,
			"schematics_sha256": SCHEMATICS_SHA256,
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"vs_ai_table_sha256": AI_TABLE_SHA256,
			"geometry_candidates_sha256": GEOMETRY_CANDIDATES_SHA256,
			"primitive_bounds_sha256": PRIMITIVE_BOUNDS_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(resolved_inputs),
		"resolved_output_bindings": sorted(resolved_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(bindings, key=lambda item: (item["group"], item["address"])) for reason, bindings in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=lambda item: (item["group"], item["address"])) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": projections,
		"excluded_object_classes": [
			"ComboTrigger1-4, invisible triggers between the six 1-6 targets that pulse two adjacent target switches at once; a table aid for shots that strike two targets, not a device.",
			"B1T1-B4T8, rings of invisible triggers around the jet bumpers used only for the table's animation.",
			"StandupTarget walls' own switch number: all eight handlers pulse 48, so their identity comes from Figure 4 rather than the script.",
			"Drain, the retained trough's entry kicker on the table's bottom edge; the outhole placement is the booklet's registered callout instead.",
			"LBlueTopB/LBlueMiddleB/LBlueBottomB, LBumper*B and LBackHole1, co-located bloom and halo copies of bound lights.",
			"GI_* lights: general illumination is an unswitched 6.3 VAC supply with no controller address.",
			"All backglass Light, Flasher and Reel objects, which render the backbox and score displays.",
		],
		"unresolved": [],
		"visual_review_cache": [
			"external:pinmame-manuals/by-machine/williams.firepower.1980/render/",
			"external:pinmame-review-artifacts/firepower-1980/",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Firepower (Williams, 1980) spatial audit",
		"",
		f"Status: {report['status']}.",
		"",
		f"The coordinate source is the retained `Firepower (Williams 1980).vpx` V1.0 by 3rdaxis, Slydog43 & G5K at SHA-256 `{TABLE_SHA256}`, bounds `{TABLE_BOUNDS}`, so every coordinate is x/952 and y/1974 rounded to at most six places. The flipper pivots land at y 0.827, the shooter-lane switch at 0.885 and the table's drain at 0.988, which is the check that the y divisor is right.",
		"",
		"## Evidence decisions",
		"",
		"- Every table object used was identified against the booklet's own location drawings (Figure 3 for coils, Figure 4 for switches) rather than taken from the script alone, because the script has one systematic binding defect: every StandupTarget handler pulses switch 48 (eight handlers, seven walls in the base table). Figure 4 was registered onto the table frame with ten control points (RMS 21.1 table units, about 0.02 of the width) and the seven walls resolved to standups 16, 31, 37, 14, 48, 50 and 38.",
		"- Seven hidden devices have no table object and take the registered Figure 4 callout at two decimals: the outhole (9), the playfield tilt (47), the lane-change switch (45), the three ball-ramp positions (51, 58, 57) and standup 49. The base table has no wall for 49; the Vs A.I. revision's StandupTarget8 wall sits at (0.1116, 0.3699), within 0.01 of the registered callout, and corroborates it.",
		"- The three POWER targets and the top centre target are collidable primitives whose stored position is a local offset; their placements are the centres of their world-space mesh bounds from `vpxtool export obj --units vpu`.",
		"- Lamp placements are the table's Light objects bound by `vpmMapLights` (TimerInterval = lamp number) and its explicit `Set Lights()` lines. Lamps 3 and 4 have two bulbs each, as Figure 6's `(x2)` says. Lamp 56, the playfield credit lamp, is modelled only by the Vs A.I. revision (CreditLight1, behind the apron's credit window, which IPDB's playfield photographs show).",
		"- Solenoid 15 has two emitters, the two Type 89 flash lamps under the FIRE and POWER inserts, matching Figure 3's two callouts.",
		"- Backbox lamps 50-55 and 57-64, the knocker (14), the coin lockout (16), the game-on relay (23), all cabinet and service switches, the DIPs and the displays take controlled not_applicable records.",
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
	]
	for directory, (count, total, digest) in sorted(EXTRACTIONS.items()):
		lines.append(f"- Extraction manifest `external:pinmame-vpx-sources/williams/firepower-1980/extracted-vpxtool/{directory}.manifest.json`, SHA-256 `{digest}`, {count} files, {total} bytes.")
	lines += [
		f"- Candidate geometry dump `external:pinmame-review-artifacts/firepower-1980/vpx-spatial-candidates.json`, SHA-256 `{GEOMETRY_CANDIDATES_SHA256}`.",
		f"- Primitive world bounds `external:pinmame-review-artifacts/firepower-1980/primitive-world-bounds.json`, SHA-256 `{PRIMITIVE_BOUNDS_SHA256}`.",
		f"- Transcribed excerpts and crops under `evidence/excerpts/{MACHINE_ID}/`.",
		"",
	]
	return "\n".join(lines)


def build_knowledge() -> str:
	return KNOWLEDGE_NOTE


def build_conversion_knowledge() -> str:
	return CONVERSION_KNOWLEDGE_NOTE


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Firepower retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Firepower extractions")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifests(source_root: Path) -> None:
	for directory, (count, total, digest) in EXTRACTIONS.items():
		manifest_path = source_root / EXTRACTION_ROOT / f"{directory}.manifest.json"
		if not manifest_path.is_file():
			raise RuntimeError(f"Firepower extraction manifest is missing: {manifest_path}")
		actual = load_json(manifest_path)
		expected = build_extraction_manifest(source_root / EXTRACTION_ROOT / directory)
		if canonical_bytes(actual) != canonical_bytes(expected):
			raise RuntimeError(f"Firepower extraction manifest does not match the files under {directory}")
		identity = (len(actual["files"]), sum(int(item["size"]) for item in actual["files"]), hashlib.sha256(canonical_bytes(actual)).hexdigest())
		if identity != (count, total, digest):
			raise RuntimeError(f"Firepower extraction identity mismatch for {directory}: {identity}")


def write_extraction_manifests(source_root: Path) -> None:
	for directory in EXTRACTIONS:
		manifest = build_extraction_manifest(source_root / EXTRACTION_ROOT / directory)
		write_json(source_root / EXTRACTION_ROOT / f"{directory}.manifest.json", manifest)
		print(directory, len(manifest["files"]), sum(item["size"] for item in manifest["files"]), hashlib.sha256(canonical_bytes(manifest)).hexdigest())


KNOWLEDGE_NOTE = """# Firepower (Williams, 1980) - recreation knowledge

Williams game number 497, February 1980, Williams System 6, four players, three-ball MULTI-BALL,
designed by Steve Ritchie with software and sound by Eugene Jarvis (IPDB 856). It is the first game
with LANE CHANGE and the first with electronic multiball. The physical release year is taken from
the machine's own instruction booklet (16P-497-103, January 1980), the March 1980 schematics and
IPDB; pinned PinMAME dates every Williams driver 1980.

## Reading the driver declaration

`src/wpc/s6games.c` declares every System 6 Firepower driver with
`INITGAMEFULL(frpwr_l6, s6_6digit_disp, 0, 45, 26, 25, 27, 28, 42, 12)`, which expands to
`core_tGameData {GEN_S6, s6_6digit_disp, {FLIP_SWNO(0,45)}, NULL, {{0}}, {0, {26, 25, 27, 28, 42, 12}}}`:

- `FLIP_SWNO(0,45)`: no left flipper matrix switch, and PinMAME's synthetic right-flipper button
  (public switch 82) is copied into matrix switch 45 every frame. On the machine, switch 45 is the
  LANE CHANGE switch the ROM reads to rotate the lit F-I-R-E lamps.
- `{{0}}`: the per-game inverted-switch mask is zero. Every public switch reads 1 closed and 0 open,
  which the ROM's own switch test confirms for all 58 wired positions.
- `{26, 25, 27, 28, 42, 12}`: the switches that fire special solenoids 17-22 (see below).

System 6 has no PinMAME profile of its own before this curation; `controllers/pinmame/system-6.json`
was written for it from `s6.c` and applies to every `GEN_S6` game.

## The controller contract a recreation drives

- Switches 1-64 are the sequential matrix, column-major: public = (column - 1) * 8 + row, which is
  exactly the number Figure 5 prints in each cell. Column 1 is the cabinet: tilts, credit button,
  three coin switches, slam tilt, high score reset. The service buttons are the direct inputs -7
  (Advance), -6 (Auto-Up/Manual-Down, 1 = Auto-Up), -5 (CPU diagnostic), -4 (sound diagnostic) and
  -3 (Master Command Enter).
- Flippers are not CPU-driven. Drive PinMAME's synthetic buttons 82 (right) and 84 (left). While
  the game is on (public solenoid 23), PinMAME fabricates flipper states 45/46 from 82 and 47/48
  from 84, and copies 82 into switch 45 (the retained flipper-button harness run shows it: 82 alone,
  with 45 never written, moves the lit lane-change lamp). The physical coils (8L25 right, 8L24 left,
  SFL-19-400/30-750-DC) are switched by the cabinet buttons through relay Z1 on the driver board,
  which the game-on line pulls in; each coil's end-of-stroke contact drops its power winding
  mechanically, so a recreation has no winding decision to make.
- Solenoids 1-8 and 14-22 are coils, 15 is two flash lamps, 9-13 are sound-command lines to the
  sound board, 2 and 3 are fitted drivers with no load (see below), 23 is the game-on enable.
  Addresses 24-44 are never published on System 6.
- Lamps 1-64: public = (column - 1) * 8 + row. Lamp 23 is not fitted. Columns 1-6 and column 7
  rows 1 and 8 (lamps 49 Right Special and 56 Credits (Playfield)) are playfield lamps; column 7
  rows 2-7 and all of column 8 are backbox inserts on the insert board.
- Displays: four six-digit player displays and a master display whose left pair (strobes 15-16) is
  the credit display and right pair (strobes 7-8) the ball-in-play and match display. PinMAME's
  display index 4 (memory positions 14-15) is credits and index 5 (positions 6-7) is ball in play;
  the ROM's solenoid test proves it by showing the test number on 4 and the solenoid number on 5.
  The Oliver seven-digit System 6 ROMs `frpwr_b6` and `frpwr_c6` publish the same six displays at
  other memory positions (see the driver `display_overrides`); their own harness runs show the
  credit on the entry at position 34 and the ball in play on the entry at position 14.
  PinMAME also publishes a 128x32 rendering frame of the segment layout, which is not a display on
  the machine.
- General illumination is an unswitched 6.3 VAC supply through fuse 6F1 (20 A) to the cabinet
  (coin-door lamps), the playfield and the insert board. There is no GI controller output.

## Special solenoids

System 6 has six special solenoid drivers, 17-22, for the four jet bumpers and two kickers
(slingshots). On the machine each is fired directly by its own special switch, 8SW65-8SW70, through
the driver board, as long as the game-on enable is set; the CPU sees only the separate scoring
contact in the matrix (switches 26, 25, 27, 28, 42 and 12). PinMAME has no public address for the
special switches and instead publishes the special solenoid whenever the matrix switch named in
`sxx.ssSw` closes. The retained gameplay harness run shows each pair: 26 -> 17 top left bumper,
25 -> 18 bottom left, 27 -> 19 top right, 28 -> 20 bottom right, 42 -> 21 right kicker,
12 -> 22 left kicker. Unlike System 11 and Data East, System 6 applies no permutation between the
special-solenoid slot and the public address.

The booklet prints solenoid 20 as `Bottom Left Jet Bumper` twice (Table 3 and Figure 3's chart),
repeating row 18. Everything else says Bottom Right: the schematic's coil 8L20 BOTTOM RIGHT JET
BUMPER and special switch 8SW68, Figure 3's callout 20 inside the lower right bumper, PinMAME's
switch map and the harness. A previous owner has pencilled `Rt` beside the row on the IPDB scan.

## Mechanisms a table author has to build

- **Outhole and ball ramp.** No trough: the three balls rest on a ball ramp below the apron, with
  rest switches 51 (left), 58 (centre) and 57 (right, the exit end). A drained ball falls into the
  outhole (9) below the apron centre; Ball Release (solenoid 1) kicks it onto the ramp. Ball Ramp
  Thrower (solenoid 8) throws the ball at position 57 into the shooter lane, onto the Ball Shooter
  switch (46). At game start with a full ramp the ROM throws the first ball; a new game cannot
  start until all balls are back on the ramp.
- **Three eject holes**: left (13, solenoid 4), right (30, solenoid 5) and upper right in the top
  corner (36, solenoid 6). A flashing hole locks the ball and a new ball is released from the ramp,
  a flashing hole or an unlit hole, in that order; locking all three balls starts MULTI-BALL.
  Otherwise the ROM kicks the ball straight back out; the harness shows repeated kicks while a hole
  switch stays closed. Star rollovers 53 and 54 sit in the lanes feeding the left and right holes.
- **Left ball saver kicker**: a kickback at the foot of the left outlane, solenoid 7. When lamp 2
  (Ball Saver Kicker On) is lit and the ball rolls over the left outside rollover (10), the ROM
  fires solenoid 7 and turns lamp 2 off. Which feat lights it is an operator adjustment: the POWER
  targets, targets 1-3 or 4-6 on one ball, or spotting 1-6. At factory settings the retained kicker
  harness run lights it from targets 1-3 and not from the POWER targets.
- **Four jet bumpers and two kickers** on special solenoids, as above.
- **Two three-target banks above the flippers**, "1" "2" "3" (17, 18, 19) left and "4" "5" "6"
  (21, 22, 23) right, with target arrows 26-31. They are standups on production machines. The first
  ten machines had two 3-banks of drop targets here (IPDB, Steve Ritchie), and the production
  hardware still carries their traces: the schematic calls the switches "Drop Target" and the
  arrows "Drop Target Arrow", Table 3 prints solenoids 2 and 3 Not Used with drivers Q17 and Q19
  fitted and their harness wires ending N/C, and switches 20, 24, 52 and 55 are printed NOT USED.
  The ROM still drives 2 and 3 as bank resets - at every ball start, and 2 when targets 1-3 are made
  (harness). A recreation of the production machine leaves them unconnected.
- **Three POWER standups** on the right (39, 40, 41, top to bottom) with blue lamps 9-11, and the
  **top centre target** (29) between the I and R lanes.
- **Four top rollover lanes F-I-R-E** (32-35) with lamps 5-8. LANE CHANGE: each closure of the right
  flipper's switch 45 rotates the lit F-I-R-E lamps one lane (harness: 45 moves lamp 5 off, lamp 6
  on). Spotting F-I-R-E advances the bonus multiplier and lights the FIRE insert.
- **Eight 50-point standups** on rubber-post runs: 16 top left; 14, 49 and 50 down the left rail,
  with 49 level with the left eject hole; 31 and 37 below the upper right eject hole; 38 middle
  right; 48 lower right.
- **Spinner** on the left orbit (15) with lamp 32.
- **FIRE and POWER inserts** above the kickers, each with two lamp bulbs (lamps 3 and 4) and one of
  the two Type 89 flash lamps on solenoid 15, which the ROM flashes every few seconds in attract
  mode.

## Tilts

Plumb bob (1), ball roll (2) and playfield (47, below the lower left playfield) tilt the ball in
play: first closure for the ball-roll and playfield tilts, third (adjustable) for the plumb bob.
Slam tilt (7) returns the game to game over.

## DIP switches and Master Command

PinMAME's DIP addresses are `bank * 8 + bit + 1` (see the controller profile). 1 and 2 are the
sound board's two-position switch DS1. 17-19 are the Master Command switches the booklet documents
(switch 8 zero audit totals, 7 restore factory settings, 6 auto-cycle), read by the ROM only while
Master Command Enter (-3) is held; PinMAME labels them D1-D3. The rest of the Master Command bank
and the second CPU-board bank (9-16, printed NOT USED in Figure 2) carry no function.

## Driver variants

- Williams: `frpwr_l6` (production L-6), `frpwr_l2` (L-2: earlier PROM 1, differing only in price
  presets and maximum credits per IPDB), the free-play-fix flipper ROM versions `frpwr_l6ff` and
  `frpwr_l2ff`, and Ted Estes's T-6 `frpwr_t6`/`frpwr_t6ff`. All identical hardware.
- Oliver System 6 custom ROMs `frpwr_a6` and `frpwr_d6` (6-digit, 2008): the same board with a 4 KB
  EPROM set.
- Oliver seven-digit conversions `frpwr_b6` and `frpwr_c6` on the same System 6 board: PinMAME's
  fp_7digit_disp moves the six displays to memory positions 0, 7, 20, 27 (seven digits wide), 34
  (credits) and 14 (ball in play), which each driver's own harness run confirms.
- The Oliver System 7 conversions `frpwr_a7`, `frpwr_b7`, `frpwr_c7`, `frpwr_d7` and `frpwr_e7`
  replace the CPU board with a Williams System 7 board, a different controller generation. They are
  not part of this record: like the Kiss and Eight Ball Deluxe prototypes, a different CPU board
  makes a separate physical record, `williams-oliver.firepower.1980`, which stays partial until a
  System 7 controller profile exists.

## Running the ROM in LibPinMAME

A first power-up from empty CMOS stops on the game-identification screen (`0497` then `1497 6` in
the player 1 display, 04 and 00 on the master display) and shows no lamps. Power up once more with
the saved NVRAM and the game comes up in attract mode with the 550,000 high score. The retained
harness runs therefore initialize each state directory with exactly one empty-NVRAM boot before the
evidentiary run.

## Retained table caveats

The retained known-working table (3rdaxis, Slydog43 & G5K, V1.0, 2018) is faithful in layout and
in almost every binding. It loads `frpwr_b7`, the Oliver System 7 conversion ROM, but every binding
this record takes from it (switches, lamps, solenoids 1-22) lies in the address space the two boards
share, and the production-ROM harness runs and the booklet confirm each one. Its defects:

1. Every 50-point standup handler pulses switch 48, so switches 14, 16, 31, 37, 38, 49 and 50 are
   never driven. The script has eight handlers but the table has only seven walls: standup 49 has
   none (the Vs A.I. revision adds it as StandupTarget8). Bind each standup to its own address.
2. Solenoid 7 only plays a sound; the table kicks the ball from its own copy of lamp 2. Drive the
   kickback from solenoid 7.
3. Lamp 56, the credit window lamp on the apron, is not modelled; the Vs A.I. revision adds it.
4. The ComboTrigger objects between the 1-6 targets pulse two target switches at once, a table aid.
5. It sets `UseSolenoids=25`, the game-on address of the System 7 ROM it loads. With any System 6
   driver of this record the game-on enable is solenoid 23, so a recreation must gate its flippers
   on 23. Loaded unchanged with a System 6 ROM, the table loses only its fast-flip key path, since
   solenoid 25 never asserts; core.vbs still forwards the ROM's flipper outputs 46 and 48, so the
   flippers move with ROM latency.

## Evidence

- Instruction Booklet 16P-497-103 (IPDB), cross-checked against a second printing (Internet
  Archive), for the switch, lamp and solenoid tables and location drawings.
- March 1980 schematics (IPDB) for wiring, the insert board, the master display, power and the
  sound board.
- Service Bulletin SS 20 for the flash lamp ground; Ted Estes's drop-target note and IPDB for the
  prototype history.
- Pinned PinMAME `8371478a` for the System 6 contract and the Oliver System 6 conversion drivers.
- The retained known-working table and its Vs A.I. revision for geometry and runtime bindings.
- LibPinMAME harness runs: solenoid test, switch test, gameplay causality, ball saver kicker, the
  flipper-button path, and the seven-digit `frpwr_b6` and `frpwr_c6` displays.
"""


CONVERSION_KNOWLEDGE_NOTE = """# Firepower, Oliver System 7 conversion - recreation knowledge

This partial record holds the five PinMAME drivers for Oliver's System 7 conversions of Williams
Firepower (IPDB 856): `frpwr_a7`, `frpwr_e7` (six-digit, 2005, revision 31), `frpwr_b7` (seven-digit,
2003), `frpwr_c7` (seven-digit, 2006, revision 38) and `frpwr_d7` (seven-digit, 2005, revision 31).
No retained source documents the conversion hardware itself. An Oliver conversion replaces the CPU
board and ROMs, so the playfield and cabinet are presumably the production machine's (curated as
`williams.firepower.1980`), but that is an assumption to verify, not a sourced fact.

## Why a separate record

Each of these drivers declares PinMAME machine driver `s7_mS7S6`: a Williams System 7 CPU board
(`GEN_S7`) with the stock System 6 sound board. The production machine and the Oliver System 6 ROMs
run on a System 6 CPU board (`GEN_S6`). A different CPU board is a different controller platform, so
these drivers follow the rule that split the Kiss Intel-8035 and Eight Ball Deluxe Motorola-68701
prototypes into their own records. The machine identity (IPDB 856, OPDB `G5VDd-MJpqO`) belongs to the
production record, so `identity` stays missing here.

## What pinned PinMAME says

- `INITGAMEFULL` passes the production machine's flipper and special-switch arguments: no left
  flipper matrix switch, the right button copied into switch 45, and special solenoids 17-22 fired by
  switches 26, 25, 27, 28, 42 and 12.
- The game-on enable is published at solenoid 25 (`S7_GAMEONSOL`), not 23.
- The `sxx.ssSw` loop runs over eight entries. When the ROM fires a special solenoid itself, System 7
  maps each PIA control line to a slot (`setSSSol`), and slots 6 and 7 publish 23 and 24. Whether this
  ROM uses those two slots is unknown.
- `s7_dips_r` has the same body as `s6_dips_r`: both return both CPU-board DIP banks, by display
  strobe position, while Master Command Enter (-3) is held. What differs is not the emulator but the
  ROM: the production record's finding that only the D1-D3 Master Command switches matter rests on
  PinMAME's System 6 source comment and the booklet, and which banks the Oliver System 7 ROM samples
  is unverified.
- `frpwr_a7` and `frpwr_e7` use the production six-digit display layout; `frpwr_b7`, `frpwr_c7` and
  `frpwr_d7` use fp_7digit_disp, with the seven-digit players at 0, 7, 20 and 27 and the two-digit
  entries at 34 and 14.

## What has been observed

One retained harness run of `frpwr_b7`, the ROM the retained known-working Firepower table loads,
repeats the production gameplay sequence. The game-on enable asserts at 25, the coin credit appears
on the entry at position 34 and the ball number on the entry at 14, and matrix switches 26, 25, 27,
28, 42 and 12 publish 17-22 in order. That last pairing is PinMAME's switch-driven path, sequential
by construction; the run never makes the ROM fire a special solenoid, never enters a service test
and never reads a DIP switch. `frpwr_a7`, `frpwr_c7`, `frpwr_d7` and `frpwr_e7` have no retained run.

## What is needed to complete it

- A Williams System 7 controller profile, derived from `s7.c`/`s7.h`, covering game-on at 25, the
  eight special-solenoid slots and the DIP banks.
- Harness runs of each driver through its solenoid and switch tests, to establish which public
  solenoids the ROM fires for each special coil and whether 23 and 24 carry anything.
- Enumeration of every address against that profile, with the production record's physical facts
  reused for the devices themselves.
"""


def generate(root: Path = ROOT) -> Path:
	write_json(root / CONVERSION_PATH.relative_to(ROOT), build_conversion())
	write_text(root / CONVERSION_KNOWLEDGE_PATH.relative_to(ROOT), build_conversion_knowledge())
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
	stale = root / (PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH).relative_to(ROOT)
	if stale.exists():
		raise RuntimeError(f"stale Firepower artifact under the other coverage directory: {stale}")
	for retired in RETIRED_ARTIFACTS:
		if (root / retired.relative_to(ROOT)).exists():
			raise RuntimeError(f"retired Oliver residual record still present: {retired}")
	definition = build()
	expected = canonical_bytes(definition)
	for path in (definition_path, root / SEED_PATH.relative_to(ROOT)):
		if not path.is_file() or path.read_bytes() != expected:
			raise RuntimeError(f"Firepower artifact drifted from its deterministic curator: {path}")
	report = build_spatial_report(definition)
	if (root / SPATIAL_REPORT_PATH.relative_to(ROOT)).read_bytes() != canonical_bytes(report):
		raise RuntimeError("Firepower spatial audit drifted from its deterministic curator")
	if (root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)).read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError("Firepower spatial review drifted from its deterministic curator")
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file() or knowledge_path.read_text(encoding="utf-8") != build_knowledge():
		raise RuntimeError("Firepower knowledge note drifted from its deterministic curator")
	conversion_path = root / CONVERSION_PATH.relative_to(ROOT)
	if not conversion_path.is_file() or conversion_path.read_bytes() != canonical_bytes(build_conversion()):
		raise RuntimeError(f"Firepower System 7 conversion record drifted from its deterministic curator: {conversion_path}")
	conversion_knowledge = root / CONVERSION_KNOWLEDGE_PATH.relative_to(ROOT)
	if not conversion_knowledge.is_file() or conversion_knowledge.read_text(encoding="utf-8") != build_conversion_knowledge():
		raise RuntimeError("Firepower System 7 conversion knowledge note drifted from its deterministic curator")
	print("Firepower definition, seed, spatial audit, knowledge note and System 7 conversion record match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifests")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extractions against their pinned manifest identities")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		write_extraction_manifests(source_root)
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifests(source_root)
		print("Firepower retained extractions match their pinned manifest identities.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
