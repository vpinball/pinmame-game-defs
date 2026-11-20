"""Fail-closed tests for the Gottlieb Class of 1812 (1991) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Lamp Matrix, Relay+Solenoid and Switch
Matrix tests for names and addresses, pinned PinMAME's gts3.c and gts3games.c for the numbering and the flipper copy,
the known-working script for bindings, the trough probes for switch 44, and IPDB's photos for the rear toys and the
right ramp's sign. A regression names the fact that broke.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_class_of_1812  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "gottlieb" / "class-of-1812-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "gottlieb" / "class-of-1812-1991.md"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "gts3.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "gottlieb.class-of-1812.1991"
MATRIX = {column * 10 + row for column in range(12) for row in range(8)}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def note_pairs(note: str, marker: str = "Address = name: ") -> dict[str, str]:
	"""Parse the "a = b; c = d." list a run note ends with."""
	body = note.split(marker, 1)[1].split(". No line of its own", 1)[0].rstrip(".")
	pairs = {}
	for item in body.split("; "):
		key, _, value = item.partition(" = ")
		pairs[key] = value
	return pairs


def allowed(rules: list[dict]) -> set[int]:
	values: set[int] = set()
	for rule in rules:
		values |= set(rule["values"]) if "values" in rule else set(range(rule["minimum"], rule["maximum"] + 1))
	return values


class ClassOf1812DefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"]}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(curate_class_of_1812.RUNTIME_EVIDENCE_PATH)
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]
		cls.profile = load(PROFILE_PATH)

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_class_of_1812.check(ROOT)

	def test_definition_validates_and_keeps_outputs_mechanisms_and_spatial_open(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["output_semantics", "mechanism_behavior", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual({"platform": "pinmame.gts3", "hardware_generation": "0x20000000000", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertEqual((528, "730", "G5DYX-M0oVW"), (self.definition["machine"]["ipdb_id"], self.definition["machine"]["model_number"], self.definition["machine"]["opdb_id"]))

	def test_single_driver_is_claimed_and_identical(self) -> None:
		self.assertEqual(["clas1812"], [d["id"] for d in self.definition["drivers"]])
		self.assertEqual("identical", self.definition["drivers"][0]["physical_compatibility"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		claimed = {d["id"] for d in catalog["drivers"] if d.get("machine_id") == curate_class_of_1812.MACHINE_ID}
		self.assertEqual({"clas1812"}, claimed)
		# The power-up screen prints game 730, IPDB's model number (the font draws 0 like O).
		self.assertIn("CLASS OF 1812 / 73O", self.runs["nvram-init"]["note"])

	def test_every_profile_address_is_enumerated_once_and_there_is_no_aux_board(self) -> None:
		groups = {group["id"]: allowed(group["address_rules"]) for group in self.profile["groups"]}
		self.assertEqual(groups["pinmame.input.switch"], set(self.switches))
		self.assertEqual(groups["pinmame.output.solenoid"], set(self.solenoids))
		# hw.lampCol = 4: the profile's auxiliary lamps 120-127 do not exist on this machine.
		self.assertEqual(groups["pinmame.output.lamp"] - set(range(120, 128)), set(self.lamps))
		self.assertEqual(MATRIX, set(self.lamps))
		self.assertEqual(set(range(1, 33)) | set(range(45, 49)), set(self.solenoids))

	def test_two_alphanumeric_displays_follow_gts3_disp_alpha(self) -> None:
		displays = [(d["kind"], d["controller_index"], d["segment_start"], d["width"]) for d in self.definition["displays"]]
		self.assertEqual([("segment", 0, 0, 20), ("segment", 1, 20, 20)], displays)

	def test_coil_names_follow_the_rom_relay_and_solenoid_test(self) -> None:
		seen = 0
		for key, address in self.named.items():
			match = re.fullmatch(r"solenoid-(\d+)-(.+)", key)
			if not match:
				continue
			seen += 1
			driver, name = int(match.group(1)), match.group(2)
			self.assertEqual(driver + 1, address)
			self.assertEqual(curate_class_of_1812.slug(curate_class_of_1812.ROM_COIL_NAMES[address]), name)
			self.assertIn(curate_class_of_1812.ROM_COIL_NAMES[address], self.solenoids[address]["physical"]["notes"])
		self.assertEqual(32, seen)
		# The walk fired drivers 0-31 in order; no driver is NOT USED.
		self.assertEqual(list(range(1, 33)), self.runs["solenoids"]["ordered_solenoid_on_sequence"])
		# The coin meter is an optional accessory; the knocker is named but no source shows it fitted.
		self.assertEqual({27: "optional", 30: "unknown"}, {a: o["availability"] for a, o in self.solenoids.items() if o["availability"] != "used"})

	def test_lamp_names_follow_the_lamp_matrix_test(self) -> None:
		pairs = note_pairs(self.runs["lamp-matrix"]["note"])
		self.assertEqual({str(address) for address in MATRIX}, set(pairs))
		for address in MATRIX:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "NOT USED":
					self.assertIn(self.lamps[address]["availability"], ("unused", "unknown"))
				else:
					self.assertEqual(curate_class_of_1812.ROM_LAMP_NAMES[address], name)
					self.assertEqual("used", self.lamps[address]["availability"])
		# Lamp 1 rose only inside the self-tests; 24 and 87 are NOT USED yet driven in play, so their fitment is unknown.
		self.assertEqual({1}, {a for a, o in self.lamps.items() if o["availability"] == "unused"})
		self.assertEqual({24, 87}, {a for a, o in self.lamps.items() if o["availability"] == "unknown"})
		self.assertEqual({24: (25, 7, 3, 18), 87: (43, 8, 3, 19)}, curate_class_of_1812.UNEXPLAINED_LAMPS)
		for address in (24, 87):
			self.assertNotIn("spatial", self.lamps[address])
			self.assertIn("No wiring source says whether a bulb is fitted", self.lamps[address]["physical"]["notes"])
		self.assertIn("never in the scripted game or the two tilt-trough runs", self.lamps[1]["physical"]["notes"])

	def test_switch_names_follow_the_switch_matrix_test(self) -> None:
		pairs = note_pairs(self.runs["switch-matrix"]["note"])
		# The credit button (3) is a control of its own in the self-tests and has no line in the Switch Matrix Test.
		expected = MATRIX - {3}
		self.assertEqual({str(address) for address in expected}, set(pairs))
		for address in expected:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "NOT USED":
					self.assertEqual("unused", self.switches[address]["availability"])
				else:
					self.assertEqual(curate_class_of_1812.ROM_SWITCH_NAMES[address], name)
					self.assertEqual("used", self.switches[address]["availability"])
		self.assertEqual({a for a in MATRIX if a >= 56}, {a for a in MATRIX if self.switches[a]["availability"] == "unused"})
		self.assertIn("ALL SWITCHES OPEN", self.runs["switch-matrix"]["note"])

	def test_every_fitted_physical_switch_is_normally_open(self) -> None:
		for address, device in self.switches.items():
			if device["kind"] == "switch" and device["availability"] in ("used", "optional"):
				with self.subTest(address=address):
					self.assertIs(False, device.get("normally_closed"))

	def test_flipper_buttons_are_copied_into_6_and_7(self) -> None:
		relationships = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		self.assertEqual({("switch.flipper-column-141", "switch.matrix-7"), ("switch.flipper-column-143", "switch.matrix-6")}, relationships)
		for address in (6, 7):
			self.assertIn("cannot be driven directly", self.switches[address]["physical"]["notes"])
		self.assertEqual(("LEFT FLIPPER", "RIGHT FLIPPER"), (curate_class_of_1812.ROM_SWITCH_NAMES[6], curate_class_of_1812.ROM_SWITCH_NAMES[7]))
		self.assertEqual({141, 143}, {a for a in range(140, 148) if self.switches[a]["availability"] == "used"})
		self.assertEqual((6, 7), curate_class_of_1812.FLIP_SWNO)
		seen = set(self.runs["gameplay"]["solenoid_addresses_seen"])
		self.assertEqual({45, 46, 47, 48}, seen & {45, 46, 47, 48})

	def test_cabinet_port_switches_are_the_coin_door_and_front_buttons(self) -> None:
		roles = {address: self.switches[address]["roles"] for address in range(0, 8)}
		self.assertEqual(
			{0: ["cabinet.coin"], 1: ["cabinet.coin"], 2: ["cabinet.coin"], 3: ["cabinet.start"], 4: ["cabinet.service"],
			 5: ["cabinet.service"], 6: ["cabinet.flipper"], 7: ["cabinet.flipper"]},
			roles,
		)
		for address in (4, 5):
			self.assertIn("using front right cabinet buttons", self.switches[address]["physical"]["notes"])
			self.assertIn("on the machine the flipper buttons do not close it", self.switches[address]["physical"]["notes"])

	def test_relays_flashers_and_led_lamps_follow_pinmame(self) -> None:
		self.assertEqual({26, 31, 32}, {a for a, o in self.solenoids.items() if o["kind"] == "relay"})
		# PinMAME types each relay's load; no source says where the relay itself is mounted.
		for address in (26, 31, 32):
			self.assertTrue(self.solenoids[address]["physical"]["location"].startswith("relay in the cabinet or backbox"), address)
		self.assertEqual(set(range(13, 26)), {a for a, o in self.solenoids.items() if o["kind"] == "flasher"})
		self.assertEqual(set(range(10, 15)), set(curate_class_of_1812.LED_LAMPS))
		for address in curate_class_of_1812.LED_LAMPS:
			self.assertIn("strobed LED", self.lamps[address]["physical"]["notes"])

	def test_placements_are_observed_in_range_and_only_backbox_flashers_and_unexplained_lamps_are_omitted(self) -> None:
		placements = [
			placement for collection in ("inputs", "outputs") for device in self.definition[collection]
			for placement in (device.get("spatial") or {}).get("placements", [])
		]
		self.assertEqual(170, len(placements))
		self.assertEqual(len(placements), len({placement["id"] for placement in placements}))
		for placement in placements:
			with self.subTest(placement=placement["id"]):
				self.assertEqual("observed", placement["provenance"]["status"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)
		omitted = sorted(
			(device["binding"]["group"], device["binding"]["device"])
			for device in self.definition["inputs"] + self.definition["outputs"] if "spatial" not in device
		)
		self.assertEqual(
			[("pinmame.output.lamp", 24), ("pinmame.output.lamp", 87)] + [("pinmame.output.solenoid", a) for a in range(13, 22)],
			omitted,
		)
		self.assertEqual("not_applicable", self.solenoids[26]["spatial"]["status"])
		# Of the 23 GI collection members, the four that show no bulb mesh are render lights and are not placed.
		self.assertEqual(23, len(curate_class_of_1812.GI_COLLECTION))
		self.assertEqual(("light18", "light21", "light22", "light23"), curate_class_of_1812.GI_RENDER_ONLY)
		self.assertEqual(19, len(self.solenoids[31]["spatial"]["placements"]))
		self.assertNotIn("quantity", self.solenoids[31])
		self.assertIn("light18, light21, light22 and light23 show none", self.solenoids[31]["physical"]["notes"])

	def test_placements_follow_the_bound_objects(self) -> None:
		def xy(device):
			(placement,) = device["spatial"]["placements"]
			return (placement["x"], placement["y"])

		# 44 closes only with both balls home, so it sits at Kicker Slot2 behind the release Slot1 that 28 kicks from.
		self.assertEqual(curate_class_of_1812.norm(665.3572, 1727.1392), xy(self.switches[44]))
		self.assertEqual(curate_class_of_1812.norm(724.0075, 1700.1406), xy(self.solenoids[28]))
		self.assertEqual(xy(self.switches[53]), xy(self.solenoids[7]))
		self.assertEqual(xy(self.switches[52]), xy(self.solenoids[6]))
		self.assertEqual(curate_class_of_1812.norm(*curate_class_of_1812.MESH_POINTS["bulb9"]), xy(self.lamps[10]))
		# The sign and crypt lamps sit on the bulb primitives the script draws them on, not on their bulb-less lights.
		for address, (bulb, _) in curate_class_of_1812.BULB_LAMPS.items():
			self.assertEqual(curate_class_of_1812.norm(*curate_class_of_1812.MESH_POINTS[bulb]), xy(self.lamps[address]))
		self.assertNotEqual(curate_class_of_1812.norm(260.67282, 673.9188), xy(self.lamps[36]))  # Light L36
		# The bank reset sits on the mean of the bank's four targets.
		left = [curate_class_of_1812.TABLE_POINTS[name] for name in ("sw16", "sw26", "sw36", "sw46")]
		mean = (round(sum(p[1] for p in left) / 4, 6), round(sum(p[2] for p in left) / 4, 6))
		self.assertEqual(curate_class_of_1812.norm(*mean), xy(self.solenoids[8]))
		self.assertEqual("emitter", self.solenoids[22]["spatial"]["placements"][0]["role"])
		self.assertEqual(2, len(self.solenoids[22]["spatial"]["placements"]))
		self.assertEqual(2, len(self.solenoids[23]["spatial"]["placements"]))
		# 24 is drawn on one dome and on a render light under the ramp, which is not placed.
		self.assertEqual(curate_class_of_1812.norm(674.6027, 259.50006), xy(self.solenoids[24]))  # Light F24a
		self.assertIn("Blue dome and under ramp", self.solenoids[24]["physical"]["notes"])
		self.assertEqual("effect", self.solenoids[10]["spatial"]["placements"][0]["role"])

	def test_rear_toys_are_clamped_to_the_rear_edge_and_cite_the_photos(self) -> None:
		def placement(device):
			(item,) = device["spatial"]["placements"]
			return item

		for device, mesh, photo in (
			(self.solenoids[11], "heart", curate_class_of_1812.HEART_PHOTO_SOURCE),
			(self.solenoids[25], "heart", curate_class_of_1812.HEART_PHOTO_SOURCE),
			(self.solenoids[12], "BottomTeeth", curate_class_of_1812.TEETH_PHOTO_SOURCE),
			(self.lamps[2], "TopTeeth", curate_class_of_1812.TEETH_PHOTO_SOURCE),
		):
			with self.subTest(device=device["id"]):
				x, y = curate_class_of_1812.MESH_POINTS[mesh]
				self.assertLess(y, 0)
				item = placement(device)
				self.assertEqual((round(x / 952, 6), 0.0), (item["x"], item["y"]))
				self.assertIn(photo, item["provenance"]["source_refs"])
				self.assertIn(f"raw centre ({x}, {y})", device["physical"]["notes"])

	def test_switch_44_placement_cites_the_probes_and_the_later_binding(self) -> None:
		refs = self.switches[44]["spatial"]["placements"][0]["provenance"]["source_refs"]
		self.assertIn(curate_class_of_1812.RUNTIME_SOURCE, refs)
		self.assertIn(curate_class_of_1812.LATER_SCRIPT_SOURCE, refs)

	def test_trough_probes_settle_switch_44(self) -> None:
		def steps(run: str) -> tuple[str, str]:
			match = re.search(r"Ball release 28 rose on steps (\[[\d, ]*\]), outhole 29 on steps (\[[\d, ]*\])", self.runs[run]["note"])
			self.assertIsNotNone(match, run)
			return match.group(1), match.group(2)

		# Held closed, the ROM serves a ball on tilt pulses 3 and 6 with the tilted ball still out.
		self.assertEqual(("[4, 11, 14, 27]", "[27]"), steps("tilt-trough-closed"))
		self.assertIn("11 tilt switch -7 pulse 3: solenoids rising [8, 9, 14, 28, 32]", self.runs["tilt-trough-closed"]["note"])
		# Opened after the release, it serves the next ball only once 44 closes again after the drain.
		self.assertEqual(("[4, 31]", "[28]"), steps("tilt-trough-open"))
		self.assertIn("30 trough switch 44 closed again: solenoids rising [8, 32]", self.runs["tilt-trough-open"]["note"])
		notes = self.switches[44]["physical"]["notes"]
		self.assertIn("The ROM thus reads 44 at 1 as both balls home in the trough", notes)
		self.assertIn("Kicker Slot2, the trough's second position", notes)
		self.assertIn(curate_class_of_1812.LATER_SCRIPT_SOURCE, self.switches[44]["provenance"]["source_refs"])
		(trough,) = [m for m in self.definition["mechanisms"] if m["id"] == "mechanism.trough"]
		self.assertIn("The ROM reads TROUGH (44) at 1 as both balls home", trough["behavior"])

	def test_insert_lamps_are_disclosed_projections(self) -> None:
		report = load(ROOT / curate_class_of_1812.SPATIAL_REPORT_PATH.relative_to(ROOT))
		projected = {entry["address"] for entry in report["projections"] if entry["reason"] == curate_class_of_1812.INSERT_PROJECTION}
		self.assertEqual(set(curate_class_of_1812.INSERT_LAMPS), projected)
		self.assertEqual(82, len(projected))
		for address in projected:
			with self.subTest(address=address):
				self.assertIn("not a measured socket", self.lamps[address]["physical"]["notes"])

	def test_table_defects_are_recorded_on_devices_not_as_conflicts(self) -> None:
		self.assertIn("TiltSwitch = 151", self.switches[-7]["physical"]["notes"])
		self.assertIn("a defect in that table", self.switches[44]["physical"]["notes"])
		self.assertIn("'Right Ramp Million (Right)', is an annotation defect", self.lamps[47]["physical"]["notes"])
		self.assertIn(curate_class_of_1812.RIGHT_RAMP_PHOTO_SOURCE, self.lamps[47]["provenance"]["source_refs"])
		self.assertIn("a comment defect", self.switches[6]["physical"]["notes"])
		excerpt = (EXCERPTS / "nztt-script-bindings.md").read_text(encoding="utf-8")
		self.assertIn("`vpmNudge.TiltSwitch = 151`", excerpt)
		self.assertIn("`If keycode = LeftFlipperKey then Controller.switch(4)=1`", excerpt)
		self.assertIn("`Sub Slot2_Hit():Controller.Switch(44) = 1:UpdateTrough:End Sub`", excerpt)
		library = (EXCERPTS / "vpm-script-library.md").read_text(encoding="utf-8")
		self.assertIn("`Const swLRFlip = 141 '06`", library)

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curate_class_of_1812.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curate_class_of_1812.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())

	def test_check_refuses_line_ending_drift_in_markdown(self) -> None:
		paths = [
			curate_class_of_1812.DEFINITION_PATH, curate_class_of_1812.SEED_PATH, curate_class_of_1812.SPATIAL_REPORT_PATH,
			curate_class_of_1812.SPATIAL_REPORT_MARKDOWN_PATH, ROOT / curate_class_of_1812.KNOWLEDGE_PATH,
			curate_class_of_1812.KNOWLEDGE_SEED_PATH,
		]
		for target, message in (
			(curate_class_of_1812.SPATIAL_REPORT_MARKDOWN_PATH, "spatial review drifted"),
			(ROOT / curate_class_of_1812.KNOWLEDGE_PATH, "knowledge note is not byte-identical"),
			(curate_class_of_1812.KNOWLEDGE_SEED_PATH, "carriage return"),
		):
			with self.subTest(target=target.name), tempfile.TemporaryDirectory() as temporary:
				root = Path(temporary)
				for path in paths:
					copy = root / path.relative_to(ROOT)
					copy.parent.mkdir(parents=True, exist_ok=True)
					copy.write_bytes(path.read_bytes())
				curate_class_of_1812.check(root)
				drifted = root / target.relative_to(ROOT)
				drifted.write_bytes(drifted.read_bytes().replace(b"\n", b"\r\n"))
				with self.assertRaisesRegex(RuntimeError, message):
					curate_class_of_1812.check(root)

	def test_unsettled_gate_lock_knocker_and_coin_doors_are_disclosed(self) -> None:
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		gate = mechanisms["mechanism.kickers-and-gate"]["behavior"]
		self.assertIn("Unresolved", gate)
		self.assertIn("which path the gate opens", gate)
		self.assertIn(curate_class_of_1812.CARDS_SOURCE, mechanisms["mechanism.kickers-and-gate"]["provenance"]["source_refs"])
		self.assertIn("fitment stays unknown", self.solenoids[30]["physical"]["notes"])
		for address in (0, 1, 2):
			with self.subTest(coin=address):
				refs = self.switches[address]["provenance"]["source_refs"]
				self.assertIn(curate_class_of_1812.TWO_SLOT_DOOR_PHOTO_SOURCE, refs)
				self.assertIn(curate_class_of_1812.ONE_SLOT_DOOR_PHOTO_SOURCE, refs)
				self.assertIn("doors differ", self.switches[address]["physical"]["notes"])
		for address in curate_class_of_1812.LED_LAMPS:
			with self.subTest(lamp=address):
				self.assertIn(curate_class_of_1812.BAT_O_METER_PHOTO_SOURCE, self.lamps[address]["provenance"]["source_refs"])
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("**mechanism_behavior.**", knowledge)
		self.assertNotIn("stack of inserts", knowledge)

	def test_source_licences_and_ipdb_capture(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		# gts3.c, gts3games.c and core.c carry no '// license:BSD-3-Clause' line, so they keep the old MAME licence.
		self.assertEqual("LicenseRef-PinMAME-Old-MAME", sources[curate_class_of_1812.CORE_SOURCE]["license"])
		page = sources[curate_class_of_1812.IDENTITY_SOURCE]
		self.assertEqual(
			f"https://web.archive.org/web/{curate_class_of_1812.IPDB_PAGE_CAPTURE}id_/https://www.ipdb.org/machine.cgi?id=528", page["uri"],
		)
		self.assertIn("https://www.ipdb.org/machine.cgi?id=528", page["locator"])
		for number, (capture, sha256, caption, size, photographer) in curate_class_of_1812.PHOTOS.items():
			with self.subTest(photo=number):
				record = next(source for source in sources.values() if source.get("original_filename") == f"image-{number}.jpg")
				self.assertEqual(f"https://web.archive.org/web/{capture}id_/https://www.ipdb.org/images/528/image-{number}.jpg", record["uri"])
				self.assertEqual(sha256, record["sha256"])
				self.assertIn(f"'{caption}' ({photographer}), a {size} JPEG", record["locator"])
				self.assertIn(sha256, (EXCERPTS / f"ipdb-photo-{number}.md").read_text(encoding="utf-8"))

	def test_excerpt_digests_match(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
		self.assertEqual(11, count)
		self.assertEqual(11, len(list(EXCERPTS.glob("*.md"))))

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# beav_butt is the excluded clone the identity notes name on purpose.
		foreign = {d["id"] for d in catalog["drivers"] if d["id"] not in ("clas1812", "beav_butt") and re.search(r"\d|_", d["id"]) and len(d["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class ClassOf1812RetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import class_of_1812_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = class_of_1812_runtime_evidence.working_root()
		if not (review_root / class_of_1812_runtime_evidence.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Class of 1812 runs are not present under this review-artifacts root")
		self.assertEqual(canonical_bytes(class_of_1812_runtime_evidence.build(review_root)), curate_class_of_1812.RUNTIME_EVIDENCE_PATH.read_bytes())

	def test_unexplained_lamp_rises_match_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import class_of_1812_runtime_evidence

		runs = class_of_1812_runtime_evidence.working_root() / class_of_1812_runtime_evidence.RUNTIME_RELATIVE / "runs"
		if not runs.is_dir():
			self.skipTest("retained Class of 1812 runs are not present under this review-artifacts root")

		def rises(name: str, lamp: int) -> list[float]:
			data = json.loads((runs / f"clas1812-{name}.json").read_text(encoding="utf-8"))
			return [e["time_s"] for e in data["events"] if e["event"] == "lamp" and e["number"] == lamp and e["state"]]

		gameplay = json.loads((runs / "clas1812-gameplay.json").read_text(encoding="utf-8"))
		held = [e["time_s"] for e in gameplay["events"] if e["event"] == "switch" and e["number"] == 52]
		for lamp, (game, closed, opened, upkicker) in curate_class_of_1812.UNEXPLAINED_LAMPS.items():
			with self.subTest(lamp=lamp):
				self.assertEqual(game, len(rises("gameplay", lamp)))
				self.assertEqual(upkicker, sum(1 for t in rises("gameplay", lamp) if held[0] <= t <= held[-1]))
				self.assertEqual(closed, len(rises("tilt-trough-closed", lamp)))
				self.assertEqual(opened, len(rises("tilt-trough-open", lamp)))
		# Lamp 1 rises only inside the self-tests.
		for name in ("gameplay", "tilt-trough-closed", "tilt-trough-open"):
			self.assertEqual([], rises(name, 1))

	def test_teeth_bursts_match_the_raw_gameplay_run(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import class_of_1812_runtime_evidence

		path = class_of_1812_runtime_evidence.working_root() / class_of_1812_runtime_evidence.RUNTIME_RELATIVE / "runs" / "clas1812-gameplay.json"
		if not path.is_file():
			self.skipTest("retained Class of 1812 runs are not present under this review-artifacts root")
		events = json.loads(path.read_text(encoding="utf-8"))["events"]

		def rises(kind: str, number: int) -> list[float]:
			return [e["time_s"] for e in events if e["event"] == kind and e["number"] == number and e["state"]]

		start, spinner = rises("switch", 3)[0], rises("switch", 15)
		pulses, rose = [], None
		for e in events:
			if e["event"] == "solenoid" and e["number"] == 12:
				if e["state"] and rose is None:
					rose = e["time_s"]
				elif not e["state"] and rose is not None:
					pulses.append((rose, e["time_s"] - rose))
					rose = None
		self.assertIsNone(rose)
		self.assertEqual(2, len(spinner))
		first = [(t, width) for t, width in pulses if t < spinner[0]]
		second = [(t, width) for t, width in pulses if t >= spinner[0]]
		words = {13: "thirteen", 16: "sixteen"}
		self.assertEqual((16, 13), (len(first), len(second)))
		self.assertLess(second[0][0] - spinner[0], 0.1)
		rest = [width for _, width in first[1:]]
		widths = [width for _, width in second]
		expected = (
			f"{words[len(first)]} from about {first[0][0] - start:.1f} s to {first[-1][0] - start:.1f} s after Start, the "
			f"first held about {first[0][1]:.1f} s and the others {min(rest):.2f}-{max(rest):.2f} s, and {words[len(second)]} "
			f"of {min(widths):.2f}-{max(widths):.2f} s each over about {second[-1][0] - second[0][0]:.1f} s, beginning within "
			f"0.1 s of the first of two spinner pulses {spinner[1] - spinner[0]:.1f} s apart"
		)
		self.assertEqual("sixteen from about 2.5 s to 8.2 s after Start, the first held about 1.1 s and the others 0.06-0.34 s, "
			"and thirteen of 0.06-0.07 s each over about 1.7 s, beginning within 0.1 s of the first of two spinner pulses "
			"0.8 s apart", expected)
		knowledge = " ".join(KNOWLEDGE_PATH.read_text(encoding="utf-8").split())
		self.assertIn(expected, knowledge)
		definition = load(DEFINITION_PATH)
		teeth = next(o for o in definition["outputs"] if o["binding"] == {"group": "pinmame.output.solenoid", "device": 12})
		mechanism = next(m for m in definition["mechanisms"] if m["id"] == "mechanism.heart-and-teeth")
		self.assertIn(expected, teeth["physical"]["notes"])
		self.assertIn(expected, mechanism["behavior"])

	def test_front_door_reader_refuses_another_page_and_a_wrong_counter(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import class_of_1812_runtime_evidence as evidence

		runtime = evidence.working_root() / evidence.RUNTIME_RELATIVE
		if not (runtime / "runs").is_dir():
			self.skipTest("retained Class of 1812 runs are not present under this review-artifacts root")
		self.assertTrue(evidence.front_door(evidence.Run(runtime, "front-door"))["note"].startswith("Self-test 9;"))

		def mutated(change) -> object:
			run = evidence.Run(runtime, "front-door")
			for texts in (run.step_held_text, run.step_text):
				for number, lines in texts.items():
					texts[number] = change(list(lines))
			return run

		with self.assertRaisesRegex(RuntimeError, "does not show the FRONT DOOR TEST page"):
			evidence.front_door(mutated(lambda lines: [line.replace("FRONT DOOR TEST", "SOUND TEST") for line in lines]))
		with self.assertRaisesRegex(RuntimeError, "moved the counters"):
			evidence.front_door(mutated(lambda lines: [line.replace("C- 1", "C- O") for line in lines]))
		# A wrong page in the settled frame alone, behind a correct held frame, is refused too.
		run = evidence.Run(runtime, "front-door")
		coin_step = next(step["step"] for step in run.data["steps"] if step.get("switch") == 2)
		run.step_text[coin_step] = ["SOUND TEST"] + list(run.step_text[coin_step][1:])
		with self.assertRaisesRegex(RuntimeError, "does not show the FRONT DOOR TEST page"):
			evidence.front_door(run)
		# A coin press without its held frame is refused.
		run = evidence.Run(runtime, "front-door")
		del run.step_held_text[coin_step]
		with self.assertRaisesRegex(RuntimeError, "lacks its held or its settled frame"):
			evidence.front_door(run)
		# A run without its coin presses is refused.
		run = evidence.Run(runtime, "front-door")
		run.data["steps"] = [step for step in run.data["steps"] if step.get("switch") not in (0, 1, 2)]
		with self.assertRaisesRegex(RuntimeError, "pressed coin switches"):
			evidence.front_door(run)

	def test_the_scripted_game_lit_the_lock_but_never_fired_the_gate(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import class_of_1812_runtime_evidence as evidence

		runs = evidence.working_root() / evidence.RUNTIME_RELATIVE / "runs"
		if not runs.is_dir():
			self.skipTest("retained Class of 1812 runs are not present under this review-artifacts root")

		def events(name: str) -> list[dict]:
			return json.loads((runs / f"clas1812-{name}.json").read_text(encoding="utf-8"))["events"]

		gameplay = events("gameplay")

		def lamp_state(lamp: int, at: float) -> int:
			state = 0
			for e in gameplay:
				if e["event"] == "lamp" and e["number"] == lamp and e["time_s"] <= at:
					state = e["state"]
			return state

		def lamp_edges(lamp: int, start: float, end: float) -> list[float]:
			return [e["time_s"] for e in gameplay if e["event"] == "lamp" and e["number"] == lamp and start <= e["time_s"] < end]

		bank = [e["time_s"] for e in gameplay if e["event"] == "switch" and e["number"] == 46 and e["state"]][0]
		ramp = [e["time_s"] for e in gameplay if e["event"] == "switch" and e["number"] == 50 and e["state"]]
		self.assertEqual(1, len(ramp))
		# L DT LIGHT LOCK was lit when the fourth left target fell, and went out.
		self.assertEqual((1, 0), (lamp_state(65, bank - 0.01), lamp_state(65, bank + 1.0)))
		self.assertEqual(0, lamp_state(65, ramp[0]))
		# R BB LOCK flashed twice at once (four edges within 0.5 s), stayed dark until about 12 s later, and then flashed
		# with no edge more than 0.6 s from the next until a second after the ramp pulse.
		edges = lamp_edges(47, bank, ramp[0] + 1.0)
		burst = [t for t in edges if t < bank + 0.5]
		self.assertEqual(4, len(burst))
		resume = next(t for t in edges if t >= bank + 0.5)
		self.assertEqual(12, round(resume - bank))
		steady = [t for t in edges if t >= resume]
		self.assertGreater(len(steady), 20)
		self.assertLess(max(later - earlier for earlier, later in zip(steady, steady[1:])), 0.6)
		self.assertLess(steady[0], ramp[0])
		self.assertGreater(steady[-1], ramp[0] + 0.5)
		# The top kicker was held only before the bank fell, and the gate rose only in the coil test.
		self.assertTrue(all(e["time_s"] < bank for e in gameplay if e["event"] == "switch" and e["number"] == 53))
		for name in evidence.RUNS:
			with self.subTest(run=name):
				rises = sum(1 for e in events(name) if e["event"] == "solenoid" and e["number"] == 10 and e["state"])
				self.assertEqual(1 if name == "solenoids" else 0, rises)
		gate = next(m for m in load(DEFINITION_PATH)["mechanisms"] if m["id"] == "mechanism.kickers-and-gate")["behavior"]
		self.assertIn("R BB LOCK (47) flashed twice at once, stayed dark until about 12 s later and then flashed through one", gate)
		self.assertIn("which fired no gate and left 47 flashing", gate)
		self.assertIn("10 rose only in the coil test", gate)

	def test_retained_sources_match_their_recorded_hashes(self) -> None:
		manuals, review = os.environ.get("PINMAME_MANUALS_ROOT"), os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals and not review:
			self.skipTest("neither PINMAME_MANUALS_ROOT nor PINMAME_REVIEW_ARTIFACTS_ROOT configured")
		expected: dict[Path, str] = {}
		if manuals:
			ipdb = Path(manuals) / "by-machine" / curate_class_of_1812.MACHINE_ID / "ipdb"
			if ipdb.is_dir():
				expected[ipdb / f"ipdb-528-wayback-{curate_class_of_1812.IPDB_PAGE_CAPTURE}.html"] = curate_class_of_1812.IPDB_PAGE_SHA256
				expected[ipdb / curate_class_of_1812.CARDS_ZIP_NAME] = curate_class_of_1812.CARDS_ZIP_SHA256
				expected[ipdb / "cards-extracted" / "Gottlieb_Class_of_1812_instruction_cards.pdf"] = curate_class_of_1812.CARDS_PDF_SHA256
				for number, (_, sha256, *_rest) in curate_class_of_1812.PHOTOS.items():
					expected[ipdb / "photos" / f"image-{number}.jpg"] = sha256
		if review:
			libraries = Path(review) / "vpm-script-libs"
			if libraries.is_dir():
				expected[libraries / "Class1812.vbs"] = curate_class_of_1812.VPM_LIBRARY_SHA256
				expected[libraries / "core.vbs"] = curate_class_of_1812.VPM_CORE_SHA256
		if not expected:
			self.skipTest("the retained Class of 1812 sources are not present under the configured roots")
		for path, sha256 in expected.items():
			with self.subTest(path=path.name):
				self.assertEqual(sha256, hashlib.sha256(path.read_bytes()).hexdigest())

	def test_placements_match_the_retained_table(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		root = Path(value).expanduser().resolve()
		if not (root / curate_class_of_1812.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Class of 1812 table is not present under this root")
		curate_class_of_1812.verify_retained_table(root)

	def test_retained_table_verifier_refuses_a_moved_point(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value or not (Path(value) / curate_class_of_1812.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Class of 1812 table is not present")
		kind, x, y = curate_class_of_1812.TABLE_POINTS["sw24"]
		original = dict(curate_class_of_1812.TABLE_POINTS)
		curate_class_of_1812.TABLE_POINTS["sw24"] = (kind, x + 1.0, y)
		try:
			with self.assertRaisesRegex(RuntimeError, "sw24"):
				curate_class_of_1812.verify_retained_table(Path(value).expanduser().resolve())
		finally:
			curate_class_of_1812.TABLE_POINTS.clear()
			curate_class_of_1812.TABLE_POINTS.update(original)

	def test_retained_table_verifier_refuses_a_moved_bulb_and_wrong_bounds(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value or not (Path(value) / curate_class_of_1812.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Class of 1812 table is not present")
		root = Path(value).expanduser().resolve()
		x, y = curate_class_of_1812.MESH_POINTS["bulb1"]
		original = dict(curate_class_of_1812.MESH_POINTS)
		curate_class_of_1812.MESH_POINTS["bulb1"] = (x + 1.0, y)
		try:
			with self.assertRaisesRegex(RuntimeError, "mesh points"):
				curate_class_of_1812.verify_retained_table(root)
		finally:
			curate_class_of_1812.MESH_POINTS.clear()
			curate_class_of_1812.MESH_POINTS.update(original)
		height = curate_class_of_1812.PLAYFIELD_HEIGHT
		curate_class_of_1812.PLAYFIELD_HEIGHT = 1990.0
		try:
			with self.assertRaisesRegex(RuntimeError, "bounds"):
				curate_class_of_1812.verify_retained_table(root)
		finally:
			curate_class_of_1812.PLAYFIELD_HEIGHT = height

	def test_retained_table_verifier_refuses_a_render_light_as_a_socket(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value or not (Path(value) / curate_class_of_1812.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Class of 1812 table is not present")
		root = Path(value).expanduser().resolve()
		original = curate_class_of_1812.GI_BULBS
		curate_class_of_1812.GI_BULBS = original + ("light18",)
		try:
			with self.assertRaisesRegex(RuntimeError, "light18 no longer shows a bulb mesh"):
				curate_class_of_1812.verify_retained_table(root)
		finally:
			curate_class_of_1812.GI_BULBS = original

	def test_retained_table_verifier_refuses_a_moved_mesh(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value or not (Path(value) / curate_class_of_1812.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Class of 1812 table is not present")
		x, y = curate_class_of_1812.MESH_POINTS["heart"]
		original = dict(curate_class_of_1812.MESH_POINTS)
		curate_class_of_1812.MESH_POINTS["heart"] = (x, y + 1.0)
		try:
			with self.assertRaisesRegex(RuntimeError, "mesh points"):
				curate_class_of_1812.verify_retained_table(Path(value).expanduser().resolve())
		finally:
			curate_class_of_1812.MESH_POINTS.clear()
			curate_class_of_1812.MESH_POINTS.update(original)


if __name__ == "__main__":
	unittest.main()
