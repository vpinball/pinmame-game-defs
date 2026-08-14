"""Curate the physical Data East Batman (1991) machine definition.

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
import hashlib
import json
import os
import tempfile
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/data-east/batman-1991.json"
SEED_PATH = ROOT / "tools/seeds/data-east/batman-1991.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/batman-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/batman-1991.md"

TRANSCRIPTION = json.loads("{\n  \"auxiliary_solenoids\": {\n    \"17\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-3\",\n        \"wire\": \"BLU-ORN\"\n      },\n      \"name\": \"Left Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q8\"\n    },\n    \"18\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-4\",\n        \"wire\": \"BLU-RED\"\n      },\n      \"name\": \"Center Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q9\"\n    },\n    \"19\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-6\",\n        \"wire\": \"BLU-YEL\"\n      },\n      \"name\": \"Right Turbo Bumper\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q10\"\n    },\n    \"20\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-7\",\n        \"wire\": \"BLU-BRN\"\n      },\n      \"name\": \"Left Slingshot\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q11\"\n    },\n    \"21\": {\n      \"coil_type\": \"23-800\",\n      \"control\": {\n        \"connector\": \"CPU CN19-8\",\n        \"wire\": \"BLU-GRN\"\n      },\n      \"name\": \"Right Slingshot\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": \"RED\"\n      },\n      \"transistor\": \"Q12\"\n    },\n    \"22\": {\n      \"coil_type\": null,\n      \"control\": {\n        \"connector\": \"CPU CN19-9\",\n        \"wire\": null\n      },\n      \"name\": \"Motor Circuit\",\n      \"note\": \"Printed 'Motor Circuit (See Schematic)' with no coil type; the associated mechanism is not identified by this table.\",\n      \"power\": {\n        \"connector\": \"PS CN3-6\",\n        \"wire\": null\n      },\n      \"transistor\": \"Q13\"\n    }\n  },\n  \"coil_drivers\": {\n    \"direct\": {\n      \"10\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"Left/Right Coil Relay\",\n        \"note\": \"The mux relay itself. Confirms sxx.muxSol = 10 in btmnGameData (degames.c:501).\",\n        \"transistor\": \"Q29\",\n        \"wire\": \"BLK-RED\"\n      },\n      \"11\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"General Illumination Relay\",\n        \"note\": \"Printed 'GENERAL ILLUM. RELAY', relay K-1 at P.S. board CN7-1/3. Confirms s11.c:1207's own '// GI output' comment. General illumination on this platform is this solenoid, not a GI channel: coreGlobals.nGI is never assigned anywhere in s11.c and gi[] is never written.\",\n        \"transistor\": \"Q28\",\n        \"wire\": \"BRN-ORN\"\n      },\n      \"12\": {\n        \"bulbs\": \"(4) No. 89\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Flash lamps\",\n        \"placement\": \"3 insert, 1 playfield\",\n        \"resistor\": \"R-11\",\n        \"transistor\": \"Q27\",\n        \"wire\": \"BRN-YEL\"\n      },\n      \"13\": {\n        \"bulbs\": \"(4) No. 89\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Flash lamps\",\n        \"placement\": \"2 insert, 2 playfield\",\n        \"resistor\": \"R-11\",\n        \"transistor\": \"Q26\",\n        \"wire\": \"BRN-GRN\"\n      },\n      \"14\": {\n        \"bulbs\": \"(4) No. 89\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Flash lamps\",\n        \"placement\": \"4 insert\",\n        \"resistor\": \"R-12\",\n        \"transistor\": \"Q25\",\n        \"wire\": \"BRN-BLU\"\n      },\n      \"15\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"Optional Ticket Dispenser\",\n        \"note\": \"Printed 'OPTIONAL TICKET DISPENSER'; not fitted on a standard cabinet.\",\n        \"resistor\": \"R-13\",\n        \"transistor\": \"Q24\",\n        \"wire\": \"BRN-VIO\"\n      },\n      \"16\": {\n        \"connector\": \"CN-12\",\n        \"name\": \"Bat Bar Motor\",\n        \"note\": \"Drives a relay board which switches the 28 VAC Batbar Motor Assy 515-5256-00-11.\",\n        \"placement\": \"2 insert, 2 playfield\",\n        \"resistor\": \"R-14\",\n        \"transistor\": \"Q23\",\n        \"wire\": \"BRN-GRY\"\n      },\n      \"9\": {\n        \"bulbs\": \"(4) No. 89\",\n        \"connector\": \"CN-12\",\n        \"name\": \"Flash lamps\",\n        \"placement\": \"3 insert, 1 playfield\",\n        \"transistor\": \"Q30\",\n        \"wire\": \"BRN-BLK\"\n      }\n    },\n    \"muxed\": {\n      \"1\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Outhole\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"3 playfield, 1 insert\"\n        },\n        \"transistor\": \"Q46\",\n        \"wire\": \"GRY-BRN\"\n      },\n      \"2\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-840\",\n          \"name\": \"Trough Eject\"\n        },\n        \"right\": {\n          \"bulbs\": \"(3) No. 906 + No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"3 ramp, 1 playfield\"\n        },\n        \"transistor\": \"Q45\",\n        \"wire\": \"GRY-RED\"\n      },\n      \"3\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Left VUK\"\n        },\n        \"right\": {\n          \"bulbs\": \"(2) No. 89 + (2) No. 906\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"2 insert, 2 playfield\"\n        },\n        \"transistor\": \"Q44\",\n        \"wire\": \"GRY-ORN\"\n      },\n      \"4\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"22-600\",\n          \"name\": \"Ball Launch\",\n          \"note\": \"50 V, driven through Q5 TIP36C\"\n        },\n        \"right\": {\n          \"bulbs\": \"(2) No. 906 + (2) No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"2 insert, 2 playfield\"\n        },\n        \"transistor\": \"Q43\",\n        \"wire\": \"GRY-YEL\"\n      },\n      \"5\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"name\": null,\n          \"note\": \"Printed 'NO COIL AT THIS LOCATION (NOT USED)'\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"4 playfield\"\n        },\n        \"transistor\": \"Q42\",\n        \"wire\": \"GRY-GRN\"\n      },\n      \"6\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Right VUK\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"3 playfield, 1 insert\"\n        },\n        \"transistor\": \"Q41\",\n        \"wire\": \"GRY-BLU\"\n      },\n      \"7\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"name\": null,\n          \"note\": \"Printed 'NO COIL AT THIS LOCATION (NOT USED)'\"\n        },\n        \"right\": {\n          \"bulbs\": \"(4) No. 89\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"4 playfield\"\n        },\n        \"transistor\": \"Q40\",\n        \"wire\": \"GRY-VIO\"\n      },\n      \"8\": {\n        \"connector\": \"CN-11\",\n        \"left\": {\n          \"coil_type\": \"23-800\",\n          \"name\": \"Knocker\",\n          \"note\": \"50 V, driven through Q3 TIP36C\"\n        },\n        \"right\": {\n          \"bulbs\": \"(2) No. 89 + (2) No. 906\",\n          \"name\": \"Flash lamps\",\n          \"placement\": \"2 insert, 2 playfield\"\n        },\n        \"transistor\": \"Q39\",\n        \"wire\": \"GRY-BLK\"\n      }\n    },\n    \"printed_statement\": \"'Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed \\\"left\\\" and \\\"right\\\". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.' (printed page 28). This is the manual's own description of the mechanism pinned PinMAME implements at s11.c:564-574, where energising the mux solenoid re-routes outputs 1-8 to 25-32.\"\n  },\n  \"document\": {\n    \"bytes\": 3598735,\n    \"character_count\": 0,\n    \"extraction_status\": \"ocr_required\",\n    \"note\": \"Taken from the manual cache's own extraction record rather than restated in prose. An earlier draft interpolated the switch-matrix PDF page number where the page count belonged and published '28 pages' for a 70-page document.\",\n    \"page_count\": 70,\n    \"text_page_count\": 0\n  },\n  \"document_sha256\": \"dc1b5b533220bcf6efa2d54e5838792b666e81c5c1a3dfd7d17261c1727e01c9\",\n  \"flipper_solenoids\": {\n    \"left\": {\n      \"coil_type\": \"23-900\",\n      \"control\": {\n        \"connector\": \"CPU CN19-2\",\n        \"wire\": \"ORN-GRY\"\n      },\n      \"flipper_pcb\": {\n        \"connector\": \"CN1-9\",\n        \"wire\": \"BLU-GRY\"\n      },\n      \"power\": {\n        \"connector\": \"CN2-1,2\",\n        \"wire\": \"GRY-YEL\"\n      }\n    },\n    \"note\": \"Printed as its own unnumbered 'Flipper Solenoids' table, listing Left Flipper and Right Flipper only - no upper flipper of either hand. Consistent with btmnGameData declaring FLIP_SWNO(15,16) with no FLIP_SOL and no upper-flipper bit.\",\n    \"right\": {\n      \"coil_type\": \"23-900\",\n      \"control\": {\n        \"connector\": \"CPU CN19-1\",\n        \"wire\": \"ORN-VIO\"\n      },\n      \"flipper_pcb\": {\n        \"connector\": \"CN1-1\",\n        \"wire\": \"BLU-VIO\"\n      },\n      \"power\": {\n        \"connector\": \"CN1-1\",\n        \"wire\": \"BLK-WHT\"\n      }\n    }\n  },\n  \"format\": \"pinmame-manual-transcription\",\n  \"lamp_matrix\": {\n    \"1\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"1 Million\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"10\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bottom 4X\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"11\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bottom 6X\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"12\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bottom 8X\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"13\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bottom 10X\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"14\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Shoot Again\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"15\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Batman's Head\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"16\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Batman's Chest\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"17\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Left Toplane\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"18\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Center Toplane\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"19\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Toplane\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"2\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Super Bumps\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"20\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Playfield Moon\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"21\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Left Return\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"22\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Return\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"23\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Left Outlane\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"24\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN7-3\",\n        \"transistor\": \"Q69\",\n        \"wire\": \"YEL-ORN\"\n      },\n      \"name\": \"Right Outlane\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"25\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Backpanel Left\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"26\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Backpanel Center\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"27\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Backpanel Right\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"28\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Backpanel 500K\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"29\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Backpanel XBall\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"3\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Lite Extra Ball\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"30\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Double Score\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"31\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"Under Ramp XBall\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"32\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN7-4\",\n        \"transistor\": \"Q68\",\n        \"wire\": \"YEL-BLK\"\n      },\n      \"name\": \"3 Million\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"33\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Left 3 Bank Top\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"34\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Left 3 Bank Middle\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"35\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Left 3 Bank Bottom\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"36\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Joker Left Eye\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"37\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Joker Right Eye\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"38\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Joker 2 Million\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"39\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Left VUK XBall\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"4\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Fast Money\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"40\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN7-6\",\n        \"transistor\": \"Q67\",\n        \"wire\": \"YEL-GRN\"\n      },\n      \"name\": \"Left 3 Bank Done\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"41\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Right 3 Bank Top\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"42\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Right 3 Bank Middle\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"43\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Right 3 Bank Bottom\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"44\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Left Bumper\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"45\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Center Bumper\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"46\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Right Bumper\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"47\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Spot Bat Monitor\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"48\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN7-7\",\n        \"transistor\": \"Q66\",\n        \"wire\": \"YEL-BLU\"\n      },\n      \"name\": \"Right 3 Bank Done\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"49\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Ramp Diverter\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"5\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Instant 2 Ball\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"50\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Insert-Moon\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"51\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Insert-5 Million\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"52\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Insert-15 Million\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"53\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Insert-10 Million\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"54\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Cab.-Start Button\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"55\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Museum Bat Symbol\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"56\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN7-8\",\n        \"transistor\": \"Q65\",\n        \"wire\": \"YEL-VIO\"\n      },\n      \"name\": \"Jackpot Lit\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"57\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (B)\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    },\n    \"58\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (A)\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN6-2\",\n        \"transistor\": \"Q73\",\n        \"wire\": \"RED-BLK\"\n      }\n    },\n    \"59\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (T)\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN6-3\",\n        \"transistor\": \"Q74\",\n        \"wire\": \"RED-ORN\"\n      }\n    },\n    \"6\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Million Plus\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"60\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (M)\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN6-5\",\n        \"transistor\": \"Q75\",\n        \"wire\": \"RED-YEL\"\n      }\n    },\n    \"61\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (A)\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN6-6\",\n        \"transistor\": \"Q76\",\n        \"wire\": \"RED-GRN\"\n      }\n    },\n    \"62\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"BATMAN (N)\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN6-7\",\n        \"transistor\": \"Q77\",\n        \"wire\": \"RED-BLU\"\n      }\n    },\n    \"63\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Lockball #1\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"64\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN7-9\",\n        \"transistor\": \"Q64\",\n        \"wire\": \"YEL-GRY\"\n      },\n      \"name\": \"Lockball #2\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"7\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Max X Value\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN6-8\",\n        \"transistor\": \"Q78\",\n        \"wire\": \"RED-VIO\"\n      }\n    },\n    \"8\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN7-1\",\n        \"transistor\": \"Q71\",\n        \"wire\": \"YEL-BRN\"\n      },\n      \"name\": \"Spot Fast Money\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN6-9\",\n        \"transistor\": \"Q79\",\n        \"wire\": \"RED-GRY\"\n      }\n    },\n    \"9\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN7-2\",\n        \"transistor\": \"Q70\",\n        \"wire\": \"YEL-RED\"\n      },\n      \"name\": \"Bottom 2X\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN6-1\",\n        \"transistor\": \"Q72\",\n        \"wire\": \"RED-BRN\"\n      }\n    }\n  },\n  \"machine_id\": \"data-east.batman.1991\",\n  \"note\": \"Hand-transcribed from 400 dpi renders. This manual has no text layer at all (70 pages, 0 characters, extraction_status ocr_required), so nothing here comes from pdftotext. Both matrices are printed column-major: address = (column-1)*8 + row, which matches pinned PinMAME's core_m2swSeq(col,row) = col*8+row-7 rather than any col*10+row WPC convention.\",\n  \"pages\": {\n    \"lamp_locations\": {\n      \"pdf\": 31,\n      \"printed\": 27\n    },\n    \"lamp_matrix\": {\n      \"pdf\": 30,\n      \"printed\": 26\n    },\n    \"solenoids\": {\n      \"pdf\": 32,\n      \"printed\": 28\n    },\n    \"special_coil_wiring\": {\n      \"pdf\": 33,\n      \"printed\": 29\n    },\n    \"switch_locations\": {\n      \"pdf\": 29,\n      \"printed\": 25\n    },\n    \"switch_matrix\": {\n      \"pdf\": 28,\n      \"printed\": 24\n    }\n  },\n  \"source_agreements\": {\n    \"confirmed\": [\n      \"core_m2swSeq(col,row) = col*8+row-7 -> both printed matrices number column-major, address = (column-1)*8 + row.\",\n      \"CORE_FIRSTSSSOL = 17 with six switched solenoids -> printed 'CPU Controlled Auxiliary Solenoids' is exactly 17-22.\",\n      \"nLamps = 64 -> printed lamp matrix is 64 cells with no 'Not Used'.\",\n      \"sxx.muxSol = 10 -> drive 10 is printed 'Left/Right Coil Relay'.\",\n      \"s11.c:1207 types solenoid 11 with the comment '// GI output' -> drive 11 is printed 'General Illumination Relay'.\",\n      \"s11.c:1208 types solenoids 12-14 as No. 89 flashers -> drives 12, 13 and 14 each drive (4) No. 89 flash lamps.\",\n      \"s11.c:1209 types solenoids 25-32 as No. 89 flashers -> the relay's right set is flash lamps on every one of drives 1-8.\",\n      \"No FLIP_SOL and no upper-flipper bit -> the printed 'Flipper Solenoids' table lists Left and Right only.\"\n    ],\n    \"divergences\": [\n      {\n        \"detail\": \"s11.c:1206 types solenoid 9 as CORE_MODOUT_BULB_44_6_3V_AC_REV - a reverse-polarity 6.3 V AC No. 44 bulb - but the Special Coil Wiring Diagram (printed page 29) shows drive 09 feeding four No. 89 bulbs at +32 V through Q30/BRN-BLK, the same arrangement as drives 12-14. Unresolved: this is an output brightness-model divergence, not an address one, but the two sources disagree about bulb type, voltage and polarity.\",\n        \"id\": \"solenoid-9-bulb-type\"\n      },\n      {\n        \"detail\": \"s11.h's DE_COMPORTS names dedicated column-1 position 2 'Ball Tilt'; the printed Switch Matrix Chart prints position 2 'Not Used'.\",\n        \"id\": \"matrix-position-2-naming\"\n      },\n      {\n        \"detail\": \"The printed matrix names 15 'Left EOS' and 16 'Right EOS'. btmnGameData declares FLIP_SWNO(15,16), and core.c:1740-1741 - under the comment 'set switches in matrix for non-fliptronic games' - writes the flipper BUTTON state into those two addresses via core_setSw. Batman declares no FLIP_SOL, so no FLIP_EOS bit is ever set and the EOS simulation block at core.c:1756-1775 never runs for this game. PinMAME therefore owns public 15 and 16 and publishes button state on them; a recreation must not drive these two addresses, because core_updateSw overwrites them every frame.\",\n        \"id\": \"switch-15-16-eos-vs-button\"\n      }\n    ],\n    \"note\": \"Each derived from pinned PinMAME 4ec52ff0ac13 BEFORE this manual was read, then confirmed against it.\"\n  },\n  \"switch_matrix\": {\n    \"1\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Plumb Tilt\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"10\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Outhole\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"11\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #1 Left\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"12\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #2 Center\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"13\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Trough #3 Right\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"14\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Shooter Lane\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"15\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Left EOS\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"16\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Right EOS\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"17\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left Top Lane\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"18\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Center Top Lane\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"19\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Right Top Lane\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"2\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"20\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"21\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left Return\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"22\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Right Return\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"23\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Left Outlane\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"24\": {\n      \"column\": 3,\n      \"column_drive\": {\n        \"connector\": \"CN8-3\",\n        \"transistor\": \"Q53\",\n        \"wire\": \"GRN-ORN\"\n      },\n      \"name\": \"Right Outlane\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"25\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"26\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"27\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"28\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Ramp Entrance\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"29\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Ramp Exit\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"3\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Credit Button\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"30\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"31\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"32\": {\n      \"column\": 4,\n      \"column_drive\": {\n        \"connector\": \"CN8-4\",\n        \"transistor\": \"Q52\",\n        \"wire\": \"GRN-YEL\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"33\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left 3 Bank Top\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"34\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left 3 Bank Middle\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"35\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left 3 Bank Bottom\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"36\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Joker Left Eye\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"37\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Joker Right Eye\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"38\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Joker Mouth\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"39\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Left VUK\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"4\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Right Coin\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"40\": {\n      \"column\": 5,\n      \"column_drive\": {\n        \"connector\": \"CN8-5\",\n        \"transistor\": \"Q51\",\n        \"wire\": \"GRN-BLK\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"41\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right 3 Bank Top\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"42\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right 3 Bank Middle\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"43\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right 3 Bank Bottom\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"44\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"45\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"46\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"47\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Left Slingshot\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"48\": {\n      \"column\": 6,\n      \"column_drive\": {\n        \"connector\": \"CN8-7\",\n        \"transistor\": \"Q50\",\n        \"wire\": \"GRN-BLU\"\n      },\n      \"name\": \"Right Slingshot\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"49\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Bat Bar Standup\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"5\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Center Coin\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"50\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Museum Motor Up\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"51\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Museum Motor Down\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"52\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Right VUK Top\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"53\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Right VUK Bottom\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"54\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Left Turbo Bumper\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"55\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Center Turbo Bumper\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"56\": {\n      \"column\": 7,\n      \"column_drive\": {\n        \"connector\": \"CN8-8\",\n        \"transistor\": \"Q49\",\n        \"wire\": \"GRN-VIO\"\n      },\n      \"name\": \"Right Turbo Bumper\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"57\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    },\n    \"58\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 2,\n      \"row_return\": {\n        \"connector\": \"CN10-8\",\n        \"transistor\": null,\n        \"wire\": \"WHT-RED\"\n      }\n    },\n    \"59\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 3,\n      \"row_return\": {\n        \"connector\": \"CN10-7\",\n        \"transistor\": null,\n        \"wire\": \"WHT-ORN\"\n      }\n    },\n    \"6\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Left Coin\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"60\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 4,\n      \"row_return\": {\n        \"connector\": \"CN10-6\",\n        \"transistor\": null,\n        \"wire\": \"WHT-YEL\"\n      }\n    },\n    \"61\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 5,\n      \"row_return\": {\n        \"connector\": \"CN10-5\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRN\"\n      }\n    },\n    \"62\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 6,\n      \"row_return\": {\n        \"connector\": \"CN10-3\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BLU\"\n      }\n    },\n    \"63\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"64\": {\n      \"column\": 8,\n      \"column_drive\": {\n        \"connector\": \"CN8-9\",\n        \"transistor\": \"Q48\",\n        \"wire\": \"GRN-GRY\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"7\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Slam Tilt\",\n      \"row\": 7,\n      \"row_return\": {\n        \"connector\": \"CN10-2\",\n        \"transistor\": null,\n        \"wire\": \"WHT-VIO\"\n      }\n    },\n    \"8\": {\n      \"column\": 1,\n      \"column_drive\": {\n        \"connector\": \"CN8-1\",\n        \"transistor\": \"Q55\",\n        \"wire\": \"GRN-BRN\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 8,\n      \"row_return\": {\n        \"connector\": \"CN10-1\",\n        \"transistor\": null,\n        \"wire\": \"WHT-GRY\"\n      }\n    },\n    \"9\": {\n      \"column\": 2,\n      \"column_drive\": {\n        \"connector\": \"CN8-2\",\n        \"transistor\": \"Q54\",\n        \"wire\": \"GRN-RED\"\n      },\n      \"name\": \"Not Used\",\n      \"row\": 1,\n      \"row_return\": {\n        \"connector\": \"CN10-9\",\n        \"transistor\": null,\n        \"wire\": \"WHT-BRN\"\n      }\n    }\n  },\n  \"version\": 1\n}")
RESOLUTION = json.loads("{\n  \"binding_routes\": {\n    \"14\": \"name-convention\",\n    \"17\": \"script-handler\",\n    \"18\": \"script-handler\",\n    \"19\": \"script-handler\",\n    \"21\": \"script-handler\",\n    \"22\": \"script-handler\",\n    \"23\": \"script-handler\",\n    \"24\": \"script-handler\",\n    \"28\": \"script-handler\",\n    \"29\": \"script-handler\",\n    \"33\": \"script-handler\",\n    \"34\": \"script-handler\",\n    \"35\": \"script-handler\",\n    \"36\": \"script-handler\",\n    \"37\": \"script-handler\",\n    \"38\": \"script-handler\",\n    \"39\": \"script-handler\",\n    \"41\": \"script-handler\",\n    \"42\": \"script-handler\",\n    \"43\": \"script-handler\",\n    \"47\": \"script-handler\",\n    \"48\": \"script-handler\",\n    \"49\": \"script-handler\",\n    \"52\": \"script-handler\",\n    \"54\": \"script-handler\",\n    \"55\": \"script-handler\",\n    \"56\": \"script-handler\"\n  },\n  \"counts\": {\n    \"lamp_bindings_in_script\": 71,\n    \"lamps_resolved\": 54,\n    \"switches_resolved\": 27\n  },\n  \"format\": \"batman-spatial-resolution\",\n  \"playfield\": {\n    \"height\": 1974.0,\n    \"note\": \"y is normalized by 1974, not the 2162 most WPC-era tables use\",\n    \"width\": 952.0\n  },\n  \"resolved\": {\n    \"lamp.1\": {\n      \"address\": 1,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l1\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 400.3871,\n        \"y\": 970.1954\n      },\n      \"x\": 0.420575,\n      \"y\": 0.491487\n    },\n    \"lamp.10\": {\n      \"address\": 10,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l10\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 437.80377,\n        \"y\": 1556.7751\n      },\n      \"x\": 0.459878,\n      \"y\": 0.78864\n    },\n    \"lamp.11\": {\n      \"address\": 11,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l11\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 526.473,\n        \"y\": 1557.1265\n      },\n      \"x\": 0.553018,\n      \"y\": 0.788818\n    },\n    \"lamp.12\": {\n      \"address\": 12,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l12\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 393.29346,\n        \"y\": 1611.3817\n      },\n      \"x\": 0.413123,\n      \"y\": 0.816303\n    },\n    \"lamp.13\": {\n      \"address\": 13,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l13\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 480.1192,\n        \"y\": 1611.2063\n      },\n      \"x\": 0.504327,\n      \"y\": 0.816214\n    },\n    \"lamp.14\": {\n      \"address\": 14,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l14\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 436.39917,\n        \"y\": 1665.8997\n      },\n      \"x\": 0.458402,\n      \"y\": 0.843921\n    },\n    \"lamp.15\": {\n      \"address\": 15,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l15\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 431.1589,\n        \"y\": 1211.8163\n      },\n      \"x\": 0.452898,\n      \"y\": 0.613889\n    },\n    \"lamp.16\": {\n      \"address\": 16,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l16\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 426.9843,\n        \"y\": 1300.9926\n      },\n      \"x\": 0.448513,\n      \"y\": 0.659064\n    },\n    \"lamp.17\": {\n      \"address\": 17,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"lamp\",\n      \"object\": \"L17f\",\n      \"object_type\": \"Flasher\",\n      \"raw\": {\n        \"x\": 372.967975,\n        \"y\": 91.705535\n      },\n      \"x\": 0.391773,\n      \"y\": 0.046457\n    },\n    \"lamp.18\": {\n      \"address\": 18,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"lamp\",\n      \"object\": \"L18f\",\n      \"object_type\": \"Flasher\",\n      \"raw\": {\n        \"x\": 474.3555,\n        \"y\": 91.143233\n      },\n      \"x\": 0.498273,\n      \"y\": 0.046172\n    },\n    \"lamp.19\": {\n      \"address\": 19,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"lamp\",\n      \"object\": \"L19f\",\n      \"object_type\": \"Flasher\",\n      \"raw\": {\n        \"x\": 573.06095,\n        \"y\": 93.9547725\n      },\n      \"x\": 0.601955,\n      \"y\": 0.047596\n    },\n    \"lamp.2\": {\n      \"address\": 2,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l2\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 460.60226,\n        \"y\": 964.73926\n      },\n      \"x\": 0.483826,\n      \"y\": 0.488723\n    },\n    \"lamp.20\": {\n      \"address\": 20,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l20\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 313.79987,\n        \"y\": 1284.219\n      },\n      \"x\": 0.329622,\n      \"y\": 0.650567\n    },\n    \"lamp.21\": {\n      \"address\": 21,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l21\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 128.95695,\n        \"y\": 1277.5276\n      },\n      \"x\": 0.135459,\n      \"y\": 0.647177\n    },\n    \"lamp.22\": {\n      \"address\": 22,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l22\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 745.89264,\n        \"y\": 1277.012\n      },\n      \"x\": 0.783501,\n      \"y\": 0.646916\n    },\n    \"lamp.23\": {\n      \"address\": 23,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"lamp\",\n      \"object\": \"l23f\",\n      \"object_type\": \"Flasher\",\n      \"raw\": {\n        \"x\": 35.200649,\n        \"y\": 1300.74445\n      },\n      \"x\": 0.036975,\n      \"y\": 0.658938\n    },\n    \"lamp.24\": {\n      \"address\": 24,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l24\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 815.7525,\n        \"y\": 1297.1001\n      },\n      \"x\": 0.856883,\n      \"y\": 0.657092\n    },\n    \"lamp.3\": {\n      \"address\": 3,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l3\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 405.6485,\n        \"y\": 1033.9186\n      },\n      \"x\": 0.426101,\n      \"y\": 0.523768\n    },\n    \"lamp.30\": {\n      \"address\": 30,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l30\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 372.05447,\n        \"y\": 753.7117\n      },\n      \"x\": 0.390814,\n      \"y\": 0.38182\n    },\n    \"lamp.31\": {\n      \"address\": 31,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l31\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 435.97302,\n        \"y\": 745.45654\n      },\n      \"x\": 0.457955,\n      \"y\": 0.377638\n    },\n    \"lamp.32\": {\n      \"address\": 32,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l32\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 410.1952,\n        \"y\": 858.403\n      },\n      \"x\": 0.430877,\n      \"y\": 0.434855\n    },\n    \"lamp.33\": {\n      \"address\": 33,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l33\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 210.97243,\n        \"y\": 942.27704\n      },\n      \"x\": 0.22161,\n      \"y\": 0.477344\n    },\n    \"lamp.34\": {\n      \"address\": 34,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l34\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 201.77013,\n        \"y\": 991.60114\n      },\n      \"x\": 0.211943,\n      \"y\": 0.502331\n    },\n    \"lamp.35\": {\n      \"address\": 35,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l35\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 200.78085,\n        \"y\": 1042.2238\n      },\n      \"x\": 0.210904,\n      \"y\": 0.527976\n    },\n    \"lamp.36\": {\n      \"address\": 36,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l36b\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 47.256046,\n        \"y\": 44.937008\n      },\n      \"x\": 0.049639,\n      \"y\": 0.022764\n    },\n    \"lamp.37\": {\n      \"address\": 37,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l37b\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 129.91951,\n        \"y\": 44.55175\n      },\n      \"x\": 0.13647,\n      \"y\": 0.022569\n    },\n    \"lamp.38\": {\n      \"address\": 38,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"L38\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 203.46892,\n        \"y\": 698.958\n      },\n      \"x\": 0.213728,\n      \"y\": 0.354082\n    },\n    \"lamp.39\": {\n      \"address\": 39,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l39\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 126.80398,\n        \"y\": 734.96173\n      },\n      \"x\": 0.133197,\n      \"y\": 0.372321\n    },\n    \"lamp.4\": {\n      \"address\": 4,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l4\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 467.43375,\n        \"y\": 1026.3248\n      },\n      \"x\": 0.491002,\n      \"y\": 0.519921\n    },\n    \"lamp.40\": {\n      \"address\": 40,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l40\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 306.4829,\n        \"y\": 1004.8196\n      },\n      \"x\": 0.321936,\n      \"y\": 0.509027\n    },\n    \"lamp.41\": {\n      \"address\": 41,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l41\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 669.9933,\n        \"y\": 965.8536\n      },\n      \"x\": 0.703774,\n      \"y\": 0.489288\n    },\n    \"lamp.42\": {\n      \"address\": 42,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l42\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 683.77216,\n        \"y\": 1010.4003\n      },\n      \"x\": 0.718248,\n      \"y\": 0.511854\n    },\n    \"lamp.43\": {\n      \"address\": 43,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l43\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 696.4429,\n        \"y\": 1062.0889\n      },\n      \"x\": 0.731558,\n      \"y\": 0.538039\n    },\n    \"lamp.44\": {\n      \"address\": 44,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"BumperL_Flasher\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 297.27396,\n        \"y\": 401.6336\n      },\n      \"x\": 0.312263,\n      \"y\": 0.203462\n    },\n    \"lamp.45\": {\n      \"address\": 45,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"BumperB_Flasher\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 379.52505,\n        \"y\": 559.4533\n      },\n      \"x\": 0.398661,\n      \"y\": 0.283411\n    },\n    \"lamp.46\": {\n      \"address\": 46,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"BumperR_Flasher\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 509.88947,\n        \"y\": 421.09796\n      },\n      \"x\": 0.535598,\n      \"y\": 0.213322\n    },\n    \"lamp.47\": {\n      \"address\": 47,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l47\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 156.35382,\n        \"y\": 826.1034\n      },\n      \"x\": 0.164237,\n      \"y\": 0.418492\n    },\n    \"lamp.48\": {\n      \"address\": 48,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l48\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 581.407,\n        \"y\": 1032.2001\n      },\n      \"x\": 0.610722,\n      \"y\": 0.522898\n    },\n    \"lamp.49\": {\n      \"address\": 49,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l49\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 843.9655,\n        \"y\": 1065.6952\n      },\n      \"x\": 0.886518,\n      \"y\": 0.539866\n    },\n    \"lamp.5\": {\n      \"address\": 5,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l5\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 385.96655,\n        \"y\": 1100.1752\n      },\n      \"x\": 0.405427,\n      \"y\": 0.557333\n    },\n    \"lamp.55\": {\n      \"address\": 55,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"lamp\",\n      \"object\": \"L55\",\n      \"object_type\": \"Flasher\",\n      \"raw\": {\n        \"x\": 710.295625,\n        \"y\": 302.49123499999996\n      },\n      \"x\": 0.746109,\n      \"y\": 0.153238\n    },\n    \"lamp.56\": {\n      \"address\": 56,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l56\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 601.55035,\n        \"y\": 745.8716\n      },\n      \"x\": 0.631881,\n      \"y\": 0.377848\n    },\n    \"lamp.57\": {\n      \"address\": 57,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l57\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 619.0875,\n        \"y\": 540.8213\n      },\n      \"x\": 0.650302,\n      \"y\": 0.273972\n    },\n    \"lamp.58\": {\n      \"address\": 58,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l58\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 669.63043,\n        \"y\": 558.8583\n      },\n      \"x\": 0.703393,\n      \"y\": 0.28311\n    },\n    \"lamp.59\": {\n      \"address\": 59,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l59\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 716.08746,\n        \"y\": 577.77344\n      },\n      \"x\": 0.752193,\n      \"y\": 0.292692\n    },\n    \"lamp.6\": {\n      \"address\": 6,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l6\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 445.0127,\n        \"y\": 1093.16\n      },\n      \"x\": 0.46745,\n      \"y\": 0.553779\n    },\n    \"lamp.60\": {\n      \"address\": 60,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l60\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 595.623,\n        \"y\": 600.8848\n      },\n      \"x\": 0.625654,\n      \"y\": 0.3044\n    },\n    \"lamp.61\": {\n      \"address\": 61,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l61\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 650.60236,\n        \"y\": 621.98315\n      },\n      \"x\": 0.683406,\n      \"y\": 0.315088\n    },\n    \"lamp.62\": {\n      \"address\": 62,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l62\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 705.72644,\n        \"y\": 640.89233\n      },\n      \"x\": 0.741309,\n      \"y\": 0.324667\n    },\n    \"lamp.63\": {\n      \"address\": 63,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l63\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 592.569,\n        \"y\": 671.1641\n      },\n      \"x\": 0.622446,\n      \"y\": 0.340002\n    },\n    \"lamp.64\": {\n      \"address\": 64,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l64\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 656.56836,\n        \"y\": 696.761\n      },\n      \"x\": 0.689673,\n      \"y\": 0.352969\n    },\n    \"lamp.7\": {\n      \"address\": 7,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l7\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 504.6435,\n        \"y\": 1085.56\n      },\n      \"x\": 0.530088,\n      \"y\": 0.549929\n    },\n    \"lamp.8\": {\n      \"address\": 8,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l8\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 174.74425,\n        \"y\": 572.63965\n      },\n      \"x\": 0.183555,\n      \"y\": 0.290091\n    },\n    \"lamp.9\": {\n      \"address\": 9,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"lamp\",\n      \"object\": \"l9\",\n      \"object_type\": \"Light\",\n      \"raw\": {\n        \"x\": 350.06747,\n        \"y\": 1557.7559\n      },\n      \"x\": 0.367718,\n      \"y\": 0.789137\n    },\n    \"switch.14\": {\n      \"address\": 14,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw14\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 901.0,\n        \"y\": 1711.0\n      },\n      \"x\": 0.946429,\n      \"y\": 0.866768\n    },\n    \"switch.17\": {\n      \"address\": 17,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw17\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 358.96082,\n        \"y\": 171.15367\n      },\n      \"x\": 0.37706,\n      \"y\": 0.086704\n    },\n    \"switch.18\": {\n      \"address\": 18,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw18\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 456.42035,\n        \"y\": 170.07762\n      },\n      \"x\": 0.479433,\n      \"y\": 0.086159\n    },\n    \"switch.19\": {\n      \"address\": 19,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw19\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 560.00244,\n        \"y\": 170.30911\n      },\n      \"x\": 0.588238,\n      \"y\": 0.086276\n    },\n    \"switch.21\": {\n      \"address\": 21,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw21\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 126.86865,\n        \"y\": 1400.2991\n      },\n      \"x\": 0.133265,\n      \"y\": 0.709371\n    },\n    \"switch.22\": {\n      \"address\": 22,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw22\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 743.85565,\n        \"y\": 1402.6525\n      },\n      \"x\": 0.781361,\n      \"y\": 0.710564\n    },\n    \"switch.23\": {\n      \"address\": 23,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw23\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 57.63405,\n        \"y\": 1456.9711\n      },\n      \"x\": 0.06054,\n      \"y\": 0.738081\n    },\n    \"switch.24\": {\n      \"address\": 24,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw24\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 811.33356,\n        \"y\": 1468.5299\n      },\n      \"x\": 0.852241,\n      \"y\": 0.743936\n    },\n    \"switch.28\": {\n      \"address\": 28,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw28\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 350.13104,\n        \"y\": 449.6984\n      },\n      \"x\": 0.367785,\n      \"y\": 0.227811\n    },\n    \"switch.29\": {\n      \"address\": 29,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw29\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 894.5659,\n        \"y\": 154.32274\n      },\n      \"x\": 0.93967,\n      \"y\": 0.078178\n    },\n    \"switch.33\": {\n      \"address\": 33,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw33\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 113.53865625,\n        \"y\": 924.2243149999999\n      },\n      \"x\": 0.119263,\n      \"y\": 0.468199\n    },\n    \"switch.34\": {\n      \"address\": 34,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw34\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 105.8062405,\n        \"y\": 978.012015\n      },\n      \"x\": 0.111141,\n      \"y\": 0.495447\n    },\n    \"switch.35\": {\n      \"address\": 35,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw35\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 98.34511,\n        \"y\": 1032.010275\n      },\n      \"x\": 0.103304,\n      \"y\": 0.522802\n    },\n    \"switch.36\": {\n      \"address\": 36,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw36\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 53.556656,\n        \"y\": 186.3145\n      },\n      \"x\": 0.056257,\n      \"y\": 0.094384\n    },\n    \"switch.37\": {\n      \"address\": 37,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw37\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 138.18794,\n        \"y\": 171.74057\n      },\n      \"x\": 0.145155,\n      \"y\": 0.087001\n    },\n    \"switch.38\": {\n      \"address\": 38,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"sw38\",\n      \"object_type\": \"Trigger\",\n      \"raw\": {\n        \"x\": 114.78728,\n        \"y\": 289.0886\n      },\n      \"x\": 0.120575,\n      \"y\": 0.146448\n    },\n    \"switch.39\": {\n      \"address\": 39,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw39\",\n      \"object_type\": \"Kicker\",\n      \"raw\": {\n        \"x\": 88.0491,\n        \"y\": 607.50604\n      },\n      \"x\": 0.092489,\n      \"y\": 0.307754\n    },\n    \"switch.41\": {\n      \"address\": 41,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw41\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 767.6781375,\n        \"y\": 935.4083975\n      },\n      \"x\": 0.806385,\n      \"y\": 0.473864\n    },\n    \"switch.42\": {\n      \"address\": 42,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw42\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 774.3657049999999,\n        \"y\": 985.13391\n      },\n      \"x\": 0.813409,\n      \"y\": 0.499055\n    },\n    \"switch.43\": {\n      \"address\": 43,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw43\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 781.074925,\n        \"y\": 1036.21463\n      },\n      \"x\": 0.820457,\n      \"y\": 0.524931\n    },\n    \"switch.47\": {\n      \"address\": 47,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"LeftSlingShot\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 222.67235,\n        \"y\": 1378.6889\n      },\n      \"x\": 0.2339,\n      \"y\": 0.698424\n    },\n    \"switch.48\": {\n      \"address\": 48,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"RightSlingShot\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 653.8071625,\n        \"y\": 1383.1350499999999\n      },\n      \"x\": 0.686772,\n      \"y\": 0.700676\n    },\n    \"switch.49\": {\n      \"address\": 49,\n      \"coordinate_origin\": \"computed-centroid\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw49\",\n      \"object_type\": \"Wall\",\n      \"raw\": {\n        \"x\": 718.4596349999999,\n        \"y\": 418.72263250000003\n      },\n      \"x\": 0.754684,\n      \"y\": 0.212119\n    },\n    \"switch.52\": {\n      \"address\": 52,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Sw52\",\n      \"object_type\": \"Kicker\",\n      \"raw\": {\n        \"x\": 777.9352,\n        \"y\": 237.70027\n      },\n      \"x\": 0.817159,\n      \"y\": 0.120416\n    },\n    \"switch.54\": {\n      \"address\": 54,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper1B\",\n      \"object_type\": \"Bumper\",\n      \"raw\": {\n        \"x\": 297.24896,\n        \"y\": 364.46854\n      },\n      \"x\": 0.312236,\n      \"y\": 0.184635\n    },\n    \"switch.55\": {\n      \"address\": 55,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper3B\",\n      \"object_type\": \"Bumper\",\n      \"raw\": {\n        \"x\": 509.81693,\n        \"y\": 394.6638\n      },\n      \"x\": 0.535522,\n      \"y\": 0.199931\n    },\n    \"switch.56\": {\n      \"address\": 56,\n      \"coordinate_origin\": \"measured-center\",\n      \"kind\": \"switch\",\n      \"object\": \"Bumper2B\",\n      \"object_type\": \"Bumper\",\n      \"raw\": {\n        \"x\": 376.59708,\n        \"y\": 559.41705\n      },\n      \"x\": 0.395585,\n      \"y\": 0.283393\n    }\n  },\n  \"source\": \"vpx-table.batman-vpw-1-1\",\n  \"unresolved\": {\n    \"lamps\": [\n      {\n        \"address\": 25,\n        \"reason\": \"bound to FlasherLight25a, absent from the extraction\"\n      },\n      {\n        \"address\": 26,\n        \"reason\": \"bound to FlasherLight26a, absent from the extraction\"\n      },\n      {\n        \"address\": 27,\n        \"reason\": \"bound to FlasherLight27a, absent from the extraction\"\n      },\n      {\n        \"address\": 28,\n        \"reason\": \"bound to FlasherLight28a, absent from the extraction\"\n      },\n      {\n        \"address\": 29,\n        \"reason\": \"bound to FlasherLight29a, absent from the extraction\"\n      },\n      {\n        \"address\": 50,\n        \"reason\": \"no Lampz.MassAssign binding\"\n      },\n      {\n        \"address\": 51,\n        \"reason\": \"no Lampz.MassAssign binding\"\n      },\n      {\n        \"address\": 52,\n        \"reason\": \"no Lampz.MassAssign binding\"\n      },\n      {\n        \"address\": 53,\n        \"reason\": \"no Lampz.MassAssign binding\"\n      },\n      {\n        \"address\": 54,\n        \"reason\": \"no Lampz.MassAssign binding\"\n      }\n    ],\n    \"switches\": [\n      {\n        \"address\": 1,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 2,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 3,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 4,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 5,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 6,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 7,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 8,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 9,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 10,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 11,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 12,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 13,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 15,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 16,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 20,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 25,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 26,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 27,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 30,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 31,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 32,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 40,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 44,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 45,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 46,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 50,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 51,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 53,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 57,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 58,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 59,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 60,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 61,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 62,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 63,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      },\n      {\n        \"address\": 64,\n        \"reason\": \"no script handler and no Sw<n> object\"\n      }\n    ]\n  },\n  \"version\": 1\n}")
ROM_SETS = json.loads("{\n  \"btmn_101\": {\n    \"macro\": \"DE_ROMSTART88\",\n    \"roms\": [\n      \"batcpub5.101\",\n      \"batcpuc5.101\",\n      \"batdsp.102\",\n      \"batman.u7\",\n      \"batman.u17\",\n      \"batman.u21\"\n    ]\n  },\n  \"btmn_103\": {\n    \"macro\": \"DE_ROMSTART48\",\n    \"roms\": [\n      \"batcpub5.103\",\n      \"batcpuc5.103\",\n      \"batdsp.102\",\n      \"batman.u7\",\n      \"batman.u17\",\n      \"batman.u21\"\n    ]\n  },\n  \"btmn_106\": {\n    \"macro\": \"DE_ROMSTART48\",\n    \"roms\": [\n      \"b5_a106.128\",\n      \"c5_a106.256\",\n      \"batdsp.102\",\n      \"batman.u7\",\n      \"batman.u17\",\n      \"batman.u21\"\n    ]\n  },\n  \"btmn_f13\": {\n    \"macro\": \"DE_ROMSTART48\",\n    \"roms\": [\n      \"batcpub5.103\",\n      \"batccpuf.103\",\n      \"bat_dspf.103\",\n      \"batman.u7\",\n      \"batman.u17\",\n      \"batman.u21\"\n    ]\n  },\n  \"btmn_g13\": {\n    \"macro\": \"DE_ROMSTART48\",\n    \"roms\": [\n      \"batcpub5.103\",\n      \"batccpug.103\",\n      \"bat_dspg.104\",\n      \"batman.u7\",\n      \"batman.u17\",\n      \"batman.u21\"\n    ]\n  }\n}")
EVIDENCE_HASHES = json.loads("{\n  \"extraction_file_count\": 1882,\n  \"extraction_total_bytes\": 220169171,\n  \"manifest_file_sha256\": \"b5d8be7de424e7eb121f61d2e07ff9c5833d648cb7c2f28942a01f7ec0354c03\",\n  \"manifest_sha256\": \"ae5e8dae78910d9038ea43dd0c30ab91bb5a9e698a9080404420ba16a85c656a\",\n  \"script_bytes\": 172870,\n  \"script_sha256\": \"f78f6b40b92c6acef4febe659fd891620773aa6a18715d2ace0cfa6565c1c53b\",\n  \"table_bytes\": 178216960,\n  \"table_sha256\": \"e3af88daaf88439d6cb1406b1f55889724b1a7da7acd786a8fd63f6cd633d25f\"\n}")
# Digests of the committed excerpts, computed at bundle time from the files themselves so the
# recorded hash cannot drift from the transcription it describes.
EXCERPT_HASHES = json.loads("{\n  \"coil-drivers.md\": \"f05ef8db0b1973a4ff8ac5f7af0eb710f4bde9758ff814c0ed2ee876def4dadb\",\n  \"coil-flash-locations.webp\": \"32fa959a16db866949b19bb6c5b4287b570d5d66ebc975fdc8234024d43b2732\",\n  \"lamp-matrix.md\": \"b2af7c8577ba2aa81dc42325bf4e98a25621b01118d93abef1bbb8cf153d5e1c\",\n  \"switch-matrix.md\": \"ea6aceaa185b972488654f994821429bb20e542170dc3446534eeb3e61504a75\"\n}")


MANUAL = "manual.data-east.batman.1991"
CORE = "pinmame.core.4ec52ff0ac13"
CATALOG = "pinmame.catalog.4ec52ff0ac13"
TABLE = "vpx-table.batman-vpw-1-1"
SCRIPT_REF = "vpx-script.batman-vpw-1-1"
LEGACY = "legacy.game.batman"
EXTRACTION = "vpx-extraction.batman-vpw-1-1"
IPDB = "ipdb.machine.195"

SW = TRANSCRIPTION["switch_matrix"]
LAMPS = TRANSCRIPTION["lamp_matrix"]
AUX = TRANSCRIPTION["coil_drivers"]["direct"]
MUX = TRANSCRIPTION["coil_drivers"]["muxed"]
AUXSOL = TRANSCRIPTION["auxiliary_solenoids"]
PLACES = RESOLUTION["resolved"]
HASHES = EVIDENCE_HASHES

# Effect coordinates observed directly from the retained VPX objects used by its known-working
# script. They identify the modeled assembly/effect location, not the under-playfield mounting
# point of a coil body. Keeping that distinction explicit avoids turning a script relationship
# into a claim about hidden hardware placement.
OUTPUT_PLACES = {
    1: (0.454752, 0.961031, "Drain"),
    2: (0.872369, 0.869841, "BallRelease"),
    3: (0.092489, 0.307754, "Sw39"),
    4: (0.943249, 0.879911, "swPlunger"),
    6: (0.817159, 0.120416, "Sw52"),
    17: (0.312236, 0.184635, "Bumper1B"),
    18: (0.395585, 0.283393, "Bumper2B"),
    19: (0.535522, 0.199931, "Bumper3B"),
    20: (0.233900, 0.698424, "LeftSlingShot"),
    21: (0.686772, 0.700676, "RightSlingShot"),
    22: (0.899321, 0.439848, "DivP"),
}

# The retained script routes switch 55 through Bumper3B and switch 56 through Bumper2B, but that
# reverses the manual's Center/Right identities relative to the independently addressed bumper
# lamps: left/center/right are physically ordered at x ~= .312/.396/.536. Preserve the raw script
# resolution in RESOLUTION, but use the manual-coherent physical identity in the canonical record
# and keep the disagreement explicit in conflict.turbo-bumper-center-right-routing below.
MANUAL_RESOLVED_PLACES = {
    "switch.55": {**PLACES["switch.56"], "address": 55},
    "switch.56": {**PLACES["switch.55"], "address": 56},
}

# Column 1 of the switch matrix is the dedicated cabinet/coin column, exactly as s11.h's
# DE_COMPORTS declares it. These are the only matrix addresses that are not playfield hardware.
CABINET_ROLES = {
    1: ["cabinet.tilt"], 3: ["cabinet.start"], 4: ["cabinet.coin"],
    5: ["cabinet.coin"], 6: ["cabinet.coin"], 7: ["cabinet.slam-tilt"],
}
# Sensors that sit inside a mechanism or a ball-handling device rather than on the playfield
# surface. No retained recreation binds an object to any of them, and inventing a coordinate for
# one would be a projection dressed as a measurement.
INTERNAL_SWITCHES = {10, 11, 12, 13, 50, 51, 53}
# PinMAME owns these two. See the note built below.
EMULATOR_OWNED_SWITCHES = {15, 16}


def prov(status, refs):
    return {"status": status, "source_refs": list(refs)}


def placement(device_id, role, key, refs):
    hit = MANUAL_RESOLVED_PLACES.get(key, PLACES.get(key))
    if hit is None:
        return None
    return {
        "status": "observed",
        "placements": [{
            "id": f"{device_id}.{role}",
            "role": role,
            "space": "playfield",
            "x": hit["x"],
            "y": hit["y"],
            "provenance": prov("observed", refs),
        }],
    }


def output_placement(device_id, address):
    hit = OUTPUT_PLACES.get(address)
    if hit is None:
        return None
    x, y, _object_name = hit
    return {
        "status": "observed",
        "placements": [{
            "id": f"{device_id}.effect",
            "role": "effect",
            "space": "playfield",
            "x": x,
            "y": y,
            "provenance": prov("observed", [TABLE, SCRIPT_REF, MANUAL]),
        }],
    }


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
        notes.append(
            "Dedicated cabinet/coin-door column. s11.h's DE_COMPORTS declares matrix column 1 as "
            "the cabinet inputs, and this manual's own chart agrees address for address."
        )
    if address in EMULATOR_OWNED_SWITCHES:
        notes.append(
            "The manual prints this address as a flipper end-of-stroke switch. Pinned PinMAME "
            "publishes something else on it: btmnGameData declares FLIP_SWNO(15,16), and "
            "core.c:1740-1741 - under its own comment 'set switches in matrix for non-fliptronic "
            "games' - writes the flipper BUTTON state here through core_setSw. Because this game "
            "declares no FLIP_SOL, no FLIP_EOS bit is ever set and the EOS simulation at "
            "core.c:1756-1775 never runs, so no end-of-stroke state is modelled at all. "
            "A recreation must NOT drive this address: core_updateSw overwrites it every frame. "
            "The retained known-working VPW 1.1 script indeed never touches 15 or 16."
        )
    entry = {
        "id": device_id,
        "label": name if not unused else f"Unused Switch {address}",
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
    elif address in EMULATOR_OWNED_SWITCHES or address in INTERNAL_SWITCHES:
        entry["spatial"] = not_applicable("internal_nonvisual", [MANUAL, SCRIPT_REF])
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
    device_id = f"coil.driver-{address}"
    notes = [
        "Left half of the Left/Right relay pair on printed drive "
        f"{address}; the right half is published at address {address + 24}.",
    ]
    if not fitted:
        notes.append("The Special Coil Wiring Diagram prints 'NO COIL AT THIS LOCATION (NOT USED)' on this half.")
    if left.get("note"):
        notes.append(left["note"] + ".")
    record = {
        "id": device_id,
        "label": left.get("name") or f"Unfitted Coil Driver {address} (Left)",
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "used" if fitted else "unused",
        "provenance": prov("validated", [MANUAL, CORE]),
        "physical": {"notes": " ".join(notes)},
        "wiring": coil_wiring(entry),
    }
    if left.get("coil_type"):
        record["physical"]["part_number"] = left["coil_type"]
    if not fitted:
        record["spatial"] = not_applicable("unused", [MANUAL])
    elif address == 8:
        record["spatial"] = not_applicable("cabinet_or_service", [MANUAL, SCRIPT_REF])
    else:
        spatial = output_placement(device_id, address)
        if spatial:
            record["spatial"] = spatial
            record["physical"]["notes"] += (
                f" Spatial effect is projected to the retained VPX assembly '{OUTPUT_PLACES[address][2]}'; "
                "this is not a measurement of the hidden coil body."
            )
        # No spatial key when the retained VPX exposes no defensible assembly coordinate.
    outputs.append(record)

# --- Public 9-16: direct drivers on CN-12, not muxed ---------------------------------------
# Kind "gi" on an ordinary solenoid address: this platform has no separate GI channel, so a
# general-illumination device binds to pinmame.output.solenoid and is typed gi.
DIRECT_KIND = {
    "9": "flasher", "10": "relay", "11": "gi", "12": "flasher",
    "13": "flasher", "14": "flasher", "15": "control_signal", "16": "motor",
}
for address in range(9, 17):
    entry = AUX[str(address)]
    device_id = f"coil.driver-{address}"
    notes = ["Direct CPU driver on CN-12; not affected by the Left/Right relay."]
    if entry.get("bulbs"):
        notes.append(f"Drives {entry['bulbs']} flash lamps ({entry['placement']}).")
    if entry.get("note"):
        notes.append(entry["note"])
    if address == 11:
        notes.append(
            "Runtime sense is inverted: the retained known-working script's SetGI comment says "
            "'Solenoid cuts GI circuit on this era of game', and its Sol11 callback extinguishes "
            "lamp 111 and the backglass GI collection when Enabled is true. Public output 11 "
            "asserted therefore means GI off; deasserted means GI on. The superseded legacy "
            "record independently preserved the same sense. PinMAME types address 11 without "
            "CORE_MODOUT_*_REV while typing address 9 with _REV; that may indicate an emulator "
            "model mismatch, but it does not resolve address 9's separate bulb-type and supply "
            "conflict, so no relationship between the two is inferred."
        )
    record = {
        "id": device_id,
        "label": entry["name"],
        "kind": DIRECT_KIND[str(address)],
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "optional" if address == 15 else "used",
        "provenance": prov("validated", [MANUAL, CORE, SCRIPT_REF, LEGACY] if address == 11 else [MANUAL, CORE]),
        "physical": {"notes": " ".join(notes)},
        "wiring": coil_wiring(entry),
    }
    if address == 11:
        record["roles"] = ["playfield.general-illumination"]
    if address == 10:
        record["spatial"] = not_applicable("internal_nonvisual", [MANUAL, CORE])
    elif address == 15:
        record["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    # Addresses 9 and 12-14 drive visible groups of flash bulbs, 11 controls visible GI bulbs,
    # and 16 drives the playfield Bat Bar mechanism. A single relay/motor coordinate or an
    # internal_nonvisual disposition would misdescribe the authoring requirement, so the spatial
    # key remains absent until all physical effects can be placed.
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
        "own PIA CA2/CB2 permutation, ssSolNo[1] = {3,4,5,1,0,2}, not the Williams ordering.",
    ]
    if entry.get("note"):
        notes.append(entry["note"])
    if address == 22:
        notes.append(
            "The retained known-working script establishes that this public drive controls the "
            "ramp diverter, but neither source establishes whether the downstream actuator is "
            "electrically a coil or a motor; it is therefore typed as a control signal rather "
            "than inventing an actuator technology."
        )
    record = {
        "id": device_id,
        "label": entry["name"],
        "kind": "control_signal" if address == 22 else "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, SCRIPT_REF] if address == 22 else [MANUAL, CORE]),
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
    spatial = output_placement(device_id, address)
    if spatial:
        record["spatial"] = spatial
        record["physical"]["notes"] += (
            f" Spatial effect is projected to the retained VPX assembly '{OUTPUT_PLACES[address][2]}'; "
            "this is not a measurement of the hidden coil or motor body."
        )
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
    outputs.append({
        "id": device_id,
        "label": f"Flash Lamps, Drive {drive} (Right)",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)},
                    {"namespace": "manual.address", "value": str(drive)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE]),
        "physical": {
            "notes": (
                f"Right half of the Left/Right relay pair on printed drive {drive}; the left half "
                f"is published at address {drive}. Drives {right['bulbs']} ({right['placement']}). "
                "s11.c:1209 types the whole 25-32 block generically as No. 89 flashers. The "
                "printed Special Coil Wiring Diagram does not agree on every drive: four of the "
                "eight right-side groups mix No. 906 bulbs in with the No. 89s, so PinMAME's "
                "uniform typing is an emulator output model rather than a statement about the "
                "bulbs actually fitted. The per-drive composition above is the manual's."
            ),
        },
        "wiring": coil_wiring(entry),
        # No spatial key. These drive visible playfield, insert and ramp bulbs, so
        # internal_nonvisual would be a false disposition; the retained table binds no object to
        # the flasher addresses, so there is no coordinate either. The schema offers only located
        # or not_applicable and neither is honest, so the gap is carried in the blocker report.
    })

# --- Public 33-44: inert on this platform ---------------------------------------------------
for address in range(33, 45):
    reason = ("core_getSol only serves 33-36 for GEN_ALLWPC/GEN_SAM, and this game is GEN_DEDMD16"
              if address <= 36 else
              "the S11 'extra' block at 37-44 is written only under S11_SNDOVERLAY or "
              "S11_PRINTERLINE, and btmnGameData sets gameSpecific1 = 0")
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
                "Not a CPU-driven output on this machine. btmnGameData declares no FLIP_SOL, so "
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
        "spatial": not_applicable("virtual", [CORE]),
    })

# --- Public 49, 50 ---------------------------------------------------------------------------
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL; btmnGameData declares custSol = 0, so nothing is published from 51 upward."),
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
    is_cabinet = "Cab." in record["name"] or record["name"].startswith("Backpanel ")
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
        if "Cab." in record["name"]:
            entry["roles"] = ["cabinet.start"]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        spatial = placement(device_id, "emitter", f"lamp.{address}", [TABLE, MANUAL])
        if spatial:
            entry["spatial"] = spatial
    outputs.append(entry)

displays = [{
    "id": "display.dmd",
    "label": "128x16 Dot Matrix Display",
    "kind": "dmd",
    "width": 128,
    "height": 16,
    "provenance": prov("validated", [CORE, MANUAL]),
    "spatial": not_applicable("cabinet_or_service", [CORE, MANUAL]),
}]

mechanisms = [
    {
        "id": "mechanism.bar-motor",
        "label": "Bar Motor",
        "kind": "motorized",
        "actuators": ["coil.driver-16"],
        "sensors": ["switch.matrix-50", "switch.matrix-51"],
        "behavior": (
            "A motorised bar driven by public solenoid 16 through a relay board that switches the "
            "28 VAC Batbar Motor Assy 515-5256-00-11. The retained known-working script models it "
            "as a cvpmMech with Sol1 = 16 and two position switches, addsw 50 at rest position 0 "
            "and addsw 51 across positions 47-49, so 50 and 51 are the travel limits of this one "
            "mechanism rather than sensors of anything else. The script also drives the Bat Bar "
            "Standup target object at switch 49 from the same position variable, dropping it out "
            "of reach as the bar advances; that is an occlusion relationship rather than the bar "
            "actuating the target, so 49 is not listed as a sensor of this mechanism."
        ),
        "assembly_part_number": "515-5256-00-11",
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.ramp-diverter",
        "label": "Ramp Diverter",
        "kind": "diverter",
        "actuators": ["coil.driver-22"],
        "sensors": [],
        "behavior": (
            "Public solenoid 22 diverts the ramp. The manual prints this drive only as 'Motor "
            "Circuit (See Schematic)' with no coil type, so its identity comes from the retained "
            "known-working script, whose own callback is named SolDiv and commented 'Ramp "
            "Diverter (22)' and which raises and lowers two ramp diverter objects from it."
        ),
        "provenance": prov("validated", [SCRIPT_REF]),
    },
    {
        "id": "mechanism.left-three-bank",
        "label": "Left 3 Bank Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
        "behavior": (
            "Three standup targets printed Left 3 Bank Top/Middle/Bottom at 33-35. They are "
            "standups, not drop targets: no solenoid resets them, and the retained script's "
            "handlers pulse the switch and nudge the target object a few units before returning "
            "it, rather than dropping and raising it."
        ),
        "positions": [
            {"id": "mechanism.left-three-bank.top", "label": "Left 3 Bank Top", "sensors": ["switch.matrix-33"]},
            {"id": "mechanism.left-three-bank.middle", "label": "Left 3 Bank Middle", "sensors": ["switch.matrix-34"]},
            {"id": "mechanism.left-three-bank.bottom", "label": "Left 3 Bank Bottom", "sensors": ["switch.matrix-35"]},
        ],
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.right-three-bank",
        "label": "Right 3 Bank Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
        "behavior": (
            "Three standup targets printed Right 3 Bank Top/Middle/Bottom at 41-43, handled the "
            "same way as the left bank and likewise not drop targets."
        ),
        "positions": [
            {"id": "mechanism.right-three-bank.top", "label": "Right 3 Bank Top", "sensors": ["switch.matrix-41"]},
            {"id": "mechanism.right-three-bank.middle", "label": "Right 3 Bank Middle", "sensors": ["switch.matrix-42"]},
            {"id": "mechanism.right-three-bank.bottom", "label": "Right 3 Bank Bottom", "sensors": ["switch.matrix-43"]},
        ],
        "provenance": prov("validated", [MANUAL, SCRIPT_REF]),
    },
    {
        "id": "mechanism.joker-face",
        "label": "Joker Face",
        "kind": "toy",
        "actuators": [],
        "sensors": ["switch.matrix-36", "switch.matrix-37", "switch.matrix-38"],
        "behavior": (
            "Three sensors on the Joker toy, printed Joker Left Eye, Joker Right Eye and Joker "
            "Mouth at 36-38, with matching Joker Left Eye and Joker Right Eye lamps at 36-37."
        ),
        "provenance": prov("validated", [MANUAL]),
    },
    {
        "id": "mechanism.ball-trough",
        "label": "Ball Trough",
        "kind": "kicker",
        "actuators": ["coil.driver-1", "coil.driver-2"],
        "sensors": ["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13"],
        "behavior": (
            "Outhole at 10 feeding a three-position trough at 11-13, kicked by the Outhole coil "
            "on printed drive 1 and the Trough Eject coil on printed drive 2. The retained script "
            "models the whole assembly through a cvpmTrough device with InitSwitches Array(13,12,11): "
            "the helper ejects slot 0, so 13 is nearest the eject, 12 is the middle position, and "
            "11 is nearest the drain-side entrance. No "
            "individual trough position has its own table object."
        ),
        "positions": [
            {"id": "mechanism.ball-trough.nearest-drain", "label": "Trough 1 (Nearest Drain)",
             "sensors": ["switch.matrix-11"]},
            {"id": "mechanism.ball-trough.middle", "label": "Trough 2",
             "sensors": ["switch.matrix-12"]},
            {"id": "mechanism.ball-trough.nearest-eject", "label": "Trough 3 (Nearest Eject)",
             "sensors": ["switch.matrix-13"]},
        ],
        "provenance": prov("observed", [MANUAL, SCRIPT_REF]),
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
        "id": "conflict.motor-circuit-identity",
        "path": "outputs[id=coil.driver-22]; mechanisms[id=mechanism.bar-motor]; mechanisms[id=mechanism.ramp-diverter]; inputs[id=switch.matrix-50]; inputs[id=switch.matrix-51]",
        "description": (
            "The manual and the retained known-working script name this hardware differently. The "
            "printed Switch Matrix Chart calls switches 50 and 51 'Museum Motor Up' and 'Museum "
            "Motor Down', and the Special Coil Wiring Diagram prints drive 22 only as 'Motor "
            "Circuit (See Schematic)' with no coil type. The script instead binds 50 and 51 as the "
            "two travel limits of a cvpmMech whose Sol1 is public solenoid 16 - the drive the same "
            "diagram wires to the 28 VAC Batbar Motor Assy - and binds public solenoid 22 to a "
            "callback named SolDiv, commented 'Ramp Diverter', which moves ramp diverter objects "
            "and no motor at all. This project's evidence order makes the known-working script "
            "authoritative for runtime causality, so the topology recorded here follows it: the "
            "50/51 pair belongs to the solenoid-16 bar mechanism and 22 is a diverter. What is NOT "
            "settled is the printed name: whether the physical machine's marketing or service "
            "vocabulary calls that assembly the Museum Motor, the Bat Bar, or both, and whether "
            "the manual's 'Motor Circuit' row for drive 22 is simply a generic label for an "
            "unlisted device. An earlier draft of this definition asserted a Museum Motor "
            "mechanism actuated by drive 22 and sensed by 50/51, which no source supports. "
            "Resolution path: the printed playfield parts pages, or a photograph of the assembly. "
            "Unresolved."
        ),
        "source_refs": [MANUAL, SCRIPT_REF],
    },
    {
        "id": "conflict.solenoid-9-bulb-type",
        "path": "outputs[id=coil.driver-9]",
        "description": (
            "s11.c:1206 types public solenoid 9 as CORE_MODOUT_BULB_44_6_3V_AC_REV - a "
            "reverse-polarity 6.3 volt AC No. 44 bulb - as a Batman/Hook-specific special case. "
            "The manual's Special Coil Wiring Diagram (printed page 29) shows printed drive 09 "
            "driven by Q30 on BRN-BLK feeding four No. 89 bulbs at +32 volts, three insert and "
            "one playfield, which is the same arrangement as drives 12, 13 and 14 that PinMAME "
            "itself types as ordinary No. 89 flashers. The two sources disagree about bulb type, "
            "supply voltage and polarity. This affects an output brightness model rather than an "
            "address, so it does not change what a consumer binds, but it is not resolvable from "
            "either source alone. Resolution path: a photograph of the socket and bulb at that "
            "circuit on an unmodified machine, or a LibPinMAME trace observing the output's duty "
            "behaviour against the other flasher drives. Unresolved."
        ),
        "source_refs": [CORE, MANUAL],
    },
    {
        "id": "conflict.matrix-position-2-naming",
        "path": "inputs[id=switch.matrix-2]",
        "description": (
            "s11.h's DE_COMPORTS macro names dedicated column-1 position 2 'Ball Tilt' and wires "
            "an input port bit to it for every Data East game. This machine's own printed Switch "
            "Matrix Chart prints position 2 'Not Used', and the Switch Part Numbers page lists no "
            "part at that address. The shared macro is a platform-wide default rather than a "
            "per-game measurement, so the printed table is the better authority for what is "
            "fitted here, and the address is recorded unused - but pinned PinMAME will still "
            "accept and publish a value on it. Unresolved in the sense that no source states "
            "whether the DE platform ever fitted the contact this bit was reserved for. "
            "Resolution path: a photograph or continuity check of an unrestored cabinet's "
            "WHT-RED CN10-8 return line, which this machine's own printed chart gives as "
            "position 2's return, showing whether any contact lands on it; or a Data East "
            "cabinet or coin-door parts page from a title whose own chart does name the "
            "position - the Lethal Weapon 3 manual retained in this repository prints it "
            "4th Coin - identifying the contact the shared macro bit was reserved for. "
            "Unresolved."
        ),
        "source_refs": [CORE, MANUAL],
    },
    {
        "id": "conflict.turbo-bumper-center-right-routing",
        "path": "inputs[id=switch.matrix-55]; inputs[id=switch.matrix-56]; outputs[id=coil.driver-18]; outputs[id=coil.driver-19]; outputs[id=lamp.matrix-45]; outputs[id=lamp.matrix-46]",
        "description": (
            "The retained known-working script routes Bumper3B_Hit to switch 55 and Bumper2B_Hit "
            "to switch 56, reversing the printed Center/Right switch identities. The manual uses "
            "one consistent Left/Center/Right vocabulary for switches 54-56, special solenoids "
            "17-19 and bumper lamps 44-46. The lamp objects independently place those identities "
            "left-to-right at x about .312, .399 and .536, so the canonical switch and coil-effect "
            "placements follow that coherent physical ordering: 55/18 are center at x about .396 "
            "and 56/19 are right at x about .536. The raw script bindings remain preserved in the "
            "embedded resolution evidence. Resolution path: inspect an unmodified physical "
            "machine or test the switch numbers in diagnostics to determine whether the table "
            "script merely crossed the two bumper callbacks. Unresolved."
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
    "btmn_103": "Batman (1.03)", "btmn_101": "Batman (1.01)", "btmn_106": "Batman (1.06)",
    "btmn_f13": "Batman (1.03 French)", "btmn_g13": "Batman (1.03 German)",
}
ROOT_DRIVER = "btmn_103"
_root = ROM_SETS[ROOT_DRIVER]["roms"]
_ROLES = ("CPU B5", "CPU C5", "display")

drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]["roms"]
    macro = ROM_SETS[driver_id]["macro"]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root and the shipped production firmware. Every btmn_* set shares one "
            "btmnGameData through PinMAME's CORE_GAMEDEF macro, so all five present identical "
            "playfield hardware and identical public addresses."
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
        note += (" Sound ROMs are byte-identical across all five sets, and the shared "
                 "btmnGameData means the address model is unchanged.")
    drivers.append({
        "id": driver_id,
        "description": DRIVER_LABELS[driver_id],
        "year": "1991",
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
        "id": IPDB, "kind": "human_review",
        "uri": "https://www.ipdb.org/machine.cgi?id=195",
        "locator": "IPDB 195 identifies Data East Batman, July 1991; used only for physical product identity and date.",
        "license": "NOASSERTION", "attribution": "Internet Pinball Database",
        "acquired_at": "2026-08-08T00:00:00Z",
    },
    {
        "id": MANUAL, "kind": "manual",
        "uri": "https://archive.org/details/Data_East_Batman_Manual",
        "locator": "Data_East_1991_Batman_Manual.pdf; printed pages 24-29",
        "sha256": TRANSCRIPTION["document_sha256"],
        "source_id": "Data_East_Batman_Manual",
        "original_filename": "Data_East_1991_Batman_Manual.pdf",
        # A hash proves the local copy has not changed; it says nothing about what the document
        # said, and this manual is a 70-page image-only scan nobody else can grep. The regions
        # actually read are transcribed beside the definition and digest-checked.
        "excerpts": [
            {
                "id": "excerpt.batman.switch-matrix",
                "locator": "printed page 24 (PDF 28), Switch Matrix Chart",
                "path": "evidence/excerpts/data-east.batman.1991/switch-matrix.md",
                "sha256": EXCERPT_HASHES["switch-matrix.md"],
                "method": "manual",
                "transcribed_by": "curator, read from a 400 dpi render; this document has no text layer",
                "reviewed": True,
            },
            {
                "id": "excerpt.batman.lamp-matrix",
                "locator": "printed page 26 (PDF 30), Lamp Matrix Chart",
                "path": "evidence/excerpts/data-east.batman.1991/lamp-matrix.md",
                "sha256": EXCERPT_HASHES["lamp-matrix.md"],
                "method": "manual",
                "transcribed_by": "curator, read from a 400 dpi render; this document has no text layer",
                "reviewed": True,
            },
            {
                "id": "excerpt.batman.coil-drivers",
                "locator": "printed pages 28-29 (PDF 32-33), Flash Lamp Coil Tests, Coil and Flash Lamp Locations drawing, CPU Controlled Auxiliary Solenoids, Flipper Solenoids, Backbox Flash Lamps inset and Special Coil Wiring Diagram",
                "image": "evidence/excerpts/data-east.batman.1991/coil-flash-locations.webp",
                "image_derivation": "Data_East_1991_Batman_Manual.pdf page 32, crop box 0.08,0.36,0.9,0.94 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 55 WebP",
                "image_sha256": EXCERPT_HASHES["coil-flash-locations.webp"],
                "path": "evidence/excerpts/data-east.batman.1991/coil-drivers.md",
                "sha256": EXCERPT_HASHES["coil-drivers.md"],
                "method": "manual",
                "transcribed_by": "curator, read from 400 dpi renders; this document has no text layer",
                "reviewed": True,
            },
        ],
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "Data East Pinball, Inc.",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": "external:pinmame-vpx-sources/data-east/batman-1991/Batman%20%28Data%20East%201991%29%20VPW%20v1.1.vpx",
        "locator": "retained known-working recreation; playfield 952 x 1974",
        "sha256": HASHES["table_sha256"],
        "known_working": True,
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; table metadata credits Javier, Dark and Ben Logan",
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": "external:pinmame-vpx-sources/data-east/batman-1991/Batman%20%28Data%20East%201991%29%20VPW%20v1.1.vbs",
        "locator": "table script; Lampz.MassAssign bindings and Controller.Switch/PulseSw handlers",
        "sha256": HASHES["script_sha256"],
        "known_working": True,
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; table metadata credits Javier, Dark and Ben Logan",
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": "external:pinmame-vpx-sources/data-east/batman-1991/extraction-manifest.json",
        "locator": (f"vpxtool extraction of the retained table, {HASHES['extraction_file_count']} files, "
                    f"{HASHES['extraction_total_bytes']} bytes; the manifest's own manifest_sha256 field is "
                    f"{HASHES['manifest_sha256']} and is recomputable by the algorithm the file states"),
        "sha256": HASHES["manifest_file_sha256"],
        "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "VPW; table metadata credits Javier, Dark and Ben Logan",
    },
    {
        "id": LEGACY, "kind": "legacy_json",
        "uri": "https://github.com/vpinball/pinmame-game-defs",
        "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
        "locator": "games/batman.json; origin=vbscript-parser",
        "attribution": "pinmame-game-defs contributors",
    },
]

_placed = sum(len(d.get("spatial", {}).get("placements", []))
              for d in inputs + outputs)

definition = {
    "format": "pinmame-machine-definition",
    "schema_version": 2,
    "machine": {
        "id": "data-east.batman.1991",
        "name": "Batman",
        "manufacturer": "Data East",
        "year": 1991,
        "kind": "physical_pinball",
        "ipdb_id": 195,
        "playfield": {"width": RESOLUTION["playfield"]["width"],
                      "height": RESOLUTION["playfield"]["height"],
                      "units": "vpx"},
        "opdb_id": "GrOpb-MQ7w1",
    },
    "controller": {
        "platform": "pinmame.dataeast",
        "hardware_generation": "0x2000",
        "inversion_applied_by_emulator": True,
    },
    "coverage": {
        "status": "partial",
        "dimensions": {
            "catalog_identity": "validated",
            "address_enumeration": "validated",
            "semantic_naming": "observed",
            "physical_wiring": "observed",
            "mechanisms": "conflicted",
            "variant_coverage": "validated",
            "recreation_knowledge": "observed",
            "spatial_placement": "observed",
        },
        "missing": [
            "input_semantics",
            "mechanism_behavior",
            "polarity",
            "recreation_notes",
            "spatial_placement",
            "unresolved_conflicts",
        ],
    },
    "drivers": drivers,
    "inputs": inputs,
    "outputs": outputs,
    "displays": displays,
    "mechanisms": mechanisms,
    "relationships": relationships,
    "conflicts": conflicts,
    "sources": sources,
    "knowledge": {"path": "knowledge/data-east/batman-1991.md", "status": "partial"},
}

# --- Spatial report ---------------------------------------------------------------------------
# Generated from the same objects as the definition, so a statement here cannot outlive the data
# behind it. Everything that has no coordinate is named rather than counted.
# Identify devices by canonical id, never by bare address: switch 17 and lamp 17 are different
# devices and a numeric-only audit cannot tell them apart, which makes the measured-versus-computed
# split unauditable and puts the same number in two different blocker lists.
_internal_nonvisual_devices = sorted(
    d["id"] for d in inputs + outputs
    if d["availability"] == "used" and "spatial" in d
    and d["spatial"].get("status") == "not_applicable"
    and d["spatial"].get("reason") == "internal_nonvisual")
_no_spatial_key = sorted(d["id"] for d in inputs + outputs if "spatial" not in d)
_KIND_TO_ID = {"switch": "switch.matrix-", "lamp": "lamp.matrix-"}
_computed = sorted(
    _KIND_TO_ID[k.split(".")[0]] + k.split(".")[1]
    for k, v in PLACES.items() if v["coordinate_origin"] == "computed-centroid")

spatial_report = {
    "format": "pinmame-spatial-blockers",
    "version": 1,
    "machine_id": "data-east.batman.1991",
    "status": "partial",
    "coordinate_convention": (
        "Normalized against the retained table's own playfield bounds, "
        f"{RESOLUTION['playfield']['width']:.0f} x {RESOLUTION['playfield']['height']:.0f}. "
        "This machine is NOT the 2162-tall playfield most WPC-era tables use; normalizing y by "
        "2162 would compress every coordinate by about nine percent. The resolver refuses to run "
        "if it ever sees different bounds."
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
            "Point-like table objects (Light, Trigger, Kicker, Bumper, Flasher, Primitive) carry "
            "their own center. Extended objects (Wall, Ramp, Rubber) are defined by drag points "
            "and have none, so those are the centroid of the object's drag points. A centroid is "
            "a derivation, not an observation, and is reported separately for that reason."
        ),
        "computed_devices": _computed,
    },
    "blockers": [
        {
            "id": "devices-without-a-retained-object",
            "severity": "major",
            "detail": (
                "These addresses are printed, fitted playfield or in-mechanism devices that the "
                "retained recreation does not model completely enough to assign every required "
                "effect coordinate. They are recorded not_applicable/internal_nonvisual only where "
                "the device genuinely has no authoring-visible playfield location; otherwise the "
                "spatial key is omitted - the schema offers only located or not_applicable, and "
                "neither is honest for an unplaced physical effect."
            ),
            "internal_nonvisual_devices": _internal_nonvisual_devices,
            "omitted_spatial_key_devices": _no_spatial_key,
        },
        {
            "id": "single-retained-recreation",
            "severity": "minor",
            "detail": (
                "Exactly one known-working recreation was retained, so every coordinate is a "
                "single measurement with nothing to corroborate it. Placements are therefore "
                "`observed` rather than `validated`; promoting this machine would need at least "
                "one further independent table to agree. The retained printed location drawings "
                "on manual pages 25 and 27 have not yet been digitized. The page-28 Coil and Flash "
                "Lamp Locations drawing is committed as a legible crop and corroborates topology, "
                "sidedness, and rough regions, but it is not a normalized coordinate source. Its "
                "1A-8A and 1B-8B callouts also show why the grouped flash-lamp outputs keep their "
                "spatial key omitted: one public address spans multiple playfield, insert, ramp, "
                "and backbox bulbs, so neither one point nor cabinet_or_service describes it."
            ),
        },
    ],
    # Resolver misses are implementation details, not curation gaps. Report only fitted devices
    # whose canonical record still lacks either a placement or an explicit non-spatial disposition.
    "unresolved": {
        "lamps": [
            {
                "address": address,
                "device_id": f"lamp.matrix-{address}",
                "reason": "fitted playfield lamp has no retained physical coordinate",
            }
            for address in (50, 51, 52, 53)
        ],
        "switches": [],
    },
}

# --- Knowledge note ---------------------------------------------------------------------------
_used_switches = sum(1 for d in inputs if d["kind"] == "switch" and d["availability"] == "used")
_switch_places = sum(1 for k in PLACES if k.startswith("switch."))
_lamp_places = sum(1 for k in PLACES if k.startswith("lamp."))
_CONFLICT_SUMMARIES = {
    "conflict.motor-circuit-identity": "the manual's Museum Motor terminology versus the working script's Bat Bar motor and ramp-diverter routing",
    "conflict.solenoid-9-bulb-type": "the bulb type and supply PinMAME assigns to solenoid 9",
    "conflict.matrix-position-2-naming": "whether dedicated matrix position 2 was ever fitted",
    "conflict.turbo-bumper-center-right-routing": "the retained script's crossed Center/Right turbo-bumper callbacks",
}
if set(_CONFLICT_SUMMARIES) != {conflict["id"] for conflict in conflicts}:
    raise SystemExit("knowledge-note conflict summaries do not match the canonical conflict set")
_conflict_summary = "; ".join(
    f"`{conflict_id}` - {summary}" for conflict_id, summary in _CONFLICT_SUMMARIES.items())

knowledge_note = f"""# Batman (Data East, 1991)

