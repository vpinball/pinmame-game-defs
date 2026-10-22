"""SlugFest identity, physical/runtime distinctions, determinism and retained evidence."""
from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

import curate_slugfest as curator  # noqa: E402
import slugfest_harness  # noqa: E402
from build_external_evidence_manifest import check_manifest  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _by_binding(machine: dict, section: str, group: str) -> dict[int, dict]:
    return {
        device["binding"]["device"]: device
        for device in machine[section]
        if device.get("binding", {}).get("group") == group
    }


def _source_by_id(machine: dict) -> dict[str, dict]:
    return {source["id"]: source for source in machine["sources"]}


def _expected_matrix() -> set[int]:
    return {column * 10 + row for column in range(1, 9) for row in range(1, 9)}


def _no_external_roots() -> dict[str, str]:
    return {
        "PINMAME_VPX_SOURCES_ROOT": "",
        "PINMAME_MANUALS_ROOT": "",
        "PINMAME_REVIEW_ARTIFACTS_ROOT": "",
    }


class SlugfestMachineBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = curator.build_machine()
        self.switches = _by_binding(self.machine, "inputs", curator.SWITCH)
        self.dips = _by_binding(self.machine, "inputs", curator.DIP)
        self.solenoids = _by_binding(self.machine, "outputs", curator.SOLENOID)
        self.lamps = _by_binding(self.machine, "outputs", curator.LAMP)
        self.gi = _by_binding(self.machine, "outputs", curator.GI)

    def test_public_address_spaces_are_complete_and_exact(self) -> None:
        # These are independently expressed ranges, not a count-only regression.
        self.assertEqual(set(range(1, 9)) | _expected_matrix() | set(range(111, 119)), set(self.switches))
        self.assertEqual(set(range(1, 9)), set(self.dips))
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(_expected_matrix(), set(self.lamps))
        self.assertEqual(set(range(5)), set(self.gi))

    def test_first_model_identity_and_exact_driver_pair(self) -> None:
        machine = self.machine["machine"]
        self.assertEqual("williams.slugfest-l-1.1991", machine["id"])
        self.assertEqual("SlugFest (First Model)", machine["name"])
        self.assertEqual("Williams", machine["manufacturer"])
        self.assertEqual(1991, machine["year"])
        self.assertEqual("60001", machine["model_number"])
        self.assertEqual(3281, machine["ipdb_id"])

        drivers = {driver["id"]: driver for driver in self.machine["drivers"]}
        self.assertEqual({"sf_l1", "sf_d1"}, set(drivers))
        self.assertEqual("sf_l1", drivers["sf_d1"]["clone_of"])
        for driver in drivers.values():
            self.assertEqual("Williams", driver["manufacturer"])
            self.assertEqual("1991", driver["year"])
            self.assertEqual("identical", driver["physical_compatibility"])

    def test_settled_matrix_and_callback_semantics(self) -> None:
        self.assertEqual("Center Target Panel", self.switches[44]["label"])
        self.assertEqual("opto", self.switches[54]["physical"]["switch_type"])
        self.assertNotIn("part_number", self.switches[54]["physical"])
        self.assertEqual("Target Panel 3 Right", self.switches[45]["label"])
        self.assertRegex(self.switches[44]["physical"]["notes"], r"center\s*/\s*3R")
        self.assertRegex(self.switches[45]["physical"]["notes"], r"center\s*/\s*3R")

        dispenser_lamp = self.solenoids[28]
        self.assertEqual("Dispenser Low Lamp", dispenser_lamp["label"])
        self.assertEqual("lamp", dispenser_lamp["kind"])
        self.assertEqual({"group": curator.SOLENOID, "device": 28}, dispenser_lamp["binding"])
        self.assertEqual("20-9679", dispenser_lamp["physical"]["part_number"])
        self.assertIn("lamp", dispenser_lamp["physical"]["notes"].casefold())
        self.assertNotEqual("motor", dispenser_lamp["kind"])
        self.assertNotEqual("flasher", dispenser_lamp["kind"])

    def test_pitch_motor_is_one_physical_motor_with_three_drive_branches(self) -> None:
        for address in (22, 23, 24):
            with self.subTest(address=address):
                device = self.solenoids[address]
                self.assertEqual("motor", device["kind"])
                self.assertEqual("14-7959", device["physical"]["part_number"])
                self.assertNotIn("quantity", device["physical"])
                self.assertIn("One shared", device["physical"]["notes"])
        pitcher = next(item for item in self.machine["mechanisms"] if item["id"] == "mechanism.pitcher")
        self.assertEqual(["solenoid.22", "solenoid.23", "solenoid.24"], pitcher["actuators"])
        self.assertRegex(pitcher["behavior"], r"One\s*14-7959 motor")

    def test_trough_component_type_uses_factory_catalog_and_game_specific_fitment(self) -> None:
        for address in (51, 52):
            with self.subTest(address=address):
                device = self.switches[address]
                self.assertEqual("microswitch", device["physical"]["switch_type"])
                self.assertEqual("5647-12133-08", device["physical"]["part_number"])
                self.assertIn(curator.MANUAL, device["provenance"]["source_refs"])
                self.assertIn(curator.COMPONENTS, device["provenance"]["source_refs"])

    def test_unjammed_is_an_operator_button_and_gi_headers_stay_distinct(self) -> None:
        button = self.switches[28]
        self.assertEqual("button", button["physical"]["switch_type"])
        self.assertFalse(button["normally_closed"])
        self.assertNotIn("initial_active", button)
        self.assertIn("operator pushbutton", button["physical"]["notes"])
        self.assertIn("table simplification", button["physical"]["notes"])
        self.assertEqual("J121-11", self.gi[3]["wiring"]["drive_connection"])
        self.assertEqual("J120-11", self.gi[4]["wiring"]["drive_connection"])

    def test_native_switch_edges_prove_named_active_levels_and_virtual_pairs(self) -> None:
        evidence = json.loads(curator.RUNTIME_PATH.read_bytes())
        observations = evidence["runtime"]["observations"]
        snapshots = {item["label"]: item for item in observations["diagnostic_snapshots"]}
        names = {41: "Target Panel-L", 23: "Dispenser Prize", 54: "Pitch Opto", 55: "Ramp Opto", 61: "L Bleacher", 62: "M Bleacher", 63: "R Bleacher"}
        self.assertEqual(21, len(snapshots))
        for address, name in names.items():
            with self.subTest(address=address):
                self.assertEqual(name, snapshots[f"switch {address} public1"]["interpreted_text"])
                for state in ("public0", "released"):
                    self.assertIn("no active switch name", snapshots[f"switch {address} {state}"]["interpreted_text"])
                self.assertEqual(address in {54, 55, 61, 62, 63}, self.switches[address]["normally_closed"])
                self.assertIn(curator.RUNTIME, self.switches[address]["provenance"]["source_refs"])
        actions = {item["input_address"]: item for item in observations["named_action_observations"]}
        for button, pair in ((112, [45, 46]), (114, [47, 48])):
            self.assertEqual([], actions[button]["observed_switch_addresses"])
            self.assertEqual([button], actions[button]["host_stimulus_switch_addresses"])
            self.assertEqual(pair, actions[button]["transitioned_solenoid_addresses"])
            self.assertEqual([31, *pair], actions[button]["active_solenoid_addresses"])
            for output in pair:
                self.assertEqual("virtual", self.solenoids[output]["kind"])
                self.assertEqual("used", self.solenoids[output]["availability"])
                self.assertNotIn("quantity", self.solenoids[output].get("physical", {}))

    def test_wpc_state_roles_distinguish_registers_fitted_relay_and_constant_zero(self) -> None:
        for address in (29, 30):
            with self.subTest(register=address):
                output = self.solenoids[address]
                self.assertEqual("used", output["availability"])
                self.assertEqual("virtual", output["kind"])
                self.assertEqual(["internal.wpc-state"], output["roles"])
                self.assertEqual("virtual", output["spatial"]["reason"])
                self.assertNotIn("part_number", output["physical"])
                self.assertIn("physical function remain unproven", output["physical"]["notes"])
        relay = self.solenoids[31]
        self.assertEqual("used", relay["availability"])
        self.assertEqual("relay", relay["kind"])
        self.assertEqual(["internal.wpc-state"], relay["roles"])
        self.assertEqual("5580-08994-01", relay["physical"]["part_number"])
        self.assertEqual("Q99", relay["wiring"]["driver_transistor"])
        self.assertEqual("cabinet_or_service", relay["spatial"]["reason"])
        self.assertIn(curator.MANUAL, relay["provenance"]["source_refs"])
        self.assertIn(curator.RUNTIME, relay["provenance"]["source_refs"])
        zero = self.solenoids[32]
        self.assertEqual("unused", zero["availability"])
        self.assertEqual("virtual", zero["kind"])
        self.assertEqual(["internal.unused.wpc-output"], zero["roles"])
        self.assertEqual("virtual", zero["spatial"]["reason"])
        self.assertIn("zero", zero["physical"]["notes"].lower())

    def test_cabinet_backbox_and_out_of_bounds_controls_are_not_clamped(self) -> None:
        # The manual controls physical classification.  In particular, no VPX
        # helper center is converted into a playfield coordinate for these devices.
        for address in (11, 21, 31):
            with self.subTest(controlled_lamp=address):
                spatial = self.lamps[address]["spatial"]
                self.assertEqual("not_applicable", spatial["status"])
                self.assertEqual("cabinet_or_service", spatial["reason"])
                self.assertNotIn("placements", spatial)
                self.assertEqual("Rear upright Bleachers Assembly", self.lamps[address]["physical"]["location"])
        for address in (17, 18, 19):
            with self.subTest(bleacher_flasher=address):
                spatial = self.solenoids[address]["spatial"]
                self.assertEqual("not_applicable", spatial["status"])
                self.assertEqual("cabinet_or_service", spatial["reason"])
                self.assertNotIn("placements", spatial)
                self.assertEqual("Cabinet/rear upright Bleachers Assembly", self.solenoids[address]["physical"]["location"])
        for address in range(81, 87):
            with self.subTest(control_lamp=address):
                spatial = self.lamps[address]["spatial"]
                self.assertEqual("not_applicable", spatial["status"])
                self.assertEqual("cabinet_or_service", spatial["reason"])
                self.assertNotIn("placements", spatial)

    def test_only_target_projections_are_canonical_and_light_references_stay_in_report(self) -> None:
        seed = curator.seed()
        report = curator.build_report(self.machine)
        projections = [row for row in seed["placements"] if row["classification"] == "target-face projection"]
        inserts = [row for row in seed["placements"] if row["classification"] == "candidate insert reference (not bulb)"]
        flashers = [row for row in seed["placements"] if row["classification"] == "candidate flasher Light center"]
        self.assertEqual(set(range(41, 48)), {row["address"] for row in projections})
        self.assertEqual(53, len(inserts))
        self.assertEqual({20, 25, 26}, {row["address"] for row in flashers})
        for address in range(41, 48):
            spatial = self.switches[address]["spatial"]
            self.assertEqual("observed", spatial["status"])
            self.assertIn("projection", self.switches[address]["physical"]["notes"])
            self.assertEqual("observed", spatial["placements"][0]["provenance"]["status"])
        for address in (20, 25, 26):
            self.assertNotIn("spatial", self.solenoids[address])
        for address in {row["address"] for row in inserts}:
            self.assertNotIn("spatial", self.lamps[address])
        self.assertEqual(63, len(report["reference_candidates"]))
        self.assertEqual("partial", self.machine["coverage"]["status"])
        self.assertIn("spatial_placement", self.machine["coverage"]["missing"])

    def test_gi_does_not_infer_bulb_quantities_from_script_helpers(self) -> None:
        # Playfield/backbox helpers are not a physical inventory. Pitch-control four
        # lamps are a separate factory-table fact, so retain that sole direct count.
        for address in (0, 1, 3, 4):
            with self.subTest(gi=address):
                self.assertNotIn("quantity", self.gi[address]["physical"])
                self.assertIn("No quantity inferred", self.gi[address]["physical"]["notes"])
        self.assertEqual(4, self.gi[2]["physical"]["quantity"])
        self.assertRegex(self.gi[2]["physical"]["notes"], r"PDF\s*97\s*/\s*2-37")

    def test_full_hashes_and_excerpt_provenance_are_present(self) -> None:
        sources = _source_by_id(self.machine)
        expected_hashes = {
            curator.CORE: "ca2339f2806c95061b22a5be44314ded4874f78f54e9e129064c0f851d17ef9f",
            curator.MANUAL: curator.MANUAL_SHA256,
            curator.SUPPLEMENT: curator.SUPPLEMENT_SHA256,
            curator.AMENDMENTS: curator.AMENDMENTS_SHA256,
            curator.COMPONENTS: curator.COMPONENT_PAGE_SHA256,
            curator.VPX_SCRIPT: curator.SCRIPT_SHA256,
            curator.VPX_TABLE: curator.TABLE_SHA256,
            curator.EXTRACTION: curator.EXTRACTION_MANIFEST_SHA256,
        }
        for source_id, expected in expected_hashes.items():
            with self.subTest(source=source_id):
                self.assertEqual(expected, sources[source_id]["sha256"])
                self.assertIsNotNone(re.fullmatch(r"[0-9a-f]{64}", sources[source_id]["sha256"]))
        for source in sources.values():
            for excerpt in source.get("excerpts", []):
                with self.subTest(excerpt=excerpt["id"]):
                    self.assertTrue(excerpt["locator"])
                    self.assertTrue(excerpt["method"])
                    self.assertTrue(excerpt["transcribed_by"])
                    self.assertTrue(excerpt["reviewed"])
                    path = ROOT / excerpt["path"]
                    self.assertTrue(path.is_file())
                    self.assertEqual(excerpt["sha256"], _sha256(path))

    def test_build_report_uses_the_declared_coordinate_convention_and_stays_partial(self) -> None:
        report = curator.build_report(self.machine)
        self.assertEqual("williams.slugfest-l-1.1991", report["machine_id"])
        self.assertTrue(report["decision"].startswith("partial:"))
        self.assertEqual("xleft0/right1;yrear0/front1", report["transform"]["convention"].replace(" ", ""))
        self.assertEqual(curator.TABLE_SHA256, report["table_sha256"])
        self.assertEqual(curator.SCRIPT_SHA256, report["script_sha256"])
        self.assertEqual(curator.MANUAL_SHA256, report["manual_sha256"])
        self.assertEqual(curator.EXTRACTION_MANIFEST_SHA256, report["extraction"]["manifest_sha256"])
        self.assertEqual(7, report["located_device_count"])
        self.assertEqual(63, len(report["reference_candidates"]))
        self.assertIn("target contacts projected", report["projection_classes"][0])


