"""Promote Mustang Pro with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text

from curate_mustang import CORE_SOURCE, PRO_KNOWLEDGE, PRO_MANUAL, PRO_VPX_SOURCE, PRO_VPX_TABLE_SOURCE, build_pro


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/mustang-pro-2014.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/mustang-pro-2014.json"

INPUT_POSITIONS = {
	1: [(0.836685, 0.552217)], 2: [(0.828638, 0.526752)], 3: [(0.820205, 0.501777)],
	4: [(0.804928, 0.312827)], 5: [(0.235154, 0.299079)], 8: [(0.764629, 0.175000)],
	9: [(0.782132, 0.256613)], 10: [(0.720481, 0.087355)], 11: [(0.618077, 0.108121)],
	12: [(0.542581, 0.112877)], 13: [(0.394201, 0.113689)], 14: [(0.326541, 0.111021)],
	24: [(0.064263, 0.775058)], 25: [(0.137409, 0.773202)], 26: [(0.233708, 0.758108)],
	27: [(0.669563, 0.755606)], 28: [(0.774817, 0.778770)], 29: [(0.847962, 0.779698)],
	30: [(0.264956, 0.243853)], 31: [(0.668691, 0.235303)], 32: [(0.460358, 0.317403)],
	33: [(0.463327, 0.203513)], 34: [(0.314517, 0.364145)], 35: [(0.372511, 0.368554)],
	36: [(0.432072, 0.372962)], 37: [(0.492156, 0.377602)], 38: [(0.551195, 0.382243)],
	39: [(0.268548, 0.149072)], 40: [(0.341693, 0.028422)], 41: [(0.369455, 0.359333)],
	42: [(0.502422, 0.369310)], 43: [(0.650078, 0.310441)], 44: [(0.931557, 0.090603)],
	45: [(0.063741, 0.098724)], 46: [(0.679728, 0.774362)], 47: [(0.939916, 0.916821)],
	48: [(0.815388, 0.396026)], 54: [(0.053334, 0.366417)], 55: [(0.141769, 0.458824)],
	81: [(0.618600, 0.877262)], 83: [(0.276385, 0.878654)],
}

# The drawing has one assembly-level callout for switches 17-23. These calibrated
# projections preserve the six physical ball positions and the jam opto in order.
TROUGH_POSITIONS = {
	17: [(0.525000, 0.930000)], 18: [(0.580000, 0.930000)], 19: [(0.635000, 0.930000)],
	20: [(0.690000, 0.930000)], 21: [(0.745000, 0.930000)], 22: [(0.800000, 0.930000)],
	23: [(0.855000, 0.900000)],
}

SOLENOID_POSITIONS = {
	1: [(0.833856, 0.878915)], 2: [(0.941484, 0.995070)],
	3: [(0.096264, 0.191111)], 4: [(0.096264, 0.191111)],
	5: [(0.063349, 0.124985)], 6: [(0.063349, 0.124985)],
	7: [(0.432072, 0.372962)], 9: [(0.264956, 0.243853)],
	10: [(0.668691, 0.235303)], 11: [(0.460358, 0.317403)], 12: [(0.463327, 0.203513)],
	13: [(0.233708, 0.758108)], 14: [(0.669563, 0.755606)],
	15: [(0.276385, 0.878654)], 16: [(0.618600, 0.877262)],
	17: [(0.168691, 0.343670)], 18: [(0.909026, 0.232765)],
	19: [(0.142633, 0.784687)], 20: [(0.878265, 0.810673)],
	21: [(0.069490, 0.082959)], 23: [(0.920713, 0.070765)],
	25: [(0.524295, 0.248550)], 26: [(0.404127, 0.247622)],
	27: [(0.637866, 0.384970)], 28: [(0.790491, 0.160093)], 29: [(0.739028, 0.039269)],
	31: [(0.471787, 0.030626)], 32: [(0.650078, 0.310441)],
}

LAMP_POSITIONS = {
	4: [(0.062435, 0.732077)], 5: [(0.061912, 0.701914)], 6: [(0.139760, 0.695650)],
	7: [(0.774033, 0.696578)], 8: [(0.861285, 0.698666)], 9: [(0.857106, 0.730684)],
	10: [(0.456374, 0.739269)], 11: [(0.456897, 0.783121)], 12: [(0.335684, 0.694258)],
	13: [(0.459509, 0.916299)], 14: [(0.456897, 0.694258)], 15: [(0.579676, 0.694026)],
	16: [(0.334117, 0.653654)], 17: [(0.457419, 0.653654)], 18: [(0.581766, 0.653422)],
	19: [(0.394723, 0.607019)], 20: [(0.460031, 0.606323)], 21: [(0.393156, 0.554118)],
	22: [(0.456897, 0.554350)], 23: [(0.520637, 0.552726)], 24: [(0.625131, 0.579872)],
	25: [(0.603187, 0.540661)], 26: [(0.460031, 0.606323)], 27: [(0.540491, 0.509571)],
	28: [(0.458986, 0.499826)], 29: [(0.373824, 0.511659)], 30: [(0.313741, 0.541357)],
	31: [(0.292842, 0.579408)], 32: [(0.116967, 0.527429)], 33: [(0.170781, 0.521861)],
	34: [(0.524817, 0.606555)], 35: [(0.216562, 0.473956)], 36: [(0.155434, 0.484049)],
	37: [(0.095873, 0.484049)], 38: [(0.079154, 0.450638)], 39: [(0.206635, 0.435789)],
	40: [(0.195664, 0.408179)], 41: [(0.183124, 0.379640)], 42: [(0.524817, 0.606555)],
	45: [(0.616967, 0.486130)], 46: [(0.739289, 0.336137)], 47: [(0.772466, 0.500058)],
	48: [(0.781870, 0.526044)], 49: [(0.789185, 0.550638)], 50: [(0.629833, 0.438921)],
	51: [(0.800353, 0.409099)], 52: [(0.769005, 0.373833)], 53: [(0.831243, 0.364559)],
	54: [(0.793887, 0.336485)], 55: [(0.851358, 0.323492)], 56: [(0.869122, 0.297042)],
	57: [(0.887931, 0.268503)], 58: [(0.231387, 0.519772)], 59: [(0.710488, 0.383345)],
	60: [(0.253853, 0.361768)], 61: [(0.245820, 0.324420)], 62: [(0.339864, 0.063167)],
	63: [(0.420324, 0.062935)], 64: [(0.528997, 0.063399)], 65: [(0.613114, 0.063631)],
	66: [(0.153605, 0.009919)], 67: [(0.282132, 0.009919)], 68: [(0.388715, 0.009919)],
	69: [(0.501045, 0.009919)], 70: [(0.607628, 0.009919)], 71: [(0.726750, 0.009919)],
	72: [(0.857889, 0.009919)], 73: [(0.338297, 0.039965)], 74: [(0.419801, 0.039733)],
	75: [(0.528997, 0.039733)], 76: [(0.612069, 0.039733)], 77: [(0.462905, 0.204466)],
	78: [(0.264368, 0.245766)], 79: [(0.461860, 0.316299)], 80: [(0.668757, 0.237877)],
	81: [(0.316092, 0.466995)], 82: [(0.322623, 0.452726)], 83: [(0.328892, 0.438805)],
	84: [(0.334639, 0.424536)], 85: [(0.340387, 0.410963)], 86: [(0.388454, 0.471868)],
	87: [(0.394723, 0.458063)], 88: [(0.400209, 0.443910)], 89: [(0.408046, 0.429988)],
	90: [(0.414054, 0.415719)], 91: [(0.460293, 0.476856)], 92: [(0.466562, 0.462819)],
	93: [(0.473093, 0.449362)], 94: [(0.478318, 0.435557)], 95: [(0.486416, 0.421868)],
	96: [(0.486938, 0.395534)], 97: [(0.359457, 0.385905)],
	102: [(0.697224, 0.308996)], 103: [(0.644649, 0.305105)], 104: [(0.586405, 0.300756)],
	105: [(0.193478, 0.215226)], 106: [(0.190726, 0.203738)], 107: [(0.075689, 0.290022)],
	108: [(0.069084, 0.279756)], 109: [(0.872624, 0.248471)], 110: [(0.817174, 0.245285)],
	111: [(0.766807, 0.242388)], 112: [(0.454807, 0.881265)],
}

# The Pro manual independently establishes the same 32-socket inventory shown by
# its lighting diagram: 15 wedge lamps, eight bayonet lamps, two spot assemblies,
# and seven rear red bayonet lamps. All four physical circuits share GI address 0.
GI_POSITIONS: list[tuple[str, float, float]] = [
	("rear-red.gi2.01", 0.022466, 0.007657), ("rear-red.gi2.02", 0.167363, 0.007657),
	("rear-red.gi2.03", 0.328980, 0.005800), ("rear-red.gi2.04", 0.490596, 0.005800),
	("rear-red.gi2.05", 0.660571, 0.005800), ("rear-red.gi2.06", 0.822187, 0.006419),
	("rear-red.gi2.07", 0.974051, 0.006419),
	("wedge.gi3.01", 0.881538, 0.099608), ("wedge.gi3.02", 0.542308, 0.117647),
	("wedge.gi3.03", 0.945385, 0.123529), ("wedge.gi3.04", 0.226154, 0.145098),
	("wedge.gi3.05", 0.320769, 0.165098), ("wedge.gi3.06", 0.955385, 0.222745),
	("wedge.gi3.07", 0.290000, 0.228627),
	("wedge.gi1.01", 0.483077, 0.375686), ("wedge.gi1.02", 0.564615, 0.381176),
	("wedge.gi1.03", 0.197692, 0.439608), ("wedge.gi1.04", 0.944615, 0.469020),
	("wedge.gi1.05", 0.948462, 0.570588), ("wedge.gi1.06", 0.146923, 0.589412),
	("wedge.gi1.07", 0.140769, 0.666275), ("wedge.gi1.08", 0.950769, 0.667059),
	("bayonet.spot-gi1.left", 0.255385, 0.476863), ("bayonet.spot-gi1.right", 0.850000, 0.520392),
	("bayonet.gi0.01", 0.279231, 0.835294), ("bayonet.gi0.02", 0.735385, 0.836078),
	("bayonet.gi0.03", 0.326923, 0.881961), ("bayonet.gi0.04", 0.783077, 0.883137),
	("bayonet.gi0.05", 0.236154, 0.931765), ("bayonet.gi0.06", 0.854615, 0.929412),
	("bayonet.gi0.07", 0.315385, 0.954118), ("bayonet.gi0.08", 0.785385, 0.954902),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament-start", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right",
	68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth", 82: "cabinet.flipper", 84: "cabinet.flipper",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
}

MANUAL_PROJECTED_INPUTS = {9, 81, 83}
MANUAL_PROJECTED_SOLENOIDS = {21, 23}
MANUAL_PROJECTED_LAMPS = set(range(102, 112))


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]] | list[tuple[str, float, float]], source_refs: tuple[str, ...]) -> None:
	placements = []
	for index, position in enumerate(positions, start=1):
		if len(position) == 3:
			suffix, x, y = position
			placement_suffix = f".{suffix}"
		else:
			x, y = position
			placement_suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{placement_suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def _located_gi(device: dict[str, object]) -> None:
	_located(device, "emitter", GI_POSITIONS, (PRO_MANUAL,))
	device.setdefault("physical", {})["quantity"] = 32
	_append_note(device, "The Pro lighting drawing proves 15 wedge-base playfield lamps, eight bayonet-base playfield lamps, two separately called-out spot assemblies, and seven red rear bayonet lamps. The plotted centers are calibrated manual-drawing projections with practical uncertainty of about plus or minus 0.04 normalized x and 0.03 y; VPT GI pools and field effects are not physical sockets. GI-0 through GI-3 share public PinMAME GI channel 0.")


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed disposition to every physical input and output."""
	if len(GI_POSITIONS) != 32:
		raise ValueError("Mustang Pro GI map must contain exactly 32 physical placements")
	if any("spatial" in device for device in [*definition["inputs"], *definition["outputs"]]):
		raise ValueError("Mustang Pro spatial promotion requires a fresh build_pro() definition")
	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", PRO_MANUAL)
		elif device["availability"] == "unused":
			if address in {49, 50}:
				_append_note(device, "The service-manual switch-location drawing plots callouts 49 and 50, but its electrical matrix table leaves both cells blank and the proven Pro script binds neither address. They remain unused controller positions; do not recreate the drawing callouts as live switches without stronger physical evidence.")
			_not_applicable(device, "unused", PRO_MANUAL, PRO_VPX_SOURCE)
		elif address in TROUGH_POSITIONS:
			_located(device, "sensor", TROUGH_POSITIONS[address], (PRO_MANUAL,))
			_append_note(device, "The manual proves six trough positions plus the jam opto but prints only one assembly callout. This is a calibrated projection within that region, with practical uncertainty of about plus or minus 0.03 normalized x and 0.02 y; the working script initializes only switches 18-23 and must not erase physical switch 17.")
		elif address in INPUT_POSITIONS:
			sources = (PRO_MANUAL, PRO_VPX_TABLE_SOURCE) if address in MANUAL_PROJECTED_INPUTS or address in {30, 31, 32, 33} else (PRO_VPX_TABLE_SOURCE,)
			_located(device, "sensor", INPUT_POSITIONS[address], sources)
			if address == 9:
				_append_note(device, "No independent switch-9 object exists in the VPT; the manual-established captive-ball front/rest contact is projected to the exact RCaptKicker1a assembly anchor, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address in {30, 31, 32, 33}:
				_append_note(device, "The physical left/right/bottom/top address follows the service-manual map. The old VPT's Bumper3/Bumper4 object names swap the bottom/top labels, so only their exact centers are used; the script/manual address semantics win.")
			elif address in {81, 83}:
				_append_note(device, "The EOS contact is implicit in the exact VPT flipper assembly, so the flipper center is an assembly projection with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device.setdefault("roles", [CABINET_INPUT_ROLES[address]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		else:
			raise ValueError(f"Mustang Pro input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", PRO_MANUAL)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[(group, address)]])
			_not_applicable(device, "cabinet_or_service", PRO_MANUAL)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			sources = (PRO_MANUAL,) if address in MANUAL_PROJECTED_SOLENOIDS else (PRO_MANUAL, PRO_VPX_TABLE_SOURCE) if address in {9, 10, 11, 12} else (PRO_VPX_TABLE_SOURCE,)
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], sources)
			device.setdefault("physical", {})["quantity"] = len(SOLENOID_POSITIONS[address])
			if address in {3, 4}:
				_append_note(device, "Outputs 3 and 4 are the power and hold windings of one physical mid-ramp actuator and intentionally share one assembly anchor.")
			elif address in {5, 6}:
				_append_note(device, "Outputs 5 and 6 are the power and hold windings of one physical upper-ramp actuator and intentionally share one assembly anchor.")
			elif address in {9, 10, 11, 12}:
				_append_note(device, "The service-manual left/right/bottom/top assignment controls; old VPT bumper object numbering is used only for exact geometry.")
			elif address == 31:
				_append_note(device, "The manual proves one physical UP POST assembly. The exact UpPost center is the physical placement; the working VPT also toggles a tangent UpPost2 collision wall at x=0.471787, y=0.046636 as part of the same route-blocking assembly, not as proof of a second physical post.")
			elif address in {21, 23}:
				_append_note(device, "The manual combines outputs 21 and 23 under one BACK PNL FLASH callout. This left/right center is a calibrated drawing projection with practical uncertainty of about plus or minus 0.04 normalized x and 0.03 y; no VPT bloom helper is treated as the physical emitter.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			sources = (PRO_MANUAL,) if address in MANUAL_PROJECTED_LAMPS else (PRO_MANUAL, PRO_VPX_TABLE_SOURCE)
			_located(device, "emitter", LAMP_POSITIONS[address], sources)
			device.setdefault("physical", {})["quantity"] = 1
			if address in {20, 26}:
				_append_note(device, "This is one color channel of the physical fourth-gear two-color insert; addresses 20 and 26 intentionally share one center and must not become two playfield inserts.")
			elif address in {34, 42}:
				_append_note(device, "This is one color channel of the physical sixth-gear two-color insert; addresses 34 and 42 intentionally share one center and must not become two playfield inserts.")
			elif address in MANUAL_PROJECTED_LAMPS:
				_append_note(device, "The manual proves this sign emitter. Its center is calibrated from the location drawing rather than an alpha-ramp visual helper, with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif group == "pinmame.output.gi" and address == 0:
			_located_gi(device)
		else:
			raise ValueError(f"Mustang Pro output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Mustang Pro knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PRO_KNOWLEDGE,
	"Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, and recreation behavior validated**",
	"Coverage: **author-ready - physical inventory, PinMAME bindings, mechanisms, recreation behavior, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nEvery physical playfield input, actuator, lamp, and GI socket has a normalized player-view placement: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. Exact object centers come from the known-working VPT only after script/manual reconciliation. Trough contacts, captive-ball switch 9, implicit EOS contacts, sign lamps, back-panel flashers, and GI sockets use explicitly disclosed assembly or drawing projections with practical uncertainty; cabinet, service, virtual, unpopulated, unused, and DIP devices are explicitly outside playfield space.\n\nThe Pro manual's lighting drawing proves 32 physical GI emitters behind one public transport channel: 15 wedge-base playfield lamps, eight bayonet-base playfield lamps, two separately called-out spot assemblies, and seven red rear bayonet lamps. Calibrated drawing projections preserve the four physical GI-0 through GI-3 regions; VPT light pools, broad fields, and reflections are excluded.\n\nThe switch-location drawing plots callouts 49 and 50 even though the electrical matrix table leaves 49-53 blank and the working Pro script binds neither 49 nor 50. The definition follows the proven controller behavior and electrical table, keeps both channels explicitly unused, and records the drawing conflict instead of inventing two live switches. The drawing is still valuable as evidence that the page was shared or revised inconsistently.\n\nThe standard lamp audit corrects a prior one-address shift: both 43 and 44 are blank, 45 is Shot Arrow #5, 49 is the bottom right 3-bank lamp, and 80 is the physical right-pop lamp. Addresses 20/26 and 34/42 are paired color channels at shared fourth-gear and sixth-gear insert centers.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `manual.mustang-pro`: official Stern `Mustang-Manual.pdf`, SHA-256 `63d0b8d44dadb22e8e878586805f805b71aa65038a77e00f5b973ece3b118235`; scanned I/O tables on PDF pages 12, 15, 18, and 20.",
	"- `manual.mustang-pro`: official Stern `Mustang-Manual.pdf`, SHA-256 `63d0b8d44dadb22e8e878586805f805b71aa65038a77e00f5b973ece3b118235`; scanned I/O tables on PDF pages 12, 15, 18, and 20, physical location drawings on PDF pages 13, 16, 19, and 21, and GI map on PDF page 40.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `vpx-table.mustang-pro-85vett-gtxjoe-1.0`: working VPT SHA-256 `3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c`, retained externally under `pinmame-game-code/mt_145/vpx-table`; source archive SHA-256 `d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615`.",
	"- `vpx-table.mustang-pro-85vett-gtxjoe-1.0`: working `Mustang Pro_85vett_mod_gtxjoe_1.0.vpt`, 32,862,208 bytes, SHA-256 `3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c`, retained externally under `pinmame-vpx-sources/stern/mustang-pro-2014`; source archive SHA-256 `d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615`. Because one embedded image stream is one byte short, the vpxtool analysis derivative sets the GameData `SIMG` and `SSND` counts to zero; the OLE rewrite also zeroes 58 residual bytes after the GameData `ENDB` marker. All 5,311 GameItem streams and the embedded script remain byte-identical. The derivative SHA-256 is `b859cc86dd69978411eeaabb135e270c950e01498b2f986b034c6b49f5b9e7ed` and it is not distributed as the source table.",
)


def promote() -> None:
	definition = build_pro()
	table_source = next(source for source in definition["sources"] if source["id"] == PRO_VPX_TABLE_SOURCE)
	table_source.update({
		"known_working": True,
		"locator": "Mustang Pro_85vett_mod_gtxjoe_1.0.vpt (32,862,208 bytes) from Mustang-Pro-85vett-gtxjoe-v1.0.zip SHA-256 d73e2e2edd7dcfef64f2396f4d09fe169f273dfb0ba86abee59b2af5a45c3615. Geometry extraction used an analysis-only derivative that set GameData SIMG/SSND counts to zero to bypass a one-byte-short embedded image stream; its OLE rewrite also zeroed 58 residual bytes after the GameData ENDB marker. All 5,311 GameItem streams and the embedded script are byte-identical to the source table.",
		"original_filename": "Mustang Pro_85vett_mod_gtxjoe_1.0.vpt",
		"rights": "NOASSERTION",
		"uri": "external:pinmame-vpx-sources/stern/mustang-pro-2014/source/Mustang-Pro-85vett-gtxjoe-v1.0.zip",
	})
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/mustang-pro-2014.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
