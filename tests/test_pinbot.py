"""Fail-closed tests for the Williams Pin-Bot (1986) definition.

Each test pins one fact against the evidence that decided it: the ROM's own coil, lamp and switch
tables and service tests for names and addresses, pinned PinMAME's pbGameData for the A/C bank, the
special-solenoid switch map and the flipper copy, and the factory drawings for the placements the
callout check validates. A regression names the fact that broke.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_pinbot  # noqa: E402
import drawing_callouts  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "pinbot-1986.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "pinbot-1986.md"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "pinbot-l5-service-and-mechanisms.json"
CALLOUT_SEED = ROOT / "tools" / "seeds" / "williams" / "pinbot-1986-callouts.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "williams.pinbot.1986"

DRIVERS = {"pb_l5", "pb_l3", "pb_l2", "pb_l1", "pb_p4", "pb_l5h", "pb_j1", "pb_j2", "pb_j3", "pb_j5"}
# Coil-test step order as the ROM displays it, paired with the address that pulsed (run coil-test).
COIL_TEST = [1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
SPECIAL_SWITCHES = {17: 53, 19: 48, 20: 54, 21: 55, 22: 52}
UNUSED_SWITCHES = {21, 27, 41, 42, 43, 57, 58, 61, 62, 63, 64}
CHEST = {28, 29, 30, 31, 32, 36, 37, 38, 39, 40, 44, 45, 46, 47, 48, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class PinbotDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(RUNTIME_PATH)

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_pinbot.check(ROOT)

	def test_definition_validates_and_stays_partial_on_spatial_only(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])

	def test_driver_tree_is_exactly_the_pb_clone_tree(self) -> None:
		self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.definition["drivers"]))
		catalog = load(ROOT / "catalog" / "pinmame.json")
		owners = {d["id"]: d.get("machine_id") for d in catalog["drivers"] if d["id"].startswith("pb_")}
		self.assertEqual(DRIVERS, set(owners))
		self.assertEqual({"williams.pinbot.1986"}, set(owners.values()))

	def test_every_controller_address_is_enumerated(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))

	def test_coil_names_follow_the_rom_coil_test(self) -> None:
		observed = self.runtime["runtime"]["observations"]["runs"]["coil-test"]["ordered_solenoid_on_sequence"]
		self.assertEqual(COIL_TEST, observed)
		for address in COIL_TEST:
			self.assertIn(curate_pinbot.ROM_COIL_NAMES[address], self.solenoids[address]["physical"]["notes"])

	def test_ac_bank_is_published_at_25_to_32(self) -> None:
		for pair in range(1, 9):
			a, c = self.solenoids[pair], self.solenoids[pair + 24]
			self.assertEqual(f"{pair:02d}A", [x["value"] for x in a["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(f"{pair:02d}C", [x["value"] for x in c["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(a["wiring"]["driver_transistor"], c["wiring"]["driver_transistor"])
			self.assertNotEqual(a["wiring"]["control_connection"], c["wiring"]["control_connection"])
		self.assertEqual("Solenoid Select (A/C) Relay", self.solenoids[14]["label"])
		self.assertEqual("relay", self.solenoids[14]["kind"])

	def test_special_solenoids_follow_their_own_switches(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["id"].startswith("relationship.special-solenoid-")}
		expected = {(f"switch.matrix-{sw}", curate_pinbot.output_id(sol)) for sol, sw in SPECIAL_SWITCHES.items()}
		self.assertEqual(expected, relations)
		self.assertEqual("gi", self.solenoids[18]["kind"])
		gameplay = self.runtime["runtime"]["observations"]["runs"]["gameplay"]["solenoid_addresses_seen"]
		self.assertTrue(set(SPECIAL_SWITCHES) <= set(gameplay))

	def test_flipper_buttons_are_copied_into_the_lane_change_switches(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if "flipper-column" in r["id"]}
		self.assertEqual({("switch.flipper-column-82", "switch.matrix-11"), ("switch.flipper-column-84", "switch.matrix-10")}, relations)
		for address in (10, 11):
			self.assertIn("cannot drive it directly", self.switches[address]["physical"]["notes"])
		levels = self.runtime["runtime"]["observations"]["runs"]["switch-levels"]["note"]
		self.assertIn("public 82: displayed 'R. LANE CHANGE'", levels)
		self.assertIn("public 84: displayed 'L. LANE CHANGE'", levels)

	def test_every_fitted_switch_is_normally_open(self) -> None:
		levels = self.runtime["runtime"]["observations"]["runs"]["switch-levels"]["note"]
		self.assertIn("for public 1-60.", levels)
		for address in range(1, 65):
			device = self.switches[address]
			if address in UNUSED_SWITCHES:
				self.assertEqual("unused", device["availability"])
				self.assertNotIn("normally_closed", device)
			else:
				self.assertEqual("used", device["availability"])
				self.assertIs(False, device["normally_closed"], address)

	def test_unused_lamp_and_backbox_lamps(self) -> None:
		self.assertEqual("unused", self.lamps[59]["availability"])
		for address in range(1, 9):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])
		self.assertEqual(2, self.lamps[1]["physical"]["quantity"])
		chest = {a for a, lamp in self.lamps.items() if lamp["label"].startswith("Chest ")}
		self.assertEqual(CHEST, chest)

	def test_rom_name_excerpt_matches_the_curator(self) -> None:
		text = (EXCERPTS / "rom-name-tables.md").read_text(encoding="utf-8")
		section = text.split("## Switch table")[1].split("## Coil table")[0]
		rows = dict(re.findall(r"^\| (\d+) \| (.+?) \|$", section, re.M))
		self.assertEqual({str(k): v for k, v in curate_pinbot.ROM_SWITCH_NAMES.items()}, rows)
		section = text.split("## Lamp table")[1].split("## Switch table")[0]
		rows = dict(re.findall(r"^\| (\d+) \| (.+?) \|$", section, re.M))
		self.assertEqual({str(k): v for k, v in curate_pinbot.ROM_LAMP_NAMES.items()}, rows)

	def test_callout_check_validates_exactly_the_agreeing_placements(self) -> None:
		seed = load(CALLOUT_SEED)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		failing = {pid for pid, d in decisions["placements"].items() if not d["agrees"]}
		self.assertEqual({"switch.matrix-40.sensor"}, failing)
		statuses = {p["id"]: p["provenance"]["status"] for p in [pl for c in ("inputs", "outputs") for d in self.definition[c] for pl in (d.get("spatial") or {}).get("placements", [])]}
		gi = {f"device.playfield-g-i-relay.emitter.{index}" for index in range(1, 28)}
		self.assertEqual({"switch.matrix-40.sensor"} | gi, {pid for pid, status in statuses.items() if status != "validated"})
		corrected = [r for r in seed["pages"]["pdf-58"]["reads"] if "verifier_note" in r]
		self.assertEqual(["24"], [r["label"] for r in corrected])

	def test_visor_gi_has_no_invented_placement(self) -> None:
		for address in (10, 18):
			self.assertNotIn("spatial", self.solenoids[address])
		self.assertEqual(27, len(self.solenoids[12]["spatial"]["placements"]))
		self.assertEqual("observed", self.solenoids[12]["spatial"]["status"])
		self.assertNotIn("quantity", self.solenoids[12]["physical"])

	def test_misprinted_parts_list_row_asserts_no_part_number(self) -> None:
		self.assertNotIn("part_number", self.switches[33]["physical"])
		self.assertIn("Visor Target top,yellow)", self.switches[33]["physical"]["notes"])
		for address in range(34, 38):
			self.assertEqual("A-11317-3", self.switches[address]["physical"]["part_number"])

	def test_country_jumper_is_w7(self) -> None:
		notes = next(i for i in self.definition["inputs"] if i["binding"]["group"] == "pinmame.input.dip")["physical"]["notes"]
		self.assertIn("W7", notes)
		self.assertNotIn("W8", notes)

	def test_manual_sources_carry_acquisition_provenance(self) -> None:
		sources = {s["id"]: s for s in self.definition["sources"]}
		archive, ipdb = sources[curate_pinbot.MANUAL_SOURCE], sources[curate_pinbot.IPDB_MANUAL_SOURCE]
		for source in (archive, ipdb):
			self.assertRegex(source["acquired_at"], r"^2026-10-09T\d\d:\d\d:\d\dZ$")
			self.assertTrue(source["sha256"] and source["original_filename"] and source["source_id"])
		self.assertIn("https://archive.org/details/PinBotInstructionManualSchematics600dpi", archive["locator"])
		self.assertIn("https://archive.org/download/PinBotInstructionManualSchematics600dpi/", archive["locator"])
		self.assertIn("mhkohne@kohne.org", archive["locator"])
		self.assertIn("https://www.ipdb.org/machine.cgi?id=1796", ipdb["locator"])
		self.assertIn("https://www.ipdb.org/files/1796/Williams_1986_Pin_bot_Manual.pdf", ipdb["locator"])
		self.assertEqual(curate_pinbot.EXTRACTION_MANIFEST_SHA256, sources[curate_pinbot.VPX_EXTRACTION_SOURCE]["sha256"])

	def test_extraction_verifier_refuses_a_refreshed_manifest(self) -> None:
		import tempfile

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			extraction = root / curate_pinbot.EXTRACTION_RELATIVE_PATH
			extraction.mkdir(parents=True)
			(extraction / "script.vbs").write_bytes(b"altered\n")
			curate_pinbot.write_extraction_manifest(root)
			with self.assertRaisesRegex(RuntimeError, "not the pinned one"):
				curate_pinbot.verify_extraction_manifest(root)

	def test_excerpt_digests_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if not d["id"].startswith("pb_") and len(d["id"]) >= 5 and "_" in d["id"]}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9]+_[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class PinbotRetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import pinbot_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = pinbot_runtime_evidence.working_root()
		if not (review_root / pinbot_runtime_evidence.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Pin-Bot runs are not present under this review-artifacts root")
		_, evidence, _ = pinbot_runtime_evidence.build(review_root)
		self.assertEqual(canonical_bytes(evidence), RUNTIME_PATH.read_bytes())

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curate_pinbot.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		if not (root / curate_pinbot.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Pin-Bot extraction is not present under this root")
		curate_pinbot.verify_extraction_manifest(root)

	def test_callout_renders_and_reads_are_unchanged(self) -> None:
		manuals = os.environ.get("PINMAME_MANUALS_ROOT")
		review = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals and not review:
			self.skipTest("no evidence roots configured")
		checked = drawing_callouts.verify_retained(
			load(CALLOUT_SEED), ROOT, Path(manuals) if manuals else None, Path(review) if review else None
		)
		self.assertGreater(checked, 0)


if __name__ == "__main__":
	unittest.main()
