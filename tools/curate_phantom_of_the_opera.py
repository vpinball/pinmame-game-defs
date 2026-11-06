"""Reproduce the reviewed Data East Phantom of the Opera contribution.

The manual transcription and resolved VPX candidates are compact, committed inputs.
External evidence is optional for reproduction, but, when supplied, is verified fail-closed.
No coordinate from a render helper is silently promoted to a physical socket.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from pinmame_game_defs.coverage import (build_coverage_report, build_curation_queue, render_coverage_markdown,
                                        render_curation_queue_markdown, write_coverage_report)
from pinmame_game_defs.jsonio import content_sha256, load_json, write_text
from pinmame_game_defs.priorities import refresh_pinside_top100
from pinmame_game_defs.registry import rebuild_catalog
from pinmame_game_defs.spatial import _round_point
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships, vpm_staged_flipper_notes
from build_external_evidence_manifest import check_manifest
from build_phantom_organ_evidence import build as build_organ_evidence
from build_phantom_runtime_evidence import build as build_service_evidence

ROOT = Path(__file__).resolve().parents[1]
ID = "data-east.phantom-of-the-opera.1990"
SLUG = "phantom-of-the-opera-1990"
MACHINE = Path(f"machines/partial/data-east/{SLUG}.json")
SEED = Path(f"tools/seeds/data-east/{SLUG}.json")
MANUAL_DATA = Path(f"tools/seeds/data-east/{SLUG}-manual.json")
PLACES = Path(f"tools/seeds/data-east/{SLUG}-places.json")
KNOWLEDGE_SEED = Path("tools/phantom_of_the_opera_knowledge.md")
KNOWLEDGE = Path(f"knowledge/data-east/{SLUG}.md")
REPORT = Path(f"reports/spatial/data-east/{SLUG}.json")
REPORT_MD = Path(f"reports/spatial/data-east/{SLUG}.md")
EXCERPTS = Path(f"evidence/excerpts/{ID}")
PIN = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CORE = "pinmame.core.46e1a01a0f73"
CATALOG = "pinmame.catalog.46e1a01a0f73"
MANUAL = "manual.data-east.phantom-of-the-opera.1990"
SCRIPT = "vpx-script.phantom-of-the-opera-1.25"
TABLE = "vpx-table.phantom-of-the-opera-1.25"
EXTRACTION = "vpx-extraction.phantom-of-the-opera-1.25"
LIBRARY = "vpm-script-library.phantom-de-vbs"
OWNERS = "human-review.phantom-knocker-owners"
IPDB = "human-review.ipdb-1777-identity"
MANUAL_FILE = "Data_East_1990_Phantom_of_the_Opera_English_Manual_with_paginated_schematics.pdf"
MANUAL_SHA = "1feebf59ab838056591fd67853bd2b54a9524447038e2a7a2c7ad3fe4765cd09"
TABLE_FILE = "Phantom Of The Opera (Data East 1990) v1.25.vpx"
TABLE_SHA = "e609fdfe0c358957ac2314f298cc6236523a62cd5cd6b979d0c1bc4f475e3bd9"
SCRIPT_SHA = "e373bf66dab343166e954fb2a7ed9c1ee0d8627ae5e125b13e4339b46757d5f6"
MANIFEST_SHA = "029e0bdb66b39060e5de73294a1f9cd5b72f5615ea1ecab2c10ec282091e0c12"
CORE_VBS_SHA = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
DE_VBS_SHA = "8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04"
PIN_SIDE_SHA = "ad9d5ebc5811d7a869f7aedbb0daa0a38f49c890638fd10dbfd46d3d0bb7161c"
MISSING = ["input_semantics", "output_semantics", "spatial_placement"]
PLAYFIELD_BOUNDS = {"left": 0, "top": 0, "right": 952, "bottom": 2162}
PLAYFIELD_WIDTH = PLAYFIELD_BOUNDS["right"] - PLAYFIELD_BOUNDS["left"]
PLAYFIELD_HEIGHT = PLAYFIELD_BOUNDS["bottom"] - PLAYFIELD_BOUNDS["top"]
EFFECT_ANCHORS = {
    16: {"object": "Plunger1", "x": 51.902588, "y": 1884.659},
    26: {"object": "BallRelease", "x": 833.5977, "y": 1858.1306},
}
ORGAN = "runtime.phantom.organ-probe"
ORGAN_EVIDENCE = Path("evidence/runtime/data-east/phantom-of-the-opera-organ.json")
ORGAN_SHA = "1335a3e09e2ff856107338331d11dcce73bd1c830358203b0651db8f2d5d60a8"
SERVICE = "runtime.phantom.service-walk"
SERVICE_EVIDENCE = Path("evidence/runtime/data-east/phantom-of-the-opera-service-walk.json")
SERVICE_SHA = "446feefe90ce811853a3b23f7419f1366de5298518ab4cdacdf8d835c4046f15"
ROM_ANALYSIS = "human-review.phantom-output20-rom-analysis"
ROM_ANALYSIS_SHA = "6a038fd88ead731c1d6a885304359ca2b301441f42de46caeb6fc1bc3462b06e"
READINGS = Path(f"tools/seeds/data-east/{SLUG}-service-readings.json")
INPUT_HASHES = {
    MANUAL_DATA: "2917ec81b87aea75a265fe83d202534b0d63fc4062abd1bb20f72390a8e8cfb1",
    PLACES: "7fba13141ae38b7f94981cf113a74432143a86af3b4e06fb9caa888873441965",
    READINGS: "f8d8d01926a2db0d060e18b3c93ecb6726025596e7a687d782cbd57822ec0741",
}
SPECIAL_PUBLIC = {17: 1, 18: 3, 19: 4, 20: 6, 21: 5, 22: 2}
SPECIAL_SWITCH = {1: 48, 2: 47, 3: 21, 4: 46, 5: 22}
BACKBOX_LAMPS = {39, 40, 47, 48}
BACKBOX_FLASH = {1: 3, 2: 1, 3: 0, 4: 1, 5: 3, 6: 2, 7: 2, 8: 2, 9: 0, 12: 0, 13: 0, 15: 2}
FLASH = set(BACKBOX_FLASH)


def text_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def aliases(namespace: str, number: int, manual: str | None = None) -> list[dict]:
    result = [{"namespace": namespace, "value": str(number)}]
    if namespace == "pinmame.switch" and number > 0:
        result.extend({
            "namespace": namespace,
            "value": value
        } for value in (f"{number:02}", f"{number:03}") if value != str(number))
    if manual is not None:
        result.append({"namespace": "manual.address", "value": manual})
    return result


def located(device_id: str, candidates: list[dict], role: str, *, status: str = "observed") -> dict:
    return {
        "status": status,
        "placements": [{
            "id": f"{device_id}.placement-{i}",
            "role": role,
            "space": "playfield",
            "x": _round_point((p["x"] - PLAYFIELD_BOUNDS["left"]) / PLAYFIELD_WIDTH),
            "y": _round_point((p["y"] - PLAYFIELD_BOUNDS["top"]) / PLAYFIELD_HEIGHT),
            "provenance": prov(TABLE, SCRIPT, MANUAL, status=status)
        } for i, p in enumerate(candidates, 1)]
    }


def matrix_excerpt(data: dict, which: str) -> str:
    switch = which == "switch"
    labels = data[f"{which}_matrix"]
    drives, returns = data[f"{which}_drives"], data[f"{which}_returns"]
    lines = [
        f"# Phantom of the Opera {which} matrix", "", f"Source: {data['locators'][which + '_matrix']}.", "",
        "Method: direct visual transcription from native-resolution renders. OCR was a search aid. Curator: project curator. Reviewed: yes.",
        "",
        "Full printed table region, column-major; line wrapping is collapsed to spaces. Literal labels are retained before reconciliation.",
        "", "| Row | " + " | ".join(f"{i+1}: {d[0]} ({d[1]}) {d[2]}" for i, d in enumerate(drives)) + " |",
        "| --- | " + " | ".join("---" for _ in drives) + " |"
    ]
    for row, ret in enumerate(returns):
        header = f"{row+1}: {ret[0]} ({ret[1]})" + (f" {ret[2]}" if len(ret) > 2 else "")
        lines.append("| " + header + " | " + " | ".join(f"{col*8+row+1}: {labels[col*8+row]}"
                                                        for col in range(8)) + " |")
    lines += [
        "",
        "The printed footnote says that the two-digit number in parentheses is the resistor/wire-colour code displayed during diagnostics.",
        "", "## Complete adjacent description list", ""
    ]
    if switch:
        lines += ["| Number | Printed description | Part No. |", "| --- | --- | --- |"]
        lines += ["| " + " | ".join(row) + " |" for row in data["switch_descriptions"]]
        lines += [
            "",
            "`*` identifies cabinet switches in the printed list. The compound rows 15, 16, 21 and 22 combine separately printed descriptions under one number; semicolons above are transcription separators, not printed punctuation. Parts shared by two descriptions are repeated as a slash-separated pair.",
            "",
            "The own-game switch schematic draws the matrix contacts open. CN8 switch-drive pins for columns 1-8 are 1, 2, 3, 4, 5, 7, 8, 9; CN10 return pins for rows 1-8 are 9, 8, 7, 6, 5, 3, 2, 1. Its colour spelling `GRN-ORG` at drive 3 is retained here; the matrix prints `GRN-ORN`. The cabinet drawing shows the cabinet contacts open too."
        ]
    else:
        lines += ["| Number | Printed description |", "| --- | --- |"]
        lines += [
            f"| {i:02}{'*' if i in BACKBOX_LAMPS else ''} | {label} |"
            for i, label in enumerate(data["lamp_descriptions"], 1)
        ]
        lines += [
            "",
            "The description-list footnote is `*Indicates Insert Lamp`; the wiring-sheet footnote calls them insert-board lamps. These four backglass lamps are cabinet/backbox devices.",
            "",
            "Lamp 25 prints Right Circle in the matrix but Left Circle in both description lists; the location drawing puts 25 on the left circle. The structured label follows the lists and drawing. The location drawing puts a 56 label on the organ while both lists and the matrix say Unused; that leader-less label is not a fitted-bulb record. The generic wiring drawing also draws every matrix symbol, including LB56, and is not proof of fitment.",
            "",
            "The own-game lamp schematic prints CPU CN7 drive pins 1, 2, 3, 4, 6, 7, 8, 9 for columns 1-8; CN6 return pins 1, 2, 3, 5, 6, 7, 8, 9 for rows 1-8. GI is drawn as parallel bulb symbols on connector 4M/F6: pin 1 YEL, pin 2 WHT-YEL, pin 3 VIO, pin 4 WHT-VIO. Those are schematic symbols, not a socket count."
        ]
    return "\n".join(lines) + "\n"


def coil_excerpt(data: dict) -> str:
    lines = [
        "# Phantom of the Opera coil and flasher circuits", "", f"Source: {data['locators']['coils']}.", "",
        "Method: direct visual transcription of the complete printed special/flipper/coil-part tables and every populated branch of the game's coil wiring. project curator; reviewed against native-resolution renders. Drawing labels are factual transcriptions; whole manual pages are retained externally.",
        "", "## Switch-triggered solenoids", "",
        "| Coil | Description | Control wire | Control pin | Trigger wire | Trigger pin | Drive transistor (TIP122) | Coil type |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    ]
    lines += ["| " + " | ".join(row) + " |" for row in data["special_coils"]]
    lines += [
        "",
        "The printed Power Line column is RED / PS CN3-6 for SP1-SP5, and `--` / PS CN3-6 for SP6. The repeated values belong to the separately printed rows. SP6's coil type is `--`; no load is drawn. The special-wiring sheet prints CPU CN16 on the trigger header, where the table and backbox connector list print CN18; the device, wire and pin numbers agree. Follow the own-game table for the structured connector and retain the disagreement as a wiring note.",
        "", "## Flipper solenoids", "",
        "| Description | Flipper GND (CPU to coil) | Power lines: switch to flipper PCB | Power lines: PCB to coil | Coil type |",
        "| --- | --- | --- | --- | --- |"
    ]
    lines += ["| " + " | ".join(row) + " |" for row in data["flipper_table"]]
    lines += [
        "",
        "The common Power Input To Flip PCB column prints BLK-WHT / 50VDC and GRY-GRY GRN / 8VAC. The flipper table prints 23-900 for each coil; the part chart lists two 23-900 coils, part 090-5020-30. These are two physical coils; the four public flipper power/hold bits are emulator state.",
        "", "## Complete coil part-number chart", "", "| Quantity used | Coil type | Data East part number |",
        "| --- | --- | --- |"
    ]
    lines += ["| " + " | ".join(map(str, row)) + " |" for row in data["coil_part_table"]]
    lines += [
        "", "## Complete populated coil/flash wiring branches", "",
        "Public numbers 25-29 below correspond to the drawing's SIDE R01-R05; 1-8 are SIDE L01-L08. The public mapping is the K1 mux in pinned s11.c, checked against the retained script. This added public column is not printed by the manual.",
        "",
        "| Public | Printed load | CPU transistor | CPU wire | CPU pin | Load-side wire | Load-side pin | Printed coil/bulbs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    ]
    lines += ["| " + " | ".join(map(str, row[:8])) + " |" for row in data["driver_rows"]]
    lines += [
        "",
        "The L01-L08 flasher supply is BRN, +32VL, PPB J6-3; R01-R03 use ORN +32VR PPB J6-4/5. R04/R05 use YEL-VIO +50VR via PPB J7-6/7 and Q4/Q3 on the PPB. The direct flashers 9, 12, 13, 15 use RED +32V; the Laserkick coil uses VIO-YEL +50VDC from PPB J7-3. The motor relay is driven from BRN-BLU/Q25 and switches WHT-RED 25VAC from BR2 in the backbox; its schematic draws a diode across the relay coil and COM/NO/NC contacts.",
        "",
        "The game's own PPB J2 connector list names only OUTHOLE, TROUGH, LEFT SIDE MIDDLE VUK, TOP LEFT SUPER VUK and RIGHT SIDE MIDDLE SUPER VUK. It marks the R06/R07/R08 destinations N.U.; no load branch for them is drawn on printed pages 27 or 42. The coil-location drawing nevertheless includes an R08 label near the apron. That isolated label does not identify a knocker or settle the state PinMAME can publish at 32.",
        "", "## Complete backbox flasher inset", "",
        "The inset has 16 drawn sockets: L01 points to 3, L02 to 1, L04 to 1, L05 to 3, L06 to 2, L07 to 2, L08 to 2, and 15 to 2. There is no L03 backbox callout. The remaining lamps in each printed total are playfield bulbs. This inset is an elevation, not a registered playfield coordinate drawing."
    ]
    return "\n".join(lines) + "\n"


def script_excerpt() -> str:
    return """# Phantom of the Opera 1.25 runtime bindings

