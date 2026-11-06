"""Rebuild the two Radical editions from reviewed, immutable factual evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pinmame_game_defs.validation import validate_against_schema, validate_machine
from pinmame_flipper_column import (flipper_column_inputs, flipper_column_relationships,
                                   VPM_LIBRARY_SOURCE, VPM_LIBRARY_URI, VPM_S11_SHA256)
from radical_spatial import apply_spatial, build_report, report_markdown, verify_spatial_evidence
from radical_evidence import extra_sources, verify_external_evidence, REGISTER
from radical_knowledge import render_knowledge
from pinmame_game_defs.jsonio import canonical_bytes, write_bytes

REV = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
MANUAL_SHA = "a5085eb4c9088f3cba48949dba9f30a72c8aa3f30208d4f65150cc6e1f777cb6"
TABLE_SHA = "03767a7b25e53d6d104fa807a48819552825b7a8b57a09dba5a12ad99a1bc77e"
SEEDS = ROOT / "tools/seeds/bally"
MANUAL = SEEDS / "radical-1990-manual.json"
ALIASES = SEEDS / "radical-1990-legacy-aliases.json"
EXCERPTS = {
    "assemblies-and-displays.md": "f8f743ef3d46163da6880b232562c24d0d8c440465cb2577d9612dd24d77ba44",
    "competition-author.md": "83a4018e5eee4bc5ab8b6ff53be259b9e08253625c27a644409d8a18e3094c2c",
    "handbook-tables.md": "31214d3cda62bf8bdc9effabe8b57a524adde3dad7693d02161884d6c4907249",
    "jpsalas-6-editions.md": "1500e38e34d2339069eff76b877ac8d12df20988da879538bd934a2b27bbf09a",
    "jpsalas-script.md": "557dc5839ff2009f55df9928110bbc08d14981c7be6870a87bf33df3b524e198",
    "lamp-location-measurements.md": "75d8b1d9b700fc2e99f8732448c4cb86d56ee54c3b3a8b2ebef589df2e7c9528",
    "parts-lighting.md": "001fc855d8919f1c6ba106d0a1d6101755d2ca3478daee5936c27b8c4f985683",
    "physical-photo-observations.md": "d4eb757469fbad267aca3dcd40010dec9c9cfe2c8cd95ad8ae817c4b729b1267",
    "pinned-controller.md": "d0899058ee542ca62ca3a192283e5651131f8b7437b84959b441ce49bc2d6396",
    "solenoid-location-measurements.md": "90715e0582ef68effd6f1c6e84b682bb8b343b69e1c9207e7d935f11ce69ae02",
    "switch-location-measurements.md": "47b403c62408f63c9b82fd0b59567b6bd677ccfaf917da8e0ea5c7477f7f6958",
    "vpm-library.md": "f8e8aca1f55681c40dc45394b4886386316dbc4ef06f24cecd01c403287c5b7a",
    "vpw-mesh-origins.md": "080a06fa1b4935781b833a420902bc815aea1cf3892b1a18bd808ab286c68132",
    "vpw-retained-bindings.md": "f4d74644884c7b16a23e857386bee7a453158222d6e1128ed61391f0a47ecc36",
    "vpw-script.md": "d93afb811915fd290135c2f2a1e7db5fe1efd121d541cbf049902231c4979f50"
}
RUNTIME = {
    "g1": "49f6e475184e6f326ef4b67032cee5fc6166c5a30a9fe96c4f15e643d63414b7",
    "l1": "5bf975d40893dbbabd1566f9ad1336193062b2ab89918bfa0e960c2fafde0e81",
    "p3": "be59d04be917dde19b19443cbdbaac9bfda847a3d31be641d06793c914f6f1e7"
}
CHECKED_INPUTS = {
    "tools/seeds/bally/radical-1990-evidence.json": "b1dc89b9f1ba2d0f44c4d468427aa7e344e78d6e1f1b850ab1c5b93a19d9a209",
    "tools/seeds/bally/radical-1990-family.json": "68e0cc80594167b296b2527f43b04cbd1fabfaf58d0449a9cbb51dbd5f2b8974",
    "tools/seeds/bally/radical-1990-frame-readings.json": "35b261703ce340a64ba9327496f9321d0cff27754360755e3b03aea34468f5db",
    "tools/seeds/bally/radical-1990-spatial.json": "e5167dd26d49b3f2b2e389eff00718300b47ea7c677dcc0a4d32bbde78a2b206"
}
SW, DIP, SOL, LAMP = "pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp"
MAN, CORE, GAME, SCRIPT, VPW = "manual.radical", "pinmame.core", "pinmame.radical", "vpx.radical.script", "vpx.prototype.script"
FAMILY_SEED = SEEDS / "radical-1990-family.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(path: Path, expected: str) -> None:
    if not path.is_file() or digest(path) != expected:
        raise RuntimeError(f"Missing or changed pinned input: {path}")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(refs)}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def excerpt(name: str, locator: str, reviewed: bool) -> dict:
    path = f"evidence/excerpts/bally.radical.1990/{name}"
    checked(ROOT / path, EXCERPTS[name])
    return {"id": "excerpt." + name.replace(".md", ""), "path": path, "sha256": EXCERPTS[name],
            "locator": locator, "method": "mixed",
            "transcribed_by": "curator; visually checked by primary curator" if reviewed else "curator", "reviewed": reviewed}


def sources() -> list[dict]:
    repo = "https://github.com/vpinball/pinmame"
    out = [
        {"id": MAN, "kind": "manual", "uri": "https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf",
         "sha256": MANUAL_SHA, "source_id": "1904", "original_filename": "Bally_1990_Radical_Operator_Handbook.pdf",
         "acquired_at": "2026-11-06T08:42:02.203570Z",
         "locator": "Verified machine page https://www.ipdb.org/machine.cgi?id=1904; freshly reacquired https://web.archive.org/web/20220706192009id_/https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf; Operator Handbook 16-2015-101, April1990, PDF50,64-65,71,73,76-77,80-85; original older download time unrecorded, fresh acquisition bytes match it exactly",
         "license": "Manufacturer copyright; no redistribution license asserted", "attribution": "Midway Manufacturing Company / Bally, 1990; Internet Pinball Database hosting",
         "excerpts": [excerpt("handbook-tables.md", "PDF 80-85; whole printed lamp, switch, solenoid and matrix regions", True), excerpt("assemblies-and-displays.md", "PDF 50,64-65,71,73,76-77; whole cited construction tables and problem-analysis paraphrase", True)]},
        {"id": GAME, "kind": "pinmame_core", "uri": repo + "/blob/" + REV + "/src/wpc/s11games.c", "revision": REV,
         "sha256": "f7c45dafbb63cee75e485cf64ea9fff8452cb3531f68df89fad9e8ff71848b5f",
         "locator": "src/wpc/s11games.c lines 45-48 and 1530-1572; gen.h GEN_S11C", "license": "PinMAME license", "attribution": "PinMAME contributors"},
        {"id": CORE, "kind": "pinmame_core", "uri": repo + "/blob/" + REV + "/src/wpc/core.c", "revision": REV,
         "sha256": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
         "locator": "src/wpc/core.c core_getSol, core_updateSw and core_swSeq2m; exact per-file hashes and numbered source regions in excerpt", "license": "PinMAME license", "attribution": "PinMAME contributors",
         "excerpts": [excerpt("pinned-controller.md", "Pinned s11games.c, s11.c, core.c, core.h, gen.h; exact line spans and file digests", True)]},
        {"id": "pinmame.system11", "kind": "pinmame_core", "uri": repo + "/blob/" + REV + "/src/wpc/s11.c", "revision": REV,
         "sha256": "03784af9fe444b3da56f72192a5b04da1aa72938435f3d902d94ab47c0f8bd9e",
         "locator": "src/wpc/s11.c pia4a_r, S11_MUXSW2 and per-game solenoid types", "license": "PinMAME license", "attribution": "PinMAME contributors"},
        {"id": "pinmame.catalog", "kind": "pinmame_catalog", "uri": repo, "revision": REV,
         "sha256": "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5",
         "locator": "PinmameGetGames; retained catalog and pinned native library", "license": "PinMAME license", "attribution": "PinMAME contributors"},
        {"id": "ipdb.radical", "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1904",
         "sha256": "52b7da2e5d8ea548413cc230fe488338a069afde0ec81424ccd153ce2a1b1bf2",
         "locator": "Retained page review-artifacts/radical-1990/ipdb/ipdb-1904-page.html; acquisition time unknown; prototype popper and sling difference",
         "license": "Copyright IPDB; no redistribution license asserted", "attribution": "Internet Pinball Database"},
        {"id": "opdb.snapshot.690f784a7968", "kind": "human_review", "uri": "https://mp-data.sfo3.cdn.digitaloceanspaces.com/latest-opdb.json",
         "revision": "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93",
         "sha256": "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93",
         "locator": "machineGroups[G59ZY] and production record G59ZY-MD8p7", "license": "NOASSERTION",
         "attribution": "Open Pinball Database contributors", "acquired_at": "2026-08-14T17:53:43Z"},
        {"id": "vpx.radical.table", "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/radical-1990/source/Radical! (Bally 1990).vpx",
         "sha256": TABLE_SHA, "locator": "Retained JPSalas table; extracted with vpxtool", "license": "Copyright authors; no redistribution license asserted", "attribution": "JPSalas and table contributors"},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/radical-1990/extracted-vpxtool/script.vbs",
         "sha256": "7e4e81501c8713589ce21c0d1b3b136122357145056cf62c4ecf5212c1b5e584",
         "locator": "vpxtool-extracted script.vbs; source table SHA-256 " + TABLE_SHA,
         "license": "Copyright authors; no redistribution license asserted", "attribution": "JPSalas and table contributors", "known_working": True,
         "excerpts": [excerpt("jpsalas-script.md", "selected script lines", False)]},
        {"id": VPW, "kind": "vpx_script", "uri": "external:pinmame-source-checkouts/vpxtable_scripts/Radical (Bally 1990) Prototype _VPWmod_v1.0.1.vbs",
         "revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e", "sha256": "04c23692dad50b977cc2ebc529a66248a4e31b38a1286f0b870bfb24c079b593",
         "locator": "selected prototype script lines; table convenience timing is not physical evidence",
         "license": "Copyright authors; no redistribution license asserted", "attribution": "VPW table and script authors",
         "excerpts": [excerpt("vpw-script.md", "selected script lines", False)]},
        {"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "sha256": VPM_S11_SHA256,
         "locator": "s11.vbs lines37-40,69-122: flipper constants and key handlers; retained VPinMAME script library", "license": "VPinMAME project license", "attribution": "VPinMAME contributors",
         "excerpts": [excerpt("vpm-library.md", "s11.vbs flipper keys and core.vbs ball-stack/flipper contract", True)]},
        {"id": "vpm-script-library.core-vbs", "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/core.vbs",
         "sha256": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69", "locator": "cvpmBallStack.InitSw1038-1042, InitKick1050; synthetic flipper constants2862-2863", "license": "VPinMAME project license", "attribution": "VPinMAME contributors",
         "excerpts": [excerpt("vpm-library.md", "core.vbs ball-stack and flipper contract", True)]},
        {"id": "legacy.radical", "kind": "legacy_json", "uri": "https://github.com/vpinball/pinmame-game-defs",
         "revision": "4ea106d080728648a693af3b4dcabb091eee0a02", "locator": "games/rad.json and platforms/system11.json; address-keyed alias seed", "attribution": "pinmame-game-defs contributors"},
    ]
    for suffix, sha in RUNTIME.items():
        path = f"evidence/runtime/system-11/radical-{suffix}-service-tests.json"
        checked(ROOT / path, sha)
        run = load(ROOT / path)
        if run.get("runtime", {}).get("game") != "radcl_" + suffix:
            raise RuntimeError(f"Wrong runtime evidence identity: {path}")
        out.append({"id": "runtime." + suffix, "kind": "runtime_scenario", "uri": path, "sha256": sha,
                    "revision": REV, "locator": "compact service-test observations and run-attributed limitations",
                    "license": "Project evidence; no ROM bytes", "attribution": "pinmame-game-defs contributors",
                    "excerpts": [{"id": "excerpt.runtime-" + suffix, "locator": "runtime.observations.runs",
                                  "path": path, "sha256": sha,
                                  "method": "mixed", "transcribed_by": "Deterministic raw-segment reader; implementation checked by primary curator", "reviewed": False}]})
    return out + extra_sources(ROOT)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def aliases(seed: dict, group: str, address: int, namespace: str) -> list[dict]:
    old = seed["groups"].get(group, {}).get(str(address), [])
    result = [{"namespace": namespace, "value": str(address)}]
    for alias in old:
        if alias not in result:
            result.append(alias)
    return result


def make_device(identifier: str, label: str, kind: str, group: str, address: int,
                availability: str, refs: tuple[str, ...], alias_seed: dict, namespace: str) -> dict:
    return {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
            "aliases": aliases(alias_seed, group, address, namespace), "availability": availability,
            "provenance": provenance(*refs)}


def clean(value: str) -> str | None:
    return None if not value or "[" in value or value.lower() == "not used" else value


def matrix_wiring(row: dict, lamp: bool = False) -> dict:
    pairs = {"driver_transistor": "column_transistor", "drive_wire": "column_wire", "drive_connection": "column_connector",
             "return_wire": "row_wire", "return_connection": "row_connector"}
    if lamp:
        pairs["return_component"] = "row_transistor"
    return {dest: row[src] for dest, src in pairs.items() if clean(row.get(src, ""))}


def build_inputs(manual: dict, legacy: dict, prototype: bool) -> list[dict]:
    result = []
    for address, label in [(-7, "Advance"), (-6, "Auto Up / Manual Down"), (-5, "CPU Diagnostics"), (-4, "Sound Diagnostics")]:
        d = make_device("switch." + slug(label), label, "switch", SW, address, "used", (CORE,), legacy, "pinmame.switch")
        d.update(normally_closed=False, physical={"location": "cabinet service", "switch_type": "button", "notes": "Public closure is 1 through the platform's direct diagnostic read path; Auto-Up/Manual-Down is a maintained selector, the others momentary buttons."}, spatial=na("cabinet_or_service", CORE))
        result.append(d)
    parts = {int(r["item"]): r["part_no"] for r in manual["switch_inventory"] if r["item"].isdigit()}
    for row in manual["switch_matrix"]:
        n = row["manual_number_expected"]
        label = row["name"]
        if n == 2: label = "A/C select relay feedback"
        if n == 16 and not prototype: label = "Snake Run"
        if n == 28 and not prototype: label = "Spot Letter"
        if n == 49 and not prototype: label = "Not used"
        if n in (57, 58): label += " (matrix copy)"
        unused = label.lower() == "not used"
        virtual = n in (2, 57, 58)
        ident = f"switch.{slug(label)}-{n}" if not unused else f"switch.unused-{n}"
        d = make_device(ident, label, "virtual" if virtual or unused else "switch", SW, n,
                        "unused" if unused else "optional" if n == 5 else "used", (MAN, CORE, "pinmame.system11"), legacy, "pinmame.switch")
        if n in (16, 49): d["provenance"]["source_refs"] += (["runtime.p3"] if prototype else ["runtime.l1", "runtime.g1"]) + ["ipdb.radical", SCRIPT]
        if virtual or unused:
            d["spatial"] = na("unused" if unused else "virtual", CORE)
            if n == 2:
                d["physical"] = {"notes": "Manual prints Not Used, but S11_MUXSW2 publishes A/C select relay feedback here; the value is virtual."}
            elif n in (57, 58):
                d["physical"] = {"notes": "PinMAME copies cabinet button state here on each update; the host drives the flipper-column input instead."}
        else:
            phys = {"location": "cabinet" if n <= 8 else "playfield"}
            part = clean(parts.get(n, ""))
            if part and not (n == 16 and not prototype):
                phys["assembly_part_number" if part.startswith("p/o ") else "part_number"] = part.removeprefix("p/o ")
            if n in (22, 23, 24, 30, 31, 32):
                phys.update(switch_type="opto", notes="C-11223-4 contains C-13205-1 optical board with three interrupters (complete tables on PDF76/77 retained). The matrix has no shading, but the assembly establishes construction. s11.c reads the uninverted matrix, INITGAME sets no invSw bits and the working cvpmDropTarget script closes at public1 when down, so the matrix contact normally rests open; this is not inferred from the optical beam.")
            if n == 20: phys.update(switch_type="microswitch", notes="Bowtie assembly C-13809 on PDF73 contains mini microswitch 5647-12073-06 and shaft B-13629; this is physical feedback despite the script's toggled-state substitution.")
            if n == 16 and not prototype: phys.update(switch_type="unknown", notes="Production service test names SNAKE RUN and the retained table binds a standup HitTarget, replacing the manual's prototype ball popper. The production contact's exact part/construction is not documented here. Public1 is the active closure in the uninverted System11 read path; the VPX handler supplies that level.")
            if n == 5: phys["notes"] = "Center coin provision depends on two- or three-slot coin door; inventory prints Not Used."
            if n in (49, 55, 56):
                phys.update(part_number="SW-1A-120", switch_type="leaf", notes="The whole inventory row lists SW-1A-114 for Kick and SW-1A-120 for Score on this sling. This matrix address is the scoring contact; the separate kick contact belongs to the physical mechanism and is not another matrix input.")
            if n == 28:
                phys["notes"] = "The April 1990 Operator Handbook 16-2015-101 depicts prototype fitment and names Advance Bonus X; production L1/G1 Switch Levels names SPOT LETTER, while P3 names ADV BONUS X. Construction remains the same standup assembly."
            d["physical"] = phys
            d["wiring"] = matrix_wiring(row)
            d["normally_closed"] = False
            if n in (11, 12): d["initial_active"] = True
            if n in (49, 50, 52, 53, 54, 55, 56): d["pulse"] = True
            if n <= 8: d["spatial"] = na("cabinet_or_service", MAN)
        result.append(d)
    column = flipper_column_inputs(flip_swno=(58, 57), flip_swno_text="FLIP_SWNO(58,57)", core_refs=(CORE, GAME, "pinmame.system11"),
        button_refs=(SCRIPT, VPM_LIBRARY_SOURCE), button_notes={"left": "Two physical flippers share this cabinet chain.", "right": "Two physical flippers share this cabinet chain."}, button_normally_closed=False)
    for d in column:
        n = d["binding"]["device"]
        d["aliases"] = aliases(legacy, SW, n, "pinmame.switch")
    result.extend(column)
    dip = make_device("switch.country-jumper", "Country jumper", "dip_switch", DIP, 0, "used", (GAME,), legacy, "pinmame.dip")
    dip.update(physical={"location": "CPU board", "switch_type": "dip"}, spatial=na("dip_switch", GAME))
    result.append(dip)
    return result


def build_outputs(manual: dict, legacy: dict, prototype: bool) -> list[dict]:
    rows = {r["printed_number"]: r for r in manual["solenoid_table"]}
    result = []
    for n in range(1, 65):
        key = f"{n:02d}A" if n <= 8 else f"{n - 24:02d}C" if 25 <= n <= 32 else f"{n:02d}"
        row = rows.get(key)
        unused = n == 24 or n >= 33 and n not in (45, 46, 47, 48)
        unfitted = not prototype and n in (3, 15)
        virtual = n == 23 or n >= 33 or n == 24
        label = row["function"] if row else ("Switched solenoid enable" if n == 23 else f"Synthetic flipper {n}" if 45 <= n <= 48 else f"Unused output {n}")
        if unfitted: label = f"Unfitted production {label} driver"
        if unused: label = f"Unused output {n}"
        kind = "virtual" if virtual or unused else "flasher" if n in (9, 16) or 25 <= n <= 32 else "gi" if n in (10, 11) else "relay" if n == 12 else "coil"
        d = make_device(f"output.{slug(label)}-{n}", label, kind, SOL, n, "unused" if unused or unfitted else "used", (MAN, CORE, "pinmame.system11"), legacy, "pinmame.solenoid")
        if n == 16:
            for alias in legacy["groups"].get(LAMP, {}).get("116", []):
                if alias not in d["aliases"]: d["aliases"].append(alias)
            d["provenance"]["source_refs"] += [SCRIPT, "legacy.radical"]
        if n in (3, 15): d["provenance"]["source_refs"] += (["runtime.p3"] if prototype else ["runtime.l1", "runtime.g1"]) + ["ipdb.radical"]
        if virtual or unused:
            d["spatial"] = na("unused" if unused else "virtual", CORE)
            if n == 23: d["physical"] = {"notes": "Virtual switched-solenoid enable; service test turns it on."}
            if 45 <= n <= 48: d["physical"] = {"notes": "Synthetic flipper state, not a separate coil or EOS contact."}
        elif unfitted:
            d["provenance"]["source_refs"] += ["photo.radical.10", "photo.radical.13"]
            notes = "Production omits this prototype load (physical edition photos, IPDB listing and production service name NOT USED). The Coil Test sweeps its address without a load."
            if n == 15:
                notes += " Output 15 also rises/clears with the entire controlled byte 9-16 at power-up in all three initialization traces; that shared byte transient is checked in compact runtime evidence."
            d["physical"] = {"notes": notes + " These explained states do not imply fitment; unused does not mean constant zero."}
            d["spatial"] = na("unused", "ipdb.radical", "runtime.l1", "runtime.g1")
        else:
            notes = ""
            if n in (13, 14): notes += "Printed table repeats 5J2-4 for coils 13 and 14; retained literally. "
            if n in (10, 11): notes += "Relay energization extinguishes this GI string; table script simplifies both strings to one callback. "
            if n == 12: notes += "Internal A/C select relay, also published as switch 2 feedback. "
            phys = {"part_number": row["part"], "notes": notes.strip() or "Manual load identity; observed emitter/effect placements are recorded separately where available. Fitted socket and coil centers have not been physically surveyed."}
            if n == 16:
                phys["notes"] += " Historical fake lamp 116 aliases are retained on this real solenoid 16 flasher: SolCallback(16) calls SetLamp 116 as a script animation key. There is no controller lamp 116 binding."
            if kind == "flasher":
                q = row["quantity_location"]
                counts = re.findall(r"(\d+)([pb])", q)
                if counts: phys["quantity"] = sum(int(i) for i, _ in counts); phys["notes"] += f" Manual quantity/location: {q}."
                if n == 32:
                    phys["notes"] += " The printed 1p1b location split is erroneous: two photographed right-side domes, script binding both bases to 32, and two playfield ramps with black/gray H-13745 cables establish two playfield emitters. The full insert-panel BOM has seven #89 backbox flashlamps, allocated by 9, 28, 29, 30 x 3, 31; no extra 32 backbox bulb is invented. The top-center label on PDF 84 is blurred (6C/8C) and remote from the second output-32 dome; the drawing is not used to establish two 08C locations. Literal table marks remain in the excerpt."
                    d["provenance"]["source_refs"] += ["parts.radical", "photo.radical.2", "photo.radical.3", "vpx-script.radical.vpw-retained"]
            d["physical"] = phys
            d["wiring"] = {"driver_transistor": row["driver_transistor"], "drive_wire": row["wire_color"], "drive_connection": row["playfield_cabinet"]}
            if not row["cpu_board"].startswith("("): d["wiring"]["control_connection"] = row["cpu_board"]
            if n in (5, 11, 12): d["spatial"] = na("internal_nonvisual" if n == 12 else "cabinet_or_service", MAN)
        result.append(d)
    inventory = {r["item"]: r for r in manual["lamp_inventory"]}
    for row in manual["lamp_matrix"]:
        n = row["manual_number_expected"]
        label = "Loop Ramp 25K" if n == 42 else row["name"]
        d = make_device(f"lamp.{slug(label)}-{n}", label, "lamp", LAMP, n, "used", (MAN,), legacy, "pinmame.lamp")
        note = "Matrix and all three ROM service sets identify25K (raw decoder2SK, S/5 shared glyph); inventory prints50K. Label follows the matrix plus runtime, while both literal readings are preserved." if n == 42 else "Printed 6 in matrix; inventory identifies 60." if n == 60 else ""
        if n == 42: d["provenance"]["source_refs"] += ["runtime.l1", "runtime.g1", "runtime.p3"]
        if 57 <= n <= 62: note += " Backbox insert; printed location legend uses b inconsistently."
        d["physical"] = {"part_number": inventory[n]["part_no"], "location": "backbox insert" if 57 <= n <= 62 else "playfield"}
        if note.strip(): d["physical"]["notes"] = note.strip()
        if 57 <= n <= 62:
            d["physical"]["notes"] += " The general inventory prints #44, while the insert-panel BOM's C-13749 six-lamp snake PCB lists #555 and diodes. Both readings are retained; the exact socket type is not resolved solely by a bulb-count match. Structured part number follows this game's inventory, not an inferred board assignment."
            d["provenance"]["source_refs"].append("parts.radical")
        d["wiring"] = matrix_wiring(row, lamp=True)
        if 57 <= n <= 62: d["spatial"] = na("cabinet_or_service", MAN)
        result.append(d)
    return result


def mechanisms(prototype: bool, inputs: list[dict], outputs: list[dict]) -> list[dict]:
    entries = [
        ("trough", "Two-ball trough and feeder", "kicker", [1, 2], [10, 11, 12, 14], "Switch 10 is the outhole, 11 and 12 the two trough positions, and 14 the shooter lane. Coil 1 transfers the drain and coil 2 feeds the shooter; script starts with two balls."),
        ("lock", "Two-position ball lock", "gate", [8], [38, 39, 40], "Lock lane 38 leads to the visible lock: 40 is front and 39 rear. Coil 8 releases its gate; it does not directly actuate the ball sensors."),
        ("bottom-bank", "Bottom three-drop bank", "drop_target_bank", [6], [22, 23, 24], "Three optical down sensors remain active while targets are down; coil 6 and the shared reset plate restore the bank. C-11223-4 contains optical board C-13205-1; both whole parts tables are retained. The table's sounds and target reset timing are implementation tuning, not measured machine motion."),
        ("top-bank", "Top three-drop bank", "drop_target_bank", [4], [30, 31, 32], "Three optical down sensors remain active while targets are down; coil 4 and the shared reset plate restore the bank. C-11223-4 contains optical board C-13205-1. Targets can jam individually; the reset actuator restores the bank together."),
        ("bowtie", "Bowtie diverter", "diverter", [7], [20], "One enabled pulse toggles the two-position latch through its flat cam; switch 20 reports position. The script alternates DiverterDown/Up and public20 only on the enabled edge; its initial wall pose is a table startup choice, not a measured factory home. No travel time is measured. A stuck microswitch can misreport which ramp branch is selected."),
        ("right-gate", "Right ball gate", "gate", [13], [], "Coil 13 controls right ball routing."),
        ("kickback", "Left outlane kickback", "kicker", [14], [51], "Left outlane switch 51 and coil 14 serve the kickback."),
        ("flippers", "Four flippers", "other", [45, 46, 47, 48], [82, 84], "Four physical flippers in two cabinet button chains. Outputs 45-48 are synthetic states, not individual windings or EOS outputs."),
        ("jets-slings", "Four jets and two slings", "other", [17, 18, 19, 20, 21, 22], [50, 52, 53, 54, 55, 56], "Four jet and two sling assemblies use special drivers 1-6, published at 17-22. The own-ROM isolated score-contact probes produce52->17,55->18,53->19,56->20,54->21,50->22. These prove the ROM response, not physical kick-contact topology or measured mechanical latency."),
        ("spinners", "Top and right spinners", "other", [], [17, 29], "Ball-driven spinners coast by inertia; there is no motor actuator."),
    ]
    if prototype:
        entries += [("popper", "Prototype ball popper", "kicker", [3], [16], "Prototype adds the popper; timed ejection in the corroborating script is a table convenience, not a measured machine delay."),
                    ("top-sling", "Prototype top sling", "kicker", [15], [49], "Prototype adds a top sling; production omits it.")]
    input_ids = {d["binding"]["device"]: d["id"] for d in inputs if d["binding"]["group"] == SW}
    output_ids = {d["binding"]["device"]: d["id"] for d in outputs if d["binding"]["group"] == SOL}
    result = []
    for ident, label, kind, actuators, sensors, behavior in entries:
        d = {"id": "mechanism." + ident, "label": label, "kind": kind,
             "actuators": [output_ids[a] for a in actuators],
             "sensors": [input_ids[a] for a in sensors],
             "behavior": behavior, "provenance": provenance(MAN, SCRIPT, VPW if prototype else CORE)}
        if ident.endswith("-bank"): d["assembly_part_number"] = "C-11223-4"
        if ident == "jets-slings": d["provenance"]["source_refs"].append("runtime.p3" if prototype else "runtime.l1")
        result.append(d)
    return result


def build(prototype: bool = False) -> dict:
    for relative, expected in CHECKED_INPUTS.items():
        checked(ROOT / relative, expected)
    for name, expected in EXCERPTS.items():
        checked(ROOT / "evidence/excerpts/bally.radical.1990" / name, expected)
    checked(MANUAL, "d9664009b3ba523f8d74caa9a3d602099837bc46b094e538676ad018cdb4f928")
    checked(ALIASES, "26b25a8f7cf9df7cdea24dbf0add9fb1c4d0348628af35937e704fb75902bd02")
    manual, legacy = load(MANUAL), load(ALIASES)
    if manual.get("pdf_sha256") != MANUAL_SHA or len(manual.get("switch_matrix", [])) != 64 or len(manual.get("lamp_matrix", [])) != 64 or len(manual.get("solenoid_table", [])) != 30:
        raise RuntimeError("Incomplete or incorrect manual seed")
    if legacy.get("format") != "radical-legacy-aliases-v1": raise RuntimeError("Invalid alias seed")
    src = sources()
    catalog = load(ROOT / "catalog/pinmame.json")
    if catalog["source"]["pinmame_revision"] != REV: raise RuntimeError("Wrong catalog revision")
    ids = {"radcl_p3"} if prototype else {"radcl_l1", "radcl_g1", "radcl_l1c"}
    drivers = []
    for entry in catalog["drivers"]:
        if entry["id"] not in ids: continue
        d = {k: entry[k] for k in ("id", "clone_of", "description", "year", "manufacturer", "flags") if k in entry}
        d["physical_compatibility"] = "identical"
        d["variant_notes"] = {
            "radcl_l1": "Production L-1; its own service tests name the Snake Run target and omit the prototype popper/top sling.",
            "radcl_g1": "German LG-1 language firmware on identical production System11C hardware; unchanged init, routing, display and sound-board layout, and its own successful service tests confirm production fitment.",
            "radcl_l1c": "2018 competition patch aa9e changes production software, not fitted hardware. Identical compatibility is inferred from the author's exact software-only release, an owner's earlier physical installation in the same patch series, and unchanged pinned routing; no replay of this exact patched archive is claimed. See author.radical.competition.",
            "radcl_p3": "P-3 physical prototype with ball popper3/sensor16 and upper sling15/score49. Own service tests and photographed prototype hardware establish this edition; it is not grouped into production merely because init/routing are shared.",
        }[d["id"]]
        drivers.append(d)
    if {d["id"] for d in drivers} != ids: raise RuntimeError("Catalog does not contain expected drivers")
    machine = {"id": "bally.radical-prototype.1990" if prototype else "bally.radical.1990", "name": "Radical! (Prototype)" if prototype else "Radical!", "manufacturer": "Bally", "year": 1990, "model_number": "2015", "ipdb_id": 1904}
    if not prototype: machine["opdb_id"] = "G59ZY-MD8p7"
    missing = ["identity", "spatial_placement"] if prototype else ["input_semantics", "spatial_placement"]
    displays = [{"id": f"display.line-{i+1}", "label": f"Alphanumeric display line {i+1}", "kind": "segment", "controller_index": i, "segment_start": start,
                 "width": 16, "height": 1, "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", GAME, MAN), "provenance": provenance(GAME, MAN)} for i, start in enumerate((0, 20))]
    inputs = build_inputs(manual, legacy, prototype)
    outputs = build_outputs(manual, legacy, prototype)
    matrix_ids = {d["binding"]["device"]: d["id"] for d in inputs if d["binding"]["group"] == SW}
    output_ids = {d["binding"]["device"]: d["id"] for d in outputs if d["binding"]["group"] == SOL}
    relations = flipper_column_relationships(flip_swno=(58, 57), matrix_ids=matrix_ids, refs=(GAME, CORE))
    relations.append({"id": "relationship.ac-relay-feedback", "kind": "direct", "source": output_ids[12], "destination": matrix_ids[2], "provenance": provenance(GAME, "pinmame.system11")})
    for sensor, coil in [(50, 22), (52, 17), (53, 19), (54, 21), (55, 18), (56, 20)] + ([(49, 15)] if prototype else []):
        relations.append({"id": f"relationship.score-{sensor}-drive-{coil}", "kind": "pulse", "source": matrix_ids[sensor], "destination": output_ids[coil], "provenance": provenance("runtime.p3" if prototype else "runtime.l1", SCRIPT)})
    definition = {"format": "pinmame-machine-definition", "schema_version": 2, "machine": machine,
            "coverage": {"status": "partial", "missing": missing, "dimensions": {"catalog_identity": "observed" if prototype else "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "observed", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed"}},
            "controller": {"platform": "pinmame.system-11", "hardware_generation": "0x400", "inversion_applied_by_emulator": True},
            "drivers": drivers, "inputs": inputs, "outputs": outputs,
            "displays": displays, "mechanisms": mechanisms(prototype, inputs, outputs), "relationships": relations, "sources": src,
            "knowledge": {"path": "knowledge/bally/radical-prototype-1990.md" if prototype else "knowledge/bally/radical-1990.md", "status": "complete"}, "conflicts": []}
    return apply_spatial(definition, ROOT)


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--regenerate", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    verify_external_evidence(ROOT)
    verify_spatial_evidence(ROOT)
    products = []
    for prototype in (False, True):
        name = "radical-prototype-1990" if prototype else "radical-1990"
        ready = ROOT / f"machines/author-ready/bally/{name}.json"
        if ready.exists(): raise RuntimeError(f"Refusing to overwrite author-ready record: {ready}")
        definition = build(prototype)
        # New knowledge files are among the products; validate filesystem references
        # after generation, and require them immediately in the read-only check.
        errors = validate_machine(definition, ROOT if args.check else None) + validate_against_schema(definition, ROOT / "schemas/machine.schema.json", name)
        if errors: raise RuntimeError("Invalid definition:\n" + "\n".join(errors))
        for path in (SEEDS / f"{name}.json", ROOT / f"machines/partial/bally/{name}.json"):
            products.append((path, canonical_bytes(definition)))
        report = build_report(definition, ROOT)
        report_errors = validate_against_schema(report, ROOT / "schemas/spatial-report.schema.json", name)
        if report_errors: raise RuntimeError("Invalid spatial report: " + "\n".join(report_errors))
        products.extend([
            (ROOT / definition["knowledge"]["path"], render_knowledge(prototype).encode("utf-8")),
            (ROOT / f"reports/spatial/bally/{name}.json", canonical_bytes(report)),
            (ROOT / f"reports/spatial/bally/{name}.md", report_markdown(report).encode("utf-8")),
        ])
    family = load(FAMILY_SEED)
    family_errors = validate_against_schema(family, ROOT / "schemas/family.schema.json", "Radical family")
    if family_errors: raise RuntimeError("Invalid family: " + "\n".join(family_errors))
    products.append((ROOT / "families/opdb/g59zy.json", canonical_bytes(family)))
    for path, content in products:
        if args.check:
            if not path.is_file() or path.read_bytes() != content: raise RuntimeError(f"Generated file differs: {path}")
        else:
            write_bytes(path, content)
    for prototype in (False, True):
        errors = validate_machine(build(prototype), ROOT)
        if errors: raise RuntimeError("Invalid generated definition:\n" + "\n".join(errors))
    print("Radical definitions " + ("checked" if args.check else "regenerated"))


if __name__ == "__main__":
    main()
