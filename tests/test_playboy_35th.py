from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
sys.path.insert(0,str(ROOT/"tools"))

DEFINITION_PATH = ROOT/"machines/partial/data-east/playboy-35th-anniversary-1989.json"
SEED_PATH = ROOT/"tools/seeds/data-east/playboy-35th-anniversary-1989.json"
MANIFEST_PATH = ROOT/"tools/seeds/data-east/playboy-35th-anniversary-1989-extraction-manifest.json"
KNOWLEDGE_PATH = ROOT/"knowledge/data-east/playboy-35th-anniversary-1989.md"
SPATIAL_JSON_PATH = ROOT/"reports/spatial/data-east/playboy-35th-anniversary-1989.json"
SPATIAL_MD_PATH = ROOT/"reports/spatial/data-east/playboy-35th-anniversary-1989.md"
EXCERPT_DIR = ROOT/"evidence/excerpts/data-east.playboy-35th-anniversary.1989"
MANUAL_NAME = "Data_East_1989_Playboy_35th_Anniversary_English_Manual_with_schematics.pdf"
TABLE_NAME = "Playboy 35th Anniversary (Data East 1989) Physics Sound Hybrid MOD 1.1.vpx"
BACKBOX_LAMPS = {26,32,57,58,59,60,61,62,63}
MANUAL_UNLOCATED_PINBALL_LAMPS = {41,49,53,54,55,56,64}
UNUSED_SWITCHES = {2,8,9,40,44,*range(52,65)}
VPX_EVIDENCE_ROOT = os.environ.get("PINMAME_PLAYBOY_VPX_SOURCES_ROOT") or os.environ.get("PINMAME_VPX_SOURCES_ROOT")
MANUAL_EVIDENCE_ROOT = os.environ.get("PINMAME_PLAYBOY_MANUALS_ROOT") or os.environ.get("PINMAME_MANUALS_ROOT")


