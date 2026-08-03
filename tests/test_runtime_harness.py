from __future__ import annotations

import importlib.util
import hashlib
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_pinmame_harness", ROOT / "tools" / "run_pinmame_harness.py")
assert SPEC is not None and SPEC.loader is not None
HARNESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)


class RuntimeHarnessTests(unittest.TestCase):
	def test_pulse_parser_supports_service_switches_and_timing(self) -> None:
		self.assertEqual((-7, 100, 1.0), HARNESS._parse_pulse("-7"))
		self.assertEqual((-7, 120, 8.0), HARNESS._parse_pulse("-7:120:8"))

	def test_config_abi_keeps_vpm_path_before_callback_table(self) -> None:
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


if __name__ == "__main__":
	unittest.main()
