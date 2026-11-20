#!/usr/bin/env python3
"""Regenerate the retained-table geometry seed for the Sega Starship Troopers (1997) curator.

The curator must reproduce byte for byte without the retained table, so the objects it places are frozen in
``tools/seeds/sega/starship-troopers-1997-spatial.json``. This tool rebuilds that seed from the retained vpxtool
extraction with the repository's own normalizing helper. It reads no coordinate until the extraction matches the file
count, byte count and manifest digest the curator pins, and it refuses to write when the table hash or bounds differ
from the pinned VPW Mod v2.0 table.

A flasher is placed only on a script-driven Light that sits on a bulb, dome or socket the table models. The table's
flasher Lights draw no bulb mesh of their own, so the builder reads the retained `vpxtool export obj --units vpu`
world-space export, splits the named mesh objects into connected pieces (vertices agreeing at 0.1 VPU welded) and
records, for every placed flasher Light, the one piece of each object whose bounds contain it, with the piece's height
above the playfield (the export's z is the negated height). The placement is the centre of the piece that holds the
bulb (the KabeSockel socket under a Mini-Mars dome, or the bulb itself), not the render Light, whose own point is kept
as ``light``. The flasher Lights that sit on no such piece are listed as unplaced. The export's frame is checked against the bumper Bumper1, whose base mesh must centre within 1 VPU of the
bumper's stored centre. The lamps whose Lights sit on a bulb the table models (the turbo bumpers, the ramp nukes and
the Tanker Bug sign) record that bulb's piece the same way and are placed at its centre, and every piece of those bulb
objects must belong to exactly one of them.

The lamps DR. 5 draws below the playfield (black boxes) light playfield inserts, and the table models no bulb or socket
under the playfield: it lights each insert with a bulb light that draws no bulb mesh. Such a lamp is projected onto that
light, the insert's position rather than a measured socket, and the builder refuses one whose light draws a bulb.

Each 7-segment LED segment is a Flasher quad over a texture that draws the one bar it lights. The quad is axis-aligned
and wrap-mapped, which VPX maps linearly across the quad's bounds, so the segment's point is the intensity-weighted
centroid of the texture's lit pixels carried onto the quad. The builder checks that each digit's seven points fall in
the A-G arrangement of the manual's "TYPICAL 7-SEGMENT ADDRESS" key and the four digits in the 2x2 layout DR. 5 draws.

Each device lists the table objects its placement comes from. An object is chosen through the table's embedded script
binding (its Hit/Slingshot handler, cvpmBallStack/cvpmSaucer/cvpmMagnet/cvpmMyMech registration, SolCallback target or
UpdateLamps assignment), never from its name alone. A ``projection`` text marks a device whose sensor or actuator the
table does not model, or binds to an object other than the one the manual places it on, and that is projected onto
the object named; a ``midpoint`` entry is the mean of two named objects and is always a projection. A ``drawing`` text
names the manual drawing a table-derived placement was checked against.

    python tools/starship_troopers_spatial_seed.py --extracted <extracted-vpxtool> --vpx <table.vpx> --obj <export.obj> [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402
from pinmame_game_defs.spatial import _round_point, extract_spatial_candidates  # noqa: E402

SEED_PATH = ROOT / "tools" / "seeds" / "sega" / "starship-troopers-1997-spatial.json"
TABLE_SHA256 = "0d7020ac848dc66f12d5faf2a12961bde69a606d154511947755bd0ac9b4731a"
BOUNDS = {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2133.17}
OBJ_SHA256 = "cb0003b5b9f3636e279d1df332ae6a848dab965906c94e6a5895ae024d83406d"

TROUGH = "the switch location drawing (DR. 5) draws 12-15 on the trough at the lower right; cvpmBallStack bsTrough (InitSw 0, 15, 14, 13, 12) has no switch objects, so each is projected onto its release kicker BallRelease"
UNDER = "the under-trough switch is mounted below the playfield (DR. 5 black box); projected onto the table object at the hole that feeds it, which the script binds to this switch"
REAR = "the switch location drawing (DR. 5) draws 33 at the rear of the warrior bug track; cvpmMyMech mBug registers it at its last steps (AddSw 33, 221, 222), where UpdateWarriorBug raises BWall24, so the rear stepper switch is projected onto that wall"
FRONT = "the switch location drawing (DR. 5) draws 34 at the front end of the warrior bug track; cvpmMyMech mBug registers it at its first steps (AddSw 34, 0, 1), where UpdateWarriorBug raises BWall1, so the front stepper switch is projected onto that wall"
BUG_HIT = "the switch location drawing (DR. 5) draws 35 on the warrior bug track; BWalls_Hit pulses 35 from whichever of BWall1-BWall24 the moving warrior bug has raised, and the switch rides the bug, so it is projected onto the midpoint of the track's end walls"
BRAIN = "the switch location drawing (DR. 5) draws 37 and 39 beside the brain bug 38 at the centre; SolBrainBug raises the walls sw38 and sw38a and sets switches 37 and 39 with no object of their own, so they are projected onto sw38a, the centre of the region SolBrainBug clears (InRect 472-714 x 871-1126)"
BRAIN_COIL = "the coil location drawing (DR. 7) draws coil 7 on the large assembly at the centre; SolBrainBug raises the walls sw38 and sw38a, so the coil is projected onto sw38a, the centre of the region SolBrainBug clears (InRect 472-714 x 871-1126)"
EOS = "the 3-Flipper Circuit Wiring Diagram (printed page 92) wires this end-of-stroke contact on the lower flipper assembly; projected onto the flipper the table animates"
SLING_LEFT = "the manual draws switch 59 at the left slingshot (DR. 5); the table's Leftslingshot handler pulses 62 instead, so it is placed on the left slingshot wall by the manual, not by the script binding"
SLING_RIGHT = "the manual draws switch 62 at the right slingshot (DR. 5); the table's Rightslingshot handler pulses 59 instead, so it is placed on the right slingshot wall by the manual, not by the script binding"
AUTO = "the coil location drawing (DR. 7) draws coil 2 at the shooter lane; SolAutoLaunch fires the table's Plunger object with Autoplunger set"
STEPPER = (
	"the coil location drawing (DR. 7) labels the stepper phases 17-20 along the warrior bug track, and the Warrior Bug Assembly's "
	"side and top views (printed page 78) mount its one HSI stepper motor (item 3) at one end of the base, opposite the bug (item "
	"15) and beside the upright Screened Plastic -21 Assy (item 14) whose #555 DR. 5 draws as lamp 34 at the rear head of the "
	"track; the top view's two #906 bulbs (item 13), a little past the middle toward the motor, are the two bulbs the table "
	"models on WarriorBugAssembly006, nearer BWall24 than BWall1, so the motor end is the rear and the motor is projected onto "
	"BWall24, the rearmost wall cvpmMyMech mBug (Sol1 = 17, four-step) raises"
)
LAMP_34 = "the script binds no object to lamp 34; DR. 5 draws it at the rear head of the warrior bug track, projected onto the rearmost bug wall BWall24"
INSERT = (
	"DR. 5 draws this lamp as a black box, mounted below the playfield, at the insert it lights; the table models no bulb or "
	"socket under the playfield, so the lamp is projected onto the bulb light UpdateLamps drives for it, which lights that insert "
	"and draws no bulb mesh: the point is the insert's position in the table, not a measured socket"
)
LED = (
	"UpdateLamps drives this segment's Flasher; the point is the lit centroid of its segment texture carried onto the Flasher's "
	"wrap-mapped quad, and each digit's seven points fall in the A-G arrangement of the TYPICAL 7-SEGMENT ADDRESS key on DR. 5 "
	"(A top, B upper right, C lower right, D bottom, E lower left, F upper left, G middle) and the four digits in its two-by-two "
	"layout (WARRIOR top left, HOPPER top right, PLASMA bottom left, TANKER bottom right)"
)
TANKER = (
	"the Tanker Bug Assembly over the super VUK (printed pages 8 and 59, item 12) carries the Screened Plastic -20 Assy, the Tanker "
	"Bug Sign (printed page 61, item 20), with three #555 bulbs in offset sockets under red, blue and fluorescent orange covers; "
	"the table models the sign upright, its three bulbs at one depth with that of 39 below those of 35 and 36, which is how DR. 5 "
	"draws 39 under the pair"
)
STACK_DISTANCE = 0.010  # normalized
SEGMENTS = "ABCDEFG"
LIT_FRACTION = 0.25  # a texture pixel counts as lit above this share of the brightest pixel

# Public switch -> [(VPX type, object, projection or None)]. A ("midpoint", "Type:a|Type:b", text) entry averages two objects.
SWITCHES = {
	9: [("Trigger", "sw9", UNDER)], 10: [("Kicker", "sw10", UNDER)],
	12: [("Kicker", "BallRelease", TROUGH)], 13: [("Kicker", "BallRelease", TROUGH)], 14: [("Kicker", "BallRelease", TROUGH)],
	15: [("Kicker", "BallRelease", TROUGH)], 16: [("Trigger", "sw16", None)],
	17: [("Wall", "T17", None)], 18: [("Wall", "T18", None)], 19: [("Wall", "T19", None)], 20: [("Wall", "T20", None)],
	21: [("Wall", "T21", None)], 22: [("Wall", "T22", None)], 23: [("Wall", "T23", None)], 24: [("Wall", "T24", None)],
	25: [("Trigger", "sw25", None)], 26: [("Trigger", "sw26", None)],
	27: [("Wall", "T27", None)], 28: [("Wall", "T28", None)], 29: [("Wall", "T29", None)], 30: [("Wall", "T30", None)],
	31: [("Wall", "T31", None)], 32: [("Wall", "T32", None)],
	33: [("Wall", "BWall24", REAR)], 34: [("Wall", "BWall1", FRONT)], 35: [("midpoint", "Wall:BWall1|Wall:BWall24", BUG_HIT)],
	37: [("Wall", "sw38a", BRAIN)], 38: [("Wall", "sw38", None)], 39: [("Wall", "sw38a", BRAIN)], 40: [("Trigger", "sw40", UNDER)],
	41: [("Trigger", "sw41", None)], 42: [("Trigger", "sw42", None)], 43: [("Trigger", "sw43", None)],
	45: [("Kicker", "sw45", None)], 46: [("Kicker", "sw46", None)], 47: [("Trigger", "sw47", None)], 48: [("Trigger", "sw48", None)],
	49: [("Bumper", "Bumper1", None)], 50: [("Bumper", "Bumper3", None)], 51: [("Bumper", "Bumper2", None)],
	52: [("Trigger", "sw52", None)], 53: [("Trigger", "sw53", None)],
	57: [("Trigger", "sw57", None)], 58: [("Trigger", "sw58", None)], 59: [("Wall", "Leftslingshot", SLING_LEFT)],
	60: [("Trigger", "sw60", None)], 61: [("Trigger", "sw61", None)], 62: [("Wall", "Rightslingshot", SLING_RIGHT)],
	81: [("Flipper", "rightflipper", EOS)], 83: [("Flipper", "leftflipper", EOS)],
}
_STEPPER_ROWS = [("Wall", "BWall24", STEPPER)]
# The warrior bug track's end walls: the front one the bug's rubber bumper end reaches, the rear one at the motor.
BUG_FRONT, BUG_REAR = "BWall1", "BWall24"
# Public solenoid -> [(VPX type, object, projection or None)].
SOLENOIDS = {
	1: [("Kicker", "BallRelease", None)], 2: [("Plunger", "plunger", AUTO)], 3: [("Kicker", "sw45", None)], 4: [("Kicker", "sw46", None)],
	5: [("Trigger", "LeftMagnet", None)], 6: [("Trigger", "RightMagnet", None)], 7: [("Wall", "sw38a", BRAIN_COIL)],
	9: [("Bumper", "Bumper1", None)], 10: [("Bumper", "Bumper3", None)], 11: [("Bumper", "Bumper2", None)],
	12: [("Wall", "Leftslingshot", None)], 13: [("Wall", "Rightslingshot", None)], 14: [("Flipper", "RightFlipperS", None)],
	17: _STEPPER_ROWS, 18: _STEPPER_ROWS, 19: _STEPPER_ROWS, 20: _STEPPER_ROWS,
	25: [("Light", "l125a", None), ("Light", "l125b", None), ("Light", "l125c", None), ("Light", "l125d", None)],
	26: [("Light", "l126a", None), ("Light", "l126b", None), ("Light", "l126c", None), ("Light", "l126d", None)],
	27: [("Light", "l127a", None), ("Light", "l127b", None), ("Light", "l127c", None), ("Light", "l127d", None)],
	28: [("Light", "l128a", None), ("Light", "l128b", None), ("Light", "l128c", None), ("Light", "l128d", None)],
	29: [("Light", "l129", None), ("Light", "l129a", None)],
	46: [("Flipper", "rightflipper", None)], 48: [("Flipper", "leftflipper", None)],
}
# Placed flasher -> the mesh objects each of its Lights must sit on: the Mini-Mars dome and its socket, or the bulbs
# modelled on the warrior bug assembly.
FLASHER_MESHES = {
	25: ("CapsRed", "KabeSockel"), 26: ("CapsYellow", "KabeSockel"), 27: ("CapsGreen", "KabeSockel"), 28: ("CapsBlue", "KabeSockel"),
	29: ("WarriorBugAssembly006",),
}
# The other script-driven flasher Lights (SetLamp 123, 130, 131 and 132 in UpdateLamps); none sits on a modelled bulb,
# dome or socket, so they place nothing.
UNPLACED_FLASHER_LIGHTS = {23: ("l123a", "l123b"), 30: ("l130b", "l130c", "l130d"), 31: ("l131b", "l131c", "l131d"), 32: ("l132",)}
BULB_OBJECTS = (
	"CapsRed", "CapsYellow", "CapsGreen", "CapsBlue", "CapsRed001", "CapsYellow001", "CapsGreen001", "CapsBlue001",
	"KabeSockel", "bulbs_red", "bulbs_yellow", "bulbs_blue", "WarriorBugAssembly006",
)
# Placed lamp -> the bulb object its Light sits on: the turbo bumper caps, the Tanker Bug sign and the ramp nukes. Every
# piece of these objects belongs to exactly one of these lamps.
LAMP_BULB_OBJECTS = ("bulbs_blue", "bulbs_red", "bulbs_yellow")
# The pieces that hold a bulb: an emitter on one of them is placed at that piece's centre.
ANCHOR_OBJECTS = ("KabeSockel", "WarriorBugAssembly006") + LAMP_BULB_OBJECTS
LAMP_MESHES = {28: "bulbs_red", 29: "bulbs_red", 30: "bulbs_red", 35: "bulbs_yellow", 36: "bulbs_red", 39: "bulbs_blue", 47: "bulbs_red", 48: "bulbs_red"}
TANKER_SIGN = (35, 36, 39)
OBJ_CONTROL = ("Bumper1", "Bumper1Base")
# The four digits in DR. 5's order (top left, top right, bottom left, bottom right), each the seven lamps of its row.
DIGITS = [list(range(first, first + 7)) for first in (49, 57, 65, 73)]
_LED_LAMPS = [address for digit in DIGITS for address in digit]
# Public lamp -> [(VPX type, object, note or None)]: the object UpdateLamps drives for lamp n.
# The lamps DR. 5 draws below the playfield: each lights an insert, and the table models no bulb under it.
INSERT_LAMPS = tuple(list(range(1, 28)) + [31, 32, 37, 38, 40] + list(range(41, 47)) + [56, 64, 72, 80])
LAMPS: dict[int, list[tuple[str, str, str | None]]] = {
	**{address: [("Light", f"l{address}", None)] for address in LAMP_MESHES},
	**{address: [("insert", f"l{address}", INSERT)] for address in INSERT_LAMPS if address not in range(13, 17) and address != 40},
	**{address: [("insert", f"l{address}a", INSERT)] for address in range(13, 17)},
	**{address: [("segment", f"l{address}", LED)] for address in _LED_LAMPS},
	34: [("Wall", "BWall24", LAMP_34)],
	40: [("insert", "l40", INSERT), ("insert", "l40a", INSERT)],
}
LAMP_DRAWINGS = {address: TANKER for address in TANKER_SIGN}


def _verify_extraction(extracted: Path) -> None:
	"""Refuse an extraction that is not, file for file, the retained one the curator pins."""
	import curate_starship_troopers as curator

	try:
		manifest = curator.build_extraction_manifest(extracted)
	except RuntimeError as error:
		raise SystemExit(str(error)) from error
	files = manifest["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(manifest)).hexdigest())
	if identity != (curator.EXTRACTION_FILE_COUNT, curator.EXTRACTION_TOTAL_BYTES, curator.EXTRACTION_MANIFEST_SHA256):
		raise SystemExit(f"the extraction is not the pinned retained extraction: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")


def _candidates(extracted: Path, vpx: Path) -> dict[tuple[str, str], dict]:
	_verify_extraction(extracted)
	candidates = extract_spatial_candidates(extracted, vpx)
	if candidates["source"]["vpx_sha256"] != TABLE_SHA256:
		raise SystemExit("the retained table is not the pinned Starship Troopers VPW Mod v2.0 table")
	if candidates["bounds"] != BOUNDS:
		raise SystemExit(f"unexpected table bounds {candidates['bounds']}")
	return {(item["type"], item["name"]): item for item in candidates["objects"]}


def _point(by_key: dict, kind: str, name: str) -> tuple[float, float]:
	found = by_key.get((kind, name))
	if found is None:
		raise SystemExit(f"missing table object {kind} {name}")
	return found["x"], found["y"]


def _normal(x: float, y: float) -> tuple[float, float]:
	"""A VPU point in the normalized playfield space, rounded as the repository's candidate extraction rounds."""
	return (
		_round_point((x - BOUNDS["left"]) / (BOUNDS["right"] - BOUNDS["left"])),
		_round_point((y - BOUNDS["top"]) / (BOUNDS["bottom"] - BOUNDS["top"])),
	)