Source: retained embedded script.vbs, SHA-256 e373bf66dab343166e954fb2a7ed9c1ee0d8627ae5e125b13e4339b46757d5f6. TastyWasps, based on 32assassin, DCrosby and Cirque; other credits in the source. Method: direct code reading, project curator, reviewed.

The script declares poto_a32 and loads de.vbs (lines 58-68); HandleMechanics=0 and HandleKeyboard=0 (316-326). Lines 133-157 bind solenoids 1-7 to SetLamp 101-107; 8 to FlashRed4; 9 to FlashRed5; 10 to SolRelayB; 11 to PFGI; 12 to FlashRed3; 13 to FlashRed1; 14 to SolRamp; 15 to FlashRed2; 16 to SolKickback; 25 to bsTrough.SolIn; 26 initially to bsTrough.SolOut then to ballreleasehack; 27 to bsSaucer.SolOut; 28 to VukTopPop; 29 to BotPop; 30/31 to empty callbacks; 32 to a Knocker sound. The callback overwrite at 26 is intentional executable code, so the later handler wins.

Lines 342-351 initialize bsTrough.InitSw 0,13,12,11,10,0,0,0 with three balls and exit BallRelease; bsSaucer.InitSw 0,28,29,0,0,0,0,0 exits sw28 and kicks one ball per command. Drain_Hit adds to the trough; sw28_Hit adds to the two-ball saucer. ballreleasehack suppresses the last trough ball unless the left saucer holds two. It is a table workaround, not a machine's physical interlock.

TopVUK asserts 36 while occupied and output 28 clears it and raises/kicks its ball; BottomVUK does the same for switch 44/output 29 (516-583). The raise timers, DestroyBall/CreateBall transfers, Kick angles/velocities and subway helper Kicker2→Kicker3 are VPX geometry/tuning, not physical device counts.

Direct switch objects are sw14,17-20,25-27,37,45; pulse objects are sw23 spinner, sw30/31 ramp gates, sw33-35/41-43/49-51 targets. Left/right sling events pulse 21/22. Bumper1 pulses 46, Bumper2 pulses 48, Bumper3 pulses 47 (663-670). This nonsequential bumper order agrees with the manual's spatial identities.

The organ initializes its counter at 0, drives switch 53 true and 52 false, and sets rampdown=1/collidable. Output 14 alternates the animation direction on rising calls. At counter >60 it asserts 52, clears 53 and makes RampOrgan noncollidable; below 0 it asserts 53, clears 52 and restores collision (707-746). Thus the comments beside initialization call the endpoints backwards, while executable state agrees with manual 52 Open / 53 Closed. There is no public direction output. A physical reconstruction uses the motor's crank/limit switches, not the script's counter as measured cam geometry.

LampTimer reads ChangedLamps into LampState/FadingLevel, then UpdateLamps uses NfadeL for 1-48 and 57-64, Flash on f49-f55, and no binding for 56. Solenoid pseudolamps 101-107 drive S101a; S102a/b/c; S103a; S104a/b; S105a; S106a/b; S107a/b. NfadeL 53,S108b1 also drives an organ glow from a rear-panel letter lamp address, while the organ animation writes it directly. This is a table-lighting defect; it is not a second physical lamp 53. The active NfadeLm115,S115a has no SetLamp115 callback.

SolRelayB(10) and PFGI(11) both invert the same GI collection (287-304). The manual identifies 10 as the PPB's A/C mux relay and 11 as the GI relay. The extra GI handler at 10 is table behavior, not a second GI control or changed physical wiring.

The five Flupper anchors are Flasherbase1-5; callbacks13/15/12/8/9 drive those anchors respectively. They do not enumerate the physical four-bulb circuits, and their library flare/bloom sprites add no bulbs. The matrix Light objects are insert overlays without shown bulb meshes; off-table L39/L40/L47/L48 and S101a are invisible backbox helpers. Rear-panel f49-f55 are render sprites. They never establish physical bulb coordinates.
"""


def organ_excerpt() -> str:
    return """# Phantom of the Opera mechanism construction

Sources: manual PDF page 8 / printed 4 (game-specific features), page 25 / printed 21 (Organ Test), page 39 / printed 35 (motor/bracket and ball feed), page 40 / printed 36 (outhole/VUK), page 65 / printed 60 (rear-under ramp). Direct visual read by project curator, reviewed against native-resolution renders. Prose is paraphrased; part labels are transcribed factual data.

The organ is a raising ramp that admits a shot to the below-playfield cavern. A relay driven by Q25 controls the motor. The CPU reads two limit switches, Organ Closed and Organ Open; neither should be closed midway, each closes just before its travel limit, and both must never be closed together. Holding Start in Organ Test repeatedly pulses the motor relay and displays Closed on player3 and Open on player4. The test lets a technician leave the ramp midway to clear both switches before Active Switch Test.

The complete motor/bracket drawing labels: motor plate 535-5773-00, insulator 515-5249-00, crank arm 515-5238-00, switch 180-5052-00 (2), motor assembly 515-5256-00-08; whole MOTOR & BRK'T ASS'Y 500-5212-00-08. The front view shows a rotary crank driving two limit-switch levers. It does not assign each drawn switch to its public number or specify measured cam angles, speed, or a reversing electrical circuit.

The full ball-feed drawing labels: spring 265-5001-00; fiber link 545-5062-00; plunger complete 515-5006-00; eject arm 535-5025-00; eject cam; coil-retainer bracket 535-5203-00; spring 266-5000-00; AE-23-840 coil 090-5005-00; screw, washer, nut; bracket-and-stop 515-5011-00. Assembly 500-5012-00.

The full outhole drawing labels: coil 090-5005-00, coil stop 515-5088-00, solenoid plunger 530-5013-02, link 530-5058-00, kicker lever assembly 515-5016-00, base plate 515-5015-00, spring 265-5000-00, striker ring 545-5032-00, coil-retainer bracket 535-5203-02, screw/washer 2 each, roll pin, clip ring. Whole OUTHOLE BALL RETURN ASSY 500-5082-00.

