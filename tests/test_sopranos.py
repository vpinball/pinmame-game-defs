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

import curate_sopranos as curator  # noqa: E402
import sopranos_runtime_evidence as evidence_tool  # noqa: E402
import sopranos_spatial_seed as seed_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "the-sopranos-2005.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-sopranos-2005.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "the-sopranos-2005-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "the-sopranos-2005-callouts.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "the-sopranos-stacking-opto-and-gameplay.json"
SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "whitestar"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "stern.the-sopranos.2005"

DRIVER_IDS = {
	"sopranos", "sopranof", "sopranog", "sopranoi", "sopranol", "sopr400", "sopr400f", "sopr400g", "sopr400i", "sopr400l",
	"sopr300", "sopr300f", "sopr300g", "sopr300i", "sopr300l", "soprano3", "sopr204", "sopr107f", "sopr107g", "sopr107i", "sopr107l",
}
# The Switch Matrix Grid's NOT USED cells (excerpt switch-matrix.md), and the Lamp Matrix Grid's (lamp-matrix.md).
NOT_USED_SWITCHES = {30, 41, 42, 43, 44, 45, 46, 47, 48, 52, 63, 64}
NOT_USED_LAMPS = {62, 63, 64}
# Cells the grid prints as optional equipment: UK buttons, the 4th/5th/6th coin slots, slam tilt and tournament kits.
OPTIONAL_SWITCHES = {1, 2, 3, 7, 8, 53, 55}
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "4d32c78ad266b18aa9abb508c63f924b92bdd8e88f933ff4e93a0a70d686a401"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


class SopranosTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("stern.the-sopranos.2005", 5053, "G5WoB-MDyNZ", 2005), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"]))
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.definition["drivers"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == "stern.the-sopranos.2005"}
		self.assertEqual(DRIVER_IDS, claimed)

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		def addresses(group: str) -> set[int]:
			return {item["binding"]["device"] for item in self.definition["inputs"] + self.definition["outputs"] if item["binding"]["group"] == group}
		self.assertEqual(set(range(-3, 1)) | set(range(1, 65)) | set(range(81, 89)), addresses("pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), addresses("pinmame.input.dip"))
		self.assertEqual(set(range(1, 51)), addresses("pinmame.output.solenoid"))
		self.assertEqual(set(range(1, 81)), addresses("pinmame.output.lamp"))
		self.assertEqual({0}, addresses("pinmame.output.gi"))
		keys = [(item["binding"]["group"], item["binding"]["device"]) for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(keys), len(set(keys)))

	def test_unused_and_optional_cells_follow_the_grids(self) -> None:
		unused = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "unused"}
		self.assertEqual(NOT_USED_SWITCHES, unused)
		optional = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "optional"}
		self.assertEqual(OPTIONAL_SWITCHES, optional)
		self.assertEqual(NOT_USED_LAMPS, {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "unused"})
		self.assertEqual("optional", self.device("output.lamp", 79)["availability"])
		self.assertEqual({33, 34, 35, 24}, {address for address in range(1, 51) if self.device("output.solenoid", address)["availability"] == "optional"})
		self.assertEqual("unused", self.device("input.switch", 88)["availability"])

	def test_polarity_follows_the_read_path_and_the_wiring_diagrams(self) -> None:
		for address in range(1, 65):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertTrue(self.device("input.switch", 81)["normally_closed"])
		self.assertTrue(self.device("input.switch", 83)["normally_closed"])
		for address in (82, 84, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({11, 12, 13, 14}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		self.assertEqual("opto", self.device("input.switch", 14)["physical"]["switch_type"])
		self.assertEqual("opto", self.device("input.switch", 15)["physical"]["switch_type"])
		self.assertIn("runtime.the-sopranos.stacking-opto-and-gameplay", self.device("input.switch", 15)["provenance"]["source_refs"])

	def test_flipper_remap_and_synthetic_states(self) -> None:
		left = self.device("output.solenoid", 48)
		right = self.device("output.solenoid", 46)
		self.assertEqual(("device.q15-left-flipper", "coil"), (left["id"], left["kind"]))
		self.assertEqual(("device.q16-right-flipper", "coil"), (right["id"], right["kind"]))
		for address in (15, 45, 47):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		for address in (16, 36, *range(37, 45), 49, 50):
			self.assertEqual(("virtual", "unused"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		self.assertEqual("relay", self.device("output.solenoid", 18)["kind"])
		flashers = {address for address in range(1, 33) if self.device("output.solenoid", address)["kind"] == "flasher"}
		# The coil chart's note lists the flash lamps the Flash test fires: Q19-Q20, Q25-Q29, Q31-Q32.
		self.assertEqual({19, 20, 25, 26, 27, 28, 29, 31, 32}, flashers)

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		self.assertEqual(("Q14", "J10-P1/2"), (self.device("output.solenoid", 14)["wiring"]["driver_transistor"], self.device("output.solenoid", 14)["wiring"]["power_connection"]))
		self.assertEqual("J7-P10", self.device("output.solenoid", 24)["wiring"]["control_connection"])
		switch = self.device("input.switch", 54)["wiring"]
		self.assertEqual(("GRN-VIO", "CN5-P8", "WHT-BLU", "CN7-P3"), (switch["drive_wire"], switch["drive_connection"], switch["return_wire"], switch["return_connection"]))
		lamp = self.device("output.lamp", 80)["wiring"]
		self.assertEqual(("YEL-GRY", "J13-P1", "RED", "J12-P11"), (lamp["drive_wire"], lamp["drive_connection"], lamp["return_wire"], lamp["return_connection"]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
		names = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		self.assertTrue({"mechanism.trough", "mechanism.safe", "mechanism.fish", "mechanism.bada-bing", "mechanism.bing-lock", "mechanism.boat-lock", "mechanism.center-lock", "mechanism.drop-target"} <= names)

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				paths.add(Path(excerpt["path"]).name)
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], sha256(ROOT / excerpt["image"]), excerpt["id"])
					paths.add(Path(excerpt["image"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != "stern.the-sopranos.2005" and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), (ROOT / "knowledge/stern/the-sopranos-2005.md").read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		self.assertEqual(set(), words & foreign)

	def test_placements_are_in_range_unique_and_from_the_seeds(self) -> None:
		seed = load(SEED_PATH)
		self.assertEqual(curator.TABLE_SHA256, seed["table"]["sha256"])
		placement_ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				placement_ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
		self.assertEqual(len(placement_ids), len(set(placement_ids)))
		missing = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"] if item.get("availability") in {"used", "optional"} and "spatial" not in item}
		self.assertEqual(set(), missing)
		self.assertEqual(33, len(self.device("output.gi", 0)["spatial"]["placements"]))
		candidates = {item["binding"]["device"] for item in self.definition["outputs"] if (item.get("spatial") or {}).get("status") == "candidate"}
		self.assertEqual({33, 34, 35, 73, 74, 75, 76, 77}, candidates)

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		import drawing_callouts

		seed = load(CALLOUT_SEED_PATH)
		statuses = {placement["id"]: placement["provenance"]["status"] for item in self.definition["inputs"] + self.definition["outputs"] for placement in (item.get("spatial") or {}).get("placements") or []}
		measured = set(seed["measurements"])
		self.assertEqual(set(statuses) - measured, set(seed["checks"]) | set(seed["excluded_checks"]))
		self.assertFalse(set(seed["checks"]) & set(seed["excluded_checks"]))
		raw = {pid: (0.0, 0.0) for pid in statuses}
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements") or []:
				raw[placement["id"]] = (placement["x"], placement["y"])
		decisions = drawing_callouts.evaluate(seed, raw, seed["limit"])
		for pid, status in statuses.items():
			if pid in measured:
				self.assertEqual("candidate", status, pid)
				self.assertEqual(tuple(raw[pid]), drawing_callouts.measured(seed, pid), pid)
				continue
			expected = "validated" if decisions["placements"].get(pid, {}).get("agrees") else "observed"
			self.assertEqual(expected, status, pid)
		self.assertEqual(114, sum(status == "validated" for status in statuses.values()))

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_only_this_game_and_evidence_pins_its_runs(self) -> None:
		document = load(EVIDENCE_PATH)
		self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
		self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"])
		self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
		self.assertEqual(set(evidence_tool.RUNS), {run["name"] for run in document["runtime"]["raw_runs"]})
		self.assertEqual(evidence_tool.RUNS, curator.RUN_MANIFESTS)
		for run in document["runtime"]["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
			self.assertEqual("sopranos", load(scenario)["game"])
			self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		steps = {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(EVIDENCE_PATH)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith("sopranos-gameplay ")}
		expected = {"left bumper (public 49) closed once": 9, "right bumper (public 50) closed once": 10, "bottom bumper (public 51) closed once": 11,
		            "left slingshot (public 59) closed once": 12, "right slingshot (public 62) closed once": 13,
		            "a ball enters the center eject (public 28) and stays": 3, "a ball enters the left eject (public 17) and stays": 21}
		for label, coil in expected.items():
			self.assertIn(coil, steps[label]["active_solenoid_addresses"], label)
		self.assertTrue({47, 48} <= set(steps["left flipper button (public 84) held 1.5 s"]["active_solenoid_addresses"]))
		self.assertTrue({45, 46} <= set(steps["right flipper button (public 82) held 1.5 s"]["active_solenoid_addresses"]))
		self.assertIn(24, steps["coin 1 on the center coin slot (public 5)"]["active_solenoid_addresses"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		self.assertEqual(canonical_bytes(evidence_tool.build(root)), EVIDENCE_PATH.read_bytes())

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_stacking_opto_runs_separate_rest_from_active(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY
		# Rebuild from the raw events: what fired while public 15 held each level, window by window.
		expected = {"sopranos-stacking-opto": [(0, set()), (1, {1, 2}), (0, set()), (1, {1, 2})], "sopranos-stacking-opto-boot-active": [(1, {1, 2})]}
		for name, windows in expected.items():
			run = load(root / name / "run.json")
			level = next(item["state"] for item in run["initial_switches"] if item["switch"] == 15)
			edges = [(event["time_s"], event["state"]) for event in run["events"] if event["event"] == "switch" and event["number"] == 15 and not event.get("initial")]
			bounds = [0.0] + [time for time, _ in edges] + [float("inf")]
			levels = [level] + [state for _, state in edges]
			fired = [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"]]
			actual = []
			for index, held in enumerate(levels):
				during = {number for time, number in fired if bounds[index] <= time < bounds[index + 1] and number in {1, 2}}
				actual.append((held, during))
			self.assertEqual(windows, actual, name)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		base = root / "stern/the-sopranos-2005"
		table = base / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = base / "Sopranos, The (Stern 2005).vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		self.assertEqual(curator.CORPUS_SCRIPT_SHA256, sha256(base / "The Sopranos (Stern 2005) v1.22.vbs"))
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(line for line in script.read_text(encoding="latin-1").splitlines() if not line.strip().startswith("'"))
		self.assertIn('cGameName="sopranos"', code)
		self.assertIn("bsTrough.InitSw 0, 14, 13, 12, 11, 0, 0, 0", code)
		self.assertIn("vpmTimer.PulseSw 22", code)
		# The avoidance claim behind the stacking-opto note: no write to 15 in the embedded script.
		self.assertIsNone(re.search(r"(Switch\(\s*15\s*\)|PulseSw\s*\(?\s*15\b)", code, re.IGNORECASE))

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_matches_its_pin(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.MACHINE_ID / "ipdb-archive"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))


if __name__ == "__main__":
	unittest.main()
