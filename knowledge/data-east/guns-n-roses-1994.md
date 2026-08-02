# Guns N' Roses

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

- `games/gnr.json#/switches/0._note`: vpmNudge.TiltSwitch=1
- `games/gnr.json#/switches/7._note`: Virtual switch — set by SolTrough(1)/SolRelease(0), no physical VPX kicker object
- `games/gnr.json#/switches/44._note`: Pulsed via PlungerKey (vpmTimer.PulseSw 62), not a physical VPX kicker
- `games/gnr.json#/coils/0._vbscript_callback`: SolTrough
- `games/gnr.json#/coils/0._inferred_type`: ball_management
- `games/gnr.json#/coils/1._vbscript_callback`: SolRelease
- `games/gnr.json#/coils/1._inferred_type`: ball_management
- `games/gnr.json#/coils/2._vbscript_callback`: SolAutofire
- `games/gnr.json#/coils/2._inferred_type`: kicker
- `games/gnr.json#/coils/2._note`: Impulse plunger via cvpmImpulseP, power=65, time=0.6
- `games/gnr.json#/coils/3._vbscript_callback`: KickerUpperLeft
- `games/gnr.json#/coils/3._inferred_type`: kicker
- `games/gnr.json#/coils/4._vbscript_callback`: KickerUpperRight
- `games/gnr.json#/coils/4._inferred_type`: kicker
- `games/gnr.json#/coils/5._vbscript_callback`: ScoopKicker
- `games/gnr.json#/coils/5._inferred_type`: kicker
- `games/gnr.json#/coils/6._vbscript_callback`: SolTrapDoor
- `games/gnr.json#/coils/6._inferred_type`: mechanism
- `games/gnr.json#/coils/6._note`: Controls SnakeTrapDoor wall and TrapFlipper
- `games/gnr.json#/coils/7._vbscript_callback`: vpmSolSound SoundFX("knocker",DOFKnocker),
- `games/gnr.json#/coils/7._inferred_type`: knocker
- `games/gnr.json#/coils/8._vbscript_callback`: ResetDropsR
- `games/gnr.json#/coils/8._inferred_type`: drop_target_reset
- `games/gnr.json#/coils/8._note`: Resets sw35, sw36, sw57
- `games/gnr.json#/coils/9._vbscript_callback`: K1Relay
- `games/gnr.json#/coils/9._inferred_type`: relay
- `games/gnr.json#/coils/9._note`: DE solenoid mux relay — SSF sound only in VBS
- `games/gnr.json#/coils/10._vbscript_callback`: GIRelay
- `games/gnr.json#/coils/10._inferred_type`: gi_relay
- `games/gnr.json#/coils/10._note`: SolModCallback — PWM controls GI lights l141, l141b-l141l, lgi
- `games/gnr.json#/coils/11._vbscript_callback`: ResetDropsL
- `games/gnr.json#/coils/11._inferred_type`: drop_target_reset
- `games/gnr.json#/coils/11._note`: Resets sw33, sw34, sw59
- `games/gnr.json#/coils/12._vbscript_callback`: SolKickBack
- `games/gnr.json#/coils/12._inferred_type`: kicker
- `games/gnr.json#/coils/13._vbscript_callback`: FlashPWM 1, f01, BL_Flashers_f1,
- `games/gnr.json#/coils/13._inferred_type`: flasher
- `games/gnr.json#/coils/13._note`: SolModCallback — DE relay-switched flasher
- `games/gnr.json#/coils/14._vbscript_callback`: FlashPWM 2, f02, BL_Flashers_f2,
- `games/gnr.json#/coils/14._inferred_type`: flasher
- `games/gnr.json#/coils/15._vbscript_callback`: FlashPWM 3, f03, BL_Flashers_f3,
- `games/gnr.json#/coils/15._inferred_type`: flasher
- `games/gnr.json#/coils/16._vbscript_callback`: FlashPWM 4, f04, BL_Flashers_f4,
- `games/gnr.json#/coils/16._inferred_type`: flasher
- `games/gnr.json#/coils/17._vbscript_callback`: FlashPWM 5, f05, BL_Flashers_f5,
- `games/gnr.json#/coils/17._inferred_type`: flasher
- `games/gnr.json#/coils/18._vbscript_callback`: FlashPWM 6, f06, BL_Flashers_f6,
- `games/gnr.json#/coils/18._inferred_type`: flasher
- `games/gnr.json#/coils/19._vbscript_callback`: FlashPWM 7, f07, BL_Flashers_f7,
- `games/gnr.json#/coils/19._inferred_type`: flasher
- `games/gnr.json#/coils/20._vbscript_callback`: FlashPWM 8, f08, BL_Flashers_f8,
- `games/gnr.json#/coils/20._inferred_type`: flasher
- `games/gnr.json#/coils/21._vbscript_name`: sLRFlipper
- `games/gnr.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/gnr.json#/coils/21._inferred_type`: flipper
- `games/gnr.json#/coils/22._vbscript_name`: sLLFlipper
- `games/gnr.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/gnr.json#/coils/22._inferred_type`: flipper
- `games/gnr.json#/coils/23._vbscript_name`: sULFlipper
- `games/gnr.json#/coils/23._vbscript_callback`: SolULFlipper
- `games/gnr.json#/coils/23._inferred_type`: flipper
- `games/gnr.json#/coils/24._inferred_type`: magnet
- `games/gnr.json#/coils/24._note`: cvpmMagnet, solenoid=51, radius=16
- `games/gnr.json#/coils/25._inferred_type`: magnet
- `games/gnr.json#/coils/25._note`: cvpmMagnet, solenoid=52, radius=16
- `games/gnr.json#/coils/26._inferred_type`: magnet
- `games/gnr.json#/coils/26._note`: cvpmMagnet, solenoid=53, radius=16
- `games/gnr.json#/_source/confidence_notes`: High confidence on switches/coils — extracted directly from VPW 1.2 VBScript. Trough is 6-ball (sw9-sw14) with virtual sw15 for shooter lane staging. Switch descriptions from VBS comments and game context. Lamps l1-l62 confirmed via VLM lightmapper BL_Inserts arrays. GI lights (l140a-f, l141/l141a-l) controlled by SolModCallback(11) GI relay. Flashers (f01-f08) controlled by SolModCallback(25-32) via DE A/B relay. Magnets use cvpmMagnet custom solenoids 51-53. Flipper solenoids use DE framework constants sLRFlipper=46, sLLFlipper=48, sULFlipper=36.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.gnr`: `games/gnr.json` at the pinned migration revision.
