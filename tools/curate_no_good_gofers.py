"""Curate the physical Williams No Good Gofers (1997) definition.

The data in this file are deliberately literal: regeneration never reads an
external manual or VPX tree.  ``--verify-extraction`` is the separate,
fail-closed evidence-identity check; ``--regenerate`` is the only write mode.
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
DEFINITION_PATH = ROOT / "machines/partial/williams/no-good-gofers-1997.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/no-good-gofers-1997.json"
SEED_PATH = ROOT / "tools/seeds/williams/no-good-gofers-1997.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/no-good-gofers-1997.json"
SPATIAL_MARKDOWN_PATH = ROOT / "reports/spatial/williams/no-good-gofers-1997.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.no-good-gofers.1997"
VPX_TABLE_SOURCE = "vpx-table.ngg-bodydump"
VPX_SCRIPT_SOURCE = "vpx-script.ngg-bodydump"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ngg-bodydump"
SIM_SOURCE = f"pinmame.sim.{PINMAME_REVISION[:12]}.ngg"

MANUAL_SHA256 = "736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d"
TABLE_SHA256 = "9f5b44285e3a10155fb0bf33a84626df45cc305f193d15963e39228355b91e59"
SCRIPT_SHA256 = "fbb6914941bd542f38e1ae9c15a6147b552cd33a22f586c85c3139da08aee766"
MANIFEST_SHA256 = "caf93fabeb7b697f65f3314425286a1f8fa96a37811b51f1abc357eb176ead66"
EXTRACTION_RELATIVE_PATH = Path("williams/no-good-gofers-1997/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/no-good-gofers-1997/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 927
EXTRACTION_TOTAL_BYTES = 127738302
TABLE_WIDTH = 964.0
TABLE_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

DRIVER_IDS = ("ngg_13", "ngg_p06", "ngg_10", "ngg_12")
DRIVER_NOTES = {
    "ngg_13": "Williams production game-ROM revision 1.3. The retained known-working VPX script binds cGameName = \"ngg_13\".",
    "ngg_p06": "Williams p0.6 prototype game-ROM revision. It is a firmware variant of the same physical 1997 No Good Gofers playfield; no contrary address or fitment evidence is retained.",
    "ngg_10": "Williams production game-ROM revision 1.0. It is an earlier firmware revision of the same physical 1997 playfield.",
    "ngg_12": "Williams production game-ROM revision 1.2. It is an earlier firmware revision of the same physical 1997 playfield.",
}

MATRIX = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
UNUSED_MATRIX = {11, 43, 87, 88}
OPTO_MATRIX = {31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 44, 45, 46, 63, 64}
MATRIX_LABELS = {
    11: "Not Used Matrix Position 11", 12: "Left Ramp Make", 13: "Start Button", 14: "Plumb Bob Tilt",
    15: "Center Ramp Make", 16: "Left Outlane", 17: "Right In-Lane", 18: "Shooter Groove",
    21: "Slam Tilt", 22: "Coin Door Closed", 23: "Jet Advance Standup", 24: "Always Closed",
    25: "Underground Pass", 26: "Left In-Lane", 27: "Right Outlane", 28: "Kickback",
    31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
    35: "Trough Ball 4", 36: "Trough Ball 5", 37: "Trough Ball 6", 38: "Jet Popper",
    41: "Left Gofer Down", 42: "Right Gofer Down", 43: "Not Used Matrix Position 43", 44: "Putt Out Popper",
    45: "Right Popper Jam", 46: "Right Popper", 47: "Left Ramp Down", 48: "Right Ramp Down",
    51: "Left Slingshot", 52: "Right Slingshot", 53: "Top Jet Bumper", 54: "Middle Jet Bumper",
    55: "Bottom Jet Bumper", 56: "Top Skill Shot", 57: "Middle Skill Shot", 58: "Lower Skill Shot",
    61: "Left Spinner", 62: "Right Spinner", 63: "Inner Wheel Opto", 64: "Outer Wheel Opto",
    65: "Left Gofer 1", 66: "Left Gofer 2", 67: "Behind Left Gofer", 68: "Hole-In-One Made",
    71: "Left Cart Path", 72: "Right Cart Path", 73: "Right Ramp Made", 74: "Golf Cart",
    75: "Right Gofer 1", 76: "Right Gofer 2", 77: "Advance Trap Value", 78: "Sand Trap Eject",
    81: "K-I-C-K Advance", 82: "(K)ick", 83: "K(I)ck", 84: "Ki(C)k", 85: "Kic(K)",
    86: "Captive Ball", 87: "Not Used Matrix Position 87", 88: "Not Used Matrix Position 88",
}

# (assembly, individual part).  A blank individual switch is intentionally not guessed from an assembly.
SWITCH_PARTS: dict[int, tuple[str | None, str | None]] = {
    12: (None, "20-10293"), 13: ("20-9663-16", None), 14: (None, "04-10346"),
    15: (None, "20-10293"), 16: ("A-17813", "5647-12693-19"), 17: ("A-17813", "5647-12693-19"),
    18: (None, "5647-12693-68"), 21: ("A-17238", None), 22: (None, "5643-09268-00"),
    23: ("A-17795-1", None), 24: (None, "5643-15190-00"), 25: (None, "5647-12693-21"),
    26: ("A-17813-1", "5647-12693-19"), 27: ("A-17813", "5647-12693-19"), 28: ("A-17813", "5647-12693-19"),
    31: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None), 32: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None),
    33: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None), 34: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None),
    35: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None), 36: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None),
    37: ("A-18617-1 LED / A-18618-1 PHOTO TRANS", None), 38: ("A-16908 LED / A-16909 PHOTO TRANS", None),
    41: ("A-16908 LED / A-16909 PHOTO TRANS", None), 42: ("A-16908 LED / A-16909 PHOTO TRANS", None),
    44: ("A-16908 LED / A-16909 PHOTO TRANS", None), 45: ("A-16908 LED / A-16909 PHOTO TRANS", None),
    46: ("A-16908 LED / A-16909 PHOTO TRANS", None), 47: (None, "5647-12693-31"), 48: (None, "5647-12693-31"),
    51: ("A-17801", "A-17800 KICK / A-17794 SCORE"), 52: ("A-17801", "A-17800 KICK / A-17794 SCORE"),
    53: ("B-12030-2", "A-16443"), 54: ("B-12030-2", "A-16443"), 55: ("B-12030-2", "A-16443"),
    56: ("A-17799-6", None), 57: ("A-17795-6", None), 58: ("A-17799-6", None),
    61: ("A-22037-2", "5647-12693-24"), 62: ("A-22037-2", "5647-12693-24"),
    63: ("A-22026 Motor 2-Opto Board", None), 64: ("A-22026 Motor 2-Opto Board", None),
    65: (None, "20-10293"), 66: (None, "20-10293"), 67: (None, "5647-12693-13"), 68: (None, "5647-12693-13"),
    71: ("A-17813", "5647-12693-19"), 72: ("A-17813", "5647-12693-19"), 73: (None, "20-10293"),
    74: ("A-22222 Qty. 2 / A-22224-4 Qty. 2", None), 75: (None, "20-10293"), 76: (None, "20-10293"),
    77: ("A-15330-6", None), 78: ("A-19693", "5647-12693-43"), 81: ("A-17799-4", None),
    82: ("B-12039-15", None), 83: ("B-12039-15", None), 84: ("B-12039-15", None), 85: ("B-12039-15", None),
    86: ("A-17813-1", "5647-12693-19"),
}

SWITCH_COLUMNS = {
    1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
    3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-White", "J206-4", "U20-15"),
    5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
    7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROWS = {
    1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
    3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
    5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
    7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED = {
    1: ("Left Coin Chute", "Orange-Brown", "J205-1", "U17-5"),
    2: ("Center Coin Chute", "Orange-Red", "J205-2", "U17-7"),
    3: ("Right Coin Chute", "Orange-Black", "J205-3", "U17-11"),
    4: ("4th Coin Chute", "Orange-Yellow", "J205-4", "U17-9"),
    5: ("Service Credits / Escape", "Orange-Green", "J205-6", "U16-9"),
    6: ("Volume Down / Down", "Orange-Blue", "J205-7", "U16-11"),
    7: ("Volume Up / Up", "Orange-Violet", "J205-8", "U16-7"),
    8: ("Begin Test / Enter", "Orange-Gray", "J205-9", "U16-5"),
}
FLIPPER_SWITCHES = {
    111: ("Lower Right Flipper EOS", "F1", "SW-1A-194", "BLACK-GREEN", "J208-13", False, "playfield"),
    112: ("Lower Right Flipper Button", "F2", "A-17316", "BLUE-VIOLET", "J212-12", True, "cabinet"),
    113: ("Lower Left Flipper EOS", "F3", "SW-1A-194", "BLACK-BLUE", "J208-12", False, "playfield"),
    114: ("Lower Left Flipper Button", "F4", "A-17316", "BLUE-GRAY", "J212-11", True, "cabinet"),
    115: ("Upper Right Flipper EOS", "F5", "SW-1A-194", "BLACK-VIOLET", "J208-11", False, "playfield"),
    116: ("Upper Right Flipper Button", "F6", "A-17316", "BLACK-YELLOW", "J212-10", True, "cabinet"),
    117: ("Not Used Upper Left Flipper EOS", "F7", None, "BLACK-GRAY", "J208-10", False, "unused"),
    118: ("Not Used Upper Left Flipper Button", "F8", None, "BLACK-BLUE", "J212-9", True, "unused"),
}

# Exact retained-VPX object centres. These are normalized exclusively by point()/located().
INPUT_POINTS = {
    12: (86.875, 202.4375), 15: (104.1875, 63.5625), 16: (119.75, 1574.25), 17: (770.75, 1577.25),
    18: (903.5625, 1935.5), 23: (211.375, 1089.625), 25: (237.5625, 2104.75), 26: (183.5, 1576.0),
    27: (839.25, 1677.25), 28: (50.75, 1737.25), 38: (94.5, 615.375), 44: (427.5625, 277.25),
    45: (759.75, 344.0), 46: (836.5, 331.5), 51: (321.0, 1829.5), 52: (630.0, 1829.5),
    53: (55.125, 828.6875), 54: (150.625, 1005.9375), 55: (69.375, 1182.4375),
    56: (380.125, 716.875), 57: (391.75, 767.5), 58: (393.5, 812.5),
    61: (240.0625, 850.9375), 62: (883.5037, 484.8201), 65: (568.5, 449.0),
    67: (593.75, 257.0), 68: (684.0, 233.0), 71: (138.75, 305.25), 72: (890.875, 266.625),
    73: (900.1875, 64.5625), 74: (478.5, 215.0), 75: (717.5, 524.375), 77: (106.5625, 1259.6875),
    78: (72.375, 1336.125), 81: (820.1875, 1103.9375), 82: (832.8125, 1166.3125),
    83: (815.5625, 1216.5625), 84: (794.375, 1271.375), 85: (774.625, 1325.625),
    86: (381.25, 1062.75), 111: (630.0, 1829.5), 113: (321.0, 1829.5), 115: (876.7578, 816.8672),
}

LAMP_LABELS = {
    11: "Outlane Extra Ball", 12: "Kickback", 13: "Lower Driving Range", 14: "Shoot Again", 15: "Special", 16: "Wheel Value", 17: "Jet Lightning", 18: "Hole 8",
    21: "Hole 5", 22: "Hole 4", 23: "Hole 3", 24: "Hit Bud", 25: "Hole 1", 26: "2X", 27: "Cart Path 2", 28: "5X Cart Path",
    31: "Hole 6", 32: "Hole 7", 33: "Hole 2", 34: "Hit Buzz", 35: "Hole 9", 36: "4X", 37: "Cart Path 4", 38: "3X",
    41: "Driving Range", 42: "Increase Golf Cart", 43: "Increase Buzz Value", 44: "Increase Bud Value", 45: "Newton Drive", 46: "Collect", 47: "Rip Off", 48: "Left Loop Drive",
    51: "(K)ick", 52: "K(I)ck", 53: "Ki(C)k", 54: "Kic(K)", 55: "Skill Shot", 56: "Relight Jackpot", 57: "Right Ramp Lock", 58: "Right Ramp Drive",
    61: "4 Strokes", 62: "3 Strokes", 63: "2 Strokes", 64: "5 Strokes", 65: "7 Strokes", 66: "6 Strokes", 67: "Left Spinner", 68: "Trap Ready",
    71: "Advance Trap", 72: "Center Drive", 73: "Center Lock", 74: "Get T.N.T.", 75: "Center Raise Gofer", 76: "Right Spinner", 77: "Right Loop Drive", 78: "Bottom Jet Bumper",
    81: "Side Ramp Drive", 82: "Extra Ball", 83: "Multiball", 84: "Jackpot", 85: "Putt Out", 86: "Top Jet Bumper", 87: "Middle Jet Bumper", 88: "Start Button",
}
LAMP_PARTS = {
    11:("A-17835","#44 / 24-6549","Not Sold Separate",1),12:("A-17835","#44 / 24-6549","Not Sold Separate",1),13:("A-17835","#44 / 24-6549","Not Sold Separate",2),14:("A-17807","#44 / 24-6549","Not Sold Separate",1),15:("A-17807","#44 / 24-6549","Not Sold Separate",1),16:("A-17807","#44 / 24-6549","Not Sold Separate",1),17:("A-17835","#44 / 24-6549","Not Sold Separate",1),18:("A-17835","#44 / 24-6549","Not Sold Separate",1),
    21:("A-22038","#555 / 24-8768","24-8767",1),22:("A-22038","#555 / 24-8768","24-8767",1),23:("A-22038","#555 / 24-8768","24-8767",1),24:("A-22038","#555 / 24-8768","24-8767",1),25:("A-22038","#555 / 24-8768","24-8767",1),26:("A-22038","#555 / 24-8768","24-8767",1),27:("A-22038","#555 / 24-8768","24-8767",1),28:("A-22038","#555 / 24-8768","24-8767",2),
    31:("A-22038","#555 / 24-8768","24-8767",1),32:("A-22038","#555 / 24-8768","24-8767",1),33:("A-17835","#44 / 24-6549","Not Sold Separate",1),34:("A-22038","#555 / 24-8768","24-8767",1),35:("A-22038","#555 / 24-8768","24-8767",1),36:("A-22038","#555 / 24-8768","24-8767",1),37:("A-22038","#555 / 24-8768","24-8767",1),38:("A-22038","#555 / 24-8768","24-8767",1),
    41:("A-22039","#555 / 24-8768","24-8767",1),42:("A-22039","#555 / 24-8768","24-8767",1),43:("A-22039","#555 / 24-8768","24-8767",1),44:("A-22039","#555 / 24-8768","24-8767",1),45:("A-22039","#555 / 24-8768","24-8767",1),46:("A-22039","#555 / 24-8768","24-8767",1),47:("A-22039","#555 / 24-8768","24-8767",1),48:("A-17835","#44 / 24-6549","Not Sold Separate",1),
    51:("A-22042","#555 / 24-8768","24-8767",1),52:("A-22042","#555 / 24-8768","24-8767",1),53:("A-22042","#555 / 24-8768","24-8767",1),54:("A-22042","#555 / 24-8768","24-8767",1),55:("A-17835 + A-22043","#44 + #555 / 24-6549 + 24-8768","Not Sold Separate + 24-8767",2),56:("A-22043","#555 / 24-8768","24-8767",1),57:("A-22043","#555 / 24-8768","24-8767",1),58:("A-22043","#555 / 24-8768","24-8767",1),
    61:("A-22040","#555 / 24-8768","24-8767",1),62:("A-22040","#555 / 24-8768","24-8767",1),63:("A-22040","#555 / 24-8768","24-8767",1),64:("A-22040","#555 / 24-8768","24-8767",1),65:("A-22040","#555 / 24-8768","24-8767",1),66:("A-22040","#555 / 24-8768","24-8767",1),67:("A-17807","#44 / 24-6549","Not Sold Separate",1),68:("A-17807","#44 / 24-6549","Not Sold Separate",2),
    71:("A-17807 + A-22041","#44 + #555 / 24-6549 + 24-8768","Not Sold Separate + 24-8767",2),72:("A-22041","#555 / 24-8768","24-8767",1),73:("A-22041","#555 / 24-8768","24-8767",1),74:("A-22041","#555 / 24-8768","24-8767",1),75:("A-22041","#555 / 24-8768","24-8767",1),76:("A-17807","#44 / 24-6549","Not Sold Separate",1),77:("A-17835","#44 / 24-6549","Not Sold Separate",1),78:(None,"#555 / 24-8768","24-8776",1),
    81:("A-22041","#555 / 24-8768","24-8767",1),82:("A-22041","#555 / 24-8768","24-8767",1),83:("A-22041","#555 / 24-8768","24-8767",1),84:("A-22041","#555 / 24-8768","24-8767",1),85:("A-22041","#555 / 24-8768","24-8767",1),86:(None,"#555 / 24-8768","24-8776",1),87:(None,"#555 / 24-8768","24-8776",1),88:("20-9663-16",None,None,1),
}
LAMP_POINTS = {
    11:[(48.625,1542.8438)],12:[(47.5,1630.4688)],13:[(149.625,1465.6562)],14:[(478,1881.1875)],15:[(840.75,1558.0312)],16:[(591.9907,1350.1238)],17:[(252.3628,1186.9849)],18:[(590.875,1589.0312)],
    21:[(475,1513.2188)],22:[(429.75,1519.9062)],23:[(388.25,1546.0312)],24:[(446.0625,1618.9375)],25:[(353.25,1631.4062)],26:[(349,1684.5)],27:[(413,1697.875)],28:[(473.25,1763.3125)],
    31:[(523.875,1522.0938)],32:[(563.25,1547.9688)],33:[(361.875,1584.4062)],34:[(505.5625,1621.6875)],35:[(599.25,1637.1562)],36:[(602,1688.625)],37:[(542.125,1699.5)],38:[(478.125,1701.75)],
    41:[(435.4907,1311.1863)],42:[(423.4313,1252.9675)],43:[(409.6813,1193.2175)],44:[(396.6813,1134.9675)],45:[(383.4313,1075.4675)],46:[(336.3847,1051.1128)],47:[(415.9875,1035.303)],48:[(285.2378,997.6723)],
    51:[(796.0312,1146.0862)],52:[(775.4062,1201.8362)],53:[(754.1562,1258.4612)],54:[(733.6562,1315.5862)],55:[(761.7996,939.3299),(628.6782,858.3875)],56:[(673.2364,706.3511)],57:[(660.7378,753.5473)],58:[(649.842,800.7109)],
    61:[(352.9375,1356.0312)],62:[(394.4375,1390.25)],63:[(331.1875,1422.0625)],64:[(297.6875,1358.2812)],65:[(264.9375,1451.5312)],66:[(261.4375,1397.2812)],67:[(251.8552,887.7422)],68:[(201.5,1304.1562)],
    71:[(141.8125,1316.1875),(438.223,736.3085)],72:[(527.8704,741.1801)],73:[(536.5579,693.6176)],74:[(514.169,634.5194)],75:[(575.0579,643.3051)],76:[(859.6052,560.6172)],77:[(819.0391,672.3483)],78:[(69.375,1182.4375)],
    81:[(383.7341,612.5475)],82:[(434.934,529.5814)],83:[(440.99,591.4884)],84:[(453.3563,662.033)],85:[(429.184,465.5814)],86:[(55.125,828.6875)],87:[(150.625,1005.9375)],
}

LAMP_COLUMNS = {1:("Yellow-Brown","J121-1","Q96"),2:("Yellow-Red","J121-2","Q100"),3:("Yellow-Orange","J121-3","Q95"),4:("Yellow-Black","J121-4","Q99"),5:("Yellow-Green","J121-5","Q94"),6:("Yellow-Blue","J121-6","Q98"),7:("Yellow-Violet","J121-7","Q93"),8:("Yellow-Gray","J121-9","Q97")}
LAMP_ROWS = {1:("Red-Brown","J125-1","Q104"),2:("Red-Black","J125-2","Q108"),3:("Red-Orange","J125-4","Q103"),4:("Red-Yellow","J125-5","Q107"),5:("Red-Green","J125-6","Q102"),6:("Red-Blue","J125-7","Q106"),7:("Red-Violet","J125-8","Q101"),8:("Red-Gray","J125-9","Q105")}

# Main manual table: label, schema kind, board class, voltage connection, transistor, control pin, wire, assembly, part.
MAIN_SOLENOIDS = {
    1:("Auto Fire","coil","High Power","J133-2","Q72","J116-1","VIO-BRN","A-22204","AE-23-800"),2:("Kickback","coil","High Power","J134-3","Q68","J116-2","VIO-RED","B-11873","AE-23-800"),3:("Clubhouse Kicker","coil","High Power","J133-2","Q71","J116-4","VIO-ORG","A-21989","AE-23-800"),4:("Left Gofer Up","coil","High Power","J133-2","Q67","J116-5","VIO-YEL","A-21815-2","LE-23-1300"),5:("Right Gofer Up","coil","High Power","J133-2","Q70","J116-6","VIO-GRN","A-21815-1","LE-23-1300"),6:("Jet Popper","coil","High Power","J133-2","Q66","J116-7","VIO-BLU","A-21988","AE-27-1200"),7:("Left Eject","coil","High Power","J133-2","Q69","J116-8","VIO-BLK","A-20496-1","AE-24-900"),8:("Upper Right Eject","coil","High Power","J133-2","Q65","J116-9","VIO-GRY","A-22022","AE-26-1200"),9:("Trough Eject","coil","Low Power","J133-3","Q44","J113-1","BRN-BLK","A-18753","AE-26-1500"),
    10:("Left Slingshot","coil","Low Power","J133-3","Q48","J113-3","BRN-RED","A-22207-2","AE-26-1200"),11:("Right Slingshot","coil","Low Power","J133-3","Q43","J113-4","BRN-ORG","A-22206-2","AE-26-1200"),12:("Top Jet Bumper","coil","Low Power","J133-3","Q47","J113-5","BRN-YEL","A-22205-2","AE-26-1200"),13:("Middle Jet Bumper","coil","Low Power","J133-3","Q42","J113-6","BRN-GRN","A-22205-2","AE-26-1200"),14:("Bottom Jet Bumper","coil","Low Power","J133-3","Q46","J113-7","BRN-BLU","A-22205-2","AE-26-1200"),15:("Left Gofer Down","coil","Low Power","J133-3","Q41","J113-8","BRN-VIO","A-21815-2","AE-30-2000"),16:("Right Gofer Down","coil","Low Power","J133-3","Q45","J113-9","BRN-GRY","A-21815-1","AE-30-2000"),
    17:("Jet Flasher","flasher","Flasher","J133-6","Q28","J111-1","BLK-BRN","A-17802","#906 / 24-8802"),18:("Lower Left Flasher","flasher","Flasher","J133-6","Q32","J111-2","BLK-RED",None,"#906 / 24-8802"),19:("Left Spinner Flasher","flasher","Flasher","J133-6","Q27","J111-3","BLK-ORG","A-17802","#906 / 24-8802"),20:("Right Spinner Flasher","flasher","Flasher","J133-6","Q31","J111-4","BLK-YEL","A-17802 + A-17983","#906 / 24-8802 + #89 / 24-8704"),21:("Lower Right Flasher","flasher","Flasher","J133-6","Q26","J111-5","BLU-GRN","A-17983","#89 / 24-8704"),
    24:("Underground Pass","coil","Flasher driver bank","J133-1","Q29","J111-8","BLU-GRY","A-21989","AE-27-1200"),25:("Sand Trap Flasher","flasher","Gen. Purpose driver bank","J133-6","Q16","J109-1","BLU-BRN","A-17802","#906 / 24-8802"),26:("Wheel Flasher","flasher","Gen. Purpose driver bank","J133-6","Q15","J109-2","BLU-RED","A-17802","#906 / 24-8802"),27:("Left Ramp Down","coil","Gen. Purpose driver bank","J133-1","Q14","J109-3","BLU-ORG","A-22016","SM1-28-900"),28:("Right Ramp Down","coil","Gen. Purpose driver bank","J133-1","Q13","J109-4","BLU-YEL","A-22016","SM1-28-900"),
}
OUTPUT_POINTS = {1:[(911.4788,2111.7246)],2:[(50.3125,1871.25)],3:[(427.5625,277.25)],4:[(568.5,449.0)],5:[(717.5,524.375)],6:[(94.5,615.375)],7:[(72.375,1336.125)],8:[(836.5,331.5)],9:[(800.4375,1865.0)],12:[(55.125,828.6875)],13:[(150.625,1005.9375)],14:[(69.375,1182.4375)],15:[(568.5,449.0)],16:[(717.5,524.375)],17:[(45.4802,1004.8671)],18:[(42.1875,1429.7188)],19:[(145.1875,687.7188)],20:[(858.0926,559.0926)],21:[(914.3125,1416.8438)],24:[(65.5625,1953.75)],25:[(203.5,1307.0)],26:[(594.75,1364.75)],33:[(876.7578,816.8672)],34:[(876.7578,816.8672)],35:[(646.0,2126.0)],45:[(630.0,1829.5)],46:[(630.0,1829.5)],47:[(321.0,1829.5)],48:[(321.0,1829.5)],51:[(844.3438,547.25)],52:[(850.7188,394.7812)],53:[(852.8125,261.7188)],56:[(107.4062,532.0312)],57:[(101.1875,382.7188)],58:[(94.1875,244.4375)]}

MANUAL_EXCERPTS = [
    ("excerpt.ngg.auxiliary-8-driver-board", "PDF page 138, printed 3-24, Auxiliary 8-driver Board A-21773", "auxiliary-8-driver-board.md", "eca7d49ebf0defcb2d228bd61ba54a91474ad45a4bf86f43516c4795429c1838"),
    ("excerpt.ngg.flipper-circuits", "PDF pages 125 and 127, printed 3-11 and 3-13, flipper circuits", "flipper-circuits.md", "4e4551c4d3c636edc4193b6c2790e4143f5adaf304ada0e15b709f484ef229f7"),
    ("excerpt.ngg.general-illumination", "PDF page 144, printed 3-30, J104/J105/J106 GI destinations", "general-illumination.md", "35de42daa352f4f191abe3fc26d6bccb2e430058e60c4c179810ac189c2aed6e"),
    ("excerpt.ngg.lamp-locations", "PDF page 102, printed 2-42, Lamp Locations", "lamp-locations.md", "b7f6a09bf596334fec2c5a11d6330ba38a8e255d68d3520930cc948a519a3557"),
    ("excerpt.ngg.lamp-matrix", "PDF page 112, printed 2-52, Lamp Matrix", "lamp-matrix.md", "7c4dd0788eb1a385e725490e0135c44161a47e6531846344ce2181c9685f1143"),
    ("excerpt.ngg.solenoid-locations", "PDF pages 104-105, printed 2-44 and 2-45, solenoid locations", "solenoid-flasher-locations.md", "b6ebe81b00bd3fba8e0b7e18cf55b794d69bf02b7d66c7ac6038da079f3bfcf1"),
    ("excerpt.ngg.solenoid-wiring", "PDF page 113, printed 2-53, Solenoid/Flasher Table", "solenoid-flasher-wiring.md", "1c7a3af0b3b7c6657c14f5f0eba8d03602f0310e0e7e52e79b24b4cf8d3419b3"),
    ("excerpt.ngg.step-flasher-locations", "PDF page 105, printed 2-45, step-flasher callouts", "step-flasher-locations.webp", "5e684e13c8263430d94bc3ba56b9845d724896a41416738b10310115c9a1fb33"),
    ("excerpt.ngg.switch-locations", "PDF pages 108-109, printed 2-48 and 2-49, Switch Locations", "switch-locations.md", "27f5e60f9854af2dfc90324560470f1b109f3e6c6feef5aebde989f73f33cc5c"),
    ("excerpt.ngg.switch-matrix", "PDF pages 111 and 116, printed 2-51 and 3-1, Switch Matrix", "switch-matrix.md", "312fad1f7e723fda5744202423ec1f2f123c9850a665f926f0e9126c7ce5c28c"),
    ("excerpt.ngg.switch-matrix-image", "PDF page 116, printed 3-1, visual opto-shading crop", "switch-matrix.webp", "8602a90ed427d7376edb9e410f42f519b1d8f020d06a8095c797f54f0436d548"),
    ("excerpt.ngg.wheel-motor-optos", "PDF page 137, printed 3-23, Motor 2-Opto Board and wheel motor", "wheel-motor-and-optos.md", "b95486be8b4e82dc896eaaa4bdeacc13efd9ee9eeece2432efc6113613277c65"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
    if not extraction_root.is_dir():
        raise RuntimeError(f"No Good Gofers retained extraction is missing: {extraction_root}")
    paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
    return {"format": "pinmame-vpx-extraction-manifest", "version": 1, "files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": sha256(path)} for path in paths]}


def configured_vpx_sources_root(required: bool) -> Path | None:
    value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if not value and required:
        raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained No Good Gofers extraction")
    return Path(value).expanduser().resolve() if value else None


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
    manifest = load_json(source_root / EXTRACTION_MANIFEST_RELATIVE_PATH)
    actual = build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)
    if canonical_bytes(manifest) != canonical_bytes(actual):
        raise RuntimeError("No Good Gofers extraction manifest does not match every retained extracted file")
    count, size = len(manifest["files"]), sum(int(item["size"]) for item in manifest["files"])
    digest = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    if (count, size, digest) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, MANIFEST_SHA256):
        raise RuntimeError(f"No Good Gofers extraction identity mismatch: files={count}, bytes={size}, sha256={digest}")
    return manifest


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
    return {"status": status, "source_refs": list(refs)}


def point(raw: tuple[float, float]) -> tuple[float, float]:
    return (round(raw[0] / TABLE_WIDTH, 6), round(raw[1] / TABLE_HEIGHT, 6))


def located(identifier: str, role: str, raw_points: list[tuple[float, float]], *refs: str, status: str = "validated") -> dict[str, Any]:
    placements = []
    for index, raw in enumerate(raw_points, start=1):
        x, y = point(raw)
        suffix = f".{index}" if len(raw_points) > 1 else ""
        placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs)})
    return {"status": status, "placements": placements}


def not_applicable(reason: str, *refs: str) -> dict[str, Any]:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def device(identifier: str, label: str, kind: str, group: str, address: int, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": [], "provenance": provenance(*refs)}
    result.update(extra)
    return result


def matrix_wiring(address: int) -> dict[str, Any]:
    column, row = divmod(address, 10)
    drive_wire, drive_connection, drive_receiver = SWITCH_COLUMNS[column]
    return_wire, return_connection, return_receiver = SWITCH_ROWS[row]
    return {"board": "WPC-95 CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection, "return_wire": return_wire, "return_connection": return_connection, "return_component": f"drive receiver {drive_receiver}; return receiver {return_receiver}"}


def sources() -> list[dict[str, Any]]:
    excerpts = [{"id": item[0], "locator": item[1], "path": f"evidence/excerpts/williams.no-good-gofers.1997/{item[2]}", "sha256": item[3], "method": "manual", "transcribed_by": "curator, visually checked against retained 300 dpi renders", "reviewed": True} for item in MANUAL_EXCERPTS]
    return [
        {"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/driver.c No Good Gofers catalog entries and src/wpc/sims/wpc/full/ngg.c CORE_GAMEDEF/CORE_CLONEDEF", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sims/wpc/full/ngg.c nggGameData GEN_WPC95 with hw.custSol=8, ngg_getSol indexing WPC_EXTBOARD2 from CORE_CUSTSOLNO(1), FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_UR), inverted-switch mask, wpc_set_modsol_aux_board(2), wheel and gofer/ramp/slam mechanisms; src/wpc/core.h CORE_FIRSTCUSTSOL=51/CORE_CUSTSOLNO; src/wpc/core.c custom-output dispatch; src/wpc/wpc.c No Good Gofers core_set_pwm_output_type table. The latter types 42+14 through 49+14 (56-63) but does not map or drive public state and extends past this driver's declared 51-58 custom range, so it is retained as a PinMAME output-type metadata defect rather than treated as a second address map.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-95.json", "revision": "repository", "locator": "WPC-95 switch, Fliptronic, LPDC mirror, standard/custom output, lamp, and five-GI controller contract", "license": "NOASSERTION", "attribution": "pinmame-game-defs"},
        {"id": MANUAL_SOURCE, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/williams.no-good-gofers.1997/archive-arcademanual_No_Good_Gofers_OPS/No_Good_Gofers_OPS.pdf", "original_filename": "No_Good_Gofers_OPS.pdf", "sha256": MANUAL_SHA256, "locator": "148-page Williams No Good Gofers Operations Manual; retained visual source for physical construction, part numbers, wiring, quantities, labels and the numbered top-view callout drawing.", "license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.", "rights": "NOASSERTION", "excerpts": excerpts},
        {"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/no-good-gofers-1997/source/No%20Good%20Gofers%20%28Williams%201997%29.vpx", "original_filename": "No Good Gofers (Williams 1997).vpx", "sha256": TABLE_SHA256, "locator": f"Retained known-working No Good Gofers recreation. Exact bounds are {TABLE_BOUNDS}; every coordinate in this definition is raw VPX x/964, y/2162. Geometry is used only for explicitly bound retained objects.", "license": "NOASSERTION", "attribution": "Bodydump; models by Dark", "rights": "NOASSERTION", "known_working": True},
        {"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/williams/no-good-gofers-1997/extracted-vpxtool/script.vbs", "original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "locator": "Retained embedded script (46,531 bytes): Const cGameName = \"ngg_13\"; SolCallback and UpdateLamps tables; cvpmBallStack trough/poppers; gofer/ramp and Slam Ramp logic; switch event handlers.", "license": "NOASSERTION", "attribution": "Bodydump; models by Dark", "rights": "NOASSERTION", "known_working": True},
        {"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/no-good-gofers-1997/extracted-vpxtool.manifest.json", "sha256": MANIFEST_SHA256, "locator": f"Canonical manifest of all {EXTRACTION_FILE_COUNT} extracted files / {EXTRACTION_TOTAL_BYTES} bytes, sorted relative POSIX path with size and SHA-256; canonical manifest SHA-256 {MANIFEST_SHA256}.", "license": "NOASSERTION", "attribution": "vpxtool extraction"},
        {"id": SIM_SOURCE, "kind": "pinmame_sim", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sims/wpc/full/ngg.c simulator state model consulted only as lower-priority support; it is not used to infer physical fitment or to override the retained VPX/manual.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
    ]


def inputs() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for address, (label, wire, connection, receiver) in DEDICATED.items():
        result.append(device(f"switch.dedicated-{address}", label, "switch", "pinmame.input.switch", address, (MANUAL_SOURCE,), availability="used", aliases=[{"namespace": "manual.position", "value": f"D{address}"}], wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": receiver}, spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE)))
    for address in MATRIX:
        label = MATRIX_LABELS[address]
        identifier = f"switch.matrix-{address}"
        if address in UNUSED_MATRIX:
            result.append(device(identifier, label, "switch", "pinmame.input.switch", address, (MANUAL_SOURCE,), availability="unused", aliases=[{"namespace": "manual.address", "value": str(address)}], spatial=not_applicable("unused", MANUAL_SOURCE)))
            continue
        physical: dict[str, Any] = {"location": label, "quantity": 1}
        assembly, part = SWITCH_PARTS.get(address, (None, None))
        if assembly: physical["assembly_part_number"] = assembly
        if part: physical["part_number"] = part
        if address in OPTO_MATRIX:
            physical["switch_type"] = "opto"
        elif address == 13:
            physical["switch_type"] = "button"
        elif address in {14, 21}:
            physical["switch_type"] = "tilt"
        elif address == 24:
            physical["switch_type"] = "other"
        if address not in INPUT_POINTS and address not in {13, 14, 21, 22, 24}:
            physical["notes"] = "No one-to-one retained VPX playfield object is bound to this physical switch; no coordinate is invented."
        extra: dict[str, Any] = {"availability": "used", "aliases": [{"namespace": "manual.address", "value": str(address)}], "physical": physical, "wiring": matrix_wiring(address), "normally_closed": address in OPTO_MATRIX}
        if address == 24:
            extra.update({"kind": "constant", "constant_active": True, "initial_active": True, "spatial": not_applicable("constant", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)})
        elif address in {13, 14, 21, 22}:
            extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
        elif address in INPUT_POINTS:
            extra["spatial"] = located(identifier, "sensor", [INPUT_POINTS[address]], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
        result.append(device(identifier, label, extra.pop("kind", "switch"), "pinmame.input.switch", address, (MANUAL_SOURCE,), **extra))
    for address, (label, manual_position, part, wire, connection, normally_closed, location) in FLIPPER_SWITCHES.items():
        identifier = f"switch.flipper-{manual_position.casefold()}"
        used = location != "unused"
        extra: dict[str, Any] = {"availability": "used" if used else "unused", "aliases": [{"namespace": "manual.position", "value": manual_position}], "normally_closed": normally_closed}
        if part:
            extra["physical"] = {"part_number": part, "location": "flipper circuit" if location == "playfield" else "cabinet opto board", "quantity": 1, "switch_type": "opto" if normally_closed else "leaf"}
        if location == "playfield":
            extra["spatial"] = located(identifier, "sensor", [INPUT_POINTS[address]], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
        elif location == "cabinet":
            extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
        else:
            extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
        extra["wiring"] = {"board": "WPC-95 CPU board", "control_wire": wire, "control_connection": connection}
        result.append(device(identifier, label, "switch", "pinmame.input.switch", address, (MANUAL_SOURCE, CORE_SOURCE), **extra))
    for address in range(1, 9):
        result.append(device(f"switch.dip-{address}", f"CPU DIP {address} (country code bit)", "dip_switch", "pinmame.input.dip", address, (CONTROLLER_SOURCE,), availability="used", aliases=[{"namespace": "controller.position", "value": str(address)}], physical={"location": "CPU board", "quantity": 1, "switch_type": "dip"}, spatial=not_applicable("dip_switch", CONTROLLER_SOURCE)))
    return result


def solenoids() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for address in range(1, 29):
        if address in {22, 23}:
            transistor, wire = {22: ("Q30", "BLU-BLK"), 23: ("Q25", "BLU-VIO")}[address]
            result.append(device(f"output.solenoid-{address:02d}-unused", f"Not Used Driver {address}", "coil", "pinmame.output.solenoid", address, (MANUAL_SOURCE,), availability="unused", aliases=[{"namespace": "manual.address", "value": str(address)}], physical={"location": "unfitted main driver position", "notes": "The power-driver transistor and supply rail are populated, but the manual prints no drive connection, load, or flashlamp type; no physical playfield device is fitted."}, wiring={"board": "WPC-95 power driver board", "driver_transistor": transistor, "drive_wire": wire, "power_connection": "J133-6", "voltage_type": "dc"}, spatial=not_applicable("unused", MANUAL_SOURCE)))
            continue
        label, kind, bank, voltage, transistor, connection, wire, assembly, part = MAIN_SOLENOIDS[address]
        identifier = f"output.solenoid-{address:02d}-{slug(label)}"
        physical = {"location": label, "quantity": 2 if address in {20, 25} else 1, "notes": f"Printed controller-bank class: {bank}."}
        if address in {20, 25}:
            physical["notes"] += " The manual prints two bulbs, but the retained table exposes one directly bound emitter; the second bulb remains spatially unplaced."
        if assembly: physical["assembly_part_number"] = assembly
        if part: physical["part_number"] = part
        extra: dict[str, Any] = {"availability": "used", "aliases": [{"namespace": "manual.address", "value": str(address)}], "physical": physical, "wiring": {"board": "WPC-95 power driver board", "driver_transistor": transistor, "drive_wire": wire, "control_connection": connection, "power_connection": voltage, "voltage_type": "dc"}}
        if address in OUTPUT_POINTS:
            extra["spatial"] = located(identifier, "emitter", OUTPUT_POINTS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, status="observed" if address in {20, 25} else "validated")
        result.append(device(identifier, label, kind, "pinmame.output.solenoid", address, (MANUAL_SOURCE, VPX_SCRIPT_SOURCE), **extra))
    virtual = {
        29:("J111 General-purpose Mirror 1","used"),30:("J111 General-purpose Mirror 2","used"),31:("PinMAME Synthetic Game-On State","used"),32:("PinMAME Constant-zero State","unused"),36:("Not Used Upper Left Flipper Hold","unused"),39:("Unused WPC-95 LPDC Output 39","unused"),40:("Unused WPC-95 LPDC Output 40","unused"),41:("WPC-95 Mirror of Output 37","used"),42:("WPC-95 Mirror of Output 38","used"),43:("WPC-95 Mirror of Output 39","unused"),44:("WPC-95 Mirror of Output 40","unused"),49:("PinMAME Simulator-only Ball Shooter","unused"),50:("Reserved Before Custom-output Boundary","unused"),
    }
    for address, (label, availability) in virtual.items():
        extra: dict[str, Any] = {"availability": availability, "aliases": [], "spatial": not_applicable("virtual", CORE_SOURCE)}
        if address in {29, 30, 31}:
            extra.update({"roles": ["internal.wpc-state"], "physical": {"notes": "Synthetic PinMAME WPC state channel; it publishes controller state but is never a physical playfield device."}})
        elif address == 32:
            extra.update({"roles": ["internal.unused.wpc-output"], "physical": {"notes": "Synthetic PinMAME WPC state channel that is constant zero and has no physical device."}})
        elif address == 36:
            extra.update({"aliases": [{"namespace": "manual.address", "value": "36"}], "wiring": {"board": "WPC-95 power driver board", "driver_transistor": "Q83", "drive_wire": "ORG-GRY", "control_connection": "J120-1", "power_connection": "J119-8", "voltage_type": "dc"}, "spatial": not_applicable("unused", MANUAL_SOURCE)})
        elif address in {41, 42, 43, 44}:
            extra["aliases"] = [{"namespace": "pinmame.mirror_of", "value": str(address - 4)}]
        refs = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE) if address == 36 else (CORE_SOURCE, CONTROLLER_SOURCE)
        result.append(device(f"output.solenoid-{address:02d}-{slug(label)}", label, "coil" if address == 36 else "virtual", "pinmame.output.solenoid", address, refs, **extra))
    flippers = {
        33:("Upper Right Flipper Power", "33", "A-15849-R", "FL-11630", "J120-6", "YEL-VIO", 1),34:("Upper Right Flipper Hold", "34", "A-15849-R", "FL-11630", "J120-4", "ORG-VIO", 1),35:("Ball Launch Ramp Power", "35", "A-22010", "LE-23-1300-T", "J120-3", "YEL-GRY", 1),45:("Lower Right Flipper Power", "29", "A-14876-R-3", "FL-11629", "J120-13", "YEL-GRN", 1),46:("Lower Right Flipper Hold", "30", "A-14876-R-3", "FL-11629", "J120-11", "ORG-GRN", 1),47:("Lower Left Flipper Power", "31", "A-15849-L-2", "FL-11629", "J120-9", "YEL-BLU", 1),48:("Lower Left Flipper Hold", "32", "A-15849-L-2", "FL-11629", "J120-7", "ORG-BLU", 1),
    }
    for address, (label, manual_number, assembly, part, connection, wire, quantity) in flippers.items():
        identifier = f"output.solenoid-{address:02d}-{slug(label)}"
        result.append(device(identifier, label, "coil", "pinmame.output.solenoid", address, (MANUAL_SOURCE, CORE_SOURCE), availability="used", aliases=[{"namespace": "manual.address", "value": manual_number}], physical={"assembly_part_number": assembly, "part_number": part, "location": "flipper circuit" if address != 35 else "ball launch ramp", "quantity": quantity}, wiring={"board": "WPC-95 power driver board", "drive_wire": wire, "control_connection": connection, "power_connection": "J119", "voltage_type": "dc"}, spatial=located(identifier, "emitter", OUTPUT_POINTS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)))
    for address, label, direction, wire, connection in ((37,"Wheel Spin Counter Clock-Wise","counter-clockwise","BRN-WHT","J110-1"),(38,"Wheel Spin Clock-Wise","clockwise","ORG-WHT","J110-3")):
        result.append(device(f"output.solenoid-{address:02d}-{slug(label)}", label, "motor", "pinmame.output.solenoid", address, (MANUAL_SOURCE, CORE_SOURCE), availability="used", aliases=[{"namespace": "manual.address", "value": str(address)}], physical={"part_number": "14-7955-1", "assembly_part_number": "A-16120 DC Motor Control Board / A-22026 Motor 2-Opto Board", "location": "wheel mechanism", "quantity": 1, "notes": f"Low-power {direction} command through the motor control board."}, wiring={"board": "WPC-95 power driver board", "drive_wire": wire, "control_connection": connection, "power_connection": "J139-2", "voltage_type": "dc"}))
    aux = ((51,42,"Upper Right 1 Flasher","Q2","J4-2","BLU-BRN","A-22199-1",1),(52,43,"Upper Right 2 Flasher","Q4","J4-3","BLU-RED","A-22199-1",1),(53,44,"Upper Right 3 Flasher","Q6","J4-4","BLU-ORG","A-22199-1",1),(54,45,"Upper Playfield Right Flasher","Q8","J4-5","BLU-YEL","A-22030",2),(55,46,"Upper Playfield Left Flasher","Q10","J4-7","BLU-GRN","A-22030",2),(56,47,"Upper Left 3 Flasher","Q12","J4-8","BLU-BLK","A-22199-2",1),(57,48,"Upper Left 2 Flasher","Q14","J4-9","BLU-VIO","A-22199-2",1),(58,49,"Upper Left 1 Flasher","Q16","J4-10","BLU-GRY","A-22199-2",1))
    for address, manual_number, label, transistor, connection, wire, assembly, quantity in aux:
        identifier = f"output.solenoid-{address:02d}-{slug(label)}"
        extra: dict[str, Any] = {"availability": "used", "aliases": [{"namespace": "manual.address", "value": str(manual_number)}, {"namespace": "manual.board", "value": f"A-21773 J4 / physical solenoid {manual_number}"}], "physical": {"assembly_part_number": assembly, "part_number": "#906 / 24-8802", "location": label, "quantity": quantity}, "wiring": {"board": "Auxiliary 8-driver Board A-21773", "driver_transistor": transistor, "drive_wire": wire, "control_connection": connection, "power_connection": "J4-1", "voltage_type": "dc"}}
        if address in OUTPUT_POINTS:
            extra["spatial"] = located(identifier, "emitter", OUTPUT_POINTS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
        result.append(device(identifier, label, "flasher", "pinmame.output.solenoid", address, (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
    return sorted(result, key=lambda item: int(item["binding"]["device"]))


def lamps() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for address in MATRIX:
        label = LAMP_LABELS[address]
        identifier = f"output.lamp-{address}-{slug(label)}"
        assembly, part, socket, quantity = LAMP_PARTS[address]
        physical: dict[str, Any] = {"location": label, "quantity": quantity}
        if assembly: physical["assembly_part_number"] = assembly
        if part: physical["part_number"] = part
        if socket: physical["notes"] = f"Socket: {socket}."
        if address in {13, 28, 68}:
            physical["notes"] = physical.get("notes", "") + " The manual prints two bulbs, but the retained table exposes one directly bound lamp object; the second bulb remains spatially unplaced."
        column, row = divmod(address, 10)
        col_wire, col_connection, col_driver = LAMP_COLUMNS[column]
        row_wire, row_connection, row_driver = LAMP_ROWS[row]
        extra: dict[str, Any] = {"availability": "used", "aliases": [{"namespace": "manual.address", "value": str(address)}], "physical": physical, "wiring": {"board": "WPC-95 power driver board", "drive_wire": col_wire, "drive_connection": col_connection, "return_wire": row_wire, "return_connection": row_connection, "driver_transistor": f"column {col_driver}; row {row_driver}"}}
        if address == 88:
            extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
        else:
            extra["spatial"] = located(identifier, "emitter", LAMP_POINTS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, status="observed" if address in {13, 28, 68} else "validated")
        result.append(device(identifier, label, "lamp", "pinmame.output.lamp", address, (MANUAL_SOURCE, VPX_SCRIPT_SOURCE), **extra))
    return result


def gi() -> list[dict[str, Any]]:
    rows = (
        (0,"Left Side String","WHT-BRN","J106-7","J106-1","#555, #545","playfield; VPX GIleft collection is an unquantified presentation proxy"),
        (1,"Right Side String","WHT-ORG","J106-8","J106-2","#555, #545","playfield; VPX GIright collection is an unquantified presentation proxy"),
        (2,"Gofer Spotlight","WHT-YEL","J106-9 / J105-9","J106-3 / J105-3","#44 playfield; #555, #545 insert","playfield and insert panel"),
        (3,"Illumination String 4","WHT-GRN","J105-10","J105-5","#44","insert panel; printed always on"),
        (4,"Illumination String 5","WHT-VIO","J105-11 / J104-1","J105-6 / J104-3","#44","insert panel and coin door; printed always on"),
    )
    result = []
    for address, label, wire, control, return_connection, part, note in rows:
        identifier = f"output.gi-{address}-{slug(label)}"
        extra: dict[str, Any] = {"availability": "used", "aliases": [{"namespace": "manual.address", "value": f"{address + 1:02d}"}], "physical": {"part_number": part, "location": note, "quantity": 1, "notes": "The manual identifies circuit destinations and bulb types, not a per-string bulb count."}, "wiring": {"board": "WPC-95 power driver board", "drive_wire": wire, "control_connection": control, "return_connection": return_connection, "voltage_type": "ac", "nominal_voltage_v": 6.8}, "range": {"minimum": 0, "maximum": 8, "steps": 9}}
        # No collection member is promoted to a physical bulb coordinate: the retained script runs UseGI=0,
        # its collections are presentation proxies, and the manual has no calibrated string layout.
        if address >= 3:
            extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
        result.append(device(identifier, label, "gi", "pinmame.output.gi", address, (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
    return result


def mechanisms() -> list[dict[str, Any]]:
    return [
        {"id":"mechanism.trough","label":"Six-ball trough and eject","kind":"kicker","actuators":["output.solenoid-09-trough-eject"],"sensors":[f"switch.matrix-{n}" for n in (31,32,33,34,35,36,37)],"behavior":"The retained VPX bsTrough models switches 32-37 as six ball positions and pulses normally-closed opto 31 while solenoid 9 fires the BallRelease kicker. The manual names all seven physical opto positions.","assembly_part_number":"A-18753","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.shooter-and-auto-fire","label":"Shooter lane and auto fire","kind":"kicker","actuators":["output.solenoid-01-auto-fire"],"sensors":["switch.matrix-18"],"behavior":"Auto Fire releases from the shooter assembly; the VPX callback binds solenoid 1 to Plunger1 and the manual identifies the Shooter Groove switch.","assembly_part_number":"A-22204","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.kickback","label":"Left outlane kickback","kind":"kicker","actuators":["output.solenoid-02-kickback"],"sensors":["switch.matrix-28","switch.matrix-16"],"behavior":"Solenoid 2 drives the Kickback plunger. It returns a ball from the left outlane when the kickback switch is hit.","assembly_part_number":"B-11873","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.putt-out-and-underground-pass","label":"Putt Out popper, Clubhouse kicker, and underground pass","kind":"kicker","actuators":["output.solenoid-03-clubhouse-kicker","output.solenoid-24-underground-pass"],"sensors":["switch.matrix-44","switch.matrix-25","switch.matrix-67","switch.matrix-68"],"behavior":"The Putt Out ball stack uses normally-closed switch 44. Solenoid 3 kicks it back to the playfield; solenoid 24 routes it into the underground pass/Jet Popper path. The script chains hole-in-one 68 through behind-left-gofer 67 back to Putt Out.","assembly_part_number":"A-21989","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.left-gofer-and-ramp","label":"Left Bud gofer and drop ramp","kind":"toy","actuators":["output.solenoid-04-left-gofer-up","output.solenoid-15-left-gofer-down","output.solenoid-27-left-ramp-down"],"sensors":["switch.matrix-41","switch.matrix-47","switch.matrix-65","switch.matrix-66"],"behavior":"The coupled left assembly raises the gofer and ramp with solenoid 4, drops the gofer with 15, and allows the ramp to lower with 27 only after the gofer is down. PinMAME and the retained VPX script both implement that state order.","assembly_part_number":"A-21815-2","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.right-gofer-and-ramp","label":"Right Buzz gofer and drop ramp","kind":"toy","actuators":["output.solenoid-05-right-gofer-up","output.solenoid-16-right-gofer-down","output.solenoid-28-right-ramp-down"],"sensors":["switch.matrix-42","switch.matrix-48","switch.matrix-73","switch.matrix-75","switch.matrix-76"],"behavior":"The coupled right assembly raises the gofer and ramp with solenoid 5, drops the gofer with 16, and lowers the ramp with 28 only after the gofer is down. Switch 73 is the Right Ramp Made switch.","assembly_part_number":"A-21815-1","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.jet-popper","label":"Jet Popper","kind":"kicker","actuators":["output.solenoid-06-jet-popper"],"sensors":["switch.matrix-38"],"behavior":"The normally-closed Jet Popper opto feeds the retained bsJetPopper kicker, which solenoid 6 ejects at 180 degrees.","assembly_part_number":"A-21988","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.sand-trap-eject","label":"Sand Trap left eject","kind":"kicker","actuators":["output.solenoid-07-left-eject"],"sensors":["switch.matrix-78"],"behavior":"The retained bsLeftEject saucer is the manual's Left Eject coil and Sand Trap Eject switch assembly.","assembly_part_number":"A-20496-1","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.upper-right-eject","label":"Upper right popper","kind":"kicker","actuators":["output.solenoid-08-upper-right-eject"],"sensors":["switch.matrix-45","switch.matrix-46"],"behavior":"Right Popper Jam and Right Popper are both normally-closed optos in the upper-right eject path. The retained bsUpperRightEject kicks from the upperrightkicker object when solenoid 8 fires.","assembly_part_number":"A-22022","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.slingshots","label":"Left and right slingshots","kind":"other","actuators":["output.solenoid-10-left-slingshot","output.solenoid-11-right-slingshot"],"sensors":["switch.matrix-51","switch.matrix-52"],"behavior":"The two slingshot callbacks pulse their matching score switches; the manual records separate left/right coil assemblies and score-switch diode construction.","assembly_part_number":"A-22207-2 / A-22206-2","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.jet-bumpers","label":"Three jet bumpers","kind":"other","actuators":["output.solenoid-12-top-jet-bumper","output.solenoid-13-middle-jet-bumper","output.solenoid-14-bottom-jet-bumper"],"sensors":["switch.matrix-53","switch.matrix-54","switch.matrix-55"],"behavior":"Top, middle, and bottom jet bumper callbacks pulse their corresponding score switches and use the three printed AE-26-1200 coil assemblies.","assembly_part_number":"A-22205-2","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.slam-ramp","label":"Ball Launch / slam ramp","kind":"diverter","actuators":["output.solenoid-35-ball-launch-ramp-power"],"sensors":["switch.matrix-68"],"behavior":"The printed Upper Left Flipper power circuit is repurposed as the Ball Launch Ramp. The VPX SolSlamRamp callback lowers its collision ramp, then timers restore it; the paired hold circuit 36 is unfitted.","assembly_part_number":"A-22010","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.wheel-and-golf-cart","label":"Wheel motor, two optos, and golf cart","kind":"motorized","actuators":["output.solenoid-37-wheel-spin-counter-clock-wise","output.solenoid-38-wheel-spin-clock-wise"],"sensors":["switch.matrix-63","switch.matrix-64","switch.matrix-71","switch.matrix-72","switch.matrix-74"],"behavior":"A 14-7955-1 wheel motor is driven both directions through A-16120. A-22026 carries the shared inner/outer optos at switches 63/64. PinMAME models 16 wheel positions; the retained VPX separately presents the Golf Cart and its two cart-path switches, so it is not falsely treated as a motor mirror.","assembly_part_number":"A-16120 / A-22026","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE,CORE_SOURCE)},
        {"id":"mechanism.captive-ball-and-kick-bank","label":"Captive ball, Advance Trap, and K-I-C-K bank","kind":"other","actuators":[],"sensors":["switch.matrix-77","switch.matrix-81","switch.matrix-82","switch.matrix-83","switch.matrix-84","switch.matrix-85","switch.matrix-86"],"behavior":"The retained script supplies a cvpmCaptiveBall for switch 86 and discrete HitTarget callbacks for Advance Trap, K-I-C-K Advance, and the four K-I-C-K letter switches. No physical actuator is claimed where the manual supplies none.","provenance":provenance(MANUAL_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.lower-flippers","label":"Lower left and right flippers","kind":"other","actuators":["output.solenoid-45-lower-right-flipper-power","output.solenoid-46-lower-right-flipper-hold","output.solenoid-47-lower-left-flipper-power","output.solenoid-48-lower-left-flipper-hold"],"sensors":["switch.flipper-f1","switch.flipper-f2","switch.flipper-f3","switch.flipper-f4"],"behavior":"The lower flippers use paired power/hold FL-11629 coils and dedicated EOS/cabinet opto inputs. PinMAME publishes the manual 29-32 circuits at public 45-48.","assembly_part_number":"A-14876-R-3 / A-15849-L-2","provenance":provenance(MANUAL_SOURCE,CORE_SOURCE,VPX_SCRIPT_SOURCE)},
        {"id":"mechanism.upper-right-flipper","label":"Upper right flipper","kind":"other","actuators":["output.solenoid-33-upper-right-flipper-power","output.solenoid-34-upper-right-flipper-hold"],"sensors":["switch.flipper-f5","switch.flipper-f6"],"behavior":"No Good Gofers fits the upper-right FL-11630 power/hold flipper and F5/F6 inputs. F7/F8 are expressly unfitted: there is no upper-left flipper.","assembly_part_number":"A-15849-R","provenance":provenance(MANUAL_SOURCE,CORE_SOURCE,VPX_SCRIPT_SOURCE)},
    ]


def relationships() -> list[dict[str, Any]]:
    return [
        {"id":"relationship.left-gofer-down-sensor","kind":"direct","source":"output.solenoid-15-left-gofer-down","destination":"switch.matrix-41","provenance":provenance(VPX_SCRIPT_SOURCE,CORE_SOURCE)},
        {"id":"relationship.right-gofer-down-sensor","kind":"direct","source":"output.solenoid-16-right-gofer-down","destination":"switch.matrix-42","provenance":provenance(VPX_SCRIPT_SOURCE,CORE_SOURCE)},
    ]


def drivers() -> list[dict[str, Any]]:
    catalog = load_json(ROOT / "catalog/pinmame.json")
    by_id = {record["id"]: record for record in catalog["drivers"]}
    result = []
    for identifier in DRIVER_IDS:
        record = by_id[identifier]
        item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
        if record.get("clone_of"):
            item["clone_of"] = record["clone_of"]
        item["physical_compatibility"] = "identical"
        item["variant_notes"] = DRIVER_NOTES[identifier]
        result.append(item)
    return result


def conflicts() -> list[dict[str, Any]]:
    return []


def build() -> dict[str, Any]:
    definition = {"format":"pinmame-machine-definition","schema_version":2,"machine":{"id":"williams.no-good-gofers.1997","name":"No Good Gofers","manufacturer":"Williams","year":1997,"kind":"physical_pinball","playfield":{"width":TABLE_WIDTH,"height":TABLE_HEIGHT,"units":"vpx","provenance":provenance(VPX_TABLE_SOURCE)}},"coverage":{"status":"partial","missing":["spatial_placement"],"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"validated","physical_wiring":"validated","mechanisms":"validated","variant_coverage":"validated","recreation_knowledge":"validated","spatial_placement":"candidate"}},"controller":{"platform":"pinmame.wpc-95","hardware_generation":"0x80","inversion_applied_by_emulator":True},"drivers":drivers(),"inputs":inputs(),"outputs":solenoids()+lamps()+gi(),"displays":[{"id":"display.dmd","label":"128x32 dot-matrix display","kind":"dmd","controller_index":0,"width":128,"height":32,"spatial":not_applicable("cabinet_or_service",MANUAL_SOURCE,CORE_SOURCE),"provenance":provenance(MANUAL_SOURCE,CORE_SOURCE)}],"mechanisms":mechanisms(),"relationships":relationships(),"sources":sources(),"knowledge":{"path":"knowledge/williams/no-good-gofers-1997.md","status":"complete"},"conflicts":conflicts()}
    ids = [item["id"] for item in definition["inputs"] + definition["outputs"]]
    duplicates = sorted({identifier for identifier in ids if ids.count(identifier) > 1})
    if duplicates:
        raise RuntimeError(f"No Good Gofers has duplicate device IDs: {duplicates}")
    return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
    unresolved_inputs = []
    resolved_inputs = []
    controlled_inputs: dict[str, list[int]] = {}
    resolved_outputs = []
    controlled_outputs: dict[str, list[dict[str, Any]]] = {}
    unresolved_outputs: list[dict[str, Any]] = []
    partially_placed_outputs: list[dict[str, Any]] = []
    placement_count = 0
    for item in definition["inputs"]:
        spatial = item.get("spatial")
        address = int(item["binding"]["device"])
        if spatial is None:
            unresolved_inputs.append(address)
        elif spatial["status"] == "not_applicable":
            controlled_inputs.setdefault(spatial["reason"], []).append(address)
        else:
            resolved_inputs.append(address); placement_count += len(spatial["placements"])
    for item in definition["outputs"]:
        spatial = item.get("spatial")
        binding = {"group":item["binding"]["group"],"address":int(item["binding"]["device"])}
        if spatial is None:
            unresolved_outputs.append({**binding,"reason":"no one-to-one retained VPX object; see blockers"})
            continue
        if spatial["status"] == "not_applicable":
            controlled_outputs.setdefault(spatial["reason"], []).append(binding)
        else:
            resolved_outputs.append(binding); placement_count += len(spatial["placements"])
            quantity = item.get("physical",{}).get("quantity")
            placement_count_for_device = len(spatial["placements"])
            if quantity and placement_count_for_device < quantity:
                partially_placed_outputs.append({**binding,"physical_quantity":quantity,"placement_count":placement_count_for_device,"reason":"retained VPX exposes fewer directly bound emitters than the manual's physical bulb quantity"})
    return {"format":"pinmame-spatial-blockers","version":1,"machine_id":definition["machine"]["id"],"status":"validated","blockers":["Several physical switches and outputs have no one-to-one retained VPX playfield object (notably the individual six-trough optos, mechanical ramp-down sensors, several gofer hit switches, both wheel optos, slingshot coils, ramp-drop coils, both wheel motor directions, and upper-playfield flasher pairs). They intentionally omit spatial coordinates rather than reusing a mechanism anchor or a presentation proxy.","Five two-bulb devices have only one directly bound retained-VPX emitter: lamp addresses 13, 28, and 68 plus solenoid/flashers 20 and 25. Their single retained placement is observed rather than complete, and each missing second bulb remains explicit.","GI 0-2 are real playfield circuits in the manual, but the known-working VPX script sets UseGI=0 and its GI collections are presentation proxies with no manual-calibrated bulb-to-coordinate correspondence. They intentionally receive no fabricated playfield placement."],"coordinate_convention":{"space":"playfield","source_bounds":{"left":0.0,"top":0.0,"right":TABLE_WIDTH,"bottom":TABLE_HEIGHT},"x":"x/964; 0=left, 1=right","y":"y/2162; 0=rear/backglass, 1=apron/player"},"extraction":{"fail_closed":True,"file_count":EXTRACTION_FILE_COUNT,"manifest_algorithm":"Canonical JSON containing format/version and every sorted relative POSIX extracted path, byte size, and SHA-256.","manifest_sha256":MANIFEST_SHA256,"manifest_uri":"external:pinmame-vpx-sources/williams/no-good-gofers-1997/extracted-vpxtool.manifest.json","source_ref":VPX_EXTRACTION_SOURCE,"total_bytes":EXTRACTION_TOTAL_BYTES,"vpxtool_version":"git:v0.33.3"},"source_hashes":{"embedded_script_sha256":SCRIPT_SHA256,"manual_sha256":MANUAL_SHA256,"table_sha256":TABLE_SHA256},"placement_count":placement_count,"resolved_input_addresses":sorted(resolved_inputs),"resolved_output_bindings":sorted(resolved_outputs,key=lambda item:(item["group"],item["address"])),"unresolved_output_bindings":sorted(unresolved_outputs,key=lambda item:(item["group"],item["address"])),"partially_placed_output_bindings":sorted(partially_placed_outputs,key=lambda item:(item["group"],item["address"])),"not_applicable_inputs":{key:sorted(value) for key,value in sorted(controlled_inputs.items())},"not_applicable_outputs":{key:sorted(value,key=lambda item:(item["group"],item["address"])) for key,value in sorted(controlled_outputs.items())},"unresolved_input_addresses":sorted(unresolved_inputs),"unresolved":[{"group":"pinmame.input.switch","address":address,"reason":"no one-to-one retained VPX object; see blockers"} for address in sorted(unresolved_inputs)],"excluded_object_classes":["VPX visual overlay lights (Lnnna/Lnnnb) where the script uses one source lamp for multiple presentation effects","upperplayfield texture controlled by script lamps 145/146; it is a presentation proxy, not four manual #906 bulb coordinates","GIleft/GIright/GIother collections because UseGI=0 and the manual does not provide individual bulb coordinate calibration"],"visual_review_cache":{"root":"external:pinmame-manuals/rendered/williams.no-good-gofers.1997/","manual_pages":["p-102.png","p-104.png","p-105.png","p-111.png","p-112.png","p-113.png","p-125.png","p-137.png","p-138.png","p-144.png"]}}


def render_spatial_report(report: dict[str, Any]) -> str:
    return "\n".join(["# No Good Gofers (Williams, 1997) spatial review","",f"Status: {report['status']}. The machine is deliberately partial: {', '.join(build()['coverage']['missing'])} remains a fail-closed blocker.","",f"The retained known-working VPX table is SHA-256 `{TABLE_SHA256}`; its extracted script is `{SCRIPT_SHA256}`. Exact table bounds are `{TABLE_BOUNDS}`. Every located point is a named retained object center normalized as x/964, y/2162 (left/rear origin convention).","","## Spatial decision","",* [f"- {item}" for item in report["blockers"]],"",f"- Located placements: {report['placement_count']}",f"- Inputs with direct retained coordinates: {len(report['resolved_input_addresses'])}",f"- Inputs intentionally unresolved: {report['unresolved_input_addresses']}",f"- Outputs intentionally unresolved: {[(item['group'],item['address']) for item in report['unresolved_output_bindings']]}",f"- Outputs with incomplete physical-quantity placement: {[(item['group'],item['address'],item['placement_count'],item['physical_quantity']) for item in report['partially_placed_output_bindings']]}","", "## Extraction identity", "", f"- {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes; canonical manifest SHA-256 `{MANIFEST_SHA256}`.","", "## Promotion decision", "", "The definition must not be promoted. It records every coordinate that has a direct named retained-VPX binding and leaves the rest absent instead of converting manual drawing callouts, mechanism anchors, or VPX presentation proxies into invented physical coordinates.", ""])


def generate(root: Path = ROOT) -> Path:
    definition = build()
    write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
    write_json(root / SEED_PATH.relative_to(ROOT), definition)
    report = build_spatial_report(definition)
    write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
    write_text(root / SPATIAL_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
    stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
    if stale.exists():
        stale.unlink()
    return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
        raise RuntimeError("Stale No Good Gofers author-ready definition is present")
    definition = build(); expected = canonical_bytes(definition)
    for path, message in ((root / DEFINITION_PATH.relative_to(ROOT), "definition"),(root / SEED_PATH.relative_to(ROOT), "seed")):
        if not path.is_file() or path.read_bytes() != expected:
            raise RuntimeError(f"No Good Gofers {message} drifted from its deterministic curator: {path}")
    report = build_spatial_report(definition)
    report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
    markdown_path = root / SPATIAL_MARKDOWN_PATH.relative_to(ROOT)
    if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
        raise RuntimeError(f"No Good Gofers spatial report drifted: {report_path}")
    if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
        raise RuntimeError(f"No Good Gofers spatial markdown drifted: {markdown_path}")
    print("No Good Gofers definition, seed, and spatial report match the deterministic curator.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()
    if args.regenerate:
        print(f"Wrote {generate(ROOT)}")
    elif args.check:
        check(ROOT)
    else:
        source_root = configured_vpx_sources_root(required=True)
        assert source_root is not None
        verify_extraction_manifest(source_root)
        print("No Good Gofers retained extraction matches its pinned manifest identity.")


if __name__ == "__main__":
    main()
