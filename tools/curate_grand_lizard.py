"""Reproduce Grand Lizard's partial, physical definition from reviewed evidence.

The tables and spatial seed are deterministic repository inputs. External roots
are optional for generation and mandatory for --verify-evidence. The curator
never promotes the record or overwrites an existing author-ready artifact.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import os
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.validation import validate_machine
from pinmame_flipper_column import (
    VPM_CORE_SHA256, VPM_LIBRARY_SOURCE, VPM_LIBRARY_URI, VPM_S11_SHA256,
    flipper_column_inputs, flipper_column_relationships, vpm_staged_flipper_notes,
)
import grand_lizard_data as data

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.grand-lizard.1986"
REV = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DEFINITION = Path("machines/partial/williams/grand-lizard-1986.json")
AUTHOR_READY = Path("machines/author-ready/williams/grand-lizard-1986.json")
SEED = Path("tools/seeds/williams/grand-lizard-1986.json")
SPATIAL = Path("tools/seeds/williams/grand-lizard-1986-spatial.json")
KNOWLEDGE = Path("knowledge/williams/grand-lizard-1986.md")
REPORT = Path("reports/spatial/williams/grand-lizard-1986.json")
REPORT_MD = Path("reports/spatial/williams/grand-lizard-1986.md")
RUNTIME = Path("evidence/runtime/williams/grand-lizard-l4-service-and-gameplay.json")
OWNER_SOURCES = Path("tools/seeds/williams/grand-lizard-1986-owner-sources.json")
OWNER = "human-review.grand-lizard.owner-repair"
EXCERPTS = Path("evidence/excerpts") / MACHINE_ID
CORE = "pinmame.core.grand-lizard"
CATALOG = "pinmame.catalog.46e1a01a0f73"
MANUAL = "manual.williams.grand-lizard.1986"
PRELIMINARY = MANUAL + ".preliminary"
IPDB = "ipdb.1070"
PROFILE = "controller-profile.pinmame-system-11"
SCRIPT = "vpx-script.grand-lizard.build-01"
TABLE = "vpx-table.grand-lizard.build-01"
RUNTIME_SOURCE = "runtime.grand-lizard.l4-service-and-gameplay"
MANUAL_HASH = "2c1e492c12d2bc03acf05095bb3dc8f9bca0c9f80dde9a02282a151faacda527"
PRELIMINARY_HASH = "ba75a70cb4d14fd1edea9631ee603796500f3e3a7ad78fea1fa9ce2bb52ff4ac"
# Acquisition times come from each retained source family, not a shared clock.
MANUAL_ACQUIRED = "2026-11-06T13:36:30.970551+00:00"
PRELIMINARY_ACQUIRED = "2026-11-06T13:38:01.388424+00:00"
VPX_INVENTORY_AT = "2026-11-06T13:44:31.736622+00:00"
# Filled with the final reviewed transcription byte identities, never refreshed by regeneration.
EXCERPT_DIGESTS: dict[str, str] = {
    "coin-lockout-wiring.md": "55458c8ebffa552a249f7b09dcc64ff4003dde53dae2ee0f5056313efc607274",
    "coin-lockout-wiring.webp": "930ca9ea36421bc74c12de4fb3e705240480ad8a6cc79f9018f0e0bac18fa1d1",
    "owner-repair.md": "66a6ad049e3567109cfeb768d696a783be4954ac78a4acc078118509f3d008ce",
    "flipper-wiring.md": "6dc9ec824bc8d4c80a157e40c5f3f174856517a6b83110a5220177f529e81a9f",
    "flipper-wiring.webp": "595b1c01cc1298b054999457cfd2e186c3aa4d546e777e00b0054a34b24aacb4",
    "gi-wiring.webp": "2eeb09a3988796671a0b9c25a65a63c1ab55b1e0a0519788c89bde63fef8d5c4",
    "lamp-matrix.md": "853334f48d9180118c7f6d181cb42fd076b06398486bfe94ac677bbac1aefec7",
    "location-lists.md": "a2c3b96cfa4edad7130f54a5474f0a3a21c6b5100350a468ff426a287011256a",
    "operation-and-mechanisms.md": "de77e4bfc22afb32d09a5698caa2e1ff26b271c1960318f71fd1e169ebe52990",
    "physical-wiring.md": "ee924d302899bd2c907ea959a98854a755e2799a90302c1fb5938cc319223d0e",
    "pinmame-contract.md": "319125d8e21611d75b92cdac7be38b2574f835a06d385f12bb877c7f4856749c",
    "script-contract.md": "8f03d2290ca758134691f9670d8ce5b1f68b1082a11a451f40fb2ded352faddb",
    "script-library.md": "50fbaa4855af491f74e80f28bbbcd803f2dc38ccee0168d1f69833f0de2f4505",
    "solenoid-table.md": "a349bf7c96da02db4c82744febd7fd85bd7871ae5b4f4358ed8702dd0f82f996",
    "spatial-flashers.webp": "eaf1c8106f44062463be78c595b8569abce057a605d16a534b6ee4b35b464c7c",
    "spatial-lamps.webp": "8f26b17ec63d7a67d4c53c46e640ed8d73a1929da1a0a01eef977ed41dded83e",
    "spatial-measurements.md": "209b84dfef0e84fbd7493f1fb80ae2a0bacce546308296507eb4a39f91c9eced",
    "switch-matrix.md": "5723785b1123bfa8b9c8fa15cc94a7c5bb9ff6b08e03f03bbb28a367007a75f5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def aliases(namespace: str, address: int, *, padded: bool = False) -> list[dict]:
    values = [str(address)]
    if padded and address > 0:
        values += [f"{address:02}", f"{address:03}"]
    return [{"namespace": namespace, "value": s} for s in dict.fromkeys(values)]


def device(identifier: str, label: str, kind: str, group: str, address: int,
           availability: str = "used", refs: tuple[str, ...] = (MANUAL, CORE, SCRIPT), **extra) -> dict:
    return {"id": identifier, "label": label, "kind": kind, "availability": availability,
            "binding": {"group": group, "device": address}, "provenance": prov(*refs),
            "aliases": aliases("pinmame.switch" if group.endswith("switch") else "pinmame.solenoid" if group.endswith("solenoid") else "pinmame.lamp", address, padded=True), **extra}


def build_inputs() -> list[dict]:
    items = []
    for n, label in [(-7, "Advance"), (-6, "Auto-Up / Manual-Down"), (-5, "CPU Diagnostic"), (-4, "Sound Diagnostic")]:
        items.append(device(f"switch.diagnostic-{abs(n)}", label, "switch", "pinmame.input.switch", n,
                            refs=(MANUAL, CORE, PROFILE), normally_closed=False, roles=["cabinet.service"],
                            physical={"switch_type": "button", "location": "coin door or CPU-board service control"},
                            spatial=na("cabinet_or_service", MANUAL, CORE)))
    for n, label in enumerate(data.SWITCH_LABELS, 1):
        unused = n == 47 or n >= 49
        col, row = divmod(n - 1, 8)
        dw, dc, q = data.SWITCH_COLUMNS[col]
        rw, rc = data.SWITCH_ROWS[row]
        physical = {"notes": f"Printed column {col + 1}, row {row + 1}."}
        if not unused:
            physical["part_number"] = data.SWITCH_PARTS[n - 1]
            physical["switch_type"] = "microswitch" if n in (*range(20, 24), 25, 26, 27) else "button" if n in (3, 8, 45, 46) else "tilt" if n in (1, 2, 7, 9) else "leaf"
        if n == 9:
            physical["notes"] += " Factory parts list identifies SW-1A-117 as Playfield Tilt. The retained evidence does not establish a precise contact center or a cabinet/service location, so this fitted switch remains an explicit spatial-placement gap."
        if n in (12, 14):
            physical["notes"] += " The parts list reverses the Left/Right trough words against the matrix's explicit lower-right/upper-left numbered positions; the numbered matrix and runtime stack order identify this position. Both printed readings are retained in the excerpts."
        if n in (38, 40):
            physical["notes"] += " The retained table swaps the A and D target callbacks: TargetD pulses 38 and TargetA pulses 40. The machine's matrix and parts/location drawing agree on 38=A, 40=D; physical positions follow that evidence and the meshes, not the erroneous table callbacks."
        if n in (43, 44):
            physical["notes"] += f" This is the matrix scoring contact. The manual separately names an A-4834-H/B-8734 special actuating contact; PinMAME synthesizes output {17 if n == 43 else 18} from this scoring bit through ssSw while enable 23 is active."
        if n == 47:
            physical["notes"] += " Both factory tables mark 47 Not Used. The table writes it from its left flipper key, but that does not establish a physical lane-change contact. FLIP_SWNO(0,48) makes no left matrix copy."
        if n == 48:
            physical["notes"] += " Matrix table calls it Right Flipper (EOS), but parts list identifies SW-1A-150 Lane Change, distinct from assembly 03-7811 EOS. PinMAME overwrites 48 from cabinet button 82 every update; drive 82, not 48. No physical EOS timing is represented."
        kwargs = {"physical": physical, "wiring": {"board": "System 11 CPU board", "drive_wire": dw, "drive_connection": dc,
                   "return_wire": rw, "return_connection": rc, "driver_transistor": q}}
        if unused:
            kwargs["spatial"] = na("unused", MANUAL, CORE)
        else:
            kwargs["normally_closed"] = False
            if n in (*range(1, 9), 45, 46):
                kwargs["spatial"] = na("cabinet_or_service", MANUAL, CORE)
                kwargs["roles"] = ["cabinet.tilt" if n in (1, 2, 7) else "cabinet.coin" if n in (4, 5, 6) else "cabinet.service" if n <= 8 else "cabinet.magna-save"]
        items.append(device(f"switch.matrix-{n}", label, "switch", "pinmame.input.switch", n,
                            "unused" if unused else "used", **kwargs))
    flippers = flipper_column_inputs(flip_swno=(0, 48), flip_swno_text="FLIP_SWNO(0,48)",
        core_refs=(CORE, PROFILE), button_refs=(SCRIPT, VPM_LIBRARY_SOURCE, PRELIMINARY),
        button_notes={"right": "The retained script passes the key to S11.VBS, which writes 82; both right flippers move together.",
                      "left": "The retained script passes the key to S11.VBS, which writes 84; both left flippers move together."},
        unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(VPM_LIBRARY_SOURCE,), button_normally_closed=False)
    left = next(d for d in flippers if d["binding"]["device"] == 84)
    left["physical"]["notes"] = "PinMAME left cabinet button bit 84 (CORE_SWLLFLIPBUTBIT). FLIP_SWNO(0,48) uses zero as the left sentinel: no left matrix copy exists and the ROM cannot read column 11 directly. With enable 23 on, this bit still synthesizes 47/48. Drive 84 for the left-flipper state; the table's extra matrix 47 write is to an unfitted position. The open cabinet contacts close while pressed, and both physical left flippers move together."
    items.extend(flippers)
    items.append({"id": "switch.country-jumper", "label": "Country Jumper (USA/Germany)", "kind": "dip_switch", "availability": "used",
                  "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
                  "physical": {"switch_type": "dip", "location": "CPU board", "notes": "Single Country jumper, core_getDip(0)<<7 at PIA2 PA7; not an eight-switch operator bank."},
                  "spatial": na("dip_switch", CORE, PROFILE), "provenance": prov(CORE, PROFILE)})
    return items


def build_outputs() -> list[dict]:
    result = []
    for n, label, kind, wire, cpu, harness, q, part in data.SOLENOIDS:
        physical = {"part_number": part, "notes": "Factory solenoid number equals the public address; CPU-plug and harness-plug names remain distinct."}
        if n == 6:
            physical["quantity"] = 2
            physical["notes"] += " The location drawing has two separate leaders ending on two lamp symbols."
        elif n == 12:
            physical["notes"] += " One identifiable circle supplies a placement, not a complete circuit count. The owner repair source describes series-paired flash lamps without mapping each pair to an output; a partner socket may be absent from this location drawing. Total quantity remains unresolved."
        elif n in (7, 19):
            physical["notes"] += " Some location leaders end on plastic outlines rather than separate lamp symbols. A measured symbol establishes one lamp for output 7, but the complete circuit bulb count is unresolved; no count is invented from leader count."
        elif n == 13:
            physical["notes"] += " Production PDF 41 B-10823 shows two playfield head sockets, and the table also names a backbox branch; the total backbox eye-bulb count remains undocumented here. Two playfield sockets do not establish total circuit quantity."
        elif n == 16:
            physical["notes"] += " Preliminary PDF 14 shows two parallel coil branches, each with an antiparallel diode, under 7L16 COIN LOCKOUT at 7J4 pins 3/4. These are two electrical windings; the drawing does not identify their physical assemblies or independently acting units. Total physical unit quantity remains unresolved."
        elif kind not in ("gi", "flasher"):
            physical["quantity"] = 1
        if n in (9, 10):
            physical["notes"] += " Factory parts list calls this a magnet relay (5580-09613-00); contacts power the A-8447 magnetic assembly. An effect anchor locates its magnetic ball interaction, not the relay coil."
        if n == 11:
            physical["notes"] += " Preliminary Power Wiring Diagram routes its contacts through the backbox/cabinet GI supply branches 3J8-6/7. The playfield branches 8/9 are unswitched. VPX PFGI dims playfield render lights as a shortcut; no proxy coordinate is used. Active output interrupts GI."
        if n == 16:
            physical["notes"] += " Fitted Coinco lockout relay; energized permits coins, de-energized rejects coins at maximum credits."
        extra = {"physical": physical, "wiring": {"board": "System 11 CPU board", "drive_wire": wire,
                 "drive_connection": cpu, "return_connection": harness, "driver_transistor": q}}
        if n in (11, 14, 15, 16):
            extra["spatial"] = na("cabinet_or_service", MANUAL, PRELIMINARY)
        if n == 16:
            extra["refs"] = (MANUAL, PRELIMINARY, CORE, SCRIPT)
        result.append(device(f"solenoid.{n}", label, kind, "pinmame.output.solenoid", n, **extra))
    for n in range(20, 65):
        if n == 23:
            label, availability = "Flipper and Switched-Solenoid Enable", "used"
            note = "Virtual PIA0 CB2 game-on enable 23; no driver-board load. Gates special outputs and synthetic cabinet flippers."
        elif n in (45, 46, 47, 48):
            side = "Right" if n <= 46 else "Left"
            label, availability = f"Synthetic {side} Flipper {'Power' if n % 2 else 'Hold'} State", "used"
            note = f"Core-fabricated pair {'45/46' if n <= 46 else '47/48'} follows button {'82' if n <= 46 else '84'} while enabled. Virtual state applies to both physical flippers of that side; no CPU coil, physical winding selection or EOS timing is measured."
        else:
            label, availability = f"Unused Solenoid Address {n}", "unused"
            note = (f"Factory table identifies hardware driver position Special #{n - 16} as Not Used, with blank wiring and part cells. No load is fitted. The virtual placeholder inventories this unfitted address without inventing a coil, flasher or relay. ROM coil-test sweep activity is not physical fitment."
                    if n <= 22 else "No per-game source: mux=0 disables 25-32; gameSpecific flags=0 disable 37-44; 33-36 are not served on GEN_S11X; 49 is an uninstalled simulator slot; 24/50 are gaps; custSol=0 disables 51-64.")
        result.append(device(f"solenoid.{n}", label, "virtual", "pinmame.output.solenoid", n, availability,
                             refs=(CORE, PROFILE, MANUAL) if n <= 22 else (CORE, PROFILE),
                             physical={"notes": note}, spatial=na("virtual" if availability == "used" else "unused", CORE, PROFILE)))
    for n, label in enumerate(data.LAMP_LABELS, 1):
        col, row = divmod(n - 1, 8)
        dw, dc, dq = data.LAMP_COLUMNS[col]
        rw, rc, rq = data.LAMP_ROWS[row]
        physical = {"notes": "Full matrix/parts-list label retained in manual excerpts."}
        extra = {"physical": physical, "wiring": {"board": "System 11 CPU board lamp matrix", "drive_wire": dw, "drive_connection": dc,
                 "return_wire": rw, "return_connection": rc, "driver_transistor": f"column {dq}; row {rq}"}}
        if n == 51:
            physical["notes"] = "Factory lamp matrix explicitly prints Not Used. The manual's Single Lamps diagnostic enumerates 01-64, including 51; any published diagnostic matrix state at this address does not establish a fitted lamp."
            extra["spatial"] = na("unused", MANUAL)
        elif n <= 6:
            physical["location"] = "backglass"
            extra["spatial"] = na("cabinet_or_service", MANUAL)
        if n in range(42, 48):
            physical["notes"] += " Matrix and parts list agree 42-44=Left, 45-47=Right; the ROM's separate Magna-Save depletion probes confirm those groups. The manual location drawing numbers and table visual bindings are mirrored across the playfield for these six lamps; physical placements follow the corrected side and lower/middle/upper order."
        result.append(device(f"lamp.matrix-{n}", label, "lamp", "pinmame.output.lamp", n, "unused" if n == 51 else "used", **extra))
    return result


def build_displays() -> list[dict]:
    rows = [(f"display.player-{n + 1}", f"Player {n + 1} {'16-segment Alphanumeric' if n < 2 else '7-segment with Comma'}", n, start, 7)
            for n, start in enumerate((1, 9, 21, 29))]
    rows += [("display.ball-match-left", "Ball In Play / Match Left Digit", 4, 0, 1), ("display.ball-match-right", "Ball In Play / Match Right Digit", 5, 8, 1),
             ("display.credits-left", "Credits Left Digit", 6, 20, 1), ("display.credits-right", "Credits Right Digit", 7, 28, 1)]
    return [{"id": ident, "label": label, "kind": "segment", "controller_index": index, "segment_start": start,
             "width": width, "height": 1, "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE, MANUAL),
             "provenance": prov(CORE, MANUAL)} for ident, label, index, start, width in rows]


def build_mechanisms() -> list[dict]:
    rows = [
        ("trough", "Three-ball Trough, Outhole and Manual Shooter", "kicker", [1, 8], [10, 11, 12, 13, 14], "A drained ball closes 10; output 1 kicks it into the three-position trough. Output 8 feeds the next ball to shooter 11; the manual plunger launches it. The retained stack starts with three balls and uses 12, 13, 14 in feed-to-rear order. A ball holds its occupied contact; update occupancy as real balls roll, rather than toggling all sensors from the coil. Held/stuck contacts can provoke retries or switch diagnostics. Eject spring/cam and ball friction are table-owned tuning; C-8492 identifies the feed assembly."),
        ("three-bank", "Three-Target Drop Bank", "drop_target_bank", [2], [25, 26, 27], "D-9355 has three individually latching spring-retracted targets, one switch each and one common reset plunger/plate. A struck target drops and holds its contact until output 2 raises the bank and releases it. The table uses cvpmDropTarget 25-27. Game rules advance cave value, extra ball and special across completions. Reset retries, dirty contacts, binding guides and weak springs can cause stuck/dropped-target reports; no factory numeric reset duration is specified."),
        ("four-bank", "Four-Target Flash Bank with Two Pair Resets", "drop_target_bank", [3, 4], [20, 21, 22, 23], "D-10883 contains four latching targets with four microswitches and two reset plungers/plates. Output 3 raises only the left pair 20/21, output 4 only right 22/23; the table uses separate two-target cvpmDropTarget instances. A hit starts the timed completion score sweep; physical targets stay down until reset. Do not model one common four-target reset. Sticking guides, switches or pair reset linkage can leave individual targets down."),
        ("lock", "Three-Ball Lock under A Ramp", "kicker", [5], [32, 33, 34], "The A ramp feeds a serial three-ball lock sensed by 32, 33, 34, and output 5 drives the C-8492 eject cam at the release end. The retained script kicks from sw34. One/two locked balls plus top release target 24, or three locked balls, starts multiball and releases the lock; 2-ball scores 2X and 3-ball scores 3X. Sensors follow ball occupancy, not an electrical coil-to-switch relationship. Ball motion queues and jam/retry handling belong to the recreation; no exact ejection speed or delay is asserted."),
        ("slingshots", "Left and Right Slingshot Kickers", "other", [17, 18], [43, 44], "Factory leaf scoring switches 43/44 are distinct from the special-solenoid trigger contacts. PinMAME deliberately uses 43/44 in ssSw to synthesize 17/18 while enable 23 is on. A ball flexes the sling rubber, closes the contact and the kicker accelerates it away; spring/linkage return releases the contact. The table animates each sling from its hit event. Rubber tension, leaf gaps and rebound are table tuning."),
        ("left-magna-save", "Left Magna-Save", "other", [9], [45], "Left cabinet button 45 requests magnetic rescue when a left charge is available. Output 9 energizes the 5580-09613-00 relay powering A-8447; the magnetic field acts on the ball near the left outlane. L-I-Z completion earns left units. The script uses cvpmMagnet LeftMagnet with grab-center disabled; its strength 12 is table tuning. The field stops when the ROM releases the relay or a charge expires. No position sensor or homing cycle exists."),
        ("right-magna-save", "Right Magna-Save", "other", [10], [46], "Right button 46 requests rescue and output 10 switches the right A-8447 through its relay. A-R-D completion earns right units. Right charge lamps 45-47 are depleted by separate presses, and output 19 flashes with the rescue. Ball response is force-based, not a held kicker. The script's magnet strength and event region are tuning, not factory measurements."),
        ("flippers", "Four Cabinet-Wired Flippers", "other", [45, 46, 47, 48], [82, 84, 48], "Both right flippers follow the right cabinet button 82, both left follow 84. Outputs 45/46 and 47/48 are paired synthetic state, not four independent CPU coils or measured power/hold windings. Only the right lane-change contact is in the matrix at 48, copied from 82 by core_updateSw; there is no left matrix contact 47. Physical coils include lower FL23/600-30/2600 and upper FL24/600-30/2600, with return springs and separate physical EOS contacts. EOS contacts open at full stroke; the emulator models no EOS timing here."),
        ("ramps", "A/B Ramps, Cave, Turnaround and Ramp Tongue", "other", [], [15, 24, 28, 29, 30, 31, 41, 42], "Two passive ramp paths pass through the lizard head: left A 31 feeds the lock, right B 29 returns via the right route; 30 detects the right chute to the upper field and 42 the ramp tongue. Turnaround 15 scores the cave, and the top-right stationary target 24 serves the speed/release role. Spinner 28 pulses once per spin. The manual's numbered switch map and retained gates locate these contacts; ramp paths, passive gates and ball dwell require geometry rather than invented extra controller coils."),
    ]
    return [{"id": f"mech.{key}", "label": label, "kind": kind, "actuators": [f"solenoid.{n}" for n in coils],
             "sensors": [f"switch.flipper-column-{n}" if n >= 81 else f"switch.matrix-{n}" for n in switches],
             "behavior": behavior, "provenance": prov(MANUAL, SCRIPT, CORE, RUNTIME_SOURCE)} for key, label, kind, coils, switches, behavior in rows]


def build_relationships() -> list[dict]:
    result = flipper_column_relationships(flip_swno=(0, 48), matrix_ids={48: "switch.matrix-48"}, refs=(CORE, PROFILE))
    for sw, sol in ((43, 17), (44, 18)):
        result.append({"id": f"relationship.special-{sol}-from-{sw}", "kind": "direct", "source": f"switch.matrix-{sw}",
                       "destination": f"solenoid.{sol}", "provenance": prov(CORE, SCRIPT)})
    return result


def excerpt(root: Path, filename: str, locator: str, **extra) -> dict:
    path = EXCERPTS / filename
    return {"id": filename.removesuffix(".md"), "locator": locator, "path": path.as_posix(), "sha256": sha256(root / path),
            "method": "manual", "transcribed_by": "curator; exact pinned source/native manual renders", "reviewed": True, **extra}


def sources(root: Path) -> list[dict]:
    records = [
        {"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REV, "locator": "PinmameGetGames grand_l4/grand_l3/grand_l1", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": REV, "locator": "src/wpc/s11games.c 38-41, 202-230; s11.c s11_dispS11, setSSSol, pia4a_r, updsol, grand_ output types; core.c/core.h flipper synthesis; gen.h GEN_S11X", "license": "NOASSERTION", "rights": "Mixed upstream terms under the pinned root LICENSE: src/wpc/s11games.c, src/wpc/s11.c and src/wpc/s11.h carry first-line BSD-3-Clause markers; src/wpc/core.c, src/wpc/core.h and src/wpc/gen.h are unmarked and retain the old MAME terms. No LICENSE/COPYING override is present in src/ or src/wpc/.", "attribution": "PinMAME contributors", "excerpts": [excerpt(root, "pinmame-contract.md", "Exact game data, variant ROMs, address and display paths")]},
        {"id": PROFILE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository", "locator": "System 11 sequential addresses, diagnostic nibble, country jumper and synthetic flipper column", "attribution": "Project contributors", "license": "MIT"},
        {"id": MANUAL, "kind": "manual", "uri": "https://web.archive.org/web/20241220022228id_/https://www.ipdb.org/files/1070/Williams_1986_Grand_Lizard_Manual.pdf", "source_id": "ipdb:1070", "original_filename": "Williams_1986_Grand_Lizard_Manual.pdf", "sha256": MANUAL_HASH,
         "acquired_at": MANUAL_ACQUIRED, "locator": "IPDB 1070 https://www.ipdb.org/machine.cgi?id=1070; production manual 52 PDF pages, source https://www.ipdb.org/files/1070/Williams_1986_Grand_Lizard_Manual.pdf; external:pinmame-manuals/by-machine/williams.grand-lizard.1986", "license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; scan hosted by IPDB", "rights": "Copyright retained by rights holders; source PDF not redistributed",
         "excerpts": [excerpt(root, "switch-matrix.md", "PDF 30 printed 26 complete switch matrix"), excerpt(root, "lamp-matrix.md", "PDF 28 printed 24 complete lamp matrix"), excerpt(root, "solenoid-table.md", "PDF 29 printed 25 complete solenoid/flipper table"), excerpt(root, "location-lists.md", "PDF 48-50 printed 44-46 complete switch/lamp/solenoid parts tables"), excerpt(root, "operation-and-mechanisms.md", "PDF 8-10, 34, 43-46 operation and assemblies")]},
        {"id": PRELIMINARY, "kind": "manual", "uri": "https://web.archive.org/web/20260210103416id_/https://www.ipdb.org/files/1070/Williams_1986_Grand_Lizard_Preliminary_Manual.pdf", "source_id": "ipdb:1070", "original_filename": "Williams_1986_Grand_Lizard_Preliminary_Manual.pdf", "sha256": PRELIMINARY_HASH, "acquired_at": PRELIMINARY_ACQUIRED,
         "locator": "IPDB 1070 https://www.ipdb.org/machine.cgi?id=1070; preliminary manual PDF 14-16 cabinet/power wiring, including PDF 14 printed 12 7L16 parallel coin-lockout coil branches at 7J4 pins 3/4; source https://www.ipdb.org/files/1070/Williams_1986_Grand_Lizard_Preliminary_Manual.pdf", "license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; scan hosted by IPDB", "rights": "Copyright retained by rights holders; source PDF not redistributed",
         "excerpts": [excerpt(root, "physical-wiring.md", "PDF 14-16 cabinet and power wiring", image=(EXCERPTS / "gi-wiring.webp").as_posix(), image_sha256="2eeb09a3988796671a0b9c25a65a63c1ab55b1e0a0519788c89bde63fef8d5c4", image_derivation="Williams_1986_Grand_Lizard_Preliminary_Manual.pdf page 16, crop box 0.01,0.47,0.79,0.72, scanned page rendered at its native resolution (embedded image xref 60, 1702px across 8.51in), rendered at 200 dpi, grayscale, 1328x553 WebP quality 80"),
                      excerpt(root, "flipper-wiring.md", "PDF 15 flipper power branches", image=(EXCERPTS / "flipper-wiring.webp").as_posix(), image_sha256="595b1c01cc1298b054999457cfd2e186c3aa4d546e777e00b0054a34b24aacb4", image_derivation="Williams_1986_Grand_Lizard_Preliminary_Manual.pdf page 15, crop box 0.21,0.53,0.74,0.85, scanned page rendered at its native resolution (embedded image xref 56, 1702px across 8.51in), rendered at 200 dpi, grayscale, 903x713 WebP quality 80"),
                      excerpt(root, "coin-lockout-wiring.md", "PDF 14 printed 12 Cabinet Wiring Diagram: 7L16, two parallel coil/diode branches, 7J4 pins 3/4", image=(EXCERPTS / "coin-lockout-wiring.webp").as_posix(), image_sha256="930ca9ea36421bc74c12de4fb3e705240480ad8a6cc79f9018f0e0bac18fa1d1", image_derivation="Williams_1986_Grand_Lizard_Preliminary_Manual.pdf page 14, crop box 0.335,0.245,0.45,0.44, scanned page rendered at its native resolution (embedded image xref 52, 1702px across 8.51in), rendered at 200 dpi, grayscale, rotated 270 degrees counter-clockwise, 429x196 WebP quality 80")]},
        {"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "sha256": VPM_S11_SHA256, "locator": f"S11.VBS key constants/handlers; core.vbs SHA256 {VPM_CORE_SHA256}", "license": "NOASSERTION", "attribution": "VPinMAME script-library contributors", "excerpts": [excerpt(root, "script-library.md", "S11.VBS lower flipper input and callback constants")]},
    ]
    for table in data.TABLES:
        suffix = table["build"]
        for role, kind, filename, digest in [("table", "vpx_table", table["filename"], table["sha256"]), ("script", "vpx_script", "extraction/script.vbs", table["script_sha256"]), ("extraction", "human_review", "extraction/manifest.json", table["manifest_sha256"])]:
            record = {"id": f"vpx-{role}.grand-lizard.{suffix}", "kind": kind, "uri": f"external:pinmame-vpx-sources/{table['directory']}/{filename}", "sha256": digest, "locator": f"Retained {suffix}; vpxtool git:v0.33.3; bounds 0,0,952,1974; full extraction {table['file_count']} files/{table['total_bytes']} bytes. Builds share ancestry; second supplementary, not independent.", "acquired_at": VPX_INVENTORY_AT, "license": "NOASSERTION", "attribution": "3rdaxis and Slydog43; credits JP Salas, Rosve, G5K"}
            if role == "script":
                record["known_working"] = False
                record["excerpts"] = [excerpt(root, "script-contract.md", "Retained embedded script bindings; exact table playability unverified; mappings checked against manual and independent ROM runs")]
            records.append(record)
    if not (root / RUNTIME).is_file():
        raise RuntimeError("Grand Lizard compact runtime evidence is missing")
    records.append({"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME.as_posix()}", "sha256": sha256(root / RUNTIME), "locator": "Fresh grand_l4 service/gameplay and isolated Magna-Save depletion runs; raw trace and binary/ROM identities retained externally", "revision": REV, "license": "MIT", "attribution": "Project harness and curator"})
    geometry = load_json(root / SPATIAL)
    factory = next(s for s in records if s["id"] == MANUAL)
    for page in ("manual49", "manual50"):
        retained = geometry["report"].get(page, {}).get("excerpt")
        if retained:
            factory["excerpts"].append(excerpt(root, "spatial-measurements.md", page + " native-pixel measurements and independent controls", **retained))
    records.extend(load_json(root / OWNER_SOURCES)["sources"])
    return records


def build(root: Path = ROOT) -> dict:
    if not (root / SPATIAL).is_file():
        raise RuntimeError("Grand Lizard required reviewed spatial seed is missing")
    geometry = load_json(root / SPATIAL)
    inputs, outputs = build_inputs(), build_outputs()
    by_id = {d["id"]: d for d in inputs + outputs}
    for identifier, spatial in geometry["devices"].items():
        if identifier not in by_id:
            raise RuntimeError(f"Spatial seed refers to unknown device: {identifier}")
        by_id[identifier]["spatial"] = copy.deepcopy(spatial["spatial"])
        if spatial.get("physical_notes"):
            by_id[identifier]["physical"]["notes"] += " " + spatial["physical_notes"]
    for n in range(42, 48):
        by_id[f"lamp.matrix-{n}"]["provenance"]["source_refs"].append(RUNTIME_SOURCE)
        for placement in by_id[f"lamp.matrix-{n}"].get("spatial", {}).get("placements", []):
            refs = placement["provenance"]["source_refs"]
            if RUNTIME_SOURCE not in refs:
                refs.append(RUNTIME_SOURCE)
    drivers = []
    for version in ("l1", "l3", "l4"):
        driver = {"id": f"grand_{version}", "description": f"Grand Lizard ({version.upper().replace('L', 'L-')})", "year": "1986", "manufacturer": "Williams", "flags": 0,
                  "physical_compatibility": "identical", "variant_notes": f"Williams {version.upper()} production firmware. Shares grandGameData, GEN_S11X, s11_dispS11, sound ROMs, mux = 0, ssSw = 43/44 and FLIP_SWNO(0,48). No hardware edition difference is declared; the firmware release does not create a new machine."}
        if version != "l4":
            driver["clone_of"] = "grand_l4"
        drivers.append(driver)
    definition = {"format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {"id": MACHINE_ID, "name": "Grand Lizard", "manufacturer": "Williams", "year": 1986, "model_number": "523", "ipdb_id": 1070, "opdb_id": "G4XPZ-M7Zob", "kind": "physical_pinball", "playfield": {"width": 952, "height": 1974, "units": "vpx", "provenance": prov(TABLE, status="observed")}},
        "controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
        "coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "observed", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed", "diagnostic_enumeration": "validated", "runtime_observation": "validated", "causal_exercise": "validated", "emulator_normalization": "validated"}},
        "drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": build_displays(), "mechanisms": build_mechanisms(), "relationships": build_relationships(), "sources": sources(root) + geometry.get("sources", []), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"}, "conflicts": []}
    for identifier in ("switch.matrix-47", "switch.matrix-48", "solenoid.13"):
        by_id[identifier]["provenance"]["source_refs"].append(OWNER)
    errors = validate_machine(definition, root)
    if errors:
        raise RuntimeError("Grand Lizard canonical validation failed:\n" + "\n".join(errors))
    return definition


def knowledge() -> str:
    return """# Williams Grand Lizard (1986)

