"""Promote The Walking Dead Premium/LE with reviewed spatial placements."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import write_json

from curate_walking_dead import build_premium


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/the-walking-dead-premium-limited-edition-2014.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-walking-dead-premium-limited-edition-2014.json"

TABLE_SOURCE = "vpx-table.walking-dead-premium-le-vpw-day-1.1"
SCRIPT_SOURCE = "vpx.walking-dead-premium-le-vpw-day-1.1"
MANUAL_SOURCE = "manual.walking-dead-premium-le"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
RUNTIME_SOURCE = "runtime.walking-dead-premium-le.gi-lamp-diagnostic"
ROM_SOURCE = "rom-static.walking-dead-premium-le-output-names"
BOOT_SOURCE = "runtime.walking-dead-premium-le.boot-start"

TABLE_SOURCE_RECORD = {
	"attribution": "Flupper1, Robby King Pin, Rothbauerw, VPW contributors, prior table authors, and vpxtable_scripts contributors",
	"id": TABLE_SOURCE,
	"kind": "vpx_table",
	"known_working": True,
	"license": "NOASSERTION",
	"locator": "The Walking Dead LE Premium (Stern 2014) day 1.1.vpx (217,935,872 bytes); ROM twd_160h; extracted with vpxtool git:v0.33.3; normalized geometry reviewed against the exact pinned script and manual physical maps",
	"original_filename": "The Walking Dead LE Premium (Stern 2014) day 1.1.vpx",
	"rights": "NOASSERTION",
	"sha256": "2aca72eb73ac11cc1f8d5633cd8bb302146ac2dd91bfa5fb8364a314b5179987",
	"uri": "local-evidence://stern/the-walking-dead-premium-limited-edition-2014/The Walking Dead LE Premium (Stern 2014) day 1.1.vpx",
}

RUNTIME_SOURCE_RECORD = {
	"attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
	"id": RUNTIME_SOURCE,
	"kind": "runtime_scenario",
	"license": "NOASSERTION",
	"locator": "Exact twd_160h lamp-diagnostic run using PinMAME DLL SHA-256 79f6cfb0048470218b2302ca4fb0d078839acf7f05883c36fc93881ba8abac84 and ROM archive twd_160h.zip from the authorized corpus. Public lamps 106-109 each emit one common value-255 event at 5.828 seconds. This trace proves activity but not the individual identities resolved by the exact-ROM name table and manual sheet Y26.",
	"revision": "4ec52ff0ac133ac251681518aed2249e19fe26eb",
	"sha256": "c8f78d6bd0d52632049f1f1ee445e47d10db698355a681dc7e8d1da14b6c4a64",
	"uri": "external:pinmame-game-code/twd_160h/harness/lamp-diagnostic-v1/run.json",
}

INPUT_POSITIONS = {
	1: [(0.810225, 0.592424)], 2: [(0.597108, 0.478274)],
	3: [(0.450630, 0.228143)], 4: [(0.450630, 0.242571)],
	9: [(0.096132, 0.581755)], 10: [(0.103929, 0.555609)], 11: [(0.111754, 0.529669)],
	18: [(0.672191, 0.924598)], 19: [(0.737551, 0.908247)],
	20: [(0.802287, 0.891896)], 21: [(0.866469, 0.876936)],
	22: [(0.884319, 0.863922)], 23: [(0.940602, 0.887037)],
	24: [(0.059674, 0.781486)], 25: [(0.140093, 0.743658)],
	26: [(0.236274, 0.741789)], 27: [(0.688525, 0.741432)],
	28: [(0.780244, 0.743658)], 29: [(0.856092, 0.783267)],
	30: [(0.648632, 0.383190)], 31: [(0.910424, 0.352023)], 32: [(0.743576, 0.290523)],
	33: [(0.940834, 0.618147)], 34: [(0.815118, 0.478575)], 35: [(0.901765, 0.152881)],
	36: [(0.705328, 0.201380)], 37: [(0.792735, 0.206053)],
	38: [(0.845675, 0.148226)], 39: [(0.948529, 0.157098)],
	40: [(0.114501, 0.412593)], 41: [(0.068839, 0.135737)],
	42: [(0.096517, 0.113665)], 43: [(0.238070, 0.135867)],
	44: [(0.363686, 0.293860)], 45: [(0.538164, 0.294088)],
	46: [(0.450105, 0.265322)], 47: [(0.294118, 0.126836)],
	48: [(0.780237, 0.616027)], 49: [(0.179576, 0.298335)],
	50: [(0.460952, 0.956926)], 51: [(0.460952, 0.956926)], 52: [(0.221141, 0.885704)],
	70: [(0.588052, 0.236942)], 72: [(0.589102, 0.186653)],
	81: [(0.627101, 0.852381)], 83: [(0.295168, 0.852381)],
}

SOLENOID_POSITIONS = {
	1: [(0.866469, 0.876936)], 2: [(0.943994, 0.985277)],
	3: [(0.393382, 0.238879), (0.506243, 0.238657)],
	4: [(0.393382, 0.238879), (0.506243, 0.238657)],
	5: [(0.078964, 0.597364)], 6: [(0.543206, 0.517064)], 7: [(0.450049, 0.343800)],
	9: [(0.648632, 0.383190)], 10: [(0.910424, 0.352023)], 11: [(0.743576, 0.290523)],
	12: [(0.096132, 0.581755), (0.103929, 0.555609), (0.111754, 0.529669)],
	13: [(0.236274, 0.741789)], 14: [(0.688525, 0.741432)],
	15: [(0.295168, 0.852381)], 16: [(0.627101, 0.852381)],
	19: [(0.597108, 0.478274)], 20: [(0.837068, 0.578316)],
	21: [(0.460952, 0.956926)], 25: [(0.771986, 0.380993)],
	26: [(0.453605, 0.202836)],
	27: [(0.393382, 0.238879), (0.506243, 0.238657)],
	28: [(0.043703, 0.550273)], 29: [(0.869034, 0.530056)],
	31: [(0.071543, 0.338021)], 32: [(0.245000, 0.160000)],
	51: [(0.221141, 0.885704)], 52: [(0.780237, 0.616027)], 53: [(0.780237, 0.616027)],
	55: [(0.165166, 0.249633)], 56: [(0.165166, 0.249633)],
}

LAMP_POSITIONS = {
	3: [(0.372121, 0.460429)], 4: [(0.460066, 0.901564)], 5: [(0.389291, 0.828171)],
	6: [(0.434375, 0.838059)], 7: [(0.486351, 0.838198)], 8: [(0.531757, 0.828330)],
	9: [(0.555769, 0.800393)], 10: [(0.458111, 0.811979)], 11: [(0.365712, 0.800331)],
	12: [(0.412763, 0.791907)], 13: [(0.460693, 0.783760)], 14: [(0.508588, 0.791698)],
	15: [(0.318847, 0.749817)], 16: [(0.376852, 0.749781)], 17: [(0.433827, 0.749648)],
	18: [(0.490626, 0.750657)], 19: [(0.544213, 0.750136)], 20: [(0.601042, 0.750240)],
	21: [(0.460743, 0.708869)], 22: [(0.058947, 0.724589)], 23: [(0.144259, 0.674260)],
	25: [(0.288144, 0.635866)], 26: [(0.180206, 0.621212)], 27: [(0.241770, 0.600849)],
	28: [(0.240890, 0.557871)], 29: [(0.323927, 0.565531)], 30: [(0.176722, 0.502224)],
	31: [(0.165883, 0.480927)], 32: [(0.140457, 0.440965)],
	34: [(0.315888, 0.544988)], 35: [(0.292752, 0.504426)],
	37: [(0.852737, 0.724544)], 38: [(0.782091, 0.674479)], 39: [(0.667252, 0.689733)],
	40: [(0.702448, 0.664296)], 42: [(0.557043, 0.696366)], 43: [(0.586941, 0.672951)],
	44: [(0.633516, 0.634586)], 45: [(0.440592, 0.646389)], 46: [(0.414899, 0.598786)],
	47: [(0.445836, 0.610140)], 48: [(0.487140, 0.616080)], 49: [(0.527726, 0.614817)],
	50: [(0.496286, 0.571524)], 51: [(0.628735, 0.551699)], 52: [(0.650351, 0.532864)],
	53: [(0.689209, 0.490538)], 54: [(0.451000, 0.423349)], 55: [(0.536749, 0.318769)],
	56: [(0.363805, 0.318798)], 58: [(0.312740, 0.276553)], 59: [(0.313758, 0.312995)],
	60: [(0.743576, 0.290523)], 61: [(0.910424, 0.352023)], 62: [(0.648632, 0.383190)],
	63: [(0.317964, 0.335011)], 64: [(0.361689, 0.371280)], 65: [(0.391357, 0.383389)],
	66: [(0.429367, 0.389920)], 67: [(0.472329, 0.389707)], 68: [(0.509855, 0.383194)],
	69: [(0.539241, 0.371404)], 70: [(0.810000, 0.477000)], 71: [(0.810000, 0.477000)],
	72: [(0.683707, 0.127360)], 73: [(0.787000, 0.025000)], 74: [(0.787000, 0.025000)],
	75: [(0.787000, 0.025000)], 76: [(0.709392, 0.157219)], 77: [(0.792861, 0.160826)],
	78: [(0.168000, 0.229000)],
	133: [(0.589311, 0.186540)], 134: [(0.589311, 0.186540)], 135: [(0.589311, 0.186540)],
	136: [(0.587855, 0.238139)], 137: [(0.587855, 0.238139)], 138: [(0.587855, 0.238139)],
	152: [(0.696654, 0.588034)], 153: [(0.696654, 0.588034)], 154: [(0.696654, 0.588034)],
	168: [(0.735704, 0.442469)], 169: [(0.735704, 0.442469)], 170: [(0.735704, 0.442469)],
	187: [(0.274839, 0.213206)], 188: [(0.274839, 0.213206)], 189: [(0.274839, 0.213206)],
	195: [(0.105437, 0.388664)], 196: [(0.105437, 0.388664)], 197: [(0.105437, 0.388664)],
	203: [(0.263975, 0.452884)], 204: [(0.263975, 0.452884)], 205: [(0.263975, 0.452884)],
}

WHITE_GI_POSITIONS = [
	(0.311248, 0.170439), (0.776579, 0.170439), (0.228043, 0.226365),
	(0.850539, 0.226365), (0.135593, 0.352197), (0.902928, 0.352197),
	(0.041602, 0.461385), (0.970724, 0.461385), (0.033898, 0.530626),
	(0.976888, 0.530626), (0.055470, 0.587883), (0.949152, 0.587883),
	(0.083205, 0.646471), (0.921418, 0.646471), (0.127889, 0.701065),
	(0.878274, 0.701065), (0.186441, 0.756991), (0.819723, 0.756991),
	(0.241911, 0.806924), (0.765794, 0.806924), (0.295840, 0.857523),
	(0.711864, 0.857523), (0.497689, 0.938083),
]

RED_GI_POSITIONS = [
	(0.144838, 0.273635), (0.890601, 0.273635), (0.063174, 0.404128),
	(0.952234, 0.404128), (0.035439, 0.511984), (0.978428, 0.511984),
	(0.053929, 0.567244), (0.959938, 0.567244), (0.090909, 0.626498),
	(0.922958, 0.626498), (0.151002, 0.682423), (0.862866, 0.682423),
	(0.251156, 0.830226), (0.759630, 0.830226),
]

# Manual Y26 shows the five-socket mounting panel from its service/rear face:
# the 077-5000-00 staple-bayonet socket mounting hardware and rear connector/
# board enclosure are exposed, rather than the decorated player-facing side.
# Socket x is normalized within the panel outline, then reflected with
# x_player = 1 - x_service; y=0 projects the vertical panel to the rear edge.
PANEL_RED_POSITIONS = [(0.967900, 0.000000), (0.771000, 0.000000)]
PANEL_GREEN_POSITIONS = [(0.546400, 0.000000), (0.480000, 0.000000), (0.415800, 0.000000)]

CABINET_INPUT_ROLES = {
	-7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
	15: "cabinet.tournament", 16: "cabinet.start",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	71: "cabinet.action", 82: "cabinet.flipper", 84: "cabinet.flipper",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.coin-meter",
	("pinmame.output.lamp", 1): "cabinet.start",
	("pinmame.output.lamp", 2): "cabinet.tournament",
	("pinmame.output.lamp", 120): "cabinet.action",
	("pinmame.output.lamp", 121): "cabinet.action",
	("pinmame.output.lamp", 122): "cabinet.action",
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
	located_sources = (TABLE_SOURCE, SCRIPT_SOURCE, MANUAL_SOURCE)
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], located_sources)
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		else:
			raise ValueError(f"Walking Dead Premium/LE input {group} {address} has no reviewed spatial disposition")

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
			sources = (MANUAL_SOURCE,) if address == 32 else located_sources
			_located(device, role, SOLENOID_POSITIONS[address], sources)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = len(SOLENOID_POSITIONS[address])
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], located_sources)
			device.setdefault("physical", {}).setdefault("quantity", 1)
		elif group == "pinmame.output.lamp" and address == 106:
			_located(device, "emitter", WHITE_GI_POSITIONS, (MANUAL_SOURCE, SCRIPT_SOURCE, ROM_SOURCE, BOOT_SOURCE, RUNTIME_SOURCE))
		elif group == "pinmame.output.lamp" and address == 107:
			_located(device, "emitter", PANEL_RED_POSITIONS, (MANUAL_SOURCE, ROM_SOURCE, BOOT_SOURCE, RUNTIME_SOURCE))
		elif group == "pinmame.output.lamp" and address == 108:
			_located(device, "emitter", PANEL_GREEN_POSITIONS, (MANUAL_SOURCE, ROM_SOURCE, BOOT_SOURCE, RUNTIME_SOURCE))
		elif group == "pinmame.output.lamp" and address == 109:
			_located(device, "emitter", RED_GI_POSITIONS, (MANUAL_SOURCE, ROM_SOURCE, BOOT_SOURCE, RUNTIME_SOURCE))
		else:
			raise ValueError(f"Walking Dead Premium/LE output {group} {address} ({kind}) has no reviewed spatial disposition")


def promote() -> None:
	definition = build_premium()
	for source in (TABLE_SOURCE_RECORD, RUNTIME_SOURCE_RECORD):
		if not any(existing["id"] == source["id"] for existing in definition["sources"]):
			definition["sources"].append(source)
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