Coverage: **partial - manual-verified semantic I/O for the full 8x8 switch and lamp matrices with
connector, wire-colour and drive-transistor wiring, all 22 printed coil drivers including the
Left/Right relay pair, and normalized placements from one retained recreation; held below
author-ready because the W7 jumper meaning and device polarities remain incomplete, only a single recreation was retained,
and {len(conflicts)} source disagreements are unresolved**

## Identity

Data East Batman, 1991, `GEN_DEDMD16` - the 128x16 DMD generation, display board 520-5042-00,
sound board 520-5050-01. PinMAME roots the family at `btmn_103` with {len(drivers)} drivers.
Every one shares `init_btmn` and therefore one `btmnGameData`, so all five are the same physical
machine; what differs is CPU game ROMs, plus a language display ROM on the French and German
sets, plus a ROM-layout macro on 1.01. Sound ROMs are byte-identical across all five.

**`batmanf` is Batman Forever, Sega 1995, `GEN_DEDMD64`.** It lives in the same game-table file
and shares a name prefix, and it is a completely different physical machine. Do not group them.

## Relationship to the shared Data East profile

Batman is **Data East hardware**, `GEN_DEDMD16`. It is not a Williams System 11 machine. What is
true is narrower and is a fact about PinMAME rather than about the cabinet: there is no `de.c`,
`degames.c` includes `s11.h`, and Data East games are driven by the same emulator source file as
Williams System 11 because the Data East CPU board was closely derived from it.

