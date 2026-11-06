"""Independent checks for Grand Lizard's retained spatial evidence."""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from grand_lizard_spatial import SEED, _affine, _outside, verify_spatial


class GrandLizardSpatialTest(unittest.TestCase):
    def test_control_fit_and_hull(self) -> None:
        controls = [
            {"pixel": [0, 0], "vpu": [10, 20]},
            {"pixel": [1, 0], "vpu": [12, 19]},
            {"pixel": [0, 1], "vpu": [13, 24]},
            {"pixel": [1, 1], "vpu": [15, 23]},
        ]
        fit = _affine(controls)
        for actual, expected in zip(fit, [[2, 3, 10], [-1, 4, 20]]):
            for a, b in zip(actual, expected):
                self.assertAlmostEqual(a, b)
        # The hull helper expects controls in LL, LR, UL, UR order.
        ordered = [controls[i] for i in (0, 1, 2, 3)]
        self.assertFalse(_outside([0.5, 0.5], ordered))
        self.assertTrue(_outside([1.5, 0.5], ordered))
        for c in controls:
            c["pixel"] = [0, 0]
        with self.assertRaisesRegex(ValueError, "degenerate"):
            _affine(controls)

    def test_expected_placements_are_addressed_and_extrapolation_is_disclosed(self) -> None:
        data = json.loads((ROOT / SEED).read_text(encoding="utf-8"))
        devices = data["devices"]
        self.assertEqual(
            {key for key in devices if key.startswith("lamp.matrix-")},
            {f"lamp.matrix-{n}" for n in range(7, 65) if n != 51},
        )
        self.assertEqual({key for key in devices if key.startswith("solenoid.")}, {f"solenoid.{n}" for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 17, 18)})
        self.assertEqual(len(devices["solenoid.6"]["spatial"]["placements"]), 2)
        self.assertEqual(len(devices["solenoid.7"]["spatial"]["placements"]), 1)
        self.assertNotIn("solenoid.13", devices)
        self.assertNotIn("solenoid.19", devices)
        for group in ("manual49", "manual50"):
            for row in data["report"][group]["placements"]:
                if row["extrapolated"]:
                    self.assertIn("outside the convex hull", devices[row["device_id"]]["physical_notes"])
        for n in range(42, 48):
            refs = devices[f"lamp.matrix-{n}"]["spatial"]["placements"][0]["provenance"]["source_refs"]
            self.assertIn("runtime.grand-lizard.l4-service-and-gameplay", refs)

    @unittest.skipUnless(all(os.environ.get(x) for x in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")), "external evidence roots not configured")
    def test_retained_sources_and_mutation_guards(self) -> None:
        vpx, manuals, review = (Path(os.environ[x]) for x in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"))
        verify_spatial(ROOT, vpx, manuals, review)
        original = json.loads((ROOT / SEED).read_text(encoding="utf-8"))

        def mutate_raw(data: dict) -> None:
            data["report"]["observations"][0]["raw_x"] += 1

        def mutate_affine(data: dict) -> None:
            data["report"]["manual49"]["pixel_to_vpu_affine_rows"][0][0] += 0.01

        def mutate_hull(data: dict) -> None:
            row = data["report"]["manual50"]["placements"][0]
            row["extrapolated"] = not row["extrapolated"]

        def mutate_mesh(data: dict) -> None:
            data["report"]["target_meshes"]["meshes"]["TargetM_7"]["bounds_min"][0] += 1

        def mutate_source(data: dict) -> None:
            data["report"]["observations"][0]["sha256"] = "0" * 64

        for mutation, message in ((mutate_raw, "raw geometry"), (mutate_affine, "affine fit"), (mutate_hull, "hull"), (mutate_mesh, "mesh bounds"), (mutate_source, "source digest")):
            with self.subTest(mutation=mutation.__name__), tempfile.TemporaryDirectory() as tmp:
                scratch = Path(tmp)
                seed_path = scratch / SEED
                seed_path.parent.mkdir(parents=True)
                data = copy.deepcopy(original)
                mutation(data)
                seed_path.write_text(json.dumps(data), encoding="utf-8")
                for name in ("manual49", "manual50"):
                    image = Path(data["report"][name]["excerpt"]["image"])
                    (scratch / image).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / image, scratch / image)
                with self.assertRaisesRegex(ValueError, message):
                    verify_spatial(scratch, vpx, manuals, review)


if __name__ == "__main__":
    unittest.main()
