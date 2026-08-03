"""Promote The Walking Dead Pro with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json

from curate_walking_dead import build_pro


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/the-walking-dead-pro-2014.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-walking-dead-pro-2014.json"

TABLE_SOURCE = "vpx-table.walking-dead-jp-salas-6.0.0-geometry"
SCRIPT_SOURCE = "vpx.walking-dead-pro.jp-salas-v5.5.0"
MANUAL_SOURCE = "manual.walking-dead-pro"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
RUNTIME_SOURCE = "runtime.walking-dead-pro.boot-start"

TABLE_SOURCE_RECORD = {
	"attribution": "JPSalas and the table contributors named by its distribution record",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": False,
	"license": "NOASSERTION",
	"locator": "JP's The Walking Dead (Original 2021) JPSalas 6.0.0.vpx (90,976,256 bytes), extracted with vpxtool git:v0.33.3. The embedded twd_156h controller binding, LE splash text, and LE-only callbacks are rejected for Pro semantics. This source contributes only shared physical geometry individually reconciled against the official Pro location maps and the exact twd_160 sidecar script.",
	"original_filename": "JP's The Walking Dead (Original 2021) JPSalas 6.0.0.vpx",
	"rights": "NOASSERTION",
	"sha256": "859589b1d1ebea3be6e66844c7126d22d42da0877e551c9f7cf90b76e4c30383",
	"uri": "https://archive.org/download/Visual-Pinball-Collection-2025-12-29/tables/JP%27s%20The%20Walking%20Dead%20%28Original%202021%29/JP%27s%20The%20Walking%20Dead%20%28Original%202021%29%20JPSalas%206.0.0.vpx",
}

INPUT_POSITIONS = {
	2: [(0.539910, 0.518354)], 3: [(0.450630, 0.228143)], 4: [(0.450630, 0.242571)],
	9: [(0.086759, 0.583557)], 10: [(0.095741, 0.556016)], 11: [(0.104268, 0.529937)],
	12: [(0.594538, 0.186566)], 13: [(0.593487, 0.237721)],
	18: [(0.672191, 0.924598)], 19: [(0.737551, 0.908247)],
	20: [(0.802287, 0.891896)], 21: [(0.866469, 0.876936)],
	22: [(0.884319, 0.863922)], 23: [(0.943655, 0.887898)],
	24: [(0.043011, 0.790648)], 25: [(0.128386, 0.749584)],
	26: [(0.236274, 0.741789)], 27: [(0.688525, 0.741432)],
	28: [(0.783613, 0.745813)], 29: [(0.860819, 0.785763)],
	30: [(0.649291, 0.383828)], 31: [(0.913734, 0.352931)], 32: [(0.744091, 0.290686)],
	33: [(0.944984, 0.616597)], 34: [(0.825138, 0.470792)], 35: [(0.885488, 0.129484)],
	36: [(0.712167, 0.205698)], 37: [(0.802819, 0.209326)],
	38: [(0.845675, 0.148226)], 39: [(0.951812, 0.159178)],
	41: [(0.065520, 0.138354)], 42: [(0.108721, 0.103877)], 43: [(0.325241, 0.086087)],
	44: [(0.363686, 0.293860)], 45: [(0.538164, 0.294088)],
	46: [(0.450105, 0.263694)], 47: [(0.290310, 0.127603)],
	81: [(0.626436, 0.854824)], 83: [(0.285888, 0.855100)],
}

SOLENOID_POSITIONS = {
	1: [(0.866469, 0.876936)], 2: [(0.943655, 0.985277)],
	3: [(0.393382, 0.238879), (0.506243, 0.238657)],
	4: [(0.393382, 0.238879), (0.506243, 0.238657)],
	7: [(0.450715, 0.345235)],
	9: [(0.649291, 0.383828)], 10: [(0.913734, 0.352931)], 11: [(0.744091, 0.290686)],
	12: [(0.086759, 0.583557), (0.095741, 0.556016), (0.104268, 0.529937)],
	13: [(0.236274, 0.741789)], 14: [(0.688525, 0.741432)],
	15: [(0.285888, 0.855100)], 16: [(0.626436, 0.854824)],
	19: [(0.591856, 0.454272)], 21: [(0.457401, 0.711049)],
	25: [(0.776851, 0.383284)], 26: [(0.449980, 0.160784)],
	27: [(0.394787, 0.176880), (0.505172, 0.176880)],
	28: [(0.058018, 0.554814)], 29: [(0.850009, 0.539255)],
	31: [(0.061276, 0.344259)],
	# The LE-bound table's f32 object coincides with lamp 58 and is not valid Pro
	# geometry. This position is read from the model-specific Pro coil map.
	32: [(0.285000, 0.213000)],
}

LAMP_POSITIONS = {
	3: [(0.364352, 0.467202)], 4: [(0.455414, 0.904621)],
	5: [(0.382066, 0.832636)], 6: [(0.428600, 0.842436)], 7: [(0.482149, 0.842254)],
	8: [(0.528765, 0.832057)], 9: [(0.552927, 0.804162)], 10: [(0.456258, 0.816610)],
	11: [(0.358431, 0.804820)], 12: [(0.407307, 0.795822)], 13: [(0.456126, 0.787469)],
	14: [(0.504630, 0.795402)], 15: [(0.313263, 0.754446)], 16: [(0.371018, 0.753775)],
	17: [(0.427336, 0.753607)], 18: [(0.484318, 0.753605)], 19: [(0.541026, 0.753493)],
	20: [(0.597469, 0.753717)], 21: [(0.457660, 0.710825)], 22: [(0.041711, 0.729619)],
	23: [(0.128688, 0.682943)], 24: [(0.733822, 0.449101)], 25: [(0.282018, 0.639716)],
	26: [(0.168005, 0.624664)], 27: [(0.232984, 0.606179)], 28: [(0.233682, 0.563530)],
	29: [(0.322704, 0.571265)], 30: [(0.170781, 0.507879)], 31: [(0.154631, 0.484039)],
	32: [(0.129031, 0.444197)], 33: [(0.094602, 0.395751)], 34: [(0.309006, 0.547952)],
	35: [(0.286749, 0.507566)], 36: [(0.256814, 0.458869)], 37: [(0.855798, 0.727199)],
	38: [(0.781347, 0.681310)], 39: [(0.666060, 0.691707)], 40: [(0.703779, 0.667870)],
	41: [(0.695776, 0.592856)], 42: [(0.556969, 0.695825)], 43: [(0.586104, 0.674095)],
	44: [(0.633694, 0.637838)], 45: [(0.437207, 0.646359)], 46: [(0.408926, 0.602623)],
	47: [(0.440176, 0.614176)], 48: [(0.482376, 0.619653)], 49: [(0.523632, 0.618554)],
	50: [(0.492029, 0.578509)], 51: [(0.630271, 0.558494)], 52: [(0.652508, 0.535973)],
	53: [(0.686538, 0.497111)], 54: [(0.444097, 0.426187)], 55: [(0.536820, 0.320798)],
	56: [(0.358629, 0.320689)], 57: [(0.267582, 0.215994)], 58: [(0.288535, 0.270378)],
	59: [(0.306900, 0.314606)], 60: [(0.744102, 0.290600)], 61: [(0.913220, 0.353071)],
	62: [(0.649564, 0.384081)], 63: [(0.315314, 0.339357)], 64: [(0.355837, 0.375307)],
	65: [(0.386624, 0.387186)], 66: [(0.424712, 0.394111)], 67: [(0.468871, 0.394225)],
	68: [(0.508880, 0.387543)], 69: [(0.538575, 0.375424)], 70: [(0.786155, 0.477078)],
	71: [(0.834821, 0.482945)], 72: [(0.686944, 0.128603)], 73: [(0.713895, 0.094957)],
	74: [(0.807265, 0.094957)], 75: [(0.896901, 0.094957)], 76: [(0.716178, 0.158095)],
	77: [(0.802658, 0.161255)], 78: [(0.117881, 0.242934)], 79: [(0.590659, 0.238929)],
	80: [(0.591285, 0.187971)],
}

# Official Pro manual PDF page 38 / printed page 36 explicitly maps 28 white
# playfield bayonets and five white back-panel bayonets. The five back-panel
# service-side socket positions are reflected into player view, normalized
# within the panel drawing, and projected across the full canonical rear edge
# at y=0. That full-width projection is an explicit authoring assumption.
GI_PLAYFIELD_POSITIONS = [
	# B circuit (nine bayonets), rear to front.
	(0.910394, 0.025354), (0.067384, 0.048074), (0.188889, 0.073922),
	(0.941219, 0.121172), (0.334050, 0.129404), (0.224731, 0.141258),
	(0.695341, 0.164965), (0.778495, 0.163319), (0.876344, 0.174185),
	# V circuit (eleven bayonets), right and centre lanes.
	(0.987097, 0.279223), (0.959498, 0.377840), (0.641219, 0.408792),
	(0.933692, 0.502140), (0.909677, 0.547909), (0.930824, 0.607673),
	(0.910394, 0.670234), (0.758423, 0.767369), (0.726165, 0.811821),
	(0.796774, 0.863846), (0.727240, 0.889035),
	# Y circuit (eight bayonets), left and lower lanes.
	(0.098925, 0.485677), (0.041577, 0.495884), (0.043369, 0.550379),
	(0.058423, 0.655746), (0.200717, 0.773461), (0.228315, 0.810175),
	(0.163799, 0.858742), (0.233692, 0.886730),
]
GI_BACK_PANEL_POSITIONS = [
	# Player-view left to right after reflecting the service/rear-face drawing.
	(0.415800, 0.000000), (0.480000, 0.000000), (0.546400, 0.000000),
	(0.771000, 0.000000), (0.967900, 0.000000),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "cabinet.flipper", 84: "cabinet.flipper",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], source_refs: tuple[str, ...]) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{device['id']}.{role}{suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed spatial disposition to every physical input and output."""
	if len(GI_PLAYFIELD_POSITIONS) != 28 or len(GI_BACK_PANEL_POSITIONS) != 5:
		raise ValueError("Walking Dead Pro GI map must contain 28 playfield and five back-panel emitters")
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], (TABLE_SOURCE,))
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Walking Dead Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			coordinate_sources = (MANUAL_SOURCE,) if address == 32 else (TABLE_SOURCE,)
			_located(device, role, SOLENOID_POSITIONS[address], coordinate_sources)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = len(SOLENOID_POSITIONS[address])
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], (TABLE_SOURCE,))
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.gi" and address == 0:
			placements = [*GI_PLAYFIELD_POSITIONS, *GI_BACK_PANEL_POSITIONS]
			_located(device, "emitter", placements, (MANUAL_SOURCE,))
			device.setdefault("physical", {})["quantity"] = len(placements)
		else:
			raise ValueError(f"Walking Dead Pro output {group} {address} ({kind}) has no reviewed spatial disposition")


def promote() -> None:
	definition = build_pro()
	if not any(existing["id"] == TABLE_SOURCE for existing in definition["sources"]):
		definition["sources"].append(TABLE_SOURCE_RECORD)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
