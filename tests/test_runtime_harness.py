from __future__ import annotations

import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_pinmame_harness", ROOT / "tools" / "run_pinmame_harness.py")
assert SPEC is not None and SPEC.loader is not None
HARNESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)


class RuntimeHarnessTests(unittest.TestCase):
	class FakeLibrary:
		def __init__(self) -> None:
			self.switch_calls: list[tuple[int, int]] = []
			self.switch_states: dict[int, int] = {}

		def PinmameSetSwitch(self, switch: int, state: int) -> None:
			self.switch_calls.append((switch, state))
			self.switch_states[switch] = state

		def PinmameGetSwitch(self, switch: int) -> int:
			return self.switch_states.get(switch, 0)

		def PinmameGetMaxLamps(self) -> int:
			return 0

		def PinmameGetChangedLamps(self, _states: object) -> int:
			return 0

		def PinmameGetMaxGIs(self) -> int:
			return 0

		def PinmameGetChangedGIs(self, _states: object) -> int:
			return 0

	def test_pulse_parser_supports_service_switches_and_timing(self) -> None:
		self.assertEqual((-7, 100, 1.0), HARNESS._parse_pulse("-7"))
		self.assertEqual((-7, 120, 8.0), HARNESS._parse_pulse("-7:120:8"))

	def test_optional_held_snapshot_runs_before_switch_release(self) -> None:
		library = self.FakeLibrary()
		recorder = HARNESS.Recorder()
		observed: list[tuple[int, int]] = []
		HARNESS._hold_switch(
			library,
			recorder,
			41,
			0.001,
			lambda: observed.append(library.switch_calls[-1]),
		)
		self.assertEqual([(41, 1)], observed)
		self.assertEqual((41, 0), library.switch_calls[-1])

	def test_held_snapshot_cli_is_opt_in(self) -> None:
		parser = HARNESS.build_parser()
		args = parser.parse_args([
			"--library", "pinmame64.dll", "--game", "twenty4_150",
			"--rom-path", "roms", "--work-dir", "state",
		])
		self.assertFalse(args.snapshot_while_held)

	def test_held_snapshot_helper_preserves_label_and_next_index(self) -> None:
		snapshots = [{"label": "existing"}]
		HARNESS._append_output_snapshot(snapshots, HARNESS.Recorder(), "while pulse 2: switch 41 held", None)
		self.assertEqual(2, len(snapshots))
		self.assertEqual("while pulse 2: switch 41 held", snapshots[1]["label"])
		self.assertEqual([], snapshots[1]["displays"])

	def test_watched_switches_are_observed_in_snapshots(self) -> None:
		library = self.FakeLibrary()
		library.PinmameSetSwitch(-7, 1)
		snapshot = HARNESS._output_snapshot(
			HARNESS.Recorder(), "service", library=library, watch_switches=(-7, -6)
		)
		self.assertEqual(
			[{"number": -7, "state": 1}, {"number": -6, "state": 0}],
			snapshot["watched_switches"],
		)

	def test_transition_summary_preserves_ordered_states_per_address(self) -> None:
		recorder = HARNESS.Recorder()
		start = recorder.event_index()
		recorder.record_solenoid(20, 255)
		recorder.record_solenoid(20, 0)
		recorder.record_lamp(4, 1)
		self.assertEqual(
			{
				"solenoids": [{"number": 20, "states": [255, 0]}],
				"lamps": [{"number": 4, "states": [1]}],
				"gis": [],
			},
			recorder.transition_summary(start),
		)

	def test_display_match_is_detected_during_the_settle_window(self) -> None:
		recorder = HARNESS.Recorder()
		texts = iter(["AUDITS", "SWITCH TEST"])
		recorder.current_display_text = lambda: next(texts, "LAMP TEST")
		matched, display_text = HARNESS._wait_for_display_match(
			self.FakeLibrary(), recorder, ["SWITCH TEST"], 0.1
		)
		self.assertEqual("SWITCH TEST", matched)
		self.assertEqual("SWITCH TEST", display_text)

	def test_structured_scenario_validates_actions_and_rejects_unknown_fields(self) -> None:
		valid = {
			"format": HARNESS.SCENARIO_FORMAT,
			"version": HARNESS.SCENARIO_VERSION,
			"game": "lwar_a83",
			"watch_switches": [-7, -6, 47],
			"initial_switches": [{"switch": 47, "state": 0}],
			"actions": [
				{"type": "pulse", "switch": -7, "hold_ms": 120, "settle_s": 0.2},
				{"type": "set_switch", "switch": 47, "state": 1, "settle_s": 0.1},
				{"type": "pulse_key", "key": "left_flipper", "hold_ms": 80, "settle_s": 0.1},
				{
					"type": "pulse_until_display",
					"switch": -7,
					"texts": ["COIL TEST", "SPULEN TEST"],
					"max_pulses": 10,
					"settle_s": 0.1,
				},
				{
					"type": "pulse_until_output",
					"switch": -7,
					"channel": "solenoid",
					"addresses": [1, 2, 3, 4],
					"max_pulses": 10,
					"settle_s": 0.1,
				},
				{
					"type": "wait_until_output",
					"channel": "solenoid",
					"addresses": [1, 2, 3, 4],
					"timeout_s": 0.2,
					"active_only": True,
				},
				{"type": "wait", "seconds": 0.1, "label": "observe"},
			],
		}
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "scenario.json"
			path.write_text(json.dumps(valid), encoding="utf-8")
			self.assertEqual(valid, HARNESS._load_scenario(path))
			valid["actions"][0]["invented"] = True
			path.write_text(json.dumps(valid), encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "scenario schema validation failed"):
				HARNESS._load_scenario(path)

	def test_display_driven_pulse_requires_exactly_one_input(self) -> None:
		invalid = {
			"format": HARNESS.SCENARIO_FORMAT,
			"version": HARNESS.SCENARIO_VERSION,
			"actions": [
				{
					"type": "pulse_until_display",
					"switch": -7,
					"key": "service_black",
					"texts": ["COIL TEST"],
				}
			],
		}
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "scenario.json"
			path.write_text(json.dumps(invalid), encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "scenario schema validation failed"):
				HARNESS._load_scenario(path)

	def test_retained_scenarios_validate_against_the_schema(self) -> None:
		paths = sorted((ROOT / "tools" / "harness-scenarios").glob("**/*.json"))
		self.assertGreaterEqual(len(paths), 2)
		for path in paths:
			with self.subTest(path=path.relative_to(ROOT).as_posix()):
				self.assertEqual(HARNESS.SCENARIO_FORMAT, HARNESS._load_scenario(path)["format"])

	def test_data_east_keyboard_sweep_does_not_write_driver_owned_flipper_switches(self) -> None:
		path = ROOT / "tools" / "harness-scenarios" / "data-east" / "alpha-special-solenoid-sweep.json"
		scenario = HARNESS._load_scenario(path)
		direct_switches = {
			action["switch"]
			for action in scenario["actions"]
			if "switch" in action
		}
		self.assertTrue(any("key" in action for action in scenario["actions"]))
		self.assertTrue(direct_switches.isdisjoint({15, 16, 30, 31, 46, 47}))

	def test_public_switch_addresses_are_bounded_before_native_calls(self) -> None:
		for value in ("-8", "121"):
			with self.subTest(value=value), self.assertRaises(HARNESS.argparse.ArgumentTypeError):
				HARNESS._parse_pulse(value)
			with self.assertRaises(HARNESS.argparse.ArgumentTypeError):
				HARNESS._parse_watch_switch(value)

	def test_key_aliases_preserve_reviewed_pinned_values(self) -> None:
		self.assertEqual(
			{"start": 27, "service_green": 33, "service_black": 34, "left_flipper": 93, "right_flipper": 94},
			HARNESS.KEY_ALIASES,
		)
		schema = json.loads(HARNESS.SCENARIO_SCHEMA_PATH.read_text(encoding="utf-8"))
		self.assertEqual(
			sorted(HARNESS.KEY_ALIASES),
			sorted(schema["$defs"]["pulseKey"]["properties"]["key"]["enum"]),
		)

	def test_config_abi_preserves_required_boundary_fields(self) -> None:
		fields = [name for name, _field_type in HARNESS.PinmameConfig._fields_]
		self.assertEqual(["audioFormat", "sampleRate", "vpmPath"], fields[:3])
		self.assertEqual("cb_OnSoundCommand", fields[-1])

	def test_initial_switch_parser_supports_default_and_explicit_states(self) -> None:
		self.assertEqual((18, 1), HARNESS._parse_initial_switch("18"))
		self.assertEqual((22, 0), HARNESS._parse_initial_switch("22:0"))
		with self.assertRaises(HARNESS.argparse.ArgumentTypeError):
			HARNESS._parse_initial_switch("18:2")

	def test_path_encoder_rejects_pinmame_buffer_overflow(self) -> None:
		with self.assertRaises(ValueError):
			HARNESS._path_bytes(Path("x" * HARNESS.PINMAME_MAX_PATH))

	def test_regular_segment_display_decodes_service_text(self) -> None:
		segments = [0x0071, 0x0877, 0x0039, 0x2201, 0x003F, 0x1873, 0x2500]
		self.assertEqual("FACTORY", HARNESS._decode_segment_frame(1, segments))

	def test_non_segment_display_is_not_decoded(self) -> None:
		self.assertIsNone(HARNESS._decode_segment_frame(14, [0x0877]))

	def test_current_display_text_uses_a_cheap_segment_only_snapshot(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.display_layouts[0] = {"type": 1}
		recorder.display_frames[0] = [0x0071, 0x0877, 0x0039, 0x2201, 0x003F, 0x1873, 0x2500]
		recorder.snapshot_displays = mock.Mock(side_effect=AssertionError("full snapshot must not run"))
		self.assertEqual("FACTORY", recorder.current_display_text())
		recorder.snapshot_displays.assert_not_called()

	def test_dmd_snapshot_records_hash_and_optional_graymap(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.display_layouts[0] = {
			"type": 14, "top": 0, "left": 0, "length": 0,
			"width": 2, "height": 2, "depth": 4,
		}
		recorder.display_frames[0] = [0, 1, 15, 7]
		with tempfile.TemporaryDirectory() as directory:
			displays = recorder.snapshot_displays(Path(directory), 3, "After pulse 1: switch -3")
			self.assertEqual(hashlib.sha256(bytes([0, 1, 15, 7])).hexdigest(), displays[0]["pixel_sha256"])
			self.assertEqual(3, displays[0]["nonzero_pixels"])
			artifact = Path(displays[0]["artifact"])
			self.assertEqual("003-after-pulse-1-switch-3-display-0.pgm", artifact.name)
			self.assertEqual(b"P5\n2 2\n255\n\x00\x11\xffw", artifact.read_bytes())

	def test_dmd_snapshot_preserves_brightness_mode_pixels(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.display_layouts[0] = {
			"type": 14, "top": 0, "left": 0, "length": 0,
			"width": 2, "height": 1, "depth": 4,
		}
		recorder.display_frames[0] = [0, 255]
		with tempfile.TemporaryDirectory() as directory:
			displays = recorder.snapshot_displays(Path(directory), 0, "booted")
			self.assertEqual(b"P5\n2 1\n255\n\x00\xff", Path(displays[0]["artifact"]).read_bytes())

	def test_dmd_change_events_are_bounded_with_a_loss_summary(self) -> None:
		recorder = HARNESS.Recorder()
		for value in range(HARNESS.MAX_DMD_EVENTS_PER_DISPLAY + 4):
			recorder.record_dmd_frame(0, [value % 256, value // 256])
		display_events = [event for event in recorder.events if event["event"] == "display"]
		self.assertEqual(HARNESS.MAX_DMD_EVENTS_PER_DISPLAY, len(display_events))
		self.assertEqual({"changed_frames": 260, "recorded_events": 256, "suppressed_events": 4}, recorder.snapshot_dmd_event_summary()["0"])

	def test_changed_lamp_addresses_drive_snapshots(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.record_lamp(88, 1)
		recorder.record_lamp(11, 1)
		recorder.record_lamp(88, 0)
		self.assertEqual([11], recorder.snapshot_active_lamps())

	def test_callback_solenoid_addresses_drive_snapshots_without_legacy_aliases(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.record_solenoid(33, 255)
		recorder.record_solenoid(14, 255)
		recorder.record_solenoid(14, 0)
		self.assertEqual([33], recorder.snapshot_active_solenoids())

	def test_changed_gi_addresses_drive_snapshots(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.record_gi(0, 9)
		recorder.record_gi(4, 255)
		recorder.record_gi(0, 0)
		self.assertEqual([4], recorder.snapshot_active_gis())

	def test_main_writes_partial_trace_and_fails_when_run_reports_failure(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			output = Path(directory) / "failed-run.json"
			argv = [
				"run_pinmame_harness.py", "--library", "pinmame64.dll", "--game", "lwar_a83",
				"--rom-path", "roms", "--work-dir", "state", "--output", str(output),
			]
			result = {"format": "pinmame-harness-run", "failure": {"type": "TimeoutError", "message": "diagnostic did not appear"}}
			with mock.patch.object(HARNESS, "run", return_value=result), mock.patch.object(HARNESS.sys, "argv", argv):
				self.assertEqual(1, HARNESS.main())
			self.assertEqual(result, json.loads(output.read_text(encoding="utf-8")))


if __name__ == "__main__":
	unittest.main()
