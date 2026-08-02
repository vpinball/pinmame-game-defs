# Jokerz!

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1988). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/jokerz.json#/switches/0._note`: Pulsed via vpmTimer.PulseSw 10
- `games/jokerz.json#/switches/4._note`: Labeled 'lanes' in script
- `games/jokerz.json#/switches/5._note`: Ramp position switch — set when ramp is lowered (LowerRamp sub). Not a physical switch object.
- `games/jokerz.json#/switches/6._note`: Ramp position switch — set when ramp is raised (RiseRamp sub). Initialized to 1 in InitCenterRamp.
- `games/jokerz.json#/switches/10._note`: Labeled 'lanes' in script
- `games/jokerz.json#/switches/11._note`: Labeled 'lanes' in script
- `games/jokerz.json#/switches/12._note`: Labeled 'lanes' in script
- `games/jokerz.json#/switches/13._note`: Labeled 'lanes' in script
- `games/jokerz.json#/switches/14._inferred_type`: standup_target
- `games/jokerz.json#/switches/14._note`: Pulsed via vpmTimer.PulseSw 24
- `games/jokerz.json#/switches/15._inferred_type`: drop_target
- `games/jokerz.json#/switches/15._note`: Left bank — reset by solenoid 3 (SolBLDropTgt)
- `games/jokerz.json#/switches/16._inferred_type`: drop_target
- `games/jokerz.json#/switches/16._note`: Left bank — reset by solenoid 3 (SolBLDropTgt)
- `games/jokerz.json#/switches/17._inferred_type`: drop_target
- `games/jokerz.json#/switches/17._note`: Left bank — reset by solenoid 3 (SolBLDropTgt)
- `games/jokerz.json#/switches/23._inferred_type`: drop_target
- `games/jokerz.json#/switches/23._note`: Right bank — reset by solenoid 4 (SolBRDropTgt)
- `games/jokerz.json#/switches/24._inferred_type`: drop_target
- `games/jokerz.json#/switches/24._note`: Right bank — reset by solenoid 4 (SolBRDropTgt)
- `games/jokerz.json#/switches/25._inferred_type`: drop_target
- `games/jokerz.json#/switches/25._note`: Right bank — reset by solenoid 4 (SolBRDropTgt)
- `games/jokerz.json#/switches/26._inferred_type`: drop_target
- `games/jokerz.json#/switches/26._note`: Top bank — reset by solenoid 6 (SolTLDropTgt)
- `games/jokerz.json#/switches/27._inferred_type`: drop_target
- `games/jokerz.json#/switches/27._note`: Top bank — reset by solenoid 6 (SolTLDropTgt)
- `games/jokerz.json#/switches/28._inferred_type`: drop_target
- `games/jokerz.json#/switches/28._note`: Top bank — reset by solenoid 6 (SolTLDropTgt)
- `games/jokerz.json#/switches/29._inferred_type`: kicker
- `games/jokerz.json#/switches/29._note`: Two-stage kicker — ball enters sw45 first, then sw46 is enabled
- `games/jokerz.json#/switches/30._inferred_type`: kicker
- `games/jokerz.json#/switches/30._note`: Kicked by solenoid 7 (SolBLKicker). Both sw45 and sw46 cleared on kick.
- `games/jokerz.json#/switches/31._inferred_type`: kicker
- `games/jokerz.json#/switches/31._note`: Kicked by solenoid 16 (bsREject). Ball lock saucer.
- `games/jokerz.json#/switches/32._inferred_type`: spinner
- `games/jokerz.json#/switches/32._note`: Pulsed via sw48_Spin
- `games/jokerz.json#/switches/33._note`: Ramp switch with physical primitive animation (sw49p)
- `games/jokerz.json#/switches/34._note`: Ramp switch with physical primitive animation (sw50p)
- `games/jokerz.json#/switches/35._inferred_type`: standup_target
- `games/jokerz.json#/switches/35._note`: Pulsed via vpmTimer.PulseSw 52
- `games/jokerz.json#/switches/36._note`: Pulsed via vpmTimer.PulseSw 53
- `games/jokerz.json#/switches/37._note`: Pulsed via vpmTimer.PulseSw 56
- `games/jokerz.json#/switches/38._inferred_type`: bumper
- `games/jokerz.json#/switches/38._note`: Pulsed via vpmTimer.PulseSw(60)
- `games/jokerz.json#/switches/39._inferred_type`: bumper
- `games/jokerz.json#/switches/39._note`: Pulsed via vpmTimer.PulseSw(61)
- `games/jokerz.json#/switches/40._inferred_type`: bumper
- `games/jokerz.json#/switches/40._note`: Pulsed via vpmTimer.PulseSw(62)
- `games/jokerz.json#/switches/41._inferred_type`: slingshot
- `games/jokerz.json#/switches/41._note`: Pulsed via vpmTimer.PulseSw(63)
- `games/jokerz.json#/switches/42._inferred_type`: slingshot
- `games/jokerz.json#/switches/42._note`: Pulsed via vpmTimer.PulseSw(64)
- `games/jokerz.json#/switches/43._note`: vpmNudge.TiltSwitch = swTilt (swTilt=67 from S11.VBS framework)
- `games/jokerz.json#/coils/0._vbscript_callback`: SolRelease
- `games/jokerz.json#/coils/0._inferred_type`: ball_management
- `games/jokerz.json#/coils/0._note`: Kicks ball from sw11 (front trough position)
- `games/jokerz.json#/coils/1._vbscript_callback`: SolBLDropTgt
- `games/jokerz.json#/coils/1._inferred_type`: drop_target_reset
- `games/jokerz.json#/coils/1._note`: Raises drop targets sw25, sw26, sw27
- `games/jokerz.json#/coils/2._vbscript_callback`: SolBRDropTgt
- `games/jokerz.json#/coils/2._inferred_type`: drop_target_reset
- `games/jokerz.json#/coils/2._note`: Raises drop targets sw36, sw37, sw38
- `games/jokerz.json#/coils/3._vbscript_callback`: bsLEject.SolOut
- `games/jokerz.json#/coils/3._inferred_type`: kicker
- `games/jokerz.json#/coils/4._vbscript_callback`: SolTLDropTgt
- `games/jokerz.json#/coils/4._inferred_type`: drop_target_reset
- `games/jokerz.json#/coils/4._note`: Raises drop targets sw41, sw42, sw43
- `games/jokerz.json#/coils/5._vbscript_callback`: SolBLKicker
- `games/jokerz.json#/coils/5._inferred_type`: kicker
- `games/jokerz.json#/coils/5._note`: Kicks from sw46, clears both sw45 and sw46
- `games/jokerz.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker_1",DOFKnocker),
- `games/jokerz.json#/coils/6._inferred_type`: knocker
- `games/jokerz.json#/coils/7._vbscript_callback`: FlashSol109
- `games/jokerz.json#/coils/7._inferred_type`: flasher
- `games/jokerz.json#/coils/7._note`: Controls two flasher objects via Lampz indices. F09 central ramp flasher.
- `games/jokerz.json#/coils/8._vbscript_callback`: SolGi
- `games/jokerz.json#/coils/8._inferred_type`: gi_relay
- `games/jokerz.json#/coils/8._note`: Inverted logic: Enabled=GI off, Disabled=GI on. Controls Lampz.state(0) and backglass brightness.
- `games/jokerz.json#/coils/9._vbscript_callback`: FlashSol111 / SetLamp 111,
- `games/jokerz.json#/coils/9._inferred_type`: flasher
- `games/jokerz.json#/coils/9._note`: Desktop mode uses SetLamp 111; VR mode uses FlashSol111. Controls card wheel backbox flasher.
- `games/jokerz.json#/coils/10._vbscript_callback`: SolRamp
- `games/jokerz.json#/coils/10._inferred_type`: motor
- `games/jokerz.json#/coils/10._note`: Drives center ramp up/down via RampTimer. Position tracked by switches 15/16.
- `games/jokerz.json#/coils/11._vbscript_callback`: bsREject
- `games/jokerz.json#/coils/11._inferred_type`: kicker
- `games/jokerz.json#/coils/11._note`: Kicks ball from sw47 (right saucer/lock)
- `games/jokerz.json#/coils/12._vbscript_callback`: SetLamp 122,
- `games/jokerz.json#/coils/12._inferred_type`: flasher
- `games/jokerz.json#/coils/12._note`: Controls Lampz index 122 (f122a, f122b) and drawbridge flash primitive
- `games/jokerz.json#/coils/13._vbscript_callback`: Flashsol125
- `games/jokerz.json#/coils/13._inferred_type`: flasher
- `games/jokerz.json#/coils/13._note`: Back wall JOKERZ! letter flasher — JO
- `games/jokerz.json#/coils/14._vbscript_callback`: Flashsol126
- `games/jokerz.json#/coils/14._inferred_type`: flasher
- `games/jokerz.json#/coils/14._note`: Back wall JOKERZ! letter flasher — KE
- `games/jokerz.json#/coils/15._vbscript_callback`: Flashsol127
- `games/jokerz.json#/coils/15._inferred_type`: flasher
- `games/jokerz.json#/coils/15._note`: Back wall JOKERZ! letter flasher — RZ
- `games/jokerz.json#/coils/16._vbscript_callback`: Flashsol128
- `games/jokerz.json#/coils/16._inferred_type`: flasher
- `games/jokerz.json#/coils/16._note`: Back wall JOKERZ! letter flasher — !
- `games/jokerz.json#/coils/17._vbscript_callback`: FlashSol129
- `games/jokerz.json#/coils/17._inferred_type`: flasher
- `games/jokerz.json#/coils/17._note`: F29 — VR-only flasher effect
- `games/jokerz.json#/coils/18._vbscript_callback`: FlashSol130
- `games/jokerz.json#/coils/18._inferred_type`: flasher
- `games/jokerz.json#/coils/18._note`: Flupper dome flasher
- `games/jokerz.json#/coils/19._vbscript_callback`: FlashSol131
- `games/jokerz.json#/coils/19._inferred_type`: flasher
- `games/jokerz.json#/coils/19._note`: Flupper dome flasher
- `games/jokerz.json#/coils/20._vbscript_callback`: FlashSol132
- `games/jokerz.json#/coils/20._inferred_type`: flasher
- `games/jokerz.json#/coils/20._note`: Flupper dome flasher
- `games/jokerz.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/jokerz.json#/coils/21._inferred_type`: flipper
- `games/jokerz.json#/coils/21._note`: sLRFlipper=46 from core.vbs
- `games/jokerz.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/jokerz.json#/coils/22._inferred_type`: flipper
- `games/jokerz.json#/coils/22._note`: sLLFlipper=48 from core.vbs
- `games/jokerz.json#/lamps/0._note`: Non-matrix. Controlled by solenoid 10 (SolGi). Lampz.obj(0) = GI collection. Inverted logic.
- `games/jokerz.json#/lamps/57._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/58._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/59._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/60._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/61._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/62._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/63._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/64._note`: Desktop-only (no callback)
- `games/jokerz.json#/lamps/65._note`: Solenoid-driven flasher (sol 11). Lampz index 111.
- `games/jokerz.json#/lamps/66._note`: Solenoid-driven flasher (sol 22). Lampz index 122. Also f122b.
- `games/jokerz.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and sw*_Hit handlers. Uses S11.VBS (System 11). Manual trough implementation (sw11/12/13 with UpdateTrough cascade, not cvpmTrough). Drain is sw10 (pulsed). Ball release is solenoid 2 (kicks from sw11). Solenoid 10 is GI relay (inverted logic in SolGi — enabled=off, disabled=on). Ramp motor solenoid 15 drives center ramp up/down with position switches 15/16. Card wheel mechanism uses cvpmMyMech. Flipper solenoid numbers (sLRFlipper=46, sLLFlipper=48) come from core.vbs S11 constants. swTilt=67 from S11.VBS framework. Flasher solenoids (9,11,22,25-32) use Lampz indices 109-132 for lamp state. Lamp indices 1-64 from Lampz.MassAssign. Lamp 0 is GI (non-matrix, solenoid-driven via sol 10).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.jokerz`: `games/jokerz.json` at the pinned migration revision.
