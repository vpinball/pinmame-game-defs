"""Gates for the Stern Meteor (1979) definition.

They lock down what was expensive to establish and cheap to lose: the physical-to-public solenoid pairing the ROM's own solenoid test proves, the
METEOR knock-down coils and drop lamps the scripted game proves, the lamp decoder arithmetic, the coin chutes the bookkeeping counts identify, the
fold of PinMAME's second root into this record, and the one conflict the retained evidence cannot settle. Fixtures that restate a printed sheet
are read from the committed excerpts, not from the curator's data module: a test that checks the generator against its own input only proves the
generator is self-consistent.
"""
from __future__ import annotations

import copy
import hashlib
import html
import json
import os
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402

import curate_meteor as curator  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/stern/meteor-1979.json"
SEED_PATH = ROOT / "tools/seeds/stern/meteor-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/meteor-1979.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/meteor-1979.json"
EXCERPTS = ROOT / "evidence/excerpts/stern.meteor.1979"
RUNTIME_PATH = ROOT / "evidence/runtime/stern/meteor-diagnostics-and-gameplay.json"
MACHINE_ID = "stern.meteor.1979"
DRIVER_IDS = {"meteor", "meteora", "meteora2", "meteorb", "meteorbf", "meteorc", "meteord", "meteore", "meteore7", "meteorf", "meteorf7", "meteorfp", "meteorg",
	"meteorg7", "meteorns"}
SEVEN_DIGIT = {"meteorb", "meteorc", "meteord", "meteore7", "meteorf7", "meteorg7"}
EXPECTED_MISSING = ["spatial_placement", "unresolved_conflicts"]
CABINET_SWITCHES = (1, 2, 3, 6, 7, 8)
UNUSED_SWITCHES = (17, 18, 25, 26)
CONFLICTED_SWITCHES = (10, 11, 20, 21, 23, 24)
# SDU driver number -> public address, from the ROM's solenoid test (retained run).
PHYSICAL_TO_PUBLIC = {1: 2, 2: 1, 3: 6, 4: 7, 5: 3, 6: 4, 7: 5, 8: 8, 9: 11, 10: 12, 11: 14, 12: 13, 13: 9, 14: 10, 15: 19, 16: 15, 17: 17, 18: 20, 19: 18}
# Public address -> the words its label must carry, from the printed SDU load names via that pairing.
SOLENOID_WORDS = {1: ("left", "slingshot"), 2: ("thumper",), 3: ("top left", "reset"), 4: ("meteor m", "knock-down"), 5: ("first e", "knock-down"), 6: ("knocker",),
	7: ("lower left", "reset"), 8: ("meteor t", "knock-down"), 9: ("right", "reset"), 10: ("right", "slingshot"), 11: ("second e", "knock-down"), 12: ("meteor o", "knock-down"),
	13: ("meteor", "reset"), 14: ("meteor r", "knock-down"), 15: ("outhole",), 18: ("coin",), 19: ("flipper", "relay")}
# METEOR target switch -> (knock-down coil, drop lamp), proven by the scripted game.
METEOR_BANK = {32: (4, 58), 31: (5, 42), 30: (8, 26), 29: (11, 10), 28: (12, 57), 27: (14, 41)}
BACKBOX_LAMPS = {13: "high score", 45: "game over", 61: "tilt", 63: "match"}
LAMPS_NOT_DRIVEN_IN_PLAY = {14, 30, 46, 62}
# Lamp-list row (the excerpt's numbering; 62 is the handwritten Tilt row) -> public lamp. The connector blocks agree wherever they print the row's pin, except
# rows 35, 36, 40 and 48, whose lamps state the disagreement; the ROM proves the METEOR drop lamps, the spot lamps and the backbox lamps.
LAMP_LIST_ROW_TO_LAMP = {1: 62, 2: 1, 3: 45, 4: 13, 5: 29, 6: 9, 7: 63, 8: 10, 9: 42, 10: 41, 11: 26, 12: 58, 13: 57, 14: 40, 15: 8, 16: 56, 17: 55,
	18: 39, 19: 24, 20: 50, 21: 34, 22: 18, 23: 2, 24: 49, 25: 33, 26: 17, 27: 15, 28: 52, 29: 36, 30: 20, 31: 4, 32: 51, 33: 35, 34: 19, 35: 31,
	36: 54, 37: 38, 38: 22, 39: 6, 40: 53, 41: 37, 42: 21, 43: 47, 44: 23, 45: 30, 46: 27, 47: 25, 48: 5, 49: 11, 50: 60, 51: 44, 52: 28, 53: 12,
	54: 59, 55: 43, 56: 11, 57: 7, 58: 14, 59: 62, 60: 46, 61: 3, 62: 61}
