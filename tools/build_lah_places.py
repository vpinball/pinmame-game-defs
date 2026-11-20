#!/usr/bin/env python3
"""Resolve normalized playfield coordinates for Last Action Hero (Data East 1993).

Reads the retained VPW 1.1 extraction (``gamedata.json`` bounds, ``gameitems/*.json``, ``collections.json``
and ``script.vbs``) and writes ``tools/last_action_hero_places.json`` in the ``pinmame-vpx-placement-resolution``
format used by the other Data East records. Every table object is chosen by what ``script.vbs`` binds to the ROM
switch, lamp or coil, or, where the script binds no object to a coil (the bumpers, the slingshots), by the manual's
and the ROM's own Left / Center / Right naming. The choice, the reason and the script patterns that prove the
binding are hard-coded here, and the builder fails closed when a named object is missing, ambiguous, outside the
table, of the wrong type or hidden, or when a binding pattern no longer matches the script.

The table is a Visual Light Mapper (VLM) build. Every lamp is driven through ``Lampz.MassAssign(n) = <Light>`` and
``Lampz.Callback(n) = "UpdateLightMap <baked lightmap primitive>, ..."``; the ``Light`` objects are bulb-mode
light-map sources hidden at start-up (none draws a bulb mesh), and the ``*_LM_*`` primitives are baked lightmaps.
A light that sits on no bulb makes no socket (docs/SPATIAL.md, "Picking the bulb"), and the table models no
insert bulb, so no matrix lamp is placed: each bound Light is listed as rejected and each lamp as unplaced. A
raised socket (a flasher dome, a crane cab lamp, a back-panel lamp) is never placed on a playfield-height
light-map source either; no bulb or dome is modelled for any of them, so every flash lamp stays unplaced
(docs/SPATIAL.md, "Light-map sources are not raised sockets"). Lightmap primitives, cabinet and topper primitives,
VR backglass sprites and Lights the script never binds are listed as rejected, each verified against the script and
the table.

Coordinate convention: x = 0 is the left side and x = 1 the right side, y = 0 is the rear/backglass end and
y = 1 the front/apron end. ``x = raw_x / 952`` and ``y = raw_y / 2162``, rounded to six decimals.

Origins:

``measured-center``
    the object's stored centre (Kicker, Bumper, Spinner, or a Light that draws its own bulb) or position (HitTarget).
``computed-centroid``
    the mean of the drag points of a Wall (the slingshots, the drop targets) or of a Trigger. A Trigger's stored
    ``center`` is only an editor pivot: it differs from the centroid of its drag points by up to 34 units, and the
    drag points are the shape the ball crosses, so the centroid is used for every Trigger.
``mesh-bounds-center``
    the centre of the x/y bounding box of a primitive's world-space mesh. The meshes are exported with
    ``vpxtool export obj --units vpu``; the bounds are embedded in ``MESH_BOUNDS`` below so the builder needs no
    external file. ``--world-obj`` re-derives them from the retained export and fails on a mismatch.
``primitive-pivot``
    the stored position of the crane primitive, which is the axis the three crane meshes rotate about. It is not
    a free primitive position: the builder proves it three ways (the three crane primitives share it, it lies
    inside each of their world-space bounds, and the script's own ball-on-the-boom formula, which circles it with a
    radius of 69.2, puts the right-limit ball on the KickerBolaIn kicker within 6 units).

Usage::

    python tools/build_lah_places.py --extracted <extracted dir> --output tools/last_action_hero_places.json
    python tools/build_lah_places.py --extracted <extracted dir> --output tools/last_action_hero_places.json --check
    python tools/build_lah_places.py --extracted <extracted dir> --output tools/last_action_hero_places.json --check --world-obj <export .obj>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

WIDTH = 952.0
HEIGHT = 2162.0

SCRIPT_SHA256 = "1038027da4bdabe7a447d96df6eb79bb3830b2af18a17330d709feb4eaa139e5"
VPX_SHA256 = "0a1e3fcfc652086003106fb22290ec54166dd5121f8d405f4a3cd2389d59b173"

WORLD_OBJ_NAME = "Last Action Hero (Data East 1993) VPW v1.1.obj"
WORLD_OBJ_SHA256 = "3213fbabb085338dd19d06179a899baedd82be4c35228f7a6cf46cd938ffa6b7"
WORLD_OBJ_RELATIVE = "data-east/last-action-hero-1993/vpw-1.1/world-obj/" + WORLD_OBJ_NAME

SOURCE = (
    "VPW 1.1 extraction (gamedata.json bounds, gameitems, collections, script.vbs sha256 " + SCRIPT_SHA256
    + ") of the retained VPX (sha256 " + VPX_SHA256 + "), objects chosen from script.vbs bindings and reconciled with the manual's "
    "switch, lamp and coil tables; primitive mesh bounds from the vpxtool git:v0.33.3 'export obj --units vpu' world-space "
    "export (sha256 " + WORLD_OBJ_SHA256 + ")"
)

ORIGIN = {
    "center": "measured-center",
    "centroid": "computed-centroid",
    "mesh": "mesh-bounds-center",
    "pivot": "primitive-pivot",
}

# x/y bounding boxes (xmin, ymin, xmax, ymax) of world-space meshes in the table's saved pose, rounded to four
# decimals. The OBJ export maps world x/y to OBJ x/y and negates the height. The diverter's stored position is its
# pivot, at one end of the flap, and blockPost's mesh is the post itself. The three crane meshes are the boom in
# three poses; they are used only to prove that the crane pivot lies inside each of them.
MESH_BOUNDS = {
    "LCrane_BM_Room": (39.9707, 126.5367, 509.3747, 816.1405),
    "MCrane_BM_Room": (231.5019, 124.7504, 616.9364, 845.7946),
    "RCrane_BM_Room": (186.0282, 138.5753, 927.1595, 412.542),
    "blockPost_BM_Room": (52.8352, 929.6947, 64.8733, 941.7329),
    "diverter_BM_Room": (352.5002, 470.0335, 467.6332, 621.9438),
}

CRANE_PRIMITIVES = ("LCrane_BM_Room", "MCrane_BM_Room", "RCrane_BM_Room")
CRANE_BALL_RADIUS = 69.2

# Lampz indices that drive solenoid-fed flash lamps, and the public solenoid each one is wired from.
FLASH_LAMPZ = {101: 25, 102: 26, 103: 27, 104: 28, 105: 29, 106: 30, 107: 31, 108: 32, 109: 9}
# The Lights the script binds with Lampz.MassAssign to a flash index (Lampz index -> Lights).
FLASH_LIGHTS = {102: ("f2",), 103: ("f3",), 104: ("f4",), 105: ("f5",), 106: ("f6",)}
# Cabinet and topper primitives the script fades with a flash or cabinet-lamp callback.
CABINET_CALLBACKS = {
    57: ("PinCab_Smart",),
    64: ("PinCab_Start",),
    101: ("PinCab_Topper_Blue", "PinCab_Top_rbulb"),
    107: ("PinCab_Topper_Red", "PinCab_Top_lbulb"),
}
# Lamps whose Light the script never binds: the single-bulb and two-bulb lamps whose only MassAssign line is a comment.
UNBOUND_LAMPS = (31, 40, 43)
COMMENTED_LIGHTS = {31: "l31b", 40: "l40b", 43: "l43b"}
CABINET_LAMPS = (64,)
BACKGLASS_FLASHERS = {26: "BGFL26_", 27: "BGFL27_", 28: "BGFL28_", 29: "BGFL29_", 32: "BGFL32_", 9: "BGFL33_"}
BACKGLASS_COUNTS = {26: 5, 27: 10, 28: 10, 29: 5, 32: 10, 9: 10}
GI_LIGHTS = tuple(f"gi{n:03d}" for n in range(1, 26))


class BuildError(RuntimeError):
    pass


class Choice:
    """One table object chosen for a key, with the reason and the script patterns proving the binding."""

    def __init__(self, obj, typ, why, bind, mode="center", extra=None):
        self.obj = obj
        self.typ = typ
        self.why = why
        self.bind = list(bind)
        self.mode = mode
        self.extra = extra  # optional callable(table, key, choice) that raises BuildError


def solcb(n, name):
    return rf'SolCallback\({n}\)\s*=\s*"{re.escape(name)}"'


def hit_trigger(n, what, obj=None, extra_bind=()):
    """A playfield Trigger whose Hit handler sets Controller.Switch(n)."""
    obj = obj or f"Sw{n}"
    return [Choice(obj, "Trigger", f"{what}: {obj}_Hit sets Controller.Switch({n}) and its UnHit clears it",
                   [rf"Sub {obj}_Hit\(\)\s*:\s*Controller\.Switch\({n}\)\s*=\s*1", *extra_bind], mode="centroid")]


# --------------------------------------------------------------------------------------------------
# Switches (public switch number -> chosen table object). 1-8, 49-53, 62-64 are cabinet or unused and are not placed.
# --------------------------------------------------------------------------------------------------

SWITCHES = {}

for _n, _what in (
    (9, "trough #1 (left, the drain end)"), (10, "trough #2"), (11, "trough #3"), (12, "trough #4"), (13, "trough #5"),
    (14, "trough #6"),
):
    SWITCHES[_n] = [Choice(f"sw{_n}", "Kicker", f"{_what}: sw{_n}_Hit sets and sw{_n}_UnHit clears Controller.Switch({_n})",
                           [rf"Sub sw{_n}_Hit\s*:\s*Controller\.Switch\({_n}\)\s*=\s*1",
                            rf"Sub sw{_n}_UnHit\s*:\s*Controller\.Switch\({_n}\)\s*=\s*0"])]
SWITCHES[15] = [Choice(
    "sw15", "Kicker",
    "trough #7 (right, the release end): the script has no Hit handler; SolTrough kicks the ball from sw14 into it and sets Controller.Switch(15), "
    "SolRelease kicks sw15 to the shooter lane and clears it",
    [r"sw14\.kick 57, 20", r"Controller\.Switch\(15\)\s*=\s*1", r"sw15\.kick 90, 10", r"Controller\.Switch\(15\)\s*=\s*0"])]
SWITCHES[16] = [Choice("sw16", "Trigger", "shooter lane: sw16_Hit sets Controller.Switch(16) and sw16_Unhit clears it",
                       [r"Sub sw16_Hit\(\)\s*:\s*Controller\.Switch\(16\)\s*=\s*1", r"Sub sw16_Unhit\s*:\s*Controller\.Switch\(16\)\s*=\s*0"],
                       mode="centroid")]
for _n in range(17, 22):
    SWITCHES[_n] = [Choice(
        f"sw{_n}", "Wall", f"drop target {_n - 16} of the five-bank (the ROM's C BOTTOM to E TOP order): Sw{_n}_Hit calls DTHit {_n} on the wall, "
        f"which DT{_n} registers as the target's primary wall",
        [rf"Sub Sw{_n}_Hit\s*:\s*DTHit {_n}\b", rf"Set DT{_n} = \(new DropTarget\)\(sw{_n}, sw{_n}a, sw{_n}_BM_Room, {_n},"], mode="centroid")]
SWITCHES[22] = [Choice("sw22", "Trigger", "left lock top: Sw22_Hit sets Controller.Switch(22) and Sw22_UnHit clears it",
                       [r"Sub Sw22_Hit\s*:\s*Controller\.Switch\(22\)\s*=\s*1", r"Controller\.Switch\(22\)\s*=\s*0"], mode="centroid")]
SWITCHES[23] = [Choice("sw23", "Trigger", "left lock bottom: Sw23_Hit sets Controller.Switch(23) and Sw23_UnHit clears it",
                       [r"Sub Sw23_Hit\b", r"Controller\.Switch\(23\)\s*=\s*1", r"Controller\.Switch\(23\)\s*=\s*0"], mode="centroid")]
SWITCHES[24] = hit_trigger(24, "single left rollover")
for _n, _what in ((28, "top rollover left"), (29, "top rollover middle"), (30, "top rollover right")):
    SWITCHES[_n] = hit_trigger(_n, _what)
for _n, _what in ((25, "right stand-up top"), (26, "right stand-up middle"), (27, "right stand-up bottom")):
    SWITCHES[_n] = [Choice(f"Sw{_n}", "HitTarget", f"{_what}: Sw{_n}_Hit calls STHit {_n}, and ST{_n} is its stand-up target",
                           [rf"Sub sw{_n}_Hit\s*:\s*STHit {_n}\b", rf"Set ST{_n} = \(new StandupTarget\)\(sw{_n}, "])]
SWITCHES[31] = [Choice("sw31", "Kicker", "right scoop assembly: sw31_Hit adds the ball to bsRScoop, which is InitSaucer sw31, 31",
                       [r"Sub sw31_Hit\s*:\s*bsRScoop\.AddBall 1", r"\.InitSaucer sw31, 31,"])]
SWITCHES[32] = [Choice("Sw32", "HitTarget", "animated cat target: Sw32_Hit calls STHit 32, and ST32 is its stand-up target",
                       [r"Sub Sw32_Hit\s*:\s*STHit 32\b", r"Set ST32 = \(new StandupTarget\)\(sw32, "])]
SWITCHES[33] = [Choice("Bumper1", "Bumper", "left turbo bumper: Bumper1_Hit pulses switch 33 (the left one of the two upper bumpers)",
                       [r"Sub Bumper1_Hit\s*\n\s*vpmTimer\.PulseSw 33\b"])]
SWITCHES[34] = [Choice("Bumper3", "Bumper", "bottom turbo bumper (the lowest of the three): Bumper3_Hit pulses switch 34",
                       [r"Sub Bumper3_Hit\s*\n\s*vpmTimer\.PulseSw 34\b"])]
SWITCHES[35] = [Choice("Bumper2", "Bumper", "right turbo bumper: Bumper2_Hit pulses switch 35 (the right one of the two upper bumpers)",
                       [r"Sub Bumper2_Hit\s*\n\s*vpmTimer\.PulseSw 35\b"])]
SWITCHES[36] = [Choice("LeftSlingshot", "Wall", "left slingshot: LeftSlingShot_Slingshot pulses switch 36",
                       [r"Sub LeftSlingShot_Slingshot\s*\n[^\n]*\n\s*vpmTimer\.PulseSw\(36\)"], mode="centroid")]
SWITCHES[37] = [Choice("RightSlingshot", "Wall", "right slingshot: RightSlingShot_Slingshot pulses switch 37",
                       [r"Sub RightSlingShot_Slingshot\s*\n[^\n]*\n\s*vpmTimer\.PulseSw\(37\)"], mode="centroid")]
SWITCHES[38] = hit_trigger(38, "right scoop rollover (the entry of the right wire ramp that ends in the right scoop)")
SWITCHES[39] = hit_trigger(39, "left captive rollover")
SWITCHES[40] = [Choice("Sw40", "HitTarget", "left captive ball target: Sw40_Hit calls STHit 40, and ST40 is its stand-up target",
                       [r"Sub Sw40_Hit\s*:\s*STHit 40\b", r"Set ST40 = \(new StandupTarget\)\(sw40, "])]
SWITCHES[41] = hit_trigger(41, "left return lane")
SWITCHES[42] = hit_trigger(42, "right return lane")
SWITCHES[43] = hit_trigger(43, "left outlane")
SWITCHES[44] = hit_trigger(44, "right outlane")
SWITCHES[45] = hit_trigger(45, "left ramp exit (the high end of the left ramp, on surface 120h)")
SWITCHES[46] = hit_trigger(46, "left ramp entrance (the low end of the left ramp, on surface 75h)")
SWITCHES[47] = [Choice("Sw47", "Kicker", "VUK in the top right corner: Sw47_hit adds the ball to bsVuk, which is InitSaucer sw47, 47",
                       [r"Sub Sw47_hit\s*:\s*bsVuk\.AddBall 1", r"\.InitSaucer sw47, 47,"])]
SWITCHES[48] = [Choice("Sw48", "Kicker", "ripper kickback: the Sw48 kicker's Hit pulses switch 48 (the Sw48a trigger beside it only updates wires)",
                       [r"Sub Sw48_Hit\s*:\s*vpmTimer\.PulseSw 48\b"])]
SWITCHES[54] = [Choice("sw54", "HitTarget", "drop target bar: Sw54_Hit pulses switch 54", [r"Sub Sw54_Hit\s*:\s*vpmTimer\.PulseSw 54\b"])]
SWITCHES[55] = hit_trigger(55, "right captive rollover")
SWITCHES[56] = [Choice("Sw56", "HitTarget", "right captive ball target: Sw56_Hit calls STHit 56, and ST56 is its stand-up target",
                       [r"Sub Sw56_Hit\s*:\s*STHit 56\b", r"Set ST56 = \(new StandupTarget\)\(sw56, "])]
SWITCHES[57] = [Choice("Sw57", "Kicker", "middle scoop left: sw57_Hit adds the ball to bsMLScoop, which is InitSaucer sw57, 57",
                       [r"Sub sw57_Hit\s*:\s*bsMLScoop\.AddBall 1", r"\.InitSaucer sw57, 57,"])]
SWITCHES[58] = [Choice("sw58", "Trigger", "middle scoop right (the centre right subway switch on surface RampSubway): Sw58_Hit pulses switch 58",
                       [r"Sub Sw58_Hit\s*:\s*vpmTimer\.PulseSw 58\b"], mode="centroid")]
SWITCHES[59] = [Choice("Sw59", "Spinner", "scoop spinner: Sw59_Spin pulses switch 59", [r"Sub Sw59_Spin\s*:\s*vpmTimer\.PulseSw 59\b"])]


def crane_choice(why, bind):
    return Choice("MCrane_BM_Room", "Primitive", why, bind, mode="pivot", extra=lambda t, k, c: check_crane(t, k, c))


# The crane limits 60 and 61 are unplaced (UNPLACED below): the script sets them from timers and binds no object to them.

# --------------------------------------------------------------------------------------------------
# Solenoids (public coil number -> chosen mechanism)
# --------------------------------------------------------------------------------------------------

SOLENOIDS = {
    1: [Choice("sw14", "Kicker", "six-ball trough lockout: SolTrough kicks the ball from the sw14 kicker into the release slot",
               [solcb(1, "SolTrough"), r"sw14\.kick 57, 20"])],
    2: [Choice("sw15", "Kicker", "ball release: SolRelease kicks the release slot sw15 to the shooter lane",
               [solcb(2, "SolRelease"), r"sw15\.kick 90, 10"])],
    3: [Choice("swPlunger", "Trigger", "ball launch: AutoLaunch fires the cvpmImpulseP plunger initialised on swPlunger",
               [solcb(3, "AutoLaunch"), r"PlungerIM\.AutoFire", r"\.InitImpulseP swPlunger"], mode="centroid")],
    5: [Choice("Sw47", "Kicker", "VUK: bsVuk.SolOut kicks the ball stack initialised on the Sw47 kicker",
               [solcb(5, "bsVuk.SolOut"), r"\.InitSaucer sw47, 47,"])],
    6: [Choice("sw31", "Kicker", "right scoop: bsRScoop.SolOut kicks the ball stack initialised on the sw31 kicker",
               [solcb(6, "bsRScoop.SolOut"), r"\.InitSaucer sw31, 31,"])],
    7: [Choice("blockPost_BM_Room", "Primitive",
               "ball lock: SolLockRelease drops the Post wall and sinks the blockPost primitive 55 units (mesh bounds centre; the Post wall's centroid lies inside the mesh)",
               [solcb(7, "SolLockRelease"), r"Post\.isdropped = true", r"For each BL in blockPost_bl : BL\.transz = -55"], mode="mesh",
               extra=lambda t, k, c: check_inside_mesh(t, k, "blockPost_BM_Room", ("Post",)))],
    12: [Choice("diverter_BM_Room", "Primitive",
                "diverter: SolDiv swaps the DivOpen and DivClose walls and the DivFlipper angle swings the diverter primitive (mesh bounds centre; both walls lie inside the mesh)",
                [solcb(12, "SolDiv"), r"For each BL in diverter_bl : BL\.ObjRotZ = a", r"DivFlipper\.RotateToEnd"], mode="mesh",
                extra=lambda t, k, c: check_inside_mesh(t, k, "diverter_BM_Room", ("DivOpen", "DivClose")))],
    13: [Choice("sw19", "Wall",
                "drop target reset: SoLDrop raises all five targets (DTRaise 17-21); the placement is the bank's middle target, the one object that stands for the bank (projection)",
                [solcb(13, "SoLDrop"), r"DTRaise 19\b", r"Sub Sw19_Hit\s*:\s*DTHit 19\b"], mode="centroid")],
    14: [crane_choice(
        "crane motor: SoLCraneMotor runs CraneTimer, which turns the crane boom; the manual's schematic book (Crane Assembly) puts the motor under the shaft "
        "that carries the boom, so the motor sits on the crane's rotation axis",
        [solcb(14, "SoLCraneMotor"), r"CraneTimer\.Enabled = Enabled"])],
    15: [Choice("Sw57", "Kicker", "middle scoop: bsMLScoop.SolOut kicks the ball stack initialised on the Sw57 kicker",
                [solcb(15, "bsMLScoop.SolOut"), r"\.InitSaucer sw57, 57,"])],
    17: [Choice("Bumper1", "Bumper", "left turbo bumper: the script leaves SolCallback(17) commented out and lets the VPX bumper kick; the left one of the two upper bumpers, "
                "which the Bumper1 switch 33 and lamp 6 also name",
                [r"^\s*'SolCallback\(17\)", r"Sub Bumper1_Hit\b"])],
    18: [Choice("Bumper3", "Bumper", "center turbo bumper (the manual's Center Turbo Bumper, the ROM's BOTTOM TURBO): the script leaves SolCallback(18) commented out; the one bumper that is neither left nor right",
                [r"^\s*'SolCallback\(18\)", r"Sub Bumper3_Hit\b"])],
    19: [Choice("Bumper2", "Bumper", "right turbo bumper: the script leaves SolCallback(19) commented out; the right one of the two upper bumpers",
                [r"^\s*'SolCallback\(19\)", r"Sub Bumper2_Hit\b"])],
    20: [Choice("LeftSlingshot", "Wall", "left slingshot: the script leaves SolCallback(20) commented out and lets the VPX slingshot kick",
                [r"^\s*'SolCallback\(20\)", r"Sub LeftSlingShot_Slingshot\b"], mode="centroid")],
    21: [Choice("RightSlingshot", "Wall", "right slingshot: the script leaves SolCallback(21) commented out and lets the VPX slingshot kick",
                [r"^\s*'SolCallback\(21\)", r"Sub RightSlingShot_Slingshot\b"], mode="centroid")],
    22: [Choice("Sw48", "Kicker", "ripper kickback: SolRipperKick kicks the Sw48 kicker",
                [solcb(22, "SolRipperKick"), r"sw48\.Kick 185,50"])],
    37: [Choice("LMagnet", "Trigger", "magnet driven by SolLeftMagnet; the script names it the left magnet (cvpmMagnet LMAG on the LMagnet trigger). The manual says only that the "
                "three magnets are in the centre of the playfield and does not locate them",
                [solcb(37, "SolLeftMagnet"), r"\.InitMagnet LMagnet, 9", r"LMAG\.MagnetOn = 1"], mode="centroid")],
    38: [Choice("CMagnet", "Trigger", "magnet driven by SolCenterMagnet; the script names it the center magnet (cvpmMagnet CMAG on the CMagnet trigger)",
                [solcb(38, "SolCenterMagnet"), r"\.InitMagnet CMagnet, 9", r"CMAG\.MagnetOn = 1"], mode="centroid")],
    39: [Choice("RMagnet", "Trigger", "magnet driven by SolRightMagnet; the script names it the right magnet (cvpmMagnet RMAG on the RMagnet trigger)",
                [solcb(39, "SolRightMagnet"), r"\.InitMagnet RMagnet, 9", r"RMAG\.MagnetOn = 1"], mode="centroid")],
}

# --------------------------------------------------------------------------------------------------
# Lamps (public lamp number -> the bulb-mode Light that Lampz.MassAssign binds to it; none is a socket)
# --------------------------------------------------------------------------------------------------

LAMP_NOTES = {
    7: "the manual's lamp chart calls lamp 7 the Top Turbo Bumper, its switch chart calls switch 34 the Bottom one and its coil table calls coil 18 the Center one; "
       "lamps 6 and 8 and switches 33 and 35 are the left and right bumpers, so by elimination the remaining lamp, switch and coil belong to the third bumper, "
       "and L7 sits within 3 units of Bumper3, the bumper that pulses switch 34; the ROM's Lamp Test names lamp 7 BOTTOM TURBO BUMPER",
    57: "lamp 57 'Smart Missile': the script binds this playfield-apron Light and also fades the cabinet primitive PinCab_Smart with a Lampz.Callback(57); the manual "
        "puts the Smart Missile push button (switch 62, part 180-0028-00) in the cabinet",
}
LAMPS = {_n: f"L{_n}" for _n in range(1, 64) if _n not in UNBOUND_LAMPS}

# --------------------------------------------------------------------------------------------------
# Unplaced keys
# --------------------------------------------------------------------------------------------------

_FLASH_WHY = (
    "the Light{s} the script binds is a bulb-mode light-map source at playfield height (show_bulb_mesh false) and the table models no bulb or dome primitive; "
    "a raised flash-lamp socket is never placed on a light-map source"
)

UNPLACED = {
    "solenoid.4": (
        "crane lock: the manual's Crane Assembly page draws its coil assembly under the boom at the cab end, so the coil rides the sweeping boom and has no fixed playfield "
        "location; the only fixed crane anchor in the table is the rotation axis, which is the motor (coil 14), not this coil; the drawing's coil callouts print no 4L"
    ),
    "switch.60": (
        "crane left limit: the script binds no object to it (the timer-driven CraneIsLeft just sets Controller.Switch(60)), and the manual's Switch Locations "
        "drawing (printed page 29) prints 60 at the left end of the boom's sweep, at the left ramp entrance beside the left lock, not at the crane's rotation "
        "axis; the table models no limit switch there, so the switch has no coordinate until a callout measurement on that drawing places it"
    ),
    "switch.61": (
        "crane right limit: the script binds no object to it (CraneIsRight just sets Controller.Switch(61)), and the Switch Locations drawing prints 61 at the "
        "right end of the boom's sweep, at the top of the right orbit beside the VUK 47; the table has a baked mesh CraneSwitch_BM_Room near that callout, "
        "but nothing in the script ties it to 61 and its function is not established, so placing the switch on it would rest on its name alone"
    ),
    "solenoid.8": "knocker: cabinet part, the drawing's coil callouts print no 8L, and the script only plays a sound on it (SolKnocker -> KnockerSolenoid)",
    "solenoid.9": (
        "four No. 89 flash lamps, two in the crane cab and two on the backbox insert panel (the manual's '(2) CRANE (2) INSERT'): the crane cab lamps are raised on the sweeping boom, "
        "the insert lamps are backbox, and the script binds no playfield Light to Lampz index 109 (its MassAssign(109) = f9 is commented out; only lightmaps, a VR backglass sprite set "
        "and no Light follow it)"
    ),
    "solenoid.10": "left/right relay: switches drives 1-8 between the coil set and the flash-lamp set on the PPB board; it has no playfield location and the script binds nothing to it",
    "solenoid.11": (
        "general illumination relay: SolGI sets Lampz.state(0), which only drives baked lightmaps (Lampz.Callback(0)) and the ramp fade; the script never binds a Light to index 0 "
        "(no MassAssign(0)), the twenty-five gi001-gi025 Lights are bulb-mode light-map sources that draw no bulb, and the manual prints no G.I. location drawing or count, "
        "so no G.I. bulb is placed"
    ),
    "solenoid.16": "shaker motor: cabinet part (drive 16, the Cabinet Shaker Motor 12 VDC); the script leaves SolCallback(16) commented out",
    "solenoid.25": (
        "flash lamps drive 1, '(4) TOP RIGHT POLICE LIGHTS': topper lamps above the backbox; the script binds no Light to Lampz index 101, only the cabinet-topper primitives "
        "PinCab_Topper_Blue and PinCab_Top_rbulb, and the manual's drawing prints no 1R on the playfield"
    ),
    "solenoid.26": "flash lamps drive 2, '(3) PLFD UPPER LEFT (1) INSERT': " + _FLASH_WHY.format(s=" f2 (the table's f2a and f2b are bound to nothing)"),
    "solenoid.27": "flash lamps drive 3, '(2) RAMP (2) INSERT': " + _FLASH_WHY.format(s=" f3"),
    "solenoid.28": "flash lamps drive 4, '(1) PLFD - UPPER RIGHT (2) INSERT (1) BACK PANEL': " + _FLASH_WHY.format(s=" f4"),
    "solenoid.29": "flash lamps drive 5, '(3) MID RIGHT PLFD (1) INSERT': " + _FLASH_WHY.format(s=" f5"),
    "solenoid.30": "flash lamps drive 6, '(4) PLFD - LOWER RIGHT': " + _FLASH_WHY.format(s=" f6"),
    "solenoid.31": (
        "flash lamps drive 7, '(4) TOP LEFT POLICE LIGHTS': topper lamps above the backbox; the script binds no Light to Lampz index 107, only the cabinet-topper primitives "
        "PinCab_Topper_Red and PinCab_Top_lbulb, and the manual's drawing prints no 7R on the playfield"
    ),
    "solenoid.32": (
        "flash lamps drive 8, '(2) LOW LEFT PLFD (2) INSERT': the script's Lampz.MassAssign(108) = f8r is commented out, so no Light is bound to index 108 (the VR backglass "
        "sprites and baked lightmaps follow it); the table has a Light named f8 at (97.8, 1140.3) that nothing binds"
    ),
}
for _n in UNBOUND_LAMPS:
    UNPLACED[f"lamp.{_n}"] = (
        f"the script's only MassAssign line for lamp {_n} is the commented-out '{COMMENTED_LIGHTS[_n]}' line, so no Light is bound to the lamp (its baked lightmaps are driven "
        f"by live Lampz.Callback({_n}) lines for both of its light-map sets); the lamp lights two inserts, and the Lights L{_n} and {COMMENTED_LIGHTS[_n].upper()} exist in "
        "the table, but placing them would rest on their names alone"
    )
for _n, _light in LAMPS.items():
    UNPLACED[f"lamp.{_n}"] = (
        f"lamp {_n}: the script binds the Light {_light} to it (Lampz.MassAssign({_n}) = l{_n}), a bulb-mode light-map source that draws no bulb "
        "(show_bulb_mesh false), and the table models no bulb for it; a light that sits on no bulb makes no socket, so the lamp has no coordinate until a "
        "measurement on the manual's Lamp Locations drawing (printed page 31) or a modelled bulb places it"
        + ("; " + LAMP_NOTES[_n] if _n in LAMP_NOTES else "")
    )
UNPLACED["lamp.64"] = "credit button lamp: cabinet part; the script binds only the cabinet primitive PinCab_Start to it (Lampz.Callback(64)) and no Light"
for _address, _pin in ((40, 5), (41, 4), (42, 3), (43, 2), (44, 1)):
    UNPLACED[f"solenoid.{_address}"] = (
        f"CN3 pin {_pin} carries port B bit {_address - 37}, and no retained page shows anything connected to it, so there is no device to place; the script binds "
        f"nothing to solenoid {_address}"
    )

# Keys whose placements must be a Light (lamps) or a switch/coil object.
MAGNETS = {37: "LMagnet", 38: "CMagnet", 39: "RMagnet"}


class Table:
    def __init__(self, extracted: Path):
        gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
        bounds = (gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"])
        if bounds != (0.0, 0.0, WIDTH, HEIGHT):
            raise BuildError(f"gamedata.json bounds {bounds} are not (0, 0, {WIDTH}, {HEIGHT})")
        script_bytes = (extracted / "script.vbs").read_bytes()
        digest = hashlib.sha256(script_bytes).hexdigest()
        if digest != SCRIPT_SHA256:
            raise BuildError(f"script.vbs sha256 {digest} differs from the pinned {SCRIPT_SHA256}")
        # The script is Windows-1252 text; Latin-1 keeps every byte and its line breaks.
        self.text = script_bytes.decode("latin-1").replace("\r\n", "\n")
        self.lines = self.text.split("\n")
        self.items = {}
        for path in sorted((extracted / "gameitems").glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            typ = next(iter(data))
            value = data[typ]
            # VBScript identifiers are case-insensitive, so the lookup is too; the stored name is kept.
            self.items.setdefault(value["name"].lower(), []).append((typ, value))
        self._mass = None

    def get(self, name, typ):
        entries = self.items.get(name.lower())
        if not entries:
            raise BuildError(f"object {name!r} is not in the table")
        if len(entries) != 1:
            raise BuildError(f"object name {name!r} is ambiguous: {[t for t, _ in entries]}")
        got, value = entries[0]
        if got != typ:
            raise BuildError(f"object {name!r} is a {got}, expected {typ}")
        return value

    def find_lines(self, pattern):
        """Line numbers matching the pattern; a pattern that spells a newline (backslash n) is matched over the whole script."""
        if "\\n" in pattern:
            regex = re.compile(pattern, re.IGNORECASE)
            return [self.text.count("\n", 0, m.start()) + 1 for m in regex.finditer(self.text)]
        regex = re.compile(pattern, re.IGNORECASE)
        return [i + 1 for i, line in enumerate(self.lines) if regex.search(line)]

    def mass_assigns(self):
        """Every uncommented Lampz.MassAssign(index) = object line, as {index: [objects]}."""
        if self._mass is None:
            out = {}
            for line in self.lines:
                m = re.match(r"\s*Lampz\.MassAssign\((\d+)\)\s*=\s*(\w+)\s*(?:'.*)?$", line, re.IGNORECASE)
                if m:
                    out.setdefault(int(m.group(1)), []).append(m.group(2))
            self._mass = out
        return self._mass


def stored_xy(typ, value):
    if typ in ("Light", "Kicker", "Bumper", "Spinner"):
        return value["center"]["x"], value["center"]["y"]
    if typ == "HitTarget":
        return value["position"]["x"], value["position"]["y"]
    raise BuildError(f"no stored centre for object type {typ}")


def centroid_xy(value):
    points = value["drag_points"]
    return (round(sum(p["x"] for p in points) / len(points), 6), round(sum(p["y"] for p in points) / len(points), 6))


def mesh_centre(name):
    if name not in MESH_BOUNDS:
        raise BuildError(f"{name} has no embedded world-space mesh bounds")
    xmin, ymin, xmax, ymax = MESH_BOUNDS[name]
    return round((xmin + xmax) / 2, 4), round((ymin + ymax) / 2, 4)


def inside(name, x, y):
    xmin, ymin, xmax, ymax = MESH_BOUNDS[name]
    return xmin <= x <= xmax and ymin <= y <= ymax


def shows_bulb(value):
    """A Light makes a socket on its own only when it is a bulb Light that also draws its bulb mesh."""
    return bool(value.get("is_bulb_light")) and bool(value.get("show_bulb_mesh"))


def check_inside_mesh(table: Table, key: str, mesh: str, walls):
    for wall in walls:
        x, y = centroid_xy(table.get(wall, "Wall"))
        if not inside(mesh, x, y):
            raise BuildError(f"{key}: wall {wall} centroid ({x}, {y}) is not inside the world-space bounds of {mesh}")


def crane_pivot(table: Table):
    positions = []
    for name in CRANE_PRIMITIVES:
        pos = table.get(name, "Primitive")["position"]
        positions.append((pos["x"], pos["y"]))
    if len({(round(x, 4), round(y, 4)) for x, y in positions}) != 1:
        raise BuildError(f"the three crane primitives do not share one pivot: {positions}")
    return positions[0]


def check_crane(table: Table, key: str, choice: Choice):
    pivot = crane_pivot(table)
    for name in CRANE_PRIMITIVES:
        if not inside(name, *pivot):
            raise BuildError(f"{key}: crane pivot {pivot} is not inside the world-space bounds of {name}")
    # The script rides the ball on a circle of radius 69.2 around LCrane_BM_Room's x/y; at the right limit the ball must sit on KickerBolaIn.
    for pattern in (r"CraneBall\.X = Cos\(\(-13\.5\+315 \+ CranePositionA\)\*Pi/180\)\*69\.2 \+ LCrane_BM_Room\.x",
                    r"CraneBall\.Y = Sin\(\(-13\.5\+315 \+ CranePositionA\)\*Pi/180\)\*69\.2 \+ LCrane_BM_Room\.y",
                    r"Const CraneMinA = -312\b"):
        if not table.find_lines(pattern):
            raise BuildError(f"{key}: crane pattern {pattern!r} does not match script.vbs")
    angle = math.radians(-13.5 + 315 - 312)
    ball = (math.cos(angle) * CRANE_BALL_RADIUS + pivot[0], math.sin(angle) * CRANE_BALL_RADIUS + pivot[1])
    pickup = table.get("KickerBolaIn", "Kicker")["center"]
    if math.dist(ball, (pickup["x"], pickup["y"])) > 6.0:
        raise BuildError(f"{key}: the right-limit crane ball {ball} is not on KickerBolaIn ({pickup['x']}, {pickup['y']})")


def resolve(table: Table, key: str, choice: Choice):
    value = table.get(choice.obj, choice.typ)
    if choice.typ == "Flasher":
        raise BuildError(f"{key}: {choice.obj} is a Flasher sprite, never a socket")
    if choice.typ == "Primitive" and "_LM_" in choice.obj:
        raise BuildError(f"{key}: {choice.obj} is a baked lightmap, never a socket")
    if choice.typ == "Light":
        if not key.startswith("lamp."):
            raise BuildError(f"{key}: a Light is placed only for a lamp")
        if not value.get("is_bulb_light"):
            raise BuildError(f"{key}: {choice.obj} is not a bulb-mode Light")
        if not shows_bulb(value):
            raise BuildError(f"{key}: {choice.obj} draws no bulb; a light-map source is never a socket")
        if value.get("is_backglass"):
            raise BuildError(f"{key}: {choice.obj} is a backglass light")
    if key.startswith("lamp.") and choice.typ != "Light":
        raise BuildError(f"{key}: a lamp is placed only on its bound Light")
    if choice.typ == "Primitive":
        if choice.mode == "mesh" and not value.get("is_visible"):
            raise BuildError(f"{key}: {choice.obj} is a hidden primitive")
        if choice.mode not in ("mesh", "pivot"):
            raise BuildError(f"{key}: a primitive is placed at its world-space mesh centre or the crane pivot, never its stored position")
    if choice.mode == "center":
        raw_x, raw_y = stored_xy(choice.typ, value)
    elif choice.mode == "centroid":
        raw_x, raw_y = centroid_xy(value)
    elif choice.mode == "mesh":
        raw_x, raw_y = mesh_centre(choice.obj)
    elif choice.mode == "pivot":
        raw_x, raw_y = crane_pivot(table)
    else:
        raise BuildError(f"{key}: unknown mode {choice.mode}")
    x, y = round(raw_x / WIDTH, 6), round(raw_y / HEIGHT, 6)
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        raise BuildError(f"{key}: {choice.obj} is outside the playfield: raw ({raw_x}, {raw_y}) -> ({x}, {y})")
    for pattern in choice.bind:
        if not table.find_lines(pattern):
            raise BuildError(f"{key}: binding pattern {pattern!r} for {choice.obj} does not match script.vbs")
    if choice.extra:
        choice.extra(table, key, choice)
    return {
        "coordinate_origin": ORIGIN[choice.mode],
        "object": value["name"],
        "object_type": choice.typ,
        "raw": {"x": raw_x, "y": raw_y},
        "x": x,
        "y": y,
    }


def verify_geometry(table: Table):
    """Cross-checks that tie the bumper, slingshot and magnet identities to the manual's Left / Center / Right naming."""
    bumper = {name: table.get(name, "Bumper")["center"]["x"] for name in ("Bumper1", "Bumper2", "Bumper3")}
    if not bumper["Bumper1"] < bumper["Bumper3"] < bumper["Bumper2"]:
        raise BuildError(f"the bumpers are no longer left, center, right in x: {bumper}")
    lower = table.get("Bumper3", "Bumper")["center"]["y"]
    if not lower > max(table.get("Bumper1", "Bumper")["center"]["y"], table.get("Bumper2", "Bumper")["center"]["y"]):
        raise BuildError("Bumper3 is no longer the lowest (front-most) bumper")
    left, right = centroid_xy(table.get("LeftSlingshot", "Wall")), centroid_xy(table.get("RightSlingshot", "Wall"))
    if not left[0] < right[0]:
        raise BuildError("the slingshots are no longer left, right in x")
    magnets = {n: centroid_xy(table.get(name, "Trigger")) for n, name in MAGNETS.items()}
    if not magnets[37][0] < magnets[38][0] < magnets[39][0]:
        raise BuildError(f"the magnets are no longer left, center, right in x: {magnets}")
    # L6/L7/L8 sit on the bumper that pulses the same side's switch (within 3 units).
    for lamp, bump in ((6, "Bumper1"), (7, "Bumper3"), (8, "Bumper2")):
        lx, ly = stored_xy("Light", table.get(f"L{lamp}", "Light"))
        bx, by = stored_xy("Bumper", table.get(bump, "Bumper"))
        if math.dist((lx, ly), (bx, by)) > 3.0:
            raise BuildError(f"lamp {lamp}'s Light is not on {bump}")
    # Trough order: the drain-end kicker is the left-most, the release slot the right-most.
    xs = [table.get(f"sw{n}", "Kicker")["center"]["x"] for n in range(9, 16)]
    if xs != sorted(xs):
        raise BuildError(f"the trough kickers sw9-sw15 are no longer ordered left to right: {xs}")


