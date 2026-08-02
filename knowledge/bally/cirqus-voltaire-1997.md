# Cirqus Voltaire

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1997). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

## Playfield devices

Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.

## Custom mechanisms

- `mechanism.ringmaster-pop-up-head`: Ringmaster Pop-Up Head Linear motor raises/lowers Ringmaster head. Sol 22 enables motor, Sol 39 controls direction. Callback UpdateRM moves ringmaster.z and collision walls based on position. [source: legacy.game.cv]
- `mechanism.left-loop-magnet`: Left Loop Magnet [source: legacy.game.cv]
- `mechanism.ramp-lock-magnet`: Ramp Lock Magnet [source: legacy.game.cv]
- `mechanism.ringmaster-magnet`: Ringmaster Magnet Grabs ball at Ringmaster head; custom kick logic on release via SolRingmasterMagnet sub [source: legacy.game.cv]
- `mechanism.spin-magnet`: Spin Magnet No solenoid assigned; used for wobble/shake physics on ringmaster head [source: legacy.game.cv]
- `mechanism.ramp-ball-lock-3-ball`: Ramp Ball Lock (3 ball) 3-ball virtual lock on upper ramp; released by Lock Post solenoid (16) [source: legacy.game.cv]
- `mechanism.ball-trough-4-ball`: Ball Trough (4 ball) [source: legacy.game.cv]
- `mechanism.popper-subway-eject`: Popper (Subway Eject) [source: legacy.game.cv]
- `mechanism.backbox-prize-wheel-bell-spinner`: Backbox Prize Wheel / Bell Spinner Custom physics simulation; ball launched by Backbox Kicker (sol 2) interacts with spinning disc. Disc has 5 spinner balls for collision detection. Bell at sw11. [source: legacy.game.cv]

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
- `games/cv.json#/switches/0._vbscript_name`: sw11
- `games/cv.json#/switches/0._note`: Rollover switch; also pulsed via vpmTimer from EndCannon sub for bell ring
- `games/cv.json#/switches/1._vbscript_name`: sw12
- `games/cv.json#/switches/2._vbscript_name`: keyFront
- `games/cv.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/cv.json#/switches/4._vbscript_name`: sw15
- `games/cv.json#/switches/5._vbscript_name`: sw16
- `games/cv.json#/switches/5._note`: Timed switch with Eddy_timer to auto-release; enabled when RMCurrPos > 4 and < 100
- `games/cv.json#/switches/6._vbscript_name`: sw17
- `games/cv.json#/switches/7._vbscript_name`: sw18
- `games/cv.json#/switches/7._note`: Sets BIPL (Ball In Plunger Lane) flag
- `games/cv.json#/switches/9._note`: Initialized to 1 at start; toggled for motor bug fix
- `games/cv.json#/switches/10._vbscript_name`: sw23
- `games/cv.json#/switches/11._note`: Set to 0 at init (.Switch(24) = 0)
- `games/cv.json#/switches/12._vbscript_name`: sw25
- `games/cv.json#/switches/13._vbscript_name`: sw26
- `games/cv.json#/switches/14._vbscript_name`: sw27
- `games/cv.json#/switches/15._vbscript_name`: sw28
- `games/cv.json#/switches/16._note`: Pulsed by SolRelease sub via vpmTimer.PulseSw 31
- `games/cv.json#/switches/17._note`: bsTrough.InitSw 0, 32, 33, 34, 35, 0, 0, 0
- `games/cv.json#/switches/21._vbscript_name`: sw36
- `games/cv.json#/switches/21._note`: Popper.InitSw 0, 36, 0, 0, 0, 0, 0, 0; subway entrance
- `games/cv.json#/switches/22._vbscript_name`: T37a, T37b, T37c
- `games/cv.json#/switches/22._note`: Three physical targets all pulse switch 37
- `games/cv.json#/switches/23._vbscript_name`: T38a, T38b
- `games/cv.json#/switches/23._note`: Two physical targets pulse switch 38; also RMHit_Hit pulses 38
- `games/cv.json#/switches/24._vbscript_name`: T41
- `games/cv.json#/switches/25._note`: mechRM.AddSw 42, 117, 118 (top position opto)
- `games/cv.json#/switches/26._note`: mechRM.AddSw 43, 88, 89 (middle position opto)
- `games/cv.json#/switches/27._note`: mechRM.AddSw 44, 0, 1 (bottom/home position opto)
- `games/cv.json#/switches/28._vbscript_name`: sw45
- `games/cv.json#/switches/29._vbscript_name`: sw46
- `games/cv.json#/switches/29._note`: Pulsed via vpmTimer.PulseSw 46
- `games/cv.json#/switches/30._vbscript_name`: sw47
- `games/cv.json#/switches/30._note`: Pulsed via vpmTimer.PulseSw 47
- `games/cv.json#/switches/31._vbscript_name`: sw48
- `games/cv.json#/switches/32._note`: LeftSlingShot_Slingshot pulses sw 51
- `games/cv.json#/switches/33._note`: RightSlingShot_Slingshot pulses sw 52
- `games/cv.json#/switches/34._vbscript_name`: UpperJetBumper
- `games/cv.json#/switches/35._vbscript_name`: MiddleJetBumper
- `games/cv.json#/switches/35._note`: Disappearing jet bumper; raised/lowered by sol 7/8
- `games/cv.json#/switches/36._vbscript_name`: LowerJetBumper
- `games/cv.json#/switches/37._vbscript_name`: T56
- `games/cv.json#/switches/38._vbscript_name`: sw57
- `games/cv.json#/switches/39._vbscript_name`: T58
- `games/cv.json#/switches/40._vbscript_name`: T61
- `games/cv.json#/switches/41._vbscript_name`: T62
- `games/cv.json#/switches/42._vbscript_name`: sw63
- `games/cv.json#/switches/43._vbscript_name`: sw64
- `games/cv.json#/switches/44._vbscript_name`: sw65
- `games/cv.json#/switches/45._vbscript_name`: sw66
- `games/cv.json#/switches/45._note`: vlLock.InitVLock Array(sw66, sw67, sw68)
- `games/cv.json#/switches/46._vbscript_name`: sw67
- `games/cv.json#/switches/47._vbscript_name`: sw68
- `games/cv.json#/switches/48._vbscript_name`: sw71
- `games/cv.json#/switches/48._note`: LeftSaucer.InitSaucer sw71, 71, 45, 10
- `games/cv.json#/switches/49._vbscript_name`: sw72
- `games/cv.json#/switches/49._note`: RightSaucer.InitSaucer sw72, 72, 140, 6
- `games/cv.json#/switches/50._vbscript_name`: sw74
- `games/cv.json#/switches/50._note`: Pulsed via vpmTimer.PulseSw 74
- `games/cv.json#/switches/51._vbscript_name`: sw75
- `games/cv.json#/switches/52._vbscript_name`: sw76
- `games/cv.json#/switches/53._vbscript_name`: sw115spinner
- `games/cv.json#/switches/53._note`: Dedicated opto; pulses on each spin
- `games/cv.json#/switches/54._vbscript_name`: sw117spinner
- `games/cv.json#/switches/54._note`: Dedicated opto; pulses on each spin
- `games/cv.json#/coils/0._vbscript_callback`: SolCallback(1) = "AutoPlunger"
- `games/cv.json#/coils/1._vbscript_callback`: SolCallback(2) = "BackBoxKick"
- `games/cv.json#/coils/1._note`: Fires plunger2 to send ball to backbox spinner/bell mechanism
- `games/cv.json#/coils/2._vbscript_callback`: Commented out in script; handled by cvpmMagnet LoopMagnet.Solenoid = 3
- `games/cv.json#/coils/2._note`: cvpmMagnet with GrabCenter=True, Size=200
- `games/cv.json#/coils/3._note`: Not wired in VPX script (handled by VPX bumper object); listed in manual
- `games/cv.json#/coils/4._vbscript_callback`: Commented out in script; handled by cvpmMagnet LockMagnet.Solenoid = 5
- `games/cv.json#/coils/4._note`: cvpmMagnet with GrabCenter=True, Size=200
- `games/cv.json#/coils/5._note`: Listed in manual; not directly wired in VPX script (see sol 34 for DiverterHold)
- `games/cv.json#/coils/6._vbscript_callback`: SolCallback(7) = "JetUp"
- `games/cv.json#/coils/6._note`: Raises disappearing middle jet bumper
- `games/cv.json#/coils/7._vbscript_callback`: SolCallBack(8) = "JetRelease"
- `games/cv.json#/coils/7._note`: Lowers disappearing middle jet bumper
- `games/cv.json#/coils/8._vbscript_callback`: SolCallBack(9) = "SolRelease"
- `games/cv.json#/coils/8._note`: Pulses sw 31 and calls bsTrough.ExitSol_On
- `games/cv.json#/coils/9._note`: Physical slingshot coil; not explicitly wired in VPX (handled by VPX slingshot object)
- `games/cv.json#/coils/10._note`: Physical slingshot coil; not explicitly wired in VPX (handled by VPX slingshot object)
- `games/cv.json#/coils/11._note`: Physical bumper coil; not explicitly wired in VPX (handled by VPX bumper object)
- `games/cv.json#/coils/12._note`: Physical bumper coil; not explicitly wired in VPX (handled by VPX bumper object)
- `games/cv.json#/coils/13._vbscript_callback`: SolCallBack(14) = "LeftSaucer.SolOut"
- `games/cv.json#/coils/13._note`: Kicks ball from left saucer at angle 45, force 10
- `games/cv.json#/coils/14._vbscript_callback`: SolCallBack(15) = "RightSaucer.SolOut"
- `games/cv.json#/coils/14._note`: Kicks ball from right saucer at angle 140, force 6
- `games/cv.json#/coils/15._vbscript_callback`: SolCallBack(16) = "LockPost"
- `games/cv.json#/coils/15._note`: Controls ball lock post for multiball; releases vlLock
- `games/cv.json#/coils/16._vbscript_callback`: SolModCallBack(17) = "Flash117"
- `games/cv.json#/coils/16._note`: PWM flasher; drives f117, f117b
- `games/cv.json#/coils/17._vbscript_callback`: SolModCallBack(18) = "Flash118"
- `games/cv.json#/coils/17._note`: PWM flasher; drives l118
- `games/cv.json#/coils/18._vbscript_callback`: SolModCallBack(19) = "Flash119"
- `games/cv.json#/coils/18._note`: PWM flasher; drives l119
- `games/cv.json#/coils/19._vbscript_callback`: SolModCallBack(20) = "Flash120"
- `games/cv.json#/coils/19._note`: PWM flasher; drives l120
- `games/cv.json#/coils/20._vbscript_callback`: SolModCallBack(21) = "Flash121"
- `games/cv.json#/coils/20._note`: PWM flasher; drives l121 and Flupper dome FlasherFlash1
- `games/cv.json#/coils/21._vbscript_callback`: SolCallBack(22) = "MotorEnable"
- `games/cv.json#/coils/21._note`: Enables ringmaster motor; plays motor sound. Also mechRM.Sol1 = 22
- `games/cv.json#/coils/22._vbscript_callback`: SolModCallBack(23) = "Flash123"
- `games/cv.json#/coils/22._note`: PWM flasher; drives f123
- `games/cv.json#/coils/23._vbscript_callback`: SolModCallBack(24) = "Flash124"
- `games/cv.json#/coils/23._note`: PWM flasher; drives l124 and Flupper dome FlasherFlash2
- `games/cv.json#/coils/24._vbscript_callback`: SolModCallBack(25) = "Flash125"
- `games/cv.json#/coils/24._note`: PWM flasher; drives Flupper dome FlasherFlash3
- `games/cv.json#/coils/25._vbscript_callback`: SolModCallBack(26) = "Flash126"
- `games/cv.json#/coils/25._note`: PWM flasher; drives l126 and Flupper dome FlasherFlash4
- `games/cv.json#/coils/26._vbscript_callback`: SolModCallBack(27) = "Flash127"
- `games/cv.json#/coils/26._note`: PWM flasher; drives l127, f127, f127a; changes Ringmaster texture based on state
- `games/cv.json#/coils/27._vbscript_callback`: SolModCallBack(28) = "Flash128"
- `games/cv.json#/coils/27._note`: PWM flasher; drives f128, f128b
- `games/cv.json#/coils/28._vbscript_callback`: SolCallBack(33) = "SolPopper"
- `games/cv.json#/coils/28._note`: Kicks ball from popper (subway) at angle 284, force 26
- `games/cv.json#/coils/29._vbscript_callback`: SolCallback(34) = "DiverterHold"
- `games/cv.json#/coils/29._note`: Holds diverter open to direct ball to right orbit
- `games/cv.json#/coils/30._vbscript_callback`: SolCallBack(35) = "SolRingmasterMagnet"
- `games/cv.json#/coils/30._note`: Grabs/releases ball at ringmaster head; cvpmMagnet with GrabCenter=0, Size=100
- `games/cv.json#/coils/31._vbscript_callback`: SolCallback(36) = "UpperPost"
- `games/cv.json#/coils/31._note`: Raises/lowers upper post wall
- `games/cv.json#/coils/32._vbscript_callback`: SolModCallBack(37) = "Flash137"
- `games/cv.json#/coils/32._note`: PWM; controls UV/neon lighting that changes playfield textures to blue
- `games/cv.json#/coils/33._note`: mechRM.Sol2 = 39; controls direction of ringmaster motor
- `games/cv.json#/coils/34._vbscript_callback`: SolCallback(sLRFlipper) = "SolRFlipper"
- `games/cv.json#/coils/34._note`: WPC framework constant sLRFlipper = 46
- `games/cv.json#/coils/35._vbscript_callback`: SolCallback(sLLFlipper) = "SolLFlipper"
- `games/cv.json#/coils/35._note`: WPC framework constant sLLFlipper = 48
- `games/cv.json#/lamps/0._vbscript_name`: l11, l11b
- `games/cv.json#/lamps/1._vbscript_name`: l12, l12b
- `games/cv.json#/lamps/2._vbscript_name`: l13, l13b
- `games/cv.json#/lamps/3._vbscript_name`: l14, l14b
- `games/cv.json#/lamps/4._vbscript_name`: l15, l15b
- `games/cv.json#/lamps/5._vbscript_name`: l16, l16b
- `games/cv.json#/lamps/6._vbscript_name`: l17, l17b
- `games/cv.json#/lamps/7._vbscript_name`: l18, l18b
- `games/cv.json#/lamps/8._vbscript_name`: l21, l21b
- `games/cv.json#/lamps/9._vbscript_name`: l22, l22b
- `games/cv.json#/lamps/10._vbscript_name`: l23, l23b
- `games/cv.json#/lamps/11._vbscript_name`: l24, l24b
- `games/cv.json#/lamps/12._vbscript_name`: l25, l25b
- `games/cv.json#/lamps/13._vbscript_name`: l26, l26b
- `games/cv.json#/lamps/14._vbscript_name`: l27, l27b
- `games/cv.json#/lamps/15._vbscript_name`: l28, l28b
- `games/cv.json#/lamps/16._vbscript_name`: l31, l31b
- `games/cv.json#/lamps/17._vbscript_name`: l32, l32b
- `games/cv.json#/lamps/18._vbscript_name`: l33, l33b
- `games/cv.json#/lamps/19._vbscript_name`: l34, l34b
- `games/cv.json#/lamps/20._vbscript_name`: l35, l35b
- `games/cv.json#/lamps/21._vbscript_name`: l36, l36b
- `games/cv.json#/lamps/22._vbscript_name`: l37, l37b
- `games/cv.json#/lamps/23._vbscript_name`: l38, l38b
- `games/cv.json#/lamps/24._vbscript_name`: l41, l41b
- `games/cv.json#/lamps/25._vbscript_name`: l42, l42b
- `games/cv.json#/lamps/26._vbscript_name`: l43, l43b
- `games/cv.json#/lamps/27._vbscript_name`: l44, l44b
- `games/cv.json#/lamps/28._vbscript_name`: l45, l45b
- `games/cv.json#/lamps/29._vbscript_name`: l46, l46b
- `games/cv.json#/lamps/30._vbscript_name`: l47, l47b
- `games/cv.json#/lamps/31._vbscript_name`: l48, l48b
- `games/cv.json#/lamps/32._vbscript_name`: l51, l51b
- `games/cv.json#/lamps/33._vbscript_name`: l52, l52b
- `games/cv.json#/lamps/34._vbscript_name`: l53, l53b
- `games/cv.json#/lamps/35._vbscript_name`: l54, l54b
- `games/cv.json#/lamps/36._vbscript_name`: l55, l55b
- `games/cv.json#/lamps/37._vbscript_name`: l56, l56b
- `games/cv.json#/lamps/38._vbscript_name`: l57, l57b
- `games/cv.json#/lamps/39._vbscript_name`: l58, l58b
- `games/cv.json#/lamps/40._vbscript_name`: l61, l61b
- `games/cv.json#/lamps/41._vbscript_name`: l62, l62b
- `games/cv.json#/lamps/42._vbscript_name`: l63, l63b
- `games/cv.json#/lamps/43._vbscript_name`: l64, l64b
- `games/cv.json#/lamps/44._vbscript_name`: l65, l65b
- `games/cv.json#/lamps/45._vbscript_name`: l66, l66b
- `games/cv.json#/lamps/46._vbscript_name`: l67, l67b
- `games/cv.json#/lamps/47._vbscript_name`: l68, l68b
- `games/cv.json#/lamps/48._vbscript_name`: l71, l71b
- `games/cv.json#/lamps/49._vbscript_name`: l72, l72b
- `games/cv.json#/lamps/50._vbscript_name`: l73, l73b
- `games/cv.json#/lamps/51._vbscript_name`: l74, l74b
- `games/cv.json#/lamps/52._vbscript_name`: l75, l75b
- `games/cv.json#/lamps/53._vbscript_name`: l76, l76b
- `games/cv.json#/lamps/54._vbscript_name`: l77, l77b
- `games/cv.json#/lamps/54._note`: Also controls Volt4 primitive via DisableLightingm and imgswapm
- `games/cv.json#/lamps/55._vbscript_name`: l78, l78b
- `games/cv.json#/lamps/56._vbscript_name`: l81, l81b
- `games/cv.json#/lamps/57._vbscript_name`: l82, l82b
- `games/cv.json#/lamps/58._vbscript_name`: l83
- `games/cv.json#/lamps/58._note`: Also swaps plastic_boombumper image via NFadeObjm
- `games/cv.json#/lamps/59._vbscript_name`: l84, l84b
- `games/cv.json#/lamps/60._vbscript_name`: l85, l85b
- `games/cv.json#/lamps/60._note`: Also controls Volt3 primitive via DisableLightingm and imgswapm
- `games/cv.json#/lamps/61._vbscript_name`: l86, l86b
- `games/cv.json#/lamps/61._note`: Also controls Volt1 primitive via DisableLightingm and imgswapm
- `games/cv.json#/lamps/62._vbscript_name`: l87, l87b
- `games/cv.json#/lamps/62._note`: Also controls Volt2 primitive via DisableLightingm and imgswapm
- `games/cv.json#/gi/0._vbscript_callback`: UpdateGI case 0
- `games/cv.json#/gi/0._note`: Controls Gi_Pf_Right_01 lights and Gi_Pf_Right_Plastics materials
- `games/cv.json#/gi/1._vbscript_callback`: UpdateGI case 1
- `games/cv.json#/gi/1._note`: Controls Gi_Pf_Middle_02 lights, Gi_Pf_Center_Plastics, MetalGroup_Center; toggles Ringmaster on/off texture
- `games/cv.json#/gi/2._vbscript_callback`: UpdateGI case 2
- `games/cv.json#/gi/2._note`: Controls Gi_Pf_Left_03 lights and Gi_Pf_Left_Plastics materials
- `games/cv.json#/mechanisms/0._vbscript_class`: cvpmMech
- `games/cv.json#/mechanisms/0._config`: {"length": 960, "mtype": "vpmMechLinear + vpmMechFast + vpmMechReverse + vpmMechOneDirSol", "sol1": 22, "sol2": 39, "steps": 118, "switches": [{"description": "Ringmaster Down (home)", "end": 1, "start": 0, "sw": 44}, {"description": "Ringmaster Middle", "end": 89, "start": 88, "sw": 43}, {"description": "Ringmaster Up (fully raised)", "end": 118, "start": 117, "sw": 42}]}
- `games/cv.json#/mechanisms/0._note`: Linear motor raises/lowers Ringmaster head. Sol 22 enables motor, Sol 39 controls direction. Callback UpdateRM moves ringmaster.z and collision walls based on position.
- `games/cv.json#/mechanisms/1._vbscript_class`: cvpmMagnet
- `games/cv.json#/mechanisms/1._config`: {"grab_center": true, "size": 200, "solenoid": 3}
- `games/cv.json#/mechanisms/2._vbscript_class`: cvpmMagnet
- `games/cv.json#/mechanisms/2._config`: {"grab_center": true, "size": 200, "solenoid": 5}
- `games/cv.json#/mechanisms/3._vbscript_class`: cvpmMagnet
- `games/cv.json#/mechanisms/3._config`: {"grab_center": false, "size": 100, "solenoid": 35}
- `games/cv.json#/mechanisms/3._note`: Grabs ball at Ringmaster head; custom kick logic on release via SolRingmasterMagnet sub
- `games/cv.json#/mechanisms/4._vbscript_class`: cvpmMagnet
- `games/cv.json#/mechanisms/4._config`: {"grab_center": true}
- `games/cv.json#/mechanisms/4._note`: No solenoid assigned; used for wobble/shake physics on ringmaster head
- `games/cv.json#/mechanisms/5._vbscript_class`: cvpmVLock
- `games/cv.json#/mechanisms/5._config`: {"kick_objects": ["sw66k", "sw67k", "sw68k"], "switches": [66, 67, 68]}
- `games/cv.json#/mechanisms/5._note`: 3-ball virtual lock on upper ramp; released by Lock Post solenoid (16)
- `games/cv.json#/mechanisms/6._vbscript_class`: cvpmBallStack
- `games/cv.json#/mechanisms/6._config`: {"balls": 4, "eject_coil": 9, "switches": [0, 32, 33, 34, 35, 0, 0, 0]}
- `games/cv.json#/mechanisms/7._vbscript_class`: cvpmBallStack
- `games/cv.json#/mechanisms/7._config`: {"eject_coil": 33, "kick_angle": 284, "kick_force": 26, "switches": [0, 36, 0, 0, 0, 0, 0, 0]}
- `games/cv.json#/mechanisms/8._note`: Custom physics simulation; ball launched by Backbox Kicker (sol 2) interacts with spinning disc. Disc has 5 spinner balls for collision detection. Bell at sw11.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.cv`: `games/cv.json` at the pinned migration revision.
