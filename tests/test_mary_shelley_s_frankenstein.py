"""Regression gates for Mary Shelley's Frankenstein's physical machine, public paths and retained evidence.

The fixtures below protect independently read facts rather than copying the curator's arrays.
External gates recompute manifests, raw observations, frame readings and geometry when evidence
roots are supplied, and refuse mutated runs.
"""
from __future__ import annotations

import copy
import hashlib
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_mary_shelley_s_frankenstein as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json

KEY = "sega.mary-shelley-s-frankenstein.1995"
RUNTIME = ROOT / "evidence/runtime/data-east/mary-shelley-s-frankenstein-frankst-service-tests.json"


def devices(definition, field, group):
    return {d["binding"]["device"]: d for d in definition[field] if d["binding"]["group"] == group}


class FrankensteinDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(curator.DEFINITION_PATH)
        cls.switches = devices(cls.definition, "inputs", "pinmame.input.switch")
        cls.coils = devices(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = devices(cls.definition, "outputs", "pinmame.output.lamp")
        cls.readings = load_json(curator.READINGS_PATH)
        cls.runtime = load_json(RUNTIME)["runtime"]

    def test_identity_variants_and_controller_are_data_east_3b(self):
        machine = self.definition["machine"]
        self.assertEqual((KEY, 947, "36", "GRB7E-MP3rR", 1995),
                         (machine["id"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"], machine["year"]))
        drivers = {d["id"]: d for d in self.definition["drivers"]}
        self.assertEqual({"frankst", "frankstg", "franksti"}, set(drivers))
        self.assertEqual({"frankstg", "franksti"}, {n for n, d in drivers.items() if d.get("clone_of") == "frankst"})
        self.assertEqual(("1994", "1995", "1995"), tuple(drivers[n]["year"] for n in ("frankst", "frankstg", "franksti")))
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in drivers.values()))
        self.assertIn("franka.103", drivers["frankst"]["variant_notes"])
        self.assertEqual("pinmame.dataeast", self.definition["controller"]["platform"])
        self.assertEqual("0x8000", self.definition["controller"]["hardware_generation"])
        self.assertEqual([(192, 64)], [(d["width"], d["height"]) for d in self.definition["displays"]])
        self.assertEqual((952, 2080), (machine["playfield"]["width"], machine["playfield"]["height"]))

    def test_entire_public_inventory_and_availability(self):
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)}, set(self.switches))
        self.assertEqual(set(range(1, 65)), set(self.coils))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual({30, 49, 50, 51, 52, 57, 58, 59, 60, 61},
                         {n for n in range(1, 65) if self.switches[n]["availability"] == "unused"})
        self.assertEqual(set(range(39, 44)), {n for n, d in self.coils.items() if d["availability"] == "unknown"})
        self.assertEqual({24, 32, *range(33, 37), *range(49, 65)}, {n for n, d in self.coils.items() if d["availability"] == "unused"})
        self.assertEqual({*range(1, 24), *range(25, 32), 37, 38, 44, *range(45, 49)}, {n for n, d in self.coils.items() if d["availability"] == "used"})
        self.assertEqual({*range(49, 55), *range(57, 63)}, {n for n, d in self.lamps.items() if d["availability"] == "unused"})

    def test_unfitted_8r_explains_its_diagnostic_state(self):
        notes = self.coils[32]["physical"]["notes"]
        self.assertEqual("virtual", self.coils[32]["kind"])
        for text in ("Not Used in this Game.", "(4) NOT USED", "#8R FLASH:NOT USED", "No gameplay or attract run published it"):
            self.assertIn(text, notes)
        self.assertIn(curator.RUNTIME, self.coils[32]["provenance"]["source_refs"])
        rom = {r["address"]: r for r in self.readings["readings"] if r["group"] == "solenoid"}
        self.assertEqual(("#8R", "FLASH:NOT USED"), (rom[32]["number"], rom[32]["name"]))

    def test_physical_contacts_rest_open_and_the_service_buttons_follow_des11(self):
        for n in range(1, 65):
            if self.switches[n]["availability"] == "used":
                self.assertIs(False, self.switches[n]["normally_closed"], n)
        for n in (-7, -6, 82, 84):
            self.assertIs(False, self.switches[n]["normally_closed"])
        self.assertTrue(self.switches[-7]["pulse"])
        self.assertFalse(self.switches[-6]["pulse"])
        self.assertIn("COREPORT_BITTOG", self.switches[-6]["physical"]["notes"])
        self.assertEqual({"tilt"}, {self.switches[n]["physical"]["switch_type"] for n in (1, 7)})
        self.assertEqual("button", self.switches[3]["physical"]["switch_type"])
        screens = {(r["run"], r["label"]): r["name"] for r in self.readings["readings"] if r["group"] == "screen"}
        self.assertEqual("SINGLE LAMP TEST NONE", screens[("lamp-test", "lamp-step-1")])
        for n in (81, 83, 85, 86, 87, 88):
            self.assertEqual(f"ACTIVE SWITCH TEST NONE ({n})", screens[("switch-test", f"switch-{n}-closed")])

    def test_rom_service_names_cover_every_address(self):
        groups = {}
        for reading in self.readings["readings"]:
            groups.setdefault(reading["group"], set()).add(reading.get("address"))
            self.assertRegex(reading["pixel_sha256"], "^[0-9a-f]{64}$")
        self.assertEqual(set(range(1, 63)) | {82, 84}, groups["switch"])
        self.assertEqual(set(range(1, 65)), groups["lamp"])
        self.assertEqual({*range(1, 10), *range(11, 23), *range(25, 33)}, groups["solenoid"])
        rom = {r["address"]: r for r in self.readings["readings"] if r["group"] == "switch"}
        self.assertEqual(("RIGHT END OF STROKE", "#64"), (rom[82]["name"], rom[82]["number"]))
        self.assertEqual(("LEFT END OF STROKE", "#63"), (rom[84]["name"], rom[84]["number"]))
        self.assertEqual("6-BALL TROUGH #7 (VUK)", rom[15]["name"])
        self.assertEqual("AUTOLAUNCH LEVER", rom[62]["name"])
        self.assertEqual("NOT USED", rom[30]["name"])
        for n in range(1, 63):
            self.assertEqual(f"#{n:02d}", rom[n]["number"])
        self.assertEqual(171, len(self.runtime["observations"]["diagnostic_snapshots"]))
        self.assertIn("ACTIVE SWITCH TEST NONE (direct write to 63)",
                      {r["name"] for r in self.readings["readings"] if r["group"] == "screen"})

    def test_literal_driver_cells_and_wiring_follow_the_tables(self):
        keys = ("driver_transistor", "board", "control_wire", "control_connection", "power_wire", "power_connection")
        self.assertEqual(("Q44/Q5", "CPU/PPB", "VIO-ORN", "PPB J 8-2", "YEL/VIO", "PPB J 7-8"), tuple(self.coils[3]["wiring"][k] for k in keys))
        self.assertEqual(("Q46", "CPU", "VIO-BRN", "PPB J 2-1", "BRN", "PPB J 6-1, 2"), tuple(self.coils[1]["wiring"][k] for k in keys))
        # Merged transistor and board cells reach the flasher row from the coil row above.
        self.assertEqual(("Q46", "CPU", "BLK-BRN", "PPB J 9-1", "ORN", "PPB J 6-4, 5"), tuple(self.coils[25]["wiring"][k] for k in keys))
        self.assertEqual(("Q41", "PPB"), (self.coils[6]["wiring"]["driver_transistor"], self.coils[6]["wiring"]["board"]))
        self.assertEqual(("Q41", "CPU"), (self.coils[30]["wiring"]["driver_transistor"], self.coils[30]["wiring"]["board"]))
        self.assertEqual(("Q26", "CPU", "BRN-GRN", "CPU CN 12-6", "RED", "PS CN 3-6,7"), tuple(self.coils[13]["wiring"][k] for k in keys))
        self.assertIn("Monster Arms 50v", self.coils[13]["physical"]["notes"])
        self.assertEqual(("RED", "BRN-BLU"), (self.coils[14]["wiring"]["power_wire"], self.coils[14]["wiring"]["control_wire"]))
        self.assertIn("BRN-BLU VIO-YEL", self.coils[14]["physical"]["notes"])
        self.assertEqual("BLU-BLK", self.coils[22]["wiring"]["control_wire"])
        # The coil diagram and the ROM put flasher 15 on the 1R-7R flasher bus; the driver table alone prints RED.
        self.assertEqual(("Q24", "BRN-VIO", "CPU CN 12-8", "ORN", "PPB J 6-4, 5"),
                         tuple(self.coils[15]["wiring"][k] for k in ("driver_transistor", "control_wire", "control_connection", "power_wire", "power_connection")))
        for text in ("prints power RED from PS CN 3-6,7", "ORG 15", "with the wires ORG BRN-VIO"):
            self.assertIn(text, self.coils[15]["physical"]["notes"])
        self.assertEqual("PPB J8-12", self.coils[16]["wiring"]["control_connection"])
        self.assertIn("J8 pin 10", self.coils[16]["physical"]["notes"])
        self.assertEqual(("Q55", "GRN-BRN", "CN8-1", "WHT-BRN", "CN10-9"),
                         tuple(self.switches[1]["wiring"][k] for k in ("driver_transistor", "drive_wire", "drive_connection", "return_wire", "return_connection")))
        self.assertEqual(("Q53", "GRN-ORN", "WHT-ORN"), tuple(self.switches[19]["wiring"][k] for k in ("driver_transistor", "drive_wire", "return_wire")))
        self.assertEqual(("Q79", "RED-GRY", "CN6-9"), tuple(self.lamps[64]["wiring"][k] for k in ("return_component", "return_wire", "return_connection")))
        self.assertEqual(("Q67", "CN7-6"), (self.lamps[33]["wiring"]["driver_transistor"], self.lamps[33]["wiring"]["drive_connection"]))

    def test_part_numbers_skip_disputed_coils_and_flashers_carry_four_89s(self):
        for n in (6, 7, 20):
            self.assertNotIn("part_number", self.coils[n]["physical"])
            self.assertIn("no coil part number is asserted", self.coils[n]["physical"]["notes"])
        self.assertIn("26-1200", self.coils[6]["physical"]["notes"])
        self.assertIn("24-1240", self.coils[7]["physical"]["notes"])
        self.assertEqual({1: "25-1240", 2: "23-800", 3: "24-940", 9: "28-1050", 12: "28-1050", 14: "27-1400", 17: "23-700", 22: "23-800"},
                         {n: self.coils[n]["physical"]["part_number"] for n in (1, 2, 3, 9, 12, 14, 17, 22)})
        for n in (15, *range(25, 32)):
            self.assertEqual(("flasher", 4), (self.coils[n]["kind"], self.coils[n]["physical"]["quantity"]))
            self.assertEqual("Bulb #89; Bulb #906" if n == 30 else "Bulb #89", self.coils[n]["physical"]["part_number"])
        self.assertIn("one No. 906", self.coils[30]["physical"]["notes"])
        self.assertNotIn("906", self.coils[25]["physical"]["notes"])
        self.assertIn("27-1500", self.coils[15]["physical"]["notes"])
        self.assertEqual(("relay", "gi"), (self.coils[10]["kind"], self.coils[11]["kind"]))
        self.assertNotIn("part_number", self.lamps[1]["physical"])

    def test_cabinet_buttons_drive_the_copy_and_synthetic_pairs(self):
        self.assertEqual(["flipper.lower.left.button"], self.switches[84]["roles"])
        self.assertEqual(["flipper.lower.right.button"], self.switches[82]["roles"])
        self.assertEqual(["flipper.lower.left.matrix-copy"], self.switches[63]["roles"])
        self.assertIn("upper right flipper", self.switches[82]["physical"]["notes"])
        self.assertIn("commented out", self.switches[63]["physical"]["notes"])
        for n in (45, 46, 47, 48):
            self.assertEqual(("virtual", "used"), (self.coils[n]["kind"], self.coils[n]["availability"]))
        copies = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "direct"}
        self.assertEqual({(self.switches[82]["id"], self.switches[64]["id"]), (self.switches[84]["id"], self.switches[63]["id"])}, copies)
        observations = self.runtime["observations"]["runs"]["gameplay"]["named_action_observations"]
        self.assertEqual({(45, 46), (47, 48)}, {tuple(o["held_synthetic_solenoid_addresses"]) for o in observations if "held_synthetic_solenoid_addresses" in o})

    def test_printer_lines_are_used_only_where_the_rom_drives_them(self):
        for n in range(37, 45):
            coil = self.coils[n]
            driven = n in (37, 38, 44)
            self.assertEqual(("virtual", "used" if driven else "unknown", "observed"),
                             (coil["kind"], coil["availability"], coil["provenance"]["status"]), n)
            self.assertIn("printer is an option", coil["physical"]["notes"])
            self.assertEqual("virtual", coil["spatial"]["reason"])
            if not driven:
                self.assertIn("non-observation is not proof of non-use", coil["physical"]["notes"])
        self.assertIn("CN3 pin 9", self.coils[37]["physical"]["notes"])
        self.assertIn("elides bits 3-6", self.coils[40]["physical"]["notes"])
        for n in (37, 38, 44):
            self.assertIn("SERVO TEST", self.coils[n]["physical"]["notes"])
        for n in (37, 38, 44):
            self.assertIn("not settled", self.coils[n]["physical"]["notes"])
        for run in self.runtime["observations"]["runs"].values():
            self.assertTrue({37, 38, 44} <= set(run["solenoid_addresses_seen"]))
        self.assertFalse(set(range(39, 44)) & set(self.runtime["observations"]["solenoid_addresses_seen"]))

    def test_mechanisms_own_the_right_devices(self):
        mech = {m["id"]: m for m in self.definition["mechanisms"]}
        ids = {n: d["id"] for n, d in self.switches.items()}
        sol = {n: d["id"] for n, d in self.coils.items()}
        self.assertEqual(([sol[1], sol[2]], [ids[n] for n in range(9, 16)]), (mech["mech.trough"]["actuators"], mech["mech.trough"]["sensors"]))
        self.assertEqual(([sol[3]], [ids[16], ids[62]]), (mech["mech.autolaunch"]["actuators"], mech["mech.autolaunch"]["sensors"]))
        self.assertEqual(([sol[n] for n in (7, 9, 12, 13)], [ids[n] for n in (53, 45, 46)]),
                         (mech["mech.north-pole"]["actuators"], mech["mech.north-pole"]["sensors"]))
        self.assertIn("Adjustment 51", mech["mech.north-pole"]["behavior"])
        self.assertEqual(([sol[14]], "diverter"), (mech["mech.diverter"]["actuators"], mech["mech.diverter"]["kind"]))
        self.assertEqual(([sol[16]], [ids[37]]), (mech["mech.laser-kick"]["actuators"], mech["mech.laser-kick"]["sensors"]))
        self.assertEqual(([sol[4]], [ids[32]]), (mech["mech.lower-scoop"]["actuators"], mech["mech.lower-scoop"]["sensors"]))
        self.assertEqual(([sol[5]], [ids[31]]), (mech["mech.upper-scoop"]["actuators"], mech["mech.upper-scoop"]["sensors"]))
        # The head servo board's link to the CPU lines PinMAME publishes is not drawn, so it names no actuator.
        head = mech["mech.creature-head"]
        self.assertEqual(("motorized", [], []), (head["kind"], head["actuators"], head["sensors"]))
        for text in ("520-5113-00", "only #1 is used", "125 BPS", "pre-recorded routine", "AnimateFranksHead", "not documented"):
            self.assertIn(text, head["behavior"])
        self.assertEqual("observed", self.definition["coverage"]["dimensions"]["mechanisms"])
        pulses = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "pulse"}
        self.assertEqual({(ids[s], sol[o]) for s, o in ((41, 17), (42, 18), (43, 19), (44, 20), (47, 21), (48, 22))}, pulses)
        gated = {r["destination"] for r in self.definition["relationships"] if r["kind"] == "relay_gated"}
        self.assertEqual({sol[n] for n in range(25, 33)}, gated)

    def test_gameplay_checkpoints_name_each_stimulus(self):
        observations = {o["label"]: o for o in self.runtime["observations"]["runs"]["gameplay"]["named_action_observations"]}
        expected = {"trough-upkick": (15, 2), "lever-autolaunch": (62, 3), "upper-scoop-kick": (31, 5), "lower-scoop-kick": (32, 4),
                    "north-pole-vuk-kick": (53, 7), "ice-cave-eject-kick": (55, 6), "laser-kick": (37, 16), "spinner-diverter": (54, 14),
                    "output-17": (41, 17), "output-20": (44, 20), "output-21": (47, 21), "output-22": (48, 22)}
        for label, (switch, output) in expected.items():
            self.assertEqual((switch, [output]), (observations[label]["input_address"], observations[label]["transitioned_solenoid_addresses"]), label)
        self.assertEqual([14, 15], observations["trough-upkick"]["host_stimulus_switch_addresses"])
        gameplay = self.runtime["observations"]["runs"]["gameplay"]
        self.assertFalse({9, 12, 13} & set(gameplay["solenoid_addresses_seen"]))
        # Only the empty-trough service runs pulse the arms coil at power-up.
        runs = self.runtime["observations"]["runs"]
        self.assertEqual({"switch-test", "lamp-test", "coil-test", "cycling", "servo-laser-kick", "gameplay"}, set(runs))
        for name, run in runs.items():
            self.assertEqual(name != "gameplay", 13 in run["solenoid_addresses_seen"], name)
        self.assertIn("the gameplay run, booted with six balls in the trough, did not", self.coils[13]["physical"]["notes"])
        coil_test = {o["label"]: o["transitioned_solenoid_addresses"] for o in self.runtime["observations"]["runs"]["coil-test"]["named_action_observations"]}
        self.assertEqual(([25], [32], [9], [11], [13]), tuple(coil_test[f"entry-{n}-fired"] for n in (2, 16, 17, 18, 20)))
        kick = {o["label"]: o["transitioned_solenoid_addresses"] for o in self.runtime["observations"]["runs"]["servo-laser-kick"]["named_action_observations"]}
        self.assertEqual({"north-pole-vuk-53-closed": [7], "ice-cave-eject-55-closed": [6], "upper-scoop-31-closed": [5],
                          "lower-scoop-32-closed": [4], "shooter-lane-16-closed": [3]}, kick)

    def test_placements_are_observed_with_explicit_omissions(self):
        report = load_json(curator.SPATIAL_REPORT_PATH)
        for n in range(9, 15):
            self.assertNotIn("spatial", self.switches[n])
            self.assertIn(self.switches[n]["id"], report["omitted_spatial_key_devices"])
        for n in (31, 32):
            self.assertNotIn("spatial", self.lamps[n])
            self.assertIn(self.lamps[n]["id"], report["omitted_spatial_key_devices"])
        statuses = {}
        for group in (self.switches, self.coils, self.lamps):
            for item in group.values():
                for placement in item.get("spatial", {}).get("placements", []):
                    statuses[placement["provenance"]["status"]] = statuses.get(placement["provenance"]["status"], 0) + 1
                    self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)
        self.assertEqual({"observed": 146}, statuses)
        self.assertEqual(146, report["placement_count"])
        self.assertEqual(22, len(self.coils[11]["spatial"]["placements"]))
        self.assertEqual(2, len(self.coils[13]["spatial"]["placements"]))
        # Output 9 opens the trap door on the player's right; 12 the one on the left.
        self.assertGreater(self.coils[9]["spatial"]["placements"][0]["x"], 0.5)
        self.assertLess(self.coils[12]["spatial"]["placements"][0]["x"], 0.5)
        self.assertIn("player's right", self.coils[9]["physical"]["notes"])
        placement = self.lamps[40]["spatial"]["placements"][0]
        self.assertNotIn(curator.SCRIPT, placement["provenance"]["source_refs"])
        self.assertNotIn(curator.SCRIPT, self.lamps[40]["provenance"]["source_refs"])
        self.assertIn("TimerInterval 39", self.lamps[40]["physical"]["notes"])
        self.assertEqual(1, len(self.lamps[39]["spatial"]["placements"]))
        for n in (8, 10):
            self.assertEqual("cabinet_or_service", self.coils[n]["spatial"]["reason"])
        self.assertEqual({"solenoid.9", "solenoid.12", "solenoid.13", "solenoid.14", "lamp.40"}, set(report["projection_notes"]))
        self.assertEqual({"single-recreation-lineage", "missing-trough-and-vuk-entrance-geometry", "gi-socket-survey", "flasher-insert-sockets"},
                         {b["id"] for b in report["blockers"]})

    def test_no_sibling_record_leak_and_precise_partial_dimensions(self):
        text = curator.DEFINITION_PATH.read_text(encoding="utf-8")
        for sibling in ("batman", "Batman", "baywatch", "Baywatch", "Batcave"):
            self.assertNotIn(sibling, text)
        self.assertEqual(["input_semantics", "output_semantics", "mechanism_behavior", "spatial_placement"], self.definition["coverage"]["missing"])
        self.assertEqual([], self.definition["conflicts"])
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertTrue(curator.DEFINITION_PATH.parent.name == "sega" and "partial" in curator.DEFINITION_PATH.parts)
        self.assertFalse(any(s["id"].startswith("vpx-script.") and len(s["id"]) == 27 for s in self.definition["sources"]))
        manual = next(s for s in self.definition["sources"] if s["id"] == curator.MANUAL)
        self.assertEqual("https://www.ipdb.org/files/947/" + curator.MANUAL_NAME, manual["uri"])
        self.assertIn("model 36, January 1995", manual["locator"])

    def test_curator_seed_and_all_generated_artifacts_are_deterministic(self):
        for path, payload in curator.artifacts():
            self.assertEqual(path.read_bytes().replace(b"\r\n", b"\n"), payload.replace(b"\r\n", b"\n"), path.name)
        self.assertEqual(canonical_bytes(self.definition), curator.SEED_PATH.read_bytes().replace(b"\r\n", b"\n"))

    def test_curator_guards_fail_on_missing_rows_and_promotion(self):
        original = curator.table

        def drop_one(filename, header):
            result = original(filename, header)
            return result[:-1] if filename == "lamps.md" and header.startswith("| Number | Column") else result

        with patch.object(curator, "table", drop_one):
            with self.assertRaisesRegex(ValueError, "incomplete"):
                curator.build()
        with self.assertRaisesRegex(ValueError, "expected one table"):
            curator.table("lamps.md", "| Number | Missing |")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / f"machines/author-ready/sega/{curator.SLUG}.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}", encoding="utf-8")
            with patch.object(sys, "argv", ["curate", "--check", "--repository-root", directory]), patch.dict(os.environ, {}, clear=False):
                for name in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"):
                    os.environ.pop(name, None)
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.main()


