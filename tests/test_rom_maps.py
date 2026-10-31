from __future__ import annotations

import copy
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.rom_maps import validate_rom_map, validate_rom_maps

ROOT = Path(__file__).resolve().parents[1]
LW3 = ROOT / "rom-maps/data-east/lethal-weapon-3-1992.lw3_208.json"
AFM = ROOT / "rom-maps/bally/attack-from-mars-1995.afm_113.json"


def _drivers() -> dict[str, set[str]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	drivers: dict[str, set[str]] = {}
	for driver in catalog["drivers"]:
		if driver.get("machine_id"):
			drivers.setdefault(driver["machine_id"], set()).add(driver["id"])
	return drivers


class RomMapRepositoryTests(unittest.TestCase):
	def test_repository_rom_maps_are_valid(self) -> None:
		self.assertEqual([], validate_rom_maps(ROOT, load_json(ROOT / "catalog/pinmame.json")))

	def test_curator_reproduces_every_map(self) -> None:
		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/curate_rom_maps.py"), "--check"], capture_output=True, text=True)
		self.assertEqual(0, result.returncode, result.stderr)

	def test_upstream_fields_are_carried_unchanged(self) -> None:
		"""The base fields must equal tomlogic's map, or the comparison the format exists for is lost."""
		upstream = load_json(ROOT / "rom-maps/_vendor/lw3_208.map.json")
		mapped = load_json(LW3)["memory_map"]
		for key, value in upstream["game_state"].items():
			self.assertEqual(value, mapped["game_state"][key], key)
		self.assertEqual(upstream["high_scores"], mapped["high_scores"])
		upstream_afm = load_json(ROOT / "rom-maps/_vendor/afm_113.map.json")
		mapped_afm = load_json(AFM)["memory_map"]
		for section in ("game_state", "high_scores", "mode_champions", "audits", "checksum8", "checksum16", "last_played"):
			self.assertEqual(upstream_afm[section], mapped_afm[section], section)
		self.assertEqual(upstream_afm["adjustments"]["A.1 Standard Adjustments"], mapped_afm["adjustments"]["A.1 Standard Adjustments"])

	def test_lw3_patch_only_entries_are_scoped_to_lw3_301(self) -> None:
		evidence = load_json(LW3)["evidence"]
		for pointer in ("/extensions/mode_state/ball_save_state", "/extensions/mode_state/ball_time", "/memory_map/adjustments/Standard Adjustments/39", "/extensions/mode_state/leo_award"):
			self.assertEqual(["lw3_301"], evidence[pointer]["applies_to"], pointer)

	def test_every_bulk_input_is_pinned(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		import curate_rom_maps
		for path in (ROOT / "tools/rom-map-inputs").glob("*.json"):
			self.assertIn(path, curate_rom_maps.PINNED, path.name)

	def test_afm_score_adjustments_are_bcd_millions(self) -> None:
		group = load_json(AFM)["memory_map"]["adjustments"]["A.2 Feature Adjustments"]
		self.assertEqual({"encoding": "bcd", "default": 50, "max": 95, "scale": 1000000},
			{key: group["36"][key] for key in ("encoding", "default", "max", "scale")})

	def test_unretained_altsound_names_are_not_carried(self) -> None:
		commands = load_json(AFM)["extensions"]["sound_commands"]["commands"]
		self.assertFalse(any("sample_name" in command for command in commands.values()))

	def test_unheard_commands_are_not_graded_observed(self) -> None:
		evidence = load_json(LW3)["evidence"]
		self.assertEqual("candidate", evidence["/extensions/sound_commands"]["status"])
		self.assertNotIn("/extensions/sound_commands/commands/0x002A", evidence)
		self.assertNotIn("/extensions/sound_commands/commands/0x006B", load_json(AFM)["evidence"])

	def test_nothing_is_validated_from_emulation(self) -> None:
		for path in (LW3, AFM):
			for pointer, entry in load_json(path)["evidence"].items():
				self.assertNotEqual("validated", entry["status"], f"{path.name} {pointer}")


class RomMapFailClosedTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.drivers = _drivers()
		cls.lw3 = load_json(LW3)
		cls.afm = load_json(AFM)

	def errors(self, document: dict) -> list[str]:
		return validate_rom_map(document, "probe.json", ROOT, self.drivers)

	def assertRejected(self, document: dict, fragment: str) -> None:
		errors = self.errors(document)
		self.assertTrue(any(fragment in error for error in errors), errors)

	def test_clean_maps_pass(self) -> None:
		self.assertEqual([], self.errors(copy.deepcopy(self.lw3)))
		self.assertEqual([], self.errors(copy.deepcopy(self.afm)))

	def test_uncovered_descriptor_is_rejected(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["extensions"]["mode_state"]["probe"] = {"label": "Probe", "start": "0x1234", "encoding": "int"}
		del document["evidence"]["/extensions/mode_state"]
		self.assertRejected(document, "/extensions/mode_state/probe: no evidence entry covers")

	def test_dangling_pointer_is_rejected(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["evidence"]["/extensions/mode_state/missing"] = copy.deepcopy(document["evidence"]["/extensions/mode_state"])
		self.assertRejected(document, "pointer resolves to nothing")

	def test_unknown_source_is_rejected(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["evidence"]["/extensions/mode_state"]["sources"] = ["no-such-source"]
		self.assertRejected(document, "unknown source")

	def test_foreign_rom_is_rejected(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["roms"] = document["roms"] + ["afm_113"]
		document["memory_map"]["_metadata"]["roms"] = document["roms"]
		self.assertRejected(document, "'afm_113' is not a driver of data-east.lethal-weapon-3.1992")

	def test_verified_rom_outside_the_map_is_rejected(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["evidence"]["/extensions/mode_state"]["verified_on"] = ["lw3_200"]
		self.assertRejected(document, "'lw3_200' is not one of this map's roms")

	def test_metadata_roms_must_match(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["memory_map"]["_metadata"]["roms"] = ["lw3_301"]
		self.assertRejected(document, "must equal $.roms")

	def test_memory_map_must_stay_upstream_valid(self) -> None:
		document = copy.deepcopy(self.lw3)
		document["memory_map"]["game_state"]["match"]["provenance"] = "inline evidence breaks the upstream schema"
		self.assertRejected(document, "memory_map")

	def test_recipe_below_rom_minimum_hold_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		replay = document["extensions"]["mode_replay"]
		step = next(step for step in replay["modes"][0]["steps"] if "sw" in step)
		step["hold"] = replay["timing"]["min_closed_ms"] - 1
		self.assertRejected(document, "is below the ROM minimum")

	def test_recipe_repeating_a_switch_too_fast_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		replay = document["extensions"]["mode_replay"]
		replay["modes"][0]["steps"] = [{"sw": 45, "hold": 10, "gap": 10}, {"sw": 45, "hold": 10, "gap": 10}]
		self.assertRejected(document, "under the 120 ms same-switch gap")

	def test_same_switch_gap_starts_at_release_not_closure(self) -> None:
		document = copy.deepcopy(self.afm)
		steps = [{"sw": 45, "hold": 200, "gap": 0}, {"sw": 45, "hold": 60, "gap": 200}]
		document["extensions"]["mode_replay"]["modes"][0]["steps"] = steps
		self.assertRejected(document, "switch 45 repeats after 0 ms")
		steps[0]["gap"] = 120
		self.assertEqual([], self.errors(document))

	def test_interleaved_switches_contribute_hold_and_gap_to_open_interval(self) -> None:
		document = copy.deepcopy(self.afm)
		steps = [{"sw": 45, "hold": 200, "gap": 10}, {"sw": 46, "hold": 60, "gap": 49}, {"sw": 45, "hold": 60}]
		document["extensions"]["mode_replay"]["modes"][0]["steps"] = steps
		self.assertRejected(document, "switch 45 repeats after 119 ms")
		steps[1]["gap"] = 50
		self.assertEqual([], self.errors(document))

	def test_repeated_block_checks_boundary_without_expanding_large_count(self) -> None:
		document = copy.deepcopy(self.afm)
		mode = document["extensions"]["mode_replay"]["modes"][0]
		mode["repeat_block"] = 1000000000
		mode["steps"] = [{"sw": 45, "hold": 60, "gap": 0}]
		self.assertRejected(document, "switch 45 repeats after 0 ms")
		mode["steps"][0]["gap"] = 120
		self.assertEqual([], self.errors(document))

	def test_ram_controlled_switch_repetition_is_checked_with_bound(self) -> None:
		for field in ("repeat_ram", "repeat_until_zero"):
			with self.subTest(field=field):
				document = copy.deepcopy(self.afm)
				step = {"sw": 45, "hold": 60, "gap": 0, field: "0x088A", "repeat_max": 2}
				document["extensions"]["mode_replay"]["modes"][0]["steps"] = [step]
				self.assertRejected(document, "switch 45 repeats after 0 ms")
				step["repeat_max"] = 1
				self.assertEqual([], self.errors(document))
				step["repeat_max"] = 2
				step["gap"] = 120
				self.assertEqual([], self.errors(document))

	def test_omitted_hold_uses_comfortable_duration(self) -> None:
		document = copy.deepcopy(self.afm)
		replay = document["extensions"]["mode_replay"]
		replay["modes"][0]["steps"] = [{"sw": 45, "gap": 0}, {"sw": 46, "gap": 60}, {"sw": 45}]
		self.assertEqual([], self.errors(document))
		replay["timing"]["comfortable_closed_ms"] = 59
		self.assertRejected(document, "switch 45 repeats after 119 ms")
		replay["timing"]["comfortable_closed_ms"] = replay["timing"]["min_closed_ms"] - 1
		self.assertRejected(document, "is below the ROM minimum")
		del replay["timing"]["comfortable_closed_ms"]
		self.assertRejected(document, "hold or timing.comfortable_closed_ms is required")

	def test_unknown_op_duration_does_not_satisfy_switch_gap(self) -> None:
		document = copy.deepcopy(self.afm)
		document["extensions"]["mode_replay"]["modes"][0]["steps"] = [
			{"sw": 45, "hold": 60, "gap": 10}, {"op": "saucer", "gap": 109}, {"sw": 45, "hold": 60}
		]
		self.assertRejected(document, "switch 45 repeats after 119 ms")

	def test_validated_from_emulation_alone_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		document["evidence"]["/extensions/mode_replay"]["status"] = "validated"
		self.assertRejected(document, "probe.json")
		document["evidence"]["/extensions/mode_replay"]["proof"] = ["rig", "harness"]
		self.assertEqual([], self.errors(document))

	def test_misspelled_confirmation_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		document["extensions"]["mode_replay"]["modes"][0]["confirm"]["sounds"] = ["typo"]
		self.assertRejected(document, "probe.json")

	def test_non_numeric_verification_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		document["extensions"]["mode_replay"]["modes"][0]["verified"]["seconds"] = "14.4"
		self.assertRejected(document, "probe.json")

	def test_duplicate_mode_id_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		modes = document["extensions"]["mode_replay"]["modes"]
		modes.append(copy.deepcopy(modes[0]))
		document["evidence"]["/extensions/mode_replay"] = copy.deepcopy(document["evidence"]["/extensions/mode_replay"])
		self.assertRejected(document, "duplicate mode id")

	def test_undescribed_op_is_rejected(self) -> None:
		document = copy.deepcopy(self.afm)
		document["extensions"]["mode_replay"]["modes"][0]["steps"].append({"op": "teleport", "gap": 0})
		self.assertRejected(document, "op 'teleport' is not described")


class Lw3SoundEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.document = load_json(LW3)
		cls.observations = load_json(ROOT / "tools/rom-map-inputs/lethal-weapon-3-1992.sound-observations.json")
		sys.path.insert(0, str(ROOT / "tools"))
		import curate_rom_maps
		cls.curator = curate_rom_maps

	def test_extra_ball_percentage_decodes_the_retained_25_percent_value(self) -> None:
		# LW3_BLIND_SPOTS_ROM.md records raw 0x25 as 25%; int would decode it as 37.
		descriptor = self.document["memory_map"]["adjustments"]["Expanded Adjustments"]["42"]
		self.assertEqual("0x1E1A", descriptor["start"])
		self.assertEqual("bcd", descriptor["encoding"])

	def test_observed_commands_use_only_the_recorded_cpu_roms(self) -> None:
		evidence = self.document["evidence"]
		for opcode, expected in (("0x00DC", ["lw3_301"]), ("0x00B6", ["lw3_208", "lw3_301"])):
			entry = evidence[f"/extensions/sound_commands/commands/{opcode}"]
			self.assertEqual("observed", entry["status"], opcode)
			self.assertEqual(["rig"], entry["proof"], opcode)
			self.assertEqual(expected, entry["verified_on"], opcode)
			self.assertIn(self.curator.LW3_OBSERVATIONS, entry["sources"])

	def test_unretained_source_observations_do_not_claim_rig_verification(self) -> None:
		# CF is player-reported with a paused recording; F6's reported forced run is absent.
		for opcode in ("0x00CF", "0x00F6"):
			self.assertNotIn(opcode, self.observations["commands"])
			entry = self.document["evidence"][f"/extensions/sound_commands/commands/{opcode}"]
			self.assertEqual("candidate", entry["status"])
			self.assertEqual(["map"], entry["proof"])
			self.assertEqual([], entry["verified_on"])
			self.assertIn("Source-reported grade: BOUND", entry["note"])

	def test_recorded_command_does_not_upgrade_an_unverified_semantic_label(self) -> None:
		self.assertIn("0x000F", self.observations["commands"])
		command = self.document["extensions"]["sound_commands"]["commands"]["0x000F"]
		self.assertIn("RE-DERIVED (unverified)", command["note"])
		self.assertNotIn("/extensions/sound_commands/commands/0x000F", self.document["evidence"])
		default = self.document["evidence"]["/extensions/sound_commands"]
		self.assertEqual("candidate", default["status"])
		self.assertEqual(["map"], default["proof"])
		self.assertEqual([], default["verified_on"])

	def test_original_command_table_is_preserved(self) -> None:
		self.assertEqual(load_json(ROOT / "tools/rom-map-inputs/lethal-weapon-3-1992.sound-commands.json"),
			self.document["extensions"]["sound_commands"]["commands"])

	def test_extractor_refuses_a_different_manifest(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			(root / "MANIFEST.sha256").write_bytes(b"unverified evidence\n")
			with self.assertRaisesRegex(RuntimeError, "manifest drifted"):
				self.curator.extract_lw3_sound_observations(root)

	def test_retained_metadata_reproduces_the_observation_input(self) -> None:
		name = "lethal-weapon-3-rom-state-2026-10-03"
		configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if configured:
			root = Path(configured) / name
		else:
			candidates = [parent / "review-artifacts" / name for parent in ROOT.parents]
			candidates += [parent / "pinmame-game-defs-working-dir/review-artifacts" / name for parent in ROOT.parents]
			root = next((candidate for candidate in candidates if candidate.is_dir()), None)
		if root is None or not root.is_dir():
			self.skipTest("retained LW3 recording metadata is not available")
		self.assertEqual(self.observations, self.curator.extract_lw3_sound_observations(root))
		# Verify metadata hashes are fail-closed as well as the manifest itself.
		with tempfile.TemporaryDirectory() as temporary:
			changed = Path(temporary)
			(changed / "MANIFEST.sha256").write_bytes((root / "MANIFEST.sha256").read_bytes())
			for run in self.observations["runs"].values():
				target = changed / run["meta_path"]
				target.parent.mkdir(parents=True, exist_ok=True)
				target.write_bytes((root / run["meta_path"]).read_bytes())
			target.write_bytes(target.read_bytes() + b" ")
			with self.assertRaisesRegex(RuntimeError, "metadata drifted"):
				self.curator.extract_lw3_sound_observations(changed)


if __name__ == "__main__":
	unittest.main()
