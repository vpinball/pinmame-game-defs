#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Stern The Sopranos (2005) curator.

The curator must reproduce byte for byte without the 73 MB table, so the objects it places are frozen in
``tools/seeds/stern/the-sopranos-2005-spatial.json``. This tool rebuilds that seed from the retained vpxtool
extraction with the repository's own normalizing helper and refuses to write when the table hash or bounds differ
from the pinned freneticamnesic/32assassin 1.0.2 table.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded
script binding (its Hit/Spin/Slingshot handler, cvpmBallStack/cvpmDropTarget/cvpmImpulseP registration,
SolCallback target or lamp fader call), never from its name alone. A ``projection`` text marks a device whose
sensor or actuator the table does not model and that is projected onto the object of the mechanism it belongs to;
a ``midpoint`` entry is the mean of two named objects and is always a projection.

    python tools/sopranos_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> [--check]
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

SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "the-sopranos-2005-spatial.json"
TABLE_SHA256 = "9bbc98d47888c28843cf17aa7f8ce5d04671da86ee1e76ddb1f2cd330b30162c"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2300.0}

TROUGH = "cvpmBallStack bsTrough (InitSw 0, 14, 13, 12, 11) has no switch objects; projected onto its release kicker BallRelease"
STACKING = "the table models no stacking opto (its solTrough pulses switch 22 instead); projected onto the trough release kicker BallRelease"
SAFE = "the safe door is the pair of walls sw21/sw24 the safe animation drops; projected onto their midpoint"
SAFE_LIMIT = "PrisonT_Timer writes switch 10 when the safe door finishes opening or closing; no switch object, projected onto the safe door walls' midpoint"
EOS = "the end-of-stroke contact sits on the flipper assembly; projected onto the flipper the table animates"
DROP = "the 1-bank drop target's {coil} coil acts on the target dtSingle registers; projected onto that target"
FISH_JAW = "the fish-jaw coil moves the fishmouth primitive SolFish animates through the invisible helper flipper fishf; projected onto the jaw primitive"
FISH_FLASH = "the table renders the fish-eye flash only as Flasher sprites f125a/f125b; projected onto the fish jaw primitive at the fish head"
BING = "the Bada Bing! motor relay turns the two pole-dancer primitives strippert_Timer spins; projected onto their midpoint"
AUTO = "cvpmImpulseP plungerIM fires from the shooter-lane trigger swplunger"

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "a|b", text) entry averages two objects.
SWITCHES = {
	9: [("Gate", "sw9", None)], 10: [("midpoint", "Wall:sw21|Wall:sw24", SAFE_LIMIT)],
	11: [("Kicker", "BallRelease", TROUGH)], 12: [("Kicker", "BallRelease", TROUGH)], 13: [("Kicker", "BallRelease", TROUGH)],
	14: [("Kicker", "BallRelease", TROUGH)], 15: [("Kicker", "BallRelease", STACKING)], 16: [("Trigger", "swPlunger", None)],
	17: [("Kicker", "sw17", None)], 18: [("Gate", "sw18", None)], 19: [("Trigger", "sw19", None)], 20: [("Trigger", "sw20", None)],
	21: [("Wall", "sw21", None)], 22: [("Trigger", "sw22", None)], 23: [("Trigger", "sw23", None)], 24: [("Wall", "sw24", None)],
	25: [("Spinner", "sw25", None)], 26: [("HitTarget", "sw26", None)], 27: [("Spinner", "sw27", None)], 28: [("Kicker", "sw28", None)],
	29: [("Gate", "sw29", None)], 31: [("Trigger", "sw31", None)], 32: [("Trigger", "sw32", None)], 33: [("Gate", "sw33", None)],
	34: [("HitTarget", "sw34", None)], 35: [("HitTarget", "sw35", None)], 36: [("HitTarget", "sw36", None)], 37: [("HitTarget", "sw37", None)],
	38: [("Trigger", "sw38", None)], 39: [("Trigger", "sw39", None)], 40: [("Trigger", "sw40", None)],
	49: [("Bumper", "Bumper1", None)], 50: [("Bumper", "Bumper2", None)], 51: [("Bumper", "Bumper3", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "LeftSlingShot", None)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "RightSlingShot", None)],
	81: [("Flipper", "RightFlipper", EOS)], 83: [("Flipper", "LeftFlipper", EOS)],
}
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Trigger", "swPlunger", AUTO)], 3: [("Kicker", "sw28", None)],
	4: [("Wall", "CenterPost", None)], 5: [("Gate", "sol5", None)], 6: [("Gate", "sol6", None)],
	7: [("HitTarget", "sw26", DROP.format(coil="trip"))], 8: [("midpoint", "Wall:sw21|Wall:sw24", SAFE)],
	9: [("Bumper", "Bumper1", None)], 10: [("Bumper", "Bumper2", None)], 11: [("Bumper", "Bumper3", None)],
	12: [("Wall", "LeftSlingShot", None)], 13: [("Wall", "RightSlingShot", None)], 14: [("HitTarget", "sw26", DROP.format(coil="reset"))],
	17: [("Primitive", "fishmouth", FISH_JAW)], 18: [("midpoint", "Primitive:stripper1|Primitive:stripper2", BING)],
	19: [("Light", "L119", None)], 20: [("Light", "L120", None)], 21: [("Kicker", "sw17", None)],
	22: [("Wall", "BoatPost", None)], 23: [("Wall", "BingPost", None)],
	25: [("Primitive", "fishmouth", FISH_FLASH)], 26: [("Light", "L126", None)], 27: [("Light", "f127", None)],
	28: [("Light", "f128", None)], 29: [("Light", "l29a", None), ("Light", "l29b", None)],
	30: [("midpoint", "Wall:sw21|Wall:sw24", SAFE)], 31: [("Light", "L131", None)],
	32: [("Light", "L32a", None), ("Light", "L32b", None)],
	45: [("Flipper", "RightFlipper", None)], 46: [("Flipper", "RightFlipper", None)],
	47: [("Flipper", "LeftFlipper", None)], 48: [("Flipper", "LeftFlipper", None)],
}
# Public lamp -> [(VPX type, object, note or None)]: the Light each lamp's NFadeL call drives.
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {address: [("Light", f"l{address}", None)] for address in list(range(1, 62)) + [78]}
STACK_DISTANCE = 0.006  # normalized; GI lights closer than this are one socket the table doubled for rendering


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned The Sopranos 1.0.2 table")
	if candidates["bounds"] != BOUNDS:
		raise SystemExit(f"unexpected table bounds {candidates['bounds']}")
	return {(item["type"], item["name"]): item for item in candidates["objects"]}


