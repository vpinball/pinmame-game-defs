# The Who's Tommy Pinball Wizard

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1994). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

## Playfield devices

Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.

## Custom mechanisms

No custom mechanism conclusion has been validated. Manuals, schematics, PinMAME source, and gameplay evidence still need to be checked.

## Ball-state transitions

Ball paths, trough ordering, locks, kickouts, and causal transitions have not yet been normalized. Relevant source notes follow under Evidence notes.

## Controller interactions

Controller callbacks and bindings are candidate evidence only until reconciled against PinMAME and physical documentation.

## Service and setup information

Unknown; locate operator/service documentation.

## Timing and tuning observations

Source timing values may describe a particular VPX implementation rather than physical hardware and require review.

## Recreation guidance

Do not treat this partial definition as a complete authoring specification. Resolve every coverage requirement and conflict before promotion.

## Evidence notes

- `games/tommy.json#/switches/0._note`: vpmNudge.TiltSwitch=1
- `games/tommy.json#/switches/1._note`: Set via keycode 3 in KeyDown/KeyUp, not a physical playfield switch
- `games/tommy.json#/switches/8._note`: Virtual switch set by SolTrough/SolRelease, no VPX kicker object. sw15.kick used for ball release.
- `games/tommy.json#/switches/10._note`: Pulsed via LeftSlingShot_Slingshot event
- `games/tommy.json#/switches/11._note`: Pulsed via RightSlingShot_Slingshot event
- `games/tommy.json#/switches/21._note`: Set by MirrorTimer when MirrorP.Z >= 137, not a physical VPX switch
- `games/tommy.json#/switches/24._note`: Set by MirrorTimer when MirrorP.Z <= 3, not a physical VPX switch
- `games/tommy.json#/switches/25._note`: Pulsed only if ball speed > 4
- `games/tommy.json#/switches/39._note`: Pulsed via Bumper1_Hit
- `games/tommy.json#/switches/40._note`: Pulsed via Bumper2_Hit
- `games/tommy.json#/switches/41._note`: Pulsed via Bumper3_Hit
- `games/tommy.json#/switches/45._note`: Flipper gate at ramp exit
- `games/tommy.json#/switches/46._note`: Flipper gate at ramp exit
- `games/tommy.json#/coils/0._vbscript_callback`: SolTrough
- `games/tommy.json#/coils/0._inferred_type`: ball_management
- `games/tommy.json#/coils/1._vbscript_callback`: SolRelease
- `games/tommy.json#/coils/1._inferred_type`: ball_management
- `games/tommy.json#/coils/2._vbscript_callback`: AutoLaunch
- `games/tommy.json#/coils/2._inferred_type`: kicker
- `games/tommy.json#/coils/2._note`: Impulse plunger via cvpmImpulseP
- `games/tommy.json#/coils/3._vbscript_callback`: ExitVUK
- `games/tommy.json#/coils/3._inferred_type`: kicker
- `games/tommy.json#/coils/4._vbscript_callback`: ExitScoop
- `games/tommy.json#/coils/4._inferred_type`: kicker
- `games/tommy.json#/coils/5._vbscript_callback`: SolEject
- `games/tommy.json#/coils/5._inferred_type`: kicker
- `games/tommy.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker_1",DOFKnocker),
- `games/tommy.json#/coils/6._inferred_type`: knocker
- `games/tommy.json#/coils/7._inferred_type`: mechanism
- `games/tommy.json#/coils/7._note`: Commented out in VBS: 'SolCallback(9)
- `games/tommy.json#/coils/8._inferred_type`: relay
- `games/tommy.json#/coils/8._note`: Commented out in VBS: 'SolCallback(10)
- `games/tommy.json#/coils/9._vbscript_callback`: GIRelay
- `games/tommy.json#/coils/9._inferred_type`: gi_relay
- `games/tommy.json#/coils/9._note`: Controls Lampz 100 (GI), 101 (GI Cabinet), 102 (Insert intensity). On=GI off, Off=GI on.
- `games/tommy.json#/coils/10._vbscript_callback`: Diverter
- `games/tommy.json#/coils/10._inferred_type`: diverter
- `games/tommy.json#/coils/11._vbscript_callback`: PropellerMove
- `games/tommy.json#/coils/11._inferred_type`: mechanism
- `games/tommy.json#/coils/11._note`: Drives propeller rotation animation
- `games/tommy.json#/coils/12._vbscript_callback`: MirrorMove
- `games/tommy.json#/coils/12._inferred_type`: mechanism
- `games/tommy.json#/coils/12._note`: Raises/lowers mirror, controls sw28 (up) and sw31 (down) position switches
- `games/tommy.json#/coils/13._vbscript_callback`: FlashSol15
- `games/tommy.json#/coils/13._inferred_type`: flasher
- `games/tommy.json#/coils/13._note`: Lampz ID 115. VR backglass flash effect.
- `games/tommy.json#/coils/14._vbscript_callback`: SolBumper1
- `games/tommy.json#/coils/14._inferred_type`: bumper
- `games/tommy.json#/coils/15._vbscript_callback`: SolBumper2
- `games/tommy.json#/coils/15._inferred_type`: bumper
- `games/tommy.json#/coils/16._vbscript_callback`: SolBumper3
- `games/tommy.json#/coils/16._inferred_type`: bumper
- `games/tommy.json#/coils/17._vbscript_callback`: SolLSling
- `games/tommy.json#/coils/17._inferred_type`: slingshot
- `games/tommy.json#/coils/18._vbscript_callback`: SolRSling
- `games/tommy.json#/coils/18._inferred_type`: slingshot
- `games/tommy.json#/coils/19._vbscript_callback`: SolEnableFlips
- `games/tommy.json#/coils/19._inferred_type`: relay
- `games/tommy.json#/coils/19._note`: Enables/disables all flippers via bFlippersEnabled flag
- `games/tommy.json#/coils/20._vbscript_callback`: Setlamp 125,
- `games/tommy.json#/coils/20._inferred_type`: flasher
- `games/tommy.json#/coils/20._note`: Lampz ID 125. Outlane flashers (F25A/B/C/D/L/R).
- `games/tommy.json#/coils/21._vbscript_callback`: Flash26
- `games/tommy.json#/coils/21._inferred_type`: flasher
- `games/tommy.json#/coils/21._note`: Lampz ID 126. Flupper dome flasher 1. Skillshot area.
- `games/tommy.json#/coils/22._vbscript_callback`: Flash27
- `games/tommy.json#/coils/22._inferred_type`: flasher
- `games/tommy.json#/coils/22._note`: Lampz ID 127. Flupper dome flasher 2.
- `games/tommy.json#/coils/23._vbscript_callback`: FlashSol28
- `games/tommy.json#/coils/23._inferred_type`: flasher
- `games/tommy.json#/coils/23._note`: Lampz ID 128. VR backglass flash effect.
- `games/tommy.json#/coils/24._vbscript_callback`: Setlamp 129,
- `games/tommy.json#/coils/24._inferred_type`: flasher
- `games/tommy.json#/coils/24._note`: Lampz ID 129. Bumper area Tommy flasher.
- `games/tommy.json#/coils/25._vbscript_callback`: Flash30
- `games/tommy.json#/coils/25._inferred_type`: flasher
- `games/tommy.json#/coils/25._note`: No Lampz ID. Drives 4 Flupper dome flashers (3-6) for back panel effect.
- `games/tommy.json#/coils/26._vbscript_callback`: FlashSol31
- `games/tommy.json#/coils/26._inferred_type`: flasher
- `games/tommy.json#/coils/26._note`: Lampz ID 131. Captive ball area flasher. VR backglass flash effect.
- `games/tommy.json#/coils/27._vbscript_callback`: Flash32
- `games/tommy.json#/coils/27._inferred_type`: flasher
- `games/tommy.json#/coils/27._note`: Lampz ID 132. Flupper dome flasher 7. Left orbit area.
- `games/tommy.json#/coils/28._vbscript_name`: sLRFlipper
- `games/tommy.json#/coils/28._vbscript_callback`: SolRFlipper
- `games/tommy.json#/coils/28._inferred_type`: flipper
- `games/tommy.json#/coils/29._vbscript_callback`: SolULFlipper
- `games/tommy.json#/coils/29._inferred_type`: flipper
- `games/tommy.json#/coils/29._note`: SolCallback(47) commented out; assigned via vpmFlips.FlipperSolNumber(2)=47
- `games/tommy.json#/coils/30._vbscript_name`: sLLFlipper
- `games/tommy.json#/coils/30._vbscript_callback`: SolLFlipper
- `games/tommy.json#/coils/30._inferred_type`: flipper
- `games/tommy.json#/coils/31._vbscript_callback`: BlinderMove
- `games/tommy.json#/coils/31._inferred_type`: mechanism
- `games/tommy.json#/coils/31._note`: Custom solenoid. Drives blinder animation (BlinderP1/BlinderP2 rotation).
- `games/tommy.json#/lamps/0._note`: Backglass lamp (VR only)
- `games/tommy.json#/lamps/9._note`: Backglass lamp (VR only)
- `games/tommy.json#/lamps/18._note`: Backglass lamp (VR only)
- `games/tommy.json#/lamps/26._note`: Backglass lamp (VR only)
- `games/tommy.json#/lamps/35._note`: Backglass lamp (VR only)
- `games/tommy.json#/lamps/62._note`: Controlled by GI Relay (sol 11). Lampz.obj(100) = GI collection.
- `games/tommy.json#/lamps/63._note`: Controlled by GI Relay (sol 11). Lampz.obj(101) = GICab collection.
- `games/tommy.json#/lamps/64._note`: Callback: InsertIntensityUpdate. Controlled by GI Relay.
- `games/tommy.json#/_source/confidence_notes`: High confidence on switches/coils. 6-ball trough (sw9-sw14) with sw15 as virtual outhole switch managed by SolTrough/SolRelease. Lamp descriptions from Lampz.MassAssign comments in VBS. Flashers on solenoids 15, 25-32 mapped to Lampz IDs 115, 125-132 via Flupper dome system. Mirror motor (sol 14) controls sw28 (mirror up) and sw31 (mirror down) position switches. Blinder motor on sol 51 (custom solenoid). Upper left flipper on sol 47 via vpmFlips.FlipperSolNumber(2)=47, SolCallback commented out. GI relay on sol 11 controls Lampz 100/101/102. Backglass lamps on IDs 1, 10, 19, 28, 37 are VR-only.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.tommy`: `games/tommy.json` at the pinned migration revision.