ROWS_AGAINST_THE_CONNECTOR_BLOCK = {35, 36, 40, 48}
# The prose of the two coils whose sheets print different wire colours that carries no wiring reading: (between the SDU sentence and the coil sheet's sentence,
# after the wire-colour remark). The wiring sentences themselves are built from the excerpt rows in the test.
CROSS_SHEET_NOTE_PROSE = {
	"Q7": ("the self-test card lists solenoid 07 as `6-Bank Drop Targets`. The ROM's solenoid test shows 07 while public 5 fires. Knocks down the METEOR first E "
		"target (switch 31), one of the six `Drop Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil "
		"sheet's `6-DROP TARGETS` row agree on the letter, and both known-working scripts drop target 31 from this address. The ROM fires it to spot the target, "
		"which a lit star rollover, return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and "
		"lower star rollovers, switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored "
		"for each player after the ball enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O "
		"and R knock-down coils after its first drain, the four targets then down, and exercised no player change). ",
		"Placed on the METEOR target it knocks down (table `sw31`); the coil sits behind the target and has no object."),
	"Q14": ("the self-test card lists solenoid 14 as `Right Sling-Shot`. The ROM's solenoid test shows 14 while public 10 fires. Fired when the right slingshot "
		"switch (public 15) closes in the retained gameplay and variant runs, and not while the game is tilted. Neither known-working script has a SolCallback for "
		"it: the table's slingshot kicks on its own hit. ",
		"Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
}
# The board each class of wired record names.
WIRING_BOARDS = {
	"mpu": "MPU module M-200 A4",
	"sdu": "Solenoid Driver / Voltage Regulator module SDU B-432 A3",
	"lda": "Lamp Driver module LDA-100 B-431 A5",
	"flipper button": "Hard-wired flipper button circuit through the SDU flipper enable relay",
	"flipper coil": "Hard-wired flipper circuit gated by the flipper enable relay (public 19)",
	"gi": "Transformer/rectifier A2, uncontrolled general-illumination buses",
}
# Public solenoid -> the playfield coil sheet rows its note quotes, by printed coil label. Every other solenoid quotes none.
COIL_SHEET_QUOTES = {1: ("LEFT SLING SHOT",), 2: ("THUMPER",), 3: ("TOP LFT. 3-BANK DROP TARG.",), 7: ("LOWER LFT. 3-BANK DR. TARG.",), 9: ("RIGHT 3-BANK DROP TARGET",),
	10: ("RIGHT SLING SHOT",), 15: ("OUT HOLE",), 46: ("LEFT FLIPPER", "RIGHT FLIPPER"), 48: ("LEFT FLIPPER", "RIGHT FLIPPER")}


def markdown_rows(path: Path, section: str | None = None) -> list[list[str]]:
	rows = []
	inside = section is None
	for line in path.read_text(encoding="utf-8").splitlines():
		if section is not None and line.startswith("## "):
			inside = line.startswith(section)
		if inside and line.startswith("|") and not re.match(r"^\|\s*:?-+", line):
			rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
	return rows


def decoder_table() -> dict[int, int]:
	"""Public lamp address -> SCR number, read from the lamp-driver excerpt (public = 16k + a + 1); every line's resistor must end at its own SCR."""
	result: dict[int, int] = {}
	for row in markdown_rows(EXCERPTS / "lamp-driver.md", "## 1."):
		if not re.match(r"^U\d$", row[0]) or row[3] == "none":
			continue
		chip, output = int(row[0][1:]) - 1, int(row[1][1:])
		resistor, transistor = row[2][1:], row[3][1:]
		assert resistor == transistor, row
		result[16 * chip + output + 1] = int(transistor)
	return result


def matrix_cells() -> dict[int, str]:
	"""Public switch address -> the playfield sheet's cell text, from the switch-matrix excerpt (public = strobe * 8 + return + 1)."""
	cells: dict[int, str] = {}
	for row in markdown_rows(EXCERPTS / "playfield-switch-matrix.md", "## Cells"):
		match = re.match(r"^I(\d)$", row[0])
		if match:
			for strobe, cell in enumerate(row[1:6]):
				cells[strobe * 8 + int(match.group(1)) + 1] = cell
	return cells


def sdu_loads() -> dict[int, str]:
	"""SDU driver number -> its printed load name, from the solenoid-driver excerpt."""
	loads = {}
	for row in markdown_rows(EXCERPTS / "solenoid-driver.md", "## Driver transistor"):
		match = re.match(r"^Q(\d+)$", row[0])
		if match:
			loads[int(match.group(1))] = row[3]
	return loads


def mesh_pieces(extraction: Path, name: str) -> list[tuple[float, float, float, float]]:
	"""World-space (left, top, right, bottom) of each connected piece of a baked primitive mesh: position + vertex * size, faces joining vertices."""
	primitive = json.loads((extraction / "gameitems" / f"Primitive.{name}.json").read_text(encoding="utf-8"))["Primitive"]
	vertices, parent = [], []
	faces = []
	for line in (extraction / "gameitems" / f"Primitive.{name}.obj").read_text(encoding="utf-8").splitlines():
		if line.startswith("v "):
			vertices.append(tuple(float(value) for value in line.split()[1:3]))
			parent.append(len(parent))
		elif line.startswith("f "):
			faces.append([int(token.split("/")[0]) - 1 for token in line.split()[1:]])

	def find(index: int) -> int:
		while parent[index] != index:
			parent[index] = parent[parent[index]]
			index = parent[index]
		return index

	for face in faces:
		for vertex in face[1:]:
			parent[find(face[0])] = find(vertex)
	groups: dict[int, list[int]] = {}
	for index in range(len(vertices)):
		groups.setdefault(find(index), []).append(index)
	origin, size = primitive["position"], primitive["size"]
	pieces = []
	for members in groups.values():
		xs = [vertices[index][0] for index in members]
		ys = [vertices[index][1] for index in members]
		pieces.append((origin["x"] + min(xs) * size["x"], origin["y"] + min(ys) * size["y"], origin["x"] + max(xs) * size["x"], origin["y"] + max(ys) * size["y"]))
	return pieces


def read_world_obj(path: Path) -> tuple[list[tuple[float, float, float]], dict[str, tuple[list[int], list[list[int]]]]]:
	"""A vpxtool world-space OBJ export: every vertex (x, y playfield VPX units, z height) and each object's vertex indices and faces."""
	vertices: list[tuple[float, float, float]] = []
	objects: dict[str, tuple[list[int], list[list[int]]]] = {}
	current = None
	with path.open(encoding="utf-8", errors="replace") as handle:
		for line in handle:
			if line.startswith("o "):
				current = line[2:].strip()
				objects.setdefault(current, ([], []))
			elif line.startswith("v "):
				parts = line.split()
				vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
				objects[current][0].append(len(vertices) - 1)
			elif line.startswith("f "):
				objects[current][1].append([int(token.split("/")[0]) - 1 for token in line.split()[1:]])
	return vertices, objects


class MeteorDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		group = lambda name: {item["binding"]["device"]: item for item in cls.definition["inputs"] + cls.definition["outputs"] if item["binding"]["group"] == name}
		cls.switches = group("pinmame.input.switch")
		cls.dips = group("pinmame.input.dip")
		cls.direct = group("physical.input.direct")
		cls.solenoids = group("pinmame.output.solenoid")
		cls.lamps = group("pinmame.output.lamp")
		cls.gi = group("physical.output.gi")
		cls.runtime = load_json(RUNTIME_PATH)
		cls.observations = cls.runtime["runtime"]["observations"]

	def test_deterministic_artifacts_match_the_curator(self) -> None:
		curator.check(ROOT)
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())

	def test_identity_and_the_driver_group_with_both_roots(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((machine["id"], machine["name"], machine["year"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"]),
			(MACHINE_ID, "Meteor", 1979, 1580, "113", "G5b38-MDqkx"))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), DRIVER_IDS)
		# PinMAME declares meteora as a second root; every other driver is a clone of meteor.
		self.assertNotIn("clone_of", drivers["meteor"])
		self.assertNotIn("clone_of", drivers["meteora"])
		for identifier in DRIVER_IDS - {"meteor", "meteora"}:
			self.assertEqual(drivers[identifier]["clone_of"], "meteor", identifier)
		for identifier, driver in drivers.items():
			if identifier in SEVEN_DIGIT:
				self.assertEqual(driver["physical_compatibility"], "compatible", identifier)
				overrides = {item["target"]: (item["segment_start"], item["width"]) for item in driver["display_overrides"]}
				self.assertEqual(overrides, {f"display.player-{n}-score": (start, 7) for n, start in zip(range(1, 5), (1, 9, 17, 25))}, identifier)
			else:
				self.assertEqual(driver["physical_compatibility"], "identical", identifier)
				self.assertNotIn("display_overrides", driver)
		for identifier in ("meteora2", "meteorns", "meteore", "meteorf", "meteorg", "meteore7", "meteorf7", "meteorg7"):
			self.assertIn("no harness run was made", drivers[identifier]["variant_notes"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == MACHINE_ID}
		self.assertEqual(claimed, DRIVER_IDS)
		record = next(item for item in catalog["machines"] if item["id"] == MACHINE_ID)
		self.assertEqual(record["missing"], EXPECTED_MISSING)

	def test_the_meteora_residual_record_is_folded_in(self) -> None:
		for path in curator.RETIRED_PATHS:
			self.assertFalse((ROOT / path).exists(), path)
		self.assertFalse((ROOT / "machines/stubs/stern/meteor-1979.json").exists())
		catalog = load_json(ROOT / "catalog/pinmame.json")
		self.assertNotIn("stern.meteor.1979.meteora", {machine["id"] for machine in catalog["machines"]})
		family = load_json(ROOT / "families/opdb/g5b38.json")
		self.assertEqual(family["members"], [{"machine_id": MACHINE_ID}])
		identity = load_json(ROOT / "reports/opdb-identity.json")
		entries = [item for item in identity["machines"] if item["machine_id"].startswith(MACHINE_ID)]
		self.assertEqual([(item["machine_id"], item["mapped_driver_count"]) for item in entries], [(MACHINE_ID, len(DRIVER_IDS))])
		self.assertNotIn("stern.meteor.1979.meteora", (ROOT / "reports/opdb-incoherences.md").read_text(encoding="utf-8"))

	def test_coverage_is_partial_with_exactly_the_documented_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual(coverage["status"], "partial")
		self.assertEqual(coverage["missing"], EXPECTED_MISSING)
		self.assertFalse((ROOT / "machines/author-ready/stern/meteor-1979.json").exists())
		conflicts = unresolved_conflicts(self.definition)
		self.assertEqual([conflict["id"] for conflict in conflicts], ["conflict.three-bank-middle-and-lower-target-switches"])
		self.assertIn("Resolution path:", conflicts[0]["description"])
		self.assertEqual(conflicts[0]["path"], "inputs[pinmame.input.switch:10|11|20|21|23|24]")
		conflicted = {address for address, item in self.switches.items() if item["provenance"]["status"] == "conflicted"}
		self.assertEqual(conflicted, set(CONFLICTED_SWITCHES))

	def test_every_matrix_address_follows_the_playfield_sheet(self) -> None:
		cells = matrix_cells()
		self.assertEqual(set(cells), set(range(1, 41)))
		for address in range(1, 41):
			item = self.switches[address]
			self.assertFalse(item["normally_closed"], address)
			cell = cells[address]
			label = re.match(r"^(.*?), (?:no )?D\b", cell).group(1)
			if label == "N/U":
				self.assertIn(address, UNUSED_SWITCHES)
				self.assertEqual(item["availability"], "unused", address)
				continue
			self.assertNotIn(address, UNUSED_SWITCHES)
			self.assertEqual(item["availability"], "used", address)
			notes = item["physical"]["notes"]
			if label == "(blank)":
				self.assertIn(address, (1, 2, 3))
				self.assertIn("unlabelled contact", notes)
			else:
				self.assertIn(f"playfield sheet: `{label}`", notes)
			if re.search(r", no D\b", cell):
				self.assertIn("draws this cell without", notes, address)
			if re.search(r", C$", cell):
				self.assertIn("capacitor", notes, address)
		self.assertEqual({address for address, item in self.switches.items() if 1 <= address <= 40 and item.get("initial_active")}, {33})
		# The cabinet sheet's tilt capacitor has both leads on one uninterrupted conductor, as the excerpt records; only the two contacts are drawn in parallel.
		cabinet = (EXCERPTS / "cabinet-wiring.md").read_text(encoding="utf-8")
		self.assertIn("its lower lead to the dot at the second switch's left terminal, where that vertical lead also ends", cabinet)
		self.assertIn("a second unlabelled contact in parallel, and beside them a capacitor whose two leads both join the same uninterrupted lead", self.switches[7]["physical"]["notes"])
		self.assertNotIn("capacitor in parallel", self.switches[7]["physical"]["notes"])

	def test_switch_wiring_follows_the_printed_strobe_and_return_lines(self) -> None:
		def printed_lines(name: str, *sections: str) -> dict[str, tuple[str, str]]:
			lines = {}
			for section in sections:
				for row in markdown_rows(EXCERPTS / name, section):
					match = re.fullmatch(r"(A4J[23]-\d+) \(([^()]+)\)", row[-1])
					if match:
						lines[row[0].split()[0]] = match.groups()
			return lines
		# The cabinet sheet labels strobes ST0 and ST1 and rows I0-I2 and I5-I7; the playfield sheet labels all five strobes and eight rows.
		cabinet = printed_lines("cabinet-wiring.md", "## Matrix rows")
		playfield = printed_lines("playfield-switch-matrix.md", "## Strobe columns", "## Return rows")
		self.assertEqual(set(cabinet), {"ST0", "ST1", "I0", "I1", "I2", "I5", "I6", "I7"})
		self.assertEqual(set(playfield), {f"ST{strobe}" for strobe in range(5)} | {f"I{row}" for row in range(8)})
		for address in range(1, 41):
			if address in UNUSED_SWITCHES:
				self.assertNotIn("wiring", self.switches[address], address)
				continue
			strobe, row = divmod(address - 1, 8)
			sheet = cabinet if address in CABINET_SWITCHES else playfield
			(control, control_wire), (ret, return_wire) = sheet[f"ST{strobe}"], sheet[f"I{row}"]
			wiring = self.switches[address]["wiring"]
			self.assertEqual({key: wiring.get(key) for key in ("control_connection", "control_wire", "return_connection", "return_wire")},
				{"control_connection": control, "control_wire": control_wire, "return_connection": ret, "return_wire": return_wire}, address)

	def test_solenoid_wiring_follows_the_solenoid_driver_sheet(self) -> None:
		rows = [row for row in markdown_rows(EXCERPTS / "solenoid-driver.md", "## Driver transistor") if re.fullmatch(r"Q\d+", row[0])]
		printed = {}
		for driver, collector, wire, *_ in rows:
			pin = re.match(r"(J\d+-\d+)\b", collector)
			if pin:
				printed[driver] = (f"A3{pin.group(1)}", wire.strip("()[]") if re.fullmatch(r"[(\[][A-Z-]+[)\]]", wire) else None)
		# The SDU sheet prints Q14's wire as a struck-through `(-B-)`; the definition takes `O-W` from the playfield coil sheet and says so on the coil.
		self.assertTrue([row for row in rows if row[0] == "Q14"][0][2].startswith("(-B-) struck through / illegible"))
		printed["Q14"] = (printed["Q14"][0], "O-W")
		by_driver = {item["wiring"]["driver_transistor"]: item for item in self.solenoids.values() if "driver_transistor" in item.get("wiring", {})}
		self.assertEqual(set(printed), set(by_driver) - {"Q15"})
		for driver, (connection, wire) in printed.items():
			wiring = by_driver[driver]["wiring"]
			self.assertEqual((wiring.get("drive_connection"), wiring.get("drive_wire")), (connection, wire), driver)
			# The note's SDU sentence quotes the SDU sheet's own reading, struck-through wire included.
			sdu_wire = "a struck-through `(-B-)` wire" if driver == "Q14" else wire
			self.assertIn(f"SDU driver {driver}, printed load `", by_driver[driver]["physical"]["notes"])
			self.assertIn(f"({connection.removeprefix('A3')}{', ' + sdu_wire if sdu_wire else ''}) on the Solenoid Driver schematic", by_driver[driver]["physical"]["notes"], driver)
		self.assert_cross_sheet_notes({driver: item["physical"]["notes"] for driver, item in by_driver.items()})
		self.assert_coil_sheet_quotes({address: item for address, item in self.solenoids.items()})

	@staticmethod
	def coil_sheet_rows() -> list[list[str]]:
		return [row for section in ("## Flippers", "## Thumper", "## Coils below") for row in markdown_rows(EXCERPTS / "playfield-coil-wiring.md", section)
			if row[1].startswith("A3")]

	def expected_cross_sheet_notes(self) -> dict[str, str]:
		"""The whole note of each coil whose two sheets print different wire colours (Q7, Q14): the SDU sentence built from the solenoid-driver excerpt row, the
		playfield coil sheet's sentence built from its excerpt row, and the fixed prose between and after them."""
		sdu = {row[0]: row for row in markdown_rows(EXCERPTS / "solenoid-driver.md", "## Driver transistor")}
		coils = {row[0]: row for row in self.coil_sheet_rows()}
		first_e, right_sling = coils['6-DROP TARGETS "E" (first)'], coils["RIGHT SLING SHOT"]
		self.assertEqual((sdu["Q7"][1:3], first_e[1:3]), (["J2-12", "(Y-B)"], ["A3-J2-12", "(Y-W)"]))
		self.assertEqual((sdu["Q14"][1], sdu["Q14"][2].split(" ")[0], right_sling[1:3]), ("J5-11", "(-B-)", ["A3J5-11", "(O-W)"]))
		q7_load = re.fullmatch(r'(M"E"T TARGET) \(printed `M"E"T TARGET` in the J2 legend\)', sdu["Q7"][3]).group(1)
		return {
			"Q7": f"SDU driver Q7, printed load `{q7_load}` ({sdu['Q7'][1]}, {sdu['Q7'][2].strip('()')}) on the Solenoid Driver schematic 12B-432-S113; "
				+ CROSS_SHEET_NOTE_PROSE["Q7"][0] + f"The playfield coil sheet prints this coil's wire as {first_e[2]} on {first_e[1]}. A wire-colour reading only; "
				"the definition follows the SDU sheet. " + CROSS_SHEET_NOTE_PROSE["Q7"][1],
			"Q14": f"SDU driver Q14, printed load `{sdu['Q14'][3]}` ({sdu['Q14'][1]}, a struck-through `{sdu['Q14'][2].split(' ')[0]}` wire) on the Solenoid Driver "
				"schematic 12B-432-S113; " + CROSS_SHEET_NOTE_PROSE["Q14"][0] + f"The playfield coil sheet prints `{right_sling[0]} {right_sling[1]} {right_sling[2]}`, "
				"which the definition follows. A wire-colour reading only. " + CROSS_SHEET_NOTE_PROSE["Q14"][1],
		}

	def assert_cross_sheet_notes(self, notes: dict[str, str]) -> None:
		# Where the two sheets print different colours for one coil, the whole note is compared word for word with its expected text, so each reading appears once,
		# credited to its own sheet, and no statement in any wording, before or after the SDU sentence, can credit a reading to another sheet or deny a printed one.
		for driver, expected in self.expected_cross_sheet_notes().items():
			self.assertEqual(notes[driver], expected, driver)

	def assert_coil_sheet_quotes(self, solenoids: dict[int, dict]) -> None:
		# Each solenoid quotes exactly its own playfield coil sheet rows, as `NAME CONNECTION (WIRE)` or `NAME` on CONNECTION (WIRE) with a connector on any board,
		# each a row of the coil excerpt; every other solenoid quotes none. Each quote is credited to the playfield coil sheet: its clause names that sheet before
		# the quote and no other source. A single-coil output's row also matches its own structured wiring, by connection or, where the coil sheet repeats another
		# pin (the thumper's A3J2-4), by colour.
		rows = {row[0]: (row[0], row[1].split(" ")[0], row[2]) for row in self.coil_sheet_rows()}
		patterns = (r"`([^`]+?) ((?:A\d+-?)?J\d+-\d+) (\([^)]*\))`", r"`([^`]+)` on ((?:A\d+-?)?J\d+-\d+) (\([^)]*\))")
		other_sources = re.compile(r"cabinet|SDU|Solenoid Driver|schematic|diagram|drawing|legend|card|manual|script|table|parts", re.I)
		for address, item in solenoids.items():
			note = item["physical"]["notes"]
			matches = [match for pattern in patterns for match in re.finditer(pattern, note)]
			quotes = sorted(match.groups() for match in matches)
			self.assertEqual(quotes, sorted(rows[name] for name in COIL_SHEET_QUOTES.get(address, ())), address)
			for match in matches:
				clause = re.split(r"[.;] ", re.sub(r"`[^`]*`", "``", note[:match.start()]))[-1]
				self.assertIn("playfield coil sheet", clause, (address, match.group(0)))
				self.assertIsNone(other_sources.search(clause), (address, match.group(0)))
			if len(quotes) == 1:
				wiring = item["wiring"]
				_, connection, wire = quotes[0]
				self.assertTrue(connection.replace("A3-J", "A3J") == wiring["drive_connection"] or wire.strip("()") == wiring["drive_wire"], address)

	def test_a_wire_reading_credited_to_the_wrong_sheet_is_refused(self) -> None:
		notes = {item["wiring"]["driver_transistor"]: item["physical"]["notes"] for item in self.solenoids.values() if "driver_transistor" in item.get("wiring", {})}
		self.assert_cross_sheet_notes(notes)
		for driver, change in (
			# The round-13 reattribution: the coil sheet's O-W credited to the SDU legend instead.
			("Q14", lambda text: text.replace("The playfield coil sheet prints `RIGHT SLING SHOT A3J5-11 (O-W)`", "The SDU sheet's J5-11 legend prints `O-W`")),
			("Q14", lambda text: text + " The SDU sheet prints the wire as O-W."),
			("Q14", lambda text: text.replace("a struck-through `(-B-)` wire", "O-W")),
			("Q7", lambda text: text.replace("(Y-W) on A3-J2-12", "(Y-B) on A3-J2-12")),
			("Q7", lambda text: text + " The SDU sheet prints (Y-W)."),
			("Q7", lambda text: text.replace("The playfield coil sheet prints this coil's wire as (Y-W) on A3-J2-12", "The SDU sheet prints this coil's wire as (Y-W) on A3-J2-12")),
			# The round-14 claims: a blank claimed for the coil sheet's printed cell, and the coil sheet's reading credited to the cabinet sheet.
			("Q14", lambda text: text + " The playfield coil sheet leaves A3J5-11's wire blank."),
			("Q14", lambda text: text.replace("The playfield coil sheet prints `RIGHT SLING SHOT", "The cabinet sheet prints `RIGHT SLING SHOT")),
			("Q7", lambda text: text.replace("The playfield coil sheet prints this coil's wire as (Y-W)", "The cabinet sheet prints this coil's wire as (Y-W)")),
			("Q7", lambda text: text + " The cabinet sheet leaves it blank."),
			# The round-15 claims: one placed before the SDU sentence, and one in words no keyword list anticipates.
			("Q14", lambda text: "The playfield coil sheet leaves A3J5-11 blank. " + text),
			("Q14", lambda text: text + " The cabinet diagram shows this lead in blue."),
		):
			changed = dict(notes)
			changed[driver] = change(notes[driver])
			self.assertNotEqual(changed[driver], notes[driver])
			with self.assertRaises(AssertionError, msg=driver):
				self.assert_cross_sheet_notes(changed)
		# A quoted coil-sheet row whose colour, pin or label the excerpt does not print, or another coil's row, is refused on any solenoid.
		self.assert_coil_sheet_quotes(self.solenoids)
		for address, old, new in (
			(3, "A3J2-10 (G-R)", "A3J2-10 (G-W)"),
			(2, "`THUMPER A3J2-4 (PUR-W)`", "`THUMPER A3J2-9 (PUR-W)`"),
			(46, "`LEFT FLIPPER A3J1-9 (-G-)`", "`LEFT FLIPPER A3J1-9 (-O-)`"),
			# The round-15 substitution: a valid row of another coil quoted on the thumper.
			(2, "`THUMPER A3J2-4 (PUR-W)`", "`LEFT SLING SHOT A3J2-4 (BRN-)`"),
			# The round-16 claims: an invented row on another board's connector, and the genuine row credited to the cabinet sheet.
			(2, "`THUMPER A3J2-4 (PUR-W)`;", "`THUMPER A3J2-4 (PUR-W)`; the playfield coil sheet also prints `THUMPER A4J2-4 (PUR-W)`;"),
			(2, "The playfield coil sheet prints `THUMPER", "The cabinet sheet prints `THUMPER"),
		):
			solenoids = copy.deepcopy(self.solenoids)
			self.assertIn(old, solenoids[address]["physical"]["notes"], address)
			solenoids[address]["physical"]["notes"] = solenoids[address]["physical"]["notes"].replace(old, new)
			with self.assertRaises(AssertionError, msg=old):
				self.assert_coil_sheet_quotes(solenoids)

	def test_every_solenoid_note_is_the_reviewed_text(self) -> None:
		self.assertEqual({address: item["physical"]["notes"] for address, item in self.solenoids.items()}, PINNED_SOLENOID_NOTES)

	def expected_hard_wiring(self) -> dict[tuple[str, int], dict[str, object]]:
		"""The whole wiring record of every wired device outside the switch matrix and the lamp list, keyed by (group, public address) and built from the
		excerpt rows that print it: the flipper buttons (public inputs 82 right, 84 left) and coils (public outputs 46 right, 48 left), every SDU driver, MPU S33
		and the general illumination."""
		sdu = (EXCERPTS / "solenoid-driver.md").read_text(encoding="utf-8")
		transformer = (EXCERPTS / "general-illumination.md").read_text(encoding="utf-8")
		cabinet = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "cabinet-wiring.md", "## Flipper buttons")}
		supply = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "playfield-coil-wiring.md", "## Supply buses")}
		pin_and_wire = lambda prefix, text: re.fullmatch(rf"({prefix}-\d+) \(([A-Z-]+)\)", text).groups()
		# The 43 VDC rail, as the transformer sheet routes it to the playfield solenoid bus, the SDU sheet draws it at the flipper enable relay's coil and names
		# the drivers' common return.
		rail = re.search(r"\b(\d+) VDC -> (J1-\d+) \(solenoid bus\)", transformer)
		relay = re.search(r'terminal 7 \(to the "(\d+) VDC" line\);.*? runs to (J3-\d+) "TO A2J3-\d+ \[([A-Z-]+)\]"', sdu)
		ground = re.search(r'"\+(\d+)V SOLENOID GND"', sdu)
		volts = int(rail.group(1))
		self.assertEqual((int(relay.group(1)), int(ground.group(1))), (volts, volts))
		# The flipper circuit: each button line on the cabinet sheet and at the SDU relay contact, the buttons' common return on the cabinet sheet, each coil's
		# return at the relay contact, and the flipper supply on the playfield coil sheet, the pin the 43 VDC rail feeds.
		buttons = {side: re.fullmatch(r"(A3J2-\d+) \(([A-Z-]+)\) - switch - joins (?:the same )?common bus", cabinet[f"{side} FLIPPER switch"]).groups()
			for side in ("LEFT", "RIGHT")}
		self.assertEqual({side: (f"A3{pin}", wire) for pin, side, wire in re.findall(r'(J2-\d+) "TO (LEFT|RIGHT) \[([A-Z-]+)\] FLIPPER BUTTON"', sdu)}, buttons)
		common = pin_and_wire("A2J2", cabinet["Common return"])
		returns = {side: (f"A3{pin}", wire) for pin, side, wire in re.findall(r'(J1-\d+) "TO (LEFT|RIGHT) FLIPPER COIL \[([A-Z-]+)\]', sdu)}
		self.assertEqual(set(returns), {"LEFT", "RIGHT"})
		flipper_supply = pin_and_wire("A2J1", supply["Flipper supply"])
		self.assertEqual(f"A2{rail.group(2)}", flipper_supply[0])
		expected: dict[tuple[str, int], dict[str, object]] = {}
		for address, side in ((82, "RIGHT"), (84, "LEFT")):
			expected[("switch", address)] = {"board": WIRING_BOARDS["flipper button"], "control_connection": buttons[side][0], "control_wire": buttons[side][1],
				"return_connection": common[0], "return_wire": common[1]}
		for address, side in ((46, "RIGHT"), (48, "LEFT")):
			expected[("solenoid", address)] = {"board": WIRING_BOARDS["flipper coil"], "control_connection": buttons[side][0], "control_wire": buttons[side][1],
				"drive_connection": returns[side][0], "drive_wire": returns[side][1], "nominal_voltage_v": volts, "power_connection": flipper_supply[0],
				"power_wire": flipper_supply[1], "voltage_type": "dc"}
		# Every SDU driver: its collector pin and wire, the relay's supply pin and wire for Q15, and the 43 VDC rating for every fitted load. Q14's SDU wire is
		# struck through; the definition takes the playfield coil sheet's right slingshot row on the same pin, as its note says.
		right_sling = next(row for row in self.coil_sheet_rows() if row[0] == "RIGHT SLING SHOT")
		for driver, collector, wire, load, *_ in markdown_rows(EXCERPTS / "solenoid-driver.md", "## Driver transistor"):
			if not re.fullmatch(r"Q\d+", driver):
				continue
			record: dict[str, object] = {"board": WIRING_BOARDS["sdu"], "driver_transistor": driver}
			if driver == "Q15":
				self.assertEqual(load, "FLIPPER ENABLE RELAY")
				record.update(power_connection=f"A3{relay.group(2)}", power_wire=relay.group(3))
			else:
				record["drive_connection"] = "A3" + re.match(r"(J\d+-\d+)\b", collector).group(1)
				printed = re.fullmatch(r"[(\[]([A-Z-]+)[)\]]", wire)
				if driver == "Q14":
					self.assertIsNone(printed)
					self.assertEqual(right_sling[1], record["drive_connection"])
					printed = re.fullmatch(r"\(([A-Z-]+)\)", right_sling[2])
				if printed:
					record["drive_wire"] = printed.group(1)
			if load != "N/U":
				record.update(nominal_voltage_v=volts, voltage_type="dc")
			expected[("solenoid", PHYSICAL_TO_PUBLIC[int(driver[1:])])] = record
		# MPU S33: the pushbutton from ground to the 6800's NMI pin.
		schematic = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "mpu-schematic.md", "## S33")}
		self.assertIn("Its left terminal goes to a ground symbol", schematic["S33"])
		mpu = re.match(r'"(U\d+) 6800 MPU"; the line from the node enters pin "(\d+)", labelled "([A-Z]+)"', schematic["U9"])
		expected[("switch", -6)] = {"board": WIRING_BOARDS["mpu"], "control_connection": f"{mpu.group(1)}-{mpu.group(2)} ({mpu.group(3)})", "return_connection": "Ground"}
		# General illumination: the playfield string on the playfield sheet, the cabinet lamp on the cabinet sheet and the backbox buses on the interboard
		# diagram, each of them a bus or return pin the transformer sheet draws, which together are all of its general-illumination pins.
		playfield = re.search(r'(A2J1-\d+) \(([A-Z-]+)\), "(\d+) VAC" at the top; return (A2J1-\d+) \(([A-Z-]+)\), "RETURN"; a lamp symbol \(circle\) between them '
			r'labelled "GEN\. ILLUM"', (EXCERPTS / "playfield-switch-matrix.md").read_text(encoding="utf-8"))
		lamp = re.fullmatch(r"(A2J2-\d+) \(([A-Z-]+)\) and (A2J2-\d+) \(([A-Z-]+)\)", cabinet["Lamp (circle, unlabelled)"])
		interboard = {f"J3-{row[0]}": row[1] for row in markdown_rows(EXCERPTS / "interboard-wiring.md", "## A2 TRANSFORMER, J3") if row[0].isdigit()}
		backbox_buses = [pin for pin, label in interboard.items() if label == "GEN ILL BUS"]
		backbox_returns = [pin for pin, label in interboard.items() if label == "GEN ILL RET. BACK BOX"]
		drawn = re.search(r"General illumination, as drawn: bus \(supply\) pins ([^;]+); return pins ([^.]+)\.", transformer)
		buses, bus_returns = (dict(re.findall(r"(J\d+-\d+) \(([A-Z-]+)\)", group)) for group in drawn.groups())
		self.assertEqual(buses, {playfield.group(1).removeprefix("A2"): playfield.group(2), lamp.group(1).removeprefix("A2"): lamp.group(2)}
			| {pin: buses.get(pin) for pin in backbox_buses})
		self.assertEqual(bus_returns, {playfield.group(4).removeprefix("A2"): playfield.group(5), lamp.group(3).removeprefix("A2"): lamp.group(4)}
			| {pin: bus_returns.get(pin) for pin in backbox_returns})
		self.assertTrue(all(buses.values()) and all(bus_returns.values()))
		expected[("gi", 1)] = {"board": WIRING_BOARDS["gi"], "nominal_voltage_v": int(playfield.group(3)),
			"power_connection": f"{playfield.group(1)} (playfield); {lamp.group(1).removeprefix('A2')} (cabinet); {', '.join(backbox_buses)} (backbox)",
			"return_connection": f"{playfield.group(4)}; {lamp.group(3).removeprefix('A2')}; {', '.join(backbox_returns)}", "voltage_type": "ac"}
		return expected

	def assert_wiring(self, items: list[dict]) -> None:
		# Every record carrying wiring is a used matrix switch, a lamp or a hard-wired record above. Matrix switches and lamps carry exactly their class's fields
		# and board (their values follow the switch sheets and the lamp list in their own tests); every other record is its whole expected record, so no field can
		# be added, dropped or changed.
		wired = {(item["binding"]["group"].split(".")[-1], item["binding"]["device"]): item["wiring"] for item in items if "wiring" in item}
		matrix = {("switch", address) for address in range(1, 41) if address not in UNUSED_SWITCHES}
		lamps = {("lamp", address) for address in LAMP_LIST_ROW_TO_LAMP.values()}
		expected = self.expected_hard_wiring()
		self.assertEqual(set(wired), matrix | lamps | set(expected))
		for keys, fields, board in ((matrix, ["board", "control_connection", "control_wire", "return_connection", "return_wire"], WIRING_BOARDS["mpu"]),
				(lamps, ["board", "drive_connection", "drive_wire", "driver_transistor"], WIRING_BOARDS["lda"])):
			for key in keys:
				self.assertEqual((sorted(wired[key]), wired[key]["board"]), (fields, board), key)
		for key, record in expected.items():
			self.assertEqual(wired[key], record, key)

	def test_every_wiring_record_follows_its_sheets(self) -> None:
		items = self.definition["inputs"] + self.definition["outputs"]
		self.assert_wiring(items)
		expected = self.expected_hard_wiring()
		self.assertEqual(expected[("switch", 84)], {"board": WIRING_BOARDS["flipper button"], "control_connection": "A3J2-2", "control_wire": "BLU",
			"return_connection": "A2J2-9", "return_wire": "O"})
		self.assertEqual(expected[("solenoid", 46)], {"board": WIRING_BOARDS["flipper coil"], "control_connection": "A3J2-1", "control_wire": "R",
			"drive_connection": "A3J1-9", "drive_wire": "O", "nominal_voltage_v": 43, "power_connection": "A2J1-6", "power_wire": "BLU-W", "voltage_type": "dc"})
		self.assertEqual(len(expected), 25)
		def swap_flipper_sides(by_key: dict) -> None:
			by_key[("solenoid", 46)]["wiring"], by_key[("solenoid", 48)]["wiring"] = by_key[("solenoid", 48)]["wiring"], by_key[("solenoid", 46)]["wiring"]
		for change in (
			# Round 16: the left flipper given the right flipper's return, and the two sides' wiring exchanged.
			lambda by_key: by_key[("solenoid", 48)]["wiring"].update(drive_connection="A3J1-9", drive_wire="O"),
			swap_flipper_sides,
			# Round 17: the left button given the right button's line, and the right flippers' supply moved to the playfield general-illumination bus.
			lambda by_key: by_key[("switch", 84)]["wiring"].update(control_connection="A3J2-1", control_wire="R"),
			lambda by_key: by_key[("solenoid", 46)]["wiring"].update(power_connection="A2J1-8", power_wire="W"),
			# An added field, a dropped rating, a changed supply wire, return, board or voltage, and wiring on a record that has none.
			lambda by_key: by_key[("solenoid", 2)]["wiring"].update(power_connection="A2J1-6"),
			lambda by_key: by_key[("solenoid", 6)]["wiring"].pop("nominal_voltage_v"),
			lambda by_key: by_key[("solenoid", 19)]["wiring"].update(power_wire="Y"),
			lambda by_key: by_key[("switch", 82)]["wiring"].update(return_wire="R"),
			lambda by_key: by_key[("switch", -6)]["wiring"].update(board="MPU-200 A4"),
			lambda by_key: by_key[("gi", 1)]["wiring"].update(nominal_voltage_v=7),
			lambda by_key: by_key[("lamp", 1)]["wiring"].update(board=WIRING_BOARDS["sdu"]),
			lambda by_key: by_key[("switch", 4)]["wiring"].update(board=WIRING_BOARDS["sdu"]),
			lambda by_key: by_key[("solenoid", 45)].update(wiring={"board": WIRING_BOARDS["flipper coil"]}),
		):
			changed = copy.deepcopy(items)
			change({(item["binding"]["group"].split(".")[-1], item["binding"]["device"]): item for item in changed})
			with self.assertRaises(AssertionError):
				self.assert_wiring(changed)

	def test_switch_test_shows_every_address_as_its_own_number(self) -> None:
		note = self.observations["runs"]["switch-test"]["note"]
		self.assertIn(", ".join(f"{address}->{address}" for address in range(1, 41)) + ".", note)

	def test_coin_chutes_follow_the_bookkeeping_counts(self) -> None:
		roles = {address: self.switches[address]["roles"] for address in (1, 2, 3)}
		self.assertEqual(roles, {1: ["cabinet.coin.1"], 2: ["cabinet.coin.2"], 3: ["cabinet.coin.3"]})
		self.assertIn("function 09", self.switches[1]["physical"]["notes"])
		self.assertIn("function 10", self.switches[2]["physical"]["notes"])
		self.assertIn("function 11", self.switches[3]["physical"]["notes"])

	def test_solenoid_translation_matches_the_printed_loads_and_the_rom_test(self) -> None:
		self.assertEqual({int(key): value for key, value in self.observations["physical_service_solenoid_to_public"].items()}, PHYSICAL_TO_PUBLIC)
		loads = sdu_loads()
		self.assertEqual(set(loads), set(PHYSICAL_TO_PUBLIC))
		for number, public in PHYSICAL_TO_PUBLIC.items():
			item = self.solenoids[public]
			aliases = {(alias["namespace"], alias["value"]) for alias in item["aliases"]}
			self.assertIn(("manual.self-test", str(number)), aliases)
			self.assertIn(("manual.address", f"SDU-Q{number}"), aliases)
			self.assertEqual(item["wiring"]["driver_transistor"], f"Q{number}")
			load = loads[number].split(" (")[0]
			self.assertIn(f"printed load `{load}`", item["physical"]["notes"], public)
			for word in SOLENOID_WORDS.get(public, ()):
				self.assertIn(word, item["label"].lower(), public)
		self.assertNotIn(16, self.solenoids)
		self.assertEqual({public for public in (17, 20) if self.solenoids[public]["availability"] == "unused"}, {17, 20})

	def test_meteor_bank_coils_and_lamps_are_the_roms(self) -> None:
		named = self.observations["named_output_addresses"]
		for switch, (coil, lamp) in METEOR_BANK.items():
			target = self.switches[switch]["id"]
			self.assertTrue(target.startswith("switch.meteor-bank-"), target)
			letter = target.removeprefix("switch.meteor-bank-").removesuffix("-target")
			self.assertEqual(named[f"meteor-{letter}-drop-lamp"], lamp)
			self.assertEqual(self.lamps[lamp]["id"], f"lamp.meteor-drop-{letter}")
			self.assertEqual(self.solenoids[coil]["id"], f"device.meteor-{letter}-knock-down")
			relationship = next(item for item in self.definition["relationships"] if item["destination"] == target and item["source"] == self.solenoids[coil]["id"])
			self.assertEqual(relationship["kind"], "pulse")
		for switch, coil_key, lamp_key in ((4, "switch-4-spot-coil", "switch-4-spot-lamp"), (38, "switch-38-spot-coil", "switch-38-spot-lamp"), (40, "switch-40-spot-coil", "switch-40-spot-lamp")):
			self.assertIn(f"switch {switch} put this lamp out", self.lamps[named[lamp_key]]["physical"]["notes"])
			self.assertIn(self.solenoids[named[coil_key]]["id"], {self.solenoids[coil]["id"] for coil, _ in METEOR_BANK.values()})
		self.assertEqual(named["tilt-lamp"], 61)

	def test_continuous_outputs_and_flipper_relay(self) -> None:
		self.assertEqual(self.solenoids[19]["id"], "device.flipper-enable-relay")
		self.assertEqual(self.solenoids[19]["spatial"]["reason"], "internal_nonvisual")
		self.assertEqual(self.solenoids[18]["spatial"]["reason"], "cabinet_or_service")
		for public in (17, 20):
			self.assertEqual(self.solenoids[public]["spatial"]["reason"], "unused")
			self.assertIn("initialisation pulse", self.solenoids[public]["physical"]["notes"])
		for public in (45, 47):
			self.assertEqual(self.solenoids[public]["kind"], "virtual")

	def test_lamp_addresses_follow_the_decoder(self) -> None:
		decoder = decoder_table()
		self.assertEqual(set(decoder), set(range(1, 65)) - {16, 32, 48, 64})
		self.assertEqual(set(self.lamps), set(decoder))
		self.assertEqual(self.observations["lamp_decoder_holes_not_seen"], [16, 32, 48, 64])
		for address, transistor in decoder.items():
			self.assertEqual(self.lamps[address]["wiring"]["driver_transistor"], f"Q{transistor}", address)

	@staticmethod
	def printed_lamp_rows() -> dict[int, tuple[int, str, str, str, str]]:
		rows = [row[:5] for row in markdown_rows(EXCERPTS / "lamp-driver.md", "## 3.") if len(row) == 6 and re.match(r"^\d+$", row[0]) and re.match(r"^J-[123]$", row[3])]
		assert len(rows) == 61, len(rows)
		# The handwritten row below the typed list on the PDF page 29 copy, as the excerpt's differences table transcribes it.
		assert "'Tilt' / 'grey-blk' / 'J-2' / '10'" in (EXCERPTS / "lamp-driver.md").read_text(encoding="utf-8")
		rows.append(["62", "Tilt", "grey-blk", "J-2", "10"])
		return {int(number): (int(number), description, wire, jack.replace("-", ""), pin) for number, description, wire, jack, pin in rows}

	@staticmethod
	def connector_block_entries() -> list[tuple[str, str, str]]:
		entries, jack = [], None
		for line in (EXCERPTS / "lamp-driver.md").read_text(encoding="utf-8").splitlines():
			if line.startswith("#"):
				heading = re.match(r"^### (J[123]) ", line)
				jack = heading.group(1) if heading else None
			elif jack and line.startswith("|"):
				cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
				if cells[0].isdigit() and re.fullmatch(r"Q\d+", cells[2]):
					entries.append((jack, cells[1], cells[2]))
		return entries

	def assert_lamp_list_rows(self, lamps: dict[int, dict]) -> None:
		printed = self.printed_lamp_rows()
		self.assertEqual(len(printed), 62)
		self.assertEqual(set(LAMP_LIST_ROW_TO_LAMP), set(printed))
		# Every row a lamp note quotes, with its whole printed tuple, is a printed row on the lamp that owns it, and every lamp quotes exactly its own rows: no row
		# is invented, dropped, altered or moved to another lamp.
		# Every mention of a row is parsed, whatever its jack, so a row on a jack the list does not print fails the comparison instead of being skipped.
		quoted: dict[int, list[tuple[int, str, str, str, str]]] = {}
		for address, item in lamps.items():
			notes = item["physical"]["notes"]
			matches = list(re.finditer(r"\brow (\d+) `([^`]*)` \(([^,()]+), (\S+) pin ([^)]+)\)", notes))
			self.assertEqual(len(matches), len(re.findall(r"\brow \d+\b", notes)), address)
			for match in matches:
				quoted.setdefault(address, []).append((int(match.group(1)), *match.groups()[1:]))
		expected: dict[int, list[tuple[int, str, str, str, str]]] = {}
		for row, lamp in LAMP_LIST_ROW_TO_LAMP.items():
			expected.setdefault(lamp, []).append(printed[row])
		self.assertEqual(set(expected), set(lamps))
		self.assertEqual({address: sorted(entries) for address, entries in quoted.items()}, {address: sorted(entries) for address, entries in expected.items()})
		# Each lamp's structured wiring is exactly its own rows' wires and connections. Two lamps take their drive connection from the connector block instead
		# of a list row; each is checked against the block below.
		overrides = {31: "A5J2-15", 62: "A5J2-7"}
		for address, entries in expected.items():
			wiring = lamps[address]["wiring"]
			self.assertEqual(wiring["drive_wire"].split("; "), list(dict.fromkeys(wire for _, _, wire, _, _ in sorted(entries))), address)
			connection = overrides.get(address) or "; ".join(dict.fromkeys(f"A5{jack}-{pin}" for _, _, _, jack, pin in sorted(entries)))
			self.assertEqual(wiring["drive_connection"], connection, address)
		self.assertEqual({lamp: lamps[lamp]["wiring"]["driver_transistor"] for lamp in overrides}, {31: "Q19", 62: "Q43"})
		# Every pin a note gives an SCR (`Jx pin p` after the SCR it belongs to, or `on pin p` on the same jack) is the connector-block entry the excerpt prints,
		# whatever the jack number, an illegible pin cell compared literally with its backticked quote; `nothing on Jx pin p` is one of the lamp's own pins that
		# the blocks leave empty. The list's own pins, written `J-x pin p`, are one of the lamp's rows' printed pins, and a printed label quoted just before one
		# is that row's label; the only remark allowed between the two is `S.P.S.A.`'s own expansion, so no other text is taken out with the statement. Once the
		# row quotes (in exactly the form compared above), these statements and the few phrases below are taken out, no pin or jack mention may remain,
		# board-qualified forms such as `A5J4-15` included, and every remaining backticked string is a label or wire of a row on one of the lamp's pins, a script
		# light name or one of the script strings the notes quote, so a statement in any other form fails instead of being skipped.
		entries = self.connector_block_entries()
		token = re.compile(r"(?P<scr>\bQ\d+\b)|(?:`(?P<label>[^`]*)`(?P<expansion> \(same player shoots again\))? on )?\bJ-(?P<list_jack>\d+) pin (?P<list_pin>\d+)"
			r"|(?P<nothing>\bnothing on )?\bJ(?P<jack>\d+) pin (?P<pin>\d+|`[^`]*`)|\bon pin (?P<bare>\d+)")
		phrases = ("the triangle column between pin 12 and", "a pin the connector block gives to no SCR", "the connector block's J3 entry for SCR", "a blank pin cell",
			"`J-2` / `10` row")
		script_strings = {"VR_Room = 0", "VR_Room = 1", "cab_mode = 0", "cab_mode = 1", "FadeReel", "UpdateMultipleLamps", "\"Game Over\" light", "\"Match\" light",
			"VR_Backbox_Backglass.blenddisablelighting"}
		claims: dict[int, set[tuple[str, str, str]]] = {}
		for address, item in lamps.items():
			notes = re.sub(r"\brow \d+ `[^`]*` \([^,()]+, \S+ pin [^)]+\)", "", item["physical"]["notes"])
			own_pins = {(jack, pin) for _, _, _, jack, pin in expected[address]}
			on_own_pins = [row for row in printed.values() if row[3:] in own_pins]
			scr = jack = None
			for match in token.finditer(notes):
				if match.group("scr"):
					scr = match.group("scr")
				elif match.group("list_jack"):
					list_pin = (f"J{match.group('list_jack')}", match.group("list_pin"))
					self.assertIn(list_pin, own_pins, address)
					if match.group("label") is not None:
						self.assertIn((match.group("label"), *list_pin), [(row[1], *row[3:]) for row in expected[address]], address)
					if match.group("expansion"):
						self.assertEqual(match.group("label"), "S.P.S.A.", address)
				elif match.group("nothing"):
					empty = (f"J{match.group('jack')}", match.group("pin"))
					self.assertIn(empty, own_pins, address)
					self.assertEqual([entry for entry in entries if entry[:2] == empty], [], address)
				else:
					jack = f"J{match.group('jack')}" if match.group("jack") else jack
					pin = (match.group("pin") or match.group("bare")).strip("`")
					self.assertIn((jack, pin, scr), entries, address)
					claims.setdefault(address, set()).add((jack, pin, scr))
			residual = token.sub(" ", notes)
			for phrase in phrases:
				residual = residual.replace(phrase, " ")
			self.assertIsNone(re.search(r"\bpins?\b|J\s*-?\s*\d", residual), address)
			allowed = {row[1] for row in on_own_pins} | {row[2] for row in on_own_pins} | script_strings
			for quoted_string in re.findall(r"`([^`]*)`", residual):
				self.assertTrue(quoted_string in allowed or re.fullmatch(r"(?:L|FlBGL)\d+[A-Za-z]?", quoted_string), (address, quoted_string))
		# Where a connector block prints the row's pin, the owning lamp's SCR is one the block puts there, or the lamp gives the block entry of its own SCR that
		# the definition follows instead.
		for row, (_, _, _, jack, pin) in printed.items():
			scrs = [scr for block, number, scr in entries if (block, number) == (jack, pin)]
			address = LAMP_LIST_ROW_TO_LAMP[row]
			transistor = lamps[address]["wiring"]["driver_transistor"]
			if row in ROWS_AGAINST_THE_CONNECTOR_BLOCK:
				self.assertTrue(scrs and transistor not in scrs, row)
				self.assertTrue(any(scr == transistor for _, _, scr in claims.get(address, ())), row)
			elif scrs:
				self.assertIn(transistor, scrs, row)
		# A lamp note names exactly its own SCR and every SCR the connector blocks print on its rows' pins, so a disputed pin's competing SCR is the one the block
		# prints. Lamp 27 also names Q9, whose block pin `?(4)` is the blot the note explains beside the list's J-1 pin 4.
		extra = {27: {"Q9"}}
		for lamp, rows in expected.items():
			block = {scr for _, _, _, jack, pin in rows for number_jack, number, scr in entries if (number_jack, number) == (jack, pin)}
			named = set(re.findall(r"\bQ\d+\b", lamps[lamp]["physical"]["notes"]))
			self.assertEqual(named, {lamps[lamp]["wiring"]["driver_transistor"]} | block | extra.get(lamp, set()), lamp)

	def test_every_printed_lamp_list_row_lands_on_its_lamp(self) -> None:
		self.assert_lamp_list_rows(self.lamps)
		entries = self.connector_block_entries()
		self.assertEqual(len(entries), 25 + 20 + 23)
		self.assertEqual([scr for jack, pin, scr in entries if (jack, pin) == ("J2", "15")], ["Q19"])
		self.assertEqual([scr for jack, pin, scr in entries if (jack, pin) == ("J2", "7")], ["Q43"])
		self.assertEqual([scr for jack, pin, scr in entries if (jack, pin) == ("J3", "7")], [])

	def test_a_lamp_list_row_moved_to_another_lamp_is_refused(self) -> None:
		# Rows 32 and 35 print the same J-3 pin 15, so swapping them between lamps 51 and 31, with their wires, keeps the row inventory and every connection.
		printed = self.printed_lamp_rows()
		quote = lambda row: "row {} `{}` ({}, {} pin {})".format(*printed[row])
		lamps = copy.deepcopy(self.lamps)
		for address, ours, theirs in ((31, 35, 32), (51, 32, 35)):
			self.assertIn(quote(ours), lamps[address]["physical"]["notes"])
			lamps[address]["physical"]["notes"] = lamps[address]["physical"]["notes"].replace(quote(ours), quote(theirs))
			lamps[address]["wiring"]["drive_wire"] = printed[theirs][2]
		with self.assertRaises(AssertionError):
			self.assert_lamp_list_rows(lamps)
		# An invented row, an extra wire and an extra connection are each refused on their own. So are an invented row on a jack the list never prints, on a lamp
		# whose connection override and wire leave the structured wiring unchanged, a row mention the quote pattern cannot parse, and a disputed pin's competing SCR
		# misnamed in the note (the block prints Q23 on J1 pin 14, lamp 5's printed pin).
		for lamp, section, field, change in (
			(1, "physical", "notes", lambda text: text + " row 63 `Invented` (W-Y, J1 pin 9)"),
			(1, "wiring", "drive_wire", lambda text: text + "; W-Y"),
			(1, "wiring", "drive_connection", lambda text: text + "; A5J1-9"),
			(31, "physical", "notes", lambda text: text + " row 63 `Invented` (O-B, J4 pin 9)"),
			(31, "physical", "notes", lambda text: text + " row 63 `Invented` (O-B J3 pin 9)"),
			(5, "physical", "notes", lambda text: text.replace("lands on Q23's block entry", "lands on Q24's block entry")),
			# The round-10 transposition: lamp 31's two SCRs swapped between J3 pin 15 and J2 pin 15.
			(31, "physical", "notes", lambda text: text.replace("SCR Q51 (lamp 51) on J3 pin 15 and SCR Q19 on J2 pin 15", "SCR Q19 (lamp 51) on J3 pin 15 and SCR Q51 on J2 pin 15")),
			(54, "physical", "notes", lambda text: text.replace("(and Q52 on pin 3 as well)", "(and Q52 on pin 9 as well)")),
			# The round-11 jack: a pairing moved to a jack the lamp driver does not have, and pairings and list pins in forms the parser does not read.
			(31, "physical", "notes", lambda text: text.replace("SCR Q51 (lamp 51) on J3 pin 15", "SCR Q51 (lamp 51) on J4 pin 15")),
			(31, "physical", "notes", lambda text: text.replace("SCR Q51 (lamp 51) on J3 pin 15", "SCR Q51 (lamp 51) on J 4 pin 15")),
			(31, "physical", "notes", lambda text: text.replace("SCR Q51 (lamp 51) on J3 pin 15", "SCR Q51 (lamp 51) at pin 15 of J4")),
			(31, "physical", "notes", lambda text: text.replace("The list prints `2X` on J-3 pin 15", "The list prints `2X` on J-3 pin 16")),
			(62, "physical", "notes", lambda text: text.replace("and nothing on J3 pin 7", "and nothing on J2 pin 7")),
			# The round-12 claims: a board-qualified pairing, an empty pin on a jack the lamp driver does not have, and a label the list does not print there.
			(31, "physical", "notes", lambda text: text + " SCR Q51 at A5J4-15."),
			(62, "physical", "notes", lambda text: text + " The block prints nothing on J4 pin 7."),
			(31, "physical", "notes", lambda text: text.replace("The list prints `2X` on J-3 pin 15,", "The list prints `2X` on J-3 pin 15 and also `3X` on J-3 pin 15,")),
			(31, "physical", "notes", lambda text: text + " The list also prints `3X` for this output."),
			# The round-13 parentheticals: a claim hidden in a remark between a quoted label and its list pin, or inside the one expansion the notes use.
			(31, "physical", "notes", lambda text: text + " The list repeats `2X` (wired to A5J4-15) on J-3 pin 15."),
			(11, "physical", "notes", lambda text: text.replace("(same player shoots again)", "(same player shoots again; `3X` at A5J4-15)")),
			(11, "physical", "notes", lambda text: text.replace("(same player shoots again)", "(same player shoots again, also `3X`)")),
		):
			lamps = copy.deepcopy(self.lamps)
			before = lamps[lamp][section][field]
			lamps[lamp][section][field] = change(before)
			self.assertNotEqual(lamps[lamp][section][field], before)
			with self.assertRaises(AssertionError, msg=(lamp, field)):
				self.assert_lamp_list_rows(lamps)

	def test_pinmame_sources_record_the_files_licenses_and_runs_claim_only_what_changed(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual(sources[curator.CATALOG_SOURCE]["license"], curator.PINMAME_CATALOG_LICENSE)
		self.assertEqual(sources[curator.CORE_SOURCE]["license"], curator.PINMAME_CORE_LICENSE)
		self.assertIn("old MAME license for the unmarked src/wpc/stgames.c, src/wpc/stsnd.c and src/wpc/core.h; BSD-3-Clause for src/wpc/by35.c and src/wpc/by35.h",
			curator.PINMAME_CORE_LICENSE)
		# The scoring bumpers changed the score display and sent sound commands but no lamp or solenoid; a drop lamp was the only one that stayed out, others blinked.
		for address in (12, 13):
			self.assertIn("it changed no lamp or solenoid; the score display advanced and sound commands were sent", self.switches[address]["physical"]["notes"], address)
		text = json.dumps(self.definition, ensure_ascii=False)
		self.assertNotIn("changed no output", text)
		self.assertNotIn("changed an output", text)
		self.assertNotIn("and only this one", text)
		for _, lamp in METEOR_BANK.values():
			if lamp != 41:
				self.assertIn("was the only lamp that stayed out through the end of that step", self.lamps[lamp]["physical"]["notes"], lamp)

	def test_backbox_lamps_and_lamps_not_driven_in_play(self) -> None:
		for address, words in BACKBOX_LAMPS.items():
			item = self.lamps[address]
			self.assertIn(words, item["label"].lower())
			self.assertEqual(item["spatial"]["reason"], "cabinet_or_service")
		for address, item in self.lamps.items():
			if address not in BACKBOX_LAMPS:
				self.assertNotIn("spatial", item, address)
		outside = set(self.observations["lamp_addresses_driven_outside_self_test"])
		self.assertEqual(set(self.lamps) - outside, LAMPS_NOT_DRIVEN_IN_PLAY)
		for address in LAMPS_NOT_DRIVEN_IN_PLAY:
			self.assertEqual(self.lamps[address]["availability"], "used")

	def test_three_flippers_on_two_buttons(self) -> None:
		self.assertEqual(self.solenoids[46]["physical"]["quantity"], 2)
		self.assertEqual(len(self.solenoids[46]["spatial"]["placements"]), 2)
		self.assertEqual(self.solenoids[48]["physical"]["quantity"], 1)
		self.assertEqual(len(self.solenoids[48]["spatial"]["placements"]), 1)
		self.assertEqual({address: self.switches[address]["availability"] for address in (81, 82, 83, 84)}, {81: "unused", 82: "used", 83: "unused", 84: "used"})
		# 1 and 2 are the winding-shunt contacts and 6 the upper right flipper's series E.O.S. contact; S33 is public switch -6, not a direct input.
		self.assertEqual(set(self.direct), {1, 2, 6})
		self.assertTrue(self.direct[1]["normally_closed"] and self.direct[2]["normally_closed"])
		self.assertEqual(self.direct[2]["physical"]["quantity"], 2)
		coil_sheet = (EXCERPTS / "playfield-coil-wiring.md").read_text(encoding="utf-8")
		self.assertIn("its lower end connects through \"E.O.S.\" to the node at the right flipper's lower end", coil_sheet)
		self.assertIn("It is the only drawing labelled E.O.S.", coil_sheet)
		series = self.direct[6]
		self.assertEqual((series["id"], series["normally_closed"], series["physical"]["quantity"]), ("switch.upper-right-flipper-series-eos-contact", False, 1))
		self.assertEqual(series["aliases"], [{"namespace": "manual.address", "value": "E.O.S."}])
		self.assertNotIn("spatial", series)
		flippers = next(item for item in self.definition["mechanisms"] if item["id"] == "mech.flippers")
		self.assertIn(series["id"], flippers["sensors"])

	def test_mpu_s33_is_the_diagnostic_input(self) -> None:
		s33 = self.switches[-6]
		self.assertEqual((s33["id"], s33["availability"], s33["normally_closed"], s33["spatial"]["reason"]), ("switch.mpu-diagnostic-s33", "used", False, "cabinet_or_service"))
		self.assertIn({"namespace": "manual.address", "value": "S33"}, s33["aliases"])
		self.assertEqual(s33["physical"]["quantity"], 1)
		self.assertEqual(s33["wiring"], {"board": "MPU module M-200 A4", "control_connection": "U9-6 (NMI)", "return_connection": "Ground"})
		self.assertIn(curator.MANUAL_SOURCE, s33["provenance"]["source_refs"])
		# The MPU schematic draws S33 from ground to the MPU's NMI input, pin 6, which PinMAME drives from public -6.
		schematic = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "mpu-schematic.md", "## S33")}
		self.assertIn("\"S33\"", schematic["S33"])
		self.assertIn("ground symbol", schematic["S33"])
		self.assertIn("pin \"6\", labelled \"NMI\"", schematic["U9"])
		self.assertIn("BY35_SWCPUDIAG", s33["physical"]["notes"])
		# IPDB reports a remote memory-clear lead to A4J3-5, which the interboard diagram prints N.U, so no remote contact is recorded.
		self.assertIn("W to A4J3-5 (MPU)", (EXCERPTS / "ipdb-schematic-errata.md").read_text(encoding="utf-8"))
		mpu_j3 = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "interboard-wiring.md", "## MPU A4, J3") if row[0].isdigit()}
		self.assertEqual((mpu_j3["1"], mpu_j3["5"]), ("SELF TEST SWITCH", "N.U"))
		self.assertIn("a lead only", s33["physical"]["notes"])
		self.assertIn("prints MPU A4J3-5 `N.U`", s33["physical"]["notes"])
		self.assertNotIn("switch.memory-clear", {item["id"] for item in self.definition["inputs"]})

	def test_sound_diagnostic_is_a_virtual_route(self) -> None:
		route = self.switches[-5]
		self.assertEqual((route["id"], route["kind"], route["availability"], route["spatial"]["reason"]), ("input.sound-diagnostic-voice-select", "virtual", "used", "virtual"))
		self.assertNotIn("normally_closed", route)
		self.assertEqual(set(route["physical"]), {"notes"})
		self.assertIn("stores it as `voiceSw`", route["physical"]["notes"])
		self.assertIn("no physical contact, polarity or fitment is recorded", route["physical"]["notes"])

	def test_tilt_and_slam_quantities_follow_the_general_operation_pages(self) -> None:
		text = (EXCERPTS / "general-operation.md").read_text(encoding="utf-8")
		self.assertIn("Check adjustment of the three (normally open) tilt switches", text)
		self.assertIn("There is a slam switch on the front door, one on the tilt board and one on the playfield", text)
		self.assertEqual((self.switches[7]["physical"]["quantity"], self.switches[8]["physical"]["quantity"]), (3, 3))
		# One contact of each is mounted with the playfield panel, so the location says so; neither is placed.
		self.assertIn("3. Panel tilt on bottom of playfield panel.", text)
		self.assertIn("underside of the playfield panel", self.switches[7]["physical"]["location"])
		self.assertEqual(self.switches[8]["physical"]["location"], "Front door, tilt board and playfield")
		for address in (7, 8):
			self.assertEqual(self.switches[address]["spatial"]["reason"], "cabinet_or_service")
			self.assertIn("no placement is asserted for that contact", self.switches[address]["physical"]["notes"])
		self.assertIn("three (normally open) tilt switches", self.switches[7]["physical"]["notes"])
		self.assertIn("Any number of slam switches could be installed by the operator", self.switches[8]["physical"]["notes"])

	def test_flipper_relay_pin_is_its_supply(self) -> None:
		wiring = self.solenoids[19]["wiring"]
		self.assertNotIn("drive_connection", wiring)
		self.assertEqual((wiring["power_connection"], wiring["power_wire"], wiring["driver_transistor"]), ("A3J3-5", "Y-W", "Q15"))
		# The interboard diagram feeds A3J3-5 from A2J3-9, not from A2J3-8 as the SDU sheet's callout prints.
		transformer_j3 = {row[0]: row[1] for row in markdown_rows(EXCERPTS / "interboard-wiring.md", "## A2 TRANSFORMER, J3") if row[0].isdigit()}
		self.assertEqual((transformer_j3["8"], transformer_j3["9"]), ("A3J3-12", "A3J3-5"))
		self.assertIn("the SDU sheet's `A2J3-8` is a misprint for A2J3-9", self.solenoids[19]["physical"]["notes"])

	def test_the_table_flippers_follow_the_relay_through_the_vpinmame_library(self) -> None:
		library = (EXCERPTS / "vpinmame-library.md").read_text(encoding="utf-8")
		self.assertIn("Const GameOnSolenoid = 19", library)
		self.assertIn("If nsol = vpmFlips.Solenoid Then vpmFlips.TiltSol bstate", library)
		relay = self.solenoids[19]
		self.assertIn(curator.VPM_LIBRARY_SOURCE, relay["provenance"]["source_refs"])
		self.assertIn("`vpmFlips.TiltSol`", relay["physical"]["notes"])
		# TiltSol reaches EnableFlippers, which with the constructor's TiltObjects=1 also calls SolGameOn; with the game off that
		# sets the tilt objects' thresholds to 100, so the thumper bumper and slingshots stop kicking on a tilt too.
		self.assertIn("EnableFlippers(aEnabled)", library)
		self.assertIn("Sol=0 : TiltObjects=1", library)
		self.assertIn("If TiltObjects then vpmnudge.solgameon aEnabled", library)
		self.assertIn("If TypeName(obj) = \"Bumper\" Then obj.Threshold = 100", library)
		self.assertIn("None of the three scripts (both corpus scripts and the retained table's) mentions `TiltObjects`", library)
		self.assertIn("So on a tilt the table's flippers go dead and the thresholds of `vpmNudge.TiltObj` (the thumper bumper and both slingshots) rise to 100",
			relay["physical"]["notes"])
		self.assertIn("a dead binding that the library makes redundant", relay["physical"]["notes"])
		self.assertNotIn("keep kicking", relay["physical"]["notes"])
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertNotIn("keep kicking", knowledge)
		self.assertIn("so on a tilt the table's flippers\ngo dead and its thumper bumper and slingshots stop kicking; the retained run exercised only the right slingshot while tilted", knowledge)
		# The ROM side was exercised only on the right slingshot while tilted; the library covers all three tilt objects.
		self.assertIn("the ROM fired nothing for the right slingshot while tilted, the only one of the three it exercised", relay["physical"]["notes"])
		self.assertNotIn("fires none of their coils", relay["physical"]["notes"])
		# The relay also pulses outside play (power-up, slam re-initialisation, burn-in, the solenoid test), stated for the retained runs, and ball 3 exercised the
		# left slingshot and left flipper, not the right slingshot.
		self.assertIn("outside play the retained runs\nshow it raised only in the power-up initialisation pulse", knowledge)
		self.assertIn("(at power-up and after a slam) and in the ROM's burn-in and solenoid\ntests, and off in steady attract mode.", knowledge)
		self.assertIn("the flipper relay off in steady attract mode, after the power-up\n  initialisation pulse, until a game starts.", knowledge)
		self.assertIn("a right slingshot hit while tilted fired nothing, and on the next ball the left\nslingshot and the left flipper button both worked", knowledge)
		self.assertNotIn("on only during a game", knowledge)
		self.assertNotIn("until the next ball", knowledge)
		# A bank's repeated reset was observed only while the host held all of its targets down.
		text = json.dumps(self.definition, ensure_ascii=False)
		self.assertNotIn("while a target stays down", text)
		self.assertEqual(text.count("while the host holds all three targets down"), 4)
		self.assertIn("while the host holds all six targets down", self.solenoids[13]["physical"]["notes"])
		library_source = next(source for source in self.definition["sources"] if source["id"] == curator.VPM_LIBRARY_SOURCE)
		self.assertEqual(library_source["sha256"], curator.VPM_LIBRARY_FILES["stern.vbs"])
		self.assertIn(curator.VPM_LIBRARY_FILES["core.vbs"], library_source["locator"])

	def test_mesh_placements_cite_the_world_space_exports(self) -> None:
		# The dead bumpers' and the G.I.'s centres come from the world-space exports, which only the extraction source pins.
		extraction = next(source for source in self.definition["sources"] if source["id"] == curator.EXTRACTION_SOURCE)
		self.assertIn(curator.WORLD_OBJ_SHA256, extraction["locator"])
		self.assertIn(curator.BUMPERS_VISIBLE_OBJ_SHA256, extraction["locator"])
		self.assertIn(curator.BUMPERS_VISIBLE_VPX_SHA256, extraction["locator"])
		gi = next(item for item in self.definition["outputs"] if item["kind"] == "gi")
		for item in [self.switches[12], self.switches[13], gi]:
			self.assertIn(curator.EXTRACTION_SOURCE, item["provenance"]["source_refs"], item["id"])
			for placement in item["spatial"]["placements"]:
				self.assertIn(curator.EXTRACTION_SOURCE, placement["provenance"]["source_refs"], placement["id"])
		for address, item in self.switches.items():
			if address not in (12, 13):
				for placement in item.get("spatial", {}).get("placements", []):
					self.assertNotIn(curator.EXTRACTION_SOURCE, placement["provenance"]["source_refs"], placement["id"])

	def test_each_excerpt_states_how_it_was_transcribed(self) -> None:
		records = {item["id"]: item for source in self.definition["sources"] for item in source.get("excerpts", [])}
		# Text copied from retained files is a manual copy; the scanned manual and card pages were read from 300 dpi renders.
		for name in ("vpinmame-library", "ipdb-schematic-errata"):
			record = records[f"excerpt.meteor.{name}"]
			self.assertEqual((record["method"], record["reviewed"]), ("manual", False), name)
			self.assertIn("copied verbatim from", record["transcribed_by"], name)
			self.assertNotIn("dpi", record["transcribed_by"], name)
		scanned = [record for key, record in records.items() if key not in ("excerpt.meteor.vpinmame-library", "excerpt.meteor.ipdb-schematic-errata")]
		self.assertEqual(len(scanned), len(records) - 2)
		for record in scanned:
			header = (ROOT / record["path"]).read_text(encoding="utf-8").splitlines()[0]
			self.assertEqual(record["method"], "mixed", record["id"])
			# Each record repeats the render range its excerpt's own header states; only the MPU sheet was read beyond the scan's 300 dpi.
			if "Transcribed from 250-600 dpi renders" in header:
				self.assertEqual(record["id"], "excerpt.meteor.mpu-schematic")
				self.assertEqual(record["transcribed_by"], "curator, read from 250-600 dpi renders of the 300 dpi scan, the faint S33 label on the 600 dpi render; not yet checked cell by cell")
			else:
				self.assertRegex(header, r"Transcribed from (page renders at their native resolution|a 300 dpi render)", record["id"])
				self.assertEqual(record["transcribed_by"], "curator, read from 300 dpi page renders; not yet checked cell by cell", record["id"])

	def test_knock_down_spotting_and_variant_runs_claim_only_what_was_run(self) -> None:
		for coil, _ in METEOR_BANK.values():
			self.assertIn("(manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, switches 4, 38 and 40)",
				self.solenoids[coil]["physical"]["notes"], coil)
			# The run had one player: it shows the restore at a drain, not a player change.
			self.assertIn("exercised no player change", self.solenoids[coil]["physical"]["notes"], coil)
		self.assertIn("The status of the target is restored for each player after the ball enters the outhole and the bonus is collected (memory).",
			(EXCERPTS / "feature-operation.md").read_text(encoding="utf-8"))
		for address in (61, 63):
			self.assertIn("The VR callback also", self.lamps[address]["physical"]["notes"], address)
		for address in BACKBOX_LAMPS:
			self.assertIn(f"as the desktop backglass reel `L{address}` (`FadeReel`)", self.lamps[address]["physical"]["notes"], address)
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		for identifier in curator.RUN_SOURCES:
			if not identifier.endswith("-variant-io"):
				continue
			note = drivers[identifier.removesuffix("-variant-io")]["variant_notes"]
			self.assertIn("only solenoid sets were compared, not firing order, timing or lamps", note, identifier)
			self.assertIn("No METEOR target switch closed before its drain", note, identifier)
			self.assertIn("though not in the same windows", note, identifier)
			# A variant that spotted a different target does not list the stand-up target among the matching steps.
			if "spots a different METEOR target" in note:
				self.assertNotIn("the stand-up target, the right three-bank", note, identifier)
		# The knowledge note limits step-by-step agreement to the steps before the drain and compares the kick and resets across the drain and serve together.
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("was run once. Before the drain each fired the same set of solenoids as `meteor` for the same steps", knowledge)
		self.assertIn("Across the drain and the next\nserve taken together each fired the outhole kick (15) and the bank resets (3, 7, 9, 13), though not in the same windows", knowledge)
		self.assertNotIn("was run once and fired the same set of solenoids", knowledge)

	def test_three_bank_assembly_numbers_follow_the_drawing_callouts(self) -> None:
		parts = (EXCERPTS / "playfield-parts.md").read_text(encoding="utf-8")
		self.assertIn("3-BANK TARGET D-580-1 to 3", parts)
		self.assertIn("\"2-3\" beside the thick dashed segments on the right (3-bank target)", parts)
		self.assertIn("\"2-2\" with thick dashed segments (3-bank target)", parts)
		self.assertIn("\"2-1\" with thick dashed segments (3-bank target)", parts)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual({bank: mechanisms[f"mech.{bank}-three-bank"]["assembly_part_number"] for bank in ("right", "top-left", "lower-left")},
			{"right": "D-580-3", "top-left": "D-580-2", "lower-left": "D-580-1"})

	def test_every_unlisted_connector_branch_is_stated_on_its_lamp(self) -> None:
		excerpt = EXCERPTS / "lamp-driver.md"
		entries, jack = [], None
		for line in excerpt.read_text(encoding="utf-8").splitlines():
			heading = re.match(r"^### (J[123]) ", line)
			if heading:
				jack = heading.group(1)
			elif line.startswith("## "):
				jack = None
			elif jack and line.startswith("|") and not re.match(r"^\|\s*:?-+", line):
				row = [cell.strip() for cell in line.strip().strip("|").split("|")]
				if row[0].isdigit():
					entries.append((jack, row[1], row[2]))
		rows = [row for row in markdown_rows(excerpt, "## 3.") if len(row) == 6 and row[0].isdigit() and re.match(r"^J-[123]$", row[3])]
		lamp_of = {transistor: address for address, transistor in decoder_table().items()}
		checked = 0
		for jack, pin, scr in entries:
			if not re.match(r"^Q\d+$", scr) or int(scr[1:]) not in lamp_of:
				continue
			notes = self.lamps[lamp_of[int(scr[1:])]]["physical"]["notes"]
			# Only the lamp-list rows this lamp's own note quotes count as listing a branch of its SCR.
			listed = {(f"J{row[3][2:]}", row[4]) for row in rows if f"row {row[0]} `{row[1]}`" in notes}
			if (jack, pin) in listed:
				continue
			# A legible branch is named by its pin, as a whole number; an illegible one quotes the printed pin cell verbatim.
			reading = f"{jack} pin {pin}" if pin.isdigit() else f"{jack} pin `{pin}`"
			self.assertRegex(notes, re.escape(reading) + r"(?![0-9])", (jack, pin, scr))
			checked += 1
		self.assertGreater(checked, 10)
		for address in (12, 28, 43, 44, 60):
			self.assertIn("a branch no lamp-list row uses; no bulb is asserted on it", self.lamps[address]["physical"]["notes"], address)

	def test_connector_block_readings_are_the_excerpts(self) -> None:
		import meteor_data as data
		self.assertEqual(curator.excerpt_connector_blocks(ROOT), data.CONNECTOR_BLOCKS)
		original = copy.deepcopy(data.CONNECTOR_BLOCKS)
		misread = copy.deepcopy(original)
		misread["J2"][misread["J2"].index(("? (4)", 39))] = ("? (6)", 39)
		with mock.patch.object(data, "CONNECTOR_BLOCKS", misread):
			with self.assertRaises(RuntimeError, msg="data disagreeing with the excerpt"):
				curator.build_definition(ROOT)
			# With the excerpt comparison bypassed, the lamp note still has to state every unlisted branch as printed.
			with mock.patch.object(curator, "excerpt_connector_blocks", lambda root: misread):
				with self.assertRaises(RuntimeError, msg="branch not stated on its lamp"):
					curator.build_definition(ROOT)
		# A pin that is only the prefix of a stated one (J3 pin 1 inside "J3 pin 13") is not stated.
		prefix = copy.deepcopy(original)
		prefix["J3"][prefix["J3"].index(("3", 52))] = ("1", 52)
		with mock.patch.object(data, "CONNECTOR_BLOCKS", prefix), mock.patch.object(curator, "excerpt_connector_blocks", lambda root: prefix):
			with self.assertRaises(RuntimeError, msg="pin prefix"):
				curator.build_definition(ROOT)
		self.assertEqual(data.CONNECTOR_BLOCKS, original)
		# The X on Q21's J1 pin 12 entry may cancel it; Spinner 3 keeps the list's pin and says so.
		self.assertIn("| 25 | 12 | Q21 | no | X drawn through the triangle column between pin 12 and Q21 |", (EXCERPTS / "lamp-driver.md").read_text(encoding="utf-8"))
		spinner = self.lamps[28]
		self.assertEqual(spinner["wiring"]["drive_connection"], "A5J1-12")
		self.assertIn("with an X drawn through the triangle column between pin 12 and Q21, a mark that may cancel that entry", spinner["physical"]["notes"])

	def test_option_switch_defaults_follow_pinned_pinmame(self) -> None:
		for address, item in self.dips.items():
			expected = "ON" if address in (20, 21) else "OFF"
			self.assertIn(f"PinMAME's default for this switch is {expected}.", item["physical"]["notes"], address)
		self.assertIn("default OFF except S20 and S21, which default ON", next(source["locator"] for source in self.definition["sources"] if source["id"] == curator.CORE_SOURCE))
		self.assertIn("(S20 and S21 ON, the rest OFF)", self.observations["runs"]["coin-bookkeeping"]["note"])

	def test_game_end_knocker_is_the_match_award(self) -> None:
		note = self.observations["runs"]["gameplay"]["note"]
		self.assertIn("Player 1's final score 539740 ends in the match number 40, the credits go from 02 to 03, and the knocker (6) fires once: a match award", note)
		self.assertIn("After the last drain the outhole kicker does not fire", note)
		self.assertIn("a match award (option switch 21, ON at PinMAME's default)", self.solenoids[6]["physical"]["notes"])
		self.assertIn("After the last ball's drain the retained gameplay trace records no pulse of it in the 30 s the host then holds 33 closed", self.solenoids[15]["physical"]["notes"])
		outhole = next(item for item in self.definition["mechanisms"] if item["id"] == "mech.outhole")
		# Only the kick-then-resets order holds in every run: some variants report 19 and 15 at the same moment.
		self.assertIn("and fires the outhole kicker followed by the four bank resets in sequence (15, then 3, 7, 9 and 13", json.dumps(outhole))
		self.assertNotIn("then fires the outhole kicker", json.dumps(outhole))
		self.assertNotIn("together", json.dumps(outhole))
		readings = {label: item["reading"] for label, item in load_json(ROOT / "tools/seeds/stern/meteor-1979-frame-readings.json")["runs"]["gameplay"].items()}
		self.assertEqual(readings["player 1 score at the game end"][-2:], readings["match number at the game end"])
		self.assertEqual(int(readings["credits at the game end"]), int(readings["credits before the last drain"]) + 1)

	def test_curator_refuses_incomplete_runtime_evidence(self) -> None:
		import tempfile
		damages = {
			"extractor": lambda document: document.pop("extractor"),
			"note": lambda document: document["runtime"]["observations"]["runs"]["gameplay"].__setitem__("note", ""),
			"version": lambda document: document.pop("version"),
			"source digest": lambda document: document["source"].__setitem__("sha256", "bogus"),
			"scenario path": lambda document: document["runtime"]["raw_runs"][0].pop("scenario_path"),
			"snapshot count": lambda document: document["runtime"]["raw_runs"][3].pop("snapshot_count"),
			"scenario digest": lambda document: document["runtime"]["raw_runs"][4].__setitem__("scenario_sha256", "0" * 64),
			"emulator": lambda document: document["runtime"].pop("emulator"),
			"gameplay actions": lambda document: document["runtime"]["observations"]["runs"]["gameplay"].pop("named_action_observations"),
			"empty gameplay actions": lambda document: document["runtime"]["observations"]["runs"]["gameplay"].__setitem__("named_action_observations", []),
			"solenoid-test order": lambda document: document["runtime"]["observations"]["runs"]["solenoid-test"].pop("ordered_solenoid_on_sequence"),
			# Truncations the field checks cannot see: only the pinned digest refuses them.
			"one gameplay action dropped": lambda document: document["runtime"]["observations"]["runs"]["gameplay"]["named_action_observations"].pop(),
			"solenoid-test order truncated": lambda document: document["runtime"]["observations"]["runs"]["solenoid-test"].__setitem__(
				"ordered_solenoid_on_sequence", document["runtime"]["observations"]["runs"]["solenoid-test"]["ordered_solenoid_on_sequence"][:1]),
		}
		for damage, apply in damages.items():
			document = copy.deepcopy(self.runtime)
			apply(document)
			with tempfile.TemporaryDirectory() as directory:
				path = Path(directory) / RUNTIME_PATH.relative_to(ROOT)
				path.parent.mkdir(parents=True)
				path.write_bytes(canonical_bytes(document))
				with self.assertRaises(RuntimeError, msg=damage):
					curator.runtime_document(Path(directory))
		# Every run source pins the committed compact evidence, so an edit to it changes the definition.
		digest = hashlib.sha256(RUNTIME_PATH.read_bytes()).hexdigest()
		runs = [source for source in self.definition["sources"] if source["id"] in curator.RUN_SOURCES.values()]
		self.assertEqual(len(runs), len(curator.RUN_SOURCES))
		for source in runs:
			self.assertIn(f"(SHA-256 {digest})", source["locator"], source["id"])

	def test_option_switches(self) -> None:
		self.assertEqual(set(self.dips), set(range(1, 33)))
		self.assertIn("Balls per game", self.dips[7]["label"])
		for address in (14, 31, 32):
			self.assertIn("Special award", self.dips[address]["label"])

	def test_mechanisms_name_existing_devices(self) -> None:
		devices = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for item in mechanisms.values():
			for device in item["actuators"] + item["sensors"]:
				self.assertIn(device, devices, item["id"])
		self.assertEqual(len(mechanisms["mech.meteor-bank"]["actuators"]), 7)
		self.assertEqual(len(mechanisms["mech.meteor-bank"]["sensors"]), 6)
		for bank in ("right", "top-left", "lower-left"):
			self.assertEqual(len(mechanisms[f"mech.{bank}-three-bank"]["sensors"]), 3)
		for relationship in self.definition["relationships"]:
			self.assertIn(relationship["source"], devices, relationship["id"])
			self.assertIn(relationship["destination"], devices, relationship["id"])

	def test_displays_match_the_pinned_dispst6_layout(self) -> None:
		displays = [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]]
		self.assertEqual(displays, [(0, 2, 6), (1, 10, 6), (2, 18, 6), (3, 26, 6), (4, 35, 2), (5, 38, 2)])

	def test_excerpts_are_pinned_present_and_clean(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"])
				self.assertFalse(excerpt["reviewed"], excerpt["id"])
		self.assertEqual(count, len(list(EXCERPTS.glob("*"))))
		self.assertEqual(count, 17)
		for path in EXCERPTS.glob("*.md"):
			text = path.read_text(encoding="utf-8")
			self.assertNotIn("\r", text, path.name)
			self.assertIsNone(re.search(r"\.png|crops/|Observations", text), path.name)

	def test_spatial_report_states_the_blockers(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(report["readiness"]["missing"], EXPECTED_MISSING)
		self.assertEqual(report["readiness"]["unresolved_conflicts"], 1)
		unplaced = {(item["group"], item["address"]) for item in report["unplaced_records"]}
		expected = {("pinmame.output.lamp", address) for address in set(self.lamps) - set(BACKBOX_LAMPS)}
		expected |= {("pinmame.input.switch", 33), ("pinmame.output.solenoid", 15), ("physical.input.direct", 6)}
		self.assertEqual(unplaced, expected)
		self.assertTrue(any("No playfield lamp is placed (56 of the 60" in blocker for blocker in report["blockers"]))

	def test_every_placement_is_inside_the_playfield(self) -> None:
		for collection in ("inputs", "outputs"):
			for item in self.definition[collection]:
				for placement in (item.get("spatial") or {}).get("placements", []):
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
					expected = "conflicted" if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] in CONFLICTED_SWITCHES else "observed"
					self.assertEqual(placement["provenance"]["status"], expected, placement["id"])
		for address in range(1, 41):
			spatial = self.switches[address].get("spatial")
			if address in CABINET_SWITCHES:
				self.assertEqual(spatial["reason"], "cabinet_or_service")
			elif address in UNUSED_SWITCHES:
				self.assertEqual(spatial["reason"], "unused")
			elif address == 33:
				self.assertIsNone(spatial)
			else:
				self.assertEqual(len(spatial["placements"]), 1, address)
		gi = self.gi[1]
		self.assertEqual(len(gi["spatial"]["placements"]), 17)
		self.assertNotIn("quantity", gi["physical"])
		# The METEOR bank reads M to R from left to right and from the lower left upwards.
		x = lambda address: self.switches[address]["spatial"]["placements"][0]["x"]
		self.assertEqual(sorted(range(27, 33), key=x), [32, 31, 30, 29, 28, 27])

	def test_knowledge_note_states_the_blockers_and_the_translations(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("1->2, 2->1, 3->6, 4->7", "16 * k + a + 1", "M 58, first E 42, T 26, second E 10, O 57, R 41", "meteora", "unresolved",
				"## What would complete the record", "option switches 14, 31 and 32"):
			self.assertIn(phrase, text)

	def test_no_other_machines_leak_into_the_artifacts(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		forbidden = {machine["id"] for machine in catalog["machines"]} - {MACHINE_ID}
		# Short names of every other Stern driver, the family a copied sibling record would come from (other makers' names include plain words).
		forbidden |= {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") != MACHINE_ID and str(driver.get("machine_id", "")).startswith("stern.")}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		tokens = set()
		for text in texts:
			tokens |= set(re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]", text))
		self.assertFalse(tokens & forbidden, sorted(tokens & forbidden)[:10])

	def test_sources_are_complete_and_pinned(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for identifier in (curator.MANUAL_SOURCE, curator.SELF_TEST_CARD_SOURCE, curator.IPDB_SOURCE, curator.SCRIPT_SOURCE, curator.STANDALONE_SOURCE, curator.TABLE_SOURCE,
				curator.TABLE_SCRIPT_SOURCE, curator.EXTRACTION_SOURCE, curator.VPM_LIBRARY_SOURCE, *curator.RUN_SOURCES.values()):
			self.assertIn(identifier, sources)
		self.assertEqual(sources[curator.SCRIPT_SOURCE]["sha256"], "3e9dab0eb394fd98462c0140866b6b58ae4c9ac2661d76528b976443f72037ea")
		self.assertEqual(sources[curator.STANDALONE_SOURCE]["sha256"], "d2e0a5ebd8d9e4544b427f7450bc24fcbdd928a2ae58ebd4c0f8e8f88dc23ca7")
		self.assertTrue(sources[curator.SCRIPT_SOURCE]["known_working"] and sources[curator.STANDALONE_SOURCE]["known_working"])
		self.assertEqual(sources[curator.TABLE_SOURCE]["sha256"], "0f8c826c3e9565835189b79d599a1dd72aa5dd20e1347d6fab8477fa1ff65614")
		self.assertEqual(sources[curator.EXTRACTION_SOURCE]["sha256"], curator.EXTRACTION_MANIFEST_SHA256)
		runs = {run["name"]: run for run in self.runtime["runtime"]["raw_runs"]}
		self.assertEqual(list(runs), list(curator.RUN_SOURCES))
		for name, identifier in curator.RUN_SOURCES.items():
			self.assertEqual(sources[identifier]["sha256"], runs[name]["sha256"])
			scenario = ROOT / runs[name]["scenario_path"]
			self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), runs[name]["scenario_sha256"], name)
			self.assertNotIn(b"\r\n", scenario.read_bytes(), name)
			self.assertEqual(curator.RUN_AT[name], sources[identifier]["acquired_at"], name)
		self.assertEqual({source["kind"] for identifier, source in sources.items() if identifier in curator.RUN_SOURCES.values()}, {"service_diagnostic", "runtime_scenario"})
		referenced = {ref for item in self.definition["inputs"] + self.definition["outputs"] for ref in item["provenance"]["source_refs"]}
		self.assertLessEqual(referenced, set(sources))
		for identifier, source in sources.items():
			self.assertRegex(source.get("acquired_at", ""), r"^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$", identifier)


class MeteorRetainedEvidenceTests(unittest.TestCase):
	"""Exact retained artifacts, checked only when the external roots are configured."""

	@staticmethod
	def _harness_root() -> Path | None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		return Path(root) / "meteor-1979" / "harness" if root else None

	def test_pinmame_source_licenses_follow_the_cited_files_markers(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		checkout = Path(root).parent / "source-checkouts" / f"pinmame-{curator.PINMAME_REVISION[:8]}"
		self.assertIn("Every file that doesn't, will stay (for now) under the 'old MAME' license.", (checkout / "LICENSE").read_text(encoding="utf-8"))
		for name in curator.PINMAME_UNMARKED_FILES + curator.PINMAME_BSD_FILES:
			first = (checkout / name).read_text(encoding="utf-8", errors="replace").splitlines()[0]
			self.assertEqual(first == "// license:BSD-3-Clause", name in curator.PINMAME_BSD_FILES, name)
		# The core source cites exactly these files, and the catalog source only stgames.c.
		sources = {source["id"]: source for source in load_json(DEFINITION_PATH)["sources"]}
		self.assertEqual(set(re.findall(r"src/wpc/\w+\.[ch]\b", sources[curator.CORE_SOURCE]["locator"])), set(curator.PINMAME_UNMARKED_FILES + curator.PINMAME_BSD_FILES))
		self.assertEqual(set(re.findall(r"src/wpc/\w+\.[ch]\b", sources[curator.CATALOG_SOURCE]["locator"])), {"src/wpc/stgames.c"})

	def test_harness_runs_reproduce_the_runtime_summary(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_meteor_runtime as summary
		self.assertEqual(canonical_bytes(summary.build(runs_root)), RUNTIME_PATH.read_bytes())

	def test_a_substituted_display_frame_is_refused(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_meteor_runtime as summary
		original = summary._load_run

		def substituted(root: Path, name: str):
			run = original(root, name)
			if name == "switch-test":
				run = copy.deepcopy(run)
				snapshot = next(item for item in run["snapshots"] if item["label"].startswith("close 5"))
				segments = snapshot["displays"][0]["segments"]
				# Show 6 where the ROM showed 5: same digit count, a different frame.
				index = next(position for position, word in enumerate(segments) if word & 0x7F == 0x6D)
				segments[index] = (segments[index] & 0x80) | 0x7D
			return run

		with mock.patch.object(summary, "_load_run", substituted):
			with self.assertRaises(RuntimeError):
				summary.build(runs_root)

	def test_a_variant_drain_without_its_kick_is_refused(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_meteor_runtime as summary
		original = summary._load_run

		def stripped(root: Path, name: str):
			run = original(root, name)
			if name == "meteora-variant-io":
				run = copy.deepcopy(run)
				drain = next(action for action in summary.windowed_actions(run) if action["step"]["label"] == summary.DRAIN_STEPS[0])
				# Drop the outhole kicks of the drain window only; the release window still fires its own.
				run["events"] = [event for event in run["events"]
					if not (event["event"] == "solenoid" and event["number"] == 15 and drain["start"] < event["time_s"] <= drain["end"])]
			return run

		with mock.patch.object(summary, "_load_run", stripped):
			with self.assertRaises(RuntimeError):
				summary.build(runs_root)

	def test_a_reference_release_without_restores_is_refused(self) -> None:
		runs_root = self._harness_root()
		if runs_root is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_meteor_runtime as summary
		original = summary._load_run

		def stripped(root: Path, name: str):
			run = original(root, name)
			if name == "gameplay":
				run = copy.deepcopy(run)
				release = next(action for action in summary.windowed_actions(run) if action["step"]["label"] == summary.DRAIN_STEPS[1])
				# Drop every solenoid event of the first release window; the drain window still restores all four targets.
				run["events"] = [event for event in run["events"]
					if not (event["event"] == "solenoid" and release["start"] < event["time_s"] <= release["end"])]
			return run

		with mock.patch.object(summary, "_load_run", stripped):
			with self.assertRaisesRegex(RuntimeError, "served ball's release"):
				summary.build(runs_root)

	def test_retained_table_extraction_and_coordinates(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import meteor_data as data
		from pinmame_game_defs.spatial import _item_point
		folder = Path(root) / curator.TABLE_RELATIVE
		table = folder / curator.TABLE_FILENAME
		self.assertEqual(table.stat().st_size, curator.TABLE_BYTES)
		self.assertEqual(hashlib.sha256(table.read_bytes()).hexdigest(), curator.TABLE_SHA256)
		curator.verify_extraction_manifest(Path(root))
		extraction = Path(root) / curator.EXTRACTION_RELATIVE
		self.assertEqual(hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest(), curator.TABLE_SCRIPT_SHA256)
		bounds = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
		self.assertEqual((bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]), (0.0, 0.0, data.TABLE_WIDTH, data.TABLE_HEIGHT))
		for name, (item_type, x, y, file) in data.OBJECTS.items():
			path = extraction / "gameitems" / file
			self.assertTrue(path.is_file(), name)
			if item_type == "Primitive":
				# A baked dead-bumper mesh: the centre of its whole bounding box.
				pieces = mesh_pieces(extraction, name)
				self.assertAlmostEqual((min(piece[0] for piece in pieces) + max(piece[2] for piece in pieces)) / 2, x, places=4, msg=name)
				self.assertAlmostEqual((min(piece[1] for piece in pieces) + max(piece[3] for piece in pieces)) / 2, y, places=4, msg=name)
				continue
			document = json.loads(path.read_text(encoding="utf-8"))
			self.assertEqual(next(iter(document)), item_type, name)
			value = document[item_type]
			self.assertEqual(value["name"], name)
			self.assertAlmostEqual(_item_point(item_type, value)[0], x, places=4, msg=name)
			self.assertAlmostEqual(_item_point(item_type, value)[1], y, places=4, msg=name)
		lights = {path.name: json.loads(path.read_text(encoding="utf-8"))["Light"] for path in (extraction / "gameitems").glob("Light.*.json")}
		self.assertEqual(len(lights), 302)
		self.assertFalse(any(light.get("show_bulb_mesh") for light in lights.values()))
		for x, y, name in data.GI_BULBS:
			light = lights[f"Light.{name}.json"]
			self.assertLess(((light["center"]["x"] - x) ** 2 + (light["center"]["y"] - y) ** 2) ** 0.5, 3.6, name)
		# Each G.I. placement is the bounding-box centre of one connected piece of the baked bulb mesh.
		centres = sorted(((left + right) / 2, (top + bottom) / 2) for left, top, right, bottom in mesh_pieces(extraction, "layer1bulbs"))
		self.assertEqual(len(centres), len(data.GI_BULBS))
		for (x, y), (expected_x, expected_y, name) in zip(centres, sorted(data.GI_BULBS)):
			self.assertAlmostEqual(x, expected_x, places=4, msg=name)
			self.assertAlmostEqual(y, expected_y, places=4, msg=name)

	def test_world_space_export_reproduces_the_mesh_centres(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import meteor_data as data
		export = Path(root) / curator.WORLD_OBJ_RELATIVE
		self.assertEqual(export.stat().st_size, curator.WORLD_OBJ_BYTES)
		self.assertEqual(hashlib.sha256(export.read_bytes()).hexdigest(), curator.WORLD_OBJ_SHA256)
		vertices, objects = read_world_obj(export)
		# The export leaves out the invisible dead-bumper meshes, which share layer1bulbs' position, size and rotation.
		self.assertNotIn("bumper2", objects)
		self.assertNotIn("bumper3", objects)
		extraction = Path(root) / curator.EXTRACTION_RELATIVE / "gameitems"
		transforms = {name: {key: json.loads((extraction / f"Primitive.{name}.json").read_text(encoding="utf-8"))["Primitive"][key] for key in ("position", "size", "rot_and_tra")}
			for name in ("bumper2", "bumper3", "layer1bulbs")}
		self.assertEqual(transforms["bumper2"], transforms["layer1bulbs"])
		self.assertEqual(transforms["bumper3"], transforms["layer1bulbs"])
		members, faces = objects["layer1bulbs"]
		parent = {index: index for index in members}

		def find(index: int) -> int:
			while parent[index] != index:
				parent[index] = parent[parent[index]]
				index = parent[index]
			return index

		for face in faces:
			for vertex in face[1:]:
				parent[find(face[0])] = find(vertex)
		groups: dict[int, list[int]] = {}
		for index in members:
			groups.setdefault(find(index), []).append(index)
		centres = sorted(((min(vertices[i][0] for i in group) + max(vertices[i][0] for i in group)) / 2, (min(vertices[i][1] for i in group) + max(vertices[i][1] for i in group)) / 2)
			for group in groups.values())
		self.assertEqual(len(centres), len(data.GI_BULBS))
		for (x, y), (expected_x, expected_y, name) in zip(centres, sorted(data.GI_BULBS)):
			self.assertAlmostEqual(x, expected_x, delta=0.0001, msg=name)
			self.assertAlmostEqual(y, expected_y, delta=0.0001, msg=name)

	def test_visibility_derivative_exports_the_dead_bumpers(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import meteor_data as data
		folder = Path(root) / curator.BUMPERS_VISIBLE_RELATIVE
		table = folder / curator.BUMPERS_VISIBLE_VPX
		self.assertEqual(table.stat().st_size, curator.BUMPERS_VISIBLE_VPX_BYTES)
		self.assertEqual(hashlib.sha256(table.read_bytes()).hexdigest(), curator.BUMPERS_VISIBLE_VPX_SHA256)
		# The derivative's re-extraction is the retained extraction with only the two primitives' visibility changed.
		manifest_bytes = (folder / "extracted-vpxtool.manifest.json").read_bytes()
		self.assertEqual(hashlib.sha256(manifest_bytes).hexdigest(), curator.BUMPERS_VISIBLE_MANIFEST_SHA256)
		self.assertEqual(manifest_bytes, curator.canonical_bytes(curator.build_extraction_manifest(folder / "extracted-vpxtool")))
		derived = {item["path"]: item for item in json.loads(manifest_bytes)["files"]}
		original = {item["path"]: item for item in curator.verify_extraction_manifest(Path(root))["files"]}
		changed = sorted(path for path in original.keys() | derived.keys() if original.get(path) != derived.get(path))
		self.assertEqual(changed, ["gameitems/Primitive.bumper2.json", "gameitems/Primitive.bumper3.json"])
		for path in changed:
			before = json.loads((Path(root) / curator.EXTRACTION_RELATIVE / path).read_text(encoding="utf-8"))["Primitive"]
			after = json.loads((folder / "extracted-vpxtool" / path).read_text(encoding="utf-8"))["Primitive"]
			self.assertEqual((before.pop("is_visible"), after.pop("is_visible")), (False, True), path)
			self.assertEqual(before, after, path)
		export = Path(root) / curator.BUMPERS_VISIBLE_OBJ_RELATIVE
		self.assertEqual(export.stat().st_size, curator.BUMPERS_VISIBLE_OBJ_BYTES)
		self.assertEqual(hashlib.sha256(export.read_bytes()).hexdigest(), curator.BUMPERS_VISIBLE_OBJ_SHA256)
		vertices, objects = read_world_obj(export)
		table_vertices, table_objects = read_world_obj(Path(root) / curator.WORLD_OBJ_RELATIVE)
		# The derivative's export adds the two bumpers and leaves every object of the table's export as it was.
		self.assertEqual(set(objects) - set(table_objects), {"bumper2", "bumper3"})
		self.assertEqual(set(table_objects) - set(objects), set())
		for name, (members, _) in table_objects.items():
			self.assertEqual([vertices[index] for index in objects[name][0]], [table_vertices[index] for index in members], name)
		for name in ("bumper2", "bumper3"):
			xs = [vertices[index][0] for index in objects[name][0]]
			ys = [vertices[index][1] for index in objects[name][0]]
			_, x, y, _ = data.OBJECTS[name]
			self.assertAlmostEqual((min(xs) + max(xs)) / 2, x, places=6, msg=name)
			self.assertAlmostEqual((min(ys) + max(ys)) / 2, y, places=6, msg=name)

	def test_retained_vpinmame_library_matches_its_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		folder = Path(root) / curator.VPM_LIBRARY_RELATIVE
		for name, digest in curator.VPM_LIBRARY_FILES.items():
			self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest, name)
		self.assertIn(b"Const GameOnSolenoid = 19", (folder / "stern.vbs").read_bytes())
		# Every line the library excerpt quotes is a line of the retained file its section names, and each `Line N:` quote is that file's line N.
		files = {name: (folder / name).read_bytes().decode("utf-8").split("\r\n") for name in curator.VPM_LIBRARY_FILES}
		current, fenced, quoted = None, False, 0
		for line in (EXCERPTS / "vpinmame-library.md").read_text(encoding="utf-8").splitlines():
			if line.startswith("## "):
				current = line[3:].strip() if line[3:].strip() in files else None
			elif line == "```":
				fenced = not fenced
			elif current and fenced and line:
				self.assertIn(line, files[current], (current, line))
				quoted += 1
			elif current and (match := re.fullmatch(r"Line (\d+): `(.*)`", line)):
				self.assertEqual(files[current][int(match.group(1)) - 1], match.group(2), (current, line))
				quoted += 1
		self.assertGreater(quoted, 60)

	def test_retained_documents_match_their_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("PINMAME_MANUALS_ROOT is not set")
		folder = Path(root) / "by-machine" / MACHINE_ID / "ipdb"
		for name, digest in ((curator.MANUAL_PDF, curator.MANUAL_SHA256), (curator.SELF_TEST_CARD_PDF, curator.SELF_TEST_CARD_SHA256), ("machine-1580.html", curator.IPDB_PAGE_SHA256)):
			self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), digest, name)
		# The errata excerpt quotes the page's own text: tags removed, entities decoded, whitespace collapsed.
		page = html.unescape(re.sub(r"<[^>]+>", " ", (folder / "machine-1580.html").read_text(encoding="utf-8", errors="replace")))
		page = re.sub(r"\s+", " ", page)
		quotes = [line[2:] for line in (EXCERPTS / "ipdb-schematic-errata.md").read_text(encoding="utf-8").splitlines() if line.startswith("> ")]
		self.assertEqual(len(quotes), 1)
		self.assertIn(quotes[0], page)

	def test_rom_archives_match_the_runs(self) -> None:
		root = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not root:
			self.skipTest("user-authorized ROM library root is not configured")
		for driver, digest in curator.ROM_ARCHIVES.items():
			self.assertEqual(hashlib.sha256((Path(root) / f"{driver}.zip").read_bytes()).hexdigest(), digest, driver)


# Every solenoid note as reviewed, word for word. The source checks above verify the wiring these notes quote against the excerpts; this pin makes any added,
# removed or reworded statement fail, in whatever wording, so a claim cannot reach a note without the test changing with it.
PINNED_SOLENOID_NOTES = {
	1: ("SDU driver Q2, printed load `LEFT SLING-SHOT` (J2-4, BRN) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 02 as "
		"`Left Sling Shot`. The ROM's solenoid test shows 02 while public 1 fires. Fired when the left slingshot switch (public 16) closes in the retained "
		"gameplay and variant runs. The playfield coil sheet prints `LEFT SLING SHOT A3J2-4 (BRN-)`. Neither known-working script has a SolCallback for it: "
		"the table's slingshot kicks on its own hit. Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits "
		"under it."),
	2: ("SDU driver Q1, printed load `CENTER THUMPER` (J2-9, PUR-W) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 01 as "
		"`Thumper Bumper`. The ROM's solenoid test shows 01 while public 2 fires. Fired when the thumper switch (public 14) closes in the retained gameplay "
		"and variant runs. The playfield coil sheet prints `THUMPER A3J2-4 (PUR-W)`; the wire colour is the SDU's J2-9 and the pin repeats the left "
		"slingshot's, so the definition follows the SDU sheet's J2-9, a connector-pin reading only. Neither known-working script has a SolCallback for it: the "
		"table's bumper kicks on its own hit. Placed on the retained table's Bumper `bumper1`, the thumper bumper whose own hit kicks the ball in that table."),
	3: ("SDU driver Q5, printed load `LEFT TOP DROP TARGET` (J2-10, G-R) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 05 "
		"as `3-Bank Drop Target (L. Top)`. The ROM's solenoid test shows 05 while public 3 fires. Raises the top left three-target bank (19-21; playfield coil "
		"sheet `TOP LFT. 3-BANK DROP TARG.` on A3J2-10 (G-R)). Fired at every serve and when the bank's last target falls (retained gameplay run). Projected "
		"onto the top left three-bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object."),
	4: ("SDU driver Q6, printed load `\"M\" TARGET` (J2-11, GREY) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 06 as `6-Bank "
		"Drop Targets`. The ROM's solenoid test shows 06 while public 4 fires. Knocks down the METEOR M target (switch 32), one of the six `Drop Target Reset "
		"(Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row agree on the "
		"letter, and both known-working scripts drop target 32 from this address. The ROM fires it to spot the target, which a lit star rollover, return lane "
		"or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, switches 4, "
		"38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player after the ball "
		"enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R knock-down coils "
		"after its first drain, the four targets then down, and exercised no player change). Placed on the METEOR target it knocks down (table `sw32`); the "
		"coil sits behind the target and has no object."),
	5: ("SDU driver Q7, printed load `M\"E\"T TARGET` (J2-12, Y-B) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 07 as "
		"`6-Bank Drop Targets`. The ROM's solenoid test shows 07 while public 5 fires. Knocks down the METEOR first E target (switch 31), one of the six `Drop "
		"Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row agree "
		"on the letter, and both known-working scripts drop target 31 from this address. The ROM fires it to spot the target, which a lit star rollover, "
		"return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, "
		"switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player "
		"after the ball enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R "
		"knock-down coils after its first drain, the four targets then down, and exercised no player change). The playfield coil sheet prints this coil's wire "
		"as (Y-W) on A3-J2-12. A wire-colour reading only; the definition follows the SDU sheet. Placed on the METEOR target it knocks down (table `sw31`); "
		"the coil sits behind the target and has no object."),
	6: ("SDU driver Q3, printed load `KNOCKER` (J2-5, B-Y) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 03 as `Knocker`. "
		"The ROM's solenoid test shows 03 while public 6 fires. In the cabinet: the cabinet sheet draws `KNOCKER` on drive A3J2-5 (B-Y) with a diode across "
		"it, fed from the A2J2-2 (G) bus. In the retained gameplay run the ROM fired it once about 2.1 s after the last ball drained, as the final score's "
		"last two digits matched the match number and the credits went up by one: a match award (option switch 21, ON at PinMAME's default). No other award "
		"event was exercised."),
	7: ("SDU driver Q4, printed load `LEFT BOTTOM DROP TARGET` (J1-5, BRN-Y) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid "
		"04 as `3-Bank Drop Target (L. Bottom)`. The ROM's solenoid test shows 04 while public 7 fires. Raises the lower left three-target bank (22-24; "
		"playfield coil sheet `LOWER LFT. 3-BANK DR. TARG.` on A3J1-5 (BRN-Y)). Fired at every serve and when the bank's last target falls (retained gameplay "
		"run). Projected onto the lower left three-bank it resets: the mean of the table's own three target objects."),
	8: ("SDU driver Q8, printed load `\"T\" TARGET` (J5-10, B-Y) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 08 as `6-Bank "
		"Drop Targets`. The ROM's solenoid test shows 08 while public 8 fires. Knocks down the METEOR T target (switch 30), one of the six `Drop Target Reset "
		"(Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row agree on the "
		"letter, and both known-working scripts drop target 30 from this address. The ROM fires it to spot the target, which a lit star rollover, return lane "
		"or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, switches 4, "
		"38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player after the ball "
		"enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R knock-down coils "
		"after its first drain, the four targets then down, and exercised no player change). Placed on the METEOR target it knocks down (table `sw30`); the "
		"coil sits behind the target and has no object."),
	9: ("SDU driver Q13, printed load `RT. DROP TARGET` (J5-12, O-B) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 13 as "
		"`3-Bank Drop Target (Right)`. The ROM's solenoid test shows 13 while public 9 fires. Raises the right three-target bank (9-11; playfield coil sheet "
		"`RIGHT 3-BANK DROP TARGET` on A3-J5-12 (O-B)). Fired at every serve and when the bank's last target falls; the ROM repeats it about every 1.2 s while "
		"the host holds all three targets down (retained gameplay run). Projected onto the right three-bank it resets: the mean of the table's own three "
		"target objects."),
	10: ("SDU driver Q14, printed load `RT. SLING-SHOT` (J5-11, a struck-through `(-B-)` wire) on the Solenoid Driver schematic 12B-432-S113; the self-test "
		"card lists solenoid 14 as `Right Sling-Shot`. The ROM's solenoid test shows 14 while public 10 fires. Fired when the right slingshot switch (public "
		"15) closes in the retained gameplay and variant runs, and not while the game is tilted. Neither known-working script has a SolCallback for it: the "
		"table's slingshot kicks on its own hit. The playfield coil sheet prints `RIGHT SLING SHOT A3J5-11 (O-W)`, which the definition follows. A wire-colour "
		"reading only. Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	11: ("SDU driver Q9, printed load `MET\"E\" TARGET` (J5-9, O-R) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 09 as "
		"`6-Bank Drop Targets`. The ROM's solenoid test shows 09 while public 11 fires. Knocks down the METEOR second E target (switch 29), one of the six "
		"`Drop Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row "
		"agree on the letter, and both known-working scripts drop target 29 from this address. The ROM fires it to spot the target, which a lit star rollover, "
		"return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, "
		"switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player "
		"after the ball enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R "
		"knock-down coils after its first drain, the four targets then down, and exercised no player change). Placed on the METEOR target it knocks down "
		"(table `sw29`); the coil sits behind the target and has no object."),
	12: ("SDU driver Q10, printed load `\"O\" TARGET` (J5-15, B-BLU) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 10 as "
		"`6-Bank Drop Targets`. The ROM's solenoid test shows 10 while public 12 fires. Knocks down the METEOR O target (switch 28), one of the six `Drop "
		"Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row agree "
		"on the letter, and both known-working scripts drop target 28 from this address. The ROM fires it to spot the target, which a lit star rollover, "
		"return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, "
		"switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player "
		"after the ball enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R "
		"knock-down coils after its first drain, the four targets then down, and exercised no player change). Placed on the METEOR target it knocks down "
		"(table `sw28`); the coil sits behind the target and has no object."),
	13: ("SDU driver Q12, printed load `METEOR DROP TARGET` (J5-13, O-W) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 12 as "
		"`6-Bank Drop Target (Reset)`. The ROM's solenoid test shows 12 while public 13 fires. Raises all six METEOR targets (27-32; the SDU sheet's `METEOR "
		"DROP TARGET`, the card's `6-Bank Drop Target (Reset)`). The playfield coil sheet does not draw it. Fired at every serve and when the bank's last "
		"target falls; the ROM repeats it about every 1.2 s while the host holds all six targets down (retained gameplay run). Each completion advances the "
		"bonus multiplier (manual). The parts list counts four `Drop Target Reset` coils B-27-2300: the three three-bank resets and this one. Projected onto "
		"the METEOR bank it resets: the mean of the table's own six target objects."),
	14: ("SDU driver Q11, printed load `\"R\" TARGET` (J5-14, Y-BLU) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 11 as "
		"`6-Bank Drop Targets`. The ROM's solenoid test shows 11 while public 14 fires. Knocks down the METEOR R target (switch 27), one of the six `Drop "
		"Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's load name and the playfield coil sheet's `6-DROP TARGETS` row agree "
		"on the letter, and both known-working scripts drop target 27 from this address. The ROM fires it to spot the target, which a lit star rollover, "
		"return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower star rollovers, "
		"switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player "
		"after the ball enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R "
		"knock-down coils after its first drain, the four targets then down, and exercised no player change). Placed on the METEOR target it knocks down "
		"(table `sw27`); the coil sits behind the target and has no object."),
	15: ("SDU driver Q16, printed load `OUT-HOLE` (J5-8, R-B) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 16 as "
		"`Out-Hole`. The ROM's solenoid test shows 16 while public 15 fires. Kicks the ball resting on the outhole (public 33) into the shooter lane (`Outhole "
		"Kicker (1) J-26-1100`; playfield coil sheet `OUT HOLE A3J5-8 (R-B)`). Fired when a game starts and to serve the next ball after a drain while play "
		"continues. In the retained gameplay and variant runs the ROM follows each serve with the four bank resets (public 3, 7, 9 and 13) and repeats the "
		"serve and the resets while 33 stays closed: about every 1.7 s at a game start and after the variant runs' drains. After the gameplay run's two drains "
		"in play it also fires the T, second E, O and R knock-down coils (public 8, 11, 12 and 14) after the first serve, and the second serve follows about "
		"3.0 s after the first (after the first drain as two kicks 0.10 s apart, followed by one set of bank resets). After the last ball's drain the retained "
		"gameplay trace records no pulse of it in the 30 s the host then holds 33 closed before crediting the next game, so the game ends with the ball in the "
		"outhole. Not placed: both known-working scripts and the retained table kick the ball from a virtual stack into the shooter lane with a `BallRelease` "
		"kicker, so no table object marks the coil, and the playfield parts drawing does not show the outhole."),
	17: ("SDU driver Q17, printed load `N/U` (J5-7) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists no solenoid 17. The ROM's solenoid "
		"test shows 17 while public 17 fires. A continuous-section driver (Q17, PIA PB4 on J4 pin 11 [Y-W]) that the SDU sheet wires only to J5 pin 7 marked "
		"`N/U`; the self-test card lists no solenoid 17 and the parts list no load for it. In the retained runs the ROM drives it only in the power-up "
		"initialisation pulse it gives all four continuous lines (at power-up and after a slam) and in its own burn-in and solenoid tests: it stays off in "
		"attract mode, play, drain, tilt and game over. With no load fitted and that pulse explained, it is unused."),
	18: ("SDU driver Q19, printed load `COIN LOCK-OUT` (J2-8, Y-W) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 19 as `Coin "
		"Lock-Out`. The ROM's solenoid test shows 19 while public 18 fires. A continuous output (Q19, PIA PB5 on J4 pin 9 [BLU-O]) to J2 pin 8 [Y-W] `COIN "
		"LOCK-OUT` (line label `COIN LD.`); the cabinet sheet draws the coil between the A2J2-2 (G) bus and A3J2-8 (Y-W) with a diode across it. The ROM "
		"energizes it about 2.5 s after the power-up pulse and keeps it on in attract mode and play (retained gameplay run), and drops it when the credits "
		"reach the maximum: in the retained coin-bookkeeping run it went off with the coin that brought the credits to 5, the maximum-credits setting at "
		"PinMAME's default (switches 17-19 OFF)."),
	19: ("SDU driver Q15, printed load `FLIPPER ENABLE RELAY` (J3-5, Y-W) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists solenoid 15 "
		"as `Flippers`. The ROM's solenoid test shows 15 while public 19 fires. A continuous output through driver Q15 (PIA PB6 on J4 pin 8 [BLU-W], `FLIPPER "
		"DISABLE`) to the `FLIPPER ENABLE RELAY` on the SDU itself: Q15's collector drives coil terminal 8 on the board, and terminal 7 takes the 43 VDC "
		"supply from J3 pin 5 [Y-W] (CR20 1N4004 across the coil), so the connector pin is the relay's supply, not its drive. The SDU sheet labels that pin "
		"`TO A2J3-8`; the transformer sheet labels A2J3-9 the `FLIPPER ENABLE RE. BUS` and A2J3-8 11.9 VDC, and the interboard wiring diagram 12B-STD.-110-2 "
		"wires A2J3-9 to A3J3-5 and A2J3-8 to A3J3-12, so the SDU sheet's `A2J3-8` is a misprint for A2J3-9. Its contacts connect each flipper button (J2-2 "
		"[BLU] left, J2-1 [R] right) to its flipper coil (J1-8 [G] left, J1-9 [O] right). The ROM raises it when a game starts and drops it on a tilt and at "
		"game over (retained runs). Neither known-working script gives 19 a SolCallback, but both set `UseSolenoids=2` and load the VPinMAME libraries with "
		"`LoadVPM \"01000100\", \"Stern.VBS\", 1.2`: stern.vbs declares `Const GameOnSolenoid = 19`, and core.vbs then hands every change of this output to "
		"`vpmFlips.TiltSol`, whose `EnableFlippers` enables or disables the flippers and, with `TiltObjects` at its default of 1 (no script changes it), calls "
		"`vpmNudge.SolGameOn` with the same state. So on a tilt the table's flippers go dead and the thresholds of `vpmNudge.TiltObj` (the thumper bumper and "
		"both slingshots) rise to 100, so those three stop kicking; in the retained gameplay run the ROM fired nothing for the right slingshot while tilted, "
		"the only one of the three it exercised. The library restores the thresholds when the game is on again. The scripts' `SolCallback(16) = "
		"\"vpmNudge.SolGameOn\"` hangs on public 16, an address the MPU-200 never drives, so it never fires: a dead binding that the library makes redundant."),
	20: ("SDU driver Q18, printed load `N/U` (J2-15) on the Solenoid Driver schematic 12B-432-S113; the self-test card lists no solenoid 18. The ROM's solenoid "
		"test shows 18 while public 20 fires. A continuous-section driver (Q18, PIA PB7 on J4 pin 10 [Y-R]) that the SDU sheet wires only to pins marked `N/U` "
		"(J2 pin 15, J5 pin 3 and J3 pin 9); the self-test card lists no solenoid 18 and the parts list no load for it. In the retained runs the ROM drives it "
		"only in the power-up initialisation pulse it gives all four continuous lines (at power-up and after a slam) and in its own burn-in and solenoid "
		"tests: it stays off in attract mode, play, drain, tilt and game over. With no load fitted and that pulse explained, it is unused."),
	45: ("PinMAME's synthetic power-winding state for the right side, asserted and released together with public 46 for the whole enabled button closure "
		"(retained gameplay and variant runs). It is not another coil and does not measure the power winding."),
	46: ("The lower right flipper and the upper right flipper (parts list `Flipper Left & Right (2)` J-25-500/34-4500; `Flipper Top` J-25-600/34-4500) are "
		"dual-winding coils hard-wired from the +43 VDC flipper supply A2J1-6 (BLU-W) through the flipper enable relay's contact to the right cabinet button; "
		"no numbered solenoid driver drives them. The SDU sheet prints the coil return as J1-9 [O] for the right and J1-8 [G] for the left flipper; the "
		"playfield coil sheet prints the same colours on the other pins (`LEFT FLIPPER A3J1-9 (-G-)`, `RIGHT FLIPPER A3J1-8 (-O-)`), a connector-pin reading "
		"only, and the definition follows the SDU sheet. The upper right flipper has no drive line of its own: the playfield coil sheet joins its lower end to "
		"the right flipper's drive through a symbol labelled `E.O.S.`, so the right button and public 46 work both right flippers, and both known-working "
		"scripts' right flipper callback moves both `RightFlipper` and `RightFlipper001`. Public 46 is PinMAME's synthetic held-coil output for the right side "
		"(FLIP_SW(FLIP_L)); PinMAME also asserts public 45 for the same interval. Both outputs are button states, not measurements of any winding. Placed on "
		"the retained table's `RightFlipper` and `RightFlipper001` pivots, which its flipper callback moves."),
	47: ("PinMAME's synthetic power-winding state for the left side, asserted and released together with public 48 for the whole enabled button closure "
		"(retained gameplay and variant runs). It is not another coil and does not measure the power winding."),
	48: ("The left flipper (parts list `Flipper Left & Right (2)` J-25-500/34-4500) is a dual-winding coil hard-wired from the +43 VDC flipper supply A2J1-6 "
		"(BLU-W) through the flipper enable relay's contact to the left cabinet button; no numbered solenoid driver drives it. The SDU sheet prints the coil "
		"return as J1-9 [O] for the right and J1-8 [G] for the left flipper; the playfield coil sheet prints the same colours on the other pins (`LEFT FLIPPER "
		"A3J1-9 (-G-)`, `RIGHT FLIPPER A3J1-8 (-O-)`), a connector-pin reading only, and the definition follows the SDU sheet. Public 48 is PinMAME's "
		"synthetic held-coil output for the left side (FLIP_SW(FLIP_L)); PinMAME also asserts public 47 for the same interval. Both outputs are button states, "
		"not measurements of any winding. Placed on the retained table's `LeftFlipper` pivot, which its flipper callback moves."),
}


if __name__ == "__main__":
	unittest.main()
