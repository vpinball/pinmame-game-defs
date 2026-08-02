# Fish Tales

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1992). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/wpc.json#/coils/1`: Unbound legacy outputs record `c_flipper_lower_right` was retained as a migration note only.
- `platforms/wpc.json#/coils/2`: Unbound legacy outputs record `c_flipper_lower_left` was retained as a migration note only.
- `platforms/wpc.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/wpc.json#/coils/4`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/ft.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/ft.json#/switches/5._note`: Ball release end; SolRelease kicks from sw16
- `games/ft.json#/switches/9._note`: Controller.Switch(22) = 1 on init
- `games/ft.json#/switches/11._note`: Controller.Switch(24) = 1 on init
- `games/ft.json#/switches/12._inferred_type`: rollover
- `games/ft.json#/switches/13._inferred_type`: rollover
- `games/ft.json#/switches/14._inferred_type`: standup_target
- `games/ft.json#/switches/15._inferred_type`: standup_target
- `games/ft.json#/switches/16._note`: Mapped to PlungerKey; Controller.Switch(31) toggled on KeyDown/KeyUp
- `games/ft.json#/switches/17._inferred_type`: rollover
- `games/ft.json#/switches/18._inferred_type`: rollover
- `games/ft.json#/switches/19._inferred_type`: spinner
- `games/ft.json#/switches/20._inferred_type`: rollover
- `games/ft.json#/switches/20._note`: Trigger at reel entry; PulseSw 35
- `games/ft.json#/switches/21._inferred_type`: saucer
- `games/ft.json#/switches/21._note`: Set on Catapult_hit, cleared by SolCatapult or timer
- `games/ft.json#/switches/22._note`: Driven by VBS ReelPosTable; not a physical switch in VPX
- `games/ft.json#/switches/23._note`: Driven by VBS ReelPosTable; not a physical switch in VPX
- `games/ft.json#/switches/24._inferred_type`: standup_target
- `games/ft.json#/switches/25._inferred_type`: rollover
- `games/ft.json#/switches/25._note`: VPX object sw42a maps to PulseSw 42
- `games/ft.json#/switches/26._inferred_type`: rollover
- `games/ft.json#/switches/26._note`: VPX object sw43a maps to PulseSw 43
- `games/ft.json#/switches/27._inferred_type`: rollover
- `games/ft.json#/switches/28._inferred_type`: rollover
- `games/ft.json#/switches/29._inferred_type`: rollover
- `games/ft.json#/switches/30._inferred_type`: saucer
- `games/ft.json#/switches/30._note`: VUK (Vertical Up Kicker) for Caster Club
- `games/ft.json#/switches/31._inferred_type`: drop_target
- `games/ft.json#/switches/32._inferred_type`: bumper
- `games/ft.json#/switches/33._inferred_type`: bumper
- `games/ft.json#/switches/34._inferred_type`: bumper
- `games/ft.json#/switches/35._inferred_type`: standup_target
- `games/ft.json#/switches/36._inferred_type`: standup_target
- `games/ft.json#/switches/37._inferred_type`: rollover
- `games/ft.json#/switches/37._note`: Held switch (Controller.Switch set/cleared on Hit/UnHit)
- `games/ft.json#/switches/38._inferred_type`: slingshot
- `games/ft.json#/switches/39._inferred_type`: slingshot
- `games/ft.json#/switches/40._inferred_type`: standup_target
- `games/ft.json#/switches/41._inferred_type`: rollover
- `games/ft.json#/switches/42._inferred_type`: saucer
- `games/ft.json#/switches/42._note`: Fish Finder saucer; SolFF controls eject
- `games/ft.json#/switches/43._inferred_type`: rollover
- `games/ft.json#/switches/44._inferred_type`: rollover
- `games/ft.json#/switches/45._inferred_type`: rollover
- `games/ft.json#/coils/0._vbscript_callback`: AutoPlunger
- `games/ft.json#/coils/0._inferred_type`: kicker
- `games/ft.json#/coils/1._vbscript_callback`: SolCatapult
- `games/ft.json#/coils/1._inferred_type`: kicker
- `games/ft.json#/coils/2._vbscript_callback`: SolVUK
- `games/ft.json#/coils/2._inferred_type`: kicker
- `games/ft.json#/coils/5._vbscript_callback`: SolGate
- `games/ft.json#/coils/5._inferred_type`: diverter
- `games/ft.json#/coils/6._vbscript_callback`: SolKnocker
- `games/ft.json#/coils/6._inferred_type`: knocker
- `games/ft.json#/coils/7._vbscript_callback`: TopperFish
- `games/ft.json#/coils/7._inferred_type`: toy
- `games/ft.json#/coils/7._note`: VR Topper fish animation; not a physical solenoid on playfield
- `games/ft.json#/coils/8._vbscript_callback`: SolDrain
- `games/ft.json#/coils/8._inferred_type`: kicker
- `games/ft.json#/coils/9._vbscript_callback`: SolRelease
- `games/ft.json#/coils/9._inferred_type`: kicker
- `games/ft.json#/coils/10._vbscript_callback`: SolFF
- `games/ft.json#/coils/10._inferred_type`: kicker
- `games/ft.json#/coils/11._vbscript_callback`: SolDTUp
- `games/ft.json#/coils/11._inferred_type`: drop_target_reset
- `games/ft.json#/coils/12._vbscript_callback`: SolDTDown
- `games/ft.json#/coils/12._inferred_type`: drop_target_trip
- `games/ft.json#/coils/16._vbscript_callback`: Flash17
- `games/ft.json#/coils/16._inferred_type`: flasher
- `games/ft.json#/coils/16._note`: PWM via SolModCallBack; also f17b
- `games/ft.json#/coils/17._vbscript_callback`: Flash18
- `games/ft.json#/coils/17._inferred_type`: flasher
- `games/ft.json#/coils/17._note`: PWM via SolModCallBack; also f18b
- `games/ft.json#/coils/18._vbscript_callback`: Flash19
- `games/ft.json#/coils/18._inferred_type`: flasher
- `games/ft.json#/coils/18._note`: PWM via SolModCallBack
- `games/ft.json#/coils/19._vbscript_callback`: Flash20
- `games/ft.json#/coils/19._inferred_type`: flasher
- `games/ft.json#/coils/19._note`: PWM via SolModCallBack
- `games/ft.json#/coils/20._vbscript_callback`: Flash21
- `games/ft.json#/coils/20._inferred_type`: flasher
- `games/ft.json#/coils/20._note`: PWM via SolModCallBack
- `games/ft.json#/coils/21._vbscript_callback`: Flash22
- `games/ft.json#/coils/21._inferred_type`: flasher
- `games/ft.json#/coils/21._note`: PWM via SolModCallBack
- `games/ft.json#/coils/22._vbscript_callback`: Flash23
- `games/ft.json#/coils/22._inferred_type`: flasher
- `games/ft.json#/coils/22._note`: PWM via SolModCallBack
- `games/ft.json#/coils/23._note`: No SolCallback(24) assigned
- `games/ft.json#/coils/24._vbscript_callback`: Flash25
- `games/ft.json#/coils/24._inferred_type`: flasher
- `games/ft.json#/coils/24._note`: PWM via SolModCallBack
- `games/ft.json#/coils/25._vbscript_callback`: Flash26
- `games/ft.json#/coils/25._inferred_type`: flasher
- `games/ft.json#/coils/25._note`: PWM via SolModCallBack
- `games/ft.json#/coils/26._vbscript_callback`: Flash27
- `games/ft.json#/coils/26._inferred_type`: flasher
- `games/ft.json#/coils/26._note`: PWM via SolModCallBack
- `games/ft.json#/coils/27._vbscript_callback`: ReelMotor
- `games/ft.json#/coils/27._inferred_type`: motor
- `games/ft.json#/coils/27._note`: Drives fishing reel mechanism; controls reel rotation and ball lock/release positions via ReelPosTable
- `games/ft.json#/coils/30._vbscript_callback`: SolRFlipper
- `games/ft.json#/coils/30._inferred_type`: flipper
- `games/ft.json#/coils/30._note`: Framework constant sLRFlipper=46 from core.vbs
- `games/ft.json#/coils/31._vbscript_callback`: SolLFlipper
- `games/ft.json#/coils/31._inferred_type`: flipper
- `games/ft.json#/coils/31._note`: Framework constant sLLFlipper=48 from core.vbs; NoUpperLeftFlipper and NoUpperRightFlipper called
- `games/ft.json#/lamps/0._vlm_array`: BL_Inserts_l11
- `games/ft.json#/lamps/1._vlm_array`: BL_Inserts_l12
- `games/ft.json#/lamps/2._vlm_array`: BL_Inserts_l13
- `games/ft.json#/lamps/3._vlm_array`: BL_Inserts_l14
- `games/ft.json#/lamps/4._vlm_array`: BL_Inserts_l15
- `games/ft.json#/lamps/5._vlm_array`: BL_Inserts_l16
- `games/ft.json#/lamps/6._vlm_array`: BL_Inserts_l17
- `games/ft.json#/lamps/7._vlm_array`: BL_Inserts_l18
- `games/ft.json#/lamps/8._vlm_array`: BL_Inserts_l21
- `games/ft.json#/lamps/9._vlm_array`: BL_Inserts_l22
- `games/ft.json#/lamps/10._vlm_array`: BL_Inserts_l23
- `games/ft.json#/lamps/11._vlm_array`: BL_Inserts_l24
- `games/ft.json#/lamps/12._vlm_array`: BL_Inserts_l25
- `games/ft.json#/lamps/13._vlm_array`: BL_Inserts_l26
- `games/ft.json#/lamps/14._vlm_array`: BL_Inserts_l27
- `games/ft.json#/lamps/15._vlm_array`: BL_Inserts_l28
- `games/ft.json#/lamps/16._vlm_array`: BL_Inserts_l31
- `games/ft.json#/lamps/17._vlm_array`: BL_Inserts_l32
- `games/ft.json#/lamps/18._vlm_array`: BL_Inserts_l33
- `games/ft.json#/lamps/19._vlm_array`: BL_Inserts_l34
- `games/ft.json#/lamps/20._vlm_array`: BL_Inserts_l35
- `games/ft.json#/lamps/21._vlm_array`: BL_Inserts_l36
- `games/ft.json#/lamps/22._vlm_array`: BL_Inserts_l37
- `games/ft.json#/lamps/23._vlm_array`: BL_Inserts_l38
- `games/ft.json#/lamps/24._vlm_array`: BL_Inserts_l41
- `games/ft.json#/lamps/25._vlm_array`: BL_Inserts_l42
- `games/ft.json#/lamps/26._vlm_array`: BL_Inserts_l43
- `games/ft.json#/lamps/27._vlm_array`: BL_Inserts_l44
- `games/ft.json#/lamps/28._vlm_array`: BL_Inserts_l45
- `games/ft.json#/lamps/29._vlm_array`: BL_Inserts_l46
- `games/ft.json#/lamps/30._vlm_array`: BL_Inserts_l47
- `games/ft.json#/lamps/31._vlm_array`: BL_Inserts_l48
- `games/ft.json#/lamps/32._vlm_array`: BL_Inserts_l51
- `games/ft.json#/lamps/33._vlm_array`: BL_Inserts_l52
- `games/ft.json#/lamps/34._vlm_array`: BL_Inserts_l53
- `games/ft.json#/lamps/35._vlm_array`: BL_Inserts_l54
- `games/ft.json#/lamps/36._vlm_array`: BL_Inserts_l55
- `games/ft.json#/lamps/37._vlm_array`: BL_Inserts_l56
- `games/ft.json#/lamps/38._vlm_array`: BL_Inserts_l57
- `games/ft.json#/lamps/39._vlm_array`: BL_Inserts_l58
- `games/ft.json#/lamps/40._vlm_array`: BL_Inserts_l61
- `games/ft.json#/lamps/41._vlm_array`: BL_Inserts_l62
- `games/ft.json#/lamps/42._vlm_array`: BL_Inserts_l63
- `games/ft.json#/lamps/43._vlm_array`: BL_Inserts_l64
- `games/ft.json#/lamps/44._vlm_array`: BL_Inserts_l65
- `games/ft.json#/lamps/45._vlm_array`: BL_Inserts_l66
- `games/ft.json#/lamps/46._vlm_array`: BL_Inserts_l67
- `games/ft.json#/lamps/47._vlm_array`: BL_Inserts_l68
- `games/ft.json#/lamps/48._vlm_array`: BL_Inserts_l71
- `games/ft.json#/lamps/49._vlm_array`: BL_Inserts_l72
- `games/ft.json#/lamps/50._vlm_array`: BL_Inserts_l73
- `games/ft.json#/lamps/51._vlm_array`: BL_Inserts_l74
- `games/ft.json#/lamps/52._vlm_array`: BL_Inserts_l75
- `games/ft.json#/lamps/53._vlm_array`: BL_Inserts_l76
- `games/ft.json#/lamps/54._vlm_array`: BL_Inserts_l77
- `games/ft.json#/lamps/55._vlm_array`: BL_Inserts_l78
- `games/ft.json#/lamps/56._vlm_array`: BL_Inserts_l81
- `games/ft.json#/lamps/57._vlm_array`: BL_Inserts_l82
- `games/ft.json#/lamps/58._vlm_array`: BL_Inserts_l83
- `games/ft.json#/lamps/59._vlm_array`: BL_Inserts_l84
- `games/ft.json#/lamps/60._vlm_array`: BL_Inserts_l85
- `games/ft.json#/lamps/61._vlm_array`: BL_Inserts_l86
- `games/ft.json#/lamps/62`: Unbound legacy outputs record `48a` was retained as a migration note only.
- `games/ft.json#/lamps/62._vlm_array`: BL_Inserts_l48a
- `games/ft.json#/lamps/62._note`: VPX-only lamp; split from L48 for better lighting geometry. Not in original WPC lamp matrix.
- `games/ft.json#/lamps/63._note`: Under apron; added to AllLamps collection. Drives Primary_StartButton and StartButton2 lighting in VR
- `games/ft.json#/gi_strings/2._note`: Also controls VLM arrays: BL_GITop, BL_GISplit_gi002, BL_GISplit_gi006, BL_GISplit_gi009, BL_GISplit_gi011, BL_GISplit_gitop020
- `games/ft.json#/gi_strings/3._note`: Also controls VLM array BL_GIBottom; affects ball color based on room brightness
- `games/ft.json#/_source/confidence_notes`: High confidence on coils/SolCallbacks, switches, and lamp matrix. No Const sw* definitions in table script - uses raw switch numbers (Controller.Switch(N), VPMTimer.PulseSw N) and raw SolCallback(N) indices. Trough is custom-implemented (not bsTrough): sw16/sw17/sw18 are trough kicker switches, sw15 (Drain_Hit) is outhole. Reel mechanism uses switches 37/38 driven by position table in VBS (not physical optos). sLLFlipper/sLRFlipper are framework constants from WPC.VBS (typically 46/34 for WPC). Flashers 17-23,25-27 use SolModCallBack for PWM dimming. Lamp numbers derived from VLM BL_Inserts_l## arrays and cross-referenced with Fish Tales manual lamp matrix. L48a is a VPX-only extra lamp (split from L48 for better lighting). L88 is Start Button lamp (added to AllLamps collection). IPDB ID: 861.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.ft`: `games/ft.json` at the pinned migration revision.
