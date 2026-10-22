"""Deterministically curate Sega Baywatch (1995), Data East 3b, from reviewed evidence.

The complete printed regions in evidence/excerpts are the tabular input; baywatch_places.json
contains recomputable observed geometry. No external evidence is needed to regenerate. Optional
evidence roots are verified fail-closed when provided. A partial cannot overwrite an author-ready
record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_flipper_column import (
    flipper_column_inputs, flipper_column_relationships, vpm_staged_flipper_notes,
    VPM_DE2_LIBRARY_SOURCE, VPM_DE2_LIBRARY_URI, VPM_DE2_SHA256,
)

ROOT=Path(__file__).resolve().parents[1]
KEY="sega.baywatch.1995"
SLUG="baywatch-1995"
REV="97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
MANUAL="manual.baywatch.production"
BULLETIN="bulletin.baywatch.74"
CORE="pinmame.baywatch.core"
SCRIPT="vpx-script.baywatch.kiwi-1-0-5"
TABLE="vpx-table.baywatch.kiwi-1-0-5"
EXTRACTION="vpx-extraction.baywatch.kiwi-1-0-5"
RUNTIME="runtime.baywatch.usa-4-00"
GEOMETRY="geometry.baywatch.kiwi-1-0-5"
DRAWING_COMPARISON="geometry.baywatch.lamp-drawing-comparison"
PHOTOS="photos.baywatch.physical"
DEFINITION_PATH=ROOT/f"machines/partial/sega/{SLUG}.json"
SEED_PATH=ROOT/f"tools/seeds/sega/{SLUG}.json"
KNOWLEDGE_PATH=ROOT/f"knowledge/sega/{SLUG}.md"
SPATIAL_REPORT_PATH=ROOT/f"reports/spatial/sega/{SLUG}.json"
EXCERPTS=ROOT/"evidence/excerpts"/KEY
UNUSED_SWITCHES={27,29,34,35,51}
MISSING=["input_semantics","output_semantics","spatial_placement"]
MIXED_FLASHERS={25,27,28,29,30,32}
MANUALS={
    "Baywatch_Manual.pdf":"9545ae03f7ef1bcc41f3e5e08b6be996d581f9141b1f70228fe9969ba9ace400",
    "Sega_1995_Baywatch_Sample_Game_Manual.pdf":"365ca47e98af2c6a76131ef6157befc99e57c90472d2a5f30810d9b232fe1d60",
    "Sega_1995_Baywatch_Service_Bulletin_74_April_28_1995_Modification_to_Baywatch_Early_Production_Games.pdf":"bbf2fa017b7f693edafe1df0b01cc4e28a4b2c7e18f68ebca1339cae0eca79b4",
}
SWITCH_LABELS=(
    "Plumb Bob Tilt|4th Coin Slot|Start Button|Right Coin Slot|Center Coin Slot|Left Coin Slot|Slam Tilt|Extra Ball Buy-in / League Button|"
    "2-Bank Stand-up Top|Trough Ball 1 Left|Trough Ball 2|Trough Ball 3|Trough Ball 4|Trough Ball 5 Right|Trough VUK Opto|Shooter Lane|"
    "SHARK S Bottom|SHARK H|SHARK A|SHARK R|SHARK K Top|Drop Target Top|Drop Target Middle|Drop Target Bottom|Left Ramp Enter|Left Ramp Exit|Unused 27|Right Ramp Enter|Unused 29|Right Ramp Exit|"
    "Right Ramp Stand-up Left|Right Ramp Stand-up Right|Left Return Lane|Unused 34|Unused 35|Left Ramp Stand-up Left|Left Ramp Stand-up Right|Top Lane Left|Top Lane Middle|Top Lane Right|"
    "Left Turbo Bumper|Bottom Turbo Bumper|Right Turbo Bumper|Upper VUK|Left Orbit Rollover|Lower Super VUK|Upper Ball Launch Rollover|Center Ramp Stand-up|Center Ramp Exit|Ball Launch Button|Unused 51|Spinner|2-Bank Stand-up Bottom|Shark Fin Flipper Rollover|Under Playfield Ramp Enter|Shark Super Scoop|Left Outlane|Right Outlane|Right Outer Return Lane|Right Inner Return Lane|Left Slingshot|Right Slingshot|Left Flipper Button Matrix Copy|Right Flipper Button Matrix Copy"
).split("|")
LAMP_LABELS=(
    "10 Million / Video Mode|20 Million / Laser Kick|30 Million / Shark|50 Million / Light Extra Ball|100 Million / Earthquake|Search and Rescue Sign|Ball Launch Button|Extra Ball Buy-in / League Button|Shoot Again|Left Turbo Bumper|Shark Super Scoop Sign|Tourist Season Sign|Ironman Sign|Shark Flip|Laser Target|Kick Target|"
    "SHARK S|SHARK H|SHARK A|SHARK R|SHARK K|Light Lock|Lock|Squid Pops|Special Left and Right Outlanes|Laser Kick|Shark Jackpot|Ramp Jackpot|Helicopter|Extra Ball Upper VUK|Wave Runner|Scarab|Tower Lock 1|Tower Lock 2|Tower Lock 3|ATV|Rescue Truck|SPF S Left|SPF P Middle|SPF F Right|"
    "GUARD G|Mitch|CPR|Surfboard Left Ramp|GUARD U|Matt|Copter Rescue|Surfboard Center Ramp|GUARD A|CJ|Diver Trapped|Surfboard Upper VUK|GUARD R|Caroline|Shark Cove|Surfboard Right Ramp|GUARD D|Stephanie|Tidal Wave|Surfboard Spinner|Tidal Wave Left Orbit|Earthquake Upper VUK|Tidal Wave Spinner|Start Button"
).split("|")
COIL_LABELS={
    1:"Trough Lock Ball",2:"Trough Up-kicker",3:"Auto Ball Launch",4:"Upper Ball Launch",5:"Upper VUK",6:"Lower Super VUK",7:"Shark Super Scoop",8:"Knocker",9:"Upper Control Gate",10:"Left Right A-B Relay",11:"General Illumination Relay",12:"Tower Lock Trapdoor",13:"Upper Left and Right Flippers",14:"Lower Control Gate",16:"Drop Bank Reset",17:"Left Turbo Bumper",18:"Bottom Turbo Bumper",19:"Right Turbo Bumper",20:"Left Slingshot",21:"Right Slingshot",22:"Laser Kick",
    25:"Rear Panel and Backbox Flashers",26:"SHARK Bank and Slings Flashers",27:"Upper Right Flipper Flashers",28:"Upper Left Flipper and Ramp Flashers",29:"Upper VUK Flashers",30:"Spinner Entrance Flashers",31:"Turbo Bumper Flashers",32:"Right Sling and Ramp Flashers",
}
DRIVER_ROWS=(
    ("bay_401","Baywatch (4.01 unofficial MOD)","2017"),
    ("bay_402","Baywatch (4.02 unofficial MOD)","2025"),
    ("bay_d300","Baywatch (3.00 Dutch)","1995"),
    ("bay_d400","Baywatch (4.00 Dutch)","1995"),
    ("bay_e400","Baywatch (4.00 English)","1995"),
    ("bay_f201","Baywatch (2.01 French)","1995"),
    ("bay_g300","Baywatch (3.00 German)","1995"),
    ("baywatch","Baywatch (4.00)","1995"),
)


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def prov(*refs,status="validated"): return {"status":status,"source_refs":list(dict.fromkeys(refs))}
def na(reason,*refs): return {"status":"not_applicable","reason":reason,"provenance":prov(*refs)}
def slug(text): return re.sub(r"[^a-z0-9]+","-",text.lower()).strip("-")
def aliases(group,n,manual=None):
    return [{"namespace":f"pinmame.{group}","value":str(n)}]+([] if manual is None else [{"namespace":"manual.address","value":manual}])


def rows(filename,columns):
    """Parse only complete pipe rows of a declared width; fail on incomplete numeric data."""
    result=[]
    for line in (EXCERPTS/filename).read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):continue
        cells=[x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells)==columns and re.fullmatch(r"\d+[LR]?",cells[0]):result.append(cells)
    return result


def checked_excerpt(filename,locator):
    path=EXCERPTS/filename
    return {"id":slug(path.stem),"locator":locator,"path":path.relative_to(ROOT).as_posix(),
            "sha256":sha(path),"method":"manual","transcribed_by":"Curator; direct visual verification of retained native-resolution renders","reviewed":True}


def drawing_excerpt(name,locator,derivation,filename="drawings.md"):
    excerpt=checked_excerpt(filename,locator)
    excerpt.update(id=name,image=f"evidence/excerpts/{KEY}/{name}.webp",image_sha256=sha(EXCERPTS/f"{name}.webp"),image_derivation=derivation)
    return excerpt


def drawing_excerpts():
    return [
        drawing_excerpt("upper-flipper-control","PDF 109 / printed 105, CPU Q26 and parallel N.O. upper flipper cabinet controls","Baywatch_Manual.pdf page 109, crop box 0.055,0.465,0.74,0.91, scanned page rendered at its native resolution (embedded image xref 866, 3300px across 11.00in), rendered at 146 dpi, capped to 1700px wide, grayscale, 1701x716 WebP quality 70"),
        drawing_excerpt("auto-launch-assembly","PDF 70 / printed 66, upper drawing, assembly 500-5969-00-33","Baywatch_Manual.pdf page 70, crop box 0.14,0.02,0.875,0.33, scanned page rendered at its native resolution (embedded image xref 554, 3300px across 11.00in), rendered at 184 dpi, capped to 1150px wide, grayscale, 1151x629 WebP quality 70"),
        drawing_excerpt("upper-launch-assembly","PDF 70 / printed 66, lower drawing, assembly 500-5862-06-33","Baywatch_Manual.pdf page 70, crop box 0.11,0.482,0.89,0.805, scanned page rendered at its native resolution (embedded image xref 554, 3300px across 11.00in), rendered at 173 dpi, capped to 1150px wide, grayscale, 1151x617 WebP quality 70"),
        drawing_excerpt("playfield-flasher-layout","PDF 43 / printed 39, complete right-hand playfield flasher-location drawing","Baywatch_Manual.pdf page 43, crop box 0.515,0.29,0.985,0.928, scanned page rendered at its native resolution (embedded image xref 338, 3300px across 11.00in), rendered at 143 dpi, capped to 570px wide, grayscale, 571x1002 WebP quality 55"),
        drawing_excerpt("flasher-bulb-composition","PDF 88 / printed 84, complete eight-branch detailed flasher drawing","Baywatch_Manual.pdf page 88, crop box 0.3,0.62,0.975,0.907, scanned page rendered at its native resolution (embedded image xref 698, 3300px across 11.00in), rendered at 174 dpi, capped to 2000px wide, grayscale, 2001x551 WebP quality 70"),
        drawing_excerpt("service-contact-construction","PDF 86 / printed 82, both service contacts and complete CN14 diagnostic branch","Baywatch_Manual.pdf page 86, crop box 0.23,0.09,0.718,0.211, scanned page rendered at its native resolution (embedded image xref 682, 3300px across 11.00in), rendered at 193 dpi, capped to 1600px wide, grayscale, 1601x258 WebP quality 70"),
        drawing_excerpt("lamp-tower-comparison","PDF 41 / printed 37, all three tower lamp socket symbols and their numbers","Baywatch_Manual.pdf page 41, crop box 0.16,0.205,0.27,0.278, scanned page rendered at its native resolution (embedded image xref 322, 3300px across 11.00in), rendered at 300 dpi, grayscale, 281x242 WebP quality 70","lamp-drawing-comparison.md"),
        drawing_excerpt("lamp-sign-comparison","PDF 41 / printed 37, lamp 12 socket symbol and number","Baywatch_Manual.pdf page 41, crop box 0.452,0.369,0.518,0.426, scanned page rendered at its native resolution (embedded image xref 322, 3300px across 11.00in), rendered at 300 dpi, grayscale, 169x189 WebP quality 70","lamp-drawing-comparison.md"),
    ]


def spatial(key,identifier,role,places):
    hits=places["placements"].get(key,[])
    if not hits:return None
    return {"status":"observed","placements":[{"id":f"{identifier}.{role}.{i}","role":role,"space":"playfield","x":h["x"],"y":h["y"],"provenance":prov(TABLE,SCRIPT,MANUAL,GEOMETRY,status="observed")} for i,h in enumerate(hits,1)]}


def drawing_comparison(places):
    """Compare independently read drawing symbols with table points, without fitting them."""
    measurement=load_json(ROOT/"tools/baywatch_lamp_drawing.json")
    corners=measurement["frame_corners_px"]
    left=(corners["rear_left"][0]+corners["front_left"][0])/2
    right=(corners["rear_right"][0]+corners["front_right"][0])/2
    rear=(corners["rear_left"][1]+corners["rear_right"][1])/2
    front=(corners["front_left"][1]+corners["front_right"][1])/2
    measurement["comparison_rectangle_px"]={"left":left,"right":right,"rear":rear,"front":front}
    for group in ("floor_controls","elevated_lamps"):
        for point in measurement[group]:
            px,py=point["centre_px"]
            x,y=(px-left)/(right-left),(py-rear)/(front-rear)
            table=places["placements"][f"lamp.{point['address']}"][0]
            point.update(drawing_normalized=[round(x,6),round(y,6)],
                         table_object=table["object"],table_normalized=[table["x"],table["y"]],
                         table_minus_drawing=[round(table["x"]-x,6),round(table["y"]-y,6)])
    return measurement


def drawing_warning(n,comparison):
    point=next(p for p in comparison["elevated_lamps"] if p["address"]==n)
    x,y=point["drawing_normalized"];tx,ty=point["table_normalized"]
    return (f"Unreconciled drawing/table position: the PDF 41 / printed 37 socket body measures approximately ({x:.6f}, {y:.6f}) in the drawing frame, whereas {point['table_object']} is ({tx:.6f}, {ty:.6f}) in the table. "
            "These elevated lamps may be projected differently in the plan drawing. The floor controls do not establish a factory coordinate for them. Retain the script-linked world-mesh position as observed, with drawing comparison uncertainty about +/-0.009 x and +/-0.004 y and additional unquantified projection uncertainty; see lamp-drawing-comparison.md and the spatial report. ")


def build():
    switches={int(r[0]):r for r in rows("switches.md",5)}
    lamps={int(r[0]):r for r in rows("lamps.md",3)}
    coils={r[0]:r for r in rows("coils.md",10) if not (r[0] in {"1","2"})}
    if set(switches)!=set(range(1,65)) or set(lamps)!=set(range(1,65)) or len(coils)!=30:
        raise ValueError("incomplete Baywatch printed table inputs")
    if len(SWITCH_LABELS)!=64 or len(LAMP_LABELS)!=64:raise ValueError("incomplete Baywatch semantic inventory")
    places=load_json(ROOT/"tools/baywatch_places.json")
    comparison=drawing_comparison(places)
    inputs=[];outputs=[]
    drive_pins=[1,2,3,4,5,7,8,9];return_pins=[9,8,7,6,5,3,2,1]
    drive_colors=["BRN","RED","ORG","YEL","BLK","BLU","VIO","GRY"]
    return_colors=["BRN","RED","ORG","YEL","GRN","BLU","VIO","GRY"]
    for n in range(1,65):
        chart=switches[n]; label=SWITCH_LABELS[n-1];identifier="switch."+slug(label)
        col,row=(n-1)//8,(n-1)%8
        unused=n in UNUSED_SWITCHES
        notes=f"Matrix chart: {chart[1]}. Parts list: {chart[2]}; marker {chart[4]}. Full printed rows and connector headings are retained in switches.md."
        if n==15:notes+=" The manual's own OPTO Theory of Operation (PDF 111) explicitly says clear beam = open matrix switch and blocked beam = closed; no extra host inversion. The table's ball stack asserts 15 while occupied."
        if n==45:notes+=" The cabinet '*' marker is misplaced: the same location drawing puts it under 49 on the rear left orbit, and sw45 is a playfield rollover in the script."
        if n==54:notes+=" A ball-operated wire-form rollover ahead of the Shark Fin flipper, not an EOS contact; the test on printed page 33 says a ball actuates it to trigger the automatic shot."
        if n in (63,64):notes+=f" FLIP6364 copies {'84' if n==63 else '82'} into this matrix address every update. Drive that flipper-column button, not {n}. The script's direct writes to {n} precede de2.vbs, which writes the effective button; a direct write alone is overwritten."
        if n==30:notes+=" Explicitly Not Shown in the factory location drawing; sw30 is bound by Hit/UnHit in the exact table."
        if n==47:notes+=" This rollover is along the upper-launch guide ahead of the plunger, not at its coil pivot: the exact table has sw47 at y=1314 and UpBLaunch at y=1416. Both observed coordinates are retained without forcing them to coincide."
        item={"id":identifier,"label":label,"kind":"switch","binding":{"group":"pinmame.input.switch","device":n},"aliases":aliases("switch",n,str(n)),"availability":"unused" if unused else "used","provenance":prov(MANUAL,CORE,*([] if unused else [SCRIPT])),"physical":{"notes":notes},"wiring":{"board":"CPU","driver_transistor":f"Q{55-col}","drive_wire":"GRN-"+drive_colors[col],"drive_connection":f"CN8-{drive_pins[col]}","return_wire":"WHT-"+return_colors[row],"return_connection":f"CN10-{return_pins[row]}"}}
        if not unused:
            item["normally_closed"]=False
            item["physical"]["switch_type"]="opto" if n==15 else "tilt" if n in (1,7) else "button" if n in (3,8,50,63,64) else "microswitch" if n in (*range(10,15),25,28) else "other"
            if re.match(r"\d{3}-",chart[3]): item["physical"]["part_number"]=chart[3]
        if n in (63,64):item["roles"]=[f"flipper.lower.{'left' if n==63 else 'right'}.matrix-copy"]
        if unused:item["spatial"]=na("unused",MANUAL)
        elif n<=8 or n in (50,63,64):item["spatial"]=na("cabinet_or_service",MANUAL,CORE)
        elif (s:=spatial(f"switch.{n}",identifier,"sensor",places)):item["spatial"]=s
        inputs.append(item)
    for n,label in [(-7,"Begin Test / Enter Black Button"),(-6,"Service Credits / Select Green Button")]:
        inputs.append({
            "id":f"switch.service-{'enter' if n==-7 else 'select'}",
            "label":label,"kind":"switch",
            "binding":{"group":"pinmame.input.switch","device":n},
            "aliases":aliases("switch",n),"availability":"used","pulse":True,
            "normally_closed":False,
            "physical":{
                "switch_type":"button","location":"inside coin door",
                "notes":"The cabinet wiring drawing (PDF 86 / printed 82) explicitly draws STEP and FOR/REV as normally-open contacts. Bulletin 74 requires both buttons to be momentary: remove the silver C-shaped latching wire form from the early green switch. des112 uses DE_COMPORTS2 and the ROM uses Enter and Select in Portals; the older diagnostics prose still describes FORWARD/REVERSE navigation. Electrical contact rest state and mechanical latching are separate facts."
            },
            "wiring":{"board":"CPU","control_wire":"GRN" if n==-7 else "BLU",
                      "control_connection":"CN14-1" if n==-7 else "CN14-2",
                      "return_wire":"WHT","return_connection":"CN14-3"},
            "provenance":prov(BULLETIN,MANUAL,CORE,SCRIPT),
            "spatial":na("cabinet_or_service",BULLETIN,MANUAL)
        })
    inputs.extend(flipper_column_inputs(flip_swno=(63,64),flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)",core_refs=(CORE,),button_refs=(SCRIPT,VPM_DE2_LIBRARY_SOURCE),button_notes={side:f"The table calls de2.vbs vpmKeyDown/vpmKeyUp, whose sw{'LL' if side=='left' else 'LR'}Flip is {84 if side=='left' else 82}. Both upper and lower {side} flippers have cabinet switch wiring in the game's SSFB diagram; the upper pair additionally accept CPU output 13." for side in ("left","right")},unused_notes=vpm_staged_flipper_notes(library="DE2.VBS"),unused_note_refs=(VPM_DE2_LIBRARY_SOURCE,)))
    for item in inputs:
        if item["binding"]["device"] in (82,84):item["normally_closed"]=False;item["provenance"]["source_refs"].append(MANUAL)
    inputs.append({"id":"dip.country-jumper-w7","label":"Country Jumper W7","kind":"dip_switch","binding":{"group":"pinmame.input.dip","device":0},"aliases":[],"availability":"unknown","physical":{"notes":"s11.c pia2a_r reads core_getDip(0)<<7. No retained Baywatch-specific evidence assigns the two public values to a country or a fitted jumper position; do not import another game's setting."},"provenance":prov(CORE,status="observed"),"spatial":na("dip_switch",CORE)})

    for n in range(1,65):
        manual_number=f"{n}L" if n<=8 else f"{n-24}R" if 25<=n<=32 else f"{n:02d}"
        printed=coils.get(manual_number)
        if n in COIL_LABELS:
            kind="flasher" if n>=25 else "gi" if n==11 else "relay" if n==10 else "coil"
            label=COIL_LABELS[n];identifier=f"{kind}."+slug(label)
            notes=f"Printed circuit {manual_number}. "
            notes+= "The whole driver table, including merged and unused cells, is retained in coils.md. "
            physical={"notes":notes}
            if printed:
                physical["part_number"]=printed[9].strip("{}")
            if n>=25:
                physical["quantity"]=4
                physical["notes"]+="Four physical sockets: the printed circuit quantities and backbox/playfield location drawing distinguish the playfield/rear-panel bulbs from the backbox insert bulbs. The general chart says Bulb #89; the detailed schematic has mixed #89/#906 populations on six circuits, preserved completely in coils.md. The parts inventory's unsplit total is not a per-circuit socket survey. "
            elif n==13:physical["quantity"]=2
            elif n not in (10,11):physical["quantity"]=1
            if n==1:physical["notes"]+="25-1240 lock-ball cam releases one of five trough balls toward the separate up-kicker; no physical lock-cam object exists in the retained table."
            if n==3:physical["notes"]+="Auto Ball Launch assembly 500-5969-00-33 and the table's Plunger1 establish the lower shooter. The circuit schematic mislabels 3L UPPER BALL LAUNCH 24-940; use the assembly's 23-800 and the driver chart."
            if n==4:physical["notes"]+="Upper Ball Launch (Kick Big) assembly 500-5862-06-33, the separate mid-right UpBLaunch plunger and switch 47. The schematic prints 22-800; the chart and assembly print 24-940."
            if n==6:physical["notes"]+="Printed description says 50V, but the power cells say BRN / PPB J6-1,2 / 32v L. This wording discrepancy is preserved; the device is the under-arch subway exit, not the rear upper VUK."
            if n==10:physical["notes"]+="K1 A/B relay on PPB selects the 1-8 versus 25-32 banks; these are eight shared drivers with alternate loads."
            if n==11:physical["notes"]+="A single relay controls G.I.; it is an ordinary solenoid callback, not a separate GI callback. GIRelay inverts Enabled into local SetLamp 200. Lamp 200 is script-local and never a public matrix address. Table bulb placements are observed; the full circuit socket quantity and backbox/cabinet allocation are not settled."
            if n==12:physical["notes"]+="27-950 opens the left metal ramp trapdoor into the under-playfield return. Botola is the physical animated door pivot; RampLG1/2/3/6 are collision-state helpers."
            if n==13:physical["notes"]+="Two physical upper flipper coils (left 24-1570, right 23-1100), driven through SSFB CN1 by Q26. AutoFlipper moves both LeftFlipper1 and RightFlipper1. The upper SSFB wiring shows N.O. cabinet buttons and diode-isolated CPU input in parallel, so neither the CPU pulse nor the player-button path erases the other."
            if n==16:physical["notes"]+="One reset coil raises drop targets 22/23/24. Its coordinate is explicitly a projection onto middle target sw23, not a measured coil centre."
            if n==25:physical["notes"]+="Both non-backbox bulbs are on the rear panel (DomeBW191/191a); PDF 45's '1 DROP TARGET, 1 BACK PANEL' wording disagrees with PDF 43/44 and the physical photograph. No drop-bank sprite is promoted."
            if n==29:physical["notes"]+="Only glow sprites f195a/f195b exist for the two playfield bulbs; no sprite origin is admitted as a socket."
            if n==30:physical["notes"]+="DomeBW196 locates one playfield bulb. The second physical socket has no admitted table object."
            item={"id":identifier,"label":label,"kind":kind,"binding":{"group":"pinmame.output.solenoid","device":n},"aliases":aliases("solenoid",n,manual_number),"availability":"used","physical":physical,"provenance":prov(MANUAL,CORE,SCRIPT)}
            if printed:
                item["wiring"]={"board":printed[3].strip("{}"),"driver_transistor":printed[2].strip("{}"),"control_wire":printed[4],"control_connection":printed[5],"power_wire":printed[6],"power_connection":printed[7]}
            if n in MIXED_FLASHERS:
                item["physical"].pop("part_number",None)
                item["physical"]["notes"]+=" conflict.flasher-bulb-composition: exact #89/#906 population is unsettled; no exclusive bulb type is asserted."
                item["provenance"]["status"]="conflicted"
            if n in (8,10):item["spatial"]=na("cabinet_or_service",MANUAL)
            elif (s:=spatial(f"solenoid.{n}",identifier,"emitter" if kind in ("gi","flasher") else "effect",places)):item["spatial"]=s
        else:
            is_aux=37<=n<=44;is_flip=45<=n<=48
            label=(f"CN3 Printer Data Bit {n-37}" if is_aux else f"Synthetic Lower {'Right' if n<=46 else 'Left'} Flipper {'Power' if n%2 else 'Hold'}" if is_flip else "Unassigned Driver 15 (Printed Not Used)" if n==15 else f"Unused Solenoid Address {n}")
            identifier=f"virtual.{slug(label)}"
            printer_pin={37:9,38:8,39:7,44:1}.get(n)
            note=("S11_PRINTERLINE publishes PIA2:B bit "+str(n-37)+" here. "+(f"The pinned pia2b_w comment explicitly names CN3 pin {printer_pin}. " if printer_pin is not None else "The pinned pia2b_w comment elides bits 3-6; no connector-pin assignment is asserted. ")+"Portals Adjustment 53 was exercised through TRANSMITTING DATA and CHECK CONNECTIONS, but no 37-44 transition was observed. That does not prove non-use; no playfield load is documented. Keep availability unknown."
                  if is_aux else "core_updateSw fabricates the paired power/hold states together from cabinet button "+str(82 if n<=46 else 84)+" while 23 enables flippers. They are virtual button-controlled states, not four independently wired CPU coils. The table uses the hold callbacks (de2.vbs sLRFlipper/sLLFlipper) to move both flippers on that side; the physical upper pair also accepts output 13."
                  if is_flip else "Printed coil 15 is NOT USED with dash marks in every authoring column, and the ROM's cycling test also names it NOT USED. A successful gameplay probe nevertheless published pulses at 15 outside the cycling test. Their purpose is not settled; neither those pulses nor non-binding in the table prove a fitted physical load. Keep availability unknown instead of silently declaring this runtime state unused." if n==15 else "No Baywatch physical load or custom driver is present at this address: 24 reserved, 33-36 have no Data East core_getSol path, 49 is a simulator slot with no Baywatch simulator, 50 reserved, 51-64 require custSol/getSol which this initializer does not declare.")
            item={"id":identifier,"label":label,"kind":"virtual","binding":{"group":"pinmame.output.solenoid","device":n},"aliases":aliases("solenoid",n),"availability":"unknown" if is_aux or n==15 else "used" if is_flip or n==23 else "unused","provenance":prov(CORE,*([MANUAL,SCRIPT] if is_flip or n==15 else []),status="observed" if is_aux or n==15 else "validated"),"physical":{"notes":note},"spatial":na("virtual" if is_aux or is_flip or n==23 or n==15 else "unused",CORE)}
            if n==23:
                item["id"]="virtual.game-on-enable";item["label"]="Game On / Switched Solenoid Enable";item["physical"]["notes"]="S11_GAMEONSOL=23 is the PIA0 CB2 switched-solenoid enable and drives the synthetic flipper states. SolRun enables gameplay and vpmNudge; no physical coil is fitted at this public address."
        outputs.append(item)
    lamp_drive_colors=["BRN","RED","ORG","BLK","GRN","BLU","VIO","GRY"]
    lamp_return_colors=["BRN","BLK","ORG","YEL","GRN","BLU","VIO","GRY"]
    for n in range(1,65):
        label=LAMP_LABELS[n-1];identifier="lamp."+slug(label);col,row=(n-1)//8,(n-1)%8
        note=f"Matrix: {lamps[n][1]}. Location list: {lamps[n][2]}. Both complete printed regions are retained in lamps.md. "
        if n==11:note+="The manual's VUK label denotes the left Shark Super Scoop indicator; the ROM calls it SHARK SUPER SCOOP and the script drives BulboF11. It is separate from lower Super VUK 46. "
        if n==12:note+="The table and physical photo place a red Tourist Season sign on the right ramp; the ROM calls it TOURIST SEASON. The manual's RIGHT RAMP ENTER names its shot, not a separate insert. "
        if n in (6,11,12,13,33,34,35):note+="FlashDL updates the modelled BulboF primitive; its coordinate uses exported world-space mesh bounds, never the corresponding Flasher sprite. "
        if n==25:note+="One public lamp drives two physical bulbs, one at each outlane. "
        if n in (33,34,35):note+="One of the tower's three #555 sockets, with teal green covers; the tower parts table specifies quantity three for this assembly. "
        if n in (12,33,34,35):note+=drawing_warning(n,comparison)
        if col==4:note+="The matrix and ROM print CN7-5; the lamp wiring schematic prints pin 6. This connector-only disagreement is preserved in the excerpt. "
        item={"id":identifier,"label":label,"kind":"lamp","binding":{"group":"pinmame.output.lamp","device":n},"aliases":aliases("lamp",n,str(n)),"availability":"used","physical":{"quantity":2 if n==25 else 1,"notes":note},"wiring":{"board":"CPU","driver_transistor":f"Q{71-col}","drive_wire":"YEL-"+lamp_drive_colors[col],"drive_connection":f"CN7-{[1,2,3,4,5,7,8,9][col]}","return_wire":"RED-"+lamp_return_colors[row],"return_connection":f"CN6-{[1,2,3,5,6,7,8,9][row]}","return_component":f"Q{72+row}"},"provenance":prov(MANUAL,SCRIPT,CORE)}
        if n in (7,8,64):item["spatial"]=na("cabinet_or_service",MANUAL)
        elif (s:=spatial(f"lamp.{n}",identifier,"emitter",places)):item["spatial"]=s
        if n in (12,33,34,35):
            item["provenance"]["source_refs"].append(DRAWING_COMPARISON)
            for placement in item["spatial"]["placements"]:
                placement["provenance"]["source_refs"].append(DRAWING_COMPARISON)
        outputs.append(item)

    sw={x["binding"]["device"]:x["id"] for x in inputs if x["binding"]["group"]=="pinmame.input.switch"}
    sol={x["binding"]["device"]:x["id"] for x in outputs if x["binding"]["group"]=="pinmame.output.solenoid"}
    mechanisms=[]
    def mech(key,label,kind,act,sensors,behavior,assembly=None):
        item={"id":"mech."+key,"label":label,"kind":kind,"actuators":[sol[n] for n in act],"sensors":[sw[n] for n in sensors],"behavior":behavior,"provenance":prov(MANUAL,SCRIPT,CORE)}
        if assembly:item["assembly_part_number"]=assembly
        mechanisms.append(item)
    mech("trough","Five-ball trough and two-stage serve","kicker",[1,2],[10,11,12,13,14,15],"Five balls occupy mechanical microswitch positions 10 (left) through 14 (right). Output 1 releases the lock-ball cam toward the opto-monitored up-kicker 15; output 2 lifts that ball to shooter lane 16. Output 3 then launches it onto the elevated shooter wire ramp. The script initializes bsTrough with switches 14,13,12,11,10 and five balls, then a separate bsTroughUp saucer at 15. TroughLock transfers one ball; bsTroughUpSolOut ejects the up-kicker. The 250ms table delay and kick strength are table tuning, not physical specifications.","500-5965-00-33")
    mech("auto-launch","Lower automatic launch","kicker",[3],[16,50],"The cabinet launch button 50 requests a shot. Output 3 fires Plunger1 at the lower-right shooter entrance (switch 16), feeding the elevated shooter wire ramp toward the top SPF lanes. This is independent of the upper mid-right kicker 4.","500-5969-00-33")
    mech("upper-launch","Upper ball launch / Kick Big","kicker",[4],[47],"Output 4 fires UpBLaunch at the mid-right side, with ball-presence rollover 47, sending a ball through the upper launch path. Both script plungers fire rearward along their own guides; do not treat output 4 as a second winding or direction of output 3.","500-5862-06-33")
    mech("upper-vuk","Rear upper VUK","kicker",[5],[44],"The saucer at rear-left switch 44 captures the ball; output 5 ejects it up to its wire return. bsUpVUK is distinct from both the under-apron Super VUK and the left Shark Super Scoop.","500-5839-01-33")
    mech("lower-vuk","Under-playfield return and lower Super VUK","kicker",[6],[55,46],"Balls entering the under-playfield ramp at 55 travel to the lower front-left Super VUK 46 under the arch. Output 6 ejects them back to play through the subway exit. The table uses a separate bsLowSVuk saucer at 46.","500-5880-00-33")
    mech("shark-scoop","Shark Super Scoop","kicker",[7],[56],"The left mid-playfield scoop 56 receives Shark shots and holds a ball until output 7 ejects it. bsSSScoop uses its own ball stack. It is not the lower under-arch VUK.","500-5953-00-33")
    mech("tower-trapdoor","Tower ramp lock trapdoor","diverter",[12],[25,26,55,46],"Completing the three-drop bank lights the lock trapdoor on the left metal ramp. Output 12 opens the physical door to divert a ball into the under-playfield ramp (55), which feeds lower VUK 46; with the door closed, the ramp continues toward exit 26. The tower's lamps 33/34/35 indicate collected locks; there are no three dedicated tower-ball sensors. The script opens Botola and swaps RampLG collision helpers while 12 is on.","500-5943-00-33")
    mech("upper-gate","Upper one-way control gate","gate",[9],[38,39,40],"Output 9 opens UpperGate; off returns it. The factory overview places this gate under the left ramp near the top rollovers. Rollover scoring switches are route sensors, not gate-limit feedback.","500-5968-00-33")
    mech("lower-gate","Lower one-way control gate","gate",[14],[47,54],"Output 14 opens LowerGate at the mid-right upper launch/Shark Fin route; off returns it. The manual puts the mini-coil under the butyrate. Switches 47 and 54 detect balls along the route, not a measured gate position.","500-5957-00-33")
    mech("shark-flips","Shark Flips automatic upper pair","other",[13],[54],"Rollover 54 lies before the upper-right Shark Fin. When Shark Flips is lit the ROM times output 13 to shoot toward the Shark Super Scoop. The manual's Shark Fin test and Adjustment 50 tune this timing. Q26 drives both upper flipper enables through isolation diodes; the script AutoFlipper rotates both upper bats. Each upper flipper also has its side's cabinet-button path, shown as N.O. on the SSFB schematic. No physical upper EOS switches are fitted.")
    mech("drops","Three-target drop bank","drop_target_bank",[16],[22,23,24],"Targets 22/23/24 latch down independently, ordered top/middle/bottom. Output 16 resets the whole bank through cdtBank.DropSol_On. Completing the bank lights a tower lock; release the three contacts when the physical bank rises.","500-5970-00-33")
    mech("bumpers","Three turbo bumpers","other",[17,18,19],[41,42,43],"Left, bottom and right switches 41/42/43 correspond to special-solenoid outputs 17/18/19. The script's Hit callbacks pulse the switches; PinMAME's DMD ROM drives the PIA special-solenoid lines. No alpha-game sequential-SP assumption is used.")
    mech("slings","Left and right slingshots","other",[20,21],[61,62],"Left 61 and right 62 trigger their respective kickers 20 and 21. The table's collision flippers are alternative simulation geometry; they are not additional physical flipper assemblies.","500-5849-00-33")
    mech("laser-kick","Left outlane Laser Kick","kicker",[22],[57],"When enabled by the ROM, left outlane switch 57 causes output 22 to kick the ball back up that lane. Completing the two stand-up targets 9/53 relights it. LaserKick.FireSpeed randomness in the table is tuning, not a measured factory value.","500-5838-01-33")
    mech("player-flippers","Cabinet-controlled flippers","other",[45,46,47,48],[82,84],"Two lower flippers and two upper flippers are fitted. Cabinet buttons 82/84 are copied to ROM matrix 64/63. PinMAME fabricates 45/46 and 47/48 together, so use one state per side and do not create independent power/hold actuators. The script's right callback moves RightFlipper and RightFlipper1, and its left callback moves LeftFlipper and LeftFlipper1. The physical upper pair also accepts CPU 13 through SSFB isolation diodes, represented by mech.shark-flips. The lower EOS power-cutoff contacts are board-local; no host-driven EOS input is exposed.")
    mech("knocker","Cabinet knocker","other",[8],[],"Output 8 pulses the cabinet-mounted 23-800 knocker. It has no ball-route sensor and no playfield placement.")
    mech("lighting-control","PPB bank selection and G.I. control","other",[10,11],[],"PPB K1 relay 10 selects alternate coil/flasher loads for drives 1-8 and 25-32. G.I. relay 11 independently switches the illumination supply; the table's inverted local lamp 200 animates these bulbs without adding another public output. Socket counts belong to the individual lighting circuits, not these relay mechanisms.")
    relationships=flipper_column_relationships(flip_swno=(63,64),matrix_ids={63:sw[63],64:sw[64]},refs=(CORE,))
    for n in range(25,33):relationships.append({"id":f"relationship.mux-{n}","kind":"relay_gated","source":sol[10],"destination":sol[n],"provenance":prov(MANUAL,CORE,SCRIPT)})
    for s,o in ((41,17),(42,18),(43,19),(61,20),(62,21)):
        relationships.append({"id":f"relationship.switch-{s}-coil-{o}","kind":"pulse","source":sw[s],"destination":sol[o],"provenance":prov(MANUAL,CORE,SCRIPT)})
    sources=build_sources(places)
    conflicts=[{
        "id":"conflict.flasher-bulb-composition",
        "path":"outputs[pinmame.output.solenoid:25|27|28|29|30|32]",
        "source_refs":[MANUAL,CORE],
        "description":"The production manual's complete driver chart (PDF 44 / printed 40) calls every flasher circuit Bulb #89. Its detailed eight-branch wiring drawing (PDF 88 / printed 84) instead specifies three #89 plus one #906 on 1R/3R/5R/6R/8R and two of each on 4R. The drawing retains older location wording, including a drop-target 1R lamp absent from the production location drawing and photographs, so its mixed bulb populations cannot silently override the production chart. Both sources agree on four sockets per circuit, and 2R/7R agree on all #89. The generic parts totals contain an inherited other-game footnote and do not settle per-circuit populations. Pinned PinMAME uniformly models 25-32 as #89 brightness, which is not physical fitment evidence. Resolution path: an owner or technician can supply socket-and-bulb close-ups, traced by harness to circuits 1R/3R/4R/5R/6R/8R on an unrestored production Baywatch, or a later production wiring revision can assign those exact socket populations. Wide playfield photos and ROM traces cannot identify every bulb base or settle this disagreement."
    }]
    for item in inputs+outputs:
        if item["binding"]["group"]=="pinmame.output.lamp" and item["binding"]["device"] in (6,12,13,33,34,35) or item["binding"]["group"]=="pinmame.output.solenoid" and item["binding"]["device"]==25 or item["binding"]["group"]=="pinmame.input.switch" and item["binding"]["device"]==54:
            item["provenance"]["source_refs"].append(PHOTOS)
            for placement in item.get("spatial",{}).get("placements",[]):
                placement["provenance"]["source_refs"].append(PHOTOS)
        if any(source["id"]==RUNTIME for source in sources) and (item["binding"]["group"]=="pinmame.output.solenoid" and item["binding"]["device"] in (*range(1,10),*range(11,23),*range(25,33)) or item["binding"]["group"]=="pinmame.output.lamp"):
            item["provenance"]["source_refs"].append(RUNTIME)
    return {"format":"pinmame-machine-definition","schema_version":2,
            "machine":{"id":KEY,"name":"Baywatch","manufacturer":"Sega","year":1995,"kind":"physical_pinball","model_number":"33","ipdb_id":2848,"opdb_id":"Grxvy-M4oZj","playfield":{"width":952,"height":2162,"units":"vpx","provenance":prov(TABLE,status="observed")}},
            "controller":{"platform":"pinmame.dataeast","hardware_generation":"0x8000","inversion_applied_by_emulator":True},
            "coverage":{"status":"partial","missing":MISSING+(["unresolved_conflicts"] if unresolved_conflicts({"conflicts":conflicts}) else []),"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"observed","physical_wiring":"observed","mechanisms":"validated","variant_coverage":"validated","recreation_knowledge":"validated","runtime_observation":"observed","causal_exercise":"observed","spatial_placement":"observed"}},
            "drivers":[{"id":n,"description":label,"year":year,"manufacturer":"Sega","flags":0,**({"clone_of":"baywatch"} if n!="baywatch" else {}),"physical_compatibility":"identical","variant_notes":"All eight drivers use init_baywatch / GEN_DEDMD64 / de_192x64DMD / FLIP6364 / SNDBRD_DE2S and the same physical I/O. Language, CPU/display firmware, and English sound-ROM population differ; later community firmware years do not create another physical machine."} for n,label,year in DRIVER_ROWS],
            "inputs":inputs,"outputs":outputs,"displays":[{"id":"display.main-dmd","label":"Backbox 192 x 64 DMD","kind":"dmd","controller_index":0,"width":192,"height":64,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service",CORE,MANUAL),"provenance":prov(CORE,MANUAL)}],"mechanisms":mechanisms,"relationships":relationships,"sources":sources,"conflicts":conflicts,"knowledge":{"path":KNOWLEDGE_PATH.relative_to(ROOT).as_posix(),"status":"complete"}}


def build_sources(places):
    manual_name="Baywatch_Manual.pdf"
    bulletin_name=next(n for n in MANUALS if "Bulletin" in n)
    base={"license":"NOASSERTION","rights":"NOASSERTION","attribution":"Sega Pinball, Inc.; hosted by IPDB"}
    sources=[
        {"id":PHOTOS,"kind":"human_review","uri":"internal:evidence/excerpts/sega.baywatch.1995/photo-receipts.md","sha256":sha(EXCERPTS/"photo-receipts.md"),"locator":"IPDB 2848 Mark Steinman photos 51946/51949 and Pinside Baywatch 550 gallery keys 35822/35797; direct resource URLs, hashes, timestamps and attribution in the receipt. External review-artifacts/sega.baywatch.1995/photos. Secondary physical/layout corroboration only; no coordinate or binding is derived from perspective photographs.","license":"NOASSERTION","rights":"Photographers retain copyright; images kept external","attribution":"Mark Steinman / IPDB; Pinside image contributors","excerpts":[checked_excerpt("physical-photos.md","four retained physical detail photographs, primary curator visually checked"),checked_excerpt("photo-receipts.md","selected acquisition records: exact resource and image-page URLs, SHA256, dimensions, timestamps and rights")]},
        {"id":CORE,"kind":"pinmame_core","uri":f"https://github.com/vpinball/pinmame/blob/{REV}/src/wpc/degames.c","revision":REV,"locator":"degames.c INITGAMES11/FLIP6364 and Baywatch block 1441-1530; s11.c setSSSol, updsol, pia2b_w, pia4a_r and s11_irqline; s11.h DE_COMPORTS2 and S11_PRINTERLINE; core.c core_updateSw/core_getSol; core.h public bands; gen.h GEN_DEDMD64. Retained source excerpt names every read path.","license":"BSD-3-Clause","attribution":"PinMAME contributors","excerpts":[checked_excerpt("controller.md","pinned sources, exact symbols and public arithmetic")]},
        {"id":"pinmame.baywatch.catalog","kind":"pinmame_catalog","uri":"https://github.com/vpinball/pinmame","revision":REV,"locator":"PinmameGetGames and degames.c baywatch root plus seven clones","license":"BSD-3-Clause","attribution":"PinMAME contributors"},
        {"id":MANUAL,"kind":"manual","uri":f"https://www.ipdb.org/files/2848/{manual_name}","original_filename":manual_name,"source_id":"IPDB 2848","sha256":MANUALS[manual_name],"acquired_at":"2026-10-21T20:56:23.794113Z","locator":"Verified IPDB machine https://www.ipdb.org/machine.cgi?id=2848; 132-page production scan; PDF 38-45 = printed 34-41, PDF 63-81 assemblies, PDF 86/88 cabinet contacts/detailed flasher wiring, PDF 109/111 upper SSFB/opto. External manuals/by-machine/sega.baywatch.1995.",**base,"excerpts":[checked_excerpt("switches.md","PDF 38-39, printed 34-35, complete switch matrix/parts list; PDF 111 opto theory"),checked_excerpt("lamps.md","PDF 40-41, printed 36-37, complete matrix/location list; PDF 91 lamp wiring"),checked_excerpt("coils.md","PDF 43-45, printed 39-41, complete coil and flipper tables; PDF 88 / printed 84 complete eight flasher branches"),checked_excerpt("mechanisms.md","PDF 10-11, 18-19, 37, 63, 70-77, 109, 111; routing, constructions and complete tower table")]+drawing_excerpts()},
        {"id":BULLETIN,"kind":"service_bulletin","uri":f"https://www.ipdb.org/files/2848/{bulletin_name}","original_filename":bulletin_name,"source_id":"IPDB 2848, Bulletin 74","sha256":MANUALS[bulletin_name],"acquired_at":"2026-10-21T20:56:23.215883Z","locator":"Both pages; April 28, 1995; retained under manuals/by-machine/sega.baywatch.1995; verified IPDB 2848 machine page",**base,"excerpts":[checked_excerpt("bulletin-74.md","pages 1-2, early latching green service-button modification")]},
        {"id":"manual.baywatch.sample","kind":"manual","uri":"https://www.ipdb.org/files/2848/Sega_1995_Baywatch_Sample_Game_Manual.pdf","original_filename":"Sega_1995_Baywatch_Sample_Game_Manual.pdf","source_id":"IPDB 2848","sha256":MANUALS["Sega_1995_Baywatch_Sample_Game_Manual.pdf"],"acquired_at":"2026-10-21T20:56:23.443317Z","locator":"19-page older sample-game excerpt, compared at PDF 13/15/17/18; production manual controls the curated physical revision. Verified machine https://www.ipdb.org/machine.cgi?id=2848",**base,"excerpts":[checked_excerpt("sample-manual.md","PDF 17 / printed 39 complete coil-location legend and drawing comparison")]},
        {"id":TABLE,"kind":"vpx_table","uri":"external:vpx-sources/sega/baywatch-1995/Baywatch%20%28Sega%29%201.0.5.vpx","sha256":places["table_sha256"],"known_working":True,"locator":"Kiwi 1.0.5; 952 x 2162 VPX units; cGameName baywatch; retained from authorized local table library","license":"NOASSERTION","rights":"NOASSERTION","attribution":"Kiwi; contributors credited in retained table","acquired_at":"2026-10-21T20:56:56.650Z"},
        {"id":SCRIPT,"kind":"vpx_script","uri":"external:vpx-sources/sega/baywatch-1995/extracted-vpxtool/script.vbs","sha256":places["script_sha256"],"known_working":True,"locator":"lines 125-241 init and ball stacks; 332-566 keys/switch handlers; 581-829 callbacks and causality; 881-1130 all lamp bindings","license":"NOASSERTION","rights":"NOASSERTION","attribution":"Kiwi; contributors credited in retained table","excerpts":[checked_excerpt("script-bindings.md","complete machine-specific I/O bindings and mechanism routines, summarized factually")]},
        {"id":EXTRACTION,"kind":"vpx_table","uri":"external:vpx-sources/sega/baywatch-1995/extracted-vpxtool/manifest.json","sha256":places["manifest_sha256"],"locator":"vpxtool git:v0.33.3; 1,638 payload files / 60,271,928 bytes; official build_external_evidence_manifest.py --game baywatch sorts all relative POSIX paths case-sensitively, records size/SHA256, canonical JSON plus LF; manifest files excluded from their own payload","license":"NOASSERTION","attribution":"Kiwi; extraction by project contributors"},
        {"id":GEOMETRY,"kind":"human_review","uri":"internal:tools/baywatch_places.json","sha256":sha(ROOT/"tools/baywatch_places.json"),"locator":"build_baywatch_places.py exact object selection, stored centres and exported world-mesh bounds; OBJ SHA256 "+places["obj_sha256"]+". One recreation lineage, all positions observed. Rejected helpers and exact omitted devices are listed.","license":"NOASSERTION","attribution":"Primary curator; Kiwi table geometry"},
        {"id":VPM_DE2_LIBRARY_SOURCE,"kind":"vpx_script","uri":VPM_DE2_LIBRARY_URI,"sha256":VPM_DE2_SHA256,"locator":"de2.vbs lines 21-36 and vpmKeyDown/vpmKeyUp; retained machine-neutral library loaded by LoadVPM at script line 125","license":"NOASSERTION","attribution":"VPinMAME script-library maintainers","excerpts":[checked_excerpt("controller.md","de2.vbs flipper and service constants and key handlers")]},
    ]
    sources.append({"id":DRAWING_COMPARISON,"kind":"human_review","uri":"internal:tools/baywatch_lamp_drawing.json","sha256":sha(ROOT/"tools/baywatch_lamp_drawing.json"),"locator":"Independent native PDF 41 / printed 37 symbol measurements, drawing frame and six floor controls; drawing_comparison() recomputes the normalized comparison without fitting controls. Elevated lamp 12/33/34/35 differences remain unreconciled. Exact extraction objects and script bindings were inspected; observed table positions are retained, not factory coordinates.","license":"NOASSERTION","attribution":"Curator; Sega drawing; Kiwi table geometry","excerpts":[checked_excerpt("lamp-drawing-comparison.md","PDF 41 / printed 37, measured frame, symbols, controls and exact table-object comparison")]})
    runtime=ROOT/"evidence/runtime/data-east/baywatch-usa-400-service-tests.json"
    if not runtime.is_file():raise ValueError("Baywatch reviewed runtime evidence is missing")
    sources.append({"id":RUNTIME,"kind":"runtime_scenario","uri":"internal:"+runtime.relative_to(ROOT).as_posix(),"sha256":sha(runtime),"revision":REV,"locator":"Fresh-state USA 4.00 switch/lamp/coil tests, printer and Shark Control probes, and successful serve/launch/eject/special-coil gameplay checkpoints; exact raw manifest/library/ROM/scenario hashes and visually read DMD frames. Failed explorations are retained separately and excluded from successful causal evidence.","license":"NOASSERTION","attribution":"Primary curator; user-authorized existing ROMs"})
    return sources


def verify_external():
    if manual_root:=os.environ.get("PINMAME_MANUALS_ROOT"):
        for filename,digest in MANUALS.items():
            path=Path(manual_root)/"by-machine"/KEY/filename
            if not path.is_file() or sha(path)!=digest:raise ValueError(f"Baywatch retained manual missing or changed: {path}")
    vpx_root=os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    review_root=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review_root:
        from build_baywatch_runtime import build as build_runtime

        review=Path(review_root)
        places=load_json(ROOT/"tools/baywatch_places.json")
        obj=review/KEY/"world-obj/Baywatch (Sega) 1.0.5.obj"
        if not obj.is_file() or sha(obj)!=places["obj_sha256"]:
            raise ValueError(f"Baywatch retained OBJ missing or changed: {obj}")
        runtime=load_json(ROOT/"evidence/runtime/data-east/baywatch-usa-400-service-tests.json")
        if build_runtime(review)!=runtime:
            raise ValueError("Baywatch runtime evidence differs from the retained runs")
        if vpx_root:
            from build_baywatch_places import build as build_places

            # This builder verifies the VPX/script identities and extraction manifest itself.
            if build_places(Path(vpx_root),obj)!=places:
                raise ValueError("Baywatch placements differ from the retained extraction and OBJ")
    elif vpx_root:
        from build_external_evidence_manifest import check_manifest
        from build_baywatch_places import MANIFEST_SHA,TABLE_SHA,SCRIPT_SHA
        base=Path(vpx_root)/"sega/baywatch-1995"
        if sha(base/"Baywatch (Sega) 1.0.5.vpx")!=TABLE_SHA or sha(base/"extracted-vpxtool/script.vbs")!=SCRIPT_SHA or check_manifest(base/"extracted-vpxtool","baywatch")!=MANIFEST_SHA:raise ValueError("Baywatch external source identity mismatch")


def artifacts():
    definition=build();places=load_json(ROOT/"tools/baywatch_places.json")
    count=sum(len(d.get("spatial",{}).get("placements",[])) for group in ("inputs","outputs") for d in definition[group])
    absent=[d["id"] for group in ("inputs","outputs") for d in definition[group] if d.get("availability") in ("used","unknown") and "spatial" not in d]
    report={"format":"pinmame-spatial-blockers","version":1,"machine_id":KEY,"status":"partial","coordinate_convention":"x=0 left, x=1 right; y=0 rear, y=1 apron; x=raw_x/952, y=raw_y/2162. Six decimal places preserve deterministic table precision, not survey accuracy.","placement_count":count,"source":{"table_sha256":places["table_sha256"],"extraction_manifest_sha256":places["manifest_sha256"],"obj_sha256":places["obj_sha256"]},"placements":places["placements"],"omitted_spatial_key_devices":absent,"blockers":[{"id":"single-recreation-lineage","severity":"major","detail":"All coordinates are observed from Kiwi 1.0.5. The pinned LW/nFozzy scripts descend from the same Kiwi table and are not independent geometry. Factory drawings and photos corroborate selected identities, quantities and sides. The measured lamp 12/33/34/35 drawing/table discrepancy remains unreconciled; no complete independent per-device placement validation is asserted."},{"id":"missing-socket-and-trough-geometry","severity":"major","detail":places["omitted"]},{"id":"gi-socket-survey","severity":"major","detail":"The table supplies 35 admitted playfield GI bulb objects after render doubles are removed, but the factory schematic shows two feeds without a complete socket-to-feed inventory. No exact physical GI total is asserted; backbox/cabinet quantities and all physical sockets still require reconciliation."}],"projection_notes":{"solenoid.16":"Reset-coil coordinate projected onto the middle drop target; not a surveyed coil position.","switch.15":"BallRelease is the trough up-kicker's own ball sensor anchor.","solenoid.12":"Botola is the physical trapdoor pivot, not the collidable RampLG helpers."},"rejected":places["rejected"],"lower_flipper_geometry":{"note":"Virtual outputs 45-48 have no physical CPU device placement. Actual lower flippers are modelled by LeftFlipper/RightFlipper; their geometry and the cabinet-controlled upper pair remain table-owned, with the mechanism contract in the definition."}}
    report["mechanical_anchors"]=places["mechanical_anchors"]
    report["drawing_table_comparison"]=drawing_comparison(places)
    report["source"]["drawing_measurements_sha256"]=sha(ROOT/"tools/baywatch_lamp_drawing.json")
    report["blockers"].append({"id":"elevated-lamp-drawing-table-difference","severity":"major","detail":"Lamp 12 and tower lamps 33/34/35 differ materially between the measured factory drawing symbols and the script-linked table mesh centres. The drawing shows the tower group farther forward, and 12 farther left and forward. Six floor controls align much more closely, but elevated projection and symbol-to-emitter offsets are unquantified. No alternate physical emitter bound to these addresses was found near the drawing locations. Keep current positions observed; reconcile the source roles before spatial validation. This is a placement limitation, not a machine-design conflict.","source_refs":[MANUAL,TABLE,SCRIPT,GEOMETRY,DRAWING_COMPARISON]})
    knowledge=(ROOT/"tools/baywatch_knowledge.md").read_bytes()
    return [(DEFINITION_PATH,canonical_bytes(definition)),(SEED_PATH,canonical_bytes(definition)),(KNOWLEDGE_PATH,knowledge),(SPATIAL_REPORT_PATH,canonical_bytes(report))]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check",action="store_true");modes.add_argument("--regenerate",action="store_true")
    parser.add_argument("--repository-root",type=Path,default=ROOT)
    args=parser.parse_args();root=args.repository_root.resolve()
    verify_external()
    existing=root/f"machines/author-ready/sega/{SLUG}.json"
    if existing.exists():raise ValueError(f"refusing to overwrite an existing author-ready Baywatch artifact: {existing}")
    for path,payload in artifacts():
        target=root/path.relative_to(ROOT)
        if args.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n",b"\n")!=payload.replace(b"\r\n",b"\n"):raise ValueError(f"Baywatch artifact missing or drifted: {target}")
        else:write_bytes(target,payload)
    print("Baywatch definition, seed, knowledge and spatial report match the curator." if args.check else "Regenerated Baywatch definition, seed, knowledge and spatial report.")


if __name__=="__main__":main()
