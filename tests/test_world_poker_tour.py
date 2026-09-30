from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "world-poker-tour-2006"
MACHINE = ROOT / "machines/partial/stern" / f"{NAME}.json"
AUDIT = ROOT / "reports/spatial/stern" / f"{NAME}.json"
SCRIPT = ROOT / "tools/curate_world_poker_tour.py"
SEED = ROOT / "tools/seeds/stern" / f"{NAME}.json"
SPATIAL = ROOT / "tools/seeds/stern" / f"{NAME}-spatial.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def address_map(records: list[dict], group: str) -> dict[int, dict]:
    return {item["binding"]["device"]: item for item in records if item["binding"]["group"] == group}


class WorldPokerTourDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load(MACHINE)
        cls.seed = load(SEED)
        cls.spatial = load(SPATIAL)

    def test_one_physical_game_and_all_46_variants(self) -> None:
        definition = self.definition
        self.assertEqual(("stern.world-poker-tour.2006", 5134, "G5poe-MQrb5"), (
            definition["machine"]["id"], definition["machine"]["ipdb_id"], definition["machine"]["opdb_id"]))
        self.assertEqual("partial", definition["coverage"]["status"])
        self.assertEqual(46, len(definition["drivers"]))
        self.assertEqual({d["id"] for d in definition["drivers"]},
                         {d["id"] for d in load(ROOT / "catalog/pinmame.json")["drivers"] if d["id"].startswith("wpt_")})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in definition["drivers"]))
        variants = {d["id"]: d for d in definition["drivers"]}
        self.assertIn("immediate auto-launch", variants["wpt_103a"]["variant_notes"])
        self.assertIn("without auto-launch", variants["wpt_111a"]["variant_notes"])
        self.assertIn("without auto-launch", variants["wpt_140l"]["variant_notes"])
        self.assertFalse((ROOT / "machines/author-ready/stern" / f"{NAME}.json").exists())

    def test_full_public_address_disposition(self) -> None:
        switches = address_map(self.definition["inputs"], "pinmame.input.switch")
        self.assertEqual(set(range(-7, 1)) | set(range(1, 73)) | set(range(81, 89)), set(switches))
        self.assertEqual(set(range(1, 9)), set(address_map(self.definition["inputs"], "pinmame.input.dip")))
        self.assertEqual({1, 2, 17, 64}, {i for i in range(1, 65) if switches[i]["availability"] == "unused"})
        self.assertEqual("used", switches[21]["availability"])
        self.assertEqual("opto", switches[21]["physical"]["switch_type"])
        self.assertEqual("conflicted", switches[54]["provenance"]["status"])
        self.assertEqual("conflicted", switches[56]["provenance"]["status"])
        self.assertEqual("J2-P2", switches[65]["wiring"]["drive_connection"])
        self.assertEqual("J2-P6", switches[68]["wiring"]["drive_connection"])
        self.assertTrue(all(switches[i]["normally_closed"] for i in (83, 81, 87, 85)))
        self.assertTrue(all(not switches[i]["normally_closed"] for i in (84, 82, 88, 86)))
        solenoids = address_map(self.definition["outputs"], "pinmame.output.solenoid")
        lamps = address_map(self.definition["outputs"], "pinmame.output.lamp")
        self.assertEqual(set(range(1, 67)), set(solenoids))
        self.assertEqual(set(range(1, 340)), set(lamps))
        self.assertEqual("unused", lamps[77]["availability"])
        self.assertEqual("Queen of spades", lamps[42]["label"])
        self.assertEqual("optional", solenoids[24]["availability"])
        self.assertEqual("conflicted", solenoids[32]["provenance"]["status"])
        self.assertEqual("090-5034-ND", solenoids[32]["physical"]["part_number"])
        self.assertEqual(("ORG", "J6-P10", "BLK-GRY", "J6-P8"),
                         (solenoids[32]["wiring"]["power_wire"], solenoids[32]["wiring"]["power_connection"],
                          solenoids[32]["wiring"]["control_wire"], solenoids[32]["wiring"]["control_connection"]))
        self.assertEqual({0}, set(address_map(self.definition["outputs"], "pinmame.output.gi")))

    def test_displays_mechanisms_and_spatial_limits(self) -> None:
        displays = self.definition["displays"]
        self.assertEqual(15, len(displays))
        self.assertEqual((128, 32), (displays[0]["width"], displays[0]["height"]))
        self.assertEqual({(5, 7)}, {(d["width"], d["height"]) for d in displays[1:]})
        self.assertTrue(all("spatial" not in d for d in displays[1:]))
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        for ident in ("four-ball-trough", "left-eight-bank", "middle-four-bank",
                      "right-four-bank", "jail-bars", "left-ramp", "right-ramp"):
            self.assertIn(f"mechanism.{ident}", mechanisms)
        self.assertEqual(2, len([m for m in mechanisms.values() if m["kind"] == "drop_target_bank" and len(m["sensors"]) == 4]))
        lamps = address_map(self.definition["outputs"], "pinmame.output.lamp")
        self.assertEqual(("observed", 0.448267, 0.525167),
                         (lamps[9]["spatial"]["status"], lamps[9]["spatial"]["placements"][0]["x"], lamps[9]["spatial"]["placements"][0]["y"]))
        for number in (1, 2, 67, 68, 75, 76, 77):
            self.assertEqual("not_applicable", lamps[number]["spatial"]["status"])
        self.assertNotIn("spatial", lamps[3])  # Apron lamp has no proved socket coordinate.
        audit = load(AUDIT)
        self.assertEqual("pinmame-spatial-blockers", audit["format"])
        self.assertEqual(self.spatial["table_manifest_sha256"], audit["extraction_manifest_sha256"])
        self.assertIn("coil.22-left-slingshot-flasher", audit["missing_spatial_ids"])
        self.assertIn("lamp.3-deal-again", audit["missing_spatial_ids"])
        self.assertEqual({"conflict.sw54-fitment", "conflict.sw56-construction", "conflict.q32-coil"},
                         set(audit["unresolved_conflict_ids"]))

    def test_excerpt_and_scenario_integrity(self) -> None:
        sources = {s["id"]: s for s in self.definition["sources"]}
        for source in sources.values():
            for excerpt in source.get("excerpts", []):
                path = ROOT / excerpt["path"]
                self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        scenario = load(ROOT / "tools/harness-scenarios/stern" / f"{NAME}-switch-test.json")
        self.assertEqual("wpt_140a", scenario["game"])
        self.assertEqual([3, 21, 63], [a["switch"] for a in scenario["actions"] if a["type"] == "pulse"])
        self.assertIn("DMD frames", scenario["notes"])
        coil_scenario = load(ROOT / "tools/harness-scenarios/stern" / f"{NAME}-coil-sweep.json")
        self.assertEqual(31, sum(a.get("label", "").startswith("advance coil diagnostic") for a in coil_scenario["actions"]))
        self.assertIn("skips Q24", coil_scenario["notes"])
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

    def test_deterministic_curator_and_fail_closed_wrong_root(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        for key in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_SOURCE_ROOT", "PINMAME_SCRIPTS_ROOT"):
            env.pop(key, None)
        for _ in range(2):
            checked = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check"], cwd=ROOT, env=env,
                                     capture_output=True, text=True, check=False)
            self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
        with tempfile.TemporaryDirectory() as temp:
            env["PINMAME_MANUALS_ROOT"] = temp
            checked = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check"], cwd=ROOT, env=env,
                                     capture_output=True, text=True, check=False)
            self.assertNotEqual(0, checked.returncode)
            self.assertIn("missing or wrong retained artifact", checked.stderr)

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not configured")
    def test_retained_vpx_manifest_recomputes(self) -> None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("external_manifest", ROOT / "tools/build_external_evidence_manifest.py")
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "stern/world-poker-tour-2006/wpt-062018a"
        self.assertEqual(self.spatial["table_sha256"], hashlib.sha256((base / "wpt 062018a.vpx").read_bytes()).hexdigest())
        self.assertEqual(self.spatial["table_manifest_sha256"],
                         module.check_manifest(base / "extract-vpxtool-v1", "wpt_140a"))
        alternate = base.parent / "world-poker-tour-stern-2006"
        self.assertEqual("92a9720af51c825c9603d9dc78acc2423b7f86c907e1c4a6e92393156a22d9b8",
                         hashlib.sha256((alternate / "World Poker Tour (Stern 2006).vpx").read_bytes()).hexdigest())
        self.assertEqual("368e8262d51e6db70f8f05a8919f008d8d0a92340d29b1527ff8e9c700ada9e6",
                         module.check_manifest(alternate / "extract-vpxtool-v1", "wpt_140a"))

    @unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
    def test_retained_manual_and_bulletin(self) -> None:
        base = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine/stern.world-poker-tour.2006"
        sources = {s["id"]: s for s in self.definition["sources"]}
        self.assertEqual(sources["manual.stern-wpt-2006"]["sha256"],
                         hashlib.sha256((base / "World_Poker_Tour_Manual.pdf").read_bytes()).hexdigest())
        self.assertEqual(sources["bulletin.stern-wpt-165"]["sha256"],
                         hashlib.sha256((base / "sb165.pdf").read_bytes()).hexdigest())

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime root not configured")
    def test_retained_rom_diagnostic(self) -> None:
        base = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "stern.world-poker-tour.2006/session-20260930"
        source = next(s for s in self.definition["sources"] if s["id"] == "runtime.wpt-140a-switch-test")
        run = base / "wpt-switch-test-final-run.json"
        self.assertEqual(source["sha256"], hashlib.sha256(run.read_bytes()).hexdigest())
        switch_data = load(run)
        events = switch_data["events"]
        switch_scenario = ROOT / "tools/harness-scenarios/stern" / f"{NAME}-switch-test.json"
        self.assertEqual(hashlib.sha256(switch_scenario.read_bytes()).hexdigest(), switch_data["scenario"]["sha256"])
        self.assertEqual(15, sum(e["event"] == "display_available" for e in events))
        self.assertEqual({3, 21, 63}, {e["number"] for e in events if e.get("event") == "switch" and e.get("state") == 1 and e.get("number") in {3, 21, 63}})
        coil_source = next(s for s in self.definition["sources"] if s["id"] == "runtime.wpt-140a-coil-test")
        coil_run = base / "wpt-coil-diagnostic-final-v2-run.json"
        self.assertEqual(coil_source["sha256"], hashlib.sha256(coil_run.read_bytes()).hexdigest())
        coil_data = load(coil_run)
        self.assertIsNone(coil_data["failure"])
        self.assertEqual(40, len(coil_data["snapshots"]))
        scenario = ROOT / "tools/harness-scenarios/stern" / f"{NAME}-coil-sweep.json"
        self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), coil_data["scenario"]["sha256"])
        self.assertEqual("ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d", coil_data["library_sha256"])

    @unittest.skipUnless(os.environ.get("PINMAME_SOURCE_ROOT") and os.environ.get("PINMAME_SCRIPTS_ROOT"), "pinned managed source roots not configured")
    def test_exact_managed_sources(self) -> None:
        checkout = Path(os.environ["PINMAME_SOURCE_ROOT"])
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(self.seed["pinmame_revision"], revision)
        script = Path(os.environ["PINMAME_SCRIPTS_ROOT"]) / "World Poker Tour (Stern 2006) v.2.3.1.vbs"
        source = next(s for s in self.definition["sources"] if s["id"] == "vpx.script.wpt-known-working")
        self.assertEqual(source["sha256"], hashlib.sha256(script.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