Williams model 523, IPDB 1070, April 1986. The three production drivers grand_l1,
grand_l3 and grand_l4 share physical hardware. The L-4 root retains U26 L-3
and U27 L-4; L-3 changes U27 and L-1 uses its own game pair. All share the same
CPU/sound topology and physical playfield. OPDB identity is G4XPZ-M7Zob.

This definition remains **partial**. Complete flasher, backglass matrix-lamp
and controlled GI bulb counts are not established. Emitter/socket coordinates,
some mechanism sensor projections and the unswitched playfield GI inventory
remain incomplete.
Observed VPX geometry is useful authoring evidence but is not automatically
validated by matching object names or by a second table of shared ancestry.

## Controller and physical construction

The pinned emulator is 46e1a01a0f73dc5ce163d98db1ae435883ecc450.
GEN_S11X chooses the System 11 controller contract, eight matrix columns,
64 lamp channels and no custom outputs. There is no A/C multiplexer, printer
or sound-overlay expansion. Every public switch/solenoid/lamp address has an
explicit disposition, including unused ranges. Switches are ordinary contact
circuits; s11's uninverted read with no invSw mask presents a closure at 1.
Factory switch parts identify leafs/buttons/tilts and drop-target microswitches;
normally_closed is never inferred from a table object's initial occupancy.

