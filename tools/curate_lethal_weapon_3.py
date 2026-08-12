"""Curate the physical Data East Lethal Weapon 3 (1992) machine definition.

Side-effect free and deterministic. The transcribed manual tables, the normalized coordinates
resolved from the retained recreation, and the ROM inventory parsed from pinned PinMAME are all
embedded as literals below, so ``--regenerate`` reproduces the canonical artifacts byte-for-byte
without reading any external evidence root. ``--check`` refuses drift.

The definition, the spatial report and the knowledge note are all generated here from the same
objects, so prose cannot outlive the data behind it. The comparison folds CRLF to LF first, so a
checkout Git rewrote under ``core.autocrlf=true`` still passes while every other byte difference
still fails; see ``_comparable``.

This file is the maintained curator. Edit it and use ``--regenerate`` to refresh the canonical
artifacts; use ``--check`` to refuse drift.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/data-east/lethal-weapon-3-1992.json"
SEED_PATH = ROOT / "tools/seeds/data-east/lethal-weapon-3-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/lethal-weapon-3-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/lethal-weapon-3-1992.md"

TRANSCRIPTION = json.loads("{\n  \"addendum\": {\n    \"dated\": \"1992-07-02\",\n    \"display_correction\": {\n      \"affects\": \"manual printed page 23\",\n      \"printed\": \"The display is made up of 32 X 128 Dots not 32 X 64 Dots.\",\n      \"significance\": \"The manual as printed states the DMD is 32x64. The addendum corrects it to 32x128, which is what pinned PinMAME independently declares: lw3 uses de_128x32DMD and SNDBRD_DEDMD32 under GEN_DEDMD32. Without the addendum the manual and the emulator would appear to disagree about the display.\"\n    },\n    \"note\": \"A two-page factory addendum issued after the manual was published. It is a primary correction to the manual, not a secondary source.\",\n    \"part_revisions\": {\n      \"ball_eject_fiber_link\": \"545-5062-00 is a Nylon Link\",\n      \"ball_feed_fulcrum_bracket\": \"535-6446-01\",\n      \"flipper_button\": \"500-5026-32\",\n      \"flipper_coil\": \"23-1100 (090-5030-00)\",\n      \"flipper_plunger_and_link_assembly\": \"515-5052-00 (added)\",\n      \"flipper_return_spring\": \"265-5030-00\",\n      \"flipper_spring_bracket\": \"535-6469-00\",\n      \"gun_assembly_nyliner\": \"545-5352-00\",\n      \"left_flipper_assembly\": \"500-5606-74\",\n      \"right_flipper_assembly\": \"500-5606-73\",\n      \"spinning_light_assembly\": \"500-5365-01\",\n      \"usa_coin_door\": \"500-5018-17\"\n    }\n  },\n  \"auxiliary_solenoids\": {\n    \"17\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-7\",\n        \"wire\": \"BLU-BRN\"\n      },\n      \"name\": \"Left Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q11\"\n    },\n    \"18\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-4\",\n        \"wire\": \"BLU-RED\"\n      },\n      \"name\": \"Center Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q9\"\n    },\n    \"19\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-3\",\n        \"wire\": \"BLU-ORN\"\n      },\n      \"name\": \"Right Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q8\"\n    },\n    \"20\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-6\",\n        \"wire\": \"BLU-YEL\"\n      },\n      \"name\": \"Left Slingshot\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q10\"\n    },\n    \"21\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-8\",\n        \"wire\": \"BLU-GRN\"\n      },\n      \"name\": \"Right Slingshot\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q12\"\n    },\n    \"22\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-9\",\n        \"wire\": \"BLU-BLK\"\n      },\n      \"name\": \"Kickback\",\n      \"note\": \"Printed 'Kickback (See Schematic)'. The legacy migrated record also names address 22 Kickback, so the two agree.\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q13\"\n    }\n  },\n  \"coil_drivers\": {\n    \"direct\": {\n      \"10\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"Left/Right Coil Relay\",\n        \"note\": \"Printed 'L/R COIL RELAY'. This is sxx.muxSol, which INITGAMES11 sets to 10 for every game it defines, and it is what re-publishes outputs 1-8 at 25-32. The legacy migrated record for this machine omits address 10 entirely.\",\n        \"transistor\": \"Q29\",\n        \"wire\": \"BLK-RED\"\n      },\n      \"11\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"General Illumination Relay\",\n        \"note\": \"Printed 'GENERAL ILLUM. RELAY', relay K-1 at P.S. board CN7-1/3. Matches s11.c's own '// GI output' comment for the lw3_ typing block. The legacy migrated record also names it GI Relay, so the manual, pinned source and the superseded record all agree.\",\n        \"transistor\": \"Q28\",\n        \"wire\": \"BRN-ORN\"\n      },\n      \"12\": {\n        \"coil_type\": \"23-800\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Ball Launch\",\n        \"note\": \"Driven through Q4 at +50 V.\",\n        \"transistor\": \"Q27\",\n        \"wire\": \"BRN-YEL\"\n      },\n      \"13\": {\n        \"connector\": \"CN-12\",\n        \"name\": null,\n        \"note\": \"Printed 'NO COIL AT THIS LOCATION'. The mars light is drawn on a node this drive touches, but the retained known-working script binds the beacon to drive 14, not 13, so nothing is fitted here.\",\n        \"transistor\": \"Q26\",\n        \"wire\": \"BRN-GRN\"\n      },\n      \"14\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"Mars Light Beacon\",\n        \"note\": \"The Special Coil Wiring Diagram draws a MARS LIGHT through a GRY lead, a 1 AMP S.B. fuse and a BLU lead to PSCN 4 on a node that both this drive and drive 13 touch, and the drawing alone does not say which energises it. The retained known-working script settles it: SolCallback(14) = \\\"SolRotateBeacons\\\", commented 'Mars Light aka Beacon'. The printed table gives this drive no coil type, so the identification is the script's rather than the manual's.\",\n        \"transistor\": \"Q25\",\n        \"wire\": \"BRN-BLU\"\n      },\n      \"15\": {\n        \"coil_type\": \"23-800\",\n        \"connector\": \"CN-12\",\n        \"name\": \"VUK\",\n        \"note\": \"Driven through Q2 at +50 V; the diagram also marks (4) playfield lamps on this branch.\",\n        \"transistor\": \"Q24\",\n        \"wire\": \"WHT-VIO\"\n      },\n      \"16\": {\n        \"bulbs\": \"(4)\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Flash Lamps\",\n        \"note\": \"Through R-14 to four lamps on the ORG return.\",\n        \"transistor\": \"Q23\",\n        \"wire\": \"BRN-GRY\"\n      },\n      \"9\": {\n        \"bulbs\": \"(4) No. 89\",\n        \"connector\": \"CN-12\",\n        \"name\": \"IWSC Building Flash Lamps\",\n        \"note\": \"Printed '(4) IWSC BUILDING'.\",\n        \"transistor\": \"Q30\",\n        \"wire\": \"BRN-BLK\"\n      }\n    },\n    \"muxed\": {\n      \"1\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Outhole\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"2 playfield, 2 insert\"\n        },\n        \"transistor\": \"Q46\",\n        \"wire\": \"GRY-BRN\"\n      },\n      \"2\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Trough Eject\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"3 back panel, 1 playfield\"\n        },\n        \"transistor\": \"Q45\",\n        \"wire\": \"GRY-RED\"\n      },\n      \"3\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"name\": null,\n          \"note\": \"Printed 'NO COIL THIS LOCATION'; the +50VR/+32VR supply block is still drawn\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"3 playfield, 1 insert\"\n        },\n        \"transistor\": \"Q44\",\n        \"wire\": \"GRY-ORN\"\n      },\n      \"4\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Left Eject\"\n        },\n        \"right\": {\n          \"bulbs\": \"(3) No. 89\",\n          \"placement\": \"3 playfield\"\n        },\n        \"transistor\": \"Q43\",\n        \"wire\": \"GRY-YEL\"\n      },\n      \"5\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Right Eject\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"2 playfield, 2 insert\"\n        },\n        \"transistor\": \"Q42\",\n        \"wire\": \"GRY-GRN\"\n      },\n      \"6\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Left 3 Bank\"\n        },\n        \"right\": {\n          \"bulbs\": \"(3) No. 89\",\n          \"placement\": \"3 playfield\"\n        },\n        \"transistor\": \"Q41\",\n        \"wire\": \"GRY-BLU\"\n      },\n      \"7\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Right 3 Bank\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"2 playfield, 2 insert\"\n        },\n        \"transistor\": \"Q40\",\n        \"wire\": \"GRY-VIO\"\n      },\n      \"8\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Knocker\",\n          \"note\": \"50 V, driven through Q5 TIP36C\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"placement\": \"3 playfield, 1 insert\"\n        },\n        \"transistor\": \"Q39\",\n        \"wire\": \"GRY-BLK\"\n      }\n    }\n  },\n  \"document\": {\n    \"bytes\": 10482189,\n    \"character_count\": 0,\n    \"extraction_status\": \"ocr_required\",\n    \"page_count\": 93,\n    \"text_page_count\": 0\n  },\n  \"document_sha256\": \"e285463cbee4fc69384b1690add6e3da4ddfc5d08245515cbc652dd179492ce5\",\n  \"flipper_solenoids\": {\n    \"left\": {\n      \"assembly\": \"090-5030-00\",\n      \"coil_type\": \"23-1100\",\n      \"control\": {\n        \"connector\": \"CPU CN19-2\",\n        \"wire\": \"ORN-GRY\"\n      },\n      \"flipper_pcb\": {\n        \"connector\": \"CN1-9\",\n        \"wire\": \"BLU-GRY\"\n      },\n      \"power\": {\n        \"connector\": \"CN2-1,2\",\n        \"wire\": \"GRY-YEL\"\n      }\n    },\n    \"note\": \"Printed as its own unnumbered 'Flipper Solenoids' table listing a left and a right flipper only - no upper flipper of either hand. Consistent with lw3GameData declaring FLIP1516 (FLIP_SWNO(15,16)) and no FLIP_SOL. Coil type 23-1100 is independently confirmed by the addendum's flipper-assembly parts table, item 12.\",\n    \"right\": {\n      \"assembly\": \"090-5030-00\",\n      \"coil_type\": \"23-1100\",\n      \"control\": {\n        \"connector\": \"CPU CN19-1\",\n        \"wire\": \"ORN-VIO\"\n      },\n      \"flipper_pcb\": {\n        \"connector\": \"CN1-1\",\n        \"wire\": \"BLU-VIO\"\n      },\n      \"power\": {\n        \"connector\": \"CN1-1\",\n        \"wire\": \"BLK-WHT\"\n      }\n    }\n  },\n  \"format\": \"pinmame-manual-transcription\",\n  \"lamp_matrix\": {\n    \"1\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip Bottom 1\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"10\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"3 Million\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"11\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bonus Multiplier\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"12\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Lite Super Leo Getz\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"13\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Lite Video\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"14\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Start Crazy Riggs\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"15\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Freeway Loops\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"16\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Lethal Weap.1,23 10 Mill.\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"17\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Shoot Again\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"18\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Murtough's Retire\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"19\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Center Drop Tar. Left\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"2\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip 2\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"20\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Center Drop Tar. Mid.\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"21\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Center Drop Tar. Right\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"22\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Drop Tar. Top\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"23\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Drop Tar. Mid.\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"24\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Drop Tar. Bot.\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"25\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Lite Karate Kick\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"26\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Million Plus\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"27\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Subway\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"28\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"2X\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"29\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"4X\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"3\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip 3\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"30\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"6X\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"31\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"8X\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"32\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Bonus Multiplier & Hold\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"33\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Cab.-Start Button\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"34\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Center Turbo Bumper\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"35\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Top Left Lane\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"36\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Top Middle Lane\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"37\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Top Right Lane\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"38\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Collect 1 L.W.123\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"39\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Lite Jackpot 1\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"4\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip 4\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"40\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Extra Ball\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"41\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Ramp Looping\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"42\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Double Jackpot\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"43\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Victory Lap\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"44\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Silent Alarm\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"45\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Left Bank 1 Top\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"46\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Left Bank 2\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"47\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Left Bank 3\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"48\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Left Bank 4 Bot.\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"49\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"3 Million\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"5\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip 5\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"50\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"6 Million\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"51\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"9 Million\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"52\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"12 Million\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"53\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"15 Million\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"54\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Collect 2 L.W.123\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"55\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Lite Jackpot 2\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"56\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Video Mode\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"57\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Karate Kick\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"58\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Collect Jackpot\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"59\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Freeway For Extra Ball\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"6\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"UziClip Top 6\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"60\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Left Turbo Bumper\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"61\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Right Turbo Bumper\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"62\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Collect 3 L.W.123\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"63\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Lite Jackpot 3\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"64\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Leo Getz\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"7\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Fire Uzi\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"8\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Bullet Proof Vest\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"9\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Start Getaway\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    }\n  },\n  \"machine_id\": \"data-east.lethal-weapon-3.1992\",\n  \"note\": \"Hand-transcribed from 400 dpi renders of the contributor-supplied operations manual. That document has no text layer at all (93 pages, 93 bytes of form feeds), so nothing here came from pdftotext. Both matrices are printed column-major: address = (column-1)*8 + row, which matches pinned PinMAME's core_m2swSeq(col,row) = col*8+row-7 rather than any col*10+row WPC convention.\",\n  \"pages\": {\n    \"lamp_locations\": {\n      \"pdf\": 31,\n      \"printed\": 27\n    },\n    \"lamp_matrix\": {\n      \"pdf\": 30,\n      \"printed\": 26\n    },\n    \"solenoids\": {\n      \"pdf\": 32,\n      \"printed\": 28\n    },\n    \"special_coil_wiring\": {\n      \"pdf\": 33,\n      \"printed\": 29\n    },\n    \"switch_locations\": {\n      \"pdf\": 29,\n      \"printed\": 25\n    },\n    \"switch_matrix\": {\n      \"pdf\": 28,\n      \"printed\": 24\n    }\n  },\n  \"resolved_by_script\": [\n    {\n      \"detail\": \"Printed drawing ambiguous between drives 13 and 14; resolved to drive 14 by the retained known-working script's own SolCallback(14) = SolRotateBeacons, commented 'Mars Light aka Beacon'. Drive 13 carries no device.\",\n      \"id\": \"mars-light-drive\"\n    }\n  ],\n  \"switch_matrix\": {\n    \"1\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Plumb Tilt\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"10\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Outhole\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"11\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #1 Left\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"12\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #2 Center\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"13\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #3 Right\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"14\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Shooter Lane\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"15\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Left EOS\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"16\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Right EOS\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"17\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left 4 Bank Top 4\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"18\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left 4 Bank Mid. 3\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"19\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left 4 Bank Mid. 2\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"2\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"4th Coin\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"20\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left 4 Bank Bot. 1\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"21\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left Orbit Rollover\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"22\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Right Orbit Rollover\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"23\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"24\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"25\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Center Drop Tar. Left\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"26\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Center Drop Tar. Mid.\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"27\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Center Drop Tar. Right\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"28\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Left Outlane\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"29\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Left Return\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"3\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Credit Button\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"30\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Left Slingshot\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"31\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"VUK\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"32\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Right Saucer\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"33\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Drop Tar. Top\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"34\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Drop Tar. Mid.\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"35\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Drop Tar. Bot.\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"36\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Outlane\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"37\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Return\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"38\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Right Slingshot\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"39\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left Stand-Up Target\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"4\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Right Coin\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"40\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left Saucer\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"41\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Left Top Lane\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"42\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Center Top Lane\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"43\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right Top Lane\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"44\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Left Turbo Bumper\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"45\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Center Turbo Bumper\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"46\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right Turbo Bumper\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"47\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Left Spinner\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"48\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right Spinner\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"49\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Ramp Entrance\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"5\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Center Coin\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"50\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Ramp Exit\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"51\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"52\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Right 10 Point\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"53\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"54\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Left Orbit R.O. Back Up\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"55\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Right Orbit R.O. Back Up\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"56\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"57\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"58\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"59\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"6\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Left Coin\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"60\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"61\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"62\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"63\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"64\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"7\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Slam Tilt\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"8\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"9\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Launch Trigger\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    }\n  },\n  \"unresolved\": [],\n  \"version\": 1\n}")
RESOLUTION = json.loads("{\n  \"binding_routes\": {\n    \"10\": \"script-handler\",\n    \"11\": \"script-handler\",\n    \"12\": \"script-handler\",\n    \"13\": \"script-handler\",\n    \"14\": \"name-convention\",\n    \"21\": \"script-handler\",\n    \"22\": \"script-handler\",\n    \"25\": \"name-convention\",\n    \"26\": \"name-convention\",\n    \"27\": \"name-convention\",\n    \"28\": \"script-handler\",\n    \"29\": \"script-handler\",\n    \"30\": \"script-handler\",\n    \"31\": \"name-convention\",\n    \"32\": \"name-convention\",\n    \"33\": \"name-convention\",\n    \"34\": \"name-convention\",\n    \"35\": \"name-convention\",\n    \"36\": \"script-handler\",\n    \"37\": \"script-handler\",\n    \"38\": \"script-handler\",\n    \"40\": \"name-convention\",\n    \"41\": \"script-handler\",\n    \"42\": \"script-handler\",\n    \"43\": \"script-handler\",\n    \"44\": \"script-handler\",\n    \"45\": \"script-handler\",\n    \"46\": \"script-handler\",\n    \"47\": \"script-handler\",\n    \"48\": \"script-handler\",\n    \"49\": \"script-handler\",\n    \"50\": \"script-handler\",\n    \"52\": \"script-handler\",\n    \"54\": \"script-handler\",\n    \"55\": \"script-handler\"\n  },\n  \"counts\": {\n    \"lamp_addresses_bound\": 64,\n    \"lamp_emitters_bound\": 68,\n    \"lamps_resolved\": 68,\n    \"switches_resolved\": 35\n  },\n  \"format\": \"lethal-weapon-3-spatial-resolution\",\n  \"multi_emitter_lamps\": {\n    \"18\": [\n      \"l18\",\n      \"l18a\"\n    ],\n    \"27\": [\n      \"L27\",\n      \"L27b\"\n    ],\n    \"7\": [\n      \"L7\",\n      \"l7d\"\n    ],\n    \"9\": [\n      \"L9c\",\n      \"l9\"\n    ]\n  },\n  \"playfield\": {\n    \"height\": 2162.0,\n    \"note\": \"y is normalized by the retained table's own 2162, asserted rather than assumed\",\n    \"width\": 952.0\n  },\n  \"resolved\": {\n    \"lamp.1\": {\n      \"address\": 1,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L1\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 469.9832,\n        \"y\": 1716.3083\n      },\n      \"x\": 0.49368,\n      \"y\": 0.793852\n    },\n    \"lamp.10\": {\n      \"address\": 10,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l10\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 216.86359,\n        \"y\": 1403.6102\n      },\n      \"x\": 0.227798,\n      \"y\": 0.649218\n    },\n    \"lamp.11\": {\n      \"address\": 11,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l11\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 280.36224,\n        \"y\": 1383.5304\n      },\n      \"x\": 0.294498,\n      \"y\": 0.639931\n    },\n    \"lamp.12\": {\n      \"address\": 12,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l12\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 340.60226,\n        \"y\": 1357.6106\n      },\n      \"x\": 0.357775,\n      \"y\": 0.627942\n    },\n    \"lamp.13\": {\n      \"address\": 13,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l13\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 402.06522,\n        \"y\": 1331.696\n      },\n      \"x\": 0.422337,\n      \"y\": 0.615956\n    },\n    \"lamp.14\": {\n      \"address\": 14,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l14\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 469.005,\n        \"y\": 1326.5585\n      },\n      \"x\": 0.492652,\n      \"y\": 0.613579\n    },\n    \"lamp.15\": {\n      \"address\": 15,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l15\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 521.2027,\n        \"y\": 1274.2999\n      },\n      \"x\": 0.547482,\n      \"y\": 0.589408\n    },\n    \"lamp.16\": {\n      \"address\": 16,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l16\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 595.10474,\n        \"y\": 1250.5726\n      },\n      \"x\": 0.62511,\n      \"y\": 0.578433\n    },\n    \"lamp.17\": {\n      \"address\": 17,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L17\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 432.69623,\n        \"y\": 1849.0043\n      },\n      \"x\": 0.454513,\n      \"y\": 0.855229\n    },\n    \"lamp.18-1\": {\n      \"address\": 18,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l18\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"1\",\n      \"raw\": {\n        \"x\": 64.64875,\n        \"y\": 1437.6057\n      },\n      \"x\": 0.067908,\n      \"y\": 0.664943\n    },\n    \"lamp.18-2\": {\n      \"address\": 18,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l18a\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"2\",\n      \"raw\": {\n        \"x\": 808.4387,\n        \"y\": 1439.2708\n      },\n      \"x\": 0.8492,\n      \"y\": 0.665713\n    },\n    \"lamp.19\": {\n      \"address\": 19,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l19\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 461.3767,\n        \"y\": 856.263\n      },\n      \"x\": 0.484639,\n      \"y\": 0.396051\n    },\n    \"lamp.2\": {\n      \"address\": 2,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L2\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 453.00272,\n        \"y\": 1677.8231\n      },\n      \"x\": 0.475843,\n      \"y\": 0.776051\n    },\n    \"lamp.20\": {\n      \"address\": 20,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l20\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 500.2392,\n        \"y\": 893.32654\n      },\n      \"x\": 0.525461,\n      \"y\": 0.413195\n    },\n    \"lamp.21\": {\n      \"address\": 21,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l21\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 547.4076,\n        \"y\": 935.7354\n      },\n      \"x\": 0.575008,\n      \"y\": 0.43281\n    },\n    \"lamp.22\": {\n      \"address\": 22,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l22\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 757.2076,\n        \"y\": 1080.2377\n      },\n      \"x\": 0.795386,\n      \"y\": 0.499647\n    },\n    \"lamp.23\": {\n      \"address\": 23,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l23\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 758.9232,\n        \"y\": 1130.2134\n      },\n      \"x\": 0.797188,\n      \"y\": 0.522763\n    },\n    \"lamp.24\": {\n      \"address\": 24,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l24\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 763.80304,\n        \"y\": 1188.6174\n      },\n      \"x\": 0.802314,\n      \"y\": 0.549777\n    },\n    \"lamp.25\": {\n      \"address\": 25,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l25\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 149.49634,\n        \"y\": 1300.0044\n      },\n      \"x\": 0.157034,\n      \"y\": 0.601297\n    },\n    \"lamp.26\": {\n      \"address\": 26,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l26\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 195.35692,\n        \"y\": 1351.8302\n      },\n      \"x\": 0.205207,\n      \"y\": 0.625268\n    },\n    \"lamp.27-1\": {\n      \"address\": 27,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L27\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"1\",\n      \"raw\": {\n        \"x\": 117.90017,\n        \"y\": 667.4007\n      },\n      \"x\": 0.123845,\n      \"y\": 0.308696\n    },\n    \"lamp.27-2\": {\n      \"address\": 27,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L27b\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"2\",\n      \"raw\": {\n        \"x\": 841.50305,\n        \"y\": 756.46326\n      },\n      \"x\": 0.883932,\n      \"y\": 0.34989\n    },\n    \"lamp.28\": {\n      \"address\": 28,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l28\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 566.2084,\n        \"y\": 1585.389\n      },\n      \"x\": 0.594757,\n      \"y\": 0.733297\n    },\n    \"lamp.29\": {\n      \"address\": 29,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l29\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 585.0607,\n        \"y\": 1524.6809\n      },\n      \"x\": 0.61456,\n      \"y\": 0.705218\n    },\n    \"lamp.3\": {\n      \"address\": 3,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L3\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 436.05893,\n        \"y\": 1640.5994\n      },\n      \"x\": 0.458045,\n      \"y\": 0.758834\n    },\n    \"lamp.30\": {\n      \"address\": 30,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l30\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 604.0881,\n        \"y\": 1464.3855\n      },\n      \"x\": 0.634546,\n      \"y\": 0.677329\n    },\n    \"lamp.31\": {\n      \"address\": 31,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l31\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 623.4329,\n        \"y\": 1403.2854\n      },\n      \"x\": 0.654866,\n      \"y\": 0.649068\n    },\n    \"lamp.32\": {\n      \"address\": 32,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l32\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 640.6036,\n        \"y\": 1346.1786\n      },\n      \"x\": 0.672903,\n      \"y\": 0.622654\n    },\n    \"lamp.33\": {\n      \"address\": 33,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l33\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 66.51722,\n        \"y\": 2241.926\n      },\n      \"x\": 0.069871,\n      \"y\": 1.036969\n    },\n    \"lamp.34\": {\n      \"address\": 34,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L34\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 529.1492,\n        \"y\": 636.9156\n      },\n      \"x\": 0.555829,\n      \"y\": 0.294596\n    },\n    \"lamp.35\": {\n      \"address\": 35,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l35\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 434.75006,\n        \"y\": 76.46345\n      },\n      \"x\": 0.45667,\n      \"y\": 0.035367\n    },\n    \"lamp.36\": {\n      \"address\": 36,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l36\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 534.7842,\n        \"y\": 91.44421\n      },\n      \"x\": 0.561748,\n      \"y\": 0.042296\n    },\n    \"lamp.37\": {\n      \"address\": 37,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l37\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 632.33234,\n        \"y\": 103.13759\n      },\n      \"x\": 0.664215,\n      \"y\": 0.047705\n    },\n    \"lamp.38\": {\n      \"address\": 38,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l38\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 186.91759,\n        \"y\": 1223.3071\n      },\n      \"x\": 0.196342,\n      \"y\": 0.565822\n    },\n    \"lamp.39\": {\n      \"address\": 39,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l39\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 148.57986,\n        \"y\": 1147.4773\n      },\n      \"x\": 0.156071,\n      \"y\": 0.530748\n    },\n    \"lamp.4\": {\n      \"address\": 4,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L4\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 419.1152,\n        \"y\": 1604.2537\n      },\n      \"x\": 0.440247,\n      \"y\": 0.742023\n    },\n    \"lamp.40\": {\n      \"address\": 40,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l40\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 102.641815,\n        \"y\": 1054.0095\n      },\n      \"x\": 0.107817,\n      \"y\": 0.487516\n    },\n    \"lamp.41\": {\n      \"address\": 41,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L41\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 136.4812,\n        \"y\": 449.85474\n      },\n      \"x\": 0.143363,\n      \"y\": 0.208073\n    },\n    \"lamp.42\": {\n      \"address\": 42,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L42\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 198.00047,\n        \"y\": 438.0172\n      },\n      \"x\": 0.207984,\n      \"y\": 0.202598\n    },\n    \"lamp.43\": {\n      \"address\": 43,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L43\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 255.77737,\n        \"y\": 427.5368\n      },\n      \"x\": 0.268674,\n      \"y\": 0.197751\n    },\n    \"lamp.44\": {\n      \"address\": 44,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L44\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 339.877,\n        \"y\": 301.6813\n      },\n      \"x\": 0.357014,\n      \"y\": 0.139538\n    },\n    \"lamp.45\": {\n      \"address\": 45,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L45\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 163.28488,\n        \"y\": 812.0039\n      },\n      \"x\": 0.171518,\n      \"y\": 0.37558\n    },\n    \"lamp.46\": {\n      \"address\": 46,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L46\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 176.76756,\n        \"y\": 868.2367\n      },\n      \"x\": 0.18568,\n      \"y\": 0.40159\n    },\n    \"lamp.47\": {\n      \"address\": 47,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L47\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 186.4685,\n        \"y\": 925.1272\n      },\n      \"x\": 0.19587,\n      \"y\": 0.427903\n    },\n    \"lamp.48\": {\n      \"address\": 48,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L48\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 198.47144,\n        \"y\": 981.8534\n      },\n      \"x\": 0.208478,\n      \"y\": 0.454141\n    },\n    \"lamp.49\": {\n      \"address\": 49,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L49\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 312.24182,\n        \"y\": 1747.1637\n      },\n      \"x\": 0.327985,\n      \"y\": 0.808124\n    },\n    \"lamp.5\": {\n      \"address\": 5,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L5\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 403.83908,\n        \"y\": 1568.4353\n      },\n      \"x\": 0.424201,\n      \"y\": 0.725456\n    },\n    \"lamp.50\": {\n      \"address\": 50,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L50\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 367.94086,\n        \"y\": 1766.9653\n      },\n      \"x\": 0.386492,\n      \"y\": 0.817283\n    },\n    \"lamp.51\": {\n      \"address\": 51,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l51\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 434.5472,\n        \"y\": 1778.349\n      },\n      \"x\": 0.456457,\n      \"y\": 0.822548\n    },\n    \"lamp.52\": {\n      \"address\": 52,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l52\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 499.43848,\n        \"y\": 1766.8431\n      },\n      \"x\": 0.52462,\n      \"y\": 0.817226\n    },\n    \"lamp.53\": {\n      \"address\": 53,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l53\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 556.8998,\n        \"y\": 1746.2819\n      },\n      \"x\": 0.584979,\n      \"y\": 0.807716\n    },\n    \"lamp.54\": {\n      \"address\": 54,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l54\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 380.89227,\n        \"y\": 655.94794\n      },\n      \"x\": 0.400097,\n      \"y\": 0.303399\n    },\n    \"lamp.55\": {\n      \"address\": 55,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l55\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 364.60944,\n        \"y\": 552.6141\n      },\n      \"x\": 0.382993,\n      \"y\": 0.255603\n    },\n    \"lamp.56\": {\n      \"address\": 56,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l56\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 350.7446,\n        \"y\": 466.06915\n      },\n      \"x\": 0.368429,\n      \"y\": 0.215573\n    },\n    \"lamp.57\": {\n      \"address\": 57,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l57\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 69.04814,\n        \"y\": 1551.3501\n      },\n      \"x\": 0.07253,\n      \"y\": 0.717553\n    },\n    \"lamp.58\": {\n      \"address\": 58,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l58\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 266.41394,\n        \"y\": 749.9903\n      },\n      \"x\": 0.279847,\n      \"y\": 0.346897\n    },\n    \"lamp.59\": {\n      \"address\": 59,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l59\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 239.53146,\n        \"y\": 656.8982\n      },\n      \"x\": 0.251609,\n      \"y\": 0.303838\n    },\n    \"lamp.6\": {\n      \"address\": 6,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L6\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 383.91083,\n        \"y\": 1531.3866\n      },\n      \"x\": 0.403268,\n      \"y\": 0.708319\n    },\n    \"lamp.60\": {\n      \"address\": 60,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L60\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 460.98788,\n        \"y\": 439.12283\n      },\n      \"x\": 0.484231,\n      \"y\": 0.20311\n    },\n    \"lamp.61\": {\n      \"address\": 61,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L61\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 665.57715,\n        \"y\": 482.1253\n      },\n      \"x\": 0.699136,\n      \"y\": 0.223\n    },\n    \"lamp.62\": {\n      \"address\": 62,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l62\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 681.287,\n        \"y\": 896.99475\n      },\n      \"x\": 0.715638,\n      \"y\": 0.414891\n    },\n    \"lamp.63\": {\n      \"address\": 63,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l63\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 709.6254,\n        \"y\": 804.94714\n      },\n      \"x\": 0.745405,\n      \"y\": 0.372316\n    },\n    \"lamp.64\": {\n      \"address\": 64,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l64\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 739.05493,\n        \"y\": 707.7263\n      },\n      \"x\": 0.776318,\n      \"y\": 0.327348\n    },\n    \"lamp.7-1\": {\n      \"address\": 7,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L7\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"1\",\n      \"raw\": {\n        \"x\": 896.3173,\n        \"y\": 1920.6625\n      },\n      \"x\": 0.94151,\n      \"y\": 0.888373\n    },\n    \"lamp.7-2\": {\n      \"address\": 7,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l7d\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"2\",\n      \"raw\": {\n        \"x\": 367.4345,\n        \"y\": 1466.1482\n      },\n      \"x\": 0.385961,\n      \"y\": 0.678144\n    },\n    \"lamp.8\": {\n      \"address\": 8,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l8\",\n      \"object_type\": \"Light\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 477.53683,\n        \"y\": 1430.6932\n      },\n      \"x\": 0.501614,\n      \"y\": 0.661745\n    },\n    \"lamp.9-1\": {\n      \"address\": 9,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L9c\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"1\",\n      \"raw\": {\n        \"x\": 794.3281,\n        \"y\": 887.4039\n      },\n      \"x\": 0.834378,\n      \"y\": 0.410455\n    },\n    \"lamp.9-2\": {\n      \"address\": 9,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l9\",\n      \"object_type\": \"Light\",\n      \"ordinal\": \"2\",\n      \"raw\": {\n        \"x\": 131.65363,\n        \"y\": 1397.1549\n      },\n      \"x\": 0.138292,\n      \"y\": 0.646233\n    },\n    \"switch.10\": {\n      \"address\": 10,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw10\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 448.39606,\n        \"y\": 2081.047\n      },\n      \"x\": 0.471004,\n      \"y\": 0.962556\n    },\n    \"switch.11\": {\n      \"address\": 11,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw11\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 686.99896,\n        \"y\": 1948.666\n      },\n      \"x\": 0.721638,\n      \"y\": 0.901326\n    },\n    \"switch.12\": {\n      \"address\": 12,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw12\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 758.11053,\n        \"y\": 1906.8884\n      },\n      \"x\": 0.796335,\n      \"y\": 0.882002\n    },\n    \"switch.13\": {\n      \"address\": 13,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw13\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 822.2155,\n        \"y\": 1868.318\n      },\n      \"x\": 0.863672,\n      \"y\": 0.864162\n    },\n    \"switch.14\": {\n      \"address\": 14,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw14\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 893.79224,\n        \"y\": 1888.2462\n      },\n      \"x\": 0.938857,\n      \"y\": 0.873379\n    },\n    \"switch.21\": {\n      \"address\": 21,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw21\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 248.5097,\n        \"y\": 65.70186\n      },\n      \"x\": 0.26104,\n      \"y\": 0.030389\n    },\n    \"switch.22\": {\n      \"address\": 22,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw22\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 882.3967,\n        \"y\": 297.74374\n      },\n      \"x\": 0.926887,\n      \"y\": 0.137717\n    },\n    \"switch.25\": {\n      \"address\": 25,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw25\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 475.6399075,\n        \"y\": 792.20897\n      },\n      \"x\": 0.499622,\n      \"y\": 0.366424\n    },\n    \"switch.26\": {\n      \"address\": 26,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw26\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 517.21955,\n        \"y\": 828.202315\n      },\n      \"x\": 0.543298,\n      \"y\": 0.383072\n    },\n    \"switch.27\": {\n      \"address\": 27,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw27\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 558.7541625,\n        \"y\": 864.2698175\n      },\n      \"x\": 0.586927,\n      \"y\": 0.399755\n    },\n    \"switch.28\": {\n      \"address\": 28,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw28\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 66.490364,\n        \"y\": 1710.0\n      },\n      \"x\": 0.069843,\n      \"y\": 0.790934\n    },\n    \"switch.29\": {\n      \"address\": 29,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw29\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 135.92296,\n        \"y\": 1578.1323\n      },\n      \"x\": 0.142776,\n      \"y\": 0.729941\n    },\n    \"switch.30\": {\n      \"address\": 30,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"LeftSlingShot\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 226.586875,\n        \"y\": 1563.545116666667\n      },\n      \"x\": 0.238011,\n      \"y\": 0.723194\n    },\n    \"switch.31\": {\n      \"address\": 31,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw31\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 305.9941,\n        \"y\": 213.7548\n      },\n      \"x\": 0.321422,\n      \"y\": 0.098869\n    },\n    \"switch.32\": {\n      \"address\": 32,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw32\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 810.46387,\n        \"y\": 360.67676\n      },\n      \"x\": 0.851328,\n      \"y\": 0.166826\n    },\n    \"switch.33\": {\n      \"address\": 33,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw33\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 814.3228475,\n        \"y\": 1055.273425\n      },\n      \"x\": 0.855381,\n      \"y\": 0.488101\n    },\n    \"switch.34\": {\n      \"address\": 34,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw34\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 818.369965,\n        \"y\": 1108.677725\n      },\n      \"x\": 0.859632,\n      \"y\": 0.512802\n    },\n    \"switch.35\": {\n      \"address\": 35,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"sw35\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 821.695215,\n        \"y\": 1166.5061249999999\n      },\n      \"x\": 0.863125,\n      \"y\": 0.53955\n    },\n    \"switch.36\": {\n      \"address\": 36,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw36\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 805.73987,\n        \"y\": 1639.337\n      },\n      \"x\": 0.846365,\n      \"y\": 0.75825\n    },\n    \"switch.37\": {\n      \"address\": 37,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw37\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 734.39923,\n        \"y\": 1574.5562\n      },\n      \"x\": 0.771428,\n      \"y\": 0.728287\n    },\n    \"switch.38\": {\n      \"address\": 38,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"RightSlingShot\",\n      \"object_type\": \"Wall\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 643.3524233333334,\n        \"y\": 1565.8709166666667\n      },\n      \"x\": 0.67579,\n      \"y\": 0.72427\n    },\n    \"switch.40\": {\n      \"address\": 40,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw40\",\n      \"object_type\": \"Kicker\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 56.35513,\n        \"y\": 904.92633\n      },\n      \"x\": 0.059197,\n      \"y\": 0.41856\n    },\n    \"switch.41\": {\n      \"address\": 41,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw41\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 435.27243,\n        \"y\": 215.90593\n      },\n      \"x\": 0.457219,\n      \"y\": 0.099864\n    },\n    \"switch.42\": {\n      \"address\": 42,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw42\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 535.14734,\n        \"y\": 230.12659\n      },\n      \"x\": 0.56213,\n      \"y\": 0.106442\n    },\n    \"switch.43\": {\n      \"address\": 43,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw43\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 632.08105,\n        \"y\": 242.92212\n      },\n      \"x\": 0.663951,\n      \"y\": 0.11236\n    },\n    \"switch.44\": {\n      \"address\": 44,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper1\",\n      \"object_type\": \"Bumper\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 460.92288,\n        \"y\": 441.1298\n      },\n      \"x\": 0.484163,\n      \"y\": 0.204038\n    },\n    \"switch.45\": {\n      \"address\": 45,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper2\",\n      \"object_type\": \"Bumper\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 530.144,\n        \"y\": 634.9131\n      },\n      \"x\": 0.556874,\n      \"y\": 0.293669\n    },\n    \"switch.46\": {\n      \"address\": 46,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper3\",\n      \"object_type\": \"Bumper\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 666.9866,\n        \"y\": 481.60703\n      },\n      \"x\": 0.700616,\n      \"y\": 0.22276\n    },\n    \"switch.47\": {\n      \"address\": 47,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw47\",\n      \"object_type\": \"Spinner\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 112.49616,\n        \"y\": 641.19275\n      },\n      \"x\": 0.118168,\n      \"y\": 0.296574\n    },\n    \"switch.48\": {\n      \"address\": 48,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw48\",\n      \"object_type\": \"Spinner\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 854.1629,\n        \"y\": 726.16504\n      },\n      \"x\": 0.89723,\n      \"y\": 0.335877\n    },\n    \"switch.49\": {\n      \"address\": 49,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw49\",\n      \"object_type\": \"Gate\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 234.37604,\n        \"y\": 604.9357\n      },\n      \"x\": 0.246193,\n      \"y\": 0.279804\n    },\n    \"switch.50\": {\n      \"address\": 50,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw50\",\n      \"object_type\": \"Gate\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 393.12015,\n        \"y\": 94.112274\n      },\n      \"x\": 0.412941,\n      \"y\": 0.04353\n    },\n    \"switch.52\": {\n      \"address\": 52,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw52\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 630.7501,\n        \"y\": 672.21906\n      },\n      \"x\": 0.662553,\n      \"y\": 0.310925\n    },\n    \"switch.54\": {\n      \"address\": 54,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw54\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 74.07084,\n        \"y\": 213.86482\n      },\n      \"x\": 0.077806,\n      \"y\": 0.09892\n    },\n    \"switch.55\": {\n      \"address\": 55,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw55\",\n      \"object_type\": \"Trigger\",\n      \"ordinal\": null,\n      \"raw\": {\n        \"x\": 883.2824,\n        \"y\": 426.22195\n      },\n      \"x\": 0.927818,\n      \"y\": 0.197142\n    }\n  },\n  \"source\": \"vpx-table.lethal-weapon-3-vpw-2-0\",\n  \"unresolved\": {\n    \"lamps\": [],\n    \"switches\": [\n      {\n        \"address\": 1,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 2,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 3,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 4,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 5,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 6,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 7,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 8,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 9,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 15,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 16,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 17,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 18,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 19,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 20,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 23,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 24,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 39,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 51,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 53,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 56,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 57,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 58,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 59,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 60,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 61,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 62,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 63,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 64,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      }\n    ]\n  },\n  \"version\": 1\n}")
ROM_SETS = json.loads("{\n  \"lw3_200\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3cpu.200\",\n      \"lw3dsp1.204\",\n      \"lw3dsp0.204\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_203\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3cpuu.203\",\n      \"lw3dsp1.204\",\n      \"lw3dsp0.204\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_205\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3gc5.205\",\n      \"lw3dsp1.205\",\n      \"lw3dsp0.205\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_207\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3gc5.207\",\n      \"lw3drom1.a26\",\n      \"lw3drom0.a26\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_208\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3cpuu.208\",\n      \"lw3drom1.a26\",\n      \"lw3drom0.a26\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_208p\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3cpuu.208\",\n      \"lw3drom1.a26\",\n      \"lw3drom0.a26\",\n      \"lw3u7.dat\",\n      \"lw3u17_vm.dat\",\n      \"lw3u21_vm.dat\"\n    ]\n  },\n  \"lw3_300\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"LW3CPUU.300\",\n      \"lw3drom1.300\",\n      \"lw3drom0.300\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_301\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"LW3CPUU.301\",\n      \"lw3drom1.300\",\n      \"lw3drom0.300\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  },\n  \"lw3_e204\": {\n    \"macro\": \"DE_ROMSTARTx0\",\n    \"roms\": [\n      \"lw3cpue.204\",\n      \"lw3dsp1a.202\",\n      \"lw3dsp0a.202\",\n      \"lw3u7.dat\",\n      \"lw3u17.dat\",\n      \"lw3u21.dat\"\n    ]\n  }\n}")
EVIDENCE_HASHES = json.loads("{\n  \"extraction_file_count\": 2135,\n  \"extraction_total_bytes\": 842643935,\n  \"manifest_file_sha256\": \"b52eac248a97cb4916924d48d46b485f378244e46ffe934c9a65dcf7dd716b32\",\n  \"manifest_sha256\": \"3735e00679d008b8bb7936bae43b11a93b231394f40b8b37a7ebf3f07fe9cb83\",\n  \"script_bytes\": 182169,\n  \"script_sha256\": \"d6c42eb3bd059ccc8126aa2ba27972ff59beb77ec53cf2efca6c1a9f6a204f11\",\n  \"table_bytes\": 374038528,\n  \"table_sha256\": \"915b733234b95497e2b47d4cfaa47e6c9fdea535d768ad61b54242419b734a52\"\n}")
DOCUMENT_HASHES = json.loads("{\n  \"LW3Addendum.pdf\": {\n    \"bytes\": 150889,\n    \"sha256\": \"c8f8a9d26532f712ac2f997d69fdec9a7701000b7d22c685cca8b63ea3e26490\"\n  },\n  \"Lethal_Weapon_3_OPS.pdf\": {\n    \"bytes\": 10482189,\n    \"sha256\": \"e285463cbee4fc69384b1690add6e3da4ddfc5d08245515cbc652dd179492ce5\"\n  }\n}")
# Digests of the committed excerpts, computed at bundle time from the files themselves so the
# recorded hash cannot drift from the transcription it describes.
EXCERPT_HASHES = json.loads("{\n  \"addendum.md\": \"b45b935091aa167427518152b1b09725fef05a33db06c87a7dcc871466c7d5c5\",\n  \"coil-drivers.md\": \"58de574339c7b817c1c4d71194c1c7c6611aaed6e6561095da84e4d5e81b89a2\",\n  \"lamp-matrix.md\": \"627fa49d6592b8d35a6536d346486add7971ff09a903406be0a8760e31cc2b68\",\n  \"switch-matrix.md\": \"f975d7d7557b6a4cdca85eeeb68ff3ec31e0b9b1010f340bb0370511d4f140f1\"\n}")
COIL_LOCATION_IMAGE_SHA256 = "4625dcabd1840761e1816ff1edd7d3a687884c1f7858a8320d7fefc958fcc953"


MANUAL = "manual.data-east.lethal-weapon-3.1992"
ADDENDUM = "manual-addendum.data-east.lethal-weapon-3.1992"
CORE = "pinmame.core.4ec52ff0ac13"
CATALOG = "pinmame.catalog.4ec52ff0ac13"
TABLE = "vpx-table.lethal-weapon-3-vpw-2-0"
SCRIPT_REF = "vpx-script.lethal-weapon-3-vpw-2-0"
LEGACY = "legacy.game.lw3"
EXTRACTION = "vpx-extraction.lethal-weapon-3-vpw-2-0"

SW = TRANSCRIPTION["switch_matrix"]
LAMPS = TRANSCRIPTION["lamp_matrix"]
AUX = TRANSCRIPTION["coil_drivers"]["direct"]
MUX = TRANSCRIPTION["coil_drivers"]["muxed"]
AUXSOL = TRANSCRIPTION["auxiliary_solenoids"]
PLACES = RESOLUTION["resolved"]
# The submitted resolver handled Trigger/Kicker/Wall/etc. but silently omitted HitTarget, even
# though the retained script's Sw17-Sw20/Sw39 handlers bind these exact named objects. Preserve the
# measured centers from the hash-pinned extraction. Every remaining unplaced switch is explicitly
# classified as cabinet/service or unused, so none belongs in the report's unresolved list.
PLACES.update({
    "switch.17": {"address": 17, "coordinate_origin": "measured-center", "kind": "switch", "object": "sw17", "object_type": "HitTarget", "ordinal": None, "raw": {"x": 92.829765, "y": 783.8604}, "x": 0.09751, "y": 0.362563},
    "switch.18": {"address": 18, "coordinate_origin": "measured-center", "kind": "switch", "object": "sw18", "object_type": "HitTarget", "ordinal": None, "raw": {"x": 103.37032, "y": 838.91345}, "x": 0.108582, "y": 0.388027},
    "switch.19": {"address": 19, "coordinate_origin": "measured-center", "kind": "switch", "object": "sw19", "object_type": "HitTarget", "ordinal": None, "raw": {"x": 114.43212, "y": 893.9585}, "x": 0.120202, "y": 0.413487},
    "switch.20": {"address": 20, "coordinate_origin": "measured-center", "kind": "switch", "object": "sw20", "object_type": "HitTarget", "ordinal": None, "raw": {"x": 126.02059, "y": 951.6377}, "x": 0.132375, "y": 0.440165},
    "switch.39": {"address": 39, "coordinate_origin": "measured-center", "kind": "switch", "object": "sw39", "object_type": "HitTarget", "ordinal": None, "raw": {"x": 99.050804, "y": 1251.1111}, "x": 0.104045, "y": 0.578682},
})
# The retained script binds the direct flashers, muxed 25-32 flashers and GI relay to exact Light
# objects. GI_BG is deliberately excluded: its raw y=-229.33345 is an off-playfield visual proxy,
# not a physical playfield emitter, while the other 35 members of the GI collection are in bounds.
PLACES.update({
    "solenoid.9-1": {"address": 9, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F109", "object_type": "Light", "ordinal": "1", "raw": {"x": 248.26761, "y": 259.59552}, "x": 0.260785, "y": 0.120072},
    "solenoid.9-2": {"address": 9, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F109a", "object_type": "Light", "ordinal": "2", "raw": {"x": 168.92593, "y": 335.0852}, "x": 0.177443, "y": 0.154989},
    "solenoid.11-1": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_027", "object_type": "Light", "ordinal": "1", "raw": {"x": 491.8548, "y": 719.68884}, "x": 0.516654, "y": 0.332881},
    "solenoid.11-2": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_LaneGuide_004", "object_type": "Light", "ordinal": "2", "raw": {"x": 384.53613, "y": 204.7578}, "x": 0.403925, "y": 0.094708},
    "solenoid.11-3": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_LaneGuide_003", "object_type": "Light", "ordinal": "3", "raw": {"x": 484.91226, "y": 218.38347}, "x": 0.509362, "y": 0.10101},
    "solenoid.11-4": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_LaneGuide_002", "object_type": "Light", "ordinal": "4", "raw": {"x": 584.185, "y": 231.36029}, "x": 0.61364, "y": 0.107012},
    "solenoid.11-5": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_LaneGuide_001", "object_type": "Light", "ordinal": "5", "raw": {"x": 680.8623, "y": 241.74174}, "x": 0.715191, "y": 0.111814},
    "solenoid.11-6": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_059", "object_type": "Light", "ordinal": "6", "raw": {"x": 749.83685, "y": 434.52307}, "x": 0.787644, "y": 0.200982},
    "solenoid.11-7": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_057", "object_type": "Light", "ordinal": "7", "raw": {"x": 762.16486, "y": 284.6407}, "x": 0.800593, "y": 0.131656},
    "solenoid.11-8": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_055", "object_type": "Light", "ordinal": "8", "raw": {"x": 714.1506, "y": 269.71735}, "x": 0.750158, "y": 0.124754},
    "solenoid.11-9": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_053", "object_type": "Light", "ordinal": "9", "raw": {"x": 802.393, "y": 239.22182}, "x": 0.84285, "y": 0.110648},
    "solenoid.11-10": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_051", "object_type": "Light", "ordinal": "10", "raw": {"x": 751.7834, "y": 167.84929}, "x": 0.789688, "y": 0.077636},
    "solenoid.11-11": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_049", "object_type": "Light", "ordinal": "11", "raw": {"x": 886.50415, "y": 61.43933}, "x": 0.931202, "y": 0.028418},
    "solenoid.11-12": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_047", "object_type": "Light", "ordinal": "12", "raw": {"x": 886.50415, "y": 137.35376}, "x": 0.931202, "y": 0.063531},
    "solenoid.11-13": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI666", "object_type": "Light", "ordinal": "13", "raw": {"x": 159.37523, "y": 48.786926}, "x": 0.167411, "y": 0.022566},
    "solenoid.11-14": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_043", "object_type": "Light", "ordinal": "14", "raw": {"x": 59.453663, "y": 140.08037}, "x": 0.062451, "y": 0.064792},
    "solenoid.11-15": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_041", "object_type": "Light", "ordinal": "15", "raw": {"x": 256.70148, "y": 255.76729}, "x": 0.269644, "y": 0.118301},
    "solenoid.11-16": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_039", "object_type": "Light", "ordinal": "16", "raw": {"x": 239.18266, "y": 422.51947}, "x": 0.251242, "y": 0.19543},
    "solenoid.11-17": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_037", "object_type": "Light", "ordinal": "17", "raw": {"x": 241.778, "y": 144.1666}, "x": 0.253968, "y": 0.066682},
    "solenoid.11-18": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_035", "object_type": "Light", "ordinal": "18", "raw": {"x": 162.61943, "y": 431.60324}, "x": 0.170819, "y": 0.199631},
    "solenoid.11-19": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_033", "object_type": "Light", "ordinal": "19", "raw": {"x": 61.400196, "y": 783.73096}, "x": 0.064496, "y": 0.362503},
    "solenoid.11-20": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI32", "object_type": "Light", "ordinal": "20", "raw": {"x": 51.018726, "y": 1108.1516}, "x": 0.053591, "y": 0.512559},
    "solenoid.11-21": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI30", "object_type": "Light", "ordinal": "21", "raw": {"x": 54.262928, "y": 1269.0642}, "x": 0.056999, "y": 0.586986},
    "solenoid.11-22": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI26", "object_type": "Light", "ordinal": "22", "raw": {"x": 545.70856, "y": 774.19147}, "x": 0.573223, "y": 0.35809},
    "solenoid.11-23": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_023", "object_type": "Light", "ordinal": "23", "raw": {"x": 893.24066, "y": 817.6639}, "x": 0.938278, "y": 0.378198},
    "solenoid.11-24": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI22", "object_type": "Light", "ordinal": "24", "raw": {"x": 848.47064, "y": 930.56226}, "x": 0.891251, "y": 0.430417},
    "solenoid.11-25": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI20", "object_type": "Light", "ordinal": "25", "raw": {"x": 845.2264, "y": 1058.384}, "x": 0.887843, "y": 0.489539},
    "solenoid.11-26": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI18", "object_type": "Light", "ordinal": "26", "raw": {"x": 852.3637, "y": 1156.359}, "x": 0.89534, "y": 0.534856},
    "solenoid.11-27": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI_015", "object_type": "Light", "ordinal": "27", "raw": {"x": 898.43146, "y": 1178.4197}, "x": 0.943731, "y": 0.54506},
    "solenoid.11-28": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI14", "object_type": "Light", "ordinal": "28", "raw": {"x": 191.43791, "y": 1546.9207}, "x": 0.20109, "y": 0.715504},
    "solenoid.11-29": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI12", "object_type": "Light", "ordinal": "29", "raw": {"x": 681.232, "y": 1546.1907}, "x": 0.71558, "y": 0.715167},
    "solenoid.11-30": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI10", "object_type": "Light", "ordinal": "30", "raw": {"x": 650.5743, "y": 1635.9741}, "x": 0.683376, "y": 0.756695},
    "solenoid.11-31": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI08", "object_type": "Light", "ordinal": "31", "raw": {"x": 219.17589, "y": 1633.0543}, "x": 0.230227, "y": 0.755344},
    "solenoid.11-32": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI06", "object_type": "Light", "ordinal": "32", "raw": {"x": 156.218, "y": 1723.3854}, "x": 0.164095, "y": 0.797126},
    "solenoid.11-33": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI01", "object_type": "Light", "ordinal": "33", "raw": {"x": 715.1745, "y": 1724.4802}, "x": 0.751234, "y": 0.797632},
    "solenoid.11-34": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI17", "object_type": "Light", "ordinal": "34", "raw": {"x": 201.11122, "y": 1434.9994}, "x": 0.211251, "y": 0.663737},
    "solenoid.11-35": {"address": 11, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "GI19", "object_type": "Light", "ordinal": "35", "raw": {"x": 796.66656, "y": 1187.8883}, "x": 0.836835, "y": 0.54944},
    "solenoid.16": {"address": 16, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F116", "object_type": "Light", "ordinal": None, "raw": {"x": 349.45334, "y": 1478.067}, "x": 0.367073, "y": 0.683657},
    "solenoid.25": {"address": 25, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F125", "object_type": "Light", "ordinal": None, "raw": {"x": 677.25916, "y": 1194.8846}, "x": 0.711407, "y": 0.552676},
    "solenoid.26-1": {"address": 26, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F126", "object_type": "Light", "ordinal": "1", "raw": {"x": 46.779305, "y": 1219.8251}, "x": 0.049138, "y": 0.564211},
    "solenoid.26-2": {"address": 26, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F126a", "object_type": "Light", "ordinal": "2", "raw": {"x": 824.6008, "y": 27.925158}, "x": 0.866177, "y": 0.012916},
    "solenoid.27-1": {"address": 27, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F127", "object_type": "Light", "ordinal": "1", "raw": {"x": 120.56716, "y": 646.91974}, "x": 0.126646, "y": 0.299223},
    "solenoid.27-2": {"address": 27, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F127a", "object_type": "Light", "ordinal": "2", "raw": {"x": 45.381783, "y": 729.05664}, "x": 0.04767, "y": 0.337214},
    "solenoid.28-1": {"address": 28, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F128", "object_type": "Light", "ordinal": "1", "raw": {"x": 80.05452, "y": 387.77502}, "x": 0.084091, "y": 0.179359},
    "solenoid.28-2": {"address": 28, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F128a", "object_type": "Light", "ordinal": "2", "raw": {"x": 41.453133, "y": 101.885254}, "x": 0.043543, "y": 0.047125},
    "solenoid.28-3": {"address": 28, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F128b", "object_type": "Light", "ordinal": "3", "raw": {"x": 143.25658, "y": 240.59781}, "x": 0.15048, "y": 0.111285},
    "solenoid.29-1": {"address": 29, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F129", "object_type": "Light", "ordinal": "1", "raw": {"x": 575.5809, "y": 346.06827}, "x": 0.604602, "y": 0.160069},
    "solenoid.29-2": {"address": 29, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F129a", "object_type": "Light", "ordinal": "2", "raw": {"x": 521.6432, "y": 27.474564}, "x": 0.547945, "y": 0.012708},
    "solenoid.30-1": {"address": 30, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F130", "object_type": "Light", "ordinal": "1", "raw": {"x": 841.02234, "y": 183.00456}, "x": 0.883427, "y": 0.084646},
    "solenoid.30-2": {"address": 30, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F130a", "object_type": "Light", "ordinal": "2", "raw": {"x": 735.0145, "y": 215.06693}, "x": 0.772074, "y": 0.099476},
    "solenoid.30-3": {"address": 30, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F130b", "object_type": "Light", "ordinal": "3", "raw": {"x": 658.37646, "y": 30.506172}, "x": 0.691572, "y": 0.01411},
    "solenoid.30-4": {"address": 30, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F130c", "object_type": "Light", "ordinal": "4", "raw": {"x": 802.57166, "y": 57.74701}, "x": 0.843037, "y": 0.02671},
    "solenoid.31": {"address": 31, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F131", "object_type": "Light", "ordinal": None, "raw": {"x": 471.5352, "y": 971.85547}, "x": 0.49531, "y": 0.449517},
    "solenoid.32-1": {"address": 32, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F132", "object_type": "Light", "ordinal": "1", "raw": {"x": 837.7309, "y": 771.26624}, "x": 0.879969, "y": 0.356737},
    "solenoid.32-2": {"address": 32, "coordinate_origin": "measured-center", "kind": "solenoid", "object": "F132a", "object_type": "Light", "ordinal": "2", "raw": {"x": 905.53046, "y": 861.9025}, "x": 0.951187, "y": 0.39866},
})

# Coils are placed at the mechanism they actuate, not at an invented winding center. Most retained
# table mechanisms expose the exact Kicker/Bumper/Plunger center or the corresponding switch
# surface. The two drop-bank resets use the visible middle-target primitives that the callbacks
# animate. The left/right slings use the same extended Wall centroids as their triggering surfaces,
# so their coordinate origin remains explicitly computed rather than masquerading as measured.
def add_actuator_proxy(address, source_key, device_id):
    source = PLACES[source_key]
    PLACES[f"solenoid.{address}"] = {
        **source,
        "address": address,
        "device_id": device_id,
        "kind": "solenoid",
    }


for _address, _source in {
    1: "switch.10", 2: "switch.13", 4: "switch.40", 5: "switch.32",
    15: "switch.31", 17: "switch.44", 18: "switch.45", 19: "switch.46",
    20: "switch.30", 21: "switch.38",
}.items():
    add_actuator_proxy(_address, _source, f"coil.driver-{_address}")

PLACES.update({
    "solenoid.6": {"address": 6, "coordinate_origin": "measured-center", "device_id": "coil.driver-6", "kind": "solenoid", "object": "BM_sw26", "object_type": "Primitive", "ordinal": None, "raw": {"x": 517.3968, "y": 827.7848}, "x": 0.543484, "y": 0.382879},
    "solenoid.7": {"address": 7, "coordinate_origin": "measured-center", "device_id": "coil.driver-7", "kind": "solenoid", "object": "BM_sw34", "object_type": "Primitive", "ordinal": None, "raw": {"x": 817.4405, "y": 1109.9131}, "x": 0.858656, "y": 0.513373},
    "solenoid.12": {"address": 12, "coordinate_origin": "measured-center", "device_id": "coil.driver-12", "kind": "solenoid", "object": "swPlunger", "object_type": "Trigger", "ordinal": None, "raw": {"x": 894.59503, "y": 1911.2178}, "x": 0.939701, "y": 0.884005},
    "solenoid.22": {"address": 22, "coordinate_origin": "measured-center", "device_id": "coil.driver-22", "kind": "solenoid", "object": "kickback", "object_type": "Plunger", "ordinal": None, "raw": {"x": 61.718273, "y": 1887.7291}, "x": 0.06483, "y": 0.87314},
})
RESOLUTION["unresolved"]["switches"] = []
HASHES = EVIDENCE_HASHES
ADDENDUM_SHA256 = DOCUMENT_HASHES["LW3Addendum.pdf"]["sha256"]

# Column 1 of the switch matrix is the dedicated cabinet/coin column, exactly as s11.h's
# DE_COMPORTS declares it. Address 9 is the separate cabinet gun-launch trigger. Addresses 15 and
# 16 are the cabinet flipper buttons: the matrix chart calls them EOS, but the same manual's Switch
# Part Numbers table marks both as cabinet switches, agreeing with PinMAME and the retained script.
CABINET_ROLES = {
    1: ["cabinet.tilt"], 2: ["cabinet.coin"], 3: ["cabinet.start"], 4: ["cabinet.coin"],
    5: ["cabinet.coin"], 6: ["cabinet.coin"], 7: ["cabinet.slam-tilt"],
    9: ["cabinet.launch"],
    15: ["cabinet.flipper.left-button"], 16: ["cabinet.flipper.right-button"],
}
# PinMAME owns these two. See the note built below.
EMULATOR_OWNED_SWITCHES = {15, 16}


def prov(status, refs):
    return {"status": status, "source_refs": list(refs)}


def placement(device_id, role, key, refs):
    """One placement per emitter, not one per address.

    The resolver keys a single-emitter address as `lamp.7` and a two-emitter address as `lamp.7-1`
    and `lamp.7-2`. Four lamp addresses on this machine drive two bulbs at genuinely different
    playfield positions - lamp 18's pair sits at opposite sides of the table - so both are emitted.
    Averaging them would produce a coordinate with no bulb in it, which is the error that demoted
    Bally Centaur.
    """
    hits = [PLACES[key]] if key in PLACES else [
        PLACES[k] for k in sorted(
            PLACES,
            key=lambda candidate: int(candidate.rsplit("-", 1)[1]) if candidate.startswith(key + "-") else 0,
        ) if k.startswith(key + "-")]
    if not hits:
        return None
    placements = []
    for index, hit in enumerate(hits, start=1):
        suffix = "" if len(hits) == 1 else f".{index}"
        placements.append({
            "id": f"{device_id}.{role}{suffix}",
            "role": role,
            "space": "playfield",
            "x": hit["x"],
            "y": hit["y"],
            "provenance": prov("observed", refs),
        })
    return {"status": "observed", "placements": placements}


def not_applicable(reason, refs):
    return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", refs)}


inputs = []
for address in range(1, 65):
    record = SW[str(address)]
    name = record["name"]
    unused = name == "Not Used"
    device_id = f"switch.matrix-{address}"
    notes = [
        f"Printed switch-matrix column {record['column']}, row {record['row']}.",
    ]
    if unused:
        notes.append("Printed NOT USED in the switch matrix; the address is strobed but carries no device.")
    if address in CABINET_ROLES:
        if address == 9:
            notes.append(
                "Cabinet launch trigger in the gun-style ball-launch control; it is not a "
                "playfield switch, which is why the manual's printed-page-25 location drawing "
                "has no address-9 callout on the playfield. The adjacent parts table does not "
                "mark 09 with its cabinet-switch asterisk, unlike 01-07 and 15-16; that legend "
                "variance is retained rather than silently read as positive cabinet evidence."
            )
        elif address == 2:
            notes.append(
                "Dedicated cabinet/coin-door column. The shared DE_COMPORTS macro labels this "
                "position 'Ball Tilt', but that is a generic platform label rather than this "
                "machine's fitted function: the machine-specific switch chart prints '4th "
                "Coin', which is used here."
            )
        elif record["column"] == 1:
            notes.append(
                "Dedicated cabinet/coin-door column. s11.h's DE_COMPORTS declares matrix column 1 "
                "as the cabinet inputs, and this manual's own chart agrees at this address."
            )
    if address in EMULATOR_OWNED_SWITCHES:
        notes.append(
            f"The manual contradicts itself at this address: the switch-matrix chart prints "
            f"'{name}', while the adjacent Switch Part Numbers table prints "
            "'Left Flip. Cab'/'Right Flip. Cab.', assigns part 180-5048-01, and marks each with "
            "the legend '* Indicates Cabinet Switches'. The cabinet-button interpretation is "
            "therefore the canonical physical semantic, and pinned PinMAME independently agrees: "
            "lw3GameData declares FLIP1516, which is "
            "FLIP_SWNO(15,16), and "
            "core.c:1740-1741 - under its own comment 'set switches in matrix for non-fliptronic "
            "games' - mirrors the flipper BUTTON state here through core_setSw. Because this game "
            "declares no FLIP_SOL, no FLIP_EOS bit is ever "
            "set and the EOS simulation at core.c:1756-1775 never runs, so no end-of-stroke state "
            "is modelled at all. The retained known-working VPW 2.0 script does drive this address "
            "from the cabinet flipper key - script.vbs:928-929 on key down and 960-961 on key up - "
            "which matches what the emulator already mirrors here and is therefore redundant "
            "rather than authoritative. The mirroring is mode-dependent: those two core_setSw "
            "calls sit inside the #ifdef PROC_SUPPORT / if (!coreGlobals.p_rocEn) guard at "
            "core.c:1733, so an ordinary emulation build rewrites this address from the flipper "
            "button bits on every core_updateSw pass and no recreation can publish an "
            "end-of-stroke reading on it, while a P-ROC build driving real hardware skips the "
            "write and takes the state from the physical switch."
        )
    canonical_name = {
        15: "Left Flipper Cabinet Button",
        16: "Right Flipper Cabinet Button",
    }.get(address, name)
    entry = {
        "id": device_id,
        "label": canonical_name if not unused else f"Unused Switch {address}",
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": [{"namespace": "pinmame.switch", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "unused" if unused else "used",
        "provenance": prov("validated", [MANUAL, CORE] + ([] if unused else [SCRIPT_REF])),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": record["column_drive"]["transistor"],
            "drive_wire": record["column_drive"]["wire"],
            "drive_connection": record["column_drive"]["connector"],
            "return_wire": record["row_return"]["wire"],
            "return_connection": record["row_return"]["connector"],
        },
    }
    if address in CABINET_ROLES:
        entry["roles"] = CABINET_ROLES[address]

    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address in CABINET_ROLES:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address in EMULATOR_OWNED_SWITCHES:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, CORE, SCRIPT_REF])
    else:
        spatial = placement(device_id, "sensor", f"switch.{address}", [TABLE, MANUAL])
        if spatial:
            entry["spatial"] = spatial
        # Otherwise the key is omitted entirely. The schema offers only `located` or
        # `not_applicable`, and neither is honest for a printed playfield device that this
        # extraction simply does not model; the Star Trek: TNG pass set that precedent.
    inputs.append(entry)

# The two coin-door diagnostic buttons. s11.h defines DE_SWADVANCE = -7 and DE_SWUPDN = -6 and
# stops there: the -5 CPU-diagnostic and -4 sound-diagnostic addresses beside them are
# S11_SWCPUDIAG/S11_SWSOUNDDIAG, Williams System 11 only. Data East publishes two, not four,
# which is a real platform difference rather than an omission here. DE also inverts Advance
# relative to Williams (s11.c reads !core_getSw(DE_SWADVANCE)).
for _address, _label, _port_label in (
    (-7, "Advance (Black Button)", "Black Button"),
    (-6, "Up/Down (Green Button)", "Green Button"),
):
    inputs.append({
        "id": f"switch.diagnostic{_address}",
        "label": _label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": _address},
        "aliases": [{"namespace": "pinmame.switch", "value": str(_address)}],
        "availability": "used",
        "provenance": prov("validated", [CORE]),
        "physical": {"notes": (
            f"Coin-door diagnostic button, named '{_port_label}' by s11.h's DE_COMPORTS, which "
            "places it in switch column 0 rather than the playfield matrix. Data East defines "
            "only these two (DE_SWADVANCE -7, DE_SWUPDN -6); the -5 and -4 addresses beside them "
            "are S11_SWCPUDIAG and S11_SWSOUNDDIAG, which exist on Williams System 11 and not "
            "here. s11.c reads Advance inverted on Data East, as !core_getSw(DE_SWADVANCE)."
        )},
        "spatial": not_applicable("cabinet_or_service", [CORE]),
    })

# DIP: s11.c declares MDRV_DIPS(1) and reads a single jumper bit on PIA2 PA7. The public address
# is 0, matching the platform profile's own {"values": [0]} rule and the Whirlwind record.
inputs.append({
    "id": "dip.jumper-w7",
    "label": "Jumper W7",
    "kind": "dip_switch",
    "binding": {"group": "pinmame.input.dip", "device": 0},
    "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
    "availability": "unknown",
    "provenance": prov("observed", [CORE]),
    "physical": {"notes": (
        "s11.c declares MDRV_DIPS(1), commented '(actually a jumper)', and pia2a_r reads it as "
        "core_getDip(0) << 7 on PIA2 PA7, annotated 'PA7 (I) Jumper W7'. Unlike S11_COMPORTS, "
        "DE_COMPORTS declares no country DIP at all, so the meaning of this bit is not stated by "
        "pinned source and this manual does not document it either."
    )},
    "spatial": not_applicable("dip_switch", [CORE]),
})

outputs = []


def coil_wiring(entry):
    """Only the fields the manual actually prints. Drive 22 has no wire colour or coil type, and
    emitting a null there would assert 'the manual says none' rather than 'the manual is silent'."""
    wiring = {"board": "CPU Board"}
    if entry.get("transistor"):
        wiring["driver_transistor"] = entry["transistor"]
    if entry.get("wire"):
        wiring["control_wire"] = entry["wire"]
    if entry.get("connector"):
        wiring["control_connection"] = entry["connector"]
    return wiring


# --- Public 1-8: the LEFT half of the Left/Right relay pair -------------------------------
# The manual states the mechanism in prose on printed page 28: "The Left/Right relay is used in
# conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these
# sets are termed 'left' and 'right'." Pinned PinMAME implements exactly that at s11.c:564-574,
# where energising the mux solenoid re-routes outputs 1-8 to 25-32.
for address in range(1, 9):
    entry = MUX[str(address)]
    left = entry["left"]
    fitted = left.get("name") is not None
    fitment_conflict = address == 3
    device_id = f"coil.driver-{address}"
    notes = [
        "Left half of the Left/Right relay pair on printed drive "
        f"{address}; the right half is published at address {address + 24}.",
    ]
    if not fitted:
        notes.append("The Special Coil Wiring Diagram prints 'NO COIL AT THIS LOCATION (NOT USED)' on this half.")
    if fitment_conflict:
        notes.append(
            "The printed-page-28 location drawing nevertheless has a clearly legible 3L callout "
            "in the lower-right shooter-housing/cabinet extension. The drawing supplies neither "
            "a device name nor a recoverable leader termination, and the retained script has no "
            "SolCallback(3), so physical fitment and function remain unresolved."
        )
    if left.get("note"):
        notes.append(left["note"] + ".")
    if address == 6:
        notes.append(
            "The drive table's printed 'Left 3 Bank' label is preserved as a manual alias, but "
            "printed-page-28 callout 6L places this reset coil at the center drop-target bank; the "
            "switch chart and retained script's dtM binding independently agree on that mechanism."
        )
    record = {
        "id": device_id,
        "label": (
            "Center Drop-Target Bank Reset (manual: Left 3 Bank)"
            if address == 6 else
            "Unresolved Left Driver 3 (manual conflict)" if fitment_conflict else
            left.get("name") or f"Unfitted Coil Driver {address} (Left)"
        ),
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "unknown" if fitment_conflict else "used" if fitted else "unused",
        "provenance": prov("candidate" if fitment_conflict else "validated", [MANUAL, CORE] + ([SCRIPT_REF] if fitment_conflict or address == 8 else [])),
        "physical": {"notes": " ".join(notes)},
        "wiring": coil_wiring(entry),
    }
    if left.get("coil_type"):
        record["physical"]["part_number"] = left["coil_type"]
    if not fitted and not fitment_conflict:
        record["spatial"] = not_applicable("unused", [MANUAL])
    else:
        spatial = placement(device_id, "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if spatial:
            record["spatial"] = spatial
            record["physical"]["notes"] += " The coordinate is the retained mechanism location confirmed by the printed coil-location drawing, not a claimed winding-center measurement."
        elif address == 8:
            record["physical"]["notes"] += " The printed-page-28 drawing has no readable 8L callout, and the retained script's KnockerPosition is only a sound-placement helper rather than physical geometry; the spatial key is omitted and the blocker report names the gap."
    outputs.append(record)

# --- Public 9-16: direct drivers on CN-12, not muxed ---------------------------------------
# Kind "gi" on an ordinary solenoid address: this platform has no separate GI channel, so a
# general-illumination device binds to pinmame.output.solenoid and is typed gi. Drives 13 and 14
# are the mars-light pair the printed diagram alone cannot disambiguate.
DIRECT_KIND = {
    "9": "flasher", "10": "relay", "11": "gi", "12": "coil",
    # Drive 13 is printed NO COIL AT THIS LOCATION and carries nothing. Drive 14 drives the mars
    # light beacon: SolCallback(14) = SolRotateBeacons in the retained script. An earlier revision
    # encoded both as unfitted while the mechanism simultaneously named 14 as its actuator, which
    # was self-contradictory.
    "13": "virtual", "14": "motor", "15": "coil", "16": "flasher",
}
for address in range(9, 17):
    entry = AUX[str(address)]
    device_id = f"coil.driver-{address}"
    notes = ["Direct CPU driver on CN-12; not affected by the Left/Right relay."]
    if entry.get("bulbs"):
        where = f" ({entry['placement']})" if entry.get('placement') else ""
        notes.append(f"Drives {entry['bulbs']} flash lamps{where}.")
    if entry.get("note"):
        notes.append(entry["note"])
    record = {
        "id": device_id,
        "label": entry["name"] or (
            "Mars Light Beacon" if address == 14 else f"Unfitted Driver {address}"),
        "kind": DIRECT_KIND[str(address)],
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "unused" if address == 13 else "used",
        # Drive 14 is identified by the retained script, not by the printed table, so the script
        # is part of its provenance rather than an unnamed influence.
        "provenance": prov("validated", [MANUAL, CORE] + ([SCRIPT_REF] if address in (13, 14) else [])),
        "physical": {"notes": " ".join(notes)},
        "wiring": coil_wiring(entry),
    }
    if address == 11:
        record["roles"] = ["playfield.general-illumination"]
    if entry.get("bulbs"):
        record["physical"]["quantity"] = int(entry["bulbs"].split("(", 1)[1].split(")", 1)[0])
    if address in (9, 11, 16):
        spatial = placement(device_id, "effect" if address in (9, 16) else "emitter", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if spatial:
            record["spatial"] = spatial
            if entry.get("bulbs") and len(spatial["placements"]) != record["physical"]["quantity"]:
                record["physical"]["notes"] += (
                    f" The known-working script exposes {len(spatial['placements'])} in-bounds Light effect "
                    f"object(s), not the manual's {record['physical']['quantity']} physical bulb sockets; "
                    "the recorded points are presentation effects and are not a complete socket survey."
                )
        if address == 11:
            record["physical"]["notes"] += (
                " The retained script's GI collection contains 35 in-bounds playfield Light "
                "objects, all recorded individually. GI_BG is excluded because its negative raw "
                "y coordinate identifies it as an off-playfield visual proxy, not a playfield bulb."
            )
    elif address == 14:
        record["spatial"] = not_applicable("cabinet_or_service", [MANUAL, SCRIPT_REF])
    elif address == 13:
        record["spatial"] = not_applicable("unused", [MANUAL, SCRIPT_REF])
    else:
        spatial = placement(device_id, "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if spatial:
            record["spatial"] = spatial
            record["physical"]["notes"] += " The coordinate is the retained mechanism location confirmed by the printed coil-location drawing, not a claimed winding-center measurement."
        else:
            record["spatial"] = not_applicable("internal_nonvisual", [MANUAL])
    outputs.append(record)

# --- Public 17-22: the six switched/special solenoids ---------------------------------------
# CORE_FIRSTSSSOL is 17 and there are six of them; the manual heads this exact block "CPU
# Controlled Auxiliary Solenoids" and numbers it 17-22. Note DE uses its own permutation of the
# PIA CA2/CB2 lines, ssSolNo[1] = {3,4,5,1,0,2}, distinct from the Williams ordering.
for address in range(17, 23):
    entry = AUXSOL[str(address)]
    device_id = f"coil.driver-{address}"
    notes = [
        "One of the six switched/special solenoids; CORE_FIRSTSSSOL is 17 and Data East uses its "
        "own PIA CA2/CB2 permutation, ssSolNo[1] = {3,4,5,1,0,2}, not the Williams ordering. The "
        "drive-transistor assignment is transcribed from this machine's own printed table rather "
        "than assumed from the platform, because it is a per-game wiring fact.",
    ]
    if entry.get("note"):
        notes.append(entry["note"])
    record = {
        "id": device_id,
        "label": entry["name"],
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE]),
        "physical": {"notes": " ".join(notes)},
        "wiring": {k: v for k, v in {
            "board": "CPU Board",
            "driver_transistor": entry["transistor"],
            "control_wire": entry["control"]["wire"],
            "control_connection": entry["control"]["connector"],
            "power_wire": entry["power"]["wire"],
            "power_connection": entry["power"]["connector"],
        }.items() if v is not None},
    }
    if entry.get("coil_type"):
        record["physical"]["part_number"] = entry["coil_type"]
    spatial = placement(device_id, "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
    if spatial:
        record["spatial"] = spatial
        record["physical"]["notes"] += " The coordinate is the retained mechanism location confirmed by the printed coil-location drawing, not a claimed winding-center measurement."
    outputs.append(record)

# --- Public 23, 24 --------------------------------------------------------------------------
outputs.append({
    "id": "coil.game-on",
    "label": "Game On / Flipper Enable",
    "kind": "control_signal",
    "binding": {"group": "pinmame.output.solenoid", "device": 23},
    "aliases": [{"namespace": "pinmame.solenoid", "value": "23"}],
    "availability": "used",
    "provenance": prov("validated", [CORE]),
    "physical": {"notes": (
        "S11_GAMEONSOL is 23, driven by PIA0 CB2 (s11.c:611-616) and typed CORE_MODOUT_PULSE. It "
        "gates the flippers and the switched solenoids rather than driving a device of its own."
    )},
    "spatial": not_applicable("virtual", [CORE]),
})
outputs.append({
    "id": "coil.unused-24",
    "label": "Unused Solenoid 24",
    "kind": "virtual",
    "binding": {"group": "pinmame.output.solenoid", "device": 24},
    "aliases": [{"namespace": "pinmame.solenoid", "value": "24"}],
    "availability": "unused",
    "provenance": prov("validated", [CORE]),
    "physical": {"notes": "Reserved slot between the switched solenoids and the muxed right set."},
    "spatial": not_applicable("unused", [CORE]),
})

# --- Public 25-32: the RIGHT half of the relay pair, all flash lamps ------------------------
for address in range(25, 33):
    drive = address - 24
    entry = MUX[str(drive)]
    right = entry["right"]
    device_id = f"flasher.driver-{drive}-right"
    record = {
        "id": device_id,
        "label": f"Flash Lamps, Drive {drive} (Right)",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(drive)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE]),
        "physical": {
            "quantity": int(right["bulbs"].split("(", 1)[1].split(")", 1)[0]),
            "notes": (
                f"Right half of the Left/Right relay pair on printed drive {drive}; the left half "
                f"is published at address {drive}. Drives {right['bulbs']} ({right['placement']}). "
                "PinMAME types the whole 25-32 block uniformly as No. 89 flashers, and this "
                "machine's printed Special Coil Wiring Diagram agrees on every one of the eight "
                "drives. The per-drive counts and locations above are the manual's."
            ),
        },
        "wiring": coil_wiring(entry),
    }
    spatial = placement(device_id, "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
    if spatial:
        record["spatial"] = spatial
        observed_count = len(spatial["placements"])
        manual_count = record["physical"]["quantity"]
        if observed_count != manual_count:
            comparison = "more" if observed_count > manual_count else "fewer"
            record["physical"]["notes"] += (
                f" The known-working script exposes {observed_count} in-bounds Light effect object(s), "
                f"{comparison} than the manual's {manual_count} physical bulb sockets. These are presentation "
                "effect centers, not a complete socket survey; no missing or extra hardware bulb is inferred."
            )
    outputs.append(record)

# --- Public 33-44: inert on this platform ---------------------------------------------------
for address in range(33, 45):
    reason = ("core_getSol only serves 33-36 for GEN_ALLWPC/GEN_SAM, and this game is GEN_DEDMD32"
              if address <= 36 else
              "the S11 'extra' block at 37-44 is written only under S11_SNDOVERLAY or "
              "S11_PRINTERLINE, and lw3GameData sets gameSpecific1 = 0")
    outputs.append({
        "id": f"coil.inert-{address}",
        "label": f"Inert Solenoid Address {address}",
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "provenance": prov("validated", [CORE]),
        "physical": {"notes": f"Always reads 0 on this machine: {reason}."},
        "spatial": not_applicable("virtual", [CORE]),
    })

# --- Public 45-48: synthesised lower flipper coils -------------------------------------------
FLIPPERS = {45: ("Synthetic Lower Right Flipper Power", "right"), 46: ("Synthetic Lower Right Flipper Hold", "right"),
            47: ("Synthetic Lower Left Flipper Power", "left"), 48: ("Synthetic Lower Left Flipper Hold", "left")}
for address, (label, side) in FLIPPERS.items():
    flip = TRANSCRIPTION["flipper_solenoids"][side]
    outputs.append({
        "id": f"coil.flipper-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE]),
        "physical": {
            "part_number": flip["coil_type"],
            "notes": (
                "Not a CPU-driven output on this machine. lw3GameData declares no FLIP_SOL, so "
                "core.c:1746-1753 synthesises these bits whenever Game On is active and the "
                "corresponding flipper button is down. Power and hold therefore assert and "
                "release together and are not independently controllable; a recreation must not "
                "model them as two separate coils. The physical coils are driven from the "
                "Flipper PCB, which the manual documents in its own unnumbered 'Flipper "
                "Solenoids' table listing a left and a right flipper only - there is no upper "
                "flipper of either hand."
            ),
        },
        "wiring": {
            "board": "Flipper PCB",
            "control_wire": flip["control"]["wire"],
            "control_connection": flip["control"]["connector"],
            "power_wire": flip["power"]["wire"],
            "power_connection": flip["power"]["connector"],
        },
        "spatial": not_applicable("virtual", [MANUAL, CORE]),
    })

# --- Public 49, 50 ---------------------------------------------------------------------------
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL; lw3GameData declares custSol = 0, so nothing is published from 51 upward."),
):
    outputs.append({
        "id": f"coil.reserved-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "provenance": prov("validated", [CORE]),
        "physical": {"notes": note},
        "spatial": not_applicable("virtual", [CORE]),
    })

# --- Lamps 1-64 -------------------------------------------------------------------------------
# Every one of the 64 matrix positions is populated on this machine: the printed chart carries no
# "Not Used" cell anywhere, which is unusual and worth stating rather than assuming.
for address in range(1, 65):
    record = LAMPS[str(address)]
    device_id = f"lamp.matrix-{address}"
    is_cabinet = record["name"].startswith("Cab.")
    entry = {
        "id": device_id,
        "label": record["name"],
        "kind": "lamp",
        "binding": {"group": "pinmame.output.lamp", "device": address},
        "aliases": [{"namespace": "pinmame.lamp", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE] + [SCRIPT_REF]),
        "physical": {"notes": f"Printed lamp-matrix column {record['column']}, row {record['row']}."},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": record["column_drive"]["transistor"],
            "drive_wire": record["column_drive"]["wire"],
            "drive_connection": record["column_drive"]["connector"],
            "return_wire": record["row_return"]["wire"],
            "return_connection": record["row_return"]["connector"],
            "return_component": record["row_return"]["transistor"],
        },
    }
    if is_cabinet:
        entry["roles"] = ["cabinet.start"]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        spatial = placement(device_id, "emitter", f"lamp.{address}", [TABLE, MANUAL])
        if spatial:
            entry["spatial"] = spatial
            if len(spatial["placements"]) > 1:
                entry["physical"]["notes"] += (
                    f" The retained table models {len(spatial['placements'])} separate bulbs on "
                    "this one address, at positions far enough apart to be distinct inserts rather "
                    "than a duplicated helper, so each is placed individually.")
    outputs.append(entry)

displays = [{
    "id": "display.dmd",
    "label": "128x32 Dot Matrix Display",
    "kind": "dmd",
    "width": 128,
    "height": 32,
    "provenance": prov("validated", [CORE, MANUAL, ADDENDUM]),
    "spatial": not_applicable("cabinet_or_service", [CORE, MANUAL]),
}]
# The manual as printed is WRONG about this and the addendum is what fixes it. Printed page 23
# says the display is 32x64; the factory addendum of 2 July 1992 states "The display is made up of
# 32 X 128 Dots not 32 X 64 Dots", which is what pinned PinMAME independently declares through
# de_128x32DMD and SNDBRD_DEDMD32 under GEN_DEDMD32. Without the addendum the manual and the
# emulator would appear to disagree, and the manual would have been the wrong side to believe.

mechanisms = [
    {
        "id": "mechanism.ball-trough",
        "label": "Ball Trough",
        "kind": "kicker",
        "actuators": ["coil.driver-1", "coil.driver-2"],
        "sensors": ["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13"],
        "behavior": (
            "Outhole at 10 feeding a three-position trough at 11-13. The manual wires printed drive "
            "1 to the Outhole coil and drive 2 to the Trough Eject coil, and the retained script "
            "binds SolCallback(1) to SolTrough and SolCallback(2) to SolRelease, so the manual and "
            "the script agree on both actuators. Individual trough positions have no table object "
            "of their own."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.center-drop-bank",
        "label": "Center Drop Target Bank",
        "kind": "drop_target_bank",
        "actuators": ["coil.driver-6"],
        "sensors": ["switch.matrix-25", "switch.matrix-26", "switch.matrix-27"],
        "behavior": (
            "Three drop targets printed Center Drop Tar. Left/Mid./Right at 25-27, reset as a bank. "
            "These are genuinely drop targets rather than standups: the retained script builds a "
            "DropTarget instance per address (DT25, DT26, DT27) and binds the reset coil through "
            "SolCallback(6) = dtMSolDropUp. The drive table calls the left relay half 'LEFT 3 "
            "BANK', but the same manual's printed-page-28 location drawing places callout 6L "
            "beside the physical center bank, so the label denotes the relay half rather than a "
            "left-side playfield bank."
        ),
        "positions": [
            {"id": "mechanism.center-drop-bank.left", "label": "Center Drop Tar. Left", "sensors": ["switch.matrix-25"]},
            {"id": "mechanism.center-drop-bank.middle", "label": "Center Drop Tar. Mid.", "sensors": ["switch.matrix-26"]},
            {"id": "mechanism.center-drop-bank.right", "label": "Center Drop Tar. Right", "sensors": ["switch.matrix-27"]},
        ],
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.right-drop-bank",
        "label": "Right Drop Target Bank",
        "kind": "drop_target_bank",
        "actuators": ["coil.driver-7"],
        "sensors": ["switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
        "behavior": (
            "Three drop targets printed Right Drop Tar. Top/Mid./Bot. at 33-35, reset as a bank by "
            "printed drive 7 ('Right 3 Bank'). The script agrees on both counts: DT33/DT34/DT35 are "
            "DropTarget instances and SolCallback(7) is dtRSolDropUp."
        ),
        "positions": [
            {"id": "mechanism.right-drop-bank.top", "label": "Right Drop Tar. Top", "sensors": ["switch.matrix-33"]},
            {"id": "mechanism.right-drop-bank.middle", "label": "Right Drop Tar. Mid.", "sensors": ["switch.matrix-34"]},
            {"id": "mechanism.right-drop-bank.bottom", "label": "Right Drop Tar. Bot.", "sensors": ["switch.matrix-35"]},
        ],
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.left-four-bank",
        "label": "Left 4 Bank Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.matrix-17", "switch.matrix-18", "switch.matrix-19", "switch.matrix-20"],
        "behavior": (
            "Four stationary stand-up targets printed Left 4 Bank Top 4 / Mid. 3 / Mid. 2 / Bot. "
            "1 at 17-20. The switch-parts table assigns all four ordinary stand-up target part "
            "180-5082-06, the printed coil inventory carries no reset drive for them, and the "
            "retained script models them as hit targets rather than DropTarget instances. They "
            "therefore have no actuator."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.mars-light",
        "label": "Mars Light Beacon",
        "kind": "motorized",
        "actuators": ["coil.driver-14"],
        "sensors": [],
        "behavior": (
            "A rotating beacon. The Special Coil Wiring Diagram draws a MARS LIGHT through a 1 AMP "
            "S.B. fuse to PSCN 4 on a node that both drive 13 and drive 14 touch, and prints 'NO "
            "COIL AT THIS LOCATION' against drive 13, so the drawing alone does not say which "
            "energises it. The retained known-working script settles it: SolCallback(14) is "
            "SolRotateBeacons, commented 'Mars Light aka Beacon'. Drive 13 carries no device."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.ball-locks",
        "label": "Ball Lock Ejects",
        "kind": "kicker",
        "actuators": ["coil.driver-4", "coil.driver-5"],
        "sensors": ["switch.matrix-32", "switch.matrix-40"],
        "behavior": (
            "Two eject assemblies, printed Left Eject on drive 4 and Right Eject on drive 5, with "
            "the Right Saucer at switch 32 and the Left Saucer at switch 40. The script binds them "
            "as two cvpmBallStack devices, SolCallback(4) = bsLock.SolOut and SolCallback(5) = "
            "bsLock2.SolOut. The same script explicitly initializes bsLock with sw40 and bsLock2 "
            "with sw32, so drive 4 pairs with the Left Saucer and drive 5 with the Right Saucer; "
            "the manual and script agree on both complete sensor-to-actuator paths."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.vertical-up-kicker",
        "label": "Vertical Up-Kicker",
        "kind": "kicker",
        "actuators": ["coil.driver-15"],
        "sensors": ["switch.matrix-31"],
        "behavior": (
            "The VUK at switch 31, kicked by printed drive 15 which the manual wires at +50 V "
            "through Q2. The script agrees: SolCallback(15) is VukTopPop."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.kickback",
        "label": "Kickback",
        "kind": "kicker",
        "actuators": ["coil.driver-22"],
        "sensors": [],
        "behavior": (
            "Printed drive 22 is 'Kickback (See Schematic)' among the switched solenoids, and the "
            "script binds SolCallback(22) to SolKickback. The superseded legacy migrated record "
            "also names address 22 Kickback, so all three agree."
        ),
        "provenance": prov("validated", [MANUAL, SCRIPT_REF, LEGACY]),
    },
    {
        "id": "mechanism.turbo-bumpers",
        "label": "Turbo Bumpers",
        "kind": "other",
        "actuators": ["coil.driver-17", "coil.driver-18", "coil.driver-19"],
        "sensors": ["switch.matrix-44", "switch.matrix-45", "switch.matrix-46"],
        "behavior": (
            "Three pop bumpers. The switched-solenoid table gives Left, Center and Right Turbo "
            "Bumper on drives 17, 18 and 19, and the switch matrix gives the matching skirt "
            "switches at 44, 45 and 46, each side agreeing on the left/center/right ordering."
        ),
        "positions": [
            {"id": "mechanism.turbo-bumpers.left", "label": "Left Turbo Bumper", "sensors": ["switch.matrix-44"]},
            {"id": "mechanism.turbo-bumpers.center", "label": "Center Turbo Bumper", "sensors": ["switch.matrix-45"]},
            {"id": "mechanism.turbo-bumpers.right", "label": "Right Turbo Bumper", "sensors": ["switch.matrix-46"]},
        ],
        "provenance": prov("validated", [MANUAL]),
    },
]

relationships = [
    {
        "id": f"relationship.left-right-relay-{drive}",
        "kind": "relay_gated",
        "source": "coil.driver-10",
        "destination": f"flasher.driver-{drive}-right",
        "provenance": prov("validated", [MANUAL, CORE]),
    }
    for drive in range(1, 9)
]

conflicts = [
    {
        "id": "conflict.drive-3-left-fitment",
        "path": "/outputs/coil.driver-3/availability",
        "description": (
            "The Special Coil Wiring Diagram prints 'NO COIL THIS LOCATION' for drive 3's left "
            "half, while the same manual's printed-page-28 location drawing has a clearly legible "
            "3L callout in the lower-right shooter-housing/cabinet extension. The drawing does not "
            "name the device or expose a recoverable leader termination, and the retained script "
            "has no SolCallback(3), so neither fitted nor unused is asserted."
        ),
        "source_refs": [MANUAL, SCRIPT_REF],
    },
    {
        "id": "conflict.drive-6-flasher-effect-count",
        "path": "/outputs/flasher.driver-6-right/spatial",
        "description": (
            "The manual prints three physical No. 89 flash lamps on right-side drive 6, while the "
            "known-working script binds four in-bounds Light effect objects (F130, F130a, F130b, "
            "F130c). The four recorded coordinates are presentation effects rather than four claimed "
            "physical sockets; an original-machine socket survey is needed to select the three bulbs."
        ),
        "source_refs": [MANUAL, TABLE, SCRIPT_REF],
    },
]

# --- Drivers ----------------------------------------------------------------------------------
# The variant prose is DERIVED from the parsed ROM inventory rather than asserted, and a guard
# below refuses to build if a note fails to name a ROM that actually differs. An earlier machine
# in this project shipped "only the CPU game ROM differs" for 45 clones when it was untrue for
# eight of them, so the rule is enforced mechanically here instead of being remembered.
DRIVER_LABELS = {
    "lw3_208": "Lethal Weapon 3 (2.08)", "lw3_207": "Lethal Weapon 3 (2.07 Canadian)",
    "lw3_205": "Lethal Weapon 3 (2.05)", "lw3_203": "Lethal Weapon 3 (2.03)",
    "lw3_200": "Lethal Weapon 3 (2.00)", "lw3_e204": "Lethal Weapon 3 (2.04 English)",
    "lw3_208p": "Lethal Weapon 3 (2.08p, Voices Mod)",
    "lw3_300": "Lethal Weapon 3 (3.00 unofficial MOD)",
    "lw3_301": "Lethal Weapon 3 (3.01 unofficial MOD)",
}
ROOT_DRIVER = "lw3_208"
# Years come from the catalog rather than being typed: this is a 1992 machine, and three of its
# nine drivers are later software (a 2013 voices mod and two 2020 community rulesets). An earlier
# revision hard-coded 1991 for all nine, which was Batman's year.
DRIVER_YEARS = {
    "lw3_200": "1992", "lw3_203": "1992", "lw3_205": "1992", "lw3_207": "1992",
    "lw3_208": "1992", "lw3_e204": "1992", "lw3_208p": "2013",
    "lw3_300": "2020", "lw3_301": "2020",
}
_root = ROM_SETS[ROOT_DRIVER]["roms"]
# Six ROMs per set on this machine, not Batman's four: the 128x32 display needs two
# display ROMs (drom1/drom0) where the 128x16 needed one.
# All six ROM roles, not three. The Voices Mod differs only in two SOUND ROMs, so a
# three-role comparison silently called it byte-identical to the root.
_ROLES = ("CPU", "display 1", "display 0", "sound U7", "sound U17", "sound U21")

drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]["roms"]
    macro = ROM_SETS[driver_id]["macro"]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root and the latest shipped production firmware. Every lw3_* set shares one "
            "lw3GameData through PinMAME's CORE_GAMEDEF macro, so all nine present identical "
            "playfield hardware and identical public addresses. Three of the nine are later "
            "software rather than factory releases - a 2013 voices mod and two 2020 community "
            "rulesets - which run on this same physical machine and so remain driver variants of "
            "it rather than new games."
        )
    else:
        differing = [(role, mine) for role, mine, theirs in zip(_ROLES, roms, _root) if mine != theirs]
        if differing:
            note = "Differs from the root in " + ", ".join(
                f"the {role} ROM ({rom})" for role, rom in differing) + "."
        else:
            note = "Byte-identical ROM set to the root."
        if macro != ROM_SETS[ROOT_DRIVER]["macro"]:
            note += (f" Also uses a different ROM layout macro ({macro} rather than "
                     f"{ROM_SETS[ROOT_DRIVER]['macro']}), which changes how the CPU images are "
                     "loaded but not the hardware.")
        note += (" The shared lw3GameData means the address model is unchanged.")
        if DRIVER_YEARS[driver_id] != "1992":
            note += (f" PinMAME dates this set {DRIVER_YEARS[driver_id]}: it is later software for "
                     "the same physical machine, not a new game.")
    drivers.append({
        "id": driver_id,
        "description": DRIVER_LABELS[driver_id],
        "year": DRIVER_YEARS[driver_id],
        "manufacturer": "Data East",
        "flags": 0,
        "physical_compatibility": "identical",
        "variant_notes": note,
        **({} if driver_id == ROOT_DRIVER else {"clone_of": ROOT_DRIVER}),
    })

# Fail closed. A note that does not name a ROM which genuinely differs is a silent lie, and this
# is the only thing standing between the parsed inventory and the published prose.
for _driver in drivers:
    _roms = ROM_SETS[_driver["id"]]["roms"]
    for _role, _mine, _theirs in zip(_ROLES, _roms, _root):
        if _mine != _theirs and _mine not in _driver["variant_notes"]:
            raise SystemExit(
                f"{_driver['id']}: {_role} ROM {_mine} differs from the root but the note omits it")

sources = [
    {
        "id": CATALOG, "kind": "pinmame_catalog",
        "uri": "https://github.com/vpinball/pinmame",
        "revision": "4ec52ff0ac133ac251681518aed2249e19fe26eb",
        "locator": "PinmameGetGames", "license": "BSD-3-Clause",
        "attribution": "PinMAME contributors",
    },
    {
        "id": CORE, "kind": "pinmame_core",
        "uri": "https://github.com/vpinball/pinmame",
        "revision": "4ec52ff0ac133ac251681518aed2249e19fe26eb",
        "locator": "src/wpc/degames.c; src/wpc/s11.c; src/wpc/s11.h; src/wpc/core.c; src/wpc/core.h; src/wpc/dedmd.c; src/wpc/desound.c",
        "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
    },
    {
        "id": MANUAL, "kind": "manual",
        "uri": "external:pinmame-manual-cache/by-machine/data-east.lethal-weapon-3.1992/contributor-supplied/Lethal_Weapon_3_OPS.pdf",
        "locator": "Lethal_Weapon_3_OPS.pdf; printed pages 24-29 (PDF 28-33); contributor-supplied scan, 93 pages, no text layer",
        "sha256": TRANSCRIPTION["document_sha256"],
        "original_filename": "Lethal_Weapon_3_OPS.pdf",
        # A hash proves the local copy has not changed; it says nothing about what the document
        # said, and this manual is a 93-page image-only scan nobody else can grep. The regions
        # actually read are transcribed beside the definition and digest-checked.
        "excerpts": [
            {
                "id": "excerpt.lethal-weapon-3.switch-matrix",
                "locator": "printed pages 24-25 (PDF 28-29), Switch Matrix Chart and complete Switch Part Numbers table",
                "path": "evidence/excerpts/data-east.lethal-weapon-3.1992/switch-matrix.md",
                "sha256": EXCERPT_HASHES["switch-matrix.md"],
                "method": "manual",
                "transcribed_by": "curator, read from a 400 dpi render; this document has no text layer",
                "reviewed": True,
            },
            {
                "id": "excerpt.lethal-weapon-3.lamp-matrix",
                "locator": "printed page 26 (PDF 30), Lamp Matrix Chart",
                "path": "evidence/excerpts/data-east.lethal-weapon-3.1992/lamp-matrix.md",
                "sha256": EXCERPT_HASHES["lamp-matrix.md"],
                "method": "manual",
                "transcribed_by": "curator, read from a 400 dpi render; this document has no text layer",
                "reviewed": True,
            },
            {
                "id": "excerpt.lethal-weapon-3.coil-drivers",
                "locator": "printed pages 28-29 (PDF 32-33), CPU Controlled Auxiliary Solenoids, Flipper Solenoids and the Special Coil Wiring Diagram",
                "path": "evidence/excerpts/data-east.lethal-weapon-3.1992/coil-drivers.md",
                "sha256": EXCERPT_HASHES["coil-drivers.md"],
                "image": "evidence/excerpts/data-east.lethal-weapon-3.1992/coil-flash-location.webp",
                "image_sha256": COIL_LOCATION_IMAGE_SHA256,
                "image_derivation": "Lethal_Weapon_3_OPS.pdf page 32, rendered at 600 dpi with pdftoppm; 1600x3600-pixel crop at +500+2670, reduced to 900px wide grayscale, quality 25 WebP",
                "method": "manual",
                "transcribed_by": "curator, read from 400 dpi renders; this document has no text layer",
                "reviewed": True,
            },
        ],
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "Data East Pinball, Inc.",
    },
    {
        # A primary factory correction to the manual, not a secondary commentary on it. Its most
        # consequential line is the display: the manual as printed says 32x64 and is simply wrong.
        "id": ADDENDUM, "kind": "service_bulletin",
        "uri": "external:pinmame-manual-cache/by-machine/data-east.lethal-weapon-3.1992/contributor-supplied/LW3Addendum.pdf",
        "locator": "LW3Addendum.pdf; 2 pages dated 2 July 1992; text changes to printed pages 19 and 23, parts changes to 30-41, and a flipper-assembly parts illustration",
        "sha256": ADDENDUM_SHA256,
        "original_filename": "LW3Addendum.pdf",
        # The addendum's excerpt hangs off the addendum, not off the manual. An earlier revision
        # attached it to the operations-manual source, so the digest described a document that
        # source did not name.
        "excerpts": [{
            "id": "excerpt.lethal-weapon-3.addendum",
            "locator": "factory addendum of 2 July 1992, both pages",
            "path": "evidence/excerpts/data-east.lethal-weapon-3.1992/addendum.md",
            "sha256": EXCERPT_HASHES["addendum.md"],
            "method": "manual",
            "transcribed_by": "curator, read from the contributor-supplied addendum",
            "reviewed": True,
        }],
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "Data East Pinball, Inc.",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": "external:pinmame-vpx-sources/data-east/lethal-weapon-3-1992/Lethal%20Weapon%203%20%28Data%20East%201992%29%20VPW%202.0.vpx",
        "locator": "retained known-working recreation, VPW 2.0; playfield 952 x 2162",
        "sha256": HASHES["table_sha256"],
        "known_working": True,
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; the table script credits tomate, apophis, iaakki, mcarter78, DGrimmReaper, fluffhead and Wylte",
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": "external:pinmame-vpx-sources/data-east/lethal-weapon-3-1992/Lethal%20Weapon%203%20%28Data%20East%201992%29%20VPW%202.0.vbs",
        "locator": "table script; vpmMapLights AllLamps binding, SolCallback/SolModCallback map and Controller.Switch handlers",
        "sha256": HASHES["script_sha256"],
        "known_working": True,
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; the table script credits tomate, apophis, iaakki, mcarter78, DGrimmReaper, fluffhead and Wylte",
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": "external:pinmame-vpx-sources/data-east/lethal-weapon-3-1992/extraction-manifest.json",
        "locator": (f"vpxtool extraction of the retained table, {HASHES['extraction_file_count']} files, "
                    f"{HASHES['extraction_total_bytes']} bytes; the manifest's own manifest_sha256 field is "
                    f"{HASHES['manifest_sha256']} and is recomputable by the algorithm the file states"),
        "sha256": HASHES["manifest_file_sha256"],
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; the table script credits tomate, apophis, iaakki, mcarter78, DGrimmReaper, fluffhead and Wylte",
    },
    {
        "id": LEGACY, "kind": "legacy_json",
        "uri": "https://github.com/vpinball/pinmame-game-defs",
        "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
        "locator": "games/lw3.json; origin=vbscript-parser",
        "attribution": "pinmame-game-defs contributors",
    },
]

_placed = sum(len(d.get("spatial", {}).get("placements", []))
              for d in inputs + outputs)

definition = {
    "format": "pinmame-machine-definition",
    "schema_version": 2,
    "machine": {
        "id": "data-east.lethal-weapon-3.1992",
        "name": "Lethal Weapon 3",
        "manufacturer": "Data East",
        "year": 1992,
        "kind": "physical_pinball",
        "playfield": {"width": RESOLUTION["playfield"]["width"],
                      "height": RESOLUTION["playfield"]["height"],
                      "units": "vpx"},
    },
    "controller": {
        "platform": "pinmame.dataeast",
        "hardware_generation": "0x4000",
        "inversion_applied_by_emulator": True,
    },
    "coverage": {
        "status": "partial",
        "dimensions": {
            "catalog_identity": "validated",
            "address_enumeration": "validated",
            "semantic_naming": "candidate",
            "physical_wiring": "validated",
            "mechanisms": "validated",
            "variant_coverage": "validated",
            "recreation_knowledge": "validated",
            "spatial_placement": "observed",
        },
        "missing": ["output_semantics", "polarity", "spatial_placement", "unresolved_conflicts"],
    },
    "drivers": drivers,
    "inputs": inputs,
    "outputs": outputs,
    "displays": displays,
    "mechanisms": mechanisms,
    "relationships": relationships,
    "conflicts": conflicts,
    "sources": sources,
    "knowledge": {"path": "knowledge/data-east/lethal-weapon-3-1992.md", "status": "partial"},
}

# --- Spatial report ---------------------------------------------------------------------------
# Generated from the same objects as the definition, so a statement here cannot outlive the data
# behind it. Everything that has no coordinate is named rather than counted.
# Identify devices by canonical id, never by bare address: switch 17 and lamp 17 are different
# devices and a numeric-only audit cannot tell them apart, which makes the measured-versus-computed
# split unauditable and puts the same number in two different blocker lists.
_unplaced_internal = sorted(
    d["id"] for d in inputs + outputs
    if d["availability"] == "used" and "spatial" in d
    and d["spatial"].get("status") == "not_applicable"
    and d["spatial"].get("reason") == "internal_nonvisual")
_no_spatial_key = sorted(d["id"] for d in inputs + outputs if "spatial" not in d)
_KIND_TO_ID = {"switch": "switch.matrix-", "lamp": "lamp.matrix-"}
_computed = sorted(
    v.get("device_id") or (_KIND_TO_ID[k.split(".")[0]] + k.split(".")[1])
    for k, v in PLACES.items() if v["coordinate_origin"] == "computed-centroid")
_spatial_blockers = []
if _unplaced_internal or _no_spatial_key:
    _spatial_blockers.append({
        "id": "devices-without-a-retained-object",
        "severity": "major",
        "detail": (
            "These fitted or unresolved-fitment devices have no honest coordinate in the retained "
            "recreation. Devices "
            "that genuinely sit inside a mechanism are recorded not_applicable/internal_nonvisual; "
            "a used or unresolved-fitment device with no retained object omits the spatial key "
            "rather than fabricating a location."
        ),
        "internal_nonvisual_devices": _unplaced_internal,
        "omitted_spatial_key_devices": _no_spatial_key,
    })
_spatial_blockers.append({
    "id": "flasher-effects-are-not-a-socket-survey",
    "severity": "major",
    "detail": (
        "The retained script binds visual Light effects, not surveyed physical bulb sockets. Manual "
        "quantities exceed the retained effect count for addresses 9, 16, 25-27, 29, 31 and 32; "
        "address 30 instead has four effects for three printed bulbs. Address 28 is the only exact "
        "count match, which still does not prove one-to-one socket identity."
    ),
    "devices": ["coil.driver-9", "coil.driver-16"] + [f"flasher.driver-{drive}-right" for drive in range(1, 9)],
})
_spatial_blockers.append({
    "id": "single-retained-recreation",
    "severity": "minor",
    "detail": (
        "Exactly one known-working recreation is admitted as canonical spatial evidence, so every "
        "coordinate remains a single-lineage measurement. Three additional local tables were "
        "inspected during maintainer review, but their credits establish one Javier to 32Assassin "
        "to VPW derivative chain rather than independent geometry. Placements are therefore "
        "`observed` rather than `validated`; promotion needs an independent table or a complete "
        "transcription of the printed location drawings on manual pages 25, 27 and 28."
    ),
})

spatial_report = {
    "format": "pinmame-spatial-blockers",
    "version": 1,
    "machine_id": "data-east.lethal-weapon-3.1992",
    "status": "partial",
    "coordinate_convention": (
        "Normalized against the retained table's own playfield bounds, "
        f"{RESOLUTION['playfield']['width']:.0f} x {RESOLUTION['playfield']['height']:.0f}, "
        "asserted rather than assumed. That extent happens to be the common WPC-era one, which is "
        "exactly why it is pinned: a machine whose bounds match the usual case is where an assumed "
        "divisor goes unnoticed. The resolver refuses to run if it ever sees different bounds."
    ),
    "placement_count": _placed,
    "source": {
        "table": TABLE,
        "extraction": EXTRACTION,
        "extraction_file_count": HASHES["extraction_file_count"],
        "extraction_manifest_sha256": HASHES["manifest_sha256"],
    },
    "coordinate_origins": {
        "measured_center": _placed - len(_computed),
        "computed_centroid": len(_computed),
        "note": (
            "Point-like table objects (Light, Trigger, Kicker, Bumper, Flasher, Primitive, "
            "HitTarget) carry "
            "their own center. Extended objects (Wall, Ramp, Rubber) are defined by drag points "
            "and have none, so those are the centroid of the object's drag points. A centroid is "
            "a derivation, not an observation, and is reported separately for that reason."
        ),
        "computed_devices": _computed,
    },
    "blockers": _spatial_blockers,
    "unresolved": RESOLUTION["unresolved"],
}

# --- Knowledge note ---------------------------------------------------------------------------
_used_switches = sum(1 for d in inputs if d["kind"] == "switch" and d["availability"] == "used")
_switch_places = sum(1 for k in PLACES if k.startswith("switch."))
_lamp_places = sum(1 for k in PLACES if k.startswith("lamp."))

knowledge_note = f"""# Lethal Weapon 3 (Data East, 1992)

