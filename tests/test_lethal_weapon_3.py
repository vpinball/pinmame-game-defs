"""Gates for the Data East Lethal Weapon 3 (1992) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major
address arithmetic, the two cabinet flipper addresses PinMAME mirrors, the Left/Right relay pairing, and
the boundary between what the retained recreation measured and what it did not.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/data-east/lethal-weapon-3-1992.json"
SEED_PATH = ROOT / "tools/seeds/data-east/lethal-weapon-3-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/lethal-weapon-3-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/lethal-weapon-3-1992.md"


# Independently maintained fixtures, transcribed from the printed charts and kept apart from the
# curator on purpose. A test that checks the generator against its own output only proves the
# generator is self-consistent; these are the check on whether it is right.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 2: "4th Coin", 3: "Credit Button", 4: "Right Coin", 5: "Center Coin", 6: "Left Coin", 7: "Slam Tilt", 8: None,
    9: "Launch Trigger", 10: "Outhole", 11: "Trough #1 Left", 12: "Trough #2 Center", 13: "Trough #3 Right", 14: "Shooter Lane", 15: "Left EOS", 16: "Right EOS",
    17: "Left 4 Bank Top 4", 18: "Left 4 Bank Mid. 3", 19: "Left 4 Bank Mid. 2", 20: "Left 4 Bank Bot. 1", 21: "Left Orbit Rollover", 22: "Right Orbit Rollover", 23: None, 24: None,
    25: "Center Drop Tar. Left", 26: "Center Drop Tar. Mid.", 27: "Center Drop Tar. Right", 28: "Left Outlane", 29: "Left Return", 30: "Left Slingshot", 31: "VUK", 32: "Right Saucer",
    33: "Right Drop Tar. Top", 34: "Right Drop Tar. Mid.", 35: "Right Drop Tar. Bot.", 36: "Right Outlane", 37: "Right Return", 38: "Right Slingshot", 39: "Left Stand-Up Target", 40: "Left Saucer",
    41: "Left Top Lane", 42: "Center Top Lane", 43: "Right Top Lane", 44: "Left Turbo Bumper", 45: "Center Turbo Bumper", 46: "Right Turbo Bumper", 47: "Left Spinner", 48: "Right Spinner",
    49: "Ramp Entrance", 50: "Ramp Exit", 51: None, 52: "Right 10 Point", 53: None, 54: "Left Orbit R.O. Back Up", 55: "Right Orbit R.O. Back Up", 56: None,
    57: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None,
}
# The adjacent Switch Part Numbers table is more specific than the matrix chart for these two
# addresses and explicitly marks both with the legend "* Indicates Cabinet Switches".
MANUAL_SWITCH_PARTS = {
    15: ("Left Flipper Cabinet Button", "Left Flip. Cab", "180-5048-01"),
    16: ("Right Flipper Cabinet Button", "Right Flip. Cab.", "180-5048-01"),
}
# A sample across all eight printed lamp columns rather than all 64, because the point is to be an
# independent check on lamp identity, not a second copy of the chart.
MANUAL_LAMPS = {
    1: "UziClip Bottom 1",
    8: "Bullet Proof Vest",
    9: "Start Getaway",
    16: "Lethal Weap.1,23 10 Mill.",
    17: "Shoot Again",
    24: "Right Drop Tar. Bot.",
    25: "Lite Karate Kick",
    32: "Bonus Multiplier & Hold",
    33: "Cab.-Start Button",
    40: "Extra Ball",
    41: "Ramp Looping",
    48: "Left Bank 4 Bot.",
    49: "3 Million",
    56: "Video Mode",
    57: "Karate Kick",
    64: "Leo Getz",
}
# Lamp 33 is the one cabinet lamp on this machine (Batman's was 54).
MANUAL_CABINET_LAMPS = {33}
# Right-side bulb composition per drive, from the Special Coil Wiring Diagram. Unlike Batman,
# every right-side group on this machine is No. 89 only - which is why the claim is pinned here
# rather than restated in prose.
MANUAL_RIGHT_SIDE_BULBS = {1: "(4) No. 89", 2: "(4) No. 89", 3: "(4) No. 89", 4: "(3) No. 89", 5: "(4) No. 89", 6: "(3) No. 89", 7: "(4) No. 89", 8: "(4) No. 89"}
MANUAL_FLASH_QUANTITIES = {9: 4, 16: 4, 25: 4, 26: 4, 27: 4, 28: 3, 29: 4, 30: 3, 31: 4, 32: 4}
# The printed left halves that carry no coil.
MANUAL_UNFITTED_LEFT_DRIVES = {3}


def switch_addresses_the_script_asserts(text: str) -> set[int]:
    """Every switch address the retained script writes, comments removed first.

    Whole-line apostrophe comments are stripped because a commented-out
    `'Sub Sw14_UnHit:Controller.Switch(14)=0` is not a script assertion - that exact trap already
    produced one wrong coordinate in this contribution. Matching is case-insensitive: VPW 2.0
    writes `Controller.switch(31)` in lower case, and a case-sensitive scan silently misses it.

    Non-literal arguments are not resolvable here. VPW 2.0 contains one, `Controller.Switch(Switchid
    mod 100)`, so this set is a lower bound on what the script drives, never an upper bound. That
    asymmetry is safe for the only use below: proving a "the script never touches N" claim false.
    It could not be used to prove such a claim true.
    """
    active = "\n".join("" if line.lstrip().startswith("'") else line
                       for line in text.splitlines())
    controller = {int(n) for n in re.findall(
        r"Controller\s*\.\s*Switch\s*\(\s*(\d+)\s*\)", active, re.IGNORECASE)}
    pulses = {int(n) for n in re.findall(
        r"vpmTimer\s*\.\s*PulseSw\s+(\d+)\b", active, re.IGNORECASE)}
    return controller | pulses


# Pinned from the retained VPW 2.0 script, and rechecked against it by
# LethalWeapon3RetainedEvidenceTests whenever the evidence root is present. It is pinned rather
# than computed so the prose guard below runs in CI, which supplies no evidence root - a gate that
# only runs on the curator's own machine is not a gate.
SCRIPT_ASSERTED_SWITCHES = frozenset(
    {9, 10, 11, 12, 13, 15, 16, 21, 22, 28, 29, 30, 31, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54, 55})
# Ways of saying "the script leaves this address alone". Any of them is a factual claim about the
# retained script and is checked against SCRIPT_ASSERTED_SWITCHES.
SCRIPT_AVOIDANCE_PHRASES = (
    r"never touch\w*", r"does ?n[o']?t touch", r"never driv\w*", r"does ?n[o']?t drive",
    r"never writ\w*", r"does ?n[o']?t write", r"never assert\w*", r"does ?n[o']?t assert",
    r"never us\w*", r"avoids?", r"leaves? (?:\w+ ){0,3}alone", r"untouched",
)


def bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
    return {int(d["binding"]["device"]): d for d in definition[collection]
            if d["binding"]["group"] == group}


class LethalWeapon3DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
        cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

    def test_machine_identity(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual("data-east.lethal-weapon-3.1992", machine["id"])
        self.assertEqual("Data East", machine["manufacturer"])
        self.assertEqual(1992, machine["year"])
        self.assertEqual(2, self.definition["schema_version"])

    def test_the_clone_tree_is_exactly_the_nine_lw3_drivers(self) -> None:
        """Nine drivers, all `lw3_*`, all one physical machine.

        Three of the nine are later software rather than factory firmware - a 2013 voices mod and
        two 2020 community rulesets - which run on this same cabinet and so stay driver variants
        rather than becoming new games. Asserted because a release year is exactly the thing that
        tempts a split.
        """
        driver_ids = {driver["id"] for driver in self.definition["drivers"]}
        self.assertEqual({"lw3_200", "lw3_203", "lw3_205", "lw3_207", "lw3_208",
                          "lw3_208p", "lw3_300", "lw3_301", "lw3_e204"}, driver_ids)
        expected_years = {
            "lw3_200": "1992", "lw3_203": "1992", "lw3_205": "1992", "lw3_207": "1992",
            "lw3_208": "1992", "lw3_e204": "1992", "lw3_208p": "2013",
            "lw3_300": "2020", "lw3_301": "2020",
        }
        for driver in self.definition["drivers"]:
            self.assertTrue(driver["id"].startswith("lw3"), driver["id"])
            self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
            # An earlier revision hard-coded 1991 for all nine, which is Batman's year, not this
            # machine's. The three non-1992 entries are later software for the same cabinet.
            self.assertEqual(expected_years[driver["id"]], driver["year"], driver["id"])

    def test_matrices_are_column_major_and_full_width(self) -> None:
        """address = (column - 1) * 8 + row, for both matrices.

        Data East inherits PinMAME's sequential conversion (`core_m2swSeq(col,row) = col*8+row-7`)
        because s11.c installs no MDRV_SWITCH_CONV of its own. This is emphatically not the
        col*10+row that WPC games use, and both printed charts confirm it cell by cell.
        """
        # The two negative addresses are coin-door diagnostic buttons in switch column 0, not
        # matrix positions; everything from 1 to 64 is the matrix itself.
        self.assertEqual(set(range(1, 65)) | {-7, -6}, set(self.switches))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        for address in range(1, 65):
            column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
            for device in (self.switches[address], self.lamps[address]):
                notes = device["physical"]["notes"]
                self.assertIn(f"column {column}, row {row}", notes, f"address {address}")

    def test_data_east_publishes_only_two_diagnostic_buttons(self) -> None:
        """s11.h defines DE_SWADVANCE -7 and DE_SWUPDN -6 and stops.

        The -5 and -4 addresses beside them are S11_SWCPUDIAG and S11_SWSOUNDDIAG, which belong
        to Williams System 11 and not to Data East. Batman runs on the shared System 11 core
        source, which is exactly why the difference is worth a gate rather than an assumption.
        """
        negatives = {a for a in self.switches if a < 1}
        self.assertEqual({-7, -6}, negatives)
        for address in negatives:
            self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])

    def test_general_illumination_uses_the_gi_output_kind(self) -> None:
        """This platform has no GI channel, so a GI device is an ordinary solenoid address typed
        `gi` - the convention the System 11 profile states and the Whirlwind record follows."""
        self.assertEqual("gi", self.solenoids[11]["kind"])

    def test_synthetic_flipper_addresses_are_virtual_and_live(self) -> None:
        """45-48 have no driver-board output behind them on this platform: real hardware fires
        the coils straight from the cabinet button. The coil itself is real and its part number
        and wiring are recorded, but the ADDRESS is synthetic."""
        for address in (45, 46, 47, 48):
            self.assertEqual("virtual", self.solenoids[address]["kind"], address)
            self.assertEqual("used", self.solenoids[address]["availability"], address)
            self.assertIn("Synthetic", self.solenoids[address]["label"], address)

    def test_four_addresses_drive_two_emitters_each(self) -> None:
        """One lamp address, two bulbs at genuinely different playfield positions.

        Lamp 18's pair sits at x=64.6 and x=808.4 in the retained table - opposite sides. Both are
        placed rather than averaged, because a centroid between two real inserts is a coordinate
        with no bulb in it.
        """
        multi = {a for a, lamp in self.lamps.items()
                 if len(lamp.get("spatial", {}).get("placements", [])) > 1}
        self.assertEqual({7, 9, 18, 27}, multi)
        for address in multi:
            placements = self.lamps[address]["spatial"]["placements"]
            self.assertEqual(2, len(placements), address)
            self.assertEqual(2, len({p["id"] for p in placements}), address)
            self.assertNotEqual(placements[0]["x"], placements[1]["x"], address)

    def test_lamp_labels_match_the_printed_chart(self) -> None:
        """An independent check on lamp identity, not a second copy of the generator.

        A review showed that an invented `lamp.matrix-1` coordinate passed the entire suite,
        because only switches had a manual-derived fixture. Labels are what a fabricated or
        misbound lamp cannot fake without also contradicting the printed chart.
        """
        for address, expected in MANUAL_LAMPS.items():
            self.assertEqual(expected, self.lamps[address]["label"], address)

    def test_the_cabinet_lamp_is_not_placed_on_the_playfield(self) -> None:
        for address in MANUAL_CABINET_LAMPS:
            spatial = self.lamps[address]["spatial"]
            self.assertEqual("not_applicable", spatial["status"], address)
            self.assertEqual("cabinet_or_service", spatial["reason"], address)
        for address, lamp in self.lamps.items():
            if address in MANUAL_CABINET_LAMPS:
                continue
            self.assertNotEqual("cabinet_or_service", (lamp.get("spatial") or {}).get("reason"), address)

    def test_right_side_bulb_composition_matches_the_printed_diagram(self) -> None:
        """PinMAME types 25-32 uniformly as No. 89, and on this machine the manual agrees.

        An earlier revision carried a sibling machine's "four of the eight mix No. 906" sentence
        into all eight notes, which this machine's own committed excerpt contradicted.
        """
        for drive, bulbs in MANUAL_RIGHT_SIDE_BULBS.items():
            notes = self.solenoids[drive + 24]["physical"]["notes"]
            self.assertIn(bulbs, notes, drive)
            # Every right-side group on THIS machine is No. 89. An earlier revision carried a
            # sibling machine's "four of the eight mix No. 906" sentence into all eight notes,
            # which its own committed excerpt contradicted.
            self.assertNotIn("906", notes, drive)
            self.assertEqual(int(bulbs[1]), self.solenoids[drive + 24]["physical"]["quantity"])

    def test_every_lamp_address_is_populated(self) -> None:
        """Unusual, and worth a gate: the printed lamp matrix has no 'Not Used' cell at all."""
        self.assertEqual(64, len(self.lamps))
        for address, lamp in self.lamps.items():
            self.assertEqual("used", lamp["availability"], address)
            self.assertNotEqual("Not Used", lamp["label"], address)

    def test_no_lamp_address_above_the_hardware_ceiling(self) -> None:
        """`nLamps` is 64 on this hardware. The superseded legacy record listed 109 and 111-132,
        and the retained script binds 71 Lampz slots; both are recreation-side fictions."""
        self.assertEqual(64, max(self.lamps))

    def test_switches_15_and_16_publish_cabinet_flipper_button_state(self) -> None:
        """The matrix chart prints EOS, but the manual's parts table and PinMAME say buttons.

        core.c:1740-1741 writes the flipper button bits into the addresses named by
        FLIP_SWNO(15,16), and because this game declares no FLIP_SOL the EOS simulation never
        runs. A consumer cannot publish an end-of-stroke reading here, so the record has to say so.

        An earlier revision of this test demanded the sentence "The retained known-working VPW 2.0
        script indeed never touches 15 or 16", which is false: VPW 2.0 drives both from the cabinet
        flipper key. That sentence was true of the Data East Batman record this one was derived
        from, and the test locked the inherited claim in place instead of checking it. The
        assertions below now name the emulator behaviour and forbid the false claim; the retained
        script itself is checked in
        `LethalWeapon3RetainedEvidenceTests.test_no_note_claims_the_script_avoids_an_address_it_actually_drives`.
        """
        for address in (15, 16):
            notes = self.switches[address]["physical"]["notes"]
            # Identifiers, not phrasing. An earlier revision asserted whole sentences, which is how
            # the false claim got locked in: rewording the note broke the test, so the note stopped
            # being reworded. Each token below names a specific thing in the pinned source or the
            # retained script that the note must account for.
            for token in ("FLIP_SWNO(15,16)",   # which addresses the emulator claims
                          "core_setSw",          # how it writes them
                          "FLIP_SOL",            # why no EOS state is simulated
                          "p_rocEn",             # the mode in which it does not write them
                          "script.vbs:928-929"): # the retained script's own writes
                self.assertIn(token, notes, f"switch {address} note omits {token}")
            self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])

    def test_no_prose_claims_the_script_avoids_an_address_it_actually_drives(self) -> None:
        """The guard for the defect a blind re-derivation found in this record.

        Switches 15 and 16 carried "The retained known-working VPW 2.0 script indeed never touches
        15 or 16". True of the Data East Batman record this one was derived from - that table's
        VPW 1.1 script really does leave them alone - and false here: VPW 2.0 drives both from the
        cabinet flipper key at script.vbs:928-929 and 960-961. Fifty-two tests passed anyway,
        because the claim lived in prose nothing compared against the script.

        This runs with no evidence root, so CI exercises it. Three earlier weaknesses are closed:
        the address scan is case-insensitive (VPW 2.0 has a lower-case `Controller.switch(31)`),
        the phrase list is no longer three hand-picked wordings, and the knowledge note is scanned
        too - the first fix corrected the device notes and left the knowledge note asserting "A
        recreation must not drive 15 or 16", which a device-notes-only guard could never see.
        """
        # The subject may be named several ways in these artifacts - "the script", "VPW 2.0", "the
        # retained table". A pattern anchored on the bare word "script" missed "VPW 2.0 leaves
        # switch 16 alone", which is exactly how these notes tend to phrase it.
        pattern = re.compile(
            r"(?:script|VPW\s*[\d.]+|retained (?:table|recreation))[^.!?]*\b(?:"
            + "|".join(SCRIPT_AVOIDANCE_PHRASES) + r")\b", re.IGNORECASE)
        # Standalone one- and two-digit numbers only. A locator like `core.c:1733`, `1740-1741` or
        # `928-929` is a citation, not an address claim, and must not be mistaken for one.
        numbers = re.compile(r"(?<![\d.:-])(\d{1,2})(?![\d:-]|\.\d)")

        sources = []
        for device in self.definition["inputs"] + self.definition["outputs"]:
            notes = (device.get("physical") or {}).get("notes") or ""
            if notes:
                sources.append((device["id"], notes))
        sources.append(("knowledge/data-east/lethal-weapon-3-1992.md",
                        (ROOT / "knowledge/data-east/lethal-weapon-3-1992.md").read_text(encoding="utf-8")))

        def offending(origin: str, text: str) -> list[str]:
            found = []
            for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z(`*])", text):
                if not pattern.search(sentence):
                    continue
                overlap = {int(n) for n in numbers.findall(sentence)} & SCRIPT_ASSERTED_SWITCHES
                if overlap:
                    found.append(f"{origin} claims the script avoids {sorted(overlap)}: "
                                 f"{sentence.strip()!r}")
            return found

        # First prove the detector is not inert. A guard that matches nothing passes everything,
        # and the corrected artifacts contain no avoidance claim at all, so live prose cannot
        # demonstrate reachability. These are the exact sentences that shipped and were wrong.
        for historical in (
            "The retained known-working VPW 2.0 script indeed never touches 15 or 16.",
            "A recreation must not drive 15 or 16. The script never writes 15 or 16.",
            "The script does not touch 31 on this machine.",
            "VPW 2.0 leaves switch 16 alone.",
        ):
            self.assertTrue(offending("fixture", historical),
                            f"the detector failed to flag a known-false claim: {historical!r}")
        # A true avoidance claim about an address the script really does leave alone must pass.
        # Keep the sentence-final period: the guard must see an address before punctuation while
        # still ignoring decimal versions such as VPW 2.0 and source locators such as core.c:1733.
        self.assertFalse(offending("fixture", "The script never touches 51."))
        self.assertTrue(offending("fixture", "The script never touches 44."))

        problems = [p for origin, text in sources for p in offending(origin, text)]
        self.assertEqual([], problems, "\n".join(problems))

    def test_general_illumination_is_solenoid_11_and_there_is_no_gi_group(self) -> None:
        """Three sources agree: s11.c's own '// GI output' comment, the manual's printed
        'General Illumination Relay', and the retained script's own 'GI Relay callback."""
        self.assertEqual("General Illumination Relay", self.solenoids[11]["label"])
        self.assertIn("playfield.general-illumination", self.solenoids[11].get("roles", []))
        groups = {d["binding"]["group"] for d in self.definition["outputs"]}
        self.assertNotIn("pinmame.output.gi", groups,
                         "Data East publishes no GI channel; nGI is never assigned in s11.c")

    def test_the_relay_gates_all_eight_right_side_outputs(self) -> None:
        """The prose says solenoid 10 gates the whole 25-32 block, so all eight are stated.

        An earlier draft declared the relationship for drive 1 only while claiming the block, and
        paired it with a coil.driver-11 to coil.driver-11 self-loop that asserted nothing.
        """
        gated = {r["destination"] for r in self.definition["relationships"]
                 if r["kind"] == "relay_gated" and r["source"] == "coil.driver-10"}
        self.assertEqual({"flasher.driver-%d-right" % d for d in range(1, 9)}, gated)
        ids = {d["id"] for collection in ("inputs", "outputs") for d in self.definition[collection]}
        for relationship in self.definition["relationships"]:
            self.assertIn(relationship["source"], ids, relationship["id"])
            self.assertIn(relationship["destination"], ids, relationship["id"])
            self.assertNotEqual(relationship["source"], relationship["destination"], relationship["id"])

    def test_manual_page_count_comes_from_recorded_metadata(self) -> None:
        """A draft interpolated the switch-matrix PDF page NUMBER where the page COUNT belonged and
        published "28 pages" for a 93-page document, in prose the ledger then contradicted."""
        import curate_lethal_weapon_3 as curator

        self.assertEqual(93, curator.TRANSCRIPTION["document"]["page_count"])
        self.assertEqual(0, curator.TRANSCRIPTION["document"]["character_count"])
        self.assertIn("93 pages", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

    def test_evidence_excerpts_exist_and_match_their_recorded_digests(self) -> None:
        """A hash proves the local copy has not changed; it says nothing about what the document
        said. This manual is a 93-page image-only scan, so the regions actually read are committed
        beside the definition and digest-checked here."""
        import hashlib

        by_id = {s["id"]: s for s in self.definition["sources"]}
        manual = by_id["manual.data-east.lethal-weapon-3.1992"]
        addendum = by_id["manual-addendum.data-east.lethal-weapon-3.1992"]
        # Each excerpt hangs off the document it was read from. An earlier revision attached the
        # addendum's transcription to the operations manual, so the digest described a document
        # that source did not name.
        self.assertEqual(3, len(manual["excerpts"]))
        self.assertEqual(1, len(addendum["excerpts"]))
        self.assertEqual("excerpt.lethal-weapon-3.addendum", addendum["excerpts"][0]["id"])
        for excerpt in manual["excerpts"] + addendum["excerpts"]:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), excerpt["path"])
            self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])

    def test_retained_table_and_extraction_are_hash_pinned(self) -> None:
        """A coordinate is only reproducible if the extraction it came from is pinned."""
        by_id = {s["id"]: s for s in self.definition["sources"]}
        for source_id in ("vpx-table.lethal-weapon-3-vpw-2-0", "vpx-script.lethal-weapon-3-vpw-2-0",
                          "vpx-extraction.lethal-weapon-3-vpw-2-0"):
            self.assertIn(source_id, by_id, source_id)
            self.assertRegex(by_id[source_id]["sha256"], r"^[0-9a-f]{64}$", source_id)

    def test_left_right_relay_pairs_drives_1_to_8_with_25_to_32(self) -> None:
        """The relay switches +32 V between a coil and a flash-lamp group on the same drive.

        s11.c:564-574 re-routes outputs 1-8 to 25-32 when the mux solenoid is energised, and the
        manual describes the identical mechanism in prose. Every right half on this machine is
        flash lamps, which is why 22 drivers yield the manual's "29 regular coils".
        """
        self.assertEqual("Left/Right Coil Relay", self.solenoids[10]["label"])
        for drive in range(1, 9):
            right = self.solenoids[drive + 24]
            self.assertEqual("flasher", right["kind"], drive)
            self.assertIn(f"left half is published at address {drive}", right["physical"]["notes"])
            self.assertIn(f"right half is published at address {drive + 24}",
                          self.solenoids[drive]["physical"]["notes"])

    def test_drive_six_is_the_center_drop_bank_despite_the_printed_alias(self) -> None:
        drive = self.solenoids[6]
        self.assertIn("Center Drop-Target Bank Reset", drive["label"])
        self.assertIn("Left 3 Bank", drive["label"])
        self.assertIn("callout 6L", drive["physical"]["notes"])
        self.assertIn("dtM", drive["physical"]["notes"])

    def test_drive_three_fitment_conflict_is_not_silently_decided(self) -> None:
        drive = self.solenoids[3]
        self.assertEqual("unknown", drive["availability"])
        self.assertNotIn("spatial", drive)
        self.assertIn("NO COIL AT THIS LOCATION", drive["physical"]["notes"])
        self.assertIn("3L callout", drive["physical"]["notes"])
        self.assertEqual("used", self.solenoids[27]["availability"])

    def test_addresses_33_to_44_are_inert(self) -> None:
        """core_getSol only serves 33-36 for GEN_ALLWPC/GEN_SAM, and the S11 extra block at 37-44
        is written only under S11_SNDOVERLAY or S11_PRINTERLINE, neither of which this game sets."""
        for address in range(33, 45):
            device = self.solenoids[address]
            self.assertEqual("virtual", device["kind"], address)
            self.assertEqual("unused", device["availability"], address)

    def test_flipper_coils_are_synthesised_in_pairs(self) -> None:
        """No FLIP_SOL, so core.c fabricates 45-48 from Game On plus button state; power and hold
        assert together and must not be modelled as independent coils."""
        for address in (45, 46, 47, 48):
            notes = self.solenoids[address]["physical"]["notes"]
            self.assertIn("synthesis", notes.lower(), address)
            self.assertIn("not independently controllable", notes, address)

    def test_no_custom_solenoids_are_published(self) -> None:
        """lw3GameData declares custSol = 0, so CORE_FIRSTCUSTSOL (51) upward is empty."""
        self.assertEqual(50, max(self.solenoids))

    def test_cabinet_column_is_not_placed_on_the_playfield(self) -> None:
        """Matrix column 1 is the dedicated cabinet/coin column per DE_COMPORTS."""
        for address in (1, 3, 4, 5, 6, 7):
            spatial = self.switches[address]["spatial"]
            self.assertEqual("not_applicable", spatial["status"], address)
            self.assertEqual("cabinet_or_service", spatial["reason"], address)

    def test_switch_labels_and_availability_match_the_printed_chart(self) -> None:
        """Checked against the independent fixture, not the curator's own transcription.

        This is what stops a wrong definition from regenerating cleanly: the address set, every
        label, and every NOT USED position have to agree with the manual as transcribed here
        separately from the generator.
        """
        for address, expected in MANUAL_SWITCHES.items():
            switch = self.switches[address]
            if expected is None:
                self.assertEqual("unused", switch["availability"], f"switch {address} is printed NOT USED")
            else:
                self.assertEqual("used", switch["availability"], address)
                canonical = MANUAL_SWITCH_PARTS.get(address, (expected,))[0]
                self.assertEqual(canonical, switch["label"], address)
                if address in MANUAL_SWITCH_PARTS:
                    _, printed_part_label, part_number = MANUAL_SWITCH_PARTS[address]
                    self.assertIn(expected, switch["physical"]["notes"], address)
                    self.assertIn(printed_part_label, switch["physical"]["notes"], address)
                    self.assertIn(part_number, switch["physical"]["notes"], address)

    def test_no_placement_exists_for_an_address_the_manual_prints_not_used(self) -> None:
        """The check that would catch an invented binding.

        Driven by the independent fixture rather than by the definition's own `availability`,
        because a wrong definition that flipped an address to `used` would otherwise be skipped by
        this guard entirely - which is exactly how it could smuggle in a fabricated coordinate.
        """
        for address, expected in MANUAL_SWITCHES.items():
            if expected is not None:
                continue
            switch = self.switches[address]
            self.assertNotIn("placements", switch.get("spatial", {}), address)
            self.assertEqual("not_applicable", switch["spatial"]["status"], address)

    def test_unfitted_left_halves_match_the_printed_wiring_diagram(self) -> None:
        for drive in range(1, 9):
            expected = "unknown" if drive in MANUAL_UNFITTED_LEFT_DRIVES else "used"
            self.assertEqual(expected, self.solenoids[drive]["availability"], drive)
            self.assertEqual("used", self.solenoids[drive + 24]["availability"], drive)
            self.assertIn(MANUAL_RIGHT_SIDE_BULBS[drive], self.solenoids[drive + 24]["physical"]["notes"], drive)

    def test_every_driver_note_names_every_rom_that_differs(self) -> None:
        """The ROM-composition rule checked as data, not trusted to the builder's guard."""
        import curate_lethal_weapon_3 as curator

        root_roms = curator.ROM_SETS["lw3_208"]["roms"]
        notes = {d["id"]: d["variant_notes"] for d in self.definition["drivers"]}
        self.assertEqual(set(notes), set(curator.ROM_SETS))
        for driver_id, entry in curator.ROM_SETS.items():
            if driver_id == "lw3_208":
                continue
            for role, mine, theirs in zip(("CPU", "display 1", "display 0"), entry["roms"], root_roms):
                if mine != theirs:
                    self.assertIn(mine, notes[driver_id], f"{driver_id}: {role} ROM {mine}")

    def test_the_voices_mod_is_the_only_set_with_different_sound_roms(self) -> None:
        """This tree is not uniform in its sound ROMs, and the exception is named.

        Eight of the nine sets share lw3u7/lw3u17/lw3u21. `lw3_208p` swaps two of the three for
        `_vm` variants, which is what makes it the Voices Mod. Asserting "all identical" across
        this tree would have been false.
        """
        import curate_lethal_weapon_3 as curator

        by_sound = {}
        for driver_id, entry in curator.ROM_SETS.items():
            by_sound.setdefault(tuple(entry["roms"][3:]), []).append(driver_id)
        self.assertEqual(2, len(by_sound), "expected exactly one sound-ROM variant in this tree")
        odd = [ids for ids in by_sound.values() if len(ids) == 1]
        self.assertEqual([["lw3_208p"]], odd)
        self.assertIn("lw3u17_vm.dat", curator.ROM_SETS["lw3_208p"]["roms"])

    def test_mechanism_topology_follows_the_known_working_script(self) -> None:
        """The script is authoritative for runtime causality, and here it settles two things.

        The Special Coil Wiring Diagram draws the mars light on a node both drive 13 and drive 14
        touch, and prints "NO COIL AT THIS LOCATION" against 13, so the drawing alone cannot say
        which energises the beacon. `SolCallback(14) = "SolRotateBeacons"` does. Separately the
        drop-target banks are real drop targets - the script builds DropTarget instances for
        25-27 and 33-35 - while 17-20 gets none, so that bank is not claimed as one.
        """
        by_id = {m["id"]: m for m in self.definition["mechanisms"]}

        self.assertEqual(["coil.driver-14"], by_id["mechanism.mars-light"]["actuators"])
        self.assertEqual([], by_id["mechanism.mars-light"]["sensors"])
        # A mechanism's actuator must be a device that exists and is used. An earlier revision
        # named drive 14 as the actuator while encoding it "virtual"/"unknown" as an unfitted
        # driver, so the record contradicted itself and this test required the wrong value.
        self.assertEqual("used", self.solenoids[14]["availability"])
        self.assertEqual("motor", self.solenoids[14]["kind"])
        self.assertIn("Mars Light", self.solenoids[14]["label"])
        self.assertEqual("unused", self.solenoids[13]["availability"],
                         "drive 13 is printed NO COIL AT THIS LOCATION")
        self.assertEqual("virtual", self.solenoids[13]["kind"])

        self.assertEqual(["coil.driver-6"], by_id["mechanism.center-drop-bank"]["actuators"])
        self.assertEqual(["coil.driver-7"], by_id["mechanism.right-drop-bank"]["actuators"])
        for mechanism_id in ("mechanism.center-drop-bank", "mechanism.right-drop-bank"):
            self.assertEqual("drop_target_bank", by_id[mechanism_id]["kind"], mechanism_id)
            self.assertEqual(3, len(by_id[mechanism_id]["positions"]), mechanism_id)
        self.assertNotEqual("drop_target_bank", by_id["mechanism.left-four-bank"]["kind"])
        self.assertEqual([], by_id["mechanism.left-four-bank"]["actuators"])
        self.assertIn("180-5082-06", by_id["mechanism.left-four-bank"]["behavior"])

        locks = by_id["mechanism.ball-locks"]
        self.assertIn("bsLock with sw40", locks["behavior"])
        self.assertIn("bsLock2 with sw32", locks["behavior"])

        for mechanism in self.definition["mechanisms"]:
            self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])

        ids = {d["id"] for collection in ("inputs", "outputs") for d in self.definition[collection]}
        for mechanism in self.definition["mechanisms"]:
            for reference in mechanism["actuators"] + mechanism["sensors"]:
                self.assertIn(reference, ids, mechanism["id"])

    def test_the_addendum_is_a_source_and_it_corrects_the_display(self) -> None:
        """The manual as printed says the DMD is 32x64 and is wrong.

        The factory addendum of 2 July 1992 corrects it to 32x128, which is what pinned PinMAME
        independently declares. Without the addendum the manual and the emulator would appear to
        disagree and the manual would be the wrong side to believe, so the addendum is recorded as
        its own source rather than folded into the manual's.
        """
        by_id = {s["id"]: s for s in self.definition["sources"]}
        addendum = by_id["manual-addendum.data-east.lethal-weapon-3.1992"]
        self.assertRegex(addendum["sha256"], r"^[0-9a-f]{64}$")
        display = self.definition["displays"][0]
        self.assertEqual((128, 32), (display["width"], display["height"]))
        self.assertIn("manual-addendum.data-east.lethal-weapon-3.1992",
                      display["provenance"]["source_refs"])

    def test_script_bound_flasher_and_gi_emitters_are_placed_individually(self) -> None:
        """The exact retained script binds these solenoids to exact Light objects."""
        expected_counts = {9: 2, 11: 35, 16: 1, 25: 1, 26: 2, 27: 2, 28: 3, 29: 2, 30: 4, 31: 1, 32: 2}
        for address, count in expected_counts.items():
            output = self.solenoids[address]
            self.assertIn(output["kind"], {"flasher", "gi"}, address)
            spatial = output["spatial"]
            self.assertEqual("observed", spatial["status"], address)
            self.assertEqual(count, len(spatial["placements"]), address)
            for placement in spatial["placements"]:
                self.assertEqual("emitter" if address == 11 else "effect", placement["role"], address)
                self.assertEqual("playfield", placement["space"], address)
                self.assertGreaterEqual(placement["x"], 0.0, address)
                self.assertLessEqual(placement["x"], 1.0, address)
                self.assertGreaterEqual(placement["y"], 0.0, address)
                self.assertLessEqual(placement["y"], 1.0, address)
            if address in MANUAL_FLASH_QUANTITIES:
                self.assertEqual(MANUAL_FLASH_QUANTITIES[address], output["physical"]["quantity"], address)
                if count != MANUAL_FLASH_QUANTITIES[address]:
                    self.assertIn("presentation effect", output["physical"]["notes"], address)

        self.assertEqual("cabinet_or_service", self.solenoids[14]["spatial"]["reason"])

    def test_conflicts_are_declared_and_counted(self) -> None:
        ids = {c["id"] for c in self.definition["conflicts"]}
        self.assertEqual({"conflict.drive-3-left-fitment", "conflict.drive-6-flasher-effect-count"}, ids)
        self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

    def test_no_other_machine_leaks_into_this_record(self) -> None:
        """The guard that would have caught four blockers at once.

        This record was derived from the Data East Batman curator, and that propagated Batman's
        facts into prose no fixture checked: `btmnGameData`, `GEN_DEDMD16`, a VPW 1.1 script, a
        No. 906 bulb mix, and 1991 driver years all survived into a 1992 machine's artifacts while
        48 tests passed. Structure was checked; inherited sentences were not.

        Cross-machine comparison is legitimate in a knowledge note or the ledger, where it is
        narrative. It is not legitimate in a device note, whose `source_refs` cover this machine's
        evidence only. So the definition, the seed and the spatial report must be free of any
        other machine's identifiers.
        """
        import json as _json

        # Derived, not hand-listed. Every OTHER machine's id, driver prefixes and short name are
        # forbidden, plus the generation constants and table builds this record must not claim.
        # An earlier revision was a nine-token blacklist that checked "VPW v1.1" when the string
        # that actually leaked was "VPW 1.1", and omitted "1991" entirely - so it would NOT have
        # caught the blockers it was written for.
        this_id = self.definition["machine"]["id"]
        catalog = load_json(ROOT / "catalog/pinmame.json")
        foreign = set()
        for record in catalog["machines"]:
            other = record.get("id") or ""
            if not other or other == this_id:
                continue
            # Full ids only. A "short name" heuristic produced tokens like `pinball`, which fires
            # inside this record's own `physical_pinball` kind, and a guard that cries wolf gets
            # deleted rather than fixed.
            foreign.add(other)
        for driver in catalog["drivers"]:
            if driver.get("machine_id") and driver["machine_id"] != this_id:
                foreign.add(driver["id"])
        foreign -= {"lethal-weapon-3", "lw3"}
        # Catalog aliases get a length floor because short driver ids fire inside ordinary English
        # (PinMAME has a driver called `ator`, which matches "actuator"). These explicit tokens do
        # NOT: an earlier revision listed "1991" and then skipped it for being four characters, so
        # the guard advertised a check it did not perform.
        explicit = {"GEN_DEDMD16", "GEN_WS", "No. 906", "VPW 1.1", "VPW v1.1",
                    "1991", "Batman", "btmnGameData", "btmn"}
        # The knowledge note is scanned too. It is machine-facing prose with the same obligation as
        # a device note, and it is where the first correction pass left a stale directive standing.
        #
        # `tools/curate_lethal_weapon_3.py` is deliberately NOT scanned. Its only cross-machine
        # mentions are explanatory code comments - "which was Batman's year", "not Batman's four" -
        # recording why a value is what it is. That is exactly the narrative comparison the ledger
        # permits outside device notes, and scanning it would force the reasoning to be deleted to
        # satisfy a guard aimed at something else.
        knowledge = ROOT / "knowledge/data-east/lethal-weapon-3-1992.md"
        blobs = [(path.name, _json.dumps(load_json(path)))
                 for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH)]
        blobs.append((knowledge.name, knowledge.read_text(encoding="utf-8")))
        for name, blob in blobs:
            for needle in sorted(n for n in foreign if len(n) >= 5) + sorted(explicit):
                self.assertIsNone(
                    re.search(r"(?<![A-Za-z0-9_])" + re.escape(needle) + r"(?![A-Za-z0-9_])", blob),
                    f"{name} carries '{needle}' from another machine")

    def test_no_two_devices_share_a_coordinate(self) -> None:
        """Regression for the bug a commented-out line caused.

        The resolver did not strip VBScript comments, and a handler body ran to the next
        UNcommented `Sub`, so `Controller.Switch(14)` sitting inside a disabled
        `'Sub Sw14_UnHit:` line was attributed to the Sw52 object. Switch 14 and switch 52 ended
        up sharing one identical coordinate. Nothing caught it, because the gates checked counts
        and origins rather than the coordinates themselves.

        Co-located devices are real - four lamp addresses here legitimately drive two emitters -
        so the rule is per-address: two DIFFERENT addresses may not sit on the exact same point
        unless that sharing is declared.
        """
        seen = {}
        for collection in ("inputs", "outputs"):
            for device in self.definition[collection]:
                group = device["binding"]["group"]
                for placement in device.get("spatial", {}).get("placements", []):
                    point = (group, placement["x"], placement["y"])
                    other = seen.get(point)
                    self.assertIsNone(
                        other,
                        f"{device['id']} shares the exact coordinate of {other} at {point[1:]}")
                    seen[point] = device["id"]

    def test_every_mechanism_actuator_is_a_used_device(self) -> None:
        """A mechanism cannot be driven by an address the record calls unfitted.

        The mars light was named as drive 14's mechanism while drive 14 was encoded as an unfitted
        virtual driver, and nothing rejected the contradiction.
        """
        outputs = {d["id"]: d for d in self.definition["outputs"]}
        for mechanism in self.definition["mechanisms"]:
            for actuator in mechanism["actuators"]:
                self.assertIn(actuator, outputs, mechanism["id"])
                self.assertEqual("used", outputs[actuator]["availability"],
                                 f"{mechanism['id']} is driven by {actuator}, which is not used")

    def test_promotion_state_is_partial(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["output_semantics", "polarity", "spatial_placement", "unresolved_conflicts"], coverage["missing"])


