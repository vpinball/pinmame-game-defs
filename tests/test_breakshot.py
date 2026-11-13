from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/capcom/breakshot-1996.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/capcom/breakshot-1996.json"
SEED_PATH = ROOT / "tools/seeds/capcom/breakshot-1996.json"
CALLOUT_PATH = ROOT / "tools/seeds/capcom/breakshot-1996-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/capcom/breakshot-1996.json"
EXCERPTS = ROOT / "evidence/excerpts/capcom.breakshot.1996"
DRIVER_IDS = ["bsv103", "bsv102", "bsb105", "bsv100r", "bsv102r"]
POOL_PLAYER_PATH = ROOT / "machines/partial/illinois-pinball/pool-player-2000.json"
POOL_PLAYER_EXCERPTS = ROOT / "evidence/excerpts/illinois-pinball.pool-player.2000"


def _load(name: str, path: Path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[name] = module
	spec.loader.exec_module(module)
	return module


CURATOR = _load("curate_breakshot", ROOT / "tools/curate_breakshot.py")
RUNTIME = _load("build_breakshot_runtime_evidence", ROOT / "tools/build_breakshot_runtime_evidence.py")
import drawing_callouts  # noqa: E402  (the curator put tools/ on sys.path)


def excerpt_tables(name: str) -> list[list[list[str]]]:
	"""Every markdown table in an excerpt, as body rows (header and rule removed)."""
	found: list[list[list[str]]] = []
	previous = False
	for line in (EXCERPTS / name).read_text(encoding="utf-8").splitlines():
		is_table = line.startswith("| ")
		if is_table and not previous:
			found.append([])
		if is_table and not line.startswith("| ---"):
			found[-1].append([cell.strip() for cell in line.strip("|").split("|")])
		previous = is_table
	return [table[1:] for table in found]


class BreakshotDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.devices = {(d["binding"]["group"].rsplit(".", 1)[1], d["binding"]["device"]): d for d in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.devices[(group, address)]

	def test_identity_coverage_and_no_author_ready_copy(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("capcom.breakshot.1996", "Breakshot", "Capcom", 1996, 3784, "G43oE-M0ok5"),
		                 (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		dimensions = self.definition["coverage"]["dimensions"]
		self.assertEqual("observed", dimensions["spatial_placement"])
		self.assertEqual({"validated"}, {state for name, state in dimensions.items() if name != "spatial_placement"})
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.capcom", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_unplaced_gi_sockets_block_promotion(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(("pinmame-spatial-blockers", "partial"), (report["format"], report["status"]))
		self.assertEqual(1, len(report["blockers"]))
		blocker = report["blockers"][0]
		for socket in CURATOR.GI_DRAWING_ONLY:
			self.assertIn(socket, blocker)
		self.assertRegex(blocker, r"Resolution path: [^.]+\.$")
		self.assertTrue(report["promotion_decision"].startswith("partial: seven fixed G.I. sockets"))
		# The record's coverage follows the sockets: any socket without a checked position keeps it partial,
		# and none left stops the build so that a promotion is made deliberately.
		self.assertEqual(self.definition["coverage"], CURATOR.coverage(["65A"]))
		with self.assertRaises(RuntimeError):
			CURATOR.coverage([])
		promoted = json.loads(json.dumps(self.definition))
		promoted["coverage"] = {"status": "author_ready", "missing": [], "dimensions": {}}
		with self.assertRaises(RuntimeError):
			CURATOR.build_spatial_report(promoted)

	def test_every_breakshot_driver_is_claimed_once_by_this_record(self) -> None:
		self.assertEqual(DRIVER_IDS, [driver["id"] for driver in self.definition["drivers"]])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = [driver["id"] for driver in catalog["drivers"] if driver.get("definition") == DEFINITION_PATH.relative_to(ROOT).as_posix()]
		self.assertEqual(sorted(DRIVER_IDS), sorted(claimed))
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["bsv103"])
		for driver_id in DRIVER_IDS[1:]:
			self.assertEqual("bsv103", by_id[driver_id]["clone_of"])
		self.assertEqual({"identical"}, {by_id[d]["physical_compatibility"] for d in ("bsv103", "bsv102", "bsb105")})
		self.assertEqual({"compatible"}, {by_id[d]["physical_compatibility"] for d in ("bsv100r", "bsv102r")})
		self.assertNotIn("pp100", by_id)
		pool_player = [driver for driver in catalog["drivers"] if driver["id"] == "pp100"]
		self.assertEqual([POOL_PLAYER_PATH.relative_to(ROOT).as_posix()], [driver.get("definition") for driver in pool_player])

	def test_the_optional_dispensers_are_documented_not_denied(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual_excerpts = {excerpt["path"] for excerpt in sources[CURATOR.MANUAL_SOURCE]["excerpts"]}
		self.assertIn("evidence/excerpts/capcom.breakshot.1996/redemption-and-dispensers.md", manual_excerpts)
		self.assertIn("PDF 145", sources[CURATOR.MANUAL_SOURCE]["locator"])
		text = json.dumps(self.definition, ensure_ascii=False)
		for denial in ("no ticket hardware", "show no dispenser", "show no dispenser on this machine"):
			self.assertNotIn(denial, text)
		for address in (32, 40, 64, 72):
			device = self.device("switch", address)
			self.assertEqual("unused", device["availability"], address)
			self.assertIn("optional ticket dispenser", device["physical"]["notes"], address)
			self.assertIn("B1-16", device["physical"]["notes"], address)
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in ("bsv100r", "bsv102r"):
			self.assertIn("ticket or token dispenser", by_id[driver_id]["variant_notes"], driver_id)
		excerpt = (EXCERPTS / "redemption-and-dispensers.md").read_text(encoding="utf-8")
		for literal in ("B1-16+ TICKET DISPENSER", "B1-17+ TOKEN DISPENSER", "C1-09 : TICKET DISPENSER TEST",
		                "C1-10 : TOKEN DISPENSER TEST", "DELTRONICS", "MODEL 1275", "CTD10", "`TO CPU J3`",
		                "TICKETMETER 1 BLU/RED", "MOTOR_DRV BLU/BRN", "`TOKEN DRIVER PCB`"):
			self.assertIn(literal, excerpt)
		source_excerpt = (EXCERPTS / "pinmame-source.md").read_text(encoding="utf-8")
		self.assertIn("//PA0   - J3 - Pin 7 - Token/Coin Meter/Printer Interface Board(Unknown purpose)", source_excerpt)
		self.assertIn("//PB6 OR IRQ5  - J3 - Pin 11", source_excerpt)

	def test_fixed_gi_sockets_are_placed_on_checked_table_lights_or_the_drawing(self) -> None:
		expected = [f"{string}{letter}" for string, (_, count) in sorted(CURATOR.GI_STRINGS.items()) for letter in CURATOR.GI_LETTERS[:count]]
		self.assertEqual(54, len(expected))
		inventory = load_json(SPATIAL_REPORT_PATH)["uncontrolled_lighting"]
		sockets = inventory["sockets"]
		self.assertEqual(expected, [entry["socket"] for entry in sockets])
		self.assertEqual({"sockets": 54, "validated": 47, "observed": 7}, inventory["counts"])
		self.assertEqual(0.07, inventory["limit"])
		lights = [entry["coordinate_source"] for entry in sockets if entry["status"] == "validated"]
		self.assertEqual(len(lights), len(set(lights)))
		self.assertEqual({f"Light.{name}" for name in CURATOR.GI_LIGHTS}, set(lights))
		self.assertNotIn("gi014", CURATOR.GI_LIGHTS)
		for entry in sockets:
			self.assertEqual(CURATOR.GI_STRINGS[entry["socket"][:2]][0], entry["wire"], entry["socket"])
			self.assertTrue(0.0 <= entry["x"] <= 1.0 and 0.0 <= entry["y"] <= 1.0, entry["socket"])
			if entry["status"] == "validated":
				self.assertEqual(CURATOR.GI_LIGHTS[entry["coordinate_source"].removeprefix("Light.")], (entry["x"], entry["y"]))
				self.assertLessEqual(max(entry["control_offset"], entry["callout_offset"]), 0.07, entry["socket"])
			else:
				self.assertEqual("observed", entry["status"], entry["socket"])
				self.assertEqual(entry["drawing_point"], [entry["x"], entry["y"]], entry["socket"])
		self.assertEqual(list(CURATOR.GI_DRAWING_ONLY), [entry["socket"] for entry in sockets if entry["status"] == "observed"])
		self.assertEqual("69", inventory["backbox"]["socket"])
		# The note's table repeats the report's coordinates, and its prose names the same counts.
		text = (ROOT / self.definition["knowledge"]["path"]).read_text(encoding="utf-8")
		rows = {line.split("|")[1].strip(): [cell.strip() for cell in line.strip("|").split("|")] for line in text.splitlines() if re.match(r"\| 6[5-8][A-Z] \|", line)}
		self.assertEqual(expected, list(rows))
		for entry in sockets:
			self.assertEqual([f"{entry['x']:.3f}", f"{entry['y']:.3f}"], rows[entry["socket"]][2:4], entry["socket"])
		prose = " ".join(text.split())
		self.assertIn("all 47 pairs land within the 0.07 callout limit", prose)
		self.assertIn("Seven sockets have no table light", prose)
		self.assertNotRegex(text, r"\{[A-Z_]+\}")
		self.assertIn("front edge", (EXCERPTS / "lamp-locations.md").read_text(encoding="utf-8"))
		self.assertIn("Those seven sockets are why the record is `partial`", prose)
		self.assertIn("`uncontrolled_lighting` places them", (ROOT / "reports/spatial/capcom/breakshot-1996.md").read_text(encoding="utf-8"))

	def test_a_changed_gi_pairing_is_refused(self) -> None:
		original = dict(CURATOR.GI_LIGHTS)
		try:
			del CURATOR.GI_LIGHTS["gi033"]
			with self.assertRaises(RuntimeError):
				CURATOR.gi_sockets(self.definition)
			CURATOR.GI_LIGHTS.clear()
			CURATOR.GI_LIGHTS.update(original)
			CURATOR.GI_LIGHTS["gi999"] = (0.5, 0.95)
			with self.assertRaises(RuntimeError):
				CURATOR.gi_sockets(self.definition)
		finally:
			CURATOR.GI_LIGHTS.clear()
			CURATOR.GI_LIGHTS.update(original)
		CURATOR.gi_sockets(self.definition)

	def test_address_spaces_are_fully_enumerated(self) -> None:
		def addresses(group: str) -> set[int]:
			return {address for kind, address in self.devices if kind == group}

		self.assertEqual(set(range(1, 97)), addresses("switch"))
		self.assertEqual(set(range(1, 52)), addresses("solenoid"))
		self.assertEqual(set(range(1, 73)), addresses("lamp"))

	def test_switch_board_less_column_layout(self) -> None:
		for address in range(9, 17):
			device = self.device("switch", address)
			self.assertEqual(("virtual", "unused"), (device["kind"], device["availability"]), address)
		self.assertIn("29 SLAM TILT", self.device("switch", 9)["physical"]["notes"])
		self.assertEqual(["cabinet.slam-tilt"], self.device("switch", 29)["roles"])
		self.assertEqual("SW00121", self.device("switch", 29)["physical"]["part_number"])
		self.assertEqual(["flipper.upper.right.button"], self.device("switch", 21)["roles"])
		self.assertEqual("tilt", self.device("switch", 30)["physical"]["switch_type"])

	def test_opto_set_is_capinvsw_and_the_manual_and_the_rom_grid(self) -> None:
		optos = {address for (group, address), d in self.devices.items() if group == "switch" and d.get("physical", {}).get("switch_type") == "opto"}
		self.assertEqual({36, 37, 38, 53, 54, 65}, optos)
		manual_optos = {int(row[0]) for table in excerpt_tables("switch-locations.md") for row in table if row and "(OPTO)" in row[1]}
		self.assertEqual(optos, manual_optos)
		for (group, address), d in self.devices.items():
			if group == "switch" and d["availability"] == "used" and d["kind"] == "switch":
				self.assertIs(address in optos, d["normally_closed"], address)

	def test_unused_matrix_positions_match_the_manual(self) -> None:
		used = {address for (group, address), d in self.devices.items() if group == "switch" and 17 <= address <= 80 and d["availability"] == "used"}
		self.assertEqual(set(range(17, 81)) - set(CURATOR.UNUSED_MATRIX), used)
		self.assertEqual({21, 29, 30} | set(range(33, 39)) | set(range(41, 48)) | set(range(49, 56)) | set(range(57, 64))
		                 | set(range(65, 72)) | set(range(73, 80)), used)

	def test_flipper_column_and_host_inputs(self) -> None:
		self.assertEqual("used", self.device("switch", 82)["availability"])
		self.assertEqual("used", self.device("switch", 84)["availability"])
		for address in (81, 83, 85, 86, 87, 88):
			self.assertEqual("unused", self.device("switch", address)["availability"], address)
		self.assertIn("end-of-stroke", self.device("switch", 81)["physical"]["notes"])
		self.assertIn("fired nothing", self.device("switch", 81)["physical"]["notes"])

	def test_script_defects_are_stated_not_copied(self) -> None:
		placement = lambda address: (lambda p: (p["x"], p["y"]))(self.device("switch", address)["spatial"]["placements"][0])
		self.assertLess(placement(41)[0], 0.5)
		self.assertGreater(placement(42)[0], 0.5)
		self.assertLess(placement(57)[0], placement(59)[0])
		self.assertGreater(placement(58)[1], placement(57)[1])
		self.assertEqual("unused", self.device("switch", 48)["availability"])
		self.assertIn("crossed", self.device("switch", 41)["physical"]["notes"])
		self.assertIn("one lower", self.device("switch", 49)["physical"]["notes"])

	def test_solenoids_follow_the_rom_test_and_manual(self) -> None:
		self.assertEqual({17, 18, 19, 20, 21, 22, 23, 24, 27}, {a for (g, a), d in self.devices.items() if g == "solenoid" and a <= 32 and d["availability"] == "unused"})
		self.assertEqual("flasher", self.device("solenoid", 28)["kind"])
		self.assertEqual(2, self.device("solenoid", 28)["physical"]["quantity"])
		self.assertEqual(2, len(self.device("solenoid", 28)["spatial"]["placements"]))
		self.assertEqual(["cabinet.knocker"], self.device("solenoid", 3)["roles"])
		for address, (_label, _kind, part, _rom, wire, connection, power, volts) in CURATOR.SOLENOIDS.items():
			wiring = self.device("solenoid", address)["wiring"]
			self.assertEqual((wire, connection, power, volts), (wiring["control_wire"], wiring["control_connection"], wiring["power_wire"], wiring["nominal_voltage_v"]), address)
			self.assertEqual(part, self.device("solenoid", address)["physical"]["part_number"], address)
		rom_rows = {int(row[0]): row[1] for row in excerpt_tables("service-tests.md")[1]}
		for address, (_label, _kind, _part, rom_name, wire, connection, power, volts) in CURATOR.SOLENOIDS.items():
			self.assertEqual(f"S{address:02d} - {rom_name} / {wire} {connection} / {power} PWR {volts}V", rom_rows[address], address)

	def test_flipper_mirrors_follow_the_pinned_source(self) -> None:
		used = {a for (g, a), d in self.devices.items() if g == "solenoid" and a > 32 and d["availability"] == "used"}
		self.assertEqual({33, 34, 45, 46, 47, 48, 51}, used)
		fired = {int(row[0]): row[2] for row in excerpt_tables("service-tests.md")[1]}
		self.assertEqual("9, 47, 48", fired[9])
		self.assertEqual("10, 45, 46", fired[10])
		self.assertEqual("11, 33, 34", fired[11])

	def test_lamps_follow_the_rom_test_with_the_sheet_disagreement_disclosed(self) -> None:
		rom_rows = {int(row[0]): row[1] for row in excerpt_tables("service-tests.md")[2]}
		for address in range(1, 65):
			device = self.device("lamp", address)
			if address == 2:
				self.assertEqual("unused", device["availability"])
				continue
			wiring = device["wiring"]
			column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
			expected = f"{column}{row}B - {CURATOR.ROM_LAMP_TEST[address]} / COL-SM{column}B {wiring['drive_connection']} {wiring['drive_wire']} / ROW-M{row}B {wiring['return_connection']} {wiring['return_wire']}"
			self.assertEqual(expected, rom_rows[address], address)
			self.assertIn(f"Column {column} {CURATOR.SHEET_COLUMNS[column]} and Row {row} {CURATOR.SHEET_ROWS[row]}", device["physical"]["notes"], address)
		self.assertEqual("8 Ball Option", self.device("lamp", 23)["label"])
		jackpot = self.device("lamp", 11)
		self.assertIn("Jackpot (two)", jackpot["physical"]["notes"])
		self.assertEqual(2, jackpot["physical"]["quantity"])
		placements = jackpot["spatial"]["placements"]
		self.assertEqual(["lamp.matrix-11.emitter.1", "lamp.matrix-11.emitter.2"], [p["id"] for p in placements])
		self.assertEqual((placements[0]["x"], placements[0]["y"]), (placements[1]["x"], placements[1]["y"]))
		self.assertIn(CURATOR.CALLOUT_SOURCE, placements[0]["provenance"]["source_refs"])
		self.assertNotIn(CURATOR.CALLOUT_SOURCE, placements[1]["provenance"]["source_refs"])
		self.assertIn({"group": "pinmame.output.lamp", "address": 11, "reason": CURATOR.JACKPOT_PROJECTION}, load_json(SPATIAL_REPORT_PATH)["projections"])
		for address in (65, 66):
			self.assertEqual(("used", "not_applicable"), (self.device("lamp", address)["availability"], self.device("lamp", address)["spatial"]["status"]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {d["id"] for d in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"]) <= ids, mechanism["id"])
			self.assertTrue(set(mechanism["sensors"]) <= ids, mechanism["id"])
		used_coils = {d["id"] for (g, a), d in self.devices.items() if g == "solenoid" and a <= 32 and d["availability"] == "used" and d["kind"] == "coil"}
		actuated = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		# Slingshots, flippers, bumpers and the knocker are ordinary devices, not mechanisms.
		self.assertEqual(used_coils - actuated, {CURATOR.solenoid_id(a) for a in (3, 4, 5, 9, 10, 11, 29, 30, 31)})
		self.assertEqual([], self.definition["relationships"])
		self.assertEqual([], self.definition["conflicts"])

	def test_every_placement_is_validated_unique_and_in_range(self) -> None:
		seen = set()
		for d in self.definition["inputs"] + self.definition["outputs"]:
			spatial = d["spatial"]
			if spatial["status"] == "not_applicable":
				continue
			self.assertEqual("validated", spatial["status"], d["id"])
			for placement in spatial["placements"]:
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				self.assertEqual("validated", placement["provenance"]["status"], placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertTrue(0 <= value <= 1, placement["id"])
					self.assertLessEqual(len(repr(value).split(".")[-1]), 6, placement["id"])
		self.assertEqual(len(seen), load_json(SPATIAL_REPORT_PATH)["placement_count"])

	def test_drawing_callout_check_decides_every_located_placement(self) -> None:
		seed = load_json(CALLOUT_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition))
		self.assertEqual(120, len(decisions["placements"]))
		self.assertTrue(all(decision["agrees"] for decision in decisions["placements"].values()))
		located = set(drawing_callouts.placements_of(self.definition))
		self.assertEqual(located, set(seed["checks"]) | set(seed["excluded_checks"]))
		self.assertEqual({"switch.matrix-35.sensor", "switch.matrix-36.sensor", "switch.matrix-37.sensor", "switch.matrix-38.sensor",
		                  "device.outhole.effect", "device.trough.effect", "lamp.matrix-11.emitter.2"}, set(seed["excluded_checks"]))
		self.assertEqual({"page": "pdf-74", "label": "11"}, seed["checks"]["lamp.matrix-11.emitter.1"])
		for pid in seed["checks"]:
			self.assertIn(CURATOR.CALLOUT_SOURCE, self.placement(pid)["provenance"]["source_refs"], pid)
		report = load_json(SPATIAL_REPORT_PATH)["drawing_callout_check"]
		self.assertEqual((120, 120, {}), (report["checked"], report["validated"], report["not_validated"]))
		self.assertEqual(hashlib.sha256(CALLOUT_PATH.read_bytes()).hexdigest(), report["seed_sha256"])

	def placement(self, pid: str) -> dict:
		for d in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (d.get("spatial") or {}).get("placements") or []:
				if placement["id"] == pid:
					return placement
		raise KeyError(pid)

	def test_excerpts_and_sources_are_pinned(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotRegex(value.lower(), r"\b[a-z]:[\\/]", source["id"])
			if source["kind"] in {"vpx_script", "manual"}:
				self.assertTrue(source.get("license") and source.get("attribution"), source["id"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertTrue(sources[CURATOR.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(CURATOR.MANUAL_SHA256, sources[CURATOR.MANUAL_SOURCE]["sha256"])
		self.assertEqual(hashlib.sha256((ROOT / "evidence/runtime/capcom/breakshot-service-diagnostics.json").read_bytes()).hexdigest(), sources[CURATOR.SERVICE_SOURCE]["sha256"])

	def test_runtime_seed_excerpt_and_evidence_agree(self) -> None:
		RUNTIME.check_seed_against_evidence()
		RUNTIME.check_service_excerpt()
		scenario = load_json(ROOT / "tools/harness-scenarios/capcom/bsv103-gameplay.json")
		self.assertTrue(any("lower-right end-of-stroke bit" in action.get("label", "") for action in scenario["actions"]))
		for path in sorted((ROOT / "tools/harness-scenarios/capcom").glob("bsv103-*.json")):
			self.assertNotIn(b"\r", path.read_bytes(), path.name)

	def test_release_edges_are_not_reported_as_firings(self) -> None:
		gameplay = {item["step"]: item for item in RUNTIME.load_seed()["gameplay"]}
		release_only = {step: (item["fired"], item["released"]) for step, item in gameplay.items() if item["released"]}
		self.assertEqual({
			"the served ball leaves the trough eject position (36 clears)": ([], [2]),
			"release the left flipper button bit": ([], [9, 47, 48]),
			"release the right flipper button bit": ([], [10, 45, 46]),
			"release public 21": ([], [11, 33, 34]),
		}, release_only)
		rows = {row[0]: row for row in excerpt_tables("service-tests.md")[3]}
		self.assertEqual(["-", "2"], rows["the served ball leaves the trough eject position (36 clears)"][2:4])
		trough = self.device("solenoid", 2)["physical"]["notes"]
		self.assertIn("pulsing it five times while trough position 1 (36) stayed closed", trough)
		self.assertIn("released 2 when the served ball left position 1 and did not fire it again", trough)
		for address in (7, 13):
			self.assertIn("run served no further ball", self.device("solenoid", address)["physical"]["notes"])
		banks = {m["id"]: m for m in self.definition["mechanisms"]}
		for identifier in ("mechanism.right-drop-bank", "mechanism.left-drop-bank"):
			text = json.dumps(banks[identifier], ensure_ascii=False)
			self.assertNotIn("next ball was served", text)
			self.assertNotIn("18,000", text)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		first = canonical_bytes(CURATOR.build())
		self.assertEqual(first, canonical_bytes(CURATOR.build()))
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())
		self.assertEqual(canonical_bytes(CURATOR.build_spatial_report(CURATOR.build())), SPATIAL_REPORT_PATH.read_bytes())

	def test_curator_check_passes_twice_and_refuses_drift(self) -> None:
		CURATOR.check()
		CURATOR.check()
		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Breakshot", b"Breakshoe", 1))
			with self.assertRaises(RuntimeError):
				CURATOR.check()
		finally:
			DEFINITION_PATH.write_bytes(original)
		CURATOR.check()

	def test_curator_requires_an_explicit_mode(self) -> None:
		argv = sys.argv
		sys.argv = ["curate_breakshot.py"]
		try:
			with self.assertRaises(SystemExit):
				CURATOR.main()
		finally:
			sys.argv = argv

	def test_knowledge_note_carries_the_callout_result(self) -> None:
		text = (ROOT / self.definition["knowledge"]["path"]).read_text(encoding="utf-8")
		self.assertNotIn("{CALLOUT_CHECK}", text)
		self.assertRegex(text, r"check 120 table placements and validate 120")
		self.assertNotIn("\r", text)


class PoolPlayerRecordTests(unittest.TestCase):
	"""pp100 is Illinois Pinball's Pool Player, split from Breakshot as its own partial conversion."""

	@classmethod
	def setUpClass(cls) -> None:
		cls.record = load_json(POOL_PLAYER_PATH)

	def test_identity_and_fail_closed_coverage(self) -> None:
		machine = self.record["machine"]
		self.assertEqual(("illinois-pinball.pool-player.2000", "Pool Player", "Illinois Pinball", 2000, 4495, "physical_conversion"),
		                 (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["kind"]))
		self.assertNotIn("opdb_id", machine)
		coverage = self.record["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertIn("identity", coverage["missing"])
		self.assertIn("variant_differences", coverage["missing"])
		self.assertNotIn("driver_mapping", coverage["missing"])
		self.assertEqual(([], [], [], []), (self.record["inputs"], self.record["outputs"], self.record["displays"], self.record["mechanisms"]))
		self.assertEqual("pinmame.capcom", self.record["controller"]["platform"])

	def test_its_one_driver_is_not_claimed_compatible(self) -> None:
		self.assertEqual(["pp100"], [driver["id"] for driver in self.record["drivers"]])
		driver = self.record["drivers"][0]
		self.assertEqual(("bsv103", "unknown"), (driver["clone_of"], driver["physical_compatibility"]))
		self.assertIn("automatic ball launchers", driver["variant_notes"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claimed = [d["id"] for d in catalog["drivers"] if d.get("definition") == POOL_PLAYER_PATH.relative_to(ROOT).as_posix()]
		self.assertEqual(["pp100"], claimed)

	def test_sources_and_excerpts_are_pinned(self) -> None:
		sources = {source["id"]: source for source in self.record["sources"]}
		self.assertEqual({CURATOR.CATALOG_SOURCE, CURATOR.CORE_SOURCE, CURATOR.POOL_PLAYER_IPDB_SOURCE,
		                  CURATOR.POOL_PLAYER_PINSIDE_SOURCE, CURATOR.POOL_PLAYER_NEWS_SOURCE}, set(sources))
		for source in self.record["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertTrue(excerpt["path"].startswith(POOL_PLAYER_EXCERPTS.relative_to(ROOT).as_posix() + "/"), excerpt["id"])
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotRegex(value.lower(), r"\b[a-z]:[\\/]", source["id"])
		self.assertEqual("426bb0c7eb99b4c419c2fca8dea02cbdf8b705671ba959bf9f9268bd3b7dc143", sources[CURATOR.POOL_PLAYER_IPDB_SOURCE]["sha256"])
		identity = (POOL_PLAYER_EXCERPTS / "identity.md").read_text(encoding="utf-8")
		self.assertIn("`Pool Player / IPD No. 4495 / 2000 / 4 Players`", identity)
		self.assertIn("`Conversion kit`", identity)
		source_excerpt = (POOL_PLAYER_EXCERPTS / "pinmame-source.md").read_text(encoding="utf-8")
		self.assertIn('CORE_CLONEDEFNV(pp100,bsv103,"Pool Player (1.0)",2000,"Illinois Pinball",cc1,0)', source_excerpt)

	def test_curator_writes_and_checks_the_record(self) -> None:
		self.assertEqual(canonical_bytes(CURATOR.build_pool_player()), POOL_PLAYER_PATH.read_bytes())
		knowledge = (ROOT / self.record["knowledge"]["path"]).read_text(encoding="utf-8")
		self.assertIn("## What a curator must establish next", knowledge)
		original = POOL_PLAYER_PATH.read_bytes()
		try:
			POOL_PLAYER_PATH.write_bytes(original.replace(b'"unknown"', b'"compatible"', 1))
			with self.assertRaises(RuntimeError):
				CURATOR.check()
		finally:
			POOL_PLAYER_PATH.write_bytes(original)
		CURATOR.check()


class BreakshotFrameCheckTests(unittest.TestCase):
	"""The runtime builder hashes each cited DMD frame from its retained image, not from run.json."""

	LAYOUT = {"width": 4, "height": 2, "depth": 2, "type": 14}

	def snapshot(self, run_dir: Path, stored: bytes, digest_of: bytes) -> dict:
		(run_dir / "dmd").mkdir(exist_ok=True)
		(run_dir / "dmd" / "000-frame-display-0.pgm").write_bytes(b"P5\n4 2\n255\n" + stored)
		display = {"artifact": "E:\\elsewhere\\dmd\\000-frame-display-0.pgm", "layout": self.LAYOUT,
		           "pixel_sha256": hashlib.sha256(digest_of).hexdigest()}
		return {"label": "frame", "displays": [display]}

	def test_scaled_and_unscaled_frames_hash_to_their_recorded_digest(self) -> None:
		import tempfile
		with tempfile.TemporaryDirectory() as folder:
			run_dir = Path(folder)
			raw = bytes([0, 1, 2, 3, 0, 0, 1, 3])
			scaled = bytes(round(value * 255 / 3) for value in raw)
			snapshot = self.snapshot(run_dir, scaled, raw)
			self.assertEqual(hashlib.sha256(raw).hexdigest(), RUNTIME.frame_digest(run_dir, snapshot))
			# A frame beyond the layout's depth is stored unscaled, even when its values look scaled.
			unscaled = bytes([0, 255, 255, 0, 0, 0, 255, 0])
			snapshot = self.snapshot(run_dir, unscaled, unscaled)
			self.assertEqual(hashlib.sha256(unscaled).hexdigest(), RUNTIME.frame_digest(run_dir, snapshot))

	def test_altered_missing_or_malformed_frames_are_refused(self) -> None:
		import tempfile
		with tempfile.TemporaryDirectory() as folder:
			run_dir = Path(folder)
			raw = bytes([0, 1, 2, 3, 0, 0, 1, 3])
			snapshot = self.snapshot(run_dir, bytes(round(value * 255 / 3) for value in raw), raw)
			path = run_dir / "dmd" / "000-frame-display-0.pgm"
			path.write_bytes(path.read_bytes()[:-1] + b"\x00")
			with self.assertRaises(ValueError):
				RUNTIME.frame_digest(run_dir, snapshot)
			path.write_bytes(b"P5\n4 3\n255\n" + bytes(12))
			with self.assertRaises(ValueError):
				RUNTIME.frame_digest(run_dir, snapshot)
			path.unlink()
			with self.assertRaises(OSError):
				RUNTIME.frame_digest(run_dir, snapshot)


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class BreakshotRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		source_root = CURATOR.configured_vpx_sources_root(required=True)
		manifest = CURATOR.verify_extraction_manifest(source_root)
		self.assertEqual(CURATOR.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match(self) -> None:
		source_root = CURATOR.configured_vpx_sources_root(required=True)
		folder = source_root / "capcom/breakshot-1996"
		self.assertEqual(CURATOR.TABLE_SHA256, CURATOR._file_sha256(folder / "source/Breakshot (Capcom 1996) VPW v1.1.vpx"))
		self.assertEqual(CURATOR.SCRIPT_SHA256, CURATOR._file_sha256(folder / "extracted-vpxtool/script.vbs"))

	def test_retained_gi_lights_match_the_pinned_centres(self) -> None:
		source_root = CURATOR.configured_vpx_sources_root(required=True)
		gameitems = source_root / "capcom/breakshot-1996/extracted-vpxtool/gameitems"
		lights = {}
		for path in sorted(gameitems.glob("Light.gi*.json")):
			light = json.loads(path.read_text(encoding="utf-8"))["Light"]
			self.assertFalse(light["is_backglass"], path.name)
			lights[light["name"]] = (round(light["center"]["x"] / 952, 6), round(light["center"]["y"] / 2162, 6))
		collections = {c["name"]: c["items"] for c in json.loads((gameitems.parent / "collections.json").read_text(encoding="utf-8"))}
		self.assertEqual(sorted(lights), sorted(collections["GI"]))
		for double, kept in CURATOR.GI_RENDER_DOUBLES.items():
			self.assertEqual(lights.pop(double), lights[kept])
		self.assertEqual(CURATOR.GI_LIGHTS, lights)

	def test_retained_manual_matches_its_pinned_hash(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("manuals root is not configured")
		path = Path(root) / "by-machine/capcom.breakshot.1996/ipdb/Capcom_1996_Breakshot_Manual.pdf"
		self.assertEqual(CURATOR.MANUAL_SHA256, CURATOR._file_sha256(path))
		self.assertEqual(CURATOR.IPDB_PAGE_SHA256, CURATOR._file_sha256(path.parent / "ipdb-machine-3784.html"))

	def test_retained_pool_player_pages_match_their_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("manuals root is not configured")
		folder = Path(root) / "by-machine/illinois-pinball.pool-player.2000/web"
		for source in load_json(POOL_PLAYER_PATH)["sources"]:
			if "original_filename" in source:
				self.assertEqual(source["sha256"], CURATOR._file_sha256(folder / source["original_filename"]), source["id"])
		self.assertEqual("c9993b8f9f8f5ccbb09677f652d8186fc2e8fef97fa19f523d7ab795768570e5", CURATOR._file_sha256(folder / "pinballnews-illinois.jpg"))

	def test_retained_review_artifacts(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		reviews = Path(root)
		self.assertGreaterEqual(drawing_callouts.verify_retained(load_json(CALLOUT_PATH), ROOT, None, reviews), 3)
		libraries = reviews / "big-bang-bar/vpm-script-libs"
		self.assertEqual(CURATOR.VPM_CAPCOM_LIBRARY_SHA256, CURATOR._file_sha256(libraries / "capcom.vbs"))
		self.assertEqual(CURATOR.VPM_CORE_LIBRARY_SHA256, CURATOR._file_sha256(libraries / "core.vbs"))
		self.assertEqual(RUNTIME.build(reviews), (ROOT / "evidence/runtime/capcom/breakshot-service-diagnostics.json").read_bytes())


if __name__ == "__main__":
	unittest.main()