Coverage: **partial - manual-verified I/O for the full 8x8 switch and lamp matrices with connector, wire-colour and drive-transistor wiring, all 22 printed coil-driver slots including the Left/Right relay pair, and nine source-reconciled mechanisms; the retained table provides normalized positions for all fitted playfield switches, 63 of 64 lamp addresses, fourteen playfield coil mechanisms, the modelled flasher effects, and 35 in-bounds GI emitters; held below author-ready because drive 3's left-side fitment, physical flasher sockets, the knocker location, spatial validation, switch polarity, and two source conflicts are not yet complete**

## Identity

Data East Lethal Weapon 3, 1992, `GEN_DEDMD32` - the 128x32 DMD generation, sound board DE2S. PinMAME roots the family at `lw3_208` with {len(drivers)} drivers, every one sharing `init_lw3` and therefore one `lw3GameData`, so all nine present identical playfield hardware. Three of the nine are later software rather than factory firmware - a 2013 voices mod and two 2020 community rulesets - which run on this same cabinet and so remain driver variants rather than new games. The voices mod is also the one set whose sound ROMs differ, swapping two of three for `_vm` variants; the other eight are uniform.

## The addendum corrects the manual about the display

The manual as printed says, on printed page 23, that the display is **32 x 64** dots. It is wrong. The factory addendum of 2 July 1992 states "The display is made up of 32 X 128 Dots not 32 X 64 Dots", and that is what pinned PinMAME independently declares through `de_128x32DMD` and `SNDBRD_DEDMD32`. Without the addendum the manual and the emulator would appear to disagree about the display and the manual would have been the wrong side to believe. It is recorded as its own source, not folded into the manual's, because it is a primary factory correction.