class LethalWeapon3SpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.report = load_json(SPATIAL_REPORT_PATH)

    def test_playfield_is_the_retained_tables_own_extent(self) -> None:
        """952 x 2162, asserted rather than assumed.

        This happens to be the common WPC-era extent, unlike the Batman recreation's 1974 - which
        is exactly why it is pinned. A machine whose bounds match the common case is where an
        assumed divisor goes unnoticed, and the resolver hard-fails on anything else.
        """
        playfield = self.definition["machine"]["playfield"]
        self.assertEqual(952.0, playfield["width"])
        self.assertEqual(2162.0, playfield["height"])
        self.assertEqual("vpx", playfield["units"])

    def test_report_is_a_blocker_report_for_a_partial_machine(self) -> None:
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])
        self.assertEqual("data-east.lethal-weapon-3.1992", self.report["machine_id"])

    def test_placement_count_matches_the_definition(self) -> None:
        placements = sum(
            len(device.get("spatial", {}).get("placements", []))
            for collection in ("inputs", "outputs")
            for device in self.definition[collection])
        self.assertEqual(placements, self.report["placement_count"])
        self.assertGreater(placements, 0)

    def test_every_used_switch_is_located_or_definitively_not_applicable(self) -> None:
        for item in self.definition["inputs"]:
            if item["kind"] != "switch" or item["availability"] != "used":
                continue
            spatial = item.get("spatial")
            self.assertIsNotNone(spatial, item["id"])
            if spatial["status"] == "not_applicable":
                self.assertIn(spatial["reason"], {"cabinet_or_service", "dip_switch"}, item["id"])
            else:
                self.assertEqual("observed", spatial["status"], item["id"])
                self.assertGreater(len(spatial["placements"]), 0, item["id"])
        self.assertEqual([], self.report["unresolved"]["switches"])

    def test_spatial_blocker_names_every_used_or_unknown_device_without_a_coordinate(self) -> None:
        blocker = next(item for item in self.report["blockers"] if item["id"] == "devices-without-a-retained-object")
        recorded = set(blocker["internal_nonvisual_devices"]) | set(blocker["omitted_spatial_key_devices"])
        expected = set()
        for collection in ("inputs", "outputs"):
            for item in self.definition[collection]:
                if item["availability"] not in {"used", "unknown"}:
                    continue
                spatial = item.get("spatial")
                if spatial is None or (spatial["status"] == "not_applicable" and spatial.get("reason") == "internal_nonvisual"):
                    expected.add(item["id"])
        self.assertEqual(expected, recorded)

    def test_computed_centroids_are_reported_separately_from_measurements(self) -> None:
        """A centroid of an extended object's drag points is a derivation, not an observation.

        Walls, ramps and rubbers carry no center at all, so their coordinate is computed. Letting
        that pass as a measurement is precisely the error that demoted Bally Centaur.
        """
        origins = self.report["coordinate_origins"]
        self.assertGreater(origins["computed_centroid"], 0)
        self.assertEqual(self.report["placement_count"],
                         origins["measured_center"] + origins["computed_centroid"])
        # Devices are named by canonical id, never by bare address: switch 17 and lamp 17 are
        # different devices and a numeric-only audit cannot tell them apart.
        devices = origins["computed_devices"]
        self.assertEqual(origins["computed_centroid"], len(devices))
        self.assertEqual(sorted(set(devices)), sorted(devices), "duplicate device in the centroid audit")
        ids = {d["id"] for collection in ("inputs", "outputs") for d in self.definition[collection]}
        for device_id in devices:
            self.assertRegex(device_id, r"^(?:(?:switch|lamp)[.]matrix|coil[.]driver)-[0-9]+$", device_id)
            self.assertIn(device_id, ids, device_id + " is audited but absent from the definition")

    def test_every_placement_is_observed_because_only_one_table_was_retained(self) -> None:
        for collection in ("inputs", "outputs"):
            for device in self.definition[collection]:
                for placement in device.get("spatial", {}).get("placements", []):
                    self.assertEqual("observed", placement["provenance"]["status"], device["id"])

    def test_single_recreation_is_declared_a_blocker(self) -> None:
        ids = {b["id"] for b in self.report["blockers"]}
        self.assertIn("single-retained-recreation", ids)

    def test_standup_targets_use_the_retained_hit_target_centers(self) -> None:
        inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]
                  if item["kind"] == "switch"}
        expected = {
            17: (0.09751, 0.362563),
            18: (0.108582, 0.388027),
            19: (0.120202, 0.413487),
            20: (0.132375, 0.440165),
            39: (0.104045, 0.578682),
        }
        for address, point in expected.items():
            placement = inputs[address]["spatial"]["placements"][0]
            self.assertEqual(point, (placement["x"], placement["y"]), address)

    def test_launch_trigger_is_a_cabinet_control(self) -> None:
        launch = next(item for item in self.definition["inputs"]
                      if item["binding"]["device"] == 9)
        self.assertEqual(["cabinet.launch"], launch["roles"])
        self.assertEqual("not_applicable", launch["spatial"]["status"])
        self.assertEqual("cabinet_or_service", launch["spatial"]["reason"])

    def test_ball_path_and_orbit_backup_switches_use_exact_retained_objects(self) -> None:
        inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]
                  if item["kind"] == "switch"}
        expected = {
            10: (0.471004, 0.962556),
            11: (0.721638, 0.901326),
            12: (0.796335, 0.882002),
            13: (0.863672, 0.864162),
            54: (0.077806, 0.09892),
            55: (0.927818, 0.197142),
        }
        for address, point in expected.items():
            spatial = inputs[address]["spatial"]
            self.assertEqual("observed", spatial["status"], address)
            placement = spatial["placements"][0]
            self.assertEqual(point, (placement["x"], placement["y"]), address)

    def test_flipper_buttons_are_cabinet_controls(self) -> None:
        inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]
                  if item["kind"] == "switch"}
        for address, side in ((15, "left"), (16, "right")):
            switch = inputs[address]
            self.assertEqual([f"cabinet.flipper.{side}-button"], switch["roles"])
            self.assertEqual("not_applicable", switch["spatial"]["status"])
            self.assertEqual("cabinet_or_service", switch["spatial"]["reason"])


