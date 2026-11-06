"""Reconcile Embryon's modeled bulb sockets with the retained table export."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_external_evidence_manifest import check_manifest

SEED = ROOT / "tools/seeds/bally/embryon-1981-bulbs.json"


def world_bounds(path: Path, names: set[str]) -> dict:
    result = {}
    name = None
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("o "):
                name = line[2:].strip()
            elif name in names and line.startswith("v "):
                point = [float(v) for v in line.split()[1:4]]
                if name not in result:
                    result[name] = [point[:], point[:]]
                else:
                    for i, value in enumerate(point):
                        result[name][0][i] = min(result[name][0][i], value)
                        result[name][1][i] = max(result[name][1][i], value)
    return result


class EmbryonBulbTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"),
                         "optional VPX evidence root not configured")
    def test_retained_meshes_and_script_bindings(self):
        seed = json.loads(SEED.read_text(encoding="utf-8"))
        root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally/embryon-1981/unclepaulie-2.0.2"
        table = root / "download/Embryon (Bally 1981) w VR Room v2.0.2.vpx"
        script = root / "extraction/script.vbs"
        obj = root / "world-obj/Embryon (Bally 1981) w VR Room v2.0.2.obj"
        for path, key in [(table, "vpx_sha256"), (script, "script_sha256"), (obj, "obj_sha256")]:
            self.assertEqual(seed[key], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(seed["manifest_sha256"], check_manifest(root / "extraction", "embryond"))
        names = {r["object"] for r in seed["bulbs"]}
        actual = world_bounds(obj, names)
        self.assertEqual(names, set(actual))
        lines = script.read_text(encoding="cp1252").splitlines()
        for row in seed["bulbs"]:
            self.assertEqual(row["bounds"], actual[row["object"]], row["object"])
            if "callback_line" in row:
                line = lines[row["callback_line"] - 1]
                self.assertIn(f'Lampz.Callback({row["output"]})', line)
                self.assertIn(f'DisableLighting2 {row["object"]},', line)
            elif row["object"].startswith("bumperbulb"):
                nr = int(row["object"].removeprefix("bumperbulb"))
                self.assertTrue(any(f'Lampz.Callback({row["output"]})' in l and f'bumperbulb{nr}flash' in l for l in lines))
                self.assertIn(f"\tFlBumperFadeTarget({nr}) = aLvl*bumperflashlevel", lines)
            else:
                self.assertEqual(87, row["output"])
                collections = json.loads((root / "extraction/collections.json").read_text(encoding="utf-8"))
                members = next(c["items"] for c in collections if c["name"] == "GIMidLane")
                self.assertIn(row["control_light"], members)
                self.assertTrue(any('Lampz.Callback(87)' in l and 'TopMidLaneLights' in l for l in lines))
                light = json.loads((root / f"extraction/gameitems/Light.{row['control_light']}.json").read_text(encoding="utf-8"))["Light"]["center"]
                center = [(a + b) / 2 for a, b in zip(*row["bounds"])]
                self.assertLess(((center[0] - light["x"]) ** 2 + (center[1] - light["y"]) ** 2) ** .5, 2)
        text = "\n".join(lines)
        for fragment in ('Eval("bumperbulb" & nr)', 'FlBumperFadeActual(nr)', 'FlBumperBulb(nr).BlendDisableLighting'):
            self.assertIn(fragment, text)
        # Independently positioned rendering lights check the baked mesh's XY frame.
        for name in ("bulb1", "bulb119"):
            row = next(r for r in seed["bulbs"] if r["object"] == name)
            light = json.loads((root / f"extraction/gameitems/Light.l{row['output']}.json").read_text(encoding="utf-8"))["Light"]["center"]
            center = [(a + b) / 2 for a, b in zip(*row["bounds"])]
            self.assertLess(((center[0] - light["x"]) ** 2 + (center[1] - light["y"]) ** 2) ** .5, 2)


if __name__ == "__main__":
    unittest.main()