## The address model, and where it differs from WPC and Whitestar

Data East runs on the shared Williams System 11 core (`s11.c`); there is no `de.c`. `s11.c` installs no switch or lamp conversion of its own, so it inherits PinMAME's sequential defaults. **Both printed matrices are column-major**: address = (column - 1) x 8 + row. Column 1 of the switch matrix is the cabinet/coin column.

- **There is no GI channel at all.** General illumination is **public solenoid 11**, printed "GENERAL ILLUM. RELAY" (K-1) and commented `// GI output` in `s11.c`'s own `lw3_` typing block. The retained script agrees, naming its callback `SolRelayGI`. This is the second Data East machine in the project to confirm it, from a different manual.
- **Public solenoid 10 is the Left/Right relay**, printed "L/R COIL RELAY", which re-publishes outputs 1-8 at 25-32. The retained script binds all eight right-side addresses to Flash1R through Flash8R, so the pairing is confirmed on both sides. The superseded legacy record omits address 10 entirely.
- **64 lamps, and every one is populated** - the printed chart carries no "Not Used" cell.
- **Solenoids 33-44 are permanently zero on this machine.** That conclusion is scoped to `lw3GameData`: other Data East/System 11-derived configurations can populate part of the range through `S11_PRINTERLINE` or `S11_SNDOVERLAY`.