The reviewed `controllers/pinmame/data-east.json` profile now represents those shared facts directly: column-major sequential switch numbering, the W7 jumper at public DIP address 0, 64 base lamps, the mux-relay pairing of an A-side address with A+24, address 23 as a virtual flipper/switched-solenoid enable, Data East's special-solenoid permutation, and no dedicated GI channel. Batman therefore no longer carries a `controller_platform` blocker.

The record therefore keeps the `pinmame.dataeast` platform rather than claiming a Williams one.
Four differences are established from pinned source:

- **Diagnostic buttons.** `s11.h` gives Data East only `DE_SWADVANCE` (-7) and `DE_SWUPDN` (-6).
  The -5 and -4 addresses beside them are `S11_SWCPUDIAG` and `S11_SWSOUNDDIAG`, Williams only.
- **Special-solenoid permutation.** `setSSSol` selects `ssSolNo[1] = {3,4,5,1,0,2}` for Data East
  against `ssSolNo[0] = {5,4,1,2,0,3}` for Williams, so the PIA-line-to-public-address map for
  17-22 differs between them.
- **Cabinet column.** Column 1 is loaded from `DE_COMPORTS`, not `S11_COMPORTS`.
- **Advance polarity.** `s11.c` reads Data East's Advance button inverted, as
  `!core_getSw(DE_SWADVANCE)`.

