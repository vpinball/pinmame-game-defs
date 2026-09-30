"""Determinism and fail-closed contracts for the seed-owned Taxi curator."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_taxi as curator
import taxi_runtime_evidence as runtime_evidence
from build_external_evidence_manifest import write_manifest
from pinmame_game_defs.jsonio import canonical_bytes
from pinmame_game_defs.schema_validation import validate_against_schema


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
			"kind": "virtual" if address == 2 else "switch",
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


# Literal alpha and numeric arrays extracted from the successful retained
# l4-labels-v3 snapshots. The numeric decoder is deliberately exercised only
# at positions 4 and 5; all other raw numeric cells remain uninterpreted.
DROP_ACTIVE_SEGMENTS = {
	27: {
		"alpha": [0, 0, 0, 56, 63, 56, 2167, 0, 0, 56, 121, 113, 8705, 0, 0, 0],
		"numeric": [0, 63, 7, 0, 91, 7, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
	28: {
		"alpha": [0, 0, 0, 56, 63, 56, 2167, 0, 0, 1334, 8713, 8719, 8719, 56, 121, 0],
		"numeric": [0, 63, 7, 0, 91, 127, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
	29: {
		"alpha": [0, 0, 0, 56, 63, 56, 2167, 0, 0, 6259, 8713, 2109, 2166, 8705, 0, 0],
		"numeric": [0, 63, 7, 0, 91, 111, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
	30: {
		"alpha": [0, 0, 2163, 8713, 4406, 10767, 63, 8705, 0, 8705, 63, 2163, 0, 0, 0, 0],
		"numeric": [0, 63, 7, 0, 79, 63, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
	31: {
		"alpha": [0, 2163, 8713, 4406, 10767, 63, 8705, 0, 1334, 8713, 8719, 8719, 56, 121, 0, 0],
		"numeric": [0, 63, 7, 0, 79, 6, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
	32: {
		"alpha": [0, 2163, 8713, 4406, 10767, 63, 8705, 0, 10767, 63, 8705, 8705, 63, 1334, 0, 0],
		"numeric": [0, 63, 7, 0, 79, 91, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128],
	},
}
DROP_RELEASE_ALPHA_SEGMENTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
DROP_RELEASE_NUMERIC_SEGMENTS = [0, 63, 7, 0, 0, 0, 0, 0, 0, 0, 27904, 16128, 48896, 16128, 16128, 16128]


def _drop_response_fixture() -> dict:
	snapshots = []
	for address, segments in DROP_ACTIVE_SEGMENTS.items():
		snapshots.extend([
			{
				"label": f"switch {address} active stimulus",
				"displays": [
					{"index": 0, "segments": list(segments["alpha"])},
					{"index": 1, "segments": list(segments["numeric"])},
				],
			},
			{
				"label": f"switch {address} release stimulus",
				"displays": [
					{"index": 0, "segments": list(DROP_RELEASE_ALPHA_SEGMENTS)},
					{"index": 1, "segments": list(DROP_RELEASE_NUMERIC_SEGMENTS)},
				],
			},
		])
	return {"snapshots": snapshots}


def _fixture_display(run: dict, label: str, display_index: int) -> dict:
	snapshot = next(item for item in run["snapshots"] if item["label"] == label)
	return next(display for display in snapshot["displays"] if display["index"] == display_index)


class TaxiFixtureCuratorTests(unittest.TestCase):
	def test_matrix_two_cannot_be_reclassified_as_a_physical_switch(self) -> None:
		temporary, root, _excerpt = _fixture_root()
		with temporary:
			seed_path = root / curator.SEED_RELATIVE_PATH
			definition = json.loads(seed_path.read_bytes())
			matrix_two = next(item for item in definition["inputs"] if item["binding"] == {"group": curator.SWITCH_GROUP, "device": 2})
			matrix_two["kind"] = "switch"
			_write_json(seed_path, definition)
			with self.assertRaisesRegex(RuntimeError, "matrix switch 2 must remain a virtual mux-feedback input"):
				curator.build(root)

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
		for source, target in ((82, 57), (84, 58)):
			self.assertEqual({self.switches[target]["id"]}, {destination for origin, destination in pairs if origin == self.switches[source]["id"]})
		self.assertEqual({45, 46, 47, 48}, {address for address, device in self.solenoids.items() if device["kind"] == "virtual" and device["availability"] == "used"})

	def test_factory_gi_relays_have_separate_physical_locations(self) -> None:
		insert = self.solenoids[10]
		playfield = self.solenoids[11]
		self.assertEqual("backbox / insert board", insert["physical"]["location"])
		self.assertEqual("cabinet_or_service", insert["spatial"]["reason"])
		self.assertEqual("playfield / underplayfield", playfield["physical"]["location"])
		self.assertEqual("internal_nonvisual", playfield["spatial"]["reason"])
		for relay in (insert, playfield):
			self.assertEqual("relay", relay["kind"])
			self.assertEqual("5580-12145-01", relay["physical"]["part_number"])
			self.assertIn("manual.taxi", relay["provenance"]["source_refs"])
			self.assertIn("manual.taxi", relay["spatial"]["provenance"]["source_refs"])
		wiring = (ROOT / "evidence/excerpts/williams.taxi.1988/solenoid-wiring.md").read_text(encoding="utf-8")
		self.assertIn("| 11 | Playfield Gen Illum | Controlled |", wiring)
		self.assertEqual("Playfield Gen Illum", playfield["label"])
		# PDF 60 uses a different literal abbreviation from PDF 72.
		locations = (ROOT / "evidence/excerpts/williams.taxi.1988/coil-locations.md").read_text(encoding="utf-8")
		self.assertIn("| 10 | 5580-12145-01 | Insert Bd Gen Illumin Relay * |", locations)
		self.assertIn("| 11 | 5580-12145-01 | Playfield Gen Illumin Relay * |", locations)

	def test_unfitted_special_output_is_grounded_in_the_factory_row(self) -> None:
		output = self.solenoids[22]
		self.assertEqual("unused", output["availability"])
		self.assertEqual("unused", output["spatial"]["reason"])
		self.assertIn("manual.taxi", output["provenance"]["source_refs"])
		self.assertIn("manual.taxi", output["spatial"]["provenance"]["source_refs"])
		self.assertNotIn("physical", output)
		text = (ROOT / "evidence/excerpts/williams.taxi.1988/solenoid-wiring.md").read_text(encoding="utf-8")
		row = next(line for line in text.splitlines() if line.startswith("| 22 |"))
		cells = [cell.strip() for cell in row.split("|")[1:-1]]
		self.assertEqual(["22", "Not Used", "Special #6", "Blu-Blk", "1P19-9", "5J3-1: 5J7-1", "Q79", "[blank]"], cells)
		for field, value in zip(("drive_wire", "control_connection", "drive_connection", "driver_transistor"), cells[3:7]):
			self.assertEqual(value, output["wiring"][field])
		for address in range(17, 23):
			row = next(line for line in text.splitlines() if line.startswith(f"| {address} |"))
			self.assertEqual(f"Special #{address - 16}", row.split("|")[3].strip())
		self.assertIn("[7P1-19,2J18-5:2J17-3]", text)

	def test_ac_guidance_matches_factory_selection_and_public_routing(self) -> None:
		for address in range(1, 9):
			with self.subTest(address=address):
				output = self.solenoids[address]
				note = output["physical"]["notes"]
				self.assertRegex(note, r"A-side.*relay 12.*de-energized")
				self.assertRegex(note, r"PinMAME.*separates.*A 1\.\.8.*C 25\.\.32")
				self.assertEqual("coil", output["kind"])
				self.assertIn("(A)", output["wiring"]["drive_connection"])
				self.assertEqual("flasher", self.solenoids[address + 24]["kind"])
				self.assertIn("(C)", self.solenoids[address + 24]["wiring"]["drive_connection"])
		for address in (9, 10, 11, 12, 13, 14, 18, 20):
			self.assertNotRegex(self.solenoids[address]["physical"]["notes"], r"A/C switched outputs require relay")

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

	def test_physical_target_order_and_projection_authorities_are_preserved(self) -> None:
		middle = [self.switches[address]["spatial"]["placements"][0] for address in (27, 28, 29)]
		self.assertLess(middle[0]["x"], middle[1]["x"])
		self.assertLess(middle[1]["x"], middle[2]["x"])
		self.assertEqual(["sw29", "sw28", "sw27"], [p["id"].split(".")[-1] for p in middle])
		for address in range(27, 33):
			self.assertIn("opto", self.switches[address]["physical"]["notes"])
			self.assertIn("recreation face anchor", self.switches[address]["physical"]["notes"])
		for address in (33, 34):
			placement = self.switches[address]["spatial"]["placements"][0]
			self.assertIn("vpx.taxi.world-mesh", placement["provenance"]["source_refs"])
			self.assertIn("world-space mesh bounds center", self.switches[address]["physical"]["notes"])
		for device in self.definition["inputs"] + self.definition["outputs"]:
			for placement in device.get("spatial", {}).get("placements", []):
				self.assertIn("manual.taxi", placement["provenance"]["source_refs"])
				self.assertIn("vpx.taxi.script", placement["provenance"]["source_refs"])
		self.assertEqual(3, len(self.definition["conflicts"]))
		self.assertIn("consumed-table defect", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_stable_source_times_and_ipdb_resource_identity_are_explicit(self) -> None:
		from datetime import datetime
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source in sources.values():
			self.assertIsNotNone(datetime.fromisoformat(source["acquired_at"]).tzinfo, source["id"])
		self.assertEqual("2505", sources["identity.taxi"]["source_id"])
		self.assertEqual("https://www.ipdb.org/machine.cgi?id=2505", sources["identity.taxi"]["uri"])
		self.assertEqual("2026-09-30T11:21:58.4931020Z", sources["identity.taxi"]["acquired_at"])
		self.assertEqual("2026-09-30T11:13:01.2008451Z", sources["vpx.taxi.table"]["acquired_at"])
		for identifier in ("manual.taxi", "manual.taxi.schematics", "manual.taxi.preliminary", "bulletins.taxi"):
			self.assertEqual("2505", sources[identifier]["source_id"])
			self.assertTrue(sources[identifier]["uri"].endswith(sources[identifier]["original_filename"]))
		self.assertIn("CreationTimeUtc", sources["vpx.taxi.world-mesh"]["locator"])

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
		names = {
			13: "JoyrideEject", 14: "sw14", 15: "sw15", 16: "sw16", 17: "Bumper1",
			19: "Bumper2", 21: "Bumper3", 23: "sw23", 24: "sw24", 25: "sw25", 26: "sw26",
			27: "sw29", 28: "sw28", 29: "sw27", 30: "sw30", 31: "sw31", 32: "sw32",
			35: "Catapult", 36: "RightLock", 37: "sw37", 38: "sw38", 39: "sw39", 40: "sw40",
		}
		for device in definition["inputs"]:
			if device["binding"]["device"] in names and device["binding"]["group"] == curator.SWITCH_GROUP:
				placement = device["spatial"]["placements"][0]
				self.assertEqual(points[names[device["binding"]["device"]]], (placement["x"], placement["y"]))
		effects = {3: "Catapult", 4: "sw28", 5: "JoyrideEject", 6: "sw31", 7: "SpinoutKicker", 8: "RightLock", 9: "TopGate", 17: "Bumper1", 19: "Bumper2", 21: "Bumper3"}
		for device in definition["outputs"]:
			if device["binding"]["group"] == curator.SOLENOID_GROUP and device["binding"]["device"] in effects:
				placement = device["spatial"]["placements"][0]
				self.assertEqual(points[effects[device["binding"]["device"]]], (placement["x"], placement["y"]))

	def test_ramp_wire_world_centers_and_independent_frame_controls(self) -> None:
		from pinmame_game_defs.spatial import _round_point
		base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/taxi/Taxi (Williams 1988)1.2/extraction-vpxtool-git-v0.33.3"
		export = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "taxi-1988/followup-1/luna-inventory/vpxtool-obj-vpu/Taxi (Williams 1988)1.2.obj"
		self.assertEqual("dfb0965ef597f88e5c94bcb63cfbb6532a57394e15993707fe88a2dc6dc50cce", _digest(export))
		names = {"sw14", "sw15", "sw16", "sw27", "sw28", "sw29", "sw30", "sw31", "sw32", "sw33P", "sw34P"}
		vertices: dict[str, list[tuple[float, ...]]] = {name: [] for name in names}
		name = ""
		with export.open(encoding="utf-8") as stream:
			for line in stream:
				if line.startswith("o "):
					name = line[2:].strip()
				elif line.startswith("v ") and name in vertices:
					vertices[name].append(tuple(map(float, line.split()[1:])))
		centers = {name: [(min(v[axis] for v in points) + max(v[axis] for v in points)) / 2 for axis in range(2)] for name, points in vertices.items()}
		for name in sorted(names - {"sw33P", "sw34P"}):
			kind = "Trigger" if name in {"sw14", "sw15", "sw16"} else "HitTarget"
			obj = json.loads((base / "gameitems" / f"{kind}.{name}.json").read_bytes())[kind]
			point = obj["center" if kind == "Trigger" else "position"]
			self.assertAlmostEqual(point["x"], centers[name][0], delta=0.05)
			self.assertAlmostEqual(point["y"], centers[name][1], delta=0.05)
		switches = _by_binding(curator.build(ROOT), "inputs", curator.SWITCH_GROUP)
		for address in (33, 34):
			placement = switches[address]["spatial"]["placements"][0]
			center = centers[f"sw{address}P"]
			self.assertEqual((_round_point(center[0] / 952), _round_point(center[1] / 1974)), (placement["x"], placement["y"]))

	def test_manual_acquisition_times_match_retained_manifest(self) -> None:
		manifest = json.loads((Path(os.environ["PINMAME_MANUALS_ROOT"]) / "manifest.json").read_bytes())
		retained = {entry["sha256"]: entry for entry in manifest["documents"] if entry.get("machine_id") == curator.MACHINE_ID}
		for source in curator.build(ROOT)["sources"]:
			if source["sha256"] in retained:
				entry = retained[source["sha256"]]
				self.assertEqual(entry["acquired_at"], source["acquired_at"])
				self.assertEqual(entry["source_id"], source["source_id"])
				self.assertEqual(entry["download_url"], source["uri"])


class TaxiRuntimeDecoderTests(unittest.TestCase):
	def test_extracted_drop_snapshots_prove_exact_names_and_numeric_addresses(self) -> None:
		run = _drop_response_fixture()
		for address, expected_label in runtime_evidence.DROP_SENSOR_LABELS.items():
			with self.subTest(address=address):
				observation = runtime_evidence.verify_drop_response(run, address)
				self.assertEqual([], observation["observed_switch_addresses"])
				self.assertEqual([address], observation["host_stimulus_switch_addresses"])
				self.assertEqual([0, 1, 0, 1], [response["display_index"] for response in observation["display_responses"]])
				active_alpha, active_numeric, release_alpha, release_numeric = observation["display_responses"]
				self.assertEqual(expected_label, active_alpha["interpreted_text"])
				self.assertEqual(list(range(16)), active_alpha["decoded_segment_positions"])
				self.assertEqual(DROP_ACTIVE_SEGMENTS[address]["alpha"], active_alpha["segments"])
				self.assertEqual(runtime_evidence.NUMERIC_ADDRESS_POSITIONS, active_numeric["decoded_segment_positions"])
				self.assertEqual(str(address), active_numeric["interpreted_text"])
				self.assertEqual(address, active_numeric["diagnostic_address"])
				self.assertEqual(DROP_ACTIVE_SEGMENTS[address]["numeric"], active_numeric["segments"])
				self.assertEqual("", release_alpha["interpreted_text"])
				self.assertEqual(DROP_RELEASE_ALPHA_SEGMENTS, release_alpha["segments"])
				self.assertEqual("", release_numeric["interpreted_text"])
				self.assertNotIn("diagnostic_address", release_numeric)
				self.assertEqual(DROP_RELEASE_NUMERIC_SEGMENTS, release_numeric["segments"])

	def test_recognized_wrong_drop_name_is_rejected(self) -> None:
		run = _drop_response_fixture()
		_fixture_display(run, "switch 27 active stimulus", 0)["segments"] = list(DROP_ACTIVE_SEGMENTS[28]["alpha"])
		with self.assertRaisesRegex(ValueError, "active alpha label"):
			runtime_evidence.verify_drop_response(run, 27)

	def test_wrong_numeric_diagnostic_address_is_rejected(self) -> None:
		run = _drop_response_fixture()
		_fixture_display(run, "switch 27 active stimulus", 1)["segments"] = list(DROP_ACTIVE_SEGMENTS[28]["numeric"])
		with self.assertRaisesRegex(ValueError, "observed numeric address 28"):
			runtime_evidence.verify_drop_response(run, 27)

	def test_unknown_numeric_pattern_and_decimal_diagnostic_are_rejected(self) -> None:
		for glyph, digit in ((0x3F, "0"), (0x06, "1"), (0x5B, "2"), (0x4F, "3"), (0x66, "4"),
			(0x6D, "5"), (0x7D, "6"), (0x07, "7"), (0x7F, "8"), (0x6F, "9")):
			with self.subTest(glyph=glyph):
				self.assertEqual(digit * 2, runtime_evidence.numeric_text([0, 0, 0, 0, glyph, glyph]))
		self.assertEqual("2.7", runtime_evidence.numeric_text([0, 0, 0, 0, 0xDB, 0x07]))
		for value, message in ((0x01, "Unrecognized numeric"), (0xDB, "decimal attribute")):
			run = _drop_response_fixture()
			_fixture_display(run, "switch 27 active stimulus", 1)["segments"][4] = value
			with self.subTest(value=value), self.assertRaisesRegex(ValueError, message):
				runtime_evidence.verify_drop_response(run, 27)

	def test_stale_release_and_unknown_alpha_pattern_are_rejected(self) -> None:
		self.assertEqual("I.1", runtime_evidence.alpha_text([0xA209, 0x0006]))
		with self.assertRaisesRegex(ValueError, "Unrecognized alpha"):
			runtime_evidence.alpha_text([0x7FFF])
		run = _drop_response_fixture()
		_fixture_display(run, "switch 27 release stimulus", 0)["segments"] = list(DROP_ACTIVE_SEGMENTS[27]["alpha"])
		with self.assertRaisesRegex(ValueError, "release alpha label is stale"):
			runtime_evidence.verify_drop_response(run, 27)

	def test_segment_response_schema_accepts_both_named_action_locations_and_rejects_bad_segments(self) -> None:
		observation = runtime_evidence.verify_drop_response(_drop_response_fixture(), 27)
		global_observation = deepcopy(observation)
		global_observation["active_solenoid_addresses"] = []
		global_observation["transitioned_solenoid_addresses"] = []
		payload = {
			"format": "pinmame-machine-evidence",
			"version": 1,
			"extractor": {"id": "fixture", "version": 1},
			"source": {
				"kind": "runtime_scenario", "repository": "test://taxi", "revision": "0" * 40,
				"path": "fixture", "sha256": "0" * 64, "license": "test-only", "quality": "observed",
			},
			"driver_ids": ["taxi_l4"], "machine_ids": [curator.MACHINE_ID],
			"switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
			"runtime": {
				"game": "taxi_l4", "rom_archive_sha256": "0" * 64,
				"raw_runs": [{"name": "l4-labels-v3", "sha256": "0" * 64, "self_test_pulses": 0}],
				"command_template": "fixture",
				"observations": {
					"named_action_observations": [global_observation],
					"runs": {"l4-labels-v3": {"named_action_observations": [observation]}},
				},
			},
		}
		schema_path = ROOT / "schemas/evidence.schema.json"
		self.assertEqual([], validate_against_schema(payload, schema_path, "Taxi segment-response fixture"))
		invalid = deepcopy(payload)
		invalid["runtime"]["observations"]["runs"]["l4-labels-v3"]["named_action_observations"][0]["display_responses"][0]["segments"][0] = 65536
		self.assertTrue(validate_against_schema(invalid, schema_path, "Taxi invalid segment-response fixture"))

	def test_failed_wrong_binary_and_wrong_scenario_runs_fail_closed(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			scenario = root / "scenario.json"
			scenario.write_bytes(b"scenario")
			run = root / "run.json"
			valid = {"failure": None, "game": "taxi_l4", "library_sha256": runtime_evidence.LIBRARY_SHA256,
				"scenario": {"sha256": _digest(scenario)}}
			for field, replacement, message in [("failure", {"message": "failed"}, "successful"),
				("library_sha256", "0" * 64, "binary"),
				("library_sha256", "ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d", "binary"),
				("scenario", {"sha256": "0" * 64}, "Scenario")]:
				_write_json(run, {**valid, field: replacement})
				with self.assertRaisesRegex(ValueError, message):
					runtime_evidence._load_run(run, scenario)


if __name__ == "__main__":
	unittest.main()
