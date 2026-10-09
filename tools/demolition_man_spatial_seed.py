#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Demolition Man (Williams 1994) curator.

The curator must reproduce byte for byte without the 112 MB table, so the objects it places are frozen in
``tools/seeds/williams/demolition-man-1994-spatial.json``. This tool rebuilds that seed from the retained vpxtool
extraction with the repository's own normalizing helper and refuses to write when the extraction's table hash
differs from the pinned Knorr/Kiwi 1.3.1 table.

Each device lists the table objects its placement comes from. An object is chosen through the retained script's
own binding (its Hit handler, cvpmBallStack/cvpmMech registration, SolCallback/SolModCallback target or lamp
fader call), never from its name alone; a ``projection`` text marks a device whose sensor or actuator the table
does not model and that is projected onto its mechanism's object.

    python tools/demolition_man_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.spatial import extract_spatial_candidates  # noqa: E402

SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "demolition-man-1994-spatial.json"
TABLE_SHA256 = "099c70add2201ea3e49c34c9f910e365bd88218d8bf755846ceee93bce82fbd3"

TROUGH = "cvpmBallStack bsTrough has no switch objects; projected onto its release kicker BallRelease"
CLAW = "the Cryoclaw arm is the Claw primitive rotated about its position; projected onto that pivot"
ELEVATOR = "the elevator is a cvpmMech with no switch object; projected onto ElevatorKicker, where the elevator takes the ball"
# Public switch -> [(VPX type, object, projection or None)].
SWITCHES = {
	15: [("Trigger", "sw15", None)], 16: [("Trigger", "sw16", None)], 17: [("Trigger", "sw17", None)], 18: [("Trigger", "sw18", None)],
	25: [("Primitive", "Claw", CLAW)], 26: [("Primitive", "Claw", CLAW)], 27: [("Trigger", "sw27", None)],
	31: [("Kicker", "BallRelease", TROUGH)], 32: [("Kicker", "BallRelease", TROUGH)], 33: [("Kicker", "BallRelease", TROUGH)],
	34: [("Kicker", "BallRelease", TROUGH)], 35: [("Kicker", "BallRelease", TROUGH)], 36: [("Kicker", "BallRelease", TROUGH)],
	38: [("Wall", "Standup38", None)], 41: [("Wall", "LeftSlingShot", None)], 42: [("Wall", "RightSlingShot", None)],
	43: [("Bumper", "leftjetbumper", None)], 44: [("Wall", "TopSlingShot", None)], 45: [("Bumper", "rightjetbumper", None)],
	46: [("Trigger", "sw46", None)], 47: [("Trigger", "sw47", None)], 48: [("Trigger", "sw48", None)],
	51: [("Trigger", "sw51", None)], 52: [("Trigger", "sw52", None)], 53: [("Trigger", "sw53", None)],
	54: [("Wall", "UpperRebound", None)], 55: [("Trigger", "sw55", None)], 56: [("Wall", "Standup56", None)],
	57: [("Wall", "Standup57", None)], 58: [("Wall", "Standup58", None)], 61: [("Trigger", "sw61", None)],
	62: [("Trigger", "sw62", None)], 63: [("Trigger", "sw63", None)], 64: [("Trigger", "sw64", None)], 65: [("Trigger", "sw65", None)],
	66: [("Kicker", "sw66", None)], 67: [("Kicker", "ElevatorKicker", ELEVATOR)], 71: [("Trigger", "sw71", None)],
	72: [("Trigger", "sw72", None)], 73: [("Kicker", "sw73", None)], 74: [("Kicker", "ElevatorKicker", None)],
	76: [("Kicker", "sw76", None)], 77: [("Wall", "Standup77", None)], 78: [("Wall", "Standup78", None)],
	81: [("Kicker", "ClawRampKicker", None)], 82: [("Trigger", "sw82", None)], 83: [("Trigger", "sw83", None)],
	84: [("Trigger", "sw84", None)], 85: [("Trigger", "sw85", None)], 86: [("Trigger", "sw86", None)],
	87: [("Wall", "Standup87", None)], 88: [("Wall", "LowerRebound", None)],
}
DIVERTER = "the right-ramp diverter coil's two windings move the DiverterR flipper; the power winding has no callback and is projected onto it"
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Kicker", "sw76", None)], 3: [("Kicker", "Kicker1", None)], 4: [("Kicker", "sw73", None)],
	5: [("Flipper", "DiverterR", DIVERTER)], 9: [("Wall", "LeftSlingShot", None)], 10: [("Wall", "RightSlingShot", None)],
	11: [("Bumper", "leftjetbumper", None)], 12: [("Wall", "TopSlingShot", None)], 13: [("Bumper", "rightjetbumper", None)],
	14: [("Kicker", "sw66", None)], 15: [("Flipper", "DiverterR", None)],
	18: [("Kicker", "ElevatorKicker", "the elevator motor's cvpmMech has no object of its own; projected onto ElevatorKicker")],
	19: [("Primitive", "Claw", CLAW)], 20: [("Primitive", "Claw", CLAW)],
	33: [("Primitive", "Claw", "the claw magnet rides on the arm; projected onto the arm's pivot")],
	21: [("Light", "l121", None)], 22: [("Light", "l122", None)], 23: [("Light", "l123", None)], 24: [("Light", "l124", None)],
	25: [("Light", "l125", None)], 26: [("Light", "l126", None)], 27: [("Light", "l127", None)], 28: [("Light", "l128", None)],
	51: [("Light", "l137", None)], 52: [("Light", "l138", None)], 53: [("Light", "l139", None)], 54: [("Light", "l140", None)],
	57: [("Light", "l143", None)], 58: [("Light", "l144", None)],
	35: [("Flipper", "LeftFlipper1", None)], 36: [("Flipper", "LeftFlipper1", None)],
	45: [("Flipper", "RightFlipper", None)], 46: [("Flipper", "RightFlipper", None)],
	47: [("Flipper", "LeftFlipper", None)], 48: [("Flipper", "LeftFlipper", None)],
}
# Public lamp -> [(VPX type, object, note or None)]: the insert Light each lamp's fader drives (the matching
# 'b' halo light is a render double at the same spot and is not placed).
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {
	address: [("Light", f"l{address}", None)]
	for address in (12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45,
		46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 76, 77, 78, 81, 84, 85)
}
LAMPS[11] = [("Light", "l11a", None), ("Light", "l11b", None)]
LAMPS[82] = [("Light", "l82", None), ("Light", "l82a", None)]
LAMPS[83] = [
	("Light", "l83", "the table's fader drives l83 and l83a from lamp 82, not 83; they are the inner pair of the centre-ramp bar"),
	("Light", "l83a", "the table's fader drives l83 and l83a from lamp 82, not 83; they are the inner pair of the centre-ramp bar"),
]
# Public G.I. string -> the table collection UpdateGI drives for it (wpc.vbs passes zero-based string numbers).
GI_COLLECTIONS = {1: "GIString2", 2: "GIString3", 3: "GIString4", 4: "GIString5"}
STACK_DISTANCE = 0.006  # normalized; bulbs closer than this are one socket the table doubled for rendering


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Demolition Man Knorr/Kiwi 1.3.1 table")
	if candidates["bounds"] != {"left": 0.0, "top": 0.0, "right": 1093.0, "bottom": 2162.0}:
		raise SystemExit(f"unexpected table bounds {candidates['bounds']}")
	return {(item["type"], item["name"]): item for item in candidates["objects"]}