The machine-level `inversion_applied_by_emulator: true` follows the repository contract: consumers must not invert normalized public LibPinMAME states again. Batman's per-game `wpc.invSw` mask is independently all zeroes; that fact is retained here rather than overloaded into the consumer-facing flag.

## The address model, and where it differs from WPC and Whitestar

Data East runs on the shared Williams System 11 core (`s11.c`); there is no `de.c`. `s11.c`
installs no switch or lamp conversion of its own, so it inherits PinMAME's sequential defaults,
`core_m2swSeq(col,row) = col*8+row-7`. **Both printed matrices are column-major**: address =
(column - 1) x 8 + row. Column 1 of the switch matrix is the cabinet/coin column, exactly as
`DE_COMPORTS` declares.

Four things will surprise anyone carrying WPC or Whitestar assumptions across.

- **There is no GI channel at all.** `coreGlobals.nGI` is never assigned anywhere in `s11.c` and
  `gi[]` is never written, so `vp_getGI` always reports zero. General illumination is **public
  solenoid 11**, which the manual prints as the "General Illumination Relay" (K-1) and which
  `s11.c:1207` comments `// GI output`. The retained script agrees, naming its own callback
  `'GI Relay`. Its runtime sense is inverted: asserted output 11 cuts the GI circuit and turns the
  playfield and backglass GI off; deasserted output 11 restores GI. The script states this in its
  own SetGI comment and implements it in `Sol11`, and the superseded legacy record preserves the
  same sense. PinMAME instead types address 11 without `_REV` while applying `_REV` to address 9;
  that discrepancy does not resolve address 9's separate bulb-type and supply conflict, so the two
  facts remain documented without inferring a causal swap.
