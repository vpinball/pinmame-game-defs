from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json
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


# The C1.01 Switch Test draws each switch's state as an icon in the left half of the DMD (one string per row, "#" lit).
SWITCH_TEST_ICONS = {
	"###/#.#": "contact closed",
	"..#/.#./#../#.#": "contact open",
	"###/.../.../###": "beam broken",
	"###/.#./.#./###": "beam clear",
}


def switch_test_icon(path: Path) -> str:
	data = path.read_bytes()
	header = b"P5\n128 32\n255\n"
	if not data.startswith(header) or len(data) != len(header) + 128 * 32:
		raise AssertionError(f"unexpected DMD frame format: {path}")
	pixels = data[len(header):]
	# the left panel's rows 1-6 and 9-30 hold the icon; rows 0, 7-8 and 31 are its frame
	lit = {(row, column) for row in [*range(1, 7), *range(9, 31)] for column in range(63) if pixels[row * 128 + column] > 200}
	rows = range(min(row for row, _ in lit), max(row for row, _ in lit) + 1)
	columns = range(min(column for _, column in lit), max(column for _, column in lit) + 1)
	return SWITCH_TEST_ICONS["/".join("".join("#" if (row, column) in lit else "." for column in columns) for row in rows)]


def icon_cell(path: Path) -> tuple[int, int]:
	"""Bottom-left corner of the lit (bright) icon in the left panel of a Switch Test or Troubleshooting frame.

	The closed-contact icon is two rows tall and the raised lever four, but both end on the same row and column of the cell.
	"""
	pixels = path.read_bytes()[len(b"P5\n128 32\n255\n"):]
	lit = [(row, column) for row in [*range(1, 7), *range(9, 31)] for column in range(63) if pixels[row * 128 + column] > 200]
	return max(row for row, _ in lit), min(column for _, column in lit)


