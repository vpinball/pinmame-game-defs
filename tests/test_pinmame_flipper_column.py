"""The PinMAME flipper column (public 81-88) on System 9/11 and Data East.

``core_updateSw`` copies the cabinet-button bits of PinMAME's flipper switch column into the matrix
switches a ``FLIP_SWNO(l, r)`` driver names, so a consumer drives 82/84 and never the matrix
addresses. These tests pin the profile rule, the shared curator helper, and every System 11 or Data
East definition that enumerates the column.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships  # noqa: E402
from pinmame_game_defs.workspace import resolve_working_root  # noqa: E402


PROFILES = {
	"pinmame.system-11": ROOT / "controllers" / "pinmame" / "system-11.json",
	"pinmame.dataeast": ROOT / "controllers" / "pinmame" / "data-east.json",
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def switch_group(profile: dict) -> dict:
	return next(group for group in profile["groups"] if group["id"] == "pinmame.input.switch")


def allowed(group: dict, address: int) -> bool:
	for rule in group["address_rules"]:
		if "values" in rule and address in rule["values"]:
			return True
		if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
			return True
	return False


class FlipperColumnProfileTests(unittest.TestCase):
	def test_both_profiles_declare_exactly_the_flipper_column_above_the_matrix(self) -> None:
		for platform, path in PROFILES.items():
			group = switch_group(load_json(path))
			with self.subTest(platform=platform):
				for address in range(81, 89):
					self.assertTrue(allowed(group, address), address)
				for address in (65, 80, 89, 90):
					self.assertFalse(allowed(group, address), address)
				notes = group["notes"]
				self.assertIn("#### Flipper column", notes)
				self.assertIn("CORE_FLIPPERSWCOL", notes)
				self.assertIn("drives `82`/`84`, never the matrix address", notes)
				for address, constant in ((81, "CORE_SWLRFLIPEOSBIT"), (82, "CORE_SWLRFLIPBUTBIT"), (83, "CORE_SWLLFLIPEOSBIT"), (84, "CORE_SWLLFLIPBUTBIT"), (88, "CORE_SWULFLIPBUTBIT")):
					self.assertIn(f"| `{address}` | `{constant}`", notes)
				self.assertNotIn("do not yet declare", notes)

	def test_the_system_11_note_keeps_one_flipper_section(self) -> None:
		notes = switch_group(load_json(PROFILES["pinmame.system-11"]))["notes"]
		self.assertEqual(1, notes.count("#### Flipper column"))
		self.assertNotIn("**Flipper buttons:**", notes)
		self.assertIn("`swURFlip = 81`", notes)


class FlipperColumnHelperTests(unittest.TestCase):
	def build(self, flip_swno: tuple[int, int]) -> dict[int, dict]:
		items = flipper_column_inputs(
			flip_swno=flip_swno, flip_swno_text=f"FLIP_SWNO{flip_swno}", core_refs=("core",), button_refs=("script",),
			button_notes={"left": "Left.", "right": "Right."}, unused_notes={81: "Staged."}, unused_note_refs=("library",),
		)
		return {item["binding"]["device"]: item for item in items}

	def test_right_button_feeds_the_right_matrix_switch_and_left_feeds_left(self) -> None:
		# FLIP_SWNO(l, r): FLIP_SWL = l receives CORE_SWLLFLIPBUTBIT (84), FLIP_SWR = r receives 82.
		for left, right in ((58, 57), (37, 38), (15, 16)):
			items = self.build((left, right))
			self.assertIn(f"matrix switch {right}", items[82]["physical"]["notes"])
			self.assertIn(f"matrix switch {left}", items[84]["physical"]["notes"])
			self.assertIn("45/46", items[82]["physical"]["notes"])
			self.assertIn("47/48", items[84]["physical"]["notes"])
			relationships = {(item["source"], item["destination"]) for item in flipper_column_relationships(
				flip_swno=(left, right), matrix_ids={left: f"switch.matrix-{left}", right: f"switch.matrix-{right}"}, refs=("core",),
			)}
			self.assertEqual({("switch.flipper-column-82", f"switch.matrix-{right}"), ("switch.flipper-column-84", f"switch.matrix-{left}")}, relationships)

	def test_only_the_two_lower_buttons_are_live(self) -> None:
		items = self.build((58, 57))
		self.assertEqual(list(range(81, 89)), sorted(items))
		self.assertEqual({82, 84}, {address for address, item in items.items() if item["availability"] == "used"})
		for address in (81, 83, 85, 86, 87, 88):
			self.assertEqual("unused", items[address]["spatial"]["reason"])
		self.assertEqual(["core", "library"], items[81]["provenance"]["source_refs"])
		self.assertEqual(["core"], items[85]["provenance"]["source_refs"])
		self.assertEqual(["core", "script"], items[82]["provenance"]["source_refs"])

	def test_a_zero_switch_number_gets_no_copy_relationship(self) -> None:
		relationships = flipper_column_relationships(flip_swno=(0, 57), matrix_ids={57: "switch.matrix-57"}, refs=("core",))
		self.assertEqual(["switch.matrix-57"], [item["destination"] for item in relationships])


class FlipperColumnDefinitionTests(unittest.TestCase):
	def test_every_enumerating_system_11_or_data_east_definition_follows_the_contract(self) -> None:
		checked = []
		for path in sorted((ROOT / "machines").glob("**/*.json")):
			definition = load_json(path)
			if definition.get("controller", {}).get("platform") not in PROFILES:
				continue
			switches = {
				item["binding"]["device"]: item
				for item in definition.get("inputs", [])
				if item["binding"]["group"] == "pinmame.input.switch" and isinstance(item["binding"]["device"], int)
			}
			column = {address: switches[address] for address in range(81, 89) if address in switches}
			if not column:
				continue
			checked.append(definition["machine"]["id"])
			with self.subTest(machine=definition["machine"]["id"]):
				self.assertEqual(set(range(81, 89)), set(column))
				self.assertEqual({82, 84}, {address for address, item in column.items() if item["availability"] == "used"})
				copies = {(item["source"], item["destination"]) for item in definition.get("relationships", []) if item["source"] in ("switch.flipper-column-82", "switch.flipper-column-84")}
				self.assertEqual(2, len(copies))
		self.assertIn("williams.whirlwind.1990", checked)
		self.assertIn("williams.high-speed.1986", checked)
		self.assertIn("bally.elvira-and-the-party-monsters.1989", checked)
		self.assertIn("williams.earthshaker.1989", checked)


class FlipperColumnPinnedSourceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.checkout = resolve_working_root(ROOT) / "source-checkouts" / "pinmame"
		if not (cls.checkout / "src" / "wpc" / "core.h").is_file():
			raise unittest.SkipTest("pinned PinMAME checkout is not available")

	def test_core_h_places_the_flipper_column_at_public_81_to_88(self) -> None:
		core_h = (self.checkout / "src" / "wpc" / "core.h").read_text(encoding="utf-8", errors="replace")
		column = int(re.search(r"#define CORE_FLIPPERSWCOL\s+(\d+)", core_h).group(1))
		self.assertEqual(11, column)
		expected = {
			"CORE_SWLRFLIPEOSBIT": 81, "CORE_SWLRFLIPBUTBIT": 82, "CORE_SWLLFLIPEOSBIT": 83, "CORE_SWLLFLIPBUTBIT": 84,
			"CORE_SWURFLIPEOSBIT": 85, "CORE_SWURFLIPBUTBIT": 86, "CORE_SWULFLIPEOSBIT": 87, "CORE_SWULFLIPBUTBIT": 88,
		}
		for constant, address in expected.items():
			bit = int(re.search(rf"#define {constant}\s+0x([0-9a-fA-F]+)", core_h).group(1), 16)
			# core_swSeq2m(n) = n + 7 maps public n to matrix index column * 8 + bit position.
			self.assertEqual(address, column * 8 + bit.bit_length() - 1 - 7, constant)
		core_c = (self.checkout / "src" / "wpc" / "core.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("int core_swSeq2m(int no) { return no+7; }", core_c)
		self.assertIn("if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);", core_c)
		self.assertIn("if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);", core_c)

	def test_no_system_11_or_data_east_driver_sets_flip_sol_eos_or_an_upper_button(self) -> None:
		wpc = self.checkout / "src" / "wpc"
		for name in ("s11games.c", "degames.c", "sims/s11/full/dd.c", "sims/s11/full/milln.c", "sims/s11/prelim/eatpm.c"):
			text = (wpc / name).read_text(encoding="utf-8", errors="replace")
			self.assertNotRegex(text, r"FLIP_SOL\s*\(|FLIP_EOS\s*\(|FLIP_SW\s*\([^)]*FLIP_U|FLIP_BUT\s*\(", name)
		# bowlgames.c also holds System 9/11 shuffle alleys (INITGAME_S10) and one Data East game (ctcheese);
		# check those entries only, since the same file carries WPC bowlers that do declare FLIP_SOL.
		bowl = (wpc / "bowlgames.c").read_text(encoding="utf-8", errors="replace")
		s10 = re.findall(r"^INITGAME_S10\(.*$", bowl, re.M)
		self.assertGreaterEqual(len(s10), 8)
		for line in s10:
			self.assertRegex(line, r"GEN_S(9|11),", line)
			self.assertNotRegex(line, r"FLIP_SOL\s*\(|FLIP_EOS\s*\(|FLIP_SW\s*\([^)]*FLIP_U|FLIP_BUT\s*\(", line)
		ctc = re.search(r"static core_tGameData ctcGameData = \{(.*?)\};", bowl, re.S).group(1)
		self.assertIn("GEN_DEDMD64", ctc)
		self.assertRegex(ctc, r"\{0,0,0,0,SNDBRD_DE2S")
		s11games = (wpc / "s11games.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("INITGAME(whirl,GEN_S11B,s11_dispS11b2,12, FLIP_SWNO(58,57)", s11games)
		self.assertIn("INITGAMEFULL(hs, GEN_S11X, s11_dispS11, 0, FLIP_SWNO(37,38)", s11games)

	def test_no_system_11_or_data_east_driver_inverts_the_flipper_column(self) -> None:
		# invSw[11] would change what core_updateSw reads from 81-88. Every initializer on these
		# platforms writes the wpc struct as {{0}}, except INITGAME_S10, which fills invSw[4] only.
		wpc = self.checkout / "src" / "wpc"
		for name in ("s11games.c", "degames.c", "sims/s11/full/dd.c", "sims/s11/full/milln.c", "sims/s11/prelim/eatpm.c"):
			text = (wpc / name).read_text(encoding="utf-8", errors="replace")
			self.assertNotIn("invSw", text, name)
			self.assertRegex(text, r"\{\{\s*0\s*\}\}", name)
		bowl = (wpc / "bowlgames.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("gen, disp, {flip,0,0,0,0,db,flags}, NULL, {{0}, {0,0,0,0,inv}}}; \\", bowl)
		self.assertRegex(re.search(r"static core_tGameData ctcGameData = \{(.*?)\};", bowl, re.S).group(1), r"NULL, \{\{0\}\}")


if __name__ == "__main__":
	unittest.main()
