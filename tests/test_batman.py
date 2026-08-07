"""Gates for the Data East Batman (1991) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major
address arithmetic, the two addresses PinMAME owns outright, the Left/Right relay pairing, and
the boundary between what the retained recreation measured and what it did not.
"""
from __future__ import annotations

import json
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
        self.assertEqual(2, self.definition["schema_version"])

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
            self.assertEqual("unused", self.solenoids[address]["availability"], address)
            self.assertIn("Synthetic", self.solenoids[address]["label"], address)

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
        groups = {d["binding"]["group"] for d in self.definition["outputs"]}
        self.assertNotIn("pinmame.output.gi", groups,
                         "Data East publishes no GI channel; nGI is never assigned in s11.c")

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

    def test_no_placement_exists_for_an_address_the_manual_prints_not_used(self) -> None:
        """The check that would catch an invented binding.

        A resolver that matched objects too loosely would place a coordinate on an address that
        carries no device at all, which is worse than leaving it unplaced.
        """
        for address, switch in self.switches.items():
            if switch["availability"] != "unused":
                continue
            self.assertNotIn("placements", switch.get("spatial", {}), address)

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

    def test_conflicts_are_declared_and_counted(self) -> None:
        ids = {c["id"] for c in self.definition["conflicts"]}
        self.assertEqual({"conflict.solenoid-9-bulb-type", "conflict.matrix-position-2-naming"}, ids)
        self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

    def test_promotion_state_is_partial(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["spatial_placement", "unresolved_conflicts"], coverage["missing"])


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

    def test_every_placement_is_observed_because_only_one_table_was_retained(self) -> None:
        for collection in ("inputs", "outputs"):
            for device in self.definition[collection]:
                for placement in device.get("spatial", {}).get("placements", []):
                    self.assertEqual("observed", placement["provenance"]["status"], device["id"])

    def test_single_recreation_is_declared_a_blocker(self) -> None:
        ids = {b["id"] for b in self.report["blockers"]}
        self.assertIn("single-retained-recreation", ids)


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


if __name__ == "__main__":
    unittest.main()