def _texture_centroid(extracted: Path, image: str) -> tuple[float, float]:
	"""Intensity-weighted centre of a texture's lit pixels as (u, v), with v = 0 at the image's top row."""
	from PIL import Image  # only the seed builder needs Pillow

	matches = sorted(path for path in (extracted / "images").iterdir() if path.stem.casefold() == image.casefold())
	if len(matches) != 1:
		raise SystemExit(f"segment texture {image} matches {len(matches)} image files")
	with Image.open(matches[0]) as picture:
		rgba = picture.convert("RGBA")
		width, height = rgba.size
		data = rgba.tobytes()
	values = [max(data[index], data[index + 1], data[index + 2]) * data[index + 3] / 255 for index in range(0, len(data), 4)]
	cutoff = max(values) * LIT_FRACTION
	total = sum_u = sum_v = 0.0
	for index, value in enumerate(values):
		if value > cutoff:
			total += value
			sum_u += value * (index % width + 0.5)
			sum_v += value * (index // width + 0.5)
	return round(sum_u / total / width, 4), round(sum_v / total / height, 4)


def _segment(extracted: Path, name: str, note: str) -> dict:
	"""A 7-segment LED segment's point: its texture's lit centroid on the Flasher's wrap-mapped quad."""
	flasher = json.loads((extracted / "gameitems" / f"Flasher.{name}.json").read_text(encoding="utf-8"))["Flasher"]
	if (flasher["rot_x"], flasher["rot_y"], flasher["rot_z"]) != (0.0, 0.0, 0.0) or flasher["image_alignment"] != "wrap":
		raise SystemExit(f"segment Flasher {name} is rotated or not wrap-mapped")
	if flasher["image_b"] not in ("", flasher["image_a"]):
		raise SystemExit(f"segment Flasher {name} blends two textures")
	corners = {(point["x"], point["y"]) for point in flasher["drag_points"]}
	xs = sorted({corner[0] for corner in corners})
	ys = sorted({corner[1] for corner in corners})
	if len(flasher["drag_points"]) != 4 or len(xs) != 2 or len(ys) != 2 or corners != {(x, y) for x in xs for y in ys}:
		raise SystemExit(f"segment Flasher {name} is not an axis-aligned quad")
	u, v = _texture_centroid(extracted, flasher["image_a"])
	x = xs[0] + u * (xs[1] - xs[0])
	y = ys[0] + v * (ys[1] - ys[0])
	point = _normal(x, y)
	return {"object": name, "type": "Flasher", "x": point[0], "y": point[1], "segment": {"image": flasher["image_a"], "u": u, "v": v}, "drawing": note}


def _entries(extracted: Path, by_key: dict, rows: list[tuple[str, str, str | None]]) -> list[dict]:
	entries = []
	for kind, name, note in rows:
		if kind == "segment":
			entries.append(_segment(extracted, name, note or ""))
			continue
		if kind == "insert":
			light = json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
			if not light["is_bulb_light"] or light["show_bulb_mesh"]:
				raise SystemExit(f"insert light {name} is not a bulb light without a bulb mesh")
			x, y = _point(by_key, "Light", name)
			entries.append({"object": name, "type": "Light", "x": x, "y": y, "projection": note})
			continue
		if kind == "midpoint":
			points = [_point(by_key, *part.split(":")) for part in name.split("|")]
			x = round(sum(p[0] for p in points) / len(points), 6)
			y = round(sum(p[1] for p in points) / len(points), 6)
			entry = {"object": name.replace("|", " + "), "type": "midpoint", "x": x, "y": y}
		else:
			x, y = _point(by_key, kind, name)
			entry = {"object": name, "type": kind, "x": x, "y": y}
		if note:
			entry["projection" if kind not in {"Light", "Flasher"} else "note"] = note
		entries.append(entry)
	return entries


def _check_digits(lamps: dict[str, list[dict]]) -> None:
	"""Each digit's segments must fall in the A-G key, and the digits in DR. 5's two-by-two layout."""
	centres = []
	for digit, addresses in enumerate(DIGITS, start=1):
		points = {letter: (lamps[str(address)][0]["x"], lamps[str(address)][0]["y"]) for letter, address in zip(SEGMENTS, addresses)}
		a, b, c, d, e, f, g = (points[letter] for letter in SEGMENTS)
		columns = max(e[0], f[0]) < min(a[0], g[0], d[0]) and max(a[0], g[0], d[0]) < min(b[0], c[0])
		rows = a[1] < min(b[1], f[1]) and max(b[1], f[1]) < g[1] < min(c[1], e[1]) and max(c[1], e[1]) < d[1]
		if not (columns and rows):
			raise SystemExit(f"7-segment digit {digit} does not match the A-G key")
		centres.append((sum(point[0] for point in points.values()) / 7, sum(point[1] for point in points.values()) / 7))
	top_left, top_right, bottom_left, bottom_right = centres
	if not (top_left[0] < top_right[0] and bottom_left[0] < bottom_right[0] and max(top_left[1], top_right[1]) < min(bottom_left[1], bottom_right[1])):
		raise SystemExit("the four 7-segment digits are not in the two-by-two layout DR. 5 draws")


def _mesh_pieces(obj: Path, names: set[str]) -> dict[str, list[tuple[int, tuple[float, float, float, float], tuple[float, float]]]]:
	"""Connected pieces of the named objects of a world-space OBJ export: vertex count, x/y bounds and z range in VPU."""
	vertices: dict[str, dict[int, tuple[float, float, float]]] = {name: {} for name in names}
	faces: dict[str, list[list[int]]] = {name: [] for name in names}
	count = 0
	current = None
	with obj.open("rb") as stream:
		for line in stream:
			head = line[:2]
			if head == b"o ":
				current = line[2:].strip().decode("utf-8")
			elif head == b"v ":
				if current in names:
					vertices[current][count] = tuple(float(value) for value in line.split()[1:4])
				count += 1
			elif head == b"f " and current in names:
				faces[current].append([int(token.split(b"/")[0]) - 1 for token in line.split()[1:]])
	result = {}
	for name in sorted(names):
		if not vertices[name]:
			raise SystemExit(f"missing mesh object {name} in the OBJ export")
		first_at: dict[tuple[float, ...], int] = {}
		parent = {index: first_at.setdefault(tuple(round(c, 1) for c in point), index) for index, point in vertices[name].items()}

		def find(index: int) -> int:
			while parent[index] != index:
				parent[index] = parent[parent[index]]
				index = parent[index]
			return index

		for face in faces[name]:
			root = find(face[0])
			for index in face[1:]:
				other = find(index)
				if other != root:
					parent[other] = root
		groups: dict[int, list[tuple[float, float, float]]] = {}
		for index, point in vertices[name].items():
			groups.setdefault(find(index), []).append(point)
		pieces = []
		for points in groups.values():
			xs = [point[0] for point in points]
			ys = [point[1] for point in points]
			zs = [point[2] for point in points]
			pieces.append((len(points), (min(xs), min(ys), max(xs), max(ys)), (min(zs), max(zs))))
		result[name] = sorted(pieces, key=lambda piece: (-piece[0], piece[1]))
	return result


def _light_centre(extracted: Path, name: str) -> tuple[float, float]:
	centre = json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]["center"]
	return centre["x"], centre["y"]


