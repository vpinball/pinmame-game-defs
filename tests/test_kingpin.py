from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import unresolved_conflicts
from pinmame_game_defs.workspace import resolve_working_root


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/capcom/kingpin-1996.json"
EXCERPTS = ROOT / "evidence/excerpts/capcom.kingpin.1996"
RUNTIME_EVIDENCE = ROOT / "evidence/runtime/capcom/kingpin-service-diagnostics.json"

_spec = importlib.util.spec_from_file_location("curate_kingpin", ROOT / "tools" / "curate_kingpin.py")
CURATOR = importlib.util.module_from_spec(_spec)
sys.modules["curate_kingpin"] = CURATOR
_spec.loader.exec_module(CURATOR)

_rom_spec = importlib.util.spec_from_file_location("capcom_kingpin_rom_records", ROOT / "tools" / "capcom_kingpin_rom_records.py")
ROM_TOOL = importlib.util.module_from_spec(_rom_spec)
_rom_spec.loader.exec_module(ROM_TOOL)

# capInvSw11 from pinned src/wpc/capgames.c, indexed by internal switch column; bit n is row n.
CAP_INV_SW11 = [0, 0x01, 0x00, 0x78, 0x88, 0x08, 0x10]


def tables(name: str) -> list[list[list[str]]]:
	"""Every markdown table in an excerpt, as body rows (header and rule removed)."""
	found: list[list[list[str]]] = []
	previous_was_table = False
	for line in (EXCERPTS / name).read_text(encoding="utf-8").splitlines():
		is_table = line.startswith("| ")
		if is_table and not previous_was_table:
			found.append([])
		if is_table and not line.startswith("| ---"):
			found[-1].append([cell.strip() for cell in line.strip("|").split("|")])
		previous_was_table = is_table
	return [table[1:] for table in found]


def table_rows(name: str, columns: int | None = None) -> list[list[str]]:
	return tables(name)[0] if columns is None else [row for row in tables(name)[0] if len(row) == columns]


class KingpinDefinitionTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.by_binding = {
			(device["binding"]["group"], device["binding"]["device"]): device
			for device in cls.definition["inputs"] + cls.definition["outputs"]
		}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_curator_output_is_committed_byte_for_byte(self) -> None:
		# covers the definition, the pinned seed and the knowledge note
		CURATOR.check(ROOT)

	def test_single_physical_driver(self) -> None:
		self.assertEqual(["kpb105"], [driver["id"] for driver in self.definition["drivers"]])
		self.assertEqual("capcom.kingpin.1996", self.definition["machine"]["id"])
		self.assertEqual(4000, self.definition["machine"]["ipdb_id"])
		self.assertEqual("pinmame.capcom", self.definition["controller"]["platform"])

	def test_complete_address_enumeration(self) -> None:
		switches = {address for group, address in self.by_binding if group == "pinmame.input.switch"}
		solenoids = {address for group, address in self.by_binding if group == "pinmame.output.solenoid"}
		lamps = {address for group, address in self.by_binding if group == "pinmame.output.lamp"}
		self.assertEqual(set(range(1, 82)) | {82, 84, 89}, switches)
		self.assertEqual(set(range(1, 52)), solenoids)
		self.assertEqual(set(range(1, 137)), lamps)

	def test_opto_set_agrees_across_pinmame_rom_and_krellan(self) -> None:
		mask_optos = {9 + row + column * 8 for column, byte in enumerate(CAP_INV_SW11) for row in range(8) if byte >> row & 1}
		rom_optos = {int(row[3]) for row in table_rows("rom-io-name-records.md", 7) if row[1] == "switch" and row[5] == "yes"}
		krellan_optos = {int(row[0]) for row in table_rows("krellan-switch-table.md") if "(italic: opto)" in row[1]}
		definition_optos = {
			address for (group, address), device in self.by_binding.items()
			if group == "pinmame.input.switch" and device.get("physical", {}).get("switch_type") == "opto"
		}
		self.assertEqual({17, 36, 37, 38, 39, 44, 48, 52, 61}, mask_optos)
		self.assertEqual(mask_optos, rom_optos)
		self.assertEqual(mask_optos, krellan_optos)
		self.assertEqual(mask_optos, definition_optos)
		for address in mask_optos:
			self.assertTrue(self.device("input.switch", address)["normally_closed"])

	def test_flipper_buttons_are_driven_through_pinmame_button_bits(self) -> None:
		# src/wpc/core.h: CORE_SWLRFLIPBUTBIT 0x02 and CORE_SWLLFLIPBUTBIT 0x08 in CORE_FLIPPERSWCOL (11);
		# cc_m2sw maps internal column 11 row r to public 81 + r. core_updateSw copies them into FLIP_SWNO(5,6).
		for bit, physical in ((0x02, 6), (0x08, 5)):
			public = 81 + bit.bit_length() - 1
			host = self.device("input.switch", public)
			self.assertEqual(("virtual", "used"), (host["kind"], host["availability"]))
			self.assertIn(f"matrix switch {physical} every frame", host["physical"]["notes"])
			self.assertIn(f"public {public}", self.device("input.switch", physical)["physical"]["notes"])
		for scenario in (ROOT / "tools/harness-scenarios/capcom").glob("kpb105-*.json"):
			actions = load_json(scenario)["actions"]
			self.assertFalse([action for action in actions if action.get("switch") in (5, 6)], scenario.name)

	def test_excerpts_agree_with_the_runtime_evidence_bundle(self) -> None:
		observations = load_json(RUNTIME_EVIDENCE)["runtime"]["observations"]
		self.assertEqual({str(n): n for n in range(1, 33)}, observations["physical_service_solenoid_to_public"])
		snapshots = {snapshot["label"].split(":")[0]: snapshot["interpreted_text"] for snapshot in observations["diagnostic_snapshots"]}
		for row in table_rows("service-solenoid-test.md"):
			number = int(row[0][1:])
			self.assertEqual(f"{row[1]} / {row[2]} / {row[3]}", snapshots[f"solenoid {number}"])
		for row in table_rows("service-lamp-test.md"):
			self.assertEqual(f"{row[0]} / {row[2]} / {row[3]} / {row[4]}", snapshots[f"lamp {row[1]}"])

	def test_rom_record_conversions(self) -> None:
		self.assertEqual(3, ROM_TOOL.lamp_public(0x27))
		self.assertEqual(121, ROM_TOOL.lamp_public(0x08))
		self.assertEqual(126, ROM_TOOL.lamp_public(0x58))
		self.assertEqual(17, ROM_TOOL.switch_public(0x18))
		self.assertEqual(47, ROM_TOOL.switch_public(0x4E))
		self.assertEqual(14, ROM_TOOL.switch_public(0x05))
		self.assertEqual(1, ROM_TOOL.coil_public(15))
		self.assertEqual(11, ROM_TOOL.coil_public(29))
		self.assertEqual(17, ROM_TOOL.coil_public(7))
		self.assertEqual(32, ROM_TOOL.coil_public(16))
		for row in table_rows("rom-io-name-records.md", 7):
			kind, number, public = row[1], int(row[2]), int(row[3])
			converted = {"lamp": ROM_TOOL.lamp_public, "switch": ROM_TOOL.switch_public, "coil": ROM_TOOL.coil_public}[kind](number)
			self.assertEqual(converted, public, row)

	def test_solenoid_test_pairs_every_displayed_coil_with_its_public_address(self) -> None:
		rows = table_rows("service-solenoid-test.md")
		self.assertEqual([f"S{n:02d}" for n in range(1, 33)], [row[0] for row in rows])
		for row in rows:
			number = int(row[0][1:])
			fired = {int(value) for value in row[4].split(",")}
			# Public 20 pulses through the whole test, so its own step cannot isolate it;
			# every other step must fire exactly the displayed S-number.
			self.assertIn(20, fired, row)
			if number != 20:
				self.assertIn(number, fired, row)
			self.assertEqual((row[1], row[2], row[3]), CURATOR.DIAG_SOLENOIDS[number])
		self.assertIn("cannot isolate it", self.device("output.solenoid", 20)["physical"]["notes"])

	def test_switch_test_prints_the_public_address(self) -> None:
		held, browsed = tables("service-switch-test.md")
		self.assertEqual(set(range(1, 5)) | set(range(9, 81)), {int(row[0]) for row in held})
		for row in held:
			self.assertEqual(int(row[0]), int(row[1]), row)
			self.assertEqual((row[2], row[3], row[4]), CURATOR.DIAG_SWITCHES[int(row[0])])
		# 05-08 carry the menu navigation, so they were browsed with the flipper buttons, not held
		self.assertEqual({5: "LEFT FLIPPER", 6: "RIGHT FLIPPER", 7: "START BUTTON", 8: "COIN DOOR"}, {int(row[0]): row[1] for row in browsed})
		for row in browsed:
			self.assertEqual((row[1], row[2], row[3]), CURATOR.DIAG_SWITCHES[int(row[0])])

	def test_lamp_test_lights_the_displayed_matrix_position(self) -> None:
		rows = table_rows("service-lamp-test.md")
		self.assertEqual(set(range(1, 129)), {int(row[1]) for row in rows})
		for row in rows:
			code, public, name = row[0], int(row[1]), row[2]
			column, matrix_row, bank = int(code[0]), int(code[1]), code[2]
			self.assertEqual(public, (column - 1) * 8 + matrix_row + (64 if bank == "B" else 0))
			if name == "NOT USED":
				# the ROM lights every matrix lamp while a NOT USED position is selected
				self.assertEqual("all 1-128", row[5], row)
			else:
				self.assertIn(public, {int(value) for value in row[5].split(",")}, row)
			self.assertEqual((code, name, row[3], row[4]), CURATOR.DIAG_LAMPS[public])
		self.assertEqual({123, 124, 125}, {int(row[1]) for row in rows if row[2] == "NOT USED"})

	def test_not_used_positions_are_unused(self) -> None:
		switch_not_used = {int(row[0]) for row in table_rows("service-switch-test.md") if row[2] == "NOT USED"}
		lamp_not_used = {int(row[1]) for row in table_rows("service-lamp-test.md") if row[2] == "NOT USED"}
		self.assertTrue(switch_not_used and lamp_not_used)
		for address in range(1, 81):
			# Krellan: 13/15 serve an optional token dispenser and 16 an optional ticket dispenser
			expected = "unused" if address in switch_not_used else "optional" if address in {13, 15, 16} else "used"
			self.assertEqual(expected, self.device("input.switch", address)["availability"], address)
		for address in range(1, 129):
			expected = "unused" if address in lamp_not_used else "used"
			self.assertEqual(expected, self.device("output.lamp", address)["availability"], address)
		for address in (34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50):
			self.assertEqual("unused", self.device("output.solenoid", address)["availability"], address)

	def test_output_kinds_follow_the_rom(self) -> None:
		for address in range(18, 32):
			self.assertEqual("flasher", self.device("output.solenoid", address)["kind"], address)
		self.assertEqual("motor", self.device("output.solenoid", 12)["kind"])
		self.assertEqual(12.0, self.device("output.solenoid", 12)["wiring"]["nominal_voltage_v"])
		self.assertEqual("backbox", self.device("output.solenoid", 20)["physical"]["location"])
		for address, target in ((33, 11), (35, 12), (45, 9), (47, 10)):
			mirror = self.device("output.solenoid", address)
			self.assertEqual("virtual", mirror["kind"])
			self.assertIn(f"physical solenoid {target}", mirror["physical"]["notes"])

	def test_table_defects_are_device_notes_not_conflicts(self) -> None:
		self.assertIn("sw32_Hit : vpmTimer.PulseSw 49", self.device("input.switch", 32)["physical"]["notes"])
		self.assertIn("SolCallback(23)", self.device("output.solenoid", 22)["physical"]["notes"])
		for conflict in self.definition["conflicts"]:
			self.assertNotIn("sw32", conflict["description"])

	def test_conflicts_name_a_resolution_path(self) -> None:
		self.assertEqual(["conflict.flasher-29-orbit-side"], [conflict["id"] for conflict in unresolved_conflicts(self.definition)])
		for conflict in self.definition["conflicts"]:
			self.assertIn("Resolution path:", conflict["description"])
		self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

	def test_ramp_feedback_is_not_claimed_as_a_physical_relationship(self) -> None:
		# The run shows switch 47 gating the ROM's drive of coil 14 (software feedback), not the
		# coil working the switch, so no relationship is asserted and the mechanism stays observed.
		self.assertEqual([], self.definition["relationships"])
		ramp = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.left-ramp-entrance")
		self.assertEqual("observed", ramp["provenance"]["status"])
		self.assertIn(CURATOR.RAMP_RUN_SOURCE, ramp["provenance"]["source_refs"])
		self.assertIn("1.3 s", ramp["behavior"])

	def test_harness_sources_pin_their_raw_runs(self) -> None:
		evidence = load_json(RUNTIME_EVIDENCE)
		runs = {run["name"]: run for run in evidence["runtime"]["raw_runs"]}
		self.assertEqual({f"kpb105-{name}" for name in ("solenoid-test", "lamp-test", "switch-test", "opto-test", "ramp-down-feedback", "ball-serve")}, set(runs))
		for run in runs.values():
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest(), run["name"])
		evidence_sha = hashlib.sha256(RUNTIME_EVIDENCE.read_bytes()).hexdigest()
		harness_sources = [source for source in self.definition["sources"] if source["kind"] in {"service_diagnostic", "runtime_scenario"}]
		self.assertEqual(6, len(harness_sources))
		for source in harness_sources:
			self.assertEqual("internal:evidence/runtime/capcom/kingpin-service-diagnostics.json", source["uri"])
			self.assertEqual(evidence_sha, source["sha256"])
			named = [name for name in runs if f"raw run {name} " in source["locator"]]
			self.assertEqual(1, len(named), source["id"])
			self.assertIn(runs[named[0]]["sha256"], source["locator"])

	def test_excerpt_address_columns_recompute_from_the_raw_runs(self) -> None:
		working_root = resolve_working_root(ROOT)
		runs_root = working_root / "review-artifacts/kingpin/harness-runs" if working_root else None
		if runs_root is None or not runs_root.is_dir():
			self.skipTest("retained Kingpin harness runs are not available")

		def switched_on(step: dict, kind: str) -> set[int]:
			return {item["number"] for item in step["transitions"][kind] if any(value > 0 for value in item["states"])}

		steps = load_json(runs_root / "final-solenoid-test/run.json")["steps"]
		selections = [step for step in steps if step["label"].startswith(("Start: enter SOLENOID TEST", "right flipper: select the next coil"))]
		self.assertGreaterEqual(len(selections), 32)
		for row, step in zip(table_rows("service-solenoid-test.md"), selections):
			self.assertEqual({int(value) for value in row[4].split(",")}, switched_on(step, "solenoids"), row[0])
		forward = [step for step in load_json(runs_root / "final-lamp-test/run.json")["steps"] if step["label"].startswith("right flipper: single lamp step")]
		self.assertGreaterEqual(len(forward), 128)
		for row in table_rows("service-lamp-test.md"):
			public = int(row[1])
			lit = {number for number in switched_on(forward[public - 1], "lamps") if number <= 128}
			expected = set(range(1, 129)) if row[5] == "all 1-128" else {int(value) for value in row[5].split(",")}
			self.assertEqual(expected, lit, row[0])

	def test_retained_raw_runs_match_their_pinned_hashes(self) -> None:
		working_root = resolve_working_root(ROOT)
		runs_root = working_root / "review-artifacts/kingpin/harness-runs" if working_root else None
		if runs_root is None or not runs_root.is_dir():
			self.skipTest("retained Kingpin harness runs are not available")
		for run in load_json(RUNTIME_EVIDENCE)["runtime"]["raw_runs"]:
			path = runs_root / f"final-{run['name'].removeprefix('kpb105-')}" / "run.json"
			self.assertEqual(run["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run["name"])

	def test_excerpt_digests_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest())
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest())

	def test_script_sources_are_not_claimed_known_working(self) -> None:
		for source in self.definition["sources"]:
			if source["kind"] == "vpx_script":
				self.assertFalse(source["known_working"])
				self.assertIn("/blob/", source["uri"])

	def test_labels_expand_rom_abbreviations(self) -> None:
		self.assertEqual("Upper Right Charmed Life", CURATOR.lamp_label("U.R. CHARMED LIFE"))
		self.assertEqual("Left Ramp Powerup", CURATOR.lamp_label("L. RAMP POWERUP"))
		self.assertEqual("G.I. 33", CURATOR.lamp_label("G.I. 33 (2,RED)"))
		self.assertEqual("Backbox G.I.", CURATOR.lamp_label("BACKBOX G.I.(2)"))
		self.assertEqual((2, True), CURATOR.lamp_bulbs("G.I. 33 (2,RED)"))
		self.assertEqual((2, False), CURATOR.lamp_bulbs("BACKBOX G.I.(2)"))
		self.assertEqual("Bump & Roll'em", CURATOR.lamp_label("BUMP & ROLL'EM"))
		self.assertEqual("Left You're Covered", CURATOR.lamp_label("L. YOU'RE COVERED"))
		self.assertEqual("Coin 1/Coin 3", CURATOR.lamp_label("COIN 1/COIN 3"))
		self.assertEqual("4X .45 Automatic", CURATOR.lamp_label("4X .45 AUTOMATIC"))


if __name__ == "__main__":
	unittest.main()