def verify_lamp_bindings(table: Table):
    """Lamp bindings must be exactly the expected Lights; flash indices exactly the expected flash Lights."""
    mass = table.mass_assigns()
    for n in range(1, 65):
        expected = [f"l{n}"] if n in LAMPS else []
        got = [name.lower() for name in mass.get(n, [])]
        if got != expected:
            raise BuildError(f"lamp {n}: Lampz.MassAssign binds {got}, expected {expected}")
    for n in UNBOUND_LAMPS:
        light = COMMENTED_LIGHTS[n]
        if not table.find_lines(rf"^\s*'\s*Lampz\.MassAssign\({n}\)\s*=\s*{light}\b"):
            raise BuildError(f"lamp {n}: the commented-out MassAssign line for {light} is gone")
        for name in (f"l{n}", light):
            table.get(name, "Light")
    for index, lights in FLASH_LIGHTS.items():
        got = [name.lower() for name in mass.get(index, []) if not name.upper().startswith("BGFL")]
        if got != list(lights):
            raise BuildError(f"flash index {index}: Lampz.MassAssign binds {got}, expected {list(lights)}")
    for index in (101, 107):
        if any(not name.upper().startswith("BGFL") for name in mass.get(index, [])):
            raise BuildError(f"flash index {index} is bound to a Light after all")
    for index in (108, 109):
        if [name for name in mass.get(index, []) if not name.upper().startswith("BGFL")]:
            raise BuildError(f"flash index {index} is bound to a Light after all")
        if not table.find_lines(rf"^\s*'\s*Lampz\.MassAssign\({index}\)\s*=\s*f{'8r' if index == 108 else '9'}\b"):
            raise BuildError(f"flash index {index}: the commented-out MassAssign line is gone")
    if 0 in mass:
        raise BuildError("Lampz index 0 (the G.I.) is bound to a Light after all")
    for n, pattern in ((25, 101), (26, 102), (27, 103), (28, 104), (29, 105), (30, 106), (31, 107), (32, 108), (9, 109)):
        if not table.find_lines(rf'^\s*SolCallBack\({n}\)\s*=\s*"Lampz\.SetLamp {pattern},"'):
            raise BuildError(f"solenoid {n} no longer drives Lampz index {pattern}")
    if not table.find_lines(r'SolCallback\(11\)\s*=\s*"SolGI"') or not table.find_lines(r"Lampz\.state\(0\) = 1"):
        raise BuildError("solenoid 11 no longer drives Lampz.state(0)")
    if not table.find_lines(r'SolCallback\(8\)\s*=\s*"SolKnocker"') or not table.find_lines(r"Sub SolKnocker\(Enabled\)\s*\n\s*If enabled Then\s*\n\s*KnockerSolenoid"):
        raise BuildError("solenoid.8: the script no longer only sounds the knocker")
    if not table.find_lines(r"^\s*'SolCallback\(16\)") or not table.find_lines(r"^\s*'SolCallback\(10\)"):
        raise BuildError("solenoids 10 or 16 are bound after all")
    for light in GI_LIGHTS:
        value = table.get(light, "Light")
        if not value.get("is_bulb_light") or shows_bulb(value):
            raise BuildError(f"{light} is not a bulb-mode Light without a bulb mesh")
    for name in ("f2", "f3", "f4", "f5", "f6"):
        value = table.get(name, "Light")
        if not value.get("is_bulb_light") or shows_bulb(value):
            raise BuildError(f"{name} is not a bulb-mode Light without a bulb mesh")
    for n in LAMPS:
        value = table.get(f"L{n}", "Light")
        if shows_bulb(value):
            raise BuildError(f"L{n} draws a bulb mesh; the precedent for insert Lights would need revisiting")
    # No modelled bulb or dome primitive exists that a raised socket could stand on.
    for name, entries in table.items.items():
        for typ, value in entries:
            if typ == "Primitive" and re.search(r"bulb|dome|flasherbase", value["name"], re.IGNORECASE) and not value["name"].startswith("PinCab_"):
                raise BuildError(f"{value['name']}: a modelled bulb or dome primitive exists; the flash lamps need revisiting")