- **Public solenoid 10 is the Left/Right relay and it re-routes addresses.** With it energised,
  outputs 1-8 are re-published at 25-32 and read zero at 1-8. The manual describes the same
  mechanism in prose: the relay "switch[es] +32 volts between coils or flash lamps; these sets
  are termed 'left' and 'right'", and it is why 22 drivers yield "29 regular coils". Every right
  half on this machine is a group of four flash lamps.
- **PinMAME's flasher typing is uniform and the machine is not.** `s11.c:1209` types the whole
  25-32 block as No. 89 bulbs, but the printed wiring diagram shows four of the eight right-side
  groups mixing No. 906 bulbs in. Treat the emulator's output type as a brightness model, not as
  evidence of what is fitted; the manual's per-drive composition is recorded on each address.
- **64 lamps, not 80**, and every one of the 64 is populated - the printed chart has no "Not
  Used" cell anywhere. Any address above 64 is not hardware; the superseded legacy record listed
  lamps at 109 and 111-132, and the retained script binds 71 `Lampz` slots, both of which are
  recreation-side fictions.
- **Solenoids 33-44 are permanently zero here.** `core_getSol` only serves 33-36 for
  `GEN_ALLWPC`/`GEN_SAM`, and the S11 extra block at 37-44 is written only under
  `S11_SNDOVERLAY` or `S11_PRINTERLINE`, neither of which this game sets.