def _containing(pieces: list, point: tuple[float, float]) -> list:
	return [piece for piece in pieces if piece[1][0] <= point[0] <= piece[1][2] and piece[1][1] <= point[1] <= piece[1][3]]


def _mesh_record(name: str, piece: tuple, point: tuple[float, float]) -> dict:
	"""One mesh piece under a Light: its x/y centre and distance in VPU, and its height range above the playfield."""
	x0, y0, x1, y1 = piece[1]
	z0, z1 = piece[2]
	centre = ((x0 + x1) / 2, (y0 + y1) / 2)
	return {
		"object": name, "x": round(centre[0], 2), "y": round(centre[1], 2), "distance": round(math.dist(centre, point), 2),
		"height": [round(-z1, 1) + 0.0, round(-z0, 1) + 0.0],
	}


def _anchor(entry: dict, found: list[dict]) -> None:
	"""Place an emitter at the centre of the one piece under its Light that holds the bulb, keeping the Light's own point."""
	anchors = [mesh for mesh in found if mesh["object"] in ANCHOR_OBJECTS]
	if len(anchors) != 1:
		raise SystemExit(f"light {entry['object']} sits on {len(anchors)} bulb-holding pieces")
	entry["mesh"] = found
	entry["anchor"] = anchors[0]["object"]
	entry["light"] = {"x": entry["x"], "y": entry["y"]}
	entry["x"], entry["y"] = _normal(anchors[0]["x"], anchors[0]["y"])


