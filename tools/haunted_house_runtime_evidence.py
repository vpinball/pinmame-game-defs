"""Derive small, fail-closed Haunted House observations from retained native traces."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json

ROOT=Path(__file__).resolve().parents[1]
FACTS=ROOT/"tools/seeds/gottlieb/haunted-house-1982-evidence.json"
OUTPUT=ROOT/"evidence/runtime/gottlieb.haunted-house.1982.json"
PIN="46e1a01a0f73dc5ce163d98db1ae435883ecc450"


def sha(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def derive(runtime_root: Path) -> dict[str, Any]:
	facts=load_json(FACTS)
	runs={}
	for info in facts["runtime_runs"]:
		path=runtime_root/info["raw_run_relative_path"]
		if not path.is_file() or sha(path)!=info["run_sha256"]:
			raise RuntimeError(f"missing or changed raw trace: {path}")
		run=load_json(path)
		if run.get("failure") or run.get("game")!="hh" or run.get("handle_mechanics")!=0:
			raise RuntimeError(f"failed or incompatible native trace: {path}")
		if run["library_sha256"]!=info["library_sha256"]:
			raise RuntimeError(f"wrong emulator: {path}")
		if run["scenario"]["sha256"]!=info["scenario_sha256"] or sha(ROOT/info["scenario_path"])!=info["scenario_sha256"]:
			raise RuntimeError(f"scenario drift: {path}")
		runs[info["name"]]=run
	service=runs["solenoid-test"]
	start=next(s["time_s"] for s in service["snapshots"] if s["label"]=="Step17 solenoid test")
	ons=[e for e in service["events"] if e["event"]=="solenoid" and e["state"] and 1<=e["number"]<=9 and e["time_s"]>start]
	# CORE_SEG9 BCD glyphs at the pinned core;6/9 deliberately differ from the
	# familiar seven-segment font. Read the multiplexed digit after it settles.
	glyphs={0x06:1,0x5b:2,0x6d:5,0x7c:6,0x7f:8,0x67:9}
	pairs=[]
	for event in ons:
		frames=[e for e in service["events"] if e["event"]=="display" and e["index"]==7 and e["time_s"]<=event["time_s"]+.25]
		if not frames:
			raise RuntimeError("coil test lacks its status digit")
		segments=frames[-1]["segments"]
		number=glyphs.get(segments[0]) if len(segments)==1 else None
		if number!=event["number"]:
			raise RuntimeError(f"coil/status mismatch: {event}, {segments}")
		pairs.append({"public_solenoid":event["number"],"status_digit_segments":segments,"displayed_number":number})
	if [p["public_solenoid"] for p in pairs] != [1,2,5,6,8,9]:
		raise RuntimeError("unexpected Haunted House coil-test sequence")
	gameplay=[]
	for step in runs["gameplay"]["steps"]:
		if step["type"] not in ("pulse","set_switch"):
			continue
		gameplay.append({"label":step["label"],"host_stimulus_switch":step["switch"],"host_state":step.get("state",step.get("active_state",1)),
			"active_solenoid_transitions":[d["number"] for d in step["transitions"]["solenoids"] if any(d["states"])],
			"active_lamp_transitions":[d["number"] for d in step["transitions"]["lamps"] if any(d["states"])],
			"solenoid_transitions":step["transitions"]["solenoids"],"lamp_transitions":[d for d in step["transitions"]["lamps"] if d["number"]<18]})
	named=[]
	for action in gameplay:
		named.append({"label":action["label"],"input_kind":"switch","input_address":action["host_stimulus_switch"],
			"observed_switch_addresses":[],"host_stimulus_switch_addresses":[action["host_stimulus_switch"]],
			"active_solenoid_addresses":[],"transitioned_solenoid_addresses":[d["number"] for d in action["solenoid_transitions"]],
			"result":"observed" if action["active_solenoid_transitions"] or action["active_lamp_transitions"] else "no_matching_transition"})
	raw=[]
	for info in facts["runtime_runs"]:
		run=runs[info["name"]]
		raw.append({"name":info["name"],"sha256":info["run_sha256"],"self_test_pulses":{"gameplay":0,"lamp-driver-test":1,"solenoid-test":2}[info["name"]],
			"scenario_path":info["scenario_path"],"scenario_sha256":info["scenario_sha256"],"action_count":run["scenario"]["action_count"],
			"nvram_initialization":"New empty state directory for this run; no inherited NVRAM.","initial_switches":run["initial_switches"],"watch_switches":run["watch_switches"],"snapshot_count":len(run["snapshots"])})
	sequence=[p["public_solenoid"] for p in pairs]
	return {"format":"pinmame-machine-evidence","version":1,"extractor":{"id":"haunted_house_runtime_evidence.py","version":1},
		"source":{"kind":"runtime_scenario","repository":"https://github.com/vpinball/pinmame","revision":PIN,
			"path":"runtime-evidence/haunted-house-1982/gameplay/run.json","sha256":next(i["run_sha256"] for i in facts["runtime_runs"] if i["name"]=="gameplay"),
			"license":"Locally generated factual observations; ROMs and NVRAM not redistributed","quality":"observed","attribution":"PinMAME contributors and primary curator"},
		"driver_ids":["hh"],"machine_ids":["gottlieb.haunted-house.1982"],"switches":[],"outputs":[],"states":[],"mechanisms":[],"recreation_notes":[],
		"runtime":{"game":"hh","rom_archive_sha256":facts["runtime_runs"][0]["rom_archive_sha256"],
			"emulator":{"binary":"builds/pinmame-46e1a01a/Release/pinmame64.dll","sha256":facts["runtime_runs"][0]["library_sha256"],"built_from_revision":PIN},
			"raw_runs":raw,"command_template":"python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game hh --rom-path <authorized-read-only-ROM-root> --work-dir <new-empty-state> --scenario tools/harness-scenarios/gts80/haunted-house-<name>.json --output <working-root>/runtime-evidence/haunted-house-1982/<name>/run.json",
			"observations":{"ordered_solenoid_on_sequence":sequence,"physical_service_solenoid_to_public":{str(i):i for i in sequence},
				"lamp_addresses_seen":sorted({e["number"] for e in runs["lamp-driver-test"]["events"] if e["event"]=="lamp"}),
				"display_indices_seen":sorted({e["index"] for e in service["events"] if e["event"]=="display_available" and e["type"] in (3,11)}),
				"runs":{"solenoid-test":{"ordered_solenoid_on_sequence":sequence,"note":f"Status display entry7 glyph pairs, read0.25s after output: {pairs}. Binary mode, keyboard handling off, mechanics0. No physical timing inferred."},
					"gameplay":{"named_action_observations":named,"note":"Direct host stimulus only; only output transitions/displays are ROM evidence. Lamp4 pulses at ball serve without an explained fitted load. Socket positions and physical quantities cannot be recovered from output activity."}}}}}


def main() -> None:
	p=argparse.ArgumentParser(description=__doc__)
	p.add_argument("--runtime-root",type=Path,required=True)
	p.add_argument("--check",action="store_true")
	a=p.parse_args()
	data=canonical_bytes(derive(a.runtime_root))
	if a.check:
		if not OUTPUT.is_file() or OUTPUT.read_bytes()!=data:
			raise RuntimeError("Haunted House compact runtime evidence drift")
	else:
		OUTPUT.parent.mkdir(parents=True,exist_ok=True)
		OUTPUT.write_bytes(data)
	print("Haunted House runtime evidence verified" if a.check else OUTPUT.relative_to(ROOT))


if __name__=="__main__":
	main()
