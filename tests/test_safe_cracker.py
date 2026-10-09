from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_safe_cracker as curator  # noqa: E402
import drawing_callouts  # noqa: E402
import safe_cracker_runtime_evidence as evidence_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "safe-cracker-1996.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "safe-cracker-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "safe-cracker-1996.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "safe-cracker-1996.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-95"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.safe-cracker.1996"

DRIVER_IDS = {"sc_18s11", "sc_18n11", "sc_18s2", "sc_18ns2", "sc_17", "sc_17n", "sc_14", "sc_10", "sc_091", "sc_18pfx"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
AUX_LAMP_ADDRESSES = {column * 10 + row for column in range(9, 15) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 38, 87, 88}
# src/wpc/sims/wpc/prelim/sc.c scGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
SC_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x7F, 0x06, 0xE0, 0x3F, 0x3F, 0x00, 0x00, 0x00, 0x00)
SCRIPT_SHA256 = "e224e815280ce8e74ec1d2dfe1562dee9e5675b3f379cb5031ff69c39007fa0a"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "e3a65641cb5957e11354aa7a538325849aeff672d4e80d98e7fd08b71d38ebdc"
# Objects whose seed coordinate is the world-space mesh centre of a baked primitive (vpxtool OBJ export), not a gameitem field.
BAKED_OBJECTS = {"bankleftlamp", "bankrightlamp", "cellarlamp", "rooflamp", "pdisc1"}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class SafeCrackerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def _placement(self, placement_id: str) -> dict:
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				if placement["id"] == placement_id:
					return placement
		raise AssertionError(placement_id)

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.safe-cracker.1996", 3782, 1996, "90003", "GRBxq-MJpOP"), (machine["id"], machine["ipdb_id"], machine["year"], machine["model_number"], machine["opdb_id"]))
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			if driver["id"].endswith(("n11", "ns2", "17n")):
				self.assertIn("No Percentaging build removes that limit", driver["variant_notes"], driver["id"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["mechanism_behavior", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 51)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES | AUX_LAMP_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		self.assertEqual(UNUSED_MATRIX_ADDRESSES | {117}, {a for a, s in self.switches.items() if s["availability"] == "unused"})
		self.assertEqual({32, 49, 50}, {a for a, c in self.coils.items() if c["availability"] == "unused"})
		self.assertEqual({4}, {a for a, s in self.switches.items() if s["availability"] == "optional"})

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (SC_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(set(curator.MASKED_SWITCHES), inverted)
		self.assertEqual(inverted, set(evidence_tool.PINMAME_MASKED))
		for address in inverted - {43}:
			self.assertTrue(self.switches[address]["normally_closed"], address)
		# 43 is masked but the ROM treats the closed contact (public 0) as active; 41 is unmasked and rests at public 1.
		self.assertFalse(self.switches[43]["normally_closed"])
		labels = [item["label"] for item in load(RUNTIME_DIRECTORY / "safe-cracker-sc_18s11-switch-edges-sweep.json")["runtime"]["observations"]["named_action_observations"]]
		self.assertTrue(any("names 'TOKN CHUTE EXIT*' on the 1 -> 0 edge" in label for label in labels))
		self.assertFalse(self.switches[41]["normally_closed"])
		self.assertTrue(self.switches[41]["initial_active"])
		self.assertIn("switch mapped backwards", self.switches[41]["physical"]["notes"])
		for address in set(self.switches) - inverted - {24} - UNUSED_MATRIX_ADDRESSES - {117}:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])
		self.assertEqual(curator.SHADED_SWITCHES - {112, 114, 116, 118}, curator.OPTO_SWITCHES)

	def test_fliptronic_column_roles(self) -> None:
		self.assertEqual(["flipper.lower.right.button"], self.switches[112]["roles"])
		self.assertEqual(["flipper.lower.left.button"], self.switches[114]["roles"])
		self.assertEqual(["flipper.upper.right.button"], self.switches[116]["roles"])
		self.assertIn("one press interrupts 112 and 116 together", self.switches[116]["physical"]["notes"])
		self.assertEqual(["cabinet.coin.token"], self.switches[118]["roles"])
		self.assertIn("TOKEN COIN SLOT", self.switches[118]["physical"]["notes"])
		self.assertIn("J13-2", self.switches[118]["physical"]["notes"])
		for address in (111, 113, 115):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"], address)

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			if address in (24, 43):
				continue
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SWITCH_NAMES.items()}, {k: v for k, v in evidence_tool.EDGE_NAMES.items() if v != "UNUSED"})
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES}, evidence_tool.T4_NAMES)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})
		self.assertEqual(curator.ROM_LAMP_NAMES, evidence_tool.LAMP_NAMES)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f'names it "{name}"', self.lamps[address]["physical"]["notes"], address)

	def test_backbox_lamps_follow_the_rom_l_numbering(self) -> None:
		self.assertEqual(curator.AUX_LAMPS, evidence_tool.AUX_LAMP_NAMES)
		for address in AUX_LAMP_ADDRESSES:
			column, row = divmod(address, 10)
			index = (column - 9) * 8 + row - 1
			expected = 24 - index if index < 24 else 48 - (index - 24)
			lamp = self.lamps[address]
			self.assertEqual(f"lamp.backbox-l{expected}", lamp["id"], address)
			self.assertEqual(curator.AUX_LAMPS[address][0], expected, address)
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual(["cabinet.backbox"], lamp["roles"], address)
		self.assertEqual({f"L{n}" for n in range(1, 49)}, {next(a["value"] for a in self.lamps[x]["aliases"] if a["namespace"] == "manual.address") for x in AUX_LAMP_ADDRESSES})
		self.assertIn("L40", self.lamps[131]["physical"]["notes"])

	def test_output_kinds_mirrors_and_backbox_devices(self) -> None:
		self.assertEqual(set(range(17, 25)), {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual("motor", self.coils[26]["kind"])
		self.assertEqual({37, 38, 39, 40}, {a for a, c in self.coils.items() if c["kind"] == "control_signal"})
		for address in (41, 42, 43, 44):
			self.assertEqual(("virtual", "used", ["internal.duplicate.lpdc-mirror"]), (self.coils[address]["kind"], self.coils[address]["availability"], self.coils[address]["roles"]), address)
		for address in (2, 4, 23, 24, 26):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
			self.assertEqual(["cabinet.backbox"], self.coils[address]["roles"], address)
		self.assertEqual({45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34"}, {a: next(x["value"] for x in self.coils[a]["aliases"] if x["namespace"] == "manual.address") for a in (45, 46, 47, 48, 33, 34)})
		self.assertEqual(("device.auto-plunger", "device.lock-up-release"), (self.coils[35]["id"], self.coils[36]["id"]))
		self.assertEqual(2, self.coils[18]["physical"]["quantity"])
		self.assertEqual(2, len(self.coils[18]["spatial"]["placements"]))
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		for address in (21, 22, 23, 24, 25, 26, 27, 28):
			self.assertIn("wiring detail", self.coils[address]["physical"]["notes"], address)

	def test_gi_strings_dim_or_stay_on_as_the_rom_says(self) -> None:
		for address in (0, 1, 2):
			self.assertIn(f"steps its brightness on public GI {address} alone", self.gi[address]["physical"]["notes"], address)
		for address in (3, 4):
			self.assertIn("'ON ONLY'", self.gi[address]["physical"]["notes"], address)
		for address in (1, 3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
		for address in (0, 2):
			self.assertNotIn("spatial", self.gi[address], address)
		self.assertIn("nevertheless dims", self.gi[1]["physical"]["notes"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		banks = {key: (mechanisms[f"mechanism.{key}"]["actuators"], mechanisms[f"mechanism.{key}"]["sensors"]) for key in ("top-left-drop-bank", "top-right-drop-bank", "bottom-left-drop-bank", "bottom-right-drop-bank")}
		self.assertEqual(([self.coils[15]["id"]], [f"switch.matrix-{a}" for a in (61, 62, 63)]), banks["top-left-drop-bank"])
		self.assertEqual(([self.coils[16]["id"]], [f"switch.matrix-{a}" for a in (66, 65, 64)]), banks["top-right-drop-bank"])
		self.assertEqual(([self.coils[27]["id"]], [f"switch.matrix-{a}" for a in (71, 72, 73)]), banks["bottom-left-drop-bank"])
		self.assertEqual(([self.coils[28]["id"]], [f"switch.matrix-{a}" for a in (76, 75, 74)]), banks["bottom-right-drop-bank"])
		token = mechanisms["mechanism.token-dispenser"]
		self.assertEqual([self.coils[4]["id"], self.coils[2]["id"]], token["actuators"])
		self.assertIn("switch.generic-118", token["sensors"])
		self.assertEqual([self.coils[a]["id"] for a in (37, 38, 39, 40)], mechanisms["mechanism.backbox-board-game"]["actuators"])
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
		uncited = {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE}
		self.assertEqual(set(sources), cited | uncited)
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("rendered at its native resolution", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.webp")}, {"switch-locations", "lamp-locations", "solenoid-flasher-locations"})
		for source_id in (curator.VPX_SCRIPT_SOURCE, curator.VPX_SCRIPT_V2_SOURCE):
			self.assertTrue(sources[source_id]["known_working"], source_id)
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertLessEqual(len(f"{value:.10f}".rstrip("0").split(".")[1]), 6, placement["id"])
			quantity = item.get("physical", {}).get("quantity")
			if quantity is not None and item["kind"] in {"lamp", "flasher"}:
				self.assertGreaterEqual(quantity, len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))
		# The jet bumpers pair as the v1.0 script binds them: top 46 on Bumper2, left 44 on Bumper1, right 45 on Bumper3.
		seed = load(curator.SPATIAL_SEED_PATH)
		self.assertEqual({"44": "Bumper1", "45": "Bumper3", "46": "Bumper2"}, {a: seed["switch"][a][0]["object"] for a in ("44", "45", "46")})
		self.assertEqual(("l28", "l27"), (seed["lamp"]["27"][0]["object"], seed["lamp"]["28"][0]["object"]))

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition), seed.get("limit", drawing_callouts.LIMIT))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		validated = {
			placement["id"]
			for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]
			for placement in (item.get("spatial") or {}).get("placements", [])
			if placement["provenance"]["status"] == "validated"
		}
		self.assertEqual(agreeing, validated)
		self.assertGreaterEqual(len(validated), 50)
		self.assertEqual({"2-43", "2-45"}, set(seed["pages"]))
		for key, page in seed["pages"].items():
			self.assertGreaterEqual(len(page["controls"]), 5, key)
			self.assertLessEqual(decisions["pages"][key]["control_loo_max"], 0.02, key)
		self.assertEqual({}, seed["measurements"])
		self.assertEqual(set(), {pid for pid in validated if pid.startswith("lamp.")})
		for pid, reason in seed["excluded_checks"].items():
			self.assertNotIn(pid, seed["checks"])
			self.assertTrue(reason)
		corrected = [read for page in seed["pages"].values() for read in page["reads"] if "verifier_note" in read]
		self.assertEqual({"18", "20"}, {read["label"] for read in corrected})

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Four catalog driver ids are ordinary words in this record's prose: "magic" (magic tokens), "rotation" (the disc's rotation), "real" and "v1" (table v1.0).
		ordinary_words = {"magic", "rotation", "real", "v1"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"bally.safe-cracker.1996"}
		)
		self.assertIn("nbaf_31", forbidden)
		self.assertIn("bally.nba-fastbreak.1997", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_safe_cracker.py", ROOT / "tools" / "safe_cracker_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "bally").glob("safe-cracker-1996*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted((ROOT / "tools" / "harness-scenarios" / "wpc-95").glob("sc-*.json")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			self.assertEqual([], found, path.name)
			self.assertNotIn("Fastbreak", text, path.name)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("token", "board game", "moving (vari) target", "spinning disc", "spatial_placement", "mechanism_behavior", "initial_active", "TOKN CHUTE EXIT"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (_directory, scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-95" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.safe-cracker.1996"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn(f"--handle-mechanics {mechanics} ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id, name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "safe-cracker-sc_18s11-switch-edges-sweep.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES - {43}:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		self.assertTrue(texts["43 -> 0"].startswith("TOKN CHUTE EXIT*"))
		self.assertTrue(texts["43 -> 1"].startswith("SWITCH EDGES"))
		self.assertTrue(texts["118 -> 1"].startswith("TOKEN COIN SLOT"))
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertTrue(texts[f"{address} -> 1"].startswith("UNUSED"), address)
		solenoids = load(RUNTIME_DIRECTORY / "safe-cracker-sc_18s11-solenoid-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[a] for a in evidence_tool.T4_ORDER], [item["transitioned_solenoid_addresses"] for item in solenoids])
		lamps = load(RUNTIME_DIRECTORY / "safe-cracker-sc_18s11-single-lamps.json")["runtime"]["observations"]["diagnostic_snapshots"]
		self.assertEqual(113, len(lamps))

	def test_moving_target_decodes_a_gray_code_and_rests_with_58_open(self) -> None:
		"""The ROM's T.16 readings for every combination of 56 (C), 57 (B) and 58 (A) are the Gray code of 0-7 with A as the least
		significant bit; the manual's Opto 3, broken at the forward-most home position, is wired to row 8, switch 58."""
		decoded = {}
		for filename in ("safe-cracker-sc_18s11-moving-target-test.json", "safe-cracker-sc_18s11-moving-target-codes.json"):
			for item in load(RUNTIME_DIRECTORY / filename)["runtime"]["observations"]["diagnostic_snapshots"]:
				match = re.fullmatch(r'MOVING TARGET TEST (\d) / SWITCH "C" \(#56\) (\w+) / SWITCH "B" \(#57\) (\w+) / SWITCH "A" \(#58\) (\w+) / .*', item["interpreted_text"])
				if match:
					bits = tuple(int(level == "OPEN") for level in match.group(2, 3, 4))
					decoded.setdefault(bits, set()).add(int(match.group(1)))
		gray = {tuple((n ^ (n >> 1)) >> shift & 1 for shift in (2, 1, 0)): {n} for n in range(8)}
		self.assertEqual(gray, decoded)
		mechanism = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.moving-target")
		self.assertIn("at home 58 reads OPEN (public 1)", mechanism["behavior"])
		self.assertNotIn("CLOSED with the target home", mechanism["behavior"])
		self.assertIn("OPTO3's collector to J1-7 White-Gray from J208-9, the matrix's row 8", self.switches[58]["physical"]["notes"])
		self.assertIn("evidence/excerpts/bally.safe-cracker.1996/moving-target-adjustment.md", {excerpt["path"] for source in self.definition["sources"] for excerpt in source.get("excerpts", [])})

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, "sc_18s11")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(mechanics, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_retained_callout_artifacts_match_the_seed(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		checked = drawing_callouts.verify_retained(seed, ROOT, None, Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))
		self.assertGreater(checked, 3)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "safe-cracker-1996" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		for snippet in ('Const cGameName="sc_18"', "Controller.Switch(41) = 1\t'switch mapped backwards", "Sub Bumper2_Hit()", 'SolCallBack(4)  \t\t= "SolTokenRelease ""R"", 81, "', "NFadeL 27, l28"):
			self.assertIn(snippet, text, snippet)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_every_table_coordinate_recomputes_from_the_retained_gameitems(self) -> None:
		"""Each table-derived seed coordinate is its object's own point: a light, kicker, bumper, gate, flipper or plunger
		centre, a trigger's or wall's drag-point centroid, a hit target's or primitive's position, or a flasher sprite's
		position. Baked lamp primitives and the spin disc use the bounding-box centre of their OBJ-export mesh after the primitive's
		object Z rotation and position, recomputed here from the retained export."""
		gameitems = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		by_name = {path.stem.split(".", 1)[1].lower(): path for path in gameitems.glob("*.json")}

		def point(name: str) -> tuple[float, float]:
			path = by_name[name.lower()]
			kind = path.stem.split(".")[0]
			data = json.loads(path.read_text(encoding="utf-8"))[kind]
			if kind in {"Trigger", "Wall"}:
				vertices = [item.get("vertex", item) for item in data["drag_points"]]
				return sum(v["x"] for v in vertices) / len(vertices), sum(v["y"] for v in vertices) / len(vertices)
			if kind in {"Primitive", "HitTarget"}:
				return data["position"]["x"], data["position"]["y"]
			if kind == "Flasher":
				return data["pos_x"], data["pos_y"]
			return data["center"]["x"], data["center"]["y"]

		def mesh_centre(name: str) -> tuple[float, float]:
			path = by_name[name.lower()]
			data = json.loads(path.read_text(encoding="utf-8"))["Primitive"]
			self.assertEqual([1.0, 1.0, 1.0], [data["size"][axis] for axis in "xyz"], name)
			self.assertEqual([0.0] * 8, [abs(value) for value in data["rot_and_tra"][:8]], name)
			angle = math.radians(data["rot_and_tra"][8])
			cos, sin = math.cos(angle), math.sin(angle)
			vertices = [tuple(map(float, line.split()[1:3])) for line in path.with_suffix(".obj").read_text(encoding="utf-8").splitlines() if line.startswith("v ")]
			self.assertGreater(len(vertices), 100, name)
			xs = [x * cos - y * sin + data["position"]["x"] for x, y in vertices]
			ys = [x * sin + y * cos + data["position"]["y"] for x, y in vertices]
			return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

		seed = load(curator.SPATIAL_SEED_PATH)
		checked = 0
		for category in ("switch", "solenoid", "lamp"):
			for address, entries in seed[category].items():
				for entry in entries:
					x, y = (mesh_centre if entry["object"].lower() in BAKED_OBJECTS else point)(entry["object"])
					self.assertAlmostEqual(x / curator.PLAYFIELD_WIDTH, entry["x"], delta=2e-6, msg=(category, address, entry["object"]))
					self.assertAlmostEqual(y / curator.PLAYFIELD_HEIGHT, entry["y"], delta=2e-6, msg=(category, address, entry["object"]))
					checked += 1
		self.assertGreater(checked, 100)


if __name__ == "__main__":
	unittest.main()
