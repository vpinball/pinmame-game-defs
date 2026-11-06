from __future__ import annotations

import hashlib
import copy
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.validation import validate_machine
import curate_transporter_the_rescue as curator


@contextmanager
def scratch_root():
    # A managed worktree is directly beneath the working root's worktrees directory.
    base = (curator.ROOT.parent.parent if curator.ROOT.parent.name == "worktrees"
            else curator.ROOT.parent / "pinmame-game-defs-working-dir")
    created = not base.exists()
    base.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="transporter-test-", dir=base) as directory:
            yield Path(directory)
    finally:
        if created:
            base.rmdir()


def table_rows(name):
    path = curator.ROOT / "evidence/excerpts" / curator.ID / f"{name}.md"
    return [[cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("|")]


def transcribed_matrix(rows):
    body = [row for row in rows if len(row) == 9 and re.fullmatch(r"[1-8]", row[0])]
    cells = []
    for row in body:
        for col, text in enumerate(row[1:], 1):
            match = re.fullmatch(r"(\d+) (.+)", text)
            if not match:
                raise ValueError(f"invalid printed matrix cell: {text!r}")
            cells.append({"printed_address": int(match[1]), "public_address": None,
                          "row": int(row[0]), "column": col, "literal_label": match[2]})
    return cells


class TransporterDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = curator.build()
        cls.inputs = {x["binding"]["device"]: x for x in cls.definition["inputs"]
                      if x["binding"]["group"] == "pinmame.input.switch"}
        cls.coils = {x["binding"]["device"]: x for x in cls.definition["outputs"]
                     if x["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {x["binding"]["device"]: x for x in cls.definition["outputs"]
                     if x["binding"]["group"] == "pinmame.output.lamp"}

    def test_exact_address_sets_and_schema(self):
        self.assertEqual(set(self.inputs), set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)))
        self.assertEqual(set(self.coils), set(range(1, 51)))
        self.assertEqual(set(self.lamps), set(range(1, 65)))
        self.assertEqual([], validate_machine(self.definition, curator.ROOT))
        self.assertEqual(self.definition["coverage"]["missing"], ["polarity", "spatial_placement"])
        self.assertEqual(self.definition["coverage"]["dimensions"]["polarity"], "unknown")
        self.assertEqual(self.definition["knowledge"]["status"], "partial")
        self.assertEqual(self.definition["machine"]["model_number"], "2008")
        self.assertEqual(self.definition["machine"]["playfield"], {"width": 952.965, "height": 1976.52, "units": "vpx"})

    def test_machine_routing_and_fitment(self):
        self.assertEqual(self.inputs[2]["id"], "switch.ac-select-feedback")
        self.assertEqual(self.inputs[2]["kind"], "virtual")
        self.assertEqual(self.inputs[5]["availability"], "optional")
        self.assertEqual(self.inputs[57]["id"], "switch.right-flipper-lane-change")
        self.assertEqual(self.inputs[58]["id"], "switch.left-flipper-lane-change")
        self.assertFalse(self.inputs[19]["normally_closed"])
        self.assertEqual(self.inputs[19]["physical"]["switch_type"], "opto")
        for n in (13, 24, *range(33, 45), 49, 50):
            self.assertEqual(self.coils[n]["availability"], "unused")
        for n in (23, 45, 46, 47, 48):
            self.assertEqual((self.coils[n]["kind"], self.coils[n]["availability"]), ("virtual", "used"))
        self.assertEqual(self.coils[34]["id"], "device.unused-solenoid-34")
        self.assertEqual(self.coils[36]["id"], "device.unused-solenoid-36")
        self.assertEqual(self.coils[27]["physical"]["quantity"], 2)
        self.assertEqual(self.coils[28]["physical"]["quantity"], 2)
        self.assertEqual(len(self.coils[9]["spatial"]["placements"]), 33)
        self.assertNotIn("quantity", self.coils[9]["physical"])
        self.assertEqual({n for n, x in self.lamps.items() if x["availability"] == "unused"}, {18, 56})
        self.assertEqual({n for n, x in self.lamps.items() if x["physical"].get("quantity") == 2}, {13, 14, 40, 55})
        self.assertEqual(self.coils[6]["physical"]["part_number"], "AE-26-1200")
        self.assertEqual(self.coils[10]["physical"]["part_number"], "SM2-35-4000-DC")
        for n in (57, 58):
            self.assertEqual(self.inputs[n]["spatial"]["reason"], "cabinet_or_service")

    def test_aliases_retained_at_original_binding(self):
        facts = json.loads((curator.ROOT / curator.FACTS).read_text(encoding="utf-8"))
        actual = {**{("inputs", x["binding"]["group"], x["binding"]["device"]): x for x in self.definition["inputs"]},
                  **{("outputs", x["binding"]["group"], x["binding"]["device"]): x for x in self.definition["outputs"]}}
        for section in ("inputs", "outputs"):
            for old in facts["legacy"][section]:
                key = (section, old["binding"]["group"], old["binding"]["device"])
                if key not in actual and key[1] == "pinmame.output.lamp" and key[2] in (107, 109):
                    continue
                self.assertIn(key, actual)
                for alias in old["aliases"]:
                    self.assertIn(alias, actual[key]["aliases"])

    def test_gi_polarity_and_shared_right_flipper_behavior(self):
        self.assertIn("Enabled output 9 turns the playfield GI off", self.coils[9]["physical"]["notes"])
        self.assertIn("polarity is unestablished", self.coils[22]["physical"]["notes"])
        self.assertIn("both the lower-right and upper-right", self.inputs[82]["physical"]["notes"])
        self.assertIn(curator.MANUAL, self.inputs[82]["provenance"]["source_refs"])
        mechanism = next(x for x in self.definition["mechanisms"] if x["id"] == "mechanism.flippers")
        self.assertIn("drives both lower-right and upper-right", mechanism["behavior"])
        knowledge = curator.knowledge_text()
        self.assertIn("enabled output 9 turns GI off", knowledge)
        self.assertIn("Output 22's lamp-on/off polarity remains unestablished", knowledge)
        self.assertIn("right cabinet button (input 82) drives both", knowledge)

    def test_jet_control_checks_exclude_the_checked_object(self):
        seed = json.loads((curator.ROOT / curator.CALLOUT_PATH).read_text(encoding="utf-8"))
        checks = curator.report(self.definition)["callout_check"]["placements"]
        for address in (60, 61, 62):
            placement = self.inputs[address]["spatial"]["placements"][0]
            check = checks[placement["id"]]
            table_object = curator.SWITCH_OBJECTS[address]
            controls = [c for c in seed["pages"][check["page"]]["controls"]
                        if c["table_object"] != table_object]
            self.assertEqual(check["control_object_excluded"], table_object)
            self.assertEqual(check["control_count"], 4)
            transform = curator.drawing_callouts.fit([(tuple(c["pixel"]), tuple(c["xy"])) for c in controls])
            offset = curator.drawing_callouts.distance(curator.drawing_callouts.apply(transform, check["pixel"]),
                                                      (placement["x"], placement["y"]))
            self.assertEqual(check["independent_control_fit"], transform)
            self.assertEqual(check["control_offset"], round(offset, 4))
            self.assertLess(offset, 0.07)
            self.assertTrue(check["agrees"])

    def test_runtime_service_evidence(self):
        path = curator.ROOT / curator.RUNTIME_PATH
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), curator.RUNTIME_SHA)
        evidence = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["runtime"]["emulator"]["built_from_revision"], curator.REVISION)
        runs = evidence["runtime"]["observations"]["runs"]
        for name in ("levels", "edges"):
            observations = runs[name]["named_action_observations"]
            for n in (1, 19, 20, 21, 22, 23, 24):
                for level in (0, 1):
                    row = next(x for x in observations if x["label"] == f"{name} switch {n} level {level}")
                    text = row["display_responses"][0]["interpreted_text"]
                    if level == 0:
                        self.assertIn("SWITCH", text)
                    else:
                        self.assertNotIn("SWITCH", text)
        coil_rows = runs["coil-repeat"]["named_action_observations"]
        for n in (13, 17, 18, 19, 20, 21, 22):
            matches = [x for x in coil_rows if n in x["transitioned_solenoid_addresses"]]
            self.assertGreaterEqual(len(matches), 3)
            if n == 13:
                self.assertTrue(all("NOT USED" in x["display_responses"][0]["interpreted_text"] for x in matches))

    def test_drift_and_missing_runtime_fail_closed(self):
        self.assertEqual((curator.ROOT / curator.DEFINITION).read_bytes(), (curator.ROOT / curator.SEED).read_bytes())
        self.assertEqual((curator.ROOT / curator.DEFINITION).read_bytes(), curator.canonical_bytes(self.definition))
        with patch.object(curator, "RUNTIME_SHA", "0" * 64), self.assertRaisesRegex(ValueError, "runtime evidence"):
            curator.build()
        with patch.object(curator, "LAMP_RUNTIME_SHA", "0" * 64), self.assertRaisesRegex(ValueError, "lamp evidence"):
            curator.build()

    def test_fact_tables_match_all_excerpt_rows(self):
        facts = json.loads((curator.ROOT / curator.FACTS).read_text(encoding="utf-8"))
        lamp, switch = table_rows("lamp-matrix"), table_rows("switch-matrix")
        expected = {
            "lamp_cells": transcribed_matrix(lamp),
            "lamp_wiring": [row for row in lamp if len(row) in (4, 5)],
            "switch_cells": transcribed_matrix(switch),
            "switch_wiring": [row for row in switch if len(row) in (3, 5)],
            "switch_parts": [row for row in table_rows("switch-parts") if re.match(r"^\d", row[0])],
            "solenoid_rows": [row for row in table_rows("solenoid-table")
                              if re.match(r"^\d", row[0]) or row[0] == "[blank]"],
            "solenoid_parts": [row for row in table_rows("solenoid-parts")
                               if re.match(r"^\d", row[0]) or row[0] == "-"],
        }
        for key, rows in expected.items():
            with self.subTest(table=key):
                self.assertEqual(facts[key], rows)

    def test_regenerate_refuses_existing_author_ready_without_writes(self):
        with scratch_root() as root:
            author, partial = root / curator.AUTHOR, root / curator.DEFINITION
            author.parent.mkdir(parents=True)
            partial.parent.mkdir(parents=True)
            author.write_bytes(b"existing author-ready artifact\n")
            partial.write_bytes(b"existing partial artifact\n")
            with patch.object(curator, "ROOT", root), patch.object(sys, "argv", ["curator", "--regenerate"]), \
                    patch.object(curator, "artifacts") as generated:
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.main()
                generated.assert_not_called()
            self.assertEqual(author.read_bytes(), b"existing author-ready artifact\n")
            self.assertEqual(partial.read_bytes(), b"existing partial artifact\n")

    def test_check_refuses_modified_generated_content_in_custom_root(self):
        with scratch_root() as root:
            target = root / curator.DEFINITION
            target.parent.mkdir(parents=True)
            target.write_bytes(b"modified\n")
            with patch.object(curator, "ROOT", root), patch.object(sys, "argv", ["curator", "--check"]), \
                    patch.object(curator, "artifacts", return_value={curator.DEFINITION: b"expected\n"}) as generated:
                with self.assertRaisesRegex(ValueError, "generated artifact drift"):
                    curator.main()
                generated.assert_called_once_with(root)
            self.assertEqual(target.read_bytes(), b"modified\n")

    def test_report_uses_supplied_root_for_drawing_and_photo(self):
        with scratch_root() as root:
            for relative in (curator.CALLOUT_PATH, curator.PHOTO_PATH):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((curator.ROOT / relative).read_bytes())
            photo_path = root / curator.PHOTO_PATH
            photo = json.loads(photo_path.read_text(encoding="utf-8"))
            photo["limitations"] = "custom-root regression sentinel"
            photo["candidate_socket_observations"][0]["pixel"][0] += 100
            photo_path.write_text(json.dumps(photo), encoding="utf-8")
            definition = copy.deepcopy(self.definition)
            original = copy.deepcopy(definition)
            result = curator.report(definition, root=root)
            self.assertEqual(definition, original)
            self.assertEqual(result["callout_check"]["photo_sockets"]["limitations"], photo["limitations"])
            self.assertEqual(result["callout_check"]["photo_sockets"]["seed_sha256"],
                             hashlib.sha256(photo_path.read_bytes()).hexdigest())
            target = photo["candidate_socket_observations"][0]["public_lamp"]
            old = next(x for x in original["outputs"] if x["binding"] == {
                "group": "pinmame.output.lamp", "device": target})["spatial"]["placements"][0]
            reported = next(x for x in result["placements"] if x["id"] == old["id"])
            self.assertNotEqual((reported["x"], reported["y"]), (old["x"], old["y"]))

    def test_artifacts_passes_custom_root_to_report(self):
        with scratch_root() as root:
            marker_definition, marker_report = {}, {"marker": "custom-root"}
            with patch.object(curator, "build", return_value=marker_definition), \
                    patch.object(curator, "report", return_value=marker_report) as make_report, \
                    patch.object(curator, "report_text", return_value="report\n"):
                curator.artifacts(root)
            args, kwargs = make_report.call_args
            self.assertEqual(args[0], marker_definition)
            self.assertEqual(kwargs.get("root", args[1] if len(args) > 1 else None), root)

    def test_verify_extraction_uses_supplied_facts_root(self):
        with scratch_root() as root:
            source_root, facts_root = root / "external", root / "custom-facts"
            extraction = source_root / curator.EXTRACTION_PATH
            (extraction / "gameitems").mkdir(parents=True)
            gameitem = {"Test": {"center": {"x": 10, "y": 20}}}
            (extraction / "gameitems" / "test.json").write_text(json.dumps(gameitem), encoding="utf-8")
            for relative, data in ((curator.FACTS, {"objects": {"test": {"file": "test.json", "x": 10, "y": 20}}}),
                                   (curator.SPATIAL_FACTS, {"objects": {}})):
                target = facts_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(data), encoding="utf-8")
            manifest = curator.manifest_bytes(curator.build_manifest(extraction, "tsptr_l3")) + b"\n"
            digest = hashlib.sha256(manifest).hexdigest()
            (extraction / "manifest.json").write_bytes(manifest)
            (extraction / "manifest.sha256").write_text(digest + "\n", encoding="ascii")
            with patch.object(curator, "MANIFEST_SHA", digest):
                curator.verify_extraction(source_root, root=facts_root)
                altered = json.loads((facts_root / curator.FACTS).read_text(encoding="utf-8"))
                altered["objects"]["test"]["x"] = 11
                (facts_root / curator.FACTS).write_text(json.dumps(altered), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "coordinate drift: test"):
                    curator.verify_extraction(source_root, root=facts_root)

    def test_family_mechanisms_and_public_flipper_contract(self):
        self.assertEqual({x["id"] for x in self.definition["drivers"]},
                         {"tsptr_l1", "tsptr_l3", "tsptr_lu3", "tsptr_l3fj", "tsptr_lx4", "tsptr_lx4b"})
        self.assertEqual({x["physical_compatibility"] for x in self.definition["drivers"]}, {"identical"})
        mechanisms = {x["id"]: x for x in self.definition["mechanisms"]}
        self.assertEqual(set(mechanisms), {"mechanism." + x for x in (
            "trough", "left-drop-bank", "middle-drop-bank", "left-lock", "right-lock", "ball-popper",
            "top-flipper-gate", "left-outlane-kicker", "flippers", "jet-bumpers", "slingshots", "transport-ramp-path")})
        self.assertEqual(mechanisms["mechanism.flippers"]["actuators"], [])
        self.assertIn("three", curator.knowledge_text())
        self.assertEqual(self.inputs[3]["roles"], ["cabinet.start"])
        for address in (19, 20, 21, 22, 23, 24):
            self.assertFalse(self.inputs[address]["normally_closed"])

    def test_physical_spatial_limits_remain_explicit(self):
        for address in (63, 64):
            self.assertEqual(self.inputs[address]["physical"]["quantity"], 2)
            self.assertEqual(len(self.inputs[address]["spatial"]["placements"]), 2)
            self.assertEqual(self.inputs[address]["spatial"]["status"], "observed")
        for address in (11, 12, 13):
            self.assertTrue(self.inputs[address]["initial_active"])
        self.assertEqual({n for n, x in self.coils.items() if "spatial" not in x}, {29, 30, 31})
        for address in set(range(1, 41)) - {18}:
            self.assertEqual(self.lamps[address]["spatial"]["status"], "observed" if address in (1, 4, 5, 6, 7, 8) else "candidate")
        for address in (13, 14, 40):
            self.assertEqual(len(self.lamps[address]["spatial"]["placements"]), 2)
        self.assertNotIn(107, self.lamps)
        self.assertNotIn(109, self.lamps)
        for p in self.coils[27]["spatial"]["placements"]:
            self.assertEqual(p["y"], 0)
        report = curator.report(self.definition)
        self.assertEqual(report["format"], "pinmame-spatial-blockers")
        checked = report["callout_check"]["placements"]
        self.assertEqual(len(checked), 14)
        self.assertTrue(all(x["agrees"] for x in checked.values()))
        self.assertIn(curator.CALLOUT_SOURCE, self.inputs[15]["spatial"]["placements"][0]["provenance"]["source_refs"])
        self.assertEqual(report["extraction_file_count"], 2104)

    @unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
    def test_original_manual_and_bulletin_bytes(self):
        base = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.ID
        for name, expected in (
            ("Bally_1989_Transporter_the_Rescue_English_Manual.pdf", "d1e29962c3bc53733ba61a62d8d814d2a1adbf508f78dfe10c01cd4fb95f2ce9"),
            ("Bally_1989_Transporter_the_Rescue_Service_Bulletin_Book_1989_includes_Transporter_SB11_SB13.pdf", "c12614faa3efee725c0c6ff0e586087987eead49fa024fe1107e61654ea1599c"),
        ):
            self.assertEqual(hashlib.sha256((base / name).read_bytes()).hexdigest(), expected)

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained drawing/library root not configured")
    def test_drawing_and_library_bytes(self):
        base = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        seed = json.loads((curator.ROOT / curator.CALLOUT_PATH).read_text(encoding="utf-8"))
        for page in seed["pages"].values():
            image = page["image"]
            self.assertEqual(hashlib.sha256((base / image["path"]).read_bytes()).hexdigest(), image["sha256"])
        for name, digest in (("s11.vbs", curator.VPM_S11_SHA256), ("core.vbs", curator.VPM_CORE_SHA256)):
            self.assertEqual(hashlib.sha256((base / "vpm-script-libs" / name).read_bytes()).hexdigest(), digest)
        photo = json.loads((curator.ROOT / curator.PHOTO_PATH).read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256((base / photo["source"]["path"]).read_bytes()).hexdigest(), photo["source"]["sha256"])
        self.assertEqual(photo["control_uncertainty_pixels"], 25)
        for row in photo["candidate_socket_observations"]:
            p = self.lamps[row["public_lamp"]]["spatial"]["placements"][0]
            self.assertEqual([p["x"], p["y"]], row["normalized"])

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained extraction root not configured")
    def test_full_external_extraction_manifest(self):
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
        curator.verify_extraction(base)
        table = base / "bally/transporter-the-rescue-1989/Transporter the Rescue (Midway 1989) VPW v1.05.vpx"
        self.assertEqual(hashlib.sha256(table.read_bytes()).hexdigest(), "4cd27942999d39e6f1e23e6a2d65f24b61dc176f7eb5ede9c720a981c05718ff")
        script = base / curator.EXTRACTION_PATH / "script.vbs"
        self.assertEqual(hashlib.sha256(script.read_bytes()).hexdigest(), "ac708574ef0cdd488f1ff4c63da2888d622e609fcf88b818448fd03a214756de")
        active = "\n".join(x for x in script.read_text(encoding="cp1252").splitlines() if not x.lstrip().startswith("'"))
        self.assertEqual({int(x) for x in re.findall(r"(?im)^SolCallback\((\d+)\)", active)},
                         {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 25, 26, 27, 28, 29, 30, 31, 32})


if __name__ == "__main__":
    unittest.main()
