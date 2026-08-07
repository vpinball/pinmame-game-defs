"""Repository-wide sidedness checks for spatial placements.

These are the cheap geometric assertions the Bally Centaur post-mortem asked for, generalized to
every record instead of being hand-copied into individual game test modules. They exist because a
transposed placement pair stays inside the valid 0..1 coordinate range, so neither the schema nor
`validate_machine` can see it, and four separate records have shipped one:

* Bally Cactus Canyon - flipper coils and buttons swapped.
* Bally Centaur - two auxiliary lamps assigned by eyeballing the playfield instead of tracing the
  decoder-to-SCR-to-connector chain.
* Stern Ripley's Believe It or Not! - the right and bottom members of both pop-bumper clusters,
  eight placements, promoted as `validated`.
* Stern Avengers Pro - the outlane and return-lane lamp labels, and the two lamps of the right
  2-bank target, in an `author_ready` record.

Two checks, because neither subsumes the other:

1. `test_left_right_pairs_are_ordered_by_x` - a device whose id contains `left` must sit at a
   smaller x than the otherwise identically-named `right` device. This is what caught Cactus Canyon
   and Avengers Pro.
2. `test_switch_coil_and_lamp_of_one_device_are_co_located` - where a switch, a coil and a lamp
   share a device name, they are one physical assembly and must share a position. This is what
   caught Ripley's, whose trio named its third member `bottom` rather than `lower` and was
   therefore invisible to check 1.

Exact coordinate equality is a PASS, not a failure. Genuinely co-located pairs are common and
legitimate - FunHouse's `device.eyes-left` and `device.eyes-right` are the two eyes of one Rudy head
mechanism and share a point, as do Indiana Jones's `device.mini-motor-left`/`-right` and The Rolling
Stones' `device.mick-motor-relay-left`/`-right`. Only a strict inversion is a defect.

`KNOWN_INVERSIONS` is a ratchet, not an excuse list. Every entry must be one of three things:

* `conflict.<id>` - a real inversion recorded as a first-class conflict because repairing it would
  assert a coordinate no source observed.
* `UNVERIFIED ...` - a suspected defect nobody has checked yet. These are debts, not decisions.
* `CORRECT: ...` - a verified inversion that is real geometry. The Walking Dead's crossing ramps are
  the worked example: a ramp named for its entrance legitimately exits on the opposite side, so
  "left ramp exit" belongs on the right. Not every inversion is a bug.

Adding an entry requires justifying it; removing one is what resolving the question looks like.
Anything NOT in the dict fails.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEFT_RIGHT_TOKENS = (("left", "right"), ("lft", "rt"))
UPPER_LOWER_TOKENS = (("upper", "lower"), ("top", "bottom"))

# record id -> {(smaller_id, larger_id): why}
#
# Every entry is a real inversion that is deliberately not "repaired", because repairing it would
# assert a coordinate no source observed. Each must point at a recorded conflict or a named open
# question. See TO_BE_FIXED.md section 2 for the full write-ups.
KNOWN_INVERSIONS: dict[str, dict[tuple[str, str], str]] = {
	"bally.flash-gordon.1980": {
		("lamp.left-outlane-special", "lamp.right-outlane-special"):
			"conflict.outlane-special-insert-side-transposition - the retained table places L15 "
			"(manual: Rt. Out Special) on the left and L31 (Lft. Out Special) on the right, while "
			"its own outlane switch objects are correctly sided. Not swapped, because an outlane "
			"insert is not necessarily co-located with the outlane switch, so nothing fixes which "
			"observed coordinate belongs to which insert.",
		("lamp.right-side-upper-target", "lamp.right-side-lower-target"):
			"conflict.right-side-target-upper-lower-transposition - the manual disagrees with "
			"itself about which of the two right-rail targets is upper, and the lamps show the "
			"same inversion against their switches.",
	},
	# --- Unverified as of 2026-08-08. These are suspected defects, not accepted ones. ---
	"capcom.big-bang-bar.1996": {
		("device.star-bumper-left", "device.star-bumper-right"):
			"UNVERIFIED suspected inversion (x 0.5854 > 0.5262). Needs the manual's playfield "
			"drawing and the retained table's own objects checked before it is either fixed or "
			"accepted. See TO_BE_FIXED.md section 2.1.",
	},
	"midway.world-cup-soccer.1994": {
		("device.upper-jet-bumper", "device.lower-jet-bumper"):
			"UNVERIFIED suspected inversion (y 0.2141 > 0.1598). Needs the manual's Solenoid "
			"Locations drawing checked. See TO_BE_FIXED.md section 2.1.",
	},
	# --- Verified CORRECT on 2026-08-08. Real geometry, not defects. Do not "fix" these. ---
	"stern.the-walking-dead-pro.2014": {
		("switch.left-ramp-exit", "switch.right-ramp-exit"):
			"CORRECT: The Walking Dead has crossing ramps. Each ramp is named for its ENTRANCE "
			"side and its exit wireform crosses the top of the playfield to descend the opposite "
			"side, so LT RAMP EXIT genuinely sits on the right. The manual's own Switch Locations "
			"drawing prints '35 / LT RAMP EXIT' in the top-RIGHT corner beside '39 / RT LOOP "
			"ROLLOVER', and '42 / RT RAMP EXIT' in the top-LEFT, with L-SLING/R-SLING in that same "
			"drawing confirming it is player view and not mirrored. The retained table's ramp "
			"wireform drag points trace the crossing physically, and both switch gates sit on the "
			"opposite ramp's descending segment. The symmetry - BOTH ramps cross - is itself "
			"evidence against a clerical swap.",
	},
	"stern.the-walking-dead-premium-limited-edition.2014": {
		("switch.left-ramp-exit", "switch.right-ramp-exit"):
			"CORRECT: same crossing-ramp geometry as the Pro edition above. Both editions share "
			"one label dict in tools/curate_walking_dead.py, which is why they look identical.",
	},
}


def definition_paths() -> list[Path]:
	paths = sorted((ROOT / "machines" / "partial").rglob("*.json"))
	paths += sorted((ROOT / "machines" / "author-ready").rglob("*.json"))
	return paths


def load(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def first_placements(definition: dict) -> dict[str, tuple[float, float]]:
	points: dict[str, tuple[float, float]] = {}
	for group in ("inputs", "outputs"):
		for device in definition.get(group) or []:
			placements = (device.get("spatial") or {}).get("placements") or []
			if placements:
				points[device["id"]] = (placements[0]["x"], placements[0]["y"])
	return points


def token_pairs(ids, tokens) -> list[tuple[str, str]]:
	"""Ids differing only by one delimited token, e.g. switch.left-outlane / switch.right-outlane."""
	found = []
	for identifier in ids:
		for smaller, larger in tokens:
			pattern = re.compile(r"(?<![a-z])%s(?![a-z])" % re.escape(smaller))
			if pattern.search(identifier):
				partner = pattern.sub(larger, identifier)
				if partner != identifier and partner in ids:
					found.append((identifier, partner))
				break
	return found


class SidednessTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.records = []
		for path in definition_paths():
			definition = load(path)
			machine_id = definition["machine"]["id"]
			if machine_id.startswith("stub."):
				continue
			cls.records.append((machine_id, definition, first_placements(definition)))

	def _allowed(self, machine_id: str, pair: tuple[str, str]) -> bool:
		return pair in KNOWN_INVERSIONS.get(machine_id, {})

	def test_left_right_pairs_are_ordered_by_x(self) -> None:
		"""x = 0 is the left side, so a `left` device must not sit right of its `right` partner."""
		compared = 0
		failures = []
		for machine_id, _, points in self.records:
			for smaller, larger in token_pairs(points, LEFT_RIGHT_TOKENS):
				compared += 1
				if points[smaller][0] > points[larger][0] and not self._allowed(machine_id, (smaller, larger)):
					failures.append(
						"%s: %s x=%.6f is right of %s x=%.6f"
						% (machine_id, smaller, points[smaller][0], larger, points[larger][0])
					)
		self.assertGreater(compared, 100, "the pair discovery stopped working")
		self.assertEqual([], failures, "\n".join(failures))

	def test_upper_lower_pairs_are_ordered_by_y(self) -> None:
		"""y = 0 is the rear/backglass end, so an `upper` device must not sit in front of `lower`."""
		compared = 0
		failures = []
		for machine_id, _, points in self.records:
			for smaller, larger in token_pairs(points, UPPER_LOWER_TOKENS):
				compared += 1
				if points[smaller][1] > points[larger][1] and not self._allowed(machine_id, (smaller, larger)):
					failures.append(
						"%s: %s y=%.6f is in front of %s y=%.6f"
						% (machine_id, smaller, points[smaller][1], larger, points[larger][1])
					)
		self.assertGreater(compared, 20, "the pair discovery stopped working")
		self.assertEqual([], failures, "\n".join(failures))

	def test_co_located_equality_is_not_treated_as_an_inversion(self) -> None:
		"""Guards the check itself.

		Genuinely co-located left/right pairs exist and are legitimate - two eyes of one head
		mechanism, two ends of one motor assembly. If this project ever switches the comparison to
		`>=`, every one of them becomes a permanent false positive, so assert at least one such
		pair exists and passes.
		"""
		equal_pairs = 0
		for machine_id, _, points in self.records:
			for smaller, larger in token_pairs(points, LEFT_RIGHT_TOKENS):
				if points[smaller][0] == points[larger][0]:
					equal_pairs += 1
		self.assertGreater(
			equal_pairs, 0,
			"expected at least one legitimately co-located left/right pair in the corpus",
		)

	def test_known_inversions_all_still_invert(self) -> None:
		"""A ratchet only works if its entries stay live.

		If a listed inversion has been fixed, the entry must be deleted rather than left to excuse a
		future regression at the same coordinates.
		"""
		by_id = {machine_id: points for machine_id, _, points in self.records}
		for machine_id, pairs in KNOWN_INVERSIONS.items():
			self.assertIn(machine_id, by_id, f"{machine_id} in KNOWN_INVERSIONS no longer exists")
			points = by_id[machine_id]
			for (smaller, larger), reason in pairs.items():
				self.assertIn(smaller, points, f"{machine_id}: {smaller} has no placement any more")
				self.assertIn(larger, points, f"{machine_id}: {larger} has no placement any more")
				axis = 1 if any(
					re.search(r"(?<![a-z])%s(?![a-z])" % t, smaller) for t, _ in UPPER_LOWER_TOKENS
				) else 0
				self.assertGreater(
					points[smaller][axis], points[larger][axis],
					f"{machine_id}: {smaller}/{larger} no longer inverts - delete the "
					f"KNOWN_INVERSIONS entry instead of leaving it. Reason on file: {reason}",
				)

	def test_every_known_inversion_names_a_conflict_or_an_open_question(self) -> None:
		for machine_id, pairs in KNOWN_INVERSIONS.items():
			for pair, reason in pairs.items():
				self.assertTrue(
					reason.startswith("conflict.")
					or reason.startswith("UNVERIFIED")
					or reason.startswith("CORRECT:"),
					f"{machine_id} {pair}: reason must cite a conflict id, be marked UNVERIFIED, "
					f"or be marked CORRECT: with the geometry that makes the inversion real",
				)


class DeviceAssemblyCoLocationTests(unittest.TestCase):
	"""A switch, coil and lamp sharing a device name are one assembly and must share a position.

	This is the check that catches the Ripley's shape, where the retained table's switch handling and
	its lamp handling disagree about which physical body carries a name. It is deliberately tolerant:
	a lamp is often nudged off an assembly's exact centre for its glow, and the tolerance only has to
	be tight enough to tell one device from its neighbour.
	"""

	TOLERANCE = 0.03

	# record id -> {(switch_id, partner_id): why}. Same ratchet contract as KNOWN_INVERSIONS.
	KNOWN_ASSEMBLY_GAPS: dict[str, dict[tuple[str, str], str]] = {
		"stern.avengers-limited-edition.2012": {
			("switch.bottom-pop-bumper", "device.bottom-pop-bumper"):
				"UNVERIFIED suspected defect. Solenoid 11 ('Bottom pop bumper') is placed at "
				"(0.670839, 0.215243), which is the LEFT bumper's position - switch 30 and "
				"solenoid 9 both sit at (0.678933, 0.213986) - while switch 32 puts the bottom "
				"bumper at (0.803850, 0.297933). Either solenoid 11 was mapped onto the wrong "
				"table object or the three bumper solenoids are mis-ordered. Note the Pro "
				"edition's curator already documents a reversed bumper switch callback in the "
				"retained script, so this family is known to be error-prone here. See "
				"TO_BE_FIXED.md section 2.1.",
		},
		"stern.metallica-pro.2013": {
			("switch.right-eject-scoop", "device.right-eject-scoop"):
				"UNVERIFIED, and quite possibly legitimate. The switch sits at (0.819515, "
				"0.566214) and the kicker coil at (0.861799, 0.532281), 0.042 apart in x. A scoop "
				"switch sits inside the hole while its kicker coil sits behind and below it, so a "
				"small genuine offset is expected; this may simply exceed a tolerance chosen for "
				"bumpers. Resolve by deciding the right tolerance for scoop assemblies rather than "
				"by moving a coordinate. See TO_BE_FIXED.md section 2.1.",
		},
	}

	@classmethod
	def setUpClass(cls) -> None:
		cls.records = []
		for path in definition_paths():
			definition = load(path)
			if definition["machine"]["id"].startswith("stub."):
				continue
			cls.records.append((definition["machine"]["id"], first_placements(definition)))

	def test_switch_and_coil_of_one_named_device_are_co_located(self) -> None:
		compared = 0
		failures = []
		for machine_id, points in self.records:
			for identifier, position in points.items():
				if not identifier.startswith("switch."):
					continue
				suffix = identifier.split(".", 1)[1]
				for prefix in ("device.", "coil."):
					partner = prefix + suffix
					if partner not in points:
						continue
					compared += 1
					if (identifier, partner) in self.KNOWN_ASSEMBLY_GAPS.get(machine_id, {}):
						continue
					other = points[partner]
					if abs(position[0] - other[0]) > self.TOLERANCE or abs(position[1] - other[1]) > self.TOLERANCE:
						failures.append(
							"%s: %s (%.6f, %.6f) and %s (%.6f, %.6f) are one assembly but sit apart"
							% (machine_id, identifier, *position, partner, *other)
						)
		self.assertGreater(compared, 20, "the assembly discovery stopped working")
		self.assertEqual([], failures, "\n".join(failures))


if __name__ == "__main__":
	unittest.main()
