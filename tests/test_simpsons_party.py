from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "the-simpsons-pinball-party-2003.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "the-simpsons-pinball-party-2003.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-simpsons-pinball-party-2003.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "the-simpsons-pinball-party-2003.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "whitestar.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "the-simpsons-pinball-party-2003.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "stern" / "the-simpsons-pinball-party-2003.md"

DRIVER_IDS = {
	"simpprty", "simpprtf", "simpprtg", "simpprti", "simpprtl",
	"simp400", "simp400f", "simp400g", "simp400i", "simp400l",
	"simp300", "simp300f", "simp300i", "simp300l",
	"simp204", "simp204f", "simp204i", "simp204l",
}
MATRIX_ADDRESSES = {(column - 1) * 8 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {27, 28}
OPTO_ADDRESSES = {14, 15}
DEDICATED_ADDRESSES = {84, 83, 82, 81, 88, -2, -1, 0}
LAMP_ADDRESSES = {(row - 1) * 8 + column for column in range(1, 9) for row in range(1, 11)}
UNUSED_LAMP_ADDRESSES = {71, 72}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def _run_curator_without_mode() -> None:
	"""Invoke the curator's CLI with no mode so argparse rejects it instead of writing files."""
	import curate_simpsons_party as curator

	argv = sys.argv
	sys.argv = ["curate_simpsons_party.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class SimpsonsPartyDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			["polarity", "output_enumeration", "spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in ("physical_wiring", "spatial_placement"):
				continue
			self.assertEqual("validated", state, dimension)
		self.assertEqual("stern.the-simpsons-pinball-party.2003", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(4674, self.definition["machine"]["ipdb_id"])
		self.assertEqual(2003, self.definition["machine"]["year"])
		self.assertEqual("Stern", self.definition["machine"]["manufacturer"])
		self.assertEqual({"width": 952.0, "height": 2115.0, "units": "vpx"}, self.definition["machine"]["playfield"])
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		self.assertEqual("0x4000000000", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_two_conflicts_are_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{"conflict.whitestar-invsw-never-populated", "conflict.upper-flipper-button-not-read"},
			set(conflicts),
		)
		for conflict in conflicts.values():
			self.assertGreaterEqual(len(conflict["source_refs"]), 2)
			self.assertIn("unresolved", conflict["description"].lower())
		self.assertIn("88", conflicts["conflict.upper-flipper-button-not-read"]["path"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_simpprty_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
			self.assertEqual("Stern", driver["manufacturer"])
			self.assertEqual("2003", driver["year"])
		self.assertEqual(1, len([d for d in self.definition["drivers"] if d["id"] == "simpprty" and "clone_of" not in d]))

	def test_the_full_whitestar_switch_matrix_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | DEDICATED_ADDRESSES | {-3}
		self.assertEqual(expected, set(self.switches) | set(self.dips))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"])
			self.assertEqual({"status": "not_applicable", "reason": "unused", "provenance": self.switches[address]["spatial"]["provenance"]}, self.switches[address]["spatial"])
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertIn(self.switches[address]["availability"], {"used", "optional"}, address)

	def test_opto_switches_are_flagged_but_not_pinmame_normalized(self) -> None:
		for address in OPTO_ADDRESSES:
			switch = self.switches[address]
			self.assertEqual("opto", switch["physical"]["switch_type"])
			self.assertTrue(switch["normally_closed"])
			self.assertIn("conflict.whitestar-invsw-never-populated", switch["physical"]["notes"])
		for address, switch in self.switches.items():
			if address in OPTO_ADDRESSES or address in UNUSED_MATRIX_ADDRESSES:
				continue
			if switch.get("physical", {}).get("switch_type") == "opto":
				self.fail(f"switch {address} unexpectedly typed opto")

	def test_dedicated_switches_and_memory_protect(self) -> None:
		for address in DEDICATED_ADDRESSES:
			self.assertIn(address, self.switches)
		self.assertIn(-3, self.switches)
		self.assertEqual("Coin Door Memory Protect Interlock", self.switches[-3]["label"])
		ds5 = self.switches[88]
		self.assertEqual("unused", ds5["availability"])
		self.assertIn("conflict.upper-flipper-button-not-read", ds5["physical"]["notes"])
		self.assertEqual({"status": "not_applicable", "reason": "cabinet_or_service", "provenance": ds5["spatial"]["provenance"]}, ds5["spatial"])
		for address in (84, 83, 82, 81, -2, -1, 0):
			self.assertEqual("used", self.switches[address]["availability"])

	def test_upper_and_top_right_flipper_solenoids_have_no_switch_binding(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		trio = mechanisms["mechanism.upper-and-top-right-flippers"]
		self.assertEqual([], trio["sensors"])
		self.assertEqual(3, len(trio["actuators"]))

	def test_flipper_power_hold_mapping_matches_pinned_source(self) -> None:
		right_power = self.solenoids[45]
		right_hold = self.solenoids[46]
		left_power = self.solenoids[47]
		left_hold = self.solenoids[48]
		for device in (right_power, right_hold):
			self.assertEqual("16", next(a["value"] for a in device["aliases"] if a["namespace"] == "manual.address"))
		for device in (left_power, left_hold):
			self.assertEqual("15", next(a["value"] for a in device["aliases"] if a["namespace"] == "manual.address"))
		self.assertIn(15, self.solenoids)
		self.assertIn(16, self.solenoids)
		self.assertEqual("unused", self.solenoids[15]["availability"])
		self.assertEqual("unused", self.solenoids[16]["availability"])
		self.assertEqual("virtual", self.solenoids[15]["kind"])

	def test_the_full_solenoid_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		flashers = {21, 22, 23, 25, 26, 27, 28, 29, 31, 32}
		for address in flashers:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		self.assertEqual("optional", self.solenoids[24]["availability"])
		for address in (33, 34, 35):
			self.assertEqual("optional", self.solenoids[address]["availability"], address)
			self.assertEqual({"status": "not_applicable", "reason": "unused", "provenance": self.solenoids[address]["spatial"]["provenance"]}, self.solenoids[address]["spatial"])
		for address in (36, 37, 38, 39, 40, 41, 42, 43, 44, 50):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		self.assertEqual("unused", self.solenoids[49]["availability"])
		self.assertEqual({"status": "not_applicable", "reason": "virtual", "provenance": self.solenoids[49]["spatial"]["provenance"]}, self.solenoids[49]["spatial"])

	def test_the_full_lamp_matrix_is_enumerated(self) -> None:
		self.assertEqual(LAMP_ADDRESSES, set(self.lamps))
		for address in UNUSED_LAMP_ADDRESSES:
			self.assertEqual("unused", self.lamps[address]["availability"])
		self.assertEqual("optional", self.lamps[32]["availability"])
		self.assertEqual("not_applicable", self.lamps[32]["spatial"]["status"])
		for address in range(73, 81):
			self.assertEqual("used", self.lamps[address]["availability"], address)
			self.assertNotIn("spatial", self.lamps[address], f"lamp {address} must omit spatial rather than fabricate it")
		self.assertEqual(2, self.lamps[16]["physical"]["quantity"])
		self.assertEqual(2, self.lamps[80]["physical"]["quantity"])

	def test_gi_is_a_single_aggregate_channel(self) -> None:
		self.assertEqual({0}, set(self.gi))
		gi = self.gi[0]
		self.assertEqual("validated", gi["spatial"]["status"])
		self.assertEqual(42, len(gi["spatial"]["placements"]))
		self.assertEqual(42, gi["physical"]["quantity"])

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen_ids: set[str] = set()
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				spatial = device.get("spatial")
				if spatial is None or spatial["status"] == "not_applicable":
					continue
				self.assertEqual("validated", spatial["status"], device["id"])
				for placement in spatial["placements"]:
					self.assertNotIn(placement["id"], seen_ids, placement["id"])
					seen_ids.add(placement["id"])
					self.assertGreaterEqual(placement["x"], 0.0)
					self.assertLessEqual(placement["x"], 1.0)
					self.assertGreaterEqual(placement["y"], 0.0)
					self.assertLessEqual(placement["y"], 1.0)

	def test_geometric_ordering_regression_assertions(self) -> None:
		# Left/right flippers: left flipper must sit left of right flipper.
		left_flipper_x = self.solenoids[47]["spatial"]["placements"][0]["x"]
		right_flipper_x = self.solenoids[45]["spatial"]["placements"][0]["x"]
		self.assertLess(left_flipper_x, right_flipper_x)
		# Outlanes/return lanes: left-named switches sit left of right-named switches.
		self.assertLess(self.switches[57]["spatial"]["placements"][0]["x"], self.switches[60]["spatial"]["placements"][0]["x"])
		self.assertLess(self.switches[58]["spatial"]["placements"][0]["x"], self.switches[61]["spatial"]["placements"][0]["x"])
		# Slingshots: left slingshot left of right slingshot.
		self.assertLess(self.switches[59]["spatial"]["placements"][0]["x"], self.switches[62]["spatial"]["placements"][0]["x"])
		# Jet bumpers: switch identity agrees with the manual name for each bumper's own position.
		left_bumper_x = self.switches[49]["spatial"]["placements"][0]["x"]
		right_bumper_x = self.switches[50]["spatial"]["placements"][0]["x"]
		self.assertLess(left_bumper_x, right_bumper_x)
		# Rear/front: trough (rear-ish, near drain at high y) sits further front (higher y) than
		# the upper playfield standups (low y, near the backglass end).
		self.assertGreater(self.switches[10]["spatial"]["placements"][0]["y"], self.switches[35]["spatial"]["placements"][0]["y"])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		actuator_ids = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		for address, solenoid in self.solenoids.items():
			if solenoid["kind"] not in ("coil", "motor"):
				continue
			if solenoid["availability"] != "used":
				continue
			if address in (45, 46, 47, 48):
				continue  # covered by mechanism.lower-flippers as a group, not per-address alias.
			if address == 2:
				continue  # Auto Launch is a standalone coil (plungerIM.AutoFire); no additional topology to document.
			self.assertIn(solenoid["id"], actuator_ids, f"solenoid {address} ({solenoid['label']}) has no mechanism")

	def test_relationships_use_proven_causality_only(self) -> None:
		self.assertEqual(1, len(self.definition["relationships"]))
		relationship = self.definition["relationships"][0]
		self.assertEqual("pulse", relationship["kind"])

	def test_display_inventory_is_the_backbox_dmd_and_mini_dmd(self) -> None:
		displays = {display["id"]: display for display in self.definition["displays"]}
		self.assertEqual({"display.dmd", "display.mini-dmd"}, set(displays))
		for display in displays.values():
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		for source in self.definition["sources"]:
			self.assertNotIn("E:\\", source["uri"])
			self.assertNotIn("C:\\", source["uri"])
			if source["id"] in ("manual.stern.the-simpsons-pinball-party.2003", "vpx-table.simpsons-party-0-8-2", "vpx-script.simpsons-party-0-8-2"):
				self.assertIn("sha256", source, source["id"])
				self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
			if source["kind"] == "manual":
				excerpts = source.get("excerpts") or []
				self.assertGreaterEqual(len(excerpts), 6)
				for excerpt in excerpts:
					self.assertIn(excerpt["method"], {"manual", "ocr", "model", "mixed"})

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		controller = load_json(CONTROLLER_PATH)
		group_ids = {group["id"] for group in controller["groups"]}
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi"},
			group_ids,
		)


class SimpsonsPartyCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_simpsons_party as curator

		definition = curator.build()
		self.assertEqual(curator.canonical_bytes(definition), curator.canonical_bytes(curator.build()))
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
		self.assertEqual(curator.canonical_bytes(definition), DEFINITION_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_simpsons_party as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_simpsons_party as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b'"partial"', b'"author_ready"', 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_simpsons_party as curator

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(SPATIAL_REPORT_PATH.read_bytes(), curator.canonical_bytes(report))
		self.assertEqual(SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"), curator.render_spatial_report(report))


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class SimpsonsPartyRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_simpsons_party as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_simpsons_party as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "stern/the-simpsons-pinball-party-2003/source/The Simpsons Pinball Party v0.8.2.vpx"
		script = source_root / "stern/the-simpsons-pinball-party-2003/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_simpsons_party as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "the-simpsons-pinball-party-2003" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