## Public switches 15 and 16 are cabinet flipper buttons despite the matrix labels

The manual contradicts itself. Its switch-matrix chart names addresses 15 and 16 Left EOS and Right EOS, but the adjacent Switch Part Numbers table lists `15* Left Flip. Cab` and `16* Right Flip. Cab.` with part number `180-5048-01`, and its legend says `* Indicates Cabinet Switches`. The parts table is the more specific physical identification and agrees with both PinMAME and the known-working script, so the canonical labels are Left/Right Flipper Cabinet Button while the printed EOS aliases remain documented.

`core.c:1740-1741` writes the flipper **button** state into the addresses `FLIP_SWNO(15,16)` names, and because this game declares no `FLIP_SOL` the end-of-stroke simulation at `core.c:1756-1775` never runs, so no end-of-stroke state is modelled.

**The mirroring is mode-dependent, and an unqualified rule here would be wrong.** Those two `core_setSw` calls sit inside `#ifdef PROC_SUPPORT` / `if (!coreGlobals.p_rocEn)` at `core.c:1733`, under the comment "Only handle flipper switches if we're not in a real game, otherwise they will get physically activated anyway". In an ordinary emulation build the addresses are rewritten from the flipper button bits on every `core_updateSw` pass, so a recreation cannot publish an end-of-stroke reading on them. In a P-ROC build driving real hardware the writes are skipped, because physical switches supply the state instead.