def _meshes(extracted: Path, obj: Path, solenoids: dict[str, list[dict]], lamps: dict[str, list[dict]]) -> tuple[dict, dict]:
	"""Attach each placed flasher and bulb lamp Light's mesh pieces, check the unplaced ones and the export's frame."""
	if hashlib.sha256(obj.read_bytes()).hexdigest() != OBJ_SHA256:
		raise SystemExit("the OBJ export is not the pinned world-space export of the retained table")
	pieces = _mesh_pieces(obj, set(BULB_OBJECTS) | {OBJ_CONTROL[1]})
	bumper = json.loads((extracted / "gameitems" / f"Bumper.{OBJ_CONTROL[0]}.json").read_text(encoding="utf-8"))["Bumper"]["center"]
	x0, y0, x1, y1 = pieces[OBJ_CONTROL[1]][0][1]
	offset = round(math.dist(((x0 + x1) / 2, (y0 + y1) / 2), (bumper["x"], bumper["y"])), 2)
	if offset > 1.0:
		raise SystemExit(f"the OBJ export's {OBJ_CONTROL[1]} lies {offset} VPU from the stored bumper centre")
	for address, objects in FLASHER_MESHES.items():
		for entry in solenoids[str(address)]:
			point = _light_centre(extracted, entry["object"])
			found = []
			for name in objects:
				matches = _containing(pieces[name], point)
				if len(matches) != 1:
					raise SystemExit(f"flasher light {entry['object']} sits on {len(matches)} pieces of {name}")
				found.append(_mesh_record(name, matches[0], point))
			_anchor(entry, found)
	unplaced = {}
	for address, names in UNPLACED_FLASHER_LIGHTS.items():
		for name in names:
			point = _light_centre(extracted, name)
			for mesh in BULB_OBJECTS:
				if _containing(pieces[mesh], point):
					raise SystemExit(f"flasher light {name} sits on a piece of {mesh}")
		unplaced[str(address)] = list(names)
	owners: dict[tuple[str, int], list[int]] = {}
	for address, name in LAMP_MESHES.items():
		(entry,) = lamps[str(address)]
		point = _light_centre(extracted, entry["object"])
		matches = _containing(pieces[name], point)
		if len(matches) != 1:
			raise SystemExit(f"lamp light {entry['object']} sits on {len(matches)} pieces of {name}")
		_anchor(entry, [_mesh_record(name, matches[0], point)])
		owners.setdefault((name, pieces[name].index(matches[0])), []).append(address)
	for name in LAMP_BULB_OBJECTS:
		for index in range(len(pieces[name])):
			if len(owners.get((name, index), [])) != 1:
				raise SystemExit(f"piece {index} of {name} belongs to lamps {owners.get((name, index), [])}")
	for address, entries in lamps.items():
		if int(address) in LAMP_MESHES:
			continue
		for entry in entries:
			if entry["type"] == "Light" and any(_containing(pieces[name], _light_centre(extracted, entry["object"])) for name in LAMP_BULB_OBJECTS):
				raise SystemExit(f"lamp light {entry['object']} sits on a bulb this seed does not record")
	control = {"table_object": f"Bumper {OBJ_CONTROL[0]}", "mesh_object": OBJ_CONTROL[1], "offset": offset}
	return unplaced, control