Cabinet buttons 82 (right) / 84 (left) drive the synthetic flipper states.
FLIP_SWNO(0,48) copies only right 82 to lane-change 48; zero means no left copy.
Matrix 47 is factory Not Used despite the table's gratuitous left-key write.
Both upper/lower flippers on one side move together. 45/46 and 47/48 are virtual
paired states, not independent CPU coils or measured winding timing.
Physical EOS and lane-change contacts are separate parts. The preliminary
power sheet omits upper-left and draws EOS contacts incorrectly; final
production tables/assembly distinguish all four coils and closed-rest EOS.

The standard display layout has four seven-character player rows and four
separate one-digit controller callbacks. Ball In Play/Match uses starts 0/8
(indices 4/5), Credits 20/28 (indices 6/7). Player starts are 1,9,21,29.
These are backbox devices.

## Ball handling and mechanisms

Playfield Tilt switch 9 (SW-1A-117) is fitted, but its precise contact center
remains unplaced. The retained evidence does not establish a cabinet/service
location, so it is not exempted from spatial coverage by its numeric range.

Three balls begin in the trough. Outhole 10 and kicker 1 collect the drain;
positions 12 (feed end lower-right), 13 (center), 14 (rear upper-left) advance as
balls roll; feed 8 serves shooter 11 for the mechanical plunger. The parts list
reverses Left/Right words for 12/14 against the explicit matrix positions;
the list and its spelling remain transcribed, not silently overwritten.

