# Jurassic Park

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/jpark.json#/switches/0._note`: vpmNudge.TiltSwitch = 1
- `games/jpark.json#/switches/1._note`: Ball enters trough from drain, kicks up chain sw9->sw10->sw11->sw12->sw13->sw14
- `games/jpark.json#/switches/6._note`: Top of trough chain; SolTrough kicks from here to sw15
- `games/jpark.json#/switches/7._note`: Virtual switch set by SolTrough/SolRelease; Controller.Switch(15) toggled in code. sw15 is a physical VPX kicker used by SolRelease to kick ball into shooter lane.
- `games/jpark.json#/switches/8._note`: Also plungerIM.Switch 16
- `games/jpark.json#/switches/17._inferred_type`: standup_target
- `games/jpark.json#/switches/18._inferred_type`: standup_target
- `games/jpark.json#/switches/19._inferred_type`: standup_target
- `games/jpark.json#/switches/20._inferred_type`: kicker
- `games/jpark.json#/switches/21._inferred_type`: opto
- `games/jpark.json#/switches/21._note`: Set by T-Rex rotation motor code (MotorTimer_Timer), not a physical VPX trigger
- `games/jpark.json#/switches/22._inferred_type`: opto
- `games/jpark.json#/switches/22._note`: Set by T-Rex rotation motor code (MotorTimer_Timer), not a physical VPX trigger
- `games/jpark.json#/switches/25._inferred_type`: kicker
- `games/jpark.json#/switches/26._inferred_type`: opto
- `games/jpark.json#/switches/26._note`: Set by T-Rex rotation motor code (MotorTimer_Timer), not a physical VPX trigger
- `games/jpark.json#/switches/27._inferred_type`: kicker
- `games/jpark.json#/switches/27._note`: Uses vpmTimer.PulseSw 37
- `games/jpark.json#/switches/28._inferred_type`: standup_target
- `games/jpark.json#/switches/29._inferred_type`: standup_target
- `games/jpark.json#/switches/30._inferred_type`: standup_target
- `games/jpark.json#/switches/31._inferred_type`: cabinet
- `games/jpark.json#/switches/31._note`: Mapped to PlungerKey in keycode handler
- `games/jpark.json#/switches/32._inferred_type`: cabinet
- `games/jpark.json#/switches/32._note`: Mapped to RightMagnaSave/LeftMagnaSave/LockBarKey in keycode handler
- `games/jpark.json#/switches/33._inferred_type`: slingshot
- `games/jpark.json#/switches/33._note`: Pulsed from LeftSlingShot_Slingshot event
- `games/jpark.json#/switches/34._inferred_type`: slingshot
- `games/jpark.json#/switches/34._note`: Pulsed from RightSlingShot_Slingshot event
- `games/jpark.json#/switches/35._inferred_type`: bumper
- `games/jpark.json#/switches/36._inferred_type`: bumper
- `games/jpark.json#/switches/37._inferred_type`: bumper
- `games/jpark.json#/switches/38._inferred_type`: captive_ball
- `games/jpark.json#/switches/39._inferred_type`: standup_target
- `games/jpark.json#/switches/40._inferred_type`: standup_target
- `games/jpark.json#/switches/41._inferred_type`: standup_target
- `games/jpark.json#/switches/42._inferred_type`: standup_target
- `games/jpark.json#/switches/43._inferred_type`: kicker
- `games/jpark.json#/switches/43._note`: Ball held for T-Rex head animation; debounced with timer
- `games/jpark.json#/switches/44._inferred_type`: kicker
- `games/jpark.json#/switches/45._inferred_type`: opto
- `games/jpark.json#/switches/45._note`: Set by T-Rex bend motor code (UpDownTimer_Timer), not a physical VPX trigger
- `games/jpark.json#/switches/46._inferred_type`: opto
- `games/jpark.json#/switches/46._note`: Set by T-Rex bend motor code (UpDownTimer_Timer), not a physical VPX trigger
- `games/jpark.json#/switches/47._inferred_type`: kicker
- `games/jpark.json#/switches/47._note`: Uses vpmTimer.PulseSw 59
- `games/jpark.json#/switches/48._inferred_type`: kicker
- `games/jpark.json#/switches/48._note`: Uses vpmTimer.PulseSw 60
- `games/jpark.json#/switches/49._inferred_type`: vuk
- `games/jpark.json#/coils/0._vbscript_callback`: BoatDockSaucer
- `games/jpark.json#/coils/0._inferred_type`: kicker
- `games/jpark.json#/coils/1._vbscript_callback`: SolRelease
- `games/jpark.json#/coils/1._inferred_type`: ball_management
- `games/jpark.json#/coils/1._note`: Kicks ball from sw15 into shooter lane
- `games/jpark.json#/coils/2._vbscript_callback`: AutoLaunch
- `games/jpark.json#/coils/2._inferred_type`: ball_management
- `games/jpark.json#/coils/2._note`: Uses cvpmImpulseP plungerIM on swPlunger
- `games/jpark.json#/coils/3._vbscript_callback`: LeftScoopEject
- `games/jpark.json#/coils/3._inferred_type`: kicker
- `games/jpark.json#/coils/4._vbscript_callback`: VukKick
- `games/jpark.json#/coils/4._inferred_type`: vuk
- `games/jpark.json#/coils/5._vbscript_callback`: Divert
- `games/jpark.json#/coils/5._inferred_type`: diverter
- `games/jpark.json#/coils/6._vbscript_callback`: RexSaucer
- `games/jpark.json#/coils/6._inferred_type`: kicker
- `games/jpark.json#/coils/7._vbscript_callback`: vpmSolSound SfxKnocker,
- `games/jpark.json#/coils/7._inferred_type`: knocker
- `games/jpark.json#/coils/8._vbscript_callback`: RaptorKick
- `games/jpark.json#/coils/8._inferred_type`: kicker
- `games/jpark.json#/coils/9._vbscript_callback`: SolGI
- `games/jpark.json#/coils/9._inferred_type`: gi_relay
- `games/jpark.json#/coils/9._note`: SolModCallBack (PWM); controls all GI lighting via VLM BL_GI array
- `games/jpark.json#/coils/10._vbscript_callback`: RexLeftRight
- `games/jpark.json#/coils/10._inferred_type`: mechanism
- `games/jpark.json#/coils/11._vbscript_callback`: RexMouth
- `games/jpark.json#/coils/11._inferred_type`: mechanism
- `games/jpark.json#/coils/12._vbscript_callback`: RexUpDown
- `games/jpark.json#/coils/12._inferred_type`: mechanism
- `games/jpark.json#/coils/13._vbscript_callback`: RexMotor
- `games/jpark.json#/coils/13._inferred_type`: mechanism
- `games/jpark.json#/coils/14._vbscript_callback`: SolTrough
- `games/jpark.json#/coils/14._inferred_type`: ball_management
- `games/jpark.json#/coils/14._note`: Kicks ball from sw14 to sw15 and sets Controller.Switch(15)=1
- `games/jpark.json#/coils/15._inferred_type`: bumper
- `games/jpark.json#/coils/15._note`: SolCallback commented out in script; framework handles
- `games/jpark.json#/coils/16._inferred_type`: bumper
- `games/jpark.json#/coils/16._note`: SolCallback commented out in script; framework handles
- `games/jpark.json#/coils/17._inferred_type`: bumper
- `games/jpark.json#/coils/17._note`: SolCallback commented out in script; framework handles
- `games/jpark.json#/coils/18._vbscript_callback`: vpmSolSound SfxSling,
- `games/jpark.json#/coils/18._inferred_type`: slingshot
- `games/jpark.json#/coils/19._vbscript_callback`: vpmSolSound SfxSling,
- `games/jpark.json#/coils/19._inferred_type`: slingshot
- `games/jpark.json#/coils/20._vbscript_callback`: ShakerMotor
- `games/jpark.json#/coils/20._inferred_type`: shaker
- `games/jpark.json#/coils/21._vbscript_callback`: RelayAC
- `games/jpark.json#/coils/21._inferred_type`: relay
- `games/jpark.json#/coils/21._note`: Callback is empty (no-op)
- `games/jpark.json#/coils/22._vbscript_callback`: Flash1
- `games/jpark.json#/coils/22._inferred_type`: flasher
- `games/jpark.json#/coils/22._note`: SolModCallBack (PWM); controls F1a/F1b lights
- `games/jpark.json#/coils/23._vbscript_callback`: Flash2
- `games/jpark.json#/coils/23._inferred_type`: flasher
- `games/jpark.json#/coils/23._note`: SolModCallBack (PWM); controls F2a/F2b/F2c lights
- `games/jpark.json#/coils/24._vbscript_callback`: Flash3
- `games/jpark.json#/coils/24._inferred_type`: flasher
- `games/jpark.json#/coils/24._note`: SolModCallBack (PWM); controls F3a/F3b/F3c/F3d lights
- `games/jpark.json#/coils/25._vbscript_callback`: Flash4
- `games/jpark.json#/coils/25._inferred_type`: flasher
- `games/jpark.json#/coils/25._note`: SolModCallBack (PWM); controls F4a/F4b/F4c/F4d lights
- `games/jpark.json#/coils/26._vbscript_callback`: Flash5
- `games/jpark.json#/coils/26._inferred_type`: flasher
- `games/jpark.json#/coils/26._note`: SolModCallBack (PWM); controls F5/F5a/F5b/F5c lights
- `games/jpark.json#/coils/27._vbscript_callback`: Flash6
- `games/jpark.json#/coils/27._inferred_type`: flasher
- `games/jpark.json#/coils/27._note`: SolModCallBack (PWM); controls F6a/F6b/F6c lights
- `games/jpark.json#/coils/28._vbscript_callback`: Flash7
- `games/jpark.json#/coils/28._inferred_type`: flasher
- `games/jpark.json#/coils/28._note`: SolModCallBack (PWM); controls F7a/F7b/F7c/F7d lights
- `games/jpark.json#/coils/29._vbscript_callback`: Flash8
- `games/jpark.json#/coils/29._inferred_type`: flasher
- `games/jpark.json#/coils/29._note`: SolModCallBack (PWM); controls F8a/F8b lights
- `games/jpark.json#/coils/30._vbscript_callback`: SolRFlipper
- `games/jpark.json#/coils/30._inferred_type`: flipper
- `games/jpark.json#/coils/30._note`: sLRFlipper=46 (DE.VBS framework constant)
- `games/jpark.json#/coils/31._vbscript_callback`: SolLFlipper
- `games/jpark.json#/coils/31._inferred_type`: flipper
- `games/jpark.json#/coils/31._note`: sLLFlipper=48 (DE.VBS framework constant)
- `games/jpark.json#/lamps/0._vlm_name`: BL_inserts_L1
- `games/jpark.json#/lamps/1._vlm_name`: BL_ins2_L2
- `games/jpark.json#/lamps/2._vlm_name`: BL_inserts_L3
- `games/jpark.json#/lamps/3._vlm_name`: BL_inserts_L4
- `games/jpark.json#/lamps/4._vlm_name`: BL_inserts_L5
- `games/jpark.json#/lamps/5._vlm_name`: BL_inserts_L6
- `games/jpark.json#/lamps/6._vlm_name`: BL_inserts_L7
- `games/jpark.json#/lamps/7._vlm_name`: BL_inserts_L8
- `games/jpark.json#/lamps/8._vlm_name`: BL_inserts_L10
- `games/jpark.json#/lamps/9._vlm_name`: BL_inserts_L11
- `games/jpark.json#/lamps/10._vlm_name`: BL_inserts_L12
- `games/jpark.json#/lamps/11._vlm_name`: BL_inserts_L13
- `games/jpark.json#/lamps/12._vlm_name`: BL_inserts_L14
- `games/jpark.json#/lamps/13._vlm_name`: BL_inserts_L15
- `games/jpark.json#/lamps/14._vlm_name`: BL_inserts_L16
- `games/jpark.json#/lamps/15._vlm_name`: BL_ins2_L17
- `games/jpark.json#/lamps/16._vlm_name`: BL_ins2_L18
- `games/jpark.json#/lamps/17._vlm_name`: BL_inserts_L19
- `games/jpark.json#/lamps/18._vlm_name`: BL_inserts_L20
- `games/jpark.json#/lamps/19._vlm_name`: BL_inserts_L21
- `games/jpark.json#/lamps/20._vlm_name`: BL_inserts_L22
- `games/jpark.json#/lamps/21._vlm_name`: BL_inserts_L23
- `games/jpark.json#/lamps/22._vlm_name`: BL_inserts_L24
- `games/jpark.json#/lamps/23._vlm_name`: BL_inserts_L25
- `games/jpark.json#/lamps/24._vlm_name`: BL_inserts_L26
- `games/jpark.json#/lamps/25._vlm_name`: BL_inserts_L27
- `games/jpark.json#/lamps/26._vlm_name`: BL_inserts_L28
- `games/jpark.json#/lamps/27._vlm_name`: BL_inserts_L29
- `games/jpark.json#/lamps/28._vlm_name`: BL_inserts_L30
- `games/jpark.json#/lamps/29._vlm_name`: BL_ins2_L31
- `games/jpark.json#/lamps/30._vlm_name`: BL_ins2_L32
- `games/jpark.json#/lamps/31._vlm_name`: BL_ins2_L33
- `games/jpark.json#/lamps/32._vlm_name`: BL_ins2_L34
- `games/jpark.json#/lamps/33._vlm_name`: BL_inserts_L35
- `games/jpark.json#/lamps/34._vlm_name`: BL_inserts_L36
- `games/jpark.json#/lamps/35._vlm_name`: BL_inserts_L37
- `games/jpark.json#/lamps/35._note`: Also has VLM layer BL_ins2_L37b
- `games/jpark.json#/lamps/36._vlm_name`: BL_inserts_L38
- `games/jpark.json#/lamps/37._vlm_name`: BL_inserts_L39
- `games/jpark.json#/lamps/38._vlm_name`: BL_inserts_L40
- `games/jpark.json#/lamps/39._vlm_name`: BL_inserts_L41
- `games/jpark.json#/lamps/40._vlm_name`: BL_inserts_L42
- `games/jpark.json#/lamps/41._vlm_name`: BL_inserts_L43
- `games/jpark.json#/lamps/42._vlm_name`: BL_inserts_L44
- `games/jpark.json#/lamps/43._vlm_name`: BL_inserts_L45
- `games/jpark.json#/lamps/44._vlm_name`: BL_ins2_L46a
- `games/jpark.json#/lamps/44._note`: Two VLM layers: L46a and L46b
- `games/jpark.json#/lamps/45._vlm_name`: BL_ins2_L47
- `games/jpark.json#/lamps/46._vlm_name`: BL_ins2_L48
- `games/jpark.json#/lamps/47._vlm_name`: BL_inserts_L49
- `games/jpark.json#/lamps/48._vlm_name`: BL_inserts_L50
- `games/jpark.json#/lamps/49._vlm_name`: BL_inserts_L51
- `games/jpark.json#/lamps/50._vlm_name`: BL_inserts_L52
- `games/jpark.json#/lamps/51._vlm_name`: BL_inserts_L53
- `games/jpark.json#/lamps/52._vlm_name`: BL_inserts_L54
- `games/jpark.json#/lamps/53._vlm_name`: BL_inserts_L55
- `games/jpark.json#/lamps/54._vlm_name`: BL_inserts_L56
- `games/jpark.json#/lamps/55._vlm_name`: BL_ins2_l57
- `games/jpark.json#/lamps/56._vlm_name`: BL_ins2_l58
- `games/jpark.json#/lamps/57._vlm_name`: BL_inserts_L59
- `games/jpark.json#/lamps/58._vlm_name`: BL_ins2_L60
- `games/jpark.json#/lamps/59._vlm_name`: BL_inserts_L61
- `games/jpark.json#/lamps/60._vlm_name`: BL_ins2_L62
- `games/jpark.json#/lamps/61._vlm_name`: BL_inserts_L63
- `games/jpark.json#/lamps/62._vlm_name`: BL_inserts_L64
- `games/jpark.json#/lamps/63._vlm_name`: BL_GISplit_L100
- `games/jpark.json#/lamps/63._note`: GI split lamp (controlled via GI relay solenoid 11)
- `games/jpark.json#/lamps/64._vlm_name`: BL_GISplit_L101
- `games/jpark.json#/lamps/64._note`: GI split lamp
- `games/jpark.json#/lamps/65._vlm_name`: BL_GISplit_L102
- `games/jpark.json#/lamps/65._note`: GI split lamp
- `games/jpark.json#/lamps/66._vlm_name`: BL_GISplit_L103
- `games/jpark.json#/lamps/66._note`: GI split lamp
- `games/jpark.json#/lamps/67._vlm_name`: BL_GISplit_L104
- `games/jpark.json#/lamps/67._note`: GI split lamp
- `games/jpark.json#/lamps/68._vlm_name`: BL_GISplit_L105
- `games/jpark.json#/lamps/68._note`: GI split lamp
- `games/jpark.json#/lamps/69._vlm_name`: BL_GISplit_L106
- `games/jpark.json#/lamps/69._note`: GI split lamp
- `games/jpark.json#/lamps/70._vlm_name`: BL_GISplit_L108
- `games/jpark.json#/lamps/70._note`: GI split lamp
- `games/jpark.json#/lamps/71._vlm_name`: BL_GISplit_L114
- `games/jpark.json#/lamps/71._note`: GI split lamp
- `games/jpark.json#/lamps/72._vlm_name`: BL_GISplit_L124
- `games/jpark.json#/lamps/72._note`: GI split lamp
- `games/jpark.json#/lamps/73._vlm_name`: BL_GISplit_l125
- `games/jpark.json#/lamps/73._note`: GI split lamp
- `games/jpark.json#/lamps/74._vlm_name`: BL_inserts_L127
- `games/jpark.json#/lamps/75._vlm_name`: BL_inserts_L128
- `games/jpark.json#/_source/confidence_notes`: High confidence on switches/coils from Controller.Switch() calls and SolCallback assignments. No Const sw* declarations in table script — all switches referenced by raw number. Lamps extracted from VLM BL_inserts_L/BL_ins2_L/BL_GISplit_L arrays — no descriptions available (VLM only provides light IDs, not names). Flashers are SolModCallBack entries (solenoid-driven). Flippers (sLRFlipper=46, sLLFlipper=48) are DE.VBS framework-defined constants, not in table script. Trough is a manual 6-ball design (sw9-sw14) with custom UpdateTrough logic, not bsTrough. GI on solenoid 11 via SolModCallBack.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.jpark`: `games/jpark.json` at the pinned migration revision.