def _entries(by_key: dict, rows: list[tuple[str, str, str | None]]) -> list[dict]:
	entries = []
	for kind, name, note in rows:
		found = by_key.get((kind, name))
		if found is None:
			raise SystemExit(f"missing table object {kind} {name}")
		entry = {"object": name, "type": kind, "x": found["x"], "y": found["y"]}
		if note:
			entry["projection" if kind != "Light" else "note"] = note
		entries.append(entry)
	return entries


def _gi(extracted: Path, by_key: dict) -> dict[str, list[dict]]:
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	result: dict[str, list[dict]] = {}
	for string, collection in GI_COLLECTIONS.items():
		lights = sorted((name for name in collections[collection] if ("Light", name) in by_key), key=str.casefold)
		groups: list[dict] = []
		for name in lights:
			point = by_key[("Light", name)]
			for group in groups:
				if math.dist((group["x"], group["y"]), (point["x"], point["y"])) < STACK_DISTANCE:
					group["collapsed"].append(name)
					break
			else:
				groups.append({"object": name, "collapsed": [name], "x": point["x"], "y": point["y"]})
		result[str(string)] = groups
	return result


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	return {
		"format": "pinmame-demolition-man-spatial-seed",
		"version": 1,
		"machine_id": "williams.demolition-man.1994",
		"table": {"sha256": TABLE_SHA256, "width": 1093.0, "height": 2162.0, "units": "vpx"},
		"switch": {str(address): _entries(by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": {str(address): _entries(by_key, rows) for address, rows in sorted(SOLENOIDS.items())},
		"lamp": {str(address): _entries(by_key, rows) for address, rows in sorted(LAMPS.items())},
		"gi": _gi(extracted, by_key),
	}


def canonical(value: dict) -> str:
	return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--extracted", type=Path, required=True)
	parser.add_argument("--vpx", type=Path, required=True)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical(build(args.extracted, args.vpx))
	if args.check:
		if not SEED_PATH.is_file() or SEED_PATH.read_bytes() != text.encode("utf-8"):
			raise SystemExit(f"Demolition Man spatial seed drift: {SEED_PATH}")
		print("Demolition Man spatial seed matches the retained extraction.")
		return
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