def lightmap_entries(table: Table):
    """Every baked lightmap primitive that Lampz.Callback fades with a lamp, as (key, object)."""
    pairs = set()
    regex = re.compile(r'^\s*Lampz\.Callback\((\d+)\)\s*=\s*"Update\w*LightMap\s+(\w+),\s*100\.0,\s*"', re.IGNORECASE)
    for line in table.lines:
        m = regex.match(line)
        if not m:
            continue
        index, name = int(m.group(1)), m.group(2)
        if index == 0:
            key = "solenoid.11"
        elif 1 <= index <= 64:
            key = f"lamp.{index}"
        elif index in FLASH_LAMPZ:
            key = f"solenoid.{FLASH_LAMPZ[index]}"
        else:
            raise BuildError(f"Lampz.Callback({index}) is outside the known lamp indices")
        if "_LM_" not in name:
            raise BuildError(f"Lampz.Callback({index}) fades {name}, which is not a lightmap primitive")
        table.get(name, "Primitive")
        pairs.add((key, name))
    if len(pairs) < 500:
        raise BuildError(f"only {len(pairs)} lightmap callbacks found; the script changed")
    return sorted(pairs)


def rejected_entries(table: Table):
    out = []
    for key, name in lightmap_entries(table):
        out.append({"key": key, "object": name, "reason": "baked VLM lightmap primitive faded by Lampz.Callback; never a socket"})
    for index, names in CABINET_CALLBACKS.items():
        key = f"lamp.{index}" if index < 100 else f"solenoid.{FLASH_LAMPZ[index]}"
        for name in names:
            table.get(name, "Primitive")
            if not table.find_lines(rf'^\s*Lampz\.Callback\({index}\)\s*=\s*"DisableLighting {name}, '):
                raise BuildError(f"{key}: {name} is not faded by Lampz.Callback({index})")
            out.append({"key": key, "object": name, "reason": "cabinet or topper primitive faded by a DisableLighting callback; not on the playfield"})
    for index, lights in FLASH_LIGHTS.items():
        key = f"solenoid.{FLASH_LAMPZ[index]}"
        for name in lights:
            value = table.get(name, "Light")
            if not table.find_lines(rf"^\s*Lampz\.MassAssign\({index}\)\s*=\s*{name}\b"):
                raise BuildError(f"{key}: {name} is not bound to Lampz index {index}")
            if not value.get("is_bulb_light") or shows_bulb(value):
                raise BuildError(f"{key}: {name} must be a bulb-mode Light that draws no bulb")
            out.append({"key": key, "object": value["name"],
                        "reason": "bulb-mode light-map source at playfield height bound to the flash lamp, with no bulb or dome modelled; a raised flash-lamp socket is not placed on it"})
    for n, light in LAMPS.items():
        value = table.get(light, "Light")
        if not table.find_lines(rf"^\s*Lampz\.MassAssign\({n}\)\s*=\s*{light}\b"):
            raise BuildError(f"lamp.{n}: {light} is not bound to the lamp")
        if not value.get("is_bulb_light") or shows_bulb(value):
            raise BuildError(f"lamp.{n}: {light} must be a bulb-mode Light that draws no bulb")
        out.append({"key": f"lamp.{n}", "object": value["name"],
                    "reason": "bulb-mode light-map source bound to the lamp by Lampz.MassAssign; it draws no bulb (show_bulb_mesh false), so it is not a socket"})
    for n, light in COMMENTED_LIGHTS.items():
        out.append({"key": f"lamp.{n}", "object": table.get(light, "Light")["name"],
                    "reason": "second-bulb Light whose Lampz.MassAssign line is commented out in the script; never bound to the lamp"})
    for n, prefix in BACKGLASS_FLASHERS.items():
        count = BACKGLASS_COUNTS[n]
        for i in range(1, count + 1):
            name = f"{prefix}{i}"
            table.get(name, "Flasher")
            index = next(k for k, v in FLASH_LAMPZ.items() if v == n)
            if not table.find_lines(rf"^\s*Lampz\.MassAssign\({index}\)\s*=\s*{name}\b"):
                raise BuildError(f"solenoid.{n}: {name} is not bound to Lampz index {index}")
            out.append({"key": f"solenoid.{n}", "object": name,
                        "reason": "VR backglass Flasher sprite bound to the flash lamp (VR mode only); backbox, never a playfield socket"})
    return sorted(out, key=lambda e: (e["key"], e["object"]))


