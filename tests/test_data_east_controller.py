from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "data-east.json"
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def address_allowed(group: dict, address: int) -> bool:
	for rule in group["address_rules"]:
		if "values" in rule and address in rule["values"]:
			return True
		if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
			return True
	return False


class DataEastControllerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(PROFILE_PATH)
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def test_profile_declares_the_shared_data_east_contract(self) -> None:
		self.assertEqual("pinmame.dataeast", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp"},
			set(self.groups),
		)
		self.assertEqual(
			1,
			self.groups["pinmame.output.solenoid"]["transports"]["controller_plugin"]["group_id"],
		)
		self.assertEqual(PINMAME_REVISION, self.profile["sources"][0]["revision"])

	def test_addresses_cover_the_base_data_east_public_namespace(self) -> None:
		for address in (-7, -6, 1, 8, 64):
			self.assertTrue(address_allowed(self.groups["pinmame.input.switch"], address))
		for address in (-5, -4, 0, 65):
			self.assertFalse(address_allowed(self.groups["pinmame.input.switch"], address))
		self.assertTrue(address_allowed(self.groups["pinmame.input.dip"], 0))
		for address in (1, 17, 23, 24, 25, 32, 37, 44, 45, 49, 50, 51, 64):
			self.assertTrue(address_allowed(self.groups["pinmame.output.solenoid"], address))
		for address in (1, 64):
			self.assertTrue(address_allowed(self.groups["pinmame.output.lamp"], address))

	def test_special_solenoid_permutation_and_mux_are_explicit(self) -> None:
		notes = self.groups["pinmame.output.solenoid"]["notes"]
		for row in (
			"| `pia1ca2_w` | `0` | `20` |",
			"| `pia1cb2_w` | `1` | `21` |",
			"| `pia3ca2_w` | `2` | `22` |",
			"| `pia3cb2_w` | `3` | `18` |",
			"| `pia4ca2_w` | `4` | `17` |",
			"| `pia4cb2_w` | `5` | `19` |",
		):
			self.assertIn(row, notes)
		self.assertIn("public `10`", notes)
		self.assertIn("public `25-32`", notes)
		self.assertIn("S11_MUXDELAY", notes)
		self.assertIn("these addresses are always zero", notes)
		self.assertIn("S11_PRINTERLINE", notes)
		self.assertIn("alpha initializers do not enable `S11_SNDOVERLAY`", notes)
		self.assertNotIn("Alpha games can use the same public range", notes)

	def test_profile_covers_every_binding_in_curated_data_east_definitions(self) -> None:
		checked = []
		for path in sorted((ROOT / "machines").glob("**/*.json")):
			definition = load_json(path)
			if definition.get("controller", {}).get("platform") != "pinmame.dataeast":
				continue
			if "identity" in definition["coverage"]["missing"]:
				continue
			self.assertTrue(
				definition["controller"]["inversion_applied_by_emulator"],
				f"{path.as_posix()}: public switch states must remain normalized for consumers",
			)
			for device in list(definition.get("inputs", [])) + list(definition.get("outputs", [])):
				binding = device.get("binding")
				if not binding:
					continue
				group_id = binding["group"]
				self.assertIn(group_id, self.groups, f"{path.as_posix()}:{device['id']}")
				self.assertTrue(
					address_allowed(self.groups[group_id], binding["device"]),
					f"{path.as_posix()}:{device['id']}:{binding['device']}",
				)
			checked.append(definition["machine"]["id"])
		self.assertEqual(7, len(checked))


if __name__ == "__main__":
	unittest.main()
