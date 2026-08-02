# The Machine: Bride of Pinbot

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1991). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/bop.json#/switches/0._note`: Set via Controller.Switch(11) in Table1_KeyDown/KeyUp on RightFlipperKey
- `games/bop.json#/switches/1._note`: Set via Controller.Switch(12) in Table1_KeyDown/KeyUp on LeftFlipperKey
- `games/bop.json#/switches/2._note`: vpmNudge.TiltSwitch = 14
- `games/bop.json#/switches/3._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/4._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/5._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/6._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/7._note`: Top trough switch closest to shooter lane. CreateSizedballWithMass at init. Trough exit — kicked by solenoid 2.
- `games/bop.json#/switches/8._note`: Middle trough switch. CreateSizedballWithMass at init.
- `games/bop.json#/switches/9._note`: Bottom trough switch (drain end). CreateSizedballWithMass at init.
- `games/bop.json#/switches/10._note`: PulseSw 28 from sw28_Hit. Drop target with animation.
- `games/bop.json#/switches/11._note`: Hit/UnHit rollover switch. Also used as plungerIM.switch for impulse plunger.
- `games/bop.json#/switches/12._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/13._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/14._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/15._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/16._note`: PulseSw 36 from sw36_Hit. Drop target with animation.
- `games/bop.json#/switches/17._note`: PulseSw 37 from sw37_Hit. Drop target with animation.
- `games/bop.json#/switches/18._note`: Set via controller.switch(38) in Drain_hit. Cleared by kisort (solenoid 1).
- `games/bop.json#/switches/19._note`: PulseSw 41 from sw41_Hit
- `games/bop.json#/switches/20._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/21._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/22._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/23._note`: Hit/UnHit kicker switch. Ejected by solenoid 3 (SolKickout).
- `games/bop.json#/switches/24._note`: PulseSw 47 from sw47_Hit
- `games/bop.json#/switches/25._note`: PulseSw 51 from sw51_Spin sub
- `games/bop.json#/switches/26._note`: Hit/UnHit rollover switch
- `games/bop.json#/switches/27._note`: PulseSw 53 from Bumper1_Hit
- `games/bop.json#/switches/28._note`: PulseSw 54 from Bumper3_Hit
- `games/bop.json#/switches/29._note`: PulseSw 55 from Bumper2_Hit
- `games/bop.json#/switches/30._note`: PulseSw 56 from UpperSlingShot_Slingshot
- `games/bop.json#/switches/31._note`: PulseSw 57 from LeftSlingShot_Slingshot
- `games/bop.json#/switches/32._note`: PulseSw 58 from RightSlingShot_Slingshot
- `games/bop.json#/switches/33._note`: Controller.Switch(63) set in sw63x_Hit. Enabled only when currentFace=2. Ejected by solenoid 15 (KickLeftEye).
- `games/bop.json#/switches/34._note`: Controller.Switch(64) set in sw64x_Hit. Enabled only when currentFace=2. Ejected by solenoid 16 (KickRightEye).
- `games/bop.json#/switches/35._note`: Controller.Switch(65) set in sw65x_Hit. Enabled only when currentFace=1. Ejected by solenoid 8 (KickMouth).
- `games/bop.json#/switches/36._note`: Mechanism switch. Set to TRUE when currentFace is 1, 2, or 3 (faces that close the switch). Managed by HeadMechCallback. Set to 1 on init.
- `games/bop.json#/switches/37._note`: Hit/UnHit switch
- `games/bop.json#/switches/38._note`: Hit/UnHit switch. LockWall dropped/raised on hit/unhit.
- `games/bop.json#/switches/39._note`: PulseSw 73 from sw73_Hit
- `games/bop.json#/switches/40._note`: PulseSw 74 from sw74_Hit
- `games/bop.json#/switches/41._note`: PulseSw 75 from sw75_Hit
- `games/bop.json#/switches/42._note`: PulseSw 76 from sw76_Hit
- `games/bop.json#/switches/43._note`: PulseSw 77 from sw77_Hit
- `games/bop.json#/switches/44._note`: PulseSw 100 from multiple wall_Hit subs (wall69, wall75, wall77, wall79, wall80, wall81, wall82, wall83, wall84). Likely mapped in WPC switch matrix extension or opto group.
- `games/bop.json#/coils/0._vbscript_callback`: kisort
- `games/bop.json#/coils/0._inferred_type`: coil
- `games/bop.json#/coils/0._note`: Kicks ball from Drain kicker. Clears switch 38.
- `games/bop.json#/coils/1._vbscript_callback`: KickBallToLane
- `games/bop.json#/coils/1._inferred_type`: coil
- `games/bop.json#/coils/1._note`: Kicks ball from trough to shooter lane.
- `games/bop.json#/coils/2._vbscript_callback`: SolKickout
- `games/bop.json#/coils/2._inferred_type`: coil
- `games/bop.json#/coils/2._note`: Ejects ball from scoop kicker (switch 46).
- `games/bop.json#/coils/3._vbscript_callback`: SolGate3
- `games/bop.json#/coils/3._inferred_type`: coil
- `games/bop.json#/coils/3._note`: Controls Gate3 diverter via vpmSolGate.
- `games/bop.json#/coils/4._vbscript_callback`: SolSS
- `games/bop.json#/coils/4._inferred_type`: coil
- `games/bop.json#/coils/4._note`: Auto-fires impulse plunger for skill shot.
- `games/bop.json#/coils/5._vbscript_callback`: solBallLockPost
- `games/bop.json#/coils/5._inferred_type`: coil
- `games/bop.json#/coils/5._note`: Drops/raises ball lock post (BL wall).
- `games/bop.json#/coils/6._vbscript_callback`: KnockerSolenoid
- `games/bop.json#/coils/6._inferred_type`: coil
- `games/bop.json#/coils/6._note`: Cabinet knocker solenoid. Sound only in VPX.
- `games/bop.json#/coils/7._vbscript_callback`: KickMouth
- `games/bop.json#/coils/7._inferred_type`: coil
- `games/bop.json#/coils/7._note`: Ejects ball from mouth (switch 65, Face 1). Launches ball upward.
- `games/bop.json#/coils/8._vbscript_callback`: KickLeftEye
- `games/bop.json#/coils/8._inferred_type`: coil
- `games/bop.json#/coils/8._note`: Ejects ball from left eye (switch 63, Face 2). Launches ball upward.
- `games/bop.json#/coils/9._vbscript_callback`: KickRightEye
- `games/bop.json#/coils/9._inferred_type`: coil
- `games/bop.json#/coils/9._note`: Ejects ball from right eye (switch 64, Face 2). Launches ball upward.
- `games/bop.json#/coils/10._vbscript_callback`: SetLamp 117,
- `games/bop.json#/coils/10._inferred_type`: flasher
- `games/bop.json#/coils/10._note`: Routes to Lampz lamp 117. Uses SolModCallBack for PWM when UsePinmameModulatedSolenoids=true.
- `games/bop.json#/coils/11._vbscript_callback`: SolFlashLR
- `games/bop.json#/coils/11._inferred_type`: flasher
- `games/bop.json#/coils/11._note`: Left ramp flasher. Custom fading sub. Backglass: Left SpaceShip.
- `games/bop.json#/coils/12._vbscript_callback`: SetLamp 119,
- `games/bop.json#/coils/12._inferred_type`: flasher
- `games/bop.json#/coils/12._note`: Routes to Lampz lamp 119. Backglass: Jackpot. Uses SolModCallBack for PWM.
- `games/bop.json#/coils/13._vbscript_callback`: SolFlashSK
- `games/bop.json#/coils/13._inferred_type`: flasher
- `games/bop.json#/coils/13._note`: Skill shot flasher. Custom fading sub. Backglass: Heart.
- `games/bop.json#/coils/14._vbscript_callback`: SetProcRedDome1
- `games/bop.json#/coils/14._inferred_type`: flasher
- `games/bop.json#/coils/14._note`: Left helmet dome flasher. Uses SolModCallBack SetRedDome1 for PWM. Backglass: Face.
- `games/bop.json#/coils/15._vbscript_callback`: SetProcRedDome2
- `games/bop.json#/coils/15._inferred_type`: flasher
- `games/bop.json#/coils/15._note`: Right helmet dome flasher. Uses SolModCallBack SetRedDome2 for PWM. Backglass: Bottom Right.
- `games/bop.json#/coils/16._vbscript_callback`: SetProcRedDome4
- `games/bop.json#/coils/16._inferred_type`: flasher
- `games/bop.json#/coils/16._note`: Jets entrance dome flasher. Uses SolModCallBack SetRedDome4 for PWM. Backglass: Title Left.
- `games/bop.json#/coils/17._vbscript_callback`: SetProcRedDome3
- `games/bop.json#/coils/17._inferred_type`: flasher
- `games/bop.json#/coils/17._note`: Left loop dome flasher. Uses SolModCallBack SetRedDome3 for PWM. Backglass: Title Right.
- `games/bop.json#/coils/18._vbscript_callback`: motor_dir
- `games/bop.json#/coils/18._inferred_type`: mechanism
- `games/bop.json#/coils/18._note`: PROC-only SolCallback. Controls head rotation direction. Non-PROC uses cvpmMyMech.Sol2=27.
- `games/bop.json#/coils/19._vbscript_callback`: motor_sol
- `games/bop.json#/coils/19._inferred_type`: mechanism
- `games/bop.json#/coils/19._note`: PROC-only SolCallback. Drives head motor on/off. Non-PROC uses cvpmMyMech.Sol1=28.
- `games/bop.json#/coils/20._vbscript_callback`: FlipperRelay
- `games/bop.json#/coils/20._inferred_type`: coil
- `games/bop.json#/coils/20._note`: PROC-only SolCallback. Enables/disables flippers. Non-PROC handles flipper enable via PinMAME framework.
- `games/bop.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/bop.json#/coils/21._inferred_type`: coil
- `games/bop.json#/coils/21._note`: Framework constant sLRFlipper=46 from core.vbs/WPC.VBS. Custom sub handles nFozzy flipper physics.
- `games/bop.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/bop.json#/coils/22._inferred_type`: coil
- `games/bop.json#/coils/22._note`: Framework constant sLLFlipper=48 from core.vbs/WPC.VBS. Custom sub handles nFozzy flipper physics.
- `games/bop.json#/lamps/48._note`: VR room backglass lamp
- `games/bop.json#/lamps/49._note`: VR room backglass lamp
- `games/bop.json#/lamps/50._note`: VR room backglass lamp
- `games/bop.json#/lamps/51._note`: VR room backglass lamp
- `games/bop.json#/lamps/52._note`: VR room backglass lamp
- `games/bop.json#/lamps/53._note`: VR room backglass lamp
- `games/bop.json#/lamps/54._note`: VR room backglass lamp
- `games/bop.json#/lamps/55._note`: VR room backglass lamp
- `games/bop.json#/lamps/56._note`: VR room backglass lamp
- `games/bop.json#/lamps/57._note`: VR room backglass lamp
- `games/bop.json#/lamps/58._note`: VR room backglass lamp
- `games/bop.json#/lamps/59._note`: VR room backglass lamp
- `games/bop.json#/lamps/60._note`: VR room backglass lamp
- `games/bop.json#/lamps/61._note`: Lampz.MassAssign only, no callback
- `games/bop.json#/lamps/62._note`: Lampz.MassAssign only, no callback
- `games/bop.json#/lamps/63._note`: Lampz.MassAssign only, no callback
- `games/bop.json#/lamps/80._note`: Driven by solenoid 17 via SetLamp/Lampz
- `games/bop.json#/lamps/81._note`: Driven by solenoid 19 via SetLamp/Lampz
- `games/bop.json#/gi/0._note`: ModLampz GI string 2. Maps to Lampz index 112 in non-modulated mode. GIRear collection. Includes DecalHeart1 material color fade.
- `games/bop.json#/gi/1._note`: ModLampz GI string 4. Maps to Lampz index 114 in non-modulated mode. GIFront collection + AmbientOverhead.
- `games/bop.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions in script — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and trough init. Custom nFozzy trough (not cvpmTrough) with 3 balls at sw27/sw26/sw25(ballrelease). Head mechanism uses cvpmMyMech with sol 27 (direction) and sol 28 (motor), switch 67 (head position). Solenoids 17-24 are flashers — 17 (Billions) and 19 (Jackpot) route through SetLamp to Lampz; 18 (left ramp) and 20 (skill shot) use custom flash subs; 21-24 are dome flashers on the helmet. Solenoids 27/28 are head motor (PROC only via SolCallback, non-PROC uses cvpmMyMech). Solenoid 40 (FlipperRelay) is PROC-only. Flipper coils use framework constants (sLRFlipper=46, sLLFlipper=48 from core.vbs). Cabinet flipper switches 11/12 set directly in KeyDown/KeyUp. UseSolenoids=2 (FastFlips), UseLamps=0, UseSync=1. Script supports both PinMAME and PROC modes. Lamp assignments from Lampz.MassAssign — comprehensive coverage of inserts 11-68, helmet/backglass lamps 71-88, GI at 91-108. Backglass body lamps 71-78 and 81-85 are VR-only. Switch 100 is rubber band impact sensor (PulseSw 100 from multiple wall_Hit subs).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.bop`: `games/bop.json` at the pinned migration revision.
