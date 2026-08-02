# Cactus Canyon

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1998). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

## Playfield devices

Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.

## Custom mechanisms

- `mechanism.train`: Train mechanism on tracks across playfield Two-solenoid directional motor. Sol1=38 (forward), Sol2=37 (reverse). VPX: Train/Train1 primitives with TransX. Position saved to registry vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear [source: legacy.game.cc]
- `mechanism.mine-sign`: Gold mine entrance sign that raises/lowers Single-solenoid reversing mechanism. VPX: MineSign primitive Z position and Mine primitive RotX. Controls sw15.IsDropped visibility vpmMechOneSol + vpmMechReverse + vpmMechLinear [source: legacy.game.cc]
- `mechanism.bart-toy`: Bart figure that moves left/right and hat lifts Sol 33 (MoveBart) oscillates Bart L/R. Sol 36 (MoveHat) lifts hat via sine animation. sw75 detects ball hitting Bart [source: legacy.game.cc]

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
- `games/cc.json#/switches/0._vbscript_name`: S11
- `games/cc.json#/switches/0._note`: Unused in switch matrix
- `games/cc.json#/switches/1._vbscript_name`: S12
- `games/cc.json#/switches/1._note`: Unused in switch matrix
- `games/cc.json#/switches/2._vbscript_name`: swStart
- `games/cc.json#/switches/2._note`: Defined in WPC.VBS as swStartButton=13
- `games/cc.json#/switches/3._vbscript_name`: swTilt
- `games/cc.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/cc.json#/switches/4._vbscript_name`: sw15
- `games/cc.json#/switches/4._note`: Gold mine sign target. sw15.IsDropped toggles based on mine sign position. Also sw15b fires PulseSwitch 15
- `games/cc.json#/switches/5._vbscript_name`: sw16
- `games/cc.json#/switches/6._vbscript_name`: sw17
- `games/cc.json#/switches/7._vbscript_name`: sw18
- `games/cc.json#/switches/7._note`: Ball in shooter lane detection. plungerIM uses swPlunger VPX object reference
- `games/cc.json#/switches/8._vbscript_name`: swSlamTilt
- `games/cc.json#/switches/8._note`: Defined in WPC.VBS as swSlamTilt=21
- `games/cc.json#/switches/9._vbscript_name`: swCoinDoor
- `games/cc.json#/switches/9._note`: Set to 1 on init: Controller.Switch(22) = 1
- `games/cc.json#/switches/10._note`: Set to 0 on init: Controller.Switch(24) = 0
- `games/cc.json#/switches/11._vbscript_name`: sw26
- `games/cc.json#/switches/12._vbscript_name`: sw27
- `games/cc.json#/switches/13._vbscript_name`: sw28
- `games/cc.json#/switches/14._vbscript_name`: sw31
- `games/cc.json#/switches/14._note`: Trough jam switch. PulseSw 31 on hit
- `games/cc.json#/switches/15._vbscript_name`: sw32
- `games/cc.json#/switches/16._vbscript_name`: sw33
- `games/cc.json#/switches/17._vbscript_name`: sw34
- `games/cc.json#/switches/18._vbscript_name`: sw35
- `games/cc.json#/switches/19._vbscript_name`: sw36
- `games/cc.json#/switches/19._note`: Opto switch
- `games/cc.json#/switches/20._vbscript_name`: sw37
- `games/cc.json#/switches/20._note`: Opto switch
- `games/cc.json#/switches/21._vbscript_name`: MinePopper
- `games/cc.json#/switches/21._note`: Gold mine VUK. Controller.Switch(41) set in MinePopper_Hit/UnHit
- `games/cc.json#/switches/22._vbscript_name`: BartPopper
- `games/cc.json#/switches/22._note`: Saloon/Bart subway VUK. Controller.Switch(42) set in BartPopper_Hit/UnHit
- `games/cc.json#/switches/23._note`: Unused in switch matrix
- `games/cc.json#/switches/24._vbscript_name`: sw44
- `games/cc.json#/switches/25._note`: Unused in switch matrix
- `games/cc.json#/switches/26._vbscript_name`: sw46
- `games/cc.json#/switches/26._note`: Beer mug target with animated mug toy
- `games/cc.json#/switches/27._vbscript_name`: sw47
- `games/cc.json#/switches/28._vbscript_name`: sw48
- `games/cc.json#/switches/29._vbscript_name`: sw51
- `games/cc.json#/switches/30._vbscript_name`: sw52
- `games/cc.json#/switches/31._vbscript_name`: Bumper1
- `games/cc.json#/switches/32._vbscript_name`: Bumper2
- `games/cc.json#/switches/33._vbscript_name`: sw55
- `games/cc.json#/switches/33._note`: Implemented as a slingshot in VPX (sw55_Slingshot), but is the bottom jet bumper in the real machine
- `games/cc.json#/switches/34._vbscript_name`: sw56
- `games/cc.json#/switches/34._note`: Opto switch
- `games/cc.json#/switches/35._vbscript_name`: sw57
- `games/cc.json#/switches/36._vbscript_name`: sw58
- `games/cc.json#/switches/37._vbscript_name`: sw61
- `games/cc.json#/switches/37._note`: Bad Guy drop target. Uses Roth drop target system (DTHit/DTRaise/DTDrop)
- `games/cc.json#/switches/38._vbscript_name`: sw62
- `games/cc.json#/switches/38._note`: Bad Guy drop target
- `games/cc.json#/switches/39._vbscript_name`: sw63
- `games/cc.json#/switches/39._note`: Bad Guy drop target
- `games/cc.json#/switches/40._vbscript_name`: sw64
- `games/cc.json#/switches/40._note`: Bad Guy drop target
- `games/cc.json#/switches/41._vbscript_name`: Sw65
- `games/cc.json#/switches/41._note`: Gate switch with sw65flip flipper gate
- `games/cc.json#/switches/42._vbscript_name`: sw66
- `games/cc.json#/switches/42._note`: Opto switch
- `games/cc.json#/switches/43._vbscript_name`: sw67
- `games/cc.json#/switches/43._note`: Opto switch
- `games/cc.json#/switches/44._vbscript_name`: sw68
- `games/cc.json#/switches/44._note`: Gate switch with sw68flip flipper gate
- `games/cc.json#/switches/45._vbscript_name`: sw71
- `games/cc.json#/switches/45._note`: Train mechanism encoder pulse. AddPulseSw in TrainMech cvpmMech. PROC mode uses sw71_Timer for pulse
- `games/cc.json#/switches/46._vbscript_name`: sw72
- `games/cc.json#/switches/46._note`: Train home position. AddSw 72,0,0 in TrainMech cvpmMech. PROC mode sets via Polly_Timer
- `games/cc.json#/switches/47._vbscript_name`: sw73
- `games/cc.json#/switches/48._vbscript_name`: sw75
- `games/cc.json#/switches/48._note`: Bart toy hit switch. Triggers Bhit animation
- `games/cc.json#/switches/49._vbscript_name`: sw77
- `games/cc.json#/switches/49._note`: Mine mechanism home position. AddSw 77,0,1 in MineMech cvpmMech. PROC mode sets via Sw15_Timer
- `games/cc.json#/switches/50._vbscript_name`: sw78
- `games/cc.json#/switches/50._note`: Mine mechanism encoder pulse. AddPulseSw 78,8,2 in MineMech cvpmMech. PROC mode pulses via sw15b_Timer
- `games/cc.json#/switches/51._vbscript_name`: sw82
- `games/cc.json#/switches/52._vbscript_name`: Sw83
- `games/cc.json#/switches/52._note`: Gate switch with sw83flip flipper gate
- `games/cc.json#/switches/53._vbscript_name`: sw84
- `games/cc.json#/switches/53._note`: Gate switch with sw84flip flipper gate
- `games/cc.json#/switches/54._vbscript_name`: sw85
- `games/cc.json#/switches/54._note`: Gate switch with sw85flip flipper gate
- `games/cc.json#/switches/55._vbscript_name`: sw86
- `games/cc.json#/switches/56._vbscript_name`: sw87
- `games/cc.json#/coils/0._vbscript_callback`: AutoPlunger
- `games/cc.json#/coils/0._note`: Uses cvpmImpulseP with IMPowerSetting=54.5
- `games/cc.json#/coils/1._vbscript_callback`: Drop1
- `games/cc.json#/coils/1._note`: Raises/drops sw61 bad guy drop target
- `games/cc.json#/coils/2._vbscript_callback`: Drop2
- `games/cc.json#/coils/2._note`: Raises/drops sw62 bad guy drop target
- `games/cc.json#/coils/3._vbscript_callback`: Drop3
- `games/cc.json#/coils/3._note`: Raises/drops sw63 bad guy drop target
- `games/cc.json#/coils/4._vbscript_callback`: Drop4
- `games/cc.json#/coils/4._note`: Raises/drops sw64 bad guy drop target
- `games/cc.json#/coils/5._vbscript_callback`: SolMinePopper
- `games/cc.json#/coils/5._note`: Gold mine VUK eject. MinePopper.kick 0,45,1.56
- `games/cc.json#/coils/6._vbscript_callback`: SolKnocker
- `games/cc.json#/coils/7._vbscript_callback`: SolSaloonPopper
- `games/cc.json#/coils/7._note`: Saloon/Bart subway VUK eject. BartPopper.kick 0,45,1.56
- `games/cc.json#/coils/8._vbscript_callback`: ReleaseBall
- `games/cc.json#/coils/8._note`: sw32.kick 53,12. Releases ball from trough to shooter lane
- `games/cc.json#/coils/9._note`: Commented out in VBS: 'SolCallback(10) = "". Hardware-driven slingshot
- `games/cc.json#/coils/10._note`: Commented out in VBS: 'SolCallback(11) = "". Hardware-driven slingshot
- `games/cc.json#/coils/11._note`: Commented out in VBS: 'SolCallback(12) = "". Hardware-driven bumper
- `games/cc.json#/coils/12._note`: Commented out in VBS: 'SolCallback(13) = "". Hardware-driven bumper
- `games/cc.json#/coils/13._vbscript_callback`: GunPostLeft
- `games/cc.json#/coils/13._note`: LPin.IsDropped controlled. Up/down post near left flipper
- `games/cc.json#/coils/14._vbscript_callback`: GunPostRight
- `games/cc.json#/coils/14._note`: RPin.IsDropped controlled. Up/down post near right flipper
- `games/cc.json#/coils/15._note`: Commented out in VBS: 'SolCallback(16) = "". Hardware-driven bumper
- `games/cc.json#/coils/16._vbscript_callback`: MoveMine
- `games/cc.json#/coils/16._note`: VPM mode: MoveMine (cvpmMech.Sol1=17). PROC mode: MoveMine_PROC. Controls mine sign up/down mechanism
- `games/cc.json#/coils/17._vbscript_callback`: Sol18
- `games/cc.json#/coils/17._note`: VPM mode: SolModCallback (modulated). PROC mode: SolCallback. Controls flasher collection F18 and Mine image swap
- `games/cc.json#/coils/18._vbscript_callback`: Sol19
- `games/cc.json#/coils/18._note`: VPM mode: SolModCallback (modulated). PROC mode: SolCallback. Flasher collection F19
- `games/cc.json#/coils/19._vbscript_callback`: Sol20
- `games/cc.json#/coils/19._note`: VPM mode: SolModCallback (modulated). PROC mode: SolCallback. Flasher collection F20
- `games/cc.json#/coils/20._vbscript_callback`: LGate
- `games/cc.json#/coils/20._note`: LLoopGate.Open toggled
- `games/cc.json#/coils/21._vbscript_callback`: RGate
- `games/cc.json#/coils/21._note`: RLoopGate.Open toggled
- `games/cc.json#/coils/22._vbscript_callback`: Sol24
- `games/cc.json#/coils/22._note`: VPM mode: SolModCallback (modulated). PROC mode: SolCallback. Flasher collection F24
- `games/cc.json#/coils/23._vbscript_callback`: Flash125
- `games/cc.json#/coils/23._note`: Uses Fluppers Flashers 2.2 system (FlasherFlash3). Originally Sol25 (commented out), replaced by Flash125
- `games/cc.json#/coils/24._vbscript_callback`: Sol26
- `games/cc.json#/coils/24._note`: VPM mode: SolModCallback (modulated). PROC mode: SolCallback. Flasher collection F26 + F26R lamp
- `games/cc.json#/coils/25._vbscript_callback`: Flash127
- `games/cc.json#/coils/25._note`: Uses Fluppers Flashers 2.2 system (FlasherFlash2). Originally Sol27 (commented out), replaced by Flash127
- `games/cc.json#/coils/26._vbscript_callback`: Flash128
- `games/cc.json#/coils/26._note`: Uses Fluppers Flashers 2.2 system (FlasherFlash1). Originally Sol28 (commented out), replaced by Flash128
- `games/cc.json#/coils/27._vbscript_callback`: MoveBart
- `games/cc.json#/coils/27._note`: Bart toy motor. Moves Bart primitive left/right via Bart1_Timer animation
- `games/cc.json#/coils/28._vbscript_callback`: MoveHat
- `games/cc.json#/coils/28._note`: Bart toy hat mechanism. Lifts Bart_Hat via Bart2_Timer sine animation
- `games/cc.json#/coils/29._vbscript_callback`: TrainB
- `games/cc.json#/coils/29._note`: VPM mode: TrainB (cvpmMech.Sol2=37). PROC mode: TrainB_PROC. Train moves backward
- `games/cc.json#/coils/30._vbscript_callback`: TrainF
- `games/cc.json#/coils/30._note`: VPM mode: TrainF (cvpmMech.Sol1=38). PROC mode: TrainF_PROC. Train moves forward
- `games/cc.json#/coils/31._vbscript_callback`: SolRFlipper
- `games/cc.json#/coils/31._note`: WPC standard sLRFlipper=46 from core.vbs. ROM-controlled flipper (WPC-95)
- `games/cc.json#/coils/32._vbscript_callback`: SolLFlipper
- `games/cc.json#/coils/32._note`: WPC standard sLLFlipper=48 from core.vbs. ROM-controlled flipper (WPC-95)
- `games/cc.json#/lamps/0._vbscript_name`: L11
- `games/cc.json#/lamps/1._vbscript_name`: L12
- `games/cc.json#/lamps/2._vbscript_name`: L13
- `games/cc.json#/lamps/3._vbscript_name`: L14
- `games/cc.json#/lamps/4._vbscript_name`: L15
- `games/cc.json#/lamps/5._vbscript_name`: L16
- `games/cc.json#/lamps/6._vbscript_name`: L17
- `games/cc.json#/lamps/6._note`: Special handling: LampState(17) read from L17.state in LampTimer. Additional L17R lamp object
- `games/cc.json#/lamps/7._vbscript_name`: L18
- `games/cc.json#/lamps/7._note`: Special handling: LampState(18) read from L18.state in LampTimer. Additional L18R lamp object
- `games/cc.json#/lamps/8._vbscript_name`: L21
- `games/cc.json#/lamps/9._vbscript_name`: L22
- `games/cc.json#/lamps/10._vbscript_name`: L23
- `games/cc.json#/lamps/11._vbscript_name`: L24
- `games/cc.json#/lamps/12._vbscript_name`: L25
- `games/cc.json#/lamps/13._vbscript_name`: L26
- `games/cc.json#/lamps/14._vbscript_name`: L27
- `games/cc.json#/lamps/15._vbscript_name`: L28
- `games/cc.json#/lamps/16._vbscript_name`: L31
- `games/cc.json#/lamps/16._note`: Drop target 2 insert
- `games/cc.json#/lamps/17._vbscript_name`: L32
- `games/cc.json#/lamps/17._note`: Drop target 0 insert (leftmost)
- `games/cc.json#/lamps/18._vbscript_name`: L33
- `games/cc.json#/lamps/19._vbscript_name`: L34
- `games/cc.json#/lamps/20._vbscript_name`: L35
- `games/cc.json#/lamps/21._vbscript_name`: L36
- `games/cc.json#/lamps/22._vbscript_name`: L37
- `games/cc.json#/lamps/23._vbscript_name`: L38
- `games/cc.json#/lamps/24._vbscript_name`: L41
- `games/cc.json#/lamps/25._vbscript_name`: L42
- `games/cc.json#/lamps/25._note`: Also referenced as light42 in drop target code (DT1 state)
- `games/cc.json#/lamps/26._vbscript_name`: L43
- `games/cc.json#/lamps/26._note`: Also referenced as light43 in drop target code (DT1 state)
- `games/cc.json#/lamps/27._vbscript_name`: L44
- `games/cc.json#/lamps/27._note`: Also referenced as light44 in drop target code (DT3 state)
- `games/cc.json#/lamps/28._vbscript_name`: L45
- `games/cc.json#/lamps/28._note`: Also referenced as light45 in drop target code (DT3 state)
- `games/cc.json#/lamps/29._vbscript_name`: L46
- `games/cc.json#/lamps/30._vbscript_name`: L47
- `games/cc.json#/lamps/31._vbscript_name`: L48
- `games/cc.json#/lamps/32._vbscript_name`: L51
- `games/cc.json#/lamps/32._note`: Drop target 3 insert. Also referenced as light50/light51 in drop target code (DT4 state)
- `games/cc.json#/lamps/33._vbscript_name`: L52
- `games/cc.json#/lamps/34._vbscript_name`: L53
- `games/cc.json#/lamps/35._vbscript_name`: L54
- `games/cc.json#/lamps/36._vbscript_name`: L55
- `games/cc.json#/lamps/37._vbscript_name`: L56
- `games/cc.json#/lamps/38._vbscript_name`: L57
- `games/cc.json#/lamps/39._vbscript_name`: L58
- `games/cc.json#/lamps/40._vbscript_name`: L61
- `games/cc.json#/lamps/41._vbscript_name`: L62
- `games/cc.json#/lamps/42._vbscript_name`: L63
- `games/cc.json#/lamps/43._vbscript_name`: L64
- `games/cc.json#/lamps/44._vbscript_name`: L65
- `games/cc.json#/lamps/45._vbscript_name`: L66
- `games/cc.json#/lamps/46._vbscript_name`: L67
- `games/cc.json#/lamps/47._vbscript_name`: L68
- `games/cc.json#/lamps/48._vbscript_name`: L71
- `games/cc.json#/lamps/49._vbscript_name`: L72
- `games/cc.json#/lamps/50._vbscript_name`: L73
- `games/cc.json#/lamps/51._vbscript_name`: L74
- `games/cc.json#/lamps/52._vbscript_name`: L75
- `games/cc.json#/lamps/53._vbscript_name`: L76
- `games/cc.json#/lamps/54._vbscript_name`: L77
- `games/cc.json#/lamps/55._vbscript_name`: L78
- `games/cc.json#/lamps/56._vbscript_name`: L81
- `games/cc.json#/lamps/57._vbscript_name`: L82
- `games/cc.json#/lamps/58._vbscript_name`: L83
- `games/cc.json#/lamps/59._vbscript_name`: L84
- `games/cc.json#/lamps/59._note`: Drop target 1 insert
- `games/cc.json#/lamps/60._vbscript_name`: L85
- `games/cc.json#/lamps/60._note`: Optional BeerMugMod override: when enabled, Lights(85) = Array(BeerMugL1,BeerMugL2,BeerMugL3)
- `games/cc.json#/lamps/61._vbscript_name`: L86
- `games/cc.json#/lamps/62._vbscript_name`: L87
- `games/cc.json#/lamps/63._vbscript_name`: L88
- `games/cc.json#/flashers/0._vbscript_name`: F18
- `games/cc.json#/flashers/0._note`: Modulated (SolModCallback in VPM mode). Flasher collection F18 + Mine image swap. Internal lamp state 148
- `games/cc.json#/flashers/1._vbscript_name`: F19
- `games/cc.json#/flashers/1._note`: Modulated (SolModCallback in VPM mode). Flasher collection F19. Internal lamp state 149
- `games/cc.json#/flashers/2._vbscript_name`: F20
- `games/cc.json#/flashers/2._note`: Modulated (SolModCallback in VPM mode). Flasher collection F20. Internal lamp state 150
- `games/cc.json#/flashers/3._vbscript_name`: F24
- `games/cc.json#/flashers/3._note`: Modulated. Flasher collection F24. Internal lamp state 154
- `games/cc.json#/flashers/4`: Duplicate binding label candidate `Middle Right Flasher (Alt)` differs from `Middle Right Flasher`.
- `games/cc.json#/flashers/4._vbscript_name`: F25
- `games/cc.json#/flashers/4._note`: Commented out in VPW. Replaced by Fluppers Flasher system (Flash125/FlasherFlash3)
- `games/cc.json#/flashers/5._vbscript_name`: F26
- `games/cc.json#/flashers/5._note`: Modulated. Flasher collection F26 + F26R reflector lamp. Internal lamp state 156
- `games/cc.json#/flashers/6._vbscript_name`: F27
- `games/cc.json#/flashers/6._note`: Original Sol27 commented out. Uses Fluppers Flasher system (Flash127/FlasherFlash2). F27R1/F27R2 reflector lamps
- `games/cc.json#/flashers/7._vbscript_name`: F28
- `games/cc.json#/flashers/7._note`: Original Sol28 commented out. Uses Fluppers Flasher system (Flash128/FlasherFlash1). F28R1/F28R2 reflector lamps
- `games/cc.json#/gi_strings/0._vbscript_name`: LeftGI
- `games/cc.json#/gi_strings/0._note`: GiCallback2 index 0. Collection of lights controlled via UpdateGI(0, step). Intensity modulated 0-8 steps in VPM mode
- `games/cc.json#/gi_strings/1._vbscript_name`: RightGI
- `games/cc.json#/gi_strings/1._note`: GiCallback2 index 1. Collection of lights controlled via UpdateGI(1, step)
- `games/cc.json#/gi_strings/2._vbscript_name`: TopGI
- `games/cc.json#/gi_strings/2._note`: GiCallback2 index 2. Collections TopGI + TopGI2 + BWGI. Also controls Bart/Bart_Hat blenddisablelighting and ColorGrade table image
- `games/cc.json#/mechanisms/0._note`: Two-solenoid directional motor. Sol1=38 (forward), Sol2=37 (reverse). VPX: Train/Train1 primitives with TransX. Position saved to registry
- `games/cc.json#/mechanisms/1._note`: Single-solenoid reversing mechanism. VPX: MineSign primitive Z position and Mine primitive RotX. Controls sw15.IsDropped visibility
- `games/cc.json#/mechanisms/2._note`: Sol 33 (MoveBart) oscillates Bart L/R. Sol 36 (MoveHat) lifts hat via sine animation. sw75 detects ball hitting Bart
- `games/cc.json#/_source/confidence_notes`: Switches and coils extracted from VPW 1.1 VBScript with cross-reference to cc_machine.yaml (P-ROC config) and pinitech.com switch chart. Lamp names from cc_machine.yaml (CCC P-ROC project). Some lamps (e.g. L86 beerMugGI) may be VPX-specific additions. GI strings handled via collections (LeftGI, RightGI, TopGI) not individual lamp numbers.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.cc`: `games/cc.json` at the pinned migration revision.
