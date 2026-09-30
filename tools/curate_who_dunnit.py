"""Build the evidence-limited Bally WHO dunnit (1995) definition.

The reviewed factory table transcriptions and the pinned coordinate register are
repository inputs. Generation never reads an external manual or VPX. In evidence
mode, --check independently re-hashes both originals and every extracted file,
and compares every registered object centre with its retained VPX JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text

ROOT = Path(__file__).resolve().parents[1]
MID = "bally.who-dunnit.1995"
PARTIAL = ROOT / "machines/partial/bally/who-dunnit-1995.json"
READY = ROOT / "machines/author-ready/bally/who-dunnit-1995.json"
SEED = ROOT / "tools/seeds/bally/who-dunnit-1995.json"
SPATIAL_SEED = ROOT / "tools/seeds/bally/who-dunnit-1995-spatial.json"
GI_SEED = ROOT / "tools/seeds/bally/who-dunnit-1995-gi-candidates.json"
REPORT = ROOT / "reports/spatial/bally/who-dunnit-1995.json"
REPORT_MD = ROOT / "reports/spatial/bally/who-dunnit-1995.md"
EXCERPTS = ROOT / f"evidence/excerpts/{MID}"
PIN = "8371478a7640f1896dcdf565aed340dc5df989ba"
MANUAL_SHA = "5fa08344d905c9730c86c6baee79b43e6a4a1c4e2230f67a08c2973b57bc714e"
TABLE_SHA = "a0f18c07f98ec7dce96cc030eb11af11a0c28d0d1cffb5390744067b9221e2a9"
SCRIPT_SHA = "034fe6483660fbc9516aa15a4727d8dc6da0cfb3db0321b0c1357523967ccd44"
MANIFEST_SHA = "0fd20d012d8219583a8222b51a0997ca4876247cc9ec19352e5a06d270d3643c"
FILE_COUNT = 631
TOTAL_BYTES = 65628606
RUNTIME_SHA = "cffa9ec8485779cc947bdcd4631d3f760654134f8749b7417aaec1d918d7b4cd"
SCENARIO_SHA = "c45e182eb928b95ea1ec85bcf784b43efc8cff09eee936e2eb6ce530df7d01d4"
MANUAL_NAME = "Bally_1995_WHO_dunnit_English_Manual_WPC_Schematic_Manual_January_1995_Rev_Level_3_OCR_searchable.pdf"
TABLE_NAME = "Who Dunnit (Bally 1995).vpx"
MANUAL_SRC = "manual.bally.who-dunnit.1995.ipdb-3685"
ASSEMBLY_SRC = "manual.bally.who-dunnit.1995.jet-assembly"
SCRIPT_SRC = "vpx-script.who-dunnit-ninuzzu-2018"
TABLE_SRC = "vpx-table.who-dunnit-ninuzzu-2018"
EXTRACTION_SRC = "vpx-extraction.who-dunnit-ninuzzu-2018"
CORE_SRC = f"pinmame.core.{PIN[:12]}"
CATALOG_SRC = f"pinmame.catalog.{PIN[:12]}"
PROFILE_SRC = "controller-profile.pinmame-wpc-95"
RUNTIME_SRC = "runtime.who-dunnit.switch-edges.wd-12"
SOL_RUNTIME = {
    "bank": ("02-three-bank-cycle", "8fb4eae8b0e4f1e1a48024997615001fd7b06e808e135c586a0abf62f0b96067", "c4fd871c2a7227618081fc3360cb1ea18c0ddcc448820a06f2a3fe1c7b291547", "013-start-selected-3-bank-cycle-display-0.pgm", "cb544d5a0b29fc9fc6000f67ff265f59c553fdae5edcd0c8713af0b7cd07ffec", "ROM T.16 3-Bank Test: direct Enter starts output 22, next Enter stops it; DMD says TEST-BANK UP/RUNNING."),
    "ramp-up": ("03-ramp", "b9eaccc180b1ccf1a02f4993dbf4f0610158ec32a890197cd7ffeeb345d6ee6d", "3a83c3d4f8ef3751b37fc0472b189fb74369ee7d5a0fa7025552a37395ff5446", "012-start-selected-ramp-action-display-0.pgm", "7febe28c13c5544a0ca79b7ce6ee39e71c0daf2a1c13942dc88ec03f3f8f786e", "ROM T.17 Ramp Test: RAMP UP selection produces output 16 pulses without built-in mechanics."),
    "ramp-down": ("06-ramp-down", "a0af5d90f2704d264804a065df3ecdae14f03a7fa5a398639d57b938daa1dbae", "124f5817e9b076348e47e2afde9c68128b52fe5736c56d787514dad95ef354b3", "013-start-selected-ramp-down-action-display-0.pgm", "e3909f173a44142880c54c367c9129453a0f72232cf00092aea5dd9502bcfafa", "ROM T.17 Ramp Test: RAMP DOWN selection produces output 5 pulses without built-in mechanics."),
    "reels": ("05-reel-selections", "39e8be5070c2baed3a381d9527495585c57c4550b2eec91a0332e82b75705224", "f6095f9dd9621d88b4f22d9e8f3ac3458ec75a836416c46b7a7ce1baa90b297b", "013-reel-select-up-3-display-0.pgm", "3b8f5a2ea4ad0dfc9992652d1e1296ca4a21ba9c8e88e58b6792cb2c41d1a8de", "ROM T.18 Reel Test: direct service Up selects left, center, right in order and activates public output pairs 23/24, 25/26, 27/28. Without host mechanics, prior hold phases can remain high."),
    "optos": ("07-opto-edges", "d5a0a0957426d09f08897d66f41cb6ab371119115c222fafa5692ace20092962", "5574f6c6635b0521843f337fb003f2f13c3ba9f1974bb857be30faf9cf84cbba", "019-opto-47-raw-1-display-0.pgm", "8c09f26108b48e4e520c5acf6f521947b07e98ed6b1f239a343e919033d02590", "ROM T.1 Switch Edges: direct raw 1 displays manual optos 12, 25, 48, 31, 41, 47; raw 0 clears each. Physical beam state remains unproven."),
}
OPTO_FRAMES = {
    12:("009-opto-12-raw-1-display-0.pgm","d76b83f0dcc60eb93b255cedc6be501d1d3f5b4de277e4b07268a0a0c9cc463a"),
    25:("011-opto-25-raw-1-display-0.pgm","4151c5cd8449eecc5cb91f835aa23aaf7a5238cfd4c12ad3f6b62118dde9c916"),
    48:("013-opto-48-raw-1-display-0.pgm","c5d37fc9044230c3c15029de508a53e29901ef3909f3ba5c707a93c19834a8fc"),
    31:("015-opto-31-raw-1-display-0.pgm","c4b7a59d08a67b70f257b515a32b5874c33dd16cdf9f2b3b656be99e2a7b53f1"),
    41:("017-opto-41-raw-1-display-0.pgm","b668e465f73fcdb64a2b6dad6f436a4fae41f6f3c7804c71e3b67dd4b566b8b5"),
    47:("019-opto-47-raw-1-display-0.pgm","8c09f26108b48e4e520c5acf6f521947b07e98ed6b1f239a343e919033d02590"),
}
OPTO = {12, 25, *range(31, 38), *range(41, 45), 47, 48}
UNUSED_SWITCH = {38, 45, 46, *range(81, 89)}
CABINET_MATRIX = {13, 14, 21, 22, 23, 24}
SWITCH_COLUMN = (("Green-Brown", "J207-1", "U20-18"), ("Green-Red", "J207-2", "U20-17"),
                 ("Green-Orange", "J207-3", "U20-16"), ("Green-Yellow", "J207-4", "U20-15"),
                 ("Green-Black", "J207-5", "U20-14"), ("Green-Blue", "J207-6", "U20-13"),
                 ("Green-Violet", "J207-7", "U20-12"), ("Green-Gray", "J207-9", "U20-11"))
SWITCH_ROW = (("White-Brown", "J209-1", "U18-11"), ("White-Red", "J209-2", "U18-9"),
              ("White-Orange", "J209-3", "U18-5"), ("White-Yellow", "J209-4", "U18-7"),
              ("White-Green", "J209-5", "U19-11"), ("White-Blue", "J209-7", "U19-9"),
              ("White-Violet", "J209-8", "U19-5"), ("White-Gray", "J209-9", "U19-7"))
LAMP_COLUMN = (("Yellow-Brown","J137-1","Q98"),("Yellow-Red","J137-2","Q97"),
               ("Yellow-Orange","J137-3","Q96"),("Yellow-Black","J137-4","Q95"),
               ("Yellow-Green","J137-5","Q94"),("Yellow-Blue","J137-6","Q93"),
               ("Yellow-Violet","J138-7","Q92"),("Yellow-Gray","J138-9","Q91"))
LAMP_ROW = (("Red-Brown","J133-1","Q90"),("Red-Black","J133-2","Q89"),
            ("Red-Orange","J133-4","Q88"),("Red-Yellow","J133-5","Q87"),
            ("Red-Green","J133-6","Q86"),("Red-Blue","J133-7","Q85"),
            ("Red-Violet","J133-8","Q84"),("Red-Gray","J133-9","Q83"))
DEDICATED = ("Left Coin Chute", "Center Coin Chute", "Right Coin Chute", "4th Coin Chute",
             "Service Credits / Escape", "Volume Down / Down", "Volume Up / Up", "Begin Test / Enter")
FLIPTRONIC = ("Lower Right Flipper EOS", "Lower Right Flipper Cabinet Opto",
              "Lower Left Flipper EOS", "Lower Left Flipper Cabinet Opto", "Spinner",
              "Upper Right Flipper Opto — Not Used", "Upper Left Flipper EOS — Not Used",
              "Upper Left Flipper Opto — Not Used")
SOLENOIDS = {
    1:("Trough", "coil"), 2:("Plunger", "coil"), 3:("Left Lock Up", "coil"),
    4:("Right Back Popper", "coil"), 5:("Ramp Down", "coil"), 6:("Not Used", "virtual"),
    7:("Knocker", "coil"), 8:("Right Front Popper", "coil"),
    9:("Left Sling", "coil"), 10:("Right Sling", "coil"),
    11:("Left Jet", "coil"), 12:("Bottom Jet", "coil"), 13:("Right Jet", "coil"),
    14:("Phone Flasher", "flasher"), 15:("Not Used", "virtual"), 16:("Ramp Up", "coil"),
    17:("Back Flasher", "flasher"), 18:("Autofire Flasher", "flasher"),
    19:("Lower Left Flasher", "flasher"), 20:("Spinner Flasher", "flasher"),
    21:("Lower Right Flasher", "flasher"), 22:("Motor 3-Bank", "motor"),
    23:("Left Slot B", "motor"), 24:("Left Slot A", "motor"),
    25:("Center Slot B", "motor"), 26:("Center Slot A", "motor"),
    27:("Right Slot B", "motor"), 28:("Right Slot A", "motor"),
    29:("WPC J111 State 1", "virtual"), 30:("WPC J111 State 2", "virtual"),
    31:("WPC Game-On State", "virtual"), 32:("WPC Constant-Zero State", "virtual"),
    33:("Upper Right Flipper Power — Not Fitted", "virtual"),
    34:("Upper Right Flipper Hold — Not Fitted", "virtual"),
    35:("Upper Left Flipper Power — Not Fitted", "virtual"),
    36:("Up Down Post", "coil"),
    45:("Lower Right Flipper Power", "coil"), 46:("Lower Right Flipper Hold", "coil"),
    47:("Lower Left Flipper Power", "coil"), 48:("Lower Left Flipper Hold", "coil"),
    49:("PinMAME Simulator Ball Shooter", "virtual"), 50:("Reserved", "virtual"),
}
FLASHER_QTY = {14:(1,0), 17:(2,1), 18:(1,0), 19:(1,1), 20:(1,2), 21:(1,1)}
DRIVERS = ("wd_03r", "wd_048r", "wd_10f", "wd_10g", "wd_10r", "wd_11", "wd_12", "wd_12g", "wd_12gp", "wd_12p")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table_labels(path: Path) -> dict[int, str]:
    result: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().split("|")[1:-1]]
        if len(cells) != 8 or not re.fullmatch(r"\d{2}(?: O)?", cells[0]):
            continue
        for index in range(0, 8, 2):
            address = int(cells[index].split()[0])
            if address in result:
                raise ValueError(f"duplicate printed address {address} in {path}")
            result[address] = cells[index + 1]
    if len(result) != 64:
        raise ValueError(f"expected 64 full matrix cells in {path}; found {len(result)}")
    return result


def solenoid_table() -> dict[int,list[str]]:
    result={}
    for line in (EXCERPTS/"solenoid-flasher.md").read_text(encoding="utf-8").splitlines():
        cells=[cell.strip() for cell in line.strip().split("|")[1:-1]]
        if len(cells)==8 and re.fullmatch(r"\d{2}",cells[0]):
            address=int(cells[0]);result[address]=cells
    if set(result)!=(set(range(1,29))|{36}):
        raise ValueError("incomplete printed WHO dunnit solenoid table")
    return result


def lamp_parts() -> dict[int,tuple[str,str]]:
    result={}
    for line in (EXCERPTS/"lamp-matrix.md").read_text(encoding="utf-8").splitlines():
        cells=[cell.strip() for cell in line.strip().split("|")[1:-1]]
        if len(cells)!=3 or not re.fullmatch(r"24-\d+",cells[1]):
            continue
        for token in cells[0].split(","):
            match=re.fullmatch(r"\s*(\d{2})(?:–(\d{2}))?\s*",token)
            if not match:raise ValueError(f"invalid lamp address range {token}")
            for address in range(int(match[1]),int(match[2] or match[1])+1):
                if address in result:raise ValueError(f"duplicate lamp assembly for {address}")
                result[address]=(cells[1],cells[2])
    if set(result)!={c*10+r for c in range(1,9) for r in range(1,9)}-{85,86,87,88}:
        raise ValueError("incomplete printed lamp part table")
    return result


def spatial_candidates() -> dict[tuple[str, int], list[dict[str, Any]]]:
    seed = load_json(SPATIAL_SEED)
    if seed["table_sha256"] != TABLE_SHA or seed["script_sha256"] != SCRIPT_SHA or seed["bounds"] != {"left":0,"top":0,"right":953,"bottom":2128}:
        raise ValueError("WHO dunnit spatial seed identity or bounds changed")
    result: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in seed["candidates"]:
        if not (0 <= item["x"] <= 1 and 0 <= item["y"] <= 1):
            raise ValueError(f"candidate outside playfield: {item}")
        result.setdefault((item["role"], item["address"]), []).append(item)
    return result


def gi_candidates() -> dict[int,list[dict[str,Any]]]:
    seed=load_json(GI_SEED)
    if seed["machine_id"]!=MID or seed["table_sha256"]!=TABLE_SHA:
        raise ValueError("WHO dunnit G.I. candidate register identity changed")
    result:dict[int,list[dict[str,Any]]]={}
    for item in seed["candidates"]:
        result.setdefault(item["address"],[]).append(item)
    if {key:len(value) for key,value in result.items()}!={0:11,1:10,2:28}:
        raise ValueError("WHO dunnit G.I. candidate collection changed")
    return result


def prov(*refs: str, status: str = "validated") -> dict[str, Any]:
    return {"status":status,"source_refs":list(refs)}


def na(reason: str, *refs: str) -> dict[str, Any]:
    return {"status":"not_applicable","reason":reason,"provenance":prov(*refs)}


def candidate_spatial(role: str, address: int, candidates: dict[tuple[str,int],list[dict[str,Any]]], *refs: str) -> dict[str, Any] | None:
    entries = candidates.get((role,address), [])
    if role=="lamp":
        # The retained script's L16/L17/L18 arrays also contain glow helpers.
        # A single printed bumper bulb must never acquire four socket placements.
        entries=[item for item in entries if item["object"].lower()==f"l{address}"]
    if not entries:
        return None
    placements = []
    for index,item in enumerate(entries,1):
        placements.append({"id":f"{role}.{address}.candidate-{index}","role":"sensor" if role == "switch" else "emitter",
                           "space":"playfield","x":item["x"],"y":item["y"],
                           "provenance":prov(*refs,status="candidate")})
    return {"status":"candidate","placements":placements}


def source_records() -> list[dict[str, Any]]:
    excerpt_info = (("switch-matrix", "PDF pages 126–127; printed 2-44–2-45"),
                    ("lamp-matrix", "PDF pages 124–125; printed 2-42–2-43"),
                    ("solenoid-flasher", "PDF pages 103, 128–129; jet assembly and printed 2-46–2-47"),
                    ("service-mechanisms", "PDF pages 2, 4, 45–46, 109; DIP chart, Security-board notice, T.16–T.18, reel assembly"))
    excerpts = [{"id":f"excerpt.who-dunnit.{name}","locator":locator,
                 "path":f"evidence/excerpts/{MID}/{name}.md","sha256":sha(EXCERPTS/f"{name}.md"),
                 "method":"mixed","transcribed_by":"primary curator; OCR checked against rendered source pages",
                 "reviewed":True} for name,locator in excerpt_info]
    return [
        {"id":CATALOG_SRC,"kind":"pinmame_catalog","uri":"https://github.com/vpinball/pinmame","revision":PIN,
         "locator":"PinmameGetGames wd_12 clone tree: ten wd_* driver records", "license":"BSD-3-Clause","attribution":"PinMAME contributors"},
        {"id":CORE_SRC,"kind":"pinmame_core","uri":"https://github.com/vpinball/pinmame","revision":PIN,
         "locator":"src/wpc/sims/wpc/prelim/wd.c lines 96–128 and 327–383: wdGameData GEN_WPC95DCS, inverted-switch mask and mechanical simulator; src/wpc/core.c core_getSol; src/wpc/wpc.c WPC row/flipper reads",
         "sha256":"ef33ac1bdae145166c00d4dadcb95e5b10f883cc88da01c7577b5ee09775f6e1","license":"BSD-3-Clause","attribution":"PinMAME contributors"},
        {"id":PROFILE_SRC,"kind":"human_review","uri":"internal:controllers/pinmame/wpc-95.json","revision":"repository",
         "locator":"Public switch, solenoid, lamp and G.I. transport rules for GEN_WPC95DCS", "license":"BSD-3-Clause","attribution":"PinMAME game definitions contributors"},
        {"id":MANUAL_SRC,"kind":"manual","uri":f"external:pinmame-manuals/by-machine/{MID}/ipdb-3685/{MANUAL_NAME}",
         "original_filename":MANUAL_NAME,"sha256":MANUAL_SHA,"acquired_at":"2026-09-30T07:48:09.694866Z",
         "locator":"188-page Bally WHO dunnit manual, model 50044, January 1995 Rev. Level 3; IPDB machine 3685 https://www.ipdb.org/machine.cgi?id=3685; direct resource https://www.ipdb.org/files/3685/"+MANUAL_NAME+"; PDF page 4 Security CPU notice; printed 2-42 to 2-47 machine tables",
         "license":"NOASSERTION","rights":"NOASSERTION","attribution":"Bally/Midway; scan hosted by the Internet Pinball Machine Database","excerpts":excerpts},
        {"id":ASSEMBLY_SRC,"kind":"manual","uri":f"external:pinmame-manuals/by-machine/{MID}/ipdb-3685/{MANUAL_NAME}",
         "original_filename":MANUAL_NAME,"sha256":MANUAL_SHA,"locator":"PDF page 103, printed 2-21 A-9415-2 Jet Bumper Coil Assembly item 7; PDF page 128, printed 2-46 solenoid locations item 13. Both print AE-26-1200, unlike the drive table on 2-46.",
         "license":"NOASSERTION","rights":"NOASSERTION","attribution":"Bally/Midway; scan hosted by the Internet Pinball Machine Database"},
        {"id":TABLE_SRC,"kind":"vpx_table","uri":f"external:pinmame-vpx-sources/bally/who-dunnit-1995/{TABLE_NAME}",
         "sha256":TABLE_SHA,"acquired_at":"2026-09-30T07:46:35Z", "locator":"ninuzzu/DJRobX VPX 1.0, January 2018, metadata manufacturer Bally year 1995; 953 by 2128 VPX bounds",
         "license":"NOASSERTION","attribution":"ninuzzu and DJRobX"},
        {"id":SCRIPT_SRC,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/bally/who-dunnit-1995/extracted/script.vbs",
         "sha256":SCRIPT_SHA,"acquired_at":"2026-09-30T07:46:35Z", "locator":"Retained table script lines 25 (wd_12), 175–273 (G.I./lamp/solenoid bindings), 327–480 (bank/ramp/reels); vpxtool git:v0.33.3",
         "license":"NOASSERTION","attribution":"ninuzzu and DJRobX","known_working":True},
        {"id":EXTRACTION_SRC,"kind":"vpx_table","uri":"external:pinmame-vpx-sources/bally/who-dunnit-1995/extracted.manifest.json",
         "sha256":MANIFEST_SHA,"acquired_at":"2026-09-30T07:52:35Z","locator":"Complete 631-file, 65,628,606-byte sorted POSIX-path/size/SHA-256 manifest; vpxtool git:v0.33.3",
         "license":"NOASSERTION","attribution":"ninuzzu and DJRobX"},
        {"id":RUNTIME_SRC,"kind":"runtime_scenario","uri":"external:review-artifacts/bally.who-dunnit.1995/session-20260930/terra-runtime/traces/06-switch-edges-115-112-114.json",
         "sha256":RUNTIME_SHA,
         "locator":"Fresh wd_12 ROM service T.1 Switch Edges, direct public 115/112/114 raw states 1 then 0, keyboard and built-in mechanics disabled; DMD 010–015 and public output transitions 45–48. Scenario SHA-256 c45e182eb928b95ea1ec85bcf784b43efc8cff09eee936e2eb6ce530df7d01d4; library SHA-256 ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d; wd_12.zip SHA-256 b17b927170f59b6daf9664260a15aaa55d8cf88dff05413a625510c11b972197",
         "license":"NOASSERTION","attribution":"PinMAME game definitions contributors"},
    ] + [
        {"id":f"runtime.who-dunnit.{key}.wd-12","kind":"runtime_scenario",
         "uri":f"external:review-artifacts/{MID}/session-20260930/sol-runtime/traces/{name}.json",
         "sha256":trace_sha,"locator":f"{description} Scenario SHA-256 {scenario_sha}; DMD {frame} SHA-256 {frame_sha}; pinned wd_12 ROM and library as in {RUNTIME_SRC}.",
         "license":"NOASSERTION","attribution":"PinMAME game definitions contributors"}
        for key,(name,trace_sha,scenario_sha,frame,frame_sha,description) in SOL_RUNTIME.items()
    ]


def inputs(candidates: dict[tuple[str,int],list[dict[str,Any]]]) -> list[dict[str, Any]]:
    labels = table_labels(EXCERPTS/"switch-matrix.md")
    if {a for a,n in labels.items() if n == "NOT USED"} != UNUSED_SWITCH:
        raise ValueError("printed unused-switch set changed")
    result = []
    for address,label in enumerate(DEDICATED,1):
        result.append({"id":f"switch.dedicated-{address}","label":label,"kind":"switch",
                       "binding":{"group":"pinmame.input.switch","device":address},
                       "aliases":[{"namespace":"pinmame.switch","value":str(address)},{"namespace":"manual.address","value":f"D{address}"}],
                       "availability":"optional" if address == 4 else "used", "normally_closed":False,
                       "physical":{"location":"coin door","switch_type":"button"},
                       "spatial":na("cabinet_or_service",MANUAL_SRC),"provenance":prov(MANUAL_SRC,CORE_SRC)})
    for address,label in sorted(labels.items()):
        col,row=divmod(address,10)
        drive,drive_conn,drive_chip=SWITCH_COLUMN[col-1]
        ret,ret_conn,ret_chip=SWITCH_ROW[row-1]
        unused=address in UNUSED_SWITCH
        cabinet=address in CABINET_MATRIX
        physical: dict[str,Any]={"switch_type":"opto" if address in OPTO else "unknown"}
        if cabinet: physical["location"]="cabinet or coin door"
        if address == 24: physical["notes"]="Manual prints Always Closed; physical matrix continuity link. The retained script writes Controller.Switch(24)=0 beside an 'always closed' comment; that table write is not a physical construction claim."
        if address in OPTO:
            physical["notes"]=("Printed shaded opto cell. " if address in (set(range(31,38))|set(range(41,45))) else
                               "Unshaded matrix cell but the locations list prints an opto assembly. ")+"CPU row path and wdGameData mask normalize this address."
        item={"id":f"switch.matrix-{address}","label":label.title() if not unused else "Not Used",
              "kind":"constant" if address==24 else "switch","binding":{"group":"pinmame.input.switch","device":address},
              "aliases":[{"namespace":"pinmame.switch","value":str(address)}],
              "availability":"unused" if unused else "used","normally_closed":address in OPTO or address==24,
              "physical":physical,
              "wiring":{"board":"WPC Security CPU board (manual)","drive_wire":drive,"drive_connection":drive_conn,
                        "return_wire":ret,"return_connection":ret_conn,
                        "return_component":f"column {drive_chip}; row {ret_chip}"},
              "provenance":prov(MANUAL_SRC,CORE_SRC,PROFILE_SRC)}
        if address in {12,25,31,41,47,48}:
            item["provenance"]=prov(MANUAL_SRC,CORE_SRC,PROFILE_SRC,"runtime.who-dunnit.optos.wd-12")
        if address==24:item["constant_active"]=True
        if unused:item["spatial"]=na("unused",MANUAL_SRC)
        elif cabinet:item["spatial"]=na("cabinet_or_service",MANUAL_SRC)
        elif address==24:item["spatial"]=na("constant",MANUAL_SRC)
        elif (sp:=candidate_spatial("switch",address,candidates,TABLE_SRC,SCRIPT_SRC,MANUAL_SRC)):
            item["spatial"]=sp
        result.append(item)
    for offset,label in enumerate(FLIPTRONIC):
        address=111+offset
        unused=offset>=5
        item={"id":f"switch.fliptronic-{address}","label":label,"kind":"switch",
              "binding":{"group":"pinmame.input.switch","device":address},
              "aliases":[{"namespace":"pinmame.switch","value":str(address)},
                         {"namespace":"manual.address","value":f"F{offset+1}"}],
              "availability":"unused" if unused else "used", "physical":{"switch_type":"opto" if offset in (1,3) else "unknown"},
              "provenance":prov(MANUAL_SRC,CORE_SRC,PROFILE_SRC,RUNTIME_SRC,status="candidate" if offset in (0,2) else "validated")}
        if unused:item["spatial"]=na("unused",MANUAL_SRC)
        elif offset in (1,3):item["spatial"]=na("cabinet_or_service",MANUAL_SRC)
        elif offset in (0,2):item["spatial"]=na("internal_nonvisual",MANUAL_SRC)
        # F5 is a playfield spinner, distinct from this profile's generic F5 EOS label.
        elif offset==4:
            item["spatial"]=candidate_spatial("switch",address,candidates,TABLE_SRC,SCRIPT_SRC,MANUAL_SRC,RUNTIME_SRC)
        result.append(item)
    chart="America Off/Off/On/On/On/On/On/On; European Off/Off/On/On/On/Off/On/On; French Off/Off/On/On/On/On/Off/Off; German Off/Off/On/On/On/On/On/Off; Spain Off/Off/On/On/Off/On/On/On"
    for address in range(1,9):
        result.append({"id":f"switch.dip-{address}","label":f"CPU DIP SW{address} (country configuration bit)",
                       "kind":"dip_switch","binding":{"group":"pinmame.input.dip","device":address},
                       "aliases":[{"namespace":"pinmame.dip","value":str(address)},
                                  {"namespace":"manual.address","value":f"SW{address}"}],
                       "availability":"used","physical":{"location":"Security CPU board","switch_type":"dip",
                       "notes":f"Front manual DIP Switch Chart: {chart}."},
                       "spatial":na("dip_switch",MANUAL_SRC),"provenance":prov(MANUAL_SRC,CORE_SRC,PROFILE_SRC)})
    return result


def outputs(candidates: dict[tuple[str,int],list[dict[str,Any]]]) -> list[dict[str,Any]]:
    labels=table_labels(EXCERPTS/"lamp-matrix.md")
    parts=lamp_parts()
    sol_rows=solenoid_table()
    if {a for a,n in labels.items() if n=="NOT USED"}!={85,86}:
        raise ValueError("printed unused-lamp set changed")
    result=[]
    for address,(label,kind) in SOLENOIDS.items():
        unused=address in {6,15,32,33,34,35,50}
        availability="unused" if unused else "unknown" if address in {37,38,39,40,41,42,43,44} else "used"
        physical:dict[str,Any]={}
        if address in FLASHER_QTY:
            pf,bb=FLASHER_QTY[address]
            physical["quantity"]=pf+bb
            physical["part_number"]="24-8704" if address==18 else "24-8802"
            physical["notes"]=f"Manual prints {pf} playfield and {bb} backbox bulb(s). One public output drives both branches."
        elif address in {23,24,25,26,27,28}:physical["notes"]="Bipolar slot-reel motor phase, paired A/B by reel; manual prints this circuit under Flasher or General Purpose."
        elif address in {37,38,39,40,41,42,43,44}:
            physical["notes"]="PinMAME-emulated state or LPDC address; the physical Security-board manual lists no fitted load at this address. Runtime significance remains unresolved."
        if address in {29,30}:
            physical["notes"]="PinMAME mirrors this WPC J111 general-purpose bit as a virtual public state channel; the factory manual assigns no separate load at this public address."
        if address==31:
            physical["notes"]="PinMAME synthetic game-on state, derived from the fast-flip RAM flag when configured; this is not a separately fitted coil."
        if address==32:
            physical["notes"]="PinMAME WPC constant-zero virtual output. The physical Security-board manual lists no load at this address."
        if address in {7}: physical["location"]="backbox"
        item={"id":f"solenoid.{address:02d}","label":label,"kind":kind,
              "binding":{"group":"pinmame.output.solenoid","device":address},
              "aliases":[{"namespace":"pinmame.solenoid","value":str(address)}],
              "availability":availability,"physical":physical,
              "provenance":prov(MANUAL_SRC,CORE_SRC,SCRIPT_SRC,status="candidate" if availability=="unknown" else "validated")}
        runtime_key="bank" if address==22 else "ramp-down" if address==5 else "ramp-up" if address==16 else "reels" if address in {23,24,25,26,27,28} else None
        if runtime_key:item["provenance"]=prov(MANUAL_SRC,CORE_SRC,SCRIPT_SRC,f"runtime.who-dunnit.{runtime_key}.wd-12")
        if address in {29,30,31}:item["roles"]=["internal.wpc-state"]
        if address==32:item["roles"]=["internal.unused.wpc-output"]
        if address in sol_rows:
            row=sol_rows[address]
            if row[4]!="blank":
                item["wiring"]={"board":"Fliptronic II board" if address==36 else "WPC Security Power Driver Board",
                                "driver_transistor":row[4],"drive_wire":row[6]}
                if row[3]!="blank":item["wiring"]["power_connection"]=row[3]
                if row[5]!="blank":item["wiring"]["drive_connection"]=row[5]
            if kind in {"coil","motor"} and address!=13 and row[7] not in {"---","blank"}:
                item["physical"]["part_number"]=row[7]
        if address==13:
            item["physical"]["notes"]="Factory drive table prints AE-26-1500; the same manual's location list and A-9415-2 assembly drawing print AE-26-1200. Fitted right-jet coil part remains unresolved."
        if address in {45,46,47,48}:
            manual_address={45:29,46:30,47:31,48:32}[address]
            item["aliases"].append({"namespace":"manual.solenoid","value":str(manual_address)})
            item["physical"]["notes"]="The manual prints this lower-flipper circuit as %d; PinMAME publishes it at public %d."%(manual_address,address)
            part={45:("J907-1","Q4","J902-13","Yel-Grn"),46:("J907-1","Q11","J902-11","Org-Grn"),
                  47:("J907-4","Q3","J902-9","Yel-Blu"),48:("J907-4","Q9","J902-7","Org-Blu")}[address]
            item["wiring"]={"board":"Fliptronic II board","power_connection":part[0],
                            "driver_transistor":part[1],"drive_connection":part[2],"drive_wire":part[3]}
            item["physical"]["part_number"]="FL-15411"
            item["provenance"]=prov(MANUAL_SRC,CORE_SRC,RUNTIME_SRC)
        if address in {7}:item["spatial"]=na("cabinet_or_service",MANUAL_SRC)
        elif address==32:item["spatial"]=na("virtual",CORE_SRC)
        elif unused:item["spatial"]=na("unused",MANUAL_SRC,CORE_SRC)
        elif kind=="virtual":item["spatial"]=na("virtual",CORE_SRC)
        result.append(item)
    for address in range(37,45):
        # WPC-95 mirrors LPDC 37–40 at 41–44; the Security-board manual has no matching load.
        result.append({"id":f"solenoid.{address:02d}","label":f"WPC-95 LPDC alias {address}","kind":"virtual",
                       "binding":{"group":"pinmame.output.solenoid","device":address},
                       "aliases":[{"namespace":"pinmame.solenoid","value":str(address)}],
                       "availability":"unknown","physical":{"notes":"Emulated WPC-95 LPDC alias; physical Security-board load unproven."},
                       "spatial":na("no_physical_device",MANUAL_SRC,CORE_SRC),
                       "provenance":prov(CORE_SRC,MANUAL_SRC,status="candidate")})
    for address,label in sorted(labels.items()):
        unused=address in {85,86}
        cabinet=address in {87,88}
        item={"id":f"lamp.matrix-{address}","label":label.title() if not unused else "Not Used",
              "kind":"lamp","binding":{"group":"pinmame.output.lamp","device":address},
              "aliases":[{"namespace":"pinmame.lamp","value":str(address)}],
              "availability":"unused" if unused else "used",
              "physical":{"location":"cabinet" if cabinet else "playfield"},
              "provenance":prov(MANUAL_SRC,SCRIPT_SRC)}
        if address in parts:
            bulb,assembly=parts[address]
            item["physical"].update({"quantity":1,"part_number":bulb,"assembly_part_number":assembly,
                                     "notes":"#555 insert bulb" if bulb=="24-8768" else "#44 incandescent bulb"})
        col,row=divmod(address,10)
        drive,drive_conn,drive_q=LAMP_COLUMN[col-1]
        ret,ret_conn,ret_q=LAMP_ROW[row-1]
        item["wiring"]={"board":"WPC Security Power Driver Board","drive_wire":drive,
                         "drive_connection":drive_conn,"return_wire":ret,"return_connection":ret_conn,
                         "return_component":f"column {drive_q}; row {ret_q}"}
        if unused:item["spatial"]=na("unused",MANUAL_SRC)
        elif cabinet:item["spatial"]=na("cabinet_or_service",MANUAL_SRC)
        elif (sp:=candidate_spatial("lamp",address,candidates,TABLE_SRC,SCRIPT_SRC,MANUAL_SRC)):
            item["spatial"]=sp
        result.append(item)
    gi=("Left Playfield","Right Playfield","Back Playfield","Insert 1","Insert 2")
    gi_objects=gi_candidates()
    gi_wiring=(("J121-1","Q18","J121-7","Wht-Brn"),("J121-2","Q10","J121-8","Wht-Org"),
               ("J121-3","Q14","J121-9","Wht-Yel"),("J120-5","Q16","J120-10","Wht-Grn"),
               ("J120-6","Q12","J120-11","Wht-Vio"))
    for address,label in enumerate(gi):
        item={"id":f"gi.string-{address+1:02d}","label":label,"kind":"gi",
              "binding":{"group":"pinmame.output.gi","device":address},
              "aliases":[{"namespace":"manual.gi","value":f"{address+1:02d}"}],
              "availability":"used","physical":{"location":"backbox" if address>=3 else "playfield",
                                                "part_number":"24-8768" if address>=3 else "24-6549",
                                                "notes":"Manual prints #555 insert bulbs." if address>=3 else "Manual prints #44 G.I. string."},
              "provenance":prov(MANUAL_SRC,CORE_SRC,SCRIPT_SRC)}
        power,triac,ret,wire=gi_wiring[address]
        item["wiring"]={"board":"WPC Security Power Driver Board","power_connection":power,
                         "driver_transistor":triac,"return_connection":ret,"return_wire":wire}
        if address>=3:item["spatial"]=na("cabinet_or_service",MANUAL_SRC)
        else:
            item["spatial"]={"status":"candidate","placements":[
                {"id":f"gi.string-{address+1:02d}.candidate-{n}","role":"emitter","space":"playfield",
                 "x":candidate["x"],"y":candidate["y"],
                 "provenance":prov(TABLE_SRC,SCRIPT_SRC,MANUAL_SRC,status="candidate")}
                for n,candidate in enumerate(gi_objects[address],1)]}
            item["physical"]["notes"]+=" Retained script dispatches this collection; only objects with a bulb mesh are coordinate candidates, and neither quantity nor physical socket agreement is proved."
        result.append(item)
    return result


def mechanisms() -> list[dict[str,Any]]:
    def mech(suffix: str,label: str,kind: str,acts: list[int],sensors: list[int],behavior: str,*refs: str) -> dict[str,Any]:
        return {"id":f"mechanism.{suffix}","label":label,"kind":kind,
                "actuators":[f"solenoid.{a:02d}" for a in acts],
                "sensors":[f"switch.matrix-{a}" for a in sensors],
                "behavior":behavior,"provenance":prov(*refs,status="observed")}
    return [
        mech("trough","Four-ball trough","kicker",[1],[31,32,33,34,35],
             "Four trough-position optos 32–35 feed the trough-eject coil 1; jam opto 31 watches the transfer. The retained script's trough routes an ejected ball into the shooter lane at 15.",MANUAL_SRC,SCRIPT_SRC),
        mech("auto-plunger","Auto plunger","kicker",[2],[15],
             "Plunger solenoid 2 launches a ball from shooter-lane switch 15; script SolAutoPlungerIM calls PlungerIM.AutoFire.",MANUAL_SRC,SCRIPT_SRC),
        mech("three-bank","Motorized three-bank","motorized",[22],[11,73,66,67,68],
             "Motor 22 raises/lowers the 3-bank. Switch 73 reports bank up and 11 reports position 2/down in the retained script; the three target contacts 66–68 remain distinct. Script initializes up, reverses travel after each endpoint, and waits one second before allowing another movement. A direct ROM T.16 test starts and stops output 22; no physical endpoint moves in that isolated run. The pinned preliminary simulator's mech mapping is inconsistent with the manual and is not physical authority.",MANUAL_SRC,SCRIPT_SRC,CORE_SRC,"runtime.who-dunnit.bank.wd-12"),
        mech("lift-ramp","Up/down ramp","diverter",[5,16],[74,36,37],
             "Solenoid 5 lowers and solenoid 16 raises the lift ramp. Switch 74 follows the endpoint in the script, with 36 Enter Ramp and 37 Made Ramp Left detecting balls. Direct ROM T.17 tests pulse 16 for RAMP UP and 5 for RAMP DOWN; no physical endpoint moves in those isolated runs. Script initializes the ramp up and changes its collision wall at the endpoints.",MANUAL_SRC,SCRIPT_SRC,"runtime.who-dunnit.ramp-up.wd-12","runtime.who-dunnit.ramp-down.wd-12"),
        mech("up-down-post","Up/down post","toy",[36],[],
             "Manual routes Up Down Post through the upper-left Fliptronic hold circuit, manual solenoid 36/public 36. Retained script starts the post down and raises it while output 36 is enabled.",MANUAL_SRC,SCRIPT_SRC,CORE_SRC),
        mech("left-reel","Left slot reel","reel",[23,24],[12],
             "Left reel uses B/A motor phases 23/24 and index opto 12. The factory A-20425 assembly lists a 1.8-degree 14-8024 stepper, hence 200 full steps per revolution. Direct ROM T.18 selection activates 23/24 without host mechanics. Retained cvpmMyMech uses a circular stepper; its phase sequence and eight-unit index window are simulation choices, not measured physical behavior.",MANUAL_SRC,SCRIPT_SRC,"runtime.who-dunnit.reels.wd-12"),
        mech("center-reel","Center slot reel","reel",[25,26],[25],
             "Center reel uses B/A motor phases 25/26 and index opto 25. The factory A-20425 assembly lists a 1.8-degree 14-8024 stepper, hence 200 full steps per revolution. Direct ROM T.18 selection activates 25/26 without host mechanics. Phase sequence, opto window and home offset remain unmeasured.",MANUAL_SRC,SCRIPT_SRC,"runtime.who-dunnit.reels.wd-12"),
        mech("right-reel","Right slot reel","reel",[27,28],[48],
             "Right reel uses B/A motor phases 27/28 and index opto 48 with the same factory 1.8-degree, 200-full-step A-20425 assembly. Direct ROM T.18 selection activates 27/28 without host mechanics. Pinned preliminary simulator incorrectly connects the first reel to solenoid 22 and the third reel to switch 12; the known-working script and factory table control the physical mapping.",MANUAL_SRC,SCRIPT_SRC,CORE_SRC,"runtime.who-dunnit.reels.wd-12"),
        mech("lockups-and-poppers","Lockups and right-side poppers","kicker",[3,4,8],[41,43,44,47,51,57],
             "Left lock-up coil 3 serves Lock Up 1 switch 51; right back/front poppers 4/8 serve their opto positions 43/44. The left/right hole and lower-right lock sensors 41,47,57 are separate ball-path signals. Ball-path sequence remains candidate because no isolated runtime trace is retained.",MANUAL_SRC,SCRIPT_SRC),
    ]


def drivers() -> list[dict[str,Any]]:
    by_id={item["id"]:item for item in load_json(ROOT/"catalog/pinmame.json")["drivers"]}
    result=[]
    for did in DRIVERS:
        item={k:v for k,v in by_id[did].items() if k in {"id","clone_of","description","year","manufacturer","flags"}}
        item["physical_compatibility"]="unknown" if did in {"wd_03r","wd_048r"} else "identical"
        item["variant_notes"]=("Prototype ROM declared on the same wdGameData; physical prototype hardware differences are undocumented."
                               if did in {"wd_03r","wd_048r"} else
                               "2020 elevator floor-text correction on the same physical game and public I/O." if did in {"wd_12p","wd_12gp"} else
                               "Language/sound or firmware revision on the same wdGameData; no distinct physical edition is documented.")
        result.append(item)
    return result


def build() -> dict[str,Any]:
    candidates=spatial_candidates()
    return {"format":"pinmame-machine-definition","schema_version":2,
            "machine":{"id":MID,"name":"WHO dunnit","manufacturer":"Bally","year":1995,
                       "kind":"physical_pinball","ipdb_id":3685,"opdb_id":"G50kj-MDqpv",
                       "playfield":{"width":953,"height":2128,"units":"vpx","provenance":prov(TABLE_SRC,EXTRACTION_SRC)}},
            "coverage":{"status":"partial",
                        "missing":["input_semantics","output_semantics","mechanism_behavior","polarity",
                                   "variant_differences","spatial_placement","unresolved_conflicts"],
                        "dimensions":{"catalog_identity":"validated","address_enumeration":"validated",
                                      "semantic_naming":"validated","physical_wiring":"observed",
                                      "mechanisms":"observed","variant_coverage":"observed",
                                      "recreation_knowledge":"validated","spatial_placement":"candidate"}},
            "controller":{"platform":"pinmame.wpc-95","hardware_generation":"0x40","inversion_applied_by_emulator":True},
            "drivers":drivers(),"inputs":inputs(candidates),"outputs":outputs(candidates),
            "displays":[{"id":"display.dmd","label":"Dot Matrix Display","kind":"dmd","controller_index":0,
                         "width":128,"height":32,"spatial":na("cabinet_or_service",MANUAL_SRC,CORE_SRC),
                         "provenance":prov(MANUAL_SRC,CORE_SRC)}],
            "mechanisms":mechanisms(),"relationships":[],"sources":source_records(),
            "knowledge":{"path":"knowledge/bally/who-dunnit-1995.md","status":"partial"},
            "conflicts":[{"id":"conflict.right-jet-coil-part","path":"outputs[id=solenoid.13].physical.part_number",
                          "description":"The manual's printed 2-46 solenoid drive table lists the right jet coil as AE-26-1500, while its 2-46 location table and printed 2-21 A-9415-2 jet assembly drawing list AE-26-1200. The physical fitted part is not established by these conflicting factory cells. Resolution path: inspect a documented original right-jet assembly or obtain an applicable factory correction before asserting a part number.",
                          "source_refs":[MANUAL_SRC,ASSEMBLY_SRC],"status":"unresolved"}]}


def spatial_report(definition:dict[str,Any]) -> dict[str,Any]:
    missing=[item["id"] for item in definition["inputs"]+definition["outputs"] if item["availability"]=="used" and "spatial" not in item]
    candidates=[item["id"] for item in definition["inputs"]+definition["outputs"] if item.get("spatial",{}).get("status")=="candidate"]
    by_class={"switch":[],"lamp":[],"gi":[]}
    for item in definition["inputs"]+definition["outputs"]:
        if item["id"] in candidates:
            by_class["gi" if item["kind"]=="gi" else "lamp" if item["kind"]=="lamp" else "switch"].append(item["id"])
    return {"format":"pinmame-spatial-blockers","version":1,"machine_id":MID,
            "table_sha256":TABLE_SHA,"script_sha256":SCRIPT_SHA,"manual_sha256":MANUAL_SHA,
            "extraction_manifest_sha256":MANIFEST_SHA,"extraction_file_count":FILE_COUNT,
            "spatial_seed_sha256":sha(SPATIAL_SEED),"gi_seed_sha256":sha(GI_SEED),
            "evidence_paths":{"table":f"vpx-sources/bally/who-dunnit-1995/{TABLE_NAME}",
                              "extracted":"vpx-sources/bally/who-dunnit-1995/extracted",
                              "extraction_manifest":"vpx-sources/bally/who-dunnit-1995/extracted.manifest.json",
                              "manual":f"manuals/by-machine/{MID}/ipdb-3685/{MANUAL_NAME}",
                              "spatial_seed":"tools/seeds/bally/who-dunnit-1995-spatial.json",
                              "gi_seed":"tools/seeds/bally/who-dunnit-1995-gi-candidates.json"},
            "bounds":{"left":0,"top":0,"right":953,"bottom":2128},
            "transform":"x=object_x/953; y=object_y/2128; player view, rear y=0, apron y=1; values rounded to six decimals",
            "projection_classes":{"switch":"Exact-name VPX collision object centre for matrix switch or F5 Spinner, candidate only; cabinet, EOS and always-closed positions use controlled not_applicable.",
                                  "lamp":"Exact LNN VPX Light centre, candidate only. L16/L17/L18 glow helpers are excluded; the factory location drawing on PDF 125 still needs device-by-device socket reconciliation.",
                                  "gi":"Script collection members GI_Left/GI_Right/GI_Top with bulb mesh; 11/10/28 retained. Other collection members are glow/reflection leads, not sockets. Factory GI socket quantity is unknown.",
                                  "flasher_and_coil":"No Flasher sprite, mesh offset or target glow is accepted as a physical load centre; factory callout and exact-table lens/mesh reconciliation remain pending.",
                                  "manual_drawing":"PDF 125 printed 2-43 provides numbered lamp callouts, but has not been metrically fitted to the VPX table frame. No callout balloon is used as a coordinate."},
            "candidate_placements":candidates,"candidate_by_class":by_class,"without_placements":missing,
            "spatial_seed_objects":load_json(SPATIAL_SEED)["candidates"],
            "gi_seed_objects":load_json(GI_SEED)["candidates"],
            "promotion_decision":"partial: no measured physical socket census or full mechanism geometry; exact VPX centres are candidates, not validated physical placements; prototype physical differences and output semantics remain unresolved."}


def report_markdown(report:dict[str,Any]) -> str:
    return (f"# WHO dunnit spatial blockers\n\nRetained VPX SHA-256 `{TABLE_SHA}`; script `{SCRIPT_SHA}`; "
            f"{FILE_COUNT}-file extraction manifest `{MANIFEST_SHA}`; manual `{MANUAL_SHA}`.\n\n"
            f"Bounds: `left=0 top=0 right=953 bottom=2128`. {report['transform']}.\n\n"
            f"{len(report['candidate_placements'])} devices have exact-name VPX object candidates; "
            f"{len(report['without_placements'])} used devices have no placement. "
            "No candidate is promoted to a physical socket without reconciling the manual location drawing. "
            "Flasher sprites, shared backbox bulbs, G.I. strings, reels and the under-playfield mechanisms need separate anchors.\n\n"
            "## Retained registers and projection classes\n\n"
            f"The [VPX object register](../../../tools/seeds/bally/who-dunnit-1995-spatial.json) has SHA-256 `{report['spatial_seed_sha256']}`; "
            f"the [G.I. bulb-mesh register](../../../tools/seeds/bally/who-dunnit-1995-gi-candidates.json) has SHA-256 `{report['gi_seed_sha256']}`. "
            "The JSON form of this report embeds each named object, file and normalized point.\n\n"+
            "\n".join(f"- **{name} ({len(report['candidate_by_class'].get(name, []))} candidate devices):** {description}" for name,description in report["projection_classes"].items())+"\n\n"
            "## Missing placements\n\n"+"\n".join(f"- `{name}`" for name in report["without_placements"])+"\n")


def verify_external() -> None:
    vpx_root=os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    manual_root=os.environ.get("PINMAME_MANUALS_ROOT")
    if vpx_root:
        root=Path(vpx_root)/"bally/who-dunnit-1995"
        if sha(root/TABLE_NAME)!=TABLE_SHA or sha(root/"extracted/script.vbs")!=SCRIPT_SHA:
            raise RuntimeError("retained WHO dunnit table or script hash mismatch")
        manifest=load_json(root/"extracted.manifest.json")
        files=[]
        for path in sorted((root/"extracted").rglob("*"),key=lambda p:p.relative_to(root/"extracted").as_posix()):
            if path.is_file(): files.append({"path":path.relative_to(root/"extracted").as_posix(),"size":path.stat().st_size,"sha256":sha(path)})
        expected={"format":"pinmame-vpx-extraction-manifest","version":1,"files":files}
        if canonical_bytes(manifest)!=canonical_bytes(expected) or len(files)!=FILE_COUNT or sum(f["size"] for f in files)!=TOTAL_BYTES or hashlib.sha256(canonical_bytes(expected)).hexdigest()!=MANIFEST_SHA:
            raise RuntimeError("retained WHO dunnit extraction manifest mismatch")
        for item in load_json(SPATIAL_SEED)["candidates"]:
            source=load_json(root/"extracted/gameitems"/item["file"])
            obj=next(iter(source.values()))
            center=obj.get("center") or obj.get("position") or obj.get("center_position")
            if obj.get("name")!=item["object"] or round(center["x"]/953,6)!=item["x"] or round(center["y"]/2128,6)!=item["y"]:
                raise RuntimeError(f"VPX object centre drift: {item['file']}")
        for item in load_json(GI_SEED)["candidates"]:
            source=load_json(root/"extracted/gameitems"/item["file"])
            obj=source["Light"]
            center=obj["center"]
            if obj.get("name")!=item["object"] or not obj.get("show_bulb_mesh") or round(center["x"]/953,6)!=item["x"] or round(center["y"]/2128,6)!=item["y"]:
                raise RuntimeError(f"VPX G.I. candidate drift: {item['file']}")
    if manual_root:
        path=Path(manual_root)/"by-machine"/MID/"ipdb-3685"/MANUAL_NAME
        if sha(path)!=MANUAL_SHA: raise RuntimeError("retained WHO dunnit manual hash mismatch")
        core_root=Path(manual_root).parent/"source-checkouts/pinmame"
        revision=subprocess.run(["git","-C",str(core_root),"rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
        if revision!=PIN or sha(core_root/"src/wpc/sims/wpc/prelim/wd.c")!="ef33ac1bdae145166c00d4dadcb95e5b10f883cc88da01c7577b5ee09775f6e1":
            raise RuntimeError("authoritative pinned WHO dunnit core checkout mismatch")
    review_root=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review_root:
        runtime=Path(review_root)/MID/"session-20260930/terra-runtime"
        if sha(runtime/"traces/06-switch-edges-115-112-114.json")!=RUNTIME_SHA or sha(runtime/"scenarios/06-switch-edges-115-112-114.json")!=SCENARIO_SHA:
            raise RuntimeError("retained WHO dunnit causal runtime evidence mismatch")
        frames={"010-f5-spinner-asserted-at-source-predicted-rom-level-1-display-0.pgm":"6400cb84f576c088cbfca5f31850156a98f87e65d8c25983aa1fa989b3eeae53",
                "012-f2-lower-right-flipper-cabinet-asserted-at-source-predicted-rom-level-1-display-0.pgm":"f1f97456c9b58797fb19e340207b02b977af29df48e0e5d551bc422ac0fb30dd",
                "014-f4-lower-left-flipper-cabinet-asserted-at-source-predicted-rom-level-1-display-0.pgm":"d41fd568e649d1271263ebd5cc85f7ad448edadb70981d35aa694c7649eb1f21"}
        for name,digest in frames.items():
            if sha(runtime/"dmd/06-switch-edges-115-112-114"/name)!=digest:
                raise RuntimeError(f"retained WHO dunnit DMD evidence mismatch: {name}")
        sol_runtime=Path(review_root)/MID/"session-20260930/sol-runtime"
        for key,(name,trace_sha,scenario_sha,frame,frame_sha,_) in SOL_RUNTIME.items():
            trace=sol_runtime/"traces"/f"{name}.json"
            scenario=sol_runtime/"scenarios"/f"{name}.json"
            if sha(trace)!=trace_sha or sha(scenario)!=scenario_sha or sha(sol_runtime/"dmd"/name/frame)!=frame_sha:
                raise RuntimeError(f"retained WHO dunnit ROM diagnostic evidence mismatch: {key}")
            result=load_json(trace)
            if result["failure"] is not None or result["handle_mechanics"]!=0:
                raise RuntimeError(f"WHO dunnit ROM diagnostic failed or enabled simulation: {key}")
        for address,(frame,digest) in OPTO_FRAMES.items():
            if sha(sol_runtime/"dmd/07-opto-edges"/frame)!=digest:
                raise RuntimeError(f"WHO dunnit ROM opto DMD frame mismatch: {address}")


def check() -> None:
    if READY.exists():raise RuntimeError("stale WHO dunnit author-ready record")
    definition=build(); report=spatial_report(definition)
    for path,content in ((PARTIAL,canonical_bytes(definition)),(SEED,canonical_bytes(definition)),
                         (REPORT,canonical_bytes(report)),(REPORT_MD,report_markdown(report).encode("utf-8"))):
        if not path.is_file() or path.read_bytes()!=content:raise RuntimeError(f"WHO dunnit deterministic artifact drift: {path}")
    verify_external()


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--regenerate",action="store_true")
    args=parser.parse_args()
    if args.check:check();print("WHO dunnit curator and retained evidence match")
    else:
        if READY.exists():raise RuntimeError("refusing to overwrite an author-ready WHO dunnit artifact")
        definition=build();report=spatial_report(definition)
        write_json(PARTIAL,definition);write_json(SEED,definition);write_json(REPORT,report);write_text(REPORT_MD,report_markdown(report))


if __name__=="__main__":main()