def _point(by_key: dict, kind: str, name: str) -> tuple[float, float]:
	found = by_key.get((kind, name))
	if found is None:
		raise SystemExit(f"missing table object {kind} {name}")
	return found["x"], found["y"]


def _entries(by_key: dict, rows: list[tuple[str, str, str | None]]) -> list[dict]:
	entries = []
	for kind, name, note in rows:
		if kind == "midpoint":
			points = [_point(by_key, *part.split(":")) for part in name.split("|")]
			x = round(sum(p[0] for p in points) / len(points), 6)
			y = round(sum(p[1] for p in points) / len(points), 6)
			entry = {"object": name.replace("|", " + "), "type": "midpoint", "x": x, "y": y}
		else:
			x, y = _point(by_key, kind, name)
			entry = {"object": name, "type": kind, "x": x, "y": y}
		if note:
			entry["projection" if kind != "Light" else "note"] = note
		entries.append(entry)
	return entries


def _gi(extracted: Path, by_key: dict) -> list[dict]:
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	lights = sorted((name for name in collections["GI"] if ("Light", name) in by_key), key=str.casefold)
	groups: list[dict] = []
	for name in lights:
		x, y = _point(by_key, "Light", name)
		for group in groups:
			if math.dist((group["x"], group["y"]), (x, y)) < STACK_DISTANCE:
				group["collapsed"].append(name)
				break
		else:
			groups.append({"object": name, "collapsed": [name], "x": x, "y": y})
	return groups


def build(extracted: Path, vpx: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	return {
		"format": "pinmame-sopranos-spatial-seed",
		"version": 1,
		"machine_id": "stern.the-sopranos.2005",
		"table": {"sha256": TABLE_SHA256, "width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx"},
		"switch": {str(address): _entries(by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": {str(address): _entries(by_key, rows) for address, rows in sorted(SOLENOIDS.items())},
		"lamp": {str(address): _entries(by_key, rows) for address, rows in sorted(LAMPS.items())},
		"gi": {"0": _gi(extracted, by_key)},
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
			raise SystemExit(f"The Sopranos spatial seed drift: {SEED_PATH}")
		print("The Sopranos spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
