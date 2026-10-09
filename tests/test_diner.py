"""Fail-closed tests for the Williams Diner (1990) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Coil, Single Lamps and
Switch Levels tests for names and addresses, pinned PinMAME's dinerGameData for the A/C bank at 12,
the switch-2 copy and the flipper copy, the manual and its amendment for wiring and parts, and the
factory drawings for the placements the callout check validates. A regression names the fact that
broke.
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

import curate_diner  # noqa: E402
import drawing_callouts  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "diner-1990.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "diner-1990.md"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "diner-l4-service-and-mechanisms.json"
CALLOUT_SEED = ROOT / "tools" / "seeds" / "williams" / "diner-1990-callouts.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "williams.diner.1990"

DRIVERS = {"diner_l4", "diner_l3", "diner_l2", "diner_l1", "diner_f2", "diner_g2", "diner_p0", "diner_l4fr"}
# Coil-test step order as the ROM displays it, paired with the address that pulsed (run coil-test).
COIL_TEST = [1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
UNUSED_SWITCHES = {25, 26, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 60, 61, 62, 63, 64}
CLOCK_LAMPS = set(range(49, 61))
# Placements the drawings do not confirm (callout check) and placements no drawing checks.
NOT_VALIDATED_BY_CALLOUTS = {
	"device.cup-flashers.emitter", "device.left-jet-bumper.effect", "device.right-jet-bumper.effect",
	"device.upper-left-eject.effect", "lamp.matrix-12.emitter", "switch.matrix-17.sensor", "switch.matrix-27.sensor",
	"switch.matrix-28.sensor", "switch.matrix-29.sensor", "switch.matrix-36.sensor", "switch.matrix-49.sensor",
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def folded(text: str) -> str:
	return text.replace("0", "O").replace("5", "S")


class DinerDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(RUNTIME_PATH)
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_diner.check(ROOT)

	def test_definition_validates_and_keeps_its_two_open_requirements(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("0x400", self.definition["controller"]["hardware_generation"])

	def test_driver_tree_is_exactly_the_diner_clone_tree(self) -> None:
		self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
		compatibility = {d["id"]: d["physical_compatibility"] for d in self.definition["drivers"]}
		self.assertEqual("unknown", compatibility.pop("diner_p0"))
		self.assertEqual({"identical"}, set(compatibility.values()))
		catalog = load(ROOT / "catalog" / "pinmame.json")
		owners = {d["id"]: d.get("machine_id") for d in catalog["drivers"] if d["id"].startswith("diner_")}
		self.assertEqual(DRIVERS, set(owners))
		self.assertEqual({"williams.diner.1990"}, set(owners.values()))

	def test_variant_service_tests_match_the_parent(self) -> None:
		for game in curate_diner.VARIANT_GAMES:
			evidence = load(curate_diner.variant_evidence_path(game))
			self.assertEqual(game, evidence["runtime"]["game"])
			for name in ("coil-test", "single-lamps", "switch-levels"):
				self.assertIn("identical to the diner_l4 run", evidence["runtime"]["observations"]["runs"][name]["note"], (game, name))

	def test_every_controller_address_is_enumerated(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))

	def test_coil_names_follow_the_rom_coil_test(self) -> None:
		self.assertEqual(COIL_TEST, self.runs["coil-test"]["ordered_solenoid_on_sequence"])
		for step, address in enumerate(COIL_TEST, start=1):
			key = f"coil-{step:02d}-{slug(folded(curate_diner.ROM_COIL_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)
			self.assertIn(curate_diner.ROM_COIL_NAMES[address], self.solenoids[address]["physical"]["notes"])

	def test_lamp_names_follow_the_single_lamps_test(self) -> None:
		for address in range(1, 65):
			key = f"lamp-{address:02d}-{slug(folded(curate_diner.ROM_LAMP_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)

	def test_switch_names_follow_the_switch_levels_test(self) -> None:
		note = self.runs["switch-levels"]["note"].split("while held: ", 1)[1].rstrip(".")
		shown = {}
		for item in note.split("; "):
			address, rest = item.split(" = ", 1)
			shown[address] = rest.rsplit(" / ", 1)[0]
		for address, name in curate_diner.ROM_SWITCH_NAMES.items():
			self.assertEqual(folded(name), shown[str(address)], address)
		for address in range(60, 65):
			self.assertEqual("SWITCH LEVELS", shown[str(address)])
		self.assertEqual("RIGHT FLIPPER", shown["82"])
		self.assertEqual("LEFT FLIPPER", shown["84"])

	def test_ac_bank_is_published_at_25_to_32_and_copied_into_switch_2(self) -> None:
		for pair in range(1, 9):
			a, c = self.solenoids[pair], self.solenoids[pair + 24]
			self.assertEqual(f"{pair:02d}A", [x["value"] for x in a["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(f"{pair:02d}C", [x["value"] for x in c["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(a["wiring"]["driver_transistor"], c["wiring"]["driver_transistor"])
		self.assertEqual("relay", self.solenoids[12]["kind"])
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		self.assertIn((curate_diner.output_id(12), "switch.matrix-2"), relations)
		self.assertEqual(["internal.ac-relay-feedback"], self.switches[2]["roles"])

	def test_special_solenoids_have_no_emulated_switch_map(self) -> None:
		self.assertFalse(any(r["id"].startswith("relationship.special-solenoid-") for r in self.definition["relationships"]))
		gameplay = set(self.runs["gameplay"]["solenoid_addresses_seen"])
		self.assertTrue({17, 18, 19, 20, 21, 22} <= gameplay)
		for address in range(17, 23):
			self.assertEqual(f"Special #{address - 16}", [x["value"] for x in self.solenoids[address]["aliases"] if x["namespace"] == "manual.special-solenoid"][0])

	def test_flipper_buttons_are_copied_into_the_lane_change_optos(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if "flipper-column" in r["id"]}
		self.assertEqual({("switch.flipper-column-82", "switch.matrix-57"), ("switch.flipper-column-84", "switch.matrix-58")}, relations)
		for address in (57, 58):
			self.assertIn("cannot drive it", self.switches[address]["physical"]["notes"])
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])

	def test_every_fitted_switch_is_normally_open(self) -> None:
		for address in range(1, 65):
			device = self.switches[address]
			if address in UNUSED_SWITCHES:
				self.assertEqual("unused", device["availability"])
				self.assertNotIn("normally_closed", device)
			else:
				self.assertIn(device["availability"], ("used", "optional"))
				self.assertIs(False, device["normally_closed"], address)
		self.assertEqual("optional", self.switches[5]["availability"])

	def test_trough_left_and_right_follow_the_matrix_and_drawing(self) -> None:
		self.assertEqual("Ball Trough #1 (Right)", self.switches[11]["label"])
		self.assertEqual("Ball Trough #3 (Left)", self.switches[13]["label"])
		self.assertIn("Ball Trough #1 (left)", self.switches[11]["physical"]["notes"])

	def test_backbox_clock_lamps_and_stepper(self) -> None:
		for address in CLOCK_LAMPS:
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])
		for address in (15, 16):
			self.assertEqual("motor", self.solenoids[address]["kind"])
			self.assertEqual("cabinet_or_service", self.solenoids[address]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", self.switches[59]["spatial"]["reason"])
		clock = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.dine-time-clock")
		self.assertEqual(["switch.matrix-59"], clock["sensors"])

	def test_eat_lamps_have_two_bulbs_and_grill_values_follow_the_rom(self) -> None:
		for address in (22, 23, 24):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"])
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]))
		self.assertEqual("Grill Bonus 150K", self.lamps[42]["label"])
		self.assertEqual("Grill Bonus 250K", self.lamps[43]["label"])
		for address in (9, 16, 61):
			self.assertEqual("#44", self.lamps[address]["physical"]["part_number"])

	def test_amendment_corrects_the_diverter_coil(self) -> None:
		diverter = self.solenoids[14]
		self.assertEqual("AE-26-1500", diverter["physical"]["part_number"])
		self.assertIn(curate_diner.AMENDMENT_SOURCE, diverter["provenance"]["source_refs"])
		self.assertIn("AE-26-1200 to AE-26-1500", (EXCERPTS / "amendment-1.md").read_text(encoding="utf-8"))

	def test_gi_relay_and_unplaced_flasher(self) -> None:
		gi = self.solenoids[10]
		self.assertEqual("gi", gi["kind"])
		self.assertEqual(28, len(gi["spatial"]["placements"]))
		self.assertEqual("observed", gi["spatial"]["status"])
		self.assertNotIn("quantity", gi["physical"])
		self.assertNotIn("spatial", self.solenoids[32])
		self.assertEqual(4, self.solenoids[30]["physical"]["quantity"])

	def test_callout_check_validates_exactly_the_agreeing_placements(self) -> None:
		seed = load(CALLOUT_SEED)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		failing = {pid for pid, d in decisions["placements"].items() if not d["agrees"]}
		self.assertEqual(NOT_VALIDATED_BY_CALLOUTS, failing)
		corrected = [(key, r["label"]) for key, page in seed["pages"].items() for r in page["reads"] if "verifier_note" in r]
		self.assertEqual([("pdf-77", "9"), ("pdf-77", "9")], corrected)

	def test_legacy_aliases_are_carried_by_binding(self) -> None:
		def values(device: dict, namespace: str) -> set[str]:
			return {alias["value"] for alias in device["aliases"] if alias["namespace"] == namespace}

		self.assertTrue({"7", "07", "007"} <= values(self.switches[7], "vpe-legacy.switch"))
		self.assertIn("c_game_on", values(self.solenoids[23], "vpe-legacy.coil"))
		self.assertTrue({"1", "01", "001"} <= values(self.lamps[1], "vpe-legacy.lamp"))
		seed = load(curate_diner.LEGACY_ALIAS_SEED_PATH)
		carried = sum(len(aliases) for addresses in seed["aliases"].values() for aliases in addresses.values())
		present = sum(1 for collection in ("inputs", "outputs") for device in self.definition[collection] for alias in device["aliases"] if alias["namespace"].startswith("vpe-legacy."))
		self.assertEqual(carried, present)
		self.assertNotIn("65", seed["aliases"]["pinmame.output.lamp"])

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		import tempfile

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curate_diner.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curate_diner.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())
			self.assertFalse((root / curate_diner.DEFINITION_PATH.relative_to(ROOT)).exists())

	def test_manual_sources_carry_acquisition_provenance(self) -> None:
		sources = {s["id"]: s for s in self.definition["sources"]}
		for key in (curate_diner.MANUAL_SOURCE, curate_diner.AMENDMENT_SOURCE):
			source = sources[key]
			self.assertRegex(source["acquired_at"], r"^2026-10-09T\d\d:\d\d:\d\dZ$")
			self.assertTrue(source["sha256"] and source["original_filename"] and source["source_id"])
			self.assertIn("https://www.ipdb.org/files/681/", source["locator"])
		self.assertIn("https://www.ipdb.org/machine.cgi?id=681", sources[curate_diner.MANUAL_SOURCE]["locator"])
		self.assertEqual(curate_diner.EXTRACTION_MANIFEST_SHA256, sources[curate_diner.VPX_EXTRACTION_SOURCE]["sha256"])

	def test_extraction_verifier_refuses_a_refreshed_manifest(self) -> None:
		import tempfile

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			extraction = root / curate_diner.EXTRACTION_RELATIVE_PATH
			extraction.mkdir(parents=True)
			(extraction / "script.vbs").write_bytes(b"altered\n")
			curate_diner.write_extraction_manifest(root)
			with self.assertRaisesRegex(RuntimeError, "not the pinned one"):
				curate_diner.verify_extraction_manifest(root)

	def test_excerpt_digests_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if not d["id"].startswith("diner_") and len(d["id"]) >= 5 and "_" in d["id"]}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9]+_[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class DinerRetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import diner_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = diner_runtime_evidence.working_root()
		if not (review_root / diner_runtime_evidence.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Diner runs are not present under this review-artifacts root")
		_, evidence, variants = diner_runtime_evidence.build(review_root)
		self.assertEqual(canonical_bytes(evidence), RUNTIME_PATH.read_bytes())
		for game, record in variants.items():
			self.assertEqual(canonical_bytes(record), curate_diner.variant_evidence_path(game).read_bytes())

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curate_diner.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		if not (root / curate_diner.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Diner extraction is not present under this root")
		curate_diner.verify_extraction_manifest(root)

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
