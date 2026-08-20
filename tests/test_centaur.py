"""Regression tests for the Bally Centaur definition and the Bally MPU-35 profile.

The solenoid numbering here is the expensive fact: the manual's printed Self Test
number and PinMAME's public solenoid address are two different numberings, and
neither retained community script matches the manual. The mapping asserted below
was read off the ROM's own solenoid self test, which pulses each coil while
displaying that coil's identification number. Anything that quietly "tidies" it
back into an identity mapping is a regression.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "centaur-1981.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "by35" / "centaur-solenoid-self-test.json"

MANUAL_SHA256 = "9893d29ee871fd8c0a2afea35e931f107fb97a8156739035e005b15fd879e7ea"
TRANSCRIPTION_SHA256 = "b2c47f5ddb5f7f22ffa680e01f8fcf84512f6afabfdc1d408b1fe45a89189c05"
TRACE_SHA256 = "e5ea81fea6bea18964708637a3486637d5d2e9045841ea2994f604863940327a"

# printed Self Test number -> (public PinMAME solenoid address, semantic device id)
#
# Asserting the device id as well as the address is the point: comparing only alias values lets a
# swap of two labels - exactly the off-by-one the legacy import already contained on the right
# four-bank - pass silently.
SELF_TEST_TO_PUBLIC_SOLENOID = {
	1: (7, "device.outhole-kicker"),
	2: (6, "device.knocker"),
	3: (8, "device.inline-drop-target-reset"),
	4: (9, "device.right-4-drop-target-reset"),
	5: (10, "device.left-thumper-bumper"),
	6: (11, "device.right-thumper-bumper"),
	7: (12, "device.left-slingshot"),
	8: (13, "device.right-slingshot"),
	9: (1, "device.orbs-target-reset"),
	10: (2, "device.right-4-drop-target-1-top"),
	11: (3, "device.right-4-drop-target-2"),
	12: (4, "device.right-4-drop-target-3"),
	13: (5, "device.right-4-drop-target-4-bottom"),
	14: (15, "device.ball-release"),
	15: (14, "device.ball-kick-to-playfield"),
	16: (18, "device.coin-lockout-door"),
	17: (19, "device.k1-relay-flipper-enable"),
	18: (20, "device.magnet"),
}

UNUSED_SWITCH_ADDRESSES = (7, 13, 14, 23, 35, 36)

# addresses the manual prints with a parenthesised physical quantity
SHARED_SWITCH_QUANTITIES = {12: 4, 15: 3, 16: 2, 18: 2, 21: 2, 34: 5}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class CentaurDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.inputs = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		cls.dips = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		}
		cls.solenoids = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.centaur.1981", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1981, machine["year"])
		self.assertEqual(476, machine["ipdb_id"])

	def test_controller_platform_is_the_bally_mpu_35_profile(self) -> None:
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertEqual("pinmame.by35", self.profile["id"])
		self.assertEqual("Bally MPU AS-2518-35", self.profile["hardware_family"])

	def test_driver_variants_are_the_same_physical_machine(self) -> None:
		drivers = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual({"centaur", "centaura", "centaurb"}, drivers)
		# The Inder game of the same name is a different physical machine and must not be grouped.
		self.assertNotIn("centauri", drivers)
		self.assertNotIn("centaurj", drivers)

	def test_solenoid_self_test_numbers_map_to_the_observed_public_addresses(self) -> None:
		for self_test, (public, device_id) in SELF_TEST_TO_PUBLIC_SOLENOID.items():
			device = self.solenoids.get(public)
			self.assertIsNotNone(device, f"public solenoid {public} is missing")
			aliases = {
				alias["value"]
				for alias in device["aliases"]
				if alias["namespace"] == "manual.self-test"
			}
			self.assertEqual({f"{self_test:02d}"}, aliases, f"public solenoid {public}")
			self.assertEqual(device_id, device["id"], f"public solenoid {public}")

	def test_committed_runtime_evidence_carries_the_same_mapping(self) -> None:
		"""The definition and the evidence artifact must not be able to drift apart."""
		evidence = load_json(EVIDENCE_PATH)
		observed = evidence["runtime"]["observations"]["physical_service_solenoid_to_public"]
		expected = {
			str(self_test): public
			for self_test, (public, _) in SELF_TEST_TO_PUBLIC_SOLENOID.items()
		}
		self.assertEqual(expected, observed)
		self.assertEqual(["centaur"], evidence["driver_ids"])
		self.assertEqual(["bally.centaur.1981"], evidence["machine_ids"])

	def test_every_observed_lamp_address_is_declared(self) -> None:
		"""Observing an address and not declaring it is silent under-reporting."""
		evidence = load_json(EVIDENCE_PATH)
		observed = set(evidence["runtime"]["observations"]["lamp_addresses_seen"])
		declared = {
			item["binding"]["device"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual(set(), observed - declared, "observed lamp addresses are undeclared")

	def test_solenoid_alias_namespace_is_consistent(self) -> None:
		"""A consumer enumerating one namespace must not silently drop devices."""
		namespaces = {
			alias["namespace"]
			for device in self.solenoids.values()
			for alias in device["aliases"]
			if alias["namespace"].startswith("pinmame.")
		}
		self.assertEqual({"pinmame.coil"}, namespaces)

	def test_printed_fourteen_and_fifteen_are_transposed(self) -> None:
		"""The single easiest thing to get wrong: the numbers collide but the devices swap."""
		self.assertEqual("device.ball-kick-to-playfield", self.solenoids[14]["id"])
		self.assertEqual("device.ball-release", self.solenoids[15]["id"])

	def test_public_seven_is_the_outhole_kicker_not_a_ball_release(self) -> None:
		"""Both retained community scripts label public 7 a release to the shooter lane."""
		self.assertEqual("device.outhole-kicker", self.solenoids[7]["id"])

	def test_magnet_and_flipper_relay_are_present_on_the_continuous_outputs(self) -> None:
		self.assertEqual("device.magnet", self.solenoids[20]["id"])
		self.assertEqual("magnet", self.solenoids[20]["kind"])
		self.assertEqual("device.k1-relay-flipper-enable", self.solenoids[19]["id"])
		self.assertEqual("relay", self.solenoids[19]["kind"])

	def test_continuous_output_one_is_the_sixth_switch_column_strobe(self) -> None:
		"""Public 17 is a strobe, not a coil, which is why it never pulses and never releases.

		A continuous output that is held never appears as a pulse, so the absence of a pulse in the
		self-test trace was never evidence that the address is unused - an inference an earlier pass
		got wrong. It reads as permanently asserted because by35.c OR-accumulates solenoid state
		within each VBLANK window, so a line toggling faster than VBLANK looks continuously on.
		"""
		device = self.solenoids[17]
		self.assertEqual("used", device["availability"])
		self.assertEqual("control_signal", device["kind"])
		self.assertEqual("validated", device["provenance"]["status"])
		self.assertIn("strobe", device["label"].lower())
		# The two recorded conflicts are both auxiliary-lamp matters; nothing disputes this strobe.
		self.assertTrue(
			all(conflict["id"].startswith("conflict.aux-lamp-") for conflict in self.definition["conflicts"])
		)
		# The conflicts are real and now cost the score, but neither is about this address.
		self.assertNotIn("coil.driver-17", [conflict["path"] for conflict in self.definition["conflicts"]])

	def test_every_mpu_option_switch_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 33)), set(self.dips))
		# All 32 now carry a function: 28 from the printed manual, and 17-20 as the centre coin
		# chute selector, which the manual omits but the community option-switch documentation
		# carried by all four retained tables supplies.
		self.assertEqual(set(), {n for n, i in self.dips.items() if i["availability"] != "used"})

	def test_mechanisms_are_documented_and_own_their_hardware_once(self) -> None:
		mechanisms = self.definition["mechanisms"]
		self.assertGreaterEqual(len(mechanisms), 10)
		owned: dict[str, str] = {}
		for mechanism in mechanisms:
			self.assertTrue(mechanism["behavior"].strip())
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owned, f"{actuator} claimed twice")
				owned[actuator] = mechanism["id"]
		names = {mechanism["id"] for mechanism in mechanisms}
		self.assertIn("mech.captive-orb-store", names)
		self.assertIn("mech.inline-drop-target-bank", names)
		# The orb store is game state, not hardware: the trough owns the coils.
		orb = next(m for m in mechanisms if m["id"] == "mech.captive-orb-store")
		self.assertEqual([], orb["actuators"])

	def test_switch_polarity_is_declared(self) -> None:
		for address, item in self.inputs.items():
			if item["availability"] in {"used", "optional"}:
				self.assertIsInstance(item.get("normally_closed"), bool, f"switch {address}")

	def test_every_declared_solenoid_is_legal_for_the_profile(self) -> None:
		group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.solenoid")
		allowed = set()
		for rule in group["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		for address in self.solenoids:
			self.assertIn(address, allowed, f"solenoid {address} is outside the profile")

	def test_switch_matrix_covers_the_printed_forty_eight_addresses(self) -> None:
		matrix = {address for address in self.inputs if 1 <= address <= 48}
		self.assertEqual(set(range(1, 49)), matrix)

	def test_blank_switch_positions_are_declared_unused(self) -> None:
		for address in UNUSED_SWITCH_ADDRESSES:
			device = self.inputs[address]
			self.assertEqual("unused", device["availability"], f"switch {address}")

	def test_shared_switch_addresses_record_their_physical_quantity(self) -> None:
		for address, quantity in SHARED_SWITCH_QUANTITIES.items():
			device = self.inputs[address]
			self.assertEqual(
				quantity,
				device.get("physical", {}).get("quantity"),
				f"switch {address} should record {quantity} physical contacts",
			)

	def test_legacy_switch_label_conflicts_are_resolved_from_the_manual(self) -> None:
		"""All seven inherited conflicts; the platform source was right in every case."""
		self.assertEqual("switch.5th-ball-trough", self.inputs[2]["id"])
		self.assertEqual("switch.credit-button", self.inputs[6]["id"])
		self.assertEqual("switch.coin-3-right", self.inputs[9]["id"])
		self.assertEqual("switch.coin-1-left", self.inputs[10]["id"])
		self.assertEqual("switch.coin-2-middle", self.inputs[11]["id"])
		self.assertEqual("switch.slam", self.inputs[16]["id"])
		# Neither legacy source was right about 7: the manual prints no description there.
		self.assertEqual("unused", self.inputs[7]["availability"])
		# All seven legacy label conflicts are gone; the only conflict left is a new, honest one.
		switch_conflicts = [
			conflict for conflict in self.definition["conflicts"]
			if conflict["path"].startswith("binding:pinmame.input.switch")
		]
		self.assertEqual([], switch_conflicts)

	def test_display_inventory_matches_dispby7(self) -> None:
		displays = {item["controller_index"]: item for item in self.definition["displays"]}
		self.assertEqual(set(range(6)), set(displays))
		for index in range(4):
			self.assertIn("Player", displays[index]["label"])
			self.assertIn("seven digits", displays[index]["label"])
		self.assertIn("two digits", displays[4]["label"])
		self.assertIn("two digits", displays[5]["label"])
		for display in displays.values():
			self.assertEqual("segment", display["kind"])
			# Backbox devices never carry playfield coordinates.
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_definition_cites_the_manual_and_the_runtime_scenario(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("manual.bally.centaur.1981", sources)
		self.assertIn("runtime.centaur.solenoid-self-test", sources)
		self.assertEqual("runtime_scenario", sources["runtime.centaur.solenoid-self-test"]["kind"])
		manual = sources["manual.bally.centaur.1981"]
		# The hash belongs in the typed field, not smuggled into free-text prose.
		self.assertEqual(MANUAL_SHA256, manual["sha256"])
		self.assertTrue(manual["uri"].startswith("external:pinmame-manuals/"))
		for field in ("license", "attribution", "original_filename", "rights", "acquired_at"):
			self.assertIn(field, manual)
		self.assertEqual(3, len(manual["excerpts"]))
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), path)
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])
			self.assertTrue((ROOT / excerpt["image"]).is_file(), excerpt["id"])
			self.assertTrue(excerpt["reviewed"])
		runtime = sources["runtime.centaur.solenoid-self-test"]
		self.assertEqual(
			"internal:evidence/runtime/by35/centaur-solenoid-self-test.json", runtime["uri"]
		)
		self.assertEqual("NOASSERTION", runtime["license"])
		self.assertIn("manual-support.bally.centaur.1981", sources)
		self.assertEqual(TRANSCRIPTION_SHA256, sources["manual-support.bally.centaur.1981"]["sha256"])

	def test_retained_evidence_hashes_match_when_the_roots_are_available(self) -> None:
		"""With the evidence roots set, prove the asserted hashes against the real files."""
		import hashlib
		import os

		manuals_root = os.environ.get("PINMAME_MANUALS_ROOT")
		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals_root or not artifacts_root:
			self.skipTest("evidence roots are not configured")
		pdf = (
			Path(manuals_root)
			/ "by-machine"
			/ "bally.centaur.1981"
			/ "archive-bally-1981-english-manual"
			/ "Bally 1981 English Manual.pdf"
		)
		transcription = Path(artifacts_root) / "centaur-1981" / "manual-transcription.md"
		for path, expected in ((pdf, MANUAL_SHA256), (transcription, TRANSCRIPTION_SHA256)):
			self.assertTrue(path.is_file(), f"missing retained evidence: {path}")
			digest = hashlib.sha256()
			with open(path, "rb") as handle:
				for chunk in iter(lambda: handle.read(1 << 20), b""):
					digest.update(chunk)
			self.assertEqual(expected, digest.hexdigest(), str(path))

	def test_synthetic_flipper_coils_are_declared(self) -> None:
		"""The flippers are real coils; PinMAME just addresses them synthetically."""
		self.assertEqual("device.flipper-lower-right", self.solenoids[46]["id"])
		self.assertEqual("device.flipper-lower-left", self.solenoids[48]["id"])
		for address in (46, 48):
			self.assertEqual("coil", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])

	def test_unenumerated_dips_are_admitted_rather_than_implied_complete(self) -> None:
		"""The MPU has 32 physical option switches and this record enumerates none."""
		dips = [
			item for item in self.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		]
		if not dips:
			self.assertIn("input_enumeration", self.definition["coverage"]["missing"])
			self.assertIn("input_semantics", self.definition["coverage"]["missing"])

	def test_coverage_does_not_claim_more_than_the_devices_support(self) -> None:
		"""Naming cannot be validated while the largest device class is legacy carry-over."""
		lamps = [
			item for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		]
		statuses = {item["provenance"]["status"] for item in lamps}
		if statuses - {"validated"}:
			self.assertNotEqual("validated", self.definition["coverage"]["dimensions"]["semantic_naming"])
			self.assertIn("output_semantics", self.definition["coverage"]["missing"])

	def test_mapping_is_rederived_from_the_raw_trace_when_it_is_available(self) -> None:
		"""Re-derive the mapping from the ROM's own output, not from a second copied table.

		The naive version of this test built a dict and let later observations overwrite earlier
		ones, which hid a genuine contradiction: an early boot-time pairing yields 11 -> 19 before
		the steady-state cycle yields 11 -> 3. Overwriting made the assertion pass for the wrong
		reason. This version instead splits the trace into complete ordered 01..18 cycles and
		requires every complete cycle to equal the expected mapping independently, so a
		contradictory or partial observation fails rather than being silently replaced.
		"""
		import hashlib
		import json
		import os

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("evidence roots are not configured")
		trace = Path(artifacts_root) / "centaur-1981" / "harness" / "soltest3.json"
		self.assertTrue(trace.is_file(), f"missing retained trace: {trace}")

		# Decode only a trace whose bytes are the ones the definition cites.
		digest = hashlib.sha256()
		with open(trace, "rb") as handle:
			for chunk in iter(lambda: handle.read(1 << 20), b""):
				digest.update(chunk)
		self.assertEqual(TRACE_SHA256, digest.hexdigest(), str(trace))

		seg7 = {
			0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4",
			0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9",
		}
		# Ordered (self_test, public) observations, in trace order, with no overwriting.
		pairs: list[tuple[int, int]] = []
		pending: int | None = None
		for event in json.loads(trace.read_text(encoding="utf-8"))["events"]:
			if event["event"] == "solenoid" and event["state"] == 1:
				pending = event["number"]
			elif event["event"] == "display" and event.get("segments") and event["index"] == 0:
				if pending is None:
					continue
				digits = "".join(seg7.get(value & 0x7F, "") for value in event["segments"])
				if len(digits) == 2 and digits.isdigit() and 1 <= int(digits) <= 18:
					pairs.append((int(digits), pending))
					pending = None

		expected = {
			self_test: public
			for self_test, (public, _) in SELF_TEST_TO_PUBLIC_SOLENOID.items()
		}
		# Split into complete ordered cycles: a cycle runs 01..18 ascending, and a number that
		# does not continue the current cycle starts a new one.
		cycles: list[dict[int, int]] = []
		current: dict[int, int] = {}
		last = 0
		for self_test, public in pairs:
			if self_test <= last:
				cycles.append(current)
				current = {}
			current[self_test] = public
			last = self_test
		cycles.append(current)

		complete = [cycle for cycle in cycles if set(cycle) == set(expected)]
		self.assertGreaterEqual(
			len(complete), 2, f"expected at least two complete self-test cycles, saw {len(cycles)}"
		)
		for index, cycle in enumerate(complete):
			self.assertEqual(expected, cycle, f"complete cycle {index} disagrees with the definition")

	def test_evidence_manifest_hashes_reproduce(self) -> None:
		"""Every hash the evidence artifact pins must be reproducible from the real files."""
		import hashlib
		import os

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("evidence roots are not configured")
		evidence = load_json(EVIDENCE_PATH)
		harness = Path(artifacts_root) / "centaur-1981" / "harness"

		def sha256_of(path: Path) -> str:
			digest = hashlib.sha256()
			with open(path, "rb") as handle:
				for chunk in iter(lambda: handle.read(1 << 20), b""):
					digest.update(chunk)
			return digest.hexdigest()

		# Each recorded run must exist under the harness directory with the recorded hash.
		recorded = {run["sha256"] for run in evidence["runtime"]["raw_runs"]}
		actual = {sha256_of(path) for path in harness.glob("*.json")}
		self.assertTrue(
			recorded <= actual,
			f"recorded run hashes not found in {harness}: {sorted(recorded - actual)}",
		)

		# The directory manifest digest must be reproducible by the documented algorithm.
		import json as _json

		self.assertIn("manifest_algorithm", evidence["source"])
		entries = [
			{
				"path": item.relative_to(harness).as_posix(),
				"size": item.stat().st_size,
				"sha256": sha256_of(item),
			}
			for item in sorted(harness.rglob("*"))
			if item.is_file()
		]
		canonical = _json.dumps(
			entries, indent=None, separators=(",", ":"), sort_keys=True, ensure_ascii=False
		).encode("utf-8")
		self.assertEqual(evidence["source"]["sha256"], hashlib.sha256(canonical).hexdigest())

	def test_schematic_lamp_names_match_the_script_bound_addresses(self) -> None:
		"""The seven lamps the retained script binds by name are the only independent check.

		Everything else in the lamp table is derived: public = 16*d + lampadr + 1 puts an address
		on an MC14514 output, the schematic gives that output's SCR and connector pin, and the pin
		carries a printed function. If the derivation were wrong these seven would disagree.
		"""
		expected = {
			11: "Shoot Again",
			13: "Ball in Play",
			27: "Match",
			29: "High Score to Date",
			43: "Tilt Warning",
			45: "Game Over",
			61: "Tilt",
		}
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address, label in expected.items():
			self.assertEqual(label, lamps[address]["label"], f"lamp {address}")
			self.assertEqual("validated", lamps[address]["provenance"]["status"], f"lamp {address}")

	def test_lamp_classes_are_consistent_across_decoders(self) -> None:
		"""Each MC14514 output drives the same class of lamp on all four decoders.

		That structure is what makes the derivation trustworthy, so it is worth pinning: if a
		future edit puts a chamber lamp where a bonus lamp belongs, the class breaks.
		"""
		lamps = {
			item["binding"]["device"]: item["label"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		classes = {
			1: "Bonus", 2: "Bonus", 4: "Bonus", 5: "Rollover",
			6: "Drop Target", 7: "Drop Target Arrow", 8: "Chamber", 11: "Captive Orbs",
		}
		for output, token in classes.items():
			members = [
				lamps[16 * d + output + 1]
				for d in range(4)
				if (16 * d + output + 1) in lamps
			]
			self.assertEqual(4, len(members), f"decoder output {output}")
			for label in members:
				self.assertIn(token.split()[-1], label, f"output {output}: {label}")

	def test_public_lamp_one_is_not_a_lamp(self) -> None:
		"""It feeds the G.I. flasher module, which is why the legacy corpus never bound it."""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual("control_signal", lamps[1]["kind"])

	def test_coverage_is_partial_and_names_the_one_blocker(self) -> None:
		"""One unlocated auxiliary circuit is the only thing between this record and author-ready.

		Public lamp 113 is fitted on the A9 board but the factory schematic prints no function for
		it and nothing locates it, so it carries no placement. Every other dimension is validated.
		The blocker must stay conspicuous rather than being papered over with a projection.
		"""
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		# Two auxiliary-lamp conflicts are unresolved, so the requirement is listed too;
		# omitting it credited this record with work nobody had done.
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], coverage["missing"])
		self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])
		self.assertTrue(
			all(v == "validated" for k, v in coverage["dimensions"].items() if k != "spatial_placement")
		)
		self.assertEqual(
			{"conflict.aux-lamp-65-97-top-lane-binding", "conflict.aux-lamp-113-unidentified"},
			{conflict["id"] for conflict in self.definition["conflicts"]},
		)

	def test_centre_coin_chute_selector_is_enumerated(self) -> None:
		"""The printed credits-per-coin tables cover chutes 1 and 3 only; 17-20 are the centre."""
		for address in (17, 18, 19, 20):
			device = self.dips[address]
			self.assertEqual("used", device["availability"])
			self.assertIn("centre", device["label"])

	def test_every_device_carries_a_spatial_record_except_the_named_blocker(self) -> None:
		"""Exactly one device may lack a spatial record, and it must be the one named in coverage."""
		unlocated = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			if "spatial" not in item:
				unlocated.append(item["binding"]["device"])
		for display in self.definition["displays"]:
			self.assertIn("spatial", display, display["id"])
		self.assertEqual([113], unlocated)

	def test_bare_auxiliary_matrix_positions_have_no_lamp(self) -> None:
		"""The A9 has twelve SCRs for sixteen matrix positions; four positions carry no bulb.

		Its MC14555B decoders are binary one-of-four, so the board reaches lamp addresses 0-3 on
		each of four data lines. The fitted circuits are 65-67, 81-83, 97-99 and 113-115; decoder
		position 3 has no SCR. PinMAME reports matrix bits rather than bulbs, so these still show
		activity during the self-test lamp sequence - that is not evidence of a lamp.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (68, 84, 100, 116):
			device = lamps[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			# The validator requires reason "unused" for an unused device; that there is no SCR
			# fitted at all is the sharper fact and lives in the device note.
			self.assertEqual("unused", device["spatial"]["reason"], address)
			self.assertIn("N/U", device["physical"]["notes"], address)

	def test_twelfth_auxiliary_circuit_claims_only_what_is_evidenced(self) -> None:
		"""113 is fitted and unnamed, and must not acquire a function or a position by inference.

		The Centaur manual's own AS-2518-43 sheet prints a function against all eleven other fitted
		outputs and leaves A9J2-11 blank, while marking the genuinely unused pins beside it N/U. An
		earlier draft placed it at the arithmetic centroid of the three top-lane inserts and called
		that validated; a centroid of three lamps in a row lands on the middle one, and it was
		neither observed nor defensible. Guard against it coming back.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		device = lamps[113]
		self.assertEqual("used", device["availability"])
		self.assertIn("A9J2-11", device["label"])
		self.assertNotIn("Guardian", device["label"])
		self.assertNotIn("Rollover", device["label"])
		self.assertNotIn("spatial", device)

	def test_outer_top_lane_lamps_follow_the_manual_not_the_table(self) -> None:
		"""A9J2-7 is TOP LEFT LANE and A9J2-18 is TOP RIGHT LANE.

		The retained community table binds these the other way round. The manual is ground truth for
		physical wiring and the same traced chain reproduces the table's other nine auxiliary
		assignments exactly, so the table is wrong here. Left must also sit left of right on the
		playfield, which is the check that would have caught the original swap.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual("Top Left Lane", lamps[65]["label"])
		self.assertEqual("Top Middle Lane", lamps[81]["label"])
		self.assertEqual("Top Right Lane", lamps[97]["label"])
		xs = [lamps[address]["spatial"]["placements"][0]["x"] for address in (65, 81, 97)]
		self.assertEqual(sorted(xs), xs, "top lanes must run left to right across the playfield")

	def test_auxiliary_board_is_sourced_from_the_centaur_manual(self) -> None:
		"""The A9 sheet is printed in Centaur's own manual, not borrowed from another game.

		An earlier pass concluded no Centaur manual carried it and fell back on the Kings of Steel
		schematics. The boards are identical, but only the Centaur print annotates the per-pin lamp
		functions, and those are what identify the twelve circuits.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (65, 66, 67, 68, 81, 82, 83, 84, 97, 98, 99, 100, 113, 114, 115, 116):
			self.assertIn(
				"manual-schematics.bally.centaur.1981",
				lamps[address]["provenance"]["source_refs"],
				address,
			)

	def test_placement_count_matches_declared_quantity_or_is_explained(self) -> None:
		"""A render primitive is not a physical contact, and a lamp pair is not one bulb.

		The retained table models a single physical target as a trigger plus a hit target plus
		several render primitives stacked at one point. An earlier pass promoted each object as its
		own sensor, which invented contacts: switch 12 carried ten placements for four physical
		targets. Placements must now equal the declared quantity, and the only permitted shortfalls
		are the ones the record explains in prose - switch 34, whose five contacts include two the
		table does not model, and the auxiliary lamp pairs, where only one of two bulbs is located.
		Those must not claim validated spatial status.
		"""
		shortfall_allowed = {34, 65, 66, 67, 81, 82, 83, 97, 98, 99, 114, 115}
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial") or {}
			placements = spatial.get("placements")
			if not placements:
				continue
			quantity = (item.get("physical") or {}).get("quantity")
			if quantity is None:
				continue
			address = item["binding"]["device"]
			if len(placements) == quantity:
				continue
			self.assertIn(address, shortfall_allowed, f"{item['id']}: {len(placements)} != {quantity}")
			self.assertLess(len(placements), quantity, item["id"])
			self.assertNotEqual("validated", spatial["status"], item["id"])

	def test_stacked_render_objects_are_not_separate_contacts(self) -> None:
		"""No two placements on one device may describe the same point."""
		for item in self.definition["inputs"] + self.definition["outputs"]:
			placements = (item.get("spatial") or {}).get("placements") or []
			for index, one in enumerate(placements):
				for other in placements[index + 1:]:
					self.assertFalse(
						abs(one["x"] - other["x"]) <= 0.01 and abs(one["y"] - other["y"]) <= 0.01,
						f"{item['id']}: {one['id']} and {other['id']} are the same location",
					)

	def test_every_auxiliary_circuit_drives_a_pair_of_lamps(self) -> None:
		"""The AS-2518-43 drives twenty-four lamps as twelve sets of two."""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (65, 66, 67, 81, 82, 83, 97, 98, 99, 113, 114, 115):
			self.assertEqual(2, lamps[address]["physical"]["quantity"], address)


class By35ProfileTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(PROFILE_PATH)
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def _allowed(self, group_id: str) -> set[int]:
		allowed: set[int] = set()
		for rule in self.groups[group_id]["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		return allowed

	def test_momentary_solenoids_stop_at_fifteen(self) -> None:
		"""Selector 15 is the idle state, so there is no public address 16."""
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual(set(range(1, 16)), allowed)
		self.assertNotIn(16, allowed)

	def test_four_continuous_outputs_are_published_at_seventeen_through_twenty(self) -> None:
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual({17, 18, 19, 20}, allowed)

	def test_lamp_decoder_slots_are_not_addressable(self) -> None:
		allowed = self._allowed("pinmame.output.lamp")
		for slot in (16, 32, 48, 64, 80, 96, 112, 128):
			self.assertNotIn(slot, allowed, f"lamp {slot} is a skipped decoder slot")
		self.assertEqual(120, len(allowed))

	def test_switch_matrix_is_six_columns_of_eight_plus_diagnostics(self) -> None:
		allowed = self._allowed("pinmame.input.switch")
		self.assertLessEqual(set(range(1, 49)), allowed)
		self.assertLessEqual({-7, -6, -5}, allowed)
		self.assertNotIn(49, allowed)

	def test_emulator_normalization_is_declared_and_not_reapplied(self) -> None:
		self.assertTrue(self.profile["inversion_applied_by_emulator"])

	def test_profile_pins_its_pinmame_revision(self) -> None:
		revisions = {source["revision"] for source in self.profile["sources"]}
		self.assertIn("4ec52ff0ac133ac251681518aed2249e19fe26eb", revisions)


if __name__ == "__main__":
	unittest.main()
