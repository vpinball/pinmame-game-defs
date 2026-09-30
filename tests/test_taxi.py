"""Determinism and fail-closed contracts for the seed-owned Taxi curator."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_taxi as curator
import taxi_runtime_evidence as runtime_evidence
from build_external_evidence_manifest import write_manifest
from pinmame_game_defs.jsonio import canonical_bytes


SEED_PATH = ROOT / curator.SEED_RELATIVE_PATH
KNOWLEDGE_SEED_PATH = ROOT / curator.KNOWLEDGE_SEED_RELATIVE_PATH
DEFINITION_PATH = ROOT / curator.PARTIAL_RELATIVE_PATH
AUTHOR_READY_PATH = ROOT / curator.AUTHOR_READY_RELATIVE_PATH
KNOWLEDGE_PATH = ROOT / curator.KNOWLEDGE_RELATIVE_PATH
SPATIAL_REPORT_PATH = ROOT / curator.SPATIAL_REPORT_RELATIVE_PATH
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / curator.SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH
EVIDENCE_BINDING_PATH = ROOT / curator.EVIDENCE_BINDING_RELATIVE_PATH


def _write_json(path: Path, value: dict) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	if path.name == curator.EVIDENCE_BINDING_RELATIVE_PATH.name:
		value = {"format": "taxi-retained-evidence-bindings", "version": 1, **value}
	path.write_bytes(canonical_bytes(value))


def _digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture_definition(excerpt_sha256: str) -> dict:
	"""A small source-neutral partial fixture with Taxi's settled address topology."""
	source = {
		"id": "manual.fixture",
		"kind": "manual",
		"uri": "test://taxi-manual",
		"locator": "fixture",
		"license": "test-only",
		"attribution": "test fixture",
		"excerpts": [{
			"id": "excerpt.fixture",
			"locator": "fixture",
			"path": "evidence/excerpts/williams.taxi.1988/fixture.md",
			"sha256": excerpt_sha256,
		}],
	}
	provenance = {"status": "candidate", "source_refs": [source["id"]]}
	inputs: list[dict] = []
	for address in sorted(curator.EXPECTED_SWITCH_BINDINGS):
		device_id = f"switch.{address}" if address >= 0 else f"switch.diagnostic-minus-{abs(address)}"
		inputs.append({
			"id": device_id,
			"label": f"Fixture switch {address}",
			"kind": "switch",
			"binding": {"group": curator.SWITCH_GROUP, "device": address},
			"aliases": [],
			"availability": "used" if address in {82, 84} else "unknown",
			"provenance": provenance,
		})
	inputs.append({
		"id": "dip.country-0",
		"label": "Fixture country DIP",
		"kind": "dip_switch",
		"binding": {"group": curator.DIP_GROUP, "device": 0},
		"aliases": [],
		"availability": "unknown",
		"provenance": provenance,
	})

	outputs: list[dict] = []
	for address in sorted(curator.EXPECTED_SOLENOID_BINDINGS):
		outputs.append({
			"id": f"solenoid.{address}",
			"label": f"Fixture solenoid {address}",
			"kind": "virtual" if address in {45, 46, 47, 48} else "coil",
			"binding": {"group": curator.SOLENOID_GROUP, "device": address},
			"aliases": [],
			"availability": "unknown",
			"provenance": provenance,
		})
	for address in sorted(curator.EXPECTED_LAMP_BINDINGS):
		outputs.append({
			"id": f"lamp.{address}",
			"label": f"Fixture lamp {address}",
			"kind": "lamp",
			"binding": {"group": curator.LAMP_GROUP, "device": address},
			"aliases": [],
			"availability": "unknown",
			"provenance": provenance,
		})

	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {"id": curator.MACHINE_ID, "name": "Taxi", "manufacturer": "Williams", "year": 1988},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "candidate",
				"address_enumeration": "candidate",
				"semantic_naming": "candidate",
				"physical_wiring": "candidate",
				"mechanisms": "candidate",
				"variant_coverage": "candidate",
				"recreation_knowledge": "candidate",
				"spatial_placement": "candidate",
			},
		},
		"controller": {"platform": "pinmame.system-11"},
		"drivers": [
			{"id": driver_id, "description": f"Fixture {driver_id}", "year": "1988", "manufacturer": "Williams", "flags": 0}
			for driver_id in sorted(curator.DRIVER_IDS)
		],
		"inputs": inputs,
		"outputs": outputs,
		"displays": [
			{"id": "display.alpha-1", "label": "Fixture alpha 1", "kind": "segment", "width": 16, "provenance": provenance},
			{"id": "display.alpha-2", "label": "Fixture alpha 2", "kind": "segment", "width": 16, "provenance": provenance},
			{"id": "display.numeric", "label": "Fixture numeric", "kind": "segment", "width": 7, "provenance": provenance},
		],
		"mechanisms": [],
		"relationships": [
			{"id": "relationship.flipper-82-to-57", "kind": "direct", "source": "switch.82", "destination": "switch.57", "provenance": provenance},
			{"id": "relationship.flipper-84-to-58", "kind": "direct", "source": "switch.84", "destination": "switch.58", "provenance": provenance},
		],
		"sources": [source],
		"knowledge": {"path": curator.KNOWLEDGE_RELATIVE_PATH.as_posix(), "status": "partial"},
	}


