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

MACHINE_ID = "bally.the-shadow.1994"
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "the-shadow-1994.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "the-shadow-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "the-shadow-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "the-shadow-1994.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "the-shadow-1994.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

DRIVER_IDS = {
	"ts_lx5", "ts_dx5", "ts_lh6", "ts_lh6p", "ts_dh6", "ts_la6", "ts_da6", "ts_lf6", "ts_df6", "ts_lm6", "ts_dm6",
	"ts_lx4", "ts_dx4", "ts_la4", "ts_da4", "ts_lf4", "ts_la2", "ts_da2", "ts_pa1", "ts_pa2",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# tsGameData's inverted-switch mask as printed in src/wpc/sims/wpc/prelim/ts.c.
INVERTED_MASK = (0x00, 0x00, 0x00, 0xE7, 0x7F, 0x00, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00)
# Cells printed with the opto shading on the switch matrix (printed 2-40).
PRINTED_SHADED = {31, 32, 33, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 85, 86, 87, 88}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_xy(device: dict) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


def mask_addresses(mask: tuple[int, ...]) -> set[int]:
	return {column * 10 + bit + 1 for column, value in enumerate(mask) for bit in range(8) if value >> bit & 1}


class TheShadowTests(unittest.TestCase):
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
		self.assertEqual((MACHINE_ID, "The Shadow", "Bally", 1994), (machine["id"], machine["name"], machine["manufacturer"], machine["year"]))
		self.assertEqual((2528, "G4jPX-M85YZ", "physical_pinball"), (machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_catalog_maps_all_twenty_drivers_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(DRIVER_IDS, mapped)
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual({"ts_pa1", "ts_pa2"}, {driver_id for driver_id, driver in drivers.items() if driver["physical_compatibility"] == "compatible"})

	def test_the_full_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		self.assertEqual({83, 117, 118}, {address for address, device in self.switches.items() if device["availability"] == "unused"})

	def test_opto_polarity_matches_the_re_derived_pinmame_mask(self) -> None:
		normalized = mask_addresses(INVERTED_MASK)
		self.assertEqual(PRINTED_SHADED, normalized)
		closed = {address for address, device in self.switches.items() if address in MATRIX_ADDRESSES and device.get("normally_closed")}
		self.assertEqual(normalized, closed)
		self.assertEqual(normalized, {address for address, device in self.switches.items() if device.get("physical", {}).get("switch_type") == "opto" and address < 100})

	def test_cabinet_buttons(self) -> None:
		self.assertEqual(["cabinet.launch"], self.switches[11]["roles"])
		self.assertEqual(["cabinet.action"], self.switches[12]["roles"])
		self.assertEqual(["cabinet.action"], self.switches[34]["roles"])
		for address in (11, 12, 13, 23, 34):
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"], address)
		self.assertIn("Phurba", self.switches[34]["physical"]["notes"])

	def test_always_closed_switch(self) -> None:
		device = self.switches[24]
		self.assertEqual("constant", device["kind"])
		self.assertTrue(device["constant_active"])
		self.assertIn("table quirk", device["physical"]["notes"])

	def test_dip_bank_follows_the_printed_country_chart(self) -> None:
		self.assertIn("America Off", self.dips[1]["physical"]["notes"])
		self.assertIn("Euopean Off", self.dips[6]["physical"]["notes"])
		self.assertIn("Spain Off", self.dips[5]["physical"]["notes"])

	def test_the_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 52)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gis))
		kinds = {address: device["kind"] for address, device in self.solenoids.items()}
		self.assertEqual({19, 20}, {address for address, kind in kinds.items() if kind == "motor"})
		self.assertEqual({35}, {address for address, kind in kinds.items() if kind == "magnet"})
		self.assertEqual({17, 18, 21, 22, 23, 26, 27, 28}, {address for address, kind in kinds.items() if kind == "flasher"})
		unused = {address for address, device in self.solenoids.items() if device["availability"] == "unused"}
		self.assertEqual({32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, unused)
		self.assertEqual("virtual", self.solenoids[51]["kind"])
		self.assertIn("mechanics bit 1", self.solenoids[51]["physical"]["notes"])
		self.assertEqual(set(), {address for address, device in self.lamps.items() if device["availability"] != "used"})

	def test_each_board_transistor_drives_one_output(self) -> None:
		seen: dict[tuple[str, str], int] = {}
		for address, device in self.solenoids.items():
			wiring = device.get("wiring", {})
			if "driver_transistor" not in wiring:
				continue
			key = (wiring["board"], wiring["driver_transistor"])
			self.assertNotIn(key, seen, f"{key} on {seen.get(key)} and {address}")
			seen[key] = address
		self.assertEqual("Q1", self.solenoids[35]["wiring"]["driver_transistor"])
		self.assertEqual("Q5", self.solenoids[36]["wiring"]["driver_transistor"])

	def test_fliptronic_upper_left_circuits_drive_the_magnet_and_knock_down(self) -> None:
		self.assertEqual("J902-3", self.solenoids[35]["wiring"]["control_connection"])
		self.assertEqual("J902-1", self.solenoids[36]["wiring"]["control_connection"])
		for address in (35, 36):
			self.assertIn("flipper block prints", self.solenoids[address]["physical"]["notes"])
		self.assertEqual(["flipper.upper.right"], self.solenoids[33]["roles"])

	def test_battlefield_mechanism(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		battlefield = mechanisms["mechanism.battlefield"]
		self.assertEqual("motorized", battlefield["kind"])
		self.assertIn("switch.matrix-37", battlefield["sensors"])
		self.assertIn("switch.matrix-38", battlefield["sensors"])
		self.assertIn("19 alone toward position 18 closing 38", battlefield["behavior"])
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertEqual(set(), set(mechanism["actuators"] + mechanism["sensors"]) - ids, mechanism["id"])
		used = {device["id"] for device in self.solenoids.values() if device["kind"] in {"coil", "motor", "magnet"} and device["availability"] == "used"}
		actuators = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		self.assertEqual(set(), used - actuators)

	def test_backbox_gi_and_lamp_misprints(self) -> None:
		for address in (2, 3):
			self.assertEqual("cabinet_or_service", self.gis[address]["spatial"]["reason"])
		for address in (0, 1, 4):
			self.assertEqual("observed", self.gis[address]["spatial"]["status"])
		# The power driver connector list's reversed J120/J121 wording is disclosed on every string, not silently dropped.
		for device in self.gis.values():
			self.assertIn("printed 3-28", device["physical"]["notes"])
		# The triac switches the return side: the return pin is the control connection, the 6.8VAC pin the supply.
		self.assertEqual(("J121-1 (Playfield)", "Brown", "J121-7 (Playfield)", "Wht-Brn"), tuple(self.gis[0]["wiring"][key] for key in ("control_connection", "control_wire", "power_connection", "power_wire")))
		self.assertEqual(("J120-5 (Backbox)", "Green", "J120-10 (Backbox)", "Wht-Grn"), tuple(self.gis[3]["wiring"][key] for key in ("control_connection", "control_wire", "power_connection", "power_wire")))
		self.assertEqual("Mini Left Standup 3", self.lamps[62]["label"])
		self.assertEqual("Mini Left Standup 2", self.lamps[63]["label"])
		self.assertIn("misprints", self.lamps[62]["physical"]["notes"])

	def test_every_placement_is_observed_and_in_range(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if spatial is None or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("observed", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])

	def test_glow_only_flashers_are_not_placed(self) -> None:
		# F117/F118 are glow images bound only by the older script; the VPW table has no socket object for 17/18.
		for address in (17, 18):
			self.assertNotIn("spatial", self.solenoids[address])
			self.assertIn("glow images", self.solenoids[address]["physical"]["notes"])
		# The ramp-ring lamps' only table objects are the glow sprites F181-F184.
		for address in (81, 82, 83, 84):
			self.assertNotIn("spatial", self.lamps[address])
			self.assertIn("glow sprite", self.lamps[address]["physical"]["notes"])

	def test_derived_placements_are_declared_projections(self) -> None:
		import curate_the_shadow as curator

		report = load_json(SPATIAL_REPORT_PATH)
		declared = {(entry["group"], entry["address"]) for entry in report["projections"]}
		self.assertEqual(set(), set(curator.DERIVED_PLACEMENTS) - declared)

	def test_callback_notes_quote_the_vpw_script(self) -> None:
		for address in (17, 18, 21, 22, 23, 26, 27, 28):
			self.assertIn(f"SolModCallback({address}) = SolFlash{address}", self.solenoids[address]["physical"]["notes"])
		self.assertIn("commented out", self.solenoids[46]["physical"]["notes"])

	def test_geometric_ordering(self) -> None:
		# Outlanes and return lanes on their printed sides.
		for left, right in ((18, 15), (17, 16), (61, 62)):
			self.assertLess(first_xy(self.switches[left])[0], first_xy(self.switches[right])[0])
		# Mini drop targets left to right.
		xs = [first_xy(self.switches[address])[0] for address in (85, 86, 87, 88)]
		self.assertEqual(sorted(xs), xs)
		# Mini left standups at the Battlefield's left edge, mini right standups at its right edge.
		self.assertLess(max(first_xy(self.switches[a])[0] for a in (71, 72, 73, 74)), min(first_xy(self.switches[a])[0] for a in (81, 82, 84)))
		# The Battlefield motor's limit switches bracket the kicker head.
		self.assertLess(first_xy(self.switches[37])[0], first_xy(self.switches[36])[0])
		self.assertLess(first_xy(self.switches[36])[0], first_xy(self.switches[38])[0])

	def test_sources_carry_hashed_reviewed_excerpts_without_local_paths(self) -> None:
		text = json.dumps(self.definition)
		self.assertNotIn("E:/", text)
		self.assertNotIn("C:\\", text)
		excerpts = self.sources["manual.bally.the-shadow.1994.operations-manual"]["excerpts"]
		self.assertEqual(38, len(excerpts))
		for excerpt in excerpts:
			self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest())
			self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest())
			self.assertTrue(excerpt["reviewed"])

	def test_no_other_machine_identifier_leaks_into_the_artifacts(self) -> None:
		catalog = load_json(CATALOG_PATH)
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID}
		artifacts = DEFINITION_PATH.read_text(encoding="utf-8") + KNOWLEDGE_PATH.read_text(encoding="utf-8") + SPATIAL_REPORT_PATH.read_text(encoding="utf-8")
		tokens = {token.lower() for token in re.findall(r"[A-Za-z0-9_]+", artifacts)}
		# Words that happen to be driver ids, each reviewed: English words, the DIP chart's country "America" and
		# the "v1" of the VPW table's file name "VPW Mod v1.0".
		self.assertEqual(set(), tokens & foreign - {"america", "escape", "pinball", "real", "v1"})
		for inherited in ("i500", "Indianapolis", "Turbo Wrench", "Race Track"):
			self.assertNotIn(inherited, artifacts)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_the_shadow as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curator.build())
		self.assertEqual(expected, canonical_bytes(curator.build()))
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())
		curator.check(ROOT)

	def test_curator_refuses_drift(self) -> None:
		import shutil
		import tempfile

		import curate_the_shadow as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			drifted = root / DEFINITION_PATH.relative_to(ROOT)
			drifted.write_bytes(drifted.read_bytes().replace(b"Inner Sanctum", b"Inner Sanctvm", 1))
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_pinned_pinmame_declares_the_game(self) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		candidates = [Path(checkout)] if checkout else []
		working_root = resolve_working_root(ROOT)
		if working_root is not None:
			candidates.append(working_root / "source-checkouts" / "pinmame")
		base = next((path for path in candidates if (path / "src/wpc/sims/wpc/prelim/ts.c").is_file()), None)
		if base is None:
			self.skipTest("pinned PinMAME checkout is not available")
		text = (base / "src/wpc/sims/wpc/prelim/ts.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("{ 0x00, 0x00, 0x00, 0xe7, 0x7f, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00}", text)
		self.assertIn("FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR)", text)
		self.assertIn("19, 20, MECH_LINEAR|MECH_STOPEND|MECH_TWODIRSOL, TS_MINIPFPOS+1, TS_MINIPFPOS-1", text)
		self.assertEqual(DRIVER_IDS, {f"ts_{suffix}" for suffix in re.findall(r"CORE_(?:GAMEDEF|CLONEDEF)\s*\(ts,(\w+)", text)})


class TheShadowRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_the_shadow as curator

		curator.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_retained_tables_scripts_and_claims(self) -> None:
		import curate_the_shadow as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "bally" / "the-shadow-1994"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "vpw-mod-1.0" / "source" / "The Shadow (Bally 1994) VPW Mod v1.0.vpx").read_bytes()).hexdigest())
		script = (root / "vpw-mod-1.0" / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script).hexdigest())
		text = script.decode("latin-1")
		self.assertIn('Const cGameName = "ts_lx5"', text)
		self.assertIn(".InitSw 0, 41, 42, 43, 44, 45, 0, 0", text)
		self.assertIn("bsLock.InitSw 0,63,64,65,0,0,0,0", text)
		self.assertIn('SolCallback(35) = "SolMagnetOn"', text)
		self.assertIn('SolCallback(sURFlipper) = "SolURFlipper"', text)
		self.assertIn("NewKickerPos = Controller.GetMech(0)", text)
		self.assertNotRegex(text, r"(?m)^\s*SolCallback\(15\)")
		self.assertEqual(curator.LEGACY_TABLE_SHA256, hashlib.sha256((root / "source" / "The Shadow (Bally 1994).vpx").read_bytes()).hexdigest())
		legacy = (root / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.LEGACY_SCRIPT_SHA256, hashlib.sha256(legacy).hexdigest())
		self.assertIn("Flash 81, F181", legacy.decode("latin-1"))

	def test_derived_placements_recompute_from_the_extraction(self) -> None:
		import curate_the_shadow as curator

		items = self._root("PINMAME_VPX_SOURCES_ROOT") / "bally" / "the-shadow-1994" / "vpw-mod-1.0" / "extracted-vpxtool" / "gameitems"

		def mesh_center(name: str) -> tuple[float, float]:
			xs: list[float] = []
			ys: list[float] = []
			for line in (items / f"Primitive.{name}.obj").read_text(encoding="utf-8").splitlines():
				if line.startswith("v "):
					_, x, y, *_ = line.split()
					xs.append(float(x))
					ys.append(float(y))
			return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

		def wall_center(name: str) -> tuple[float, float]:
			wall = json.loads((items / f"Wall.{name}.json").read_text(encoding="utf-8"))["Wall"]
			xs = [point["x"] for point in wall["drag_points"]]
			ys = [point["y"] for point in wall["drag_points"]]
			return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

		definition = load_json(DEFINITION_PATH)
		devices = {(d["binding"]["group"], int(d["binding"]["device"])): d for d in definition["inputs"] + definition["outputs"]}
		for key, (method, names) in curator.DERIVED_PLACEMENTS.items():
			centers = [(mesh_center if method == "mesh" else wall_center)(name) for name in names]
			x = sum(c[0] for c in centers) / len(centers) / 975.0
			y = sum(c[1] for c in centers) / len(centers) / 1974.0
			placement = devices[key]["spatial"]["placements"][0]
			self.assertAlmostEqual(x, placement["x"], places=5, msg=str(key))
			self.assertAlmostEqual(y, placement["y"], places=5, msg=str(key))

	def test_retained_manual_hash(self) -> None:
		import curate_the_shadow as curator

		root = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / "bally.the-shadow.1994" / "ipdb-2528"
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256((root / "Manual_Bally_1994_The_Shadow.pdf").read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
