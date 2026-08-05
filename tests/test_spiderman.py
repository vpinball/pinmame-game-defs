from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.evidence_policy import EvidenceAssertion, decide_evidence, evidence_priority
from pinmame_game_defs.jsonio import content_sha256


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/author-ready/stern/spider-man-2007.json"
CATALOG_PATH = ROOT / "catalog/pinmame.json"
CURATOR_PATH = ROOT / "tools/curate_spiderman_spatial.py"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/spider-man-2007.json"
EXPECTED_TABLE_SHA256 = "97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47"
EXPECTED_EMBEDDED_SCRIPT_SHA256 = "ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128"
EXPECTED_SIDECAR_SCRIPT_SHA256 = "cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def load_curator():
	spec = importlib.util.spec_from_file_location("curate_spiderman_spatial_test", CURATOR_PATH)
	assert spec is not None and spec.loader is not None
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def provenance_refs(value: object) -> list[str]:
	refs: list[str] = []
	if isinstance(value, dict):
		if isinstance(value.get("source_refs"), list):
			refs.extend(str(ref) for ref in value["source_refs"])
		for child in value.values():
			refs.extend(provenance_refs(child))
	elif isinstance(value, list):
		for child in value:
			refs.extend(provenance_refs(child))
	return refs


class SpiderManSpatialTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.catalog = load_json(CATALOG_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")[0]

	def test_catalog_machine_hash_matches_definition_and_driver_records(self) -> None:
		expected_hash = content_sha256(self.definition)
		machine = next(machine for machine in self.catalog["machines"] if machine["id"] == "stern.spider-man.2007")
		self.assertEqual(DEFINITION_PATH.relative_to(ROOT).as_posix(), machine["definition"])
		self.assertEqual(expected_hash, machine["definition_sha256"])
		drivers = [driver for driver in self.catalog["drivers"] if driver.get("machine_id") == machine["id"]]
		self.assertEqual(45, len(drivers))
		self.assertTrue(all(driver["definition_sha256"] == expected_hash for driver in drivers))

	def test_author_ready_inventory_is_fully_disposed(self) -> None:
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(96, len(self.definition["inputs"]))
		self.assertEqual(117, len(self.definition["outputs"]))
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in [*self.definition["inputs"], *self.definition["outputs"]]))
		self.assertEqual(
			{
				"status": "not_applicable",
				"reason": "cabinet_or_service",
				"provenance": {
					"status": "validated",
					"source_refs": ["pinmame.core.4ec52ff0ac13", "manual.spider-man.2007-service"],
				},
			},
			self.definition["displays"][0]["spatial"],
		)
		self.assertFalse((ROOT / "machines/partial/stern/spider-man-2007.json").exists())
		self.assertTrue(all("128×32 DMD topology" in driver["variant_notes"] for driver in self.definition["drivers"]))
		self.assertIn("x≈0.066, y≈0.432", self.solenoids[28]["physical"]["notes"])

	def test_sandman_flasher_callouts_are_disclosed_manual_projections(self) -> None:
		device = self.solenoids[23]
		self.assertIn("manual page 11 callouts", device["physical"]["notes"])
		self.assertIn("No exact F23 socket objects", device["physical"]["notes"])
		for placement in device["spatial"]["placements"]:
			self.assertEqual(["manual.spider-man.2007-service"], placement["provenance"]["source_refs"])

	def test_exact_table_source_and_bounds_are_hash_locked(self) -> None:
		source = next(item for item in self.definition["sources"] if item["id"] == "vpx-table.spider-man-3.0")
		self.assertEqual(EXPECTED_TABLE_SHA256, source["sha256"])
		self.assertIn("right=952, bottom=2115", source["locator"])
		self.assertTrue(source["uri"].startswith("external:pinmame-vpx-sources/stern/spider-man-2007/source/"))
		self.assertNotIn("L:\\", json.dumps(source))
		script = next(item for item in self.definition["sources"] if item["id"] == "vpx.spider-man-3.0")
		self.assertEqual(EXPECTED_EMBEDDED_SCRIPT_SHA256, script["sha256"])
		self.assertEqual(EXPECTED_TABLE_SHA256, script["locator"].split("table SHA-256 ", 1)[1].split(")", 1)[0])
		self.assertIn("vpxtool git:v0.33.3", script["locator"])
		self.assertEqual(script["sha256"], load_json(SPATIAL_REPORT_PATH)["script"]["sha256"])
		sidecar = next(item for item in self.definition["sources"] if item["id"] == "vpx-sidecar.spider-man-3.0")
		self.assertEqual(EXPECTED_SIDECAR_SCRIPT_SHA256, sidecar["sha256"])
		self.assertIn("not paired", sidecar["locator"])
		self.assertEqual(EXPECTED_SIDECAR_SCRIPT_SHA256, load_json(SPATIAL_REPORT_PATH)["sidecar_script"]["sha256"])

	def test_embedded_script_authority_is_domain_specific(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		embedded = sources["vpx.spider-man-3.0"]
		sidecar = sources["vpx-sidecar.spider-man-3.0"]
		self.assertTrue(embedded["known_working"])
		self.assertFalse(sidecar.get("known_working", False))

		embedded_assertion = EvidenceAssertion(
			"embedded-causality",
			embedded["id"],
			embedded["kind"],
			known_working=embedded["known_working"],
		)
		manual_causality = EvidenceAssertion("conflicting-manual-causality", "manual.spider-man.2007-service", "manual")
		causality = decide_evidence("mechanism_causality", [manual_causality, embedded_assertion])
		self.assertEqual("embedded-causality", causality.value)
		self.assertEqual(("vpx.spider-man-3.0",), causality.selected_source_refs)
		self.assertEqual(400, causality.priority)
		self.assertEqual(400, evidence_priority("mechanism_causality", embedded_assertion))

		manual_wiring = EvidenceAssertion("manual-wiring", "manual.spider-man.2007-service", "manual")
		physical_script = EvidenceAssertion(
			"conflicting-script-wiring",
			embedded["id"],
			embedded["kind"],
			known_working=embedded["known_working"],
		)
		wiring = decide_evidence("physical_wiring", [physical_script, manual_wiring])
		self.assertEqual("manual-wiring", wiring.value)
		self.assertEqual(("manual.spider-man.2007-service",), wiring.selected_source_refs)

	def test_sidecar_cannot_be_represented_as_paired_authoritative_script(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("causality_authoritative_embedded_script", report["script"]["role"])
		self.assertEqual(EXPECTED_TABLE_SHA256, report["script"]["table_sha256"])
		self.assertEqual("secondary_corroborating_unpaired_script", report["sidecar_script"]["role"])
		self.assertFalse(report["sidecar_script"]["paired_with_table"])
		self.assertNotIn("vpx-sidecar.spider-man-3.0", provenance_refs(self.definition))
		eos = self.switches[85]
		self.assertEqual(["manual.spider-man.2007-service", "pinmame.core.4ec52ff0ac13"], eos["provenance"]["source_refs"])
		self.assertIn("does not assert switch 85", next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.upper-right-flipper")["behavior"])

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "set PINMAME_VPX_SOURCES_ROOT for the external embedded-script extraction check")
	def test_fresh_extraction_locks_embedded_script_and_sidecar_divergence(self) -> None:
		vpxtool = shutil.which("vpxtool") or shutil.which("vpxtool.exe")
		if vpxtool is None:
			self.skipTest("vpxtool is unavailable for the external integration check")
		source_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		vpx = source_root / "stern/spider-man-2007/source/Spider-Man_3.0.vpx"
		sidecar = source_root / "stern/spider-man-2007/source/Spider-Man_3.0.vbs"
		if not vpx.is_file() or not sidecar.is_file():
			self.skipTest(f"Spider-Man external VPX source cache is unavailable under {source_root}")
		self.assertEqual(EXPECTED_TABLE_SHA256, hashlib.sha256(vpx.read_bytes()).hexdigest())
		with tempfile.TemporaryDirectory(prefix="spiderman-vpxtool-test-") as temporary:
			result = subprocess.run([vpxtool, "extract", "--force", "--output-dir", temporary, str(vpx)], check=False, capture_output=True, text=True)
			self.assertEqual(0, result.returncode, result.stderr)
			embedded = Path(temporary) / "script.vbs"
			self.assertTrue(embedded.is_file())
			embedded_bytes = embedded.read_bytes()
			embedded_text = embedded_bytes.decode("utf-8-sig")
			self.assertEqual(EXPECTED_EMBEDDED_SCRIPT_SHA256, hashlib.sha256(embedded_bytes).hexdigest())
			self.assertEqual(EXPECTED_SIDECAR_SCRIPT_SHA256, hashlib.sha256(sidecar.read_bytes()).hexdigest())
			self.assertNotEqual(hashlib.sha256(embedded_bytes).digest(), hashlib.sha256(sidecar.read_bytes()).digest())
			self.assertIn("Const UseSolenoids = 1", embedded_text)
			self.assertNotIn("NoUpperRightFlipper", embedded_text)
			self.assertIn("Controller.Switch(86)=1", embedded_text)
			self.assertIn('SolCallback(14) = "solURFlipper"', embedded_text)
			sidecar_text = sidecar.read_text(encoding="utf-8-sig")
			self.assertIn("Const UseSolenoids = 2", sidecar_text)
			self.assertIn("NoUpperRightFlipper", sidecar_text)

	def test_manual_review_artifact_manifest_is_nonempty_and_hash_locked(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		artifacts = report["review_artifacts"]
		self.assertEqual("external:pinmame-review-artifacts/stern/spider-man-2007/manual-pages", artifacts["uri"])
		self.assertEqual(23, len(artifacts["files"]))
		self.assertEqual([6, 8, 9, 10, 11, 37, 68, 69, 85, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 118, 119, 120, 121], [item["page"] for item in artifacts["files"]])
		self.assertTrue(all(len(item["sha256"]) == 64 for item in artifacts["files"]))

	def test_hidden_assembly_anchors_and_trough_order_are_explicit(self) -> None:
		trough = [self.switches[address]["spatial"]["placements"][0] for address in (18, 19, 20, 21, 22)]
		self.assertEqual(sorted(point["x"] for point in trough), [point["x"] for point in trough])
		self.assertEqual(sorted((point["y"] for point in trough), reverse=True), [point["y"] for point in trough])
		for address in (49, 50):
			self.assertEqual((0.501990, 0.312554), tuple(self.switches[address]["spatial"]["placements"][0][key] for key in ("x", "y")))
		for left, right in ((53, 54), (57, 58)):
			self.assertEqual(self.switches[left]["spatial"]["placements"][0]["x"], self.switches[right]["spatial"]["placements"][0]["x"])
		self.assertIn("assembly projection", self.switches[22]["physical"]["notes"])
		self.assertEqual((0.764706, 0.315258), tuple(self.solenoids[5]["spatial"]["placements"][0][key] for key in ("x", "y")))

	def test_upper_right_flipper_d15_d16_are_used_and_wired(self) -> None:
		button = self.switches[86]
		eos = self.switches[85]
		self.assertEqual("used", button["availability"])
		self.assertEqual("used", eos["availability"])
		self.assertEqual("switch.upper-right-flipper-button", button["id"])
		self.assertEqual("switch.upper-right-flipper-eos", eos["id"])
		self.assertIn("vpx.spider-man-3.0", button["provenance"]["source_refs"])
		self.assertEqual("cabinet.flipper.button", button["roles"][0])
		self.assertEqual((0.855358, 0.460841), tuple(eos["spatial"]["placements"][0][key] for key in ("x", "y")))
		mechanism = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.upper-right-flipper")
		self.assertEqual(["switch.upper-right-flipper-button", "switch.upper-right-flipper-eos"], mechanism["sensors"])
		self.assertIn("switch 86", mechanism["behavior"])
		self.assertIn("output 14", mechanism["behavior"])
		self.assertIn("does not assert switch 85", mechanism["behavior"])


	def test_physical_flasher_multiplicity_and_back_panel_lamps(self) -> None:
		for address, quantity in ((23, 2), (25, 2), (28, 2), (31, 3)):
			self.assertEqual(quantity, self.solenoids[address]["physical"]["quantity"])
			self.assertEqual(quantity, len(self.solenoids[address]["spatial"]["placements"]))
		q28_points = {(point["x"], point["y"]) for point in self.solenoids[28]["spatial"]["placements"]}
		self.assertEqual(2, len(q28_points))
		self.assertIn("two distinct Q28", self.solenoids[28]["physical"]["notes"])
		for address in (29, 30):
			self.assertEqual(0.0, self.solenoids[address]["spatial"]["placements"][0]["y"])
			self.assertIn("back-panel", self.solenoids[address]["physical"]["notes"])
		for address in range(66, 72):
			self.assertEqual(0.0, self.lamps[address]["spatial"]["placements"][0]["y"])
		for address in (55, 56, 73, 79, 80):
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"])

	def test_gi_circuit_counts_do_not_count_render_helpers(self) -> None:
		placements = self.gi["spatial"]["placements"]
		self.assertEqual(44, self.gi["physical"]["quantity"])
		self.assertIn("US/non-Euro", self.gi["physical"]["location"])
		self.assertIn("Euro hardware has 3", self.gi["physical"]["notes"])
		self.assertEqual(42, len(placements))
		self.assertEqual({"brown": 8, "yellow": 11, "violet": 13, "green": 10}, {
			circuit: sum(f".emitter.{circuit}." in point["id"] for point in placements)
			for circuit in ("brown", "yellow", "violet", "green")
		})
		self.assertEqual(10, sum(point["y"] == 0.0 for point in placements))
		self.assertIn("coin-door bulbs", self.gi["physical"]["notes"])

	def test_base_entry_point_refuses_to_clobber_author_ready(self) -> None:
		base_spec = importlib.util.spec_from_file_location("curate_spiderman_base_test", ROOT / "tools/curate_spiderman.py")
		assert base_spec is not None and base_spec.loader is not None
		base = importlib.util.module_from_spec(base_spec)
		base_spec.loader.exec_module(base)
		before = DEFINITION_PATH.read_bytes()
		with self.assertRaisesRegex(RuntimeError, "author-ready canonical definition already exists"):
			base.main()
		self.assertEqual(before, DEFINITION_PATH.read_bytes())

	def test_incomplete_base_is_rejected_before_promotion(self) -> None:
		spatial = load_curator()
		base = copy.deepcopy(self.definition)
		base["outputs"] = base["outputs"][:-1]
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			partial = root / "partial.json"
			author_ready = root / "author-ready.json"
			partial.write_text(json.dumps(base), encoding="utf-8")
			spatial.PARTIAL_PATH = partial
			spatial.AUTHOR_READY_PATH = author_ready
			with self.assertRaisesRegex(RuntimeError, "base evidence is incomplete"):
				spatial.promote()
			self.assertFalse(author_ready.exists())

	def test_post_commit_seed_recreates_promoted_artifact(self) -> None:
		spatial = load_curator()
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("tools/seeds/stern/spider-man-2007.json", report["promotion_seed"]["path"])
		self.assertEqual("f7a34de84cac7e19d852c54f2d83939f995902578cd6ae64b01ed1aff1c06f6c", report["promotion_seed"]["sha256"])
		self.assertTrue(report["promotion_seed"]["byte_identical_to_author_ready"])
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			author_ready = root / "author-ready.json"
			spatial.PARTIAL_PATH = ROOT / "machines/partial/stern/spider-man-2007.json"
			spatial.AUTHOR_READY_PATH = author_ready
			self.assertFalse(spatial.PARTIAL_PATH.exists())
			self.assertTrue(spatial.SEED_PATH.exists())
			spatial.promote()
			first = author_ready.read_bytes()
			self.assertEqual(DEFINITION_PATH.read_bytes(), first)
			author_ready.unlink()
			spatial.promote()
			self.assertEqual(first, author_ready.read_bytes())


if __name__ == "__main__":
	unittest.main()