def _fixture_root() -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
	temporary = tempfile.TemporaryDirectory()
	root = Path(temporary.name)
	excerpt = root / "evidence/excerpts/williams.taxi.1988/fixture.md"
	excerpt.parent.mkdir(parents=True, exist_ok=True)
	excerpt.write_text("fixture excerpt\n", encoding="utf-8")
	_write_json(root / curator.SEED_RELATIVE_PATH, _fixture_definition(_digest(excerpt)))
	knowledge_seed = root / curator.KNOWLEDGE_SEED_RELATIVE_PATH
	knowledge_seed.parent.mkdir(parents=True, exist_ok=True)
	knowledge_seed.write_bytes(b"# Fixture Taxi knowledge\r\n")
	_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, {"files": [
		{"root": "manuals", "path": "fixture.pdf", "size": 0, "sha256": hashlib.sha256(b"").hexdigest()}
	]})
	return temporary, root, excerpt


def _by_binding(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class TaxiFixtureCuratorTests(unittest.TestCase):
	def test_another_games_binding_register_cannot_be_used(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			path = root / curator.EVIDENCE_BINDING_RELATIVE_PATH
			register = json.loads(path.read_bytes())
			register["format"] = "another-game-evidence"
			_write_json(path, register)
			with self.assertRaisesRegex(RuntimeError, "wrong format"):
				curator.build(root)

	def test_generation_rejects_a_missing_binding_input_before_writing(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			(root / curator.EVIDENCE_BINDING_RELATIVE_PATH).unlink()
			with self.assertRaisesRegex(RuntimeError, "binding register is missing"):
				curator.generate(root)
			self.assertFalse((root / curator.PARTIAL_RELATIVE_PATH).exists())

	def test_retained_manifest_checks_extracted_bytes_not_only_manifest_hash(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			vpx_root = root / "retained"
			vpx_root.mkdir()
			table = vpx_root / "script.vbs"
			table.write_bytes(b"original extraction")
			write_manifest(vpx_root, "taxi_l4")
			manifest = vpx_root / "manifest.json"
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, {"files": [
				{"root": "vpx", "path": "manifest.sha256", "size": 65, "sha256": _digest(vpx_root / "manifest.sha256"),
				 "extraction_manifest": {"path": "manifest.json", "size": manifest.stat().st_size, "sha256": _digest(manifest)}}
			]})
			curator.verify_retained(vpx_root, None, None, root=root)
			table.write_bytes(b"changed extraction")
			with self.assertRaisesRegex(RuntimeError, "extraction content drifted"):
				curator.verify_retained(vpx_root, None, None, root=root)

	def test_seed_drives_byte_deterministic_generation(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			catalog = root / "catalog/pinmame.json"
			coverage = root / "reports/coverage.json"
			catalog.parent.mkdir(parents=True, exist_ok=True)
			coverage.parent.mkdir(parents=True, exist_ok=True)
			catalog.write_bytes(b"catalog sentinel\n")
			coverage.write_bytes(b"coverage sentinel\n")
			first = curator.generate(root)
			first_bytes = first.read_bytes()
			first_report = (root / curator.SPATIAL_REPORT_RELATIVE_PATH).read_bytes()
			self.assertEqual(root / curator.PARTIAL_RELATIVE_PATH, first)
			curator.check(root)
			curator.generate(root)
			self.assertEqual(first_bytes, first.read_bytes())
			self.assertEqual(first_report, (root / curator.SPATIAL_REPORT_RELATIVE_PATH).read_bytes())
			self.assertEqual((root / curator.SEED_RELATIVE_PATH).read_bytes(), first.read_bytes())
			self.assertEqual((root / curator.KNOWLEDGE_SEED_RELATIVE_PATH).read_bytes(), (root / curator.KNOWLEDGE_RELATIVE_PATH).read_bytes())
			self.assertEqual(b"catalog sentinel\n", catalog.read_bytes())
			self.assertEqual(b"coverage sentinel\n", coverage.read_bytes())

	def test_check_rejects_missing_or_modified_repository_excerpts(self) -> None:
		temporary, root, excerpt = _fixture_root()
		with temporary:
			curator.generate(root)
			excerpt.unlink()
			with self.assertRaisesRegex(RuntimeError, "excerpt"):
				curator.check(root)
			excerpt.write_text("changed fixture excerpt\n", encoding="utf-8")
			with self.assertRaisesRegex(RuntimeError, "excerpt"):
				curator.check(root)

	def test_check_rejects_generated_definition_drift(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			curator.generate(root)
			(root / curator.PARTIAL_RELATIVE_PATH).write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "definition drifted"):
				curator.check(root)

	def test_missing_and_malformed_seed_fail_closed(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			with self.assertRaisesRegex(RuntimeError, "machine seed is missing"):
				curator.build(root)
			path = root / curator.SEED_RELATIVE_PATH
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(b"{ this is not JSON }\n")
			with self.assertRaisesRegex(RuntimeError, "machine seed is malformed"):
				curator.build(root)

	def test_partial_seed_cannot_overwrite_an_author_ready_artifact(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			opposing = root / curator.AUTHOR_READY_RELATIVE_PATH
			opposing.parent.mkdir(parents=True, exist_ok=True)
			opposing.write_bytes(b"author-ready bytes\n")
			with self.assertRaisesRegex(RuntimeError, "author-ready Taxi artifact"):
				curator.generate(root)
			with self.assertRaisesRegex(RuntimeError, "stale opposing-status artifact"):
				curator.check(root)
			self.assertEqual(b"author-ready bytes\n", opposing.read_bytes())

	def test_retained_register_rejects_modified_evidence_and_wrong_source_root(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			vpx_root = root / "vpx"
			manuals_root = root / "manuals"
			review_root = root / "review"
			for directory in (vpx_root, manuals_root, review_root):
				directory.mkdir()
			table = vpx_root / "table.vpx"
			manifest = vpx_root / "table.manifest.json"
			manual = manuals_root / "manual.pdf"
			review = review_root / "geometry.json"
			table.write_bytes(b"vpx")
			manifest.write_bytes(b"manifest")
			manual.write_bytes(b"manual")
			review.write_bytes(b"review")
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, {"files": [
				{"root": "vpx", "path": "table.vpx", "size": table.stat().st_size, "sha256": _digest(table), "extraction_manifest": {"path": "table.manifest.json", "size": manifest.stat().st_size, "sha256": _digest(manifest)}},
				{"root": "manuals", "path": "manual.pdf", "size": manual.stat().st_size, "sha256": _digest(manual)},
				{"root": "review", "path": "geometry.json", "size": review.stat().st_size, "sha256": _digest(review)},
			]})
			curator.verify_retained(vpx_root, manuals_root, review_root, root=root)
			table.write_bytes(b"bad")
			with self.assertRaisesRegex(RuntimeError, "SHA-256 drifted"):
				curator.verify_retained(vpx_root, manuals_root, review_root, root=root)
			with self.assertRaisesRegex(RuntimeError, "readable vpx source root"):
				curator.verify_retained(root / "wrong-vpx-root", manuals_root, review_root, root=root)


class TaxiCatalogOwnershipTests(unittest.TestCase):
	def test_catalog_assigns_exactly_the_taxi_clone_tree(self) -> None:
		catalog = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
		owners = {entry["id"]: entry["machine_id"] for entry in catalog["drivers"] if entry["id"].startswith("taxi_")}
		self.assertEqual(curator.DRIVER_IDS, set(owners))
		self.assertEqual({curator.MACHINE_ID}, set(owners.values()))


class TaxiSeededDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = curator.build(ROOT)
		cls.switches = _by_binding(cls.definition, "inputs", curator.SWITCH_GROUP)
		cls.dips = _by_binding(cls.definition, "inputs", curator.DIP_GROUP)
		cls.solenoids = _by_binding(cls.definition, "outputs", curator.SOLENOID_GROUP)
		cls.lamps = _by_binding(cls.definition, "outputs", curator.LAMP_GROUP)

	def test_seed_and_generated_definition_are_byte_identical(self) -> None:
		self.assertTrue(DEFINITION_PATH.is_file(), "Taxi is expected to remain a partial unless the seed explicitly changes status")
		self.assertFalse(AUTHOR_READY_PATH.exists(), "a partial Taxi record must not retain an author-ready twin")
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())
		self.assertEqual(SEED_PATH.read_bytes(), DEFINITION_PATH.read_bytes())
		self.assertEqual(curator.knowledge_text(ROOT), KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_drivers_inputs_outputs_and_displays_match_the_settled_contract(self) -> None:
		self.assertEqual(curator.DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual(77, len(self.definition["inputs"]))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual(114, len(self.definition["outputs"]))
		self.assertEqual([7, 16, 16], sorted(display["width"] for display in self.definition["displays"] if display["kind"] == "segment"))

	def test_flipper_column_copies_and_synthetic_outputs_are_explicit(self) -> None:
		self.assertEqual("pinmame.system-11", self.definition["controller"]["platform"])
		self.assertEqual("used", self.switches[82]["availability"])
		self.assertEqual("used", self.switches[84]["availability"])
		pairs = {(item["source"], item["destination"]) for item in self.definition["relationships"] if item["kind"] == "direct"}
		self.assertIn((self.switches[82]["id"], self.switches[57]["id"]), pairs)
		self.assertIn((self.switches[84]["id"], self.switches[58]["id"]), pairs)
		self.assertEqual({45, 46, 47, 48}, {address for address, device in self.solenoids.items() if device["kind"] == "virtual" and device["availability"] == "used"})

	def test_drop_inputs_mux_feedback_and_physical_population_stay_distinct(self) -> None:
		for address in range(27, 33):
			self.assertFalse(self.switches[address]["normally_closed"])
		self.assertEqual("virtual", self.switches[2]["kind"])
		self.assertNotIn("physical", self.switches[2])
		pairs = {(x["source"], x["destination"]) for x in self.definition["relationships"] if x["kind"] == "direct"}
		self.assertIn((self.solenoids[12]["id"], self.switches[2]["id"]), pairs)
		self.assertEqual(3, self.solenoids[15]["physical"]["quantity"])
		self.assertEqual(2, self.solenoids[32]["physical"]["quantity"])
		self.assertNotIn("quantity", self.lamps[1]["physical"])
		self.assertEqual("unknown", next(x for x in self.definition["drivers"] if x["id"] == "taxi_p5")["physical_compatibility"])
		self.assertEqual({"spatial_placement", "variant_differences", "output_semantics", "unresolved_conflicts"}, set(self.definition["coverage"]["missing"]))
		self.assertEqual(3, len(self.definition["conflicts"]))
		self.assertTrue(all(x["status"] == "unresolved" for x in self.definition["conflicts"]))
		self.assertNotIn("drive_connection", self.solenoids[14]["wiring"])
		self.assertNotIn("drive_connection", self.solenoids[17]["wiring"])
		self.assertNotIn("quantity", self.solenoids[16]["physical"])
		self.assertEqual("conflicted", self.solenoids[16]["provenance"]["status"])

	def test_a_status_edit_cannot_promote_the_unresolved_candidate(self) -> None:
		definition = json.loads(json.dumps(self.definition))
		definition["coverage"]["status"] = "author_ready"
		definition["coverage"]["missing"] = []
		errors = curator._validation_errors(definition)
		self.assertTrue(errors, "unknown prototype and incomplete physical/spatial evidence must block promotion")

	def test_rom_excerpt_coil_indices_are_complete_and_not_public_address_guesses(self) -> None:
		text = (ROOT / "evidence/excerpts/williams.taxi.1988/rom-tables.md").read_text(encoding="utf-8")
		self.assertNotIn("| None |", text)
		for section in text.split("## taxi_")[1:]:
			coil = section.split("| Coil service index |", 1)[1]
			indices = [int(line.split("|")[1].strip()) for line in coil.splitlines() if line.startswith("| ") and line.split("|")[1].strip().isdigit()]
			self.assertEqual(list(range(1, 31)), indices)

	def test_check_and_spatial_artifacts_are_seed_deterministic(self) -> None:
		curator.check(ROOT)
		report = curator.build_spatial_report(self.definition)
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))
		self.assertEqual(self.definition["coverage"]["missing"], report["coverage"]["missing"])
		self.assertIn("located_devices", report)
		self.assertIn("unplaced_physical_devices", report)
		self.assertIn("not_applicable_devices", report)
		self.assertIn("source_hashes", report)


@unittest.skipUnless(
	EVIDENCE_BINDING_PATH.is_file()
	and os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	and os.environ.get("PINMAME_MANUALS_ROOT")
	and os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"),
	"Taxi external evidence binding register or configured evidence roots are not present",
)
class TaxiRetainedEvidenceTests(unittest.TestCase):
	def test_external_evidence_register_matches_read_only_roots(self) -> None:
		curator.verify_retained(
			Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]),
			Path(os.environ["PINMAME_MANUALS_ROOT"]),
			Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]),
		)

	def test_runtime_summary_is_derived_from_successful_pinned_runs(self) -> None:
		runtime_evidence.check(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))

	def test_wrong_drop_response_or_missing_core_copy_blocks_runtime_summary(self) -> None:
		from unittest.mock import patch
		review_root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		original_load = runtime_evidence._load_run
		for mismatch in ("drop release", "cabinet copy"):
			def altered(path: Path, scenario: Path) -> dict:
				run = original_load(path, scenario)
				if path.name == "l4-labels-v3.json":
					if mismatch == "drop release":
						active = next(x for x in run["snapshots"] if x["label"] == "switch 27 active stimulus")
						release = next(x for x in run["snapshots"] if x["label"] == "switch 27 release stimulus")
						release["displays"] = active["displays"]
					else:
						held = next(x for x in run["snapshots"] if x["label"] == "right cabinet flipper column stimulus (held)")
						for switch in held["watched_switches"]:
							if switch["number"] == 57:
								switch["state"] = 0
				return run
			with self.subTest(mismatch=mismatch), patch.object(runtime_evidence, "_load_run", altered):
				with self.assertRaises(ValueError):
					runtime_evidence.build(review_root)

	def test_spatial_anchors_recompute_with_the_repository_helper(self) -> None:
		from pinmame_game_defs.spatial import extract_spatial_candidates
		base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/taxi/Taxi (Williams 1988)1.2"
		actual = extract_spatial_candidates(base / "extraction-vpxtool-git-v0.33.3", base / "Taxi (Williams 1988)1.2.vpx", "git:v0.33.3")
		points = {x["name"]: (x["x"], x["y"]) for x in actual["objects"]}
		definition = curator.build(ROOT)
		names = {13: "JoyrideEject", 17: "Bumper1", 19: "Bumper2", 21: "Bumper3", 24: "sw24", 35: "Catapult", 36: "RightLock"}
		for device in definition["inputs"]:
			if device["binding"]["device"] in names and device["binding"]["group"] == curator.SWITCH_GROUP:
				placement = device["spatial"]["placements"][0]
				self.assertEqual(points[names[device["binding"]["device"]]], (placement["x"], placement["y"]))


class TaxiRuntimeDecoderTests(unittest.TestCase):
	def test_decimal_alternate_one_and_unknown_patterns_are_preserved(self) -> None:
		self.assertEqual("I.1?", runtime_evidence.alpha_text([0xA209, 0x0006, 0x7FFF]))

	def test_failed_wrong_binary_and_wrong_scenario_runs_fail_closed(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			scenario = root / "scenario.json"
			scenario.write_bytes(b"scenario")
			run = root / "run.json"
			valid = {"failure": None, "game": "taxi_l4", "library_sha256": runtime_evidence.LIBRARY_SHA256,
				"scenario": {"sha256": _digest(scenario)}}
			for field, replacement, message in [("failure", {"message": "failed"}, "successful"),
				("library_sha256", "0" * 64, "binary"), ("scenario", {"sha256": "0" * 64}, "Scenario")]:
				_write_json(run, {**valid, field: replacement})
				with self.assertRaisesRegex(ValueError, message):
					runtime_evidence._load_run(run, scenario)


if __name__ == "__main__":
	unittest.main()
