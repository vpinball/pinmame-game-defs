"""Retain the reviewed Stern 24 (2009) spatial evidence as a schema-v2 partial."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, write_json, write_text

from curate_twenty_four import (
	CORE_SOURCE,
	KNOWLEDGE,
	MANUAL_SOURCE,
	RUNTIME_COIL_SOURCE,
	RUNTIME_LAMP_SOURCE,
	RUNTIME_SWITCH_HIGH_SOURCE,
	RUNTIME_SWITCH_LOW_SOURCE,
	RUNTIME_SUITCASE_SOURCE,
	SAM_REFERENCE_SOURCE,
	VPX_SOURCE,
	build,
)


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/twenty-four-2009.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/twenty-four-2009.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/twenty-four-2009.md"

TABLE_SOURCE = "vpx-table.stern-24-2009-local"
EMBEDDED_SCRIPT_SOURCE = "vpx.stern-24-embedded-2.0.1"

TABLE_SOURCE_RECORD = {
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"uri": "external:pinmame-vpx-sources/stern/twenty-four-2009/source/24 (Stern 2009).vpx",
	"sha256": "7e8bf294f3b3dd4bfe53e2727957d000568bc9d079caeed60038ceeb8d1b89f5",
	"locator": "Exact 24 (Stern 2009).vpx found in the first required primary local table directory, retained in the established external VPX cache and extracted with vpxtool git:v0.33.3. Embedded game name is twenty4_150 and the playfield bounds are 979 by 2300. Direct playfield object centers supply geometry only; controller causality remains reconciled to the pinned known-working v2.3.1 script.",
	"original_filename": "24 (Stern 2009).vpx",
	"known_working": True,
	"license": "NOASSERTION",
	"attribution": "Table authors credited in the embedded VPX script; source retained externally",
	"rights": "NOASSERTION",
	"acquired_at": "2026-08-04T00:00:00Z",
}

EMBEDDED_SCRIPT_SOURCE_RECORD = {
	"id": EMBEDDED_SCRIPT_SOURCE,
	"kind": "vpx_script",
	"uri": "external:pinmame-review-artifacts/stern/twenty-four-2009/extracted/script.vbs",
	"sha256": "be3a0e0e96df6d232fa1fa99110e63781abdca5484a1b97de75de0fd1760135a",
	"locator": "Script extracted from the exact local 24 (Stern 2009).vpx with vpxtool git:v0.33.3. It confirms the embedded twenty4_150 object names, callbacks, and direct render helpers. This embedded 2.0.1 script predates the pinned v2.3.1 semantic script and its visible-lock handler is not used to override the reviewed bottom-to-ROM mapping; the newer pinned script remains the causality tie-breaker.",
	"revision": "2.0.1",
	"license": "NOASSERTION",
	"attribution": "Table authors credited in the embedded VPX script; source retained externally",
	"rights": "NOASSERTION",
	"acquired_at": "2026-08-04T00:00:00Z",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(dict.fromkeys(source_refs))}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], *source_refs: str) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _append_note(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	if not isinstance(physical, dict):
		physical = {}
		device["physical"] = physical
	previous = physical.get("notes")
	physical["notes"] = f"{previous} {note}" if isinstance(previous, str) and previous else note


def _point(x: float, y: float) -> list[tuple[float, float]]:
	return [(x, y)]


# All direct values are normalized from the extracted VPX playfield bounds.
# Projections below are not perspective estimates: they are explicitly derived
# from direct anchors and the documented ordered assembly. Their notes disclose
# the practical uncertainty to an author.
INPUT_POSITIONS = {
	1: _point(0.164819, 0.188801), 2: _point(0.281104, 0.173904), 3: _point(0.204435, 0.154732),
	4: _point(0.077429, 0.606847), 5: _point(0.119294, 0.568861), 6: _point(0.123520, 0.544395),
	7: _point(0.128090, 0.520139), 8: _point(0.132536, 0.496686), 9: _point(0.136141, 0.472678),
	10: _point(0.183861, 0.413478), 11: _point(0.185062, 0.224781), 13: _point(0.303980, 0.210958),
	14: _point(0.053777, 0.202741), 23: _point(0.940245, 0.891630), 24: _point(0.055158, 0.774130),
	25: _point(0.129213, 0.753913), 26: _point(0.216502, 0.742885), 27: _point(0.694272, 0.747842),
	28: _point(0.781410, 0.755435), 29: _point(0.858018, 0.774565), 30: _point(0.520314, 0.179845),
	31: _point(0.723910, 0.183740), 32: _point(0.591699, 0.256672), 33: _point(0.555868, 0.292535),
	34: _point(0.591094, 0.311433), 39: _point(0.852528, 0.542760), 40: _point(0.852864, 0.515881),
	41: _point(0.852507, 0.488920), 43: _point(0.609803, 0.050623), 44: _point(0.604715, 0.074850),
	45: _point(0.604699, 0.098961), 46: _point(0.063113, 0.188293), 48: _point(0.472676, 0.079457),
	54: _point(0.928215, 0.143491), 55: _point(0.531042, 0.108913), 56: _point(0.622063, 0.109783),
	57: _point(0.710930, 0.108913), 58: _point(0.704104, 0.282934), 60: _point(0.376028, 0.363361),
	61: _point(0.570885, 0.409409), 62: _point(0.820667, 0.126341),
}

# The exact table exposes Drain and BallRelease but no trough contact objects.
# These five ordered points are an explicit trough-region projection between
# those anchors, with practical uncertainty of about +/-0.03 normalized.
TROUGH_POSITIONS = {
	18: _point(0.554578, 0.948280), 19: _point(0.634218, 0.929093), 20: _point(0.713857, 0.909906),
	21: _point(0.793497, 0.890719), 22: _point(0.833317, 0.881126),
}

EOS_POSITIONS = {81: _point(0.627104, 0.851511), 83: _point(0.286698, 0.853653)}
FLIPPER_BUTTON_ADDRESSES = {82, 84}
FLIPPERS = {15: _point(0.286698, 0.853653), 16: _point(0.627104, 0.851511)}
BUMPERS = {9: _point(0.520314, 0.179845), 10: _point(0.723910, 0.183740), 11: _point(0.591699, 0.256672)}
SLINGS = {17: _point(0.216502, 0.742885), 18: _point(0.694272, 0.747842)}
SUITCASE = _point(0.472676, 0.079457)
SAFEHOUSE = _point(0.220633, 0.191522)
SNIPER = _point(0.693565, 0.077391)
POST45 = _point(0.604998, 0.111830)

OUTPUT_POSITIONS = {
	1: _point(0.873136, 0.871533), 2: _point(0.941201, 0.952984), 3: _point(0.204435, 0.154732),
	4: _point(0.376028, 0.363361), 5: _point(0.570885, 0.409409), 6: _point(0.493871, 0.075000),
	7: _point(0.747702, 0.074130), 9: BUMPERS[9], 10: BUMPERS[10], 11: BUMPERS[11],
	12: SAFEHOUSE, 13: _point(0.244521, 0.217870), 14: SNIPER, 15: FLIPPERS[15], 16: FLIPPERS[16],
	17: SLINGS[17], 18: SLINGS[18], 19: _point(0.134823, 0.132553), 20: SNIPER,
	21: SUITCASE, 22: _point(0.050870, 0.313424), 23: SUITCASE, 25: SUITCASE,
	26: _point(0.621344, 0.185702), 27: _point(0.878493, 0.515853), 28: POST45,
	29: _point(0.807799, 0.281797), 30: SUITCASE, 31: [_point(0.709262, 0.753323)[0], _point(0.201659, 0.754986)[0]],
	32: _point(0.155022, 0.264470),
}

FLASHER_QUANTITIES = {19: 3, 20: 2, 26: 3, 27: 1, 31: 2, 32: 3}

LAMP_POSITIONS = {
	3: (0.457354, 0.862935), 4: (0.388407, 0.490000), 5: (0.514045, 0.489891), 6: (0.477528, 0.417391),
	7: (0.885342, 0.352935), 8: (0.140449, 0.645652), 10: (0.052094, 0.703913), 11: (0.130490, 0.692826),
	12: (0.776558, 0.693043), 13: (0.856997, 0.704130), 14: (0.782176, 0.486522), 15: (0.781920, 0.512500),
	16: (0.781154, 0.538913), 17: (0.325332, 0.533478), 18: (0.449949, 0.533261), 19: (0.575077, 0.533696),
	20: (0.325843, 0.562174), 21: (0.450970, 0.562609), 22: (0.575587, 0.562391), 23: (0.327375, 0.607391),
	24: (0.451481, 0.607609), 25: (0.576609, 0.607609), 26: (0.327375, 0.636522), 27: (0.451992, 0.636304),
	28: (0.577120, 0.636522), 29: (0.327886, 0.681087), 30: (0.451992, 0.680870), 31: (0.577630, 0.681304),
	32: (0.328396, 0.709565), 33: (0.452503, 0.709565), 34: (0.577120, 0.710000), 35: (0.328396, 0.754565),
	36: (0.453524, 0.754783), 37: (0.578652, 0.754783), 38: (0.329418, 0.783696), 39: (0.454035, 0.783478),
	40: (0.578652, 0.783478), 41: (0.205567, 0.470978), 42: (0.202503, 0.497609), 43: (0.197906, 0.522935),
	44: (0.192799, 0.549674), 45: (0.189224, 0.574891), 46: (0.125128, 0.314565), 47: (0.152451, 0.362717),
	48: (0.388748, 0.393441), 49: (0.558820, 0.439963), 50: (0.804137, 0.587174), 51: (0.662497, 0.382789),
	52: (0.545965, 0.388261), 53: (0.638917, 0.430870), 54: (0.617467, 0.478478), 55: (0.839122, 0.225652),
	56: (0.804392, 0.310870), 57: (0.766599, 0.358043), 58: (0.727273, 0.403696), 59: (0.689990, 0.452609),
	60: (0.520833, 0.179485), 61: (0.724038, 0.184391), 62: (0.594099, 0.255502), 63: (0.846272, 0.395652),
	64: (0.799285, 0.440652), 65: (0.241062, 0.319130), 66: (0.283453, 0.295978), 67: (0.331971, 0.268261),
	68: (0.304903, 0.341522), 69: (0.353422, 0.328478), 70: (0.419305, 0.270870), 71: (0.437181, 0.320000),
	72: (0.532431, 0.072609), 73: (0.621808, 0.072609), 74: (0.711696, 0.072609), 75: (0.490041, 0.302935),
	76: (0.518641, 0.318587), 77: (0.549285, 0.334891), 78: (0.581461, 0.351848), 79: (0.456588, 0.368261),
	80: (0.260981, 0.245217),
}

GI_POSITIONS = [
	(0.692536, 0.832411), (0.758540, 0.812251), (0.724782, 0.715956), (0.692032, 0.769358),
	(0.221069, 0.770859), (0.152545, 0.812036), (0.187815, 0.715741), (0.217542, 0.831553),
	(0.069410, 0.572264), (0.049760, 0.468678), (0.055806, 0.378173), (0.053790, 0.080066),
	(0.333521, 0.067413), (0.612876, 0.296247), (0.509082, 0.250995), (0.918745, 0.075580),
	(0.880611, 0.448527), (0.882427, 0.536256), (0.485333, 0.109459), (0.574609, 0.108373),
	(0.664522, 0.108916), (0.755074, 0.108373),
]


def _apply_input_spatial(definition: dict[str, object]) -> None:
	for device in definition["inputs"]:  # type: ignore[index]
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", SAM_REFERENCE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in FLIPPER_BUTTON_ADDRESSES:
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif address in TROUGH_POSITIONS:
			_located(device, "sensor", TROUGH_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE, VPX_SOURCE)
			device["roles"] = [*(device.get("roles") or []), "internal.trough"]
			if address == 22:
				_append_note(device, "The exact VPX exposes Drain and BallRelease but no SW18-SW22 contact objects. This point is an ordered trough-region projection between those direct anchors, with practical uncertainty of about plus or minus 0.03 normalized in both axes; it is not copied from a perspective drawing.")
		elif address in EOS_POSITIONS:
			_located(device, "sensor", EOS_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
			_append_note(device, "The normally-closed EOS contact has no standalone VPX render object; this is a disclosed projection to the exact lower-flipper assembly center, not a cabinet control.")
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE)
		elif group == "pinmame.input.switch" and (address in {15, 16, 65, 66, 67, 68, 69} or address <= 0):
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"24 input {group} {address} has no reviewed spatial disposition")
		if address == 48 and device["spatial"]["status"] == "validated":  # type: ignore[index]
			_append_note(device, "No direct switch leaf is present; the point is the exact Suitcase primitive assembly/home marker and is a shared-assembly projection for the home contact.")


def _apply_output_spatial(definition: dict[str, object]) -> None:
	for device in definition["outputs"]:  # type: ignore[index]
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif (group, address) == ("pinmame.output.solenoid", 8):
			device["roles"] = ["cabinet.shaker"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif (group, address) == ("pinmame.output.solenoid", 24):
			device["roles"] = ["cabinet.coin-meter"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in OUTPUT_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			_located(device, role, OUTPUT_POSITIONS[address], TABLE_SOURCE, MANUAL_SOURCE, VPX_SOURCE)
			if address in FLASHER_QUANTITIES:
				device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address in {19, 20, 31}:
				_append_note(device, "The VPX flasher helper objects are synchronized render layers for this one addressed physical flasher circuit; the quantity is the physical Stern inventory count, not the number of VPX Light objects.")
			if address in {21, 23, 25, 30}:
				_append_note(device, "This is a shared moving Suitcase assembly anchor from the exact VPX Primitive.Suitcase position. Q21/Q23/Q25/Q30 are separate physical stepper drive positions, not four independent playfield locations; phase order remains explicitly unresolved in the mechanism knowledge.")
		elif group == "pinmame.output.lamp" and address in {1, 2}:
			device["roles"] = ["cabinet.start" if address == 1 else "cabinet.tournament"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", [LAMP_POSITIONS[address]], TABLE_SOURCE, MANUAL_SOURCE)
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.gi" and address == 0:
			_located(device, "emitter", GI_POSITIONS, TABLE_SOURCE, MANUAL_SOURCE)
			device.setdefault("physical", {})["quantity"] = len(GI_POSITIONS)
			_append_note(device, "The 40 exact VPX GI Light objects were reconciled to 22 physical GI anchors: each broad odd GI_n object and its localized even GI_n helper are one synchronized socket, and the four GI_LaneGuide objects are independent anchors. This explicitly collapses render helpers rather than claiming 40 physical lamps.")
		else:
			raise ValueError(f"24 output {group} {address} ({kind}) has no reviewed spatial disposition")


def apply_spatial(definition: dict[str, object]) -> None:
	definition["schema_version"] = 2
	definition["sources"].extend([TABLE_SOURCE_RECORD, EMBEDDED_SCRIPT_SOURCE_RECORD])  # type: ignore[index]
	_apply_input_spatial(definition)
	_apply_output_spatial(definition)
	for display in definition["displays"]:  # type: ignore[index]
		display["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": _provenance(CORE_SOURCE, MANUAL_SOURCE)}


def _partialize(definition: dict[str, object]) -> None:
	"""Make uncertainty visible without throwing away reviewed spatial evidence."""
	definition["coverage"]["status"] = "partial"  # type: ignore[index]
	definition["coverage"]["missing"] = [  # type: ignore[index]
		"input_semantics", "output_semantics", "mechanism_behavior", "recreation_notes", "spatial_placement", "unresolved_conflicts",
	]
	dimensions = definition["coverage"]["dimensions"]  # type: ignore[index]
	dimensions["semantic_naming"] = "conflicted"
	dimensions["physical_wiring"] = "conflicted"
	dimensions["mechanisms"] = "conflicted"
	dimensions["recreation_knowledge"] = "conflicted"
	dimensions["spatial_placement"] = "observed"
	definition["knowledge"]["status"] = "partial"  # type: ignore[index]
	definition["conflicts"] = [
		{
			"id": "conflict.suitcase-stepper-phase-order",
			"path": "mechanisms[mechanism.suitcase].behavior",
			"description": "The pinned v2.3.1 script and exact table identify Q21/Q23/Q25/Q30 as the four suitcase stepper drive positions, but no authoritative source establishes their A/B/C/D phase order or individual wiring. The ordinary coil test skips these decoder holes and the suitcase menu capture proves only that a separate test exists. Resolution path: a LibPinMAME gameplay-harness run against a legal twenty4_150 ROM that enters the dedicated Suitcase Motor Test already located in the ROM's auxiliary diagnostic menu and records the assertion order of public outputs 21, 23, 25 and 30 across a full travel cycle, or a continuity check by an owner or operator on an unrestored machine's 511-5072-00 24 V stepper and its 036-5634-11-A7 cable. Unresolved.",
			"source_refs": [VPX_SOURCE, TABLE_SOURCE, MANUAL_SOURCE, RUNTIME_COIL_SOURCE, RUNTIME_SUITCASE_SOURCE],
		},
		{
			"id": "conflict.playfield-contact-construction",
			"path": "inputs[*].physical",
			"description": "The ROM diagnostics establish switch labels and state behavior, and Stern page 43 identifies two suitcase microswitch part types, but the available official material does not establish factory contact construction, normal state, and mounting/seat for every used playfield contact. Used matrix records therefore retain switch_type unknown. Resolution path: a complete official Stern service chart or playfield parts list that names a switch part number per numbered contact, the way the retained partial parts book already does on page 43 for the suitcase's 180-5119-00 and 180-5119-02 microswitches, or a close-up parts survey of an unrestored playfield by an owner recording the fitted contact type at each used address; no ROM diagnostic can supply it, because the Switch Test reports labels and state only. Unresolved.",
			"source_refs": [MANUAL_SOURCE, RUNTIME_SWITCH_LOW_SOURCE, RUNTIME_SWITCH_HIGH_SOURCE, TABLE_SOURCE],
		},
		{
			"id": "conflict.hidden-trough-seats",
			"path": "inputs[pinmame.input.switch 18-22].spatial",
			"description": "The exact VPX exposes Drain and BallRelease but no SW18-SW22 contact objects. The ordered five-point projection preserves controller order and shared-assembly geometry with about +/-0.03 normalized practical uncertainty, but not physical seat coordinates or contact/optic construction. Resolution path: a ball-trough assembly drawing or parts page from a complete Stern 24 book that seats SW18-SW22 individually, an underside photograph of an unrestored machine's trough with the five contacts and their board visible, or a second independently authored known-working 24 recreation that models each trough contact as its own object rather than the Drain/BallRelease pair the retained table exposes. Unresolved.",
			"source_refs": [VPX_SOURCE, TABLE_SOURCE, MANUAL_SOURCE],
		},
		{
			"id": "conflict.lamp-face-and-q27-naming",
			"path": "outputs[pinmame.output.lamp 72-78] and outputs[pinmame.output.solenoid 27]",
			"description": "The ROM diagnostic groups lamps 72-75 as CTU and 76-78 as MOLE without establishing individual face order; the exact script's Q27 description contains the tentative 'under jet?' wording. Bindings and coordinates are retained, but physical naming is not fully authoritative. Resolution path: a photograph of an unrestored 24 playfield showing the CTU and MOLE insert legends in their physical order, taken while the ROM's own Single Lamp Test drives 72-78 one address at a time on that machine so each face can be read off against its address, plus a photograph or complete Stern coil chart locating the Q27 flasher socket; the retained partial parts book carries no lamp-location or flash-lamp drawing, and the captured Single Lamp Test sweep names the two insert groups only. Unresolved.",
			"source_refs": [RUNTIME_LAMP_SOURCE, VPX_SOURCE, TABLE_SOURCE],
		},
	]
	for device in definition["inputs"]:  # type: ignore[index]
		binding = device["binding"]
		if binding["group"] == "pinmame.input.switch" and int(binding["device"]) in (*TROUGH_POSITIONS.keys(), 48, 81, 83):
			if device.get("spatial", {}).get("status") == "validated":
				device["spatial"]["status"] = "observed"

def _knowledge_with_status() -> str:
	return _knowledge().rstrip() + """

