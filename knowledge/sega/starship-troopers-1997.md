# Starship Troopers

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Sega (1997). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/sst.json#/switches/0._vbscript_name`: sw9
- `games/sst.json#/switches/0._inferred_type`: rollover
- `games/sst.json#/switches/0._note`: Controller.Switch on/off; also calls WireRampOff
- `games/sst.json#/switches/1._vbscript_name`: sw10
- `games/sst.json#/switches/1._inferred_type`: scoop
- `games/sst.json#/switches/1._note`: PulseSw 10; ball destroyed by timer then added to bsSuperVUK after 1800ms delay
- `games/sst.json#/switches/2._inferred_type`: trough
- `games/sst.json#/switches/2._note`: bsTrough.InitSw position 5 (4th ball)
- `games/sst.json#/switches/3._inferred_type`: trough
- `games/sst.json#/switches/3._note`: bsTrough.InitSw position 4
- `games/sst.json#/switches/4._inferred_type`: trough
- `games/sst.json#/switches/4._note`: bsTrough.InitSw position 3
- `games/sst.json#/switches/5._inferred_type`: trough
- `games/sst.json#/switches/5._note`: bsTrough.InitSw position 2 (first ball stacks here)
- `games/sst.json#/switches/6._vbscript_name`: sw16
- `games/sst.json#/switches/6._inferred_type`: rollover
- `games/sst.json#/switches/6._note`: Controller.Switch on/off
- `games/sst.json#/switches/7._vbscript_name`: T17
- `games/sst.json#/switches/7._inferred_type`: drop_target
- `games/sst.json#/switches/7._note`: vpmTimer.PulseSw 17
- `games/sst.json#/switches/8._vbscript_name`: T18
- `games/sst.json#/switches/8._inferred_type`: drop_target
- `games/sst.json#/switches/8._note`: vpmTimer.PulseSw 18
- `games/sst.json#/switches/9._vbscript_name`: T19
- `games/sst.json#/switches/9._inferred_type`: drop_target
- `games/sst.json#/switches/9._note`: vpmTimer.PulseSw 19
- `games/sst.json#/switches/10._vbscript_name`: T20
- `games/sst.json#/switches/10._inferred_type`: drop_target
- `games/sst.json#/switches/10._note`: vpmTimer.PulseSw 20
- `games/sst.json#/switches/11._vbscript_name`: T21
- `games/sst.json#/switches/11._inferred_type`: drop_target
- `games/sst.json#/switches/11._note`: vpmTimer.PulseSw 21
- `games/sst.json#/switches/12._vbscript_name`: T22
- `games/sst.json#/switches/12._inferred_type`: drop_target
- `games/sst.json#/switches/12._note`: vpmTimer.PulseSw 22
- `games/sst.json#/switches/13._vbscript_name`: T23
- `games/sst.json#/switches/13._inferred_type`: drop_target
- `games/sst.json#/switches/13._note`: vpmTimer.PulseSw 23
- `games/sst.json#/switches/14._vbscript_name`: T24
- `games/sst.json#/switches/14._inferred_type`: drop_target
- `games/sst.json#/switches/14._note`: vpmTimer.PulseSw 24
- `games/sst.json#/switches/15._vbscript_name`: sw25
- `games/sst.json#/switches/15._inferred_type`: standup_target
- `games/sst.json#/switches/15._note`: vpmTimer.PulseSw 25
- `games/sst.json#/switches/16._vbscript_name`: sw26
- `games/sst.json#/switches/16._inferred_type`: ramp_switch
- `games/sst.json#/switches/16._note`: PulseSw 26; calls WireRampOff on hit, WireRampOn on unhit
- `games/sst.json#/switches/17._vbscript_name`: T27
- `games/sst.json#/switches/17._inferred_type`: drop_target
- `games/sst.json#/switches/17._note`: vpmTimer.PulseSw 27
- `games/sst.json#/switches/18._vbscript_name`: T28
- `games/sst.json#/switches/18._inferred_type`: drop_target
- `games/sst.json#/switches/18._note`: vpmTimer.PulseSw 28
- `games/sst.json#/switches/19._vbscript_name`: T29
- `games/sst.json#/switches/19._inferred_type`: drop_target
- `games/sst.json#/switches/19._note`: vpmTimer.PulseSw 29
- `games/sst.json#/switches/20._vbscript_name`: T30
- `games/sst.json#/switches/20._inferred_type`: drop_target
- `games/sst.json#/switches/20._note`: vpmTimer.PulseSw 30
- `games/sst.json#/switches/21._vbscript_name`: T31
- `games/sst.json#/switches/21._inferred_type`: drop_target
- `games/sst.json#/switches/21._note`: vpmTimer.PulseSw 31
- `games/sst.json#/switches/22._vbscript_name`: T32
- `games/sst.json#/switches/22._inferred_type`: drop_target
- `games/sst.json#/switches/22._note`: vpmTimer.PulseSw 32
- `games/sst.json#/switches/23._inferred_type`: opto
- `games/sst.json#/switches/23._note`: mBug.AddSw 33,221,222 — warrior bug stepper mech fully extended position
- `games/sst.json#/switches/24._inferred_type`: opto
- `games/sst.json#/switches/24._note`: mBug.AddSw 34,0,1 — warrior bug stepper mech fully retracted position
- `games/sst.json#/switches/25._vbscript_name`: BWalls
- `games/sst.json#/switches/25._inferred_type`: standup_target
- `games/sst.json#/switches/25._note`: vpmTimer.PulseSw 35; BWalls_Hit collection handler
- `games/sst.json#/switches/26._inferred_type`: opto
- `games/sst.json#/switches/26._note`: Set directly by SolBrainBug(7) — Controller.Switch(37)=True when brain bug raised
- `games/sst.json#/switches/27._vbscript_name`: sw38
- `games/sst.json#/switches/27._inferred_type`: standup_target
- `games/sst.json#/switches/27._note`: PulseSw 38 via timer; drop target that becomes active when brain bug is raised
- `games/sst.json#/switches/28._inferred_type`: opto
- `games/sst.json#/switches/28._note`: Set directly by SolBrainBug(7) — Controller.Switch(39)=True when brain bug raised
- `games/sst.json#/switches/29._vbscript_name`: sw40
- `games/sst.json#/switches/29._inferred_type`: rollover
- `games/sst.json#/switches/29._note`: Controller.Switch on/off
- `games/sst.json#/switches/30._vbscript_name`: sw41
- `games/sst.json#/switches/30._inferred_type`: rollover
- `games/sst.json#/switches/30._note`: Controller.Switch on/off
- `games/sst.json#/switches/31._vbscript_name`: sw42
- `games/sst.json#/switches/31._inferred_type`: rollover
- `games/sst.json#/switches/31._note`: Controller.Switch on/off
- `games/sst.json#/switches/32._vbscript_name`: sw43
- `games/sst.json#/switches/32._inferred_type`: rollover
- `games/sst.json#/switches/32._note`: Controller.Switch on/off
- `games/sst.json#/switches/33._vbscript_name`: sw45
- `games/sst.json#/switches/33._inferred_type`: vuk
- `games/sst.json#/switches/33._note`: bsLeftVUK cvpmSaucer; InitKicker sw45, 45, 131, 15, 15
- `games/sst.json#/switches/34._vbscript_name`: sw46
- `games/sst.json#/switches/34._inferred_type`: vuk
- `games/sst.json#/switches/34._note`: bsSuperVUK cvpmBallStack; InitSw 0,46,0,0,0,0,0,0; InitKick sw46,182,72
- `games/sst.json#/switches/35._vbscript_name`: sw47
- `games/sst.json#/switches/35._inferred_type`: rollover
- `games/sst.json#/switches/35._note`: Controller.Switch on/off
- `games/sst.json#/switches/36._vbscript_name`: sw48
- `games/sst.json#/switches/36._inferred_type`: rollover
- `games/sst.json#/switches/36._note`: Controller.Switch on/off
- `games/sst.json#/switches/37._vbscript_name`: Bumper1
- `games/sst.json#/switches/37._inferred_type`: bumper
- `games/sst.json#/switches/37._note`: vpmTimer.PulseSw 49
- `games/sst.json#/switches/38._vbscript_name`: Bumper3
- `games/sst.json#/switches/38._inferred_type`: bumper
- `games/sst.json#/switches/38._note`: vpmTimer.PulseSw 50
- `games/sst.json#/switches/39._vbscript_name`: Bumper2
- `games/sst.json#/switches/39._inferred_type`: bumper
- `games/sst.json#/switches/39._note`: vpmTimer.PulseSw 51
- `games/sst.json#/switches/40._vbscript_name`: sw52
- `games/sst.json#/switches/40._inferred_type`: standup_target
- `games/sst.json#/switches/40._note`: vpmTimer.PulseSw 52
- `games/sst.json#/switches/41._vbscript_name`: sw53
- `games/sst.json#/switches/41._inferred_type`: standup_target
- `games/sst.json#/switches/41._note`: vpmTimer.PulseSw 53
- `games/sst.json#/switches/42._inferred_type`: tilt
- `games/sst.json#/switches/42._note`: vpmNudge.TiltSwitch = 56
- `games/sst.json#/switches/43._vbscript_name`: sw57
- `games/sst.json#/switches/43._inferred_type`: rollover
- `games/sst.json#/switches/43._note`: Controller.Switch on/off
- `games/sst.json#/switches/44._vbscript_name`: sw58
- `games/sst.json#/switches/44._inferred_type`: rollover
- `games/sst.json#/switches/44._note`: Controller.Switch on/off; applies inlane slowdown (vely*0.8)
- `games/sst.json#/switches/45._vbscript_name`: Rightslingshot
- `games/sst.json#/switches/45._inferred_type`: slingshot
- `games/sst.json#/switches/45._note`: vpmTimer.PulseSw 59 in Rightslingshot_Slingshot event
- `games/sst.json#/switches/46._vbscript_name`: sw60
- `games/sst.json#/switches/46._inferred_type`: rollover
- `games/sst.json#/switches/46._note`: Controller.Switch on/off
- `games/sst.json#/switches/47._vbscript_name`: sw61
- `games/sst.json#/switches/47._inferred_type`: rollover
- `games/sst.json#/switches/47._note`: Controller.Switch on/off; applies inlane slowdown (vely*0.8)
- `games/sst.json#/switches/48._vbscript_name`: Leftslingshot
- `games/sst.json#/switches/48._inferred_type`: slingshot
- `games/sst.json#/switches/48._note`: vpmTimer.PulseSw 62 in Leftslingshot_Slingshot event
- `games/sst.json#/switches/49._inferred_type`: cabinet_switch
- `games/sst.json#/switches/49._note`: Controller.Switch(88) set by RightMagnaSave/LockbarKey keydown/keyup; triggers mini flipper SolRFlipperS
- `games/sst.json#/coils/0._vbscript_callback`: SolRelease
- `games/sst.json#/coils/0._inferred_type`: ball_management
- `games/sst.json#/coils/0._note`: bsTrough.ExitSol_On — kicks ball from trough to shooter lane
- `games/sst.json#/coils/1._vbscript_callback`: SolAutolaunch
- `games/sst.json#/coils/1._inferred_type`: autoplunger
- `games/sst.json#/coils/1._note`: Fires plunger via Plunger.AutoPlunger and Plunger.Fire
- `games/sst.json#/coils/2._vbscript_callback`: SolLeftVuk
- `games/sst.json#/coils/2._inferred_type`: vuk
- `games/sst.json#/coils/2._note`: bsLeftVUK.ExitSol_On — ejects from left VUK (sw45)
- `games/sst.json#/coils/3._vbscript_callback`: bsSupervuk.SolOut
- `games/sst.json#/coils/3._inferred_type`: vuk
- `games/sst.json#/coils/3._note`: bsSuperVUK standard eject — kicks from sw46
- `games/sst.json#/coils/4._vbscript_callback`: SolLeftMagnet
- `games/sst.json#/coils/4._inferred_type`: magnet
- `games/sst.json#/coils/4._note`: cvpmMagnet; InitMagnet LeftMagnet, 30; GrabCenter=1
- `games/sst.json#/coils/5._vbscript_callback`: SolRightMagnet
- `games/sst.json#/coils/5._inferred_type`: magnet
- `games/sst.json#/coils/5._note`: cvpmMagnet; InitMagnet RightMagnet, 30; GrabCenter=1
- `games/sst.json#/coils/6._vbscript_callback`: SolBrainBug
- `games/sst.json#/coils/6._inferred_type`: mechanism
- `games/sst.json#/coils/6._note`: Raises/lowers brain bug assembly; sets Controller.Switch 37/39 directly; controls sw38/sw38a drop state
- `games/sst.json#/coils/7._vbscript_callback`: SolKnocker
- `games/sst.json#/coils/7._inferred_type`: knocker
- `games/sst.json#/coils/8._vbscript_callback`: SolRFlipperS
- `games/sst.json#/coils/8._inferred_type`: flipper
- `games/sst.json#/coils/8._note`: Commented out SolCallback — controlled directly via LockbarKey/RightMagnaSave keybinding to switch 88
- `games/sst.json#/coils/9._vbscript_callback`: FlippersEnabled=
- `games/sst.json#/coils/9._inferred_type`: flipper_relay
- `games/sst.json#/coils/9._note`: Enables/disables flipper response
- `games/sst.json#/coils/10._inferred_type`: mechanism
- `games/sst.json#/coils/10._note`: cvpmMyMech Sol1=17; Steps=222, Length=600ms; controls warrior bug raise/lower with switches 33/34
- `games/sst.json#/coils/11._vbscript_callback`: SetLamp 123,
- `games/sst.json#/coils/11._inferred_type`: flasher
- `games/sst.json#/coils/11._note`: Routes to lamp 123 via SetLamp for fading flasher control
- `games/sst.json#/coils/12._vbscript_callback`: Sol25
- `games/sst.json#/coils/12._inferred_type`: flasher
- `games/sst.json#/coils/12._note`: FlashBlinkingRed / FlashoffRed
- `games/sst.json#/coils/13._vbscript_callback`: Sol26
- `games/sst.json#/coils/13._inferred_type`: flasher
- `games/sst.json#/coils/13._note`: FlashBlinkingYellow / FlashoffYellow
- `games/sst.json#/coils/14._vbscript_callback`: Sol27
- `games/sst.json#/coils/14._inferred_type`: flasher
- `games/sst.json#/coils/14._note`: FlashBlinkingGreen / FlashoffGreen
- `games/sst.json#/coils/15._vbscript_callback`: Sol28
- `games/sst.json#/coils/15._inferred_type`: flasher
- `games/sst.json#/coils/15._note`: FlashBlinkingBlue / FlashoffBlue
- `games/sst.json#/coils/16._vbscript_callback`: SetLamp 129,
- `games/sst.json#/coils/16._inferred_type`: flasher
- `games/sst.json#/coils/16._note`: Routes to lamp 129 via SetLamp; X4 multiplied flasher
- `games/sst.json#/coils/17._vbscript_callback`: SetLamp 130,
- `games/sst.json#/coils/17._inferred_type`: flasher
- `games/sst.json#/coils/17._note`: Routes to lamp 130 via SetLamp; X4 multiplied flasher
- `games/sst.json#/coils/18._vbscript_callback`: SetLamp 131,
- `games/sst.json#/coils/18._inferred_type`: flasher
- `games/sst.json#/coils/18._note`: Routes to lamp 131 via SetLamp; X4 multiplied flasher
- `games/sst.json#/coils/19._vbscript_callback`: SetLamp 132,
- `games/sst.json#/coils/19._inferred_type`: flasher
- `games/sst.json#/coils/19._note`: Routes to lamp 132 via SetLamp; X2 multiplied flasher
- `games/sst.json#/coils/20._vbscript_name`: sLRFlipper
- `games/sst.json#/coils/20._vbscript_callback`: SolRFlipper
- `games/sst.json#/coils/20._inferred_type`: flipper
- `games/sst.json#/coils/20._note`: Framework constant (core.vbs: sLRFlipper=46); nFozzy physics
- `games/sst.json#/coils/21._vbscript_name`: sLLFlipper
- `games/sst.json#/coils/21._vbscript_callback`: SolLFlipper
- `games/sst.json#/coils/21._inferred_type`: flipper
- `games/sst.json#/coils/21._note`: Framework constant (core.vbs: sLLFlipper=48); nFozzy physics
- `games/sst.json#/lamps/0._inferred_type`: insert
- `games/sst.json#/lamps/1._inferred_type`: insert
- `games/sst.json#/lamps/2._inferred_type`: insert
- `games/sst.json#/lamps/3._inferred_type`: insert
- `games/sst.json#/lamps/4._inferred_type`: insert
- `games/sst.json#/lamps/5._inferred_type`: insert
- `games/sst.json#/lamps/6._inferred_type`: insert
- `games/sst.json#/lamps/7._inferred_type`: insert
- `games/sst.json#/lamps/8._inferred_type`: insert
- `games/sst.json#/lamps/9._inferred_type`: insert
- `games/sst.json#/lamps/10._inferred_type`: insert
- `games/sst.json#/lamps/11._inferred_type`: insert
- `games/sst.json#/lamps/12._inferred_type`: insert
- `games/sst.json#/lamps/13._inferred_type`: insert
- `games/sst.json#/lamps/14._inferred_type`: insert
- `games/sst.json#/lamps/15._inferred_type`: insert
- `games/sst.json#/lamps/16._inferred_type`: insert
- `games/sst.json#/lamps/17._inferred_type`: insert
- `games/sst.json#/lamps/18._inferred_type`: insert
- `games/sst.json#/lamps/19._inferred_type`: insert
- `games/sst.json#/lamps/20._inferred_type`: insert
- `games/sst.json#/lamps/21._inferred_type`: insert
- `games/sst.json#/lamps/22._inferred_type`: insert
- `games/sst.json#/lamps/23._inferred_type`: insert
- `games/sst.json#/lamps/24._inferred_type`: insert
- `games/sst.json#/lamps/25._inferred_type`: insert
- `games/sst.json#/lamps/26._inferred_type`: insert
- `games/sst.json#/lamps/27._inferred_type`: insert
- `games/sst.json#/lamps/28._inferred_type`: insert
- `games/sst.json#/lamps/29._inferred_type`: insert
- `games/sst.json#/lamps/30._inferred_type`: insert
- `games/sst.json#/lamps/31._inferred_type`: insert
- `games/sst.json#/lamps/32._inferred_type`: insert
- `games/sst.json#/lamps/33._inferred_type`: insert
- `games/sst.json#/lamps/34._inferred_type`: insert
- `games/sst.json#/lamps/35._inferred_type`: insert
- `games/sst.json#/lamps/36._inferred_type`: insert
- `games/sst.json#/lamps/37._inferred_type`: insert
- `games/sst.json#/lamps/38._inferred_type`: insert
- `games/sst.json#/lamps/39._inferred_type`: insert
- `games/sst.json#/lamps/40._inferred_type`: insert
- `games/sst.json#/lamps/41._inferred_type`: insert
- `games/sst.json#/lamps/42._inferred_type`: insert
- `games/sst.json#/lamps/43._inferred_type`: insert
- `games/sst.json#/lamps/44._inferred_type`: insert
- `games/sst.json#/lamps/45._inferred_type`: insert
- `games/sst.json#/lamps/46._inferred_type`: insert
- `games/sst.json#/lamps/47._inferred_type`: insert
- `games/sst.json#/lamps/48._inferred_type`: insert
- `games/sst.json#/lamps/49._inferred_type`: insert
- `games/sst.json#/lamps/50._inferred_type`: insert
- `games/sst.json#/lamps/51._inferred_type`: insert
- `games/sst.json#/lamps/52._inferred_type`: insert
- `games/sst.json#/lamps/53._inferred_type`: insert
- `games/sst.json#/lamps/54._inferred_type`: insert
- `games/sst.json#/lamps/55._inferred_type`: insert
- `games/sst.json#/lamps/56._inferred_type`: insert
- `games/sst.json#/lamps/57._inferred_type`: insert
- `games/sst.json#/lamps/58._inferred_type`: insert
- `games/sst.json#/lamps/59._inferred_type`: insert
- `games/sst.json#/lamps/60._inferred_type`: insert
- `games/sst.json#/lamps/61._inferred_type`: insert
- `games/sst.json#/lamps/62._inferred_type`: insert
- `games/sst.json#/lamps/63._inferred_type`: insert
- `games/sst.json#/lamps/64._inferred_type`: insert
- `games/sst.json#/lamps/65._inferred_type`: insert
- `games/sst.json#/lamps/66._inferred_type`: insert
- `games/sst.json#/lamps/67._inferred_type`: insert
- `games/sst.json#/lamps/68._inferred_type`: insert
- `games/sst.json#/lamps/69._inferred_type`: insert
- `games/sst.json#/lamps/70._inferred_type`: insert
- `games/sst.json#/lamps/71._inferred_type`: insert
- `games/sst.json#/lamps/72._inferred_type`: insert
- `games/sst.json#/lamps/73._inferred_type`: insert
- `games/sst.json#/lamps/74._inferred_type`: insert
- `games/sst.json#/lamps/75._inferred_type`: insert
- `games/sst.json#/lamps/76._inferred_type`: insert
- `games/sst.json#/lamps/77._inferred_type`: insert
- `games/sst.json#/lamps/78._inferred_type`: flasher
- `games/sst.json#/lamps/78._note`: Brain Bug Flasher — controlled by coil 23 via SetLamp 123
- `games/sst.json#/lamps/79._inferred_type`: flasher
- `games/sst.json#/lamps/79._note`: Warrior Bug Sled Flasher (F5) — controlled by coil 29 via SetLamp 129; X4
- `games/sst.json#/lamps/80._inferred_type`: flasher
- `games/sst.json#/lamps/80._note`: Left Ramp Flasher (F6) — controlled by coil 30 via SetLamp 130; X4
- `games/sst.json#/lamps/81._inferred_type`: flasher
- `games/sst.json#/lamps/81._note`: Right Ramp Flasher (F7) — controlled by coil 31 via SetLamp 131; X4
- `games/sst.json#/lamps/82._inferred_type`: flasher
- `games/sst.json#/lamps/82._note`: Pop Bumpers Flasher (F8) — controlled by coil 32 via SetLamp 132; X2
- `games/sst.json#/lamps/83._inferred_type`: gi
- `games/sst.json#/lamps/83._note`: General Illumination — single GI string; GICallback(0); 28 light objects (Light001-Light028) + 5 flasher objects
- `games/sst.json#/_source/confidence_notes`: High confidence on switches/coils from VPW VBScript. Sega Whitestar platform (sega.vbs). Trough is standard cvpmBallStack with 4 balls and switches 15/14/13/12. Warrior bug uses cvpmMyMech (custom stepper class) with Sol1=17, position switches 33/34. BrainBug opto switches 37/39 set directly via Controller.Switch in SolBrainBug handler. Mini flipper (sol 14) commented out in script but present in SolRFlipperS sub — controlled via LockbarKey/RightMagnaSave binding to switch 88. Flasher coils 23/25-32 use SetLamp to virtual lamp numbers 123/129-132 for fading. Lamp IDs from UpdateLamps sub using JP's flasher fading system. GI is single string on lamp 200 via GICallback(0). Framework flipper constants from core.vbs (sLRFlipper=46, sLLFlipper=48).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.sst`: `games/sst.json` at the pinned migration revision.
