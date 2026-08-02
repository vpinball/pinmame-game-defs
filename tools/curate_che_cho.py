from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

CATALOG_SOURCE = "pinmame.catalog.4ec52ff0ac13"
CORE_SOURCE = "pinmame.wpc.che-cho.4ec52ff0ac13"
VPX_SOURCE = "vpx.che-cho.watacaractr.1.0"
PLAYFIELD_SOURCE = "screenshot.che-cho.playfield"
ROM_SOURCE = "rom.che-cho.static"
RUNTIME_SOURCE = "runtime.che-cho.harness"
RELEASE_SOURCE = "release.che-cho.vpu"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def aliases(namespace: str, address: int) -> list[dict[str, str]]:
	return [{"namespace": namespace, "value": str(address)}]


CABINET_SWITCHES: dict[int, tuple[str, str, str]] = {
	1: ("coin-1", "Coin chute 1", "used"),
	2: ("coin-2", "Coin chute 2", "optional"),
	3: ("coin-3", "Coin chute 3", "optional"),
	4: ("coin-4", "Coin chute 4", "optional"),
	5: ("service-enter", "Coin-door Enter button", "used"),
	6: ("service-up", "Coin-door Up button", "used"),
	7: ("service-down", "Coin-door Down button", "used"),
	8: ("service-escape", "Coin-door Escape button", "used"),
}

MATRIX_SWITCHES: dict[int, tuple[str, str]] = {
	11: ("lower-right-flipper-eos", "Lower-right flipper EOS"),
	12: ("lower-left-flipper-eos", "Lower-left and upper-left flipper EOS circuit"),
	13: ("start", "Start button"),
	14: ("tilt", "Tilt"),
	15: ("outhole", "Outhole"),
	16: ("trough-right", "Trough right / eject position"),
	17: ("trough-center", "Trough center"),
	18: ("trough-left", "Trough left"),
	21: ("slam-tilt", "Slam tilt"),
	22: ("coin-door-closed", "Coin-door closed interlock"),
	23: ("ticket-dispenser", "Ticket-dispenser feedback (not installed in the VPX original)"),
	25: ("left-bumper", "Left pop bumper"),
	26: ("right-bumper", "Right pop bumper"),
	27: ("bottom-bumper", "Bottom pop bumper and cul-de-sac contacts"),
	28: ("bottom-eject", "Bottom eject / motorcycle return"),
	31: ("bong-b", "B-O-N-G rollover B"),
	32: ("bong-o", "B-O-N-G rollover O"),
	33: ("bong-n", "B-O-N-G rollover N"),
	34: ("bong-g", "B-O-N-G rollover G"),
	35: ("right-eject", "Right eject"),
	36: ("left-eject", "Left eject / House Party"),
	37: ("left-slingshot", "Left slingshot; also one half of Road Closed"),
	38: ("right-slingshot", "Right slingshot; also one half of Road Closed"),
	41: ("top-cheech", "Top Cheech rollover"),
	42: ("top-and", "Top ampersand rollover"),
	43: ("top-chong", "Top Chong rollover"),
	51: ("and-a-drop", "A-N-D drop target A"),
	52: ("and-n-drop", "A-N-D drop target N"),
	53: ("and-d-drop", "A-N-D drop target D"),
	54: ("the-t-drop", "T-H-E drop target T"),
	55: ("the-h-drop", "T-H-E drop target H"),
	56: ("the-e-drop", "T-H-E drop target E"),
	57: ("pedro-p-target", "P-E-D-R-O stand-up target P"),
	58: ("pedro-e-target", "P-E-D-R-O stand-up target E"),
	61: ("pedro-d-target", "P-E-D-R-O stand-up target D"),
	62: ("pedro-r-target", "P-E-D-R-O stand-up target R"),
	63: ("pedro-o-target", "P-E-D-R-O stand-up target O"),
	64: ("man-m-target", "M-A-N stand-up target M"),
	65: ("man-a-target", "M-A-N stand-up target A"),
	66: ("man-n-target", "M-A-N stand-up target N"),
	67: ("right-road-trip-advance", "Right Road-Trip advance trigger"),
	68: ("left-road-trip-advance", "Left Road-Trip advance trigger"),
	71: ("left-loop", "Left loop rollover"),
	72: ("right-loop", "Right loop rollover"),
	73: ("left-outlane", "Left outlane"),
	74: ("right-outlane", "Right outlane"),
	75: ("shooter-lane", "Shooter lane"),
}

FLIPPER_SWITCHES: dict[int, tuple[str, str, str]] = {
	111: ("dedicated-lower-right-eos", "Dedicated lower-right EOS input", "unused"),
	112: ("lower-right-flipper-button", "Lower-right flipper button", "used"),
	113: ("dedicated-lower-left-eos", "Dedicated lower-left EOS input", "unused"),
	114: ("lower-left-flipper-button", "Lower-left flipper button", "used"),
	115: ("upper-right-eos", "Upper-right flipper EOS input", "unused"),
	116: ("upper-right-flipper-button", "Upper-right flipper button", "unused"),
	117: ("upper-left-eos", "Upper-left flipper EOS input", "unused"),
	118: ("upper-left-flipper-button", "Upper-left flipper button", "unused"),
}

