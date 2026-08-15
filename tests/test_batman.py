"""Gates for the Data East Batman (1991) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major
address arithmetic, the two addresses PinMAME owns outright, the Left/Right relay pairing, and
the boundary between what the retained recreation measured and what it did not.
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/data-east/batman-1991.json"
SEED_PATH = ROOT / "tools/seeds/data-east/batman-1991.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/batman-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/batman-1991.md"
CATALOG_PATH = ROOT / "catalog/pinmame.json"


# An independently maintained fixture, keyed by address, transcribed from the printed Switch
# Matrix Chart on manual page 24. This is deliberately NOT read from the curator or its embedded
# transcription: a test that checks the generator against its own output only proves the generator
# is self-consistent. Every address the manual prints NOT USED is listed here explicitly, so a
# definition that quietly promoted one to `used` and gave it an invented coordinate fails.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 2: None, 3: "Credit Button", 4: "Right Coin", 5: "Center Coin",
    6: "Left Coin", 7: "Slam Tilt", 8: None,
    9: None, 10: "Outhole", 11: "Trough #1 Left", 12: "Trough #2 Center", 13: "Trough #3 Right",
    14: "Shooter Lane", 15: "Left EOS", 16: "Right EOS",
    17: "Left Top Lane", 18: "Center Top Lane", 19: "Right Top Lane", 20: None,
    21: "Left Return", 22: "Right Return", 23: "Left Outlane", 24: "Right Outlane",
    25: None, 26: None, 27: None, 28: "Ramp Entrance", 29: "Ramp Exit", 30: None, 31: None, 32: None,
    33: "Left 3 Bank Top", 34: "Left 3 Bank Middle", 35: "Left 3 Bank Bottom",
    36: "Joker Left Eye", 37: "Joker Right Eye", 38: "Joker Mouth", 39: "Left VUK", 40: None,
    41: "Right 3 Bank Top", 42: "Right 3 Bank Middle", 43: "Right 3 Bank Bottom",
    44: None, 45: None, 46: None, 47: "Left Slingshot", 48: "Right Slingshot",
    49: "Bat Bar Standup", 50: "Museum Motor Up", 51: "Museum Motor Down",
    52: "Right VUK Top", 53: "Right VUK Bottom", 54: "Left Turbo Bumper",
    55: "Center Turbo Bumper", 56: "Right Turbo Bumper",
    57: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None,
}
# The printed Special Coil Wiring Diagram, page 29: the left half of these two drives reads
# "NO COIL AT THIS LOCATION (NOT USED)" while their right halves still drive flash lamps.
MANUAL_UNFITTED_LEFT_DRIVES = {5, 7}


# The right-side bulb composition, transcribed from the printed Special Coil Wiring Diagram on
# manual page 29 and maintained here separately from the curator. PinMAME types the whole 25-32
# block uniformly as No. 89; the machine does not, and four of these eight carry No. 906 bulbs.
MANUAL_RIGHT_SIDE_BULBS = {
    1: "(4) No. 89", 2: "(3) No. 906 + No. 89", 3: "(2) No. 89 + (2) No. 906",
    4: "(2) No. 906 + (2) No. 89", 5: "(4) No. 89", 6: "(4) No. 89",
    7: "(4) No. 89", 8: "(2) No. 89 + (2) No. 906",
}

# Lamp labels for the addresses whose identity a fabricated coordinate would have to survive.
# Sampled across all eight printed columns rather than exhaustively, because the point is to be an
# independent check on the generator, not a second copy of it. A review demonstrated that an
# invented lamp.matrix-1 coordinate passed the whole suite while only switches had a fixture.
MANUAL_LAMPS = {
    1: "1 Million", 8: "Spot Fast Money", 9: "Bottom 2X", 15: "Batman's Head",
    16: "Batman's Chest", 17: "Left Toplane", 24: "Right Outlane", 25: "Backpanel Left",
    32: "3 Million", 33: "Left 3 Bank Top", 40: "Left 3 Bank Done", 41: "Right 3 Bank Top",
    48: "Right 3 Bank Done", 49: "Ramp Diverter", 54: "Cab.-Start Button",
    56: "Jackpot Lit", 57: "BATMAN (B)", 62: "BATMAN (N)", 63: "Lockball #1", 64: "Lockball #2",
}
# Backpanel lamps and the start-button lamp are outside playfield coordinate space.
MANUAL_CABINET_LAMPS = {25, 26, 27, 28, 29, 54}


def bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
    return {int(d["binding"]["device"]): d for d in definition[collection]
            if d["binding"]["group"] == group}


class BatmanDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
        cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

    def test_machine_identity(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual("data-east.batman.1991", machine["id"])
        self.assertEqual("Data East", machine["manufacturer"])
        self.assertEqual(1991, machine["year"])
        self.assertEqual(195, machine["ipdb_id"])
        self.assertNotIn("model_number", machine)
        ipdb = next(source for source in self.definition["sources"] if source["id"] == "ipdb.machine.195")
        self.assertEqual("https://www.ipdb.org/machine.cgi?id=195", ipdb["uri"])
        self.assertEqual(2, self.definition["schema_version"])

    def test_catalog_retains_the_pinned_pinmame_baseline(self) -> None:
        self.assertEqual(
            {
                "library_sha256": "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c",
                "library_version": "3.7.0",
                "pinmame_revision": "8371478a7640f1896dcdf565aed340dc5df989ba",
            },
            load_json(CATALOG_PATH)["source"],
        )

    def test_batman_forever_is_not_grouped_into_this_machine(self) -> None:
        """`batmanf` is Batman Forever, Sega 1995, GEN_DEDMD64 - a different physical machine.

        It shares a PinMAME name prefix and lives in the same game-table file, which is exactly
        why this is asserted rather than assumed.
        """
        driver_ids = {driver["id"] for driver in self.definition["drivers"]}
        self.assertEqual({"btmn_101", "btmn_103", "btmn_106", "btmn_f13", "btmn_g13"}, driver_ids)
        for driver_id in driver_ids:
            self.assertFalse(driver_id.startswith("batmanf"), driver_id)

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

    def test_synthetic_flipper_addresses_are_virtual_and_unused(self) -> None:
        """45-48 have no driver-board output behind them on this platform: real hardware fires
        the coils straight from the cabinet button. The coil itself is real and its part number
        and wiring are recorded, but the ADDRESS is synthetic."""
        for address in (45, 46, 47, 48):
            self.assertEqual("virtual", self.solenoids[address]["kind"], address)
            self.assertEqual("used", self.solenoids[address]["availability"], address)
            self.assertIn("Synthetic", self.solenoids[address]["label"], address)

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
        """PinMAME types 25-32 uniformly as No. 89; the machine does not.

        An earlier draft said the printed diagram showed No. 89 "on every one of the eight
        drives" in the same sentence that listed No. 906 bulbs for that drive - a claim its own
        committed excerpt contradicted.
        """
        for drive, bulbs in MANUAL_RIGHT_SIDE_BULBS.items():
            notes = self.solenoids[drive + 24]["physical"]["notes"]
            self.assertIn(bulbs, notes, drive)
            self.assertNotIn("every one of the eight drives", notes, drive)

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

    def test_pinmame_owns_switches_15_and_16(self) -> None:
        """The manual prints them as flipper EOS; PinMAME publishes button state there instead.

        core.c:1740-1741 writes the flipper button bits into the addresses named by
        FLIP_SWNO(15,16), and because this game declares no FLIP_SOL the EOS simulation never
        runs. A consumer that drives these addresses will be overwritten every frame, so the
        record has to say so.
        """
        for address in (15, 16):
            notes = self.switches[address]["physical"]["notes"]
            self.assertIn("must NOT drive this address", notes, address)
            self.assertIn("FLIP_SWNO(15,16)", notes, address)
            self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])

    def test_general_illumination_is_solenoid_11_and_there_is_no_gi_group(self) -> None:
        """Three sources agree: s11.c's own '// GI output' comment, the manual's printed
        'General Illumination Relay', and the retained script's own 'GI Relay callback."""
        self.assertEqual("General Illumination Relay", self.solenoids[11]["label"])
        self.assertIn("playfield.general-illumination", self.solenoids[11].get("roles", []))
        notes = self.solenoids[11]["physical"]["notes"]
        self.assertIn("asserted therefore means GI off", notes)
        self.assertIn("deasserted means GI on", notes)
        self.assertIn("does not resolve address 9", notes)
        self.assertIn("vpx-script.batman-vpw-1-1", self.solenoids[11]["provenance"]["source_refs"])
        self.assertIn("legacy.game.batman", self.solenoids[11]["provenance"]["source_refs"])
        groups = {d["binding"]["group"] for d in self.definition["outputs"]}
        self.assertNotIn("pinmame.output.gi", groups,
                         "Data East publishes no GI channel; nGI is never assigned in s11.c")

    def test_trough_positions_preserve_the_known_working_script_order(self) -> None:
        trough = next(mechanism for mechanism in self.definition["mechanisms"]
                      if mechanism["id"] == "mechanism.ball-trough")
        self.assertEqual(
            ["switch.matrix-11", "switch.matrix-12", "switch.matrix-13"],
            [position["sensors"][0] for position in trough["positions"]],
        )
        self.assertIn("InitSwitches Array(13,12,11)", trough["behavior"])

    def test_retained_manual_matches_its_pinned_digest(self) -> None:
        manuals_root = os.environ.get("PINMAME_MANUALS_ROOT")
        if not manuals_root:
            self.skipTest("manuals root is not configured")
        import curate_batman as curator

        manual = (Path(manuals_root) / "by-machine" / "data-east.batman.1991" / "archive-org"
                  / "Data_East_1991_Batman_Manual.pdf")
        self.assertTrue(manual.is_file(), manual)
        self.assertEqual(curator.TRANSCRIPTION["document_sha256"], curator._file_sha256(manual))

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
        published "28 pages" for a 70-page document, in prose the ledger then contradicted."""
        import curate_batman as curator

        self.assertEqual(70, curator.TRANSCRIPTION["document"]["page_count"])
        self.assertEqual(0, curator.TRANSCRIPTION["document"]["character_count"])
        self.assertIn("70 pages", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

    def test_evidence_excerpts_exist_and_match_their_recorded_digests(self) -> None:
        """A hash proves the local copy has not changed; it says nothing about what the document
        said. This manual is a 70-page image-only scan, so the regions actually read are committed
        beside the definition and digest-checked here."""
        import hashlib

        manual = next(s for s in self.definition["sources"] if s["id"].startswith("manual."))
        self.assertGreaterEqual(len(manual["excerpts"]), 3)
        for excerpt in manual["excerpts"]:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), excerpt["path"])
            self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])
            if "image" in excerpt:
                image = ROOT / excerpt["image"]
                self.assertTrue(image.is_file(), excerpt["image"])
                self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image.read_bytes()).hexdigest(), excerpt["id"])

    def test_retained_table_and_extraction_are_hash_pinned(self) -> None:
        """A coordinate is only reproducible if the extraction it came from is pinned."""
        by_id = {s["id"]: s for s in self.definition["sources"]}
        for source_id in ("vpx-table.batman-vpw-1-1", "vpx-script.batman-vpw-1-1",
                          "vpx-extraction.batman-vpw-1-1"):
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

    def test_unfitted_left_halves_are_declared_unused(self) -> None:
        """Printed drives 5 and 7 carry 'NO COIL AT THIS LOCATION (NOT USED)' on the left half
        while their right halves still drive flash lamps."""
        for drive in (5, 7):
            self.assertEqual("unused", self.solenoids[drive]["availability"], drive)
            self.assertEqual("used", self.solenoids[drive + 24]["availability"], drive)

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
        """btmnGameData declares custSol = 0, so CORE_FIRSTCUSTSOL (51) upward is empty."""
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
                self.assertEqual(expected, switch["label"], address)

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
            expected = "unused" if drive in MANUAL_UNFITTED_LEFT_DRIVES else "used"
            self.assertEqual(expected, self.solenoids[drive]["availability"], drive)
            self.assertEqual("used", self.solenoids[drive + 24]["availability"], drive)

    def test_every_driver_note_names_every_rom_that_differs(self) -> None:
        """The ROM-composition rule checked as data, not trusted to the builder's guard."""
        import curate_batman as curator

        root_roms = curator.ROM_SETS["btmn_103"]["roms"]
        notes = {d["id"]: d["variant_notes"] for d in self.definition["drivers"]}
        self.assertEqual(set(notes), set(curator.ROM_SETS))
        for driver_id, entry in curator.ROM_SETS.items():
            if driver_id == "btmn_103":
                continue
            for role, mine, theirs in zip(("CPU B5", "CPU C5", "display"), entry["roms"], root_roms):
                if mine != theirs:
                    self.assertIn(mine, notes[driver_id], f"{driver_id}: {role} ROM {mine}")

    def test_sound_roms_are_identical_across_the_clone_tree(self) -> None:
        import curate_batman as curator

        sound = {tuple(entry["roms"][3:]) for entry in curator.ROM_SETS.values()}
        self.assertEqual(1, len(sound), "the definition claims the sound ROMs never differ")

    def test_mechanism_topology_follows_the_known_working_script(self) -> None:
        """The script is authoritative for runtime causality, and an earlier draft ignored it.

        That draft asserted a "Museum Motor" actuated by solenoid 22 and sensed by switches 50/51.
        The retained script binds 50 and 51 as the two travel limits of a cvpmMech whose Sol1 is
        solenoid 16, and binds 22 to a callback named SolDiv commented "Ramp Diverter". No source
        supported the original topology. The banks were likewise called drop targets when nothing
        resets them and the script only nudges the target object.
        """
        by_id = {m["id"]: m for m in self.definition["mechanisms"]}

        bar = by_id["mechanism.bar-motor"]
        self.assertEqual(["coil.driver-16"], bar["actuators"])
        self.assertEqual(["switch.matrix-50", "switch.matrix-51"], sorted(bar["sensors"]))
        self.assertNotIn("switch.matrix-49", bar["sensors"], "49 is occluded by the bar, not a sensor of it")

        diverter = by_id["mechanism.ramp-diverter"]
        self.assertEqual("diverter", diverter["kind"])
        self.assertEqual(["coil.driver-22"], diverter["actuators"])
        self.assertEqual("control_signal", self.solenoids[22]["kind"])
        self.assertIn("downstream actuator", self.solenoids[22]["physical"]["notes"])

        for mechanism_id in ("mechanism.left-three-bank", "mechanism.right-three-bank"):
            self.assertNotEqual("drop_target_bank", by_id[mechanism_id]["kind"], mechanism_id)

        self.assertNotIn("mechanism.museum-motor", by_id)
        ids = {d["id"] for collection in ("inputs", "outputs") for d in self.definition[collection]}
        for mechanism in self.definition["mechanisms"]:
            for reference in mechanism["actuators"] + mechanism["sensors"]:
                self.assertIn(reference, ids, mechanism["id"])

    def test_visible_grouped_outputs_do_not_claim_a_false_spatial_disposition(self) -> None:
        """They drive visible lamps or a playfield mechanism, so internal_nonvisual is wrong.

        The retained table binds no object to them, so there is no coordinate either. The schema
        offers only located or not_applicable and neither is honest, so the key is omitted and the
        gap is carried in the blocker report instead.
        """
        for address in (9, 11, 12, 13, 14, 16, *range(25, 33)):
            flasher = self.solenoids[address]
            self.assertIn(flasher["kind"], {"flasher", "gi", "motor"}, address)
            self.assertNotIn("spatial", flasher, f"address {address} must not claim a disposition")

    def test_effect_coordinates_are_only_assigned_to_scripted_playfield_assemblies(self) -> None:
        expected = {1, 2, 3, 4, 6, 17, 18, 19, 20, 21, 22}
        located = {
            address for address, output in self.solenoids.items()
            if output.get("spatial", {}).get("status") == "observed"
        }
        self.assertEqual(expected, located)
        for address in expected:
            placement = self.solenoids[address]["spatial"]["placements"][0]
            self.assertEqual("effect", placement["role"])
            self.assertEqual("observed", placement["provenance"]["status"])

    def test_turbo_bumper_positions_follow_the_manual_identity_order(self) -> None:
        """The retained script crosses its Center/Right callbacks; the manual and lamp trio do not."""
        positions = {}
        for label, devices in (
            ("switch", self.switches), ("coil", self.solenoids), ("lamp", self.lamps)
        ):
            addresses = (54, 55, 56) if label == "switch" else ((17, 18, 19) if label == "coil" else (44, 45, 46))
            positions[label] = [devices[address]["spatial"]["placements"][0]["x"] for address in addresses]
            self.assertEqual(sorted(positions[label]), positions[label], label)
        conflict_ids = {conflict["id"] for conflict in self.definition["conflicts"]}
        self.assertIn("conflict.turbo-bumper-center-right-routing", conflict_ids)

    def test_synthetic_flipper_outputs_publish_meaningful_state_but_no_physical_device(self) -> None:
        for address in range(45, 49):
            output = self.solenoids[address]
            self.assertEqual("used", output["availability"], address)
            self.assertEqual("virtual", output["kind"], address)
            self.assertEqual("not_applicable", output["spatial"]["status"], address)
            self.assertEqual("virtual", output["spatial"]["reason"], address)

    def test_conflicts_are_declared_and_counted(self) -> None:
        ids = {c["id"] for c in self.definition["conflicts"]}
        self.assertEqual({"conflict.solenoid-9-bulb-type", "conflict.matrix-position-2-naming",
                          "conflict.motor-circuit-identity",
                          "conflict.turbo-bumper-center-right-routing"}, ids)
        self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

    def test_promotion_state_is_partial(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["input_semantics", "mechanism_behavior", "polarity",
                          "recreation_notes", "spatial_placement", "unresolved_conflicts"],
                         coverage["missing"])


class BatmanSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.report = load_json(SPATIAL_REPORT_PATH)

    def test_playfield_is_the_retained_tables_own_extent(self) -> None:
        """952 x 1974, NOT the 2162 most WPC-era tables use.

        Normalizing y by 2162 would compress every coordinate by about nine percent. This is the
        same class of trap the Indiana Jones (1093 wide) and Theatre of Magic (2594.1 tall)
        passes had to catch, so it gets a gate rather than a comment.
        """
        playfield = self.definition["machine"]["playfield"]
        self.assertEqual(952.0, playfield["width"])
        self.assertEqual(1974.0, playfield["height"])
        self.assertEqual("vpx", playfield["units"])
        self.assertNotEqual(2162, playfield["height"])

    def test_report_is_a_blocker_report_for_a_partial_machine(self) -> None:
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])
        self.assertEqual("data-east.batman.1991", self.report["machine_id"])

    def test_placement_count_matches_the_definition(self) -> None:
        placements = sum(
            len(device.get("spatial", {}).get("placements", []))
            for collection in ("inputs", "outputs")
            for device in self.definition[collection])
        self.assertEqual(placements, self.report["placement_count"])
        self.assertGreater(placements, 0)

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
            self.assertRegex(device_id, r"^(switch|lamp)[.]matrix-[0-9]+$", device_id)
            self.assertIn(device_id, ids, device_id + " is audited but absent from the definition")

    def test_every_placement_is_observed_because_only_one_table_was_retained(self) -> None:
        for collection in ("inputs", "outputs"):
            for device in self.definition[collection]:
                for placement in device.get("spatial", {}).get("placements", []):
                    self.assertEqual("observed", placement["provenance"]["status"], device["id"])

    def test_single_recreation_is_declared_a_blocker(self) -> None:
        blockers = {blocker["id"]: blocker for blocker in self.report["blockers"]}
        self.assertIn("single-retained-recreation", blockers)
        detail = blockers["single-retained-recreation"]["detail"]
        self.assertIn("page-28 Coil and Flash Lamp Locations", detail)
        self.assertIn("1A-8A and 1B-8B", detail)
        self.assertIn("neither one point nor cabinet_or_service", detail)

    def test_report_distinguishes_resolver_misses_from_real_spatial_gaps(self) -> None:
        self.assertEqual([], self.report["unresolved"]["switches"])
        lamps = self.report["unresolved"]["lamps"]
        self.assertEqual([50, 51, 52, 53], [entry["address"] for entry in lamps])
        self.assertEqual(
            [f"lamp.matrix-{address}" for address in (50, 51, 52, 53)],
            [entry["device_id"] for entry in lamps],
        )
        for entry in lamps:
            self.assertIn("physical coordinate", entry["reason"])


