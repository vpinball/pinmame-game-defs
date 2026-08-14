"""Guards the rule that decides whether a legacy label pair is a conflict.

`import-legacy` used to emit a conflict whenever a platform record and a game
record spelled one address differently, which produced dozens of records that no
evidence could resolve because there was nothing to resolve. `_names_one_device`
suppresses those. The risk runs in one direction: a false positive **deletes a
real disagreement**, silently and permanently, so the opposite-side cases are
pinned here explicitly.

The first version of the helper failed exactly that way. Side words are stripped
as noise -- they do not distinguish a device from itself -- so `Upper Left
Flipper` and `Upper Right Flipper` reduced to the same core and merged on the
equality check before the side guard ever ran.
"""

from __future__ import annotations

import unittest

from pinmame_game_defs.legacy import _names_one_device


class NamesOneDeviceTests(unittest.TestCase):
	def test_opposite_sides_are_never_one_device(self) -> None:
		"""The regression that shipped in the first draft of the helper."""
		for first, second in [
			("Upper Left Flipper", "Upper Right Flipper"),
			("Left Slingshot", "Right Slingshot"),
			("Left Pop Bumper", "Right Pop Bumper"),
			("Left Coin Chute", "Right Coin Chute"),
			("Left Outlane", "Right Outlane"),
		]:
			with self.subTest(first=first, second=second):
				self.assertFalse(_names_one_device(first, second))

	def test_a_device_class_word_is_not_noise(self) -> None:
		"""A button is not an end-of-stroke contact, and not a relay.

		An earlier draft treated `relay`, `solenoid` and a bare subset match as
		noise, which merged `Right Flipper Button` with `Right Flipper EOS` and
		`Start Button` with `Start Relay`.
		"""
		for first, second in [
			("Right Flipper Button", "Right Flipper EOS"),
			("Left Flipper Button", "Left Flipper EOS"),
			("Start Button", "Start Relay"),
			("Coin Button 3", "Right Coin Chute"),
		]:
			with self.subTest(first=first, second=second):
				self.assertFalse(_names_one_device(first, second))

	def test_genuinely_different_devices_stay_conflicts(self) -> None:
		for first, second in [
			("Ball Roll Tilt", "Drop Target 2"),
			("Coin Button 1", "Backbox Basket Score 1"),
			("ROM Started", "Flasher F19"),
			("ROM Started", "Tilt"),
			("ROM Started", "Upper Right Flipper"),
			("Tilt", "Top Saucer Kicker"),
			("Slam Tilt", "Standup Target"),
			("Left Outlane", "Left Inlane"),
			("Drop Target 1", "Drop Target 2"),
			("Lamp 12", "Lamp 13"),
		]:
			with self.subTest(first=first, second=second):
				self.assertFalse(_names_one_device(first, second))

	def test_two_names_for_one_device_are_not_a_conflict(self) -> None:
		for first, second in [
			("ROM Started", "Game On Relay"),
			("ROM Started", "Game On Solenoid"),
			("ROM Started", "Game On / GI Relay"),
			("ROM Started", "GI Relay"),
			("Coin Button 1", "Coin 1"),
			("Lower Right Flipper", "Right Flipper"),
			("Lower Left Flipper", "Left Flipper"),
			("Upper Left Flipper", "Upper Left Flipper Button"),
			("Tilt", "Plumb Bob Tilt"),
			("Tilt", "Tilt (with Bracket)"),
			("Start Button", "Credit Button"),
		]:
			with self.subTest(first=first, second=second):
				self.assertTrue(_names_one_device(first, second))

	def test_centre_and_center_are_one_spelling(self) -> None:
		self.assertTrue(_names_one_device("Center Pop Bumper", "Centre Pop Bumper"))

	def test_comparison_is_symmetric(self) -> None:
		for first, second in [
			("ROM Started", "Game On Relay"),
			("Upper Left Flipper", "Upper Right Flipper"),
			("Ball Roll Tilt", "Drop Target 2"),
		]:
			with self.subTest(first=first, second=second):
				self.assertEqual(_names_one_device(first, second), _names_one_device(second, first))


if __name__ == "__main__":
	unittest.main()