MATRIX_ADDRESSES = [column * 10 + row for column in range(1, 9) for row in range(1, 9)]


def input_device(address: int, identifier: str, label: str, availability: str, source_refs: tuple[str, ...], *, pulse: bool = True, switch_type: str = "microswitch") -> dict[str, object]:
	return {
		"id": f"switch.{identifier}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address},
		"aliases": aliases("pinmame.switch", address),
		"normally_closed": False,
		"pulse": pulse,
		"availability": availability,
		"physical": {"location": label, "switch_type": switch_type},
		"provenance": provenance(*source_refs),
	}


def all_inputs() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address, (identifier, label, availability) in CABINET_SWITCHES.items():
		items.append(input_device(address, identifier, label, availability, (CORE_SOURCE, RUNTIME_SOURCE), pulse=address <= 4, switch_type="button"))
	for address in MATRIX_ADDRESSES:
		if address in MATRIX_SWITCHES:
			identifier, label = MATRIX_SWITCHES[address]
			availability = "unused" if address == 23 else "used"
			pulse = address not in {11, 12, 14, 15, 16, 17, 18, 21, 22, 28, 35, 36, 51, 52, 53, 54, 55, 56, 75}
			switch_type = "tilt" if address in {14, 21} else "button" if address == 13 else "microswitch"
			refs = (CORE_SOURCE, VPX_SOURCE, RUNTIME_SOURCE) if address in {31, 32, 33, 34, 41, 42, 43, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72} else (CORE_SOURCE, VPX_SOURCE)
			items.append(input_device(address, identifier, label, availability, refs, pulse=pulse, switch_type=switch_type))
		else:
			items.append(input_device(address, f"unused-matrix-{address}", f"Unused WPC matrix position {address}", "unused", (CORE_SOURCE, VPX_SOURCE), pulse=True, switch_type="unknown"))
	for address, (identifier, label, availability) in FLIPPER_SWITCHES.items():
		items.append(input_device(address, identifier, label, availability, (CORE_SOURCE, VPX_SOURCE), pulse=False, switch_type="button"))
	for address in range(1, 9):
		items.append({
			"id": f"dip.wpc-option-{address}",
			"label": f"WPC CPU-board configuration bit {address}",
			"kind": "dip_switch",
			"binding": {"group": "pinmame.input.dip", "device": address},
			"aliases": aliases("pinmame.dip", address),
			"availability": "optional",
			"physical": {"location": "CPU board option/country configuration", "switch_type": "dip"},
			"provenance": provenance(CORE_SOURCE),
		})
	return items


SOLENOIDS: dict[int, tuple[str, str, str, str]] = {
	1: ("outhole-to-trough", "Outhole-to-trough eject", "coil", "used"),
	2: ("trough-eject", "Trough eject to shooter lane", "coil", "used"),
	3: ("and-drop-reset", "A-N-D three-target bank reset", "coil", "used"),
	4: ("the-drop-reset", "T-H-E three-target bank reset", "coil", "used"),
	5: ("left-bumper", "Left pop-bumper coil", "coil", "used"),
	6: ("right-bumper", "Right pop-bumper coil", "coil", "used"),
	7: ("knocker", "Cabinet knocker", "coil", "used"),
	8: ("bottom-bumper", "Bottom pop-bumper coil", "coil", "used"),
	9: ("bottom-eject", "Bottom eject coil", "coil", "used"),
	10: ("right-eject", "Right eject coil", "coil", "used"),
	11: ("left-eject", "Left eject coil", "coil", "used"),
	12: ("right-gate", "Right one-way gate actuator", "coil", "used"),
	13: ("left-gate", "Left one-way gate actuator", "coil", "used"),
	15: ("left-slingshot", "Left slingshot coil", "coil", "used"),
	16: ("right-slingshot", "Right slingshot coil", "coil", "used"),
	17: ("flasher-17", "Playfield flasher pair 17", "flasher", "used"),
	18: ("flasher-18", "Playfield flasher pair 18", "flasher", "used"),
	19: ("flasher-19", "Playfield illumination output 19", "flasher", "used"),
	20: ("flasher-20", "Playfield illumination output 20", "flasher", "used"),
	21: ("jade-debbie-flasher", "Jade and Debbie character flashers", "flasher", "used"),
	22: ("chong-jackpot-flasher", "Chong jackpot and bird-cage flashers", "flasher", "used"),
	23: ("checkpoint-plastic-flasher", "Checkpoint and Cheech/Chong plastic flashers", "flasher", "used"),
	24: ("character-spotlights", "Cheech and Chong character spotlights", "flasher", "used"),
	25: ("flasher-25", "Playfield flasher group 25", "flasher", "used"),
	26: ("flasher-26", "Playfield flasher group 26", "flasher", "used"),
	27: ("unbound-flasher-27", "Unbound WPC flasher output 27", "flasher", "unused"),
	28: ("unrendered-flasher-28", "Reserved flasher output 28 with its VPX render binding commented out", "flasher", "unused"),
	29: ("j111-state-29", "J111 auxiliary state output 29", "virtual", "unused"),
	30: ("j111-state-30", "J111 auxiliary state output 30", "virtual", "unused"),
	31: ("game-on", "Game-on state and flipper-enable relay", "relay", "used"),
	34: ("upper-right-flipper", "Generic upper-right flipper callback", "coil", "unused"),
	36: ("upper-left-flipper", "Generic upper-left flipper callback; table drives its upper flipper with output 48 instead", "coil", "unused"),
	46: ("lower-right-flipper", "Lower-right flipper coil callback", "coil", "used"),
	48: ("left-flippers", "Lower-left and upper-left flipper coil callback", "coil", "used"),
}


