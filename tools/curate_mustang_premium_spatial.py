"""Promote Mustang Premium / Limited Edition / Boss with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text

from curate_mustang import CORE_SOURCE, PREMIUM_KNOWLEDGE, PREMIUM_MANUAL, VPX_SOURCE, build_premium


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/mustang-premium-limited-edition-boss-2014.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/mustang-premium-limited-edition-boss-2014.json"

TABLE_SOURCE = "vpx-table.mustang-premium-le-vpw-1.27-geometry"
TABLE_SOURCE_RECORD = {
	"attribution": "VPW and the table authors credited by the table distribution",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "Mustang (Stern 2014) v1.27.vpx (192,118,784 bytes), exact mt_145h table extracted with vpxtool git:v0.33.3. Coordinates are accepted only where the table geometry and working script reconcile with the official service-manual maps. Visual light pools, field proxies, apron helpers, and backglass effects are excluded from physical counts.",
	"original_filename": "Mustang (Stern 2014) v1.27.vpx",
	"rights": "NOASSERTION",
	"sha256": "f3f5e24665cf8bc0231f16e9cb28eed7c2cc1ff265d9c7e3cf93bf8589fe59e1",
	"uri": "external:pinmame-vpx-sources/stern/mustang-premium-limited-edition-boss-2014/source/Mustang (Stern 2014) v1.27.vpx",
}

INPUT_POSITIONS = {
	1: [(0.836685, 0.552217)], 2: [(0.828638, 0.526752)], 3: [(0.820205, 0.501777)],
	4: [(0.804928, 0.312827)], 5: [(0.235154, 0.299079)], 8: [(0.764629, 0.175000)],
	9: [(0.782132, 0.256613)], 10: [(0.720481, 0.087355)], 11: [(0.611576, 0.110183)],
	12: [(0.542581, 0.112465)], 13: [(0.395129, 0.113689)], 14: [(0.325612, 0.112671)],
	24: [(0.064263, 0.774106)], 25: [(0.133074, 0.772377)], 26: [(0.233761, 0.758179)],
	27: [(0.669622, 0.755202)], 28: [(0.771882, 0.776815)], 29: [(0.842091, 0.777743)],
	30: [(0.262323, 0.243660)], 31: [(0.663674, 0.236336)], 32: [(0.449914, 0.297830)],
	33: [(0.462082, 0.203375)], 34: [(0.313860, 0.363567)], 35: [(0.372892, 0.368395)],
	36: [(0.432750, 0.373100)], 37: [(0.492195, 0.377867)], 38: [(0.550815, 0.382450)],
	39: [(0.268548, 0.149072)], 40: [(0.341693, 0.028422)], 41: [(0.369455, 0.359333)],
	42: [(0.502422, 0.369310)], 43: [(0.650206, 0.307576)], 44: [(0.830160, 0.034438)],
	45: [(0.207834, 0.047032)], 46: [(0.610495, 0.786830)], 47: [(0.939916, 0.916821)],
	48: [(0.815388, 0.396026)], 49: [(0.118001, 0.231297)], 50: [(0.074407, 0.144520)],
	52: [(0.466488, 0.233822)], 53: [(0.466488, 0.233822)], 54: [(0.053334, 0.366417)],
	55: [(0.141769, 0.458824)], 56: [(0.737245, 0.421137)], 57: [(0.180933, 0.547827)],
	81: [(0.618600, 0.878654)], 83: [(0.276385, 0.878654)],
}

# The manual establishes six physical trough-position sensors plus the jam opto,
# while the VPW stack shortcut instantiates only switches 18-23. These projected
# centers preserve the manual's left-to-right physical ordering within the exact
# trough region; they are deliberately not attributed to the eject-kicker center.
TROUGH_POSITIONS = {
	17: [(0.525000, 0.930000)], 18: [(0.580000, 0.930000)], 19: [(0.635000, 0.930000)],
	20: [(0.690000, 0.930000)], 21: [(0.745000, 0.930000)], 22: [(0.800000, 0.930000)],
	23: [(0.855000, 0.900000)],
}

SOLENOID_POSITIONS = {
	1: [(0.833856, 0.878915)], 2: [(0.941842, 0.985262)],
	3: [(0.118001, 0.231297)], 4: [(0.118001, 0.231297)],
	5: [(0.074407, 0.144520)], 6: [(0.074407, 0.144520)],
	7: [(0.432750, 0.373100)], 9: [(0.262323, 0.243660)],
	10: [(0.663674, 0.236336)], 11: [(0.449914, 0.297830)], 12: [(0.462082, 0.203375)],
	13: [(0.233761, 0.758179)], 14: [(0.669622, 0.755202)],
	15: [(0.276385, 0.878654)], 16: [(0.618600, 0.878654)],
	17: [(0.167610, 0.343172)], 18: [(0.906869, 0.234729)],
	19: [(0.132415, 0.782087)], 20: [(0.879799, 0.815076)],
	21: [(0.069490, 0.082959)], 22: [(0.466488, 0.233822)],
	23: [(0.920713, 0.070765)], 25: [(0.521691, 0.248550)],
	26: [(0.403259, 0.248778)], 27: [(0.636909, 0.384933)],
	28: [(0.788056, 0.149137)], 29: [(0.734669, 0.023781)], 30: [(0.468571, 0.291221)],
	51: [(0.272378, 0.044101)], 52: [(0.651646, 0.039562)],
	53: [(0.737245, 0.421137)], 54: [(0.737245, 0.421137)],
	55: [(0.180933, 0.547827)], 56: [(0.180933, 0.547827)],
	59: [(0.650206, 0.307576)], 60: [(0.070417, 0.351844)],
}

LAMP_POSITIONS = {
	9: [(0.842557, 0.019509)], 10: [(0.725087, 0.020102)], 11: [(0.608298, 0.020059)],
	12: [(0.503221, 0.018409)], 13: [(0.397579, 0.018959)], 14: [(0.281591, 0.019387)],
	15: [(0.161212, 0.019344)], 16: [(0.611746, 0.063533)], 17: [(0.534775, 0.064143)],
	18: [(0.416569, 0.064143)], 19: [(0.339139, 0.063940)],
	20: [(0.338933, 0.040579)], 21: [(0.415652, 0.040338)],
	22: [(0.532484, 0.040134)], 23: [(0.609914, 0.040134)],
	24: [(0.244837, 0.325160)], 25: [(0.831243, 0.364559)], 26: [(0.850062, 0.323676)],
	27: [(0.867988, 0.296833)], 28: [(0.887164, 0.266853)], 29: [(0.629833, 0.438921)],
	30: [(0.719248, 0.453087)], 31: [(0.739289, 0.335933)], 32: [(0.793429, 0.337082)],
	33: [(0.772868, 0.500793)], 34: [(0.781238, 0.525905)], 35: [(0.790053, 0.551971)],
	36: [(0.774033, 0.696789)], 37: [(0.858428, 0.700146)], 38: [(0.855677, 0.731742)],
	39: [(0.061510, 0.701895)], 40: [(0.134537, 0.696006)], 41: [(0.060426, 0.731720)],
	42: [(0.095873, 0.484049)], 43: [(0.079655, 0.450638)], 44: [(0.183124, 0.380354)],
	45: [(0.194592, 0.409844)], 46: [(0.205810, 0.436705)], 47: [(0.214869, 0.473956)],
	48: [(0.153741, 0.483673)], 49: [(0.197483, 0.577387)], 50: [(0.451420, 0.782442)],
	51: [(0.456374, 0.739269)], 52: [(0.335684, 0.694258)], 53: [(0.456897, 0.694258)],
	54: [(0.580605, 0.694026)], 55: [(0.334117, 0.653654)], 56: [(0.458348, 0.653654)],
	57: [(0.582695, 0.653422)], 58: [(0.291616, 0.580641)], 59: [(0.313741, 0.542375)],
	60: [(0.373123, 0.512738)], 61: [(0.455932, 0.500608)], 62: [(0.540224, 0.511091)],
	63: [(0.601957, 0.541272)], 64: [(0.624524, 0.581260)], 65: [(0.393156, 0.554118)],
	66: [(0.456046, 0.554118)], 67: [(0.519465, 0.553414)], 68: [(0.394741, 0.605986)],
	69: [(0.457632, 0.605751)], 70: [(0.522107, 0.605516)], 73: [(0.453216, 0.916045)],
	77: [(0.462290, 0.203104)], 78: [(0.263320, 0.245260)],
	79: [(0.461871, 0.316110)], 80: [(0.670986, 0.236473)],
	81: [(0.316006, 0.466929)], 82: [(0.322100, 0.452729)], 83: [(0.328518, 0.438932)],
	84: [(0.334924, 0.424851)], 85: [(0.341272, 0.411038)], 86: [(0.389014, 0.471703)],
	87: [(0.395408, 0.457905)], 88: [(0.401271, 0.444087)], 89: [(0.407920, 0.430145)],
	90: [(0.413990, 0.415936)], 91: [(0.460839, 0.476621)], 92: [(0.467612, 0.463026)],
	93: [(0.473806, 0.449252)], 94: [(0.480401, 0.435578)], 95: [(0.485839, 0.421883)],
	96: [(0.486310, 0.396448)], 97: [(0.359886, 0.386286)],
	98: [(0.252871, 0.360933)], 99: [(0.230625, 0.517550)],
	100: [(0.169973, 0.519980)], 101: [(0.117915, 0.527237)],
	102: [(0.697224, 0.308996)], 103: [(0.644649, 0.305105)],
	104: [(0.586405, 0.300756)], 105: [(0.193478, 0.215226)],
	106: [(0.190726, 0.203738)], 107: [(0.075689, 0.290022)],
	108: [(0.069084, 0.279756)], 109: [(0.872624, 0.248471)],
	110: [(0.817174, 0.245285)], 111: [(0.766807, 0.242388)],
	112: [(0.454044, 0.881265)],
	113: [(0.770042, 0.371966)], 114: [(0.710996, 0.383600)],
	115: [(0.802107, 0.407217)], 116: [(0.618517, 0.484535)],
	117: [(0.252871, 0.360933)], 118: [(0.252871, 0.360933)], 119: [(0.252871, 0.360933)],
	120: [(0.230625, 0.517550)], 121: [(0.230625, 0.517550)], 122: [(0.230625, 0.517550)],
	123: [(0.169973, 0.519980)], 124: [(0.169973, 0.519980)], 125: [(0.169973, 0.519980)],
	126: [(0.117915, 0.527237)], 127: [(0.117915, 0.527237)], 128: [(0.117915, 0.527237)],
	130: [(0.770042, 0.371966)], 131: [(0.770042, 0.371966)], 132: [(0.770042, 0.371966)],
	133: [(0.710996, 0.383600)], 134: [(0.710996, 0.383600)], 135: [(0.710996, 0.383600)],
	136: [(0.802107, 0.407217)], 137: [(0.802107, 0.407217)], 138: [(0.802107, 0.407217)],
	139: [(0.618517, 0.484535)], 140: [(0.618517, 0.484535)], 141: [(0.618517, 0.484535)],
}

# The official lighting drawing has 25 genuine playfield GI callouts: seven on
# GI-3, ten on GI-1 (including two separately marked spot assemblies), and eight
# on GI-0. Its printed inventory reconciles as 15 wedge lamps (GI-3 plus eight
# non-spot GI-1), eight GI-0 bayonets, two separate GI-1 spots, and seven red
# GI-2 rear bayonets. Playfield points are calibrated drawing projections; the
# rear red row additionally reconciles to exact VPW object centers.
GI_POSITIONS: list[tuple[str, float, float]] = [
	("rear-red.gi2.01", 0.022466, 0.007657),
	("rear-red.gi2.02", 0.167363, 0.007657),
	("rear-red.gi2.03", 0.328980, 0.005800),
	("rear-red.gi2.04", 0.490596, 0.005800),
	("rear-red.gi2.05", 0.660571, 0.005800),
	("rear-red.gi2.06", 0.822187, 0.006419),
	("rear-red.gi2.07", 0.974051, 0.006419),
	("wedge.gi3.01", 0.881538, 0.099608),
	("wedge.gi3.02", 0.542308, 0.117647),
	("wedge.gi3.03", 0.945385, 0.123529),
	("wedge.gi3.04", 0.226154, 0.145098),
	("wedge.gi3.05", 0.320769, 0.165098),
	("wedge.gi3.06", 0.955385, 0.222745),
	("wedge.gi3.07", 0.290000, 0.228627),
	("wedge.gi1.01", 0.483077, 0.375686),
	("wedge.gi1.02", 0.564615, 0.381176),
	("wedge.gi1.03", 0.197692, 0.439608),
	("wedge.gi1.04", 0.944615, 0.469020),
	("wedge.gi1.05", 0.948462, 0.570588),
	("wedge.gi1.06", 0.146923, 0.589412),
	("wedge.gi1.07", 0.140769, 0.666275),
	("wedge.gi1.08", 0.950769, 0.667059),
	("bayonet.spot-gi1.left", 0.255385, 0.476863),
	("bayonet.spot-gi1.right", 0.850000, 0.520392),
	("bayonet.gi0.01", 0.279231, 0.835294),
	("bayonet.gi0.02", 0.735385, 0.836078),
	("bayonet.gi0.03", 0.326923, 0.881961),
	("bayonet.gi0.04", 0.783077, 0.883137),
	("bayonet.gi0.05", 0.236154, 0.931765),
	("bayonet.gi0.06", 0.854615, 0.929412),
	("bayonet.gi0.07", 0.315385, 0.954118),
	("bayonet.gi0.08", 0.785385, 0.954902),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right",
	68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 71: "cabinet.action",
	82: "cabinet.flipper", 84: "cabinet.flipper",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.solenoid", 31): "cabinet.speaker-panel",
	("pinmame.output.solenoid", 32): "cabinet.speaker-panel",
	("pinmame.output.solenoid", 61): "cabinet.backbox",
	("pinmame.output.solenoid", 62): "cabinet.backbox",
	("pinmame.output.solenoid", 63): "cabinet.backbox",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
	("pinmame.output.lamp", 129): "cabinet.action",
	("pinmame.output.lamp", 142): "cabinet.action",
	("pinmame.output.lamp", 143): "cabinet.action",
	("pinmame.output.lamp", 144): "cabinet.action",
}

MANUAL_PROJECTED_INPUTS = {9, 17, 18, 19, 20, 21, 22, 23, 49, 50, 52, 53, 81, 83}
MANUAL_PROJECTED_LAMPS = {98, 99, 100, 101, 113, 114, 115, 116}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(
	device: dict[str, object],
	role: str,
	positions: list[tuple[float, float]] | list[tuple[str, float, float]],
	source_refs: tuple[str, ...],
) -> None:
	placements = []
	for index, position in enumerate(positions, start=1):
		if len(position) == 3:
			suffix, x, y = position
			placement_suffix = f".{suffix}"
		else:
			x, y = position
			placement_suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{device['id']}.{role}{placement_suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def _located_gi(device: dict[str, object]) -> None:
	placements = []
	for suffix, x, y in GI_POSITIONS:
		source_refs = (PREMIUM_MANUAL, TABLE_SOURCE) if suffix.startswith("rear-red") else (PREMIUM_MANUAL,)
		placements.append({
			"id": f"{device['id']}.emitter.{suffix}",
			"role": "emitter",
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": _provenance(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}
	_append_note(device, "The seven rear red GI-2 bayonet centers reconcile the manual row with exact VPW geometry. The 25 playfield centers are calibrated projections of the manual's seven GI-3, ten GI-1, and eight GI-0 callouts, with practical uncertainty of about plus or minus 0.04 normalized x and 0.03 y; they are not inferred from the VPW GI_ALL render collection. Physical GI-0 through GI-3 share one PinMAME transport channel.")


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed spatial disposition to every physical input and output."""
	if len(GI_POSITIONS) != 32:
		raise ValueError("Mustang Premium GI map must contain exactly 32 physical placements")
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PREMIUM_MANUAL)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PREMIUM_MANUAL)
		elif address in TROUGH_POSITIONS:
			_located(device, "sensor", TROUGH_POSITIONS[address], (PREMIUM_MANUAL,))
			_append_note(device, "The manual proves six trough positions plus the jam opto but prints only an assembly-level callout. This center is a calibrated projection within that trough region, with practical uncertainty of about plus or minus 0.03 normalized x and 0.02 y; the working VPW shortcut initializes only switches 18-23 and must not erase physical switch 17.")
		elif address in INPUT_POSITIONS:
			sources = (PREMIUM_MANUAL, TABLE_SOURCE) if address in MANUAL_PROJECTED_INPUTS else (TABLE_SOURCE,)
			_located(device, "sensor", INPUT_POSITIONS[address], sources)
			if address == 9:
				_append_note(device, "No independent sw9 object exists; this manual-established captive-ball front/rest switch is projected to the exact RCaptKicker1a assembly anchor. Practical uncertainty is about plus or minus 0.02 normalized x and y.")
			elif address in {49, 50}:
				_append_note(device, "The manual establishes this physical ramp-down sensor, while the working VPW omits or synthesizes its state. The coordinate is the exact corresponding ramp-assembly centroid, not a claimed sensor-object center; practical uncertainty is about plus or minus 0.03 normalized x and y.")
			elif address in {52, 53}:
				_append_note(device, "Both channels are physical optos on one car/turntable assembly and intentionally share its exact center; they are not separate turntables.")
			elif address in {81, 83}:
				_append_note(device, "The EOS contact is implicit in the exact VPW flipper assembly, so the flipper center is an assembly projection with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PREMIUM_MANUAL)
		else:
			raise ValueError(f"Mustang Premium input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PREMIUM_MANUAL)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "cabinet_or_service", PREMIUM_MANUAL)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], (TABLE_SOURCE,))
			device.setdefault("physical", {}).setdefault("quantity", 1)
			if address in {3, 4}:
				_append_note(device, "Outputs 3 and 4 are the power and hold windings of one physical mid-ramp actuator and intentionally share one assembly anchor.")
			elif address in {5, 6}:
				_append_note(device, "Outputs 5 and 6 are the power and hold windings of one physical upper-ramp actuator and intentionally share one assembly anchor.")
			elif address in {53, 54, 55, 56}:
				_append_note(device, "The up/down windings for this single drop-target assembly intentionally share one target anchor.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			sources = (PREMIUM_MANUAL, TABLE_SOURCE) if address in MANUAL_PROJECTED_LAMPS else (TABLE_SOURCE,)
			_located(device, "emitter", LAMP_POSITIONS[address], sources)
			physical = device.setdefault("physical", {})
			physical.setdefault("quantity", 1)
			if address in MANUAL_PROJECTED_LAMPS:
				_append_note(device, "The manual proves this white arrow channel, while the working VPW has no trustworthy standalone white-emitter object here. The coordinate is projected to the corresponding exact RGB module anchor, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			if 117 <= address <= 128 or 130 <= address <= 141:
				_append_note(device, "This controller channel is one color of a single physical RGB module; all three channel records intentionally share one emitter center and must not be recreated as three separate modules.")
		elif group == "pinmame.output.gi" and address == 0:
			_located_gi(device)
		else:
			raise ValueError(f"Mustang Premium output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Mustang Premium knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PREMIUM_KNOWLEDGE,
	"Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**",
	"Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, recreation behavior, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nEvery physical playfield input, actuator, lamp, and GI socket has a normalized player-view placement: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. Exact object centers come from the known-working VPW table only after script/manual reconciliation. The seven trough contacts, ramp-position sensors, implicit EOS contacts, white-arrow companions, and 25 playfield GI callouts use explicitly disclosed assembly or drawing projections with practical uncertainty; cabinet, service, speaker-panel, backbox, virtual, unpopulated, and DIP devices are explicitly outside playfield space.\n\nThe official lighting drawing proves 32 physical GI emitters across four physical circuits behind one PinMAME transport channel: seven GI-3 and eight non-spot GI-1 wedge lamps, two separately called-out GI-1 spot assemblies, eight GI-0 bayonet lamps, and seven red GI-2 rear bayonet lamps. The seven rear red centers additionally reconcile to exact VPW geometry. The VPW `GI_ALL` collection contains 52 render lights and broad GI field helpers; those are excluded from the physical count. Public lamp 98 remains manual white-arrow diagnostic 109 even though the table also uses that state as a render trigger for `GI_ALL`.\n\nThe service manual proves trough switches 17-22 plus jam 23, but provides only one assembly callout. Their seven distinct points are calibrated projections within that region and preserve physical ordering. The proven VPW shortcut initializes 18-23 and omits physical 17; this is retained as a runtime discrepancy, not promoted into a false hardware inventory.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `vpx.mustang-premium-le-vpw-1.27`:",
	"- `vpx-table.mustang-premium-le-vpw-1.27-geometry`: exact known-working table `Mustang (Stern 2014) v1.27.vpx`, 192,118,784 bytes, SHA-256 `f3f5e24665cf8bc0231f16e9cb28eed7c2cc1ff265d9c7e3cf93bf8589fe59e1`; retained externally under `pinmame-vpx-sources/stern/mustang-premium-limited-edition-boss-2014/source`.\n- `vpx.mustang-premium-le-vpw-1.27`:",
)


def promote() -> None:
	definition = build_premium()
	if not any(source["id"] == TABLE_SOURCE for source in definition["sources"]):
		definition["sources"].append(TABLE_SOURCE_RECORD)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/mustang-premium-limited-edition-boss-2014.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
