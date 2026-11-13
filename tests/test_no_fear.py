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

import curate_no_fear as curator  # noqa: E402
import no_fear_runtime_evidence as evidence_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "no-fear-dangerous-sports-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "no-fear-dangerous-sports-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "no-fear-dangerous-sports-1995.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "no-fear-dangerous-sports-1995.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-security"
SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "wpc-security"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "williams.no-fear-dangerous-sports.1995"

DRIVER_IDS = {"nf_23x", "nf_23", "nf_23f", "nf_22", "nf_20", "nf_11x", "nf_10f", "nf_101", "nf_08x"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# src/wpc/sims/wpc/prelim/nf.c nfGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
NF_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0xFF, 0xE3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
SCRIPT_SHA256 = "580749d770efe2e887fd92f7d05b3afa7f848f64e9f2736204986353b00817c5"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class NoFearTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(
			("williams.no-fear-dangerous-sports.1995", 2852, 1995, "50025", "Gr2Y2-MDxZq"),
			(machine["id"], machine["ipdb_id"], machine["year"], machine["model_number"], machine["opdb_id"]),
		)
		self.assertEqual(("pinmame.wpc-security", "0x20"), (self.definition["controller"]["platform"], self.definition["controller"]["hardware_generation"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual("nf_23x", self.definition["drivers"][0]["id"])
		self.assertEqual({"nf_08x"}, {k for k, v in drivers.items() if v["physical_compatibility"] == "unknown"})
		self.assertEqual(DRIVER_IDS - {"nf_08x"}, {k for k, v in drivers.items() if v["physical_compatibility"] == "identical"})
		self.assertIn(evidence_tool.IDENTIFICATION.replace("NO FEAR PINBALL / ", ""), drivers["nf_23x"]["variant_notes"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 51)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		unscanned = {column * 10 + row for column in (7, 8) for row in range(1, 9)}
		self.assertEqual({12, 36, 43, 44, 45, 52, 53, 65, 68, 117} | unscanned, {a for a, s in self.switches.items() if s["availability"] == "unused"})
		self.assertEqual(set(evidence_tool.UNSCANNED), unscanned)
		self.assertEqual({4}, {a for a, s in self.switches.items() if s["availability"] == "optional"})
		self.assertEqual({9, 13, 32, 35, 36, *range(37, 45), 49, 50}, {a for a, c in self.coils.items() if c["availability"] == "unused"})
		self.assertEqual({29, 30, 31}, {a for a, c in self.coils.items() if c["kind"] == "virtual" and c["availability"] == "used"})
		self.assertEqual({58}, {a for a, lamp in self.lamps.items() if lamp["availability"] == "unused"})

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (NF_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(set(curator.MASKED_SWITCHES), inverted)
		self.assertEqual(inverted, set(evidence_tool.PINMAME_MASKED))
		# The matrix shades all of columns 3 and 4; 43-45 are unused positions PinMAME's mask leaves alone.
		self.assertEqual(curator.SHADED_SWITCHES - {112, 114, 116, 118} - {43, 44, 45}, inverted)
		for address in inverted - {36}:
			self.assertTrue(self.switches[address]["normally_closed"], address)
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
		for address in set(self.switches) - (inverted - {36}) - {24}:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])
		self.assertEqual("unused", self.switches[36]["availability"])

	def test_fliptronic_column_roles(self) -> None:
		self.assertEqual(["flipper.lower.right.button"], self.switches[112]["roles"])
		self.assertEqual(["flipper.upper.right.button"], self.switches[116]["roles"])
		self.assertEqual(["flipper.lower.left.button"], self.switches[114]["roles"])
		self.assertEqual(["flipper.lower.left.button"], self.switches[118]["roles"])
		self.assertIn("writes 112 and 116 together", self.switches[116]["physical"]["notes"])
		self.assertIn("writes 114 and 118 together", self.switches[118]["physical"]["notes"])
		self.assertEqual(set(evidence_tool.SYNTHESIZED), {111, 113, 115})
		for address in evidence_tool.SYNTHESIZED:
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"], address)
		self.assertIn("J906-5 N/C", self.switches[117]["physical"]["notes"])
		self.assertEqual(set(evidence_tool.FLIPPER_FIRES), set(curator.FLIPPER_FIRES))
		for address, fired in evidence_tool.FLIPPER_FIRES.items():
			text = curator.FLIPPER_FIRES[address]
			self.assertEqual(fired, {int(number) for number in re.findall(r"\d+", text)}, address)
			self.assertIn(f"fired {text}", self.switches[address]["physical"]["notes"], address)
		for address in (112, 114, 116, 118):
			rom_name = evidence_tool.FLIPPER_EDGES[address][2]
			self.assertIn(f"'{rom_name}'", self.switches[address]["physical"]["notes"], address)
		flippers = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(["switch.generic-115", "switch.generic-116"], flippers["mechanism.upper-right-flipper"]["sensors"])
		self.assertIn("switch.generic-118", flippers["mechanism.lower-left-flipper"]["sensors"])

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			if address == 24:
				continue
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual(curator.ROM_SWITCH_NAMES, {k: v for k, v in evidence_tool.EDGE_NAMES.items() if v != "UNUSED"})
		self.assertEqual(curator.UNUSED_NAMED, frozenset(k for k, v in evidence_tool.EDGE_NAMES.items() if v == "UNUSED"))
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES}, evidence_tool.T4_NAMES)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual({number: (name, wires) for number, name, wires, _ in evidence_tool.T12_ORDER}, {
			{45: 1, 46: 2, 47: 3, 48: 4, 33: 5, 34: 6}[a]: v for a, v in curator.ROM_SOLENOID_NAMES.items() if a in curator.T12_ADDRESSES
		})
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})
		self.assertEqual(curator.ROM_LAMP_NAMES, evidence_tool.LAMP_NAMES)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f'names it "{name}"', self.lamps[address]["physical"]["notes"], address)
		for string, _label, text, _presses in evidence_tool.GI_STRINGS:
			name, _, wires = text.split(" / ")
			self.assertIn(f"names it '{name}' ({wires})", self.gi[string]["physical"]["notes"], string)

	def test_outputs_kinds_and_cabinet_roles(self) -> None:
		self.assertEqual(set(range(17, 29)), {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual({3, 5, 6}, {a for a, c in self.coils.items() if c["kind"] == "magnet"})
		self.assertEqual({17: 2, 18: 1, 19: 1, 20: 3, 21: 3, 22: 1, 23: 3, 24: 1, 25: 2, 26: 1, 27: 1, 28: 1}, {a: self.coils[a]["physical"]["quantity"] for a in range(17, 29)})
		for address in (7, 9, 13, 22, 26, 27):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		self.assertEqual(["cabinet.knocker"], self.coils[7]["roles"])
		for address in (35, 36):
			self.assertEqual("unused", self.coils[address]["availability"], address)
			self.assertIn("THE UPPER LEFT FLIPPER IS NOT USED", self.coils[address]["physical"]["notes"], address)
		self.assertEqual(("device.upper-right-flipper-power", "device.upper-right-flipper-hold"), (self.coils[33]["id"], self.coils[34]["id"]))
		self.assertEqual({86: ["cabinet.launch-button-lamp"], 87: ["cabinet.buy-in"], 88: ["cabinet.start-button-lamp"]}, {a: self.lamps[a]["roles"] for a in (86, 87, 88)})
		self.assertEqual((2, 2), (self.lamps[37]["physical"]["quantity"], self.lamps[48]["physical"]["quantity"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual(["cabinet.backbox"], self.gi[address]["roles"], address)
		for address in range(5):
			self.assertIn("columns are swapped", self.gi[address]["physical"]["notes"], address)
		# Solenoid 19: the legacy settlement is handed to this curator, which keeps the historical trace pinned.
		flasher = self.coils[19]
		self.assertEqual(("device.no-fear-flasher", "No Fear Flasher", "flasher", "used"), (flasher["id"], flasher["label"], flasher["kind"], flasher["availability"]))
		self.assertNotIn({"namespace": "vpe-legacy.coil", "value": "c_game_on"}, flasher["aliases"])
		self.assertIn(curator.FLASHER_HISTORY_SOURCE, flasher["provenance"]["source_refs"])
		history = next(source for source in self.definition["sources"] if source["id"] == curator.FLASHER_HISTORY_SOURCE)
		self.assertEqual(hashlib.sha256((ROOT / history["uri"].removeprefix("internal:")).read_bytes()).hexdigest(), history["sha256"])

	def test_legacy_aliases_are_carried_by_binding(self) -> None:
		seed = load(curator.LEGACY_ALIAS_SEED_PATH)
		self.assertEqual("williams.no-fear-dangerous-sports.1995", seed["machine_id"])
		by_group = {
			"pinmame.input.switch": self.switches, "pinmame.output.solenoid": self.coils, "pinmame.output.lamp": self.lamps,
		}
		count = 0
		for group, addresses in seed["aliases"].items():
			for address, aliases in addresses.items():
				device = by_group[group][int(address)]
				for namespace, value in aliases:
					self.assertIn({"namespace": namespace, "value": value}, device["aliases"], (group, address, value))
					count += 1
		self.assertGreater(count, 250)
		self.assertIn({"namespace": "vpe-legacy.switch", "value": "s_flipper_lower_right"}, self.switches[112]["aliases"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		accelerator = mechanisms["mechanism.ball-accelerator"]
		self.assertEqual([self.coils[a]["id"] for a in (6, 5, 3)], accelerator["actuators"])
		self.assertEqual([f"switch.matrix-{a}" for a in (46, 47, 48)], accelerator["sensors"])
		for label, coil in evidence_tool.ACCELERATOR_PULSES:
			if coil:
				self.assertIn(f"of {label.split()[0]} fired {coil}", accelerator["behavior"], label)
		trough = mechanisms["mechanism.underground-trough"]
		self.assertEqual([self.coils[1]["id"]], trough["actuators"])
		self.assertEqual([f"switch.matrix-{a}" for a in (38, 37, 42, 41)], trough["sensors"])
		self.assertEqual([self.coils[a]["id"] for a in (8, 12)], mechanisms["mechanism.drop-target"]["actuators"])
		self.assertEqual([self.coils[16]["id"]], mechanisms["mechanism.skull"]["actuators"])
		self.assertEqual([self.coils[14]["id"]], mechanisms["mechanism.ball-trough"]["actuators"])
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
			for placement in spatial.get("placements", []):
				cited.update(placement["provenance"]["source_refs"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		self.assertEqual(set(sources), cited | {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE})
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.iterdir()}, excerpts)
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])
		contract = (EXCERPT_DIRECTORY / "vpx-script-contract.md").read_text(encoding="utf-8")
		self.assertIn(SCRIPT_SHA256, contract)
		for snippet in ('Const cGameName = "nf_23x"', 'SolCallback(14)= "ReleaseBall"', 'SolModCallback(19)= "FlashMod119"', "Case 0 : for each xx in GI_Top"):
			self.assertIn(snippet, contract, snippet)
		for path in EXCERPT_DIRECTORY.glob("*.md"):
			self.assertIsNone(re.search(r"[A-Z]:[\\/]", path.read_text(encoding="utf-8")), path.name)

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		candidates = []
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			group = item["binding"]["group"]
			category = {curator.SWITCH_GROUP: "switch", curator.SOLENOID_GROUP: "solenoid", curator.LAMP_GROUP: "lamp", curator.GI_GROUP: "gi"}[group]
			# Light-map sources with no bulb (G.I., flashers, raised lamps) are only candidates; every other placement is observed.
			expected = "candidate" if (category, item["binding"]["device"]) in curator.CANDIDATE_PLACEMENTS else "observed"
			self.assertEqual(expected, spatial["status"], item["id"])
			if item["kind"] == "flasher" or category == "gi":
				self.assertEqual("candidate", expected, item["id"])
			if expected == "candidate":
				candidates.append(item["id"])
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertEqual(expected, placement["provenance"]["status"], placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertLessEqual(len(f"{value:.10f}".rstrip("0").split(".")[1]), 6, placement["id"])
				refs = placement["provenance"]["source_refs"]
				self.assertLessEqual({curator.VPX_TABLE_SOURCE, curator.VPX_SCRIPT_SOURCE}, set(refs), placement["id"])
				self.assertEqual((category, item["binding"]["device"]) in curator.PROJECTED_PLACEMENTS, curator.MANUAL_SOURCE in refs, placement["id"])
			quantity = item.get("physical", {}).get("quantity")
			if quantity is not None and item["kind"] in {"lamp", "flasher"}:
				self.assertGreaterEqual(quantity, len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))
		report = load(SPATIAL_REPORT_PATH)
		self.assertEqual([], report["without_placements"])
		self.assertEqual([], report["placement_status"]["validated"])
		self.assertEqual(
			{("gi", 0), ("gi", 1), ("gi", 2)} | {("lamp", a) for a in (38, 82, 83, 84, 85)} | {("solenoid", a) for a in (17, 18, 19, 20, 21, 23, 24, 25, 28)},
			set(curator.CANDIDATE_PLACEMENTS),
		)
		self.assertEqual(sorted(candidates), report["placement_status"]["candidate"])
		seed = load(curator.SPATIAL_SEED_PATH)
		self.assertEqual("sw32", seed["switch"]["31"][0]["object"])
		self.assertEqual({"3": "RightMagnet", "5": "CenterMagnet", "6": "LeftMagnet"}, {a: seed["solenoid"][a][0]["object"] for a in ("3", "5", "6")})
		self.assertEqual({"0", "1", "2"}, set(seed["gi"]))
		self.assertNotIn("58", seed["lamp"])
		for address in (86, 87, 88):
			self.assertNotIn(str(address), seed["lamp"])
		# Only fitted playfield devices are placed: no backbox flasher, unfitted driver or cabinet device.
		for address in (7, 9, 13, 22, 26, 27):
			self.assertNotIn(str(address), seed["solenoid"])

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "williams" / "no-fear-dangerous-sports-1995" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		for snippet in (
			'Const cGameName = "nf_23x"', ".HandleMechanics = 0", ".Switch(22) = 1", ".Switch(24) = 1", 'SolCallback(14)= "ReleaseBall"',
			'SolModCallback(19)= "FlashMod119"', "Sub Lmag(Enabled)", "Case 0 : for each xx in GI_Top",
		):
			self.assertIn(snippet, text, snippet)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_every_table_coordinate_recomputes_from_the_retained_gameitems(self) -> None:
		"""Each seed coordinate is its object's own point: a light, kicker, spinner, flipper or trigger centre (a trigger's
		position, not the centroid of its outline), a wall's drag-point centroid, or a hit target's or primitive's position;
		never a Flasher sprite."""
		gameitems = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		by_name = {path.stem.split(".", 1)[1].lower(): path for path in gameitems.glob("*.json")}

		def point(name: str) -> tuple[float, float]:
			path = by_name[name.lower()]
			kind = path.stem.split(".")[0]
			data = json.loads(path.read_text(encoding="utf-8"))[kind]
			if kind in {"Wall", "Rubber"}:
				vertices = [item.get("vertex", item) for item in data["drag_points"]]
				return sum(v["x"] for v in vertices) / len(vertices), sum(v["y"] for v in vertices) / len(vertices)
			if kind in {"Primitive", "HitTarget"}:
				return data["position"]["x"], data["position"]["y"]
			self.assertNotEqual("Flasher", kind, name)
			return data["center"]["x"], data["center"]["y"]

		seed = load(curator.SPATIAL_SEED_PATH)
		checked = 0
		for category in ("switch", "solenoid", "lamp", "gi"):
			for address, entries in seed[category].items():
				for entry in entries:
					x, y = point(entry["object"])
					self.assertAlmostEqual(x / curator.PLAYFIELD_WIDTH, entry["x"], delta=2e-6, msg=(category, address, entry["object"]))
					self.assertAlmostEqual(y / curator.PLAYFIELD_HEIGHT, entry["y"], delta=2e-6, msg=(category, address, entry["object"]))
					checked += 1
		self.assertGreater(checked, 120)

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Catalog driver ids that are ordinary words in this record's prose, and the retained table's version "v1.1.1".
		ordinary_words = {"pinball", "real", "rock", "v1"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"williams.no-fear-dangerous-sports.1995"}
		)
		self.assertIn("corv_21", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_no_fear.py", ROOT / "tools" / "no_fear_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "williams").glob("no-fear-dangerous-sports-1995*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted(SCENARIO_DIRECTORY.glob("nf-*.json")),
			*sorted(EXCERPT_DIRECTORY.glob("*.md")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			self.assertEqual([], found, path.name)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("ball accelerator", "underground trough", "skull", "spatial_placement", "112 and 116", "114 and 118", "0.8X"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (scenario, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = SCENARIO_DIRECTORY / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(evidence_tool.LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(evidence_tool.ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["williams.no-fear-dangerous-sports.1995"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn(f"--handle-mechanics {evidence_tool.MECHANICS} ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
			snapshots = document["runtime"]["observations"]["diagnostic_snapshots"]
			identification = next(item for item in snapshots if item["label"] == evidence_tool.IDENTIFICATION_LABEL)
			self.assertEqual(evidence_tool.IDENTIFICATION, identification["interpreted_text"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual(set(evidence_tool.RUNS), {f"no-fear-nf_23x-{name}.json" for _, name, _ in curator.RUNTIME_SOURCES})
		for source_id, _name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "no-fear-nf_23x-switch-edges.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES - {36}:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		for address in curator.UNUSED_NAMED:
			self.assertTrue(texts[f"{address} -> 1"].startswith("UNUSED"), address)
		for address in curator.UNSCANNED:
			self.assertTrue(texts[f"{address} -> 1"].startswith("SWITCH EDGES / T.1 LAST SW. 68"), address)
		self.assertTrue(texts["117 -> 1"].startswith("SWITCH EDGES"))
		self.assertNotIn("22 -> 1", texts)
		solenoids = load(RUNTIME_DIRECTORY / "no-fear-nf_23x-solenoid-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[a] for a in evidence_tool.T4_ORDER], [item["transitioned_solenoid_addresses"] for item in solenoids])
		flippers = load(RUNTIME_DIRECTORY / "no-fear-nf_23x-flipper-coil-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([sorted(coils) for *_, coils in evidence_tool.T12_ORDER], [item["transitioned_solenoid_addresses"] for item in flippers])
		lamps = load(RUNTIME_DIRECTORY / "no-fear-nf_23x-single-lamps.json")["runtime"]["observations"]["diagnostic_snapshots"]
		self.assertEqual(65, len(lamps))

	def test_every_reading_is_pinned_to_its_frame(self) -> None:
		seed = load(evidence_tool.FRAME_SEED_PATH)
		self.assertEqual(set(evidence_tool.RUNS), set(seed))
		for filename in evidence_tool.RUNS:
			snapshots = load(RUNTIME_DIRECTORY / filename)["runtime"]["observations"]["diagnostic_snapshots"]
			self.assertEqual(seed[filename], {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in snapshots}, filename)
		with self.assertRaises(ValueError):
			observations = {"diagnostic_snapshots": [dict(item) for item in load(RUNTIME_DIRECTORY / "no-fear-nf_23x-ball-accelerator-test.json")["runtime"]["observations"]["diagnostic_snapshots"]]}
			observations["diagnostic_snapshots"][1]["pixel_sha256"] = "0" * 64
			evidence_tool._check_pinned_frames("no-fear-nf_23x-ball-accelerator-test.json", observations)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, evidence_tool.GAME)
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(evidence_tool.MECHANICS, run["handle_mechanics"], filename)
			self.assertIn({"state": 0, "switch": 22}, run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_builders_refuse_transitions_in_the_wrong_direction(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY

		def mutated(directory: str, label: str, channel: str, number: int, states: list[int]) -> dict:
			run = evidence_tool._load_run(root / directory, directory)
			step = next(item for item in run["steps"] if item["label"] == label)
			for item in step["transitions"][channel]:
				if item["number"] == number:
					item["states"] = states
			return run

		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(mutated("nf-single-lamps", "T.8 Up 1", "lamps", 12, [0]))
		with self.assertRaises(ValueError):
			evidence_tool.build_accelerator(mutated("nf-ball-accelerator-test", "46 with all three magnets enabled", "solenoids", 6, [1]))
		with self.assertRaises(ValueError):
			evidence_tool.build_accelerator(mutated("nf-ball-accelerator-test", "46 with all three magnets enabled", "solenoids", 6, [1, 0, 1, 0]))
		with self.assertRaises(ValueError):
			evidence_tool.build_edges(mutated("nf-switch-edges", "112 -> 1", "solenoids", 45, [1]))
		with self.assertRaises(ValueError):
			evidence_tool.build_edges(mutated("nf-switch-edges", "112 -> 0", "solenoids", 46, [1]))
		with self.assertRaises(ValueError):
			evidence_tool.build_trough(mutated("nf-underground-trough-test", "AUTOMATIC: right popper", "solenoids", 1, [0]))
		# An interrupted hold or a release before the switch opens contradicts the T.18 hold observations.
		for label, coil in (("AUTOMATIC: trough eject", 14), ("AUTOMATIC: auto plunger", 2), ("AUTOMATIC: right popper", 1)):
			for states in ([1, 0, 1], [1, 0]):
				with self.subTest(coil=coil, states=states), self.assertRaises(ValueError):
					evidence_tool.build_trough(mutated("nf-underground-trough-test", label, "solenoids", coil, states))

		def skull(coil: int, first: list[int]) -> dict:
			run = evidence_tool._load_run(root / "nf-skull-test", "nf-skull-test")
			for step in run["steps"]:
				if step["label"].startswith("T.19 frame "):
					for item in step["transitions"]["solenoids"]:
						if item["number"] == coil:
							item["states"] = first if step["label"] == "T.19 frame 0" else []
			return run

		# A sustained activation or a single pulse contradicts the T.19 'pulses ... repeatedly' observation.
		for coil in (16, 21):
			for first in ([1], [1, 0]):
				with self.subTest(coil=coil, first=first), self.assertRaises(ValueError):
					evidence_tool.build_skull(skull(coil, first))
		extra = mutated("nf-single-lamps", "T.8 Up 1", "lamps", 12, [1, 0, 1])
		next(item for item in extra["steps"] if item["label"] == "T.8 Up 1")["transitions"]["lamps"].append({"number": 88, "states": [1]})
		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(extra)



if __name__ == "__main__":
	unittest.main()