def all_solenoids() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address in range(1, 51):
		identifier, label, kind, availability = SOLENOIDS.get(address, (f"unused-wpc-position-{address}", f"Unused WPC output position {address}", "virtual", "unused"))
		items.append({
			"id": f"device.{identifier}",
			"label": label,
			"kind": kind,
			"binding": {"group": "pinmame.output.solenoid", "device": address},
			"aliases": aliases("pinmame.solenoid", address),
			"availability": availability,
			"physical": {"location": label, "notes": "This is a virtual-table device; physical cabinet wiring is not applicable."},
			"provenance": provenance(CORE_SOURCE, VPX_SOURCE),
		})
	return items


LAMPS: dict[int, tuple[str, str, str]] = {
	11: ("route-pedros-house", "Road-Trip location: Pedro's House", "used"),
	12: ("route-drive-in", "Road-Trip location: Drive-In Theater", "used"),
	13: ("route-upholstery-factory", "Road-Trip location: Upholstery Factory", "used"),
	14: ("route-hollywood-hotel", "Road-Trip location: Hollywood Hotel", "used"),
	15: ("route-car-wash", "Road-Trip location: Car Wash", "used"),
	16: ("route-police-station", "Road-Trip location: Police Station", "used"),
	17: ("hidden-17", "Hidden off-playfield matrix lamp 17", "unused"),
	18: ("hidden-18", "Hidden off-playfield matrix lamp 18", "unused"),
	21: ("hidden-21", "Hidden off-playfield matrix lamp 21", "unused"),
	22: ("hidden-22", "Hidden off-playfield matrix lamp 22", "unused"),
	23: ("and-a", "A-N-D target insert A", "used"),
	24: ("and-n", "A-N-D target insert N", "used"),
	25: ("and-d", "A-N-D target insert D", "used"),
	26: ("the-t", "T-H-E target insert T", "used"),
	27: ("the-h", "T-H-E target insert H", "used"),
	28: ("the-e", "T-H-E target insert E", "used"),
	31: ("pedro-p", "P-E-D-R-O target insert P", "used"),
	32: ("pedro-e", "P-E-D-R-O target insert E", "used"),
	33: ("pedro-d", "P-E-D-R-O target insert D", "used"),
	34: ("pedro-r", "P-E-D-R-O target insert R", "used"),
	35: ("pedro-o", "P-E-D-R-O target insert O", "used"),
	36: ("man-m", "M-A-N target insert M", "used"),
	37: ("man-a", "M-A-N target insert A", "used"),
	38: ("man-n", "M-A-N target insert N", "used"),
	41: ("bong-b", "B-O-N-G rollover insert B", "used"),
	42: ("bong-o", "B-O-N-G rollover insert O", "used"),
	43: ("bong-n", "B-O-N-G rollover insert N", "used"),
	44: ("bong-g", "B-O-N-G rollover insert G", "used"),
	45: ("left-eject-25k", "Left eject award 25K", "used"),
	46: ("left-eject-50k", "Left eject award 50K", "used"),
	47: ("left-eject-100k", "Left eject award 100K", "used"),
	48: ("left-eject-150k-lock", "Left eject 150K / Lock", "used"),
	51: ("bonus-2x", "Bonus multiplier 2X", "used"),
	52: ("bonus-3x", "Bonus multiplier 3X", "used"),
	53: ("bonus-4x", "Bonus multiplier 4X", "used"),
	54: ("bonus-5x", "Bonus multiplier 5X", "used"),
	55: ("bonus-6x", "Bonus multiplier 6X", "used"),
	56: ("top-cheech", "Top rollover insert Cheech", "used"),
	57: ("top-and", "Top rollover insert ampersand", "used"),
	58: ("top-chong", "Top rollover insert Chong", "used"),
	61: ("right-eject-150k-lock", "Right eject 150K / Lock", "used"),
	62: ("right-eject-pick-up-lines", "Right eject Pick-Up Lines", "used"),
	63: ("right-eject-extra-ball", "Right eject Extra Ball", "used"),
	64: ("right-eject-jackpot", "Right eject Jackpot", "used"),
	65: ("left-3k", "Left 3K award", "used"),
	66: ("left-road-trip-advance", "Left Road-Trip Advance", "used"),
	67: ("right-3k", "Right 3K award", "used"),
	68: ("right-road-trip-advance", "Right Road-Trip Advance", "used"),
	71: ("the-man-50k", "The Man bonus 50K", "used"),
	72: ("the-man-100k", "The Man bonus 100K", "used"),
	73: ("the-man-200k", "The Man bonus 200K", "used"),
	74: ("the-man-300k", "The Man bonus 300K", "used"),
	75: ("the-man-500k", "The Man bonus 500K", "used"),
	76: ("left-drain-extra-ball", "Left drain Extra Ball", "used"),
	77: ("right-drain-extra-ball", "Right drain Extra Ball", "used"),
	78: ("take-a-little-trip", "Take a Little Trip", "used"),
	81: ("left-million", "Left 1 Million When Lit", "used"),
	82: ("right-million", "Right 1 Million When Lit", "used"),
	83: ("hidden-83", "Hidden off-playfield matrix lamp 83", "unused"),
	84: ("hidden-84", "Hidden off-playfield matrix lamp 84", "unused"),
	85: ("route-battle-of-bands", "Road-Trip location: Battle of the Bands", "used"),
	86: ("route-our-lady", "Road-Trip location: Our Lady of 13th Street (ROM: School)", "used"),
	87: ("route-boardwalk", "Road-Trip location: Boardwalk", "used"),
	88: ("route-strawberrys-house", "Road-Trip location: Strawberry's House", "used"),
}