The retained known-working VPW 2.0 script does drive both addresses from the cabinet flipper key, at `script.vbs:928-929` on key down and `960-961` on key up. That agrees with what the emulator mirrors, so it is redundant in an ordinary build rather than authoritative - and it is what a P-ROC-mode consumer would need. An earlier revision of this note asserted flatly that a recreation "must not drive 15 or 16" while the working recreation does exactly that; the rule was both unqualified and contradicted by the evidence.

The superseded legacy record labels them "Left/Right Flipper Button", which describes what the emulator publishes rather than what the manual prints; both are recorded here.

## Lamps bind through `vpmMapLights`, not `Lampz`

The retained table uses the older idiom: each light's own `TimerInterval` field IS its ROM lamp index, and the lights sit in an `AllLamps` collection. A resolver written for the newer `Lampz.MassAssign` convention finds **zero** lamps here and reports a clean-looking result, which is how it was nearly missed. Four addresses - 7, 9, 18 and 27 - drive two bulbs at genuinely different playfield positions; lamp 18's pair sits at opposite sides of the table. Each is placed individually rather than averaged, because a centroid between two real inserts is a coordinate with no bulb in it.

## Evidence and its limits

The contributor-supplied manual has **no text layer whatsoever** - {TRANSCRIPTION['document']['page_count']} pages, {TRANSCRIPTION['document']['character_count']} characters - so every table here was read from 400 dpi renders and transcribed by hand. Four excerpts are committed beside this definition and digest-checked.

