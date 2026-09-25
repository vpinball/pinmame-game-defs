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

DEFINITION_PATH = ROOT / "machines" / "partial" / "sega" / "goldeneye-1996.json"
SEED_PATH = ROOT / "tools" / "seeds" / "sega" / "goldeneye-1996.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "sega" / "goldeneye-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "sega" / "goldeneye-1996.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "sega" / "goldeneye-1996.json"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "goldeneye-satellite-and-ball-serve.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
MACHINE_ID = "sega.goldeneye.1996"
UNUSED_MATRIX = {8, 21, 22, 29, 35, 36, 37, 38, 49}
UNUSED_SOLENOIDS = {3, 5, 6, 7, 19, 23}
UNUSED_LAMPS = {9, 64, 70, 71}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_xy(device: dict) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


class GoldenEyeTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = by_address(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = by_address(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_address(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gis = by_address(cls.definition, "outputs", "pinmame.output.gi")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def test_identity_and_honest_partial_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "GoldenEye", "Sega", 1996), (machine["id"], machine["name"], machine["manufacturer"], machine["year"]))
		self.assertEqual((3792, "G43wE-MQV5K", "physical_pinball"), (machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["output_semantics", "spatial_placement", "unresolved_conflicts"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
		self.assertEqual(["conflict.bulb-types"], [conflict["id"] for conflict in self.definition["conflicts"]])
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_catalog_maps_the_single_driver_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual({"gldneye"}, mapped)
		self.assertEqual(["gldneye"], [driver["id"] for driver in self.definition["drivers"]])

	def test_the_full_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(-3, 1)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		self.assertEqual(UNUSED_MATRIX, {address for address in range(1, 65) if self.switches[address]["availability"] == "unused"})
		self.assertEqual({1, 2, 3, 4}, {address for address, dip in self.dips.items() if dip["availability"] == "used"})

	def test_flipper_buttons_are_matrix_switches_and_the_dedicated_inputs_are_unused(self) -> None:
		self.assertEqual(["flipper.lower.left.button"], self.switches[63]["roles"])
		self.assertEqual(["flipper.lower.right.button"], self.switches[64]["roles"])
		for address in (82, 84, 85, 86, 87, 88):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("switch", self.switches[address]["kind"], address)
		self.assertIn("NOT USED", self.switches[84]["physical"]["notes"])

	def test_emulator_written_end_of_stroke_inputs_are_virtual_and_not_host_driven(self) -> None:
		# FLIP_SOL(FLIP_L) implies FLIP_EOS, so core_updateSw rewrites 81 (from 46) and 83 (from 48) every frame.
		for address, winding in ((81, "46"), (83, "48")):
			device = self.switches[address]
			self.assertEqual(("virtual", "used"), (device["kind"], device["availability"]), address)
			self.assertEqual(["internal.synthetic-flipper"], device["roles"])
			self.assertEqual("virtual", device["spatial"]["reason"])
			self.assertIn(f"public {winding}", device["physical"]["notes"])
			self.assertIn("must not drive it", device["physical"]["notes"])
			self.assertNotIn("normally_closed", device)

	def test_the_only_opto_rests_open_and_is_consumed_as_delivered(self) -> None:
		optos = {address for address, device in self.switches.items() if device.get("physical", {}).get("switch_type") == "opto"}
		self.assertEqual({15}, optos)
		self.assertFalse(self.switches[15]["normally_closed"])
		self.assertIn("runtime.goldeneye.satellite-and-ball-serve", self.switches[15]["provenance"]["source_refs"])
		self.assertTrue(all(device.get("normally_closed") in (None, False) for device in self.switches.values()))

	def test_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 81)), set(self.lamps))
		self.assertEqual({0}, set(self.gis))
		self.assertEqual(UNUSED_SOLENOIDS | {15, 16, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {a for a, d in self.solenoids.items() if d["availability"] == "unused"})
		self.assertEqual({8, 24}, {a for a, d in self.solenoids.items() if d["availability"] == "optional"})
		self.assertEqual({35, 36}, {a for a, d in self.solenoids.items() if d["availability"] == "unknown"})
		self.assertEqual(set(range(25, 33)), {a for a, d in self.solenoids.items() if d["kind"] == "flasher"})
		self.assertEqual({33, 34}, {a for a, d in self.solenoids.items() if d["kind"] == "magnet"})
		self.assertEqual("relay", self.solenoids[21]["kind"])
		self.assertEqual(UNUSED_LAMPS, {a for a, d in self.lamps.items() if d["availability"] == "unused"})

	def test_flipper_enables_are_control_signals_not_coils(self) -> None:
		for address, side in ((45, "right"), (46, "right"), (47, "left"), (48, "left")):
			device = self.solenoids[address]
			self.assertEqual("control_signal", device["kind"])
			self.assertEqual([f"flipper.lower.{side}"], device["roles"])
			self.assertIn("runtime.goldeneye.satellite-and-ball-serve", device["provenance"]["source_refs"])
		self.assertIn("Q16", self.solenoids[45]["physical"]["notes"])
		self.assertIn("Q15", self.solenoids[47]["physical"]["notes"])

	def test_speaker_panel_letters_and_start_lamp_are_cabinet_devices(self) -> None:
		for address in range(72, 81):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual(["cabinet.start"], self.lamps[57]["roles"])
		self.assertNotIn("spatial", self.lamps[58])
		# LL40 is a ramp-effect light with no bulb or insert object, so lamp 40 is not placed either.
		self.assertNotIn("spatial", self.lamps[40])

	def test_bulb_type_disagreement_is_a_conflict_on_every_playfield_lamp_and_906_flasher(self) -> None:
		conflict = self.definition["conflicts"][0]
		self.assertIn("Resolution path:", conflict["description"])
		self.assertNotIn("status", conflict)
		playfield = {a for a, d in self.lamps.items() if d["availability"] == "used"} - {57} - set(range(72, 81))
		self.assertEqual(playfield, {a for a, d in self.lamps.items() if d["provenance"]["status"] == "conflicted"})
		for address in playfield:
			self.assertIn("conflict.bulb-types", self.lamps[address]["physical"]["notes"], address)
		for address in (19, 27, 41):
			self.assertIn("Use #555 Bulbs only", self.lamps[address]["physical"]["notes"], address)
		self.assertEqual({25, 26, 27}, {a for a, d in self.solenoids.items() if d["provenance"]["status"] == "conflicted"})
		for address in (25, 26, 27):
			self.assertIn("#906", self.solenoids[address]["physical"]["notes"])

	def test_legacy_numeric_and_zero_padded_aliases_are_kept(self) -> None:
		def values(device: dict, namespace: str) -> list[str]:
			return [alias["value"] for alias in device.get("aliases", []) if alias["namespace"] == namespace]

		self.assertEqual(["7", "07", "007"], values(self.switches[7], "vpe-legacy.switch"))
		self.assertEqual(["63", "063"], values(self.switches[63], "vpe-legacy.switch"))
		self.assertEqual(["45", "045"], values(self.solenoids[45], "vpe-legacy.coil"))
		self.assertEqual(["1", "01", "001"], values(self.lamps[1], "vpe-legacy.lamp"))
		# The legacy record exposed the G.I. relay as lamp 0.
		self.assertEqual(["0", "00", "000"], values(self.gis[0], "vpe-legacy.lamp"))
		self.assertEqual([], values(self.lamps[40], "vpe-legacy.lamp"))

	def test_every_placement_is_observed_and_in_range(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("observed", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])

	def test_geometric_ordering(self) -> None:
		# Top lanes, left to right, and the matching lamps.
		self.assertLess(first_xy(self.switches[53])[0], first_xy(self.switches[52])[0])
		self.assertLess(first_xy(self.switches[52])[0], first_xy(self.switches[51])[0])
		self.assertLess(first_xy(self.lamps[30])[0], first_xy(self.lamps[31])[0])
		self.assertLess(first_xy(self.lamps[31])[0], first_xy(self.lamps[32])[0])
		# Outlanes, return lanes and slingshots sit on their printed sides.
		for left, right in ((57, 58), (59, 60), (61, 62)):
			self.assertLess(first_xy(self.switches[left])[0], 0.5)
			self.assertGreater(first_xy(self.switches[right])[0], 0.5)
		self.assertLess(first_xy(self.lamps[33])[0], first_xy(self.lamps[10])[0])
		# The bottom turbo bumper is below the left and right ones.
		self.assertGreater(first_xy(self.switches[42])[1], first_xy(self.switches[41])[1])
		self.assertGreater(first_xy(self.switches[42])[1], first_xy(self.switches[43])[1])
		# Right 5-bank runs from top (44) to bottom (48).
		ys = [first_xy(self.switches[address])[1] for address in (44, 45, 46, 47, 48)]
		self.assertEqual(sorted(ys), ys)

	def test_every_used_actuator_belongs_to_a_mechanism(self) -> None:
		actuators = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		used = {device["id"] for device in self.solenoids.values() if device["kind"] in {"coil", "motor", "relay", "magnet"} and device["availability"] == "used"}
		self.assertEqual(set(), used - actuators)
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertEqual(set(), set(mechanism["actuators"] + mechanism["sensors"]) - ids, mechanism["id"])

	def test_sources_carry_hashed_excerpts_without_local_paths(self) -> None:
		text = json.dumps(self.definition)
		self.assertNotIn("E:/", text)
		self.assertNotIn("C:\\", text)
		excerpts = self.sources["manual.sega.goldeneye.1996.operations-manual"]["excerpts"]
		self.assertEqual(39, len(excerpts))
		for excerpt in excerpts:
			self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest())
			self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest())
			self.assertTrue(excerpt["reviewed"])

	def test_runtime_evidence_is_pinned_and_matches_the_source_record(self) -> None:
		evidence = load_json(RUNTIME_PATH)
		self.assertEqual(["gldneye"], evidence["driver_ids"])
		self.assertEqual([MACHINE_ID], evidence["machine_ids"])
		runtime = evidence["runtime"]
		self.assertEqual("gldneye", runtime["game"])
		self.assertEqual(7, len(runtime["raw_runs"]))
		for run in runtime["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest(), run["name"])
		self.assertEqual({1, 2, 4, 17, 18, 20, 21, 24, 26, 32, 34, 45, 46, 47, 48}, set(runtime["observations"]["solenoid_addresses_seen"]))
		self.assertEqual("internal:evidence/runtime/whitestar/goldeneye-satellite-and-ball-serve.json", self.sources["runtime.goldeneye.satellite-and-ball-serve"]["uri"])

	def test_no_other_machine_identifier_leaks_into_the_artifacts(self) -> None:
		catalog = load_json(CATALOG_PATH)
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID}
		artifacts = DEFINITION_PATH.read_text(encoding="utf-8") + KNOWLEDGE_PATH.read_text(encoding="utf-8") + SPATIAL_REPORT_PATH.read_text(encoding="utf-8")
		# Every whole token, not only ones with an underscore, so a leaked clone-free driver id such as another
		# game's parent short name is caught too. The allowed tokens are English words or the sega2.vbs quote
		# ("GoldenEye and Apollo13 ...") that happen to be driver ids; each was reviewed.
		tokens = {token.lower() for token in re.findall(r"[A-Za-z0-9_]+", artifacts)}
		self.assertEqual(set(), tokens & foreign - {"apollo13", "escape", "pinball", "real"})
		for inherited in ("i500", "Indianapolis", "WPC-Security", "wpc_m"):
			self.assertNotIn(inherited, artifacts)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_goldeneye as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curator.build())
		self.assertEqual(expected, canonical_bytes(curator.build()))
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())
		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_refuses_drift(self) -> None:
		import shutil
		import tempfile

		import curate_goldeneye as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			drifted = root / DEFINITION_PATH.relative_to(ROOT)
			drifted.write_bytes(drifted.read_bytes().replace(b"Satellite Home", b"Satellite H0me", 1))
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_pinned_pinmame_declares_the_game_and_magnet_board(self) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		candidates = [Path(checkout)] if checkout else []
		working_root = resolve_working_root(ROOT)
		if working_root is not None:
			candidates.append(working_root / "source-checkouts" / "pinmame")
		base = next((path for path in candidates if (path / "src/wpc/segames.c").is_file()), None)
		if base is None:
			self.skipTest("pinned PinMAME checkout is not available")
		games = (base / "src/wpc/segames.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("INITGAME(gldneye,GEN_WS,se_dmd128x32,SE_BOARDID_520_5143_00)", games)
		self.assertIn("{FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), 0, 2, 0, 0, hw}", games)
		se = (base / "src/wpc/se.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("core_write_masked_pwm_output_8b(CORE_MODOUT_SOL0 + 33 - 1, selocals.auxdata, 0x03); // Solenoids 33..34: magnet 1 & 2 enable states", se)
		self.assertIn("static READ_HANDLER(switch_r)	{ return ~core_getSwCol(selocals.swCol); }", se)
		self.assertNotIn('strncasecmp(gn, "gldneye"', se)


class GoldenEyeRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_goldeneye as curator

		curator.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_retained_table_and_script_hashes_and_claims(self) -> None:
		import curate_goldeneye as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "sega" / "goldeneye-1996"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "source" / "Goldeneye (Sega 1996) VPW 1.2.1.vpx").read_bytes()).hexdigest())
		script = (root / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script).hexdigest())
		text = script.decode("latin-1")
		self.assertIn('Const cGameName = "gldneye"', text)
		self.assertIn("bsTrough.InitSw 0,14,13,12,11,10,0,0", text)
		self.assertIn("If Enabled Then vpmTimer.PulseSw 15", text)
		self.assertIn('SolCallback(33)="SolRadarMagnet"', text)
		self.assertIn('SolCallback(34)="SolFlipperMagnet"', text)
		self.assertIn('SolCallback(45)="TiltMod"', text)
		self.assertIn('SolCallback(22)="DropRamp1.Enabled="', text)
		self.assertIn("Controller.Switch(23)=1", text)
		self.assertNotRegex(text, r"(?m)^\s*SolCallback\((35|36)\)")

	def test_retained_script_library_constants(self) -> None:
		import curate_goldeneye as curator

		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "goldeneye" / "vpm-script-libs"
		sega2 = (root / "sega2.vbs").read_bytes()
		self.assertEqual(curator.SEGA2_VBS_SHA256, hashlib.sha256(sega2).hexdigest())
		text = sega2.decode("latin-1")
		for constant in ("Const swLRFlip         = 64", "Const swLLFlip         = 63", "Const GameOnSolenoid = 48", "Const swSlamTilt       = 8"):
			self.assertIn(constant, text)
		self.assertEqual(curator.CORE_VBS_SHA256, hashlib.sha256((root / "core.vbs").read_bytes()).hexdigest())

	def test_retained_harness_runs(self) -> None:
		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "goldeneye" / "harness"
		for run in load_json(RUNTIME_PATH)["runtime"]["raw_runs"]:
			path = root / f"{run['name']}.json"
			self.assertEqual(run["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run["name"])
			self.assertIsNone(load_json(path)["failure"], run["name"])

	def test_runtime_observations_are_recomputed_from_the_raw_runs(self) -> None:
		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "goldeneye" / "harness"
		evidence = load_json(RUNTIME_PATH)["runtime"]
		runs = {run["name"]: load_json(root / f"{run['name']}.json") for run in evidence["raw_runs"]}
		observations = evidence["observations"]["named_action_observations"]

		def edges(name: str, kind: str, number: int, state: int) -> list[float]:
			return [event["time_s"] for event in runs[name]["events"] if event["event"] == kind and event["number"] == number and event["state"] == state]

		def label(name: str, index: int = 0) -> str:
			matches = [observation["label"] for observation in observations if f"({name})" in observation["label"]]
			return matches[index]

		recomputed: dict[str, list[float]] = {}

		def figures(text: str) -> list[str]:
			return re.findall(r"about (?:every )?(\d+(?:\.\d+)?) s", text)

		def matches(figure: str, value: float) -> bool:
			return abs(float(figure) - value) <= 0.5 * 10 ** -len(figure.partition(".")[2]) + 1e-9

		def record(text: str, value: float) -> None:
			recomputed.setdefault(text, []).append(value)

		def stated(name: str, value: float, digits: int, index: int = 0) -> None:
			# Each figure must appear, rounded to the stated precision, in the observation naming the run it was
			# measured in; every figure a label states must be one of these (checked at the end).
			text = label(name, index)
			record(text, value)
			self.assertTrue(any(matches(figure, value) for figure in figures(text) if len(figure.partition(".")[2]) == digits), (name, round(value, 3), text))

		def after_start(name: str) -> set[int]:
			start = edges(name, "switch", 3, 1)[0]
			return {event["number"] for event in runs[name]["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > start}

		seen = {event["number"] for run in runs.values() for event in run["events"] if event["event"] == "solenoid" and event["state"]}
		self.assertEqual(seen, set(evidence["observations"]["solenoid_addresses_seen"]))

		away = "gldneye-attract-satellite-away"
		stated(away, edges(away, "solenoid", 21, 1)[0], 1)  # 9.3
		stated(away, edges(away, "solenoid", 21, 0)[0] - edges(away, "solenoid", 21, 1)[0], 1)  # 13.8
		self.assertEqual([], [event for event in runs["gldneye-attract-satellite-home"]["events"] if event["event"] == "solenoid"])
		edge = "gldneye-satellite-home-edge"
		stated(edge, edges(edge, "solenoid", 21, 0)[0] - edges(edge, "switch", 20, 1)[0], 2)  # 0.11
		serve = "gldneye-ball-serve-and-launch"
		meter = [off - on for on, off in zip(edges(serve, "solenoid", 24, 1), edges(serve, "solenoid", 24, 0))]
		stated(serve, meter[0], 2)  # 0.14, coin meter
		stated(serve, max(meter), 2)  # 0.19 once
		stated(serve, edges(serve, "solenoid", 1, 1)[0] - edges(serve, "switch", 15, 1)[0], 2, 1)  # 0.28
		enables = edges(serve, "solenoid", 45, 1)[0]
		shooter = [observation["label"] for observation in observations if observation["input_address"] == 16][0]
		self.assertIn("about 14.8 s later", shooter)
		record(shooter, enables - edges(serve, "switch", 16, 1)[0])
		self.assertAlmostEqual(14.8, enables - edges(serve, "switch", 16, 1)[0], delta=0.05)
		self.assertEqual({45, 46, 47, 48}, {event["number"] for event in runs[serve]["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] == enables and event["number"] >= 45})
		fire = [observation["label"] for observation in observations if observation["input_address"] == 9][0]
		fired = edges(serve, "switch", 9, 1)[0]
		self.assertIn(f"about {edges(serve, 'solenoid', 2, 1)[0] - fired:.2f} s later", fire)  # 0.08
		self.assertIn(f"about {edges(serve, 'solenoid', 34, 0)[0] - edges(serve, 'solenoid', 34, 1)[0]:.1f} s", fire)  # 5.8
		self.assertIn(f"again {edges(serve, 'solenoid', 2, 1)[1] - edges(serve, 'solenoid', 2, 1)[0]:.1f} s later", fire)  # 3.9
		search = edges(serve, "solenoid", 18, 1)[0]
		self.assertIn(f"about {search - edges(serve, 'switch', 16, 0)[0]:.1f} s after that", fire)  # 18.5
		for value in (edges(serve, "solenoid", 2, 1)[0] - fired, edges(serve, "solenoid", 34, 0)[0] - edges(serve, "solenoid", 34, 1)[0], search - edges(serve, "switch", 16, 0)[0]):
			record(fire, value)
		order = []
		for event in runs[serve]["events"]:
			if event["event"] == "solenoid" and event["state"] and event["time_s"] >= search and event["number"] not in order:
				order.append(event["number"])
		self.assertIn("pulsing " + ", ".join(str(number) for number in order[:-1]) + f" and {order[-1]}", fire)

		control = "gldneye-ball-serve-without-vuk"
		self.assertEqual([], edges(control, "switch", 15, 1))
		first_launch = edges(control, "solenoid", 2, 1)[0]
		pulses = edges(control, "solenoid", 17, 1)
		before = [time for time in pulses if time < first_launch]
		self.assertEqual(5, len(before))
		stated(control, (before[-1] - before[0]) / 4, 1)  # 0.7
		stated(control, edges(control, "solenoid", 1, 1)[0] - pulses[0], 2)  # 3.45
		kicks = edges(control, "solenoid", 1, 1)
		stated(control, (kicks[-1] - kicks[0]) / (len(kicks) - 1), 1)  # 4.2
		self.assertEqual(9, len(kicks))
		self.assertIn("firing 1 nine times", label(control))
		start = edges(control, "switch", 3, 1)[0]
		self.assertEqual({1, 2, 17}, {event["number"] for event in runs[control]["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > start})

		opto_only = "gldneye-ball-serve-vuk-opto-only"
		self.assertEqual([], edges(opto_only, "switch", 14, 0))
		stated(opto_only, edges(opto_only, "solenoid", 1, 1)[0] - edges(opto_only, "switch", 15, 1)[0], 2)  # 0.25
		trough_only = "gldneye-ball-serve-trough-release-only"
		self.assertEqual([], edges(trough_only, "switch", 15, 1))
		stated(trough_only, edges(trough_only, "solenoid", 1, 1)[0] - edges(trough_only, "switch", 14, 0)[0], 2)  # 0.81
		self.assertEqual(5, len(edges(trough_only, "solenoid", 1, 1)))
		for name in (opto_only, trough_only):
			kicks = edges(name, "solenoid", 1, 1)
			burst = [time for time in kicks if time < kicks[0] + 5]
			self.assertEqual(5, len(burst), name)
			self.assertIn("four more times", label(name))
			stated(name, (burst[-1] - burst[0]) / 4, 2)  # 0.94 / 0.93
		# The VUK-only run resumes the lock-ball retries with 15 still at 1; the trough-only run stops.
		self.assertGreater(len([time for time in edges(opto_only, "solenoid", 17, 1) if time > edges(opto_only, "solenoid", 1, 1)[4]]), 0)
		last = max(event["time_s"] for event in runs[trough_only]["events"] if event["event"] == "solenoid" and event["time_s"] > edges(trough_only, "switch", 3, 1)[0])
		end = runs[trough_only]["snapshots"][-1]["time_s"]
		self.assertIn(f"remaining {end - last:.1f} s", label(trough_only))

		# Each observation's solenoid list is what its own run changed after Start, where the run pressed Start.
		for observation in observations:
			named = re.search(r"\((gldneye-[a-z-]+)\)", observation["label"])
			name = named.group(1) if named else None
			if name in (control, opto_only, trough_only):
				self.assertEqual(after_start(name), set(observation["transitioned_solenoid_addresses"]), name)
		# Two-way: every "about ... s" figure a label states was recomputed above.
		for observation in observations:
			for figure in figures(observation["label"]):
				self.assertTrue(any(matches(figure, value) for value in recomputed.get(observation["label"], [])), (figure, observation["label"]))

	def test_retained_manual_hashes(self) -> None:
		import curate_goldeneye as curator

		root = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / "sega.goldeneye.1996"
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256((root / "Sega_1996_Goldeneye_Manual.pdf").read_bytes()).hexdigest())
		self.assertEqual(curator.MANUAL_OCR_SHA256, hashlib.sha256((root / "Sega_1996_Goldeneye_Manual.ocr.pdf").read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
