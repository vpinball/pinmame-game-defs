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

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "elvira-and-the-party-monsters-1989.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "elvira-and-the-party-monsters-1989.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "elvira-and-the-party-monsters-1989.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "elvira-and-the-party-monsters-1989.md"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

DRIVER_IDS = {"eatpm_l4", "eatpm_l1", "eatpm_l2", "eatpm_f1", "eatpm_4u", "eatpm_4g", "eatpm_3g", "eatpm_p7"}
UNUSED_MATRIX = {10, 14, 24, 38, 39, 40, 59, 60, 61, 62, 63, 64}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_x(device: dict) -> float:
	return device["spatial"]["placements"][0]["x"]


class ElviraTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = by_address(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = by_address(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_address(cls.definition, "outputs", "pinmame.output.lamp")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def test_identity_and_honest_partial_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.elvira-and-the-party-monsters.1989", 782, "Grlxp-MVKBW"), (machine["id"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual({"width": 952.0, "height": 1974.0, "units": "vpx"}, machine["playfield"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["input_semantics", "output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual({"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True}, self.definition["controller"])

	def test_curator_output_and_seed_are_byte_identical(self) -> None:
		import curate_elvira
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curate_elvira.build())
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())

	def test_driver_family_matches_the_catalog_clone_tree(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load_json(CATALOG_PATH)
		owners = {driver["id"]: driver["machine_id"] for driver in catalog["drivers"] if driver["id"].startswith("eatpm_")}
		self.assertEqual(DRIVER_IDS, set(owners))
		self.assertEqual({"bally.elvira-and-the-party-monsters.1989"}, set(owners.values()))
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"eatpm_3g", "eatpm_p7"}, {driver for driver, value in compatibility.items() if value == "compatible"})

	def test_every_controller_address_is_enumerated_once(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		ids = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(ids), len(set(ids)))

	def test_switch_matrix_dispositions_follow_the_manual(self) -> None:
		unused = {address for address, item in self.switches.items() if item["availability"] == "unused" and address <= 64}
		self.assertEqual(UNUSED_MATRIX, unused)
		self.assertEqual("A/C Relay Select", self.switches[2]["label"])
		self.assertEqual(["internal.ac-relay-feedback"], self.switches[2]["roles"])
		self.assertEqual(("Right Flipper", "Left Flipper"), (self.switches[57]["label"], self.switches[58]["label"]))
		# 41-43 on the drop-target opto board; 2, 57 and 58 on the Backbox Interconnect Board's 4N25s.
		for address in (2, 41, 42, 43, 57, 58):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
		self.assertIn("U3, labelled RT L.C.", self.switches[57]["physical"]["notes"])
		self.assertIn("U2, labelled LT L.C.", self.switches[58]["physical"]["notes"])
		# PinMAME rewrites 57/58 from its flipper switch column; consumers must drive public 82/84.
		for address in (57, 58):
			self.assertIn("public 82 (right button", self.switches[address]["physical"]["notes"])
			self.assertIn("84 (left button", self.switches[address]["physical"]["notes"])
		# FLIP_SWNO(58,57): 82 (CORE_SWLRFLIPBUTBIT) is copied into 57 and 84 into 58; nothing else is read.
		self.assertEqual({82, 84}, {address for address in range(81, 89) if self.switches[address]["availability"] == "used"})
		self.assertIn("matrix switch 57", self.switches[82]["physical"]["notes"])
		self.assertIn("matrix switch 58", self.switches[84]["physical"]["notes"])
		pairs = {(item["source"], item["destination"]) for item in self.definition["relationships"]}
		self.assertIn(("switch.flipper-column-82", "switch.matrix-57"), pairs)
		self.assertIn(("switch.flipper-column-84", "switch.matrix-58"), pairs)
		self.assertEqual({"Lock 1", "Lock 2", "Lock 3"}, {self.switches[address]["label"] for address in (49, 50, 51)})

	def test_ac_mux_bank_pairs_share_driver_transistors(self) -> None:
		for address in range(1, 9):
			self.assertEqual(
				self.solenoids[address]["wiring"]["driver_transistor"],
				self.solenoids[address + 24]["wiring"]["driver_transistor"],
				address,
			)
		self.assertEqual({"flasher"}, {self.solenoids[address]["kind"] for address in range(25, 33)})
		self.assertEqual("unused", self.solenoids[4]["availability"])
		self.assertEqual("A/C Select Relay", self.solenoids[12]["label"])
		self.assertEqual(("gi", "gi"), (self.solenoids[10]["kind"], self.solenoids[11]["kind"]))
		self.assertEqual("cabinet_or_service", self.solenoids[10]["spatial"]["reason"])
		self.assertNotIn("spatial", self.solenoids[11])

	def test_special_solenoids_keep_the_printed_special_order(self) -> None:
		expected = {
			17: "Left Thumper Bumper", 18: "Left Slingshot Kicker", 19: "Right Thumper Bumper",
			20: "Right Slingshot Kicker", 21: "Bottom Thumper Bumper", 22: "Flip Up Reset",
		}
		self.assertEqual(expected, {address: self.solenoids[address]["label"] for address in expected})
		for address in expected:
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(f"Special #{address - 16}", aliases["manual.special-solenoid"])

	def test_pinned_s11_permutation_maps_handlers_back_to_printed_order(self) -> None:
		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		source = Path(checkout) / "src" / "wpc" / "s11.c" if checkout else None
		if source is None or not source.is_file():
			self.skipTest("pinned PinMAME checkout is not available")
		text = source.read_text(encoding="utf-8", errors="replace")
		ss_sol_no = [int(value) for value in re.search(r"ssSolNo\[2\]\[6\]\s*=\s*\{\{([0-9,\s]+)\}", text).group(1).split(",")]
		handlers = {f"pia{pia}{line.lower()}2_w": int(index) for pia, line, index in re.findall(r"WRITE_HANDLER\(pia(\d)(c[ab])2_w\)\s*\{\s*setSSSol\(data,\s*(\d)\);", text)}
		labels: dict[int, int] = {}
		for pia, body in re.findall(r"PIA (\d) \([0-9a-f]+\)\s*\*/(.*?)\}", text, re.S):
			for line, number in re.findall(r"C([AB])2\s+(?:\(I\)\s+)?[A-F]\s+SST?(\d)", body):
				key = f"pia{pia}c{line.lower()}2_w"
				if key in handlers:
					labels[handlers[key]] = int(number)
		self.assertEqual(set(range(6)), set(labels))
		self.assertEqual({17 + ss_sol_no[index]: number for index, number in labels.items()}, {17 + n: n + 1 for n in range(6)})

	def test_flipper_outputs_are_synthetic_and_upper_flippers_absent(self) -> None:
		for address in (45, 46, 47, 48):
			self.assertEqual(("virtual", "used"), (self.solenoids[address]["kind"], self.solenoids[address]["availability"]))
		for address in range(33, 45):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		# core.vbs defines sLRFlipper = 46 and sLLFlipper = 48, so the script binding lives on the hold addresses.
		self.assertIn("sLRFlipper = 46", self.solenoids[46]["physical"]["notes"])
		self.assertIn("sLLFlipper = 48", self.solenoids[48]["physical"]["notes"])
		self.assertNotIn("SolCallback", self.solenoids[45]["physical"]["notes"])

	def test_sided_devices_sit_on_their_named_side(self) -> None:
		self.assertLess(first_x(self.solenoids[18]), first_x(self.solenoids[20]))
		self.assertLess(first_x(self.solenoids[17]), first_x(self.solenoids[19]))
		self.assertLess(first_x(self.switches[33]), first_x(self.switches[34]))
		self.assertLess(first_x(self.switches[17]), first_x(self.switches[20]))
		self.assertLess(first_x(self.lamps[29]), first_x(self.lamps[30]))
		self.assertLess(first_x(self.lamps[31]), first_x(self.lamps[32]))
		self.assertLess(first_x(self.lamps[14]), first_x(self.lamps[15]))
		# Lamp Location Diagram: skull eye 18 above and right of 17, matching the bulb covers.
		self.assertLess(first_x(self.lamps[17]), first_x(self.lamps[18]))
		self.assertLess(self.lamps[18]["spatial"]["placements"][0]["y"], self.lamps[17]["spatial"]["placements"][0]["y"])
		elvira = [first_x(self.lamps[address]) for address in range(1, 7)]
		self.assertEqual(sorted(elvira), elvira)

	def test_disputed_and_offboard_lamps_carry_no_invented_coordinates(self) -> None:
		for address in (11, 20):
			self.assertNotIn("spatial", self.lamps[address])
		for address in range(57, 65):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)

	def test_placements_are_normalized(self) -> None:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if spatial and spatial["status"] != "not_applicable":
				for placement in spatial["placements"]:
					self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
					self.assertEqual(placement["x"], round(placement["x"], 6))

	def test_addresses_named_by_conflicts_stay_conflicted(self) -> None:
		for address in (53, 54, 55, 56):
			self.assertEqual("conflicted", self.switches[address]["provenance"]["status"], address)
		for address in (11, 20):
			self.assertEqual("conflicted", self.lamps[address]["provenance"]["status"], address)
		for address in (15, 16):
			self.assertEqual("conflicted", self.solenoids[address]["provenance"]["status"], address)
			self.assertEqual("observed", self.solenoids[address]["spatial"]["status"], address)
		self.assertEqual("conflicted", next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.flip-up-targets")["provenance"]["status"])

	def test_conflicts_are_actionable(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.slingshot-lamp-sides", "conflict.flasher-bulb-quantities", "conflict.flip-up-switch-roles"}, set(conflicts))
		for conflict in conflicts.values():
			self.assertIn("Resolution path:", conflict["description"])
			self.assertNotEqual("ignored", conflict.get("status"))

	def test_special_solenoid_relationships_pair_same_named_devices(self) -> None:
		pairs = {(item["source"], item["destination"]) for item in self.definition["relationships"] if item["id"].startswith("relationship.special-solenoid-")}
		self.assertEqual(
			{
				("switch.matrix-35", "device.left-thumper-bumper"), ("switch.matrix-33", "device.left-slingshot-kicker"),
				("switch.matrix-36", "device.right-thumper-bumper"), ("switch.matrix-34", "device.right-slingshot-kicker"),
				("switch.matrix-37", "device.bottom-thumper-bumper"),
			},
			pairs,
		)

	def test_excerpts_are_reviewed_manual_transcriptions(self) -> None:
		excerpts = self.sources["manual.bally.elvira-and-the-party-monsters.1989"]["excerpts"]
		self.assertEqual(11, len(excerpts))
		for excerpt in excerpts:
			self.assertEqual(("manual", True), (excerpt["method"], excerpt["reviewed"]))
			self.assertTrue((ROOT / excerpt["path"]).is_file())

	def test_knowledge_note_names_the_open_questions(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("S11_MUXSW2", "Dead Head", "Barbeque", "flip-up", "FACTORY SETTING"):
			self.assertIn(phrase, text)

	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_manifest(self) -> None:
		import curate_elvira

		curate_elvira.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_retained_table_and_script_hashes(self) -> None:
		import curate_elvira

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "bally" / "elvira-and-the-party-monsters-1989"
		table = root / "Elvira and the Party Monsters (Bally 1989) nude.vpx"
		self.assertEqual(curate_elvira.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / "extracted-vpxtool" / "script.vbs"
		self.assertEqual(curate_elvira.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())

	def test_retained_manual_hash(self) -> None:
		import curate_elvira

		manual = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / "bally.elvira-and-the-party-monsters.1989" / "Elvira_and_the_Partymonsters_OCR_searchable.pdf"
		self.assertEqual(curate_elvira.MANUAL_SHA256, hashlib.sha256(manual.read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