The adjacent VUK 500-5067-00 table is complete: 1 Vert.Kick.Cap545-5078-00; 2 Pin.094x.500535-5111-00; 3 Plunger Assy515-5096-00; 4 Coil Retainer Brkt.(2)535-5203-01; 5 Coil23-800090-5001-01; 6 Phillips Screw(4)#8-32x1/4 LG.; 7 1N4004 Diode112-5003-00; 8 Compression Ring(3)270-5010-00; 9 Spring266-5099-00; 10 Bumper280-5003-00; 11 VUK Bracket535-5271-00; 12 Cap Spring*265-5016-00. Footnote: spring added when used with microswitch. The coil part chart on printed 26 instead prints 090-5001-00 for 23-800; retain that part-number distinction without changing physical identity.

The game's rear-under BALL RAMP ASS'Y 500-5161-00 drawing labels 545-5144-00 ball ramp, 500-5159-00 micro-switch/bracket assembly, 535-5800-01 and 535-5800-02 deflectors,535-5731-00 hanger bracket (2), 535-5795-00/626-5005-00,237-5808-00(4),249-5001-00 rivet(2),240-5004-00 nut(2),237-5501-00 screw(2). Its revision A adds foam tape and plate, E.C.,1-15-90. This is a physical ball path, not the table's teleporting helper count.

The organ opens after completing three organ targets or the lit shooter-lane skill shot. The manual describes initial capture/release, then locking two balls before a countdown expires for three-ball play; the third serve releases both stored balls. During three-ball play an organ-target hit opens the organ for a timed jackpot shot. Exact game timing and operator choices remain ROM-owned; geometry, animation rate and ball velocities remain recreation-owned.
"""


def library_excerpt() -> str:
    return f"""# Phantom of the Opera flipper input path

The retained table loads de.vbs at script line 68. Retained de.vbs SHA-256 {DE_VBS_SHA}, core.vbs SHA-256 {CORE_VBS_SHA}; both are VPinMAME contributors' libraries, retained from the working installation. Direct code read, project curator, reviewed.

de.vbs lines 33-36 declares swLRFlip=82, swLLFlip=84, swURFlip=86, swULFlip=88. vpmKeyDown/vpmKeyUp set/clear 82 and 84 for the lower right/left keys. The table's KeyDownHandler/KeyUpHandler invoke that library path (core.vbs lines 2854-2855 dispatch); its direct writes 15/16 are overwritten by PinMAME's FLIP1516 copy. Drive 82/84.

core.vbs defines sLRFlipper=46 and sLLFlipper=48. These are the table's callbacks for the synthetic hold bits; core_updateSw synthesizes 45/46 and 47/48 as pairs while game-on 23 is enabled. The physical machine has two 23-900 flipper coils on its solid-state flipper board, not four driver-board outputs.

The table calls vpmInit and does not declare cSingleLFlip/cSingleRFlip or call NoUpperLeftFlipper/NoUpperRightFlipper. de.vbs can therefore write 86/88 on staged keys, but no upper flipper is fitted and the eight-bit Data East matrix-strobe read cannot reach that column. The unused flipper-column records explain the distinction.
"""


def owner_excerpt() -> str:
    return """# Phantom of the Opera knocker fitment: owner observations

Source: https://pinside.com/pinball/forum/topic/phantom-of-the-opera-where-is-the-knocker-located , retained JSON capture SHA-256 ad9d5ebc5811d7a869f7aedbb0daa0a38f49c890638fd10dbfd46d3d0bb7161c, acquired 2026-11-06T13:12:53Z. Attribution: named Pinside contributors. License/rights: NOASSERTION, original rights retained. Method: direct read/paraphrase by project curator, reviewed. No photograph or whole page is redistributed.