Spatial placement rests on one canonical VPW 2.0 extraction whose playfield is 952 x 2162. Fourteen playfield coils are placed at the retained Kicker, Bumper, Plunger, target-bank or slingshot mechanism they actuate, with the manual location drawing independently confirming the physical feature; these are mechanism locations, not invented winding centers. The knocker remains unplaced because the printed drawing has no readable 8L callout and the script's `KnockerPosition` is only a sound-placement helper. Driver 3 also remains unplaced and has unknown fitment: the drive table prints no coil while the same manual's location drawing clearly prints `3L` in the lower-right shooter-housing/cabinet extension without naming the device. The retained script also binds direct flashers 9 and 16, muxed flashers 25-32, and the solenoid-11 GI relay to exact Light objects; all in-bounds visual effects are retained individually, while the `GI_BG` object is excluded because its negative raw y coordinate makes it an off-playfield proxy.

Flasher Light objects are presentation effects rather than a physical socket survey. Their counts are lower than the manual bulb quantities at addresses 9, 16, 25-27, 29, 31 and 32; address 30 is the opposite mismatch, with four retained effects for three printed bulbs, and is preserved as `conflict.drive-6-flasher-effect-count`. Address 28 happens to match three-to-three, but count agreement alone still does not prove socket identity. Three additional local tables were inspected during maintainer review, but their credits establish a Javier to 32Assassin to VPW derivative chain, so they are not independent corroboration. Every coordinate therefore remains `observed` until an independent recreation or a complete original-machine location/socket survey agrees.

