"""Reproduce Dirty Harry from reviewed literals and the committed evidence seed.

The seed records source identities and individual coordinate reads, not consumer
object mappings. External inputs are optional for regeneration, but when supplied
their exact bytes and complete extraction are checked. Promotion is fail-closed.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_json, write_text
from build_external_evidence_manifest import build_manifest, check_manifest, canonical_bytes as manifest_bytes

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.dirty-harry.1995"
SEED = Path("tools/seeds/williams/dirty-harry-1995.json")
CIRCUIT_SEED = Path("tools/seeds/williams/dirty-harry-1995-circuits.json")
SPATIAL_SEED = Path("tools/seeds/williams/dirty-harry-1995-spatial.json")
NOTE_SEED = Path("tools/seeds/williams/dirty-harry-1995.md")
MACHINE = Path("machines/partial/williams/dirty-harry-1995.json")
NOTE = Path("knowledge/williams/dirty-harry-1995.md")
REPORT = Path("reports/spatial/williams/dirty-harry-1995.json")
REPORT_MD = Path("reports/spatial/williams/dirty-harry-1995.md")
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CORE = "pinmame.dh.core"
MANUAL = "manual.dirty-harry"
SCRIPT = "vpx-script.dirty-harry-2-0"
TABLE = "vpx-table.dirty-harry-2-0"
AMENDMENT = "amendment.dirty-harry.16-10007"
LIBRARY = "vpm-library.wpc"
RUNTIME = "runtime.dirty-harry"
SW = "pinmame.input.switch"
SOL = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
GI = "pinmame.output.gi"
MATRIX = tuple(c * 10 + r for c in range(1, 9) for r in range(1, 9))
MASK = (0, 0, 0, 0xff, 0x7f, 0, 0, 0, 0, 0, 0, 0)
SWITCHES = {
	11: "Gun Handle Trigger", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Shooter Lane",
	16: "Right Outlane", 17: "Right Inlane", 18: "Standup 8", 21: "Slam Tilt", 22: "Coin Door Closed",
	23: "Buy-in Button", 24: "Always Closed", 25: "Left Inlane", 26: "Left Outlane", 27: "Standup 1", 28: "Standup 2",
	31: "Trough Jam", 32: "Trough 1", 33: "Trough 2", 34: "Trough 3", 35: "Trough 4", 38: "Right Ramp Make",
	41: "Left Ramp Enter", 42: "Right Loop", 43: "Left Ramp Make", 44: "Gun Chamber", 45: "Gun Popper",
	46: "Warehouse Popper", 47: "Left Popper", 51: "Right Ramp Enter", 54: "Standup 6", 55: "Standup 7",
	56: "Standup 5", 57: "Standup 4", 58: "Standup 3", 61: "Left Sling", 62: "Right Sling", 63: "Left Jet",
	64: "Middle Jet", 65: "Right Jet", 66: "Left Rollover", 67: "Middle Rollover", 68: "Right Rollover",
	71: "Left Loop", 73: "Safehouse", 76: "Gun Position", 77: "Gun Lockup",
}
LAMPS = {
	11: "Left Rollover", 12: "Middle Rollover", 13: "Right Rollover", 14: "Magnum Jets", 15: "Magnum Bullets",
	16: "Light Extra Ball", 17: "Light Shootout", 18: "Playfield Promotion", 21: "Right Ramp Badge", 22: "Silver 6 Bullet",
	23: "Right Loop Generic", 24: "Magna Force", 25: "Right Ramp Generic", 26: "Right Ramp Jackpot", 27: "Right Loop HQ",
	28: "Warehouse Badge", 31: "Barroom Brawl", 32: "Car Chase", 33: "Warehouse Raid", 34: "Letter Bomb", 35: "Meet the Mob",
	36: "Stop Scorpio", 37: "Crime Wave", 38: "Bank Robber Hurry Up", 41: "Safehouse Badge", 42: "Left Ramp Badge",
	43: "Silver 3 Bullet", 44: "Super Jackpot", 45: "Left Ramp Generic", 46: "Ramp Start Multiball", 47: "Magazine Award",
	48: "Contraband", 51: "Safehouse", 52: "Silver 4 Bullet", 53: "Silver 5 Bullet", 54: "Left Loop HQ",
	55: "Warehouse Start Multiball", 56: "Feel Lucky", 57: "Right Shootout", 58: "Light Ransom", 61: "Left Loop Generic",
	62: "Ricochet", 63: "Extra Ball", 64: "HQ Badge", 65: "Ransom", 66: "Silver 1 Bullet", 67: "HQ", 68: "Silver 2 Bullet",
	77: "Shoot Again", 78: "Silver 7 Bullet", 81: "Silver 8 Bullet", 82: "Left Shootout", 83: "Light Magna Force",
	84: "Jets 84", 85: "Jets 85", 86: "Body Armor", 87: "Buy-in Button", 88: "Start Button",
}
# Printed coil numbers 29-36 are circuit identifiers. The lower windings publish
# at 45-48; 33-36 retain their numbers. Power callbacks 33/45/47 aggregate hold.
COILS = {
	1: ("Ball Release", "coil", "AE-26-1500"), 2: ("Autoplunger", "coil", "AE-23-800"),
	3: ("Gun Launch", "coil", "AE-23-800"), 4: ("Top Right Popper", "coil", "AE-23-800"),
	5: ("Gun Popper", "coil", "AE-24-900"), 7: ("Knocker", "coil", "AE-23-800"),
	8: ("Trap Door High", "coil", "A-14701"), 9: ("Left Sling", "coil", "AE-26-1200"),
	10: ("Right Sling", "coil", "AE-26-1200"), 11: ("Left Jet", "coil", "AE-26-1200"),
	12: ("Middle Jet", "coil", "AE-26-1200"), 13: ("Right Jet", "coil", "AE-26-1200"),
	14: ("Left Popper", "coil", "AE-26-1200"), 15: ("Ramp Diverter", "coil", "AE-26-1200"),
	16: ("Trap Door Hold", "coil", "A-14701"), 17: ("Headquarters", "flasher", "24-8802"),
	18: ("Safehouse", "flasher", "24-8802"), 19: ("Warehouse", "flasher", "24-8802"),
	20: ("Gun Motor", "motor", "A-19735"), 21: ("Gun Loaded", "flasher", "24-8802"),
	22: ("Right Ramp", "flasher", "24-8704"), 23: ("Right Back", "flasher", "24-8802"),
	24: ("Left Back", "flasher", "24-8802"), 26: ("Top Left Popper", "coil", "AE-26-1500"),
	27: ("Left Diverter", "coil", "AE-26-1200"), 28: ("Right Loop Gate", "coil", "A-14406"),
	33: ("Upper Right Flipper Power", "coil", "FL-11629"), 34: ("Upper Right Flipper Hold", "coil", "FL-11629"),
	35: ("Right Loop Magnet", "magnet", "20-9247"), 45: ("Lower Right Flipper Power", "coil", "FL-11629"),
	46: ("Lower Right Flipper Hold", "coil", "FL-11629"), 47: ("Lower Left Flipper Power", "coil", "FL-11629"),
	48: ("Lower Left Flipper Hold", "coil", "FL-11629"),
}

def prov(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}

def na(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}

def device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, *refs: str) -> dict[str, Any]:
	ns = {SW: "pinmame.switch", SOL: "pinmame.solenoid", LAMP: "pinmame.lamp", GI: "pinmame.gi", "pinmame.input.dip": "pinmame.dip"}[group]
	values = list(dict.fromkeys((str(address), f"{address:02}", f"{address:03}")))
	return {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "aliases": [{"namespace": ns, "value": value} for value in values], "provenance": prov(*refs)}

def locate(item: dict[str, Any], seed: dict[str, Any], category: str, role: str) -> None:
	entries = seed["placements"].get(category, {}).get(str(item["binding"]["device"]), [])
	if not entries:
		return
	placements = []
	for i, entry in enumerate(entries, 1):
		refs = entry["source_refs"]
		placements.append({"id": f'{item["id"]}.{role}-{i}', "role": role, "space": "playfield",
			"x": entry["x"], "y": entry["y"], "provenance": prov(*refs, status=entry["status"])})
	item["spatial"] = {"status": "validated" if all(e["status"] == "validated" for e in entries) else "observed", "placements": placements}
	item.setdefault("physical", {})["notes"] = item.get("physical", {}).get("notes", "") + " " + " ".join(dict.fromkeys(e["note"] for e in entries))
	item["physical"]["notes"] = item["physical"]["notes"].strip()

def inputs(seed: dict[str, Any]) -> list[dict[str, Any]]:
	result = []
	for address, label in enumerate(("Left Coin Chute", "Center Coin Chute", "Right Coin Chute", "4th Coin Chute", "Service Credit / Escape", "Volume Down / Down", "Volume Up / Up", "Begin Test / Enter"), 1):
		d = device(f"switch.dedicated-{address}", label, "switch", SW, address, "used", MANUAL, CORE, LIBRARY)
		d.update(normally_closed=False, physical={"location": "Coin door", "switch_type": "button" if address > 4 else "leaf"}, spatial=na("cabinet_or_service", MANUAL))
		d["wiring"] = seed["wiring"]["dedicated"][str(address)]
		result.append(d)
	for address in MATRIX:
		used = address in SWITCHES
		d = device(f"switch.matrix-{address}", SWITCHES.get(address, f"Not Used ({address})"), "constant" if address == 24 else "switch", SW, address, "used" if used else "unused", MANUAL, CORE, RUNTIME)
		d["wiring"] = seed["wiring"]["switch"][str(address)]
		if not used:
			d["spatial"] = na("unused", MANUAL, AMENDMENT) if address in (53, 88) else na("unused", MANUAL)
			if address in (53,88): d["provenance"] = prov(MANUAL,CORE,AMENDMENT,RUNTIME)
			d["physical"] = {"notes": "Production matrix and switch-location table explicitly print Not Used."}
			if address == 53:
				d["physical"]["notes"] += " Amendment 16-10007 removes sample Drop Target Reset. The location drawing retains a stale 53 callout; it is not evidence of production fitment. See the sample-hardware mechanism and knowledge note."
		elif address == 24:
			d.update(constant_active=True, initial_active=True, spatial=na("constant", MANUAL, SCRIPT), physical={"notes": "Printed Always Closed; table establishes public 1 before play. Virtual recreation ties this input active."})
		else:
			masked = bool(MASK[address // 10] & (1 << (address % 10 - 1)))
			d["normally_closed"] = masked
			d["physical"] = {"part_number": seed["parts"]["switch"][str(address)], "switch_type": "opto" if masked else "microswitch",
				"notes": "Matrix CPU read is raw swMatrix through wpc_pic_r. The game's invSw mask and the ROM-active public level 1 derive a normally closed matrix contact on masked positions, normally open on unmasked positions. Do not apply another inversion."}
			if address in (14,21): d["physical"]["switch_type"] = "tilt"
			if address in (13,23): d["physical"]["switch_type"] = "button"
			if address in (18,27,28,54,55,56,57,58,61,62,63,64,65): d["physical"]["switch_type"] = "leaf"
			if address in (32,33,34,35): d["initial_active"] = True
			if address == 22: d["initial_active"] = True
			if address in (11,13,14,21,22,23): d["spatial"] = na("cabinet_or_service", MANUAL)
			else: locate(d,seed,"switch","sensor")
			if str(address) in seed.get("switch_notes", {}): d["physical"]["notes"] += " " + seed["switch_notes"][str(address)]
		result.append(d)
	for address in (*range(91,99), *range(101,109)):
		d = device(f"switch.unfitted-column-{address}", f"Unfitted Matrix Column ({address})", "virtual", SW,address,"unused",CORE,MANUAL)
		d.update(spatial=na("no_physical_device",CORE,MANUAL),physical={"notes":"The Security PIC can select internal columns 9/10, but the game's CPU connector matrix and wiring enumerate only columns 1-8. No custom column is declared by dhGameData."})
		result.append(d)
	for address in range(111,119):
		f = seed["flipper_switches"][str(address)]
		d = device(f"switch.fliptronic-{address}", f["label"], "switch",SW,address,f["availability"],MANUAL,CORE,LIBRARY)
		d["aliases"].append({"namespace":"manual.address","value":f"F{address-110}"})
		d.update(physical=f["physical"], wiring=f["wiring"])
		if "normally_closed" in f: d["normally_closed"] = f["normally_closed"]
		if f["availability"] == "unused": d["spatial"] = na("unused",MANUAL,CORE)
		elif address % 2 == 0: d["spatial"] = na("cabinet_or_service",MANUAL)
		else: locate(d,seed,"switch","sensor")
		result.append(d)
	for address in range(1,9):
		d=device(f"dip.cpu-option-{address}", f"CPU Option / Country Bit {address}","dip_switch","pinmame.input.dip",address,"used",CORE,LIBRARY)
		d.update(spatial=na("dip_switch",CORE),physical={"notes":"WPC option byte, not a playfield contact. wpc.vbs exposes W20/W19 on masks 0x04/0x08 and the country encoding on 0xf0; remaining bits are retained without an invented option name."})
		result.append(d)
	return result

def outputs(seed: dict[str, Any]) -> list[dict[str, Any]]:
	result = []
	for address in range(1,51):
		if address in COILS:
			label,kind,part = COILS[address]
			d=device(f"device.solenoid-{address}",label,kind,SOL,address,"used",MANUAL,CORE,SCRIPT)
			d["physical"] = {"part_number":part,"notes":seed["coil_notes"].get(str(address),"Printed physical circuit; public address derived from the WPC driver and retained script.")}
			if str(address) in seed["wiring"]["coil"]: d["wiring"]=seed["wiring"]["coil"][str(address)]
			if address==7: d["spatial"]=na("cabinet_or_service",MANUAL)
			else: locate(d,seed,"solenoid","emitter" if kind=="flasher" else "effect")
			if address in (17,18,19,21,22,23,24): d["physical"]["quantity"]={17:2,18:1,19:1,21:1,22:1,23:2,24:2}[address]
			if address in (45,46,47,48): d["aliases"].append({"namespace":"manual.address","value":str(address-16)})
		elif str(address) in seed.get("virtual_outputs",{}):
			v=seed["virtual_outputs"][str(address)]
			d=device(f"device.solenoid-{address}",v["label"],"virtual",SOL,address,v["availability"],CORE)
			d.update(spatial=na("virtual",CORE),physical={"notes":v["notes"]})
			if address in (29,30,31): d["roles"] = ["internal.wpc-state"]
			if address == 32: d["roles"] = ["internal.unused.wpc-output"]
		else:
			availability = seed.get("output_disposition",{}).get(str(address),"unused")
			d=device(f"device.solenoid-{address}",f"Unfitted / Reserved Output {address}","virtual",SOL,address,availability,MANUAL,CORE)
			if address in (6,25,36):
				d["label"] = {6:"Removed Sample Drop Target Down",25:"Removed Sample Drop Reset",36:"Removed Sample Left Loop Gate"}[address]
				d["provenance"] = prov(MANUAL,CORE,AMENDMENT,"runtime.dirty-harry-coils")
			d.update(spatial=na("unused" if availability=="unused" else "no_physical_device",MANUAL,CORE),physical={"notes":seed["coil_notes"].get(str(address),"No physical circuit: WPC Security core_getSol returns zero for 37-44; 49-50 belong only to the built-in simulator; no custom-output hook is declared.")})
		result.append(d)
		if address in (33,34,35,36): d["aliases"].append({"namespace":"manual.address","value":str(address)})
	for address in MATRIX:
		used=address in LAMPS
		d=device(f"lamp.matrix-{address}",LAMPS.get(address,f"Not Used ({address})"),"lamp",LAMP,address,"used" if used else "unused",MANUAL,CORE)
		d["wiring"]=seed["wiring"]["lamp"][str(address)]
		if not used: d["spatial"]=na("unused",MANUAL)
		else:
			d["physical"]=copy.deepcopy(seed["parts"]["lamp"][str(address)])
			if address in (87,88): d["spatial"]=na("cabinet_or_service",MANUAL)
			else: locate(d,seed,"lamp","emitter")
		result.append(d)
	for address in range(5):
		g=seed["gi"][str(address)]
		d=device(f"gi.string-{address+1}",g["label"],"gi",GI,address,"used",MANUAL,CORE)
		d.update(wiring=g["wiring"], physical=g["physical"])
		d["aliases"].append({"namespace":"manual.address","value":f"{address+1:02}"})
		if g["cabinet"]: d["spatial"]=na("cabinet_or_service",MANUAL)
		else: locate(d,seed,"gi","emitter")
		result.append(d)
	return result

def load_seed(root: Path = ROOT) -> dict[str,Any]:
	seed=load_json(root/SEED)
	for path in (CIRCUIT_SEED,SPATIAL_SEED):
		part=load_json(root/path)
		if seed.keys() & part.keys(): raise ValueError(f"Ambiguous Dirty Harry seed writers: {path}")
		seed.update(part)
	return seed

def build(root: Path = ROOT) -> dict[str, Any]:
	seed=load_seed(root)
	for relative,digest in seed.get("committed_artifacts",{}).items():
		path=root/relative
		if not path.is_file() or file_sha256(path)!=digest:
			raise ValueError(f"Dirty Harry committed evidence drift: {relative}")
	d=copy.deepcopy(seed["definition"])
	d["inputs"]=inputs(seed)
	d["outputs"]=outputs(seed)
	# Source/excerpt hashes are pinned literals in the seed; do not repin from disk.
	for source in d["sources"]:
		for excerpt in source.get("excerpts",[]):
			for path_key,hash_key in (("path","sha256"),("image","image_sha256")):
				if path_key in excerpt and file_sha256(root/excerpt[path_key]) != excerpt[hash_key]:
					raise ValueError(f"Dirty Harry excerpt drift: {excerpt[path_key]}")
	ids=[x["id"] for coll in ("inputs","outputs","displays","mechanisms") for x in d[coll]]
	if len(ids)!=len(set(ids)): raise ValueError("Dirty Harry duplicate device/mechanism ID")
	if bool(unresolved_conflicts(d)) != ("unresolved_conflicts" in d["coverage"]["missing"]):
		raise ValueError("Dirty Harry conflict coverage mismatch")
	return d

def report(definition: dict[str,Any], root: Path = ROOT) -> dict[str,Any]:
	seed=load_seed(root)
	devices=definition["inputs"]+definition["outputs"]+definition["displays"]
	states={state: sorted(d["id"] for d in devices if d.get("spatial",{}).get("status")==state) for state in ("validated","observed","candidate","not_applicable")}
	missing=sorted(d["id"] for d in devices if d.get("availability","used") in ("used","optional") and "spatial" not in d)
	controls=copy.deepcopy(seed["drawing_controls"])
	for drawing in controls.values():
		left,top,right,bottom=drawing["frame"]
		for control in drawing["controls"]:
			x,y=control["pixel"]
			projected=((x-left)/(right-left),(y-top)/(bottom-top))
			raw_x,raw_y=control["table_raw"]
			exact=(raw_x/964,raw_y/2162)
			control["normalized_drawing"]=[round(v,6) for v in projected]
			control["normalized_table"]=[round(v,6) for v in exact]
			control["offset"]=round(sum((a-b)**2 for a,b in zip(projected,exact))**.5,6)
	return {"format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,
		"coordinate_convention":{"x":"left=0 right=1","y":"rear=0 apron=1","bounds":seed["bounds"],"precision":"at most six decimals"},
		"source_identities":seed["evidence"],"placement_status":states,"without_placements":missing,
		"placements":seed["placements"],"drawing_frame_checks":controls,"unresolved":seed["spatial_gaps"],
		"drawing_extrapolation":"Only three upper-playfield jet controls reconcile the lamp frame. Reads outside their control extent are extrapolated and remain observed. This is not a callout fit or a validation; no control was generated from table coordinates.",
		"promotion_decision":"partial; authoring-critical dimensions in coverage.missing remain. No helper or glow is promoted to a physical socket."}

def render_report(value: dict[str,Any]) -> str:
	lines=["# Dirty Harry (Williams, 1995): spatial evidence", "", "Coverage: **partial**. Coordinates use x left=0/right=1 and y rear=0/apron=1.","", "## Status", ""]
	lines += [f"- {key}: {len(items)} devices" for key,items in value["placement_status"].items()]
	lines += [f"- Used devices without placement: {', '.join(value['without_placements']) or 'none'}", "", "## Remaining evidence gaps", ""]
	lines += [f"- {gap}" for gap in value["unresolved"]]
	lines += ["", "The JSON companion lists every coordinate, raw object or drawing read, projection, provenance role and evidence identity. Table lights and Flasher sprites that only paint glow are excluded from emitter counts.", "", value["promotion_decision"], ""]
	return "\n".join(lines)

def verify_table_points(seed: dict[str, Any], folder: Path) -> None:
	"""Recompute stored points from source geometry, retaining the projection policy."""
	for collection in seed["placements"].values():
		for entries in collection.values():
			for entry in entries:
				if not (point := entry.get("table_point")):
					continue
				item = load_json(folder / point["source_path"])[entry["object_type"]]
				if point["method"] == "center":
					x, y = item["center"]["x"], item["center"]["y"]
				elif point["method"] == "drag_point_centroid":
					points = item["drag_points"]
					x, y = (sum(p[axis] for p in points) / len(points) for axis in ("x", "y"))
				else:
					raise ValueError(f"Unverified Dirty Harry point method: {point['method']}")
				if (x, y) != (point["x"], point["y"]) or (round(x / 964, 6), round(y / 2162, 6)) != (entry["x"], entry["y"]):
					raise ValueError(f"Dirty Harry table point drift: {entry['object']}")
				if entry.get("object_type") == "Light" and not item["show_bulb_mesh"]:
					raise ValueError(f"Dirty Harry GI object is not an explicit bulb: {entry['object']}")

def verify_run(pinned: dict[str, Any], run: dict[str, Any], name: str) -> None:
	"""Check observations against raw events, never host switch readback."""
	if run["failure"] or run["game"] != "dh_lx2" or run["handle_mechanics"] != 0:
		raise ValueError(f"Dirty Harry runtime contract mismatch: {name}")
	if run["library_sha256"] != pinned["library_sha256"] or run["scenario"]["sha256"] != pinned["scenario"]["sha256"]:
		raise ValueError(f"Dirty Harry runtime library/scenario drift: {name}")
	for observation in pinned["steps"]:
		step = run["steps"][observation["step"] - 1]
		snapshot = run["snapshots"][observation["step"]]
		if step["step"] != observation["step"] or step["label"] != observation["label"] or snapshot["label"] != observation["label"]:
			raise ValueError(f"Dirty Harry runtime step identity drift: {name}:{observation['step']}")
		frame = snapshot.get("displays", [{}])[0]
		if (step["transitions"].get("solenoids", []) != observation["solenoid_transitions"]
			or snapshot["active_solenoids"] != observation["active_solenoids"]
			or frame.get("pixel_sha256") != observation["display_pixel_sha256"]):
			raise ValueError(f"Dirty Harry runtime observation drift: {name}:{step['label']}")
	if "motor20_intervals_s" in pinned:
		events = [e for e in run["events"] if e.get("event") == "solenoid" and e.get("number") == 20]
		if [e["state"] for e in events] != [1, 0, 1, 0]:
			raise ValueError(f"Dirty Harry motor event order drift: {name}")
		intervals = [round(events[i + 1]["time_s"] - events[i]["time_s"], 6) for i in (0, 2)]
		if intervals != pinned["motor20_intervals_s"]:
			raise ValueError(f"Dirty Harry motor timeout drift: {name}")

def verify_runtime(seed: dict[str, Any], root: Path, retained: Path) -> None:
	ledger = load_json(root / "tools/seeds/williams/dirty-harry-1995-runtime.json")
	for name, expected in seed["evidence"]["runtime_manifests"].items():
		folder = retained / "runtime" / name
		manifest = build_manifest(folder, "dh_lx2")
		identity = (len(manifest["files"]), sum(f["size"] for f in manifest["files"]), check_manifest(folder, "dh_lx2"))
		if identity != (expected["file_count"], expected["total_bytes"], expected["sha256"]):
			raise ValueError(f"Dirty Harry runtime directory drift: {name}")
	for name, pinned in ledger["runs"].items():
		verify_run(pinned, load_json(retained / "runtime" / name / "run.json"), name)
	for header in load_json(root / "tools/seeds/williams/dirty-harry-1995-dmd-headers.json").values():
		path = retained / header["artifact"]
		if not path.is_file() or file_sha256(path) != header["file_sha256"]:
			raise ValueError(f"Dirty Harry DMD header source drift: {path}")
		magic, dimensions, maximum, pixels = path.read_bytes().split(b"\n", 3)
		first, last = header["rows"]
		mask = bytes(int(bool(v)) for v in pixels[first * 128:(last + 1) * 128])
		if (magic, dimensions, maximum) != (b"P5", b"128 32", b"255") or len(pixels) != 4096 or mask != base64.b64decode(header["mask"]):
			raise ValueError(f"Dirty Harry DMD header mask drift: {path}")
	# Exported world-space vertices prove the numbers used for offset primitives.
	groups: dict[str, list[list[float]]] = {}
	name = None
	with (retained / "sol-inspection/obj/Dirty Harry (1995).obj").open(encoding="utf-8") as stream:
		for line in stream:
			if line.startswith(("o ", "g ")):
				name = line[2:].strip()
				groups.setdefault(name, [])
			elif line.startswith("v ") and name:
				groups[name].append(list(map(float, line.split()[1:4])))
	for collection in seed["placements"].values():
		for entries in collection.values():
			for entry in entries:
				if not (bounds := entry.get("mesh_bounds_vpu")):
					continue
				vertices = groups[entry["object"]]
				low = [min(v[k] for v in vertices) for k in range(3)]
				high = [max(v[k] for v in vertices) for k in range(3)]
				point = (round((low[0] + high[0]) / 2 / 964, 6), round((low[1] + high[1]) / 2 / 2162, 6))
				if bounds != {"minimum": low, "maximum": high} or point != (entry["x"], entry["y"]):
					raise ValueError(f"Dirty Harry world mesh drift: {entry['object']}")

def verify_external(root: Path = ROOT) -> None:
	seed=load_seed(root)
	for env,paths in seed["external_files"].items():
		if value:=os.environ.get(env):
			for relative,sha in paths.items():
				path=Path(value)/relative
				if not path.is_file() or file_sha256(path)!=sha: raise ValueError(f"Dirty Harry retained artifact mismatch: {path}")
	if value:=os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
		folder=Path(value)/"williams/dirty-harry-1995/extracted"
		actual=build_manifest(folder,"dh_lx2")
		identity=(len(actual["files"]),sum(f["size"] for f in actual["files"]),hashlib.sha256(manifest_bytes(actual)+b"\n").hexdigest())
		expected=seed["evidence"]["extraction"]
		if identity!=(expected["file_count"],expected["total_bytes"],expected["sha256"]): raise ValueError(f"Dirty Harry full extraction drift: {identity}")
		verify_table_points(seed, folder)
	if value:=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
		verify_runtime(seed, root, Path(value) / MACHINE_ID)

def artifacts(root: Path = ROOT) -> dict[Path,bytes]:
	if (root/"machines/author-ready/williams/dirty-harry-1995.json").exists(): raise ValueError("Refusing to overwrite author-ready Dirty Harry")
	d=build(root); r=report(d,root)
	return {MACHINE:canonical_bytes(d),NOTE:(root/NOTE_SEED).read_bytes(),REPORT:canonical_bytes(r),REPORT_MD:render_report(r).encode("utf-8")}

def check(root: Path = ROOT) -> None:
	verify_external(root)
	for path,data in artifacts(root).items():
		if not (root/path).is_file() or (root/path).read_bytes()!=data: raise ValueError(f"Dirty Harry deterministic artifact drift: {path}")

def generate(root: Path = ROOT) -> None:
	verify_external(root)
	for path,data in artifacts(root).items():
		if path.suffix==".json": write_json(root/path,load_json_bytes(data))
		else: write_text(root/path,data.decode("utf-8"))

def load_json_bytes(data: bytes) -> Any:
	import json
	return json.loads(data)

def main() -> None:
	p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group(required=True)
	m.add_argument("--check",action="store_true");m.add_argument("--regenerate",action="store_true");args=p.parse_args()
	if args.check: check(); print("Dirty Harry deterministic artifacts and configured evidence match.")
	else: generate(); print("Wrote Dirty Harry definition, knowledge note and spatial reports.")

if __name__=="__main__": main()