def build(table: Table):
    verify_geometry(table)
    verify_lamp_bindings(table)
    placements = {}
    for prefix, group in (("switch", SWITCHES), ("solenoid", SOLENOIDS)):
        for number in sorted(group):
            key = f"{prefix}.{number}"
            placements[key] = sorted((resolve(table, key, choice) for choice in group[number]), key=lambda p: p["object"])
    overlap = set(placements) & set(UNPLACED)
    if overlap:
        raise BuildError(f"keys both placed and unplaced: {sorted(overlap)}")
    return {
        "format": "pinmame-vpx-placement-resolution",
        "placements": placements,
        "rejected": rejected_entries(table),
        "source": SOURCE,
        "table_bounds": {"height": HEIGHT, "width": WIDTH},
        "unplaced": [{"key": key, "reason": reason} for key, reason in sorted(UNPLACED.items())],
        "version": 1,
    }


def render(document) -> bytes:
    return (json.dumps(document, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def derive_mesh_bounds(obj_path: Path) -> dict:
    """Recompute MESH_BOUNDS from the retained world-space OBJ export, refusing any other export."""
    digest = hashlib.sha256()
    bounds: dict[str, list[float]] = {}
    current = None
    with obj_path.open("rb") as stream:
        for line in stream:
            digest.update(line)
            if line.startswith(b"o "):
                current = line[2:].strip().decode("utf-8")
            elif line.startswith(b"v ") and current in MESH_BOUNDS:
                x, y = (float(value) for value in line.split()[1:3])
                box = bounds.setdefault(current, [x, y, x, y])
                box[0], box[1], box[2], box[3] = min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)
    if digest.hexdigest() != WORLD_OBJ_SHA256:
        raise BuildError(f"{obj_path} sha256 {digest.hexdigest()} is not the pinned world-space export {WORLD_OBJ_SHA256}")
    return {name: tuple(round(value, 4) for value in box) for name, box in sorted(bounds.items())}


def check_mesh_bounds(obj_path: Path) -> None:
    derived = derive_mesh_bounds(obj_path)
    if derived != dict(sorted(MESH_BOUNDS.items())):
        raise BuildError(f"embedded MESH_BOUNDS differ from the world-space export: {derived}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--extracted", required=True, type=Path, help="retained vpxtool extraction directory")
    parser.add_argument("--output", required=True, type=Path, help="last_action_hero_places.json to write (or compare with --check)")
    parser.add_argument("--check", action="store_true", help="compare --output with the generated bytes")
    parser.add_argument("--world-obj", type=Path, help="retained 'vpxtool export obj --units vpu' export; re-derives MESH_BOUNDS and fails on a mismatch")
    args = parser.parse_args(argv)
    try:
        if args.world_obj:
            check_mesh_bounds(args.world_obj)
            print(f"MESH_BOUNDS match {args.world_obj}")
        data = render(build(Table(args.extracted)))
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.check:
        current = args.output.read_bytes() if args.output.is_file() else None
        if current != data:
            print(f"DRIFT: {args.output} differs from the regenerated placements", file=sys.stderr)
            return 1
        print(f"{args.output} is up to date")
        return 0
    args.output.write_bytes(data)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