class SlugfestSeedGuardTests(unittest.TestCase):
    def _assert_seed_rejected(self, mutator, message: str) -> None:
        malformed = deepcopy(curator.seed())
        mutator(malformed)
        # Patch the imported loader rather than editing a real seed: this proves
        # the curator's own guard and leaves retained evidence immutable.
        with patch.object(curator, "load_json", return_value=malformed):
            with self.assertRaisesRegex(ValueError, message):
                curator.seed()

    def test_seed_rejects_missing_device_binding(self) -> None:
        self._assert_seed_rejected(lambda value: value["placements"].pop(), "missing, duplicate or unexpected")

    def test_seed_rejects_raw_normalization_drift(self) -> None:
        self._assert_seed_rejected(
            lambda value: value["placements"][0].__setitem__("raw_x", value["placements"][0]["raw_x"] + 1),
            "normalization drift",
        )

    def test_seed_rejects_bounds_drift(self) -> None:
        self._assert_seed_rejected(lambda value: value["bounds"].__setitem__("right", 1101), "bounds drift")

    def test_seed_rejects_source_identity_hash_drift(self) -> None:
        self._assert_seed_rejected(lambda value: value.__setitem__("table_sha256", "0" * 64), "does not identify")


class SlugfestDeterminismTests(unittest.TestCase):
    def _generated_bytes(self) -> dict[Path, bytes]:
        machine = curator.build_machine()
        report = curator.build_report(machine)
        expected = {
            curator.MACHINE_PATH: canonical_bytes(machine),
            curator.REPORT_PATH: canonical_bytes(report),
        }
        knowledge = curator.KNOWLEDGE_SEED_PATH.read_text(encoding="utf-8")
        expected[curator.KNOWLEDGE_PATH] = knowledge.encode("utf-8")
        expected[curator.REPORT_MARKDOWN_PATH] = curator.report_markdown(report).encode("utf-8")
        return expected

    def test_builders_are_byte_deterministic(self) -> None:
        first_machine, second_machine = curator.build_machine(), curator.build_machine()
        self.assertEqual(canonical_bytes(first_machine), canonical_bytes(second_machine))
        self.assertEqual(canonical_bytes(curator.build_report(first_machine)), canonical_bytes(curator.build_report(second_machine)))
        self.assertEqual(curator.seed(), curator.seed())

    def test_canonical_outputs_exist_and_match_exactly(self) -> None:
        expected = self._generated_bytes()
        for path, payload in expected.items():
            with self.subTest(path=path):
                self.assertEqual(payload, path.read_bytes())

    def test_check_mode_is_builder_deterministic_without_writing_the_repository(self) -> None:
        machine = curator.build_machine()
        report = curator.build_report(machine)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source_excerpts = curator.EXCERPT_ROOT
            temporary_excerpts = temporary / "evidence" / "excerpts" / curator.MACHINE_ID
            shutil.copytree(source_excerpts, temporary_excerpts)
            runtime_path = temporary / "evidence" / "runtime" / "wpc-alpha" / "slugfest-switch-edges.json"
            runtime_path.parent.mkdir(parents=True)
            runtime_path.write_bytes(curator.RUNTIME_PATH.read_bytes())
            machine_path = temporary / "machines" / "partial" / "williams" / "slugfest-l-1-1991.json"
            report_path = temporary / "reports" / "spatial" / "williams" / "slugfest-l-1-1991.json"
            knowledge_path = temporary / "knowledge" / "williams" / "slugfest-l-1-1991.md"
            markdown_path = temporary / "reports" / "spatial" / "williams" / "slugfest-l-1-1991.md"
            for path, payload in {
                machine_path: canonical_bytes(machine),
                report_path: canonical_bytes(report),
                knowledge_path: curator.KNOWLEDGE_SEED_PATH.read_bytes(),
                markdown_path: curator.report_markdown(report).encode("utf-8"),
            }.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
            with patch.multiple(
                curator,
                ROOT=temporary,
                EXCERPT_ROOT=temporary_excerpts,
                RUNTIME_PATH=runtime_path,
                MACHINE_PATH=machine_path,
                REPORT_PATH=report_path,
                KNOWLEDGE_PATH=knowledge_path,
                REPORT_MARKDOWN_PATH=markdown_path,
                AUTHOR_READY_PATH=temporary / "author-ready.json",
            ), patch.dict(os.environ, _no_external_roots()), patch.object(sys, "argv", ["curate_slugfest.py", "--check"]):
                self.assertEqual(0, curator.main())
                self.assertEqual(0, curator.main())
                machine_path.write_bytes(b"{}\n")
                with self.assertRaisesRegex(ValueError, "curator drift"):
                    curator.main()

    def test_author_ready_refusal_is_a_real_main_guard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            author_ready_path = Path(directory) / "author-ready.json"
            author_ready_path.write_text("{}\n", encoding="utf-8")
            with patch.object(curator, "AUTHOR_READY_PATH", author_ready_path), patch.object(sys, "argv", ["curate_slugfest.py", "--check"]):
                with self.assertRaisesRegex(ValueError, "refusing to overwrite an existing author-ready definition"):
                    curator.main()