The four-target flash bank D-10883 has two independent pair resets 3/4 for
20/21 and 22/23. The rear three-bank D-9355 has one reset 2 for 25-27. Targets
latch down and keep their switches closed until physically raised. Reset
plungers/plates, guides, retract springs and microswitch adjustment determine
actual recovery; no electrical coil-to-sensor relationship is invented.

The A-ramp lock under the left ramp holds up to three balls at 32/33/34.
Output 5 drives the release-end C-8492 eject cam. Three locked balls, or one/two
plus top release target 24, starts multiball. The ROM supplies retries/rules;
the recreation must move balls and update serial occupancy realistically.
The script's sw34 kick direction/speed and magnet strength 12 are tuning,
not physical factory measurements. Held sensors may trigger retries or startup
switch reports; the game can compensate scoring after 60 balls without a switch.

Slingshots 17/18 have physical trigger contacts separate from scoring 43/44.
PinMAME's ssSw map deliberately uses the scoring bits to emulate the triggers
when enable 23 is on. Output 19 is a right flasher, not a third bumper: this
machine has no pop bumpers. Contacts, kick arms and rubber tension return the
ball and open the switch after impact; exact motion is table-owned.

Magna-Save outputs 9/10 drive relay 5580-09613-00, which powers A-8447 magnetic
assemblies near the left/right outlanes. 45/46 are cabinet request buttons.
L-I-Z earns left units; A-R-D earns right units. Isolated ROM depletion runs
settle left lamps 42-44 and right 45-47: three requests exhaust one group and
the next two no longer energize its relay. The manual drawing and retained
table visual bindings place those number groups on the wrong sides; physical
side/order follow the matrix, rule descriptions, separate relay responses and
the corrected lamp map. Do not reproduce the mirrored visual shortcut.

