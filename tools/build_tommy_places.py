#!/usr/bin/env python3
"""Resolve normalized playfield coordinates for The Who's Tommy Pinball Wizard (Data East 1994).

Reads the retained VPW Mod 1.2.1 extraction (``gamedata.json`` bounds, ``gameitems/*.json`` and
``script.vbs``) and writes ``tools/tommy_places.json`` in the ``pinmame-vpx-placement-resolution``
format used by the other Data East records. Every table object is chosen by what ``script.vbs``
actually binds to the ROM switch, lamp or coil, never by its name alone; the choice, the reason and
the script pattern that proves the binding are hard-coded in the tables below, and the builder fails
closed when a named object is missing, ambiguous, outside the table, hidden when the reason needs it
visible, or when a binding pattern no longer matches the script.

Coordinate convention: x = 0 is the left side and x = 1 the right side, y = 0 is the rear/backglass
end and y = 1 the front/apron end. ``x = raw_x / 952`` and ``y = raw_y / 2162``, rounded to six
decimals.

Origins:

``measured-center``
    the object's stored centre (Light, Kicker, Trigger, Spinner, Bumper) or position (HitTarget).
``computed-centroid``
    the mean of a Wall's drag points (slingshots, diverter, mirror target).
``mesh-bounds-center``
    the centre of the x/y bounding box of a primitive's world-space mesh. The meshes are exported
    with ``vpxtool export obj --units vpu``; the bounds are embedded in ``MESH_BOUNDS`` below so the
    builder needs no external file. ``--world-obj`` (or the default location under the review
    artifacts root) re-derives them from the export and fails on a mismatch.

Usage::

    python tools/build_tommy_places.py --extracted <extracted dir> --output tools/tommy_places.json
    python tools/build_tommy_places.py --extracted <extracted dir> --output tools/tommy_places.json --check
    python tools/build_tommy_places.py --extracted <extracted dir> --report <placement-report.md>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

WIDTH = 952.0
HEIGHT = 2162.0

SCRIPT_SHA256 = "c6d74cb6fafd0aad6c12129272a3cd0a4f5086b2f75c7f6f8d00850e555717d1"
VPX_SHA256 = "65b781c4ce13f253dace8003b4c06fe55d447255d51eb9821732c64bad4c7d0b"
WORLD_OBJ_SHA256 = "94a1844d11cfe4132e9e6a1f4be75df38637dd502066a10ff0b0eca60fd3cc67"

SOURCE = (
    "VPW Mod 1.2.1 extraction (gamedata.json bounds, gameitems, script.vbs sha256 " + SCRIPT_SHA256
    + "), objects chosen from script.vbs bindings; mesh bounds from the vpxtool 0.33.3 "
    "'export obj --units vpu' world-space export (sha256 " + WORLD_OBJ_SHA256 + ") of the VPX (sha256 "
    + VPX_SHA256 + ")"
)

# x/y bounding boxes (xmin, ymin, xmax, ymax) of world-space meshes in the table's saved pose. The
# OBJ export maps world x/y to OBJ x/y and negates the height.
MESH_BOUNDS = {
    "BlinderP1": (403.9059, 1874.6683, 798.6606, 2170.3416),
    "BlinderP2": (403.7647, 1879.1448, 775.0441, 2175.9863),
    "Flasherbase1": (863.8799, 43.9076, 922.9100, 103.4851),
    "Flasherbase2": (22.3119, 1056.0449, 71.7068, 1155.8940),
    "Flasherbase3": (124.2267, -0.1200, 172.2267, 43.9588),
    "Flasherbase4": (284.2248, -0.1200, 332.2248, 43.9588),
    "Flasherbase5": (620.2789, -0.1200, 668.2789, 43.9588),
    "Flasherbase6": (763.2014, -0.1200, 811.2014, 43.9588),
    "Flasherbase7": (45.3119, 52.3359, 104.3419, 111.9134),
    "MirrorP": (674.6269, 469.1802, 769.3731, 576.3198),
    "Propeller1": (159.4016, 184.8034, 289.2508, 248.6699),
    "Propeller2": (662.4016, 184.8034, 792.2508, 248.6699),
}

ORIGIN = {
    "center": "measured-center",
    "centroid": "computed-centroid",
    "mesh": "mesh-bounds-center",
}


class BuildError(RuntimeError):
    pass


class Choice:
    """One table object chosen for a key, with the reason and the script patterns proving the binding."""

    def __init__(self, obj, typ, why, bind, mode="center", doubles=(), companion=None, visible=None,
                 note=None):
        self.obj = obj
        self.typ = typ
        self.why = why
        self.bind = list(bind)
        self.mode = mode
        self.doubles = list(doubles)
        self.companion = companion
        self.visible = visible
        self.note = note


def hit(obj):
    return [rf"Sub\s+{obj}_Hit\b"]


def lamp_bind(n, *objs):
    return [rf"Lampz\.MassAssign\({n}\)\s*=\s*{o}\b" for o in objs]


# --------------------------------------------------------------------------------------------------
# Switches (public switch number -> chosen table object)
# --------------------------------------------------------------------------------------------------

SWITCHES = {}

for _n, _o, _w in (
    (9, "sw9", "trough position 6, the drain-side end of the physical trough"),
    (10, "sw10", "trough position 5"),
    (11, "sw11", "trough position 4"),
    (12, "sw12", "trough position 3"),
    (13, "sw13", "trough position 2"),
    (14, "sw14", "trough position 1, the ball-release end"),
):
    SWITCHES[_n] = [Choice(_o, "Kicker", f"{_w}; the script sets Controller.Switch({_n}) from {_o}_Hit/_UnHit",
                           hit(_o) + [rf"Sub\s+{_o}_UnHit\b"])]

SWITCHES[15] = [Choice(
    "sw15", "Kicker",
    "ball-release/shooter-feed position: no sw15 handler exists, SolTrough sets Controller.Switch(15)=1 and "
    "SolRelease clears it after sw15.kick, so sw15 is the kicker that holds the released ball",
    [r"Controller\.Switch\(15\)\s*=\s*1", r"Controller\.Switch\(15\)\s*=\s*0", r"sw15\.kick"])]
SWITCHES[16] = [Choice(
    "sw16", "Trigger", "shooter-lane trigger; sw16_Hit sets Controller.Switch(16) and plungerIM.Switch 16",
    hit("sw16") + [r"\.Switch 16"])]
SWITCHES[17] = [Choice(
    "LeftSlingShot", "Wall", "left slingshot wall: LeftSlingShot_Slingshot pulses switch 17 (drag-point centroid)",
    [r"Sub\s+LeftSlingShot_Slingshot", r"vpmTimer\.PulseSw 17\b"], mode="centroid")]
SWITCHES[18] = [Choice(
    "RightSlingShot", "Wall", "right slingshot wall: RightSlingShot_Slingshot pulses switch 18 (drag-point centroid)",
    [r"Sub\s+RightSlingShot_Slingshot", r"vpmTimer\.PulseSw 18\b"], mode="centroid")]
SWITCHES[19] = [Choice(
    "sw19", "Kicker", "vertical up kicker (VUK); sw19_hit sets Controller.Switch(19)=1",
    [r"Sub\s+sw19_hit\b", r"Controller\.Switch\(19\)\s*=\s*1"])]

for _n, _o, _w in (
    (20, "sw20", "left ramp left standup target"),
    (21, "sw21", "left ramp right standup target"),
    (22, "sw22", "right ramp standup target"),
):
    SWITCHES[_n] = [Choice(
        _o, "HitTarget",
        f"{_w}; {_o}_Hit calls STHit {_n} (target array ST{_n} = Array({_o}, {_o}p, {_n}, 0)); the HitTarget is "
        f"visible and carries the collision",
        [rf"Sub\s+{_o}_Hit\s*:\s*STHit {_n}\b", rf"ST{_n}\s*=\s*Array\({_o},"], visible=True)]

SWITCHES[23] = [Choice(
    "sw23", "Kicker", "left scoop kicker; sw23_hit sets Controller.Switch(23)=1",
    [r"sub\s+sw23_hit\b", r"Controller\.Switch\(23\)\s*=\s*1"])]
SWITCHES[24] = [Choice(
    "sw24", "Wall",
    "silverball standup target: sw24_Hit pulses switch 24 on the Wall (drag-point centroid); the visible sw24p "
    "animation primitive sits 18 units further back and is not what the script binds",
    [r"Sub\s+sw24_Hit\b", r"vpmTimer\.PulseSw 24\b"], mode="centroid")]

for _n, _o, _w in (
    (25, "sw25", "left target bank, lower target"),
    (26, "sw26", "left target bank, middle target"),
    (27, "sw27", "left target bank, upper target"),
    (33, "sw33", "right target bank, upper target"),
    (34, "sw34", "right target bank, middle target"),
    (35, "sw35", "right target bank, lower target"),
    (38, "sw38", "middle standup target"),
    (43, "sw43", "captive-ball standup target"),
):
    SWITCHES[_n] = [Choice(
        _o, "HitTarget",
        f"{_w}; {_o}_Hit calls STHit {_n} (ST{_n} = Array({_o}, {_o}p, {_n}, 0)). The HitTarget is invisible and "
        f"carries the collision; the visible {_o}p primitive sits at the same position",
        [rf"Sub\s+{_o}_Hit\s*:\s*STHit {_n}\b", rf"ST{_n}\s*=\s*Array\({_o},"], companion=f"{_o}p")]

SWITCHES[28] = [Choice(
    "MirrorP", "Primitive",
    "mirror motor UP limit: synthesized, no own geometry. MirrorTimer_Timer sets Controller.Switch(28)=1 when "
    "MirrorP.Z >= 137, so the switch is projected onto the mirror mechanism's primitive (mesh bounds centre)",
    [r"If MirrorP\.Z >= 137 then", r"Controller\.Switch\(28\)\s*=\s*1"], mode="mesh", visible=True)]
SWITCHES[29] = [Choice(
    "sw29", "Trigger", "rollover trigger; sw29_Hit sets Controller.Switch(29)=1",
    hit("sw29") + [r"Controller\.Switch\(29\)\s*=\s*1"])]
SWITCHES[30] = [Choice(
    "sw30", "Trigger", "right-ramp entry trigger (flap sw30p follows Spinner_RightRamp); sw30_Hit sets "
    "Controller.Switch(30)=1", [r"Sub\s+sw30_Hit\b", r"Controller\.Switch\(30\)\s*=\s*1"])]
SWITCHES[31] = [Choice(
    "MirrorP", "Primitive",
    "mirror motor DOWN limit: synthesized, no own geometry. MirrorTimer_Timer sets Controller.Switch(31)=1 when "
    "MirrorP.Z <= 3, so the switch is projected onto the mirror mechanism's primitive (mesh bounds centre)",
    [r"If MirrorP\.Z <= 3 then", r"Controller\.Switch\(31\)\s*=\s*1"], mode="mesh", visible=True)]
SWITCHES[32] = [Choice(
    "sw32", "Wall", "mirror target wall: sw32_Hit pulses switch 32 via ShakeMirror (drag-point centroid)",
    [r"Sub\s+sw32_Hit\b", r"vpmTimer\.PulseSw 32\b"], mode="centroid")]
SWITCHES[36] = [Choice(
    "sw36", "Trigger", "rollover trigger; sw36_Hit sets Controller.Switch(36)=1",
    [r"Sub\s+sw36_Hit\b", r"Controller\.Switch\(36\)\s*=\s*1"])]
SWITCHES[37] = [Choice(
    "sw37", "Trigger", "rollover trigger; sw37_Hit sets Controller.Switch(37)=1",
    [r"Sub\s+sw37_Hit\b", r"Controller\.Switch\(37\)\s*=\s*1"])]
SWITCHES[39] = [Choice(
    "sw39", "Spinner", "left spinner; sw39_Spin pulses switch 39", [r"Sub\s+sw39_Spin\b.*PulseSw 39\b"], visible=True)]
SWITCHES[40] = [Choice(
    "sw40", "Spinner", "right spinner; sw40_Spin pulses switch 40", [r"Sub\s+sw40_Spin\b.*PulseSw 40\b"], visible=True)]
SWITCHES[41] = [Choice(
    "sw41", "Trigger", "under-playfield trough switch of the mirror hole (SubwayRamp); sw41_Hit pulses switch 41",
    [r"Sub\s+sw41_Hit\b", r"vpmTimer\.PulseSw 41\b"])]
SWITCHES[42] = [Choice(
    "sw42", "Trigger", "under-playfield trough switch of the skill-shot hole (SubwayRamp); sw42_Hit pulses switch 42",
    [r"Sub\s+sw42_Hit\b", r"vpmTimer\.PulseSw 42\b"])]
SWITCHES[47] = [Choice(
    "sw47", "Kicker", "top-left eject kicker; sw47_Hit sets Controller.Switch(47)=1",
    [r"Sub\s+sw47_Hit\b", r"Controller\.Switch\(47\)\s*=\s*1"])]
SWITCHES[48] = [Choice(
    "sw48", "Trigger", "rollover trigger; sw48_Hit sets Controller.Switch(48)=1",
    [r"Sub\s+sw48_Hit\b", r"Controller\.Switch\(48\)\s*=\s*1"])]
SWITCHES[49] = [Choice(
    "Bumper1", "Bumper", "top bumper: Bumper1_Hit pulses switch 49", [r"Sub\s+Bumper1_Hit\b", r"vpmTimer\.PulseSw 49\b"])]
SWITCHES[50] = [Choice(
    "Bumper2", "Bumper", "centre bumper: Bumper2_Hit pulses switch 50", [r"Sub\s+Bumper2_Hit\b", r"vpmTimer\.PulseSw 50\b"])]
SWITCHES[51] = [Choice(
    "Bumper3", "Bumper", "right bumper: Bumper3_Hit pulses switch 51", [r"Sub\s+Bumper3_Hit\b", r"vpmTimer\.PulseSw 51\b"])]
SWITCHES[55] = [Choice(
    "sw55", "Trigger", "lane trigger; sw55_Hit sets Controller.Switch(55)=1",
    [r"Sub\s+sw55_Hit\b", r"Controller\.Switch\(55\)\s*=\s*1"])]
SWITCHES[56] = [Choice(
    "sw56", "Trigger", "lane trigger; sw56_Hit sets Controller.Switch(56)=1",
    [r"Sub\s+sw56_Hit\b", r"Controller\.Switch\(56\)\s*=\s*1"])]
SWITCHES[57] = [Choice(
    "sw57", "Trigger", "left-ramp entry trigger (flap sw57p follows Spinner_LeftRamp); sw57_Hit sets "
    "Controller.Switch(57)=1", [r"Sub\s+sw57_Hit\b", r"Controller\.Switch\(57\)\s*=\s*1"])]
SWITCHES[58] = [Choice(
    "sw58", "Trigger", "wire-ramp exit trigger (Ramp2); sw58_Hit sets Controller.Switch(58)=1",
    [r"Sub\s+sw58_Hit\b", r"Controller\.Switch\(58\)\s*=\s*1"])]
SWITCHES[62] = [Choice(
    "sw62", "Trigger", "wire-ramp exit trigger (Ramp5); sw62_Hit sets Controller.Switch(62)=1",
    [r"Sub\s+sw62_Hit\b", r"Controller\.Switch\(62\)\s*=\s*1"])]


# --------------------------------------------------------------------------------------------------
# Lamps (public lamp number -> chosen Light). Every lamp is bound by ``Lampz.MassAssign(n)``.
# --------------------------------------------------------------------------------------------------

LAMPS = {}


def _lamp(n, obj, why, doubles=(), extra=()):
    LAMPS.setdefault(n, []).append(Choice(
        obj, "Light", why, lamp_bind(n, obj) + list(extra), doubles=[obj, *doubles]))


# Skitso inserts: one Light each, no halo.
for _n, _o, _w in (
    (2, "l2", "CHRISTMAS mission flag"), (3, "l3", "COUSIN KEVIN mission flag"),
    (4, "l4", "HOLIDAY CAMP mission flag"), (5, "l5", "LITE EXTRA BALL mission flag"),
    (6, "l6", "SILVER BALL mission flag"), (7, "l7", "CAPTAIN WALKER mission flag"),
    (8, "l8", "PINBALL WIZARD mission flag"), (9, "l9", "SKILL SHOT insert"),
    (11, "l11", "SMASH THE MIRROR mission flag"), (12, "l12", "FIDDLE ABOUT mission flag"),
    (13, "l13", "ACID QUEEN mission flag"), (14, "l14", "THERE'S A DOCTOR mission flag"),
    (15, "l15", "TOMMY SCORING mission flag"), (16, "l16", "SALLY SIMPSON mission flag"),
    (31, "l31", "LITE L flag"), (32, "l32", "GENIUS-WOW insert (one light)"),
    (53, "l53", "LITE R flag"), (63, "l63", "COLLECT insert"),
):
    _lamp(_n, _o, f"{_w}; single Light bound by Lampz.MassAssign({_n})")

# Silver balls: Light plus a TL reflection flasher (rejected).
for _n, _o, _w in ((20, "l20", "left silver ball"), (21, "l21", "centre silver ball"), (22, "l22", "right silver ball")):
    _lamp(_n, _o, f"{_w}; the bound reflection flasher TL{_n} is a Flasher sprite on the reflection layer",
          doubles=[f"TL{_n}"])

# Inserts with a halo Light (``*h``) and sometimes a TL reflection flasher.
for _n, _o, _w, _tl in (
    (24, "l24", "SILVERBALL insert", True), (25, "l25", "target arrow", True), (26, "l26", "target arrow", True),
    (27, "l27", "target arrow", True), (33, "l33", "target arrow", True), (34, "l34", "target arrow", True),
    (35, "l35", "target arrow", True), (38, "l38", "MORE TIME", True),
    (41, "l41", "T of TOMMY", False), (42, "l42", "O of TOMMY", False), (43, "l43", "first M of TOMMY", False),
    (44, "l44", "second M of TOMMY", False), (45, "l45", "Y of TOMMY", False),
    (17, "l17", "JACKPOT", False), (18, "l18", "DOUBLE JACKPOT", False), (29, "l29", "SPINNER BONUS (left)", False),
    (30, "l30", "EXTRA BALL", False), (36, "l36", "MYSTERY", False), (47, "l47", "MULTIBALL", False),
    (48, "l48", "SHOOT AGAIN", False), (52, "l52", "SPINNER BONUS (right)", False), (54, "l54", "HOLIDAY CAMP", False),
    (62, "l62", "MULTI BALL", False), (57, "l57", "ACID QUEEN (left)", False), (58, "l58", "ACID QUEEN (top)", False),
    (59, "l59", "ACID QUEEN (right)", False),
):
    _lamp(_n, _o, f"{_w}; the Light is the bulb, {_o}h is its halo" + (f" and TL{_n} its reflection flasher" if _tl else ""),
          doubles=[f"{_o}h"] + ([f"TL{_n}"] if _tl else []))

# Two-bulb lamps (the manual's X2 outlane and return-lane lamps).
_lamp(46, "l46", "SPECIAL left outlane bulb (X2 lamp); l46h halo and TL46 reflection are doubles",
      doubles=["l46h", "TL46"])
_lamp(46, "l46a", "SPECIAL right outlane bulb (X2 lamp); l46ah halo and TL46a reflection are doubles",
      doubles=["l46ah", "TL46a"])
_lamp(55, "l55", "DOUBLE SPINNER VALUE left return-lane bulb; l55h halo is a double", doubles=["l55h"])
_lamp(55, "l55a", "DOUBLE SPINNER VALUE right return-lane bulb; l55ah halo is a double", doubles=["l55ah"])

# Bumper lamps: the Light nearest the cap is the bulb; b/c/d are glow and skirt-reflection helpers.
for _n, _o, _b in ((49, "l49", "Bumper1 (top)"), (50, "l50", "Bumper2 (centre)"), (51, "l51", "Bumper3 (right)")):
    _lamp(_n, _o,
          f"{_b} cap lamp: the primary Light, 2-3 units from the bumper centre; {_o}b/{_o}c/{_o}d are wide glow and "
          f"skirt-highlight helpers bound to the same lamp ({_o}a is not bound in the script)",
          doubles=[f"{_o}b", f"{_o}c", f"{_o}d"])

# Ramp signs. Bulb1..Bulb4 are DisableLighting targets; Bulb3/Bulb4 do not exist in the table.
for _n, _o, _w, _extra in (
    (39, "l39", "left ramp sign lamp, DisableLighting target Bulb2", ["l39a"]),
    (60, "l60", "left ramp sign lamp, DisableLighting target Bulb1", ["l60a"]),
    (40, "l40", "right ramp sign lamp, DisableLighting target Bulb3 (absent in the table)", ["l40a", "l40b"]),
    (61, "l61", "right ramp sign lamp, DisableLighting target Bulb4 (absent in the table)", ["l61a", "l61b"]),
):
    _lamp(_n, _o, f"{_w}; the l?a/l?b Flasher sprites bound to the same lamp are rejected", doubles=_extra)

_lamp(56, "l56", "airplane lamp: the only bound Light, drawn with show_bulb_mesh and sitting on the Airplane primitive "
      "(position 476, 204)")


# --------------------------------------------------------------------------------------------------
# Solenoids (public coil number -> chosen mechanism or flasher)
# --------------------------------------------------------------------------------------------------

SOLENOIDS = {}


def _sol(n, choices):
    SOLENOIDS[n] = list(choices)


def solcb(n, name):
    return rf'SolCallback\({n}\)\s*=\s*"{name}"'


_sol(1, [Choice("sw14", "Kicker", "6-ball lockout: SolTrough kicks the trough-end kicker sw14",
                [solcb(1, "SolTrough"), r"sw14\.kick 57, 20"])])
_sol(2, [Choice("sw15", "Kicker", "ball release: SolRelease kicks sw15",
                [solcb(2, "SolRelease"), r"sw15\.kick 57, 10"])])
_sol(3, [Choice("swPlunger", "Trigger", "autolaunch: AutoLaunch fires plungerIM, initialised on swPlunger",
                [solcb(3, "AutoLaunch"), r"InitImpulseP swPlunger", r"PlungerIM\.AutoFire"])])
_sol(4, [Choice("sw19", "Kicker", "VUK: ExitVUK kicks sw19", [solcb(4, "ExitVUK"), r"sw19\.kick 0, 40"])])
_sol(5, [Choice("sw23", "Kicker", "left scoop: ExitScoop kicks sw23", [solcb(5, "ExitScoop"), r"sw23\.Kick 0, 28"])])
_sol(6, [Choice("sw47", "Kicker", "top-left eject: SolEject kicks sw47", [solcb(6, "SolEject"), r"sw47\.kick 180"])])
_sol(12, [Choice("TopDiverter", "Wall", "top diverter: Diverter drops/raises Wall TopDiverter (drag-point centroid)",
                 [solcb(12, "Diverter"), r"TopDiverter\.IsDropped = 0"], mode="centroid")])
_sol(13, [
    Choice("Propeller1", "Primitive", "airplane motor, left propeller: PropellerMove spins Propeller1 "
           "(mesh bounds centre; the stored position is the pivot, 28 units further forward)",
           [solcb(13, "PropellerMove"), r"Propeller1\.RotZ = 360 - discAngle"], mode="mesh", visible=True),
    Choice("Propeller2", "Primitive", "airplane motor, right propeller: PropellerMove spins Propeller2 "
           "(mesh bounds centre; the stored position is the pivot, 28 units further forward)",
           [solcb(13, "PropellerMove"), r"Propeller2\.RotZ = 360 - discAngle"], mode="mesh", visible=True),
])
_sol(14, [Choice("MirrorP", "Primitive", "mirror motor relay: MirrorMove raises/lowers MirrorP (stored position "
                 "equals the mesh bounds centre)", [solcb(14, "MirrorMove"), r"MirrorP\.Z = MirrorP\.Z [-+] 2"],
                 mode="mesh", visible=True)])
_sol(15, [Choice("F15", "Light", "mirror flasher X1: FlashSol15 -> Setlamp 115 -> Lampz.MassAssign(115) = F15; "
                 "the pF15 lens primitive is 3.5 units away",
                 [solcb(15, "FlashSol15"), r"Setlamp 115, 1", *lamp_bind(115, "F15")], doubles=["F15"])])
_sol(17, [Choice("Bumper1", "Bumper", "top bumper: SolCallback(17) = SolBumper1 (comment 'Top Bumper'); the "
                 "SolBumper1 body is commented out, the bumper is Bumper1 (switch 49)",
                 [solcb(17, "SolBumper1"), r"Sub\s+Bumper1_Hit\b"])])
_sol(18, [Choice("Bumper2", "Bumper", "centre bumper: SolCallback(18) = SolBumper2 (comment 'Center bumper'); the "
                 "SolBumper2 body is commented out, the bumper is Bumper2 (switch 50)",
                 [solcb(18, "SolBumper2"), r"Sub\s+Bumper2_Hit\b"])])
_sol(19, [Choice("Bumper3", "Bumper", "right bumper: SolCallback(19) = SolBumper3 (comment 'Right bumper'); the "
                 "SolBumper3 body is commented out, the bumper is Bumper3 (switch 51)",
                 [solcb(19, "SolBumper3"), r"Sub\s+Bumper3_Hit\b"])])
_sol(20, [Choice("LeftSlingShot", "Wall", "left slingshot: solLSling sets LeftSlingShot.SlingshotThreshold "
                 "(drag-point centroid)", [solcb(20, "SolLSling"), r"LeftSlingShot\.SlingshotThreshold = 2500"],
                 mode="centroid")])
_sol(21, [Choice("RightSlingShot", "Wall", "right slingshot: solRSling sets RightSlingShot.SlingshotThreshold "
                 "(drag-point centroid)", [solcb(21, "SolRSling"), r"RightSlingShot\.SlingshotThreshold = 2500"],
                 mode="centroid")])


# Flashers. Lights are the bulbs the script drives through Lampz.MassAssign(1nn); Flupper domes are the
# Flasherbase primitives of InitFlasher nr (Objlevel(nr) is raised by the Flash26/27/30/32 callbacks).
_sol(25, [
    Choice(o, "Light", f"bottom-arch flashlamp ({side}), X4 group: SolCallback(25) = 'Setlamp 125,' -> "
           f"Lampz.MassAssign(125) = {o}", [r'SolCallback\(25\)\s*=\s*"Setlamp 125,"', *lamp_bind(125, o)],
           doubles=[o])
    for o, side in (("F25A", "left, outer"), ("F25B", "left, inner"), ("F25C", "right, inner"),
                    ("F25D", "right, outer"))
])


def _dome(n, nr, group, where, mesh_note):
    base = f"Flasherbase{nr}"
    return Choice(
        base, "Primitive",
        f"{group}: Flash{n} raises Objlevel({nr}), InitFlasher {nr} binds {base} as the dome; {where}; {mesh_note}",
        [rf"Objlevel\({nr}\)\s*=\s*1", rf"InitFlasher {nr},"], mode="mesh", visible=True,
        doubles=[base, f"Flasherlight{nr}", f"Flasherlit{nr}", f"Flasherflash{nr}", f"Flasherbloom{nr}"])


_sol(26, [
    _dome(26, 1, "upper-right-corner flashlamp (X4 group)", "red dome in the corner",
          "mesh centre equals the stored position"),
])
_sol(27, [
    _dome(27, 2, "left-scoop flashlamp (X2 group)", "round dome beside the left scoop",
          "mesh centre equals the stored position"),
    Choice("F27", "Light", "left-scoop flashlamp (X2 group): Flash27 -> Lampz 127 -> Lampz.MassAssign(127) = F27; "
           "drawn with show_bulb_mesh", [solcb(27, "Flash27"), r"Lampz\.SetLamp 127, 1", *lamp_bind(127, "F27")],
           doubles=["F27"]),
])
_sol(28, [
    Choice(o, "Light", f"top-eject flashlamp (X2 group): FlashSol28 -> Setlamp 128 -> Lampz.MassAssign(128) = {o}; "
           "drawn with show_bulb_mesh", [solcb(28, "FlashSol28"), r"Setlamp 128, 1", *lamp_bind(128, o)],
           doubles=[o])
    for o in ("F28A", "F28B")
])
_sol(29, [
    Choice(o, "Light", f"bumper hot-dog flashlamp (X4 group, two Lights modelled): SolCallback(29) = 'Setlamp 129,' "
           f"-> Lampz.MassAssign(129) = {o}; pF29 is the single elongated lens both Lights sit inside",
           [r'SolCallback\(29\)\s*=\s*"Setlamp 129,"', *lamp_bind(129, o)], doubles=[o])
    for o in ("F29A", "F29B")
])
_sol(30, [
    _dome(30, nr, "back-panel flashlamp (X4 group)", f"back-wall dome {nr - 2} of 4",
          "stored y is 0.0 (the rear edge), the mesh centre is the dome's projection")
    for nr in (3, 4, 5, 6)
])
_sol(31, [
    Choice(o, "Light", f"captive-ball hot-dog flashlamp (X2 group): FlashSol31 -> Setlamp 131 -> "
           f"Lampz.MassAssign(131) = {o}; the pF31{o[-1]} lens primitive sits at the same point",
           [solcb(31, "FlashSol31"), r"Setlamp 131, 1", *lamp_bind(131, o)], doubles=[o])
    for o in ("F31A", "F31B")
])
_sol(32, [
    _dome(32, 7, "top-left flashlamp (X4 group)", "red dome in the upper-left corner",
          "mesh centre equals the stored position"),
    Choice("F32A", "Light", "top hot-dog flashlamp (X4 group): Flash32 -> Lampz 132 -> Lampz.MassAssign(132) = F32A; "
           "it sits inside the corner lens primitive pF32A", [solcb(32, "Flash32"), r"Lampz\.SetLamp 132, 1", *lamp_bind(132, "F32A")],
           doubles=["F32A"]),
])
_sol(51, [
    Choice(o, "Primitive", f"blinder motor: BlinderMove drives {o} through BlinderForward/BlinderBack (mesh bounds "
           "centre in the saved, stowed pose; the stored position is the hinge at the front edge)",
           [solcb(51, "BlinderMove"), rf"{o}\.rotY\s*=\s*{o}\.rotY"], mode="mesh", visible=True)
    for o in ("BlinderP1", "BlinderP2")
])


# --------------------------------------------------------------------------------------------------
# Keys left unplaced and objects deliberately rejected
# --------------------------------------------------------------------------------------------------

UNPLACED = {
    "lamp.1": "backbox insert lamp: the script binds only VR backglass bulbs (VRBGBulb*) to it, not a playfield object",
    "lamp.10": "backbox insert lamp: the script binds only VR backglass bulbs (VRBGBulb*) to it, not a playfield object",
    "lamp.19": "backbox insert lamp: the script binds only VR backglass bulbs (VRBGBulb*) to it, not a playfield object",
    "lamp.28": "backbox insert lamp: the script binds only VR backglass bulbs (VRBGBulb*) to it, not a playfield object",
    "lamp.37": "backbox insert lamp: the script binds only VR backglass bulbs (VRBGBulb*) to it, not a playfield object",
    "lamp.23": "cabinet button lamp: not on the playfield; the script reads it only to light its cabinet button primitives (script lines 5048-5049)",
    "lamp.64": "cabinet button lamp: not on the playfield; the script reads it only to light its cabinet button primitives (script lines 5048-5049)",
    "solenoid.8": "knocker is a cabinet device: not placed",
    "solenoid.11": "GI emitter survey deferred to the curator",
}

# (key, object, type, reason) for objects that look like candidates but are not the placement.
REJECTED = [
    ("switch.20", "sw20p", "Primitive", "hidden staging primitive at (105.0, 2039.8), far from the visible HitTarget"),
    ("switch.21", "sw21p", "Primitive", "hidden staging primitive at (151.9, 2039.3), far from the visible HitTarget"),
    ("switch.22", "sw22p", "Primitive", "hidden staging primitive at (191.4, 2046.8), far from the visible HitTarget"),
    ("switch.24", "sw24p", "Primitive", "animation primitive (transx pulse) 18 units behind the Wall the script binds"),
    ("lamp.39", "Bulb2", "Primitive", "DisableLighting target of lamp 39, not a bulb socket; its mesh centre "
     "(261.4, 649.1) is 13 units from the bound Light l39"),
    ("lamp.60", "Bulb1", "Primitive", "DisableLighting target of lamp 60, not a bulb socket; its mesh centre "
     "(261.4, 649.1) is 15 units from the bound Light l60"),
    ("lamp.39", "l39a", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("lamp.60", "l60a", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("lamp.40", "l40a", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("lamp.40", "l40b", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("lamp.61", "l61a", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("lamp.61", "l61b", "Flasher", "glow sprite bound to the same lamp, not a socket"),
    ("solenoid.25", "F25L", "Light", "wide glow (falloff 170) between F25A and F25B, not a separate lamp"),
    ("solenoid.25", "F25R", "Light", "wide glow (falloff 170) between F25C and F25D, not a separate lamp"),
    ("solenoid.31", "F31C", "Light", "wide glow (falloff 200) between F31A and F31B, not a separate lamp"),
    ("solenoid.26", "F26A", "Light", "bound to Lampz 126 but sits on no modelled dome or lens, so it is a lighting effect, not a socket"),
    ("solenoid.26", "F26B", "Light", "bound to Lampz 126 but sits on no modelled dome or lens, so it is a lighting effect, not a socket"),
    ("solenoid.26", "F26C", "Light", "bound to Lampz 126 but sits on no modelled dome or lens, so it is a lighting effect, not a socket"),
    ("solenoid.32", "F32B", "Light", "bound to Lampz 132 but sits on no modelled dome or lens along the top edge, so it is a lighting effect, not a socket"),
    ("solenoid.32", "F32C", "Light", "bound to Lampz 132 but sits on no modelled dome or lens along the top edge, so it is a lighting effect, not a socket"),
]

# Lamps whose bound TL reflection flashers are rejected as placements (positions are read from the table).
TL_LAMPS = (20, 21, 22, 24, 25, 26, 27, 33, 34, 35, 38, 46)


# Uncertainties the curator should know about; written into the human report only.
NOTES = [
    "Out of range: no chosen object lies outside 0..1. Rejected sprites do (TL46 and TL46a sit at y = -291 on the "
    "reflection layer; Flasherlight3..6 and the Flasherbase3..6 mesh minima reach y = -0.12). BlinderP1/BlinderP2 meshes "
    "extend to y = 2170.3 / 2176.0, past the 2162 front edge in the saved pose, but their centres are inside.",
    "solenoid.51 blinder: the stored position of both primitives is the hinge (419.5, 2100.0); the placement is the "
    "mesh-bounds centre of the saved, stowed pose, which is asymmetric (x 404..799). The BlinderCollide wall "
    "(centroid 443.5, 1830.7) spans the lower playfield and is not what the coil moves. Treat the blinder position as "
    "approximate.",
    "solenoid.13 propellers: the stored position (223, 245) / (726, 245) is the spin pivot; the mesh-bounds centre is "
    "28 units further toward the rear (y 216.7). The airplane hangs at height 255, so both are projections.",
    "switch.28/31: the mirror up/down limits have no geometry; both are projected onto MirrorP (mesh centre equals its "
    "stored position, 722.0, 522.75) and so share one point; switch.32 (Wall sw32 centroid 724.3, 520.6) is 3 units away.",
    "switch.15: sw15 has no Hit handler. Controller.Switch(15) is set in SolTrough and cleared in SolRelease, so the "
    "position is where the released ball waits, not a detector the script reads from geometry.",
    "solenoid.17/18/19: SolBumper1..3 bodies are commented out, so the coil-to-bumper pairing rests on the SolCallback "
    "names and comments (Top, Center, Right) plus the matching switch 49/50/51 handlers.",
    "lamp.49/50/51: the literal 'smallest falloff' rule would pick l49d/l50d/l51d, white skirt highlights 17-24 units "
    "below the cap; l49/l50/l51 are the primary bulb Lights 2-3 units from the bumper centre and were used instead. "
    "l49c/l50c/l51c sit exactly on the bumper centre.",
    "lamp.39/60 and lamp.40/61 are two lamps at nearly one location each (3-4 units apart): the left and right ramp "
    "signs carry two bound bulbs. Bulb1/Bulb2 exist as DisableLighting primitives, Bulb3/Bulb4 are named in the "
    "script but absent from the table (Lampz.Callback 40/61 would fail silently).",
    "lamp.56: l56 is the only Light bound to the lamp and carries the bulb mesh on the Airplane (Airplane position "
    "476, 204; mesh centre 475.1, 179.0).",
    "solenoid.26: the table models one red dome (Flasherbase1, upper-right corner) plus three plain Lights F26A..C with "
    "no lens primitive under them; only the dome is placed, so the manual's X4 group has one placement.",
    "solenoid.29: the manual group is X4 but the table models two Lights (F29A/F29B) inside the single elongated lens "
    "primitive pF29 (x 484..532, y 151..310, centre 507.9, 230.5). Two placements, not four.",
    "solenoid.32: dome 7 plus F32A, which sits inside the large corner lens pF32A (x 43..181, y 77..231); F32B/F32C "
    "lie along the top edge on no lens and are rejected.",
    "solenoid.30: the four back-panel domes are modelled on the rear wall at heights 41..139; the placements are their "
    "projections onto the rear edge (y = 21.9), not playfield positions.",
    "solenoid.25: F25A..D were taken as the X4 group; F25L/F25R are wide (falloff 170) glow Lights between each pair.",
    "switch.24: the Wall centroid (440.0, 566.2) is bound; the visible animation primitive sw24p is at (440.0, 548.0).",
    "switch.20-22: the hidden sw20p/sw21p/sw22p primitives sit off-table staging positions near y = 2040; the visible "
    "HitTarget sw20..22 carries both collision and appearance.",
    "Mesh bounds come from the table's saved pose (MirrorP up, blinders stowed, propellers at RotZ 0).",
]


# --------------------------------------------------------------------------------------------------
# Table access
# --------------------------------------------------------------------------------------------------

class Table:
    def __init__(self, extracted: Path):
        self.root = extracted
        gamedata = json.loads((extracted / "gamedata.json").read_text(encoding="utf-8"))
        bounds = (gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"])
        if bounds != (0.0, 0.0, WIDTH, HEIGHT):
            raise BuildError(f"gamedata.json bounds {bounds} are not (0, 0, {WIDTH}, {HEIGHT})")
        script_path = extracted / "script.vbs"
        script_bytes = script_path.read_bytes()
        digest = hashlib.sha256(script_bytes).hexdigest()
        if digest != SCRIPT_SHA256:
            raise BuildError(f"script.vbs sha256 {digest} differs from the pinned {SCRIPT_SHA256}")
        self.lines = script_bytes.decode("utf-8").splitlines()
        self.items = {}
        for path in sorted((extracted / "gameitems").glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            typ = next(iter(data))
            value = data[typ]
            name = value["name"]
            self.items.setdefault(name, []).append((typ, value))

    def get(self, name, typ):
        entries = self.items.get(name)
        if not entries:
            raise BuildError(f"object {name!r} is not in the table")
        if len(entries) != 1:
            raise BuildError(f"object name {name!r} is ambiguous: {[t for t, _ in entries]}")
        got, value = entries[0]
        if got != typ:
            raise BuildError(f"object {name!r} is a {got}, expected {typ}")
        return value

    def find_lines(self, pattern):
        regex = re.compile(pattern, re.IGNORECASE)
        return [i + 1 for i, line in enumerate(self.lines) if regex.search(line)]


def stored_xy(typ, value):
    if typ in ("Light", "Kicker", "Trigger", "Spinner", "Bumper"):
        return value["center"]["x"], value["center"]["y"]
    if typ in ("HitTarget", "Primitive"):
        return value["position"]["x"], value["position"]["y"]
    raise BuildError(f"no stored centre for object type {typ}")


def centroid_xy(value):
    points = value["drag_points"]
    return (round(sum(p["x"] for p in points) / len(points), 6),
            round(sum(p["y"] for p in points) / len(points), 6))


def is_visible(typ, value):
    for key in ("is_visible", "visible"):
        if key in value and value[key] is not None:
            return bool(value[key])
    return True


def resolve(table: Table, key: str, choice: Choice, lamp_number: int | None = None):
    """Return (placement dict, report row) for one choice, failing closed on any inconsistency."""
    value = table.get(choice.obj, choice.typ)
    if choice.typ == "Light":
        if value.get("is_backglass"):
            raise BuildError(f"{key}: {choice.obj} is a backglass light")
        if re.match(r"^TL\d", choice.obj) or re.search(r"\dh$|\dah$", choice.obj):
            raise BuildError(f"{key}: {choice.obj} is a halo or reflection double, not a bulb")
    if choice.typ == "Flasher":
        raise BuildError(f"{key}: {choice.obj} is a Flasher sprite, never a socket")
    if choice.visible and not is_visible(choice.typ, value):
        raise BuildError(f"{key}: {choice.obj} is invisible but the reason needs it visible")
    if choice.companion:
        companion = table.get(choice.companion, "Primitive")
        if not is_visible("Primitive", companion):
            raise BuildError(f"{key}: companion {choice.companion} is not visible")
        cx, cy = stored_xy("Primitive", companion)
        ox, oy = stored_xy(choice.typ, value)
        if abs(cx - ox) > 2.5 or abs(cy - oy) > 2.5:
            raise BuildError(f"{key}: companion {choice.companion} is not at {choice.obj}'s position")
    if choice.mode == "center":
        raw_x, raw_y = stored_xy(choice.typ, value)
    elif choice.mode == "centroid":
        raw_x, raw_y = centroid_xy(value)
    elif choice.mode == "mesh":
        if choice.obj not in MESH_BOUNDS:
            raise BuildError(f"{key}: no mesh bounds for {choice.obj}")
        x0, y0, x1, y1 = MESH_BOUNDS[choice.obj]
        raw_x, raw_y = round((x0 + x1) / 2, 4), round((y0 + y1) / 2, 4)
    else:
        raise BuildError(f"{key}: unknown mode {choice.mode}")
    x, y = round(raw_x / WIDTH, 6), round(raw_y / HEIGHT, 6)
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        raise BuildError(f"{key}: {choice.obj} is outside the playfield: raw ({raw_x}, {raw_y}) -> ({x}, {y})")
    bindings = {}
    for pattern in choice.bind:
        lines = table.find_lines(pattern)
        if not lines:
            raise BuildError(f"{key}: binding pattern {pattern!r} for {choice.obj} does not match script.vbs")
        bindings[pattern] = lines
    for double in choice.doubles:
        if double not in table.items:
            raise BuildError(f"{key}: collapsed object {double!r} is not in the table")
    placement = {
        "coordinate_origin": ORIGIN[choice.mode],
        "object": choice.obj,
        "object_type": choice.typ,
        "raw": {"x": raw_x, "y": raw_y},
        "x": x,
        "y": y,
    }
    if choice.doubles:
        placement["collapsed_from"] = sorted(set(choice.doubles))
    row = {"key": key, "choice": choice, "raw": (raw_x, raw_y), "norm": (x, y), "bindings": bindings}
    return placement, row


def verify_lamp_bindings(table: Table):
    """Every collapsed double of a lamp must itself be bound to that lamp in the script."""
    for n, choices in LAMPS.items():
        for choice in choices:
            for double in choice.doubles:
                if not table.find_lines(rf"Lampz\.MassAssign\({n}\)\s*=\s*{double}\b"):
                    raise BuildError(f"lamp.{n}: {double} is not bound by Lampz.MassAssign({n})")


def rejected_entries(table: Table):
    out = []
    for key, obj, typ, reason in REJECTED:
        table.get(obj, typ)
        out.append({"key": key, "object": obj, "reason": reason})
    for n in TL_LAMPS:
        for name in sorted(table.items):
            if re.fullmatch(rf"TL{n}a?", name):
                if not table.find_lines(rf"Lampz\.MassAssign\({n}\)\s*=\s*{name}\b"):
                    raise BuildError(f"{name} is not bound to lamp {n}")
                value = table.get(name, "Flasher")
                out.append({"key": f"lamp.{n}", "object": name, "reason": (
                    f"reflection Flasher sprite at ({value['pos_x']:g}, {value['pos_y']:g}), bound to the lamp but "
                    f"not at the bulb")})
    for n in (49, 50, 51):
        name = f"l{n}a"
        table.get(name, "Light")
        if table.find_lines(rf"Lampz\.MassAssign\({n}\)\s*=\s*{name}\b"):
            raise BuildError(f"{name} unexpectedly bound to lamp {n}")
        out.append({"key": f"lamp.{n}", "object": name, "reason": "wide ceiling light that no Lampz.MassAssign binds"})
    return sorted(out, key=lambda e: (e["key"], e["object"]))


def unplaced_entries():
    return [{"key": key, "reason": reason} for key, reason in sorted(UNPLACED.items())]


def build(table: Table):
    verify_lamp_bindings(table)
    placements = {}
    rows = []
    for prefix, group in (("switch", SWITCHES), ("lamp", LAMPS), ("solenoid", SOLENOIDS)):
        for number in sorted(group):
            key = f"{prefix}.{number}"
            entries = []
            for choice in group[number]:
                placement, row = resolve(table, key, choice)
                entries.append(placement)
                rows.append(row)
            entries.sort(key=lambda p: p["object"])
            placements[key] = entries
    overlap = set(placements) & set(UNPLACED)
    if overlap:
        raise BuildError(f"keys both placed and unplaced: {sorted(overlap)}")
    document = {
        "format": "pinmame-vpx-placement-resolution",
        "placements": placements,
        "rejected": rejected_entries(table),
        "source": SOURCE,
        "table_bounds": {"height": HEIGHT, "width": WIDTH},
        "unplaced": unplaced_entries(),
        "version": 1,
    }
    return document, rows


def render(document) -> bytes:
    return (json.dumps(document, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# --------------------------------------------------------------------------------------------------
# World mesh verification and the human report
# --------------------------------------------------------------------------------------------------

def default_world_obj() -> Path | None:
    candidates = []
    root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    suffix = Path("data-east.the-who-s-tommy-pinball-wizard.1994/session-20261009/spatial/export/tommy.obj")
    if root:
        candidates.append(Path(root) / suffix)
    here = Path(__file__).resolve()
    candidates.append(here.parents[3] / "review-artifacts" / suffix)
    candidates.append(here.parents[2] / "pinmame-game-defs-working-dir/review-artifacts" / suffix)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def verify_world_obj(path: Path):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != WORLD_OBJ_SHA256:
        raise BuildError(f"{path} sha256 {digest} differs from the pinned {WORLD_OBJ_SHA256}")
    bounds = {}
    current = None
    for line in data.decode("utf-8").splitlines():
        if line.startswith("o "):
            current = line[2:].strip()
        elif line.startswith("v ") and current in MESH_BOUNDS:
            x, y = (float(v) for v in line.split()[1:3])
            b = bounds.setdefault(current, [x, y, x, y])
            b[0], b[1], b[2], b[3] = min(b[0], x), min(b[1], y), max(b[2], x), max(b[3], y)
    for name, expected in MESH_BOUNDS.items():
        got = bounds.get(name)
        if got is None or any(abs(a - b) > 6e-5 for a, b in zip(got, expected)):
            raise BuildError(f"mesh bounds of {name} differ from the world export: {got} vs {expected}")


def write_report(document, rows, table: Table, path: Path):
    out = ["# The Who's Tommy Pinball Wizard: VPX placement report", ""]
    out.append(f"Generated by `tools/build_tommy_places.py`; source: {SOURCE}.")
    out.append("")
    out.append("Coordinates are raw VPX units (table 952 x 2162) and normalized x = raw_x / 952, y = raw_y / 2162. "
               "`script` lists the first matching `script.vbs` line of each binding pattern.")
    out.append("")
    for heading, prefix in (("Switches", "switch"), ("Lamps", "lamp"), ("Solenoid-driven devices", "solenoid")):
        out.append(f"## {heading}")
        out.append("")
        out.append("| key | object | type | origin | raw | normalized | script lines | why |")
        out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in rows:
            if not row["key"].startswith(prefix + "."):
                continue
            c = row["choice"]
            lines = sorted({ln for found in row["bindings"].values() for ln in found[:1]})
            out.append("| {key} | {obj} | {typ} | {origin} | {rx:.4f}, {ry:.4f} | {x:.6f}, {y:.6f} | {lines} | {why} |".format(
                key=row["key"], obj=c.obj + (f" (+{len(c.doubles) - 1} doubles)" if len(c.doubles) > 1 else ""),
                typ=c.typ, origin=ORIGIN[c.mode], rx=row["raw"][0], ry=row["raw"][1], x=row["norm"][0],
                y=row["norm"][1], lines=", ".join(str(n) for n in lines), why=c.why.replace("|", "/")))
        out.append("")
    out.append("## Collapsed doubles")
    out.append("")
    for row in rows:
        c = row["choice"]
        if len(c.doubles) > 1:
            out.append(f"- {row['key']} `{c.obj}`: " + ", ".join(f"`{d}`" for d in sorted(set(c.doubles))))
    out.append("")
    out.append("## Uncertainties")
    out.append("")
    for note in NOTES:
        out.append(f"- {note}")
    out.append("")
    out.append("## Rejected")
    out.append("")
    for entry in document["rejected"]:
        out.append(f"- {entry['key']} `{entry['object']}`: {entry['reason']}")
    out.append("")
    out.append("## Unplaced")
    out.append("")
    for entry in document["unplaced"]:
        out.append(f"- {entry['key']}: {entry['reason']}")
    out.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\n".join(out)).encode("utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--extracted", required=True, type=Path, help="retained vpxtool extraction directory")
    parser.add_argument("--output", type=Path, help="tommy_places.json to write (or compare with --check)")
    parser.add_argument("--check", action="store_true", help="compare --output with the generated bytes")
    parser.add_argument("--report", type=Path, help="write the human placement report here")
    parser.add_argument("--world-obj", type=Path, help="vpxtool world-space OBJ export to re-derive mesh bounds from")
    args = parser.parse_args(argv)
    try:
        table = Table(args.extracted)
        world = args.world_obj or default_world_obj()
        if world is not None:
            verify_world_obj(world)
        else:
            print("note: world OBJ export not found; embedded mesh bounds were not re-verified", file=sys.stderr)
        document, rows = build(table)
        data = render(document)
        if args.report:
            write_report(document, rows, table, args.report)
        if args.output:
            if args.check:
                current = args.output.read_bytes() if args.output.is_file() else None
                if current != data:
                    print(f"DRIFT: {args.output} differs from the regenerated placements", file=sys.stderr)
                    return 1
                print(f"{args.output} is up to date ({len(document['placements'])} keys)")
            else:
                args.output.write_bytes(data)
                print(f"wrote {args.output} ({len(document['placements'])} keys, "
                      f"{sum(len(v) for v in document['placements'].values())} placements)")
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
