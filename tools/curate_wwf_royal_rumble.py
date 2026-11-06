"""Deterministic production WWF Royal Rumble curation from pinned factual excerpts.

No network or optional external evidence is needed to reproduce the artifacts.
External byte verification lives in the focused tests; missing or changed portable
inputs always fail. The curator owns the source and coverage decisions.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

import wwf_manual as manual
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.wwf-royal-rumble.1994"
SLUG = "wwf-royal-rumble-1994"
DEFINITION = f"machines/partial/data-east/{SLUG}.json"
SEED = f"tools/seeds/data-east/{SLUG}.json"
KNOWLEDGE = f"knowledge/data-east/{SLUG}.md"
REPORT = f"reports/spatial/data-east/{SLUG}.json"
MANUAL = "manual.wwf"
CORE = "pinmame.wwf"
S11 = "pinmame.wwf-s11"
CORE_C = "pinmame.wwf-core"
SCRIPT = "vpx-script.wwf-local"
TABLE = "vpx-table.wwf-local"
RUNTIME = "runtime.wwf"
CORE_REFS = [CORE, S11, CORE_C, "pinmame.wwf-core-h"]


def prov(*refs, status="validated"):
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason, *refs):
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def alias(namespace, address):
    return [{"namespace": namespace, "value": str(address)}]


def device(prefix, label, group, address, kind, refs, availability="used"):
    return {"id": prefix + "." + slug(label), "label": label, "kind": kind,
            "binding": {"group": group, "device": address}, "aliases": alias(
                "pinmame.switch" if group.endswith("switch") else "pinmame.lamp" if group.endswith("lamp") else "pinmame.solenoid", address),
            "availability": availability, "provenance": prov(*refs)}


def _load(root, path):
    return json.loads((root / path).read_text(encoding="utf-8"))


def build(root=ROOT):
    root = Path(root)
    evidence = _load(root, "tools/wwf_evidence.json")
    places = _load(root, "tools/wwf_places.json")
    if {d["id"] for d in evidence["drivers"]} != {"wwfr_106", "wwfr_103", "wwfr_103f"}:
        raise ValueError("Incomplete WWF driver inventory")
    if set(places["devices"]) != {f"switch.{n}" for n in [*range(9,48),*range(49,57),58]} | {f"solenoid.{n}" for n in [1,2,3,4,5,6,7,9,12,13,17,18,19,20,21,22]} | {"lamp.61"}:
        raise ValueError("Incomplete or unexpected WWF placement inventory")
    for relative, expected in evidence["portable_inputs"].items():
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Missing or changed WWF portable input: {path}")
    for source in evidence["sources"]:
        if source["kind"] == "runtime_scenario":
            runtime = root / source["uri"]
            if not runtime.is_file() or hashlib.sha256(runtime.read_bytes()).hexdigest() != source["sha256"]:
                raise ValueError(f"Missing or changed WWF runtime evidence: {runtime}")
        for excerpt in source.get("excerpts", []):
            path = root / excerpt["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != excerpt["sha256"]:
                raise ValueError(f"Missing or changed WWF excerpt: {path}")
            if excerpt.get("image"):
                image = root / excerpt["image"]
                if not image.is_file() or hashlib.sha256(image.read_bytes()).hexdigest() != excerpt["image_sha256"]:
                    raise ValueError(f"Missing or changed WWF excerpt image: {image}")
    switches, lamps, coils = manual.switch_rows(root), manual.lamp_rows(root), manual.coil_rows(root)
    sc, sr = manual.switch_column_headings(root), manual.switch_row_headings(root)
    lc, lr = manual.lamp_column_headings(root), manual.lamp_row_headings(root)
    inputs, outputs, relationships = [], [], []

    def locate(d, key, role):
        records = places["devices"].get(key, [])
        if records:
            d["spatial"] = {"status": "observed", "placements": [
                {"id": d["id"] + f".{role}.{i+1}", "role": role, "space": "playfield",
                 "x": p["x"], "y": p["y"], "provenance": prov(*p.get("source_refs", [TABLE,SCRIPT,MANUAL]), status="observed")}
                for i, p in enumerate(records)]}

    for n, row in switches.items():
        label = row["Parts-list description (p29)"]
        unused = label == "Not Used"
        d = device("switch", f"Unused {n}" if unused else label, "pinmame.input.switch", n,
                   "switch", [MANUAL, S11, CORE, RUNTIME], "unused" if unused else "used")
        d["aliases"] += [{"namespace": "manual.address", "value": f"{n:02}"}]
        col, r = sc[(n-1)//8+1], sr[(n-1)%8+1]
        d["wiring"] = {"board": "CPU", "drive_wire": col["Drive wire"], "drive_connection": col["CPU connection"],
                       "driver_transistor": col["Drive transistor"], "return_wire": r["Return wire"], "return_connection": r["CPU connection"]}
        note = "Printed matrix label: " + row["Matrix label (p28)"] + ". "
        if unused:
            d["spatial"] = na("unused", MANUAL)
        else:
            # The page 28 circuit uses N.O. and COM. Pinned row read is uninverted;
            # positive service-test observations are retained separately, not host readback.
            d["normally_closed"] = False
            d["physical"] = {"notes": note + "Page 28 wires the matrix contact N.O.–COM through a blocking diode; s11.c pia4a_r reads the uninverted matrix. Service-test readings are separate from injected host levels."}
            if row["Part No."] not in ("---", "See Cabinet"):
                d["physical"]["part_number"] = row["Part No."]
            if n <= 8 or n >= 62:
                d["spatial"] = na("cabinet_or_service", MANUAL)
            else:
                locate(d, f"switch.{n}", "sensor")
        if n in (63, 64):
            d["physical"]["notes"] += f" This is a synthesized cabinet-button matrix copy: core_updateSw overwrites direct host writes on each update. Drive public {84 if n==63 else 82}. The exact table's extra direct writes to {n} are ineffective."
        if n == 20:
            d["physical"]["notes"] += " The right VUK assembly page 55 lists 180-5116-00 instead of this chart's 180-5054-00. The binding and ball path agree."
        if n == 62:
            d["physical"]["notes"] += " The retained 2017 table drives TAG active-high from plunger and both MagnaSave keys. The retained VPU2.0.3 VR script reverses only its plunger path, after key-handler early-return guards; its MagnaSave paths remain active-high. This consumed-script inconsistency is not a hardware polarity claim."
            d["provenance"]["source_refs"].append("vpx-script.wwf-vpu203")
        inputs.append(d)
    inputs.extend(flipper_column_inputs(flip_swno=(63,64), flip_swno_text="FLIP_SWNO(63,64)",
        core_refs=CORE_REFS, button_refs=[SCRIPT,"vpm.wwf-de"],
        button_notes={"left":"The local table and de.vbs drive public 84. Physical lower and upper SSFB boards are separate; the table moves both same-side flippers together.",
                      "right":"The local table and de.vbs drive public 82. Physical lower and upper SSFB boards are separate; the table moves both same-side flippers together."},
        button_normally_closed=False))
    for n,label in [(-7,"Black Step Service Button"),(-6,"Green Forward Reverse Service Button")]:
        d=device("switch",label,"pinmame.input.switch",n,"switch",[S11,MANUAL])
        d["physical"]={"location":"coin door service panel","switch_type":"button"}
        d["spatial"]=na("cabinet_or_service",MANUAL);inputs.append(d)
    inputs.append({"id":"dip.pia2-port-a-bit7","label":"PIA2 Port A Bit 7 Configuration Input","kind":"dip_switch",
        "binding":{"group":"pinmame.input.dip","device":0},"availability":"unknown","aliases":[],
        "physical":{"notes":"The shared driver exposes one DIP bank and pia2a_r supplies core_getDip(0)<<7 under a shared Jumper W7 comment. DE_COMPORTS declares no Country DIP. Bounded static analysis of all three CPUs verifies normal DDRA=$FF, which masks external PA7; reviewed IRQ reads discard it and the fatal blink loop masks output to bit4. Indexed/scheduler coverage gaps prevent a whole-program unused claim. Raw DIP0=1 probes are separate stimuli. No WWF physical jumper or country setting is established."},
        "spatial":na("dip_switch",S11),"provenance":prov(S11,"pinmame.wwf-s11-h",CORE_C,"rom-static.wwf-pia2","pinmame.wwf-pia6821",status="observed")})

    for n,row in lamps.items():
        label=row["Location-table description (p31)"]
        d=device("lamp",label,"pinmame.output.lamp",n,"lamp",[MANUAL,S11,RUNTIME])
        d["aliases"] += alias("manual.address",f"{n:02}")
        c,r=lc[(n-1)//8+1],lr[(n-1)%8+1]
        d["wiring"]={"board":"CPU","drive_wire":c["18V drive wire"],"drive_connection":c["Connection"],
                     "driver_transistor":c["Transistor"],"return_wire":r["GND return wire"],"return_connection":r["Connection"],"return_component":r["Transistor"]}
        d["physical"]={"quantity":2 if n==28 else 1,"notes":"Printed matrix label: "+row["Matrix label (p30)"]+". "}
        if n in (15,16,27):d["spatial"]=na("cabinet_or_service",MANUAL)
        else:locate(d,f"lamp.{n}","emitter")
        if n in (15,16,27,59):d["physical"]["notes"] += "The local script omits this lamp binding; the manual and ROM establish its fitment."
        if n==15:
            d["physical"]["notes"] += " The newer VPU2.0.3 table adds its cabinet/VR lamp binding; this supplies no playfield socket."
            d["provenance"]["source_refs"].append("vpx-script.wwf-vpu203")
        if n in (62,63):
            d["physical"]["notes"] += " Physical bulb placement withheld: the manual lamp-location drawing places 62 at the front/bottom bumper and 63 at the rear/right bumper, while both related tables bind L62 to the rear/right body and L63 to the front/bottom body. The separate manual switch-location drawing agrees with the table's 50/51 sensor positions; matching names do not resolve lamp wiring. Verify actual lamp-test addresses or socket wires on a production machine."
            d["provenance"]["status"]="conflicted"
            d["provenance"]["source_refs"] += [SCRIPT,"vpx-script.wwf-vpu203"]
        outputs.append(d)

    for printed,row in coils.items():
        n=int(printed[:-1])+24 if printed.endswith("R") else int(printed.rstrip("L"))
        label=row["Description p33"].split(";")[0]
        unused=label=="Not Used"
        kind="flasher" if printed.endswith("R") else "gi" if n==11 else "relay" if n==10 else "motor" if n==16 else "virtual" if unused else "coil"
        d=device(kind,f"Unused Solenoid {n}" if unused else label,"pinmame.output.solenoid",n,kind,[MANUAL,S11,CORE_C,RUNTIME],"unused" if unused else "used")
        d["aliases"] += alias("manual.address",printed)
        d["physical"]={"notes":"Manual coil/flasher chart printed "+printed+". "}
        if not unused:
            for field,key in [("Coil or flash type","part_number")]:
                if row[field] != "---":d["physical"][key]=row[field]
            d["wiring"]={k:row[f] for k,f in [("board","Board"),("driver_transistor","Drive transistor"),("control_wire","D.T. control line"),("control_connection","Control connect"),("power_wire","Power line"),("power_connection","Power connection")] if row[f]!="---"}
        if printed.endswith("R"):
            q=4
            d["physical"].update(quantity=q,notes=d["physical"]["notes"]+row["Description p33"].split(";",1)[1].strip()+" as printed; quantity counts playfield and backbox insert bulbs together. Table effect lights do not prove every socket.")
            if n==32:d["physical"]["notes"] += " Page33 prints X1 P/F, Insert X2, but the game's schematic draws four bulbs and labels two playfield/two insert; its 32-bulb parts inventory and ROM's 2-INS 2-R/UPPER label corroborate four. Follow the schematic's fitted load and preserve the chart misprint."
            locate(d,f"solenoid.{n}","emitter")
        elif unused:d["spatial"]=na("unused",MANUAL)
        elif n in (8,10,16):d["spatial"]=na("cabinet_or_service",MANUAL)
        elif n==11:
            d["physical"]["notes"] += "Relay is on the power supply; its G.I. bulbs span the machine. PFGI inverts the callback: energized 11 darkens its collection. No dedicated GI callback exists. No total G.I. socket count or complete socket map is established."
        else:locate(d,f"solenoid.{n}","effect")
        if n in (5,6):d["physical"]["notes"] += "The assembly pages 54/55 specify 24-940 coils, unlike the 23-800 coil chart; retain the chart's part without treating the part-number disagreement as a binding conflict."
        if n==9:d["physical"]["notes"] += "Chart calls Q30 PPB; schematic page 34 draws it on the CPU board."
        if n>=17 and n<=22:d["physical"]["notes"] += "WWF's own Cycling Coils test pairs the printed name with this public output. The Data East PIA slot permutation is {3,4,5,1,0,2}; no sequential SP alias is invented."
        outputs.append(d)

    for n in [23,24,*range(33,51)]:
        if n==23:label,kind,availability,notes="Game On / Switched Solenoid Enable","control_signal","used","PIA0 CB2 enables switched coils and synthetic flippers; no separate playfield load."
        elif 37<=n<=44:label,kind,availability,notes=f"Printer Data Bit {n-37}","virtual","unknown","S11_PRINTERLINE exposes PIA2 port B here; no physical playfield load is fitted. Verified static printer code reads the $0A00 character buffer and writes PB after CRA IRQ2/CA2-ready. Stock s11 supplies no CA2 ready input, so the reviewed helper times out before its write. This explains bounded silent probes, not a whole-program unused claim or a reconstructed physical printer protocol."
        elif 45<=n<=48:
            side="Right" if n<47 else "Left";phase="Power" if n%2 else "Hold"
            label,kind,availability,notes=f"{side} Flipper {phase} State","virtual","used","core_updateSw synthesizes both same-side states together from the cabinet button and game-on enable. These are not two measured winding phases. The table reads 46/48 and moves both lower and upper same-side flippers together; the physical four-flipper inventory and separate SSFB supplies are retained in the mechanism note."
        else:label,kind,availability,notes=f"Unused Solenoid Address {n}","virtual","unused","This address has no WWF physical output: reserved gap, non-Data-East remap, or inactive simulator channel in the pinned core; WWF has no simulator or custom-solenoid handler."
        d=device("control" if n==23 else "virtual",label,"pinmame.output.solenoid",n,kind,CORE_REFS,availability)
        d["physical"]={"notes":notes};d["spatial"]=na("virtual",*CORE_REFS)
        if 37<=n<=44:
            d["provenance"]["status"]="observed"
            d["provenance"]["source_refs"] += ["rom-static.wwf-pia2","pinmame.wwf-pia6821"]
        outputs.append(d)

    imap={d["binding"]["device"]:d["id"] for d in inputs}
    smap={d["binding"]["device"]:d["id"] for d in outputs if d["binding"]["group"].endswith("solenoid")}
    relationships.extend(flipper_column_relationships(flip_swno=(63,64),matrix_ids={63:imap[63],64:imap[64]},refs=tuple(CORE_REFS)))
    mechanisms=[]
    spec=_load(root,"tools/wwf_mechanisms.json")
    expected_mechanisms = {"trough", "autolaunch", "ring-eject", "right-vuk", "scoop-vuk",
                           "lower-drop-bank", "upper-drop-bank", "back-diverter", "left-diverter",
                           "right-diverter", "flippers", "captive-ball", "shaker", "bumpers-slings"}
    if {m["id"] for m in spec} != {"mechanism." + name for name in expected_mechanisms} or len(spec) != len(expected_mechanisms):
        raise ValueError("Incomplete or duplicate WWF mechanism inventory")
    for m in spec:
        m=copy.deepcopy(m);m["actuators"]=[smap[n] for n in m["actuators"]];m["sensors"]=[imap[n] for n in m["sensors"]]
        m["provenance"]=prov(MANUAL,SCRIPT,CORE,status="observed" if m["id"]=="mechanism.right-diverter" else "validated");mechanisms.append(m)
    drivers=copy.deepcopy(evidence["drivers"])
    for d in drivers:
        d["physical_compatibility"]="identical"
        d["variant_notes"]="Production widebody WWF: shared GEN_DEDMD32, FLIP6364, S11_PRINTERLINE, 128x32 DMD and DE2S hardware. CPU/display revision and language differ; no hardware override. All three variants were probed with source-matching ROM members. The French CPU/display archive was obtained from archived IPDB and assembled with unchanged shared sound members. Prototype magnet test games and the narrowbody whitewood are not represented by these drivers."
    result={"format":"pinmame-machine-definition","schema_version":2,
        "machine":{"id":KEY,"name":"WWF Royal Rumble","manufacturer":"Data East","year":1994,"kind":"physical_pinball","model_number":"500-5523-01","ipdb_id":2820,"opdb_id":"G57y6-MLej6","playfield":{"width":1093,"height":2162,"units":"vpx","provenance":prov(TABLE)}},
        "controller":{"platform":"pinmame.dataeast","hardware_generation":"0x4000","inversion_applied_by_emulator":True},
        "coverage":{"status":"partial","missing":["input_semantics","output_semantics","mechanism_behavior","spatial_placement","unresolved_conflicts"],"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"observed","physical_wiring":"observed","mechanisms":"observed","variant_coverage":"validated","recreation_knowledge":"validated","spatial_placement":"conflicted","runtime_observation":"observed"}},
        "drivers":drivers,"inputs":inputs,"outputs":outputs,
        "displays":[{"id":"display.dmd","label":"Backbox Dot Matrix Display","kind":"dmd","controller_index":0,"width":128,"height":32,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service",MANUAL,CORE),"provenance":prov(MANUAL,CORE,RUNTIME)}],
        "mechanisms":mechanisms,"relationships":relationships,"sources":evidence["sources"],
        "conflicts":[{"id":f"wwf.lamp-{n}-physical-position","path":f"outputs.{'lamp.bottom-turbo-bumper' if n==62 else 'lamp.right-turbo-bumper'}.spatial",
            "description":f"Lamp {n}: the printed page 31 lamp drawing places 62 at the front/bottom bumper and 63 at the rear/right bumper. Both related VPX scripts bind 62 to the rear/right bulb body and 63 to the front/bottom body. The printed page 29 switch drawing separately places 50 rear/right and 51 front/bottom, matching the consumed sensor bindings despite their Bottom/Right labels. No independent socket wire trace or production lamp-test observation settles which lamp mapping is physical. Retain fitment and runtime bindings, and withhold the disputed physical coordinate. Resolution path: a production-machine owner or service technician can observe which bumper bulb lights for lamps 62 and 63 in the machine's lamp test, or trace each socket's lamp-matrix wire pair.",
            "source_refs":[MANUAL,SCRIPT,"vpx-script.wwf-vpu203"],"status":"unresolved"} for n in (62,63)],
        "knowledge":{"path":KNOWLEDGE,"status":"complete"}}
    return result


def artifacts(root=ROOT):
    d=build(root)
    places=_load(Path(root),"tools/wwf_places.json")
    report={"format":"pinmame-spatial-blockers","version":1,"machine_id":KEY,
        "coordinate_convention":"x left to right; y rear to front; (x/1093,y/2162), rounded to six decimals with repository helper",
        "placement_count":sum(len(x.get("spatial",{}).get("placements",[])) for c in ("inputs","outputs") for x in d[c]),
        "retained_evidence":_load(Path(root),"tools/wwf_evidence.json")["retained"],
        "lighting_audit":_load(Path(root),"tools/wwf_lighting_audit.json"),
        "objects":places,"blockers":["Complete physical bulb/socket map, especially G.I. count, wiring membership and all mixed playfield/backbox flash circuits; insert polygons and glow helpers are excluded.","Right upper diverter: table alternates position on each enabled pulse; physical startup orientation and correspondence to the coil/plunger/crank assembly need an operating-machine observation.","Meaningful WWF PIA2 printer-byte semantics at 37–44 remain unknown; absence in existing runs does not establish unused."],
        "promotion_decision":"Remain partial. No author-ready claim; physical placement is not manufactured from visual proxies."}
    report["blockers"].append("PIA2 port A bit 7 reads shared-core DIP bank 0; the WWF-specific physical configuration meaning is not established. DE_COMPORTS does not declare the System 11 Country DIP. A raw DIP=1 probe supplies no physical jumper identity.")
    report["blockers"].append("Lamps 62/63: manual lamp-location drawing versus related-table bulb bindings exchange the rear/right and front/bottom assemblies. Physical lamp-test or socket-wire evidence is needed; sensor 50/51 names do not settle it.")
    report["static_evidence_scope"] = "All three reviewed normal setups use DDRA=$FF. Reviewed printer-send code waits for CA2-ready IRQ2 absent from stock s11 input wiring. These bounded source/static explanations do not settle the physical jumper/printer protocol or exhaust indexed/scheduled code paths."
    return d,report,(Path(root)/"tools/wwf_knowledge.md").read_bytes()


def main():
    p=argparse.ArgumentParser(description=__doc__);mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true");mode.add_argument("--regenerate",action="store_true");p.add_argument("--repository-root",type=Path,default=ROOT);a=p.parse_args();root=a.repository_root.resolve()
    if (root/f"machines/author-ready/data-east/{SLUG}.json").exists():raise ValueError("Refusing to overwrite/demote an author-ready artifact")
    d,r,k=artifacts(root)
    payloads={DEFINITION:(json.dumps(d,indent="\t",sort_keys=True,ensure_ascii=False)+"\n").encode(),SEED:(json.dumps(d,indent="\t",sort_keys=True,ensure_ascii=False)+"\n").encode(),REPORT:(json.dumps(r,indent="\t",sort_keys=True,ensure_ascii=False)+"\n").encode(),KNOWLEDGE:k}
    for path,payload in payloads.items():
        target=root/path
        if a.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n",b"\n")!=payload.replace(b"\r\n",b"\n"):raise ValueError(f"WWF artifact drift: {target}")
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(payload)
    print("WWF definition, seed, knowledge and spatial report match." if a.check else "Regenerated WWF artifacts.")


if __name__=="__main__":main()
