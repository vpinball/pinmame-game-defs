"""Promote Metallica Premium / Limited Edition with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import write_json, write_text

from curate_metallica import CORE_SOURCE, MANUAL_SOURCE, PREMIUM_KNOWLEDGE, VPX_SOURCE, VPX_TABLE_SOURCE, build_premium


PARTIAL_PATH = ROOT / "machines/partial/stern/metallica-premium-limited-edition-2013.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/metallica-premium-limited-edition-2013.json"

DIRECT_SOURCES = (MANUAL_SOURCE, VPX_SOURCE, VPX_TABLE_SOURCE)

INPUT_POSITIONS = {
	1: [(0.191759, 0.703592)], 3: [(0.059250, 0.479418)], 4: [(0.062139, 0.389601)],
	7: [(0.125069, 0.491806)], 9: [(0.125264, 0.457961)],
	18: [(0.565274, 0.940586)], 19: [(0.661250, 0.914083)],
	20: [(0.757227, 0.888562)], 21: [(0.855903, 0.863163)],
	22: [(0.900000, 0.890000)], 23: [(0.942423, 0.911169)],
	24: [(0.056139, 0.742408)], 25: [(0.126141, 0.703491)],
	26: [(0.282798, 0.720336)], 27: [(0.701945, 0.719894)],
	28: [(0.793139, 0.716093)], 29: [(0.876483, 0.748814)],
	30: [(0.609808, 0.124695)], 31: [(0.836014, 0.154043)], 32: [(0.665768, 0.218572)],
	33: [(0.186353, 0.222100)], 34: [(0.186353, 0.222100)],
	35: [(0.454604, 0.117562)], 36: [(0.184264, 0.326680)], 37: [(0.303279, 0.313888)],
	38: [(0.124831, 0.329618)], 39: [(0.841242, 0.415086)],
	40: [(0.670810, 0.372407)], 41: [(0.800701, 0.381795)], 42: [(0.563102, 0.286302)],
	43: [(0.093013, 0.097521)], 44: [(0.708680, 0.077643)],
	45: [(0.797060, 0.082145)], 46: [(0.913523, 0.074920)],
	47: [(0.591456, 0.104294)], 50: [(0.059561, 0.106073)],
	51: [(0.806064, 0.568948)], 52: [(0.206991, 0.194319)], 53: [(0.475346, 0.154012)],
	54: [(0.658092, 0.307063)], 55: [(0.672144, 0.285475)], 56: [(0.672144, 0.285475)],
	57: [(0.465320, 0.459637)], 58: [(0.479282, 0.436438)], 59: [(0.487989, 0.411479)],
	60: [(0.251574, 0.334229)], 61: [(0.232906, 0.301897)], 62: [(0.212833, 0.269981)],
	63: [(0.522900, 0.376119)], 64: [(0.522666, 0.376099)],
	81: [(0.660495, 0.828849)], 83: [(0.324765, 0.828700)],
}

SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.855903, 0.863163)], 2: [(0.942384, 0.902411)],
	3: [(0.186353, 0.222100)], 4: [(0.453765, 0.224876)],
	5: [(0.658092, 0.307063)], 6: [(0.806064, 0.568948)],
	9: [(0.609808, 0.124695)], 10: [(0.836014, 0.154043)], 11: [(0.665768, 0.218572)],
	12: [(0.672144, 0.285475)], 13: [(0.282798, 0.720336)], 14: [(0.701945, 0.719894)],
	15: [(0.324765, 0.828700)], 16: [(0.660495, 0.828849)],
	18: [(0.445353, 0.075947)], 19: [(0.161927, 0.175367)], 20: [(0.186353, 0.222100)],
	23: [(0.295714, 0.155228)], 25: [(0.711659, 0.165854)],
	26: [(0.155106, 0.127482), (0.189682, 0.111923)],
	27: [(0.389813, 0.090960), (0.517706, 0.092053)],
	28: [(0.237497, 0.191206), (0.580200, 0.231229)],
	29: [(0.790852, 0.305200)], 30: [(0.789757, 0.243561)],
	31: [(0.492473, 0.451197)], 32: [(0.454109, 0.288284)],
	51: [(0.462533, 0.485362)], 52: [(0.522666, 0.376099)],
	53: [(0.551829, 0.309179)], 54: [(0.232438, 0.302036)],
	55: [(0.548260, 0.022270)], 56: [(0.672144, 0.285475)],
}

FLASHER_QUANTITIES = {19: 1, 21: 3, 22: 3, 23: 1, 25: 1, 26: 2, 27: 2, 28: 2, 29: 1, 30: 1, 31: 2, 32: 1}

LAMP_QUANTITIES = {25: 2, 53: 2}

LAMP_POSITIONS = {
	17: [(0.810352, 0.448962)], 18: [(0.783051, 0.485479)], 19: [(0.762352, 0.519753)],
	21: [(0.458502, 0.304936)], 22: [(0.686806, 0.268904)], 23: [(0.781003, 0.564010)],
	24: [(0.810124, 0.572895)], 25: [(0.759371, 0.586215)], 26: [(0.790919, 0.653819)],
	27: [(0.872626, 0.679744)], 28: [(0.685974, 0.450805)], 29: [(0.659835, 0.488313)],
	30: [(0.637350, 0.522300)], 31: [(0.769263, 0.418730)], 32: [(0.656510, 0.401906)],
	33: [(0.361570, 0.305243)], 34: [(0.377428, 0.346229)], 35: [(0.393199, 0.377615)],
	37: [(0.604823, 0.692698)], 38: [(0.548294, 0.686171)], 39: [(0.492934, 0.683480)],
	40: [(0.435107, 0.685563)], 41: [(0.379661, 0.692326)], 42: [(0.193443, 0.658411)],
	43: [(0.146373, 0.610267)], 44: [(0.198198, 0.605012)], 45: [(0.219246, 0.583035)],
	46: [(0.340430, 0.495675)], 47: [(0.322124, 0.460959)], 48: [(0.300377, 0.423285)],
	49: [(0.127812, 0.336430)], 50: [(0.152536, 0.377489)], 51: [(0.175880, 0.408342)],
	53: [(0.494995, 0.877688)], 55: [(0.418857, 0.809089)], 56: [(0.468333, 0.809112)],
	57: [(0.518161, 0.809758)], 58: [(0.566991, 0.809482)], 59: [(0.384790, 0.754152)],
	60: [(0.455706, 0.753974)], 61: [(0.524753, 0.754435)], 62: [(0.595456, 0.753908)],
	63: [(0.058425, 0.707354)], 64: [(0.127486, 0.663399)], 65: [(0.309461, 0.343378)],
	66: [(0.704375, 0.127860)], 67: [(0.758697, 0.126907)], 68: [(0.407623, 0.165896)],
	69: [(0.455043, 0.157332)], 70: [(0.499183, 0.167578)], 71: [(0.211489, 0.355878)],
	73: [(0.665741, 0.219453)], 74: [(0.834953, 0.155124)], 75: [(0.609386, 0.124029)],
	77: [(0.224177, 0.454073)], 78: [(0.223363, 0.477100)], 79: [(0.222879, 0.500506)],
	80: [(0.219410, 0.521961)],
}

RGB_POSITIONS = {
	87: [(0.143356, 0.571677)], 88: [(0.143356, 0.571677)], 89: [(0.143356, 0.571677)],
	90: [(0.722853, 0.400220)], 91: [(0.722853, 0.400220)], 92: [(0.722853, 0.400220)],
	99: [(0.842162, 0.399062)], 100: [(0.842162, 0.399062)], 101: [(0.842162, 0.399062)],
	102: [(0.095053, 0.283652)], 103: [(0.095053, 0.283652)], 104: [(0.095053, 0.283652)],
	108: [(0.272384, 0.371514)], 109: [(0.272384, 0.371514)], 110: [(0.272384, 0.371514)],
	126: [(0.336693, 0.251626)], 127: [(0.336693, 0.251626)], 128: [(0.336693, 0.251626)],
}

RED_GI_POSITIONS: list[tuple[str, float, float]] = [
	("vpx.gir1", 0.157771, 0.785398), ("vpx.gir2", 0.238343, 0.740317),
	("vpx.gir3", 0.788135, 0.798484), ("vpx.gir4", 0.743324, 0.737215),
	("vpx.gir5", 0.029802, 0.609245), ("vpx.gir6", 0.867415, 0.585202),
	("vpx.gir7", 0.105635, 0.044632), ("vpx.gir8", 0.314176, 0.056265),
	("vpx.gir9", 0.605445, 0.080308), ("vpx.gir10", 0.863968, 0.015936),
]

BLUE_GI_POSITIONS: list[tuple[str, float, float]] = [
	("vpx.gib1", 0.193533, 0.796932), ("vpx.gib2", 0.236620, 0.719375),
	("vpx.gib3", 0.757112, 0.807015), ("vpx.gib4", 0.748495, 0.718600),
	("vpx.gib5", 0.033249, 0.645696), ("vpx.gib6", 0.884650, 0.625532),
	("vpx.gib7", 0.134934, 0.113658), ("vpx.gib8", 0.057377, 0.063246),
	("vpx.gib9", 0.334859, 0.073328), ("vpx.gib10", 0.576146, 0.064797),
	("vpx.gib11", 0.931184, 0.050836),
]

WHITE_UPPER_POSITIONS: list[tuple[str, float, float]] = [
	("vpx.gispotl1", 0.159651, 0.858123), ("vpx.gispotl2", 0.277970, 0.719929),
	("vpx.gispotr1", 0.762630, 0.846998), ("vpx.gispotr2", 0.710782, 0.720769),
	("vpx.gispotr3", 0.891070, 0.424445),
]

WHITE_PLAYFIELD_POSITIONS: list[tuple[str, float, float]] = [
	("vpx.giw1", 0.236111, 0.809389), ("vpx.giw2", 0.265494, 0.760278),
	("vpx.giw3", 0.728622, 0.816944), ("vpx.giw4", 0.712532, 0.760907),
	("vpx.giw5", 0.030432, 0.625065), ("vpx.giw6", 0.875535, 0.600509),
	("vpx.giw7", 0.860144, 0.504805), ("vpx.giw8", 0.850350, 0.481509),
	("vpx.giw9", 0.115782, 0.423583), ("vpx.giw10", 0.043025, 0.290731),
	("vpx.giw11", 0.279485, 0.273102), ("vpx.giw12", 0.276687, 0.245398),
	("vpx.giw13", 0.349444, 0.128917), ("vpx.giw14", 0.336852, 0.096806),
	("vpx.giw15", 0.157757, 0.099324), ("vpx.giw16", 0.089197, 0.055250),
	("vpx.giw17", 0.671255, 0.073509), ("vpx.giw18", 0.762202, 0.066583),
	("vpx.giw19", 0.847552, 0.086102), ("vpx.giw20", 0.930103, 0.014324),
	("vpx.giw21", 0.868540, 0.191880), ("vpx.giw23", 0.879733, 0.123250),
]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "service.ticket",
	-3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right",
	68: "cabinet.coin.fourth", 69: "cabinet.coin.fifth",
	82: "flipper.lower.right.button", 84: "flipper.lower.left.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.solenoid", 21): "cabinet.rear-panel",
	("pinmame.output.solenoid", 22): "cabinet.rear-panel",
	("physical.output.ticket", 33): "service.ticket",
	("physical.output.ticket", 34): "service.ticket",
	("physical.output.ticket", 35): "service.ticket",
	("pinmame.output.lamp", 72): "cabinet.start",
	("pinmame.output.lamp", 76): "cabinet.tournament",
}


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


def _apply_gi(device: dict[str, object], address: int) -> None:
	if address == 130:
		_located(device, "emitter", RED_GI_POSITIONS, DIRECT_SOURCES)
		device.setdefault("physical", {})["quantity"] = 11
		_append_note(device, "The official red-GI map proves nine wedge-base and two bayonet fixtures. The exact table exposes ten one-for-one GIR authoring-light centers; the eleventh physical socket remains proven by the manual but is not assigned a fabricated point. Recreate all 11 from the manual map and treat these ten coordinates as calibrated anchors.")
	elif address == 132:
		_located(device, "emitter", BLUE_GI_POSITIONS, DIRECT_SOURCES)
		device.setdefault("physical", {})["quantity"] = 11
		_append_note(device, "The official blue-GI map proves nine wedge-base and two bayonet fixtures, matching the exact table's 11 GIB centers.")
	elif address == 134:
		_located(device, "emitter", WHITE_UPPER_POSITIONS, DIRECT_SOURCES)
		device.setdefault("physical", {})["quantity"] = 11
		_append_note(device, "Driver-board CN22 feeds five front spot lamps and six back-panel lamps. The five exact GIWU spot centers are in playfield space; the manual-proven six back-panel fixtures remain in the quantity but intentionally have no playfield coordinate.")
	elif address == 136:
		_located(device, "emitter", WHITE_PLAYFIELD_POSITIONS, DIRECT_SOURCES)
		device.setdefault("physical", {})["quantity"] = 28
		_append_note(device, "Driver-board CN23 feeds the white LED system. The manual proves 22 wedge-base and two bayonet playfield fixtures plus two wedge-base and two bayonet bottom-arch fixtures. The exact table exposes 22 GIW authoring centers; the remaining six physical sockets stay explicit in quantity and in the manual map rather than receiving invented separation coordinates.")
	else:
		raise ValueError(f"Unexpected Metallica Premium GI address {address}")


def apply_spatial(definition: dict[str, object]) -> None:
	"""Apply one reviewed spatial disposition to every physical input and output."""
	if any("spatial" in device for collection in (definition["inputs"], definition["outputs"]) for device in collection):
		raise ValueError("Metallica Premium spatial curation requires an unspatialized base definition")

	for device in definition["inputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			if address == 81:
				device["roles"] = ["flipper.lower.right.eos"]
			elif address == 83:
				device["roles"] = ["flipper.lower.left.eos"]
			sources = (MANUAL_SOURCE,) if address == 22 else DIRECT_SOURCES
			_located(device, "sensor", INPUT_POSITIONS[address], sources)
			if address == 22:
				_append_note(device, "The manual requires this downstream trough-jam opto, while the exact table pulses it during eject without a dedicated geometry object. Its point is a disclosed regional projection between trough switch 21 and shooter-lane switch 23, with practical uncertainty of about plus or minus 0.04 normalized x and 0.03 normalized y.")
			elif address in {26, 27}:
				_append_note(device, "The switch is implicit in the exact VPX slingshot collision wall. This point is the six-vertex wall centroid with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address in {33, 34}:
				_append_note(device, "The two limit switches belong to the moving grave-marker assembly. The exact table does not expose separate contact centers; both use its manual-confirmed LMagnet assembly anchor and remain distinct controller sensors.")
			elif address in {55, 56}:
				_append_note(device, "This is the exact snake moving-assembly pivot, not a claim that the jaw-open and latch contacts occupy the same internal point. The manual and proven script distinguish their functions.")
			elif address in {60, 61, 62}:
				_append_note(device, "This is the exact visible target primitive center; the normally-closed under-playfield contact follows the moving target at the same assembly position.")
			elif address in {81, 83}:
				_append_note(device, "The normally-closed EOS contact is implicit in the exact lower-flipper assembly; this is its assembly center, with practical uncertainty of about plus or minus 0.03 normalized x and y.")
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Metallica Premium input {group} {address} has no reviewed spatial disposition")

	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			if group == "pinmame.output.solenoid" and address in {21, 22}:
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
				_append_note(device, "The official back-panel map proves three physical flasher bulbs on this side; all stay outside normalized playfield space.")
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], DIRECT_SOURCES)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address in {3, 20}:
				_append_note(device, "The grave-marker magnet and motor belong to one moving assembly and intentionally share the table's manual-confirmed LMagnet anchor; their controller functions remain independent.")
			elif address in {5, 12, 56}:
				_append_note(device, "This actuator belongs to the snake's ball-eject/jaw/latch assembly. The exact ball-hold kicker or moving-snake pivot supplies the rest-state assembly point; internal coils are not falsely separated.")
			elif address in {13, 14}:
				_append_note(device, "This exact VPX slingshot-wall centroid is the manual-confirmed coil assembly projection, with practical uncertainty of about plus or minus 0.02 normalized x and y.")
			elif address == 18:
				_append_note(device, "The exact BM_sparkyhead rest-state pivot supplies the Sparky step-up assembly point. It is a moving parent-relative coordinate, not an internal coil center.")
			elif address == 31:
				_append_note(device, "The official coil map proves two coffin-insert flasher bulbs. The exact table exposes one composite F31 anchor, so quantity remains two but no unsupported bulb separation is invented.")
			elif address == 54:
				_append_note(device, "The reset coil acts on the complete three-target bank. This point is the centroid of exact target centers 60-62, not a claim that the under-playfield reset coil sits on the playfield surface.")
		elif group == "pinmame.output.lamp" and 1 <= address <= 80:
			if address in LAMP_POSITIONS:
				_located(device, "emitter", LAMP_POSITIONS[address], DIRECT_SOURCES)
				quantity = LAMP_QUANTITIES.get(address, 1)
				device.setdefault("physical", {})["quantity"] = quantity
				if quantity > len(LAMP_POSITIONS[address]):
					_append_note(device, "The official Premium lamp-location map proves two physical bulbs for this output. The exact table exposes one composite light anchor, so quantity remains two but no unsupported bulb separation is invented.")
			else:
				raise ValueError(f"Used Metallica Premium standard lamp {address} has no reviewed position")
		elif group == "pinmame.output.lamp" and address in RGB_POSITIONS:
			_located(device, "emitter", RGB_POSITIONS[address], DIRECT_SOURCES)
			device.setdefault("physical", {})["quantity"] = 1
			_append_note(device, "This record is one color channel of one physical tri-color module. All three public channel records intentionally share the same module center and must not be built as separate lamps.")
		elif group == "pinmame.output.lamp" and address in {130, 132, 134, 136}:
			_apply_gi(device, address)
		elif group == "pinmame.output.gi" and address == 0:
			device["roles"] = ["internal.compatibility"]
			_not_applicable(device, "internal_nonvisual", VPX_SOURCE, CORE_SOURCE)
			_append_note(device, "This is PinMAME's aggregate compatibility callback, not another physical GI circuit. Physical emitters are represented only by public lamp channels 130, 132, 134, and 136.")
		else:
			raise ValueError(f"Metallica Premium output {group} {address} ({kind}) has no reviewed spatial disposition")


def _replace_once(value: str, anchor: str, replacement: str) -> str:
	if value.count(anchor) != 1:
		raise ValueError(f"Metallica Premium knowledge anchor must occur exactly once: {anchor!r}")
	return value.replace(anchor, replacement, 1)


SPATIAL_KNOWLEDGE = _replace_once(
	PREMIUM_KNOWLEDGE,
	"Coverage: **author-ready - complete physical inventory, public PinMAME bindings, custom mechanisms, and recreation behavior validated**",
	"Coverage: **author-ready - complete physical inventory, public PinMAME bindings, custom mechanisms, recreation behavior, and spatial placements validated**",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"Physical RGB-object coordinates were recovered from the exact working table during curation but have not yet been normalized and promoted into the definition.",
	"All physical tri-color module centers are normalized from the exact working table and reconciled with the manual wiring map. Each RGB channel record shares its physical module point; never create one lamp per color channel.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"## Sources\n",
	"## Spatial coordinate model\n\nEvery physical playfield sensor, actuator, controlled lamp, and GI authoring anchor uses one normalized player-view frame from the exact 952.941 by 2117.647 VPW table: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 apron. Exact object centers are accepted only after the proven script establishes controller semantics and the official manual confirms the physical assembly. Cabinet, service, back-panel, virtual, DIP, unused, and compatibility-only records never receive fake playfield points. The trough-jam opto, moving-assembly contacts, slingshot contacts/coils, EOS contacts, and bank reset are explicitly identified as regional or assembly projections rather than fabricated internal component centers.\n\nThe grave marker is one moving assembly with separate magnet output 3, motor output 20, down/up switches 33/34, ball opto 52, and flasher 19. The electric-chair/Sparky area keeps magnet 4, standup 35, ball opto 53, step-up 18, and its flashers separate. The coffin mechanism likewise separates three lock optos 57-59 and lock release 51 from magnet position/detection switches 64/63, lowering output 52, and virtual processor bits 57/58. Snake eject 5, latch release 12, jaw close 56, ball switch 54, jaw-open 55, and latch 56 remain distinct controller devices even where only one defensible rest-state assembly pivot exists.\n\nPhysical lighting multiplicity follows the manual, not the render-object count. Standard lamps 25 (Mystery) and 53 (Shoot Again) each drive two physical bulbs while the exact table supplies one composite anchor, so their quantities remain two without invented bulb separation. Red GI is nine wedge plus two bayonet fixtures; the table supplies ten calibrated GIR anchors and the manual retains the eleventh without invented precision. Blue GI is nine wedge plus two bayonet and matches 11 GIB anchors. CN22 drives five exact front spot-lamp anchors plus six back-panel fixtures outside playfield space. CN23 drives 22 wedge and two bayonet playfield fixtures plus four bottom-arch fixtures; the exact table supplies 22 GIW anchors, while the remaining six are retained in physical quantity and located by the cited manual map rather than guessed. Public `pinmame.output.gi/0` is only an aggregate compatibility callback and creates no additional bulbs. Back-panel flashers 21/22 each have three physical bulbs outside playfield space. Coffin flasher 31 has two physical bulbs but one defensible composite F31 anchor.\n\n## Sources\n",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; wiring PDF pages 42-50 and Premium service tables pages 103-110.",
	"- `manual.metallica-pro-premium`: official Stern `MTLAB1-compressed.pdf`, SHA-256 `f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090`; RGB/GI driver and physical lighting maps on PDF pages 45-50 (pages 47-50 are LE-titled sheets applied to this combined Premium/LE record because the editions share the playfield), Premium switch/lamp/coil location maps on pages 104, 106, and 108, and auxiliary output map on page 110.",
)
SPATIAL_KNOWLEDGE = _replace_once(
	SPATIAL_KNOWLEDGE,
	"- `vpx-table.metallica-premium-monsters-vpw-2.0`: exact local table, SHA-256 `afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f`; used read-only to resolve RGB timer addresses and physical object positions.",
	"- `vpx-table.metallica-premium-monsters-vpw-2.0`: exact known-working `Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx`, 424,071,168 bytes, SHA-256 `afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f`; retained externally under `pinmame-vpx-sources/stern/metallica-premium-limited-edition-2013/source` and extracted read-only with vpxtool git:v0.33.3 for the sole normalized geometry frame.",
)


def promote() -> None:
	definition = build_premium()
	table_source = next(source for source in definition["sources"] if source["id"] == VPX_TABLE_SOURCE)
	table_source["known_working"] = True
	table_source["uri"] = "external:pinmame-vpx-sources/stern/metallica-premium-limited-edition-2013/source/Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx"
	table_source["locator"] = "Metallica Premium Monsters (Stern 2013) VPW 2.0.vpx (424,071,168 bytes); exact mtl_180h table extracted with vpxtool git:v0.33.3; its 952.941 by 2117.647 bounds are the sole normalized coordinate frame after script/manual reconciliation"
	manual_source = next(source for source in definition["sources"] if source["id"] == MANUAL_SOURCE)
	manual_source["locator"] = "MTLAB1-compressed.pdf: RGB/GI board and lighting maps on PDF pages 45-50 (pages 47-50 are LE-titled sheets applied to the combined Premium/LE record because the editions share the playfield); Premium switch/lamp/coil location maps on pages 104, 106, 108, and 110; related service tables on pages 103-109"
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/metallica-premium-limited-edition-2013.md", SPATIAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
