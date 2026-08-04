"""Promote the exact physical Stern Spider-Man (2007) definition.

The retained Spider-Man_3.0.vpx is the matching original-machine table.  Its
script supplies runtime causality and its extracted object geometry supplies
direct centers.  The Stern manual supplies physical inventory, multiplicity,
hidden assembly construction, and GI/lamp maps.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/spider-man-2007.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/spider-man-2007.json"
# The partial is removed on promotion; this tracked, byte-stable canonical seed
# keeps recreation safe after the promoting commit no longer contains that path.
SEED_PATH = ROOT / "tools/seeds/stern/spider-man-2007.json"

TABLE_SOURCE = "vpx-table.spider-man-3.0"
SCRIPT_SOURCE = "vpx.spider-man-3.0"
SIDECAR_SCRIPT_SOURCE = "vpx-sidecar.spider-man-3.0"
MANUAL_SOURCE = "manual.spider-man.2007-service"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"

TABLE_SHA256 = "97a0a94e122ab070bd98300b191d5c6e58c255dc285a846f4f52d9ff3ffa7c47"
EMBEDDED_SCRIPT_SHA256 = "ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128"
SIDECAR_SCRIPT_SHA256 = "cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237"
VPXTOOL_VERSION = "git:v0.33.3"
EXTERNAL_SOURCE_URI = "external:pinmame-vpx-sources/stern/spider-man-2007/source"

TABLE_SOURCE_RECORD: dict[str, object] = {
	"attribution": "Spider-Man_3.0.vpx table authors; retained exact working table",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": (
		"Spider-Man_3.0.vpx (62,373,888 bytes), ROM sman_261 family; exact first-tier "
		"table retained and extracted with vpxtool git:v0.33.3. Its embedded Script "
		"stream hashes to ce456682b9161116b167ff7c70095d986901e2c226aa5e48a0ee7e572374d128. "
		"Playfield bounds "
		"left=0, top=0, right=952, bottom=2115. Direct centers and collections were "
		"reviewed against Stern manual PDF pages 6, 8-11, 68-69, 85, 91-100, and 118-121."
	),
	"original_filename": "Spider-Man_3.0.vpx",
	"rights": "NOASSERTION",
	"sha256": TABLE_SHA256,
	"uri": f"{EXTERNAL_SOURCE_URI}/Spider-Man_3.0.vpx",
}


EMBEDDED_SCRIPT_SOURCE_RECORD: dict[str, object] = {
	"attribution": "Spider-Man_3.0.vpx table authors; embedded Script stream",
	"id": SCRIPT_SOURCE,
	"kind": "vpx_script",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": (
		"Embedded Script stream freshly extracted from the exact retained Spider-Man_3.0.vpx "
		f"(table SHA-256 {TABLE_SHA256}) with vpxtool {VPXTOOL_VERSION}; embedded script "
		f"SHA-256 {EMBEDDED_SCRIPT_SHA256}. This paired embedded script is the causality "
		"authority; switch 85/EOS polarity remains manual physical-wiring evidence because "
		"the script does not assert that switch."
	),
	"sha256": EMBEDDED_SCRIPT_SHA256,
	"uri": f"{EXTERNAL_SOURCE_URI}/Spider-Man_3.0.vpx",
}


SIDECAR_SCRIPT_SOURCE_RECORD: dict[str, object] = {
	"attribution": "Spider-Man_3.0.vbs table authors and vpxtable_scripts contributors",
	"id": SIDECAR_SCRIPT_SOURCE,
	"kind": "vpx_script",
	"license": "NOASSERTION",
	"locator": (
		f"Secondary/corroborating sidecar Spider-Man_3.0.vbs, SHA-256 {SIDECAR_SCRIPT_SHA256}, "
		"retained beside the VPX but not paired as its authoritative script. It declares "
		"NoUpperRightFlipper and NoUpperLeftFlipper and Const UseSolenoids = 2; the paired "
		"embedded Script stream instead omits both declarations and uses Const UseSolenoids = 1. "
		"It also contains sidecar-only cvpmSaucer exit-variance settings and later audio/rolling "
		"helper changes. No canonical causal assertion references this sidecar."
	),
	"revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e",
	"sha256": SIDECAR_SCRIPT_SHA256,
	"uri": f"{EXTERNAL_SOURCE_URI}/Spider-Man_3.0.vbs",
}


def _p(*refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(refs)}


def _located(
	device: dict[str, object],
	role: str,
	positions: list[tuple[float, float]] | list[tuple[str, float, float]],
	source_refs: tuple[str, ...],
) -> None:
	placements: list[dict[str, object]] = []
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
			"provenance": _p(*source_refs),
		})
	device["spatial"] = {"status": "validated", "placements": placements}


def _na(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _p(*source_refs)}


# Centers from the retained table's Wall, Trigger, Kicker, Spinner, Flipper,
# and Primitive objects, normalized by the exact 952 x 2115 VPX bounds.  The
# trough sequence is the manual's under-apron assembly projection: cvpmTrough
# exposes switches 18-21 only as logical positions, while the manual resolves
# the distinct SW22 opto board and the physical order.
INPUT_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.138028, 0.582658)], 2: [(0.140301, 0.557399)], 3: [(0.142894, 0.531917)],
	4: [(0.145811, 0.506891)], 5: [(0.148405, 0.481268)], 6: [(0.271422, 0.392656)],
	7: [(0.169544, 0.410954)], 8: [(0.063550, 0.155792)],
	9: [(0.442017, 0.318489)], 10: [(0.500630, 0.319680)], 11: [(0.558421, 0.320720)],
	12: [(0.421551, 0.216664)], 13: [(0.551265, 0.216422)], 14: [(0.095156, 0.613533)],
	18: [(0.560000, 0.940000)], 19: [(0.635000, 0.922000)], 20: [(0.710000, 0.904000)],
	21: [(0.785000, 0.886000)], 22: [(0.840000, 0.870000)],
	23: [(0.937040, 0.884368)], 24: [(0.060924, 0.762064)], 25: [(0.132222, 0.742553)],
	26: [(0.227998, 0.728366)], 27: [(0.675814, 0.728070)], 28: [(0.771928, 0.741430)],
	29: [(0.844407, 0.761170)], 30: [(0.630252, 0.161466)], 31: [(0.824842, 0.156619)],
	32: [(0.744748, 0.240898)], 33: [(0.627363, 0.087123)], 34: [(0.716255, 0.083570)],
	35: [(0.805804, 0.082270)], 36: [(0.792797, 0.286307)], 37: [(0.938813, 0.097289)],
	38: [(0.938813, 0.166083)], 39: [(0.788012, 0.539657)], 40: [(0.782694, 0.566182)],
	41: [(0.777048, 0.591548)], 42: [(0.493960, 0.202600)], 43: [(0.139673, 0.094164)],
	44: [(0.633403, 0.241608)], 45: [(0.940126, 0.189835)], 46: [(0.871586, 0.563593)],
	47: [(0.317752, 0.214657)], 48: [(0.050158, 0.287234)],
	49: [(0.501990, 0.312554)], 50: [(0.501990, 0.312554)],
	53: [(0.505485, 0.151773)], 54: [(0.505485, 0.151773)],
	57: [(0.764706, 0.315258)], 58: [(0.764706, 0.315258)], 59: [(0.487658, 0.121444)],
	63: [(0.755252, 0.349291)], 81: [(0.621301, 0.845924)], 83: [(0.289980, 0.846515)],
	85: [(0.855358, 0.460841)],
}

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "cabinet.flipper.button", 84: "cabinet.flipper.button", 86: "cabinet.flipper.button",
	-7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
}

# Direct physical output/effect centers or explicit manual assembly anchors.
SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.856749, 0.864243)], 2: [(0.937960, 0.971572)], 3: [(0.715861, 0.394799)],
	4: [(0.792797, 0.286307)], 5: [(0.764706, 0.315258)], 7: [(0.579549, 0.042961)],
	8: [(0.866752, 0.041624)], 9: [(0.630252, 0.161466)], 10: [(0.824842, 0.156619)],
	11: [(0.744748, 0.240898)], 12: [(0.487658, 0.121444)], 13: [(0.505485, 0.151773)],
	14: [(0.855358, 0.460841)], 15: [(0.289980, 0.846515)], 16: [(0.621301, 0.845924)],
	17: [(0.227998, 0.728366)], 18: [(0.675814, 0.728070)], 19: [(0.158633, 0.564880)],
	20: [(0.501990, 0.312554)], 21: [(0.541627, 0.180524)], 22: [(0.352488, 0.059662)],
	23: [(0.609638, 0.203251), (0.357931, 0.135461)],
	25: [(0.296351, 0.039657), (0.148897, 0.066785)], 26: [(0.488905, 0.216992)],
	27: [(0.505485, 0.151773)],
	28: [(0.066000, 0.432000), (0.066000, 0.577000)],
	29: [(0.098214, 0.000000)], 30: [(0.877626, 0.000000)],
	31: [(0.630252, 0.161466), (0.824842, 0.156619), (0.744748, 0.240898)],
}

LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	3: [(0.453388, 0.852246)], 4: [(0.452009, 0.651448)], 5: [(0.516085, 0.679374)],
	6: [(0.593750, 0.697784)], 7: [(0.556263, 0.733274)], 8: [(0.543330, 0.771474)],
	9: [(0.450368, 0.765455)], 10: [(0.364627, 0.771868)], 11: [(0.347886, 0.733688)],
	12: [(0.311187, 0.697311)], 13: [(0.388721, 0.679019)], 14: [(0.450827, 0.718647)],
	15: [(0.874606, 0.347340)], 16: [(0.898897, 0.296040)], 17: [(0.207543, 0.478064)],
	18: [(0.205154, 0.504755)], 19: [(0.202882, 0.532113)], 20: [(0.200020, 0.559406)],
	21: [(0.197151, 0.586850)], 22: [(0.293330, 0.498050)], 23: [(0.289916, 0.531058)],
	24: [(0.287290, 0.563800)], 25: [(0.074678, 0.209323)], 26: [(0.092732, 0.260949)],
	27: [(0.117680, 0.313017)], 28: [(0.296251, 0.423330)], 29: [(0.397584, 0.425887)],
	30: [(0.415638, 0.478457)], 31: [(0.434480, 0.530851)], 32: [(0.193244, 0.442479)],
	33: [(0.568934, 0.459634)], 34: [(0.537881, 0.511200)], 35: [(0.508666, 0.564657)],
	36: [(0.676405, 0.457240)], 37: [(0.636620, 0.509131)], 38: [(0.610327, 0.544873)],
	39: [(0.585183, 0.578531)], 40: [(0.560301, 0.611835)], 41: [(0.062172, 0.688918)],
	42: [(0.135964, 0.676803)], 43: [(0.772059, 0.675236)], 44: [(0.845588, 0.686229)],
	45: [(0.392791, 0.380290)], 46: [(0.464942, 0.400355)], 47: [(0.544315, 0.422134)],
	48: [(0.710150, 0.558540)], 49: [(0.436417, 0.254713)], 50: [(0.486903, 0.219046)],
	51: [(0.537520, 0.254713)], 52: [(0.441242, 0.352423)], 53: [(0.495536, 0.353664)],
	54: [(0.552849, 0.355024)], 57: [(0.628676, 0.045686)], 58: [(0.717371, 0.043292)],
	59: [(0.806460, 0.041253)], 60: [(0.630515, 0.161348)], 61: [(0.825893, 0.156856)],
	62: [(0.742910, 0.241726)], 63: [(0.702994, 0.586052)], 64: [(0.696264, 0.613933)],
	65: [(0.322348, 0.458806)],
	66: [(0.258264, 0.000000)], 67: [(0.257643, 0.000000)], 68: [(0.256709, 0.000000)],
	69: [(0.600572, 0.000000)], 70: [(0.601396, 0.000000)], 71: [(0.601396, 0.000000)],
	72: [(0.872866, 0.508850)], 74: [(0.419687, 0.232565)], 75: [(0.246717, 0.252778)],
	76: [(0.172138, 0.669090)], 77: [(0.855830, 0.418203)], 78: [(0.916886, 0.243913)],
}

GI_POSITIONS: list[tuple[str, float, float]] = [
	("brown.01", 0.220561, 0.818672), ("brown.02", 0.153738, 0.798963),
	("brown.03", 0.209346, 0.752905), ("brown.04", 0.184346, 0.722822),
	("brown.05", 0.044159, 0.608817), ("brown.06", 0.053738, 0.547095),
	("brown.07", 0.107944, 0.459544), ("brown.08", 0.230374, 0.366494),
	("yellow.01", 0.693692, 0.823755), ("yellow.02", 0.759112, 0.805083),
	("yellow.03", 0.699533, 0.754772), ("yellow.04", 0.726402, 0.723133),
	("yellow.05", 0.833879, 0.564419), ("yellow.06", 0.689252, 0.268672),
	("yellow.07", 0.656542, 0.221992), ("yellow.08", 0.684346, 0.085166),
	("yellow.09", 0.592056, 0.082573), ("yellow.10", 0.766355, 0.080913),
	("yellow.11", 0.845561, 0.077905),
	("violet.01", 0.050000, 0.338589), ("violet.02", 0.044159, 0.275311),
	("violet.03", 0.178738, 0.249378), ("violet.04", 0.248131, 0.251245),
	("violet.05", 0.377103, 0.207573), ("violet.06", 0.228738, 0.200622),
	("violet.07", 0.150000, 0.181535), ("violet.08", 0.367523, 0.156846),
	("violet.09", 0.215421, 0.149689), ("violet.10", 0.061215, 0.039938),
	("violet.11", 0.226636, 0.023029), ("violet.12", 0.378738, 0.017946),
	("violet.13", 0.478972, 0.016909),
	("green.01", 0.090187, 0.000000), ("green.02", 0.181075, 0.000000),
	("green.03", 0.272430, 0.000000), ("green.04", 0.363551, 0.000000),
	("green.05", 0.455140, 0.000000), ("green.06", 0.542056, 0.000000),
	("green.07", 0.632243, 0.000000), ("green.08", 0.724533, 0.000000),
	("green.09", 0.815888, 0.000000), ("green.10", 0.907009, 0.000000),
]


def apply_spatial(definition: dict[str, object]) -> None:
	located_sources = (TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	for device in definition["inputs"]:
		device.pop("spatial", None)
		binding = device["binding"]
		group = str(binding["group"])
		address = int(binding["device"])
		if group == "pinmame.input.dip":
			_na(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_na(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], located_sources)
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			refs = (MANUAL_SOURCE, SCRIPT_SOURCE) if address == 86 else (MANUAL_SOURCE,)
			_na(device, "cabinet_or_service", *refs)
		else:
			raise ValueError(f"Spider-Man input {group} {address} has no spatial disposition")
		if group == "pinmame.input.switch" and address in {1, 2, 3, 4, 5}:
			device.setdefault("physical", {}).update({"quantity": 1, "location": "Green Goblin five-opto ramp assembly"})
		if group == "pinmame.input.switch" and address in {18, 19, 20, 21, 22}:
			device.setdefault("physical", {}).update({
				"quantity": 1,
				"location": "Under-apron 4-ball trough assembly 500-6318-24-ND",
				"notes": "Switches 18-21 are the cvpmTrough ball-position switches in table order; SW22 is the separate trough-jam opto shown on manual page 85. The normalized points are the documented assembly projection along the apron edge because no physical switch-center objects exist in the VPX.",
			})
		if group == "pinmame.input.switch" and address in {49, 50}:
			device.setdefault("physical", {}).update({"quantity": 1, "location": "Motorized Sandman 3-bank assembly 500-7056-00 / 500-7058-00"})
		if group == "pinmame.input.switch" and address in {53, 54}:
			device.setdefault("physical", {}).update({"quantity": 1, "location": "Sandman motorized gate assembly 500-7061-00"})
		if group == "pinmame.input.switch" and address in {57, 58}:
			device.setdefault("physical", {}).update({"quantity": 1, "location": "Doc Ock motorized gate assembly 500-7061-00"})
		if group == "pinmame.input.switch" and address == 85:
			switch_type = device.setdefault("physical", {}).get("switch_type", "leaf")
			device["physical"] = {
				"notes": "The Stern switch matrix calls D16 the upper-right flipper end-of-stroke contact and the manual establishes its normally-closed physical wiring. The embedded script does not assert switch 85; the exact VPX RightFlipper2 center is used only as the disclosed assembly projection because the table has no separate EOS object.",
				"location": "Upper-right flipper EOS D16",
				"quantity": 1,
				"switch_type": switch_type,
			}
		if group == "pinmame.input.switch" and address == 86:
			switch_type = device.setdefault("physical", {}).get("switch_type", "button")
			device["physical"] = {
				"notes": "The Stern switch matrix identifies D15 as the upper-right flipper button. The exact VPX embedded script asserts switch 86 from RightFlipperKey and registers Q14 through solURFlipper; this is cabinet hardware and intentionally has no playfield coordinate.",
				"location": "Upper-right flipper cabinet button D15",
				"quantity": 1,
				"switch_type": switch_type,
			}

	for device in definition["outputs"]:
		device.pop("spatial", None)
		binding = device["binding"]
		group = str(binding["group"])
		address = int(binding["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_na(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			_na(device, "virtual", CORE_SOURCE)
		elif group == "pinmame.output.lamp" and address in {1, 2}:
			device["roles"] = [{1: "cabinet.start", 2: "cabinet.tournament"}[address]]
			_na(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 19:
			physical = device.setdefault("physical", {})
			physical.update({
				"quantity": 1,
				"location": "Green Goblin assembly 511-5058-00",
				"notes": "Q19 is the Green Goblin motor/actuator in the Stern coil chart. The table's FlasherGoblin render helper is not counted as a second physical effect; the normalized effect point is the exact Goblin primitive anchor.",
			})
			_located(device, "effect", SOLENOID_POSITIONS[address], (TABLE_SOURCE, MANUAL_SOURCE, SCRIPT_SOURCE))
		elif (group, address) in {
			("physical.output.ticket", 33), ("physical.output.ticket", 34), ("physical.output.ticket", 35),
		}:
			device["roles"] = ["service.ticket"]
			_na(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 6:
			device["roles"] = ["cabinet.shaker"]
			_na(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 24:
			device["roles"] = ["cabinet.knocker_or_coin_meter"]
			_na(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			placement_sources = (MANUAL_SOURCE,) if address == 23 else (TABLE_SOURCE, MANUAL_SOURCE, SCRIPT_SOURCE)
			_located(device, role, SOLENOID_POSITIONS[address], placement_sources)
			physical = device.setdefault("physical", {})
			quantity = {23: 2, 25: 2, 28: 2, 31: 3}.get(address, 1)
			physical.setdefault("quantity", quantity)
			if address == 5:
				physical.setdefault("location", "Doc Ock motorized gate assembly 500-7061-00")
				physical.setdefault("notes", "Q5 is the 24 VAC motor/relay that moves the Doc Ock gate; the exact table uses the Octopus primitive as the shared assembly anchor for its two limit switches.")
			elif address == 13:
				physical.setdefault("location", "Sandman motorized gate assembly 500-7061-00")
				physical.setdefault("notes", "Q13 is the 24 VAC motor/relay that moves the Sandman gate; the exact table uses the Sandman primitive as the shared assembly anchor for its two limit switches.")
			elif address == 20:
				physical.setdefault("location", "Motorized Sandman 3-bank assembly 500-7056-00 / 500-7058-00")
			elif address == 23:
				physical.setdefault("location", "Two Sandman flasher bulbs shown as Q23 (X2) on manual page 11")
				physical.setdefault("notes", "The two Q23 coordinates are disclosed normalized projections from the two manual page 11 callouts. No exact F23 socket objects exist in the retained VPX; Illumina/Fotocellula objects are render helpers and are not promoted as physical bulbs.")
			elif address == 25:
				physical.setdefault("location", "Two Venom flasher bulbs shown as Q25 (X2) on manual page 11")
			elif address == 27:
				physical.setdefault("location", "Sandman dome assembly")
				physical.setdefault("notes", "The table's broad FlashGiallo helper is outside the playfield bounds; this is the normalized Sandman assembly anchor for the manual's single Q27 dome flasher.")
			elif address == 28:
				physical.setdefault("location", "Two Green Goblin flasher bulbs in assembly 511-5058-00")
				physical.setdefault("notes", "Manual page 11 marks two distinct Q28 bulbs in the Green Goblin underside assembly. Their two normalized points are disclosed projections from the two manual callouts (x≈0.066, y≈0.432 and 0.577); the exact VPX FlasherGoblin overlay and Primitive.Goblin toy anchor corroborate the local assembly but are not counted as extra sockets.")
			elif address in {29, 30}:
				physical.setdefault("location", "Rear back-panel flasher assembly")
				physical.setdefault("notes", f"Manual page 11 identifies Q{address} as the {'left' if address == 29 else 'right'} back-panel flasher. The VPX Flash{'Blu' if address == 29 else 'Rosso'} x anchor is retained and its helper y is explicitly projected to the canonical rear boundary y=0; it is not a playfield-depth placement.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], (TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE))
			device.setdefault("physical", {}).setdefault("quantity", 1)
			if address in range(66, 72):
				device["physical"].update({
					"location": "Rear back panel; y=0 boundary projection",
					"notes": "Manual page 9 identifies 66-68 and 69-71 as back-panel lamps. The x values are the exact table bulbPr3-bulbPr8 anchors; their y=-12 VPX helpers are projected to the canonical rear boundary y=0.",
				})
		elif group == "pinmame.output.gi" and address == 0:
			actual = {circuit: sum(name.startswith(f"{circuit}.") for name, _, _ in GI_POSITIONS) for circuit in ("brown", "yellow", "violet", "green")}
			if actual != {"brown": 8, "yellow": 11, "violet": 13, "green": 10} or len(GI_POSITIONS) != 42:
				raise ValueError(f"Spider-Man GI reconciliation mismatch: {actual!r}")
			_located(device, "emitter", GI_POSITIONS, (MANUAL_SOURCE,))
			device.setdefault("physical", {}).update({
				"quantity": 44,
				"location": "US/non-Euro hardware: 32 playfield bulbs, 10 rear back-panel bulbs, and 2 coin-door bulbs on four fused GI circuits",
				"notes": "Regional scope is explicitly US/non-Euro hardware. Manual page 121 gives brown=8, yellow=11, violet=13, and green=10 rear-panel bulbs plus 2 US coin-door bulbs; Euro hardware has 3 coin-door bulbs and is not represented by this quantity. The 42 playfield/rear placements are normalized to the exact VPX playfield coordinate convention; rear-panel bulbs are projected to y=0 and the two US coin-door bulbs remain quantity-only cabinet hardware. VPX GI collection members and lightmap helpers are synchronized render helpers, not extra physical sockets.",
			})
		else:
			raise ValueError(f"Spider-Man output {group} {address} ({kind}) has no spatial disposition")

	for display in definition["displays"]:
		if display["id"] != "display.dmd":
			raise ValueError(f"Spider-Man display {display['id']} has no spatial disposition")
		_na(display, "cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE)


def _load_base() -> dict[str, object]:
	if PARTIAL_PATH.exists():
		return load_json(PARTIAL_PATH)
	if SEED_PATH.exists():
		return load_json(SEED_PATH)
	raise RuntimeError(
		f"Refusing Spider-Man promotion: neither partial input nor pinned seed exists ({PARTIAL_PATH}, {SEED_PATH})"
	)


def _assert_complete_base(definition: dict[str, object]) -> None:
	"""Reject a partial/edited base rather than promoting by assumption."""
	expected_inputs = {
		*(('pinmame.input.switch', address) for address in range(1, 65)),
		*(('pinmame.input.switch', address) for address in (65, 66, 67, 68, 69, 70, 71, 72, 81, 82, 83, 84, 85, 86, 87, 88)),
		*(('pinmame.input.switch', address) for address in range(-7, 1)),
		*(('pinmame.input.dip', address) for address in range(1, 9)),
	}
	expected_outputs = {
		*(('pinmame.output.solenoid', address) for address in range(1, 34)),
		*(('physical.output.ticket', address) for address in (33, 34, 35)),
		*(('pinmame.output.lamp', address) for address in range(1, 81)),
		('pinmame.output.gi', 0),
	}
	actual_inputs = {(item["binding"]["group"], item["binding"]["device"]) for item in definition.get("inputs", [])}
	actual_outputs = {(item["binding"]["group"], item["binding"]["device"]) for item in definition.get("outputs", [])}
	expected_mechanisms = {
		"mechanism.four-ball-trough", "mechanism.auto-launch", "mechanism.doc-ock-vuk", "mechanism.doc-ock-magnet",
		"mechanism.doc-ock-motorized-gate", "mechanism.sandman-vuk", "mechanism.sandman-motorized-gate",
		"mechanism.sandman-motorized-three-bank", "mechanism.left-control-gate", "mechanism.right-control-gate",
		"mechanism.loop-diverter", "mechanism.lower-left-flipper", "mechanism.lower-right-flipper",
		"mechanism.upper-right-flipper", "mechanism.green-goblin-shake",
	}
	actual_mechanisms = {item.get("id") for item in definition.get("mechanisms", [])}
	if actual_inputs != expected_inputs or actual_outputs != expected_outputs or actual_mechanisms != expected_mechanisms:
		raise RuntimeError(
			"Refusing Spider-Man promotion: base evidence is incomplete "
			f"(inputs={len(actual_inputs)}/{len(expected_inputs)}, outputs={len(actual_outputs)}/{len(expected_outputs)}, "
			f"mechanisms={len(actual_mechanisms)}/{len(expected_mechanisms)})"
		)


def _canonicalize_causality(definition: dict[str, object]) -> dict[str, object]:
	"""Bind semantic claims to the exact table's embedded Script stream."""
	sources = [source for source in definition["sources"] if source.get("id") not in {TABLE_SOURCE, SCRIPT_SOURCE, SIDECAR_SCRIPT_SOURCE}]
	sources.extend([EMBEDDED_SCRIPT_SOURCE_RECORD, SIDECAR_SCRIPT_SOURCE_RECORD, TABLE_SOURCE_RECORD])
	definition["sources"] = sources
	for mechanism in definition["mechanisms"]:
		behavior = str(mechanism.get("behavior", ""))
		behavior = behavior.replace("known-working VPX script", "embedded VPX script extracted from the retained exact table")
		behavior = behavior.replace("working Spider-Man 3.0 VPX script", "embedded Spider-Man 3.0 VPX script extracted from the retained exact table")
		if mechanism["id"] == "mechanism.upper-right-flipper":
			behavior = (
				"The Stern manual identifies D15 as the upper-right flipper button (public switch 86) "
				"and D16 as its normally-closed EOS (public switch 85). The exact table's embedded "
				"script asserts switch 86 from RightFlipperKey and registers ROM output 14 to "
				"solURFlipper/RightFlipper2; it does not assert switch 85. The EOS identity and "
				"normally-closed physical wiring therefore remain manual-authoritative."
			)
		mechanism["behavior"] = behavior
	return definition


def _prepare_definition(definition: dict[str, object]) -> dict[str, object]:
	_assert_complete_base(definition)
	_canonicalize_causality(definition)
	definition["schema_version"] = 2
	definition["machine"]["kind"] = "physical_pinball"
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	return definition


def promote() -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite author-ready canonical definition: {AUTHOR_READY_PATH}")
	definition = _prepare_definition(_load_base())
	write_json(AUTHOR_READY_PATH, definition)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
