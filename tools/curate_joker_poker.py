"""Deterministic, fail-closed curation of Gottlieb Joker Poker (1978, System 1).

The secondary chart is a candidate for wiring, not a substitute factory schematic.
The exact VPX supplies implementation bindings and observed interaction locations;
its insert glow objects are deliberately not promoted to physical bulb sockets.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.joker-poker.1978"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
DEFINITION_PATH = Path("machines/partial/gottlieb/joker-poker-1978.json")
SEED_PATH = Path("tools/seeds/gottlieb/joker-poker-1978.json")
KNOWLEDGE_PATH = Path("knowledge/gottlieb/joker-poker-1978.md")
KNOWLEDGE_SEED_PATH = Path("tools/seeds/gottlieb/joker-poker-1978.md")
REPORT_PATH = Path("reports/spatial/gottlieb/joker-poker-1978.json")
REPORT_MARKDOWN_PATH = REPORT_PATH.with_suffix(".md")
EXCERPTS = Path("evidence/excerpts") / MACHINE_ID
VPX_RELATIVE = Path("gottlieb/joker-poker-1978")
TABLE_FILE = "Joker Poker (Gottlieb 1978) 1.1.vpx"
TABLE_SHA256 = "dfab53a93623a396010f83c3d062014189cc185083bd5f9296f1a184ee2ed518"
SCRIPT_SHA256 = "07c82d5f27b3c49961676cd8ef6840caf5a0720ecdafe6b3910994a40bed02b1"
EXTRACTION_MANIFEST_SHA256 = "debf1ef824468121b6b5d323ed5a6bf2ff545cf3a81eac13314e9aae14926539"
SPATIAL_CANDIDATES_SHA256 = "19d1c0b3d815e5dba29722d8fb166fdaa3e3949b5b8c4c5dbecd8e15e82cd128"
CHART_FILE = "Gottlieb_Joker_Poker_Tech_Chart.pdf"
CHART_SHA256 = "7a5391c0dc0e373da1fc6252750a76aad7fe0490f1f25f7b879da9503f2601b0"
LIBRARY_HASHES = {
	"gts1.vbs": "554da222cdff8080854c9bf59ad891fd8f44f2a3013deba4f6f0d62058ca3d78",
	"core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69",
	"VPMKeys.vbs": "563f599c5d5adf22ac0f9ba8cf2ffe90491fe868b72233f7e7b4960b81e8f4c1",
}
CORE = "pinmame.core.gts1"
CORE_COMMON = "pinmame.core.common"
GAME = "pinmame.game.jokrpokr"
SCRIPT = "vpx-script.joker-poker-1-1"
TABLE = "vpx-table.joker-poker-1-1"
CHART = "technical-chart.joker-poker"
LIBRARY = "vpm-library.gts1"
PHOTO = "ipdb.1306.photo.32830"
BACKBOX_PHOTO = "ipdb.1306.photo.12959"
SWITCH = "pinmame.input.switch"
DIP = "pinmame.input.dip"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"

# These are the official spatial helper's six-decimal results for exact bound objects.
# The external gate recomputes every point from retained gameitems, including walls.
POINTS = {
	"Bumper1": (0.229779, 0.324728), "Bumper2": (0.648897, 0.253114),
	"LeftFlipper": (0.27416, 0.797418), "RightFlipper": (0.630777, 0.797418),
	"RightFlipper1": (0.503414, 0.303873), "Drain": (0.495798, 0.911002),
	"sw11": (0.540704, 0.13979), "sw11b": (0.054884, 0.686689),
	"sw12": (0.621061, 0.140114), "sw12b": (0.119748, 0.68124),
	"sw12d": (0.782563, 0.682927), "sw13": (0.702468, 0.140374),
	"sw13b": (0.852941, 0.688765), "sw20": (0.806197, 0.168786),
	"sw21": (0.093225, 0.469318), "sw22": (0.262999, 0.432019),
	"sw23": (0.318146, 0.419564), "sw30": (0.851366, 0.344869),
	"sw31": (0.48989, 0.38259), "sw32": (0.545825, 0.370135),
	"sw33": (0.600972, 0.35807), "sw41": (0.779149, 0.499157),
	"sw42": (0.792805, 0.52718), "sw43": (0.806329, 0.555202),
	"sw44": (0.81959, 0.583485), "sw50": (0.094013, 0.205274),
	"sw51": (0.147321, 0.19243), "sw52": (0.200368, 0.179456),
	"sw53": (0.251838, 0.166742), "sw54": (0.304359, 0.153769),
	"sw40a": (0.681097, 0.692016), "sw40b": (0.821471, 0.540767),
	"sw40c": (0.842763, 0.215137), "sw40d": (0.536545, 0.360505),
	"sw40e": (0.28334, 0.416612), "sw40f": (0.057646, 0.283625),
	"sw40g": (0.071637, 0.414628), "sw40h": (0.07013, 0.508721),
	"sw40i": (0.179158, 0.171663), "sw40j": (0.787693, 0.347073),
	"LeftSlingShot": (0.225336, 0.662772),
}
# Script-bound insert/glow centers are portable candidates for future socket
# reconciliation. They are never used as canonical physical lamp placements.
RENDER_POINTS = {
	"l4": (0.456408, 0.84821), "l8": (0.495864, 0.557311),
	"l9": (0.471967, 0.652536), "l10": (0.484047, 0.605183),
	"l11": (0.4612, 0.699371), "l12": (0.451024, 0.746659),
	"l13": (0.560071, 0.610048), "l14": (0.572361, 0.562474),
	"l15": (0.546218, 0.656461), "l16": (0.537749, 0.704366),
	"l18": (0.52672, 0.750032), "l19": (0.85281, 0.288921),
	"l20": (0.777311, 0.204333), "l21": (0.61896, 0.08316),
	"l22": (0.70063, 0.08316), "l23": (0.537027, 0.083031),
	"l24": (0.851103, 0.639238), "l25": (0.11791, 0.625746),
	"l26": (0.784926, 0.626524), "l27": (0.053834, 0.637779),
	"l28": (0.452928, 0.509244),
}
SWITCH_OBJECTS = {
	10: ["Bumper1", "Bumper2"], 11: ["sw11", "sw11b"],
	12: ["sw12", "sw12b", "sw12d"], 13: ["sw13", "sw13b"],
	20: ["sw20"], 30: ["sw30"],
	40: [f"sw40{x}" for x in "abcdefghij"] + ["LeftSlingShot"],
}
for _n in (21, 22, 23, 31, 32, 33, 41, 42, 43, 44, 50, 51, 52, 53, 54):
	SWITCH_OBJECTS[_n] = [f"sw{_n}"]

SWITCH_LABELS = {
	0: ("test", "Self Test"), 1: ("coin-1", "Coin Chute 1"),
	2: ("coin-2", "Coin Chute 2"), 3: ("start", "Replay / Start Button"),
	4: ("tilt", "Tilt"), 10: ("pop-bumpers", "Pop Bumper Scoring Contacts"),
	11: ("a-rollovers", "A Rollovers"), 12: ("b-rollovers", "B Rollovers"),
	13: ("c-rollovers", "C Rollovers"), 20: ("extra-ball-target", "Extra Ball Standup Target"),
	21: ("ten-drop", "Ten Drop Target"), 22: ("jack-drop-1", "Jack Drop Target 1"),
	23: ("jack-drop-2", "Jack Drop Target 2"), 30: ("special-rollover", "Special Rollover"),
	31: ("queen-drop-1", "Queen Drop Target 1"), 32: ("queen-drop-2", "Queen Drop Target 2"),
	33: ("queen-drop-3", "Queen Drop Target 3"), 40: ("ten-point-contacts", "Ten Point Contacts"),
	41: ("king-drop-1", "King Drop Target 1"), 42: ("king-drop-2", "King Drop Target 2"),
	43: ("king-drop-3", "King Drop Target 3"), 44: ("king-drop-4", "King Drop Target 4"),
	50: ("ace-drop-1", "Ace Drop Target 1"), 51: ("ace-drop-2", "Ace Drop Target 2"),
	52: ("joker-drop", "Joker Drop Target"), 53: ("ace-drop-3", "Ace Drop Target 3"),
	54: ("ace-drop-4", "Ace Drop Target 4"), 56: ("audits-reset", "Audits Reset"),
	66: ("outhole", "Outhole"), 76: ("slam-tilt", "Slam Tilt"),
	82: ("right-flipper-button", "Right Flipper Button"),
	84: ("left-flipper-button", "Left Flipper Button"),
}
LAMP_LABELS = {
	1: ("relay.game-over-q", "Game Over Q Relay", "relay"),
	2: ("relay.tilt-t", "Tilt T Relay", "relay"),
	3: ("lamp.high-game-to-date", "High Game to Date", "lamp"),
	4: ("lamp.shoot-again", "Same Player Shoot Again", "lamp"),
	8: ("lamp.aces-bonus", "Aces Bonus", "lamp"),
	9: ("lamp.queens-bonus", "Queens Bonus", "lamp"),
	10: ("lamp.kings-bonus", "Kings Bonus", "lamp"),
	11: ("lamp.jacks-bonus", "Jacks Bonus", "lamp"),
	12: ("lamp.tens-bonus", "Tens Bonus", "lamp"),
	13: ("lamp.bonus-4000", "4000 Bonus", "lamp"),
	14: ("lamp.bonus-5000", "5000 Bonus", "lamp"),
	15: ("lamp.bonus-3000", "3000 Bonus", "lamp"),
	16: ("lamp.bonus-2000", "2000 Bonus", "lamp"),
	17: ("coil.kings-reset", "Kings Drop Target Bank Reset", "coil"),
	18: ("lamp.bonus-1000", "1000 Bonus", "lamp"),
	19: ("lamp.special", "Special Rollover", "lamp"),
	20: ("lamp.extra-ball", "Extra Ball Target", "lamp"),
	21: ("lamp.top-b", "Top B Rollover", "lamp"),
	22: ("lamp.top-c", "Top C Rollover", "lamp"),
	23: ("lamp.top-a", "Top A Rollover", "lamp"),
	24: ("lamp.bottom-c", "Bottom C Rollover", "lamp"),
	25: ("lamp.left-bottom-b", "Left Bottom B Rollover", "lamp"),
	26: ("lamp.right-bottom-b", "Right Bottom B Rollover", "lamp"),
	27: ("lamp.bottom-a", "Bottom A Rollover", "lamp"),
	28: ("lamp.bonus-5x", "5X Bonus", "lamp"),
}
SOLENOID_LABELS = {
	1: ("coil.outhole", "Outhole"), 2: ("coil.knocker", "Knocker"),
	3: ("coil.chime-10", "10 Point Chime"), 4: ("coil.chime-100", "100 Point Chime"),
	5: ("coil.chime-1000", "1000 Point Chime"),
	6: ("coil.ten-jacks-reset", "Ten and Jacks Drop Target Reset"),
	7: ("coil.queens-reset", "Queens Drop Target Reset"),
	8: ("coil.aces-reset", "Aces and Joker Drop Target Reset"),
}


def provenance(status, *refs):
	return {"status": status, "source_refs": list(refs)}


def not_applicable(reason, *refs, status="validated"):
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(status, *refs)}


def located(objects, role="sensor", status="observed"):
	return {"status": status, "placements": [
		{"id": name.lower(), "role": role, "space": "playfield", "x": POINTS[name][0],
		 "y": POINTS[name][1], "provenance": provenance(status, TABLE, SCRIPT)}
		for name in objects
	]}


def aliases(group, address):
	ns = {SWITCH: "pinmame.switch", LAMP: "pinmame.lamp", SOLENOID: "pinmame.solenoid", DIP: "pinmame.dip"}[group]
	values = [str(address)]
	if group == SWITCH and 0 <= address < 10:
		values += [f"{address:02}", f"{address:03}"]
	return [{"namespace": ns, "value": x} for x in values]


def device(identifier, label, kind, group, address, availability, status, *refs):
	return {"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address}, "aliases": aliases(group, address),
		"availability": availability, "provenance": provenance(status, *refs)}


def sources(root=ROOT):
	def excerpt(name, locator):
		path = EXCERPTS / name
		return {"id": name.removesuffix(".md"), "locator": locator, "path": path.as_posix(),
			"sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
			"method": "manual", "transcribed_by": "GPT Sol, 2026-10-21", "reviewed": True}
	base = "https://github.com/vpinball/pinmame/blob/" + REVISION + "/src/wpc/"
	result = [
		{"id": CORE, "kind": "pinmame_core", "uri": base + "gts1.c", "revision": REVISION,
		 "sha256": "87f544ffd01f78fb193ca55bedd817fc7267d476ec9112af4c06ade8bc50fe61",
		 "locator": "GTS1_sw2m/GTS1_m2sw; port_w devices 2/3/4; lamp_w; SWITCH_UPDATE; GTS1_vblank", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_COMMON, "kind": "pinmame_core", "uri": base + "core.c", "revision": REVISION,
		 "sha256": "ae94d4ae8078f684b3ba58fd35cac84bf58e181de1e6f25ecb95f03c66966dcc",
		 "locator": "core_updateSw, core_getSol, core_getSw, core_getDip; core.h constants", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": GAME, "kind": "pinmame_core", "uri": base + "gts1games.c", "revision": REVISION,
		 "sha256": "1693527852b4d66e6a83d91f9b37d99b25d209c2196634d2c7920905bb1dc7c0",
		 "locator": "sys1_disp; INIT_S1; Joker Poker INIT_S1 and CORE_CLONEDEFNV; 417.cpu", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": SCRIPT, "kind": "vpx_script", "uri": "local-vpx://gottlieb/joker-poker-1978/extracted/script.vbs",
		 "sha256": SCRIPT_SHA256, "revision": "Joker Poker 1.1; extracted with vpxtool git:v0.33.3",
		 "locator": "SolCallback; Table1_Init; switch handlers; Lights; UpdateMultipleLamps",
		 "known_working": False, "license": "NOASSERTION", "attribution": "Goldchicco, 32assassin, BorgDogs",
		 "acquired_at": "2026-10-21T20:55:40.579381Z", "excerpts": [excerpt("vpx-runtime.md", "script.vbs lines 49-421 and gts1.vbs keyboard handlers")]},
		{"id": TABLE, "kind": "vpx_table", "uri": "local-vpx://gottlieb/joker-poker-1978/" + TABLE_FILE,
		 "sha256": TABLE_SHA256, "revision": "1.1; Sept 2021; vpxtool git:v0.33.3", "locator": "gamedata bounds 0,0,952,1927; extracted/gameitems; retained manifest.json",
		 "license": "NOASSERTION", "attribution": "Goldchicco, 32assassin, BorgDogs", "acquired_at": "2026-10-21T20:55:39.918939Z"},
		{"id": LIBRARY, "kind": "vpx_script", "uri": "local-vpx://gottlieb/joker-poker-1978/libraries/gts1.vbs",
		 "sha256": LIBRARY_HASHES["gts1.vbs"], "revision": "VBS 3.61", "locator": "GTS1 constants and vpmKeyDown/vpmKeyUp; core.vbs cvpmDropTarget/cvpmBallStack",
		 "license": "NOASSERTION", "attribution": "VPinMAME script-library contributors", "excerpts": [excerpt("vpx-runtime.md", "Retained shared library paragraph")]},
		{"id": CHART, "kind": "manual", "uri": "https://www.pinballrebel.com/pinball/cards/Tech_Charts/" + CHART_FILE,
		 "sha256": CHART_SHA256, "revision": "undated secondary technical chart", "locator": "PDF page 1; complete Fuse List, Switch Matrix, Lamps and solenoids and Solenoids tables",
		 "license": "NOASSERTION", "attribution": "inkochnito (www.inkochnito.nl), hosted by Pinball Rebel",
		 "acquired_at": "2026-10-21T20:55:12.959281Z", "excerpts": [excerpt("technical-chart.md", "PDF page 1, all factual tables")]},
		{"id": PHOTO, "kind": "human_review", "uri": "https://www.ipdb.org/images/1306/image-18.jpg",
		 "sha256": "2454e148c09fce41cf227252cd9d002526d781a961e7df3238ffa7a0b76d26bc",
		 "locator": "IPDB machine 1306 https://www.ipdb.org/machine.cgi?id=1306; photo page https://www.ipdb.org/showpic.pl?id=1306&picno=32830; playfield and apron factory card B-18450",
		 "source_id": "ipdb:1306:32830", "license": "NOASSERTION", "attribution": "Jim Palson, photograph hosted by IPDB; factory card by D. Gottlieb & Co.",
		 "acquired_at": "2026-10-21T20:58:16.898Z", "excerpts": [excerpt("factory-card.md", "Photo 32830, apron instruction card B-18450 and visible device layout")]},
		{"id": BACKBOX_PHOTO, "kind": "human_review", "uri": "https://www.ipdb.org/images/1306/image-12.jpg",
		 "sha256": "41edd4c8e93c96df071194faa3d4136a5409c53d258efefb93e94144401b7670",
		 "locator": "IPDB machine 1306 https://www.ipdb.org/machine.cgi?id=1306; photo page https://www.ipdb.org/showpic.pl?id=1306&picno=12959; all five backglass display windows",
		 "source_id": "ipdb:1306:12959", "license": "NOASSERTION", "attribution": "Bill Dempski, photograph hosted by IPDB",
		 "acquired_at": "2026-10-21T21:12:44.364Z", "excerpts": [excerpt("backbox-displays.md", "Photo 12959, observed backbox display fitment")]},
		{"id": "runtime.joker-poker.boot-blocker", "kind": "runtime_scenario",
		 "uri": "local-review://gottlieb.joker-poker.1978/runtime/log-diagnostic-arguments.json",
		 "sha256": "eb85ad85fe8bf58f3f91c729bf893305805aff6b67d6aedc67a74b1cb373f1ef",
		 "revision": REVISION, "locator": "Fresh-state load attempt and emulator audit callbacks: A1752CF.bin/A1753CE.bin NOT FOUND; state 2 to 0 before ready",
		 "license": "MIT", "attribution": "PinMAME harness diagnostic by project contributors",
		 "excerpts": [excerpt("runtime-limitation.md", "Failed fresh-state startup; no gameplay or self-test observations")]},
	]
	return result


def build(root=ROOT):
	inputs = []
	matrix = [10 * r + s for r in range(8) for s in range(8)]
	for address in list(range(-8, 0)) + matrix + list(range(81, 89)):
		if address in SWITCH_LABELS:
			slug, label = SWITCH_LABELS[address]
			d = device("switch." + slug, label, "switch", SWITCH, address, "used", "observed", SCRIPT, LIBRARY, CORE)
			d["physical"] = {"notes": "Contact construction and wire assignments require the factory schematic; secondary chart is transcribed without upgrading it to primary evidence."}
			if address in SWITCH_OBJECTS:
				d["spatial"] = located(SWITCH_OBJECTS[address])
				if address == 40:
					d["spatial"]["status"] = "candidate"
					for p in d["spatial"]["placements"]:
						p["provenance"]["status"] = "candidate"
					d["physical"]["notes"] += " Eleven script-bound scoring-rubber regions; wall centroids are interaction-region projections, not surveyed leaf-switch positions."
			elif address == 66:
				d["physical"]["notes"] += " InitNoTrough supplies this state; the BallRelease object is the virtual ejection point, not a surveyed outhole switch."
			else:
				d["spatial"] = not_applicable("cabinet_or_service", LIBRARY, CORE, status="observed")
			if address in (82, 84):
				d["roles"] = ["button.flipper.right" if address == 82 else "button.flipper.left"]
			inputs.append(d)
		else:
			# Matrix col 6 (public units 5) is read but absent from this game's chart;
			# public 46 is the undocumented fourth special input. Do not guess non-fitment.
			chart_unused = address >= 0 and address <= 77 and address % 10 < 5
			unknown = chart_unused or (0 <= address <= 77 and (address % 10 == 5 or address == 46))
			status = "candidate" if unknown or chart_unused else "validated"
			d = device(f"switch.unresolved-{address}" if unknown else f"switch.unused-{str(address).replace('-', 'minus-')}",
				f"Unverified Not Used Switch {address}" if chart_unused else (f"Unresolved Switch {address}" if unknown else f"Unused Switch {address}"),
				"virtual", SWITCH, address, "unknown" if unknown else "unused", status, CORE, CHART if chart_unused else CORE_COMMON)
			if unknown:
				d["physical"] = {"notes": "CPU read path reaches this address. " + ("The secondary chart prints Not Used, but no retained factory wiring verifies non-fitment; that candidate claim does not establish unused availability." if chart_unused else "This game's secondary matrix does not document it; omission does not establish non-fitment.")}
			else:
				d["spatial"] = not_applicable("unused", CORE, CHART if chart_unused else CORE_COMMON, status=status)
			inputs.append(d)
	for address in range(1, 25):
		d = device(f"dip.cpu-{address}", f"CPU DIP Bit {address}", "dip_switch", DIP, address, "used", "validated", CORE, GAME)
		d["spatial"] = not_applicable("dip_switch", CORE)
		d["physical"] = {"notes": "Public bit order from core_getDip; printed S1-S8 labels are reordered by gts1.h. Game-specific option meanings and physical S-number mapping remain uncurated."}
		inputs.append(d)
	outputs = []
	for address in range(1, 49):
		if address in SOLENOID_LABELS:
			identifier, label = SOLENOID_LABELS[address]
			d = device(identifier, label, "coil", SOLENOID, address, "used", "observed", SCRIPT, CHART, CORE)
			d["physical"] = {"notes": "Physical part, transistor, connector and wire candidates are transcribed in the secondary chart excerpt; factory schematic confirmation is outstanding."}
			if address in (2, 3, 4, 5):
				d["spatial"] = not_applicable("cabinet_or_service", CHART, SCRIPT, status="candidate")
		elif address == 17:
			d = device("signal.game-on", "Game On (Q energized and T clear)", "virtual", SOLENOID, address, "used", "validated", CORE)
			d["physical"] = {"notes": "Derived in lamp_w: lamp 1 on and lamp 2 off. Enables synthetic flippers; no additional physical coil."}
			d["spatial"] = not_applicable("virtual", CORE)
		elif 45 <= address <= 48:
			side = "right" if address <= 46 else "left"
			d = device(f"signal.{side}-flipper-{address}", f"Synthetic {side.title()} Flipper Output {address}", "virtual", SOLENOID, address, "used", "validated", CORE_COMMON, CORE, GAME)
			d["physical"] = {"notes": f"Button {82 if side == 'right' else 84} publishes this pair while game-on is true. No driver-board output or independently measured winding state. The right button moves both right-side flippers in the script."}
			d["spatial"] = not_applicable("virtual", CORE_COMMON)
		else:
			unknown = 9 <= address <= 12
			d = device(f"solenoid.unresolved-{address}" if unknown else f"solenoid.unused-{address}", f"Unresolved Solenoid {address}" if unknown else f"Unpublished Solenoid {address}", "virtual", SOLENOID, address, "unknown" if unknown else "unused", "candidate" if unknown else "validated", CORE, CORE_COMMON)
			if unknown:
				d["physical"] = {"notes": "U4 ioport can write this bit; no load or runtime purpose is established. A sweep alone would not establish physical fitment."}
			else:
				d["spatial"] = not_applicable("unused", CORE, CORE_COMMON)
		outputs.append(d)
	for address in range(1, 65):
		if address in LAMP_LABELS:
			identifier, label, kind = LAMP_LABELS[address]
			d = device(identifier, label, kind, LAMP, address, "used", "candidate" if address <= 3 else "observed", CHART, SCRIPT, CORE)
			d["physical"] = {"notes": "Secondary chart label; primary wiring, bulb counts and precise physical location require verification."}
			if address == 17:
				d["physical"]["notes"] += " LampCallback reads Controller.Lamp(17) and resets dtkk on its rising edge. It is a reset coil, not a lamp. Chart transistor types differ between its two tables."
			elif address in (1, 2):
				d["spatial"] = not_applicable("internal_nonvisual", CHART, CORE, status="candidate")
			elif address == 3:
				d["spatial"] = not_applicable("cabinet_or_service", CHART, BACKBOX_PHOTO, status="candidate")
			else:
				d["physical"]["notes"] += f" Script binds l{address}, an insert/render light with no shown bulb mesh. Its center is retained only in the spatial report as an unverified render anchor, not a physical emitter placement."
		else:
			chart_unused = address <= 36
			unknown = chart_unused or 37 <= address <= 44
			d = device(f"lamp.unresolved-{address}" if unknown else f"lamp.unused-{address}", f"Unverified Not Used Lamp {address}" if chart_unused else (f"Unresolved Lamp Driver {address}" if unknown else f"Unused Lamp {address}"), "virtual", LAMP, address, "unknown" if unknown else "unused", "candidate" if unknown or chart_unused else "validated", CORE, CHART if chart_unused else CORE_COMMON)
			if unknown:
				d["physical"] = {"notes": "The emulator's lamp latch writes can reach this bit. " + ("The secondary chart prints Not Used, but no retained factory wiring verifies non-fitment; that candidate claim does not establish unused availability." if chart_unused else "The game's secondary chart ends at L36. Physical fitment and runtime purpose remain unresolved.")}
			else:
				d["spatial"] = not_applicable("unused", CORE, CHART if chart_unused else CORE_COMMON, status="candidate" if chart_unused else "validated")
		outputs.append(d)
	mechanisms = []
	for slug, label, actuator, addresses in [
		("ten-jacks", "Ten and Jacks Shared Reset Group", "coil.ten-jacks-reset", [21,22,23]),
		("queens", "Queens Three-Target Bank", "coil.queens-reset", [31,32,33]),
		("kings", "Kings Four-Target Bank", "coil.kings-reset", [41,42,43,44]),
		("aces-joker", "Aces and Joker Five-Target Bank", "coil.aces-reset", [50,51,52,53,54]),
	]:
		mechanisms.append({"id": "mechanism." + slug, "label": label, "kind": "drop_target_bank", "actuators": [actuator], "sensors": ["switch." + SWITCH_LABELS[n][0] for n in addresses],
			"behavior": "Each struck target drops and its scoring state remains set until the reset output lifts the group. " + ("The isolated Ten target and two Jacks are separated on the playfield and share solenoid 6; do not model them as three adjacent targets." if slug == "ten-jacks" else "The ordered target/switch mapping is given by the exact InitDrop array in the runtime excerpt.") + " Factory reset linkage, pulse duration, jam behavior and power-on physical state remain unverified.", "provenance": provenance("observed", SCRIPT, CHART, PHOTO)})
	mechanisms += [
		{"id": "mechanism.outhole", "label": "Single-Ball Outhole and Serve", "kind": "kicker", "actuators": ["coil.outhole"], "sensors": ["switch.outhole"], "behavior": "Drain_Hit adds the ball to cvpmBallStack.InitNoTrough, which supplies switch 66 until solenoid 1 serves through the BallRelease proxy. This is an occupied ball state, not a coil-to-switch electrical relationship. Recreate the manual shooter lane and passive plunger separately; ejection tuning belongs to the table. Physical eject path, sensor position and timing remain unverified.", "provenance": provenance("observed", SCRIPT, CHART)},
		{"id": "mechanism.direct-coils", "label": "Directly Switched Pops, Kicking Rubber and Flippers", "kind": "other", "actuators": [], "sensors": ["switch.pop-bumpers", "switch.ten-point-contacts", "switch.left-flipper-button", "switch.right-flipper-button"], "behavior": "Two pops share CPU score input 10. The single powered left kicking rubber shares score input 40 with passive contacts. Three flippers are cabinet-button switched, with the top flipper tied to the right button. They are not additional numbered solenoid drivers; use physical/table behavior and synthetic flipper states as documented. Direct power contacts, EOS wiring and exact assemblies require the primary schematic.", "provenance": provenance("candidate", CHART, SCRIPT, PHOTO)},
	]
	displays = []
	for index, (slug, label, start, width) in enumerate([
		("player-1", "Player 1 Score", 12, 6), ("player-2", "Player 2 Score", 18, 6),
		("player-3", "Player 3 Score", 0, 6), ("player-4", "Player 4 Score", 6, 6),
		("ball", "Ball in Play", 40, 2), ("credits", "Credits", 32, 2),
	]):
		displays.append({"id": "display." + slug, "label": label, "kind": "segment", "controller_index": index,
			"segment_start": start, "width": width, "height": 1, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", GAME, BACKBOX_PHOTO, status="observed"), "provenance": provenance("validated", GAME)})
	return {"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Joker Poker", "manufacturer": "Gottlieb", "year": 1978, "kind": "physical_pinball", "model_number": "417 SS", "ipdb_id": 1306, "opdb_id": "GR9o1-MQjj8", "playfield": {"width": 952, "height": 1927, "units": "vpx", "provenance": provenance("observed", TABLE)}},
		"controller": {"platform": "pinmame.gts1", "hardware_generation": "0x100000000", "inversion_applied_by_emulator": True},
		"coverage": {"status": "partial", "missing": ["input_semantics", "output_semantics", "mechanism_inventory", "mechanism_behavior", "polarity", "provenance", "spatial_placement"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "candidate", "mechanisms": "observed", "variant_coverage": "validated", "recreation_knowledge": "observed", "spatial_placement": "observed", "runtime_observation": "unknown", "causal_exercise": "unknown"}},
		"drivers": [{"id": "jokrpokr", "clone_of": "gts1", "description": "Joker Poker", "year": "1978", "manufacturer": "Gottlieb", "flags": 0, "physical_compatibility": "identical", "variant_notes": "The pinned catalog has this single game driver, using 417.cpu, INIT_S1, GEN_GTS1, sys1_disp and the chime machine module. gts1 is a non-game system root, not another Joker Poker variant. The same-titled electromechanical game has no place in this physical SS record."}],
		"inputs": inputs, "outputs": outputs, "displays": displays, "mechanisms": mechanisms, "relationships": [],
		"sources": sources(root), "knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": "partial"}, "conflicts": []}


def build_spatial_report(definition):
	return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"decision": "partial; physical wiring/polarity, full mechanisms, emitter inventory and positions remain incomplete",
		"coordinate_system": "x=0 left, x=1 right; y=0 rear/backglass, y=1 apron; (x/952,y/1927), official helper rounds to six decimals",
		"evidence": {"vpx": {"root": VPX_RELATIVE.as_posix(), "file": TABLE_FILE, "sha256": TABLE_SHA256, "tool": "vpxtool git:v0.33.3", "extraction": "extracted", "manifest_sha256": EXTRACTION_MANIFEST_SHA256, "file_count": 1031, "byte_count": 67599557, "manifest_algorithm": "tools/build_external_evidence_manifest.py: all relative POSIX paths sorted case-sensitively, size and SHA256; compact sorted-key UTF-8 JSON plus LF, excluding manifest.json and manifest.sha256", "spatial_candidates_sha256": SPATIAL_CANDIDATES_SHA256}, "technical_chart": {"file": CHART_FILE, "sha256": CHART_SHA256, "role": "secondary candidate wiring only"}},
		"bound_object_points": {name: {"x": point[0], "y": point[1]} for name, point in sorted(POINTS.items())},
		"projections": ["Scoring-rubber wall drag-point centroids are candidate interaction regions, not measured switch contacts; no bulb or reset-coil locations are inferred.", "Drop-target centers locate observed target sensors; no physical reset-solenoid anchor is claimed.", "BallRelease is a virtual ejection proxy; outhole sensor and coil placements are withheld."],
		"unclaimed_render_light_objects": [f"l{n}" for n in sorted(LAMP_LABELS) if n not in (1,2,3,17)],
		"unverified_render_light_points": {name: {"x": point[0], "y": point[1], "status": "candidate", "physical_socket_verified": False} for name, point in sorted(RENDER_POINTS.items())},
		"lamp_policy": "Lights maps 21 insert/glow objects without shown bulb meshes. They identify runtime render regions, not physical emitter centers or counts. No canonical lamp placements or bulb quantities are inferred.",
		"gi_policy": "The table forces GI collection on and uses no GI callbacks. The secondary fuse table describes playfield/coin-chute and name/scene circuits; primary wiring and socket inventory remain outstanding. No fictitious controller GI address is assigned.",
		"unresolved_switches": [d["binding"]["device"] for d in definition["inputs"] if d["availability"] == "unknown"],
		"unresolved_outputs": [{"group": d["binding"]["group"], "address": d["binding"]["device"]} for d in definition["outputs"] if d["availability"] == "unknown"],
		"missing_spatial": [d["id"] for section in ("inputs", "outputs") for d in definition[section] if d.get("availability") != "unused" and "spatial" not in d],
		"promotion_blockers": definition["coverage"]["missing"]}


def render_report(report):
	return "# Joker Poker (1978) spatial blockers\n\n" + report["decision"] + ".\n\n" + report["coordinate_system"] + ".\n\n" + report["lamp_policy"] + "\n\n" + report["gi_policy"] + "\n\n" + "\n".join("- " + p for p in report["projections"]) + "\n\nSee the adjacent JSON for exact artifact hashes, extraction manifest, every bound-object coordinate, unresolved addresses and missing placements.\n"


def check_external_evidence():
	from build_external_evidence_manifest import check_manifest
	from pinmame_game_defs.spatial import extract_spatial_candidates
	def verify(path, expected):
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
			raise RuntimeError(f"missing or changed external evidence: {path}")
	if text := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
		root = Path(text) / VPX_RELATIVE
		verify(root / TABLE_FILE, TABLE_SHA256)
		verify(root / "extracted/script.vbs", SCRIPT_SHA256)
		verify(root / "spatial-candidates.json", SPATIAL_CANDIDATES_SHA256)
		if check_manifest(root / "extracted", "jokrpokr") != EXTRACTION_MANIFEST_SHA256:
			raise RuntimeError("retained extraction manifest drift")
		for name, digest in LIBRARY_HASHES.items():
			verify(root / "libraries" / name, digest)
		points = extract_spatial_candidates(root / "extracted", root / TABLE_FILE, "vpxtool git:v0.33.3")
		actual = {item["name"]: (item["x"], item["y"]) for item in points["objects"]}
		for name, point in (POINTS | RENDER_POINTS).items():
			if actual.get(name) != point:
				raise RuntimeError(f"bound object coordinate drift: {name}: {actual.get(name)} != {point}")
	if text := os.environ.get("PINMAME_MANUALS_ROOT"):
		verify(Path(text) / "by-machine" / MACHINE_ID / CHART_FILE, CHART_SHA256)
	if text := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
		root = Path(text) / MACHINE_ID
		verify(root / "photos/ipdb-1306-32830-illuminated-playfield.jpg", "2454e148c09fce41cf227252cd9d002526d781a961e7df3238ffa7a0b76d26bc")
		verify(root / "photos/ipdb-1306-12959-backglass.jpg", "41edd4c8e93c96df071194faa3d4136a5409c53d258efefb93e94144401b7670")
		verify(root / "runtime/log-diagnostic-arguments.json", "eb85ad85fe8bf58f3f91c729bf893305805aff6b67d6aedc67a74b1cb373f1ef")


def artifacts(root=ROOT):
	definition = build(root)
	report = build_spatial_report(definition)
	return {DEFINITION_PATH: canonical_bytes(definition), SEED_PATH: canonical_bytes(definition),
		REPORT_PATH: canonical_bytes(report), REPORT_MARKDOWN_PATH: render_report(report).encode("utf-8"),
		KNOWLEDGE_PATH: (root / KNOWLEDGE_SEED_PATH).read_bytes()}


def check(root=ROOT):
	if (root / "machines/author-ready/gottlieb/joker-poker-1978.json").exists():
		raise RuntimeError("refuse to overwrite an existing author-ready definition")
	for path, expected in artifacts(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != expected:
			raise RuntimeError(f"curated artifact drift: {path}")
	check_external_evidence()


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--check", action="store_true")
	group.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	if args.check:
		check()
	else:
		if (ROOT / "machines/author-ready/gottlieb/joker-poker-1978.json").exists():
			raise RuntimeError("refuse to overwrite an existing author-ready definition")
		check_external_evidence()
		for path, payload in artifacts().items():
			path = ROOT / path
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(payload)
	print("Joker Poker partial curation is deterministic")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
