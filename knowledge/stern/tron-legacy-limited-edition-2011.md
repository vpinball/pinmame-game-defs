# TRON Legacy - Limited Edition

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2011). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/sam.json#/coils/2`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/sam.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/tron-legacy.json#/switches/0._note`: cvpmDropTarget DTBank4. sw01_Hit calls DTBank4.Hit 4. Part of 4-bank drop target.
- `games/tron-legacy.json#/switches/1._note`: cvpmDropTarget DTBank4. sw02_Hit calls DTBank4.Hit 3.
- `games/tron-legacy.json#/switches/2._note`: cvpmDropTarget DTBank4. sw03_Hit calls DTBank4.Hit 2.
- `games/tron-legacy.json#/switches/3._note`: cvpmDropTarget DTBank4. sw04_Hit calls DTBank4.Hit 1.
- `games/tron-legacy.json#/switches/4._note`: PulseSw 7. Has animated primitive sw7p with TransX displacement on hit.
- `games/tron-legacy.json#/switches/5._note`: PulseSw 8. Has animated primitive sw8p with TransX displacement on hit.
- `games/tron-legacy.json#/switches/6._note`: bsRHole cvpmBallStack. sw11_Hit captures ball, animates Z descent, DestroyBall then bsRHole.AddBall. Kicked out by solenoid 4 (bsRHole.SolOut) at angle 200, force 24.
- `games/tron-legacy.json#/switches/7._note`: Controller.Switch(12) on/off via sw12_Hit/UnHit. Rollover-type switch on ramp entrance.
- `games/tron-legacy.json#/switches/8._note`: PulseSw 13. Has animated primitive sw13p with TransX displacement on hit.
- `games/tron-legacy.json#/switches/9._note`: Controller.Switch(14) on/off via sw14_Hit/UnHit.
- `games/tron-legacy.json#/switches/10._note`: Controller.Switch(16) = 0 in Table_KeyUp for StartGameKey. Standard SAM start button switch.
- `games/tron-legacy.json#/switches/11._note`: bsTrough.InitSw 0,21,20,19,18 — sw18 is position 4 (nearest eject/shooter lane). 4-ball trough.
- `games/tron-legacy.json#/switches/12._note`: bsTrough.InitSw 0,21,20,19,18 — sw19 is position 3.
- `games/tron-legacy.json#/switches/13._note`: bsTrough.InitSw 0,21,20,19,18 — sw20 is position 2.
- `games/tron-legacy.json#/switches/14._note`: bsTrough.InitSw 0,21,20,19,18 — sw21 is position 1 (nearest drain).
- `games/tron-legacy.json#/switches/15._note`: vpmTimer.PulseSw 22 called inside solTrough when ball is ejected from trough. Confirms ball reached shooter lane.
- `games/tron-legacy.json#/switches/16._note`: Controller.Switch(23) on/off via ShooterLane_Hit/Unhit. Also controls Lanelight1 state.
- `games/tron-legacy.json#/switches/17._note`: Controller.Switch(24) on/off via sw24_Hit/UnHit.
- `games/tron-legacy.json#/switches/18._note`: Controller.Switch(25) on/off via sw25_Hit/UnHit.
- `games/tron-legacy.json#/switches/19._note`: PulseSw 26. Fired from LeftSlingShot_Slingshot event. VPX physics-handled.
- `games/tron-legacy.json#/switches/20._note`: PulseSw 27. Fired from RightSlingShot_Slingshot event. VPX physics-handled.
- `games/tron-legacy.json#/switches/21._note`: Controller.Switch(28) on/off via sw28_Hit/UnHit.
- `games/tron-legacy.json#/switches/22._note`: Controller.Switch(29) on/off via sw29_Hit/UnHit.
- `games/tron-legacy.json#/switches/23._note`: PulseSw 30. Bumper2b_Hit. VPX physics-handled.
- `games/tron-legacy.json#/switches/24._note`: PulseSw 31. Bumper1b_Hit. VPX physics-handled.
- `games/tron-legacy.json#/switches/25._note`: PulseSw 32. Bumper3b_Hit. VPX physics-handled.
- `games/tron-legacy.json#/switches/26._note`: Controller.Switch(34) on/off via sw34_Hit/UnHit.
- `games/tron-legacy.json#/switches/27._note`: Controller.Switch(35) on/off via sw35_Hit/UnHit.
- `games/tron-legacy.json#/switches/28._note`: PulseSw 36 via sw36_Spin event. Spinner with SpinnerT1 primitive rotation tracking.
- `games/tron-legacy.json#/switches/29._note`: Controller.Switch(37) on/off via sw37_Hit/UnHit.
- `games/tron-legacy.json#/switches/30._note`: Controller.Switch(38) on/off via sw38_Hit/UnHit.
- `games/tron-legacy.json#/switches/31._note`: Controller.Switch(39) on/off via sw39_Hit/UnHit.
- `games/tron-legacy.json#/switches/32._note`: Controller.Switch(41) on/off via sw41_Hit/UnHit.
- `games/tron-legacy.json#/switches/33._note`: Controller.Switch(43) on/off via sw43_Hit/UnHit.
- `games/tron-legacy.json#/switches/34._note`: PulseSw 44 via sw44_Spin event. Spinner with SpinnerT4 primitive rotation tracking.
- `games/tron-legacy.json#/switches/35._note`: Controller.Switch(46) on/off via sw46_Hit/UnHit.
- `games/tron-legacy.json#/switches/36._note`: PulseSw 48. Has animated primitive sw48p with TransX displacement on hit.
- `games/tron-legacy.json#/switches/37._note`: PulseSw 49. Part of 3-target motor bank (sw49/50/51). Has animated primitives SW49P. Flasherswitch49 state toggles on hit. Targets only active when bank is raised (TBDown=0).
- `games/tron-legacy.json#/switches/38._note`: PulseSw 50. Part of 3-target motor bank. Has animated primitives SW50P. Flasherswitch50 state toggles on hit.
- `games/tron-legacy.json#/switches/39._note`: PulseSw 51. Part of 3-target motor bank. Has animated primitives SW51P. Flasherswitch51 state toggles on hit.
- `games/tron-legacy.json#/switches/40._note`: Controller.Switch(52) set by TBMove/TBTimer animation. =1 when bank is fully lowered (TBPos=29), =0 when bank is up (TBPos=0) or at step 26. Position switch for motor target bank mechanism.
- `games/tron-legacy.json#/switches/41._note`: Controller.Switch(53) set by TBMove/TBTimer animation. =1 when bank is fully raised (TBPos=0), =0 at step 2 and when lowered (TBPos=29). Position switch for motor target bank mechanism.
- `games/tron-legacy.json#/switches/42._note`: Controller.Switch(54) set by RecognizerTimer. =1 when recognizer.rotz >= 18 (rightmost position). Recognizer toy position switch.
- `games/tron-legacy.json#/switches/43._note`: Controller.Switch(55) set by RecognizerTimer. =1 when recognizer.rotz is approximately 0 (center). Recognizer toy position switch.
- `games/tron-legacy.json#/switches/44._note`: Controller.Switch(56) set by RecognizerTimer. =1 when recognizer.rotz <= -18 (leftmost position). Recognizer toy position switch.
- `games/tron-legacy.json#/coils/0._vbscript_callback`: solTrough
- `games/tron-legacy.json#/coils/0._inferred_type`: ball_management
- `games/tron-legacy.json#/coils/0._note`: solTrough calls bsTrough.ExitSol_On and vpmTimer.PulseSw 22 (shooter lane confirm). Ejects ball from 4-ball trough via BallRelease kicker at angle 90, force 8.
- `games/tron-legacy.json#/coils/1._vbscript_callback`: solAutofire
- `games/tron-legacy.json#/coils/1._inferred_type`: ball_management
- `games/tron-legacy.json#/coils/1._note`: SolAutofire sets AP=True, triggering PlungerPTimer loop which auto-fires via Plunger1. Uses cvpmImpulseP plungerIM initialized with swplunger VPX object.
- `games/tron-legacy.json#/coils/2._vbscript_callback`: DTBank4.SolDropUp
- `games/tron-legacy.json#/coils/2._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/2._note`: Resets 4-bank drop targets (sw01-sw04) via cvpmDropTarget framework.
- `games/tron-legacy.json#/coils/3._vbscript_callback`: bsRHole.SolOut
- `games/tron-legacy.json#/coils/3._inferred_type`: ball_management
- `games/tron-legacy.json#/coils/3._note`: Kicks ball out of right hole/arcade scoop (sw11). bsRHole.SolOut at angle 200, force 24, KickZ=0.4.
- `games/tron-legacy.json#/coils/4._vbscript_callback`: SolDiscMotor
- `games/tron-legacy.json#/coils/4._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/4._note`: Controls spinning disc toy via myTurnTable class (ttDisc1). When enabled, disc spins at stepAngle=Discdir (40 or -40 degrees). Disc1 primitive rotates. Direction controlled by separate discdirrelay (sol 22, commented out). Sound 'spindisc' plays while active.
- `games/tron-legacy.json#/coils/5._vbscript_callback`: TBMove
- `games/tron-legacy.json#/coils/5._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/5._note`: Controls rising/lowering motor target bank (sw49/50/51 targets). TBMove triggers TBTimer which animates MotorBank Z position through 29 steps. Sets position switches sw52 (down) and sw53 (up). At step 0 (raised): targets enabled, DPWall dropped. At step 28: targets disabled.
- `games/tron-legacy.json#/coils/6._vbscript_callback`: orbitpost
- `games/tron-legacy.json#/coils/6._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/6._note`: Controls UpPost drop wall. Enabled = UpPost.Isdropped=false (post raised). Disabled = UpPost.Isdropped=true (post down). Gates orbit shot.
- `games/tron-legacy.json#/coils/7._vbscript_callback`: shaker
- `games/tron-legacy.json#/coils/7._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/7._note`: COMMENTED OUT in VBS. SolCallback(8) = 'shaker'. Shaker motor — not implemented in this VPW mod.
- `games/tron-legacy.json#/coils/8._vbscript_callback`: SolLFlipper
- `games/tron-legacy.json#/coils/8._inferred_type`: flipper
- `games/tron-legacy.json#/coils/8._note`: nFozzy flipper implementation. LF.Fire on enable. Also drives LeftFlipper1 (upper left flipper primitive). SAM framework sol 15 = left flipper (InitVpmFFlipsSAM).
- `games/tron-legacy.json#/coils/9._vbscript_callback`: SolRFlipper
- `games/tron-legacy.json#/coils/9._inferred_type`: flipper
- `games/tron-legacy.json#/coils/9._note`: nFozzy flipper implementation. RF.Fire on enable. SAM framework sol 16 = right flipper (InitVpmFFlipsSAM).
- `games/tron-legacy.json#/coils/10._vbscript_callback`: SetLampMod 17,
- `games/tron-legacy.json#/coils/10._inferred_type`: flasher
- `games/tron-legacy.json#/coils/10._note`: SolModCallback PWM flasher. Comment says 'flash zen'. ModLampz drives F117 VPX flasher object.
- `games/tron-legacy.json#/coils/11._vbscript_callback`: SetLampMod 18,
- `games/tron-legacy.json#/coils/11._inferred_type`: flasher
- `games/tron-legacy.json#/coils/11._note`: SolModCallback PWM flasher. Comment says 'flash videogame'. ModLampz drives Flasher7, Monitorlicht1, Flasher7a VPX objects.
- `games/tron-legacy.json#/coils/12._vbscript_callback`: FlashSol19
- `games/tron-legacy.json#/coils/12._inferred_type`: flasher
- `games/tron-legacy.json#/coils/12._note`: SolModCallback with custom FlashSol19 sub driving dome flashers 5 and 6 (FlasherFlash5/6). Uses Hannibal's flasher dome system.
- `games/tron-legacy.json#/coils/13._vbscript_callback`: setLampMod 20,
- `games/tron-legacy.json#/coils/13._inferred_type`: flasher
- `games/tron-legacy.json#/coils/13._note`: SolModCallback PWM flasher. Comment says 'LE apron left'. ModLampz drives Lanelight VPX object.
- `games/tron-legacy.json#/coils/14._vbscript_callback`: setlampmod 21,
- `games/tron-legacy.json#/coils/14._inferred_type`: flasher
- `games/tron-legacy.json#/coils/14._note`: SolModCallback PWM flasher. Comment says 'LE apron right'. ModLampz drives Lanelight VPX object.
- `games/tron-legacy.json#/coils/15._vbscript_callback`: recogrelay
- `games/tron-legacy.json#/coils/15._inferred_type`: mechanism
- `games/tron-legacy.json#/coils/15._note`: Controls recognizer toy oscillation. When enabled, starts RecognizerTimer which sweeps recognizer.rotz between -20 and +20 degrees. Sets position switches sw54/55/56. Comment says 'LE recognizer'.
- `games/tron-legacy.json#/coils/16._vbscript_callback`: FlashSol25
- `games/tron-legacy.json#/coils/16._inferred_type`: flasher
- `games/tron-legacy.json#/coils/16._note`: SolModCallback with custom FlashSol25 sub driving dome flashers 3 and 4 (FlasherFlash3/4). Comment says 'flash right domes x2'.
- `games/tron-legacy.json#/coils/17._vbscript_callback`: SetLampMod 26,
- `games/tron-legacy.json#/coils/17._inferred_type`: flasher
- `games/tron-legacy.json#/coils/17._note`: SolModCallback PWM flasher. Comment says 'flash disc left'. ModLampz drives F126 VPX object.
- `games/tron-legacy.json#/coils/18._vbscript_callback`: SetLampMod 27,
- `games/tron-legacy.json#/coils/18._inferred_type`: flasher
- `games/tron-legacy.json#/coils/18._note`: SolModCallback PWM flasher. Comment says 'flash disc right'. ModLampz drives F127 VPX object.
- `games/tron-legacy.json#/coils/19._vbscript_callback`: FlashSol28
- `games/tron-legacy.json#/coils/19._inferred_type`: flasher
- `games/tron-legacy.json#/coils/19._note`: SolModCallback with custom FlashSol28 sub driving dome flashers 1 and 2 (FlasherFlash1/2). Comment says 'flash backpanel x2'.
- `games/tron-legacy.json#/coils/20._vbscript_callback`: SetLampMod 29,
- `games/tron-legacy.json#/coils/20._inferred_type`: flasher
- `games/tron-legacy.json#/coils/20._note`: SolModCallback PWM flasher. Comment says 'flash recognizer'. ModLampz drives f129 and f129a VPX objects.
- `games/tron-legacy.json#/coils/21._vbscript_callback`: SetLampMod 30,
- `games/tron-legacy.json#/coils/21._inferred_type`: flasher
- `games/tron-legacy.json#/coils/21._note`: SolModCallback PWM flasher. Comment says 'disc motor relay'. Not the actual disc motor (that's sol 5) — this is a flasher/lamp effect.
- `games/tron-legacy.json#/coils/22._vbscript_callback`: SetLampMod 31,
- `games/tron-legacy.json#/coils/22._inferred_type`: flasher
- `games/tron-legacy.json#/coils/22._note`: SolModCallback PWM flasher. Comment says 'flash red disc left x2'. ModLampz drives f131a and f131b VPX objects.
- `games/tron-legacy.json#/coils/23._vbscript_callback`: SetLampMod 32,
- `games/tron-legacy.json#/coils/23._inferred_type`: flasher
- `games/tron-legacy.json#/coils/23._note`: SolModCallback PWM flasher. Comment says 'LE flash red disc x2'. ModLampz drives f132a and f132b VPX objects.
- `games/tron-legacy.json#/lamps/0._note`: Also has l1a secondary light object.
- `games/tron-legacy.json#/lamps/1._note`: Also has l2a secondary light object.
- `games/tron-legacy.json#/lamps/2._note`: Also has l3a secondary light object.
- `games/tron-legacy.json#/lamps/3._note`: Also has l4a secondary light object.
- `games/tron-legacy.json#/lamps/4._note`: Also has l5a and f5TOP flasher primitive. DisableLighting callback on p5.
- `games/tron-legacy.json#/lamps/5._note`: Also has l6a and f6TOP flasher primitive. DisableLighting callback on p6.
- `games/tron-legacy.json#/lamps/6._note`: Also has l7a and f7TOP flasher primitive. DisableLighting callback on p7.
- `games/tron-legacy.json#/lamps/7._note`: Also has l8a and f8TOP flasher primitive. DisableLighting callback on p8.
- `games/tron-legacy.json#/lamps/8._note`: Also has l9a and f9TOP flasher primitive. DisableLighting callback on p9.
- `games/tron-legacy.json#/lamps/9._note`: Also has l10a and f10TOP flasher primitive. DisableLighting callback on p10.
- `games/tron-legacy.json#/lamps/10._note`: Also has l11a and f11top flasher primitive. DisableLighting callback on p11.
- `games/tron-legacy.json#/lamps/11._note`: Also has l12a and f12TOP flasher primitive. DisableLighting callback on p12.
- `games/tron-legacy.json#/lamps/12._note`: Also has l13a and f13TOP flasher primitive. DisableLighting callback on p13 (commented out).
- `games/tron-legacy.json#/lamps/13._note`: Also has l14a and f14top flasher primitive. DisableLighting callback on p14.
- `games/tron-legacy.json#/lamps/14._note`: Also has l15a. DisableLighting callback on p15.
- `games/tron-legacy.json#/lamps/15._note`: Also has l16a. DisableLighting callback on p16.
- `games/tron-legacy.json#/lamps/16._note`: Also has l17a and f17TOP flasher primitive. DisableLighting callback on p17.
- `games/tron-legacy.json#/lamps/17._note`: Also has l18a. DisableLighting callback on p18.
- `games/tron-legacy.json#/lamps/18._note`: Also has l19a. DisableLighting callback on p19 (commented out).
- `games/tron-legacy.json#/lamps/19._note`: Also has l20a and f20TOP flasher primitive. DisableLighting callback on p20.
- `games/tron-legacy.json#/lamps/20._note`: Also has l21a. DisableLighting callback on p21.
- `games/tron-legacy.json#/lamps/21._note`: Also has l22a and f22TOP flasher primitive. DisableLighting callback on p22.
- `games/tron-legacy.json#/lamps/22._note`: Also has l23a and f23TOP flasher primitive. DisableLighting callback on p23.
- `games/tron-legacy.json#/lamps/23._note`: Also has l24a and f24TOP flasher primitive. DisableLighting callback on p24.
- `games/tron-legacy.json#/lamps/24._note`: Also has l25a and f25TOP flasher primitive. DisableLighting callback on p25.
- `games/tron-legacy.json#/lamps/25._note`: Also has l26a and f26TOP flasher primitive. DisableLighting callback on p26.
- `games/tron-legacy.json#/lamps/26._note`: Also has l27a and f27TOP flasher primitive. DisableLighting callback on p27.
- `games/tron-legacy.json#/lamps/27._note`: Also has l28d and f28TOP flasher primitive. DisableLighting callback on p28 (commented out).
- `games/tron-legacy.json#/lamps/28._note`: Also has l29d and f29TOP flasher primitive. DisableLighting callback on p29.
- `games/tron-legacy.json#/lamps/29._note`: Also has l30a and f30TOP flasher primitive. DisableLighting callback on p30.
- `games/tron-legacy.json#/lamps/30._note`: Also has l31a and f31TOP flasher primitive. DisableLighting callback on p31.
- `games/tron-legacy.json#/lamps/31._note`: Also has l32a and f32TOP flasher primitive. DisableLighting callback on p32.
- `games/tron-legacy.json#/lamps/32._note`: Also has l33a. DisableLighting callback on p33.
- `games/tron-legacy.json#/lamps/33._note`: Also has l34a. DisableLighting callback on p34.
- `games/tron-legacy.json#/lamps/34._note`: Also has l35a and f35TOP flasher primitive. DisableLighting callback on p35.
- `games/tron-legacy.json#/lamps/35._note`: Also has l36a and f36TOP flasher primitive. DisableLighting callback on p36 (commented out).
- `games/tron-legacy.json#/lamps/36._note`: Also has l37a and f37TOP flasher primitive. DisableLighting callback on p37.
- `games/tron-legacy.json#/lamps/37._note`: Also has l38a and f38TOP flasher primitive. DisableLighting callback on p38.
- `games/tron-legacy.json#/lamps/38._note`: Also has l39a and f39TOP flasher primitive. DisableLighting callback on p39.
- `games/tron-legacy.json#/lamps/39._note`: Also has l40a and f40TOP flasher primitive. DisableLighting callback on p40.
- `games/tron-legacy.json#/lamps/40._note`: Also has l42a and f42TOP flasher primitive. DisableLighting callback on p42. Note: l42a is assigned to lamp 40 (likely typo in VBS: Lampz.MassAssign(40) = l42a).
- `games/tron-legacy.json#/lamps/41._note`: Also has l43a and f43TOP flasher primitive. DisableLighting callback on p43.
- `games/tron-legacy.json#/lamps/42._note`: Also has l45a and f45TOP flasher primitive. DisableLighting callback on p45 (intensity 30 instead of 50).
- `games/tron-legacy.json#/lamps/43._note`: DisableLighting callback on l46p with intensity 200 (stronger than insert lamps).
- `games/tron-legacy.json#/lamps/44._note`: DisableLighting callback on l47p with intensity 200.
- `games/tron-legacy.json#/lamps/45._note`: DisableLighting callback on l48p with intensity 200.
- `games/tron-legacy.json#/lamps/46._note`: Also has l49a. DisableLighting callback on p49.
- `games/tron-legacy.json#/lamps/47._note`: Also has l50a. DisableLighting callback on p50.
- `games/tron-legacy.json#/lamps/48._note`: Also has l51a and f51TOP flasher primitive. DisableLighting callback on p51.
- `games/tron-legacy.json#/lamps/49._note`: Also has l52a and f52TOP flasher primitive. DisableLighting callback on p52.
- `games/tron-legacy.json#/lamps/50._note`: Also has l53a and f53TOP flasher primitive. DisableLighting callback on p53.
- `games/tron-legacy.json#/lamps/51._note`: Also has l54a and f54TOP flasher primitive. DisableLighting callback on p54.
- `games/tron-legacy.json#/lamps/52._note`: Also has l55a. DisableLighting callback on p55.
- `games/tron-legacy.json#/lamps/53._note`: Also has l56a. DisableLighting callback on p56.
- `games/tron-legacy.json#/lamps/54._note`: Also has l57a. DisableLighting callback on p57.
- `games/tron-legacy.json#/lamps/55._note`: Also has l58a. DisableLighting callback on p58.
- `games/tron-legacy.json#/lamps/56._note`: Also has l59a and f59TOP flasher primitive. DisableLighting callback on p59.
- `games/tron-legacy.json#/lamps/57._note`: Also has l60a and f60TOP flasher primitive. DisableLighting callback on p60.
- `games/tron-legacy.json#/lamps/58._note`: Also has l61a and f61TOP flasher primitive. DisableLighting callback on p61 (commented out).
- `games/tron-legacy.json#/lamps/59._note`: Also has l62a and f62top flasher primitive. DisableLighting callback on p62.
- `games/tron-legacy.json#/lamps/60._note`: Also has l63a. DisableLighting callback on p63.
- `games/tron-legacy.json#/lamps/61._note`: Also has l64a. DisableLighting callback on p64.
- `games/tron-legacy.json#/lamps/62._note`: Lampz.MassAssign(65) = l01. VR Start button light. Stern manual says lamp 1 is start button — remapped to lamp 65 in this VPW table.
- `games/tron-legacy.json#/lamps/63._note`: Lampz.MassAssign(66) = l02. VR Tournament button light. Stern manual says lamp 2 is tournament button — remapped to lamp 66 in this VPW table.
- `games/tron-legacy.json#/lamps/64._note`: COMMENTED OUT in MassAssign (Lampz.MassAssign(101) = l101) but actively read via Lampz.state(101) for SetRGBLamp Rampenlicht2 (left ramp neon glow). Part of RGB triplet 101/102/103.
- `games/tron-legacy.json#/lamps/65._note`: COMMENTED OUT in MassAssign but actively read via Lampz.state(102) for left ramp neon glow RGB.
- `games/tron-legacy.json#/lamps/66._note`: COMMENTED OUT in MassAssign but actively read via Lampz.state(103) for left ramp neon glow RGB. Also drives Reflect2/Reflect3 sidewall colors.
- `games/tron-legacy.json#/lamps/67._note`: COMMENTED OUT in MassAssign but actively read via Lampz.state(104) for SetRGBLamp Rampenlicht1 (right ramp neon glow). Part of RGB triplet 104/105/106. Also drives Rechterstring material color.
- `games/tron-legacy.json#/lamps/68._note`: COMMENTED OUT in MassAssign but actively read via Lampz.state(105) for right ramp neon glow RGB.
- `games/tron-legacy.json#/lamps/69._note`: COMMENTED OUT in MassAssign but actively read via Lampz.state(106) for right ramp neon glow RGB. Also drives Reflect1 sidewall color.
- `games/tron-legacy.json#/_source/confidence_notes`: High confidence extraction from VPW VBScript. Platform is SAM (LoadVPM '01560000', 'sam.VBS', 3.10). ROM is trn_174h. Trough is a 4-ball cvpmBallStack with InitSw 0,21,20,19,18,0,0,0 — sw18-21 are ball stack positions (18 nearest shooter, 21 nearest drain). No explicit drain switch in InitSw (first arg is 0), but Drain_Hit calls bsTrough.AddBall. solTrough (sol 1) calls bsTrough.ExitSol_On and also PulseSw 22 (shooter lane confirm). Right hole (Arcade Scoop) uses separate cvpmBallStack bsRHole with InitSw 0,11 — ball sinks via sw11_Hit/Timer animation then DestroyBall/AddBall. Drop targets are cvpmDropTarget DTBank4 with InitDrop Array(sw04,sw03,sw02,sw01),Array(4,3,2,1) — switches 1-4. Solenoid 3 resets them (DTBank4.SolDropUp). Motor target bank (sw49/50/51) rises/lowers via solenoid 6 (TBMove) with elaborate Z-animation. Position tracked by Controller.Switch(52) for down and Controller.Switch(53) for up. Recognizer toy driven by solenoid 23 (recogrelay) with RecognizerTimer rotating recognizer.rotz; position switches: sw54 (rotz>=18, right), sw55 (center ~0), sw56 (rotz<=-18, left). Disc motor is solenoid 5 (SolDiscMotor) using myTurnTable class. Flippers use InitVpmFFlipsSAM — SAM framework assigns sol 15=left, sol 16=right (confirmed by SolCallback). No upper flippers active (sol 12 commented out as 'upperleftflipper'). Commented-out solenoids: 8 (shaker), 9/10/11 (flashers as SolModCallback), 12 (upper left flipper), 13/14 (slingshots), 22 (disc direction relay). Slingshots handled by VPX physics with PulseSw only (26 left, 27 right). Bumpers same — PulseSw only (31 top, 30 middle, 32 bottom). Spinner sw36 uses _Spin event (PulseSw 36). Spinner sw44 also uses _Spin (PulseSw 44). Lamps 1-64 from Lampz.MassAssign with rich VPX object names. Lamps 101-106 are RGB channels (commented out in MassAssign but actively read via Lampz.state() for ramp neon glow effects). Lamps 65-66 mapped to l01/l02 (start/tournament buttons). Flasher solenoids use SolModCallback with SetLampMod for PWM control. GI handled via ModLampz channel 0 with GICallback2.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.trn`: `games/trn.json` at the pinned migration revision.
- `legacy.game.tron-legacy`: `games/tron-legacy.json` at the pinned migration revision.