## Public switches 15 and 16 belong to the emulator

The printed matrix names them Left EOS and Right EOS. Pinned PinMAME publishes something else
there. `btmnGameData` declares `FLIP_SWNO(15,16)`, and `core.c:1740-1741` - under its own comment
"set switches in matrix for non-fliptronic games" - writes the flipper **button** state into those
two addresses via `core_setSw`. Because this game declares no `FLIP_SOL`, no `FLIP_EOS` bit is
ever set and the end-of-stroke simulation at `core.c:1756-1775` never runs at all.

**A recreation must not drive public 15 or 16**, because `core_updateSw` overwrites them on every
frame. The retained known-working script never touches either address, which is the behaviour this
predicts.

## Flipper coils are synthesised, and fire in pairs

There is no `FLIP_SOL`, so `core.c:1746-1753` fabricates 45-48 from Game On plus button state:
power and hold assert and release together. They are not independently controllable and must not
be modelled as separate coils. The manual's own unnumbered "Flipper Solenoids" table lists a left
and a right flipper and nothing else - there is no upper flipper of either hand, which is
consistent with the driver setting no upper-flipper bit.

## Evidence and its limits

The retained manual has **no text layer whatsoever** ({TRANSCRIPTION['document']['page_count']} pages,
{TRANSCRIPTION['document']['character_count']} characters, `{TRANSCRIPTION['document']['extraction_status']}`), so every table here was read from 400 dpi renders and
transcribed by hand. Nothing came from `pdftotext`.