The drive-6 label is reconciled by the manual's own location drawing. Its drive table says `LEFT 3 BANK`, but printed page 28 places callout 6L beside the center drop-target bank, agreeing with the switch chart and the known-working script's `dtM` binding. The definition therefore calls the device Center Drop-Target Bank Reset while preserving `Left 3 Bank` as the manual wording; the relay-half name alone does not establish left-versus-center placement, as drive 7 appears in the same printed Left coil column but is named `RIGHT 3 BANK`.
"""


def build() -> dict:
	"""Return the canonical definition assembled from the embedded literals."""
	return definition


def _comparable(payload: bytes) -> bytes:
	"""``payload`` with CRLF folded to LF, so the comparison ignores line endings and nothing else.

	These artifacts are compared byte-for-byte rather than as canonical JSON because their bytes
	are their identity: the gate has to keep refusing a reformatted definition, reordered keys or
	changed indentation. What it must not refuse is a checkout Git rewrote on the way to disk, as
	the Windows default ``core.autocrlf=true`` does to every LF in the working tree.
	"""
	return payload.replace(b"\r\n", b"\n")


def _definition_bytes() -> bytes:
	with tempfile.TemporaryDirectory() as scratch:
		probe = Path(scratch) / "definition.json"
		write_json(probe, definition)
		return probe.read_bytes()


def _artifacts() -> tuple[tuple[Path, bytes], ...]:
	report_bytes = (json.dumps(spatial_report, indent="\t", sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
	definition_bytes = _definition_bytes()
	return (
		(DEFINITION_PATH, definition_bytes),
		(SEED_PATH, definition_bytes),
		(SPATIAL_REPORT_PATH, report_bytes),
		(KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
	)


def _write(root: Path) -> None:
	existing = root / "machines/author-ready/data-east/lethal-weapon-3-1992.json"
	if existing.is_file() and definition["coverage"]["status"] != "author_ready":
		raise RuntimeError(f"refusing to curate while an author-ready artifact exists (preserved): {existing}")
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	for path, payload in _artifacts()[2:]:
		target = root / path.relative_to(ROOT)
		target.parent.mkdir(parents=True, exist_ok=True)
		with target.open("wb") as stream:
			stream.write(payload)


def _check(root: Path) -> None:
	for path, expected in _artifacts():
		target = root / path.relative_to(ROOT)
		label = {"machines": "definition", "seeds": "seed", "reports": "spatial report"}.get(
			next((part for part in ("machines", "seeds", "reports") if part in target.parts), ""),
			"knowledge note")
		if not target.is_file():
			raise RuntimeError(f"Lethal Weapon 3 {label} is missing: {target}")
		if _comparable(target.read_bytes()) != _comparable(expected):
			raise RuntimeError(f"Lethal Weapon 3 {label} does not match the deterministic curator: {target}")
	report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
	expected_format = "pinmame-spatial-audit" if definition["coverage"]["status"] == "author_ready" else "pinmame-spatial-blockers"
	if report.get("format") != expected_format or report.get("machine_id") != definition["machine"]["id"]:
		raise RuntimeError(
			f"Lethal Weapon 3 spatial report must be {expected_format} for a "
			f"{definition['coverage']['status']} machine and must name this machine")
	placements = sum(
		len(device.get("spatial", {}).get("placements", []))
		for collection in ("inputs", "outputs")
		for device in definition[collection])
	if report.get("placement_count") != placements:
		raise RuntimeError(
			f"Lethal Weapon 3 spatial report claims {report.get('placement_count')} placements "
			f"but the definition carries {placements}")
	print("Lethal Weapon 3 definition, seed, spatial report, and knowledge note match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts.")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed.")
	parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository root to operate on.")
	args = parser.parse_args()
	root = args.repository_root.resolve()
	if args.regenerate:
		_write(root)
		print(f"Wrote {DEFINITION_PATH.relative_to(ROOT)} and {SEED_PATH.relative_to(ROOT)}")
		return
	_check(root)


if __name__ == "__main__":
	main()
