"""Reproduce Star Wars' complete semantic inventory and honest partial coverage.

Normal generation reads committed seeds and excerpts only. External artifacts
are independently verified by the retained-evidence tests and runtime builder.
The baseline is the immutable pre-curation definition, not this tool's output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import curate_star_wars_spatial as places
import star_wars_pinmame as pin
from pinmame_flipper_column import flipper_column_relationships, VPM_DE_LIBRARY_SOURCE, VPM_DE_LIBRARY_URI, VPM_DE_SHA256

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tools/seeds/data-east/star-wars-1992-baseline.json"
KNOWLEDGE = ROOT / "knowledge/data-east/star-wars-1992.md"
EXCERPTS = ROOT / "evidence/excerpts" / places.KEY
RUNTIME_PATH = ROOT / "tools/star_wars_runtime.json"
RUNTIME = "runtime.star-wars.stwr-103-service-tests"
IDENTITY = "identity.star-wars.ipdb-2358"
FACTS_SHA = "6609a0e86212233872a24cd8b3d1a5988498fdff6ed170c8f9e5a15b7cc3689a"
RUNTIME_SHA = "58e51bec86678816337e8c17bc1432ef6055d71e6890eb8e1660562bca52c4bf"
RUNTIME_EVIDENCE = ROOT / "evidence/runtime/data-east/star-wars-stwr_103-service-tests.json"
MECHANISM_EXCERPT_SHA = "0739f6a43cde76f1f9a4ce75fa57e20a35e9659cb10a2f4fbefd879626f69d53"
READINGS_SHA = "e13c0130ae7c65e134c2d832af8bbb888ee3a9ae3c87438dcb14afc76dd28201"
ANNIVERSARY = "service.star-wars.official-104-readme"
ANNIVERSARY_EXCERPT_SHA = "a1d4bfca007917a7e12726815dcb92d16de79e4f74c548a827a14f2a53902da9"


def prov(*refs: str, status="observed") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def pinned(path: Path, digest: str) -> bytes:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"pinned evidence drift: {path.relative_to(ROOT)}")
    return data


def table_rows(title: str, columns: int) -> list[list[str]]:
    text = pinned(EXCERPTS / "manual-spatial.md", places.EXCERPT_SHA).decode("utf-8")
    region = text.split(title, 1)[1].split("\n## ", 1)[0]
    return [[v.strip() for v in line.strip().strip("|").split("|")]
            for line in region.splitlines() if line.startswith("|") and len(line.split("|")) == columns + 2][2:]


def manual_rows() -> tuple[dict, dict, dict]:
    switches = {}
    for number, label, part in table_rows("## Complete switch parts chart", 3):
        numbers = range(52, 65) if "through" in number else [int(number.rstrip("*"))]
        for n in numbers:
            switches[n] = {"label": label, "part": part}
    lamps = {int(n): {"label": label} for n, label in table_rows("## Lamp Locations: complete list", 2)}
    coils = {n: {"label": label, "part": part, "kind": "coil"} for n, label, part in (
        (1, "Outhole", "23-840"), (2, "Trough Eject", "23-840"), (3, "Ball Launch", "23-800"),
        (4, "Left Power Scoop", "25-1240"), (5, "Left Vertical Up Kicker", "23-800"),
        (6, "Three-Bank Drop Target Reset", "23-800"), (7, "Right Power Scoop", "23-800"),
        (8, "Knocker", "23-800"), (9, "R2D2 Dance / Raise", "23-800"), (16, "Laser Kickback", "23-800"),
        (17, "Top Turbo Bumper", "23-800"), (18, "Left Turbo Bumper", "23-800"),
        (19, "Right Turbo Bumper", "23-800"), (20, "Bottom Turbo Bumper", "23-800"),
        (21, "Left Slingshot", "23-800"), (22, "Right Slingshot", "23-800"))}
    coils.update({10: {"label": "K1 Left/Right Coil Multiplexer", "kind": "relay"},
                  11: {"label": "General Illumination (Inverted Relay)", "kind": "gi"},
                  12: {"label": "Death Star Entrance Bar Motor", "kind": "motor", "part": "515-5256-00"},
                  15: {"label": "Death Star and R2D2 Rotation Motors", "kind": "motor"}})
    for n in range(25, 33):
        coils[n] = {"label": f"Flasher Bank {n - 24}R", "kind": "flasher"}
    if set(switches) != set(range(1, 65)) or set(lamps) != set(range(1, 65)):
        raise ValueError("factory table parsing did not produce the complete matrix")
    return switches, lamps, coils


def excerpt(identifier: str, filename: str, digest: str, locator: str, **extra) -> dict:
    return {"id": f"excerpt.star-wars.{identifier}", "path": f"evidence/excerpts/{places.KEY}/{filename}",
            "sha256": digest, "locator": locator, "method": "manual", "reviewed": True,
            "transcribed_by": "primary curator; visually checked native renders and retained DMD screens", **extra}


def add_evidence(definition: dict) -> None:
    sources = {s["id"]: s for s in definition["sources"]}
    common = ("manual-mechanisms.md", MECHANISM_EXCERPT_SHA)
    sources[places.MANUAL]["excerpts"].append(excerpt("mechanisms", *common,
        "PDF 7,25-26,30-31,33 / printed pp.3,23-24,28-29,31; complete auxiliary/flipper and major-assembly tables and main drivers 9-16 drawing region",
        image=f"evidence/excerpts/{places.KEY}/motor-relay-wiring.webp",
        image_sha256="c1689be36c1ac0cf0ca23069400fe52661e84f4bc6790bb5f91783af68690620",
        image_derivation="Star_Wars_DE_OPS.pdf page 31, crop box 0.21,0.68,0.66,0.95, scanned page rendered at its native resolution (embedded image xref 115, 2523px across 8.41in), rendered at 300 dpi, grayscale, 1137x885 WebP quality 80"))
    sources[places.SCHEMATIC]["excerpts"].append(excerpt("contacts", *common,
        "PDF 6,9-10 / printed pp.50,53-54; full playfield contact region, matrix and service connector transcription",
        image=f"evidence/excerpts/{places.KEY}/contact-construction.webp",
        image_sha256="bfd4a9809638f30d798b40f7ed2a02909872b30d5807bea12153b2c93a08086c",
        image_derivation="starwars_schematics.pdf page 6, crop box 0.31,0.49,0.4,0.9, scanned page rendered at its native resolution (embedded image xref 28, 4956px across 16.52in), rendered at 300 dpi, grayscale, 447x1348 WebP quality 80"))
    sources[places.SCHEMATIC]["excerpts"].append(excerpt("service-circuit", *common,
        "PDF 9 / printed p.53; CPU CN14 service-input filters and logic",
        image=f"evidence/excerpts/{places.KEY}/service-input-wiring.webp",
        image_sha256="af9e499d1daa9fd319f1e9eee68f3f59f0af82cea8042459c9a6204585ae489b",
        image_derivation="starwars_schematics.pdf page 9, crop box 0.04,0.64,0.32,0.93, scanned page rendered at its native resolution (embedded image xref 45, 4956px across 16.54in), rendered at 300 dpi, grayscale, 1387x948 WebP quality 80"))
    sources[places.SCHEMATIC]["excerpts"].append(excerpt("cpu-j8", *common,
        "PDF 2 complete CPU JUMPER TABLE and PDF 10 / printed p.54 PIA 11B PA7 J8 ground branch; factory installed J8 reads 0",
        image=f"evidence/excerpts/{places.KEY}/cpu-j8-wiring.webp",
        image_sha256="4570a34bec5c1e252c3eb1817a01b23d1da03c8e8df6aae2004379218f132828",
        image_derivation="starwars_schematics.pdf page 10, crop box 0.25,0.19,0.39,0.43, scanned page rendered at its native resolution (embedded image xref 50, 4956px across 16.52in), rendered at 300 dpi, grayscale, 694x787 WebP quality 80"))
    sources.update({s["id"]: s for s in pin.core_sources()})
    sources[ANNIVERSARY] = {"id": ANNIVERSARY, "kind": "service_bulletin", "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "Stern Pinball, Inc., copyright 1992-2012", "original_filename": "STAR_WARS_readme.txt",
        "uri": "external:pinmame-review-artifacts/star-wars-1992-curation-2026-10-22/STAR_WARS_readme.txt",
        "sha256": "0ebe249845d5ba4da8433e4d1c52dbc208cefb208c019faa109ef41144cd5bfb",
        "locator": "Contributor-authorized stwr_104.zip member; official V1.04 change list dated December 19, 2012; IPDB2358 official anniversary download listing; read and retained 2026-10-22",
        "excerpts": [excerpt("anniversary-104", "anniversary-104.md", ANNIVERSARY_EXCERPT_SHA, "Complete V1.04 change list, factual paraphrase; rules evidence, not EPROM fitting instructions")]}
    readings = ("identity-and-runtime.md", READINGS_SHA)
    sources[places.SCRIPT]["excerpts"] = [excerpt("vpw-implementation", *readings,
        "script.vbs 114,127,165-352,363-434,481-569,1172-1175,1284 onwards; complete callback, key-handler and mechanism initialization regions, including R2 head limits314-316")]
    sources[VPM_DE_LIBRARY_SOURCE] = {"id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI,
        "sha256": VPM_DE_SHA256, "license": "NOASSERTION", "attribution": "VPinMAME script-library contributors, installed VBS v3.61",
        "locator": "de.vbs constants21-36 and vpmKeyDown/Up62-133; retained contributor installation, independently hashed 2026-10-22",
        "excerpts": [excerpt("de-vbs", *readings, "complete DE data constants, lower/staged flipper and service key handlers")]}
    sources[RUNTIME] = {"id": RUNTIME, "kind": "runtime_scenario", "uri": RUNTIME_EVIDENCE.relative_to(ROOT).as_posix(),
        "sha256": RUNTIME_SHA, "revision": pin.PINMAME_REVISION,
        "locator": "stwr_103 CPU 1.03 / DMD 1.05; exact-title checkpointed switch, single-lamp and cycling-coil tests; retained raw trace and every PGM pinned in this portable derivative; generated 2026-10-22",
        "acquired_at": "2026-10-22T15:34:50Z",
        "excerpts": [excerpt("diagnostics", *readings, "native CPU1.03/DMD1.05 diagnostic readings; complete named-frame inventory in tools/star_wars_runtime.json")]}
    # The archived page was retained unmodified, independently of the VPX header.
    sources[IDENTITY] = {"id": IDENTITY, "kind": "human_review", "license": "NOASSERTION",
        "attribution": "Internet Pinball Database, IPDB 2358; archived original page", "source_id": "2358", "rights": "NOASSERTION", "original_filename": "ipdb-wayback.html",
        "uri": "external:pinmame-review-artifacts/star-wars-1992-curation-2026-10-22/ipdb-wayback.html",
        "sha256": "e7316dee4043faf4351180bb2f90a7466ea1a6acb9549cdf1378333eb632a893",
        "acquired_at": "2026-10-22T15:17:50Z",
        "locator": "IPDB #2358 https://www.ipdb.org/machine.cgi?id=2358; unmodified capture https://web.archive.org/web/20250108044008id_/https://www.ipdb.org/machine.cgi?id=2358; title Star Wars (Data East), October 15 1992, model 500-5524-01; factual excerpt in identity-and-runtime.md",
        "excerpts": [excerpt("identity", *readings, "IPDB2358 title, manufacture date, model, electronics and physical features")]}
    definition["sources"] = list(sources.values())


def build() -> dict:
    pinned(EXCERPTS / "manual-mechanisms.md", MECHANISM_EXCERPT_SHA)
    pinned(EXCERPTS / "identity-and-runtime.md", READINGS_SHA)
    pinned(EXCERPTS / "anniversary-104.md", ANNIVERSARY_EXCERPT_SHA)
    pinned(RUNTIME_EVIDENCE, RUNTIME_SHA)
    runtime = json.loads(pinned(RUNTIME_PATH, FACTS_SHA))
    definition = json.loads(BASELINE.read_text(encoding="utf-8"))
    switches, lamps, coils = manual_rows()
    definition["drivers"] = pin.driver_records(definition["drivers"])
    next(d for d in definition["drivers"] if d["id"] == "stwr_104")["variant_notes"] += " Stern's retained official readme (service.star-wars.official-104-readme) dates V1.04 December 19, 2012 and lists a ten-second Freeze ball save, revised ramp/Force scoring, bonus, combo, audio and audit behavior. These rules changes do not establish EPROM/socket compatibility; the full factual change list is excerpted."
    refs = (places.SCRIPT, RUNTIME)
    definition["inputs"] = pin.inputs(definition["inputs"], switches, runtime_source_refs=refs)
    definition["outputs"] = pin.outputs(definition["outputs"], lamps, coils, runtime_source_refs=refs)
    for device in definition["inputs"]:
        address = device["binding"]["device"]
        if device["availability"] != "used":
            if address in (18, 52):
                device["physical"]["notes"] += f" ROM diagnostics name this '{runtime['switches'][str(address)]['name']}', but the factory parts chart explicitly says Not Used and VPW binds no physical device here. Software recognition is not fitment."
            continue
        if device["kind"] == "dip_switch":
            continue
        device["normally_closed"] = False
        if 1 <= address <= 64:
            if address == 1:
                device["physical"].pop("part_number", None)
                device["physical"]["assembly_part_number"] = "500-5023-00"
                device["physical"]["switch_type"] = "tilt"
            observation = runtime["switches"][str(address)]
            device["wiring"] = {"board": "CPU switch matrix", "drive_wire": observation["drive_wire"],
                "return_wire": observation["return_wire"], "return_connection": f"CPU CN10-{(9,8,7,6,5,3,2,1)[(address - 1) % 8]}"}
            if address > 8:
                device["wiring"]["drive_connection"] = f"CPU CN8-{(1,2,3,4,5,7,8,9)[(address - 1) // 8]}"
            device["physical"]["notes"] = f"Factory parts chart: {switches[address]['label']}. Normally-open contact; unmasked INITGAMES11 matrix is read directly by pia4a_r. stwr_103 Active Switch Test names the closed contact at public 1; a ball resting on it is an actuated state, not normally-closed construction."
            if address in (15, 16):
                host = 84 if address == 15 else 82
                device["physical"]["notes"] += f" core_updateSw rewrites this matrix contact from host flipper button {host}; drive {host}, not this matrix copy. The harness's repeatedly reasserted pulse can transiently force the matrix between rewrites and is not a supported flipper interface."
        elif address == -7:
            device["wiring"] = {"board": "CPU service inputs", "control_connection": "CN14-3", "return_connection": "CN14-2 GND"}
            device["physical"]["notes"] = "Black Advance: momentary service step button, released public 0, pressed 1. PinMAME complements it to PIA2 CA1; do not invert the public value again. Exact-title harness navigation proves ROM acceptance."
            device["pulse"] = True
        elif address == -6:
            device["wiring"] = {"board": "CPU service inputs", "control_connection": "CN14-4", "return_connection": "CN14-2 GND"}
            device["physical"]["notes"] = "Green Forward/Reverse: maintained push-on/push-off service selector. Up/forward is public 0, down/reverse 1; keep that state between Advance pulses. This is the contact's up/released reference, not a spring-return button. Internal LS02/PIA polarity is already handled by PinMAME."
            device["pulse"] = False
        elif address in (82, 84):
            device["provenance"]["source_refs"].append(VPM_DE_LIBRARY_SOURCE)
            device["physical"]["notes"] += " The cabinet leaf contact closes to energize its flipper ground circuit, so the released button is normally open. ROM test names the corresponding matrix contact at public 1; synthetic coil pair follows only while output 23 enables it."
    for device in definition["outputs"]:
        group, address = device["binding"]["group"], device["binding"]["device"]
        if device["availability"] != "used" or device["kind"] in ("virtual", "control_signal"):
            continue
        if group == "pinmame.output.solenoid":
            device["physical"]["notes"] = f"Factory wiring and retained VPW callback/ROM diagnostic identify public solenoid {address}."
            if address == 10:
                device["spatial"] = places.not_applicable("internal_nonvisual", [places.MANUAL, pin.PINMAME_S11_SOURCE_ID])
                device["physical"]["notes"] += " K1 selects coil bank 1-8 versus flash bank 25-32; consume the already-demultiplexed public outputs, not K1 as a playfield coil."
            elif address == 11:
                device.pop("spatial", None)
                device["physical"]["notes"] += " Relay is on the power-supply board. Public 1 extinguishes GI; public 0 illuminates it (VPW Sol11). The 17 observed GI placements are table bulb candidates, not the complete factory socket inventory. Legacy lamp 111 was a table-local Lampz helper; its legacy alias now resolves here."
            elif address == 8:
                device["spatial"] = places.not_applicable("cabinet_or_service", [places.MANUAL, places.SCHEMATIC])
                device["physical"]["location"] = "cabinet knocker"
            elif address == 15:
                device["physical"]["notes"] += " One relay drives two separate 28VAC motors: Death Star 515-5570-00 and R2D2 515-5571-00. The placement is the Death Star assembly anchor, not both motor centres; the R2D2 rotation mechanism shares this binding."
            elif address == 12:
                device["physical"]["notes"] += " 28VAC bar motor through relay board 520-5010-00; sensors 41/42 are pre-limit contacts. Script reverse-motion model is a recreation implementation, not evidence of physical electrical reversal."
            elif address >= 25:
                device["physical"]["notes"] += " Bank location and bulb annotations are transcribed in manual-spatial.md; no complete quantity is asserted where factory totals conflict."
            if address in range(17, 23):
                index = address - 17
                device["wiring"] = {"board": "CPU controlled auxiliary solenoids",
                    "control_wire": ("BLU-BRN", "BLU-RED", "BLU-ORN", "BLU-YEL", "BLU-GRN", "BLU-BLK")[index],
                    "control_connection": f"CPU CN19-{(7,4,3,6,8,9)[index]}",
                    "driver_transistor": ("Q11", "Q9", "Q8", "Q10", "Q12", "Q13")[index],
                    "power_wire": "RED", "power_connection": "PS CN3-8"}
            if address in (12, 15):
                device["wiring"] = {"board": "Relay board 520-5010-00", "nominal_voltage_v": 28, "voltage_type": "ac"}
        elif address == 17:
            raise AssertionError("unused lamp unexpectedly marked used")
        else:
            observation = runtime["lamps"][str(address)]
            device["wiring"] = {"drive_wire": observation["drive_wire"], "return_wire": observation["return_wire"]}
            device["physical"]["notes"] = f"Factory lamp chart {address}: {lamps[address]['label']}; ROM single-lamp test names this same public address '{runtime['lamps'][str(address)]['name']}'. Physical placement/quantity is separate from the diagnostic string."
    unused_lamp = next(d for d in definition["outputs"] if d["binding"] == {"group": "pinmame.output.lamp", "device": 17})
    unused_lamp["physical"]["notes"] += " The ROM single-lamp test does pulse 17 as X MODE; this is an unfitted testable matrix position, not proof of a populated bulb."
    # Spatial decoration reuses observed geometry but never upgrades it to validated.
    definition = places.build(definition)
    add_evidence(definition)
    definition["machine"].update({"kind": "physical_pinball", "model_number": "500-5524-01",
        "playfield": {"width": 946, "height": 2162, "units": "vpx", "provenance": prov(places.TABLE)}})
    definition["controller"]["hardware_generation"] = "0x4000"
    definition["displays"] = [{"id": "display.dmd", "label": "Backbox Dot Matrix Display", "kind": "dmd",
        "controller_index": 0, "width": 128, "height": 32, "physical_location": "cabinet_or_service",
        "spatial": places.not_applicable("cabinet_or_service", [places.MANUAL, RUNTIME]),
        "provenance": prov(pin.PINMAME_DEGAMES_SOURCE_ID, pin.PINMAME_DEDMD_SOURCE_ID, places.MANUAL, RUNTIME)}]
    definition["relationships"] = flipper_column_relationships(flip_swno=(15, 16),
        matrix_ids={d["binding"]["device"]: d["id"] for d in definition["inputs"] if d["binding"]["group"] == "pinmame.input.switch"},
        refs=(pin.PINMAME_CORE_SOURCE_ID, pin.PINMAME_CORE_HEADER_SOURCE_ID))
    definition["mechanisms"] = mechanisms(definition)
    definition["coverage"] = {"status": "partial",
        "missing": ["variant_differences", "spatial_placement", "unresolved_conflicts"],
        "dimensions": {"catalog_identity": "observed", "address_enumeration": "validated",
            "semantic_naming": "observed", "physical_wiring": "observed", "mechanisms": "observed",
            "variant_coverage": "candidate", "recreation_knowledge": "observed", "spatial_placement": "observed"}}
    definition["knowledge"] = {"path": KNOWLEDGE.relative_to(ROOT).as_posix(), "status": "partial"}
    return definition


def mechanisms(definition: dict) -> list[dict]:
    sw = {d["binding"]["device"]: d["id"] for d in definition["inputs"] if d["kind"] == "switch"}
    sol = {d["binding"]["device"]: d["id"] for d in definition["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
    result = []
    def add(key, label, kind, actuators, sensors, behavior, part=None, positions=None):
        item = {"id": f"mechanism.{key}", "label": label, "kind": kind,
                "actuators": [sol[n] for n in actuators], "sensors": [sw[n] for n in sensors],
                "behavior": behavior, "provenance": prov(places.MANUAL, places.SCHEMATIC, places.SCRIPT, RUNTIME)}
        if part: item["assembly_part_number"] = part
        if positions: item["positions"] = [{"id": f"position.{key}.{name}", "label": name, "sensors": [sw[n]]} for name,n in positions]
        result.append(item)
    add("ball-feed", "Outhole and Three-Ball Feed Trough", "kicker", [1,2], [10,11,12,13],
        "Outhole switch 10 detects a drained ball; coil 1 returns it to the feed trough. Three physical trough contacts 11/12/13 sense the queue; coil 2 ejects its leading ball toward shooter switch 14. Factory names left/center/right are distinct from VPW's virtual array (11,13,12,10). Initialize three balls; do not model switch 10 as a fourth trough contact. A failed eject must leave the actual occupied contact closed for the ROM's retry/search logic.", "500-5012-01")
    add("ball-launch", "Automatic Ball Launcher", "kicker", [3], [14],
        "A served ball closes shooter-lane 14; coil 3 launches it. Shifter fire button 50 is the player's launch/skill-shot control, not the lane occupancy switch. VPW uses cvpmImpulseP; its speed 65 and 0.5 tuning are table physics, not factory travel time.", "500-5477-01")
    add("cabinet-shifter", "Cabinet Shifter and Fire Button", "other", [], [50,51],
        "Hand-operated front-cabinet assembly 500-5620-00 contains the fire/button harness (50), the Shift Down microswitch (51), and a spring. The factory chart explicitly leaves 52 unfitted despite the ROM's SHIFT UP diagnostic label; do not invent another input. VPW's Plunger/LockBar key asserts both 50 and 51 and clears both on release, while Left/Right Magna-Save latch 51 off/on; neither writes 50. These keyboard conveniences do not change the two fitted physical contacts or prove a motorized lever, spring force or travel specification.", "500-5620-00")
    for key,label,coil,sensor,part in [("left-scoop","Left Force Scoop",4,37,"500-5468-02"),("right-scoop","Right Sarlacc Scoop",7,33,"500-5468-00")]:
        add(key,label,"kicker",[coil],[sensor],"Ball occupancy holds the scoop contact closed until the corresponding eject coil releases the ball back onto the playfield. Keep occupancy during a failed eject. The two scoops have separate switches and coils; do not route them through the VUK counter.",part)
    add("return-vuk", "Death Star / Obi-Wan Underchute and Left VUK", "kicker", [5], [34,35,36],
        "Death Star trough 34 and Obi-Wan trough 35 route balls beneath the playfield to the left VUK 36. Coil 5 lifts a waiting ball to the wire ramp. VPW AddVUK delays its virtual arrival 200ms, counts queued balls, and holds 36 until its queue empties. That counter is a recreation of the shared return, not extra physical switches or measured transit time. A jam leaves the corresponding real occupancy contact closed.", "500-5116-04")
    add("drop-bank", "Three-Bank Drop Target Reset", "drop_target_bank", [6], [30,31,32],
        "Hits drop individual top/middle/bottom targets and close 30/31/32; they stay down and active until coil 6 resets the bank. Reset opens all three after the targets rise. Preserve partially dropped banks and failed resets; fixed X-Wing targets 25-29 do not share this reset.", "500-5621-03")
    add("death-star-bar", "Death Star Entrance Bar", "motorized", [12], [40,41,42],
        "Motor/relay 12 raises or lowers the entrance bar carrying hit target 40. End contacts 41 UP and 42 DOWN close just before their respective travel limits and must never be on together. VPW models reciprocal travel with vpmMechReverse, 72 steps and marks 0/71, disabling target 40 collision when lowered. These are software marks, not degrees or factory timing. Start with actual bar state and sensor feedback; do not fabricate a successful limit on a jam.", "500-5618-00", [("up",41),("down",42)])
    add("death-star-r2-rotation", "Death Star and R2D2 Rotation Drive", "rotary", [15], [],
        "Shared relay 15 drives two separate 28VAC motors: Death Star 515-5570-00 and R2D2 515-5571-00 (R2D2 unit 500-5484-00). No rotation index contact is listed. VPW uses a 360-step circular Death Star model and invokes UpdateR2Head, oscillating artwork between -80 and +60 degrees. These are visual phase/travel choices, not measured factory steps or travel. Turning off the relay stops drive, with table-owned coast tuning. One controller actuator is intentionally owned by this combined drive mechanism.")
    add("r2-dance", "R2D2 Raise / Dance", "toy", [9], [38],
        "Coil 9 lifts the R2D2 body; releasing it returns the toy. Switch 38 is the entrance ball switch, not a toy-position sensor. VPW SolR2/UpdateR2 animates height separately from output 15's head rotation. Its height/speed constants are artwork tuning; there is no encoded physical position telemetry.", "500-5484-00")
    add("laser-kickback", "Left Outlane Laser Kickback", "kicker", [16], [24],
        "When the ROM enables Laser Kick, a ball at left outlane 24 is returned by coil 16; otherwise it drains. VPW pulls back the kickback at initialization, fires on the output's rising state, and retracts on release. Lamp 56 is the lit feature indication, not an actuator.", "500-5080-00")
    for n,sensor,label in [(17,45,"Top"),(18,46,"Left"),(19,47,"Right"),(20,48,"Bottom")]:
        add(f"{label.lower()}-bumper", f"{label} Turbo Bumper", "kicker", [n],[sensor], "Ball contact closes the scoring/trigger switch and the corresponding special coil kicks the ball away. The physical trigger circuit and ROM diagnostic share this coil; do not assume a host switch closure makes PinMAME synthesize a special output (ssSw is empty). Return the skirt/contact when the ball leaves.", "500-5227-01")
    for n,sensor,label in [(21,43,"Left"),(22,44,"Right")]:
        add(f"{label.lower()}-sling", f"{label} Slingshot", "kicker", [n],[sensor], "Rubber deflection closes the sling switch and the physical special-solenoid circuit kicks the ball. ROM diagnostics publish the named output; ssSw is empty, so a recreation must not rely on PinMAME deriving a kick from a host switch pulse alone.", "500-5226-00")
    for side,button,outputs,part in [("left",84,[47,48],"500-5606-74"),("right",82,[45,46],"500-5606-73")]:
        add(f"{side}-flipper", f"{side.title()} Flipper", "other", outputs,[button], "Cabinet button drives the solid-state flipper hardware while game-on output 23 enables it. PinMAME supplies identical synthetic power/hold states for this non-CPU-controlled initializer; they do not measure winding duty or EOS. Drive host button 84 left / 82 right and release to return the bat. Physical coil 090-5032-00 (22-1080); table physics determines stroke/return.",part)
    add("knocker", "Cabinet Knocker", "other", [8], [], "Momentary coil 8 strikes the cabinet knocker. It has no scoring/position switch; release returns the striker. The retained table defines a sound routine without assigning SolCallback(8), an omitted recreation callback rather than evidence of absent factory hardware.")
    return result


def knowledge(definition: dict) -> str:
    lines = ["# Star Wars (Data East, 1992)", "", "Full semantic curation of the physical game, IPDB 2358, model 500-5524-01. The physical release is 1992; the catalog root's 2012 year belongs to anniversary firmware. Identity was checked against the retained archived IPDB page and factory manual independently of the VPX header.", "", "## Controller and inputs", "", "All eleven catalog drivers share Data East CPU revision 3, GEN_DEDMD32, DE2 sound and one 128×32 DMD. The definition enumerates 75 inputs: service -7/-6, matrix 1-64, flipper column 81-88 and CPU jumper DIP 0. The factory board calls it J8 at PIA 11B PA7, factory installed (DIP 0 = 0), not a bank of operator adjustments. The shared Williams W7/Germany/USA terminology is not declared by this Data East driver and is not assigned to this jumper. No extra/custom switch or lamp columns, custom coils, or printer line are enabled.", "", "The factory matrix contacts are normally open. INITGAMES11 has no inversion mask; pia4a_r reads core_getSwCol directly. The ROM's Active Switch Test names used contacts at public 1. A ball resting on a trough or cam mark does not turn its contact into normally-closed construction. The cabinet flipper leaf switch closes its ground circuit; use host 84 left and 82 right. core_updateSw copies them to matrix 15/16 and synthesizes 47/48 and 45/46 while game-on 23 is enabled. No EOS or upper flipper feedback is modeled. Do not independently drive the matrix copies or invert public inputs again.", "", "Black Advance -7 is a momentary step; Green -6 is maintained (0 forward/up, 1 reverse/down). The harness enters diagnostics by the ROM's exact displayed title, never by counting page presses. Its pulse helper reasserts a held input every 10ms; the diagnostic names seen during forced matrix 15/16 holds are therefore not proof that direct matrix writes survive core rewrites.", "", "Factory-unused matrix 18 and 52 have ROM diagnostic names MIDDLE LOOP and SHIFT UP. The factory switch parts list and retained script establish no fitted device there, so they remain unused with the software names disclosed. Matrix 2 is fourth coin, not the generic platform's ball-roll tilt: this manual explicitly says the game has no ball-roll tilt. Unused positions 8/9/18/49/52-64 and flipper-column 81/83/85-88 are explicitly disposed.", "", "## Outputs and display", "", "All 128 output positions are enumerated: solenoids 1-64 and lamps 1-64. The independent ROM coil test confirms 17 top bumper, 18 left bumper, 19 right bumper, 20 bottom bumper, 21 left sling, 22 right sling. The Data East PIA permutation is derived for this initializer rather than borrowed from another game. Drivers 13/14 are test-pulsed as NOT USED and the factory drawing explicitly fits no load. Reserved, printer, upper-flipper, simulator and custom ranges are positively explained by the pinned core.", "", "K1 relay 10 multiplexes A-side coils 1-8 and C-side flash banks 25-32; PinMAME already publishes their separated states. Solenoid 11 controls GI in reverse: 1 turns the lights off, 0 on. Lampz111 was a VPW-local helper, not a native lamp. The invalid native lamp 111 record is removed, and its VPE legacy lamp aliases now target the actual GI binding. The old duplicate semantic ID is retired; retained semantic IDs for real controller bindings are otherwise preserved. GI geometry remains an observed table grouping and does not prove the full factory bulb inventory.", "", "The missing knocker (8), multiplexer (10), cabinet credit lamp (25), sphere lamps (29/30), service controls and full synthetic flipper range are present. Lamp 17 is physically Not Used despite the ROM's X MODE sweep label. The single-lamp test identifies all 64 addresses; activity alone never proves a populated load. The backbox has one controller-index-0 128×32 DMD; the sound-layout callback is not another physical display.", "", "## Mechanisms and recreation", "", "Install three balls, with the queue sensing contacts 11/12/13 occupied once settled and the separate outhole 10 clear. Factory recommended pitch is approximately 6.5 degrees. Preserve real occupancy and failed eject/reset states so the ROM can perform its own retry and ball-search handling. Do not start with diagnostic switches or tilt active. Mechanism descriptions below separate factory topology from retained VPW implementation and explicitly identify table-owned tuning.", ""]
    for item in definition["mechanisms"]:
        lines += [f"### {item['label']}", "", item["behavior"], ""]
    lines += ["## Evidence and reproducibility", "", "Factory authority: the complete switch-parts and lamp-location tables, all eight flash-bank annotations, cabinet/shifter parts, auxiliary/flipper coils, major assemblies, contact construction and motor-relay diagrams are committed under evidence/excerpts/data-east.star-wars.1992. Native renders and OCR remain beside the hashed original PDFs in the external manuals root. The operator scan and separate schematics are related factory material, not independent confirmations.", "", "Runtime authority: retained VPW v1.2.2 (table ea240a0193d6…, script 1d5252b9ef7d…) and the exact stwr_103 CPU 1.03 / display 1.05 diagnostic runs. tools/star_wars_pinmame.json pins the initializer, complete ROM chip manifests and source hashes at PinMAME 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. The native DLL is dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead; its source snapshot was verified against all source/build files at that commit before running. No ROM bytes, manuals or table files are redistributed.", "", "The compact runtime derivative pins every raw trace and DMD snapshot; build_star_wars_runtime.py recomputes it from the retained runs. The normal curator uses an immutable baseline plus committed source/excerpt/runtime seeds and is independent of external roots. Its --check mode refuses byte drift. Runtime names are software observations; table coordinates and the factory physical construction have separate authority.", "", "## Remaining requirements", "", "Coverage remains partial with three explicit missing requirements, for an 81% completion score:", "", "- **variant_differences**: all eleven ROM manifests and logical controller/display differences are inventoried, but real-board socket compatibility of one- versus two-chip DMD sets and the anniversary revisions is not established by the emulator initializer. Obtain game-board/EPROM fitting instructions or a verified physical upgrade report before assigning physical_compatibility; all variants remain unknown.", "- **spatial_placement**: every published coordinate remains observed, not independently validated. Flash banks 5R/7R/8R and sphere lamps 29/30 lack defensible individual socket positions. Trough, cam sensors and coil effects use disclosed assembly projections; the GI table grouping is incomplete as a physical socket inventory. Output 15's Death Star anchor does not locate its second, R2D2 motor.", "- **unresolved_conflicts**: factory flash-bank annotations disagree on 4R/6R totals and 8R playfield versus insert-panel placement. The operator sheet's 6R total also differs from the separate schematic. ROM strings cannot settle fitted socket counts. Resolution requires photographs of populated banks and their harnesses or a later factory correction.", "", "This is not author-ready and no requirement is cleared merely because a controller address toggled.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if places.DEFINITION.exists() and json.loads(places.DEFINITION.read_text(encoding="utf-8"))["coverage"]["status"] == "author_ready":
        raise SystemExit("refusing to overwrite author-ready definition")
    definition = build()
    artifacts = {places.DEFINITION: places.canonical(definition), places.REPORT: places.canonical(places.report(definition)),
                 KNOWLEDGE: knowledge(definition).encode("utf-8")}
    for path,data in artifacts.items():
        if args.check:
            if path.read_bytes().replace(b"\r\n", b"\n") != data:
                raise SystemExit(f"drift: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print("Star Wars definition, knowledge and spatial report match" if args.check else "Wrote Star Wars curation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