class SlugfestRetainedEvidenceTests(unittest.TestCase):
    def test_retained_native_frames_and_scenario_match_exactly(self) -> None:
        review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not review_root:
            self.skipTest("retained review-artifact root not configured")
        root = Path(review_root) / curator.MACHINE_ID
        self.assertTrue(root.is_dir(), "explicit review-artifact root missing")
        evidence = json.loads(curator.RUNTIME_PATH.read_bytes())
        run = evidence["runtime"]["raw_runs"][0]
        raw_path = root / "harness" / f"{run['name']}.json"
        self.assertEqual(run["sha256"], _sha256(raw_path))
        raw = json.loads(raw_path.read_bytes())
        self.assertIsNone(raw["failure"])
        self.assertEqual(run["scenario_sha256"], _sha256(ROOT / run["scenario_path"]))
        self.assertEqual(run["scenario_sha256"], raw["scenario"]["sha256"])
        self.assertEqual(run["action_count"], len(raw["steps"]))
        self.assertEqual(evidence["runtime"]["emulator"]["sha256"], raw["library_sha256"])
        snapshots = {item["label"]: item for item in raw["snapshots"]}
        for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]:
            recorded = snapshots[item["label"]]
            self.assertEqual(item["pixel_sha256"], recorded["displays"][0]["pixel_sha256"])
            self.assertEqual(item["active_solenoid_addresses"], recorded["active_solenoids"])
            # Preserve the original recorded locator; find its retained basename
            # without rewriting the immutable raw run after worktree cleanup.
            frame_path = root / "harness" / "switch-edges-2-dmd" / Path(recorded["displays"][0]["artifact"]).name
            frame = frame_path.read_bytes()
            pixel_bytes = frame.split(b"\n", 3)[-1]
            self.assertEqual(4096, len(pixel_bytes))
            self.assertEqual(item["pixel_sha256"], hashlib.sha256(pixel_bytes).hexdigest())

    def test_verify_external_sources_is_a_clean_no_op_without_configured_roots(self) -> None:
        with patch.dict(os.environ, _no_external_roots()):
            self.assertIsNone(curator.verify_external_sources())

    def _roots_or_skip(self) -> tuple[Path, Path]:
        vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        manuals_root = os.environ.get("PINMAME_MANUALS_ROOT")
        if not vpx_root or not manuals_root:
            self.skipTest("retained VPX/manual roots are not configured")
        vpx, manuals = Path(vpx_root), Path(manuals_root)
        if not vpx.is_dir() or not manuals.is_dir():
            self.fail("explicit retained VPX/manual root does not exist")
        return vpx, manuals

    def test_external_sources_recompute_full_manifest_hashes_and_raw_centers(self) -> None:
        vpx_root, manuals_root = self._roots_or_skip()
        table_base = vpx_root / "williams" / curator.SLUG
        extraction = table_base / "extracted-vpxtool"
        manual_base = manuals_root / "by-machine" / curator.MACHINE_ID

        curator.verify_external_sources()
        self.assertEqual(curator.EXTRACTION_MANIFEST_SHA256, check_manifest(extraction, "sf_l1"))
        manifest = json.loads((extraction / "manifest.json").read_bytes())
        self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
        self.assertEqual(curator.EXTRACTION_TOTAL_BYTES, sum(item["size"] for item in manifest["files"]))
        self.assertEqual(curator.TABLE_SHA256, _sha256(table_base / curator.TABLE_NAME))
        self.assertEqual(curator.SCRIPT_SHA256, _sha256(extraction / "script.vbs"))
        for name, digest in (
            (curator.MANUAL_NAME, curator.MANUAL_SHA256),
            (curator.SUPPLEMENT_NAME, curator.SUPPLEMENT_SHA256),
            (curator.AMENDMENTS_NAME, curator.AMENDMENTS_SHA256),
        ):
            with self.subTest(manual=name):
                self.assertEqual(digest, _sha256(manual_base / name))

        collection = next(item["items"] for item in json.loads((extraction / "collections.json").read_bytes()) if item["name"] == "AllLamps")
        for row in curator.seed()["placements"]:
            with self.subTest(object=row["object"]):
                payload = json.loads((extraction / row["file"]).read_bytes())
                self.assertEqual(row["type"], next(iter(payload)))
                self.assertEqual({"x": row["raw_x"], "y": row["raw_y"]}, payload[row["type"]]["center"])
                if row["group"] == curator.LAMP:
                    self.assertIn(row["object"], collection)
                    self.assertEqual(row["address"], payload[row["type"]]["timer_interval"])

    def test_out_of_range_control_helpers_are_observed_but_never_clamped(self) -> None:
        vpx_root, _ = self._roots_or_skip()
        extraction = vpx_root / "williams" / curator.SLUG / "extracted-vpxtool"
        collection = next(item["items"] for item in json.loads((extraction / "collections.json").read_bytes()) if item["name"] == "AllLamps")
        expected_centers = {
            81: (713.375, 2149.486), 82: (827.47125, 2149.9902), 83: (938.637, 2149.6484),
            84: (408.25012, 2150.019), 85: (561.2797, 2138.5566), 86: (563.14215, 2232.584),
        }
        lamps = _by_binding(curator.build_machine(), "outputs", curator.LAMP)
        for address, center in expected_centers.items():
            with self.subTest(address=address):
                name = f"L{address}"
                light = json.loads((extraction / "gameitems" / f"Light.{name}.json").read_bytes())["Light"]
                self.assertEqual({"x": center[0], "y": center[1]}, light["center"])
                self.assertGreater(light["center"]["y"], 2000)
                self.assertIn(name, collection)
                self.assertEqual(address, light["timer_interval"])
                self.assertEqual("not_applicable", lamps[address]["spatial"]["status"])
                self.assertNotIn("placements", lamps[address]["spatial"])

    def test_external_table_hash_guard_can_fail_without_mutating_retained_bytes(self) -> None:
        vpx_root, manuals_root = self._roots_or_skip()
        table_path = (vpx_root / "williams" / curator.SLUG / curator.TABLE_NAME).resolve()
        real_sha256 = curator.sha256

        def wrong_table_hash(path: Path) -> str:
            if path.resolve() == table_path:
                return "0" * 64
            return real_sha256(path)

        with patch.object(curator, "sha256", side_effect=wrong_table_hash), patch.dict(
            os.environ,
            {"PINMAME_VPX_SOURCES_ROOT": str(vpx_root), "PINMAME_MANUALS_ROOT": str(manuals_root)},
        ):
            with self.assertRaisesRegex(ValueError, "VPX/script hash drift"):
                curator.verify_external_sources()


