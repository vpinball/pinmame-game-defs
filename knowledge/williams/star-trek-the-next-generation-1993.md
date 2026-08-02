# Star Trek: The Next Generation

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/sttng.json#/switches/0._note`: Directly set via keyFront in KeyDown/KeyUp handlers
- `games/sttng.json#/switches/1._note`: Set via PlungerKey and LockBarKey in KeyDown/KeyUp handlers
- `games/sttng.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/sttng.json#/switches/9._note`: Controller.Switch(22) = 1 in table init
- `games/sttng.json#/switches/11._note`: Controller.Switch(24) = 0 set in init, but PinMAME defines this as always closed
- `games/sttng.json#/switches/13._note`: Standup target; PulseSw in T26_Hit
- `games/sttng.json#/switches/14._note`: Neutral zone hole entry; PulseSw 27 in sw27_Hit. Also triggers T27 target animation
- `games/sttng.json#/switches/15._note`: Standup target; PulseSw in T28_Hit
- `games/sttng.json#/switches/16._note`: Opto switch. Used in BorgLock ball stack InitSw
- `games/sttng.json#/switches/17._note`: Opto. Set in sw32_Hit, cleared when sw36 (Under L Gun 1) is hit
- `games/sttng.json#/switches/18._note`: Opto. Set in sw33_Hit, cleared when sw37 (Under R Gun 1) is hit
- `games/sttng.json#/switches/19._note`: Opto. Set by Kicker2_Hit when ball enters right cannon
- `games/sttng.json#/switches/21._note`: Opto. Kicker trigger for left gun loading
- `games/sttng.json#/switches/22._note`: Opto. Kicker trigger for right gun loading
- `games/sttng.json#/switches/23._note`: Opto. Set by Kicker1_Hit when ball enters left cannon
- `games/sttng.json#/switches/24._note`: Opto. Primary lock kicker position
- `games/sttng.json#/switches/25._note`: Opto
- `games/sttng.json#/switches/26._note`: Opto
- `games/sttng.json#/switches/28._note`: PulseSw in sw45_Hit
- `games/sttng.json#/switches/29._note`: Set via sw46t_Hit trigger, not a kicker
- `games/sttng.json#/switches/30._note`: Start Mission scope; trigger with sw47dr drop mechanism
- `games/sttng.json#/switches/32._note`: Drop target; PulseSw in T51_Hit
- `games/sttng.json#/switches/33._note`: Drop target; PulseSw in T52_Hit
- `games/sttng.json#/switches/34._note`: Drop target; PulseSw in T53_Hit
- `games/sttng.json#/switches/35._note`: Drop target; PulseSw in T54_Hit
- `games/sttng.json#/switches/36._note`: Drop target; PulseSw in T55_Hit
- `games/sttng.json#/switches/37._note`: Drop target; PulseSw in T56_Hit
- `games/sttng.json#/switches/38._note`: Single drop target; handled via TopDrop cvpmDropTarget object
- `games/sttng.json#/switches/40._note`: Opto. bsTrough.InitSw position 6 (sw61)
- `games/sttng.json#/switches/41._note`: Opto. bsTrough.InitSw position 5 (sw62)
- `games/sttng.json#/switches/42._note`: Opto. bsTrough.InitSw position 4 (sw63)
- `games/sttng.json#/switches/43._note`: Opto. bsTrough.InitSw position 3 (sw64)
- `games/sttng.json#/switches/44._note`: Opto. bsTrough.InitSw position 2 (sw65)
- `games/sttng.json#/switches/45._note`: Opto. bsTrough.InitSw position 1 (sw66)
- `games/sttng.json#/switches/46._note`: PulseSw 67 in SolRelease callback
- `games/sttng.json#/switches/47._note`: Auto-plunger switch; set in AutoPlunger_Hit
- `games/sttng.json#/switches/48._note`: PulseSw 71 in LeftJetBumper_hit
- `games/sttng.json#/switches/49._note`: PulseSw 72 in RightJetBumper_hit
- `games/sttng.json#/switches/50._note`: PulseSw 73 in BottomJetBumper_hit
- `games/sttng.json#/switches/51._note`: PulseSw 74 in SlingShotRight_Slingshot
- `games/sttng.json#/switches/52._note`: PulseSw 75 in SlingShotLeft_Slingshot
- `games/sttng.json#/switches/56._note`: PulseSw in T81_Hit
- `games/sttng.json#/switches/57._note`: PulseSw in T82_Hit
- `games/sttng.json#/switches/59._note`: PulseSw in T84_Hit
- `games/sttng.json#/switches/60._note`: PulseSw in T85_Hit
- `games/sttng.json#/switches/61._note`: PulseSw in T86_Hit
- `games/sttng.json#/switches/64._note`: WPC F7 switch. PulseSw 117 in sw117spinner_Spin
- `games/sttng.json#/switches/65._note`: Custom switch column 9. Set dynamically by CannonLTimer based on cannon position
- `games/sttng.json#/switches/66._note`: Custom switch column 9. Set dynamically by CannonRTimer based on cannon position
- `games/sttng.json#/switches/67._note`: Custom switch column 9. Set dynamically by CannonRTimer based on cannon position
- `games/sttng.json#/switches/68._note`: Custom switch column 9. Set dynamically by CannonLTimer based on cannon position
- `games/sttng.json#/coils/0._vbscript_callback`: LeftCannonKicker
- `games/sttng.json#/coils/0._inferred_type`: kicker
- `games/sttng.json#/coils/0._note`: Fires ball from left cannon
- `games/sttng.json#/coils/1._vbscript_callback`: RightCannonKicker
- `games/sttng.json#/coils/1._inferred_type`: kicker
- `games/sttng.json#/coils/1._note`: Fires ball from right cannon
- `games/sttng.json#/coils/2._vbscript_callback`: UnderLeftGun
- `games/sttng.json#/coils/2._inferred_type`: kicker
- `games/sttng.json#/coils/2._note`: Kicks ball from under-left-gun to left cannon
- `games/sttng.json#/coils/3._vbscript_callback`: UnderRightGun
- `games/sttng.json#/coils/3._inferred_type`: kicker
- `games/sttng.json#/coils/3._note`: Kicks ball from under-right-gun to right cannon
- `games/sttng.json#/coils/4._vbscript_callback`: LeftLock
- `games/sttng.json#/coils/4._inferred_type`: kicker
- `games/sttng.json#/coils/4._note`: Ejects ball from left lock (under-left-lock sw1)
- `games/sttng.json#/coils/5._vbscript_callback`: AutoPlunge
- `games/sttng.json#/coils/5._inferred_type`: ball_management
- `games/sttng.json#/coils/5._note`: Auto-launches ball from shooter lane
- `games/sttng.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/sttng.json#/coils/6._inferred_type`: knocker
- `games/sttng.json#/coils/7._vbscript_callback`: Kickback
- `games/sttng.json#/coils/7._inferred_type`: kicker
- `games/sttng.json#/coils/7._note`: Left outlane kickback
- `games/sttng.json#/coils/8._inferred_type`: slingshot
- `games/sttng.json#/coils/8._note`: PinMAME defines sLSling=9. No explicit SolCallback in VBS — handled by VPM framework
- `games/sttng.json#/coils/9._inferred_type`: slingshot
- `games/sttng.json#/coils/9._note`: PinMAME defines sRSling=10. No explicit SolCallback in VBS — handled by VPM framework
- `games/sttng.json#/coils/10._vbscript_callback`: SolRelease
- `games/sttng.json#/coils/10._inferred_type`: ball_management
- `games/sttng.json#/coils/10._note`: bsTrough.ExitSol_On — ejects ball from trough. PinMAME: sTrough=11
- `games/sttng.json#/coils/11._inferred_type`: bumper
- `games/sttng.json#/coils/11._note`: PinMAME defines sJet1=12. No explicit SolCallback in VBS — handled by VPM framework
- `games/sttng.json#/coils/12._inferred_type`: bumper
- `games/sttng.json#/coils/12._note`: PinMAME defines sJet2=13. No explicit SolCallback in VBS — handled by VPM framework
- `games/sttng.json#/coils/13._inferred_type`: bumper
- `games/sttng.json#/coils/13._note`: PinMAME defines sJet3=14. No explicit SolCallback in VBS — handled by VPM framework
- `games/sttng.json#/coils/14._vbscript_callback`: TopDiverter
- `games/sttng.json#/coils/14._inferred_type`: diverter
- `games/sttng.json#/coils/15._vbscript_callback`: BorgLock.SolOut
- `games/sttng.json#/coils/15._inferred_type`: kicker
- `games/sttng.json#/coils/15._note`: Ejects ball from Borg lock
- `games/sttng.json#/coils/16._vbscript_callback`: LeftCannonMotor
- `games/sttng.json#/coils/16._inferred_type`: mechanism
- `games/sttng.json#/coils/16._note`: Rotates left cannon. Position tracked by switches 122 (mark) and 127 (home)
- `games/sttng.json#/coils/17._vbscript_callback`: RightCannonMotor
- `games/sttng.json#/coils/17._inferred_type`: mechanism
- `games/sttng.json#/coils/17._note`: Rotates right cannon. Position tracked by switches 125 (home) and 126 (mark)
- `games/sttng.json#/coils/18._vbscript_callback`: Flash120
- `games/sttng.json#/coils/18._inferred_type`: flasher
- `games/sttng.json#/coils/18._note`: SolModCallBack; also drives l83
- `games/sttng.json#/coils/19._vbscript_callback`: Flash121
- `games/sttng.json#/coils/19._inferred_type`: flasher
- `games/sttng.json#/coils/19._note`: SolModCallBack; also drives l121
- `games/sttng.json#/coils/20._vbscript_callback`: Flash122
- `games/sttng.json#/coils/20._inferred_type`: flasher
- `games/sttng.json#/coils/20._note`: SolModCallBack; also drives f122b, f122s
- `games/sttng.json#/coils/21._vbscript_callback`: Flash123
- `games/sttng.json#/coils/21._inferred_type`: flasher
- `games/sttng.json#/coils/21._note`: SolModCallBack; also drives f123a, ShieldGiBig7/8/10
- `games/sttng.json#/coils/22._vbscript_callback`: SetLamp 124,
- `games/sttng.json#/coils/22._inferred_type`: flasher
- `games/sttng.json#/coils/22._note`: Uses SetLamp to lamp 124 rather than SolModCallBack
- `games/sttng.json#/coils/23._vbscript_callback`: Flash125
- `games/sttng.json#/coils/23._inferred_type`: flasher
- `games/sttng.json#/coils/23._note`: SolModCallBack; left popper area. Also drives l125
- `games/sttng.json#/coils/24._vbscript_callback`: Flash126
- `games/sttng.json#/coils/24._inferred_type`: flasher
- `games/sttng.json#/coils/24._note`: SolModCallBack; also drives f126s, l78borgb1, l78borga1, l78d1, l78e1
- `games/sttng.json#/coils/25._vbscript_callback`: Flash127
- `games/sttng.json#/coils/25._inferred_type`: flasher
- `games/sttng.json#/coils/25._note`: SolModCallBack; also drives f127s, l78b1, l78c1, l78borgd1, l78borge1
- `games/sttng.json#/coils/26._vbscript_callback`: Flash128
- `games/sttng.json#/coils/26._inferred_type`: flasher
- `games/sttng.json#/coils/26._note`: SolModCallBack; also drives f128s, GiBigGreen, l78a1, l78borgc1
- `games/sttng.json#/coils/27._vbscript_callback`: UnderDiverterTop
- `games/sttng.json#/coils/27._inferred_type`: diverter
- `games/sttng.json#/coils/27._note`: WPC extboard solenoid. Controls DiverterFRG and sw37dr1 drop walls
- `games/sttng.json#/coils/28._vbscript_callback`: UnderDiverterBottom
- `games/sttng.json#/coils/28._inferred_type`: diverter
- `games/sttng.json#/coils/28._note`: WPC extboard solenoid. Controls DiverterFLG drop wall
- `games/sttng.json#/coils/29._vbscript_callback`: TopDrop.SolDropUp
- `games/sttng.json#/coils/29._inferred_type`: drop_target_reset
- `games/sttng.json#/coils/29._note`: WPC extboard solenoid. Resets the single top drop target
- `games/sttng.json#/coils/30._vbscript_callback`: TopDrop.SolDropDown
- `games/sttng.json#/coils/30._inferred_type`: drop_target_reset
- `games/sttng.json#/coils/30._note`: WPC extboard solenoid. Drops the top drop target
- `games/sttng.json#/coils/31._vbscript_callback`: Flash141
- `games/sttng.json#/coils/31._inferred_type`: flasher
- `games/sttng.json#/coils/31._note`: SolModCallBack; also drives f141s, f141s1, GiBigGreen, l141, l141a
- `games/sttng.json#/coils/32._vbscript_callback`: Flash142
- `games/sttng.json#/coils/32._inferred_type`: flasher
- `games/sttng.json#/coils/32._note`: SolModCallBack; also drives f142s, f142s1, GiBigRed, GiBigRed1, l142
- `games/sttng.json#/lamps/0._note`: Also l11b, f11
- `games/sttng.json#/lamps/1._note`: Also l12b, f12
- `games/sttng.json#/lamps/2._note`: Also l13b
- `games/sttng.json#/lamps/3._note`: Also l14b
- `games/sttng.json#/lamps/4._note`: Also l15b, f15
- `games/sttng.json#/lamps/5._note`: Also l16b
- `games/sttng.json#/lamps/6._note`: Also l17b
- `games/sttng.json#/lamps/7._note`: Also l18b
- `games/sttng.json#/lamps/8._note`: Also l21b
- `games/sttng.json#/lamps/9._note`: Also l22b
- `games/sttng.json#/lamps/10._note`: Also l23b
- `games/sttng.json#/lamps/11._note`: Also l24b, f24
- `games/sttng.json#/lamps/12._note`: Also l25b, f25
- `games/sttng.json#/lamps/13._note`: Also l26b, f26, f26s, f26s1, l26blue
- `games/sttng.json#/lamps/14._note`: Also l27b
- `games/sttng.json#/lamps/15._note`: Also l28b, f28
- `games/sttng.json#/lamps/16._note`: Also l31b
- `games/sttng.json#/lamps/17._note`: Also l32b
- `games/sttng.json#/lamps/18._note`: Also l33b
- `games/sttng.json#/lamps/19._note`: Also l34b, f34
- `games/sttng.json#/lamps/20._note`: Also l35b
- `games/sttng.json#/lamps/21._note`: Also l36b
- `games/sttng.json#/lamps/22._note`: Also l37b
- `games/sttng.json#/lamps/23._note`: Also l38b, f38
- `games/sttng.json#/lamps/24._note`: Also l41b, f41
- `games/sttng.json#/lamps/25._note`: Also l42b
- `games/sttng.json#/lamps/26._note`: Also l43b
- `games/sttng.json#/lamps/27._note`: Also l44b
- `games/sttng.json#/lamps/28._note`: Also l45b, f45
- `games/sttng.json#/lamps/29._note`: Also l46b
- `games/sttng.json#/lamps/30._note`: Also l47b
- `games/sttng.json#/lamps/31._note`: Also l48b, f48
- `games/sttng.json#/lamps/32._note`: Also l51b
- `games/sttng.json#/lamps/33._note`: Also f52, f52s, f52s1. l52 position moves with left cannon
- `games/sttng.json#/lamps/34._note`: Also f53, f53s. Object-based fade (NFadeObjm)
- `games/sttng.json#/lamps/35._note`: Also l54b
- `games/sttng.json#/lamps/36._note`: Also l55b
- `games/sttng.json#/lamps/37._note`: Also l56b
- `games/sttng.json#/lamps/38._note`: Also l57b
- `games/sttng.json#/lamps/39._note`: Also l58b
- `games/sttng.json#/lamps/40._note`: Also l61b
- `games/sttng.json#/lamps/41._note`: Also l62b
- `games/sttng.json#/lamps/42._note`: Also l63b
- `games/sttng.json#/lamps/43._note`: Also l64b
- `games/sttng.json#/lamps/44._note`: Also l65b
- `games/sttng.json#/lamps/45._note`: Also l66b
- `games/sttng.json#/lamps/46._note`: Also l67b, f67
- `games/sttng.json#/lamps/47._note`: Also l68b, f68
- `games/sttng.json#/lamps/48._note`: Also l71b
- `games/sttng.json#/lamps/49._note`: Also l72b
- `games/sttng.json#/lamps/50._note`: Also l73b
- `games/sttng.json#/lamps/51._note`: Also l74b
- `games/sttng.json#/lamps/52._note`: Also l75b
- `games/sttng.json#/lamps/53._note`: Also l76b
- `games/sttng.json#/lamps/54._note`: Also l77b
- `games/sttng.json#/lamps/55._note`: Borg ship lamp. Multiple VPX objects: l78a-e (custom mod), l78borga-e (original). Also l78a1-e1, l78borga1-e1 for flasher intensities
- `games/sttng.json#/lamps/56._note`: Also l81b
- `games/sttng.json#/lamps/57._note`: Also f82, f82s, f82s1. l82 position moves with right cannon
- `games/sttng.json#/lamps/58._note`: Also l84b, f84
- `games/sttng.json#/lamps/59._note`: Also f85, f85s. Object-based fade (NFadeObjm)
- `games/sttng.json#/lamps/60._note`: Also f86, f86s, f86s1. Object-based fade (NFadeObjm)
- `games/sttng.json#/lamps/61._note`: Also l124b. Autofire flasher lamp driven via SetLamp from coil 24
- `games/sttng.json#/_source/confidence_notes`: High confidence on switches/coils/lamps. No Const sw* declarations — switches referenced by number directly. Solenoid numbers 51-54 are WPC extboard solenoids; flasher solenoids 55-56 are extboard custom. Spinner is WPC F7 (switch 117). Flipper coil IDs (sLRFlipper, sLLFlipper, sURFlipper) are framework constants defined in wpc.VBS, not in the table script. Trough uses 6-ball stack (sw61-sw66). STTNG has dual photon cannon mechanisms with motor solenoids and position-tracking switches. Borg lock is a separate ball stack device. Lamp vpx_names derived from NFadeLm/NFadeL calls in UpdateLamps.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.sttng`: `games/sttng.json` at the pinned migration revision.
