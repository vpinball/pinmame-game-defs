"""Regression contract for the complete semantic Star Wars curation."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.completion import completion_score
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_star_wars_runtime as runtime_builder
import curate_star_wars as curator
import curate_star_wars_spatial as spatial
import star_wars_pinmame as pinmame
import star_wars_harness as title_reader


BASELINE = ROOT / "tools/seeds/data-east/star-wars-1992-baseline.json"
PINMAME_SEED = ROOT / "tools/star_wars_pinmame.json"
DEFINITION = ROOT / "machines/partial/data-east/star-wars-1992.json"

EXPECTED_DRIVERS = {
    "stwr_101", "stwr_102", "stwr_103", "stwr_104", "stwr_106", "stwr_107",
    "stwr_107s", "stwr_a046", "stwr_a14", "stwr_e12", "stwr_g11",
}
FACTORY_UNUSED_MATRIX = {8, 9, 18, 49, *range(52, 65)}
UNUSED_FLIPPER_COLUMN = {81, 83, 85, 86, 87, 88}
PHYSICAL_SOLENOIDS = {*range(1, 13), 15, 16, *range(17, 23), *range(25, 33)}
USED_VIRTUAL_SOLENOIDS = {23, 45, 46, 47, 48}
UNUSED_SOLENOIDS = {13, 14, 24, *range(33, 45), *range(49, 65)}


def by_binding(records: list[dict]) -> dict[tuple[str, int], dict]:
    return {(record["binding"]["group"], record["binding"]["device"]): record for record in records}


def alias_pairs(record: dict) -> set[tuple[str, str]]:
    return {(alias["namespace"], alias["value"]) for alias in record.get("aliases", [])}


class StarWarsCurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        cls.definition = curator.build()
        cls.inputs = by_binding(cls.definition["inputs"])
        cls.outputs = by_binding(cls.definition["outputs"])
        cls.mechanisms = {item["id"]: item for item in cls.definition["mechanisms"]}

    def test_complete_address_sets_and_explicit_dispositions(self):
        switch_keys = {address for (group, address) in self.inputs if group == "pinmame.input.switch"}
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)}, switch_keys)
        self.assertEqual({0}, {address for (group, address) in self.inputs if group == "pinmame.input.dip"})
        self.assertEqual(75, len(self.definition["inputs"]))

        matrix_unused = {
            address for address in range(1, 65)
            if self.inputs[("pinmame.input.switch", address)]["availability"] == "unused"
        }
        self.assertEqual(FACTORY_UNUSED_MATRIX, matrix_unused)
        self.assertEqual(
            UNUSED_FLIPPER_COLUMN,
            {address for address in range(81, 89)
             if self.inputs[("pinmame.input.switch", address)]["availability"] == "unused"},
        )
        self.assertEqual(
            {-7, -6, *(set(range(1, 65)) - FACTORY_UNUSED_MATRIX), 82, 84},
            {address for address in switch_keys
             if self.inputs[("pinmame.input.switch", address)]["availability"] == "used"},
        )
        self.assertEqual(
            "CPU Jumper J8 (PIA 11B PA7)",
            self.inputs[("pinmame.input.dip", 0)]["label"],
        )
        self.assertIn("factory installed (DIP 0 = 0)",
                      self.inputs[("pinmame.input.dip", 0)]["physical"]["notes"])
        self.assertEqual("Plumb Tilt", self.inputs[("pinmame.input.switch", 1)]["label"])
        self.assertEqual("4th Coin", self.inputs[("pinmame.input.switch", 2)]["label"])
        tilt = self.inputs[("pinmame.input.switch", 1)]
        self.assertNotIn("part_number", tilt["physical"])
        self.assertEqual("500-5023-00", tilt["physical"]["assembly_part_number"])
        for address in set(range(1, 65)) - FACTORY_UNUSED_MATRIX | {82, 84}:
            self.assertFalse(self.inputs[("pinmame.input.switch", address)]["normally_closed"], address)

        solenoids = {
            address: record for (group, address), record in self.outputs.items()
            if group == "pinmame.output.solenoid"
        }
        lamps = {
            address: record for (group, address), record in self.outputs.items()
            if group == "pinmame.output.lamp"
        }
        self.assertEqual(set(range(1, 65)), set(solenoids))
        self.assertEqual(set(range(1, 65)), set(lamps))
        self.assertEqual(128, len(self.definition["outputs"]))
        self.assertEqual(PHYSICAL_SOLENOIDS | USED_VIRTUAL_SOLENOIDS,
                         {address for address, record in solenoids.items() if record["availability"] == "used"})
        self.assertEqual(UNUSED_SOLENOIDS,
                         {address for address, record in solenoids.items() if record["availability"] == "unused"})
        self.assertEqual({17}, {address for address, record in lamps.items() if record["availability"] == "unused"})
        self.assertEqual(set(range(1, 65)) - {17},
                         {address for address, record in lamps.items() if record["availability"] == "used"})

        expected_specials = {
            8: ("Knocker", "coil", "used"),
            10: ("K1 Left/Right Coil Multiplexer", "relay", "used"),
            11: ("General Illumination (Inverted Relay)", "gi", "used"),
            13: ("Factory Driver 13 (No Load Fitted)", "virtual", "unused"),
            14: ("Factory Driver 14 (No Load Fitted)", "virtual", "unused"),
            23: ("Game On / Flipper and Switched-Solenoid Enable", "control_signal", "used"),
            45: ("Synthetic Right Flipper Power State", "virtual", "used"),
            48: ("Synthetic Left Flipper Hold State", "virtual", "used"),
        }
        self.assertEqual(expected_specials, {
            address: (solenoids[address]["label"], solenoids[address]["kind"], solenoids[address]["availability"])
            for address in expected_specials
        })
        self.assertEqual("Not Used", lamps[17]["label"])
        self.assertIn("X MODE", lamps[17]["physical"]["notes"])

    def test_legacy_bindings_survive_except_retired_lamp_111(self):
        for section in ("inputs", "outputs"):
            original = by_binding(self.baseline[section])
            current = by_binding(self.definition[section])
            for binding, record in original.items():
                if binding == ("pinmame.output.lamp", 111):
                    continue
                self.assertIn(binding, current)
                self.assertEqual(record["id"], current[binding]["id"], binding)
                self.assertTrue(alias_pairs(record) <= alias_pairs(current[binding]), binding)

        retired = next(record for record in self.baseline["outputs"]
                       if record["binding"] == {"group": "pinmame.output.lamp", "device": 111})
        self.assertEqual({"group": "pinmame.output.lamp", "device": 111}, retired["binding"])
        self.assertNotIn(("pinmame.output.lamp", 111), self.outputs)
        self.assertNotIn(retired["id"], {record["id"] for record in self.definition["outputs"]})
        migrated = {pair for pair in alias_pairs(retired) if pair[0] == "vpe-legacy.lamp"}
        gi_relay = self.outputs[("pinmame.output.solenoid", 11)]
        self.assertTrue(migrated <= alias_pairs(gi_relay))
        self.assertNotIn(("pinmame.lamp", "111"), alias_pairs(gi_relay))

        gi_spatial = gi_relay["spatial"]
        self.assertEqual("observed", gi_spatial["status"])
        self.assertEqual(len(spatial.GEOMETRY["gi"]), len(gi_spatial["placements"]))
        self.assertTrue(all(placement["role"] == "emitter" for placement in gi_spatial["placements"]))

    def test_display_and_flipper_controller_causality(self):
        self.assertEqual(1, len(self.definition["displays"]))
        display = self.definition["displays"][0]
        self.assertEqual(("display.dmd", "dmd", 0, 128, 32),
                         (display["id"], display["kind"], display["controller_index"],
                          display["width"], display["height"]))
        self.assertEqual(("not_applicable", "cabinet_or_service"),
                         (display["spatial"]["status"], display["spatial"]["reason"]))
        self.assertIn(pinmame.PINMAME_DEDMD_SOURCE_ID, display["provenance"]["source_refs"])

        self.assertEqual(
            {
                ("switch.flipper-column-82", "switch.matrix-16", "direct"),
                ("switch.flipper-column-84", "switch.matrix-15", "direct"),
            },
            {(item["source"], item["destination"], item["kind"])
             for item in self.definition["relationships"]},
        )

    def test_mechanism_inventory_has_exact_physical_causality(self):
        expected = {
            "mechanism.ball-feed": (("device.trough-eject-in", "device.trough-ball-release"),
                                    ("switch.trough-ball-4-jam", "switch.trough-ball-1", "switch.trough-ball-3", "switch.trough-ball-2")),
            "mechanism.ball-launch": (("device.auto-plunger",), ("switch.shooter-lane-auto-plunger",)),
            "mechanism.cabinet-shifter": ((), ("switch.launch-button", "switch.right-magna-save-coin-door")),
            "mechanism.left-scoop": (("device.left-saucer-eject",), ("switch.left-saucer-eject",)),
            "mechanism.right-scoop": (("device.right-saucer-eject",), ("switch.right-saucer-eject",)),
            "mechanism.return-vuk": (("device.left-popper-death-star-vuk",),
                                     ("switch.death-star-entrance", "switch.r2d2-entrance", "switch.death-star-vuk")),
            "mechanism.drop-bank": (("device.drop-target-bank-reset",),
                                    ("switch.drop-target-1", "switch.drop-target-2", "switch.drop-target-3")),
            "mechanism.death-star-bar": (("device.death-star-entrance-bar-motor",),
                                          ("switch.death-star-door-switch", "switch.death-star-door-closed-position", "switch.death-star-door-open-position")),
            "mechanism.death-star-r2-rotation": (("device.r2d2-2-death-star-rotation-motor",), ()),
            "mechanism.r2-dance": (("device.r2d2-up-motor",), ("switch.r2d2-position-switch-continuous",)),
            "mechanism.laser-kickback": (("device.kickback",), ("switch.rollover-lane-switch-continuous.24",)),
            "mechanism.top-bumper": (("device.top-turbo-bumper",), ("switch.top-bumper",)),
            "mechanism.left-bumper": (("device.left-turbo-bumper",), ("switch.middle-left-bumper",)),
            "mechanism.right-bumper": (("device.right-turbo-bumper",), ("switch.middle-right-bumper",)),
            "mechanism.bottom-bumper": (("device.bottom-turbo-bumper",), ("switch.bottom-bumper",)),
            "mechanism.left-sling": (("device.left-slingshot",), ("switch.left-slingshot",)),
            "mechanism.right-sling": (("device.right-slingshot",), ("switch.right-slingshot",)),
            "mechanism.left-flipper": (("solenoid.47", "device.flipper-lower-left"), ("switch.flipper-column-84",)),
            "mechanism.right-flipper": (("solenoid.45", "device.flipper-lower-right"), ("switch.flipper-column-82",)),
            "mechanism.knocker": (("solenoid.8",), ()),
        }
        self.assertEqual(set(expected), set(self.mechanisms))
        for identifier, (actuators, sensors) in expected.items():
            mechanism = self.mechanisms[identifier]
            self.assertEqual((actuators, sensors), (tuple(mechanism["actuators"]), tuple(mechanism["sensors"])))
            self.assertNotIn("timing", mechanism)
        self.assertIn("table physics", self.mechanisms["mechanism.ball-launch"]["behavior"])
        self.assertIn("not degrees or factory timing", self.mechanisms["mechanism.death-star-bar"]["behavior"])
        rotation = self.mechanisms["mechanism.death-star-r2-rotation"]["behavior"]
        self.assertIn("table-owned coast tuning", rotation)
        self.assertIn("two separate 28VAC motors", rotation)
        self.assertIn("515-5570-00", rotation)
        self.assertIn("515-5571-00", rotation)

    def test_partial_coverage_and_spatial_gaps_are_exact(self):
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["variant_differences", "spatial_placement", "unresolved_conflicts"], coverage["missing"])
        self.assertEqual(81, completion_score(coverage["status"], coverage["missing"]))
        self.assertEqual([], validate_machine(self.definition, ROOT))

        report = spatial.report(self.definition)
        unplaced = {binding for binding, record in self.outputs.items() if "spatial" not in record}
        self.assertEqual(
            {
                ("pinmame.output.solenoid", 29),
                ("pinmame.output.solenoid", 31),
                ("pinmame.output.solenoid", 32),
                ("pinmame.output.lamp", 29),
                ("pinmame.output.lamp", 30),
            },
            unplaced,
        )
        self.assertEqual({self.outputs[binding]["id"] for binding in unplaced}, set(report["unplaced_records"]))
        for device in self.definition["inputs"] + self.definition["outputs"]:
            spatial_record = device.get("spatial")
            if spatial_record is None:
                continue
            self.assertIn(spatial_record["status"], {"observed", "not_applicable"}, device["id"])
            for placement in spatial_record.get("placements", []):
                self.assertEqual("observed", placement["provenance"]["status"])
                self.assertGreaterEqual(placement["x"], 0)
                self.assertLessEqual(placement["x"], 1)
                self.assertGreaterEqual(placement["y"], 0)
                self.assertLessEqual(placement["y"], 1)

    def test_curator_is_deterministic_and_spatial_default_is_full_curation(self):
        self.assertEqual(spatial.canonical(self.definition), spatial.canonical(curator.build()))
        self.assertEqual(spatial.canonical(self.definition), spatial.canonical(spatial.build()))
        self.assertEqual(spatial.canonical(self.definition), DEFINITION.read_bytes().replace(b"\r\n", b"\n"))
        self.assertEqual(
            curator.knowledge(self.definition).encode("utf-8"),
            curator.KNOWLEDGE.read_bytes().replace(b"\r\n", b"\n"),
        )
        check = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/curate_star_wars.py"), "--check"],
            cwd=ROOT,
            env=os.environ.copy(),
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, check.returncode, check.stdout + check.stderr)

    def test_full_excerpt_digests_and_guard_mutants_fail_closed(self):
        excerpts = []
        for source in self.definition["sources"]:
            for excerpt in source.get("excerpts", []):
                excerpts.append(excerpt)
                path = ROOT / excerpt["path"]
                self.assertTrue(path.is_file(), path)
                self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), path)
                if "image" in excerpt:
                    image = ROOT / excerpt["image"]
                    self.assertTrue(image.is_file(), image)
                    self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image.read_bytes()).hexdigest(), image)
        self.assertGreaterEqual(len(excerpts), 5)
        with self.assertRaises(ValueError):
            curator.pinned(ROOT / excerpts[0]["path"], "0" * 64)
        with patch.object(curator, "EXCERPTS", ROOT / "not-a-retained-star-wars-excerpt-root"):
            with self.assertRaises(FileNotFoundError):
                curator.build()

        switches, lamps, coils = curator.manual_rows()
        self.assertEqual({1: "Plumb Tilt", 2: "4th Coin", 18: "Not Used", 52: "Not Used"},
                         {address: switches[address]["label"] for address in (1, 2, 18, 52)})
        self.assertEqual({17: "Not Used", 29: "Death Star Sphere 1", 30: "Death Star Sphere 2"},
                         {address: lamps[address]["label"] for address in (17, 29, 30)})
        with self.assertRaises(ValueError):
            pinmame.inputs(self.baseline["inputs"], {key: value for key, value in switches.items() if key != 64})
        with self.assertRaises(ValueError):
            pinmame.outputs(self.baseline["outputs"], {key: value for key, value in lamps.items() if key != 64}, coils)

    def test_rom_manifest_source_records_and_optional_checkout_are_pinned(self):
        seed = json.loads(PINMAME_SEED.read_text(encoding="utf-8"))
        canonical_drivers = json.dumps(seed["drivers"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("a8e7d46cc46bf3cda4f86994b86c3b0a95b7786f61a8c534839bd9e710e6c586",
                         hashlib.sha256(canonical_drivers).hexdigest())
        self.assertEqual("97aa922bf8e4b6970126192ec1ac1fb0305a4f62", pinmame.PINMAME_REVISION)
        self.assertEqual(EXPECTED_DRIVERS, {driver["id"] for driver in seed["drivers"]})
        self.assertEqual(11, len(seed["drivers"]))
        self.assertTrue(all(driver["roms"]["cpu"]["sha1"] and driver["roms"]["dmd"]["chips"] and driver["roms"]["sound"]["chips"]
                            for driver in seed["drivers"]))
        source_records = {record["id"]: record for record in pinmame.core_sources()}
        self.assertEqual(set(pinmame.PINMAME_SOURCE_IDS), set(source_records))
        self.assertEqual(
            set(seed["pinmame"]["source_files"].values()),
            {record["sha256"] for record in source_records.values()},
        )
        self.assertTrue(all(record["revision"] == pinmame.PINMAME_REVISION for record in source_records.values()))
        drivers = pinmame.driver_records(self.baseline["drivers"])
        self.assertEqual(EXPECTED_DRIVERS, {driver["id"] for driver in drivers})
        self.assertTrue(all(driver["physical_compatibility"] == "unknown" for driver in drivers))

        checkout = ROOT.parent.parent / "source-checkouts" / "pinmame"
        if not checkout.is_dir():
            self.skipTest("pinned PinMAME checkout is not retained beside the working root")
        head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True, capture_output=True)
        self.assertEqual(0, head.returncode, head.stderr)
        self.assertEqual(pinmame.PINMAME_REVISION, head.stdout.strip())
        self.assertEqual(seed["pinmame"]["source_files"], pinmame.verify_source_checkout(checkout))
        mutant = copy.deepcopy(pinmame._SEED)
        mutant["drivers"][0]["roms"]["cpu"]["sha1"] = "0" * 40
        with patch.object(pinmame, "_SEED", mutant):
            with self.assertRaises(ValueError):
                pinmame.verify_source_checkout(checkout)

    def test_runtime_derivative_and_optional_retained_runs_match_exactly(self):
        data = json.loads(curator.RUNTIME_PATH.read_text(encoding="utf-8"))
        self.assertEqual(curator.FACTS_SHA, hashlib.sha256(curator.RUNTIME_PATH.read_bytes()).hexdigest())
        self.assertEqual(curator.RUNTIME_SHA, hashlib.sha256(curator.RUNTIME_EVIDENCE.read_bytes()).hexdigest())
        source = json.loads(curator.RUNTIME_EVIDENCE.read_text(encoding="utf-8"))["source"]
        self.assertEqual(pinmame.PINMAME_REPOSITORY, source["repository"])
        self.assertEqual(pinmame.PINMAME_REVISION, source["revision"])
        self.assertEqual(("stwr_103", pinmame.PINMAME_REVISION, runtime_builder.LIBRARY_SHA),
                         (data["game"], data["pinmame_revision"], data["library_sha256"]))
        self.assertEqual({*range(1, 65), 82, 84}, {int(number) for number in data["switches"]})
        self.assertEqual(set(range(1, 65)), {int(number) for number in data["lamps"]})
        self.assertEqual(set(runtime_builder.COIL_NAMES), {int(number) for number in data["solenoids"]})
        self.assertEqual("MIDDLE LOOP", data["switches"]["18"]["name"])
        self.assertEqual("SHIFT UP", data["switches"]["52"]["name"])
        self.assertEqual("X MODE", data["lamps"]["17"]["name"])
        chips = next(driver for driver in pinmame._SEED["drivers"] if driver["id"] == "stwr_103")["roms"]
        members = {member["name"]: member for member in data["rom_archive"]["members"]}
        for chip in [chips["cpu"], *chips["dmd"]["chips"], *chips["sound"]["chips"]]:
            self.assertEqual((chip["crc32"], chip["sha1"]), (members[chip["name"]]["crc32"], members[chip["name"]]["sha1"]))
        self.assertEqual(data["artifact_manifest_sha256"],
                         hashlib.sha256(runtime_builder.canonical(data["artifacts"])).hexdigest())

        configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not configured:
            self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
        retained = Path(configured) / runtime_builder.FOLDER
        self.assertTrue(retained.is_dir(), retained)
        rebuilt = runtime_builder.build(retained)
        # Authorized ROMs are a separate optional read-only root. Even without
        # them every retained raw trace/frame is verified, rather than skipped.
        self.assertEqual({k:v for k,v in data.items() if k != "rom_archive"}, rebuilt)
        rom_root = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
        if rom_root:
            evidence = runtime_builder.envelope(rebuilt, retained, Path(rom_root))
            self.assertEqual(runtime_builder.canonical(data), runtime_builder.canonical(rebuilt))
            self.assertEqual(curator.RUNTIME_EVIDENCE.read_bytes(), runtime_builder.canonical(evidence))

    def test_navigation_rejects_unknown_and_ambiguous_titles(self):
        self.assertEqual([], title_reader.match_titles(bytes(4096), 128, 32))
        self.assertEqual([], title_reader.match_titles(bytes(4096), 32, 128))
        for name in ("not a ROM title", "SWITCH TEST"):
            with self.assertRaises(ValueError):
                title_reader.check_targets({"actions": [{"type": "pulse_until_display", "texts": [name]}]})
        for name in ("ACTIVE SWITCH TEST", "LAMP TEST", "CYCLING COILS"):
            title_reader.check_targets({"actions": [{"type": "pulse_until_display", "texts": [name]}]})
        configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not configured:
            self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
        root = Path(configured) / runtime_builder.FOLDER
        for title, template in title_reader.TEMPLATES.items():
            pixels = (root / template["source_frame"]).read_bytes().split(b"\n255\n", 1)[1]
            self.assertIn(title, title_reader.match_titles(pixels, 128, 32))


if __name__ == "__main__":
    unittest.main()
