"""Fail-closed tests for the Gottlieb Stargate (1995) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Lamp Matrix, Relay & Solenoid, Aux Driver
and Switch Edges tests for names and addresses, pinned PinMAME's gts3.c and gts3games.c for the numbering, the flipper
copy and the auxiliary board, and the retained known-working table for bindings and placements. A regression names the
fact that broke.
"""

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
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_stargate  # noqa: E402
import gts3_dmd_text  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "gottlieb" / "stargate-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "gottlieb" / "stargate-1995.md"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "gts3.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "gottlieb.stargate.1995"
DRIVERS = {"stargate", "stargat1", "stargat2", "stargat3", "stargat4", "stargat5"}
MATRIX = {column * 10 + row for column in range(12) for row in range(8)}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def note_pairs(note: str) -> dict[str, str]:
	"""Parse the "Address = name: a = b; c = d." list a run note ends with."""
	body = note.split("Address = name: ", 1)[1].split(". No SWITCH line", 1)[0].rstrip(".")
	pairs = {}
	for item in body.split("; "):
		key, _, value = item.partition(" = ")
		pairs[key] = value
	return pairs


def allowed(rules: list[dict]) -> set[int]:
	values: set[int] = set()
	for rule in rules:
		values |= set(rule["values"]) if "values" in rule else set(range(rule["minimum"], rule["maximum"] + 1))
	return values


class StargateDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"]}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(curate_stargate.runtime_evidence_path("stargat5"))
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]
		cls.profile = load(PROFILE_PATH)

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_stargate.check(ROOT)

	def test_definition_validates_and_keeps_its_two_open_requirements(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["polarity", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual({"platform": "pinmame.gts3", "hardware_generation": "0x20000000000", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertEqual((2847, "742", "G50pv-MdE6R"), (self.definition["machine"]["ipdb_id"], self.definition["machine"]["model_number"], self.definition["machine"]["opdb_id"]))

	def test_driver_tree_is_exactly_the_stargate_clone_tree_and_identical(self) -> None:
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual(DRIVERS, set(drivers))
		self.assertEqual({"identical"}, {d["physical_compatibility"] for d in drivers.values()})
		catalog = load(ROOT / "catalog" / "pinmame.json")
		claimed = {d["id"] for d in catalog["drivers"] if d.get("machine_id") == curate_stargate.MACHINE_ID}
		self.assertEqual(DRIVERS, claimed)

	def test_variant_service_tests_match_the_primary_set(self) -> None:
		for game in curate_stargate.VARIANT_SETS:
			with self.subTest(game=game):
				evidence = load(curate_stargate.runtime_evidence_path(game))
				comparison = evidence["runtime"]["observations"]["runs"]["comparison"]["note"]
				self.assertTrue(comparison.startswith("Every lamp, solenoid, aux driver and switch name"), comparison)
				self.assertEqual(self.named, evidence["runtime"]["observations"]["named_output_addresses"])

	def test_every_profile_address_is_enumerated_once(self) -> None:
		groups = {group["id"]: allowed(group["address_rules"]) for group in self.profile["groups"]}
		self.assertEqual(groups["pinmame.input.switch"], set(self.switches))
		self.assertEqual(groups["pinmame.output.solenoid"], set(self.solenoids))
		self.assertEqual(groups["pinmame.output.lamp"], set(self.lamps))
		self.assertEqual(set(range(-8, -4)) | MATRIX | set(range(140, 148)), groups["pinmame.input.switch"])
		self.assertEqual(MATRIX | set(range(120, 128)), groups["pinmame.output.lamp"])
		self.assertEqual(set(range(1, 33)) | set(range(45, 49)), groups["pinmame.output.solenoid"])

	def test_coil_names_follow_the_rom_relay_and_solenoid_test(self) -> None:
		for key, address in self.named.items():
			match = re.fullmatch(r"solenoid-(\d+)-(.+)", key)
			if not match:
				continue
			driver, name = int(match.group(1)), match.group(2)
			self.assertEqual(driver + 1, address)
			self.assertEqual(curate_stargate.slug(curate_stargate.ROM_COIL_NAMES[address]), name)
			self.assertIn(f"\"{curate_stargate.ROM_COIL_NAMES[address]}\"", self.solenoids[address]["physical"]["notes"])
		# The walk fires drivers 0-31 and then wraps back to driver 0.
		self.assertEqual(list(range(1, 33)) + [1], self.runs["solenoids"]["ordered_solenoid_on_sequence"])
		self.assertEqual({21, 25}, {a for a, o in self.solenoids.items() if o["availability"] == "unused"})

	def test_lamp_names_follow_the_lamp_matrix_test(self) -> None:
		pairs = note_pairs(self.runs["lamp-matrix"]["note"])
		self.assertEqual({str(address) for address in MATRIX}, set(pairs))
		for address in MATRIX:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "(NOT USED)":
					self.assertEqual("unused", self.lamps[address]["availability"])
				else:
					self.assertEqual(curate_stargate.ROM_LAMP_NAMES[address], name)
					self.assertEqual("used", self.lamps[address]["availability"])

	def test_aux_driver_outputs_are_lamps_120_to_127(self) -> None:
		for address in range(120, 128):
			key = f"aux-{address - 120}-{curate_stargate.slug(curate_stargate.ROM_AUX_NAMES[address])}"
			self.assertEqual(address, self.named[key])
			self.assertEqual("flasher", self.lamps[address]["kind"])
		self.assertEqual("not_applicable", self.lamps[126]["spatial"]["status"])
		self.assertEqual("not_applicable", self.lamps[127]["spatial"]["status"])

	def test_switch_names_follow_the_switch_edges_test(self) -> None:
		pairs = note_pairs(self.runs["switch-edges"]["note"])
		expected = (MATRIX - {4})
		self.assertEqual({str(address) for address in expected}, set(pairs))
		for address in expected:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "(NOT USED)":
					self.assertEqual("unused", self.switches[address]["availability"])
				else:
					self.assertEqual(curate_stargate.ROM_SWITCH_NAMES[address], name)
					self.assertEqual("used", self.switches[address]["availability"])

	def test_every_fitted_physical_switch_is_normally_open_except_the_unproven_glider_left(self) -> None:
		for address, device in self.switches.items():
			if device["kind"] == "switch" and device["availability"] in ("used", "optional"):
				with self.subTest(address=address):
					if address == 20:
						self.assertNotIn("normally_closed", device)
						self.assertIn("Polarity unknown", device["physical"]["notes"])
					else:
						self.assertIs(False, device.get("normally_closed"))

	def test_flipper_buttons_are_copied_into_81_and_82(self) -> None:
		relationships = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		self.assertEqual({("switch.flipper-column-141", "switch.matrix-82"), ("switch.flipper-column-143", "switch.matrix-81")}, relationships)
		for address in (81, 82):
			self.assertIn("cannot be driven directly", self.switches[address]["physical"]["notes"])
		self.assertEqual({141, 143}, {a for a in range(140, 148) if self.switches[a]["availability"] == "used"})
		self.assertEqual((81, 82), curate_stargate.FLIP_SWNO)

	def test_horus_target_defect_is_recorded_on_the_device_not_as_a_conflict(self) -> None:
		for address in (116, 117):
			notes = self.switches[address]["physical"]["notes"]
			self.assertIn("switch mod 100", notes)
			self.assertIn(f"pulses {address - 100} instead of {address}", notes)
		excerpt = (EXCERPTS / "vpw-script-bindings.md").read_text(encoding="utf-8")
		self.assertIn("`vpmTimer.PulseSw switch mod 100`", excerpt)

	def test_relays_follow_the_platform_and_the_rom(self) -> None:
		self.assertEqual("relay", self.solenoids[26]["kind"])
		self.assertEqual("relay", self.solenoids[31]["kind"])
		self.assertEqual("relay", self.solenoids[32]["kind"])
		self.assertEqual(16, len(self.solenoids[31]["spatial"]["placements"]))
		self.assertTrue(all(p["provenance"]["status"] == "observed" for p in self.solenoids[31]["spatial"]["placements"]))
		self.assertEqual(["motor", "motor"], [self.solenoids[23]["kind"], self.solenoids[24]["kind"]])

	def test_no_placement_is_validated(self) -> None:
		statuses = {
			placement["provenance"]["status"]
			for collection in ("inputs", "outputs") for device in self.definition[collection]
			for placement in (device.get("spatial") or {}).get("placements", [])
		}
		self.assertEqual({"observed"}, statuses)

	def test_placements_are_in_range(self) -> None:
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				for placement in (device.get("spatial") or {}).get("placements", []):
					with self.subTest(placement=placement["id"]):
						self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)

	def test_legacy_aliases_are_carried_by_binding(self) -> None:
		seed = load(curate_stargate.LEGACY_ALIAS_SEED_PATH)
		carried = sum(len(aliases) for addresses in seed["aliases"].values() for aliases in addresses.values())
		present = sum(1 for collection in ("inputs", "outputs") for device in self.definition[collection] for alias in device["aliases"] if alias["namespace"].startswith("vpe-legacy."))
		self.assertEqual(carried, present)
		values = {alias["value"] for alias in self.switches[5]["aliases"] if alias["namespace"] == "vpe-legacy.switch"}
		self.assertTrue({"5", "05", "005"} <= values)

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curate_stargate.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curate_stargate.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())

	def test_extraction_verifier_refuses_a_refreshed_manifest(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			extraction = root / curate_stargate.EXTRACTION_RELATIVE_PATH
			extraction.mkdir(parents=True)
			(extraction / "script.vbs").write_bytes(b"altered\n")
			curate_stargate.write_extraction_manifest(root)
			with self.assertRaisesRegex(RuntimeError, "not the pinned one"):
				curate_stargate.verify_extraction_manifest(root)

	def test_excerpt_digests_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if not d["id"].startswith("stargat") and re.search(r"\d|_", d["id"]) and len(d["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)

	def test_dmd_decoder_reads_a_frame_built_from_the_glyph_table(self) -> None:
		glyphs = gts3_dmd_text.load_glyphs()
		by_char: dict[tuple[int, str], str] = {}
		for key, char in glyphs.items():
			height = int(key.split(":")[0].split("x")[1])
			by_char.setdefault((height, char), key)
		frame = [[0] * 128 for _ in range(32)]

		def draw(text: str, height: int, top: int) -> None:
			x = 2
			for char in text:
				if char == " ":
					x += 4
					continue
				key = by_char[(height, char)]
				size, bits = key.split(":")
				width = int(size.split("x")[0])
				value = int(bits, 16)
				for y in range(height):
					for column in range(width):
						if value >> (width * height - 1 - (y * width + column)) & 1:
							frame[top + y][x + column] = 1
				x += width + 1

		draw("SOLENOID:12", 5, 2)
		draw("TOP PYRAMID", 7, 12)
		data = b"P5\n128 32\n255\n" + bytes(255 if pixel else 0 for row in frame for pixel in row)
		self.assertEqual(["SOLENOID:12", "TOP PYRAMID"], gts3_dmd_text.decode(data, glyphs))
		self.assertEqual((110, "X"), gts3_dmd_text.labelled(["SWITCH:B0", "X"], "SWITCH"))
		# A raster byte that is a whitespace level is a pixel, and a truncated file is refused rather than read past.
		raster = bytes([10, 32, 9, 13]) + bytes(128 * 32 - 4)
		self.assertEqual(raster, gts3_dmd_text.read_pgm(b"P5\n128 32\n255\n" + raster)[2])
		for truncated in (b"", b"P5\n128 32\n", b"P5\n128 32\n255", b"P5\n128 32\n255\n" + raster[:-1]):
			with self.subTest(truncated=truncated[:16]), self.assertRaises(ValueError):
				gts3_dmd_text.read_pgm(truncated)


class StargateRetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import stargate_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = stargate_runtime_evidence.working_root()
		if not (review_root / stargate_runtime_evidence.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Stargate runs are not present under this review-artifacts root")
		bundles = stargate_runtime_evidence.build(review_root)
		for game, bundle in bundles.items():
			self.assertEqual(canonical_bytes(bundle), curate_stargate.runtime_evidence_path(game).read_bytes(), game)

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curate_stargate.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		if not (root / curate_stargate.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Stargate extraction is not present under this root")
		curate_stargate.verify_extraction_manifest(root)


if __name__ == "__main__":
	unittest.main()
