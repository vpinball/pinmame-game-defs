# Judge Dredd

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/jd.json#/switches/0._note`: Controller.Switch(11) set via LeftMagnaSave key. Used for left plunger lane in Air Raid / Missile mode.
- `games/jd.json#/switches/1._note`: Controller.Switch(12) set via PlungerKey
- `games/jd.json#/switches/2._note`: vpmNudge.TiltSwitch = 14
- `games/jd.json#/switches/3._note`: Kickback / Missile Launcher lane switch. Controller.Switch(15) on/off.
- `games/jd.json#/switches/4._note`: PulseSw 16
- `games/jd.json#/switches/5._note`: PulseSw 17
- `games/jd.json#/switches/6._note`: sw18, sw18a, sw18b all use switch 18. Bank of 3 targets with custom hit IDs 180/181/182 for animation but same ROM switch.
- `games/jd.json#/switches/7._note`: Controller.Switch(22)=1 on init (coin door closed)
- `games/jd.json#/switches/8._note`: STHit 25
- `games/jd.json#/switches/9._note`: Controller.Switch(26) on/off. Reactor lane captive ball.
- `games/jd.json#/switches/10._note`: STHit 27
- `games/jd.json#/switches/11._note`: Controller.Switch(28) set by CraneMag sub. Signals crane has grabbed a ball.
- `games/jd.json#/switches/12._note`: Controller.Switch(31) set via keycode 3
- `games/jd.json#/switches/13._note`: sw67_Hit pulses switch 32 (remapped). Opto at main ramp entrance.
- `games/jd.json#/switches/14._note`: PulseSw 33
- `games/jd.json#/switches/15._note`: PulseSw 34
- `games/jd.json#/switches/16._note`: PulseSw 35
- `games/jd.json#/switches/17._note`: STHit 36
- `games/jd.json#/switches/18._note`: PulseSw 37
- `games/jd.json#/switches/19._note`: PulseSw 38
- `games/jd.json#/switches/20._note`: Controller.Switch(41) on/off
- `games/jd.json#/switches/21._note`: PulseSw 42
- `games/jd.json#/switches/22._note`: PulseSw 43
- `games/jd.json#/switches/23._note`: Controller.Switch(44) set via RightMagnaSave key
- `games/jd.json#/switches/24._note`: PulseSw 51 in LeftSlingShot_Slingshot sub
- `games/jd.json#/switches/25._note`: PulseSw 52 in RightSlingShot_Slingshot sub
- `games/jd.json#/switches/26._note`: Controller.Switch(53) on/off. Reactor lane captive ball.
- `games/jd.json#/switches/27._note`: JUDGE drop target bank — J. DT54 array: sw54, sw54off, sw54prim.
- `games/jd.json#/switches/28._note`: JUDGE drop target bank — U. DT55 array: sw55, sw55off, sw55prim.
- `games/jd.json#/switches/29._note`: JUDGE drop target bank — D. DT56 array: sw56, sw56off, sw56prim.
- `games/jd.json#/switches/30._note`: JUDGE drop target bank — G. DT57 array: sw57, sw57off, sw57prim.
- `games/jd.json#/switches/31._note`: JUDGE drop target bank — E. DT58 array: sw58, sw58off, sw58prim.
- `games/jd.json#/switches/32._note`: Controller.Switch(62) on/off. Critical for tracking balls exiting Deadworld crane.
- `games/jd.json#/switches/33._note`: PulseSw 63
- `games/jd.json#/switches/34._note`: PulseSw 64
- `games/jd.json#/switches/35._note`: PulseSw 65. Comment says 'Not used?'
- `games/jd.json#/switches/36._note`: PulseSw 66
- `games/jd.json#/switches/37._note`: STHit 68
- `games/jd.json#/switches/38._note`: Controller.Switch(71) set/cleared during crane movement. Signals crane is at disc position.
- `games/jd.json#/switches/39._note`: PulseSw 72
- `games/jd.json#/switches/40._note`: bsBotVUK.AddBall. InitSaucer sw73, 73.
- `games/jd.json#/switches/41._note`: bsTopVUK.AddBall. InitSaucer sw74, 74.
- `games/jd.json#/switches/42._note`: PulseSw 75
- `games/jd.json#/switches/43._note`: PulseSw 76
- `games/jd.json#/switches/44._note`: Controller.Switch(77) toggled in FWTimer_Timer. Signals ball in Deadworld slot passing drop position.
- `games/jd.json#/switches/45._note`: Ball trough position 1
- `games/jd.json#/switches/46._note`: Ball trough position 2
- `games/jd.json#/switches/47._note`: Ball trough position 3
- `games/jd.json#/switches/48._note`: Ball trough position 4
- `games/jd.json#/switches/49._note`: Ball trough position 5
- `games/jd.json#/switches/50._note`: Ball trough position 6. sw86.kick used by JDTrough solenoid.
- `games/jd.json#/switches/51._note`: PulseSw 87 fired in JDTrough sub after ball eject. Confirms ball reached shooter lane.
- `games/jd.json#/coils/0._vbscript_callback`: CraneMag
- `games/jd.json#/coils/0._inferred_type`: mechanism
- `games/jd.json#/coils/0._note`: Magnet inside crane arm to grab/release balls
- `games/jd.json#/coils/1._vbscript_callback`: bsBotVUK.SolOut
- `games/jd.json#/coils/1._inferred_type`: ball_management
- `games/jd.json#/coils/1._note`: Bottom (Left) Vertical Up Kicker / Popper. InitSaucer sw73, 73, direction 0, force 100.
- `games/jd.json#/coils/2._vbscript_callback`: bsTopVUK.SolOut
- `games/jd.json#/coils/2._inferred_type`: ball_management
- `games/jd.json#/coils/2._note`: Top (Right) Vertical Up Kicker / Popper. InitSaucer sw74, 74, direction 280, force 50.
- `games/jd.json#/coils/3._vbscript_callback`: CraneArm
- `games/jd.json#/coils/3._inferred_type`: mechanism
- `games/jd.json#/coils/3._note`: Crane arm movement
- `games/jd.json#/coils/4._vbscript_callback`: ResetDrops
- `games/jd.json#/coils/4._inferred_type`: drop_target_reset
- `games/jd.json#/coils/4._note`: Resets J-U-D-G-E drop targets
- `games/jd.json#/coils/5._vbscript_callback`: SolWheelDrive
- `games/jd.json#/coils/5._inferred_type`: mechanism
- `games/jd.json#/coils/5._note`: Rotates Deadworld globe
- `games/jd.json#/coils/6._vbscript_callback`: SolKnocker
- `games/jd.json#/coils/6._inferred_type`: knocker
- `games/jd.json#/coils/7._vbscript_callback`: JDPlunger
- `games/jd.json#/coils/7._inferred_type`: ball_management
- `games/jd.json#/coils/7._note`: Impulse plunger for right shooter lane
- `games/jd.json#/coils/8._vbscript_callback`: KickBack
- `games/jd.json#/coils/8._inferred_type`: ball_management
- `games/jd.json#/coils/8._note`: Kickback / Missile launcher plunger
- `games/jd.json#/coils/9._vbscript_callback`: TripDrop
- `games/jd.json#/coils/9._inferred_type`: drop_target_reset
- `games/jd.json#/coils/9._note`: Drops the center 'D' drop target for certain modes to enable subway
- `games/jd.json#/coils/10._vbscript_callback`: Diverter
- `games/jd.json#/coils/10._inferred_type`: diverter
- `games/jd.json#/coils/11._vbscript_callback`: JDTrough
- `games/jd.json#/coils/11._inferred_type`: ball_management
- `games/jd.json#/coils/11._note`: Kicks ball from sw86 into shooter lane. PulseSw 87 after eject.
- `games/jd.json#/coils/12._vbscript_callback`: SetLamp 117,
- `games/jd.json#/coils/12._inferred_type`: flasher
- `games/jd.json#/coils/13._vbscript_callback`: SetLamp 118,
- `games/jd.json#/coils/13._inferred_type`: flasher
- `games/jd.json#/coils/14._vbscript_callback`: SetLamp 119,
- `games/jd.json#/coils/14._inferred_type`: flasher
- `games/jd.json#/coils/15._vbscript_callback`: SetLamp 120,
- `games/jd.json#/coils/15._inferred_type`: flasher
- `games/jd.json#/coils/16._vbscript_callback`: FlashSol21
- `games/jd.json#/coils/16._inferred_type`: flasher
- `games/jd.json#/coils/16._note`: Custom flash sub with bloom effects. MassAssign(121) commented out — uses FlashSol21 sub instead.
- `games/jd.json#/coils/17._vbscript_callback`: FlashSol22
- `games/jd.json#/coils/17._inferred_type`: flasher
- `games/jd.json#/coils/17._note`: Custom flash sub with bloom effects. MassAssign(122) commented out — uses FlashSol22 sub instead.
- `games/jd.json#/coils/18._vbscript_callback`: SetLamp 123,
- `games/jd.json#/coils/18._inferred_type`: flasher
- `games/jd.json#/coils/19._vbscript_callback`: SetLamp 124,
- `games/jd.json#/coils/19._inferred_type`: flasher
- `games/jd.json#/coils/20._vbscript_callback`: SetLamp 125,
- `games/jd.json#/coils/20._inferred_type`: flasher
- `games/jd.json#/coils/21._vbscript_callback`: FlashSol26
- `games/jd.json#/coils/21._inferred_type`: flasher
- `games/jd.json#/coils/21._note`: Custom flash sub with bloom effects. MassAssign(126) commented out — uses FlashSol26 sub instead.
- `games/jd.json#/coils/22._vbscript_callback`: SetLamp 127,
- `games/jd.json#/coils/22._inferred_type`: flasher
- `games/jd.json#/coils/23._vbscript_callback`: SetLamp 128,
- `games/jd.json#/coils/23._inferred_type`: flasher
- `games/jd.json#/coils/23._note`: No VPX playfield object — backglass only. No MassAssign(128) in script.
- `games/jd.json#/lamps/23._note`: Callback to PinCab_EB button lamp
- `games/jd.json#/lamps/40._note`: Has dual insert (L61 + L61a)
- `games/jd.json#/lamps/56._note`: Decal flash material swap
- `games/jd.json#/lamps/57._note`: Decal flash material swap
- `games/jd.json#/lamps/62._note`: Callback to PinCab_Super button lamp
- `games/jd.json#/lamps/63._note`: Callback to PinCab_Start button lamp
- `games/jd.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, and PulseSw calls. Lamp IDs from Lampz.MassAssign() calls; descriptions inferred from VBScript comments and object names. Flashers (coils 17-28) use SetLamp with 100+ lamp IDs (117-128). Slingshots (coils 15-16) commented out in SolCallback — handled by VPX directly. Trough uses 6 switches (81-86) with a custom implementation (not bsTrough). sw87 is pulsed on trough eject as shooter lane confirmation. Flipper coils use framework constants (sLRFlipper, sLLFlipper, sURFlipper, sULFlipper). Upper flippers present (4-flipper game).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.jd`: `games/jd.json` at the pinned migration revision.