class BatmanCuratorTests(unittest.TestCase):
    def test_seed_is_byte_identical_to_the_definition(self) -> None:
        self.assertEqual(SEED_PATH.read_bytes(), DEFINITION_PATH.read_bytes())

    def test_curator_check_is_idempotent(self) -> None:
        import curate_batman as curator

        curator._check(ROOT)
        curator._check(ROOT)

    def test_curator_check_rejects_edited_artifacts(self) -> None:
        import shutil
        import tempfile

        import curate_batman as curator

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

        import curate_batman as curator

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
        import curate_batman as curator

        argv = sys.argv
        sys.argv = ["curate_batman.py"]
        try:
            with self.assertRaises(SystemExit):
                curator.main()
        finally:
            sys.argv = argv

    def test_knowledge_note_states_the_platform_differences(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in ("no GI channel", "952 x 1974", "batmanf", "Left/Right relay"):
            self.assertIn(phrase, text, phrase)
        conflicts = load_json(DEFINITION_PATH)["conflicts"]
        self.assertEqual(2, text.count(f"{len(conflicts)} source disagreements"))
        for conflict in conflicts:
            self.assertIn(f"`{conflict['id']}`", text, conflict["id"])


def _evidence_root() -> Path | None:
    """The retained VPX sources root, or None when it is not available."""
    import os

    override = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if override:
        base = Path(override) / "data-east" / "batman-1991"
        return base if base.is_dir() else None
    for parent in ROOT.resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
        if candidate.is_dir():
            base = candidate / "data-east" / "batman-1991"
            return base if base.is_dir() else None
    return None


class BatmanRetainedEvidenceTests(unittest.TestCase):
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
            ("vpx-table.batman-vpw-1-1", "Batman (Data East 1991) VPW v1.1.vpx"),
            ("vpx-script.batman-vpw-1-1", "Batman (Data East 1991) VPW v1.1.vbs"),
        ):
            path = self.base / name
            self.assertTrue(path.is_file(), str(path))
            self.assertEqual(self.sources[source_id]["sha256"], self._sha256(path), source_id)

    def test_extraction_manifest_recomputes_over_every_retained_file(self) -> None:
        """Not just the manifest's own hash: every entry is re-hashed against the extraction."""
        if self.base is None:
            self.skipTest("retained VPX sources are not available")
        import hashlib
        import json as _json

        manifest_path = self.base / "extraction-manifest.json"
        self.assertTrue(manifest_path.is_file(), str(manifest_path))
        self.assertEqual(self.sources["vpx-extraction.batman-vpw-1-1"]["sha256"],
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


if __name__ == "__main__":
    unittest.main()
