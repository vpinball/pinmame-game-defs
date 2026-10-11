from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
DEFINITION_PATH = ROOT / "machines/partial/williams/terminator-2-judgment-day-1991.json"
AUDIT_PATH = ROOT / "reports/spatial/williams/terminator-2-judgment-day-1991.json"


def load(path: Path) -> dict[str, object]:
	return json.loads(path.read_text(encoding="utf-8"))


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class Terminator2DefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.audit = load(AUDIT_PATH)

	def test_definition_is_fail_closed_and_preserves_conflicts(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("unknown", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual({"conflict.solenoid-12-physical-presence", "conflict.lamp-schematic-connector-labels", "conflict.gi-string-routing"}, {item["id"] for item in self.definition["conflicts"]})
		# The lamp sheets disagree only on connector labels, a wiring detail kept as an ignored conflict.
		statuses = {item["id"]: item.get("status", "unresolved") for item in self.definition["conflicts"]}
		self.assertEqual("ignored", statuses.pop("conflict.lamp-schematic-connector-labels"))
		self.assertEqual({"unresolved"}, set(statuses.values()))
		for lamp in (item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"):
			self.assertEqual("validated", lamp["provenance"]["status"])
			self.assertIn(f"J137-{lamp['binding']['device'] // 10}", lamp["physical"]["notes"])
			self.assertIn("conflict.lamp-schematic-connector-labels is ignored", lamp["physical"]["notes"])
		self.assertNotEqual("author_ready", self.definition["coverage"]["status"])

	def test_switch_matrix_and_controller_inputs_are_complete(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 9)) | {row * 10 + column for row in range(1, 9) for column in range(1, 9)} | set(range(111, 119)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual("constant", switches[24]["kind"])
		self.assertTrue(switches[24]["constant_active"])
		self.assertTrue(switches[22]["normally_closed"])
		self.assertEqual("Gun Loaded", switches[31]["label"])
		self.assertEqual("Mid Right Standup Target", switches[47]["label"])
		self.assertEqual("Top Lane Center", switches[57]["label"])
		self.assertEqual("Shooter", switches[78]["label"])
		self.assertEqual("unused", switches[88]["availability"])
		self.assertEqual("validated", switches[51]["spatial"]["status"])

	def test_flipper_buttons_are_the_generic_column_button_bits(self) -> None:
		# t2GameData declares FLIP_SWNO(12,11) with no FLIP_SOL: core_updateSw copies the generic
		# button bits 112/114 into matrix 11/12.
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		for address, matrix, side in ((112, 11, "right"), (114, 12, "left")):
			button = switches[address]
			self.assertEqual("used", button["availability"])
			self.assertEqual([f"flipper.lower.{side}.button"], button["roles"])
			self.assertFalse(button["normally_closed"])
			self.assertEqual("cabinet_or_service", button["spatial"]["reason"])
			self.assertIn(f"copies it to matrix switch {matrix}", button["physical"]["notes"])
			self.assertIn(f"from generic cabinet input {address}", switches[matrix]["physical"]["notes"])
			self.assertIn("cannot be driven directly", switches[matrix]["physical"]["notes"])
		# Nothing synthesizes the EOS bits, but they are host-writable and readable, so unproven.
		for address, side in ((111, "right"), (113, "left")):
			eos = switches[address]
			self.assertEqual("optional", eos["availability"])
			self.assertEqual([f"internal.flipper.lower.{side}.eos"], eos["roles"])
			self.assertNotIn("normally_closed", eos)
			self.assertEqual("internal_nonvisual", eos["spatial"]["reason"])
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", switches[address]["availability"])
			self.assertEqual(["internal.unused.flipper"], switches[address]["roles"])

	def test_outputs_displays_mechanisms_and_variants_are_explicit(self) -> None:
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual(set(range(1, 51)), set(solenoids))
		for address in (29, 30):
			self.assertEqual("virtual", solenoids[address]["kind"], address)
			self.assertEqual("used", solenoids[address]["availability"], address)
			self.assertEqual(["internal.wpc-state"], solenoids[address]["roles"], address)
		self.assertEqual("relay", solenoids[31]["kind"])
		self.assertEqual("used", solenoids[31]["availability"])
		self.assertEqual(["internal.wpc-state"], solenoids[31]["roles"])
		self.assertEqual("cabinet_or_service", solenoids[31]["spatial"]["reason"])
		self.assertIn("real Game-On solenoid", solenoids[31]["physical"]["notes"])
		self.assertEqual("unused", solenoids[32]["availability"])
		self.assertEqual(["internal.unused.wpc-output"], solenoids[32]["roles"])
		self.assertIn("constant zero", solenoids[32]["physical"]["notes"])
		self.assertEqual(set(row * 10 + column for row in range(1, 9) for column in range(1, 9)), set(lamps))
		self.assertEqual(set(range(5)), set(gi))
		self.assertEqual("optional", solenoids[12]["availability"])
		self.assertNotIn("vpx-script.t2-vpw-0022", solenoids[12]["provenance"]["source_refs"])
		self.assertIn("no SolCallback(12)", solenoids[12]["physical"]["notes"])
		self.assertIn("KNOCK DOWN", solenoids[12]["physical"]["notes"])
		self.assertIn("runtime.terminator-2.t2-l8.solenoid-flasher-tests", solenoids[12]["provenance"]["source_refs"])
		# The manual and the ROM's flasher test agree on 24; the script's missing callback is a table gap.
		self.assertEqual("used", solenoids[24]["availability"])
		self.assertIn("F.L. C. BACKGLASS", solenoids[24]["physical"]["notes"])
		self.assertIn("gap in the table", solenoids[24]["physical"]["notes"])
		self.assertIn("runtime.terminator-2.t2-l8.solenoid-flasher-tests", solenoids[24]["provenance"]["source_refs"])
		conflict = {item["id"]: item for item in self.definition["conflicts"]}["conflict.solenoid-12-physical-presence"]
		resolution = conflict["description"].split("Resolution path:", 1)[1]
		self.assertNotIn("harness", resolution)
		self.assertIn("KNOCK DOWN", conflict["description"])
		self.assertIn("Not Used", json.dumps(self.definition["conflicts"]))
		self.assertEqual("flasher", solenoids[17]["kind"])
		self.assertEqual("coil", solenoids[28]["kind"])
		self.assertEqual({"control_wire": "Vio-Brn", "control_connection": "J130-1", "driver_transistor": "Q82"}, {key: solenoids[1]["wiring"][key] for key in ("control_wire", "control_connection", "driver_transistor")})
		self.assertEqual("J109-7", solenoids[46]["wiring"]["control_connection"])
		self.assertEqual("J120-7", gi[0]["wiring"]["control_connection"])
		self.assertEqual("Lower Right Flipper", solenoids[46]["label"])
		self.assertEqual("Lower Left Flipper", solenoids[48]["label"])
		self.assertEqual("dmd", self.definition["displays"][0]["kind"])
		self.assertEqual(9, len(self.definition["mechanisms"]))
		self.assertEqual({"relationship.trough-release", "relationship.drop-target-reset"}, {relationship["id"] for relationship in self.definition["relationships"]})
		self.assertNotIn("switch.matrix-31", {relationship["source"] for relationship in self.definition["relationships"]})
		self.assertEqual({"t2_d2", "t2_d3", "t2_d4", "t2_d6", "t2_d8", "t2_l2", "t2_l2sp1", "t2_l3", "t2_l4", "t2_l6", "t2_l8", "t2_l81", "t2_l82", "t2_l83", "t2_l84", "t2_p2f", "t2_p2g", "t2_f19", "t2_f20", "t2_f32"}, {driver["id"] for driver in self.definition["drivers"]})
		self.assertTrue(all(driver["physical_compatibility"] == "compatible" for driver in self.definition["drivers"] if driver["id"].startswith("t2_f")))
		self.assertFalse((ROOT / "machines/stubs/t2_l8.json").exists())
		self.assertFalse((ROOT / "knowledge/stubs/t2_l8.md").exists())
		self.assertEqual("Data Base 3", lamps[25]["label"])

	def test_retained_script_semantics_and_spatial_provenance_are_exact(self) -> None:
		trough = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.three-ball-trough")
		gun = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.gun-traverse")
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertIn("18,17,16,15", trough["behavior"])
		knowledge = (ROOT / "knowledge/williams/terminator-2-judgment-day-1991.md").read_text(encoding="utf-8")
		self.assertIn("switch 18 as the outhole/exit and switches 17, 16, and 15 as the three stack seats", knowledge)
		self.assertIn("length 240", gun["behavior"])
		self.assertIn("CurrentPos=aNewPos/3", gun["behavior"])
		self.assertEqual("conflicted", bindings(self.definition, "outputs", "pinmame.output.gi")[2]["spatial"]["status"])
		self.assertEqual((0.938104, 0.899932), tuple(switches[78]["spatial"]["placements"][0][key] for key in ("x", "y")))
		self.assertEqual((0.614497, 0.922582), tuple(switches[15]["spatial"]["placements"][0][key] for key in ("x", "y")))
		self.assertEqual("observed", switches[15]["spatial"]["status"])
		self.assertEqual((0.48207, 0.184143), tuple(switches[41]["spatial"]["placements"][0][key] for key in ("x", "y")))
		self.assertEqual((0.206389, 0.738286), tuple(switches[44]["spatial"]["placements"][0][key] for key in ("x", "y")))
		self.assertEqual((0.204672, 0.237459), tuple(switches[61]["spatial"]["placements"][0][key] for key in ("x", "y")))
		self.assertEqual("not_applicable", switches[34]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[34]["spatial"]["reason"])
		self.assertEqual("not_applicable", solenoids[7]["spatial"]["status"])
		self.assertEqual("not_applicable", solenoids[24]["spatial"]["status"])
		self.assertEqual("observed", lamps[52]["spatial"]["status"])
		self.assertEqual(["manual.williams.terminator-2-judgment-day.1991", "vpx-table.t2-vpw-0022", "vpx-script.t2-vpw-0022"], lamps[52]["spatial"]["placements"][0]["provenance"]["source_refs"])
		for device in [*self.definition["inputs"], *self.definition["outputs"]]:
			for item in device.get("spatial", {}).get("placements", []):
				self.assertIn("vpx-table.t2-vpw-0022", item["provenance"]["source_refs"])
				self.assertLessEqual(len(str(item["x"]).split(".")[-1]), 6)

	def test_audit_is_separate_fail_closed_evidence(self) -> None:
		self.assertEqual("pinmame-spatial-blockers", self.audit["format"])
		self.assertTrue(self.audit["extraction"]["fail_closed"])
		self.assertEqual("f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9", self.audit["extraction"]["manifest_sha256"])
		self.assertEqual("external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json", self.audit["extraction"]["manifest_uri"])
		self.assertIn("sorted relative POSIX path", self.audit["extraction"]["manifest_algorithm"])
		self.assertIn("GI string geometry/routing", json.dumps(self.audit["unresolved"]))
		self.assertEqual([
			{"kind": "spatial", "scope": "solenoid/effect geometry", "addresses": [12]},
			{"kind": "spatial", "scope": "GI string geometry/routing", "addresses": [0, 1, 4], "group": "pinmame.output.gi"},
		], self.audit["unresolved"])
		self.assertIn("Light2", self.audit["candidate_geometry"]["excluded_graphical_objects"])
		sources = {item["id"]: item for item in self.definition["sources"]}
		manual = sources["manual.williams.terminator-2-judgment-day.1991"]
		self.assertEqual("8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b", manual["sha256"])
		self.assertEqual("Terminator 2 Judgement Day Operations Manual.pdf", manual["original_filename"])
		self.assertEqual({
			"excerpt.t2.switch-matrix", "excerpt.t2.solenoid-table-01-08", "excerpt.t2.solenoid-table-09-16",
			"excerpt.t2.solenoid-table-flashers-gi", "excerpt.t2.lamp-matrix", "excerpt.t2.lamp-schematic",
			"excerpt.t2.major-mechanisms-map", "excerpt.t2.cannon-platform-assembly",
		}, {excerpt["id"] for excerpt in manual["excerpts"]})
		self.assertTrue(all("scanned page rendered at its native resolution" in excerpt["image_derivation"] for excerpt in manual["excerpts"]))
		self.assertTrue(all("pdftoppm" not in excerpt["image_derivation"] for excerpt in manual["excerpts"]))
		self.assertEqual("3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c", sources["vpx-table.t2-vpw-0022"]["sha256"])
		self.assertEqual("b5153ac46f6d4b58afb676c1f7bfdff17c6ffb953941daed8dd841c679f4e831", sources["vpx-script.t2-vpw-0022"]["sha256"])
		self.assertEqual("https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Terminator%202%20%28Williams%201991%29.vbs", sources["vpx-script.t2-modern-comparison"]["uri"])

	def test_curator_check_is_clean(self) -> None:
		environment = {**__import__("os").environ, "PYTHONPATH": "src"}
		result = subprocess.run([sys.executable, "tools/curate_terminator_2.py", "--check"], cwd=ROOT, env=environment, capture_output=True, text=True)
		self.assertEqual(0, result.returncode, result.stdout + result.stderr)

	def test_retained_extraction_manifest_recomputes_every_file(self) -> None:
		source_root_value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not source_root_value:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		source_root = Path(source_root_value)
		extraction_root = source_root / "williams/terminator-2-judgment-day-1991/extracted-vpxtool"
		manifest_path = source_root / "williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json"
		actual = load(manifest_path)
		paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
		expected_files = []
		for path in paths:
			digest = hashlib.sha256()
			with path.open("rb") as stream:
				for block in iter(lambda: stream.read(1024 * 1024), b""):
					digest.update(block)
			expected_files.append({
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": digest.hexdigest(),
			})
		self.assertEqual({"format": "pinmame-vpx-extraction-manifest", "version": 1, "files": expected_files}, actual)
		canonical = (json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
		self.assertEqual("f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9", hashlib.sha256(canonical).hexdigest())
		self.assertEqual(548, len(actual["files"]))
		self.assertEqual(132477924, sum(item["size"] for item in actual["files"]))



class Terminator2SolenoidFlasherTestEvidence(unittest.TestCase):
	"""Each test step ties a printed name to the address that pulsed; the raw run is checked when retained."""

	PATH = ROOT / "evidence" / "runtime" / "wpc-alpha" / "terminator-2-t2_l8-solenoid-flasher-tests.json"
	SCENARIO = ROOT / "tools" / "harness-scenarios" / "wpc-alpha" / "t2-solenoid-flasher-tests.json"
	LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"

	def test_the_rom_names_and_pulses_12_and_24(self) -> None:
		import hashlib
		import os

		evidence = json.loads(self.PATH.read_text(encoding="utf-8"))
		self.assertEqual(["t2_l8"], evidence["driver_ids"])
		runtime = evidence["runtime"]
		self.assertEqual(self.LIBRARY_SHA256, runtime["emulator"]["sha256"])
		(raw,) = runtime["raw_runs"]
		self.assertEqual(hashlib.sha256(self.SCENARIO.read_bytes()).hexdigest(), raw["scenario_sha256"])
		self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
		actions = runtime["observations"]["named_action_observations"]
		pulsed = [item["transitioned_solenoid_addresses"] for item in actions]
		self.assertEqual([[n] for n in range(1, 15)] + [[17]] + [[n] for n in range(18, 28)] + [[17]], pulsed)
		by_address = {item["transitioned_solenoid_addresses"][0]: item["label"] for item in actions}
		self.assertIn("prints KNOCK DOWN", by_address[12])
		self.assertIn("prints F.L. C. BACKGLASS", by_address[24])
		texts = {item["label"]: item["interpreted_text"] for item in runtime["observations"]["diagnostic_snapshots"]}
		self.assertEqual("KNOCK DOWN / T.4 12 REPEAT / BRN-YEL VIO-ORN", texts["T.4 SOLENOID TEST at solenoid 12"])
		self.assertEqual("F.L. C. BACKGLASS / T.5 24 REPEAT / BLU-GRY RED-WHT", texts["T.5 FLASHER TEST at flasher 24"])
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		import build_external_evidence_manifest as manifest

		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		digest = manifest.check_manifest(path.parent, "t2_l8")
		self.assertIn(f"t2_l8/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
		run = json.loads(path.read_text(encoding="utf-8"))
		self.assertIsNone(run["failure"])
		self.assertEqual(self.LIBRARY_SHA256, run["library_sha256"])
		# The summary and the raw run agree on driver, library and scenario.
		self.assertEqual("t2_l8", run["game"])
		self.assertEqual(runtime["game"], run["game"])
		self.assertEqual(runtime["emulator"]["sha256"], run["library_sha256"])
		self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
		steps = {step["label"]: step for step in run["steps"]}
		for label, address in (("solenoid test up to 12", 12), ("flasher test up to 24", 24)):
			fired = {item["number"] for item in steps[label]["transitions"]["solenoids"] if any(item["states"])}
			self.assertEqual({address}, fired, label)
		raw_frames = {snap["label"]: (snap["displays"][0]["pixel_sha256"], snap["displays"][0]["nonzero_pixels"]) for snap in run["snapshots"] if snap["displays"]}
		summary = {item["label"]: (item["pixel_sha256"], item["nonzero_pixels"]) for item in runtime["observations"]["diagnostic_snapshots"]}
		# Every summary frame is the raw frame of the step it names.
		raw_label = {
			"game identification": "Enter 2 (game identification)",
			"T.4 SOLENOID TEST at solenoid 11": "solenoid test up to 11",
			"T.4 SOLENOID TEST at solenoid 12": "solenoid test up to 12",
			"T.4 SOLENOID TEST at solenoid 13": "solenoid test up to 13",
			"T.5 FLASHER TEST started at flasher 17 (name line dimmed mid-blink)": "Enter 6 (start T.5 at flasher 17)",
			"T.5 FLASHER TEST wrapped back to flasher 17 (name and number in their blink-off phase)": "flasher test up, wrapping to 17",
			"T.5 FLASHER TEST at flasher 23": "flasher test up to 23",
			"T.5 FLASHER TEST at flasher 24": "flasher test up to 24",
			"T.5 FLASHER TEST at flasher 25": "flasher test up to 25",
		}
		self.assertEqual(set(raw_label), set(summary))
		for label, frame in summary.items():
			self.assertEqual(raw_frames[raw_label[label]], frame, label)


if __name__ == "__main__":
	unittest.main()
