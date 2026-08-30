from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from pinmame_game_defs.jsonio import load_json

sys.path.insert(0, str(ROOT / "tools"))
from attach_vpx_script_io import label_well_formed as tool_label_ok

CORPUS_REPOSITORIES = (
	"https://github.com/sverrewl/vpxtable_scripts",
	"https://github.com/jsm174/vpx-standalone-scripts",
)
EXPECTED_ATTACHED_MACHINES = 279
EXPECTED_ATTACHED_DEVICES = 13186
EXPECTED_ATTACHED_SCRIPTS = 351


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
		self.assertEqual(30, len(definition["inputs"]))
		self.assertEqual(18, len(definition["outputs"]))
		for device in definition["inputs"] + definition["outputs"]:
			self.assertEqual("candidate", device["provenance"]["status"])
			self.assertIn("vpx-script.", device["provenance"]["source_refs"][0])

	def test_lamp_candidates_come_from_the_script(self) -> None:
		definition = load_json(ROOT / "machines/partial/capcom/kingpin-1996.json")
		lamp = next(device for device in definition["outputs"] if device["binding"] == {"device": 5, "group": "pinmame.output.lamp"})
		self.assertEqual("candidate", lamp["provenance"]["status"])
		self.assertEqual("lamp", lamp["kind"])
		self.assertEqual(113, sum(1 for device in definition["outputs"] if device["kind"] == "lamp"))
		self.assertEqual(146, len(definition["inputs"]) + len(definition["outputs"]))

	def test_note_device_counts_name_only_define_derived_devices(self) -> None:
		# Round-6 blocker: the PinMAME source-contract section must not attribute
		# VPX-script or synthetic devices to the driver source.
		import re as _re

		for path in sorted((ROOT / "machines" / "partial").rglob("*.json")):
			definition = load_json(path)
			text = (ROOT / definition["knowledge"]["path"]).read_text(encoding="utf-8")
			claim = _re.search(r"named switch/solenoid symbols are carried as (\d+) candidate devices", text)
			if claim is None:
				continue
			define_ids = {source["id"] for source in definition["sources"] if source.get("id", "").startswith("pinmame.driver.")}
			actual = sum(
				1
				for device in definition["inputs"] + definition["outputs"]
				if device.get("provenance", {}).get("source_refs")
				and all(ref in define_ids for ref in device["provenance"]["source_refs"])
			)
			self.assertEqual(int(claim.group(1)), actual, definition["machine"]["id"])
			self.assertGreater(actual, 0, definition["machine"]["id"])

	def test_extraction_report_agrees_with_its_evidence_files(self) -> None:
		# Round-7 blocker: the extraction was regenerated without committing the
		# evidence, leaving report and evidence contradicting each other. This
		# always-on check needs no external evidence root. Identical-content
		# scripts share one evidence file, so paths may differ between an entry
		# and its evidence; the content hash stem and the counts must not.
		report = load_json(ROOT / "reports" / "vpx-script-extraction.json")
		switch_total = 0
		output_total = 0
		for entry in report["entries"]:
			evidence = load_json(ROOT / entry["evidence"])
			stem = Path(entry["evidence"]).stem
			self.assertTrue(evidence["source"]["sha256"].startswith(stem), entry["evidence"])
			self.assertEqual(entry["switch_candidate_count"], len(evidence["switches"]), entry["evidence"])
			self.assertEqual(entry["output_candidate_count"], len(evidence["outputs"]), entry["evidence"])
			switch_total += len(evidence["switches"])
			output_total += len(evidence["outputs"])
		self.assertEqual(report["switch_candidate_count"], switch_total)
		self.assertEqual(report["output_candidate_count"], output_total)

	def test_the_vpx_labeler_does_not_mangle_plain_symbols(self) -> None:
		import sys

		sys.path.insert(0, str(ROOT / "tools"))
		import attach_vpx_script_io as tool

		self.assertEqual("startgate", tool.vpx_symbol_label("startgate"))
		# clean_label capitalizes the first letter at device-build time.
		self.assertEqual("sol Game On", tool.vpx_symbol_label("solGameOn"))
		self.assertEqual("Sol Kickback", tool.vpx_symbol_label("SolKickback"))
		self.assertEqual("Trough", tool.vpx_symbol_label("swTrough"))
		self.assertEqual("BJet", tool.vpx_symbol_label("sBJet"))

	def test_stored_labels_pass_the_well_formedness_rule(self) -> None:
		for definition in self.attached:
			for device in definition["inputs"] + definition["outputs"]:
				self.assertTrue(tool_label_ok(device["label"]), (definition["machine"]["id"], device["id"], device["label"]))

	def test_script_citations_hash_the_pinned_corpora(self) -> None:
		# Evidence-gated: recompute every cited script's SHA-256 against the
		# pinned corpora checkouts and skip cleanly when they are absent.
		corpora_root = ROOT.parent / "pinmame-game-defs-working-dir" / "source-checkouts"
		vpxtable = corpora_root / "vpxtable_scripts"
		standalone = corpora_root / "vpx-standalone-scripts"
		if not vpxtable.is_dir() or not standalone.is_dir():
			self.skipTest("pinned VPX script corpora are not available")
		checked = 0
		for definition in self.attached:
			for source in corpus_source_records(definition):
				corpus_root = vpxtable if "vpxtable-scripts" in source["locator"] else standalone
				script_path = source["locator"].split(": ", 1)[1]
				import hashlib

				digest = hashlib.sha256((corpus_root / script_path).read_bytes()).hexdigest()
				self.assertEqual(digest, source["sha256"], (definition["machine"]["id"], source["id"]))
				checked += 1
		self.assertGreaterEqual(checked, 300)

	def test_handler_symbols_and_out_of_range_addresses_are_never_attached(self) -> None:
		# VBScript keyboard/form handlers (Table1_KeyDown and friends) and script
		# keyboard-alias references outside the public address ranges must not
		# become devices. Nemesis's script reads Controller.Switch(-3); the
		# definition must carry no such device.
		definition = load_json(ROOT / "machines/partial/peyper-spain/nemesis-1986.json")
		self.assertEqual([], [device for device in definition["inputs"] if device["binding"]["device"] < 1])
		for definition in self.attached:
			for device in definition["inputs"] + definition["outputs"]:
				# Case-sensitive: handler labels carry title-case "Key Down"/"Key
				# Up" from symbol splitting, while legitimate labels such as
				# South Park's "Mr Hankey Up" only collide case-insensitively.
				self.assertIsNone(
					re.search(r"Key (Down|Up)$|(Init|Timer)$", device["label"]),
					(definition["machine"]["id"], device["id"], device["label"]),
				)
				group = device["binding"]["group"]
				address = device["binding"]["device"]
				bounds = {"pinmame.input.switch": (1, 128), "pinmame.output.solenoid": (1, 128), "pinmame.output.lamp": (1, 128), "pinmame.output.gi": (0, 16)}[group]
				self.assertTrue(bounds[0] <= address <= bounds[1], (definition["machine"]["id"], device["id"], address))

	def test_the_candidate_filter_rejects_handlers_and_fragments_directly(self) -> None:
		# Unit-level regression for the guardrails: the persisted ids cannot carry
		# underscores (slug destroys them), so the filter itself is tested here.
		sys.path.insert(0, str(ROOT / "tools"))
		import attach_vpx_script_io as tool

		def switch(symbol: str, address: int) -> dict[str, object]:
			return {"group": "pinmame.input.switch", "symbol": symbol, "address": address, "label": symbol}

		self.assertFalse(tool.candidate_allowed(switch("Table1_KeyDown", 14)))
		self.assertFalse(tool.candidate_allowed(switch("Table1_KeyUp", 16)))
		self.assertFalse(tool.candidate_allowed(switch("Table1_Init", -5)))
		self.assertFalse(tool.candidate_allowed(switch("RampLiftTimer_Timer", 25)))
		self.assertFalse(tool.candidate_allowed(switch("swKey", -3)))
		self.assertFalse(tool.candidate_allowed(switch("swZero", 0)))
		self.assertTrue(tool.candidate_allowed(switch("swCoin1", 13)))
		# Raw VBScript fragments never become labels either.
		self.assertFalse(tool.label_well_formed("Vpm Sol Sound Sound FX("))
		self.assertFalse(tool.label_well_formed("Set Lamp 117,"))
		self.assertFalse(tool.label_well_formed("Dt Drop.Sol Unhit 1,"))
		self.assertFalse(tool.label_well_formed("L2"))
		self.assertTrue(tool.label_well_formed("Saucers On"))

	def test_headline_matches_the_attachments(self) -> None:
		# Round-5 major: notes must not headline "identity only" over definitions
		# that carry a declared platform or candidate devices.
		for definition in self.attached:
			note_path = ROOT / definition["knowledge"]["path"]
			text = note_path.read_text(encoding="utf-8")
			has_attachments = bool(definition.get("controller")) or bool(definition["inputs"] or definition["outputs"])
			if has_attachments:
				self.assertNotIn("machine identity only", text, definition["machine"]["id"])
			else:
				self.assertIn("machine identity only", text, definition["machine"]["id"])

	def test_helper_call_symbols_are_never_attached(self) -> None:
		# Round-5 major: vpmSolSound/SetLamp123-style library helpers are not
		# devices; no pass-attached label may come from one.
		import sys

		sys.path.insert(0, str(ROOT / "tools"))
		import attach_vpx_script_io as tool

		self.assertFalse(tool.candidate_allowed({"group": "pinmame.output.solenoid", "symbol": "vpmSolSound", "address": 1, "label": "Vpm Sol Sound"}))
		self.assertFalse(tool.candidate_allowed({"group": "pinmame.output.solenoid", "symbol": "SetLamp123", "address": 17, "label": "Set Lamp123"}))
		self.assertFalse(tool.candidate_allowed({"group": "pinmame.output.lamp", "symbol": "UpdateMultipleLamps", "address": 5, "label": "Update Multiple Lamps"}))
		self.assertTrue(tool.candidate_allowed({"group": "pinmame.output.solenoid", "symbol": "sTrough", "address": 1, "label": "Trough"}))
		for definition in self.attached:
			for device in definition["inputs"] + definition["outputs"]:
				self.assertNotIn("vpm sol sound", device["label"].casefold(), (definition["machine"]["id"], device["id"]))
				self.assertFalse(re.match(r"^(?:set|update) ", device["label"].casefold()), (definition["machine"]["id"], device["id"]))

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
