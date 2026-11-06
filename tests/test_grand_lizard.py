"""Grand Lizard's complete address contract and honest remaining coverage gates."""
from __future__ import annotations

import copy
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine
import curate_grand_lizard as curator
import grand_lizard_data as data


class GrandLizardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(ROOT / curator.DEFINITION)
        cls.inputs = {d["binding"]["device"]: d for d in cls.definition["inputs"] if d["binding"]["group"].endswith("switch")}
        cls.solenoids = {d["binding"]["device"]: d for d in cls.definition["outputs"] if d["binding"]["group"].endswith("solenoid")}
        cls.lamps = {d["binding"]["device"]: d for d in cls.definition["outputs"] if d["binding"]["group"].endswith("lamp")}

    def test_identity_variants_and_stale_stub(self):
        machine = self.definition["machine"]
        self.assertEqual(("williams.grand-lizard.1986", "523", 1070, "G4XPZ-M7Zob", 1986),
                         (machine["id"], machine["model_number"], machine["ipdb_id"], machine["opdb_id"], machine["year"]))
        drivers = {d["id"]: d for d in self.definition["drivers"]}
        self.assertEqual({"grand_l1", "grand_l3", "grand_l4"}, set(drivers))
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in drivers.values()))
        self.assertNotIn("clone_of", drivers["grand_l4"])
        self.assertTrue(all(drivers[n]["clone_of"] == "grand_l4" for n in ("grand_l1", "grand_l3")))
        self.assertEqual("0x100", self.definition["controller"]["hardware_generation"])
        catalog = load_json(ROOT / "catalog/pinmame.json")
        self.assertEqual(set(drivers), {d["id"] for d in catalog["drivers"] if d["machine_id"] == machine["id"]})
        for path in (ROOT / "machines/stubs").rglob("*.json"):
            self.assertFalse(set(drivers) & {d["id"] for d in load_json(path)["drivers"]}, path)

    def test_source_acquisition_times_belong_to_their_retained_source(self):
        sources = {source["id"]: source for source in self.definition["sources"]}
        self.assertEqual("2026-11-06T13:36:30.970551+00:00", sources[curator.MANUAL]["acquired_at"])
        self.assertEqual("2026-11-06T13:38:01.388424+00:00", sources[curator.PRELIMINARY]["acquired_at"])
        for table in data.TABLES:
            for role in ("table", "script", "extraction"):
                self.assertEqual("2026-11-06T13:44:31.736622+00:00",
                                 sources[f"vpx-{role}.grand-lizard.{table['build']}"]["acquired_at"])

    def test_full_input_and_output_ranges(self):
        self.assertEqual({*range(-7, -3), *range(1, 65), *range(81, 89)}, set(self.inputs))
        dips = [d for d in self.definition["inputs"] if d["kind"] == "dip_switch"]
        self.assertEqual([0], [d["binding"]["device"] for d in dips])
        self.assertEqual(set(range(1, 65)), set(self.solenoids))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual({47, *range(49, 65), 81, 83, 85, 86, 87, 88},
                         {n for n, d in self.inputs.items() if d["availability"] == "unused"})
        self.assertEqual({*range(20, 23), 24, *range(25, 45), *range(49, 65)},
                         {n for n, d in self.solenoids.items() if d["availability"] == "unused"})
        self.assertEqual({51}, {n for n, d in self.lamps.items() if d["availability"] == "unused"})
        for n, d in self.inputs.items():
            if 1 <= n <= 64 and d["availability"] == "used":
                self.assertFalse(d["normally_closed"])
            if 1 <= n <= 64:
                self.assertIn({"namespace": "pinmame.switch", "value": f"{n:03}"}, d["aliases"])

    def test_playfield_tilt_is_unplaced_without_cabinet_exemption(self):
        switch = self.inputs[9]
        self.assertEqual("used", switch["availability"])
        self.assertEqual("SW-1A-117", switch["physical"]["part_number"])
        self.assertEqual("tilt", switch["physical"]["switch_type"])
        self.assertFalse(switch["normally_closed"])
        self.assertNotIn("spatial", switch)
        self.assertFalse(any(role.startswith("cabinet.") for role in switch.get("roles", [])))
        self.assertIn("spatial-placement gap", switch["physical"]["notes"])
        report = load_json(ROOT / curator.REPORT)
        self.assertIn("switch.matrix-9", {item["id"] for item in report["unplaced"]})
        self.assertEqual({"output_semantics", "spatial_placement"}, set(self.definition["coverage"]["missing"]))

    def test_flipper_zero_sentinel_and_synthetic_states(self):
        self.assertIn("no left matrix copy", self.inputs[84]["physical"]["notes"])
        self.assertIn("unfitted", self.inputs[84]["physical"]["notes"])
        self.assertIn("overwrites 48", self.inputs[48]["physical"]["notes"])
        self.assertEqual("SW-1A-150", self.inputs[48]["physical"]["part_number"])
        copies = [d for d in self.definition["relationships"] if d["source"].startswith("switch.flipper-column")]
        self.assertEqual([( "switch.flipper-column-82", "switch.matrix-48")], [(d["source"], d["destination"]) for d in copies])
        for n in (23, 45, 46, 47, 48):
            self.assertEqual(("used", "virtual", "virtual"), (self.solenoids[n]["availability"], self.solenoids[n]["kind"], self.solenoids[n]["spatial"]["reason"]))
        for n in (82, 84):
            self.assertFalse(self.inputs[n]["normally_closed"])

    def test_special_solenoids_and_physical_kinds(self):
        self.assertEqual("Right Magnet Flasher", self.solenoids[19]["label"])
        self.assertEqual("flasher", self.solenoids[19]["kind"])
        self.assertEqual("Coin-Lockout Relay", self.solenoids[16]["label"])
        self.assertEqual("404603-2", self.solenoids[16]["physical"]["part_number"])
        self.assertEqual("gi", self.solenoids[11]["kind"])
        self.assertEqual("cabinet_or_service", self.solenoids[11]["spatial"]["reason"])
        self.assertIn("playfield branches 8/9 are unswitched", self.solenoids[11]["physical"]["notes"])
        self.assertEqual({(43, 17), (44, 18)},
                         {(int(d["source"].rsplit("-", 1)[1]), int(d["destination"].split(".")[1]))
                          for d in self.definition["relationships"] if d["id"].startswith("relationship.special-")})
        self.assertEqual("relay", self.solenoids[9]["kind"])
        self.assertEqual("relay", self.solenoids[10]["kind"])

    def test_coin_lockout_windings_do_not_guess_physical_unit_quantity(self):
        lockout = self.solenoids[16]
        self.assertNotIn("quantity", lockout["physical"])
        self.assertEqual("relay", lockout["kind"])
        self.assertEqual("404603-2", lockout["physical"]["part_number"])
        self.assertEqual({"group": "pinmame.output.solenoid", "device": 16}, lockout["binding"])
        self.assertEqual(("1P12-9", "7P1-18, 7P4-4", "Q6"),
                         tuple(lockout["wiring"][k] for k in ("drive_connection", "return_connection", "driver_transistor")))
        self.assertEqual("cabinet_or_service", lockout["spatial"]["reason"])
        self.assertIn(curator.PRELIMINARY, lockout["provenance"]["source_refs"])
        self.assertIn("two parallel coil branches", lockout["physical"]["notes"])
        source = next(s for s in self.definition["sources"] if s["id"] == curator.PRELIMINARY)
        excerpt = next(e for e in source["excerpts"] if e["id"] == "coin-lockout-wiring")
        self.assertEqual("55458c8ebffa552a249f7b09dcc64ff4003dde53dae2ee0f5056313efc607274", excerpt["sha256"])
        self.assertEqual("930ca9ea36421bc74c12de4fb3e705240480ad8a6cc79f9018f0e0bac18fa1d1", excerpt["image_sha256"])
        for field, digest in (("path", "sha256"), ("image", "image_sha256")):
            self.assertEqual(excerpt[digest], curator.sha256(ROOT / excerpt[field]))
        self.assertIn("page 14, crop box 0.335,0.245,0.45,0.44", excerpt["image_derivation"])
        self.assertTrue(excerpt["reviewed"])
        blockers = load_json(ROOT / curator.REPORT)["readiness"]["blockers"]
        self.assertTrue(any("output 16 physical actuator quantity unresolved" in b for b in blockers))

    def test_physical_corrected_targets_and_magna_save_side(self):
        self.assertEqual("A Stationary Target", self.inputs[38]["label"])
        self.assertEqual("D Stationary Target", self.inputs[40]["label"])
        self.assertGreater(self.inputs[38]["spatial"]["placements"][0]["x"], self.inputs[40]["spatial"]["placements"][0]["x"])
        for left, right in ((42, 45), (43, 46), (44, 47)):
            self.assertLess(self.lamps[left]["spatial"]["placements"][0]["x"], 0.5)
            self.assertGreater(self.lamps[right]["spatial"]["placements"][0]["x"], 0.5)
            self.assertIn(curator.RUNTIME_SOURCE, self.lamps[left]["provenance"]["source_refs"])
        self.assertEqual(6, sum(d.get("spatial", {}).get("reason") == "cabinet_or_service" for d in self.lamps.values()))

    def test_displays_use_actual_eight_layouts_and_physical_groups(self):
        displays = self.definition["displays"]
        self.assertEqual(list(range(8)), [d["controller_index"] for d in displays])
        self.assertEqual([1, 9, 21, 29, 0, 8, 20, 28], [d["segment_start"] for d in displays])
        self.assertEqual([7, 7, 7, 7, 1, 1, 1, 1], [d["width"] for d in displays])
        self.assertEqual(["display.ball-match-left", "display.ball-match-right", "display.credits-left", "display.credits-right"], [d["id"] for d in displays[4:]])
        self.assertTrue(all(d["spatial"]["reason"] == "cabinet_or_service" for d in displays))

    def test_mechanism_topology_and_no_invented_coil_sensor_copies(self):
        mechs = {d["id"]: d for d in self.definition["mechanisms"]}
        self.assertEqual(["solenoid.3", "solenoid.4"], mechs["mech.four-bank"]["actuators"])
        self.assertEqual(["switch.matrix-20", "switch.matrix-21", "switch.matrix-22", "switch.matrix-23"], mechs["mech.four-bank"]["sensors"])
        self.assertEqual(["solenoid.2"], mechs["mech.three-bank"]["actuators"])
        self.assertEqual(["solenoid.5"], mechs["mech.lock"]["actuators"])
        self.assertTrue(all(d["source"].startswith("switch.") for d in self.definition["relationships"]))

    def test_honest_partial_and_provenance_fail_closed(self):
        self.assertEqual({"output_semantics", "spatial_placement"}, set(self.definition["coverage"]["missing"]))
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertEqual(2, self.solenoids[6]["physical"]["quantity"])
        for n in (7, 12, 13, 19):
            self.assertNotIn("quantity", self.solenoids[n]["physical"])
        self.assertNotIn("quantity", self.solenoids[11]["physical"])
        self.assertTrue(all("quantity" not in self.lamps[n]["physical"] for n in range(1, 7)))
        altered = copy.deepcopy(self.definition)
        altered["coverage"]["status"] = "author_ready"
        altered["coverage"]["missing"] = []
        self.assertTrue(validate_machine(altered, ROOT))
        self.assertEqual([], validate_machine(self.definition, ROOT))
        curator.verify_excerpts(ROOT)

    def test_determinism_and_author_ready_guard(self):
        curator.check(ROOT)
        expected = canonical_bytes(curator.build(ROOT))
        self.assertEqual(expected, (ROOT / curator.SEED).read_bytes())
        self.assertEqual(expected, (ROOT / curator.DEFINITION).read_bytes())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / curator.AUTHOR_READY
            target.parent.mkdir(parents=True)
            target.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.generate(root)
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.check(root)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / curator.EXCERPTS / "switch-matrix.md"
            target.parent.mkdir(parents=True)
            target.write_text("drift", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "excerpt drifted"):
                curator.verify_excerpts(root)

    @unittest.skipUnless(all(os.environ.get(n) for n in ("PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_VPX_SOURCES_ROOT")), "optional retained evidence roots are not configured")
    def test_retained_evidence(self):
        curator.verify_evidence(ROOT)


if __name__ == "__main__":
    unittest.main()
