# Spectrum

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1981). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/bally.json#/coils/1`: Unbound legacy outputs record `c_flipper_lower_right` was retained as a migration note only.
- `platforms/bally.json#/coils/2`: Unbound legacy outputs record `c_flipper_lower_left` was retained as a migration note only.
- `platforms/bally.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/bally.json#/coils/4`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/spectrum.json#/switches/0._note`: Controller.Switch(1) set via RightFlipperKey in Table1_KeyDown/KeyUp
- `games/spectrum.json#/switches/1._note`: Controller.Switch(2) set via LeftFlipperKey in Table1_KeyDown/KeyUp
- `games/spectrum.json#/switches/2._note`: Controller.Switch(7) on/off. Dual-direction kick: sol 1 kicks left, sol 2 kicks right.
- `games/spectrum.json#/switches/3._note`: bsD cvpmBallStack. InitSaucer Drain, 8. Single ball drain — early Bally has no multi-switch trough.
- `games/spectrum.json#/switches/4._note`: vpmNudge.TiltSwitch = 15
- `games/spectrum.json#/switches/5._note`: Controller.Switch(17) on/off. Dual-direction kick: sol 3 kicks left, sol 4 kicks right (inferred from sub pairing).
- `games/spectrum.json#/switches/6._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/7._note`: Controller.Switch on/off. Multiple VPX objects: sw19, sw19a, sw19b
- `games/spectrum.json#/switches/8._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/9._note`: Controller.Switch on/off. Multiple VPX objects: sw21, sw21a, sw21b
- `games/spectrum.json#/switches/10._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/11._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/12._note`: Controller.Switch(24) on/off. Dual-direction kick similar to sw7/sw17.
- `games/spectrum.json#/switches/13._note`: Controller.Switch on/off. Multiple VPX objects: sw25a, sw25b, sw25c — all map to switch 25
- `games/spectrum.json#/switches/14._note`: vpmTimer.PulseSw 26
- `games/spectrum.json#/switches/15._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/16._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/17._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/18._note`: Controller.Switch on/off
- `games/spectrum.json#/switches/19._note`: vpmTimer.PulseSw 31
- `games/spectrum.json#/switches/20._note`: Controller.Switch on/off. Multiple VPX objects: sw32a, sw32b, sw32c — all map to switch 32
- `games/spectrum.json#/switches/21._note`: Controller.Switch on/off. Multiple VPX objects: sw33, sw33a
- `games/spectrum.json#/switches/22._note`: DTHit 34. Reset by sol 11 (DT_G_Reset).
- `games/spectrum.json#/switches/23._note`: DTHit 35. Reset by sol 11 (DT_G_Reset).
- `games/spectrum.json#/switches/24._note`: DTHit 36. Reset by sol 11 (DT_G_Reset).
- `games/spectrum.json#/switches/25._note`: DTHit 37. Reset by sol 12 (DT_Y_Reset).
- `games/spectrum.json#/switches/26._note`: DTHit 38. Reset by sol 12 (DT_Y_Reset).
- `games/spectrum.json#/switches/27._note`: DTHit 39. Reset by sol 12 (DT_Y_Reset).
- `games/spectrum.json#/switches/28._note`: Controller.Switch on/off. Multiple VPX objects: sw40, sw40a
- `games/spectrum.json#/switches/29._note`: Controller.Switch(41) on/off. Dual-direction kick similar to sw7/sw17.
- `games/spectrum.json#/switches/30._note`: DTHit 42. Reset by sol 10 (DT_B_Reset).
- `games/spectrum.json#/switches/31._note`: DTHit 43. Reset by sol 10 (DT_B_Reset).
- `games/spectrum.json#/switches/32._note`: DTHit 44. Reset by sol 10 (DT_B_Reset).
- `games/spectrum.json#/switches/33._note`: DTHit 45. Reset by sol 13 (DT_R_Reset).
- `games/spectrum.json#/switches/34._note`: DTHit 46. Reset by sol 13 (DT_R_Reset).
- `games/spectrum.json#/switches/35._note`: DTHit 47. Reset by sol 13 (DT_R_Reset).
- `games/spectrum.json#/switches/36._note`: Controller.Switch(48) on/off. Dual-direction kick similar to sw7/sw17.
- `games/spectrum.json#/coils/0._vbscript_callback`: kicker_topleft
- `games/spectrum.json#/coils/0._inferred_type`: ball_management
- `games/spectrum.json#/coils/0._note`: Kicks ball from sw7 saucer to the left (angle 290)
- `games/spectrum.json#/coils/1._vbscript_callback`: kicker_topright
- `games/spectrum.json#/coils/1._inferred_type`: ball_management
- `games/spectrum.json#/coils/1._note`: Kicks ball from sw7 saucer to the right (angle 70)
- `games/spectrum.json#/coils/2._vbscript_callback`: kicker_midleft
- `games/spectrum.json#/coils/2._inferred_type`: ball_management
- `games/spectrum.json#/coils/2._note`: Kicks ball from sw41 saucer
- `games/spectrum.json#/coils/3._vbscript_callback`: kicker_midright
- `games/spectrum.json#/coils/3._inferred_type`: ball_management
- `games/spectrum.json#/coils/3._note`: Kicks ball from sw48 saucer
- `games/spectrum.json#/coils/4._vbscript_callback`: DrainSolOut
- `games/spectrum.json#/coils/4._inferred_type`: ball_management
- `games/spectrum.json#/coils/4._note`: bsD.SolOut — ejects ball from drain (cvpmBallStack)
- `games/spectrum.json#/coils/5._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/spectrum.json#/coils/5._inferred_type`: knocker
- `games/spectrum.json#/coils/5._note`: Sound-only callback in VPX — physical knocker coil
- `games/spectrum.json#/coils/6._vbscript_callback`: kicker_botleft
- `games/spectrum.json#/coils/6._inferred_type`: ball_management
- `games/spectrum.json#/coils/6._note`: Kicks ball from sw17 saucer
- `games/spectrum.json#/coils/7._vbscript_callback`: kicker_botright
- `games/spectrum.json#/coils/7._inferred_type`: ball_management
- `games/spectrum.json#/coils/7._note`: Kicks ball from sw24 saucer
- `games/spectrum.json#/coils/8._vbscript_callback`: DT_B_Reset
- `games/spectrum.json#/coils/8._inferred_type`: drop_target_reset
- `games/spectrum.json#/coils/8._note`: Resets drop targets sw42, sw43, sw44
- `games/spectrum.json#/coils/9._vbscript_callback`: DT_G_Reset
- `games/spectrum.json#/coils/9._inferred_type`: drop_target_reset
- `games/spectrum.json#/coils/9._note`: Resets drop targets sw34, sw35, sw36
- `games/spectrum.json#/coils/10._vbscript_callback`: DT_Y_Reset
- `games/spectrum.json#/coils/10._inferred_type`: drop_target_reset
- `games/spectrum.json#/coils/10._note`: Resets drop targets sw37, sw38, sw39
- `games/spectrum.json#/coils/11._vbscript_callback`: DT_R_Reset
- `games/spectrum.json#/coils/11._inferred_type`: drop_target_reset
- `games/spectrum.json#/coils/11._note`: Resets drop targets sw45, sw46, sw47
- `games/spectrum.json#/coils/12._vbscript_callback`: SolGI
- `games/spectrum.json#/coils/12._inferred_type`: gi
- `games/spectrum.json#/coils/12._note`: Enables/disables GI lighting. Iterates GI array setting state.
- `games/spectrum.json#/coils/13._vbscript_callback`: vpmNudge.SolGameOn
- `games/spectrum.json#/coils/13._inferred_type`: system
- `games/spectrum.json#/coils/13._note`: Standard Bally game-on solenoid. Enables nudge/tilt detection.
- `games/spectrum.json#/_source/confidence_notes`: High confidence on switches/coils from explicit Controller.Switch() and SolCallback assignments. No Const sw* definitions — switches identified from _Hit/_UnHit subs and Controller.Switch() calls. No NFadeL/NFadeLm/Flash/Lampz macros found — lamps use vpmMapLights AllLamps (implicit VPX light-to-lamp mapping; actual lamp IDs depend on VPX table light numbering, not extractable from script alone). Early Bally -17/-35 platform. Drain uses cvpmBallStack (not cvpmTrough) with single switch 8. Four saucer kickers (sw7, sw17, sw24, sw41, sw48) each have dual-direction kick logic. Drop targets in 4 banks of 3.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.spectrum`: `games/spectrum.json` at the pinned migration revision.
