"""Production identity, physical/runtime authority and fail-closed evidence checks."""
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import load_json
from tools import curate_alien_poker as curator
from tools.alien_poker_runtime import runtime_evidence


def keyed(items, group):
    return {item["binding"]["device"]: item for item in items if item["binding"]["group"] == group}


class AlienPokerTests(unittest.TestCase):
    def test_physical_identity_and_conversion_split(self):
        production, conversion = curator.build(), curator.conversion()
        self.assertEqual(production["machine"]["ipdb_id"], 48)
        self.assertEqual(production["machine"]["opdb_id"], "G4yen-MD12Y")
        self.assertEqual(production["machine"]["model_number"], "501")
        self.assertEqual(production["controller"]["platform"], "pinmame.system-6")
        self.assertEqual({d["id"] for d in production["drivers"]},
                         {"alpok_l2", "alpok_l2ff", "alpok_l6", "alpok_l6ff", "alpok_f6", "alpok_f6ff"})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in production["drivers"]))
        self.assertEqual([d["id"] for d in conversion["drivers"]], ["alpok_b6"])
        self.assertEqual(conversion["machine"]["kind"], "physical_conversion")
        self.assertNotIn("opdb_id", conversion["machine"])
        self.assertIsNone(conversion["machine"]["year"])
        self.assertEqual(conversion["drivers"][0]["year"], "2006")
        self.assertEqual(conversion["inputs"], [])  # no production hardware is silently inherited
        catalog = load_json(curator.ROOT / "catalog/pinmame.json")
        for driver in catalog["drivers"]:
            if driver["id"] == "alpok_b6":
                self.assertEqual(driver["machine_id"], conversion["machine"]["id"])

    def test_exact_transport_ranges_and_real_dispositions(self):
        production = curator.build()
        switches = keyed(production["inputs"], "pinmame.input.switch")
        dips = keyed(production["inputs"], "pinmame.input.dip")
        coils = keyed(production["outputs"], "pinmame.output.solenoid")
        lamps = keyed(production["outputs"], "pinmame.output.lamp")
        self.assertEqual(set(switches), set(range(-7, -2)) | set(range(1, 65)) | set(range(81, 89)))
        self.assertEqual(set(dips), {1, 2} | set(range(9, 25)))
        self.assertEqual(set(coils), set(range(1, 24)) | set(range(45, 49)))
        self.assertEqual(set(lamps), set(range(1, 65)))
        self.assertTrue(all(switches[n]["availability"] == "unused" for n in range(44, 65)))
        self.assertEqual({n for n, item in dips.items() if item["availability"] == "used"}, {1, 2, 17, 18, 19})
        self.assertTrue(all(coils[n]["kind"] == "control_signal" for n in range(9, 14)))
        self.assertTrue(all(coils[n]["availability"] == "used" for n in range(45, 49)))
        self.assertEqual(coils[23]["kind"], "relay")
        self.assertEqual(lamps[49]["availability"], "unused")
        self.assertFalse(any(o["kind"] == "gi" for o in production["outputs"]))
        self.assertEqual({a["value"] for a in switches[9]["aliases"]}, {"9", "09", "009"})
        self.assertTrue(all(switches[n]["normally_closed"] is False for n in range(1, 43)))
        self.assertNotIn("normally_closed", switches[43])
        self.assertNotIn("location", switches[43]["physical"])
        self.assertEqual(switches[43]["spatial"]["reason"], "virtual")
        self.assertNotIn("normally_closed", switches[-7])  # unresolved service construction stays explicit
        self.assertEqual(switches[10]["physical"]["switch_type"], "other")
        self.assertEqual(switches[10]["physical"]["part_number"], "1B-2001-124-4")
        self.assertIn("Drive 82", switches[43]["physical"]["notes"])

    def test_factory_semantics_mechanisms_and_display_correction(self):
        production = curator.build()
        coils = keyed(production["outputs"], "pinmame.output.solenoid")
        self.assertEqual((coils[18]["label"], coils[19]["label"]), ("Right Jet Bumper", "Left Jet Bumper"))
        self.assertEqual(coils[4]["wiring"]["drive_connection"], "2P11-8, 8P3-20")
        self.assertEqual(coils[21]["physical"]["part_number"], "SA3-24-750-DC")
        bank = next(m for m in production["mechanisms"] if m["id"] == "mech.royal-flush")
        self.assertEqual(bank["actuators"], [f"solenoid.{n}" for n in [4, 5, 6, 7, 8, 21]])
        self.assertEqual(bank["sensors"], [f"switch.{n}" for n in [42, 34, 26, 18, 10]])
        self.assertIn("common release", bank["behavior"])
        self.assertNotIn("assembly_part_number", bank)  # generic D8362 is not this individual-reset bank
        displays = production["displays"]
        self.assertEqual([d["segment_start"] for d in displays], [1, 9, 21, 29, 0, 8, 20, 28])
        self.assertEqual([d["label"] for d in displays[4:]],
                         ["Ball in Play Tens", "Ball in Play Units", "Credit Tens", "Credit Units"])
        self.assertTrue(all(d["spatial"]["reason"] == "cabinet_or_service" for d in displays))
        self.assertEqual({(r["source"], r["destination"]) for r in production["relationships"]},
                         {(f"switch.{sw}", f"solenoid.{coil}") for sw, coil in [(35, 17), (37, 18), (36, 19), (38, 20), (13, 22)]})

    def test_spatial_projections_and_precise_partial_gate(self):
        production = curator.build()
        switches = keyed(production["inputs"], "pinmame.input.switch")
        lamps = keyed(production["outputs"], "pinmame.output.lamp")
        self.assertEqual(production["coverage"]["status"], "partial")
        self.assertEqual(set(production["coverage"]["missing"]), {"polarity", "spatial_placement"})
        self.assertEqual(set(curator.report()["unplaced"]), {"switch.9", "switch.31", "solenoid.1", "lamp.56"})
        self.assertEqual(curator.report()["unplaced_physical_counterparts"], ["switch.43"])
        self.assertEqual(len(lamps[18]["spatial"]["placements"]), 2)
        self.assertEqual(len(lamps[37]["spatial"]["placements"]), 2)
        self.assertEqual(lamps[37]["physical"]["quantity"], 2)
        self.assertNotIn("spatial", lamps[56])
        self.assertTrue(all(lamps[n]["spatial"]["reason"] == "cabinet_or_service" for n in [50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64]))
        self.assertTrue(all(switches[n]["spatial"]["status"] == "observed" for n in [13, 19, 21, 28, 33, 39, 40, 41]))
        for n in range(29, 33):
            self.assertEqual(len(lamps[n]["spatial"]["placements"]), 1)
            self.assertNotIn("quantity", lamps[n]["physical"])
        self.assertTrue(all(s["excerpts"][0]["reviewed"] for s in production["sources"] if s.get("excerpts")))

    def test_runtime_has_rom_responses_not_host_readback(self):
        evidence = runtime_evidence()
        observations = evidence["runtime"]["observations"]["runs"]
        responses = observations["switch"]["named_action_observations"]
        self.assertEqual([r["input_address"] for r in responses], list(range(1, 43)))
        self.assertTrue(all(not r["observed_switch_addresses"] for r in responses))
        self.assertTrue(all(r["display_responses"] for r in responses))
        self.assertEqual(observations["solenoid"]["ordered_solenoid_on_sequence"], list(range(1, 23)) + [1])
        right = next(a for a in observations["gameplay"]["named_action_observations"] if a["input_address"] == 82)
        self.assertEqual(right["observed_switch_addresses"], [43])
        self.assertIn(45, right["active_solenoid_addresses"])
        self.assertIn(46, right["active_solenoid_addresses"])
        self.assertEqual(len(evidence["runtime"]["raw_runs"]), 6)
        self.assertEqual(evidence["runtime"]["emulator"]["built_from_revision"], curator.REV)

    def test_determinism_and_byte_identical_seeds(self):
        with patch.dict(os.environ, {}, clear=True):
            curator.check()
        for artifact, seed in [(curator.PRODUCTION, curator.SEED), (curator.CONVERSION, curator.CONVERSION_SEED),
                               (curator.RUNTIME_PATH, "tools/seeds/williams/alien-poker-1980-runtime.json")]:
            self.assertEqual((curator.ROOT / artifact).read_bytes(), (curator.ROOT / seed).read_bytes())

    def test_mutation_guards_and_author_ready_protection(self):
        with tempfile.TemporaryDirectory(dir=curator.ROOT) as directory, patch.dict(os.environ, {}, clear=True):
            root = Path(directory)
            for relative in [*curator.EXCERPT_HASHES, curator.DATA_PATH]:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(curator.ROOT / relative, target)
            curator.generate(root)
            curator.check(root)
            seed = root / curator.SEED
            seed.write_bytes(seed.read_bytes() + b" ")
            with self.assertRaisesRegex(RuntimeError, "drifted artifact"):
                curator.check(root)
            curator.generate(root)
            excerpt = root / curator.EXCERPT
            excerpt.write_text("wrong physical mapping", encoding="utf8")
            with self.assertRaisesRegex(RuntimeError, "changed excerpt"):
                curator.generate(root)
            shutil.copyfile(curator.ROOT / curator.EXCERPT, excerpt)
            evidence = root / curator.DATA_PATH
            evidence.write_bytes(evidence.read_bytes() + b" ")
            with self.assertRaisesRegex(RuntimeError, "changed curation evidence seed"):
                curator.generate(root)
            shutil.copyfile(curator.ROOT / curator.DATA_PATH, evidence)
            ready = root / "machines/author-ready/williams/alien-poker-1980.json"
            ready.parent.mkdir(parents=True)
            ready.write_text("protected", encoding="utf8")
            with self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.generate(root)
            self.assertEqual(ready.read_text(encoding="utf8"), "protected")

    def test_configured_roots_fail_closed_when_missing(self):
        for variable in ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"]:
            with self.subTest(variable=variable), tempfile.TemporaryDirectory(dir=curator.ROOT) as directory:
                with patch.dict(os.environ, {variable: directory}, clear=True):
                    with self.assertRaises(RuntimeError):
                        curator.verify_inputs(curator.ROOT)

    def test_retained_evidence_when_configured(self):
        if not all(os.environ.get(v) for v in ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"]):
            self.skipTest("optional retained evidence roots not configured")
        curator.verify_inputs(curator.ROOT)
        directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "williams.alien-poker.1980/runtime"
        self.assertEqual(runtime_evidence(directory), runtime_evidence())


if __name__ == "__main__":
    unittest.main()
