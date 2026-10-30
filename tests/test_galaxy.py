"""Gates for the Stern Galaxy (1980) definition.

They lock down what was expensive to establish and cheap to lose: the lamp decoder arithmetic, the blotted connector pins and the one
corrected lamp row, the physical-to-public solenoid mapping the ROM's own test proves, the general-illumination relay, and the boundary
between what the retained runs measured and what they did not. Fixtures that restate a printed sheet are read from the committed
excerpts, not from the curator's data module: a test that checks the generator against its own input only proves the generator is
self-consistent.
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

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402
from pinmame_game_defs.conflicts import unresolved_conflicts  # noqa: E402

import curate_galaxy as curator  # noqa: E402

DEFINITION_PATH = ROOT / "machines/partial/stern/galaxy-1980.json"
SEED_PATH = ROOT / "tools/seeds/stern/galaxy-1980.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/galaxy-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/galaxy-1980.json"
EXCERPTS = ROOT / "evidence/excerpts/stern.galaxy.1980"
RUNTIME_PATH = ROOT / "evidence/runtime/stern/galaxy-diagnostics-and-gameplay.json"
MACHINE_ID = "stern.galaxy.1980"
IDENTICAL_DRIVERS = {"galaxy", "galaxyfp", "galaxyps"}
SEVEN_DIGIT_DRIVERS = {"galaxyb", "galaxyc"}
EXPECTED_MISSING = ["spatial_placement"]
OPEN_SWITCHES = {17, 25, 27, 28, 31, 32, 34}
# Public address -> the words the device label must carry, from the printed Solenoid Identification list via the ROM's test pairing.
SOLENOID_WORDS = {1: ("right", "slingshot"), 2: ("left", "slingshot"), 3: ("top", "thumper"), 4: ("drop-target", "reset"), 5: ("kicker",), 6: ("knocker",),
	7: ("lower", "right", "thumper"), 8: ("saucer",), 9: ("red",), 10: ("blue",), 11: ("out-hole",), 12: ("lower", "left", "thumper"), 13: ("yellow",),
	14: ("black",), 17: ("general", "illumination", "relay"), 18: ("coin",), 19: ("flipper", "relay")}
UNUSED_SOLENOIDS = {15, 20}
UNUSED_LAMPS = {14, 15, 29, 30, 31, 46, 47, 62}
BACKBOX_LAMPS = {13: "high score", 45: "game over", 61: "tilt", 63: "match"}
# Connector-block rows whose hand-written pin is blotted or overprinted -> the pin the lamp list and the ROM settle.
SETTLED_PINS = {("J1", 24): 5, ("J1", 20): 13, ("J2", 23): 8, ("J2", 53): 3, ("J3", 44): 19, ("J3", 38): 25}


def markdown_rows(path: Path) -> list[list[str]]:
	rows = []
	for line in path.read_text(encoding="utf-8").splitlines():
		if line.startswith("|") and not re.match(r"^\|\s*:?-+", line):
			rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
	return rows


def connector_rows() -> list[tuple[str, str, int]]:
	"""(jack, printed pin cell, SCR number) in printed order, read from the connector-label excerpt."""
	rows = []
	jack = None
	for line in (EXCERPTS / "lamp-driver-connector-labels.md").read_text(encoding="utf-8").splitlines():
		match = re.match(r"^### (J\d)$", line)
		if match:
			jack = match.group(1)
			continue
		match = re.match(r"^\| ([^|]+) \| T? ?\| Q(\d+) \|", line)
		if match and jack:
			rows.append((jack, match.group(1).strip(), int(match.group(2))))
	return rows


def decoder_table() -> dict[int, int]:
	"""Public lamp address -> SCR number, read from the decoder excerpt (public = 16k + a + 1)."""
	result: dict[int, int] = {}
	chip = None
	for line in (EXCERPTS / "lamp-driver-decoder-outputs.md").read_text(encoding="utf-8").splitlines():
		match = re.match(r"^### U(\d) \(MC14514B\)$", line)
		if match:
			chip = int(match.group(1)) - 1
			continue
		match = re.match(r"^\| S(\d+) \| \d+ \| R(\d+) \| Q(\d+) \|", line)
		if match and chip is not None:
			assert match.group(2) == match.group(3), line
			result[16 * chip + int(match.group(1)) + 1] = int(match.group(3))
	return result


def lamp_list() -> list[tuple[str, str, str, int]]:
	rows = markdown_rows(EXCERPTS / "lamp-driver-lamp-list.md")
	return [(row[0], row[1], row[2], int(row[3])) for row in rows[1:] if len(row) >= 4 and row[3].isdigit()]


class GalaxyDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		group = lambda name: {item["binding"]["device"]: item for item in cls.definition["inputs"] + cls.definition["outputs"] if item["binding"]["group"] == name}
		cls.switches = group("pinmame.input.switch")
		cls.dips = group("pinmame.input.dip")
		cls.direct = group("physical.input.direct")
		cls.solenoids = group("pinmame.output.solenoid")
		cls.lamps = group("pinmame.output.lamp")
		cls.runtime = load_json(RUNTIME_PATH)

	def test_deterministic_artifacts_match_the_curator(self) -> None:
		curator.check(ROOT)
		self.assertEqual(canonical_bytes(self.definition), SEED_PATH.read_bytes())

	def test_identity_and_driver_group(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((machine["id"], machine["name"], machine["year"], machine["ipdb_id"], machine["model_number"]), (MACHINE_ID, "Galaxy", 1980, 980, "114"))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), IDENTICAL_DRIVERS | SEVEN_DIGIT_DRIVERS)
		self.assertNotIn("clone_of", drivers["galaxy"])
		for identifier in set(drivers) - {"galaxy"}:
			self.assertEqual(drivers[identifier]["clone_of"], "galaxy")
		for identifier in IDENTICAL_DRIVERS:
			self.assertEqual(drivers[identifier]["physical_compatibility"], "identical")
		for identifier in SEVEN_DIGIT_DRIVERS:
			self.assertEqual(drivers[identifier]["physical_compatibility"], "compatible")
			starts = [item["segment_start"] for item in drivers[identifier]["display_overrides"] if item["width"] == 7]
			self.assertEqual(starts, [1, 9, 17, 25])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == MACHINE_ID}
		self.assertEqual(claimed, set(drivers))

	def test_coverage_is_partial_with_exactly_the_documented_blockers(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual(coverage["status"], "partial")
		self.assertEqual(coverage["missing"], EXPECTED_MISSING)
		self.assertFalse(unresolved_conflicts(self.definition))
		self.assertFalse((ROOT / "machines/author-ready/stern/galaxy-1980.json").exists())

	def test_every_matrix_address_is_enumerated_named_and_normally_open(self) -> None:
		self.assertEqual(set(self.switches), {-7, -6, -5, *range(1, 41), 81, 82, 83, 84})
		rows = markdown_rows(EXCERPTS / "switch-identification.md")
		printed = {int(row[0]): row[1] for row in rows if row[0].isdigit()}
		printed.update({int(row[2]): row[3] for row in rows if len(row) > 3 and row[2].isdigit()})
		self.assertEqual(set(printed), set(range(1, 41)))
		self.assertEqual({address for address, text in printed.items() if text == "OPEN"}, OPEN_SWITCHES | {33})
		for address in range(1, 41):
			item = self.switches[address]
			self.assertEqual(item["availability"], "unused" if address in OPEN_SWITCHES else "used", address)
			self.assertIs(item["normally_closed"], False, address)
		self.assertIn("out-hole", self.switches[33]["label"].lower())
		self.assertTrue(self.switches[33]["initial_active"])
		self.assertEqual({address for address in (81, 82, 83, 84) if self.switches[address]["availability"] == "unused"}, {81, 83})

	def test_switch_test_shows_every_address_as_its_own_number(self) -> None:
		note = self.runtime["runtime"]["observations"]["runs"]["switch-test"]["note"]
		pairs = re.findall(r"(\d+)->(\d+)", note)
		self.assertEqual(pairs, [(str(address), str(address)) for address in range(1, 41)])

	def test_hard_wired_inputs(self) -> None:
		self.assertEqual(set(self.direct), {1, 2, 3})
		for address in (1, 2):
			self.assertIs(self.direct[address]["normally_closed"], True)
			self.assertIn("end-of-stroke", self.direct[address]["label"].lower())
		self.assertIn("memory clear", self.direct[3]["label"].lower())

	def test_solenoid_translation_matches_the_printed_list_and_the_rom_test(self) -> None:
		printed = {int(row[0]): row[1] for row in markdown_rows(EXCERPTS / "solenoid-identification.md") if row[0].isdigit()}
		self.assertEqual(printed.get(15), "RIGHT & LEFT FLIPPERS")
		mapping = {int(key): value for key, value in self.runtime["runtime"]["observations"]["physical_service_solenoid_to_public"].items()}
		self.assertEqual(mapping, {1: 2, 2: 1, 3: 6, 4: 7, 5: 3, 6: 4, 7: 5, 8: 8, 9: 11, 10: 12, 11: 14, 12: 13, 13: 9, 14: 10, 15: 19, 16: 15, 17: 17, 18: 20, 19: 18})
		for physical, public in mapping.items():
			item = self.solenoids[public]
			self.assertIn({"namespace": "manual.self-test", "value": str(physical)}, item["aliases"])
			self.assertEqual(item["wiring"]["driver_transistor"], f"Q{physical}")
			if printed.get(physical) == "OPEN":
				self.assertIn(public, UNUSED_SOLENOIDS | {17}, public)
		for public, words in SOLENOID_WORDS.items():
			label = self.solenoids[public]["label"].lower()
			self.assertTrue(all(word in label for word in words), (public, label))
			self.assertEqual(self.solenoids[public]["availability"], "used")
		for public in UNUSED_SOLENOIDS:
			self.assertEqual(self.solenoids[public]["availability"], "unused", public)
		self.assertNotIn(16, self.solenoids)

	def test_general_illumination_relay(self) -> None:
		relay = self.solenoids[17]
		self.assertEqual(relay["kind"], "relay")
		self.assertIn("GEN. ILLUM. RELAY", relay["physical"]["notes"])
		self.assertEqual(relay["wiring"]["drive_connection"], "A3J5-7")
		relationships = [item for item in self.definition["relationships"] if item["source"] == relay["id"]]
		self.assertEqual([(item["kind"], item["destination"]) for item in relationships], [("inverted", "gi.general-illumination")])
		self.assertIn("J2 pin 15", self.solenoids[20]["physical"]["notes"])

	def test_lamp_addresses_follow_the_decoder_and_the_connector_table(self) -> None:
		decoder = decoder_table()
		self.assertEqual(set(decoder), {*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)})
		self.assertEqual(sorted(decoder.values()), list(range(1, 61)))
		connectors: dict[tuple[str, int], int] = {}
		settled = dict(SETTLED_PINS)
		for jack, cell, q in connector_rows():
			if (jack, q) in settled:
				connectors[(jack, settled.pop((jack, q)))] = q
			elif cell.isdigit() and (jack, int(cell)) not in connectors:
				connectors[(jack, int(cell))] = q
		self.assertFalse(settled)
		self.assertEqual(connectors[("J1", 14)], 9)
		q_to_public = {q: public for public, q in decoder.items()}
		rows = lamp_list()
		self.assertEqual(len(rows), 53)
		listed: dict[int, list[str]] = {}
		for description, wire, jack, pin in rows:
			if description == "SPOT No":
				self.assertEqual((jack, pin), ("J1", 8))
				jack, pin = "J2", 8
			public = q_to_public[connectors[(jack, pin)]]
			listed.setdefault(public, []).append(description)
			self.assertIn(f"A5{jack}-{pin}", self.lamps[public]["wiring"]["drive_connection"], description)
		self.assertEqual(len(listed[11]), 2)
		self.assertEqual(listed[11][0], "SAME PLAYER SHOOTS AGAIN")
		self.assertTrue(all(len(names) == 1 for public, names in listed.items() if public != 11))
		self.assertEqual(self.lamps[27]["wiring"]["drive_connection"], "A5J2-8")
		self.assertEqual(set(self.lamps), set(decoder))
		self.assertEqual(set(decoder) - set(listed), UNUSED_LAMPS)
		for public, q in decoder.items():
			self.assertEqual(self.lamps[public]["wiring"]["driver_transistor"], f"Q{q}")

	def test_lamp_availability_and_backbox_lamps(self) -> None:
		for public, words in BACKBOX_LAMPS.items():
			self.assertIn(words, self.lamps[public]["label"].lower())
			self.assertEqual(self.lamps[public]["spatial"]["reason"], "cabinet_or_service")
		for public in UNUSED_LAMPS:
			self.assertEqual(self.lamps[public]["availability"], "unused")
		outside = set(self.runtime["runtime"]["observations"]["lamp_addresses_driven_outside_self_test"])
		self.assertFalse(outside & UNUSED_LAMPS)
		self.assertTrue({11, 27, 34, 35, 40} <= outside)

	def test_option_switches(self) -> None:
		self.assertEqual(set(self.dips), set(range(1, 33)))

	def test_mechanisms_name_existing_devices_and_each_actuator_once(self) -> None:
		devices = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		actuators = []
		for mechanism in self.definition["mechanisms"]:
			for reference in mechanism["actuators"] + mechanism["sensors"]:
				self.assertIn(reference, devices, mechanism["id"])
			actuators += mechanism["actuators"]
		self.assertEqual(len(actuators), len(set(actuators)))
		for relationship in self.definition["relationships"]:
			self.assertIn(relationship["source"], devices)
			self.assertIn(relationship["destination"], devices)

	def test_displays_match_the_pinned_dispst6_layout(self) -> None:
		layout = [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]]
		self.assertEqual(layout, [(0, 2, 6), (1, 10, 6), (2, 18, 6), (3, 26, 6), (4, 35, 2), (5, 38, 2)])

	def test_excerpts_are_pinned_and_present(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"])
		self.assertEqual(count, len(list(EXCERPTS.glob("*.md"))))
		self.assertEqual(len(list(EXCERPTS.glob("*.webp"))), 9)

	def test_spatial_report_states_the_blockers(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(report["readiness"]["missing"], EXPECTED_MISSING)
		self.assertEqual([item["id"] for item in report["unplaced_records"]], ["gi.general-illumination"])

	def test_every_playfield_device_is_placed_inside_the_playfield(self) -> None:
		for collection in ("inputs", "outputs"):
			for item in self.definition[collection]:
				spatial = item.get("spatial")
				if item["id"] == "gi.general-illumination":
					self.assertIsNone(spatial)
					continue
				self.assertIsNotNone(spatial, item["id"])
				for placement in spatial.get("placements", []):
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
					self.assertEqual(placement["provenance"]["status"], "observed", placement["id"])
		self.assertEqual(len(self.lamps[27]["spatial"]["placements"]), 2)
		left, right = self.solenoids[48]["spatial"]["placements"], self.solenoids[46]["spatial"]["placements"]
		self.assertTrue(all(placement["x"] < 0.5 for placement in left) and all(placement["x"] > 0.5 for placement in right))

	def test_knowledge_note_states_the_translations(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("1->2, 2->1, 3->6", "GEN. ILLUM. RELAY", "16 * k + a + 1", "public 14, 15, 29, 30, 31, 46, 47 and 62"):
			self.assertIn(phrase, text)

	def test_no_other_machines_leak_into_the_artifacts(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		forbidden = {machine["id"] for machine in catalog["machines"]} - {MACHINE_ID}
		# Short names of every other Stern driver, the family a copied sibling record would come from (other makers' names include plain words).
		forbidden |= {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") != MACHINE_ID and str(driver.get("machine_id", "")).startswith("stern.")}
		forbidden.discard("stars")  # a Stern title and a plain word: the playfield has star roll-overs
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		tokens = set()
		for text in texts:
			tokens |= set(re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]", text))
		self.assertFalse(tokens & forbidden, sorted(tokens & forbidden)[:10])

	def test_sources_are_complete_and_scripts_are_pinned(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		for identifier in (curator.MANUAL_SOURCE, curator.IPDB_SOURCE, curator.SCRIPT_SOURCE, curator.TABLE_SOURCE, curator.TABLE_SCRIPT_SOURCE, *curator.RUN_SOURCES.values()):
			self.assertIn(identifier, sources)
		self.assertEqual(sources[curator.SCRIPT_SOURCE]["sha256"], "ac7e8751a2f26307a8d2ddd9a74c64af944b32aef8f2ddf896c1eab13d2856e4")
		self.assertEqual(sources[curator.TABLE_SCRIPT_SOURCE]["sha256"], sources[curator.SCRIPT_SOURCE]["sha256"])
		runs = {run["name"]: run["sha256"] for run in self.runtime["runtime"]["raw_runs"]}
		for name, identifier in curator.RUN_SOURCES.items():
			self.assertEqual(sources[identifier]["sha256"], runs[name])


class GalaxyRetainedEvidenceTests(unittest.TestCase):
	"""Exact retained artifacts, checked only when the external roots are configured."""

	def test_harness_runs_reproduce_the_runtime_summary(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		import summarize_galaxy_runtime as summary
		self.assertEqual(canonical_bytes(summary.build(Path(root) / "galaxy-1980" / "harness")), RUNTIME_PATH.read_bytes())

	def test_retained_table_extraction_and_coordinates(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not set")
		import galaxy_data as data
		from build_external_evidence_manifest import check_manifest
		from pinmame_game_defs.spatial import _item_point
		folder = Path(root) / curator.TABLE_RELATIVE
		self.assertEqual(hashlib.sha256((folder / curator.TABLE_FILENAME).read_bytes()).hexdigest(), curator.TABLE_SHA256)
		extraction = Path(root) / curator.EXTRACTION_RELATIVE
		self.assertEqual(check_manifest(extraction, "galaxy"), curator.EXTRACTION_MANIFEST_SHA256)
		self.assertEqual(hashlib.sha256((extraction / "script.vbs").read_bytes()).hexdigest(), curator.SCRIPT_SHA256)
		bounds = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
		self.assertEqual((bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]), (0.0, 0.0, data.TABLE_WIDTH, data.TABLE_HEIGHT))
		for name, (item_type, x, y, file) in data.OBJECTS.items():
			document = json.loads((extraction / "gameitems" / file).read_text(encoding="utf-8"))
			self.assertEqual(next(iter(document)), item_type, name)
			value = document[item_type]
			self.assertEqual(value["name"], name)
			self.assertEqual(_item_point(item_type, value)[:2], (x, y), name)

	def test_retained_manual_matches_its_pinned_hash(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("PINMAME_MANUALS_ROOT is not set")
		path = Path(root) / "by-machine" / MACHINE_ID / "ipdb" / curator.MANUAL_PDF
		self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), curator.MANUAL_SHA256)


if __name__ == "__main__":
	unittest.main()
