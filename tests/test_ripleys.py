from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "stern" / "ripley-s-believe-it-or-not-2004.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "ripleys-boot-start-and-gameplay.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "whitestar.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "ripley-s-believe-it-or-not-2004.md"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class RipleysDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")

	def test_identity_driver_family_and_author_ready_gate(self) -> None:
		self.assertEqual(
			{"id": "stern.ripley-s-believe-it-or-not.2004", "ipdb_id": 4917, "kind": "physical_pinball", "manufacturer": "Stern", "name": "Ripley's Believe It or Not!", "year": 2004},
			self.definition["machine"],
		)
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertTrue(all(value == "validated" for value in self.definition["coverage"]["dimensions"].values()))
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])
		expected = {f"rip{version}{language}" for version in ("300", "301", "302", "310") for language in ("", "f", "g", "i", "l")} | {f"ripleys{language}" for language in ("", "f", "g", "i", "l")}
		self.assertEqual(expected, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(expected, {driver["id"] for driver in catalog["drivers"] if driver["root_driver"] == "ripleys"})
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "ripley-s-believe-it-or-not-2004.json").exists())

	def test_whitestar_profile_and_complete_input_spaces(self) -> None:
		self.assertEqual("pinmame.whitestar", self.profile["id"])
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 65)) | set(range(-3, 1)) | set(range(81, 89)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual({10, 37, 63, 64, 85, 86, 87}, {address for address, switch in switches.items() if switch["availability"] == "unused"})
		self.assertTrue(switches[83]["normally_closed"])
		self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Upper-right flipper button", switches[88]["label"])
		self.assertEqual("Coin-door memory protect", switches[-3]["label"])
		self.assertEqual(("180-5000-01", "500-5808-00", "CN6-P12"), (switches[-3]["physical"]["part_number"], switches[-3]["physical"]["assembly_part_number"], switches[-3]["wiring"]["drive_connection"]))
		self.assertEqual(["180-5192-02", "180-5192-04", "180-5192-00"], [switches[address]["physical"]["part_number"] for address in (-2, -1, 0)])
		self.assertTrue(all(not switches[address]["pulse"] for address in (-3, -2, -1, 0)))

	def test_switch_semantics_and_proven_script_contact_behavior(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		expected_pulses = {2, 3, 4, 5, 6, 7, 9, 15, 17, 19, 20, 21, 22, 25, 26, 27, 32, 49, 50, 51, 59, 62}
		self.assertEqual(expected_pulses, {address for address in range(1, 65) if switches[address]["availability"] != "unused" and switches[address]["pulse"]})
		self.assertEqual(["Four-ball trough 1 (left)", "Four-ball trough 2", "Four-ball trough 3", "Four-ball trough 4 / VUK opto", "Four-ball stacking opto"], [switches[address]["label"] for address in range(11, 16)])
		self.assertEqual(["Vari-target opto 1", "Vari-target opto 2", "Vari-target opto 3"], [switches[address]["label"] for address in range(41, 44)])
		self.assertEqual({-3, 11, 12, 13, 14, 42, 43}, {address for address, switch in switches.items() if switch.get("initial_active")})
		self.assertEqual("180-5190-28", switches[31]["physical"]["part_number"])
		self.assertNotIn("assembly_part_number", switches[31]["physical"])
		self.assertEqual("500-5190-28", switches[53]["physical"]["assembly_part_number"])
		self.assertNotIn("part_number", switches[53]["physical"])
		for address, expected in {
			1: ("GRN-BRN", "CN5-P1", "WHT-BRN", "CN7-P9"),
			8: ("GRN-BRN", "CN5-P1", "WHT-GRY", "CN7-P1"),
			9: ("GRN-RED", "CN5-P3", "WHT-BRN", "CN7-P9"),
			64: ("GRN-GRY", "CN5-P9", "WHT-GRY", "CN7-P1"),
		}.items():
			wiring = switches[address]["wiring"]
			self.assertEqual(expected, (wiring["drive_wire"], wiring["drive_connection"], wiring["return_wire"], wiring["return_connection"]))

	def test_physical_q_outputs_and_public_whitestar_remap_are_explicit(self) -> None:
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 51)), set(outputs))
		for address in list(range(1, 15)) + list(range(17, 33)):
			self.assertIn({"namespace": "manual.address", "value": f"Q{address}"}, outputs[address]["aliases"])
		self.assertEqual(("device.q14-upper-right-flipper", "Q14"), (outputs[14]["id"], outputs[14]["wiring"]["driver_transistor"]))
		self.assertEqual(("virtual", "used"), (outputs[15]["kind"], outputs[15]["availability"]))
		self.assertEqual(("virtual", "unused"), (outputs[16]["kind"], outputs[16]["availability"]))
		self.assertEqual(("device.q16-right-flipper", "Q16"), (outputs[46]["id"], outputs[46]["wiring"]["driver_transistor"]))
		self.assertEqual(("device.q15-left-flipper", "Q15"), (outputs[48]["id"], outputs[48]["wiring"]["driver_transistor"]))
		self.assertEqual({45, 47}, {address for address in (45, 46, 47, 48) if outputs[address]["kind"] == "virtual"})
		self.assertIn("power-phase compatibility", outputs[45]["label"])
		self.assertIn("power-phase compatibility", outputs[47]["label"])
		self.assertEqual({33, 34, 35}, {address for address, output in outputs.items() if output["availability"] == "optional" and address >= 33})
		self.assertEqual(set(range(36, 45)) | {49, 50}, {address for address, output in outputs.items() if address >= 33 and output["availability"] == "unused"})
		self.assertEqual("optional", outputs[24]["availability"])
		self.assertIn("deliberately comments out", outputs[24]["physical"]["notes"])

	def test_lamps_flashers_gi_and_native_displays_are_complete(self) -> None:
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertTrue(all(lamp["availability"] == "used" for lamp in lamps.values()))
		self.assertEqual({11, 16, 50, 51, 52, 63, 65, 76, 77, 78}, {address for address, lamp in lamps.items() if lamp["physical"]["part_number"] == "165-5000-44"})
		for address, expected in {
			1: ("YEL-BRN", "J13-P9", "RED-BRN", "J12-P1"),
			8: ("YEL-GRY", "J13-P1", "RED-BRN", "J12-P1"),
			9: ("YEL-BRN", "J13-P9", "RED-BLK", "J12-P2"),
			80: ("YEL-GRY", "J13-P1", "RED", "J12-P11"),
		}.items():
			wiring = lamps[address]["wiring"]
			self.assertEqual(expected, (wiring["drive_wire"], wiring["drive_connection"], wiring["return_wire"], wiring["return_connection"]))
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual({0}, set(gi))
		self.assertIn("four separately fused physical strings", gi[0]["physical"]["notes"])
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual({25, 26, 27, 28, 29, 30, 31, 32}, {address for address, output in solenoids.items() if output["kind"] == "flasher"})
		self.assertEqual((2, 2), (solenoids[25]["physical"]["quantity"], solenoids[30]["physical"]["quantity"]))
		self.assertIn("one #89", solenoids[30]["physical"]["notes"])
		self.assertIn("one #906", solenoids[30]["physical"]["notes"])
		self.assertEqual([(128, 32), (5, 7), (5, 7), (5, 7)], [(display["width"], display["height"]) for display in self.definition["displays"]])
		self.assertEqual([0, 1, 2, 3], [display["controller_index"] for display in self.definition["displays"]])

	def test_custom_mechanisms_capture_authoring_causality(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		vari = mechanisms["mechanism.vari-target"]
		self.assertEqual(["switch.41-vari-target-opto-1", "switch.42-vari-target-opto-2", "switch.43-vari-target-opto-3"], vari["sensors"])
		for fragment in ("seven mechanical stops", "267-unit lever", "spring factor 0.3", "return speed 600", "path length 1/6", "1/2", "3/4", "closes 42 and 43"):
			self.assertIn(fragment, vari["behavior"])
		self.assertIn("100 ms", mechanisms["mechanism.trough"]["behavior"])
		self.assertEqual(["device.q19-idol-magnet", "device.q22-idol-opto-led"], mechanisms["mechanism.idol-magnet"]["actuators"])
		for fragment in ("150 ms", "tick 3", "tick 4", "tick 12"):
			self.assertIn(fragment, mechanisms["mechanism.shrunken-head-magnet"]["behavior"])
		self.assertEqual(["device.q15-left-flipper", "device.q16-right-flipper"], mechanisms["mechanism.lower-flippers"]["actuators"])
		for fragment in ("TempleDiv", "LockDiverter", "end position", "lock seats 44-46"):
			self.assertIn(fragment, mechanisms["mechanism.ramp-diverters"]["behavior"])
		self.assertIn("Q5's proven LockDiverter", mechanisms["mechanism.three-ball-lock"]["behavior"])
		self.assertEqual(["switch.1-left-cabinet-button-uk-only", "switch.8-right-cabinet-button-uk-only"], mechanisms["mechanism.optional-uk-controls"]["sensors"])
		self.assertIn("must not invent", mechanisms["mechanism.optional-q24-output"]["behavior"])

	def test_every_reference_binding_and_mechanism_endpoint_resolves_uniquely(self) -> None:
		items = [*self.definition["inputs"], *self.definition["outputs"]]
		self.assertEqual(len(items), len({item["id"] for item in items}))
		self.assertEqual(len(items), len({(item["binding"]["group"], item["binding"]["device"]) for item in items}))
		item_ids = {item["id"] for item in items}
		actuators: list[str] = []
		for mechanism in self.definition["mechanisms"]:
			self.assertLessEqual(set(mechanism["actuators"] + mechanism["sensors"]), item_ids)
			actuators.extend(mechanism["actuators"])
		self.assertEqual(len(actuators), len(set(actuators)))
		source_ids = {source["id"] for source in self.definition["sources"]}
		for item in [*items, *self.definition["displays"], *self.definition["mechanisms"]]:
			self.assertLessEqual(set(item["provenance"]["source_refs"]), source_ids)

	def test_exact_artifact_and_runtime_hashes_are_pinned_with_evidence_limits(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual("94a94aef7437fa5f78cadddd66801e96224cfe6a5b8ff643c4c6b09d979fad9e", sources["manual.stern-ripleys.2004"]["sha256"])
		self.assertEqual("3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7", sources["vpx.ripleys-vpwmod-1.3"]["sha256"])
		self.assertEqual("092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3", sources["rom.stern-ripleys.3.20"]["sha256"])
		self.assertEqual(
			["1ef3c8baa88ace776fdf3ddbc59137afca0e7e9a6803339627985378a818270e", "e98f6058ba3d4cbd4e772606f1bc8f03039d334cde8d6045ec18d15444bf8ecc", "d389ced56f57bccd2704758cdac167b56d0a6f1621f306033adcc74d22fd57c7"],
			[run["sha256"] for run in self.evidence["runtime"]["raw_runs"]],
		)
		self.assertEqual([{"depth": 2, "height": 32, "type": 14, "width": 128}, {"depth": 2, "height": 7, "type": 526, "width": 5}], self.evidence["runtime"]["observations"]["display_layouts_seen"])
		self.assertEqual([0, 1, 2, 3], self.evidence["runtime"]["observations"]["display_indices_seen"])
		self.assertNotIn("physical_service_solenoid_to_public", self.evidence["runtime"]["observations"])
		self.assertIn("front-inserted PDF page 8", sources["manual.stern-ripleys.2004"]["locator"])
		self.assertIn("appended PDF page 190", sources["manual.stern-ripleys.2004"]["locator"])
		self.assertIn("pixel-frame callbacks only for the main DMD", self.knowledge)
		self.assertIn("must not invent either a physical or audible knocker", self.knowledge)


if __name__ == "__main__":
	unittest.main()
