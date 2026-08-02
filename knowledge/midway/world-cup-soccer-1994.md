# World Cup Soccer

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Midway (1994). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/wcs.json#/switches/0._vbscript_name`: swCoin1
- `games/wcs.json#/switches/0._inferred_type`: cabinet
- `games/wcs.json#/switches/0._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/1._vbscript_name`: swCoin2
- `games/wcs.json#/switches/1._inferred_type`: cabinet
- `games/wcs.json#/switches/1._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/2._vbscript_name`: swCoin3
- `games/wcs.json#/switches/2._inferred_type`: cabinet
- `games/wcs.json#/switches/2._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/3._vbscript_name`: swCoin4
- `games/wcs.json#/switches/3._inferred_type`: cabinet
- `games/wcs.json#/switches/3._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/4._vbscript_name`: swCancel
- `games/wcs.json#/switches/4._inferred_type`: cabinet
- `games/wcs.json#/switches/4._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/5._vbscript_name`: swDown
- `games/wcs.json#/switches/5._inferred_type`: cabinet
- `games/wcs.json#/switches/5._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/6._vbscript_name`: swUp
- `games/wcs.json#/switches/6._inferred_type`: cabinet
- `games/wcs.json#/switches/6._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/7._vbscript_name`: swEnter
- `games/wcs.json#/switches/7._inferred_type`: cabinet
- `games/wcs.json#/switches/7._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/8._vbscript_name`: Controller.Switch(12)
- `games/wcs.json#/switches/8._inferred_type`: button
- `games/wcs.json#/switches/8._note`: Activated via LeftMagnaSave keycode
- `games/wcs.json#/switches/9._vbscript_name`: vpmNudge.TiltSwitch
- `games/wcs.json#/switches/9._inferred_type`: cabinet
- `games/wcs.json#/switches/9._note`: Set via vpmNudge.TiltSwitch = 14
- `games/wcs.json#/switches/10._vbscript_name`: sw15
- `games/wcs.json#/switches/10._inferred_type`: rollover
- `games/wcs.json#/switches/11._vbscript_name`: sw16
- `games/wcs.json#/switches/11._inferred_type`: rollover
- `games/wcs.json#/switches/11._note`: Also has target T16 pulsing sw16
- `games/wcs.json#/switches/12._vbscript_name`: sw17
- `games/wcs.json#/switches/12._inferred_type`: rollover
- `games/wcs.json#/switches/13._vbscript_name`: sw18
- `games/wcs.json#/switches/13._inferred_type`: rollover
- `games/wcs.json#/switches/14._vbscript_name`: Controller.Switch(22)
- `games/wcs.json#/switches/14._inferred_type`: cabinet
- `games/wcs.json#/switches/14._note`: Set to 1 at init
- `games/wcs.json#/switches/15._vbscript_name`: Controller.Switch(23)
- `games/wcs.json#/switches/15._inferred_type`: button
- `games/wcs.json#/switches/15._note`: Activated via keycode 3
- `games/wcs.json#/switches/16._vbscript_name`: Controller.Switch(24)
- `games/wcs.json#/switches/16._inferred_type`: cabinet
- `games/wcs.json#/switches/16._note`: Set to 1 at init
- `games/wcs.json#/switches/17._vbscript_name`: T25
- `games/wcs.json#/switches/17._inferred_type`: target
- `games/wcs.json#/switches/17._note`: PulseSw 25 on T25_Hit
- `games/wcs.json#/switches/18._vbscript_name`: sw26
- `games/wcs.json#/switches/18._inferred_type`: rollover
- `games/wcs.json#/switches/19._vbscript_name`: sw27spinner
- `games/wcs.json#/switches/19._inferred_type`: spinner
- `games/wcs.json#/switches/19._note`: PulseSw 27 on sw27spinner_Spin
- `games/wcs.json#/switches/20._vbscript_name`: T28
- `games/wcs.json#/switches/20._inferred_type`: target
- `games/wcs.json#/switches/20._note`: PulseSw 28 on T28_Hit
- `games/wcs.json#/switches/21._vbscript_name`: bsTrough.InitSw
- `games/wcs.json#/switches/21._inferred_type`: trough
- `games/wcs.json#/switches/21._note`: bsTrough.InitSw 0, 31, 32, 33, 34, 35, 0, 0
- `games/wcs.json#/switches/22._vbscript_name`: bsTrough.InitSw
- `games/wcs.json#/switches/22._inferred_type`: trough
- `games/wcs.json#/switches/22._note`: bsTrough.InitSw 0, 31, 32, 33, 34, 35, 0, 0
- `games/wcs.json#/switches/23._vbscript_name`: bsTrough.InitSw
- `games/wcs.json#/switches/23._inferred_type`: trough
- `games/wcs.json#/switches/23._note`: bsTrough.InitSw 0, 31, 32, 33, 34, 35, 0, 0
- `games/wcs.json#/switches/24._vbscript_name`: bsTrough.InitSw
- `games/wcs.json#/switches/24._inferred_type`: trough
- `games/wcs.json#/switches/24._note`: bsTrough.InitSw 0, 31, 32, 33, 34, 35, 0, 0
- `games/wcs.json#/switches/25._vbscript_name`: bsTrough.InitSw
- `games/wcs.json#/switches/25._inferred_type`: trough
- `games/wcs.json#/switches/25._note`: bsTrough.InitSw 0, 31, 32, 33, 34, 35, 0, 0
- `games/wcs.json#/switches/26._vbscript_name`: vpmTimer.PulseSw 36
- `games/wcs.json#/switches/26._inferred_type`: ball_release
- `games/wcs.json#/switches/26._note`: Pulsed in SolRelease when ball exits trough
- `games/wcs.json#/switches/27._vbscript_name`: T37
- `games/wcs.json#/switches/27._inferred_type`: target
- `games/wcs.json#/switches/27._note`: PulseSw 37 on T37_Hit
- `games/wcs.json#/switches/28._vbscript_name`: sw38
- `games/wcs.json#/switches/28._inferred_type`: rollover
- `games/wcs.json#/switches/28._note`: Controller.Switch set; triggers CheckBallCount after 1000ms
- `games/wcs.json#/switches/29._vbscript_name`: sw41
- `games/wcs.json#/switches/29._inferred_type`: target
- `games/wcs.json#/switches/29._note`: PulseSw 41 on sw41_Hit; plays goal sounds
- `games/wcs.json#/switches/30._vbscript_name`: sw42
- `games/wcs.json#/switches/30._inferred_type`: vuk
- `games/wcs.json#/switches/30._note`: bsGoalPopper.InitSw 0, 42; VUK kicker
- `games/wcs.json#/switches/31._vbscript_name`: mGoalie.AddSw 43
- `games/wcs.json#/switches/31._inferred_type`: mech
- `games/wcs.json#/switches/31._note`: mGoalie.AddSw 43, 60, 79 -- goalie mech position switch
- `games/wcs.json#/switches/32._vbscript_name`: mGoalie.AddSw 44
- `games/wcs.json#/switches/32._inferred_type`: mech
- `games/wcs.json#/switches/32._note`: mGoalie.AddSw 44, 0, 20 -- goalie mech position switch
- `games/wcs.json#/switches/33._vbscript_name`: sw45
- `games/wcs.json#/switches/33._inferred_type`: vuk
- `games/wcs.json#/switches/33._note`: bsTVPopper.InitSw 0, 45; VUK kicker
- `games/wcs.json#/switches/34._vbscript_name`: sw47
- `games/wcs.json#/switches/34._inferred_type`: rollover
- `games/wcs.json#/switches/35._vbscript_name`: vpmTimer.PulseSw 48
- `games/wcs.json#/switches/35._inferred_type`: target
- `games/wcs.json#/switches/35._note`: PulseSw 48 on GWalls_Hit -- goalie wall collision
- `games/wcs.json#/switches/36._vbscript_name`: sw51
- `games/wcs.json#/switches/36._inferred_type`: rollover
- `games/wcs.json#/switches/36._note`: PulseSw 51; skill shot target
- `games/wcs.json#/switches/37._vbscript_name`: sw52
- `games/wcs.json#/switches/37._inferred_type`: rollover
- `games/wcs.json#/switches/37._note`: PulseSw 52; skill shot target
- `games/wcs.json#/switches/38._vbscript_name`: sw53
- `games/wcs.json#/switches/38._inferred_type`: rollover
- `games/wcs.json#/switches/38._note`: PulseSw 53; skill shot target
- `games/wcs.json#/switches/39._vbscript_name`: sw54
- `games/wcs.json#/switches/39._inferred_type`: saucer
- `games/wcs.json#/switches/39._note`: bsRightEjectHole.InitKicker sw54, 54
- `games/wcs.json#/switches/40._vbscript_name`: sw55
- `games/wcs.json#/switches/40._inferred_type`: saucer
- `games/wcs.json#/switches/40._note`: bsUpperEjectHole.InitKicker sw55, 55
- `games/wcs.json#/switches/41._vbscript_name`: sw56
- `games/wcs.json#/switches/41._inferred_type`: saucer
- `games/wcs.json#/switches/41._note`: bsLeftEjectHole.InitKicker sw56, 56
- `games/wcs.json#/switches/42._vbscript_name`: sw61
- `games/wcs.json#/switches/42._inferred_type`: rollover
- `games/wcs.json#/switches/42._note`: PulseSw 61; animates Rollover81
- `games/wcs.json#/switches/43._vbscript_name`: sw62
- `games/wcs.json#/switches/43._inferred_type`: rollover
- `games/wcs.json#/switches/43._note`: PulseSw 62; animates Rollover82
- `games/wcs.json#/switches/44._vbscript_name`: sw63
- `games/wcs.json#/switches/44._inferred_type`: rollover
- `games/wcs.json#/switches/44._note`: PulseSw 63; animates Rollover83
- `games/wcs.json#/switches/45._vbscript_name`: sw64
- `games/wcs.json#/switches/45._inferred_type`: rollover
- `games/wcs.json#/switches/45._note`: PulseSw 64; animates Rollover84
- `games/wcs.json#/switches/46._vbscript_name`: sw65
- `games/wcs.json#/switches/46._inferred_type`: target
- `games/wcs.json#/switches/46._note`: PulseSw 65; TackleSW per comment
- `games/wcs.json#/switches/47._vbscript_name`: T66
- `games/wcs.json#/switches/47._inferred_type`: target
- `games/wcs.json#/switches/47._note`: PulseSw 66 on T66_Hit
- `games/wcs.json#/switches/48._vbscript_name`: T67
- `games/wcs.json#/switches/48._inferred_type`: target
- `games/wcs.json#/switches/48._note`: PulseSw 67 on T67_Hit
- `games/wcs.json#/switches/49._vbscript_name`: sw71
- `games/wcs.json#/switches/49._inferred_type`: rollover
- `games/wcs.json#/switches/49._note`: PulseSw 71; left_ramp_made_L per comment
- `games/wcs.json#/switches/50._vbscript_name`: sw72
- `games/wcs.json#/switches/50._inferred_type`: spinner
- `games/wcs.json#/switches/50._note`: Controller.Switch set; left_ramp_entry per comment
- `games/wcs.json#/switches/51._vbscript_name`: sw74
- `games/wcs.json#/switches/51._inferred_type`: rollover
- `games/wcs.json#/switches/51._note`: PulseSw 74; left_ramp_made_R per comment
- `games/wcs.json#/switches/52._vbscript_name`: sw75
- `games/wcs.json#/switches/52._inferred_type`: spinner
- `games/wcs.json#/switches/52._note`: Controller.Switch set; right_ramp_entry per comment
- `games/wcs.json#/switches/53._vbscript_name`: sw76
- `games/wcs.json#/switches/53._inferred_type`: rollover
- `games/wcs.json#/switches/53._note`: Controller.Switch set; minipf per comment; adjusts BallCount
- `games/wcs.json#/switches/54._vbscript_name`: sw77
- `games/wcs.json#/switches/54._inferred_type`: rollover
- `games/wcs.json#/switches/54._note`: Controller.Switch set; minipf per comment
- `games/wcs.json#/switches/55._vbscript_name`: sw78
- `games/wcs.json#/switches/55._inferred_type`: rollover
- `games/wcs.json#/switches/55._note`: PulseSw 78; right_ramp_made per comment
- `games/wcs.json#/switches/56._vbscript_name`: Bumper1
- `games/wcs.json#/switches/56._inferred_type`: bumper
- `games/wcs.json#/switches/56._note`: PulseSw 81 on Bumper1_Hit
- `games/wcs.json#/switches/57._vbscript_name`: Bumper2
- `games/wcs.json#/switches/57._inferred_type`: bumper
- `games/wcs.json#/switches/57._note`: PulseSw 82 on Bumper2_Hit
- `games/wcs.json#/switches/58._vbscript_name`: Bumper3
- `games/wcs.json#/switches/58._inferred_type`: bumper
- `games/wcs.json#/switches/58._note`: PulseSw 83 on Bumper3_Hit
- `games/wcs.json#/switches/59._vbscript_name`: SlingShotLeft
- `games/wcs.json#/switches/59._inferred_type`: slingshot
- `games/wcs.json#/switches/59._note`: PulseSw 84 on SlingShotLeft_Slingshot
- `games/wcs.json#/switches/60._vbscript_name`: SlingShotRight
- `games/wcs.json#/switches/60._inferred_type`: slingshot
- `games/wcs.json#/switches/60._note`: PulseSw 85 on SlingShotRight_Slingshot
- `games/wcs.json#/switches/61._vbscript_name`: sw86
- `games/wcs.json#/switches/61._inferred_type`: rollover
- `games/wcs.json#/switches/62._vbscript_name`: sw87
- `games/wcs.json#/switches/62._inferred_type`: rollover
- `games/wcs.json#/switches/63._vbscript_name`: sw88
- `games/wcs.json#/switches/63._inferred_type`: rollover
- `games/wcs.json#/switches/64._vbscript_name`: swLRFlip
- `games/wcs.json#/switches/64._inferred_type`: cabinet
- `games/wcs.json#/switches/64._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/65._vbscript_name`: swLLFlip
- `games/wcs.json#/switches/65._inferred_type`: cabinet
- `games/wcs.json#/switches/65._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/66._vbscript_name`: swURFlip
- `games/wcs.json#/switches/66._inferred_type`: cabinet
- `games/wcs.json#/switches/66._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/switches/67._vbscript_name`: swULFlip
- `games/wcs.json#/switches/67._inferred_type`: cabinet
- `games/wcs.json#/switches/67._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/coils/0._vbscript_callback`: bsgoalpopper.SolOut
- `games/wcs.json#/coils/0._inferred_type`: vuk
- `games/wcs.json#/coils/1._vbscript_callback`: SolTvPopper
- `games/wcs.json#/coils/1._inferred_type`: vuk
- `games/wcs.json#/coils/1._note`: Originally bstvpopper.SolOut, overridden with custom sub
- `games/wcs.json#/coils/2._vbscript_callback`: KickBack
- `games/wcs.json#/coils/2._inferred_type`: kickback
- `games/wcs.json#/coils/3._vbscript_callback`: LockRelease
- `games/wcs.json#/coils/3._inferred_type`: post
- `games/wcs.json#/coils/4._vbscript_callback`: SolUpperEjectHole
- `games/wcs.json#/coils/4._inferred_type`: saucer
- `games/wcs.json#/coils/4._note`: Originally bsupperejecthole.SolOut, overridden with custom sub
- `games/wcs.json#/coils/5._vbscript_callback`: SolRelease
- `games/wcs.json#/coils/5._inferred_type`: ball_release
- `games/wcs.json#/coils/6._vbscript_callback`: bsrightejecthole.SolOut
- `games/wcs.json#/coils/6._inferred_type`: saucer
- `games/wcs.json#/coils/7._vbscript_callback`: bsleftejecthole.SolOut
- `games/wcs.json#/coils/7._inferred_type`: saucer
- `games/wcs.json#/coils/8._vbscript_callback`: RampDiverter
- `games/wcs.json#/coils/8._inferred_type`: diverter
- `games/wcs.json#/coils/8._note`: Diverter_Hold; originally SolCallback(8), reassigned to 16
- `games/wcs.json#/coils/9._vbscript_callback`: SetModLamp 117,
- `games/wcs.json#/coils/9._inferred_type`: flasher
- `games/wcs.json#/coils/9._note`: Modulated solenoid; maps to lamp 117 (goalcagetop)
- `games/wcs.json#/coils/10._vbscript_callback`: SetModLamp 118,
- `games/wcs.json#/coils/10._inferred_type`: flasher
- `games/wcs.json#/coils/10._note`: Modulated solenoid; maps to lamp 118 (goal)
- `games/wcs.json#/coils/11._vbscript_callback`: SetModLamp 119,
- `games/wcs.json#/coils/11._inferred_type`: flasher
- `games/wcs.json#/coils/11._note`: Modulated solenoid; maps to lamp 119 (skillshot)
- `games/wcs.json#/coils/12._vbscript_callback`: SetModLamp 120,
- `games/wcs.json#/coils/12._inferred_type`: flasher
- `games/wcs.json#/coils/12._note`: Modulated solenoid; maps to lamp 120 (jetbumpers)
- `games/wcs.json#/coils/13._vbscript_callback`: mGoalie.Sol1
- `games/wcs.json#/coils/13._inferred_type`: motor
- `games/wcs.json#/coils/13._note`: cvpmMech single-sol goalie mechanism; vpmMechLinear + vpmMechReverse + vpmMechOneSol
- `games/wcs.json#/coils/14._vbscript_callback`: SetModLamp 122,
- `games/wcs.json#/coils/14._inferred_type`: flasher
- `games/wcs.json#/coils/14._note`: Modulated solenoid; maps to lamp 122 (spinningball)
- `games/wcs.json#/coils/15._vbscript_callback`: ttBall.SolMotorState True,
- `games/wcs.json#/coils/15._inferred_type`: motor
- `games/wcs.json#/coils/15._note`: mBall.Sol1=23; ball_clockwise for spinnerDisk
- `games/wcs.json#/coils/16._vbscript_callback`: ttBall.SolMotorState False,
- `games/wcs.json#/coils/16._inferred_type`: motor
- `games/wcs.json#/coils/16._note`: mBall.Sol2=24; ball_counter_clockwise for spinnerDisk
- `games/wcs.json#/coils/17._vbscript_callback`: SetModLamp 125,
- `games/wcs.json#/coils/17._inferred_type`: flasher
- `games/wcs.json#/coils/17._note`: Modulated solenoid; maps to lamp 125 (leftramp_entrance)
- `games/wcs.json#/coils/18._vbscript_callback`: SetModLamp 126,
- `games/wcs.json#/coils/18._inferred_type`: flasher
- `games/wcs.json#/coils/18._note`: Modulated solenoid; maps to lamp 126 (lock_area)
- `games/wcs.json#/coils/19._vbscript_callback`: SetModLamp 127,
- `games/wcs.json#/coils/19._inferred_type`: flasher
- `games/wcs.json#/coils/19._note`: Modulated solenoid; maps to lamp 127 (flipper_lanes)
- `games/wcs.json#/coils/20._vbscript_callback`: SetModLamp 128,
- `games/wcs.json#/coils/20._inferred_type`: flasher
- `games/wcs.json#/coils/20._note`: Modulated solenoid; maps to lamp 128 (ramp_rear)
- `games/wcs.json#/coils/21._vbscript_name`: GameOnSolenoid
- `games/wcs.json#/coils/21._inferred_type`: system
- `games/wcs.json#/coils/21._note`: WPC framework constant from WPC.vbs
- `games/wcs.json#/coils/22._vbscript_callback`: SolGoalieMagnet
- `games/wcs.json#/coils/22._inferred_type`: magnet
- `games/wcs.json#/coils/22._note`: Originally mGoalieMagnet.MagnetOn=, overridden with SolGoalieMagnet sound sub
- `games/wcs.json#/coils/23._vbscript_callback`: LoopGate
- `games/wcs.json#/coils/23._inferred_type`: gate
- `games/wcs.json#/coils/24._vbscript_callback`: SolLockMagnet
- `games/wcs.json#/coils/24._inferred_type`: magnet
- `games/wcs.json#/coils/25._vbscript_callback`: SolRFlipper
- `games/wcs.json#/coils/25._vbscript_name`: sLRFlipper
- `games/wcs.json#/coils/25._inferred_type`: flipper
- `games/wcs.json#/coils/25._note`: core.vbs framework constant sLRFlipper = 46
- `games/wcs.json#/coils/26._vbscript_callback`: SolLFlipper
- `games/wcs.json#/coils/26._vbscript_name`: sLLFlipper
- `games/wcs.json#/coils/26._inferred_type`: flipper
- `games/wcs.json#/coils/26._note`: core.vbs framework constant sLLFlipper = 48
- `games/wcs.json#/lamps/24._note`: Multiple VPX objects: lf41/lf41a
- `games/wcs.json#/lamps/25._note`: Multiple VPX objects: lf42/lf42a
- `games/wcs.json#/lamps/26._note`: Multiple VPX objects: lf43/lf43a
- `games/wcs.json#/lamps/29._note`: Multiple VPX objects: lf46/lf46a
- `games/wcs.json#/lamps/30._note`: Multiple VPX objects: lf47/lf47a
- `games/wcs.json#/lamps/31._note`: Multiple VPX objects: l48/l48a
- `games/wcs.json#/lamps/47._note`: Multiple VPX objects: l68/l68a/l68b
- `games/wcs.json#/lamps/48._note`: Multiple VPX objects: l71/l71a
- `games/wcs.json#/lamps/55._note`: Multiple VPX objects: l78/l78a
- `games/wcs.json#/lamps/60._note`: Multiple VPX objects: l85/l85a/l85b
- `games/wcs.json#/lamps/61._note`: Multiple VPX objects: l86/l86a/l86b
- `games/wcs.json#/lamps/62._inferred_type`: flasher
- `games/wcs.json#/lamps/62._note`: Driven by SolModCallBack(17). VPX objects: l117/f117/f117a
- `games/wcs.json#/lamps/63._inferred_type`: flasher
- `games/wcs.json#/lamps/63._note`: Driven by SolModCallBack(18). VPX objects: f118a
- `games/wcs.json#/lamps/64._inferred_type`: flasher
- `games/wcs.json#/lamps/64._note`: Driven by SolModCallBack(19). VPX objects: l119a/f119/f119a/f119c/f119e
- `games/wcs.json#/lamps/65._inferred_type`: flasher
- `games/wcs.json#/lamps/65._note`: Driven by SolModCallBack(20); shares VPX object lf47a. VPX objects: lf47a
- `games/wcs.json#/lamps/66._inferred_type`: flasher
- `games/wcs.json#/lamps/66._note`: Driven by SolModCallBack(22). VPX objects: f122a/f122b
- `games/wcs.json#/lamps/67._inferred_type`: flasher
- `games/wcs.json#/lamps/67._note`: Driven by SolModCallBack(25). VPX objects: f125
- `games/wcs.json#/lamps/68._inferred_type`: flasher
- `games/wcs.json#/lamps/68._note`: Driven by SolModCallBack(26). VPX objects: l126/f126a/f126b/f126c
- `games/wcs.json#/lamps/69._inferred_type`: flasher
- `games/wcs.json#/lamps/69._note`: Driven by SolModCallBack(27). VPX objects: f127
- `games/wcs.json#/lamps/70._inferred_type`: flasher
- `games/wcs.json#/lamps/70._note`: Driven by SolModCallBack(28). VPX objects: l128a/l128b/f128a/f128b/f128c/f128d/f128e/f128f
- `games/wcs.json#/_source/confidence_notes`: High confidence on switches, coils, and lamps. No Const sw* or Const s* declarations in table script -- all switch/coil IDs are hardcoded numeric in Controller.Switch(), vpmTimer.PulseSw(), SolCallback(), and ball stack init calls. Lamp numbers extracted from UpdateLamps() flash/flashm/lampmod/flashmod calls. Flipper solenoid IDs (sLRFlipper=46, sLLFlipper=48) from core.vbs framework. WPC platform confirmed via LoadVPM wpc.VBS. Trough config uses 5 balls with switches 31-35. Goalie and soccer ball mechs use cvpmMech with solenoids 21,23,24. Some commented-out SolCallback lines preserved as notes.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.wcs`: `games/wcs.json` at the pinned migration revision.