The retained table also swaps A/D target callbacks 38/40. Both factory matrix
and parts/drawing agree 38=A and 40=D; the physical mesh anchors follow those
letters. This is a table defect, not unresolved machine identity.

## Lamps, flashers and general illumination

Lamps 1-6 are backglass indicators and 51 is unfitted. Their individual circuit
bulb quantities are unspecified in the retained lists, so no quantity defaults
to one. The table comments out
five backglass assignments and 51; commented code does not establish absence.
Lamp row/column connectors, transistor identifiers and all 64 literal matrix
labels are preserved in the excerpts. Light overlays and copied LightNb glow
helpers are not observed bulb sockets and do not establish physical quantity.

The factory flasher map shows two sockets on 6 (lock), one symbol for 12 (three-bank), and
one identifiable 7 symbol. Other 7/19 leaders end on plastic outlines and cannot
be counted as sockets. 13 spans the head and backbox:
B-10823 head mounting shows two head sockets, but the backbox count remains
unknown. The single 12 symbol also fails to establish its complete circuit
count: the owner describes series-paired flashers without mapping each pair.
These count gaps prevent full output-semantics completion. Clear wiring or
continuity evidence for outputs 7/12/19 and the original eye-flasher panel
can settle the remaining counts.
The retained Jeff-Z owner repair photograph corroborates two head lamps and
the disconnected left auxiliary flipper contact. It does not show complete
original flasher circuits; repair/replacement parts are disclosed in its source.

