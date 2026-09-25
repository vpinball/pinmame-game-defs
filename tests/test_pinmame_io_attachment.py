from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CORE_SOURCE_ID = f"pinmame.core.{PINMAME_REVISION[:12]}"

EXPECTED_PLATFORM_COUNTS = {
	"pinmame.by35": 42,
	# Kingpin (curated 2026-09-25) now declares its platform from the curated definition.
	"pinmame.capcom": 3,
	"pinmame.dataeast": 13,
	"pinmame.p2k": 1,
	"pinmame.sam": 8,
	"pinmame.stern-mpu200": 23,
	"pinmame.system-11": 24,
	"pinmame.wpc-95": 6,
	"pinmame.wpc-dcs": 3,
	"pinmame.wpc-fliptronic": 6,
	# The Shadow (curated 2026-09-26) now declares its platform from the curated definition.
	"pinmame.wpc-security": 3,
}
# Modules whose generation the reviewed profiles do not cover (or which belong
# to a different generation than the profile name suggests) must never claim.
UNMAPPED_MODULES = {"by35_mBY17", "by35_mST100", "by35_mST100s", "by35_GP"}


def partial_definitions() -> list[dict[str, object]]:
	return [load_json(path) for path in sorted((ROOT / "machines" / "partial").rglob("*.json"))]


def attached_definitions() -> list[dict[str, object]]:
	"""Definitions whose controller platform was declared by the attachment pass.

	The pass is the only writer that cites its CORE_GAMEDEF with an explicit
	"machine module" locator, which separates it from every earlier platform
	declaration.
	"""
	result = []
	for definition in partial_definitions():
		if not definition.get("controller", {}).get("platform"):
			continue
		if any("machine module " in source.get("locator", "") for source in definition["sources"] if source["id"].startswith("pinmame.core.")):
			result.append(definition)
	return result


class PinmameIoAttachmentTests(unittest.TestCase):
	def test_platform_attachments_match_the_reviewed_module_mapping(self) -> None:
		counts: dict[str, int] = {}
		for definition in attached_definitions():
			platform = definition["controller"]["platform"]
			counts[platform] = counts.get(platform, 0) + 1
		self.assertEqual(EXPECTED_PLATFORM_COUNTS, counts)

	def test_every_declared_platform_cites_its_core_game_def(self) -> None:
		for definition in attached_definitions():
			core_sources = [source for source in definition["sources"] if source["id"] == CORE_SOURCE_ID and "machine module " in source["locator"]]
			self.assertEqual(1, len(core_sources), definition["machine"]["id"])
			self.assertEqual(PINMAME_REVISION, core_sources[0]["revision"])
			self.assertNotIn("controller_platform", definition["coverage"]["missing"], definition["machine"]["id"])

	def test_notes_never_claim_a_platform_the_definition_does_not_declare(self) -> None:
		# Round-3 blocker: the platform revert fixed the definitions but left the
		# prose asserting the removed claims. The invariant is repository-wide.
		for definition in partial_definitions():
			declared = definition.get("controller", {}).get("platform")
			note_path = ROOT / definition["knowledge"]["path"]
			if not note_path.is_file():
				continue
			text = note_path.read_text(encoding="utf-8")
			claimed = re.findall(r"the definition declares controller platform `([^`]+)` from it\.", text)
			for platform in claimed:
				self.assertEqual(declared, platform, definition["machine"]["id"])

	def test_demoted_identity_records_stay_honest(self) -> None:
		# Round-3 blocker: shared OPDB records may be claimed as resolved by at
		# most one record, and name disagreements keep identity unresolved.
		owners: dict[str, list[str]] = {}
		ipdb_owners: dict[str, list[str]] = {}
		for definition in partial_definitions():
			if "identity" in definition["coverage"]["missing"]:
				continue
			opdb_id = definition["machine"].get("opdb_id")
			ipdb_id = definition["machine"].get("ipdb_id")
			if opdb_id:
				owners.setdefault(opdb_id, []).append(definition["machine"]["id"])
			if ipdb_id:
				ipdb_owners.setdefault(ipdb_id, []).append(definition["machine"]["id"])
		for label, table in (("opdb", owners), ("ipdb", ipdb_owners)):
			for value, sharers in table.items():
				self.assertEqual(1, len(sharers), (label, value, sorted(sharers)))

	def test_the_module_mapping_rule_holds_for_every_attachment(self) -> None:
		# The declared platform must equal the reviewed module mapping applied to
		# the locator's module, and unmapped modules must never claim.
		sys.path.insert(0, str(ROOT / "tools"))
		import attach_pinmame_io

		for definition in attached_definitions():
			locator = next(source["locator"] for source in definition["sources"] if "machine module " in source["locator"])
			module = locator.split("machine module ", 1)[1].split(")", 1)[0].strip()
			if module.startswith("by35_mBY35_"):
				expected = "pinmame.by35"
			elif module.startswith("de_m"):
				expected = "pinmame.dataeast"
			else:
				expected = attach_pinmame_io.MODULE_PLATFORMS.get(module)
			self.assertIsNotNone(expected, (definition["machine"]["id"], module))
			self.assertEqual(expected, definition["controller"]["platform"], (definition["machine"]["id"], module))
			self.assertFalse(module in UNMAPPED_MODULES, (definition["machine"]["id"], module))

	def test_candidate_devices_carry_candidate_provenance(self) -> None:
		definition = load_json(ROOT / "machines/partial/williams/demolition-man-1994.json")
		self.assertEqual("pinmame.wpc-dcs", definition["controller"]["platform"])
		labels = {device["id"]: device for device in definition["inputs"]}
		self.assertIn("switch.launch", labels)
		self.assertEqual({"device": 11, "group": "pinmame.input.switch"}, labels["switch.launch"]["binding"])
		self.assertEqual("candidate", labels["switch.launch"]["provenance"]["status"])
		self.assertTrue(any(source["id"].startswith("pinmame.driver.") for source in definition["sources"]))
		# The attachment deliberately does not model WPC channel 32; it must not
		# appear as a physical coil either.
		self.assertEqual(
			[],
			[output for output in definition["outputs"] if output["binding"] == {"device": 32, "group": "pinmame.output.solenoid"}],
		)

	def test_sam_partials_introduced_by_the_attachment_model_game_on(self) -> None:
		definition = load_json(ROOT / "machines/partial/stern/shrek-2008.json")
		self.assertEqual("pinmame.sam", definition["controller"]["platform"])
		matches = [output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"}]
		self.assertEqual(1, len(matches))
		self.assertEqual("virtual", matches[0]["kind"])
		self.assertNotIn("wiring", matches[0])

	def test_unmapped_modules_stay_unclaimed(self) -> None:
		# Sega Whitestar machines carry de_m modules but no reviewed profile, and
		# System 3-7 has no profile either; their controller_platform must stay
		# honestly missing.
		definition = load_json(ROOT / "machines/partial/stern/elvis-2004.json")
		self.assertNotIn("controller", definition)
		self.assertIn("controller_platform", definition["coverage"]["missing"])
		self.assertTrue(any(device["binding"]["group"] == "pinmame.input.switch" for device in definition["inputs"]))

	def test_mpu100_machines_are_not_claimed_as_mpu200(self) -> None:
		# GEN_STMPU100 is a distinct generation with a different cabinet-switch
		# matrix column; the reviewed module mapping must not hand those machines
		# the MPU-200 profile.
		definition = load_json(ROOT / "machines/partial/stern/nugent-1978.json")
		self.assertNotIn("controller", definition)
		self.assertIn("controller_platform", definition["coverage"]["missing"])


if __name__ == "__main__":
	unittest.main()
