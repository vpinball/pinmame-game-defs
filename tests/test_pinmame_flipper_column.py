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


# Curated Data East records: machine id -> (degames.c INITGAMES11 prefix, FLIP_SWNO (left, right)).
DATA_EAST_MACHINES = {
	"data-east.batman.1991": ("btmn", (15, 16)),
	"data-east.laser-war.1987": ("lwar", (47, 46)),
	"data-east.lethal-weapon-3.1992": ("lw3", (15, 16)),
	"data-east.playboy-35th-anniversary.1989": ("play", (15, 16)),
	"data-east.secret-service.1988": ("ssvc", (30, 31)),
	"data-east.time-machine.1988": ("tmac", (15, 16)),
	"data-east.torpedo-alley.1988": ("torp", (15, 16)),
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
		for machine in DATA_EAST_MACHINES:
			self.assertIn(machine, checked)

	def test_every_data_east_record_copies_to_its_own_flip_swno_pair(self) -> None:
		# The (left, right) pairs are FLIP1516 / FLIP4746 / FLIP3031 as degames.c declares them; the
		# pinned-source test below checks that declaration for each driver prefix.
		for machine, (prefix, (left, right)) in DATA_EAST_MACHINES.items():
			definition = next(
				load_json(path) for path in (ROOT / "machines").glob("**/*.json")
				if load_json(path)["machine"]["id"] == machine
			)
			with self.subTest(machine=machine):
				self.assertEqual("pinmame.dataeast", definition["controller"]["platform"])
				switches = {item["id"]: item for item in definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
				copies = {(item["source"], item["destination"]) for item in definition["relationships"] if item["source"].startswith("switch.flipper-column-")}
				destinations = {source: switches[destination]["binding"]["device"] for source, destination in copies}
				self.assertEqual({"switch.flipper-column-82": right, "switch.flipper-column-84": left}, destinations)
				for address in (left, right):
					notes = next(item for item in switches.values() if item["binding"]["device"] == address)["physical"]["notes"]
					self.assertIn(f"public {84 if address == left else 82}", notes, address)
				for address in (82, 84):
					notes = switches[f"switch.flipper-column-{address}"]["physical"]["notes"]
					self.assertIn(f"matrix switch {right if address == 82 else left}", notes)
				for address in range(45, 49):
					solenoid = next(
						item for item in definition["outputs"]
						if item["binding"]["group"] == "pinmame.output.solenoid" and item["binding"]["device"] == address
					)
					self.assertIn("public 82" if address in (45, 46) else "public 84", solenoid["physical"]["notes"], address)


class FlipperColumnDataEastLibraryTests(unittest.TestCase):
	"""The retained DE.VBS/DE2.VBS copies behind every Data East 81-88 and staged-flipper note."""

	def test_retained_data_east_libraries_match_their_pins_and_upper_constants(self) -> None:
		import hashlib
		import os

		from pinmame_flipper_column import VPM_CORE_SHA256, VPM_DE2_SHA256, VPM_DE_SHA256, VPM_UPPER_FLIP_SWITCHES

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		library = Path(root) / "vpm-script-libs"
		for name, digest in (("de.vbs", VPM_DE_SHA256), ("de2.vbs", VPM_DE2_SHA256), ("core.vbs", VPM_CORE_SHA256)):
			self.assertEqual(digest, hashlib.sha256((library / name).read_bytes()).hexdigest(), name)
		for name, key in (("de.vbs", "DE.VBS"), ("de2.vbs", "DE2.VBS")):
			text = (library / name).read_text(encoding="utf-8", errors="replace")
			upper_right, upper_left = VPM_UPPER_FLIP_SWITCHES[key]
			with self.subTest(library=name):
				self.assertRegex(text, r"Const swLRFlip\s*=\s*82\b")
				self.assertRegex(text, r"Const swLLFlip\s*=\s*84\b")
				self.assertRegex(text, rf"Const swURFlip\s*=\s*{upper_right}\b")
				self.assertRegex(text, rf"Const swULFlip\s*=\s*{upper_left}\b")
		core = (library / "core.vbs").read_text(encoding="utf-8", errors="replace").splitlines()
		# The lines vpm_staged_flipper_notes(single_flip_at=...) cites.
		self.assertEqual("If not cSingleLFlip Then", core[2110].strip())
		self.assertEqual("if err.number = 0 then NoUpperLeftFlipper", core[2111].strip())
		self.assertEqual("If not cSingleRFlip Then", core[2114].strip())
		self.assertEqual("if err.number = 0 then NoUpperRightFlipper", core[2115].strip())
		self.assertEqual("vpmFlips.Init", core[2311].strip())


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

	def test_each_curated_data_east_driver_declares_the_recorded_flip_swno_pair(self) -> None:
		degames = (self.checkout / "src" / "wpc" / "degames.c").read_text(encoding="utf-8", errors="replace")
		macros = {
			name: (int(left), int(right))
			for name, left, right in re.findall(r"^#define (FLIP\d{4})\s+FLIP_SWNO\((\d+),(\d+)\)", degames, re.M)
		}
		for machine, (prefix, pair) in DATA_EAST_MACHINES.items():
			with self.subTest(machine=machine):
				line = re.search(rf"^INITGAMES11\({prefix}\s*,\s*(GEN_DE\w*)\s*,[^,]+,\s*(FLIP\d{{4}})\s*,", degames, re.M)
				self.assertIsNotNone(line, prefix)
				self.assertEqual(pair, macros[line.group(2)], prefix)

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
