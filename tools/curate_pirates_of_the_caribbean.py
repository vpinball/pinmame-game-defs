"""Curate the physical Stern Pirates of the Caribbean (2006) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring
detail, and normalized coordinate is embedded as a literal, so regeneration
reproduces the canonical artifact byte-for-byte without reading the external
evidence roots.  ``--check`` refuses drift, and ``--regenerate`` is the only path
that writes the canonical definition and its pinned seed.

Identity note.  PinMAME's clone-tree parent is ``potc_600af``, the 2008 V6.0
firmware, and the superseded generated stub therefore recorded the machine year
as 2008.  The physical machine is a 2006 Stern production game: the retained
manual's own printed page 3 carries ``(c)2006  820-6384-00 Rev A``, and pinned
PinMAME's own catalog dates the earliest firmware in this clone tree
(``potc_108as`` through ``potc_115gf``) 2006.  Under this project's identity rule
a later firmware revision does not create a new physical game, so the physical
record is ``stern.pirates-of-the-caribbean.2006`` and the parent driver's own
2008 year is carried only on that driver's record.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/stern/pirates-of-the-caribbean-2006.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/pirates-of-the-caribbean-2006.json"
SEED_PATH = ROOT / "tools/seeds/stern/pirates-of-the-caribbean-2006.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/pirates-of-the-caribbean-2006.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/pirates-of-the-caribbean-2006.md"
# The generated stub this definition supersedes. It is deliberately left on disk by this
# worktree: pruning it here would leave the shared catalog (which this branch must not
# regenerate) pointing at a missing file and would break tests/test_classification.py. The
# integrator's rebuild_catalog call prunes both the stub definition and its knowledge note
# through _prune_generated_stubs once this definition claims the potc_* clone-tree root.
SUPERSEDED_STUB_PATH = ROOT / "machines/stubs/potc_600af.json"
SUPERSEDED_STUB_KNOWLEDGE_PATH = ROOT / "knowledge/stubs/potc_600af.md"

MACHINE_ID = "stern.pirates-of-the-caribbean.2006"
KNOWLEDGE_PATH = "knowledge/stern/pirates-of-the-caribbean-2006.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-sam"
MANUAL_SOURCE = "manual.stern.pirates-of-the-caribbean.2006"
MANUAL_SUPPORT_SOURCE = "manual-support.stern.pirates-of-the-caribbean.2006"
VPX_TABLE_SOURCE = "vpx-table.potc-stern-2006"
VPX_SCRIPT_SOURCE = "vpx-script.potc-stern-2006"
VPX_EXTRACTION_SOURCE = "vpx-extraction.potc-stern-2006"

TABLE_SHA256 = "d69fea24ad8d1dd4fc49c84214e71b448d6a602b6ef768a329a55a94f15aad59"
SCRIPT_SHA256 = "fb6cec754fc907f1fbb41f1f71273d6585db73365073b3a18cfe2c12d90c39e3"
MANUAL_SHA256 = "faa493698371d4e6d2d821c9f6489ce780d50cfd92c5a0ed71c50a99df1875be"
MANUAL_TRANSCRIPTION_SHA256 = "e440218cd68c47b1a21a1643f53cb82a7a2f5bb3530b59035045d9a0eb199314"
VPX_GEOMETRY_SHA256 = "12f88a9f9a2a76a13a6c71cf3491bf96d4480842663bdf5dc8b388733d6c3dfe"

EXTRACTION_RELATIVE_PATH = Path("stern/pirates-of-the-caribbean-2006/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/pirates-of-the-caribbean-2006/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "b462146e7b641f57fdb08a032c9298ce921675e63798ba245bcca0e3904fe799"
EXTRACTION_FILE_COUNT = 1229
EXTRACTION_TOTAL_BYTES = 85415058

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2155"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2155.0

EXCERPT_ROOT = "evidence/excerpts/stern.pirates-of-the-caribbean.2006"

# --- Drivers -------------------------------------------------------------------------------------
# 28 drivers: CORE_GAMEDEF(potc, 600af, ...) plus 27 CORE_CLONEDEF(potc, ...) rows, counted from
# src/wpc/sam.c at the pinned revision (`grep -c "CORE_CLONEDEF(potc," src/wpc/sam.c` -> 27).
DRIVER_IDS = (
	"potc_600af",
	"potc_108as",
	"potc_109ai",
	"potc_109as",
	"potc_109gf",
	"potc_110af",
	"potc_110ai",
	"potc_110gf",
	"potc_111as",
	"potc_113af",
	"potc_113ai",
	"potc_113as",
	"potc_113gf",
	"potc_115af",
	"potc_115ai",
	"potc_115as",
	"potc_115gf",
	"potc_300af",
	"potc_300ai",
	"potc_300al",
	"potc_300gf",
	"potc_400af",
	"potc_400ai",
	"potc_400al",
	"potc_400gf",
	"potc_600ai",
	"potc_600as",
	"potc_600gf",
)

DRIVER_NOTE_PARENT = (
	"PinMAME's clone-tree parent and this definition's reference driver for address semantics. It "
	"is the 2008 V6.0 English/French firmware, not the 2006 production firmware; every potc_* "
	"driver shares the one static potcGameData struct produced by sam.c's INITGAME macro, so the "
	"choice of parent carries no controller-address, polarity, or playfield consequence. This is "
	"also the driver the retained known-working table binds (Const cGameName=\"potc_600af\") and "
	"the only one for which sam.c sets a fast-flip watch address (samlocals.fastflipaddr = "
	"0x0105a7fe for any driver whose short name starts potc_600)."
)


def _firmware_note(version: str, languages: str, year: str) -> str:
	return (
		f"Stern {version} {languages} game ROM for the same physical machine, dated {year} in the "
		"pinned catalog. It shares the one static potcGameData struct with every other potc_* "
		"driver, so no controller address, switch polarity, lamp, solenoid, or playfield fact "
		"differs from the reference driver."
	)


DRIVER_COMPATIBILITY: dict[str, tuple[str, str]] = {"potc_600af": ("identical", DRIVER_NOTE_PARENT)}
for _driver_id, _version, _languages, _year in (
	("potc_108as", "V1.08", "English/Spanish", "2006"),
	("potc_109ai", "V1.09", "English/Italian", "2006"),
	("potc_109as", "V1.09", "English/Spanish", "2006"),
	("potc_109gf", "V1.09", "German/French", "2006"),
	("potc_110af", "V1.10", "English/French", "2006"),
	("potc_110ai", "V1.10", "English/Italian", "2006"),
	("potc_110gf", "V1.10", "German/French", "2006"),
	("potc_111as", "V1.11", "English/Spanish", "2006"),
	("potc_113af", "V1.13", "English/French", "2006"),
	("potc_113ai", "V1.13", "English/Italian", "2006"),
	("potc_113as", "V1.13", "English/Spanish", "2006"),
	("potc_113gf", "V1.13", "German/French", "2006"),
	("potc_115af", "V1.15", "English/French", "2006"),
	("potc_115ai", "V1.15", "English/Italian", "2006"),
	("potc_115as", "V1.15", "English/Spanish", "2006"),
	("potc_115gf", "V1.15", "German/French", "2006"),
	("potc_300af", "V3.00", "English/French", "2007"),
	("potc_300ai", "V3.00", "English/Italian", "2007"),
	("potc_300al", "V3.00", "English/Spanish", "2007"),
	("potc_300gf", "V3.00", "German/French", "2007"),
	("potc_400af", "V4.00", "English/French", "2007"),
	("potc_400ai", "V4.00", "English/Italian", "2007"),
	("potc_400al", "V4.00", "English/Spanish", "2007"),
	("potc_400gf", "V4.00", "German/French", "2007"),
	("potc_600ai", "V6.0", "English/Italian", "2008"),
	("potc_600as", "V6.0", "English/Spanish", "2008"),
	("potc_600gf", "V6.0", "German/French", "2008"),
):
	DRIVER_COMPATIBILITY[_driver_id] = ("identical", _firmware_note(_version, _languages, _year))

# --- Printed switch matrix -----------------------------------------------------------------------
# Transcribed from PDF page 6 (printed "DR. 4"), SWITCH MATRIX GRID (#1-#64).
# address -> (in-cell annotation, label, part number, printed location)
NOT_USED = ("", "", "", "")
SWITCH_MATRIX: dict[int, tuple[str, str, str, str]] = {
	1: ("", "Left Lane", "500-6227-04", "below playfield"),
	2: ("", "Right Lane", "500-6227-04", "below playfield"),
	3: ("(OPTO PAIR)", "Hit Chest", "500-6775-00", "above playfield"),
	4: ("(OPTO PAIR)", "Plunder Exit", "500-6775-00", "above playfield"),
	5: NOT_USED,
	6: ("", "Chest Lock", "180-5119-02", "above playfield"),
	7: NOT_USED,
	8: ("", "Left Orbit", "180-5087-00", "above playfield"),
	9: ("« D.O.T.S. »", "Top Center VUK", "180-5209-00", "below playfield"),
	10: ("", "Left Ramp Enter", "180-5087-00", "above playfield"),
	11: ("(OPTO PAIR)", "Plunder Enter", "500-6775-00", "above playfield"),
	12: ("", "Left Top Lane", "180-5183-00", "above playfield"),
	13: ("", "Middle Top Lane", "180-5087-00", "above playfield"),
	14: ("", "Right Top Lane", "180-5183-00", "above playfield"),
	15: ("CABINET", "Tournament Start", "180-5119-03", "Front Molding"),
	16: ("CABINET", "Start Button", "180-5174-00", "In Cabinet"),
	17: NOT_USED,
	18: ("(4-BALL)", "Trough #4 (L)", "180-5119-02", "below playfield"),
	19: ("(4-BALL)", "Trough #3", "180-5119-02", "below playfield"),
	20: ("(4-BALL)", "Trough #2", "180-5119-02", "below playfield"),
	# The manual leaves the location cell blank on these two rows: the transmitter and receiver part
	# numbers occupy it. The other three switches of the same trough print "below playfield".
	21: ("(VUK OPTO)", "Trough #1 (R)", "515-0173-00 (TX) / 515-0174-00 (RX)", ""),
	22: ("(STACK OPTO)", "Trough Jam", "515-0173-00 (TX) / 515-0174-00 (RX)", ""),
	23: ("", "Shooter Lane", "180-5157-00", "above playfield"),
	24: ("", "Left Outlane", "500-6227-04", "below playfield"),
	25: ("", "Left Inlane", "500-6227-04", "below playfield"),
	26: ("", "Left Sling", "180-5054-00", "2 per Asm."),
	27: ("", "Right Sling", "180-5054-00", "2 per Asm."),
	28: ("", "Right Inlane", "500-6227-04", "below playfield"),
	29: ("", "Right Outlane", "500-6227-04", "below playfield"),
	30: ("", "Left Bumper", "180-5015-04", "below playfield"),
	31: ("", "Right Bumper", "180-5015-04", "below playfield"),
	32: ("", "Bottom Bumper", "180-5015-04", "below playfield"),
	33: NOT_USED,
	34: NOT_USED,
	35: NOT_USED,
	36: NOT_USED,
	37: ('YEL 1-1/2" S/U', "L. Bonus Treasure", "515-6027-06", "below playfield"),
	38: NOT_USED,
	39: ('YEL 1-1/2" S/U', "R. Bonus Treasure", "515-6027-06", "below playfield"),
	40: NOT_USED,
	41: NOT_USED,
	42: ("", "Plunder 1", "180-5133-02", "above playfield"),
	43: ("", "Plunder 2", "180-5133-02", "above playfield"),
	44: ("", "Plunder 3", "180-5133-02", "above playfield"),
	45: ("", "Plunder 4", "180-5133-02", "above playfield"),
	46: ("", "Plunder 5", "180-5133-02", "above playfield"),
	47: ("", "Plunder 6", "180-5133-02", "above playfield"),
	48: NOT_USED,
	49: NOT_USED,
	50: ('GRN 1/2" S/U', "Pirate 1 (Left)", "515-7581-04", "below playfield"),
	51: ('GRN 1/2" S/U', "Pirate 2", "515-7581-04", "below playfield"),
	52: ('GRN 1/2" S/U', "Pirate 3", "515-7581-04", "below playfield"),
	53: ('GRN 1/2" S/U', "Pirate 4", "515-7581-04", "below playfield"),
	54: ('GRN 1/2" S/U', "Pirate 5", "515-7581-04", "below playfield"),
	55: ('GRN 1/2" S/U', "Pirate 6 (Right)", "515-7581-04", "below playfield"),
	56: ("", "Pop Eject", "180-5186-01", "below playfield"),
	57: ("", "Jack Scoop Exit", "180-5210-00", "above playfield"),
	58: ("", "Right Orbit", "180-5087-00", "above playfield"),
	59: NOT_USED,
	60: ("(OPTO PAIR)", "Skill Hole Made", "500-6775-00", "above playfield"),
	61: ("(OPTO PAIR)", "Ship Made", "500-6775-00", "above playfield"),
	62: ("", "Ship Fully Sunk", "180-5189-00", "below playfield"),
	63: ("", "Ship Home", "180-5189-00", "below playfield"),
	64: NOT_USED,
}

# Switch construction is recorded only where the manual states it. The seven addresses below are
# the exhaustive result of sweeping all 64 printed cells for both of this page's own opto cues --
# an in-cell "(OPTO PAIR)"/"(VUK OPTO)"/"(STACK OPTO)" annotation, and a transmitter/receiver part
# number pair in place of a mechanical switch part. This page carries no shaded-cell legend at all,
# and no cell on it is shaded.
OPTO_SWITCHES = (3, 4, 11, 21, 22, 60, 61)

# Return (row) lines, CPU/Sound Board: return index 1-16 -> (IC, wire, connector).
SWITCH_RETURNS = {
	1: ("IC-U22A", "White-Brown", "J6-P9"),
	2: ("IC-U22B", "White-Red", "J6-P8"),
	3: ("IC-U22C", "White-Orange", "J6-P7"),
	4: ("IC-U22D", "White-Yellow", "J6-P6"),
	5: ("IC-U15A", "White-Green", "J6-P5"),
	6: ("IC-U15B", "White-Blue", "J6-P3"),
	7: ("IC-U15C", "White-Violet", "J6-P2"),
	8: ("IC-U15D", "White-Gray", "J6-P1"),
	9: ("IC-U35A", "Tan-Black", "J12-P9"),
	10: ("IC-U35B", "Tan-Red", "J12-P8"),
	11: ("IC-U35C", "Tan-Orange", "J12-P7"),
	12: ("IC-U35D", "Tan-Yellow", "J12-P6"),
	13: ("IC-U40A", "Tan-Green", "J12-P4"),
	14: ("IC-U40B", "Tan-Blue", "J12-P3"),
	15: ("IC-U40C", "Tan-Violet", "J12-P2"),
	16: ("IC-U40D", "Tan-White", "J12-P1"),
}

# Drive (column) lines: drive index 1-4 -> (transistor, wire, connector).
SWITCH_DRIVES = {
	1: ("Q1", "Green-Brown", "J1-P1"),
	2: ("Q2", "Green-Red", "J1-P3"),
	3: ("Q3", "Green-Orange", "J1-P4"),
	4: ("Q4", "Green-Yellow", "J1-P5"),
}

# --- Printed dedicated switches ------------------------------------------------------------------
# public address -> (printed D-number, label, part number, printed location, IC, wire, connector,
#                    availability, switch_type or "", roles)
DEDICATED_SWITCHES: dict[int, tuple[str, str, str, str, str, str, str, str, str, tuple[str, ...]]] = {
	-7: ("D-17", "Tilt Pendulum (Plumb Bob)", "", "See Sec. 4, Chp. 1, Pg. 47 for cab. parts", "IC-41", "Light Green-Brown", "J13-P1", "used", "tilt", ("cabinet.tilt",)),
	-6: ("D-18", "Slam Tilt", "502-5032-00", "Optional Kit", "IC-41", "Light Green-Red", "J13-P3", "optional", "tilt", ("cabinet.slam-tilt",)),
	-5: ("D-19", "Ticket Notch", "180-5119-02", "Below P/F", "IC-41", "Light Green-Orange", "J13-P4", "optional", "", ("cabinet.ticket-notch",)),
	-4: ("D-20", "Not Used", "", "", "IC-41", "Light Green-Yellow", "J13-P5", "unused", "", ()),
	-3: ("D-21", "Back (Green Button)", "180-5192-04", "Coin Door", "IC-41", "Light Green-Black", "J13-P6", "used", "button", ("cabinet.service.back",)),
	-2: ("D-22", "Minus (Red Button)", "180-5192-02", "Coin Door", "IC-41", "Light Green-Blue", "J13-P7", "used", "button", ("cabinet.service.minus",)),
	-1: ("D-23", "Plus (Red Button)", "180-5192-02", "Coin Door", "IC-41", "Light Green-Violet", "J13-P8", "used", "button", ("cabinet.service.plus",)),
	0: ("D-24", "Select (Black Button)", "180-5192-00", "Coin Door", "IC-41", "Light Green-Gray", "J13-P9", "used", "button", ("cabinet.service.select",)),
	65: ("D-1", "Left Coin Slot", "180-5204-00", "Coin Door", "IC-U02", "Pink-Brown", "J2-P2", "used", "", ("cabinet.coin.1",)),
	66: ("D-2", "Center Coin Slot/DBA", "180-5204-00", "Coin Door", "IC-U02", "Pink-Red", "J2-P3", "used", "", ("cabinet.coin.2",)),
	67: ("D-3", "Right Coin Slot", "180-5204-00", "Coin Door", "IC-U02", "Pink-Orange", "J2-P4", "used", "", ("cabinet.coin.3",)),
	68: ("D-4", "Fourth Coin Slot", "180-5204-00", "Coin Door", "IC-U02", "Pink-Yellow", "J2-P6", "used", "", ("cabinet.coin.4",)),
	69: ("D-5", "Fifth Coin Slot", "", 'printed "IF USED" with no part number', "IC-U02", "Pink-Green", "J2-P7", "optional", "", ("cabinet.coin.5",)),
	70: ("D-6", "Not Used", "", "", "IC-U02", "Pink-Blue", "J2-P8", "unused", "", ()),
	71: ("D-7", "L. Post Save (UK Only)", "180-5160-01", "Cabinet Side", "IC-U02", "Pink-Violet", "J2-P9", "optional", "button", ("cabinet.post-save.left-uk",)),
	72: ("D-8", "R. Post Save (UK Only)", "180-5160-01", "Cabinet Side", "IC-U02", "Pink-Gray", "J2-P10", "optional", "button", ("cabinet.post-save.right-uk",)),
	81: ("D-12", "Right Flipper E.O.S.", "180-5149-00", "Flipper Asm.", "IC-U04", "Gray-Yellow", "J3-P5", "used", "", ("cabinet.flipper.right-eos",)),
	82: ("D-11", "R. Flipper Button", "180-5160-01", "Cabinet Side", "IC-U04", "Gray-Orange", "J3-P4", "used", "button", ("cabinet.flipper.right-button",)),
	83: ("D-10", "Left Flipper E.O.S.", "180-5149-00", "Flipper Asm.", "IC-U04", "Gray-Red", "J3-P2", "used", "", ("cabinet.flipper.left-eos",)),
	84: ("D-9", "Left Flipper Button", "180-5160-01", "Cabinet Side", "IC-U04", "Gray-Brown", "J3-P1", "used", "button", ("cabinet.flipper.left-button",)),
	85: ("D-16", "Not Used", "", "", "IC-U04", "Gray-Black", "J3-P9", "unused", "", ()),
	86: ("D-15", "Not Used", "", "", "IC-U04", "Gray-Violet", "J3-P8", "unused", "", ()),
	87: ("D-14", "Not Used", "", "", "IC-U04", "Gray-Blue", "J3-P7", "unused", "", ()),
	88: ("D-13", "Not Used", "", "", "IC-U04", "Gray-Green", "J3-P6", "unused", "", ()),
}

FLIPPER_COLUMN_BITS = {
	81: "CORE_SWLRFLIPEOSBIT (0x01)",
	82: "CORE_SWLRFLIPBUTBIT (0x02)",
	83: "CORE_SWLLFLIPEOSBIT (0x04)",
	84: "CORE_SWLLFLIPBUTBIT (0x08)",
	85: "CORE_SWURFLIPEOSBIT (0x10)",
	86: "CORE_SWURFLIPBUTBIT (0x20)",
	87: "CORE_SWULFLIPEOSBIT (0x40)",
	88: "CORE_SWULFLIPBUTBIT (0x80)",
}

# --- Printed Coils Detailed Chart Table ----------------------------------------------------------
# address -> (label, transistor, power wire, power connection, volts, control wire,
#             control connection, coil/bulb part, output kind, quantity, availability)
SOLENOIDS: dict[int, tuple[str, str, str, str, float, str, str, str, str, int, str]] = {
	1: ("Trough Up-Kicker", "Q1", "Yellow-Violet", "J10-P9/10", 50.0, "Brown-Black", "J8-P1", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	2: ("Auto Launch", "Q2", "Yellow-Violet", "J10-P9/10", 50.0, "Brown-Red", "J8-P3", "23-800 / 090-5001-00-ND", "coil", 1, "used"),
	3: ("Top Center VUK", "Q3", "Yellow-Violet", "J10-P9/10", 50.0, "Brown-Orange", "J8-P4", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	4: ("Chest Lid", "Q4", "Yellow-Violet", "J10-P9/10", 50.0, "Brown-Yellow", "J8-P5", "27-1400 / 511-5031-00", "coil", 1, "used"),
	5: ("Raise Sails", "Q5", "Yellow-Violet", "J10-P9/10", 50.0, "Brown-Green", "J8-P6", "26-1200 / 500-7051-00", "coil", 1, "used"),
	6: ("Plunder Disk Motor", "Q6", "Brown", "J10-P9/10", 20.0, "Brown-Blue", "J8-P7", "Motor 12V / 511-5024-04", "motor", 1, "used"),
	7: ("Not Used", "Q7", "", "J10-P9/10", 0.0, "Brown-Violet", "J8-P8", "", "coil", 1, "unused"),
	8: ("Not Used", "Q8", "", "J10-P9/10", 0.0, "Brown-Gray", "J8-P9", "", "coil", 1, "unused"),
	9: ("Left Bumper", "Q9", "Yellow-Violet", "J10-P9/10", 50.0, "Blue-Brown", "J9-P1", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	10: ("Right Bumper", "Q10", "Yellow-Violet", "J10-P9/10", 50.0, "Blue-Red", "J9-P2", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	11: ("Bottom Bumper", "Q11", "Yellow-Violet", "J10-P9/10", 50.0, "Blue-Orange", "J9-P4", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	12: ("Not Used", "Q12", "", "J10-P9/10", 0.0, "Blue-Yellow", "J9-P5", "", "coil", 1, "unused"),
	13: ("Not Used", "Q13", "", "J10-P9/10", 0.0, "Blue-Green", "J9-P6", "", "coil", 1, "unused"),
	14: ("Not Used", "Q14", "", "J10-P6/7", 0.0, "Blue-Black", "J9-P7", "", "coil", 1, "unused"),
	15: ("Left Flipper", "Q15", "Gray-Yellow to 3A Fuse to Red-Yellow", "J10-P6/7", 50.0, "Orange-Gray", "J9-P8", "23-1100 / 090-5030-00-ND", "coil", 1, "used"),
	16: ("Right Flipper", "Q16", "Blue-Yellow to 3A Fuse to Red-Yellow", "J10-P6/7", 50.0, "Orange-Violet", "J9-P9", "23-1100 / 090-5030-00-ND", "coil", 1, "used"),
	17: ("Not Used", "Q17", "", "J7-P1", 0.0, "Violet-Brown", "J7-P2", "", "coil", 1, "unused"),
	18: ("Pop Bumper Eject", "Q18", "Brown", "J7-P1", 20.0, "Violet-Red", "J7-P3", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	19: ("Chest Kicker", "Q19", "Brown", "J7-P1", 20.0, "Violet-Orange", "J7-P4", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	20: ("Flash: Chest", "Q20", "Orange", "J7-P1", 20.0, "Violet-White", "J7-P6", "#89 Bulb / 165-5000-89", "flasher", 1, "used"),
	21: ("Ship Motor", "Q21", "Brown", "J7-P1", 20.0, "Violet-Green", "J7-P7", "Motor 24V / 041-5101-00", "motor", 1, "used"),
	22: ("Flash: Rear Center", "Q22", "Orange", "J7-P1", 20.0, "Violet-Blue", "J7-P8", "#89 Bulb / 165-5000-89", "flasher", 2, "used"),
	23: ("Plunder Pin", "Q23", "Brown", "J7-P1", 20.0, "Violet-Black", "J7-P9", "22-900 / 090-5020-20-ND", "coil", 1, "used"),
	24: ("Optional Coil", "Q24", "Red", "J16-P4>8", 5.0, "Violet-Gray", "J7-P10", "Opt. 5v", "coil", 1, "optional"),
	25: ("Left Slingshot", "Q25", "Brown", "J6-P10", 20.0, "Black-Brown", "J6-P1", "23-800 / 090-5001-00-ND", "coil", 1, "used"),
	26: ("Right Slingshot", "Q26", "Brown", "J6-P10", 20.0, "Black-Red", "J6-P2", "23-800 / 090-5001-00-ND", "coil", 1, "used"),
	27: ("Ship Motor Relay", "Q27", "Brown", "J6-P10", 20.0, "Black-Orange", "J6-P3", "Relay PCB / 511-5024-03", "relay", 1, "used"),
	28: ("Lower Sails Latch", "Q28", "Brown", "J6-P10", 20.0, "Black-Yellow", "J6-P4", "29-1400 / 500-7052-00", "coil", 1, "used"),
	29: ("Ship Pin (Up Post)", "Q29", "Brown", "J6-P10", 20.0, "Black-Green", "J6-P5", "26-1200 / 090-5044-00-ND", "coil", 1, "used"),
	30: ("Flash: Back Right", "Q30", "Orange", "J6-P10", 20.0, "Black-Blue", "J6-P6", "#89 Bulb / 165-5000-89", "flasher", 3, "used"),
	31: ("Flash: Back Left", "Q31", "Orange", "J6-P10", 20.0, "Black-Violet", "J6-P7", "#89 Bulb / 165-5000-89", "flasher", 1, "used"),
	32: ("Flash: Ship", "Q32", "Orange", "J6-P10", 20.0, "Black-Gray", "J6-P8", "#89 Bulb / 165-5000-89", "flasher", 1, "used"),
}

# The manual's own "Test Flash Lamps" note names this game's flashers explicitly:
# "Flashers tested are all Flash Lamps located between Q1-Q32 (This Game: Q20, Q22, Q30, Q31 &
# Q32)". Pinned sam.c's own potc block declares exactly the same five addresses as #89 bulbs
# (CORE_MODOUT_BULB_89_20V_DC_WPC at SOL0+20-1, SOL0+22-1 and SOL0+30-1 for a run of 3).
FLASHER_ADDRESSES = (20, 22, 30, 31, 32)

# --- Printed Lamp Matrix Grid --------------------------------------------------------------------
# address -> (label, printed bulb type, part number)
LAMPS: dict[int, tuple[str, str, str]] = {
	1: ("Start Button", "#555 Clear", "165-5002-00"),
	2: ("Tournament Start Button", "#CM86 Clr.", "165-5103-00"),
	3: ("Shoot Again", "#555 Clear", "165-5002-00"),
	4: ("Left Outlane", "#555 Clear", "165-5002-00"),
	5: ("Left Inlane", "#555 Clear", "165-5002-00"),
	6: ("Right Inlane", "#555 Clear", "165-5002-00"),
	7: ("Right Outlane", "#555 Clear", "165-5002-00"),
	8: ("Four Winds", "#555 Clear", "165-5002-00"),
	9: ("Compass - North", "#555 Clear", "165-5002-00"),
	10: ("Compass - Sword Fight", "#555 Clear", "165-5002-00"),
	11: ("Compass - Davy Jones", "#555 Clear", "165-5002-00"),
	12: ("Compass - East", "#555 Clear", "165-5002-00"),
	13: ("Compass - Heart SJP", "#555 Clear", "165-5002-00"),
	14: ("Compass - All Pirates", "#555 Clear", "165-5002-00"),
	15: ("Compass - South", "#555 Clear", "165-5002-00"),
	16: ("Compass - Port Royal", "#555 Clear", "165-5002-00"),
	17: ("Compass - Kraken", "#555 Clear", "165-5002-00"),
	18: ("Compass - West", "#555 Clear", "165-5002-00"),
	19: ("Compass - Jack/Monkey", "#555 Clear", "165-5002-00"),
	20: ("Compass - Ship Sunk", "#555 Clear", "165-5002-00"),
	21: ("Right Bonus Treasure", "#555 Clear", "165-5002-00"),
	22: ("Left Side Lane Arrow", "#555 Clear", "165-5002-00"),
	23: ("Ship Jackpot", "#555 Clear", "165-5002-00"),
	24: ("(H)eart", "LED on PCB", "520-5258-00"),
	25: ("Davy Jones", "#555 Clear", "165-5002-00"),
	26: ("Timed Ball Lock", "#555 Clear", "165-5002-00"),
	27: ("Pop Bumper", "#555 LED", "112-5024-08"),
	28: ("Left Orbit Arrow", "#555 Clear", "165-5002-00"),
	29: ("Left Orbit Jackpot", "#555 Clear", "165-5002-00"),
	30: ("Right Orbit Jackpot", "#555 Clear", "165-5002-00"),
	31: ("Right Special", "#555 Clear", "165-5002-00"),
	32: ("H(e)art", "LED on PCB", "520-5258-00"),
	33: ("Backpanel #1 (L)", "#44 Red", "165-5053-02-HF"),
	34: ("Backpanel #2", "#44 Red", "165-5053-02-HF"),
	35: ("Backpanel #3", "#44 Red", "165-5053-02-HF"),
	36: ("Backpanel #4", "#44 Red", "165-5053-02-HF"),
	37: ("Backpanel #5", "#44 Red", "165-5053-02-HF"),
	38: ("Backpanel #6", "#44 Red", "165-5053-02-HF"),
	39: ("Backpanel #7 (R)", "#44 Red", "165-5053-02-HF"),
	40: ("He(a)rt", "LED on PCB", "520-5258-00"),
	41: ("Pirate 6", "#555 Clear", "165-5002-00"),
	42: ("Left Special", "#555 Clear", "165-5002-00"),
	43: ("Left Bonus Treasure", "#555 Clear", "165-5002-00"),
	44: ("Chest Arrow", "#555 Clear", "165-5002-00"),
	45: ("Left Ramp Arrow", "#555 Clear", "165-5002-00"),
	46: ("Port Royal", "#555 Clear", "165-5002-00"),
	47: ("Tortuga", "#555 Clear", "165-5002-00"),
	48: ("Hea(r)t", "LED on PCB", "520-5258-00"),
	49: ("Pirate 1", "#555 Clear", "165-5002-00"),
	50: ("Pirate 2", "#555 Clear", "165-5002-00"),
	51: ("Pirate 3", "#555 Clear", "165-5002-00"),
	52: ("Pirate 4", "#555 Clear", "165-5002-00"),
	53: ("Pirate 5", "#555 Clear", "165-5002-00"),
	54: ("Heart Multiball", "#555 Clear", "165-5002-00"),
	55: ("Ke(y)", "#555 Clear", "165-5002-00"),
	56: ("Hear(t)", "LED on PCB", "520-5258-00"),
	57: ("Scoop Arrow", "#555 Clear", "165-5002-00"),
	58: ("(J)ack", "#555 Clear", "165-5002-00"),
	59: ("J(a)ck", "#555 Clear", "165-5002-00"),
	60: ("Ja(c)k", "#555 Clear", "165-5002-00"),
	61: ("Jac(k)", "#555 Clear", "165-5002-00"),
	62: ("(K)ey", "Lamp Note 1 (White LED Module, wedge base #555 style)", "112-5024-08"),
	63: ("K(e)y", "#555 Clear", "165-5002-00"),
	64: ("Heart 1 (double-dot)", "LEDs / PCB", "520-5258-00"),
	65: ("Ship Arrow", "#555 Clear", "165-5002-00"),
	66: ("Interceptor", "#555 Clear", "165-5002-00"),
	67: ("Dauntless", "#44 Blue", "165-5053-05-HF"),
	68: ("Edinburgh Trader", "#44 Blue", "165-5053-05-HF"),
	69: ("Terpsichore", "#555 Clear", "165-5002-00"),
	70: ("Award Compass", "Lamp Note 1 (White LED Module, wedge base #555 style)", "112-5024-08"),
	71: ("Right Orbit Arrow", "#555 Clear", "165-5002-00"),
	72: ("Heart 2 (double-dot)", "LEDs / PCB", "520-5258-00"),
	73: ("Kraken Mouth", "#44 Red", "165-5053-02-HF"),
	74: ("Center Arrow", "#555 Clear", "165-5002-00"),
	75: ("Center Jackpot", "#44 Blue", "165-5053-05-HF"),
	76: ("Extra Ball", "#44 Blue", "165-5053-05-HF"),
	77: ("Liars Dice", "#555 Clear", "165-5053-05-HF"),
	78: ("Left Top Lane", "#44 Green", "165-5053-04-HF"),
	79: ("Middle Top Lane", "#44 Green", "165-5053-04-HF"),
	80: ("Right Top Lane", "#44 Green", "165-5053-04-HF"),
}

# Printed bulb quantities where the matrix cell states one: "FOUR WINDS (X2)", "POP BUMPER (X3)".
LAMP_QUANTITIES = {8: 2, 27: 3}

# Back-panel lamps, per printed page 91 (Back Panel Assembly): seven #44 Red sockets labelled
# LP. 33 - LP. 39 (ITEM 3, QTY. 7) and three #44 Green sockets labelled LAMP 78 - LAMP 80
# (ITEM 4, QTY. 3), which is also the "10 LAMPS (7 RED / 3 GREEN) LOCATED ON THE BACK PANEL"
# the Lamp Locations page counts in its own back-panel inset.
BACK_PANEL_LAMPS = (33, 34, 35, 36, 37, 38, 39, 78, 79, 80)

# Cabinet button lamps: neither is drawn on the Lamp Locations playfield plan.
CABINET_LAMPS = (1, 2)

# Column (drive) lines of the lamp matrix: 1-8 -> (IC, wire, connector).
LAMP_COLUMNS = {
	1: ("IC-U17", "Yellow-Brown", "J13-P9"),
	2: ("IC-U16", "Yellow-Red", "J13-P8"),
	3: ("IC-U15", "Yellow-Orange", "J13-P7"),
	4: ("IC-U14", "Yellow-Black", "J13-P6"),
	5: ("IC-U13", "Yellow-Green", "J13-P5"),
	6: ("IC-U12", "Yellow-Blue", "J13-P4"),
	7: ("IC-U11", "Yellow-Violet", "J13-P3"),
	8: ("IC-U10", "Yellow-Gray", "J13-P1"),
}

# Row (ground) lines of the lamp matrix: 1-10 -> (transistor, wire, connector).
LAMP_ROWS = {
	1: ("Q33", "Ground Red-Brown", "J12-P1"),
	2: ("Q34", "Ground Red-Black", "J12-P2"),
	3: ("Q35", "Ground Red-Orange", "J12-P3"),
	4: ("Q36", "Ground Red-Yellow", "J12-P4"),
	5: ("Q37", "Ground Red-Green", "J12-P5"),
	6: ("Q38", "Ground Red-Blue", "J12-P6"),
	7: ("Q39", "Ground Red-Violet", "J12-P8"),
	8: ("Q40", "Ground Red-Gray", "J12-P9"),
	9: ("Q41", "Ground Red-White", "J12-P10"),
	10: ("Q42", "Ground Red", "J12-P11"),
}

# --- Normalized positions from the retained table -----------------------------------------------
# Every value below is object_centre / bounds, rounded to six places, taken from the retained
# extraction and reproduced in
# external:pinmame-review-artifacts/pirates-of-the-caribbean-2006/vpx-geometry.txt.
SWITCH_POSITIONS: dict[int, tuple[float, float]] = {
	1: (0.060155, 0.532107),
	2: (0.936788, 0.558887),
	3: (0.680835, 0.452586),
	4: (0.195862, 0.158359),
	6: (0.852067, 0.343775),
	8: (0.073155, 0.369644),
	9: (0.481739, 0.041539),
	10: (0.141321, 0.288959),
	11: (0.064984, 0.093045),
	12: (0.652119, 0.162314),
	13: (0.737736, 0.146153),
	14: (0.821797, 0.162531),
	18: (0.878522, 0.867797),
	19: (0.878522, 0.867797),
	20: (0.878522, 0.867797),
	21: (0.878522, 0.867797),
	22: (0.878522, 0.867797),
	23: (0.938619, 0.894553),
	24: (0.057971, 0.70361),
	25: (0.133489, 0.744156),
	26: (0.2243, 0.736206),
	27: (0.686166, 0.735225),
	28: (0.77457, 0.743852),
	29: (0.847818, 0.751321),
	30: (0.634287, 0.218747),
	31: (0.843513, 0.205462),
	32: (0.764428, 0.289786),
	37: (0.11911, 0.539315),
	39: (0.845732, 0.556299),
	42: (0.037871, 0.095256),
	43: (0.032115, 0.052009),
	44: (0.088183, 0.018027),
	45: (0.183567, 0.008208),
	46: (0.270231, 0.027079),
	47: (0.307537, 0.066323),
	50: (0.146317, 0.37685),
	51: (0.270067, 0.347999),
	52: (0.40261, 0.318395),
	53: (0.504065, 0.387239),
	54: (0.626928, 0.44996),
	55: (0.749608, 0.46683),
	56: (0.557229, 0.277936),
	57: (0.560722, 0.392456),
	58: (0.891305, 0.421608),
	60: (0.736947, 0.080391),
	61: (0.295276, 0.261411),
	62: (0.358456, 0.192749),
	63: (0.358456, 0.192749),
	81: (0.620861, 0.844229),
	83: (0.28719, 0.844229),
}

# The retained table object each switch placement was taken from, and, where the placement is a
# documented projection onto the switch's own mechanism assembly rather than the switch's own
# object, why.
SWITCH_OBJECTS = {
	1: "sw1 (Trigger)",
	2: "sw2 (Trigger)",
	3: "sw3 (Trigger)",
	4: "sw4 (Trigger)",
	6: "sw6 (Trigger)",
	8: "sw8 (Gate)",
	9: "sw9 (Kicker)",
	10: "sw10 (Gate)",
	11: "sw11 (Gate)",
	12: "sw12 (Trigger)",
	13: "sw13 (Gate)",
	14: "sw14 (Trigger)",
	18: "BallRelease (Kicker)",
	19: "BallRelease (Kicker)",
	20: "BallRelease (Kicker)",
	21: "BallRelease (Kicker)",
	22: "BallRelease (Kicker)",
	23: "sw23 (Trigger)",
	24: "sw24 (Trigger)",
	25: "sw25 (Trigger)",
	26: "LeftSlingShot (Wall)",
	27: "RightSlingShot (Wall)",
	28: "sw28 (Trigger)",
	29: "sw29 (Trigger)",
	30: "Bumper2 (Bumper)",
	31: "Bumper3 (Bumper)",
	32: "Bumper1 (Bumper)",
	37: "sw37 (HitTarget)",
	39: "sw39 (HitTarget)",
	42: "sw42 (HitTarget)",
	43: "sw43 (HitTarget)",
	44: "sw44 (HitTarget)",
	45: "sw45 (HitTarget)",
	46: "sw46 (HitTarget)",
	47: "sw47 (HitTarget)",
	50: "sw50 (HitTarget)",
	51: "sw51 (HitTarget)",
	52: "sw52 (HitTarget)",
	53: "sw53 (HitTarget)",
	54: "sw54 (HitTarget)",
	55: "sw55 (HitTarget)",
	56: "sw56 (Kicker)",
	57: "SW57 (Trigger)",
	58: "sw58 (Gate)",
	60: "sw60 (Trigger)",
	61: "sw61 (Trigger)",
	62: "ship (Primitive)",
	63: "ship (Primitive)",
	81: "RightFlipper (Flipper)",
	83: "LeftFlipper (Flipper)",
}

SWITCH_PROJECTIONS = {
	18: "Trough position #4; the four trough position switches and the trough jam opto have no individual objects in the retained table, which models the whole 4-ball trough through one cvpmBallStack instance. Projected onto the trough's own ball-release kicker (BallRelease), the object bsTROUGH.InitKick names.",
	19: "Trough position #3; projected onto the trough's own ball-release kicker for the same reason as address 18.",
	20: "Trough position #2; projected onto the trough's own ball-release kicker for the same reason as address 18.",
	21: "Trough position #1; projected onto the trough's own ball-release kicker for the same reason as address 18.",
	22: "Trough jam / stack opto, which sits in the trough's own exit path; the retained script asserts it with vpmTimer.PulseSw 22 from inside SolTrough rather than through an object. Projected onto the trough's own ball-release kicker.",
	62: "Ship Fully Sunk; the retained script derives it from the ship mechanism's own software position counter (ShipTimer_Timer, ShipPos 0-3) with no sensor object anywhere in the table. Projected onto the ship assembly's own Primitive.",
	63: "Ship Home; derived from the same software position counter. Projected onto the ship assembly's own Primitive.",
	81: "Right flipper end-of-stroke switch, part 180-5149-00 on the Flipper Asm.; projected onto the right flipper assembly's own object, which is also where public solenoid 16 is placed.",
	83: "Left flipper end-of-stroke switch, part 180-5149-00 on the Flipper Asm.; projected onto the left flipper assembly's own object, which is also where public solenoid 15 is placed.",
}

SOLENOID_POSITIONS: dict[int, tuple[float, float]] = {
	1: (0.878522, 0.867797),
	2: (0.940617, 0.982041),
	3: (0.481739, 0.041539),
	4: (0.783613, 0.343387),
	5: (0.352074, 0.210725),
	6: (0.168845, 0.070088),
	9: (0.634287, 0.218747),
	10: (0.843513, 0.205462),
	11: (0.764428, 0.289786),
	15: (0.28719, 0.844229),
	16: (0.620861, 0.844229),
	18: (0.557229, 0.277936),
	19: (0.885683, 0.357643),
	20: (0.636135, 0.324872),
	21: (0.358456, 0.192749),
	23: (0.185452, 0.133558),
	25: (0.2243, 0.736206),
	26: (0.686166, 0.735225),
	27: (0.358456, 0.192749),
	28: (0.352074, 0.210725),
	29: (0.28441, 0.30521),
	31: (0.060078, 0.166915),
	32: (0.177401, 0.215803),
}

SOLENOID_OBJECTS = {
	1: "BallRelease (Kicker)",
	2: "Plunger (Plunger)",
	3: "sw9 (Kicker)",
	4: "chest (Primitive)",
	5: "SailsUp (Wall)",
	6: "Plunder (Trigger, the turntable cvpmTurnTable drives)",
	9: "Bumper2 (Bumper)",
	10: "Bumper3 (Bumper)",
	11: "Bumper1 (Bumper)",
	15: "LeftFlipper (Flipper)",
	16: "RightFlipper (Flipper)",
	18: "sw56 (Kicker)",
	19: "ChestPin (Wall)",
	20: "F20 (Light)",
	21: "ship (Primitive)",
	23: "TortugaPost (Wall)",
	25: "LeftSlingShot (Wall)",
	26: "RightSlingShot (Wall)",
	27: "ship (Primitive)",
	28: "SailsDown (Wall)",
	29: "ShipPin (Wall)",
	31: "F31 (Light)",
	32: "F32 (Light)",
}

SOLENOID_PROJECTIONS = {
	5: "Raise Sails; the sails latch has no separate visible object, so this is projected onto the ship's own SailsUp state Wall, which SolSailsUp is the sub that drops.",
	21: "Ship Motor; a motor has no single point of action, so this is projected onto the ship assembly's own Primitive, the object SolShipMotor translates.",
	27: "Ship Motor Relay; a Relay PCB (511-5024-03) with no point of action on the playfield at all. Projected onto the ship assembly it reverses, the mechanism it belongs to. The Coil & Flash Lamp Locations page draws its callout on the playfield beside the ship motor's own callout.",
	28: "Lower Sails Latch; projected onto the ship's own SailsDown state Wall, which SolSailsDown is the sub that drops.",
}

# Lamp placements. Every entry is the deduplicated set of distinct emitter positions; where the
# retained table models one physical bulb twice as co-located render doubles, only one is kept, and
# the count of kept placements equals the manual's printed bulb quantity.
LAMP_POSITIONS: dict[int, tuple[tuple[float, float], ...]] = {
	3: ((0.455424, 0.883256),),
	4: ((0.071352, 0.662451),),
	5: ((0.133853, 0.680572),),
	6: ((0.77513, 0.679964),),
	7: ((0.835364, 0.662223),),
	8: ((0.469051, 0.690183), (0.442966, 0.691274)),
	9: ((0.45375, 0.627379),),
	10: ((0.515693, 0.644314),),
	11: ((0.562968, 0.665303),),
	12: ((0.598385, 0.691046),),
	13: ((0.562899, 0.721896),),
	14: ((0.516343, 0.742581),),
	15: ((0.456091, 0.756364),),
	16: ((0.391181, 0.74236),),
	17: ((0.345726, 0.721837),),
	18: ((0.313798, 0.690143),),
	19: ((0.34518, 0.665861),),
	20: ((0.391912, 0.644775),),
	21: ((0.779175, 0.563461),),
	22: ((0.116542, 0.600536),),
	23: ((0.367812, 0.420696),),
	24: ((0.693112, 0.382094),),
	25: ((0.36901, 0.594555),),
	26: ((0.273024, 0.519831),),
	27: ((0.63438, 0.219294), (0.843549, 0.205802), (0.765333, 0.290088)),
	28: ((0.081683, 0.376663),),
	29: ((0.126197, 0.426192),),
	30: ((0.855243, 0.443051),),
	31: ((0.896151, 0.509567),),
	32: ((0.714882, 0.384867),),
	40: ((0.739612, 0.388583),),
	41: ((0.728, 0.495011),),
	42: ((0.092708, 0.486247),),
	43: ((0.187513, 0.540853),),
	44: ((0.662145, 0.493739),),
	45: ((0.232204, 0.405993),),
	46: ((0.271623, 0.454954),),
	47: ((0.273725, 0.487214),),
	48: ((0.767152, 0.392514),),
	49: ((0.173686, 0.401491),),
	50: ((0.290923, 0.376472),),
	51: ((0.416209, 0.346295),),
	52: ((0.505682, 0.420225),),
	53: ((0.605549, 0.477826),),
	54: ((0.596859, 0.584698),),
	55: ((0.688298, 0.538174),),
	56: ((0.791692, 0.394839),),
	57: ((0.548388, 0.432206),),
	58: ((0.540978, 0.474152),),
	59: ((0.534193, 0.497785),),
	60: ((0.527871, 0.521232),),
	61: ((0.521664, 0.545996),),
	62: ((0.587537, 0.522839),),
	63: ((0.638745, 0.530752),),
	64: ((0.742505, 0.367196),),
	65: ((0.35366, 0.368068),),
	66: ((0.368208, 0.451973),),
	67: ((0.36934, 0.484611),),
	68: ((0.368439, 0.516446),),
	69: ((0.36877, 0.54765),),
	70: ((0.440373, 0.497622),),
	71: ((0.912179, 0.395015),),
	72: ((0.780789, 0.375903),),
	73: ((0.259149, 0.19539),),
	74: ((0.468807, 0.347961),),
	75: ((0.439639, 0.402098),),
	76: ((0.440141, 0.434602),),
	77: ((0.440437, 0.465663),),
}

# Retained lamp objects that were excluded as co-located render doubles of a bulb already placed.
EXCLUDED_LAMP_OBJECTS = (
	"l27D, l27e, l27f -- second Light object at each of the three pop-bumper positions already "
	"placed from l27c, l27b and l27a; the manual prints POP BUMPER (X3), so three placements, not "
	"six.",
	"l24B, l32b, l40b, l48b, l56b -- Flasher objects the retained script drives from the matching "
	"Light's own state (MiscTimer_Timer sets l24B.visible = L24.state and so on). Render doubles of "
	"the 520-5258-00 HEART LED PCB, not additional bulbs.",
	"GISpot1b, GISpot2b, GISpot3b -- Flasher render doubles the same timer drives from GISpot1-3's "
	"own state; general-illumination effects, not matrix lamps.",
	"GISpot1b3 -- a fourth spot-flasher parked at raw (-1295.169, 3806.534), far outside the "
	"playfield bounds; a table modelling leftover, excluded rather than clamped.",
)

# --- Helpers -------------------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Pirates of the Caribbean retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Pirates of the Caribbean extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Pirates of the Caribbean retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Pirates of the Caribbean retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Pirates of the Caribbean retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: tuple[tuple[float, float], ...], *source_refs: str) -> dict[str, Any]:
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


# --- Sources -------------------------------------------------------------------------------------


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the potc_* clone tree: CORE_GAMEDEF(potc, 600af, ...) plus 27 CORE_CLONEDEF(potc, ...) rows in src/wpc/sam.c",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sam.c INITGAME(potc, GEN_SAM, sam_dmd128x32, SAM_2COL, SAM_NO_AUX), whose macro "
				"expands to potcGameData = {GEN_SAM, sam_dmd128x32, {FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L), 0, "
				"2, 16, 0, 0, 0, 0, sam_getSol}} and leaves the trailing wpc/simData/sxx members at their C "
				"zero-initialization default, so wpc.invSw is all zero; grep for invSw across src/wpc/sam.c "
				"returns no assignment anywhere in the file. src/wpc/sam.c's own per-game potc_ block sets "
				"lamp 27 and lamps 24/32/40/48/56/64/72 to CORE_MODOUT_LED_STROBE_1_10MS with the comments "
				"'Bumper 3 LEDs' and 'Board 520-5258-00: H/E/A/R/T LED' plus two 'Heart Chest double LED' "
				"entries, and solenoids 20, 22 and 30-32 to CORE_MODOUT_BULB_89_20V_DC_WPC. sam.c's I/O "
				"decode maps SOL_B (0x02400021) to public solenoids 1-8, SOL_A (0x02400020) to 9-16, SOL_C "
				"(0x02400022) to 17-24 and FLSH_LMP (0x02400023) to 25-32, and its own address-decode comment "
				"documents ten lamp rows by eight lamp columns with rows 8 and 9 coming from the Aux Lamp "
				"strobe. src/wpc/core.c MDRV_SWITCH_CONV/MDRV_LAMP_CONV(core_swSeq2m, core_m2swSeq) with "
				"core_swSeq2m(no) = no+7, CORE_FLIPPERSWCOL = 11, CORE_SWLRFLIPEOSBIT 0x01 through "
				"CORE_SWULFLIPBUTBIT 0x80, the locals.flipMask construction that yields 0x0f for this game's "
				"hw.flippers, core_getSol's GEN_SAM branches, core_getAllSol/core_getAllPhysicSols, and "
				"coreGlobals.nSolenoids = CORE_FIRSTCUSTSOL-1+hw.custSol = 66 with nLamps = 64+2*8 = 80 and "
				"nGI = 1; src/wpc/vpintf.c vp_getLamp/vp_getChangedSolenoids/vp_getChangedGI; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_SAM = 0x0100000000000"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/sam.json",
			"revision": "repository",
			"locator": (
				"Stern S.A.M. public switch, DIP, solenoid, lamp and single-GI address rules. Every rule the "
				"profile states was re-derived from pinned source for this curation and matched: sequential "
				"switch numbering with matrix 1-64, dedicated D-1 to D-8 at 65-72, dedicated D-17 to D-24 at "
				"-7 to 0, the flipper column at 81-88, solenoids 1-66 with 33 as the synthetic game-on state, "
				"and one aggregate GI channel at address 0. Two of the profile's prose notes are imprecise "
				"without affecting any address rule and were left unchanged rather than edited from inside a "
				"single game's curation: hw.custSol is hardcoded 16 by sam.c's INITGAME macro for every SAM "
				"game rather than configured per game, and the platform-level inversion_applied_by_emulator "
				"flag is true while pinned SAM source populates no inverted-switch mask at all (see "
				"conflict.sam-invsw-never-populated)."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/stern.pirates-of-the-caribbean.2006/ipdb/Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf",
			"original_filename": "Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"207-page OCR'd (Adobe Acrobat Pro Paper Capture) scan of the Stern Disney's Pirates of the "
				"Caribbean service and game manual, part 820-6384-00 Rev A, (c)2006 on printed page 3. PDF "
				"page 6 carries the Switch Matrix Grid (#1-#64), the Dedicated Switches D-1 to D-24 block and "
				"the CPU/Sound Bd. SW1 DIP block; PDF page 7 the Switch Locations plan and wiring schematics; "
				"PDF page 8 the Lamp Matrix Grid (01-80); PDF page 9 the Lamp Locations plan with its "
				"back-panel inset; PDF page 10 the Coils Detailed Chart Table; PDF page 11 the Coil & Flash "
				"Lamp Locations plan with its own back-panel inset; PDF page 115 (printed page 91) the Back "
				"Panel Assembly parts page the lamp-matrix footnote points at. The text layer is substantial "
				"but its front-matter pages decode as an unreadable custom encoding and its multi-column "
				"tables scramble, so every table used here was read from a rendered page."
			),
			"license": "NOASSERTION",
			"attribution": "Stern Pinball, Inc. / Disney",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.potc.switch-matrix",
					"locator": "PDF page 6, printed DR. 4, SWITCH MATRIX GRID (#1-#64)",
					"path": f"{EXCERPT_ROOT}/switch-matrix.md",
					"sha256": "b7ccfb326f62def2a3bb1a64dc13f47fbbfed0f00787e5de4d4eab40db7a08b9",
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.potc.dedicated-switches",
					"locator": "PDF page 6, printed DR. 4, Dedicated Switches (D-1 - D-24) and CPU/SOUND BD. SW1 DIP SWITCH blocks",
					"path": f"{EXCERPT_ROOT}/dedicated-switches.md",
					"sha256": "18e5fc7deae0d50d0b697f7151d765dea887ece90ccb70a5555d420e900b9b08",
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.potc.lamp-matrix",
					"locator": "PDF page 8, printed DR. 6, LAMP MATRIX GRID (01-80)",
					"path": f"{EXCERPT_ROOT}/lamp-matrix.md",
					"sha256": "e72e6877612477ba12c913a0dc7e9c894acbab57aba3fbf17a1a501bd86f8d2b",
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.potc.coils-detailed-chart",
					"locator": "PDF page 10, printed DR. 8, COILS DETAILED CHART TABLE",
					"path": f"{EXCERPT_ROOT}/coils-detailed-chart.md",
					"sha256": "c4075cb99e268ef09f9dca2e1c329ce9d898043a03534208cb2681f196a21acb",
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.potc.back-panel-lamp-locations",
					"locator": "PDF pages 9 and 11, printed DR. 7 Lamp Locations and DR. 9 Coil & Flash Lamp Locations, including both back-panel insets",
					"path": f"{EXCERPT_ROOT}/lamp-and-coil-locations.md",
					"sha256": "8ee8f828d8b81e9e7147354c035685a4cd0c1bfabd50f97b8afca165355e5633",
					"image": f"{EXCERPT_ROOT}/back-panel-lamp-locations.webp",
					"image_sha256": "884825be954551f716271a0ed92b2933da9ea793fb5b9022bfaca649b2d6d2ec",
					"image_derivation": "Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf page 9, crop box 0.1369,0.0848,0.5290,0.2424 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP. The crop is included because the fact it fixes -- that lamps 33-39 and 78-80 are back-panel devices -- is carried by the drawing and its two in-drawing notes, not by prose.",
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi rendered pages",
					"reviewed": True,
				},
				{
					"id": "excerpt.potc.back-panel-assembly",
					"locator": "PDF page 115, printed page 91, Back Panel Assembly, Individual Parts Only (Items 1-9 + Misc.)",
					"path": f"{EXCERPT_ROOT}/back-panel-assembly.md",
					"sha256": "f01e7e7e9d5d086525a1138a2c65bad53ccc0d30d25a6681830ece618d196fd0",
					"image": f"{EXCERPT_ROOT}/back-panel-flashers.webp",
					"image_sha256": "b2841303ed853c048ec74ed69788172baddc53d75945dc06261201250775d77d",
					"image_derivation": "Stern_2006_Pirates_of_the_Caribbean_Pinball_Service_Game_Manual.pdf page 115, crop box 0.30,0.22,0.94,0.47 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP. The crop is included because the socket callouts are part of the drawing: it is what shows both of the two #89 sockets on the back panel labelled Q22 FLASH and no Q30 socket anywhere.",
					"method": "manual",
					"transcribed_by": "curator, read from the 250 dpi rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/pirates-of-the-caribbean-2006/manual-transcription.md",
			"revision": "2026-08-08",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained curation record of which manual pages were rendered and read, which pages were "
				"checked and found not to carry a needed table, and how the physical year and machine "
				"identity were established. The committed digest-verified transcriptions themselves live "
				f"under {EXCERPT_ROOT}/ and are the canonical copies. This record also documents that IPDB "
				"was unreachable during this pass (HTTP 403 behind Cloudflare to a plain fetch, no headful "
				"browser session available), which is why machine.ipdb_id is omitted rather than guessed."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/pirates-of-the-caribbean-2006/source/Pirates%20of%20the%20Caribbean%20%28Stern%202006%29.vpx",
			"original_filename": "Pirates of the Caribbean (Stern 2006).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working community recreation of the physical machine. Exact playfield bounds "
				f"from its own gamedata.json are {TABLE_BOUNDS}; normalized coordinates are "
				f"x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. Geometry authority only for named table "
				"objects; the full per-object dump is retained at "
				"external:pinmame-review-artifacts/pirates-of-the-caribbean-2006/vpx-geometry.txt, SHA-256 "
				f"{VPX_GEOMETRY_SHA256}. This is a thin build by this project's standards -- 1,229 extracted "
				"files and a 32,543-byte script against the 240-290 kB VPW-authored scripts several other "
				"games in this run used -- and it is judged accordingly: its object set is good enough to "
				"place most addresses but it is not treated as authority for any address it does not model."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors (no author credit is present in the retained file's own table info)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/stern/pirates-of-the-caribbean-2006/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Retained embedded script, 32,543 bytes, 919 lines. Runtime and mechanism-causality "
				'authority: Const cGameName = "potc_600af", Const UseSolenoids = 1, Const UseLamps = True, '
				"Const UseGI = 0 with a GICallback set anyway, Const UseVPMModSol = 1, LoadVPM with sam.VBS "
				"and InitVpmFFlipsSAM; SolCallBack entries for 1, 2, 3, 4, 5, 6, 15, 16, 18, 19, 21, 23, 27, "
				"28 and 29 with SolModCallBack entries for the five flashers 20, 22, 30, 31 and 32; "
				"vpmMapLights AllLamps binding 78 lamp addresses by each Light's own TimerInterval; "
				"vpmNudge.TiltSwitch = -7; cvpmBallStack instances bsTROUGH (InitSw 0,21,20,19,18,0,0,0 and "
				"InitKick BallRelease), bsPOP (InitSaucer sw56,56) and bsL (InitSw 0,9,... and InitKick sw9); "
				"cvpmTurnTable mDISC (InitTurnTable Plunder,20) driven by SolSpinner off solenoid 6; the "
				"ShipTimer_Timer software position counter that derives switches 62 and 63; and "
				"Controller.Switch(63) = 1 in Table1_Init."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/pirates-of-the-caribbean-2006/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} "
				f"files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. "
				f"Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
	]

# --- Devices -------------------------------------------------------------------------------------

MANUAL_REFS = (MANUAL_SOURCE, CORE_SOURCE)
SCRIPT_REFS = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
GEOMETRY_REFS = (VPX_TABLE_SOURCE, MANUAL_SOURCE)

OPTO_POLARITY_NOTE = (
	"Identified as opto construction by this manual's own in-cell annotation; the switch-matrix page "
	"carries no shaded-cell opto legend and shades nothing. Pinned PinMAME applies zero switch-matrix "
	"inversion for this driver -- sam.c's INITGAME macro leaves core_gameData->wpc.invSw at its C "
	"zero-initialization default and no Stern S.A.M. game in sam.c ever assigns it -- so the public "
	"switch state is raw hardware polarity, not emulator-normalized. Physical normally-closed "
	"construction and controller normalization are independent facts and neither is settled here; see "
	"conflict.sam-invsw-never-populated."
)


def _switch_wiring(address: int) -> dict[str, Any]:
	drive_index = (address - 1) // 16 + 1
	return_index = (address - 1) % 16 + 1
	transistor, drive_wire, drive_connection = SWITCH_DRIVES[drive_index]
	ic, return_wire, return_connection = SWITCH_RETURNS[return_index]
	return {
		"board": "S.A.M. CPU/Sound board",
		"driver_transistor": transistor,
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_component": ic,
		"return_wire": return_wire,
		"return_connection": return_connection,
	}


def _matrix_switch(address: int) -> dict[str, Any]:
	annotation, label, part_number, location = SWITCH_MATRIX[address]
	drive_index = (address - 1) // 16 + 1
	return_index = (address - 1) % 16 + 1
	device: dict[str, Any] = {
		"id": f"switch.matrix-{address}",
		"label": label or "Not Used",
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address},
		"aliases": [
			{"namespace": "pinmame.switch", "value": str(address)},
			{"namespace": "manual.address", "value": f"SW. #{address}"},
		],
		"provenance": provenance(*(SCRIPT_REFS if address in SWITCH_POSITIONS else MANUAL_REFS)),
	}
	notes = [f"Printed switch-matrix drive row {drive_index} (transistor {SWITCH_DRIVES[drive_index][0]}), return column {return_index}."]
	physical: dict[str, Any] = {}
	if not label:
		device["availability"] = "unused"
		notes.append(
			"Printed NOT USED with no part number and no location. The drive and return lines that reach "
			"this matrix position are the shared column and row harness lines, so nothing on the page is "
			"specific to it."
		)
		device["spatial"] = not_applicable("unused", MANUAL_SOURCE)
	else:
		device["availability"] = "used"
		if part_number:
			physical["part_number"] = part_number
		if location:
			physical["location"] = location
		if address in OPTO_SWITCHES:
			physical["switch_type"] = "opto"
			notes.append(f"Printed in-cell annotation: {annotation}.")
			notes.append(OPTO_POLARITY_NOTE)
		elif address in (15, 16):
			physical["switch_type"] = "button"
			notes.append("Printed CABINET; a cabinet button rather than a playfield switch.")
		elif annotation:
			notes.append(f"Printed in-cell annotation: {annotation}.")
		if address not in OPTO_SWITCHES and address not in (15, 16):
			notes.append(
				"The manual states no construction type for this address beyond its part number, and its "
				"switch-wiring schematic inset labels normally-open, common and normally-closed terminals "
				"generically without saying which any individual switch uses, so switch_type is omitted "
				"rather than inferred from the part-number family."
			)
		if address in (21, 22):
			notes.append(
				"The manual leaves this row's location cell blank because the transmitter and receiver part "
				"numbers occupy it; the other three switches of the same four-ball trough print \"below "
				"playfield\". No location is asserted here rather than carried across from a neighbouring row."
			)
		if address in LAMP_MATRIX_MIRROR_NOTES:
			notes.append(LAMP_MATRIX_MIRROR_NOTES[address])
		if address in (30, 31, 32):
			notes.append(POP_BUMPER_POSITION_NOTE)
		if address == 42:
			notes.append(
				"The retained known-working script does not assert this address: it defines Sub sw43_Hit "
				"twice, once pulsing switch 42 and once pulsing switch 43, and defines no sw42_Hit at all, "
				"so only one of the two definitions can survive and Plunder 1 goes unreported at runtime. "
				"The table does contain a correctly positioned sw42 HitTarget object, which is what this "
				"record's placement uses; the missing handler is a defect in the retained recreation, not "
				"evidence about the physical machine."
			)
		if address == 63:
			device["initial_active"] = True
			notes.append(
				"The retained script sets Controller.Switch(63) = 1 in Table1_Init, so the ship rests at its "
				"home position with this switch made before the game controller starts."
			)
		if address in SWITCH_POSITIONS:
			device["spatial"] = located(f"switch.matrix-{address}", "sensor", (SWITCH_POSITIONS[address],), *GEOMETRY_REFS)
		else:
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	device["wiring"] = _switch_wiring(address)
	return device


LAMP_MATRIX_MIRROR_NOTES = {
	12: "The matching indicator lamp for this lane, LP. #78 (Left Top Lane), is a back-panel device rather than a playfield insert; see the lamp record for address 78.",
	13: "The matching indicator lamp for this lane, LP. #79 (Middle Top Lane), is a back-panel device rather than a playfield insert; see the lamp record for address 79.",
	14: "The matching indicator lamp for this lane, LP. #80 (Right Top Lane), is a back-panel device rather than a playfield insert; see the lamp record for address 80.",
}

POP_BUMPER_POSITION_NOTE = (
	"The manual names the three pop bumpers LEFT, RIGHT and BOTTOM on both its switch page (SW. #30/#31/"
	"#32) and its coil page (#9/#10/#11), and its Coil & Flash Lamp Locations plan draws the three coil "
	"callouts at the cluster's left, right and player-nearest positions in that order. The retained "
	"table's three Bumper objects sit at normalized (0.634, 0.219), (0.843, 0.205) and (0.764, 0.290), "
	"which admits exactly one bijection consistent with those three names. The retained script instead "
	"binds them in naive numeric order (Bumper1 -> 30, Bumper2 -> 31, Bumper3 -> 32), which puts LEFT on "
	"the player-nearest bumper; this record follows the manual and the table's own geometry for "
	"placement and records the disagreement as conflict.pop-bumper-position-naming."
)


def _dedicated_switch(address: int) -> dict[str, Any]:
	d_number, label, part_number, location, ic, wire, connector, availability, switch_type, roles = DEDICATED_SWITCHES[address]
	if 65 <= address <= 72:
		identifier = f"switch.dedicated-{address}"
		board_note = "Read through sam.c's dedswitch_lower_r, which returns coreGlobals.swMatrix[9] as the low byte of the dedicated-switch word."
	elif 81 <= address <= 88:
		identifier = f"switch.flipper-{address}"
		board_note = (
			f"Read through PinMAME's flipper switch column (CORE_FLIPPERSWCOL = 11), bit {FLIPPER_COLUMN_BITS[address]}. "
			"sam.c's dedswitch_lower_r reverses each nibble of that column to reach the hardware's own "
			"D-9 to D-16 order, which is why the printed D-number and the public address run in opposite "
			"directions within each group of four."
		)
	else:
		identifier = f"switch.service-{d_number.lower().replace('-', '')}"
		board_note = "Read through sam.c's dedswitch_upper_r, which returns coreGlobals.swMatrix[0] as the low byte of the upper dedicated-switch word."
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address},
		"aliases": [
			{"namespace": "pinmame.switch", "value": str(address)},
			{"namespace": "manual.address", "value": f"SW. {d_number}"},
		],
		"availability": availability,
		"provenance": provenance(*MANUAL_REFS),
	}
	notes = [f"Printed dedicated switch {d_number}.", board_note]
	physical: dict[str, Any] = {}
	if part_number:
		physical["part_number"] = part_number
	if location:
		physical["location"] = location
	if switch_type:
		physical["switch_type"] = switch_type
	if address in (85, 86, 87, 88):
		notes.append(
			"Structurally unreachable for this driver as well as printed NOT USED: potcGameData's "
			"hw.flippers is FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), so core.c's locals.flipMask evaluates to "
			"0x0f and core_updateSw never writes any of the four upper-flipper bits of the flipper column."
		)
	if address in (81, 83):
		notes.append(
			"An end-of-stroke switch on the flipper assembly. sam.c's switch read synthesizes the EOS state "
			"from its own flipper button bit (data |= (data & (bit8|bit10|bit12|bit14)) << 1, with the "
			"source comment 'SAM is not using standard VPM flipper coils, so the EOS simulation does not "
			"take place, and the ROM reports technician errors'), so a recreation does not need to drive "
			"this address independently even though the physical switch exists."
		)
	if address == -7:
		notes.append(
			"The retained known-working script confirms the public address directly: vpmNudge.TiltSwitch = -7."
		)
	if address == -2 or address == -1:
		notes.append(
			"Pinned sam.c disagrees with itself about which of the two red coin-door adjustment buttons this "
			"is: its descriptive comment block lists D21 as Plus and D22 as Minus, while its own keyboard "
			"input-port table (SAM_COMPORTS) puts Minus on the bit that becomes public -2 and Plus on the "
			"bit that becomes public -1. This manual agrees with the input-port table, so two sources "
			"against one resolve it that way; see conflict.coin-door-adjust-button-order."
		)
	if availability == "unused":
		device["spatial"] = not_applicable("unused", MANUAL_SOURCE)
	elif address in SWITCH_POSITIONS:
		device["spatial"] = located(identifier, "sensor", (SWITCH_POSITIONS[address],), *GEOMETRY_REFS)
	else:
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	device["wiring"] = {
		"board": "S.A.M. CPU/Sound board",
		"return_component": ic,
		"return_wire": wire,
		"return_connection": connector,
	}
	if roles:
		device["roles"] = list(roles)
	return device


def _dip_switch(position: int) -> dict[str, Any]:
	return {
		"id": f"dip.sw1-{position}",
		"label": f"CPU/Sound Board SW1 DIP Position #{position}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": position},
		"aliases": [
			{"namespace": "pinmame.dip", "value": str(position)},
			{"namespace": "manual.address", "value": f"SW. D-{24 + position}"},
		],
		"availability": "used",
		"physical": {
			"location": "CPU/Sound board, SW1, located between connectors J3/J13",
			"notes": (
				f"Printed as SW. D-{24 + position} on the same page as the dedicated switches, with the cell "
				"reading DIP SWITCH POSITION #" + str(position) + " and ON / OFF. sam.c reads the bank "
				"through dedswitch_upper_r as the high byte of the upper dedicated-switch word and exposes it "
				"on PinMAME's own DIP channel, not as a switch address. The low five bits select the country "
				"setting; the manual's own operating pages document positions 6, 7 and 8 as unused by the "
				"country table."
			),
		},
		"spatial": not_applicable("dip_switch", MANUAL_SOURCE),
		"provenance": provenance(*MANUAL_REFS),
	}


def input_devices() -> list[dict[str, Any]]:
	devices = [_dedicated_switch(address) for address in sorted(DEDICATED_SWITCHES) if address <= 0]
	devices += [_matrix_switch(address) for address in sorted(SWITCH_MATRIX)]
	devices += [_dedicated_switch(address) for address in sorted(DEDICATED_SWITCHES) if address > 0]
	devices += [_dip_switch(position) for position in range(1, 9)]
	return devices

# --- Outputs -------------------------------------------------------------------------------------

SOLENOID_ROLES = {
	1: ("trough.eject",),
	2: ("shooter.autolaunch",),
	15: ("flipper.left.coil",),
	16: ("flipper.right.coil",),
}

SOLENOID_EXTRA_NOTES = {
	4: "SolChest in the retained script drops the ChestOpen wall and raises ChestClosed, and a companion timer rotates the chest Primitive from RotX 0 to 66 degrees, so the lid is a hinged flap rather than a translating cover.",
	6: "Drives the motorised Plunder disc. The retained script registers it as a cvpmTurnTable (mDISC.InitTurnTable Plunder, 20) and gates the disc's own rotation with SolSpinner, so this is a continuous motor output, not a pulsed coil.",
	19: "Kicks the ball back out of the treasure chest. The retained script's SolChestExit raises and lowers the ChestPin wall rather than firing a kicker object, so the placement is that pin's own position at the chest exit.",
	21: "The ship's traverse motor. Direction comes from solenoid 27, not from this output: the retained script's SolShipMotor only enables the position timer, and SolMotorDir sets the sign the timer steps by.",
	22: "Printed FLASH: REAR CENTER (X2), two #89 bulbs. Printed page 91 (Back Panel Assembly) lists exactly two #89 sockets on the back panel and labels both of them Q22 FLASH, so both bulbs are backbox devices with no playfield coordinate. The retained table models three F22 Light objects, two of them at the playfield's own rear edge and one further onto the playfield; the third is an extra render light, not a third bulb.",
	24: "Printed OPTIONAL COIL, the only 5 volt output on the board and the only one wired to J16 rather than J6/J7/J8/J9. The manual's own note reads: 'Coil Q24 is Optional. If either a Coin Meter, Token Dispenser or Knocker (all optional equipment) is required, call Technical Support.' The retained script's own SolCallback(24) = FastFlips.TiltSol line is commented out.",
	27: "A relay PCB rather than a coil: it reverses the ship motor's direction. See relationship rel.ship-motor-direction-relay.",
	30: "Printed FLASH: BACK RIGHT [X3], three #89 bulbs. The Coil & Flash Lamp Locations page draws two of the three callouts on the playfield and one in its back-panel inset, and the retained table independently models two F30 Light objects on the playfield plus a co-located pair at the playfield's own rear edge -- but printed page 91 lists no Q30 socket on the back panel at all. Because the split between playfield and backbox bulbs cannot be settled, no placement set can be produced whose count matches the printed quantity, so this record carries no spatial key; see conflict.flasher-back-panel-bulb-count.",
}


def _solenoid(address: int) -> dict[str, Any]:
	label, transistor, power_wire, power_connection, volts, control_wire, control_connection, coil_part, kind, quantity, availability = SOLENOIDS[address]
	device: dict[str, Any] = {
		"id": f"solenoid.{address}",
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [
			{"namespace": "pinmame.solenoid", "value": str(address)},
			{"namespace": "manual.address", "value": f"#{address}"},
		],
		"availability": availability,
		"provenance": provenance(*(SCRIPT_REFS if address in SOLENOID_POSITIONS else MANUAL_REFS)),
	}
	group = "High Current Coils Group 1" if address <= 8 else "High Current Coils Group 2" if address <= 16 else "Low Current Coils Group 1" if address <= 24 else "Low Current Coils Group 2"
	notes = [f"Printed in the Coils Detailed Chart Table under {group}, drive transistor {transistor} on the I/O Power Driver board."]
	physical: dict[str, Any] = {}
	if coil_part:
		physical["part_number"] = coil_part
	if quantity > 1:
		physical["quantity"] = quantity
	if availability == "unused":
		notes.append(
			"Printed NOT USED. The drive transistor and its control-line wire colour and connector pin are "
			"populated, but the power line colour, the power voltage and the coil part are all blank, which "
			"is what shows nothing is fitted."
		)
	if address in FLASHER_ADDRESSES:
		notes.append(
			"One of the five flasher outputs this game fits. The manual's own Test Flash Lamps note names "
			"them explicitly (This Game: Q20, Q22, Q30, Q31 & Q32) and pinned sam.c's own potc block declares "
			"exactly the same five addresses as #89 bulbs, with zero disagreement between the two."
		)
	if address in SOLENOID_EXTRA_NOTES:
		notes.append(SOLENOID_EXTRA_NOTES[address])
	if address in (9, 10, 11):
		notes.append(POP_BUMPER_POSITION_NOTE)
	if address in (15, 16):
		notes.append(
			"S.A.M. flippers are fully CPU-controlled through a single ordinary numbered solenoid each, not "
			"through PinMAME's legacy lower-flipper addresses: sam.c writes only coreGlobals.solenoids and "
			"the physical output array and never touches coreGlobals.solenoids2, so public 45-48 stay dead "
			"for this platform. The retained known-working script confirms the binding directly with "
			"SolCallBack(15) = SolLFlipper and SolCallBack(16) = SolRFlipper. sam.c drives a 40 ms power "
			"pulse followed by a 1 ms hold pulse every 12 ms (SAM_SOL_FLIPSTART 13 to SAM_SOL_FLIPEND 16 "
			"carry a 14 ms switchDownLatency for this reason), so the single address carries both phases."
		)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	wiring: dict[str, Any] = {
		"board": "S.A.M. I/O Power Driver board",
		"driver_transistor": transistor,
		"control_wire": control_wire,
		"control_connection": control_connection,
		"power_connection": power_connection,
	}
	if power_wire:
		wiring["power_wire"] = power_wire
	if volts:
		wiring["nominal_voltage_v"] = volts
		wiring["voltage_type"] = "dc"
	device["wiring"] = wiring
	if address in SOLENOID_ROLES:
		device["roles"] = list(SOLENOID_ROLES[address])
	if address == 30:
		pass  # deliberately no spatial key; see conflict.flasher-back-panel-bulb-count
	elif availability == "unused":
		device["spatial"] = not_applicable("unused", MANUAL_SOURCE)
	elif address in (22, 24):
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	elif address in SOLENOID_POSITIONS:
		role = "emitter" if kind == "flasher" else "effect"
		device["spatial"] = located(f"solenoid.{address}", role, (SOLENOID_POSITIONS[address],), *GEOMETRY_REFS)
	else:
		raise RuntimeError(f"solenoid {address} has no spatial disposition")
	return device


VIRTUAL_SOLENOIDS: dict[int, tuple[str, str, str]] = {
	33: (
		"PinMAME SAM game-on state",
		"virtual",
		"PinMAME's synthetic S.A.M. game-on state, not a driver-board transistor. sam.c's VBLANK handler "
		"reads one byte of game RAM at samlocals.fastflipaddr (0x0105a7fe for any driver whose short name "
		"starts potc_600) and publishes the result on public solenoid address 33 (SAM_FASTFLIPSOL), with "
		"core.c's own comment '33 SAM fake GameOn sol for fast flips'. sam.c explicitly declares it "
		"CORE_MODOUT_NONE so it carries no bulb or coil physics. A recreation reads it to know whether "
		"flipper power is enabled; nothing drives it.",
	),
	34: ("Unused (S.A.M. reads the game-on state here)", "virtual", "", ),
	35: ("Unused (S.A.M. reads the game-on state here)", "virtual", ""),
	36: ("Unused (S.A.M. reads the game-on state here)", "virtual", ""),
	37: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	38: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	39: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	40: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	41: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	42: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	43: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	44: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	45: ("Unused legacy lower-right flipper power address", "virtual", ""),
	46: ("Unused legacy lower-right flipper hold address", "virtual", ""),
	47: ("Unused legacy lower-left flipper power address", "virtual", ""),
	48: ("Unused legacy lower-left flipper hold address", "virtual", ""),
	49: ("PinMAME built-in ball simulator output", "virtual", ""),
	50: ("PinMAME reserved simulated output", "virtual", ""),
}

VIRTUAL_SOLENOID_GROUP_NOTES = {
	"34-36": (
		"Enumerated but carries no state a consumer can use. core_getSol's 33-36 branch returns the same "
		"synthetic game-on bit for every address in the range when the generation is GEN_SAM, but the two "
		"aggregate paths a consumer actually reads through -- core_getAllSol and core_getAllPhysicSols -- "
		"publish the game-on state at address 33 only and leave 34-36 at zero. No driver-board transistor "
		"exists behind any of them."
	),
	"37-44": (
		"Enumerated by PinMAME's S.A.M. extra-solenoid range but never written for this platform. "
		"core_getAllSol and core_getAllPhysicSols mirror internal solenoid indices 41-48 into public 37-44 "
		"for GEN_ALLS11 | GEN_SAM | GEN_SPA, and sam.c writes nothing to those indices; core_getSol's own "
		"37-44 branch does not even list GEN_SAM, so it returns zero. No physical output exists behind them "
		"and this manual prints no coil beyond #32."
	),
	"45-48": (
		"PinMAME's legacy lower-flipper addresses, dead on this platform. They are computed from "
		"coreGlobals.solenoids2, which sam.c only ever writes as the game-on bit 0x10, and "
		"coreGlobals.hasModulatedFlippers is never set for S.A.M. This game's two flipper coils are the "
		"ordinary numbered solenoids 15 and 16."
	),
	"49-50": (
		"PinMAME's own built-in ball simulator outputs (CORE_FIRSTSIMSOL = 49), answered by sim_getSol. The "
		"retained known-working script implements its own ball handling through cvpmBallStack instances and "
		"never references either address."
	),
}

AUX_SOLENOID_NOTE = (
	"Enumerated because sam.c's INITGAME macro hardcodes hw.custSol = 16 for every Stern S.A.M. game, so "
	"coreGlobals.nSolenoids is always CORE_FIRSTCUSTSOL - 1 + 16 = 66 and LibPinMAME's ChangedSolenoids "
	"contract always covers 51-66. No auxiliary driver board is fitted to this machine: potcGameData "
	"declares SAM_NO_AUX, so none of sam.c's auxiliary-board write paths (SAM_GAME_AUXSOL8_CSTB, "
	"SAM_GAME_AUXSOL8_DSTB, SAM_GAME_AUXSOL6, SAM_GAME_AUXSOL12, SAM_GAME_METALLICA_MAGNET, SAM_GAME_IJ4) "
	"is enabled and nothing ever writes these sixteen outputs. The manual prints no auxiliary coil table "
	"and its Coils Detailed Chart Table stops at #32."
)


def _virtual_solenoid(address: int) -> dict[str, Any]:
	label, kind, note = VIRTUAL_SOLENOIDS[address]
	if not note:
		for span, text in VIRTUAL_SOLENOID_GROUP_NOTES.items():
			low, high = (int(part) for part in span.split("-"))
			if low <= address <= high:
				note = text
				break
	return {
		"id": f"solenoid.{address}",
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
		"availability": "used" if address == 33 else "unused",
		"physical": {"notes": note},
		"spatial": not_applicable("virtual", CORE_SOURCE),
		"provenance": provenance(CORE_SOURCE),
	}


def _aux_solenoid(address: int) -> dict[str, Any]:
	return {
		"id": f"solenoid.{address}",
		"label": f"Auxiliary driver output {address - 50} (no auxiliary board fitted)",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
		"availability": "unused",
		"physical": {"notes": AUX_SOLENOID_NOTE},
		"spatial": not_applicable("unused", CORE_SOURCE, MANUAL_SOURCE),
		"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
	}


def solenoid_outputs() -> list[dict[str, Any]]:
	devices = [_solenoid(address) for address in sorted(SOLENOIDS)]
	devices += [_virtual_solenoid(address) for address in sorted(VIRTUAL_SOLENOIDS)]
	devices += [_aux_solenoid(address) for address in range(51, 67)]
	return devices


def _lamp(address: int) -> dict[str, Any]:
	label, bulb, part_number = LAMPS[address]
	row = (address - 1) // 8 + 1
	column = (address - 1) % 8 + 1
	transistor, row_wire, row_connection = LAMP_ROWS[row]
	ic, column_wire, column_connection = LAMP_COLUMNS[column]
	device: dict[str, Any] = {
		"id": f"lamp.{address}",
		"label": label,
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": address},
		"aliases": [
			{"namespace": "pinmame.lamp", "value": str(address)},
			{"namespace": "manual.address", "value": f"LP. #{address}"},
		],
		"availability": "used",
		"provenance": provenance(*(SCRIPT_REFS if address in LAMP_POSITIONS else MANUAL_REFS)),
	}
	notes = [
		f"Printed lamp-matrix row {row} (ground transistor {transistor}), column {column} ({ic}). "
		f"Printed bulb type: {bulb}.",
		"S.A.M. publishes its lamp matrix row-major, so the public address is (row - 1) * 8 + column: "
		"rows 1-8 carry public 1-64 through the eight main strobe lines and rows 9 and 10 carry public "
		"65-80 through the Aux Lamp strobe's two data bits. This is the opposite axis order from the "
		"Whitestar switch matrix and had to be re-derived from this manual's own printed grid; sam.c's own "
		"per-game potc block confirms it independently by naming lamps 24, 32, 40, 48, 56, 64 and 72 as the "
		"H, E, A, R, T and two Heart Chest LEDs of board 520-5258-00, which is column 8 of rows 3 to 9.",
	]
	physical: dict[str, Any] = {"part_number": part_number}
	quantity = LAMP_QUANTITIES.get(address)
	if quantity:
		physical["quantity"] = quantity
	if address in CABINET_LAMPS:
		physical["location"] = "cabinet button"
		notes.append(
			"A cabinet button lamp: it is not drawn anywhere on the Lamp Locations playfield plan, and the "
			"retained table's AllLamps collection contains no object for it."
		)
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	elif address in BACK_PANEL_LAMPS:
		physical["location"] = "back panel"
		notes.append(
			"A back-panel device, not a playfield insert. Printed page 91 (Back Panel Assembly) lists it "
			"among ITEM 3 (seven #44 Red sockets labelled LP. 33 to LP. 39) or ITEM 4 (three #44 Green "
			"sockets labelled LAMP 78 to LAMP 80), and the Lamp Locations page's own back-panel inset draws "
			"all ten with the grey 'Lamps on Back Panel' shading and counts them in its own note: 'THERE ARE "
			"10 LAMPS (7 RED / 3 GREEN) LOCATED ON THE BACK PANEL.' The retained table does model a Light "
			"object for each at the extreme rear edge of the playfield (normalized y between 0.020 and "
			"0.022) as a visual proxy; those coordinates are recorded in the retained geometry dump and are "
			"deliberately not promoted to playfield placements."
		)
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		if address in (24, 32, 40, 48, 56, 64, 72):
			notes.append(
				"An LED on board 520-5258-00, the Heart Chest LED PCB, rather than a socketed bulb. Pinned "
				"sam.c's potc block names this exact address on that exact board."
			)
		if address in (64, 72):
			notes.append(
				"The matrix cell prints the label with the suffix (double-dot) and pinned sam.c's own comment "
				"for both addresses reads 'Heart Chest double LED', so the LED package on the PCB shows two "
				"dots. Neither the matrix nor any parts page prints a bulb quantity for either address, so "
				"none is asserted and the single position on the PCB carries one placement."
			)
		if quantity:
			notes.append(
				f"The matrix cell prints a quantity of {quantity} bulbs on this one address, so it carries "
				f"{quantity} placements."
			)
		if address == 77:
			notes.append(
				"The matrix cell prints the bulb type #555 Clear but the part number 165-5053-05-HF, which "
				"is the #44 Blue part used by lamps 67, 68, 75 and 76 on the same page. Both are transcribed "
				"verbatim in the excerpt; the disagreement is about a bulb type, not an address, and is not "
				"resolved here."
			)
		device["spatial"] = located(f"lamp.{address}", "emitter", LAMP_POSITIONS[address], *GEOMETRY_REFS)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	device["wiring"] = {
		"board": "S.A.M. I/O Power Driver board",
		"driver_transistor": transistor,
		"drive_wire": column_wire,
		"drive_connection": column_connection,
		"return_component": ic,
		"return_wire": row_wire,
		"return_connection": row_connection,
		"nominal_voltage_v": 18.0,
		"voltage_type": "dc",
	}
	return device


def lamp_outputs() -> list[dict[str, Any]]:
	return [_lamp(address) for address in sorted(LAMPS)]


def gi_outputs() -> list[dict[str, Any]]:
	return [
		{
			"id": "gi.0",
			"label": "General Illumination Relay",
			"kind": "gi",
			"binding": {"group": "pinmame.output.gi", "device": 0},
			"aliases": [{"namespace": "pinmame.gi", "value": "0"}],
			"availability": "used",
			"physical": {
				"notes": (
					"Stern S.A.M. has exactly one general-illumination channel: sam.c sets coreGlobals.nGI = 1 "
					"and drives coreGlobals.gi[0] from bit 0 of the latch at I/O address 0x0240002B with its "
					"own comment 'Bit 0 drives GI relay'. There is no per-string channel, so every physical "
					"illumination string behind the relay switches together. The retained known-working script "
					"matches that shape: its UpdateGI ignores the string number entirely and switches one GI "
					"collection of 85 members plus an empty GI2 collection. This manual prints no general-"
					"illumination bulb table anywhere. What it does state is that ten clear #44 sockets on the "
					"back panel are G.I. rather than matrix lamps (printed page 91 ITEM 2, QTY. 10, plus the "
					"Lamp Locations note 'THE TOP TEN CLEAR BULBS ARE G.I.s; NOT CONTROL LAMPS') and that the "
					"three LED modules on the right ramp are also G.I. ('THE 3 LEDS MODULES ON THE RIGHT RAMP "
					"ARE G.I.s; NOT CONTROL LAMPS'). The playfield G.I. bulb inventory is spread across the "
					"Section 4 assembly pages and was not exhaustively enumerated in this pass, so no bulb "
					"quantity and no placement set is asserted and this record carries no spatial key."
				)
			},
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, status="observed"),
		}
	]


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 Dot Matrix Display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]

# --- Mechanisms, relationships and conflicts -----------------------------------------------------


def mechanisms() -> list[dict[str, Any]]:
	return [
		{
			"id": "mech.ball-trough",
			"label": "Four-Ball Trough",
			"kind": "kicker",
			"actuators": ["solenoid.1"],
			"sensors": [
				"switch.matrix-18",
				"switch.matrix-19",
				"switch.matrix-20",
				"switch.matrix-21",
				"switch.matrix-22",
			],
			"behavior": (
				"A four-ball trough below the playfield. The manual prints its four position switches as "
				"TROUGH #4 (L), #3, #2 and #1 (R) at public 18, 19, 20 and 21, and prints them as two "
				"different constructions on the same page: #4, #3 and #2 are mechanical switches "
				"(180-5119-02) while #1 is an opto pair annotated (VUK OPTO) with transmitter and receiver "
				"parts 515-0173-00 and 515-0174-00. A fifth address, public 22, is a second opto pair "
				"annotated (STACK OPTO) and named TROUGH JAM in italics; it sits in the trough's own exit "
				"path rather than at a ball rest position. Solenoid 1 (Trough Up-Kicker, 26-1200) lifts one "
				"ball out to the shooter lane. The retained known-working script models the whole assembly as "
				"one cvpmBallStack (bsTROUGH.InitSw 0,21,20,19,18,0,0,0 with InitKick BallRelease and "
				"Balls = 4) and asserts the jam opto as a pulse from inside SolTrough (vpmTimer.PulseSw 22), "
				"which is the ball crossing that opto as it leaves rather than the coil actuating the switch. "
				"None of the five switches has its own object in the retained table, so all five placements "
				"are documented projections onto the trough's own ball-release kicker. Default state at rest "
				"with a full trough is all four position switches made; solenoid 1 is a single pulse per "
				"ball, not a hold."
			),
			"positions": [
				{"id": "trough.ball-4", "label": "Trough #4 (left, furthest from the kicker)", "sensors": ["switch.matrix-18"]},
				{"id": "trough.ball-3", "label": "Trough #3", "sensors": ["switch.matrix-19"]},
				{"id": "trough.ball-2", "label": "Trough #2", "sensors": ["switch.matrix-20"]},
				{"id": "trough.ball-1", "label": "Trough #1 (right, at the kicker)", "sensors": ["switch.matrix-21"]},
				{"id": "trough.jam", "label": "Trough Jam / stack opto in the exit path", "sensors": ["switch.matrix-22"]},
			],
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.auto-launch",
			"label": "Auto Launch",
			"kind": "kicker",
			"actuators": ["solenoid.2"],
			"sensors": ["switch.matrix-23"],
			"behavior": (
				"A 23-800 auto-launch coil in the shooter lane, fired by the ROM to put a served ball into "
				"play without the player pulling the plunger. Public switch 23 (Shooter Lane, 180-5157-00) "
				"reports the ball waiting in the lane. The retained script wires solenoid 2 to a "
				"cvpmImpulseP plunger (PlungerIM.AutoFire) at the plunger's own position. The coil does not "
				"actuate the switch: the ball resting on the lane switch is what closes it, and launching "
				"releases it."
			),
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.top-center-vuk",
			"label": "Top Center Vertical Up-Kicker",
			"kind": "kicker",
			"actuators": ["solenoid.3"],
			"sensors": ["switch.matrix-9"],
			"behavior": (
				"A vertical up-kicker at the top centre of the playfield, coil 26-1200 on public solenoid 3, "
				"with public switch 9 (Top Center VUK, 180-5119-02-family part 180-5209-00) reporting a ball "
				"held in the kicker's own cup. The switch cell carries the manual's D.O.T.S. annotation, "
				"which the Lamp Locations page defines as 'Diode On Terminal Strip' -- a wiring note, not a "
				"construction type. The retained script models it as a cvpmBallStack kicker (bsL.InitSw 0, 9 "
				"with InitKick sw9, 89, 20), so the ball is captured, held on the switch, and then kicked "
				"upward at a steep angle."
			),
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.pop-bumper-eject",
			"label": "Pop Bumper Eject Hole",
			"kind": "kicker",
			"actuators": ["solenoid.18"],
			"sensors": ["switch.matrix-56"],
			"behavior": (
				"An eject hole in the pop-bumper area: public switch 56 (Pop Eject, 180-5186-01) reports a "
				"ball in the hole and public solenoid 18 (Pop Bumper Eject, 26-1200) ejects it. The retained "
				"script models it as a saucer (bsPOP.InitSaucer sw56, 56, 75, 8), so the ball is held on the "
				"switch until the ROM fires the coil. This is the ejector for the hole beside the three pop "
				"bumpers, not the pop bumpers themselves, whose own coils are public 9, 10 and 11."
			),
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.treasure-chest",
			"label": "Treasure Chest",
			"kind": "toy",
			"actuators": ["solenoid.4", "solenoid.19", "solenoid.20"],
			"sensors": ["switch.matrix-3", "switch.matrix-6"],
			"behavior": (
				"A hinged treasure chest on the right side of the playfield that opens its lid to accept a "
				"ball and locks it. Public solenoid 4 (Chest Lid, 27-1400) opens and closes the lid; the "
				"retained script's SolChest drops the ChestOpen wall while raising ChestClosed and a "
				"companion timer rotates the chest Primitive from RotX 0 to 66 degrees in 3-degree steps, so "
				"the lid is a flap that swings up rather than a cover that slides. Public solenoid 19 (Chest "
				"Kicker, 26-1200) releases a locked ball: the script's SolChestExit raises and lowers the "
				"ChestPin wall at the chest exit. Public switch 3 (Hit Chest) is an opto pair in front of the "
				"chest that registers a shot at it; public switch 6 (Chest Lock, 180-5119-02, above "
				"playfield) registers a ball actually captured inside. Public solenoid 20 (Flash: Chest, one "
				"#89 bulb) is the chest's own flasher. Neither coil actuates either switch: the ball does. "
				"Default state is lid closed with the release pin up."
			),
			"positions": [
				{"id": "chest.closed", "label": "Lid closed", "sensors": []},
				{"id": "chest.open", "label": "Lid open", "sensors": []},
				{"id": "chest.locked", "label": "Ball captured inside", "sensors": ["switch.matrix-6"]},
			],
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.plunder-disc",
			"label": "Plunder Spinning Disc",
			"kind": "rotary",
			"actuators": ["solenoid.6", "solenoid.23"],
			"sensors": [
				"switch.matrix-4",
				"switch.matrix-11",
				"switch.matrix-42",
				"switch.matrix-43",
				"switch.matrix-44",
				"switch.matrix-45",
				"switch.matrix-46",
				"switch.matrix-47",
			],
			"behavior": (
				"A motorised disc at the rear left of the playfield, ringed by six stand-up targets. Public "
				"solenoid 6 (Plunder Disk Motor, 'Motor 12V', part 511-5024-04) spins the disc "
				"continuously while asserted; it is a motor output, not a pulsed coil, and the manual prints "
				"it in the High Current group alongside the coils. The disc has no position sensor of any "
				"kind: no printed switch reports its angle and the retained script drives it as a "
				"cvpmTurnTable (mDISC.InitTurnTable Plunder, 20, SpinUp 1000, SpinDown 10) whose visible "
				"rotation is a free-running timer stepping RotatingPlatform.RotZ by 7 degrees, so a "
				"recreation gets speed but not phase. Public switch 11 (Plunder Enter) and public switch 4 "
				"(Plunder Exit) are both opto pairs at the entrance and exit and are how the ROM knows a "
				"ball is on the disc; the retained script keeps its own BallinSpin counter off exactly those "
				"two. Public switches 42 to 47 (Plunder 1 to Plunder 6, 180-5133-02, above playfield) are "
				"the six stand-up targets around the disc. Public solenoid 23 (Plunder Pin, 22-900) is a "
				"retractable post at the disc; the retained script raises and lowers its TortugaPost wall. "
				"None of the coils actuates any of the switches."
			),
			"provenance": provenance(*SCRIPT_REFS),
		},
		{
			"id": "mech.black-pearl-ship",
			"label": "Sinking Ship",
			"kind": "motorized",
			"actuators": ["solenoid.5", "solenoid.21", "solenoid.27", "solenoid.28", "solenoid.29", "solenoid.32"],
			"sensors": ["switch.matrix-61", "switch.matrix-62", "switch.matrix-63"],
			"behavior": (
				"The machine's headline mechanism: a model ship at the rear left that rotates about its "
				"beam to dive bow-down through a series of positions as the player sinks it, with its masts "
				"folding forward as it goes. It is driven by a 24 volt motor (public solenoid 21, Ship "
				"Motor, part 041-5101-00) whose direction is set by a separate relay PCB (public solenoid "
				"27, Ship Motor Relay, part 511-5024-03) rather than by reversing the motor output itself: "
				"the retained script's SolShipMotor only enables the position timer while SolMotorDir sets "
				"the sign the timer steps by, so a recreation must read 27 to know which way 21 will travel. "
				"Two limit switches report the ends of travel, both 180-5189-00 below the playfield: public "
				"switch 63 (Ship Home) at the upright rest position and public switch 62 (Ship Fully Sunk) "
				"at the far end. Between the two ends neither switch is made, so the mechanism reports three "
				"distinguishable states, not a continuous position. Public switch 61 (Ship Made) is a "
				"separate opto pair in the ship's own shot path, not a position sensor. Two more coils act "
				"on the sails rather than the hull: public solenoid 5 (Raise Sails, 26-1200) and public "
				"solenoid 28 (Lower Sails Latch, 29-1400) set the mast attitude, and the retained script "
				"only accepts either while the hull is at home (both subs test If ShipPos = 0). Public "
				"solenoid 29 (Ship Pin, printed 'UP POST', 26-1200) is a retractable post in front of the "
				"ship, and public solenoid 32 (Flash: Ship, one #89 bulb) is its flasher. Startup and reset "
				"behavior: the retained script sets Controller.Switch(63) = 1 at load, so the ship rests at "
				"home with the home switch made and the sails latched down. The motor does not actuate "
				"either limit switch through the coil; the hull reaching the end of travel closes it."
			),
			"positions": [
				{"id": "ship.home", "label": "Home (upright, sails down)", "sensors": ["switch.matrix-63"], "description": "Rest position. The retained script's own position counter reads 0 here and both sails coils are only accepted in this state."},
				{"id": "ship.travelling", "label": "Travelling between the ends", "sensors": [], "description": "Neither limit switch is made. The retained script steps an internal counter through two intermediate sink attitudes here, which is table modelling rather than reported hardware state."},
				{"id": "ship.fully-sunk", "label": "Fully sunk", "sensors": ["switch.matrix-62"], "description": "Far end of travel, reported by the Ship Fully Sunk limit switch."},
			],
			"provenance": provenance(*SCRIPT_REFS),
		},
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "rel.ship-motor-direction-relay",
			"kind": "relay_gated",
			"source": "solenoid.27",
			"destination": "solenoid.21",
			"provenance": provenance(*SCRIPT_REFS),
		}
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.sam-invsw-never-populated",
			"path": "controller.inversion_applied_by_emulator; inputs[binding.device=3,4,11,21,22,60,61]",
			"description": (
				"The controller profile pinmame.sam declares inversion_applied_by_emulator: true as a "
				"platform capability, matching every WPC profile this project has curated. For Stern S.A.M. "
				"pinned PinMAME applies none. sam.c's INITGAME macro expands to a positional aggregate "
				"initializer that stops at the hw sub-struct, so core_gameData->wpc.invSw is left at its C "
				"zero-initialization default, and core.c copies those zeros straight into "
				"coreGlobals.invSw at machine init. Searching the whole of src/wpc/sam.c for invSw returns no "
				"assignment anywhere, so this is a platform-wide fact to check on every future S.A.M. "
				"curation rather than a defect specific to this game -- the same shape as the Whitestar gap "
				"already recorded for Stern The Simpsons Pinball Party. Against that, this manual positively "
				"identifies seven switches as opto pairs: 3 (Hit Chest), 4 (Plunder Exit) and 11 (Plunder "
				"Enter) annotated (OPTO PAIR), 21 (Trough #1) annotated (VUK OPTO), 22 (Trough Jam) "
				"annotated (STACK OPTO), and 60 (Skill Hole Made) and 61 (Ship Made) annotated (OPTO PAIR); "
				"21 and 22 additionally print transmitter and receiver part numbers 515-0173-00 and "
				"515-0174-00 in place of a mechanical switch part. That set is the exhaustive result of "
				"sweeping all 64 printed cells for both of this page's own cues, and the page carries no "
				"shaded-cell legend and shades nothing. Physical construction is therefore known for seven "
				"addresses while their emulator-side normalization is not, and the manual never states "
				"normally-open or normally-closed for any individual switch either -- its own switch-wiring "
				"schematic inset labels all three terminals generically. Resolution path: a LibPinMAME "
				"gameplay-harness trace of a legal potc ROM observing the idle public state of switches 3, 4, "
				"11, 21, 22, 60 and 61 with and without a ball present. Unresolved."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE, CONTROLLER_SOURCE],
		},
		{
			"id": "conflict.flasher-back-panel-bulb-count",
			"path": "outputs[binding.device=22,30]",
			"description": (
				"The manual disagrees with itself about how its five flasher bulbs are split between the "
				"playfield and the back panel. The Coils Detailed Chart Table prints public solenoid 22 as "
				"FLASH: REAR CENTER (X2) and public solenoid 30 as FLASH: BACK RIGHT [X3], both #89 bulbs. "
				"The Coil & Flash Lamp Locations page draws one 22 callout and one 30 callout inside its "
				"back-panel inset with the grey 'Coils / Flash Lamps on Back Panel' shading, plus one 22 and "
				"two 30 callouts on the playfield plan -- which adds up to both printed quantities. But "
				"printed page 91 (Back Panel Assembly, Individual Parts Only) lists exactly two #89 sockets "
				"on the back panel as its ITEM 5 (QTY. 2) and labels both of them Q22 FLASH, with no Q30 "
				"socket drawn or listed anywhere on the page. The two pages cannot both be right. The "
				"retained known-working table is consistent with page 91 for address 22 (two co-located F22 "
				"Light objects at the playfield's own rear edge, normalized y 0.019 and 0.020) but also adds "
				"a third F22 light further onto the playfield, and for address 30 it models two playfield "
				"lights plus a co-located pair at the rear edge -- so it reproduces both readings at once and "
				"settles nothing. This record follows page 91's explicit parts list for address 22 and gives "
				"it a controlled cabinet_or_service spatial record with quantity 2. For address 30 no "
				"placement set can be produced whose count matches the printed quantity of three without "
				"choosing a side, so that record carries no spatial key at all. Resolution path: a "
				"photograph or lamp test of an unrestored machine's back panel showing how many #89 sockets "
				"are fitted and which driver each is wired to. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_TABLE_SOURCE],
		},
		{
			"id": "conflict.pop-bumper-position-naming",
			"path": "inputs[binding.device=30,31,32]; outputs[binding.device=9,10,11]",
			"description": (
				"The manual names the three pop bumpers LEFT, RIGHT and BOTTOM consistently on both of its "
				"own pages -- SW. #30/#31/#32 on the Switch Matrix Grid and #9/#10/#11 in the Coils Detailed "
				"Chart Table -- and its Coil & Flash Lamp Locations plan draws the three coil callouts at the "
				"bumper cluster's left, right and player-nearest positions in that order. The retained "
				"known-working script binds them the other way: its three Bumper objects pulse switches 30, "
				"31 and 32 in naive numeric order (Bumper1 -> 30, Bumper2 -> 31, Bumper3 -> 32), and those "
				"objects sit at normalized (0.764, 0.290), (0.634, 0.219) and (0.843, 0.205), which makes the "
				"script's LEFT bumper the player-nearest one and its BOTTOM bumper the rightmost. Only one "
				"bijection between three names and three positions is geometrically coherent, and the "
				"manual's two pages plus the table's own geometry agree on it against the script's identifier "
				"ordering alone, so this record uses the manual's reading for all six placements. The "
				"disagreement is recorded rather than silently resolved because the runtime script is "
				"normally this project's authority for address semantics and it is the source being "
				"overruled. Resolution path: a photograph of the physical playfield with the bumper harness "
				"visible, or a coil test on real hardware. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE],
		},
		{
			"id": "conflict.coin-door-adjust-button-order",
			"path": "inputs[binding.device=-2,-1]",
			"description": (
				"Pinned sam.c disagrees with itself about which of the two red coin-door adjustment buttons "
				"lands on public switch -2 and which on -1. Its descriptive comment block over "
				"dedswitch_upper_r reads 'D21 - DED #22 - Plus (Coin Door)' then 'D22 - DED #23 - Minus', "
				"while its own keyboard input-port table SAM_COMPORTS assigns 'Minus' to the port bit that "
				"CORE_SETKEYSW shifts into switch-column-0 bit 5 (public -2) and 'Plus' to the bit that "
				"becomes bit 6 (public -1). This manual's own dedicated-switch block agrees with the "
				"input-port table: D-22 is MINUS (< / - RED BUTTON), part 180-5192-02, and D-23 is PLUS "
				"(+ / > RED BUTTON), same part. Two sources against one resolve it in favour of Minus at -2 "
				"and Plus at -1, which is what this record uses. It is recorded as a first-class conflict for "
				"provenance completeness in the same spirit as the naming defect already recorded for "
				"Williams Bram Stoker's Dracula, even though both addresses are coin-door service buttons "
				"and neither can affect an authored playfield device. Unresolved in pinned source."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE],
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

# --- Definition ----------------------------------------------------------------------------------

SPATIAL_GAPS = (
	"outputs[binding.device=30] (pinmame.output.solenoid, FLASH: BACK RIGHT [X3]) has no spatial key: "
	"the manual disagrees with itself about how its three #89 bulbs split between the playfield and the "
	"back panel, so no placement set can match the printed quantity without picking a side. See "
	"conflict.flasher-back-panel-bulb-count.",
	"outputs[binding.device=0] (pinmame.output.gi, General Illumination Relay) has no spatial key: this "
	"manual prints no general-illumination bulb table, so neither a bulb quantity nor a placement set "
	"can be asserted. The ten back-panel G.I. sockets and the three right-ramp LED modules are the only "
	"G.I. inventory it states; the playfield G.I. bulbs are spread across the Section 4 assembly pages "
	"and were not exhaustively enumerated in this pass.",
)


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Pirates of the Caribbean",
			"manufacturer": "Stern",
			"year": 2006,
			"kind": "physical_pinball",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "observed",
				"spatial_placement": "observed",
			},
		},
		"controller": {
			"platform": "pinmame.sam",
			"hardware_generation": "0x100000000000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Pirates of the Caribbean device identifiers are not unique: {duplicates}")
	placement_ids: list[str] = []
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device.get("spatial")
		if spatial and spatial["status"] != "not_applicable":
			placement_ids += [placement["id"] for placement in spatial["placements"]]
	placement_duplicates = sorted({item for item in placement_ids if placement_ids.count(item) > 1})
	if placement_duplicates:
		raise RuntimeError(f"Pirates of the Caribbean placement identifiers are not unique: {placement_duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	missing_inputs: list[int] = []
	placement_count = 0
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			missing_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	missing_outputs: list[dict[str, Any]] = []
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			missing_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
		"blockers": list(SPATIAL_GAPS),
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/pirates-of-the-caribbean-2006/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
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
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/stern.pirates-of-the-caribbean.2006/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/pirates-of-the-caribbean-2006/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"geometry": {
				"path": "external:pinmame-review-artifacts/pirates-of-the-caribbean-2006/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": list(EXCLUDED_LAMP_OBJECTS),
		"unresolved": [
			{"group": "pinmame.output.solenoid", "address": binding["address"]}
			for binding in missing_outputs
			if binding["group"] == "pinmame.output.solenoid"
		]
		+ [
			{"group": "pinmame.output.gi", "address": binding["address"]}
			for binding in missing_outputs
			if binding["group"] == "pinmame.output.gi"
		]
		+ [{"group": "pinmame.input.switch", "address": address} for address in sorted(missing_inputs)],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Pirates of the Caribbean (Stern, 2006) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `partial` at "
		"`machines/partial/stern/pirates-of-the-caribbean-2006.json`. Two output addresses carry no "
		"spatial record at all and are named below; four unresolved conflicts and incomplete "
		"recreation knowledge are recorded in the definition itself.",
		"",
		"The matching source is the retained known-working `Pirates of the Caribbean (Stern 2006).vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds from the table's own `gamedata.json` are `{TABLE_BOUNDS}`, so every canonical coordinate "
		f"is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT} rounded to at most six fractional places. Note "
		"the y divisor: this table is 2155 units tall, not the 2162 most WPC-era tables in this project "
		"use.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the Stern service manual is "
		"the physical inventory, quantity, wiring and location authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- This is a thin recreation by this project's standards: 1,229 extracted files and a 32,543-byte "
		"script, against the 240-290 kB VPW-authored scripts several other games in this run used. It is "
		"judged on what it actually models rather than promoted for being present. Where it models an "
		"address with a plausibly placed object, that object is used; where it does not, no coordinate is "
		"invented.",
		"- Lamps 33-39 and 78-80 are back-panel devices per printed page 91 and the Lamp Locations page's "
		"own back-panel inset, so all ten carry a controlled `cabinet_or_service` record even though the "
		"retained table models a Light object for each at the extreme rear edge of the playfield "
		"(normalized y 0.020 to 0.022). Those rear-edge coordinates are recorded in the retained geometry "
		"dump and deliberately not promoted.",
		"- Lamps 1 and 2 are cabinet button lamps: neither is drawn on the Lamp Locations playfield plan "
		"and neither has an object in the retained table's `AllLamps` collection.",
		"- The three pop bumpers are placed from the manual's own left/right/bottom naming and the "
		"retained table's own geometry, which admit exactly one coherent bijection, rather than from the "
		"retained script's naive numeric object ordering. See "
		"`conflict.pop-bumper-position-naming`.",
		"- Public solenoid 22 (`FLASH: REAR CENTER (X2)`) is a backbox device: printed page 91 lists two "
		"`#89` sockets on the back panel and labels both `Q22 FLASH`. It carries a controlled "
		"`cabinet_or_service` record with quantity 2.",
		"- Public solenoids 33 to 66 are enumerated because `hw.custSol` is hardcoded 16 for every Stern "
		"S.A.M. game, but nothing on this machine drives any of them; 33 is PinMAME's synthetic game-on "
		"state and the rest are dead address space. All carry a controlled `virtual` or `unused` record.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} address {entry['address']}: {entry['reason']}")
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
		f"- Devices with no `spatial` key at all: {len(report['unresolved'])}",
		"",
		"## Named spatial gaps",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Excluded retained objects",
		"",
	]
	for entry in report["excluded_object_classes"]:
		lines.append(f"- {entry}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. Two output addresses have no spatial record, four "
		"conflicts remain unresolved (`conflict.sam-invsw-never-populated`, "
		"`conflict.flasher-back-panel-bulb-count`, `conflict.pop-bumper-position-naming`, "
		"`conflict.coin-door-adjust-button-order`), opto polarity is unsettled for all seven "
		"manual-identified opto addresses because pinned Stern S.A.M. source normalizes nothing. Recreation "
		"knowledge remains observed until the missing placements and polarity conflicts can be reconciled. The record therefore stays `partial` "
		"with `coverage.missing = [\"polarity\", \"recreation_notes\", \"spatial_placement\", \"unresolved_conflicts\"]` and "
		"`coverage.dimensions.physical_wiring = \"conflicted\"`.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Curation record of which manual pages were rendered and read, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- Full per-object geometry dump of the retained extraction, SHA-256 `{VPX_GEOMETRY_SHA256}`.",
		f"- Committed, digest-verified manual transcriptions under `{EXCERPT_ROOT}/`.",
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
	stale_author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready.exists():
		stale_author_ready.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_author_ready_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready_path.exists():
		raise RuntimeError(f"Stale Pirates of the Caribbean author-ready definition is still present: {stale_author_ready_path}")
	for superseded in (SUPERSEDED_STUB_PATH, SUPERSEDED_STUB_KNOWLEDGE_PATH):
		superseded_path = root / superseded.relative_to(ROOT)
		if superseded_path.is_file():
			stub = load_json(superseded_path) if superseded_path.suffix == ".json" else None
			if stub is not None and stub["machine"]["id"] != "stub.pinmame.potc_600af":
				raise RuntimeError(f"Unexpected content at the superseded stub path: {superseded_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Pirates of the Caribbean definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Pirates of the Caribbean seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Pirates of the Caribbean definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Pirates of the Caribbean seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Pirates of the Caribbean spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Pirates of the Caribbean spatial review drifted from its deterministic curator: {markdown_path}")
	print("Pirates of the Caribbean definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Pirates of the Caribbean extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Pirates of the Caribbean retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