def all_lamps() -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address in MATRIX_ADDRESSES:
		identifier, label, availability = LAMPS[address]
		items.append({
			"id": f"lamp.{identifier}",
			"label": label,
			"kind": "lamp",
			"binding": {"group": "pinmame.output.lamp", "device": address},
			"aliases": aliases("pinmame.lamp", address),
			"availability": availability,
			"physical": {"location": label, "notes": "Matrix address uses WPC column/row notation as returned by ChangedLamps."},
			"provenance": provenance(VPX_SOURCE, PLAYFIELD_SOURCE, RUNTIME_SOURCE, ROM_SOURCE),
		})
	return items


def all_gi() -> list[dict[str, object]]:
	return [{
		"id": f"gi.string-{address}",
		"label": f"WPC GI string {address}; combined by the working table",
		"kind": "gi",
		"binding": {"group": "pinmame.output.gi", "device": address},
		"aliases": aliases("pinmame.gi", address),
		"availability": "used",
		"physical": {"location": "General illumination", "notes": "The proven VPX GI callback intentionally applies every one of the five controller channels to the same aGiLights collection."},
		"provenance": provenance(CORE_SOURCE, VPX_SOURCE, RUNTIME_SOURCE),
	} for address in range(5)]


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *source_refs: str) -> dict[str, object]:
	return {"id": f"mechanism.{identifier}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*source_refs)}


def mechanisms() -> list[dict[str, object]]:
	return [
		mechanism("trough", "Three-ball trough and outhole", "kicker", ["device.outhole-to-trough", "device.trough-eject"], ["switch.outhole", "switch.trough-right", "switch.trough-center", "switch.trough-left"], "Initialize three balls on switches 16, 17, and 18. A drain occupies outhole switch 15; output 1 transfers it into the left end of the trough. Output 2 ejects the rightmost ball toward the manual shooter lane at angle 45 and nominal force 7.", VPX_SOURCE, RUNTIME_SOURCE),
		mechanism("and-drop-bank", "A-N-D three-target drop bank", "drop_target_bank", ["device.and-drop-reset"], ["switch.and-a-drop", "switch.and-n-drop", "switch.and-d-drop"], "Targets 51-53 remain down/active until output 3 raises the entire top bank. Their matching progress lamps are 23-25.", VPX_SOURCE, RUNTIME_SOURCE),
		mechanism("the-drop-bank", "T-H-E three-target drop bank", "drop_target_bank", ["device.the-drop-reset"], ["switch.the-t-drop", "switch.the-h-drop", "switch.the-e-drop"], "Targets 54-56 remain down/active until output 4 raises the entire middle bank. Their matching progress lamps are 26-28.", VPX_SOURCE, RUNTIME_SOURCE),
		mechanism("left-eject", "Left eject / House Party", "kicker", ["device.left-eject"], ["switch.left-eject"], "Switch 36 captures one ball. Output 11 ejects at angle 90, force 20, angle variation 3, and force variation 3.", VPX_SOURCE),
		mechanism("right-eject", "Right eject", "kicker", ["device.right-eject"], ["switch.right-eject"], "Switch 35 captures one ball. Output 10 ejects at angle 0, force 27, angle variation 3, and force variation 3.", VPX_SOURCE),
		mechanism("bottom-eject", "Bottom eject and motorcycle return", "kicker", ["device.bottom-eject"], ["switch.bottom-eject"], "Switch 28 captures one ball. Output 9 ejects at angle 243, force 24, Z offset 1.5, angle variation 3, and force variation 3. Releasing switch 28 starts the motorcycle cop's return animation.", VPX_SOURCE),
		mechanism("pop-bumpers", "Three pop bumpers", "kicker", ["device.left-bumper", "device.right-bumper", "device.bottom-bumper"], ["switch.left-bumper", "switch.right-bumper", "switch.bottom-bumper"], "Switches 25, 26, and 27 operate left, right, and bottom bumpers through outputs 5, 6, and 8. Every bumper hit also shakes the decorative clown ball; script-only cul-de-sac contacts pulse switch 27.", CORE_SOURCE, VPX_SOURCE),
		mechanism("slingshots", "Left and right slingshots", "kicker", ["device.left-slingshot", "device.right-slingshot"], ["switch.left-slingshot", "switch.right-slingshot"], "Switch 37 drives output 15 and switch 38 drives output 16. The upper right sling uses the right contact/output. The Road Closed target is script-only and deliberately pulses both 37 and 38 together.", CORE_SOURCE, VPX_SOURCE),
		mechanism("road-closed", "Road Closed self-resetting target", "drop_target_bank", [], ["switch.left-slingshot", "switch.right-slingshot"], "This custom physical-looking target has no dedicated PinMAME input or reset output. A hit pulses both sling switches 37/38, plays its effects, enables its timer, and the timer immediately restores IsDropped to zero with a reset sound.", VPX_SOURCE),
		mechanism("gates", "Left and right one-way gates", "gate", ["device.left-gate", "device.right-gate"], [], "Output 13 opens the left gate and output 12 opens the right gate; their disabled states close the gates. Gate-hit sounds are local and add no controller inputs.", VPX_SOURCE),
		mechanism("flippers", "Three-flipper playfield", "other", ["device.left-flippers", "device.lower-right-flipper"], ["switch.lower-left-flipper-button", "switch.lower-right-flipper-button", "switch.lower-left-flipper-eos", "switch.lower-right-flipper-eos"], "Generic output 48 moves both the lower-left and upper-left flippers together; output 46 moves the lower-right flipper. Cabinet buttons are 114 left and 112 right. The pre-Fliptronics EOS positions are matrix switches 12 left and 11 right. Game-on output 31 gates flipper availability.", CORE_SOURCE, VPX_SOURCE, RUNTIME_SOURCE),
		mechanism("manual-shooter", "Manual shooter", "other", [], ["switch.shooter-lane"], "Switch 75 reports the ball in the shooter lane. There is no launch coil; the author must provide a manual plunger and tune the launch path into the table geometry.", CORE_SOURCE, VPX_SOURCE),
		mechanism("motorcycle-cop", "Motorcycle cop animation", "motorized", [], [], "A script-local trigger moves the cop from 0 to 725 at 5 units per 10 ms tick. It waits at the eject, then switch 28 UnHit reverses direction at 2.5 units per tick until position 0. No PinMAME motor, position switch, or output exists.", VPX_SOURCE),
		mechanism("van-transfer", "Van hidden-ball transfer", "toy", [], [], "VanKickerEnter and the associated hidden kickers transfer a ball locally through the van animation. They do not expose PinMAME switches or outputs and must not be invented as controller addresses.", VPX_SOURCE),
		mechanism("decorative-animations", "Character, bird, head, projector, and clown animations", "toy", [], ["switch.and-n-drop", "switch.pedro-d-target", "switch.man-m-target", "switch.man-a-target", "switch.man-n-target"], "Target-hit counters and random branches drive local spotlights, voices, Cheech/Chong head turns, the caged bird, projector art, and character illumination. The clown captive decoration shakes on bumper hits. These animations use script timers and standard lamp/flasher channels but add no controller devices.", VPX_SOURCE),
	]


def relationships() -> list[dict[str, object]]:
	pairs = [
		("left-bumper", "switch.left-bumper", "device.left-bumper"),
		("right-bumper", "switch.right-bumper", "device.right-bumper"),
		("bottom-bumper", "switch.bottom-bumper", "device.bottom-bumper"),
		("left-sling", "switch.left-slingshot", "device.left-slingshot"),
		("right-sling", "switch.right-slingshot", "device.right-slingshot"),
		("bottom-eject", "switch.bottom-eject", "device.bottom-eject"),
		("right-eject", "switch.right-eject", "device.right-eject"),
		("left-eject", "switch.left-eject", "device.left-eject"),
	]
	return [{"id": f"relationship.{identifier}", "kind": "pulse", "source": source, "destination": destination, "provenance": provenance(VPX_SOURCE)} for identifier, source, destination in pairs] + [
		{"id": "relationship.left-flippers", "kind": "relay_gated", "source": "switch.lower-left-flipper-button", "destination": "device.left-flippers", "provenance": provenance(CORE_SOURCE, VPX_SOURCE)},
		{"id": "relationship.right-flipper", "kind": "relay_gated", "source": "switch.lower-right-flipper-button", "destination": "device.lower-right-flipper", "provenance": provenance(CORE_SOURCE, VPX_SOURCE)},
	]


SOURCES: list[dict[str, object]] = [
	{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames entry che_cho", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sims/wpc/full/hd.c; src/wpc/wpc.h; src/wpc/wpc.c; src/wpc/core.h; src/wpc/core.c", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
	{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Cheech%20%26%20Chong%20-%20Road-Trippin.vbs", "revision": VPX_REVISION, "sha256": "1893c13b913b987984144fd1d072e6b3c4f4c0df324298722449176f95164b29", "locator": "Cheech & Chong - Road-Trippin.vbs: initialization, ball stacks, switch events, solenoid callbacks, lamp map, GI callback, flippers, toys, and timers", "license": "NOASSERTION", "attribution": "watacaractr, JP Salas, table contributors, and vpxtable_scripts contributors"},
	{"id": PLAYFIELD_SOURCE, "kind": "vpx_table", "uri": "https://www.vpforums.org/index.php?app=downloads&showfile=15975", "sha256": "339a2bc5a4bc8b87453d23cf2031a510cffedc4a0ba927ac4920b0bbe0b4424b", "locator": "Public cabinet screenshot screenshot-91165.png (1688x3000); playfield text, location inserts, target groups, awards, and custom mechanisms. Companion screenshot-91166.png SHA-256 5c024f765af406f32aeb4cf18b8543cb87258a500bab8619d8d02f9e3c936cf1", "license": "NOASSERTION", "attribution": "watacaractr and table contributors", "original_filename": "screenshot-91165.png", "rights": "NOASSERTION"},
	{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "https://archive.org/details/Visual-Pinball-Collection-2025-12-29", "sha256": "1a8e89cdd6a280e803028a9b70a5e89471455fa9712813421449ffae8bb5d0af", "locator": "roms/che_cho.zip (archive SHA-256 34d1f6a3fc31b988fe4c0a38904df2d533e3cb0735995134d113dcb7f96157c2), extracted che_cho.rom; route-name string table and game-specific text only; ROM bytes remain external", "license": "NOASSERTION", "attribution": "watacaractr; preserved by Internet Archive; analyzed locally"},
	{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "local-evidence://pinmame-harness/che_cho", "sha256": "f02c828737fda8cb66bbb88c4038607de3c659ce8827bf0f6b7242ed2107f361", "locator": "tools/run_pinmame_harness.py with exact che_cho.zip; target-lamps.json proves 51-56 to lamps 23-28 and 57/58/61-66 to lamps 31-38; playfield-semantics.json SHA-256 2e0fad699c5969b74c5d0ce9467c837e6d953f3e431892ca81a932207afc26c3 proves switches 31-34 to B-O-N-G lamps 41-44 and 41-43 to top lamps 56-58; route-clean-one-edge.json SHA-256 dae166cf8f694829e8ff71d4719ef7a2c39ff5c3a1e090cf944042b8f7fa9dda validates route progression, five GI channels, displays, trough, and game-on", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM and mutable NVRAM remain external"},
	{"id": RELEASE_SOURCE, "kind": "human_review", "uri": "https://vpuniverse.com/files/file/7061-cheech-chong-road-trippin-bally-2021/", "locator": "Original release page: watacaractr, July 2021, ROM name che_cho, virtual-original description and installation notes", "license": "NOASSERTION", "attribution": "watacaractr and VPUniverse"},
]


def build_definition() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 1,
		"machine": {"id": "watacaractr.cheech-chong-road-trippin.2021", "name": "Cheech & Chong: Road-Trip'pin", "manufacturer": "watacaractr / Bally virtual platform", "year": 2021, "kind": "virtual_pinball"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "not_applicable", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.wpc-alpha", "hardware_generation": "0x00000002", "inversion_applied_by_emulator": True},
		"drivers": [{"id": "che_cho", "description": "Cheech & Chong: Road-Trip'pin (Harley-Davidson unofficial MOD)", "year": "2021", "manufacturer": "Bally/watacaractr", "flags": 0, "physical_compatibility": "identical", "variant_notes": "The sole PinMAME driver is the custom virtual-original ROM. It imports Harley-Davidson's WPC alphanumeric hardware and simulator contract but defines a different virtual playfield, rules presentation, art, target semantics, and local scripted toys."}],
		"inputs": all_inputs(),
		"outputs": all_solenoids() + all_lamps() + all_gi(),
		"displays": [
			{"id": "display.upper", "label": "Upper 16-character alphanumeric display", "kind": "segment", "width": 16, "provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE)},
			{"id": "display.lower", "label": "Lower 16-character alphanumeric display", "kind": "segment", "width": 16, "provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE)},
		],
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": SOURCES,
		"knowledge": {"path": "knowledge/watacaractr/cheech-chong-road-trippin-2021.md", "status": "complete"},
		"conflicts": [],
	}


KNOWLEDGE = """# Cheech & Chong: Road-Trip'pin (watacaractr, 2021)

Coverage: **author-ready - complete controller inventory, virtual mechanisms, displays, and recreation behavior validated**

## Identity and evidence precedence

This is a 2021 virtual-original table by watacaractr, not a manufactured Bally machine and not a physical Harley-Davidson conversion. PinMAME describes it as an unofficial Harley-Davidson MOD because `che_cho` imports the 1991 game's WPC alphanumeric machine driver, input ports, sound ROMs, and simulator base. The recreated playfield, theme, rules text, semantic I/O, art, and script-only mechanisms are specific to Road-Trip'pin.

The known-working `Cheech & Chong - Road-Trippin.vbs` script is ground truth for every controller binding and mechanism. Pinned PinMAME source defines the public WPC topology, display layout, base output constants, and ROM identity. The custom ROM's string table and repeatable live scenarios validate the rethemed semantics. Public release screenshots resolve the playfield labels. Harley service-test labels describe the inherited firmware address slots only and must never override the custom script, ROM text, or Road-Trip'pin playfield art.

## Controller topology

The public WPC switch and lamp addresses are matrix notation, not sequential indices: `11..18`, `21..28`, through `81..88`. Coin/service inputs are `1..8`; the generic flipper column is `111..118`. The table uses cabinet buttons 112 right and 114 left, while its pre-Fliptronics EOS contacts are matrix switches 11 right and 12 left. The harness had to retain ChangedLamps' matrix addresses; polling sequential lamp indices would silently mislabel WPC evidence.

Standard WPC outputs are enumerated through 50 even though the table binds only selected positions. Outputs 1-28 are the standard driver bank, 29-31 are state lines including game-on 31, and generic flipper callbacks include upper-right 34, upper-left 36, lower-right 46, and lower-left 48. Road-Trip'pin deliberately drives its upper-left and lower-left flippers together from 48, leaving 36 unused. Outputs 17-26 are custom flashers; 27 has no callback and 28's renderer line is commented out. Every unused controller position remains explicit in the JSON.

All five WPC GI callbacks, channels 0-4, are active. The proven script intentionally applies every channel to one shared `aGiLights` collection. Recreate that compatibility behavior unless a future table revision proves distinct GI regions.

## Ball lifecycle and ejects

Initialize three balls in the trough on switches 16, 17, and 18. The outhole is 15. Output 1 transfers a drained ball to the trough and output 2 sends the rightmost trough ball toward the manual shooter at angle 45 and force 7. Shooter switch 75 is held while the ball waits; there is no launch coil.

The left eject captures on 36 and output 11 kicks at 90 degrees, force 20, with angle and force variation 3. The right eject captures on 35 and output 10 kicks at 0 degrees, force 27, with the same variation. The bottom eject captures on 28; output 9 kicks at 243 degrees, force 24, Z offset 1.5, and variation 3. Switch 28 UnHit is also the return cue for the motorcycle cop animation.

## Targets, rollovers, lamps, and route

The top drop bank uses switches 51-53, reset output 3, and lamps 23-25 to spell A-N-D. The middle bank uses switches 54-56, reset output 4, and lamps 26-28 to spell T-H-E. Stand-ups 57, 58, and 61-66 light 31-38 in order to spell P-E-D-R-O and M-A-N. Live ROM scenarios prove these one-to-one progress-lamp sequences.

Rollover switches 31-34 light lamps 41-44 and complete B-O-N-G. Top rollovers 41-43 light 56-58 for Cheech, ampersand, and Chong. Switches 67/68 are right/left Road-Trip advance triggers; 71/72 are loop rollovers; 73/74 are outlanes. Matrix lamps 17, 18, 21, 22, 83, and 84 exist in the inherited matrix but are parked off-playfield by the working table and must not be represented as visible inserts.

The ROM string table fixes the ten route names and matrix order: 11 Pedro's House, 12 Drive-In Theater, 13 Upholstery Factory, 14 Hollywood Hotel, 15 Car Wash, 16 Police Station, 86 Our Lady of 13th Street (the display abbreviates this as `SCHOOL`), 87 Boardwalk, 88 Strawberry's House, and 85 Battle of the Bands (`B-O-B` in ROM text). A clean live game begins with 11 and 12 already lit and announces Factory onward as route progress accumulates; preserve the actual ROM state rather than inventing an alternative starting location.

## Coils, flashers, flippers, and gates

Pop switches 25, 26, and 27 map to outputs 5, 6, and 8. Left/right sling switches 37/38 map to outputs 15/16. The Road Closed target has no dedicated controller address: its hit event pulses both 37 and 38, then a local timer restores the target. Output 12 opens the right one-way gate and 13 the left. Output 7 is the knocker. Game-on 31 enables gameplay/flippers.

Flasher 21 illuminates Jade and Debbie; 22 drives the Chong jackpot and bird-cage group; 23 covers Checkpoint and Cheech/Chong plastics; 24 drives the Cheech and Chong spotlights. Outputs 17, 18, 19, 20, 25, and 26 retain the script object-group names where the public evidence supplies no more durable semantic label. These are still exact controller bindings; do not split one output's multiple VPX objects into fictional additional outputs.

## Script-only custom mechanisms

The motorcycle cop is a local timer animation, not a PinMAME motor. Its hit trigger advances from 0 to 725 by 5 units every 10 ms; after the bottom-eject ball leaves switch 28, it returns by 2.5 units per tick. The van uses hidden local kickers to transfer a ball through its animation and exposes no controller switch or coil. The clown decoration shakes on pop hits. Cheech/Chong heads, the bird cage, projectors, and character lights use target-hit counters, random sound branches, and local timers. Preserve these behaviors as authored but do not allocate controller addresses for them.

The Road Closed target is similarly local despite looking like a conventional drop target. It momentarily reports both sling switches and self-resets; there is no reset solenoid. Cul-de-sac contacts reuse bottom-bumper switch 27. These deliberate multiplexed semantics are necessary for ROM rules compatibility.

## Displays and sound

The exact display contract is two rows of sixteen `CORE_SEG16R` characters: row 0 begins at segment 0 and row 1 begins at segment 20. The harness decodes these rows for service menus and rule correlation. The game ROM reuses Harley-Davidson U15/U18 sound ROMs but the intended table experience also requires the separately distributed `che_cho` altsound package. Altsound files are media, not playfield devices, and are not stored in this repository.

## Recreation checklist

- Create every JSON switch, output, matrix lamp, GI string, DIP/configuration bit, and both 16-character displays; retain explicit unused positions.
- Initialize the three-ball trough exactly and implement all three eject vectors, the manual shooter, both drop-bank reset relationships, gates, pops, slings, and the combined left-flipper callback.
- Build the ten route inserts at their exact matrix addresses and preserve the ROM's initially lit route state.
- Implement Road Closed, motorcycle cop, van transfer, clown shake, character heads, bird cage, and projector effects as script-local mechanisms with no invented PinMAME I/O.
- Treat the public VPX script as ground truth whenever inherited Harley diagnostics disagree with the custom table.

## Sources

- `vpx.che-cho.watacaractr.1.0`: pinned known-working table script, SHA-256 `1893c13b913b987984144fd1d072e6b3c4f4c0df324298722449176f95164b29`.
- `screenshot.che-cho.playfield`: public full-playfield screenshot SHA-256 `339a2bc5a4bc8b87453d23cf2031a510cffedc4a0ba927ac4920b0bbe0b4424b` and companion perspective screenshot SHA-256 `5c024f765af406f32aeb4cf18b8543cb87258a500bab8619d8d02f9e3c936cf1`.
- `rom.che-cho.static`: exact external `che_cho.zip` SHA-256 `34d1f6a3fc31b988fe4c0a38904df2d533e3cb0735995134d113dcb7f96157c2`; extracted main ROM SHA-256 `1a8e89cdd6a280e803028a9b70a5e89471455fa9712813421449ffae8bb5d0af`. ROM bytes remain outside the repository.
- `runtime.che-cho.harness`: isolated game-start, target/lamp, B-O-N-G/top-rollover, route, display, GI, and service scenarios. Exact raw-run hashes are recorded in the source locator and compact runtime evidence.
- `pinmame.wpc.che-cho.4ec52ff0ac13`: pinned driver declaration, WPC address conversion, inherited Harley simulator contract, output topology, and two-row display layout.
"""


EVIDENCE_SUMMARY = {
	"format": "pinmame-machine-evidence",
	"version": 1,
	"extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
	"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/che_cho/harness", "sha256": "f02c828737fda8cb66bbb88c4038607de3c659ce8827bf0f6b7242ed2107f361", "license": "NOASSERTION", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external", "quality": "validated"},
	"driver_ids": ["che_cho"],
	"machine_ids": ["watacaractr.cheech-chong-road-trippin.2021"],
	"switches": [],
	"outputs": [],
	"states": [],
	"mechanisms": [],
	"recreation_notes": [],
	"runtime": {
		"game": "che_cho",
		"rom_archive_sha256": "34d1f6a3fc31b988fe4c0a38904df2d533e3cb0735995134d113dcb7f96157c2",
		"raw_runs": [
			{"name": "target-lamps", "sha256": "f02c828737fda8cb66bbb88c4038607de3c659ce8827bf0f6b7242ed2107f361", "self_test_pulses": 0},
			{"name": "playfield-semantics", "sha256": "2e0fad699c5969b74c5d0ce9467c837e6d953f3e431892ca81a932207afc26c3", "self_test_pulses": 0},
			{"name": "route-clean-one-edge", "sha256": "dae166cf8f694829e8ff71d4719ef7a2c39ff5c3a1e090cf944042b8f7fa9dda", "self_test_pulses": 0},
			{"name": "single-lamps-service", "sha256": "0826401a91c77fb0845e943d0f76cd3d98957f76097dc422aebe16620aff8ad9", "self_test_pulses": 0},
		],
		"observations": {
			"switch_to_lamp": {"31": 41, "32": 42, "33": 43, "34": 44, "41": 56, "42": 57, "43": 58, "51": 23, "52": 24, "53": 25, "54": 26, "55": 27, "56": 28, "57": 31, "58": 32, "61": 33, "62": 34, "63": 35, "64": 36, "65": 37, "66": 38},
			"gi_addresses_seen": [0, 1, 2, 3, 4],
			"named_output_addresses": {"game_on": 31, "trough_eject": 2},
			"initial_lamp_addresses": [11, 12],
		},
		"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game che_cho --rom-path <roms> --work-dir <isolated-state> --initial-switch 16 --initial-switch 17 --initial-switch 18 --pulse 1:250:0.5 --pulse 13:250:1.2 --pulse 18:80:0.8 --pulse <playfield-switch>:20:1.4 --output <external-json>",
	},
}


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


for path in (ROOT / "machines/stubs/che_cho.json", ROOT / "knowledge/stubs/che_cho.md"):
	if path.exists():
		path.unlink()

write_json(ROOT / "machines/author-ready/watacaractr/cheech-chong-road-trippin-2021.json", build_definition())
write_json(ROOT / "evidence/runtime/wpc/che-cho-gameplay.json", EVIDENCE_SUMMARY)
knowledge_path = ROOT / "knowledge/watacaractr/cheech-chong-road-trippin-2021.md"
knowledge_path.parent.mkdir(parents=True, exist_ok=True)
knowledge_path.write_text(KNOWLEDGE, encoding="utf-8")