The topic began with Pintucky buying replacement hardware and discovering no installation to replace. Timerider (#10) independently reports that his machine had no mechanism, strike plate, spare holes or wiring. Schusler (#11) confirms absent hardware and notes the manual/schematic omission. Pintucky's follow-up (#15, https://pinside.com/pinball/forum/topic/phantom-of-the-opera-where-is-the-knocker-located#post-632114) still found no installation trace. AndHart120 (#6) reports the same absence on his machine. These direct inspections support the own-game PPB connector list's N.U. R08 branch; the first generic suggestion to look in a Data East backbox is not machine-specific evidence.

This settles physical non-fitment of a production knocker. Physical absence alone does not classify the emulator state published at 32; that requires the separately retained service evidence.
"""


def controller_excerpt(data: dict) -> str:
    text = """# Phantom of the Opera controller construction

Sources: manual PDF 2 / red insert printed i, CPU Jumper Table; PDF 42 / printed 38 cabinet drawing; PDF 51 / printed 46 CPU Board Assembly Drawing; PDF 53 / printed 48 CPU logic sheet 2; pinned s11.h, s11.c and degames.c. Direct visual/code read by project curator; reviewed. The accompanying tight crop shows the entire relevant PIA11B PA7 net, including the jumper path previously omitted from the transcription.

CPU PIA11B PA7 pin 9 connects both to a +5V pull-up through RA4, 4.7K, and to two circle terminals with a dashed jumper link to ground, labelled J8. The rotated designator reads J8; the CPU Board Assembly Drawing independently labels that jumper position J8. RA3, 4.7K x8, is the neighboring port-B pull-up array, not the PA7 resistor. With J8 installed the net is grounded; with it removed RA4 pulls it high. The complete CPU Jumper Table below explicitly lists J8 installed for Phantom of the Opera, CPU Ver 2, ROMs 5B,5C. This is documented factory configuration, not a survey of every surviving board.

The inherited s11 machine driver declares one DIP-style bit, and pia2a_r returns core_getDip(0)<<7. Thus public bit 0 at value 0 supplies low PA7, corresponding to the documented grounded J8 configuration; value 1 supplies high PA7, corresponding electrically to removing J8. S11_COMPORTS declares a Country input; DE_COMPORTS used by poto does not. Neither this transport nor the jumper drawing establishes Phantom's firmware purpose. Do not rename J8 as Williams W7 or assert a Country function without game-specific evidence. The definition retains an input_semantics blocker for the unresolved firmware interpretation.

The cabinet drawing depicts open STEP and Forward/Reverse contacts into CN14 (STEP pin 4, BLU; Forward/Reverse pin 3, GRN; common ground pin 2, WHT). The CPU logic sheet 1 inverts both through LS02 gates before the PIA control inputs. The emulator presents public Advance inverted to PIA2 CA1 and Up/Down directly to CB1; consume its public states as delivered. Physical normally-open construction is separate from the maintained/toggled service convention.
"""
    text += "\n## Complete CPU Jumper Table\n\n"
    text += "| Game | CPU* Version | ROM Location | Jumpers Installed | Jumpers Removed |\n"
    text += "| --- | --- | --- | --- | --- |\n"
    text += "".join("| " + " | ".join(row) + " |\n" for row in data["cpu_jumper_table"])
    text += "\nThe blank second Game cell belongs to the merged Laser Wars entry. Printed comma separators, ampersands, case and the unlettered J5/J6 entries are retained; surrounding table spacing is normalized.\n\n"
    text += "*Version 1 has a 2K RAM which is a 24-pin IC at location 5D.\n\n"
    text += "*Version 2 has an 8K RAM which is a 28-pin IC at location 5D.\n"
    return text


def playfield_parts_excerpt(data: dict) -> str:
    lines = [
        "# Phantom of the Opera complete Playfield Parts list", "",
        "Source: " + data["locators"]["playfield_parts"] + ".", "",
        "Method: direct visual transcription by project curator from the native-resolution page; reviewed. Both printed columns are transcribed, rows 1-18 at left and 19-74 at right. Fraction glyphs use plain-text fractions; line wrapping and column spacing are normalized. Printed descriptions, parenthesized counts, part numbers and the spelling Guage are retained. The adjacent location drawing is not reproduced or used here as registered geometry.", "",
        "| Number | Description | Part Number |", "| --- | --- | --- |"
    ]
    lines.extend("| " + " | ".join(map(str, row)) + " |" for row in data["playfield_parts"])
    lines += ["", "Row 1 supplies the Organ Motor part 041-5001-00; the motor/bracket drawing separately identifies motor assembly 515-5256-00-08 and complete mechanism 500-5212-00-08. These part numbers describe different levels of assembly."]
    return "\n".join(lines) + "\n"


def output20_excerpt() -> str:
    return f"""# Phantom output 20: bounded ROM analysis

Method: direct source/decoded-instruction review by project curator. Reviewed: yes. No ROM execution, complete reachability proof, or Ghidra decompilation is claimed. External analysis manifest SHA-256: {ROM_ANALYSIS_SHA}; exact tools, source hashes, decoder scripts and instruction windows remain in external:pinmame-review-artifacts/phantom-of-the-opera-1990/output20-re/.

Target: authorized poto_a32.zip SHA-256 7e90f6a0547d1a83b6aff8492ba0f0e8767a0f87345b9c2b47095a78764bf4e7. DE_ROMSTART48 loads potob5.3-2 at $4000 (16384 bytes; SHA-256 8cc90253c0d4808865eebb6d6d9a009703706e8f8012dda574d0fd3a4ff3e952) and potoc5.3-2 at $8000 (32768 bytes; SHA-256 406dba207a46c69301e6bb13a3b9cc6f27e0987e75eeceb5297b011ef89a43df). Python 3.13.5 used the opcode metadata from pinned PinMAME 6800dasm.c. Its SHA-256 is c2bd5d12fa01b9543529471f83b3cfd966a956e50bdcf1cec80b1353de0557a2. All source is pinned to {PIN}.

Source contract: s11.c maps PIA1 to $2400-$2403 in standard order, so CRA is $2401. Its CA2 callback calls setSSSol(data,0); Data East permutation index 3 plus CORE_FIRSTSSSOL 17 selects public 20. Low requests activation, gated by ssEn. PIA0 CB2 at $2103 controls that enable. The alpha ssSw array supplies no switch-synthesis route for SP6.

Observed static bytes, decoded without byte columns: reset initializes shadow $0102 to $38 at $42E2. Routine $4C29, called at reset $42F4 and periodically from IRQ $435A, loads that shadow and stores it to CRA at $4C96 with bit 2 cleared, then $4CA3 with bit 2 set. These are the only raw extended stores found to CRA; the only raw extended shadow references are the initialization and two reads. Conditional inference: if the shadow remains $38, CRA receives $38/$3C, both CA2 high/inactive in set/reset mode. No startup activation follows from these writes.

The adjacent indexed PIA test can write $31/$39/$35/$3D through STA 0,X at $4294. Starting PIA1 at X=$2403 eventually reaches CRA $2401. Its preceding PIA0 CB2 test ends high, disabling ssEn before the straight-line PIA1 test; the ending high request also clears the stored special bit. This sequence does not establish a published output 20 pulse. Normal reset skips the test with a jump at $4242 to $42CC; alternate reachability and interleaving were not proved.

Coverage limit: vector-seeded direct flow covers 623 instruction starts and reaches event dispatch $45ED, JSR 0,X, with the target loaded from an event structure. Dynamic targets and indexed-store base/value ranges were not resolved. Extended-address scans do not rule out an indirect write to $0102 or $2401. Availability remains unknown. The remaining proof is to resolve those dispatch targets and indexed writes; quiet service/gameplay traces and physical non-fitment alone do not prove unused state. ROM bytes and raw byte columns are not redistributed.
"""


def excerpts(data: dict) -> dict[Path, str]:
    return {
        EXCERPTS / "playfield-parts.md": playfield_parts_excerpt(data),
        EXCERPTS / "output20-rom-analysis.md": output20_excerpt(),
        EXCERPTS / "controller-contract.md": controller_excerpt(data),
        EXCERPTS / "switch-matrix.md": matrix_excerpt(data, "switch"),
        EXCERPTS / "lamp-matrix.md": matrix_excerpt(data, "lamp"),
        EXCERPTS / "coil-and-flipper.md": coil_excerpt(data),
        EXCERPTS / "mechanism-construction.md": organ_excerpt(),
        EXCERPTS / "script-bindings.md": script_excerpt(),
        EXCERPTS / "vpm-script-library-flippers.md": library_excerpt(),
        EXCERPTS / "knocker-owner-inspections.md": owner_excerpt()
    }


def source_excerpt(path: Path, value: str, locator: str) -> dict:
    result = {
        "id": "excerpt.phantom." + path.stem,
        "locator": locator,
        "path": path.as_posix(),
        "sha256": hashlib.sha256(value.encode()).hexdigest(),
        "method": "manual",
        "transcribed_by": "project curator",
        "reviewed": True
    }
    if path.stem == "mechanism-construction":
        result.update(
            image=(EXCERPTS / "organ-drive-assembly.webp").as_posix(),
            image_sha256="a9eefdec8f4842f71b49e5263a3a2b9eb0b15baa967186548f4990e898e4e91a",
            image_derivation=
            "Data_East_1990_Phantom_of_the_Opera_English_Manual_with_paginated_schematics.pdf page 39, crop box 0.08,0.08,0.92,0.37, scanned page rendered at its native resolution (embedded image xref 79, 1700px across 23.61in), rendered at 72 dpi, grayscale, 1428x638 WebP quality 80"
        )
    if path.stem == "controller-contract":
        result.update(
            image=(EXCERPTS / "cpu-pia-pa7.webp").as_posix(),
            image_sha256="de65dda8b7650ed69fc9ded384f600c94aacc298ffd6a67875b3e29f65e6b9e5",
            image_derivation=
            "Data_East_1990_Phantom_of_the_Opera_English_Manual_with_paginated_schematics.pdf page 53, crop box 0.2,0.2,0.47,0.43, scanned page rendered at its native resolution (embedded image xref 106, 3307px across 45.93in), rendered at 72 dpi, grayscale, 894x509 WebP quality 80"
        )
    return result


def sources(data: dict) -> list[dict]:
    ex = excerpts(data)
    result = [
        {
            "id": CATALOG,
            "kind": "pinmame_catalog",
            "uri": "https://github.com/vpinball/pinmame",
            "revision": PIN,
            "locator": "PinmameGetGames; degames.c:300-325 poto_a32/poto_a31/poto_a29",
            "license": "BSD-3-Clause",
            "attribution": "PinMAME contributors"
        },
        {
            "id": CORE,
            "kind": "pinmame_core",
            "uri": "https://github.com/vpinball/pinmame/tree/" + PIN,
            "revision": PIN,
            "locator": "src/wpc/degames.c:77-83,300-325 INITGAMES11(poto); de_dispAlpha3; src/wpc/s11.c pia4a_r, setSSSol, updsol, MACHINE_INIT(s11) poto block; core.c core_updateSw/core_getSol; core.h; LICENSE:4-18 per-file first-line markers (core.c and core.h are unmarked)",
            "license": "PinMAME license",
            "attribution": "PinMAME contributors"
        },
        {
            "id": MANUAL,
            "kind": "manual",
            "uri": f"https://www.ipdb.org/files/1777/{MANUAL_FILE}",
            "source_id": "1777",
            "original_filename": MANUAL_FILE,
            "sha256": MANUAL_SHA,
            "locator": "IPDB 1777, https://www.ipdb.org/machine.cgi?id=1777; " +
            "; ".join(data["locators"].values()),
            "acquired_at": "2026-11-06T13:06:21Z",
            "license": "NOASSERTION",
            "rights": "Original copyright retained; whole manual retained locally, not redistributed",
            "attribution": "Data East Pinball, Incorporated; Inkochnito scan assembly; Internet Pinball Database hosting",
            "excerpts": [
                source_excerpt(p, t, data["locators"][key])
                for p, t, key in [(EXCERPTS / "switch-matrix.md", ex[EXCERPTS / "switch-matrix.md"],
                                   "switch_matrix"),
                                  (EXCERPTS / "lamp-matrix.md", ex[EXCERPTS / "lamp-matrix.md"],
                                   "lamp_matrix"),
                                  (EXCERPTS / "coil-and-flipper.md", ex[EXCERPTS / "coil-and-flipper.md"],
                                   "coils"),
                                  (EXCERPTS / "mechanism-construction.md",
                                   ex[EXCERPTS / "mechanism-construction.md"], "organ"),
                                  (EXCERPTS / "playfield-parts.md",
                                   ex[EXCERPTS / "playfield-parts.md"], "playfield_parts")]
            ]
        },
        {
            "id": TABLE,
            "kind": "vpx_table",
            "uri": "https://vpuniverse.com/files/file/17168-phantom-of-the-opera-data-east-1990/",
            "sha256": TABLE_SHA,
            "original_filename": TABLE_FILE,
            "locator": "Version 1.25, extracted/gamedata.json bounds 0,0..952,2162 and extracted/gameitems; vpxtool git:v0.33.3",
            "known_working": True,
            "acquired_at": "2026-11-06T13:04:47Z",
            "license": "NOASSERTION",
            "attribution": "TastyWasps; original 32assassin; DCrosby; Cirque; Hauntfreaks; redbone; VPW testing",
            "excerpts": [
                source_excerpt(EXCERPTS / "script-bindings.md", ex[EXCERPTS / "script-bindings.md"],
                               "Embedded script and its exact bound gameitems; rejected helpers documented")
            ]
        },
        {
            "id": SCRIPT,
            "kind": "vpx_script",
            "uri": "external:pinmame-vpx-sources/data-east/phantom-of-the-opera-1990/extracted/script.vbs",
            "sha256": SCRIPT_SHA,
            "locator": "Embedded script from exact retained VPX 1.25; line references in excerpt; vpxtool git:v0.33.3",
            "known_working": True,
            "acquired_at": "2026-11-06T13:04:47Z",
            "license": "NOASSERTION",
            "attribution": "TastyWasps and contributors credited in retained script",
            "excerpts": [
                source_excerpt(
                    EXCERPTS / "script-bindings.md", ex[EXCERPTS / "script-bindings.md"],
                    "script.vbs:58-68,133-160,263-304,342-355,473-746,757-896,1175-1202,3185-3373")
            ]
        },
        {
            "id": EXTRACTION,
            "kind": "human_review",
            "uri": "external:pinmame-vpx-sources/data-east/phantom-of-the-opera-1990/extracted/manifest.json",
            "sha256": MANIFEST_SHA,
            "locator": "2699 files, 272164712 bytes; build_external_evidence_manifest.py v1: case-sensitive sorted relative POSIX paths with byte size/SHA256, JSON sorted keys/compact separators/ensure_ascii=False plus LF; manifest.json and manifest.sha256 excluded",
            "acquired_at": "2026-11-06T13:04:47Z",
            "license": "NOASSERTION",
            "attribution": "Derived extraction integrity manifest; original asset rights retained"
        },
        {
            "id": LIBRARY,
            "kind": "vpx_script",
            "uri": "external:pinmame-vpx-sources/data-east/phantom-of-the-opera-1990/de.vbs",
            "sha256": DE_VBS_SHA,
            "locator": "de.vbs Last Updated in VBS v3.61; core.vbs SHA256:" + CORE_VBS_SHA,
            "license": "NOASSERTION",
            "attribution": "VPinMAME script library contributors",
            "acquired_at": "2026-11-06T13:04:47Z",
            "excerpts": [
                source_excerpt(EXCERPTS / "vpm-script-library-flippers.md",
                               ex[EXCERPTS / "vpm-script-library-flippers.md"],
                               "de.vbs:33-36,62-122 and core.vbs cvpmFlips2.Init/vpmInit/flipper constants")
            ]
        },
        {
            "id": OWNERS,
            "kind": "human_review",
            "uri": "https://pinside.com/pinball/forum/topic/phantom-of-the-opera-where-is-the-knocker-located",
            "sha256": PIN_SIDE_SHA,
            "locator": "Direct owner inspections, posts 6, 10, 11, 15; retained pinside-knocker-page.json",
            "license": "NOASSERTION",
            "attribution": "AndHart120, Timerider, Schusler, Pintucky via Pinside",
            "acquired_at": "2026-11-06T13:12:53Z",
            "excerpts": [
                source_excerpt(EXCERPTS / "knocker-owner-inspections.md",
                               ex[EXCERPTS / "knocker-owner-inspections.md"],
                               "posts 6, 10, 11, 15; exact post 15 URL in excerpt")
            ]
        },
        {
            "id": IPDB,
            "kind": "human_review",
            "uri": "https://www.ipdb.org/machine.cgi?id=1777",
            "sha256": "b3ec2991bbf25a0a9696595cb2c8cbd84efd5c144a868359ed550cc4bb53c0be",
            "locator": "Verified title Phantom of the Opera, Data East, January 1990, model 500-5508-01; early-production speaker-note distinguished from production hardware",
            "license": "NOASSERTION",
            "attribution": "Internet Pinball Database contributors"
        },
    ]
    manual_record = next(item for item in result if item["id"] == MANUAL)
    manual_record["excerpts"].append(
        source_excerpt(EXCERPTS / "controller-contract.md", ex[EXCERPTS / "controller-contract.md"],
                       data["locators"]["controller"] + "; PDF42/printed38 cabinet"))
    result.append({
        "id": ORGAN,
        "kind": "runtime_scenario",
        "uri": ORGAN_EVIDENCE.as_posix(),
        "sha256": ORGAN_SHA,
        "revision": PIN,
        "locator": "Five fresh-state poto_a32 probes: closed/midway initial crank x narrow/wide candidate limit pattern plus open-contact jam; exact raw hashes, binary/ROM hashes, scenarios and synthetic-model limits in compact evidence",
        "license": "NOASSERTION",
        "attribution": "Authorized local ROM; PinMAME contributors; project curator synthetic host model",
        "acquired_at": "2026-11-06T13:34:48Z"
    })
    result.append({
        "id": SERVICE,
        "kind": "runtime_scenario",
        "uri": SERVICE_EVIDENCE.as_posix(),
        "sha256": SERVICE_SHA,
        "revision": PIN,
        "locator": "Two successful fresh-state all-direct poto_a32 runs; external:pinmame-review-artifacts/phantom-of-the-opera-1990/runtime/direct1/run.json and direct2/run.json. Exact raw/scenario/manifest/ROM/binary hashes and per-address segment frames are retained in the compact evidence; builder tools/build_phantom_runtime_evidence.py.",
        "license": "NOASSERTION",
        "attribution": "Authorized local ROM; PinMAME contributors; locally captured diagnostic display segments"
    })
    result.append({
        "id": ROM_ANALYSIS,
        "kind": "human_review",
        "uri": "external:pinmame-review-artifacts/phantom-of-the-opera-1990/output20-re/manifest.json",
        "sha256": ROM_ANALYSIS_SHA,
        "revision": PIN,
        "locator": "Bounded poto_a32 static review: PIA1 CRA $2401, shadow $0102, stores $4C96/$4CA3, gated indexed PIA test, unresolved $45ED event dispatch. Exact input/member/source hashes and decoder limitations in retained analysis.",
        "license": "NOASSERTION",
        "attribution": "project curator direct review of authorized local ROM and pinned PinMAME source; no ROM redistribution",
        "excerpts": [source_excerpt(EXCERPTS / "output20-rom-analysis.md",
                                    ex[EXCERPTS / "output20-rom-analysis.md"],
                                    "analysis.md; identity.json; shadow-and-call-windows.asm; pinned s11.c/s11.h/6821pia.c/6800dasm.c")]
    })
    return result


def inputs(data: dict, places: dict) -> list[dict]:
    descriptions = {int(row[0].rstrip("*")): row for row in data["switch_descriptions"]}
    result = []
    for n, printed in enumerate(data["switch_matrix"], 1):
        unused = printed == "Not Used"
        desc = descriptions.get(n, [str(n), printed, "--"])
        label = f"Unused Switch {n}" if unused else desc[1]
        if n in (15, 16):
            label = ("Left" if n == 15 else "Right") + " Flipper Button (FLIP1516 copy)"
        item = {
            "id": f"switch.matrix-{n}",
            "label": label,
            "kind": "switch",
            "binding": {
                "group": "pinmame.input.switch",
                "device": n
            },
            "aliases": aliases("pinmame.switch", n, str(n)),
            "availability": "unused" if unused else "used",
            "physical": {
                "notes": (f"Manual matrix prints {printed}; description list prints {desc[1]}."
                          if n in descriptions else
                          f"Manual matrix prints {printed}; description list row 54 reads Not Used Through 64.")
            },
            "provenance": prov(MANUAL, CORE, *([] if unused else [SCRIPT]))
        }
        if unused:
            item["spatial"] = na("unused", MANUAL, CORE)
        else:
            col, row = divmod(n - 1, 8)
            item["physical"]["quantity"] = 1
            if not desc[2].startswith("See"):
                item["physical"]["part_number"] = desc[2]
            item["wiring"] = {
                "board": "CPU Board",
                "drive_wire": data["switch_drives"][col][0],
                "return_wire": data["switch_returns"][row][0],
                "driver_transistor": data["switch_drives"][col][2],
                "drive_connection": f"CPU CN8-{[1,2,3,4,5,7,8,9][col]}",
                "return_connection": f"CPU CN10-{[9,8,7,6,5,3,2,1][row]}"
            }
            if n not in (15, 16):
                item["normally_closed"] = False
                item["physical"][
                    "notes"] += " The game's matrix schematic draws an open contact, the zero-inversion Data East pia4a_r read is uninverted, and the retained script asserts public 1 for closure."
            if n in {1, 3, 4, 5, 6, 7, 15, 16}:
                item["physical"]["location"] = "cabinet"
                item["spatial"] = na("cabinet_or_service", MANUAL, CORE)
            elif str(n) in places["switches"]:
                p = places["switches"][str(n)]
                item["spatial"] = located(item["id"], [p], "sensor")
                item["physical"][
                    "notes"] += f" VPX anchor {p['object']} ({p['file']}); sensor/effect projection where the object represents a ball-contact assembly rather than the contact body."
            if n in (11, 12, 13, 53): item["initial_active"] = True
            if n == 52: item["initial_active"] = False
            if n in (15, 16):
                item["physical"][
                    "notes"] += f" Pinned core_updateSw overwrites this matrix address from the cabinet flipper column ({84 if n==15 else 82}); drive that column address. This is no independently writable EOS input."
            if n in (21, 22):
                item["physical"][
                    "notes"] += " The two printed contacts are a special-coil trigger and a matrix point switch. One public matrix input does not count both physical contacts as two colocated matrix sensors."
            if n in (28, 29):
                item["physical"][
                    "notes"] += " The two physical left-VUK ball contacts are represented by bsSaucer slots 1/2; only its mouth sw28 is modelled. Switch 29 has no independent retained-table sensor coordinate."
            if n in (36, 44):
                item["physical"][
                    "notes"] += " The table's occupied VUK kicker is a defensible projection for the internal ball contact, not a measured switch-body mounting point."
            if n in (37, 45):
                item["physical"][
                    "notes"] += " The invisible enabled subway trigger is collision geometry bound by executable code, not a visible socket; its sensor coordinate remains observed."
            if n in (1, 7):
                item["physical"][
                    "notes"] += " The table vpmNudge.TiltSwitch=7 asserts Slam Tilt for a nudge rather than physical Plumb Tilt 1; this table defect does not rename the hardware contacts."
            if n in (52, 53):
                item["physical"][
                    "notes"] += " Motor/bracket 500-5212-00-08 contains two 180-5052-00 limit switches. The manual's Organ Test says both contacts are electrically open midway and each closes before its endpoint. The table counter supplies feedback, not physical sensor coordinates."
        result.append(item)
    for n, label in [(-7, "Black STEP / Advance Button"), (-6, "Green Forward/Reverse Button")]:
        result.append({
            "id": f"switch.diagnostic-{abs(n)}",
            "label": label,
            "kind": "switch",
            "binding": {
                "group": "pinmame.input.switch",
                "device": n
            },
            "aliases": aliases("pinmame.switch", n),
            "availability": "used",
            "normally_closed": False,
            "physical": {
                "location": "coin door",
                "notes": "Own-game cabinet drawing shows an open contact; the Green Forward/Reverse button is maintained/toggled in the DE_COMPORTS and de.vbs public contract. A public inactive/active level is not by itself a physical construction measurement."
            },
            "spatial": na("cabinet_or_service", MANUAL, CORE, LIBRARY),
            "provenance": prov(MANUAL, CORE, LIBRARY)
        })
    result.append({
        "id": "dip.emulator-configuration-0",
        "label": "CPU PA7 Jumper J8 (firmware purpose unresolved)",
        "kind": "dip_switch",
        "binding": {
            "group": "pinmame.input.dip",
            "device": 0
        },
        "aliases": aliases("pinmame.dip", 0),
        "availability": "used",
        "physical": {
            "quantity": 1,
            "location": "CPU board in backbox",
            "notes": "The own-game schematic draws J8 from PIA11B PA7 pin 9 to ground, with a parallel RA4 4.7K pull-up to +5V. The CPU Jumper Table documents J8 installed for Phantom CPU Ver 2, ROMs 5B,5C, hence a grounded PA7 factory configuration. The inherited pia2a_r returns core_getDip(0)<<7: public configuration bit 0 at value 0 matches that grounded net, and value 1 matches the removed-jumper high level. This is a jumper position, not a physical DIP-switch bank. Its firmware purpose remains unresolved; DE_COMPORTS declares no Country port and the inherited Williams Country/W7 label is not game-specific evidence. Documented factory installation is not a claim about every surviving board."
        },
        "spatial": na("dip_switch", CORE, MANUAL),
        "provenance": prov(CORE, MANUAL, status="candidate")
    })
    result += flipper_column_inputs(
        flip_swno=(15, 16),
        flip_swno_text="FLIP1516 = FLIP_SWNO(15,16)",
        core_refs=(CORE, ),
        button_refs=(MANUAL, SCRIPT, LIBRARY),
        button_notes={
            "left": "The de.vbs key handler writes 84; the own-game cabinet drawing shows the normally-open button contact.",
            "right": "The de.vbs key handler writes 82; the own-game cabinet drawing shows the normally-open button contact."
        },
        button_normally_closed=False,
        unused_notes=vpm_staged_flipper_notes(library="DE.VBS"),
        unused_note_refs=(LIBRARY, SCRIPT))
    return result


def outputs(data: dict, places: dict) -> list[dict]:
    result = []
    for n, label in enumerate(data["lamp_descriptions"], 1):
        unused = n == 56
        col, row = divmod(n - 1, 8)
        item = {
            "id": f"lamp.matrix-{n}",
            "label": f"Unused Lamp {n}" if unused else label,
            "kind": "lamp",
            "binding": {
                "group": "pinmame.output.lamp",
                "device": n
            },
            "aliases": aliases("pinmame.lamp", n, str(n)),
            "availability": "unused" if unused else "used",
            "physical": {
                "notes": f"Manual matrix label: {data['lamp_matrix'][n-1]}; own-game description: {label}."
            },
            "wiring": {
                "board": "CPU Board",
                "drive_wire": data['lamp_drives'][col][0],
                "return_wire": data['lamp_returns'][row][0],
                "driver_transistor": data['lamp_drives'][col][2] + " / " + data['lamp_returns'][row][2],
                "drive_connection": f"CPU CN7-{[1,2,3,4,6,7,8,9][col]}",
                "return_connection": f"CPU CN6-{[1,2,3,5,6,7,8,9][row]}"
            },
            "provenance": prov(MANUAL, SCRIPT)
        }
        if unused:
            item['spatial'] = na("unused", MANUAL)
            item['physical'][
                'notes'] += " Both own-game lists say Unused. The generic matrix-symbol schematic and leader-less 56 on the location drawing do not establish fitment."
        else:
            item['physical']['quantity'] = 1
            if n in BACKBOX_LAMPS:
                item['physical']['location'] = 'backbox insert panel'
                item['physical'][
                    'notes'] += ' Off-table invisible table light is a backglass helper, not playfield geometry.'
                item['spatial'] = na('cabinet_or_service', MANUAL, SCRIPT)
            elif 49 <= n <= 55:
                item['physical']['location'] = 'upright rear playfield panel'
                item['physical'][
                    'notes'] += ' The own-game location drawing orders seven PHANTOM sockets on the rear panel. The table drives Flasher sprites f49-f55, which do not establish socket centers; no invented coordinates are assigned.'
            else:
                p = places['lamps'][str(n)]
                item['spatial'] = located(item['id'], [p], 'emitter', status='candidate')
                item['physical'][
                    'notes'] += f" Table {p['object']} is the script-bound insert light; it has no shown bulb mesh. This coordinate is an insert-center projection candidate, not an observed socket."
        if n == 25:
            item['physical'][
                'notes'] += ' The description lists and left-side location drawing settle the matrix Right Circle misprint as Left Circle.'
        if n == 53:
            item['physical'][
                'notes'] += ' The extra script binding NfadeL53,S108b1 and organ animation writes are a lighting defect; that organ helper is excluded from this rear-panel lamp.'
        result.append(item)
    rows = {r[0]: r for r in data['driver_rows']}
    for n in range(1, 51):
        item = {
            'id': f'coil.driver-{n}',
            'label': f'Unused Solenoid {n}',
            'kind': 'virtual',
            'binding': {
                'group': 'pinmame.output.solenoid',
                'device': n
            },
            'aliases': aliases('pinmame.solenoid', n),
            'availability': 'unused',
            'physical': {
                'notes': 'Pinned core exposes no populated game-specific device here.'
            },
            'spatial': na('unused', CORE),
            'provenance': prov(CORE)
        }
        if n in rows:
            r = rows[n]
            item['label'] = r[1].title()
            item[
                'kind'] = 'flasher' if n in FLASH else 'relay' if n == 10 else 'gi' if n == 11 else 'motor' if n == 14 else 'coil'
            item['availability'] = 'used'
            item['provenance'] = prov(MANUAL, SCRIPT, CORE)
            item['physical'] = {
                'notes': f"Own-game schematic {r[1]}; public {n} is " +
                (f"SIDE L{n:02}." if n <= 8 else f"SIDE R{n-24:02}." if n >= 25 else f"printed {n:02}.")
            }
            item['aliases'] = aliases(
                'pinmame.solenoid', n,
                f'SIDE L{n:02}' if n <= 8 else f'SIDE R{n-24:02}' if n >= 25 else f'{n:02}')
            item['wiring'] = {
                'board': 'CPU / PPB',
                'driver_transistor': r[2],
                'control_wire': r[3],
                'control_connection': r[4],
                'drive_wire': r[5],
                'drive_connection': r[6]
            }
            item.pop('spatial')
            if n in FLASH:
                back = BACKBOX_FLASH[n]
                item['physical']['quantity'] = r[8]
                item['physical']['location'] = 'backbox' if back == r[
                    8] else 'playfield and backbox' if back else 'playfield'
                item['physical'][
                    'notes'] += f" Printed bulbs {r[7]}, total {r[8]}; backbox inset assigns {back}, leaving {r[8]-back} on the playfield. Table lighting simplifies the multi-bulb circuit; render lights and dome anchors do not supply missing socket positions."
                if back == r[8]: item['spatial'] = na('cabinet_or_service', MANUAL)
            elif n == 10:
                item['physical'][
                    'notes'] += ' K1 selects the alternate branch of shared drivers 1-8/25-32. The table also toggles GI from this callback; the physical wiring identifies 11 alone as the GI relay.'
                item['spatial'] = na('internal_nonvisual', MANUAL, CORE)
            elif n == 11:
                item['physical'][
                    'notes'] += ' The power-supply relay switches GI inversely (on means dark in the script). Its playfield/backbox/cabinet factory-socket inventory remains incomplete; no quantity is inferred from 32 collection entries. The twelve observed VPX bulb-mesh placements retain one member per render pair; GI_25 and bumper glows are excluded. Observing those meshes does not validate a complete physical socket inventory.'
                item['spatial'] = located(item['id'],
                                          places['gi_bulb_candidates'],
                                          'emitter',
                                          status='observed')
            elif n == 14:
                motor_part = next(row[2] for row in data['playfield_parts'] if row[0] == 1)
                item['physical'].update(part_number=motor_part,
                                        assembly_part_number='500-5212-00-08',
                                        quantity=1,
                                        location='organ mechanism, upper right playfield')
                item['physical'][
                    'notes'] += ' The complete Playfield Parts list, PDF33/printed29 row 1, supplies Organ Motor 041-5001-00. Q25 energizes the motor relay board, switching 25 VAC to the crank motor. Switch 52 is Open; 53 Closed. No independent direction output or measured motor speed is declared.'
                item['wiring'].update(nominal_voltage_v=25, voltage_type='ac')
            else:
                item['physical'].update(part_number=r[7], quantity=1)
                p = EFFECT_ANCHORS[n] if n in EFFECT_ANCHORS else places['switches'][str({
                    25: 10, 27: 28, 28: 36, 29: 44
                }[n])]
                item['spatial'] = located(item['id'], [p], 'effect')
                item['physical'][
                    'notes'] += f" Effect/assembly projection on {p['object']}; not an observed under-playfield coil-body mount."
                if n == 26:
                    item['physical']['assembly_part_number'] = '500-5012-00'
                    item['physical'][
                        'notes'] += ' ballreleasehack overrides the direct callback and suppresses the table final-ball serve unless its left saucer has two balls; do not turn that workaround into a physical interlock.'
                if n == 25:
                    item['physical']['assembly_part_number'] = '500-5082-00'
                    item['physical'][
                        'notes'] += ' The script directly removes drain balls into its virtual trough; its bsTrough.SolIn callback is not a faithful physical outhole simulation.'
        elif n in SPECIAL_PUBLIC:
            sp = SPECIAL_PUBLIC[n]
            r = data['special_coils'][sp - 1]
            item['label'] = r[1] if sp != 6 else 'Unfitted Special-Solenoid Driver SP6'
            item['aliases'] = aliases('pinmame.solenoid', n, r[0])
            item['provenance'] = prov(MANUAL, CORE)
            item['availability'] = 'unknown' if sp == 6 else 'used'
            item['kind'] = 'virtual' if sp == 6 else 'coil'
            item['physical'] = {
                'notes': f"Printed {r[0]}; s11.c handler slots 0-5 name SP6,SP5,SP2,SP3,SP1,SP4 and apply the Data East permutation 3,4,5,1,0,2. This derives public {n} from the own-game wiring, not from sequential SP numbering. INITGAMES11 leaves ssSw empty, so PinMAME does not synthesize switch-triggered alpha firings. The table performs its own sling/bumper physics."
            }
            item['wiring'] = {'board': 'CPU Board', 'driver_transistor': r[6]}
            if sp != 6:
                item['physical'].update(part_number=r[7], quantity=1)
                item['wiring'].update(control_wire=r[2],
                                      control_connection=r[3],
                                      drive_wire=r[4],
                                      drive_connection=r[5],
                                      power_wire='RED',
                                      power_connection='PS CN3-6')
                item['spatial'] = located(item['id'], [places['switches'][str(SPECIAL_SWITCH[sp])]], 'effect')
                item['physical'][
                    'notes'] += ' The contact/coil on the named bumper or sling is a physical direct reflex; the public address may remain quiet in play. The special drawing prints CN16 on its trigger header where the own-game table/backbox list print CN18; wiring-note disagreement only.'
            else:
                item['physical'][
                    'notes'] += ' The manual fits no coil. Bounded ROM analysis accounts for CRA $2401 stores from shadow $0102 initialized to $38: $38/$3C hold CA2 inactive. The adjacent indexed PIA test is gated off in its straight-line sequence. Event dispatch $45ED and indexed-store ranges remain unresolved, so no-load and quiet traces are not promoted to constant-zero proof.'
                item['provenance']['source_refs'].append(ROM_ANALYSIS)
                item['spatial'] = na('no_physical_device', MANUAL, CORE)
        elif n == 23:
            item.update(label='Game On / Flipper and Special-Solenoid Enable',
                        kind='control_signal',
                        availability='used',
                        spatial=na('internal_nonvisual', CORE))
            item['physical'][
                'notes'] = 'Public 23 is the shared enable state consumed by core_updateSw; no independent playfield coil exists at this address.'
        elif n in (30, 31, 32):
            item.update(label=f'Unfitted Mux Branch R{n-24:02}',
                        availability='unused',
                        spatial=na('no_physical_device', MANUAL, CORE, OWNERS, SERVICE))
            item['provenance'] = prov(MANUAL, CORE, SCRIPT, OWNERS, SERVICE)
            item['physical'][
                'notes'] = 'The own-game PPB J2 list marks the branch N.U. and draws no load. The ROM service sweep names it UNUSED COIL and pulses it in its R-bank test sequence; this explains the public state without fitting a physical load. '
            if n == 32:
                item['physical'][
                    'notes'] += 'Multiple owners found no knocker, mounting traces or wiring. The table adds a knocker sound; its callback does not prove a physical coil. The isolated R08 location label is weaker than the connector/wiring evidence and direct owner inspections.'
        elif 45 <= n <= 48:
            side = 'Right' if n <= 46 else 'Left'
            phase = 'Power' if n % 2 else 'Hold'
            item.update(label=f'Synthetic {side} Flipper {phase}',
                        availability='used',
                        spatial=na('virtual', CORE, MANUAL))
            item['physical'][
                'notes'] = f'Emulator-generated {side.lower()} button-derived state; the machine has one 23-900 coil on this side. Do not count this as another physical winding output or driver transistor.'
            item['provenance'] = prov(CORE, MANUAL, LIBRARY)
        elif n == 49:
            item['physical'][
                'notes'] = 'Cross-platform simulator ball-shooter state. The physical machine has a manual plunger.'
        result.append(item)
    return result


def mechanisms() -> list[dict]:
    specs = [
        ('organ', 'Raising Organ and Cavern', 'motorized', [14], [37, 52, 53],
         "Upper-right ramp/hood pivots on its hinge and is moved by a rotary crank/25VAC motor through relay 14. Open 52 and Closed 53 are open midway, close before their respective endpoints and must not both close. The retained table starts closed (53 active), toggles direction in its animation on 14 pulses, and opens the collision path into the cavern. Its counter 0..60 is table tuning, not physical cam marks. Manual Organ Test pulses the relay while Start is held. Five fresh-state synthetic probes establish: startup with Closed 53 already active does not move; startup midway powers 14 until 53; completing 41-43 powers 14 until Open 52, then a timed return stops on 53. With both host limit inputs held open, three automatic attempts each stop after about six host-clock seconds rather than running indefinitely. In Organ Test, Start held produces repeated short pulses independent of those limits. Candidate cam width and powered speed were varied; neither is a physical measurement."
         ),
        ('left-vuk', 'Two-ball Left VUK / Lock', 'kicker', [27], [28, 29],
         "Two ball-presence contacts in one left-side stack; bsSaucer slots 1/2 assert 28/29, capacity two, one ball released by 27. Its mouth feeds the left wire ramp through a separate VPX raise helper; helper Kicker1 is not another physical actuator. Default empty. Exact physical sensor offsets remain unlocated."
         ),
        ('trough', 'Three-ball Trough and Outhole', 'kicker', [25, 26], [10, 11, 12, 13, 14],
         "Outhole 10 is recovered by 25 into the three-ball trough 11/12/13; 26 feeds the manual shooter lane 14. The table starts three balls in its stack (13,12,11 active), destroys drain balls into that model and maps 25 to its stack input. The two physical coils remain distinct. Script ballreleasehack is a recreation workaround, not physical wiring."
         ),
        ('top-super-vuk', 'Top Super VUK', 'kicker', [28], [36],
         "Below-playfield subway delivers a ball to occupied switch 36; 28 ejects it upward into its return path. The table clears 36 as it destroys/recreates/raises the ball before kicking it. Default empty. These teleport/height increments do not prescribe physical tuning."
         ),
        ('right-super-vuk', 'Right Super VUK / Magic Mirror Return', 'kicker', [29], [44, 45],
         "A ball through the spring-return hanging Magic Mirror enters the subway at 45 and reaches the right VUK contact 44. Output 29 ejects it back to the surface/return route. 45 is a ball-path switch, not directly actuated by 29. The table's BottomVUK/teleport helpers simplify this path; default empty."
         ),
        ('kickback', 'Left-outlane Laser Kick', 'kicker', [16], [17],
         "The left outlane ball switch 17 reports a ball. When ROM rules allow, 16 fires the kickback to return that ball to play; otherwise it drains. The script fires/pulls back Plunger1. A sensed ball does not mechanically force a coil command."
         ),
        ('left-sling', 'Left Slingshot', 'kicker', [18], [21],
         "Special SP3 drives the left sling 23-800 coil; the manual separately lists trigger and matrix-point contacts. A physical trigger reflex acts while enabled. PinMAME alpha omits ssSw synthesis, so the VPX sling collision both rebounds the ball and pulses 21."
         ),
        ('right-sling', 'Right Slingshot', 'kicker', [21], [22],
         "Special SP5 drives the right sling 23-800 coil with distinct trigger and point contacts; enabled hardware reflex. The VPX sling collision supplies physics and pulses 22 rather than awaiting an alpha special callback."
         ),
        ('left-bumper', 'Left Pop Bumper', 'kicker', [19], [46],
         "Special SP4, 23-800 coil, skirt/trigger and point contact on the left bumper. The retained Bumper1 pulses 46 and performs its own recoil/lighting."
         ),
        ('center-bumper', 'Center Pop Bumper', 'kicker', [22], [47],
         "Special SP2, 23-800 coil, skirt/trigger and point contact on the lower center bumper. The retained Bumper3 pulses 47; object numbering is not switch numbering."
         ),
        ('right-bumper', 'Right Pop Bumper', 'kicker', [17], [48],
         "Special SP1, 23-800 coil, skirt/trigger and point contact on the right bumper. The retained Bumper2 pulses 48."
         ),
        ('left-flipper', 'Left Cabinet-wired Flipper', 'other', [], [84],
         "One physical 23-900 coil on the solid-state flipper board drives the left bat. The normally-open cabinet microswitch writes public 84; core copies it to 15 and fabricates 47/48 while enabled 23. EOS/power/hold hardware must not be reconstructed as independent CPU outputs."
         ),
        ('right-flipper', 'Right Cabinet-wired Flipper', 'other', [], [82],
         "One physical 23-900 coil on the solid-state flipper board drives the right bat. The normally-open cabinet microswitch writes public 82; core copies it to 16 and fabricates 45/46 while enabled 23. PinMAME models no physical EOS contact here."
         )
    ]
    return [{
        'id': 'mechanism.' + key,
        'label': label,
        'kind': kind,
        'actuators': [f'coil.driver-{n}' for n in acts],
        'sensors': [f'switch.flipper-column-{n}' if n >= 81 else f'switch.matrix-{n}' for n in sens],
        'behavior': behavior,
        'provenance': prov(MANUAL, SCRIPT, CORE, *([ORGAN] if key == 'organ' else [])),
        **({
            'assembly_part_number': '500-5212-00-08',
            'positions': [{
                'id': 'closed',
                'label': 'Organ Closed',
                'sensors': ['switch.matrix-53']
            }, {
                              'id': 'open',
                              'label': 'Organ Open',
                              'sensors': ['switch.matrix-52']
                          }]
        } if key == 'organ' else {})
    } for key, label, kind, acts, sens, behavior in specs]


def attach_service_readings(machine: dict) -> dict:
    """Keep literal ROM names beside physical labels without promoting host inputs."""
    readings = load_json(ROOT / READINGS)
    groups = {
        'pinmame.input.switch': 'switch_test',
        'pinmame.output.lamp': 'lamp_test',
        'pinmame.output.solenoid': 'coil_test',
    }
    for device in machine['inputs'] + machine['outputs']:
        binding = device['binding']
        row = readings.get(groups.get(binding['group']), {}).get(str(binding['device']))
        if row is None:
            continue
        name, code = row['name'].strip(), row['code'].strip()
        device['aliases'].extend([
            {
                'namespace': 'rom.diagnostic.name',
                'value': name
            },
            {
                'namespace': 'rom.diagnostic.code',
                'value': code
            },
        ])
        device['physical']['notes'] += (
            f' Both fresh direct-switch service runs display {name!r}, code {code!r}. '
            'Names preserve the segment decoder glyphs; this does not establish physical construction or fitment.'
        )
        if SERVICE not in device['provenance']['source_refs']:
            device['provenance']['source_refs'].append(SERVICE)
    return machine


def build_machine() -> dict:
    data, places = load_json(ROOT / MANUAL_DATA), load_json(ROOT / PLACES)
    original = {
        "machine": {
            "id": ID,
            "name": "Phantom of the Opera",
            "manufacturer": "Data East",
            "year": 1990,
            "kind": "physical_pinball",
            "ipdb_id": 1777,
            "opdb_id": "Grq1D-MQokp"
        },
        "drivers": [
            dict(
                {
                    "id": name,
                    "description": "Phantom of the Opera, The (" + version + ")",
                    "year": "1990",
                    "manufacturer": "Data East",
                    "flags": 0
                }, **({
                    "clone_of": "poto_a32"
                } if name != "poto_a32" else {}))
            for name, version in (("poto_a29", "2.9"), ("poto_a31", "3.1"), ("poto_a32", "3.2"))
        ]
    }
    drivers = original['drivers']
    for d in drivers:
        d['physical_compatibility'] = 'identical'
        d['variant_notes'] = 'Production firmware revision ' + {
            'poto_a29': '2.9',
            'poto_a31': '3.1',
            'poto_a32': '3.2'
        }[d['id']] + '. Pinned degames.c shares the poto initializer, GEN_DE, FLIP1516, two 16-character rows, DE1S sound and all three sound ROMs; no controller or physical-layout override. Early promotional speaker/amplifier installations mentioned by IPDB are not another supported driver or playfield edition.'
    relations = flipper_column_relationships(flip_swno=(15, 16),
                                             matrix_ids={
                                                 15: 'switch.matrix-15',
                                                 16: 'switch.matrix-16'
                                             },
                                             refs=(CORE, ))
    return attach_service_readings({
        'format': 'pinmame-machine-definition',
        'schema_version': 2,
        'machine': {
            **original['machine'], 'model_number': '500-5508-01',
            'playfield': {
                'width': PLAYFIELD_WIDTH,
                'height': PLAYFIELD_HEIGHT,
                'units': 'vpx',
                'provenance': prov(TABLE)
            }
        },
        'controller': {
            'platform': 'pinmame.dataeast',
            'hardware_generation': '0x1000',
            'inversion_applied_by_emulator': True
        },
        'coverage': {
            'status': 'partial',
            'missing': MISSING,
            'dimensions': {
                'catalog_identity': 'validated',
                'address_enumeration': 'validated',
                'semantic_naming': 'candidate',
                'physical_wiring': 'validated',
                'mechanisms': 'validated',
                'variant_coverage': 'validated',
                'recreation_knowledge': 'validated',
                'spatial_placement': 'candidate'
            }
        },
        'drivers': drivers,
        'inputs': inputs(data, places),
        'outputs': outputs(data, places),
        'displays': [{
            'id': f'display.segment-{i}',
            'label': f'Player {1 if i==0 else 3}/{2 if i==0 else 4} alphanumeric row',
            'kind': 'segment',
            'controller_index': i,
            'segment_start': start,
            'width': 16,
            'physical_location': 'cabinet_or_service',
            'spatial': na('cabinet_or_service', MANUAL, CORE),
            'provenance': prov(MANUAL, CORE)
        } for i, start in enumerate((0, 20))],
        'mechanisms': mechanisms(),
        'relationships': relations,
        'sources': sources(data),
        'knowledge': {
            'path': KNOWLEDGE.as_posix(),
            'status': 'partial'
        },
        'conflicts': []
    })


def build_report(machine: dict) -> dict:
    placed = [
        d['id'] for d in machine['inputs'] + machine['outputs'] if d.get('spatial', {}).get('placements')
    ]
    unplaced = [d['id'] for d in machine['inputs'] + machine['outputs'] if 'spatial' not in d]
    return {
        'format': 'pinmame-spatial-blockers',
        'version': 1,
        'machine_id': ID,
        'coordinate_convention': 'x0 left, x1 right; y0 rear/backglass, y1 front/apron',
        'bounds': dict(PLAYFIELD_BOUNDS),
        'normalization': 'round((x-left)/(right-left),6), round((y-top)/(bottom-top),6); no axis flip',
        'evidence': {
            'table_sha256': TABLE_SHA,
            'script_sha256': SCRIPT_SHA,
            'manual_sha256': MANUAL_SHA,
            'extraction_manifest_sha256': MANIFEST_SHA,
            'extraction_files': 2699,
            'extraction_bytes': 272164712,
            'manifest_algorithm': 'tools/build_external_evidence_manifest.py:canonical_bytes(build_manifest(directory,poto_a32))+LF',
            'sources': {
                'vpx': 'external:pinmame-vpx-sources/data-east/phantom-of-the-opera-1990',
                'manual': 'external:pinmame-manuals/by-machine/' + ID + '/ipdb-1777/' + MANUAL_FILE
            }
        },
        'placed_devices': placed,
        'unplaced_devices': unplaced,
        'projections': [{
            'class': 'assembly-effect',
            'devices': ['coil.driver-' + str(n) for n in (16, 17, 18, 19, 21, 22, 25, 26, 27, 28, 29)],
            'status': 'observed',
            'rule': 'coil effect projected onto its own script-bound ball-contact assembly; no coil-body mount claimed'
        }, {
            'class': 'internal-ball-contact',
            'devices': ['switch.matrix-' + str(n) for n in (10, 28, 36, 44)],
            'status': 'observed',
            'rule': 'ball contact projected onto its own assembly mouth/kicker; no independent hidden contact geometry'
        }, {
            'class': 'insert-center',
            'devices': ['lamp.matrix-' + str(n) for n in [*range(1, 39), *range(41, 47), *range(57, 65)]],
            'status': 'candidate',
            'rule': 'script-bound Light is an insert overlay without shown bulb mesh, so it is not validated as a socket'
        }],
        'rejected_helpers': [
            'off-table L39/L40/L47/L48/S101a', 'f49-f55 back-wall Flasher sprites',
            'S108b1 organ glow from matrix53', 'GI odd render doubles,GI_25 and bumper glows',
            'Flupper flare/bloom/light render components as extra bulbs',
            'Kicker1/Kicker2/Kicker3 as extra physical actuators'
        ],
        'blockers': [{
            'dimension': 'input_semantics',
            'devices': ['dip.emulator-configuration-0'],
            'reason': 'J8 is a real CPU PA7 ground-jumper position, documented installed for this game; its physical circuit and factory low level are known. The firmware interpretation of PA7/configuration bit 0 is unresolved, so an inherited Country/W7 identity is not asserted.',
            'would_resolve': 'Game-specific CPU/firmware documentation or ROM dataflow from PIA2 port A at $2800, bit 7, establishing the consuming branch and meaning for the supported production firmware. A board photo can corroborate a surviving board installation, but does not establish firmware purpose.'
        }, {
            'dimension': 'output_semantics',
            'devices': ['coil.driver-20'],
            'reason': 'SP6 is physically unfitted. Known direct CRA $2401 writes from shadow $0102 initialized to $38 request inactive CA2; the adjacent indexed PIA-test sequence is gated off. Bounded static analysis did not resolve indirect event dispatch or every indexed-store range. Retained runtime traces did not publish 20, which is not unused proof.',
            'would_resolve': 'Resolve event-dispatch targets at ROM $45ED (JSR 0,X) and indexed-store base/value ranges that could modify shadow $0102 or PIA1 CRA $2401; establish whether a reachable enabled path can request low CA2. The known direct stores at $4C96/$4CA3 are already accounted for in the pinned ROM-analysis excerpt.'
        }, {
            'dimension': 'spatial_placement',
            'devices': list(dict.fromkeys(unplaced + ['coil.driver-11']
                           + ['coil.driver-' + str(n) for n in sorted(FLASH - {1})])),
            'reason': 'Three trough sensors, separate left-stack sensor 29, organ motor/limits, rear PHANTOM sockets, all individual flasher sockets and complete GI socket survey lack registered physical coordinates. Insert-overlay candidates and 12 observed VPX bulb meshes do not establish a complete factory-socket inventory.',
            'would_resolve': 'Registered own-game drawings/photographs or measured socket survey, including underside/apron and rear-panel bulbs; reconcile each candidate and quantity to the physical circuit.'
        }],
        'promotion_decision': {
            'status': 'partial',
            'author_ready': False,
            'reason': 'Do not promote observed geometry into author-ready physical completeness.'
        }
    }


def desired() -> dict[Path, str]:
    m = build_machine()
    r = build_report(m)
    md = f'# Phantom of the Opera spatial blockers\n\nThe record remains **partial**. Coordinates use the exact retained table bounds {PLAYFIELD_WIDTH}×{PLAYFIELD_HEIGHT}; x runs left to right and y rear to apron.\n\n'
    md += '\n\n'.join(
        '**' + b['dimension'] + '**: ' + b['reason'] + ' Resolution: ' + b['would_resolve']
        for b in r['blockers']
    ) + '\n\nAll raw object candidates, rejected helpers, projection classes and extraction hashes are in the adjacent JSON report and pinned places seed. No Flasher sprite, insert overlay or GI render double is silently promoted to a physical socket.\n'
    return {
        MACHINE: text_json(m),
        SEED: text_json(m),
        REPORT: text_json(r),
        REPORT_MD: md,
        KNOWLEDGE: (ROOT / KNOWLEDGE_SEED).read_text(encoding='utf-8'),
        **excerpts(load_json(ROOT / MANUAL_DATA))
    }


def verify_external() -> None:
    vpx = os.environ.get('PINMAME_VPX_SOURCES_ROOT')
    if vpx:
        p = Path(vpx) / 'data-east' / SLUG
        for file, digest in [(TABLE_FILE, TABLE_SHA), ('extracted/script.vbs', SCRIPT_SHA),
                             ('de.vbs', DE_VBS_SHA), ('core.vbs', CORE_VBS_SHA)]:
            if not (p / file).is_file() or sha(p / file) != digest:
                raise ValueError('retained evidence mismatch: ' + str(p / file))
        if check_manifest(p / 'extracted', 'poto_a32') != MANIFEST_SHA:
            raise ValueError('extraction manifest digest mismatch')
    manuals = os.environ.get('PINMAME_MANUALS_ROOT')
    if manuals:
        p = Path(manuals) / 'by-machine' / ID / 'ipdb-1777' / MANUAL_FILE
        if not p.is_file() or sha(p) != MANUAL_SHA: raise ValueError('retained manual mismatch: ' + str(p))
    review = os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT')
    if review:
        p = Path(review) / SLUG / 'pinside-knocker-page.json'
        if not p.is_file() or sha(p) != PIN_SIDE_SHA: raise ValueError('owner capture mismatch: ' + str(p))
        if check_manifest(Path(review) / SLUG / 'output20-re', 'poto_a32') != ROM_ANALYSIS_SHA:
            raise ValueError('retained output-20 analysis manifest mismatch')
        if build_organ_evidence(Path(review) / SLUG / 'organ') != load_json(ROOT / ORGAN_EVIDENCE):
            raise ValueError('retained organ evidence disagrees with compact artifact')
        if build_service_evidence(Path(review)) != load_json(ROOT / SERVICE_EVIDENCE):
            raise ValueError('retained service evidence disagrees with compact artifact')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if (ROOT / 'machines/author-ready/data-east' / f'{SLUG}.json').exists():
        raise ValueError('refusing to overwrite or accept an author-ready artifact')
    data = load_json(ROOT / MANUAL_DATA)
    places = load_json(ROOT / PLACES)
    if data['manual_sha256'] != MANUAL_SHA or places['source_sha256'] != SCRIPT_SHA:
        raise ValueError('pinned curator inputs disagree')
    if len(data['switch_matrix']) != 64 or len(data['lamp_matrix']) != 64:
        raise ValueError('incomplete matrix transcription')
    for path, expected_hash in INPUT_HASHES.items():
        if content_sha256(load_json(ROOT / path)) != expected_hash:
            raise ValueError('reviewed curator input drift: ' + str(path))
    verify_external()
    if sha(ROOT / 'tools/phantom_organ_probe.py') != '4e05666177e56628209eab14dc5abdf7a21738b2fcb7efa76efcf5cdbcb64986':
        raise ValueError('reactive organ adapter differs from the executed source')
    for path, expected_hash in ((ORGAN_EVIDENCE, ORGAN_SHA), (SERVICE_EVIDENCE, SERVICE_SHA)):
        if not (ROOT / path).is_file() or sha(ROOT / path) != expected_hash:
            raise ValueError('compact runtime evidence mismatch: ' + str(path))
    expected = desired()
    if args.check:
        drift = [
            str(p) for p, t in expected.items() if not (ROOT / p).is_file() or (ROOT / p).read_text(
                encoding='utf-8').replace('\r\n', '\n') != t.replace('\r\n', '\n')
        ]
        catalog = load_json(ROOT / 'catalog/pinmame.json')
        rows = [r for r in catalog['machines'] if r['id'] == ID]
        if (len(rows) != 1 or rows[0]['definition_sha256'] != content_sha256(build_machine())
                or rows[0]['definition'] != MACHINE.as_posix()):
            drift.append('catalog/pinmame.json')
        drivers = {row['id']: row for row in catalog['drivers']}
        for driver in ('poto_a29', 'poto_a31', 'poto_a32'):
            row = drivers.get(driver, {})
            if row.get('machine_id') != ID or row.get('definition') != MACHINE.as_posix():
                drift.append('catalog/pinmame.json')
        coverage, queue = build_coverage_report(ROOT), build_curation_queue(ROOT)
        generated = {
            Path('reports/coverage.json'): text_json(coverage),
            Path('reports/coverage.md'): render_coverage_markdown(coverage),
            Path('reports/curation-queue.json'): text_json(queue),
            Path('reports/curation-queue.md'): render_curation_queue_markdown(queue),
        }
        priority = ROOT / 'docs/pinside-top100.md'
        if priority.is_file():
            generated[Path('docs/pinside-top100.md')] = refresh_pinside_top100(
                priority.read_text(encoding='utf-8'), catalog)
        drift.extend(
            str(p) for p, t in generated.items()
            if not (ROOT / p).is_file() or (ROOT / p).read_text(encoding='utf-8') != t)
        if drift: raise SystemExit('drift: ' + ', '.join(drift))
    else:
        for p, t in expected.items():
            write_text(ROOT / p, t)
        rebuild_catalog(ROOT)
        write_coverage_report(ROOT)
    return 0


if __name__ == '__main__': raise SystemExit(main())
