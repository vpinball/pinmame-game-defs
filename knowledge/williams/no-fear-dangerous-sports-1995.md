# No Fear: Dangerous Sports

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
- `games/nf.json#/switches/0._note`: Controller.Switch(11) set via PlungerKey and LockBarKey
- `games/nf.json#/switches/1._note`: vpmNudge.TiltSwitch = 14
- `games/nf.json#/switches/2._note`: Controller.Switch(15) on/off. Auto plunger (cvpmImpulseP) fires from this switch.
- `games/nf.json#/switches/3._note`: sw16_spin PulseSw 16. Spinner object with sw16_Animate.
- `games/nf.json#/switches/4._note`: Controller.Switch(17) on/off
- `games/nf.json#/switches/5._note`: Controller.Switch(18) on/off
- `games/nf.json#/switches/6._note`: Controller.Switch(22) = 1 on init
- `games/nf.json#/switches/7._note`: Controller.Switch(23) set via keyFront
- `games/nf.json#/switches/8._note`: Controller.Switch(24) = 1 on init. Always closed switch.
- `games/nf.json#/switches/9._note`: Controller.Switch(25) on/off. KickBackIM.AddBall/RemoveBall on hit/unhit.
- `games/nf.json#/switches/10._note`: Controller.Switch(26) on/off
- `games/nf.json#/switches/11._note`: sw27_Slingshot PulseSw 27. Slingshot object with animation timer.
- `games/nf.json#/switches/12._note`: sw28_Slingshot PulseSw 28. Slingshot object with animation timer.
- `games/nf.json#/switches/13._note`: PulseSw 31 fired in ReleaseBall sub after trough eject.
- `games/nf.json#/switches/14._note`: Ball trough position 1. sw32.kick used by ReleaseBall solenoid.
- `games/nf.json#/switches/15._note`: Ball trough position 2
- `games/nf.json#/switches/16._note`: Ball trough position 3
- `games/nf.json#/switches/17._note`: Ball trough position 4
- `games/nf.json#/switches/18._note`: Controller.Switch(37) on/off
- `games/nf.json#/switches/19._note`: Controller.Switch(38) on/off
- `games/nf.json#/switches/20._note`: Controller.Switch(41) on/off. SubwayVUK solenoid ejects from this kicker.
- `games/nf.json#/switches/21._note`: Controller.Switch(42) on/off
- `games/nf.json#/switches/22._note`: PulseSw 46. Opto on jump ramp magnet path.
- `games/nf.json#/switches/23._note`: PulseSw 47. Opto on jump ramp magnet path.
- `games/nf.json#/switches/24._note`: PulseSw 48. Opto on jump ramp magnet path.
- `games/nf.json#/switches/25._note`: DTHit 51. Single drop target with sw51a alternate prim. DropTargetUP (coil 12) and DropTargetDOWN (coil 8).
- `games/nf.json#/switches/26._note`: Controller.Switch(54) on/off
- `games/nf.json#/switches/27._note`: PulseSw 55
- `games/nf.json#/switches/28._note`: STHit 56. Standup target with animation.
- `games/nf.json#/switches/29._note`: STHit 57. Standup target with animation.
- `games/nf.json#/switches/30._note`: PulseSw 58
- `games/nf.json#/switches/31._note`: Controller.Switch(61) on/off. LeftKicker solenoid (coil 15) ejects from this kicker.
- `games/nf.json#/switches/32._note`: PulseSw 62
- `games/nf.json#/switches/33._note`: PulseSw 63
- `games/nf.json#/switches/34._note`: PulseSw 64
- `games/nf.json#/switches/35._note`: PulseSw 66
- `games/nf.json#/switches/36._note`: PulseSw 67
- `games/nf.json#/coils/0._vbscript_callback`: SubwayVUK
- `games/nf.json#/coils/0._inferred_type`: ball_management
- `games/nf.json#/coils/0._note`: Ejects ball from sw41 kicker via KickBall. Ball kicked at angle 135.
- `games/nf.json#/coils/1._vbscript_callback`: SolAutoPlungerIM
- `games/nf.json#/coils/1._inferred_type`: ball_management
- `games/nf.json#/coils/1._note`: cvpmImpulseP auto-fires from sw15 (shooter lane)
- `games/nf.json#/coils/2._vbscript_callback`: Rmag
- `games/nf.json#/coils/2._inferred_type`: magnet
- `games/nf.json#/coils/2._note`: Jump ramp magnet. Affects ball velocity when enabled. VPX object: RightMagnet.
- `games/nf.json#/coils/3._vbscript_callback`: SolKickbackIM
- `games/nf.json#/coils/3._inferred_type`: ball_management
- `games/nf.json#/coils/3._note`: cvpmImpulseP kickback fires from sw25 lane
- `games/nf.json#/coils/4._vbscript_callback`: Cmag
- `games/nf.json#/coils/4._inferred_type`: magnet
- `games/nf.json#/coils/4._note`: Jump ramp magnet. VPX object: CenterMagnet.
- `games/nf.json#/coils/5._vbscript_callback`: Lmag
- `games/nf.json#/coils/5._inferred_type`: magnet
- `games/nf.json#/coils/5._note`: Jump ramp magnet. VPX object: LeftMagnet.
- `games/nf.json#/coils/6._vbscript_callback`: SolKnocker
- `games/nf.json#/coils/6._inferred_type`: knocker
- `games/nf.json#/coils/7._vbscript_callback`: DropTargetDOWN
- `games/nf.json#/coils/7._inferred_type`: drop_target_knock_down
- `games/nf.json#/coils/7._note`: Knocks down drop target at sw51
- `games/nf.json#/coils/8._inferred_type`: unused
- `games/nf.json#/coils/8._note`: Commented out: '9-N.U.
- `games/nf.json#/coils/9._inferred_type`: slingshot
- `games/nf.json#/coils/9._note`: Commented out in SolCallback — handled by VPX directly. VPX object: sw28.
- `games/nf.json#/coils/10._inferred_type`: slingshot
- `games/nf.json#/coils/10._note`: Commented out in SolCallback — handled by VPX directly. VPX object: sw27.
- `games/nf.json#/coils/11._vbscript_callback`: DropTargetUP
- `games/nf.json#/coils/11._inferred_type`: drop_target_reset
- `games/nf.json#/coils/11._note`: Resets drop target at sw51
- `games/nf.json#/coils/12._inferred_type`: unused
- `games/nf.json#/coils/12._note`: Commented out: '13-N.U.
- `games/nf.json#/coils/13._vbscript_callback`: ReleaseBall
- `games/nf.json#/coils/13._inferred_type`: ball_management
- `games/nf.json#/coils/13._note`: Kicks ball from sw32 (trough position 1) and pulses sw31. Custom trough, not bsTrough.
- `games/nf.json#/coils/14._vbscript_callback`: LeftKicker
- `games/nf.json#/coils/14._inferred_type`: ball_management
- `games/nf.json#/coils/14._note`: Ejects ball from sw61 kicker via KickBall. Ball kicked at angle 170.
- `games/nf.json#/coils/15._vbscript_callback`: SolMouth
- `games/nf.json#/coils/15._inferred_type`: mechanism
- `games/nf.json#/coils/15._note`: Controls FlipperJaw (mechanical flipper object). RotateToEnd on enable, RotateToStart on disable. Skull jaw animation.
- `games/nf.json#/coils/16._vbscript_callback`: FlashMod117
- `games/nf.json#/coils/16._inferred_type`: flasher
- `games/nf.json#/coils/16._note`: SolModCallback PWM. Two flashers: f117a, f117b.
- `games/nf.json#/coils/17._vbscript_callback`: FlashMod118
- `games/nf.json#/coils/17._inferred_type`: flasher
- `games/nf.json#/coils/17._note`: SolModCallback PWM. Single flasher with mayo.
- `games/nf.json#/coils/18._vbscript_callback`: FlashMod119
- `games/nf.json#/coils/18._inferred_type`: flasher
- `games/nf.json#/coils/18._note`: SolModCallback PWM. Single flasher with mayo.
- `games/nf.json#/coils/19._vbscript_callback`: FlashMod120
- `games/nf.json#/coils/19._inferred_type`: flasher
- `games/nf.json#/coils/19._note`: SolModCallback PWM.
- `games/nf.json#/coils/20._vbscript_callback`: FlashMod121
- `games/nf.json#/coils/20._inferred_type`: flasher
- `games/nf.json#/coils/20._note`: SolModCallback PWM. f121 initialized to State=0 in Table1_Init.
- `games/nf.json#/coils/21._vbscript_callback`: FlashMod123
- `games/nf.json#/coils/21._inferred_type`: flasher
- `games/nf.json#/coils/21._note`: SolModCallback PWM.
- `games/nf.json#/coils/22._vbscript_callback`: FlashMod124
- `games/nf.json#/coils/22._inferred_type`: flasher
- `games/nf.json#/coils/22._note`: SolModCallback PWM. Single flasher with mayo.
- `games/nf.json#/coils/23._vbscript_callback`: FlashMod125
- `games/nf.json#/coils/23._inferred_type`: flasher
- `games/nf.json#/coils/23._note`: SolModCallback PWM. Two flashers: f125a, f125b.
- `games/nf.json#/coils/24._vbscript_callback`: FlashMod128
- `games/nf.json#/coils/24._inferred_type`: flasher
- `games/nf.json#/coils/24._note`: SolModCallback PWM. f128 initialized to State=0 in Table1_Init.
- `games/nf.json#/lamps/60._note`: Launch button lamp. LaunchButton.blenddisablelighting controlled by state.
- `games/nf.json#/lamps/61._note`: Start button lamp. f88.visible controlled by state.
- `games/nf.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, and PulseSw calls. Lamps identified from VLM BL_inserts_l* arrays (l11-l85) plus l86 (launch button) and l88 (start button). Flashers (coils 17-25, 28) use SolModCallback with PWM. Slingshots (coils 10-11) commented out — handled by VPX directly. Trough is custom (not bsTrough/cvpmTrough): 4 switches (sw32-sw35), ReleaseBall kicks sw32 and pulses sw31. Three magnets (coils 3,5,6) on jump ramps. Skull mouth (coil 16) uses FlipperJaw mechanical flipper object. Flipper coils use framework constants (sLRFlipper=46, sLLFlipper=48, sURFlipper=34).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.nf`: `games/nf.json` at the pinned migration revision.