## Status decision

This is a schema-v2 **partial**, not author-ready. The direct VPX coordinates, disclosed shared-assembly anchors, ordered trough projection, physical quantities, and controller-to-mechanism records are retained as evidence. The conflicts above remain open because an author still lacks the suitcase phase wiring, complete factory contact construction/normal states, precise hidden trough seats, and a few physical names needed for a full recreation.
"""


def _knowledge() -> str:
	return KNOWLEDGE.rstrip() + """

## Normalized spatial retrofit

Coordinates use the global playfield space: x=0 is left, x=1 is right, y=0 is rear/backglass, and y=1 is front/apron. The exact working VPX was found in the required search order at `L:\\Visual Pinball\\Tables\\24 (Stern 2009).vpx`, copied to the established external VPX cache, and extracted with vpxtool `git:v0.33.3`. Its embedded `twenty4_150` script is retained as an object/callback artifact, while the pinned known-working v2.3.1 script remains the semantic and causality tie-breaker where the older embedded script differs.

Direct centers are used for the exact VPX playfield objects: targets, bumpers, gates, lanes, routes, flippers, slingshots, toy anchors, visible lock, lamps, and flasher helpers. The suitcase, Safe House, Sniper House, Q21/Q23/Q25/Q30 stepper drives, and switch 48 deliberately use shared-assembly anchors. EOS contacts are disclosed projections to exact flipper centers. Trough switches 18-22 are an ordered projection between the exact VPX Drain and BallRelease anchors because the working VPX has no trough-contact objects; the stated uncertainty is practical authoring tolerance, not coordinate precision. No coordinate is inferred from a perspective drawing.