def _check_assemblies(by_key: dict, solenoids: dict[str, list[dict]], lamps: dict[str, list[dict]]) -> None:
	"""The modelled parts must agree with the assembly drawings the stepper and Tanker sign placements rely on."""
	front = by_key[("Wall", BUG_FRONT)]["y"]
	rear = by_key[("Wall", BUG_REAR)]["y"]
	for entry in solenoids["29"]:
		if not abs(entry["y"] - rear) < abs(entry["y"] - front):
			raise SystemExit(f"warrior bug bulb {entry['object']} is not nearer the rear wall {BUG_REAR}")
	sign = {address: lamps[str(address)][0]["mesh"][0] for address in TANKER_SIGN}
	depths = [mesh["y"] for mesh in sign.values()]
	if max(depths) - min(depths) > 2.0:
		raise SystemExit("the Tanker Bug sign's bulbs do not stand at one depth")
	if not sign[39]["height"][1] < min(sign[35]["height"][0], sign[36]["height"][0]):
		raise SystemExit("the Tanker Bug sign's lamp 39 bulb is not below those of 35 and 36")


def _gi(extracted: Path, by_key: dict) -> list[dict]:
	"""One socket per light of the GILamps collection that UpdateLamps drives as lamp 200 (UpdateGi's G.I. 0)."""
	collections = {item["name"]: item["items"] for item in json.loads((extracted / "collections.json").read_text(encoding="utf-8"))}
	lights = sorted(collections["GILamps"], key=str.casefold)
	groups: list[dict] = []
	for name in lights:
		light = json.loads((extracted / "gameitems" / f"Light.{name}.json").read_text(encoding="utf-8"))["Light"]
		if not light["show_bulb_mesh"]:
			raise SystemExit(f"G.I. light {name} draws no bulb")
		point = _point(by_key, "Light", name)
		for group in groups:
			if math.dist((group["x"], group["y"]), point) < STACK_DISTANCE:
				raise SystemExit(f"G.I. lights {group['object']} and {name} stack on one socket")
		groups.append({"object": name, "x": point[0], "y": point[1]})
	return groups


