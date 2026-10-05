"""Deterministic curation of the four Spooky Pinball pinHeck games.

America's Most Haunted (2014), Domino's Spectacular Pinball Adventure (2016), Rob Zombie's Spookshow
International (2016) and The Jetsons (2017) run on one board and one PinMAME platform
(controllers/pinmame/pinheck.json), so one curator builds all four records from the same inputs:

- tools/pinheck_charts.json: the factory switch, lamp and wire-to-board charts, transcribed from the
  PDFs' text layer and checked against their renders (the excerpts under evidence/excerpts/<machine>/);
- tools/pinheck_runtime.json: the compact summary of the retained LibPinMAME service-test and game-start
  runs (tools/pinheck_runtime.py), including the curator's reading of every frame it relies on;
- the pinned PinMAME source (97aa922b) for the controller contract and the driver sets;
- tools/pinheck_photo_placements.json: for Rob Zombie's Spookshow International and The Jetsons, positions measured on
  playfield photographs rectified at playfield level (each game's frame method and uncertainty are stated in it);
- tools/amh_lw_placements.json: for America's Most Haunted, the LW recreation table object that places each device
  and the script line that binds it (the only pinHeck game with a retained recreation).

``--check`` regenerates in memory and refuses drift; ``--regenerate`` writes; ``--game`` limits either to
one game. Bare CI needs no external files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.identifiers import slug
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes

ROOT = Path(__file__).resolve().parents[1]
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
REV12 = REVISION[:12]
# The retained runtime runs were recorded with LibPinMAME built at this earlier revision, which named each set after the game
# alone (amh, dominos, rzspook, jetsons); 97aa922b renamed them after their code version and added America's Most Haunted V22.
RUN_REVISION = "b7a60eb0dd9722f5397fc296987d94528ab111ff"
CHARTS = load_json(ROOT / "tools/pinheck_charts.json")
RUNTIME = load_json(ROOT / "tools/pinheck_runtime.json")
CURATOR = "the curator on 2026-10-05"
CHART_READER = "transcribed from the PDF text layer (the RZ wiring chart from its raster) and checked against the renders on 2026-10-05"
PROFILE = "controller-profile.pinmame-pinheck"
CATALOG = f"pinmame.catalog.{REV12}"
CORE = f"pinmame.core.{REV12}"
BOARD = f"pinmame.board.{REV12}"
PINHECK_GEN = "0x10000000000000"
SWITCH, SOLENOID, LAMP = "pinmame.input.switch", "pinmame.output.solenoid", "pinmame.output.lamp"

# America's Most Haunted's LW recreation (v2.0 by freneticamnesic, Shoopity and LoadedWeapon): its own game code, no ROM, but
# laid out like the real machine and numbered after the factory charts. Every canonical coordinate is x/952 and y/2185.
AMH_TABLE = {
	"filename": "America's Most Haunted (Spooky Pinball 2014) LW.vpx", "sha256": "c677c6b98bfd563f4ae83dc93bd5c6f807b9bce6b380063655b9e40e595d0500",
	"bytes": 347865088, "width": 952.0, "height": 2185.0, "relative": "spooky-pinball/america-s-most-haunted-2014/lw",
	"manifest_sha256": "b717aa8414042919fc8fd55e9de9a469d078f819f9c61908163d04a9ceb470e2", "file_count": 2185, "total_bytes": 388534248,
	"script_sha256": "ffaeea988c8e27d2d7768c4cfcdfe280776e4b108921c1f728ec51bfff099a0d", "script_bytes": 618900,
	"obj_sha256": "6ed05f976f7b5d01ed85c31449ebe3e5334953eaa95df310f7c8228c730adfa1", "obj_bytes": 65869696,
	"obj": "obj-vpu/America's Most Haunted (Spooky Pinball 2014) LW.obj",
}
# America's Most Haunted V22 (amh_022): the two retained downloads and what was read from them. ROM bytes stay external.
AMH_V22 = {
	"card": {"id": "rom.amh-v22-card", "filename": "AMH_SD.zip", "url": "https://www.benheck.com/Downloads/amh/AMH_SD.zip",
	         "sha256": "0bad77fd8c692fed60fe056c97a3a2362a38bd449409e43c6d8eb9002dd24964", "bytes": 595918968, "acquired_at": "2026-10-05T20:43:08Z",
	         "last_modified": "2025-02-23T17:38:32Z", "member": "DMD/PROP_022.bin", "crc": "53a6b98b", "sha1": "6427841d9f3ac6a744bf86856dfd3faf58e43828"},
	"hex": {"id": "rom.amh-v22-hex", "filename": "AMH_V022.hex", "url": "https://www.benheck.com/Downloads/pinball_update_hex/AMH_V022.hex",
	        "sha256": "b9271c8ea1df39f195a2946efa5af24b41d95abb042c73a56970de005776b82d", "bytes": 612459, "acquired_at": "2026-10-05T20:42:43Z",
	        "last_modified": "2025-02-23T17:45:43Z", "crc": "b74f2a7b", "sha1": "4a36e71ba9fcfcd5779645e849babeed5a842c0b"},
	# VERSION.TXT at the card's root, 88 bytes with CRLF line ends.
	"version_txt": "GAME: America's Most Haunted\r\n\r\nCODE REVISION: 22\r\n\r\nA/V REVISION: 22\r\n\r\nDATE: 10/3/2015",
	"version_sha256": "bfd9e8904b7dc3089d7d13ed4b5abaa836939e0f6de271b8beeb7545b5b175a2",
}
# Rob Zombie's Spookshow International and The Jetsons: positions measured on photographs (tools/pinheck_photo_placements.json).
PHOTO = load_json(ROOT / "tools/pinheck_photo_placements.json")["games"]

# How each kind of placement point is taken from the table (the spatial report's projection classes).
AMH_PROJECTIONS = {
	"object_centre": "The object's own centre (Light, Trigger, Kicker and Bumper centre fields): the bulb, switch or kicker itself.",
	"wall_centroid": "The mean of a target or slingshot wall's drag points: the target face or slingshot the switch sits on.",
	"flipper_pivot": "The flipper's centre, its pivot: the end-of-stroke contacts and both windings sit on the flipper assembly and have no object of their own.",
	"servo_axis": "A primitive's position about which the script turns it (ObjRotZ): the Spooky Door's hinge and the ghost's spindle, where each servo sits; their mesh centres are recorded beside them.",
	"servo_assembly": "A primitive the script moves vertically, at its position, which agrees with its exported mesh centre within two units: the Hellevator car and the target bank.",
	"flasher_bulb": "The light a timer copies from the flasher lamp's placeholder, beside the modelled dome base.",
	"shared_rgb": "One point for the ghost LED's three channels, declared as a shared RGB emitter.",
}
AMH_TABLE_SOURCE, AMH_SCRIPT_SOURCE = "vpx-table.amh-lw-2-0", "vpx-script.amh-lw-2-0"
AMH_PLACEMENTS = load_json(ROOT / "tools/amh_lw_placements.json")
# Used devices the table cannot place, and why.
AMH_UNPLACED = {
	(SWITCH, 54): "BASEMENT UPPER [35] is a switch in the basement subway under the playfield; the table models the subway off the playfield (TrSw35 at x=1026.5), so it has no playfield position.",
	(SWITCH, 55): "BASEMENT LOWER [36] is a switch in the basement subway; the table's TrSw36 sits off the playfield at x=1027.",
	**{(SOLENOID, address): ("The on-board RGB LEDs light the cabinet's left and right playfield edges (the script's leftRGB and rightRGB, "
	                         "'cabinet GI'); nothing retained says which LED feeds which side, and the table draws each side as a row of "
	                         "about 35 lights, not as the physical strip.") for address in range(51, 57)},
}
CORE_FILES = {
	CORE: ("src/wpc/pinheck.c", "bab6056f69236a77fa3b95641dec94a99cd29c38925df8d0f836e02103d181b9",
	       "file header; PINHECK_SOL_*, PINHECK_LAMP_ST; pinheck_brd_swcol/cab/lamps/sols/gi/start/rgb/servo; pinheck_sw2m/lamp2m/m2sw; "
	       "pinheck_getsol; pinheck_brd_init/reset/vblank; SWITCH_UPDATE(pinheck); pinheck_vblank (core_updateSw(0))"),
	BOARD: ("src/wpc/pinheck/board.c", "7f46c9a93a9a2fbb51816d510ccb5cee28c46a23324531c35484f97c42e93b5b",
	        "coil port/bit tables, watchdog, lamp strobe, GI 74HC595, cabinet 74HC165, WS2801 chains, servo timing, switch read"),
}

GAMES: dict[str, dict[str, Any]] = {
	"amh": {
		"machine": "spooky-pinball.america-s-most-haunted.2014", "stem": "spooky-pinball/america-s-most-haunted-2014",
		"name": "America's Most Haunted", "year": 2014, "model": "AMH01", "ipdb": 6161, "opdb": "G4ELZ-MQ27w", "firmware": "V23",
		"sim": ("src/wpc/sims/pinheck/amh.c", "dc0d1902ffd11fb20791bbdaef057ca1eaa67be6d96c8e42f8cdff6f7a055a09"),
		"rom": "AMH_SD_V023.zip from benheck.com with AMH_V023.hex added to the root, as the PinMAME pull request describes; the PIC32 runs the Intel HEX, the Propeller PROP_023.BIN (CRC bd5a99e8) from DMD/",
		"drivers": {"amh_023": None,
		            "amh_022": ("The earlier code update V22 (the card's VERSION.TXT: code and A/V revision 22, dated 10/3/2015): benheck.com's "
		                        "AMH_SD.zip card with AMH_V022.hex from its pinball_update_hex folder added to the root; the PIC32 runs the Intel "
		                        "HEX (CRC b74f2a7b), the Propeller DMD/PROP_022.bin (CRC 53a6b98b). It runs on the same board and playfield and "
		                        "shares V23's switch, lamp and output definitions in PinMAME. Every retained runtime run used V23; PinMAME notes "
		                        "that its DMD frame address is verified for V23 only, while the display itself is decoded from the scan pins. "
		                        "Sources rom.amh-v22-card and rom.amh-v22-hex record both downloads, the card's VERSION.TXT and the CRC check.")},
		"display": {"kind": "dmd", "width": 128, "height": 32, "label": "128x32 dot matrix (raw DMD scanned by a Propeller cog)"},
		"editions": [(6161, "America's Most Haunted", "150 units (confirmed), first produced March 21, 2014, two art packages (Reality Green and Animated Blue)")],
		"documents": {"switch": "AMH_Switch_Matrix_Production.pdf", "lamp": "AMH_Light_Matrix_Production.pdf", "wiring": "AMH-WIRE-TO-BOARD.pdf"},
		"servos": {57: "Hellevator", 58: "Spooky Door", 59: "Ghost", 60: "Target"},
		"servo_rom": {57: ["HELL UP", "HELL DOWN"], 58: ["DOOR OPEN", "DOOR CLOSE"], 59: ["GHOST LEFT", "GHOST MIDDLE", "GHOST RIGHT"], 60: ["TARGET UP", "TARGET DOWN"]},
		"rgb": {51: "RGB1 red", 52: "RGB1 green", 53: "RGB1 blue", 54: "RGB2 red", 55: "RGB2 green", 56: "RGB2 blue", 62: "Ghost red",
		        63: "Ghost green (REV 1) or blue (REV 2)", 64: "Ghost blue (REV 1) or green (REV 2)"},
		"rgb_rom": ("RGB1=RED/GREEN/BLUE light 51/52/53; RGB2=RED/GREEN/BLUE light 54/55/56; the ghost is on-board WS2801 LED 2 (onbLed2), "
		            "and the test's GHOST TYPE item, REV 1 on a fresh NVRAM, selects its channel order: under REV 1 GHOST=RED/GREEN/BLUE "
		            "light 62/63/64, and after Enter on that item switches it to REV 2 they light 62/64/63"),
		"rgb_notes": {address: ("The ROM swaps the ghost LED's green and blue bytes between the two GHOST TYPE settings, so what this "
		                        f"channel shows depends on the operator setting: {colours}. The setting presumably matches two "
		                        "revisions of the ghost LED; no retained source says which revision a given machine carries.")
		              for address, colours in ((63, "green under REV 1 (the default), blue under REV 2"),
		                                       (64, "blue under REV 1 (the default), green under REV 2"))},
		"optos": {95: "the Ghost Loop opto (opto 1 on the aux board, yellow/red)", 96: "the Spooky Door opto (opto 2 on the aux board, yellow/blue)"},
		"trough": [84, 85, 86, 87],
		"manual_plunger": True,
	},
	"dominos": {
		"machine": "spooky-pinball.domino-s-spectacular-pinball-adventure.2016", "stem": "spooky-pinball/domino-s-spectacular-pinball-adventure-2016",
		"name": "Domino's Spectacular Pinball Adventure", "year": 2016, "model": "00003", "ipdb": 6418, "opdb": "GxvQ7-MNE7O", "firmware": "V6",
		"drivers": {"dominos_006": None},
		"sim": ("src/wpc/sims/pinheck/dominos.c", "4f9ef11b89c7d3f380a421f27ce9f6d0ed8f313d91ed422a77c99e6b9876d590"),
		"rom": "Spooky's DOM_v6.zip code update: DOM_V006.PRG, PRP_V008.BIN and the SD card's DMD/ and SFX/ folders",
		"display": {"kind": "video", "width": 128, "height": 32, "label": "128x32 RGB332 serial colour display"},
		"editions": [(6418, "Standard Edition", "about 60 units, production from October 17, 2016"),
		             (6586, "Limited Edition", "75 units, November 2016; IPDB: exactly the same as the Standard Edition except the backglass art and the LE metal plaque")],
		"documents": {"switch": "Dominos-Switch-Matrix.pdf", "lamp": "Dominos-Lamp-Matrix.pdf", "wiring": "DOMINOS-WIRE-TO-BOARD.pdf"},
		"solenoid_list": "2016_Domino_s_Spectacular_Pinball_Adventure_Standard_Edition_Domino_s_Pinball_Solenoid_List.pdf",
		"servos": {57: "Noid Orbit", 58: "Target Bank"},
		"servo_rom": {57: ["NOID RIGHT", "NOID STOP", "NOID LEFT"], 58: ["TARGET DOWN", "TARGET UP"]},
		"rgb": {51: "RGB1 red", 52: "RGB1 green", 53: "RGB1 blue", 54: "RGB2 red", 55: "RGB2 green", 56: "RGB2 blue"},
		"rgb_rom": "RGB1 RED/GREEN/BLUE light 51/52/53 (WHITE all three), RGB2 RED/GREEN/BLUE light 54/55/56",
		"optos": {95: ("one of the two cabinet optos; the charts do not say which. The wire chart's OPTOS box names an Opto - 3 "
		               "'Noid Loop' and an Opto - 4 'Scoop' pair (its captions sit over the other header's colours), the switch chart "
		               "prints cabinet cells 13 and 14 as just 'Opto', the ROM's Switch Edge test does not name them, and PinMAME's "
		               "simulator calls 95 the center ramp opto and 96 the oven ramp opto"),
		          96: "the other of the two cabinet optos (see 95)"},
		"cabinet_labels": {13: "Opto (cabinet 13)", 14: "Opto (cabinet 14)"},
		"missing": ["input_semantics", "mechanism_behavior", "output_semantics", "spatial_placement"],
		"rgb_unnamed": "The ROM holds all three channels at full, white, from attract mode through its RGB test, which never names them; the wire chart's RGB Com Out header leads to an external WS2801 chain whose load neither chart names.",
		"trough": [12, 13, 14],
		"manual_plunger": True,
	},
	"rzspook": {
		"machine": "spooky-pinball.rob-zombie-s-spookshow-international.2016", "stem": "spooky-pinball/rob-zombie-s-spookshow-international-2016",
		"name": "Rob Zombie's Spookshow International", "year": 2016, "model": "00002", "ipdb": 6416, "opdb": "G5pp2-ME0eP", "firmware": "V26",
		"drivers": {"rzspook_026": None},
		"sim": ("src/wpc/sims/pinheck/rzspook.c", "7393a81c2afe259b9f3375a9e2b3e23d732649d820bb60da4a4ec4b88bf6a312"),
		"rom": "Spooky's rzupdate_V26.zip code update (Google Drive link on spookypinball.com): RZO_V026.PRG, PRP_V008.BIN and the SD card's DMD/ and sound folders",
		"display": {"kind": "video", "width": 128, "height": 32, "label": "128x32 RGB332 serial colour display (the \"Chroma Corpse\" display)"},
		"editions": [(6416, "Standard Edition", "250 units (confirmed), February 2016"),
		             (6417, "Limited Edition", "50 units (confirmed); IPDB: a different backglass, different side rails and a numbered plaque")],
		"documents": {"switch": "RZ_Switch_Matrix_Production.pdf", "lamp": "RZ_Lamp_Matrix_Production.pdf", "wiring": "wiring-board-chart.png"},
		"servos": {57: "Spaulding (gate)", 58: "Robot"},
		"servo_rom": {57: ["GATE OPEN", "GATE CLOSE"], 58: ["ROBOT START", "ROBOT END"]},
		"rgb": {51: "RGB1 red", 52: "RGB1 green", 53: "RGB1 blue", 54: "RGB2 red", 55: "RGB2 green", 56: "RGB2 blue", 62: "Living Dead Girl red", 63: "Living Dead Girl blue", 64: "Living Dead Girl green"},
		"rgb_rom": "RGB1 RED/GREEN/BLUE light 51/52/53, RGB2 RED/GREEN/BLUE light 54/55/56; LDG RED lights 62, LDG GREEN 64 and LDG BLUE 63, so the Living Dead Girl LED's green and blue arrive on PinMAME's B and G slots",
		"optos": {95: "the Spaulding opto at the upper playfield gate (Opto - 4)", 96: "the upper playfield exit opto (Opto - 3)"},
		"trough": [12, 13, 14, 15, 16, 17, 18],
		"manual_plunger": True,
	},
	"jetsons": {
		"machine": "spooky-pinball.the-jetsons.2017", "stem": "spooky-pinball/the-jetsons-2017",
		"name": "The Jetsons", "year": 2017, "model": "00004", "ipdb": 6577, "opdb": "GweVl-Mb5lx", "firmware": "V4", "manufacturer": "The Pinball Company",
		"drivers": {"jetsons_004": None},
		"sim": ("src/wpc/sims/pinheck/jetsons.c", "7a0f27cc1b868d0e7b249217a3a0c63665573aa58e3f07b90da4b5d31073c9a7"),
		"rom": "Spooky's Jetsons_Code.zip code update: Jetsons/JET_V004.PRG, Jetsons/PRP_V002.BIN and the SD card's folders",
		"display": {"kind": "video", "width": 128, "height": 64, "label": "128x64 colour display"},
		"editions": [(6577, "Regular Edition", "75 units (confirmed), charcoal grey armour"),
		             (6608, "Special Edition", "25 units (confirmed), purple armour and a backbox topper")],
		"documents": {"switch": "Jetsons_Switch_Matrix_Production.pdf", "lamp": "Jetsons_Light_Matrix_Production.pdf", "wiring": "JETSONS-WIRE-TO-BOARD.pdf"},
		"solenoid_list": "2017_The_Jetsons_Regular_Edition_Jetsons_Solenoid_List.pdf",
		"servos": {57: "Orbitty topper (Special Edition)"},
		"optional_servos": {57: "IPDB lists the topper only on the Special Edition (IPDB 6608), so only those 25 machines carry this servo."},
		"unknown_servos": {58: ("Servo 1 (chart: Open)", "The wire chart's SERVOS box reads 'Topper - 0 / Open - 1' and the switch chart "
		                        "leaves SERVO 1 unnamed, so no retained source names a load; yet the ROM holds a non-zero position "
		                        "here from attract mode on in every run, which nothing explains. This firmware has no Servo test.")},
		"rgb": {51: "RGB1 red", 52: "RGB1 green", 53: "RGB1 blue", 54: "RGB2 red", 55: "RGB2 green", 56: "RGB2 blue"},
		"rgb_rom": "RGB1 RED/GREEN/BLUE light 51/52/53 (WHITE all three), RGB2 RED/GREEN/BLUE light 54/55/56",
		"rgb_unnamed": ("The ROM's RGB test never names or lights this channel and it stays at 0 in every run, but the wire chart "
		                "prints an RGB Com Out header for an external WS2801 chain and PinMAME publishes only that chain's first LED, "
		                "so a constant 0 here does not show that nothing is connected."),
		"optos": {92: "the first trough position (Opto6, Trough emitter/receiver)", 93: "the trough jam opto (Opto5)", 96: "the scoop opto (Opto - 3)"},
		"trough": [52, 53, 54, 92],
		"manual_plunger": False,
	},
}


# ---------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------
def public_number(n: int) -> int:
	"""Factory switch or lamp number 0-63 to its public address: (n / 8 + 1) * 10 + n % 8 + 1."""
	return (n // 8 + 1) * 10 + n % 8 + 1


def factory_number(address: int) -> int:
	return (address // 10 - 1) * 8 + address % 10 - 1


def cabinet_public(n: int) -> int:
	return n if n < 9 else n + 82


def gi_public(pin: int) -> int:
	return 25 + pin if pin < 8 else 29 + pin


def current_driver(game: str) -> str:
	"""The PinMAME set that runs the code the retained runs used."""
	return next(iter(GAMES[game]["drivers"]))


def ids(game: str) -> dict[str, str]:
	key = GAMES[game]["machine"].split(".")[1]
	return {"switch": f"spooky.switch-matrix.{key}", "lamp": f"spooky.lamp-matrix.{key}", "wiring": f"spooky.wire-to-board.{key}",
	        "sim": f"pinmame.sim.{game}.{REV12}", "ipdb": f"ipdb.{GAMES[game]['ipdb']}", "list": f"ken-layton.solenoid-list.{key}",
	        **{f"rt-{test}": f"runtime.{game}.{test}" for test in RUNTIME["games"][game]["runs"]}}


def prov(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...],
           status: str = "validated") -> dict[str, Any]:
	namespace = {SWITCH: "pinmame.switch", SOLENOID: "pinmame.solenoid", LAMP: "pinmame.lamp"}[group]
	return {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
	        "aliases": [{"namespace": namespace, "value": str(address)}], "availability": availability,
	        "provenance": prov(*refs, status=status)}


def runs(game: str) -> dict[str, Any]:
	return RUNTIME["games"][game]["runs"]


def chart(game: str) -> dict[str, Any]:
	return CHARTS[game]


def clean(text: str) -> str:
	return " ".join(text.replace("“", "\"").replace("”", "\"").split())


# ---------------------------------------------------------------------------------------------
# What the ROM's own service tests show (tools/pinheck_runtime.json)
# ---------------------------------------------------------------------------------------------
def rom_coils(game: str) -> dict[int, str]:
	"""Solenoid test: the item name shown, and the one coil address Enter fired while it was shown."""
	steps = {step["label"]: step for step in runs(game)["solenoid"]["steps"]}
	result: dict[int, str] = {}
	for label, step in steps.items():
		if not label.startswith("Item "):
			continue
		fired = [int(n) for n, peak in steps[f"Enter on item {label[5:]}"]["solenoid_peaks"].items() if int(n) <= 24 and peak == 255]
		if len(fired) != 1:
			raise ValueError(f"{game}: solenoid test {label} fired {fired}")
		if result.get(fired[0], step["displayed_text"]) != step["displayed_text"]:
			raise ValueError(f"{game}: coil {fired[0]} shown under two names")
		result[fired[0]] = step["displayed_text"]
	if sorted(result) != list(range(1, 25)):
		raise ValueError(f"{game}: the solenoid walk did not reach every coil")
	return result


def rom_gi(game: str) -> dict[int, str]:
	"""Lamp test GI items: the item name and the single GI output lit while it was shown."""
	result: dict[int, str] = {}
	for step in runs(game)["lamp"]["steps"]:
		gi = [n for n in step["active_solenoids"] if 25 <= n <= 44]
		if step["label"].startswith("Item ") and len(gi) == 1 and not [n for n in step["active_lamps"] if n != 91]:
			result.setdefault(gi[0], step["displayed_text"])
	if sorted(result) != [*range(25, 33), *range(37, 45)]:
		raise ValueError(f"{game}: the lamp walk did not isolate all sixteen GI outputs")
	return result


def rom_lamps(game: str) -> dict[int, str]:
	"""Lamp test single-lamp items: the item name and the one matrix lamp lit while it was shown."""
	result: dict[int, str] = {}
	for step in runs(game)["lamp"]["steps"]:
		lamps = [n for n in step["active_lamps"] if n != 91]
		if step["label"].startswith("Item ") and len(lamps) == 1:
			result.setdefault(lamps[0], step["displayed_text"])
	expected = [public_number(n) for n in range(64)]
	if sorted(result) != expected:
		raise ValueError(f"{game}: the lamp walk did not isolate all 64 matrix lamps")
	for address, text in result.items():
		if [int(x) for x in re.findall(r"\d+", text)] != [factory_number(address)]:
			raise ValueError(f"{game}: lamp {address} shown as {text!r}")
	return result


def grid(game: str) -> dict[str, list[str]]:
	return runs(game)["switch"]["grid"]["drawn_by_public"]


def held_text(game: str, address: int) -> str | None:
	step = next((step for step in runs(game)["switch"]["steps"] if step["label"] == f"Close {address}"), None)
	return step.get("held_displayed_text") if step else None


# ---------------------------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------------------------
CABINET_HEADER_ADDRESS = {"door": 1, "user0": 2, "launch": 2, "r. flipper": 3, "l. flipper": 4, "menu": 5, "enter": 6,
                          "coin mech": 7, "tilt": 8, "start but": 94, "start button": 94}
READ_PATH = ("pinHeck reads the matrix uncomplemented: board.c pulls a return line low for every closed contact in the strobed "
             "column and the driver has no invSw mask, so public 1 is the closed contact. The ROM's Switch Edge test drew this "
             "closure while the host held public 1, so the contact rests open (normally_closed false), whatever its construction.")


def cabinet_wiring(game: str) -> dict[int, tuple[str, str]]:
	result: dict[int, tuple[str, str]] = {}
	for entry in chart(game)["cabinet_header"]["entries"]:
		name, _, colour = entry.partition(" - ")
		address = CABINET_HEADER_ADDRESS.get(name.strip().casefold())
		if address is not None:
			result[address] = (name.strip(), colour.strip())
	return result


NOT_WALKED = {
	1: "The Switch Edge walk toggled it separately (released, then held again) instead of closing it.",
	3: "The Switch Edge walk drives the button through 112 instead, because core_updateSw rewrites this address every vblank.",
	4: "The Switch Edge walk drives the button through 114 instead, because core_updateSw rewrites this address every vblank.",
	5: "Not closed in the Switch Edge walk because it leaves the test; every walk used it to leave the test it ran.",
	6: "Not closed in the Switch Edge walk because it restarts the test; every walk opened the operator menu and started its test with it.",
}


def drawn_note(game: str, address: int) -> str:
	if address in NOT_WALKED:
		return NOT_WALKED[address]
	drawn = grid(game).get(str(address))
	if not drawn:
		return "The ROM's Switch Edge test drew nothing for this closure."
	what = drawn[0]
	if what.startswith("matrix "):
		n = int(what.split()[1])
		return f"The ROM's Switch Edge test drew this closure at factory switch {n} (column {n // 8}, row {n % 8}) of its 8x8 grid."
	return f"The ROM's Switch Edge test drew this closure as firmware {what}."


def switch_input(game: str, address: int, label: str, availability: str, refs: tuple[str, ...], notes: str,
                 physical_extra: dict[str, Any] | None = None, status: str = "validated") -> dict[str, Any]:
	item = device(f"switch.{address:03d}-{slug(label)}", clean(label), "switch", SWITCH, address, availability, refs, status)
	text = held_text(game, address) if address in range(1, 99) and address != 1 else None
	if text:
		notes += f" While it was held the ROM printed {text!r}."
	item["physical"] = {"notes": notes, **(physical_extra or {})}
	if availability == "used":
		item["normally_closed"] = False
	return item


def inputs(game: str) -> list[dict[str, Any]]:
	g, c, i = GAMES[game], chart(game), ids(game)
	records: list[dict[str, Any]] = []
	header = cabinet_wiring(game)
	cabinet, cabinet_colour = {}, {}
	for k, v in c["cabinet_switches"].items():
		match = re.fullmatch(r"(.*?)\s*\((.*)\)", clean(v)) if game == "amh" else None
		cabinet[int(k)], cabinet_colour[int(k)] = (match.group(1), match.group(2)) if match else (clean(v), "")
	cabinet.update(g.get("cabinet_labels", {}))
	for address in range(1, 9):
		label = cabinet[address]
		refs: tuple[str, ...] = (i["switch"], CORE, PROFILE, i["rt-switch"])
		wire = header.get(address)
		notes = (f"Firmware cabinet input {address} (U12 D{address - 1}), published at {address} by pinheck_brd_cab and "
		         f"SWITCH_UPDATE(pinheck). {drawn_note(game, address)}")
		physical: dict[str, Any] = {"location": "cabinet or coin door", "switch_type": "button"}
		availability = "used" if label else "unused"
		if address == 1:
			if label:
				notes += f" The factory chart prints {label!r} in this cell."
			label = "Coin Door Closed"
			notes += (" pinheck_brd_reset sets it at every reset because the door rests closed; the ROM printed DOOR CLOSE while it "
			          "was 1 and dropped the text when the host released it, so 1 means the door is closed.")
			physical["switch_type"] = "other"
			availability = "used"
		elif address in (3, 4):
			side = "Right" if address == 3 else "Left"
			label = label or f"{side} Flipper"
			button = 112 if address == 3 else 114
			notes += (f" ROM-readable copy of the {side.lower()} flipper button: FLIP_SWNO(4, 3) makes core_updateSw copy public {button} "
			          f"into this address on every vblank, so a host drives {button}; a direct write here is overwritten.")
			availability = "used"
		elif address == 5 and not label:
			label = "Menu (Back)"
			availability = "used" if wire else "unused"
			notes += (" The factory switch chart leaves the cell blank but the wire chart's cabinet header wires 'menu' here; "
			          "PinMAME's port names the bit Back, and the ROM leaves a test on it.")
			refs = (*refs, i["wiring"])
		elif address == 2 and not label:
			label = "User Button (not fitted)"
			notes += (" PinMAME's port names the bit User; the factory chart leaves it blank and the cabinet header prints "
			          "'user0' without a wire colour.")
			refs = (*refs, i["wiring"])
		elif not label:
			label = f"Unused Cabinet Input {address}"
		if wire and wire[1]:
			notes += f" Cabinet header pin '{wire[0]}', wire {wire[1]}."
		if cabinet_colour.get(address):
			notes += f" The chart cell adds '({cabinet_colour[address]})'."
		item = switch_input(game, address, label, availability, refs, notes, physical)
		if address == 1:
			item["initial_active"] = True
		item["spatial"] = na("cabinet_or_service", i["switch"], CORE)
		records.append(item)
	columns, rows = c["switch_matrix"]["columns"], c["switch_matrix"]["rows"]
	for n in range(64):
		address = public_number(n)
		label = clean(c["switch_matrix"]["cells"][str(n)])
		column, row = divmod(n, 8)
		notes = f"Factory switch {n}, column {column}, row {row}. {drawn_note(game, address)}"
		refs = (i["switch"], CORE, i["rt-switch"], i["sim"])
		if label:
			notes += " " + READ_PATH
			if "EOS" in label.upper():
				notes += (" Flipper end-of-stroke contact read by the ROM through the matrix; the flippers are ROM-driven board "
				          "coils, so a recreation closes it when the flipper reaches its stroke.")
			item = switch_input(game, address, label, "used", refs, notes)
			if address in g["trough"]:
				item["initial_active"] = True
				item["physical"]["notes"] += " A full trough holds this contact closed at power-up."
		else:
			notes += " The factory chart leaves this cell blank: no switch is fitted. The firmware still reads the position."
			item = switch_input(game, address, f"Unused Matrix Switch {n}", "unused", refs, notes)
			item["spatial"] = na("unused", i["switch"], CORE)
		wiring = {"board": "pinHeck", "drive_connection": f"PCB switch column connector COL{column}",
		          "return_connection": f"PCB switch row connector ROW{row}"}
		if columns.get(str(column)):
			wiring["drive_wire"] = columns[str(column)]
		if rows.get(str(row)):
			wiring["return_wire"] = rows[str(row)]
		item["wiring"] = wiring
		records.append(item)
	for address in range(91, 99):
		n = address - 82
		label = cabinet.get(n, "")
		refs = (i["switch"], CORE, PROFILE, i["rt-switch"])
		if n < 16:
			notes = f"Firmware cabinet input {n} (U11 D{n - 8}), published at {address} = {n} + 82. {drawn_note(game, address)}"
		else:
			notes = ("swMatrix[9] bit 7. pinheck.c maps firmware cabinet inputs 9-15 to 91-97 only, so no firmware input reaches "
			         f"98. {drawn_note(game, address)}")
		physical = {"location": "playfield", "switch_type": "opto"} if address in g.get("optos", {}) else {"location": "cabinet", "switch_type": "button"}
		if address in g.get("optos", {}):
			notes += f" This is {g['optos'][address]}. " + READ_PATH
			refs = (*refs, i["wiring"], i["sim"])
		elif address == 94:
			notes += " Start button (swMatrix[9] bit 3, SWITCH_UPDATE's Start)."
			physical = {"location": "cabinet front", "switch_type": "button"}
		wire = header.get(address)
		if wire and wire[1]:
			notes += f" Cabinet header pin '{wire[0]}', wire {wire[1]}."
		if cabinet_colour.get(n):
			notes += f" The chart cell adds '({cabinet_colour[n]})'."
		if label:
			item = switch_input(game, address, label, "used", refs, notes, physical)
			if address in g["trough"]:
				item["initial_active"] = True
				item["physical"]["notes"] += " A full trough blocks it at power-up."
			if address not in g.get("optos", {}):
				item["spatial"] = na("cabinet_or_service", i["switch"], CORE)
		else:
			item = switch_input(game, address, f"Unused Cabinet Input {address}", "unused", refs,
			                    notes + " The factory chart leaves this cabinet input blank.")
			item["spatial"] = na("unused", i["switch"], CORE)
		records.append(item)
	for address in range(101, 109):
		item = device(f"switch.{address:03d}-unused-core-column", f"Unused Core Column {address}", "virtual", SWITCH, address, "unused", (CORE, PROFILE))
		item["physical"] = {"notes": "Internal column 10 exists because CORE_STDSWCOLS reserves twelve columns; no pinHeck code reads or writes it."}
		item["spatial"] = na("unused", CORE, PROFILE)
		records.append(item)
	for address in range(111, 119):
		bit = address - 111
		side = "Right" if address in (111, 112, 115, 116) else "Left"
		if address in (112, 114):
			cabinet_input = 3 if side == "Right" else 4
			item = device(f"switch.{address:03d}-{slug(side)}-flipper-button", f"{side} Flipper Button (PinMAME Flipper Column)", "switch",
			              SWITCH, address, "used", (CORE, PROFILE, i["rt-switch"]))
			item["roles"] = [f"flipper.lower.{side.lower()}.button"]
			item["physical"] = {"location": "cabinet flipper button", "switch_type": "button", "notes": (
				f"PinMAME's flipper column (CORE_FLIPPERSWCOL), bit 0x{1 << bit:02X}: the {side.lower()} cabinet flipper button as the "
				f"ROM receives it. core_updateSw copies it into cabinet input {cabinet_input} on every vblank; drive this address. "
				f"{drawn_note(game, address)}")}
			item["normally_closed"] = False
			item["spatial"] = na("cabinet_or_service", CORE, PROFILE)
		else:
			item = device(f"switch.{address:03d}-unused-flipper-column", f"Unused Flipper Column Bit {address}", "virtual", SWITCH,
			              address, "unused", (CORE, PROFILE))
			item["physical"] = {"notes": "core_updateSw copies only the two lower button bits; without FLIP_EOS or an upper FLIP_SW bit nothing reads this address."}
			item["spatial"] = na("unused", CORE, PROFILE)
		records.append(item)
	return records


# ---------------------------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------------------------
# Ken Layton's solenoid lists (IPDB, 2019): coil number -> (function, wire colour, coil part number) as printed.
SOLENOID_LISTS = {
	"dominos": {0: ("Knocker (optional)", "", "23-800"), 1: ("Shaker motor (optional)", "", ""), 2: ("Lower Pop Bumper", "Purple-Green", "23-800"),
	            3: ("Left Pop Bumper", "Purple-Blue", "23-800"), 4: ("Right Pop Bumper", "Purple-White", "23-800"),
	            5: ("Magnet Coil", "Purple-Gray", "20-9247"), 6: ("Up Post", "Purple-Red", "AE-27-1200"), 7: ("Not Used", "Not Used", "Not Used"),
	            8: ("Left Scoop", "Orange-Green", "23-800"), 9: ("Left Flipper High Center", "Orange-Violet", "FL-11269"),
	            10: ("Left Slingshot", "Orange-Black", "23-800"), 11: ("Left Flipper Low", "Orange-Blue", "FL-11269"),
	            12: ("Right Scoop", "Orange-White", "23-800"), 13: ("Not Used", "Not Used", "Not Used"), 14: ("Not Used", "Not Used", "Not Used"),
	            15: ("Not Used", "Not Used", "Not Used"), 16: ("Auto Launcher", "Blue-Black", "23-800"), 17: ("Ball Trough", "Blue-White", "26-1200"),
	            18: ("Right Flipper Low", "Blue-Violet", "FL-11269"), 19: ("Right Slingshot", "Blue-Red", "23-800"),
	            20: ("Right Flipper High Center", "Blue-Green", "FL-11269"), 21: ("Not Used", "Not Used", "Not Used"),
	            22: ("Not Used", "Not Used", "Not Used"), 23: ("Not Used", "Not Used", "Not Used")},
	"jetsons": {0: ("Knocker (optional)", "", "23-800"), 1: ("Shaker Motor (optional)", "", ""), 2: ("Right Flipper Low", "Orange-Green", "FL-11629"),
	            3: ("Right Flipper High Center", "Orange-Violet", "FL-11629"), 4: ("Ball Trough Load", "Orange-Black", "26-1200"),
	            5: ("Ball Launch", "Orange-Gray", "23-800"), 6: ("Left Flipper High Center", "Orange-White", "FL-11629"),
	            7: ("Left Flipper Low", "Orange-Blue", "FL-11629"), 8: ("Scoop", "Blue-Green", "23-800"), 9: ("Left Slingshot", "Blue-Red", "23-800"),
	            10: ("Right Slingshot", "Blue-Gray", "23-800"), 11: ("Not Used", "Not Used", "Not Used"), 12: ("Not Used", "Not Used", "Not Used"),
	            13: ("Not Used", "Not Used", "Not Used"), 14: ("Not Used", "Not Used", "Not Used"), 15: ("Not Used", "Not Used", "Not Used"),
	            16: ("Up Post", "Violet-Black", "AE-27-1200"), 17: ("Lower Pop Bumper", "Violet-Green", "23-800"),
	            18: ("Left Pop Bumper", "Violet-White", "23-800"), 19: ("Saucer Kick Out", "Violet-Red", "23-800"),
	            20: ("Right Pop Bumper", "Violet-Gray", "23-800"), 21: ("Not Used", "Not Used", "Not Used"),
	            22: ("Not Used", "Not Used", "Not Used"), 23: ("Not Used", "Not Used", "Not Used")},
}


def coil_kind(label: str) -> str:
	text = label.casefold()
	return "magnet" if "magnet" in text else "motor" if "shaker" in text else "coil"


def bank_tick(game: str, coil: int) -> tuple[str, str]:
	bank = chart(game)["coil_banks"][str(coil // 8)]
	wire = next((tick["wire"] for tick in bank["ticks"] if tick["label"] == str(coil)), "")
	return bank["power"], wire


def coil_output(game: str, address: int, rom: dict[int, str]) -> dict[str, Any]:
	i, coil = ids(game), address - 1
	chart_text = clean(chart(game)["coils"].get(str(coil), ""))
	name, _, chart_colour = chart_text.partition(" - ") if game == "amh" else (chart_text, "", "")
	listed = SOLENOID_LISTS.get(game, {}).get(coil)
	rom_name = rom[address]
	refs = [i["wiring"], CORE, BOARD, i["rt-solenoid"], i["sim"]]
	if listed:
		refs.append(i["list"])
	unused_rom = rom_name == "UNUSED" or re.fullmatch(r"SOL\d+", rom_name)
	if name:
		availability = "optional" if "(option" in name.casefold() else "used"
		label = name.replace(" (option)", "").strip()
	elif unused_rom:
		availability, label = "unused", f"Unused Coil {coil}"
	else:
		availability, label = "unknown", rom_name.title()
	item = device(f"coil.{address:02d}-{slug(label)}", label, coil_kind(label), SOLENOID, address, availability, tuple(refs))
	power, wire = bank_tick(game, coil)
	wire = wire or chart_colour
	notes = (f"Factory coil {coil} on Sol Bank {coil // 8} (power {power}), MOSFET {coil} (IRL540 on the wire chart), "
	         f"published at {address} = coil + 1. The ROM's Solenoid test names it {rom_name} and pressing Enter on that item "
	         f"fired exactly this address.")
	if availability == "optional":
		notes += " The chart marks it an option: fitted only on machines that carry it."
	if availability == "unused":
		notes += " The wire chart prints no wire on this pin and the ROM's own coil list calls it unused."
	if availability == "unknown":
		notes += " The production wire chart prints nothing on this pin, so whether production machines fit a load is not settled."
	physical: dict[str, Any] = {"notes": notes}
	if listed and listed[2] and listed[2] != "Not Used":
		physical["part_number"] = listed[2]
		physical["notes"] += f" Ken Layton's solenoid list: {listed[0]}, {listed[1] or 'no wire colour'}, coil {listed[2]}."
	if availability != "unused":
		physical["quantity"] = 1
	item["physical"] = physical
	wiring: dict[str, Any] = {"board": "pinHeck", "driver_transistor": f"IRL540 MOSFET {coil}",
	                          "control_connection": f"Sol Bank {coil // 8} pin {coil}", "nominal_voltage_v": 50, "voltage_type": "dc"}
	if wire and wire != "key":
		wiring["control_wire"] = wire
	if game != "amh":
		wiring["power_connection"] = f"Sol Bank {coil // 8} pwr (fuse F{coil // 8 + 1} 3A Slow-BLO)"
	item["wiring"] = wiring
	if availability == "unused":
		item["spatial"] = na("unused", i["wiring"], CORE)
	elif "knocker" in label.casefold() or "shaker" in label.casefold():
		item["spatial"] = na("cabinet_or_service", i["wiring"])
	return item


def gi_output(game: str, address: int, rom_gi: dict[int, str]) -> dict[str, Any]:
	i = ids(game)
	pin = address - 25 if address <= 32 else address - 29
	header = "GI_0" if pin < 8 else "GI_1"
	ticks = chart(game)["gi_flashers"].get(header, [])
	text = clean(next((tick["wire"] for tick in ticks if tick["label"] == str(pin)), "")) if isinstance(ticks, list) else ""
	colour, _, name = text.partition(" - ")
	rom_name = rom_gi[address]
	notes = (f"GI output {pin}: {'the first' if pin < 8 else 'the second'} 74HC595 byte of the board's GI shift register "
	         f"(pinheck_brd_gi), published at {address}. The ROM's Lamp test lights only this address under {rom_name}.")
	refs = [i["wiring"], CORE, BOARD, i["rt-lamp"], i["rt-game"]]
	if name and colour != "key":
		label = name
		kind = "flasher" if "flasher" in name.casefold() else "gi"
		availability = "used"
		notes += (f" The wire chart prints {header} pin {pin}: '{text}'. The pin-to-address assignment (GI pin k on public "
		          f"{'25+k' if pin < 8 else '29+k'}) is observed: with a game started, every output whose chart pin names a GI "
		          "string stayed steadily lit and every output whose pin names a flasher did not, on each pinHeck game whose chart "
		          "labels both.")
		status = "observed"
	else:
		label = f"{'Backbox' if pin < 8 else 'Playfield'} GI Output {pin}"
		kind, availability, status = "gi", "unknown", "observed"
		notes += (f" The ROM's own name places it in the {'backbox' if pin < 8 else 'playfield'} group. The wire chart prints no "
		          f"wire on {header} pin {pin}{' (a key position)' if colour == 'key' else ''}, which does not prove that nothing "
		          "is connected; the ROM drives it like any other GI output.")
	item = device(f"gi.{address:02d}-{slug(label)}", label, kind, SOLENOID, address, availability, tuple(refs), status)
	item["physical"] = {"notes": notes}
	wiring: dict[str, Any] = {"board": "pinHeck", "control_connection": f"{header} pin {pin}"}
	if colour and colour != "key":
		wiring["control_wire"] = colour
	item["wiring"] = wiring
	return item


def virtual_output(address: int, label: str, notes: str) -> dict[str, Any]:
	item = device(f"solenoid.{address:02d}-{slug(label)}", label, "virtual", SOLENOID, address, "unused", (CORE, PROFILE))
	item["physical"] = {"notes": notes}
	item["spatial"] = na("unused", CORE, PROFILE)
	return item


def simulator_shooter(game: str) -> dict[str, Any]:
	i = ids(game)
	if not GAMES[game]["manual_plunger"]:
		item = virtual_output(49, "Simulator Shooter Output", "The simulator declaration disables the manual plunger, so sim_getSol "
		                      "never raises the shooter release and core.c publishes a constant 0 here; the ROM never drives it.")
		item["provenance"] = prov(CORE, i["sim"], PROFILE)
		item["spatial"] = na("unused", CORE, i["sim"])
		return item
	item = device("solenoid.49-simulator-shooter-release", "Simulator Shooter Release", "virtual", SOLENOID, 49, "used", (CORE, i["sim"], PROFILE))
	item["physical"] = {"notes": ("PinMAME's built-in playfield simulator: the game's simulator declaration enables the manual plunger, "
	                              "and core.c publishes sim_getSol(49), the shooter-release state the simulator raises when its "
	                              "shooter key is released. It carries state only while PinMAME's keyboard handling drives the "
	                              "simulator; there is no board output and the ROM never drives it.")}
	item["spatial"] = na("virtual", CORE, i["sim"])
	return item


def custom_output(game: str, address: int) -> dict[str, Any]:
	g, i = GAMES[game], ids(game)
	if 57 <= address <= 61:
		servo = address - 57
		name = g["servos"].get(address)
		if name:
			rom = g.get("servo_rom", {}).get(address)
			notes = (f"Servo {servo}: pinheck_brd_servo scales the pulse width between the game's servoMin and servoMax onto 0-255 "
			         "and holds the last level when pulses stop. The charts name it " + repr(name) + ".")
			if rom:
				notes += f" The ROM's Servo test moves only this address for {', '.join(rom)}."
			optional = g.get("optional_servos", {}).get(address)
			refs = (i["switch"], i["wiring"], CORE, i["sim"], *((i["rt-servo"],) if "rt-servo" in i else ()))
			item = device(f"servo.{address:02d}-{slug(name)}", name, "servo", SOLENOID, address, "optional" if optional else "used", refs)
			item["range"] = {"minimum": 0, "maximum": 255}
			item["physical"] = {"notes": notes + (f" {optional}" if optional else ""), "quantity": 1}
		elif address in g.get("unknown_servos", {}):
			label, why = g["unknown_servos"][address]
			item = device(f"servo.{address:02d}-servo-{servo}", label, "servo", SOLENOID, address, "unknown",
			              (i["switch"], i["wiring"], CORE, *(i[f"rt-{test}"] for test in RUNTIME["games"][game]["runs"])), "observed")
			item["range"] = {"minimum": 0, "maximum": 255}
			item["physical"] = {"notes": f"Servo {servo}. {why}"}
		else:
			item = device(f"servo.{address:02d}-unused-servo-{servo}", f"Unused Servo {servo}", "servo", SOLENOID, address, "unused",
			              (i["wiring"], CORE, *((i["rt-servo"],) if "rt-servo" in i else ())))
			driven = ("the ROM's Servo test never drives it" if "rt-servo" in i else
			          "the ROM holds it at 0 in every retained run (this firmware has no Servo test)")
			item["physical"] = {"notes": f"Servo header {servo} carries no name on the charts and {driven}, so PinMAME publishes a constant 0."}
			item["spatial"] = na("unused", i["wiring"], CORE)
		return item
	names = g.get("rgb", {})
	if address in names:
		item = device(f"rgb.{address:02d}-{slug(names[address])}", names[address], "rgb_lamp", SOLENOID, address, "used",
		              (i["wiring"], CORE, i["rt-rgb"]))
		source = "on-board WS2801 LED" if address <= 56 or game == "amh" else "first LED of the external WS2801 chain"
		item["physical"] = {"notes": (f"{source.capitalize()} channel, published as a 0-255 level. The ROM's RGB test: {g['rgb_rom']}."
		                              + (f" {g['rgb_notes'][address]}" if address in g.get("rgb_notes", {}) else ""))}
		return item
	if "rgb_unnamed" in g and address >= 62:
		channel = "red green blue".split()[address - 62]
		item = device(f"rgb.{address:02d}-external-led-0-{channel}", f"External RGB LED 0 {channel}", "rgb_lamp", SOLENOID, address,
		              "unknown", (i["wiring"], CORE, i["rt-rgb"]), "observed")
		item["physical"] = {"notes": "First LED of the external WS2801 chain. " + g["rgb_unnamed"]}
		return item
	# A dark channel is never declared unused from the RGB test alone: give the game a name or an rgb_unnamed reason.
	raise ValueError(f"{game}: RGB channel {address} has neither a name nor an rgb_unnamed reason")


def lamp_output(game: str, address: int, rom_lamps: dict[int, str]) -> dict[str, Any]:
	c, i = chart(game), ids(game)
	n = factory_number(address)
	column, row = divmod(n, 8)
	label = clean(c["lamp_matrix"]["cells"][str(n)])
	refs = (i["lamp"], CORE, i["rt-lamp"])
	notes = (f"Factory lamp {n}, column {column}, row {row}, published at {address}. The ROM's Lamp test lights only this address "
	         f"under {rom_lamps[address]}.")
	if label and label.upper() != "NOT USED":
		kind = "flasher" if "FLASHER" in label.upper() else "lamp"
		item = device(f"lamp.{address:02d}-{slug(label)}", label, kind, LAMP, address, "used", refs)
		item["physical"] = {"notes": notes, "quantity": 1}
	else:
		item = device(f"lamp.{address:02d}-unused-lamp-{n}", f"Unused Lamp {n}", "lamp", LAMP, address, "unused", refs)
		item["physical"] = {"notes": notes + (" The factory chart prints NOT USED." if label else " The factory chart leaves the cell blank.")}
		item["spatial"] = na("unused", i["lamp"], CORE)
	wiring = {"board": "pinHeck", "drive_connection": f"Light Column {column}", "return_connection": f"Light Row {row}"}
	if c["lamp_matrix"]["columns"].get(str(column)):
		wiring["drive_wire"] = c["lamp_matrix"]["columns"][str(column)]
	if c["lamp_matrix"]["rows"].get(str(row)):
		wiring["return_wire"] = c["lamp_matrix"]["rows"][str(row)]
	item["wiring"] = wiring
	return item


def outputs(game: str) -> list[dict[str, Any]]:
	i = ids(game)
	rom, gi, lamps = rom_coils(game), rom_gi(game), rom_lamps(game)
	records = [coil_output(game, address, rom) for address in range(1, 25)]
	records += [gi_output(game, address, gi) for address in range(25, 33)]
	records += [virtual_output(address, f"Dead Upper Flipper Slot {address}",
	                           "core_getAllPhysicSols fills 33-36 from upper-flipper solenoid bits that no pinHeck driver sets; always 0.")
	            for address in range(33, 37)]
	records += [gi_output(game, address, gi) for address in range(37, 45)]
	records += [virtual_output(address, f"Dead Lower Flipper Slot {address}",
	                           "Lower-flipper solenoid bits; the vblank calls core_updateSw(0), so none is fabricated; always 0.")
	            for address in range(45, 49)]
	records.append(simulator_shooter(game))
	records.append(virtual_output(50, "Reserved Simulator Output", "Reserved; nothing writes it."))
	records += [custom_output(game, address) for address in range(51, 65)]
	records += [lamp_output(game, address, lamps) for address in [public_number(n) for n in range(64)]]
	start = device("lamp.91-start-button", "Start Button", "lamp", LAMP, 91, "used", (i["wiring"], CORE, i["rt-lamp"]))
	start["physical"] = {"location": "cabinet front", "quantity": 1, "notes": (
		"The Start button's LED, a separate board output (PA3, pinheck_brd_start) published as internal lamp 64 = public 91; "
		"the cabinet header wires 'start light'.")}
	start["spatial"] = na("cabinet_or_service", i["wiring"], CORE)
	records.append(start)
	for address in range(92, 99):
		item = device(f"lamp.{address:02d}-unused-lamp-slot", f"Unused Lamp Slot {address}", "virtual", LAMP, address, "unused", (CORE, PROFILE))
		item["physical"] = {"notes": "coreGlobals.nLamps = 72 publishes 92-98 but no board output feeds them."}
		item["spatial"] = na("unused", CORE, PROFILE)
		records.append(item)
	return records


# ---------------------------------------------------------------------------------------------
# Mechanisms: (key, label, kind, actuator outputs, sensor inputs, behaviour)
# ---------------------------------------------------------------------------------------------
FLIPPER_TEXT = ("A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input {button} (host public "
                "{host}), the ROM fires the {high} winding to lift the bat and holds it on the {hold} winding, and the matrix "
                "end-of-stroke contact {eos} tells it the stroke is complete. PinMAME publishes no Fliptronic states for this "
                "platform: the coil addresses are the flipper.")
MECHANISMS: dict[str, list[tuple[str, str, str, list[int], list[int], str]]] = {
	"amh": [
		("trough", "Four-ball trough, drain kicker and ball loader", "kicker", [22, 21], [88, 84, 85, 86, 87],
		 "A drained ball lands on the drain switch 88 and the DRAIN KICK coil (22) kicks it into the four-ball trough, sensed by 84-87 "
		 "(Trough Ball 1-4). BALL LOAD (21) feeds one ball to the shooter lane (82). In the game-start run (all four trough contacts "
		 "closed, Start pressed) the ROM pulsed 21 about every 1.6 s for 20 s, because no ball ever reached 82 to close it."),
		("shooter-lane", "Shooter lane and autolauncher", "kicker", [23], [82],
		 "AUTOPLUNGER (23) kicks the ball resting on the shooter lane switch 82 into play; PinMAME's simulator also offers a manual "
		 "plunger here."),
		("right-flipper", "Right flipper", "other", [17, 18], [75, 112], FLIPPER_TEXT.format(button=3, host=112, high="RFLIP HIGH (17)", hold="RFLIP HOLD (18)", eos="75 (RIGHT EOS)")),
		("left-flipper", "Left flipper", "other", [19, 20], [74, 114], FLIPPER_TEXT.format(button=4, host=114, high="LFLIP HIGH (19)", hold="LFLIP HOLD (20)", eos="74 (LEFT EOS)")),
		("left-slingshot", "Left slingshot", "kicker", [9], [73], "Slingshot switch 73 closes and the ROM fires LSLING (9)."),
		("right-slingshot", "Right slingshot", "kicker", [10], [76], "Slingshot switch 76 closes and the ROM fires RSLING (10)."),
		("pop-bumper-0", "Pop bumper 0 (upper left)", "kicker", [14], [56], "Pop bumper 0: skirt switch 56, coil POP BUMP 0 (14), the wire chart's upper left pop."),
		("pop-bumper-1", "Pop bumper 1 (upper right)", "kicker", [15], [67], "Pop bumper 1: skirt switch 67, coil POP BUMP 1 (15), the wire chart's upper right pop."),
		("pop-bumper-2", "Pop bumper 2 (lower)", "kicker", [16], [66], "Pop bumper 2: skirt switch 66, coil POP BUMP 2 (16), the wire chart's lower pop."),
		("basement-scoop", "Basement scoop", "kicker", [11], [37, 54, 55],
		 "The basement: lanes 54 (Basement Upper) and 55 (Basement Lower) lead to the basement right scoop (37), which SCOOPKICK (11) "
		 "ejects; the IPDB features count two vertical up-kickers."),
		("spooky-door", "Spooky Door and the VUK behind it", "gate", [58, 12], [96, 38],
		 "The Spooky Door is servo 1 (58): the ROM's Servo test sets DOOR OPEN (level 7) and DOOR CLOSE (level 128). Behind it the VUK "
		 "(12) lifts a ball resting on 38 (VUK LEFT BEHIND DOOR); opto 96 (the Spooky Door opto on the aux board) sees a ball at the door."),
		("hellevator", "Hellevator", "motorized", [57], [64, 46],
		 "The Hellevator car is servo 0 (57): HELL UP (level 228) and HELL DOWN (level 14) in the Servo test. Switch 64 senses a ball "
		 "in the car and 46 is the elevator call button target; IPDB describes it carrying the ball to upper and lower levels."),
		("ghost-loop-magnet", "Ghost loop magnet", "other", [1], [95],
		 "LOOP MAGNET (1) on the ghost loop, with the Ghost Loop opto 95 (opto 1 on the aux board) seeing the ball pass."),
		("ghost", "Ghost figure", "toy", [59, 62, 63, 64], [],
		 "The ghost figure turns on servo 2 (59: GHOST LEFT 14, MIDDLE 128, RIGHT 242 in the Servo test) and glows from on-board "
		 "WS2801 LED 2. Red is 62; green and blue are 63 and 64 under the RGB test's default GHOST TYPE REV 1 and swap to 64 and 63 "
		 "under REV 2, an operator setting. IPDB calls it a colour-changing ghost."),
		("ghost-targets", "Three-target bank", "drop_target_bank", [60], [33, 34, 35],
		 "Ghost targets 1-3 (33-35) on a bank that servo 3 (60) raises and lowers: TARGET UP (level 7) and TARGET DOWN (level 228). "
		 "IPDB: the 3-target bank drops into the playfield."),
		("balcony-jump", "Balcony jump ramp", "other", [], [52, 51, 53],
		 "The balcony jump: 52 senses the approach, 51 a successful jump and 53 a ball that falls short onto the pop path."),
	],
	"dominos": [
		("trough", "Three-ball trough", "kicker", [18], [12, 13, 14],
		 "Three balls rest on 12-14 (Trough Ball 1-3); the Ball Trough coil (18) feeds one to the shooter lane."),
		("shooter-lane", "Shooter lane and autolauncher", "kicker", [17], [11],
		 "The Autolauncher (17) kicks the ball resting on the shooter lane switch 11 into play; PinMAME's simulator also offers a "
		 "manual plunger here."),
		("right-flipper", "Right flipper", "other", [21, 19], [15, 112], FLIPPER_TEXT.format(button=3, host=112, high="Right Flipper High (21)", hold="Right Flipper Low (19)", eos="15")),
		("left-flipper", "Left flipper", "other", [10, 12], [21, 114], FLIPPER_TEXT.format(button=4, host=114, high="Left Flipper High (10)", hold="Left Flipper Low (12)", eos="21")),
		("left-slingshot", "Left slingshot", "kicker", [11], [22], "Slingshot switch 22 closes and the ROM fires the Left Sling (11)."),
		("right-slingshot", "Right slingshot", "kicker", [20], [16], "Slingshot switch 16 closes and the ROM fires the Right Sling (20)."),
		("lower-pop", "Lower pop bumper", "kicker", [3], [44], "Skirt switch 44, coil 3."),
		("left-pop", "Left pop bumper", "kicker", [4], [45], "Skirt switch 45, coil 4."),
		("right-pop", "Right pop bumper", "kicker", [5], [43], "Skirt switch 43, coil 5."),
		("left-scoop", "Left scoop", "kicker", [9], [25], "The Left Scoop coil (9) ejects a ball held on 25."),
		("right-scoop", "Right scoop", "kicker", [13], [48], "The Right Scoop coil (13) ejects a ball held on 48."),
		("up-post", "Orbit up-post", "other", [7], [36, 46], "The Up Post (7) between the orbits (36 right, 46 left) returns an orbit shot instead of letting it loop."),
		("noid", "The Noid", "motorized", [57], [58, 37, 38],
		 "The Noid figure turns on servo 0 (57, the chart's Noid Orbit servo); 58 (Noid Home) closes when it is at home, and the Noid "
		 "orbits 37/38 run past it. PinMAME's simulator models it as a continuous-rotation servo."),
		("noid-bank", "Noid target bank", "drop_target_bank", [58], [26, 27, 28],
		 "Noid Bank Right/Middle/Left (26-28) on the target bank that servo 1 (58, Target Bank) lowers into the playfield."),
	],
	"rzspook": [
		("trough", "Seven-ball trough", "kicker", [18], [12, 13, 14, 15, 16, 17, 18],
		 "Seven balls rest on 12-18 (Trough 1-7); BALL LOAD (18) feeds one to the shooter lane. In the game-start run (all seven "
		 "contacts closed, Start pressed) the ROM pulsed 18 every 6 s for 20 s, because no ball ever reached the shooter switch."),
		("shooter-lane", "Shooter lane and autolauncher", "kicker", [17], [11],
		 "AUTOPLUNGER (17) kicks the ball resting on the shooter lane switch 11 into play; PinMAME's simulator also offers a manual plunger."),
		("right-flipper", "Right flipper", "other", [20, 19], [24, 112], FLIPPER_TEXT.format(button=3, host=112, high="RFLIP HIGH (20)", hold="RFLIP LOW (19)", eos="24")),
		("left-flipper", "Left flipper", "other", [14, 13], [25, 114], FLIPPER_TEXT.format(button=4, host=114, high="LFLIP HIGH (14)", hold="LFLIP LOW (13)", eos="25")),
		("upper-flipper", "Upper flipper", "other", [3, 8], [41],
		 "The upper flipper on UFLIP HIGH (3) and UFLIP LOW (8) with its end-of-stroke contact 41; the ROM fires it from the right button."),
		("left-lower-slingshot", "Left lower slingshot", "kicker", [12], [26], "Switch 26, coil 12 (LEFT SLING)."),
		("left-upper-slingshot", "Left upper slingshot", "kicker", [11], [57], "Switch 57, coil 11 (UL SLING)."),
		("right-lower-slingshot", "Right lower slingshot", "kicker", [21], [23], "Switch 23, coil 21 (RIGHT SLING)."),
		("right-upper-slingshot", "Right upper slingshot", "kicker", [22], [32], "Switch 32, coil 22 (UR SLING)."),
		("right-pop", "Right pop bumper", "kicker", [6], [36], "Skirt switch 36, coil 6."),
		("lower-left-pop", "Lower left pop bumper", "kicker", [9], [54], "Skirt switch 54, coil 9 (LLEFT POP)."),
		("upper-left-pop", "Upper left pop bumper", "kicker", [10], [55], "Skirt switch 55, coil 10 (ULEFT POP)."),
		("vuk", "Vertical up-kicker", "kicker", [4], [43], "The VUK (4) lifts a ball held on 43; 44 (Secret Passage) feeds it."),
		("drop-target-lock", "Drop target and rail lock", "drop_target_bank", [7, 5], [48, 35, 33, 34],
		 "A single drop target (48) guards the right inner orbit (35); the Drop Target coil (7) resets it. With it down, the orbit "
		 "leads to a rail lock: Right Rail Lower (33) and Upper (34) hold balls behind the BALL STOP post (5, the chart's stop post "
		 "on the right inner orbit), which drops to release one."),
		("upper-playfield-gate", "Spaulding gate and upper playfield", "gate", [57], [95, 96, 37, 38],
		 "Servo 0 (57, Spaulding) is the gate to the elevated mini-playfield: GATE OPEN and GATE CLOSE in the Servo test. Opto 95 sees "
		 "the ball at the gate, 37/38 are the upper playfield's switches and opto 96 sees it leave."),
		("robot", "Captain Spaulding robot", "toy", [58], [], "The animated robot is servo 1 (58): ROBOT START and ROBOT END in the Servo test."),
		("living-dead-girl", "Living Dead Girl", "toy", [62, 63, 64], [46, 47],
		 "The Living Dead Girl figure with targets 46 (right) and 47 (left), lit by the first LED of the external WS2801 chain: LDG RED "
		 "on 62, LDG GREEN on 64 and LDG BLUE on 63."),
	],
	"jetsons": [
		("trough", "Three-ball trough with optos", "kicker", [5], [92, 52, 53, 54, 93],
		 "Balls rest in the trough on the trough opto 92 (Opto6) and the Ball Trough 1-3 contacts 52-54, with the jam opto 93 (Opto5) "
		 "watching the exit. LOAD COIL (5) feeds one to the shooter lane; in the game-start run the ROM pulsed it about every 1.8 s "
		 "for 20 s, because no ball ever reached the shooter switch."),
		("shooter-lane", "Shooter lane and launcher", "kicker", [6], [51, 2],
		 "PLUNGER (6, the Ball Launch coil) fires the ball on the shooter lane switch 51; the cabinet Launch button is input 2."),
		("right-flipper", "Right flipper", "other", [4, 3], [55, 112], FLIPPER_TEXT.format(button=3, host=112, high="RFLIP HIGH (4)", hold="RFLIP LOW (3)", eos="55")),
		("left-flipper", "Left flipper", "other", [7, 8], [26, 114], FLIPPER_TEXT.format(button=4, host=114, high="LFLIP HIGH (7)", hold="LFLIP LOW (8)", eos="26")),
		("left-slingshot", "Left slingshot", "kicker", [10], [23], "Switch 23, coil 10."),
		("right-slingshot", "Right slingshot", "kicker", [11], [44], "Switch 44, coil 11."),
		("lower-pop", "Lower pop bumper", "kicker", [18], [34], "Skirt switch 34, coil 18 (BOTTOM POP)."),
		("left-pop", "Left pop bumper", "kicker", [19], [35], "Skirt switch 35, coil 19."),
		("right-pop", "Right pop bumper", "kicker", [21], [36], "Skirt switch 36, coil 21."),
		("scoop", "Scoop", "kicker", [9], [21, 96], "The Scoop coil (9) ejects a ball held on 21; the scoop opto 96 (Opto - 3) sees it enter."),
		("kickout-hole", "Kickout hole", "kicker", [20], [17], "SAUCER (20, the Saucer Kick Out coil) ejects a ball held on 17 (Kickout Hole)."),
		("up-post", "Orbit up-post", "other", [17], [11, 56, 16],
		 "BALL STOP (17, the chart's Up Post) between the orbits (11 right, 56 left) and the Elroy loop (16)."),
		("orbitty-topper", "Orbitty topper (Special Edition)", "toy", [57], [],
		 "Servo 0 (57) drives the backbox topper, which IPDB lists only on the Special Edition, so the output is optional; the ROM's "
		 "firmware has no Servo test, so its travel is not observed."),
	],
}


def mechanisms(game: str, ins: list[dict[str, Any]], outs: list[dict[str, Any]]) -> list[dict[str, Any]]:
	i = ids(game)
	sw = {d["binding"]["device"]: d["id"] for d in ins}
	sol = {d["binding"]["device"]: d["id"] for d in outs if d["binding"]["group"] == SOLENOID}
	result = []
	for key, label, kind, actuators, sensors, behavior in MECHANISMS[game]:
		refs = [i["switch"], i["wiring"], CORE, i["sim"], i["rt-solenoid"], i["rt-switch"], i["ipdb"]]
		if any(57 <= a <= 61 for a in actuators) and "rt-servo" in i:
			refs.append(i["rt-servo"])
		if any(a >= 62 for a in actuators):
			refs.append(i["rt-rgb"])
		if key == "trough":
			refs.append(i["rt-game"])
		result.append({"id": f"mechanism.{key}", "label": label, "kind": kind, "actuators": [sol[a] for a in actuators],
		               "sensors": [sw[s] for s in sensors], "behavior": behavior, "provenance": prov(*refs, status="observed")})
	return result


def displays(game: str) -> list[dict[str, Any]]:
	d, i = GAMES[game]["display"], ids(game)
	layout = ("CORE_DMD layout, 16 brightness levels (depth 4 at the LibPinMAME interface)" if d["kind"] == "dmd" else
	          "CORE_VIDEO layout, handed to LibPinMAME as 16-bit 5.6.5 frames (depth 16)")
	return [{"id": "display.main", "label": f"{d['label']}; {layout}", "kind": d["kind"], "controller_index": 0, "width": d["width"],
	         "height": d["height"], "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE),
	         "provenance": prov(CORE, i["sim"], i["rt-switch"])}]


# ---------------------------------------------------------------------------------------------
# Excerpts and sources
# ---------------------------------------------------------------------------------------------
def excerpt_dir(game: str) -> str:
	return f"evidence/excerpts/{GAMES[game]['machine']}"


def chart_excerpt(game: str, kind: str) -> str:
	"""The static chart transcription, committed beside the definition."""
	return (ROOT / excerpt_dir(game) / f"{kind}.md").read_bytes().decode()


def solenoid_list_excerpt(game: str) -> str:
	rows = "".join(f"| {coil} | {f} | {w or '(blank)'} | SOL{coil} | {p or '(blank)'} | {coil // 8} | F{coil // 8 + 1} 3A Slo |\n"
	               for coil, (f, w, p) in SOLENOID_LISTS[game].items())
	return (f"# Ken Layton's solenoid list ({GAMES[game]['solenoid_list']})\n\nTranscribed from the PDF's text layer and checked "
	        f"against its render by {CURATOR}. One page; every row as printed, including Not Used rows.\n\n"
	        "| SOL # | FUNCTION | WIRE COLOR | DRIVER | COIL # | BANK # | FUSE # |\n|---|---|---|---|---|---|---|\n" + rows +
	        "\nFooter as printed: Driver Transistors IRL540; " + ("Feb. 10, 2019" if game == "dominos" else "Feb. 11, 2019") + " Ken Layton.\n")


def ipdb_excerpt(game: str) -> str:
	g = GAMES[game]
	lines = "".join(f"- IPDB {number}: {title}; {detail}.\n" for number, title, detail in g["editions"])
	return (f"# IPDB identity: {g['name']}\n\nRead from the IPDB machine pages saved by {CURATOR}.\n\n{lines}\n"
	        f"MPU: PinHeck System. Model number {g['model']}. Every edition runs the same code update and shares the playfield; "
	        "IPDB lists the editions' differences as cosmetic or, for The Jetsons' Special Edition, a backbox topper.\n")


def rom_excerpt(game: str) -> str:
	rom, gi, lamps = rom_coils(game), rom_gi(game), rom_lamps(game)
	grid_rows = "".join(f"| {address} | {', '.join(drawn) or '(nothing)'} |\n" for address, drawn in sorted(grid(game).items(), key=lambda kv: int(kv[0])))
	coil_rows = "".join(f"| {address} | {name} |\n" for address, name in sorted(rom.items()))
	gi_rows = "".join(f"| {address} | {name} |\n" for address, name in sorted(gi.items()))
	lamp_rows = "".join(f"| {address} | {name} |\n" for address, name in sorted(lamps.items()))
	return (f"# ROM service tests: {GAMES[game]['name']} ({GAMES[game]['firmware']})\n\nDerived from tools/pinheck_runtime.json, "
	        f"which pins every retained run and frame by SHA-256; frame texts read by {CURATOR}.\n\n"
	        "## Switch Edge test: what the ROM drew for each closed public switch\n\n| Public | Drawn as |\n|---|---|\n" + grid_rows +
	        "\n## Solenoid test: item name and the one coil address Enter fired\n\n| Public | ROM name |\n|---|---|\n" + coil_rows +
	        "\n## Lamp test: GI items and the one output lit\n\n| Public | ROM name |\n|---|---|\n" + gi_rows +
	        "\n## Lamp test: single-lamp items and the one lamp lit\n\n| Public | ROM name |\n|---|---|\n" + lamp_rows)


def runtime_excerpt(game: str) -> str:
	rows = "".join(f"| {test} | {run['run_sha256']} | {run['scenario_sha256']} | {run['manifest_sha256']} |\n"
	               for test, run in runs(game).items())
	library = {run["library_sha256"] for run in runs(game).values()}
	seed = RUNTIME["games"][game]["baseline_state"]
	start = "an empty state directory" if seed is None else (
		"a copy of the retained post-update state, session-20261005/baseline-state (canonical manifest SHA-256 "
		f"{seed['manifest_sha256']}; " + "; ".join(f"{f['path']} {f['sha256']}" for f in seed["files"]) + ")")
	return (f"# Runtime provenance: {GAMES[game]['name']}\n\nLibPinMAME built from PinMAME {RUN_REVISION} (pinmame64.dll SHA-256 "
	        f"{', '.join(sorted(library))}), which named the set `{game}` (now `{current_driver(game)}`), ROM set {GAMES[game]['rom']}. Each run started from {start} "
	        "and is retained with its scenario, DMD frames, state and a canonical manifest under the working root's "
	        f"review-artifacts/{GAMES[game]['machine']}/session-20261005/runtime/.\n\n| Test | run.json SHA-256 | scenario SHA-256 | manifest SHA-256 |\n|---|---|---|---|\n" + rows)


def placements_excerpt() -> str:
	t = AMH_TABLE
	rows = "".join(f"| {e['group']} {e['address']} | {e['object']} ({e['object_kind']}, {e['read_from']}) | {e['x']}, {e['y']} | "
	               f"{', '.join(str(v) for v in normalized(e['x'], e['y']))} | {e['binding']} |\n" for e in AMH_PLACEMENTS["placements"])
	unplaced = "".join(f"- {group.split('.')[-1]} {address}: {reason}\n" for (group, address), reason in AMH_UNPLACED.items())
	return (f"# LW recreation placements: America's Most Haunted\n\nTable `{t['filename']}` (SHA-256 {t['sha256']}, {t['bytes']} bytes), "
	        f"version 2.0 by freneticamnesic, Shoopity and LoadedWeapon; extracted with vpxtool 0.33.3 (manifest SHA-256 {t['manifest_sha256']}, "
	        f"{t['file_count']} files, {t['total_bytes']} bytes); its script.vbs SHA-256 {t['script_sha256']}. Playfield bounds left=0 top=0 "
	        f"right={t['width']:g} bottom={t['height']:g}; normalized = (x/{t['width']:g}, y/{t['height']:g}). The table runs its own port of the "
	        "game code, not the ROM, so each object was chosen by what its script does, checked against the factory chart's label. "
	        f"The primitives' stated mesh centres come from `vpxtool export obj --units vpu` (OBJ SHA-256 {t['obj_sha256']}).\n\n"
	        "| Device | Table object | Raw VPX | Normalized | Script binding |\n|---|---|---|---|---|\n" + rows +
	        "\n## Used devices without a placement\n\n" + unplaced)


def photo_excerpt(game: str) -> str:
	r = PHOTO[game]
	photos = "".join(f"- {ph['id']} ({ph['role']}): {ph['title']}, {ph['url']}, original file `{ph['original_filename']}`, "
	                 f"{ph['size_px'][0]} x {ph['size_px'][1]} px, SHA-256 {ph['sha256']}. {ph['notes']}\n" for ph in r["photos"])
	rows = "".join(f"| {e['group']} {e['address']} | {e['x']}, {e['y']} | {e['frame_px'][0]}, {e['frame_px'][1]} | {e['level']} | "
	               f"{e['confidence']} | {e['feature']} |\n" for e in r["placements"])
	unplaced = "".join(f"- {e['group']} {e['address']}: {e['reason']}\n" for e in r["unplaced"])
	return (f"# Photo placements: {GAMES[game]['name']}\n\n## Photographs\n\n{photos}\n## Frame\n\n{r['method']} Normalization: "
	        f"{r['frame']['normalization']}. The measurement files (rectified frame, boundary readings, homographies, overlays) are "
	        f"retained under the working root's review-artifacts/{GAMES[game]['machine']}/{r['measurement_dir']}/ (manifest SHA-256 "
	        f"{r['measurement_manifest_sha256']}).\n\n## Placements\n\nOnly playfield-level parts read at medium or high confidence are "
	        "placed, and flipper pivots and sling centres, which stand about an inch above the playfield.\n\n"
	        "| Device | Normalized | Frame px | Level | Confidence | Feature |\n|---|---|---|---|---|---|\n" + rows +
	        "\n## Used devices without a placement\n\n" + unplaced)

def v22_excerpt() -> str:
	card, hexfile, text = AMH_V22["card"], AMH_V22["hex"], AMH_V22["version_txt"]
	if hashlib.sha256(text.encode()).hexdigest() != AMH_V22["version_sha256"]:
		raise ValueError("the V22 VERSION.TXT transcription no longer matches its recorded hash")
	rows = "".join(f"| {f['filename']} | {f['url']} | {f['bytes']} | {f['sha256']} | {f['last_modified']} | {f['acquired_at']} |\n" for f in (card, hexfile))
	return ("# America's Most Haunted V22 (amh_022)\n\nThe two downloads that make up PinMAME's amh_022 set, retained under the working "
	        "root's roms/spooky-pinball/ and assembled as the V23 set is: the card with the Intel HEX added to its root.\n\n"
	        "| File | URL | Bytes | SHA-256 | Server Last-Modified | Acquired |\n|---|---|---|---|---|---|\n" + rows +
	        f"\n## The card's VERSION.TXT ({len(text.encode())} bytes, SHA-256 {AMH_V22['version_sha256']}, CRLF line ends)\n\n```\n"
	        + text.replace("\r\n", "\n") + "\n```\n\n## Checked against PinMAME's set\n\n"
	        f"`src/wpc/sims/pinheck/amh.c` at {REVISION} declares `PINHECK_HEX_ROMSTART(amh_022, \"AMH_V022.hex\", 612459, CRC(B74F2A7B) "
	        "SHA1(4a36e71ba9fcfcd5779645e849babeed5a842c0b), \"PROP_022.BIN\", CRC(53A6B98B) SHA1(6427841d9f3ac6a744bf86856dfd3faf58e43828))`.\n\n"
	        "| Image | Bytes | CRC32 | SHA-1 |\n|---|---|---|---|\n"
	        f"| {hexfile['filename']} | {hexfile['bytes']} | {hexfile['crc']} | {hexfile['sha1']} |\n"
	        f"| {card['filename']}: {card['member']} | 32768 | {card['crc']} | {card['sha1']} |\n")


def transcriptions(game: str) -> dict[str, str]:
	texts = {"rom-service-tests.md": rom_excerpt(game), "runtime-provenance.md": runtime_excerpt(game), "ipdb.md": ipdb_excerpt(game)}
	if game == "amh":
		texts["table-placements.md"] = placements_excerpt()
		texts["rom-v22.md"] = v22_excerpt()
	if game in PHOTO:
		texts["photo-placements.md"] = photo_excerpt(game)
	if "solenoid_list" in GAMES[game]:
		texts["solenoid-list.md"] = solenoid_list_excerpt(game)
	return texts


def excerpt(game: str, name: str, locator: str, text: str, method: str, reviewed: bool, transcriber: str) -> dict[str, Any]:
	key = GAMES[game]["machine"].split(".")[1]
	return {"id": f"excerpt.{key}.{name.removesuffix('.md')}", "locator": locator, "path": f"{excerpt_dir(game)}/{name}",
	        "sha256": hashlib.sha256(text.encode()).hexdigest(), "method": method, "transcribed_by": transcriber, "reviewed": reviewed}


def acquisition(game: str, filename: str) -> dict[str, Any]:
	return load_json(Path(__file__).resolve().parent / "pinheck_acquisitions.json")[GAMES[game]["machine"]][filename]


def sources(game: str) -> list[dict[str, Any]]:
	g, i = GAMES[game], ids(game)
	texts = transcriptions(game)
	gen = {name: excerpt(game, name, locator, texts[name], "manual", True, CURATOR) for name, locator in (
		("rom-service-tests.md", "Switch Edge grid decode, Solenoid test names and fires, Lamp test GI and lamp items"),
		("runtime-provenance.md", "Library, ROM set, run, scenario and manifest hashes"),
		("ipdb.md", "IPDB machine pages of every edition"),
		("solenoid-list.md", "Whole list"))
		if name in texts}

	def doc(kind: str, filename: str, name: str, locator: str, reviewed: bool) -> dict[str, Any]:
		record = acquisition(game, filename)
		return {"id": i[kind], "kind": "manual", "uri": f"external:manuals/{record['relative_path']}", "sha256": record["sha256"],
		        "locator": locator, "attribution": record["attribution"], "license": "NOASSERTION", "rights": "NOASSERTION",
		        "original_filename": filename, "acquired_at": record["acquired_at"], "source_id": record["download_url"],
		        "excerpts": [excerpt(game, f"{name}.md", "Whole chart", chart_excerpt(game, name), "mixed", reviewed, CHART_READER)]}

	result = [
		{"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REVISION,
		 "locator": f"PinmameGetGames: {', '.join(g['drivers'])} (clone{'s' if len(g['drivers']) > 1 else ''} of the unreported pinHeck system set)", "attribution": "PinMAME contributors", "license": "BSD-3-Clause"},
		*[{"id": identifier, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/{path}", "revision": REVISION,
		   "sha256": digest, "locator": f"{path}: {locator}", "attribution": "PinMAME contributors", "license": "BSD-3-Clause"}
		  for identifier, (path, digest, locator) in CORE_FILES.items()],
		{"id": i["sim"], "kind": "pinmame_sim", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/{g['sim'][0]}", "revision": REVISION,
		 "sha256": g["sim"][1], "locator": f"{g['sim'][0]}: switch/solenoid defines, game data, mechanism handler and ROM_START",
		 "attribution": "PinMAME contributors", "license": "BSD-3-Clause"},
		{"id": PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/pinheck.json", "revision": "repository",
		 "locator": "pinHeck switch, solenoid and lamp address rules", "attribution": "PinMAME contributors", "license": "BSD-3-Clause"},
		doc("switch", g["documents"]["switch"], "switch-matrix", "Switch matrix, cabinet switch block, connector pin lists", True),
		doc("lamp", g["documents"]["lamp"], "lamp-matrix", "Light matrix and connector pin lists", True),
		doc("wiring", g["documents"]["wiring"], "wire-to-board", "Every connector, coil bank, GI header, opto and servo block", False),
		{"id": i["ipdb"], "kind": "human_review", "uri": f"https://www.ipdb.org/machine.cgi?id={g['ipdb']}", "locator": f"IPDB {', '.join(str(e[0]) for e in g['editions'])}",
		 "attribution": "The Internet Pinball Database", "license": "NOASSERTION", "acquired_at": acquisition(game, f"machine.cgi?id={g['ipdb']}")["acquired_at"],
		 "sha256": acquisition(game, f"machine.cgi?id={g['ipdb']}")["sha256"], "excerpts": [gen["ipdb.md"]]},
	]
	if "solenoid_list" in g:
		record = acquisition(game, g["solenoid_list"])
		result.append({"id": i["list"], "kind": "manual", "uri": f"external:manuals/{record['relative_path']}", "sha256": record["sha256"],
		               "locator": "Whole page", "attribution": "Ken Layton (IPDB)", "license": "NOASSERTION", "rights": "NOASSERTION",
		               "original_filename": g["solenoid_list"], "acquired_at": record["acquired_at"], "source_id": record["download_url"],
		               "excerpts": [gen["solenoid-list.md"]]})
	if game == "amh":
		v22 = excerpt(game, "rom-v22.md", "Downloads, VERSION.TXT and the CRC/SHA-1 check against amh.c", texts["rom-v22.md"], "manual", True, CURATOR)
		for part, what in (("card", "the V22 SD card image (DMD/ and SFX/ folders, VERSION.TXT); its DMD/PROP_022.bin is the Propeller program"),
		                   ("hex", "the V22 PIC32 program as Intel HEX")):
			f = AMH_V22[part]
			result.append({"id": f["id"], "kind": "rom_static_analysis", "uri": f["url"], "sha256": f["sha256"], "original_filename": f["filename"],
			               "acquired_at": f["acquired_at"],
			               "locator": (f"{f['filename']}, {f['bytes']} bytes: {what}. Retained under the working root's roms/spooky-pinball/; "
			                           "ROM bytes are never copied into this repository."),
			               "attribution": "Spooky Pinball (distributed by Ben Heckendorn, benheck.com)", "license": "NOASSERTION", "rights": "NOASSERTION",
			               "excerpts": [v22]})
		t = AMH_TABLE
		placements = excerpt(game, "table-placements.md", "Every placement and its script binding", texts["table-placements.md"], "manual", True, CURATOR)
		result += [
			{"id": AMH_TABLE_SOURCE, "kind": "vpx_table", "uri": f"external:pinmame-vpx-sources/{t['relative']}/{t['filename']}",
			 "original_filename": t["filename"], "sha256": t["sha256"], "revision": "2.0",
			 "locator": (f"America's Most Haunted v2.0 (released 2025-10-29), {t['bytes']} bytes, from the operator's table folder: the "
			             "freneticamnesic and Shoopity table updated by LoadedWeapon. It runs its own port of the game code, not the ROM; the "
			             "operator reviewed its layout as faithful to the machine. Playfield bounds left=0 top=0 right=952 bottom=2185; "
			             f"normalized coordinates are x/952 and y/2185. Extraction manifest SHA-256 {t['manifest_sha256']} "
			             f"(external:pinmame-vpx-sources/{t['relative']}/{t['filename'].removesuffix('.vpx')}.manifest.json). The geometry "
			             "source of every placement; the older table in the operator's archive is this one's ancestor and adds nothing independent."),
			 "attribution": "freneticamnesic, Shoopity and LoadedWeapon", "license": "NOASSERTION", "rights": "NOASSERTION",
			 "known_working": False, "excerpts": [placements]},
			{"id": AMH_SCRIPT_SOURCE, "kind": "vpx_script",
			 "uri": f"external:pinmame-vpx-sources/{t['relative']}/{t['filename'].removesuffix('.vpx')}/script.vbs",
			 "original_filename": "script.vbs", "sha256": t["script_sha256"],
			 "locator": (f"The LW table's embedded script, {t['script_bytes']} bytes: a port of the original game code with switch handlers "
			             "named after the factory switch numbers (TrSwN, WaSwN and the trough, drain, door and scoop kickers), "
			             "light(n) driving the n-th member of Light_Inserts, and the magnet, autoplunger and servo animations. It does not "
			             "run the ROM, so it identifies objects, never public addresses or causality."),
			 "attribution": "freneticamnesic, Shoopity and LoadedWeapon", "license": "NOASSERTION", "rights": "NOASSERTION",
			 "known_working": False, "excerpts": [placements]},
		]
	if game in PHOTO:
		photos = excerpt(game, "photo-placements.md", "Every measured placement and every unplaced device", texts["photo-placements.md"], "manual", True, CURATOR)
		result += [{"id": ph["id"], "kind": "human_review", "uri": ph["url"], "sha256": ph["sha256"], "original_filename": ph["original_filename"],
		            "acquired_at": "2026-10-05T00:00:00Z",
		            "locator": f"{ph['title']}, {ph['size_px'][0]} x {ph['size_px'][1]} px. {ph['notes']}",
		            "attribution": ph["attribution"], "license": "NOASSERTION", "rights": "NOASSERTION", "excerpts": [photos]}
		           for ph in PHOTO[game]["photos"]]
	for test, run in runs(game).items():
		result.append({"id": i[f"rt-{test}"], "kind": "runtime_scenario",
		               "uri": f"external:pinmame-review-artifacts/{g['machine']}/session-20261005/runtime/{game}-{test}/run.json",
		               "sha256": run["run_sha256"], "revision": RUN_REVISION,
		               "locator": f"tools/harness-scenarios/pinheck/{game}-{test}.json (scenario {run['scenario_sha256']}); directory manifest {run['manifest_sha256']}",
		               "attribution": "Generated locally from PinMAME and the user-authorized ROM set; ROM bytes remain external", "license": "NOASSERTION",
		               "excerpts": [gen["rom-service-tests.md"], gen["runtime-provenance.md"]]})
	return result


def normalized(x: float, y: float) -> tuple[float, float]:
	return round(x / AMH_TABLE["width"], 6), round(y / AMH_TABLE["height"], 6)


def place_amh(ins: list[dict[str, Any]], outs: list[dict[str, Any]]) -> None:
	"""Give each America's Most Haunted device its LW table placement (observed: one recreation, no factory drawing)."""
	groups = {"switch": SWITCH, "solenoid": SOLENOID, "lamp": LAMP}
	by_binding = {(d["binding"]["group"], d["binding"]["device"]): d for d in ins + outs}
	runtime = ids("amh")["rt-lanes"]
	for entry in AMH_PLACEMENTS["placements"]:
		item = by_binding[(groups[entry["group"]], entry["address"])]
		if item["availability"] not in ("used", "optional"):
			raise ValueError(f"{item['id']}: a placement for a device that is not used")
		role = "sensor" if entry["group"] == "switch" else "emitter" if item["kind"] in ("lamp", "flasher", "rgb_lamp", "gi") else "effect"
		x, y = normalized(entry["x"], entry["y"])
		refs = [AMH_TABLE_SOURCE, AMH_SCRIPT_SOURCE, *([runtime] if entry["address"] in (61, 62, 63) and entry["group"] == "switch" else [])]
		item["spatial"] = {"status": "observed", "placements": [
			{"id": f"{item['id']}.{role}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": prov(*refs, status="observed")}]}
		if entry["group"] == "solenoid" and entry["address"] in (62, 63, 64):
			item["physical"].update({"quantity": 1, "shared_emitter_group": "ghost-led", "co_located_addresses": [62, 63, 64],
			                         "shared_physical_quantity": 1,
			                         "emitter_channel": {62: "red", 63: "green", 64: "blue"}[entry["address"]]})
		if entry["group"] == "switch" and entry["address"] in (61, 62, 63):
			item["physical"]["notes"] += (" The LW recreation names its top-lane triggers out of order (TrSw40 is its B lane, TrSw41 its O lane), "
			                              "a defect of that table: its own code and lamps, and the ROM's lanes run, put this lane at "
			                              f"{ {61: 'the left', 62: 'the middle', 63: 'the right'}[entry['address']] }.")
	for (group, address), reason in AMH_UNPLACED.items():
		item = by_binding[(group, address)]
		if "spatial" in item:
			raise ValueError(f"{item['id']}: both placed and listed as unplaced")
	missing = [key for key, d in by_binding.items() if d["availability"] in ("used", "optional") and "spatial" not in d and key not in AMH_UNPLACED]
	if missing:
		raise ValueError(f"used America's Most Haunted devices with neither a placement nor a reason: {missing}")