class FrankensteinRetainedEvidenceTests(unittest.TestCase):
    def root(self, name):
        if not os.environ.get(name):
            self.skipTest(f"{name} is not declared")
        return Path(os.environ[name])

    def test_recompute_exact_table_geometry_and_extraction(self):
        from build_frankenstein_places import build
        self.assertEqual(load_json(ROOT / "tools/frankenstein_places.json"), build(self.root("PINMAME_VPX_SOURCES_ROOT")))

    def test_retained_script_bindings_match_the_curated_routes(self):
        script = (self.root("PINMAME_VPX_SOURCES_ROOT") / "sega/mary-shelley-s-frankenstein-1995/extracted-vpxtool/script.vbs").read_text(encoding="latin-1")
        callbacks = {int(n): value for n, value in re.findall(r'(?im)^SolCallback\((\d+)\)\s*=\s*"([^"]+)"', script)}
        self.assertEqual({1: "SolLockout", 2: "SolBallRelease", 3: "SolAutoLaunch", 4: "SolLowerScoopEject", 5: "SolTopScoopEject",
                          6: "SolIceCaveEject", 7: "SolVUKEject", 9: "SolTrapLeftHand", 11: "SolGI", 12: "SolTrapRightHand",
                          13: "SolFranksArms", 14: "SolOrbitDiverter", 16: "SolKickback"},
                         {n: callbacks[n] for n in (1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 16)})
        self.assertEqual({15: "SolFlasher 0, ", **{n: f"SolFlasher {n - 24}, " for n in range(25, 32)}},
                         {n: callbacks[n] for n in (15, *range(25, 32))})
        self.assertNotIn(10, callbacks)
        self.assertNotIn(32, callbacks)
        for binding in (".InitSw 0, 14, 13, 12, 11, 10, 9, 0", "If keycode = PlungerKey Then Controller.Switch(62) = True",
                        'LoadVPM "01550000", "DE.VBS", 3.26'):
            self.assertIn(binding, script)
        self.assertRegex(script, r'Const cGameName\s*=\s*"frankst"')

    def test_pinned_driver_block_and_rom_members_match_the_initializer(self):
        from pinmame_game_defs.workspace import resolve_working_root
        working = resolve_working_root(ROOT)
        source = Path(os.environ["PINMAME_SOURCE_ROOT"]) if os.environ.get("PINMAME_SOURCE_ROOT") else working / "source-checkouts/pinmame" if working else None
        if source is None or not (source / "src/wpc/degames.c").is_file():
            self.skipTest("pinned PinMAME source is unavailable")
        text = (source / "src/wpc/degames.c").read_text(encoding="utf-8")
        self.assertIn("INITGAMES11(frankst,GEN_DEDMD64, de_192x64DMD, FLIP6364, SNDBRD_DE2S, SNDBRD_DEDMD64, S11_PRINTERLINE)", text)
        block = text[text.index("INITGAMES11(frankst,"):text.index("CORE_CLONEDEFNV(franksti")]
        for member in load_json(curator.READINGS_PATH)["rom_members"]:
            self.assertIn(member["name"], block)
        for driver in ("frankstg", "franksti"):
            self.assertIn(f"#define init_{driver} init_frankst", text)
        s11 = (source / "src/wpc/s11.c").read_text(encoding="utf-8")
        self.assertIn('strncasecmp(gn, "frankst", 7)', s11)

    def test_manual_pins_fail_when_declared_root_is_wrong(self):
        self.root("PINMAME_MANUALS_ROOT")
        curator.verify_external()
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": directory}):
                with self.assertRaisesRegex(ValueError, "manual missing or changed"):
                    curator.verify_external()

    def test_raw_runtime_manifest_frame_readings_and_checkpoints_recompute(self):
        from build_frankenstein_runtime import build
        self.assertEqual(load_json(RUNTIME), build(self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")))

    def test_runtime_builder_refuses_changed_runs_scenarios_and_claims(self):
        import build_frankenstein_runtime as builder
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")
        original_digest = builder.digest
        with patch.object(builder, "digest", side_effect=lambda p: "0" * 64 if p.parent.name == "coil-test" and p.name == "run.json" else original_digest(p)):
            with self.assertRaisesRegex(ValueError, "raw run changed"):
                builder.build(review)
        original_read = builder.read_json
        scenario = ROOT / "tools/harness-scenarios/data-east/frankst-gameplay.json"

        def changed_scenario(path):
            data = original_read(path)
            if Path(path) == scenario:
                data = copy.deepcopy(data)
                data["notes"] = "changed"
            return data

        with patch.object(builder, "read_json", changed_scenario):
            with self.assertRaisesRegex(ValueError, "scenario changed"):
                builder.build(review)

        def mutated(change):
            def read(path):
                data = original_read(path)
                if Path(path).name == "run.json":
                    data = copy.deepcopy(data)
                    change(Path(path).parent.name, data)
                return data
            return read

        def lamp(name, run):
            if name == "lamp-test":
                next(s for s in run["snapshots"] if s["label"] == "lamp-step-40")["active_lamps"] = [41]

        def frame(name, run):
            if name == "switch-test":
                next(s for s in run["snapshots"] if s["label"] == "switch-30-closed")["displays"][0]["pixel_sha256"] = "0" * 64

        def checkpoint(name, run):
            if name == "gameplay":
                next(s for s in run["steps"] if s["label"] == "north-pole-vuk-kick")["matched_outputs"] = []

        def level(name, run):
            if name == "switch-test":
                snap = next(s for s in run["snapshots"] if s["label"] == "switch-41-closed")
                next(w for w in snap["watched_switches"] if w["number"] == 41)["state"] = 0

        def coil(name, run):
            if name == "coil-test":
                next(s for s in run["steps"] if s["label"] == "entry-17-fired")["transitions"]["solenoids"] = []

        def trap(name, run):
            if name == "gameplay":
                run["events"].append({"event": "solenoid", "number": 13, "state": 1})

        # Raw-run digests are pinned, so bypass that guard to reach each claim check.
        with patch.object(builder, "digest", side_effect=lambda p: load_json(builder.SEED)["runs"][p.parent.name]["sha256"] if p.name == "run.json" else original_digest(p)):
            for name, change, message in (("lamp", lamp, "lamp reading"), ("frame", frame, "frame changed"),
                                          ("checkpoint", checkpoint, "checkpoint did not fire"),
                                          ("level", level, "public level"), ("coil", coil, "coil reading"),
                                          ("trap", trap, "trap door or creature output")):
                with self.subTest(name=name):
                    with patch.object(builder, "read_json", mutated(change)):
                        with self.assertRaisesRegex(ValueError, message):
                            builder.build(review)


if __name__ == "__main__":
    unittest.main()