GI 11 interrupts backbox/cabinet lighting through power-supply relay contacts
and 3J8-6/7. The playfield GI branches 3J8-8/9 to 8J4 bypass that relay. The
table's PFGI dims the playfield rendering as an artistic shortcut; no
playfield lamp coordinate is attributed to GI 11. Its complete backbox/cabinet
socket inventory and quantity also remain unquantified. Unswitched playfield GI has
no PinMAME callback to bind; its physical socket inventory/positions still
need complete underside evidence and are an explicit spatial blocker.

Coin-lockout output 16 remains a fitted Coinco 404603-2 relay circuit.
Preliminary PDF 14 draws two parallel coil/diode branches under 7L16 at
7J4 pins 3/4. This establishes two windings, but not their mechanical unit
identities. The production table has no quantity column; its one channel
row does not establish one assembly. Physical unit quantity remains
unspecified and is an output-semantics blocker. A complete coin-door
assembly drawing or original, traced photograph can settle the actuator count.

## Evidence and readiness

The production 52-page manual and preliminary 34-page schematic manual are
retained with immutable hashes under the external manuals root. Full matrix
and parts tables, source-contract excerpts and tightly cropped wiring regions
travel with this contribution. The two retained local VPX builds share the
3rdaxis/Slydog43 ancestry. Neither exact build was launched or independently
verified playable in this contribution. Their script mappings were checked
against the manual and independent ROM runs; geometry remains observed.
Exact extraction manifests record every relative path, size and SHA256 in
case-sensitive path order, using canonical UTF8 JSON bytes plus
newline; vpxtool reported a malformed scratched-glass PNG dimension warning.
That warning is retained and does not change successful object extraction.

