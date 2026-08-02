# Johnny Mnemonic

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1995). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/jm.json#/switches/0._note`: vpmTimer.PulseSw 11 via PlungerKey
- `games/jm.json#/switches/1._note`: cvpmMech AddSw — X axis home position switch at step range 0-2
- `games/jm.json#/switches/2._note`: Controller.Switch(13) toggled via StartGameKey
- `games/jm.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/jm.json#/switches/4._note`: Controller.Switch(15) on/off
- `games/jm.json#/switches/5._note`: Controller.Switch(16) on/off
- `games/jm.json#/switches/6._note`: Controller.Switch(17) on/off
- `games/jm.json#/switches/7._note`: Controller.Switch(18) on/off
- `games/jm.json#/switches/8._note`: Referenced in comments only (sw21)
- `games/jm.json#/switches/9._note`: Controller.Switch(22)=1 on init
- `games/jm.json#/switches/10._note`: Controller.Switch(23) toggled via KeyFront
- `games/jm.json#/switches/11._note`: Controller.Switch(24)=1 on init — always closed switch
- `games/jm.json#/switches/12._note`: PulseSw 25 in RightSlingShot_Slingshot — note: VPX sub name says Right but comment says Left Sling Shot
- `games/jm.json#/switches/13._note`: PulseSw 26 in LeftSlingShot_Slingshot — note: VPX sub name says Left but comment says Right Sling Shot
- `games/jm.json#/switches/14._note`: STHit 27
- `games/jm.json#/switches/15._note`: STHit 28
- `games/jm.json#/switches/16._note`: PulseSw 31 fired during SolRelease (trough eject confirmation)
- `games/jm.json#/switches/17._note`: Ball trough position 1. sw32.kick used by SolRelease.
- `games/jm.json#/switches/18._note`: Ball trough position 2
- `games/jm.json#/switches/19._note`: Ball trough position 3
- `games/jm.json#/switches/20._note`: Ball trough position 4
- `games/jm.json#/switches/21._note`: Controller.Switch(36) set in KickToGlove_hit/unhit. VUK that feeds ball up to glove mechanism.
- `games/jm.json#/switches/22._note`: cvpmMech AddSw — Y axis home position switch at step range 0-1502
- `games/jm.json#/switches/23._note`: PulseSw 38
- `games/jm.json#/switches/24._note`: Controller.Switch(41) on/off
- `games/jm.json#/switches/25._note`: Controller.Switch(42) on/off
- `games/jm.json#/switches/26._note`: DTHit 43 — single drop target
- `games/jm.json#/switches/27._note`: PulseSw 44
- `games/jm.json#/switches/28._note`: PulseSw 45
- `games/jm.json#/switches/29._note`: PulseSw 46
- `games/jm.json#/switches/30._note`: Controller.Switch(47) on/off. Ball lock kicker — CrazyBobKick solenoid ejects.
- `games/jm.json#/switches/31._note`: PulseSw 48 in sw48_spin
- `games/jm.json#/switches/32._note`: Controller.Switch(51)=1 on Matrix11_Hit. 3x3 glove target matrix.
- `games/jm.json#/switches/33._note`: Controller.Switch(52)=1 on Matrix21_Hit
- `games/jm.json#/switches/34._note`: Controller.Switch(53)=1 on Matrix31_Hit
- `games/jm.json#/switches/35._note`: Controller.Switch(54) on/off
- `games/jm.json#/switches/36._note`: Controller.Switch(55) on/off
- `games/jm.json#/switches/37._note`: Controller.Switch(56) on/off
- `games/jm.json#/switches/38._note`: Controller.Switch(57) on/off
- `games/jm.json#/switches/39._note`: Controller.Switch(58) on/off
- `games/jm.json#/switches/40._note`: Controller.Switch(61)=1 on Matrix12_Hit
- `games/jm.json#/switches/41._note`: Controller.Switch(62)=1 on Matrix22_Hit
- `games/jm.json#/switches/42._note`: Controller.Switch(63)=1 on Matrix32_Hit
- `games/jm.json#/switches/43._note`: Controller.Switch(64) on/off
- `games/jm.json#/switches/44._note`: Controller.Switch(65) on/off
- `games/jm.json#/switches/45._note`: Controller.Switch(66) on/off
- `games/jm.json#/switches/46._note`: Controller.Switch(67) toggled via rightmagnasave key
- `games/jm.json#/switches/47._note`: Controller.Switch(68) toggled via leftmagnasave key
- `games/jm.json#/switches/48._note`: Controller.Switch(71)=1 on Matrix13_Hit
- `games/jm.json#/switches/49._note`: Controller.Switch(72)=1 on Matrix23_Hit
- `games/jm.json#/switches/50._note`: Controller.Switch(73)=1 on Matrix33_Hit
- `games/jm.json#/switches/51._note`: cvpmMech AddPulseSwNew — X axis encoder pulse switch (steps 4-9)
- `games/jm.json#/switches/52._note`: cvpmMech AddPulseSwNew — X axis encoder pulse switch (steps 0-5)
- `games/jm.json#/switches/53._note`: cvpmMech AddPulseSwNew — Y axis encoder pulse switch (steps 0-5)
- `games/jm.json#/switches/54._note`: cvpmMech AddPulseSwNew — Y axis encoder pulse switch (steps 4-9)
- `games/jm.json#/switches/55._note`: Controller.Switch(78) on/off
- `games/jm.json#/switches/56._note`: Virtual/opto switch. Controller.Switch(115) set when ball caught by glove magnet (TriggerGloveMag_Hit), cleared on DoHandMagnet off. Extended switch number beyond standard WPC matrix.
- `games/jm.json#/coils/0._vbscript_callback`: SolRelease
- `games/jm.json#/coils/0._inferred_type`: ball_management
- `games/jm.json#/coils/0._note`: Kicks ball from sw32. PulseSw 31 fired as trough jam confirmation.
- `games/jm.json#/coils/1._vbscript_callback`: SolAutofire
- `games/jm.json#/coils/1._inferred_type`: ball_management
- `games/jm.json#/coils/1._note`: Impulse plunger auto-fire. PlungerIM.AutoFire.
- `games/jm.json#/coils/2._vbscript_callback`: SolKickToGlove
- `games/jm.json#/coils/2._inferred_type`: ball_management
- `games/jm.json#/coils/2._note`: VUK that kicks ball up to glove mechanism from below playfield
- `games/jm.json#/coils/3._vbscript_callback`: DoClearMatrix
- `games/jm.json#/coils/3._inferred_type`: mechanism
- `games/jm.json#/coils/3._note`: Clears all balls from 3x3 hand matrix targets. Kicks balls from Matrix kickers.
- `games/jm.json#/coils/4._vbscript_callback`: DoHandMagnet
- `games/jm.json#/coils/4._inferred_type`: mechanism
- `games/jm.json#/coils/4._note`: Glove magnet — picks up ball from matrix targets or holds ball caught at TriggerGloveMag. Clears switch 115 on disable.
- `games/jm.json#/coils/5._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/jm.json#/coils/5._inferred_type`: knocker
- `games/jm.json#/coils/5._note`: Sound-only knocker implementation
- `games/jm.json#/coils/6._inferred_type`: mechanism
- `games/jm.json#/coils/6._note`: Commented out in SolCallback — handled natively by VPX slingshot object
- `games/jm.json#/coils/7._inferred_type`: mechanism
- `games/jm.json#/coils/7._note`: Commented out in SolCallback — handled natively by VPX slingshot object
- `games/jm.json#/coils/8._inferred_type`: mechanism
- `games/jm.json#/coils/8._note`: Commented out in SolCallback — handled natively by VPX bumper object
- `games/jm.json#/coils/9._inferred_type`: mechanism
- `games/jm.json#/coils/9._note`: Commented out in SolCallback — handled natively by VPX bumper object
- `games/jm.json#/coils/10._inferred_type`: mechanism
- `games/jm.json#/coils/10._note`: Commented out in SolCallback — handled natively by VPX bumper object
- `games/jm.json#/coils/11._vbscript_callback`: CrazyBobKick
- `games/jm.json#/coils/11._inferred_type`: ball_management
- `games/jm.json#/coils/11._note`: Ejects ball from Crazy Bob's VUK (switch 47)
- `games/jm.json#/coils/12._vbscript_callback`: ResetDrop
- `games/jm.json#/coils/12._inferred_type`: drop_target_reset
- `games/jm.json#/coils/12._note`: Resets single drop target (sw43)
- `games/jm.json#/coils/13._vbscript_callback`: DropTargetDown
- `games/jm.json#/coils/13._inferred_type`: drop_target_reset
- `games/jm.json#/coils/13._note`: Forces drop target down (sw43)
- `games/jm.json#/coils/14._vbscript_callback`: Flash117
- `games/jm.json#/coils/14._inferred_type`: flasher
- `games/jm.json#/coils/14._note`: SolModCallback with PWM level. Controller.SolMask(1017) for PWM.
- `games/jm.json#/coils/15._vbscript_callback`: Flash118
- `games/jm.json#/coils/15._inferred_type`: flasher
- `games/jm.json#/coils/15._note`: SolModCallback with PWM level. Controller.SolMask(1018) for PWM.
- `games/jm.json#/coils/16._vbscript_callback`: Flash119
- `games/jm.json#/coils/16._inferred_type`: flasher
- `games/jm.json#/coils/16._note`: SolModCallback with PWM level. Controller.SolMask(1019) for PWM.
- `games/jm.json#/coils/17._vbscript_callback`: Flash120
- `games/jm.json#/coils/17._inferred_type`: flasher
- `games/jm.json#/coils/17._note`: SolModCallback with PWM level. Controller.SolMask(1020) for PWM.
- `games/jm.json#/coils/18._inferred_type`: mechanism
- `games/jm.json#/coils/18._note`: Commented out in SolCallback — used internally by cvpmMech (.Sol2=-21 on MoveGloveX). Glove X-axis motor direction.
- `games/jm.json#/coils/19._inferred_type`: mechanism
- `games/jm.json#/coils/19._note`: Commented out in SolCallback — used internally by cvpmMech (.Sol1=22 on MoveGloveX). Glove X-axis motor enable.
- `games/jm.json#/coils/20._inferred_type`: mechanism
- `games/jm.json#/coils/20._note`: Commented out in SolCallback — used internally by cvpmMech (.Sol2=-23 on MoveGloveY). Glove Y-axis motor direction.
- `games/jm.json#/coils/21._inferred_type`: mechanism
- `games/jm.json#/coils/21._note`: Commented out in SolCallback — used internally by cvpmMech (.Sol1=24 on MoveGloveY). Glove Y-axis motor enable.
- `games/jm.json#/coils/22._vbscript_callback`: Flash125
- `games/jm.json#/coils/22._inferred_type`: flasher
- `games/jm.json#/coils/22._note`: SolModCallback with PWM level. Controller.SolMask(1025) for PWM.
- `games/jm.json#/coils/23._vbscript_callback`: Flash126
- `games/jm.json#/coils/23._inferred_type`: flasher
- `games/jm.json#/coils/23._note`: SolModCallback with PWM level. Controller.SolMask(1026) for PWM.
- `games/jm.json#/coils/24._vbscript_callback`: Flash127
- `games/jm.json#/coils/24._inferred_type`: flasher
- `games/jm.json#/coils/24._note`: SolModCallback with PWM level. Controller.SolMask(1027) for PWM.
- `games/jm.json#/coils/25._vbscript_callback`: Flash128
- `games/jm.json#/coils/25._inferred_type`: flasher
- `games/jm.json#/coils/25._note`: SolModCallback with PWM level. Controller.SolMask(1028) for PWM.
- `games/jm.json#/coils/26._vbscript_callback`: SolLeftDiverterHold
- `games/jm.json#/coils/26._inferred_type`: diverter
- `games/jm.json#/coils/26._note`: Hold coil — toggles LeftDiverterOpen/LeftDiverterClosed IsDropped state
- `games/jm.json#/coils/27._vbscript_callback`: SolRightDiverterHold
- `games/jm.json#/coils/27._inferred_type`: diverter
- `games/jm.json#/coils/27._note`: Hold coil — toggles RightDiverterOpen/RightDiverterClosed IsDropped state
- `games/jm.json#/_source/confidence_notes`: High confidence on switches/coils. All switch data extracted from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and inline comments. No Const sw* definitions found — IDs extracted directly from VPX object handlers. Lamp matrix uses vpmMapLights AllLamps (timer-interval-based, no explicit IDs in script — lamps not enumerable from VBS alone). Flashers (coils 17-20, 25-28) use SolModCallback with PWM level. Glove mechanism uses cvpmMech for X/Y motor axes (solenoids 21-24) with encoder switches 74-77 and home switches 12/37. Matrix switches 51-53, 61-63, 71-73 are the 3x3 hand matrix targets. Switch 115 is a virtual/opto switch for glove magnet ball detection. Slingshots (coils 9-10) and bumpers (coils 11-13) are commented out in SolCallback — handled natively by VPX. GI has 5 strings (0-4) via GiCallBack2.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.jm`: `games/jm.json` at the pinned migration revision.
