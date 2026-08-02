from __future__ import annotations

import importlib.util
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

	def test_changed_lamp_addresses_drive_snapshots(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.record_lamp(88, 1)
		recorder.record_lamp(11, 1)
		recorder.record_lamp(88, 0)
		self.assertEqual([11], recorder.snapshot_active_lamps())

	def test_changed_gi_addresses_drive_snapshots(self) -> None:
		recorder = HARNESS.Recorder()
		recorder.record_gi(0, 9)
		recorder.record_gi(4, 255)
		recorder.record_gi(0, 0)
		self.assertEqual([4], recorder.snapshot_active_gis())


if __name__ == "__main__":
	unittest.main()
