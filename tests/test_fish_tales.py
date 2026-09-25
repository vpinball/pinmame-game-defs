from __future__ import annotations

import json
import os
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "fish-tales-1992.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "fish-tales-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "fish-tales-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "fish-tales-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "fish-tales-1992.json"

DRIVER_IDS = {"ft_l5", "ft_l5p", "ft_d5", "ft_d6", "ft_l3", "ft_l4", "ft_p2", "ft_p4", "ft_p5"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
MANUAL_OPTO_ADDRESSES = {37, 38}
RUNTIME_EDGES_PATH = ROOT / "evidence" / "runtime" / "wpc-fliptronic" / "fish-tales-switch-edges.json"
EDGES_SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / "ft-switch-edges-37-38-47-48.json"
EDGES_SCENARIO_SHA256 = "e12eff3f8ea3c65f05bf27c79b9eb9d8927af7ddf64e7e0cbb0f03134a96ca8d"
EDGES_RAW_SHA256 = "f5c546faed84d49654bec3612d26e688b90829c3bcff5492e171734383566872"
EDGES_ROM_SHA256 = "81acda6f1def49374d3345a44b4df64320309d8a9741117bf207172c82d78dea"
EDGES_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
# DMD pixel hash -> (the ROM's top display line, the scenario step the frame was captured after).
EDGES_FRAMES = {
	"2140f3780f3dee47dc37845a8e3488bea31ab7e61ff4c9894e8d7e87766f2ded": ("CAPTIVE BALL", "41 -> 1"),
	"76891ba61e6b744d7d4809ba2053b2ae50dd31260927c5303338568c3c0a12d5": ("R FLIPPER EOS", "112 -> 1"),
	"f4bfa35f9ef07ffd831240f2c8948a04e1ac74a0a7e5d13f55ab848a8e36d764": ("BALL POPPER", "47 -> 1"),
	"33493d7a8157514684ca96a0feb846f7d5eebf9220beb2b97776ac5ab5e29e38": ("SWITCH EDGES", "47 -> 0"),
	"82e23eb5acdb5afe3ab03f245703c2a9bc3f0a4096cd8fc25ac9bbd4e0ef5b7b": ("DROP TARGET", "48 -> 1"),
	"d42e7c5818a575f26924214bdfdba47d7d5369f99bcc10dfc5313d7624f1cfb0": ("SWITCH EDGES", "48 -> 0"),
	"f5a6e9ffe8c042a2e324ad759033b444a4cfb7434cf595295000b0fd943862cf": ("SWITCH EDGES", "37 -> 1"),
	"ddcfcc3e48a02b1481fbb4e213e41d10828c6f6c27cbf025b6b54ba9dbd6fa8e": ("REEL 1 OPTO", "37 -> 0"),
	"57a871527c458d98eaa3228b962bf53e51180a3a95f4fcbcceb45c959c692de1": ("SWITCH EDGES", "38 -> 1"),
	"0f2c81dddf62f03e9e7d28a12049bfa024566af9323ee942e8ab0987a9b6a407": ("REEL 2 OPTO", "38 -> 0"),
}
RUNTIME_CONTROL_PATH = ROOT / "evidence" / "runtime" / "wpc-fliptronic" / "addams-family-switch-edges-control.json"
CONTROL_SCENARIO_PATH = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / "taf-switch-edges-control-53-57.json"
CONTROL_SCENARIO_SHA256 = "30f2d408561edea255f25ddd63deb68b3c963838d63134a854c990f6ae1030e5"
CONTROL_RAW_SHA256 = "ca09333def6bda985d7e375227c07c699fa7de2c33869458102d92cde79cc78f"
CONTROL_ROM_SHA256 = "6373de2ff091a8022f96f363a66cac6f8c9095bbfbf859c4ff7c7335b9c54f70"
# DMD pixel hash -> (the ROM's top display line, the scenario step the frame was captured after).
CONTROL_FRAMES = {
	"8f010fabc7f287ee": ("GRAVE", "41 -> 1"),
	"edea90f3b07e7423": ("BOOKCASE OPTO 1", "53 -> 1"),
	"1cf0799e3255c6a5": ("SWITCH EDGES", "53 -> 0"),
	"9fcd4f3ae36090b3": ("BUMPER LANE OPTO", "57 -> 1"),
	"ff7c73bdb19133e6": ("SWITCH EDGES", "57 -> 0"),
}
EDGES_PINNED_FRAMES = {sha: text for sha, (text, _) in EDGES_FRAMES.items()}
EDGES_PINNED_FRAME_LABELS = {sha: label for sha, (_, label) in EDGES_FRAMES.items()}
# Transcription of the known-working table's RotateReel Select Case (script.vbs:1611-1633):
# (ReelPosition start, end, sw38, sw37). Re-checked against the retained script when the evidence
# root is configured.
ROTATE_REEL_CASES = (
	(0, 20, 1, 1), (20, 30, 0, 1), (30, 50, 1, 1), (50, 60, 0, 0), (60, 80, 0, 1), (80, 90, 0, 0),
	(90, 110, 1, 0), (110, 120, 0, 0), (120, 140, 0, 1), (140, 150, 0, 0), (150, 170, 1, 0),
	(170, 180, 0, 0), (180, 200, 0, 1), (200, 210, 0, 0), (210, 230, 1, 0), (230, 240, 0, 0),
	(240, 260, 0, 1), (260, 270, 0, 0), (270, 290, 1, 0), (290, 300, 0, 0), (300, 320, 0, 1),
	(320, 330, 0, 0), (330, 360, 1, 0),
)


def rotate_reel_public_one_windows(address: int) -> list[tuple[int, int]]:
	"""Contiguous ReelPosition windows in which the table writes public 1 to 37 or 38."""
	column = 3 if address == 37 else 2
	windows: list[tuple[int, int]] = []
	for case in ROTATE_REEL_CASES:
		if case[column] != 1:
			continue
		if windows and windows[-1][1] == case[0]:
			windows[-1] = (windows[-1][0], case[1])
		else:
			windows.append((case[0], case[1]))
	return windows


NOT_FITTED_UPPER_FLIPPER_SOLENOIDS = {33, 34, 35, 36}
FAKE_REEL_SOLENOIDS = {51, 52, 53}


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
	import curate_fish_tales as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_fish_tales.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class FishTalesDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_author_ready_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.fish-tales.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(861, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_reel_opto_public_level_is_a_mixed_level_exception_not_a_conflict(self) -> None:
		# The settled consumer contract plus PinMAME's guessed mask is a per-game data defect, not a
		# disagreement about the physical machine, so no conflict is recorded.
		self.assertEqual([], self.definition["conflicts"])
		self.assertNotIn("conflict.", json.dumps(self.definition))
		for address in (37, 38):
			switch = self.switches[address]
			self.assertEqual("validated", switch["provenance"]["status"], address)
			notes = switch["physical"]["notes"]
			self.assertIn("mixed-level exception", notes, address)
			self.assertIn("reads public 37/38 = 0 as the opto made", notes, address)
			self.assertIn("RotateReel", notes, address)
			self.assertIn("runtime.the-addams-family.switch-edges-control", switch["provenance"]["source_refs"], address)

	def test_no_curator_constant_name_leaks_into_generated_prose(self) -> None:
		import curate_fish_tales as curator

		names = sorted(name for name in vars(curator) if name.isupper() and "_" in name)
		self.assertIn("RUNTIME_EDGES_SOURCE", names)
		for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
			text = path.read_text(encoding="utf-8")
			leaked = [name for name in names if re.search(rf"\b{name}\b", text)]
			self.assertEqual([], leaked, path.name)

	def test_generation_control_shows_the_t1_top_line_is_logical_on_wpc_fliptronic(self) -> None:
		import hashlib

		evidence = load_json(RUNTIME_CONTROL_PATH)
		self.assertEqual("taf_l7", evidence["runtime"]["game"])
		(raw,) = evidence["runtime"]["raw_runs"]
		self.assertEqual(hashlib.sha256(CONTROL_SCENARIO_PATH.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertEqual(CONTROL_SCENARIO_SHA256, raw["scenario_sha256"])
		self.assertEqual(CONTROL_RAW_SHA256, raw["sha256"])
		self.assertEqual(CONTROL_ROM_SHA256, evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual(EDGES_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
		named = {}
		for item in evidence["runtime"]["observations"]["named_action_observations"]:
			level = "1" if " set to 1 " in item["label"] else "0"
			named[(item["input_address"], level)] = item["label"]
		self.assertEqual({(a, b) for a in (41, 53, 57) for b in "01"}, set(named))
		for address in (41, 53, 57):
			self.assertIn(f"reads public {address} = 1 as active", named[(address, "1")])
		# tafGameData's mask inverts 53 and 57, so their public 1 is an open matrix contact.
		mask = (0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00)
		for address in (53, 57):
			index = (address // 10) * 8 + (address % 10 - 1)
			self.assertTrue((mask[index // 8] >> (index % 8)) & 1, address)
		snapshots = evidence["runtime"]["observations"]["diagnostic_snapshots"]
		texts = {item["pixel_sha256"][:16]: item["interpreted_text"] for item in snapshots}
		for prefix, (top_line, _label) in CONTROL_FRAMES.items():
			self.assertTrue(texts[prefix].startswith(top_line), top_line)
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		run = load_json(path)
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		self.assertEqual(0, run["handle_mechanics"])
		shown = {}
		for snap in run["snapshots"]:
			if " -> " not in snap["label"]:
				continue
			address, state = (int(part.split()[0]) for part in snap["label"].split(" -> "))
			levels = {w["number"]: w["state"] for w in snap["watched_switches"]}
			self.assertEqual(state, levels[address], snap["label"])
			shown.setdefault(snap["displays"][0]["pixel_sha256"][:16], set()).add(snap["label"])
		for prefix, (_top_line, label) in CONTROL_FRAMES.items():
			self.assertIn(label, shown.get(prefix, set()), label)

	def test_switch_edges_evidence_shows_the_level_the_rom_reads_as_active(self) -> None:
		import hashlib

		evidence = load_json(RUNTIME_EDGES_PATH)
		self.assertEqual("ft_l5", evidence["runtime"]["game"])
		(raw,) = evidence["runtime"]["raw_runs"]
		self.assertEqual(hashlib.sha256(EDGES_SCENARIO_PATH.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertEqual(EDGES_SCENARIO_SHA256, raw["scenario_sha256"])
		self.assertEqual(EDGES_RAW_SHA256, raw["sha256"])
		self.assertEqual(EDGES_ROM_SHA256, evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual(EDGES_LIBRARY_SHA256, evidence["runtime"]["emulator"]["sha256"])
		named = {}
		for item in evidence["runtime"]["observations"]["named_action_observations"]:
			level = "1" if " set to 1 " in item["label"] else "0"
			named[(item["input_address"], level)] = item["label"]
		self.assertEqual({(a, b) for a in (37, 38, 41, 47, 48, 112) for b in "01"}, set(named))
		for address in (41, 47, 48):
			self.assertIn(f"reads public {address} = 1 as active", named[(address, "1")])
			self.assertIn("returns to SWITCH EDGES", named[(address, "0")])
		for address in (37, 38):
			self.assertIn(f"reads public {address} = 0 as active", named[(address, "0")])
			self.assertIn(f"reads public {address} = 1 as inactive", named[(address, "1")])
		self.assertIn("fires the right flipper (public 46)", named[(112, "1")])
		texts = {item["pixel_sha256"]: item["interpreted_text"] for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]}
		for pixel_sha256, top_line in EDGES_PINNED_FRAMES.items():
			self.assertTrue(texts[pixel_sha256].startswith(top_line), top_line)
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		run = load_json(path)
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		self.assertEqual(0, run["handle_mechanics"])
		shown: dict[str, str] = {}
		for snap in run["snapshots"]:
			if " -> " not in snap["label"]:
				continue
			address, state = (int(part.split()[0]) for part in snap["label"].split(" -> "))
			levels = {w["number"]: w["state"] for w in snap["watched_switches"]}
			self.assertEqual(state, levels[address], snap["label"])
			shown[snap["displays"][0]["pixel_sha256"]] = snap["label"]
		for pixel_sha256, label in EDGES_PINNED_FRAME_LABELS.items():
			self.assertEqual(label, shown.get(pixel_sha256), label)
		for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]:
			if "was set to" in item["label"]:
				self.assertIn(item["pixel_sha256"], shown, item["label"])

	def test_the_stale_partial_artifact_is_gone(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_ft_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in DRIVER_IDS - {"ft_l5"}:
			self.assertEqual("ft_l5", by_id[driver_id]["clone_of"], driver_id)
		self.assertNotIn("clone_of", by_id["ft_l5"])

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_matrix_contact_polarity_is_the_contact_while_the_rom_reads_the_switch_inactive(self) -> None:
		# 37/38: the mask turns public 0 into a closed contact and the T.1 top line names them made at
		# public 0, so the contact closes only when actuated. 47/48: unmasked microswitches read active
		# at public 1, closed only when actuated.
		for address in sorted(MANUAL_OPTO_ADDRESSES):
			switch = self.switches[address]
			self.assertEqual("opto", switch["physical"]["switch_type"], address)
			self.assertFalse(switch["normally_closed"], address)
			self.assertIn("normally_closed is false", switch["physical"]["notes"], address)
			self.assertIn("not on part construction", switch["physical"]["notes"], address)
			self.assertIn("runtime.fish-tales.switch-edges", switch["provenance"]["source_refs"], address)
		for address in (47, 48):
			switch = self.switches[address]
			self.assertFalse(switch["normally_closed"], address)
			self.assertEqual("microswitch", switch["physical"]["switch_type"], address)
			self.assertIn("never inverts them", switch["physical"]["notes"], address)
			self.assertIn("runtime.fish-tales.switch-edges", switch["provenance"]["source_refs"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertFalse(switch["normally_closed"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_reel_opto_mask_bit_arithmetic(self) -> None:
		import curate_fish_tales as curator

		# core_setSw/core_getSw index invSw by wpc_sw2m(no)/8 with wpc_sw2m(no) = (no/10)*8 + (no%10-1),
		# so mask index 3 is matrix column 3 and 0xc0 inverts rows 7/8: public 37/38, not 47/48.
		mask = (0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

		def sw2m(number: int) -> int:
			return (number // 10) * 8 + (number % 10 - 1)

		inverted = {number for number in MATRIX_ADDRESSES if (mask[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual({37, 38}, inverted)
		self.assertEqual(inverted, curator.PINMAME_NORMALIZED_SWITCHES)
		self.assertEqual(inverted, curator.ROM_ACTIVE_AT_PUBLIC_ZERO)

	def test_reel_positions_follow_rotate_reel_in_public_level_terms(self) -> None:
		# ft_handleMech's guessed windows set public 1 on 37/38, which the ROM reads as inactive, so no
		# mechanism text may call the optos closed there; the positions follow the table's RotateReel.
		self.assertEqual(
			[(0, 50), (60, 80), (120, 140), (180, 200), (240, 260), (300, 320)],
			rotate_reel_public_one_windows(37),
		)
		self.assertEqual(
			[(0, 20), (30, 50), (90, 110), (150, 170), (210, 230), (270, 290), (330, 360)],
			rotate_reel_public_one_windows(38),
		)
		reel = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.reel")
		positions = {position["id"]: position for position in reel["positions"]}
		for position_id, address in (("opto-1", 37), ("opto-2", 38)):
			position = positions[position_id]
			self.assertEqual([f"switch.matrix-{address}"], position["sensors"])
			text = position["description"]
			self.assertIn("RotateReel", text)
			self.assertIn(f"public {address} = 1", text)
			self.assertIn("ROM-inactive", text)
			self.assertIn("public 0 (made, ROM-active) elsewhere", text)
			windows = ", ".join(f"{start}-{end}" for start, end in rotate_reel_public_one_windows(address))
			self.assertIn(windows.rsplit(", ", 1)[0], text)
			self.assertIn(windows.rsplit(", ", 1)[1], text)
		for mechanism in self.definition["mechanisms"]:
			mechanism_positions = mechanism.get("positions", [])
			texts = [mechanism["behavior"]] + [position["description"] for position in mechanism_positions]
			for position in mechanism_positions:
				if {"switch.matrix-37", "switch.matrix-38"} & set(position["sensors"]):
					self.assertNotRegex(position["description"], r"(?i)\bclosed\b")
			for text in texts:
				self.assertNotRegex(text, r"(?i)closed (during|only at)[^.]*(lock|release|ball ?1 ?up)")
		self.assertIn("ROM reads those optos as inactive", reel["behavior"])
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("public-1 windows are where the ROM reads the\noptos as *inactive*", knowledge)

	def test_no_upper_flippers_despite_the_driver_declaration(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
			self.assertNotIn("wiring", self.switches[address], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		for address in sorted(NOT_FITTED_UPPER_FLIPPER_SOLENOIDS):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)
			self.assertIn("not fitted", self.solenoids[address]["physical"]["notes"].lower())
		# No conflicts entry documents the flipper-fitment disagreement -- it is a resolved finding,
		# not an open one, matching this project's precedent for asymmetric-evidence corrections.
		conflict_ids = {conflict["id"] for conflict in self.definition["conflicts"]}
		self.assertFalse(any("flipper" in identifier for identifier in conflict_ids))

	def test_lower_flipper_supply_and_drive_connections_are_distinct(self) -> None:
		expected = {
			45: ("J907-8, 9", "J902-13"),
			46: ("J907-8, 9", "J902-11"),
			47: ("J907-6, 7", "J902-9"),
			48: ("J907-6, 7", "J902-7"),
		}
		for address, (power, control) in expected.items():
			self.assertEqual(power, self.solenoids[address]["wiring"]["power_connection"], address)
			self.assertEqual(control, self.solenoids[address]["wiring"]["control_connection"], address)

	def test_fake_reel_solenoids_are_virtual_pinmame_only_bookkeeping(self) -> None:
		for address in sorted(FAKE_REEL_SOLENOIDS):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"], address)
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("virtual", device["spatial"]["reason"], address)
			self.assertIn("CORE_CUSTSOLNO", device["physical"]["notes"], address)
		self.assertIn("never references", self.solenoids[51]["physical"]["notes"])

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 54))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 28):
			if address == 24:
				continue
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		self.assertEqual("flasher", self.solenoids[24]["kind"])
		self.assertEqual("unused", self.solenoids[24]["availability"])
		self.assertEqual("motor", self.solenoids[28]["kind"])
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50, 51, 52, 53):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in (29, 30, 31):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		self.assertEqual("unused", self.solenoids[32]["availability"])
		self.assertEqual(["internal.unused.wpc-output"], self.solenoids[32]["roles"])

	def test_knocker_and_backbox_fish_are_cabinet_devices_not_playfield(self) -> None:
		for address, label in ((7, "Knocker"), (8, "Backbox Fish")):
			device = self.solenoids[address]
			self.assertEqual(label, device["label"])
			self.assertEqual("used", device["availability"])
			self.assertEqual("not_applicable", device["spatial"]["status"])
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (2, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(21, len(self.gi[2]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[4]["spatial"]["placements"]))
		for address in (0, 1, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamps_16_17_18_are_backbox_devices_despite_matching_boat_switch_theme(self) -> None:
		for address in (16, 17, 18):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], lamp["roles"], address)
		for address in (44, 45, 46):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"], address)

	def test_lamp_48_has_two_disclosed_placements_and_no_lamp_is_unused(self) -> None:
		self.assertEqual(2, self.lamps[48]["physical"]["quantity"])
		self.assertEqual(2, len(self.lamps[48]["spatial"]["placements"]))
		self.assertIn("inferred", self.lamps[48]["physical"]["notes"].lower())
		for lamp in self.lamps.values():
			self.assertEqual("used", lamp["availability"], lamp["id"])

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable":
				continue
			self.assertEqual("validated", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				located += 1
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				self.assertEqual("playfield", placement["space"])
				for axis in ("x", "y"):
					self.assertGreaterEqual(placement[axis], 0.0)
					self.assertLessEqual(placement[axis], 1.0)
					self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)
				self.assertEqual("validated", placement["provenance"]["status"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("validated", report["status"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual(located, report["placement_count"])

	def test_reel_opto_switches_are_projected_onto_the_reel_object(self) -> None:
		for address in (37, 38):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"])
			placement = switch["spatial"]["placements"][0]
			self.assertAlmostEqual(0.122796, placement["x"], places=6)
			self.assertAlmostEqual(0.457965, placement["y"], places=6)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		lamp_y = {addr: pos[1] for addr, pos in _emitter_positions(self.lamps).items()}
		# Left jet bumper (51) is left of right jet bumper (53); center (52) sits between them.
		self.assertLess(switch_x[51], switch_x[52])
		self.assertLess(switch_x[52], switch_x[53])
		# Left slingshot is left of right slingshot.
		self.assertLess(switch_x[57], switch_x[58])
		# Left standup targets are left of right standup targets.
		self.assertLess(switch_x[27], switch_x[54])
		self.assertLess(switch_x[28], switch_x[55])
		# Left/right boat entry and exit lanes keep left-right ordering.
		self.assertLess(switch_x[43], switch_x[42])
		# Left fish lamps (45-47) sit left of the matching right fish lamps (55-57).
		self.assertLess(lamp_x[45], lamp_x[55])
		self.assertLess(lamp_x[46], lamp_x[56])
		self.assertLess(lamp_x[47], lamp_x[57])
		# Trough position 1 (nearest the release exit) sits closer to the shooter lane (larger x,
		# toward the Plunger at x=0.939) than trough position 3 (nearest the outhole).
		self.assertGreater(switch_x[16], switch_x[18])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.reel", "mechanism.catapult",
				"mechanism.casters-club", "mechanism.fish-finder", "mechanism.gate",
				"mechanism.drop-target-ramp", "mechanism.jet-bumpers", "mechanism.slingshots",
				"mechanism.knocker", "mechanism.backbox-fish", "mechanism.boat",
				"mechanism.lower-flippers",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("reel", mechanisms["mechanism.reel"]["kind"])
		self.assertIn("Habit Trail", mechanisms["mechanism.casters-club"]["behavior"])

	def test_relationships_field_is_present_and_empty(self) -> None:
		# No causal solenoid-to-different-switch pulse relationship was independently evidenced for
		# this machine's trough/catapult/reel routing beyond ordinary direct switch assertions, so
		# the (schema-optional, non-empty-not-required) relationships array stays empty rather than
		# asserting an unevidenced causal link.
		self.assertEqual([], self.definition["relationships"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.ft-vpw-1-1", sources)
		self.assertTrue(sources["vpx-script.ft-vpw-1-1"]["known_working"])
		self.assertEqual(
			"b6289a7087f11bd1902d8b059fe663723a6319c6490d1a2fa124d3dd7089e1f5",
			sources["vpx-script.ft-vpw-1-1"]["sha256"],
		)
		self.assertEqual(
			"1f82c0237831b50c514e53c8938636f59ee584fc4346c143a3216b9f5d8a1029",
			sources["vpx-table.ft-vpw-1-1"]["sha256"],
		)
		self.assertNotIn("rom.ft", sources)
		runtime = [source["id"] for source in self.definition["sources"] if source["kind"] == "runtime_scenario"]
		self.assertEqual(["runtime.fish-tales.switch-edges", "runtime.the-addams-family.switch-edges-control"], runtime)
		self.assertEqual(
			"internal:evidence/runtime/wpc-fliptronic/fish-tales-switch-edges.json",
			sources["runtime.fish-tales.switch-edges"]["uri"],
		)
		for source in self.definition["sources"]:
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_manual_source_excerpts_are_reviewed_and_hashed(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.williams.fish-tales.1992"]
		excerpts = manual.get("excerpts") or []
		self.assertGreaterEqual(len(excerpts), 7)
		for excerpt in excerpts:
			self.assertTrue(excerpt["reviewed"])
			self.assertEqual("manual", excerpt["method"])
			self.assertTrue((ROOT / excerpt["path"]).is_file(), excerpt["path"])

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])
		groups = {group["id"]: group for group in profile["groups"]}
		used = {device["binding"]["group"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		self.assertTrue(used <= set(groups))

		def allowed(group_id: str, address: int) -> bool:
			for rule in groups[group_id]["address_rules"]:
				if "values" in rule and address in rule["values"]:
					return True
				if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
					return True
			return False

		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			self.assertTrue(allowed(device["binding"]["group"], device["binding"]["device"]), device["id"])


def _switch_positions(switches: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in switches.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


def _emitter_positions(lamps: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in lamps.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class FishTalesCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_fish_tales as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_fish_tales as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_fish_tales as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Fish Tales", b"Fish Sales", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_fish_tales as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class FishTalesRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_fish_tales as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_fish_tales as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/fish-tales-1992/source/Fish Tales (Williams 1992) VPW 1.1.vpx"
		script = source_root / "williams/fish-tales-1992/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_rotate_reel_transcription_matches_the_retained_script(self) -> None:
		import curate_fish_tales as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		script = (source_root / "williams/fish-tales-1992/extracted-vpxtool/script.vbs").read_text(encoding="utf-8", errors="replace")
		pattern = re.compile(
			r"Case\s+\(ReelPosition >= (\d+) and ReelPosition < (\d+)\)\s*:\s*sw38 = ([01])\s*:\s*sw37 = ([01])"
		)
		cases = tuple(tuple(int(value) for value in match.groups()) for match in pattern.finditer(script))
		self.assertEqual(ROTATE_REEL_CASES, cases)

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_fish_tales as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "fish-tales" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