def place_photo(game: str, ins: list[dict[str, Any]], outs: list[dict[str, Any]]) -> None:
	"""Placements measured on photographs (observed: photographs, no factory drawing or recreation table)."""
	groups = {"switch": SWITCH, "solenoid": SOLENOID, "lamp": LAMP}
	by_binding = {(d["binding"]["group"], d["binding"]["device"]): d for d in ins + outs}
	for entry in PHOTO[game]["placements"]:
		item = by_binding[(groups[entry["group"]], entry["address"])]
		if item["availability"] not in ("used", "optional"):
			raise ValueError(f"{item['id']}: a placement for a device that is not used")
		role = "sensor" if entry["group"] == "switch" else "emitter" if item["kind"] in ("lamp", "flasher", "rgb_lamp", "gi") else "effect"
		item["spatial"] = {"status": "observed", "placements": [
			{"id": f"{item['id']}.{role}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			 "provenance": prov(*entry["photos"], status="observed")}]}
	listed = {(groups[e["group"]], e["address"]) for e in PHOTO[game]["unplaced"]}
	missing = [key for key, d in by_binding.items() if d["availability"] in ("used", "optional") and "spatial" not in d and key not in listed]
	if missing:
		raise ValueError(f"used {GAMES[game]['name']} devices with neither a placement nor a reason: {missing}")

def build(game: str) -> dict[str, Any]:
	g, i = GAMES[game], ids(game)
	ins, outs = inputs(game), outputs(game)
	if game == "amh":
		place_amh(ins, outs)
	if game in PHOTO:
		place_photo(game, ins, outs)
	catalog = load_json(ROOT / "catalog/pinmame.json")
	records = {d["id"]: d for d in catalog["drivers"]}
	editions = "; ".join(f"IPDB {number} {title}" for number, title, _ in g["editions"])
	drivers = []
	for driver_id, earlier in g["drivers"].items():
		record = records[driver_id]
		notes = (f"Code update {g['firmware']} ({g['rom']}), loaded as {driver_id}.zip. Every edition ({editions}) runs this code on the same "
		         "board and playfield; PinMAME declares the set as a clone of the unreported pinHeck system set."
		         f" PinMAME revisions before 97aa922b named it `{game}`.") if earlier is None else f"{earlier} PinMAME loads it as {driver_id}.zip."
		drivers.append({"id": driver_id, "clone_of": record["clone_of"], "description": record["description"], "year": record["year"],
		                "manufacturer": record["manufacturer"], "flags": record["flags"], "physical_compatibility": "identical",
		                "variant_notes": notes})
	machine = {"id": g["machine"], "name": g["name"], "manufacturer": "Spooky Pinball", "year": g["year"], "kind": "physical_pinball",
	           "model_number": g["model"], "ipdb_id": g["ipdb"], "opdb_id": g["opdb"]}
	return {
		"format": "pinmame-machine-definition", "schema_version": 2, "machine": machine,
		"controller": {"platform": "pinmame.pinheck", "hardware_generation": PINHECK_GEN, "inversion_applied_by_emulator": True},
		"drivers": drivers, "inputs": ins, "outputs": outs, "displays": displays(game),
		"mechanisms": mechanisms(game, ins, outs), "relationships": [], "sources": sources(game),
		"knowledge": {"path": f"knowledge/{g['stem']}.md", "status": "partial"},
		"coverage": {"status": "partial", "missing": g.get("missing", ["mechanism_behavior", "output_semantics", "spatial_placement"]),
		             "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
		                            "physical_wiring": "observed", "mechanisms": "observed", "variant_coverage": "validated",
		                            "recreation_knowledge": "observed", "spatial_placement": "observed" if game == "amh" or game in PHOTO else "unknown",
		                            "runtime_observation": "observed",
		                            "causal_exercise": "observed"}},
		"conflicts": [],
	}


# ---------------------------------------------------------------------------------------------
# Knowledge note, spatial blocker report, CLI
# ---------------------------------------------------------------------------------------------
GAME_NOTES = {
	"amh": ("America's Most Haunted was Spooky Pinball's first production game, designed by Ben Heckendorn. It is the only pinHeck "
	        "game with a raw 128x32 DMD (scanned by a Propeller cog) and the only one whose PIC32 program ships as Intel HEX, so it "
	        "boots without the flash-and-restart cycle the other three need. Every playfield lamp and the cabinet are LED. Coils 7 and 8 "
	        "are named PROTO BG 1 by the ROM (a prototype backglass output) and carry nothing on the production wire chart; coils 2-6, 13 "
	        "and 24 are UNUSED in the ROM's own list. The lamp matrix carries three flashers (40 UPPER LEFT FLASHER, 41 HELL FLASHER, 42 "
	        "SCOOP FLASHER). The wire chart has no GI header; its GI legend names four playfield strings (Lower red, Mid yellow, Upper "
	        "purple, Scoop purple/black) on a green common, and with a game started the ROM held 26 and 37-39 steadily lit, but which "
	        "output feeds which string is not printed anywhere retained."),
	"dominos": ("Domino's was built under licence for Domino's Pizza; IPDB records about 60 Standard and 75 Limited Editions that differ "
	            "only in the backglass art and the LE plaque. Its knocker and shaker are options. The GI_1 header names four outputs: pin 12 "
	            "Right Flasher (41), 13 Left Flasher (42), 14 GI (43) and pin 15 Oven Flasher (44). Which of the two cabinet optos (95, 96) is "
	            "the scoop opto and which the Noid loop opto is not printed anywhere: the switch chart calls both 'Opto', the ROM's "
	            "Switch Edge test does not name them, and an exploratory game probe drew no ROM response from either."),
	"rzspook": ("Rob Zombie's Spookshow International has a seven-ball trough, three flippers, four slingshots, a drop target guarding "
	            "a rail lock and an elevated mini-playfield behind the Spaulding gate. The GI_1 header names bottom playfield GI 1 and 2 "
	            "(38, 39), red GI lamps (40), the purple and red flashers (41, 42) and white GI lamps (43); its pin 15 is a key position. "
	            "The Living Dead Girl figure is lit by the external WS2801 chain's first LED, whose green and blue arrive on PinMAME's "
	            "B (64) and G (63) slots, as the ROM's own RGB test shows."),
	"jetsons": ("The Jetsons was built by Spooky Pinball for The Pinball Company: 75 Regular and 25 Special Editions, the Special "
	            "Edition adding purple armour and the Orbitty backbox topper on servo 0. Its 128x64 colour display is the only one of "
	            "its size on pinHeck. The trough mixes optos (92 trough, 93 jam) with matrix contacts, and the cabinet carries a Launch "
	            "button (input 2). The GI_1 header names the ramp and scoop flashers (37, 38) and the left and right GI (39, 40)."),
}


MECHANISM_GAP = ("the mechanism inventory names each mechanism's coils, switches and service-test positions, but no retained source "
                 "gives its home and startup state, its timing, how the ROM resets it or how it fails, so mechanism behaviour stays "
                 "open until a manual, a known-working table or a gameplay harness run supplies it.")


AMH_SPATIAL_NOTE = ("the placements come from the LW recreation table (v2.0), whose layout the operator reviewed as faithful but "
                    "which no factory location drawing or second independent table checks, so they stay observed. Its script ports the "
                    "game code and names objects after the factory switch and lamp numbers; each object was taken from what its handler "
                    "does (`table-placements.md` cites the line), and where the table's names disagree the ROM decides: its top-lane "
                    "triggers are named out of order, and the lanes run proves the chart's 40 \"O\", 41 \"R\", 42 \"B\". The basement "
                    "subway switches (54, 55) are modelled off the playfield and the two side RGB strips (51-56) are not tied to an LED, "
                    "so those stay unplaced")


PHOTO_SPATIAL_NOTE = ("the placements are measured on photographs rectified at playfield level (`photo-placements.md` names the "
                      "photographs, the frame and its uncertainty, and every device left out). They stay observed: no factory "
                      "location drawing or recreation table checks them, a position can be off by a few percent, and raised parts, "
                      "parts hidden under the apron or ramps, GI and the RGB strings are not placed")


def unknown_summary(machine: dict[str, Any]) -> str:
	return ", ".join(f"{d['binding']['device']} ({d['label']})" for d in machine["outputs"] if d["availability"] == "unknown")


def knowledge(game: str, machine: dict[str, Any]) -> str:
	g = GAMES[game]
	used = lambda group: sum(1 for d in machine["inputs"] + machine["outputs"] if d["binding"]["group"] == group and d["availability"] == "used")
	text = f"""# {g['name']} (Spooky Pinball, {g['year']})

This definition covers the physical machine (IPDB {', '.join(str(e[0]) for e in g['editions'])}, model {g['model']}) and its {'two' if len(g['drivers']) > 1 else 'one'}
PinMAME {'drivers' if len(g['drivers']) > 1 else 'driver'}, {' and '.join(f'`{d}`' for d in g['drivers'])}, {'the V23 and V22 code updates' if len(g['drivers']) > 1 else 'the ' + g['firmware'] + ' code update'} on the Spooky Pinball pinHeck board (PIC32MX795 game CPU, Parallax Propeller
display/sound/media CPU). It is partial: every controller address is enumerated and checked against the ROM's own service
tests{', and all but the two cabinet optos are named,' if 'input_semantics' in machine['coverage']['missing'] else ' and named,'} but {'the placements come from one recreation table and are not yet checked against a factory drawing' if game == 'amh' else 'the placements are measured on photographs, not a factory drawing' if game in PHOTO else 'no placement exists'}, the mechanisms are inventoried
without their full behaviour, and some outputs keep an unknown fitment.

## Machine

{GAME_NOTES[game]}

Editions: {'; '.join(f'IPDB {n} {t} ({d})' for n, t, d in g['editions'])}.

## Running it

The romset is {g['rom']}, loaded as `{current_driver(game)}.zip`{'; `amh_022.zip` holds V22, built the same way from the V22 card and hex' if game == 'amh' else ''}. PinMAME before 97aa922b
named it `{game}.zip`, and the retained harness scenarios still name that set. pinHeck also needs `pinheck.zip` holding the Propeller's 32 KB mask ROM (`p8x32a.rom`, CRC32 f99b3070).
{'America' + chr(39) + 's Most Haunted needs no flashing: PinMAME programs the Intel HEX into the PIC32 at every start.' if game == 'amh' else 'On an empty NVRAM the ROM first programs its program flash and AV EEPROM from the romset (about eight emulated minutes), shows CODE UPDATE COMPLETE / PLEASE RESTART, and after the next start once more asks for a restart; from the third start it boots to attract mode. The harness runs started from a retained copy of that post-update NVRAM.'}

## Controller contract

The platform contract is `controllers/pinmame/pinheck.json`. In short: factory switch and lamp `n` (0-63) are public
`(n / 8 + 1) * 10 + n % 8 + 1` (11-88); cabinet inputs are 1-8 and 91-97; the host drives the flipper buttons at 112 (right) and 114
(left), which PinMAME copies to cabinet inputs 3 and 4; factory coil `n` is public `n + 1` (1-24); GI outputs 0-7 are 25-32 and 8-15
are 37-44; 51-56 are the on-board RGB LEDs, 57-61 the servos (0-255 position), 62-64 the external or third RGB LED; the Start lamp
is 91. On every switch public 1 is the closed contact; no switch is inverted. {used(SWITCH)} inputs, {used(SOLENOID)} solenoid-group
outputs and {used(LAMP)} lamps are used.

## What the ROM itself proves

Every pinHeck game has the same operator menu (Enter, 6, opens it; the right flipper button steps; Back, 5, leaves). Its Switch
Edge test draws each closure in an 8x8 grid laid out like the factory chart, so closing every public address proved the
switch formula for all 64 matrix positions and the cabinet mapping for 2-8 and 91-97. The Solenoid test names each of the 24
coils, and pressing Enter fired exactly coil `n + 1` every time. The Lamp test names the sixteen GI outputs (the playfield group
44 down to 37, the backbox group 32 down to 25) and then every matrix lamp by its factory number, lighting only that address. The
Servo and RGB tests name the servos and LED channels the game uses. A game-start run (trough full, Start pressed) shows the ROM
pulsing its trough feed coil repeatedly while no ball reaches the shooter lane.

## Mechanisms

"""
	for mechanism in machine["mechanisms"]:
		text += f"### {mechanism['label']}\n\n{mechanism['behavior']}\n\n"
	text += f"""## Evidence and remaining work

Factory chart transcriptions, the ROM service-test tables and the IPDB identity are under `{excerpt_dir(game)}/`; the runtime
summary is `tools/pinheck_runtime.json` (rebuilt by `tools/pinheck_runtime.py` from the retained runs), the scenarios are
`tools/harness-scenarios/pinheck/{game}-*.json`. Remaining: {AMH_SPATIAL_NOTE if game == 'amh' else PHOTO_SPATIAL_NOTE if game in PHOTO else 'no placement (no factory-layout table is retained)'};
{MECHANISM_GAP} The outputs whose fitment stays unknown: {unknown_summary(machine)}.
"""
	return text


def report(game: str, machine: dict[str, Any]) -> dict[str, Any]:
	used = [d["id"] for d in machine["inputs"] + machine["outputs"] if d.get("availability") in ("used", "optional") and "spatial" not in d]
	unknown = [d["id"] for d in machine["outputs"] if d.get("availability") == "unknown"]
	observed = [d["id"] for d in machine["inputs"] + machine["outputs"] if d.get("spatial", {}).get("status") == "observed"]
	if game == "amh":
		spatial = [
			{"dimension": "spatial_placement", "records": observed,
			 "reason": ("Placed from one recreation table, the LW v2.0 table, whose layout the operator reviewed as faithful; no factory "
			            "location drawing or second independent factory-layout table is retained to check them, so every placement stays observed."),
			 "resolution": "Spooky Pinball's playfield location drawing, a second independent recreation, or a measured playfield scan, overlaid as docs/SPATIAL.md describes."},
			{"dimension": "spatial_placement", "records": used,
			 "reason": " ".join(dict.fromkeys(AMH_UNPLACED.values())),
			 "resolution": "A photograph of the basement subway and of the cabinet RGB strip harness, or a harness run that tells RGB1 from RGB2 by side."}]
		decision = "partial; placements observed on the LW recreation table"
		t, groups = AMH_TABLE, {"switch": SWITCH, "solenoid": SOLENOID, "lamp": LAMP}
		by_binding = {(d["binding"]["group"], d["binding"]["device"]): d["id"] for d in machine["inputs"] + machine["outputs"]}
		classes: dict[str, list[str]] = {key: [] for key in AMH_PROJECTIONS}
		for entry in AMH_PLACEMENTS["placements"]:
			key = ("flipper_pivot" if entry["object_kind"] == "Flipper" else "servo_axis" if entry["object"] in ("PrDoor", "PrGhost")
			       else "servo_assembly" if entry["object_kind"] == "Primitive" else "flasher_bulb" if entry["object"].endswith("a")
			       else "shared_rgb" if entry["object"] == "GILight1" else "wall_centroid" if entry["object_kind"] == "Wall" else "object_centre")
			classes[key].append(by_binding[(groups[entry["group"]], entry["address"])])
		audit = {
			"evidence": {
				"table": {"uri": f"external:pinmame-vpx-sources/{t['relative']}/{t['filename']}", "sha256": t["sha256"], "bytes": t["bytes"]},
				"extraction_manifest": {"uri": f"external:pinmame-vpx-sources/{t['relative']}/{t['filename'].removesuffix('.vpx')}.manifest.json",
				                        "sha256": t["manifest_sha256"], "files": t["file_count"], "bytes": t["total_bytes"],
				                        "algorithm": "Canonical JSON of format, version and every extracted file as sorted relative POSIX path, size and SHA-256."},
				"script": {"path": "script.vbs", "sha256": t["script_sha256"], "bytes": t["script_bytes"]},
				"mesh_export": {"uri": f"external:pinmame-vpx-sources/{t['relative']}/{t['obj']}", "sha256": t["obj_sha256"], "bytes": t["obj_bytes"],
				                "tool": "vpxtool 0.33.3 export obj --units vpu"},
				"seed": "tools/amh_lw_placements.json", "excerpt": f"{excerpt_dir(game)}/table-placements.md"},
			"transformation": {"bounds": {"left": 0, "top": 0, "right": t["width"], "bottom": t["height"]},
			                   "formula": "x / 952, y / 2185, rounded to six decimals"},
			"projection_classes": {key: {"method": AMH_PROJECTIONS[key], "records": records} for key, records in classes.items()},
		}
	elif game in PHOTO:
		r = PHOTO[game]
		spatial = [
			{"dimension": "spatial_placement", "records": observed,
			 "reason": f"Measured on photographs rectified at playfield level. {r['method']} No factory location drawing or recreation table is retained to check them, so they stay observed.",
			 "resolution": "Spooky Pinball's playfield location drawing, a measured playfield scan, or a faithful recreation table."},
			{"dimension": "spatial_placement", "records": used,
			 "reason": "Each record's reason is listed in photo-placements.md: raised, hidden under the apron, ramps or upper playfield, not a point device, or read only at low confidence.",
			 "resolution": "Close-up photographs of those parts with the playfield glass off, or a playfield scan."}]
		decision = "partial; placements observed on rectified photographs"
		audit = {"evidence": {"seed": "tools/pinheck_photo_placements.json", "excerpt": f"{excerpt_dir(game)}/photo-placements.md",
		                      "measurement_dir": r["measurement_dir"], "measurement_manifest_sha256": r["measurement_manifest_sha256"],
		                      "photographs": {ph["id"]: ph["sha256"] for ph in r["photos"]}},
		         "transformation": {"frame": [r["frame"]["width"], r["frame"]["height"]], "formula": r["frame"]["normalization"]}}
	else:
		spatial = [{"dimension": "spatial_placement", "records": used,
		            "reason": "No retained factory-layout geometry: no VPX table that runs this ROM exists.",
		            "resolution": "A factory-layout table, the playfield drawing with switch and lamp locations, or a measured playfield scan."}]
		decision = "partial; no placement evidence is retained"
		audit = {}
	return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": GAMES[game]["machine"],
	        "decision": decision, **audit,
	        "coordinate_convention": "x=0 left, 1 right; y=0 rear, 1 front",
	        "unplaced_records": used,
	        "blockers": [
		        *spatial,
		        {"dimension": "output_semantics", "records": unknown,
		         "reason": ("The ROM drives every GI output, so the wire chart's blank GI header pins leave the fitment of those outputs open; "
		                    "an RGB or servo output listed here is one whose load no chart names while PinMAME can still publish state there."),
		         "resolution": "A photograph of the GI_0/GI_1, servo and RGB Com Out harnesses on a production machine, or an owner's check of which pins carry wires."},
		        {"dimension": "mechanism_behavior", "records": [m["id"] for m in machine["mechanisms"]],
		         "reason": "No retained manual or known-working table describes home and startup states, timing, resets or failure modes.",
		         "resolution": "The game's operations manual, a known-working table, or gameplay harness runs that exercise each mechanism."},
		        *([{"dimension": "input_semantics", "records": [d["id"] for d in machine["inputs"] if d["binding"]["device"] in (95, 96)],
		            "reason": "The charts name a scoop opto and a Noid loop opto but not which cabinet input each reaches.",
		            "resolution": "A gameplay harness run that lets a ball reach the scoop or the Noid loop, or an owner's check of the Opto3/Opto4 harness."}]
		          if "input_semantics" in machine["coverage"]["missing"] else [])],
	        "promotion": {"allowed": False, "missing": machine["coverage"]["missing"]}}


def artifacts(game: str) -> dict[Path, bytes]:
	machine = build(game)
	stem = GAMES[game]["stem"]
	result = {Path(f"machines/partial/{stem}.json"): canonical_bytes(machine),
	          Path(f"knowledge/{stem}.md"): knowledge(game, machine).encode(),
	          Path(f"reports/spatial/{stem}.json"): canonical_bytes(report(game, machine))}
	result.update({Path(f"{excerpt_dir(game)}/{name}"): text.encode() for name, text in transcriptions(game).items()})
	return result


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	parser.add_argument("--game", choices=sorted(GAMES), action="append")
	parser.add_argument("--repository-root", type=Path, default=ROOT)
	args = parser.parse_args()
	for game in args.game or sorted(GAMES):
		if (args.repository_root / f"machines/author-ready/{GAMES[game]['stem']}.json").exists():
			raise SystemExit("Refusing to overwrite an existing author-ready artifact")
		for path, payload in artifacts(game).items():
			target = args.repository_root / path
			if args.check:
				if not target.is_file() or target.read_bytes().replace(b"\r\n", b"\n") != payload:
					raise SystemExit(f"Curator drift: {path.as_posix()}")
			else:
				write_bytes(target, payload)
		print(f"{GAMES[game]['name']}: artifacts {'match' if args.check else 'written'}; partial blockers remain explicit.")


if __name__ == "__main__":
	main()
