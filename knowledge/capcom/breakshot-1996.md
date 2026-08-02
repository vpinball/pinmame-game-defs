# Breakshot

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Capcom (1996). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/brkshot.json#/switches/0._vbscript_callback`: vpmNudge.TiltSwitch
- `games/brkshot.json#/switches/0._inferred_type`: tilt
- `games/brkshot.json#/switches/1._vbscript_name`: sw35
- `games/brkshot.json#/switches/1._inferred_type`: trough
- `games/brkshot.json#/switches/2._vbscript_name`: sw36
- `games/brkshot.json#/switches/2._inferred_type`: trough
- `games/brkshot.json#/switches/3._vbscript_name`: sw37
- `games/brkshot.json#/switches/3._inferred_type`: trough
- `games/brkshot.json#/switches/4._vbscript_name`: sw38
- `games/brkshot.json#/switches/4._inferred_type`: trough
- `games/brkshot.json#/switches/5._vbscript_name`: RightSlingShot
- `games/brkshot.json#/switches/5._inferred_type`: slingshot
- `games/brkshot.json#/switches/5._note`: Tween-animated; switch set to 1 on sling fire, 0 on return
- `games/brkshot.json#/switches/6._vbscript_name`: LeftSlingShot
- `games/brkshot.json#/switches/6._inferred_type`: slingshot
- `games/brkshot.json#/switches/6._note`: Tween-animated; switch set to 1 on sling fire, 0 on return
- `games/brkshot.json#/switches/7._vbscript_name`: SW43
- `games/brkshot.json#/switches/7._inferred_type`: rollover
- `games/brkshot.json#/switches/7._note`: Plunger lane rollover, not baked
- `games/brkshot.json#/switches/8._vbscript_name`: SW44
- `games/brkshot.json#/switches/8._inferred_type`: rollover
- `games/brkshot.json#/switches/9._vbscript_name`: SW45
- `games/brkshot.json#/switches/9._inferred_type`: rollover
- `games/brkshot.json#/switches/10._vbscript_name`: SW46
- `games/brkshot.json#/switches/10._inferred_type`: rollover
- `games/brkshot.json#/switches/11._vbscript_name`: SW47
- `games/brkshot.json#/switches/11._inferred_type`: rollover
- `games/brkshot.json#/switches/12._vbscript_name`: sw48
- `games/brkshot.json#/switches/12._inferred_type`: drop_target
- `games/brkshot.json#/switches/13._vbscript_name`: sw49
- `games/brkshot.json#/switches/13._inferred_type`: drop_target
- `games/brkshot.json#/switches/14._vbscript_name`: sw50
- `games/brkshot.json#/switches/14._inferred_type`: drop_target
- `games/brkshot.json#/switches/15._vbscript_name`: sw51
- `games/brkshot.json#/switches/15._inferred_type`: standup_target
- `games/brkshot.json#/switches/16._vbscript_name`: SW53
- `games/brkshot.json#/switches/16._inferred_type`: opto
- `games/brkshot.json#/switches/17._vbscript_name`: SW54
- `games/brkshot.json#/switches/17._inferred_type`: opto
- `games/brkshot.json#/switches/18._vbscript_name`: sw55
- `games/brkshot.json#/switches/18._inferred_type`: standup_target
- `games/brkshot.json#/switches/19._vbscript_name`: Bumper3
- `games/brkshot.json#/switches/19._vbscript_callback`: vpmTimer.PulseSw(57)
- `games/brkshot.json#/switches/19._inferred_type`: bumper
- `games/brkshot.json#/switches/20._vbscript_name`: Bumper2
- `games/brkshot.json#/switches/20._vbscript_callback`: vpmTimer.PulseSw(58)
- `games/brkshot.json#/switches/20._inferred_type`: bumper
- `games/brkshot.json#/switches/21._vbscript_name`: Bumper1
- `games/brkshot.json#/switches/21._vbscript_callback`: vpmTimer.PulseSw(59)
- `games/brkshot.json#/switches/21._inferred_type`: bumper
- `games/brkshot.json#/switches/22._vbscript_name`: SW60
- `games/brkshot.json#/switches/22._inferred_type`: rollover
- `games/brkshot.json#/switches/23._vbscript_name`: SW61
- `games/brkshot.json#/switches/23._inferred_type`: rollover
- `games/brkshot.json#/switches/24._vbscript_name`: SW62
- `games/brkshot.json#/switches/24._inferred_type`: rollover
- `games/brkshot.json#/switches/25._vbscript_name`: SW63
- `games/brkshot.json#/switches/25._inferred_type`: rollover
- `games/brkshot.json#/switches/26._vbscript_name`: SW65
- `games/brkshot.json#/switches/26._inferred_type`: opto
- `games/brkshot.json#/switches/27._vbscript_callback`: Controller.Switch(66)
- `games/brkshot.json#/switches/27._inferred_type`: mechanism
- `games/brkshot.json#/switches/27._note`: Center post position switch; 1=up, 0=down. Controlled by solenoids 12 (up) and 14 (release)
- `games/brkshot.json#/switches/28._vbscript_name`: sw67
- `games/brkshot.json#/switches/28._inferred_type`: kicker
- `games/brkshot.json#/switches/29._vbscript_name`: sw68
- `games/brkshot.json#/switches/29._inferred_type`: kicker
- `games/brkshot.json#/switches/30._vbscript_name`: sw69
- `games/brkshot.json#/switches/30._inferred_type`: kicker
- `games/brkshot.json#/switches/31._vbscript_name`: sw70
- `games/brkshot.json#/switches/31._inferred_type`: kicker
- `games/brkshot.json#/switches/32._vbscript_name`: sw73
- `games/brkshot.json#/switches/32._inferred_type`: drop_target
- `games/brkshot.json#/switches/33._vbscript_name`: sw74
- `games/brkshot.json#/switches/33._inferred_type`: drop_target
- `games/brkshot.json#/switches/34._vbscript_name`: sw75
- `games/brkshot.json#/switches/34._inferred_type`: drop_target
- `games/brkshot.json#/switches/35._vbscript_name`: sw76
- `games/brkshot.json#/switches/35._inferred_type`: standup_target
- `games/brkshot.json#/switches/36._vbscript_name`: sw77
- `games/brkshot.json#/switches/36._inferred_type`: standup_target
- `games/brkshot.json#/switches/37._vbscript_name`: sw78
- `games/brkshot.json#/switches/37._inferred_type`: standup_target
- `games/brkshot.json#/switches/38._vbscript_name`: SW79
- `games/brkshot.json#/switches/38._inferred_type`: rollover
- `games/brkshot.json#/coils/0._vbscript_callback`: SolTrough
- `games/brkshot.json#/coils/0._inferred_type`: ball_management
- `games/brkshot.json#/coils/0._note`: Kicks ball from sw35 drain toward trough stack
- `games/brkshot.json#/coils/1._vbscript_callback`: SolRelease
- `games/brkshot.json#/coils/1._inferred_type`: ball_management
- `games/brkshot.json#/coils/1._note`: Kicks ball from sw36 trough to plunger lane
- `games/brkshot.json#/coils/2._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/brkshot.json#/coils/2._inferred_type`: knocker
- `games/brkshot.json#/coils/3._vbscript_callback`: framework-driven
- `games/brkshot.json#/coils/3._inferred_type`: slingshot
- `games/brkshot.json#/coils/3._note`: Hardware-driven by CAPCOM.VBS framework; commented in script but not assigned via SolCallback
- `games/brkshot.json#/coils/4._vbscript_callback`: framework-driven
- `games/brkshot.json#/coils/4._inferred_type`: slingshot
- `games/brkshot.json#/coils/4._note`: Hardware-driven by CAPCOM.VBS framework; commented in script but not assigned via SolCallback
- `games/brkshot.json#/coils/5._vbscript_callback`: Kickback
- `games/brkshot.json#/coils/5._inferred_type`: kicker
- `games/brkshot.json#/coils/6._vbscript_callback`: ResetDropsRight
- `games/brkshot.json#/coils/6._inferred_type`: drop_target_reset
- `games/brkshot.json#/coils/6._note`: Resets drop targets sw48, sw49, sw50
- `games/brkshot.json#/coils/7._vbscript_callback`: RightSaucer
- `games/brkshot.json#/coils/7._inferred_type`: kicker
- `games/brkshot.json#/coils/7._note`: Ejects ball from right VUK (sw67)
- `games/brkshot.json#/coils/8._vbscript_name`: sLRFlipper
- `games/brkshot.json#/coils/8._vbscript_callback`: SolLRFlipper
- `games/brkshot.json#/coils/8._inferred_type`: flipper
- `games/brkshot.json#/coils/8._note`: Framework-defined constant (CAPCOM.VBS: sLRFlipper=9)
- `games/brkshot.json#/coils/9._vbscript_name`: sURFlipper
- `games/brkshot.json#/coils/9._vbscript_callback`: SolURFlipper
- `games/brkshot.json#/coils/9._inferred_type`: flipper
- `games/brkshot.json#/coils/9._note`: Framework-defined constant (CAPCOM.VBS: sURFlipper=10). Despite name, drives the upper right flipper
- `games/brkshot.json#/coils/10._vbscript_name`: sLLFlipper
- `games/brkshot.json#/coils/10._vbscript_callback`: SolLLFlipper
- `games/brkshot.json#/coils/10._inferred_type`: flipper
- `games/brkshot.json#/coils/10._note`: Framework-defined constant (CAPCOM.VBS: sLLFlipper=11). Despite Capcom naming as 'Upper Right', drives the lower right flipper in VPX
- `games/brkshot.json#/coils/11._vbscript_callback`: PostUp
- `games/brkshot.json#/coils/11._inferred_type`: mechanism
- `games/brkshot.json#/coils/11._note`: Raises center post; sets sw66=1 when fully up
- `games/brkshot.json#/coils/12._vbscript_callback`: ResetDropsLeft
- `games/brkshot.json#/coils/12._inferred_type`: drop_target_reset
- `games/brkshot.json#/coils/12._note`: Resets drop targets sw73, sw74, sw75
- `games/brkshot.json#/coils/13._vbscript_callback`: PostRelease
- `games/brkshot.json#/coils/13._inferred_type`: mechanism
- `games/brkshot.json#/coils/13._note`: Drops center post; sets sw66=0 when down. Also triggered during power-up
- `games/brkshot.json#/coils/14._vbscript_callback`: SolRightGate
- `games/brkshot.json#/coils/14._inferred_type`: gate
- `games/brkshot.json#/coils/15._vbscript_callback`: SolLeftGate
- `games/brkshot.json#/coils/15._inferred_type`: gate
- `games/brkshot.json#/coils/16._vbscript_callback`: CLeftPocket
- `games/brkshot.json#/coils/16._inferred_type`: kicker
- `games/brkshot.json#/coils/16._note`: Ejects ball from center left kicker (sw68)
- `games/brkshot.json#/coils/17._vbscript_callback`: CenterPocket
- `games/brkshot.json#/coils/17._inferred_type`: kicker
- `games/brkshot.json#/coils/17._note`: Ejects ball from center center kicker (sw69)
- `games/brkshot.json#/coils/18._vbscript_callback`: FlashLight
- `games/brkshot.json#/coils/18._inferred_type`: flasher
- `games/brkshot.json#/coils/18._note`: SolModCallback (PWM). Controls s128a and s128b light objects plus BL_Flashers lightmap tinting
- `games/brkshot.json#/coils/19._vbscript_callback`: framework-driven
- `games/brkshot.json#/coils/19._inferred_type`: bumper
- `games/brkshot.json#/coils/19._note`: Hardware-driven by CAPCOM.VBS framework; commented in script
- `games/brkshot.json#/coils/20._vbscript_callback`: framework-driven
- `games/brkshot.json#/coils/20._inferred_type`: bumper
- `games/brkshot.json#/coils/20._note`: Hardware-driven by CAPCOM.VBS framework; commented in script
- `games/brkshot.json#/coils/21._vbscript_callback`: framework-driven
- `games/brkshot.json#/coils/21._inferred_type`: bumper
- `games/brkshot.json#/coils/21._note`: Hardware-driven by CAPCOM.VBS framework; commented in script
- `games/brkshot.json#/coils/22._vbscript_callback`: CRightPocket
- `games/brkshot.json#/coils/22._inferred_type`: kicker
- `games/brkshot.json#/coils/22._note`: Ejects ball from center right kicker (sw70)
- `games/brkshot.json#/lamps/0._vbscript_name`: l3
- `games/brkshot.json#/lamps/0._inferred_type`: insert
- `games/brkshot.json#/lamps/1._vbscript_name`: l4
- `games/brkshot.json#/lamps/1._inferred_type`: insert
- `games/brkshot.json#/lamps/2._vbscript_name`: l5
- `games/brkshot.json#/lamps/2._inferred_type`: insert
- `games/brkshot.json#/lamps/3._vbscript_name`: l6
- `games/brkshot.json#/lamps/3._inferred_type`: insert
- `games/brkshot.json#/lamps/4._vbscript_name`: l7
- `games/brkshot.json#/lamps/4._inferred_type`: insert
- `games/brkshot.json#/lamps/5._vbscript_name`: l8
- `games/brkshot.json#/lamps/5._inferred_type`: insert
- `games/brkshot.json#/lamps/6._vbscript_name`: l9
- `games/brkshot.json#/lamps/6._inferred_type`: insert
- `games/brkshot.json#/lamps/7._vbscript_name`: l10
- `games/brkshot.json#/lamps/7._inferred_type`: insert
- `games/brkshot.json#/lamps/8._vbscript_name`: l11
- `games/brkshot.json#/lamps/8._inferred_type`: insert
- `games/brkshot.json#/lamps/9._vbscript_name`: l12
- `games/brkshot.json#/lamps/9._inferred_type`: insert
- `games/brkshot.json#/lamps/10._vbscript_name`: l13
- `games/brkshot.json#/lamps/10._inferred_type`: insert
- `games/brkshot.json#/lamps/11._vbscript_name`: l14
- `games/brkshot.json#/lamps/11._inferred_type`: insert
- `games/brkshot.json#/lamps/12._vbscript_name`: l15
- `games/brkshot.json#/lamps/12._inferred_type`: insert
- `games/brkshot.json#/lamps/13._vbscript_name`: l16
- `games/brkshot.json#/lamps/13._inferred_type`: insert
- `games/brkshot.json#/lamps/14._vbscript_name`: l17
- `games/brkshot.json#/lamps/14._inferred_type`: insert
- `games/brkshot.json#/lamps/15._vbscript_name`: l18
- `games/brkshot.json#/lamps/15._inferred_type`: insert
- `games/brkshot.json#/lamps/16._vbscript_name`: l19
- `games/brkshot.json#/lamps/16._inferred_type`: insert
- `games/brkshot.json#/lamps/17._vbscript_name`: l20
- `games/brkshot.json#/lamps/17._inferred_type`: insert
- `games/brkshot.json#/lamps/18._vbscript_name`: l21
- `games/brkshot.json#/lamps/18._inferred_type`: insert
- `games/brkshot.json#/lamps/19._vbscript_name`: l22
- `games/brkshot.json#/lamps/19._inferred_type`: insert
- `games/brkshot.json#/lamps/20._vbscript_name`: l23
- `games/brkshot.json#/lamps/20._inferred_type`: insert
- `games/brkshot.json#/lamps/21._vbscript_name`: l24
- `games/brkshot.json#/lamps/21._inferred_type`: insert
- `games/brkshot.json#/lamps/22._vbscript_name`: l25
- `games/brkshot.json#/lamps/22._inferred_type`: insert
- `games/brkshot.json#/lamps/22._note`: Has custom AdjustBulbTint animation callback
- `games/brkshot.json#/lamps/23._vbscript_name`: l26
- `games/brkshot.json#/lamps/23._inferred_type`: insert
- `games/brkshot.json#/lamps/23._note`: Has custom AdjustBulbTint animation callback
- `games/brkshot.json#/lamps/24._vbscript_name`: l27
- `games/brkshot.json#/lamps/24._inferred_type`: insert
- `games/brkshot.json#/lamps/25._vbscript_name`: l28
- `games/brkshot.json#/lamps/25._inferred_type`: insert
- `games/brkshot.json#/lamps/26._vbscript_name`: l29
- `games/brkshot.json#/lamps/26._inferred_type`: insert
- `games/brkshot.json#/lamps/27._vbscript_name`: l30
- `games/brkshot.json#/lamps/27._inferred_type`: insert
- `games/brkshot.json#/lamps/28._vbscript_name`: l31
- `games/brkshot.json#/lamps/28._inferred_type`: insert
- `games/brkshot.json#/lamps/29._vbscript_name`: l32
- `games/brkshot.json#/lamps/29._inferred_type`: insert
- `games/brkshot.json#/lamps/30._vbscript_name`: l33
- `games/brkshot.json#/lamps/30._inferred_type`: insert
- `games/brkshot.json#/lamps/31._vbscript_name`: l34
- `games/brkshot.json#/lamps/31._inferred_type`: insert
- `games/brkshot.json#/lamps/32._vbscript_name`: l35
- `games/brkshot.json#/lamps/32._inferred_type`: insert
- `games/brkshot.json#/lamps/33._vbscript_name`: l36
- `games/brkshot.json#/lamps/33._inferred_type`: insert
- `games/brkshot.json#/lamps/34._vbscript_name`: l37
- `games/brkshot.json#/lamps/34._inferred_type`: insert
- `games/brkshot.json#/lamps/35._vbscript_name`: l38
- `games/brkshot.json#/lamps/35._inferred_type`: insert
- `games/brkshot.json#/lamps/36._vbscript_name`: l39
- `games/brkshot.json#/lamps/36._inferred_type`: insert
- `games/brkshot.json#/lamps/37._vbscript_name`: l40
- `games/brkshot.json#/lamps/37._inferred_type`: insert
- `games/brkshot.json#/lamps/38._vbscript_name`: l41
- `games/brkshot.json#/lamps/38._inferred_type`: insert
- `games/brkshot.json#/lamps/39._vbscript_name`: l42
- `games/brkshot.json#/lamps/39._inferred_type`: insert
- `games/brkshot.json#/lamps/40._vbscript_name`: l43
- `games/brkshot.json#/lamps/40._inferred_type`: insert
- `games/brkshot.json#/lamps/41._vbscript_name`: l44
- `games/brkshot.json#/lamps/41._inferred_type`: insert
- `games/brkshot.json#/lamps/42._vbscript_name`: l45
- `games/brkshot.json#/lamps/42._inferred_type`: insert
- `games/brkshot.json#/lamps/43._vbscript_name`: l46
- `games/brkshot.json#/lamps/43._inferred_type`: insert
- `games/brkshot.json#/lamps/44._vbscript_name`: l47
- `games/brkshot.json#/lamps/44._inferred_type`: insert
- `games/brkshot.json#/lamps/45._vbscript_name`: l48
- `games/brkshot.json#/lamps/45._inferred_type`: insert
- `games/brkshot.json#/lamps/46._vbscript_name`: l49
- `games/brkshot.json#/lamps/46._inferred_type`: insert
- `games/brkshot.json#/lamps/47._vbscript_name`: l50
- `games/brkshot.json#/lamps/47._inferred_type`: insert
- `games/brkshot.json#/lamps/48._vbscript_name`: l51
- `games/brkshot.json#/lamps/48._inferred_type`: insert
- `games/brkshot.json#/lamps/49._vbscript_name`: l52
- `games/brkshot.json#/lamps/49._inferred_type`: insert
- `games/brkshot.json#/lamps/50._vbscript_name`: l53
- `games/brkshot.json#/lamps/50._inferred_type`: insert
- `games/brkshot.json#/lamps/51._vbscript_name`: l54
- `games/brkshot.json#/lamps/51._inferred_type`: insert
- `games/brkshot.json#/lamps/52._vbscript_name`: l55
- `games/brkshot.json#/lamps/52._inferred_type`: insert
- `games/brkshot.json#/lamps/53._vbscript_name`: l56
- `games/brkshot.json#/lamps/53._inferred_type`: insert
- `games/brkshot.json#/lamps/54._vbscript_name`: l57
- `games/brkshot.json#/lamps/54._inferred_type`: insert
- `games/brkshot.json#/lamps/55._vbscript_name`: l58
- `games/brkshot.json#/lamps/55._inferred_type`: insert
- `games/brkshot.json#/lamps/56._vbscript_name`: l59
- `games/brkshot.json#/lamps/56._inferred_type`: insert
- `games/brkshot.json#/lamps/57._vbscript_name`: l60
- `games/brkshot.json#/lamps/57._inferred_type`: insert
- `games/brkshot.json#/lamps/58._vbscript_name`: l61
- `games/brkshot.json#/lamps/58._inferred_type`: insert
- `games/brkshot.json#/lamps/59._vbscript_name`: l62
- `games/brkshot.json#/lamps/59._inferred_type`: insert
- `games/brkshot.json#/lamps/60._vbscript_name`: l63
- `games/brkshot.json#/lamps/60._inferred_type`: insert
- `games/brkshot.json#/lamps/61._vbscript_name`: l64
- `games/brkshot.json#/lamps/61._inferred_type`: insert
- `games/brkshot.json#/_source/confidence_notes`: High confidence on switches/coils. Capcom platform using CAPCOM.VBS. Flipper solenoid constants (sLRFlipper=9, sURFlipper=10, sLLFlipper=11) are framework-defined in CAPCOM.VBS. UseLamps=1 with vpmMapLights AllLamps means VPX light numbers match lamp IDs. UseGI=0 means GI not routed through PinMAME. Physical trough is manual kicker-based (sw35=drain, sw36/37/38=trough stack) with no bsTrough/cvpmTrough object. SolModCallback(28) is PWM flasher. Solenoids 4/5 (slingshots) and 29/30/31 (bumpers) are hardware-driven by CAPCOM.VBS framework, not assigned via SolCallback. Slingshot switches 41/42 are tween-animated. Drop targets use DTArray helper class. Standup targets use STArray helper class. Optos at sw53/54/65. No spinner switch found in script (sound-only reference). No named switch constants (Const sw*) in table script.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.brkshot`: `games/brkshot.json` at the pinned migration revision.