The spatial report inventories every located, unplaced and not-applicable
record, raw geometry/drawing evidence, projections and remaining dimensions.
Curator generation is independent of external paths; evidence-enabled checks
recompute exact sources, manifests and geometry. Runtime traces use fresh
state directories and legal existing ROMs; host-written switch readback is
not presented as ROM evidence. Full source locators and trace hashes are in
the definition and compact runtime evidence. Author-ready promotion is refused.
"""


def products(root: Path = ROOT) -> dict[Path, bytes]:
    verify_excerpts(root)
    definition = build(root)
    geometry = load_json(root / SPATIAL)
    records = definition["inputs"] + definition["outputs"] + definition["displays"]
    report = {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
              "coordinate_convention": "x = 0 left, x = 1 right; y = 0 rear/backglass, y = 1 apron; VPX/player view", "spatial_seed": SPATIAL.as_posix(),
              "spatial_seed_sha256": sha256(root / SPATIAL), "evidence": geometry.get("report", {}),
              "located": [{"id": d["id"], "spatial": d["spatial"]} for d in records if "placements" in d.get("spatial", {})],
              "unplaced": [{"id": d["id"], "label": d["label"]} for d in records if "spatial" not in d],
              "not_applicable": [{"id": d["id"], "reason": d["spatial"]["reason"]} for d in records if d.get("spatial", {}).get("status") == "not_applicable"],
              "readiness": {"status": "partial", "missing": definition["coverage"]["missing"], "blockers": ["Complete flasher 7/12/13/19, backglass matrix-lamp 1-6 and controlled backbox/cabinet GI bulb inventories unquantified; coin-lockout output 16 physical actuator quantity unresolved despite two schematic windings", "Playfield Tilt switch 9 has no retained contact-center measurement", "Physical emitter positions and unswitched playfield GI inventory incomplete; observed mechanism projections unvalidated"]}}
    md = f"# Grand Lizard spatial blockers\n\nStatus: **partial**. Coordinates use x = 0 left, x = 1 right, y = 0 rear, y = 1 apron.\n\n{len(report['located'])} located records; {len(report['unplaced'])} unplaced records.\n\n"
    md += "The pinned spatial seed records exact source object paths/hashes and raw coordinates. Every placement remains observed unless independently validated by its recorded manual measurement. Render lights are not sockets. Table ancestry does not establish independence.\n\n"
    unplaced = "; ".join(f"`{entry['id']}` ({entry['label']})" for entry in report["unplaced"])
    md += f"Unplaced devices: {unplaced}.\n\n"
    md += "Remaining: complete flasher 7/12/13/19, backglass matrix-lamp 1-6 and controlled backbox/cabinet GI socket counts; coin-lockout output 16 physical actuator quantity (two schematic windings do not establish mechanical units); the contact center of Playfield Tilt switch 9; physical lamp/flasher sockets and unswitched playfield GI; validation of projected sensors/effects. See the JSON report for every device, source and projection.\n"
    return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition), KNOWLEDGE: knowledge().encode("utf-8"), REPORT: canonical_bytes(report), REPORT_MD: md.encode("utf-8")}


def verify_excerpts(root: Path = ROOT) -> None:
    if not EXCERPT_DIGESTS:
        raise RuntimeError("Grand Lizard excerpt pins are missing")
    for name, digest in EXCERPT_DIGESTS.items():
        if not (root / EXCERPTS / name).is_file() or sha256(root / EXCERPTS / name) != digest:
            raise RuntimeError(f"Grand Lizard reviewed excerpt drifted: {name}")


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Grand Lizard partial curator refuses an existing author-ready artifact")
    for path, expected in products(root).items():
        if not (root / path).is_file() or (root / path).read_bytes() != expected:
            raise RuntimeError(f"Grand Lizard deterministic artifact missing or drifted: {path}")


def generate(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY).exists():
        raise RuntimeError("Refusing to overwrite an existing author-ready Grand Lizard artifact")
    for path, payload in products(root).items():
        write_bytes(root / path, payload)


def verify_evidence(root: Path = ROOT) -> None:
    from build_external_evidence_manifest import build_manifest, check_manifest
    names = ("PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_VPX_SOURCES_ROOT")
    if any(not os.environ.get(n) for n in names):
        raise RuntimeError("Grand Lizard manual, review-artifacts and VPX evidence roots must all be configured")
    manuals, review, vpx = [Path(os.environ[n]) for n in names]
    verify_excerpts(root)
    manifest_records = {record["id"]: record for record in load_json(manuals / "manifest.json")["documents"]}
    for source_id, acquired_at in ((MANUAL, MANUAL_ACQUIRED), (PRELIMINARY, PRELIMINARY_ACQUIRED)):
        if manifest_records.get(source_id, {}).get("acquired_at") != acquired_at:
            raise RuntimeError(f"Grand Lizard retained manual acquisition metadata drifted: {source_id}")
    for filename, digest in [("Williams_1986_Grand_Lizard_Manual.pdf", MANUAL_HASH), ("Williams_1986_Grand_Lizard_Preliminary_Manual.pdf", PRELIMINARY_HASH)]:
        if sha256(manuals / "by-machine" / MACHINE_ID / filename) != digest:
            raise RuntimeError(f"Grand Lizard retained manual drifted: {filename}")
    from tempfile import TemporaryDirectory
    from render_excerpt_image import DEFAULT_MAX_WIDTH, DEFAULT_MIN_GLYPH_PIXELS, render
    lockout = next(e for s in sources(root) if s["id"] == PRELIMINARY
                   for e in s["excerpts"] if e["id"] == "coin-lockout-wiring")
    with TemporaryDirectory() as temporary:
        derivation, digest = render(
            manuals / "by-machine" / MACHINE_ID / "Williams_1986_Grand_Lizard_Preliminary_Manual.pdf",
            14, Path(temporary) / "coin-lockout-wiring.webp", (0.335, 0.245, 0.45, 0.44),
            DEFAULT_MIN_GLYPH_PIXELS, DEFAULT_MAX_WIDTH, 80, rotate=270, color=False)
    if (derivation, digest) != (lockout["image_derivation"], lockout["image_sha256"]):
        raise RuntimeError("Grand Lizard coin-lockout crop drifted from native PDF pixels")
    for table in data.TABLES:
        directory = vpx / table["directory"]
        extraction = directory / "extraction"
        manifest = build_manifest(extraction, "grand_l4")
        actual = (check_manifest(extraction, "grand_l4"), len(manifest["files"]), sum(f["size"] for f in manifest["files"]))
        if actual != (table["manifest_sha256"], table["file_count"], table["total_bytes"]):
            raise RuntimeError(f"Grand Lizard retained extraction drifted: {table['build']}")
        if sha256(directory / table["filename"]) != table["sha256"] or sha256(extraction / "script.vbs") != table["script_sha256"]:
            raise RuntimeError("Grand Lizard retained table/script drifted")
    if sha256(review / "vpm-script-libs/s11.vbs") != VPM_S11_SHA256 or sha256(review / "vpm-script-libs/core.vbs") != VPM_CORE_SHA256:
        raise RuntimeError("Grand Lizard retained script library drifted")
    from grand_lizard_spatial import verify_spatial
    from grand_lizard_runtime_evidence import build as runtime_build
    verify_spatial(root, vpx, manuals, review)
    if canonical_bytes(runtime_build(review)) != (root / RUNTIME).read_bytes():
        raise RuntimeError("Grand Lizard compact runtime evidence drifted from raw runs")
    photos = review / "grand-lizard-1986/physical-photos"
    if check_manifest(photos, "grand_l4") != "2263cba9550c6cba7004b66f3172b390cd1178ae8c00af768e9469bf02703b49":
        raise RuntimeError("Grand Lizard owner/photo evidence drifted")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--verify-evidence", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    elif args.verify_evidence:
        verify_evidence()
    else:
        generate()


if __name__ == "__main__":
    main()