class SlugfestHarnessGuardTests(unittest.TestCase):
    def test_visually_retained_template_matches_only_its_exact_title_band(self) -> None:
        title, template = next(iter(slugfest_harness.TEMPLATES.items()))
        first, last = template["rows"]
        frame = bytearray(128 * 32)
        frame[first * 128:(last + 1) * 128] = base64.b64decode(template["mask"])
        self.assertEqual([title], slugfest_harness.match_titles(frame, 128, 32))
        self.assertEqual([], slugfest_harness.match_titles(frame, 127, 32))

    def test_title_checkpoint_guards_reject_unknown_and_ambiguous_targets(self) -> None:
        scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-alpha" / "sf-switch-edges.json"
        slugfest_harness.check_targets(json.loads(scenario_path.read_text(encoding="utf-8")))
        with self.assertRaisesRegex(ValueError, "unverified or ambiguous"):
            slugfest_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["UNVERIFIED TITLE"]}]})
        # A prefix would be unsafe if a later retained template extended it.
        # Use the harness's real ambiguity guard with an in-memory template set.
        with patch.object(slugfest_harness, "TEMPLATES", {"MENU": {}, "MENU EXTENDED": {}}):
            with self.assertRaisesRegex(ValueError, "unverified or ambiguous"):
                slugfest_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["MENU"]}]})

    def test_harness_refuses_a_title_checkpoint_for_the_wrong_game(self) -> None:
        argv = [
            "slugfest_harness.py", "--library", "unused", "--game", "sf_d1",
            "--rom-path", "unused", "--work-dir", "unused",
        ]
        with patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(ValueError, "verified only against sf_l1"):
                slugfest_harness.main()


if __name__ == "__main__":
    unittest.main()