The 40 exact VPX GI objects are not 40 physical sockets: each broad odd `GI_n` and its localized even helper are synchronized render layers for one physical GI position, and four lane-guide objects provide the remaining anchors. The definition therefore carries 22 physical GI anchors. Flasher quantities follow the semantic comments and physical inventory (`Q19` x3, `Q20` x2, `Q26` x3, `Q27` x1, `Q31` x2, `Q32` x3), while synchronized VPX helper objects are not multiplied into hardware.

The older embedded script's visible-lock ordering is superseded by the reviewed v2.3.1 mapping: physical bottom/middle/top contacts 43/44/45 bind to ROM switches 45/44/43. The official Stern parts book, IPDB, and manufacturer evidence remain authoritative for physical multiplicity and custom mechanisms; the SAM reference manual remains limited to shared board topology and connector pinouts. The unresolved suitcase stepper phase order, exact factory contact construction, and precise hidden trough contact seats remain concrete author tasks documented in the base knowledge and mechanism records.

## Spatial evidence

- `vpx-table.stern-24-2009-local`: exact VPX SHA-256 `7e8bf294f3b3dd4bfe53e2727957d000568bc9d079caeed60038ceeb8d1b89f5`, 61,915,136 bytes, retained under the external VPX source cache; extracted object packet and candidate map are retained under the external review-artifact cache.
- `vpx.stern-24-embedded-2.0.1`: extracted script SHA-256 `be3a0e0e96df6d232fa1fa99110e63781abdca5484a1b97de75de0fd1760135a`; it is an older embedded artifact and does not override the pinned semantic v2.3.1 script.
- The geometry source search stopped after the exact table was found in `L:\\Visual Pinball\\Tables`; the archive folder and public VPU/VPF fallback were not needed.
"""


def _refuse_nonidentical(path: Path, generated: bytes, label: str) -> None:
	if path.exists() and path.read_bytes() != generated:
		raise FileExistsError(f"Refusing to overwrite existing reviewed {label}: {path}")


def demote() -> None:
	definition = build()
	apply_spatial(definition)
	_partialize(definition)
	definition_bytes = canonical_bytes(definition)
	knowledge_bytes = _knowledge_with_status().encode("utf-8")
	if AUTHOR_READY_PATH.exists():
		raise FileExistsError(f"Refusing to replace existing author-ready artifact: {AUTHOR_READY_PATH}")
	# Preflight every target before writing any of them. Existing reviewed partial
	# and knowledge artifacts are accepted only when this run reproduces bytes.
	_refuse_nonidentical(PARTIAL_PATH, definition_bytes, "partial definition")
	_refuse_nonidentical(KNOWLEDGE_PATH, knowledge_bytes, "knowledge")
	write_json(PARTIAL_PATH, definition)
	write_text(KNOWLEDGE_PATH, knowledge_bytes.decode("utf-8"))


if __name__ == "__main__":
	demote()
