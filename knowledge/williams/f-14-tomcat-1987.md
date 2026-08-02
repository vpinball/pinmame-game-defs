# F-14 Tomcat

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1987). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

## Playfield devices

Switch, lamp/GI, and controlled-device candidates are in the adjacent machine definition. Source-specific implementation notes are retained below.

## Custom mechanisms

- `mechanism.beacons`: Rotating Beacons (Backbox) Three rotating beacon lights (red, white, blue) plus F-14 model flames and retractable wings. Animated via BeaconTimer. Real machine uses motor (part 14-7946). [source: legacy.game.f14]
- `mechanism.upper-diverter`: Upper Diverter (Launch Ramp) [source: legacy.game.f14]
- `mechanism.lower-diverter`: Lower Diverter (Launch Ramp) [source: legacy.game.f14]

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

- `games/f14.json#/switches/0._vbscript_name`: swTilt
- `games/f14.json#/switches/0._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/1._vbscript_name`: swBallRollTilt
- `games/f14.json#/switches/1._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/2._vbscript_name`: swStartButton
- `games/f14.json#/switches/2._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/3._vbscript_name`: swCoin3
- `games/f14.json#/switches/3._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/4._vbscript_name`: swCoin2
- `games/f14.json#/switches/4._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/5._vbscript_name`: swCoin1
- `games/f14.json#/switches/5._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/6._vbscript_name`: swSlamTilt
- `games/f14.json#/switches/6._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/7._vbscript_name`: swHiScoreReset
- `games/f14.json#/switches/7._note`: Framework-defined in S11.VBS
- `games/f14.json#/switches/8._vbscript_callback`: sw10_hit / sw10_UnHit
- `games/f14.json#/switches/9._vbscript_callback`: sw11_Hit / sw11_UnHit
- `games/f14.json#/switches/9._note`: Trough position 1 (closest to shooter lane)
- `games/f14.json#/switches/10._vbscript_callback`: sw12_Hit / sw12_UnHit
- `games/f14.json#/switches/10._note`: Trough position 2
- `games/f14.json#/switches/11._vbscript_callback`: sw13_Hit / sw13_UnHit
- `games/f14.json#/switches/11._note`: Trough position 3
- `games/f14.json#/switches/12._vbscript_callback`: sw14_Hit / sw14_UnHit
- `games/f14.json#/switches/12._note`: Trough position 4 (farthest from shooter lane)
- `games/f14.json#/switches/13._vbscript_callback`: Controller.Switch(15) via KeyDown/KeyUp
- `games/f14.json#/switches/13._note`: End-of-stroke switch for right flipper. Directly set via LeftFlipperKey in VBS (reversed per PinMAME convention)
- `games/f14.json#/switches/14._vbscript_callback`: sw16_Hit / sw16_Unhit
- `games/f14.json#/switches/15._vbscript_callback`: sw20_Hit / sw20_Unhit
- `games/f14.json#/switches/16._vbscript_callback`: sw21_Hit / sw21_UnHit
- `games/f14.json#/switches/16._note`: cvpmImpulseP with switch 21 (plungerIM07a)
- `games/f14.json#/switches/17._vbscript_callback`: sw22_Hit / sw22_UnHit
- `games/f14.json#/switches/17._note`: cvpmImpulseP with switch 22 (plungerIM10)
- `games/f14.json#/switches/18._vbscript_callback`: sw23_Hit / sw23_UnHit
- `games/f14.json#/switches/18._note`: cvpmImpulseP with switch 23 (plungerIM05a)
- `games/f14.json#/switches/19._vbscript_callback`: sw24_hit / sw24_unhit
- `games/f14.json#/switches/19._note`: Vertical up-kicker. Animated pUpKicker prim. Kicked by Sol 3 (SolTopHole)
- `games/f14.json#/switches/20._vbscript_callback`: vpmTimer.PulseSw(25)
- `games/f14.json#/switches/21._vbscript_callback`: vpmTimer.PulseSw(26)
- `games/f14.json#/switches/22._vbscript_callback`: vpmTimer.PulseSw(28)
- `games/f14.json#/switches/23._vbscript_callback`: sw30_Hit / sw30_Unhit
- `games/f14.json#/switches/23._note`: Also triggers WireRampOn False
- `games/f14.json#/switches/24._vbscript_callback`: sw31_Hit / sw31_Unhit
- `games/f14.json#/switches/24._note`: Also triggers WireRampOn False
- `games/f14.json#/switches/25._vbscript_callback`: sw32_Hit / sw32_Unhit
- `games/f14.json#/switches/25._note`: Also triggers WireRampOn False
- `games/f14.json#/switches/26._vbscript_callback`: vpmTimer.PulseSw(33)
- `games/f14.json#/switches/27._vbscript_callback`: vpmTimer.PulseSw(34)
- `games/f14.json#/switches/28._vbscript_callback`: vpmTimer.PulseSw(35)
- `games/f14.json#/switches/29._vbscript_callback`: vpmTimer.PulseSw(36)
- `games/f14.json#/switches/30._vbscript_callback`: vpmTimer.PulseSw(37)
- `games/f14.json#/switches/31._vbscript_callback`: vpmTimer.PulseSw(38)
- `games/f14.json#/switches/32._vbscript_callback`: vpmTimer.PulseSw(41)
- `games/f14.json#/switches/33._vbscript_callback`: vpmTimer.PulseSw(42)
- `games/f14.json#/switches/34._vbscript_callback`: vpmTimer.PulseSw(43)
- `games/f14.json#/switches/35._vbscript_callback`: vpmTimer.PulseSw(44)
- `games/f14.json#/switches/36._vbscript_callback`: vpmTimer.PulseSw(45)
- `games/f14.json#/switches/37._vbscript_callback`: vpmTimer.PulseSw(46)
- `games/f14.json#/switches/38._vbscript_callback`: vpmTimer.PulseSw(47)
- `games/f14.json#/switches/39._vbscript_callback`: vpmTimer.PulseSw(48)
- `games/f14.json#/switches/40._vbscript_callback`: vpmTimer.PulseSw(49)
- `games/f14.json#/switches/41._vbscript_callback`: vpmTimer.PulseSw(50)
- `games/f14.json#/switches/42._vbscript_callback`: vpmTimer.PulseSw(51)
- `games/f14.json#/switches/43._vbscript_callback`: vpmTimer.PulseSw(52)
- `games/f14.json#/switches/44._vbscript_callback`: vpmTimer.PulseSw(53)
- `games/f14.json#/switches/45._vbscript_callback`: vpmTimer.PulseSw(54)
- `games/f14.json#/switches/46._vbscript_callback`: sw55_Hit / sw55_unHit
- `games/f14.json#/switches/46._note`: LODKick activated by Sol 12. Yagov kickback lane.
- `games/f14.json#/switches/47._vbscript_callback`: vpmTimer.PulseSw(56)
- `games/f14.json#/switches/48._vbscript_callback`: vpmTimer.PulseSw(57)
- `games/f14.json#/switches/48._note`: Triggered from LeftSlingShot_Slingshot sub
- `games/f14.json#/switches/49._vbscript_callback`: vpmTimer.PulseSw(58)
- `games/f14.json#/switches/49._note`: Triggered from RightSlingShot_Slingshot sub
- `games/f14.json#/switches/50._vbscript_callback`: sw59_Hit / sw59_UnHit
- `games/f14.json#/switches/51._vbscript_callback`: sw60_Hit / sw60_UnHit
- `games/f14.json#/switches/52._vbscript_callback`: sw61_Hit / sw61_unHit
- `games/f14.json#/switches/52._note`: LaserKick activated by Sol 13. Left outlane rescue.
- `games/f14.json#/switches/53._vbscript_callback`: sw62_Hit / sw62_UnHit
- `games/f14.json#/switches/54._vbscript_callback`: Controller.Switch(63) via KeyDown/KeyUp
- `games/f14.json#/switches/54._note`: End-of-stroke switch for left flipper. Directly set via RightFlipperKey in VBS (reversed per PinMAME convention)
- `games/f14.json#/switches/55._vbscript_name`: swURFlip
- `games/f14.json#/switches/55._note`: Framework-defined in S11.VBS. Directly set via flipper key.
- `games/f14.json#/switches/56._vbscript_name`: swLRFlip
- `games/f14.json#/switches/56._note`: Framework-defined in S11.VBS. Directly set via flipper key.
- `games/f14.json#/switches/57._vbscript_name`: swULFlip
- `games/f14.json#/switches/57._note`: Framework-defined in S11.VBS. Directly set via flipper key.
- `games/f14.json#/switches/58._vbscript_name`: swLLFlip
- `games/f14.json#/switches/58._note`: Framework-defined in S11.VBS. Directly set via flipper key.
- `games/f14.json#/coils/0._vbscript_callback`: kisort
- `games/f14.json#/coils/0._inferred_type`: ball_management
- `games/f14.json#/coils/0._note`: Kicks ball from outhole (sw10) back to trough. Manual trough management (no bsTrough helper).
- `games/f14.json#/coils/1._vbscript_callback`: doflyin:Sol02A
- `games/f14.json#/coils/1._inferred_type`: ball_management
- `games/f14.json#/coils/1._note`: Dual callback: doflyin triggers VR F-14 fly-in animation, Sol02A kicks ball from trough (sw11) to shooter lane. Manual trough management.
- `games/f14.json#/coils/2._vbscript_callback`: SolTopHole
- `games/f14.json#/coils/2._inferred_type`: kicker
- `games/f14.json#/coils/2._note`: Vertical up-kicker at sw24. Animated pUpKicker primitive.
- `games/f14.json#/coils/3._vbscript_callback`: Sol05a
- `games/f14.json#/coils/3._inferred_type`: kicker
- `games/f14.json#/coils/3._note`: cvpmImpulseP plungerIM05a, switch 23, kick power 70
- `games/f14.json#/coils/4._vbscript_callback`: vpmSolSound SoundFX("fx_KnockerLouder",DOFKnocker),
- `games/f14.json#/coils/4._inferred_type`: knocker
- `games/f14.json#/coils/5._vbscript_callback`: Sol07A
- `games/f14.json#/coils/5._inferred_type`: kicker
- `games/f14.json#/coils/5._note`: cvpmImpulseP plungerIM07a, switch 21, kick power 75
- `games/f14.json#/coils/6._vbscript_callback`: FlashFL109
- `games/f14.json#/coils/6._inferred_type`: flasher
- `games/f14.json#/coils/6._note`: SolModCallback. PWM flasher. Drives F109 light + ModFlashFlasher 1. Blue color. Top playfield position.
- `games/f14.json#/coils/7._vbscript_callback`: Sol10
- `games/f14.json#/coils/7._inferred_type`: kicker
- `games/f14.json#/coils/7._note`: cvpmImpulseP plungerIM10, switch 22, kick power 70
- `games/f14.json#/coils/8._vbscript_callback`: SetGI
- `games/f14.json#/coils/8._inferred_type`: gi_relay
- `games/f14.json#/coils/8._note`: Controls GILighting collection. System 11 GI on/off relay.
- `games/f14.json#/coils/9._vbscript_callback`: Sol12_Solenoid
- `games/f14.json#/coils/9._inferred_type`: kicker
- `games/f14.json#/coils/9._note`: Enables/disables LODKick wall at sw55. High-speed kickback. Strength adjustable via YagovKick variable.
- `games/f14.json#/coils/10._vbscript_callback`: Sol13_Solenoid
- `games/f14.json#/coils/10._inferred_type`: kicker
- `games/f14.json#/coils/10._note`: Enables/disables LaserKick wall at sw61. Left outlane ball save. Animated pLaserKick primitive.
- `games/f14.json#/coils/11._inferred_type`: relay
- `games/f14.json#/coils/11._note`: No SolCallback in VBS. System 11 A/C relay that multiplexes solenoids 1-8 between 'A' (mechanism) and 'C' (flasher) functions.
- `games/f14.json#/coils/12._vbscript_callback`: FlashFL115
- `games/f14.json#/coils/12._inferred_type`: flasher
- `games/f14.json#/coils/12._note`: SolModCallback. PWM flasher. Drives F115 light + ModFlashFlasher 2. Red color.
- `games/f14.json#/coils/13._vbscript_callback`: SolRotateBeacons
- `games/f14.json#/coils/13._inferred_type`: mechanism
- `games/f14.json#/coils/13._note`: Controls 3 rotating beacon lights (red/white/blue) and F-14 model toy flames/wings. Motor-driven in real machine.
- `games/f14.json#/coils/14._inferred_type`: slingshot
- `games/f14.json#/coils/14._note`: Special solenoid #1. No SolCallback in VBS (auto-fired by VPX).
- `games/f14.json#/coils/15._inferred_type`: slingshot
- `games/f14.json#/coils/15._note`: Special solenoid #2. No SolCallback in VBS (auto-fired by VPX).
- `games/f14.json#/coils/16._inferred_type`: bumper
- `games/f14.json#/coils/16._note`: Special solenoid #4. No SolCallback in VBS (auto-fired by VPX).
- `games/f14.json#/coils/17._vbscript_callback`: Sol21
- `games/f14.json#/coils/17._inferred_type`: diverter
- `games/f14.json#/coils/17._note`: Controls Sol21wall and Diverter1. Init state: dropped (closed). Special solenoid #5.
- `games/f14.json#/coils/18._vbscript_callback`: Sol22
- `games/f14.json#/coils/18._inferred_type`: diverter
- `games/f14.json#/coils/18._note`: Controls Sol22wall and Diverter2. Init state: dropped (closed). Special solenoid #6.
- `games/f14.json#/coils/19._vbscript_callback`: FlashFL101
- `games/f14.json#/coils/19._inferred_type`: flasher
- `games/f14.json#/coils/19._note`: SolModCallback. A/C flasher (shares driver with Sol 1A Outhole). PWM. Drives F101 + ModFlashFlasher 4,10. White color.
- `games/f14.json#/coils/20._vbscript_callback`: FlashFL102
- `games/f14.json#/coils/20._inferred_type`: flasher
- `games/f14.json#/coils/20._note`: SolModCallback. A/C flasher (shares driver with Sol 2A Feeder). PWM. Drives F102 + ModFlashFlasher 8. Red color.
- `games/f14.json#/coils/21._vbscript_callback`: FlashFL103
- `games/f14.json#/coils/21._inferred_type`: flasher
- `games/f14.json#/coils/21._note`: SolModCallback. A/C flasher (shares driver with Sol 3A Popper). PWM. Drives F103 + ModFlashFlasher 7. Red color.
- `games/f14.json#/coils/22._vbscript_callback`: FlashFL104
- `games/f14.json#/coils/22._inferred_type`: flasher
- `games/f14.json#/coils/22._note`: SolModCallback. A/C flasher (shares driver with Sol 4A Spare). PWM. Drives F104 + ModFlashFlasher 14,6. Red color.
- `games/f14.json#/coils/23._vbscript_callback`: FlashFL105
- `games/f14.json#/coils/23._inferred_type`: flasher
- `games/f14.json#/coils/23._note`: SolModCallback. A/C flasher (shares driver with Sol 5A Center Right Eject). PWM. Drives F105 + ModFlashFlasher 13,5. White color.
- `games/f14.json#/coils/24._vbscript_callback`: FlashFL106
- `games/f14.json#/coils/24._inferred_type`: flasher
- `games/f14.json#/coils/24._note`: SolModCallback. A/C flasher (shares driver with Sol 6A Knocker). PWM. Drives F106 + ModFlashFlasher 12,11. Blue color.
- `games/f14.json#/coils/25._vbscript_callback`: FlashFL107
- `games/f14.json#/coils/25._inferred_type`: flasher
- `games/f14.json#/coils/25._note`: SolModCallback. A/C flasher (shares driver with Sol 7A Right Eject). PWM. Drives F107 + ModFlashFlasher 3,9. Red color.
- `games/f14.json#/coils/26._vbscript_callback`: Flash108
- `games/f14.json#/coils/26._inferred_type`: flasher
- `games/f14.json#/coils/26._note`: SolModCallback. A/C flasher (shares driver with Sol 8A Spare). Drives F108/f108a/f108c/f108d. Comment in VBS: 'not sure why 32 works. Service manual says it should be 8.'
- `games/f14.json#/coils/27._vbscript_name`: sURFlipper
- `games/f14.json#/coils/27._vbscript_callback`: SolURFlipper
- `games/f14.json#/coils/27._inferred_type`: flipper
- `games/f14.json#/coils/27._note`: Framework-defined in core.vbs
- `games/f14.json#/coils/28._vbscript_name`: sULFlipper
- `games/f14.json#/coils/28._vbscript_callback`: SolULFlipper
- `games/f14.json#/coils/28._inferred_type`: flipper
- `games/f14.json#/coils/28._note`: Framework-defined in core.vbs
- `games/f14.json#/coils/29._vbscript_name`: sLRFlipper
- `games/f14.json#/coils/29._vbscript_callback`: SolRFlipper
- `games/f14.json#/coils/29._inferred_type`: flipper
- `games/f14.json#/coils/29._note`: Framework-defined in core.vbs
- `games/f14.json#/coils/30._vbscript_name`: sLLFlipper
- `games/f14.json#/coils/30._vbscript_callback`: SolLFlipper
- `games/f14.json#/coils/30._inferred_type`: flipper
- `games/f14.json#/coils/30._note`: Framework-defined in core.vbs
- `games/f14.json#/lamps/0._note`: Center playfield insert
- `games/f14.json#/lamps/1._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/2._note`: Bonus value 1000
- `games/f14.json#/lamps/3._note`: Bonus multiplier lane
- `games/f14.json#/lamps/4._note`: Left rescue kickback indicator
- `games/f14.json#/lamps/5._note`: Center kill target lamp
- `games/f14.json#/lamps/6._note`: Right rescue indicator
- `games/f14.json#/lamps/7._note`: Bottom rescue indicator
- `games/f14.json#/lamps/8._note`: Ball release/lock release lamp
- `games/f14.json#/lamps/9._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/10._note`: Bonus value 2000
- `games/f14.json#/lamps/11._note`: Bonus multiplier lane
- `games/f14.json#/lamps/12._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/13._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/14._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/15._note`: Last-ball safety feature indicator
- `games/f14.json#/lamps/16._note`: Special award lamp (blue insert)
- `games/f14.json#/lamps/17._note`: Kill lane sequence lamp
- `games/f14.json#/lamps/18._note`: Bonus value 4000
- `games/f14.json#/lamps/19._note`: Bonus multiplier lane
- `games/f14.json#/lamps/20._note`: Bonus value 8000
- `games/f14.json#/lamps/21._note`: Bonus value 16000
- `games/f14.json#/lamps/22._note`: Bonus value 32000
- `games/f14.json#/lamps/23._note`: Bonus value 64000. VBS: p24a also animated.
- `games/f14.json#/lamps/24._note`: Shoot again / extra ball indicator
- `games/f14.json#/lamps/25._note`: Extra ball indicator in left bonus multiplier lane
- `games/f14.json#/lamps/26._note`: Bonus multiplier lane
- `games/f14.json#/lamps/27._note`: Bonus multiplier lane
- `games/f14.json#/lamps/28._note`: Bonus multiplier lane
- `games/f14.json#/lamps/29._note`: Bonus multiplier lane
- `games/f14.json#/lamps/30._note`: Bonus multiplier collect
- `games/f14.json#/lamps/31._note`: Landing indicator near ball popper
- `games/f14.json#/lamps/32._note`: TOMCAT target letter - lower left bank
- `games/f14.json#/lamps/33._note`: TOMCAT target letter - lower left bank
- `games/f14.json#/lamps/34._note`: TOMCAT target letter - lower left bank
- `games/f14.json#/lamps/35._note`: TOMCAT target letter - lower right bank
- `games/f14.json#/lamps/36._note`: TOMCAT target letter - lower right bank
- `games/f14.json#/lamps/37._note`: TOMCAT target letter - lower right bank
- `games/f14.json#/lamps/38._note`: Flipper lane indicator. VBS: p39a also animated.
- `games/f14.json#/lamps/39._note`: Lock-on indicator near ball popper
- `games/f14.json#/lamps/40._note`: Center numbered target 3
- `games/f14.json#/lamps/41._note`: Center numbered target 2
- `games/f14.json#/lamps/42._note`: Center numbered target 1
- `games/f14.json#/lamps/43._note`: Center numbered target 4
- `games/f14.json#/lamps/44._note`: Center numbered target 5
- `games/f14.json#/lamps/45._note`: Center numbered target 6
- `games/f14.json#/lamps/46._note`: Flipper lane indicator
- `games/f14.json#/lamps/47._note`: 2000 points spinner lane insert
- `games/f14.json#/lamps/48._note`: TOMCAT target letter - upper left bank
- `games/f14.json#/lamps/49._note`: TOMCAT target letter - upper left bank
- `games/f14.json#/lamps/50._note`: TOMCAT target letter - upper left bank
- `games/f14.json#/lamps/51._note`: TOMCAT target letter - upper right bank
- `games/f14.json#/lamps/52._note`: TOMCAT target letter - upper right bank
- `games/f14.json#/lamps/53._note`: TOMCAT target letter - upper right bank
- `games/f14.json#/lamps/54._note`: Yagov lane indicator
- `games/f14.json#/lamps/55._note`: Spinner value indicator
- `games/f14.json#/lamps/56._note`: Red ramp lock indicator - top. Backbox-style bulb (pfil57/pBulb57 animated).
- `games/f14.json#/lamps/57._note`: Red ramp lock indicator - middle. Backbox-style bulb (pfil58/pBulb58 animated).
- `games/f14.json#/lamps/58._note`: Red ramp lock indicator - lower. Backbox-style bulb (pfil59/pBulb59 animated).
- `games/f14.json#/lamps/59._note`: Green ramp landing indicator - top. Backbox-style bulb (pfil60/pBulb60 animated).
- `games/f14.json#/lamps/60._note`: Green ramp landing indicator - middle. Backbox-style bulb (pfil61/pBulb61 animated).
- `games/f14.json#/lamps/61._note`: Green ramp landing indicator - lower. Backbox-style bulb (pfil62/pBulb62 animated).
- `games/f14.json#/lamps/62._note`: Second Yagov/Line of Death indicator insert
- `games/f14.json#/lamps/63._note`: Extra ball indicator in right bonus multiplier lane
- `games/f14.json#/flashers/0`: Duplicate binding label candidate `Flasher 1C - Yagov White` differs from `Flasher 1C (Yagov White)`.
- `games/f14.json#/flashers/0._color`: white
- `games/f14.json#/flashers/0._vpx_objects`: F101, ModFlashFlasher 4, ModFlashFlasher 10, pFiliment01C
- `games/f14.json#/flashers/1`: Duplicate binding label candidate `Flasher 2C - Left Lane` differs from `Flasher 2C (Left Lane)`.
- `games/f14.json#/flashers/1._color`: red
- `games/f14.json#/flashers/1._vpx_objects`: F102, ModFlashFlasher 8, f102e, f102f, pFiliment02c
- `games/f14.json#/flashers/2`: Duplicate binding label candidate `Flasher 3C - Right Lane` differs from `Flasher 3C (Right Lane)`.
- `games/f14.json#/flashers/2._color`: red
- `games/f14.json#/flashers/2._vpx_objects`: F103, ModFlashFlasher 7, f103e, f103f, pfiliment03c
- `games/f14.json#/flashers/3`: Duplicate binding label candidate `Flasher 4C - Bottom Red` differs from `Flasher 4C (Bottom Red)`.
- `games/f14.json#/flashers/3._color`: red
- `games/f14.json#/flashers/3._vpx_objects`: F104, ModFlashFlasher 14, ModFlashFlasher 6, pFiliment04C
- `games/f14.json#/flashers/4`: Duplicate binding label candidate `Flasher 5C - Bottom White` differs from `Flasher 5C (Bottom White)`.
- `games/f14.json#/flashers/4._color`: white
- `games/f14.json#/flashers/4._vpx_objects`: F105, ModFlashFlasher 13, ModFlashFlasher 5, pFiliment05C
- `games/f14.json#/flashers/5`: Duplicate binding label candidate `Flasher 6C - Bottom Blue` differs from `Flasher 6C (Bottom Blue)`.
- `games/f14.json#/flashers/5._color`: blue
- `games/f14.json#/flashers/5._vpx_objects`: F106, ModFlashFlasher 12, ModFlashFlasher 11, pFiliment06C
- `games/f14.json#/flashers/6`: Duplicate binding label candidate `Flasher 7C - Top White / Top Red Left` differs from `Flasher 7C (Top White / Top Red Left)`.
- `games/f14.json#/flashers/6._color`: red
- `games/f14.json#/flashers/6._vpx_objects`: F107, ModFlashFlasher 3, ModFlashFlasher 9, pFiliment07C, pFiliment07Ca
- `games/f14.json#/flashers/7`: Duplicate binding label candidate `Flasher 8C - Radar` differs from `Flasher 8C (Radar Flasher)`.
- `games/f14.json#/flashers/7._color`: white
- `games/f14.json#/flashers/7._vpx_objects`: F108, f108a, f108c, f108d
- `games/f14.json#/flashers/7._note`: VBS comment: 'not sure why 32 works. Service manual says it should be 8.'
- `games/f14.json#/flashers/8`: Duplicate binding label candidate `Flasher 9 - Top Blue` differs from `Flasher 9 (Top Blue)`.
- `games/f14.json#/flashers/8._color`: blue
- `games/f14.json#/flashers/8._vpx_objects`: F109, ModFlashFlasher 1, pFiliment09
- `games/f14.json#/flashers/9`: Duplicate binding label candidate `Flasher 10 - Top Right Red` differs from `Flasher 10 (Top Right Red)`.
- `games/f14.json#/flashers/9._color`: red
- `games/f14.json#/flashers/9._vpx_objects`: F115, ModFlashFlasher 2
- `games/f14.json#/gi/0._vbscript_callback`: SetGI (Sol 11)
- `games/f14.json#/gi/0._note`: Single GI string controlled by solenoid 11 (GI relay). Uses GILighting and GIBulbs collections. GI001_animate handles PWM dimming of GI bulbs, ramp plastics, and clear plastics.
- `games/f14.json#/mechanisms/0._note`: Three rotating beacon lights (red, white, blue) plus F-14 model flames and retractable wings. Animated via BeaconTimer. Real machine uses motor (part 14-7946).
- `games/f14.json#/mechanisms/1._vpx_objects`: Sol21wall, Diverter1, pDiverter1
- `games/f14.json#/mechanisms/2._vpx_objects`: Sol22wall, Diverter2, pDiverter2
- `games/f14.json#/_source/confidence_notes`: High confidence on switches and coils from VBS + manual. Lamp descriptions reconstructed from manual OCR (garbled) cross-referenced with game adjustment text and known gameplay. Lamps L57-L62 have backbox bulb/filament treatment in VBS. System 11 A/C relay (sol 14) splits solenoids 1-8 between 'A' (mechanisms) and 'C' (flashers) sides. Flipper solenoid IDs (sLRFlipper=46, sLLFlipper=48, sURFlipper=34, sULFlipper=36) come from core.vbs. VPX table uses manual trough management (not bsTrough helper). SolCallback(2) uses dual-callback syntax 'doflyin:Sol02A'.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.f14`: `games/f14.json` at the pinned migration revision.
