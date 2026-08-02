# GoldenEye

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Sega (1996). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/goldeneye.json#/switches/0._note`: vpmNudge.TiltSwitch=1
- `games/goldeneye.json#/switches/1._note`: Controller.Switch(3) toggled in KeyDown/KeyUp via StartGameKey
- `games/goldeneye.json#/switches/2._note`: Controller.Switch(7) toggled in KeyDown/KeyUp via KeySlamDoorHit
- `games/goldeneye.json#/switches/3._note`: Controller.Switch(9) toggled in KeyDown/KeyUp via PlungerKey
- `games/goldeneye.json#/switches/4._note`: bsTrough.InitSw 0,14,13,12,11,10 — position 5 (leftmost in trough)
- `games/goldeneye.json#/switches/5._note`: bsTrough.InitSw position 4
- `games/goldeneye.json#/switches/6._note`: bsTrough.InitSw position 3
- `games/goldeneye.json#/switches/7._note`: bsTrough.InitSw position 2
- `games/goldeneye.json#/switches/8._note`: bsTrough.InitSw position 1 (rightmost, first filled)
- `games/goldeneye.json#/switches/9._note`: Pulsed by SolLockOut (sol 17): vpmTimer.PulseSw 15
- `games/goldeneye.json#/switches/10._note`: bsPlunger.InitSaucer Plunger,16 — ball in shooter lane
- `games/goldeneye.json#/switches/11._note`: GateSw17_Hit: vpmTimer.PulseSw 17
- `games/goldeneye.json#/switches/12._note`: GateSw18_Hit: vpmTimer.PulseSw 18
- `games/goldeneye.json#/switches/13._note`: GateSw19_Hit: vpmTimer.PulseSw 19
- `games/goldeneye.json#/switches/14._note`: Controller.Switch(20) cleared by SolSatMotorRelay(false)
- `games/goldeneye.json#/switches/15._note`: Controller.Switch(23) set in RadarKicker_hit, cleared by SolRadarMagnet(false) and SolSatMotorRelay(false)
- `games/goldeneye.json#/switches/16._note`: vpmTimer.PulseSw 24 in HideFlipper_Timer (ball released from flipper magnet)
- `games/goldeneye.json#/switches/17._note`: SS25_hit: vpmTimer.PulseSw 25
- `games/goldeneye.json#/switches/18._note`: SS26_hit: vpmTimer.PulseSw 26
- `games/goldeneye.json#/switches/19._note`: SS27_hit: vpmTimer.PulseSw 27
- `games/goldeneye.json#/switches/20._note`: SS28_hit: vpmTimer.PulseSw 28
- `games/goldeneye.json#/switches/21._note`: SS30_hit: vpmTimer.PulseSw 30
- `games/goldeneye.json#/switches/22._note`: SS31_hit: vpmTimer.PulseSw 31
- `games/goldeneye.json#/switches/23._note`: GateSw32_Hit: vpmTimer.PulseSw 32
- `games/goldeneye.json#/switches/24._note`: SS33_hit: vpmTimer.PulseSw 33
- `games/goldeneye.json#/switches/25._note`: SS34_hit: vpmTimer.PulseSw 34
- `games/goldeneye.json#/switches/26._note`: SS39_hit: vpmTimer.PulseSw 39
- `games/goldeneye.json#/switches/27._note`: GateSw40_Hit: vpmTimer.PulseSw 40
- `games/goldeneye.json#/switches/28._note`: LeftTurboBumper_Hit: vpmTimer.PulseSw 41
- `games/goldeneye.json#/switches/29._note`: BottomTurboBumper_Hit: vpmTimer.PulseSw 42
- `games/goldeneye.json#/switches/30._note`: RightTurboBumper_Hit: vpmTimer.PulseSw 43
- `games/goldeneye.json#/switches/31._note`: SS44_hit: vpmTimer.PulseSw 44
- `games/goldeneye.json#/switches/32._note`: SS45_hit: vpmTimer.PulseSw 45
- `games/goldeneye.json#/switches/33._note`: SS46_hit: vpmTimer.PulseSw 46
- `games/goldeneye.json#/switches/34._note`: SS47_hit: vpmTimer.PulseSw 47
- `games/goldeneye.json#/switches/35._note`: SS48_hit: vpmTimer.PulseSw 48
- `games/goldeneye.json#/switches/36._note`: sw49_Hit/UnHit: Controller.Switch(49)
- `games/goldeneye.json#/switches/37._note`: bsScoop.InitSw 0,50 — Mode Start scoop kicker
- `games/goldeneye.json#/switches/38._note`: sw51_Hit/UnHit: Controller.Switch(51)
- `games/goldeneye.json#/switches/39._note`: sw52_Hit/UnHit: Controller.Switch(52)
- `games/goldeneye.json#/switches/40._note`: sw53_Hit/UnHit: Controller.Switch(53)
- `games/goldeneye.json#/switches/41._note`: GateSw54_Hit: vpmTimer.PulseSw 54
- `games/goldeneye.json#/switches/42._note`: sw55_Hit/UnHit: Controller.Switch(55)
- `games/goldeneye.json#/switches/43._note`: bsTank.InitSw 0,56 — ball in tank
- `games/goldeneye.json#/switches/44._note`: sw57_Hit/UnHit: Controller.Switch(57)
- `games/goldeneye.json#/switches/45._note`: sw58_Hit/UnHit: Controller.Switch(58)
- `games/goldeneye.json#/switches/46._note`: sw59_Hit/UnHit: Controller.Switch(59)
- `games/goldeneye.json#/switches/47._note`: sw60_Hit/UnHit: Controller.Switch(60)
- `games/goldeneye.json#/switches/48._note`: LeftSlingShot_Slingshot: vpmTimer.PulseSw 61
- `games/goldeneye.json#/switches/49._note`: RightSlingShot_Slingshot: vpmTimer.PulseSw 62
- `games/goldeneye.json#/switches/50._note`: Controller.Switch(63) toggled in SolLFlipper
- `games/goldeneye.json#/switches/51._note`: Controller.Switch(64) toggled in SolRFlipper
- `games/goldeneye.json#/coils/0._vbscript_callback`: bsTrough.SolOut
- `games/goldeneye.json#/coils/0._inferred_type`: ball_management
- `games/goldeneye.json#/coils/1._vbscript_callback`: bsPlunger.SolOut
- `games/goldeneye.json#/coils/1._inferred_type`: ball_management
- `games/goldeneye.json#/coils/2._vbscript_callback`: bsScoop.SolOut
- `games/goldeneye.json#/coils/2._inferred_type`: kicker
- `games/goldeneye.json#/coils/3._vbscript_callback`: vpmSolSound SoundFX("knocker_1",DOFKnocker),
- `games/goldeneye.json#/coils/3._inferred_type`: knocker
- `games/goldeneye.json#/coils/4._vbscript_callback`: bsTank.SolOut
- `games/goldeneye.json#/coils/4._inferred_type`: ball_management
- `games/goldeneye.json#/coils/5._vbscript_callback`: SolLockOut
- `games/goldeneye.json#/coils/5._inferred_type`: kicker
- `games/goldeneye.json#/coils/5._note`: Pulses switch 15 when enabled
- `games/goldeneye.json#/coils/6._vbscript_callback`: SolUpDownRamp
- `games/goldeneye.json#/coils/6._inferred_type`: mechanism
- `games/goldeneye.json#/coils/6._note`: Raises/lowers the moving ramp (Ramp005, Mramp collidable toggles)
- `games/goldeneye.json#/coils/7._vbscript_callback`: SolSatLaunchRamp
- `games/goldeneye.json#/coils/7._inferred_type`: mechanism
- `games/goldeneye.json#/coils/7._note`: Raises pop-up ramp in front of satellite dish
- `games/goldeneye.json#/coils/8._vbscript_callback`: SolSatMotorRelay
- `games/goldeneye.json#/coils/8._inferred_type`: mechanism
- `games/goldeneye.json#/coils/8._note`: Rotates the satellite dish via RotRadar timer
- `games/goldeneye.json#/coils/9._vbscript_callback`: DropRamp1.Enabled=
- `games/goldeneye.json#/coils/9._inferred_type`: mechanism
- `games/goldeneye.json#/coils/9._note`: Enables/disables DropRamp1 collidable state
- `games/goldeneye.json#/coils/10._vbscript_callback`: Sol25
- `games/goldeneye.json#/coils/10._inferred_type`: flasher
- `games/goldeneye.json#/coils/10._note`: Fading flasher. Controls Flash001, Flash002, Flasha001/Flasha001B
- `games/goldeneye.json#/coils/11._vbscript_callback`: Sol26
- `games/goldeneye.json#/coils/11._inferred_type`: flasher
- `games/goldeneye.json#/coils/11._note`: Fading flasher. Controls Flasha003, LL15/LL15F/LLb015
- `games/goldeneye.json#/coils/12._vbscript_callback`: Sol27
- `games/goldeneye.json#/coils/12._inferred_type`: flasher
- `games/goldeneye.json#/coils/12._note`: Fading flasher. Controls Flash003A, Flash003B, Flasha002
- `games/goldeneye.json#/coils/13._vbscript_callback`: Sol28
- `games/goldeneye.json#/coils/13._inferred_type`: flasher
- `games/goldeneye.json#/coils/13._note`: Fading flasher. Controls Flash004, Flasha0004
- `games/goldeneye.json#/coils/14._vbscript_callback`: Sol29
- `games/goldeneye.json#/coils/14._inferred_type`: flasher
- `games/goldeneye.json#/coils/14._note`: Calls Flash1 — controls Flasherbase1 via FlupperDome system
- `games/goldeneye.json#/coils/15._vbscript_callback`: sol30
- `games/goldeneye.json#/coils/15._inferred_type`: flasher
- `games/goldeneye.json#/coils/15._note`: Fading flasher. Controls Rampflash4, Flash003
- `games/goldeneye.json#/coils/16._vbscript_callback`: Sol31
- `games/goldeneye.json#/coils/16._inferred_type`: flasher
- `games/goldeneye.json#/coils/16._note`: Calls Flash3 + Flash2 — controls Flasherbase3, Flasherbase2 via FlupperDome system
- `games/goldeneye.json#/coils/17._vbscript_callback`: Sol32
- `games/goldeneye.json#/coils/17._inferred_type`: flasher
- `games/goldeneye.json#/coils/17._note`: Calls Flash4 — controls Flasherbase4 via FlupperDome system
- `games/goldeneye.json#/coils/18._vbscript_callback`: SolRadarMagnet
- `games/goldeneye.json#/coils/18._inferred_type`: magnet
- `games/goldeneye.json#/coils/18._note`: Satellite dish magnet. Holds ball in radar lock, clears sw23 on release
- `games/goldeneye.json#/coils/19._vbscript_callback`: SolFlipperMagnet
- `games/goldeneye.json#/coils/19._inferred_type`: magnet
- `games/goldeneye.json#/coils/19._note`: Ball saver magnet near flippers (cvpmMagnet). Pulses sw24 on release
- `games/goldeneye.json#/coils/20._vbscript_callback`: TiltMod
- `games/goldeneye.json#/coils/20._inferred_type`: tilt
- `games/goldeneye.json#/coils/21._vbscript_name`: sLRFlipper
- `games/goldeneye.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/goldeneye.json#/coils/21._inferred_type`: flipper
- `games/goldeneye.json#/coils/21._note`: Framework-defined constant (core.vbs: sLRFlipper=46). Toggles Controller.Switch(64)
- `games/goldeneye.json#/coils/22._vbscript_name`: sLLFlipper
- `games/goldeneye.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/goldeneye.json#/coils/22._inferred_type`: flipper
- `games/goldeneye.json#/coils/22._note`: Framework-defined constant (core.vbs: sLLFlipper=48). Toggles Controller.Switch(63)
- `games/goldeneye.json#/lamps/0._note`: Lampz.obj(0) = GI collection. Callback: GIUpdates. Controls playfield GI fading
- `games/goldeneye.json#/lamps/14._note`: Also LL15F. Sol26 flasher directly modulates LL15/LL15F/LLb015 intensity
- `games/goldeneye.json#/lamps/18._note`: Also LL19A, LL19B — bumper lamp with multiple VPX objects
- `games/goldeneye.json#/lamps/26._note`: Also LL27A, LL27B — bumper lamp with multiple VPX objects
- `games/goldeneye.json#/lamps/33._note`: Callback: DisableLighting GreenLight primitive
- `games/goldeneye.json#/lamps/39._note`: Also LL41A, LL41B — bumper lamp with multiple VPX objects
- `games/goldeneye.json#/lamps/47._note`: ll49.state controls helicopter rotor animation via Rotor_timer
- `games/goldeneye.json#/lamps/48._note`: Callback: DisableLighting RedLightA primitive
- `games/goldeneye.json#/lamps/49._note`: Callback: DisableLighting RedLightB primitive
- `games/goldeneye.json#/lamps/55._note`: Also LL58bis — two VPX objects
- `games/goldeneye.json#/lamps/65._note`: Callback: DisableLighting spotlightLight primitive
- `games/goldeneye.json#/_source/confidence_notes`: High confidence. Extracted from VPW 1.0 release VBS. Uses SEGA2.VBS framework (Whitestar gen 1). No Const sw* declarations in table script; switches identified from Controller.Switch() calls, vpmTimer.PulseSw calls, and cvpmBallStack.InitSw parameters. Lampz (nFozzy) system with MassAssign for lamps 0-69 plus desktop backglass 72-80. Flasher solenoids 25-32 use fading timers. sLRFlipper=46 and sLLFlipper=48 are framework-defined constants from core.vbs.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.goldeneye`: `games/goldeneye.json` at the pinned migration revision.
