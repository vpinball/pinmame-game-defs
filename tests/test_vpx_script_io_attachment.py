from __future__ import annotations

import re
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
CORPUS_REPOSITORIES = (
	"https://github.com/sverrewl/vpxtable_scripts",
	"https://github.com/jsm174/vpx-standalone-scripts",
)
EXPECTED_ATTACHED_MACHINES = 303
EXPECTED_ATTACHED_DEVICES = 17142
EXPECTED_ATTACHED_SCRIPTS = 384


def corpus_source_records(definition: dict[str, object]) -> list[dict[str, object]]:
	# The attachment pass always records the script's SHA-256. Centaur's earlier
	# curated corpus citation predates this pass and carries no hash, so it is
	# deliberately excluded from the attachment invariants.
	return [
		source
		for source in definition.get("sources", [])
		if source.get("kind") == "vpx_script"
		and source.get("uri") in CORPUS_REPOSITORIES
		and "/blob/" not in source.get("uri", "")
		and len(source.get("sha256", "")) == 64
	]


class VpxScriptIoAttachmentTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definitions = [load_json(path) for path in sorted((ROOT / "machines" / "partial").rglob("*.json"))]
		cls.attached = [definition for definition in cls.definitions if corpus_source_records(definition)]

	def test_attachment_scale_matches_the_reported_pass(self) -> None:
		self.assertEqual(EXPECTED_ATTACHED_MACHINES, len(self.attached))
		device_count = sum(len(definition["inputs"]) + len(definition["outputs"]) for definition in self.attached)
		self.assertEqual(EXPECTED_ATTACHED_DEVICES, device_count)
		script_count = sum(len(corpus_source_records(definition)) for definition in self.attached)
		self.assertEqual(EXPECTED_ATTACHED_SCRIPTS, script_count)

	def test_every_cited_script_is_licensed_and_hashed(self) -> None:
		for definition in self.attached:
			for source in corpus_source_records(definition):
				self.assertTrue(source["license"], definition["machine"]["id"])
				self.assertTrue(source["attribution"], definition["machine"]["id"])
				self.assertEqual(64, len(source["sha256"]), definition["machine"]["id"])
				self.assertNotIn("/blob/", source["uri"])

	def test_south_park_candidate_devices_are_candidates(self) -> None:
		definition = load_json(ROOT / "machines/partial/sega/south-park-1999.json")
		self.assertEqual(31, len(definition["inputs"]))
		self.assertEqual(21, len(definition["outputs"]))
		switch = next(device for device in definition["inputs"] if device["binding"]["device"] == 15)
		self.assertEqual("candidate", switch["provenance"]["status"])
		self.assertIn("vpx-script.", switch["provenance"]["source_refs"][0])

	def test_lamp_candidates_come_from_the_script(self) -> None:
		definition = load_json(ROOT / "machines/partial/capcom/kingpin-1996.json")
		lamp = next(device for device in definition["outputs"] if device["binding"] == {"device": 5, "group": "pinmame.output.lamp"})
		self.assertEqual("candidate", lamp["provenance"]["status"])
		self.assertEqual("lamp", lamp["kind"])
		self.assertEqual(113, sum(1 for device in definition["outputs"] if device["kind"] == "lamp"))

	def test_handler_symbols_and_out_of_range_addresses_are_never_attached(self) -> None:
		# VBScript keyboard/form handlers (Table1_KeyDown and friends) and script
		# keyboard-alias references outside the public address ranges must not
		# become devices. Nemesis's script reads Controller.Switch(-3); the
		# definition must carry no such device.
		definition = load_json(ROOT / "machines/partial/peyper-spain/nemesis-1986.json")
		self.assertEqual([], [device for device in definition["inputs"] if device["binding"]["device"] < 1])
		for definition in self.attached:
			for device in definition["inputs"] + definition["outputs"]:
				self.assertFalse(
					re.search(r"_(?:keydown|keyup|init|mousedown|mouseup)$", device["id"], re.IGNORECASE),
					(definition["machine"]["id"], device["id"]),
				)
				group = device["binding"]["group"]
				address = device["binding"]["device"]
				bounds = {"pinmame.input.switch": (1, 128), "pinmame.output.solenoid": (1, 128), "pinmame.output.lamp": (1, 128), "pinmame.output.gi": (0, 16)}[group]
				self.assertTrue(bounds[0] <= address <= bounds[1], (definition["machine"]["id"], device["id"], address))

	def test_retheme_scripts_do_not_supply_machine_labels(self) -> None:
		# Gremlins re-themes Victory's ROM but not Victory's playfield; the title
		# match must cite only scripts whose path names the machine.
		definition = load_json(ROOT / "machines/partial/gottlieb/victory-1987.json")
		locations = [source["locator"] for source in definition["sources"] if source.get("kind") == "vpx_script" and len(source.get("sha256", "")) == 64]
		self.assertTrue(locations)
		self.assertTrue(all("victory" in locator.casefold() for locator in locations))
		self.assertFalse(any("gremlins" in locator.casefold() for locator in locations))

	def test_attachment_never_touches_machines_that_already_had_devices(self) -> None:
		# The PinMAME define-attachment machines (e.g. Demolition Man) kept their
		# original device set; no corpus script sources were blended into them.
		definition = load_json(ROOT / "machines/partial/williams/demolition-man-1994.json")
		self.assertEqual([], corpus_source_records(definition))


if __name__ == "__main__":
	unittest.main()