def troubleshooting_runs() -> dict[str, tuple[set[int], list[list[str]]]]:
	"""Each run's switches held at 1 (from the excerpt's prose) and its message table."""
	text = (EXCERPTS / "service-troubleshooting.md").read_text(encoding="utf-8")
	runs = {}
	for name, table in zip(re.findall(r"^## Run `([a-z-]+)`", text, re.M), tables("service-troubleshooting.md")):
		held_text = re.search(r"## Run `" + name + r"`\n\nHeld at public 1 from power-up: ([0-9, -]+)\.", text)
		held = set()
		for part in held_text.group(1).split(", "):
			low, _, high = part.partition("-")
			held |= set(range(int(low), int(high or low) + 1))
		runs[name] = (held, table)
	return runs


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

	def test_switch_test_icons_fix_every_contact_polarity(self) -> None:
		held, browsed = tables("service-switch-test.md")
		icons = {int(row[0]): (row[5], row[6]) for row in held}
		self.assertEqual(CURATOR.OPTO_SWITCHES, {address for address, pair in icons.items() if pair == ("beam broken", "beam clear")})
		self.assertEqual(set(icons) - CURATOR.OPTO_SWITCHES, {address for address, pair in icons.items() if pair == ("contact closed", "contact open")})
		# browsed entries: the buttons were released, the coin door switch stayed at 1 from the step that opened the menu
		self.assertEqual(
			{5: ("0", "contact open"), 6: ("0", "contact open"), 7: ("0", "contact open"), 8: ("1", "contact closed")},
			{int(row[0]): (row[5], row[6]) for row in browsed},
		)
		for address in range(1, 81):
			device = self.device("input.switch", address)
			if device["availability"] == "unused":
				self.assertNotIn("normally_closed", device, address)
			else:
				self.assertIs(address in CURATOR.OPTO_SWITCHES, device["normally_closed"], address)
		self.assertNotIn("polarity", self.definition["coverage"]["missing"])

	def test_troubleshooting_excerpt_matches_its_scenarios(self) -> None:
		for name, (held, _table) in troubleshooting_runs().items():
			scenario = load_json(ROOT / f"tools/harness-scenarios/capcom/kpb105-troubleshooting-{name}.json")
			self.assertEqual({item["switch"] for item in scenario["initial_switches"] if item["state"] == 1}, held, name)
			self.assertFalse({item["switch"] for item in scenario["initial_switches"] if item["state"] != 1}, name)

	def test_troubleshooting_report_fixes_the_rest_level_it_checks(self) -> None:
		parsed = troubleshooting_runs()
		runs = {name: {int(row[1]) for row in table if row[1] != "lamp"} for name, (_held, table) in parsed.items()}
		held = parsed["held"][0]
		self.assertEqual(set(), runs["baseline"])
		self.assertEqual({9, 10}, runs["slam-tilt"])
		self.assertEqual(CURATOR.TROUBLESHOOTING_REPORTED_AT_1, (runs["held"] & held) | runs["slam-tilt"])
		self.assertEqual(CURATOR.TROUBLESHOOTING_REPORTED_AT_0, runs["held"] - held)
		self.assertEqual(CURATOR.TROUBLESHOOTING_UNCHECKED, held - runs["held"] - CURATOR.OPTO_SWITCHES)
		self.assertTrue({9, 33, 34} <= CURATOR.TROUBLESHOOTING_REPORTED_AT_1)
		for address in range(1, 81):
			device = self.device("input.switch", address)
			if device["availability"] == "unused" or address in CURATOR.OPTO_SWITCHES:
				continue
			notes = device["physical"]["notes"]
			refs = device["provenance"]["source_refs"]
			if address in CURATOR.TROUBLESHOOTING_REPORTED_AT_1 | CURATOR.TROUBLESHOOTING_REPORTED_AT_0:
				self.assertIn("C5 Troubleshooting report lists this switch", notes, address)
				self.assertIn(CURATOR.TROUBLESHOOTING_BASELINE_SOURCE, refs, address)
			elif address in CURATOR.DROP_TARGET_RESET:
				self.assertIn("In the drop-target run, a game with every target at 0 draws no reset", notes, address)
				self.assertIn(CURATOR.DROP_RUN_SOURCE, refs, address)
			else:
				self.assertIn("ordinary construction", notes, address)
			if address in CURATOR.TROUBLESHOOTING_UNCHECKED:
				self.assertIn(CURATOR.TROUBLESHOOTING_BASELINE_SOURCE, refs, address)
				self.assertIn(CURATOR.TROUBLESHOOTING_HELD_SOURCE, refs, address)

	def test_committed_drop_target_observations_and_bank_membership(self) -> None:
		observations = load_json(RUNTIME_EVIDENCE)["runtime"]["observations"]["runs"]["kpb105-drop-targets"]["named_action_observations"]
		fired = {item["label"]: set(item["active_solenoid_addresses"]) for item in observations}
		self.assertFalse({6, 7} & fired["play with all seven drop targets at 0 (standing): control window"])
		self.assertFalse({6, 7} & fired["KING: one target down (25 at 1), a single target that should not reset the bank"])
		self.assertIn(6, fired["KING: 28 down, all four KING targets at 1"])
		self.assertNotIn(7, fired["KING: 28 down, all four KING targets at 1"])
		self.assertIn(7, fired["PIN: 31 down, all three PIN targets at 1"])
		self.assertNotIn(6, fired["PIN: 31 down, all three PIN targets at 1"])
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		for mechanism_id, coil in (("mechanism.king-drop-targets", 6), ("mechanism.pin-drop-targets", 7)):
			mechanism = mechanisms[mechanism_id]
			self.assertEqual([f"solenoid.{coil}"], mechanism["actuators"])
			self.assertEqual(
				sorted(f"switch.{address}" for address, reset in CURATOR.DROP_TARGET_RESET.items() if reset == coil),
				sorted(mechanism["sensors"]),
			)

	def test_drop_target_run_resets_a_bank_only_when_all_its_targets_read_1(self) -> None:
		working_root = resolve_working_root(ROOT)
		path = working_root / "review-artifacts/kingpin/harness-runs/final-drop-targets/run.json" if working_root else None
		if path is None or not path.is_file():
			self.skipTest("retained Kingpin drop-target run is not available")
		steps = {step["label"]: step for step in load_json(path)["steps"]}

		def fired(label: str) -> set[int]:
			return {item["number"] for item in steps[label]["transitions"]["solenoids"] if any(value > 0 for value in item["states"])}

		self.assertFalse({6, 7} & fired("play with all seven drop targets at 0 (standing): control window"))
		self.assertFalse({6, 7} & fired("KING: one target down (25 at 1), a single target that should not reset the bank"))
		self.assertIn(6, fired("KING: 28 down, all four KING targets at 1"))
		self.assertFalse({6, 7} & fired("KING: 28 back up, all four at 0"))
		self.assertIn(7, fired("PIN: 31 down, all three PIN targets at 1"))
		self.assertFalse({6, 7} & fired("PIN: 31 back up, all three at 0"))

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
		self.assertEqual(
			{f"kpb105-{name}" for name in (
				"solenoid-test", "lamp-test", "switch-test", "opto-test", "ramp-down-feedback", "ball-serve",
				"troubleshooting-baseline", "troubleshooting-held", "troubleshooting-slam-tilt", "drop-targets",
			)},
			set(runs),
		)
		for run in runs.values():
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest(), run["name"])
		evidence_sha = hashlib.sha256(RUNTIME_EVIDENCE.read_bytes()).hexdigest()
		harness_sources = [source for source in self.definition["sources"] if source["kind"] in {"service_diagnostic", "runtime_scenario"}]
		self.assertEqual(10, len(harness_sources))
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

	def test_excerpt_icons_recompute_from_the_raw_frames(self) -> None:
		working_root = resolve_working_root(ROOT)
		frames = working_root / "review-artifacts/kingpin/harness-runs/final-switch-test/dmd" if working_root else None
		if frames is None or not frames.is_dir():
			self.skipTest("retained Kingpin harness frames are not available")
		held, browsed = tables("service-switch-test.md")
		for row in held:
			prefix = f"-hold-public-switch-{row[0]}-while-the-switch-test-names-it"
			(pressed,) = [path for path in frames.iterdir() if path.name.endswith(prefix + "-held-display-0.pgm")]
			(released,) = [path for path in frames.iterdir() if path.name.endswith(prefix + "-display-0.pgm")]
			self.assertEqual((row[5], row[6]), (switch_test_icon(pressed), switch_test_icon(released)), row[0])
		steps = {int(row[0]): row[4] for row in browsed}
		for address, label in steps.items():
			slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
			(frame,) = [path for path in frames.iterdir() if path.name[4:] == f"{slug}-display-0.pgm"]
			self.assertEqual({int(row[0]): row[6] for row in browsed}[address], switch_test_icon(frame), address)

	def test_troubleshooting_tables_recompute_from_the_raw_frames(self) -> None:
		working_root = resolve_working_root(ROOT)
		runs_root = working_root / "review-artifacts/kingpin/harness-runs" if working_root else None
		if runs_root is None or not (runs_root / "final-troubleshooting-held").is_dir():
			self.skipTest("retained Kingpin harness frames are not available")
		# each switch's icon cell, learned from the Switch Test frames that held it alone
		switch_frames = runs_root / "final-switch-test/dmd"
		cell = {}
		for row in tables("service-switch-test.md")[0]:
			(frame,) = [path for path in switch_frames.iterdir() if path.name.endswith(f"-hold-public-switch-{row[0]}-while-the-switch-test-names-it-held-display-0.pgm")]
			cell[icon_cell(frame)] = int(row[0])
		self.assertEqual(76, len(cell))
		for name, (_held, table) in troubleshooting_runs().items():
			frames = runs_root / f"final-troubleshooting-{name}/dmd"
			# the page after the last transcribed message is the summary screen again, so no message was left out
			(summary,) = [path for path in frames.iterdir() if "-start-enter-c5-troubleshooting-summary-screen-" in path.name]
			(after,) = [path for path in frames.iterdir() if path.name.endswith(f"-right-flipper-troubleshooting-message-{len(table) + 1}-display-0.pgm")]
			self.assertEqual(summary.read_bytes(), after.read_bytes(), name)
			for row in table:
				(frame,) = [path for path in frames.iterdir() if path.name.endswith(f"-right-flipper-troubleshooting-message-{row[0]}-display-0.pgm")]
				if row[1] == "lamp":
					self.assertNotIn(icon_cell(frame), cell, (name, row[0]))
				else:
					self.assertEqual(int(row[1]), cell[icon_cell(frame)], (name, row[0]))

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
				if source["id"] == CURATOR.VPX_TABLE_SCRIPT_SOURCE:
					self.assertTrue(source["uri"].startswith("external:pinmame-vpx-sources/"))
				else:
					self.assertIn("/blob/", source["uri"])

	def test_spatial_placements_are_observed_and_cite_the_retained_table(self) -> None:
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual({"width": 952.0, "height": 2162.0}, {k: self.definition["machine"]["playfield"][k] for k in ("width", "height")})
		located = 0
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			located += 1
			self.assertEqual("observed", spatial["status"], device["id"])
			self.assertIn(device["availability"], {"used", "optional"}, device["id"])
			for placement in spatial["placements"]:
				self.assertEqual("observed", placement["provenance"]["status"])
				refs = placement["provenance"]["source_refs"]
				self.assertEqual([CURATOR.VPX_TABLE_SOURCE, CURATOR.VPX_TABLE_SCRIPT_SOURCE], refs[:2])
				group = {"pinmame.input.switch": "switch", "pinmame.output.solenoid": "solenoid"}.get(device["binding"]["group"], "lamp")
				self.assertEqual(list(CURATOR.PLACEMENT_EXTRA_REFS.get((group, device["binding"]["device"]), ())), refs[2:], device["id"])
			self.assertIn("Placement (observed)", device["physical"]["notes"], device["id"])
		self.assertEqual(179, located)
		# the kid-flasher substitution depends on the ROM names and Krellan, so its placements cite them
		for address in (19, 24):
			refs = self.device("output.solenoid", address)["spatial"]["placements"][0]["provenance"]["source_refs"]
			self.assertIn(CURATOR.KRELLAN_SOURCE, refs)
			self.assertIn(CURATOR.SOLENOID_TEST_SOURCE, refs)
		# every used playfield device without a placement says why
		for device in self.definition["inputs"] + self.definition["outputs"]:
			if "spatial" not in device and device["availability"] in {"used", "optional"}:
				self.assertIn("No playfield placement:", device["physical"]["notes"], device["id"])

	def test_kid_flashers_follow_krellan_not_the_table_binding(self) -> None:
		left = self.device("output.solenoid", 19)["spatial"]["placements"][0]
		right = self.device("output.solenoid", 24)["spatial"]["placements"][0]
		self.assertLess(left["x"], 0.5)
		self.assertGreater(right["x"], 0.5)
		self.assertEqual("F24", CURATOR.SPATIAL_FLASHERS[19][0][0][2])
		self.assertEqual("F19", CURATOR.SPATIAL_FLASHERS[24][0][0][2])
		krellan = {int(row[0]): row[1] for row in table_rows("krellan-solenoid-table.md")}
		self.assertIn("Sudden", krellan[19])
		self.assertIn("Death", krellan[24])

	def test_spatial_report_is_committed_and_reconciles(self) -> None:
		report = load_json(ROOT / "reports/spatial/capcom/kingpin-1996.json")
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(canonical_bytes(CURATOR.build_spatial_report(self.definition)), canonical_bytes(report))
		unplaced = {item["device"] for item in report["unplaced"]}
		self.assertEqual({"switch.45", "switch.46", "switch.47", "switch.48", "solenoid.3", "solenoid.6", "solenoid.7", "solenoid.14", "solenoid.22", "solenoid.29"}, unplaced)
		walls = {switch_id for switch_id in report["centroid_placements"]}
		self.assertEqual({f"switch.{a}" for a, entry in CURATOR.SPATIAL_SWITCHES.items() if entry[3] == "Wall"} | {f"solenoid.{a}" for a, entry in CURATOR.SPATIAL_COILS.items() if entry[3] == "Wall"}, walls)
		for identifier in walls:
			group, address = identifier.split(".")
			device = self.device("input.switch" if group == "switch" else "output.solenoid", int(address))
			self.assertIn("the centroid of the outline points of the wall", device["physical"]["notes"], identifier)
		self.assertEqual({"lamp.116", "lamp.119", "lamp.120"}, set(report["backpanel_clamps"]))
		self.assertTrue(all(item["reason"] for item in report["unplaced"]))

	def test_retained_extraction_matches_its_manifest(self) -> None:
		working_root = resolve_working_root(ROOT)
		sources = working_root / "vpx-sources" if working_root else None
		if sources is None or not (sources / CURATOR.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Kingpin table extraction is not available")
		extraction = sources / CURATOR.EXTRACTION_RELATIVE_PATH
		manifest = load_json(sources / CURATOR.EXTRACTION_MANIFEST_RELATIVE_PATH)
		paths = sorted((path for path in extraction.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction).as_posix())
		expected = {
			"format": "pinmame-vpx-extraction-manifest",
			"version": 1,
			"files": [
				{"path": path.relative_to(extraction).as_posix(), "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
				for path in paths
			],
		}
		self.assertEqual(canonical_bytes(expected), canonical_bytes(manifest))
		self.assertEqual(CURATOR.EXTRACTION_FILE_COUNT, len(paths))
		self.assertEqual(CURATOR.EXTRACTION_TOTAL_BYTES, sum(path.stat().st_size for path in paths))
		self.assertEqual(CURATOR.EXTRACTION_MANIFEST_SHA256, hashlib.sha256(canonical_bytes(manifest)).hexdigest())
		self.assertEqual(CURATOR.VPX_TABLE_SCRIPT_SHA256, hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest())
		table = sources / "capcom/kingpin-1996" / CURATOR.VPX_TABLE_FILENAME
		self.assertEqual(CURATOR.VPX_TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())

	def test_placements_are_their_objects_centres_in_the_retained_extraction(self) -> None:
		working_root = resolve_working_root(ROOT)
		sources = working_root / "vpx-sources" if working_root else None
		if sources is None or not (sources / CURATOR.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Kingpin table extraction is not available")
		items = {}
		for path in (sources / CURATOR.EXTRACTION_RELATIVE_PATH / "gameitems").glob("*.json"):
			item_type, name = path.stem.split(".", 1)
			items[name] = (item_type, json.loads(path.read_text(encoding="utf-8"))[item_type])

		def centre(name: str) -> tuple[float, float]:
			item_type, value = items[name]
			if item_type == "Wall":
				points = value["drag_points"]
				x, y = sum(point["x"] for point in points) / len(points), sum(point["y"] for point in points) / len(points)
			elif item_type == "Primitive":
				x, y = value["position"]["x"], value["position"]["y"]
			else:
				x, y = value["center"]["x"], value["center"]["y"]
			return round(x / 952.0, 6), round(y / 2162.0, 6)

		for address, (x, y, name, item_type, _note) in {**CURATOR.SPATIAL_SWITCHES, **CURATOR.SPATIAL_COILS}.items():
			self.assertEqual((x, y), centre(name), (address, name))
			self.assertEqual(items[name][0], item_type, (address, name))
		for address, (points, _note) in CURATOR.SPATIAL_FLASHERS.items():
			for x, y, name, item_type in points:
				self.assertEqual((x, y), centre(name), (address, name))
				self.assertEqual(items[name][0], item_type, (address, name))
		for address, points in CURATOR.SPATIAL_LAMPS.items():
			for x, y, name, raw_y in points:
				expected_x, expected_y = centre(name)
				self.assertEqual(expected_x, x, (address, name))
				self.assertEqual(expected_y if raw_y is None else 0.0, y, (address, name))
				if raw_y is not None:
					self.assertEqual(expected_y, raw_y, (address, name))
					self.assertLess(raw_y, 0.0, (address, name))

	def test_placed_objects_are_bound_to_their_addresses_in_the_table_script(self) -> None:
		working_root = resolve_working_root(ROOT)
		sources = working_root / "vpx-sources" if working_root else None
		if sources is None or not (sources / CURATOR.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Kingpin table extraction is not available")
		lines = (sources / CURATOR.EXTRACTION_RELATIVE_PATH / "script.vbs").read_text(encoding="latin-1").replace("\r\n", "\n").split("\n")
		active = [line.split("'", 1)[0] if '"' not in line.split("'", 1)[0] else line for line in lines if not line.strip().startswith("'")]
		script = "\n".join(active)
		subs: dict[str, str] = {}
		current = None
		for line in active:
			match = re.match(r"\s*Sub\s+(\w+)", line, re.I)
			if match:
				current = match.group(1).lower()
				subs[current] = ""
			if current:
				subs[current] += line + "\n"
				if re.match(r"\s*End\s+Sub", line, re.I) or re.search(r"End Sub\s*$", line, re.I):
					current = None

		def lamp_bound(number: int, name: str) -> bool:
			return re.search(rf"^\s*(NFadeLm?|Flashm?)\s+{number}\s*,\s*{name}\b", script, re.M | re.I) is not None

		def callback(address: int) -> str:
			match = re.search(rf"SolCallback\({address}\)\s*=\s*\"([^\"]*)\"", script, re.I)
			return match.group(1) if match else ""

		def switch_bound(name: str, address: int) -> bool:
			bodies = [body for sub, body in subs.items() if sub.startswith(name.lower() + "_")]
			return any(re.search(rf"Switch\({address}\)\s*=\s*1|PulseSw\s*{address}\b", body) for body in bodies)

		# lamps: every placed light is bound to its own address
		for address, points in CURATOR.SPATIAL_LAMPS.items():
			for _x, _y, name, _raw in points:
				self.assertTrue(lamp_bound(address, name), (address, name))
		# switches: the placed object's handler asserts the address, except the documented projections
		projections = {32, 33, 34, 36, 37, 38, 39, 52}
		# ball-stack entry switches: the object's handlers add the ball to the stack whose InitSw names the address
		stacks = {35: ("bsTrough", "35,36,37,38,39"), 44: ("bsLock", "0,44,45,46"), 51: ("bsVUK", "0,51")}
		drops = {25: "dtDropL", 26: "dtDropL", 27: "dtDropL", 28: "dtDropL", 29: "dtDropR", 30: "dtDropR", 31: "dtDropR"}
		for bank, targets in (("dtDropL", (25, 26, 27, 28)), ("dtDropR", (29, 30, 31))):
			objects = ",".join(f"sw{target}" for target in targets)
			numbers = ", ".join(str(target) for target in targets)
			self.assertIn(f"{bank}.InitDrop Array({objects}),Array({numbers})", script)
		for address, (_x, _y, name, _type, note) in CURATOR.SPATIAL_SWITCHES.items():
			if address in projections:
				self.assertTrue(note, address)
				continue
			if address in drops:
				self.assertEqual(f"sw{address}", name, address)
				continue
			if address in stacks:
				stack, init = stacks[address]
				self.assertIn(f"{stack}.InitSw {init}", script, address)
				bodies = "".join(body for sub, body in subs.items() if sub.startswith(name.lower() + "_"))
				self.assertIn(f"{stack}.AddBall Me", bodies, (address, name))
				continue
			self.assertTrue(switch_bound(name, address), (address, name))
		self.assertTrue(switch_bound("sw32", 49), "the captive-ball target's handler pulses 49, the documented table defect")
		self.assertIn("bsTrough.InitSw 35,36,37,38,39", script)
		self.assertIn("bsTrough.InitKick BallRelease", script)
		# flashers: driven directly, or through the flash routines' pseudo-lamps
		routes = {18: ("LeftRampFlash", 130), 23: ("RightRampFlash", 129), 27: ("SetLamp 131,", 131)}
		for address, (points, _note) in CURATOR.SPATIAL_FLASHERS.items():
			names = [name for _x, _y, name, _type in points]
			if address in (19, 24):
				continue
			if address in routes:
				routine, lamp = routes[address]
				self.assertEqual(routine, callback(address), address)
				if routine.startswith("SetLamp"):
					for name in names:
						self.assertTrue(lamp_bound(lamp, name), (address, name))
				else:
					self.assertRegex(subs[routine.lower()], rf"SetFlash {lamp}, 1", address)
					for name in names:
						self.assertTrue(lamp_bound(lamp, name), (address, name))
			else:
				self.assertEqual(f"{names[0]}.State=".lower(), callback(address).lower(), address)
		# the kid flashers are swapped against the table on purpose: each placed object is bound to the other address
		self.assertEqual("f24.state=", callback(24).lower())
		self.assertEqual("f24", CURATOR.SPATIAL_FLASHERS[19][0][0][2].lower())
		self.assertEqual("f19.state=", callback(19).lower())
		self.assertEqual("f19", CURATOR.SPATIAL_FLASHERS[24][0][0][2].lower())
		# coils: the callback and the object its routine or ball stack acts on
		coil_evidence = {
			1: ("bsTrough.SolIn", "Drain", r"Sub Drain_Hit"),
			2: ("bsTrough.SolOut", "BallRelease", r"bsTrough\.InitKick BallRelease"),
			8: ("bsLock.SolOut", "GunKicker", r"bsLock\.InitKick GunKicker"),
			9: ("SolLFlipper", "LeftFlipper", r"LeftFlipper\.RotateToEnd"),
			10: ("SolRFlipper", "RightFlipper", r"RightFlipper\.RotateToEnd"),
			11: ("bsVUK.SolOut", "sw51b", r"bsVUK\.InitKick sw51b"),
			12: ("SlotMachineMotor", "SLOTmachineCylinder", r"SLOTmachineCylinder\.RotX = SlotPos"),
			13: ("LoopGate", "Gate2", r"Gate2\.Collidable"),
			32: ("SolAutoFire", "swPlunger", r"InitImpulseP swplunger"),
		}
		for address, (routine, name, pattern) in coil_evidence.items():
			self.assertEqual(routine.lower(), callback(address).lower(), address)
			self.assertEqual(name, CURATOR.SPATIAL_COILS[address][2], address)
			self.assertRegex(script, pattern, address)
		# slings and bumpers: no coil callback; the placed object is the one whose handler asserts the matching switch
		for coil, switch in ((4, 41), (5, 42), (15, 58), (16, 59), (17, 57)):
			self.assertEqual(CURATOR.SPATIAL_SWITCHES[switch][2], CURATOR.SPATIAL_COILS[coil][2], coil)
		self.assertEqual(
			set(CURATOR.SPATIAL_COILS), set(coil_evidence) | {4, 5, 15, 16, 17},
		)

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
