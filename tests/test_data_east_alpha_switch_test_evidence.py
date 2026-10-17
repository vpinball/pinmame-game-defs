from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import data_east_alpha_switch_test_evidence as evidence_tool  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS  # noqa: E402

SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "data-east"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "data-east"
# The address each settled record cites, and the name the ROM's Switch Test printed for it.
SETTLED = {"lwar_a83": (17, "LEFT KICKBCK"), "ssvc_a26": (32, "LEFT KICKBCK")}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class DataEastAlphaSwitchTestEvidenceTests(unittest.TestCase):
	def test_scenarios_probe_every_address_after_a_reference_and_skip_the_flipper_pair(self) -> None:
		for game in evidence_tool.GAMES.values():
			with self.subTest(game=game.game):
				scenario = load(SCENARIO_DIRECTORY / f"{game.scenario}.json")
				self.assertEqual(game.game, scenario["game"])
				pulses = [action for action in scenario["actions"] if action["type"] == "pulse"]
				self.assertEqual(2 * len(game.probes), len(pulses))
				for reference, probe, address in zip(pulses[0::2], pulses[1::2], game.probes):
					self.assertEqual(game.alternate if address == game.reference else game.reference, reference["switch"])
					self.assertEqual(f"reference {reference['switch']} before {address}", reference["label"])
					self.assertEqual(address, probe["switch"])
					self.assertEqual(f"announce switch {address}", probe["label"])
					for action in (reference, probe):
						self.assertTrue(action["snapshot_while_held"])
						self.assertEqual(3000, action["hold_ms"])
				direct = {action["switch"] for action in scenario["actions"] if "switch" in action}
				self.assertTrue(direct.isdisjoint(game.flipper_pair))
				self.assertTrue(direct.isdisjoint(range(1, 9)), "cabinet column 1 is keyboard-backed while service keys are in use")

	def test_evidence_is_tied_to_its_scenario_pinned_binary_and_rom(self) -> None:
		for game in evidence_tool.GAMES.values():
			with self.subTest(game=game.game):
				document = load(RUNTIME_DIRECTORY / game.output)
				scenario_path = SCENARIO_DIRECTORY / f"{game.scenario}.json"
				self.assertEqual([game.game], document["driver_ids"])
				self.assertEqual([game.machine_id], document["machine_ids"])
				self.assertEqual(evidence_tool.LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
				self.assertEqual(evidence_tool.REVISION, document["runtime"]["emulator"]["built_from_revision"])
				self.assertEqual(evidence_tool.REVISION, document["source"]["revision"])
				self.assertEqual(game.rom_archive_sha256, document["runtime"]["rom_archive_sha256"])
				self.assertEqual(f"external:pinmame-review-artifacts/{game.directory}", document["source"]["path"])
				raw_runs = document["runtime"]["raw_runs"]
				self.assertEqual([f"{game.scenario}-{name}" for name in evidence_tool.RUNS], [raw["name"] for raw in raw_runs])
				scenario = load(scenario_path)
				for raw in raw_runs:
					self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"])
					self.assertEqual(len(scenario["actions"]), raw["action_count"])
					self.assertEqual(f"tools/harness-scenarios/data-east/{game.scenario}.json", raw["scenario_path"])
				self.assertNotEqual(raw_runs[0]["sha256"], raw_runs[1]["sha256"], "the two runs must be independent recordings")

	def test_every_reading_decodes_from_its_raw_segments(self) -> None:
		for game in evidence_tool.GAMES.values():
			with self.subTest(game=game.game):
				run = load(RUNTIME_DIRECTORY / game.output)["runtime"]["observations"]["runs"][evidence_tool.RUNS[0]]
				observations = run["named_action_observations"]
				self.assertEqual(game.probes, [item["input_address"] for item in observations])
				for item in observations:
					self.assertEqual([item["input_address"]], item["host_stimulus_switch_addresses"])
					self.assertEqual([], item["observed_switch_addresses"])
					self.assertEqual([0, 1], [response["display_index"] for response in item["display_responses"]])
					for response in item["display_responses"]:
						decoded = "".join(SEGMENT_16_CHARACTERS[value] for value in response["segments"])
						self.assertEqual(decoded, response["interpreted_text"], item["label"])
					if item["result"] == "observed":
						text = " ".join(" ".join(response["interpreted_text"] for response in item["display_responses"]).split())
						self.assertTrue(item["label"].endswith(f"the ROM shows {text}"), item["label"])
				self.assertEqual([{"after_service_pulses": run["diagnostic_checkpoints"][0]["after_service_pulses"], "matched_text": "SWITCH TEST"}], run["diagnostic_checkpoints"])

	def test_the_settled_addresses_read_the_kickback_name(self) -> None:
		for game_name, (address, name) in SETTLED.items():
			with self.subTest(game=game_name):
				game = evidence_tool.GAMES[game_name]
				readings = evidence_tool.readings(load(RUNTIME_DIRECTORY / game.output))
				self.assertEqual(name, readings[address])

	def test_derivation_refuses_an_unstable_reference_and_identical_probe_text(self) -> None:
		game = evidence_tool.GAMES["lwar_a83"]

		def snapshot(label: str, text: str) -> dict:
			rows = [text[:7].ljust(7), text[7:].ljust(7)]
			reverse = {}
			for value, character in SEGMENT_16_CHARACTERS.items():
				reverse.setdefault(character, value)
			return {
				"label": label,
				"displays": [
					{"index": index, "layout": {"type": 0}, "segments": [reverse[character] for character in row], "text": row}
					for index, row in enumerate(rows)
				],
			}

		def name(address: int) -> str:
			# Letters only: the alphanumeric font has no glyph for every digit.
			return f"SW {chr(65 + address // 26)}{chr(65 + address % 26)}"

		run = {"snapshots": [], "steps": [
			{"label": "toggle Green once"},
			{"label": "advance to Switch Test", "matched_text": "SWITCH TEST", "pulses": 6},
		]}
		for address in game.probes:
			reference = game.alternate if address == game.reference else game.reference
			run["snapshots"].append(snapshot(f"reference {reference} before {address} (held)", "TILT" if reference == game.reference else "OUTHOLE"))
			run["snapshots"].append(snapshot(f"announce switch {address} (held)", name(address)))
		readings, _block = evidence_tool.derive(run, game)
		self.assertEqual({address: name(address) for address in game.probes}, readings)

		# Public 10 follows a reference closure of 9; repeating that reference text means 10 printed no name of its own.
		repeated = copy.deepcopy(run)
		repeated["snapshots"][3] = snapshot(f"announce switch {game.probes[1]} (held)", "TILT")
		readings, block = evidence_tool.derive(repeated, game)
		self.assertNotIn(game.probes[1], readings)
		self.assertEqual("no_matching_transition", block["named_action_observations"][1]["result"])

		unstable = copy.deepcopy(run)
		unstable["snapshots"][2] = snapshot(f"reference {game.reference} before {game.probes[1]} (held)", "OTHER")
		with self.assertRaisesRegex(ValueError, "not address-driven"):
			evidence_tool.derive(unstable, game)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_evidence_matches_the_retained_raw_runs(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for game in evidence_tool.GAMES.values():
			document = load(RUNTIME_DIRECTORY / game.output)
			self.assertEqual(evidence_tool.manifests.check_manifest(root / game.directory, game.game), document["source"]["sha256"])
			for raw, name in zip(document["runtime"]["raw_runs"], evidence_tool.RUNS):
				run_path = root / game.directory / name / "run.json"
				run = json.loads(run_path.read_bytes())
				self.assertIsNone(run["failure"])
				self.assertEqual(game.game, run["game"])
				self.assertEqual(document["runtime"]["emulator"]["sha256"], run["library_sha256"])
				self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
				self.assertEqual(hashlib.sha256(run_path.read_bytes()).hexdigest(), raw["sha256"])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_tool_refuses_a_run_from_another_library(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		game = evidence_tool.GAMES["lwar_a83"]
		directory = root / game.directory / evidence_tool.RUNS[0]
		original = evidence_tool.LIBRARY_SHA256
		try:
			evidence_tool.LIBRARY_SHA256 = "0" * 64
			with self.assertRaisesRegex(ValueError, "wrong pinned emulator binary"):
				evidence_tool._load_run(directory, game)
		finally:
			evidence_tool.LIBRARY_SHA256 = original

	def test_rom_archives_match_the_pinned_digests(self) -> None:
		rom_root = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not rom_root:
			self.skipTest("PINMAME_ROM_LIBRARY_ROOT is not set")
		for game in evidence_tool.GAMES.values():
			with self.subTest(game=game.game):
				archive = Path(rom_root) / f"{game.game}.zip"
				self.assertEqual(game.rom_archive_sha256, hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
