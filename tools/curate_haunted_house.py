"""Deterministic Haunted House curation from reviewed, machine-specific facts.

The evidence seed pins source bytes and exact table objects; the definition seed is
the resulting canonical artifact. External inputs are read only and verified when
their roots are configured. No source manual, ROM or VPX bytes enter the repository.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.haunted-house.1982"
RELATIVE = "gottlieb/haunted-house-1982"
DEFINITION = f"machines/partial/{RELATIVE}.json"
SEED = f"tools/seeds/{RELATIVE}.json"
FACTS = f"tools/seeds/{RELATIVE}-evidence.json"
LAYOUT = f"tools/seeds/{RELATIVE}-layout.json"
KNOWLEDGE = f"knowledge/{RELATIVE}.md"
KNOWLEDGE_SEED = f"tools/seeds/{RELATIVE}.md"
REPORT = f"reports/spatial/{RELATIVE}.json"
REPORT_MD = f"reports/spatial/{RELATIVE}.md"
SWITCH, DIP = "pinmame.input.switch", "pinmame.input.dip"
LAMP, SOL, GI = "pinmame.output.lamp", "pinmame.output.solenoid", "pinmame.output.gi"
MANUAL, CORE, SCRIPT, TABLE, VPW, PHOTO, RUNTIME = (
	"manual.haunted-house", "pinmame.haunted-house.core", "vpx.haunted-house.script",
	"vpx.haunted-house.table", "vpx.haunted-house.vpw-script", "ipdb.haunted-house.photos", "runtime.haunted-house",
)
MISSING = ["output_semantics", "provenance", "spatial_placement"]

# Address | literal physical function | level | part | branch wire | bound collision objects.
# Shared numbers retain every contact; these are not copied from another System 80 game.
SWITCH_ROWS = """
0|#1 Drop Target|cellar|B-18094|700|sw00
1|Pop Bumper|cellar|B-19643|500|Bumper4
2|#1 Drop Target|attic|B-18094|100|sw02
3|#1 Target|attic|B-20867|122|sw03
4|Left Return Rollover|main|B-18892|333|sw04
5|#3 Target|main|B-21561|344|sw05
6|#1 Trough|main|B-21492|277|sw06
10|#2 Drop Target|cellar|B-18094|711|sw10
11|Kicking Target|cellar|B-18808|511|sw11
12|#2 Drop Target|attic|B-18094|111|sw12
13|#2 Target|attic|B-20867|133|sw13
14|#1 Kicking Target|main|B-18808|744|sw14
15|#4 Target|main|B-21561|766|sw15
16|#2 Trough|main|B-21492|288|sw16
20|#3 Drop Target|cellar|B-18095|722|sw20
21|Outside Rollover|cellar|B-18892|522|sw21
22|#3 Drop Target|attic|B-18095|122|sw22
23|#3 Target|attic|B-20867|166|sw23
24|#2 Kicking Target|main|B-21570|755|sw24
25|#5 Top Kicking Target|main|B-18808|777|sw25
26|Roll Down Target Trough|main|B-20878|322|sw26
30|#4 Drop Target|cellar|B-18093|733|sw30
31|Up Kicker|cellar|B-21415|533|sw31
32|#4 Drop Target|attic|B-18093|133|sw32
33|#4 Target|attic|B-20867|177|sw33
34|Left Outside Rollover|main|B-19754|011|sw34
35|Rollunder|main|B-21137|022|sw35
36|Trap Door Trough|main|B-21492|033|sw36
40|#5 Drop Target|cellar|B-18093|744|sw40
41|Hole|cellar|B-19857|544|sw41
42|10 Point (two contacts)|attic|B-18079|144|ScorringRubber1,ScorringRubber2
43|Pop Bumper|attic|B-19777|155|Bumper3
44|Pop Bumpers (two)|main|B-19643 / B-19777|044|Bumper1,Bumper2
45|Up Kicker|main|B-21415|055|sw45
46|Top Center Hole|main|B-19857|066|sw46
50|Right Target|cellar|B-21561|755|sw50
51|10 Point and Kicking Rubber (three contacts)|cellar|B-18078 / B-18079 / B-18808|566|ScorringRubber4,ScorringRubber5,LowerSlingShot
54|Right Outside Rollover|main|B-19754|100|sw54
55|Right Bottom Target|main|B-21561|111|sw55
60|Left Target|cellar|B-21561|766|sw60
64|Roundabout|main|B-21569|300|sw64
65|Right Side Kicker|main|B-18079|844|sw65
66|10 Point and Kicking Rubber (two contacts)|main|B-18079 / B-18808|355|sw66b,UpperSlingShot
67|Outhole|main|B-18892|155|Kicker1
"""

# Lamp name/printed connector/wire. Positions are selected separately from factory
# drawings; a script's glow/insert centre is never automatically a bulb placement.
LAMP_ROWS = """
3|Shoot Again|main|A3J3-C-bar|588
8|Extra Ball|main|A3J2-10|544
18|Double Bonus Upstairs Playfield|main|A3J3-16|166
19|Double Bonus Main Playfield|main|A3J3-15|177
20|Double Bonus Cellar|main|A3J3-21|300
21|Double Scoring|attic|A3J3-20|311
22|Double Scoring|main|A3J3-18|322
23|Double Scoring|cellar|A3J3-19|333
24|#1 Sequence|cellar|A3J3-9|344
25|#2 Sequence and Left Target|cellar|A3J3-10|355
26|#3 Sequence and Right Target|cellar|A3J3-12|366
27|Top Left Hole|main|A3J3-11|377
28|Top Center Hole|main|A3J3-Y|500
29|Top Right Hole|main|A3J3-X|511
30|#1 Kicking Target|main|A3J3-V|522
31|#2 Kicking Target|main|A3J3-W|533
32|#3 Target|main|A3J3-5|544
33|#4 Target|main|A3J3-6|555
34|#5 Top Kicking Target|main|A3J3-K|566
35|1X Bonus Multiplier|main|A3J3-7|577
36|2X Bonus Multiplier|main|A3J4-1|700
37|3X Bonus Multiplier|main|A3J4-2|711
38|4X Bonus Multiplier|main|A3J4-4|722
39|5X Bonus Multiplier|main|A3J4-3|733
40|#2 Target|attic|A3J3-4|744
41|#3 Target|attic|A3J3-3|755
42|#4 Target|attic|A3J3-T|766
44|Special|attic|A3J3-D|800
45|Special|cellar|A3J3-F|811
46|Left Outside Rollover|main|A3J3-P|822
47|Roundabout|main|A3J3-M|833
51|Roll Down Target|main|A3J3-N|877
"""


def rows(text: str) -> dict[int, list[str]]:
	return {int(parts[0]): parts[1:] for line in text.strip().splitlines() if (parts := line.split("|"))}


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def prov(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs or (MANUAL, CORE, SCRIPT, RUNTIME)))}


def na(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": prov(*(refs or (MANUAL, CORE)))}


def device(identifier: str, label: str, kind: str, group: str, address: int, *, availability: str = "used", refs: tuple[str, ...] = ()) -> dict[str, Any]:
	namespace = {SWITCH: "switch", DIP: "dip", LAMP: "lamp", SOL: "solenoid", GI: "gi"}[group]
	aliases = [{"namespace": f"pinmame.{namespace}", "value": str(address)}]
	if group == SWITCH and 0 <= address <= 77:
		aliases += [{"namespace": "vpe-legacy.switch", "value": v} for v in dict.fromkeys((str(address), f"{address:02}", f"{address:03}"))]
	if group == LAMP and address < 52 and address != 2:
		aliases.append({"namespace": "manual.address", "value": f"L{address}"})
	if group == LAMP and address == 3:
		aliases.append({"namespace": "manual.address", "value": "L2"})
	return {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases, "availability": availability, "provenance": prov(*refs)}


def table_location(identifier: str, role: str, names: list[str], facts: dict[str, Any]) -> dict[str, Any]:
	placements = []
	for index, name in enumerate(names, 1):
		point = facts["table_points"][name]
		placements.append({"id": f"{identifier}.placement-{index}", "role": role, "space": "playfield",
			"x": round(point["x"] / 1116, 6), "y": round(point["y"] / 2186, 6),
			"provenance": prov(*point.get("source_refs",[TABLE,SCRIPT,MANUAL]), status="observed")})
	return {"status": "observed", "placements": placements}


def input_devices(facts: dict[str, Any]) -> list[dict[str, Any]]:
	result = []
	physical = rows(SWITCH_ROWS)
	addresses = list(range(-8, 0)) + [10*s+r for s in range(8) for r in range(8)] + list(range(111, 119))
	cabinet = {7: "Self/Test Button", 17: "Left Coin Chute", 27: "Right Coin Chute", 37: "Center Coin Chute", 47: "Replay / Start Button", 57: "Plumb Bob and Ball Roll Tilt"}
	for address in addresses:
		if address in physical:
			label, level, part, wire, objects = physical[address]
			identifier = f"switch.{level}-{slug(label)}"
			d = device(identifier, f"{level.title()}: {label}", "switch", SWITCH, address)
			names = objects.split(",")
			d.update(normally_closed=False, physical={"location": f"{level} playfield", "part_number": part, "switch_type": "leaf", "quantity": len(names),
				"notes": "Printed 37 matrix contact is normally open; the unmasked System 80 RIOT read returns its closed contact at public 1. Printed 49/53 supplies the physical assignment. "
				+ ("Cellar devices are projected vertically onto global player view; their local playing direction faces the other way. " if level == "cellar" else "")
				+ ("Shared matrix address: retain every listed scoring contact. " if len(names) > 1 else "")},
				wiring={"board": "A1 control board", "drive_connection": f"A1J6-{address//10+1}", "drive_wire": f"4{address//10}{address//10}", "return_connection": f"A1J6-{address%10+10}", "return_wire": f"6{address%10}{address%10}", "control_wire": wire},
				spatial=table_location(identifier, "sensor", names, facts))
			if address in (0, 10, 20, 30, 40, 2, 12, 22, 32):
				d["physical"]["notes"] += "Hold closed while down; clear only when the reset physically raises this target."
			if address in (31, 41, 45, 46, 65, 67):
				d["physical"]["notes"] += "Occupancy follows the ball, not an arbitrary fixed pulse; the older script clears some occupied switches inside kick callbacks."
			if address == 67:
				d["initial_active"] = True
				d["physical"]["notes"] += " Fresh probe starts with the single ball at the outhole. Kicker1 is a table trough surrogate; its stored centre is not the physical outhole."
				# The table models a hidden transport trough at the right edge. It does
				# not provide the switch's actual physical centre at the drain.
				d.pop("spatial")
			elif address in (6, 16, 26, 36):
				d["physical"]["notes"] += "Trough switch projected onto the bound ball-path trigger below the relevant entrance; it is not a cabinet flipper input."
			if address == 36:
				d["physical"]["notes"] += " This normally open matrix switch is separate from the normally closed coil-side TRAP DOOR SW. contact."
		elif address in cabinet or address in (-1, -4, 112, 114):
			label = cabinet.get(address, {-1: "Slam / Anti-Cheat Switch", -4: "Sound Board Test Button", 112: "Right Red Flipper Button (synthetic column)", 114: "Left Red Flipper Button (synthetic column)"}.get(address, ""))
			d = device(f"switch.cabinet-{slug(label)}", label, "switch", SWITCH, address)
			d.update(normally_closed=address == -1, physical={"location": "cabinet or service", "switch_type": "tilt" if address in (-1,57) else "button", "notes": "Printed 42 bottom-board/cabinet drawing identifies the cabinet wiring. Direct host writes require keyboard handling off."}, spatial=na("cabinet_or_service"))
			if address == -1:
				d["initial_active"] = False
				d["physical"]["notes"] += " Normally closed physical slam contact; PinMAME public -1=1 means opened/slammed. Hold public 0 at rest; do not invert again."
			if address == 57:
				d["physical"].update(quantity=2, notes="Plumb-bob and ball-roll tilt are parallel contacts on return 7/strobe 5 (printed 42). Closing 57 drops game-on and raises the T relay in the retained gameplay run.")
			if address in (112,114):
				d["physical"]["notes"] = "The CPU never scans this column. PinMAME uses this cabinet-button bit to synthesize the corresponding pair 45/46 or 47/48 while game-on is true. Green auxiliary buttons are hardware-only and require consumer-side input; no independent CPU matrix address exists for them."
		else:
			d = device(f"virtual.switch-{address if address >= 0 else 'minus-'+str(-address)}", f"Unused switch position {address}", "virtual", SWITCH, address, availability="unused", refs=(CORE, MANUAL))
			d.update(physical={"notes": "No fitted matrix branch on the complete game switch diagram; strobe 7 is explicitly NOT USED. Dedicated video inputs belong only to the video driver, and unused flipper-column bits are never scanned by this game's CPU."}, spatial=na("unused"))
		result.append(d)
	labels = {13: "Extra Credits",14: "Coin Chute Control",15: "Maximum Credits (bit 1)",16: "Maximum Credits (bit 2)",17: "Balls per Game",18: "Match",19: "Replay Limit",20: "Novelty Mode",21: "Game Mode",22: "Playfield Special",23: "High Game to Date (bit 1)",24: "High Game to Date (bit 2)",25: "Must Remain ON",26: "Must Remain ON",27: "Coin Switch Tune",28: "Credits Displayed",29: "Tilt Penalty",30: "Attract Features",31: "Must Remain OFF",32: "Background Tone",33: "Sound SB1-1 Self-Test",34: "Sound SB1-2 Not Used",35: "Sound Attract Interval (bit 1)",36: "Sound Attract Interval (bit 2)",37: "Sound Background Enable",38: "Sound SB1-6 Not Used",39: "Sound SB1-7 Not Used",40: "Sound SB1-8 Not Used",41: "Unfitted Sound-Only Board S1",42: "Unfitted Sound-Only Board S2"}
	for address in range(1,43):
		label = labels.get(address, f"{('Left','Right','Center')[(address-1)//4]} Coin Pricing (bit {(address-1)%4+1})") if address <= 12 else labels[address]
		d = device(f"dip.option-{address}", label, "dip_switch", DIP, address, availability="optional" if address in (38,39) else "unused" if address in (34,40,41,42) else "used", refs=(MANUAL,CORE,"firmware.haunted-house.speech-manual","firmware.haunted-house.prom-manual"))
		d.update(physical={"location": "backbox CPU board" if address <=32 else "backbox sound board", "switch_type": "dip", "notes": "Physical settings and German chute exceptions are transcribed in manual-adjustments.md. Public ordinal is bank*8+bit+1. The sound-only bank 41–42 is absent on this sound/speech-board machine."}, spatial=na("dip_switch", MANUAL, CORE))
		if address in (31,32):
			d["physical"]["notes"]+=" On Flipprojets 3/4 and A/B variants, CPU 31 selects Extra Ball difficulty and 32 Special difficulty: OFF conservative/default, ON liberal. The authors report factory 32's printed background-tone option was never implemented."
		if address in (33,38,39):
			d["physical"]["notes"]+={33:" On the speech conversion SB1-1 selects the normal/multiball message set; select normal for this stock single-ball machine.",38:" Factory SB1-6 is unused; rev 4 speech hardware uses it for Speech ON/OFF.",39:" Factory SB1-7 is unused; rev 4 speech hardware uses it for extended Tilt/Slam voices."}[address]
			if address in (38,39):
				d["label"]=f"Sound SB1-{address-32}: unused stock / {'Speech Enable' if address==38 else 'Extended Tilt-Slam Voices'} on rev 4"
		result.append(d)
	return result


def output_devices(facts: dict[str, Any]) -> list[dict[str, Any]]:
	result = []
	solenoids = {
		1: ("top-hole", "Top Center Hole Kicker", "coil", "A-16570", "main", "A3J4-7", "266", "Q60", "sw46"),
		2: ("main-up-kicker", "Main Up Kicker", "coil", "A-5194", "main", "A3J4-13", "200", "Q57/Q58", "sw45"),
		5: ("attic-drop-reset", "Attic Four-Target Reset", "coil", "A-18102", "attic", "A3J4-6", "211", "Q61/Q62", "sw02,sw12,sw22,sw32"),
		6: ("cellar-hole", "Cellar Lower Hole Kicker", "coil", "A-16570", "cellar", "A3J4-12", "233", "Q63/Q64", "sw41"),
		8: ("knocker", "Knocker", "coil", None, "cabinet", "A3J5-8", "888", "Q53", ""),
		9: ("outhole", "Outhole Ball Release", "coil", "A-5195", "main", "A3J4-8", "244", "Q59", ""),
	}
	for address in list(range(1,12)) + [45,46,47,48]:
		if address in solenoids:
			name,label,kind,part,level,connector,wire,transistor,objects = solenoids[address]
			d = device(f"coil.{name}",label,kind,SOL,address)
			d.update(physical={"location": f"{level} playfield" if level != "cabinet" else "cabinet fuse/knocker panel", "notes": "Public address agrees with the game's own printed 14 Note A, printed 38 circuit and ROM Step 17."}, wiring={"board":"A3 driver board","drive_connection":connector,"drive_wire":wire,"driver_transistor":transistor,"nominal_voltage_v":24,"voltage_type":"dc"})
			if part is not None:
				d["physical"]["part_number"] = part
			if address == 5:
				d["physical"]["notes"] += " The reset effect is projected onto its own bank's target geometry, not an observed winding centre."
			elif address in (1, 2, 6):
				d["physical"]["notes"] += " The effect is projected onto its own sensor, not an observed winding centre."
			if address == 8:
				d["physical"]["notes"] = "Printed 14 Note A and ROM Step 17 identify the knocker as public solenoid 8. PDF 46/printed 42 cabinet wiring shows A3J5-8 and wire 888 on the 24 V DC circuit. The general coil chart lists A-5195 for knockers but warns that coil usage may vary by game; an exact winding part is not established by the game-specific coil table."
				d["spatial"] = na("cabinet_or_service")
			elif objects:
				# The reset-bank anchor is one target, not four coils; kickers use their own sensors.
				d["spatial"] = table_location(d["id"],"effect",[objects.split(",")[0]],facts)
			elif address == 9:
				d["physical"]["notes"] += " The script's Kicker1 is a hidden trough surrogate, so its coordinates are deliberately not used for the real outhole winding."
		elif address in (3,4,7):
			chute = {3:"left",4:"right",7:"center"}[address]
			d = device(f"coil.optional-{chute}-coin-counter",f"Optional {chute.title()} Mechanical Coin Counter","coil",SOL,address,availability="optional")
			d.update(physical={"location":"cabinet coin-counter option","notes":"Printed 14 Note B excludes optional counters from Step 17; the coin-input probe pulses this output. German Note D swaps center/right outputs 4/7. Optional fitment is not proof that every machine carries a counter."},spatial=na("cabinet_or_service"))
		else:
			name = "game-on" if address==10 else "tilt-relay-copy" if address==11 else f"flipper-{address}"
			d = device(f"virtual.{name}",f"Synthetic {name}","virtual",SOL,address,refs=(CORE,RUNTIME))
			d.update(physical={"notes":"No independent physical coil at this address. 10=(lamp 0 and not lamp 1); 11=lamp 1. 45/46 follow right 112 and 47/48 follow left 114 while 10 is enabled; paired states do not measure a winding or EOS timing. The eight hardware-wired flippers are enumerated as a mechanism."},spatial=na("virtual",CORE))
		result.append(d)
	lamps = rows(LAMP_ROWS)
	actuators = {
		0:("relay.game-over-q","Q Game-Over Relay","relay","A-16890","A3J3-A-bar","288","","Switches common playfield power and the match/ball-in-play lightbox branches; energized during play."),
		1:("relay.tilt-t","T Tilt Relay","relay","A-16890","A3J3-B-bar","277","","Interrupts the playfield AC GI and this game's controlled-lamp +6V DC; PinMAME does not emulate that DC cut. Tilt legend is on the other contact."),
		2:("coil.coin-lockout","Coin Lockout Coil","coil",None,"A3J5-2","877","","Lamp 2 is the coin-lockout circuit, not the attic first-target insert. The older script's local SetLamp100 drives a render light named L2; 100 is not a public lamp. PDF 29/printed 25 identifies Z1 Q3, A3 Q3 and A3J5-2; that driver region omits the winding and its wiring and supply. PDF 46/printed 42 traces wire 877 through A12J7/P7-8 to the front-door coil, whose other end is pin 7/wire 222; PDF 45/printed 41 identifies wire 222 as +24V DC. The winding part number remains unknown."),
		12:("relay.cellar-up-kicker-k","Cellar Up-Kicker K Relay","relay","A-20558","A3J3-25","100","sw31","The L12 load is K relay; its normally open contact switches +38V DC onto the separate A-21741 cellar up-kicker coil. Project the effect onto SW31; do not call A-21741 a direct lamp-driver winding."),
		13:("coil.cellar-drop-reset","Cellar Five-Target Reset","coil","A-17891","A3J3-24","111","sw00","Lamp-driver control through booster Q3 (2N5875 or 2N5879) to the five-target reset. Projection onto the bank, not its winding centre."),
		15:("coil.right-side-kicker","Right Side Kicker","coil","A-5195","A3J3-23","133","sw65","Lamp-driver control through booster Q1 to the right-side kicking device; it is not an automatic shooter-lane plunger."),
		16:("coil.trap-door","Trap Door Coil","coil","A-17875","A3J3-13","144","BM_pTrapDoor","Lamp-driver control through booster Q2 to the hinged trap door. The local coil-side TRAP DOOR SW. contact is not matrix 36. No position sensor is published. Its effect is projected onto the world-mesh bounds of its own closed plate/linkage in retained VPW2.1, corroborated by the manual assembly and physical photo; this is not a winding-centre measurement or the primitive's stored pivot."),
		17:("relay.playfield-u","U Playfield Selection Relay","relay","A-16890","A3J3-14","155","","Selects main versus cellar illumination and flipper circuits; lamp 17=1 is the cellar interval in the script and ROM probe. Attic green-button flippers are separate hardware circuits. The relay's location is not a bulb coordinate."),
	}
	for address in range(64):
		if address in lamps:
			label,level,connector,wire = lamps[address]
			d = device(f"lamp.{level}-{slug(label)}",f"{level.title()}: {label}","lamp",LAMP,address)
			d.update(physical={"location":f"{level} playfield","part_number":"#44 bulb","notes":"Printed 38/39 wiring and printed 49/53 assignment. A rendered insert or glow alone does not place the physical socket; unverified socket positions remain absent."},wiring={"board":"A3 driver board","drive_connection":connector,"drive_wire":wire,"driver_transistor":f"Q{address+1}","nominal_voltage_v":6,"voltage_type":"dc"})
			if address == 3:
				d["physical"].update(quantity=2,location="main playfield and backbox",notes="One Z1 Q4 latch and common A3 Q4 collector drive playboard L3 and lightbox L2 in parallel. Public 3 controls both; public 2 is the separate coin lockout. Only a proven playfield bulb would receive a placement.")
			if address == 51:
				d["physical"]["notes"] += " Physical Q-bar output Q52: this is the complement of public 47, not an independent 52nd latch."
			if address == 8:
				d["physical"]["notes"] += " The main parts drawing mislabels the between-flipper Shoot Again location L8; the physical photo and runtime table put Extra Ball by the right-bottom target. That misprinted label is not used as a socket coordinate."
		elif address in actuators:
			identifier,label,kind,part,connector,wire,anchor,note = actuators[address]
			d = device(identifier,label,kind,LAMP,address)
			d.update(physical={"location":"cabinet coin door" if address==2 else "under playfield", "notes":note},wiring={"board":"A3 driver board","drive_connection":connector,"driver_transistor":f"Q{address+1}"})
			if part is not None:
				d["physical"]["part_number"] = part
			if wire is not None:
				d["wiring"]["drive_wire"] = wire
			d["wiring"].update(nominal_voltage_v=24,voltage_type="dc")
			if anchor:
				d["spatial"] = table_location(identifier,"effect",[anchor],facts)
			elif address == 2:
				d["spatial"] = na("cabinet_or_service")
			elif address in (0,1,17):
				d["spatial"] = na("internal_nonvisual")
		elif address in (9,10,11):
			name = {9:"Sound16",10:"High Game to Date",11:"Game Over"}[address]
			d = device(f"control.{slug(name)}" if address==9 else f"lamp.lightbox-{slug(name)}",name,"control_signal" if address==9 else "lamp",LAMP,address)
			note = {9:"Printed 25/26 and 31/32: public 9 is Sound16, the fifth sound-command bit, not illumination.",10:"Printed 25/26 and 31/32: public 10 is Z3 Q3/high game to date (printed L11). ROM gameplay verifies lamp 10 during the high-score presentation.",11:"Printed 25/26 and 31/32: public 11 is Z3 Q4/game over (printed L10). ROM gameplay verifies lamp 11 flashing in attract."}[address]
			d.update(physical={"location":"backbox", "notes":note},spatial=na("internal_nonvisual" if address==9 else "cabinet_or_service"))
			if address in (10,11):
				d["aliases"] = [a for a in d["aliases"] if a["namespace"] != "manual.address"] + [{"namespace":"manual.address","value":f"L{21-address}"}]
		elif address == 4:
			d = device("control.unresolved-lamp-4","Unresolved lamp-driver output 4","control_signal",LAMP,4,availability="unknown",refs=(MANUAL,CORE,RUNTIME))
			d["provenance"]["status"] = "observed"
			d["physical"] = {"notes":"A3J2-2/Q5 has no load named on this game's complete wiring or assignment pages, but the ROM pulses public 4 at ball serve as well as in the all-driver chase. The retained evidence does not explain that normal-play state. Fitment remains unknown; a test pulse is not proof of a fitted lamp."}
			d["wiring"] = {"board":"A3 driver board","drive_connection":"A3J2-2","driver_transistor":"Q5 MPS-A13"}
		else:
			mirror = 48 <= address <= 50 or 52 <= address <= 60
			d = device(f"virtual.lamp-{address}",f"{'Inverted latch copy' if address<52 and mirror else 'Physical-output solenoid mirror' if mirror else 'Unfitted/reserved lamp position'} {address}","virtual",LAMP,address,availability="used" if 48<=address<=50 else "optional" if mirror else "unused",refs=(CORE,MANUAL))
			d.update(physical={"notes":f"Complement of public lamp {address-4}, with no fitted load on this game's diagram." if 48<=address<=50 else f"Mirrors solenoid {address-51} only in physical-output mode; binary lamp state remains 0. No second physical actuator." if mirror else "No fitted game load on the complete wiring and assignment pages. The all-driver service chase sweeps even unfitted latch positions; 61–63 are constant-zero reserved slots."},spatial=na("virtual" if mirror else "unused",CORE,MANUAL))
		result.append(d)
	d = device("virtual.gi-0","PinMAME Tilt-Relay GI Model","virtual",GI,0,availability="optional",refs=(CORE,MANUAL))
	d.update(physical={"notes":"One inverted #44 physical-GI model follows lamp 1 at 46e1a01a; binary GI is constant 0. It cannot represent the actual U-relay selection, the eight #313 cellar lights, all main/attic sockets or the controlled-lamp power cut. Recreate those from the physical relay circuits."},spatial=na("virtual",CORE))
	result.append(d)
	return result


def displays(facts: dict[str, Any]) -> list[dict[str, Any]]:
	result = []
	for index,start in enumerate((2,9,22,29)):
		result.append({"id":f"display.player-{index+1}-score","label":f"Player {index+1} Score","kind":"segment","controller_index":index,"segment_start":start,"width":6,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service"),"provenance":prov(CORE,MANUAL)})
	for index,(name,start) in enumerate(zip(("credits-tens","credits-units","ball-tens","ball-units"),(40,41,42,43)),4):
		result.append({"id":f"display.{name}","label":name.replace("-"," ").title(),"kind":"segment","controller_index":index,"segment_start":start,"width":1,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service"),"provenance":prov(CORE,MANUAL)})
	result.append({"id":"display.monster-bonus","label":"Monster Bonus (six-digit display below cellar window)","kind":"segment","controller_index":8,"segment_start":50,"width":6,"physical_location":"playfield","provenance":prov(CORE,MANUAL,PHOTO)})
	return result


def mechanisms(definition: dict[str, Any]) -> list[dict[str, Any]]:
	by_address = {d["binding"]["device"]:d["id"] for d in definition["inputs"] if d["binding"]["group"]==SWITCH}
	data = [
		("attic-drops","Attic Four-Target Bank","drop_target_bank",["coil.attic-drop-reset"],[2,12,22,32],"Four drop leaves stay closed when down. Solenoid 5 raises all four; clear leaves only as targets rise. The retained gameplay probe completed the bank and observed output 5. Reset retry timing and target animation are table-owned."),
		("cellar-drops","Cellar Five-Target Bank","drop_target_bank",["coil.cellar-drop-reset"],[0,10,20,30,40],"Five drop leaves stay closed when down. L13 drives booster Q3 and A-17891 to raise the bank. The probe's final down target produced L13; clear leaves on physical reset, not immediately on a hit."),
		("cellar-up-kicker","Cellar Return Up-Kicker and K Relay","kicker",["relay.cellar-up-kicker-k"],[31],"The cellar rear cup closes 31. L12 energizes A-20558 K relay, whose normally open contact applies 38V to separate A-21741 winding. The vertical plunger returns the ball to the main level and 31 opens after departure. The ROM probe raised L12 and cleared L17. Do not model the relay as the high-current winding itself."),
		("cellar-lower-hole","Cellar Lower Special Hole","kicker",["coil.cellar-hole"],[41],"The lower/end cellar hole holds the ball on 41 until public 6 ejects it back onto the cellar. It is a separate device and path from the rear up-kicker 31."),
		("main-up-kicker","Main-Level Vertical Up-Kicker","kicker",["coil.main-up-kicker"],[45],"The main-level cup closes 45; output 2 drives A-5194's vertical plunger and wireform. Clear 45 as the ball leaves. The script's kick angle and delay are implementation tuning, not physical measurements; a callback name alone does not establish a cross-level destination."),
		("top-center-hole","Main Top-Center Hole","kicker",["coil.top-hole"],[46],"Ball occupancy closes 46; public 1 drives the hole kicker. This central hole differs from the left/right cellar-entry troughs 6/16. It is not a startup ball inventory merely because a script initializes 46."),
		("right-side-kicker","Right-Side Help Kicker","kicker",["coil.right-side-kicker"],[65],"The right-side contact 65 requests L15. Q1 boosts the lamp-driver control into A-5195. Its spring/plunger throws the ball away from the right drain area. The impulse-plunger class used by the script is a simulation helper, not a motorized shooter plunger."),
		("trap-door","Hinged Trap Door and Trough","gate",["coil.trap-door"],[36],"L16/Q2/A-17875 moves the hinged circular door through a lever, link and plunger; springs provide return action. Opening admits the ball into the separate trough 36 leading to the cellar. The local coil-side cutoff/hold contact has no public matrix address; 36 is the normally open trough leaf. Door plane, spring return and link topology are physical; script animation speed is not."),
		("secret-passage","Passive Secret Passage Roll-Down Target","gate",[],[26],"The main target face rocks on its fulcrum/shaft under ball force, letting the ball enter the hidden passage to the cellar; its spring returns the face. SW26 belongs to the downstream trough, not a target-position sensor. There is no separately commanded reset coil for this passive target."),
		("outhole-and-shooter","Single-Ball Outhole and Manual Shooter","kicker",["coil.outhole"],[67],"The main drain closes 67 at the outhole. Solenoid 9 ejects the single ball into the manual shooter lane. No separate trough stack, automatic shooter coil or motor is documented. Table Kicker1..Kicker6 transport and configurable MaxBalls are recreation helpers; do not count them as fitted devices."),
		("local-reflex-devices","Hardware-Wired Bumpers and Kicking Devices","other",[],[1,11,14,24,25,42,43,44,51,66],"Four pop-bumper driver boards respond to local switches: two main bumpers share 44, attic 43, cellar 1. Main kicking devices correspond to 14/24/25 and the kicking-rubber portion of 66; cellar kicking target 11 and the kicking-rubber portion of 51 are locally powered. Other 42/51/66 leaves only score. These coils are not public CPU solenoids; use physical switch/relay causality rather than inventing controller outputs. Their supply-enabling relays belong to the illumination/selection mechanism, not duplicate actuator instances."),
		("eight-flippers","Eight Flippers and Four Cabinet Buttons","other",[],[112,114],"Four main flippers are operated by the red cabinet buttons; two attic and two cellar flippers use the green buttons, with relay contacts enabling the cellar during cellar play. PinMAME exposes only the synthetic red-button pair 112/114 and outputs 45–48. Green inputs and EOS contacts are hardware-only, with no separate CPU address. The older retained table optionally couples button pairs and routes callbacks differently; the later VPW script and physical apron instructions describe the separate green controls."),
		("illumination-selection","Three-Level Illumination and U Relay","other",["relay.game-over-q","relay.tilt-t","relay.playfield-u"],[],"Printed 39 switches main/cellar AC illumination through U and cuts playfield supply with T. Eight #313 lamps illuminate the cellar from the underside of the main playfield around the viewing glass; they are not a singleton floor light. Attic illumination, bumper lamps and lightbox name/scene lamps have separate physical branches. A11 is an autonomous 555/counter/decoder lightbox sequencer, not a bank of extra controller lamp callbacks. Physical socket positions/count reconciliation remain incomplete."),
	]
	result=[]
	photo_refs={"secret-passage":"ipdb.haunted-house.photo-59175","trap-door":"ipdb.haunted-house.photo-59181","illumination-selection":"ipdb.haunted-house.photo-59173"}
	for n,label,kind,actuators,sensors,behavior in data:
		refs=[MANUAL,CORE,SCRIPT,VPW,PHOTO,RUNTIME]
		if n in photo_refs:
			refs.append(photo_refs[n])
		result.append({"id":f"mechanism.{n}","label":label,"kind":kind,"actuators":actuators,"sensors":[by_address[a] for a in sensors],"behavior":behavior,"provenance":prov(*refs)})
	return result


def source_records(facts: dict[str, Any]) -> list[dict[str, Any]]:
	sources = copy.deepcopy(facts["sources"])
	for source in sources:
		for excerpt in source.get("excerpts",[]):
			path = ROOT / excerpt["path"]
			if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=excerpt["sha256"]:
				raise RuntimeError(f"missing or changed excerpt: {excerpt['path']}")
			if "image" in excerpt:
				image=ROOT/excerpt["image"]
				if not image.is_file() or hashlib.sha256(image.read_bytes()).hexdigest()!=excerpt["image_sha256"]:
					raise RuntimeError(f"missing or changed excerpt image: {excerpt['image']}")
	return sources


def drawing_projections(facts: dict[str, Any]) -> dict[str, Any]:
	from haunted_house_layout import plan
	path=ROOT/LAYOUT
	if hashlib.sha256(path.read_bytes()).hexdigest()!=facts["manual_layout_sha256"]:
		raise RuntimeError("manual layout read seed drift")
	return plan(facts,load_json(path))


def add_drawing_locations(definition: dict[str, Any], facts: dict[str, Any]) -> None:
	measurements=drawing_projections(facts)["measurements"]
	for collection in ("inputs","outputs","displays"):
		for d in definition[collection]:
			if collection=="displays":
				key=f"display:{d['controller_index']}"
			else:
				group=d["binding"]["group"]
				kind={SWITCH:"switch",LAMP:"lamp",SOL:"solenoid"}.get(group)
				key=f"{kind}:{d['binding']['device']}"
			if key not in measurements:
				continue
			m=measurements[key]
			d["spatial"]={"status":"observed","placements":[{"id":f"{d['id']}.drawing-projection","role":"display" if collection=="displays" else "sensor" if collection=="inputs" else "emitter" if d["kind"]=="lamp" else "effect","space":"playfield","x":m["xy"][0],"y":m["xy"][1],"provenance":prov(MANUAL,TABLE,CORE,status="observed")}]}
			if "physical" in d:
				d["physical"]["notes"]+=" Factory-drawing measurement: "+m["basis"]+(" Extrapolated outside the control convex hull; remains observed." if m["extrapolated"] else " Within the control convex hull; remains observed.")


def build() -> dict[str, Any]:
	facts = load_json(ROOT / FACTS)
	drivers = copy.deepcopy(facts["drivers"])
	for d in drivers:
		if d["id"] in ("hh","hh_1"):
			d.update(physical_compatibility="identical",variant_notes="Factory revision 2 from serial 5000 onward; revision 1 through 4999. Same System 80 address contract, six-digit displays and sound/speech board without fitted speech chip. Physical release year remains 1982.")
		elif d["id"]=="hh7":
			d.update(physical_compatibility="compatible",variant_notes="2008 seven-digit display conversion changes the system ROMs and four player display modules; the six-digit Monster Bonus and four status digits are unchanged.",display_overrides=[{"target":f"display.player-{i+1}-score","segment_start":start,"width":7,"provenance":prov(CORE,VPW)} for i,start in enumerate((2,9,22,29))])
		else:
			voice=d["id"].startswith("hh_4")
			note="Flipprojets replacement game PROM for the factory System 80 playfield. "
			note+=("Requires the documented SC-01/sound-memory board conversion; PinMAME sound ROMs remain NO_DUMP. " if voice else "Uses the standard non-speaking sound board. ")
			if d["id"].endswith("a"):
				note+="A adds the Extra Ball LED flash correction. "
			elif d["id"].endswith("b"):
				note+="B includes the LED correction and immediately returns an unlit-arrow secret-passage ball; no new physical tunnel gate is implied. "
			note+="CPU DIPs 31/32 now select award difficulty. "
			if voice:
				note+="Sound SB1-6 enables speech, SB1-7 Tilt/Slam voices, SB1-1 selects the normal/multiball message set; this machine uses normal. "
			note+="Full differences and author sources are in the knowledge note."
			d.update(physical_compatibility="compatible" if voice else "identical",variant_notes=note)
	definition = {"format":"pinmame-machine-definition","schema_version":2,
		"machine":{"id":MACHINE_ID,"name":"Haunted House","manufacturer":"Gottlieb","year":1982,"kind":"physical_pinball","model_number":"669","ipdb_id":1133,"opdb_id":"G5BP6-MJK4Z","playfield":{"width":1116,"height":2186,"units":"vpx","provenance":prov(TABLE,status="observed")}},
		"controller":{"platform":"pinmame.gts80","hardware_generation":"0x200000000","inversion_applied_by_emulator":True},
		"coverage":{"status":"partial","missing":MISSING,"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"observed","physical_wiring":"observed","mechanisms":"validated","variant_coverage":"validated","recreation_knowledge":"validated","spatial_placement":"observed"}},
		"drivers":drivers,"inputs":input_devices(facts),"outputs":output_devices(facts),"displays":displays(facts),"mechanisms":[],"relationships":[],"sources":source_records(facts),"knowledge":{"path":KNOWLEDGE,"status":"partial"},"conflicts":[]}
	add_drawing_locations(definition,facts)
	definition["mechanisms"] = mechanisms(definition)
	outputs = {(d["binding"]["group"],d["binding"]["device"]):d["id"] for d in definition["outputs"]}
	for a,b in ((44,48),(45,49),(46,50),(47,51)):
		definition["relationships"].append({"id":f"relationship.inverted-lamp-{a}-{b}","kind":"inverted","source":outputs[LAMP,a],"destination":outputs[LAMP,b],"provenance":prov(CORE,MANUAL)})
	for a,b in ((1,11),):
		definition["relationships"].append({"id":f"relationship.lamp-{a}-solenoid-{b}","kind":"direct","source":outputs[LAMP,a],"destination":outputs[SOL,b],"provenance":prov(CORE)})
	return definition


def spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	facts=load_json(ROOT/FACTS)
	devices=definition["inputs"]+definition["outputs"]+definition["displays"]
	return {"format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,"coverage_status":"partial","coordinate_convention":"global player view: x0 left/x1 right; y0 rear/y1 apron", "normalization":{"left":0,"top":0,"right":1116,"bottom":2186,"formula":"round(x/1116,6), round(y/2186,6)"},
		"sources":facts["external_inputs"],"table_points":facts["table_points"],"world_mesh_controls":facts["world_mesh_controls"],"factory_drawing_projections":drawing_projections(facts),"placement_count":sum(len(d.get("spatial",{}).get("placements",[])) for d in devices),
		"projections":{"cellar":"Vertical projection of the bound collision geometry into the main player's plan view; local cellar playing direction is reversed. No Z coordinate or second coordinate space is invented.","actuators":"K relay effect at its own cellar up-kicker; drop resets at their own bank's first target; main hole/kicker effects at their own sensor geometry. Trap-door effect at its closed plate/linkage world-mesh bounds centre; its mesh coordinate frame is checked against four independently placed bumper objects. These are mechanism anchors, not observed winding centres.","troughs":"Bound below-playfield ball-path triggers are observed projections, not an entrance-hole measurement."},
		"not_socket_evidence":["script-local SetLamp100 and 111","insert/glow/lightmap centres without physical socket corroboration","script Kicker1..6 hidden trough transport","TrapDoor kicker outside table bounds","single GILower render light","desktop-only lower insert offsets"],
		"unplaced":[d["id"] for d in devices if "spatial" not in d],
		"blockers":["Public lamp 4 pulses at ball serve but has no explained physical load.","Remaining controlled-lamp and GI sockets need defensible geometry. Existing locations are observed, including explicitly disclosed mechanism effects, drawing projections and extrapolations; render surrogates do not fill gaps."],
		"promotion_decision":"Remain partial. Source-verified controller structure and mechanisms do not validate every fitted socket, modification or unexplained output."}


def render_report(report: dict[str, Any]) -> str:
	lines=["# Haunted House spatial evidence", "", "Status: **partial**. Coordinates use global player view, x left to right and y rear to apron.", "", f"{report['placement_count']} observed placements. Exact object coordinates and source hashes are in the companion JSON.", "", "## Projection policy", ""]
	lines += [f"- **{k}:** {v}" for k,v in report["projections"].items()]
	lines += ["", "## Remaining blockers", ""]+[f"- {x}" for x in report["blockers"]]
	lines += ["", "## Devices without a defensible placement", ""]+[f"- `{x}`" for x in report["unplaced"]]
	return "\n".join(lines)+"\n"


def verify_external_inputs() -> None:
	facts=load_json(ROOT/FACTS)
	for run in facts["runtime_runs"]:
		path=ROOT/run["scenario_path"]
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=run["scenario_sha256"]:
			raise RuntimeError(f"missing or changed committed scenario: {path}")
	for item in facts["external_inputs"]:
		root=os.environ.get(item["environment_root"])
		if not root:
			continue
		path=Path(root)/item["relative_path"]
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item["sha256"]:
			raise RuntimeError(f"missing or changed external evidence: {path}")
		if item.get("manifest"):
			from build_external_evidence_manifest import check_manifest
			if check_manifest(path.parent,"hh") != item["sha256"]:
				raise RuntimeError(f"extraction manifest drift: {path.parent}")
	review_root=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if review_root:
		from haunted_house_runtime_evidence import derive
		derive(Path(review_root).parent/"runtime-evidence")


def artifacts() -> dict[str, bytes]:
	definition=build()
	report=spatial_report(definition)
	return {DEFINITION:canonical_bytes(definition),SEED:canonical_bytes(definition),REPORT:canonical_bytes(report),REPORT_MD:render_report(report).encode("utf-8"),KNOWLEDGE:(ROOT/KNOWLEDGE_SEED).read_bytes()}


def check(root: Path = ROOT) -> None:
	verify_external_inputs()
	if (root/f"machines/author-ready/{RELATIVE}.json").exists():
		raise RuntimeError("author-ready artifact exists; refusing implicit demotion or overwrite")
	for name,expected in artifacts().items():
		path=root/name
		if not path.is_file() or path.read_bytes()!=expected:
			raise RuntimeError(f"curation drift: {name}")


def generate(root: Path = ROOT) -> None:
	verify_external_inputs()
	if (root/f"machines/author-ready/{RELATIVE}.json").exists():
		raise RuntimeError("author-ready artifact exists; refusing overwrite")
	for name,data in artifacts().items():
		path=root/name
		path.parent.mkdir(parents=True,exist_ok=True)
		path.write_bytes(data)


def main() -> None:
	p=argparse.ArgumentParser(description=__doc__)
	p.add_argument("--check",action="store_true")
	p.add_argument("--regenerate",action="store_true")
	a=p.parse_args()
	if a.check==a.regenerate:
		p.error("choose exactly one of --check and --regenerate")
	(check if a.check else generate)()
	print("Haunted House curator check passed" if a.check else DEFINITION)


if __name__ == "__main__":
	main()