def build(extracted: Path, vpx: Path, obj: Path) -> dict:
	by_key = _candidates(extracted, vpx)
	solenoids = {str(address): _entries(extracted, by_key, rows) for address, rows in sorted(SOLENOIDS.items())}
	lamps = {str(address): _entries(extracted, by_key, rows) for address, rows in sorted(LAMPS.items())}
	for address, text in LAMP_DRAWINGS.items():
		for entry in lamps[str(address)]:
			entry["drawing"] = text
	_check_digits(lamps)
	unplaced, control = _meshes(extracted, obj, solenoids, lamps)
	_check_assemblies(by_key, solenoids, lamps)
	return {
		"format": "pinmame-starship-troopers-spatial-seed",
		"version": 3,
		"machine_id": "sega.starship-troopers.1997",
		"table": {"sha256": TABLE_SHA256, "width": BOUNDS["right"], "height": BOUNDS["bottom"], "units": "vpx", "obj_sha256": OBJ_SHA256, "obj_control": control},
		"switch": {str(address): _entries(extracted, by_key, rows) for address, rows in sorted(SWITCHES.items())},
		"solenoid": solenoids,
		"unplaced_solenoid_lights": unplaced,
		"lamp": lamps,
		"gi": {"0": _gi(extracted, by_key)},
	}


def canonical(value: dict) -> str:
	return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--extracted", type=Path, required=True)
	parser.add_argument("--vpx", type=Path, required=True)
	parser.add_argument("--obj", type=Path, required=True, help="the retained vpxtool export obj --units vpu export of the table")
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	text = canonical(build(args.extracted, args.vpx, args.obj))
	if args.check:
		if not SEED_PATH.is_file() or SEED_PATH.read_bytes() != text.encode("utf-8"):
			raise SystemExit(f"Starship Troopers spatial seed drift: {SEED_PATH}")
		print("Starship Troopers spatial seed matches the retained extraction.")
		return
	SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
	SEED_PATH.write_bytes(text.encode("utf-8"))
	print(f"Wrote {SEED_PATH}")


if __name__ == "__main__":
	main()