Spatial placement rests on **one** retained recreation, the VPW v1.1 build, whose playfield is
**952 x 1974** - not the 2162 most WPC-era tables use. {_switch_places} of the {_used_switches}
fitted switches and {_lamp_places} of the 64 lamps resolved to an object; nothing resolved to an
address the manual prints "Not Used", which is the check that would have caught an invented
binding. {len(_computed)} coordinates are centroids of an extended object's drag points rather
than a measured center, and are reported as such in the spatial report. Effect coordinates for
ball-handling coils, bumpers, slingshots and the ramp diverter are projections to the exact VPX
assemblies exercised by the working script; they do not pretend to locate hidden coil bodies.

{len(conflicts)} source disagreements are recorded as unresolved conflicts rather than decided: {_conflict_summary}.
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
	existing = root / "machines/author-ready/data-east/batman-1991.json"
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
			raise RuntimeError(f"Batman {label} is missing: {target}")
		if _comparable(target.read_bytes()) != _comparable(expected):
			raise RuntimeError(f"Batman {label} does not match the deterministic curator: {target}")
	report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
	expected_format = "pinmame-spatial-audit" if definition["coverage"]["status"] == "author_ready" else "pinmame-spatial-blockers"
	if report.get("format") != expected_format or report.get("machine_id") != definition["machine"]["id"]:
		raise RuntimeError(
			f"Batman spatial report must be {expected_format} for a "
			f"{definition['coverage']['status']} machine and must name this machine")
	placements = sum(
		len(device.get("spatial", {}).get("placements", []))
		for collection in ("inputs", "outputs")
		for device in definition[collection])
	if report.get("placement_count") != placements:
		raise RuntimeError(
			f"Batman spatial report claims {report.get('placement_count')} placements "
			f"but the definition carries {placements}")
	print("Batman definition, seed, spatial report, and knowledge note match the deterministic curator.")


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _vpx_sources_root(explicit: Path | None) -> Path:
	if explicit is not None:
		return explicit.expanduser().resolve()
	if value := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
		return Path(value).expanduser().resolve()
	for parent in ROOT.resolve().parents:
		candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
		if candidate.is_dir():
			return candidate
	raise RuntimeError("Batman VPX sources root was not supplied and could not be discovered")


