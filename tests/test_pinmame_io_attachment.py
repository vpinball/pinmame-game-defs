from __future__ import annotations

import json
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CORE_SOURCE_ID = f"pinmame.core.{PINMAME_REVISION[:12]}"

EXPECTED_PLATFORM_COUNTS = {
	"pinmame.by35": 53,
	"pinmame.capcom": 4,
	"pinmame.dataeast": 14,
	"pinmame.p2k": 1,
	"pinmame.sam": 9,
	"pinmame.stern-mpu200": 20,
	"pinmame.system-11": 24,
	"pinmame.wpc-95": 7,
	"pinmame.wpc-alpha": 1,
	"pinmame.wpc-dcs": 3,
	"pinmame.wpc-fliptronic": 6,
	"pinmame.wpc-security": 6,
}


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
