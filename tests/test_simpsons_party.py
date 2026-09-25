from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "the-simpsons-pinball-party-2003.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "the-simpsons-pinball-party-2003.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-simpsons-pinball-party-2003.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "the-simpsons-pinball-party-2003.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "whitestar.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "the-simpsons-pinball-party-2003.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "stern" / "the-simpsons-pinball-party-2003.md"

DRIVER_IDS = {
	"simpprty", "simpprtf", "simpprtg", "simpprti", "simpprtl",
	"simp400", "simp400f", "simp400g", "simp400i", "simp400l",
	"simp300", "simp300f", "simp300i", "simp300l",
	"simp204", "simp204f", "simp204i", "simp204l",
}
MATRIX_ADDRESSES = {(column - 1) * 8 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {27, 28}
OPTO_ADDRESSES = {14, 15}
DEDICATED_ADDRESSES = {84, 83, 82, 81, 88, -2, -1, 0}
FLIPPER_COLUMN_HOLES = {85, 86, 87}
LAMP_ADDRESSES = {(row - 1) * 8 + column for column in range(1, 9) for row in range(1, 11)}
AUX_PORT_LAMP_ADDRESSES = set(range(81, 97))
UNUSED_LAMP_ADDRESSES = {71, 72}
STACKING_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "simpsons-pinball-party-stacking-opto.json"
FLIPPER_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "simpsons-pinball-party-flipper-buttons.json"
RAW_RUN_PREFIX = "external:pinmame-review-artifacts/"


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
	import curate_simpsons_party as curator

	argv = sys.argv
	sys.argv = ["curate_simpsons_party.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class SimpsonsPartyDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		# Held at partial by lamp 80's unplaced second LED and by public lamps 81-96, whose
		# availability is unknown. Polarity and both former conflicts were settled on 2026-09-25.
		self.assertEqual(["output_semantics", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["semantic_naming"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in ("semantic_naming", "spatial_placement"):
				continue
			self.assertEqual("validated", state, dimension)
		self.assertEqual("stern.the-simpsons-pinball-party.2003", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(4674, self.definition["machine"]["ipdb_id"])
		self.assertEqual(2003, self.definition["machine"]["year"])
		self.assertEqual("Stern", self.definition["machine"]["manufacturer"])
		self.assertEqual({"width": 952.0, "height": 2115.0, "units": "vpx"}, self.definition["machine"]["playfield"])
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		self.assertEqual("0x4000000000", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_former_conflicts_are_settled_and_nothing_still_cites_them(self) -> None:
		"""Both conflicts were resolved by evidence, so no record may keep pointing at them.

		conflict.whitestar-invsw-never-populated fell to the script (switch 14) and ROM runs
		(switch 15). conflict.upper-flipper-button-not-read was never a disagreement about the
		machine: DS-5 is the doubled right button's second contact, and PinMAME preserves a host
		write to public 88 even though it never synthesizes it.
		"""
		self.assertEqual([], self.definition["conflicts"])
		definition_text = DEFINITION_PATH.read_text(encoding="utf-8")
		for stale in ("conflict.whitestar-invsw-never-populated", "conflict.upper-flipper-button-not-read"):
			self.assertNotIn(stale, definition_text, stale)
		text = definition_text + KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for claim in ("structurally unreachable", "always reads inactive", "never read by this driver"):
			self.assertNotIn(claim, text, claim)

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_simpprty_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
			self.assertEqual("Stern", driver["manufacturer"])
			self.assertEqual("2003", driver["year"])
		self.assertEqual(1, len([d for d in self.definition["drivers"] if d["id"] == "simpprty" and "clone_of" not in d]))

	def test_the_full_whitestar_switch_matrix_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | DEDICATED_ADDRESSES | FLIPPER_COLUMN_HOLES | {-3}
		self.assertEqual(expected, set(self.switches) | set(self.dips))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"])
			self.assertEqual({"status": "not_applicable", "reason": "unused", "provenance": self.switches[address]["spatial"]["provenance"]}, self.switches[address]["spatial"])
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertIn(self.switches[address]["availability"], {"used", "optional"}, address)

	def test_opto_switches_are_flagged_but_not_pinmame_normalized(self) -> None:
		"""Whitestar normalizes nothing; 14 is settled by the script and 15 by the ROM.

		se.c's switch_r returns ~core_getSwCol, so public 1 is the CPU's closed-contact reading,
		and both optos are active at 1: their matrix-facing contact rests open.
		"""
		for address in OPTO_ADDRESSES:
			switch = self.switches[address]
			notes = switch["physical"]["notes"]
			self.assertEqual("opto", switch["physical"]["switch_type"])
			self.assertFalse(switch["normally_closed"], f"switch {address}: the opto's matrix contact rests open")
			self.assertIn("~core_getSwCol", notes)
			self.assertIn("zero-initialized", notes)
			self.assertIn("never inverts it", notes)
			self.assertNotIn("PinMAME normalizes", notes)
		self.assertIn("cvpmBallStack.SetSw", self.switches[14]["physical"]["notes"])
		self.assertIn("vpm-script-library.core-vbs-3-61", self.switches[14]["provenance"]["source_refs"])
		self.assertNotIn("runtime.simpsons-pinball-party.stacking-opto", self.switches[14]["provenance"]["source_refs"])
		self.assertIn("runtime.simpsons-pinball-party.stacking-opto", self.switches[15]["provenance"]["source_refs"])
		self.assertIn("vpmTimer.PulseSw 15", self.switches[15]["physical"]["notes"])
		for address, switch in self.switches.items():
			if address in OPTO_ADDRESSES or address in UNUSED_MATRIX_ADDRESSES:
				continue
			if switch.get("physical", {}).get("switch_type") == "opto":
				self.fail(f"switch {address} unexpectedly typed opto")

	def test_dedicated_switches_and_memory_protect(self) -> None:
		for address in DEDICATED_ADDRESSES:
			self.assertIn(address, self.switches)
		self.assertIn(-3, self.switches)
		self.assertEqual("Coin Door Memory Protect Interlock", self.switches[-3]["label"])
		ds5 = self.switches[88]
		self.assertEqual("used", ds5["availability"])
		self.assertEqual(["flipper.upper.right.button"], ds5["roles"])
		self.assertEqual("180-5164-00 Doubled", ds5["physical"]["part_number"])
		self.assertEqual(ds5["physical"]["part_number"], self.switches[82]["physical"]["part_number"])
		for phrase in ("second contact", "core_updateSw rewrites only the bits inside flipMask", "drive 82 and 88 together"):
			self.assertIn(phrase, ds5["physical"]["notes"])
		self.assertIn("runtime.simpsons-pinball-party.flipper-buttons", ds5["provenance"]["source_refs"])
		self.assertEqual({"status": "not_applicable", "reason": "cabinet_or_service", "provenance": ds5["spatial"]["provenance"]}, ds5["spatial"])
		for address in (84, 83, 82, 81, 88, -2, -1, 0):
			self.assertEqual("used", self.switches[address]["availability"])
			self.assertFalse(self.switches[address]["normally_closed"], address)
		for address in FLIPPER_COLUMN_HOLES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)

	def test_upper_and_top_right_flippers_follow_the_cabinet_buttons(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		trio = mechanisms["mechanism.upper-and-top-right-flippers"]
		self.assertEqual(["switch.dedicated-ds-1", "switch.dedicated-ds-5"], trio["sensors"])
		self.assertEqual(3, len(trio["actuators"]))
		self.assertIn("DS-1 (public 84)", self.solenoids[12]["physical"]["notes"])
		for address in (13, 14):
			self.assertIn("DS-5 (public 88)", self.solenoids[address]["physical"]["notes"], address)
			self.assertIn("runtime.simpsons-pinball-party.flipper-buttons", self.solenoids[address]["provenance"]["source_refs"])

	def test_flipper_power_hold_mapping_matches_pinned_source(self) -> None:
		right_power = self.solenoids[45]
		right_hold = self.solenoids[46]
		left_power = self.solenoids[47]
		left_hold = self.solenoids[48]
		for device in (right_power, right_hold):
			self.assertEqual("16", next(a["value"] for a in device["aliases"] if a["namespace"] == "manual.address"))
		for device in (left_power, left_hold):
			self.assertEqual("15", next(a["value"] for a in device["aliases"] if a["namespace"] == "manual.address"))
		self.assertIn(15, self.solenoids)
		self.assertIn(16, self.solenoids)
		# Public 15 is PinMAME's fast-flip/game-on state (se.c fastflipaddr, simpprty only).
		self.assertEqual("used", self.solenoids[15]["availability"])
		self.assertEqual("Fast-Flip Game-On State", self.solenoids[15]["label"])
		self.assertEqual("virtual", self.solenoids[15]["kind"])
		self.assertEqual("virtual", self.solenoids[15]["spatial"]["reason"])
		self.assertIn("seventeen clone drivers", self.solenoids[15]["physical"]["notes"])
		self.assertEqual("unused", self.solenoids[16]["availability"])

	def test_the_full_solenoid_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		flashers = {21, 22, 23, 25, 26, 27, 28, 29, 31, 32}
		for address in flashers:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		self.assertEqual("optional", self.solenoids[24]["availability"])
		for address in (33, 34, 35):
			self.assertEqual("optional", self.solenoids[address]["availability"], address)
			self.assertEqual({"status": "not_applicable", "reason": "unused", "provenance": self.solenoids[address]["spatial"]["provenance"]}, self.solenoids[address]["spatial"])
		for address in (36, 37, 38, 39, 40, 41, 42, 43, 44, 50):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		self.assertEqual("unused", self.solenoids[49]["availability"])
		self.assertEqual({"status": "not_applicable", "reason": "virtual", "provenance": self.solenoids[49]["spatial"]["provenance"]}, self.solenoids[49]["spatial"])

	def test_the_full_public_lamp_range_is_enumerated(self) -> None:
		# hw.lampCol = 4 makes PinMAME publish 1-96, not 1-80 (and not the 81-112 an earlier
		# pass assumed): two of the four declared columns are the printed rows 9-10.
		self.assertEqual(LAMP_ADDRESSES | AUX_PORT_LAMP_ADDRESSES, set(self.lamps))
		for address in UNUSED_LAMP_ADDRESSES:
			self.assertEqual("unused", self.lamps[address]["availability"])
		self.assertEqual("optional", self.lamps[32]["availability"])
		self.assertEqual("not_applicable", self.lamps[32]["spatial"]["status"])
		self.assertEqual(2, self.lamps[16]["physical"]["quantity"])
		for address in AUX_PORT_LAMP_ADDRESSES:
			lamp = self.lamps[address]
			self.assertEqual("virtual", lamp["kind"], address)
			self.assertEqual("unknown", lamp["availability"], address)
			self.assertEqual("virtual", lamp["spatial"]["reason"], address)
			port = "$3406" if address <= 88 else "$3407"
			self.assertIn(port, lamp["label"], address)
			self.assertIn("Resolution path:", lamp["physical"]["notes"], address)

	def test_mode_sign_leds_are_placed_per_led_only_where_the_evidence_separates_them(self) -> None:
		"""Lamps 73-80 are the back-panel LED mode sign (board 520-5225-00), not the TV.

		The sign is vertical, so L1-L7 share one playfield point and each is placed at its own
		retained primitive. Lamp 80 is two LEDs (L8, L9) with one retained object, so it gets no
		spatial key rather than a one-of-two placement.
		"""
		column = []
		for address in range(73, 80):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertIn("520-5225-00", lamp["physical"]["notes"], address)
			placements = lamp["spatial"]["placements"]
			self.assertEqual(1, len(placements), address)
			self.assertEqual("emitter", placements[0]["role"])
			column.append((placements[0]["x"], placements[0]["y"]))
		xs = [x for x, _ in column]
		ys = [y for _, y in column]
		self.assertLess(max(xs) - min(xs), 0.0002)
		self.assertLess(max(ys) - min(ys), 0.0002)
		self.assertLess(max(ys), 0.05, "the sign stands at the rear of the playfield")
		self.assertEqual(len(set(column)), len(column), "each lamp keeps its own primitive's coordinate")
		lamp80 = self.lamps[80]
		self.assertEqual(2, lamp80["physical"]["quantity"])
		self.assertNotIn("spatial", lamp80)
		self.assertIn("L8 at the bottom-left and L9 at the bottom-right", lamp80["physical"]["notes"])

	def test_gi_is_a_single_aggregate_channel(self) -> None:
		self.assertEqual({0}, set(self.gi))
		gi = self.gi[0]
		self.assertEqual("validated", gi["spatial"]["status"])
		self.assertEqual(42, len(gi["spatial"]["placements"]))
		self.assertEqual(42, gi["physical"]["quantity"])

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen_ids: set[str] = set()
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				spatial = device.get("spatial")
				if spatial is None or spatial["status"] == "not_applicable":
					continue
				self.assertEqual("validated", spatial["status"], device["id"])
				for placement in spatial["placements"]:
					self.assertNotIn(placement["id"], seen_ids, placement["id"])
					seen_ids.add(placement["id"])
					self.assertGreaterEqual(placement["x"], 0.0)
					self.assertLessEqual(placement["x"], 1.0)
					self.assertGreaterEqual(placement["y"], 0.0)
					self.assertLessEqual(placement["y"], 1.0)

	def test_geometric_ordering_regression_assertions(self) -> None:
		# Left/right flippers: left flipper must sit left of right flipper.
		left_flipper_x = self.solenoids[47]["spatial"]["placements"][0]["x"]
		right_flipper_x = self.solenoids[45]["spatial"]["placements"][0]["x"]
		self.assertLess(left_flipper_x, right_flipper_x)
		# Outlanes/return lanes: left-named switches sit left of right-named switches.
		self.assertLess(self.switches[57]["spatial"]["placements"][0]["x"], self.switches[60]["spatial"]["placements"][0]["x"])
		self.assertLess(self.switches[58]["spatial"]["placements"][0]["x"], self.switches[61]["spatial"]["placements"][0]["x"])
		# Slingshots: left slingshot left of right slingshot.
		self.assertLess(self.switches[59]["spatial"]["placements"][0]["x"], self.switches[62]["spatial"]["placements"][0]["x"])
		# Jet bumpers: switch identity agrees with the manual name for each bumper's own position.
		left_bumper_x = self.switches[49]["spatial"]["placements"][0]["x"]
		right_bumper_x = self.switches[50]["spatial"]["placements"][0]["x"]
		self.assertLess(left_bumper_x, right_bumper_x)
		# Rear/front: trough (rear-ish, near drain at high y) sits further front (higher y) than
		# the upper playfield standups (low y, near the backglass end).
		self.assertGreater(self.switches[10]["spatial"]["placements"][0]["y"], self.switches[35]["spatial"]["placements"][0]["y"])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		actuator_ids = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		for address, solenoid in self.solenoids.items():
			if solenoid["kind"] not in ("coil", "motor"):
				continue
			if solenoid["availability"] != "used":
				continue
			if address in (45, 46, 47, 48):
				continue  # covered by mechanism.lower-flippers as a group, not per-address alias.
			if address == 2:
				continue  # Auto Launch is a standalone coil (plungerIM.AutoFire); no additional topology to document.
			self.assertIn(solenoid["id"], actuator_ids, f"solenoid {address} ({solenoid['label']}) has no mechanism")

	def test_spatial_report_names_the_single_remaining_gap(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual(1, len(report["blockers"]))
		self.assertIn("Lamp 80", report["blockers"][0])
		self.assertEqual([{"address": 80, "group": "pinmame.output.lamp"}], report["omitted_outputs"])
		self.assertEqual([], report["omitted_inputs"])
		self.assertEqual(2, len(report["additional_tables_checked"]))

	def test_relationships_use_proven_causality_only(self) -> None:
		self.assertEqual(1, len(self.definition["relationships"]))
		relationship = self.definition["relationships"][0]
		self.assertEqual("pulse", relationship["kind"])

	def test_display_inventory_is_the_backbox_dmd_and_mini_dmd(self) -> None:
		displays = {display["id"]: display for display in self.definition["displays"]}
		self.assertEqual({"display.dmd", "display.mini-dmd"}, set(displays))
		for display in displays.values():
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		for source in self.definition["sources"]:
			self.assertNotIn("E:\\", source["uri"])
			self.assertNotIn("C:\\", source["uri"])
			if source["id"] in ("manual.stern.the-simpsons-pinball-party.2003", "vpx-table.simpsons-party-0-8-2", "vpx-script.simpsons-party-0-8-2"):
				self.assertIn("sha256", source, source["id"])
				self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
			if source["kind"] == "manual":
				excerpts = source.get("excerpts") or []
				self.assertGreaterEqual(len(excerpts), 6)
				for excerpt in excerpts:
					self.assertIn(excerpt["method"], {"manual", "ocr", "model", "mixed"})

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		controller = load_json(CONTROLLER_PATH)
		group_ids = {group["id"] for group in controller["groups"]}
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi"},
			group_ids,
		)


def _raw_run(raw: dict[str, object]) -> dict[str, object] | None:
	"""Load a retained raw harness run and check its hash, or return None without the evidence root."""
	import hashlib

	root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not root:
		return None
	locator = str(raw["retained_from"])
	path = Path(root) / locator[len(RAW_RUN_PREFIX):]
	if hashlib.sha256(path.read_bytes()).hexdigest() != raw["sha256"]:
		raise AssertionError(f"{raw['name']}: retained raw run does not match its pinned SHA-256")
	return load_json(path)


def _fired(run: dict[str, object]) -> list[tuple[float, int]]:
	return [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"]]


class SimpsonsPartyRuntimeEvidenceTests(unittest.TestCase):
	def _check_scenarios(self, evidence: dict[str, object]) -> None:
		import hashlib

		self.assertEqual("simpprty", evidence["runtime"]["game"])
		self.assertEqual("deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c", evidence["runtime"]["emulator"]["sha256"])
		for raw in evidence["runtime"]["raw_runs"]:
			self.assertTrue(raw["retained_from"].startswith(RAW_RUN_PREFIX), raw["name"])
			scenario = ROOT / raw["scenario_path"]
			self.assertEqual(raw["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest(), raw["name"])

	def test_stacking_opto_runtime_evidence_separates_rest_from_active(self) -> None:
		evidence = load_json(STACKING_EVIDENCE_PATH)
		self._check_scenarios(evidence)
		observations = evidence["runtime"]["observations"]["named_action_observations"]
		# 0 at boot and a fall to 0 draw nothing; 1 at boot and every rise to 1 draw the up-kicker
		# and the auto launch.
		self.assertEqual([[], [1, 2], [1, 2], [], [1, 2]], [item["transitioned_solenoid_addresses"] for item in observations])
		self.assertTrue(all(address <= 80 for address in evidence["runtime"]["observations"]["lamp_addresses_seen"]))
		kick = [1, 1, 1, 1, 1, 1, 2]
		expected = {
			# boot at 0, raised to 1, lowered to 0, raised to 1 again
			"simpprty-stacking-opto": [(0, []), (1, kick), (0, []), (1, kick)],
			# boot with 15 held at 1 from power-up, then 35 s of attract mode still at 1
			"simpprty-stacking-opto-boot-active": [(1, kick), (1, [])],
		}
		for raw in evidence["runtime"]["raw_runs"]:
			run = _raw_run(raw)
			if run is None:
				continue
			fired = _fired(run)
			self.assertEqual({1, 2}, {number for _, number in fired}, raw["name"])
			self.assertFalse([e for e in run["events"] if e["event"] == "lamp" and e["number"] > 80], raw["name"])
			snapshots = run["snapshots"]
			level = {s["label"]: next(w["state"] for w in s["watched_switches"] if w["number"] == 15) for s in snapshots}
			# Rebuild each window from the raw run: which level switch 15 held, and what fired.
			edges = [0.0] + [s["time_s"] for s in snapshots[1:]]
			windows = []
			for start, snap in zip(edges, snapshots[1:]):
				burst = [number for time, number in fired if start < time <= snap["time_s"]]
				windows.append((level[snap["label"]], burst))
			self.assertEqual(expected[raw["name"]], windows, raw["name"])

	def test_flipper_button_runtime_evidence_ties_ds5_to_solenoids_13_and_14(self) -> None:
		evidence = load_json(FLIPPER_EVIDENCE_PATH)
		self._check_scenarios(evidence)
		observations = {item["input_address"]: item for item in evidence["runtime"]["observations"]["named_action_observations"] if "alone" in item["label"]}
		self.assertEqual([45, 46], observations[82]["transitioned_solenoid_addresses"])
		self.assertEqual([13, 14], observations[88]["transitioned_solenoid_addresses"])
		self.assertEqual([12, 47, 48], observations[84]["transitioned_solenoid_addresses"])
		self.assertTrue(all(address <= 80 for address in evidence["runtime"]["observations"]["lamp_addresses_seen"]))
		(raw,) = evidence["runtime"]["raw_runs"]
		run = _raw_run(raw)
		if run is None:
			return
		# Rebuild what each held button turned on, straight from the raw run's per-step transitions.
		turned_on = {}
		for step in run["steps"]:
			turned_on[step["label"]] = sorted(
				item["number"] for item in step["transitions"].get("solenoids", []) if 1 in item["states"]
			)
		self.assertEqual([45, 46], turned_on["Right Flipper Button (DS-3, public 82) held alone"])
		self.assertEqual([13, 14], turned_on["Upper Rt. Flipper Button (DS-5, public 88) held alone"])
		self.assertEqual([13, 14, 45, 46], turned_on["Upper Rt. Flipper Button pressed together with DS-3"])
		self.assertEqual([12, 47, 48], turned_on["Left Flipper Button (DS-1, public 84) held alone as a control"])
		# Public 15, the fast-flip/game-on state, is 0 through attract mode and rises with the game.
		active15 = {s["label"]: 15 in s["active_solenoids"] for s in run["snapshots"]}
		self.assertFalse(active15["left coin 4"])
		self.assertTrue(active15["Start button"])
		self.assertFalse([e for e in run["events"] if e["event"] == "lamp" and e["number"] > 80])


class SimpsonsPartyCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_simpsons_party as curator

		definition = curator.build()
		self.assertEqual(curator.canonical_bytes(definition), curator.canonical_bytes(curator.build()))
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
		self.assertEqual(curator.canonical_bytes(definition), DEFINITION_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_simpsons_party as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_simpsons_party as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b'"partial"', b'"author_ready"', 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_simpsons_party as curator

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(SPATIAL_REPORT_PATH.read_bytes(), curator.canonical_bytes(report))
		self.assertEqual(SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"), curator.render_spatial_report(report))


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class SimpsonsPartyRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_simpsons_party as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_simpsons_party as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "stern/the-simpsons-pinball-party-2003/source/The Simpsons Pinball Party v0.8.2.vpx"
		script = source_root / "stern/the-simpsons-pinball-party-2003/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_simpsons_party as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "the-simpsons-pinball-party-2003" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
