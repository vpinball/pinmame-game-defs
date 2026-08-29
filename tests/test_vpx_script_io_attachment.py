from __future__ import annotations

import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
CORPUS_REPOSITORIES = (
	"https://github.com/sverrewl/vpxtable_scripts",
	"https://github.com/jsm174/vpx-standalone-scripts",
)
EXPECTED_ATTACHED_MACHINES = 323
EXPECTED_ATTACHED_DEVICES = 19407
EXPECTED_ATTACHED_SCRIPTS = 424


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
		self.assertEqual(116, sum(1 for device in definition["outputs"] if device["kind"] == "lamp"))

	def test_negative_addresses_get_identifier_safe_ids(self) -> None:
		definition = load_json(ROOT / "machines/partial/peyper-spain/nemesis-1986.json")
		switch = next(device for device in definition["inputs"] if device["binding"] == {"device": -3, "group": "pinmame.input.switch"})
		self.assertEqual("switch.nemesis-key-down-m3", switch["id"])
		self.assertEqual(-3, switch["binding"]["device"])

	def test_attachment_never_touches_machines_that_already_had_devices(self) -> None:
		# The PinMAME define-attachment machines (e.g. Demolition Man) kept their
		# original device set; no corpus script sources were blended into them.
		definition = load_json(ROOT / "machines/partial/williams/demolition-man-1994.json")
		self.assertEqual([], corpus_source_records(definition))


if __name__ == "__main__":
	unittest.main()
