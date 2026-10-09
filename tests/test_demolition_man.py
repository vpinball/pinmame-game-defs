from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_demolition_man as curator  # noqa: E402
import demolition_man_runtime_evidence as evidence_tool  # noqa: E402
import demolition_man_spatial_seed as seed_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "demolition-man-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "demolition-man-1994.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "demolition-man-1994-spatial.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-dcs"
SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "wpc-dcs"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "williams.demolition-man.1994"

DRIVER_IDS = {
	"dm_lx4", "dm_dx4", "dm_lx4c", "dm_lx3", "dm_dx3", "dm_la1", "dm_da1", "dm_h5", "dm_dh5", "dm_h5b", "dm_dh5b",
	"dm_h6", "dm_h6b", "dm_h6c", "dm_pa2", "dm_pa3", "dm_px5", "dm_px6", "dm_dt099", "dm_dt101",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {28, 37, 68, 75}
# Every halftone 'Opto Switch' cell of the Switch Matrix page (excerpt switch-matrix.md), listed independently of the mask.
SHADED_CELLS = {31, 32, 33, 34, 35, 36, 71, 72, 73, 74, 25, 26, 76, 67}
# src/wpc/sims/wpc/full/dm.c dmGameData inverted-switch mask at the pinned revision (index 0 is the coin door).
DM_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x30, 0x3F, 0x00, 0x00, 0x40, 0x2F, 0x00, 0x00, 0x00, 0x00)
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "63759f135cb709df5908c8014b851822ba09fd16a9e6858d9e39d7255c7364f9"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


class DemolitionManTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("williams.demolition-man.1994", 1994, 662, "50028"), (machine["id"], machine["year"], machine["ipdb_id"], machine["model_number"]))
		self.assertEqual("pinmame.wpc-dcs", self.definition["controller"]["platform"])
		self.assertEqual("0x10", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load(ROOT / "catalog" / "pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver.get("machine_id") == machine["id"]}
		self.assertEqual(DRIVER_IDS, claimed)
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"dm_dt099", "dm_dt101"}, {key for key, value in compatibility.items() if value == "compatible"})
		self.assertEqual({"dm_pa2", "dm_pa3", "dm_px5", "dm_px6"}, {key for key, value in compatibility.items() if value == "unknown"})
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		groups: dict[str, list[int]] = {}
		for item in self.definition["inputs"] + self.definition["outputs"]:
			groups.setdefault(item["binding"]["group"], []).append(item["binding"]["device"])
		for group, addresses in groups.items():
			self.assertEqual(len(addresses), len(set(addresses)), group)
		switches = set(groups["pinmame.input.switch"])
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), switches)
		self.assertEqual(set(range(1, 9)), set(groups["pinmame.input.dip"]))
		self.assertEqual(set(range(1, 59)), set(groups["pinmame.output.solenoid"]))
		self.assertEqual(MATRIX_ADDRESSES, set(groups["pinmame.output.lamp"]))
		self.assertEqual(set(range(5)), set(groups["pinmame.output.gi"]))
		unused = {address for address in MATRIX_ADDRESSES if self.device("input.switch", address)["availability"] == "unused"}
		self.assertEqual(UNUSED_MATRIX_ADDRESSES, unused)

	def test_inverted_switch_mask_is_exactly_the_shaded_opto_cells(self) -> None:
		masked = {address for address in MATRIX_ADDRESSES if DM_INVERTED_SWITCH_MASK[sw2m(address) // 8] & (1 << (sw2m(address) % 8))}
		self.assertEqual(SHADED_CELLS, masked)
		self.assertEqual(SHADED_CELLS, set(curator.OPTO_SWITCHES))
		source = ROOT.parent / "pinmame"
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			switch = self.device("input.switch", address)
			expected = address in SHADED_CELLS or address == 24
			self.assertEqual(expected, switch["normally_closed"], address)
			self.assertEqual("opto" if address in SHADED_CELLS else switch["physical"]["switch_type"], switch["physical"]["switch_type"], address)
		self.assertTrue(all(self.device("input.switch", address)["physical"]["switch_type"] == "opto" for address in SHADED_CELLS))
		del source

	def test_flipper_column_reflects_the_rom_run(self) -> None:
		for address in (112, 114, 118):
			button = self.device("input.switch", address)
			self.assertEqual("used", button["availability"])
			self.assertFalse(button["normally_closed"])
			self.assertIn("fire", button["physical"]["notes"])
		for address in (115, 116):
			self.assertEqual("unused", self.device("input.switch", address)["availability"])
		for address in (111, 113, 117):
			self.assertIn("synthesizes", self.device("input.switch", address)["physical"]["notes"])
		# core.c synthesizes an end-of-stroke bit only through FLIP_EOS, which FLIP_SOL supplies; dmGameData has no FLIP_SOL(FLIP_UR).
		self.assertIn("does not synthesize", self.device("input.switch", 115)["physical"]["notes"])
		self.assertNotIn("from public 33", self.device("input.switch", 115)["physical"]["notes"])
		self.assertEqual("magnet", self.device("output.solenoid", 33)["kind"])
		self.assertEqual("unused", self.device("output.solenoid", 34)["availability"])
		self.assertEqual({35, 36, 45, 46, 47, 48}, {address for address in range(33, 49) if self.device("output.solenoid", address)["kind"] == "coil" and self.device("output.solenoid", address)["availability"] == "used"})

	def test_auxiliary_flashers_publish_at_the_custom_range(self) -> None:
		for public, printed in zip(range(51, 59), range(37, 45)):
			flasher = self.device("output.solenoid", public)
			self.assertEqual("flasher", flasher["kind"])
			self.assertIn({"namespace": "manual.address", "value": str(printed)}, flasher["aliases"])
			self.assertIn(f"T.5 {printed}", flasher["physical"]["notes"].replace(f"number {printed}", f"T.5 {printed}"))
			self.assertEqual("unused", self.device("output.solenoid", printed)["availability"])
			self.assertEqual("virtual", self.device("output.solenoid", printed)["kind"])
		self.assertEqual(2, self.device("output.solenoid", 55)["physical"]["quantity"])

	def test_state_channels_and_unused_drivers(self) -> None:
		for address in (29, 30, 31):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]))
		self.assertEqual("unused", self.device("output.solenoid", 32)["availability"])
		for address in (6, 8, 16):
			self.assertEqual("unused", self.device("output.solenoid", address)["availability"])
			self.assertIn("NOT USED", self.device("output.solenoid", address)["physical"]["notes"])
		self.assertEqual({18, 19, 20}, {address for address in range(1, 29) if self.device("output.solenoid", address)["kind"] == "motor"})

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f'"{name}"' if address not in UNUSED_MATRIX_ADDRESSES else "'NOT USED'", self.device("input.switch", address)["physical"]["notes"], address)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(name, self.device("output.lamp", address)["physical"]["notes"], address)
		for address, (_test, name, _number, wires) in curator.ROM_OUTPUT_NAMES.items():
			notes = self.device("output.solenoid", address)["physical"]["notes"]
			self.assertIn(name, notes, address)
			self.assertIn(wires, notes, address)
		self.assertEqual(evidence_tool.EDGE_NAMES, curator.ROM_SWITCH_NAMES)
		self.assertEqual(evidence_tool.LAMP_NAMES, curator.ROM_LAMP_NAMES)

	def test_mechanisms_and_relationships_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		ids = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		self.assertTrue({"mechanism.cryoclaw", "mechanism.elevator", "mechanism.right-ramp-diverter", "mechanism.ball-trough"} <= ids)
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"]) | set(mechanism["sensors"]) <= known, mechanism["id"])
		claw = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.cryoclaw")
		self.assertEqual({"device.claw-motor-left", "device.claw-motor-right", "device.claw-magnet"}, set(claw["actuators"]))
		pairs = {(item["source"], item["destination"]) for item in self.definition["relationships"]}
		self.assertEqual(
			{("switch.matrix-41", "device.left-slingshot"), ("switch.matrix-42", "device.right-slingshot"), ("switch.matrix-44", "device.top-slingshot"),
			 ("switch.matrix-43", "device.left-jet-bumper"), ("switch.matrix-45", "device.right-jet-bumper")},
			pairs,
		)

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
				paths.add(path.name)
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], sha256(ROOT / excerpt["image"]), excerpt["id"])
					paths.add(Path(excerpt["image"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)

	def test_placements_are_in_range_unique_and_from_the_seed(self) -> None:
		seed = load(SEED_PATH)
		placement_ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			self.assertIn(spatial["status"], {"observed", "validated"}, item["id"])
			for placement in spatial["placements"]:
				placement_ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				self.assertEqual(placement["x"], round(placement["x"], 6))
		self.assertEqual(len(placement_ids), len(set(placement_ids)))
		self.assertEqual(2, len(self.device("output.lamp", 11)["spatial"]["placements"]))
		self.assertEqual(2, self.device("output.lamp", 82)["physical"]["quantity"])
		self.assertEqual(seed["table"]["sha256"], curator.TABLE_SHA256)
		missing = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"] if item.get("availability") == "used" and "spatial" not in item}
		self.assertEqual({"gi.string-1", "lamp.matrix-71", "lamp.matrix-72", "lamp.matrix-73", "device.claw-flasher", "device.elevator-2-flasher", "device.elevator-1-flasher"}, missing)

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		import drawing_callouts

		seed = load(ROOT / "tools/seeds/williams/demolition-man-1994-callouts.json")
		self.assertEqual("williams.demolition-man.1994", seed["machine_id"])
		statuses = {placement["id"]: placement["provenance"]["status"] for item in self.definition["inputs"] + self.definition["outputs"] for placement in (item.get("spatial") or {}).get("placements") or []}
		self.assertEqual(set(statuses), set(seed["checks"]) | set(seed["excluded_checks"]))
		self.assertFalse(set(seed["checks"]) & set(seed["excluded_checks"]))
		raw = {pid: (0.0, 0.0) for pid in statuses}
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements") or []:
				raw[placement["id"]] = (placement["x"], placement["y"])
		decisions = drawing_callouts.evaluate(seed, raw, seed["limit"])
		for pid, status in statuses.items():
			expected = "validated" if decisions["placements"].get(pid, {}).get("agrees") else "observed"
			self.assertEqual(expected, status, pid)
		self.assertEqual(111, sum(status == "validated" for status in statuses.values()))
		for pid in seed["excluded_checks"]:
			self.assertEqual("observed", statuses[pid], pid)

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_scenarios_name_no_game_and_runtime_evidence_pins_its_runs(self) -> None:
		for filename, builder in evidence_tool.BUILDERS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			run = document["runtime"]["raw_runs"][0]
			scenario = SCENARIO_DIRECTORY / f"{run['name']}.json"
			self.assertEqual(run["scenario_sha256"], sha256(scenario), filename)
			self.assertNotIn("dm_", scenario.read_text(encoding="utf-8"), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"])
			self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		for filename, builder in evidence_tool.BUILDERS.items():
			self.assertEqual(canonical_bytes(builder(root)), (RUNTIME_DIRECTORY / filename).read_bytes(), filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_runtime_evidence_refuses_an_altered_or_missing_frame(self) -> None:
		import shutil
		import tempfile

		source = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / "dm-claw-test"
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			copy = root / evidence_tool.HARNESS_DIRECTORY / "dm-claw-test"
			shutil.copytree(source, copy)
			frame = sorted((copy / "dmd").glob("*.pgm"))[-1]
			data = bytearray(frame.read_bytes())
			data[-1] ^= 0xFF
			frame.write_bytes(bytes(data))
			with self.assertRaises(ValueError):
				evidence_tool.build_claw_test(root)
			frame.unlink()
			with self.assertRaises(ValueError):
				evidence_tool.build_claw_test(root)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_and_placement_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		table = root / "williams/demolition-man-1994/source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = root / "williams/demolition-man-1994/source/Demolition Man (Knorr-Kiwi) 1.3.1.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		text = script.read_text(encoding="latin-1")
		self.assertIn('Const cGameName = "dm_lx4"', text)
		self.assertIn('SolModCallback(51) = "Flash137"', text)
		self.assertIn("NFadeLm 82,  l83", text)

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_matches_its_pin(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.MACHINE_ID / "ipdb-662"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))
		self.assertEqual(curator.PARTS_LIST_SHA256, sha256(root / curator.PARTS_LIST_NAME))
		self.assertEqual(curator.IPDB_PAGE_SHA256, sha256(root / "ipdb-662-page-wayback.html.gz"))


if __name__ == "__main__":
	unittest.main()