def load_json(path: Path) -> dict[str,object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return digest.hexdigest()


def bindings(definition: dict[str,object], collection: str, group: str) -> dict[int,dict[str,object]]:
    return {item["binding"]["device"]:item for item in definition[collection] if item["binding"]["group"] == group}


class PlayboyDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.switches = bindings(cls.definition,"inputs","pinmame.input.switch")
        cls.dips = bindings(cls.definition,"inputs","pinmame.input.dip")
        cls.solenoids = bindings(cls.definition,"outputs","pinmame.output.solenoid")
        cls.lamps = bindings(cls.definition,"outputs","pinmame.output.lamp")

    def test_identity_bounds_and_partial_blockers_are_exact(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual("data-east.playboy-35th-anniversary.1989",machine["id"])
        self.assertEqual("Playboy 35th Anniversary",machine["name"])
        self.assertEqual("Data East",machine["manufacturer"])
        self.assertEqual(1989,machine["year"])
        playfield = machine["playfield"]
        self.assertEqual(952.0,playfield["width"])
        self.assertEqual(1974.0,playfield["height"])
        self.assertEqual("vpx",playfield["units"])
        coverage = self.definition["coverage"]
        self.assertEqual("partial",coverage["status"])
        self.assertEqual(
            {"controller_platform","output_semantics","mechanism_behavior","polarity","spatial_placement","unresolved_conflicts"},
            set(coverage["missing"]),
        )

    def test_single_driver_case_is_explicit_and_catalog_claims_it_once(self) -> None:
        drivers = self.definition["drivers"]
        self.assertEqual(["play_a24"],[driver["id"] for driver in drivers])
        self.assertNotIn("clone_of",drivers[0])
        self.assertIn("single-driver coverage is deliberate",drivers[0]["variant_notes"])
        catalog = load_json(ROOT/"catalog/pinmame.json")
        rows = [row for row in catalog["drivers"] if row["id"] == "play_a24"]
        self.assertEqual(1,len(rows))
        self.assertEqual("data-east.playboy-35th-anniversary.1989",rows[0]["machine_id"])
        self.assertEqual(DEFINITION_PATH.relative_to(ROOT).as_posix(),rows[0]["definition"])
        self.assertFalse((ROOT/"machines/stubs/play_a24.json").exists())
        self.assertFalse((ROOT/"knowledge/stubs/play_a24.md").exists())

    def test_controller_contract_and_mux_delay_are_recorded(self) -> None:
        self.assertEqual(
            {"platform":"pinmame.dataeast","hardware_generation":"0x1000","inversion_applied_by_emulator":False},
            self.definition["controller"],
        )
        source = next(item for item in self.definition["sources"] if item["kind"] == "pinmame_core")
        for fragment in ("core_tGameData","wpc.invSw zero-initialized","core.c lines 2455-2456","one-IRQ mux delay","pia0b_w/updsol","lines 1145-1149","lines 714-715","737-738","746-747","SP6, SP5, SP2, SP3, SP1, and SP4"):
            self.assertIn(fragment,source["locator"])
        self.assertEqual("BSD-3-Clause",source["license"])
        note = self.solenoids[25]["physical"]["notes"]
        self.assertIn("one IRQ",note)
        self.assertIn("must not add another delay",note)
        relationships = self.definition["relationships"]
        self.assertEqual(set(range(25,33)),{int(row["destination"].rsplit("-",1)[1]) for row in relationships})
        self.assertTrue(all(row["source"] == "coil.driver-10" for row in relationships))

    def test_full_input_space_and_printed_unused_cells_are_enumerated(self) -> None:
        self.assertEqual({-7,-6}|set(range(1,65)),set(self.switches))
        self.assertEqual({0},set(self.dips))
        for address in range(1,65):
            expected = "unused" if address in UNUSED_SWITCHES else "used"
            self.assertEqual(expected,self.switches[address]["availability"],address)
        self.assertEqual("Center 3 Bank Middle",self.switches[42]["label"])
        self.assertEqual("Grotto 2",self.switches[31]["label"])
        self.assertEqual("Drop2 Center",self.switches[50]["label"])

    def test_switch_matrix_wires_follow_column_and_row(self) -> None:
        drives = ["GRN-BRN","GRN-RED","GRN-ORN","GRN-YEL","GRN-BLK","GRN-BLU","GRN-VIO","GRN-GRY"]
        returns = ["WHT-BRN","WHT-RED","WHT-ORN","WHT-YEL","WHT-GRN","WHT-BLU","WHT-VIO","WHT-GRY"]
        for address in (5,18,24,34,39,42,59):
            column,row = divmod(address-1,8)
            self.assertEqual(drives[column],self.switches[address]["wiring"]["drive_wire"])
            self.assertEqual(returns[row],self.switches[address]["wiring"]["return_wire"])

    def test_flipper_addresses_preserve_the_eos_button_conflict(self) -> None:
        for address,side in ((15,"left"),(16,"right")):
            switch = self.switches[address]
            self.assertEqual(f"flipper.lower.{side}.button",switch["roles"][0])
            self.assertEqual("conflicted",switch["provenance"]["status"])
            self.assertIn("physical EOS",switch["physical"]["notes"])
            self.assertEqual("cabinet_or_service",switch["spatial"]["reason"])
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("PinMAME public-address behavior",knowledge)
        self.assertNotIn("preceding Data East machines",knowledge)

    def test_laser_kick_uses_the_executable_in_bounds_binding(self) -> None:
        switch = self.switches[17]
        self.assertEqual("candidate",switch["spatial"]["status"])
        placement = switch["spatial"]["placements"][0]
        self.assertAlmostEqual(53.316788/952.0,placement["x"],places=6)
        self.assertAlmostEqual(1590.0859/1974.0,placement["y"],places=6)
        self.assertIn("Kicker001_Hit",switch["physical"]["notes"])

    def test_all_lamps_exist_and_the_55_name_gap_is_explained(self) -> None:
        self.assertEqual(set(range(1,65)),set(self.lamps))
        self.assertEqual("Miss September Lites Out-lane 50k",self.lamps[11]["label"])
        self.assertEqual("Drop Target 50k",self.lamps[46]["label"])
        self.assertEqual('pinb"A"ll',self.lamps[55]["label"])
        for address in BACKBOX_LAMPS:
            self.assertEqual("not_applicable",self.lamps[address]["spatial"]["status"],address)
            self.assertEqual("cabinet_or_service",self.lamps[address]["spatial"]["reason"],address)
            self.assertIn("nine addresses with no numeric Light object",self.lamps[address]["physical"]["notes"],address)
        for address in MANUAL_UNLOCATED_PINBALL_LAMPS:
            self.assertNotIn("spatial",self.lamps[address],address)
            self.assertEqual("candidate",self.lamps[address]["provenance"]["status"],address)
            self.assertIn("manual location drawing does not show",self.lamps[address]["physical"]["notes"],address)

    def test_lamp_wires_follow_column_and_row(self) -> None:
        drives = ["YEL-BRN","YEL-RED","YEL-ORN","YEL-BLK","YEL-GRN","YEL-BLU","YEL-VIO","YEL-GRY"]
        returns = ["RED-BRN","RED-BLK","RED-ORN","RED-YEL","RED-GRN","RED-BLU","RED-VIO","RED-GRY"]
        for address in (4,18,24,46,51,54,55,61):
            column,row = divmod(address-1,8)
            self.assertEqual(drives[column],self.lamps[address]["wiring"]["drive_wire"])
            self.assertEqual(returns[row],self.lamps[address]["wiring"]["return_wire"])

    def test_full_solenoid_space_and_playboy_typing_are_enumerated(self) -> None:
        self.assertEqual(set(range(1,51)),set(self.solenoids))
        self.assertEqual("flasher",self.solenoids[9]["kind"])
        self.assertEqual("relay",self.solenoids[10]["kind"])
        self.assertEqual("gi",self.solenoids[11]["kind"])
        for address in range(12,16):
            self.assertEqual("flasher",self.solenoids[address]["kind"],address)
        expected = {25:"Outhole",26:"Trough Eject",27:"Vertical Up Kicker",28:"Champagne Kicker",29:"Drop Target Reset",30:"Grotto Kicking",31:"Unfitted Mux Branch R07",32:"Knocker"}
        for address,label in expected.items():
            self.assertEqual(label,self.solenoids[address]["label"])
            self.assertEqual("conflicted",self.solenoids[address]["provenance"]["status"])
        self.assertEqual("unknown",self.solenoids[31]["availability"])
        self.assertNotIn("quantity",self.solenoids[31]["physical"])
        self.assertEqual(("not_applicable","virtual"),(self.solenoids[31]["spatial"]["status"],self.solenoids[31]["spatial"]["reason"]))
        self.assertIn("only a ROM or runtime trace can establish",self.solenoids[31]["physical"]["notes"])
        self.assertEqual(4,self.solenoids[9]["physical"]["quantity"])
        self.assertEqual(5,self.solenoids[13]["physical"]["quantity"])
        self.assertIn("not additive",self.solenoids[9]["physical"]["notes"])
        expected_backbox = {3:3,4:3,8:2,9:2,12:4,14:3,15:1}
        for address,count in expected_backbox.items():
            qualifier = "at least " if address in {14,15} else ""
            self.assertIn(f"backbox inset contains {qualifier}{count} clearly legible bulb symbol",self.solenoids[address]["physical"]["notes"],address)
        for address in {3,4,8,9,12,14,15}:
            self.assertEqual("conflicted",self.solenoids[address]["provenance"]["status"],address)
        self.assertEqual("backbox/back panel",self.solenoids[12]["physical"]["location"])
        self.assertEqual(("not_applicable","cabinet_or_service"),(self.solenoids[12]["spatial"]["status"],self.solenoids[12]["spatial"]["reason"]))

    def test_manual_solenoid_aliases_exist_only_for_printed_addresses(self) -> None:
        import curate_playboy_35th as curator
        expected = {}
        expected.update({number:f"SIDE L {number:02d}" for number in range(1,9)})
        expected.update({number:str(number) for number in range(9,17)})
        expected.update({17:"SP1",18:"SP3",19:"SP4",20:"SP6",21:"SP5",22:"SP2"})
        expected.update({number:f"SIDE R {number-24:02d}" for number in range(25,33)})
        derived = {17 + curator.SPECIAL_DE_PERMUTATION[handler]:printed for handler,printed in curator.SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
        self.assertEqual({17:1,18:3,19:4,20:6,21:5,22:2},derived)
        self.assertEqual(derived,curator.SPECIAL_PUBLIC_TO_PRINTED)
        manual_source = "manual.data-east.playboy-35th-anniversary.1989"
        for address,item in self.solenoids.items():
            aliases = [alias["value"] for alias in item["aliases"] if alias["namespace"] == "manual.address"]
            if address in expected:
                self.assertEqual([expected[address]],aliases,address)
                self.assertIn(manual_source,item["provenance"]["source_refs"],address)
                self.assertIn(f"Manual printed address {expected[address]}.",item["physical"]["notes"],address)
            else:
                self.assertEqual([],aliases,address)
                self.assertNotIn(manual_source,item["provenance"]["source_refs"],address)
                self.assertNotIn("manual printed address",item["physical"]["notes"].casefold(),address)

    def test_control_virtual_and_synthetic_outputs_have_dispositions(self) -> None:
        self.assertEqual("control_signal",self.solenoids[23]["kind"])
        self.assertEqual(("coil","unused","unused"),(self.solenoids[20]["kind"],self.solenoids[20]["availability"],self.solenoids[20]["spatial"]["reason"]))
        self.assertEqual(("virtual","unused","virtual"),(self.solenoids[24]["kind"],self.solenoids[24]["availability"],self.solenoids[24]["spatial"]["reason"]))
        self.assertEqual({17:"Q8",18:"Q10",19:"Q11",20:"Q13",21:"Q12",22:"Q9"},{address:self.solenoids[address]["wiring"]["driver_transistor"] for address in range(17,23)})
        self.assertEqual("unused",self.solenoids[24]["availability"])
        for address in range(33,45):
            self.assertEqual(("virtual","unused"),(self.solenoids[address]["kind"],self.solenoids[address]["availability"]),address)
        for address in range(45,49):
            self.assertEqual(("virtual","used"),(self.solenoids[address]["kind"],self.solenoids[address]["availability"]),address)
            self.assertIn("Synthetic PinMAME",self.solenoids[address]["physical"]["notes"])
            self.assertNotIn("quantity",self.solenoids[address]["physical"])
            self.assertNotIn("part_number",self.solenoids[address]["physical"])
            self.assertEqual(("not_applicable","virtual"),(self.solenoids[address]["spatial"]["status"],self.solenoids[address]["spatial"]["reason"]),address)
        self.assertEqual("unused",self.solenoids[49]["availability"])
        self.assertEqual("unused",self.solenoids[50]["availability"])

    def test_displays_are_controlled_not_applicable_records(self) -> None:
        displays = self.definition["displays"]
        self.assertEqual([1,9,21,29],[display["segment_start"] for display in displays])
        self.assertEqual([7,7,7,7],[display["width"] for display in displays])
        for display in displays:
            self.assertEqual("not_applicable",display["spatial"]["status"])
            self.assertEqual("cabinet_or_service",display["spatial"]["reason"])

    def test_mechanisms_have_causal_topology_not_feature_labels(self) -> None:
        mechanisms = {item["id"]:item for item in self.definition["mechanisms"]}
        trough = mechanisms["mechanism.ball-trough"]
        self.assertEqual(["coil.driver-26"],trough["actuators"])
        self.assertEqual(["switch.matrix-11","switch.matrix-12","switch.matrix-13"],trough["sensors"])
        self.assertEqual(3,len(trough["positions"]))
        drop = mechanisms["mechanism.drop-bank"]
        self.assertEqual(["coil.driver-29"],drop["actuators"])
        self.assertEqual(["switch.matrix-49","switch.matrix-50","switch.matrix-51"],drop["sensors"])
        fixed = mechanisms["mechanism.playboy-standups"]
        self.assertEqual([],fixed["actuators"])
        self.assertIn("no dropping faces",fixed["behavior"])
        self.assertEqual(["coil.driver-18"],mechanisms["mechanism.left-slingshot"]["actuators"])
        self.assertEqual(["coil.driver-19"],mechanisms["mechanism.left-pop"]["actuators"])
        self.assertEqual(["coil.driver-22"],mechanisms["mechanism.right-pop"]["actuators"])
        self.assertEqual(["switch.matrix-47"],mechanisms["mechanism.center-pop"]["sensors"])
        self.assertEqual(["switch.matrix-48"],mechanisms["mechanism.right-pop"]["sensors"])
        self.assertEqual("candidate",mechanisms["mechanism.center-pop"]["provenance"]["status"])
        self.assertEqual("candidate",mechanisms["mechanism.right-pop"]["provenance"]["status"])
        self.assertEqual(self.switches[47]["spatial"]["placements"][0]["x"],self.solenoids[17]["spatial"]["placements"][0]["x"])
        self.assertEqual(self.switches[47]["spatial"]["placements"][0]["y"],self.solenoids[17]["spatial"]["placements"][0]["y"])
        self.assertEqual(self.switches[48]["spatial"]["placements"][0]["x"],self.solenoids[22]["spatial"]["placements"][0]["x"])
        self.assertEqual(self.switches[48]["spatial"]["placements"][0]["y"],self.solenoids[22]["spatial"]["placements"][0]["y"])

    def test_ten_conflicts_are_exact_and_first_class(self) -> None:
        expected = {
            "conflict.shared-port-position-2-vs-unfitted",
            "conflict.left-eos-vs-public-button-state","conflict.right-eos-vs-public-button-state",
            "conflict.shooter-laser-switch-part-numbers","conflict.outputs-4-and-5-share-pseudo-lamp-105",
            "conflict.outputs-13-through-15-script-comments-vs-manual","conflict.muxed-c-bank-core-bulb-type-vs-manual-coils",
            "conflict.drop-reset-coil-type-print","conflict.special-solenoid-19-vs-background-proxy",
            "conflict.flash-location-drawing-vs-playfield-proxies",
        }
        self.assertEqual(expected,{item["id"] for item in self.definition["conflicts"]})
        self.assertTrue(all(item["source_refs"] for item in self.definition["conflicts"]))

    def test_spatial_pair_is_complete_normalized_and_names_concrete_blockers(self) -> None:
        report = load_json(SPATIAL_JSON_PATH)
        self.assertTrue(SPATIAL_MD_PATH.is_file())
        self.assertEqual({"left":0.0,"top":0.0,"right":952.0,"bottom":1974.0},report["coordinate_system"]["raw_bounds"])
        self.assertEqual(set(self.definition["coverage"]["missing"]),{row["dimension"] for row in report["blockers"]})
        for blocker in report["blockers"]:
            self.assertTrue(blocker["devices"],blocker["dimension"])
            self.assertTrue(blocker["reason"].strip(),blocker["dimension"])
            self.assertTrue(blocker["would_resolve"].strip(),blocker["dimension"])
        spatial_blocker = next(blocker for blocker in report["blockers"] if blocker["dimension"] == "spatial_placement")
        self.assertEqual(
            {f"coil.driver-{number}" for number in [1,2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,21,22,25,26,27,28,29,30]},
            {device for device in spatial_blocker["devices"] if device.startswith("coil.driver-")},
        )
        placement_ids = set()
        for device in list(self.definition["inputs"])+list(self.definition["outputs"]):
            spatial = device.get("spatial")
            if not spatial or spatial["status"] == "not_applicable":
                continue
            for placement in spatial["placements"]:
                self.assertNotIn(placement["id"],placement_ids)
                placement_ids.add(placement["id"])
                for axis in ("x","y"):
                    self.assertGreaterEqual(placement[axis],0.0)
                    self.assertLessEqual(placement[axis],1.0)
                    self.assertLessEqual(len(str(placement[axis]).partition(".")[2]),6)

    def test_excerpts_are_committed_reviewed_and_hash_pinned(self) -> None:
        manual = next(item for item in self.definition["sources"] if item["kind"] == "manual")
        self.assertTrue(manual["uri"].startswith("external:pinmame-manuals/"))
        self.assertTrue(all(item["uri"] == "https://github.com/vpinball/pinmame" for item in self.definition["sources"] if item["kind"] in {"pinmame_catalog","pinmame_core"}))
        self.assertTrue(all(item["uri"].startswith("external:pinmame-vpx-sources/") for item in self.definition["sources"] if item["kind"] in {"vpx_table","vpx_script"} and item["id"] != "vpx-extraction.playboy-35th-hybrid-1.1"))
        self.assertTrue(all(not item["uri"].startswith(("source-checkouts/","vpx-sources/","external:pinmame-manual-cache/")) for item in self.definition["sources"]))
        self.assertEqual(4,len(manual["excerpts"]))
        for excerpt in manual["excerpts"]:
            path = ROOT/excerpt["path"]
            self.assertTrue(path.is_file(),path)
            self.assertTrue(excerpt["reviewed"],path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),excerpt["sha256"],path)
        switch_text = (EXCERPT_DIR/"switch-matrix.md").read_text(encoding="utf-8")
        lamp_text = (EXCERPT_DIR/"lamp-matrix.md").read_text(encoding="utf-8")
        coil_text = (EXCERPT_DIR/"coil-and-flipper.md").read_text(encoding="utf-8")
        for literal in ("42 Ctr 3 Bank-Mid","21: Left Slingshot Trigger Sw.; Left Slingshot Point Sw.","52: Not Used Thru 64"):
            self.assertIn(literal,switch_text)
        for literal in ("46 DropTar. 50K","55 pinbAll","61 mansIon","Miss September Lites Out-lane 50k"):
            self.assertIn(literal,lamp_text)
        for literal in ("SP5 | Right Slingshot","23-1200","12-1200","090-5008-00","Backbox Flash lamps","INSERT 2 DROP FLASH","| 12 | 4 | 4 |","Three further glyphs resemble `5`/`6`","lack of a registered coordinate frame"):
            self.assertIn(literal,coil_text)
        self.assertNotIn("Retained VPX playfield effect objects",coil_text)
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("manual places those PINBALL letters on the playfield",knowledge)
        self.assertNotIn("six-machine",knowledge)
        self.assertIn("seven routed PINBALL lamps are not located by the manual's drawing at all",knowledge)
        self.assertNotIn("seven routed lamps disagree on playfield/backglass plane",knowledge)

    def test_definition_seed_and_manifest_digests_are_pinned(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(),SEED_PATH.read_bytes())
        manifest = load_json(MANIFEST_PATH)
        algorithm = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
        self.assertEqual(algorithm,manifest["manifest_algorithm"])
        body = {key:value for key,value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
        self.assertEqual("408ba0ec4e18187f0f86c1970c33cc31b93af53df24ad83f2eeea599822bb672",hashlib.sha256(canonical).hexdigest())
        self.assertEqual(manifest["manifest_sha256"],hashlib.sha256(canonical).hexdigest())
        self.assertEqual(2270,manifest["file_count"])
        self.assertEqual(164978347,manifest["total_bytes"])
        extraction_source = next(item for item in self.definition["sources"] if item["id"].startswith("vpx-extraction"))
        self.assertEqual("228204226a90f8974c46d30ef4d9b24c24852099ddccf8f8c743cd4051eaadaf",extraction_source["sha256"])
        self.assertIn(f"algorithm: {algorithm}",extraction_source["locator"])
        self.assertEqual(extraction_source["sha256"],sha256(MANIFEST_PATH))

    def test_no_other_machine_identifiers_leak_into_generated_artifacts(self) -> None:
        this_id = self.definition["machine"]["id"]
        catalog = load_json(ROOT/"catalog/pinmame.json")
        foreign = {record["id"] for record in catalog["machines"] if record.get("id") and record["id"] != this_id}
        # Bare ROM ids such as ``pinball`` are ordinary English words and are not safe
        # contamination sentinels. Underscore-bearing ids remain unambiguous.
        foreign.update(
            driver["id"]
            for driver in catalog["drivers"]
            if driver.get("machine_id") and driver["machine_id"] != this_id and "_" in driver["id"]
        )
        explicit = {"Batman","btmnGameData","btmn","lw3GameData","tmacGameData","ssvcGameData","torpGameData","lwarGameData","GEN_DEDMD16","GEN_DEDMD32","VPW 1.1","VPW 2.0"}
        blobs = [(path.name,json.dumps(load_json(path))) for path in (DEFINITION_PATH,SEED_PATH,SPATIAL_JSON_PATH)]
        blobs.append((KNOWLEDGE_PATH.name,KNOWLEDGE_PATH.read_text(encoding="utf-8")))
        for name,blob in blobs:
            for needle in sorted(value for value in foreign if len(value) >= 5) + sorted(explicit):
                self.assertIsNone(
                    re.search(r"(?<![A-Za-z0-9_])"+re.escape(needle)+r"(?![A-Za-z0-9_])",blob),
                    f"{name} carries {needle!r} from another machine",
                )

    def test_catalog_derived_foreign_identifiers_are_absent(self) -> None:
        catalog = load_json(ROOT/"catalog/pinmame.json")
        own = {"play_a24","data-east.playboy-35th-anniversary.1989"}
        # Full machine ids and underscore-bearing ROM short names are unambiguous
        # catalog identifiers. Bare driver ids such as "pinball" are ordinary words
        # in this definition and therefore unsuitable as a contamination sentinel.
        foreign = {
            row["id"]
            for key in ("drivers","machines")
            for row in catalog[key]
            if row["id"] not in own and (key == "machines" or "_" in row["id"])
        }
        artifacts = "\n".join(path.read_text(encoding="utf-8") for path in [DEFINITION_PATH,SEED_PATH,KNOWLEDGE_PATH,SPATIAL_JSON_PATH,SPATIAL_MD_PATH])
        for identifier in foreign:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(identifier)}(?![A-Za-z0-9_])"
            self.assertIsNone(re.search(pattern,artifacts,re.IGNORECASE),identifier)
        definition_text = DEFINITION_PATH.read_text(encoding="utf-8")
        self.assertNotIn('"width": 1000.0',definition_text)
        self.assertNotIn('"height": 1910.0',definition_text)


class PlayboyCuratorTests(unittest.TestCase):
    def test_curator_is_deterministic_and_check_passes_twice(self) -> None:
        import curate_playboy_35th as curator
        self.assertEqual(curator.json_text(curator.build_machine()).encode("utf-8"),DEFINITION_PATH.read_bytes())
        curator.check()
        curator.check()

    def test_check_refuses_drift_and_crlf_is_folded(self) -> None:
        import curate_playboy_35th as curator
        original = KNOWLEDGE_PATH.read_bytes()
        try:
            KNOWLEDGE_PATH.write_bytes(original+b"drift\n")
            with self.assertRaises(SystemExit):
                curator.check()
        finally:
            KNOWLEDGE_PATH.write_bytes(original)
        curator.check()
        # The system temp directory, not ROOT/"tmp": that path is gitignored (.gitignore line 2),
        # so it exists only on a machine that happens to have created it and is never present in a
        # clean checkout. Pinning the scratch directory inside the repository made this test pass
        # locally and fail on CI with FileNotFoundError. Nothing here needs to live in the repo -
        # the file is written, read back through compare_lf and discarded.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"fold.txt"
            path.write_bytes(b"alpha\r\nbeta\r\n")
            self.assertTrue(curator.compare_lf(path,"alpha\nbeta\n"))

    def test_curator_refuses_an_author_ready_twin(self) -> None:
        import curate_playboy_35th as curator
        path = ROOT/curator.AUTHOR_READY_PATH
        self.assertFalse(path.exists())
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text("{}\n",encoding="utf-8")
        try:
            with self.assertRaises(RuntimeError):
                curator.generate()
            with self.assertRaises(SystemExit):
                curator.check()
        finally:
            path.unlink()
        curator.check()


@unittest.skipUnless(VPX_EVIDENCE_ROOT,"retained VPX evidence root is not configured")
class PlayboyRetainedVpxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert VPX_EVIDENCE_ROOT is not None
        cls.root = Path(VPX_EVIDENCE_ROOT)/"data-east/playboy-35th-anniversary-1989"
        cls.extract = cls.root/"vpxtool-extract"

    def test_table_script_identity_hashes_and_bounds(self) -> None:
        self.assertEqual("3b32aeacee1c5beb1c723e6e1bba79ae269deb36cc56101201b5d171a7a8336b",sha256(self.root/TABLE_NAME))
        script = self.extract/"script.vbs"
        self.assertEqual("83e632d397afbec660ea356b1820aadbd648d0a90d4affdce5bfc4e864bb0da5",sha256(script))
        script_text = script.read_text(encoding="utf-8",errors="replace")
        self.assertRegex(script_text,r'Const\s+cGameName\s*=\s*"play_a24"')
        gamedata = load_json(self.extract/"gamedata.json")
        self.assertEqual((0.0,0.0,952.0,1974.0),(gamedata["left"],gamedata["top"],gamedata["right"],gamedata["bottom"]))
        self.assertEqual(1748,len([path for path in (self.extract/"gameitems").rglob("*") if path.is_file()]))

    def test_setlamp_idiom_and_numeric_light_accounting(self) -> None:
        script = (self.extract/"script.vbs").read_text(encoding="utf-8",errors="replace")
        active = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("'"))
        self.assertEqual(16,len(re.findall(r"\bSetLamp\b",active,re.IGNORECASE)))
        self.assertNotRegex(active,r"\bLampz\.MassAssign\b")
        self.assertNotRegex(active,r"\bvpmMapLights\b")
        lights = {}
        for path in (self.extract/"gameitems").glob("Light.L*.json"):
            match = re.fullmatch(r"Light\.L(\d+)\.json",path.name,re.IGNORECASE)
            if match:
                lights[int(match.group(1))] = path
        self.assertEqual(55,len(lights))
        self.assertEqual(BACKBOX_LAMPS,set(range(1,65))-set(lights))
        for address in BACKBOX_LAMPS:
            self.assertTrue((self.extract/"gameitems"/f"Flasher.l{address}.json").is_file(),address)
            self.assertRegex(active,rf"(?im)^\s*Flash\s+{address}\s*,\s*l{address}\b")
        for address in MANUAL_UNLOCATED_PINBALL_LAMPS:
            data = load_json(lights[address])["Light"]
            self.assertTrue(data["is_backglass"],address)

    def test_pop_bumper_manual_script_and_geometry_agree(self) -> None:
        import curate_playboy_35th as curator
        script = (self.extract/"script.vbs").read_text(encoding="utf-8",errors="replace")
        self.assertRegex(script,r"(?im)^\s*Sub\s+Bumper1_Hit\s*:\s*vpmTimer\.PulseSw\s+46\b")
        self.assertRegex(script,r"(?im)^\s*Sub\s+Bumper2_Hit\s*:\s*vpmTimer\.PulseSw\s+47\b")
        self.assertRegex(script,r"(?im)^\s*Sub\s+Bumper3_Hit\s*:\s*vpmTimer\.PulseSw\s+48\b")
        definition_switches = bindings(load_json(DEFINITION_PATH),"inputs","pinmame.input.switch")
        self.assertEqual("Left Pop Bumper",definition_switches[46]["label"])
        self.assertEqual("Center Pop Bumper",definition_switches[47]["label"])
        self.assertEqual("Right Pop Bumper",definition_switches[48]["label"])
        self.assertRegex(script,r"(?im)^\s*Sub\s+Bumper2_Hit\b[^\r\n]*RandomSoundBumperMiddle\s+Bumper2\b")
        for address in (46,47,48):
            placement = definition_switches[address]["spatial"]["placements"][0]
            raw_x,raw_y = curator.RAW_SWITCH_POINTS[address]
            self.assertAlmostEqual(raw_x/952.0,placement["x"],places=6,msg=address)
            self.assertAlmostEqual(raw_y/1974.0,placement["y"],places=6,msg=address)
        for address in (47,48):
            self.assertEqual("validated",definition_switches[address]["provenance"]["status"])
            self.assertEqual("observed",definition_switches[address]["spatial"]["status"])

    def test_curator_uses_exact_retained_light_centers(self) -> None:
        import curate_playboy_35th as curator
        for address,expected in curator.RAW_LAMP_POINTS.items():
            names = [f"Light.l{address}.json"]
            if len(expected) == 2:
                names.append(f"Light.l{address}a.json")
            actual = []
            for name in names:
                center = load_json(self.extract/"gameitems"/name)["Light"]["center"]
                actual.append((center["x"],center["y"]))
            self.assertEqual(expected,actual,address)

    def test_curator_uses_exact_retained_switch_flash_and_gi_geometry(self) -> None:
        import curate_playboy_35th as curator
        direct_switches = {30:("Spinner.Spinner.json","Spinner"),**{number:(f"HitTarget.sw{number}.json","HitTarget") for number in [34,35,36,37,38,39,41,42,43,49,50,51]}}
        for address,(filename,item_type) in direct_switches.items():
            item = load_json(self.extract/"gameitems"/filename)[item_type]
            point = item["center"] if item_type == "Spinner" else item["position"]
            self.assertEqual(curator.RAW_SWITCH_POINTS[address],(point["x"],point["y"]),address)
        for address,filename in {21:"Wall.Leftslingshot.json",22:"Wall.Rightslingshot.json"}.items():
            points = load_json(self.extract/"gameitems"/filename)["Wall"]["drag_points"]
            actual = (sum(point["x"] for point in points)/len(points),sum(point["y"] for point in points)/len(points))
            self.assertEqual(curator.RAW_SWITCH_POINTS[address],actual,address)
        flash_names = {
            1:["Fl1"],2:["Fl2"],3:["Fl3"],4:["Fl4"],5:["Fl5"],6:["Fl6"],7:["Fl7"],8:["Fl8"],
            9:["Fl9","Fl9a","Fl9b","Fl9c"],12:["Fl20","Fl21","Fl22"],13:["Fl13"],14:["Fl14"],15:["FL15"],
        }
        for address,names in flash_names.items():
            actual = []
            for name in names:
                center = load_json(self.extract/"gameitems"/f"Light.{name}.json")["Light"]["center"]
                actual.append((center["x"],center["y"]))
            self.assertEqual(curator.RAW_FLASH_POINTS[address],actual,address)
        collection = next(row for row in load_json(self.extract/"collections.json") if row["name"] == "aGiLights")
        actual_gi = []
        for name in collection["items"]:
            matches = list((self.extract/"gameitems").glob(f"*.{name}.json"))
            self.assertEqual(1,len(matches),name)
            record = load_json(matches[0])
            item = next(iter(record.values()))
            center = item["center"]
            actual_gi.append((center["x"],center["y"]))
        self.assertEqual(curator.RAW_GI_POINTS,actual_gi)

    def test_retained_extraction_matches_every_manifest_entry(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        actual_paths = {path.relative_to(self.extract).as_posix() for path in self.extract.rglob("*") if path.is_file()}
        self.assertEqual({row["path"] for row in manifest["files"]},actual_paths)
        total = 0
        for row in manifest["files"]:
            path = self.extract/row["path"]
            total += path.stat().st_size
            self.assertEqual(row["bytes"],path.stat().st_size,row["path"])
            self.assertEqual(row["sha256"],sha256(path),row["path"])
        self.assertEqual(manifest["total_bytes"],total)


@unittest.skipUnless(MANUAL_EVIDENCE_ROOT,"retained manual root is not configured")
class PlayboyRetainedManualTests(unittest.TestCase):
    def test_manual_identity_and_text_layer_metadata(self) -> None:
        assert MANUAL_EVIDENCE_ROOT is not None
        root = Path(MANUAL_EVIDENCE_ROOT)
        base = root/"by-machine/data-east.playboy-35th-anniversary.1989/contributor-supplied"
        if not base.is_dir() and root.name == "manuals":
            base = root.parent/"manual-cache/by-machine/data-east.playboy-35th-anniversary.1989/contributor-supplied"
        manual = base/MANUAL_NAME
        self.assertEqual(14450592,manual.stat().st_size)
        self.assertEqual("0c4be366c30942919b7101c69acfb6563ac8bc6cd5aaaac0bad24ae5b9b1afa7",sha256(manual))
        metadata = load_json(base/"hashes.json")[MANUAL_NAME]
        self.assertEqual(76,metadata["page_count"])
        self.assertEqual(76678,metadata["sampled_characters"])


if __name__ == "__main__":
    unittest.main()
