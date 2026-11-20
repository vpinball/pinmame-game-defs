"""Gates for the Data East Last Action Hero (1993) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major address
arithmetic, the cabinet flipper addresses PinMAME mirrors into 63 and 64, the Left/Right relay pairing, the three
magnets on PIA2 port B, what the ROM's own service tests said about every public address, and the boundary between
what the retained recreation measured and what it did not (no matrix lamp or raised flash-lamp socket is placed on a
light-map source). The fixtures below are typed from the printed charts and the read DMD frames and kept apart from the
curator on purpose: a test that checks the generator against its own output only proves the generator is
self-consistent.

Tests that need retained evidence run only when its root is set and skip cleanly otherwise:
PINMAME_VPX_SOURCES_ROOT (the table extraction and its world-space export), PINMAME_REVIEW_ARTIFACTS_ROOT (the
harness runs), PINMAME_MANUALS_ROOT (the manual scans) and PINMAME_ROM_LIBRARY_ROOT (the ROM archive).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

KEY = "data-east.last-action-hero.1993"
SLUG = "last-action-hero-1993"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
AUTHOR_READY_PATH = ROOT / f"machines/author-ready/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
SPATIAL_MARKDOWN_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.md"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/last-action-hero-lah_112-service-tests.json"
RUNTIME_PATH = ROOT / "tools/last_action_hero_runtime.json"
PLACES_PATH = ROOT / "tools/last_action_hero_places.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY
VPX_ROOT = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
REVIEW_ROOT = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
MANUALS_ROOT = os.environ.get("PINMAME_MANUALS_ROOT")
ROM_ROOT = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
SOURCE_DIRECTORY = Path("data-east/last-action-hero-1993/vpw-1.1")
EXTRACTION_RELATIVE = SOURCE_DIRECTORY / "extracted-vpxtool"
WORLD_OBJ_RELATIVE = SOURCE_DIRECTORY / "world-obj/Last Action Hero (Data East 1993) VPW v1.1.obj"
SESSION_RELATIVE = Path("data-east.last-action-hero.1993/session-20261120/final/lah_112")
MANUALS = {
    "by-machine/data-east.last-action-hero.1993/ipdb-1416/Data_East_1993_Last_Action_Hero_Manual.pdf":
        "546f0272d7d2a4334224843fc1498077c45896cb8c492daa569ac07d3161c61d",
    "by-machine/data-east.last-action-hero.1993/ipdb-1416/Data_East_1993_Last_Action_Hero_Schematics_BW.pdf":
        "7925654b30802ba7246efdddcebb90cba62cffd39ad36945124d005fec30d702",
}
ROM_SHA256 = "3143ec1d9ff49c0344da87a3c8e5a8202d59322c5edee7bb903e0bb7affb6363"
TOOL_PATH = os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")])

# --- Independent fixtures ----------------------------------------------------------------------------------
# Printed switch chart cells, spread over all eight columns.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 2: "4th Coin", 3: "Credit Button", 7: "Slam Tilt", 8: "Launch Trigger", 9: "Trough #1 Left", 15: "Trough #7 Right",
    16: "Shooter Lane", 17: "Drop Target C", 21: "Drop Target E", 31: "Right Scoop Assem.", 34: "Bottom Turbo Bumper", 47: "VUK",
    48: "Ripper Kickback", 54: "Drop Target Bar (2)", 60: "Crane Left Limit", 61: "Crane Right Limit", 62: "Smart Missile",
    63: "Left Flipper", 64: "Right Flipper",
}
UNUSED_SWITCHES = set(range(49, 54))
# The ROM's Active Switch Test names, read from the retained frames.
ROM_SWITCHES = {
    1: "PLUMB TILT", 8: "LAUNCH BUTTON", 10: "TROUGH #2 M-L-L", 17: "DROP TARGET C BOTTOM", 21: "DROP TARGET E TOP", 34: "BOTTOM TURBO BUMPER",
    46: "LEFT RAMP ENTER", 54: "DROP TARGET BAR X2", 55: "RGT. CAPTIVE ROLLOVER", 62: "SMART MISSILE", 63: "LEFT FLIPPER", 64: "RIGHT FLIPPER",
    49: "NOT USED", 53: "NOT USED",
}
MANUAL_LAMPS = {
    1: "Grid: Find Benedict", 7: "Top Turbo Bumper", 17: "C", 31: "Captive Ball X2", 32: "Ticket", 40: "Return Lanes X2", 43: "Outlanes X2",
    55: "Shoot The Crane", 57: "Smart Missile", 58: "R", 63: "R", 64: "Credit Button",
}
ROM_LAMPS = {
    1: "GRID: FIND BENEDICT", 7: "BOTTOM TURBO BUMPER", 9: "GRID: BLOW OUT", 17: "-C-", 31: "CAPTIVE BALLS X2", 46: "RIPPER COLLECT",
    55: "CRANE READY", 57: "SMART MISSILE X2", 64: "CREDIT BUTTON",
}
# Cycling Coils names, read from the retained frames.
ROM_COILS = {
    1: "COIL: LOCK OUT", 3: "COIL: AUTO LAUNCH 50V", 4: "COIL: CRANE LOCK", 7: "COIL: LEFT LOCK", 9: "FLASH:2-INSERT 2-CRANE", 11: "RELAY: G.I.RELAY",
    14: "COIL: CRANE MOTOR", 16: "COIL: SHAKER MOTOR", 18: "COIL: BOTTOM TURBO", 22: "COIL: RIPPER PIT 50V", 25: "FLASH: 4-BIG RGT MARS",
    31: "FLASH: 4-BIG LEFT MARS", 32: "FLASH: 2-INS 1-TAR PIT",
}
DRIVER_ROMS = {
    "lah_112": ("lahcpua.112", "lahdispa.106"), "lah_f104": ("lahcpua.104", "lahdispf.101"), "lah_l104": ("lahcpua.104", "lahdispl.102"),
    "lah_c106": ("lahcpuc.106", "lahdispa.104"), "lah_107": ("lahcpua.107", "lahdispa.104"), "lah_l108": ("lahcpua.108", "lahdispl.104"),
    "lah_l108_105": ("lahcpua.108", "lahdispl.105"), "lah_110": ("lahcpua.110", "lahdispa.106"), "lah_113": ("lahcpua.113", "lahdispa.106"),
}
# Public magnet address -> (device id, Magnet Control Board output pin, MOSFET).
MAGNETS = {37: ("magnet.magnet-2", "Magnet Control Board J2-4", "Q2"), 38: ("magnet.magnet-1", "Magnet Control Board J2-3", "Q1"),
           39: ("magnet.magnet-3", "Magnet Control Board J2-7", "Q3")}
# Every output the record leaves without any spatial record, and every device that carries a cabinet record instead.
UNPLACED_OUTPUTS = {("solenoid", n) for n in (4, 8, 9, 11, 26, 27, 28, 29, 30, 32, 40, 41, 42, 43, 44)} | {("lamp", n) for n in range(1, 64)}
# The matrix lamps whose Lampz.MassAssign line binds one Light each; every other lamp below 64 lights two inserts.
BOUND_LAMPS = [n for n in range(1, 64) if n not in (31, 40, 43)]
CABINET_OUTPUTS = {("solenoid", n) for n in (10, 16, 25, 31)} | {("lamp", 64)}
PROJECTIONS = {("pinmame.output.solenoid", 13), ("pinmame.output.solenoid", 14)}
# The playfield switches the record leaves without a coordinate: the crane limits, whose factory callouts sit at the ends of the sweep.
UNPLACED_INPUTS = {60, 61}
FLASH_KEYS = {"solenoid.9", "solenoid.11", *(f"solenoid.{n}" for n in range(25, 33))}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def gameitems(extraction: Path) -> dict[str, tuple[str, dict]]:
    items = {}
    for path in (extraction / "gameitems").glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        kind = next(iter(data))
        items[data[kind]["name"].lower()] = (kind, data[kind])
    return items


def device_key(device: dict) -> str:
    group = device["binding"]["group"]
    prefix = {"pinmame.input.switch": "switch", "pinmame.output.solenoid": "solenoid", "pinmame.output.lamp": "lamp"}[group]
    return f"{prefix}.{device['binding']['device']}"


class DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}

    def test_identity_and_variants(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual((KEY, "Data East", 1993, 1416, "GRwyq-MW9lN", "500-5527-01"),
                         (machine["id"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"], machine["model_number"]))
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        self.assertEqual(set(DRIVER_ROMS), set(drivers))
        self.assertNotIn("clone_of", drivers["lah_112"])
        for driver_id, (cpu, display) in DRIVER_ROMS.items():
            driver = drivers[driver_id]
            self.assertEqual("unknown" if driver_id == "lah_l108_105" else "identical", driver["physical_compatibility"], driver_id)
            if driver_id != "lah_112":
                self.assertEqual("lah_112", driver["clone_of"], driver_id)
                if cpu != "lahcpua.112":
                    self.assertIn(cpu, driver["variant_notes"], driver_id)
                if display != "lahdispa.106":
                    self.assertIn(display, driver["variant_notes"], driver_id)
        self.assertEqual("2014", drivers["lah_113"]["year"])
        self.assertEqual({"1993"}, {d["year"] for i, d in drivers.items() if i != "lah_113"})
        self.assertIn("NO_DUMP", drivers["lah_l108_105"]["variant_notes"])
        self.assertIn("cGameName lah_113", drivers["lah_113"]["variant_notes"])

    def test_controller_platform(self) -> None:
        self.assertEqual({"platform": "pinmame.dataeast", "hardware_generation": "0x4000", "inversion_applied_by_emulator": True}, self.definition["controller"])

    def test_every_address_is_enumerated_once(self) -> None:
        self.assertEqual({*range(1, 65), -7, -6, *range(81, 89)}, set(self.inputs))
        self.assertEqual(["dip.jumper-w7"], [item["id"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"])
        (jumper,) = [item for item in self.definition["inputs"] if item["id"] == "dip.jumper-w7"]
        self.assertIn("PA7, pin 9 of the 6821 at 11B", jumper["physical"]["notes"])
        self.assertIn("taken to ground through a link labelled J8", jumper["physical"]["notes"])
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(["display.dmd"], [display["id"] for display in self.definition["displays"]])
        self.assertEqual((128, 32), (self.definition["displays"][0]["width"], self.definition["displays"][0]["height"]))

    def test_the_matrix_is_column_major(self) -> None:
        for address in range(1, 65):
            column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
            self.assertTrue(self.inputs[address]["physical"]["notes"].startswith(f"Printed switch-matrix column {column}, row {row};"), address)
            self.assertTrue(self.lamps[address]["physical"]["notes"].startswith(f"Printed lamp-matrix column {column}, row {row};"), address)
        self.assertEqual(("Q53", "CN8-3", "WHT-BLU", "CN10-3"), tuple(self.inputs[22]["wiring"][key] for key in ("driver_transistor", "drive_connection", "return_wire", "return_connection")))

    def test_rom_names_and_unused_switches(self) -> None:
        for address, name in ROM_SWITCHES.items():
            self.assertIn(f"'{name}'", self.inputs[address]["physical"]["notes"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("unused", self.inputs[address]["availability"], address)
            self.assertEqual("unused", self.inputs[address]["spatial"]["reason"], address)
        for address, name in ROM_LAMPS.items():
            self.assertIn(f"under '{name}'", self.lamps[address]["physical"]["notes"], address)
        for address, name in ROM_COILS.items():
            self.assertIn(f"names public {address} '{name}'", self.solenoids[address]["physical"]["notes"], address)

    def test_polarity_follows_construction(self) -> None:
        for address, item in self.inputs.items():
            if 1 <= address <= 64 and address not in UNUSED_SWITCHES:
                self.assertIs(False, item["normally_closed"], address)
            if address in UNUSED_SWITCHES:
                self.assertNotIn("normally_closed", item, address)
        self.assertIs(False, self.inputs[-7]["normally_closed"])
        self.assertNotIn("normally_closed", self.inputs[-6])
        self.assertIs(False, self.inputs[82]["normally_closed"])
        self.assertIs(False, self.inputs[84]["normally_closed"])
        self.assertIn("polarity", self.definition["coverage"]["missing"])

    def test_flipper_column_and_the_matrix_copies(self) -> None:
        self.assertEqual("switch.left-flipper-copy", self.inputs[63]["id"])
        self.assertEqual("switch.right-flipper-copy", self.inputs[64]["id"])
        self.assertEqual(["flipper.lower.left.button"], self.inputs[84]["roles"])
        self.assertEqual(["flipper.lower.right.button"], self.inputs[82]["roles"])
        for address in (81, 83, 85, 86, 87, 88):
            self.assertEqual("unused", self.inputs[address]["availability"], address)
            self.assertIn("shows NONE", self.inputs[address]["physical"]["notes"], address)
        self.assertIn("A consumer drives 84, not 63", self.inputs[63]["physical"]["notes"])
        self.assertIn("A consumer drives 82, not 64", self.inputs[64]["physical"]["notes"])
        for address in range(45, 49):
            self.assertEqual("virtual", self.solenoids[address]["kind"], address)
            self.assertEqual("used", self.solenoids[address]["availability"], address)
        self.assertNotIn("part_number", self.inputs[64]["physical"])
        self.assertEqual("180-5048-01", self.inputs[63]["physical"]["part_number"])

    def test_lamps_cover_the_whole_matrix(self) -> None:
        self.assertEqual(["cabinet.start-button-lamp"], self.lamps[64]["roles"])
        for address, item in self.lamps.items():
            self.assertEqual("lamp", item["kind"], address)
            self.assertIn(f"turns on public lamp address {address} alone", item["physical"]["notes"], address)
            self.assertIn("it cannot show how many bulbs the address drives", item["physical"]["notes"], address)
        self.assertEqual({31: 2, 40: 2, 43: 2}, {a: item["physical"]["quantity"] for a, item in self.lamps.items() if "quantity" in item["physical"]})
        self.assertEqual("lamp.bottom-turbo-bumper", self.lamps[7]["id"])
        self.assertEqual(
            {31: "conflicted", 32: "conflicted"},
            {a: item["provenance"]["status"] for a, item in self.lamps.items() if item["provenance"]["status"] != "validated"},
        )
        self.assertEqual(("lamp.captive-balls-x2", "lamp.ticket"), (self.lamps[31]["id"], self.lamps[32]["id"]))

    def test_solenoid_address_model(self) -> None:
        kinds = {address: item["kind"] for address, item in self.solenoids.items()}
        self.assertEqual("flasher", kinds[9])
        self.assertEqual("relay", kinds[10])
        self.assertEqual("gi", kinds[11])
        # RY1's contacts feed every G.I. line (power-supply sheet, printed page 59), so the relay is not playfield-only.
        self.assertEqual(["playfield.general-illumination", "backbox.general-illumination", "cabinet.general-illumination"], self.solenoids[11]["roles"])
        self.assertEqual(("motor", "motor"), (kinds[14], kinds[16]))
        self.assertEqual("control_signal", kinds[23])
        self.assertEqual({"flasher"}, {kinds[address] for address in range(25, 33)})
        self.assertEqual({"magnet"}, {kinds[address] for address in range(37, 40)})
        self.assertEqual({"coil"}, {kinds[address] for address in (*range(1, 9), 12, 13, 15, *range(17, 23))})
        for address in (24, 33, 34, 35, 36, 49, 50):
            self.assertEqual("unused", self.solenoids[address]["availability"], address)
        for address in range(40, 45):
            self.assertEqual(("unknown", "candidate"), (self.solenoids[address]["availability"], self.solenoids[address]["provenance"]["status"]), address)
        self.assertEqual({8: 3, 1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, {n - 24: self.solenoids[n]["physical"]["quantity"] for n in range(25, 33)})
        # Three is the working 8R count, not a settled one: the wiring drawings count four.
        self.assertEqual({9, 32}, {a for a, item in self.solenoids.items() if item["provenance"]["status"] == "conflicted"})
        self.assertEqual(4, self.solenoids[9]["physical"]["quantity"])
        gi = self.solenoids[11]["physical"]["notes"]
        for branch in ("F1 'Playfield'", "F2 'Backbox Door & Speaker Panel'", "F3 'Playfield & Coin Door'", "F4 'Backbox Door'"):
            self.assertIn(branch, gi)
        for fact in ("coil on CN7 pins 1 and 3", "CN8 pins 1-4", "contacts 4 and 3 are connected to nothing", "opens the common feed of every G.I. line"):
            self.assertIn(fact, gi)
        self.assertNotIn("which of those branches", gi)
        game_on = self.solenoids[23]["physical"]["notes"]
        for fact in ("off in the test's entry frame at 47.15 s", "came on at 47.33 s and stayed on", "0.40 s and 0.44 s after the run set the shooter-lane switch 16"):
            self.assertIn(fact, game_on)
        self.assertNotIn("during that test", game_on)
        self.assertIn("a missing callout is weaker evidence than those positive records", self.solenoids[29]["physical"]["notes"])
        for address in (37, 38, 39):
            magnet = self.solenoids[address]["physical"]["notes"]
            self.assertIn("these are public address transitions, not measured magnet timing", magnet, address)
            self.assertNotIn("the CPU's data line rather than", magnet, address)
        for address in range(1, 9):
            notes = self.solenoids[address]["physical"]["notes"]
            self.assertIn(f"draws this drive's left-set output from input J1-{address}", notes, address)
            self.assertEqual(address in (3, 5), f"names that input J1-{address}" in notes, address)
        self.assertEqual((12, "dc"), (self.solenoids[14]["wiring"]["nominal_voltage_v"], self.solenoids[14]["wiring"]["voltage_type"]))
        self.assertEqual(50, self.solenoids[22]["wiring"]["nominal_voltage_v"])
        self.assertEqual(("BLU-BLK", "PPB J8-12"), (self.solenoids[22]["wiring"]["control_wire"], self.solenoids[22]["wiring"]["control_connection"]))
        # The wiring sheet runs 3, 5, 6 and 8 through the J8 boosters on the 50 V bus, and 1, 2, 4 and 7 on 32 V.
        boosted = {3: "PPB J8-2", 5: "PPB J8-4", 6: "PPB J8-7", 8: "PPB J8-10"}
        for address in range(1, 9):
            wiring = self.solenoids[address]["wiring"]
            if address in boosted:
                self.assertEqual((50, "dc", boosted[address], "YEL-VIO", "PPB J7-8,9"), (
                    wiring["nominal_voltage_v"], wiring["voltage_type"], wiring["control_connection"], wiring["power_wire"], wiring["power_connection"],
                ), address)
            else:
                self.assertEqual((32, "dc", "PPB J6-3"), (wiring["nominal_voltage_v"], wiring["voltage_type"], wiring["power_connection"]), address)
        self.assertEqual("VIO-GRY", self.solenoids[8]["wiring"]["control_wire"])
        self.assertNotIn("nominal_voltage_v", self.solenoids[16].get("wiring", {}))
        for address, pin in zip(range(40, 45), (5, 4, 3, 2, 1)):
            item = self.solenoids[address]
            self.assertEqual(("control_signal", f"control.cn3-pin-{pin}"), (item["kind"], item["id"]), address)
            self.assertNotIn("spatial", item, address)
            self.assertIn(f"on CN3 pin {pin}", item["physical"]["notes"], address)

    def test_the_pinmame_sources_carry_their_own_licences(self) -> None:
        licences = {s["uri"].rsplit("/", 1)[1]: (s["license"], s.get("rights", "")) for s in self.definition["sources"] if s["kind"] == "pinmame_core"}
        self.assertEqual({"degames.c", "s11.c", "s11.h", "core.c", "core.h"}, set(licences))
        for name in ("degames.c", "s11.c", "s11.h"):
            self.assertEqual(("BSD-3-Clause", ""), licences[name], name)
        for name in ("core.c", "core.h"):
            self.assertEqual("NOASSERTION", licences[name][0], name)
            self.assertIn("old MAME", licences[name][1], name)

    def test_the_magnets_follow_the_board_numbering(self) -> None:
        for address, (identifier, connection, mosfet) in MAGNETS.items():
            item = self.solenoids[address]
            self.assertEqual(identifier, item["id"], address)
            self.assertEqual((connection, mosfet, "Magnet Control Board"),
                             (item["wiring"]["control_connection"], item["wiring"]["driver_transistor"], item["wiring"]["board"]), address)
            self.assertNotIn("power_connection", item["wiring"], address)
        facts = load_json(RUNTIME_PATH)
        self.assertEqual([38, 37, 39] * 5 + [38, 37], facts["magnet_test_on_sequence"])

    def test_right_hand_flash_lamps_pair_with_the_relay(self) -> None:
        gated = sorted(item["destination"] for item in self.definition["relationships"] if item["kind"] == "relay_gated" and item["source"] == "relay.left-right-relay")
        self.assertEqual([f"flasher.{n}r" for n in range(1, 9)], gated)

    def test_the_conflicts_are_the_captive_ball_lamp_and_the_8r_count(self) -> None:
        conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
        self.assertEqual(["conflict.flash-drive-9-supply", "conflict.flash-lamps-8r-quantity", "conflict.right-captive-ball-lamp"], sorted(conflicts))
        drive_9 = conflicts["conflict.flash-drive-9-supply"]
        self.assertEqual(("outputs.flasher.crane-and-insert", "unresolved"), (drive_9["path"], drive_9["status"]))
        self.assertIn("Resolution path: with the power off, check whether the common wire", drive_9["description"])
        self.assertNotIn("power_connection", self.solenoids[9]["wiring"])
        lamp, flash = conflicts["conflict.right-captive-ball-lamp"], conflicts["conflict.flash-lamps-8r-quantity"]
        self.assertEqual(("outputs.lamp.captive-balls-x2", "unresolved"), (lamp["path"], lamp["status"]))
        self.assertIn("Resolution path: run the single-lamp test on lamp 32 of a production machine", lamp["description"])
        self.assertEqual(("outputs.flasher.8r", "unresolved"), (flash["path"], flash["status"]))
        self.assertIn("Resolution path: on a production machine, select 8R in the Select Coil test", flash["description"])
        self.assertIn("The record keeps three as the working quantity", flash["description"])
        for address in (32, 40, 48, 56, 57, 60, 61, 62):
            self.assertNotIn("part_number", self.inputs[address]["physical"], address)
            self.assertIn("nothing retained settles which is right", self.inputs[address]["physical"]["notes"], address)
        self.assertIn("Both wiring drawings count four", self.solenoids[32]["physical"]["notes"])
        self.assertIn("the disagreement is a wiring detail, so no conflict is recorded", self.solenoids[8]["physical"]["notes"])
        for address in (28, 29):
            self.assertNotIn("part_number", self.solenoids[address]["physical"], address)
            self.assertIn("three No. 906 and one No. 89", self.solenoids[address]["physical"]["notes"], address)

    def test_the_captive_ball_run_never_changes_lamp_32(self) -> None:
        facts = load_json(RUNTIME_PATH)["captive_lamps"]
        self.assertEqual([41, 42, 40, 56, 39, 55], [step["switch"] for step in facts])
        for step in facts:
            self.assertEqual(0, step["lamp_32_changes"], step["label"])
            self.assertGreater(step["lamp_31_changes"], 0, step["label"])
            self.assertIn(31, step["lamps_changed"], step["label"])
            self.assertNotIn(32, step["lamps_changed"], step["label"])

    def test_mechanisms_name_their_devices(self) -> None:
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        crane = mechanisms["mechanism.crane"]
        self.assertEqual((["motor.crane", "coil.crane-lock"], ["switch.crane-left-limit", "switch.crane-right-limit"]), (crane["actuators"], crane["sensors"]))
        self.assertEqual("candidate", crane["provenance"]["status"])
        self.assertEqual("candidate", mechanisms["mechanism.ball-lock"]["provenance"]["status"])
        self.assertEqual(["switch.middle-scoop-left", "switch.middle-scoop-right"], mechanisms["mechanism.middle-scoop"]["sensors"])
        self.assertEqual(["mechanism.drop-targets.c", "mechanism.drop-targets.r", "mechanism.drop-targets.a", "mechanism.drop-targets.n", "mechanism.drop-targets.e"],
                         [p["id"] for p in mechanisms["mechanism.drop-targets"]["positions"]])
        # Printed page 4: hitting the DANGER bar (switch 54) behind the targets resets the bank.
        self.assertEqual("switch.drop-target-bar", mechanisms["mechanism.drop-targets"]["sensors"][-1])
        self.assertIn("'hitting the DANGER bar behind the drop targets will reset the drop target bank'", mechanisms["mechanism.drop-targets"]["behavior"])
        self.assertIn("DANGER bar", self.inputs[54]["physical"]["notes"])
        self.assertIn("at the front of the cabinet's right side", self.inputs[8]["physical"]["notes"])

    def test_compatibility_aliases_survive_the_migration(self) -> None:
        for address in (46, 48):
            values = {(alias["namespace"], alias["value"]) for alias in self.solenoids[address]["aliases"]}
            self.assertTrue({("pinmame.coil", str(address)), ("pinmame.solenoid", str(address))} <= values, address)
        legacy = next(source for source in self.definition["sources"] if source["id"] == "legacy.game.lah")
        self.assertEqual(sha256_file(ROOT / "games/lah.json"), legacy["sha256"])
        self.assertEqual("MIT", legacy["license"])
        self.assertIn("carries no licence file", legacy["rights"])

    def test_coverage_gate(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["input_semantics", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"], coverage["missing"])
        self.assertEqual("complete", self.definition["knowledge"]["status"])
        self.assertFalse(AUTHOR_READY_PATH.exists())
        entry = next(machine for machine in load_json(ROOT / "catalog/pinmame.json")["machines"] if machine["id"] == KEY)
        self.assertEqual(63, entry["completion_score"])

    def test_the_curator_check_passes_and_refuses_drift(self) -> None:
        import curate_last_action_hero as curator

        curator.check(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_MARKDOWN_PATH, KNOWLEDGE_PATH):
                target = root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
            curator.check(root)
            knowledge = root / KNOWLEDGE_PATH.relative_to(ROOT)
            knowledge.write_bytes(knowledge.read_bytes().replace(b"column-major", b"row-major", 1))
            with self.assertRaises(RuntimeError):
                curator.check(root)
            shutil.copyfile(KNOWLEDGE_PATH, knowledge)
            stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_bytes(DEFINITION_PATH.read_bytes())
            with self.assertRaises(RuntimeError):
                curator.check(root)
            with self.assertRaises(RuntimeError):
                curator.generate(root)

    def test_seed_is_byte_identical_to_the_definition(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

    def test_other_machines_are_not_named_in_the_artifacts(self) -> None:
        catalog = load_json(ROOT / "catalog/pinmame.json")
        paths = [DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_MARKDOWN_PATH, EVIDENCE_PATH, *sorted(EXCERPTS.iterdir())]
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for machine in catalog["machines"]:
            if machine["id"] != KEY:
                self.assertNotIn(machine["id"], text)
        for forbidden in ("Rocky", "rab_", "Tommy", "tftc", "Tales from the Crypt", "gnr_", "Guns N", "Jurassic", "Lethal Weapon", "Simpsons", "Batman"):
            self.assertNotIn(forbidden, text, forbidden)

    def test_knowledge_note_states_the_platform_facts(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in (
            "lah_112", "lah_113", "no GI channel", "Left/Right relay", "S11_PRINTERLINE", "never 63 or 64", "column-major", "Magnet Control Board",
            "145 degrees", "What would complete the record", "Visual Light Mapper", "Three conflicts are open", "CLOSE ??????", "CN3 pins 5, 4, 3, 2 and 1",
        ):
            self.assertIn(phrase, text, phrase)
        self.assertNotIn("{", re.sub(r"`[^`]*`", "", text))
        self.assertIn(f"{len(self.definition['drivers'])} PinMAME drivers", text)


class ExcerptTests(unittest.TestCase):
    def test_parsed_tables_match_the_independent_fixtures(self) -> None:
        import lah_manual

        switches = lah_manual.switch_data()["chart"]
        for address, printed in MANUAL_SWITCHES.items():
            self.assertEqual(printed, switches[address]["printed"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("Not Used", switches[address]["printed"], address)
        lamps = lah_manual.lamp_data()["chart"]
        for address, printed in MANUAL_LAMPS.items():
            self.assertEqual(printed, lamps[address]["printed"], address)
        coils = lah_manual.coil_data()
        self.assertEqual("Q46", coils["muxed"][1]["Transistor"])
        self.assertEqual("Knocker", coils["muxed"][8]["Left coil"])
        self.assertEqual("Q30", coils["direct"][9]["Transistor"])
        self.assertEqual("Q13", coils["auxiliary"][22]["Drive transistor"])
        self.assertEqual("(1) PLFD - UPPER RIGHT (2) INSERT (1) BACK PANEL (4) 89", coils["muxed"][4]["Right set"])
        magnets = lah_manual.schematic_data()["magnet_pins"]
        self.assertEqual(("INPUT 2", "CPU CN3-9"), (magnets["J1-6"]["Signal"], magnets["J1-6"]["Other end"]))
        self.assertEqual(("OUTPUT 1", "MAGNET 1"), (magnets["J2-3"]["Signal"], magnets["J2-3"]["Other end"]))

    def test_the_parser_rejects_a_ragged_table(self) -> None:
        import lah_manual

        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.md"
            path.write_bytes(b"## Table\n\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n")
            with self.assertRaises(ValueError):
                lah_manual.read_tables(path)

    def test_every_recorded_excerpt_digest_matches_its_file(self) -> None:
        definition = load_json(DEFINITION_PATH)
        recorded = [excerpt for source in definition["sources"] for excerpt in source.get("excerpts", [])]
        self.assertEqual(sorted(path.name for path in EXCERPTS.iterdir()), sorted(Path(item["path"]).name for item in recorded))
        for excerpt in recorded:
            self.assertEqual(sha256_file(ROOT / excerpt["path"]), excerpt["sha256"], excerpt["id"])
            self.assertTrue(excerpt["reviewed"], excerpt["id"])
            self.assertEqual("manual", excerpt["method"], excerpt["id"])
            self.assertTrue(excerpt["transcribed_by"].startswith("curator"), excerpt["id"])
            self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])

    def test_the_rom_wires_agree_with_the_manual_charts(self) -> None:
        import build_lah_runtime_evidence as builder
        import lah_manual

        facts = load_json(RUNTIME_PATH)
        for group, chart in (("rom_switch_names", lah_manual.switch_data()["chart"]), ("rom_lamp_names", lah_manual.lamp_data()["chart"])):
            self.assertEqual({str(n) for n in range(1, 65)}, set(facts[group]), group)
            for key, reading in facts[group].items():
                row = chart[int(key)]
                drive = re.sub(r"-\s+", "-", row["drive"]["wire"])
                self.assertEqual(f"{drive} {row['return']['wire']}", " ".join(builder.manual_spelling(w) for w in reading["wires"].split()), (group, key))


class SpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.places = load_json(PLACES_PATH)
        cls.report = load_json(SPATIAL_REPORT_PATH)
        cls.devices = cls.definition["inputs"] + cls.definition["outputs"]

    def test_every_placement_is_in_range_unique_and_observed(self) -> None:
        identifiers = []
        for device in self.devices:
            spatial = device.get("spatial")
            if not spatial or spatial["status"] == "not_applicable":
                continue
            self.assertEqual("observed", spatial["status"], device["id"])
            for placement in spatial["placements"]:
                identifiers.append(placement["id"])
                self.assertTrue(0.0 <= placement["x"] <= 1.0 and 0.0 <= placement["y"] <= 1.0, placement["id"])
                self.assertEqual("observed", placement["provenance"]["status"], placement["id"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(len(identifiers), self.report["placement_count"])

    def test_normalization_matches_the_raw_coordinates(self) -> None:
        self.assertEqual({"width": 952.0, "height": 2162.0}, self.places["table_bounds"])
        for key, hits in self.places["placements"].items():
            for hit in hits:
                self.assertEqual(round(hit["raw"]["x"] / 952.0, 6), hit["x"], key)
                self.assertEqual(round(hit["raw"]["y"] / 2162.0, 6), hit["y"], key)

    def test_the_definition_carries_exactly_the_resolved_placements(self) -> None:
        resolved = {key: sorted((hit["x"], hit["y"]) for hit in hits) for key, hits in self.places["placements"].items()}
        placed = {}
        for device in self.devices:
            spatial = device.get("spatial")
            if spatial and spatial["status"] != "not_applicable":
                placed[device_key(device)] = sorted((p["x"], p["y"]) for p in spatial["placements"])
        self.assertEqual(resolved, placed)

    def test_the_unplaced_set_is_exact(self) -> None:
        without = {tuple(device_key(device).split(".")) for device in self.definition["outputs"] if "spatial" not in device}
        self.assertEqual({(group, str(n)) for group, n in UNPLACED_OUTPUTS}, without)
        self.assertEqual(
            {f"{group}.{n}" for group, n in UNPLACED_OUTPUTS} | {f"switch.{n}" for n in UNPLACED_INPUTS}, {entry["key"] for entry in self.report["unresolved"]}
        )
        self.assertLessEqual({entry["key"] for entry in self.report["unresolved"]}, {entry["key"] for entry in self.places["unplaced"]})
        for device in self.definition["inputs"]:
            self.assertEqual(device["binding"]["device"] not in UNPLACED_INPUTS, "spatial" in device, device["id"])
        outputs = {tuple(device_key(d).split(".")): d for d in self.definition["outputs"]}
        for group, n in CABINET_OUTPUTS:
            self.assertEqual("cabinet_or_service", outputs[(group, str(n))]["spatial"]["reason"], (group, n))

    def test_no_lamp_flash_lamp_or_gi_is_placed(self) -> None:
        self.assertFalse(FLASH_KEYS & set(self.places["placements"]))
        self.assertEqual([], [key for key in self.places["placements"] if key.startswith("lamp.")])
        rejected = {(entry["key"], entry["object"].lower()) for entry in self.places["rejected"]}
        for n in BOUND_LAMPS:
            self.assertIn((f"lamp.{n}", f"l{n}"), rejected, n)
        for key, hits in self.places["placements"].items():
            for hit in hits:
                self.assertNotEqual("Light", hit["object_type"], key)
                if hit["object_type"] == "Primitive":
                    self.assertIn(hit["coordinate_origin"], ("mesh-bounds-center", "primitive-pivot"), key)
                    self.assertNotIn("_LM_", hit["object"], key)

    def test_the_projections_are_declared(self) -> None:
        self.assertEqual(PROJECTIONS, {(p["group"], p["address"]) for p in self.report["projections"]})
        self.assertFalse({"switch.60", "switch.61"} & set(self.places["placements"]))
        for key in ("solenoid.14",):
            self.assertEqual(("MCrane_BM_Room", "primitive-pivot"), (self.places["placements"][key][0]["object"], self.places["placements"][key][0]["coordinate_origin"]), key)
        self.assertEqual("sw19", self.places["placements"]["solenoid.13"][0]["object"])

    def test_the_builder_refuses_what_is_never_a_socket(self) -> None:
        import build_lah_places as builder

        class FakeTable:
            def __init__(self, value: dict) -> None:
                self.value = value

            def get(self, name: str, typ: str) -> dict:
                return self.value

            def find_lines(self, pattern: str) -> list[int]:
                return [1]

        light = {"name": "l57", "center": {"x": 166.0, "y": 1000.0}, "is_bulb_light": True, "show_bulb_mesh": True}
        placed = builder.resolve(FakeTable(light), "lamp.57", builder.Choice("l57", "Light", "fixture", [r"x"]))
        self.assertEqual((0.17437, 0.462535), (placed["x"], placed["y"]))
        for key, value, choice in (
            ("lamp.57", {**light, "is_bulb_light": False}, builder.Choice("l57", "Light", "fixture", [r"x"])),
            ("lamp.57", {**light, "show_bulb_mesh": False}, builder.Choice("l57", "Light", "fixture", [r"x"])),
            ("solenoid.26", light, builder.Choice("f2", "Light", "fixture", [r"x"])),
            ("solenoid.26", {"name": "f2"}, builder.Choice("f2", "Flasher", "fixture", [r"x"])),
            ("solenoid.12", {"name": "diverter_LM_Flashes_f2", "is_visible": True}, builder.Choice("diverter_LM_Flashes_f2", "Primitive", "fixture", [r"x"], mode="mesh")),
            ("solenoid.12", {"name": "diverter_BM_Room", "is_visible": True}, builder.Choice("diverter_BM_Room", "Primitive", "fixture", [r"x"])),
            ("lamp.57", {"name": "PinCab_Smart", "is_visible": True}, builder.Choice("PinCab_Smart", "Primitive", "fixture", [r"x"], mode="mesh")),
        ):
            with self.assertRaises(builder.BuildError, msg=(key, choice.obj)):
                builder.resolve(FakeTable(value), key, choice)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_placements_equal_the_extraction(self) -> None:
        command = [
            sys.executable, "-B", str(ROOT / "tools/build_lah_places.py"), "--extracted", str(Path(VPX_ROOT) / EXTRACTION_RELATIVE),
            "--output", str(PLACES_PATH), "--check", "--world-obj", str(Path(VPX_ROOT) / WORLD_OBJ_RELATIVE),
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": TOOL_PATH})
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_placement_check_refuses_altered_line_ends(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            altered = Path(scratch) / PLACES_PATH.name
            altered.write_bytes(PLACES_PATH.read_bytes().replace(b"\n", b"\r\n"))
            command = [
                sys.executable, "-B", str(ROOT / "tools/build_lah_places.py"), "--extracted", str(Path(VPX_ROOT) / EXTRACTION_RELATIVE),
                "--output", str(altered), "--check",
            ]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": TOOL_PATH})
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_every_placed_object_exists_and_the_lamp_lights_draw_no_bulb(self) -> None:
        items = gameitems(Path(VPX_ROOT) / EXTRACTION_RELATIVE)
        for key, hits in self.places["placements"].items():
            for hit in hits:
                kind, value = items[hit["object"].lower()]
                self.assertEqual(hit["object_type"], kind, hit["object"])
                self.assertNotEqual("Light", kind, key)
        for n in BOUND_LAMPS:
            kind, value = items[f"l{n}"]
            self.assertEqual(("Light", True, False), (kind, value["is_bulb_light"], value["show_bulb_mesh"]), n)
        for name in ("f2", "f3", "f4", "f5", "f6"):
            kind, value = items[name]
            self.assertEqual(("Light", True, False), (kind, value["is_bulb_light"], value["show_bulb_mesh"]), name)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_extraction_manifest_is_recomputable(self) -> None:
        import curate_last_action_hero as curator

        curator.verify_extraction_manifest(Path(VPX_ROOT))

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_extraction_gate_refuses_changed_manifest_bytes_and_a_missing_table(self) -> None:
        import curate_last_action_hero as curator

        retained = (Path(VPX_ROOT) / curator.EXTRACTION_MANIFEST_RELATIVE_PATH).read_bytes()
        with tempfile.TemporaryDirectory() as scratch:
            manifest = Path(scratch) / curator.EXTRACTION_MANIFEST_RELATIVE_PATH
            manifest.parent.mkdir(parents=True)
            manifest.write_bytes(retained.replace(b"\n", b"\r\n"))
            with self.assertRaisesRegex(RuntimeError, "bytes are not the cited ones"):
                curator.verify_extraction_manifest(Path(scratch))
            manifest.write_bytes(retained)
            with self.assertRaisesRegex(RuntimeError, "table is missing or not the cited one"):
                curator.verify_extraction_manifest(Path(scratch))

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_mesh_bounds_rederive_from_the_world_export(self) -> None:
        import build_lah_places as builder

        builder.check_mesh_bounds(Path(VPX_ROOT) / WORLD_OBJ_RELATIVE)
        with tempfile.TemporaryDirectory() as scratch:
            other = Path(scratch) / "other.obj"
            other.write_bytes(b"o diverter_BM_Room\nv 0 0 0\n")
            with self.assertRaises(builder.BuildError):
                builder.check_mesh_bounds(other)


class RuntimeEvidenceTests(unittest.TestCase):
    def test_the_definition_records_the_evidence_digest(self) -> None:
        definition = load_json(DEFINITION_PATH)
        (source,) = [s for s in definition["sources"] if s["id"] == "runtime.last-action-hero.lah-112-service-tests"]
        self.assertEqual(sha256_file(EVIDENCE_PATH), source["sha256"])

    def test_cycling_coils_order_is_the_public_address_order(self) -> None:
        runs = load_json(EVIDENCE_PATH)["runtime"]["observations"]["runs"]
        expected = [address for drive in range(1, 9) for address in (drive, 10, drive + 24)] + [9, *range(11, 23)]
        self.assertEqual(expected, runs["cycling-coils"]["ordered_solenoid_on_sequence"])

    def test_the_cited_counts_are_in_the_bundle(self) -> None:
        runs = load_json(EVIDENCE_PATH)["runtime"]["observations"]["runs"]
        self.assertIn("Magnet Test: hold Start 2.5 s: 37 x6, 38 x6, 39 x5", runs["crane-magnet-laser"]["note"])
        self.assertIn("Trough: press Start with 15 empty: 1 x3, 14 x1, 16 x7", runs["trough-serve"]["note"])
        self.assertIn("on at 5.81 s, off at 17.00 s, on at 17.07 s, off at 36.38 s", runs["trough-serve"]["note"])
        self.assertEqual([7, 14, 16], runs["trough-serve"]["ordered_solenoid_on_sequence"][:3])

    def test_the_game_on_boundaries_are_pinned(self) -> None:
        runs = load_json(EVIDENCE_PATH)["runtime"]["observations"]["runs"]
        self.assertIn(
            "Output 23 (game on) by host time: on at 10.98 s, off at 29.02 s, on at 42.80 s, off at 44.73 s, on at 45.04 s, off at 47.03 s, on at 47.33 s; "
            "the Active Switch Test entry frame, the baseline NONE frame, is at 47.15 s",
            runs["active-switches"]["note"],
        )
        for name, lane, on in (("trough-serve", "28.73", "29.13"), ("captive-lamps", "28.74", "29.18")):
            self.assertIn(f"Output 23 (game on) came on once, at {on} s, after the run set the shooter-lane switch 16 at {lane} s, and stayed on.", runs[name]["note"], name)
        facts = load_json(RUNTIME_PATH)["game_on_23"]
        self.assertEqual((47.15, 47.33), (facts["active-switches"]["test_entry_s"], facts["active-switches"]["levels"][-1]["time_s"]))

    def test_every_scenario_is_committed_and_valid(self) -> None:
        import lah_harness

        evidence = load_json(EVIDENCE_PATH)
        runs = evidence["runtime"]["raw_runs"]
        self.assertEqual(7, len(runs))
        for run in runs:
            path = ROOT / run["scenario_path"]
            self.assertNotIn(b"\r\n", path.read_bytes(), run["name"])
            self.assertEqual(run["scenario_sha256"], sha256_file(path), run["name"])
            scenario = load_json(path)
            self.assertEqual("lah_112", scenario["game"])
            self.assertEqual(run["action_count"], len(scenario["actions"]))
            self.assertFalse([a for a in scenario["actions"] if a["type"] in ("pulse_key", "set_key")], "named keys would enable keyboard handling")
            lah_harness.check_targets(scenario)

    def test_the_harness_refuses_ambiguous_title_targets(self) -> None:
        import lah_harness

        lah_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["ACTIVE SWITCH TEST"]}]})
        with self.assertRaises(ValueError):
            lah_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["SWITCH TEST"]}]})
        with self.assertRaises(ValueError):
            lah_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["NOT A TITLE"]}]})

    def test_every_cited_frame_is_pinned_by_its_reading(self) -> None:
        import lah_readings

        evidence = load_json(EVIDENCE_PATH)
        snapshots = {item["label"]: item["pixel_sha256"] for item in evidence["runtime"]["observations"]["diagnostic_snapshots"]}
        self.assertEqual(lah_readings.READ_FRAME_DIGESTS, snapshots)
        for digest in snapshots.values():
            self.assertRegex(digest, r"^[0-9a-f]{64}$")

    @unittest.skipUnless(REVIEW_ROOT, "PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
    def test_the_evidence_rebuilds_from_the_retained_runs(self) -> None:
        session = Path(REVIEW_ROOT) / SESSION_RELATIVE
        manifest_files = [session / "manifest.json", session / "manifest.sha256"]
        before = [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files]
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/build_lah_runtime_evidence.py"), "--check"],
            capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": TOOL_PATH},
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        # --check verifies the pinned external manifest and must never rewrite it.
        self.assertEqual(before, [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files])


class RetainedSourceTests(unittest.TestCase):
    @unittest.skipUnless(MANUALS_ROOT, "PINMAME_MANUALS_ROOT is not set")
    def test_the_retained_manuals_are_the_cited_scans(self) -> None:
        manuals = {s["original_filename"]: s["sha256"] for s in load_json(DEFINITION_PATH)["sources"] if s["kind"] == "manual"}
        for relative, digest in MANUALS.items():
            self.assertEqual(digest, sha256_file(Path(MANUALS_ROOT) / relative), relative)
            self.assertEqual(digest, manuals[Path(relative).name], relative)

    @unittest.skipUnless(ROM_ROOT, "PINMAME_ROM_LIBRARY_ROOT is not set")
    def test_the_rom_archive_is_the_one_the_runs_used(self) -> None:
        self.assertEqual(ROM_SHA256, sha256_file(Path(ROM_ROOT) / "lah_112.zip"))
        self.assertEqual(ROM_SHA256, load_json(EVIDENCE_PATH)["runtime"]["rom_archive_sha256"])


if __name__ == "__main__":
    unittest.main()