def _write_extraction_manifest(source_root: Path) -> Path:
	base = source_root / "data-east/batman-1991"
	extraction = base / "vpxtool-extract"
	if not extraction.is_dir():
		raise RuntimeError(f"Batman retained extraction is missing: {extraction}")
	paths = sorted(
		(path for path in extraction.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction).as_posix(),
	)
	body = {
		"files": [
			{
				"bytes": path.stat().st_size,
				"path": path.relative_to(extraction).as_posix(),
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
	}
	canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
	manifest = dict(body)
	manifest["manifest_sha256"] = hashlib.sha256(canonical).hexdigest()
	target = base / "extraction-manifest.json"
	write_json(target, manifest)
	print(
		f"Batman extraction: files={len(paths)}, bytes={sum(path.stat().st_size for path in paths)}, "
		f"manifest_sha256={manifest['manifest_sha256']}, file_sha256={_file_sha256(target)}"
	)
	return target


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts.")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed.")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest.")
	parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository root to operate on.")
	parser.add_argument("--vpx-sources-root", type=Path, help="Override the discoverable retained VPX sources root.")
	args = parser.parse_args()
	root = args.repository_root.resolve()
	if args.write_extraction_manifest:
		print(f"Wrote {_write_extraction_manifest(_vpx_sources_root(args.vpx_sources_root))}")
		return
	if args.regenerate:
		_write(root)
		print(f"Wrote {DEFINITION_PATH.relative_to(ROOT)} and {SEED_PATH.relative_to(ROOT)}")
		return
	_check(root)


if __name__ == "__main__":
	main()