class LethalWeapon3CuratorTests(unittest.TestCase):
    def test_seed_is_byte_identical_to_the_definition(self) -> None:
        self.assertEqual(SEED_PATH.read_bytes(), DEFINITION_PATH.read_bytes())

    def test_curator_check_is_idempotent(self) -> None:
        import curate_lethal_weapon_3 as curator

        curator._check(ROOT)
        curator._check(ROOT)

    def test_curator_check_rejects_edited_artifacts(self) -> None:
        import shutil
        import tempfile

        import curate_lethal_weapon_3 as curator

        owned = {path.relative_to(ROOT) for path, _ in curator._artifacts()}
        self.assertGreaterEqual(len(owned), 4)
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for relative in owned:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            curator._check(root)
            for relative in owned:
                target = root / relative
                original = target.read_bytes()
                target.write_bytes(original + b"\n")
                with self.assertRaises(RuntimeError, msg=f"editing {relative} was not detected"):
                    curator._check(root)
                target.write_bytes(original)
            curator._check(root)

    def test_curator_check_survives_a_crlf_checkout_but_still_refuses_a_reformat(self) -> None:
        """The gate forgives line endings and nothing else.

        Git's Windows default core.autocrlf=true rewrites every LF in the working tree, so an
        untouched clone would otherwise fail this gate for a reason unrelated to curation. A
        normalisation loose enough to also forgive reformatting would undo the byte-exactness the
        comparison exists for, so both halves are asserted.
        """
        import shutil
        import tempfile

        import curate_lethal_weapon_3 as curator

        owned = {path.relative_to(ROOT) for path, _ in curator._artifacts()}
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for relative in owned:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
                target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            curator._check(root)
            definition = root / DEFINITION_PATH.relative_to(ROOT)
            definition.write_bytes(
                (json.dumps(load_json(definition), indent=4, sort_keys=True) + "\n").encode("utf-8"))
            with self.assertRaises(RuntimeError, msg="a reformatted definition must still be refused"):
                curator._check(root)

    def test_curator_requires_an_explicit_mode(self) -> None:
        import curate_lethal_weapon_3 as curator

        argv = sys.argv
        sys.argv = ["curate_lethal_weapon_3.py"]
        try:
            with self.assertRaises(SystemExit):
                curator.main()
        finally:
            sys.argv = argv

    def test_knowledge_note_states_the_platform_differences(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in ("no GI channel", "952 x 2162", "vpmMapLights", "Left/Right relay", "32 X 64"):
            self.assertIn(phrase, text, phrase)


def _evidence_root() -> Path | None:
    """The retained VPX sources root, or None when it is not available."""
    import os

    override = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if override:
        base = Path(override) / "data-east" / "lethal-weapon-3-1992"
        return base if base.is_dir() else None
    for parent in ROOT.resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
        if candidate.is_dir():
            base = candidate / "data-east" / "lethal-weapon-3-1992"
            return base if base.is_dir() else None
    return None


def _manuals_root() -> Path | None:
    """The retained manuals root, or None when it is not available."""
    import os

    override = os.environ.get("PINMAME_MANUALS_ROOT")
    if override:
        candidate = Path(override)
        return candidate if candidate.is_dir() else None
    for parent in ROOT.resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "manuals"
        if candidate.is_dir():
            return candidate
    return None


class LethalWeapon3RetainedEvidenceTests(unittest.TestCase):
    """Prove the recorded hashes describe the artifacts actually retained.

    These skip cleanly when the external evidence root is absent, so the no-evidence run stays
    green without weakening the canonical checks. A recorded digest that nothing recomputes is
    a digest nobody has ever checked.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.sources = {s["id"]: s for s in cls.definition["sources"]}
        cls.base = _evidence_root()
        cls.manuals = _manuals_root()

    @staticmethod
    def _sha256(path: Path) -> str:
        import hashlib

        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                digest.update(block)
        return digest.hexdigest()

    def test_retained_table_and_script_match_their_recorded_hashes(self) -> None:
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        for source_id, name in (
            ("vpx-table.lethal-weapon-3-vpw-2-0", "Lethal Weapon 3 (Data East 1992) VPW 2.0.vpx"),
            ("vpx-script.lethal-weapon-3-vpw-2-0", "Lethal Weapon 3 (Data East 1992) VPW 2.0.vbs"),
        ):
            path = self.base / name
            self.assertTrue(path.is_file(), str(path))
            self.assertEqual(self.sources[source_id]["sha256"], self._sha256(path), source_id)

    def test_retained_manual_and_addendum_match_their_recorded_hashes(self) -> None:
        if self.manuals is None:
            self.skipTest("retained manuals are not available")
        base = (self.manuals / "by-machine" / "data-east.lethal-weapon-3.1992"
                / "contributor-supplied")
        for source_id, name in (
            ("manual.data-east.lethal-weapon-3.1992", "Lethal_Weapon_3_OPS.pdf"),
            ("manual-addendum.data-east.lethal-weapon-3.1992", "LW3Addendum.pdf"),
        ):
            path = base / name
            self.assertTrue(path.is_file(), str(path))
            self.assertEqual(self.sources[source_id]["sha256"], self._sha256(path), source_id)

    def test_pinned_script_address_set_still_matches_the_retained_script(self) -> None:
        """SCRIPT_ASSERTED_SWITCHES must keep describing the actual retained script.

        The prose guard runs from that pinned literal so it works in CI, where no evidence root
        exists. A pinned literal nobody rechecks is exactly the kind of stale fact this whole
        contribution keeps tripping over, so recheck it whenever the evidence is present.
        """
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        script = self.base / "Lethal Weapon 3 (Data East 1992) VPW 2.0.vbs"
        self.assertTrue(script.is_file(), str(script))
        self.assertEqual(
            SCRIPT_ASSERTED_SWITCHES,
            switch_addresses_the_script_asserts(
                script.read_text(encoding="utf-8-sig", errors="replace")),
            "the retained script's switch assertions have drifted from the pinned set")

    def test_extraction_manifest_recomputes_over_every_retained_file(self) -> None:
        """Not just the manifest's own hash: every entry is re-hashed against the extraction."""
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        import hashlib
        import json as _json

        manifest_path = self.base / "extraction-manifest.json"
        self.assertTrue(manifest_path.is_file(), str(manifest_path))
        self.assertEqual(self.sources["vpx-extraction.lethal-weapon-3-vpw-2-0"]["sha256"],
                         self._sha256(manifest_path))
        recorded = _json.loads(manifest_path.read_text(encoding="utf-8"))
        body = {k: v for k, v in recorded.items() if k != "manifest_sha256"}
        canonical = _json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual(recorded["manifest_sha256"], hashlib.sha256(canonical).hexdigest())

        extraction = self.base / "vpxtool-extract"
        present = sorted(p.relative_to(extraction).as_posix() for p in extraction.rglob("*") if p.is_file())
        self.assertEqual(sorted(e["path"] for e in recorded["files"]), present,
                         "the manifest and the retained extraction disagree about which files exist")
        for entry in recorded["files"]:
            path = extraction / entry["path"]
            self.assertEqual(entry["bytes"], path.stat().st_size, entry["path"])
            self.assertEqual(entry["sha256"], self._sha256(path), entry["path"])

    def test_retained_hit_target_positions_match_the_spatial_definition(self) -> None:
        """The first resolver skipped HitTarget objects; verify the repaired centers at source."""
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.base / "vpxtool-extract" / "gameitems"
        definition = {item["binding"]["device"]: item for item in self.definition["inputs"]
                      if item["kind"] == "switch"}
        for address in (17, 18, 19, 20, 39):
            path = extraction / f"HitTarget.sw{address}.json"
            self.assertTrue(path.is_file(), str(path))
            item = json.loads(path.read_text(encoding="utf-8"))["HitTarget"]
            position = item["position"]
            placement = definition[address]["spatial"]["placements"][0]
            self.assertEqual(round(position["x"] / 952.0, 6), placement["x"], address)
            self.assertEqual(round(position["y"] / 2162.0, 6), placement["y"], address)

    def test_retained_ball_path_and_orbit_switch_positions_match_the_definition(self) -> None:
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.base / "vpxtool-extract" / "gameitems"
        definition = {item["binding"]["device"]: item for item in self.definition["inputs"]
                      if item["kind"] == "switch"}
        object_types = {10: "Kicker", 11: "Kicker", 12: "Kicker", 13: "Kicker", 54: "Trigger", 55: "Trigger"}
        for address, object_type in object_types.items():
            name = f"sw{address}" if address < 54 else f"Sw{address}"
            path = extraction / f"{object_type}.{name}.json"
            self.assertTrue(path.is_file(), str(path))
            item = json.loads(path.read_text(encoding="utf-8"))[object_type]
            center = item["center"]
            placement = definition[address]["spatial"]["placements"][0]
            self.assertEqual(round(center["x"] / 952.0, 6), placement["x"], address)
            self.assertEqual(round(center["y"] / 2162.0, 6), placement["y"], address)

    def test_retained_flasher_and_gi_light_centers_match_the_definition(self) -> None:
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        script = (self.base / "Lethal Weapon 3 (Data East 1992) VPW 2.0.vbs").read_text(encoding="utf-8-sig", errors="replace")
        extraction = self.base / "vpxtool-extract" / "gameitems"
        definition = bindings(self.definition, "outputs", "pinmame.output.solenoid")
        callbacks = {
            int(address): callback
            for address, callback in re.findall(r'(?im)^\s*SolModCallback\((\d+)\)\s*=\s*"([^"]+)"', script)
        }
        collections = load_json(self.base / "vpxtool-extract" / "collections.json")
        gi_names = next(item["items"] for item in collections if item["name"] == "GI")
        for address in (9, 11, 16, 25, 26, 27, 28, 29, 30, 31, 32):
            callback = callbacks[address]
            if address == 11:
                body = re.search(rf'(?ims)^\s*Sub\s+{re.escape(callback)}\s*\([^)]*\)(.*?)^\s*End\s+Sub', script).group(1)
                self.assertRegex(body, r'(?i)For\s+each\s+bulb\s+in\s+GI')
                object_names = gi_names
            else:
                body = re.search(rf'(?ims)^\s*Sub\s+{re.escape(callback)}\s*\([^)]*\)(.*?)^\s*End\s+Sub', script).group(1)
                object_names = re.findall(r'(?im)^\s*(F\d+[A-Za-z]*)\.state\s*=\s*level\b', body)
            observed = []
            for object_name in object_names:
                path = extraction / f"Light.{object_name}.json"
                self.assertTrue(path.is_file(), str(path))
                center = json.loads(path.read_text(encoding="utf-8"))["Light"]["center"]
                if 0.0 <= center["x"] <= 952.0 and 0.0 <= center["y"] <= 2162.0:
                    observed.append((round(center["x"] / 952.0, 6), round(center["y"] / 2162.0, 6)))
            recorded = [(item["x"], item["y"]) for item in definition[address]["spatial"]["placements"]]
            self.assertEqual(sorted(observed), sorted(recorded), address)

    def test_retained_actuator_objects_independently_reproduce_coil_locations(self) -> None:
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.base / "vpxtool-extract" / "gameitems"
        objects = {
            1: ("Kicker.sw10.json", "Kicker", "center"),
            2: ("Kicker.sw13.json", "Kicker", "center"),
            4: ("Kicker.Sw40.json", "Kicker", "center"),
            5: ("Kicker.Sw32.json", "Kicker", "center"),
            6: ("Primitive.BM_sw26.json", "Primitive", "position"),
            7: ("Primitive.BM_sw34.json", "Primitive", "position"),
            12: ("Trigger.swPlunger.json", "Trigger", "center"),
            15: ("Kicker.sw31.json", "Kicker", "center"),
            17: ("Bumper.Bumper1.json", "Bumper", "center"),
            18: ("Bumper.Bumper2.json", "Bumper", "center"),
            19: ("Bumper.Bumper3.json", "Bumper", "center"),
            22: ("Plunger.kickback.json", "Plunger", "center"),
        }
        observed = {}
        for address, (filename, section, point_name) in objects.items():
            payload = json.loads((extraction / filename).read_text(encoding="utf-8"))[section]
            point = payload[point_name]
            observed[address] = (round(point["x"] / 952.0, 6), round(point["y"] / 2162.0, 6))
        for address, filename in ((20, "Wall.LeftSlingShot.json"), (21, "Wall.RightSlingShot.json")):
            wall = json.loads((extraction / filename).read_text(encoding="utf-8"))["Wall"]
            points = wall["drag_points"]
            observed[address] = (
                round(sum(point["x"] for point in points) / len(points) / 952.0, 6),
                round(sum(point["y"] for point in points) / len(points) / 2162.0, 6),
            )
        definition = bindings(self.definition, "outputs", "pinmame.output.solenoid")
        for address, expected in observed.items():
            placements = definition[address]["spatial"]["placements"]
            self.assertEqual(1, len(placements), address)
            self.assertEqual(expected, (placements[0]["x"], placements[0]["y"]), address)
        self.assertNotIn("spatial", definition[3], "drive 3 fitment conflicts within the manual")
        self.assertNotIn("spatial", definition[8], "the drawing has no readable 8L callout and the script only supplies a sound helper")

    def test_retained_alllamps_collection_independently_reproduces_lamp_addresses(self) -> None:
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.base / "vpxtool-extract" / "gameitems"
        collections = load_json(self.base / "vpxtool-extract" / "collections.json")
        names = next(item["items"] for item in collections if item["name"] == "AllLamps")
        observed = {address: [] for address in range(1, 65)}
        for object_name in names:
            path = extraction / f"Light.{object_name}.json"
            self.assertTrue(path.is_file(), str(path))
            light = json.loads(path.read_text(encoding="utf-8"))["Light"]
            address = light["timer_interval"]
            self.assertIn(address, observed, object_name)
            center = light["center"]
            if 0.0 <= center["x"] <= 952.0 and 0.0 <= center["y"] <= 2162.0:
                observed[address].append((round(center["x"] / 952.0, 6), round(center["y"] / 2162.0, 6)))
        definition = bindings(self.definition, "outputs", "pinmame.output.lamp")
        for address in range(1, 65):
            recorded = [(item["x"], item["y"]) for item in definition[address].get("spatial", {}).get("placements", [])]
            self.assertEqual(sorted(observed[address]), sorted(recorded), address)


if __name__ == "__main__":
    unittest.main()
